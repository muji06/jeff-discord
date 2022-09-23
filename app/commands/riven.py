from discord.ext import commands
import discord
import json
from requests import get
import time

class riven(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='riven', description="Shows the matching riven prices.",aliases=['riv','r'])
    async def riven(self, ctx,*, weapon:str = None):
        """
        Usage: !riven <weapon-name>\n
        Shows the matching riven prices
        """
        start = time.time()
        if weapon is None:
            error = discord.Embed(
                description="Please provide a weapon name."
            )
            await ctx.send(embed=error)
        
        weapon = weapon.capitalize()
        try:
            response = get("https://n9e5v4d8.ssl.hwcdn.net/repos/weeklyRivensPC.json")
            rivens = json.loads(response.text)

            name = ''
            emb_title = ''
            emb_description = ''

            for riven in rivens:
                if riven['compatibility'] is None: 
                    continue
                if weapon in riven['compatibility'] and riven['rerolled'] == False:
                    name = riven['compatibility']
                    emb_title = riven['compatibility']
                    emb_description = f"Median price unrolled {riven['median']}<:Platinum:992917150358589550>"
                    break


            riven_embed = discord.Embed(
                title=emb_title,
                description=emb_description)

            if len(name) != 0:

                name = '_'.join(name.lower().split(' '))
                res_market = get(f"https://api.warframe.market/v1/auctions/search?type=riven&weapon_url_name={name}&sort_by=price_asc")
                market = json.loads(res_market.text)['payload']['auctions']
                counter = 0
                for x in market:
                    if counter == 3:
                        break

                    if x['owner']['status'] != 'offline':
                        attributes = ""
                        for att in x['item']['attributes']:
                            sign = ''
                            symbol = '%'
                            bonus = ' '.join(att['url_name'].split('_')).capitalize()
                            if 'positive' in att:
                                sign = '+'
                            
                            if 'range' in att['url_name']:
                                symbol = 'm'
                            elif 'combo_duration' in att['url_name']:
                                symbol = 's'
                            elif 'punch' in att['url_name']:
                                symbol = ''

                            attributes +=f"{sign}{att['value']}{symbol} {bonus}\n"

                        counter += 1
                        
                        riven_embed.add_field(
                            name=f"{x['owner']['ingame_name']}: {x['item']['weapon_url_name'].capitalize()} {x['item']['name'].capitalize()} {x['buyout_price']}<:Platinum:992917150358589550>",
                            value=attributes,
                            inline=False
                        )
            
                riven_embed.set_footer(
                    text=f"Latency: {round((time.time() - start)*1000)}ms"
                    )
                await ctx.send(embed=riven_embed)
            else:
                error = discord.Embed(
                    description="Riven not found, make sure to type the correct name."
                )
        except:
            await ctx.send("Something went wrong.")

async def setup(bot):
    await bot.add_cog(riven(bot))