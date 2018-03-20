#!/usr/bin/python
# Simple script to remove all data related to an interface in the dhcp_configuration

import fileinput
import os
import sys
import subprocess

interface = sys.argv[1]

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data in lines:
            print("data found")
            input_file.write('')
# ------------------------------------------------------------------------
def main(interface):

    cow( '/etc/default/isc-dhcp-server', 'INTERFACESv4=\"' + interface + '\"' )
    cow( '/etc/dhcpcd.conf' , 'include \"/etc/dhcpcd.d/' + interface + '.conf\"' + ';' )
    cow( '/etc/network/interfaces' , 'source /etc/network/interfaces.d/' + interface )

    os.remove('/etc/network/interfaces.d/'+interface)
    os.remove('/etc/dhcpcd.d/'+interface+'.conf')
# ------------------------------------------------------------------------

main(interface)
