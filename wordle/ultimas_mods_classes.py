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
        if word in self.storage.storageList:
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