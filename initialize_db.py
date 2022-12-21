import sqlite3
conn = sqlite3.connect('actions/example.db')

c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE orders
#              (text, trans text, symbol text, qty real, price real)''')


# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

# EXISTING ORDERS
# Create table
c.execute('''CREATE TABLE orders
            (order_date, order_number INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, color, size, status, 
            FOREIGN KEY(email) REFERENCES users(email))''')

# data to be added
purchases = [('2006-01-05',123456,'example@rasa.com','blue', 9, 'shipped'),
             ('2021-01-05',123457,'me@rasa.com','black', 10, 'order pending'),
             ('2021-01-05',123458,'me@gmail.com','gray', 11, 'delivered'),
             ('2021-02-05',123459,'a@mail.com','gray', 11, 'delivered'),
            ]
# add data
c.executemany('INSERT INTO orders VALUES (?,?,?,?,?,?)', purchases)

# AVAILABLE INVENTORY
# Create table
c.execute('''CREATE TABLE inventory
             (size, color, count)''')

# data to be added
inventory = [(8, 'blue', 10),
            (9, 'blue', 10),
            (10, 'blue', 10),
            (11, 'blue', 10),
            (12, 'blue', 10),
            (7, 'black', 10),
            (8, 'black', 10),
            (9, 'black', 10),
            (10, 'black', 10),
            (11, 'black ', 10),
            (12, 'black', 10),
            (7, 'red', 10),
            (8, 'red', 10),
            (9, 'red', 10),
            (10, 'red', 10),
            (11, 'red', 10),
            (12, 'red', 10),
            (7, 'green', 10),
            (8, 'green', 10),
            (9, 'green ', 10),
            (10, 'green', 10),
            (11, 'green', 10),
            (12, 'green', 10),
            (7, 'blue', 10)
            ]

# add data
c.executemany('INSERT INTO inventory VALUES (?,?,?)', inventory)

# Create table
c.execute('''CREATE TABLE users
             (email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, status INTEGER NOT NULL DEFAULT 0, PRIMARY KEY(email))''')

users_data = [  ('me@rasa.com', '123456', 1),
                ('example@rasa.com', '111222', 0),
                ('me@gmail.com', '121212', 0)  
            ]

c.executemany('INSERT INTO users VALUES (?,?,?)', users_data)
# Save (commit) the changes
conn.commit()

# end connection
conn.close()