import discord
import re, random
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import json, asyncio

with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

target_user_id = int(jdata['BOT_ID'])
target_channel_id = int(jdata['Chat_Channel'])
reaction_emoji_1 = jdata['rec_love1']
reaction_emoji_2 = jdata['rec_love2']
class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
        # 获取删除的消息内容和相关信息
        content = message.content
        author = message.author
        channel = message.channel
        attachment_urls = " "
        if message.stickers:
            sticker_names = "\n".join([sticker.name for sticker in message.stickers])
            content += f"\n貼圖：\n{sticker_names}"

        mag_channel = self.bot.get_channel(int(jdata['message_log']))
        embed = discord.Embed(title=f":x: {channel} 刪除的訊息LOG",
            colour=0x00b0f4)
        embed.add_field(name=f"",
                        value=f"{author.mention}",
                        inline=False)
        embed.add_field(name=f"內容",
                        value=f"{content}",
                        inline=False)
                        
        if message.attachments:
            attachment_urls = "\n".join([attachment.url for attachment in message.attachments])
            embed.set_image(url=f"{attachment_urls}")   
            
        await mag_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, msg):
        # 檢查 "XXX的機率"
        if msg.channel.id == int(jdata['probability_channel']) and re.search(r"的機率$", msg.content):
            probability = random.randint(0, 100)
            await msg.channel.send(f"{msg.content}:{probability}%")

        # 檢查特定消息
        elif msg.channel.id == int(jdata['probability_channel']) and re.match(r"雙子幫我選.*? (.+)", msg.content):
            match = re.match(r"雙子幫我選.*? (.+)", msg.content) # 使用正则表达式匹配

            if match:
                items_input = match.group(1)  # 获取物品部分
                items = items_input.split('/')

                if len(items) > 1:  # 多物品
                    selected_item = random.choice(items) 
                    await msg.channel.send(f"FUWAMOCOが選んだ {selected_item} BAU!BAU!")
                else:
                    await msg.channel.send(f"FUWAMOCOが選んだ{selected_item} BAU!BAU!")
                
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
    elif msg.author.id == target_user_id and msg.channel.id == target_channel_id:
        await msg.add_reaction(reaction_emoji_1)
        await msg.add_reaction(reaction_emoji_2)


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