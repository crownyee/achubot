import discord
from discord.ext import commands
from core.__init__ import Cog_Extension
import motor.motor_asyncio
import random, asyncio
import core.__draw__ as draw_data
from core.__mogo__ import my_mongodb

class draw_button(Cog_Extension):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def draw_fortune(self, interaction):
        #基礎資料獲得
        user = interaction.user
        myguild = interaction.guild
        member = interaction.user
        collection = my_mongodb.collection
        self.channel
        try:
            if await collection.find_one({"_id": user.id}) == None:
                firstData = {
                    "_id": user.id,
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

        try:
            drawdata =  await collection.find_one({"_id": user.id})
            
            if drawdata['draw_in'] == 1:
                # 如果他們已有身分組，不進行任何操作，或給予用戶通知
                await self.channel.send(f"{user.mention} 你已經抽過籤了!")
                return
            else:
                # 移除先前的幸運身分組
                roles_to_remove = draw_data.LUCKY_ROLES_IDS
                for _role_id in roles_to_remove:
                    role = discord.utils.get(myguild.roles, id=int(_role_id))
                    if role in member.roles:
                        await member.remove_roles(role)

                # 抽取新的幸運身分組
                fortune_list = draw_data.LUCKY_ROLES
                fortune_roles = draw_data.LUCKY_ROLES_IDS
                fortune_today = random.choice(fortune_list)
                role_id = int(fortune_roles[fortune_list.index(fortune_today)])
                role = discord.utils.get(myguild.roles, id=role_id)
                await collection.update_one({"_id": user.id},{"$set": {"draw_ID": role_id}})
                await member.add_roles(role)
                #DD隨機
                group = random.choice(list(draw_data.luck_data.keys()))
                members = draw_data.luck_data[group].split(',')
                selected_member = random.choice(members).strip()
                
                #隨機數字、顏色
                selected_colors = random.choice(draw_data.luck_colors)  # 選取一個顏色
                luck_number = random.randint(1, 100)

                # 創建運勢提醒訊息
                embed = discord.Embed(title=f"今日抽籤運勢", colour=0x00b0f4)
                embed.add_field(name="今日DD",
                                value=selected_member,
                                inline=True)
                embed.add_field(name="幸運顏色",
                                value=selected_colors,
                                inline=True)
                embed.add_field(name="幸運數字",
                                value=luck_number,
                                inline=True)

                embed.set_image(url=f"{fortune_today}")
                embed.set_thumbnail(url=f"{drawdata['user_photo']}")
                await self.channel.send(f"{user.mention} BAU BAU ~ 今天的解籤是:")
                await self.channel.send(embed=embed)
                #更新狀態
                await collection.update_one({"_id": user.id}, {"$set": {"draw_in": 1}})
        except Exception as e:
            print(e)
            await self.channel.send("資料發生錯誤 請通知<@820697596535635968>")
             
    @commands.command()
    async def createbutton(self,ctx):
        button = discord.ui.Button(label="抽籤!", style=discord.ButtonStyle.primary, custom_id="button_respond")

        async def button_callback(interaction):
            await interaction.response.defer()
            await self.draw_fortune(interaction) 

        button.callback = button_callback
        view = discord.ui.View()
        view.add_item(button)
        await ctx.send(draw_data.PERO_draw, view=view)

    @commands.Cog.listener()
    async def on_interaction(self, interaction: discord.Interaction):
        # interaction.data 是一個包含交互資訊的字典
        # 有些交互不包含 custom_id，需要判斷式處理來防止出錯
        if "custom_id" in interaction.data:
            if interaction.data["custom_id"] == "button_respond":
                await interaction.response.defer()
                await self.draw_fortune(interaction)
    
async def setup(bot):
    await bot.add_cog(draw_button(bot))

