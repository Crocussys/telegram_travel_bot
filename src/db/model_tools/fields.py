from .expressions import *


class Check:
    def __init__(self, expression, valid=False):
        self.expression = expression
        self.valid = valid

    def get_constraint_sql(self, name):
        return f"CONSTRAINT {name} CHECK ({self.expression.get_sql_expr()}){'' if self.valid else ' NOT VALID'}"


class Field(ExpressionBasic):
    def __init__(
            self,
            postgres_type,
            null=True,
            blank=False,
            default=None,
            primary_key=False,
            unique=False,
            checks=None,
            value=None
    ):
        super().__init__()
        if checks is None:
            checks = []
        self.name = None
        self.postgres_type = postgres_type
        self.null = null
        self.blank = blank
        self.default = default
        self.primary_key = primary_key
        self.unique = unique
        self.checks = checks
        self.value = value

        if self.blank:
            self.checks.append(Check(NotEqual(self, S("''"))))

    def get_sql(self):
        sql = [self.name, self.postgres_type]
        if not self.null:
            sql.append("NOT NULL")
        if self.default is not None:
            sql.append(f"DEFAULT {self.default}")
        return " ".join(sql)

    def get_sql_expr(self):
        return self.name

    def equal(self, other, valid=False):
        self.checks.append(Check(Equal(self, S(other)), valid))
        return self

    def not_equal(self, other, valid=False):
        self.checks.append(Check(NotEqual(self, S(other)), valid))
        return self

    def less_than(self, other, valid=False):
        self.checks.append(Check(LessThan(self, S(other)), valid))
        return self

    def greater_than(self, other, valid=False):
        self.checks.append(Check(GreaterThan(self, S(other)), valid))
        return self

    def less_than_or_equal(self, other, valid=False):
        self.checks.append(Check(LessThanOrEqual(self, S(other)), valid))
        return self

    def greater_than_or_equal(self, other, valid=False):
        self.checks.append(Check(GreaterThanOrEqual(self, S(other)), valid))
        return self

    def between(self, value1, value2, valid=False):
        self.checks.append(Check(Between(self.name, S(value1), S(value2)), valid))
        return self

    def not_between(self, value1, value2, valid=False):
        self.checks.append(Check(NotBetween(self.name, S(value1), S(value2)), valid))
        return self

    def like(self, pattern, valid=False):
        self.checks.append(Check(Like(self.name, S(pattern)), valid))
        return self

    def not_like(self, pattern, valid=False):
        self.checks.append(Check(NotLike(self.name, S(pattern)), valid))
        return self

    def in_(self, values, valid=False):
        self.checks.append(Check(In(self.name, [S(val) for val in values]), valid))
        return self

    def not_in_(self, values, valid=False):
        self.checks.append(Check(NotIn(self.name, [S(val) for val in values]), valid))
        return self

class BigSerialField(Field):
    def __init__(self, *args, **kwargs):
        super().__init__("bigserial", *args, **kwargs)


class NumericField(Field):
    def __init__(self, precision=None, scale=0, *args, **kwargs):
        assert precision is None or precision > 0
        self.precision = precision
        self.scale = scale
        if self.precision is None:
            super().__init__(f"numeric", *args, **kwargs)
        elif self.scale == 0:
            super().__init__(f"numeric({self.precision})", *args, **kwargs)
        else:
            super().__init__(f"numeric({self.precision}, {self.scale})", *args, **kwargs)


class CharField(Field):
    def __init__(self, length, *args, **kwargs):
        self.length = length
        super().__init__(f"character({self.length})", *args, **kwargs)


class VarCharField(Field):
    def __init__(self, max_length, *args, **kwargs):
        self.max_length = max_length
        super().__init__(f"character varying({self.max_length})", *args, **kwargs)
