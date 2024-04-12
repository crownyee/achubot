import discord
from discord import app_commands
from core.__init__ import Cog_Extension
import json,asyncio, logging
from holodex.client import HolodexClient
from googleapiclient.discovery import build
with open('./json/setting.json','r',encoding='utf8') as jfile:
 	jdata = json.load(jfile)

CHANNELSUBS = jdata['SUBs_Channel']
TESTSUBS = jdata['Test_Channel']
last_count = float(jdata['SUBCOUNT'])
fwmc = jdata['FWMC']
logging.basicConfig(filename='./json/log.txt', level=logging.ERROR)
class HoloCog(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def holo_SUB():
            await self.bot.wait_until_ready()
            
            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))
                self.channel_2 = self.bot.get_channel(int(TESTSUBS))
                #search = await self.holodex_client_2.autocomplete("fuwamoco")
                #channel_id = search.contents[0].value
                channelD = await self.holodex_client.channel(fwmc)
                subs_count = int(channelD.subscriber_count) / 10000
                global last_count
                
                if subs_count - last_count > 0:
                    try:
                        print(subs_count)
                        display_count = format(subs_count, ".1f")
                        await self.channel_2.send(f"FUWAMOCO更新訂閱:{display_count}萬")
                        numbers = str(display_count).split('.')
                        d = "․"
                        await self.channel.edit(name=f"fwmc-{numbers[0] + d + numbers[1]}萬")
                        last_count = subs_count
                        jdata['SUBCOUNT'] = subs_count  # 在 jdata 中更新最後訂閱數
                        with open('./json/setting.json', 'w', encoding='utf8') as jfile:
                            json.dump(jdata, jfile, indent=4, ensure_ascii=False)  # 將更新後的數據寫入設定檔案
                        await asyncio.sleep(5)
                        
                    except Exception as e:
                        logging.error(f"holocount.py  holo_SUB: {e}")  

                await asyncio.sleep(270)

        self.bg_subs = asyncio.create_task(holo_SUB())

        
    @app_commands.command(name='update_sub',description="更新訂閱")
    async def update_sub(self,ita:discord.Interaction):
        try:
            global last_count

            youtube = build('youtube', 'v3', developerKey=jdata['YOUTUBE_API_KEY'])
            request = youtube.channels().list(part='statistics', id=fwmc)
            response = request.execute()
            subs_count = response['items'][0]['statistics']['subscriberCount']
            subs_count = int(subs_count) / 10000
            last_count = subs_count
            display_count = format(subs_count, ".1f")
            await ita.response.send_message(f"FUWAMOCO更新訂閱:{display_count}萬")
            numbers = str(display_count).split('.')
            d = "․"
            await self.channel.edit(name=f"fwmc-{numbers[0] + d + numbers[1]}萬")
            # 更新頻道名稱、發送訊息後
            jdata['SUBCOUNT'] = subs_count  # 在 jdata 中更新最後訂閱數
            with open('./json/setting.json', 'w', encoding='utf8') as jfile:
                json.dump(jdata, jfile, indent=4, ensure_ascii=False)  # 將更新後的數據寫入設定檔案
        except Exception as e:
            logging.error(f"holocount.py  update_sub: {e}")  
        
    def cog_unload(self):
        self.holodex_client.close()
        

async def setup(bot):
    await bot.add_cog(HoloCog(bot))



"""
    @app_commands.command(name='update_sub',description="更新訂閱")
    async def update_sub(self,ita:discord.Interaction):
        try:
            global last_count
            
            channel = await self.holodex_client.channel(channel_id=fwmc)
            subs_count = int(channel.subscribere_count) / 10000
            last_count = subs_count
            display_count = format(subs_count, ".1f")
            await self.channel_2.send(f"FUWAMOCO更新訂閱:{display_count}萬")
            numbers = str(display_count).split('.')
            d = "․"
            await self.channel.edit(name=f"fwmc-{numbers[0] + d + numbers[1]}萬")
            # 更新頻道名稱、發送訊息後
            jdata['SUBCOUNT'] = subs_count  # 在 jdata 中更新最後訂閱數
            with open('./json/setting.json', 'w', encoding='utf8') as jfile:
                json.dump(jdata, jfile, indent=4, ensure_ascii=False)  # 將更新後的數據寫入設定檔案
        except Exception as e:
            logging.error(f"holocount.py  update_sub: {e}")

"""