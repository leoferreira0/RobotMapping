
import sys
from prefect import Client

client = Client()
client.create_project(project_name=sys.argv[1])



