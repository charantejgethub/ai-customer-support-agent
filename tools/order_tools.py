import sqlite3

DATABASE_PATH = "data/customer_support.db"


def get_order_status(order_id):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.order_id,
            customers.name,
            products.name,
            orders.quantity,
            orders.status
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.customer_id
        JOIN products
            ON orders.product_id = products.product_id
        WHERE orders.order_id = ?
        """,
        (order_id,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return "Order not found."

    order_id, customer_name, product_name, quantity, status = result

    return {
        "order_id": order_id,
        "customer": customer_name,
        "product": product_name,
        "quantity": quantity,
        "status": status
    }

def get_my_order_status(order_id, customer_id):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.order_id,
            customers.name,
            products.name,
            orders.quantity,
            orders.status
        FROM orders
        JOIN customers
            ON orders.customer_id = customers.customer_id
        JOIN products
            ON orders.product_id = products.product_id
        WHERE orders.order_id = ?
        AND orders.customer_id = ?
        """,
        (order_id, customer_id)
    )

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return {
            "error": "Order not found or does not belong to the current customer."
        }

    order_id, customer_name, product_name, quantity, status = result

    return {
        "order_id": order_id,
        "customer": customer_name,
        "product": product_name,
        "quantity": quantity,
        "status": status
    }