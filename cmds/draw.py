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
                        #如果找到對應身分組，給用戶添加身分組
                        fortune_list = draw_data.LUCKY_ROLES
                        fortune_roles = draw_data.LUCKY_ROLES_IDS
                        fortune_today = random.choice(fortune_list)
                        role_id = int(fortune_roles[fortune_list.index(fortune_today)])
                        role = discord.utils.get(guild.roles, id=role_id)
                        await collection.update_one({"_id": payload.user_id},{"$set": {"draw_ID": role_id}})
                        await payload.member.add_roles(role)
                        
                        # 創建運勢提醒訊息
                        embed = discord.Embed(title=f"今日運勢", colour=0x00b0f4)
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


'''
                if now == '0000':
                    for guild in self.bot.guilds:
                        CLEAN_ROLES = [discord.utils.get(guild.roles, id=int(role_id)) for role_id in draw_data.LUCKY_ROLES_IDS]

                        for member in guild.members:
                            try:
                                roles_to_remove = [role for role in member.roles if role in CLEAN_ROLES]
                                if roles_to_remove:
                                    await member.remove_roles(*roles_to_remove, reason="每日運勢身分組清除")
                            except Exception as e:
                                logging.error(f"Faild for {member.name}: {e}")

                            await asyncio.sleep(0.5)

'''