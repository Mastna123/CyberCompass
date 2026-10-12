# CyberCompass (Team README)

Internal notes for the team: how to run the app, how the code is organized, and how we work together.

---

## Team
 
| Member | Role | Responsible for |
|---|---|---|
| Justin Garter | UX & Instructional Design | Interface design, lab flow, plain-language lab content |
| Derrick Johnson | Security Validation & Environment Isolation | Lab isolation, security architecture, threat/control accuracy |
| Isabella Havens | Platform Development & Learning Analytics | Web app (frontend/backend), database, user accounts, analytics/reports |
| Nick Mast | QA, Integration & Project Management | Usability testing, integration, QA criteria, project management, repo admin |
| Luke Schnur | Lab Infrastructure | Virtualization, virtual networking, Guacamole, lab containers |

Questions go in the Teams group chat. We meet **Thursdays 6–7 PM** on Teams. Bi-weekly on Mondays (9/28, 10/12, 10/26, etc.) with Daniel **as a group**.

---

## Setup (one time)

You need [Python 3.11+](https://www.python.org/downloads/) and [Git](https://git-scm.com/downloads).

```powershell
git clone <repo URL>
cd "<repo folder>"
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

> If you see "running scripts is disabled", run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then try again.

## Run the app

```powershell
.venv\Scripts\Activate.ps1
cd app
python -m flask --app app run --debug
```

Open http://127.0.0.1:5000. Press **Ctrl + C** to stop.

---

## Where things are

```
app/
  app.py              Routes (one function per page)
  data.py             Placeholder data (will become SQLite)
  templates/          HTML pages
    base.html         Shared layout every page uses
    partials/         Reusable pieces (nav, etc.)
  static/css/
    theme.css         All colors and fonts (Starlight theme)
    app.css           Reusable styles (cards, buttons, etc.)
requirements.txt      Python packages
```

**Design:** Pages follow the final low-fi wireframes and the Starlight theme in [Figma](https://www.figma.com/design/nA4x6CqtTcYfF5Ks14gLYT/CyberCompass-Hi-Fi-Options?node-id=35-1096&m=dev)

## Status

- [x] Home / dashboard (placeholder data)
- [ ] Lab library + lab overview
- [ ] Lab player + results
- [ ] Admin pages + reports
- [ ] SQLite database + login

---

## Code rules

1. Math and logic go in Python. Templates only display values.
2. No colors or font sizes in HTML. Use a class from `app.css`.
3. Our CSS classes start with `cc-` (for CyberCompass).
4. Add a comment at the top of each file saying what it's for.
5. Lab content is a placeholder until Justin writes it. Security claims get marked `TODO: Derrick review`.

## Git workflow

1. Make a branch: `git checkout -b your-branch-name`
2. Commit small and often: `git commit -m "Add lab library page"`
3. Push and open a pull request. Nick (or another teammate) reviews it before it's merged.
4. Never commit directly to `main`.
5. Note any AI help in your pull request description.
6. Never commit passwords, keys, or real credentials.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `No module named flask` | Turn on the venv: `.venv\Scripts\Activate.ps1` |
| `TemplateNotFound` | The `templates` folder must be inside `app/` |
| Changes don't show | Hard refresh with **Ctrl + F5** |