from symbol.symbol import SymbolTable, GlobalSymbolTable, ValSymbol, VarSymbol, TypeSymbol, FunctionSymbol


class Stack(object):
    def __init__(self, global_symtab=GlobalSymbolTable()):
        self.global_symtab = global_symtab
        self.scopes = [self.global_symtab]

    def add_scope(self, name):
        print("Create new stack: %s" % name)
        self.scopes.append(SymbolTable(name, self.scopes[-1].level + 1, self.scopes[-1]))

    def pop_scope(self):
        print("Pop stack: %s" % self.scopes[-1].name)
        self.scopes.pop()

    def get_last_scope(self):
        return self.scopes[-1]

    def get_global_scope(self):
        return self.scopes[0]


class StackManager(object):
    def __init__(self, global_symtab=None):
        if global_symtab is None:
            self.scope_stack = Stack()
        else:
            self.scope_stack = Stack(global_symtab)
        self.global_symtab = self.scope_stack.get_global_scope()


def add_func_to_stack(node, stack):
    stack.insert(FunctionSymbol(node.symbol.name, node.type.name, node.arguments, node.body))


def add_full_func_to_stack(node, stack):
    add_func_to_stack(node, stack)
    stack.add_scope(node.symbol.name)
    last_scope = stack.get_last_scope()
    if node.arguments is not None:
        for argument in node.arguments:
            if argument.const is True:
                symbol = ValSymbol(argument.symbol.name, argument.type.name)
            else:
                symbol = VarSymbol(argument.symbol.name, argument.type.name)
            last_scope.insert(symbol)


def add_var_to_stack(node, stack):
    if node.const is True:
        stack.insert(ValSymbol(node.symbol.name, node.type.name))
    else:
        stack.insert(VarSymbol(node.symbol.name, node.type.name))


def add_type_to_stack(node, stack):
    stack.insert(TypeSymbol(node.name))
