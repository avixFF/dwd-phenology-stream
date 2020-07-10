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


class AddPlantKind(BaseMigration):

    def up(self):
        migrate(
            self.migrator.add_column(
                Plant._meta.table_name, 'kind', CharField(null=True)
            ),
        )

    def down(self):
        migrate(
            self.migrator.drop_column(Plant._meta.table_name, 'kind'),
        )
