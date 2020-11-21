import os
import re
import time
import hashlib
import requests
import pandas as pd
from io import StringIO
from loaders import Loader
from dateutil.parser import parse as parsedate


class CsvLoader(Loader):

    delimiter = ','

    def __init__(self, config: dict = {}):
        """
        Config:
        - delimiter (default: ',')
        - cache_dir (default: 'cache')
        - eor_mode (default: False) - whether to use 'eor' string as row separator instead of newline
        """
        self._delimiter = config.get('delimiter', CsvLoader.delimiter)
        self._cache_dir = config.get('cache_dir', 'cache')
        self._eor_mode = config.get('eor_mode', False)

    def _writeCache(self, data: str, key: str) -> int:
        os.makedirs(self._cache_dir, exist_ok=True)

        with open(f'{self._cache_dir}/{key}', 'w') as f:
            return f.write(data)

    def _readCache(self, key: str):
        path = f'{self._cache_dir}/{key}'

        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()

    def _cache(self, url: str, duration: int = 60):
        """
        Arguments:
            - url (str): URL from which to download DataFrame
            - duration (int): duration of the cache in seconds
        """

        # First define cache variables and try to get cached timestamp
        hash = self._getHash(url)

        content_cache_key = f'{hash}.pkl'
        timestamp_cache_key = f'{hash}.timestamp'

        content_file_path = f'{self._cache_dir}/{content_cache_key}'

        cached_timestamp = self._readCache(timestamp_cache_key)

        # If current timestamp is less than cached timestamp it means
        # that cache hasn't expired yet and we can just read cached data
        if cached_timestamp is not None \
                and int(time.time()) < int(cached_timestamp):
            try:
                return pd.read_pickle(content_file_path)
            except:
                pass

        # If reading cache has failed or cached timestamp is less than
        # current time then we fetch the url and get last modified date
        response = requests.get(url)

        data_timestamp = int(time.time()) + duration

        # last_modified = response.headers.get('Last-Modified')

        # if last_modified is not None:
        #     data_timestamp = int(parsedate(last_modified).timestamp())

        def update():
            content = response.text
            stream = None

            if self._eor_mode:
                content = re.sub(rf'\s*{self._delimiter}\s*',
                                 self._delimiter, content)
                content = re.sub(rf'{self._delimiter}eor{self._delimiter}+',
                                 '\n', content)

                stream = StringIO(content)

                # Source: https://stackoverflow.com/a/10289740/2467106
                #
                # Move the pointer (similar to a cursor in a text editor) to the end of the file
                stream.seek(0, os.SEEK_END)

                # This code means the following code skips the very last character in the file -
                # i.e. in the case the last line is null we delete the last line
                # and the penultimate one
                pos = stream.tell() - 1

                # Read each character in the file one at a time from the penultimate
                # character going backwards, searching for a newline character
                # If we find a new line, exit the search
                while pos > 0 and stream.read(1) != "\n":
                    pos -= 1
                    stream.seek(pos, os.SEEK_SET)

                # So long as we're not at the start of the file, delete all the characters ahead
                # of this position
                if pos > 0:
                    stream.seek(pos, os.SEEK_SET)
                    stream.truncate()

                stream.seek(0, os.SEEK_SET)
            else:
                stream = StringIO(content)

            df = pd.read_csv(
                stream,
                sep=rf'\s*{self._delimiter}\s*',
                engine='python',
            )

            if type(df) is not pd.DataFrame:
                raise Exception('Callback must return pandas.DataFrame')

            os.makedirs(self._cache_dir, exist_ok=True)

            df.to_pickle(content_file_path)

            self._writeCache(str(data_timestamp), timestamp_cache_key)

            return df

        if cached_timestamp is not None:
            if data_timestamp > int(cached_timestamp):
                return update()
            else:
                return pd.read_pickle(content_file_path)
        else:
            return update()

    def _getHash(self, url: str) -> str:
        return hashlib.sha1(url.encode()).hexdigest()

    def load(self, options: dict = {}):
        return self._cache(
            options.get('url'),
            options.get('cache', 5)
        )
