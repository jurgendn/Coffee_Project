from flask import Blueprint, render_template, redirect, request, make_response, session, flash
from admin.admin import Admin, LoginForm
import admin.admin as ad

admin_manage = Blueprint("admin_manage", __name__,
                         static_folder='static', template_folder='templates')


@admin_manage.route("/")
def admin_homepage():
    form = LoginForm()
    print(ad.generate_password_hash('122', method='sha256'))
    return render_template("login.html", form=form)


@admin_manage.route("/login_info", methods=["GET", "POST"])
def get_login_info():
    form = LoginForm(request.form)
    email = form.username.data
    passwd = form.passwd.data
    adm = ad.get_admin_info(email)
    if ad.is_valid_admin(email, passwd):
        session['email'] = email
        resp = make_response(redirect("/"))
        resp.set_cookie('usrname', adm.name)
        return resp
    else:
        return redirect("/admin")


@admin_manage.route("/log_out")
def log_out():
    email = session['email']
    ad.log_out(email)
    return redirect("/")
