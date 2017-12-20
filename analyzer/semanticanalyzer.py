from parsing.ast import NodeVisitor
from symbol.stack import Stack, add_var_to_stack, add_func_to_stack


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

        if self._stack.get_last_scope().lookup(node.symbol.name, True) is not None:
            self.errors.append(
                "A variable with the same name has already been declared in this scope: %s." % node.symbol.name)
        elif self._stack.get_global_scope().lookup(node.symbol.name, True) is not None:
            self.errors.append(
                "A variable is shadowing another variable in the global scope: %s." % node.symbol.name)
        else:
            add_var_to_stack(node, self._stack.get_last_scope())

    def visit_FunctionDeclaration(self, node):
        self.visit(node.type)

        if self._stack.get_last_scope() is not self._stack.get_global_scope():
            if self._stack.get_last_scope().lookup(node.symbol.name, False) is not None:
                self.errors.append("A function with the same name has already been declared: %s." % node.symbol.name)
            else:
                add_func_to_stack(node, self._stack.get_last_scope())

        # Create the new stack
        self._stack.add_scope(node.symbol.name)
        if node.arguments is not None:
            for argument in node.arguments:
                self.visit(argument)
        if node.body is not None:
            for statement in node.body:
                self.visit(statement)

        print(self._stack.get_last_scope())

        # Pop the stack
        self._stack.pop_scope()

    def visit_Symbol(self, node):
        if self._stack.get_last_scope().lookup(node.name, True) is None and \
                self._stack.get_global_scope().lookup(node.name, True) is None:
            self.errors.append(
                "Unknown symbol reference: %s\n       This symbol has not been declared in this scope." % node.name)

    def visit_Type(self, node):
        if self._stack.get_last_scope().lookup(node.name, False) is None:
            self.errors.append("Unknown type reference: %s\n       This type has not been declared." % node.name)
