import logging
import os

class Process():
    """
    Base process class
    Inherited classes should implement func
    """

    def __init__(self, params):
        self.name = params['name']
        self.params = params

        self.logger = logging.getLogger('main.' + self.name)

        logging_path = params['logs']
        os.makedirs(os.path.dirname(logging_path), exist_ok=True)
        file_handler = logging.FileHandler(logging_path, mode='w+')

        self.logger.addHandler(file_handler)

        self.tries = 0
        self.max_tries = params['max_tries']
        self.retry_wait_time = params['retry_wait_time']

    def execute(self):
        success = False
        while self.tries < self.max_tries:
            self.logger.info('Start Execution no. {}'.format(self.tries))

            try:
                self.func()
                success = True
            except Exception:
                self.logger.exception('{} failed..'.format(self.name))
            self.tries += 1

            if success:
                break
            else:
                self.logger.info('Waiting for {} minutes before retrying...')
                sleep(60 * self.retry_wait_time)

                self.logger.info('Retrying job...')

        if success:
            self.logger.info('Successful executed')
        else:
            self.logger.info('Terminating job - Failed {} times'.format(self.tries))

    def func(self):
        """
        Main function to execute
        """
        pass