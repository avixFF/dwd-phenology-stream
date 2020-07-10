from peewee import *
from database.models import BaseModel


class Station(BaseModel):
    '''
    Schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phaenologie_Stationen_Sofortmelder.txt
    '''
    class Meta:
        table_name = 'dwd_stations'

    id = IntegerField(primary_key=True)
    name = CharField(null=True, index=True)
    latitude = FloatField(index=True)
    longitude = FloatField(index=True)
    height = FloatField(index=True)
    natural_region_group_code = IntegerField(index=True)
    natural_region_group = CharField(index=True)
    natural_region_code = IntegerField(index=True)
    natural_region = CharField(index=True)
    date = DateField(null=True, index=True, formats=['%d.%m.%Y'])
    state = CharField(index=True)


class Phase(BaseModel):
    '''
    Part of schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phase.txt
    '''
    class Meta:
        table_name = 'dwd_phases'

    id = IntegerField(primary_key=True)
    weight = IntegerField(default=0)


class PhaseName(BaseModel):
    '''
    Part of schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Phase.txt
    '''
    class Meta:
        table_name = 'dwd_phase_names'

    phase_id = ForeignKeyField(Phase, primary_key=True)
    name_german = CharField(null=True, index=True)
    name_english = CharField(null=True, index=True)


class Plant(BaseModel):
    '''
    Part of schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Pflanze.txt
    '''
    class Meta:
        table_name = 'dwd_plants'

    id = IntegerField(primary_key=True)
    kind = CharField(null=True, index=True)


class PlantName(BaseModel):
    '''
    Part of schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Pflanze.txt
    '''
    class Meta:
        table_name = 'dwd_plant_names'

    plant_id = ForeignKeyField(Plant, primary_key=True)
    name_german = CharField(null=True, index=True)
    name_english = CharField(null=True, index=True)
    name_latin = CharField(null=True, index=True)


class Record(BaseModel):
    '''
    Schema for CSV file: https://opendata.dwd.de/climate_environment/CDC/help/PH_Beschreibung_Pflanze.txt
    '''
    class Meta:
        primary_key = CompositeKey(
            'station_id',
            'object_id',
            'phase_id',
            'date',
        )
        table_name = 'dwd_records'

    station_id = IntegerField(index=True)
    year = IntegerField(index=True)
    data_quality_bit = IntegerField(index=True)
    object_id = IntegerField(index=True)
    phase_id = IntegerField(index=True)
    date = DateField(index=True)
    date_quality_bit = IntegerField(index=True)
    day_of_year = IntegerField(index=True)
