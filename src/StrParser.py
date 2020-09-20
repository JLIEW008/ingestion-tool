import datetime

class StrParser():
    """
    Class to parses config strings
    """

    # list of supported types currently
    SUPPORTED_PARSING_TYPES = [
        'sgx'
    ]

    # mapping file
    sgx_mapping = None

    def __init__(self, date, info_generator):
        self.date = date
        self.info_generator = info_generator
        self.info_generator.generate()

    def parse(self, string, type=None):
        """
        Default only parses for date

        :param: String to parse
        :param: Type of parsing applied
            - SGX: Change {SGX_DATE} to int
        """
        string = self.date.strftime(string)

        if type in self.SUPPORTED_PARSING_TYPES:
            string = self.extra_parse(string, type)

        return string

    def extra_parse(self, string, type):
        """
        Executes additional parsing according to type
        """
        if type == 'sgx':
            if self.sgx_mapping is None:
                self.sgx_mapping = self.info_generator.load_mapping_file()
            string = string.replace('{SGX_DATE}', str(self.__get_sgx_date()))

        return string

    def __get_sgx_date(self):
        """
        Returns {SGX_IDX} given date
        """
        formatted_date = self.date.strftime('%Y-%m-%d')

        if formatted_date not in self.sgx_mapping:
            raise ValueError('Date provided does not exists')

        return self.sgx_mapping[formatted_date]
