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
network =  sys.argv[4]
prefix = sys.argv[5]
ip = sys.argv[6]
gw = sys.argv[7]

# functions
from misc_rs import cow # check or  write
from misc_rs import cor # check or replace
from misc_rs import comment #check or write
from misc_rs import execute # execute a command 
from misc_rs import rwl # remove white lines

# ---------------------------------- main --------------------------------
def main(enable,conf_type,interface,network,prefix,ip,gw):
    file_dir = '/etc/network/interfaces.d/'
    file_int = '/etc/network/interfaces.d/'+interface

    if network=='':
        print('manual/dhcp type')
    else:
        # -------------------------- ip calculations -----------------------------
        networkprefix = network+'/'+prefix
        netmask = str(ipaddress.ip_network(networkprefix).netmask)
        broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # ----------- removing white lines -------------
    rwl( '/etc/network/interfaces.d/' , interface )

    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the interface 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down' ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet dhcp', ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        for path in execute(['ifquery','-a']):
            print(path, end='')
        #for path in execute(['systemctl','restart','networking']):
        #    print(path, end='')
        for path in execute(['ip','link','set','dev',interface,'down']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',interface,'up']):
            print(path, end='')
    else: # Disable the interface 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down' ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'iface ' + interface + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + interface, \
                     'allow-hotplug ' + interface, \
                     'iface ' + interface + ' inet dhcp', ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        #for path in execute(['systemctl','restart','networking']):
        #    print(path, end='')

main(enable,conf_type,interface,network,prefix,ip,gw)
