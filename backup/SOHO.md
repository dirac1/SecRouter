Small HOme and Office Config 
============================

This is a configuration to the requirements of a SOHO environment, with this basic configuration for the raspberrypi used as a prototype:

* Bridged Interfaces: eth1 (manual) eth2 (manual) under the bridge br0 (static conf) (LAN)
 * No Vlan configuration
* DHCP Server configuration in authoritative mode for br0 with an adequate VSLR (remember to use the same network segment from the static conf)
* Simple Firewall Rules for WAN ( Create them using a file)
* Nat Rule to masquerade all the packets coming from the LAN
* DNS Cache and Forwarder server (remember to create to redirect all request using port 53 to the router)



