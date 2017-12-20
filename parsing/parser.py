from parsing.tokens import *
from parsing.ast import *


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        print(self.current_token)

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        """
        Compare the current token type with the passed token type and if they match
        then "eat" the current token and assign the next token to the self.current_token
        otherwise raise an exception.
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
            print(self.current_token)
        else:
            self.error()

    def eat_EOL(self):
        """
        Eat all the next EOL
        """
        print("Start eating EOL")
        self.eat(EOL)
        while self.current_token.type == EOL:
            self.eat(EOL)
        print("Stop eating EOL")

    def root_list(self):
        """
        root_list : root
                  | root EOL root_list
        """
        if self.current_token.type == EOL:
            self.eat_EOL()

        node = self.root()
        results = [node]

        while self.current_token.type == EOL:
            self.eat_EOL()
            if self.current_token is not None and self.current_token.type is not EOF:
                results.append(self.root())

        return results

    def root(self):
        """
        root : variable_declaration
             | function_declaration
        """
        statement = None
        if self.current_token.type in (LATEINIT, VAR, VAL):
            statement = self.variable_declaration()
        elif self.current_token.type == FUNC:
            statement = self.function_declaration()
        else:
            self.error()
        return statement

    def function_declaration(self):
        """
        function_declaration : FUNC symbol LPAREN function_arguments RPAREN type body
                             | FUNC symbol LPAREN RPAREN type body
                             | FUNC symbol type body
        """
        self.eat(FUNC)
        symbol = self.symbol()
        arguments = None
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            if self.current_token.type == RPAREN:
                self.eat(RPAREN)
            else:
                arguments = self.function_argument_list()
                self.eat(RPAREN)
        type = self.type()
        body = self.body()
        return FunctionDeclaration(symbol, arguments, type, body)

    def function_argument_list(self):
        """
        function_argument_list : function_argument
                               | function_argument COMMA function_argument_list
        """
        node = self.function_argument()
        results = [node]

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            results.append(self.function_argument())

        return results

    def function_argument(self):
        """
        function_argument : (VAR | VAL) symbol type
                          | (VAR | VAL) symbol type EQUAL expr
        """
        const = False
        if self.current_token.type == VAR:
            self.eat(VAR)
        else:
            self.eat(VAL)
            const = True
        symbol = self.symbol()
        type = self.type()
        expr = None
        if self.current_token.type == EQUAL:
            self.eat(EQUAL)
            expr = self.expr()
        return VariableDeclaration(False, const, symbol, type, expr)

    def body(self):
        """
        body : RARROW statement
             | LBRACE statement_list RBRACE
        """
        if self.current_token.type == RARROW:
            self.eat(RARROW)
            return [self.statement()]
        else:
            self.eat(LBRACE)
            node = self.statement_list()
            self.eat(RBRACE)
            return node

    def statement_list(self):
        """
        statement_list : annotation
                       | statement
                       | statement EOL statement_list
        """
        if self.current_token.type == EOL:
            self.eat_EOL()

        node = self.statement()
        results = [node]

        while self.current_token.type == EOL:
            self.eat_EOL()
            if self.current_token.type == RBRACE:
                break
            if self.current_token.type == ANNOTATION:
                results.append(self.annotation())
            else:
                results.append(self.statement())

        return results

    def statement(self):
        """
        statement : variable_declaration
                  | variable_assignment
                  | expr
        """
        if self.current_token.type in (LATEINIT, VAL, VAR):
            return self.variable_declaration()
        elif self.current_token.type == SYMBOL:
            #
            # A statement starting with a SYMBOL can either be a variable_assignment and a expr
            #
            symbol = self.symbol()
            if self.current_token.type == EQUAL:
                # VariableAssignment
                self.eat(EQUAL)
                return VariableAssignment(symbol, self.expr())
            elif self.current_token.type in (PLUS, MINUS):
                # Term
                op = self.current_token
                self.eat(self.current_token.type)
                return BinOp(symbol, op, self.term())
            elif self.current_token.type in (STAR, SLASH):
                # Factor
                op = self.current_token
                self.eat(self.current_token.type)
                return BinOp(symbol, op, self.factor())
            else:
                return symbol
        else:
            return self.expr()

    def variable_assignment(self):
        """
        variable_assignment : symbol EQUAL expr
        """
        symbol = self.symbol()
        self.eat(EQUAL)
        return VariableAssignment(symbol, self.expr())

    def variable_declaration(self):
        """
        function_argument : (VAR | VAL) symbol type
                          | (VAR | VAL) symbol type EQUAL expr
        """
        const = False
        if self.current_token.type == VAR:
            self.eat(VAR)
        else:
            self.eat(VAL)
            const = True
        symbol = self.symbol()
        type = self.type()
        expr = []
        if self.current_token.type == EQUAL:
            self.eat(EQUAL)
            expr = self.expr()
        return VariableDeclaration(False, const, symbol, type, expr)

    def symbol(self):
        """
        symbol : SYMBOL
        """
        token = self.current_token
        self.eat(SYMBOL)
        return Symbol(token.value)

    def type(self):
        """
        type : COLON SYMBOL
        """
        self.eat(COLON)
        token = self.current_token
        self.eat(SYMBOL)
        return Type(token.value)

    def expr(self):
        """
        expr : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(node, token, self.term())

        return node

    def term(self):
        """
        term : factor ((STAR | SLASH) factor)*
        """
        node = self.factor()

        while self.current_token.type in (STAR, SLASH):
            token = self.current_token
            if token.type == STAR:
                self.eat(STAR)
            elif token.type == SLASH:
                self.eat(SLASH)

            node = BinOp(node, token, self.factor())

        return node

    def factor(self):
        """
        factor : (PLUS | MINUS) factor
               | INTEGER
               | FLOAT
               | LPAREN expr RPAREN
               | symbol
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == FLOAT:
            self.eat(FLOAT)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        else:
            return self.symbol()

    def parse(self):
        """
        root_list : root
                  | root EOL root_list

        root : variable_declaration
             | function_declaration

        function_declaration : FUNC symbol LPAREN function_arguments RPAREN type body
                             | FUNC symbol LPAREN RPAREN type body
                             | FUNC symbol type body

        function_argument_list : function_argument
                               | function_argument COMMA function_argument_list

        function_argument : (VAR | VAL) symbol type
                          | (VAR | VAL) symbol type EQUAL expr

        body : RARROW statement
             | LBRACE statement_list RBRACE

        statement_list : (annotation)? statement
                       | (annotation)? statement EOL statement_list

        statement : variable_declaration
                  | variable_assignment
                  | expr

        variable_assignment : symbol EQUAL expr

        variable_declaration : (VAR | VAL) symbol type
                             | (VAR | VAL) symbol type EQUAL expr

        expr : term ((PLUS | MINUS) term)*

        term : factor ((STAR | SLASH) factor)*

        factor : (PLUS | MINUS) factor
               | INTEGER
               | FLOAT
               | LPAREN expr RPAREN
               | symbol

        symbol : SYMBOL

        type : COLON SYMBOL

        annotation : ANNOTATION
        """
        node = self.root_list()
        if self.current_token.type != EOF:
            self.error()

        return node
