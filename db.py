__author__ = 'TungDesign'
# coding=utf-8

from sqlite3 import dbapi2 as sqlite3
from flask import g

def connect_db():
    """
    Connects to the specific database.

    :return: :rtype: Returns the connection value of the database.
    """
    print "Connectar db"
    try:
        rv = sqlite3.connect("skoab_database.sqlite3")
        print "Creating db"
        rv.row_factory = sqlite3.Row
        return rv
    except sqlite3.Error as e:
        print "An error occurred:", e.args[0]

def get_db():
    """
    Opens a new database connection, if there is none yet for the
    current application context.

    :return: :rtype: Returns the value of the connection.
    """
    if not hasattr(g, 'sqlite_db'):
        print "Creating new connection"
        g.sqlite_db = connect_db()
    return g.sqlite_db

#Not complete!!!
def setup():
    """
    Creates our database with
    Skapar vår databas med för nuvarande två tables en för meddelanden samt en för produkter, ska byggas ut med
    ytterligare tables för användare och ordrar

    """
    db = get_db()
    db.execute("drop table if exists messages")
    db.execute("drop table if exists product")
    db.execute("create table messages(id integer primary key, name text, message text, email text)")
    db.execute("create table product(product_id integer primary key ,product_name text,price integer ,max_size integer,min_size integer,brand text ,category text,info text,classification text, pic_url integer)")
    db.commit()

