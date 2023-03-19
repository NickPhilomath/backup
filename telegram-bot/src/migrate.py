
import mysql.connector
import dbfunctions as db
import const


if __name__ == '__main__':
    mydb = mysql.connector.connect(
            host=const.HOST,
            user=const.MYSQL_USER,
            password=const.MYSQL_PASS
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE backup")

    db.create_users_table()

    print("migrate compleated.")
