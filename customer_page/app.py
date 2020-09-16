from flask import Flask, render_template, redirect, url_for, request, g, session, flash
import sqlite3 as sql
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from flask_login import login_user, logout_user, login_required
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime
from flask_mail import Mail, Message
import numpy as np
db = SQLAlchemy()

app = Flask(__name__)
mail = Mail(app)

app.config['SECRET_KEY'] = 'thisismysecretkeydonotstealit'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../DB.db'

db.init_app(app)
UPLOAD_FOLDER = './static/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_manager = LoginManager()
login_manager.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'thuchanhtin20173005@gmail.com'
app.config['MAIL_PASSWORD'] = '20173005tt'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

"""
    Tạo các bảng trong cơ sở dữ liệu: có 4 bảng user, products, kart và complete với:
    + user lưu thông tin người dùng
    + products lưu thông tin của sản phẩm
    + kart lưu thông tin giỏ hàng
    + complete lưu thông tin giao dịch của người dùng
"""


class User(UserMixin, db.Model):
    __tablename__ = 'CUSTOMER'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(1000))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    avatar = db.Column(db.String(100))
    phone = db.Column(db.String(20))


class Products(db.Model):
    __tablename__ = 'PRODUCTS'
    ID = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(1000))
    linkimg = db.Column(db.String(100))
    category = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    brand = db.Column(db.String(100))


class Kart(db.Model):
    __tablename__ = 'CART'
    cartID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer)
    ID = db.Column(db.String(100))
    amounts = db.Column(db.Integer)
    time = db.Column(db.String(100))


class Complete(db.Model):
    __tablename__ = 'TRANSACTION'
    ID = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(1000))
    product_list = db.Column(db.String(100))
    total = db.Column(db.Integer)
    date = db.Column(db.String(100))
    address = db.Column(db.String(1000))
    method = db.Column(db.String(100))


class Count_Visit(db.Model):
    __tablename__ = 'COUNT_VISIT'
    date_visit = db.Column(db.String(100), primary_key=True)
    web_home = db.Column(db.Integer)
    web_about = db.Column(db.Integer)
    web_store = db.Column(db.Integer)
    web_booking = db.Column(db.Integer)
    web_coffeesraw = db.Column(db.Integer)
    web_machinery = db.Column(db.Integer)

# set up để sau khi đăng nhập load được thông tin người dùng


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# set up trang chủ, tùy thuộc vào trạng thái là có người dùng hay không để hiện thị


@app.route('/')
def home():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=1, web_about=0,
                                web_store=0, web_booking=0, web_coffeesraw=0, web_machinery=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_home = check.web_home + 1
        db.session.commit()
    if current_user.get_id():
        return render_template("index.html", user=current_user)
    else:
        return render_template("index.html")
# set up trang About


@app.route('/about')
def about():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0, web_about=1,
                                web_store=0, web_booking=0, web_coffeesraw=0, web_machinery=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_about = check.web_about + 1
        db.session.commit()
    return render_template('about.html')

# set up trang about/sales


@app.route('/about/sales')
def sales():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0, web_about=1,
                                web_store=0, web_booking=0, web_coffeesraw=0, web_machinery=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_about = check.web_about + 1
        db.session.commit()
    return render_template('sales.html')

# set up tang about/history


@app.route('/about/history')
def history():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0, web_about=1,
                                web_store=0, web_booking=0, web_coffeesraw=0, web_machinery=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_about = check.web_about + 1
        db.session.commit()
    return render_template('history.html')

# set up trang products


@app.route('/products')
def products():
    if current_user.get_id():
        return render_template("products.html", user=current_user)
    else:
        return render_template("products.html")

# set up trang product_coffees với những sản phẩm mà có ID có RW thì sẽ được hiển thị


