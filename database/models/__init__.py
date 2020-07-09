from peewee import Model
from .. import connection as db


class BaseModel(Model):
    class Meta:
        database = db
