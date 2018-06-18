import sys, re, logging, os, ipaddress, socket, paramiko, ipcalc, pytz, webbrowser, zipfile, Languages
import os.path
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QTableWidgetItem, QFileDialog
import View_Cache
import time

from PyQt5 import uic
ssh_ip_url= ""
ssh_user=""
password = ""
ssh_cliente = ""

interfaces = " "
var = ["eth0" + "_Enable", "eth1" + "_Enable"]
var2 = ["eth0" + "_Enable", "eth1" + "_Enable"]

class Main(QDialog):

    def __init__(self):
        global ssh_ip_url, ssh_user, var
        QDialog.__init__(self)
        self.start_paramiko(str(ssh_ip_url),str(ssh_user),str(password))
        uic.loadUi("Main Window\Main.ui",self) #cargando archivo.ui
        self.interface_comboBox.addItem("N/A") #agregar interfaz vacia
        self.interface_client_comboBox.addItem("N/A")
        self.static_comboBox.addItem("N/A")
        self.status_comboBox.addItem("N/A")
        self.phisical_interfaces_comboBox.addItem("N/A")
        self.vlan_comboBox.addItem("N/A")
        self.bridge_comboBox.addItem("N/A")
        self.bridge_comboBox.addItem("bridge.default")
        self.static_route_comboBox.addItem("N/A")
        self.arp_comboBox.addItem("N/A")
        self.home()

        if not(os.path.isfile("arp_status.txt")):
            f = open("arp_status.txt",'w')
            f.write("Arp.0_Disable,eth0,1.1.1.1,FF:FF:FF:FF:FF\n")
            f.close()


        if not(os.path.isfile("static_route_status.txt")):
            f = open("static_route_status.txt",'w')
            f.write("SR.0_Disable,eth0,1.1.1.1,FF:FF:FF:FF:FF\n")
            f.close()

        if not(os.path.isfile("vlan_status.txt")):
            f = open("vlan_status.txt",'w')
            f.write("Vlan.0_Disable,0,300,eth0\n")
            f.close()

        if not(os.path.isfile("bridge_status.txt")):
            f = open("bridge_status.txt",'w')
            f.write("bridge.default,Disable,default,300,eth0\n")
            f.close()

        if not(os.path.isfile("estados.txt")):
            f = open("estados.txt",'w')
            for i in interfaces:
                if i != "lo" and i != "wlan0":
                    f.write(i+"_Enable\n")
            f.close()
        if not(os.path.isfile("client_state.txt")):
            k = open("client_state.txt","w")
            for i in interfaces:
                if i != "lo" and i != "wlan0":
                    k.write(i + ("_Enable\n"))
            k.close()
        if not(os.path.isfile("status.txt")):
            l = open("status.txt", 'w')
            l.write("Disable")
            l.close()
        if not(os.path.isfile("phisical_interface_status.txt")):
            f = open("phisical_interface_status.txt",'w')
            for i in interfaces:
                validar = re.search("eth",i)
                validar2 = re.search("w",i)
                if validar:
                    f.write(i+"_Enable\n")
                if validar2:
                    f.write(i+"_Enable\n")
            f.close()
        if not(os.path.isfile("ntp.txt")):
            f = open("ntp.txt",'w')
            f.write("Disable")
            f.close()
        for i in interfaces:
            if i != "lo" and i != "wlan0":
                self.interface_sniffer.addItem(i)
                self.interface_comboBox.addItem(i)
                self.interface_client_comboBox.addItem(i)
                self.static_comboBox.addItem(i)
                self.status_comboBox.addItem(i)
                self.nat_in_combobox.addItem(i)
                self.nat_out_combobox.addItem(i)
            validar = re.search("eth",i)
            validar2 = re.search("w",i)
            validar3 = re.search("Br",i)
            validar4 =  re.search("vlan",i)
            validar5 = re.search(".",i)
            if not(validar3) and not(validar4) and i != "lo":
                self.in_combobox.addItem(i)
                self.out_combobox.addItem(i)
            if validar and (len(i) < 5):  #OJO!!! ESTO ES UN PQC
                self.phisical_interfaces_comboBox.addItem(i)
            if validar2:
                self.phisical_interfaces_comboBox.addItem(i)

        a = open("estados.txt",'r')
        b = open("client_state.txt","r")
        var = a.readlines()
        var2 = b.readlines()
        a.close()
        b.close()

        horHeaders = ["IP Address", "MAC Address","Time Expires","Hostname"]
        self.columnview.setColumnCount(4)
        self.columnview.setHorizontalHeaderLabels(horHeaders)

        zone = pytz.all_timezones
        for i in zone:
            self.timezone.addItem(i)



#DHCP SERVER:
        self.interface_comboBox.currentIndexChanged.connect(self.combobox)
        self.dhcp_client_config_box.hide()
        self.status_leases.hide()
        self.static_config_box.hide()
        self.dhcp_client_button.clicked.connect(self.menu1)
        self.static_leases_button.clicked.connect(self.menu2)
        self.enable_disable_button.clicked.connect(self.enable_disable)
        self.dhcp_save_button.clicked.connect(self.save_button)
        self.dhcp_server_delete_button.clicked.connect(self.delete_button)
        self.dhcp_server_button.clicked.connect(self.interface)
        self.interface_comboBox.currentIndexChanged.connect(self.meh)
#STATIC:
        self.static_leases_apply_button.clicked.connect(self.satatic)
        self.dns_ether_and_rout_button.clicked.connect(self.check_dns)
#STATUS:
        self.status_delete_Button.clicked.connect(self.delete_status)
        self.status_leases_button.clicked.connect(self.leases)
        self.status_leases_button.clicked.connect(self.log)
        self.refresh_status_button.clicked.connect(self.leases)
        self.refresh_status_button.clicked.connect(self.log)
#DHCP CLIENT:
        self.interface_client_comboBox.currentIndexChanged.connect(self.client_dhcp_combobox)
        self.client_dhcp_apply_button.clicked.connect(self.enable_disable_dhcp)
        self.client_dhcp_release_button.clicked.connect(self.release)
        self.client_dhcp_renew_button.clicked.connect(self.renew)

############################### ROUTING #######################################
#DNS
        self.dns_ether_and_rout_button.clicked.connect(self.check_dns)
        self.enable_routing_Button.clicked.connect(self.dns_routing)
        self.view_cache_button.clicked.connect(self.view_cache)
        self.flush_button.clicked.connect(self.flush)
        self.view_cache_button.clicked.connect(self.view_cache)

#PHISICAL INTERFACES
        self.phisical_interfaces_comboBox.currentIndexChanged.connect(self.phisical_interface)
        self.enable_disable__interfaces_button.clicked.connect(self.apply_phisical_interfaces)
        self.delete_interface_button.clicked.connect(self.delete_phisical_interface)
        self.manual_radioButton.clicked.connect(self.radian_button)
        self.static_radioButton.clicked.connect(self.radian_button)
        self.dhcp_radioButton.clicked.connect(self.radian_button)
        self.phisical_interfaces_comboBox.currentIndexChanged.connect(self.phisical_interface)
# VLAN
        self.Vlan.clicked.connect(self.vlan)
        self.enable_disable__vlan_button.clicked.connect(self.apply_vlan)
        self.manual_vlan_radioButton.clicked.connect(self.radio_vlan_button)
        self.static_vlan_radioButton.clicked.connect(self.radio_vlan_button)
        self.dhcp_vlan_radioButton.clicked.connect(self.radio_vlan_button)
        self.add_vlan_Button.clicked.connect(self.add_vlan)
        self.remove_vlan_Button.clicked.connect(self.remove_vlan)
        self.vlan_comboBox.currentIndexChanged.connect(self.change_vlan)
# BRIDGE
        self.Bridge.clicked.connect(self.bridge)
        self.enable_disable__bridge_button.clicked.connect(self.apply_bridge)
        self.delete_bridge_button.clicked.connect(self.delete_bridge)
        self.manual_bridge_radioButton.clicked.connect(self.radio_bridge_button)
        self.static_bridge_radioButton.clicked.connect(self.radio_bridge_button)
        self.dhcp_bridge_radioButton.clicked.connect(self.radio_bridge_button)
        self.add_bridge_Button.clicked.connect(self.add_bridge)
        self.remove_bridge_Button.clicked.connect(self.remove_bridge)
        self.bridge_comboBox.currentIndexChanged.connect(self.change_bridge)
# STATIC ROUTING
        self.static_routing_ether_and_rout_button.clicked.connect(self.static_route)
        self.enable_disable_static_route_button.clicked.connect(self.apply_static_route)
        #self.inter_static_route_radioButton.clicked.connect(self.radio_static_route_button)
        #self.vlan_static_route_radioButton.clicked.connect(self.radio_static_route_button)
        #self.bridge_static_route_radioButton.clicked.connect(self.radio_static_route_button)
        self.add_static_route_Button.clicked.connect(self.add_static_route)
        self.remove_static_route_button.clicked.connect(self.remove_static_route)
        self.static_route_comboBox.currentIndexChanged.connect(self.change_static_route)
# STATIC ARP
        self.Arp.clicked.connect(self.arp)
        self.enable_disable_arp_button.clicked.connect(self.apply_arp)
        #self.inter_arp_radioButton.clicked.connect(self.radio_arp_button)
        #self.vlan_arp_radioButton.clicked.connect(self.radio_arp_button)
        #self.bridge_arp_radioButton.clicked.connect(self.radio_arp_button)
        self.add_arp_Button.clicked.connect(self.add_arp)
        self.remove_arp_button.clicked.connect(self.remove_arp)
        self.arp_comboBox.currentIndexChanged.connect(self.change_arp)

############################# FIREWALL #########################################
        self.apply_filter_button.clicked.connect(self.apply_filter)
        self.add_main.clicked.connect(self.Add_main)
        self.delete_main.clicked.connect( self.Delete_main)
        self.apply_main.clicked.connect(self.delete_rule)
        self.apply_policy.clicked.connect(self.policy)
        self.view_main.clicked.connect(self.view_rule)
        self.flush_main.clicked.connect(self.flush)
        self.table_comboBox.currentIndexChanged.connect(self.rule)
        self.chain_combox.currentIndexChanged.connect(self.change_chain_filter)
        self.e_in.clicked.connect(self.check_in_out_filter)
        self.e_out.clicked.connect(self.check_in_out_filter)
        self.rule_combobox.currentIndexChanged.connect(self.change_rule)
        self.action_combobox.currentIndexChanged.connect(self.change_action)
        self.e_mac.clicked.connect(self.change_mac)
        self.e_geoip.clicked.connect(self.change_geoip)
        self.e_IP_Match.clicked.connect(self.change_ip)
        self.e_src_addr.clicked.connect(self.change_ip)
        self.e_dst_addr.clicked.connect(self.change_ip)
        self.e_src_addr_range.clicked.connect(self.change_ip)
        self.e_dst_addr_range.clicked.connect(self.change_ip)
        self.e_tcp_Match.clicked.connect(self.change_port)
        self.e_src_port_tcp.clicked.connect(self.change_port)
        self.e_dst_port_tcp.clicked.connect(self.change_port)
        self.e_tcp_flags.clicked.connect(self.change_port)
        self.e_udp_Match.clicked.connect(self.change_udp)
        self.e_src_port_udp.clicked.connect(self.change_udp)
        self.e_dst_port_udp.clicked.connect(self.change_udp)
        self.e_icmp_type.clicked.connect(self.change_icmp)
        self.e_multi_port.clicked.connect(self.change_multiport)
        self.e_src_port_multi.clicked.connect(self.change_multiport)
        self.e_dst_port_multi.clicked.connect(self.change_multiport)
        self.e_state.clicked.connect(self.change_state)
        self.e_limit.clicked.connect(self.change_limit)
        self.e_limit_rate.clicked.connect(self.change_limit)
        self.e_limit_burst.clicked.connect(self.change_limit)
        self.e_time.clicked.connect(self.change_time)
        self.e_date_start.clicked.connect(self.change_time)
        self.e_date_stop.clicked.connect(self.change_time)
        self.e_time_start.clicked.connect(self.change_time)
        self.e_time_stop.clicked.connect(self.change_time)
        self.e_month_days.clicked.connect(self.change_time)
        self.e_week_days.clicked.connect(self.change_time)
        self.e_string.clicked.connect(self.change_string)
        self.e_algo.clicked.connect(self.change_string)
        self.e_from_data.clicked.connect(self.change_string)
        self.e_to_data.clicked.connect(self.change_string)
        self.e_check_string.clicked.connect(self.change_string)
        self.e_ttl.clicked.connect(self.change_ttl)
        self.e_ttl_eq.clicked.connect(self.change_ttl)
        self.e_ttl_gt.clicked.connect(self.change_ttl)
        self.e_ttl_lt.clicked.connect(self.change_ttl)
        self.e_comment.clicked.connect(self.change_comment)

#--------------------------------- NAT ----------------------------------------
        self.nat_apply_filter_button.clicked.connect(self.apply_nat)
        self.nat_chain_combox.currentIndexChanged.connect(self.change_chain_nat)
        self.nat_e_in.clicked.connect(self.check_in_out_nat)
        self.nat_e_out.clicked.connect(self.check_in_out_nat)
        self.nat_rule_combobox.currentIndexChanged.connect(self.change_rule_nat)
        self.nat_action_combobox.currentIndexChanged.connect(self.change_action_nat)
        self.nat_chain_combox.currentIndexChanged.connect(self.change_action_nat)
        self.nat_e_IP_Match.clicked.connect(self.change_ip_nat)
        self.nat_e_src_addr.clicked.connect(self.change_ip_nat)
        self.nat_e_dst_addr.clicked.connect(self.change_ip_nat)
        self.nat_e_src_addr_range.clicked.connect(self.change_ip_nat)
        self.nat_e_dst_addr_range.clicked.connect(self.change_ip_nat)
        self.nat_e_tcp_Match.clicked.connect(self.change_port_nat)
        self.nat_e_src_port_tcp.clicked.connect(self.change_port_nat)
        self.nat_e_dst_port_tcp.clicked.connect(self.change_port_nat)
        self.nat_e_tcp_flags.clicked.connect(self.change_port_nat)
        self.nat_e_udp_Match.clicked.connect(self.change_udp_nat)
        self.nat_e_src_port_udp.clicked.connect(self.change_udp_nat)
        self.nat_e_dst_port_udp.clicked.connect(self.change_udp_nat)
        self.nat_e_icmp_type.clicked.connect(self.change_icmp_nat)
        self.nat_e_multi_port.clicked.connect(self.change_multiport_nat)
        self.nat_e_src_port_multi.clicked.connect(self.change_multiport_nat)
        self.nat_e_dst_port_multi.clicked.connect(self.change_multiport_nat)
        self.nat_e_state.clicked.connect(self.change_state_nat)
        self.nat_e_limit.clicked.connect(self.change_limit_nat)
        self.nat_e_limit_rate.clicked.connect(self.change_limit_nat)
        self.nat_e_limit_burst.clicked.connect(self.change_limit_nat)
        self.nat_e_time.clicked.connect(self.change_time_nat)
        self.nat_e_date_start.clicked.connect(self.change_time_nat)
        self.nat_e_date_stop.clicked.connect(self.change_time_nat)
        self.nat_e_time_start.clicked.connect(self.change_time_nat)
        self.nat_e_time_stop.clicked.connect(self.change_time_nat)
        self.nat_e_month_days.clicked.connect(self.change_time_nat)
        self.nat_e_week_days.clicked.connect(self.change_time_nat)
        self.nat_e_string.clicked.connect(self.change_string_nat)
        self.nat_e_algo.clicked.connect(self.change_string_nat)
        self.nat_e_from_data.clicked.connect(self.change_string_nat)
        self.nat_e_to_data.clicked.connect(self.change_string_nat)
        self.nat_e_check_string.clicked.connect(self.change_string_nat)
        self.nat_e_ttl.clicked.connect(self.change_ttl_nat)
        self.nat_e_ttl_eq.clicked.connect(self.change_ttl_nat)
        self.nat_e_ttl_gt.clicked.connect(self.change_ttl_nat)
        self.nat_e_ttl_lt.clicked.connect(self.change_ttl_nat)
        self.nat_e_comment.clicked.connect(self.change_comment_nat)
        self.e_masquerade.clicked.connect(self.change_masquerade)
        self.ping_apply.clicked.connect(self.ping)
        self.traceroute_apply.clicked.connect(self.traceroute)
        self.lookup_apply.clicked.connect(self.lookup)
        self.whois_apply.clicked.connect(self.whois)
        self.ipcalc_button.clicked.connect(self.ipcalc)
        self.e_src_sniffer.clicked.connect(self.change_sniffer)
        self.e_dst_sniffer.clicked.connect(self.change_sniffer)
        self.e_src_port_sniffer.clicked.connect(self.change_sniffer)
        self.e_dst_port_sniffer.clicked.connect(self.change_sniffer)
        self.start_button.clicked.connect(self.sniffer)
        self.apply_time.clicked.connect(self.time_date)
        self.timezone.currentIndexChanged.connect(self.time_zone)
        self.apply_logging.clicked.connect(self.logging)
        self.reboot_button.clicked.connect(self.reboot)
        self.clear_button.clicked.connect(self.clear)
        self.refresh_button.clicked.connect(self.logging)
        self.int_config.clicked.connect(self.interface_config)
        self.update_button.clicked.connect(self.update)
        self.status.clicked.connect(self.web)
        self.backup_button.clicked.connect(self.backup)
        self.restore_button.clicked.connect(self.restore)
        self.comboBox.currentIndexChanged.connect(self.backup_type)
        self.ntp_button.clicked.connect(self.ntp)
        self.upload_button.clicked.connect(self.change_upload)
        self.change_pass_button.clicked.connect(self.change_pass)
        self.Maintab.currentChanged.connect(self.home)
        self.chain_comboBox.currentIndexChanged.connect(self.change_delete_rule)
        self.chain_flush_comboBox.currentIndexChanged.connect(self.change_flush)
        self.chain_policy_comboBox.currentIndexChanged.connect(self.change_policy)
        self.spanish_button.clicked.connect(self.prueba1)
        self.english_button.clicked.connect(self.prueba2)
        self.pushButton_6.clicked.connect(self.delete_backup)
#aca
# validaciones:
        self.network_line_edit.textChanged.connect(self.validar_network_line_edit) # llamada a validar network
        self.prefijo_line_edit.textChanged.connect(self.validar_prefijo_line_edit) # llamada a validar prefijo
        self.getaway_line_edit.textChanged.connect(self.validar_getaway_line_edit) # llamada a validar getaway
        self.pool_range_start_line_edit.textChanged.connect(self.validar_pool_range_start_line_edit) # llamada a validar start_pool
        self.pool_range_stop_line_edit.textChanged.connect(self.validar_pool_range_stop_line_edit) # llamada a validar stop_pool
        self.dns_server_line_edit.textChanged.connect(self.validar_dns_server_line_edit)# llamada a validar dns
        self.time_hour_line_edit.textChanged.connect(self.validar_horas) # llamada a validar hora
        self.time_minute_line_edit.textChanged.connect(self.validar_minutos) #llamada a validar minutos
        self.time_second_line_edit.textChanged.connect(self.validar_segundos) #llamada a validar segundos
        self.ip_static_line_edit.textChanged.connect(self.validar_ip_static_line_edit) #llamar a vaclidar ip estatico
        self.mac_static_line_edit.textChanged.connect(self.validar_mac_static_line_edit) #llamar a validar mac estatico
        self.dhcp_server_apply_button.clicked.connect(self.apply_button)
        self.server1.textChanged.connect(self.validar_server1_line_edit)
        self.server2.textChanged.connect(self.validar_server2_line_edit)
        self.server3.textChanged.connect(self.validar_server3_line_edit)
        self.cache_size.textChanged.connect(self.validar_size_cache_line_edit)
        self.language_config.hide()
        self.interfaces.hide()
        self.static_routing.hide()
        self.Vlan_config.hide()
        self.Bridge_config.hide()
        self.arp_config.hide()
        self.nat_config.hide()
        self.filter_config.hide()
        self.tools_config.hide()
        self.logging_config.hide()
        self.time_config.hide()
        self.upload_config.hide()
        self.e_in.setEnabled(False)
        self.e_out.setEnabled(False)
        self.in_not.setEnabled(False)
        self.out_not.setEnabled(False)
        self.in_combobox.setEnabled(False)
        self.out_combobox.setEnabled(False)
        self.rule_line_edit.setEnabled(False)
        self.reject_combobox.setEnabled(False)
        self.log_combobox.setEnabled(False)
        self.prefix_line_edit.setEnabled(False)
        self.e_mac.setEnabled(False)
        self.mac_not.setEnabled(False)
        self.mac_line_edit.setEnabled(False)
        self.e_geoip.setEnabled(False)
        self.geoip_not.setEnabled(False)
        self.geoip_line_edit.setEnabled(False)
        self.e_src_addr.setEnabled(False)
        self.src_addr_not.setEnabled(False)
        self.src_addr_line_edit.setEnabled(False)
        self.e_dst_addr.setEnabled(False)
        self.dst_addr_not.setEnabled(False)
        self.dst_addr_line_edit.setEnabled(False)
        self.e_src_addr_range.setEnabled(False)
        self.src_addr_range_not.setEnabled(False)
        self.src_addr_range_line_edit.setEnabled(False)
        self.e_dst_addr_range.setEnabled(False)
        self.dst_addr_range_not.setEnabled(False)
        self.dst_addr_range_line_edit.setEnabled(False)
        self.e_src_port_tcp.setEnabled(False)
        self.e_dst_port_tcp.setEnabled(False)
        self.e_tcp_flags.setEnabled(False)
        self.src_port_tcp_not.setEnabled(False)
        self.src_port_tcp_line_edit.setEnabled(False)
        self.dst_port_tcp_not.setEnabled(False)
        self.dst_port_tcp_line_edit.setEnabled(False)
        self.tcp_flags_not.setEnabled(False)
        self.tcp_flags_line_edit.setEnabled(False)
        self.e_src_port_udp.setEnabled(False)
        self.e_dst_port_udp.setEnabled(False)
        self.src_port_udp_not.setEnabled(False)
        self.src_port_udp_line_edit.setEnabled(False)
        self.dst_port_udp_not.setEnabled(False)
        self.dst_port_udp_line_edit.setEnabled(False)
        self.icmp_type_not.setEnabled(False)
        self.icmp_type_line_edit.setEnabled(False)
        self.e_src_port_multi.setEnabled(False)
        self.e_dst_port_multi.setEnabled(False)
        self.protocol_combobox.setEnabled(False)
        self.protocol_not.setEnabled(False)
        self.src_port_multi_not.setEnabled(False)
        self.src_port_multi_line_edit.setEnabled(False)
        self.dst_port_multi_not.setEnabled(False)
        self.dst_port_multi_line_edit.setEnabled(False)
        self.state_not.setEnabled(False)
        self.state_line_edit.setEnabled(False)
        self.e_limit_rate.setEnabled(False)
        self.e_limit_burst.setEnabled(False)
        self.limit_rate_line_edit.setEnabled(False)
        self.limit_burst_line_edit.setEnabled(False)
        self.e_date_start.setEnabled(False)
        self.e_date_stop.setEnabled(False)
        self.e_time_start.setEnabled(False)
        self.e_time_stop.setEnabled(False)
        self.e_month_days.setEnabled(False)
        self.e_week_days.setEnabled(False)
        self.date_start_line_edit.setEnabled(False)
        self.date_stop_line_edit.setEnabled(False)
        self.time_start_line_edit.setEnabled(False)
        self.time_stop_line_edit.setEnabled(False)
        self.month_days_not.setEnabled(False)
        self.month_days_line_edit.setEnabled(False)
        self.week_days_not.setEnabled(False)
        self.week_days_line_edit.setEnabled(False)
        self.e_algo.setEnabled(False)
        self.e_from_data.setEnabled(False)
        self.e_to_data.setEnabled(False)
        self.e_check_string.setEnabled(False)
        self.algo_combobox.setEnabled(False)
        self.from_data_line_edit.setEnabled(False)
        self.to_data_line_edit.setEnabled(False)
        self.check_string_not.setEnabled(False)
        self.check_string_line_edit.setEnabled(False)
        self.e_ttl_eq.setEnabled(False)
        self.e_ttl_gt.setEnabled(False)
        self.e_ttl_lt.setEnabled(False)
        self.ttl_eq_not.setEnabled(False)
        self.ttl_eq_not.setEnabled(False)
        self.ttl_gt_line_edit.setEnabled(False)
        self.ttl_lt_line_edit.setEnabled(False)
        self.ttl_eq_line_edit.setEnabled(False)
        self.comment_line_edit.setEnabled(False)
        self.nat_dst_addr_range_not.setEnabled(False)
        self.nat_dst_addr_range_line_edit.setEnabled(False)
        self.nat_e_src_port_tcp.setEnabled(False)
        self.nat_e_dst_port_tcp.setEnabled(False)
        self.nat_e_tcp_flags.setEnabled(False)
        self.nat_src_port_tcp_not.setEnabled(False)
        self.nat_src_port_tcp_line_edit.setEnabled(False)
        self.nat_dst_port_tcp_not.setEnabled(False)
        self.nat_dst_port_tcp_line_edit.setEnabled(False)
        self.nat_tcp_flags_not.setEnabled(False)
        self.nat_tcp_flags_line_edit.setEnabled(False)
        self.nat_e_src_port_udp.setEnabled(False)
        self.nat_e_dst_port_udp.setEnabled(False)
        self.nat_src_port_udp_not.setEnabled(False)
        self.nat_src_port_udp_line_edit.setEnabled(False)
        self.nat_dst_port_udp_not.setEnabled(False)
        self.nat_dst_port_udp_line_edit.setEnabled(False)
        self.nat_icmp_type_not.setEnabled(False)
        self.nat_icmp_type_line_edit.setEnabled(False)
        self.nat_e_src_port_multi.setEnabled(False)
        self.nat_e_dst_port_multi.setEnabled(False)
        self.nat_protocol_combobox.setEnabled(False)
        self.nat_protocol_not.setEnabled(False)
        self.nat_src_port_multi_not.setEnabled(False)
        self.nat_src_port_multi_line_edit.setEnabled(False)
        self.nat_dst_port_multi_not.setEnabled(False)
        self.nat_dst_port_multi_line_edit.setEnabled(False)
        self.nat_state_not.setEnabled(False)
        self.nat_state_line_edit.setEnabled(False)
        self.nat_e_limit_rate.setEnabled(False)
        self.nat_e_limit_burst.setEnabled(False)
        self.nat_limit_rate_line_edit.setEnabled(False)
        self.nat_limit_burst_line_edit.setEnabled(False)
        self.nat_e_date_start.setEnabled(False)
        self.nat_e_date_stop.setEnabled(False)
        self.nat_e_time_start.setEnabled(False)
        self.nat_e_time_stop.setEnabled(False)
        self.nat_e_month_days.setEnabled(False)
        self.nat_e_week_days.setEnabled(False)
        self.nat_date_start_line_edit.setEnabled(False)
        self.nat_date_stop_line_edit.setEnabled(False)
        self.nat_time_start_line_edit.setEnabled(False)
        self.nat_time_stop_line_edit.setEnabled(False)
        self.nat_month_days_not.setEnabled(False)
        self.nat_month_days_line_edit.setEnabled(False)
        self.nat_week_days_not.setEnabled(False)
        self.nat_week_days_line_edit.setEnabled(False)
        self.nat_e_algo.setEnabled(False)
        self.nat_e_from_data.setEnabled(False)
        self.nat_e_to_data.setEnabled(False)
        self.nat_e_check_string.setEnabled(False)
        self.nat_algo_combobox.setEnabled(False)
        self.nat_from_data_line_edit.setEnabled(False)
        self.nat_to_data_line_edit.setEnabled(False)
        self.nat_check_string_not.setEnabled(False)
        self.nat_check_string_line_edit.setEnabled(False)
        self.nat_e_ttl_eq.setEnabled(False)
        self.nat_e_ttl_gt.setEnabled(False)
        self.nat_e_ttl_lt.setEnabled(False)
        self.nat_ttl_eq_not.setEnabled(False)
        self.nat_ttl_eq_not.setEnabled(False)
        self.nat_ttl_gt_line_edit.setEnabled(False)
        self.nat_ttl_lt_line_edit.setEnabled(False)
        self.nat_ttl_eq_line_edit.setEnabled(False)
        self.nat_comment_line_edit.setEnabled(False)
        self.nat_rule_line_edit.setEnabled(False)
        self.nat_in_combobox.setEnabled(False)
        self.nat_out_combobox.setEnabled(False)
        self.nat_e_in.setEnabled(False)
        self.nat_e_out.setEnabled(False)
        self.nat_in_not.setEnabled(False)
        self.nat_out_not.setEnabled(False)
        self.snat.setEnabled(False)
        self.dnat.setEnabled(False)
        self.nat_log_combobox.setEnabled(False)
        self.nat_prefix_line_edit.setEnabled(False)
        self.e_masquerade.setEnabled(False)
        self.masquerade.setEnabled(False)
        self.redirect.setEnabled(False)
        self.src_sniffer.setEnabled(False)
        self.dst_sniffer.setEnabled(False)
        self.src_port_sniffer.setEnabled(False)
        self.dst_port_sniffer.setEnabled(False)
        #self.chain_combox.setEnabled(False)
        self.chain_target_action.setEnabled(False)
        self.pass_textEdit.hide()
    def start_paramiko( cuarto, ip, user, password,):
        global ssh_cliente, interfaces
        paramiko.util.log_to_file('ssh.log')
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #user = "secrouter"
        #password = "ducaco1234"
        #ip = "192.168.1.10"
        ssh_cliente.connect(ip, port = 22, username = user, password = password)
        sftp = ssh_cliente.open_sftp()
        interfaces = sftp.listdir(path="/sys/class/net")
        return True

