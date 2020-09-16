from sqlalchemy import create_engine, Table, MetaData

database = "sqlite:///./DB.db"


def connect_db(table):
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Trs_Table = Table(table, metadata, autoload=True)
    return engine, conn, Trs_Table


def close_db(engine, conn):
    conn.close()
    engine.dispose()


def get_all_transaction(table):
    engine, conn, Trs_Table = connect_db(table)
    trs = Trs_Table.select().execute().fetchall()
    close_db(engine, conn)
    return trs

def get_total_revenue(table):
    trs = get_all_transaction(table)
    return sum(t[4] for t in trs)

def get_total_visit(table):
    vs = get_all_transaction(table)
    return sum(t[1]+t[2]+t[3]+t[4] for t in vs)