import os
import fileinput
import ipaddress
import subprocess
hostname_default = 'client'
ip_default = '192.168.1.1'
mac_default = 'FF:FF:FF:FF:FF:FF'
# -------------------------- comment function -----------------------------
def comment(interface,input_file,text,do=True,comment_glyph='#'):
    with fileinput.FileInput(input_file, inplace=True) as file:
        for line in file:
            if do:
                print(line.replace(text,comment_glyph + text), end='')
            else:
                print(line.replace(comment_glyph + text,text), end='')
# First
# to generate a static lease you'll need to add the next statement to The new file static.leases
    #host [hostname] {
    #hardware ethernet [mac];
    #fixed-address [ip];
                #}
# -------------------------- main -----------------------------
def main(hostname=hostname_default, ip=ip_default, mac=mac_default):

    dhcpcd = open('/etc/dhcpcd.d/static.leases','a')
    data = [ 'host ' + hostname + '{' \
             ,'hardware ethernet ' + mac \
             , 'fiex-address ' + ip \
             , '}' ]
    for value in data:
        dhcpcd.writelines('\n'.join(data))
    subprocess.call('/etc/init.d/isc-dhcp-server restart')

main()
