![](https://github.com/lexuzieel/dwd-phenology-stream/raw/master/data/demo.gif)

# Running in Docker

The application is ready to be run in containers by simply invoking `docker-compose up` command.
Of course, this assumes you have docker installed and ready on your machine.

The application is set up to automatically fetch data from DWD repository every 10 minutes:

```
app_1       | Updated: Stations
app_1       | Updated: Phases reference
app_1       | Updated: Phase names
app_1       | Updated: Plants reference
app_1       | Updated: Plants names
...
app_1       | Fetching: PH_Sofortmelder_Wildwachsende_Pflanze_Wiesen-Fuchsschwanz_akt.txt ... fetched 912 rows
app_1       | Updating plant kinds...
app_1       | Pushing to the database...
app_1       | Done
app_1       | Generating cache...
app_1       | Done
```

When the `docker-compose up` command is ran, the following steps are performed:
- Python application image is downloaded from [Docker Hub](https://hub.docker.com/repository/docker/lexuzieel/dwd-phenology-stream-app)
- MySQL 5.7 set up locally with `app` database storing application data
- Grafana 7.1.5 is installed with provisioned plugins, datasource (linked to installed MySQL) and dashboard for phenological data monitoring
- nginx reverse proxy for both Grafana & application web assets (in /data directory)

> **IMPORTANT:** To launch application in background mode, run `docker-compose up -d`

After the application has been spun up, it will be available at http://localhost

First step that you must take for the dashboard setup is to login with an adminsitrator account (login: admin, password: admin - password change is requested upon first login).

![](https://i.imgur.com/XeywxhK.png)

After that, the dashboard should be accessible through the side menu.

![](https://i.imgur.com/2zZCIEO.png)

After you open the dashboard, you can **star** (mark as favourite) it - this will allow you to set this dashboard as the default one which everybody sees upon accessing the site.

![](https://i.imgur.com/eXAv5lk.png)

> **NOTICE:** On the first run of the application the view cache is generated soon after the data is processed. During this time an error in Grafana dashboard can occur, showing error on data load.

# Manual installation

- Clone the repository
- Initialize pipenv repository by running `pipenv install` and then get into virtual environment by running `pipenv shell`
- Setup MySQL database and user with permissions to insert data and edit schema (for migrations and cache regeneration)
- Copy `.env.example` to `.env` and update values relevant to your database configuration
- Migrate database schema by running `pipenv run python . --migrate database.migrations.dwd.CreateTables`
- Optionally setup a cron job to run `run.sh` and `backup.sh` periodically
  - Old backups are removed automatically, only five most recent are left

## Migration

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
