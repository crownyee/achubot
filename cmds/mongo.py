import discord
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio,json
from datetime import datetime, time
import core.__draw__ as draw_data

import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
#database = client['myproject1']
#collection
#collection = database['collect1']

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

uri = jdata['MongoAPI']
class MyDATA(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    #簽到
    @app_commands.command(name='daily',description="每日簽到")
    async def daily(self, ita:discord.Interaction):
        database = self.mongoConnect['myproject1']
        collection = database['collect1']
        try:
            if await collection.find_one({"_id": ita.user.id}) == None:
                firstData = {
                    "_id": ita.user.id,
                    "user_name": ita.user.display_name,
                    "user_photo": str(ita.user.display_avatar),
                    "sign_in": 0,
                    "draw_in": 0,
                    "draw_ID": "",
                    "money": 5000
                }
                await ita.response.send_message("已新增個人資料")
                collection.insert_one(firstData) #加入會員
            
            userData = await collection.find_one({"_id": ita.user.id}) # Fetch
            if userData['sign_in'] == 1:
                await ita.response.send_message("今日已簽到")
            else:
                userData['sign_in'] = 1
                userData['money'] += 1000
                await collection.replace_one({"_id": ita.user.id}, userData) #更新
                await ita.response.send_message("簽到成功!")
        except Exception as e:
            print(e)
            await ita.response.send_message("資料發生錯誤 請通知管理員") 

    #顯示個人資訊
    @app_commands.command(name='information', description="個人資訊")
    async def information(self, ita: discord.Interaction):
        database = self.mongoConnect['myproject1']
        collection = database['collect1']
        infodata = await collection.find_one({"_id": ita.user.id})
        #infodata['user_name'] = ita.user.display_name
        #await collection.replace_one({"_id": ita.user.id}, infodata)
        try:
            embed = discord.Embed(title="使用者資訊",
                                colour=0x00b0f4,
                                timestamp=datetime.now())
            embed.add_field(name=f"",
                            value=f"{ita.user.mention}",
                            inline=False)
            if infodata['sign_in'] == 1:
                embed.add_field(name="簽到狀態",
                                value=f"今日已簽到",
                                inline=True)
            else:
                embed.add_field(name="簽到狀態",
                                value="今日未簽到",
                                inline=True)

            draw_role = ita.guild.get_role(infodata['draw_ID'])
            embed.add_field(name="抽籤狀態",
                            value=draw_role.mention,
                            inline=True)
            
            embed.add_field(name="錢包",
                            value=infodata['money'],
                            inline=True)
            embed.set_thumbnail(url=f"{infodata['user_photo']}",)
            await ita.response.send_message(embed=embed,ephemeral=True)
        except Exception as e:
            print(e)
            await ita.response.send_message("資料發生錯誤 請通知管理員")

    #手動
    @commands.has_permissions(administrator=True)  # 只允许管理员使用
    @app_commands.command(name='init',description="初始化資料")
    async def init(self, ita:discord.Interaction):
        await ita.response.defer()

        database = self.mongoConnect['myproject1']
        collection = database['collect1']
        await collection.update_many({"_id": ita.user.id},{"$set":{"sign_in": 0}})
        await collection.update_many({"_id": ita.user.id},{"$set":{"draw_in": 0}})

        await ita.edit_original_response(content=f'成功!')
async def setup(bot):
    await bot.add_cog(MyDATA(bot))
'''
document = {
    'user_id': 1,
    'username': 'ACHU01',
    'user_photo': 'test_url',
    'sign_in': 0,
    'draw_in': 0
}

try:
    client.admin.command('ping')
    select = collection.insert_one(document)
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

'''