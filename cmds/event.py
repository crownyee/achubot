import discord
import re, random
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import json, asyncio, os, sys

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)


class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author == self.bot.user:
            return

        # 檢查 @everyone 警告
        if "@everyone" in msg.content:
            mag_channel = self.bot.get_channel(int(jdata['manage_Channel']))
            embed = discord.Embed(title="違規名單",
                    colour=0x00b0f4)
            embed.add_field(name=f"",
                            value=f"{msg.author.mention}\nID:{msg.author.id}",
                            inline=False)
            embed.add_field(name=f"內容",
                            value=f"{msg.content}",
                            inline=False)
            #warning_msg = f"{msg.author.display_name} (ID: {msg.author.id}) WARNING"
            await mag_channel.send(embed=embed)

        # 檢查 "XXX的機率"
        elif msg.channel.id == int(jdata['probability_channel']) and re.search(r"的機率$", msg.content):
            probability = random.randint(0, 100)
            await msg.channel.send(f"{msg.content}:{probability}%")

        # 檢查自定義!命令
        elif msg.content.startswith('!'):
            try:
                with open('./json/commands.json', 'r', encoding='utf-8') as f:
                    command_dict = json.load(f)
            except FileNotFoundError:
                command_dict = {}

            cmd = msg.content[1:]
            if cmd in command_dict:
                await msg.channel.send(command_dict[cmd])

        # 處理其他指令
        await self.bot.process_commands(msg)

async def setup(bot):
    await bot.add_cog(Event(bot))


'''

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(jdata['join_leave'])
        await channel.send(f'{member} 歡迎加入，請詳閱群規 ! !')
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(jdata['join_leave'])
        await channel.send(f'{member} 變成 DD 叛逃了 ! !')
'''
'''
        def check(reaction, user):
            return str(reaction.emoji) == "❌" and reaction.message.id == bot_msg.id and user == msg.author
        
        #https://x.com/shiorinovella/status/1685514440517484544?s=20
        if re.search(r'https?://(?:x\.com|twitter\.com)/[^/]+/status/\d+', msg.content):
            replaced_message = re.sub(r'(?:x\.com|twitter\.com)', 'vxtwitter.com', msg.content)
            mention = f"By {msg.author.mention} 轉發了一則訊息"
            await msg.delete()
            bot_msg = await msg.channel.send(mention + "\n" + replaced_message)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                await bot_msg.delete()

        #https://www.phixiv.net
        if re.search(r'https?://www.(?:pixiv\.net)', msg.content):
            replaced_message = re.sub(r'(?:pixiv\.net)', 'phixiv.net', msg.content)
            mention = f"By {msg.author.mention} 轉發了一則訊息"
            await msg.delete()
            bot_msg = await msg.channel.send(mention + "\n" + replaced_message)

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                pass

            else:
                await bot_msg.delete()
'''