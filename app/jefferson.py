import logging as log
import discord
from discord.ext import commands
from discord import app_commands
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

async def startup():
    await bot.wait_until_ready()
    # await tree.sync() # guild=discord.Object(id=992897664087760979)
    log.info("Ready to sync!")

async def load():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            await bot.load_extension(f'commands.{file[:-3]}') # remove the .py
            # bot.loop.create_task(startup())

# need this to sync all
@bot.tree.command(name="sync",description="Owner only")
async def sync(interaction: discord.Interaction):
    if interaction.user.id == "336563297648246785":
        await bot.tree.sync()
        await interaction.response.send_message("Command tree synced.", ephemeral=True)
    else:
        await interaction.response.send_message("Must be owner to use!", ephemeral=True)

@bot.event
async def on_ready():
    # Due to an unfortunate error ,we have to clear all commands in here
    log.info("Deleting locally")
    bot.tree.clear_commands(guild=discord.Object(id=992897664087760979))
    bot.tree.add_command(sync, guild=discord.Object(id=992897664087760979))
    await bot.tree.sync(guild=discord.Object(id=992897664087760979))
    log.info("Done with local deletion")

    await load()
    print("Jefferson ready")


bot.run(token)
