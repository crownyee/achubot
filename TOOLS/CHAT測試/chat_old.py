import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import json, datetime, pytz
import asyncio
import pytchat
from collections import deque
from holodex.client import HolodexClient
from emoji import emojize

#Json
with open('./json/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

#Setting
CHANNELSUBS = jdata['Chat_Channel']
TESTSUBS = jdata['Test_Channel']
#'UCt9H_RpQzhxzlyBxFqrdHqA'
streamer = 'UCt9H_RpQzhxzlyBxFqrdHqA'

#Class
class FW_Chat(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_streaming = False  #Status
        self.msg_queue = asyncio.Queue(maxsize=90000)
        async def holo_chat():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))
                self.channel_2 = self.bot.get_channel(int(TESTSUBS))
                try:
                    fwmc_live = await self.holodex_client.live_streams(channel_id=streamer)
                    if fwmc_live:
                        fwmc_status = fwmc_live.contents[0].status  
                        fwmc_id = fwmc_live.contents[0].id
                        live_time = fwmc_live.contents[0].start_scheduled                    
                except IndexError:
                    fwmc_status = 'upcoming'
                    fwmc_id = 'gxZYeXU5Dek'
                    live_time = '2025-01-31T16:00:00.000Z'

                #Time轉換
                utc_time = datetime.datetime.fromisoformat(live_time.replace("Z", "+00:00"))
                cst_timezone = pytz.timezone('Asia/Shanghai')
                cst_time = utc_time.astimezone(cst_timezone).replace(second=0, microsecond=0)
                current_time = datetime.datetime.now().astimezone(cst_timezone).replace(second=0, microsecond=0)
                notification_time = cst_time - datetime.timedelta(minutes=15)

                if (fwmc_status == 'live'  or current_time >= notification_time) and not self.is_streaming:
                    await self.channel_2.send(f"開始抓取直播...")
                    self.live_msgs = [asyncio.create_task(self.process_msgs()) for _ in range(8)]
                    self.monitor = asyncio.create_task(self.start_monitor(video_id=fwmc_id))
                    self.is_streaming = True  # 改變狀態
                    
                await asyncio.sleep(300)

        self.bg_chat = asyncio.create_task(holo_chat())
        
    @app_commands.command(name='start_monitor_command', description="抓取直播")
    async def start_monitor_command(self, ita: discord.Interaction, video_id: str):
        self.live_msgs = [asyncio.create_task(self.process_msgs()) for _ in range(8)]
        self.live_monitor_task = asyncio.create_task(self.start_monitor(video_id=video_id))
        await ita.response.send_message(f"開始抓取 [直播](<https://www.youtube.com/watch?v={video_id}>)")
    async def start_monitor(self, video_id):
        chat = pytchat.create(video_id=video_id)
        while chat.is_alive():
            for c in chat.get().sync_items():
                await self.msg_queue.put(c)
            await asyncio.sleep(3)  #避免"out of quota"錯誤

        chat.terminate()
        self.is_streaming = False
        for live_msg in self.live_msgs:
            live_msg.cancel()
            
        await self.channel.send(f"<:0_meba_BAU:1145138276517294211> <:0_meba_BAU:1145138276517294211>")
    async def process_msgs(self):
        while True:
            if self.msg_queue: # 如果隊列裡有消息
                c = await self.msg_queue.get()
                #c = msg_queue.popleft() # 從隊列頭取出消息
                #UCueVmJBtrjJp29cdqVU2cCg
                #if c.author.isChatOwner or c.author.isChatModerator:
                if c.author.channelId == streamer:
                    try:
                        await self.channel.send(f"**{c.author.name}**: {emojize(c.message)}")
                    except Exception as err:
                        print(f"Error occurred: {err}")
            else:
                await asyncio.sleep(1)

    def cog_unload(self):
        self.holodex_client.close()

async def setup(bot):
    await bot.add_cog(FW_Chat(bot))



'''
    @app_commands.command(name='start_monitor_command', description="抓取直播")
    async def start_monitor_command(self, ita: discord.Interaction, video_id: str):
        self.live_monitor_task = asyncio.create_task(self.start_monitor(video_id=video_id))
        await ita.response.send_message(f"開始抓取 [直播](<https://www.youtube.com/watch?v={video_id}>)")
'''