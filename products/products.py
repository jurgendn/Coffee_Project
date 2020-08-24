from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from flask import Flask, render_template

app = Flask(__name__)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class Products:
    def __init__(self, ID, name, phone, email, address):
        self.ID = ID
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address


app.route("/login", method=['POST'])


def log():
    form = LoginForm()
    return render_template('login.html', form=form)


app.run()
