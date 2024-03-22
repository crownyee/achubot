import discord
from discord.ext import commands
from core.__init__ import Cog_Extension
import json,asyncio
from holodex.client import HolodexClient

with open('./json/setting.json','r',encoding='utf8') as jfile:
 	jdata = json.load(jfile)

CHANNELSUBS = jdata['SUBs_Channel']
TESTSUBS = jdata['Test_Channel']
last_count = float(jdata['SUBCOUNT'])

class HoloCog(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def holo_SUB():
            await self.bot.wait_until_ready()
            
            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))
                self.channel_2 = self.bot.get_channel(int(TESTSUBS))
                search = await self.holodex_client_2.autocomplete("fuwamoco")
                channel_id = search.contents[0].value
                channelD = await self.holodex_client.channel(channel_id)
                subs_count = int(channelD.subscriber_count) / 10000
                global last_count
                
                if subs_count - last_count > 0:
                    display_count = format(subs_count, ".1f")
                    await self.channel_2.send(f"FUWAMOCO更新訂閱:{display_count}萬")
                    numbers = str(display_count).split('.')
                    d = "․"
                    await self.channel.edit(name=f"fwmc-{numbers[0] + d + numbers[1]}萬")
                    last_count = subs_count
                    # 更新頻道名稱、發送訊息後
                    jdata['SUBCOUNT'] = subs_count  # 在 jdata 中更新最後訂閱數
                    with open('./json/setting.json', 'w', encoding='utf8') as jfile:
                        json.dump(jdata, jfile, indent=4, ensure_ascii=False)  # 將更新後的數據寫入設定檔案

                    await asyncio.sleep(5)
                    #embed = discord.Embed(title="Holodex Channel Info", color=discord.Color.blue())
                    #embed.add_field(name="Name", value=channel.name)
                    #embed.add_field(name="Subscriber Count", value=channel.subscriber_count)

                    #await ctx.send(embed=embed)

                #last_count = subs_count
                #await self.channel.send(subs_count)

                await asyncio.sleep(270)

        self.bg_subs = asyncio.create_task(holo_SUB())

    def cog_unload(self):
        self.holodex_client.close()
        

async def setup(bot):
    await bot.add_cog(HoloCog(bot))
