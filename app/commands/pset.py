from discord.ext import commands
from discord import app_commands
import discord
import json
import time
from requests import get
from redis_manager import cache

class pset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="pset", with_app_command=True)
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def ping(self, ctx,*, prime):
        start = time.time()
        if prime is None:
            error = discord.Embed(
                description="Be sure to provide a prime name"
            )
            await ctx.send(embed=error)
            return
        elif 'forma' in prime.lower():
            error = discord.Embed(
                description="Why would you search forma"
            )
            await ctx.send(embed=error)
            return
        
        download_start = time.time()
        metadata = get('https://wf.snekw.com/void-wiki/meta').json()
        
        cached = True
        # check if we have data cached
        if cache.cache.exists("void:1"):
            cached_void = json.loads(cache.cache.get("void:1"))
        else:
            cached = False

        if cached and cached_void['meta']['hash'] == metadata['meta']['hash']:
            data = cached_void
        else:
            cached = False # recreate it later
            res = get('https://wf.snekw.com/void-wiki')
            data = json.loads(res.text)
            
        download_timer = time.time() - download_start
        calculation_start = time.time()
        primes = data['data']['PrimeData']
        text = ''
        item = ''
        return
        




async def setup(bot):
    await bot.add_cog(pset(bot))
