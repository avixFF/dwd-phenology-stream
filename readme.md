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

# Methodology

## Phase mapping

Each relevant phase is assigned a weight, denoting "ripeness" of the phase.
This will make it possible to compare phases between each other, moving away from textual representation.

Example for common fruit phenological phases:

| Phase name                               | Weight |
|------------------------------------------|:------:|
| fruit ripe for picking                   | 3      |
| end of flowering in the observation area | 2      |
| beginning of flowering                   | 1      |
