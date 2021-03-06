
import random

class GameIO:
    
    MARGIN = "          "
    L_BORDER = MARGIN + "|| "
    R_BORDER = " ||\n"
    SEPARATOR = " | "
    GO_RED = '\033[31m'
    GO_GREEN = '\033[32m'
    RESET_COL = '\033[0m'

    def __init__(self, word_length):
        pass

    @staticmethod
    def clue_cmpnts_output(clue):
        out = []
        for i, letter in enumerate(clue.get_word()):
            if clue.get_cmpnts()[i] == Clue.LETTER_IN_POS:
                out.append(GameIO.GO_GREEN + letter.upper() + GameIO.RESET_COL)
            elif clue.get_cmpnts()[i] == Clue.LETTER_NOT_IN:
                out.append(GameIO.GO_RED + letter.upper() + GameIO.RESET_COL)
            elif clue.get_cmpnts()[i] == Clue.LETTER_IN_NO_POS:
                out.append(letter.upper())
            else:
                out = ""
        return out

    @staticmethod
    def clue_output(clue):
        word_length = len(clue.get_word())
        h_border = GameIO.MARGIN + "==" + word_length * "====" + "=\n"
        return h_border + GameIO.L_BORDER \
               + GameIO.SEPARATOR.join(GameIO.clue_cmpnts_output(clue)) \
               + GameIO.R_BORDER + h_border        

    @staticmethod
    def clue_cmpnt_input(letter):
        letter = letter.lower()
        if letter == 'y':
            convert = Clue.LETTER_IN_POS
        elif letter == 'n':
            convert = Clue.LETTER_NOT_IN
        elif letter == 'e':
            convert = Clue.LETTER_IN_NO_POS     
        else:
            raise ValueError()
        return convert
       
    @staticmethod
    def clue_input(guess):
        valid_answer = False
        while not valid_answer:
            clue_string = GameIO.input(f"My guess is {guess}, what is your answer\n"\
               + "('y' for 'yes', 'n' for 'no' and 'e' for 'elsewhere', "\
               + "separated by spaces)?\n  ")
            try:
                cmpnts = tuple(map(GameIO.clue_cmpnt_input, clue_string.split()))
                if len(cmpnts)==len(guess):
                    pos = 0
                    while pos<len(cmpnts) and (cmpnts[pos] in Clue.answer_cmpnts):
                        pos += 1
                    valid_answer = pos==len(cmpnts)
            except ValueError:
                pass
            if not valid_answer:
                GameIO.output("Your answer is too long or contains invalid characters")
        return Clue(guess, cmpnts)
    
    @staticmethod
    def word_input():
        return GameIO.input('Please enter your next guess: ').lower()
    
    @staticmethod
    def secret_msg_output(word_size):
        GameIO.input(f"Press enter when you've chosen a {word_size}-letter" \
              + "word from the word base;\nbut don't tell me what it is!")
    
    @staticmethod
    def output(msg):
        print(msg)
        
    @staticmethod 
    def input(msg):
        return input(msg)

class Clue(object):
    
    LETTER_IN_POS = 0
    LETTER_IN_NO_POS = 1 
    LETTER_NOT_IN = 2
    answer_cmpnts = {LETTER_IN_POS, LETTER_IN_NO_POS, LETTER_NOT_IN}
    
    def __init__(self, guess, clue_cmpnts):
        self.guess = guess
        self.clue_cmpnts = clue_cmpnts
        
    def __str__(self):
        return GameIO.clue_output(self)        
    
    def __repr__(self):
        return f'Clue({self.guess}, {self.clue_cmpnts})'

    def __eq__(self, other):
        return self.guess == other.guess and self.clue_cmpnts == other.clue_cmpnts
    
    def get_word(self):
        return self.guess
    
    def get_cmpnts(self):
        return self.clue_cmpnts
    
    def is_winner(self):
        if self.clue_cmpnts == (Clue.LETTER_IN_POS,)*len(self.clue_cmpnts):
            return True
        else:
            return False
    
    @staticmethod
    def generate_clue(secret_word : str, guessed_word : str):
        """
        Input:

        secret_word: string 
        
        """
        p=()
        n=len(secret_word)
        d={}
        for i in range(n):
            s=secret_word[i]
            g=guessed_word[i]
            d[s]=-1 if s not in d else d[s]-1
            d[g]=1 if g not in d else d[g]+1
        for i in range(n):
            if secret_word[i]==guessed_word[i]:
                p=p+(Clue.LETTER_IN_POS,)
            elif guessed_word[i] in secret_word:
                if d[guessed_word[i]]>0:
                    p=p+(Clue.LETTER_NOT_IN,)
                    d[guessed_word[i]]=d[guessed_word[i]]-1
                else:
                    p=p+(Clue.LETTER_IN_NO_POS,)
            else:
                p=p+(Clue.LETTER_NOT_IN,)
        return Clue(guessed_word,p)
        

