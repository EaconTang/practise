#coding=utf-8
'''
for 性能测试[OCM-1364]邮箱管家新邮件到达检查工具的开发
'''

import paho.mqtt.client as mqtt
import time

broker = "10.12.100.109"
broker_eclipse = "iot.eclipse.org"
broker_tyk01 = "tyk01.rd.mt"
port = 80
username = "admin@emi.cn"
passwd = "{SES}BAENmEUULoUroPNwyGUUPUkPjBpQhAkg"
subscribe_list = [("admin", 0), ("nancy", 0), ("mail", 0)]      #[(topic,qos),]


def on_connect(client,userdata,rc):
    '''callback when connected'''
    print "OK!Connected with result code " + str(rc)
    print str(client) + ' ' + str(userdata)
    #client.subscribe(subscribe_list)


def on_disconnect(client,userdata,rc):
    if rc != 0:
        print "Unexpected disconnection! ",
    print str(rc) + str(userdata)


def on_message(client,userdata,msg):
    '''
    Called when a message has been received on a topic that
    the client subscribes to.
    '''
    print "Topic: " + msg.topic + ", " + "Payload: " + str(msg.payload)


def on_publish():
    pass

def do_something():
    pass


if __name__ == '__main__':
    client = mqtt.Client()
    client.username_pw_set('user','passwd')
    client.on_connect = on_connect
    client.on_message = on_message
    #client.username_pw_set(username,passwd)
    client.on_disconnect = on_disconnect

    try:
        #client.connect(broker_eclipse)     #Connected with result code 0
        client.connect(broker)
        print "haha1"
        client.subscribe(topic="a/b/c")
        #client.loop_forever()
        while True:
             client.publish(time.ctime().__str__())
             #print "haha2"
             client.loop()
    except Exception,e:
        print time.ctime(),
        print e
    finally:
        client.disconnect()