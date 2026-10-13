import os
import sqlite3

DATABASE_PATH = "data/customer_support.db"


def create_database():
    
    os.makedirs("data", exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH)

    # Create tables
    with open("database/schema.sql", "r") as file:
        schema = file.read()

    connection.executescript(schema)

    # -------------------------
    # Customers
    # -------------------------

    customers = [
        (1, "Rahul", "rahul@example.com"),
        (2, "Priya", "priya@example.com"),
        (3, "Arjun", "arjun@example.com"),
    ]

    connection.executemany(
        """
        INSERT OR IGNORE INTO customers
        (customer_id, name, email)
        VALUES (?, ?, ?)
        """,
        customers
    )

    # -------------------------
    # Products
    # -------------------------

    products = [
        (101, "iPhone 15", 60000, 10),
        (102, "Samsung S24", 55000, 5),
        (103, "OnePlus 12", 45000, 8),
        (104, "Sony WH-1000XM5", 30000, 15),
    ]

    connection.executemany(
        """
        INSERT OR IGNORE INTO products
        (product_id, name, price, stock)
        VALUES (?, ?, ?, ?)
        """,
        products
    )

    # -------------------------
    # Orders
    # -------------------------

    orders = [
        (1001, 1, 101, 1, "Shipped"),
        (1002, 2, 102, 1, "Delivered"),
        (1003, 3, 103, 2, "Processing"),
        (1004, 1, 104, 1, "Out for Delivery"),
    ]

    connection.executemany(
        """
        INSERT OR IGNORE INTO orders
        (order_id, customer_id, product_id, quantity, status)
        VALUES (?, ?, ?, ?, ?)
        """,
        orders
    )

    connection.commit()
    connection.close()

    print("Database created and sample data inserted!")


if __name__ == "__main__":
    create_database()