class Storage(object):

    def __init__(self):
        self.storageList = []
        
    def add_clue(self, clue):
        self.storageList.append(clue)

    def is_empty(self):
        if len(self.storageList) == 0:
            return True
        else:
            return False

    def __contains__(self, word):  #https://docs.python.org/3/reference/datamodel.html#object.__contains__
        for i in range(len(self.storageList)):
            if self.storageList[i].guess == word:
                return True
        return False
            
    def is_compatible_with_clues(self, word):
        f=0
        while f<len(self.storageList) and self.storageList[f]==Clue.generate_clue(word,self.storageList[f].get_word()):
            f=f+1
        return f==len(self.storageList)
       
    def __repr__(self):
        return f'Storage({self.storageList})'


def test_computer_player():
    wordlist = list(map(lambda x: x.strip(),
                       filter(lambda x: len(x)==6, open('lemario.txt', encoding='utf-8'))))
    random.seed(8)
    storage = Storage()
    cplay = ComputerPlayer(wordlist, storage)
    
    secret = 'folga'
    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)
    
    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    storage = Storage()
    cplay = ComputerPlayer(wordlist, storage)
    secret = 'cinco'
    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)


    storage = Storage()
    cplay = ComputerPlayer(wordlist, storage)
    secret = 'XXXXX'
    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    new = cplay.next_guess()
    print(f'{new}....', end='')
    assert storage.is_compatible_with_clues(new)
    print('OK')
    clue = Clue.generate_clue(secret, new)
    storage.add_clue(clue)

    try:
        new = cplay.next_guess()
        assert False
    except AssertionError as e:
        raise(e)
    except Exception as e:
        print('OK, excepci??n capturada')
    
    print('OK')


def main():
    from os import path
    found = False
    while not found:
        dict_filename = GameIO.input(\
"""Enter the name of the dictionary file
Press enter to use the default file, i.e. lemario.txt: """\
                             )
        if not dict_filename: 
            dict_filename = "lemario.txt"
        if path.exists(dict_filename): 
            found = True
        else: 
            GameIO.output("File not found. Please try again")

    replies = {"c", "h"}
    foundp = founds = False  
    while not (foundp and founds):
        while not foundp:
            p_type = GameIO.input("Enter the player type, h for human or c for computer:\n"\
                  + "Press enter to use default player, i.e. human: ")
            if not p_type: 
                p_type = 'h'
            if p_type in replies: 
                foundp = True
            else: 
                GameIO.output("Invalid player type. Please try again.")
        while not founds:
            s_type = GameIO.input("Enter the server type, h for human or c for computer:\n"\
                  + "Press enter to use default server, i.e. computer: ")
            if not s_type: 
                s_type = 'c'
            if s_type in replies: 
                founds = True   
            else: 
                GameIO.output("Invalid server type. Please try again.")
        if p_type == s_type == "h":
            GameIO.output("Human player and human server not an option. Please try again.")
            founds = foundp = False
    
    word_length = "not_a_number"
    while word_length and not word_length.isdigit():
        word_length = GameIO.input("Enter the word length (a positive unsigned integer):\n"\
             + "Press enter to use default word length, i.e. 5: ")
    if not word_length: word_length = 5
    
    attempts = "not_a_number"
    while attempts and not attempts.isdigit():
        attempts = GameIO.input("Enter the allowed number of attempts (a positive unsigned integer):\n"\
             + "Press enter to use default word length, i.e. 6: ")
    if not attempts: attempts = 6

    a_seed = "not_a_number"
    while a_seed and not a_seed.isdigit():
        a_seed = GameIO.input("Enter the seed value (a positive unsigned integer):\n"\
             + "Press enter to let the system randomly choose a seed: ")
        # apparently, random is a global variable
    if not a_seed: 
        random.seed()
    else: 
        random.seed(a_seed)

    game = Game(dict_filename, p_type=="h", s_type=="c", word_length, attempts)
    game.play()
