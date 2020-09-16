import sqlite3

import click
from flask import Flask, current_app, g, jsonify, render_template
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine
from wtforms import Form, PasswordField, StringField, SubmitField, validators

app = Flask(__name__)
app.debug = True

query = "INSERT INTO PRODUCTS (ID, name, price, amount, brand, description) VALUES ('MC01', 'Máy pha cà phê Võ Đang', 4500000, 8, 'Võ Đang', 'Tuyệt đỉnh võ học')"

engine = create_engine("sqlite:///DB.db")
conn = engine.connect()
re = conn.execute(query)
conn.close()
engine.dispose()
print(re)


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=20)])
    passwd = PasswordField('Password', [validators.Length(min=8, max=40)])
    submit = SubmitField('Submit')


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


@app.route('/')
def dashboard():
    return render_template('index.html')


@app.route("/edit")
def edit():
    return render_template('product_spec.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route("/products")
def get_products():
    return render_template("product.html")


@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)


@app.route("/dataTable", methods=['POST'])
def dataTable():
    ret = ""
    for entry in "SELECT * FROM CUSTOMER":
        ret += 'id="{0}" name="{1}" phone = "{2}" mail = "{3}" >{entry.id} {entry.name} {entry.phone} {entry.mail}'.format(
            entry)
    return ret


app.run()
