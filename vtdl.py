#!/usr/bin/env python
# Simple Python script for searching & downloading samples from VirusTotal.

import gevent.monkey
import gevent.queue
gevent.monkey.patch_all()

import click
import os.path
import requests
import time

VT_SEARCH = "https://www.virustotal.com/vtapi/v2/file/search"
VT_DOWNLOAD = "https://www.virustotal.com/vtapi/v2/file/download"

apikey = open(os.path.expanduser("~/.vtdl"), "rb").read().strip()
queue = gevent.queue.Queue()

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

        if "offset" not in r.json():
            break

        data["offset"] = r.json()["offset"]
        r = requests.post(VT_SEARCH, data=data)

    download(hashes[:count])

def _download_helper():
    t = time.time()
    while not queue.empty():
        h = queue.get()
        if not h:
            break

        if h == "wait":
            time.sleep(max(0, 60 - time.time() + t))
            t = time.time()
            continue

        if os.path.exists(h):
            print "skipping..", h
            continue

        r = requests.get(VT_DOWNLOAD, params={"apikey": apikey, "hash": h})
        open(h, "wb").write(r.content)

@vtdl.command()
@click.argument("hashes", nargs=-1)
def download(hashes, workercount=32):
    for idx, h in enumerate(hashes):
        if idx and idx % 500 == 0:
            for _ in xrange(workercount):
                queue.put("wait")
        queue.put(h)

    workers = [
        gevent.spawn(_download_helper)
        for _ in xrange(workercount)
    ]
    gevent.joinall(workers)

if __name__ == "__main__":
    vtdl()
