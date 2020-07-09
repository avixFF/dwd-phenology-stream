from peewee import *
from .. import BaseModel


class Station(BaseModel):
    '''
    Schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt
    '''
    class Meta:
        table_name = 'dwd_stations'

    id = IntegerField(primary_key=True)  # Stations_id
    name = CharField(null=True, index=True)  # Stationsname
    latitude = FloatField(index=True)  # geograph.Breite
    longitude = FloatField(index=True)  # geograph.Laenge
    height = FloatField(index=True)  # Stationshoehe
    natural_region_group_code = \
        IntegerField(index=True)  # Naturraumgruppe_Code
    natural_region_group = CharField(index=True)  # Naturraumgruppe
    natural_region_code = IntegerField(index=True)  # Naturraum_Code
    natural_region = CharField(index=True)  # Naturraum
    date = \
        DateField(null=True, index=True,
                  formats=['%d.%m.%Y'])  # Datum Stationsaufloesung
    state = CharField(index=True)  # Bundesland


class Phase(BaseModel):
    class Meta:
        table_name = 'dwd_phases'

    id = IntegerField(primary_key=True)
    # name = TextField(null=True, index=True)
    # latitude = FloatField(index=True)
    # longitude = FloatField(index=True)
    # naturraum = TextField(null=True, index=True)
    # state = TextField(null=True, index=True)


class PhaseName(BaseModel):
    class Meta:
        # primary_key = False
        table_name = 'dwd_phase_names'

    phase_id = ForeignKeyField(Phase, primary_key=True)
    name_german = CharField(null=True, index=True)
    name_english = CharField(null=True, index=True)


class Plant(BaseModel):
    class Meta:
        table_name = 'dwd_plants'

    id = IntegerField(primary_key=True)


class PlantName(BaseModel):
    class Meta:
        # primary_key = False
        table_name = 'dwd_plant_names'

    plant_id = ForeignKeyField(Plant, primary_key=True)
    name_german = CharField(null=True, index=True)
    name_english = CharField(null=True, index=True)
    name_latin = CharField(null=True, index=True)


class Record(BaseModel):
    class Meta:
        primary_key = CompositeKey(
            'station_id',
            'object_id',
            'phase_id',
            'date',
        )
        table_name = 'dwd_records'

    station_id = IntegerField()
    year = IntegerField()
    data_quality_bit = IntegerField()
    object_id = IntegerField()
    phase_id = IntegerField()
    date = DateField()
    date_quality_bit = IntegerField()
    day_of_year = IntegerField()
