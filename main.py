from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def respond_as_therapist(text):
    """Dummy answer for testing"""
    return "I understand you, sometime is okay to not feel good, actually is more than just okay."
    

@app.route('/') 
def home(): 
    """Render the home page."""
    return render_template('index.html')


@app.route('/journal', methods = ['GET', 'POST'])
def journal():
    """Render the journal page."""
    ai_response = None 
    if request.method == 'POST':
        user_input = request.form.get('entry')
        ai_response = respond_as_therapist(user_input)
    return render_template('journal.html', ai_response = ai_response)


if __name__ == '__main__': 
    app.run(debug=True)