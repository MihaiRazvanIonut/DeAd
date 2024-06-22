from base_repository import *


class UserRepository(PostgresRepository):
    TABLE_NAME = 'users'


class InviteRepository(PostgresRepository):
    TABLE_NAME = 'invites'
