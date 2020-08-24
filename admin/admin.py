from wtforms import Form, StringField, PasswordField, SubmitField, validators

class LoginForm(Form):
    username = StringField("Username", [validators.Length(min=6, max=20)])
    password = PasswordField("Password", [validators.Length(min=6, max=30), validators.DataRequired()])
    submit = SubmitField("Log In")

class Admin:
    def __init__(self, ID, name, dob, phone, email, address):
        self.ID = ID
        self.name = name
        self.dob = dob
        self.phone = phone
        self.email = email
        self.address = address
    

