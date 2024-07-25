# Cogs/power_regen.py
import discord
from discord.ext import commands, tasks
import aiosqlite
import logging

logger = logging.getLogger(__name__)

class PowerRegenCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_user_power_regeneration(self, user_id):
        async with aiosqlite.connect('rpg_bot.db') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT power_remaining, max_power, power_regeneration FROM users WHERE user_id = ?', (user_id,))
                profile = await cursor.fetchone()
        if profile is None:
            return None
        return profile

    @tasks.loop(minutes=1)
    async def regen_task(self):
        async with aiosqlite.connect('rpg_bot.db') as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT user_id, power_regeneration FROM users')
                users = await cursor.fetchall()
                for user_id, power_regeneration in users:
                    power_data = await self.get_user_power_regeneration(user_id)
                    if power_data is None:
                        continue
                    power_remaining, max_power, _ = power_data
                    new_power_remaining = min(max_power, power_remaining + power_regeneration)
                    if new_power_remaining != power_remaining:
                        await cursor.execute('UPDATE users SET power_remaining = ? WHERE user_id = ?', (new_power_remaining, user_id))
                        await conn.commit()

    @commands.command(name='power')
    async def power(self, ctx):
        user_id = ctx.author.id
        profile = await self.get_user_power_regeneration(user_id)
        if profile is None:
            await ctx.send("Profile not found.")
            return
        
        power_remaining, max_power, power_regeneration = profile
        power_regeneration = f"{power_regeneration:.2f}"

        embed = discord.Embed(
            title=f"{ctx.author.display_name}'s Power Status",
            color=discord.Color.blue()
        )
        embed.add_field(name='Power', value=f'{power_remaining:.0f}/{max_power} [{power_regeneration}/m]', inline=True)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.regen_task.is_running():
            self.regen_task.start()

    @regen_task.before_loop
    async def before_regen_task(self):
        await self.bot.wait_until_ready()

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(PowerRegenCog(bot))
