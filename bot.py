import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set command prefix and create bot instance
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Load cogs from the 'cogs' directory
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog}')
                print(f'Loaded {filename}')
            except Exception as e:
                print(f'Failed to load extension {filename}.', e)

# Run the bot with the token
bot.run(TOKEN)
