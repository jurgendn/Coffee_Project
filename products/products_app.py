from sqlalchemy import create_engine, Table
from wtforms import Form, StringField, IntegerField, SelectField, SubmitField, validators
from wtforms.fields.html5 import IntegerRangeField

database = "sqlite:///DB.db"

class Add_Product(Form):
    name = StringField("Name: ")
    category = SelectField("Category: ",choices=[('Coffee Machine', 'Coffee Machine'), ('Accessory', 'Accessory'), ('Raw Material', 'Raw Material'), ('Others', 'Others')])
    price = IntegerField("Price: ")
    amount = IntegerRangeField("Amount: ", [validators.NumberRange(min=0)])
    brand = StringField("Brand: ")
    description = StringField("Description: ")
    save = SubmitField("Save")
    cancel = SubmitField("Cancel")

class Products:
    
    def __init__(self, ID, name, category, price, amount, brand, description):
        self.ID = ID
        self.name = name
        self.category = category
        self.price = price
        self.amount = amount
        self.brand = brand
        self.description = description


def connect_db():
    engine = create_engine(database)
    return engine, engine.connect()


def close_db(engine, conn):
    conn.close()
    engine.dispose()


def get_database():
    engine, conn= connect_db()
    dt = conn.execute("SELECT * FROM PRODUCTS")
    product_db = dt.fetchall()
    close_db(engine, conn)    
    return product_db

def get_products():
    product_db = get_database()
    product_list = []
    for prd in product_db:
        product_list.append(Products(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6]))
    return product_list

def add_products(prd):
    engine, conn = connect_db()
    query = "INSERT INTO PRODUCTS (ID, name, category, price, amount, brand, description) VALUES ('{}','{}','{}',{},{},'{}','{}')".format(prd.ID, prd.name, prd.category, prd.price, prd.amount, prd.brand, prd.description)
    conn.execute(query)
    close_db(engine, conn)