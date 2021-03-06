import random

def choose_secret_word(ime_datoteke):
    with open(ime_datoteke, 'r', encoding='utf-8') as file:  # iz 'words.txt' preberemo besede in jih damo v seznam
        words = file.read().splitlines()  # iz 'words.txt' preberemo besede in jih damo v seznam
    return random.choice(words)

def show_known_letters(secret_word, guessed_letters):
    word = ''
    if guessed_letters:
        for letter in secret_word:
            if letter in guessed_letters:
                word += f'{letter} '
            else:
                word += f'_ '
    else:
        word = '_ ' * len(secret_word)
    return word


def check_guessed_letter(letter):
    if len(letter) != 1:
        return False
    elif not letter.isalpha():
        return False
    else:
        return True


class Hangman:
    def __init__(self, secret_word='',current_guessed_letter='', guessed_letters='',
                 number_of_tries=0, missed_tries=0, user_name='', correct_letters=''):
        self.user_name = user_name
        self.secret_word = secret_word
        self.current_guessed_letter = current_guessed_letter
        self.guessed_letters = guessed_letters
        self.number_of_tries = number_of_tries
        self.missed_tries = missed_tries
        self.correct_letters = correct_letters


    def correct_letter(self): #preveri ali je ugibana črka v besedi ali ne (če je v besedi vrne true, drugače false
        if self.current_guessed_letter.upper() in self.secret_word.upper():
            self.correct_letters = self.correct_letters + self.current_guessed_letter.lower()
            return True
        else:
            return False


    def add_tries(self): #prišteje poizkus vsem poizkusom, in prišteje poizkus napačnim poizkusom, če le ta ni pravilen
        if self.number_of_tries == None:
            self.number_of_tries = 1
        else:
            self.number_of_tries += 1

        if not self.correct_letter():
            if self.missed_tries == None:
                self.missed_tries = 1
            else:
                self.missed_tries += 1




    def add_letter_to_guessed_letters(self): #doda črko v mmnožico poizkusov, toda le če je poizkus ena sama črka

        if self.guessed_letter_valid():
            self.guessed_letters = self.guessed_letters + self.current_guessed_letter


    def guessed_letter_valid(self): #preveri ali je poizkus veljaven
        if len(self.current_guessed_letter) != 1:
            return False
        elif not self.current_guessed_letter.isalpha():
            return False
        else:
            return True



    def check_win(self): #preveri ali je igralec že zmagal
        if len(set(self.secret_word)) == len(set(self.correct_letters)):
            return True
        return False

    def check_lose(self):
        if not self.check_win() and self.missed_tries == 7:
            return True
        else:
            return False

    def show_known_letters(self):
        word = ''
        if self.guessed_letters:
            for letter in self.secret_word:
                if letter in self.guessed_letters:
                    word += f'{letter} '
                else:
                    word += f'_ '
        else:
            word = '_ ' * len(self.secret_word)
        return word

    def save_to_database(self, db):
        if self.guessed_letter_valid():
            self.add_tries()
            self.add_letter_to_guessed_letters()
            self.correct_letter()

            #if self.check_lose():
             #   db.guessed_letters = ''
              #  db.number_of_tries = 0
              #  db.missed_tries = 0
              #  db.secret_word = ''
              #  db.correct_letters = ''
              #  db.save()
              #  return 'izgubil'

            #elif self.check_win():
            #    db.guessed_letters = ''
            #    db.number_of_tries = 0
            #    db.missed_tries = 0
            #    db.secret_word = ''
            #    db.correct_letters = ''
            #    db.save()
            #    return 'zmaga'


            db.guessed_letters = self.guessed_letters
            db.number_of_tries = self.number_of_tries
            db.missed_tries = self.missed_tries
            db.secret_word = self.secret_word
            db.correct_letters = self.correct_letters

            db.save()

    def set_to_zero(self, db):
        if self.check_lose() or self.check_win():
            db.guessed_letters = ''
            db.number_of_tries = 0
            db.missed_tries = 0
            db.secret_word = ''
            db.correct_letters = ''
            db.save()








    #def save_to_database(self):


app = Hangman(secret_word='andraz', current_guessed_letter='ž', guessed_letters='and', number_of_tries=0,
              missed_tries=0)
print(f'check win {app.check_win()}')
print(f'check lose {app.check_lose()}')
if app.check_lose():
    print('izgubil je')
else:
    print('ni izgubil')
print(app.guessed_letter_valid())
print(app.correct_letter())
print(app.add_tries())
print(app.add_letter_to_guessed_letters())

print(app.check_win())
print(app.secret_word)
print(app.current_guessed_letter)
print(app.guessed_letters)
print(app.number_of_tries)
print(app.missed_tries)

print('-' * 50)
app = Hangman(secret_word='andraz', current_guessed_letter='o', guessed_letters='and', number_of_tries=0,
              missed_tries=0)

print(app.guessed_letter_valid())
print(app.correct_letter())
print(app.add_tries())
print(app.add_letter_to_guessed_letters())

print(app.check_win())
print(app.secret_word)
print(app.current_guessed_letter)
print(app.guessed_letters)
print(app.number_of_tries)
print(app.missed_tries)





krneki = 'krneki'

krneki = krneki + 'a'
print(krneki)















