#!/bin/bash
# You must run this script as root
# Script to start SecRouter in a Debian-like distribution
# !! Designed for Raspbian !!

# --- Package installation and admin configuration ---
printf "Creating the router user controller: secrouter\nthe default password is: routersec\n==========\nadding the group: network\n"
groupadd network
useradd -m -s /bin/bash -c "router controller" -u 1337 -g network secrouter
echo -e "routersec\nroutersec" | passwd secrouter
printf "adding secrouter to sudoers\n"
echo -e 'secrouter  ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers

# --- Adding network scripts ---
#printf "Adding network scripts to secrouter home folder"
#cp -r /root/secrouter/* /home/secrouter

# --- Package installation and admin configuration ---
printf "Updating, Upgrading and Downloading basic packages\n==========\n"
apt-get update && apt-get upgrade -y
apt-get install wget curl git zip zsh vim tmux sudo htop iftop ipcalc ipython iw lm-sensors logrotate ncdu ntp vlan  -y
apt-get install build-essential libssl-dev libffi-dev python-dev -y

# Networking packages
printf "Downloading network packages\n=========="
apt-get install isc-dhcp-server isc-dhcp-client dnsutils bridge-utils vlan bind9 iptables traceroute ifupdown2 hostapd whois ntp -y

# --- Ethernet & Routing ---
printf "Creating Files for Ethernet & Routing Module\n==========\n"
touch /etc/network/secrouter.conf
mkdir -v /etc/network/interfaces.d
mkdir -v /etc/network/vlan.d
mkdir -v /etc/network/bridge.d
mkdir -v /etc/network/arp.d
printf "source /etc/network/interfaces.d/*\nsource /etc/network/vlan.d/*\nsource /etc/network/bridge.d/*" > /etc/network/secrouter.conf
cp /etc/network/interfaces /etc/network/interfaces.bak
touch /etc/network/interfaces.d/eth0
printf "auto eth0\n    iface eth0 inet dhcp" > /etc/network/interfaces.d/eth0
printf "auto lo\n    iface lo inter loopback" > /etc/network/interfaces
printf "source /etc/network/secrouter.conf\n" >> /etc/network/interfaces
ifquery -a

# ---Firewall ---
printf "Configuring Firewall Module\n==========\n"
printf "net.ipv4.ip_forward = 1" > /etc/sysctl.conf
sysctl -p /etc/sysctl.conf

# xtables-addons Installation 
printf "Configuring RPI kernel to add xtables-addons modules for the Firewall Module"
printf "=========="
apt-get install rpi-update
rpi-update 
gcc --version | grep gcc
apt-get install gcc-4.9 g++-4.9 -y
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 50
apt-get install libncurses5-dev bc -y
/usr/bin/wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source && sudo chmod +x /usr/bin/rpi-source && /usr/bin/rpi-source -q --tag-update
rpi-source
printf "if the version is different from listed up here you should install this one instead with this command:\n apt-get install gcc-X.X g++-X.X \n and then change it with:\n update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-X.X 50\nDone\nInstalling xtable-addons dependencies"
apt-get install libtext-csv-xs-perl geoip-database libgeoip1 iptables-dev -y
cd /root || exit #Be Aware
wget http://downloads.sourceforge.net/project/xtables-addons/Xtables-addons/xtables-addons-2.14.tar.xz
tar xf xtables-addons-2.14.tar.xz
cd /root/xtables-addons-2.14 || exit # Be Aware
/bin/bash /root/xtables-addons-2.14/configure
make 
make install 
mkdir -v /usr/share/xt_geoip
cd /usr/share/xt_geoip || exit
/bin/bash /root/xtables-addons-2.14/geoip/xt_geoip_dl
/root/xtables-addons-2.14/geoip/xt_geoip_build -D . *.csv

# --- System Administration  ---
printf "Installing System Administration module\n==========\nInstalling Netadata for system monitoring\n"
# netdata installation 
apt-get install zlib1g-dev uuid-dev libmnl-dev pkg-config curl gcc make autoconf autoconf-archive autogen automake python python-yaml python-mysqldb nodejs lm-sensors python-psycopg2 netcat git -y
cd /root || exit
# ----------------------------------- Until this part everything works fine
git clone https://github.com/firehol/netdata.git --depth=1 ~/netdata
cd netdata || exit
echo -ne '\n' | /bin/bash /root/netdata/netdata-installer.sh
iptables -A INPUT -p tcp -m tcp --dport 19999 -j ACCEPT # Allow port 19999/tcp for monitoring via browser
printf "To view the Monitoring system in your browser, you must add this rule:\n    iptables -A INPUT -p tcp -m tcp --dport 19999 -j ACCEPT\nWe already added. However, if you Flush the INPUT chain, you will have to add it again\n" 

# --- SSH server Hardening  ---
# FIX SSH PROBLEM
printf "Hardening SSH Server\n==========\n"
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak || true
printf "saving default sshd_config to sshd_config.bak\n"
printf "LogLevel VERBOSE\nPermitRootLogin no\nAllowUsers secrouter\nAllowGroups network\nMaxAuthTries 3\nMaxSessions 3\nProtocol 2\nPermitEmptyPasswords no\nAuthorizedKeysFile	.ssh/authorized_keys\nChallengeResponseAuthentication no\nX11Forwarding no\nUsePAM yes\nPrintMotd no\nSubsystem	sftp	/usr/lib/ssh/sftp-server\nAcceptEnv LANG LC_*\n" > /etc/ssh/sshd_config
printf "hardening sshd_config"
mkdir -v /home/secrouter/.ssh
chmod 700 /home/secrouter/.ssh
chown secrouter:network /home/secrouter/.ssh
printf "Changing .ssh directory permissions\n"
systemctl restart ssh
printf "====\n"
printf "The best way to harden your system besides this configuration is to always use public keys instead of passwords and if you have to use passwords, Use long random words as passwords to improve the entropy of it\n==========\n"

# --- Adding kernel modules  ---
printf "Adding kernel modules"
printf "8021q\nx_tables\nnf_conntrack\nbridge" > /etc/modules
lsmod
# --- Must reboot ---
printf "======================================\n"
printf "THE SYSTEM WILL REBOOT IN 10 SECONDS\n"
max=10
for i in $(seq 1 $max)
do
    sleep 1
    COUNT=`expr $max - $i`
    printf "                 $COUNT\r"
done
reboot
