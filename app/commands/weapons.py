from discord.ext import commands
import discord
import json
from requests import get
from funcs import dispo
import time

class weapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='weapon', description="Find the stats of certain weapon",aliases=['wep','weap'])
    async def weapon(self, ctx, *,message:str = None):
        """
        Usage: !weapon <weapon-name>\n
        Find the stats of certain weapon
        """
        start = time.time()
        if message is None:
            error = discord.Embed(description="Usage: !weapon <weapon-name>")
            await ctx.send(embed=error)
            return
        res = get(f"https://api.warframestat.us/weapons/{message}")
        data = json.loads(res.text)

        if(res.status_code == 404):
            error = discord.Embed(description="Be sure to write the right weapon name")
            await ctx.send(embed=error)
            return

        res = get('https://wf.snekw.com/weapons-wiki')
        try:
            snekw = json.loads(res.text)['data'][data['name']]

            description  = ''
            if snekw['Slot'] != 'Melee':
                description +=(f"Class: {snekw['Slot']}{chr(10)}"+
                f"Type: {snekw['Class']}{chr(10)}"+
                f"Mastery: {snekw['Mastery']}{chr(10)}"+
                f"Ammo: {snekw['MaxAmmo'] if 'MaxAmmo' in snekw else '∞'}{chr(10)}"+
                f"Magazine: {snekw['Magazine']}{chr(10)}"+
                f"Reload: {snekw['Reload']}{chr(10)}"+
                f"Trigger: {snekw['Trigger']}{chr(10)}"
                # f"{'**Zoom**:'+{chr(10)}+ chr(10).join([str(zoom_option) for zoom_option in snekw['Zoom']]) if 'Zoom' in snekw else ''}{chr(10)}"
                )

                if 'Zoom' in snekw:
                    description += '**Zoom**:\n'
                    description += '\n'.join([str(zoom_option) for zoom_option in snekw['Zoom']])
                    description += '\n'
                
                description +=f"Disposition: {snekw['Disposition']}  ({dispo(float(snekw['Disposition']))}){chr(10)}{chr(10)}"

            else:
                description +=(f"Class: {snekw['Slot']}{chr(10)}"+
                f"Type: {snekw['Class']}{chr(10)}"+
                f"Mastery: {snekw['Mastery']}{chr(10)}"+
                f"Attack Speed: {snekw['Attacks'][0]['FireRate']}{chr(10)}"+
                f"Combo Duration: {snekw['ComboDur']}{chr(10)}"+
                f"Range: {snekw['MeleeRange']}{chr(10)}"+
                f"Disposition: {snekw['Disposition']}  ({dispo(float(snekw['Disposition']))}){chr(10)}{chr(10)}"
                )
            wepembed = discord.Embed(
                title=data['name'],
                description=description,
                url=data['wikiaUrl'],
                color=discord.Colour.random())
            

            for x in snekw['Attacks']:
                total = 0
                max = ''
                percentmax = 0
                damagestring = ''
                damage = x['Damage']
                for type in damage:
                    damagestring += f"{type.capitalize()}: {damage[type]}{chr(10)}"
                    total += damage[type]
                    if damage[type] >= percentmax:
                        percentmax = damage[type]
                        max = type.capitalize()
                
            
                if snekw['Slot'] != 'Melee':
                    wepembed.add_field(
                        name=f"***Attack Mode***: {x['AttackName'] if 'AttackName' in x else 'Normal Attack' }{chr(10)}"+
                        f"Type: {x['ShotType'] if 'ShotType' in x else '-'}",
                        value=f"{'Critical Chance: '+str(round(x['CritChance']*100))+'%'+chr(10) if 'CritChance' in x else ''}"+
                        f"{'Critical Damage: '+ str(x['CritMultiplier'])+'x'+chr(10) if 'CritMultiplier' in x else ''}"+
                        f"{'Status Chance: '+ str(round(x['StatusChance']*100))+'%'+chr(10) if 'StatusChance' in x else '' }"+
                        f"Multishot: {x['Multishot'] if 'Multishot' in x else '1'}{chr(10)}"+
                        f"{'Charge Time: '+ str(x['FireRate'])+'s'+chr(10) if 'ShotType' in x and x['ShotType'] == 'Charged Shot' else 'Firerate: '+str(x['FireRate'])+chr(10) if 'FireRate' in x else ''}"+
                        f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else '' }"+
                        f"{'Falloff: '+(str(round(x['Falloff']['Reduction'] * 100))+'%' if 'Reduction'in x['Falloff'] else '')+'('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m)'+chr(10) if 'Falloff' in x else ''}"+
                        f"{'Punchthrough: '+str(x['PunchThrough'])+chr(10) if 'PunchThrough' in x else ''}"+
                        f"**Damage**:{chr(10)}"+
                        damagestring + chr(10)+
                        f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x['Multishot'],percentmax*100/total,max)}",
                        inline=True
                    )
                else:
                    wepembed.add_field(
                        name=f"***Attack Mode***: {x['AttackName'] if 'AttackName' in x else 'Normal Attack' }{chr(10)}"+
                        f"{'Type: '+x['ShotType'] if 'ShotType' in x else ''}",
                        value=f"{'Critical Chance: '+str(round(x['CritChance']*100))+'%'+chr(10) if 'CritChance' in x else ''}"+
                        f"{'Critical Damage: '+ str(x['CritMultiplier'])+'x'+chr(10) if 'CritMultiplier' in x else ''}"+
                        f"{'Status Chance: '+ str(round(x['StatusChance']*100))+'%'+chr(10) if 'StatusChance' in x else '' }"+
                        multishot(x) +
                        # f"{ '' if 'Multishot' not in x else 'Multishot: '+str(x['Multishot'])+chr(10)}"+
                        # f"{'Charge Time: '+ x['ChargeTime']+'{chr(10)}' if 'ChargeTime' in x and 'AttackName' not in x else 'Firerate: '+x['FireRate']+'{chr(10)}' if 'FireRate' in x else ''}"+
                        f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else '' }"+
                        f"{'Falloff: '+str(round(x['Falloff']['Reduction']) * 100)+'%('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else ''}"+
                        # f"{'Punchthrough: '+x['PunchThrough']+'{chr(10)}' if 'PunchThrough' in x else ''}"+
                        f"**Damage**:{chr(10)}"+
                        damagestring + chr(10)+
                        f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * (x['Multishot'] if 'Multishot' in x else 1),percentmax*100/total,max)}",
                        inline=True
                    )

            if 'wikiaThumbnail' in snekw:
                wepembed.set_thumbnail(url=data['wikiaThumbnail'])
            wepembed.set_footer(
                text=f"Latency: {round((time.time() - start)*1000)}ms"
            )

            await ctx.send(embed=wepembed)
        except:
            await ctx.send('Something went wrong!')

async def setup(bot):
    await bot.add_cog(weapon(bot))

def multishot(x):
    if 'Multishot' in x:
        return f"Multishot: {x['Multishot']}{chr(10)}"
    else:
        return ''
