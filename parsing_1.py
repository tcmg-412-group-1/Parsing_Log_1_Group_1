#!/usr/bin/env python3

import requests
import re
from collections import Counter
import csv

URL = "https://s3.amazonaws.com/tcmg476/http_access_log"
CACHED_LOG_FILENAME = "parsing_log_1"

def parse(log):
    regexp = r'\d{2}\/\D{3}\/\d{4}'
    time = re.findall(regexp, log)
    return time

def write_csv(counter):
    with open('frequency.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Date and Time', 'Frequency']
        writer.writerow(header)
        for item in counter:
            writer.writerow((item, counter[item]))

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

write_csv(Counter(parse(file_contents)))
