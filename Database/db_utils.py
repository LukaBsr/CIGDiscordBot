# Database/db_utils.py
import aiosqlite
import logging

logger = logging.getLogger(__name__)

async def get_user_profile(user_id: int):
    try:
        async with aiosqlite.connect('rpg_bot.db') as conn:
            async with conn.cursor() as cursor:
                # Check if the user exists
                await cursor.execute('SELECT level, xp, power_remaining, max_power, power_regeneration FROM users WHERE user_id = ?', (user_id,))
                profile = await cursor.fetchone()

                if profile is None:
                    # User does not exist, insert a new profile with default values
                    logger.info(f"User {user_id} not found in database. Adding new entry.")
                    await cursor.execute(
                        'INSERT INTO users (user_id, level, xp, power_remaining, max_power, power_regeneration) VALUES (?, 1, 0, 100, 100, 1.00)',
                        (user_id,)
                    )
                    await conn.commit()

                    # Fetch the newly inserted profile
                    await cursor.execute('SELECT level, xp, power_remaining, max_power, power_regeneration FROM users WHERE user_id = ?', (user_id,))
                    profile = await cursor.fetchone()

                logger.debug(f"Fetched profile data: {profile}")  # Debug: Check the fetched profile data

                # Unpack the profile data
                level, xp, power_remaining, max_power, power_regeneration = profile

                # Fetch ores associated with the user
                await cursor.execute('SELECT ore_name, amount FROM ores WHERE user_id = ?', (user_id,))
                ores = await cursor.fetchall()
                ores_dict = dict(ores)
            
        return {
            'level': level,
            'xp': xp,
            'power_remaining': power_remaining,
            'max_power': max_power,
            'power_regeneration': power_regeneration,
            'ores': ores_dict
        }
    except Exception as e:
        logger.error(f"Error fetching user profile: {e}")
        return None
