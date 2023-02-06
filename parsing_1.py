#!/usr/bin/env python3

from collections import Counter
from datetime import datetime
import re
import requests

URL = "https://s3.amazonaws.com/tcmg476/http_access_log"
CACHED_LOG_FILENAME = "parsing_log_1"
APACHE_LOG_DATE_FORMAT = "%d/%b/%Y"

# log format:
# hostname( identity)? userid [DD/Mon/YYYY:HH:MM:SS -####] "request" status response_size
# Note that this skips malformed lines like the one on line 604735 in the
# example file. Unfortunately, this causes the regex to be much longer than
# it needs to be. I'd love to write a proper parser for this, but the
# prospect of doing so in a dynamically typed language scares me a little.
APACHE_LOG_REGEX = r"^[_0-9.A-Za-z-]+(?: [_0-9.A-Za-z-]+)? [_0-9.A-Za-z-]+ \[(\d{2}\/\w{3}\/\d{4}):\d{2}:\d{2}:\d{2} -\d{4}\] \"[^\"]*\" \d{3} [0-9-]+$"

def parse(log):
    dates = re.findall(APACHE_LOG_REGEX, log, re.MULTILINE)
    # This maps `datetime.strptime` across every date in dates and creates a
    # new list with the results
    return [datetime.strptime(date, APACHE_LOG_DATE_FORMAT) for date in dates]

file_contents = ""

try:
    # Counterintuitively, brazenly trying to open the file and handling any
    # resultant errors is better than checking if the file exists. Checking for
    # existence before opening the file could lead to a time-of-check to
    # time-of-use bug.
    with open(CACHED_LOG_FILENAME, "r") as log:
        file_contents = log.read()
except FileNotFoundError:
    with open(CACHED_LOG_FILENAME, "w") as log:
        r = requests.get(URL, stream=True)
        # When reading a file, Python automatically decodes the data from
        # UTF-8 and normalizes all Windows-style newlines to Unix-style
        # newlines. Here, we have to do it ourselves.
        file_contents = r.content.decode().replace("\r\n", "\n")
        log.write(file_contents)

dates = parse(file_contents)
