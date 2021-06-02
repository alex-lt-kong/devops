#!/usr/bin/python3

import datetime
import os
import socket
import subprocess
import sys
import time

boot_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# This delay has to be long enough to accommodate the startup time of pfSense.
time.sleep(300)

fsck_info = ''
if os.uname()[4][:3] == 'arm':
    fsck_info += '\n\nIt appears that this is an ARM-based platform, its fsck information is shown as follows:\n'
    for line in open('/var/log/syslog'):
        if "systemd-fsck" in line:
            fsck_info += line

ps = subprocess.Popen(('/bin/echo', '-e', 'Subject:[{}] Booted\n{} is booted at {}{}'.format(socket.gethostname(), socket.gethostname(), boot_time, fsck_info)), stdout=subprocess.PIPE)
output = subprocess.check_output(('/usr/bin/msmtp', '-t', 'root'), stdin=ps.stdout)


