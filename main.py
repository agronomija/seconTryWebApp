from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy
from hangman import Hangman, choose_secret_word, show_known_letters, check_guessed_letter
import os


app = Flask(__name__)
db = SQLAlchemy("sqlite:///db.sqlite")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    secret_word = db.Column(db.String, unique=False)
    current_guessed_letter = db.Column(db.String, unique=False)
    guessed_letters = db.Column(db.String, unique=False)
    number_of_tries = db.Column(db.Integer, unique=False)
    missed_tries = db.Column(db.Integer, unique=False)
    correct_letters = db.Column(db.String, unique=False)
    user_name = db.Column(db.String, unique=True)
    user_password = db.Column(db.String, unique=False)
    user_email = db.Column(db.String, unique=True)
    user_fb = db.Column(db.String, unique=True)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, unique=False)
    name = db.Column(db.String, unique=False)


class Private_message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, unique=False)
    sender = db.Column(db.String, unique=False)
    reciever = db.Column(db.String, unique=False)
    title = db.Column(db.String, unique=False)


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
            user.save()
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




@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'GET':
        piskotek = request.cookies.get('user_name_test')
        if piskotek:
            vpisan = f'Vpisan je {piskotek}, če se želite prijaviti z drugim računom se morate najprej odjaviti.'
            return render_template('signin.html', vpisan=vpisan)
        else:
            return render_template('signin.html')


@app.route('/search_user', methods=['POST'])
def search_user():
    email = request.form.get('user-email')
    print(email)
    password = request.form.get('user-password')
    print(password)

    user = db.query(User).filter_by(user_email=email).first()



    if not user:
        ni_userja = 'Pod temi podatki ni shranjenega nobenega uporabnika'
        return render_template('signin.html', ni_userja=ni_userja)

    if user and user.user_password == password:
        response = make_response(render_template('about_me.html', user_name=user.user_name))
        response.set_cookie('user_name_test', user.user_name)
        print(user.user_name)
        return response


    return render_template('signin.html', obvestilo='Pod tem emailom in passwordom ni nobenega uporabnika, '
                                                        'oskusite znova.')


@app.route('/logout')
def logout():

    response = make_response(render_template('about_me.html', obvestilo_o_izpisu='Uspešno ste se izpisali'))
    response.set_cookie('user_name_test', expires=0)
    return response


@app.route('/tic-tac-toe')
def tic_tac():
    return render_template('tic-tac-toe.html')


