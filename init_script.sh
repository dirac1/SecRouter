#!/bin/bash
# You must run this script as root
# Script to start SecRouter in a Debian-like distribution
# !! This script is designed for Raspbian !!

# --- Package installation and admin configuration ---
echo "Creating the router user controller: secrouter"
echo "the default password is: routersec"
echo "----------------------------------------------------"
groupadd network
useradd -m -s /bin/bash -c "router controller" -u 1337 -g network secrouter
passwd secrouter
echo -e "routersec\nroutersec" | passwd secrouter
sudo adduser secrouter sudo 
echo "!!!!! the default password is: routersec !!!!!"

# --- Package installation and admin configuration ---
echo "Updating, Upgrading and Downloading basic packages"
echo "----------------------------------------------------"
apt-get update && apt-get upgrade -y
apt-get install wget curl git zip zsh vim tmux sudo htop iftop ipcalc ipython iwlm-sensors logrotate ncdu ntp vlan  -y
apt-get install build-essential libssl-dev libffi-dev python-dev -y

# Networking packages
echo "Downloading network packages"
echo "----------------------------------------------------"
apt-get install isc-dhcp-server isc-dhcp-client dnsutils bridge-utils vlan bind9iptables traceroute ifupdown2 hostapd whois ntp -y

# --- Ethernet & Routing ---
echo "Creating Files for Ethernet & Routing Module"
echo "----------------------------------------------------"
mkdir /etc/network/secrouter.conf
touch /etc/network/interfaces.d /etc/network/vlan.d /etc/network/bridge.d /etc/network/arp.d
echo "source /etc/network/interfaces.d\nsource /etc/network/vlan.d\nsource /etc/network/bridge.d" > /etc/network/secrouter.conf
echo "source /etc/network/secrouter.conf" > /etc/network/interfaces

# ---Firewall ---
echo "Configuring Firewall Module"
echo "----------------------------------------------------"
echo "net.ipv4.ip_forward = 1" > /etc/sysctl.conf
sysctl -p /etc/sysctl.conf

# xtables-addons Installation 
echo "Configuring RPI kernel to add xtables-addons modules for the Firewall Module"
echo "----------------------------------------------------"
apt-get install rpi-update
rpi-update 
gcc --version | grep gcc
apt-get install gcc-4.9 g++-4.9
update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 50
apt-get install libncurses5-dev
wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source && sudo chmod +x /usr/bin/rpi-source && /usr/bin/rpi-source -q --tag-update
rpi-source
echo "if the version is different from listed up here you should install this one instead with this command:\n apt-get install gcc-X.X g++-X.X \n and then change it with:\n update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-X.X 50"
echo "Done"
echo "Installing xtable-addons dependencies"
apt-get install libtext-csv-xs-perl geoip-database libgeoip1 iptables-dev
wget http://downloads.sourceforge.net/project/xtables-addons/Xtables-addons/xtables-addons-2.14.tar.xz
tar xf xtables-addons-2.14.tar.xz
cd xtables-addons-2.14 # !!!!!!! Remember the modifications
/bin/bash configure
make
make install
mkdir /usr/share/xt_geoip
cd /usr/share/xt_geoip # !!!!!!!! Remember the modifications
/bin/bash /usr/lib/xtables-addons/xt_geoip_dl
/usr/lib/xtables-addons/xt_geoip_build -D . *.csv

# --- System Administration  ---
echo "Installing System Administration module"
echo "----------------------------------------------------"
echo "Installing Netadata for system monitoring"
# Netdata installation 
apt-get install zlib1g-dev uuid-dev libmnl-dev pkg-config curl gcc make autoconf autoconf-archive autogen automake python python-yaml python-mysqldb nodejs lm-sensors python-psycopg2 netcat git -y
git clone https://github.com/firehol/netdata.git --depth=1 ~/netdata
cd netdata
/bin/bash /netdata-installer.sh
iptables -A INPUT -p tcp -m tcp --dport 19999 -j ACCEPT 
# Allow port 19999/tcp for monitoring via browser
echo "To view the Monitoring system in your browser, you must add this rule:"
echo "iptables -A INPUT -p tcp -m tcp --dport 19999 -j ACCEPT"
echo "We already added it this time. However, if you Flush the INPUT chain, you will have to add it later"


