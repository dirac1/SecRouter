Small and Medium Enterprise 
===========================

This is a configuration to the requirements of a SME environment, with this basic configuration for the raspberrypi used as a prototype:

 
* Bridged Vlan Interfaces for trunking in one port which will go to the ethernet switch:
vlan100 static conf (Admin) vlan200 static conf (Office) vlan300 static conf(CCTV and server) in  the bridge br0 (manual) (LAN)
*  multiple DHCP Server instances for VLANs with an adequate VSLR (remember to use the same network segment from the static conf)
* Simple Firewall Rules for WAN ( Create them using a file)
* Nat Rule to masquerade all the packets coming from the LAN
* DNS Cache and Forwarder server (remember to create to redirect all request using port 53 to the router)



