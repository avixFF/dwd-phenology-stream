import importlib
from database import connection as db, migrator


def run(path: str = None, fresh: bool = False, reverse: bool = False):
    path = path.replace('/', '.')
    parts = path.rsplit('.', 1)
    module = importlib.import_module(parts[0])
    name = parts[1]

    migration = getattr(module, name)

    if reverse:
        print(f'Reverting migration {path}...')
    else:
        print(f'Running migration {path}...')

    if fresh:
        migration(db, migrator).down()
        migration(db, migrator).up()
    else:
        if reverse:
            migration(db, migrator).down()
        else:
            migration(db, migrator).up()
