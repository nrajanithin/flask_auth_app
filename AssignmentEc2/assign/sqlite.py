import sqlite3

connect = sqlite3.connect('database.db')
print("opened")

connect.execute('DROP TABLE IF EXISTS users')
connect.execute('CREATE TABLE users (firstname TEXT, lastname TEXT, email TEXT, username TEXT PRIMARYKEY ,password TEXT)')
print("Table created successfully")
connect.close()
