import importlib.util
import inspect
import psycopg
from pathlib import Path
from .model_tools import Model


class ModuleWithModelsBasic:
    def __init__(self, module_name=None, models_path=None):
        self.module_name = module_name
        self.models_path = models_path

    def check__(self, others):
        assert self.module_name is not None
        assert self.module_name != ""
        assert self.module_name not in others
        p = Path(self.models_path)
        assert p.exists()
        assert p.is_file()
        assert p.suffix == ".py"


class ModelsManager:
    def __init__(self, modules):
        self.models = []
        self.model_names = []
        self.module_names = []

        for module in modules:
            module.check__(self.module_names)

            spec = importlib.util.spec_from_file_location(module.module_name, module.models_path)
            models_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(models_module)

            self.models.extend([
                cls()
                for _, cls in inspect.getmembers(models_module, inspect.isclass)
                if (
                        issubclass(cls, Model)
                        and cls is not Model
                        and cls.__module__ == models_module.__name__
                )
            ])
            self.module_names.append(module.module_name)

    def create_table_sql(self, model_name):
        for model in self.models:
            if model.Meta.table_name == model_name:
                return f"CREATE TABLE {model.Meta.table_name} ({model.get_sql4create()});"

        raise Exception(f"Model {model_name} not found.")


class CustomFunctionsBase:
    def __init__(self, conn):
        self.conn = conn


class Core:
    def __init__(self, user, password, hostname, port, db_name, modules, custom_functions_cls=None):
        self.mm = ModelsManager(modules)
        self.conn = psycopg.connect(f"postgres://{user}:{password}@{hostname}:{port}/{db_name}")
        if custom_functions_cls is not None:
            self.custom_functions = custom_functions_cls(self.conn)
        else:
            self.custom_functions = None
        self.is_changeable = True
        self.need_migrate = None

    def __del__(self):
        if self.conn is not None:
            self.conn.close()

    def change_protected(self, func):
        def wrapper(*args, **kwargs):
            if self.is_changeable:
                func(*args, **kwargs)
            else:
                raise Exception("You try change structure in runtime.")
        return wrapper

    def only_if_NOT_needed_to_migrate(self, func):
        def wrapper(*args, **kwargs):
            if self.need_migrate is None:
                raise Exception("You need execute check before that")
            if not self.need_migrate:
                func(*args, **kwargs)
            else:
                raise Exception("Needed migrations")
        return wrapper

    def check(self):
        pass

    def freeze(self):
        pass

    @only_if_NOT_needed_to_migrate
    def create_table(self, model_name):
        sql = self.mm.create_table_sql(model_name)
        with self.conn.cursor() as cur:
            cur.execute(sql)

    def select(self):
