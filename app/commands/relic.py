from discord.ext import commands
from discord import app_commands
import discord
import json
from requests import get
import time
from funcs import optimized_find, relic_finder
from threading import Thread

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
            price = relic_finder(relic) or "-"
            if 'IsBaro' in relic and relic['IsBaro']:
                info = '(B)'
            elif 'Valuted' in relic and relic['Valuted']:
                info = '(V)'
            
            embed = discord.Embed(
                title=f"{info} {relic}{chr(10)}",
                color=discord.Colour.random(),
                description=f"{price}\nAlso showing the 3 lowest warframe.market prices."
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
            threads = {}
            returns = {}
            for x in range(6):
                returns[f'{x}'] = None
                name = drop[x]['Item'] + ' ' + drop[x]['Part']
                threads[x] = Thread(target=optimized_find, args=(name, returns, f'{x}'))
                threads[x].start()
                
            for x in range(6):
                threads[x].join()
            
            embed.add_field(
                name="Common/Bronze",
                value=f"{drop[0]['Item']} {drop[0]['Part']} {returns['0']}{chr(10)}"\
                        +f"{drop[1]['Item']} {drop[1]['Part']} {returns['1']}{chr(10)}"\
                        +f"{drop[2]['Item']} {drop[2]['Part']} {returns['2']}"
            ,inline=False)
            embed.add_field(
                name="Uncommon/Silver",
                value=f"{drop[3]['Item']} {drop[3]['Part']} {returns['3']}{chr(10)}"\
                        +f"{drop[4]['Item']} {drop[4]['Part']} {returns['4']}"
            ,inline=False)
            embed.add_field(
                name="Rare/Gold",
                value=f"{drop[5]['Item']} {drop[5]['Part']} {returns['5']}"
            ,inline=False)
        

      
            embed.set_footer(
                    text=f"Latency: {round((time.time() - start)*1000)}ms"
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(relic(bot))