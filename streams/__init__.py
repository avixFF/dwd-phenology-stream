class Stream():
    '''
    Abstract stream factory
    '''

    types = [
        'dwd-phenology',
    ]

    def __init__(self, config: dict = {}):
        self._config = config

    @staticmethod
    def make(stream_type: str, config: dict = {}):
        if stream_type not in Stream.types:
            raise Exception(f'Unsupported stream type "{stream_type}"')

        if stream_type == 'dwd-phenology':
            import streams.dwd
            return dwd.Stream(config)

    def fetch(self):
        raise NotImplementedError
