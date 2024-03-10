import discord
from discord.ext import commands, tasks
from core.__init__ import Cog_Extension
import json, datetime, pytz
import asyncio
import pytchat
from collections import deque
from holodex.client import HolodexClient
from emoji import emojize

with open('./json/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

CHANNELSUBS = jdata['SUBs_Channel']
TESTSUBS = jdata['Test_Channel']
msg_queue = deque(maxlen=60000)
streamer = 'UCt9H_RpQzhxzlyBxFqrdHqA'

class FW_Chat(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_streaming = False  # 新增狀態檢查變數

        async def holo_chat():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))
                self.channel_2 = self.bot.get_channel(int(TESTSUBS))
                fwmc_live = await self.holodex_client.live_streams(channel_id=streamer)
                fwmc_status = fwmc_live.contents[0].status
                fwmc_id = fwmc_live.contents[0].id
                live_time = fwmc_live.contents[0].start_scheduled

                utc_time = datetime.datetime.fromisoformat(live_time.replace("Z", "+00:00"))
                cst_timezone = pytz.timezone('Asia/Shanghai')
                cst_time = utc_time.astimezone(cst_timezone).replace(second=0, microsecond=0)
                current_time = datetime.datetime.now().astimezone(cst_timezone).replace(second=0, microsecond=0)
                notification_time = cst_time - datetime.timedelta(minutes=15)

                asyncio.create_task(self.process_msgs())
                if (fwmc_status == 'live'  or current_time >= notification_time) and not self.is_streaming:
                    await self.channel_2.send(f"開始抓取直播...")
                    asyncio.create_task(self.start_monitor(video_id=fwmc_id))
                    self.is_streaming = True  # 改變狀態

                await asyncio.sleep(300)

        asyncio.create_task(holo_chat())

    async def start_monitor(self, video_id):
        chat = pytchat.create(video_id=video_id)
        while chat.is_alive():
            for c in chat.get().sync_items():
                msg_queue.append(c)  # 当streamer发送消息时，将消息放入队列
            await asyncio.sleep(5)  # 这里添加稍许的稍息，以避免"out of quota"错误

        chat.terminate()
        self.is_streaming = False
        await self.channel.send(f"<:0_meba_BAU:1145138276517294211> <:0_meba_BAU:1145138276517294211>")
        #await self.channel_2.send(f"停止直播...")

    async def process_msgs(self):
        while True:
            if msg_queue: # 如果隊列裡有消息
                c = msg_queue.popleft() # 從隊列頭取出消息
                #UCueVmJBtrjJp29cdqVU2cCg
                if c.author.channelId == 'UCt9H_RpQzhxzlyBxFqrdHqA':
                #if c.author.isChatOwner or c.author.isChatModerator:
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