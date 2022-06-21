import platform
if platform.system().lower() == 'windows':
    import os
    os.system("")  # enables ansi escape characters in terminal (supposedly) 
import random, io
s
class Game(object):

    # precondition: not (client_is_human==True and server_is_computer==False)
    def __init__(self, filename, client_is_human, server_is_computer, word_length, max_attempts):

        self.wordlst = []
        with open(filename, 'r', encoding = 'utf8') as rows:
            for row in rows:
                if len(row.strip()) == word_length:
                    self.wordlst.append(row.strip())
        self.word_length = word_length
        self.max_attemps = max_attemps
        self.storage = Storage()
        if client_is_human == True:
            self.player = HumanPlayer(self.wordlst, self.storage)
        else:
            self.player = ComputerPlayer(self.wordlst, self.storage)
        if server_is_computer == True:
            self.server = ComputerServer(self.wordlst)
        else:
            self.server = HumanServer(self.wordlst)
        self.play()

    def play(self):
        
        attemps = 0
        secret = self.server.generate_secret()
        while attemps <= self.max.attemps:
            guess = self.player.next_guess()
            self.server.get_clue(guess)
        final_msg = "" if self.server.get_secret() == None \
                    else "The secret word was " + self.server.get_secret() + "."
        GameIO.output(final_msg)
        if not clue.is_winner():
            GameIO.output(f"Game over. Better luck to the {self.player} next time!")
        else:
            GameIO.output(f"Congratulations to the {self.player} for finding the secret word.")

class ComputerServer(object):
    
    def __init_(self, wordlst):
        self.wordlst = wordlst
        self.secret = None
        self.generate_secret()
        
    def generate_secret(self):
        self.secret = self.wordlst[random.randint(0,len(self.wordlst)-1)]
        
    def get_secret(self):
        return self.secret
    
    def get_clue(self, guess):
        return GameIO.clue_output(guess)
 
class HumanServer(object):

    def __init__(self,wordlst):
        self.word_length=len(wordlst[0])
        self.secret=None
        self.wordlst = wordlst
        self.generate_secret()
        
    def generate_secret(self):
        return GameIO.secret_msg_output(self.word_length)
    
    def get_clue(self, guess):
        return GameIO.clue_output(guess)

# computerPlayer está cambiada

class ComputerPlayer(object):

    player = 'computer'
    
    def __init__(self, wordlst, storage):
        self.wordlst = wordlst
        self.storage = storage
        
    def next_guess(self):
        """
        input: 

        self - contains a storage instance & a wordlist*

        *the wordlist contains all suitable words for the case
        this means that we only consider words of a certain length
        in this case, the length is 6
        ---------

        output: 

        str - a feasible solution considering word length 
        and being compatible with clues already given 
        """
        pos = 0
        while pos < len(self.wordlst):
            if self.storage.__contains__(self.wordlst[pos]) or not self.storage.is_compatible_with_clues(self.wordlst[pos]):
                pos += 1
            else:
                return self.wordlst[pos]
        raise Exception('It is not possible to find another candidate')    
        
    
    def __str__(self):
        return ComputerPlayer.player

# HumanPlayer está cambiada pero daba error - 21:31 creo q ya no

class HumanPlayer(object):

    # Errors
    UNKNOWN_WORD_MSG = "The word you guessed is not in the dictionary"
    # Warnings
    MSG_PREFIX = "Warning: "
    REPEAT_WORD_MSG = MSG_PREFIX + "you have already guessed that word"
    INCONSISTENT_WORD_MSG = MSG_PREFIX \
            + "the word you guessed is not compatible with the previous clues"
    player = 'human' 

    def __init__(self, wordlst, storage):
        self.wordlst = wordlst
        self.storage = storage
        
    def next_guess(self):
        """
        input: same as in computerplayer, a wordlist and an instance of Storage class

        ----

        output: a word that is a feasible solution OR an exception describing an error 
        that's considered in this class
        """
        guess = GameIO.word_input()
        if len(guess) != len(self.wordlst[0]):
            raise Exception(HumanPlayer.UNKNOWN_WORD_MSG)
        elif guess not in self.wordlst:
            if guess in self.storage:
                raise Exception(HumanPlayer.REPEAT_WORD_MSG)
            else:
                raise Exception(HumanPlayer.INCONSISTENT_WORD_MSG)
        return guess
    
    def __str__(self):
        return HumanPlayer.player

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
        if word in self.storageList:
            return True
        else: 
            return False
    #esta de debajo seguro que se puede hacer mejor :D  
    def is_compatible_with_clues(self, word):
        f=0
        while f<len(self.storageList) and self.storageList[f]==Clue.generate_clue(word,self.storageList[f].get_word()):
            f=f+1
        return f==len(self.storageList)
       
    def __repr__(self):
        return f'Storage({self.storageList})'

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
        
class MyInput():
    def __init__(self, answers):
        self.pos = 0
        self.answers = answers
    def input(self, msg):
        if self.pos<len(self.answers):
            ans = self.answers[self.pos]
            self.pos += 1
        else:
            ans = ''
        return ans

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
        print('OK, excepción capturada')
    
    print('OK')

