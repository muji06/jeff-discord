from discord.ext import commands
from discord import app_commands
import discord
import json
import time
from requests import get
from redis_manager import cache
from funcs import optimized_find, update_cache
from threading import Thread


class pset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="pset", with_app_command=True)
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def ping(self, ctx,*, prime_set=None):
        start = time.time()
        if prime_set is None:
            error = discord.Embed(
                description="Be sure to provide a prime name"
            )
            await ctx.send(embed=error)
            return
        elif 'forma' in prime_set.lower():
            error = discord.Embed(
                description="Why would you search forma"
            )
            await ctx.send(embed=error)
            return
        
        download_start = time.time()
        # metadata = get('https://wf.snekw.com/void-wiki/meta').json()
        
        # check if we have data cached
        cached = True
        if cache.cache.exists("void:1"):
            cached_void = json.loads(cache.cache.get("void:1"))
            data = cached_void
        else:
            cached = False
            update_cache("void:1",cache)
            cached_void = json.loads(cache.cache.get("void:1"))
            data = cached_void

        primes = data['PrimeData']
        item_name = prime_set.lower()
        text = ''
        item = ''
        prime_dict = None
        # get the prime dict
        for prime in primes:
            if "Prime" not in prime:
                continue
            prime_name = prime.lower()
            if item_name in prime_name:
                prime_dict = primes[prime]
                item = prime
        
        if not prime_dict:
            error = discord.Embed(
                description="Did not find any primes with that name"
            )
            await ctx.send(embed=error)
            return
        
        # download the stuff
        threads = {}
        returns = {}
        for part in prime_dict["Parts"]:
            trade_name = f"{item} {part if len(part.split(' ')) == 1 else part.replace('blueprint','').strip()}"
            threads[part] = Thread(target=optimized_find, args=(trade_name, returns, part))
            threads[part].start()
            # text += f"{part}: {find(trade_name)}{chr(10)}"
        
        # download set price on separate thread
        # now we join 1 by 1
        for part in prime_dict["Parts"]:
            threads[part].join()
            text += f"{part}: {returns[part]}{chr(10)}"

        set_name = f"{item} set"
        set_thread = Thread(target=optimized_find, args=(set_name, returns, 'set'))
        set_thread.start()
        set_thread.join()
        set_price = returns['set']
        if "Failed" in set_price: # try again without set suffix
            set_thread = Thread(target=optimized_find, args=(item, returns, 'set'))
            set_thread.start()
            set_thread.join()
            set_price = returns['set']

        set_price = f"Full set: {set_price}"
    
        download_timer = time.time() - download_start
        
        set_embed = discord.Embed(
            description=set_price+"\n\n"+text,
            title=item
        )
        if cached:
            set_embed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Cached Latency: {round(download_timer*1000)}ms{chr(10)}"
            )
        else:
            set_embed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}"
            )  
        
        await ctx.send(embed=set_embed)



async def setup(bot):
    await bot.add_cog(pset(bot))
