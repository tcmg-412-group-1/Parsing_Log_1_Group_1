import pip._vendor.requests as request
import re
from collections import Counter
import csv

url = "https://s3.amazonaws.com/tcmg476/http_access_log"

r = request.get(url, stream=True)

open('parsing_log_1', 'wb'). write(r.content)

def reader(filename):
    with open(filename) as file:
        log = file.read()
        regexp = r'\d{2}\/\D{3}\/\d{4}'
        time = re.findall(regexp, log)
        return(time)

def count(time):
    return Counter(time)

def write_csv(counter):
    with open ('frequency.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        header = ['Date and Time', 'Frequency']
        writer.writerow(header)
        for item in counter:
            writer.writerow((item, counter[item]))

write_csv(count(reader('parsing_log_1')))