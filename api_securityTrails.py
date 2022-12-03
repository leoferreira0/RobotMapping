import consults
import postDB
import sys
import requests

def securityTrails_(client, domain):
    scanner = 'SecurityTrails'
    api_key = ''
    h = {'Accept' : 'application/json', 'Content-Type' : 'application/json', 'apiKey' : api_key}
    url = f'https://api.securitytrails.com/v1/domain/{domain}/subdomains'

    securityTrails = requests.get(url, headers = h, verify=True)

    for subdomains in securityTrails.json()['subdomains']:
        subdomain = subdomains + '.' + domain

        ip = consults.consult_ip(subdomain)

        if(ip == '0.0.0.0'):
            continue

        nameserver = consults.consult_ns(subdomain)
        block_ip = consults.consult_block(ip)

        if '.br' in domain:
            top_level_domain = domain.split('.')[1] + '.' + domain.split('.')[2]
        else:
            top_level_domain = domain.split('.')[1]

        dic_sub = {}
        dic_sub['server.address'] = subdomain
        dic_sub['server.domain'] = subdomain
        dic_sub['server.ip'] = ip
        dic_sub['server.registered_domain'] = domain
        dic_sub['server.top_level_domain'] = top_level_domain
        dic_sub['vulnerability.scanner.vendor'] = scanner
        dic_sub['dns.namersever'] = nameserver
        dic_sub['server.ipblock'] = block_ip

        postDB.post(dic_sub, client)

def main():
    client = sys.argv[1]
    domain = sys.argv[2]

    securityTrails_(client, domain)

if __name__ == "__main__":
    main()