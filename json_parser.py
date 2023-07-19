import json
import random
import datetime

def p_JSON():
    with open('./mqtt_msg.json') as f:
        params = json.load(f)
        for param in params:
            print(param)

if __name__ == '__main__':
    p_JSON()