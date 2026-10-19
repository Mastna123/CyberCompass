"""Placeholder data so the pages have something to show.

!! Replace with SQLite queries later. Keep the same keys and the templates won't need to change."""

# The five tracks from the contract. Colors come from theme.css.
TRACKS = [
    {"id": "identity", "name": "Identity and access",       "icon": "bi-key",      "n": 1},
    {"id": "data",     "name": "Data handling and sharing", "icon": "bi-folder",   "n": 2},
    {"id": "network",  "name": "Network and device",        "icon": "bi-wifi",     "n": 3},
    {"id": "social",   "name": "Social engineering",        "icon": "bi-envelope", "n": 4},
    {"id": "emerging", "name": "Emerging risk",             "icon": "bi-stars",    "n": 5},
]

# status can be "new", "in_progress", or "done"
# minutes / xp / due dates are placeholders until the team decides them
LABS = [
    {"id": 1, "title": "Password security", "track": "identity", "minutes": 15, "xp": 150, "status": "done", "assigned": False},
    {"id": 2, "title": "Multifactor authentication", "track": "identity", "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Fri"},
    {"id": 3, "title": "Account recovery", "track": "identity", "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 4, "title": "File permissions", "track": "data", "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 5, "title": "Secure file sharing", "track": "data", "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Oct 10"},
    {"id": 6, "title": "Backups", "track": "data", "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 7, "title": "Wi-Fi security", "track": "network", "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 8, "title": "Software updates", "track": "network", "minutes": 15, "xp": 150, "status": "done", "assigned": False},
    {"id": 9, "title": "Phishing", "track": "social", "minutes": 15, "xp": 150, "status": "in_progress", "assigned": False,
     "scenario_title": "[Scenario title from Justin]", "step": 2},
    {"id": 10, "title": "Safe downloads", "track": "social", "minutes": 15, "xp": 150, "status": "new", "assigned": False},
    {"id": 11, "title": "Safe AI usage", "track": "emerging", "minutes": 15, "xp": 150, "status": "new", "assigned": True, "due": "Oct 17"},
]

CURRENT_USER = {
    "first_name": "Alex",
    "initials": "AL",
    "role_group": "Office staff",
    "org": "Riverside Accounting",
    "streak_weeks": 3,
    "xp": 1240,
}

BADGE_TOTAL = 8   # placeholder until the team decides the badge list
BADGES = [
    {"name": "[Badge name]", "icon": "bi-star",        "tone": "green"},
    {"name": "[Badge name]", "icon": "bi-flag",        "tone": "coral"},
    {"name": "[Badge name]", "icon": "bi-arrow-repeat", "tone": "teal"},
]


def get_track(track_id):
    """Find one track by its id."""
    for t in TRACKS:
        if t["id"] == track_id:
            return t
    return None


def track_progress():
    """For each track: how many labs are done, the total, and the percent done.

    Used by the "Progress by track" bars on the Home page.
    """
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
