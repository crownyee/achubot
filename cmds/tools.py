import discord
import re
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio
import subprocess

class Mywork(Cog_Extension):
    #指令
    @commands.command()
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)

    @commands.command()
    async def bau(self, ctx, mes: str = ''):
        if mes:
            await ctx.send(f"{mes}")
        await ctx.send(f"<:0_meba_BAU:1145138276517294211> <:0_meba_BAU:1145138276517294211>")
        await ctx.message.delete()

    @commands.command()
    async def get_user_info(self,ctx, user_id):
        # 获取用户对象
        user = ctx.guild.get_member(int(user_id))
        print(user)
        if user is not None:
            # 显示图片
            avatar_url = str(user.display_avatar)
            await ctx.send(f"{avatar_url}")
            
            # 显示名字
            display_name = user.display_name
            await ctx.send(f"{display_name}")
        else:
            await ctx.send("AAAAAA")

async def setup(bot):
    await bot.add_cog(Mywork(bot))

#網頁版
'''
    @commands.command()
    async def live_space(self,ctx, account: str):
        txtfile = './json/cc.txt'
        try:
            if re.search(r'https?://(?:x\.com|twitter\.com)/i/spaces/\d+', account):
                replaced_message = re.sub(r'(?:x\.com|twitter\.com)', 'twitter.com',account)
                command = f"/home/container/.local/bin/twspace_dl -i {replaced_message} -u -s -c {txtfile}"
                master_url = subprocess.run(command,shell=True,capture_output=True,text=True)
                await asyncio.sleep(1)
                await ctx.send(f'```{master_url.stdout}```')
            else:
                command = f"/home/container/.local/bin/twspace_dl -U {account} -u -s -c {txtfile}"
                master_url = subprocess.run(command,shell=True,capture_output=True,text=True)
                await asyncio.sleep(1)
                await ctx.send(f'```{master_url.stdout}```')
        except re.KeyError:
            await ctx.send(f'URL error 請使用twitter.com的帳號或是space')
'''
#廢棄
'''
@commands.command()
async def sayed(self, ctx,*,message):
    await ctx.message.delete()
    await ctx.send(message)

command = f"twspace_dl -U {account} -u -s -c {txtfile}"
master_url = subprocess.run(command, shell=True, capture_output=True, text=True)
await ctx.send(f'```{master_url.stdout}```')
'''