#apagar
    def menu1(self):
        self.dhcp_client_config_box.show()
        self.dhcp_server_config_box.hide()
        self.static_config_box.hide()
    def menu2(self):
        self.dhcp_client_config_box.hide()
        self.dhcp_server_config_box.hide()
        self.static_config_box.show()


#-------- BOTON APLLY DE MODULO DHCP SERVER ------------------------------------
    def interface(self):
        self.interface_comboBox.clear()

        sftp = ssh_cliente.open_sftp()
        interfaces = sftp.listdir(path="/sys/class/net")
        for i in interfaces:
            if i != "lo":
                self.interface_comboBox.addItem(i)

    def meh(self):
        if self.interface_comboBox.currentText() == self.phisical_interfaces_comboBox.currentText():
            self.network_line_edit.setText(self.network_interfaces.text())
            self.prefijo_line_edit.setText(self.pref_interfaces.text())
            self.getaway_line_edit.setText(self.ip_interfaces.text())

    def apply_button (self):


        inter = self.interface_comboBox.currentText()
        network = self.network_line_edit.text()
        getaway = self.getaway_line_edit.text()
        prefijo = self.prefijo_line_edit.text()
        pool_start = self.pool_range_start_line_edit.text()
        pool_stop = self.pool_range_stop_line_edit.text()
        dns = self.dns_server_line_edit.text()
        hour = self.time_hour_line_edit.text()
        minute = self.time_minute_line_edit.text()
        second = self.time_second_line_edit.text()
        print(inter)
        #try:
        Pool_Network_Size = len(list(ipaddress.ip_network(network).hosts()))-1
        Pool_Range_Size = (int(ipaddress.IPv4Address(pool_start)) - int(ipaddress.IPv4Address(pool_stop)))+1 # makes the calculation using Pool_Range
        Private = ipaddress.ip_network(network).is_private #check if the network is private
        Range_Valid = False if Pool_Range_Size - Pool_Network_Size > 0 else True #Check if the range length is valid
        Lease_Time_secs = int(hour)*3600 + int(minute)*60 + int(second)
        print(Lease_Time_secs)
        print(Range_Valid)
        if self.arp_check_box.isChecked():
            check = True
        else:
            check = False
        stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_server/dhcp_server.py " + str(inter) + " " + str(network) + " " + str(prefijo) + " " + str(getaway) + " " + str(pool_start) + " " + str(pool_stop) + " " + str(dns) + " "
        + "9.9.9.9"  + " " + str(Lease_Time_secs) + " " + str(check))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)

        if Private == True:
            print('IP PRIVADA')
        else:
            print("IP PUBLICA")

        stdin, stdout, stderr = ssh_cliente.exec_command("sudo reboot ")
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        QMessageBox.warning(self,"Advertencia","El dispositivo se reiniciara para configurar el servidor DHCP.",QMessageBox.Ok)
        exit()


#------------------------- MODULO BOTON SAVE DEL SERVIDOR DHCP ---------------------

    def save_button (self):
            inter = self.interface_comboBox.currentText()
            network = self.network_line_edit.text()
            getaway  = self.getaway_line_edit.text()
            prefijo = self.prefijo_line_edit.text()
            dns = self.dns_server_line_edit.text()
            pool_start = self.pool_range_start_line_edit.text()
            pool_stop = self.pool_range_stop_line_edit.text()
            hour = self.time_hour_line_edit.text()
            minute = self.time_minute_line_edit.text()
            second = self.time_second_line_edit.text()
            if self.arp_check_box.isChecked():
                w = "check"
            else:
                w ="unchek"
            sftp = ssh_cliente.open_sftp()
            save =sftp.file("/home/secrouter/tmp/" + str(inter)+'_save.txt', "w", -1)
            save.write(network + ',' + getaway + ',' + prefijo + ',' + dns + ',' + pool_start + ',' + pool_stop + ',' + hour  + ',' + minute + ',' + second+ ',' + w)
            save.flush()
            sftp.close()
            QMessageBox.information(self,"Save","Configuracion guardado con exito!.",QMessageBox.Ok)


#----------------------- MODULO DELETE DEL SERVIDOR DHCP ------------------------------------------

    def delete_button (self):

        inter = self.interface_comboBox.currentText()
        self.network_line_edit.setText("")
        self.network_line_edit.setStyleSheet("no border")
        self.getaway_line_edit.setText("")
        self.getaway_line_edit.setStyleSheet("no border")
        self.prefijo_line_edit.setText("")
        self.prefijo_line_edit.setStyleSheet("no border")
        self.dns_server_line_edit.setText("")
        self.dns_server_line_edit.setStyleSheet("no border")
        self.pool_range_start_line_edit.setText("")
        self.pool_range_start_line_edit.setStyleSheet("no border")
        self.pool_range_stop_line_edit.setText("")
        self.pool_range_stop_line_edit.setStyleSheet("no border")
        self.time_hour_line_edit.setText("")
        self.time_hour_line_edit.setStyleSheet("no border")
        self.time_minute_line_edit.setText("")
        self.time_minute_line_edit.setStyleSheet("no border")
        self.time_second_line_edit.setText("")
        self.time_second_line_edit.setStyleSheet("no border")
        #sftp.remove('/home/secrouter/'+ str(inter) +'_save.txt')
        try:
            tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_server/delete.py " +str(inter))
            x = stderr.readlines()
            print(x)
        except: pass


#---------------------- MODULO DISABLE/ENABLE DHCP ------------------------------------------------------
    def clear(self):
        inter = self.interface_comboBox.currentText()
        self.network_line_edit.setText("")
        self.network_line_edit.setStyleSheet("no border")
        self.getaway_line_edit.setText("")
        self.getaway_line_edit.setStyleSheet("no border")
        self.prefijo_line_edit.setText("")
        self.prefijo_line_edit.setStyleSheet("no border")
        self.dns_server_line_edit.setText("")
        self.dns_server_line_edit.setStyleSheet("no border")
        self.pool_range_start_line_edit.setText("")
        self.pool_range_start_line_edit.setStyleSheet("no border")
        self.pool_range_stop_line_edit.setText("")
        self.pool_range_stop_line_edit.setStyleSheet("no border")
        self.time_hour_line_edit.setText("")
        self.time_hour_line_edit.setStyleSheet("no border")
        self.time_minute_line_edit.setText("")
        self.time_minute_line_edit.setStyleSheet("no border")
        self.time_second_line_edit.setText("")
        self.time_second_line_edit.setStyleSheet("no border")

    def combobox(self):
        #sftp = ssh_cliente.open_sftp()
        #interfaces = sftp.listdir(path="/sys/class/net")
        #if not(os.path.isfile("estados.txt")):
        #    f = open("estados.txt",'w')
        #    for i in interfaces:
        #        if i != "lo" and i != "wlan0":
        #            f.write(i+"_Disable\n")
        #    f.close()

        inter = self.interface_comboBox.currentText()
        estado = open("estados.txt", "r")
        var = estado.readlines()
        estado.close()
        self.network_line_edit.setText("")
        self.network_line_edit.setStyleSheet("no border")
        self.getaway_line_edit.setText("")
        self.getaway_line_edit.setStyleSheet("no border")
        self.prefijo_line_edit.setText("")
        self.prefijo_line_edit.setStyleSheet("no border")
        self.dns_server_line_edit.setText("")
        self.dns_server_line_edit.setStyleSheet("no border")
        self.pool_range_start_line_edit.setText("")
        self.pool_range_start_line_edit.setStyleSheet("no border")
        self.pool_range_stop_line_edit.setText("")
        self.pool_range_stop_line_edit.setStyleSheet("no border")
        self.time_hour_line_edit.setText("")
        self.time_hour_line_edit.setStyleSheet("no border")
        self.time_minute_line_edit.setText("")
        self.time_minute_line_edit.setStyleSheet("no border")
        self.time_second_line_edit.setText("")
        self.time_second_line_edit.setStyleSheet("no border")
        #if inter == "N/A": self.clear()
        for i in var:

            if i == (str(inter) +"_Enable\n") or i == (str(inter) +"_Enable") :
                try:
                    sftp = ssh_cliente.open_sftp()
                    save = sftp.file("/home/secrouter/tmp/"+ str(inter)+'_save.txt', "r", -1)
                    a = save.readlines()
                    save.close()
                    c = a[0].split(",")
                    self.network_line_edit.setText(c[0])
                    self.getaway_line_edit.setText(c[1])
                    self.prefijo_line_edit.setText(c[2])
                    self.dns_server_line_edit.setText(c[3])
                    self.pool_range_start_line_edit.setText(c[4])
                    self.pool_range_stop_line_edit.setText(c[5])
                    self.time_hour_line_edit.setText(c[6])
                    self.time_minute_line_edit.setText(c[7])
                    self.time_second_line_edit.setText(c[8])
                    w = c[9]
                    if w == "check":
                        self.arp_check_box.setChecked(True)
                    else:
                        self.arp_check_box.setChecked(False)
                except:
#                    self.clear()
                    self.enable_disable_button.setText("Enable")
                    self.network_line_edit.setEnabled(True)
                    self.getaway_line_edit.setEnabled(True)
                    self.prefijo_line_edit.setEnabled(True)
                    self.dns_server_line_edit.setEnabled(True)
                    self.pool_range_start_line_edit.setEnabled(True)
                    self.pool_range_stop_line_edit.setEnabled(True)
                    self.time_hour_line_edit.setEnabled(True)
                    self.time_minute_line_edit.setEnabled(True)
                    self.time_second_line_edit.setEnabled(True)

            elif  i == (str(inter) +"_Disable\n") or i == (str(inter) +"_Disable"):
                try:
                    sftp = ssh_cliente.open_sftp()
                    save = sftp.file("/home/secrouter/tmp/"+ str(inter)+'_save.txt', "r", -1)
                    a = save.readlines()
                    save.close()
                    print(a)
                    c = a[0].split(",")
                    elf.network_line_edit.setText(c[0])
                    self.getaway_line_edit.setText(c[1])
                    self.prefijo_line_edit.setText(c[2])
                    self.dns_server_line_edit.setText(c[3])
                    self.pool_range_start_line_edit.setText(c[4])
                    self.pool_range_stop_line_edit.setText(c[5])
                    self.time_hour_line_edit.setText(c[6])
                    self.time_minute_line_edit.setText(c[7])
                    self.time_second_line_edit.setText(c[8])
                    w = c[9]
                    if w == "check":
                        self.arp_check_box.setChecked(True)
                    else:
                        self.arp_check_box.setChecked(False)
                except:
    #                self.clear()
                    self.enable_disable_button.setText("Disable")
                    self.network_line_edit.setEnabled(False)
                    self.getaway_line_edit.setEnabled(False)
                    self.prefijo_line_edit.setEnabled(False)
                    self.dns_server_line_edit.setEnabled(False)
                    self.pool_range_start_line_edit.setEnabled(False)
                    self.pool_range_stop_line_edit.setEnabled(False)
                    self.time_hour_line_edit.setEnabled(False)
                    self.time_minute_line_edit.setEnabled(False)
                    self.time_second_line_edit.setEnabled(False)

        #    if not(i == (str(inter) +"_Disable\n") or i == (str(inter) +"_Disable")) or not(i == (str(inter) +"_Enable\n") or i == (str(inter) +"_Enable")):
        #        self.network_line_edit.setText("")
        #        self.prefix_line_edit.setText("")
        #        self.getaway_line_edit.setText("")
        #        self.pool_range_start_line_edit.setText("")
        #        self.pool_range_stop_line_edit.setText("")
        #        self.time_hour_line_edit.setText("")
        #        self.time_minute_line_edit.setText("")
        #        self.time_second_line_edit.setText("")
        #        self.arp_check_box.setChecked(False)

    def enable_disable(self):

        inter = self.interface_comboBox.currentText()
        cont = 0
        estado = open("estados.txt", "r")
        var = estado.readlines()
        for i in var:

            if  i == (str(inter) +"_Enable\n"):
                var[cont] = inter +"_Disable"
                #print (var[cont])
                self.enable_disable_button.setText("Enable")
                self.network_line_edit.setEnabled(False)
                self.getaway_line_edit.setEnabled(False)
                self.prefijo_line_edit.setEnabled(False)
                self.dns_server_line_edit.setEnabled(False)
                self.pool_range_start_line_edit.setEnabled(False)
                self.pool_range_stop_line_edit.setEnabled(False)
                self.time_hour_line_edit.setEnabled(False)
                self.time_minute_line_edit.setEnabled(False)
                self.time_second_line_edit.setEnabled(False)
                inter = self.interface_comboBox.currentText()
                network = self.network_line_edit.text()
                getaway  = self.getaway_line_edit.text()
                prefijo = self.prefijo_line_edit.text()
                tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_server/disable.py " +str(inter) +" " +str(network) + " " + str(prefijo) + " " +  str(getaway))
                x = stderr.readlines()
                print(x)

            if  i == (str(inter) +"_Disable\n"):
                var[cont] = inter +"_Enable"
                #print (var[cont])
                self.enable_disable_button.setText("Disable")
                self.network_line_edit.setEnabled(True)
                self.getaway_line_edit.setEnabled(True)
                self.prefijo_line_edit.setEnabled(True)
                self.dns_server_line_edit.setEnabled(True)
                self.pool_range_start_line_edit.setEnabled(True)
                self.pool_range_stop_line_edit.setEnabled(True)
                self.time_hour_line_edit.setEnabled(True)
                self.time_minute_line_edit.setEnabled(True)
                self.time_second_line_edit.setEnabled(True)
                inter = self.interface_comboBox.currentText()
                network = self.network_line_edit.text()
                getaway  = self.getaway_line_edit.text()
                prefijo = self.prefijo_line_edit.text()
                tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_server/enable.py " +str(inter) +" " +str(network) + " " + str(prefijo) + " " +  str(getaway))
                x = stderr.readlines()
                print(x)
            cont += 1
        f = open("estados.txt",'w')
        for i in var:
            if (i != "\n"):
                f.write(i+"\n")
        f.close()

#--------------------------- MODULO APPLY STATIC --------------------------------

    def satatic(self):

        a = self.ip_static_line_edit.text()
        b = self.mac_static_line_edit.text()
        c = self.validar_ip_static_line_edit()
        d = self.validar_mac_static_line_edit()
        e = self.static_comboBox.currentText()
        f = self.host_static_line_edit.text()

        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_server/static_leases.py " +str(e) +" " +str(f) + " " + str(a) + " " +  str(b))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        if c == False or d == False:
            QMessageBox.warning(self,"Advertencia","Uno o varios de los campos son incorrectos.",QMessageBox.Ok)
        else:
            pass
            #####   ENVIAR ####
#------------------------------  DELETE LEASES ---------------------------

    def delete_status (self):
        a = self.status_comboBox.currentText()
        stdin, stdout, stderr = ssh_cliente.exec_command("sudo rm /var/lib/dhcp/dhcpd.leases")
        b = stderr.readlines()
        print(b)
        c = stdout.readlines()
        print(c)
        stdin, stdout, stderr = ssh_cliente.exec_command("sudo /etc/init.d/isc-dhcp-server restart")
        d = stderr.readlines()
        print(d)
        f = stdout.readlines()
        print(f)
        self.leases()
        self.log()


#----------------------------------  STATUS LEASES -------------------------

    def leases(self):
        stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_server/show_leases.py")
        a = stderr.readlines()
        print(a)
        b = stdout.readlines()
        print(b)
        self.columnview.setRowCount(len(b))
        count = 0
        for i in b:
            c = i.split(",")
            item0 = QTableWidgetItem(str(c[0]))
            item1 = QTableWidgetItem(str(c[1]))
            item2 = QTableWidgetItem(str(c[2]))
            item3 = QTableWidgetItem(str(c[3]))
            self.columnview.setItem(count,0,item0)
            self.columnview.setItem(count,1,item1)
            self.columnview.setItem(count,2,item2)
            self.columnview.setItem(count,3,item3)
            count += 1



#----------------------------- LOG STATUS LEASES -------------------------------

    def log(self):
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo cat /var/lib/dhcp/dhcpd.leases")
        a = stdout.readlines()
        for i in a:
            self.log_plain_text.append(str(i))



# ---------------------------- ENABLE/DISABLE CLIENT DHCP ---------------------

    def client_dhcp_combobox(self):
        inter = self.interface_client_comboBox.currentText()
        a = open("client_state.txt","r")
        b = a.readlines()
        a.close()
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        try:
            tdin, stdout, stderr = ssh_cliente.exec_command("sudo sh -c 'cat /var/lib/dhcp/dhclient."+str(inter)+".leases | grep fixed-address | tail -n 1'" )
            x = stdout.readlines()
            a1 = x[0]
            b1 = a1.split(" ")
            c1 = b1[3]
            self.lineEdit_3.setText(str(c1[:-2]))

            tdin, stdout, stderr = ssh_cliente.exec_command("sudo sh -c 'cat /var/lib/dhcp/dhclient."+str(inter)+".leases | grep subnet-mask | tail -n 1'" )
            x = stdout.readlines()
            a2 = x[0]
            b2 = a2.split(" ")
            c2 = b2[4]
            addr = ipcalc.Network(str(c1[:-2]), mask=str(c2[:-2]))
            network_with_cidr = str(addr.guess_network())
            self.lineEdit_2.setText(str(network_with_cidr))

            tdin, stdout, stderr = ssh_cliente.exec_command("sudo sh -c 'cat /var/lib/dhcp/dhclient."+str(inter)+".leases | grep routers | tail -n 1'" )
            x = stdout.readlines()
            a3 = x[0]
            b3 = a3.split(" ")
            c3 = b3[4]
            self.lineEdit_4.setText(str(c3[:-2]))

            tdin, stdout, stderr = ssh_cliente.exec_command("sudo sh -c 'cat /var/lib/dhcp/dhclient."+str(inter)+".leases | grep domain-name-servers | tail -n 1'" )
            x = stdout.readlines()
            a4 = x[0]
            b4 = a4.split(" ")
            c4 = b4[4]
            self.lineEdit_5.setText(str(c4[:-2]))
            #for i in range((len(x) - 14), len(x) , 1):
                #print(x[i])

            for i in b:
                if  i == (str(inter) +"_Enable\n") :
                    self.lineEdit.setText("Active")
                    self.client_dhcp_apply_button.setText("Disable")

                elif  i == (str(inter) +"_Disable\n"):
                    self.lineEdit.setText("Down")
                    self.client_dhcp_apply_button.setText("Enable")
        except:
            pass

    def enable_disable_dhcp(self):

        inter = self.interface_client_comboBox.currentText()
        a = open("client_state.txt","r")
        var2 = a.readlines()
        a.close()

        for i in var2:

            if  i == (str(inter) +"_Enable\n"):
                var2[cont] = inter +"_Disable"
                self.client_dhcp_apply_button.setText("Enable")
                tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_client/dhcp_client.py " + " " + inter + " " +"False")
                x = stderr.readlines()
                #print(x)

            if  i == (str(inter) +"_Disable\n"):
                var2[cont] = inter +"_Enable"
                self.client_dhcp_apply_button.setText("Disable")
                tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp/dhcp_client/dhcp_client.py "+ " " + inter+ " " + "True")
                x = stderr.readlines()
                #print(x)
            cont += 1
        f = open("client_state.txt",'w')
        for i in var:
            if (i != "\n"):
                f.write(i+"\n")
        f.close()

#----------------------------- MODULO RElEASE ---------------------------------
    #True
    def release(self):
        inter = self.interface_client_comboBox.currentText()
        self.lineEdit.setText("Release")
        self.lineEdit_2.setText("0.0.0.0")
        self.lineEdit_3.setText("0.0.0.0")
        self.lineEdit_4.setText("0.0.0.0")
        self.lineEdit_5.setText("0.0.0.0")
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp_client_release_renew.py"+ " " + str(inter) + " " + "True")
        a = stdout.readlines()
        print(a)
# MANDAR ALGUN COMANDO


#--------------------------- MODULO RENEW -------------------------------------
    #False
    def renew(self):
        if self.lineEdit.text() == "Release":
            tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/dhcp_client_release_renew.py"+ " " + str(inter) + " " + "True")
            a = stdout.readlines()
        print(a)
        #MANDAR ALGUN COMANDO


