import sqlite3

DATABASE_PATH = "data/customer_support.db"


def create_support_ticket(customer_id, issue, order_id=None):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO tickets
        (customer_id, order_id, issue, status)
        VALUES (?, ?, ?, ?)
        """,
        (customer_id, order_id, issue, "Open")
    )

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "ticket_id": ticket_id,
        "customer_id": customer_id,
        "order_id": order_id,
        "issue": issue,
        "status": "Open"
    }


def create_my_support_ticket(issue, customer_id, order_id=None):
    return create_support_ticket(
        customer_id,
        issue,
        order_id
    )

def verify_order_belongs_to_customer(order_id, customer_id):

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT order_id
        FROM orders
        WHERE order_id = ?
        AND customer_id = ?
        """,
        (order_id, customer_id)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None