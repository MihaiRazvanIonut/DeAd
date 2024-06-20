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

    def update_by_id(self, prisoner_id: str, entry: dict):
        fields = list(entry.keys())
        values = list(entry.values())
        pairs = f'fields'
        for field in fields[1:]:
            pass
        sql = f'UPDATE {self.TABLE_NAME} SET {pairs} WHERE id = %s'
        pass

    def delete(self, condition: str):
        pass

    def insert(self, entry: dict):
        fields = list(entry.keys())
        values = list(entry.values())
        flat_fields = str(fields[0])
        for field in fields[1:]:
            flat_fields += f', {field}'
        sql = f"INSERT INTO {self.TABLE_NAME} ({flat_fields}) VALUES ({'%s' + (', %s' * (len(values) - 1))})"
        try:
            self._client.execute(sql, values)
        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')
