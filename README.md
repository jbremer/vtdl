# vtdl
Easiest way to download samples through VirusTotal Intelligence.

Setup by running the following command as root: `cp vtdl.py /usr/bin/vtdl`.

E.g., given `hashes.txt` containing a list of md5 or sha1 hashes, to download
all the samples (that are available on VirusTotal anyway), run:
`vtdl $(cat hashes.txt)`.
