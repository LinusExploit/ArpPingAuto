This script automatically connect to a PANOS firewall and will do the followings:
<br>
1)Collect Interface ip addresses
<br>
2)Collect ARP entries from the firewall
<br>
3)Collect Translated Source and Destination Entries in NAT Policies 
<br>
4)Send GARP for interface ips 
<br>
5)Send GARP for natted addresses based on ussr request 
<br>
6)Send ICMP packets for each arp entry based on user request 
<br>

<br>
Note: Currently the script is doing the work on the policies that are pushed from Panorama to the firewall.
<br>

<br>
Below is an example of running the script. Please Check the options at the launch of the script for your case. Once all info is collected script will pause simulating an actual 
<br>
migration where you will need the commands after the switch over to the new firewalls. 
<br>
<br>

Note: For NAT functionarlity currently the script support rules pushed from Panorama and it still lacks the capability to resolve addresses objects if names are used. 

# main.py 192.168.1.245 admin xxxxx
<br>
Is Sending ICMP for ARP entries required? (Yes | No).No
<br>
Is Sending GARP for NAT entries required? (Yes | No).Yes
<br>
Fetching all interfaces from the device Started!
<br>
Fetching IPs in Source Translation and Dynamic Translation Policies Started!
<br>
Fetching IPs in Source Translation and Dynamic Translation Policies Completed!
<br>
Do you want to execute the commands now ? (Yes|No). Yes
<br>
Sending GARP commands for all interfaces Started!
<br>
Sending GARP commands NAT Policies Started!
<br>
Done Sending GARP commands
<br>
Sending Ping commands for all arp entries!
<br>
<br>
<br>
<br>
Number of failed attempts since last successful login: 0
<br>
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
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.70
<br>
1 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/3 ip 192.168.8.1
<br>
1 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/4 ip 1.1.1.1
<br>
0 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.14
<br>
1 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.23
<br>
1 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.24
<br>
1 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.102
<br>
1 ARPs were sent
<br>
<br>
admin@NGFW-HOME-1(active)> test arp gratuitous interface ethernet1/2 ip 192.168.1.104
<br>
1 ARPs were sent
<br>
>admin@NGFW-HOME-1(active)> 
<br>
Process finished with exit code 0
<br>
