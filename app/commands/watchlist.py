from logging import getLogger
from discord.ext import commands
import discord
import json
from requests import get
import time
from database import Session, Watchlists

logger = getLogger(__name__)

watchlist_events = {
    "darvo": "darvo:<item-on-sale>:<price*>",
    "fissure": "fissure:<relic-tier>:<mission-type>",
    "arbitration": "arbitration:<mission-type>",
    "market": "market:<item-name>:<price>",
}


class watchlist(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(name="watchlist", invoke_without_command=True, aliases=["wl","watch"])
    async def watchlist(self, ctx: commands.Context):
        embed = discord.Embed(
            color=discord.Color.random(),
            title="Watchlist",
            description="Subcommands: \n" +\
                        "- add\n" +\
                        "- remove\n" +\
                        "- edit\n" +\
                        "- get\n"
            )
        
        await ctx.send(embed=embed)

    @watchlist.command(name="add")
    async def add(self, ctx: commands.Context, *, params: str = None):
        if not params:
            help_embed = discord.Embed(
                title="Watchlist add",
                color=discord.Color.random(),
                description="The proper command format is as following:\n"+\
                            "`watchlist add <event>:<target>:<option>`\n\n"+\
                            "**Events**:\n"+\
                            "*Fields marked with \* are optional*"
            )
            for event, cmd in watchlist_events.items():
                help_embed.add_field(name=event, value=cmd, inline=False)
            return await ctx.send(embed=help_embed)

        try:
            data = json.loads(params)
        except json.JSONDecodeError:
            return await ctx.send("Invalid JSON format. Please provide proper data.")

        # Get user data from database
        user = Session.get(Watchlists, str(ctx.author.id))

        # Check if user exists and has an existing watchlist
        if user and user.watch_list:
            user.watch_list.append(data)
        else:
            # Create new user entry if it doesn't exist
            user_data = Watchlists(user_id=str(ctx.author.id), watch_list=[data])
            Session.add(user_data)

        Session.commit()

        await ctx.send("Entry added to your watchlist.")

    @watchlist.command(name="remove")
    async def remove(self, ctx: commands.Context, index: int|str = None):
        if index is None:
            await ctx.send("Please specify the index of the entry you want to remove.")
            return
        
        if str(index).lower() == "all":
            confirmation = await ctx.send("Are you sure you want to remove all entries from your watchlist? (y/n)")
            response = await self.bot.wait_for("message", check=lambda m: m.author.id == ctx.author.id and m.channel == ctx.channel)
            if response.content.lower() != "y":
                await ctx.send("Removal cancelled.")
                return
            
            try:
                user = Session.get(Watchlists, str(ctx.author.id))
                if not user:
                    await ctx.send("Your watchlist is already empty.")
                    return

                user.watch_list = []
                Session.commit()

                await ctx.send("All entries removed from your watchlist.")
            except Exception as e:
                # Handle potential database errors gracefully
                await ctx.send("An error occurred while removing entries. Please try again later.")
                logger.error(e)
            return


        try:
            user = Session.get(Watchlists, str(ctx.author.id))
            if not user or not user.watch_list:
                return await ctx.send("Your watchlist is empty.")

            if len(user.watch_list) < index or index < 0:
                return await ctx.send("Invalid index. Please enter a valid index within your watchlist.")

            item = user.watch_list.pop(index)
            Session.commit()

            await ctx.send(f"Removed the following entry:\n{item}")
        except Exception as e:
            # Handle potential database errors gracefully
            await ctx.send("An error occurred while removing the entry. Please try again later.")
            logger.error(e)

    @watchlist.command(name="edit")
    async def edit(self, ctx: commands.Context, index: int = None, *, new_data: str = None):
        if all([index is None, new_data is None]):
            return await ctx.send("Please specify the index of the entry you want to edit and the new data.")

        if index is None:
            return await ctx.send("Please specify the index of the entry you want to edit.")

        if new_data is None:
            return await ctx.send("Please provide the new data you want to edit.")

        try:
            user = Session.get(Watchlists, str(ctx.author.id))
            if not user or not user.watch_list:
                return await ctx.send("Your watchlist is empty or the index is invalid.")

            if len(user.watch_list) < index or index < 0:
                return await ctx.send("Invalid index. Please enter a valid index within your watchlist.")

            try:
                new_data_dict = json.loads(new_data)
            except json.JSONDecodeError:
                return await ctx.send("Invalid JSON format for new data. Please provide proper data.")

            for key, value in new_data_dict.items():
                user.watch_list[index][key] = value

            Session.commit()

            await ctx.send(f"Entry at index {index} edited successfully!")
        except Exception as e:
            # Handle potential database errors gracefully
            await ctx.send("An error occurred while editing the entry. Please try again later.")
            logger.error(e)

    @watchlist.command(name="get")
    async def get(self, ctx: commands.Context):
        user = Session.get(Watchlists, str(ctx.author.id))
        if not user or not user.watch_list:
            return await ctx.send("Your watchlist is currently empty.")

        # Construct embed for displaying watchlist
        embed = discord.Embed(
            color=discord.Color.random(),
            title=f"{ctx.author.name}'s Watchlist",
            description="",
        )

        for i, entry in enumerate(user.watch_list):
            # Format entry data for embed description
            formatted_entry = f"{i+1}. {entry}"  # Example formatting

            # Add formatted entry to embed description
            embed.description += formatted_entry + "\n"

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(watchlist(bot))