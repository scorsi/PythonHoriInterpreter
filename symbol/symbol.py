from collections import OrderedDict


class Symbol(object):
    def __init__(self, name, type=None):
        self.name = name
        self.type = type


class VarSymbol(Symbol):
    def __init__(self, name, type, value=None):
        super().__init__(name, type)
        self.__set_value(value)

    def __str__(self):
        return "<Var(name='{name}', type='{type}', value='{value}'>".format(
            name=self.name,
            type=self.type,
            value=self.__get_value()
        )

    __repr__ = __str__

    def __get_value(self):
        return self.__value

    def __set_value(self, value):
        self.__value = value

    value = property(__get_value, __set_value)


class ValSymbol(Symbol):
    def __init__(self, name, type, value=None):
        super().__init__(name, type)
        self.__value = value

    def __str__(self):
        return "<Val(name='{name}', type='{type}', value='{value}'>".format(
            name=self.name,
            type=self.type,
            value=self.__get_value()
        )

    __repr__ = __str__

    def __get_value(self):
        return self.__value

    def __set_value(self, value):
        if self.__get_value() is None:
            self.__value = value
        else:
            raise Exception("A val cannot be reassigned")

    value = property(__get_value, __set_value)


class TypeSymbol(Symbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return "<Type(name='{name}'>".format(
            name=self.name
        )

    __repr__ = __str__


class BuiltinTypeSymbol(TypeSymbol):
    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        return "<BuiltinType(name='{name}'>".format(
            name=self.name
        )

    __repr__ = __str__


class FunctionSymbol(Symbol):
    def __init__(self, name, type, params, body):
        super().__init__(name, type)
        self.params = params if params is not None else []
        self.body = body

    def __str__(self):
        return "<Function(name='{name}', type='{type}', params={params}, body={body}>".format(
            name=self.name,
            type=self.type,
            params=self.params,
            body=self.body
        )

    __repr__ = __str__


class SymbolTable(object):
    def __init__(self, name, level, enclosing_scope=None):
        self._symbols = OrderedDict()
        self.name = name
        self.level = level
        self.enclosing_scope = enclosing_scope

    def __str__(self):
        h1 = 'SYMBOL TABLE'
        lines = ['\n', h1, '=' * len(h1)]
        for header_name, header_value in (
                ('Name', self.name),
                ('Level', self.level),
                ('Enclosing scope', self.enclosing_scope.name if self.enclosing_scope else None)
        ):
            lines.append('%-15s: %s' % (header_name, header_value))
        h2 = 'Scope (symbol table) contents'
        lines.extend([h2, '-' * len(h2)])
        lines.extend(
            ('%7s: %r' % (key, value))
            for key, value in self._symbols.items()
        )
        lines.append('\n')
        s = '\n'.join(lines)
        return s

    __repr__ = __str__

    def insert(self, symbol):
        print('Insert: %s' % symbol.name)
        self._symbols[symbol.name] = symbol

    def lookup(self, name, current_scope_only=False):
        print('Lookup: %s (Scope name: %s)' % (name, self.name))
        # 'symbol' is either an instance of the Symbol class or None
        symbol = self._symbols.get(name)

        if symbol is not None:
            return symbol

        if current_scope_only:
            return None

        # recursively go up the chain and lookup the name
        if self.enclosing_scope is not None:
            return self.enclosing_scope.lookup(name)
        return None


class GlobalSymbolTable(SymbolTable):
    def __init__(self):
        super().__init__("Global", 1)
        self._init_builtins()

    def _init_builtins(self):
        self.insert(BuiltinTypeSymbol('Int'))
        self.insert(BuiltinTypeSymbol('Float'))
