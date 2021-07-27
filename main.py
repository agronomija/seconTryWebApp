from flask import Flask, render_template, request, redirect, url_for, make_response
from sqla_wrapper import SQLAlchemy
from hangman import Hangman, choose_secret_word, show_known_letters, check_guessed_letter



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
        if piskotek:
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
            user = user = db.query(User).filter_by(user_name=piskotek).first()

        return render_template('fizz-buzz.html',)


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)










