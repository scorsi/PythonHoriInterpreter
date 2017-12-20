from symbol.symbol import SymbolTable, GlobalSymbolTable


class StackElement(object):
    def __init__(self, scope):
        self.scope = scope
        self.return_value = None


class Stack(object):
    def __init__(self, global_symtab=GlobalSymbolTable()):
        self.global_symtab = global_symtab
        self.elements = [StackElement(self.global_symtab)]

    def add(self, name):
        # print("Create new stack: %s" % name)
        self.elements.append(StackElement(SymbolTable(name, self.elements[-1].scope.level + 1, self.elements[-1].scope)))

    def pop(self):
        # print("Pop stack: %s" % self.elements[-1].scope.name)
        self.elements.pop()

    def last(self):
        return self.elements[-1]

    def first(self):
        return self.elements[0]


class StackManager(object):
    def __init__(self, global_symtab=None):
        if global_symtab is None:
            self.stack = Stack()
        else:
            self.stack = Stack(global_symtab)
        self.global_symtab = self.stack.first()

