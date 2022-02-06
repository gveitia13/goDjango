from django.test import TestCase

# Create your tests here.
import sqlite3

from sqlite3 import Error

from goDjango.settings import BASE_DIR


def sql_connection():
    try:

        con = sqlite3.connect(BASE_DIR / 'db.sqlite3')

        return con

    except Error:

        print(Error)


def sql_table(con):
    cursorObj = con.cursor()

    cursorObj.execute(
        "CREATE TABLE sale_sale("
        "id integer PRIMARY KEY,"
        "name text,"
        "price real, "
        "cost real,"
        "point_of_sale text,"
        "hash text,"
        "date_creation text,"
        "date_updated text)"
    )

    con.commit()


con = sql_connection()

sql_table(con)
