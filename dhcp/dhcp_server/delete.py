#!/usr/bin/python
# Simple script to remove all data related to an interface in the dhcp_configuration

import fileinput
import os
import sys
import subprocess

interface = sys.argv[1]

# --------------------------  check and replace  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it
def cor(file_dir,data,replace):
    with fileinput.FileInput(file_dir,inplace=True) as file:
        for line in file:
            print(line.replace(data,replace),end=' ')
# ------------------------------------------------------------------------
def main(interface):
    cor( '/etc/default/isc-dhcp-server', 'INTERFACESv4=\"' + interface + '\"', ' ' )
    cor( '/etc/dhcpcd.conf' , 'include \"/etc/dhcpcd.d/' + interface + '.conf\"' + ';' , ' ' )
    cor( '/etc/network/interfaces' , 'source /etc/network/interfaces.d/' + interface, ' ' )

    os.remove('/etc/network/interfaces.d/'+interface)
    dhcp_dir = os.listdir('/etc/dhcpcd.d/')
    for files in dhcp_dir:
        if files == interface + '.conf': # check if the file exist in the directory and erase it
            print('/etc/dhcpcp.d/'+ interface+'.conf exists')
            os.remove('/etc/dhcpcd.d/'+ interface + '.conf')
        if files == interface + '.conf.disabled': # check if the file exist in the directory and erase it
            print('/etc/dhcpcp.d/'+ interface +'.conf.disabled exists')
            os.remove('/etc/dhcpcd.d/'+ interface + '.conf.disabled')

# ------------------------------------------------------------------------

main(interface)
