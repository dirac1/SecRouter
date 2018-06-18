import ipaddress
import socket

Disable = True
Interface = 'eth0'
Network = '192.168.1.0'+ '/' + '24'
Gateway = '192.168.1.1'
Pool_Range = ['192.168.1.2','192.168.1.254']
DNS_Server = ['8.8.8.8',',9.9.9.9']
NTP_Server = '192.168.1.1'
Lease_Time = ['12','00','00']
Add_ARP = False


# IP calculations 
Netmask = str(ipaddress.ip_network(Network).netmask) # makes the Netmask calculation using the variable Network

Broadcast = str(ipaddress.ip_network(Network).broadcast_address)

Pool_Network_Size = len(list(ipaddress.ip_network(Network).hosts()))-1 # makes the calculation using the variable Network

Pool_Range_Size = (int(ipaddress.IPv4Address(Pool_Range[1])) - int(ipaddress.IPv4Address(Pool_Range[0])))+1 # makes the calculation using Pool_Range

Private= ipaddress.ip_network(Network).is_private #check if the network is private

Range_Valid = False if Pool_Range_Size - Pool_Network_Size > 0 else True #Check if the range length is valid

Lease_Time_secs = int(Lease_Time[0])*3600+int(Lease_Time[1])*60+int(Lease_Time[2])

