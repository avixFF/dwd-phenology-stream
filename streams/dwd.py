import os
import requests
import datetime
import pydash as _
import pandas as pd
from bs4 import BeautifulSoup
import database.models.dwd as dwd
from loaders.CsvLoader import CsvLoader
from streams import Stream as BaseStream


class Stream(BaseStream):

    def fetch(self):
        self._loader = CsvLoader({
            'delimiter': ';',
            'eor_mode': True,
        })

        # Cache stations, phases and plants definitions for 1 day

        cache_duration = 3600 * 24

        self._stations = self._loader.load({
            'url': _.get(self._config, 'stations.url'),
            'cache': cache_duration
        }).rename(
            columns=_.get(self._config, 'stations.field_map', {})
        )
        self._stations.columns = map(str.lower, self._stations.columns)
        self._stations = \
            self._stations.where(pd.notnull(self._stations), None)

        self._phases = self._loader.load({
            'url': _.get(self._config, 'phases.url'),
            'cache': cache_duration
        }).rename(
            columns=_.get(self._config, 'phases.field_map', {})
        )
        self._phases.columns = map(str.lower, self._phases.columns)
        self._phases = \
            self._phases.where(pd.notnull(self._phases), None)

        self._plants = self._loader.load({
            'url': _.get(self._config, 'plants.url'),
            'cache': cache_duration
        }).rename(
            columns=_.get(self._config, 'plants.field_map', {})
        )
        self._plants.columns = map(str.lower, self._plants.columns)
        self._plants = \
            self._plants.where(pd.notnull(self._plants), None)

        # Stations

        dwd.Station.insert_many(
            self._stations.to_dict('records')
        ).on_conflict(
            preserve=[dwd.Station.id],
            update={
                dwd.Station.name: dwd.Station.name,
                dwd.Station.latitude: dwd.Station.latitude,
                dwd.Station.longitude: dwd.Station.longitude,
                dwd.Station.height: dwd.Station.height,
                dwd.Station.natural_region_group_code: dwd.Station.natural_region_group_code,
                dwd.Station.natural_region_group: dwd.Station.natural_region_group,
                dwd.Station.natural_region_code: dwd.Station.natural_region_code,
                dwd.Station.natural_region: dwd.Station.natural_region,
                dwd.Station.date: dwd.Station.date,
                dwd.Station.state: dwd.Station.state,
            }
        ).execute()

        print('Updated: Stations')

        # Phases

        dwd.Phase.insert_many(
            self._phases.loc[:, ['id']].to_dict('records')
        ).on_conflict(
            preserve=[dwd.Phase.id]
        ).execute()

        print('Updated: Phases reference')

        dwd.PhaseName.insert_many(
            self._phases.rename(columns={
                'id': 'phase_id',
            }).to_dict('records')
        ).on_conflict(
            preserve=[dwd.PhaseName.phase_id],
            update={
                dwd.PhaseName.name_german: dwd.PhaseName.name_german,
                dwd.PhaseName.name_english: dwd.PhaseName.name_english,
            }
        ).execute()

        print('Updated: Phase names')

        # Plants

        dwd.Plant.insert_many(
            self._plants.loc[:, ['id']].to_dict('records')
        ).on_conflict(
            preserve=[dwd.Plant.id]
        ).execute()

        print('Updated: Plants reference')

        dwd.PlantName.insert_many(
            self._plants.rename(columns={
                'id': 'plant_id',
            }).to_dict('records')
        ).on_conflict(
            preserve=[dwd.PlantName.plant_id],
            update={
                dwd.PlantName.name_german: dwd.PlantName.name_german,
                dwd.PlantName.name_english: dwd.PlantName.name_english,
                dwd.PlantName.name_latin: dwd.PlantName.name_latin,
            }
        ).execute()

        print('Updated: Plants names')

        sources = _.get(self._config, 'sources', [])

        aggregate = None

        for source in sources:

            source_type = source.get('type')

            if source_type == 'index':
                url = source.get('url')
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                files = []

                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.startswith(source.get('prefix')):
                        files.append(href)

                source['data_frames'] = []

                for file in files:
                    print(f'Fetching: {file} ... ', end='')

                    df = self._loader.load({
                        'url': f'{url}/{file}',
                        'cache': 3600
                    })

                    print(f'fetched {df.shape[0]} rows')

                    source['data_frames'].append(df)

                    df.columns = map(str.lower, df.columns)

                    if aggregate is None:
                        aggregate = df
                    else:
                        aggregate = pd.concat([aggregate, df])
            else:
                raise Exception(f'Unknown source type "{source_type}"')

        aggregate = aggregate.rename(
            columns=_.get(self._config, 'field_map', {})
        )

        aggregate.dropna(inplace=True, subset=['date'])

        aggregate['date'] = aggregate['date'].fillna(0).astype(int) \
            .astype(str).apply(
                lambda x: datetime.date(
                    year=int(x[0:4]),
                    month=int(x[4:6]),
                    day=int(x[6:8]),
                ).isoformat()
        )

        aggregate['day_of_year'] = aggregate['day_of_year'].fillna(0) \
            .astype(int)

        print('Pushing to the database... ')

        records = aggregate.to_dict('records')

        dwd.Record.insert_many(records).on_conflict(
            preserve=[
                dwd.Record.station_id,
                dwd.Record.object_id,
                dwd.Record.phase_id,
                dwd.Record.date,
            ],
        ).execute()

        print('Done')
