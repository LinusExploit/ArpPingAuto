# ArpPingAuto
This will automatically connect to  a PAN OS firewall, read IP addresses of interfaces and the ARP table. 
Then it will send GARP commands for all interfaces and also will send an ICMP request for all arp entries on the firewall

<br>
─$ python3 script.py  192.168.1.245 admin Asd_12345 
<br>                                                                                                                                                              
Sending GARP commands for all interfaces Started:
<br>
Done Sending GARP commands, Now verifying results:
<br>
Last login: Thu Oct 21 11:33:18 2021 from 192.168.1.247
<br>

Number of failed attempts since last successful login: 0
<br>

test arp gratuitous interface ethernet1/1 ip 192.168.7.1
<br>
test arp gratuitous interface ethernet1/2 ip 192.168.1.70
<br>
test arp gratuitous interface ethernet1/3 ip 192.168.8.1
<br>
test arp gratuitous interface ethernet1/4 ip 1.1.1.1
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/1 ip 192.168.7.1
<br>
1 ARPs were sent
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.70
<br>
1 ARPs were sent
<br>

admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/3 ip 192.168.8.1
<br>
1 ARPs were sent
<br>

admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/4 ip 1.1.1.1
<br>
0 ARPs were sent
<br>

admin@NGFW-HOME-1(active)> 
<br>
Sending Ping commands for all arp entries:
<br>
ping source 192.168.7.1 count 2 host 192.168.7.2
<br>
ping source 192.168.1.70 count 2 host 192.168.1.1
<br>
ping source 192.168.1.70 count 2 host 192.168.1.5
<br>
ping source 192.168.1.70 count 2 host 192.168.1.60
<br>
ping source 192.168.1.70 count 2 host 192.168.1.66
<br>
ping source 192.168.1.70 count 2 host 192.168.1.67
<br>
ping source 192.168.1.70 count 2 host 192.168.1.71
<br>
ping source 192.168.1.70 count 2 host 192.168.1.110
<br>a
