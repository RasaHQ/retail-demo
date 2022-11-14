import sqlite3
conn = sqlite3.connect('example.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')


# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# Create table

c.execute('''CREATE TABLE status 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, name)''')

statuses = [
    ('shipped',),
    ('order pending',),
    ('delivered',)
]

c.executemany('INSERT INTO status (name) VALUES(?)', statuses)


c.execute('''CREATE TABLE user
        (id INTEGER PRIMARY KEY AUTOINCREMENT, email)''')

users = [
    ('example@rasa.com',),
    ('me@rasa.com',),
    ('me@gmail.com',)
]

c.executemany('INSERT INTO user (email) VALUES (?)', users)


c.execute('''CREATE TABLE orders
             (order_number INTEGER PRIMARY KEY AUTOINCREMENT, order_date, user, color, size, status,
             FOREIGN KEY(user) REFERENCES user(id),
             FOREIGN KEY(status) REFERENCES status(id))''')

# data to be added
purchases = [('2006-01-05',1,'blue', 9, 1),
             ('2021-01-05',2,'black', 10, 2),
             ('2021-01-05',3,'gray', 11, 3),
            ]

# add data
c.executemany('INSERT INTO orders (order_date, user, color, size, status) VALUES (?,?,?,?,?)', purchases)

# AVAILABLE INVENTORY
# Create table
c.execute('''CREATE TABLE inventory
             (size, color, count)''')

# data to be added
inventory = [(7, 'blue', 1),
             (8, 'blue', 3),
             (9, 'blue', 0),
             (10, 'blue', 1),
             (11, 'blue', 0),
             (12, 'blue', 3),
             (7, 'black', 3333),
             (8, 'black', 1),
             (9, 'black', 0),
             (10, 'black', 1)
            ]

# add data
c.executemany('INSERT INTO inventory VALUES (?,?,?)', inventory)


# Save (commit) the changes
conn.commit()

# end connection
conn.close()