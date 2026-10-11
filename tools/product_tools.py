import sqlite3

DATABASE_PATH = "data/customer_support.db"


def get_product_info(product_name):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT product_id, name, price, stock
        FROM products
        WHERE LOWER(name) LIKE LOWER(?)
        """,
        (f"%{product_name}%",)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return "Product not found."

    product_id, name, price, stock = result

    return {
        "product_id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }