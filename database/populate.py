import datetime
import os
import random
import sys
import uuid

import psycopg
import uuid6
from dotenv import load_dotenv
from faker import Faker
from faker.providers import ssn, address

import constants
import providers
import tables

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
faker.add_provider(providers.CustomProvider)

entries_counter = 1

user_ids: list[str] = []
prisoner_ids: list[str] = []
visitor_ids: list[str] = []
visit_ids: list[str] = []
visit_prisoner_entries: list[(str, str)] = []


def drop_table(table_name: str) -> str:
    return f"DROP TABLE IF EXISTS {table_name} CASCADE"


def insert_into_table(table_name: str, fields_num: int):
    return f"INSERT INTO {table_name} values ({"%s" + ", %s" * (fields_num - 1)})"


def generate_id():
    return str(uuid6.uuid7().int % sys.maxsize)


def populate_prisoners():
    for _ in range(0, constants.PRISONERS_NUMBER):
        prisoner_ids.append(generate_id())
        cursor.execute(
            query=insert_into_table(tables.Prisoners.TABLE_NAME, len(tables.Prisoners.TABLE_COLUMNS)),
            params=(
                prisoner_ids[-1], faker.ssn(), faker.first_name(), faker.last_name(),
                faker.date_time(), faker.country(), uuid.uuid4(),
                faker.address(), faker.phone_number(), faker.email(),
                faker.phone_number(), faker.date_time(), faker.date_time(), faker.crime(),
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
                faker.last_name(), len(user_ids) == 1
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
        visit_prisoner_entries.append((visit_ids[-1], random_prisoner_id))
        restricted_visit = faker.boolean(chance_of_getting_true=5)
        summary = faker.text() if restricted_visit else None
        cursor.execute(
            query=insert_into_table(tables.Visits.TABLE_NAME, len(tables.Visits.TABLE_COLUMNS)),
            params=(
                visit_ids[-1], random_prisoner_id, faker.date(), faker.date_time(), faker.date_time(),
                faker.visit_purpose(), restricted_visit, summary, False
            )
        )


def populate_visitations():
    for visit_prisoner_entry in visit_prisoner_entries:
        visitors_num = int(random.random() * constants.MAX_VISITORS_PER_VISIT_NUMBER)
        visitors: list[str] = []
        for index in range(0, visitors_num):
            visitors.append(visitor_ids[int(random.random() * constants.VISITORS_NUMBER)])
        for visitor in visitors:
            visit_role = int(faker.boolean(chance_of_getting_true=70))
            cursor.execute(
                query=insert_into_table(tables.Visitations.TABLE_NAME, len(tables.Visitations.TABLE_COLUMNS)),
                params=(
                    generate_id(), visitor, visit_prisoner_entry[0], visit_role
                )
            )


def populate_mood_indexes():
    for visit_prisoner_entry in visit_prisoner_entries:
        cursor.execute(
            query=insert_into_table(tables.MoodIndexes.TABLE_NAME, len(tables.MoodIndexes.TABLE_COLUMNS)),
            params=(
                generate_id(), visit_prisoner_entry[1], visit_prisoner_entry[0],
                int(random.random() * 10 + 1),
                int(random.random() * 10 + 1),
                int(random.random() * 10 + 1),
                int(random.random() * 10 + 1)
            )
        )


def populate_items():
    for visit_prisoner_entry in visit_prisoner_entries:
        cursor.execute(
            query=insert_into_table(tables.Items.TABLE_NAME, len(tables.Items.TABLE_COLUMNS)),
            params=(
                generate_id(), visit_prisoner_entry[1], visit_prisoner_entry[0],
                faker.prisoner_item(), int(faker.boolean(chance_of_getting_true=70))
            )
        )


def populate_invites():
    for _ in user_ids[1:]:
        cursor.execute(
            query=insert_into_table(tables.Invites.TABLE_NAME, len(tables.Invites.TABLE_COLUMNS)),
            params=(
                uuid.uuid4(), user_ids[0], 1, None
            )
        )
    for _ in range(0, constants.WAITING_USERS):
        cursor.execute(
            query=insert_into_table(tables.Invites.TABLE_NAME, len(tables.Invites.TABLE_COLUMNS)),
            params=(
                uuid.uuid4(), user_ids[0], 0, faker.date_time()
            )
        )


def populate_actions():
    for visit_id in visit_ids:
        random_user_id_index = int(random.random() * constants.USERS_NUMBER)
        cursor.execute(
            query=insert_into_table(tables.Actions.TABLE_NAME, len(tables.Actions.TABLE_COLUMNS)),
            params=(
                generate_id(), "create", user_ids[random_user_id_index], visit_id, faker.date_time()
            )
        )
    for _ in range(0, constants.ACTIONS_NUMBER):
        random_user_id = user_ids[int(random.random() * constants.USERS_NUMBER)]
        random_visit_id = visit_ids[int(random.random() * constants.VISITS_NUMBER)]
        cursor.execute(
            query=insert_into_table(tables.Actions.TABLE_NAME, len(tables.Actions.TABLE_COLUMNS)),
            params=(
                generate_id(), "update", random_user_id, random_visit_id, faker.date_time()
            )
        )


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
    print(f"Populating script finished in {(finish - start).total_seconds()}s")

    connection.commit()
except BaseException as e:
    print()
    print("Exception: ", e)
    connection.rollback()
finally:
    cursor.close()
    connection.close()
