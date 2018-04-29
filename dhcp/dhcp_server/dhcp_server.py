#!/usr/bin/python
# coding=utf-8

import sys
import os
import ipaddress
import socket
import fileinput
import subprocess

# variables 
interface= sys.argv[1]
network= sys.argv[2]
prefix = sys.argv[3]
gateway= sys.argv[4]
Pool_Range_Start = sys.argv[5]
Pool_Range_Stop = sys.argv[6]
DNS_Server_1 = sys.argv[7]
DNS_Server_2 = sys.argv[8]
lease_time= sys.argv[9]
Add_ARP = sys.argv[10]

# functions
from misc_rs import cow # check or  write
from misc_rs import execute # execute a command 

# ---------------------------------- main --------------------------------
def main(interface,network,prefix,gateway,Pool_Range_Start,Pool_Range_Stop,DNS_Server_1,DNS_Server_2,lease_time,Add_ARP):

    # transitive variable
    Pool_Range=[]
    Pool_Range.append(Pool_Range_Start)
    Pool_Range.append(Pool_Range_Stop)
    DNS_Server = []
    DNS_Server.append(DNS_Server_1)
    DNS_Server.append(DNS_Server_2)
    networkprefix = network + '/' + prefix

    # -------------------------- ip calculations -----------------------------
    netmask = str(ipaddress.ip_network(networkprefix).netmask)

    broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    #------------------ writing on /etc/default/isc-dhcp-server -------------------------
    cow('/etc/default/isc-dhcp-server' , 'INTERFACESv4=\"' + interface + '\"' )

    # -------------------------- writing on /etc/dhcpcp.conf-----------------------------
    cow( '/etc/dhcpcd.conf' , 'include \"/etc/dhcpcd.d/' + interface + '.conf\"' + ';' )

    # ------------- checking and overwriting /etc/dhcpcd.d/ínterface.conf ----------
    dhcp_dir = os.listdir('/etc/dhcpcd.d/')
    for files in dhcp_dir:
        if files == interface + '.conf': # check if the file exist in the directory and erase it
            print('/etc/dhcpcp.d/'+ interface+'.conf exists')
            os.remove('/etc/dhcpcd.d/'+ interface + '.conf')
        if files == interface + '.conf.disabled': # check if the file exist in the directory and erase it
            print('/etc/dhcpcp.d/'+ interface +'.conf.disabled exists')
            os.remove('/etc/dhcpcd.d/'+ interface + '.conf.disabled')

    static_lease_dir = os.listdir('/etc/dhcpcd.d/')
    for files in static_lease_dir:
        if files == 'static.leases.'+ interface:
            os.remove('/etc/dhcpcd.d/static.leases.'+ interface)

    # ------------- writing the configuration file ------------- 
    dhcpd = open('/etc/dhcpcd.d/'+ interface + '.conf','a')
    conf = [ 'subnet ' + network + ' netmask ' + netmask + ' ' + '{', \
             'interface ' + interface + ';', \
             'authoritative;', \
             'range ' + Pool_Range[0] + ' ' + Pool_Range[1] + ';', \
             'option routers ' +  gateway + ';', \
             'option subnet-mask ' + netmask + ';', \
             'option broadcast-address ' +  broadcast + ';', \
             'option domain-name-servers ' + DNS_Server[0] + ',' + DNS_Server[1] + ';', \
             'max-lease-time ' + str(lease_time) + ';', \
             '} ' ]

    if Add_ARP==False:
        conf.pop(2)
        conf.insert(2,'#authoritative;')

    dhcpd.writelines('\n'.join(conf))
    dhcpd.close()

    # Restart the dhcp server to apply the changes     
    for path in execute(["systemctl","restart","isc-dhcp-server"]):
        print(path , end = '')

main(interface, network, prefix, gateway, Pool_Range_Start, Pool_Range_Stop, DNS_Server_1, DNS_Server_2, lease_time, Add_ARP)
