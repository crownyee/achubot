import sys,os
import discord
from discord import app_commands
from discord.ext import commands,tasks
import json,asyncio
#import TOOLS.bus_d as bus_run
with open('./json/setting.json','r',encoding='utf8') as jfile:
    jdata = json.load(jfile)

# Discord機器人令牌
TOKEN = jdata['MTOKEN']
intents = discord.Intents.all()
#intents.message_content = True
#intents.members = True
#intents.typing = True
#intents.presences = True
bot = commands.Bot(command_prefix = ['!','！'], intents=intents)

#開機，重啟
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="FUWAMOCO✔️"))
    await bot.tree.sync()
    print("Ready")

@commands.has_permissions(administrator=True)
@bot.command() 
async def frt(ctx):
    try:
        await ctx.send("重啟bot...") 
        await ctx.message.delete()
        os.execv(sys.executable, ['python'] + sys.argv)
    except discord.errors.NotFound:
        pass
    
#重新加載bus資料夾的程式
@bot.command()
async def reload_bus(ctx):
    try:
        for filename in os.listdir("./bus"):
            if filename.endswith(".py"):
                module_name = f"bus.{filename[:-3]}"
                await bot.reload_extension(module_name)
        await ctx.send("已成功重新載入 `bus` 資料夾中的程式")
    except discord.errors.NotFound:
        pass

#Load
async def loadExtensions():
    folders = [
        'cmds',
        'game',
        'holo',
        'data'
    ]
    for folder in folders:
        for filename in os.listdir(f"./{folder}"):
            if filename.endswith('.py'):
                await bot.load_extension(f"{folder}.{filename[:-3]}")

async def main():
    async with bot:
        await loadExtensions()
        #asyncio.create_task(bus_run.run_data_fetch())
        await bot.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())


'''
#開機，重啟
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="FUWAWA的肚子✔️"))
    await bot.tree.sync()
    channel = bot.get_channel(int(jdata['wake_mes']))
    print("...")
    await channel.send("我醒了")

#@commands.has_permissions(administrator=True)
@bot.command() 
async def frt(ctx):
    await ctx.send("重啟bot...") 
    await ctx.message.delete()
    #重启bot
    os.execv(sys.executable, ['python'] + sys.argv)

#@commands.has_permissions(administrator=True)
@bot.command()
async def fst(ctx):
    await ctx.send('Shutting down...')
    await ctx.message.delete()
    await bot.close()

'''


'''#重新加載bus資料夾的程式
@bot.command()
async def reload_bus(ctx):
    try:
        await bot.unload_extension('bus')
        for filename in os.listdir(f"./bus"):
            if filename.endswith('.py'):
                await bot.load_extension(f"bus.{filename[:-3]}")

        await ctx.send('已重新載入 bus 資料夾的程式')
    except Exception as e:
        await ctx.send(f'重新載入失敗: {e}')'''