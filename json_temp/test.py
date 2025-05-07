import json
import sys,os

with open("./json_temp/serverdata.json",'r',encoding="utf8") as f :
    jdata = json.load(f)

for data in jdata:
    if data['server_ID'] == "1":
        print(data['message_log'])