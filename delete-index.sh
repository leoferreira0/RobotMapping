client=$1
curl -XDELETE --insecure --user admin:'' https://167.86.125.56:9200/subdomain-$client
curl -XDELETE --insecure --user admin:'' https://167.86.125.56:9200/scan-$client