def register_user(username,password,firstname,lastname, email, telephone, org_no, org_name, address_field1, address_field2, zipcode, city):
    """
    Creates a new user by taking information the person have filled in at the frontend and putting it in a database.

    :param username: The specified input of the user for their username.
    :param password: The specified input of the user for their password.
    :param firstname: The specified input of the user for their firstname.
    :param lastname: The specified input of the user for their lastname.
    """
    db = get_db()
    if check_username(username):
        return False
    else:
        db.execute('insert into user (username, password, firstname, surname, email, telephone, org_no, org_name, address_field1, address_field2, zipcode, city) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (username, password, firstname, lastname, email, telephone, org_no, org_name, address_field1, address_field2, zipcode, city))
        db.commit()
        return True


def get_product_id(name):
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT Product_ID from product where Product_Name = ?', [name])
    result = cursor.fetchone()
    product_id = str(result[0])
    return product_id


def check_password(username, password):
    """
    Verifies the input of username and password against the database.

    :param username: The username that has been given by the user.
    :param password: The password that has been given by the user.
    :return: :rtype: Returns true if the username and password matches, else it returns false.
    """
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT Password from user where Username = ?', [username])
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        c.commit()
        if str(result[0]) == password:
            return True
        else:
            return False


def change_password(username,password):
    c = get_db()
    c.execute("UPDATE user SET Password=? WHERE username =?", (password, username))
    c.commit()


def add_new_message(name, message, email, category):
    """
    Allows the user to write messages that gets put into the database

    :param name: Name of the user.
    :param message: Input of message by the user.
    :param email: Email given by the user.
    """
    c = get_db()
    c.execute("insert into messages(name,message,email,category) values(?,?,?,?)", (name, message, email, category))
    c.commit()


def add_new_product (product_id, product_name, price, max_size, min_size, brand, category, info, classification, pic_url):
    """
    Allows a user to add new products to the database

    :param product_id: The product id of the new product, input by the user.
    :param product_name: The product name of the new product, input by the user.
    :param price: The product price of the new product, input by the user.
    :param max_size: The product maximum size of the new product, input by the user.
    :param min_size: The product minimum size of the new product, input by the user.
    :param brand: The product brand of the new product, input by the user.
    :param category: The product category of the new product, input by the user.
    :param info: The product information of the new product, input by the user.
    :param pic_url: The link to the picture of the new product, input by the user.
    :param classification: The product classification of the new product, input by the user.
    """
    c = get_db()
    c.execute("insert into Product(product_id, product_name, price, max_size, min_size, brand, category, info, classification, pic_url) values(?,?,?,?,?,?,?,?,?,?)",[product_id, product_name,price,max_size,min_size,brand,category,info,classification,pic_url])
    c.commit()


def add_new_offer (url_to, pic_url):
    """
    Allows a user to add new products to the database

    :param url_to: The url which the offer should link to, input by the user.
    :param pic_url: The link to the picture of the offer, input by the user.
    """
    c = get_db()
    c.execute("insert into offer(url_to, pic_url) values(?,?)",[url_to, pic_url])
    c.commit()


def get_messages(type):
    """
    Returns all the messages in the database, specified by the type input.

    :param type: Represents the wanted category of messages.
    :return: :rtype: Returns the messages found in the database.
    """
    c = get_db()
    result = c.execute('SELECT * from messages where Category = ?', [type])
    c.commit()
    return result.fetchall()


def get_all_products():
    """
    Picks out all the products in the database and returns them.

    :return: :rtype: Returns the products selected from the database, represented in result.
    """
    c = get_db()
    result = c.execute("select * from Product")
    c.commit()
    return result.fetchall()


def get_index_products():
    c = get_db()
    result = c.execute("select * from Product ORDER BY Product_ID desc limit 6")
    c.commit()
    return result.fetchall()


def get_offer_products():
    c = get_db()
    result = c.execute("select * from offer ORDER BY offer_id asc")
    c.commit()
    return result.fetchall()


def set_admin(name):
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT Authority from user where Username = ?', [name])
    result = cursor.fetchone()
    if not check_username(name) or int(result[0] == 3):
        message=name+" already have authority 3"
        return message
    elif int(result[0]) == 2:
        s = "UPDATE user SET Authority=3 WHERE Username='"+name+"'"
        c.execute(s)
        c.commit()
        message=name+" was promoted to authority 3"
        return message
    elif int(result[0] == 1):
        s="UPDATE user SET Authority=2 WHERE Username='"+name+"'"
        c.execute(s)
        c.commit()
        message=name+" was promoted to authority 2"
        return message


def get_all_users():
    """
    A function that returns all the information about the users

    :return: :rtype: Returns user information.
    """
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT * from user')
    result = cursor.fetchall()
    return result

def get_all_users_except_logged(name):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("SELECT * from user where username!=?", [name])
    result = cursor.fetchall()
    return result

def remove_user(name):
    """
    Allows a Admin to change a normal members Authority to a Admin level.

    :param name: The name of the user to be promoted.
    """
    if check_username(name)==False:
        return False
    else:
        c = get_db()
        s="DELETE FROM user WHERE Username='"+name+"'"
        c.execute(s)
        c.commit()
    return True


def check_username(name):
    """
    A function that checks that the username isn't already in the database.

    :param name: Name of the user that is to be checked.
    :return: :rtype: Returns true if the username isn't in the database and false if it is.
    """
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT username from user where Username = ?', [name])
    result = cursor.fetchone()
    if result == None:
        return False
    else:
        c.commit()
        return True


def get_specific_product(type,id,sort):
    """
    Allows the website to pick out a specific product based on a search of an attribute and search word.

    :param type: The type of the wanted product, input by user.
    :param id: The id of the wanted product, input by user.
    :return: :rtype: Returns the products that meets the search criterias.
    """
    c = get_db()
    s="select * from product where "+type+"='"+id+"'"
    if(sort !=""):
        s=s+" ORDER BY "+sort+""
    print(s)
    result = c.execute(s)
    c.commit()
    return result.fetchall()


def get_authority(user_name):
    c = get_db()
    result = c.execute('select authority from user where username=?', [user_name])
    c.commit()
    authority=int(result.fetchone()[0])
    return authority


def alter_product(product_id, product_name, price, max_size, min_size, brand, category, info, pic_url, filename):
    c = get_db()
    c.execute("UPDATE product SET Product_Name=?, Price=?, Max_size=?, Min_size=?, Brand=?, Category=?, Info=?, classification=?, pic_url=? WHERE product_id =?", (product_name, price, max_size, min_size, brand, category, info, filename, pic_url, product_id))
    c.commit()


def add_new_order(user_id, date_placed, products, total):
    c = get_db()
    c.execute("insert into orderregister(user_id, date_placed, total_ammount) values(?,?,?)", [user_id, date_placed, total])
    c.commit()
    order_id = c.execute("SELECT last_insert_rowid()").fetchall()[0][0]
    d = get_db()
    for product in products:
        d.execute("insert into order_product_occurrence(order_id, product_id, size, quantity, unit_price) values(?,?,?,?,?)", [order_id, product[0], product[1], product[2], product[3]])
        d.commit()


#Väldigt lik funktionen under och bör slås ihop med den.
def get_user(username):
    c = get_db()
    result = c.execute('select * from user where username=?', [username])
    c.commit()
    user=result.fetchall()
    return user

def get_user_id(user_name):
    """ Gets user_id from input username :param user_name: Username of wanted user :return: User_id of wanted user """
    c = get_db()
    result = c.execute('select user_id from user where username=?', [user_name])
    c.commit()
    user_id=int(result.fetchone()[0])
    return user_id


def remove_product(product_id):
    c = get_db()
    c.execute("delete FROM product WHERE Product_ID = ?", [product_id])
    c.commit()


def get_user_orders(user_id):
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT * from orderregister where user_id = ?', [user_id])
    return cursor.fetchall()

def get_order_products(order_id):
    c = get_db()
    cursor = c.cursor()
    cursor.execute('SELECT * from order_product_occurrance where order_id = ?', [order_id])
    return cursor.fetchall()

if __name__ == '__main__':
    p = connect_db()
    print p