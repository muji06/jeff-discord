from discord.ext import commands
import discord
import json
from requests import get

class nightwave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='nightwave', description="Show the current Nightwave Rotation",aliases=['nw','night'])
    async def sortie(self, ctx, lang:str = None):
        """
        Usage: !nightwave <language>\n
        Defualt language is en (english)\n
        Show the current Nightwave Rotation
        """
        if lang is None:
            lang = 'en'
        response = get(f"https://api.warframestat.us/PC/nightwave?language={lang}")
        data = json.loads(response.text)

        embed = discord.Embed(
            title=f"{data['tag']}",
            description=f"Challenges:",
            color=discord.Colour.random()
            )
        for x in data['activeChallenges'] :
            nw_type=""
            if 'isDaily' in x and x['isDaily'] == True:
                nw_type="Daily"
            elif x['isElite'] == True:
                nw_type="Elite Weekly"
            else:
                nw_type="Weekly"
            embed.add_field(
                name=f"{nw_type}:{x['desc']}",
                value=f"{x['reputation']} Reputation",
                inline=False
            )
        

        embed.set_footer(text="Valid Languages: en, es, fr, it, ko, pl, pt, ru, zh")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(nightwave(bot))