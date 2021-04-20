from flask import Flask, render_template, redirect, request, session
from datetime import datetime
import random

app = Flask(__name__)
app.secret_key='whatever'

@app.route('/')
def inex():
    if 'gold' not in session:
        session['gold']=0
        session['move']=0
        session['end_game']=False
    if 'activities' not in session:
        session['activities'] = []
        session['activities'].insert(0,"Game Began")
    return render_template('index.html', gold = session['gold'], activities=session['activities'])

@app.route('/process_money', methods=['POST'])
def process_money():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if session['end_game']:
        return redirect('/')
    if session['move'] > 10 and not session['end_game']:
        if session['gold'] >= 300:
            session['activities'].insert(1, f"Congratulation!, you have won over 250 gold ({now}) - Reset to play agian!")
        elif session['gold'] >= 100:
            session['activities'].insert(1, f"Well done, you have won! ({now}) - Reset to play agian!")
        elif session['gold'] >= 0:
            session['activities'].insert(1, f"Uf, You won for very little! ({now}) - Reset to play agian!")
        else:
            session['activities'].insert(1, f"You lost..now you are bankrupt ({now}) - Reset to play agian..")
        session['end_game'] = True
        return redirect('/')
    
    if request.form['action'] == "casino":
        gold = random.randrange(-50,50)
        if gold < 0:
            session['activities'].insert(1, f"Entered a casino and lose {gold} golds.. Ouch.. ({now})")
            
        else:
            session['activities'].insert(1, f"Entered a casino and win {gold} golds! yeah! ({now})")
        session['gold']+=gold

    else:
        if request.form['action'] == "farm":
            gold = random.randrange(10, 21)
        if request.form['action'] == "cave":
            gold = random.randrange(5, 11)
        if request.form['action'] == "house":
            gold = random.randrange(2, 6)
        session['gold'] += gold
        session['activities'].insert(1, f"Earned {gold} golds from the {request.form['action']}! ({now})")
    session['move'] += 1
    return redirect('/')

@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

if __name__=='__main__':
    app.run(debug=True)
