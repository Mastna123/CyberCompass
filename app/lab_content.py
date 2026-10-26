"""
LAB CONTENT (owned by Justin, UX & Instructional Design)

This file holds the words learners see in each lab. No coding needed:
  - Only change the text inside the quotes.
  - Keep the commas, brackets, and quote marks as they are.
  - Plain text only (no HTML).
  - Anything still in [square brackets] shows on the site as a placeholder.
  - Any security claim (what a threat does, how a control works)
    gets a Derrick review before it's final.

Questions about how this file is used: ask Isabella.
"""

# ---------------------------------------------------------------------------
# The four steps every lab follows (shown on each lab's overview page).
# TODO(Justin): confirm step names and write a one-line summary for each.
# ---------------------------------------------------------------------------
LAB_STEPS = [
    {"title": "Learn", "summary": "[One-line description]"},
    {"title": "Make the call", "summary": "[One-line description]"},
    {"title": "Apply the control", "summary": "[One-line description]"},
    {"title": "Try it again", "summary": "[One-line description]"},
]

# ---------------------------------------------------------------------------
# Default text for any lab that doesn't have its own content yet.
# Leave this as is. It's what shows until a lab is filled in below.
# ---------------------------------------------------------------------------
PLACEHOLDER = {
    # Overview page
    "scenario_title": "[Scenario title]",
    "situation": "[Short description of the scenario]",
    "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
    "level": "Beginner",

    # Step 1: Learn
    "learn": "[One short, plain-language idea]",

    # Step 2: Make the call
    "prompt": "[What the learner has to decide]",
    # TODO(Justin): write the choices and mark exactly one as "safe": True
    # TODO(Derrick): confirm the safe choice is correct
    "choices": [
        {"key": "A", "label": "[Choice A]", "safe": False},
        {"key": "B", "label": "[Choice B]", "safe": False},
        {"key": "C", "label": "[Choice C]", "safe": True},
        {"key": "D", "label": "[Choice D]", "safe": False},
    ],
    "result_safe": "[What happens when they make the safe choice]",
    "result_unsafe": "[What happens when they make an unsafe choice]",

    # Step 3: Apply the control
    "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],

    # Step 4: Try it again
    "retry_prompt": "[A new version of the same situation]",

    # Shown when the learner clicks "Need a hint?"
    "hint": "[A short hint that points them in the right direction]",
}

# ---------------------------------------------------------------------------
# Content for each lab. The number is the lab's id (see LABS in data.py).
# Only fill in what's different from the placeholder above.
# TODO(Justin): fill in each lab. Copy the Phishing block as a template.
# ---------------------------------------------------------------------------
LAB_CONTENT = {
    9: {  # Phishing
        "scenario_title": "[Scenario title]",
        "situation": "[Short description of the scenario]",
    },
}