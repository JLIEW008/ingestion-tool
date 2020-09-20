class ConfigError(Exception):
    """
    Exception raised for errors in the config
    """

    def __init__(self, message):
        self.message = message