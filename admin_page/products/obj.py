from wtforms import Form, StringField, IntegerField, SelectField, SubmitField, validators, FileField, BooleanField
from wtforms.fields.html5 import IntegerRangeField, IntegerField
import products.products_app as ppa

# Forms


class Add_Product(Form):
    name = StringField("Name: ")
    category = SelectField("Category: ", choices=[('Coffee Machine', 'Coffee Machine'), (
        'Accessory', 'Accessory'), ('Raw Material', 'Raw Material'), ('Others', 'Others')])
    price = IntegerField("Price: ")
    amount = IntegerField("Amount")
    brand = StringField("Brand: ")
    description = StringField("Description: ")
    img = FileField("Add Photo")
    lock = BooleanField("Lock")
    save = SubmitField("Save")


class Filter(Form):
    keyword = StringField('Keywords')
    category = SelectField("Category: ", choices=[('All', 'All'), ('Coffee Machine', 'Coffee Machine'), (
        'Accessory', 'Accessory'), ('Raw Material', 'Raw Material'), ('Others', 'Others'), ])
    lower_bound = IntegerField("From: ")
    upper_bound = IntegerField("To: ")
    filt = SubmitField("Filter")


# Products
class Products:

    def __init__(self, ID, name, category, price, amount, brand, description, prd_img, lock):
        self.ID = ID
        self.name = name
        self.category = category
        self.price = price
        self.amount = amount
        self.brand = brand
        self.description = description
        self.linkimg = prd_img
        self.lock = lock
