from flask import Blueprint, request, redirect, render_template, url_for
from transaction.transaction_app import Transaction
import transaction.transaction_app as tta

transaction = Blueprint('transaction', __name__,
                        static_folder='static', template_folder='templates')


@transaction.route("/")
def transaction_list():
    t = tta.get_all_transaction()
    return render_template("transaction.html", transactions=t)
