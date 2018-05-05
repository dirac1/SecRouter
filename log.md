TODOS
======

**2018-03-18**

DHCP Server 
-----------
* Add the other files being used in the dhcp server to the enable and disable script
    - you must comment the interface on isc-dhcp-server 
    - you must comment the interface configuration on interface.d/[interface] **DONE**

* Start building the Static leases script 

* Create a new user inside de router 

* Give new user, super user access to the network characteristics **DONE** 
    - created a new group called network
    - allowed the user to run commands without password
 
* Enable one interface at a time 
    - Found a way to do it without involving modifying system services


DHCP CLIENT
-----------
* Start building the dhcp client script (you'll need extra scripts to do the renew/release buttons) **DONE**
    - Created a separated script for release/renew


**2018-03-20**

Debugging DHCP Server
---------------------
* Fix disable.py/enable.py to comment and uncomment the statement 'include /etc/dhcpcd.d/[interface]';



**2018-03-21**

Debugging DHCP Server
---------------------
* All scripts in dhcp\_server are working after debug with the prototype
    - You should find the way to show in leases status tab which hostnames are in static mode 
 
**2018-03-22**

Debugging DHCP Client
---------------------

* Debugged dhcp\_client scripts

**2018-03-24**

Ethernet & Routing
---------------------
* After all the conversations to consider the way to build this module, most of the requirment in it will be satisfied using the same methodology (writing on configuration files).
    - Vlan, Bridges, and Interfaces will be configured using ifupdown2 package
    - DNS will be configured using BIND9 
    - ARP will be configured using ip neigh (reviewing to make it permanent changes)

**2018-03-26**

Ethernet & Routing
---------------------
* ARP will be configured using the command ''arp'' inside the configuration file ''/etc/network/interfaces''
    - the next value needs to be added: ''post-up arp -f /etc/ethers''
    - inside the file /etc/ethers/ you'll add the entries using this format: ''\[MAC\] \[IP\]''
    - And restarting the interface

**2018-03-27**

Ethernet & Routing
---------------------
* Bridge an Vlans will be configured using the ifupdown2 configuration file in ''/etc/network/interfaces'' using individual files with the 'include source/to/file' statement

* DNS will be possible using the package BIND9, it just needs to configure one file and it'll accept just one variable, servers. It'll be possible to show the actual cache and to flush it.
    - DNS will have 1 toggle button (enable/disable) and 2 normal buttons to flush the cache and to view cache
    - DNS enable button will run a script in the router while disable will simply stop and disable (don't start on boot) the bind9 service
    - view cache will adquire data from the 
TO FIX: The cache isn't showed inside the database but the DNS server is working  **DONE**

**2018-03-31**

Ethernet & Routing
---------------------
* Interfaces, vlans, bridges configuration will be made using three separated directories included inside /etc/network/interfaces in the correct order -> /etc/network/interfaces.d -> /etc/network/vlan.d -> /etc/network/bridge.d
    - An initial script bonded to the sub-category button will write the statements inside /etc/network/ 
    - Therefore, each interface configuration will be placed based on his type.

* The static routing sub-category will bond to the interface used (interface,bridge,vlan)

* The same method will be used for arp 
    
**2018-03-31**

Ethernet & Routing
---------------------
* Creating the in_ipconf, vlan_ipconf and bridge_ipconf scripts 


**2018-04-01**

Ethernet & Routing
---------------------
* Debugging and improving int,vlan,bridge scripts

**2018-04-01**

Ethernet & Routing
---------------------
* Created static_route and static_arp and debugged them.

**2018-04-09**

Ethernet & Routing
---------------------
* Debugging  bridge script with the GUI

Firewall
--------
Firewall will contain three sub-categories: Filter, Port-Forwarding and NAT

* Documenting and sketching Filter module

**2018-04-13/14**

Ethernet & Routing
---------------------

* Debugging Vlan script and dhcp server modifications 

**2018-04-15**

Ethernet & Routing
---------------------

* Debugging ip route script  and arp static script

Firewall
--------
* The iptables rule design will be handled inside the GUI and  will be send to a script that will apply and save the rule

* Designing on paper Filter module

**2018-04-16**

Firewall
--------
* fix filter.py, sma function  and improve the whole script **DONE**
* Filter subsection GUI ready, testing backend 
* Designed Filter-controller.py script 

**2018-04-17**

Firewall
--------
* Debugged Firewall_controller.py (previously Filter_controller.py) script
* Filter subsection already tested Match and Target
* Nat backend script almost done
* Main Firewall section GUI designed with commands

**2018-04-18/19**

Firewall
--------
* Debugged Nat frontend (almost done)
* Finished filter frontend/backend
* Finished Main frontend/backend

SysAdmin
--------
* Started the GUI design on paper it'll contain three sections: Tools, System and ...

**2018-04-20**

SysAdmin
--------
* Started init_script.sh 
* Installed xtables-addons (geoIP) and netdata to monitor the system


**2018-04-21**

Ethernet & Routing
------------------
* Create a new function to erase blank lines in the configuration files, added stdout information regarding the configuration per function

**2018-04-22**

Firewall
--------
* Debugged NAT and Main
* Documentation and Flow Diagrams

SysAdmin
--------
* GUI design is ready, will have Three sections: ADMINISTRATION, LOGGING AND TOOLS

**2018-04-23**

SysAdmin
--------
* Adding backend configuration to the tools subsection
* Creating backup.py 

**2018-04-24**

SysAdmin
--------
* finished backup.py 
* finished Adding backend configuration to the tools subsection

**2018-04-25**

SysAdmin
--------

* GUI Activities
* Debugging backup_restore.py

**2018-04-28**

SysAdmin
--------
* Debugged and tested backup_restore.py
* Added NTP Client to the Administration subcategory
* Debugged Gui with backup_restore.py
* Added name translation for Ping,traceroute,whois in Tools subcategory

Firewall
--------
* Added upload file subcategory

DHCP Server 
-----------
* Network and gateway values linked with ethernet and routing values for each interface (physical,vlan or bridge)

**REMEMBER TO TEST ALL THE SCRIPTS AGAIN BECAUSE OF THE FUNCTION MOVEMENT TO A NEW FILE**

**2018-04-30**

SysAdmin
--------
* Planning password management in the module

**2018-04-30**

Secrouter
---------
* Creating init script

**2018-05-02**

SysAdmin
--------
* Module finished with documentation 

Secrouter
---------
* merging Login window with main window

**2018-05-03**

Secrouter
---------
* merging Login window with main window
* debugging init\_script.py
* creating SME and SOHO configurations

**2018-05-04**

Secrouter
---------
* merged Login window with main window
* debugguing init\_script.py
* Fixed Issue with STATUS subcategory in SysAdmin
* Fixing Saving data in GUI 

Home & About
------------
* Created this subcategories and now are functional (Need to add the University and School Logo)

DHCP Server 
-----------
* ToDo: Restart the device after configuring any DHCP Server Instance

Login
-----
* Removed Public Key Authentication (Will be a future feature)
