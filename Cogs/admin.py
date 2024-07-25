# Cogs/admin.py
import discord
from discord.ext import commands
import logging
from Cogs.utils import level_up

logger = logging.getLogger(__name__)

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='addxp')
    @commands.has_permissions(administrator=True)  # Only allow admins to use this command
    async def add_xp(self, ctx, xp_amount: int, member: discord.Member = None):
        try:
            member = member or ctx.author
            user_id = member.id

            # Log the request
            logger.info(f"Adding {xp_amount} XP to user {user_id}")

            # Update XP and level using the level_up function
            level, new_xp = await level_up(user_id, xp_amount)

            # Send confirmation message
            await ctx.send(f"Added {xp_amount} XP to {member.display_name}. New XP: {new_xp}. Current Level: {level}")
        except Exception as e:
            logger.error(f"Error adding XP: {e}")
            await ctx.send(f"Failed to add XP due to an error: {e}")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
