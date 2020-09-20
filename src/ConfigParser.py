from src.exceptions.ConfigError import ConfigError
from src.StrParser import StrParser
from src.InfoGeneratorFactory import InfoGeneratorFactory
import datetime

class ConfigParser():
    """
    Parser to ensure that the necessary information can
    be found in the input configuration and also packs
    different information for further use
        - job information
    """
    def __init__(self, config):
        self.config = config
        self.__parse()

    def __parse(self):
        """
        Main function to execute different forms of parsing
        """
        self.__parse_global_info()
        self.__parse_jobs()

    def __get_date(self, src_info, info_generator):
        """
        Parse date to obtain correct run
        """
        if self.config['date'] == 'latest':
            date = info_generator.get_latest_date()
            return datetime.datetime.strptime(
                    date,
                    '%Y-%m-%d')

        return datetime.datetime.strptime(
                self.config['date'],
                '%Y-%m-%d')

    def __parse_global_info(self):
        """
        Saves common information required by Processes
        """
        self.job_max_tries = self.config['job_details']['retries']
        self.job_retry_wait_time = self.config['job_details']['retry_wait_time']

    def __parse_jobs(self):
        """
        Generate configuration to be used by processes
        """
        if 'sources' not in self.config:
            raise ConfigError('Please specify the sources')

        self.job_info = []
        for src_info in self.config['sources']:
            src_name = src_info['name'] if 'name' in src_info else ''

            if 'type' not in src_info:
                raise ConfigError('Please specify source type for {}'.format(src_name))

            type = src_info['type']
            jobs = src_info['jobs']
            parsing_type = src_info['parsing']

            info_generator = InfoGeneratorFactory.get_info_generator(parsing_type)

            date = self.__get_date(src_info, info_generator)

            str_parser = StrParser(date, info_generator)

            for job in jobs:

                name = '{}.{}'.format(src_name, job['name'])

                job_details = {
                    'name': name,
                    'type': type,
                    'max_tries': self.job_max_tries,
                    'retry_wait_time': self.job_retry_wait_time
                }

                for key, val in job.items():
                    if key not in job_details:
                        job_details[key] = str_parser.parse(val, parsing_type)

                self.job_info.append(job_details)

    def get_job_info(self):
        """
        Return a list of information required to create a list of processes
        """
        return self.job_info

    def use_concurrency(self):
        return 'concurrency' in self.config

    def get_concurrency_config(self):
        """
        Get config relevant to concurrency
        """
        return self.config['concurrency']

    def get_runner_timeout(self):
        """
        Returns the timeout for each req
        """
        return self.config['runner_details']['timeout']



