import datetime
import os
import random
import uuid

import psycopg
from dotenv import load_dotenv
from faker import Faker
from faker.providers import ssn, address

import constants
import tables
import utils

faker = Faker()
faker.add_provider(ssn)
faker.add_provider(address)

load_dotenv()
DB_NAME = os.getenv("DB_NAME", "detention_admin")

connection = psycopg.connect(f"dbname={DB_NAME}")
cursor = connection.cursor()

faker = Faker()
faker.add_provider(ssn)
faker.add_provider(address)

entries_counter = 1

user_ids: list[str] = []
prisoner_ids: list[str] = []
visitor_ids: list[str] = []
visit_ids: list[str] = []
visitations: list[(str, str)] = []


def drop_table(table_name: str) -> str:
    return f"DROP TABLE IF EXISTS {table_name} CASCADE"


def insert_into_table(table_name: str, fields_num: int):
    return f"INSERT INTO {table_name} values ({"%s" + ", %s" * (fields_num - 1)})"


def generate_id():
    global entries_counter
    generated = (
        utils.base36encode(entries_counter).lower()
    )
    entries_counter += 1
    return generated


def populate_prisoners():
    for _ in range(0, constants.PRISONERS_NUMBER):
        prisoner_ids.append(generate_id())
        cursor.execute(
            query=insert_into_table(tables.Prisoners.TABLE_NAME, len(tables.Prisoners.TABLE_COLUMNS)),
            params=(
                prisoner_ids[-1], faker.ssn(), faker.first_name(), faker.last_name(),
                faker.date_time(), faker.country(), uuid.uuid4(),
                faker.address(), faker.phone_number(), faker.email(),
                faker.phone_number(), faker.date_time(), faker.date_time(), faker.text()[0:9],
                random.random() * 1000 + 1, faker.date_time(), faker.boolean(chance_of_getting_true=70)
            )
        )


def populate_users():
    for _ in range(0, constants.USERS_NUMBER):
        user_ids.append(generate_id())
        cursor.execute(
            query=insert_into_table(tables.Users.TABLE_NAME, len(tables.Users.TABLE_COLUMNS)),
            params=(
                user_ids[-1],
                faker.user_name(), faker.sha256(), faker.sha256(), faker.first_name(),
                faker.last_name(), faker.boolean(chance_of_getting_true=5)
            )
        )


def populate_visitors():
    for _ in range(0, constants.VISITORS_NUMBER):
        visitor_ids.append(generate_id())
        cursor.execute(
            query=insert_into_table(tables.Visitors.TABLE_NAME, len(tables.Visitors.TABLE_COLUMNS)),
            params=(
                visitor_ids[-1], faker.first_name(), faker.last_name(), faker.text(), uuid.uuid4()
            )
        )


def populate_visits():
    for _ in range(0, constants.VISITS_NUMBER):
        visit_ids.append(generate_id())
        random_prisoner_id = prisoner_ids[int(random.random() * constants.PRISONERS_NUMBER)]
        visitations.append((visit_ids[-1], random_prisoner_id))
        restricted_visit = faker.boolean(chance_of_getting_true=5)
        summary = faker.text() if restricted_visit else None
        cursor.execute(
            query=insert_into_table(tables.Visits.TABLE_NAME, len(tables.Visits.TABLE_COLUMNS)),
            params=(
                visit_ids[-1], random_prisoner_id, faker.date(), faker.date_time(), faker.date_time(),
                faker.text(), restricted_visit, summary
            )
        )


def populate_visitations():
    for visitation in visitations:
        visitors_num = int(random.random() * constants.MAX_VISITORS_PER_VISIT_NUMBER)
        visitors: list[str] = []
        for index in range(0, visitors_num):
            visitors.append(visitor_ids[int(random.random() * constants.VISITORS_NUMBER)])
        for visitor in visitors:
            visit_role = 0 if faker.boolean(30) else 1
            cursor.execute(
                query=insert_into_table(tables.Visitations.TABLE_NAME, len(tables.Visitations.TABLE_COLUMNS)),
                params=(
                    generate_id(), visitor, visitation[0], visit_role
                )
            )


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
    print(f"Populating script finished in {(finish - start).seconds}s")

    connection.commit()
except BaseException as e:
    print()
    print("Exception: ", e)
    connection.rollback()
finally:
    cursor.close()
    connection.close()
