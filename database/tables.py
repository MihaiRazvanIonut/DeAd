class Visits:
    TABLE_NAME = "visits"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id VARCHAR PRIMARY KEY,
        prisoner_id VARCHAR NOT NULL,
        date Date NOT NULL,
        start_time DATE NOT NULL,
        end_time DATE NOT NULL,
        purpose VARCHAR NOT NULL,
        restricted BOOLEAN NOT NULL,
        summary TEXT,
        CONSTRAINT fk_visit_prisoner FOREIGN KEY (prisoner_id) REFERENCES prisoners(id)
        )
    """


class Visitations:
    TABLE_NAME = "visitations"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        nin VARCHAR NOT NULL,
        visit_id VARCHAR NOT NULL,
        visit_role INTEGER NOT NULL,
        CONSTRAINT fk_visitation_visitor FOREIGN KEY (nin) REFERENCES visitors(nin),
        CONSTRAINT fk_visitation_visit FOREIGN KEY (visit_id) REFERENCES visits(id)
        )
    """


class Visitors:
    TABLE_NAME = "visitors"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        nin VARCHAR PRIMARY KEY,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        relationship VARCHAR,
        image VARCHAR
        )
    """


class Prisoners:
    TABLE_NAME = "prisoners"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id VARCHAR PRIMARY KEY,
        nin VARCHAR NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        date_of_birth DATE NOT NULL,
        nationality VARCHAR NOT NULL,
        image VARCHAR,
        address VARCHAR,
        phone_number VARCHAR,
        email VARCHAR,
        emergency_contact VARCHAR NOT NULL,
        arrest_date DATE NOT NULL,
        conviction_date DATE NOT NULL,
        crime_committed VARCHAR NOT NULL,
        case_number INTEGER NOT NULL,
        release_date DATE NOT NULL,
        repeated_felon BOOLEAN NOT NULL
        )
    """


class MoodIndexes:
    TABLE_NAME = "mood_indexes"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        prisoner_id VARCHAR NOT NULL,
        visit_id VARCHAR NOT NULL,
        arousal INTEGER NOT NULL,
        flow INTEGER NOT NULL,
        control INTEGER NOT NULL,
        relaxation INTEGER NOT NULL,
        CONSTRAINT fk_mood_prisoner FOREIGN KEY (prisoner_id) REFERENCES prisoners(id),
        CONSTRAINT fk_mood_visit FOREIGN KEY (visit_id) REFERENCES visits(id)
        )
    """


class Items:
    TABLE_NAME = "items"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        prisoner_id VARCHAR NOT NULL,
        visit_id VARCHAR NOT NULL,
        name VARCHAR NOT NULL,
        action INTEGER NOT NULL,
        CONSTRAINT fk_item_prisoner FOREIGN KEY (prisoner_id) REFERENCES prisoners(id),
        CONSTRAINT fk_item_visit FOREIGN KEY (visit_id) REFERENCES visits(id)
        )
    """


class Users:
    TABLE_NAME = "users"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id VARCHAR PRIMARY KEY,
        username VARCHAR NOT NULL,
        hash VARCHAR NOT NULL,
        salt VARCHAR NOT NULL,
        first_name VARCHAR NOT NULL,
        last_name VARCHAR NOT NULL,
        admin BOOLEAN NOT NULL
        )
    """


class Invites:
    TABLE_NAME = "invites"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id VARCHAR PRIMARY KEY,
        creator_id VARCHAR NOT NULL,
        invitee_id VARCHAR NOT NULL,
        status INTEGER NOT NULL,
        expiry_date DATE NOT NULL,
        CONSTRAINT fk_invites_creator FOREIGN KEY (creator_id) REFERENCES users(id)
        )
    """


class Actions:
    TABLE_NAME = "actions"
    TABLE_CREATE = f"""
        CREATE TABLE {TABLE_NAME} (
        id VARCHAR PRIMARY KEY,
        type INTEGER NOT NULL,
        user_id VARCHAR NOT NULL,
        visit_id VARCHAR NOT NULL,
        time DATE NOT NULL,
        CONSTRAINT fk_actions_user FOREIGN KEY (user_id) REFERENCES users(id),
        CONSTRAINT fk_actions_visit FOREIGN KEY (visit_id) REFERENCES visits(id)
        )
    """


DB_TABLES = (
    Users(), Prisoners(), Visitors(),
    Visits(), Visitations(), MoodIndexes(),
    Items(), Invites(), Actions()
)
