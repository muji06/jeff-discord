from discord.ext import commands
import discord
import json
from requests import get
from funcs import find, update_cache
import time
import re
from redis_manager import cache

class arcane(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='arcane', with_app_command=True, description="Shows the matching arcane")
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def arcane(self, ctx,*, arcane:str = None):
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
        
        donwload_start = time.time()
        cached = True
        # check if we have data cached
        if cache.cache.exists("arcane:1"):
            cached_arcanes = json.loads(cache.cache.get("arcane:1"))
            snekw = cached_arcanes['Arcanes']
        else:
            cached = False
            update_cache("arcane:1",cache)
            try:
                cached_arcanes = json.loads(cache.cache.get("arcane:1"))
                snekw = cached_arcanes['Arcanes']
            except KeyError:
                error = discord.Embed(
                    description="[BROKEN FOR NOW] Arcane names could not be pulled from warframe wiki"
                )
                await ctx.send(embed=error)
                return
                
        download_timer = time.time() - donwload_start
        data = None
        for x in snekw:
            # print(f"{data['name']} vs {snekw[x]['Name']}")
            if arcane in snekw[x]['Name']:
                # print('Found mod!!!!!!!!!!!!!!!!!!!!!')
                data = snekw[x]
                break

        if data is None:
            error = discord.Embed(
                description="Be sure to type the correct arcane name. [BROKEN] new arcane names could not be pulled from warframe wiki"
            )
            await ctx.send(embed=error)
            return
        market_start = time.time()
        price_unranked = find(data['Name'],0)
        price_ranked = find(data['Name'],data['MaxRank'])
        market_timer = time.time() - market_start
        criteria = ""
        if data['Criteria']:
            criteria = f"{data['Criteria']}:{chr(10)}"
        stats = f"{criteria}"+re.sub('<br \/>',chr(10),str(data['Description']))
        arcane_embed = discord.Embed(
            title=f"{data['Name']} | {data['Rarity']}",
            description=f"***At maximum rank ({data['MaxRank']})***{chr(10)}{chr(10)}{stats}{chr(10)}{chr(10)}Unranked: {price_unranked}{chr(10)}Rank {data['MaxRank']}: {price_ranked}"
        )
        if not cached:
            arcane_embed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}Market Price Latency: {round(market_timer*1000)}ms"
            )
        else:
            arcane_embed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Cached Latency: {round(download_timer*1000)}ms{chr(10)}Market Price Latency: {round(market_timer*1000)}ms"
            )
        await ctx.send(embed=arcane_embed)


async def setup(bot):
    await bot.add_cog(arcane(bot))