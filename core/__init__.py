import discord
from discord.ext import commands
from holodex.client import HolodexClient

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.holodex_client = HolodexClient('533d4a71-c7e4-4b75-ba49-f0f9c2808ad2')
        self.holodex_client_2 = HolodexClient('75cf3c69-8ef8-4360-bcf0-d10dbd9b93dc')