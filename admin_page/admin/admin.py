from wtforms import Form, StringField, PasswordField, SubmitField, FileField
from wtforms.fields.html5 import EmailField

from sqlalchemy import create_engine, Table, MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

database = "sqlite:///./DB.db"


class LoginForm(Form):
    username = StringField('Username')
    passwd = PasswordField("Password")
    submit = SubmitField('Login')


class Admin:
    def __init__(self, ID, name, passwd, avatar, address, phone, email, permission):
        self.ID = ID
        self.name = name
        self.passwd = passwd
        self.address = address
        self.phone = phone
        self.email = email
        self.avatar = 'static/img/avatars/' + avatar
        self.permission = permission


class AdminInfo(Form):
    name = StringField("Employee name")
    address = StringField("Address")
    phone = StringField("Phone Number")
    email = EmailField("Email")


class ChangePasswd(Form):
    old_password = PasswordField("Old Password")
    new_password = PasswordField("New Password")
    confirm_passwd = PasswordField("Confirm Password")


class UploadAvt(Form):
    uploader = FileField("Chooose File")
    save = SubmitField("Save Change")

# Database


def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Admin_Table = Table('ADMIN', metadata, autoload=True)
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
    return Admin(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7])


def is_valid_admin(email, passwd):
    adm = get_admin_info(email)
    return True if check_password_hash(adm.passwd, passwd) else False


def log_out(email):
    session.pop('email')
    session.pop('permission_type')
    return True


def change_profile_image(email):
    engine, conn, Admin_Table = connect_db()
    try:
        Admin_Table.update(
            whereclause=Admin_Table.c.email == email).values(avatar=email[:-4]+'.jpeg').execute()
    except:
        close_db(engine, conn)
        print("Invalid")
    close_db(engine, conn)


def update_info(name, email, phone, address):
    engine, conn, Adm = connect_db()
    Adm.update(whereclause=Adm.c.email == email).values(
        name=name, email=email, phone=phone, address=address).execute()
    close_db(engine, conn)


def update_passwd(email, old_pass, new_pass, confirm_pass):
    admin = get_admin_info(session['email'])
    print(check_password_hash(admin.passwd, old_pass))
    if not check_password_hash(admin.passwd, old_pass):
        print(check_password_hash(admin.passwd, old_pass))
        return False
    if new_pass != confirm_pass:
        return False
    engine, conn, Adm = connect_db()
    Adm.update(whereclause=Adm.c.email == email).values(
        passwd=generate_password_hash(new_pass, method='sha256')).execute()
    close_db(engine, conn)
    return True
