import sqlite3

import click
from flask import Flask, current_app, g, jsonify, render_template

app = Flask(__name__)
app.debug = True


class Customer:
    def __init__(self, ID, name, phone, mail):
        self.ID = ID
        self.name = name
        self.phone = phone
        self.mail = mail


class Products:
    def __init__(self, ID, name, price, amount):
        self.ID = ID
        self.name = name
        self.price = price
        self.amount = amount


conn = sqlite3.connect("DB.db")

c = conn.execute("SELECT * FROM CUSTOMER")
data = c.fetchall()
data_customers = [Customer(t[0], t[1], t[2], t[3]) for t in data]

p = conn.execute("SELECT * FROM PRODUCTS")
data_product = p.fetchall()
print(data_product)
products = [Products(t[0], t[1], t[2], t[3]) for t in data_product]


@app.route("/")
def homepage():
    name = "Jurgen"
    if name == "Jurgen":
        return render_template('base.html', username=name)
    else:
        return render_template('base.html', username="guest")


@app.route('/dash')
def dashboard():
    return render_template('index.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/products")
def get_products():
    return render_template("product.html", products=products)


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/dataTable", methods=['POST'])
def dataTable():
    ret = ""
    for entry in "SELECT * FROM CUSTOMER":
        ret += 'id="{0}" name="{1}" phone = "{2}" mail = "{3}" >{entry.id} {entry.name} {entry.phone} {entry.mail}'.format(
            entry)
    return ret


app.run()
