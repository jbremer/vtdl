#!/bin/sh
# Simple bash script for downloading samples from VirusTotal.
# Requires curl, wget, and jq.

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 [-1] <query..>"
    echo "  -1: Do not split the query up, use it as a whole."
    exit 1
fi

# Fetch the apikey and the query.
APIKEY="$(cat ~/.vtdl)"

if [ -z "$APIKEY" ]; then
    echo "Please provide a proper apikey (put it in ~/.vtdl)!"
    exit 1
fi

if [ -z "$*" ]; then
    echo "Please provide a search query!"
    exit 1
fi

# Search for something and download all matches.
vt_search() {
    echo "Query: $*"
    for hash in $(curl -s https://www.virustotal.com/vtapi/v2/file/search -F "apikey=$APIKEY" -F "query=$*"|jq -r ".hashes[]"); do
        echo "https://www.virustotal.com/vtapi/v2/file/download?apikey=$APIKEY&hash=$hash" -O "$hash"
    done|xargs -P 10 -n 3 wget
}

if [ "$1" = "-1" ]; then
    vt_search "$*"
    exit 0
fi

# Try to download one or more sample(s) by hash.
for part in $*; do
    if echo $part|grep -Eq '^[a-fA-F0-9]{32,64}$'; then
        if wget -q "https://www.virustotal.com/vtapi/v2/file/download?apikey=$APIKEY&hash=$part" -O "$part"; then
            echo "Downloaded sample by hash: $part"
        else
            echo "Not a known hash: $part"
            vt_search "$part"
        fi
    else
        vt_search "$part"
    fi
done
