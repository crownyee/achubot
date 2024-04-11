import discord
from discord.ext import commands
from holodex.client import HolodexClient

class Cog_Extension(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.holodex_client = HolodexClient('df1fab08-008b-42cf-8620-4a8776e9dd0d')
        self.holodex_client_2 = HolodexClient('5c22346d-1381-4a29-96c6-739814d36006')
        self.holodex_client_3 = HolodexClient('4372f53a-5865-431c-97d2-313ce173c479')