import discord
import json
import time
import asyncio
from discord.ext import commands
from redis_manager import cache
from models.wfm import PriceCheck

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
        
        primes = json.loads(cache.get("void:1"))['PrimeData']
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
        returns = {}
        tasks = []
        for part in prime_dict["Parts"]:
            trade_name = f"{item} {part if len(part.split(' ')) == 1 else part.replace('blueprint','').strip()}"
            price_checker = PriceCheck(item=trade_name)
            task = asyncio.create_task(self.fetch_price(price_checker, part, returns))
            tasks.append(task)
        
        await asyncio.gather(*tasks)

        for part in prime_dict["Parts"]:
            text += f"{part}: {returns[part]}\n"

        set_name = f"{item} set"
        set_price_checker = PriceCheck(item=set_name)
        await self.fetch_price(set_price_checker, 'set', returns)
        
        set_price = returns['set']
        if "Failed" in set_price or "N/A" in set_price:  # try again without set suffix
            set_price_checker = PriceCheck(item=item)
            await self.fetch_price(set_price_checker, 'set', returns)
            set_price = returns['set']

        set_price = f"Full set: {set_price}"
    
        download_timer = time.time() - download_start
        
        set_embed = discord.Embed(
            description=set_price+"\n\n"+text,
            title=item
        )

        set_embed.set_footer(
            text=f"Total Latency: {round((time.time() - start)*1000)}ms\nDownload Latency: {round(download_timer*1000)}ms\n"
        )  
        
        await ctx.send(embed=set_embed)

    async def fetch_price(self, price_checker: PriceCheck, part_key: str, returns_dict: dict):
        """Helper method to fetch price for a part and store it in the returns dictionary"""
        try:
            result = await price_checker.check_async()
            returns_dict[part_key] = result
        except Exception as e:
            returns_dict[part_key] = f"(error)"


async def setup(bot):
    await bot.add_cog(pset(bot))
