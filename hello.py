import sqlite3

import click
from flask import Flask, current_app, g, jsonify, render_template
from flask.cli import with_appcontext

app = Flask(__name__)


class Customer:
    def __init__(self, ID, name, phone, mail):
        self.ID = ID
        self.name = name
        self.phone = phone
        self.mail = mail


g = sqlite3.connect("DB.db")
c = g.execute("SELECT * FROM CUSTOMER")
data = c.fetchall()
print(data[0])

customers = [Customer(t[0], t[1], t[2], t[3]) for t in data]


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
def products():
    return render_template("product.html", products=customers)


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