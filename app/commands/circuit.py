import discord

from datetime import datetime, timedelta
from discord.ext import commands

from redis_manager import cache
from funcs import FIRST_WEEK, ROTATIONS

from requests import get
from math import floor

class circuit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='circuit', description="List the current rotation of incarnon genesis", aliases=['circus','incarnon'])
    async def circuit(self, ctx):

        # time reference
        response = get("https://timezone.abstractapi.com/v1/current_time/?api_key=23368da787414c17b1e67f510447f287&location=Paris, France")

        current_timestamp = datetime.strptime(response.json()["datetime"], "%Y-%m-%d %H:%M:%S")

        if cache.cache.exists("circuit:1"):
            current_rotation = cache.cache.get("circuit:1").decode("utf-8")
        else:
            week1_timestamp = datetime.fromtimestamp(FIRST_WEEK)
            weeks_passed = (current_timestamp - week1_timestamp).days // 7
            index = weeks_passed % len(ROTATIONS) # get index
            current_rotation = ",".join(ROTATIONS[index])

        weapons = str(current_rotation).split(",")
        
        text = "**Weapons**:\n"
        for weapon in weapons:
            text += f"- {weapon}\n"

        days, hours, minutes, seconds = calculate_time_remaining(current_timestamp)


        embed = discord.Embed(
            title="Current Circuit Rotation for incarnon genesis",
            description=f"{text}",
            color=discord.Colour.random()
            )

        embed.set_footer(text=f"Rotation ends in:{days}d, {hours}h, {minutes}m, {seconds}s\n")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(circuit(bot))

def calculate_time_remaining(current_time: datetime):
    # get first week time
    week1_timestamp = datetime.fromtimestamp(FIRST_WEEK)
    # check how much time passed
    time_passed = current_time - week1_timestamp
    # get the number of weeks
    weeks_passed = time_passed.days//7
    # get the timestamp for next reset
    next_reset = week1_timestamp + timedelta(weeks=weeks_passed + 1)

    time_remaining = next_reset - current_time

    # now parse it into different periods
    days = time_remaining.days
    hours, remainder = divmod(time_remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return days, hours, minutes, seconds
