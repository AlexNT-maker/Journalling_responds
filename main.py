from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def respond_as_therapist(text):
    """Dummy answer for testing"""
    return "I understand you, sometime is okay to not feel good, actually is more than just okay."
    

@app.route('/') 
def home(): 
    """Render the home page."""
    return render_template('index.html')


@app.route('/journal', methods=['GET', 'POST'])
def journal():
    ai_response = ""
    user_text = ""

    if request.method == 'POST':
        user_text = request.form.get('user_text', '').strip()
        no_reply = request.form.get('no_reply')  

        if not user_text:
            ai_response = "Text is empty, Try again!"
        elif no_reply == 'on':  
            ai_response = None  # No answer
        else:
            # Here you make AI call (mock example):
            ai_response = f"I feel like you want to express something deeper, tell me more about this.: {user_text[:60]}..."

    return render_template('journal.html', ai_response=ai_response, user_text=user_text)



if __name__ == '__main__': 
    app.run(debug=True)