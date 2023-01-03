from discord.ext import commands
from discord import app_commands
import discord
import json
from requests import get

class prime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name='prime', with_app_command=True, description="Find what relics drop certain part.")
    @app_commands.guilds(discord.Object(id=992897664087760979))
    async def sortie(self, ctx,* ,part:str = None):
        """
        Usage: !prime <prime-part-name>\n
        
        Find what relics drop certain part.
        """
        if part is None:
            error = discord.Embed(
                description="Be sure to provide a prime part name"
            )
            await ctx.send(embed=error)
            return
        elif 'forma' in part:
            error = discord.Embed(
                description="Forma is not implemented for now"
            )
            await ctx.send(embed=error)
            return
        
        res = get(f'https://api.warframestat.us/drops/search/{part}')
        print(f'https://api.warframestat.us/drops/search/{part}')
        data = json.loads(res.text)
        if len(data) == 0:
            error = discord.Embed(
                description="Be sure to type the correct prime part"
            )
            await ctx.send(embed=error)
            return

        res = get('https://wf.snekw.com/void-wiki')
        relic = json.loads(res.text)['data']['RelicData']
        count = 0
        text = ''
        item = ''
        
        for x in data:
            if str(x['place']).endswith('Relic'):
                if count == 0:
                    item = x['item']
                
                if len(item) != 0 and item == x['item']:
                    rel = ' '.join(x['place'].split(' ')[:-1])
                    r = relic[rel]
                    info = ''
                    if 'IsBaro' in r and r['IsBaro']:
                        info = '(B)'
                    elif 'Vaulted' in r:
                        info = '(V)'
                    
                    text += f"{info} {x['place']} - {x['rarity']}{chr(10)}"
                    count += 1
                
        if count == 0:
            error = discord.Embed(
                description="No relic drop found!"
            )
            await ctx.send(embed=error)
            return
        
        else:
            prime_part = discord.Embed(
                description=text,
                title=item
            )
            await ctx.send(embed=prime_part)


async def setup(bot):
    await bot.add_cog(prime(bot), guild= discord.Object(id=992897664087760979))