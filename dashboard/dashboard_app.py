try:
    import products.products_app as ppa
except:
    pass

def get_all_categories():
    cat = ppa.get_all_categories()
    print(cat)
    return True