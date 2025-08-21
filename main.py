from flask import Flask, render_template, request
import random
from datetime import timedelta, date
from models import MoodEntry, JournalEntry
from extensions import db 
from sqlalchemy import func
from services.ai import generate_care_reply, AIResult
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mood.db'
db.init_app(app)


@app.route('/') 
def home(): 
    """Render the home page."""
    return render_template('index.html')


@app.route('/journal', methods=['GET', 'POST'])
def journal():
    """Render the journal page and handle user input for AI replies."""
    ai_response = ""
    user_text = ""

    if request.method == 'POST':
        user_text = request.form.get('user_text', '').strip()
        no_reply = request.form.get('no_reply')

        if not user_text:
            ai_response = "Text is empty, Try again!"
            result = None
        elif no_reply == 'on':
            ai_response = None
            result = None
        else:
            result = None
            try:
                result = generate_care_reply(user_text, respect_no_reply=False)
                ai_response = result.text
            except Exception as e:
                print("AI ERROR", repr(e))
                ai_response = (
                    "I couldn't reach the assistant right now. "
                    "If you want, try again in a bit — and in the meantime, "
                    "keep writing. I'm here for you. ❤️"
                )

        # --- save mood if provided (μία φορά την ημέρα) ---
        if result and getattr(result, "mood", None) is not None:
            today_d = date.today()
            existing = MoodEntry.query.filter_by(date=today_d).first()
            if existing:
                existing.mood = result.mood
            else:
                db.session.add(MoodEntry(date=today_d, mood=result.mood))

        # --- save journal entry ---
        if user_text:
            db.session.add(JournalEntry(user_text=user_text, ai_response=ai_response))

        db.session.commit()

    return render_template('journal.html', ai_response=ai_response, user_text=user_text)


@app.route('/insights')
def insights():
    """Renders the insights page with data from DB."""
    today = date.today()
    start_30 = today - timedelta(days=29)
    start_7 = today - timedelta(days=6)

    # We bring only the last 30 days

    rows_30 = (
        db.session.query(
            MoodEntry.date.label("d"),
            func.avg(MoodEntry.mood).label("avg_mood")
        )
        .filter(MoodEntry.date >= start_30)
        .group_by(MoodEntry.date)
        .order_by(MoodEntry.date)
        .all()
    )

    # We put the results on dict for quick lookup
    by_day_30 = {r.d: round(float(r.avg_mood), 2) for r in rows_30}

    # We create continuous timeline, so to look and the blank dates
    def build_series(start_day, end_day):
        out = []
        cur = start_day
        while cur <= end_day:
            mood_val = by_day_30.get(cur, None)  # None => empty graph
            out.append({"date": cur.strftime("%Y-%m-%d"), "mood": mood_val})
            cur += timedelta(days=1)
        return out

    month_data = build_series(start_30, today)
    week_data = build_series(start_7, today)

    return render_template('insights.html', week_data=week_data, month_data=month_data)

@app.route('/seed_moods')
def seed_moods():
    """Generates random mood values, for testing only."""
    today = date.today()
    for i in range(10):
        d = today - timedelta(days=i)
        db.session.add(MoodEntry(date=d, mood=random.randint(3,10)))
    db.session.commit()
    return "Seeded!"


with app.app_context():
    db.create_all()


if __name__ == '__main__': 
    app.run(debug=True)