import sys
import postDB
import consults
import os

def sublist3r_(client, domain):
    scanner = 'Sublist3r'

    os.system("rm /tool/robot_prefect/tmp/sublist3r.tmp")
    os.system("touch /tool/robot_prefect/tmp/sublist3r.tmp")

    os.system("docker run --rm -v "+"/tool/robot_prefect/tmp:/tmp "+"tool-kali:1.0 sublist3r -d " +domain+ " -o /tmp/sublist3r.tmp")
    with open ('/tool/robot_prefect/tmp/sublist3r.tmp') as file:
        for subdomains in file:
            subdomain = subdomains.rstrip('\n')

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

    os.system("rm /tool/robot_prefect/tmp/sublist3r.tmp")

def main():
    client = sys.argv[1]
    domain = sys.argv[2]

    sublist3r_(client, domain)

if __name__ == "__main__":
    main()