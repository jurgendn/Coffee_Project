from datetime import datetime, date, timedelta, tzinfo, timezone
from math import inf
import os

from flask import render_template, Blueprint, request, redirect, current_app, make_response, session, url_for
from products.products_app import Products, Add_Product, Filter
import products.products_app as ppa
import warehouse.warehouse_app as ww

products = Blueprint('products', __name__,
                     static_folder="static", template_folder="templates")


@products.route("/", methods=["GET"])
def products_page():
    form = Filter()
    cat = request.args.get('category')
    lower = request.args.get('lower_bound')
    upper = request.args.get('upper_bound')
    if lower == '':
        lower = 0
    if upper == '':
        upper = inf

    return render_template('product.html', products=ppa.get_filter_prd(cat, lower, upper), form=form)


@products.route("/edit", methods=["GET", "POST"])
def edit_products():
    form = Add_Product()
    prd_id = request.args.get("ProductID")
    prd = ppa.get_prd_by_id(prd_id)[0]
    prd_obj = Products(prd[0], prd[1], prd[2], int(
        prd[3]), int(prd[4]), prd[5], prd[6], prd[7], prd[8])
    resp = make_response(render_template(
        'product_spec.html', title="Edit Product", action="edit_prd", prd=prd_obj, form=form))
    resp.set_cookie("ProductID", prd_id, path='/',
                    expires=datetime.now() + timedelta(minutes=70))
    session['checked_box'] = prd.lock
    return resp


@products.route("/new-product")
def add_products():
    form = Add_Product()
    return render_template("product_spec.html", title="Add Product", action="add_prd", prd=None, form=form)


@products.route("/add_prd", methods=["POST"])
def get_new_prd():
    id_dict = {'Coffee Machine': 'CM', 'Accessory': 'AS',
               'Raw Material': 'RW', 'Others': "OT"}
    form = Add_Product(request.form)
    name = form.name.data
    category = form.category.data
    price = form.price.data
    amount = form.amount.data
    brand = form.brand.data
    description = form.description.data
    # image = request.files[form.img.name]
    order_num = len(ppa.get_prd_by_categories(cat=category))
    ID = id_dict[category] + str(order_num)
    path = '/products/static/img/products/{}.jpeg'.format(ID)
    # try:
    #     f = open(path, "wb")
    # except:
    #     f = open(path, "xb")
    # f.write(image.read())
    # f.close()
    new_product = Products(ID, name, category, price,
                           amount, brand, description, path)
    ppa.add_products(new_product)
    ww.add_activity(ID, amount)
    return redirect("/products/?category=All&lower_bound=&upper_bound=&brand=&filt=Filter")


@products.route("/edit_prd", methods=["GET", "POST"])
def edit_prd():
    form = Add_Product(request.form)
    ID = request.cookies.get("ProductID")
    old_prd = ppa.get_prd_by_id(ID)[0]
    old_amount = old_prd[4]
    name = form.name.data
    category = form.category.data
    price = form.price.data
    amount = form.amount.data
    lock = 1 if form.lock.data == True else 0
    print(lock)
    if amount > old_amount:
        ww.add_activity(ID, amount - old_amount)
    brand = form.brand.data
    description = form.description.data
    image = request.files[form.img.name]
    path = '/products/static/img/products/{}.jpeg'.format(ID)
    # try:
    #     f = open(path, "w+b")
    # except:
    #     f = open(path, "x+b")
    # f.write(image.read())
    # f.close()
    new_product = Products(ID, name, category, price,
                           amount, brand, description, path, lock)
    ppa.update_product(prd=new_product)
    resp = make_response(redirect(
        "/products/?category=All&lower_bound=&upper_bound=&brand=&filt=Filter"))
    resp.delete_cookie("ProductID")
    return resp


@ products.route("/rm", methods=["GET", "POST"])
def remove_prd():
    ID = request.args.get("ProductID")
    ppa.remove(ID)
    return redirect("/products/?category=All&lower_bound=&upper_bound=&brand=&filt=Filter")
