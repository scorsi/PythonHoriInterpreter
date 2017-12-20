from parsing.ast import NodeVisitor
from symbol.stack import add_var_to_stack, add_func_to_stack
from symbol.symbol import GlobalSymbolTable, ValSymbol, VarSymbol
from parsing.tokens import PLUS, STAR, SLASH, MINUS


class TreeOptimizer(NodeVisitor):
    """
    The TreeOptimizer will optimize some statements
    """

    pass


class GlobalSymbolTableCreator(NodeVisitor):
    """
    The GlobalSymbolTableCreator will create the useful GlobalSymbolTable
    It will also compute all global VariableDeclaration
    """

    def __init__(self):
        self.global_table = GlobalSymbolTable()
        self.errors = []

    def visit_list(self, node):
        for item in node:
            self.visit(item)

    def visit_Num(self, node):
        return ValSymbol('anonymous', node.type, node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left.type != right.type:
            self.errors.append("Types mismatch")
            return None
        if left.value is None or right.value is None:
            self.errors.append("Try to compute a not initialize variable")
            return None
        if node.op.type is PLUS:
            return ValSymbol('anonymous', left.type, left.value + right.value)
        elif node.op.type is STAR:
            return ValSymbol('anonymous', left.type, left.value * right.value)
        elif node.op.type is SLASH:
            return ValSymbol('anonymous', left.type, left.value / right.value)
        elif node.op.type is MINUS:
            return ValSymbol('anonymous', left.type, left.value - right.value)
        else:
            self.errors.append("Unknown error")
            return None

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        if expr.value is None:
            self.errors.append("Try to compute a not initialize variable")
            return None
        return ValSymbol('anonymous', expr.type, -expr.value)

    def visit_VariableAssignment(self, node):
        pass

    def visit_VariableDeclaration(self, node):
        value = None
        if node.expr is not None:
            value = self.visit(node.expr)
            if value is not None:
                value = value.value

        if node.const is True:
            self.global_table.insert(ValSymbol(node.symbol.name, node.type.name, value))
        else:
            self.global_table.insert(VarSymbol(node.symbol.name, node.type.name, value))

    def visit_FunctionDeclaration(self, node):
        add_func_to_stack(node, self.global_table)

    def visit_Symbol(self, node):
        symbol = self.global_table.lookup(node.name)
        if symbol is None:
            self.errors.append("Try to get value of an undeclared variable")
            return None
        return symbol

    def visit_Type(self, node):
        pass
