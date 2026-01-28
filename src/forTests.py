from db import ModelsManager, ModuleWithModelsBasic


class MyModule(ModuleWithModelsBasic):
    def __init__(self):
        super().__init__("test", r"D:\Code\Repositories\telegram_travel_bot\src\bot\models.py")


if __name__ == "__main__":
    m = MyModule()
    mm = ModelsManager([m])
    print(mm.create_table_sql("product"))
