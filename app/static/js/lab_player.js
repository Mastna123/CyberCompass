/*
  LAB PLAYER
  Shows one stage of the lab at a time and sends each try to Flask.
  Flask decides whether a choice was safe. The answer key is never sent to the browser.
*/
document.addEventListener("DOMContentLoaded", () => {
    const player = document.getElementById("lab-player");
    if (!player) return;

    const stages = player.querySelectorAll(".cc-stage");
    const stepperItems = document.querySelectorAll(".cc-stepper li");
    let hintsUsed = 0;
    let stageStartedAt = Date.now();

    // Tell Flask which stage the learner reached, so Resume can open there.
    // Fire and forget: if it fails, the learner keeps going and just resumes a bit earlier.
    function saveProgress(name) {
        fetch(player.dataset.progressUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ stage: name }),
        }).catch(() => console.warn("Could not save progress"));
    }

    // Show one stage and update the stepper at the top
    function showStage(name, { save = true } = {}) {
        let currentStep = 1;
        stages.forEach((stage) => {
            const isThisOne = stage.dataset.stage === name;
            stage.hidden = !isThisOne;
            if (isThisOne) currentStep = Number(stage.dataset.step);
        });
        stepperItems.forEach((item) => {
            const step = Number(item.dataset.step);
            item.classList.toggle("done", step < currentStep);
            item.classList.toggle("current", step === currentStep);
        });
        stageStartedAt = Date.now();   // used for "time to correct"
        window.scrollTo(0, 0);
        if (save) saveProgress(name);
    }

    // Send one try to Flask. Flask replies with the saved record, including "safe".
    async function saveTry(tryNumber, choice) {
        const response = await fetch(player.dataset.attemptUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                try_number: tryNumber,
                choice: choice,
                seconds: Math.round((Date.now() - stageStartedAt) / 1000),
                hints_used: hintsUsed,
            }),
        });
        if (!response.ok) throw new Error("Could not save this try");
        return response.json();
    }

    // Which answer is selected in a group ("first" or "second")
    function pickedChoice(groupName) {
        const picked = player.querySelector(`[data-group="${groupName}"] [aria-pressed="true"]`);
        return picked ? picked.dataset.choice : null;
    }

    // Shows the green or red banner and the result text after a try.
    // prefix is "result" for the first try and "retry" for the second.
    function showFeedback(prefix, saved) {
        document.getElementById(`${prefix}-safe`).hidden = !saved.safe;
        document.getElementById(`${prefix}-unsafe`).hidden = saved.safe;

        // textContent (not innerHTML) so the text is always shown as plain text.
        // Only the second try has a safe-choice label (Flask leaves it out after the first try).
        const label = document.getElementById(`${prefix}-safe-label`);
        if (label) label.textContent = saved.safe_label || "";
        document.getElementById(`${prefix}-text`).textContent = saved.result;
    }

    // "Next" buttons move to the stage named in data-next
    player.querySelectorAll("[data-next]").forEach((button) => {
        button.addEventListener("click", () => showStage(button.dataset.next));
    });

    // Picking an answer highlights it and turns on that group's "Lock it in" button
    player.querySelectorAll(".cc-choices").forEach((group) => {
        const lockButton = player.querySelector(`[data-lock="${group.dataset.group}"]`);
        group.querySelectorAll(".cc-choice").forEach((choice) => {
            choice.addEventListener("click", () => {
                group.querySelectorAll(".cc-choice").forEach((c) => c.setAttribute("aria-pressed", "false"));
                choice.setAttribute("aria-pressed", "true");
                lockButton.disabled = false;
            });
        });
    });

    // First try: save it, then show what happened
    player.querySelector('[data-lock="first"]').addEventListener("click", async () => {
        try {
            const saved = await saveTry(1, pickedChoice("first"));
            showFeedback("result", saved);
            showStage("result");
        } catch (error) {
            alert("Something went wrong saving your answer. Please try again.");
        }
    });

    // Second try: save it, then show how it went.
    // save: false because Flask already cleared their progress (the lab is finished).
    player.querySelector('[data-lock="second"]').addEventListener("click", async () => {
        try {
            const saved = await saveTry(2, pickedChoice("second"));
            showFeedback("retry", saved);
            showStage("retry-result", { save: false });
        } catch (error) {
            alert("Something went wrong saving your answer. Please try again.");
        }
    });

    document.getElementById("finish-button").addEventListener("click", () => {
        window.location.href = player.dataset.finishUrl;
    });

    // Hint button: show the hint and count it ("hint requests" is one of our measurements)
    document.getElementById("hint-button").addEventListener("click", () => {
        hintsUsed += 1;
        document.getElementById("hint-box").hidden = false;
    });

    // Open where the learner left off (Flask sends "learn" if they haven't started)
    showStage(player.dataset.startStage || "learn", { save: false });
});