import datetime
import os

import psycopg
from dotenv import load_dotenv

import tables

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "detention_admin")

connection = psycopg.connect(f"dbname={DB_NAME}")
cursor = connection.cursor()


def drop_table(table_name: str) -> str:
    return f"DROP TABLE IF EXISTS {table_name} CASCADE"


def populate():
    pass


try:
    print("Dropping existing tables...", end='')
    for table in tables.DB_TABLES:
        cursor.execute(drop_table(table.TABLE_NAME))

    print("Done")

    print("Creating tables...", end='')
    for table in tables.DB_TABLES:
        cursor.execute(table.TABLE_CREATE)

    print("Done")

    start = datetime.datetime.now(datetime.UTC)
    print("Populating tables...", end='')
    populate()
    finish = datetime.datetime.now(datetime.UTC)
    print(f"Populating script finished in {(finish - start).microseconds / 1000}ms")

    connection.commit()
except BaseException as e:
    print(e)
finally:
    connection.close()
