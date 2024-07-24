import logging
from discord.ext import commands

logger = logging.getLogger(__name__)

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send('Hello!')

    @commands.command(name='info')
    async def info(self, ctx):
        await ctx.send('This is an RPG bot!')

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(ExampleCog(bot))
