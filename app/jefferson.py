import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='-', intents=intents)

async def load():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            await bot.load_extension(f'commands.{file[:-3]}') 

@bot.tree.command(name="sync")
async def func(interaction: discord.Interaction):
    if interaction.user.id == "336563297648246785":
        await bot.tree.sync()


@bot.event
async def on_ready():
    bot.remove_command('help')
    await load()
    await bot.tree.sync()


bot.run(token)
