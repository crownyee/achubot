import logging

import discord
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio
from datetime import datetime
import core.__draw__ as draw_data
from core.__whitelist__ import mywhite
from core.__mogo__ import my_mongodb

logging.basicConfig(filename='./json/error_log.txt', level=logging.ERROR)

class MyDATA(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.collection = my_mongodb.collection
        self.channel = self.bot.get_channel(int(draw_data.DRAW_channel))
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()

    #簽到
    @app_commands.command(name='daily',description="每日簽到")
    async def daily(self, ita:discord.Interaction):
        await ita.response.defer()
        try:
            if await self.collection.find_one({"_id": ita.user.id}) == None:
                firstData = {
                    "_id": ita.user.id,
                    "user_name": ita.user.display_name,
                    "user_photo": str(ita.user.display_avatar),
                    "sign_in": 0,
                    "draw_in": 0,
                    "draw_ID": "",
                    "money": 5000,
                    "Backpack": {}
                }
                await ita.edit_original_response(content=f"首次簽到已新增個人資料")
                self.collection.insert_one(firstData) #加入會員  
            
            userData = await self.collection.find_one({"_id": ita.user.id}) # Fetch
            if userData['sign_in'] == 1:  
                await ita.edit_original_response(content=f"今日已簽到")
            else:
                userData['sign_in'] = 1   
                userData['money'] += 1000  
                await self.collection.replace_one({"_id": ita.user.id}, userData) #更新  
                await ita.edit_original_response(content=f'簽到成功!')
        except Exception as e:
            logging.error(f"mongo.py  daily: {e}")
            await ita.edit_original_response(content=f"資料發生錯誤 請通知管理員") 

    #顯示個人資訊
    @app_commands.command(name='information', description="個人資訊")
    async def information(self, ita: discord.Interaction):
        infodata = await self.collection.find_one({"_id": ita.user.id})
        await self.collection.update_one({"_id": ita.user.id}, {"$set": {"user_name":ita.user.display_name}})
        await self.collection.update_one({"_id": ita.user.id},{"$set": {"user_photo": str(ita.user.display_avatar)}})
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
                            value=f"{draw_role.mention}",  
                            inline=True)
            
            embed.add_field(name="錢包",
                            value=infodata['money'],  
                            inline=True)
            embed.set_thumbnail(url=f"{str(ita.user.display_avatar)}")
            await ita.response.send_message(embed=embed,ephemeral=True)
        except Exception as e:
            logging.error(f"mongo.py  information: {e}")
            await ita.response.send_message("資料發生錯誤 請通知管理員")

    #手動
    @app_commands.command(name='init',description="初始化資料(admin only)")
    @app_commands.check(mywhite.iswhitelist)  
    async def init(self, ita:discord.Interaction):
        await ita.response.defer()
        try:
            await self.collection.update_many({},{"$set":{"sign_in": 0}})
            await self.collection.update_many({},{"$set":{"draw_in": 0}})

            await ita.edit_original_response(content=f'成功!')
        except Exception as e:
            logging.error(f"mongo.py  init: {e}")
    
    #給錢
    @app_commands.command(name='give', description="(admin only)")
    @app_commands.check(mywhite.iswhitelist)  
    async def give(self, ita: discord.Interaction, user_: discord.User, give_: int):
        await ita.response.defer()
        try:
            userData = await self.collection.find_one({"_id": user_.id})
            money = userData['money']  
            money += give_
            await self.collection.update_one(
                {"_id": user_.id},
                {"$set": {"money": money}},
            )
            embed = discord.Embed(
                title="發送點數",
                description=f"已發送{give_}給{user_.mention}",
                colour=0x5636a1
            )
            await ita.edit_original_response(embed=embed)
        except Exception as e:
            logging.error(f"mongo.py give: {e}")
async def setup(bot):
    await bot.add_cog(MyDATA(bot))
'''
# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
#database = client['myproject1']
#collection
#collection = database['collect1']


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