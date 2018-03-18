#!/usr/bin/python
# APPLY BUTTON for DHCP tab in the category DHCP Client
import os
import subprocess
import fileinput
interface_default = 'eth1'
# You have a check button to activate the dhcp client
# Renew and Release buttons will be separated 

# All the data from the lease is in /var/lib/dhcp/dhclient.lease
# /etc/network/interface 
#    auto [interface]
#    iface [interface] inet dhcp
# delete dhclient.leases to forget the lease

