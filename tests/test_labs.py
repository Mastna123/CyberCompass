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

    def test_missing_lab_is_404(self):
        self.assertEqual(self.client.get("/labs/9999").status_code, 404)
        self.assertEqual(self.client.get("/labs/9999/play").status_code, 404)


class LabContentTest(unittest.TestCase):
    def test_content_ids_match_labs(self):
        """Every content block belongs to a real lab, so none is silently ignored."""
        lab_ids = {lab["id"] for lab in data.LABS}
        self.assertEqual(set(lab_content.LAB_CONTENT) - lab_ids, set())

    def test_exactly_one_safe_choice(self):
        for lab in data.LABS:
            with self.subTest(lab=lab["title"]):
                choices = data.get_lab(lab["id"])["choices"]
                self.assertEqual(len([c for c in choices if c["safe"]]), 1)
                keys = [c["key"] for c in choices]
                self.assertEqual(len(keys), len(set(keys)), "choice keys must be unique")

    def test_every_lab_has_role_groups(self):
        allowed = {"Everyone", "Leadership", "Management", "Office staff", "Frontline staff"}
        for lab in data.LABS:
            with self.subTest(lab=lab["title"]):
                self.assertTrue(lab.get("role_groups"))
                self.assertLessEqual(set(lab["role_groups"]), allowed)

    def test_no_dashes_in_learner_text(self):
        """Team writing rule: no em or en dashes in anything learners read."""
        path = lab_content.__file__
        with open(path, encoding="utf-8") as f:
            text = f.read()
        self.assertNotIn("—", text)
        self.assertNotIn("–", text)


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
        self.assertEqual(self.post(9999, {"choice": "A", "try_number": 1}).status_code, 404)

    def test_clamps_seconds_and_hints(self):
        lab_id = data.LABS[0]["id"]
        r = self.post(lab_id, {"choice": "A", "try_number": 1, "seconds": "abc", "hints_used": 999})
        self.assertEqual(r.get_json()["seconds"], 0)
        self.assertEqual(r.get_json()["hints_used"], 50)


if __name__ == "__main__":
    unittest.main()
