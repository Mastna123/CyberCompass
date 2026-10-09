from flask import Flask, render_template

import data

app = Flask(__name__)


@app.context_processor
def inject_globals():
    """Values every template can use without passing them each time."""
    return {"user": data.CURRENT_USER, "get_track": data.get_track}


@app.route("/")
def home():
    resume_lab = next((lab for lab in data.LABS if lab["status"] == "in_progress"), None)
    assigned = [lab for lab in data.LABS if lab["assigned"] and lab["status"] != "done"]
    done = [lab for lab in data.LABS if lab["status"] == "done"]

    return render_template(
        "home.html",
        active="home",
        resume_lab=resume_lab,
        next_due=assigned[0] if assigned else None,
        assigned=assigned[1:],
        done_count=len(done),
        total_count=len(data.LABS),
        recent=done[:2],
        tracks=data.track_progress(),
        badges=data.BADGES,
        badge_total=data.BADGE_TOTAL,
        closest=data.closest_track(),
    )