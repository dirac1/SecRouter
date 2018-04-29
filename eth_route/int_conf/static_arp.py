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
ip =  sys.argv[4]
mac = sys.argv[5]

# functions
from misc_rs import cow # check or  write
from misc_rs import cor # check or replace
from misc_rs import comment #check or write
from misc_rs import execute # execute a command 
from misc_rs import rwl # remove white lines

# ---------------------------------- main --------------------------------
def main(enable,conf_type,interface,ip,mac):
    print(" ### Starting configuration ### ")
    # ----------- remove white lines -------------
    rwl('/etc/network/arp.d/','ether.'+interface)
    # ------------------------- configuration --------------------------------
    if enable=='1': # Enable the route 

        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/interfaces.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cow(file_int,data_int)
            cow(file_arp,data_arp)

            for path in execute(['arp','-f',file_arp]):
                print(path, end='')

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/vlan.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cow(file_int,data_int)
            cow(file_arp,data_arp)

            for path in execute(['arp','-f',file_arp]):
                print(path, end='')


        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/bridge.d/'+interface
            data_arp = mac + ' ' + ip
            data_int = 'post-up arp -f '+ file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cow(file_int,data_int)
            cow(file_arp,data_arp)

            for path in execute(['arp','-f',file_arp]):
                print(path, end='')

        print(" ### Actual configuration ### ")
        for path in execute(['ifquery','-a']):
            print(path, end='')

    else: # Disable the route 

        if conf_type=='1': # conf_type == phy 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/interfaces.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cor(file_int,data_int,'')
            cor(file_arp,data_arp,'')

            for path in execute(['ip','neigh','del',ip,'dev',interface]):
                print(path, end='')

        if conf_type=='2': # conf_type == vlan 
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/vlan.d/'+interface
            data_arp = mac+' '+ip
            data_int = 'post-up arp -f '+file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cor(file_int,data_int,'')
            cor(file_arp,data_arp,'')

            for path in execute(['ip','neigh','del',ip,'dev',interface]):
                print(path, end='')

        if conf_type=='3': # conf_type == bridge
           # --------------------------------------- 
            file_arp = '/etc/network/arp.d/ether.'+interface
            file_int = '/etc/network/bridge.d/'+interface
            data_arp = mac + ' ' + ip
            data_int = 'post-up arp -f '+ file_arp

            open(file_int, 'a').close()
            open(file_arp, 'a').close()
            cor(file_int,data_int,'')
            cor(file_arp,data_arp,'')

            for path in execute(['ip','neigh','del',ip,'dev',interface]):
                print(path, end='')

        print(" ### Actual configuration ### ")
        for path in execute(['ifquery','-a']):
            print(path, end='')



main(enable,conf_type,interface,ip,mac)
