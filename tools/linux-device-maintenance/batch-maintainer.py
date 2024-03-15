#!/usr/bin/env python3

import argparse
import colorama
import datetime as dt
import json
import os
import stat
import subprocess
import sys

backup_path = ''
maintainer_path = ''
settings_path = './settings.json'
ssh_key_dir = '/tmp'
global_exclusions = ''

#from colorama import Fore, Style
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


def shell_maintenance_command(login, order: int, total: int):

    global maintainer_path

    with open(maintainer_path, 'w') as out:
        bash_script = f'''
shopt -s expand_aliases
source $HOME/.profile
{login} << HERE

  echo -e "\n{color.BOLD}unattended-upgrades log:{color.END}"
  tac /var/log/unattended-upgrades/unattended-upgrades.log | grep installed -m 1 -A 7 | tac

  echo -e "\n{color.BOLD}crontab:{color.END}"
  grep --invert-match "^#" /var/spool/cron/crontabs/root

  echo -e "\n{color.BOLD}System uptime:{color.END}"
  /usr/bin/uptime

  echo -e "\n{color.BOLD}Top-3 program by memory usage:{color.END}"
  /bin/ps -eo cmd,pid,ppid,%mem,%cpu --sort=-%mem | head -n 4

  echo -e "\n{color.BOLD}ufw status:{color.END}"
  /usr/sbin/ufw status

  echo -e "\n{color.BOLD}Sending test email...{color.END}"
  echo -e "subject:E-mail Facility Test ({order + 1:02} of {total:02})\\nThis is a test email" | msmtp -t root

HERE
'''
# grep --invert-match "^#" /var/spool/cron/crontabs/root -> match lines that do not start with # only
        out.write(bash_script + '\n')
    os.chmod(maintainer_path, stat.S_IXUSR + stat.S_IWRITE + stat.S_IREAD)
    subprocess.call(maintainer_path, shell=True, executable='/bin/bash')


def generate_and_run(server_name: str, username: str, host: str, port: int,
                     ssh_key: str, directory: str, exclusions: str):

    global backup_path
    server_backup_path = os.path.join(backup_path, server_name + '/')
    if os.path.isdir(server_backup_path) is False:
        os.mkdir(server_backup_path)

    if os.path.isfile(f'{ssh_key_dir}/{ssh_key}'):
        command = ['/usr/bin/rsync', '-av', '--relative',
                '--human-readable',
                '-e', f'/usr/bin/ssh -p {port} -i {ssh_key_dir}/{ssh_key}',
                f'{username}@{host}:{directory}', server_backup_path]
    else:
        command = ['/usr/bin/rsync', '-av', '--relative',
                '--human-readable',
                '-e', f'/usr/bin/ssh -p {port}',
                f'{username}@{host}:{directory}', server_backup_path]

    for exclusion in exclusions:
        command.extend(['--exclude', exclusion])

    print('\n\n\n========== Task to run ==========')
    print(f'Host: {host}\nDirectory: {directory}\nCommand: {" ".join(command)}')
    print('running...\n')

    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    # https://stackoverflow.com/questions/1606795/catching-stdout-in-realtime-from-subprocess
    for line in iter(p.stdout.readline, b''):
        print(">>> " + line.rstrip().decode('utf-8'))


def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--since-index', '-s', type=int, help='Skip all devices before index')
    args = parser.parse_args()

    global settings_path, backup_path, maintainer_path, ssh_key_dir, global_exclusions
    try:
        with open(settings_path, 'r') as json_file:
            json_str = json_file.read()
            json_data = json.loads(json_str)
        backup_path = os.path.join(json_data['settings']['backup_path'],
                                   dt.datetime.now().strftime('%Y%m%d') + '/')
        maintainer_path = json_data['settings']['maintainer_path']
        ssh_key_dir =  json_data['settings']['ssh_key_dir']
        global_exclusions =  json_data['settings']['global_exclusions']
    except Exception as e:
        print(f'JSON Error: {e}')
        return

    if os.path.isdir(backup_path) is False:
        os.mkdir(backup_path)

    servers_list = list(json_data['servers'].keys())
    for i in range(len(servers_list)):
        if i < args.since_index:
            continue
        print(colorama.Fore.RED  + color.BOLD + f'=====  {servers_list[i]} ({i} of {len(servers_list)}) =====\n' + color.END + colorama.Style.RESET_ALL)
        json_server = json_data['servers'][servers_list[i]]

        if os.path.isfile(f'{ssh_key_dir}/{json_server["key"]}'):
            login = 'ssh {}@{} -p {} -i {}/{}'.format(
                    json_server['user'],
                    json_server['host'],
                    json_server['port'],
                    ssh_key_dir,
                    json_server['key']
                )
        else:
            login = 'ssh {}@{} -p {}'.format(
                    json_server['user'],
                    json_server['host'],
                    json_server['port']
                )
        shell_maintenance_command(login, i, len(servers_list))

        input('Press Enter to start files backup')
        for j in range(len(json_server['directories'])):
            excl = json_server['exclusions']
            excl.extend(global_exclusions)
            generate_and_run(
                server_name=servers_list[i],
                username=json_server['user'],
                host=json_server['host'],
                port=json_server['port'],
                ssh_key=json_server['key'],
                directory=json_server['directories'][j],
                exclusions=excl
            )
        print('\n\n')

if __name__ == '__main__':

    main()
