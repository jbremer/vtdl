#!/usr/bin/env python
# Simple Python script for searching & downloading samples from VirusTotal.

import gevent.monkey
gevent.monkey.patch_all()

import click
import os.path
import requests

VT_SEARCH = "https://www.virustotal.com/vtapi/v2/file/search"
VT_DOWNLOAD = "https://www.virustotal.com/vtapi/v2/file/download"

apikey = open(os.path.expanduser("~/.vtdl"), "rb").read().strip()

@click.group()
def vtdl():
    pass

@vtdl.command()
@click.argument("query")
@click.option("-c", "--count", default=100)
def search(query, count):
    data = {
        "apikey": apikey,
        "query": query,
    }

    r = requests.post(VT_SEARCH, data=data)

    hashes = []
    while len(hashes) < count:
        hashes.extend(r.json()["hashes"])

        data["offset"] = r.json()["offset"]
        r = requests.post(VT_SEARCH, data=data)

    download(hashes[:count])

def _download_helper(h):
    r = requests.get(VT_DOWNLOAD, params={"apikey": apikey, "hash": h})
    open(h, "wb").write(r.content)

@vtdl.command()
@click.argument("hashes", nargs=-1)
def download(hashes):
    workers = []
    for h in hashes:
        workers.append(gevent.spawn(_download_helper, h))
    gevent.joinall(workers)

if __name__ == "__main__":
    vtdl()
