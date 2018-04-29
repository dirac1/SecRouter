#!/usr/bin/python
# coding=utf-8
# DISABLE Button for the DHCP Tab in the category DHCP SERVER
import os
import fileinput
import ipaddress
import subprocess
import sys
# variables
interface = sys.argv[1]
network = sys.argv[2]
prefix = sys.argv[3]
gateway= sys.argv[4]

# functions
from misc_rs import comment #check or write
from misc_rs import execute # execute a command 

# ----------------------------- main --------------------------
def main(interface,network,prefix,gateway):

    networkprefix = network +"/"+ prefix
    # -------------------------- ip calculations -----------------------------
    netmask = str(ipaddress.ip_network(networkprefix).netmask)

    broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # -------------------------- --------------- -----------------------------
    dhcp_dir = os.listdir('/etc/dhcpcd.d')
    for file in dhcp_dir:
        if file == interface + '.conf':
            os.rename('/etc/dhcpcd.d/' + interface + '.conf', '/etc/dhcpcd.d/' + interface + '.conf.disabled')

            # comment isc-dhcp-server 
            comment(interface,'/etc/default/isc-dhcp-server','INTERFACESv4=\"'+interface+'\"')

            # comment dhcpcd to disable
            comment(interface,'/etc/dhcpcd.conf','include \"/etc/dhcpcd.d/'+interface+'.conf'+'\";')

    # Restart the server to apply the changes
        for path in execute(['/etc/init.d/isc-dhcp-server','restart']):
            print(path, end='')

main(interface,network,prefix,gateway)
