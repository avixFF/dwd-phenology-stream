from database import connection as db, migrator

# Define migration classes here

from database.migrations.dwd import CreateTables as DWD_CreateTables  # noqa

migrations = [
    DWD_CreateTables,
]

def run(fresh=False):
    for migration in migrations:
        if fresh:
            migration(db, migrator).down()
            migration(db, migrator).up()
        else:
            migration(db, migrator).up()
