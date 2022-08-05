#!/usr/bin/python3

import click
import datetime as dt
import logging
import os
import socket
import subprocess
import time

app_dir = os.path.dirname(os.path.realpath(__file__))
log_path = os.path.join(app_dir, 'bn.log')

@click.command()
@click.option('--debug', is_flag=True)
@click.option('--delay', default=300, help='seconds to wait before sending')
@click.option('--tail', default=30, help='lines of log to append')
def main(debug: bool, delay: int, tail: int):

    boot_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logging.basicConfig(
        filename=log_path,
        level=logging.DEBUG if debug else logging.INFO,
        format=('%(asctime)s %(levelname)s '
                '%(module)s - %(funcName)s: %(message)s'),
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    logging.debug(f'Delay for {delay} seconds before sending notification')
    time.sleep(delay)

    fsck_info = ''
    if os.uname()[4][:3] == 'arm':
        fsck_info += '\n\nIt appears that this is an ARM-based platform, '
        fsck_info += 'its fsck information is shown as follows:\n'
        for line in open('/var/log/syslog'):
            if "systemd-fsck" in line:
                fsck_info += line

    try:
        with open(log_path, 'r') as log_file:
            lines = log_file.readlines()[-1 * tail:]
            lines = ''.join(lines)
    except Exception as e:
        logging.info('Unable to read log file'
                     f'(notification will be sent anyway): {e}')

    cmd = ['/bin/echo', '-e',
           (f'Subject:Device [{socket.getfqdn()}] booted\n'
            f'{socket.getfqdn()} is booted at {boot_time}{fsck_info}\n\n'
            f'Latest log:\n{lines}')]
    p1 = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    cmd = ['/usr/bin/msmtp', '-t', 'root']
    p2 = subprocess.Popen(cmd, stdin=p1.stdout,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p2.communicate()

    if p2.returncode == 0:
        logging.info('boot notification sent without errors')
    else:
        logging.error(f'msmtp returns non-zero exit code: {p2.returncode}')
        logging.error(f'stdout: {stdout.decode("utf-8")}')
        logging.error(f'stderr: {stderr.decode("utf-8")}')


if __name__ == '__main__':

    main()
