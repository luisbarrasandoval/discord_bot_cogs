from discord.ext import commands
from dotenv import load_dotenv
import discord
import os


PREFIX = '!'
DESCRIPTION = 'A bot for the Discord server.'


initial_extensions = [
    "cogs.GitHub",
    'cogs.Poll',
]


bot = commands.Bot(command_prefix=PREFIX, description=DESCRIPTION)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')


if __name__ == '__main__':
    load_dotenv()
    API_KEY = os.getenv("TOKEN")

    for extension in initial_extensions:
        bot.load_extension(extension)

    bot.run(API_KEY)
