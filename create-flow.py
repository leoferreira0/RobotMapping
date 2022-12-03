import sys
import shutil
import subprocess
from prefect import unmapped
from prefect import task, Flow
from prefect.executors import DaskExecutor

projeto = sys.argv[1]
client = sys.argv[2]

@task
def start_scan():
    subprocess.check_output(f"sudo /tool/robot_prefect/start_scan.sh {client}", shell=True)

@task
def leitura_domain(client):
    domain_list = f'/tool/robot_prefect/clients/{client}/domains.txt'
    with open(domain_list) as file:
        lines_domain = file.readlines()
    lines_domain = list(map(str.strip, lines_domain))
    return lines_domain

@task
def start_shodan(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/api_shodan.py {client} {domain}", shell=True)

@task
def start_bynaryEdge(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/api_binaryEdge.py {client} {domain}", shell=True)

@task
def start_securityTrails(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/api_securityTrails.py {client} {domain}", shell=True)

@task
def start_assetfinder(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/tool_assetfinder.py {client} {domain}", shell=True)

@task
def start_subfinder(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/tool_subfinder.py {client} {domain}", shell=True)

@task
def start_sublist3r(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/tool_sublist3r.py {client} {domain}", shell=True)

@task
def start_amass(client, domain):
    subprocess.check_output(f"sudo python3 /tool/robot_prefect/tool_amass.py {client} {domain}", shell=True)

@task
def finish_scan():
    subprocess.check_output(f"sudo /tool/robot_prefect/finish_scan.sh {client} parallelism", shell=True)

with Flow(projeto+"_flow") as flow:
    # Variaveis
    domains = leitura_domain(client)
    # Start das sessoes
    domains.set_upstream(start_scan)
    shodan_start = start_shodan.map(unmapped(client), domains)
    amass_start = start_amass.map(unmapped(client), domains)
    assetfinder_start = start_assetfinder.map(unmapped(client), domains)
    binaryEdge_start = start_bynaryEdge.map(unmapped(client), domains)
    securityTrails_start = start_securityTrails.map(unmapped(client), domains)
    subfinder_start = start_subfinder.map(unmapped(client), domains)
    sublist3r_start = start_sublist3r.map(unmapped(client), domains)
    # Finalizacao
    finish_scan.set_upstream(shodan_start)
    finish_scan.set_upstream(amass_start)
    finish_scan.set_upstream(assetfinder_start)
    finish_scan.set_upstream(binaryEdge_start)
    finish_scan.set_upstream(securityTrails_start)
    finish_scan.set_upstream(subfinder_start)
    finish_scan.set_upstream(sublist3r_start)

# Numeros de CORES e THREADS
flow.executor = DaskExecutor(cluster_kwargs={"n_workers": 4, "threads_per_worker": 1})
# Registrar o FLOW no Projeto
flow.register(project_name=projeto)


