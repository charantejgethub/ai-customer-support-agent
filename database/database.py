import sqlite3

DATABASE_PATH = "data/customer_support.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)