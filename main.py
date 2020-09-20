import argparse
from src.Runner import Runner
from src.Utils import set_logging_format
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description = 'File ingestion'
    )

    parser.add_argument(
        'config_path',
        type=str,
        help='path to config file. Expected to be yaml/json')

    parser.add_argument(
        '--date',
        type=str,
        default='latest',
        help='Date to extract data - YYYY-MM-DD format')

    args = parser.parse_args()

    set_logging_format()

    start = datetime.datetime.now()

    runner = Runner(args.config_path, args.date)

    runner.run()