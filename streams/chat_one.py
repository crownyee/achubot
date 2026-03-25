#Discord
import discord
from discord import app_commands
from core.__init__ import Cog_Extension

#Tools
import json, datetime, pytz
import asyncio,pytchat,logging
from emoji import emojize
from collections import deque
from holodex.client import HolodexClient

#Json
from core import __json__
jdata = __json__.get_setting_data()
logging.basicConfig(filename='./json/error_log.txt', level=logging.ERROR)

#Setting
CHANNELSUBS = jdata['Chat_Channel']
TESTSUBS = jdata['Test_Channel']
streamer = jdata['FWMC']

#member sticker
text = {
    ":_FUWAheart:": "<:01_meba_FuwaHeart:1165451742813630544>",
    ":_MOCOheart:": "<:01_meba_MocoHeart:1165451682512113704>",
    ":_FUWApat:": "<:02_meba_Fuwapat:1165451854113689620>",
    ":_MOCOpat:": "<:02_meba_Mocopat:1165451790997794886>",
    ":_FUWAlight:": "<:03_meba_Fuwalight:1165451537397579806>",
    ":_MOCOlight:": "<:03_meba_Mocolight:1165451620721631353>",
    ":_FUWAwww:": "<:04_meba_FUWAwww:1252081921782190201>",
    ":_MOCOwww:": "<:04_meba_MOCOwww:1252082026379608164>",
    ":_FUWApien:": "<:05_meba_FUWApien:1252081750117711872>",
    ":_MOCOpien:": "<:05_meba_MOCOpien:1252081638566002708>",
    ":_FUWAhm:": "<:06_meba_FuwaAhm:1165451900989222912>",
    ":_BAU:": "<:0_meba_BAU:1145138276517294211>",
    ":_FUWAawa:": "<:0_meba_FuwaAwa:1145138273178628106>",
    ":_FUWAMOCO:": "<:0_meba_FuwaMoco:1145138289209258114>",
    ":_FUWAyes:": "<:0_meba_FuwaYes:1145138294133375129>",
    ":_MOCOCOHOEH:": "<:0_meba_MOCOCOHOEH:1252081797337190421>",
    ":_MOCOsweat:": "<:0_meba_MOCOsweat:1252081854060822590>",
    ":_MOGOJYAN:": "<:0_meba_MOGOJYAN:1252081954782707845>",
    ":_MOCOhuh:": "<:0_meba_MocoHuh:1145138281755971715>",
    ":_MOCOniya:": "<:0_meba_MocoNiya:1145138267197554808>",
    ":_MOCOsneeze:": "<:0_meba_Mocosneeze:1165451418635882606>",
    ":_KUSA:": "<:0_meba_kusa:1252081775954366504>",
    ":_mochidonut:": "<:0_meba_mochidonut:1165451286318166096>",
    ":_emojiF:": "<:0_meba_w0_F_:1252081899090743316>",
    ":_emojiW:": "<:0_meba_w1_W_:1252082337446105108>",
    ":_emojiM:": "<:0_meba_w3_M_:1252081878899359765>",
    ":_emojiC:": "<:0_meba_w4_C_:1252081710493995119>",
    ":_MOCOthumb:": "<:0_meba_MOCOthumb:1252081997775365243>"
}


#Class

class FW_Chat(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.msg_queue = asyncio.Queue()
        self.live_streams = []
        self.processed_streams = set()
        async def holo_chat():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                self.channel = self.bot.get_channel(int(CHANNELSUBS))  
                self.channel_2 = self.bot.get_channel(int(TESTSUBS))  
                try:
                    fwmc_live = await self.holodex_client.live_streams(channel_id=streamer)
                    # 如果fwmc_live為None或是空的，則無直播信息
                    if not fwmc_live or not fwmc_live.contents:
                        raise ValueError("No live data available.")

                    for live in fwmc_live.contents:
                            live_stream_info = [live.status, live.id, live.start_scheduled]
                            self.live_streams.append(live_stream_info)

                except Exception as e:
                    # 處理無直播信息的情況
                    self.live_streams.append(['upcoming','gxZYeXU5Dek','2029-01-31T16:00:00.000Z'])

                for stream_info in self.live_streams:
                    #Time轉換
                    utc_time = datetime.datetime.fromisoformat(stream_info[2].replace("Z", "+00:00"))
                    cst_timezone = pytz.timezone('Asia/Shanghai')
                    cst_time = utc_time.astimezone(cst_timezone).replace(second=0, microsecond=0)
                    current_time = datetime.datetime.now().astimezone(cst_timezone).replace(second=0, microsecond=0)
                    notification_time = cst_time - datetime.timedelta(minutes=10)
                    
                    if (stream_info[0] == 'live' or current_time >= notification_time) and (stream_info[1] not in self.processed_streams):
                        self.processed_streams.add(stream_info[1])
                        await self.channel_2.send(f"<:0_meba_BAU:1145138276517294211>開 [直播](<https://www.youtube.com/watch?v={stream_info[1]}>)")  
                        self.live_msgs = [asyncio.create_task(self.process_msgs()) for _ in range(1)]
                        self.monitor = asyncio.create_task(self.start_monitor(video_id=stream_info[1]))  
                    
                await asyncio.sleep(300)

        self.bg_chat = asyncio.create_task(holo_chat())

    @app_commands.command(name='start_monitor_command', description="抓取直播")
    async def start_monitor_command(self, ita: discord.Interaction, video_id: str):
        self.live_msgs = [asyncio.create_task(self.process_msgs()) for _ in range(1)]
        self.live_monitor_task = asyncio.create_task(self.start_monitor(video_id=video_id))
        await ita.response.send_message(f"開始抓取 [直播](<https://www.youtube.com/watch?v={video_id}>)")

    async def start_monitor(self, video_id):
        chat = pytchat.create(video_id=video_id)
        try:
            while chat.is_alive():
                for c in chat.get().sync_items():  
                    await self.msg_queue.put(c)
                await asyncio.sleep(1)  # 避免 "out of queue" 錯誤
        except Exception as e:
            logging.error(f"chat_one.py pytchat: {e}")

        finally:
            chat.terminate()
            for live_msg in self.live_msgs:
                live_msg.cancel()
            # asyncio.gather 等待所有消息處理任務完成或取消
            await asyncio.gather(*self.live_msgs, return_exceptions=True)
            self.processed_streams.remove(video_id)
            self.live_streams.clear()
            await self.channel_2.send(f"<:0_meba_BAU:1145138276517294211>斷 [直播](<https://www.youtube.com/watch?v={video_id}>)")  


    async def process_msgs(self):
        while True:
            if self.msg_queue: # 如果隊列裡有消息
                c = await self.msg_queue.get()
                if c.author.channelId == streamer:
                    try:
                        msg = c.message
                        # 取代所有會員表情關鍵字
                        for k, v in text.items():
                            msg = msg.replace(k, v)
                        await self.channel.send(f"{emojize(msg)}") 
                    except Exception as e:
                        logging.error(f"chat_one.py process_msgs: {e}")
            else:
                await asyncio.sleep(1)

async def setup(bot):
    await bot.add_cog(FW_Chat(bot))