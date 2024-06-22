from base_repository import *


class UserRepository(PostgresRepository):
    TABLE_NAME = 'users'


class SessionRepository(PostgresRepository):
    TABLE_NAME = 'sessions'
