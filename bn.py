#!/usr/bin/python3

import argparse
import datetime as dt
import os
import socket
import subprocess
import time


def main():

    ap = argparse.ArgumentParser()
    ap.add_argument('--debug', dest='debug', action='store_true')
    args = vars(ap.parse_args())
    debug_mode = args['debug']

    boot_time = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if debug_mode is False:
        time.sleep(300)
        # Delay the message so that it is sent AFTER network is up.

    fsck_info = ''
    if os.uname()[4][:3] == 'arm':
        fsck_info += '\n\nIt appears that this is an ARM-based platform, '
        fsck_info += 'its fsck information is shown as follows:\n'
        for line in open('/var/log/syslog'):
            if "systemd-fsck" in line:
                fsck_info += line

    command = ('/bin/echo', '-e',
               (f'Subject:Device [{socket.gethostname()}] booted\n'
                f'{socket.gethostname()} is booted at {boot_time}{fsck_info}'))
    ps = subprocess.Popen(command, stdout=subprocess.PIPE)
    output = subprocess.check_output(('/usr/bin/msmtp', '-t', 'root'),
                                     stdin=ps.stdout)


if __name__ == '__main__':

    main()