def test_human_player():
    wordlist = list(map(lambda x: x.strip(),
                    filter(lambda x: len(x)==6, open('lemario.txt', encoding='utf8'))))
    old_input = GameIO.input
    old_output = GameIO.output    
    secret = 'folga'
    
    test = ['flaon', 'folia', 'folla', 'folga']
    random.seed(8)
    storage = Storage()
    hplay = HumanPlayer(wordlist, storage)
    myinput = MyInput(test)
    GameIO.input = myinput.input
    sout = io.StringIO("")
    GameIO.output = lambda x: sout.write(f'{x}')
    try:
        
        for _ in range(len(test)):
            word = hplay.next_guess()
            storage.add_clue(Clue.generate_clue(secret, word))
        assert sout.getvalue() == ''
    finally:
        GameIO.input = old_input
        GameIO.output = old_output
    
    
    test = ['flaon', 'flaon']
    random.seed(8)
    storage = Storage()
    hplay = HumanPlayer(wordlist, storage)
    myinput = MyInput(test)
    GameIO.input = myinput.input
    sout = io.StringIO("")
    GameIO.output = lambda x: sout.write(f'#{x}#')
    try:
        secret = 'folga'
        for _ in range(len(test)):
            word = hplay.next_guess()
            storage.add_clue(Clue.generate_clue(secret, word))
        #print(f':{sout.getvalue()}:')
        assert sout.getvalue() == '#Warning: you have already guessed that word#'
    finally:
        GameIO.input = old_input
        GameIO.output = old_output
    
    test = ['flaon', 'flaco']
    random.seed(8)
    storage = Storage()
    hplay = HumanPlayer(wordlist, storage)
    myinput = MyInput(test)
    GameIO.input = myinput.input
    sout = io.StringIO("")
    GameIO.output = lambda x: sout.write(f'#{x}#')
    try:
        secret = 'folga'
        for _ in range(len(test)):
            word = hplay.next_guess()
            storage.add_clue(Clue.generate_clue(secret, word))
        #print(f':{sout.getvalue()}:')
        assert sout.getvalue() == '#Warning: the word you guessed is not compatible with the previous clues#'
    finally:
        GameIO.input = old_input
        GameIO.output = old_output
        
    test = ['flaon', 'flaco', 'flaon', 'folia', 'folla', 'flaco', 'folga']
    random.seed(8)
    storage = Storage()
    hplay = HumanPlayer(wordlist, storage)
    myinput = MyInput(test)
    GameIO.input = myinput.input
    sout = io.StringIO("")
    GameIO.output = lambda x: sout.write(f'#{x}#')
    try:
        secret = 'folga'
        for _ in range(len(test)):
            word = hplay.next_guess()
            storage.add_clue(Clue.generate_clue(secret, word))
        #print(f':{sout.getvalue()}:')
        assert sout.getvalue() == '#Warning: the word you guessed is not compatible with the previous clues#'+\
            '#Warning: you have already guessed that word#'+ \
            '#Warning: you have already guessed that word#'
    finally:
        GameIO.input = old_input
        GameIO.output = old_output
        
    print('OK')

def test_computer_server():
    wordlst = ['avion']


    old_input = GameIO.input
    old_output = GameIO.output
    try:
        cs = ComputerServer(wordlst)
        cs.generate_secret()
        assert cs.get_secret() == 'avion'
        sout = io.StringIO("")
        GameIO.output = lambda x: None
        clue = cs.get_clue('altar')
        assert clue.get_word() == 'altar' and list(clue.get_cmpnts()) == [0,2,2,2,2]

    finally:
        GameIO.input = old_input
        GameIO.output = old_output

    print('OK')

def test_human_server():
    wordlst = list(map(lambda x: x.strip(),
                       filter(lambda x: len(x)==5, open('lemario.txt', encoding='utf8'))))


    old_input = GameIO.input
    old_output = GameIO.output
    try:
        hs = HumanServer(wordlst)
        test = ['y y y b b', 'y y n n e y', 'y y y', 'y y n n e']
        myinput = MyInput(test)
        GameIO.input = myinput.input
        sout = io.StringIO("")
        GameIO.output = lambda x: sout.write(f'#{x}#')
        res = hs.get_clue('avion')
        assert res.get_word() == 'avion' and list(res.get_cmpnts()) == [0, 0, 2, 2, 1]
        assert sout.getvalue() == '#Your answer is too long or contains invalid characters##Your answer is too long or contains invalid characters##Your answer is too long or contains invalid characters##          =======================\n          || \x1b[32mA\x1b[0m | \x1b[32mV\x1b[0m | \x1b[31mI\x1b[0m | \x1b[31mO\x1b[0m | N ||\n          =======================\n#'
#         assert sout.getvalue() == \
#             """#Press enter when you've chosen a 4-letterword from the word base;
# but don't tell me what it is!#"""
    finally:
        GameIO.input = old_input
        GameIO.output = old_output

    print('OK')

def test_play():
    old_output = GameIO.output
    sout = io.StringIO("")
    random.seed(8)
    GameIO.output = lambda x: sout.write(f'#{x}#\n')
    try:
        game = Game('lemario.txt', False, True, 5, 100)
        game.play()
        #print(repr(sout.getvalue()))
        assert sout.getvalue() == '#          =======================\n          || \x1b[31mM\x1b[0m | O | N | \x1b[31mS\x1b[0m | \x1b[31mE\x1b[0m ||\n          =======================\n#\n#          =======================\n          || \x1b[31mI\x1b[0m | \x1b[31mN\x1b[0m | \x1b[31mG\x1b[0m | \x1b[32mO\x1b[0m | \x1b[32mN\x1b[0m ||\n          =======================\n#\n#          =======================\n          || \x1b[31mC\x1b[0m | A | L | \x1b[32mO\x1b[0m | \x1b[32mN\x1b[0m ||\n          =======================\n#\n#          =======================\n          || \x1b[32mF\x1b[0m | \x1b[32mL\x1b[0m | \x1b[32mA\x1b[0m | \x1b[32mO\x1b[0m | \x1b[32mN\x1b[0m ||\n          =======================\n#\n#The secret word was flaon.#\n#Congratulations to the computer for finding the secret word.#\n'
    finally:
        GameIO.output = old_output
    print(OK)
