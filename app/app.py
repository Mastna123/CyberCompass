"""CyberCompass web app: page routes.

Run with: python -m flask --app app run --debug
"""
from flask import Flask, abort, jsonify, render_template, request

import data
import lab_content

app = Flask(__name__)


@app.context_processor
def inject_globals():
    """Values every template can use without passing them each time."""
    return {
        "user": data.CURRENT_USER,
        "role_label": data.PERMISSION_ROLES[data.CURRENT_USER["role"]],   # "Learner" or "Learning administrator"
        "get_track": data.get_track,
        "status_labels": data.STATUS_LABELS,
    }


@app.route("/")
def home():
    """Dashboard: what the learner should do next and how they're doing."""
    resume_id = data.resume_lab_id()                      # most recently worked on, not finished
    in_progress_lab = data.get_lab(resume_id) if resume_id else None
    assigned_labs = [lab for lab in data.LABS if lab["assigned"] and lab["status"] != "done"]
    finished_labs = [lab for lab in data.LABS if lab["status"] == "done"]

    return render_template(
        "home.html",
        active="home",                                    # which nav link to highlight
        resume_lab=in_progress_lab,                       # big midnight card at the top
        resume_percent=round(in_progress_lab["step"] / 4 * 100) if in_progress_lab else 0,
        next_due=assigned_labs[0] if assigned_labs else None,
        assigned_labs=assigned_labs,                      # full list, including next_due
        done_count=len(finished_labs),
        total_count=len(data.LABS),
        done_percent=round(len(finished_labs) / len(data.LABS) * 100),
        recent_results=finished_labs[:2],
        tracks=data.track_progress(),
        closest_track=data.closest_track(),
        badges=data.BADGES,
        badge_total=data.BADGE_TOTAL,
    )


@app.route("/labs")
def library():
    """Lab library: every lab as a card, with optional track and status filters."""
    selected_track = request.args.get("track")     # e.g. /labs?track=social
    selected_status = request.args.get("status")   # e.g. /labs?status=done

    labs = data.LABS
    if selected_track:
        labs = [lab for lab in labs if lab["track"] == selected_track]
    if selected_status:
        labs = [lab for lab in labs if lab["status"] == selected_status]
    labs = sorted(labs, key=lambda lab: not lab["assigned"])   # assigned labs first

    return render_template(
        "labs.html",
        active="labs",
        labs=labs,
        tracks=data.TRACKS,
        selected_track=selected_track,
        selected_status=selected_status,
        # A real track with no labs yet (like Emerging risk) gets a "coming soon" message
        track_coming_soon=bool(selected_track) and data.get_track(selected_track) is not None
            and not any(lab["track"] == selected_track for lab in data.LABS),
    )


@app.route("/labs/<int:lab_id>")
def lab_overview(lab_id):
    """One lab's intro page: the situation, how the lab works, and a Start button."""
    lab = data.get_lab(lab_id)
    if lab is None:
        abort(404)   # shows a "Not Found" page for labs that don't exist

    return render_template(
        "lab_overview.html",
        active="labs",
        lab=lab,
        track=data.get_track(lab["track"]),
        steps=lab_content.LAB_STEPS,
        current_step=lab["step"],                      # which step "How this lab works" highlights
        started=data.has_progress(lab_id),             # "Resume lab" instead of "Start lab"
    )


@app.route("/labs/<int:lab_id>/play")
def lab_play(lab_id):
    """The lab itself: Learn → Make the call → Apply the control → Try it again."""
    lab = data.get_lab(lab_id)
    if lab is None:
        abort(404)
    saved_first_try = data.first_try(lab_id)
    first_try_result = data.result_for(lab, 1, saved_first_try["choice"]) if saved_first_try else ""
    return render_template(
        "lab_play.html",
        lab=lab,
        steps=lab_content.LAB_STEPS,
        start_stage=lab["stage"],                         # where Resume picks up
        first_try_safe=data.first_try_safe(lab_id),       # for "What happened" on resume
        first_try_result=first_try_result,                # the message for their saved first try
        retry_choices=data.shuffled_retry_choices(lab),   # new order and letters for Try it again
    )


def json_object():
    """The JSON body the browser sent, or {} if it's missing or isn't a {...} object."""
    body = request.get_json(silent=True)
    return body if isinstance(body, dict) else {}


def whole_number(value, low, high):
    """Turn a value from the browser into a whole number between low and high.
    Anything that isn't a number becomes `low`. Never trust input from the browser."""
    try:
        return max(low, min(int(value), high))
    except (TypeError, ValueError):
        return low


# TODO(Isabella): add CSRF protection to this route when login is added
@app.post("/api/labs/<int:lab_id>/attempts")
def record_attempt(lab_id):
    """Save one try from the lab player. The browser sends JSON, and we check it before saving."""
    lab = data.get_lab(lab_id)
    if lab is None:
        abort(404)

    body = json_object()
    choice = body.get("choice")
    try_number = body.get("try_number")
    # type() check: JSON true would otherwise count as 1
    if type(try_number) is not int or try_number not in (1, 2):
        return jsonify({"error": "Invalid attempt"}), 400
    valid_choices = [c["key"] for c in data.choices_for_try(lab, try_number)]
    if choice not in valid_choices:
        return jsonify({"error": "Invalid attempt"}), 400

    record = data.save_attempt(
        lab_id=lab_id,
        try_number=try_number,
        choice=choice,
        seconds=whole_number(body.get("seconds"), 0, 3600),
        hints_used=whole_number(body.get("hints_used"), 0, 50),
    )
    if try_number == 2:
        data.clear_progress(lab_id)   # finished, so there's nothing left to resume
    
    # Send back what happened for this choice, so the player can show it
    reply = {**record, "result": data.result_for(lab, try_number, choice)}
    # The safe choice is only named once the lab is over. After try 1 it would give away try 2,
    # which uses the same choices (just shuffled) unless the lab has its own retry_choices.
    if try_number == 2:
        reply["safe_label"] = data.safe_choice_label(lab, try_number)
    return jsonify(reply), 201


# TODO(Isabella): add CSRF protection to this route when login is added
@app.post("/api/labs/<int:lab_id>/progress")
def record_progress(lab_id):
    """Save which stage of the lab player the learner reached, so Resume can open there."""
    if data.get_lab(lab_id) is None:
        abort(404)

    stage = json_object().get("stage")
    if not isinstance(stage, str) or stage not in data.STAGES:
        return jsonify({"error": "Invalid stage"}), 400

    data.save_progress(lab_id, stage)
    return jsonify({"stage": stage}), 200