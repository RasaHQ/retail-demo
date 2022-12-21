import sqlite3

path_to_db = "actions/example.db"
connection = sqlite3.connect(path_to_db)
cursor = connection.cursor()
'''cursor.execute("SELECT email FROM users WHERE status == 1")
email = cursor.fetchone()[0]
color = 'blue'
size = 10
shoe = [(tracker.get_slot("color")), (tracker.get_slot("size"))]
cursor.execute("INSERT into orders (order_date, email, color, size, status) values (?,?,?,?,?)", (str(datetime.now().date()), email, color, size, "reserved"))
cursor.execute("UPDATE inventory SET count=count-1 WHERE color=? AND size=?", (color, size))'''

cursor.execute("Select * FROM orders")
records = cursor.fetchall()
for row in records:
    print(row)
cursor.execute("Select * FROM users")
records = cursor.fetchall()
for row in records:
    print(row)
cursor.execute("Select * FROM inventory")
records = cursor.fetchall()
for row in records:
    print(row)
connection.commit()
connection.close()