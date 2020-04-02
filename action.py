from RebootMachinesObj import RebootMachinesObj
from RebootGroupsObj import RebootGroupsObj
from novaclient.client import Client
from DataObj import DataObj
import urllib.parse
import requests
import time
import json
import os


def get_nova_credentials_v2():
    d = {}
    d['version'] = os.environ['OS_NOVA_VERSION']
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    d['user_domain_name'] = os.environ['OS_USER_DOMAIN_NAME']
    return d


credentials = get_nova_credentials_v2()
nova_client = Client(**credentials)
sList = nova_client.servers.list()

url = os.environ['OS_AUTH_URL'] + "/auth/tokens"
r1 = urllib.parse.urlsplit(url)
temp = r1.netloc
domain = temp.split(':')[0]

data = {"auth": {
    "identity": {
        "methods": ["password"],
        "password": {
            "user": {
                "name": os.environ['OS_USERNAME'],
                "domain": {"id": "default"},
                "password": os.environ['OS_PASSWORD']
            }
        }
    },
    "scope": {
        "project": {
            "name": os.environ['OS_PROJECT_NAME'],
            "domain": {"id": "default"}
        }
    }
}
}
headers = {'Content-type': "application/json", 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
token = None
headers = r.headers

if headers.get('X-Subject-Token') is not None:
    token = headers.get('X-Subject-Token')
elif headers.get('x-subject-token') is not None:
    token = headers.get('x-subject-token')
else:
    print('Headers is not valid!')
    exit(-1)
url = "https://" + domain + ":8774/v2.1/os-server-groups"
headers = {'X-Auth-Token': token}
r = requests.get(url, headers=headers)

computerListObjects = []

for item in json.loads(r.text)['server_groups']:
    computerListObjects.append(DataObj(item))

delay_time = None
if os.environ['DELAY'] == '':
    delay_time = 5
    print('Delay not specified, default delay is 5 min')
else:
    delay_time = int(os.environ['DELAY'])

delay = 60 * delay_time
close_time = time.time() + delay

percent = None
if os.environ['PERCENT'] == '':
    percent = 30
    print('Percentage not specified, default percent is 30%')
else:
    percent = int(os.environ['PERCENT'])

print('\nReboot machines in server groups')
rebootMachinesObj = RebootMachinesObj(sList, computerListObjects, close_time, percent)
rebootMachinesObj.reboot_percent_machines()
print('-' * 40)
print('\nReboot machines')
reboot_groups = RebootGroupsObj(nova_client, computerListObjects, close_time, percent)
reboot_groups.reboot_percent_machines()
print('-' * 40)
