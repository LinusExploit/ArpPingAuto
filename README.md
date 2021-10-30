# ArpPingAuto
This will automatically connect to  a PAN OS firewall, read IP addresses of interfaces and the ARP table. 
Then it will send GARP commands for all interfaces and also will send an ICMP request for all arp entries on the firewall

>> main.py 192.168.1.245 admin Asd_12345<br>
Is Sending ICMP for ARP entries required? (Yes | No).No<br>
Is Sending GARP for NAT entries required? (Yes | No).Yes<br>
Fetching all interfaces from the device Started!<br>
Fetching IPs in Source Translation and Dynamic Translation Policies Started!<br>
Fetching IPs in Source Translation and Dynamic Translation Policies Completed!<br>
Do you want to execute the commands now ? (Yes|No). Yes<br>
Sending GARP commands for all interfaces Started!<br>
Sending GARP commands NAT Policies Started!<br>
Done Sending GARP commands<br>
Sending Ping commands for all arp entries!<br>
<br>



Number of failed attempts since last successful login: 0<br>
<br>

test arp gratuitous interface ethernet1/1 ip 192.168.7.1<br>
test arp gratuitous interface ethernet1/2 ip 192.168.1.70<br>
test arp gratuitous interface ethernet1/3 ip 192.168.8.1<br>
test arp gratuitous interface ethernet1/4 ip 1.1.1.1<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/1 ip 192.168.7.1<br>
<br>
1 ARPs were sent<br>
<br>

admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.70<br>

1 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/3 ip 192.168.8.1<br>

1 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/4 ip 1.1.1.1<br>

0 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.14<br>

1 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.23<br>

1 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.24<br>

1 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.102<br>

1 ARPs were sent<br>


admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.104<br>

1 ARPs were sent<br>

>admin@NGFW-HOME-1(active)> <br>

Process finished with exit code 0<br>
