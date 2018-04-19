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
       ttl_match = ""
       comment = ""
       super_match = ""
       def sma(value,salt,is_not):
           salt = salt + ' '
           return salt + value if is_not == False else salt + '! ' + value + ' '
   # ------------------------------- NAT SUB-CATEGORY -------------------------------
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
              iprange_match = '-m iprange ' + src_addr_range + ' ' + dst_addr_range+ ' '
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

           tcp_match = '-p tcp -m tcp ' + src_port_tcp + ' ' + dst_port_tcp + ' ' + tcp_flags+ ' '

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

           udp_match = '-p udp -m udp ' + src_port_udp + ' ' + dst_port_udp+ ' '

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
               protocol = self.protocol_combobox.currentText()
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

           multi_match = '-p ' + protocol + ' '+ '-m multiport ' +  src_port_multi + ' ' +  dst_port_multi+ ' '
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
               limit_rate ='--limit-rate ' + limit_rate
           else:
               limit_rate = ''
           ## Limit Burst
           if self.e_limit_burst.isChecked():
               limit_burst = self.limit_burst_line_edit.text()
               limit_burst = 'limit-burst ' + limit_burst
           else:
               limit_burst = ''

           limit_match = '-m limit ' + limit_rate + ' ' + limit_burst+ ' '
       else:
           limit_match = ''
       # Limit match END

       if self.e_time.isChecked():
           # Date Start
           if self.e_date_start.isChecked():
               date_start = self.date_start_line_edit.text()
               date_start = '--datestart ' + date_start
           else:
               date_start = ''
           # Date Stop
           if self.e_date_stop.isChecked():
               date_stop = self.date_stop_line_edit.text()
               date_stop = '--datestop ' + date_stop
           else:
               date_stop = ''

           # Time Start
           if self.e_time_start.isChecked():
               time_start = self.time_start_line_edit.text()
               time_start = '--timestart ' + time_start
           else:
               time_start = ''
           # Time Stop
           if self.e_time_stop.isChecked():
               time_stop = self.time_stop_line_edit.text()
               time_stop = '--timestop ' + time_stop
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

           time_match = '-m time '+ date_start + ' ' + date_stop + ' ' + time_start + ' ' + time_stop + ' ' + month_days + ' ' + week_days+ ' '
       else:
           time_match = ''
       # Time Match END
       # String Match
       if self.e_string.isChecked():
           # Algorithm
           if self.e_algo.isChecked():
               algo = '--algo ' + self.algo_combobox.currentText()
           else:
               algo = ''
           # From
           if self.e_from_data.isChecked():
               from_data = self.from_data_line_edit.text()
               from_data = '--from ' + from_data
           else:
               from_data = ''

           # To
           if self.e_to_data.isChecked():
               to_data = self.to_data_line_edit.text()
               to_data = '--to ' + to_data
           else:
               time_start = ''
           # String
           if self.e_check_string.isChecked():
              check_string = self.check_string_line_edit.text()
              check_string = sma(check_string,'--string',self.check_string_not.isChecked())
           else:
               check_string = ''

           string_match = '-m string ' + algo + ' ' + from_data + ' ' + to_data + ' ' + check_string+ ' '
       else:
           string_match = ''

       # String Match END

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
               ttl_gt = '--ttl-gt ' + ttl_gt
           else:
               ttl_gt = ''
           ## TTL less than
           if self.e_ttl_lt.isChecked():
               ttl_lt = self.ttl_lt_line_edit.text()
               ttl_lt = '--ttl-lt ' + ttl_lt
           else:
               ttl_lt = ''

           ttl_match = '-m ttl ' + ' ' +ttl_eq + ' ' + ttl_gt + ' ' + ttl_lt + ' '
       else:
           ttl_match = ''
       # TTL Match END

       # comment Match
       if self.e_comment.isChecked():
          comment = self.comment_line_edit.text()
          comment = '-m comment --comment ' + '\'' + 'comment' + '\'' + ' '
       else:
          comment  = ''

       # General definition of matches
       if self.e_comment.isChecked() or self.e_geoip.isChecked() or self.e_ttl.isChecked()  or self.e_string.isChecked() or  self.e_time.isChecked() or sef.e_limit.isChecked() or self.e_state.isChecked() or self.e_tcp_Match.isChecked() or self.e_multi_port.isChecked() or self.e_udp_Match.isChecked() or self.e_icmp_type.isChecked() or self.e_IP_Match.isChecked():
           super_match =  src_addr  + dst_addr + iprange_match + tcp_match  + udp_match + icmp_type
           super_match = super_match  + multi_match  +limit_match+ time_match + state + string_match + ttl_match
           super_match = super_match   + comment

       # NAT TARGETS : MASQUERADE - REDIRECT - SNAT - DNAT - LOG
       x = self.action_combobox.currentText()
       if x == "MASQUERADE": # ONLY FOR POSTROUTING CHAIN
           action = '-j MASQUERADE '
           if self.e_masquerade_to_ports.isChecked():
               action = action + '--to-ports ' + masquerade_to_ports_line_edit.text() # -j MASQUERADE --to-ports 1-1024
       if x == "REDIRECT": # ONLY FOR PREROUTING AND POSTROUTING CHAIN
           action = '-j REDIRECT '
           if self.e_redirect_to_ports.isChecked():
               action = action + '--to-ports ' + redirect_to_ports_line_edit.text() # -j REDIRECT --to-ports 1-1024
       if x == "SNAT": # ONLY FOR INPUT AND  POSTROUTING CHAIN
           action = '-j SNAT --to-source ' + snat_to_source_line_edit.text() # -j SNAT --to-source [ipaddr[-ipaddr]][:port[-port]]
       if x == "DNAT": # ONLY FOR OUTPUT AND  PREROUTING CHAIN
           action = '-j DNAT --to-destination ' + redirect_to_ports_line_edit.text() # -j DNAT --to-destination [ipaddr[-ipaddr]][:port[-port]]
       if x == "LOG":
           action = '-j LOG --log-level' + self.log_combobox.currentText() + ' --log-prefix ' + self.prefix_line_edit.text()
       print(action)
