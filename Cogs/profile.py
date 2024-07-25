import discord
# Cogs/profile.py
from discord.ext import commands
import logging
from Database.db_utils import get_user_profile
from Cogs.utils import get_xp_for_level

logger = logging.getLogger(__name__)

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_progress_bar(self, current, max_val, length=20):
        progress = int((current / max_val) * length)
        return '█' * progress + '░' * (length - progress)

    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        user = member or ctx.author
        user_id = user.id
        
        profile = await get_user_profile(user_id)
        logger.info(f"Profile fetched for {user_id}: {profile}")  # Info log for profile fetch

        ores_list = '\n'.join(f'{ore}: {amount}' for ore, amount in profile['ores'].items())

        # Calculate XP needed for current and next level
        xp_needed = get_xp_for_level(profile['level'])
        current_xp = profile["xp"]
        xp_progress = self.get_progress_bar(current_xp, xp_needed)

        # Format power regeneration to two decimal places
        power_regeneration = f"{profile['power_regeneration']:.2f}"

        embed = discord.Embed(
            title=f"{user.display_name}'s Profile",
            color=discord.Color.purple()  # Changed color for a more lively look
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(text="RPG Bot - Profile Command", icon_url=ctx.bot.user.display_avatar.url)
        embed.timestamp = ctx.message.created_at

        embed.add_field(name='Level', value=profile['level'], inline=True)
        embed.add_field(name='Power', value=f'{profile["power_remaining"]:.0f}/{profile["max_power"]} [{power_regeneration}/m]', inline=True)
        embed.add_field(name='XP', value=f'{current_xp}/{xp_needed} XP', inline=True)
        embed.add_field(name='XP Progress', value=f'[{xp_progress}]', inline=True)

        if ores_list:
            embed.add_field(name='Ores', value=ores_list, inline=False)
        else:
            embed.add_field(name='Ores', value='No ores collected', inline=False)

        # Placeholder for tools - Update this part when you add tools
        embed.add_field(name='Tools', value='No tools available yet.', inline=False)

        await ctx.send(embed=embed)


# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(ProfileCog(bot))