################################################################################
############################### ROUTING  #######################################
################################################################################

    def dns_routing(self):

        a = open("status.txt","r")
        status = a.readlines()
        a.close()
        server1 = self.server1.text()
        server2 = self.server2.text()
        server3 = self.server3.text()
        cache_size = self.cache_size.text()

        if server1 == "": server1 = "8.8.4.4"
        if server2 == "": server2= "8.8.4.4"
        if server3 == "": server3 = "8.8.4.4"
        if cache_size == "": cache_size = 2

        if status[0] == "Disable":
            tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/dns/dns.py "+ str(server1) + " " + str(server2) + " " + str(server3) + " " + str(cache_size))
            a = stderr.readlines()
            print(a)

            w = open("status.txt","w")
            w.write("Enable")
            w.close()

            z = open("config.txt","w")
            z.write(str(server1)+","+str(server2)+","+str(server3)+","+str(cache_size))
            z.close()

            self.enable_routing_Button.setText("Disable")
            self.check_dns()

        if status[0] == "Enable":
            self.enable_routing_Button.setText("Enable")

            tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/dns/dns_disable.py")
            a = stderr.readlines()
            print(a)

            w = open("status.txt","w")
            w.write("Disable")
            w.close()

            self.server1.setEnabled(True)
            self.server2.setEnabled(True)
            self.server3.setEnabled(True)
            self.cache_size.setEnabled(True)
            #self.server1.setText('')
            #self.server2.setText('')
            #self.server3.setText('')
            #self.cache_size.setText('')


    def check_dns(self):
        a = open("status.txt","r")
        status = a.readlines()
        a.close()

        w = open("config.txt","r")
        config = w.readlines()
        w.close()
        print(status[0])
        for i in config:
            var = i.split(",")
            if status[0] == "Enable":
                self.enable_routing_Button.setText("Disable")
                self.server1.setEnabled(False)
                self.server2.setEnabled(False)
                self.server3.setEnabled(False)
                self.cache_size.setEnabled(False)

                self.server1.setText(str(var[0]))
                self.server2.setText(str(var[1]))
                self.server3.setText(str(var[2]))
                self.cache_size.setText(str(var[3]))

            if status[0] == "Disable":
                self.enable_routing_Button.setText("Enable")
                self.server1.setEnabled(True)
                self.server2.setEnabled(True)
                self.server3.setEnabled(True)
                self.cache_size.setEnabled(True)

                self.server1.setText(str(var[0]))
                self.server2.setText(str(var[1]))
                self.server3.setText(str(var[2]))
                self.cache_size.setText(str(var[3]))



    def view_cache(self):
        sftp = ssh_cliente.open_sftp()
        cache =sftp.file('sudo python3 /home/secrouter/parsed_cache.txt', "r", -1)
        View_Cache.launch(cache)

    def flush(self):
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/dns/dns_flush.py")
        a = stderr.readlines()
        print(a)

#-------------------------- PHISICAL INTERFACES ------------------------------

    def apply_phisical_interfaces(self):
        self.radian_button()
        inter = self.phisical_interfaces_comboBox.currentText()
        network = self.network_interfaces.text()
        prefijo = self.pref_interfaces.text()
        ip = self.ip_interfaces.text()
        getaway = self.gateway_interfaces.text()
        f = open("phisical_interface_status.txt","r")
        status = f.readlines()
        f.close()
        cont = 0
        estado = 0
        var = [""]

        for i in status:
            c =i.split(",")
            print(c[0])
            if  c[0] == (str(inter) +"_Enable"):
                f = open("phisical_interface_status.txt","r+")
                d = f.readlines()
                f.seek(0)
                for i in d:
                    a = i.split(",")
                    if a[0] == (str(inter) +"_Enable"):
                        if self.manual_radioButton.isChecked():
                            f.write(str(inter) +"_Disable,"+ str(self.network_interfaces.text()) +","+ str(self.pref_interfaces.text()) +","+ str(self.ip_interfaces.text())+","+ str(self.gateway_interfaces.text())+ ",manual\n")
                        if self.static_radioButton.isChecked():
                            f.write(str(inter) +"_Disable,"+ str(self.network_interfaces.text()) +","+ str(self.pref_interfaces.text()) +","+ str(self.ip_interfaces.text())+","+ str(self.gateway_interfaces.text())+ ",static\n")
                        if self.dhcp_radioButton.isChecked():
                            f.write(str(inter) +"_Disable,"+ str(self.network_interfaces.text()) +","+ str(self.pref_interfaces.text()) +","+ str(self.ip_interfaces.text())+","+ str(self.gateway_interfaces.text())+ ",dhcp\n")
                    else:
                        f.write(i)
                f.truncate()
                f.close()

                if self.manual_radioButton.isChecked():
                    estado = 1
                    self.enable_disable__interfaces_button.setText("Enable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py " + str(0) + " "+ str(1) + " " + str(inter) + " "+ "''"+ " "+ "''"+ " "+ "''"+ " "+ "''")
                    x = stderr.readlines()

                    print(x)
                if self.static_radioButton.isChecked():
                    estado  = 2
                    self.enable_disable__interfaces_button.setText("Enable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py "+ str(0) + " "+ str(2) + " " + str(inter)+ " " + str(network)  + " "+str(prefijo)+ " "+ str(ip)+ " "+ str(getaway))
                    x = stderr.readlines()
                    print(x)
                    self.interface_comboBox.currentText()

                if self.dhcp_radioButton.isChecked():
                    estado = 3
                    self.enable_disable__interfaces_button.setText("Enable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py " + str(0) + " "+ str(3) + " " + str(inter) + " "+ "''"+ " "+ "''"+ " "+ "''"+ " "+ "''")
                    x = stderr.readlines()
                    print(x)


            elif  c[0] == (str(inter) +"_Disable"):
                f = open("phisical_interface_status.txt","r+")
                d = f.readlines()
                f.seek(0)
                for i in d:
                    b = i.split(",")
                    print(b[0])
                    print("estoy antes eth1_disable")
                    if b[0] == (str(inter) +"_Disable"):
                        print("estoy en eth1_disable")
                        if self.manual_radioButton.isChecked():
                            f.write(str(inter) +"_Enable,"+ str(self.network_interfaces.text()) +","+ str(self.pref_interfaces.text()) +","+ str(self.ip_interfaces.text())+","+ str(self.gateway_interfaces.text())+ ",manual\n")
                        if self.static_radioButton.isChecked():
                            f.write(str(inter) +"_Enable,"+ str(self.network_interfaces.text()) +","+ str(self.pref_interfaces.text()) +","+ str(self.ip_interfaces.text())+","+ str(self.gateway_interfaces.text())+ ",static\n")
                        if self.dhcp_radioButton.isChecked():
                            f.write(str(inter) +"_Enable,"+ str(self.network_interfaces.text()) +","+ str(self.pref_interfaces.text()) +","+ str(self.ip_interfaces.text())+","+ str(self.gateway_interfaces.text())+ ",dhcp\n")
                    else:
                        f.write(i)
                f.truncate()
                f.close()
                if self.manual_radioButton.isChecked():
                    estado = 1
                    self.enable_disable__interfaces_button.setText("Disable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py " + str(1) + " "+ str(1) + " " + str(inter) + " "+ "''"+ " "+ "''"+ " "+ "''"+ " "+ "''")
                    x = stderr.readlines()
                    print(x)
                if self.static_radioButton.isChecked():
                    estado  = 2
                    self.enable_disable__interfaces_button.setText("Disable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py "+ str(1) + " "+ str(2) + " " + str(inter)+ " " + str(network)  + " "+str(prefijo)+ " "+ str(ip)+ " "+ str(getaway))
                    x = stderr.readlines()
                    print(x)
                if self.dhcp_radioButton.isChecked():
                    estado = 3
                    self.enable_disable__interfaces_button.setText("Disable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py " + str(1) + " "+ str(3) + " " + str(inter) + " "+ "''"+ " "+ "''"+ " "+ "''"+ " "+ "''")
                    x = stderr.readlines()
                    print(x)


            cont += 1

    def radian_button(self):
        if self.manual_radioButton.isChecked() or self.dhcp_radioButton.isChecked():
            self.network_interfaces.setEnabled(False)
            self.network_interfaces.setText("")
            self.pref_interfaces.setEnabled(False)
            self.pref_interfaces.setText("")
            self.ip_interfaces.setEnabled(False)
            self.ip_interfaces.setText("")
            self.gateway_interfaces.setEnabled(False)
            self.gateway_interfaces.setText("")
        else:
            self.network_interfaces.setEnabled(True)
            self.pref_interfaces.setEnabled(True)
            self.ip_interfaces.setEnabled(True)
            self.gateway_interfaces.setEnabled(True)

    def phisical_interface(self):


        interface = self.phisical_interfaces_comboBox.currentText()
        f = open("phisical_interface_status.txt","r")
        status = f.readlines()
        f.close()

        for i in status:
            a = i.split(",")
            if  a[0] == (str(interface) +"_Enable\n") or a[0] == (str(interface) +"_Enable") :
                print(a[5])
                if a[5] == "manual\n":
                    self.manual_radioButton.setChecked(True)
                if a[5] == "static\n":
                    self.static_radioButton.setChecked(True)
                if a[5] == "dhcp\n":
                    self.dhcp_radioButton.setChecked(True)
                self.network_interfaces.setText(str(a[1]))
                self.pref_interfaces.setText(str(a[2]))
                self.ip_interfaces.setText(str(a[3]))
                self.gateway_interfaces.setText(str(a[4]))
                self.radian_button()
                self.enable_disable__interfaces_button.setText("Disable")


            if  a[0] == (str(interface) +"_Disable\n") or a[0] == (str(interface) +"_Disable"):
                if a[5] == "manual\n":
                    self.manual_radioButton.setChecked(True)
                if a[5] == "static\n":
                    self.static_radioButton.setChecked(True)
                if a[5] == "dhcp\n":
                    self.dhcp_radioButton.setChecked(True)
                self.network_interfaces.setText(str(a[1]))
                self.pref_interfaces.setText(str(a[2]))
                self.ip_interfaces.setText(str(a[3]))
                self.gateway_interfaces.setText(str(a[4]))
                self.radian_button()
                self.enable_disable__interfaces_button.setText("Enable")


    def delete_phisical_interface(self):

        interface = phisical_interfaces_comboBox.text()
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/int_ipconf.py "+ str(0) + " "+ str(2) + " " + str(inter)+ " " + str(network)  + " "+str(prefijo)+ " "+ str(ip)+ " "+ str(getaway))
        a = stderr.readlines()
        print(a)
        pass
