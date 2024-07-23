import sqlite3
from discord.ext import commands
import discord

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_user_profile(self, user_id):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        
        # Get user profile
        cursor.execute('SELECT level, xp, power_remaining FROM users WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
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

    @commands.command(name='profile')
    async def profile(self, ctx):
        user_id = ctx.author.id
        profile = self.get_user_profile(user_id)

        ores_list = ', '.join(f'{ore}: {amount}' for ore, amount in profile['ores'].items())

        embed = discord.Embed(title=f"{ctx.author.display_name}'s Profile", color=discord.Color.blue())
        embed.add_field(name='Level', value=profile['level'], inline=False)
        embed.add_field(name='XP', value=f'{profile["xp"]} XP', inline=False)
        embed.add_field(name='Power Remaining', value=profile['power_remaining'], inline=False)
        embed.add_field(name='Ores', value=ores_list if ores_list else 'No ores collected', inline=False)

        await ctx.send(embed=embed)

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Profile(bot))
