import datetime
import os
import random
import uuid

import psycopg
from dotenv import load_dotenv
from faker import Faker
from faker.providers import ssn, address

import tables
from constants import *

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "detention_admin")

connection = psycopg.connect(f"dbname={DB_NAME}")
cursor = connection.cursor()

faker = Faker()
faker.add_provider(ssn)
faker.add_provider(address)


def drop_table(table_name: str) -> str:
    return f"DROP TABLE IF EXISTS {table_name} CASCADE"


def insert_into_table(table_name: str, fields_num: int):
    return f"INSERT INTO {table_name} values ({"%s" + ", %s" * (fields_num - 1)})"


def populate_users():
    for _ in range(0, USERS_NUMBER):
        columns_number = len(tables.Users.TABLE_COLUMNS)
        cursor.execute(
            query=insert_into_table(tables.Users.TABLE_NAME, columns_number),
            params=(
                uuid.uuid4(), faker.user_name(), faker.sha256(), faker.sha256(), faker.first_name(),
                faker.last_name(), faker.boolean(chance_of_getting_true=5)
            )
        )
    connection.commit()


def populate_prisoners():
    for _ in range(0, PRISONERS_NUMBER):
        columns_number = len(tables.Prisoners.TABLE_COLUMNS)
        cursor.execute(
            query=insert_into_table(tables.Prisoners.TABLE_NAME, columns_number),
            params=(
                uuid.uuid4(), faker.ssn(), faker.first_name(), faker.last_name(), faker.date_time(),
                faker.country(), uuid.uuid4(), faker.address(), faker.phone_number(), faker.email(),
                faker.phone_number(), faker.date_time(), faker.date_time(), faker.text()[0:9],
                random.random() * 1000 + 1, faker.date_time(), faker.boolean(chance_of_getting_true=70)
            )
        )
    connection.commit()


def populate_visitors():
    pass


def populate_visits():
    pass


def populate_visitations():
    pass


def populate_mood_indexes():
    pass


def populate_items():
    pass


def populate_invites():
    pass


def populate_actions():
    pass


def populate():
    print("Populating users...", end='')
    populate_users()
    print("Done")

    print("Populating prisoners...", end='')
    populate_prisoners()
    print("Done")

    print("Populating visitors...", end='')
    populate_visitors()
    print("Done")

    print("Populating visits...", end='')
    populate_visits()
    print("Done")

    print("Populating visitations...", end='')
    populate_visitations()
    print("Done")

    print("Populating mood_indexes...", end='')
    populate_mood_indexes()
    print("Done")

    print("Populating items...", end='')
    populate_items()
    print("Done")

    print("Populating invites...", end='')
    populate_invites()
    print("Done")

    print("Populating actions...", end='')
    populate_actions()
    print("Done")


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
    print("Populating tables...")
    populate()
    finish = datetime.datetime.now(datetime.UTC)
    print(f"Populating script finished in {(finish - start).microseconds / 1000}ms")

    connection.commit()
except BaseException as e:
    print()
    print("Exception: ", e)
    connection.rollback()
finally:
    cursor.close()
    connection.close()