#-------------------------------- VLAN ----------- ------------------------------
    def vlan(self):
        id = self.ID_vlan.text()
        g = open("vlan_status.txt","r")
        vlan = g.readlines()
        g.close()
        c = ""
        a = [""]
        b = [""]
        self.vlan_comboBox.clear()
        for i in vlan:
            a = i.split(",")
            c = a[0]

            if a[0] == (str(c[:len(c)-7]) +"_Enable"):
                b = a[0]
                self.vlan_comboBox.addItem(b[:(len(b) - 7)])
                self.enable_disable__vlan_button.setText("Disable")

            if a[0] == (str(c[:len(c)-8]) +"_Disable"):
                b = a[0]
                self.vlan_comboBox.addItem(b[:(len(b) - 8)])
                self.enable_disable__vlan_button.setText("Enable")


    def change_vlan(self):
        g = open("vlan_status.txt","r")
        x = g.readlines()
        g.close()
        a = [""]
        vlan = self.vlan_comboBox.currentText()
        for i in x:
            a =i.split(",")


            if a[0] == (str(vlan) +"_Enable"):
                self.ID_vlan.setEnabled(False)
                self.mtu_vlan.setEnabled(False)
                self.bandto_vlan.setEnabled(False)
                self.network_vlan.setEnabled(False)
                self.pref_vlan.setEnabled(False)
                self.ip_vlan.setEnabled(False)
                self.gateway_vlan.setEnabled(False)
                self.ID_vlan.setText(a[1])
                self.mtu_vlan.setText(a[2])
                self.bandto_vlan.setText(a[3])
                self.network_vlan.setText(a[4])
                self.pref_vlan.setText(a[5])
                self.ip_vlan.setText(a[6])
                self.gateway_vlan.setText(a[7])
                self.enable_disable__vlan_button.setText("Disable")
                if a[8] == "manual\n" or a[8] == "manual":
                    self.manual_vlan_radioButton.setChecked(True)
                if a[8] == "static\n" or a[8] == "static":
                    self.static_vlan_radioButton.setChecked(True)
                if a[8] == "dhcp\n" or a[8] == "dhcp":
                    self.dhcp_vlan_radioButton.setChecked(True)
            if a[0] == (str(vlan) +"_Disable"):
                self.ID_vlan.setEnabled(True)
                self.mtu_vlan.setEnabled(True)
                self.bandto_vlan.setEnabled(True)
                self.network_vlan.setEnabled(True)
                self.pref_vlan.setEnabled(True)
                self.ip_vlan.setEnabled(True)
                self.gateway_vlan.setEnabled(True)
                self.enable_disable__vlan_button.setText("Enable")
                self.ID_vlan.setText(a[1])
                self.mtu_vlan.setText(a[2])
                self.bandto_vlan.setText(a[3])
                self.network_vlan.setText(a[4])
                self.pref_vlan.setText(a[5])
                self.ip_vlan.setText(a[6])
                self.gateway_vlan.setText(a[7])
                if a[8] == "manual\n" or a[8] == "manual":
                    self.manual_vlan_radioButton.setChecked(True)
                if a[8] == "static\n" or a[8] == "static":
                    self.static_vlan_radioButton.setChecked(True)
                if a[8] == "dhcp\n" or a[8] == "dhcp":
                    self.dhcp_vlan_radioButton.setChecked(True)

    def add_vlan(self):
        id = self.ID_vlan.text()
        g = open("vlan_status.txt","r")
        vlan = g.readlines()
        g.close()
        a = False
        b = [" "]
        x = ""
        y = ""
        z = ""
        for i in vlan:
            b = i.split(",")
            if b[0] == ("Vlan." + str(id) +"_Enable") or b[0] == ("Vlan."+ str(id) +"_Disable"):
                a = True
        if id != "":
            if a == False:
                x =self.ID_vlan.text()
                y =self.mtu_vlan.text()
                z =self.bandto_vlan.text()
                network = self.network_vlan.text()
                ip = self.ip_vlan.text()
                pref = self.pref_vlan.text()
                gateway = self.gateway_vlan.text()
                f = open("vlan_status.txt","a")
                if self.manual_vlan_radioButton.isChecked():
                    f.write("Vlan." + str(id) +"_Disable," + str(x) +","+ str(y) +","+ str(z)+","+ str(network)+","+ str(pref) +","+ str(ip)+","+ str(gateway)+",manual\n")
                if self.static_vlan_radioButton.isChecked():
                    f.write("Vlan." + str(id) +"_Disable," + str(x) +","+ str(y) +","+ str(z)+","+ str(network)+","+ str(pref) +","+ str(ip)+","+ str(gateway)+",static\n")
                if self.dhcp_vlan_radioButton.isChecked():
                    f.write("Vlan." + str(id) +"_Disable," + str(x) +","+ str(y) +","+ str(z)+","+ str(network)+","+ str(pref) +","+ str(ip)+","+ str(gateway)+",static\n")

                f.close()
                self.vlan_comboBox.addItem("Vlan." + str(id))
            else:
                QMessageBox.warning(self,"Advertencia","Vlan ya agregada",QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Advertencia","Introducir ID de la Vlan",QMessageBox.Ok)



    def remove_vlan(self):
        vlan = self.vlan_comboBox.currentText()

        f = open("vlan_status.txt","r+")
        d = f.readlines()
        f.seek(0)
        c = 1
        a = [" "]
        print(str(vlan)+"_Enable")

        for i in d:
            a = i.split(",")
            if a[0] == (str(vlan)+"_Enable") or a[0] == (str(vlan)+"_Disable") :
                self.vlan_comboBox.removeItem(c)


            c += 1
        for i in d:
            a = i.split(",")
            if a[0] != (str(vlan)+"_Enable"):
                if a[0] != (str(vlan)+"_Disable"):
                    f.write(i)
        f.truncate()
        f.close()
        self.change_vlan()


    def apply_vlan(self):
        vlan = self.vlan_comboBox.currentText()
        id = self.ID_vlan.text()
        mtu = self.mtu_vlan.text()
        raw = self.bandto_vlan.text()
        network = self.network_vlan.text()
        ip = self.ip_vlan.text()
        pref = self.pref_vlan.text()
        gateway = self.gateway_vlan.text()

        f = open("vlan_status.txt","r+")
        status = f.readlines()
        a = [" "]
        for i in status:
            a = i.split(",")
            if  a[0] == (str(vlan) +"_Enable"):
                f.seek(0)
                for i in status:
                    a = i.split(",")
                    if a[0] != (str(vlan) +"_Enable"):
                        f.write(i)
                    else:
                        if self.manual_vlan_radioButton.isChecked():
                            w = "manual"
                        if self.static_vlan_radioButton.isChecked():
                            w = "static"
                        if self.dhcp_vlan_radioButton.isChecked():
                            w = "dhcp"
                        f.write(str(vlan)+"_Disable"+ "," +str(a[1])+ "," +str(a[2])+ "," +str(a[3])+ "," +str(a[4])+ "," +str(a[5])+ "," +str(a[6]) + "," +str(a[7]) + ","+ str(w) + "\n")

                if self.manual_vlan_radioButton.isChecked():
                    estado = 1
                    self.enable_disable__interfaces_button.setText("Enable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/vlan_ipconf.py " + str(0) + " "+ str(1) + " " + str(raw) + " " + str(id)+" " + str(mtu)+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)
                if self.static_vlan_radioButton.isChecked():
                    estado  = 2
                    self.enable_disable__interfaces_button.setText("Enable")

                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/vlan_ipconf.py "+ str(0) + " "+ str(2) + " " + str(raw)+ " " + str(id)+" " + str(mtu)  + " " + str(network)  + " "+str(pref)+ " "+str(ip)+ " "+ str(gateway))
                    x = stderr.readlines()
                    print(x)
                if self.dhcp_vlan_radioButton.isChecked():
                    estado = 3
                    self.enable_disable__interfaces_button.setText("Enable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/vlan_ipconf.py " + str(0) + " "+ str(3) + " " + str(raw)+ " " + str(id)+" " + str(mtu) + " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)

                self.enable_disable__vlan_button.setText("Enable")
                self.ID_vlan.setEnabled(True)
                self.mtu_vlan.setEnabled(True)
                self.bandto_vlan.setEnabled(True)
                self.network_vlan.setEnabled(True)
                self.pref_vlan.setEnabled(True)
                self.ip_vlan.setEnabled(True)
                self.gateway_vlan.setEnabled(True)

            if  a[0] == (str(vlan) +"_Disable"):
                f.seek(0)
                for i in status:
                    a = i.split(",")
                    if a[0] != (str(vlan) +"_Disable"):
                        f.write(i)
                    else:
                        if self.manual_vlan_radioButton.isChecked():
                            w = "manual"
                        if self.static_vlan_radioButton.isChecked():
                            w = "static"
                        if self.dhcp_vlan_radioButton.isChecked():
                            w = "dhcp"
                        f.write(str(vlan)+"_Enable"+ "," +str(a[1])+ "," +str(a[2])+ "," +str(a[3])+ "," +str(a[4])+ "," +str(a[5])+ "," +str(a[6])+ "," +str(a[7])+ "," +str(w)+ "\n")
                f.truncate()


                self.enable_disable__vlan_button.setText("Disable")
                self.ID_vlan.setEnabled(False)
                self.mtu_vlan.setEnabled(False)
                self.bandto_vlan.setEnabled(False)
                self.network_vlan.setEnabled(False)
                self.pref_vlan.setEnabled(False)
                self.ip_vlan.setEnabled(False)
                self.gateway_vlan.setEnabled(False)

                if self.manual_vlan_radioButton.isChecked():
                    estado = 1
                    self.enable_disable__interfaces_button.setText("Disable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/vlan_ipconf.py " + str(1) + " "+ str(1) + " " + str(raw) + " " + str(id)+" " + str(mtu)+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)
                if self.static_vlan_radioButton.isChecked():
                    estado  = 2
                    self.enable_disable__interfaces_button.setText("Disable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/vlan_ipconf.py "+ str(1) + " "+ str(2) + " " + str(raw)+ " " + str(id)+" " + str(mtu)  + " " + str(network)  + " "+str(pref)+ " "+str(ip)+ " "+ str(gateway))
                    x = stderr.readlines()
                    print(x)
                if self.dhcp_vlan_radioButton.isChecked():
                    estado = 3
                    self.enable_disable__interfaces_button.setText("Disable")
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/vlan_ipconf.py " + str(1) + " "+ str(3) + " " + str(raw)+ " " + str(id)+" " + str(mtu) + " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)

        f.close()


    def radio_vlan_button(self):
        if self.manual_vlan_radioButton.isChecked() or self.dhcp_vlan_radioButton.isChecked():
            self.network_vlan.setEnabled(False)
            self.network_vlan.setText("")
            self.pref_vlan.setEnabled(False)
            self.pref_vlan.setText("")
            self.ip_vlan.setEnabled(False)
            self.ip_vlan.setText("")
            self.gateway_vlan.setEnabled(False)
            self.gateway_vlan.setText("")
        else:

            self.network_vlan.setEnabled(True)
            self.pref_vlan.setEnabled(True)
            self.ip_vlan.setEnabled(True)
            self.gateway_vlan.setEnabled(True)



#-------------------------------- BRIDGE -----------------------------------------
    def bridge(self):
        name = self.name_bridge.text()
        w = self.bridge_comboBox.currentText()
        g = open("bridge_status.txt","r")
        bridge = g.readlines()
        g.close()
        self.bridge_comboBox.clear()
        a = [""]
        b = [""]
        for i in bridge:
            a = i.split(",")
            self.bridge_comboBox.addItem(a[0])



    def change_bridge(self):
        g = open("bridge_status.txt","r")
        x = g.readlines()
        g.close()
        a = [""]
        bridge = self.bridge_comboBox.currentText()
        for i in x:
            a =i.split(",")
            print(a[9])
            if a[1] == ("Enable") and a[0] == str(bridge):
                self.name_bridge.setEnabled(False)
                self.in_to_bridge.setEnabled(False)
                self.stp_bridge.setEnabled(False)
                self.network_bridge.setEnabled(False)
                self.pref_bridge.setEnabled(False)
                self.ip_bridge.setEnabled(False)
                self.gateway_bridge.setEnabled(False)
                self.name_bridge.setText(a[2])
                self.in_to_bridge.setText(a[3])
                self.stp_bridge.setText(a[4])
                self.network_bridge.setText(a[5])
                self.pref_bridge.setText(a[6])
                self.ip_bridge.setText(a[7])
                self.gateway_bridge.setText(a[8])
                self.enable_disable__bridge_button.setText("Disable")
                if a[9] == "manual\n":
                    self.manual_bridge_radioButton.setChecked(True)
                if a[9] == "static\n":
                    self.static_bridge_radioButton.setChecked(True)
                if a[9] == "dhcp\n":
                    self.static_bridge_radioButton.setChecked(True)

            if a[1] == ("Disable") and a[0] == str(bridge):
                self.name_bridge.setEnabled(True)
                self.in_to_bridge.setEnabled(True)
                self.stp_bridge.setEnabled(True)
                self.enable_disable__bridge_button.setText("Enable")
                self.name_bridge.setText(a[2])
                self.in_to_bridge.setText(a[3])
                self.stp_bridge.setText(a[4])
                self.network_bridge.setText(a[5])
                self.pref_bridge.setText(a[6])
                self.ip_bridge.setText(a[7])
                self.gateway_bridge.setText(a[8])
                if a[9] == "manual\n":
                    self.manual_bridge_radioButton.setChecked(True)
                if a[9] == "static\n":
                    self.static_bridge_radioButton.setChecked(True)
                if a[9] == "dhcp\n":
                    self.static_bridge_radioButton.setChecked(True)

    def add_bridge(self):
        name = self.name_bridge.text()
        g = open("bridge_status.txt","r")
        bridge = g.readlines()
        g.close()
        a = False
        b = [" "]
        x = ""
        y = ""
        z = ""
        for i in bridge:
            print(i)
            b = i.split(",")
            print(b[0])
            if b[0] == ("bridge." +str(name)):
                a = True
        if name != "":
            if a == False:
                x =self.name_bridge.text()
                y =self.in_to_bridge.text()
                z =self.stp_bridge.text()
                w = self.network_bridge.text()
                p = self.pref_bridge.text()
                q = self.ip_bridge.text()
                r = self.gateway_bridge.text()

                f = open("bridge_status.txt","a")
                if self.manual_bridge_radioButton.isChecked():
                    f.write("Bridge." + str(name)+ "," +"Disable," + str(x) +","+ str(y) +","+ str(z) +","+str(w)+","+str(p)+","+str(q)+","+ str(r) +",manual\n")
                if self.static_bridge_radioButton.isChecked():
                    f.write("Bridge." + str(name)+ "," +"Disable," + str(x) +","+ str(y) +","+ str(z) +","+str(w)+","+str(p)+","+str(q)+","+ str(r) +",static\n")
                if self.dhcp_bridge_radioButton.isChecked():
                    f.write("Bridge." + str(name)+ "," +"Disable," + str(x) +","+ str(y) +","+ str(z) +","+str(w)+","+str(p)+","+str(q)+","+ str(r) +",dhcp\n")
                f.close()
                self.bridge_comboBox.addItem("Bridge." + str(name))
            else:
                QMessageBox.warning(self,"Advertencia","Bridge ya agregado",QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Advertencia","Introducir nombre del BRIDGE",QMessageBox.Ok)



    def remove_bridge(self):
        bridge = self.bridge_comboBox.currentText()
        f = open("bridge_status.txt","r+")
        d = f.readlines()
        f.seek(0)
        c = 1
        a = [" "]

        for i in d:
            a = i.split(",")
            print(a[0])
            if a[0] == bridge:
                self.bridge_comboBox.removeItem((c+1))
                self.name_bridge.setText("")
                self.in_to_bridge.setText("")
                self.stp_bridge.setText("")
                self.network_bridge.setText("")
                self.pref_bridge.setText("")
                self.ip_bridge.setText("")
                self.gateway_bridge.setText("")

            c += 1
        f.seek(0)
        for i in d:
            a = i.split(",")
            if a[0] != (str(bridge)):
                if a[0] != (str(bridge)):
                    f.write(i)
        f.truncate()
        f.close()
        self.change_bridge()


    def apply_bridge(self):
        bridge = self.bridge_comboBox.currentText()
        int =self.in_to_bridge.text()
        name = self.name_bridge.text()
        stp = self.stp_bridge.text()
        network = self.network_bridge.text()
        pref = self.pref_bridge.text()
        ip = self.ip_bridge.text()
        gateway = self.gateway_bridge.text()

        f = open("bridge_status.txt","r+")
        status = f.readlines()

        a = [" "]

        for i in status:
            a = i.split(",")

            if a[1] == "Enable" and a[0] == bridge:
                self.enable_disable__bridge_button.setText("Enable")
                if self.manual_bridge_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py " + +str(0)+ " " +str(3) + " " + "\'" + int + "\'" + " "+ str(stp) + " "+ str(name) + " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)

                if self.static_bridge_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py " +str(0)+ " "+str(2)  + " "+ "\'" + str(int) + "\'" + " "+ str(stp) + " "+ str(name) +" "+str(network)+" "+str(pref)+" "+str(ip)+" "+str(gateway))
                    x = stderr.readlines()
                    print(x)

                if self.dhcp_bridge_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py " +str(0)+ " " +str(3) + " " + "\'" + int + "\'" + " "+ str(stp) + " "+ str(name) + " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)
                f.seek(0)
                for i in status:
                    b = i.split(",")
                    if  b[0] != (bridge):
                        f.write(i)
                    if b[1] == ("Enable") and b[0] == (bridge):
                        if self.manual_bridge_radioButton.isChecked():
                            w = "manual"
                        if self.static_bridge_radioButton.isChecked():
                            w = "static"
                        if self.dhcp_bridge_radioButton.isChecked():
                            w = "dhcp"
                        f.write("Bridge." + str(name)+ "," +"Disable," + str(name) +","+ str(int) +","+ str(stp)+","+ str(network)+","+ str(pref)+","+ str(ip)+","+ str(gateway)+","+ str(w)+"\n")
                f.truncate()
                f.close()
                self.name_bridge.setEnabled(True)
                self.in_to_bridge.setEnabled(True)
                self.stp_bridge.setEnabled(True)
                self.network_bridge.setEnabled(True)
                self.pref_bridge.setEnabled(True)
                self.ip_bridge.setEnabled(True)
                self.gateway_bridge.setEnabled(True)

            if  a[1] == "Disable" and a[0]== bridge:
                self.enable_disable__bridge_button.setText("Disable")
                if self.manual_bridge_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py "  +str(1)+ " " +str(3) + " " + "\'" + int + "\'" + " "+ str(stp) + " "+ str(name) + " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)

                if self.static_bridge_radioButton.isChecked():
                    print("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py " +str(0)+ " "+str(2)  + " "+ "\'" + str(int) + "\'" + " "+ str(stp) + " "+ str(name) +" "+str(network)+" "+str(pref)+" "+str(ip)+" "+str(gateway))
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py " + " " +str(1)+ " "+str(2)  + " "+ "\'" + str(int) + "\'" + " "+ str(stp) + " "+ str(name) +" "+str(network)+" "+str(pref)+" "+str(ip)+" "+str(gateway))
                    x = stderr.readlines()
                    print(x)

                if self.dhcp_bridge_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/bridge_ipconf.py "  +str(1)+ " " +str(3) + " " + "\'" + int + "\'" + " "+ str(stp) + " "+ str(name) + " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'"+ " "+ "\'\'")
                    x = stderr.readlines()
                    print(x)
                f.seek(0)
                for i in status:
                    b = i.split(",")
                    if  b[0] != (bridge):
                        f.write(i)
                    if b[1] == ("Disable") and b[0] == (bridge):
                        if self.manual_bridge_radioButton.isChecked():
                            w = "manual"
                        if self.static_bridge_radioButton.isChecked():
                            w = "static"
                        if self.dhcp_bridge_radioButton.isChecked():
                            w = "dhcp"
                        f.write("Bridge." + str(name)+ "," +"Enable,"+ str(name) +","+ str(int) +","+ str(stp)+","+ str(network)+","+ str(pref)+","+ str(ip)+","+ str(gateway)+","+ str(w)+"\n")
                f.truncate()
                f.close()
                self.name_bridge.setEnabled(False)
                self.in_to_bridge.setEnabled(False)
                self.stp_bridge.setEnabled(False)
                self.network_bridge.setEnabled(False)
                self.pref_bridge.setEnabled(False)
                self.ip_bridge.setEnabled(False)
                self.gateway_bridge.setEnabled(False)


    def radio_bridge_button(self):
        if self.manual_bridge_radioButton.isChecked() or self.dhcp_bridge_radioButton.isChecked():
            self.network_bridge.setEnabled(False)
            self.network_bridge.setText("")
            self.pref_bridge.setEnabled(False)
            self.pref_bridge.setText("")
            self.ip_bridge.setEnabled(False)
            self.ip_bridge.setText("")
            self.gateway_bridge.setEnabled(False)
            self.gateway_bridge.setText("")
        else:

            self.network_bridge.setEnabled(True)
            self.pref_bridge.setEnabled(True)
            self.ip_bridge.setEnabled(True)
            self.gateway_bridge.setEnabled(True)


    def delete_bridge(self):
        pass
#-------------------------------- STATIC ROUTING -----------------------------------------
    def static_route(self):
        interface = self.interface_static_route.text()
        g = open("static_route_status.txt","r")
        route = g.readlines()
        g.close()
        self.static_route_comboBox.clear()
        a = [""]
        b = [""]
        c = 0
        for i in route:
            a = i.split(",")

            if a[0] == ("SR." + str(c) +"_Enable"):
                b = a[0]
                self.static_route_comboBox.addItem(b[:(len(b) - 7)])
                self.enable_disable_static_route_button.setText("Disable")

            if a[0] == ("SR." + str(c) +"_Disable"):
                b = a[0]
                self.static_route_comboBox.addItem(b[:(len(b) - 8)])
                self.enable_disable_static_route_button.setText("Enable")

            c += 1
    def change_static_route(self):
        g = open("static_route_status.txt","r")
        x = g.readlines()
        g.close()
        a = [""]
        route = self.static_route_comboBox.currentText()
        for i in x:
            print(i)
            a =i.split(",")
            if a[0] == (str(route) +"_Enable"):
                self.interface_static_route.setEnabled(False)
                self.network_static_route.setEnabled(False)
                self.pref_static_route.setEnabled(False)
                self.gateway_static_route.setEnabled(False)
                self.interface_static_route.setText(a[1])
                self.network_static_route.setText(a[2])
                self.pref_static_route.setText(a[3])
                self.gateway_static_route.setText(a[4])
                if a[5]== "bridge\n":
                    self.bridge_static_route_radioButton.setChecked(True)
                if a[5]=="vlan\n":
                    self.vlan_static_route_radioButton.setChecked(True)
                if a[5]=="interface\n":
                    self.inter_static_route_radioButton.setChecked(True)
                self.enable_disable_static_route_button.setText("Disable")
            if a[0] == (str(route) +"_Disable"):
                self.interface_static_route.setEnabled(True)
                self.network_static_route.setEnabled(True)
                self.pref_static_route.setEnabled(True)
                self.gateway_static_route.setEnabled(True)
                self.enable_disable_static_route_button.setText("Enable")
                self.interface_static_route.setText(a[1])
                self.network_static_route.setText(a[2])
                self.pref_static_route.setText(a[3])
                self.gateway_static_route.setText(a[4])
                if a[5]== "bridge\n":
                    self.bridge_static_route_radioButton.setChecked(True)
                if a[5]=="vlan\n":
                    self.vlan_static_route_radioButton.setChecked(True)
                if a[5]=="interface\n":
                    self.inter_static_route_radioButton.setChecked(True)

    def add_static_route(self):

        g = open("static_route_status.txt","r")
        route = g.readlines()
        g.close()
        a = False
        b = [" "]
        x = ""
        y = ""
        z = ""
        c = 0
        for i in route:
            c += 1

        if (self.interface_static_route.text() != "") or (self.network_static_route.text() != "") or (self.pref_static_route.text() != "") or (self.gateway_static_route.text() != ""):
            if a == False:
                x =self.interface_static_route.text()
                y =self.network_static_route.text()
                w = self.gateway_static_route.text()
                q = self.pref_static_route.text()
                if self.bridge_static_route_radioButton.isChecked():
                    t = "bridge"
                if self.vlan_static_route_radioButton.isChecked():
                    t = "vlan"
                if self.inter_static_route_radioButton.isChecked():
                    t = "interface"

                f = open("static_route_status.txt","a")
                f.write("SR." + str(c) +"_Disable," + str(x) +","+ str(y)+","+ str(q) +","+ str(w)+","+ str(t))
                f.close()
                self.static_route_comboBox.addItem("SR." + str(c))
            else:
                QMessageBox.warning(self,"Advertencia","Ruta Estatica ya agregada",QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Advertencia","Campo vacio",QMessageBox.Ok)

        c += 1

    def remove_static_route(self):
        route = self.static_route_comboBox.currentText()

        f = open("static_route_status.txt","r+")
        d = f.readlines()
        f.seek(0)
        c = 1
        a = [" "]

        for i in d:
            a = i.split(",")
            if a[0] == (str(route)+"_Enable") or a[0] == (str(route)+"_Disable") :
                self.static_route_comboBox.removeItem(c)


            c += 1
        f.seek(0)
        for i in d:
            a = i.split(",")
            if a[0] != (str(route)+"_Enable"):
                if a[0] != (str(route)+"_Disable"):
                    f.write(i)
        f.truncate()
        f.close()
        self.change_static_route()


    def apply_static_route(self):
        route = self.static_route_comboBox.currentText()
        int = self.interface_static_route.text()
        network = self.network_static_route.text()
        pref = self.pref_static_route.text()
        gw = self.gateway_static_route.text()[:-1]
        f = open("static_route_status.txt","r+")
        status = f.readlines()
        a = [" "]
        f.close()
        for i in status:
            a = i.split(",")
            if  a[0] == (str(route) +"_Enable"):

                if self.inter_static_route_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_route.py  " +str(0)+ " " +str(1) + " " +  str(int)  + " "+ str(network) + " "+ str(pref) + " "+ str(gw))
                    x = stderr.readlines()
                    y = stdout.readlines()
                    print(x)
                    print(y)

                if self.vlan_static_route_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_route.py  " +str(0)+ " " +str(2) + " " +  str(int)  + " "+ str(network) + " "+ str(pref) + " "+ str(gw))
                    x = stderr.readlines()
                    print(x)

                if self.bridge_static_route_radioButton.isChecked():
                    tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_route.py  " +str(0)+ " " +str(3) + " " +  str(int)  + " "+ str(network) + " "+ str(pref) + " "+ str(gw))
                    x = stderr.readlines()
                    print(x)
                f = open("static_route_status.txt","r+")
                status = f.readlines()
                a = [" "]

                f.seek(0)
                for i in status:
                    b = i.split(",")
                    if  b[0] != (str(route) +"_Enable"):
                        f.write(i)
                    if b[0] == (str(route) +"_Enable"):
                        if self.bridge_static_route_radioButton.isChecked():
                            t = "bridge"
                        if self.vlan_static_route_radioButton.isChecked():
                            t = "vlan"
                        if self.inter_static_route_radioButton.isChecked():
                            t = "interface"
                        f.write(str(route) + "_Disable,"+ str(int) +"," + str(network) +","+ str(pref) +","+ str(gw)+","+ str(t)+"\n")
                    f.truncate()
                f.close()

                self.enable_disable_static_route_button.setText("Enable")
                self.interface_static_route.setEnabled(True)
                self.network_static_route.setEnabled(True)
                self.pref_static_route.setEnabled(True)
                self.gateway_static_route.setEnabled(True)


            if  a[0] == (str(route) +"_Disable"):
                if self.inter_static_route_radioButton.isChecked():

                    stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_route.py" +" " +str(1) +" "+ str(1)+ " "+ str(int)+ " "+str(network)+ " "+ str(pref) + " " + str(gw))
                    x = stderr.readlines()
                    y = stdout.readlines()
                    print(x)
                    print(y)

                if self.vlan_static_route_radioButton.isChecked():
                    stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_route.py  " +str(1)+ " " +str(2) + " " +  str(int)  + " "+ str(network) + " "+ str(pref) + " "+ str(gw))
                    x = stderr.readlines()
                    print(x)

                if self.bridge_static_route_radioButton.isChecked():
                    stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_route.py  " +str(1)+ " " +str(3) + " " +  str(int)  + " "+ str(network) + " "+ str(pref) + " "+ str(gw))
                    x = stderr.readlines()
                    print(x)

                f = open("static_route_status.txt","r+")
                status = f.readlines()
                a = [" "]
                f.seek(0)


                for i in status:
                    b = i.split(",")
                    if  b[0] != (str(route) +"_Disable"):
                       f.write(i)
                    if b[0] == (str(route) +"_Disable"):
                        if self.bridge_static_route_radioButton.isChecked():
                            t = "bridge"
                        if self.vlan_static_route_radioButton.isChecked():
                            t = "vlan"
                        if self.inter_static_route_radioButton.isChecked():
                            t = "interface"
                        f.write(str(route) + "_Enable,"+ str(int) +"," + str(network) +","+ str(pref) +","+ str(gw)+","+str(t)+"\n")
                    f.truncate()
                f.close()
                self.enable_disable_static_route_button.setText("Disable")
                self.interface_static_route.setEnabled(False)
                self.network_static_route.setEnabled(False)
                self.pref_static_route.setEnabled(False)
                self.gateway_static_route.setEnabled(False)



#-------------------------------- ARP  -----------------------------------------
    def arp(self):
        interface = self.arp_comboBox.currentText()
        g = open("arp_status.txt","r")
        arp = g.readlines()
        g.close()

        a = [""]
        b = [""]
        c = 0
        for i in arp:
            a = i.split(",")

            if a[0] == ("Arp." + str(c) +"_Enable"):
                b = a[0]
                self.arp_comboBox.addItem(b[:(len(b) - 7)])
                self.enable_disable_arp_button.setText("Disable")

            if a[0] == ("Arp." + str(c) +"_Disable"):
                b = a[0]
                self.arp_comboBox.addItem(b[:(len(b) - 8)])
                self.enable_disable_arp_button.setText("Enable")

            c += 1
    def change_arp(self):
        g = open("arp_status.txt","r")
        x = g.readlines()
        g.close()
        a = [""]
        arp = self.arp_comboBox.currentText()
        for i in x:
            print(i)
            a =i.split(",")
            if a[0] == (str(arp) +"_Enable"):
                self.interface_arp.setEnabled(False)
                self.ip_arp.setEnabled(False)
                self.mac_arp.setEnabled(False)
                self.interface_arp.setText(a[1])
                self.ip_arp.setText(a[2])
                self.mac_arp.setText(a[3])
                if a[4] == "interface\n":
                    self.inter_arp_radioButton.setChecked(True)
                if a[4] == "vlan\n":
                    self.vlan_arp_radioButton.setChecked(True)
                if a[4] == "bridge\n":
                    self.bridge_arp_radioButton.setChecked(True)
                self.enable_disable_arp_button.setText("Disable")

            if a[0] == (str(arp) +"_Disable"):
                self.interface_arp.setEnabled(True)
                self.ip_arp.setEnabled(True)
                self.mac_arp.setEnabled(True)
                self.enable_disable_arp_button.setText("Enable")
                self.ip_arp.setText(a[2])
                self.mac_arp.setText(a[3])
                self.interface_arp.setText(a[1])
                if a[4] == "interface\n":
                    self.inter_arp_radioButton.setChecked(True)
                if a[4] == "vlan\n":
                    self.vlan_arp_radioButton.setChecked(True)
                if a[4] == "bridge\n":
                    self.bridge_arp_radioButton.setChecked(True)

    def add_arp(self):
        ip = self.ip_arp.text()
        mac = self.mac_arp.text()
        g = open("arp_status.txt","r")
        route = g.readlines()
        g.close()
        a = False
        b = [" "]
        x = ""
        y = ""
        z = ""
        c = 0
        for i in route:
            c += 1
        if (ip != "") or (mac != ""):
            if a == False:
                x =self.interface_arp.text()
                y =self.ip_arp.text()
                z =self.mac_arp.text()
                f = open("arp_status.txt","a")
                if self.inter_arp_radioButton.isChecked():
                    w = "interface"
                if self.vlan_arp_radioButton.isChecked():
                    w= "vlan"
                if self.bridge_arp_radioButton.isChecked():
                    w= "bridge"
                f.write("Arp." + str(c) +"_Disable," + str(x) +","+ str(y) +","+ str(z) +"," + str(w))
                f.close()
                self.arp_comboBox.addItem("Arp." + str(c))
            else:
                QMessageBox.warning(self,"Advertencia","ARP ya agregada",QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Advertencia","Campo vacio",QMessageBox.Ok)

        c += 1

    def remove_arp(self):
        arp = self.arp_comboBox.currentText()

        f = open("arp_status.txt","r+")
        d = f.readlines()
        f.seek(0)
        c = 1
        a = [" "]

        for i in d:
            a = i.split(",")
            if a[0] == (str(arp)+"_Enable") or a[0] == (str(arp)+"_Disable") :
                self.arp_comboBox.removeItem(c)

            c += 1
        f.seek(0)
        for i in d:
            a = i.split(",")
            if a[0] != (str(arp)+"_Enable"):
                if a[0] != (str(arp)+"_Disable"):
                    f.write(i)
        f.truncate()
        f.close()
        self.change_arp()


    def apply_arp(self):
        arp = self.arp_comboBox.currentText()
        int = self.interface_arp.text()
        ip = self.ip_arp.text()
        mac = self.mac_arp.text()[:-1]
        f = open("arp_status.txt","r+")
        status = f.readlines()
        a = [" "]
        for i in status:
            a = i.split(",")
            if  a[0] == (str(arp) +"_Enable"):
                    if self.inter_arp_radioButton.isChecked():
                        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_arp.py " +str(0)+ " " +str(1) + " " +  str(int)  + " "+ str(ip) + " "+ str(mac))
                        x = stderr.readlines()
                        y = stdout.readlines()
                        print(x)
                        print(y)

                    if self.vlan_arp_radioButton.isChecked():
                        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_arp.py " +str(0)+ " " +str(2) + " " +  str(int)  + " "+ str(ip) + " "+ str(mac))
                        x = stderr.readlines()
                        print(x)

                    if self.bridge_arp_radioButton.isChecked():
                        tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_arp.py " +str(0)+ " " +str(3) + " " +  str(int)  + " "+ str(ip) + " "+ str(mac))
                        x = stderr.readlines()
                        print(x)
                    f = open("arp_status.txt","r+")
                    status = f.readlines()
                    a = [" "]

                    f.seek(0)
                    for i in status:
                        b = i.split(",")
                        if  b[0] != (str(arp) +"_Enable"):
                            f.write(i)
                        if b[0] == (str(arp) +"_Enable"):
                            if self.inter_arp_radioButton.isChecked():
                                w = "interface"
                            if self.vlan_arp_radioButton.isChecked():
                                w= "vlan"
                            if self.bridge_arp_radioButton.isChecked():
                                w= "bridge"
                            f.write(str(arp) + "_Disable,"+ str(int) +"," + str(ip) +","+ str(mac)+","+ str(w)+ "\n")
                        f.truncate()
                    f.close()

                    self.enable_disable_arp_button.setText("Enable")
                    self.interface_arp.setEnabled(True)
                    self.ip_arp.setEnabled(True)
                    self.mac_arp.setEnabled(True)



            if  a[0] == (str(arp) +"_Disable"):

                if self.inter_arp_radioButton.isChecked():
                    stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_arp.py " +str(1)+ " " +str(1) + " " +  str(int)  + " "+ str(ip) + " "+ str(mac))
                    x = stderr.readlines()
                    y = stdout.readlines()
                    print(x)
                    print(y)

                if self.vlan_arp_radioButton.isChecked():
                    stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_arp.py "  +str(1)+ " " +str(2) + " " +  str(int)  + " "+ str(ip) + " "+ str(mac))
                    x = stderr.readlines()
                    print(x)

                if self.bridge_arp_radioButton.isChecked():
                    stdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/eth_route/int_conf/static_arp.py "+str(1)+ " " +str(3) + " " +  str(int)  + " "+ str(ip) + " "+ str(mac))
                    x = stderr.readlines()
                    print(x)

                f = open("arp_status.txt","r+")
                status = f.readlines()
                a = [" "]
                f.seek(0)


                for i in status:
                    b = i.split(",")
                    if  b[0] != (str(arp) +"_Disable"):
                       f.write(i)
                    if b[0] == (str(arp) +"_Disable"):
                        if self.inter_arp_radioButton.isChecked():
                            w = "interface"
                        if self.vlan_arp_radioButton.isChecked():
                            w= "vlan"
                        if self.bridge_arp_radioButton.isChecked():
                            w= "bridge"
                        f.write(str(arp) + "_Enable,"+ str(int) +"," + str(ip) +","+ str(mac)+","+ str(w)+"\n")
                    f.truncate()
                f.close()
                self.enable_disable_arp_button.setText("Disable")
                self.interface_arp.setEnabled(False)
                self.ip_arp.setEnabled(False)
                self.mac_arp.setEnabled(False)



################################################################################
############################### FIREWALL #######################################
################################################################################


# -------------------------------- FILTER ---------------------------------------

    def apply_filter (self):
         src_addr = ""
         dst_addr = ""
         iprange_match = ""
         tcp_match = ""
         udp_match = ""
         icmp_type = ""
         multi_match = ""
         limit_match = ""
         time_match = ""
         state = ""
         string_match = ""
         mac = ""
         ttl_match = ""
         geoip = ""
         comment = ""
         super_match = ""
         in_if =""
         out_if = ""
         def sma(value,salt,is_not):
             salt = salt + ' '
             return salt + value + ' '  if is_not == False else salt + '! ' + value + ' '
     # ------------------------------- FILTER SUB-CATEGORY -------------------------------
     # --- MATCHES ---
         # IP match
         ## Source Address
         if self.e_IP_Match.isChecked():

            if self.e_src_addr.isChecked():

                 src_addr = self.src_addr_line_edit.text()
                 src_addr = sma(src_addr,'-s',self.src_addr_not.isChecked())
            else:
                 src_addr = ''
             ## Destination Address
            if self.e_dst_addr.isChecked():
                 dst_addr = self.dst_addr_line_edit.text()
                 dst_addr = sma(dst_addr,'-d',self.dst_addr_not.isChecked())
            else:
                 dst_addr = ''
             ## iprange sub-match
             ### Source Address Range
            if self.e_src_addr_range.isChecked() or self.e_dst_addr_range.isChecked():
                if self.e_src_addr_range.isChecked():
                     src_addr_range = self.src_addr_range_line_edit.text()
                     src_addr_range = sma(src_addr_range,'--src-range',self.src_addr_range_not.isChecked())
                else:
                     src_addr_range = ''

                 ### Destination Address Range
                if self.e_dst_addr_range.isChecked():
                     dst_addr_range = self.dst_addr_range_line_edit.text()
                     dst_addr_range = sma(dst_addr_range,'--dst-range',self.dst_addr_range_not.isChecked())
                else:
                     dst_addr_range = ''
                iprange_match = '-m iprange ' + src_addr_range  + dst_addr_range
            else:
                iprange_match = ''


         else:
             ip_rule = ''

         # IP match END

         # Port match

         ## TCP match
         if self.e_tcp_Match.isChecked():
         ### Source Port
             if self.e_src_port_tcp.isChecked():
                 src_port_tcp = self.src_port_tcp_line_edit.text()
                 src_port_tcp = sma(src_port_tcp,'--sport',self.src_port_tcp_not.isChecked())
             else:
                 src_port_tcp = ''
             ### Destination Port
             if self.e_dst_port_tcp.isChecked():
                 dst_port_tcp = self.dst_port_tcp_line_edit.text()
                 dst_port_tcp = sma(dst_port_tcp,'--dport',self.src_port_tcp_not.isChecked())
             else:
                 dst_port_tcp = ''
             ### TCP Flag
             if self.e_tcp_flags.isChecked():
                 tcp_flags = self.tcp_flags_line_edit.text()
                 tcp_flags = sma(tcp_flags,'--tcp-flags ',self.tcp_flags_not.isChecked())
             else:
                 tcp_flags = ''

             tcp_match = '-p tcp -m tcp ' + src_port_tcp  + dst_port_tcp + tcp_flags

         else:
             tcp_match = ''


         ## UDP match
         ### Source Port
         if self.e_udp_Match.isChecked():
             if self.e_src_port_udp.isChecked():
                 src_port_udp = self.src_port_udp_line_edit.text()
                 src_port_udp = sma(src_port_udp,'--sport',self.src_port_udp_not.isChecked())
             else:
                 src_port_udp = ''
             ### Destination Port
             if self.e_dst_port_udp.isChecked():
                 dst_port_udp = self.dst_port_udp_line_edit.text()
                 dst_port_udp = sma(dst_port_udp,'--dport',self.dst_port_udp_not.isChecked())
             else:
                 dst_port_udp = ''

             udp_match = '-p udp -m udp ' + src_port_udp  + dst_port_udp

         ## icmp match
         ### icmp type
         if self.e_icmp_type.isChecked():
             icmp_type = self.icmp_type_line_edit.text()
             icmp_type = sma(icmp_type,'-p icmp -m icmp --icmp-type',self.icmp_type_not.isChecked())
         else:
             icmp_type = ''

         ## Multiport match
         if self.e_multi_port.isChecked():
             if self.e_src_port_multi.isChecked() or self.e_dst_port_multi.isChecked():
                 protocol = self.protocol_combobox.currentText() + ' '
             else:
                QMessageBox.warning(self,"Advertencia","debe poseer algun puerto de destino u origen",QMessageBox.Ok)
                self.e_multi_port.Checked(False)
             ### Source Port
             if self.e_src_port_multi.isChecked():
                 src_port_multi = self.src_port_multi_line_edit.text()
                 src_port_multi = sma(src_port_multi,'--sport',self.src_port_multi_not.isChecked())
             else:
                 src_port_multi = ''
             ### Destination Port
             if self.e_dst_port_multi.isChecked():
                 dst_port_multi = self.dst_port_multi_line_edit.text()
                 dst_port_multi = sma(dst_port_multi,'--dport',self.dst_port_multi_not.isChecked())
             else:
                 dst_port_multi = ''

             multi_match = '-p ' + protocol + '-m multiport ' +  src_port_multi  +  dst_port_multi
         else:
             multi_match = ''
         ## Multiport match END
         # Port match END

         # State match
         if self.e_state.isChecked():
             state = self.state_line_edit.text()
             state = sma(state,'-m state --state', self.state_not.isChecked())
         else:
             state = ''
         # State match END

         # Limit match
         ## Limit Rate
         if self.e_limit.isChecked():
             if self.e_limit_rate.isChecked():
                 limit_rate = self.limit_rate_line_edit.text()
                 limit_rate ='--limit-rate ' + limit_rate + ' '
             else:
                 limit_rate = ''
             ## Limit Burst
             if self.e_limit_burst.isChecked():
                 limit_burst = self.limit_burst_line_edit.text()
                 limit_burst = 'limit-burst ' + limit_burst + ' '
             else:
                 limit_burst = ''

             limit_match = '-m limit ' + limit_rate + limit_burst
         else:
             limit_match = ''
         # Limit match END

         if self.e_time.isChecked():
             # Date Start
             if self.e_date_start.isChecked():
                 date_start = self.date_start_line_edit.text()
                 date_start = '--datestart ' + date_start + ' '
             else:
                 date_start = ''
             # Date Stop
             if self.e_date_stop.isChecked():
                 date_stop = self.date_stop_line_edit.text()
                 date_stop = '--datestop ' + date_stop + ' '
             else:
                 date_stop = ''

             # Time Start
             if self.e_time_start.isChecked():
                 time_start = self.time_start_line_edit.text()
                 time_start = '--timestart ' + time_start + ' '
             else:
                 time_start = ''
             # Time Stop
             if self.e_time_stop.isChecked():
                 time_stop = self.time_stop_line_edit.text()
                 time_stop = '--timestop ' + time_stop + ' '
             else:
                 time_stop = ''

             # Month Days
             if self.e_month_days.isChecked():
                 month_days = self.month_days_line_edit.text()
                 month_days = sma(month_days,'--monthdays',self.month_days_not.isChecked())
             else:
                 month_days = ''
             # Week Days
             if self.e_week_days.isChecked():
                 week_days = self.week_days_line_edit.text()
                 week_days = sma(week_days,'--weekdays',self.week_days_not.isChecked())
             else:
                 week_days = ''

             time_match = '-m time '+ date_start  + date_stop + time_start + time_stop + month_days + week_days
         else:
             time_match = ''
         # Time Match END
         # String Match
         if self.e_string.isChecked():
             # Algorithm
             if self.e_algo.isChecked():
                 algo = '--algo ' + self.algo_combobox.currentText() + ' '
             else:
                 algo = ''
             # From
             if self.e_from_data.isChecked():
                 from_data = self.from_data_line_edit.text()
                 from_data = '--from ' + from_data + ' '
             else:
                 from_data = ''

             # To
             if self.e_to_data.isChecked():
                 to_data = self.to_data_line_edit.text()
                 to_data = '--to ' + to_data + ' '
             else:
                 time_start = ''
             # String
             if self.e_check_string.isChecked():
                check_string = self.check_string_line_edit.text()
                check_string = sma(check_string,'--string',self.check_string_not.isChecked())
             else:
                 check_string = ''

             string_match = '-m string ' + algo + from_data  + to_data  + check_string
         else:
             string_match = ''

         # String Match END

         # MAC Match
         if self.e_mac.isChecked():
            mac = self.mac_line_edit.text()
            mac = sma(mac,'-m mac --mac-source',self.mac_not.isChecked()) # ONLY FOR INPUT AND FORWARD CHAIN!
         else:
             mac = ''
         # MAC Match END

         # TTL Match
         # -m ttl --ttl-eq --ttl-gt --ttl-lt
         if self.e_ttl.isChecked():
             ## TTL equal
             if self.e_ttl_eq.isChecked():
                ttl_eq = self.ttl_eq_line_edit.text()
                ttl_eq = sma(ttl_eq,'--ttl-eq',self.ttl_eq_not.isChecked())
             else:
                 ttl_eq  = ''
             ## TTL greater than
             if self.e_ttl_gt.isChecked():
                 ttl_gt = self.ttl_gt_line_edit.text()
                 ttl_gt = '--ttl-gt ' + ttl_gt + ' '
             else:
                 ttl_gt = ''
             ## TTL less than
             if self.e_ttl_lt.isChecked():
                 ttl_lt = self.ttl_lt_line_edit.text()
                 ttl_lt = '--ttl-lt ' + ttl_lt + ' '
             else:
                 ttl_lt = ''

             ttl_match = '-m ttl '  +ttl_eq  + ttl_gt  + ttl_lt
         else:
             ttl_match = ''
         # TTL Match END
         # geoIP Match
         if self.e_geoip.isChecked():

            geoip = self.geoip_line_edit.text()
            geoip = sma(geoip,'-m geoip --source-country',self.geoip_not.isChecked())
         else:
            geoip  = ''

         # geoIP Match END

         # comment Match
         if self.e_comment.isChecked():
            comment = self.comment_line_edit.text()
            comment = '-m comment --comment ' + '\'' +comment + '\'' + ' '
         else:
            comment  = ''

         # geoIP Match END

         # FILTER
         if self.rule_combobox.currentText() == "ADD in line":
             line = self.rule_line_edit.text()
             chain = self.chain_combox.currentText()
             var_rule = "-I " + line + " " + chain + " "
         if self.rule_combobox.currentText() == "APPEND":
             var_rule = "-A " + self.chain_combox.currentText() + " "
         if self.rule_combobox.currentText() == "INSERT":
             var_rule = "-I 1 " + self.chain_combox.currentText() + " "
        #TARGET
         x = self.action_combobox.currentText()
         print(x)
         if x == "JUMP":
             action = '-j ' + self.chain_target_action.currentText()
         if x == "REJECT":
             action = '-j REJECT --reject-with ' + self.reject_combobox.currentText()
         if x == "LOG":
             action = '-j LOG --log-level ' + self.log_combobox.currentText() + ' --log-prefix ' + '\"' + self.prefix_line_edit.text() + '\"'
         if x == "ACCEPT":
             action = '-j ACCEPT'
         if x == "DROP":
             action = "-j DROP"
         if x == "RETURN":
             action = "-j RETURN"

         if self.chain_combox.currentText() == "INPUT":
             out_if = ""
             if self.e_in.isChecked():
                  if self.in_not.isChecked():
                      in_if = "-i " + '! '+ self.in_combobox.currentText() + " "
                  else:
                      in_if = "-i " + self.in_combobox.currentText() + " "
             else:
                  in_if =""

         if self.chain_combox.currentText() == "OUTPUT":
              in_if == ""
              if self.e_out.isChecked():
                  if self.out_not.isChecked():
                      out_if = "-o " + '! '+ self.out_combobox.currentText() + " "
                  else:
                      out_if = "-o " + self.out_combobox.currentText() + " "
              else:
                  out_if =""

         if self.chain_combox.currentText() == "FORWARD":
              if self.e_in.isChecked():

                  if self.in_not.isChecked():
                      in_if = "-i " + '! '+ self.in_combobox.currentText() + " "
                  else:
                      in_if = "-i " + self.in_combobox.currentText() + " "
              else:
                  in_if = ""
              if self.e_out.isChecked():

                  if self.out_not.isChecked():
                      out_if = "-o " + '! '+ self.out_combobox.currentText() + " "
                  else:
                      out_if = "-o " + self.out_combobox.currentText() + + " "
              else:
                  out_if = ""



         # General definition of matches
         if self.e_comment.isChecked() or self.e_geoip.isChecked() or self.e_ttl.isChecked()  or self.e_string.isChecked() or  self.e_time.isChecked() or  self.e_mac.isChecked() or self.e_limit.isChecked() or self.e_state.isChecked() or self.e_tcp_Match.isChecked() or self.e_multi_port.isChecked() or self.e_udp_Match.isChecked() or self.e_icmp_type.isChecked() or self.e_IP_Match.isChecked():
             super_match = src_addr  + dst_addr + iprange_match + tcp_match  + udp_match + icmp_type
             super_match = super_match  + multi_match  +limit_match+ time_match + state + string_match  + mac + ttl_match
             super_match = super_match  + geoip + comment
             rule = var_rule + in_if + out_if + super_match + action

         print(rule)
         w = self.chain_combox.currentText()
         print(str(rule) + ' ' + str(w))
         tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/firewall/firewall_controller.py " + '\'' + str(rule) + '\'' +    ' '+ "filter" +    ' ' +  '\'' + str(w) + '\'' )
         x = stderr.readlines()
         y = stdout.readlines()
         print(x)
         print(y)

    def change_chain_filter(self):

        if self.chain_combox.currentText() == "INPUT":
            self.e_in.setEnabled(True)
            self.e_out.setEnabled(False)
            self.e_mac.setEnabled(True)
            self.e_geoip.setEnabled(True)
        if self.chain_combox.currentText() == "OUTPUT":
            self.e_out.setEnabled(True)
            self.e_in.setEnabled(False)
            self.e_mac.setEnabled(False)
            self.e_geoip.setEnabled(False)
        if self.chain_combox.currentText() == "FORWARD":
            self.e_in.setEnabled(True)
            self.e_out.setEnabled(True)
            self.e_mac.setEnabled(True)
            self.e_geoip.setEnabled(False)
        if self.chain_combox.currentText() == " " or self.chain_combox.currentText() == "USER DEFINED":
            self.e_in.setEnabled(False)
            self.e_out.setEnabled(False)
            self.e_mac.setEnabled(False)
            self.e_geoip.setEnabled(False)

    def check_in_out_filter(self):
        if self.e_in.isChecked():
            self.in_not.setEnabled(True)
            self.in_combobox.setEnabled(True)
        else:
            self.in_not.setEnabled(False)
            self.in_combobox.setEnabled(False)

        if self.e_out.isChecked():
            self.out_not.setEnabled(True)
            self.out_combobox.setEnabled(True)
        else:
            self.out_not.setEnabled(False)
            self.out_combobox.setEnabled(False)

    def change_rule(self):

        if self.rule_combobox.currentText() == "ADD in line":
            self.rule_line_edit.setEnabled(True)
        else:
            self.rule_line_edit.setEnabled(False)
    def change_action(self):
        if self.action_combobox.currentText() == "REJECT":
            self.reject_combobox.setEnabled(True)
        else:
            self.reject_combobox.setEnabled(False)

        if self.action_combobox.currentText() == "LOG":
            self.log_combobox.setEnabled(True)
            self.prefix_line_edit.setEnabled(True)
        else:
            self.log_combobox.setEnabled(False)
            self.prefix_line_edit.setEnabled(False)
        if self.action_combobox.currentText() == "JUMP":
            self.chain_target_action.setEnabled(True)
        else:
            self.chain_target_action.setEnabled(False)
    def change_mac(self):
        if self.e_mac.isChecked():
            self.mac_not.setEnabled(True)
            self.mac_line_edit.setEnabled(True)
        else:
            self.mac_not.setEnabled(False)
            self.mac_line_edit.setEnabled(False)
    def change_geoip(self):
        if self.e_geoip.isChecked():
            self.geoip_not.setEnabled(True)
            self.geoip_line_edit.setEnabled(True)
        else:
            self.geoip_not.setEnabled(False)
            self.geoip_line_edit.setEnabled(False)

    def change_ip(self):
        if self.e_IP_Match.isChecked():
            self.e_src_addr.setEnabled(True)
            self.e_dst_addr.setEnabled(True)
            self.e_src_addr_range.setEnabled(True)
            self.e_dst_addr_range.setEnabled(True)

            if self.e_src_addr.isChecked():
                self.src_addr_not.setEnabled(True)
                self.src_addr_line_edit.setEnabled(True)
            else:
                self.src_addr_not.setEnabled(False)
                self.src_addr_line_edit.setEnabled(False)

            if self.e_dst_addr.isChecked():
                self.dst_addr_not.setEnabled(True)
                self.dst_addr_line_edit.setEnabled(True)
            else:
                self.dst_addr_not.setEnabled(False)
                self.dst_addr_line_edit.setEnabled(False)

            if self.e_src_addr_range.isChecked():
                self.src_addr_range_not.setEnabled(True)
                self.src_addr_range_line_edit.setEnabled(True)
            else:
                self.src_addr_range_not.setEnabled(False)
                self.src_addr_range_line_edit.setEnabled(False)

            if self.e_dst_addr_range.isChecked():
                self.dst_addr_range_not.setEnabled(True)
                self.dst_addr_range_line_edit.setEnabled(True)
            else:
                self.dst_addr_range_not.setEnabled(False)
                self.dst_addr_range_line_edit.setEnabled(False)
        else:
            self.e_src_addr.setEnabled(False)
            self.e_dst_addr.setEnabled(False)
            self.e_src_addr_range.setEnabled(False)
            self.e_dst_addr_range.setEnabled(False)
            self.src_addr_not.setEnabled(False)
            self.src_addr_line_edit.setEnabled(False)
            self.dst_addr_not.setEnabled(False)
            self.dst_addr_line_edit.setEnabled(False)
            self.src_addr_range_not.setEnabled(False)
            self.src_addr_range_line_edit.setEnabled(False)
            self.dst_addr_range_not.setEnabled(False)
            self.dst_addr_range_line_edit.setEnabled(False)

    def change_port(self):
        if self.e_tcp_Match.isChecked():
            self.e_src_port_tcp.setEnabled(True)
            self.e_dst_port_tcp.setEnabled(True)
            self.e_tcp_flags.setEnabled(True)

            if self.e_src_port_tcp.isChecked():
                self.src_port_tcp_not.setEnabled(True)
                self.src_port_tcp_line_edit.setEnabled(True)
            else:
                self.src_port_tcp_not.setEnabled(False)
                self.src_port_tcp_line_edit.setEnabled(False)

            if self.e_dst_port_tcp.isChecked():
                self.dst_port_tcp_not.setEnabled(True)
                self.dst_port_tcp_line_edit.setEnabled(True)
            else:
                self.dst_port_tcp_not.setEnabled(False)
                self.dst_port_tcp_line_edit.setEnabled(False)

            if self.e_tcp_flags.isChecked():
                self.tcp_flags_not.setEnabled(True)
                self.tcp_flags_line_edit.setEnabled(True)
            else:
                self.tcp_flags_not.setEnabled(False)
                self.tcp_flags_line_edit.setEnabled(False)
        else:
            self.e_src_port_tcp.setEnabled(False)
            self.e_dst_port_tcp.setEnabled(False)
            self.e_tcp_flags.setEnabled(False)
            self.src_port_tcp_not.setEnabled(False)
            self.src_port_tcp_line_edit.setEnabled(False)
            self.dst_port_tcp_not.setEnabled(False)
            self.dst_port_tcp_line_edit.setEnabled(False)
            self.tcp_flags_not.setEnabled(False)
            self.tcp_flags_line_edit.setEnabled(False)

    def change_udp(self):
        if self.e_udp_Match.isChecked():
            self.e_src_port_udp.setEnabled(True)
            self.e_dst_port_udp.setEnabled(True)

            if self.e_src_port_udp.isChecked():
                self.src_port_udp_not.setEnabled(True)
                self.src_port_udp_line_edit.setEnabled(True)
            else:
                self.src_port_udp_not.setEnabled(False)
                self.src_port_udp_line_edit.setEnabled(False)

            if self.e_dst_port_udp.isChecked():
                self.dst_port_udp_not.setEnabled(True)
                self.dst_port_udp_line_edit.setEnabled(True)
            else:
                self.dst_port_udp_not.setEnabled(False)
                self.dst_port_udp_line_edit.setEnabled(False)
        else:
            self.e_src_port_udp.setEnabled(False)
            self.e_dst_port_udp.setEnabled(False)
            self.src_port_udp_not.setEnabled(False)
            self.src_port_udp_line_edit.setEnabled(False)
            self.dst_port_udp_not.setEnabled(False)
            self.dst_port_udp_line_edit.setEnabled(False)

    def change_icmp(self):
        if self.e_icmp_type.isChecked():
            self.icmp_type_not.setEnabled(True)
            self.icmp_type_line_edit.setEnabled(True)
        else:
            self.icmp_type_not.setEnabled(False)
            self.icmp_type_line_edit.setEnabled(False)

    def change_multiport(self):
        if self.e_multi_port.isChecked():
            self.e_src_port_multi.setEnabled(True)
            self.e_dst_port_multi.setEnabled(True)
            self.protocol_combobox.setEnabled(True)
            self.protocol_not.setEnabled(True)

            if self.e_src_port_multi.isChecked():
                self.src_port_multi_not.setEnabled(True)
                self.src_port_multi_line_edit.setEnabled(True)
            else:
                self.src_port_multi_not.setEnabled(False)
                self.src_port_multi_line_edit.setEnabled(False)

            if self.e_dst_port_multi.isChecked():
                self.dst_port_multi_not.setEnabled(True)
                self.dst_port_multi_line_edit.setEnabled(True)
            else:
                self.dst_port_multi_not.setEnabled(False)
                self.dst_port_multi_line_edit.setEnabled(False)
        else:
            self.e_src_port_multi.setEnabled(False)
            self.e_dst_port_multi.setEnabled(False)
            self.protocol_combobox.setEnabled(False)
            self.protocol_not.setEnabled(False)
            self.src_port_multi_not.setEnabled(False)
            self.src_port_multi_line_edit.setEnabled(False)
            self.dst_port_multi_not.setEnabled(False)
            self.dst_port_multi_line_edit.setEnabled(False)

    def change_state(self):

        if self.e_state.isChecked():
            self.state_not.setEnabled(True)
            self.state_line_edit.setEnabled(True)
        else:
            self.state_not.setEnabled(False)
            self.state_line_edit.setEnabled(False)

    def change_limit(self):
        if self.e_limit.isChecked():
            self.e_limit_rate.setEnabled(True)
            self.e_limit_burst.setEnabled(True)

            if self.e_limit_rate.isChecked():
                self.limit_rate_line_edit.setEnabled(True)
            else:
                self.limit_rate_line_edit.setEnabled(False)

            if self.e_limit_burst.isChecked():
                self.limit_burst_line_edit.setEnabled(True)
            else:
                self.limit_burst_line_edit.setEnabled(False)

        else:
            self.e_limit_rate.setEnabled(False)
            self.e_limit_burst.setEnabled(False)
            self.limit_rate_line_edit.setEnabled(False)
            self.limit_burst_line_edit.setEnabled(False)

    def change_time(self):

        if self.e_time.isChecked():
            self.e_date_start.setEnabled(True)
            self.e_date_stop.setEnabled(True)
            self.e_time_start.setEnabled(True)
            self.e_time_stop.setEnabled(True)
            self.e_month_days.setEnabled(True)
            self.e_week_days.setEnabled(True)

            if self.e_date_start.isChecked():
                self.date_start_line_edit.setEnabled(True)
            else:
                self.date_start_line_edit.setEnabled(False)

            if self.e_date_stop.isChecked():
                self.date_stop_line_edit.setEnabled(True)
            else:
                self.date_stop_line_edit.setEnabled(False)

            if self.e_time_start.isChecked():
                self.time_start_line_edit.setEnabled(True)
            else:
                self.time_start_line_edit.setEnabled(False)

            if self.e_time_stop.isChecked():
                self.time_stop_line_edit.setEnabled(True)
            else:
                self.time_stop_line_edit.setEnabled(False)

            if self.e_month_days.isChecked():
                self.month_days_not.setEnabled(True)
                self.month_days_line_edit.setEnabled(True)
            else:
                self.month_days_not.setEnabled(False)
                self.month_days_line_edit.setEnabled(False)

            if self.e_week_days.isChecked():
                self.week_days_not.setEnabled(True)
                self.week_days_line_edit.setEnabled(True)
            else:
                self.week_days_not.setEnabled(False)
                self.week_days_line_edit.setEnabled(False)
        else:
            self.e_date_start.setEnabled(False)
            self.e_date_stop.setEnabled(False)
            self.e_time_start.setEnabled(False)
            self.e_time_stop.setEnabled(False)
            self.e_month_days.setEnabled(False)
            self.e_week_days.setEnabled(False)
            self.date_start_line_edit.setEnabled(False)
            self.date_stop_line_edit.setEnabled(False)
            self.time_start_line_edit.setEnabled(False)
            self.time_stop_line_edit.setEnabled(False)
            self.month_days_not.setEnabled(False)
            self.month_days_line_edit.setEnabled(False)
            self.week_days_not.setEnabled(False)
            self.week_days_line_edit.setEnabled(False)

    def change_string(self):
        if self.e_string.isChecked():
            self.e_algo.setEnabled(True)
            self.e_from_data.setEnabled(True)
            self.e_to_data.setEnabled(True)
            self.e_check_string.setEnabled(True)

            if self.e_algo.isChecked():
                self.algo_combobox.setEnabled(True)
            else:
                self.algo_combobox.setEnabled(False)

            if self.e_from_data.isChecked():
                self.from_data_line_edit.setEnabled(True)
            else:
                self.from_data_line_edit.setEnabled(False)

            if self.e_to_data.isChecked():
                self.to_data_line_edit.setEnabled(True)
            else:
                self.to_data_line_edit.setEnabled(False)

            if self.e_check_string.isChecked():
                self.check_string_not.setEnabled(True)
                self.check_string_line_edit.setEnabled(True)
            else:
                self.check_string_not.setEnabled(False)
                self.check_string_line_edit.setEnabled(False)

        else:
            self.e_algo.setEnabled(False)
            self.e_from_data.setEnabled(False)
            self.e_to_data.setEnabled(False)
            self.e_check_string.setEnabled(False)
            self.algo_combobox.setEnabled(False)
            self.from_data_line_edit.setEnabled(False)
            self.to_data_line_edit.setEnabled(False)
            self.check_string_not.setEnabled(False)
            self.check_string_line_edit.setEnabled(False)

    def change_ttl(self):
        if self.e_ttl.isChecked():
            self.e_ttl_eq.setEnabled(True)
            self.e_ttl_gt.setEnabled(True)
            self.e_ttl_lt.setEnabled(True)

            if self.e_ttl_eq.isChecked():
                self.ttl_eq_not.setEnabled(True)
                self.ttl_eq_line_edit.setEnabled(True)
            else:
                self.ttl_eq_not.setEnabled(False)
                self.ttl_eq_line_edit.setEnabled(False)

            if self.e_ttl_gt.isChecked():
                self.ttl_gt_line_edit.setEnabled(True)
            else:
                self.ttl_gt_line_edit.setEnabled(False)

            if self.e_ttl_lt.isChecked():
                self.ttl_lt_line_edit.setEnabled(True)
            else:
                self.ttl_lt_line_edit.setEnabled(False)

        else:
            self.e_ttl_eq.setEnabled(False)
            self.e_ttl_gt.setEnabled(False)
            self.e_ttl_lt.setEnabled(False)
            self.ttl_eq_not.setEnabled(False)
            self.ttl_eq_not.setEnabled(False)
            self.ttl_eq_line_edit.setEnabled(False)
            self.ttl_gt_line_edit.setEnabled(False)
            self.ttl_lt_line_edit.setEnabled(False)

    def change_comment(self):
        if self.e_comment.isChecked():
            self.comment_line_edit.setEnabled(True)
        else:
            self.comment_line_edit.setEnabled(False)


################################################################################
#################################### NAT  ######################################
################################################################################
    def apply_nat (self):
         src_addr = ""
         dst_addr = ""
         iprange_match = ""
         tcp_match = ""
         udp_match = ""
         icmp_type = ""
         multi_match = ""
         limit_match = ""
         time_match = ""
         state = ""
         string_match = ""
         ttl_match = ""
         comment = ""
         super_match = ""
         in_if = ""
         def sma(value,salt,is_not):
             salt = salt + ' '
             return salt + value + ' '  if is_not == False else salt + '! ' + value + ' '
     # ------------------------------- FILTER SUB-CATEGORY -------------------------------
     # --- MATCHES ---
         # IP match
         ## Source Address

         if self.nat_rule_combobox.currentText() == "ADD in line":
             line = self.nat_rule_line_edit.text()
             chain = self.nat_chain_combox.currentText()
             var_rule = "-I " + line + " " + chain + " "
         if self.nat_rule_combobox.currentText() == "APPEND":
             var_rule = "-A " + self.nat_chain_combox.currentText() + " "
         if self.nat_rule_combobox.currentText() == "INSERT":
             var_rule = "-I 1 " + self.nat_chain_combox.currentText() + " "


         if self.nat_e_IP_Match.isChecked():

             if self.nat_e_src_addr.isChecked():

                 src_addr = self.nat_src_addr_line_edit.text()
                 src_addr = sma(src_addr,'-s',self.nat_src_addr_not.isChecked())
             else:
                 src_addr = ''
             ## Destination Address
             if self.nat_e_dst_addr.isChecked():
                 dst_addr = self.nat_dst_addr_line_edit.text()
                 dst_addr = sma(dst_addr,'-d',self.nat_dst_addr_not.isChecked())
             else:
                 dst_addr = ''
             ## iprange sub-match
             ### Source Address Range
             if self.nat_e_src_addr_range.isChecked() or self.nat_e_dst_addr_range.isChecked():
                 if self.nat_e_src_addr_range.isChecked():
                     src_addr_range = self.nat_src_addr_range_line_edit.text()
                     src_addr_range = sma(src_addr_range,'--src-range',self.nat_src_addr_range_not.isChecked())
                 else:
                     src_addr_range = ''

                 ### Destination Address Range
                 if self.nat_e_dst_addr_range.isChecked():
                     dst_addr_range = self.nat_dst_addr_range_line_edit.text()
                     dst_addr_range = sma(dst_addr_range,'--dst-range',self.nat_dst_addr_range_not.isChecked())
                 else:
                     dst_addr_range = ''
                 iprange_match = '-m iprange ' + src_addr_range  + dst_addr_range
             else:
                iprange_match = ''


         else:
             ip_rule = ''

         # IP match END

         # Port match

         ## TCP match
         if self.nat_e_tcp_Match.isChecked():
         ### Source Port
             if self.nat_e_src_port_tcp.isChecked():
                 src_port_tcp = self.nat_src_port_tcp_line_edit.text()
                 src_port_tcp = sma(src_port_tcp,'--sport',self.nat_src_port_tcp_not.isChecked())
             else:
                 src_port_tcp = ''
             ### Destination Port
             if self.nat_e_dst_port_tcp.isChecked():
                 dst_port_tcp = self.nat_dst_port_tcp_line_edit.text()
                 dst_port_tcp = sma(dst_port_tcp,'--dport',self.nat_src_port_tcp_not.isChecked())
             else:
                 dst_port_tcp = ''
             ### TCP Flag
             if self.nat_e_tcp_flags.isChecked():
                 tcp_flags = self.nat_tcp_flags_line_edit.text()
                 tcp_flags = sma(tcp_flags,'--tcp-flags ',self.nat_tcp_flags_not.isChecked())
             else:
                 tcp_flags = ''

             tcp_match = '-p tcp -m tcp ' + src_port_tcp  + dst_port_tcp + tcp_flags

         else:
             tcp_match = ''


         ## UDP match
         ### Source Port
         if self.nat_e_udp_Match.isChecked():
             if self.nat_e_src_port_udp.isChecked():
                 src_port_udp = self.nat_src_port_udp_line_edit.text()
                 src_port_udp = sma(src_port_udp,'--sport',self.nat_src_port_udp_not.isChecked())
             else:
                 src_port_udp = ''
             ### Destination Port
             if self.nat_e_dst_port_udp.isChecked():
                 dst_port_udp = self.nat_dst_port_udp_line_edit.text()
                 dst_port_udp = sma(dst_port_udp,'--dport',self.nat_dst_port_udp_not.isChecked())
             else:
                 dst_port_udp = ''

             udp_match = '-p udp -m udp ' + src_port_udp  + dst_port_udp

         ## icmp match
         ### icmp type
         if self.nat_e_icmp_type.isChecked():
             icmp_type = self.nat_icmp_type_line_edit.text()
             icmp_type = sma(icmp_type,'-p icmp -m icmp --icmp-type',self.nat_icmp_type_not.isChecked())
         else:
             icmp_type = ''

         ## Multiport match
         if self.nat_e_multi_port.isChecked():
             if self.nat_e_src_port_multi.isChecked() or self.nat_e_dst_port_multi.isChecked():
                 protocol = self.nat_protocol_combobox.currentText() + ' '
             else:
                QMessageBox.warning(self,"Advertencia","debe poseer algun puerto de destino u origen",QMessageBox.Ok)
                self.nat_e_multi_port.Checked(False)
             ### Source Port
             if self.nat_e_src_port_multi.isChecked():
                 src_port_multi = self.nat_src_port_multi_line_edit.text()
                 src_port_multi = sma(src_port_multi,'--sport',self.nat_src_port_multi_not.isChecked())
             else:
                 src_port_multi = ''
             ### Destination Port
             if self.nat_e_dst_port_multi.isChecked():
                 dst_port_multi = self.nat_dst_port_multi_line_edit.text()
                 dst_port_multi = sma(dst_port_multi,'--dport',self.nat_dst_port_multi_not.isChecked())
             else:
                 dst_port_multi = ''

             multi_match = '-p ' + protocol + '-m multiport ' +  src_port_multi  +  dst_port_multi
         else:
             multi_match = ''
         ## Multiport match END
         # Port match END

         # State match
         if self.nat_e_state.isChecked():
             state = self.nat_state_line_edit.text()
             state = sma(state,'-m state --state', self.nat_state_not.isChecked())
         else:
             state = ''
         # State match END

         # Limit match
         ## Limit Rate
         if self.nat_e_limit.isChecked():
             if self.nat_e_limit_rate.isChecked():
                 limit_rate = self.nat_limit_rate_line_edit.text()
                 limit_rate ='--limit-rate ' + limit_rate + ' '
             else:
                 limit_rate = ''
             ## Limit Burst
             if self.nat_e_limit_burst.isChecked():
                 limit_burst = self.nat_limit_burst_line_edit.text()
                 limit_burst = 'limit-burst ' + limit_burst + ' '
             else:
                 limit_burst = ''

             limit_match = '-m limit ' + limit_rate + limit_burst
         else:
             limit_match = ''
         # Limit match END

         if self.nat_e_time.isChecked():
             # Date Start
             if self.nat_e_date_start.isChecked():
                 date_start = self.nat_date_start_line_edit.text()
                 date_start = '--datestart ' + date_start + ' '
             else:
                 date_start = ''
             # Date Stop
             if self.nat_e_date_stop.isChecked():
                 date_stop = self.nat_date_stop_line_edit.text()
                 date_stop = '--datestop ' + date_stop + ' '
             else:
                 date_stop = ''

             # Time Start
             if self.nat_e_time_start.isChecked():
                 time_start = self.nat_time_start_line_edit.text()
                 time_start = '--timestart ' + time_start + ' '
             else:
                 time_start = ''
             # Time Stop
             if self.nat_e_time_stop.isChecked():
                 time_stop = self.nat_time_stop_line_edit.text()
                 time_stop = '--timestop ' + time_stop + ' '
             else:
                 time_stop = ''

             # Month Days
             if self.nat_e_month_days.isChecked():
                 month_days = self.nat_month_days_line_edit.text()
                 month_days = sma(month_days,'--monthdays',self.nat_month_days_not.isChecked())
             else:
                 month_days = ''
             # Week Days
             if self.nat_e_week_days.isChecked():
                 week_days = self.nat_week_days_line_edit.text()
                 week_days = sma(week_days,'--weekdays',self.nat_week_days_not.isChecked())
             else:
                 week_days = ''

             time_match = '-m time '+ date_start  + date_stop + time_start + time_stop + month_days + week_days
         else:
             time_match = ''
         # Time Match END
         # String Match
         if self.nat_e_string.isChecked():
             # Algorithm
             if self.nat_e_algo.isChecked():
                 algo = '--algo ' + self.nat_algo_combobox.currentText() + ' '
             else:
                 algo = ''
             # From
             if self.nat_e_from_data.isChecked():
                 from_data = self.nat_from_data_line_edit.text()
                 from_data = '--from ' + from_data + ' '
             else:
                 from_data = ''

             # To
             if self.nat_e_to_data.isChecked():
                 to_data = self.nat_to_data_line_edit.text()
                 to_data = '--to ' + to_data + ' '
             else:
                 time_start = ''
             # String
             if self.nat_e_check_string.isChecked():
                check_string = self.nat_check_string_line_edit.text()
                check_string = sma(check_string,'--string',self.nat_check_string_not.isChecked())
             else:
                 check_string = ''

             string_match = '-m string ' + algo + from_data  + to_data  + check_string
         else:
             string_match = ''

         # String Match END

        # TTL Match
         # -m ttl --ttl-eq --ttl-gt --ttl-lt
         if self.nat_e_ttl.isChecked():
             ## TTL equal
             if self.nat_e_ttl_eq.isChecked():
                ttl_eq = self.nat_ttl_eq_line_edit.text()
                ttl_eq = sma(ttl_eq,'--ttl-eq',self.nat_ttl_eq_not.isChecked())
             else:
                 ttl_eq  = ''
             ## TTL greater than
             if self.nat_e_ttl_gt.isChecked():
                 ttl_gt = self.nat_ttl_gt_line_edit.text()
                 ttl_gt = '--ttl-gt ' + ttl_gt + ' '
             else:
                 ttl_gt = ''
             ## TTL less than
             if self.nat_e_ttl_lt.isChecked():
                 ttl_lt = self.nat_ttl_lt_line_edit.text()
                 ttl_lt = '--ttl-lt ' + ttl_lt + ' '
             else:
                 ttl_lt = ''

             ttl_match = '-m ttl '  +ttl_eq  + ttl_gt  + ttl_lt
         else:
             ttl_match = ''
         # TTL Match END

         # comment Match
         if self.nat_e_comment.isChecked():
            comment = self.nat_comment_line_edit.text()
            comment = '-m comment --comment ' + '\'' +comment + '\'' + ' '
         else:
            comment  = ''


         x = self.nat_action_combobox.currentText()

         if x == "MASQUERADE" and self.nat_chain_combox.currentText() == "POSTROUTING":
             action = '-j MASQUERADE'
             if self.e_masquerade.isChecked():
                 action = action + '--to-ports ' + self.masquerade.text()

         if x == "REDIRECT" and (self.nat_chain_combox.currentText() == "PRETROUTING" or self.nat_chain_combox.currentText() == "POSTROUTING"):
            action = '-j REDIRECT --to-ports ' + self.redirect.text()

         if x == "SNAT" and (self.nat_chain_combox.currentText() == "INPUT" or self.nat_chain_combox.currentText() == "POSTROUTING"):
            action = '-j SNAT --to-source ' + self.snat.text()

         if x == "DNAT" and (self.nat_chain_combox.currentText() == "OUTPUT" or  self.nat_chain_combox.currentText() == "PREROUTING"):
              action = '-j DNAT --to-destination ' + self.dnat.text()

         if x == "LOG":
              action = '-j LOG --log-level' + self.log_combobox.currentText() + ' --log-prefix ' + self.prefix_line_edit.text()



         if self.nat_chain_combox.currentText() == "INPUT" or self.nat_chain_combox.currentText() == "PREROUTING" :
              out_if = ""
              if self.nat_e_in.isChecked():
                  if self.nat_in_not.isChecked():
                      in_if = "-i " + '! '+ self.nat_in_combobox.currentText() + " "
                  else:
                      in_if = "-i " + self.nat_in_combobox.currentText() + " "
              else:
                  in_if =""

         if self.nat_chain_combox.currentText() == "OUTPUT" or self.nat_chain_combox.currentText() == "POSTROUTING":
             #in_if == ""
             if self.nat_e_out.isChecked():
                 if self.nat_out_not.isChecked():
                     out_if = "-o " + '! '+ self.nat_out_combobox.currentText() + " "
                 else:
                     out_if = "-o " + self.nat_out_combobox.currentText() + " "
             else:
                  out_if =""



         # General definition of matches
         super_match = src_addr  + dst_addr + iprange_match + tcp_match  + udp_match + icmp_type
         super_match = super_match  + multi_match  +limit_match+ time_match + state + string_match + ttl_match
         super_match = super_match  + comment
         rule = var_rule + in_if + out_if + super_match + action

         #print(rule)
         w = self.nat_chain_combox.currentText()
         print('\'' + str(rule) + '\'' +  ' ' +  '\'' + str(w) + '\'' + " " + '\'' + "nat" + '\'')
         tdin, stdout, stderr = ssh_cliente.exec_command("sudo python3 /home/secrouter/firewall/firewall_controller.py " + '\'' + str(rule) + '\'' + " " + '\'' + "nat" + '\'' + ' ' +  '\'' + str(w) + '\'' )
         x = stderr.readlines()
         y = stdout.readlines()
         print(x)
         for i in y:
             print(i)

    def change_chain_nat(self):

        if self.nat_chain_combox.currentText() == "INPUT" or self.nat_chain_combox.currentText() == "PREROUTING":
            self.nat_e_in.setEnabled(True)
            self.nat_e_out.setEnabled(False)
            self.nat_e_out.setChecked(False)
            self.nat_out_not.setChecked(False)
            self.nat_out_not.setEnabled(False)
            self.nat_out_combobox.setEnabled(False)

        if self.nat_chain_combox.currentText() == "OUTPUT" or self.nat_chain_combox.currentText() == "POSTROUTING":
            self.nat_e_out.setEnabled(True)
            self.nat_e_in.setEnabled(False)
            self.nat_e_in.setChecked(False)
            self.nat_in_not.setChecked(False)
            self.nat_in_not.setEnabled(False)
            self.nat_in_combobox.setEnabled(False)

        if self.nat_chain_combox.currentText() == " ":
            self.nat_e_in.setEnabled(False)
            self.nat_e_out.setEnabled(False)
            self.nat_in_not.setEnabled(False)
            self.nat_out_not.setEnabled(False)
            self.nat_in_combobox.setEnabled(False)
            self.nat_out_combobox.setEnabled(False)
            self.nat_e_in.setChecked(False)
            self.nat_e_out.setChecked(False)
            self.nat_in_not.setChecked(False)
            self.nat_out_not.setChecked(False)


    def check_in_out_nat(self):
        if self.nat_e_in.isChecked():
            self.nat_in_not.setEnabled(True)
            self.nat_in_combobox.setEnabled(True)
        else:
            self.nat_in_not.setEnabled(False)
            self.nat_in_combobox.setEnabled(False)

        if self.nat_e_out.isChecked():
            self.nat_out_not.setEnabled(True)
            self.nat_out_combobox.setEnabled(True)
        else:
            self.nat_out_not.setEnabled(False)
            self.nat_out_combobox.setEnabled(False)

    def change_rule_nat(self):

        if self.nat_rule_combobox.currentText() == "ADD in line":
            self.nat_rule_line_edit.setEnabled(True)
        else:
            self.nat_rule_line_edit.setEnabled(False)

    def change_action_nat(self):
        if (self.nat_action_combobox.currentText() == "SNAT" and self.nat_chain_combox.currentText() == "INPUT") or (self.nat_action_combobox.currentText() == "SNAT" and self.nat_chain_combox.currentText() == "POSTROUTING"):
            self.snat.setEnabled(True)
        else:
            self.snat.setEnabled(False)

        if self.nat_action_combobox.currentText() == "DNAT" and self.nat_chain_combox.currentText() == "PREROUTING":
            self.dnat.setEnabled(True)
        else:
            self.dnat.setEnabled(False)

        if self.nat_action_combobox.currentText() == "LOG" and (self.nat_chain_combox.currentText() == "OUTPUT" or self.nat_chain_combox.currentText() == "PREROUTING"):
            self.nat_log_combobox.setEnabled(True)
            self.nat_prefix_line_edit.setEnabled(True)
        else:
            self.nat_log_combobox.setEnabled(False)
            self.nat_prefix_line_edit.setEnabled(False)

        if self.nat_action_combobox.currentText() == "MASQUERADE" and self.nat_chain_combox.currentText() == "POSTROUTING":
            self.e_masquerade.setEnabled(True)

        else:
            self.e_masquerade.setEnabled(False)


        if self.nat_action_combobox.currentText() == "REDIRECT"and (self.nat_chain_combox.currentText() == "PREROUTING" or self.nat_chain_combox.currentText() == "POSTROUTING"):
            self.redirect.setEnabled(True)
        else:
            self.redirect.setEnabled(False)

    def change_masquerade(self):
        if self.e_masquerade.isChecked():
            self.masquerade.setEnabled(True)
        else:
            self.masquerade.setEnabled(False)

    def change_ip_nat(self):
        if self.nat_e_IP_Match.isChecked():
            self.nat_e_src_addr.setEnabled(True)
            self.nat_e_dst_addr.setEnabled(True)
            self.nat_e_src_addr_range.setEnabled(True)
            self.nat_e_dst_addr_range.setEnabled(True)

            if self.nat_e_src_addr.isChecked():
                self.nat_src_addr_not.setEnabled(True)
                self.nat_src_addr_line_edit.setEnabled(True)
            else:
                self.nat_src_addr_not.setEnabled(False)
                self.nat_src_addr_line_edit.setEnabled(False)

            if self.nat_e_dst_addr.isChecked():
                self.nat_dst_addr_not.setEnabled(True)
                self.nat_dst_addr_line_edit.setEnabled(True)
            else:
                self.nat_dst_addr_not.setEnabled(False)
                self.nat_dst_addr_line_edit.setEnabled(False)

            if self.nat_e_src_addr_range.isChecked():
                self.nat_src_addr_range_not.setEnabled(True)
                self.nat_src_addr_range_line_edit.setEnabled(True)
            else:
                self.nat_src_addr_range_not.setEnabled(False)
                self.nat_src_addr_range_line_edit.setEnabled(False)

            if self.nat_e_dst_addr_range.isChecked():
                self.nat_dst_addr_range_not.setEnabled(True)
                self.nat_dst_addr_range_line_edit.setEnabled(True)
            else:
                self.nat_dst_addr_range_not.setEnabled(False)
                self.nat_dst_addr_range_line_edit.setEnabled(False)
        else:
            self.nat_e_src_addr.setEnabled(False)
            self.nat_e_dst_addr.setEnabled(False)
            self.nat_e_src_addr_range.setEnabled(False)
            self.nat_e_dst_addr_range.setEnabled(False)
            self.nat_src_addr_not.setEnabled(False)
            self.nat_src_addr_line_edit.setEnabled(False)
            self.nat_dst_addr_not.setEnabled(False)
            self.nat_dst_addr_line_edit.setEnabled(False)
            self.nat_src_addr_range_not.setEnabled(False)
            self.nat_src_addr_range_line_edit.setEnabled(False)
            self.nat_dst_addr_range_not.setEnabled(False)
            self.nat_dst_addr_range_line_edit.setEnabled(False)

    def change_port_nat(self):
        if self.nat_e_tcp_Match.isChecked():
            self.nat_e_src_port_tcp.setEnabled(True)
            self.nat_e_dst_port_tcp.setEnabled(True)
            self.nat_e_tcp_flags.setEnabled(True)

            if self.nat_e_src_port_tcp.isChecked():
                self.nat_src_port_tcp_not.setEnabled(True)
                self.nat_src_port_tcp_line_edit.setEnabled(True)
            else:
                self.nat_src_port_tcp_not.setEnabled(False)
                self.nat_src_port_tcp_line_edit.setEnabled(False)

            if self.nat_e_dst_port_tcp.isChecked():
                self.nat_dst_port_tcp_not.setEnabled(True)
                self.nat_dst_port_tcp_line_edit.setEnabled(True)
            else:
                self.nat_dst_port_tcp_not.setEnabled(False)
                self.nat_dst_port_tcp_line_edit.setEnabled(False)

            if self.nat_e_tcp_flags.isChecked():
                self.nat_tcp_flags_not.setEnabled(True)
                self.nat_tcp_flags_line_edit.setEnabled(True)
            else:
                self.nat_tcp_flags_not.setEnabled(False)
                self.nat_tcp_flags_line_edit.setEnabled(False)
        else:
            self.nat_e_src_port_tcp.setEnabled(False)
            self.nat_e_dst_port_tcp.setEnabled(False)
            self.nat_e_tcp_flags.setEnabled(False)
            self.nat_src_port_tcp_not.setEnabled(False)
            self.nat_src_port_tcp_line_edit.setEnabled(False)
            self.nat_dst_port_tcp_not.setEnabled(False)
            self.nat_dst_port_tcp_line_edit.setEnabled(False)
            self.nat_tcp_flags_not.setEnabled(False)
            self.nat_tcp_flags_line_edit.setEnabled(False)

    def change_udp_nat(self):
        if self.nat_e_udp_Match.isChecked():
            self.nat_e_src_port_udp.setEnabled(True)
            self.nat_e_dst_port_udp.setEnabled(True)

            if self.nat_e_src_port_udp.isChecked():
                self.nat_src_port_udp_not.setEnabled(True)
                self.nat_src_port_udp_line_edit.setEnabled(True)
            else:
                self.nat_src_port_udp_not.setEnabled(False)
                self.nat_src_port_udp_line_edit.setEnabled(False)

            if self.nat_e_dst_port_udp.isChecked():
                self.nat_dst_port_udp_not.setEnabled(True)
                self.nat_dst_port_udp_line_edit.setEnabled(True)
            else:
                self.nat_dst_port_udp_not.setEnabled(False)
                self.nat_dst_port_udp_line_edit.setEnabled(False)
        else:
            self.nat_e_src_port_udp.setEnabled(False)
            self.nat_e_dst_port_udp.setEnabled(False)
            self.nat_src_port_udp_not.setEnabled(False)
            self.nat_src_port_udp_line_edit.setEnabled(False)
            self.nat_dst_port_udp_not.setEnabled(False)
            self.nat_dst_port_udp_line_edit.setEnabled(False)

    def change_icmp_nat(self):
        if self.nat_e_icmp_type.isChecked():
            self.nat_icmp_type_not.setEnabled(True)
            self.nat_icmp_type_line_edit.setEnabled(True)
        else:
            self.nat_icmp_type_not.setEnabled(False)
            self.nat_icmp_type_line_edit.setEnabled(False)

    def change_multiport_nat(self):
        if self.nat_e_multi_port.isChecked():
            self.nat_e_src_port_multi.setEnabled(True)
            self.nat_e_dst_port_multi.setEnabled(True)
            self.nat_protocol_combobox.setEnabled(True)
            self.nat_protocol_not.setEnabled(True)

            if self.nat_e_src_port_multi.isChecked():
                self.nat_src_port_multi_not.setEnabled(True)
                self.nat_src_port_multi_line_edit.setEnabled(True)
            else:
                self.nat_src_port_multi_not.setEnabled(False)
                self.nat_src_port_multi_line_edit.setEnabled(False)

            if self.nat_e_dst_port_multi.isChecked():
                self.nat_dst_port_multi_not.setEnabled(True)
                self.nat_dst_port_multi_line_edit.setEnabled(True)
            else:
                self.nat_dst_port_multi_not.setEnabled(False)
                self.nat_dst_port_multi_line_edit.setEnabled(False)
        else:
            self.nat_e_src_port_multi.setEnabled(False)
            self.nat_e_dst_port_multi.setEnabled(False)
            self.nat_protocol_combobox.setEnabled(False)
            self.nat_protocol_not.setEnabled(False)
            self.nat_src_port_multi_not.setEnabled(False)
            self.nat_src_port_multi_line_edit.setEnabled(False)
            self.nat_dst_port_multi_not.setEnabled(False)
            self.nat_dst_port_multi_line_edit.setEnabled(False)

    def change_state_nat(self):

        if self.nat_e_state.isChecked():
            self.nat_state_not.setEnabled(True)
            self.nat_state_line_edit.setEnabled(True)
        else:
            self.nat_state_not.setEnabled(False)
            self.nat_state_line_edit.setEnabled(False)

    def change_limit_nat(self):
        if self.nat_e_limit.isChecked():
            self.nat_e_limit_rate.setEnabled(True)
            self.nat_e_limit_burst.setEnabled(True)

            if self.nat_e_limit_rate.isChecked():
                self.nat_limit_rate_line_edit.setEnabled(True)
            else:
                self.nat_limit_rate_line_edit.setEnabled(False)

            if self.nat_e_limit_burst.isChecked():
                self.nat_limit_burst_line_edit.setEnabled(True)
            else:
                self.nat_limit_burst_line_edit.setEnabled(False)

        else:
            self.nat_e_limit_rate.setEnabled(False)
            self.nat_e_limit_burst.setEnabled(False)
            self.nat_limit_rate_line_edit.setEnabled(False)
            self.nat_limit_burst_line_edit.setEnabled(False)

    def change_time_nat(self):

        if self.nat_e_time.isChecked():
            self.nat_e_date_start.setEnabled(True)
            self.nat_e_date_stop.setEnabled(True)
            self.nat_e_time_start.setEnabled(True)
            self.nat_e_time_stop.setEnabled(True)
            self.nat_e_month_days.setEnabled(True)
            self.nat_e_week_days.setEnabled(True)

            if self.nat_e_date_start.isChecked():
                self.nat_date_start_line_edit.setEnabled(True)
            else:
                self.nat_date_start_line_edit.setEnabled(False)

            if self.nat_e_date_stop.isChecked():
                self.nat_date_stop_line_edit.setEnabled(True)
            else:
                self.nat_date_stop_line_edit.setEnabled(False)

            if self.nat_e_time_start.isChecked():
                self.nat_time_start_line_edit.setEnabled(True)
            else:
                self.nat_time_start_line_edit.setEnabled(False)

            if self.nat_e_time_stop.isChecked():
                self.nat_time_stop_line_edit.setEnabled(True)
            else:
                self.nat_time_stop_line_edit.setEnabled(False)

            if self.nat_e_month_days.isChecked():
                self.nat_month_days_not.setEnabled(True)
                self.nat_month_days_line_edit.setEnabled(True)
            else:
                self.nat_month_days_not.setEnabled(False)
                self.nat_month_days_line_edit.setEnabled(False)

            if self.nat_e_week_days.isChecked():
                self.nat_week_days_not.setEnabled(True)
                self.nat_week_days_line_edit.setEnabled(True)
            else:
                self.nat_week_days_not.setEnabled(False)
                self.nat_week_days_line_edit.setEnabled(False)
        else:
            self.nat_e_date_start.setEnabled(False)
            self.nat_e_date_stop.setEnabled(False)
            self.nat_e_time_start.setEnabled(False)
            self.nat_e_time_stop.setEnabled(False)
            self.nat_e_month_days.setEnabled(False)
            self.nat_e_week_days.setEnabled(False)
            self.nat_date_start_line_edit.setEnabled(False)
            self.nat_date_stop_line_edit.setEnabled(False)
            self.nat_time_start_line_edit.setEnabled(False)
            self.nat_time_stop_line_edit.setEnabled(False)
            self.nat_month_days_not.setEnabled(False)
            self.nat_month_days_line_edit.setEnabled(False)
            self.nat_week_days_not.setEnabled(False)
            self.nat_week_days_line_edit.setEnabled(False)

    def change_string_nat(self):
        if self.nat_e_string.isChecked():
            self.nat_e_algo.setEnabled(True)
            self.nat_e_from_data.setEnabled(True)
            self.nat_e_to_data.setEnabled(True)
            self.nat_e_check_string.setEnabled(True)

            if self.nat_e_algo.isChecked():
                self.nat_algo_combobox.setEnabled(True)
            else:
                self.nat_algo_combobox.setEnabled(False)

            if self.nat_e_from_data.isChecked():
                self.nat_from_data_line_edit.setEnabled(True)
            else:
                self.nat_from_data_line_edit.setEnabled(False)

            if self.nat_e_to_data.isChecked():
                self.nat_to_data_line_edit.setEnabled(True)
            else:
                self.nat_to_data_line_edit.setEnabled(False)

            if self.nat_e_check_string.isChecked():
                self.nat_check_string_not.setEnabled(True)
                self.nat_check_string_line_edit.setEnabled(True)
            else:
                self.nat_check_string_not.setEnabled(False)
                self.nat_check_string_line_edit.setEnabled(False)

        else:
            self.nat_nat_e_algo.setEnabled(False)
            self.nat_e_from_data.setEnabled(False)
            self.nat_e_to_data.setEnabled(False)
            self.nat_e_check_string.setEnabled(False)
            self.nat_algo_combobox.setEnabled(False)
            self.nat_from_data_line_edit.setEnabled(False)
            self.nat_to_data_line_edit.setEnabled(False)
            self.nat_check_string_not.setEnabled(False)
            self.nat_check_string_line_edit.setEnabled(False)

    def change_ttl_nat(self):
        if self.nat_e_ttl.isChecked():
            self.nat_e_ttl_eq.setEnabled(True)
            self.nat_e_ttl_gt.setEnabled(True)
            self.nat_e_ttl_lt.setEnabled(True)

            if self.nat_e_ttl_eq.isChecked():
                self.nat_ttl_eq_not.setEnabled(True)
                self.nat_ttl_eq_line_edit.setEnabled(True)
            else:
                self.nat_ttl_eq_not.setEnabled(False)
                self.nat_ttl_eq_line_edit.setEnabled(False)

            if self.nat_e_ttl_gt.isChecked():
                self.nat_ttl_gt_line_edit.setEnabled(True)
            else:
                self.nat_ttl_gt_line_edit.setEnabled(False)

            if self.nat_e_ttl_lt.isChecked():
                self.nat_ttl_lt_line_edit.setEnabled(True)
            else:
                self.nat_ttl_lt_line_edit.setEnabled(False)

        else:
            self.nat_e_ttl_eq.setEnabled(False)
            self.nat_e_ttl_gt.setEnabled(False)
            self.nat_e_ttl_lt.setEnabled(False)
            self.nat_ttl_eq_not.setEnabled(False)
            self.nat_ttl_eq_not.setEnabled(False)
            self.nat_ttl_eq_line_edit.setEnabled(False)
            self.nat_ttl_gt_line_edit.setEnabled(False)
            self.nat_ttl_lt_line_edit.setEnabled(False)

    def change_comment_nat(self):
        if self.nat_e_comment.isChecked():
            self.nat_comment_line_edit.setEnabled(True)
        else:
            self.nat_comment_line_edit.setEnabled(False)

#-------------------------------MAIN SECTION ------------------------------------
    def Add_main (self):
        add_user_chain = 'iptables -N ' + self.create_line_edit.text()
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo " + str(add_user_chain))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        self.change_combobox()

    def change_combobox(self):
        w = "sudo python3 /home/secrouter/firewall/parser_chain.py"
        tdin, stdout, stderr = ssh_cliente.exec_command(str(w) +" " +'\''+  'filter'+'\'')
        x = stderr.readlines()
        y = stdout.readlines()
        print(y)
        self.chain_combox.clear()
        self.chain_comboBox.clear()
        self.chain_policy_comboBox.clear()
        self.chain_policy_comboBox.addItem("INPUT")
        self.chain_policy_comboBox.addItem("FORWARD")
        self.chain_policy_comboBox.addItem("OUTPUT")
        self.chain_comboBox.addItem("INPUT")
        self.chain_comboBox.addItem("FORWARD")
        self.chain_comboBox.addItem("OUTPUT")
        self.chain_combox.addItem("INPUT")
        self.chain_combox.addItem("FORWARD")
        self.chain_combox.addItem("OUTPUT")
        self.view_chain_comboBox.clear()
        self.view_chain_comboBox.addItem("INPUT")
        self.view_chain_comboBox.addItem("FORWARD")
        self.view_chain_comboBox.addItem("OUTPUT")
        for i in y:
            self.chain_policy_comboBox.addItem(i[:-1])
            self.chain_comboBox.addItem(i[:-1])
            self.chain_combox.addItem(i[:-1])
            self.view_chain_comboBox.addItem(i[:-1])

        w = "sudo python3 /home/secrouter/firewall/parser_chain.py"
        tdin, stdout, stderr = ssh_cliente.exec_command(str(w) +" " +'\''+  'nat'+'\'')
        x = stderr.readlines()
        k = stdout.readlines()
        self.nat_chain_combox.clear()
        for i in k:
            self.chain_policy_comboBox.addItem(i[:-1])
            self.chain_comboBox.addItem(i[:-1])
            self.nat_chain_combox.addItem(i[:-1])


    def Delete_main(self):
        del_user_chain = 'iptables -X ' + self.create_line_edit.text()
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo " + str(del_user_chain))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        self.change_combobox()
    def delete_rule(self):
        if self.chain_comboBox.currentText() != '':
            delete_rule = 'iptables -t '+self.chain_comboBox.currentText() + ' -D ' +  self.chain_comboBox_2.currentText() + ' ' + self.at_line_line_edit.text()
            tdin, stdout, stderr = ssh_cliente.exec_command("sudo " + str(delete_rule))
            x = stderr.readlines()
            y = stdout.readlines()
        print(x)
        print(y)
    def policy(self):
        add_policy = 'iptables -t '+ self.chain_policy_comboBox.currentText() + ' -P ' + self.chain_policy_comboBox_2.currentText() + ' ' + self.accept_main.currentText()
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo " + str(add_policy))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
    def rule(self):
        if self.table_comboBox.currentText() == "filter":
            self.view_chain_comboBox.clear()
            self.view_chain_comboBox.addItem("INPUT")
            self.view_chain_comboBox.addItem("FORWARD")
            self.view_chain_comboBox.addItem("OUTPUT")
        if self.table_comboBox.currentText() == "nat":
            self.view_chain_comboBox.clear()
            self.view_chain_comboBox.addItem("PREROUTING")
            self.view_chain_comboBox.addItem("POSTROUTING")
            self.view_chain_comboBox.addItem("INPUT")
            self.view_chain_comboBox.addItem("OUTPUT")

    def change_delete_rule(self):
        if  self.chain_comboBox.currentText() == "filter":
            self.chain_comboBox_2.clear()
            self.chain_comboBox_2.addItem("INPUT")
            self.chain_comboBox_2.addItem("FORWARD")
            self.chain_comboBox_2.addItem("OUTPUT")
        if  self.chain_comboBox.currentText() == "nat":
            self.chain_comboBox_2.clear()
            self.chain_comboBox_2.addItem("PREROUTING")
            self.chain_comboBox_2.addItem("POSTROUTING")
            self.chain_comboBox_2.addItem("INPUT")
            self.chain_comboBox_2.addItem("OUTPUT")
    def change_flush(self):
        if  self.chain_flush_comboBox.currentText() == "filter":
            self.chain_flush_comboBox_2.clear()
            self.chain_flush_comboBox_2.addItem("INPUT")
            self.chain_flush_comboBox_2.addItem("FORWARD")
            self.chain_flush_comboBox_2.addItem("OUTPUT")
        if  self.chain_flush_comboBox.currentText() == "nat":
            self.chain_flush_comboBox_2.clear()
            self.chain_flush_comboBox_2.addItem("PREROUTING")
            self.chain_flush_comboBox_2.addItem("POSTROUTING")
            self.chain_flush_comboBox_2.addItem("INPUT")
            self.chain_flush_comboBox_2.addItem("OUTPUT")

    def change_policy(self):
        if  self.chain_policy_comboBox.currentText() == "filter":
            self.chain_policy_comboBox_2.clear()
            self.chain_policy_comboBox_2.addItem("INPUT")
            self.chain_policy_comboBox_2.addItem("FORWARD")
            self.chain_policy_comboBox_2.addItem("OUTPUT")
        if  self.chain_policy_comboBox.currentText() == "nat":
            self.chain_policy_comboBox_2.clear()
            self.chain_policy_comboBox_2.addItem("PREROUTING")
            self.chain_policy_comboBox_2.addItem("POSTROUTING")
            self.chain_policy_comboBox_2.addItem("INPUT")
            self.chain_policy_comboBox_2.addItem("OUTPUT")

    def view_rule(self):
        self.textEdit.clear()
        view_button = 'iptables -n --line-numbers -t ' + self.table_comboBox.currentText() + ' ' + '-L' + ' ' + self.view_chain_comboBox.currentText()
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo " + str(view_button))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        for i in y:
            self.textEdit.append(str(i))

    def flush(self):
        self.textEdit.clear()
        flush_button = 'iptables -t '+self.chain_flush_comboBox.currentText()+ ' -F ' + self.chain_flush_comboBox_2.currentText()
        tdin, stdout, stderr = ssh_cliente.exec_command("sudo " + str(flush_button))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)

################################################################################
############################## SYS AND ADMIN ###################################
################################################################################

    def ping(self):

        v = socket.gethostbyname(self.ping_line_edit.text())
        print( "ping " + v)
        for i in range(5):
            tdin, stdout, stderr = ssh_cliente.exec_command( "ping " + str(v) + " -c 1")
            y = stdout.readlines()
            print(y)
            for i in y:
                validar = re.search("bytes from", i)
                if validar:
                    self.ping_textedit.append(i)



    def ececuteCmd(self):
        try:
            var = "ping " + str(self.ping_line_edit.text()) + " -c 5"
            channel = ssh_cliente.invoke_shell()
            timeout = 60 # timeout is in seconds
            channel.settimeout(timeout)
            newline        = '\r'
            line_buffer    = ''
            channel_buffer = ''

            channel.send(var + ' ; exit ' + newline)

            while True:
                channel_buffer = channel.recv(10).decode('UTF-8')

                if len(channel_buffer) == 0:
                    break
                channel_buffer  = channel_buffer.replace('\r', '')
                if channel_buffer != '\n':
                    line_buffer += str(channel_buffer)
                else:

                    print (line_buffer)
                    validar = re.search("bytes", line_buffer)
                    if validar:
                        self.ping_textedit.append(line_buffer)
                    line_buffer   = ''
        except paramiko.SSHException as e:
            pass

    def traceroute(self):
        v = socket.gethostbyname(self.traceroute_line_edit.text())
        tdin, stdout, stderr = ssh_cliente.exec_command( "traceroute " + str(v))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        for i in y:
            print(i)
            self.traceroute_textEdit.append(i)


    def lookup(self):
        tdin, stdout, stderr = ssh_cliente.exec_command( "dig " + str(self.lookup_line_edit.text()))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        for i in y:
            print(i)
            validar = re.search(str(self.lookup_line_edit.text()), i)
            if validar:
                self.ip_lookup_line_edit.setText(i)


    def whois(self):
        v = socket.gethostbyname(self.whois_line_edit.text())
        tdin, stdout, stderr = ssh_cliente.exec_command( "whois " + str(v))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        for i in y:
            self.whois_textEdit.append(i)

    def ipcalc(self):
        tdin, stdout, stderr = ssh_cliente.exec_command( "ipcalc " + str(self.network_ipcalc.text())+ " " + str(self.pref_ipcalc.text()))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        for i in y:
            self.ipcalc_textEdit.append(str(i))

    def sniffer(self):
        interface = self.interface_sniffer.currentText()
        var = "-i " + str(interface) + " -c " + str(self.packges_sniffer.text())

        if self.e_src_sniffer.isChecked():
            var = var + " -n -src host " + self.src_sniffer.text()
        if self.e_dst_sniffer.isChecked():
            var = var + " -n -dst host " + self.dst_sniffer.text()
        if self.e_src_port_sniffer.isChecked():
            var = var + " -n -src port " + self.src_port_sniffer.text()
        if self.e_dst_port_sniffer.isChecked():
            var = var + " -n -dst port " + self.dst_port_sniffer.text()

        var = var + " -w " +"/home/secrouter/" + self.save_sniffer.text() +".cap"

        print( "sudo tcpdump " + str(var))
        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo tcpdump " + str(var))
        x = stderr.readlines()
        y = stdout.readlines()

        print(x)
        print(y)
        sftp = ssh_cliente.open_sftp()
        sftp.get("/home/secrouter/" + self.save_sniffer.text() +".cap",self.save_sniffer.text() +".cap")
        sftp.close()


    def change_sniffer(self):
        if self.e_src_sniffer.isChecked():
            self.src_sniffer.setEnabled(True)
        else:
            self.src_sniffer.setEnabled(False)

        if self.e_dst_sniffer.isChecked():
            self.dst_sniffer.setEnabled(True)
        else:
            self.dst_sniffer.setEnabled(False)

        if self.e_src_port_sniffer.isChecked():
            self.src_port_sniffer.setEnabled(True)
        else:
            self.src_port_sniffer.setEnabled(False)

        if self.e_dst_port_sniffer.isChecked():
            self.dst_port_sniffer.setEnabled(True)
        else:
            self.dst_port_sniffer.setEnabled(False)


    def time_date(self):
        date = self.dateEdit.date().toPyDate()
        time = self.timeEdit.time().toPyTime()

        print(date)
        print(time)
        print(self.timezone.currentText())
        print("sudo date --set " + str(time))
        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo date --set " + str(date))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)

        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo  date --set " + str(time))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)

    def time_zone(self):

        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo cp /usr/share/zoneinfo/"+self.timezone.currentText() +" /etc/localtime ")
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)

    def logging(self):
        self.loggin_TextEdit.clear()
        if self.nro_linea.text() !='':
            if self.loggin_combobox.currentText() == "DHCP":
                tdin, stdout, stderr = ssh_cliente.exec_command( "sudo journalctl -u isc-dhcp-server -n "+str(self.nro_linea.text()))
                x = stderr.readlines()
                y = stdout.readlines()
                self.textEdit.clear()
                print(x)
                print(y)
                for i in y:
                    self.loggin_TextEdit.append(str(i))

            if self.loggin_combobox.currentText() == "DNS":
                tdin, stdout, stderr = ssh_cliente.exec_command( "sudo journalctl -u bind9  -n " +str(self.nro_linea.text()))
                x = stderr.readlines()
                y = stdout.readlines()
                self.textEdit.clear()
                print(x)
                print(y)
                for i in y:
                    self.loggin_TextEdit.append(str(i))

            if self.loggin_combobox.currentText() == "Firewall":
                tdin, stdout, stderr = ssh_cliente.exec_command( "sudo journalctl -u iptables  -n " +str(self.nro_linea.text()))
                x = stderr.readlines()
                y = stdout.readlines()
                self.textEdit.clear()
                print(x)
                print(y)
                for i in y:
                    self.loggin_TextEdit.append(str(i))

            if self.loggin_combobox.currentText() == "Kernel":
                tdin, stdout, stderr = ssh_cliente.exec_command( "sudo dmesg")
                x = stderr.readlines()
                y = stdout.readlines()
                self.textEdit.clear()
                print(x)
                print(y)
                for i in y:
                    self.loggin_TextEdit.append(str(i))

            if self.loggin_combobox.currentText() == "All":
                tdin, stdout, stderr = ssh_cliente.exec_command( "sudo journalctl -n " +str(self.nro_linea.text()))
                x = stderr.readlines()
                y = stdout.readlines()
                self.textEdit.clear()
                print(x)
                print(y)
                for i in y:
                    self.loggin_TextEdit.append(str(i))
        else:
            QMessageBox.warning(self,"Advertencia","numero de linea no indicado.",QMessageBox.Ok)

    def clear(Self):
        Self.loggin_TextEdit.clear()

    def reboot(self):

        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo reboot")
        exit()

    def interface_config(self):

        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo ifquery -a")
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)
        for i in y:
            self.loggin_TextEdit.append(str(i))

    def update(self):
        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo apt-get update && sudo apt-get upgrade -y")
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)

    def web(self):
        #global a
        #url = str(a)
        webbrowser.open("http://"+ ssh_ip_url + ":19999", new=2, autoraise=True)

    def backup(self):

        backup_zip = zipfile.ZipFile(str(self.backup_name.text())+'_GUI'+'.zip', 'w')

        for folder, subfolders, files in os.walk('..'):
            for file in files:
                if file.endswith('.txt'):
                    backup_zip.write(os.path.join(folder, file), file, compress_type = zipfile.ZIP_DEFLATED)

        backup_zip.close()
        print(str(self.backup_name.text())+'_GUI'+'.zip')
        sftp = ssh_cliente.open_sftp()

        sftp.put(str(self.backup_name.text())+'_GUI'+'.zip','/home/secrouter/backup/' + str(self.backup_name.text())+'_GUI'+'.zip')
        sftp.close()

        tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/sysadmin/backup_restore.py " + str(0)  + ' ' + str(self.backup_name.text()))
        x = stderr.readlines()
        y = stdout.readlines()
        print(x)
        print(y)




    def backup_type(self):
        if self.comboBox.currentText() == "USER":
            tdin, stdout, stderr = ssh_cliente.exec_command( "ls /home/secrouter/backup ")
            x = stderr.readlines()
            y = stdout.readlines()
            print(x)
            print(y)
            for i in y:
                if i != "\n":
                    self.backup_list.addItem(i[:-8])

    def restore(self):
        print(self.comboBox.currentText())
        if self.comboBox.currentText() == "USER":
            sftp = ssh_cliente.open_sftp()
            sftp.get("/home/secrouter/backup/" + self.backup_list.currentText() +'_GUI'+'.zip', self.backup_list.currentText()+'_GUI'+'.zip')
            sftp.close()


            for folder, subfolders, files in os.walk('..'):
                for file in files:
                    if file.endswith('.txt'):
                        try:
                            os.remove(file)
                        except:
                            pass

            backup_zip = zipfile.ZipFile(self.backup_list.currentText()+'_GUI'+'.zip')
            backup_zip.extractall('..\Proyecto_Main_Window')
            backup_zip.close()

            tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/sysadmin/backup_restore.py " + str(1)  + ' ' + str(self.backup_list.currentText()))

            QMessageBox.warning(self,"Advertencia","El dispositivo se reiniciara para finalizar la configuracion.",QMessageBox.Ok)
            exit()


        if self.comboBox.currentText() == "SME":
            sftp = ssh_cliente.open_sftp()
            sftp.get("/home/secrouter/backup/SME" +'_GUI'+'.zip', 'SME_GUI'+'.zip')
            sftp.close()


            for folder, subfolders, files in os.walk('..'):
                for file in files:
                    if file.endswith('.txt'):
                        try:
                            os.remove(file)
                        except:
                            pass

            backup_zip = zipfile.ZipFile('SME_GUI'+'.zip')
            backup_zip.extractall('..\Proyecto_Main_Window')
            backup_zip.close()

            tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/sysadmin/backup_restore.py " + str(1)  + ' ' + 'SME')
            QMessageBox.warning(self,"Advertencia","El dispositivo se reiniciara para finalizar la configuracion.",QMessageBox.Ok)
            exit()
        if self.comboBox.currentText() == "SoHO":
            sftp = ssh_cliente.open_sftp()
            sftp.get("/home/secrouter/backup/SOHO" +'_GUI'+'.zip', 'SOHO_GUI'+'.zip')
            sftp.close()


            for folder, subfolders, files in os.walk('..'):
                for file in files:
                    if file.endswith('.txt'):
                        try:
                            os.remove(file)
                        except:
                            pass

            backup_zip = zipfile.ZipFile('SOHO_GUI'+'.zip')
            backup_zip.extractall('..\Proyecto_Main_Window')
            backup_zip.close()

            tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/sysadmin/backup_restore.py " + str(1)  + ' ' + 'SOHO')
            QMessageBox.warning(self,"Advertencia","El dispositivo se reiniciara para finalizar la configuracion.",QMessageBox.Ok)
            exit()

