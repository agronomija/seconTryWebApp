import random
def choose_secret_word(ime_datoteke):
    with open(ime_datoteke, 'r', encoding='utf-8') as file:  # iz 'words.txt' preberemo besede in jih damo v seznam
        words = file.read().splitlines()  # iz 'words.txt' preberemo besede in jih damo v seznam
    return random.choice(words)



class Hangman:
    def __init__(self, secret_word=None,current_guessed_letter=None, guessed_letters=set(),
                 number_of_tries = 0, missed_tries=0, user_name=None):
        self.user_name = user_name
        self.secret_word = secret_word
        self.current_guessed_letter = current_guessed_letter
        self.guessed_letters = guessed_letters
        self.number_of_tries = number_of_tries
        self.missed_tries = missed_tries
        self.correct_letters = []


    def correct_letter(self): #preveri ali je ugibana črka v besedi ali ne (če je v besedi vrne true, drugače false
        if self.current_guessed_letter.upper() in self.secret_word.upper():
            self.correct_letters.append(self.current_guessed_letter.lower())
            return True
        else:
            return False


    def add_tries(self): #prišteje poizkus vsem poizkusom, in prišteje poizkus napačnim poizkusom, če le ta ni pravilen
        self.number_of_tries += 1
        if not self.correct_letter():
            self.missed_tries += 1


    def add_letter_to_guessed_letters(self): #doda črko v mmnožico poizkusov, toda le če je poizkus ena sama črka

        if self.guessed_letter_valid():
            self.guessed_letters.add(self.current_guessed_letter)


    def guessed_letter_valid(self): #preveri ali je poizkus veljaven
        if len(self.current_guessed_letter) != 1:
            return False
        elif not self.current_guessed_letter.isalpha():
            return False
        else:
            return True


    def show_looking_word(self):
        word = ''
        for letter in self.secret_word:
            if letter in self.guessed_letters:
                word += f'{letter} '
            else:
                word += f'_ '
        return word


    def check_win(self): #preveri ali je igralec že zmagal
        if len(set(self.secret_word)) == len(set(self.correct_letters)):
            return True
        return False

    #def save_to_database(self):


app = Hangman(secret_word='andraz', current_guessed_letter='ž', guessed_letters={'n', 'd', 'r', 'z'}, number_of_tries=0,
              missed_tries=0)

print(app.guessed_letter_valid())
print(app.correct_letter())
print(app.add_tries())
print(app.add_letter_to_guessed_letters())
print(app.show_looking_word())
print(app.check_win())
print(app.secret_word)
print(app.current_guessed_letter)
print(app.guessed_letters)
print(app.number_of_tries)
print(app.missed_tries)





















