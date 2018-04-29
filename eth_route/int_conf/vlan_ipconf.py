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
vlan_raw_device = sys.argv[3]
vlan_id = sys.argv[4]
mtu = sys.argv[5]
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
def main(enable,conf_type,vlan_raw_device,vlan_id,mtu,network,prefix,ip,gw):
    file_dir = '/etc/network/vlan.d/'
    file_int = '/etc/network/vlan.d/'+'vlan'+vlan_id

    if network=='':
        print('manual/dhcp type')
    else:
        # -------------------------- ip calculations -----------------------------
        networkprefix = network+'/'+prefix
        netmask = str(ipaddress.ip_network(networkprefix).netmask)
        broadcast = str(ipaddress.ip_network(networkprefix).broadcast_address)

    # ----------- removing white lines -------------
    rwl('/etc/network/vlan.d/','vlan'+vlan_id)

    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the vlan 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + vlan_raw_device+'.'+vlan_id, \
                     'iface ' + vlan_raw_device+'.'+vlan_id + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down', \
                     'vlan-raw-device '+ vlan_raw_device, ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + vlan_raw_device+'.'+vlan_id, \
                     'iface ' + vlan_raw_device+'.'+vlan_id + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + vlan_raw_device+'.'+vlan_id, \
                     'iface ' + vlan_raw_device+'.'+vlan_id + ' inet dhcp' ]
            open(file_int, 'a').close()
            for value in data:
                cow(file_int,value)

        for path in execute(['ip','link','add','link',vlan_raw_device,'name',vlan_raw_device+'.'+vlan_id , 'type', 'vlan','id',vlan_id]):
            print(path,end=' ')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',vlan_raw_device+'.'+vlan_id,'down']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',vlan_raw_device+'.'+vlan_id,'up']):
            print(path, end='')

    else: # Disable the vlan 

        if conf_type=='1': # conf_type == manual 
           # --------------------------------------- 
            data = [ 'auto ' + vlan_raw_device+'.'+vlan_id, \
                     'iface ' + vlan_raw_device+'.'+vlan_id + ' inet manual', \
                     'pre-up ifconfig $IFACE up', \
                     'post-down ifconfig $IFACE down', \
                     'vlan-raw-device '+ vlan_raw_device, ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='2': # conf_type == static 
           # --------------------------------------- 
            data = [ 'auto ' + vlan_raw_device+'.'+vlan_id, \
                     'iface ' + vlan_raw_device+'.'+vlan_id + ' inet static', \
                     'address ' + ip, \
                     'netmask ' + netmask, \
                     'gateway ' + gw ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        if conf_type=='3': # conf_type == dhcp 
           # --------------------------------------- 
            data = [ 'auto ' + vlan_raw_device+'.'+vlan_id, \
                     'iface ' + vlan_raw_device+'.'+vlan_id + ' inet dhcp' ]
            open(file_int, 'a').close()
            for value in data:
                cor(file_int,value,'')

        for path in execute(['ip','link','delete',vlan_raw_device+'.'+vlan_id]):
            print(path,end=' ')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',vlan_raw_device,'down']):
            print(path, end='')
        for path in execute(['ip','link','set','dev',vlan_raw_device,'up']):
            print(path, end='')

main(enable,conf_type,vlan_raw_device,vlan_id,mtu,network,prefix,ip,gw)
