from ..db import Model


class Product(Model):
    def __init__(self, id, name, short_name, description, short_description, amount, file_id, photo_id):
        super().__init__()
        self.id = id
        self.name = name
        self.short_name = short_name
        self.description = description
        self.short_description = short_description
        self.amount = amount
        self.file_id = file_id
        self.photo_id = photo_id

    def get_short_name(self):
        if self.short_name is not None:
            return self.short_name
        else:
            return self.name
