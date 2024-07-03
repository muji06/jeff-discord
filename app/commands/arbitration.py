from math import floor
from discord.ext import commands
import discord
import json
from requests import get
import time
from datetime import datetime

class arbitration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='arbitration', description="Data about current arbitration.",aliases=['arbie','arbi','arb'])
    async def arbitration(self, ctx):
        """
        Usage: !arbitration\n
        Data about current arbitration.
        """
        start = time.time()
        res = get('https://api.warframestat.us/pc/arbitration')
        data = json.loads(res.text)
        expiry= datetime.strptime(data['expiry'],'%Y-%m-%dT%H:%M:%S.%f%z').astimezone()
        now = datetime.fromtimestamp(time.time()).astimezone()
        delta = expiry - now
        seconds = floor(delta.total_seconds()%60)
        minutes = floor(delta.total_seconds()/60)

        embed = discord.Embed(
            color=discord.Colour.random(),
            title=f"Arbitration{chr(10)}{data['type']} | {data['enemy']}",
            description=f"**{data['node']}**"
        )

        embed.set_footer(
            text=f"{minutes} minutes and {seconds} seconds remaining.{chr(10)}"+f"Latency: {round((time.time() - start)*1000)}ms"
        )
        await ctx.send(embed=embed)

    @discord.app_commands.command(name='arbie', description="Data about current arbitration.")
    async def arbitration_slash(self, interaction: discord.Interaction):
        """
        Usage: !arbitration\n
        Data about current arbitration.
        """
        start = time.time()
        res = get('https://api.warframestat.us/pc/arbitration')
        data = json.loads(res.text)
        expiry= datetime.strptime(data['expiry'],'%Y-%m-%dT%H:%M:%S.%f%z').astimezone()
        now = datetime.fromtimestamp(time.time()).astimezone()
        delta = expiry - now
        seconds = floor(delta.total_seconds()%60)
        minutes = floor(delta.total_seconds()/60)

        embed = discord.Embed(
            color=discord.Colour.random(),
            title=f"Arbitration{chr(10)}{data['type']} | {data['enemy']}",
            description=f"**{data['node']}**"
        )

        embed.set_footer(
            text=f"{minutes} minutes and {seconds} seconds remaining.{chr(10)}"+f"Latency: {round((time.time() - start)*1000)}ms"
        )
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(arbitration(bot))