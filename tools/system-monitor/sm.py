#!/usr/bin/python3
from elasticsearch import Elasticsearch
from typing import Dict, Any

import datetime as dt
import json
import os
import psutil
import socket
import subprocess

curr_dir = os.path.dirname(os.path.realpath(__file__))
config_path = os.path.join(curr_dir, 'config.json')
config: Dict[str, Any] = {}


def get_system_resources() -> Dict[str, Any]:
    return {
        'host': socket.getfqdn(),
        'cpu': psutil.cpu_percent(interval=5),
        'ram': psutil.virtual_memory()[2],
        'timestamp_utc': dt.datetime.utcnow(),
    }


def get_cpu_temp()-> Dict[str, Any]:

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


def main():

    global config
    with open(config_path, 'r') as f:
        config = json.load(f)

    es = Elasticsearch(
        config['es']['url'],
        http_auth=(config['es']['username'], config['es']['password'])
    )

    for key in config['items']:
        if config['items'][key] is False:
            continue
        sr_doc = get_system_resources()
        resp = es.index(index=key, body=sr_doc)
        if resp['result'] != 'created':
            raise RuntimeError(resp)


if __name__ == "__main__":
    main()
