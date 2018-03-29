#!/usr/bin/python

import re

parsed = open('parsed_cache.txt', 'w') # output file
with open('named_dump.db','r') as dump: # file to be parsed
    data = dump.readlines()

# regex notations    
regex = '(^[^;]*$)'
regex2 = '(^[^$]*$)'
regex_ip = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
regex_url= '^\w+\.[a-z]+'  # quite simple don't use it anywhere else

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
                parsed.write(parsed_url+',')
            if i:
                parsed_ip = i.group().strip()
                parsed.write(parsed_ip+'\n')

parsed.close()
