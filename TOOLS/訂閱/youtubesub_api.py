import discord
from discord.ext import tasks, commands
from core.__init__ import Cog_Extension

from googleapiclient.discovery import build
import json, asyncio

with open('./json/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

CHANNEL_ID = jdata['FWMC']
CHANNELSUBS = jdata['SUBs_Channel']
youtube = build('youtube', 'v3', developerKey=jdata['YOUTUBE_API_KEY'])
last_subs = 0

class YTtest(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def subs():
            await self.bot.wait_until_ready()
            
            while not self.bot.is_closed():
                request = youtube.channels().list(part='statistics', id=CHANNEL_ID)
                response = request.execute()
                subs_count = response['items'][0]['statistics']['subscriberCount']
                global last_subs

                if int(subs_count) - int(last_subs) >= 1000:
                    self.channel = self.bot.get_channel(int(CHANNELSUBS))
                    if self.channel:
                        s = str(int(subs_count)/10000)
                        d = "․"
                        await self.channel.send(f"更新{s[:2] + s[2:]}萬")
                        await self.channel.edit(name=f"fwmc-{s[:2] + d + s[2:]}萬")

                last_subs = int(subs_count)
                await asyncio.sleep(300)

        self.sub_back = asyncio.create_task(subs())

async def setup(bot):
    await bot.add_cog(YTtest(bot))