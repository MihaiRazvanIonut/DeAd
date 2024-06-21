from base_repository import *


class InviteRepository(PostgresRepository):
    TABLE_NAME = 'invites'


class UserRepository(PostgresRepository):
    TABLE_NAME = 'users'
