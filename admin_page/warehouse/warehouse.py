from flask import Flask, redirect, render_template, request, url_for, Blueprint

from warehouse.warehouse_app import WarehouseActivities, Filter
import warehouse.warehouse_app as wwa

warehouse = Blueprint('warehouse', __name__,
                      static_folder='static', template_folder='templates')


@warehouse.route("/", methods=["GET"])
def get_atv():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    if start_date == '':
        start_date = "NG"
    if end_date == '':
        end_date = "NG"
    activities = wwa.get_by_date(start_date, end_date)
    print(activities)
    form = Filter()
    return render_template("warehouse.html", activities=activities, form=form)
