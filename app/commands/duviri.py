# from discord.ext import commands
# from discord import app_commands
# import discord
# import json
# import requests

# CYCLES = [
#     # name       kullervo?      POI
#     ("Sorrow"   ,True       ,["Archarbor", "Kullervo's Hold"]   ),
#     ("Fear"     ,True       ,["Amphitheater", "Kullervo's Hold"]),
#     ("Joy"      ,False      ,["Archarbor", "Amphitheater"]      ),
#     ("Anger"    ,True       ,["Amphitheater", "Kullervo's Hold"]),
#     ("Envy"     ,False      ,["Archarbor", "Amphitheater"]      ),
# ]

# url = "https://api.warframestat.us/pc/duviriCycle/"


# class duviri(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

#     @commands.hybrid_command(name="duviri", with_app_command=True)
#     # @app_commands.guilds(discord.Object(id=992897664087760979))
#     async def duviri(self, ctx: commands.Context):
#         response = requests.get("https://api.warframestat.us/PC/dailyDeals?language=en")
#         data = json.loads(response.text)[0]
#         set_embed = discord.Embed(
#             description=f"## {data['item']}\n### {data['total']-data['sold']}/{data['total']} left\nPrice: ~~{data['originalPrice']}~~ {data['salePrice']}<:Platinum:992917150358589550> ({data['discount']}% off)",
#             title="Darvo's Daily Deal"
#         )
#         set_embed.set_footer(text=f"Ends in {data['eta']}")
        
#         await ctx.send(embed=set_embed)


# async def setup(bot):
#     await bot.add_cog(duviri(bot))


# from datetime import datetime

# target_timestamp = datetime.strptime(expire, "%Y-%m-%dT%H:%M:%S.%fZ")

# response = requests.get("https://timezone.abstractapi.com/v1/current_time/?api_key=23368da787414c17b1e67f510447f287&location=London, England")

# current_timestamp = datetime.strptime(response.json()["datetime"], "%Y-%m-%d %H:%M:%S")
# time_left = current_timestamp - target_timestamp

# hours, remainder = divmod(time_left.seconds, 3600)
# minutes, seconds = divmod(remainder, 60)

# timing = ""

# if hours:
#     timing += f"{hours} hour "
# if minutes > 1:
#     timing += f"{minutes} minutes "
# elif minutes:
#     timing += f"{minutes} minute "
# if seconds > 1:
#     timing += f"{seconds} seconds "
# elif seconds:
#     timing += f"{seconds} second"


# print(f"{timing}")