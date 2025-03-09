from discord.ext import commands
import discord
import json
from requests import get
from funcs import dispo, update_cache
from models.weapon import Weapon
import time
from redis_manager import cache

class weapon(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    async def get_weapon(self, ctx: commands.Context, message:str):
        start = time.time()
        if message is None:
            error = discord.Embed(description="Usage: !weapon <weapon-name>")
            await ctx.send(embed=error)
            return
        download_start = time.time()

        # check if we have data cached
        cached = True
        if cache.cache.exists("weapon:1"):
            cached_weapons = json.loads(cache.cache.get("weapon:1"))
            data = cached_weapons
        else:
            cached = False
            update_cache("weapon:1",cache)
            cached_weapons = json.loads(cache.cache.get("weapon:1"))
            data = cached_weapons

        download_timer = time.time() - download_start

        # first we test if we have weapon on wiki
        message = message.lower()
        wiki_wep = ""
        # test with full text first
        for x in data:
            if message == x.lower():
                wiki_wep = x
                break
            
        # if not full word then partial    
        if wiki_wep == "":
            for x in data:
                if message in x.lower():
                    wiki_wep = x
                    break

        if len(wiki_wep) == 0:
            error = discord.Embed(description="Be sure to write the right weapon name")
            await ctx.send(embed=error)
            return
        
        weapon_instance = Weapon.from_dict(wiki_wep, data[wiki_wep])

        calculaton_start = time.time()

        wepembed = discord.Embed(
            title=weapon_instance.name,
            description=weapon_instance.get_description(),
            url=f"https://wiki.warframe.com/w/{'_'.join(weapon_instance.name.split(' '))}",
            color=discord.Colour.random())

        for attack in weapon_instance.attacks:
            wepembed.add_field(name=attack.title, value=str(attack), inline=True)

        calculaton_timer = time.time() - calculaton_start
        if cached:
            wepembed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Cached Latency: {round(download_timer*1000)}ms{chr(10)}Calculation Latency: {round(calculaton_timer*1000)}ms"
            )
        else:
            wepembed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}Calculation Latency: {round(calculaton_timer*1000)}ms"
            )    
        await ctx.send(embed=wepembed)


    @commands.command(name='wep', description="Find the stats of certain weapon",aliases=['w','weap',"weapon"])
    async def weapon_alt(self, ctx, *,message:str = None):
        """
        Usage: -weapon <weapon-name>\n
        Find the stats of certain weapon
        """
        await self.get_weapon(ctx, message)

    async def autocomplete(self, interaction: discord.Interaction, current: str) -> list[discord.app_commands.Choice[str]]:
        if cache.cache.exists("weapon:1"):
            cached_weapons = json.loads(cache.cache.get("weapon:1"))
            data = cached_weapons
        else:
            update_cache("weapon:1",cache)
            cached_weapons = json.loads(cache.cache.get("weapon:1"))
            data = cached_weapons

        return [discord.app_commands.Choice(name=weapon, value=weapon) for weapon in data.keys() if current.lower() in weapon.lower()][:24]


    @discord.app_commands.command(name='weapon', description="Find the stats of certain weapon")
    @discord.app_commands.autocomplete(weapon=autocomplete)
    async def weapon_slash(self, interaction: discord.Interaction, weapon:str = None):
        """
        Usage: /weapon <weapon-name>\n
        Find the stats of certain weapon
        """
        ctx = await self.bot.get_context(interaction)
        await self.get_weapon(ctx, weapon)



async def setup(bot):
    await bot.add_cog(weapon(bot))


def multishot(x):
    if 'Multishot' in x:
        return f"Multishot: {x['Multishot']}{chr(10)}"
    else:
        return ''
