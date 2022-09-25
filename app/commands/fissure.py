from discord.ext import commands
import discord
import json
from requests import get
import time

class fissure(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='fissure', description="Show the current Fissures",aliases=['fis','fiss','f'])
    async def sortie(self, ctx,type:str = None):
        """
        Usage: !fissure <type> \n
        Default language is en (english)\n
        """
        start = time.time()
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

        fissure_list = []

        if f_type == '':
            for x in data:
                if not x['isStorm'] and not x['isHard']:
                    fissure_list.append((x['tierNum'],f"{x['tier']} - {x['missionType']} - {x['enemy']}", f"{x['node']}{chr(10)}Ends in {x['eta']}"))

        elif f_type == 'Steel Path':
            for x in data:
                if x['isHard']:
                    fissure_list.append((x['tierNum'],f"{x['tier']} - {x['missionType']} - {x['enemy']}", f"{x['node']}{chr(10)}Ends in {x['eta']}"))


        elif f_type == 'Railjack':
            for x in data:
                if x['isStorm']:
                    fissure_list.append((x['tierNum'],f"{x['tier']} - {x['missionType']} - {x['enemy']}", f"{x['node']}{chr(10)}Ends in {x['eta']}"))
    
        fissures_sorted = sorted(fissure_list, key=lambda x: x[0])
        
        for fissure in fissure_list:
            embed.add_field(
                name=fissure[1],
                value=fissure[2],
                inline=False
            )

        embed.set_footer(text=f"Valid fissure types are: rj (Railjack), sp (Steel Path), <empty> (Normal)"+"\n"+f"Latency: {round((time.time() - start)*1000)}ms")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(fissure(bot))