import os
import logging
import discord

from discord.ext import commands
from dotenv import load_dotenv
from database import  init_db

logger = logging.getLogger(__name__)

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

async def load():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            await bot.load_extension(f'commands.{file[:-3]}') 

    logger.info("Loading database")
    init_db() 


@bot.tree.command(name="sync")
async def func(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.id == 336563297648246785:
        try:
            await bot.tree.sync()
            await interaction.followup.send("Done.", ephemeral=True)
        except: 
            await interaction.followup.send("Something went wrong!", ephemeral=True)
    else:
        file = discord.File("silicate.jpg")
        logging.info(f"Sync command used by {interaction.user}")
        await interaction.followup.send("blehhhh",file=file, ephemeral=True)

@bot.event
async def on_ready():
    bot.remove_command('help')
    await load()
    # await bot.tree.sync()


bot.run(token, root_logger=True)
