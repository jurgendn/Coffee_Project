import os

from flask import (Flask, Response, g, jsonify, redirect, render_template,
                   session, url_for, flash)
from flask_login import LoginManager, UserMixin
from wtforms import Form, StringField

from admin.admin_manage import admin_manage
from products.products import products
from transaction.transaction import transaction
from warehouse.warehouse import warehouse
from dashboard.dashboard import dashboard

# ---------------------------------------------------------------
# Config app
# ---------------------------------------------------------------

app = Flask(__name__)
app.register_blueprint(products, url_prefix="/products")
app.register_blueprint(admin_manage, url_prefix="/admin")
app.register_blueprint(transaction, url_prefix="/transactions")
app.register_blueprint(warehouse, url_prefix="/warehouse")
app.register_blueprint(dashboard, url_prefix="/dashboard")

app.secret_key = 'dungcohoikhongladamday'

# ---------------------------------------------------------------


def check_for_existing_admin():
    try:
        _ = session["email"]
        return True
    except:
        return False


@app.route("/")
def homepage():
    if check_for_existing_admin():
        flash("Successfully")
        return redirect("/dashboard")
    return redirect("/admin/login")


app.run(debug=True, port=5003)
