from discord.ext import commands
import discord
import json
from requests import get
from funcs import dispo
import time
from redis_manager import cache

class weapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(name='weapon', description="Find the stats of certain weapon",aliases=['wep','weap'])
    # async def weapon(self, ctx, *,message:str = None):
    #     """
    #     Usage: !weapon <weapon-name>\n
    #     Find the stats of certain weapon
    #     """
    #     start = time.time()
    #     if message is None:
    #         error = discord.Embed(description="Usage: !weapon <weapon-name>")
    #         await ctx.send(embed=error)
    #         return
    #     download_start = time.time()
    #     res = get(f"https://api.warframestat.us/weapons/{message}")
    #     data = json.loads(res.text)
    #     wiki_res = get('https://wf.snekw.com/weapons-wiki')
    #     download_timer = time.time() - download_start

    #     snekw = ""
    #     if res.status_code == 404:
    #         # first we test if we have weapon on wiki
    #         data = json.loads(wiki_res.text)['data']
    #         message = message.lower()
    #         wiki_wep = ""
    #         for x in data:
    #             if message in x.lower():
    #                 wiki_wep = x
    #                 break

    #         if len(wiki_wep) == 0:
    #             error = discord.Embed(description="Be sure to write the right weapon name")
    #             await ctx.send(embed=error)
    #             return
    #         snekw = data[wiki_wep]
    #     else:

    #         try:
    #             snekw = json.loads(wiki_res.text)['data'][data['name']]
    #         except KeyError:
    #             await ctx.send('Something went wrong!')
    #             return

    #     calculaton_start = time.time()
    #     if len(snekw) == 0:
    #         error = discord.Embed(description="Be sure to write the right weapon name")
    #         await ctx.send(embed=error)
    #         return
    #     description = ''
    #     if snekw['Slot'] != 'Melee':
    #         description +=(f"Class: {snekw['Slot']}{chr(10)}"+
    #                         f"Type: {snekw['Class']}{chr(10)}"+
    #                         f"Mastery: {snekw['Mastery']}{chr(10)}"+
    #                         f"Ammo: {snekw['AmmoMax'] if 'AmmoMax' in snekw else '∞'}{chr(10)}"+
    #                         f"Ammo Pickup: {snekw['AmmoPickup'] if 'AmmoPickup' in snekw else ''}{chr(10) if 'AmmoPickup' in snekw else ''}" +
    #                         f"Magazine: {snekw['Magazine']}{chr(10)}"+
    #                         f"Reload: {snekw['Reload']}{chr(10)}"+
    #                         f"Trigger: {snekw['Trigger']}{chr(10)}"
    #                         # f"{'**Zoom**:'+{chr(10)}+ chr(10).join([str(zoom_option) for zoom_option in snekw['Zoom']]) if 'Zoom' in snekw else ''}{chr(10)}"
    #                         )

    #         if 'Zoom' in snekw:
    #             description += '**Zoom**:\n'
    #             description += '\n'.join([str(zoom_option) for zoom_option in snekw['Zoom']])
    #             description += '\n'

    #         description +=f"Disposition: {snekw['Disposition']}  ({dispo(float(snekw['Disposition']))}){chr(10)}{chr(10)}"
    #     else:
    #         description +=(f"Class: {snekw['Slot']}{chr(10)}"+
    #         f"Type: {snekw['Class']}{chr(10)}"+
    #         f"Mastery: {snekw['Mastery']}{chr(10)}"+
    #         f"Attack Speed: {snekw['Attacks'][0]['FireRate']}{chr(10)}"+
    #         f"Combo Duration: {snekw['ComboDur']}{chr(10)}"+
    #         f"Range: {snekw['MeleeRange']}{chr(10)}"+
    #         f"Disposition: {snekw['Disposition']}  ({dispo(float(snekw['Disposition']))}){chr(10)}{chr(10)}"
    #         )

    #     if 'wikiaUrl' not in data:
    #         wepembed = discord.Embed(
    #             title=snekw['Name'],
    #             description=description,
    #             url=f"https://warframe.fandom.com/wiki/{'_'.join(snekw['Name'].split(' '))}",
    #             color=discord.Colour.random())
    #     else:
    #         wepembed = discord.Embed(
    #             title=data['name'],
    #             description=description,
    #             url=data['wikiaUrl'],
    #             color=discord.Colour.random())

    #     for x in snekw['Attacks']:
    #         total = 0
    #         max = ''
    #         percentmax = 0
    #         damagestring = ''
    #         damage = x['Damage']
    #         for type in damage:
    #             damagestring += f"{type.capitalize()}: {damage[type]}{chr(10)}"
    #             total += damage[type]
    #             if damage[type] >= percentmax:
    #                 percentmax = damage[type]
    #                 max = type.capitalize()


    #         if snekw['Slot'] != 'Melee':
    #             wepembed.add_field(
    #                 name=f"***Attack Mode***: {x['AttackName'] if 'AttackName' in x else 'Normal Attack' }{chr(10)}"+
    #                 f"Type: {x['ShotType'] if 'ShotType' in x else '-'}",
    #                 value=f"{'Critical Chance: '+str(round(x['CritChance']*100))+'%'+chr(10) if 'CritChance' in x else ''}"+
    #                 f"{'Critical Damage: '+ str(x['CritMultiplier'])+'x'+chr(10) if 'CritMultiplier' in x else ''}"+
    #                 f"{'Status Chance: '+ str(round(x['StatusChance']*100))+'%'+chr(10) if 'StatusChance' in x else '' }"+
    #                 f"Multishot: {x['Multishot'] if 'Multishot' in x else '1'}{chr(10)}"+
    #                 f"{'Charge Time: '+ str(x['FireRate'])+'s'+chr(10) if 'ShotType' in x and x['ShotType'] == 'Charged Shot' else 'Firerate: '+str(x['FireRate'])+chr(10) if 'FireRate' in x else ''}"+
    #                 f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else '' }"+
    #                 f"{'Falloff: '+(str(round(x['Falloff']['Reduction'] * 100))+'%' if 'Reduction'in x['Falloff'] else '')+'('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m)'+chr(10) if 'Falloff' in x else ''}"+
    #                 f"{'Punchthrough: '+str(x['PunchThrough'])+chr(10) if 'PunchThrough' in x else ''}"+
    #                 f"**Damage**:{chr(10)}"+
    #                 damagestring + chr(10)+
    #                 f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x.get('Multishot',1),percentmax*100/total,max)}",
    #                 inline=True
    #             )
    #         else:
    #             wepembed.add_field(
    #                 name=f"***Attack Mode***: {x['AttackName'] if 'AttackName' in x else 'Normal Attack' }{chr(10)}"+
    #                 f"{'Type: '+x['ShotType'] if 'ShotType' in x else ''}",
    #                 value=f"{'Critical Chance: '+str(round(x['CritChance']*100))+'%'+chr(10) if 'CritChance' in x else ''}"+
    #                 f"{'Critical Damage: '+ str(x['CritMultiplier'])+'x'+chr(10) if 'CritMultiplier' in x else ''}"+
    #                 f"{'Status Chance: '+ str(round(x['StatusChance']*100))+'%'+chr(10) if 'StatusChance' in x else '' }"+
    #                 multishot(x) +
    #                 # f"{ '' if 'Multishot' not in x else 'Multishot: '+str(x['Multishot'])+chr(10)}"+
    #                 # f"{'Charge Time: '+ x['ChargeTime']+'{chr(10)}' if 'ChargeTime' in x and 'AttackName' not in x else 'Firerate: '+x['FireRate']+'{chr(10)}' if 'FireRate' in x else ''}"+
    #                 f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else '' }"+
    #                 f"{'Falloff: '+str(round(x['Falloff']['Reduction']) * 100)+'%('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else ''}"+
    #                 # f"{'Punchthrough: '+x['PunchThrough']+'{chr(10)}' if 'PunchThrough' in x else ''}"+
    #                 f"**Damage**:{chr(10)}"+
    #                 damagestring + chr(10)+
    #                 f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x.get('Multishot',1),percentmax*100/total,max)}",
    #                 inline=True
    #             )
    #     calculaton_timer = time.time() - calculaton_start
    #     if 'wikiaThumbnail' in data:
    #         wepembed.set_thumbnail(url=data['wikiaThumbnail'])
    #     wepembed.set_footer(
    #         text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}Calculation Latency: {round(calculaton_timer*1000)}ms"
    #     )

    #     await ctx.send(embed=wepembed)

    @commands.command(name='wep', description="Find the stats of certain weapon",aliases=['w','wep','weap',"weapon"])
    async def weapon_alt(self, ctx, *,message:str = None):
        """
        Usage: !weapon <weapon-name>\n
        Find the stats of certain weapon
        """
        start = time.time()
        if message is None:
            error = discord.Embed(description="Usage: !weapon <weapon-name>")
            await ctx.send(embed=error)
            return
        download_start = time.time()
        # metadata = get('https://wf.snekw.com/weapons-wiki/meta').json()

        cached = True
        # check if we have data cached
        if cache.cache.exists("weapon:1"):
            cached_weapons = json.loads(cache.cache.get("weapon:1"))
            data = cached_weapons
        else:
            cached = False # recreate it later
            wiki_res = get('https://wf.snekw.com/weapons-wiki')
            data = json.loads(wiki_res.text)

        download_timer = time.time() - download_start

        wiki_data = data['data']
        snekw = ""
        # first we test if we have weapon on wiki
        message = message.lower()
        wiki_wep = ""
        # test with full text first
        for x in wiki_data:
            if message == x.lower():
                wiki_wep = x
                break
            
        # if not full word then partial    
        if wiki_wep == "":
            for x in wiki_data:
                if message in x.lower():
                    wiki_wep = x
                    break

        if len(wiki_wep) == 0:
            error = discord.Embed(description="Be sure to write the right weapon name")
            await ctx.send(embed=error)
            return
        snekw = wiki_data[wiki_wep]

        calculaton_start = time.time()
        if len(snekw) == 0:
            error = discord.Embed(description="Be sure to write the right weapon name")
            await ctx.send(embed=error)
            return
        description = ''
        if snekw['Slot'] != 'Melee':
            description +=(f"Class: {snekw['Slot']}{chr(10)}"+
                            f"Type: {snekw['Class']}{chr(10)}"+
                            f"Mastery: {snekw['Mastery']}{chr(10)}"+
                            f"Ammo: {snekw['AmmoMax'] if 'AmmoMax' in snekw else '∞'}{chr(10)}"+
                            f"Ammo Pickup: {snekw['AmmoPickup'] if 'AmmoPickup' in snekw else ''}{chr(10) if 'AmmoPickup' in snekw else ''}" +
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
            title=snekw['Name'],
            description=description,
            url=f"https://warframe.fandom.com/wiki/{'_'.join(snekw['Name'].split(' '))}",
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
                    f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else '' }"+
                    f"{'Falloff: '+(str(round(x['Falloff']['Reduction'] * 100))+'%' if 'Reduction'in x['Falloff'] else '')+'('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m)'+chr(10) if 'Falloff' in x else ''}"+
                    f"{'Punchthrough: '+str(x['PunchThrough'])+chr(10) if 'PunchThrough' in x else ''}"+
                    f"**Damage**:{chr(10)}"+
                    damagestring + chr(10)+
                    f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x.get('Multishot',1),percentmax*100/total,max)}",
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
                    f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else '' }"+
                    f"{'Falloff: '+str(round(x['Falloff']['Reduction']) * 100)+'%('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else ''}"+
                    # f"{'Punchthrough: '+x['PunchThrough']+'{chr(10)}' if 'PunchThrough' in x else ''}"+
                    f"**Damage**:{chr(10)}"+
                    damagestring + chr(10)+
                    f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x.get('Multishot',1),percentmax*100/total,max)}",
                    inline=True
                )
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
        
        # # readd the data to redis
        # if not cached:
        #     text = json.dumps(data)
        #     cache.cache.set("weapon:1",text)


    @discord.app_commands.command(name='weapon', description="Find the stats of certain weapon")
    async def weapon_slash(self, interaction: discord.Interaction, message:str = None):
        """
        Usage: !weapon <weapon-name>\n
        Find the stats of certain weapon
        """
        start = time.time()
        if message is None:
            error = discord.Embed(description="Usage: !weapon <weapon-name>")
            await interaction.response.send_message(embed=error)
            return
        download_start = time.time()
        # metadata = get('https://wf.snekw.com/weapons-wiki/meta').json()

        cached = True
        # check if we have data cached
        if cache.cache.exists("weapon:1"):
            cached_weapons = json.loads(cache.cache.get("weapon:1"))
            data = cached_weapons
        else:
            cached = False # recreate it later
            wiki_res = get('https://wf.snekw.com/weapons-wiki')
            data = json.loads(wiki_res.text)

        download_timer = time.time() - download_start

        wiki_data = data['data']
        snekw = ""
        # first we test if we have weapon on wiki
        message = message.lower()
        wiki_wep = ""
        # test with full text first
        for x in wiki_data:
            if message == x.lower():
                wiki_wep = x
                break
            
        # if not full word then partial    
        if wiki_wep == "":
            for x in wiki_data:
                if message in x.lower():
                    wiki_wep = x
                    break

        if len(wiki_wep) == 0:
            error = discord.Embed(description="Be sure to write the right weapon name")
            await interaction.response.send_message(embed=error)
            return
        snekw = wiki_data[wiki_wep]

        calculaton_start = time.time()
        if len(snekw) == 0:
            error = discord.Embed(description="Be sure to write the right weapon name")
            await interaction.response.send_message(embed=error)
            return
        description = ''
        if snekw['Slot'] != 'Melee':
            description +=(f"Class: {snekw['Slot']}{chr(10)}"+
                            f"Type: {snekw['Class']}{chr(10)}"+
                            f"Mastery: {snekw['Mastery']}{chr(10)}"+
                            f"Ammo: {snekw['AmmoMax'] if 'AmmoMax' in snekw else '∞'}{chr(10)}"+
                            f"Ammo Pickup: {snekw['AmmoPickup'] if 'AmmoPickup' in snekw else ''}{chr(10) if 'AmmoPickup' in snekw else ''}" +
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
            title=snekw['Name'],
            description=description,
            url=f"https://warframe.fandom.com/wiki/{'_'.join(snekw['Name'].split(' '))}",
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
                    f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else '' }"+
                    f"{'Falloff: '+(str(round(x['Falloff']['Reduction'] * 100))+'%' if 'Reduction'in x['Falloff'] else '')+'('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m)'+chr(10) if 'Falloff' in x else ''}"+
                    f"{'Punchthrough: '+str(x['PunchThrough'])+chr(10) if 'PunchThrough' in x else ''}"+
                    f"**Damage**:{chr(10)}"+
                    damagestring + chr(10)+
                    f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x.get('Multishot',1),percentmax*100/total,max)}",
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
                    f"{'AoE Radius: '+str(x['Radius'])+'m'+chr(10) if 'Radius' in x and 'ShotType' in x and x['ShotType'] == 'AoE' else 'AoE Radius: '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else '' }"+
                    f"{'Falloff: '+str(round(x['Falloff']['Reduction']) * 100)+'%('+str(x['Falloff']['StartRange'])+' - '+str(x['Falloff']['EndRange'])+'m'+chr(10) if 'Falloff' in x else ''}"+
                    # f"{'Punchthrough: '+x['PunchThrough']+'{chr(10)}' if 'PunchThrough' in x else ''}"+
                    f"**Damage**:{chr(10)}"+
                    damagestring + chr(10)+
                    f"{'Total: '+'{0:.2f} ({1:.2f}%{2})'.format(total * x.get('Multishot',1),percentmax*100/total,max)}",
                    inline=True
                )
        calculaton_timer = time.time() - calculaton_start
        if cached:
            wepembed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Cached Latency: {round(download_timer*1000)}ms{chr(10)}Calculation Latency: {round(calculaton_timer*1000)}ms"
            )
        else:
            wepembed.set_footer(
                text=f"Total Latency: {round((time.time() - start)*1000)}ms{chr(10)}Download Latency: {round(download_timer*1000)}ms{chr(10)}Calculation Latency: {round(calculaton_timer*1000)}ms"
            )    
        await interaction.response.send_message(embed=wepembed)
        



async def setup(bot):
    await bot.add_cog(weapon(bot))


def multishot(x):
    if 'Multishot' in x:
        return f"Multishot: {x['Multishot']}{chr(10)}"
    else:
        return ''
