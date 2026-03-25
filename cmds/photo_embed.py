#Discord
import discord
from discord import app_commands
from discord.ext import commands
#Cog
from core.__init__ import Cog_Extension

#Tools
import re, random
import aiohttp,io
import asyncio

#Json
from core import __json__
jdata = __json__.get_setting_data()


class photo_embed(Cog_Extension):


    @commands.Cog.listener()
    async def on_message(self, msg):
        # 忽略自己的消息
        if msg.author == self.bot.user:
            return

        await asyncio.sleep(1)

        all_category = jdata['photo_category']
        if msg.channel.category and (str(msg.channel.category.id) in all_category):
            await asyncio.sleep(0.5)
            image_urls = []
            attachment_image_urls = []
            
            # 處理嵌入中的圖片
            for embed in msg.embeds:
                if embed.image and embed.image.url:
                    image_urls.append(embed.image.url)


            #if msg.attachments:
            #    for attachment in msg.attachments:
            #        await msg.channel.send(attachment.url)

            if image_urls:
                for url in image_urls:
                    # 下載圖片
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as resp:
                            if resp.status == 200:
                                img_bytes = await resp.read()
                                filename = url.split("/")[-1].split("?")[0].split(":")[0]
                                file = discord.File(io.BytesIO(img_bytes), filename=filename)
                                await msg.channel.send(file=file)

    @app_commands.command(name="upload_image")
    @commands.has_permissions(administrator=True)
    async def upload_image(self, interaction: discord.Interaction, upfile: discord.Attachment):
        await interaction.response.defer(ephemeral=True)
        # 下載圖片
        img_bytes = await upfile.read()
        filename = upfile.filename
        download_file = discord.File(io.BytesIO(img_bytes), filename=filename)
        # 由Bot傳送圖片到同一頻道
        await interaction.channel.send(file=download_file)
        await interaction.followup.send("SUCCESS", ephemeral=True)


async def setup(bot):
    await bot.add_cog(photo_embed(bot))