import mysql.connector
import hashlib
connection_address = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'learnpython',
    'database': 'pass_manage'
}
logged_in = False
connection = mysql.connector.connect(**connection_address)
cursor = connection.cursor(buffered=True)


def get_rows():
    global cursor
    values = []
    rows = cursor.rowcount
    if rows == 0:
        return 'no_rows_returned'
    elif rows != 0:
        if rows == 1:
            row = cursor.fetchone()
            values.append(list(row))
            return values
        else:
            row = cursor.fetchall()
            for value in row:
                values.append(list(value))
            return values


stmt = f"SELECT * FROM user;"
cursor.execute(stmt)
print(cursor.rowcount)
row = get_rows()
print(row)

