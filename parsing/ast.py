class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class AST(object):
    """
    The AST class is the base class of all the AST Nodes
    It don't have to be instantiated
    """

    pass


class Num(AST):
    """
    The Num represents an integer or a float value
    Examples:
        42
        789.98
    """

    def __init__(self, token):
        self.token = token
        self.value = token.value
        self.type = token.type

    def __str__(self):
        return 'Num({value}, {type})'.format(
            value=self.value,
            type=self.type
        )

    __repr__ = __str__


class BinOp(AST):
    """
    The BinOp represents any numeric operation
    Examples:
        3 + 2
        42 * 2
        6 / 1
        2 - 8
        3 + (5 * 4)
    """

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __str__(self):
        return 'BinOp({left}, {op}, {right})'.format(
            left=self.left,
            op=self.op,
            right=self.right
        )

    __repr__ = __str__


class UnaryOp(AST):
    """
    The UnaryOp represents a unary operator followed by an expression
    Examples:
        - 3
        + 42
        - 4 * 12
        5 * - 67
    """

    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __str__(self):
        return 'UnaryOp({op}, {expr})'.format(
            op=self.op,
            expr=self.expr
        )

    __repr__ = __str__


class VariableAssignment(AST):
    """
    The VariableAssignment represents the assignment of a variable
    Examples:
         a = 3
         test = 4 + 2
    """

    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return 'VariableAssignment({left}, {right})'.format(
            left=self.left,
            right=self.right
        )

    __repr__ = __str__


class VariableDeclaration(AST):
    """
    The VariableDeclaration represents the variable declaration
    Examples:
        var a : Int = 3
        var b : Int = 4 * 2
        val c : Float = 42
        lateinit var d : Bool
    """

    def __init__(self, lateinit, const, symbol, type, expr=None):
        self.lateinit = lateinit
        self.const = const
        self.symbol = symbol
        self.type = type
        self.expr = expr

    def __str__(self):
        return 'VariableDeclaration({lateinit}, {const}, {symbol}, {type}, {expr})'.format(
            lateinit=self.lateinit,
            const=self.const,
            symbol=self.symbol,
            type=self.type,
            expr=self.expr
        )

    __repr__ = __str__


class FunctionDeclaration(AST):
    """
    The FunctionDeclaration represents the declaration of a function
    Examples:
        func test(val a : Int) : Int -> a
        func addTwo (val b : Int) : Int -> b * 2
    """

    def __init__(self, symbol, arguments, type, body):
        self.symbol = symbol
        self.arguments = arguments
        self.type = type
        self.body = body

    def __str__(self):
        return 'FunctionDeclaration({symbol}, {arguments}, {type}, {body})'.format(
            symbol=self.symbol,
            arguments=self.arguments,
            type=self.type,
            body=self.body
        )

    __repr__ = __str__


class Symbol(AST):
    """
    The Symbol represents an user-defined symbol
    Examples:
        a
        test
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Symbol({name})'.format(
            name=self.name
        )

    __repr__ = __str__


class Type(AST):
    """
    The Type represents an type symbol
    Examples:
        Int
        Float
    """

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Type({name})'.format(
            name=self.name
        )

    __repr__ = __str__
