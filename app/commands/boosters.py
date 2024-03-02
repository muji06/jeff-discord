from discord.ext import commands
import discord
import json
from requests import get
import time
from funcs import get_global_booster_name, discord_timestamp
from dateutil.parser import isoparse

class boosters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='boosters', with_app_command=True, description="Data about current alerts.")
    async def boosters(self, ctx):
        """
        Usage: !boosters\n
        Data about current global boosters
        """
        start = time.time()
        embed = discord.Embed(
            color=discord.Colour.random(),
            title=f"Global Boosters"
        )

        res = get('https://api.warframestat.us/PC/globalUpgrades')
        data = json.loads(res.text)
        if len(data) == 0:
            err = discord.Embed(
                color=discord.Colour.random(),
                description="There are no active global boosters currently running."
            )
            await ctx.send(embed=err)
            return

        for alert in data:
            x_eta = int(isoparse(alert.get("end")).timestamp())
            key = f"""{get_global_booster_name(alert.get("upgrade"))}"""
            value = f'Expiry: {discord_timestamp(x_eta)}'
            embed.add_field(name=key,value=value, inline=False)

        embed.set_footer(
            text=f"Latency: {round((time.time() - start)*1000)}ms"
        )
        await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(boosters(bot))