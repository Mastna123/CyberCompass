"""CyberCompass web app: page routes. Run with: python -m flask --app app run --debug"""

from flask import Flask, render_template

import data

app = Flask(__name__)


@app.context_processor
def inject_globals():
    """Values every template can use without passing them each time."""
    return {"user": data.CURRENT_USER, "get_track": data.get_track}


@app.route("/")
@app.route("/")
def home():
    """Dashboard: what the learner should do next and how they're doing."""
    in_progress_lab = next((lab for lab in data.LABS if lab["status"] == "in_progress"), None)
    assigned_labs = [lab for lab in data.LABS if lab["assigned"] and lab["status"] != "done"]
    finished_labs = [lab for lab in data.LABS if lab["status"] == "done"]

    return render_template(
        "home.html",
        active="home",                                    # which nav link to highlight
        resume_lab=in_progress_lab,                       # big midnight card at the top
        resume_percent=round(in_progress_lab["step"] / 4 * 100) if in_progress_lab else 0,
        next_due=assigned_labs[0] if assigned_labs else None,
        other_assigned=assigned_labs[1:],                 # everything after the first
        done_count=len(finished_labs),
        total_count=len(data.LABS),
        done_percent=round(len(finished_labs) / len(data.LABS) * 100),
        recent_results=finished_labs[:2],
        tracks=data.track_progress(),
        closest_track=data.closest_track(),
        badges=data.BADGES,
        badge_total=data.BADGE_TOTAL,
    )