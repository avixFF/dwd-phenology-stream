# import argparse
from database import connection as db, migrator

# Define migration classes here

from database.migrations.dwd import CreateTables as DWD_CreateTables  # noqa

migrations = [
    DWD_CreateTables,
]

# parser = argparse.ArgumentParser()
# parser.add_argument(
#     '-r', '--reverse',
#     const=True,
#     action='store_const',
#     default=False
# )
# parser.add_argument(
#     '--fresh',
#     const=True,
#     action='store_const',
#     default=False
# )

# args = parser.parse_args()


def run(fresh=False):
    for migration in migrations:
        if fresh:
            migration(db, migrator).down()
            migration(db, migrator).up()
        else:
            migration(db, migrator).up()
            # if args.reverse:
            #     migration(db, migrator).down()
            # else:
