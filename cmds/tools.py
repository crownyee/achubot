import discord
import re
from discord import app_commands
from discord.ext import commands
from core.__init__ import Cog_Extension
import asyncio
import subprocess
from core.__whitelist__ import mywhite
class Mywork(Cog_Extension):
    #指令
    @commands.command()
    @commands.check(mywhite.iswhitelist)
    async def clean(self, ctx, num: int):
        await ctx.channel.purge(limit=num + 1)
 
    @commands.command()
    @commands.check(mywhite.iswhitelist)
    async def bau(self, ctx, mes: str = ''):
        if mes:
            await ctx.send(f"{mes}")
        await ctx.send(f"<:0_meba_BAU:1145138276517294211> <:0_meba_BAU:1145138276517294211>")
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(Mywork(bot))

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