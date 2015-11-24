#coding=utf-8
import requests

# curl -v 'http://tyk01.rd.mt/coremail/s/json?func=domain:getDomainConfig' -H 'Content-Type: text/x-json' -d '{domain:"qq.com",appkey:"pKGorKs="}'


url_github = 'https://api.github.com/events'
url_1 = 'http://tyk01.rd.mt/coremail/s/json'
#
# res = requests.get(url)
#
# print res.encoding
# print res.status_code
# print res.content
# print res.raw
#

payload1 = {
    'func':'getDomainConfig',
    'domain':'qq.com',
    'appkey':"pKGorKs=",
}

payload2 = {
    "func":"domain:getDomains",
    "key":"out",
    "appkey":"pKGorKs="
}

url_getDomains = 'http://tyk01.rd.mt/coremail/s/json'

import json
print json.dumps(payload2)
# r = requests.get(url_getDomains,params=json.dumps(payload2))

r = requests.post(url_getDomains,data=json.dumps(payload2))

print r.url
print r.status_code
print r.content

