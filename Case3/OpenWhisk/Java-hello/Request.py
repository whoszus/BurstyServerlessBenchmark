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
user_pass = AUTH_KEY.split(':')
response = requests.post(url, json=PARAMS, params={'blocking': BLOCKING, 'result': RESULT}, auth=(user_pass[0], user_pass[1]))
print(response.text)