@app.route('/products/product_coffees', methods=['GET', 'POST'])
def coffees():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0, web_about=0,
                                web_store=0, web_booking=0, web_coffeesraw=1, web_machinery=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_coffeesraw = check.web_coffeesraw + 1
        db.session.commit()
    if request.method == 'GET':
        products = Products.query.all()
        lst_products = []
        for product in products:
            if "RW" in product.ID:
                lst_products.append(product)
        return render_template('product_coffees.html', products=lst_products, user=current_user.get_id(), search=True)
    else:
        session['search'] = request.form['search']
        category = request.form.get('Category')
        session['search_category'] = str(category)
        session['search_price'] = str(request.form.get('Price'))
        return redirect("/products/product_coffees/search?searchkey="+session['search']+'&'+session['search_category']+'&'+session['search_price'])


"""set up ứng dụng search cho trang product_coffees, trước hết là hiển thị ra các sản phẩm coffees trước,
rồi sau đó mới search, với input mà thuộc ID hoặc name of product thì sẽ hiển thị ra còn nếu không sản phầm
đó sẽ không được hiển thị"""


@app.route('/products/product_coffees/search')
def search():
    if 1 > 0:
        products = Products.query.all()
        lst_products = []
        for product in products:
            if "RW" in product.ID:
                lst_products.append(product)

        lst_products_finish = []
        input_search = session['search']
        if len(input_search) > 0:
            for product in lst_products:
                if (input_search in product.ID) or (input_search in product.name):
                    lst_products_finish.append(product)
        else:
            lst_products_finish = lst_products
        search_category = session['search_category']
        #print("len sau lan 1",len(lst_products_finish))
        # print("search_category",search_category)
        filter_product2 = []
        search_price = session['search_price']
        if search_category != "All":
            for product in lst_products_finish:
                if product.category == search_category:
                    filter_product2.append(product)
        else:
            filter_product2 = lst_products_finish
        # print("len(filter_product2)",len(filter_product2))
        finish_product_sure = []
        if search_price == "max 50k":
            for product in filter_product2:
                if int(product.price) < 50000:
                    finish_product_sure.append(product)
        if search_price == "50k 100k":
            for product in filter_product2:
                if 50000 <= int(product.price) < 100000:
                    finish_product_sure.append(product)
        if search_price == "more 100k":
            for product in filter_product2:
                if int(product.price) > 100000:
                    finish_product_sure.append(product)
        if search_price == "All":
            finish_product_sure = filter_product2
        if len(finish_product_sure) == 0:
            flash('Not Found!')
        else:
            if len(input_search) == 0:
                input_search = "Invalid"
            flash('Category: '+search_category+'--- Price: ' +
                  search_price+'--- More feature: '+input_search)
        return render_template('product_coffees.html', products=finish_product_sure, user=current_user.get_id(), search=False)

# Trình bày nhiều thông tin hơn về sản phẩm


@app.route('/productDescription', methods=['GET', 'POST'])
def productDescription():
    ID = request.args.get('ID')
    product = Products.query.filter_by(ID=ID).first()
    if request.method == 'GET':
        session['ID'] = ID
        return render_template("productDescription.html", product=product, user=current_user.get_id())
    else:
        amount = request.form['number']
        checkamount = Products.query.filter_by(ID=session['ID']).first()
        if int(amount) > int(checkamount.amount):
            flash('Insufficient.')
            return redirect("/productDescription?ID="+session['ID'])
        vari1 = checkamount.amount
        temp = int(vari1)-int(amount)
        checkamount.amount = str(temp)
        db.session.commit()
        ID = session['ID']
        if current_user.get_id():
            return redirect(url_for('addToCart', lst=str(amount)+'&'+str(ID)))
        else:
            flash("Please login first")
            return redirect("/productDescription?ID="+session['ID'])

# Cho sản phẩm vào giỏ hàng


