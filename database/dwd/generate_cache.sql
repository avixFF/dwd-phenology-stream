drop table if exists dwd_records_cache_fruits;
create table dwd_records_cache_fruits
(
    key `weight` (`weight`),
    key `lat` (`lat`),
    key `lon` (`lon`),
    key `station` (`station`),
    key `state` (`state`),
    key `date` (`date`)
)
select avg(dwd_phases.weight)                                    as "weight",
       dwd_stations.longitude                                    as "lon",
       dwd_stations.latitude                                     as "lat",
       dwd_stations.name                                         as "station",
       substring_index(group_concat(dwd_stations.state), ',', 1) as "state",
       dwd_records.date                                          as "date"
from dwd_records
         join dwd_plants on dwd_plants.id = dwd_records.object_id
         join dwd_phases on dwd_phases.id = dwd_records.phase_id
         join dwd_stations on dwd_stations.id = dwd_records.station_id
where kind = 'fruit'
group by date, lon, lat, station;

drop table if exists dwd_records_cache_crops;
create table dwd_records_cache_crops
(
    key `weight` (`weight`),
    key `lat` (`lat`),
    key `lon` (`lon`),
    key `station` (`station`),
    key `state` (`state`),
    key `date` (`date`)
)
select avg(dwd_phases.weight)                                    as "weight",
       dwd_stations.longitude                                    as "lon",
       dwd_stations.latitude                                     as "lat",
       dwd_stations.name                                         as "station",
       substring_index(group_concat(dwd_stations.state), ',', 1) as "state",
       dwd_records.date                                          as "date"
from dwd_records
         join dwd_plants on dwd_plants.id = dwd_records.object_id
         join dwd_phases on dwd_phases.id = dwd_records.phase_id
         join dwd_stations on dwd_stations.id = dwd_records.station_id
where kind = 'crop'
group by date, lon, lat, station;

drop table if exists dwd_records_cache_wild;
create table dwd_records_cache_wild
(
    key `weight` (`weight`),
    key `lat` (`lat`),
    key `lon` (`lon`),
    key `station` (`station`),
    key `state` (`state`),
    key `date` (`date`)
)
select avg(dwd_phases.weight)                                    as "weight",
       dwd_stations.longitude                                    as "lon",
       dwd_stations.latitude                                     as "lat",
       dwd_stations.name                                         as "station",
       substring_index(group_concat(dwd_stations.state), ',', 1) as "state",
       dwd_records.date                                          as "date"
from dwd_records
         join dwd_plants on dwd_plants.id = dwd_records.object_id
         join dwd_phases on dwd_phases.id = dwd_records.phase_id
         join dwd_stations on dwd_stations.id = dwd_records.station_id
where kind = 'wild'
group by date, lon, lat, station;
