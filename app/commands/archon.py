from discord.ext import commands
import discord
import json
from requests import get
from funcs import get_shard

class archon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='archon', description="Show the current Archon Hunt Rotation",aliases=['archonhunt','sportie','ah'])
    async def sortie(self, ctx, lang:str = None):
        """
        Usage: !archon <language>\n
        Defualt language is en (english)\n
        Show the current archon Rotation
        """
        if lang is None:
            lang = 'en'
        response = get(f"https://api.warframestat.us/pc/archonHunt?language={lang}")
        data = json.loads(response.text)

        embed = discord.Embed(
            title="Archon Hunt",
            description=f"Boss: {data['boss']}({get_shard(data['boss'])})\nFaction: {data['faction']}",
            color=discord.Colour.random()
            )

        for x in range(len(data["missions"])):
            mission = data["missions"][x]
            embed.add_field(name=f"({x+1}) {mission['type']}",
            value=f"{mission['node']}",
            inline=False)

        embed.set_footer(text=f"Ends in {data['eta']}\nValid Languages: en, es, fr, it, ko, pl, pt, ru, zh")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(archon(bot))