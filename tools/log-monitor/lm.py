from typing import Dict, Any
import json
import logging
import os
import signal
import subprocess
import sys
import threading
import time

stop_signal = False
status_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'status.json'
)
settings_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'settings.json'
)
json_settings: Dict[str, Any] = {}


def monitor_log():

    global stop_signal
    status = {}
    if os.path.exists(status_file):
        logging.info('Loading existing status file')
        with open(status_file) as f:
            status = json.load(f)
    else:
        logging.info('Status file does not exist, will create one')
        status = {
            'last_position': 0,
            'modification_time': 0
        }

    while stop_signal is False:

        for _ in range(json_settings['matching']['interval_sec']):
            time.sleep(1)
            if stop_signal:
                break

        if status['last_position'] > os.path.getsize(json_settings['log_path']):
            logging.info(
                'last_position is greater than log file size, resetting to 0'
            )
            status['last_position'] = 0
            with open(status_file, 'w') as f:
                json.dump(status, f)
        elif status['last_position'] == os.path.getsize(json_settings['log_path']):
            #  os.path.getmtime():
            # Return the time of last modification of path. The return value
            # is a floating point number giving the number of seconds since
            # the epoch (see the time module).
            modification_time = os.path.getmtime(json_settings['log_path'])
            if status['modification_time'] == modification_time:
                logging.info(
                    f'log file size ({status["last_position"]}bytes) and time '
                    f'of last modification ({modification_time}) not changed')
                continue

        with open(json_settings['log_path']) as f:
            f.seek(status['last_position'])
            loglines = f.readlines()
            status['last_position'] = f.tell()
            with open(status_file, 'w') as f:
                json.dump(status, f)

            for logline in loglines:
                if json_settings['matching']['keyword'] not in logline:
                    continue
                evaluated_cmd = []
                for ele in json_settings['matching']['on_matched']:
                    evaluated_cmd.append(
                        ele.format(LINE=logline)
                    )
                subprocess.call(evaluated_cmd)

    logging.debug('stop_signal received, monitor_log() exited')


def signal_handler(*args):

    global stop_signal
    stop_signal = True
    logging.info('Stop signal received, exiting')


def main() -> None:

    global json_settings
    with open(settings_file) as f:
        json_settings = json.load(f)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(module)s | %(funcName)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    logging.info('Log monitor started')

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    if os.path.exists(json_settings['log_path']) is False:
        logging.error('Log file not found')
        sys.exit(1)

    ml_thread = threading.Thread(target=monitor_log, args=())
    ml_thread.start()
    ml_thread.join()


if __name__ == '__main__':
    main()
