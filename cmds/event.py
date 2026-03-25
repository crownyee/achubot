#Discord
import discord
from discord import app_commands
from discord.ext import commands
#Cog
from core.__init__ import Cog_Extension

#Tools
import re, random
import asyncio

#Json
from core import __json__
jdata = __json__.get_setting_data()


class Event(Cog_Extension):

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author == self.bot.user:
            return
    
        content = message.content or "(無文字內容)"
        author = message.author
        channel = message.channel
        attachment_urls = []

        #圖片
        if message.attachments:
            attachment_urls = [attachment.url for attachment in message.attachments]

        message_log_channel = self.bot.get_channel(int(jdata['message_log']))
        embed = discord.Embed(
            title=":x: 訊息被刪除",
            description=f"頻道：{channel.mention}",
            colour=0x00b0f4,
            timestamp=discord.utils.utcnow()
        )
        embed.set_author(name=f"{author} (ID: {author.id})", icon_url=author.display_avatar.url)

        #顯示名字和display name
        embed.add_field(
            name="",
            value=f"{author.mention}（{author.display_name}）",
            inline=False)
        embed.add_field(name="內容", value=content, inline=False)

        #圖片
        if attachment_urls:
            embed.set_image(url=attachment_urls[0])  # 第一張圖直接顯示
            if len(attachment_urls) > 1:
                import aiohttp, io
                for url in attachment_urls[1:]:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                img_bytes = await resp.read()
                                filename = url.split("/")[-1].split("?")[0].split(":")[0]
                                file = discord.File(io.BytesIO(img_bytes), filename=filename)
                                #await message_log_channel.send(file=file, reference=None, mention_author=False)


        await message_log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        await asyncio.sleep(1)

        if msg.author.bot:
            return

        # 檢查自定義!命令
        if msg.content.startswith('!'):
            try:
                command_dict = __json__.load_json('./json/commands.json')
            except FileNotFoundError:
                command_dict = {}

            cmd = msg.content[1:].split()[0]
            if cmd in command_dict:
                await msg.channel.send(command_dict[cmd])
                return

        # 檢查 "XXX的機率"
        elif msg.channel.id == int(jdata['probability_channel']) and re.search(r"的機率$", msg.content):
            probability = random.randint(0, 100)
            await msg.channel.send(f"{msg.content}:{probability}%")


        # 檢查特定消息
        elif msg.channel.id == int(jdata['probability_channel']) and re.match(r"雙子幫我選.*? (.+)", msg.content):
            match = re.match(r"雙子幫我選.*? (.+)", msg.content) # 正則表達式

            if match:
                items_input = match.group(1)  # 物品分割
                items = items_input.split('/')

                if len(items) > 1:  # 多物品
                    selected_item = random.choice(items) 
                    await msg.channel.send(f"FUWAMOCOが選んだ {selected_item} BAU!BAU!")
                else:
                    await msg.channel.send(f"FUWAMOCOが選んだ{selected_item} BAU!BAU!")

        # 處理其他指令
        await self.bot.process_commands(msg)

async def setup(bot):
    await bot.add_cog(Event(bot))


'''
target_user_id = jdata['BOT_ID']
target_channel_id = jdata['Chat_Channel']
reaction_emoji_1 = jdata['rec_love1']
reaction_emoji_2 = jdata['rec_love2']

    elif msg.author.id == target_user_id and msg.channel.id == target_channel_id:
        await msg.add_reaction(reaction_emoji_1)
        await msg.add_reaction(reaction_emoji_2)


    # 檢查 @everyone 警告
    if "@everyone" in msg.content:
        ban_log_channel = self.bot.get_channel(jdata['ban_Channel'])
        embed = discord.Embed(title="違規名單",
                colour=0x00b0f4)
        embed.add_field(name=f"",
                        value=f"{msg.author.mention}\nID:{msg.author.id}",
                        inline=False)
        embed.add_field(name=f"內容",
                        value=f"{msg.content}",
                        inline=False)
        #warning_msg = f"{msg.author.display_name} (ID: {msg.author.id}) WARNING"
        await ban_log_channel.send(embed=embed)

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