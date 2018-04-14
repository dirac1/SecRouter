def interface(self):
      #self.interface_comboBox.clear()
      sftp = ssh_cliente.open_sftp()
      interfaces = sftp.listdir(path="/sys/class/net")
      for i in interfaces:
          if i != "lo":
              self.interface_comboBox.addItem(i)

    def apply_button (self):
        
        def sma(value,salt):
            salt = salt + ' '
            check = value +'_check_box'
              if self.check.isChecked():
                  is_not = True
              else:
                  is_not = False
           return salt + value if is_not else salt + '! ' + value
    # ------------------------------- FILTER SUB-CATEGORY -------------------------------   
    # --- MATCHES ---
        # IP match
        ## Source Address 
        if e_IP_Match == True:
            if e_src_addr == True:
                src_addr = self.src_addr_line_edit.text()
                src_addr = sma(src_addr,'-s')
            else:
                src_addr = ''
            ## Destination Address 
            if e_dst_addr==True:
                dst_addr = self.dst_addr_line_edit.text()
                dst_addr = sma(src_addr,'-s')
            else:
                dst_addr = ''
            ## iprange sub-match
            ### Source Address Range 
            if e_src_addr_range == True:
                src_addr_range = self.src_addr_range.text()
                src_addr_range = sma(src_addr_range,'--src-range')
            else:
                src_addr_range = ''

            ### Destination Address Range
            if e_dst_addr_range == True:
                dst_addr_range = self.dst_addr_range.text()
                dst_addr_range = sma(dst_addr_range,'--dst-range')
            else:
                dst_addr_range = ''

            iprange_rule = '-m iprange ' + src_addr_range + dst_addr_range
            ip_rule = src_addr + ' ' + dst_addr + ' ' + iprange_rule
        else:
            ip_rule = ''
        # IP match END

        # Port match

        ## TCP match
        if e_tcp_Match == True:
        ### Source Port
            if e_src_port_tcp == True:
                src_port_tcp = self.src_port_tcp_line_edit.text()
                src_port_tcp = sma(src_port_tcp,'--sport')
            else:
                src_port_tcp = ''
            ### Destination Port
            if e_dst_port_tcp == True:
                dst_port_tcp = self.dst_port_tcp_line_edit.text()
                dst_port_tcp = sma(dst_port_tcp,'--dport')
            else:
                dst_port_tcp = ''
            ### TCP Flag
            if e_tcp_flags == True:
                tcp_flags = self.tcp_flags_line_edit.text()
                tcp_flags = '--tcp-flags ' + tcp_flags
            else:
                tcp_flags = ''

            tcp_match = '-p tcp -m tcp ' + src_port_tcp + ' ' + dst_port_tcp + ' ' + tcp_flags
        else:
            tcp_match = ''


        ## UDP match
        ### Source Port
        if e_udp_Match == True:
            if e_src_port_udp == True:
                src_port_udp = self.src_port_udp_line_edit.text()
                src_port_udp = sma(src_port_udp,'--sport')
            else:
                src_port_udp = ''
            ### Destination Port
            if e_dst_port_udp == True:
                dst_port_udp = self.dst_port_udp_line_edit.text()
                dst_port_udp = sma(dst_port_udp,'--dport')
            else:
                dst_port_udp = ''

            udp_match = '-p udp -m udp ' + src_port_udp + ' ' + dst_port_udp

        ## icmp match
        ### icmp type
        if e_icmp_type == True:
            icmp_type = self.icmp_type_line_edit.text()
            icmp_type = sma(icmp_type,'-p icmp -m icmp --icmp-type')
        else:
            icmp_type = ''

        ## Multiport match
        if e_multi_port == True:
        # FALTA EL COMBO BOX Que selecciona el protocolo
            protocol = '-p ' + protocol
            ### Source Port
            if e_src_port_multi == True:
                src_port_multi = self.src_port_multi_line_edit.text()
                src_port_multi = sma(src_port_multi,'--sport')
            else:
                src_port_multi = ''
            ### Destination Port
            if e_dst_port_multi == True:
                dst_port_multi = self.dst_port_multi_line_edit.text()
                dst_port_multi = sma(dst_port_multi,'--dport')
            else:
                dst_port_multi = ''

            multi_match = protocol + ' ' +  src_port_multi + ' ' +  dst_port_multi
        else:
            multi_match = ''
        ## Multiport match END
        # Port match END

        # State match
        if e_state == True:
            state = self.state_line_edit.text()
            state = sma(state,'-m state --state')
        else:
            state = ''
        # State match END

        # Limit match
        ## Limit Rate 
        if e_limit == True:
            if e_limit_rate == True:
                limit_rate = self.limit_rate_line_edit.text()
                limit_rate ='--limit-rate ' + limit_rate
            else:
                limit_rate = ''
            ## Limit Burst 
            if e_limit_burst == True:
                limit_burst = self.limit_burst_line_edit.text()
                limit_burst = 'limit-burst ' + limit_burst
            else:
                limit_burst = ''

            limit_match = '-m limit ' + limit_rate + ' ' + limit_burst
        else:
            limit_match = ''
        # Limit match END

        # Time Match
        # --datestart YYYY[-MM[-DD[Thh[:mm[:ss]]]]]
        # --datestop YYYY[-MM[-DD[Thh[:mm[:ss]]]]]
        # --timestart hh:mm[:ss]
        # --timestop hh:mm[:ss]
        # [!] --monthdays day[,day...]
        # [!] --weekdays day[,day...]
        if e_time == True:
            # Date Start
            if e_date_start == True:
                date_start = self.date_start_line_edit.text()
                date_start = '--datestart ' + date_start
            else:
                date_start = ''
            # Date Stop
            if e_date_stop == True:
                date_stop = self.date_stop_line_edit.text()
                date_stop = '--datestop ' + date_stop
            else:
                date_stop = ''

            # Time Start
            if e_time_start == True:
                time_start = self.time_start_line_edit.text()
                time_start = '--timestart ' + time_start
            else:
                time_start = ''
            # Time Stop
            if e_time_stop == True:
                time_stop = self.time_stop_line_edit.text()
                time_stop = '--timestop ' + time_stop
            else:
                time_stop = ''

            # Month Days 
            if e_month_days == True:
                month_days = self.month_days_line_edit.text()
                month_days = sma(month_days,'--monthdays')
            else:
                month_days = ''
            # Week Days    
            if e_week_days == True:
                week_days = self.week_days_line_edit.text()
                week_days = sma(week_days,'--monthdays')
            else:
                week_days = ''

            time_match = '-m time ' date_start + ' ' + date_stop + ' ' + time_start + ' ' + time_stop + ' ' + month_days + ' ' + week_days
        else:
            time_match = ''
        # Time Match END

        # String Match
        if e_string == True:
            # Algorithm
            if e_algo == True:
                algo = self.algo_line_edit.text()
                algo = '--algo ' + algo # [ bmp | kmp ]
            else:
                algo = ''
            # From
            if e_from_data == True:
                from_data = self.from_data_line_edit.text()
                from_data = '--from ' + from_data
            else:
                from_data = ''

            # To
            if e_to_data == True:
                to_data = self.to_data_line_edit.text()
                to_data = '--to ' + to_data
            else:
                time_start = ''
            # String
            if e_check_string == True:
               check_string = self.check_string_line_edit.text()
                check_string = sma(check_string,'--string')
            else:
                check_string = ''

            string_match = '-m string ' + algo + ' ' + from_data + ' ' + to_data + ' ' + check_string
        else:
            string_match = ''
        # String Match END

        # MAC Match
            if e_mac == True:
               mac = self.mac_line_edit.text()
               mac = sma(mac,'-m mac --mac-source') # ONLY FOR INPUT AND FORWARD CHAIN!
            else:
                mac = ''
        # MAC Match END

        # TTL Match
        # -m ttl --ttl-eq --ttl-gt --ttl-lt 
        if e_ttl == True:
            ## TTL equal
            if e_ttl_eq == True:
               ttl_eq = self.ttl_eq_line_edit.text()
               ttl_eq = sma(ttl_eq,'--ttl-eq')
            else:
                ttl_eq  = ''
            ## TTL greater than
            if e_ttl_gt == True:
                ttl_gt = self.ttl_gt_line_edit.text()
                ttl_gt = '--ttl-gt ' + ttl_gt
            else:
                ttl_gt = ''
            ## TTL less than
            if e_ttl_lt == True:
                ttl_lt = self.ttl_lt_line_edit.text()
                ttl_lt = '--ttl-lt ' + ttl_lt
            else:
                ttl_lt = ''

            ttl_match = '-m ttl ' + ttl_eq + ttl_gt + ttl_lt
        else:
            match_ttl = ''
        # TTL Match END

        # geoIP Match
        if e_geoip == True:
           geoip = self.geoip_line_edit.text()
           geoip = sma(geoip,'-m geoip --source-country')
        else:
           geoip  = ''
        # geoIP Match END

        # comment Match
        if e_comment == True:
           comment = self.comment_line_edit.text()
           comment = sma(comment,'-m comment --comment')
        else:
           comment  = ''
        # geoIP Match END

        # General definition of matches
        super_match =  ip_match + ' ' + tcp_match + ' ' + udp_match + ' ' + icmp_type + ' ' + multi_match + ' ' + \
                       limit_match + ' ' + time_match + ' ' + state + ' ' + string_match + ' ' + mac ' ' + \
                       ttl_match + ' ' + geoip + ' ' + comment
    # --- TARGETS ---
    #
    # --jump -j will be used to jump to different targets
    #  As stated before you can jump to other chains using --jump [ USER_DEFINED | INPUT | FORWARD | OUTPUT ]
    # The targets for secrouter be will be ACCEPT - DROP - RETURN - REJECT - LOG
    #
    # ACTION : ACCEPT (accept the packet), DROP (drops the packet), RETURN (Go back to the original Chain) 
    # ACTION : REJECT 	--reject-with [options] (will send a response to the hosts matching this rule )
    # ACTION : LOG
    # --log-level level
    #     Level of logging, which can be (system-specific) numeric or a mnemonic. Possible values are (in decreasing order of priority): emerg, alert, crit, error, warning, notice, info or debug.
    # --log-prefix prefix
    #     Prefix log messages with the specified prefix; up to 29 letters long, and useful for distinguishing messages in the logs.
    # --log-tcp-options
    #     Log options from the TCP packet header.
    # --log-ip-options
    #     Log options from the IP/IPv6 packet header.




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
      #except:
      #    QMessageBox.warning(self,"Advertencia","Uno o varios de los campos son incorrectos.",QMessageBox.Ok)
