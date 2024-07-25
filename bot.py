# bot.py
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import logging
import asyncio

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('discord')  # Use 'discord' to capture logs from discord.py

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Adjust based on your bot’s needs

bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')
    logger.info('Bot is ready.')

# List of cogs to load
initial_extensions = [
    'Cogs.profile',
    'Cogs.admin',
    'Cogs.power_regen'
]

async def load_cogs():
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            logger.info(f'Loaded extension: {extension}')
        except Exception as e:
            logger.error(f'Failed to load extension {extension}.', exc_info=e)

if __name__ == '__main__':
    asyncio.run(load_cogs())
    bot.run(TOKEN)
