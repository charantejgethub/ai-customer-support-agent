import sqlite3

DATABASE_PATH = "data/customer_support.db"


def get_customer_orders(customer_id):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            orders.order_id,
            products.name,
            orders.quantity,
            orders.status
        FROM orders
        JOIN products
            ON orders.product_id = products.product_id
        WHERE orders.customer_id = ?
        """,
        (customer_id,)
    )

    results = cursor.fetchall()

    connection.close()

    if not results:
        return "No orders found for this customer."

    orders = []

    for order in results:

        order_id, product_name, quantity, status = order

        orders.append({
            "order_id": order_id,
            "product": product_name,
            "quantity": quantity,
            "status": status
        })

    return orders


def get_customer_by_email(email):
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT customer_id, name, email
        FROM customers
        WHERE LOWER(email) = LOWER(?)
        """,
        (email,)
    )

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return "Customer not found."

    customer_id, name, email = result

    return {
        "customer_id": customer_id,
        "name": name,
        "email": email
    }

def get_my_orders(customer_id):
    return get_customer_orders(customer_id)