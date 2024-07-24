import discord
import logging
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)  # Adjust the logging level as needed
logger = logging.getLogger(__name__)

# Set command prefix and create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Load cogs from the 'cogs' directory
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user.name}')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            cog = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog}')
                logger.info(f'Loaded {filename}')
            except Exception as e:
                logger.error(f'Failed to load extension {filename}: {e}')

# Error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        logger.error(f'Command "{ctx.invoked_with}" not found. Message: {ctx.message.content}')
        await ctx.send(f'Command "{ctx.invoked_with}" not found.')
    else:
        logger.error(f'An error occurred: {error}. Message: {ctx.message.content}')
        await ctx.send(f'An error occurred: {error}')

# Run the bot with the token
bot.run(TOKEN)
