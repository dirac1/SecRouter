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

# variables vlan
# --------------------------  check and replace  -----------------------------
# function to check if the file contain the value, if it is there the function will delete it
def cor(file_dir,data,replace):
    with fileinput.FileInput(file_dir,inplace=True) as file:
        for line in file:
            print(line.replace(data,replace),end=' ')

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will replace it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data+'\n')

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