@app.route("/addToCart")
def addToCart():
    a = request.args.get('lst')
    lst = a.split('&')
    ID = lst[1]
    number = int(lst[0])
    time = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
    new_kart = Kart(userID=current_user.get_id(),
                    ID=ID, amounts=number, time=time)
    db.session.add(new_kart)
    db.session.commit()
    return redirect(url_for('cart'))

# set up trang Mycart bao gồm những products mà user đã chọn trong session này


@app.route('/MyCart', methods=['GET', 'POST'])  # chinhs la cai /cart ben kia
@login_required
def cart():
    all_receipt = Kart.query.filter_by(userID=current_user.get_id()).with_entities(
        Kart.ID, Kart.amounts, Kart.time, Kart.cartID).all()  # choose all rows have userID=currentID???/
    lst_productsID = []
    lst_time = []
    lst_cartID = []
    for i in range(len(all_receipt)):
        lst_productsID.append(all_receipt[i][0])
        lst_time.append(all_receipt[i][2])
        lst_cartID.append(all_receipt[i][3])
    session['cartIDs'] = lst_cartID
    lst_products = []
    lst_amounts = []
    for i in range(len(all_receipt)):
        lst_amounts.append(all_receipt[i][1])
    print("lst_amounts", lst_amounts)
    session['amount'] = lst_amounts
    total = 0
    for i in range(len(lst_productsID)):
        a = Products.query.filter_by(ID=lst_productsID[i]).first()
        lst_products.append(a)
        total = total + a.price*lst_amounts[i]
    if request.method == 'GET':
        return render_template('cart.html', products=lst_products, totalPrice=total, amounts=lst_amounts, rang=len(lst_amounts), times=lst_time, cartIDs=lst_cartID)
    else:
        session['total'] = total
        print("total là:", total)
        lst_productnames = []
        session['ID'] = lst_productsID
        for product in lst_products:
            lst_productnames.append(product.name)
        session['products_name'] = lst_productnames
        session['date'] = datetime.datetime.now().strftime("%y-%m-%d %H:%M:%S")
        session['address'] = request.form['add']
        method = request.form.get('method')
        session['method'] = str(method)
        return redirect(url_for('complete'))

# Bước hoàn thành giao dịch, với bước này thì sẽ thêm record vào table "complete" đồng thời xóa hết hàng hóa của user
# đó tại table kart


@app.route('/complete')
def complete():
    add = session['address']
    lst_sanpham = ''
    method = session['method']
    for i in range(len(session['products_name'])):
        lst_sanpham = lst_sanpham + \
            session['ID'][i]+':' + str(session['amount'][i])+';'
    if len(lst_sanpham) == 0:
        flash('Your cart do not have any products. Please add something to continue.')
        return redirect(url_for('cart'))
    new_com = Complete(ID="{}_{}".format(current_user.get_id(), session['date']), user_id=current_user.get_id(
    ), product_list=lst_sanpham, total=session['total'], date=session['date'], address=add, method=method)
    db.session.add(new_com)
    db.session.commit()
    for cartID in session['cartIDs']:
        Kart.query.filter_by(cartID=cartID).delete()
        db.session.commit()
    if method == "Credit":
        flash("Your ID Cart is "+str(new_com.ID) +
              ". We will send you products as soon as possible when receive money.")
    return redirect(url_for('home'))

# BỎ product trong giỏ hàng


@app.route('/remove')
def remove():
    cartID = request.args.get('cartID')
    temp = Kart.query.filter_by(cartID=cartID).first()
    add_amount = Products.query.filter_by(ID=temp.ID).first()
    add_amount.amount = str(int(add_amount.amount)+int(temp.amounts))
    Kart.query.filter_by(cartID=cartID).delete()
    db.session.commit()
    return redirect(url_for('cart'))

# Tương tự với products/product_coffee


