#!/usr/bin/python3
from elasticsearch import Elasticsearch

import datetime as dt
import os
import psutil
import socket


es_url = os.environ['ELASTICSEARCH_URL']
es_http_username = os.environ['ELASTICSEARCH_HTTP_USERNAME']
es_http_password = os.environ['ELASTICSEARCH_HTTP_PASSWORD']


def main():
    es = Elasticsearch(
        es_url, http_auth=(es_http_username, es_http_password)
    )

    doc = {
        'host': socket.getfqdn(),
        'cpu': psutil.cpu_percent(interval=5),
        'ram': psutil.virtual_memory()[2],
        'timestamp_utc': dt.datetime.utcnow(),
    }

    resp = es.index(index="system-resources",  document=doc)
    if resp['result'] != 'created':
        raise RuntimeError(resp)


if __name__ == "__main__":
    main()
