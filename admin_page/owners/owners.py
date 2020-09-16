from flask import Blueprint, redirect, render_template, url_for, make_response, request
from werkzeug.security import generate_password_hash
import owners.app as oa
from admin.admin import AdminInfo

owners = Blueprint('owners', __name__, static_folder='static',
                   template_folder='templates')


@owners.route('/')
def owners_home():
    adm = oa.get_all_admin()
    return render_template('admin_list.html', admins=adm)


@owners.route("edit_admin_permission", methods=['GET'])
def change_permission():
    parameters = request.args.get('permission')
    parameters = parameters.split("_")
    print(parameters)
    oa.update_admin(int(parameters[1]), parameters[0])
    return redirect("/owners")


@owners.route("new_admin")
def new_admin():
    form = AdminInfo()
    return render_template("add_admin.html", form=form)


@owners.route("add_admin", methods=['GET'])
def add_admin():
    name = request.args.get('name')
    email = request.args.get('email')
    phone = request.args.get('phone')
    address = request.args.get("address")
    permission = "Manager"
    passwd = generate_password_hash('1', method='sha256')
    avatar = ''
    adm = [name, passwd, avatar, address, phone, email, permission]
    oa.add_admin(adm)
    return redirect("/owners")
