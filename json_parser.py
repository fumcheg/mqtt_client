import json
import random
import datetime

def read_JSON(fname):
    with open(fname) as f:
        msg = {}
        params = json.load(f)
        for param in params:
            match param['type']:
                case "timestamp":
                    msg[param['parameter']] = str(datetime.datetime.now())
                case "float":
                    if param['value'] is None:
                        msg[param['parameter']] = round(gen_value(param['min'], param['max']), param['decimal'])
                    else:
                        msg[param['parameter']] = param['value']
    return json.dumps(msg)

def gen_value(minv, maxv):
    return random.random() * (maxv - minv) + minv


# def get_JSONMessage():
#     return  json.dumps({'temperature':round(gen_value(10,20), 2),
#                         'humidity':round(gen_value(28,30), 2),
#                         'timestamp':str(datetime.datetime.now()),
#                         'wind':round(gen_value(2,5), 2),
#                         'rain':0,
#                         'pressure':round(gen_value(1005,1007), 2),
#                         'posLat':round(gen_value(25.041, 25.044), 4),
#                         'posLon':round(gen_value(55.217, 55.220), 4)}, indent=4)

# def gen_value(minv, maxv):
#     return random.random() * (maxv - minv) + minv