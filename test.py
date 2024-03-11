import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.all()
#intents.message_content = True
#intents.members = True
#intents.typing = True
#intents.presences = True
bot = commands.Bot(command_prefix = ['!','！'], intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def create(ctx):
    button = Button(label="按我！", style=discord.ButtonStyle.primary, custom_id="button_respond")


    view = View()
    view.add_item(button)
    await ctx.send("點擊下面的按鈕！", view=view)

bot.run('MTEzNTU3ODcwODE0OTgwNTE2OA.Gdfjh1.-EIDNMhAPp0UM9gQu50t5bC54MbeWGKqYc1nck')