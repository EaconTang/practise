import paho.mqtt.publish as publish



TOPIC = '[topic]test'
PAYLOAD = '[payload]test'
HOSTNAME = 'tyk01.rd.mt'
HOSTNAME_eclipse = 'iot.eclipse.org'
PORT = 6901
KEEPALIVE = 60
AUTH = {'username':'tyk','password':'123'}

msgs = [
    {
        'topic':"paho/test/multiple1",
        'payload':"multiple 1"
    },
    {
        'topic':TOPIC,
        'payload':PAYLOAD
    },
    {
        'topic':"a/b/c",
        'paload':"hello"
    }
]

#publish.single(topic=TOPIC,payload=PAYLOAD,hostname=HOSTNAME,port=PORT,keepalive=KEEPALIVE,auth=AUTH)
#publish.single(TOPIC,PAYLOAD,HOSTNAME)
publish.multiple(msgs,hostname=HOSTNAME)