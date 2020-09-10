import os

from flask import (Blueprint, flash, make_response, redirect, render_template,
                   request, session, url_for)
from werkzeug.utils import secure_filename

import admin.admin as ad
from admin.admin import Admin, AdminInfo, LoginForm, UploadAvt

admin_manage = Blueprint("admin_manage", __name__,
                         static_folder='static', template_folder='templates')


# Login, log out
@admin_manage.route("/")
def admin_homepage():
    form = AdminInfo()
    admin = ad.get_admin_info(session['email'])
    return render_template('home.html', form=form, admin=admin)


@admin_manage.route("/login")
def login_page():
    form = LoginForm()
    return render_template("login.html", form=form)


@admin_manage.route("/login_info", methods=["GET", "POST"])
def get_login_info():
    form = LoginForm(request.form)
    email = form.username.data
    passwd = form.passwd.data
    adm = ad.get_admin_info(email)
    if ad.is_valid_admin(email, passwd):
        session['email'] = email
        flash("Login Successfully!")
        resp = make_response(redirect("/"))
        resp.set_cookie('usrname', adm.name)
        return resp
    else:
        return redirect("/admin/login")


@admin_manage.route("/log_out")
def log_out():
    email = session['email']
    ad.log_out(email)
    return redirect("/")


# Profile
@admin_manage.route("/upload_avatar")
def upload_avt():
    form = UploadAvt()
    admin = ad.get_admin_info(session['email'])
    return render_template('upload_avt.html', form=form, admin_img=admin.avatar)


@admin_manage.route("avt_upload_xyz", methods=['POST'])
def get_image():
    form = UploadAvt(request.form)
    image = request.files[form.uploader.name]
    try:
        f = open('admin/static/img/avatars/'+session['email'][:-4]+'.jpeg', "wb")
    except:
        f = open('admin/static/img/avatars/'+session['email'][:-4]+'.jpeg', "xb")
    f.write(image.read())
    f.close()
    ad.change_profile_image(session['email'])
    return redirect("/admin")
