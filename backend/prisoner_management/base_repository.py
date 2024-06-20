import psycopg
from psycopg.rows import dict_row

import exceptions


class BasePostgresRepository:
    _connection = None
    _client = None

    def __init__(self, connection_info: str):
        if not self._connection:
            self._connection = psycopg.connect(connection_info, row_factory=dict_row)
            self._client = self._connection.cursor()

    def commit(self):
        self._connection.commit()

    def rollback(self):
        self._connection.rollback()


class PostgresRepository(BasePostgresRepository):
    TABLE_NAME: str = ""

    def find_by_id(self, columns: str = '*', condition_value: str | None = None):
        try:
            if not condition_value:
                sql = f"SELECT {columns} FROM {self.TABLE_NAME}"
            else:
                sql = f"SELECT {columns} FROM {self.TABLE_NAME} WHERE id = %s"

            return self._client.execute(sql, (condition_value,)).fetchone()
        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')

    def update(self, update_values: dict[str, str], columns: str | None = None, condition: str | None = None):
        pass

    def delete(self, condition: str):
        pass

    def insert(self, fields: str, values: list):
        sql = f"INSERT INTO {self.TABLE_NAME} ({fields}) VALUES ({'%s' + (', %s' * (len(values) - 1))})"
        try:
            self._client.execute(sql, values)
        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')
