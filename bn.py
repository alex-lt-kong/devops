#!/usr/bin/python3

import click
import datetime as dt
import logging
import os
import socket
import subprocess
import time

app_dir = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option('--debug', is_flag=True)
@click.option(
    '--delay', default=300,
    help='Number of seconds to wait before sending the notification email')
def main(debug: bool, delay: int):

    boot_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logging.basicConfig(
        filename=os.path.join(app_dir, 'bn.log'),
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

    cmd = ['/bin/echo', '-e',
           (f'Subject:Device [{socket.gethostname()}] booted\n'
            f'{socket.gethostname()} is booted at {boot_time}{fsck_info}')]
    ps = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    cmd = ['/usr/bin/msmtp', '-t', 'root']
    p = subprocess.Popen(cmd, stdin=ps.stdout,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()

    if p.returncode == 0:
        logging.info('boot notification sent without error')
    else:
        logging.error(f'ffmpeg non-zero exist code: {p.returncode}')
        logging.error(f'stdout: {stdout.decode("utf-8")}')
        logging.error(f'stderr: {stderr.decode("utf-8")}')


if __name__ == '__main__':

    main()
