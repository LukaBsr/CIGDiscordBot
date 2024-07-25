# Cogs/utils.py
import aiosqlite

def get_xp_for_level(level):
    return 100 + 20 * (level - 1)

async def level_up(user_id: int, xp_gain: int):
    async with aiosqlite.connect('rpg_bot.db') as conn:
        async with conn.cursor() as cursor:
            # Fetch current profile
            await cursor.execute('SELECT level, xp FROM users WHERE user_id = ?', (user_id,))
            profile = await cursor.fetchone()
            if profile is None:
                # If the user does not exist in the database, create a default profile
                await cursor.execute(
                    'INSERT INTO users (user_id, level, xp, power_remaining, max_power, power_regeneration) VALUES (?, 1, 0, 100, 100, 1.00)',
                    (user_id,)
                )
                profile = (1, 0)  # Default profile

            level, current_xp = profile
            new_xp = current_xp + xp_gain

            # Level up logic
            xp_for_next_level = get_xp_for_level(level)
            while new_xp >= xp_for_next_level:
                new_xp -= xp_for_next_level
                level += 1
                xp_for_next_level = get_xp_for_level(level)

            # Update the profile in the database
            await cursor.execute(
                'UPDATE users SET level = ?, xp = ? WHERE user_id = ?',
                (level, new_xp, user_id)
            )
            await conn.commit()

    return level, new_xp
