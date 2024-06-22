from base_repository import *


class ActionRepository(PostgresRepository):
    TABLE_NAME = 'actions'

    def find_join_with_user(self, columns: str = '*'):
        sql = f'SELECT {columns} FROM {self.TABLE_NAME} a JOIN users u on a.user_id = u.id'
        try:
            return self._client.execute(sql).fetchall()

        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')
