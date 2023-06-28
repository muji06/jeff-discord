import discord
from discord.ext import commands
from discord import app_commands
import discord
import json
import requests
from redis_manager import cache

MAPPINGS = {
    "Ostrons":("plains", "poe", "cetus", "ostron", "earth"),
    "Solaris United":("venus", "fortuna", "4tuna", "solaris", "vallis"),
    "Entrati":("deimos", "necralisk", "cambion", "entrati"),
}



# class PersistentView(discord.ui.View):
#     def __init__(self, embed: discord.Embed):
#         super().__init__(timeout=None)
#         self.embed = embed 

#     def edit_embed(self, new_embed):
#         self.embed = new_embed
        
#     @discord.ui.button(label='Previous', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
#     async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.edit_message(embed=self.embed)

#     @discord.ui.button(label='Next', style=discord.ButtonStyle.green, custom_id='persistent_view:red')
#     async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
#         await interaction.response.edit_message(embed=self.embed)



class bounty(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="bounty", with_app_command=True)
    async def bounty(self, ctx: commands.Context, place = None):
        if not place:
            err_embed = discord.Embed(
                    description="Specify the bounty place (e.g. -bounty cetus)"
                )
            await ctx.send(embed=err_embed)
            return
        syndicate = list(filter(lambda x: f"{place}" in MAPPINGS[x], MAPPINGS ))
        print(f"{syndicate=}")
        if not syndicate:
            err_embed = discord.Embed(
                    description="Be sure to type the correct planet/syndicate/node"
                )
            await ctx.send(embed=err_embed)
            return

        response = requests.get("https://api.warframestat.us/PC/syndicateMissions/?language=en")
        data = json.loads(response.text)
        
        # filter the bounty data
        bounties = list(filter(lambda x : x["syndicate"] == syndicate[0], data))
        if not bounties:
            print(f"{bounties=}")
            
            err_embed = discord.Embed(
                    description="Something went wrong. Try again later."
                )
            await ctx.send(embed=err_embed)
            return
        embed = discord.Embed(
            title=f"{bounties[0]['syndicate']} Bounties"
        )
        for job in bounties[0]['jobs']:
            embed.add_field(
                name=f"[{'-'.join([f'{x}' for x in job['enemyLevels']])}]{job['type']}",
                value="- "+"\n- ".join(job["rewardPool"]))
        
        embed.set_footer(
            text=f"Rotation ends in {bounties[0]['eta']}"
        )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(bounty(bot))



    # 'rewardPool': ['3X 1,500 Credits Cache',
    #  '150 Endo',
    #  '15X Pustulite',
    #  '2X 3,000 Credits Cache',
    #  '250 Endo',
    #  'Aya',
    #  'Scintillant'],
    # 'type': 'Anomaly Retrieval',
    # 'enemyLevels': [5, 15],