@app.route('/hangman', methods=['POST', 'GET'])
def hangman():
    piskotek = request.cookies.get('user_name_test')
    ni_piskotka = 'Za nadaljevanje se morate vpisati'
    beseda = choose_secret_word('words.txt')
    if request.method == 'GET':
        if piskotek and db.query(User).filter_by(user_name=piskotek).first(): #nazadnje dodal
            user = db.query(User).filter_by(user_name=piskotek).first()
            if not user.secret_word:
                user.secret_word = beseda

                print('število number of tries...', user.number_of_tries)
                user.save()
                prikaz_besede = show_known_letters(beseda, user.guessed_letters)
                return render_template('hangman.html', piskotek=piskotek, prikaz_besede=prikaz_besede)
            if user.secret_word:
                prikaz_besede = show_known_letters(user.secret_word, user.guessed_letters)
                dosedanji_poizkusi = user.number_of_tries
                zgreseni = user.missed_tries
                dosedanje_crke = user.guessed_letters
                return render_template('hangman.html', piskotek=piskotek, prikaz_besede=prikaz_besede,
                                       dosedanji_poizkusi=dosedanji_poizkusi, zgreseni=zgreseni, dosedanje_crke=dosedanje_crke)
        else:
            return render_template('hangman.html', ni_piskotka=ni_piskotka)

    elif request.method == 'POST':
        uporabnik = request.cookies.get('user_name_test')
        ugibana_crka = request.form.get('ugibana-crka')
        if check_guessed_letter(ugibana_crka):
            user = db.query(User).filter_by(user_name=uporabnik).first() #poiscemo uporabnika s dolocenim usernamom v bazi


            if user.guessed_letters == None: #če je ravno začel igro

                user.current_guessed_letter = ugibana_crka
                user.guessed_letters = ''
                user.number_of_tries = 0
                user.missed_tries = 0
                user.correct_letters = ''

                pregled = Hangman(secret_word=user.secret_word, current_guessed_letter=ugibana_crka,
                                  guessed_letters=user.guessed_letters, number_of_tries=user.number_of_tries,
                                  missed_tries=user.missed_tries, correct_letters=user.correct_letters)


                pregled.save_to_database(user)

                if pregled.check_lose():
                    iskana_beseda = pregled.secret_word
                    poizkusi = pregled.number_of_tries
                    napacni_poizkusi = pregled.missed_tries
                    poraz = 'poraz'

                    pregled.set_to_zero(user)

                    return render_template('hangman.html', iskana_beseda=iskana_beseda, uporabnik=uporabnik,
                                           poizkusi=poizkusi,
                                           napacni_poizkusi=napacni_poizkusi, poraz=poraz)

                elif pregled.check_win():

                    iskana_beseda = pregled.secret_word
                    poizkusi = pregled.number_of_tries
                    napacni_poizkusi = pregled.missed_tries
                    zmaga = 'zmaga'

                    pregled.set_to_zero(user)

                    return render_template('hangman.html', iskana_beseda=iskana_beseda, uporabnik=uporabnik,
                                            poizkusi=poizkusi,
                                            napacni_poizkusi=napacni_poizkusi, zmaga=zmaga)


                else:

                    iskana_beseda = pregled.secret_word
                    poizkusi = pregled.number_of_tries
                    napacni_poizkusi = pregled.missed_tries
                    igraj_naprej = 'nadaljuj'

                    print(f'user.guessed-letters == None....iskana beseda: {iskana_beseda}, poizkusi: {poizkusi}, napacni_poizkusi: {napacni_poizkusi}')
                    prikaz = pregled.show_known_letters()

                    return render_template('hangman.html', uporabnik=uporabnik,
                                           poizkusi=poizkusi,
                                           napacni_poizkusi=napacni_poizkusi, igraj_naprej=igraj_naprej, prikaz=prikaz)




            elif user.guessed_letters != None:  # če je že igral prej

                pregled = Hangman(secret_word=user.secret_word, current_guessed_letter=ugibana_crka,
                                  guessed_letters=user.guessed_letters, number_of_tries=user.number_of_tries,
                                  missed_tries=user.missed_tries, correct_letters=user.correct_letters)

                pregled.save_to_database(user)

                if pregled.check_lose():
                    iskana_beseda = pregled.secret_word
                    poizkusi = pregled.number_of_tries
                    napacni_poizkusi = pregled.missed_tries
                    poraz = 'poraz'

                    pregled.set_to_zero(user)
                    return render_template('hangman.html', iskana_beseda=iskana_beseda, uporabnik=uporabnik,
                                           poizkusi=poizkusi,
                                           napacni_poizkusi=napacni_poizkusi, poraz=poraz)

                elif pregled.check_win():

                    iskana_beseda = pregled.secret_word
                    poizkusi = pregled.number_of_tries
                    napacni_poizkusi = pregled.missed_tries
                    zmaga = 'zmaga'

                    pregled.set_to_zero(user)
                    return render_template('hangman.html', iskana_beseda=iskana_beseda, uporabnik=uporabnik,
                                           poizkusi=poizkusi,
                                           napacni_poizkusi=napacni_poizkusi, zmaga=zmaga)


                else:
                    dosedanje_crke = user.guessed_letters
                    iskana_beseda = pregled.secret_word
                    poizkusi = pregled.number_of_tries
                    napacni_poizkusi = pregled.missed_tries
                    igraj_naprej = 'nadaljuj'
                    prikaz = pregled.show_known_letters()
                    print(f'user.guessed-letters != None.....iskana beseda: {iskana_beseda}, poizkusi: {poizkusi}, napacni_poizkusi: {napacni_poizkusi}')
                    return render_template('hangman.html', uporabnik=uporabnik,
                                           poizkusi=poizkusi,
                                           napacni_poizkusi=napacni_poizkusi, igraj_naprej=igraj_naprej, prikaz=prikaz,
                                           dosedanje_crke=dosedanje_crke)
        else:
            napacen_znak = 'Vnesli ste napačen znak, sprejemamo le črke.'
            return render_template('hangman.html', napacen_znak=napacen_znak)

