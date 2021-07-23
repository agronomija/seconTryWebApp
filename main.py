from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy
from hangman import Hangman, choose_secret_word


app = Flask(__name__)
db = SQLAlchemy("sqlite:///db.sqlite")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secret_word = db.Column(db.String, unique=False)
    current_guessed_letter = db.Column(db.String, unique=False)
    guessed_letters = db.Column(db.String, unique=False)
    number_of_tries = db.Column(db.Integer, unique=False)
    missed_tries = db.Column(db.Integer, unique=False)
    user_name = db.Column(db.String, unique=True)
    user_password = db.Column(db.String, unique=False)
    user_email = db.Column(db.String, unique=True)

db.create_all()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET': #poskrbi da če je že nekdo vpisan ga napoti na about_me.html in ga pozdravi,
        #drugače pa mu napiše da ga ne pozna in mu reče da se mora vpisati ali registrerati..

        user_name = request.cookies.get('user_name_test')
        if user_name:
            print(user_name)
            return render_template('about_me.html', user_name=user_name)
        else:
            print('pod tem imenom ni nobenega cookija..')
            return render_template('about_me.html')



@app.route('/register', methods=['POST', 'GET'])
def register():
    piskotek = request.cookies.get('user_name_test')

    if request.method == 'GET':
        ze_vpisan = 'Nekdo je ze vpisan. Če to niste vi, potem se morate najprej odjaviti'
        if piskotek:
            return render_template('about_me.html', ze_vpisan=ze_vpisan)
        else:
            nihce_vpisan = 'za nadaljevanje se vpisi..'
            return render_template('login.html', nihce_vpisan=nihce_vpisan)

    elif request.method == 'POST':
        password = request.form.get('user-password')
        email = request.form.get('user-email')
        user_name = request.form.get('user-name')


        if not db.query(User).filter_by(user_name=user_name).first() and not db.query(User).filter_by(user_email=email).first():
            user = User(user_name=user_name, user_email=email, user_password=password)
            response = make_response(render_template('about_me.html', user_name=user_name))
            response.set_cookie('user_name_test', user_name)
            return response
            #tukaj je potrebno dodat cookie

        elif db.query(User).filter_by(user_email=email).first() and db.query(User).filter_by(user_name=user_name).first():
            enak_username_email = 'Ta email in username že obstajata'
            return render_template('login.html', enak_username_email=enak_username_email)

        elif db.query(User).filter_by(user_email=email).first():
            enak_email = 'ta email že obstaja'
            return render_template('login.html', enak_email=enak_email)

        elif db.query(User).filter_by(user_name=user_name).first():
            enak_username = 'ta username že obstaja'
            return render_template('login.html', enak_username=enak_username)




@app.route('/signin', methods=['POST'])
def signin():
    return render_template('about_me.html', tukej='prišel iz /signin routa')



if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)










