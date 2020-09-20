import os

class InfoGenerator():
    base_directory = 'mapping/'

    def __init__(self):
        os.makedirs(self.base_directory, exist_ok=True)
        self.files_loaded = {}

    def cache(self, file_name, content):
        """
        Creates a cache to prevent reloading.
        Only effective if Singleton Implemented...
        """
        self.files_loaded[file_name] = content

    def get_latest_date(self):
        pass

    def generate(self):
        pass

    def load(self, file_name):
        pass