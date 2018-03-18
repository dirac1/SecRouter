import os
import fileinput
import ipaddress
import subprocess
interface_default='eth0'
network_default = '192.168.1.0'+ '/' + '24'
gateway_default = '192.168.1.1'

# -------------------------- comment function -----------------------------
def comment(interface,input_file,text,do=True,comment_glyph='#'):
    with fileinput.FileInput(input_file, inplace=True) as file:
        for line in file:
            if do:
                print(line.replace(text,comment_glyph + text), end='')
            else:
                print(line.replace(comment_glyph + text,text), end='')

# -------------------------- main -----------------------------
def main(interface=interface_default,network=network_default,gateway=gateway_default):

    # -------------------------- ip calculations -----------------------------
    netmask = str(ipaddress.ip_network(network).netmask) # makes the netmask calculation using the variable network

    broadcast = str(ipaddress.ip_network(network).broadcast_address)
    # -------------------------- --------------- -----------------------------

    dhcp_dir = os.listdir('/etc/dhcpcd.d/')
    for file in dhcp_dir:
        if file == interface + '.conf.disabled':
            os.rename('/etc/dhcpcd.d/' + interface + '.conf.disabled', '/etc/dhcpcd.d/' + interface + '.conf')
            # comment dhcpcd to disable
            commentary = ('include \"dhcpd.d/'+ interface + '.conf\"')
            comment(interface,'/etc/dhcpcd.conf',commentary,False)
            # comment isc-dhcp-server 
            comment(interface,'/etc/default/isc-dhcp-server','INTERFACESv4=\"'+interface+'\"',False)
            # comment interfaces.d/[interface] 
            data = [ 'auto ' + interface \
                     ,'iface ' + interface + ' inet' + ' static' \
                     , 'address ' + gateway \
                     , 'netmask ' + broadcast ]
            for value in data:
                comment(interface,'/etc/network/interfaces.d/'+interface,value,False)
        else:
            print('The configuration file doesn\'t exist')

    subprocess.call('/etc/init.d/isc-dhcp-server restart')

main()