#aqui
    def delete_backup(self):
        sftp = ssh_cliente.open_sftp()
        print("/home/secrouter/backup/" + self.backup_name.text() +'_GUI'+'.zip')
        print("/home/secrouter/backup/" + self.backup_name.text() +'.tar.gz')
        sftp.remove("/home/secrouter/backup/" + self.backup_name.text() +'_GUI'+'.zip')
        sftp.remove("/home/secrouter/backup/" + self.backup_name.text() +'.tar.gz')
        sftp.close()
        QMessageBox.warning(self,"Advertencia", " se ha borrado el archivo " + self.backup_name.text() +'.tar.gz',QMessageBox.Ok)

    def ntp(self):
        f = open("ntp.txt",'r')
        var = f.readline()
        f.close()

        if var == "Enable":
            self.ntp_button.setText("Enable")
            f = open("ntp.txt",'w')
            f.write("Disable")
            f.close()
            tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/sysadmin/ntp_client.py " + str(1) + ' ' + str(self.ntp_server1.text()) + ' ' + str(self.ntp_server2.text()))
            x = stderr.readlines()
            y = stdout.readlines()
            print(x)
            print(y)

        if var == "Disable":
            self.ntp_button.setText("Disable")
            f = open("ntp.txt",'w')
            f.write("Enable")
            f.close()
            tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/sysadmin/ntp_client.py " + str(0) + ' ' + str(self.ntp_server1.text()) + ' ' + str(self.ntp_server2.text()))
            x = stderr.readlines()
            y = stdout.readlines()
            print(x)
            print(y)

    def change_upload(self):
        a = True

        var = QFileDialog.getOpenFileName()
        print (var[0])
        self.file_upload.setText(var[0])


        if self.file_upload.text() != '':
            sftp = ssh_cliente.open_sftp()
            sftp.put(str(var[0]),'/home/secrouter/tmp/upload_rule.txt')
            sftp.close()
            tdin, stdout, stderr = ssh_cliente.exec_command( "sudo python3 /home/secrouter/firewall/upload_rules.py " +"upload_rule.txt")
            x = stderr.readlines()
            y = stdout.readlines()
            print(x)
            print(y)
            for i in y:
                self.upload_textEdit.append(i)

    def change_pass(self):
        global password
        self.pass_textEdit.clear()
        self.pass_textEdit.hide()
        if self.old_pass.text() == password:
            if self.new_pass.text() == self.rep_new_pass.text():
                print("echo -e "+ '\"' + str(self.old_pass.text()) +'\n' + str(self.new_pass.text()) +'\n' + str(self.rep_new_pass.text()) +'\"' +" | passwd")
                tdin, stdout, stderr = ssh_cliente.exec_command("echo -e "+ '\"' + str(self.old_pass.text()) +'\n' + str(self.new_pass.text()) +'\n' + str(self.rep_new_pass.text()) +'\"' +" | passwd")
                x = stderr.readlines()
                y = stdout.readlines()
                print(x)
                print(y)
                a = re.search("successfully",str(x))
                if not(a):
                    self.pass_textEdit.show()
                    for i in x:
                        self.pass_textEdit.append(i)

                if a:
                    password = self.new_pass.text()
                    QMessageBox.warning(self,"Exito!","clave cambiada con exito",QMessageBox.Ok)
                    self.pass_textEdit.hide()
            else:
                QMessageBox.warning(self,"Error","La nueva clave no coincide",QMessageBox.Ok)
        else:
            QMessageBox.warning(self,"Error","Clave actual invalida",QMessageBox.Ok)

    def home(self):

        if self.Maintab.currentIndex() == 0:
            tdin, stdout, stderr = ssh_cliente.exec_command("uname -n")
            x = stderr.readlines()
            a = stdout.readlines()
            for i in a:
                self.hostname.setText(i)
                tdin, stdout, stderr = ssh_cliente.exec_command("uname -m")
                x = stderr.readlines()
                b = stdout.readlines()
            for i in b:
                self.architecture.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command("sh -c 'dmesg | grep OF:'")
            c = stdout.readlines()
            for i in c:
                self.device.setText(i[38::])
                x = stderr.readlines()
            tdin, stdout, stderr = ssh_cliente.exec_command("uname -rs")
            x = stderr.readlines()
            d = stdout.readlines()
            for i in d:
                self.kernel.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command("uptime -p")
            x = stderr.readlines()
            e = stdout.readlines()
            for i in e:
                self.uptime.setText(i[3::])
            tdin, stdout, stderr = ssh_cliente.exec_command('date "+%T"')
            x = stderr.readlines()
            f = stdout.readlines()
            for i in f:
                self.time_2.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command('date "+%D"')
            x = stderr.readlines()
            g = stdout.readlines()
            for i in g:
                self.date.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command('sudo systemctl is-active isc-dhcp-server')
            x = stderr.readlines()
            h = stdout.readlines()
            for i in h:
                self.dhcp_active.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command('sudo systemctl is-active bind9')
            x = stderr.readlines()
            j = stdout.readlines()
            for i in j:
                self.dns_active.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command('sudo systemctl is-active ntp')
            x = stderr.readlines()
            g = stdout.readlines()
            for i in g:
                self.ntp_active.setText(i)
            tdin, stdout, stderr = ssh_cliente.exec_command('ls /sys/class/net')
            x = stderr.readlines()
            h = stdout.readlines()
            for i in h:
                if i != "lo":
                    self.plainTextEdit.appendPlainText("- "+i)

    def prueba1(self):
        self.Maintab.setTabText(0,"Inicio")
        self.Maintab.setTabText(1,"Ethernet y routing")
        self.Maintab.setTabText(4,"Admin. de Sis.")
        self.Maintab.setTabText(5,"Acerca de..")

        self.groupBox_34.setTitle("Informacion")
        self.groupBox_35.setTitle("Hora y Fecha")
        self.groupBox_37.setTitle("Servicios")
        self.groupBox_36.setTitle("Interfaces Disponibles")
        self.interfaces.setTitle("Interfaces Fiscias")
        self.groupBox.setTitle("Interfaz")
        self.groupBox_3.setTitle("configuración:")
        self.groupBox_4.setTitle("configuración:")
        self.static_vlan_radioButton.setText("Estatica")
        self.dns_ether_and_rout_button.setText("SERVIDOR \n DNS")
        self.interface_ether_and_rout_button_button.setText("INTERFACES \n FISICAS")
        self.Vlan.setText("CONFIGURACION \n DE VLAN")
        self.Bridge.setText(" CONFIGURACION \n DE BRIDGE ")
        self.static_routing_ether_and_rout_button.setText("ROUTING ESTATICO")
        self.Arp.setText("CONFIGURACION \n DE ARP")
        self.Vlan_config.setTitle("Configuración de Vlan:")
        self.add_vlan_Button.setText("Agregar")
        self.remove_vlan_Button.setText("Remover")
        self.static_radioButton.setText("Estatica")
        self.label_157.setText("Dispositivo")
        self.label_158.setText("Arquitectura")
        self.label_159.setText("Modelo")
        self.label_161.setText("Tiempo Activo")
        self.label_163.setText("Servidor DHCP")
        self.label_162.setText("Servidor DNS")
        self.label_20.setText("Red")
        self.label_22.setText("P. enlace")
        self.label_30.setText("Unir a")
        self.label_45.setText("Red")
        self.label_44.setText("P. enlace")
        self.Bridge_config.setTitle("Configuración de Bridge:")
        self.add_bridge_Button.setText("Agregar")
        self.remove_bridge_Button.setText("Remover")
        self.groupBox_6.setTitle("Configuración:")
        self.static_bridge_radioButton.setText("Estatica")
        self.label_24.setText("Red")
        self.label_23.setText("P. enlace")
        self.label_31.setText("Nombre")
        self.label_32.setText("Enlaza a")
        self.label_33.setText("Modo STP")
        self.static_routing.setTitle("Configuración de rutas estaticas")
        self.add_static_route_Button.setText("Agregar")
        self.remove_static_route_button.setText("Remover")
        self.groupBox_9.setTitle("Configuración:")
        self.groupBox_8.setTitle("Ruta")
        self.inter_static_route_radioButton.setText("Interfaz")
        self.label_35.setText("Interfaz")
        self.mac__static_route.setText("Red")
        self.label_42.setText("P. enlace")
        self.arp_config.setTitle("Configuración de ARP")
        self.add_arp_Button.setText("Agregar")
        self.remove_arp_button.setText("Remover")
        self.groupBox_11.setTitle("Configuración")
        self.inter_arp_radioButton.setText("Interfaz")
        self.label_37.setText("Interfaz")
        self.label_8.setText("SERVIDOR 1")
        self.label_14.setText("SERVIDOR 2")
        self.label_15.setText("SERVIDOR 3")
        self.label_16.setText('Max. caché')
        self.view_cache_button.setText("Ver caché")
        self.flush_button.setText("Vaciar caché")
        self.dns.setTitle("Caché de DNS y Forwarding")
        self.dhcp_server_button.setText("SERVIDOR \n DHCP")
        self.dhcp_server_config_box.setTitle("CONFIGURACION DE SERVIDOR DHCP")
        self.label.setText("INTERFAZ")
        self.label_2.setText("RED")
        self.label_5.setText("RANGO DE IP")
        self.label_7.setText("SERVIDOR DNS")
        self.label_9.setText("TIEMPO")
        self.arp_check_box.setText("Autoritativo")
        self.dhcp_save_button.setText("Guardar")
        self.dhcp_server_apply_button.setText("Aplicar")
        self.dhcp_server_delete_button.setText("Borrar")
        self.status_leases.setTitle("ESTADOS Y ARRENDAMIENTOS")
        self.label_12.setText("INTERFAZ")
        self.status_delete_Button.setText("Borrar")
        self.refresh_status_button.setText("Refrescar")
        self.status_leases_button.setText("ESTADOS Y \n ARRENDAMIENTOS")
        self.static_leases_button.setText("ARRENDAMIENTO \n ESTATICO")
        self.static_config_box.setTitle("ARRENDAMIENTO ESTATICO")
        self.status_client_line_edit_5.setText("INTERFAZ")
        self.status_client_line_edit_4.setText("NOMBRE")
        self.static_leases_apply_button.setText("APLICAR")
        self.dhcp_client_button.setText("CLIENTE DHCP")
        self.dhcp_client_config_box.setTitle("CLIENTE DHCP")
        self.groupBox_2.setTitle("CLIENTE:")
        self.label_34.setText("INTERFAZ")
        self.status_client_line_edit.setText("ESTADO:")
        self.network_client_label.setText("RED:")
        self.label_40.setText("P. ENLACE:")
        self.label_41.setText("SERVIDOR DNS:")
        self.client_dhcp_release_button.setText("Liberar")
        self.client_dhcp_renew_button.setText("Renovar")
        self.upload_config.setTitle("CARGAR REGLAS DESDE UN ARCHIVO")
        self.upload_button.setText("Cargar")
        self.upload.setText("CARGAR \n REGLAS")
        self.label_48.setText("Regla")
        self.label_70.setText("En")
        self.label_130.setText("ENTRADA")
        self.label_132.setText("SALIDA")
        self.label_131.setText("interfaz")
        self.label_133.setText("Interfaz")
        self.nat_apply_filter_button.setText("Aplicar")
        self.label_96.setText("Accion:")
        self.tabWidget_2.setTabText(1,"OBJETIVO")
        self.tabWidget_2.setTabText(0,"COINCIDENCIAS")
        self.label_95.setText("Para la fuente")
        self.label_114.setText("Para el destino")
        self.label_97.setText("Nivel")
        self.label_98.setText("Prefijo")
        self.label_128.setText("Puertos")
        self.label_134.setText("Puertos")
        self.label_47.setText("Reglas:")
        self.label_49.setText("en")
        self.label_50.setText("ENTRADA")
        self.label_52.setText("SALIDA")
        self.label_51.setText("interfaz")
        self.label_53.setText("interfaz")
        self.apply_filter_button.setText("Aplicar")
        self.tabWidget.setTabText(0,"CONINCIDIENCIAS")
        self.tabWidget.setTabText(1,"OBJETIVO")
        self.label_91.setText("Accion:")
        self.label_92.setText("Rechazar con")
        self.label_93.setText("Nivel")
        self.label_94.setText("Prefijo")
        self.filter_config.setTitle("FILTRO")
        self.filter.setText("FILTRO")
        self.main.setText("PRINCIPAL")
        self.main_config.setTitle("PRINCIPAL")
        self.label_46.setText("Crear cadena")
        self.add_main.setText("Añadir")
        self.delete_main.setText("Borrar")
        self.label_61.setText("Borrar regla")
        self.label_62.setText("Linea:")
        self.apply_main.setText("Aplicar")
        self.groupBox_16.setTitle("ADVERTENCIA!")
        self.label_65.setText("Politica")
        self.apply_policy.setText("Aplicar")
        self.view_main.setText("Ver")
        self.flush_main.setText("Vaciar")
        self.administration.setText("ADMINISTRACION")
        self.administration_config.setTitle("ADMINISTRACION")
        self.groupBox_29.setTitle("Administrador de contraseña:")
        self.label_135.setText("contraseña Actual")
        self.label_136.setText("Nueva contraseña")
        self.label_137.setText("Repetir contraseña")
        self.change_pass_button.setText("Aplicar")
        self.groupBox_30.setTitle("Reinicio de router:")
        self.reboot_button.setText("Reiniciar")
        self.groupBox_31.setTitle("Actualizacion del sistema:")
        self.update_button.setText("Actualizar")
        self.groupBox_32.setTitle("Restauracion del sistema:")
        self.label_138.setText("Restaurar de")
        self.restore_button.setText("restaurar")
        self.groupBox_33.setTitle("Archivos de restauracion:")
        self.label_139.setText("Nombre")
        self.backup_button.setText("Guardar")
        self.pushButton_6.setText("Borrar")
        self.time.setText("FECHA Y HORA")
        self.time_config.setTitle("FECHA Y HORA")
        self.label_140.setText("Fecha:")
        self.label_141.setText("Hora:")
        self.label_142.setText("Zona Horaria:")
        self.apply_time.setText("Aplicar")
        self.groupBox_28.setTitle("CLIENTE NTP")
        self.label_155.setText("Servidor 1")
        self.label_156.setText("Servidor 2")
        self.loggin.setText("REGISTRO")
        self.logging_config.setTitle("REGISTRO")
        self.label_154.setText("Lineas:")
        self.apply_logging.setText("Aplicar")
        self.int_config.setText("Configuracion de interfaz")
        self.refresh_button.setText("Refrescar")
        self.clear_button.setText("Limpiar")
        self.tools.setText("HERRAMIENTAS")
        self.tools_config.setTitle("HERRAMIENTAS")
        self.status.setText("ESTADO")
        self.language.setText("IDIOMAS")
        self.ping_apply.setText("Aplicar")
        self.traceroute_apply.setText("Aplicar")
        self.lookup_apply.setText("Aplicar")
        self.whois_apply.setText("Aplicar")
        self.ipcalc_button.setText("Aplicar")
        self.label_151.setText("Guardar en")
        self.start_button.setText("Aplicar")
        self.Amoungpa.setText("Cantidad de paquetes")
        self.toolBox_3.setItemText(4,"Calculadora IP")
        self.label_145.setText("Red")
        self.language_config.setTitle("SELECCION DE LENGUAJE")
        self.spanish_button.setText("Español")
        self.english_button.setText("Ingles")        #aca configuración
    def prueba2(self):
        self.Maintab.setTabText(0,"Home")
        self.Maintab.setTabText(1,"Ethernet and routing")
        self.Maintab.setTabText(4,"Sys. Admin.")
        self.Maintab.setTabText(5,"About")

        self.groupBox_34.setTitle("Information")
        self.groupBox_35.setTitle("Time and Date")
        self.groupBox_37.setTitle("Services")
        self.groupBox_36.setTitle("Available Interfaces")
        self.interfaces.setTitle("Phisical Interfaces")
        self.groupBox.setTitle("Interface")
        self.groupBox_3.setTitle("configuration:")
        self.Vlan_config.setTitle("Vlan Configuration:")
        self.remove_vlan_Button.setText("Remove")
        self.groupBox_4.setTitle("Configuration:")
        self.dns_ether_and_rout_button.setText("DNS \n SERVER")
        self.interface_ether_and_rout_button_button.setText("PHYSICAL \n INTERFACES")
        self.Vlan.setText("VLAN \n CONFIGURATION")
        self.Bridge.setText("BRIDGE \n CONFIGURATION")
        self.static_routing_ether_and_rout_button.setText("STATIC ROUTING")
        self.Arp.setText("ARP \n CONFIGURATION")
        self.add_vlan_Button.setText("Add")
        self.static_vlan_radioButton.setText("Static")
        self.static_radioButton.setText("Static")
        self.label_157.setText("Hostname")
        self.label_158.setText("Architecture")
        self.label_159.setText("Device")
        self.label_161.setText("Uptime")
        self.label_163.setText("DHCP Server")
        self.label_162.setText("DNS Server")
        self.label_20.setText("Network")
        self.label_22.setText("Gateway")
        self.label_30.setText("bond to")
        self.label_45.setText("Network")
        self.label_44.setText("Gateway")
        self.Bridge_config.setTitle("Bridge Configuration:")
        self.add_bridge_Button.setText("Add")
        self.remove_bridge_Button.setText("Remove")
        self.groupBox_6.setTitle("Configuration:")
        self.static_bridge_radioButton.setText("Static")
        self.label_24.setText("Network")
        self.label_23.setText("Gateway")
        self.label_31.setText("Name")
        self.label_32.setText("Link to")
        self.label_33.setText("STP mode")
        self.static_routing.setTitle("Static Route Configuration")
        self.add_static_route_Button.setText("Add")
        self.remove_static_route_button.setText("Remove")
        self.groupBox_9.setTitle("Configuration")
        self.groupBox_8.setTitle("Route")
        self.inter_static_route_radioButton.setText("interface")
        self.label_35.setText("Interface")
        self.mac__static_route.setText("Network")
        self.label_42.setText("Gateway")
        self.arp_config.setTitle("ARP Configuration")
        self.add_arp_Button.setText("Add")
        self.remove_arp_button.setText("Remove")
        self.groupBox_11.setTitle("Configuración")
        self.inter_arp_radioButton.setText("Interface")
        self.label_37.setText("Interface")
        self.dns.setTitle("DNS Cache and Forwarding")
        self.label_8.setText("SERVER 1")
        self.label_14.setText("SERVER 2")
        self.label_15.setText("SERVIDOR 3")
        self.label_16.setText('Max. Cache size')
        self.view_cache_button.setText("View cache")
        self.flush_button.setText("Flush cache")
        self.dhcp_server_button.setText("DHCP \n Server")
        self.dhcp_server_config_box.setTitle("DHCP SERVER CONFIG")
        self.label.setText("INTERFACE")
        self.label_2.setText("NETWORK")
        self.label_5.setText("POOL RANGE")
        self.label_7.setText("DNS SERVER")
        self.label_9.setText("LEASES TIME")
        self.arp_check_box.setText("Authoritative")
        self.dhcp_save_button.setText("Save")
        self.dhcp_server_apply_button.setText("Apply")
        self.dhcp_server_delete_button.setText("Delete")
        self.status_leases.setTitle("ESTATUS AND LEASES")
        self.label_12.setText("INTERFACE")
        self.status_delete_Button.setText("Delete")
        self.refresh_status_button.setText("Refresh")
        self.status_leases_button.setText("STATUS AND LEASES")
        self.static_leases_button.setText("STATIC LEASES")
        self.static_config_box.setTitle("STATIC LEASES CONFIG")
        self.status_client_line_edit_5.setText("INTERFACE")
        self.status_client_line_edit_4.setText("HOSTNAME")
        self.static_leases_apply_button.setText("Apply")
        self.dhcp_client_button.setText("DHCP CLIENT")
        self.dhcp_client_config_box.setTitle("DHCP CLIENT CONFIG")
        self.groupBox_2.setTitle("DHCP CLIENT:")
        self.label_34.setText("INTERFACE")
        self.status_client_line_edit.setText("STATUS:")
        self.network_client_label.setText("NETWORK:")
        self.label_40.setText("GATEWAY:")
        self.label_41.setText("DNS SERVER:")
        self.client_dhcp_release_button.setText("Release")
        self.client_dhcp_renew_button.setText("Renew")
        self.upload_config.setTitle("UPLOAD RULES FROM FILE")
        self.upload_button.setText("Upload")
        self.upload.setText("UPLOAD \n RULE")
        self.label_48.setText("Rule")
        self.label_70.setText("In")
        self.label_130.setText("IN")
        self.label_132.setText("OUT")
        self.label_131.setText("Interface")
        self.label_133.setText("Interface")
        self.nat_apply_filter_button.setText("Apply")
        self.label_96.setText("Action:")
        self.tabWidget_2.setTabText(1,"TARGET")
        self.tabWidget_2.setTabText(0,"MATCH")
        self.label_95.setText("To source")
        self.label_114.setText("To destination")
        self.label_97.setText("Level")
        self.label_98.setText("Prefix")
        self.label_128.setText("To ports")
        self.label_134.setText("To ports")
        self.label_47.setText("Rule:")
        self.label_49.setText("In")
        self.label_50.setText("IN")
        self.label_52.setText("OUT")
        self.label_51.setText("interface")
        self.label_53.setText("interface")
        self.apply_filter_button.setText("Apply")
        self.tabWidget.setTabText(0,"MATCH")
        self.tabWidget.setTabText(1,"TARGET")
        self.label_91.setText("Action:")
        self.label_92.setText("Reject with")
        self.label_93.setText("Level")
        self.label_94.setText("Prefix")
        self.filter_config.setTitle("FILTER")
        self.filter.setText("FILTER")
        self.filter_config.setTitle("FILTRO")
        self.filter.setText("FILTRO")
        self.main.setText("MAIN")
        self.main_config.setTitle("MAIN")
        self.label_46.setText("Create a chain:")
        self.add_main.setText("Add")
        self.delete_main.setText("Delete")
        self.label_61.setText("Delete rule in")
        self.label_62.setText("At line")
        self.apply_main.setText("Apply")
        self.groupBox_16.setTitle("WARNING!")
        self.label_65.setText("Add policy")
        self.apply_policy.setText("Apply")
        self.view_main.setText("View")
        self.flush_main.setText("Flush")
        self.administration.setText("ADMINISTRATION")
        self.administration_config.setTitle("ADMINISTRATION")
        self.groupBox_29.setTitle("Password management:")
        self.label_135.setText("Old password")
        self.label_136.setText("New password")
        self.label_137.setText("Repeat password")
        self.change_pass_button.setText("Apply")
        self.groupBox_30.setTitle("Router reboot:")
        self.reboot_button.setText("Reboot")
        self.groupBox_31.setTitle("system update:")
        self.update_button.setText("Update")
        self.groupBox_32.setTitle("Restore default router configuration:")
        self.label_138.setText("Restore to")
        self.restore_button.setText("restore")
        self.groupBox_33.setTitle("Actual configuration backup:")
        self.label_139.setText("Name")
        self.backup_button.setText("Save")
        self.pushButton_6.setText("Delete")
        self.time.setText("TIME AND DATE")
        self.time_config.setTitle("TIME AND DATE")
        self.label_140.setText("Date:")
        self.label_141.setText("Time:")
        self.label_142.setText("Timezone:")
        self.apply_time.setText("Apply")
        self.groupBox_28.setTitle("NTP CLIENT")
        self.label_155.setText("Server 1")
        self.label_156.setText("Server 2")
        self.logging_config.setTitle("LOGGING")
        self.label_154.setText("Lines:")
        self.apply_logging.setText("Apply")
        self.int_config.setText("Interface configuration")
        self.refresh_button.setText("Refresh")
        self.clear_button.setText("Clear")
        self.tools.setText("TOOLS")
        self.tools_config.setTitle("TOOLS")
        self.status.setText("ESTATUS")
        self.language.setText("LANGUAGE")
        self.ping_apply.setText("Apply")
        self.traceroute_apply.setText("Apply")
        self.lookup_apply.setText("Apply")
        self.whois_apply.setText("Apply")
        self.ipcalc_button.setText("Apply")
        self.label_151.setText("Save to filename")
        self.start_button.setText("Aplicar")
        self.Amoungpa.setText("Amoung of packges")
        self.toolBox_3.setItemText(4,"IP Calculator")
        self.label_145.setText("Network")
        self.language_config.setTitle("SELECT LAGUAGE")
        self.spanish_button.setText("Spanish")
        self.english_button.setText("English")

        # aqui


