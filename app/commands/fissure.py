from discord.ext import commands
import discord
import json
from requests import get

class fissure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fissure', description="Show the current Fissures",aliases=['fis','fiss','f'])
    async def sortie(self, ctx,type:str = None):
        """
        Usage: !fissure <type> \n
        Default language is en (english)\n
        """
        if type == 'sp':
            f_type = 'Steel Path'
        elif type == 'rj':
            f_type = 'Railjack'
        else:
            f_type = ''

        response = get(f"https://api.warframestat.us/pc/fissures?language=en")
        data = json.loads(response.text)

        embed = discord.Embed(
            title=f"{f_type} Fissures",
            color=discord.Colour.random()
            )

        if f_type == '':
            for x in data:
                if not x['isStorm'] and not x['isHard']:

                    embed.add_field(name=f"{x['tier']} - {x['missionType']} - {x['enemy']}",
                    value=f"{x['node']}{chr(10)}{x['eta']}",
                    inline=False)

        elif f_type == 'Steel Path':
            for x in data:
                if x['isHard']:

                    embed.add_field(name=f"{x['tier']} - {x['missionType']} - {x['enemy']}",
                    value=f"{x['node']}{chr(10)}{x['eta']}",
                    inline=False)

        elif f_type == 'Railjack':
            for x in data:
                if x['isStorm']:

                    embed.add_field(name=f"{x['tier']} - {x['missionType']} - {x['enemy']}",
                    value=f"{x['node']}{chr(10)}{x['eta']}",
                    inline=False)    

        embed.set_footer(text=f"Ends in {data['eta']}\nValid fissure types are: rj (Railjack), sp (Steel Path), <empty> (Normal)")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(fissure(bot))