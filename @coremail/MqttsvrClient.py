#coding=utf-8
'''
for 性能测试[OCM-1364]邮箱管家新邮件到达检查工具的开发
'''

import paho.mqtt.client as mqtt

broker = "10.12.100.109"
port = 6900
username = "admin@emi.cn"
passwd = "{SES}BAENmEUULoUroPNwyGUUPUkPjBpQhAkg"
subscribe_list = [("admin", 0), ("nancy", 0), ("mail", 0)]

def on_connect(client,userdata,flags,rc):
    '''callback when connected'''
    print "Connected with result code " + str(rc)
    client.subscribe(subscribe_list)

def on_message(client,userdata,msg):
    '''callback when receive message'''
    print "Topic: " + msg.topic + ", " + "Payload: " + str(msg.payload)


def do_something():
    pass

if __name__ == '__main__':
    client = mqtt.Client()
    #client.username_pw_set(username,passwd)
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(broker,port,60)
        client.loop_forever()
    except Exception,e:
        print e
    finally:
        client.disconnect()