#-------------------------- MODULO DE VALIDACION ------------------------------
## OPCIONAL ARREGLAR REGULAR EXPRESION PARA IP'S PRIVADAS
###  CAMBIAR LAS VALIDACIONES COMO FUNCIONES

#VALIDACION DEL NETWORK LINETEXT:
    def validar_network_line_edit(self):
        network = self.network_line_edit.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",network)
        if network == "":
            self.network_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.network_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.network_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True

#VALIDACION DE SUFIJO LINETEXT:

    def validar_prefijo_line_edit(self):
        prefijo = self.prefijo_line_edit.text()
        try:
            if prefijo == "":
                self.prefijo_line_edit.setStyleSheet("no border")
                return False
            elif  int(prefijo) > 32 or int(prefijo) < 0:

                self.prefijo_line_edit.setStyleSheet("border: 1px solid red")
                return False
            else:
                self.prefijo_line_edit.setStyleSheet("border: 1px solid #00b300")
                return True
        except: self.prefijo_line_edit.setStyleSheet("border: 1px solid red")

#VALIDAR GETAWAY

    def validar_getaway_line_edit(self):
        getaway = self.getaway_line_edit.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",getaway)
        if getaway == "":
            self.getaway_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.getaway_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.getaway_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True

#VALIDAR START POOL

    def validar_pool_range_start_line_edit(self):
        start_pool   = self.pool_range_start_line_edit.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",start_pool)
        if start_pool == "":
            self.pool_range_start_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.pool_range_start_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.pool_range_start_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True

