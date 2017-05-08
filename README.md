# vtdl
Easiest way to download samples through VirusTotal Intelligence.

Setup by running the following command as root: `cp vtdl.py /usr/bin/vtdl`.

Example use-cases:

* Download one or more hashes: `vtdl download hash1 hash2`.
* Given`hashes.txt` containing a list of md5 or sha1 hashes, to download
  all the samples (that are available on VirusTotal anyway), run:
  `vtdl download $(cat hashes.txt)`.
* Search for a malware family or variant and fetch the first 5000 samples:
  `vtdl search zeus -c 5000`.
