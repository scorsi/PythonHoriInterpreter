from parsing.tokens import *


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.text_pos = 0  # The self.text position
        self.current_char = self.text[self.text_pos]

    def error(self):
        raise Exception("Unrecognized character")

    def advance(self):
        """
        Advance the `text_pos` pointer and set the `current_char` variable.
        """
        self.text_pos += 1
        if self.text_pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.text_pos]

    def peek(self):
        """
        Get the next char without advancing
        """
        peek_pos = self.text_pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace() and self.current_char != '\n':
            self.advance()

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()
        self.advance()  # pass the newline char

    def number(self):
        """
        Return a (multidigit) integer or float consumed from the input.
        """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            # Float number
            result += self.current_char
            self.advance()
            while self.current_char is not None and self.current_char.isdigit():
                result += self.current_char
                self.advance()

            return Token(FLOAT, float(result))
        else:
            return Token(INTEGER, int(result))

    def symbol(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def id(self):
        """
        Handle identifiers and reserved keywords
        """
        result = self.symbol()
        return RESERVED_KEYWORDS.get(result.lower(), Token(SYMBOL, result))

    def create_token(self, type, value):
        """
        Return a token with the given information and advance of the necessary char
        """
        for i in range(0, len(value)):
            self.advance()
        return Token(type, value)

    def get_next_token(self):
        """
        This method is responsible for breaking a sentence apart into tokens.
        One token at a time.
        """
        while self.current_char is not None:
            # EOL
            if self.current_char == '\n':
                return self.create_token(EOL, '\n')

            # Spaces
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            # Comments
            if self.current_char == '#':
                self.skip_comment()
                continue

            # ANNOTATION
            if self.current_char == "@":
                self.advance()
                return Token(ANNOTATION, self.text())

            # SYMBOL or Keywords
            if self.current_char.isalpha():
                return self.id()

            # INTEGER or FLOAT
            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '=':
                # DOUBLEEQUAL
                if self.peek() == '=':
                    return self.create_token(DOUBLEEQUAL, "==")
                # EQUAL
                return self.create_token(EQUAL, '=')

            # COLON
            if self.current_char == ':':
                return self.create_token(COLON, ':')

            # SEMICOLON
            if self.current_char == ';':
                return self.create_token(SEMICOLON, ';')

            if self.current_char == '-':
                # RARROW
                if self.peek() == '>':
                    return self.create_token(RARROW, "->")
                # MINUS
                return self.create_token(MINUS, '-')

            if self.current_char == '<':
                # LARROW
                if self.peek() == '-':
                    return self.create_token(LARROW, "<-")
                # LCHEV
                return self.create_token(LCHEV, '<')

            # RCHEV
            if self.current_char == '>':
                return self.create_token(RCHEV, '>')

            # PLUS
            if self.current_char == '+':
                return self.create_token(PLUS, '+')

            # STAR
            if self.current_char == '*':
                return self.create_token(STAR, '*')

            # SLASH
            if self.current_char == '/':
                return self.create_token(SLASH, '/')

            # ANTISLASH
            if self.current_char == '\\':
                return self.create_token(ANTISLASH, '\\')

            # PERCENTAGE
            if self.current_char == '%':
                return self.create_token(PERCENTAGE, '%')

            # LPAREN
            if self.current_char == '(':
                return self.create_token(LPAREN, '(')

            # RPAREN
            if self.current_char == ')':
                return self.create_token(RPAREN, ')')

            # LBRACE
            if self.current_char == '{':
                return self.create_token(LBRACE, '{')

            # RBRACE
            if self.current_char == '}':
                return self.create_token(RBRACE, '}')

            # COMMA
            if self.current_char == ',':
                return self.create_token(COMMA, ',')

            self.error()

        return Token(EOF, None)
