import sqlite3

# Connect to the database (creates the database if it doesn't exist)
conn = sqlite3.connect('../../finances_predictor/db.sqlite3')

# Create a cursor object to execute SQL commands
c = conn.cursor()

# Create the tables
c.execute('''CREATE TABLE IF NOT EXISTS User (
             id INTEGER PRIMARY KEY,
             username TEXT NOT NULL,
             password TEXT NOT NULL
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS Portfolio (
             id INTEGER PRIMARY KEY,
             user_id INTEGER NOT NULL,
             name TEXT NOT NULL,
             approach TEXT NOT NULL,
             FOREIGN KEY(user_id) REFERENCES User(id)
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS Asset (
             id INTEGER PRIMARY KEY,
             portfolio_id INTEGER NOT NULL,
             symbol TEXT NOT NULL,
             shares INTEGER NOT NULL,
             FOREIGN KEY(portfolio_id) REFERENCES Portfolio(id)
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS Goal (
             id INTEGER PRIMARY KEY,
             portfolio_id INTEGER NOT NULL,
             name TEXT NOT NULL,
             amount REAL NOT NULL,
             FOREIGN KEY(portfolio_id) REFERENCES Portfolio(id)
             )''')

c.execute('''CREATE TABLE IF NOT EXISTS History (
             id INTEGER PRIMARY KEY,
             asset_id INTEGER NOT NULL,
             date TEXT NOT NULL,
             price REAL NOT NULL,
             FOREIGN KEY(asset_id) REFERENCES Asset(id)
             )''')

# Commit changes and close the connection
conn.commit()
conn.close()
