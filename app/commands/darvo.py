from discord.ext import commands
from discord import app_commands
import discord
import json
import requests
from redis_manager import cache

class darvo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="darvo", with_app_command=True)
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def darvo(self, ctx: commands.Context):
        response = requests.get("https://api.warframestat.us/PC/dailyDeals?language=en")
        data = json.loads(response.text)[0]
        set_embed = discord.Embed(
            description=f"## {data['item']}\n### {data['total']-data['sold']}/{data['total']} left\nPrice: ~~{data['originalPrice']}~~ {data['salePrice']}<:Platinum:992917150358589550> ({data['discount']}% off)",
            title="Darvo's Daily Deal"
        )
        set_embed.set_footer(text=f"Ends in {data['eta']}")
        
        await ctx.send(embed=set_embed)


async def setup(bot):
    await bot.add_cog(darvo(bot))
