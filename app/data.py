"""Placeholder data so the pages have something to show.

TODO(Isabella): replace this placeholder data with SQLite queries.
Keep the same keys and the templates won't need to change.
"""
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
    {"id": 1, "title": "Phishing email", "track": "social", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "in_progress", "assigned": False, "step": 2, "time_left": "about 8 min left"},
    {"id": 2, "title": "Password reuse", "track": "identity", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "done", "assigned": False, "completed": "Sep 18"},
    {"id": 3, "title": "MFA push fatigue", "track": "identity", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Friday"},
    {"id": 4, "title": "Software updates", "track": "network", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "done", "assigned": False, "completed": "Sep 11"},
    {"id": 5, "title": "Secure file sharing", "track": "data", "role_groups": ["Everyone"], "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Oct 30"},
    {"id": 6, "title": "Payment change fraud", "track": "social", "role_groups": ["Leadership", "Office staff"], "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Nov 6"},
    {"id": 7, "title": "Executive impersonation", "track": "social", "role_groups": ["Office staff", "Management", "Frontline staff"], "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 8, "title": "Responding to a report", "track": "social", "role_groups": ["Leadership", "Management"], "minutes": 15, "xp": 150, "status": "new", "assigned": False},
]

# TODO(Isabella): comes from the logged-in user once accounts are built
CURRENT_USER = {
    "id": 1,
    "first_name": "Alex",
    "initials": "AL",
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
            return {**lab_content.PLACEHOLDER, **content, **lab}
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


def closest_track():
    """The started track with the fewest labs left (for the line under the ring)."""
    started = [t for t in track_progress() if 0 < t["done"] < t["total"]]
    if not started:
        return None
    return min(started, key=lambda t: t["total"] - t["done"])


# Every saved try from the lab player.
# TODO(Isabella): move to an "attempts" table in SQLite. This list empties when the server restarts.
ATTEMPTS = []


def save_attempt(lab_id, try_number, choice, seconds, hints_used):
    """Record one try and return it. Flask decides if the choice was safe, not the browser."""
    lab = get_lab(lab_id)
    picked = next(c for c in lab["choices"] if c["key"] == choice)
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