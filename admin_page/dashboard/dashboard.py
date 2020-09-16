from flask import Blueprint, redirect, render_template, url_for, request, make_response
import dashboard.dashboard_app as dda


dashboard = Blueprint('dashboard', __name__,
                      static_folder='static', template_folder='templates')


@dashboard.route("/")
def dashboard_page():
    revenue = dda.get_total_revenue('TRANSACTION')
    vstor = dda.get_total_visit("COUNT_VISIT")
    return render_template("dashboard.html", rev=revenue, vstor=vstor)
