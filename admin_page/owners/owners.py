from flask import Blueprint, redirect, render_template, url_for, make_response, request
import owners.app as oa

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
