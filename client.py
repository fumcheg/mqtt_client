import paho.mqtt.client as mqtt
import json
import random
import datetime
#import threading
import time

CLIENT_ID = 'paho_client_01'
BROKER_IP = '192.168.1.1'

def get_JSONMessage():
    return  json.dumps({'temperature':round(gen_value(10,20), 2),
                        'humidity':round(gen_value(28,30), 2),
                        'timestamp':str(datetime.datetime.now()),
                        'wind':round(gen_value(2,5), 2),
                        'rain':0,
                        'pressure':round(gen_value(1005,1007), 2),
                        'posLat':round(gen_value(25.041, 25.044), 4),
                        'posLon':round(gen_value(55.217, 55.220), 4)}, indent=4)

def gen_value(minv, maxv):
    return random.random() * (maxv - minv) + minv

def client_init(client_id):
    client = mqtt.Client(client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport='tcp')
    client.user_data_set({'id':client_id})
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    return client

def on_connect(client_id, userdata, flags, rc):
    print(f"client <{userdata['id']}>: Connection result is {('OK', 'NOT OK')[bool(rc)]}")

def on_publish(client_id, userdata, mid):
    print(f"client <{userdata['id']}>: Publishing message id={mid}")

def on_message(client_id, userdata, message):
    print(f"client <{userdata['id']}>: Recieved message with topic={message.topic}," +
            "payload={message.payload}, qos={message.qos}, retain={message.retain}")

def on_subscribe(client_id, userdata, mid, granted_qos):
    print(f"client <{userdata['id']}>: Subscribing request id={mid}, qos={', '.join(str(i) for i in granted_qos)}")

def pub_JSON(client):
    pub_msg = get_JSONMessage()
    client.publish('megatopic/value',pub_msg, qos=1)
    #timer = threading.Timer(5.0, pub_JSON, args=(client,))
    #timer.start()
    time.sleep(5)

if __name__ == "__main__":
    client = client_init(CLIENT_ID)
    client.connect(BROKER_IP, port=1883)
    client.subscribe('notmytopics/#', qos=2)
    client.loop_start()
    while True:
        pub_JSON(client)

    #pub_JSON(client)
    #client.loop_forever()