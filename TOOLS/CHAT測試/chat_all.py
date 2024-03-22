import discord
from discord.ext import commands, tasks
from core.__init__ import Cog_Extension
import json,asyncio,pytchat
from collections import deque
from holodex.client import HolodexClient
from emoji import emojize

with open('./json/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

CHANNELSUBS = jdata['SUBs_Channel']
streamer = 'UCZLZ8Jjx_RN2CXloOmgTHVg'
msg_queue = deque(maxlen=900000)

class FW_Chat(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_streaming = False
        self.other_monitor_tasks = []

        async def holo_chat():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))
                arr = []

                fwmc_live = await self.holodex_client.live_streams(channel_id=streamer)
                fwmc_status = fwmc_live.contents[0].status
                fwmc_id = fwmc_live.contents[0].id
                holo_channel = await self.holodex_client_2.live_streams(org='Hololive', lang='all', status='live')

                asyncio.create_task(self.process_msgs())
                if fwmc_status == 'live' and not self.is_streaming:
                    await self.stop_other_monitors()  # 停止其他抓取直播的任務
                    await asyncio.sleep(0.5)
                    self.current_monitor_task = asyncio.create_task(self.start_monitor(video_id=fwmc_id))
                    self.is_streaming = True  # 改變狀態

                for index in range(len(holo_channel.contents)):
                    if holo_channel.contents[index].channel.org == 'Hololive':
                        arr.append(holo_channel.contents[index].id)
                        await asyncio.sleep(0.5)

                for stream_id in arr:
                    await self.channel.send(f"抓取其他[直播](<https://www.youtube.com/watch?v={stream_id}>)")
                    task = asyncio.create_task(self.start_monitor(video_id=stream_id))
                    self.other_monitor_tasks.append(task)
                    await asyncio.sleep(1)

                await asyncio.sleep(180)

        asyncio.create_task(holo_chat())

    async def start_monitor(self, video_id):
        chat = pytchat.create(video_id=video_id)
        while chat.is_alive():
            for c in chat.get().sync_items():
                msg_queue.append(c)  # 列隊
            await asyncio.sleep(5)  # 避免"out of quota"錯誤

        chat.terminate()
        self.is_streaming = False
        await self.channel.send(f"停止直播...")

    async def stop_other_monitors(self):
        for task in self.other_monitor_tasks:
            task.cancel()
            await self.channel.send(f"[直播](<https://www.youtube.com/watch?v={task}>)")
        await asyncio.gather(*self.other_monitor_tasks, return_exceptions=True)
        self.other_monitor_tasks = []

    async def process_msgs(self):
        while True:
            if msg_queue: # 如果隊列裡有消息
                c = msg_queue.popleft() # 從隊列頭取出消息
                #UCueVmJBtrjJp29cdqVU2cCg
                #if c.author.isChatOwner or c.author.isChatModerator:
                if c.author.channelId == 'UCZLZ8Jjx_RN2CXloOmgTHVg':
                    try:
                        await self.channel.send(f"**{c.author.name}**: {emojize(c.message)}")
                    except Exception as err:
                        print(f"Error occurred: {err}")
            else:
                await asyncio.sleep(1)

    async def monitor_and_process_msgs(self, video_id):
        chat = pytchat.create(video_id=video_id)
        while True:
            for c in chat.get().sync_items():
                msg_queue.append(c)
                if msg_queue: # 如果隊列裡有訊息
                    c = msg_queue.popleft() # 從隊列頭取出消息
                    if c.author.channelId == streamer:
                        await self.channel.send(f"**{c.author.name}** in [直播](<https://www.youtube.com/watch?v={video_id}>) : {emojize(c.message)}")
                else:
                    await asyncio.sleep(1)

            await asyncio.sleep(5) 


    def cog_unload(self):
        self.holodex_client.close()

async def setup(bot):
    await bot.add_cog(FW_Chat(bot))
    


'''
import discord
from discord.ext import commands, tasks
from core.__init__ import Cog_Extension
import json,asyncio,pytchat
from collections import deque
from holodex.client import HolodexClient
from emoji import emojize

with open('./json/setting.json', 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

CHANNELSUBS = jdata['FUWC_Channel']
streamer = 'UCt9H_RpQzhxzlyBxFqrdHqA'
msg_queue = deque(maxlen=900000)

class FW_Chat(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.handled_streams = set()

        async def holo_chat():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))
                arr = []
                
                holo_channel = await self.holodex_client_2.live_streams(org='Hololive',lang='all',status='live')
                for index in range(len(holo_channel.contents)):
                    if holo_channel.contents[index].channel.org == 'Hololive':
                        arr.append(holo_channel.contents[index].id)
                        await asyncio.sleep(0.5)

                for stream_id in arr:
                    if stream_id not in self.handled_streams:  # 如果直播ID还没有处理过
                        #await self.channel.send(f"開始抓取直播...")
                        asyncio.create_task(self.monitor_and_process_msgs(video_id=stream_id))
                        self.handled_streams.add(stream_id)  # 添加直播ID到已处理集合中
                        await asyncio.sleep(1)


                await asyncio.sleep(180)

        asyncio.create_task(holo_chat())


    async def monitor_and_process_msgs(self, video_id):
        chat = pytchat.create(video_id=video_id)
        while chat.is_alive():
            for c in chat.get().sync_items():
                msg_queue.append(c)
                if msg_queue: # 如果隊列裡有訊息
                    c = msg_queue.popleft() # 從隊列頭取出消息

                    if c.author.channelId == streamer:
                        try:
                            await self.channel.send(f"**{c.author.name}** in [直播](<https://www.youtube.com/watch?v={video_id}>) : {emojize(c.message)}")
                        except Exception as err:
                            print(f"Error occurred: {err}")

            await asyncio.sleep(5) 

        chat.terminate()
        #await self.channel.send(f"停止直播...")
        self.handled_streams.remove(video_id)



    def cog_unload(self):
        self.holodex_client.close()

async def setup(bot):
    await bot.add_cog(FW_Chat(bot))

'''