from discord.ext import commands
from discord import app_commands
import discord
import json
from requests import get
import time
from funcs import find

class relic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='relic', with_app_command=True, description="Find what parts your relic drops")
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def baro(self, ctx, *,relic:str = None):
        """
        Usage: !relic\n
        Find what parts your relic drops
        """
        if relic is None:
            error = discord.Embed(
                description=f"Please provide a relic to check."
            )
            await ctx.send(embed=error)
            return

        start = time.time()
        relic = relic.title()

        res = get('https://wf.snekw.com/void-wiki')
        data = json.loads(res.text)['data']['RelicData']
        if relic not in data:
            error = discord.Embed(
                description="This relic doesn't exist! \nCheck if you typed it correctly."
            )
            await ctx.send(embed=error)
        else:
            drop = data[relic]['Drops']

            info = ''
            price = ''#await relic_finder(relic)
            if 'IsBaro' in relic and relic['IsBaro']:
                info = '(B)'
            elif 'Valuted' in relic and relic['Valuted']:
                info = '(V)'
            
            embed = discord.Embed(
                title=f"{info} {relic}{chr(10)}{price}",
                color=discord.Colour.random(),
                description=f"Also showing the 3 lowest warframe.market prices."
            )
            # print(f"Bronze:")
            # print(f"{drop[0]['Item']} {drop[0]['Part']}")
            # print(f"{drop[1]['Item']} {drop[1]['Part']}")
            # print(f"{drop[2]['Item']} {drop[2]['Part']}")
            # print(f"Silver:")
            # print(f"{drop[3]['Item']} {drop[3]['Part']}")
            # print(f"{drop[4]['Item']} {drop[4]['Part']}")
            # print(f"Gold")
            # print(f"{drop[5]['Item']} {drop[5]['Part']}")

            embed.add_field(
                name="Common/Bronze",
                value=f"{drop[0]['Item']} {drop[0]['Part']} {await find(drop[0]['Item'] + ' ' + drop[0]['Part'])}{chr(10)}"\
                        +f"{drop[1]['Item']} {drop[1]['Part']} {await find(drop[1]['Item'] + ' ' + drop[1]['Part'])}{chr(10)}"\
                        +f"{drop[2]['Item']} {drop[2]['Part']} {await find(drop[2]['Item'] + ' ' + drop[2]['Part'])}"
            ,inline=False)
            embed.add_field(
                name="Uncommon/Silver",
                value=f"{drop[3]['Item']} {drop[3]['Part']} {await find(drop[3]['Item'] + ' ' + drop[3]['Part'])}{chr(10)}"\
                        +f"{drop[4]['Item']} {drop[4]['Part']} {await find(drop[4]['Item'] + ' ' + drop[4]['Part'])}"
            ,inline=False)
            embed.add_field(
                name="Rare/Gold",
                value=f"{drop[5]['Item']} {drop[5]['Part']} {await find(drop[5]['Item'] + ' ' + drop[5]['Part'])}"
            ,inline=False)
        

      
            embed.set_footer(
                    text=f"Latency: {round((time.time() - start)*1000)}ms"
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(relic(bot))