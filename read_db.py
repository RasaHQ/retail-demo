import sqlite3
conn = sqlite3.connect('example.db')
c = conn.cursor()

# show all entries
for row in c.execute('SELECT * FROM orders ORDER BY order_number'):
        print(row)

# for row in c.execute('SELECT * FROM inventory ORDER BY color'):
#         print(row)

# t = ('RHAT',)
# c.execute('SELECT * FROM stocks WHERE symbol=?', t)
# print(c.fetchone())

# update status


inp1 = 'changed'
inp2 = 'me@rasa.com'

status = [
    (inp1),
    (inp2)
]

c.execute('UPDATE orders SET status=? WHERE order_email=?', status)

# show all entries
for row in c.execute('SELECT * FROM orders ORDER BY order_number'):
        print(row)

# # get status based on order num
# inp = 123456
# order_num = (inp,)
# c.execute('SELECT * FROM orders WHERE order_number=?', order_num)
# rw = list(c.fetchone())
# print(rw[5])

# # get status based on email
# inp = 'me@rasa.com'
# order_email = (inp,)
# c.execute('SELECT * FROM orders WHERE order_email=?', order_email)
# rw = list(c.fetchone())
# print(rw[5])

# # cancel + return order
# inp = 'me@rasa.com'
# order_email = (inp,)
# c.execute('SELECT * FROM orders WHERE order_email=?', order_email)
# rw = list(c.fetchone())
# # then print message about order being cancelled

# inventory search
inp1 = 'blue'
inp2 = 6

color = (inp1,)
size = (inp2,)

shoe = [
    (inp1),
    (inp2)
]

c.execute('SELECT * FROM inventory WHERE color=? AND size=?', shoe)
search = c.fetchone()
print(search)

if isinstance(search, tuple):
    print('Looks like you are in luck!')
else: 
    print('sorry those are out of stock.')

# change status of item
c.execute('SELECT * FROM orders WHERE order_number=?', order_num)
rw = list(c.fetchone())
print(rw[5])

