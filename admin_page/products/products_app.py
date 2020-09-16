from sqlalchemy import MetaData, Table, create_engine

from products.obj import Add_Product, Filter, Products


# Define database directory
database = "sqlite:///./DB.db"


# -------------------------------------------------
# Database -> connection
#   create_connection -> connect_db
#   close_connection -> close_db
# -------------------------------------------------
def connect_db():
    engine = create_engine(database, connect_args={'check_same_thread': False})
    conn = engine.connect()
    metadata = MetaData(bind=engine)
    Prd_Table = Table('PRODUCTS', metadata, autoload=True)
    return engine, conn, Prd_Table


def close_db(engine, conn):
    conn.close()
    engine.dispose()


# -------------------------------------------------
# Working with database
# ----------------------------------
#   get_all_databse (list)  -> get_database
#   get database            -> convert to Products instances -> get_products
#   get product by its id   -> get_prd_by_id
#   update products info    -> update_products
# ----------------------------------
#   Working with filter
#       filter by price
#       filter by category
#       filter by brand
# -------------------------------------------------


# Get database -> return a list of tuple
# return type:
#   [(prd1),(pr2),...]
def get_database():
    engine, conn, Prd_Table = connect_db()
    product_db = Prd_Table.select().execute().fetchall()
    close_db(engine, conn)
    return product_db


# Get products
# Return type:
#   list of Products' objects:
#       [Prd1, Prd2,...]
def get_products():
    product_db = get_database()
    product_list = []
    for prd in product_db:
        product_list.append(
            Products(prd[0], prd[1], prd[2], prd[3], prd[4], prd[5], prd[6], prd[7], prd[8]))
    return product_list


# Get product by id
# Use try - except to avoid crash
# return:
#   Products' object
def get_prd_by_id(prd_id):
    engine, conn, Prd_Table = connect_db()
    try:
        prd = Prd_Table.select(whereclause=Prd_Table.c.ID ==
                               prd_id).execute().fetchall()
        close_db(engine, conn)
        return prd
    except:
        close_db(engine, conn)
        return False

# ----------------------------------
# FILTERING
# ----------------------------------


# Filter by category
#   Input: category -> choose from form
#   Output: list of products with the category above
def get_prd_by_categories(cat):
    engine, conn, Prd_Table = connect_db()
    prd = Prd_Table.select(
        whereclause=Prd_Table.c.category == cat).execute().fetchall()
    prd_by_cat = [Products(p[0], p[1], p[2], p[3], p[4],
                           p[5], p[6], p[7], p[8]) for p in prd]
    close_db(engine, conn)
    return prd_by_cat


def get_all_categories():
    prd_list = get_products()
    cat = []
    cat = [prd.category for prd in prd_list if prd not in cat]
    return cat


# Filter by price range
#   Input: Price range:
#           min: 0
#           max: inf
#   Output: Matching products
def get_prd_by_price_range(min=0, max=1e20):
    engine, conn, Prd_Table = connect_db()
    prd = Prd_Table.select(whereclause=Prd_Table.c.price >=
                           min and Prd_Table.c.price <= max).execute().fetchall()
    prd_by_price_range = [Products(p[0], p[1], p[2], p[3], p[4],
                                   p[5], p[6], p[7], p[8]) for p in prd]
    close_db(engine, conn)
    return prd_by_price_range


# Filter by brand
# Input: Brand <- select form selection form <- wtforms
#           Choices retrieve from database
# Output: Matching products
def get_prd_by_brand(brand):
    engine, conn, Prd_Table = connect_db()
    prd = Prd_Table.select(whereclause=Prd_Table.c.brand ==
                           brand).execute().fetchall()
    prd_by_brand = [Products(p[0], p[1], p[2], p[3], p[4],
                             p[5], p[6], p[7], p[8]) for p in prd]
    close_db(engine, conn)
    return prd_by_brand


# ---------------------------------
# Make changes to database
# ---------------------------------
def update_product(prd):
    engine, conn, Prd_Table = connect_db()
    Prd_Table.update(whereclause=Prd_Table.c.ID == prd.ID).values(
        name=prd.name, price=prd.price, amount=prd.amount, brand=prd.brand, description=prd.description, lock=prd.lock).execute()
    close_db(engine, conn)
    return 0


def add_products(prd):
    engine, conn, Prd_Table = connect_db()
    Prd_Table.insert(None).values(ID=prd.ID, name=prd.name, category=prd.category,
                                  price=prd.price, amount=prd.amount, brand=prd.brand, description=prd.description, lock=0).execute()
    close_db(engine, conn)
    return True


def remove(prd_id):
    engine, conn, Prd_Table = connect_db()
    Prd_Table.update(whereclause=Prd_Table.c.ID == prd_id).values(lock=1)
    close_db(engine, conn)
    return True


def get_filter_prd(category, lower, upper, status):
    prd = get_products()
    target_prd = []
    for product in prd:
        if product.price >= float(lower) and product.price <= float(upper) and product.lock==status:
            if category == 'All':
                target_prd.append(product)
            elif product.category == category:
                target_prd.append(product)
    return target_prd
