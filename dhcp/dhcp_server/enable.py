#!/usr/bin/python
# ENABLE Button for the DHCP Tab in the category DHCP SERVER
# conding=utf-8
import os
import fileinput
import ipaddress
import subprocess
import sys

# variables
interface = sys.argv[1]
network= sys.argv[2]
prefix = sys.argv[3]
gateway= sys.argv[4]

# functions
from misc_rs import comment #check or write
from misc_rs import execute # execute a command 

# -------------------------- main -----------------------------
def main(interface,network,prefix,gateway):
    networkprefix = network +"/"+ prefix
    # -------------------------- ip calculations -----------------------------
    netmask = str(ipaddress.ip_network(networkprefix).netmask) # makes the netmask calculation using the variable network

    broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # -------------------------- --------------- -----------------------------
    dhcp_dir = os.listdir('/etc/dhcpcd.d/')
    for file in dhcp_dir:
        if file == interface + '.conf.disabled':
            os.rename('/etc/dhcpcd.d/' + interface + '.conf.disabled', '/etc/dhcpcd.d/' + interface + '.conf')

            # comment isc-dhcp-server 
            comment(interface,'/etc/default/isc-dhcp-server','INTERFACESv4=\"'+interface+'\"',False)

            # comment dhcpcd to disable
            commentary='include \"/etc/dhcpcd.d/'+interface+'.conf\";'
            comment(interface,'/etc/dhcpcd.conf',commentary,False)

     # Restart the dhcp server   
    for path in execute(['/etc/init.d/isc-dhcp-server','restart']):
        print(path, end='')

main(interface,network,prefix,gateway)
