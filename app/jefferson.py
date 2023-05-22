import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

t = os.getenv('TOKEN')

i = discord.Intents.default()
i.message_content = True
bot = commands.Bot(command_prefix='-', intents=i)

async def load():
    for f in os.listdir('./comms'):
        if f.endswith('.py'):
            await bot.load_extension(f'comms.{f[:-3]}') 

@bot.tree.command(name="sync")
async def func(interaction: discord.Interaction):
    if interaction.user.id == "336563297648246785":
        await bot.tree.sync()


@bot.event
async def on_ready():
    bot.remove_command('help')
    await load()
    await bot.tree.sync()


bot.run(t)
