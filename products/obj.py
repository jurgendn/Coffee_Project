from wtforms import Form, StringField, IntegerField, SelectField, SubmitField, validators
from wtforms.fields.html5 import IntegerRangeField

### Forms

class Add_Product(Form):
    name = StringField("Name: ")
    category = SelectField("Category: ", choices=[('Coffee Machine', 'Coffee Machine'), (
        'Accessory', 'Accessory'), ('Raw Material', 'Raw Material'), ('Others', 'Others')])
    price = IntegerField("Price: ")
    amount = IntegerRangeField("Amount: ", [validators.NumberRange(min=0)])
    brand = StringField("Brand: ")
    description = StringField("Description: ")
    save = SubmitField("Save")
    cancel = SubmitField("Cancel")


class Filter(Form):
    keyword = StringField('Keywords')
    category = SelectField("Category: ", choices=[('Coffee Machine', 'Coffee Machine'), (
        'Accessory', 'Accessory'), ('Raw Material', 'Raw Material'), ('Others', 'Others'), ('All', 'All')])
    price = IntegerField("Price: ")
    brand = StringField("Brand: ")
    filt = SubmitField("Filter")

### Products

class Products:

    def __init__(self, ID, name, category, price, amount, brand, description):
        self.ID = ID
        self.name = name
        self.category = category
        self.price = price
        self.amount = amount
        self.brand = brand
        self.description = description