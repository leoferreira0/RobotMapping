client=$1
tipo=$2

finish=$(date -u +%FT%TZ)
scan_start=$(cat /tool/robot_prefect/clients/$client/start)
echo $scan_start
curl -XPOST --insecure --user admin:'' https://167.86.125.56:9200/scan-$client/_doc?refresh -H "Content-Type: application/json" -d @- <<EOF
    {
    "@timestamp":"$finish",
    "scan.start":"$scan_start",
    "scan.finish":"$finish",
    "scan.type":"$tipo",
    "scan.client":"$client"
    }
EOF