@app.route('/fizz-buzz', methods=['GET', 'POST'])
def fizz_buzz():
    piskotek = request.cookies.get('user_name_test')
    if request.method == 'GET':
        if piskotek:
            user = db.query(User).filter_by(user_name=piskotek).first()
            if not user.user_fb:
                zacetek = 'start'
                return render_template('fizz-buzz.html', zacetek=zacetek)

        return render_template('fizz-buzz.html',)


@app.route('/message', methods=['GET', 'POST'])
def message():
    piskotek = request.cookies.get('user_name_test')

    #if request.method == 'GET' and not piskotek:
        #return render_template('messages.html')

    if request.method == 'GET':
        messages = db.query(Message).all()
        return render_template('messages.html', piskotek=piskotek, messages=messages)

    #elif request.method == 'GET' and not piskotek:
     #   render_template('messages.html')

    elif request.method == 'POST':
        message = request.form.get('message')
        messages = Message(message=message, name=piskotek)
        messages.save()

        messages = db.query(Message).all()

        return render_template('messages.html', messages=messages, piskotek=piskotek)


@app.route('/profile')
def profile():
    piskotek = request.cookies.get('user_name_test')
    if not piskotek:
        ni_userja = 'Pod tem cookiejam ni shranjenega nobenega userja, znova se prijavi s pravim profilom'
        return render_template('profile.html', ni_userja=ni_userja)

    elif piskotek and not db.query(User).filter_by(user_name=piskotek).first():
        je_piskotek_ni_userja = 'Pod tem piskotkom ni prijavljen noben user, zato se znova oprijavite'
        return render_template('profile.html', je_piskotek_ni_userja=je_piskotek_ni_userja)

    else:
        user = db.query(User).filter_by(user_name=piskotek).first()
        user_name = user.user_name
        user_email = user.user_email

        return render_template('profile.html', user_name=user_name, user_email=user_email)

@app.route('/users')
def user_search():
    users = db.query(User).all()
    print(users[0].user_name)
    piskotek = request.cookies.get('user_name_test')

    return render_template('users.html', users=users, piskotek=piskotek)




@app.route('/users/<user_name>')
def send_message(user_name):
    piskotek = request.cookies.get('user_name_test')
    registreraj_se = 'za nadaljevanje se je potrebno registrirati'
    if piskotek:
        return render_template('user_message.html', user_name=user_name, piskotek=piskotek)
    return render_template('user_message.html', registreraj_se=registreraj_se)


@app.route('/sent_unsent', methods=['GET','POST'])
def sent_unsent():
    #reciever = request.form.get('reciever')
    sender = request.cookies.get('user_name_test')
    message = request.form.get('message')
    #title = reciever.form.get('title')
    #user = db.query(User).get(reciever)
    if request.method == 'POST':
        reciever = request.form.get('reciever')
        message = request.form.get('message')
        title = request.form.get('title')
        user = db.query(User).filter_by(user_name=reciever).first()
        if not user:
            no_user = 'Pod tem imenom ni nobenega uporabnika'
            return render_template('sent_unsent.html', no_user=no_user)

        else:
            sporocilo = Private_message(message=message, reciever=reciever, sender=sender, title=title)
            sporocilo.save()

            return render_template('sent_unsent.html', reciever=reciever)



@app.route('/recieved_messages')
def recieved_messages():
    sporocila = db.query(Private_message).all()
    piskotek = request.cookies.get('user_name_test')
    return render_template('recieved_messages.html', sporocila=sporocila, piskotek=piskotek)


@app.route('/sent_messages')
def sent_messages():
    sporocila = db.query(Private_message).all()
    piskotek = request.cookies.get('user_name_test')
    return render_template('sent_messages.html', sporocila=sporocila, piskotek=piskotek)

@app.route('/cv')
def cv():
    return render_template('CV.html')


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)










