import requests
import json

username='admin'
password='admin'
server_name='dal-server-2:8081'
options='?q=status:merged&o=DETAILED_ACCOUNTS&n=1'
url = 'http://'
if (username != ''):
    url = url + username + ':' + password + '@'

url = url + server_name + '/changes/'
if (options != ''):
    url = url + options

print(url)
resp = requests.get(url)

print(resp)
#print(resp.headers)
#print(resp.content)

if resp.status_code != 200:
    quit()

print(resp.content)
text = resp.content
json_str = text.decode('UTF-8')[5:]
print(json_str)

changes = json.loads(json_str)

print(changes)

