from db.model_tools import Model
from db.model_tools.fields import *


class Product(Model):
    id = BigSerialField(primary_key=True)
    name = VarCharField(128, null=False, blank=True)
    short_name = VarCharField(32, blank=True)
    description = VarCharField(1024, blank=True)
    short_description = VarCharField(255, blank=True)
    amount = NumericField(12, 2, null=False).greater_than_or_equal(0)
    file_id = CharField(71, null=False)
    photo_id = CharField(82)
