from yaml import load, Loader
from src.ConfigParser import ConfigParser
from src.ProcessFactory import ProcessFactory
import logging
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

class Runner():
    def __init__(self, config_path, input_date):
        self.config_path = config_path
        self.input_date = input_date
        self.__setup()

    def run(self):
        """
        Main function to run jobs
        May use multithreading if added in config
        """
        num_jobs = len(self.processes)

        if self.config_parser.use_concurrency():
            concurrency_config = self.config_parser.get_concurrency_config()

            num_workers = concurrency_config['num_workers'] \
                    if concurrency_config['type'] == 'manual' \
                    else min(os.cpu_count() * 2, num_jobs)

            self.logger.info('[Concurrency] Using {} worker(s)'.format(num_workers))

            with ThreadPoolExecutor(max_workers=num_workers) as executor:
                futures = [
                    executor.submit(process.execute) for process in self.processes
                ]

                runner_timeout = self.config_parser.get_runner_timeout()

                for future in as_completed(futures, 60 * runner_timeout):
                    try:
                        result = future.result()
                    except Exception as e:
                        self.logger.exception(e)
        else:
            self.results = [process.execute() for process in self.processes]

    def __setup_logger(self):
        """
        Setup logger according to config
        """
        logging_path = self.config['logger']['output_file']
        os.makedirs(os.path.dirname(logging_path), exist_ok=True)
        file_handler = logging.FileHandler(logging_path, mode='w+')

        self.logger = logging.getLogger('main')

        self.logger.addHandler(file_handler)

    def __setup(self):
        """
        Setup for further operations
         - Configuration parsing
         - Create processes
        """

        with open(self.config_path, 'r') as f:
            self.config = load(f, Loader=Loader)

        self.config['date'] = self.input_date

        self.__setup_logger()

        try:
            self.config_parser = ConfigParser(self.config)
        except Exception:
            self.logger.exception('Failed to parse config')
            sys.exit(1)


        processes_info = self.config_parser.get_job_info()

        self.processes = [
            ProcessFactory.get_process(params, params['type']) \
                    for params in processes_info
        ]