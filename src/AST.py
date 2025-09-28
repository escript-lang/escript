class Base:
    def __init__(self, _eval: callable):
        self._eval = _eval

class Information(Base):
    def __init__(self):
        super().__init__(
            _eval=lambda x, node: print("Escript v0.0.1\nAuthor: filcher (https://github.com/filcherock)\n", end="")
        )


class Number(Base):
    __match_args__ = ("value",)

    def __init__(self, value):
        super().__init__(
            _eval=lambda x, node: node.value
        )
        self.value = value

class Var(Base):
    __match_args__ = ("name",)

    def __init__(self, name):
        def _eval(x, node):
            if node.name in x.env:
                return x.env[node.name]
            raise NameError(f"Variable '{node.name}' is not defined")

        super().__init__(
            _eval=_eval
        )
        self.name = name

class BinAction(Base):
    __match_args__ = ("left", "op", "right")

    def __init__(self, left, op, right):
        def _eval(x, node):
            _left = x.eval(node.left)
            _right = x.eval(node.right)

            operators = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b,
                '**': lambda a, b: a ** b,

                # Logics
                '>': lambda a, b: a > b,
                '<': lambda a, b: a < b,
                '==': lambda a, b: a == b,
                '>=': lambda a, b: a >= b,
                '<=': lambda a, b: a <= b
            }

            if node.op in operators:
                return operators[node.op](_left, _right)
            else:
                raise ValueError(f"Unknown operator: {node.op}")

        super().__init__(_eval)
        self.left = left
        self.op = op
        self.right = right

class String(Base):
    __match__args__ = ("value",)

    def __init__(self, value):
        super().__init__(
            _eval=lambda x, node: node.value
        )
        self.value = value

class Boolean(Base):
    __match__args__ = ("value",)

    def __init__(self, value):
        super().__init__(
            _eval=lambda x, node: node.value
        )
        self.value = value

class Assign(Base):
    __match_args__ = ("name", "expr")

    def __init__(self, name, expr):
        super().__init__(
            _eval=lambda x, node: x.env.update({node.name: x.eval(node.expr)}) or None
        )
        self.name = name
        self.expr = expr


class Print(Base):
    __match_args__ = ("expr",)

    def __init__(self, expr):
        super().__init__(
            _eval=lambda x, node: print(x.eval(node.expr), end="")
        )
        self.expr = expr

class Println(Base):
    __match_args__ = ("expr",)

    def __init__(self, expr):
        super().__init__(
            _eval=lambda x, node: print(x.eval(node.expr))
        )
        self.expr = expr

class getString(Base):
    __match_args__ = ("type",)

    def __init__(self, var):
        super().__init__(
            _eval=lambda x, node: str(input())
        )
        self.var = var

class getInt(Base):
    __match_args__ = ("type",)

    def __init__(self, var):
        super().__init__(
            _eval=lambda x, node: int(input())
        )
        self.var = var

class getFloat(Base):
    __match_args__ = ("type",)

    def __init__(self, var):
        super().__init__(
            _eval=lambda x, node: float(input())
        )
        self.var = var

class Program(Base):
    __match_args__ = ("statements",)

    def __init__(self, statements):
        super().__init__(
            _eval=lambda x, node: [x.eval(stmt) for stmt in node.statements]
        )
        self.statements = statements