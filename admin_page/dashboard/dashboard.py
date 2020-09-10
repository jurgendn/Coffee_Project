from flask import Blueprint, redirect, render_template, url_for, request, make_response
try:
    import dashboard.dashboard_app as dda
except:
    pass

dashboard = Blueprint('dashboard', __name__,
                      static_folder='static', template_folder='templates')


@dashboard.route("/")
def dashboard_page():
    print(dda.get_all_categories())
    return render_template("dashboard.html")
