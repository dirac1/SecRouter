#!/usr/bin/python
import paramiko
import sys
import os
import ipaddress
import socket
import fileinput

# Variables to receive from GUI
Enable = True
Apply   = True
Interface = 'eth0'
Network = '192.168.1.0'+ '/' + '24'
Gateway = '192.168.1.1'
Pool_Range = ['192.168.1.2','192.168.1.254']
DNS_Server = ['8.8.8.8',',9.9.9.9']
NTP_Server = '192.168.1.1'
Lease_Time = ['12','00','00']
Add_ARP = True

# Transitive Variables
Servers = ''

# -------------------------- Check or Write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
# THE FUNCTION HAS A PROBLEM CLOSING THE FILE
def cow(file_dir,data):
    input_file = open(file_dir,'r')
    found = False
    while not found:
        for line in input_file:
            if data in line:
                found = True
                break
        else:
            input_file = open(file_dir,'a')
            input_file.write(data + '\n')
            input_file.close()
    input_file.close()

# -------------------------- IP calculations -----------------------------
Netmask = str(ipaddress.ip_network(Network).netmask) # makes the Netmask calculation using the variable Network

Broadcast = str(ipaddress.ip_network(Network).broadcast_address)

Pool_Network_Size = len(list(ipaddress.ip_network(Network).hosts()))-1 # makes the calculation using the variable Network

Pool_Range_Size = (int(ipaddress.IPv4Address(Pool_Range[1])) - int(ipaddress.IPv4Address(Pool_Range[0])))+1 # makes the calculation using Pool_Range

Private= ipaddress.ip_network(Network).is_private #check if the network is private

Range_Valid = False if Pool_Range_Size - Pool_Network_Size > 0 else True #Check if the range length is valid

Lease_Time_secs = int(Lease_Time[0])*3600+int(Lease_Time[1])*60+int(Lease_Time[2])

#------------------ Writing on /etc/default/isc-dhcp-server -----------------------------
data1 = 'INTERFACESv4=\"' + Interface + '\"\n'
isc_dhcp_server = '/home/dirac/SecRouter/isc-dhcp-server'
#cow(isc_dhcp_server, data1)

# -------------------------- Writing on /etc/dhcpcp.conf-----------------------------
data2 = 'include \"dhcpd.d/' + Interface + '.conf\"'
dhcpcd = '/home/dirac/SecRouter/dhcpcd.conf'
#cow(dhcpcd, data2)

#------------------ Writing on /etc/network/interface -----------------------------
data3 = 'iface ' + Interface + ' inet ' + 'static\n' + 'address ' + Gateway + '\n' + 'netmask' + Broadcast
network_interface = '/home/dirac/SecRouter/isc-dhcp-server'
#cow(network_interface, data3)

# ------------- Writing on /etc/dhcpcp.conf/dhcpcd.d/Ínterface.conf ----------
dhcp_dir = os.listdir('/home/dirac/SecRouter/etc/')
for files in dhcp_dir:
    if files == Interface + '.conf': # Check if the file exist in the directory and erase it
        print('The file exists')
        os.remove('/home/dirac/SecRouter/etc/'+ Interface + '.conf')
    if files == Interface + '.conf.disabled': # Check if the file exist in the directory and erase it
        print('The file exists')
        os.remove('/home/dirac/SecRouter/etc/'+ Interface + '.conf.disabled')

dhcpd = open('/home/dirac/SecRouter/etc/'+ Interface + '.conf','a')
# writing the data into the configuration file
dhcpd.writelines('#eth0 dhcp server configuration \n')
l1 = 'subnet ' + Network + ' ' + Netmask + ' ' + '{'
l2 = 'interface ' + Interface + ';'
if Add_ARP == True:
    l3 = 'authoritative;'
else:
    l3 = '#authoritative;'
l4 = 'range ' + Pool_Range[0] + ' ' + Pool_Range[1] + ';'
l5 = 'option routers ' +  Gateway + ';'
l6 = 'option subnet-mask ' + Netmask + ';'
l7 = 'option broadcast-address ' +  Broadcast + ';'
l8 = 'option domain-name-servers ' + DNS_Server[0] + ' ' + DNS_Server[1] + ';'
l9 = 'option ntp-server ' + NTP_Server + ';'
l10 = 'max-lease-time ' + str(Lease_Time_secs) + ';'
data = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,'}','']

dhcpd.writelines('\n'.join(data))
dhcpd.writelines('#end of eth0 dhcp server configuration')
dhcpd.close()
