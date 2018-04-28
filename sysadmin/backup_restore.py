#!/usr/bin/python
# coding=utf-8

import sys
import os
import ipaddress
import fileinput
import subprocess
import shutil

# variables 
bor = sys.argv[1]
filename = sys.argv[2]

# --------------------------  check and replace  -----------------------------
# function to check if the file contain the value, if it is there the function will delete it
def cor(file_int,data,replace):
    with fileinput.FileInput(file_int,inplace=True) as file:
        for line in file:
            print(line.replace(data,replace),end=' ')

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will replace it  
def cow(file_int,data):
     with open(file_int,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
             print("cow: data not found")
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

# ----------- remove white lines -------------
def rwl(directory,filename):
    file_to_clean = directory+filename
    for files in os.listdir(directory):
        if files == filename:
            with open(file_to_clean) as infile, open('output', 'w') as outfile:
                for line in infile:
                    if not line.strip(): continue  # skip the empty line
                    outfile.write(line)  # non-empty line. Write it to output
            os.remove(file_to_clean)
            os.rename('output',file_to_clean)
        else:
            print('rwl: The file does not exist')

# ---------------------------------- main --------------------------------
def main(bor,filename):
# BACKUP 
    secrouter_backup_dir = '/home/secrouter/backup' # backup root directory
    backup_dir = '/home/secrouter/backup/'+filename # backup directory
    backup_dir_dhcp = backup_dir+'/dhcp' # dhcp directory
    backup_dir_ethroute = backup_dir+'/ethroute' # ethernet and routing directory
    if bor == '0':
        # 1. create the file name directory with the hierarchy
        os.mkdir(backup_dir)

        # dhcp directory creation
        os.mkdir(backup_dir_dhcp)
        os.mkdir(backup_dir_dhcp+'/dhcpcd.d')

        # ethernet and routing directory
        os.mkdir(backup_dir_ethroute)
        os.mkdir(backup_dir_ethroute+'/interfaces.d')
        os.mkdir(backup_dir_ethroute+'/vlan.d')
        os.mkdir(backup_dir_ethroute+'/bridge.d')
        os.mkdir(backup_dir_ethroute+'/arp.d')

        # 2. Copy all the configurations files inside the file name directory.  
        # DHCP
        if os.path.isfile('/etc/dhcpcd.conf'):
            shutil.copy2('/etc/dhcpcd.conf',backup_dir_dhcp)
        if os.path.isfile('/etc/default/isc-dhcp-server'):
            shutil.copy2('/etc/default/isc-dhcp-server',backup_dir_dhcp)

        dhcpcd_d = os.listdir('/etc/dhcpcd.d')
        if dhcpcd_d != []:
            for value in dhcpcd_d:
                if os.path.isfile( dhcpcd_d + value ):
                    shutil.copy2(dhcpcd_d + value , backup_dir_dhcp+'/dhcpcd.d' )

        # Ethernet & Routing
        if os.path.isfile( '/etc/network/secrouter.conf' ):
            shutil.copy2('/etc/network/secrouter.conf' , backup_dir_ethroute)
        if os.path.isfile( '/etc/bind/named.conf.options' ):
            shutil.copy2('/etc/bind/named.conf.options' , backup_dir_ethroute)

        eth_multi_files = ['/interfaces.d', \
                           '/vlan.d', \
                           '/bridge.d', \
                           '/arp.d' ]
        for files in eth_multi_files:
            this = os.listdir('/etc/network' + files)
            if this != []:
                for value in this:
                    shutil.copy2('/etc/network' + files + '/' + value , backup_dir_ethroute + files )

        # Firewall
        if os.path.isfile('/etc/iptables.rules'):
            shutil.copy2('/etc/iptables.rules' , backup_dir)

        # Compressing ../backup/filename
        backup = secrouter_backup_dir + '/' + filename + '.tar.gz'
        for path in execute(['tar','-czvf',backup,'-C',secrouter_backup_dir,filename]):
            print(path, end='')

        # Erasing transitive directory
        shutil.rmtree('/home/secrouter/backup/'+ filename)

# RESTORE
    else:
    # 1. Descompress the backup file from the backup directory
        backup_compressed = secrouter_backup_dir + '/' + filename + '.tar.gz'
        for path in execute(['tar','-xzvf',backup_compressed,'-C','/home/secrouter/backup']):
            print(path, end='')

    # 2. delete old configuration files
        if os.path.isfile('/etc/dhcpcd.conf'):
            os.remove('/etc/dhcpcd.conf')
        if os.path.isfile('/etc/default/isc-dhcp-server'):
            os.remove('/etc/default/isc-dhcp-server')

        dhcpcd_d = os.listdir('/etc/dhcpcd.d')
        if dhcpcd_d != []:
            for value in dhcpcd_d:
                os.remove(dhcpcd_d+ '/' + files )

        if os.path.isfile( '/etc/network/secrouter.conf' ):
            os.remove('/etc/network/secrouter.conf')
        if os.path.isfile( '/etc/bind/named.conf.options' ):
            os.remove('/etc/bind/named.conf.options')

        eth_multi_files = ['/interfaces.d', \
                           '/vlan.d', \
                           '/bridge.d', \
                           '/arp.d' ]
        for files in eth_multi_files:
            this = os.listdir('/etc/network' + files)
            if this != []:
                for value in this:
                    os.remove('/etc/network' + files + '/' + value)

        if os.path.isfile('/etc/iptables.rules'):
            os.remove('/etc/iptables.rules')
        print('--- *** ---')
        print('--- Deleted old configuration files ---')

    # 3. Copy the backup files from the filename to the system
        shutil.copy2('/home/secrouter/backup/'+filename+'/dhcp/dhcpcd.conf', '/etc')
        shutil.copy2('/home/secrouter/backup/'+filename+'/dhcp/isc-dhcp-server','/etc/default')

        dhcpcd_d = os.listdir('/home/secrouter/backup/'+filename+'/dhcp/dhcpcd.d')
        for value in dhcpcd_d:
            if os.path.isfile( dhcpcd_d + value ):
                shutil.copy2(dhcpcd_d + value , '/etc/dhcpcd.d' )

        # Ethernet & Routing
        shutil.copy2('/home/secrouter/backup/'+filename+'/ethroute/secrouter.conf' , '/etc/network')
        shutil.copy2('/home/secrouter/backup/'+filename+'/ethroute/named.conf.options','/etc/bind')

        eth_multi_files = ['/interfaces.d', \
                           '/vlan.d', \
                           '/bridge.d', \
                           '/arp.d' ]
        for files in eth_multi_files:
            this = os.listdir( '/home/secrouter/backup/'+filename+'/ethroute/'+ files)
            if this != []:
                for value in this:
                    shutil.copy2( '/home/secrouter/backup/'+filename+'/ethroute/'+ files + '/' + value , '/etc/network' + files )

    # Firewall
        shutil.copy2('/home/secrouter/backup/'+filename+'/iptables.rules' , '/etc')
        print('--- *** ---')
        print('--- copied new configuration files ---')

# 4. delete the uncompressed files from the backup directory
        shutil.rmtree('/home/secrouter/backup/'+ filename)

    # 5. Restart The services 

        # Restart Networking
        for path in execute(['systemctl','restart','networking']):
            print(path, end='')
        print('-----------------------------------')
        print('NEW ETHERNET & ROUTING CONFIGURATION:')
        for path in execute(['ifquery','-a']):
            print(path, end='')
        print('-----------------------------------')

        # Restart Firewall
        iptables_rules = open('/etc/iptables.rules', 'w')
        p = subprocess.Popen(["iptables-restore"], stdout=iptables_rules)
        iptables_rules.close()
        print('-----------------------------------')
        print('NEW FILTER RULES:')
        for path in execute(["iptables",'-v','-L','-t', 'filter']):
            print(path, end="")
        print('-----------------------------------')
        print('NEW NAT RULES:')
        for path in execute(["iptables",'-v','-L','-t', 'nat']):
            print(path, end="")
        print('-----------------------------------')
        print('RESTARTING THE SYSTEM TO APPLY CHANGES')

        # Restart DHCP
        print('-----------------------------------')
        print('RESTARTING DHCP SERVER:')
        for path in execute(["systemctl","restart","isc-dhcp-server"]):
            print(path , end = '')
        print('-----------------------------------')


#        for path in execute(['reboot']):
#            print(path, end="")

main(bor,filename)

