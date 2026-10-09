# CyberCompass

## DEV - Code guide (web app)

**Where things go**
| File / folder | What it's for |
|---|---|
| `app/app.py` | Routes: one function per page. Gathers data and picks a template. |
| `app/data.py` | Placeholder data. Will be replaced by SQLite queries. |
| `app/templates/base.html` | Shared layout every page extends. |
| `app/templates/partials/` | Small pieces reused across pages (nav, decorations). |
| `app/static/css/theme.css` | **All colors and fonts.** Change the theme here only. |
| `app/static/css/app.css` | Reusable styles (cards, chips, buttons). Uses theme variables only. |

**Rules**
1. Math and decisions happen in Python, not in templates.
2. No colors or font sizes in HTML. Use a class from `app.css`.
3. Our classes start with `cc-`. Bootstrap classes are for layout/spacing only.
4. Use `{# #}` comments in templates to explain sections.
5. Lab content (scenario text, lessons) is a placeholder until written by Justin.

**Common classes**
| Class | Looks like |
|---|---|
| `cc-card` | White rounded card |
| `cc-hero` | Midnight card with stars |
| `cc-chip`, `cc-chip gold`, `cc-chip indigo` | Small pill labels |
| `btn-cc`, `btn-cc-outline`, `btn-cc-white` | Buttons (add `sm` or `lg`) |
| `cc-tile track-1` … `track-5` | Icon square in a track's colors |
| `cc-track` + `<span class="track-N" style="width: N%">` | Progress bar |
| `cc-meta`, `cc-label`, `cc-item-title`, `cc-stat` | Text sizes |

**Adding a new page**
1. Add a function with `@app.route(...)` in `app.py`.
2. Create `templates/yourpage.html` that starts with `{% extends "base.html" %}`.
3. Put content inside `{% block content %}`.
