import sqlite3
from discord.ext import commands
import discord

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_user_profile(self, user_id):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT level, xp, power_remaining, max_power, power_regeneration FROM users WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        print(f"Fetched profile data: {profile}")  # Debug: Check the fetched profile data
        if profile is None:
            profile = (1, 0, 100, 100, 1.00)  # Default profile if not found
        level, xp, power_remaining, max_power, power_regeneration = profile
        
        cursor.execute('SELECT ore_name, amount FROM ores WHERE user_id = ?', (user_id,))
        ores = cursor.fetchall()
        ores_dict = dict(ores)
        
        conn.close()
        return {
            'level': level,
            'xp': xp,
            'power_remaining': power_remaining,
            'max_power': max_power,
            'power_regeneration': power_regeneration,
            'ores': ores_dict
        }

    def get_progress_bar(self, current, max_val, length=20):
        progress = int((current / max_val) * length)
        return '█' * progress + '░' * (length - progress)

    def get_xp_for_level(self, level):
        return 100 + 20 * (level - 1)

    @commands.command(name='profile')
    async def profile(self, ctx, member: discord.Member = None):
        user = member or ctx.author
        user_id = user.id
        profile = self.get_user_profile(user_id)
        
        print(f"Profile fetched for {user_id}: {profile}")  # Debug: Confirm profile fetch

        ores_list = '\n'.join(f'{ore}: {amount}' for ore, amount in profile['ores'].items())

        # Calculate XP needed for current and next level
        xp_needed = self.get_xp_for_level(profile['level'])
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

    @profile.error
    async def profile_error(self, ctx, error):
        if isinstance(error, commands.MemberNotFound):
            await ctx.send("Member not found. Please make sure to mention a valid user.")


# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(ProfileCog(bot))
