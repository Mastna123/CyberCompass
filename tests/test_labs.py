"""Smoke tests for the lab pages and the attempt API.

Run from the repo root:  python -m unittest discover tests -v
Checks that every lab page loads, every lab has exactly one safe choice,
and Flask scores tries correctly. No browser or server needed.
"""
import os
import sys
import unittest

# app/ isn't a package, so put it on the path the same way Flask does when run from app/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app  # noqa: E402
import data  # noqa: E402
import lab_content  # noqa: E402


class LabPagesTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_loads(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_home_lists_every_assigned_lab(self):
        """Assigned to you shows all assigned labs, including the one in Next due."""
        page = self.client.get("/").get_data(as_text=True)
        assigned = [lab for lab in data.LABS if lab["assigned"] and lab["status"] != "done"]
        self.assertTrue(assigned, "demo data should have at least one assigned lab")
        # The first one shows in Next due and in the list, so it appears at least twice
        self.assertGreaterEqual(page.count(assigned[0]["title"]), 2)
        for lab in assigned:
            self.assertIn(lab["title"], page)

    def test_library_shows_every_lab(self):
        page = self.client.get("/labs").get_data(as_text=True)
        self.assertIn(f"{len(data.LABS)} labs", page)

    def test_every_lab_overview_and_player_load(self):
        for lab in data.LABS:
            with self.subTest(lab=lab["title"]):
                self.assertEqual(self.client.get(f"/labs/{lab['id']}").status_code, 200)
                self.assertEqual(self.client.get(f"/labs/{lab['id']}/play").status_code, 200)

    def test_empty_track_says_coming_soon(self):
        """A track with no labs yet shows "Coming soon" instead of 0/0."""
        empty = [t for t in data.TRACKS if not any(lab["track"] == t["id"] for lab in data.LABS)]
        if not empty:
            self.skipTest("every track has labs now")
        home = self.client.get("/").get_data(as_text=True)
        self.assertIn("Coming soon", home)
        self.assertNotIn("0/0", home)
        library = self.client.get(f"/labs?track={empty[0]['id']}").get_data(as_text=True)
        self.assertIn("Labs for this track are coming soon.", library)

    def test_filters_with_no_match_keep_normal_message(self):
        page = self.client.get("/labs?track=identity&status=in_progress").get_data(as_text=True)
        self.assertIn("No labs match these filters.", page)
        self.assertNotIn("coming soon", page)

    def test_missing_lab_is_404(self):
        self.assertEqual(self.client.get("/labs/9999").status_code, 404)
        self.assertEqual(self.client.get("/labs/9999/play").status_code, 404)


class LabContentTest(unittest.TestCase):
    def test_content_ids_match_labs(self):
        """Every content block belongs to a real lab, so none is silently ignored."""
        lab_ids = {lab["id"] for lab in data.LABS}
        self.assertEqual(set(lab_content.LAB_CONTENT) - lab_ids, set())

    def test_exactly_one_safe_choice(self):
        """Checks both tries: the main choices and any lab's own retry_choices."""
        for lab in data.LABS:
            full_lab = data.get_lab(lab["id"])
            for try_number in (1, 2):
                with self.subTest(lab=lab["title"], try_number=try_number):
                    choices = data.choices_for_try(full_lab, try_number)
                    self.assertEqual(len([c for c in choices if c["safe"]]), 1)
                    keys = [c["key"] for c in choices]
                    self.assertEqual(len(keys), len(set(keys)), "choice keys must be unique")

    def test_every_lab_has_role_groups(self):
        allowed = {"Everyone", *data.ROLE_GROUPS}
        for lab in data.LABS:
            with self.subTest(lab=lab["title"]):
                self.assertTrue(lab.get("role_groups"))
                self.assertLessEqual(set(lab["role_groups"]), allowed)

    def test_role_groups_match_the_contract(self):
        self.assertEqual(data.ROLE_GROUPS, ["Leadership", "Management", "Office staff", "Frontline staff"])


class RolesTest(unittest.TestCase):
    def test_current_user_has_valid_role_and_group(self):
        self.assertIn(data.CURRENT_USER["role"], data.PERMISSION_ROLES)
        self.assertIn(data.CURRENT_USER["role_group"], data.ROLE_GROUPS)

    def test_is_admin(self):
        self.assertTrue(data.is_admin({"role": "admin"}))
        self.assertFalse(data.is_admin({"role": "learner"}))

    def test_home_shows_role_and_group(self):
        page = app.test_client().get("/").get_data(as_text=True)
        self.assertIn(data.PERMISSION_ROLES[data.CURRENT_USER["role"]], page)
        self.assertIn(data.CURRENT_USER["role_group"], page)

    def test_no_dashes_in_learner_text(self):
        """Team writing rule: no em or en dashes in anything learners read."""
        path = lab_content.__file__
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertNotIn("—", text)
        self.assertNotIn("–", text)


class CleanStateTest(unittest.TestCase):
    """Starts each test with no saved progress or tries, and puts the demo data back after."""

    def setUp(self):
        self.client = app.test_client()
        self.saved_progress = dict(data.PROGRESS)
        self.saved_attempts = list(data.ATTEMPTS)
        data.PROGRESS.clear()
        data.ATTEMPTS.clear()
        self.lab_id = data.LABS[0]["id"]

    def tearDown(self):
        data.PROGRESS.clear()
        data.PROGRESS.update(self.saved_progress)
        data.ATTEMPTS[:] = self.saved_attempts


class ResumeTest(CleanStateTest):
    """Resume opens the lab player at the stage the learner reached."""

    def save_stage(self, stage, lab_id=None):
        return self.client.post(f"/api/labs/{lab_id or self.lab_id}/progress", json={"stage": stage})

    def play_page(self):
        return self.client.get(f"/labs/{self.lab_id}/play").get_data(as_text=True)

    def test_new_lab_starts_at_learn(self):
        self.assertIn('data-start-stage="learn"', self.play_page())

    def test_player_opens_at_saved_stage(self):
        self.assertEqual(self.save_stage("control").status_code, 200)
        self.assertIn('data-start-stage="control"', self.play_page())
        self.assertIn("Step 3 of 4", self.client.get("/").get_data(as_text=True))

    def test_result_stage_without_first_try_falls_back(self):
        self.save_stage("result")
        self.assertIn('data-start-stage="decide"', self.play_page())

    def test_result_stage_shows_saved_first_try(self):
        safe_key = next(c["key"] for c in data.get_lab(self.lab_id)["choices"] if c["safe"])
        self.client.post(f"/api/labs/{self.lab_id}/attempts", json={"choice": safe_key, "try_number": 1})
        self.save_stage("result")
        page = self.play_page()
        self.assertIn('data-start-stage="result"', page)
        self.assertIn('id="result-safe" >', page)
        
    def test_rejects_bad_stage(self):
        url = f"/api/labs/{self.lab_id}/progress"
        self.assertEqual(self.save_stage("finished").status_code, 400)
        self.assertEqual(self.client.post(url, json={}).status_code, 400)
        self.assertEqual(self.client.post(url, json={"stage": ["learn"]}).status_code, 400)
        self.assertEqual(self.client.post(url, json=["learn"]).status_code, 400)
        self.assertEqual(self.save_stage("learn", lab_id=9999).status_code, 404)

    def test_resume_card_without_time_left_has_no_stray_dot(self):
        """Labs other than the demo have no time_left, so the line must end at "of 4"."""
        lab = next(l for l in data.LABS if not l.get("time_left"))
        self.save_stage("control", lab_id=lab["id"])
        self.assertIn("Step 3 of 4</div>", self.client.get("/").get_data(as_text=True))

    def test_home_resumes_most_recent_lab(self):
        first, second = data.LABS[0], data.LABS[1]
        self.save_stage("control", lab_id=second["id"])
        self.save_stage("decide", lab_id=first["id"])
        self.assertEqual(data.resume_lab_id(), first["id"])
        data.PROGRESS[(data.CURRENT_USER["id"], second["id"])]["updated_at"] = "9999-01-01T00:00:00"
        self.assertEqual(data.resume_lab_id(), second["id"])
        self.assertIn("Step 3 of 4", self.client.get("/").get_data(as_text=True))

    def test_second_try_clears_progress(self):
        self.save_stage("retry")
        self.client.post(f"/api/labs/{self.lab_id}/attempts", json={"choice": "A", "try_number": 2})
        self.assertFalse(data.has_progress(self.lab_id))
        self.assertNotIn("Pick up where you left off", self.client.get("/").get_data(as_text=True))


class RetryTest(CleanStateTest):
    """Try it again shuffles and re-letters the choices so learners can't just click the letter they missed."""

    def test_shuffle_never_hangs_on_bad_content(self):
        """Content with no safe choice is caught by LabContentTest; it must not freeze the page."""
        no_safe = [{"key": k, "label": k, "safe": False} for k in "ABCD"]
        self.assertEqual(len(data.shuffled_retry_choices({"choices": no_safe})), 4)
        all_safe = [{"key": k, "label": k, "safe": True} for k in "ABCD"]
        self.assertEqual(len(data.shuffled_retry_choices({"choices": all_safe})), 4)
        all_safe_retry = {"choices": no_safe[:1] + all_safe[1:], "retry_choices": all_safe}
        self.assertEqual(len(data.shuffled_retry_choices(all_safe_retry)), 4)
        one = [{"key": "A", "label": "A", "safe": True}]
        self.assertEqual(data.shuffled_retry_choices({"choices": one})[0]["letter"], "A")

    def test_shuffle_keeps_choices_and_reletters(self):
        lab = data.get_lab(self.lab_id)
        for _ in range(20):   # shuffling is random, so check it several times
            shuffled = data.shuffled_retry_choices(lab)
            self.assertEqual({c["key"] for c in shuffled}, {c["key"] for c in lab["choices"]})
            self.assertEqual([c["letter"] for c in shuffled], ["A", "B", "C", "D"])
            self.assertNotEqual([c["key"] for c in shuffled], [c["key"] for c in lab["choices"]])
            safe_letter = next(c["letter"] for c in shuffled if c["safe"])
            first_try_safe_key = next(c["key"] for c in lab["choices"] if c["safe"])
            self.assertNotEqual(safe_letter, first_try_safe_key, "safe answer must move")

    def test_try_two_uses_lab_retry_choices(self):
        """If a lab has its own retry_choices, try 2 is scored against those."""
        retry = [
            {"key": "A", "label": "Retry safe", "safe": True},
            {"key": "E", "label": "Retry unsafe", "safe": False},
        ]
        content = lab_content.LAB_CONTENT.setdefault(self.lab_id, {})
        content["retry_choices"] = retry
        try:
            page = self.client.get(f"/labs/{self.lab_id}/play").get_data(as_text=True)
            self.assertIn("Retry safe", page)
            post = lambda body: self.client.post(f"/api/labs/{self.lab_id}/attempts", json=body)
            self.assertTrue(post({"choice": "A", "try_number": 2}).get_json()["safe"])
            self.assertFalse(post({"choice": "E", "try_number": 2}).get_json()["safe"])
            self.assertEqual(post({"choice": "E", "try_number": 1}).status_code, 400)
        finally:
            del content["retry_choices"]

class ResultTest(CleanStateTest):
    """After a try, the learner sees the result for the exact choice they made."""

    def post(self, body):
        return self.client.post(f"/api/labs/{self.lab_id}/attempts", json=body)

    def test_each_choice_returns_its_own_result(self):
        lab = data.get_lab(self.lab_id)
        for choice in lab["choices"]:
            with self.subTest(choice=choice["key"]):
                result = self.post({"choice": choice["key"], "try_number": 1}).get_json()["result"]
                expected = choice.get("result") or (lab["result_safe"] if choice["safe"] else lab["result_unsafe"])
                self.assertEqual(result, expected)
                self.assertTrue(result)

    def test_falls_back_to_general_message(self):
        """A lab without per-choice results still gets the general safe or unsafe text."""
        lab = data.get_lab(data.LABS[1]["id"])
        unsafe = next(c for c in lab["choices"] if not c["safe"])
        self.assertNotIn("result", unsafe)
        r = self.client.post(f"/api/labs/{lab['id']}/attempts", json={"choice": unsafe["key"], "try_number": 1})
        self.assertEqual(r.get_json()["result"], lab["result_unsafe"])

    def test_resume_shows_saved_result(self):
        lab = data.get_lab(self.lab_id)
        unsafe = next(c for c in lab["choices"] if not c["safe"] and c.get("result"))
        self.post({"choice": unsafe["key"], "try_number": 1})
        self.client.post(f"/api/labs/{self.lab_id}/progress", json={"stage": "result"})
        page = self.client.get(f"/labs/{self.lab_id}/play").get_data(as_text=True)
        self.assertIn(unsafe["result"].replace("'", "&#39;"), page)

    def test_result_text_not_in_page_before_answering(self):
        """Results only show up after a try, so they can't give the answer away."""
        page = self.client.get(f"/labs/{self.lab_id}/play").get_data(as_text=True)
        for choice in data.get_lab(self.lab_id)["choices"]:
            if choice.get("result"):
                self.assertNotIn(choice["result"].replace("'", "&#39;"), page)

class FeedbackTest(CleanStateTest):
    """The learner can tell right away if they got it right, and the overview shows where they are."""

    def test_second_try_says_safe_choice(self):
        """Once the lab is over, a wrong second try names the safe choice."""
        lab = data.get_lab(self.lab_id)
        retry = data.choices_for_try(lab, 2)
        safe = next(c for c in retry if c["safe"])
        unsafe = next(c for c in retry if not c["safe"])
        self.client.post(f"/api/labs/{self.lab_id}/attempts", json={"choice": unsafe["key"], "try_number": 1})
        body = self.client.post(f"/api/labs/{self.lab_id}/attempts", json={"choice": unsafe["key"], "try_number": 2}).get_json()
        self.assertFalse(body["safe"])
        self.assertEqual(body["safe_label"], safe["label"])

    def test_first_try_never_reveals_safe_choice(self):
        """Naming the safe choice after try 1 would give away Try it again, so it's left out everywhere."""
        lab = data.get_lab(self.lab_id)
        unsafe = next(c for c in lab["choices"] if not c["safe"])
        body = self.client.post(f"/api/labs/{self.lab_id}/attempts", json={"choice": unsafe["key"], "try_number": 1}).get_json()
        self.assertNotIn("safe_label", body)
        # Resumed at "What happened": the page still doesn't name it
        self.client.post(f"/api/labs/{self.lab_id}/progress", json={"stage": "result"})
        page = self.client.get(f"/labs/{self.lab_id}/play").get_data(as_text=True)
        self.assertNotIn("result-safe-label", page)
        self.assertNotIn("The safe choice was", page.split('data-stage="retry-result"')[0])

    def test_safe_label_not_in_page_before_answering(self):
        page = self.client.get(f"/labs/{self.lab_id}/play").get_data(as_text=True)
        self.assertIn('<strong id="retry-safe-label"></strong>', page)

class AttemptApiTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post(self, lab_id, body):
        return self.client.post(f"/api/labs/{lab_id}/attempts", json=body)

    def test_flask_scores_each_choice(self):
        for lab in data.LABS:
            for choice in data.get_lab(lab["id"])["choices"]:
                with self.subTest(lab=lab["title"], choice=choice["key"]):
                    r = self.post(lab["id"], {"choice": choice["key"], "try_number": 1})
                    self.assertEqual(r.status_code, 201)
                    self.assertEqual(r.get_json()["safe"], choice["safe"])

    def test_rejects_bad_input(self):
        lab_id = data.LABS[0]["id"]
        self.assertEqual(self.post(lab_id, {"choice": "Z", "try_number": 1}).status_code, 400)
        self.assertEqual(self.post(lab_id, {"choice": "A", "try_number": 3}).status_code, 400)
        self.assertEqual(self.post(lab_id, {}).status_code, 400)
        self.assertEqual(self.post(lab_id, {"choice": "A", "try_number": True}).status_code, 400)
        self.assertEqual(self.post(lab_id, {"choice": ["A"], "try_number": 1}).status_code, 400)
        self.assertEqual(self.post(lab_id, ["A", 1]).status_code, 400)
        self.assertEqual(self.post(9999, {"choice": "A", "try_number": 1}).status_code, 404)

    def test_clamps_seconds_and_hints(self):
        lab_id = data.LABS[0]["id"]
        r = self.post(lab_id, {"choice": "A", "try_number": 1, "seconds": "abc", "hints_used": 999})
        self.assertEqual(r.get_json()["seconds"], 0)
        self.assertEqual(r.get_json()["hints_used"], 50)


if __name__ == "__main__":
    unittest.main()
