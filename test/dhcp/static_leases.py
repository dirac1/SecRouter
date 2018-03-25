import os
import fileinput
import ipaddress
import subprocess
interface_default = 'eth0'
hostname_default = 'client'
ip_default = '192.168.1.1'
mac_default = 'FF:FF:FF:FF:FF:FF'

# -------------------------- check or write  -----------------------------
# function to check if the file contain the value, if it isn't there the function will write it  
def cow(file_dir,data):
     with open(file_dir,'r+') as input_file:
         lines = [line.strip().replace('\n','') for line in input_file.readlines()]
         if data not in lines:
            print("data not found")
            input_file.write(data)

# -------------------------- main -----------------------------

def main(interface=interface_default, hostname=hostname_default, ip=ip_default, mac=mac_default):
    checkfile = 'include \"dhcpd.d/static.leases.'+ interface
    cow('/home/dirac/SecRouter/dhcpcd.conf', checkfile)

    static_leases = open('/home/dirac/SecRouter/etc/static.leases.' + interface,'a')
    data = [ 'host ' + hostname + '{' \
             ,'hardware ethernet ' + mac + ';' \
             , 'fiex-address ' + ip + ';' \
             , '}\n' ]
    static_leases.writelines('\n'.join(data))

   # subprocess.call('/etc/init.d/isc-dhcp-server restart')

main()
