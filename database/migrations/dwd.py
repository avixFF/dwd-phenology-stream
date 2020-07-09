from playhouse.migrate import *
from database.migrations import Migration as BaseMigration
from database.models.dwd import Station, Phase, PhaseName, Plant, PlantName, Record


class CreateTables(BaseMigration):

    def up(self):
        # print('dwd migration up')
        # print(Station)
        self.db.create_tables([
            Station, Phase, PhaseName, Plant, PlantName, Record
        ])
        # migrate(
        #     self.migrator.create_table()
        #     self.migrator.add_column(
        #         'dwd_plants', 'id', IntegerField(primary_key=True, default=0)
        #     ),
        # )

    def down(self):
        # print('dwd migration down')
        self.db.drop_tables([
            Station, Phase, PhaseName, Plant, PlantName, Record
        ])
