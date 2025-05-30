import requests,asyncio
import json,logging
from core.__init__ import Cog_Extension

logging.basicConfig(filename='./json/error_log.txt', level=logging.ERROR)

app_id = ''
app_key = ''
auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.app_id,
            'client_secret' : self.app_key
        }

class data():

    def __init__(self, app_id, app_key, auth_response):
        self.app_id = app_id
        self.app_key = app_key
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }

async def run_data_fetch():
    while True:
        try:
            with open('./json/setting.json','r',encoding='utf8') as jfile:
                jdata = json.load(jfile)

            urls = [jdata['url_1'], jdata['url_2'], jdata['url_3']]
            a = Auth(app_id, app_key)
            auth_response =  requests.post(auth_url, a.get_auth_header())
            d = data(app_id, app_key, auth_response)
            all_data = []
            for url in urls:
                response =  requests.get(url, headers=d.get_data_header())
                data_json = json.loads(response.text)
                all_data.extend(data_json)
        except Exception as e:
            logging.error(f"bus_d.py bus: {e}")
        
        with open("./json/busdata.json", 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=4)

        await asyncio.sleep(215)

