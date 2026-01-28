class ExpressionBasic:
    def __init__(self):
        pass

    def get_sql_expr(self):
        pass


class S(ExpressionBasic):
    def __init__(self, value):
        super().__init__()
        self.value = value

    def get_sql_expr(self):
        return self.value


class Equal(ExpressionBasic):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.left.get_sql_expr()} = {self.right.get_sql_expr()}'


class NotEqual(ExpressionBasic):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.left.get_sql_expr()} != {self.right.get_sql_expr()}'


class LessThan(ExpressionBasic):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.left.get_sql_expr()} < {self.right.get_sql_expr()}'


class GreaterThan(ExpressionBasic):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.left.get_sql_expr()} > {self.right.get_sql_expr()}'


class LessThanOrEqual(ExpressionBasic):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.left.get_sql_expr()} <= {self.right.get_sql_expr()}'


class GreaterThanOrEqual(ExpressionBasic):
    def __init__(self, left, right):
        super().__init__()
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.left.get_sql_expr()} >= {self.right.get_sql_expr()}'


class Between(ExpressionBasic):
    def __init__(self, name, left, right):
        super().__init__()
        self.name = name
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.name} BETWEEN {self.left.get_sql_expr()} AND {self.right.get_sql_expr()}'


class NotBetween(ExpressionBasic):
    def __init__(self, name, left, right):
        super().__init__()
        self.name = name
        self.left = left
        self.right = right

    def get_sql_expr(self):
        return f'{self.name} NOT BETWEEN {self.left.get_sql_expr()} AND {self.right.get_sql_expr()}'


class Like(ExpressionBasic):
    def __init__(self, name, pattern):
        super().__init__()
        self.name = name
        self.pattern = pattern

    def get_sql_expr(self):
        return f'{self.name} LIKE {self.pattern.get_sql_expr()}'


class NotLike(ExpressionBasic):
    def __init__(self, name, pattern):
        super().__init__()
        self.name = name
        self.pattern = pattern

    def get_sql_expr(self):
        return f'{self.name} NOT LIKE {self.pattern.get_sql_expr()}'


class In(ExpressionBasic):
    def __init__(self, name, values):
        super().__init__()
        self.name = name
        self.values = values

    def get_sql_expr(self):
        return f'{self.name} IN ({", ".join([value.get_sql_expr() for value in self.values])})'


class NotIn(ExpressionBasic):
    def __init__(self, name, values):
        super().__init__()
        self.name = name
        self.values = values

    def get_sql_expr(self):
        return f'{self.name} NOT IN ({", ".join([value.get_sql_expr() for value in self.values])})'


class And(ExpressionBasic):
    def __init__(self, *args):
        super().__init__()
        self.conditions = args

    def get_sql_expr(self):
        return f'({" AND ".join([condition.get_sql_expr() for condition in self.conditions])})'


class Or(ExpressionBasic):
    def __init__(self, *args):
        super().__init__()
        self.conditions = args

    def get_sql_expr(self):
        return f'({" OR ".join([condition.get_sql_expr() for condition in self.conditions])})'


class Not(ExpressionBasic):
    def __init__(self, expression):
        super().__init__()
        self.expression = expression

    def get_sql_expr(self):
        return f'NOT {self.expression.get_sql_expr()}'
