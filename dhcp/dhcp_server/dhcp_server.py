#!/usr/bin/python
# coding=utf-8
# APPLY BUTTOn for the DHCP tab in the category DHCP SERVER
import sys
import os
import ipaddress
import socket
import fileinput
import subprocess

# Default variables (testing)
#interface_default = 'eth0'
#network_default = '192.168.1.0'+ '/' + '24'
#gateway_default = '192.168.1.1'
#Pool_Range_default = ['192.168.1.2','192.168.1.254']
#DNS_Server_default = ['8.8.8.8',',9.9.9.9']
#NTP_Server_default = '192.168.1.1'
#lease_time_default = '120000'

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data)

# ----------- execute command and print the stout or stderr  ---------------
def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)

# ---------------------------------- main --------------------------------
def main(interface,network,gateway,Pool_Range_Start,Pool_Range_Stop,DNS_Server_1,DNS_Server_2,NTP_Server,lease_time,Add_ARP):

    # transitive variable
    servers = ''
    Pool_Range=[]
    Pool_Range.append(Pool_Range_Start)
    Pool_Range.append(Pool_Range_Stop)
    DNS_Server = []
    DNS_Server.append(DNS_Server_1)
    DNS_Server.append(DNS_Server_2)

    # -------------------------- ip calculations -----------------------------
    netmask = str(ipaddress.ip_network(network).netmask) # makes the netmask calculation using the variable network

    broadcast = str(ipaddress.ip_network(network).broadcast_address)

    #------------------ writing on /etc/default/isc-dhcp-server -----------------------------
    data1 = 'interfacesv4=\"' + interface + '\"'
    isc_dhcp_server = '/etc/default/isc-dhcp-server'
    cow(isc_dhcp_server, data1)

    # -------------------------- writing on /etc/dhcpcp.conf-----------------------------
    data2 = 'include \"dhcpd.d/' + interface + '.conf\"'
    dhcpcd = '/etc/dhcpcd.conf'
    cow(dhcpcd, data2)

    #------------------ writing on /etc/network/interfaces.d/[interface] -----------------------
    # There's a tricky thing in this code for the future you'll need to review it
    data3 = 'auto ' + interface
    data4 = 'iface ' + interface + ' inet ' + 'static'
    data5 = 'address ' + gateway
    data6 = 'netmask ' + broadcast
    data7 = [data3, data4, data5, data6]
    network_interface = '/etc/network/interfaces.d/'
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

    static_lease_dir = os.listdir('/etc/dhcpcd.d/')
    for files in static_lease_dir:
        if files == 'static.leases.'+ interface:
            os.remove('/etc/dhcpcd.d/static.leases.'+ interface)

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
    l10 = 'max-lease-time ' + str(lease_time) + ';'
    data = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10,'}','']

    dhcpd.writelines('\n'.join(data))
    dhcpd.writelines('#end of eth0 dhcp server configuration')
    dhcpd.close()

    # Restart the dhcp server to apply the changes     
#    for path in execute(["sudo systemctl restart isc-dhcp-server"]):
#        print(path,end="")

main()
