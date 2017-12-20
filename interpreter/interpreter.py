from parsing.ast import NodeVisitor
from symbol.stack import StackManager
from symbol.symbol import ValSymbol, VarSymbol, FunctionSymbol
from parsing.tokens import PLUS, STAR, SLASH, MINUS


class Interpreter(NodeVisitor):
    """
    The Interpreter have to interpret the whole tree
    """

    def __init__(self, global_table):
        self._sm = StackManager(global_table)

    def error(self, msg):
        raise RuntimeError("Error: " + msg)

    def interpret(self):
        main = self._sm.stack.last().scope.lookup("main")
        if main is None:
            self.error("Undefined main reference")
        if isinstance(main, FunctionSymbol):
            return_value = self.visit(main)
            print("\n\nMain returned: %s" % return_value)
        else:
            self.error("\"main\" must refer to function")

    def visit_Num(self, node):
        self._sm.stack.last().return_value = node.value

        return VarSymbol('anonymous', node.type, node.value)

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)

        if left.type != right.type:
            print(left)
            print(right)
            self.error("Types mismatch")
        if left.value is None or right.value is None:
            self.error("Try to compute a not initialized variable")

        if node.op.type is PLUS:
            left.value += right.value
        elif node.op.type is STAR:
            left.value *= right.value
        elif node.op.type is SLASH:
            left.value /= right.value
        elif node.op.type is MINUS:
            left.value -= right.value
        else:
            self.error("Unknown Error")

        self._sm.stack.last().return_value = left.value
        return left

    def visit_UnaryOp(self, node):
        expr = self.visit(node.expr)
        if expr.value is None:
            self.error("Try to compute a not initialized variable")

        self._sm.stack.last().return_value = expr.value
        return VarSymbol('anonymous', expr.type, -expr.value)

    def visit_VariableAssignment(self, node):
        expr = self.visit(node.right)
        if expr is None or expr.value is None:
            self.error("Try to assign a variable to a not initialized variable")

        symbol = self.visit(node.left)

        if symbol.type is not expr.type:
            self.error("Types mismatch")
        symbol.value = expr.value

        self._sm.stack.last().return_value = symbol.value
        return True

    def visit_VariableDeclaration(self, node):
        value = None
        if node.expr is not None:
            value = self.visit(node.expr)
            if value is not None:
                value = value.value

        if node.const is True:
            self._sm.stack.last().scope.insert(ValSymbol(node.symbol.name, node.type.name, value))
        else:
            self._sm.stack.last().scope.insert(VarSymbol(node.symbol.name, node.type.name, value))

        self._sm.stack.last().return_value = value
        return True

    def visit_FunctionSymbol(self, node):
        # Create a new scope
        self._sm.stack.add(node.name)
        for statement in node.body:
            ret = self.visit(statement)
            if ret is None:
                break

        print(self._sm.stack.last().scope)

        return_value = self._sm.stack.last().return_value
        # Pop the current scope
        self._sm.stack.pop()
        return return_value

    def visit_FunctionDeclaration(self, node):
        pass

    def visit_Symbol(self, node):
        symbol = self._sm.stack.last().scope.lookup(node.name)
        if symbol is None:
            self.error("Try to get value of an undeclared variable")

        self._sm.stack.last().return_value = symbol.value
        return symbol

    def visit_Type(self, node):
        pass
