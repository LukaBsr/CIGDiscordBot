import sqlite3
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_xp_for_level(self, level):
        return 100 + 20 * (level - 1)  # XP needed for the specified level

    def update_user_xp(self, user_id, xp_change):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT level, xp FROM users WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        
        if profile is None:
            print(f"No profile found for user {user_id}, creating default profile.")  # Debug
            cursor.execute('INSERT INTO users (user_id, level, xp, power_remaining, max_power, power_regeneration) VALUES (?, 1, 0, 100, 100, 1.00)',
                        (user_id,))
            profile = (1, 0)  # Default profile if not found
        
        level, current_xp = profile
        new_xp = current_xp + xp_change
        
        while new_xp >= self.get_xp_for_level(level):
            new_xp -= self.get_xp_for_level(level)
            level += 1
            print(f"Level up! New level: {level}")  # Debug
            max_power = 100 + 5 * (level - 1)
            power_regeneration = 1.00 + 0.1 * (level - 1)
            cursor.execute('UPDATE users SET level = ?, xp = ?, max_power = ?, power_regeneration = ? WHERE user_id = ?',
                           (level, new_xp, max_power, power_regeneration, user_id))
            conn.commit()
        
        if new_xp != current_xp:
            cursor.execute('UPDATE users SET xp = ? WHERE user_id = ?', (new_xp, user_id))
            conn.commit()
        
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        updated_data = cursor.fetchone()
        print(f"Updated user {user_id} XP by {xp_change}. Post-update data: {updated_data}")  # Debug
        conn.close()

    @commands.command(name='getxp')
    @commands.has_role('dev bot')
    async def getxp(self, ctx, xp: int):
        user_id = ctx.author.id
        try:
            self.update_user_xp(user_id, xp)
            await ctx.send(f'Added {xp} XP to {ctx.author.display_name}.')
        except Exception as e:
            print(f"Error in getxp command: {e}")
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name='rmxp')
    @commands.has_role('dev bot')
    async def rmxp(self, ctx, xp: int):
        user_id = ctx.author.id
        try:
            self.update_user_xp(user_id, -xp)
            await ctx.send(f'Removed {xp} XP from {ctx.author.display_name}.')
        except Exception as e:
            print(f"Error in rmxp command: {e}")
            await ctx.send(f"An error occurred: {e}")

    @getxp.error
    @rmxp.error
    async def admin_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the required role to use this command.")

    @commands.command(name='deleteaccount')
    @commands.has_role('dev bot')
    async def deleteaccount(self, ctx):
        user_id = ctx.author.id
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
        cursor.execute('DELETE FROM ores WHERE user_id = ?', (user_id,))
        conn.commit()
        conn.close()

        await ctx.send(f'Your account has been deleted, {ctx.author.display_name}.')

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(AdminCog(bot))
