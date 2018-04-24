#!/usr/bin/python
# coding = utf-8

import re
import sys
from subprocess import check_output

table = sys.argv[1]

parsed = open('/home/secrouter/firewall/parsed_chain.txt', 'w') # output file
out = check_output(['iptables','-L','-t',table])
out = out.decode("utf-8").split('\n')
regex = '(^Chain.*\()'
for data in out:
    z = re.match(regex,data)
    if z:
        parsed_value = z.group().replace('Chain','').replace(' (','')
        print(z.group().replace('Chain','').replace(' (',''))
        parsed.write(parsed_value+'\n')
parsed.close()
