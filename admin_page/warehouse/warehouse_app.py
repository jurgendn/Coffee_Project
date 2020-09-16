from datetime import date, datetime, timedelta

from flask import session
from sqlalchemy import MetaData, Table, create_engine
from wtforms import Form, SelectField, SubmitField
from wtforms.fields.html5 import DateField

database = "sqlite:///./DB.db"


class WarehouseActivities:
    def __init__(self, ID, prd_ID, executer_ID, amount, date):
        self.ID = ID
        self.prd_ID = prd_ID
        self.executer_ID = executer_ID
        self.amount = amount
        self.date = date


class Filter(Form):
    start_date = DateField("Start Date")
    end_date = DateField("End Date")
    fil = SubmitField("Filter")


def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Warehouse = Table('WAREHOUSE', metadata, autoload=True)
    return engine, conn, Warehouse


def close_db(engine, conn):
    conn.close()
    engine.dispose()


def get_all_activities():
    engine, conn, Warehouse = connect_db()
    activities = Warehouse.select().execute().fetchall()
    close_db(engine, conn)
    return activities


def add_activity(prd_ID, amount):
    engine, conn, Warehouse = connect_db()
    activities = get_all_activities()
    Warehouse.insert().values(ID=len(activities), prd_id=prd_ID,
                              executer_id=session['email'], amount=amount, date=datetime.now()).execute()
    close_db(engine, conn)
    return True


def get_by_date(start_date='NG', end_date='NG'):
    activities = get_all_activities()
    target_activities = []
    # print("Target: ", type(date.fromisoformat(start_date)))
    # print(type(date.fromisoformat(activities[0][4].split(" ")[0])))
    if start_date == "NG" and end_date != "NG":
        for act in activities:
            if date.fromisoformat(act[4].split(" ")[0]) <= date.fromisoformat(end_date):
                target_activities.append(WarehouseActivities(
                    act[0], act[1], act[2], act[3], act[4]))
    elif end_date == "NG" and start_date != "NG":
        for act in activities:
            if date.fromisoformat(act[4].split(" ")[0]) >= date.fromisoformat(start_date):
                target_activities.append(WarehouseActivities(
                    act[0], act[1], act[2], act[3], act[4]))
    elif start_date != "NG" and end_date != "NG":
        for act in activities:
            if date.fromisoformat(act[4].split(" ")[0]) <= date.fromisoformat(end_date) and date.fromisoformat(act[4].split(" ")[0]) >= date.fromisoformat(start_date):
                target_activities.append(WarehouseActivities(
                    act[0], act[1], act[2], act[3], act[4]))
    else:
        target_activities = [WarehouseActivities(
                    act[0], act[1], act[2], act[3], act[4]) for act in activities]
    return target_activities
