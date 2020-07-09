from peewee import Database
from playhouse.migrate import *


class Migration():

    def __init__(self, db: Database, migrator: SchemaManager):
        self.db = db
        self.migrator = migrator

    def up(self):
        raise NotImplementedError

    def down(self):
        raise NotImplementedError
