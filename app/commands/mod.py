from discord.ext import commands
from discord import app_commands
import discord
import json
from requests import get
from funcs import find,polarity
import time

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='mod', with_app_command=True, description="Shows the closest matching mod")
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def mod(self, ctx,*, mod:str = None):
        """
        Usage: !mod <mod-name>\n
        Shows the closest matching mod and its market price
        """
        start = time.time()
        if mod is None:
            error = discord.Embed(
                description="Please provide a mod."
            )
            await ctx.send(embed=error)
            return

        download_start = time.time()
        response = get(f"https://api.warframestat.us/mods/{mod}")
        download_timer = time.time() - download_start
        data = json.loads(response.text)

        if 'code' in data and data['code'] == 404:
            error = discord.Embed(
                description="Be sure to tyoe the correct mod name"
            )
            await ctx.send(embed=error)
            return
        else:
            download_start = time.time()

            res_snekw = get('https://wf.snekw.com/mods-wiki')
            download_timer += time.time() - download_start
            snekw = json.loads(res_snekw.text)['data']['Mods']
            snekw_mod = None
            for x in snekw:
                # print(f"{data['name']} vs {snekw[x]['Name']}")
                if data['name'].lower() == snekw[x]['Name'].lower():
                    # print('Found mod!!!!!!!!!!!!!!!!!!!!!')
                    snekw_mod = snekw[x]
                    break

            if snekw_mod is None:
                await ctx.send("Internal Error!")
                return

            price_ranked = ''
            price_unranked = ''
            market_start = time.time()
            if snekw_mod['Tradable']:
                price_ranked = await find(snekw_mod['Name'],snekw_mod['MaxRank'])
                price_unranked = await find(snekw_mod['Name'],0)
            market_timer = time.time() - market_start

            if 'wikiaThumbnail' in data:
                

                embed = discord.Embed(
                    color=discord.Colour.random(),

                    description=f"{('**Unranked: **'+price_unranked+chr(10)+'**Maxed: **'+price_ranked) if snekw_mod['Tradable'] else ''}",
                )
                embed.set_image(url=data['wikiaThumbnail'])
                embed.set_footer(
                    text=f"{'Transmutable' if 'Transmutable' in snekw_mod else 'Not transmutable'}"+"\n"+f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}Market Price Latency: {round(market_timer*1000)}ms"
                )
                await ctx.send(embed=embed)

            else:
                pol = ''
                if 'Polarity' in snekw_mod:
                    pol = polarity(snekw_mod['Polarity'])
                
                embed = discord.Embed(
                    color=discord.Colour.random(),
                    title=f"{snekw_mod['Name']}{pol} ({data['rarity']}){chr(10)}{snekw_mod['Type']} Mod",
                    description=(f"Drain cost: {snekw_mod['BaseDrain']} - {snekw_mod['BaseDrain'] + snekw_mod['MaxRank']} (Ranks 0 - {snekw_mod['MaxRank']})"
                    +'\n\n'+f"**Effect at rank {snekw_mod['MaxRank']}:**"+'\n'+snekw_mod['Description']
                    +'\n\n'+f"{('**Unranked: **'+str(price_unranked)+chr(10)+'**Maxed: **'+str(price_ranked)) if snekw_mod['Transmutable'] else ''}")
                )
                embed.set_footer(
                    text=f"{'Transmutable' if 'Transmutable' in snekw else 'Not transmutable'}"+"\n"+f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}Market Price Latency: {round(market_timer*1000)}ms"
                )
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(mod(bot))