from parsing.ast import NodeVisitor
from symbol.symbol import VarSymbol, ValSymbol, FunctionSymbol
from symbol.stack import Stack


class SemanticAnalyzer(NodeVisitor):
    """
    SyntaxAnalyzer analyze the whole tree to checks every symbol
    """

    def __init__(self, global_scope):
        self._stack = Stack(global_scope)
        self.errors = []
        self.warnings = []

    def get_stack(self):
        return self._stack

    def visit_Num(self, node):
        pass

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_VariableAssignment(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_VariableDeclaration(self, node):
        self.visit(node.type)
        # We should check the expr before the symbol in case of `var a : Int = a`
        if node.expr is not None:
            self.visit(node.expr)

        if self._stack.last().scope.lookup(node.symbol.name, True) is not None:
            self.errors.append(
                "A variable with the same name has already been declared in this scope: %s." % node.symbol.name)
        elif self._stack.last().scope.lookup(node.symbol.name, True) is not None:
            self.errors.append(
                "A variable is shadowing another variable in the global scope: %s." % node.symbol.name)
        else:
            if node.const is True:
                self._stack.last().scope.insert(VarSymbol(node.symbol.name, node.type))
            else:
                self._stack.last().scope.insert(ValSymbol(node.symbol.name, node.type))

    def visit_FunctionDeclaration(self, node):
        self.visit(node.type)

        if self._stack.last() is not self._stack.last():
            if self._stack.last().lookup(node.symbol.name, False) is not None:
                self.errors.append("A function with the same name has already been declared: %s." % node.symbol.name)
            else:
                self._stack.last().scope.insert(FunctionSymbol(node.symbol.name, node.type, node.arguments, node.body))

        # Create the new stack
        self._stack.add(node.symbol.name)
        if node.arguments is not None:
            for argument in node.arguments:
                self.visit(argument)
        if node.body is not None:
            for statement in node.body:
                self.visit(statement)

        # Pop the stack
        self._stack.pop()

    def visit_Symbol(self, node):
        if self._stack.last().scope.lookup(node.name, True) is None and \
                self._stack.first().scope.lookup(node.name, True) is None:
            self.errors.append(
                "Unknown symbol reference: %s\n       This symbol has not been declared in this scope." % node.name)

    def visit_Type(self, node):
        if self._stack.last().scope.lookup(node.name, False) is None:
            self.errors.append("Unknown type reference: %s\n       This type has not been declared." % node.name)
