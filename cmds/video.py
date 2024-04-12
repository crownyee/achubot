import json
import discord,datetime
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
from core.__whitelist__ import mywhite
import logging

logging.basicConfig(filename='./json/log.txt', level=logging.ERROR)
with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

import googleapiclient.discovery
import googleapiclient.errors


class fmvideo(Cog_Extension):
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    @app_commands.command(name='fwmc_info', description="雙子資訊")
    async def fwmc_info(self,ita: discord.Interaction):
        await ita.response.defer()
        embed = discord.Embed(title="FUWAMOCO個人介紹",
                            url="https://www.youtube.com/@FUWAMOCOch",
                            description="關於:\n「魔界看門犬」姊妹中負責掌管一切的角色，因為一次非比尋常的惡作劇惹怒眾神而被關進大監獄「The Cell」中。\n\nFUWAWA介紹:\n她可以冷靜的照顧自己的雙胞胎妹妹「Mococo」和寵物「Pero」。\n但相對地在世人眼中，她也是一個愛說話愛玩，容易引起騷動的人。\n「把你們都弄得毛茸茸的怎麼樣～？」\n\nMOCOCO介紹:\n本來就喜歡玩耍的她，在獄中也是過著玩遊戲看動畫的日子，還時常把姊姊「Fuwawa」和「Pero」牽扯進來。\n有傳言說她參與逃獄只是覺得好玩。\n「遊戲時間到啦！大家都準備好了吧！」",
                            colour=0x1c7497)

        embed.set_author(name="FUWAMOCO",
                        url="https://www.youtube.com/@FUWAMOCOch",
                        icon_url="https://pbs.twimg.com/profile_images/1684033348086419459/NEAktg4s_400x400.jpg")

        embed.add_field(name="Youtube",
                        value="https://www.youtube.com/@FUWAMOCOch",
                        inline=False)
        embed.add_field(name="Twitter",
                        value="https://twitter.com/fuwamoco_en",
                        inline=False)
        embed.add_field(name="繪師媽媽",
                        value="https://twitter.com/rswxx",
                        inline=True)
        embed.add_field(name="模組爸爸",
                        value="https://twitter.com/MegaJujube",
                        inline=True)

        embed.set_image(url="https://pbs.twimg.com/profile_banners/1656889310472437761/1690345515/1500x500")

        embed.set_thumbnail(url="https://pbs.twimg.com/profile_images/1684033348086419459/NEAktg4s_400x400.jpg")

        embed.set_footer(text="FUWAMOCO資訊列",
                        icon_url="https://pbs.twimg.com/profile_images/1684033348086419459/NEAktg4s_400x400.jpg")

        await ita.edit_original_response(embed=embed)


    @app_commands.command(name="fwmc_mv", description='雙子單曲和COVER')
    async def fwmc_mv(self,ita: discord.Interaction):
        await ita.response.defer()
        # 建立YouTube API客戶端
        youtube = googleapiclient.discovery.build("youtube", "v3", developerKey=jdata['YOUTUBE_API_KEY'])
        
        embed = discord.Embed(title="FUWAMOCO mv cover 統計",
                              colour=0x00b0f4)
        embed.set_author(name="FUWAMOCO Ch. hololive-EN",
                         url="https://www.youtube.com/@FUWAMOCOch",
                         icon_url="https://yt3.googleusercontent.com/zt63obGOD6fnCX0elnzt8xkylqOTnAENmSCKmwg_PSiC857DDgB28kEjQ-FJlWGtNYZ9lqzEag=s176-c-k-c0x00ffffff-no-rj")
        #讀取
        try:
            with open('./json/description.json','r',encoding='utf8') as dfile:
                video_list = json.load(dfile)
        except FileNotFoundError:
            video_list = []

        for video in video_list:
            video_id = video['video_id']
            video_name = video['video_name']
            
            try:
                # 執行Videos: list請求，並指定要檢索的影片ID和要返回的資訊
                request = youtube.videos().list(
                    part="statistics",
                    id=video_id
                )
                response = request.execute()
                # 從回應中提取觀看次數
                view_count = response["items"][0]["statistics"]["viewCount"]
                
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                field_value = f"{video_url}\n總觀看次數: {int(view_count):,.0f} views."
                embed.add_field(name=video_name, value=field_value, inline=False)
                
            except googleapiclient.errors.HttpError as e:
                await ita.response.send_message("發生HTTP錯誤", e)
                logging.error(f"video.py  fwmc_mv: {e}")
        
        await ita.edit_original_response(embed=embed)

    @app_commands.command(name="fwmc_add", description='新增影片和標題')
    @app_commands.check(mywhite.iswhitelist)
    async def fwmc_add(self, ita: discord.Interaction, video_id: str, video_name: str):
        await ita.response.defer()
        #讀取
        try:
            with open('./json/description.json','r',encoding='utf8') as dfile:
                video_list = json.load(dfile)
        except Exception as e:
            video_list = []
            logging.error(f"video.py  fwmc_add: {e}")
        #新增
        new_video_entry = {
            "video_id": video_id,
            "video_name": video_name
        }
        video_list.append(new_video_entry)

        #寫回
        with open('./json/description.json','w',encoding='utf8') as dfile:
            json.dump(video_list, dfile, indent=4, ensure_ascii=False)

        #傳送
        await ita.edit_original_response(content=f"https://www.youtube.com/watch?v={video_id}")

async def setup(bot):
    await bot.add_cog(fmvideo(bot))