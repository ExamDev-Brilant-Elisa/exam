#ddos

import requests

from datetime import date
from datetime import time

def ddos(ip, date, time):

    if (date == 2019, 11, 6) and (time == 22, 52):
        requests.post(ip, data={key:value})
        print("coucou")
    else:
        print("error")

print (ddos (date, time))

#récupérer les lignes

def get_log(lines):
    log_file = open("file","r")
    lines = 0
    for lines in file.readlines():
        lines += 1
    counter = lines-5
    for line in file.readlines(counter,lines):
        print(line)






