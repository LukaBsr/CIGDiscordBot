import sqlite3
import asyncio
from discord.ext import commands, tasks

class PowerRegenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.regen_task.start()  # Start the task when the cog is loaded

    def get_user_power_regeneration(self, user_id):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT power_remaining, max_power, power_regeneration FROM users WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        conn.close()
        if profile is None:
            return None
        return profile

    @tasks.loop(minutes=1)
    async def regen_task(self):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_id, power_regeneration FROM users')
        users = cursor.fetchall()
        for user_id, power_regeneration in users:
            power_data = self.get_user_power_regeneration(user_id)
            if power_data is None:
                continue
            power_remaining, max_power, _ = power_data
            new_power_remaining = min(max_power, power_remaining + power_regeneration)
            if new_power_remaining != power_remaining:
                cursor.execute('UPDATE users SET power_remaining = ? WHERE user_id = ?', (new_power_remaining, user_id))
                conn.commit()
        conn.close()

    @commands.command(name='power')
    async def power(self, ctx):
        user_id = ctx.author.id
        profile = self.get_user_power_regeneration(user_id)
        if profile is None:
            await ctx.send("Profile not found.")
            return
        
        power_remaining, max_power, power_regeneration = profile
        power_regeneration = f"{power_regeneration:.2f}"

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Power Status",
            color=discord.Color.blue()
        )
        embed.add_field(name='Power', value=f'{power_remaining}/{max_power} [{power_regeneration}/m]', inline=True)
        await ctx.send(embed=embed)

    @commands.command(name='setpower')
    @commands.has_role('dev bot')
    async def setpower(self, ctx, power: int):
        user_id = ctx.author.id
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET power_remaining = ? WHERE user_id = ?', (power, user_id))
        conn.commit()
        conn.close()
        await ctx.send(f'Your power has been set to {power}.')

    @commands.command(name='setpowerregen')
    @commands.has_role('dev bot')
    async def setpowerregen(self, ctx, regen: float):
        user_id = ctx.author.id
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET power_regeneration = ? WHERE user_id = ?', (regen, user_id))
        conn.commit()
        conn.close()
        await ctx.send(f'Your power regeneration rate has been set to {regen}.')

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(PowerRegenCog(bot))
