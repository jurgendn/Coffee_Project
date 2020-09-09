from flask import Flask, Response, g, jsonify, render_template, url_for, redirect, session
from flask_login import LoginManager, UserMixin
from wtforms import Form, StringField

from products.products import products
from admin.admin_manage import admin_manage
from transaction.transaction import transaction

# ---------------------------------------------------------------
# Config app
# ---------------------------------------------------------------

app = Flask(__name__)
app.register_blueprint(products, url_prefix="/products")
app.register_blueprint(admin_manage, url_prefix="/admin")
app.register_blueprint(transaction, url_prefix="/transactions")

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
        return render_template("index.html")
    return redirect("/admin")


app.run(debug=True, port=5001)
