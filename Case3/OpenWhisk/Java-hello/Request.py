import subprocess
import requests

APIHOST = 'https://172.16.101.166:31001'
AUTH_KEY = subprocess.check_output("wsk property get --auth", shell=True).split()[2] 
NAMESPACE = 'guest'
ACTION = 'guest/hello-java'
PARAMS = {'name':'tinker'}
BLOCKING = 'true'
RESULT = 'true'

url = APIHOST + '/api/v1/namespaces/' + NAMESPACE + '/actions/' + ACTION
user_pass = AUTH_KEY.decode().split(':')
# response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=('guest', '23bc46b1-71f6-4ed5-8c54-816aa4f8c502:123zO3xZCLrMN6v2BKK1dXYFpXlPkccOFqm12CdAsMgRU4VrNZ9lyGVCGuMDGIwP'))
print(response.text)