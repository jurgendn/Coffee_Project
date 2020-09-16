# -------------------------------------------------------
# Import modules
# -----------------------------
from datetime import date, timedelta

from sqlalchemy import MetaData, Table, create_engine
from wtforms import Form, IntegerField, StringField

# -------------------------------------------------------
# DB declaration
# -----------------------------
database = "sqlite:///./DB.db"


# -------------------------------------------------------
# Transaction class
# -----------------------------
class Transaction:
    def __init__(self, ID, user_ID, products_list, total, date, method):
        self.ID = ID
        self.user_ID = user_ID
        self.products_list = products_list
        self.total = total
        self.date = date
        self.method = method

# --------------------------------------------------------
# Convert to objects


def parse_product_list(prd_raw):
    # t is a string: ID1:am1;ID2:am2;...
    tmp = prd_raw.split(";")
    prd_list = []
    for pr in tmp:
        prd_list.append(pr.split(":"))
    return prd_list


def convert_to_obj(t):
    return Transaction(t[0], t[1], parse_product_list(t[2]), t[3], t[4], t[5])


# -------------------------------------------------------
# Request methods
# -----------------------------
def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Prd_Table = Table('TRANSACTION', metadata, autoload=True)
    return engine, conn, Prd_Table


def close_db(engine, conn):
    conn.close()
    engine.dispose()
# ------------------------------


# --------------------------------------------------------
# Get data from db
# ------------------------------
def get_all_transaction():
    engine, conn, Trans_tab = connect_db()
    transactions_list = Trans_tab.select().execute().fetchall()
    close_db(engine, conn)
    prd_list = [Transaction(t[0], t[1], parse_product_list(
        t[2]), t[3], t[4], t[5]) for t in transactions_list]
    return prd_list
# --------------------------------------------------------
