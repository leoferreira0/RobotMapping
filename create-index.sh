client=$1
echo "[+] Criando index SUBDOMAIN"
echo
curl -XPUT --insecure --user admin:'' https://167.86.125.56:9200/subdomain-$client -H "Content-Type: application/json" -d @- <<EOF
{
        "mappings":{
                "properties":{
                        "@timestamp":{"type":"date"},
                        "server.address": {"type":"keyword"},
                        "server.domain": {"type":"keyword"},
                        "dns.nameserver": {"type":"keyword"},
                        "server.ip": {"type":"ip"},
                        "server.ipblock": {"type":"keyword"},
                        "vulnerability.scanner.vendor": {"type":"keyword"},
                        "server.registered_domain": {"type":"keyword"},
                        "server.top_level_domain": {"type":"keyword"},
                        "scan.start":{"type":"date"}
                }
        }
}
EOF
curl -XPUT --insecure --user admin:'' https://167.86.125.56:9200/scan-$client -H "Content-Type: application/json" -d @- <<EOF
{
        "mappings":{
                "properties":{
                        "@timestamp":{"type":"date"},
                        "scan.start":{"type":"date"},
                        "scan.finish":{"type":"date"},
                        "scan.type":{"type":"keyword"},
                        "scan.client":{"type":"keyword"}
                }
        }
}
EOF
mkdir /tool/robot_prefect/clients/$client
touch /tool/robot_prefect/clients/$client/domains.txt
touch /tool/robot_prefect/clients/$client/start
