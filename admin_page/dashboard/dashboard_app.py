from sqlalchemy import create_engine, Table, MetaData

database = "sqlite:///./DB.db"


def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Trs_Table = Table('TRANSACTION', metadata, autoload=True)
    return engine, conn, Trs_Table


def close_db(engine, conn):
    conn.close()
    engine.dispose()


def get_all_transaction():
    engine, conn, Trs_Table = connect_db()
    trs = Trs_Table.select().execute().fetchall()
    close_db(engine, conn)
    return trs

def get_total_revenue():
    trs = get_all_transaction()
    return sum(t[3] for t in trs)