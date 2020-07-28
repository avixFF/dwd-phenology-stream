# Installation

- Clone the repository
- Initialize pipenv repository by running `pipenv install` and then get into virtual environment by running `pipenv shell`
- Setup MySQL database and user with permissions to insert data and edit schema (for migrations and cache regeneration)
- Copy `.env.example` to `.env` and update values relevant to your database configuration
- Migrate database schema by running `pipenv run python . --migrate database.migrations.dwd.CreateTables`
- Optionally setup a cron job to run `run.sh` and `backup.sh` periodically
  - Old backups are removed automatically, only five most recent are left

# Migration

Migrations are located in `database/migrations` directory. In order to launch a migration, pass at least one fully-qualified migration class name using `migrate` argument.

```
python . --migrate path/to/module.Class [... path/to/another/module.Class] [--fresh] [--reverse]
```

Parameters:

- *migrate* - a list of fully-qualified migration class names
- *fresh* - run `down()` method first, then `up()`
- *reverse* - run `down()` on listed migrations in reverse order

# References

- [Germany GeoJSON](https://github.com/isellsoap/deutschlandGeoJSON/blob/master/2_bundeslaender/4_niedrig.geo.json)
- [Grafana Worldmap Panel](https://github.com/grafana/worldmap-panel)
- [Grafanimate](https://github.com/panodata/grafanimate)
- [Hiveeyes](https://community.hiveeyes.org/t/developing-grafana-worldmap-ng/1824)
- [Peewee ORM](http://docs.peewee-orm.com/en/latest/peewee/quickstart.html)
- [MySQL views](https://dev.mysql.com/doc/refman/8.0/en/create-view.html)
- [Mapbox](https://www.mapbox.com/)
- [DataGrip](https://www.jetbrains.com/datagrip/)

- [Wheat phenology (picture example)](https://www.nature.com/articles/s41437-020-0320-1)
