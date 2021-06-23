# Imports
import pyperclip
import mysql.connector
import hashlib
import random

# Configuration
connection_address = {
    'host': 'localhost',
    'port': '3306',
    'user': 'root',
    'password': 'learnpython',
    'database': 'pass_manage'
}

# Variables
logged_in = False
user_id = None
chars = "abcdefghijklmnopqrstuvwxyz1234567890@#$%^*()[]{};:/?<>|+-_=&!`"
menu1 = """
----------------------------------
--------------MENU---------------|
1. Register                      |
2. Login                         |
q. Quit                          |
---------------------------------|
"""
menu2 = """
------------------------------------------------
---------------------MENU-----------------------|
1. Create password                              |
2. Find a password for a site (or) app.         |
3. Find sites and apps connected to a username. |
4. Update username of a specific site (or) app. |
5. Update password of a specific site (or) app. |
6. Remove a site (or) app.                      |
q. Quit                                         |
------------------------------------------------|
"""
menu3 = """
-----------------------------------------------
---------------------MENU----------------------|
1. To generate a password for you and save it. |
2. To specify a password that is to be saved.  |
q. Quit                                        |
-----------------------------------------------|
"""
menu4 = """
-------------------------------------------------
---------------------MENU------------------------|
1. To generate a password for you and update it. |
2. To specify a password that is to be updated.  |
q. Quit                                          |
-------------------------------------------------|
"""
# Functions


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


def user_registration(username):
    global cursor
    global logged_in
    if logged_in is not True:
        check1_stmt = f"SELECT * FROM `user` WHERE `username` = '{username}';"
        cursor.execute(check1_stmt)
        rows = get_rows()
        if rows == 'no_rows_returned':
            global user_id
            password = str(input("Enter your desired master password: ")).strip(" ").lower()
            hash = hashlib.sha256(password.encode("utf-8"))
            pass_hashed = hash.hexdigest()
            stmt = f"INSERT INTO `user`(`username`, `password`) VALUES ('{username}', '{pass_hashed}');"
            cursor.execute(stmt)
            connection.commit()
            stmt = f"SELECT `user_id` FROM `user` WHERE `username` = '{username}';"
            cursor.execute(stmt)
            row = get_rows()
            user_id = row[0][0]
            logged_in = True
            print("Your account was created successfully and you are logged in!\n")
        else:
            print("You already have an account registered, please login to continue!\n")
    else:
        print("You are already logged in!")


def user_login(username):
    global logged_in
    if logged_in is not True:
        global cursor
        stmt = f"SELECT `user_id` FROM `user` WHERE `username` = '{username}';"
        cursor.execute(stmt)
        rows = get_rows()
        if rows != 'no_rows_returned':
            global user_id
            user_id = rows[0][0]
            password = str(input("Enter your password: ")).strip(" ").lower()
            stmt2 = f"SELECT `password` FROM `user` WHERE `user_id` = {user_id};"
            cursor.execute(stmt2)
            rows = get_rows()
            hash = hashlib.sha256(password.encode("utf-8"))
            pass_hashed = hash.hexdigest()
            if rows[0][0] == pass_hashed:
                logged_in = True
                print("You are successfully logged in!\n")
            else:
                print("Incorrect Password! Please try again!\n")
        else:
            print("Your username doesn't exist, please register to continue!\n")
    else:
        print("You are already logged in!\n")


def create_password():
    global logged_in
    if logged_in is True:
        global cursor
        global user_id
        appname = str(input("Enter a site (or) app name: ")).strip(" ").lower()
        stmt = f"SELECT * FROM `passwords` WHERE `app_name` = '{appname}' AND `user_id` = {user_id};"
        cursor.execute(stmt)
        rows = get_rows()

        if rows == 'no_rows_returned':
            global menu3
            print(menu3)
            derive_method = str(input("Enter a character to continue: ")).strip(" ").lower()
            if derive_method == '1':
                pass_len = int(input("Enter a desired length you want your password to be: "))
                password = ""
                for x in range(0, pass_len):
                    password_char = random.choice(chars)
                    password += password_char
                username = str(input("Enter a username/email for the site (or) app: ")).strip(" ").lower()
                stmt = f"""INSERT INTO `passwords` (`user_id`, `username`, `password`, `app_name`) 
                VALUES ({user_id}, '{username}','{password}',  '{appname}')"""
                cursor.execute(stmt)
                connection.commit()
                print("Your password was generated and saved!")
                pyperclip.copy(password)
                print(f"Here is your password copied to clipboard: {password}")
            elif derive_method == '2':
                password = str(input(f"Enter a desired password for {appname}: ")).strip(" ").lower()
                username = str(input("Enter a username/email for the site (or) app: ")).strip(" ").lower()
                stmt = f"""INSERT INTO `passwords` (`user_id`, `username`, `password`, `app_name`) 
                VALUES ({user_id}, '{username}','{password}',  '{appname}')"""
                cursor.execute(stmt)
                connection.commit()
                print("Your password was generated and saved!")
                pyperclip.copy(password)
                print(f"Here is your password copied to clipboard: {password}\n")
        else:
            print("Your entered site (or) app name already exists, please enter a different one!\n")
    else:
        print("You aren't logged in, please login  to continue!\n")


def find_password():
    global logged_in
    if logged_in is True:
        global cursor
        global user_id
        appname = str(input("Enter a site (or) app name to search for: ")).strip(" ").lower()
        stmt = f"SELECT * FROM `passwords` WHERE `app_name` = '{appname}' AND `user_id` = {user_id};"
        cursor.execute(stmt)
        rows = get_rows()
        if rows != 'no_rows_returned':
            print(f"Username: {rows[0][2]}\nPassword: {rows[0][3]}")
            print("Your password was copied to clipboard!\n")
        else:
            print("Your entered site (or) app name doesn't exists, please enter a existing one!]\n")
    else:
        print("You aren't logged in, please login  to continue!\n")


