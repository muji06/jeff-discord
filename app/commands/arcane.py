from discord.ext import commands
from discord import app_commands
import discord
import json
from requests import get
from funcs import find,polarity
import time
import re

class arcane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='arcane', with_app_command=True, description="Shows the matching arcane")
    @app_commands.guilds(discord.Object(id=992897664087760979))
    async def mod(self, ctx,*, arcane:str = None):
        """
        Usage: !arcane <arcane-name>\n
        Shows the closest matching arcane and its market price
        """
        start = time.time()
        if arcane is None:
            error = discord.Embed(
                description="Please provide an arcane."
            )
            await ctx.send(embed=error)
            return

        arcane = arcane.title()
        
        
        res_snekw = get('https://wf.snekw.com/arcane-wiki')
        snekw = json.loads(res_snekw.text)['data']['Arcanes']
        data = None
        for x in snekw:
            # print(f"{data['name']} vs {snekw[x]['Name']}")
            if arcane in snekw[x]['Name']:
                # print('Found mod!!!!!!!!!!!!!!!!!!!!!')
                data = snekw[x]
                break

        if data is None:
            error = discord.Embed(
                description="Be sure to type the correct arcane name."
            )
            await ctx.send(embed=error)
            return

        price_unranked = await find(data['Name'],0)
        price_ranked = await find(data['Name'],data['MaxRank'])
        stats = f"{data['Criteria']}:{chr(10)}"+re.sub('<br \/>',chr(10),str(data['Description']))
        arcane_embed = discord.Embed(
            title=f"{data['Name']} | {data['Rarity']}",
            description=f"***At maximum rank ({data['MaxRank']})***{chr(10)}{chr(10)}{stats}{chr(10)}{chr(10)}Unranked: {price_unranked}{chr(10)}Rank {data['MaxRank']}: {price_ranked}"
        )
        arcane_embed.set_footer(
            text=f"Latency: {round((time.time() - start)*1000)}ms"
        )
        await ctx.send(embed=arcane_embed)


async def setup(bot):
    await bot.add_cog(arcane(bot), guild= discord.Object(id=992897664087760979))