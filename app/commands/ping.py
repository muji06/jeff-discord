from discord.ext import commands
from discord import app_commands
import discord
import json
import requests
from redis_manager import cache

class ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="ping", with_app_command=True)
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def ping(self, ctx: commands.Context):
        # await ctx.send("Pong")
        cache.cache.ping()
        await ctx.send("Pong")
    # @app_commands.command(name="ping")
    # @app_commands.guilds(discord.Object(id=970744489171898458))
    # async def ping(self, interaction: discord.Interaction):
    #     await interaction.response.send_message('Pong')



async def setup(bot):
    await bot.add_cog(ping(bot))
