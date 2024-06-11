import argparse
import datetime
import logging
import glob
import os
import shutil
import sys


def remove_file_or_directory(path):
    if os.path.isfile(path):
        os.remove(path)
        logging.info(f"File '{path}' has been removed.")
    elif os.path.isdir(path):
        shutil.rmtree(path)
        logging.info(f"Directory '{path}' and its contents have been removed.")
    else:
        logging.error(f"No file or directory found at '{path}'.")



def main():

    ap = argparse.ArgumentParser()
    ap.add_argument(
        '--pattern', '-p', dest='pattern', required=True,
        help=r"You should include {time_filter}, which will be replaced by the real filter"
    )
    ap.add_argument('--days-ago', '-d', dest='days_ago', required=True)
    args = vars(ap.parse_args())
    time_filter = (
        datetime.datetime.now() - datetime.timedelta(days=int(args['days_ago']))
    ).strftime("%Y%m%d")
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format='%(asctime)s|%(levelname)7s|%(funcName)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    pattern = args["pattern"].replace(r"{time_filter}", time_filter)
    logging.info(f'pattern: {pattern}')
    file_list = glob.glob(pattern)
    
    if len(file_list) == 0:
        logging.info('file_list is empty')
        
    for f in file_list:
        try:
            remove_file_or_directory(f)
        except Exception as ex:
            logging.error(f'Error removing {f}: {ex}')
        
    
if __name__ == '__main__':
        
    main()
