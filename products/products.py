from flask import render_template, Blueprint, request, redirect, current_app
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
    return render_template('product_spec.html', title="Edit Product", form=form)


@products.route("/new-product")
def add_products():
    form = Add_Product()
    return render_template("product_spec.html", title="Add Product", form=form)


@products.route("/asb", methods=["POST"])
def get_new_prd():
    order_num = len(ppa.get_products())
    engine, conn = ppa.connect_db()
    id_dict = {'Coffee Machine': 'CM', 'Accessory': 'AS',
               'Raw Material': 'RW', 'Others': "OT"}
    form = Add_Product(request.form)
    name = form.name.data
    category = form.category.data
    price = form.price.data
    amount = form.amount.data
    brand = form.brand.data
    description = form.description.data
    print(order_num)
    ID = id_dict[category] + str(order_num)
    new_product = Products(ID, name, category, price,
                           amount, brand, description)
    ppa.add_products(new_product)
    ppa.close_db(engine, conn)
    return redirect("/products/")
