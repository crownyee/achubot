import discord
from discord.ext import commands
from holodex.client import HolodexClient

from core import __json__
jdata = __json__.load_json('./json/setting.json')

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.holodex_client = HolodexClient(jdata['HOLODEX_API_KEY'])
        self.holodex_client_2 = HolodexClient(jdata['HOLODEX_API_KEY_2'])
        self.holodex_client_3 = HolodexClient(jdata['HOLODEX_API_KEY_3'])