from src.Process import Process
import requests
import os

class DLProcess(Process):
    """
    Process to download files from online sources
    """
    def __init__(self, params):
        super(DLProcess, self).__init__(params)

    def func(self):
        """
        Downloads the file according to the provided configuration
        """
        url, output_path, file_name \
            = self.params['url'], self.params['output_path'], self.params['file_name']

        self.logger.info('Downloading from {}'.format(url))

        r = requests.get(url)

        self.logger.info('Download completed. Writing to {}{}'.format(output_path, file_name))

        os.makedirs(output_path, exist_ok=True)

        with open(self.params['output_path'] + self.params['file_name'], 'wb') as f:
            f.write(r.content)

        self.logger.info('Complete writing to {}{}'.format(output_path, file_name))