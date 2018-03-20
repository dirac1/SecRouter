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

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data)

# ----------- execute command and print the stout or stderr  -------------
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# ---------------------------------- main --------------------------------
def main(interface,network,prefix,gateway,Pool_Range_Start,Pool_Range_Stop,DNS_Server_1,DNS_Server_2,NTP_Server,lease_time,Add_ARP):

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
    cow( '/etc/default/isc-dhcp-server' , 'INTERFACESv4=\"' + interface + '\"' )

    # -------------------------- writing on /etc/dhcpcp.conf-----------------------------
    cow( '/etc/dhcpcd.conf' , 'include \"/etc/dhcpcd.d/' + interface + '.conf\"' + ';' )

    # -------------------------- writing on /etc/dhcpcp.conf-----------------------------
    cow( '/etc/network/interfaces' , 'source /etc/network/interfaces.d/' + interface )

    #------------------ writing on /etc/network/interfaces.d/[interface] ----------------
    # There's a tricky thing in this code for the future you'll need to review it
    data = [ 'auto ' + interface, \
             '    iface ' + interface + ' inet ' + 'static', \
             '    address ' + gateway, \
             '    netmask ' + netmask ]
    network_interface = '/etc/network/interfaces.d/' + interface
    dhcpd = open( network_interface , 'w+' )
    dhcpd.writelines('\n'.join(data))
    dhcpd.close()

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
             '', \
             'range ' + Pool_Range[0] + ' ' + Pool_Range[1] + ';', \
             'option routers ' +  gateway + ';', \
             'option subnet-mask ' + netmask + ';', \
             'option broadcast-address ' +  broadcast + ';', \
             'option domain-name-servers ' + DNS_Server[0] + ',' + DNS_Server[1] + ';', \
             'max-lease-time ' + str(lease_time) + ';', \
             '} ' ]

    if Add_ARP:
        data.insert(3,'authoritative;')
    else:
        data.insert(3,'#authoritative;')

    dhcpd.writelines('\n'.join(conf))
    dhcpd.close()

    # Restart the dhcp server to apply the changes     
    for path in execute(["systemctl","restart","isc-dhcp-server"]):
        print(path , end = '')

main(interface, network, prefix, gateway, Pool_Range_Start, Pool_Range_Stop, DNS_Server_1, DNS_Server_2, lease_time, Add_ARP)
