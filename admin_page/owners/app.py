from sqlalchemy import create_engine, Table, MetaData
from admin.admin import Admin

database = "sqlite:///./DB.db"


def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Admin_Table = Table('ADMIN', metadata, autoload=True)
    return engine, conn, Admin_Table


def close_db(engine, conn):
    conn.close()
    engine.dispose()


def get_all_admin():
    engine, conn, Adm = connect_db()
    admin_list = Adm.select().execute().fetchall()
    close_db(engine, conn)
    return [Admin(ad[0], ad[1], ad[2], ad[3], ad[4], ad[5], ad[6], ad[7]) for ad in admin_list]

def update_admin(ID, permission):
    engine, conn, Adm = connect_db()
    Adm.update(whereclause=Adm.c.ID==ID).values(permission=permission).execute()
    close_db(engine, conn)