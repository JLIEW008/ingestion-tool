import logging

def set_logging_format():
    """
    Set formatting for loggers
    """
    FORMAT = '[%(levelname)s] %(asctime)s [%(name)s] %(message)s'
    logging.basicConfig(format=FORMAT, level=logging.INFO)
