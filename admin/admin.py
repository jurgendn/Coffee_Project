from wtforms import Form, StringField, PasswordField, SubmitField

from sqlalchemy import create_engine, Table, MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

database = "sqlite:///DB.db"


class LoginForm(Form):
    username = StringField('Username')
    passwd = PasswordField("Password")
    submit = SubmitField('Login')


class Admin:
    def __init__(self, ID, name, passwd, address, phone, email):
        self.ID = ID
        self.name = name
        self.passwd = passwd
        self.address = address
        self.phone = phone
        self.email = email

# Database


def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Admin_Table = Table('Admin', metadata, autoload=True)
    return engine, conn, Admin_Table


def close_db(engine, conn):
    conn.close()
    engine.dispose()


def get_admin_info(email):
    engine, conn, Admin_Table = connect_db()
    try:
        info = Admin_Table.select(
            whereclause=Admin_Table.c.email == email).execute().fetchall()[0]
    except:
        close_db(engine, conn)
        return "Invalid"
    close_db(engine, conn)
    return Admin(info[0], info[1], info[2], info[3], info[4], info[5])


def is_valid_admin(email, passwd):
    adm = get_admin_info(email)
    return True if check_password_hash(adm.passwd, passwd) else False


def log_out(email):
    session.pop('email')
