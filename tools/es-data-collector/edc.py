#!/usr/bin/python3
from elasticsearch import Elasticsearch
from typing import Dict, Any

import datetime as dt
import logging
import json
import os
import psutil
import socket
import subprocess
import sys


curr_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(curr_dir, 'config.json')
config: Dict[str, Any] = {}


def get_environment_temperature() -> Dict[str, Any]:
    
    retry = 0
    max_retry = 10
    while retry < max_retry:

        f = open(config['environment-temperature']['device-path'], 'r')
        data = f.read()
        f.close()

        if "YES" in data:
            (discard, sep, reading) = data.partition(' t=')
            t = round(float(reading) / 1000.0, 1)
            if t <= 60 and t >= -10:
                break

        time.sleep(5)
        t = 32767
        retry += 1

    return {
        'host': socket.getfqdn(),
        'temp': t,
        'location': config['environment-temperature']['location'],
        'timestamp_utc': dt.datetime.utcnow(),
    }



def get_voltage() -> Dict[str, Any]:

    apcaccess_process = subprocess.Popen(['/sbin/apcaccess',
                                          '-u', '-p', 'LINEV'],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
    out, err = apcaccess_process.communicate()

    return {
        'host': socket.getfqdn(),
        'voltage': float(out.decode("utf-8")),
        'timestamp_utc': dt.datetime.utcnow(),
    }


def get_system_resources() -> Dict[str, Any]:
    return {
        'host': socket.getfqdn(),
        'cpu': psutil.cpu_percent(interval=5),
        'ram': psutil.virtual_memory()[2],
        'timestamp_utc': dt.datetime.utcnow(),
    }


def get_cpu_temp() -> Dict[str, Any]:

    sensors_process = subprocess.Popen(['/usr/bin/sensors', '-j'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    out, err = sensors_process.communicate()
    json_str = out.decode("utf-8")
    json_data = json.loads(json_str)
    return {
        'host': socket.getfqdn(),
        'temp': json_data['coretemp-isa-0000']['Package id 0']['temp1_input'],
        'timestamp_utc': dt.datetime.utcnow(),
    }


def upload_one_doc(es: Elasticsearch, doc, index) -> None:
    logging.info(f'Uploading data {doc} to [{index}]')
    resp = es.index(index=index, body=doc, request_timeout=30)
    if resp['result'] != 'created':
        raise RuntimeError(resp)


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    logging.info('Starting ES data collector')
    global config
    with open(config_path, 'r') as f:
        config = json.load(f)

    es = Elasticsearch(
        config['es']['url'],
        http_auth=(config['es']['username'], config['es']['password'])
    )

    for index in config['items']:
        if config['items'][index] is False:
            continue
        if index == 'system-resources':
            upload_one_doc(es, get_system_resources(), index)
        if index == 'cpu-temp':
            upload_one_doc(es, get_cpu_temp(), index)
        if index == 'voltage':
            upload_one_doc(es, get_voltage(), index)
        if index == 'environment-temperature':
            upload_one_doc(es, get_environment_temperature(), index)

    logging.info('ES data collector exited')


if __name__ == "__main__":
    main()
