from math import floor
from discord.ext import commands
import discord
import json
from requests import get
import time

class listen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='listen', invoke_without_command=True, aliases=["listener"])
    async def listen(self, ctx):
        pass
        
async def setup(bot):
    await bot.add_cog(listen(bot))