def find_usernames():
    global logged_in
    if logged_in is True:
        global user_id
        global cursor
        username = str(input("Enter a username (or) email to search for: ")).strip(" ").lower()
        stmt = f"SELECT * FROM `passwords` WHERE `username` = '{username}' AND `user_id` = {user_id};"
        cursor.execute(stmt)
        rows = get_rows()
        if rows != 'no_rows_returned':
            i = 1
            for row in rows:
                print(f"{i}. Site (or) App Name: {row[4]}\n   Password: {row[3]}")
                i += 1
            print(" ")
        else:
            print("Your username (or) email doesn't exists, please enter a valid email!")
    else:
        print("You aren't logged in, please login to continue!\n")


def update_username():
    global logged_in
    if logged_in is True:
        global cursor
        global user_id
        appname = str(input("Enter a site (or) app name that is to be updated: ")).strip(" ").lower()
        stmt = f"SELECT * FROM `passwords` WHERE `app_name` = '{appname}' AND `user_id` = {user_id};"
        cursor.execute(stmt)
        rows = get_rows()
        if rows != 'no_rows_returned':
            username = str(input("Enter a username to update: ")).strip(" ").lower()
            stmt2 = f"UPDATE `passwords` SET `username` = '{username}' WHERE `app_name` = '{appname}' and `user_id` = '{user_id}';"
            cursor.execute(stmt2)
            connection.commit()
            print(f"Your username for {appname} was successfully updated!\n")

        else:
            print("Your entered site (or) app name doesn't exist, please enter a existing one!\n")
    else:
        print("You aren't logged in, please login to continue!\n")


def update_password():
    global logged_in
    if logged_in is True:
        global cursor
        global user_id
        appname = str(input("Enter a site (or) app name that is to be updated: ")).strip(" ").lower()
        stmt = f"SELECT * FROM `passwords` WHERE `app_name` = '{appname}' AND `user_id` = {user_id};"
        cursor.execute(stmt)
        rows = get_rows()

        if rows != 'no_rows_returned':
            global menu4
            print(menu4)
            derive_method = str(input("Enter a character to continue: ")).strip(" ").lower()
            if derive_method == '1':
                pass_len = int(input("Enter a desired length you want your password to be: "))
                password = ""
                for x in range(0, pass_len):
                    password_char = random.choice(chars)
                    password += password_char
                stmt = f"""UPDATE `passwords` SET `password` = '{password}' 
                WHERE `app_name` = '{appname}' AND `user_id` = '{user_id}';"""
                cursor.execute(stmt)
                connection.commit()
                print("Your password was generated and saved!")
                pyperclip.copy(password)
                print(f"Here is your password copied to clipboard: {password}")
            elif derive_method == '2':
                password = str(input(f"Enter a desired password for {appname}: ")).strip(" ").lower()
                stmt = f"""UPDATE `passwords` SET `password` = '{password}' 
                WHERE `app_name` = '{appname}' AND `user_id` = '{user_id}';"""
                cursor.execute(stmt)
                connection.commit()
                print("Your password was generated and saved!")
                pyperclip.copy(password)
                print(f"Here is your password copied to clipboard: {password}\n")

        else:
            print("Your entered site (or) app name doesn't exist, please enter a existing one!\n")
    else:
        print("You aren't logged in, please login  to continue!\n")


def delete_account():
    global logged_in
    if logged_in is True:
        global user_id
        global cursor
        appname = str(input("Enter a site (or) app name that is to be deleted: ")).strip(" ").lower()
        stmt = f"SELECT * FROM `passwords` WHERE `app_name` = '{appname}' AND `user_id` = {user_id};"
        cursor.execute(stmt)
        rows = get_rows()
        print("Are you sure?")
        assurity = str(input("(y) Yes & (n) No: ")).strip(" ").lower()
        if assurity == 'y':
            if rows != 'no_rows_returned':
                stmt = f"DELETE FROM `passwords` WHERE `app_name` = '{appname}' AND (`user_id` = '10');"
                cursor.execute(stmt)
                connection.commit()
                print("Your specified site (or) app was removed!\n")

            else:
                print("Your username (or) email doesn't exists, please enter a valid email!")
        else:
            print("Your site (or) app wasn't removed!")
    else:
        print("You aren't logged in, please login to continue!\n")


if __name__ == '__main__':
    connection = mysql.connector.connect(**connection_address)
    cursor = connection.cursor(buffered=True)

    while logged_in is False:
        print(menu1)
        main_input = str(input("Enter any character given above: ")).strip(" ").lower()

        if main_input == '1':
            register_username = str(input("Enter your desired username: ")).strip(" ").lower()
            user_registration(username=register_username)
        elif main_input == '2':
            login_username = input("Enter your username to login: ")
            user_login(username=login_username)
        elif main_input == 'q':
            print("Thank You for using Pass-Manage!")
            break
        else:
            print("Pass-Manage couldn't understand?\n")

    while logged_in is True:
        print(menu2)
        sub_input = str(input("Enter a character a above to continue: ")).strip(" ").lower()

        if sub_input == '1':
            create_password()
        elif sub_input == 'q':
            print("Thank You for using Pass-Manage!")
            break
        elif sub_input == '2':
            find_password()
        elif sub_input == '3':
            find_usernames()
        elif sub_input == '4':
            update_username()
        elif sub_input == '5':
            update_password()
        elif sub_input == '6':
            delete_account()
        else:
            print("Pass-Manage couldn't understand?\n")
