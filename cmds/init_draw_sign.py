import discord
from core.__init__ import Cog_Extension
import asyncio, json
import motor.motor_asyncio
from datetime import datetime, timedelta

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

uri = jdata['MongoAPI']

class init_test(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mongoConnect = motor.motor_asyncio.AsyncIOMotorClient(uri)

        async def SignIn():
            await self.bot.wait_until_ready()

            while not self.bot.is_closed():
                now = datetime.now()
                now = now.strftime('%H%M')
                if now == '0018':
                    database = self.mongoConnect['myproject1']
                    collection = database['collect1']
                    await collection.update_many({}, {"$set": {"sign_in": 0}})  
                    await collection.update_many({}, {"$set": {"draw_in": 0}})       

                await asyncio.sleep(60)  # 等待下一次檢查

        self.bg_draw = asyncio.create_task(SignIn())

async def setup(bot):
    await bot.add_cog(init_test(bot))

'''
網站版
time_f = datetime.now() - timedelta(hours=16)
now = time_f.strftime('%H%M')
'''