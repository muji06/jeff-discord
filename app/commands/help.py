from discord.ext import commands
import discord

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help',  with_app_command=True, description="Lists all commands")
    # @app_commands.guilds(discord.Object(id=992897664087760979))
    async def help(self, ctx, lang:str = None):
        """
        Usage: !sortie <language>\n
        Defualt language is en (english)\n
        Show the current Sortie Rotation
        """

        cog_desc = ""+\
        "**-alert**: Shows currently running alerts\n\n"+\
        "**-arbitration**: Shows currently running arbitration\n\n"+\
        "**-arcane** <arcane-name>: Shows arcane stats and market price\n\n"+\
        "**-archon** (optional)<language>: Shows current archon rotation\n\n"+\
        "**-baro** : Show current baro status and his inventory\n\n"+\
        "**-bounty** <location>: Shows currently running bounties in a specific planet\n\n"+\
        "**-circuit**: List the current rotation of incarnon genesis\n\n"+\
        "**-darvo**: Shows current Darvo sale\n\n"+\
        "**-duviri**: Show the current Duviri mood as well as the points of interest for that mood\n\n"+\
        "**-fissure** (optional)<rj|sp>: Shows the current fissures\n\n"+\
        "**-mod** <mod-name>: Shows the mod stats and market price\n\n"+\
        "**-nightwave**: Shows current nightwave quests\n\n"+\
        "**-prime** <prime-part>: Finds market price and what drops it\n\n"+\
        "**-pset** <prime-name>: Finds market prices for all parts\n\n"+\
        "**-relic** <relic-name>: Lists all parts dropping from a relic and their market prices\n\n"+\
        "**-riven** <weapon-name>: Shows matching riven prices\n\n"+\
        "**-sortie** (optional)<language>: Shows daily sortie\n\n"+\
        "**-weapon** <weapon-name>: Shows weapon stats\n\n"
        embed = discord.Embed(
            title="Commands",
            description=cog_desc
        ) 

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))