#VALIDAR STOP POOL

    def validar_pool_range_stop_line_edit(self):
        stop_pool   = self.pool_range_stop_line_edit.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",stop_pool)
        if stop_pool == "":
            self.pool_range_stop_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.pool_range_stop_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.pool_range_stop_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True


#VALIDAR DNS

    def validar_dns_server_line_edit(self):
        dns   = self.dns_server_line_edit.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",dns)
        if dns == "":
            self.dns_server_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.dns_server_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.dns_server_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True


#VALIDAR HORAS

    def validar_horas(self):
        hora = self.time_hour_line_edit.text()
        try:
            if hora == "":
                self.time_hour_line_edit.setStyleSheet("no border")
                return False
            elif  int(hora) > 72 or int(hora) < 0:
                self.time_hour_line_edit.setStyleSheet("border: 1px solid red")
                return False
            else:
                self.time_hour_line_edit.setStyleSheet("border: 1px solid #00b300")
                return True
        except: self.time_hour_line_edit.setStyleSheet("border: 1px solid red")


#VALIDAR MINUTOS

    def validar_minutos(self):
        minutos = self.time_minute_line_edit.text()
        try:
            if minutos == "":
                self.time_minute_line_edit.setStyleSheet("no border")
                return False
            elif  int(minutos) > 60 or int(minutos) < 0:
                self.time_minute_line_edit.setStyleSheet("border: 1px solid red")
                return False
            else:
                self.time_minute_line_edit.setStyleSheet("border: 1px solid #00b300")
                return True
        except: self.time_minute_line_edit.setStyleSheet("border: 1px solid red")


