#!/usr/bin/python
import sys
import os
import ipaddress
import socket
import fileinput
import subprocess
# Default variables (testing)
interface_default = 'eth0'
network_default = '192.168.1.0'+ '/' + '24'
gateway_default = '192.168.1.1'
Pool_Range_default = ['192.168.1.2','192.168.1.254']
DNS_Server_default = ['8.8.8.8',',9.9.9.9']
NTP_Server_default = '192.168.1.1'
lease_time_default = ['12','00','00']

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data)

# -------------------------- ip calculations -----------------------------
#netmask = str(ipaddress.ip_network(network).netmask) # makes the netmask calculation using the variable network

#broadcast = str(ipaddress.ip_network(network).broadcast_address)

#pool_network_size = len(list(ipaddress.ip_network(network).hosts()))-1 # makes the calculation using the variable network

#pool_range_size = (int(ipaddress.ipv4address(pool_range[1])) - int(ipaddress.ipv4address(pool_range[0])))+1 # makes the calculation using pool_range

#private= ipaddress.ip_network(network).is_private #check if the network is private

#range_valid = false if pool_range_size - pool_network_size > 0 else true #check if the range length is valid

#lease_time_secs = int(lease_time[0])*3600+int(lease_time[1])*60+int(lease_time[2])

# ------------------------------------------------------------------------
# ---------------------------------- main --------------------------------
# ------------------------------------------------------------------------
def main(interface=interface_default,network=network_default,gateway=gateway_default,Pool_Range=Pool_Range_default,DNS_Server=DNS_Server_default,NTP_Server=NTP_Server_default,lease_time=lease_time_default,Add_ARP=True):

    # transitive variable
    servers = ''

    # -------------------------- ip calculations -----------------------------
    netmask = str(ipaddress.ip_network(network).netmask) # makes the netmask calculation using the variable network

    broadcast = str(ipaddress.ip_network(network).broadcast_address)

    lease_time_secs = int(lease_time[0])*3600+int(lease_time[1])*60+int(lease_time[2])

    #------------------ writing on /etc/default/isc-dhcp-server -----------------------------
    data1 = 'interfacesv4=\"' + interface + '\"'
    isc_dhcp_server = '/etc/default/isc-dhcp-server'
    cow(isc_dhcp_server, data1)

    # -------------------------- writing on /etc/dhcpcp.conf-----------------------------
    data2 = 'include \"dhcpd.d/' + interface + '.conf\"'
    dhcpcd = '/etc/dhcpcd.conf'
    cow(dhcpcd, data2)

    #------------------ writing on /etc/network/interfaces.d/[interface] -----------------------------
    # There's a tricky thing in this code for the future you'll need to review it
    data3 = 'auto ' + interface
    data4 = 'iface ' + interface + ' inet ' + 'static'
    data5 = 'address ' + gateway
    data6 = 'netmask ' + broadcast
    data7 = [data3, data4, data5, data6]
    network_interface = '/etc/network/interfaces/interfaces.d/'
    dhcpd = open(network_interface + interface,'w+')
    dhcpd.writelines('\n'.join(data7))
    dhcpd.close()

    # ------------- writing on /etc/dhcpcp.conf/dhcpcd.d/ínterface.conf ----------
    dhcp_dir = os.listdir('/etc/dhcpcd.d/')
    for files in dhcp_dir:
        if files == interface + '.conf': # check if the file exist in the directory and erase it
            print('the file exists')
            os.remove('/etc/dhcpcd.d/'+ interface + '.conf')
        if files == interface + '.conf.disabled': # check if the file exist in the directory and erase it
            print('the file exists')
            os.remove('/etc/dhcpcd.d/'+ interface + '.conf.disabled')

    dhcpd = open('/etc/dhcpcd.d/'+ interface + '.conf','a')
    # writing the data into the configuration file
    dhcpd.writelines('#eth0 dhcp server configuration \n')
    l1 = 'subnet ' + network + ' ' + netmask + ' ' + '{'
    l2 = 'interface ' + interface + ';'
    if Add_ARP:
        l3 = 'authoritative;'
    else:
        l3 = '#authoritative;'
    l4 = 'range ' + Pool_Range[0] + ' ' + Pool_Range[1] + ';'
    l5 = 'option routers ' +  gateway + ';'
    l6 = 'option subnet-mask ' + netmask + ';'
    l7 = 'option broadcast-address ' +  broadcast + ';'
    l8 = 'option domain-name-servers ' + DNS_Server[0] + ' ' + DNS_Server[1] + ';'
    l9 = 'option ntp-server ' + NTP_Server + ';'
    l10 = 'max-lease-time ' + str(lease_time_secs) + ';'
    data = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,'}','']

    dhcpd.writelines('\n'.join(data))
    dhcpd.writelines('#end of eth0 dhcp server configuration')
    dhcpd.close()

# Restart the dhcp server (Not sure if i should enable it in this way)    
    subprocess.call('sudo systemctl restart isc-dhcp-server')

main()
