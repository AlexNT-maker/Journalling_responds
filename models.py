from extensions import db
from datetime import datetime 


class MoodEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date= db.Column(db.Date, nullable = False)
    mood= db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"<Moodentry {self.date} - {self.mood}>"

class JournalEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_text = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable = True)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)