#!/usr/bin/python

import re
import subprocess


# functions
from misc_rs import execute # execute a command 

# ----------- main -------------
def main():

    for path in execute(["rndc","dumpdb","-cache"]):
        print(path , end = '')

    parsed = open('/home/secrouter/eth_route/dns/parsed_cache.csv', 'w') # output file
    with open('/var/cache/bind/named_dump.db','r') as dump: # file to be parsed
        data = dump.readlines()


    # regex notations    
    regex = '(^[^;]*$)'
    regex2 = '(^[^$]*$)'
    regex_ip = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
    regex_url='(https?:\/\/)?([\da-zA-Z\.-]+)\.([a-zA-Z\.]{2,6})([\/\w\.-]*)*\/?'
    # parsing
    for line in data:
        z = re.match( regex, line )
        w = re.match( regex2, line )
        if z and w:
            parsed_data = z.group().strip().split()
            for value in parsed_data:
                u = re.match( regex_url, value )
                i = re.match( regex_ip, value )
                if u:
                    parsed_url = u.group().strip()
                    parsed.write(parsed_url)
                if i:
                    parsed_ip = i.group().strip()
                    parsed.write(','+parsed_ip+'\n')

    parsed.close()

main()
