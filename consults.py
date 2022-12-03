import socket
import requests

def consult_ip(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except:
        return '0.0.0.0'

def consult_ns(subdomain):
    try:
        h = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        rdap_domain = requests.get(f'https://www.rdap.net/domain/{subdomain}', headers = h)
        nameserver = ''
        for nameservers in rdap_domain.json()['nameservers']:
            nameserver = nameserver + nameservers['ldhName'] + ', '

        return nameserver
    except:
        return 'NA'

def consult_block(ip):
    try:
        h = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
        rdap_ip = requests.get(f'https://www.rdap.net/ip/{ip}', headers = h)
        block_ip = rdap_ip.json()['handle']
    
        return block_ip
    except:
        return 'NA'




        