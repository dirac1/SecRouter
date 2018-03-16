import os
import fileinput
interface_default='eth0'

def main(interface=interface_default):
    dhcp_dir = os.listdir('/home/dirac/SecRouter/etc/')
    for file in dhcp_dir:
        if file == interface + '.conf.disabled':
            os.rename('/home/dirac/SecRouter/etc/' + interface + '.conf.disabled', '/home/dirac/SecRouter/etc/' + Interface + '.conf')
            look = ('include \"dhcpd.d/'+ interface + '.conf\"')
            commented = ('#include \"dhcpd.d/'+ interface + '.conf\"')
            with fileinput.FileInput('/home/dirac/SecRouter/dhcpd.conf', inplace=True) as file:
                for line in file:
                    print(line.replace(commented,look), end='')
        else:
            print('The configuration file doesn\'t exist')

main()
