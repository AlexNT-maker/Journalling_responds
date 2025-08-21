# Copilot Instructions for AI_Journalling

## Project Overview
This is a Flask-based journalling and mood tracking web application. The main features are:
- **Journal Entry**: Users submit text entries, optionally receiving an AI-generated response (mocked in `main.py`).
- **Mood Tracking**: Users log daily mood scores.
- **Insights**: Aggregated mood and journal data are visualized for the last 7/30 days.

## Architecture & Key Files
- `main.py`: Flask app entry point. Defines routes for home (`/`), journal (`/journal`), and insights (`/insights`). Handles form submissions, AI response logic, and DB commits.
- `models.py`: SQLAlchemy models for `MoodEntry` and `JournalEntry`. Each journal entry can store both user text and an AI response.
- `extensions.py`: Initializes the SQLAlchemy `db` object for use across the app.
- `instance/mood.db`: SQLite database file (auto-created).
- `templates/`: Jinja2 HTML templates for all pages.
- `static/`: CSS and JS assets for UI styling and interactivity.

## Data Flow & Patterns
- All DB operations use SQLAlchemy via the shared `db` object.
- Journal entries and mood scores are stored in separate tables.
- AI responses are currently mocked; real integration should replace `respond_as_therapist()` in `main.py`.
- Insights are calculated using SQL queries (see `/insights` route).

## Developer Workflows
- **Run the app**: `python main.py` (ensure Flask and Flask-SQLAlchemy are installed)
- **Database**: No migrations; tables are auto-created on first run. To reset, delete `instance/mood.db`.
- **Debugging**: Use Flask's built-in debugger. No custom logging or error handling patterns.
- **Testing**: No test files or frameworks present.

## Conventions & Patterns
- All database models inherit from `db.Model`.
- Timestamps use UTC (`datetime.utcnow`).
- HTML templates use Jinja2 and expect variables named as in route return values.
- CSS/JS files are referenced from `/static/` in templates.
- No environment variable usage detected (despite `.env` file presence).

## Integration Points
- To add real AI, replace the mock in `respond_as_therapist()`.
- For new features, follow the pattern: define model in `models.py`, add route in `main.py`, create template in `templates/`.

## Examples
- Adding a new journal entry:
  ```python
  new_entry = JournalEntry(user_text="text", ai_response="response")
  db.session.add(new_entry)
  db.session.commit()
  ```
- Rendering a template:
  ```python
  return render_template('journal.html', ai_response=ai_response, user_text=user_text)
  ```

## Key Directories
- `templates/` — HTML templates
- `static/` — CSS/JS assets
- `instance/` — SQLite DB

---
**Feedback requested:** If any section is unclear or missing, please specify so it can be improved for future AI agents.
