
from flask import Flask, render_template, request, redirect, url_for, session, flash

from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'  # Required for Flask Debug Toolbar and Session

@app.route('/', methods=['GET', 'POST'])
def start_survey():
    """Show the start page for the survey and initialize session responses."""
    if request.method == 'POST':
        # Initialize session responses when the start button is clicked
        session['responses'] = []
        return redirect('/questions/0')
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("start.html", title=title, instructions=instructions)

@app.route('/questions/<int:qid>', methods=['GET', 'POST'])
def show_question(qid):
    """Show current question and handle user's answer with protections and flash messages."""
    responses = session.get('responses', [])
    
    # If user has answered all questions, redirect to thank you page
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')
    
    # If user tries to access a question out of order, flash a message and redirect to the correct question
    if qid != len(responses):
        flash("You're trying to access an invalid question!")
        return redirect(f"/questions/{len(responses)}")
    
    question = satisfaction_survey.questions[qid]
    return render_template("question.html", question_text=question.question, choices=question.choices, qid=qid)

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Handle answer to current question and redirect to next question using session."""
    responses = session['responses']
    
    # Capture the answer from the form data
    answer = request.form.get('choice')
    
    # Append the answer to the session responses
    responses.append(answer)
    session['responses'] = responses
    
    # Check if there are more questions to answer
    if len(responses) < len(satisfaction_survey.questions):
        # Redirect to next question
        return redirect(f"/questions/{len(responses)}")
    else:
        # Redirect to thank you page if all questions are answered
        return redirect('/thanks')

@app.route('/thanks')
def thanks():
    """Show thank you message after completing the survey."""
    return render_template("thanks.html")

if __name__ == '__main__':
    app.run(debug=True)
