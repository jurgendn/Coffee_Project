from flask import render_template, Blueprint, request, redirect, current_app, make_response
from products.products_app import Products, Add_Product
import products.products_app as ppa
from flask_sqlalchemy import SQLAlchemy

products = Blueprint('products', __name__,
                     static_folder="static", template_folder="templates")


@products.route("/")
def products_page():
    return render_template('product.html', products=ppa.get_products())


@products.route("/edit", methods=["GET", "POST"])
def edit_products():
    form = Add_Product()
    prd_id = request.args.get("ProductID")
    prd = ppa.get_prd_by_id(prd_id)[0]
    prd_obj = Products(prd[0], prd[1], prd[2], int(
        prd[3]), int(prd[4]), prd[5], prd[6])
    resp = make_response(render_template(
        'product_spec.html', title="Edit Product", action="edit_prd", prd=prd_obj, form=form))
    resp.set_cookie("ProductID", prd_id, path='/', expires=60*60*24)
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
    order_num = len(ppa.get_prd_by_categories(cat=category))
    ID = id_dict[category] + str(order_num)
    new_product = Products(ID, name, category, price,
                           amount, brand, description)
    ppa.add_products(new_product)
    return redirect("/products/")


@products.route("/edit_prd", methods=["GET", "POST"])
def edit_prd():
    form = Add_Product(request.form)
    ID = request.cookies.get("ProductID")
    print(ID)
    name = form.name.data
    category = form.category.data
    price = form.price.data
    amount = form.amount.data
    brand = form.brand.data
    description = form.description.data
    new_product = Products(ID, name, category, price,
                           amount, brand, description)
    ppa.update_product(prd=new_product)
    return redirect("/products")


@products.route("/rm", methods=["GET", "POST"])
def remove_prd():
    ID = request.args.get("ProductID")
    ppa.remove(ID)
    return redirect("/products")
