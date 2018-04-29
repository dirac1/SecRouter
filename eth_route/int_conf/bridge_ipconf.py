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
int_bridge = sys.argv[3]
stp_mode = sys.argv[4]
bridge_name = sys.argv[5]
network =  sys.argv[6]
prefix = sys.argv[7]
ip = sys.argv[8]
gw = sys.argv[9]

# functions
from misc_rs import cow # check or  write
from misc_rs import cor # check or replace
from misc_rs import comment #check or write
from misc_rs import execute # execute a command 
from misc_rs import rwl # remove white lines

# ---------------------------------- main --------------------------------
def main(enable,conf_type,int_bridge,stp_mode,bridge_name,network,prefix,ip,gw):

    if network=='':
        print('manual/dhcp type')
    else:
        # -------------------------- ip calculations -----------------------------
        networkprefix = network+'/'+prefix
        netmask = str(ipaddress.ip_network(networkprefix).netmask)
        broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    file_dir = '/etc/network/bridge.d/'
    file_int = '/etc/network/bridge.d/'+bridge_name

    # ----------- removing white lines -------------
    rwl('/etc/network/bridge.d/',bridge_name)

    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the bridge 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + bridge_name, \
                     'iface ' + bridge_name + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down', \
                    'bridge_ports '+ int_bridge, \
                    'bridge_stp ' + stp_mode ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)
        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + bridge_name, \
                     'iface ' + bridge_name + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw, \
                     'bridge_ports '+ int_bridge, \
                     'bridge_stp ' + stp_mode ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + bridge_name, \
                     'iface ' + bridge_name + ' inet dhcp', \
                     'bridge_ports '+ int_bridge, \
                     'bridge_stp ' + stp_mode ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        for path in execute(['ip','link','add','name',bridge_name, 'type', 'bridge']):
            print(path,end=' ')
        for path in execute(['ip','link','set',int_bridge, 'master',bridge_name]):
            print(path,end=' ')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',bridge_name,'down']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',bridge_name,'up']):
            print(path, end='')

    else: # Disable the bridge 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + bridge_name, \
                     'iface ' + bridge_name + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down', \
                     'bridge_ports '+ int_bridge, \
                     'bridge_stp ' + stp_mode ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')
        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + bridge_name, \
                     'iface ' + bridge_name + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw, \
                     'bridge_ports '+ int_bridge, \
                     'bridge_stp ' + stp_mode ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + bridge_name, \
                     'iface ' + bridge_name + ' inet dhcp', \
                     'bridge_ports '+ int_bridge, \
                     'bridge_stp ' + stp_mode ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        for path in execute(['ip','link','delete',bridge_name,'type','bridge']):
            print(path,end=' ')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        for interface in int_bridge.split(' '):
            for path in execute(['ip','link','set','dev',interface,'down']):
                print(path, end='')
            for path in execute(['ip','link','set','dev',interface,'up']):
                print(path, end='')

main(enable,conf_type,int_bridge,stp_mode,bridge_name,network,prefix,ip,gw)
