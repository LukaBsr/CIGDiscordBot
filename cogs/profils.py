import sqlite3
from discord.ext import commands
import discord

class ProfileCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_user_profile(self, user_id):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        
        # Get user profile
        cursor.execute('SELECT level, xp, power_remaining FROM users WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        print(f"Fetched profile data: {profile}")
        if profile is None:
            profile = (1, 0, 0)  # Default profile if not found
        level, xp, power_remaining = profile
        
        # Get ores
        cursor.execute('SELECT ore_name, amount FROM ores WHERE user_id = ?', (user_id,))
        ores = cursor.fetchall()
        ores_dict = dict(ores)
        
        conn.close()
        return {
            'level': level,
            'xp': xp,
            'power_remaining': power_remaining,
            'ores': ores_dict
        }

    def get_progress_bar(self, current, max_val, length=20):
        progress = int((current / max_val) * length)
        return '█' * progress + '░' * (length - progress)

    @commands.command(name='profile')
    async def profile(self, ctx):
        user_id = ctx.author.id
        profile = self.get_user_profile(user_id)
        
        print(f"Profile fetched for {user_id}: {profile}")  # Debug: Confirm profile fetch

        ores_list = '\n'.join(f'{ore}: {amount}' for ore, amount in profile['ores'].items())
        xp_progress = self.get_progress_bar(profile["xp"] % 100, 100)  # Assuming 100 XP needed per level

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Profile",
            color=discord.Color.purple()
        )
        embed.set_thumbnail(url=ctx.author.display_avatar.url)
        embed.set_footer(text="RPG Bot - Profile Command", icon_url=ctx.bot.user.display_avatar.url)
        embed.timestamp = ctx.message.created_at

        embed.add_field(name='Level', value=profile['level'], inline=True)
        embed.add_field(name='Power Remaining', value=profile['power_remaining'], inline=True)
        embed.add_field(name='XP', value=f'{profile["xp"]} XP', inline=True)
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
