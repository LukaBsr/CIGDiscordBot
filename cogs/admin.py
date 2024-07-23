import sqlite3
from discord.ext import commands

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def update_user_xp(self, user_id, xp_change):
        conn = sqlite3.connect('rpg_bot.db')
        cursor = conn.cursor()
        
        # Check if user profile exists
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        profile = cursor.fetchone()
        
        if profile is None:
            # Initialize user profile if not exists
            print(f"No profile found for user {user_id}, creating default profile.")  # Debug
            cursor.execute('INSERT INTO users (user_id, level, xp, power_remaining) VALUES (?, 1, 0, 0)',
                        (user_id,))
        
        # Update user XP
        cursor.execute('UPDATE users SET xp = xp + ? WHERE user_id = ?', (xp_change, user_id))
        conn.commit()
        
        # Fetch and print updated data for verification
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        updated_data = cursor.fetchone()
        print(f"Updated user {user_id} XP by {xp_change}. Post-update data: {updated_data}")  # Debug
        conn.close()


    @commands.command(name='getxp')
    @commands.has_role('dev bot')
    async def getxp(self, ctx, xp: int):
        user_id = ctx.author.id
        self.update_user_xp(user_id, xp)
        await ctx.send(f'Added {xp} XP to {ctx.author.display_name}.')

    @commands.command(name='rmxp')
    @commands.has_role('dev bot')
    async def rmxp(self, ctx, xp: int):
        user_id = ctx.author.id
        self.update_user_xp(user_id, -xp)
        await ctx.send(f'Removed {xp} XP from {ctx.author.display_name}.')

    @getxp.error
    @rmxp.error
    async def admin_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRole):
            await ctx.send("You don't have the required role to use this command.")

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(AdminCog(bot))