@app.route('/products/raw_materials', methods=['GET', 'POST'])
def raw_materials():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0, web_about=0,
                                web_store=0, web_booking=0, web_coffeesraw=0, web_machinery=1)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_machinery = check.web_machinery + 1
        db.session.commit()
    if request.method == 'GET':
        products = Products.query.all()
        lst_products = []
        for product in products:
            if "CM" in product.ID or "AS" in product.ID:
                lst_products.append(product)
        return render_template('raw_materials.html', products=lst_products, user=current_user.get_id(), search=True)
    else:
        session['search_machinery'] = request.form['search']
        session['machinery_category'] = str(request.form.get('Category'))
        session['machinery_price'] = str(request.form.get('Price'))
        return redirect('/products/raw_materials/search?searchkey='+session['search_machinery']+'&'+session['machinery_category']+'&'+session['machinery_price'])


@app.route('/products/raw_materials/search')
def search1():
    if 1 > 0:
        products = Products.query.all()
        lst_products = []
        for product in products:
            if "CM" in product.ID or "AS" in product.ID:
                lst_products.append(product)
        lst_products_finish = []
        input_search = session['search_machinery']
        if len(input_search) > 0:
            for product in lst_products:
                if (input_search in product.ID) or (input_search in product.name):
                    lst_products_finish.append(product)
        else:
            lst_products_finish = lst_products
        search_category = session['machinery_category']
        #print("len sau lan 1",len(lst_products_finish))
        # print("search_category",search_category)
        filter_product2 = []
        search_price = session['machinery_price']
        if search_category != "All":
            for product in lst_products_finish:
                if product.category == search_category:
                    filter_product2.append(product)
        else:
            filter_product2 = lst_products_finish
        # print("len(filter_product2)",len(filter_product2))
        finish_product_sure = []
        if search_price == "max 50k":
            for product in filter_product2:
                if int(product.price) < 50000:
                    finish_product_sure.append(product)
        if search_price == "50k 100k":
            for product in filter_product2:
                if 50000 <= int(product.price) < 100000:
                    finish_product_sure.append(product)
        if search_price == "more 100k":
            for product in filter_product2:
                if int(product.price) > 100000:
                    finish_product_sure.append(product)
        if search_price == "All":
            finish_product_sure = filter_product2
        if len(finish_product_sure) == 0:
            flash('Not find products you want to search.')
        else:
            if len(input_search) == 0:
                input_search = "You not fill"
            flash('Category: '+search_category+'--- Price: ' +
                  search_price+'--- More feature: '+input_search)
        return render_template('raw_materials.html', products=finish_product_sure, user=current_user.get_id(), search=False)

# set up trang booking


@app.route('/products/booking')
def booking():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0,
                                web_about=0, web_store=0, web_booking=1, web_coffeesraw=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_booking = check.web_booking + 1
        db.session.commit()
    if current_user.get_id():
        return render_template('booking.html', user=current_user)
    else:
        return render_template('booking.html')

# set up trang store


@app.route('/store')
def store():
    time = datetime.datetime.now().strftime("%y-%m-%d")
    check = Count_Visit.query.filter_by(date_visit=time).first()
    if check is None:
        new_count = Count_Visit(date_visit=time, web_home=0,
                                web_about=0, web_store=1, web_booking=0, web_coffeesraw=0)
        db.session.add(new_count)
        db.session.commit()
    else:
        check.web_store = check.web_store + 1
        db.session.commit()
    return render_template('store.html')

# set up trang myaccount


@app.route('/myaccount')
@login_required
def myaccount():
    return render_template('myaccount.html', user=current_user)

# show mọi giao dịch của khách hàng


@app.route('/alldeal')
def alldeal():
    lst_deal = Complete.query.filter_by(user_id=current_user.get_id()).with_entities(
        Complete.ID, Complete.user_id, Complete.product_list, Complete.total, Complete.date, Complete.address, Complete.method).all()
    print("lst_deal:", lst_deal)
    return render_template("all_deal.html", alldeal=lst_deal)


# hàm check sự hợp lệ của file
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# set up trang edit_profile tức sửa trang cá nhân


