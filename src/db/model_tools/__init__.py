class Model:
    class Meta:
        def __init__(self, cls):
            self.table_name = cls.__name__.lower()
            self.cols = []

            for k, v in cls.__dict__.items():
                if not callable(v) and not k.startswith('_'):
                    v.name = k.lower()
                    self.cols.append(v)

    def __init__(self):
        self.Meta = self.Meta(self.__class__)

    def get_sql4create(self):
        primary_keys = []
        checks = []
        lines = []
        for col in self.Meta.cols:
            if col.primary_key:
                primary_keys.append(col.name)
            checks.extend([col.checks[i].get_constraint_sql(f"{self.Meta.table_name}_{col.name}_{i}") for i in range(len(col.checks))])
            lines.append(col.get_sql())
        if primary_keys:
            lines.append(f"PRIMARY KEY ({", ".join(primary_keys)})")
        lines.extend(checks)
        return ", ".join(lines)
