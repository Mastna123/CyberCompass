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
# ---------------------------------------------------------------------------
# TODO(Justin): review step wording
LAB_STEPS = [
    {"title": "Learn", "summary": "Pick up one quick idea you'll use in this lab."},
    {"title": "Make the call", "summary": "Decide what you'd do, then see what happens."},
    {"title": "Apply the control", "summary": "Walk through the safe way, one step at a time."},
    {"title": "Try it again", "summary": "Handle a new version of the same situation."},
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

    # Optional: any choice can have its own "result" (what happens after picking it).
    # Leave it out and the general result_safe / result_unsafe text is used instead.

    # Step 3: Apply the control
    "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],

    # Step 4: Try it again
    "retry_prompt": "[A new version of the same situation]",
    # Optional: a lab can have its own "retry_choices" for Try it again.
    # Same layout as "choices" above, with exactly one marked "safe": True.
    # Leave it out and Try it again reuses the choices above in a new order.

    # Shown when the learner clicks "Need a hint?"
    "hint": "[A short hint that points them in the right direction]",
}

# ---------------------------------------------------------------------------
# Content for each lab. The number is the lab's id (see LABS in data.py).
# Situation, prompt, and choices come from the lab catalog (Encounter / Unsafe / Safe).
# Everything in [square brackets] is still a placeholder.
# TODO(Justin): fill in the bracketed text for each lab.
# A lab can also have its own "retry_choices" for Try it again (see PLACEHOLDER above).
# ---------------------------------------------------------------------------
LAB_CONTENT = {
        1: {  # Phishing email
        # TODO(Justin): demo wording I kept simple on purpose. Please review and expand it however you'd like.
        # TODO(Derrick): confirm the safe choice and that each result is accurate
        "scenario_title": "The overdue invoice",
        "situation": "An overdue invoice from a lookalike vendor address arrives with a zipped attachment.",
        "desk_preview": "In this lab, you'll see a pretend email inbox with the overdue invoice in it. You can check the sender, the subject, and the attachment name, then decide what to do below.",
        "outcomes": [
            "Spot the warning signs in a suspicious email",
            "Use the Report button instead of replying or forwarding",
            "Explain why surprise attachments are risky",
        ],
        "learn": "Scammers want you to act fast. An urgent tone, a sender address that's almost right, and an attachment you weren't expecting are all signs to slow down and report the email instead of opening it.",
        "prompt": "What do you do with this email?",
        "choices": [
            {"key": "A", "label": "Open the zipped attachment to check the invoice.", "safe": False,
            "result": "The zip file wasn't an invoice. It installed malware on your computer, and IT had to take your laptop offline to clean it up."},
            {"key": "B", "label": "Report it with the Report button without opening it.", "safe": True,
            "result": "IT confirmed it was a phishing email and blocked the sender for everyone, so nobody else could fall for it."},
            {"key": "C", "label": "Reply and ask the vendor to confirm it's real.", "safe": False,
            "result": "The scammer wrote back right away saying the invoice is real and the payment is urgent. Now they know your email is active, and they keep pushing."},
            {"key": "D", "label": "Forward it to a coworker to take a look.", "safe": False,
            "result": "Your coworker opened the attachment, thinking you'd already checked it. Now their computer has the problem instead of yours."},
        ],
        "control_steps": [
            "Don't open the attachment or click any links.",
            "Look closely at the sender's address. Small misspellings are a common giveaway.",
            "Click the Report button so IT can check it and warn everyone else.",
            "If you think a real bill might be overdue, contact the vendor using contact info you already have.",
        ],
        "retry_prompt": "A week later, another overdue invoice shows up from a slightly different vendor address. It has a zipped attachment and warns about a late fee.",
        "hint": "Look closely at the sender's address. Does it match the vendor's real one?",
    },
    2: {  # Password reuse
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "A site you shop on was breached, and you use the same password for your work email.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "What do you do about your work email password?",
        "choices": [
            {"key": "A", "label": "Keep the current password.", "safe": False},
            {"key": "B", "label": "Change it to a small variation, like adding a number.", "safe": False},
            {"key": "C", "label": "Pick one new password and use it on both sites.", "safe": False},
            {"key": "D", "label": "Set a unique password and store it in a password manager.", "safe": True},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[A new version of the same situation]",
        "hint": "[A short hint that points them in the right direction]",
    },
    3: {  # MFA push fatigue
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "Login approval prompts you didn't trigger keep coming.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "What do you do with the prompts?",
        "choices": [
            {"key": "A", "label": "Deny every prompt and report the attempt.", "safe": True},
            {"key": "B", "label": "Approve one so the prompts stop.", "safe": False},
            {"key": "C", "label": "Ignore them and keep working.", "safe": False},
            {"key": "D", "label": "Approve it, since it might be you on another device.", "safe": False},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[A new version of the same situation]",
        "hint": "[A short hint that points them in the right direction]",
    },
    4: {  # Software updates
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "An update asks for a restart in the middle of the afternoon.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "What do you do with the update?",
        "choices": [
            {"key": "A", "label": "Postpone it until tomorrow.", "safe": False},
            {"key": "B", "label": "Postpone it until the end of the week.", "safe": False},
            {"key": "C", "label": "Install it right away or before you clock out today.", "safe": True},
            {"key": "D", "label": "Turn off update reminders so they stop interrupting.", "safe": False},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[A new version of the same situation]",
        "hint": "[A short hint that points them in the right direction]",
    },
    5: {  # Secure file sharing
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "A client folder needs to go to one outside contact.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "How do you share the folder?",
        "choices": [
            {"key": "A", "label": "Share it as “anyone with the link” with no expiration.", "safe": False},
            {"key": "B", "label": "Share with the named person only and set an expiration date.", "safe": True},
            {"key": "C", "label": "Share it with anyone at their company, with no expiration.", "safe": False},
            {"key": "D", "label": "Upload it to your personal cloud storage and share it from there.", "safe": False},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[A new version of the same situation]",
        "hint": "[A short hint that points them in the right direction]",
    },
    6: {  # Payment change fraud
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "A known vendor emails new bank details right before a large payment.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "What do you do before the payment goes out?",
        "choices": [
            {"key": "A", "label": "Update the bank details in the payment system.", "safe": False},
            {"key": "B", "label": "Reply to the same email to confirm the change.", "safe": False},
            {"key": "C", "label": "Call the phone number listed in the email.", "safe": False},
            {"key": "D", "label": "Call the vendor at a number already on file before changing anything.", "safe": True},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[A new version of the same situation]",
        "hint": "[A short hint that points them in the right direction]",
    },
    7: {  # Executive impersonation
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "An email that looks like it's from the owner asks for an urgent, confidential wire transfer.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "What do you do with the request?",
        "choices": [
            {"key": "A", "label": "Send the money, since it came from the boss.", "safe": False},
            {"key": "B", "label": "Reply to the email to confirm before sending.", "safe": False},
            {"key": "C", "label": "Verify with the owner by a known phone number or in person first.", "safe": True},
            {"key": "D", "label": "Keep it confidential and send it before the deadline.", "safe": False},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[Text version: someone claiming to be the CEO texts your personal phone and asks you to buy gift cards]",
        "hint": "[A short hint that points them in the right direction]",
    },
    8: {  # Responding to a report
        # TODO(Derrick): confirm the safe choice and that each unsafe choice is really unsafe
        "scenario_title": "[Scenario title]",
        "situation": "An employee admits they clicked a suspicious link an hour ago.",
        "outcomes": ["[Learning outcome 1]", "[Learning outcome 2]", "[Learning outcome 3]"],
        "learn": "[One short, plain-language idea]",
        "prompt": "How do you respond?",
        "choices": [
            {"key": "A", "label": "Thank them and get IT involved right away.", "safe": True},
            {"key": "B", "label": "Tell them to be more careful and move on.", "safe": False},
            {"key": "C", "label": "Ask them to keep it quiet so it doesn't spread.", "safe": False},
            {"key": "D", "label": "Try to clean it up yourself before telling anyone.", "safe": False},
        ],
        "result_safe": "[What happens when they make the safe choice]",
        "result_unsafe": "[What happens when they make an unsafe choice]",
        "control_steps": ["[Step 1]", "[Step 2]", "[Step 3]"],
        "retry_prompt": "[A new version of the same situation]",
        "hint": "[A short hint that points them in the right direction]",
    },
}
