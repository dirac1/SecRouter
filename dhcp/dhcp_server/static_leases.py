#!/usr/bin/python
# APPLY BUTTON for the DHCP TAB in the category Static Leases

import os
import fileinput
import ipaddress
import subprocess
import sys

# variables
interface = sys.argv[1]
hostname = sys.argv[2]
ip = sys.argv[3]
mac = sys.argv[4]

# functions
from misc_rs import cow # check or  write
from misc_rs import execute # execute a command 

# -------------------------- main -----------------------------
def main(interface, hostname, ip, mac):

    checkfile = 'include \"/etc/dhcpcd.d/static.leases.' + interface + '\";'
    cow('/etc/dhcpcd.conf', checkfile)

    static_leases = open('/etc/dhcpcd.d/static.leases.' + interface,'a')
    data = [ 'host ' + hostname + '{' \
             ,'hardware ethernet ' + mac + ';' \
             , 'fixed-address ' + ip + ';' \
             , '}\n' ]
    static_leases.writelines('\n'.join(data))

     # Restart the dhcp server   
    for path in execute(['/etc/init.d/isc-dhcp-server','restart']):
        print(path, end='')

main(interface,hostname,ip,mac)
