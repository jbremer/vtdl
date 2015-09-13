# vtdl
Easiest way to download samples through VirusTotal Intelligence.

Setup by running the following command as root: `cp vtdl.sh /usr/bin/vtdl`.
Also install all the required packages by running:
`apt-get install curl wget jq`.
From there on one can download one or more samples by hash or through the
search utility.

E.g., given `hashes.txt` containing a list of md5 or sha1 hashes, to download
all the samples (that are available on VirusTotal anyway), run:
`vtdl $(cat hashes.txt)`.
