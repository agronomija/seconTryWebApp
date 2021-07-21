from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy
import hangman


app = Flask(__name__)
db = SQLAlchemy("sqlite:///db.sqlite")


class Vislice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secret_word = db.Column(db.String, unique=False)
    current_guessed_letter = db.Column(db.String, unique=False)
    guessed_letters = db.Column(db.String, unique=False)
    number_of_tries = db.Column(db.Integer, unique=False)
    missed_tries = db.Column(db.Integer, unique=False)
    username = db.Column(db.Integer, unique=True)


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def home():

    user_name = request.cookies.get('user_name')
    print(user_name)
    if request.method == 'GET':
        return render_template('home.html', user_name=user_name)

    elif request.method == 'POST' and request.form.get('izpis'):

        response = make_response(render_template('home.html', user_name=user_name))
        response.set_cookie('user_name', expires=0)
        return response

    elif request.method == 'POST':
        user_name = request.form.get('user_name')
        response = make_response(render_template('home.html', user_name=user_name))
        response.set_cookie('user_name', user_name)
        return response

@app.route('/about_me')
def about_me():
    return render_template('about_me.html')

@app.route('/hangman')
def hangman():
    user_name = request.cookies.get('user_name')
    sporocilo = 'Prosim vpišite svoje uporabniško ime za nadaljevanje!'
    if not user_name:
        user_name = None
        return render_template('home.html', sporocilo=sporocilo)

    return render_template('hangman.html', user_name=user_name)

@app.route('/fizz-buzz')
def fizz_buzz():
    return render_template('fizz-buzz.html')

@app.route('/tic-tac-toe')
def tic_tac_toe():
    return render_template('tic-tac-toe.html')




if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
