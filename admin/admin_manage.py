from flask import Blueprint, render_template
from admin.admin import Admin

admin_manage = Blueprint("admin_manage",__name__,
                         static_folder='static', template_folder='templates')


@admin_manage.route("/")
def admin_homepage():
    return render_template('admin.html')
