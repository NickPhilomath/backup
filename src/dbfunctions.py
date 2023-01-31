import const
import mysql.connector

# mydb = mysql.connector.connect(
#   host="localhost",
#   user="yourusername",
#   password="yourpassword"
# )



class MySQLCursor:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=const.HOST,
            user=const.MYSQL_USER,
            password=const.MYSQL_PASS,
            database=const.DATABASE_NAME
        )

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.connection.commit()
        except mysql.connector.Error as e:
            print(e)
            self.connection.rollback()


def create_database():
    with MySQLCursor() as cur:
        query = f"CREATE DATABASE {const.DATABASE_NAME}"
        cur.execute(query)


def create_users_table():
    with MySQLCursor() as cur:
        query = "CREATE TABLE users (id BIGINT NOT NULL AUTO_INCREMENT, username CHAR(30) NOT NULL, password CHAR(16) NOT NULL, chat_id BIGINT, PRIMARY KEY (id))"
        cur.execute(query)

def authorized_chat_id(user):
    with MySQLCursor() as cur:
        query = f"SELECT chat_id FROM users WHERE username='{user}'"
        cur.execute(query)
        result = cur.fetchone()
    return result[0]

def authorized_username(chat_id):
    with MySQLCursor() as cur:
        query = f"SELECT username FROM users WHERE chat_id='{chat_id}'"
        cur.execute(query)
        result = cur.fetchone()
    return result[0]

def all_chat_ids():
    with MySQLCursor() as cur:
        query = f"SELECT chat_id FROM users"
        cur.execute(query)
        result = cur.fetchall()
    return [r[0] for r in result]

def authorize(username, password, chat_id):
    # check if password is correct
    with MySQLCursor() as cur:
        query = f"SELECT password FROM users WHERE username='{username}'"
        cur.execute(query)
        user_password = cur.fetchone()[0]

    print("up", user_password)

    if user_password == password:
        # authorize user to the chat 
        with MySQLCursor() as cur:
            query = f"UPDATE users SET chat_id='{chat_id}' WHERE username='{username}'"
            cur.execute(query)
        
        return True
    return False



if __name__ == '__main__':
    print(all_chat_ids())


# def show_menu():
#     with SqliteCursor(const.dbname) as cur:
#         queryvar = "SELECT dish FROM menu"
#         cur.execute(queryvar)
#         all = cur.fetchall()
#         return [e[0] for e in all]


# def show_descr(item):
#     with SqliteCursor(const.dbname) as cur:
#         queryvar = "SELECT description FROM menu WHERE dish =:dish"
#         cur.execute(queryvar, {"dish": item})
#         all = cur.fetchall()
#         # return [e[0] for e in all[0]] # or like that?
#         return all[0][0]


# def show_price(item):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "SELECT price FROM menu WHERE dish =:dish"
#     c.execute(queryvar, {"dish" :item})
#     all = c.fetchall()
#     lst = list()
#     for e in all:
#         e = e[0]
#         lst.append(e)
#     return lst[0]


# def show_photo(item):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "SELECT picture FROM menu WHERE Dish =:dish"
#     c.execute(queryvar, {"dish" :item})
#     all = c.fetchall()
#     lst = list()
#     for e in all:
#         e = e[0]
#         lst.append(e)
#     return lst[0]


# def addtocart(id, item, price):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "INSERT INTO cart VALUES(?,?,?)"
#     c.execute(queryvar, (id, item, price))
#     conn.commit()


# def showcart(id):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "SELECT Dish FROM cart WHERE user =:user"
#     c.execute(queryvar, {"user" :id})
#     return c.fetchall()


# def summary(id):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "SELECT Price FROM cart WHERE user =:user"
#     c.execute(queryvar, {"user" :id})
#     sum = 0
#     for item in c.fetchall():
#         sum += item[0]
#     return sum


# def empty_cart(id):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "DELETE from cart WHERE user =:user"
#     c.execute(queryvar, {"user" :id})
#     conn.commit()


# def save_order(id,status):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "INSERT INTO orders(user,status) VALUES(?,?)"
#     c.execute(queryvar, (id, status))
#     conn.commit()


# def location(id,loc):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     #queryvar = "INSERT INTO orders(location) VALUES(?)"
#     queryvar = "UPDATE orders SET location = (?) WHERE user = (?)"
#     c.execute(queryvar,(loc,id))
#     conn.commit()


# def status(st,id):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "UPDATE orders SET status = (?) WHERE user = (?)"
#     c.execute(queryvar,(st,id))
#     conn.commit()


# def show_status(id):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "SELECT status FROM Orders WHERE user =:user"
#     c.execute(queryvar, {"user" :id})
#     return (c.fetchall()[0][0])


# def delete_order(id):
#     conn = sqlite3.connect('menu.db')
#     c = conn.cursor()
#     queryvar = "DELETE from Orders WHERE user =:user"
#     c.execute(queryvar, {"user" :id})
#     conn.commit()
