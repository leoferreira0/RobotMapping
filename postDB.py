import requests
import json
from time import strftime

dadosTemp = {}
data = {}

def post(data, client):
    date = ''
    url = f'https://167.86.125.56:9200/subdomain-{client}/_doc?refresh'
    headers = {'Accept' : 'application/json', 'Content-Type' : 'application/json'}
    auth = ('admin','')

    with open (f'/tool/robot_prefect/clients/{client}/start') as file:
        for i in file:
            date = i.rstrip('\n')

    dadosTemp = {'scan.start': date, '@timestamp': strftime("%Y-%m-%dT%H:%M:%S")}
    data.update(dadosTemp)

    r = requests.post(url, headers=headers, auth=auth, data=json.dumps(data), verify=False)



