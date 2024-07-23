import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('rpg_bot.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    level INTEGER NOT NULL,
    xp INTEGER NOT NULL,
    power_remaining INTEGER NOT NULL
)
''')

# Create ores table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ores (
    user_id INTEGER,
    ore_name TEXT,
    amount INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    PRIMARY KEY(user_id, ore_name)
)
''')

# Commit and close the connection
conn.commit()
conn.close()
print('Database setup complete.')