@app.route("/edit_profile", methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        phone = request.form['phonenumber']
        if request.files:
            file = request.files['image']
            if file.filename == '' and len(phone) > 0:
                edituser = User.query.filter_by(
                    id=current_user.get_id()).first()
                edituser.phone = phone
                db.session.commit()
                return redirect(url_for('myaccount', user=current_user))
            if file.filename == '' and len(phone) == 0:
                flash('Please make input to update phone or image.')
                return redirect(url_for('edit'))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                edituser = User.query.filter_by(
                    id=current_user.get_id()).first()
                new_filename = 'img/'+str(filename)
                edituser.avatar = url_for('static', filename=new_filename)
                if len(phone) > 0:
                    edituser.phone = phone
                db.session.commit()
                return redirect(url_for('myaccount', user=current_user))
        else:
            return redirect(url_for('about'))

    return render_template('edit.html')

# change password


@app.route('/changepass', methods=['GET', 'POST'])
def changepass():
    if request.method == 'POST':
        currentpass = request.form['currentpass']
        newpass = request.form['newpass']
        checkpass = request.form['checkpass']
        real_user = User.query.filter_by(id=current_user.get_id()).first()
        realpass = real_user.password
        if not check_password_hash(realpass, currentpass):
            flash('Please check your current password.')
            return redirect(url_for('changepass'))
        if len(newpass) == 0:
            flash('You need to write new password.')
            return redirect(url_for('changepass'))
        if not newpass == checkpass:
            flash('Please write the new password again carefully.')
            return redirect(url_for('changepass'))
        real_user.password = generate_password_hash(newpass, method='sha256')
        db.session.commit()
        return redirect(url_for('myaccount', user=current_user))
    else:
        return render_template('changepass.html')


# login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if request.form.get('chooseremember'):
            remember = True
        else:
            remember = False
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))

        login_user(user, remember=remember)

        return redirect(url_for('home'))
    else:
        return render_template('log in.html')

# register new account


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        phone = request.form['phone']
        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists. Please choose another.')
            return redirect(url_for('signup'))
        if password != request.form["password-repeat"]:
            flash('New password which you write again different with new password.')
            return redirect(url_for('signup'))
        if not request.form.getlist('agree'):
            flash('You need to agree my licence to register new account.')
            return redirect(url_for('signup'))
        if not phone.isnumeric():
            flash('Phone number only consist of numberic characters.')
            return redirect(url_for('signup'))
        msg = Message(
            'Hello', sender='thuchanhtin20173005@gmail.com', recipients=[email])
        code_confirm = np.random.randint(1000, 9999)
        session['code_confirm'] = str(code_confirm)
        msg.body = "Hello Flask message sent from Flask-Mail. Your code is " + \
            str(code_confirm)
        mail.send(msg)
        session['emailregister'] = email
        session['nameregister'] = name
        session['passwordregister'] = password
        session['phoneregister'] = phone
        return redirect(url_for('confirm'))
    else:
        return render_template('register.html')

# sau khi đăng kí thì user cần nhập mã xác thực để có thể đăng kí thành công tài khoản


@app.route('/cofirmemail', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        if request.form['yourcode'] == session['code_confirm']:
            print("code nhap vao:", request.form['yourcode'])
            email = session['emailregister']
            name = session['nameregister']
            password = session['passwordregister']
            phone = session['phoneregister']
            new_user = User(email=email, name=name, password=generate_password_hash(
                password, method='sha256'), avatar=url_for('static', filename='img/bg.jpg'), phone=phone)
            db.session.add(new_user)
            db.session.commit()
            flash('Now you can log in with account you just register.')
            return redirect(url_for('login'))
        else:
            flash('Code not true. Please check your email again.')
            return redirect(url_for('confirm'))
    else:
        flash('We sent to you your code, please check your email and fill in this box.')
        return render_template('confirm.html')

# log out account


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
