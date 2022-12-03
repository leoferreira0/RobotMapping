client=$1
dir_client=/tool/robot_prefect/clients/$client
DATE=$(date -u +%FT%TZ)

echo $DATE > $dir_client/start