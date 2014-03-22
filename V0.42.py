# coding=utf-8
import os
from flask import Flask, request, session, g, redirect, url_for, \
    render_template, flash, send_from_directory
from werkzeug.utils import secure_filename
from datetime import datetime
import db


app = Flask(__name__)

app.config.update(dict(
    SECRET_KEY='os.urandom(24)',
    UPLOAD_FOLDER='C:\Users\Patrick\Desktop\PycharmProjects\V0.42\static\uploads',
    ALLOWED_EXTENSIONS={'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'JPG'}
))



def allowed_file(filename):
    """
    For a given file, return whether it's an allowed type or not.

    :param filename: Name of the file to be checked.
    :return: :rtype: Returns the allowed extension added to the filename, after check.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """
    The app route for the uploaded file.

    :param filename: Name of the uploaded file.
    :return: :rtype: Returns the uploaded folder and filename.
    """
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/')
def index():
    """
    The app route for the rendered index page, when you go to the websites start page.

    :return: :rtype: Returns the rendered template for the index.html and allproducts.
    """
    if not session.has_key('cart'):
        session['cart']=[]
        session['cart_length']=0

    indexproducts = db.get_index_products()
    offerproducts = db.get_offer_products()
    return render_template("index.html", data=indexproducts, offers=offerproducts)


@app.route('/add_offer')
def add_offer():
    """
    The app route for the add offer site.

    :return: :rtype: Returns the rendered add offer site.
    """

    return render_template("add_offer.html")


@app.route('/my_page')
def mypage():
    """
    The app route for the my page site.

    :return: :rtype: Returns the rendered my page site.
    """

    return render_template("my_page.html")

@app.route('/user_info/<name>')
def userinfo(name):

    userinfo= db.get_user(name)
    return render_template("user_info.html", user= userinfo)

@app.route('/products')
def product():
    """
    The app route for the rendered product page, showing the products in the database.

    :return: :rtype: Returns the rendered template for the products.html and related products.
    """
    allproducts = db.get_all_products()
    return render_template("products.html", data=allproducts)

@app.route('/products/<name>')
def specproduct(name):
    """
    Calls for a function that sorts out the product with the name you searched
    for as well as render a product page for that product.

    :param name: Name of the product wanted.
    :return: :rtype: Returns the rendered template for productdetail.html, related products, name, comments ans avaliable sizes.
    """
    sizes = []
    product= db.get_specific_product("product_name",name,"")
    if str(product[0][6]) == "Jacka" or str(product[0][6]) == "Jacket":
        sizes = ["Small", "Medium", "Large", "XL", "XXL", "XXXL"]
    else:
        x = int(product[0][4])
        while x <= int(product[0][3]):
            sizes.append(x)
            x += 1
    product_id = db.get_product_id(name)
    comments = db.get_messages(product_id)
    return render_template("productdetail.html",data=product,name=name,comments=comments, sizes=sizes)

@app.route('/category/<name>')
def speccategory(name):
    """
    Allows the webpage to pick out all products of a specific category and then render a page with all products
    of that category
    :param name: The name of the parameter in the specified category
    :return: :rtype: Returns the rendered html-template, for category with the return values of product and name
    """
    product= db.get_specific_product("category",name,"")
    return render_template("category.html",data=product,name=name)

@app.route('/category/<category>/sorted_by_<sort>')
def sortby(category,sort):
    product = db.get_specific_product("category",category,sort)
    return render_template("category.html",data=product)

@app.route('/kuk', methods=['GET', 'POST'])
def changepassword():
    password=request.form['old_password']
    username= session['username']
    if db.check_password(username,password) == False:
        print(request.form['new_password'])
        error = 'Invalid password'
        print("1")
    elif request.form['new_password'] != request.form['confirm_password']:
            error = 'Inputted password and confirmed password, must match'
            print("olikA LÖSEN")
    else:
        print("2")
        db.change_password(session['username'],request.form['new_password'])
        print("3")
    return redirect(url_for('userinfo(username)'))



@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    The app route for the register page, allowing users to register to the database.

    :return: :rtype: Returns the redirect for the homepage if the user is succesfully registered
    else renders the register home page if the user fails to login properly.
    """
    if request.method == 'POST':
        if request.form['username'] == "":
            error = 'Must input username'
        elif request.form['password'] != request.form['confirmed_password']:
            error = 'Inputted password and confirmed password, must match'
        elif request.form['firstname'] == "":
            error = 'Must input firstname'
        elif request.form['lastname'] == "":
            error = 'Must input lastname'
        else:
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            if not db.register_user(username, password, firstname, lastname):
                message = 'The username already exists'
                return render_template('register.html', message=message)
            else:
                session['logged_in'] = True
                session['authority'] = db.get_authority(username)
                session['username'] = username
            return redirect(url_for('index'))
        return render_template('register.html', error=error)
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Function that controls the login of users of the website.
    It takes in the parameters of username and password  from the website login form.
    If succesful, it redirects you to the logged in view.

    :return: :rtype: Returns the redirect to the homepage, if you're logged in
    else it renders the login.html and sends an error message.
    """
    error = None
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        if db.check_password(username,password) == False:
            error = 'Invalid password or username'
        else:
            session['authority'] = db.get_authority(username)
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/login_checkout', methods=['GET', 'POST'])
def login_checkout():
    """
    Function that controls the login of users of the website.
    It takes in the parameters of username and password  from the website login form.
    If succesful, it redirects you to the logged in view.

    :return: :rtype: Returns the redirect to the homepage, if you're logged in
    else it renders the login.html and sends an error message.
    """
    error = None
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        if db.check_password(username,password) == False:
            error = 'Invalid password or username'
        else:
            session['authority'] = db.get_authority(username)
            session['username'] = username
            session['logged_in'] = True
            return redirect(url_for('add_order'))
    return render_template('login.html', error=error)


@app.route('/add_product')
def add_product():
    """
    The app route for the add product site.

    :return: :rtype: Returns the rendered add product site.
    """
    return render_template("add_product.html")

@app.route('/alter/<name>')
def alter(name):
    """
    The app route for the add product site.

    :return: :rtype: Returns the rendered add product site.
    """
    data = db.get_specific_product("product_name",name,"")
    return render_template("alter.html",data=data,name=name)

@app.route('/about_us')
def about():
    """
    The app route for the about page.

    :return: :rtype: Returns the rendered about page.
    """
    return render_template("about.html")

@app.route('/contact')
def contact():
    """
    The app route for the contact page.

    :return: :rtype: Returns the rendered contact page.
    """
    return render_template("contact.html")

@app.route('/show')
def show():
    """
    The app route for the contact messages page, allowing you to show messages in the database,
    stored from the contact page.

    :return: :rtype: Returns the rendered show.html and the data that is to be shown.
    """
    all = db.get_messages(1)
    return render_template("show.html", data=all)



# Allows you to log out when youve been log in and redirects you to the startpage after doing so
@app.route('/logout')
def logout():
    """
    The app route for the logout page, that allows you to logout by pressing the list item in the navbar.

    :return: :rtype: Redirects you to the home page.
    """
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/admin_users', methods=['GET', 'POST'])
def admin_users():
    """
    An app route for the handling of the user that is to be promoted or removed.

    :return: :rtype: Returns the rendered template and the list of users
    and if an action has been done, a message will also be sent.
    """
    user_name = db.get_all_users()
    if request.method == 'POST':
        for x in user_name:
            if str(x[0]) in request.form:
                print str(x[0])
                message = handle_users(x[1], "promote")
                return render_template("admin_users.html", all_users=user_name, message=message)
            elif str(x[1]) in request.form:
                print str(x[1])
                message = handle_users(x[1], "remove")
                user_names = db.get_all_users()
                return render_template("admin_users.html", all_users=user_names, message=message)
    return render_template("admin_users.html", all_users=user_name)

#Plockar in namn, meddelande och email från contact html sidan och sänder dem vidare till sidan för att spara medelandet
# anropar även en funktion som lägger till informationen i våran databas
@app.route("/save_message", methods=['POST', 'GET'])
def save():
    """
    The app route for the save message page, adding information to the database inputted
    by the user, on the contact page.

    :return: :rtype: Returns a message and an url to get back to the contact page.
    """
    name = request.form['name']
    message = request.form['message']
    email = request.form['email']
    category=request.form['category']
    db.add_new_message(name, message, email, category)
    return "Thank you ""<a href='" + url_for("index") + "'> Back to Index</a>"

@app.route("/save_product", methods=['POST', 'GET'])
def saveproduct():
    """
    The app route for the save product page, adding information to the database inputted
    by the user, on the add product page.

    :return: :rtype: Returns a message and an url to get back to the add product page.
    """
    Product_ID = request.form['product_id']
    Product_Name = request.form['product_name']
    Price = request.form['price']
    Max_Size = request.form['max_size']
    Min_Size = request.form['min_size']
    Brand = request.form['brand']
    Category = request.form['category']
    Info = request.form['info']
    Classification = request.form['classification']
    Pic_URL = request.files['pic_url']
    # # Check if the file is one of the allowed types/extensions
    if Pic_URL and allowed_file(Pic_URL.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(Pic_URL.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        Pic_URL.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.add_new_product(Product_ID, Product_Name, Price, Max_Size, Min_Size, Brand, Category, Info, Classification, filename)
    return "Thank you <a href='" + url_for("add_product") + "'>Back to form</a>"





@app.route("/alter_product", methods=['POST', 'GET'])
def alterproduct():
    """
    The app route for the save product page, adding information to the database inputted
    by the user, on the add product page.

    :return: :rtype: Returns a message and an url to get back to the add product page.
    """
    product_id = request.form['product_id']
    product_name = request.form['product_name']
    price = request.form['price']
    max_size = request.form['max_size']
    min_size = request.form['min_size']
    brand = request.form['brand']
    category = request.form['category']
    info = request.form['info']
    classification = request.form['classification']
    filename = request.form['pic_url']
    db.alter_product(product_id, product_name, price, max_size, min_size, brand, category, info, classification, filename)
    return "Thank you <a href='" + url_for("index") + "'>Back to form</a>"


@app.route('/remove_product')
def remove_product():
    """
    The app route for the add product site.

    :return: :rtype: Returns the rendered remove product site.
    """
    return render_template("remove_product.html")

@app.route("/remove_product", methods=['POST', 'GET'])
def removeproduct():
    """
    The app route for the remove product page, for a product specified
    by the user, on the add product page.

    :return: :rtype: Returns a message and an url to get back to the remove product page.
    """
    Product_ID = request.form['product_id']
    db.remove_product(Product_ID)
    return "Thank you <a href='" + url_for("remove_product") + "'>Back to form</a>"


def handle_users(user_name, action):
    """
    A function to handle the promotion or removal of users through using functions
    in the database and handling the input parameters.

    :param user_name: The identification name of the user to handle.
    :param action: The action to be done to the user, either promote or remove.
    :return: :rtype: Returns a message of the preformed action.
    """
    if action == "promote":
        if not db.set_admin(user_name):
            message = user_name + " is already promoted"
        else:
            db.set_admin(user_name)
            message = user_name + " was promoted"
    else:
        if not db.remove_user(user_name):
            message = user_name + " was not found in the database"
        else:
            db.remove_user(user_name)
            message = user_name + " was removed"
    return message


@app.route("/save_offer", methods=['POST', 'GET'])
def saveoffer():
    """
    The app route for the save offer page, adding information to the database inputted
    by the user, on the add offer page.

    :return: :rtype: Returns a message and an url to get back to the add offer page.
    """
    url_to = request.form['url_to']
    pic_url = request.files['pic_url']
    # # Check if the file is one of the allowed types/extensions
    if pic_url and allowed_file(pic_url.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(pic_url.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        pic_url.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    db.add_new_offer(url_to, filename)
    return "Thank you <a href='" + url_for("add_offer") + "'>Back to form</a>"


@app.route('/add_to_cart', methods=['GET', 'POST'])
def add_to_cart():
    """
    adds selected item, with selected size and quantity, to the session which represents the cart.

    :return: url for products page
    """
    item = request.form['button']
    size = request.form['size']
    quantity = int(request.form['quantity'])
    for x in session['cart']:
        if x['item']==item or x['size']==size:
            x['quantity'] = quantity
            return redirect(url_for('product'))
    if quantity > 0:
        session['cart_length']+=1
        session['cart'].append({'item':item, 'cart_index':session['cart_length'],'quantity':quantity,'size':size, 'a_sizes':[]})
    return redirect(url_for('product'))


@app.route('/remove_from_cart', methods=['GET', 'POST'])
def remove_from_cart():
    """
    Removes selected item from the session representing the cart
    :return: url for list_cart which then shows the cart page
    """
    index = int(request.form['button'])
    for x in session['cart']:
        if index == int(x['cart_index']):
            session['cart'].remove(x)

    return redirect(url_for("list_cart"))

@app.route('/edit_post_in_cart', methods=['GET', 'POST'])
def edit_post_in_cart():
    """
    Edits the selected size and/or quantity of a item in the shopping cart in the session array.
    :return: returns the url for the cart which now is updated
    """
    index = int(request.form['button'])
    qtty = int(request.form['quantity'])
    size = request.form['size']
    print "in edit"
    print qtty

    for x in session['cart']:
        if int(x['cart_index']) == index:
            x['quantity'] = qtty
            x['size'] = size


    return redirect(url_for("list_cart"))

@app.route('/cart')
def list_cart():
    """
    gets all the information about the items in the session['cart'] array, from the database and sends them to the
    html page for the cart.
    :return: returns the entire session['cart'] array which describes whats in the cart and the url to the cart page.
    """
    cart_db = []
    sizes = []
    qttys = []
    index = []
    total = 0
    a_sizes = []

    for x in session['cart']:
        item = db.get_specific_product("product_id", x['item'],"")[0]
        cart_db.append(item)
        sizes.append(x['size'])
        qttys.append(x['quantity'])
        total += item[2] * x['quantity']
        index.append(x['cart_index'])

        if str(item[6]) == "Jacka" or str(item[6]) == "Jacket":
            sz = ["Small", "Medium", "Large", "XL", "XXL", "XXXL"]
        else:
            i = int(item[4])
            sz = []
            while i <= int(item[3]):
                sz.append(i)
                i += 1
        a_sizes.append(sz)
    print session['cart']
    return render_template("cart.html", data=cart_db, sizes=sizes, qttys=qttys, total=total, index=index,
                           a_sizes=a_sizes)

@app.route("/add_order", methods=['GET', 'POST'])
def add_order():
    """
    """
    date_placed = str(datetime.now())
    date_delivered = "29 / 05 / 1814"
    products = []
    for x in session['cart']:
        products.append([x['item'], x['size'], x['quantity']])
        db.add_new_order(db.get_user_id(session['username']), date_placed, date_delivered, products)
    session['cart'] = []
    return render_template("cart.html")


@app.route('/orders')
def orders():
    order_list = db.get_user_orders(db.get_user_id(session['username']))
    return render_template("orders.html", order_list=order_list)


@app.route('/orders/<name>')
def specorders(name):
    order_details = db.get_order_products(name)
    product_details = []
    for x in order_details:
        product_details.append(db.get_specific_product("product_id", str(x[1]))[0],"")
    return render_template("orderdetail.html",order_nr=order_details[0][0] ,order_details=zip(order_details,product_details))

# Implementera inte igen föränn vi skrivit in databasen som den är nu i db.py
#@app.route("/init_db")message
#def setup_db():
#Warning this method will remove all data from the database
#    db.setup()
#   return "Database created"

#Flask function that runs after each request used to close the database
@app.teardown_appcontext
def close_db(error):
    """
    Closes the database again at the end of the request.

    :param error: Parameter representing an error in the close down.
    """
    print ("Closing db")
    if hasattr(g, 'sqlite_db'):
        print "found it"
        g.sqlite_db.close()


if __name__ == '__main__':
    app.debug = True
    app.run()
