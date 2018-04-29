#!/usr/bin/python
# coding=utf-8

import sys
import os
import ipaddress
import fileinput
import subprocess

# variables 
enable = sys.argv[1]
conf_type = sys.argv[2]
interface = sys.argv[3]
dst_network =  sys.argv[4]
prefix = sys.argv[5]
gw = sys.argv[6]

# functions
from misc_rs import cow # check or  write
from misc_rs import cor # check or replace
from misc_rs import comment #check or write
from misc_rs import execute # execute a command 
from misc_rs import rwl # remove white lines

# ---------------------------------- main --------------------------------
def main(enable,conf_type,interface,dst_network,prefix,gw):
    print(" ### Starting configuration ### ")
    # -------------------------- ip calculations -----------------------------
    networkprefix = dst_network+'/'+prefix
    netmask = str(ipaddress.ip_network(networkprefix).netmask)
    broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # ip route add [dst_network]+/+[prefix] via [gw] dev [interface]

    # ----------- remove white lines -------------
    rwl('/etc/network/interfaces.d/',interface)
    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the route 
        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_int = '/etc/network/interfaces.d/'+interface
           # data = [ 'up route add -net '+ dst_network +' netmask ' + netmask +' gw ' + gw, \
           #          'down route del -net ' +  dst_network +' netmask '+ netmask + ' gw ' + gw ]
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_int = '/etc/network/vlan.d/'+interface
           # data = [ 'up route add -net '+ dst_network +' netmask ' + netmask +' gw ' + gw, \
           #          'down route del -net ' +  dst_network +' netmask '+ netmask + ' gw ' + gw ]
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_int = '/etc/network/bridge.d/'+interface
           # data = [ 'up route add -net '+ dst_network +' netmask ' + netmask +' gw ' + gw, \
           #          'down route del -net ' +  dst_network +' netmask '+ netmask + ' gw ' + gw ]
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        print(" ### Actual configuration ### ")
        for path in execute(['ip','route','add',dst_network+'/'+prefix,'via',gw,'dev',interface]):
            print(path, end='')
        for path in execute(['ifquery','-a']):
            print(path, end='')

    else: # Disable the route 

        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_int = '/etc/network/interfaces.d/'+interface
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_int = '/etc/network/vlan.d/'+interface
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_int = '/etc/network/bridge.d/'+interface
            data = [ 'post-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface, \
                     'pre-up ip route add '+ dst_network+'/'+prefix+ ' via ' + gw +' dev ' + interface ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        print(" ### Actual configuration ### ")
        for path in execute(['ip','route','delete',dst_network+'/'+prefix]):
            print(path, end='')
        for path in execute(['ifquery','-a']):
            print(path, end='')

main(enable,conf_type,interface,dst_network,prefix,gw)
