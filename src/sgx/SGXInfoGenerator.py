from src.InfoGenerator import InfoGenerator
import json
import requests
import datetime
import os
import operator

class SGXInfoGenerator(InfoGenerator):
    """
    Generates relevant mapping to be used by
    StrParser to convert variables to the expected
    name
    TODO: Change to Singleton for effective caching and prevent mistakes
    """
    # file to store mapping of <date>: <idx>
    MAPPING_FILE_NAME = 'sgx_date_mapping.json'

    # using tick data filename from sgx to obtain date from idx
    MAPPING_URL = 'https://links.sgx.com/1.0.0/derivatives-historical/{idx}/TC.txt'

    # File formats
    MAPPING_FORMAT = [
        '%Y%m%d_web.atic1',
        '%Y%m%d.atic1',
        'TC_%Y%m%d.txt'
    ]

    # unavailable data on SGX
    UNAVAILABLE_INDICES = set([
        2725, 2726, 2727, 2728, 2729, 2730, 2731, 2732, 2733, 2734,
        2735, 2736, 2737, 2738, 2739, 2740, 2741, 2742, 2743, 2744,
        2745, 2746, 2747, 2748, 2749, 2750, 2751, 2752, 2753, 2754,
        2771, 2772, 2873, 3025, 3257, 3590, 3591, 3710, 3711, 3712,
        3848, 3849, 3874, 4239
    ])

    def __init__(self):
        super(SGXInfoGenerator, self).__init__()

    def get_latest_date(self):
        """
        Obtains latest date with data.
        Determined from mapping file for SGX data
        """
        return self.get_latest_mapping_date()

    def get_latest_mapping_date(self):
        """
        Obtain mapping and return max date
        """
        mapping = self.load_mapping_file()
        return max(mapping.keys())

    def generate(self):
        """
        Create/update mapping files
        """
        self.generate_date_to_idx()

    def generate_date_to_idx(self):
        """
        Generates the whole range of indices
        Determined from request header
        """
        file_path = self.base_directory + self.MAPPING_FILE_NAME

        mapping = self.load_mapping_file()
        available_indices = [idx for date, idx in mapping.items()]

        max_idx = max(available_indices) if len(available_indices) > 0 else 0

        idx = max_idx + 1

        while True:
            r = requests.head(self.MAPPING_URL.replace('{idx}', str(idx)))

            if r.headers['Content-Type'] == 'application/download':
                content_disposition = r.headers['Content-Disposition']
                file_name = content_disposition.split('filename=')[-1]

                date = self.__get_sgx_date(file_name, idx)

                date_str = date.strftime('%Y-%m-%d')

                mapping[date_str] = idx
            else:
                if idx not in self.UNAVAILABLE_INDICES:
                    break
            idx += 1

        with open(file_path, 'w') as f:
            json.dump(mapping, f)

    def __get_sgx_date(self, date_str, idx):
        """
        Returns the correct date according to the available formats
        """
        for format in self.MAPPING_FORMAT:
            try:
                date = datetime.datetime.strptime(date_str, format)
                break
            except ValueError as e:
                print(e)
        return date

    def load_mapping_file(self):
        return self.load(self.MAPPING_FILE_NAME)

    def load(self, file_name):
        """
        Load function. Does not ensure that the file is updated.
        Uses cache if available
        """
        if file_name in self.files_loaded:
            return self.files_loaded[file_name]

        file_path = self.base_directory + file_name

        if not os.path.exists(file_path):
            with open(file_path, 'w+') as f:
                json.dump({}, f)

        with open(file_path, 'r') as f:
            content = json.load(f)

        self.cache(file_name, content)

        return content