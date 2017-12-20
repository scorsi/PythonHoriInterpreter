class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """
        String representation of the class instance.
        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
            Token(MUL, '*')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    __repr__ = __str__


# Keywords
VAR = "Variable"
VAL = "Const Variable"
FUNC = "Function"
LATEINIT = "Late init"

# Symbols
SYMBOL = "Symbol"
ANNOTATION = "Annotation"

# Numbers
INTEGER = "Integer"
FLOAT = "Float"

# Recognized Characters
LPAREN = "Left Parenthesis '('"
RPAREN = "Right Parenthesis ')'"
LBRACE = "Left Curly Bracket '{'"
RBRACE = "Right Curly Bracket '}'"
LCHEV = "Left Chevron '<'"
RCHEV = "Right Chevron '>'"
LARROW = "Left Arrow '<-'"
RARROW = "Right Arrow '->'"
EQUAL = "Equal '='"
DOUBLEEQUAL = "Double Equal '=='"
COLON = "Colon ':'"
COMMA = "Comma ','"
SEMICOLON = "Semicolon ';'"
STAR = "Star '*'"
SLASH = "Slash '/'"
ANTISLASH = "AntiSlash '\\'"
PLUS = "Plus '+'"
MINUS = "Minus '-'"
PERCENTAGE = "Percentage '%'"
DOT = "Dot '.'"

EOL = "End of line"
EOF = "End of file"

RESERVED_KEYWORDS = {
    "var": Token(VAR, "var"),
    "val": Token(VAL, "val"),
    "func": Token(FUNC, "func"),
    "lateinit": Token(LATEINIT, "lateinit")
}
