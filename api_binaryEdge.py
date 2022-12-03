import consults
import postDB
import sys
import requests

def binaryEdge_(client, domain):
    scanner = 'BinaryEdge'
    api_key = '932d0151-d1e1-495b-b8c8-f03efac0b837'
    h = {'Accept' : 'application/json', 'Content-Type' : 'application/json', 'X-Key' : api_key}
    url = f'https://api.binaryedge.io/v2/query/domains/subdomain/{domain}'

    binaryedge = requests.get(url, headers = h, verify=True)

    for subdomains in binaryedge.json()['events']:
        subdomain = subdomains

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

    binaryEdge_(client, domain)

if __name__ == "__main__":
    main()
