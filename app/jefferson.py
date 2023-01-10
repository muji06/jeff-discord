
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
    await bot.tree.sync(guild= discord.Object(id=992897664087760979))

async def load():
    for file in os.listdir('./commands'):
        if file.endswith('.py'):
            await bot.load_extension(f'commands.{file[:-3]}') # remove the .py
            bot.loop.create_task(startup())


@bot.event
async def on_ready():
    await load()
    print("Jefferson ready")


bot.run(token)
