"""Placeholder data so the pages have something to show.

TODO(Isabella): replace this placeholder data with SQLite queries.
Keep the same keys and the templates won't need to change.
"""
import random
from datetime import datetime

import lab_content

# The five tracks from the contract. "n" links each track to its colors in theme.css.
TRACKS = [
    {"id": "identity", "name": "Identity and access",       "icon": "bi-key",      "n": 1},
    {"id": "data",     "name": "Data handling and sharing", "icon": "bi-folder",   "n": 2},
    {"id": "network",  "name": "Network and device",        "icon": "bi-wifi",     "n": 3},
    {"id": "social",   "name": "Social engineering",        "icon": "bi-envelope", "n": 4},
    {"id": "emerging", "name": "Emerging risk",             "icon": "bi-stars",    "n": 5},
]

# One entry per lab: the 8 core labs from the lab catalog.
# status can be "new", "in_progress", or "done".
# role_groups: who the lab is for. "Everyone" means every role group takes it.
# minutes / xp / due dates / statuses are placeholders until the team decides them.
LABS = [
    {"id": 1, "title": "Phishing email", "track": "social", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "in_progress", "assigned": False, "time_left": "about 8 min left"},
    {"id": 2, "title": "Password reuse", "track": "identity", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "done", "assigned": False, "completed": "Sep 18"},
    {"id": 3, "title": "MFA push fatigue", "track": "identity", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Friday"},
    {"id": 4, "title": "Software updates", "track": "network", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "done", "assigned": False, "completed": "Sep 11"},
    {"id": 5, "title": "Secure file sharing", "track": "data", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Oct 30"},
    {"id": 6, "title": "Payment change fraud", "track": "social", "role_groups": ["Leadership", "Office staff"], "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Nov 6"},
    {"id": 7, "title": "Executive impersonation", "track": "social", "role_groups": ["Office staff", "Management", "Frontline staff"], "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 8, "title": "Responding to a report", "track": "social", "role_groups": ["Leadership", "Management"], "minutes": 15, "xp": 150, "status": "new", "assigned": False},
]

# Every account has one permission role and one role group.
# Permission role: what the account can do. Learning administrators can also take labs.
PERMISSION_ROLES = {"learner": "Learner", "admin": "Learning administrator"}

# Role group: who the person is at work. Decides which labs are for them.
# A lab's role_groups uses these names, or "Everyone".
# ("Deskless workers" was renamed to "Frontline staff".)
ROLE_GROUPS = ["Leadership", "Management", "Office staff", "Frontline staff"]

# TODO(Isabella): comes from the logged-in user once accounts are built
CURRENT_USER = {
    "id": 1,
    "first_name": "Alex",
    "initials": "AL",
    "role": "learner",
    "role_group": "Office staff",
    "org": "Riverside Accounting",
    "streak_weeks": 3,
    "xp": 1240,
}

# TODO(Justin): badge names and what earns each one
# TODO(Isabella): track earned badges per user once the database is set up
BADGE_TOTAL = 8
BADGES = [
    {"name": "[Badge name]", "icon": "bi-star",         "tone": "green"},
    {"name": "[Badge name]", "icon": "bi-flag",         "tone": "coral"},
    {"name": "[Badge name]", "icon": "bi-arrow-repeat", "tone": "teal"},
]

# Status names shown on the lab cards.
STATUS_LABELS = {"new": "New", "in_progress": "In progress", "done": "Done"}


def is_admin(user):
    """True if this user is a Learning administrator (for the admin pages, once they exist)."""
    return user["role"] == "admin"


def get_track(track_id):
    """Find one track by its id."""
    for track in TRACKS:
        if track["id"] == track_id:
            return track
    return None


def get_lab(lab_id):
    """Find one lab by id and combine it with its content from lab_content.py.

    Order matters: placeholder text first, then the lab's real content,
    then the lab's data (id, track, status...). Later ones win.
    """
    for lab in LABS:
        if lab["id"] == lab_id:
            content = lab_content.LAB_CONTENT.get(lab_id, {})
            stage = get_progress_stage(lab_id)
            progress = {"stage": stage, "step": STAGES[stage]}
            return {**lab_content.PLACEHOLDER, **content, **lab, **progress}
    return None


def track_progress():
    """For each track: how many labs are done, the total, and the percent done."""
    rows = []
    for track in TRACKS:
        track_labs = [lab for lab in LABS if lab["track"] == track["id"]]
        done = len([lab for lab in track_labs if lab["status"] == "done"])
        total = len(track_labs)
        percent = round(done / total * 100) if total else 0
        rows.append({**track, "done": done, "total": total, "percent": percent})
    return rows


def choices_for_try(lab, try_number):
    """The choices for one try. Try 2 uses the lab's own retry_choices if Justin wrote them."""
    if try_number == 2:
        return lab.get("retry_choices") or lab["choices"]
    return lab["choices"]


def shuffled_retry_choices(lab):
    """Try 2's choices in a new order, re-lettered A, B, C... so the letter from try 1 means nothing.

    The safe choice always moves to a different spot than it had in try 1.
    Each choice keeps its real "key" (what the browser sends back) and gets a "letter" (what it shows).
    """
    original = choices_for_try(lab, 2)
    first_try_safe_spot = next((i for i, c in enumerate(lab["choices"]) if c["safe"]), None)

    def safe_spot(choices):
        return next((i for i, c in enumerate(choices) if c["safe"]), None)

    shuffled = random.sample(original, len(original))
    # Only reshuffle when moving is possible (at least one safe and one unsafe choice),
    # so a content mistake can never loop forever
    can_move = (
        len(original) > 1
        and first_try_safe_spot is not None
        and any(c["safe"] for c in original)
        and any(not c["safe"] for c in original)
    )
    while can_move and safe_spot(shuffled) == first_try_safe_spot:
        shuffled = random.sample(original, len(original))
    return [{**choice, "letter": chr(ord("A") + i)} for i, choice in enumerate(shuffled)]


def closest_track():
    """The started track with the fewest labs left (for the line under the ring)."""
    started = [t for t in track_progress() if 0 < t["done"] < t["total"]]
    if not started:
        return None
    return min(started, key=lambda t: t["total"] - t["done"])


# Every saved try from the lab player.
# TODO(Isabella): move to an "attempts" table in SQLite. This list empties when the server restarts.
ATTEMPTS = []

def first_try(lab_id):
    """The current user's latest first try on this lab, or None if there isn't one yet."""
    for record in reversed(ATTEMPTS):
        if record["lab_id"] == lab_id and record["user_id"] == CURRENT_USER["id"] and record["try_number"] == 1:
            return record
    return None


def result_for(lab, try_number, choice_key):
    """What happened after this choice. Uses the choice's own "result" if it has one,
    otherwise the lab's general safe or unsafe message."""
    picked = next((c for c in choices_for_try(lab, try_number) if c["key"] == choice_key), None)
    if picked is None:
        return ""
    if picked.get("result"):
        return picked["result"]
    return lab["result_safe"] if picked["safe"] else lab["result_unsafe"]

def safe_choice_label(lab, try_number):
    """The wording of the safe choice, so we can show it after the learner answers."""
    safe = next((c for c in choices_for_try(lab, try_number) if c["safe"]), None)
    return safe["label"] if safe else ""

def first_try_safe(lab_id):
    """Was the learner's latest first try on this lab safe? None if there's no first try yet."""
    for record in reversed(ATTEMPTS):
        if record["lab_id"] == lab_id and record["user_id"] == CURRENT_USER["id"] and record["try_number"] == 1:
            return record["safe"]
    return None


# Lab player stages, and which step (1-4) of the stepper each one belongs to.
# Names match data-stage in lab_play.html.
STAGES = {"learn": 1, "decide": 2, "result": 2, "control": 3, "retry": 4}

# Where each learner is in each lab, so Resume opens the right stage.
# Key: (user_id, lab_id). Value: {"stage": ..., "updated_at": ...}
# TODO(Isabella): move to a "progress" table next to "attempts". This empties when the server restarts.
# Lab 1 starts at "decide" so the demo resume card has something to show.
PROGRESS = {(1, 1): {"stage": "decide", "updated_at": None}}


def get_progress_stage(lab_id):
    """The stage the current user should land on in this lab ("learn" if they haven't started)."""
    saved = PROGRESS.get((CURRENT_USER["id"], lab_id))
    if saved is None:
        return "learn"
    # "What happened" needs the first try. If it's gone (server restarted), go back to the question.
    if saved["stage"] == "result" and first_try_safe(lab_id) is None:
        return "decide"
    return saved["stage"]


def has_progress(lab_id):
    """True if the current user started this lab and hasn't finished it."""
    return (CURRENT_USER["id"], lab_id) in PROGRESS


def resume_lab_id():
    """The lab the current user worked on most recently and hasn't finished, or None."""
    mine = [(lab_id, saved) for (user_id, lab_id), saved in PROGRESS.items() if user_id == CURRENT_USER["id"]]
    if not mine:
        return None
    # updated_at is an ISO date string, so text order is time order. The demo seed has None, so it sorts first.
    return max(mine, key=lambda item: item[1]["updated_at"] or "")[0]


def save_progress(lab_id, stage):
    """Remember which stage the current user reached in this lab."""
    PROGRESS[(CURRENT_USER["id"], lab_id)] = {
        "stage": stage,
        # Full precision so two saves in the same second still sort in order (see resume_lab_id)
        "updated_at": datetime.now().isoformat(timespec="microseconds"),
    }


def clear_progress(lab_id):
    """Forget the current user's place in this lab (they finished it)."""
    PROGRESS.pop((CURRENT_USER["id"], lab_id), None)


def reset_all():
    """DEV ONLY: put the current user back at the start, with no labs done.

    The labs, their content, and assignments stay. Only progress is cleared:
    saved tries, where they are in each lab, lab status, XP, and streak.
    Restarting the server brings the demo data back, since it all lives in memory for now.
    """
    ATTEMPTS.clear()
    PROGRESS.clear()
    for lab in LABS:
        lab["status"] = "new"
        lab.pop("completed", None)
        lab.pop("time_left", None)
    CURRENT_USER["xp"] = 0
    CURRENT_USER["streak_weeks"] = 0


def save_attempt(lab_id, try_number, choice, seconds, hints_used):
    """Record one try and return it. Flask decides if the choice was safe, not the browser."""
    lab = get_lab(lab_id)
    picked = next(c for c in choices_for_try(lab, try_number) if c["key"] == choice)
    record = {
        "lab_id": lab_id,
        "user_id": CURRENT_USER["id"],
        "try_number": try_number,
        "choice": choice,
        "safe": picked["safe"],
        "seconds": seconds,
        "hints_used": hints_used,
        "saved_at": datetime.now().isoformat(timespec="seconds"),
    }
    ATTEMPTS.append(record)
    return record