import Extract_main as ex

import enum

class LexTokens(enum.Enum):
    var_type = 1
    int_literal = 2
    decimal_literal = 3
    character = 4
    if_key = 5
    right_brace = 6
    left_brace = 7
    right_paren = 8
    left_paren = 9
    var_name = 10
    assignment = 11
    Equality = 12
    Increment = 13
    Arithmetic = 14

class Lexer :
    def __init__(self, string_stream):
        self.text = string_stream
        self.ind = 0
        self.cur_char = string_stream[0]
        self.tokens = []
        while self.ind < len(string_stream):
            self.tokens.append(self.next_token()) 
        

    def is_letter(self):
        return self.cur_char.isalpha()
        #return self.cur_char >= int('a') and self.cur_char <= int('z') or self.cur_char >= int('A') and self.cur_char <= int('Z')
    
    def consume(self):
        self.ind += 1
        if self.ind >= len(self.text):
            
            return
        self.cur_char = self.text[self.ind]

    def match(self, x):
        if (self.cur_char == x):
            self.consume()

    def whitespace(self):
        
        while self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\n':
            
            self.consume()


    def word(self):
        #########
        #KeyWords
        #########
        buff = ''
        if self.cur_char == 'i':
            buff += self.cur_char
            self.consume()
            if self.cur_char == 'f':
                buff += self.cur_char
                self.consume()
                return (LexTokens.if_key, 'if')
            elif self.cur_char =='n':
                buff += self.cur_char
                self.consume()
                if self.cur_char == 't':
                    buff += self.cur_char
                    self.consume()
                    return (LexTokens.var_type, 'int')
        
        if self.cur_char == 'b':
            buff += self.cur_char
            self.consume()
            if self.cur_char == 'o':
                buff += self.cur_char
                self.consume()
                if self.cur_char == 'o':
                    buff += self.cur_char
                    self.consume()
                    if self.cur_char == 'l':
                        buff += self.cur_char
                        self.consume()
                        return (LexTokens.var_type, 'bool')
        
        if self.cur_char == 'f':
            buff += self.cur_char
            self.consume()
            if self.cur_char == 'l':
                buff += self.cur_char
                self.consume()
                if self.cur_char == 'o':
                    buff += self.cur_char
                    self.consume()
                    if self.cur_char == 'a':
                        buff += self.cur_char
                        self.consume()
                        if self.cur_char == 't':
                            buff += self.cur_char
                            self.consume()
                            return (LexTokens.var_type, "float")
        
            

        
        while self.is_letter():
            buff += self.cur_char
            self.consume()

        return (LexTokens.var_name, buff)

    def is_number(self):
        return self.cur_char.isnumeric()
    
    def number(self):
        buff = ""
        while self.is_number():
            buff += self.cur_char
            self.consume()
        if self.cur_char == '.':
            buff += self.cur_char
            self.consume()
            while self.is_number():
                buff += self.cur_char
                self.consume()
            return (LexTokens.decimal_literal, buff)
        return (LexTokens.int_literal, buff)

    def equ(self):
        if self.cur_char == '=':
            self.consume()
            return (LexTokens.Equality, '==')
        return (LexTokens.assignment, '=')

    def arithmetic(self):
        buff = self.cur_char
        self.consume()
        if self.cur_char == buff:
            self.consume()
            return (LexTokens.Increment, '{0}{1}'.format(buff, buff))
        return (LexTokens.Arithmetic, buff)

    def next_token(self):
        while self.cur_char:
            
            if self.cur_char == ' ' or self.cur_char == '\t' or self.cur_char == '\n':
                
                self.whitespace()
                continue
            if self.cur_char == '{':
                self.consume()
                return (LexTokens.left_brace, '{')
            if self.cur_char == '}':
                self.consume()
                return (LexTokens.right_brace, '}')
            if self.cur_char == '{':
                self.consume()
                return (LexTokens.left_paren, '(')
            if self.cur_char == '}':
                self.consume()
                return (LexTokens.right_paren, ')')
            if self.cur_char == '=':
                self.consume()
                return self.equ()
            if self.is_letter():
                return self.word()
            if self.cur_char in ['+', '-', '/', '*']:
                return self.arithmetic()
            if self.is_number():
                return self.number()
            self.consume()
            #return (LexTokens.Prob_val, self.cur_char)


if __name__ == "__main__":
    l = Lexer(ex.extract_main("test_program.c"))
    for lexems in l.tokens:
        print(lexems)