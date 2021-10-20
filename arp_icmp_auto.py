import sys
import requests
import paramiko
import xml.etree.ElementTree as XTREE
import urllib3
import time
urllib3.disable_warnings()

session = requests.session()
session.verify = False
interfaces = {}
ips = {}


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
    xcmd_part2 = list(map(lambda y: '<{}>'.format(y), split_cmd))
    xcmd = ''.join(xcmd_part1) + ''.join(xcmd_part2)
    #print(xcmd)
    url = 'https://{}/api/?type=op&cmd={}&key={}'.format(sys.argv[1], xcmd, key)
    print(url)
    response = session.get(url)
    print(response.text)


def fetch_interfaces(key):
    xcmd = "<show><interface>all</interface></show>"
    url = 'https://{}/api/?type=op&cmd={}&key={}'.format(sys.argv[1], xcmd, key)
    response = session.get(url)
    root = XTREE.fromstring(response.text)
    items = root.findall("./result/ifnet/")
    for child in items:
        interfaces[child.find('name').text] =child.find('ip').text.split('/')[0]
    for k,v in list(interfaces.items()):
        if 'tunnel' in k:
          del interfaces[k]
    #print(interfaces)


def fetch_arp(key):
        xcmd = "<show><arp><entry name='all'/></arp></show>"
        url = 'https://{}/api/?type=op&cmd={}&key={}'.format(sys.argv[1], xcmd, key)
        response = session.get(url)
        root = XTREE.fromstring(response.text)
        #print(response.text)
        items = root.findall("./result/entries/")
        for child in items:
            ips[child.find('ip').text] =child.find('interface').text
        #print(ips)


def send_commands():
    session = paramiko.SSHClient()
    session.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    session.connect(sys.argv[1], username = sys.argv[2], password = sys.argv[3])
    connection = session.invoke_shell()
    time.sleep(2)
    print("Sending GARP commands for all interfaces Started:")
    for k,v in interfaces.items():
        connection.send('test arp gratuitous interface {} ip {}\n'.format(k,v))
        time.sleep(1)
    print("Done Sending GARP commands, Now verifying results:")
    print(connection.recv(1000000).decode('utf-8'))

    print("Sending Ping commands for all arp entries:")
    for k,v in ips.items():
        print('ping source {} count 2 host {}\n'.format(interfaces[v], k))
        connection.send('ping source {} count 2 host {}\n'.format(interfaces[v], k))
        time.sleep(1)


def main():
    ip = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    url = 'https://{}/api/?type=keygen&user={}&password={}'.format(sys.argv[1], sys.argv[2], sys.argv[3])
    api_key = panos_auth(url)
    #print(api_key)
    cmd = "show interface all"
    fetch_interfaces( api_key)
    fetch_arp(api_key)
    send_commands()

main()
