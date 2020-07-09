class Loader():
    """
    Abstract data loader class.
    """

    def __init__(self, config: dict = {}):
        pass

    def load(self, options: dict = {}):
        raise NotImplementedError
