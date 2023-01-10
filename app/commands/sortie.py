from discord.ext import commands
from discord import app_commands
import discord
import json
from requests import get

class sortie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='sortie',  with_app_command=True, description="Show the current Sortie Rotation")
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def sortie(self, ctx, lang:str = None):
        """
        Usage: !sortie <language>\n
        Defualt language is en (english)\n
        Show the current Sortie Rotation
        """
        if lang is None:
            lang = 'en'
        response = get(f"https://api.warframestat.us/pc/sortie?language={lang}")
        data = json.loads(response.text)

        embed = discord.Embed(
            title="Sortie",
            description=f"Boss: {data['boss']}\nFaction: {data['faction']}",
            color=discord.Colour.random()
            )

        for x in range(len(data["variants"])):
            mission = data["variants"][x]
            embed.add_field(name=f"({x+1}) {mission['missionType']}",
            value=f"{mission['node']}\nCondition: {mission['modifier']}\nEffect: {mission['modifierDescription']}",
            inline=False)

        embed.set_footer(text=f"Ends in {data['eta']}\nValid Languages: en, es, fr, it, ko, pl, pt, ru, zh")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(sortie(bot))