#VALIDAR SEGUNDOS

    def validar_segundos(self):
        segundos = self.time_second_line_edit.text()
        try:
            if segundos == "":
                self.time_second_line_edit.setStyleSheet("no border")
                return False
            elif  int(segundos) > 60 or int(segundos) < 0:
                self.time_second_line_edit.setStyleSheet("border: 1px solid red")
                return False
            else:
                self.time_second_line_edit.setStyleSheet("border: 1px solid #00b300")
                return True
        except: self.time_second_line_edit.setStyleSheet("border: 1px solid red")

#VALIDAR IP ESTATICA

    def validar_ip_static_line_edit(self):
        static_ip  = self.ip_static_line_edit.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",static_ip)
        if static_ip == "":
            self.ip_static_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.ip_static_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.ip_static_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True

#VALIDAR MAC ESTATICA

    def validar_mac_static_line_edit(self):
        static_mac  = self.mac_static_line_edit.text()
        validar = re.match(r'([0-9A-F]{2}[:-]){5}([0-9A-F]{2})',static_mac)
        if static_mac == "":
            self.mac_static_line_edit.setStyleSheet("no border")
            return False
        elif (not validar):
            self.mac_static_line_edit.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.mac_static_line_edit.setStyleSheet("border: 1px solid #00b300")
            return True

    def validar_server1_line_edit(self):
        server1 = self.server1.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",server1)
        if server1 == "":
            self.server1.setStyleSheet("no border")
            return False
        elif (not validar):
            self.server1.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.server1.setStyleSheet("border: 1px solid #00b300")
            return True

    def validar_server2_line_edit(self):
        server2 = self.server2.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",server2)
        if server2 == "":
            self.server2.setStyleSheet("no border")
            return False
        elif (not validar):
            self.server2.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.server2.setStyleSheet("border: 1px solid #00b300")
            return True

    def validar_server3_line_edit(self):
        server3 = self.server3.text()
        validar = re.match("(([2][5][0-5]\.)|([2][0-4][0-9]\.)|([0-1]?[0-9]?[0-9]\.)){3}(([2][5][0-5])|([2][0-4][0-9])|([0-1]?[0-9]?[0-9]))",server3)
        if server3 == "":
            self.server3.setStyleSheet("no border")
            return False
        elif (not validar):
            self.server3.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.server3.setStyleSheet("border: 1px solid #00b300")
            return True

    def validar_size_cache_line_edit(self):
        w = self.cache_size.text()
        validar = re.match("^[-+]?[0-9]+$",w)

        if w == "":
            self.cache_size.setStyleSheet("no border")
            return False
        elif not(validar):
            self.cache_size.setStyleSheet("border: 1px solid red")
            return False
        else:
            self.cache_size.setStyleSheet("border: 1px solid #00b300")
            return True
def run(var1,var2,var3):

    global ssh_ip_url
    global ssh_user
    global password
    ssh_ip_url= var1
    ssh_user = var2
    password= var3
    app2 = QApplication(sys.argv)
    main = Main()
    main.show()
    app2.exec_()
