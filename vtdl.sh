#!/bin/sh
# Simple bash script for downloading samples from VirusTotal.
# Requires curl, wget, and jq.

if [ "$#" -eq 0 ]; then
    echo "Usage: $0 <query..>"
    exit 1
fi

# Fetch the apikey and the query.
APIKEY="$(cat ~/.vtdl)"
QUERY="$*"

if [ -z "$APIKEY" ]; then
    echo "Please provide a proper apikey (put it in ~/.vtdl)!"
    exit 1
fi

if [ -z "$QUERY" ]; then
    echo "Please provide a search query!"
    exit 1
fi

for hash in $(curl -s https://www.virustotal.com/vtapi/v2/file/search -F "apikey=$APIKEY" -F "query=$QUERY"|jq -r '.hashes[]'); do
    echo "https://www.virustotal.com/vtapi/v2/file/download?apikey=$APIKEY&hash=$hash" -O "$hash"
done|xargs -P 10 -n 3 wget
