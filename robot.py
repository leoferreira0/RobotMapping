import sys
import os
import api_binaryEdge
import api_securityTrails
import api_shodan
import tool_amass
import tool_assetfinder
import tool_subfinder
import tool_sublist3r

def main():
    client = sys.argv[1]

    os.system(f"sh /tool/robot_prefect/start_scan.sh {client}")

    with open (f'/tool/robot_prefect/clients/{client}/domains.txt') as file:
        for domain in file:
            domain = domain.rstrip('\n')
            
            api_shodan.shodan_(client, domain)
            api_binaryEdge.binaryEdge_(client, domain)
            api_securityTrails.securityTrails_(client, domain)
            tool_amass.amass_(client, domain)
            tool_assetfinder.assetfinder_(client, domain)
            tool_subfinder.subfinder_(client, domain)
            tool_sublist3r.sublist3r_(client, domain)

    os.system(f"sh /tool/robot_prefect/finish_scan.sh {client} not_parallelism")

if __name__ == "__main__":
    main()