import paho.mqtt.client as mqtt
import time
from json_parser import read_JSON

CLIENT_ID   = 'paho_client_01'
BROKER_IP   = '192.168.1.1'
JSON_FILE   = './mqtt_msg.json'
PUB_FREQ    = 5 #sec
PUB_TOPIC   ='aprotech/test'

u_data = {}

def client_init(client_id):
    client = mqtt.Client(client_id, clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport='tcp')
    u_data['id'] = client_id
    client.user_data_set(u_data)
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    return client

def on_connect(client, userdata, flags, rc):
    print(f"client <{userdata['id']}>: Connection result is {('OK', 'NOT OK')[bool(rc)]}")

def on_publish(client, userdata, mid):
    print(f"client <{userdata['id']}>: Publishing message id={mid} -> Message payload:\n{u_data['pub_msg']}")

def on_message(client, userdata, message):
    print(f"client <{userdata['id']}>: Recieved message with topic={message.topic}, " +
            f"payload={message.payload}, qos={message.qos}, retain={message.retain}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"client <{userdata['id']}>: Subscribing request id={mid}, qos={', '.join(str(i) for i in granted_qos)}")

def on_disconnect(client, userdata, rc):
    print(f'MQTT client is disconnected')


def pub_JSON(client):
    pub_msg = read_JSON(JSON_FILE)
    u_data['pub_msg'] = pub_msg
    time.sleep(PUB_FREQ)
    client.user_data_set(u_data)
    client.publish(PUB_TOPIC, pub_msg, qos=0)
    

if __name__ == "__main__":
    try:
        client = client_init(CLIENT_ID)
        client.connect(BROKER_IP, port=1883)
        client.subscribe('notmytopics/#', qos=0)
        client.loop_start()
        while True:
            pub_JSON(client)
    except TimeoutError:
        print("\nERR: Connection timeout")
    except KeyboardInterrupt:
        client.disconnect()
        print("\nERR: Script was terminated by user")
    except OSError:
        print("\nERR: Network problem, probably")