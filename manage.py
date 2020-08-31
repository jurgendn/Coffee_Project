from flask import Flask, render_template, jsonify, Response, url_for, g
from flask_sqlalchemy import SQLAlchemy
from admin.admin_manage import admin_manage
from products.products import products

app = Flask(__name__)
app.register_blueprint(admin_manage, url_prefix="/admin")
app.register_blueprint(products, url_prefix="/products")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DB.db'

@app.route("/")
def homepage():
    return render_template('index.html')

app.run(debug=True)