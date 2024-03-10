import discord,logging
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension

import json, random, asyncio
from datetime import datetime, time
import core.__draw__ as draw_data

import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

split_parts = draw_data.rec_emoji.strip("<:>").split(":")
emoji_name = split_parts[0]  # 這裡 '_BAU' 是第二個元素
with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)
uri = jdata['MongoAPI']

luck_data = {
    "staff": "友人A,春先のどか,YAGOO",
    "0th": "ときのそら,ロボ子,星街すいせい,さくらみこ,あずき",
    "JP_1gen": "白上フブキ,アキ・ローゼンター,夏色まつり,赤井はあと,夜空メル",
    "JP_2gen": "湊あくあ,紫咲シオン,百鬼あやめ,癒月ちょこ,大空スバル",
    "JP_Ggen": "大神ミオ,猫又おかゆ,戌神ころね",
    "JP_3gen": "兎田ぺこら,不知火フレア,白銀ノエル,宝鐘マリン,潤羽るしあ",
    "JP_4gen": "天音かな,角巻わため,常闇トワ,姫森ルーナ,桐生ココ",
    "JP_5gen": "雪花ラミィ,桃鈴ねね,獅白ぼたん,尾丸ポルカ,魔乃アロエ",
    "JP_HoloX": "ラプラス・ダークネス,鷹嶺ルイ,博衣こより,沙花叉クロヱ,風真いろは",
    "JP_ReGLOSS": "火威青,音乃瀬奏,一条莉々華,儒烏風亭らでん,轟はじめ",
    "EN_Myth": "Gawr Gura,Watson Amelia,Ninomae Ina'nis,Takanashi Kiara,Mori Calliope",
    "EN_Promise": "Hakos Baelz,Nanashi Mumei,Ouro Kronii,IRyS,Ceres Fauna,Tsukumo Sana",
    "EN_Advent": "Fuwawa Abyssgard,Mococo Abyssgard,Nerissa Ravencroft,Koseki Bijou,Shiori Novella",
    "ID_1gen": "Ayunda Risu,Moona Hoshinova,Airani Iofifteen",
    "ID_2gen": "Kureiji Ollie,Anya Melfissa,Pavolia Reine",
    "ID_3gen": "Vestia Zeta,Kaela Kovalskia,Kobo Kanaeru"
}


class draw_lots(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message_id = payload.message_id
        self.channel = self.bot.get_channel(int(draw_data.rec_channel))
        # 確定觸發事件的用戶不是機器人本身
        if payload.user_id == self.bot.user.id:
            return
        
        if message_id == draw_data.rec_id:
            if payload.emoji.name == emoji_name:
                #觸發資料
                guild = self.bot.get_guild(payload.guild_id)
                message = await guild.get_channel(payload.channel_id).fetch_message(draw_data.rec_id)
                user = guild.get_member(payload.user_id)
                #資料庫
                database = self.mongoConnect['myproject1']
                collection = database['collect1']
                try:
                    if await collection.find_one({"_id": payload.user_id}) == None:
                        firstData = {
                            "_id": payload.user_id,
                            "user_name": user.display_name,
                            "user_photo": str(user.display_avatar),
                            "sign_in": 0,
                            "draw_in": 0,
                            "draw_ID": 0,
                            "money": 5000
                        }
                        collection.insert_one(firstData) #加入會員
                except Exception as e:
                    print(e)
                    await self.channel.send("資料發生錯誤 請通知<@820697596535635968>")

                drawdata =  await collection.find_one({"_id": payload.user_id})

                try:
                    await message.remove_reaction(payload.emoji, user)
                    if drawdata['draw_in'] == 1:
                        # 如果他們已有身分組，不進行任何操作，或給予用戶通知
                        await self.channel.send(f"{user.mention} 你已經抽過籤了!")
                        return
                    else:
                        roles_to_remove = draw_data.LUCKY_ROLES_IDS
                        for role_id in roles_to_remove:
                            role = discord.utils.get(guild.roles, id=int(role_id))
                            if role:
                                await payload.member.remove_roles(role)
                        #抽籤隨機
                        fortune_list = draw_data.LUCKY_ROLES
                        fortune_roles = draw_data.LUCKY_ROLES_IDS
                        fortune_today = random.choice(fortune_list)
                        role_id = int(fortune_roles[fortune_list.index(fortune_today)])
                        role = discord.utils.get(guild.roles, id=role_id)
                        await collection.update_one({"_id": payload.user_id},{"$set": {"draw_ID": role_id}})
                        await payload.member.add_roles(role)

                        #DD隨機
                        group = message.content.split(' ')[1]
                        if group in luck_data:
                            members = luck_data[group].split(',')  # 從幸運名單中獲取該團體的成員列表
                            selected_member = random.choice(members).strip()  # 從成員列表中隨機選擇一個成員
                            response = selected_member
                        
                        #隨機數字、顏色
                        luck_colors = ['紅色', '藍色', '綠色', '黃色', '粉紅色', '橙色', '紫色', '淺藍色', '灰色', '棕色', '黑色', '白色', '金色', '銀色']
                        selected_colors = random.sample(luck_colors, 1)
                        luck_number = random.randint(1, 100)

                        # 創建運勢提醒訊息
                        embed = discord.Embed(title=f"今日抽籤運勢", colour=0x00b0f4)
                        embed.add_field(name="今日DD",
                                        value=response,
                                        inline=True)
                        embed.add_field(name="幸運顏色",
                                        value=selected_colors,
                                        inline=True)
                        embed.add_field(name="幸運數字",
                                        value=luck_number,
                                        inline=True)

                        embed.set_image(url=f"{fortune_today}")
                        await self.channel.send(f"{user.mention}")
                        await self.channel.send(embed=embed)
                        #更新狀態
                        await collection.update_one({"_id": payload.user_id}, {"$set": {"draw_in": 1}})
                except Exception as e:
                    print(e)
                    await self.channel.send("資料發生錯誤 請通知<@820697596535635968>") 

    @commands.command()
    async def adda(self, ctx, message_id: str):
        message = await ctx.fetch_message(message_id)
        await message.add_reaction(draw_data.rec_emoji)

async def setup(bot):
    await bot.add_cog(draw_lots(bot))
