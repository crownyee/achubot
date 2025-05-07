import discord
from discord import app_commands
from core.__init__ import Cog_Extension
import logging,asyncio,json

logging.basicConfig(filename='./json/error_log.txt', level=logging.ERROR)

'''
"url_1": "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Taipei/262?&$select=PlateNumb,RouteName,StopName&%24format=JSON",
"url_2": "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Taichung/306?&$select=PlateNumb,RouteName,StopName&%24format=JSON",
"url_3": "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Kaohsiung/紅33?&$select=PlateNumb,RouteName,StopName&%24format=JSON"
'''

'''
"url_1": "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Taipei?$filter=PlateNumb%20eq%20%27FAA-065%27&$format=JSON",
"url_2": "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Taichung?$filter=PlateNumb%20eq%20%27783-U8%27&$format=JSON",
"url_3": "https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Kaohsiung?$filter=PlateNumb%20eq%20%27KKA-9137%27&$format=JSON"

'''



class bus_track(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def bus_ttt():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                try:
                    self.channel_1 = await self.bot.fetch_channel(int(1267784724542394418))
                    self.channel_2 = await self.bot.fetch_channel(int(1267785097549971476))
                    self.channel_3 = await self.bot.fetch_channel(int(1267785124582526986))

                    with open("./json/busdata.json", 'r', encoding='utf-8') as f:
                        bus_data = json.load(f)

                    stop_names = {}
                    route_names = {}
                    for bus in bus_data:
                        if bus['PlateNumb'] == 'FAA-065':
                            route_names['FAA-065'] = bus['RouteName']['Zh_tw']
                            stop_names['FAA-065'] = bus['StopName']['Zh_tw']
                        elif bus['PlateNumb'] == '783-U8':
                            route_names['783-U8'] = bus['RouteName']['Zh_tw']
                            stop_names['783-U8'] = bus['StopName']['Zh_tw']
                        elif bus['PlateNumb'] == 'KKA-9137':
                            route_names['KKA-9137'] = bus['RouteName']['Zh_tw']
                            stop_names['KKA-9137'] = bus['StopName']['Zh_tw']

                    if 'FAA-065' in stop_names:
                        await self.channel_1.edit(name=f"台北{route_names['FAA-065']}-{stop_names['FAA-065']}")
                    else:
                        await self.channel_1.edit(name="台北-FAA-065")

                    if '783-U8' in stop_names:
                        await self.channel_2.edit(name=f"台中{route_names['783-U8']}-{stop_names['783-U8']}")
                    else:
                        await self.channel_2.edit(name="台中-783-U8")

                    if 'KKA-9137' in stop_names:
                        await self.channel_3.edit(name=f"高雄{route_names['KKA-9137']}-{stop_names['KKA-9137']}")
                    else:
                        await self.channel_3.edit(name="高雄-KKA-9137")

                except Exception as e:
                    logging.error(f"bus.py bus: {e}")

                await asyncio.sleep(220)

        self.bg_bus = asyncio.create_task(bus_ttt())

    @app_commands.command(name="change_route",description="台北/台中/台南 跟 路線")
    async def change_route(self, ita:discord.Interaction,city: str, route: str):
        try:
            with open('./json/setting.json','r',encoding='utf8') as jfile:
                url_update = json.load(jfile)
            
            if city == '台北':
                url_key = 'url_1'
                url_up = f'https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Taipei/{route}?&$select=PlateNumb,RouteName,StopName&%24format=JSON'
            elif city == '台中':
                url_key = 'url_2'
                url_up = f'https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Taichung/{route}?&$select=PlateNumb,RouteName,StopName&%24format=JSON'
            elif city == '高雄':
                url_key = 'url_3'
                url_up = f'https://tdx.transportdata.tw/api/basic/v2/Bus/RealTimeNearStop/City/Kaohsiung/{route}?&$select=PlateNumb,RouteName,StopName&%24format=JSON'

            url_update[url_key] = url_up
            with open('./json/setting.json', 'w',encoding='utf8') as f:
                json.dump(url_update, f, indent=4,ensure_ascii=False)
            
            await ita.response.send_message(content=f'{city}路線更改成{route}')
        except Exception as e:
            await ita.response.send_message(content=f'執行時BOT出現錯誤!')
            logging.error(f"bus_update bus_track.py: {e}")

async def setup(bot):
    await bot.add_cog(bus_track(bot))


'''
        try:
            a = Auth(app_id, app_key)
            auth_response = requests.post(auth_url, a.get_auth_header())
            d = data(app_id, app_key, auth_response)
            data_taipei = requests.get(url_1, headers=d.get_data_header())
            data_j = json.loads(data_taipei.text)
            with open("./json/busdata.json", 'w', encoding='utf-8') as f:
                json.dump(data_j, f,ensure_ascii=False, indent=4)
        except Exception as e:
            logging.error(f"bus.py  taipei_bus: {e}")

if __name__ == '__main__':
    try:
        a = Auth(app_id, app_key)
        auth_response = requests.post(auth_url, a.get_auth_header())
        d = data(app_id, app_key, auth_response)
        data_response = requests.get(url, headers=d.get_data_header())
        data = json.loads(data_response.text)
        with open("json/busdata.json", 'w', encoding='utf-8') as f:
            json.dump(data, f,ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"bus.py  taipei_bus: {e}")
'''