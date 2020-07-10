from playhouse.migrate import *
from database.migrations import Migration as BaseMigration
from database.models.dwd import Station, Phase, PhaseName, Plant, PlantName, Record


class CreateTables(BaseMigration):

    def up(self):
        self.db.create_tables([
            Station, Phase, PhaseName, Plant, PlantName, Record
        ])

    def down(self):
        self.db.drop_tables([
            Station, Phase, PhaseName, Plant, PlantName, Record
        ])
