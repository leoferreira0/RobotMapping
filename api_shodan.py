import consults
import postDB
import sys
import shodan

def shodan_(client, domain):
    scanner = 'Shodan'
    api_key = '6R4vFs9GQnv80gHv1HbpPCjlp69mGxjj'
    api = shodan.Shodan(api_key)
    result = api.search('hostname:'+domain)
    lista = []

    for matches in result['matches']:
        for hostname in matches['hostnames']:

            if domain in hostname:
                lista = lista + [hostname]

    for subdomains in lista:
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

    shodan_(client, domain)

if __name__ == "__main__":
    main()
