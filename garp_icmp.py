# This is a sample Python script.

import sys
import requests
import paramiko
import xml.etree.ElementTree as XTREE
import urllib3
import time
import json
import re
import ipaddress as ip

urllib3.disable_warnings()

session = requests.session()
session.verify = False
interfaces = {}
interfaces_masks  = {}
ips = {}
nat_ips = []            #a list of nat rules , each entry is a dictionary of rule name and mapped ips
nat_garp = {}


                        # check if ip is part of the network
def is_In_Network(ip_value, network):
    return ip.ip_address(ip_value) in ip.ip_network(network)



                        # Connect to the firewall collect version and number of virtual systems
def fetch_info(key):
    pass

def fetch_nat(key):
    print('Fetching IPs in Source Translation and Dynamic Translation Policies Started!')
    # this is a function that looks at nat entries on the firewall  it checks for mapped addresses in snat and dnat and send a DARP for these entries

    # We will first extract the firewall version to be used in the URLs
    # we will execute the show system info command on the firewall
    response = send_command_global('show system info', key)
    root = XTREE.fromstring(response)
    item = root.find("./result/system/sw-version")
    sw_version = re.findall(r'(^\d{1,2}\.\d{1,2})\.', item.text)[0]

    # This will be using restapi as each rule will be parsed easily within the json dictionary directly
    # the url is:
    # curl -H 'X-PAN-KEY: token' -k  -X GET 'https://192.168.1.245/restapi/v10.0/Policies/NatRules?location=panorama-pushed'
    url = 'https://{}/restapi/v{}/Policies/NatRules?location=panorama-pushed&vsys=vsys1'.format(sys.argv[1], sw_version,key)

    response = session.get(url, headers = {'X-PAN-KEY':key})

    #convert the response into a dictionary python object
    result = json.loads(response.text)

    # each value inside key path result -> entry of the response is a nat policy on the firewall
    for rule in result['result']['entry']:

        # check for source translation in the rule:
        if 'source-translation' in rule.keys():

            # parse the type of the nat translation so we can lookup the mapped ip.
            nat_type=list(rule['source-translation'].keys())[0]

            # skip if the translated address belong to the interface.
            if('interface-address' in rule['source-translation'][nat_type].keys()):
                continue

            # find the mapped ip inside the dictionary result. This is either
            # a dictionary with member key that has a list of the translated addresses or
            # a direct string with the name of the mapped address

            mapped_ip = rule['source-translation'][nat_type]['translated-address']

            # To cover the first case where the translated address is a member dictionary
            if 'dict' in str(type(mapped_ip)):
                # get the list of the mapped ips which is the value of of the member key
                members = mapped_ip['member']
                # store the mapped ips inside the nat_ips array
                for ip in members:
                    nat_ips.append(ip)
            # This is to cover the case where the value of translated address dictionary is not a dictionary but a direct string
            else:
                nat_ips.append(mapped_ip)

        # Check if the rule has a destination translation and parse the destination ip
        if 'destination-translation' in rule.keys():
            # Here we just need to find the pre-nat ip which can be directly done via accesing the destination key in the rule
           for item in rule['destination']['member']:
               nat_ips.append(item)



        # This is a function that takes the mapped ip as an input and returns the interface on which they are routed to Send a proper GARP
        # Inputs are the array of mapped ip addresses

        #This is a function to associated natted ip addresses with an interface as we will send arp entries only
        # to ips that belong to an interface subnet
    print('Fetching IPs in Source Translation and Dynamic Translation Policies Completed!')

def associate_mapped_ips():
    #iterate over the natted ip addresses
    for ip in nat_ips:
        # if the entry is a valid ipv4 address
        if re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', ip):
            for k,v in interfaces_masks.items():
                if is_In_Network(ip, v):
                    nat_garp[ip] = k
                    continue




def panos_auth(url):
    session = requests.session()
    session.verify = False
    response = session.get(url)
    root = XTREE.fromstring(response.text)
    return root.find('./result/key').text


def send_command_global(cmd, key):
    split_cmd=cmd.split(' ' )
    xcmd_part1 = list(map(lambda y: '<{}>'.format(y), split_cmd))
    split_cmd.reverse()
    xcmd_part2 = list(map(lambda y: '</{}>'.format(y), split_cmd))
    xcmd = ''.join(xcmd_part1) + ''.join(xcmd_part2)
    url = 'https://{}/api/?type=op&cmd={}&key={}'.format(sys.argv[1], xcmd, key)
    response = session.get(url)
    return response.text


def fetch_interfaces(key):
    print("Fetching all interfaces from the device Started!")
    xcmd = "<show><interface>all</interface></show>"
    url = 'https://{}/api/?type=op&cmd={}&key={}'.format(sys.argv[1], xcmd, key)
    response = session.get(url)
    root = XTREE.fromstring(response.text)
    items = root.findall("./result/ifnet/")
    for child in items:
        if 'tunnel' in child.find('name').text or 'loop' in child.find('name').text:
            continue
        interfaces[child.find('name').text] =child.find('ip').text.split('/')[0]
        if (child.find('ip').text != 'N/A'):
            ifc = ip.IPv4Interface(child.find('ip').text).network
            interfaces_masks[child.find('name').text] = str(ifc)




def fetch_arp(key):
        print("Fetching all arp entries from the device Started!")
        xcmd = "<show><arp><entry name='all'/></arp></show>"
        url = 'https://{}/api/?type=op&cmd={}&key={}'.format(sys.argv[1], xcmd, key)
        response = session.get(url)
        root = XTREE.fromstring(response.text)
        items = root.findall("./result/entries/")
        for child in items:
            ips[child.find('ip').text] =child.find('interface').text


def send_commands(nat_flag, icmp_flag):
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(sys.argv[1], username = sys.argv[2], password = sys.argv[3])
    connection = session.invoke_shell()
    time.sleep(2)
    print("Sending GARP commands for all interfaces Started!")
    for k,v in interfaces.items():
        connection.send('test arp gratuitous interface {} ip {}\n'.format(k,v))
        time.sleep(1)
    if (nat_flag):
        print("Sending GARP commands NAT Policies Started!")
        for k,v in nat_garp.items():
           connection.send('test arp gratuitous interface {} ip {}\n'.format(v, k))
           time.sleep(1)

    print("Done Sending GARP commands")

    if (icmp_flag):
        print("Sending Ping commands for all arp entries!")
        for k,v in ips.items():
          print('ping source {} count 2 host {}'.format(interfaces[v], k))
          connection.send('ping source {} interval 1 count 2 host {}\n'.format(interfaces[v], k))
          time.sleep(1)

    print(connection.recv(100000).decode('utf-8'))

def start():
    ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    switch_arp = input('Is Sending ICMP for ARP entries required? (Yes | No).')
    switch_nat = input('Is Sending GARP for NAT entries required? (Yes | No).')

    url = 'https://{}/api/?type=keygen&user={}&password={}'.format(sys.argv[1], sys.argv[2], sys.argv[3])
    api_key = panos_auth(url)
    cmd = "show interface all"
    fetch_interfaces( api_key)
    if switch_arp == 'Yes':
        fetch_arp(api_key)
    if switch_nat == 'Yes':
        fetch_nat(api_key)
        associate_mapped_ips()

    switch = input('Do you want to execute the commands now ? (Yes|No). ')

    if (switch == 'Yes'):
        send_commands(switch_nat, switch_arp)

    else:
        print('Exiting without sending any command to the device!\nPlease Run the Script Again if Needed!')
        sys.exit()


if __name__ == '__main__':
    start()

