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

    def find_by_id(self, id_value: str, columns: str = '*'):
        sql = f"SELECT {columns} FROM {self.TABLE_NAME} WHERE id = %s"
        try:
            return self._client.execute(sql, (id_value,)).fetchone()

        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')

    def update_by_id(self, prisoner_id: str, entry: dict):
        fields = list(entry.keys())
        values = list(entry.values())
        values.append(prisoner_id)
        pairs = f'{fields[0]} = %s'
        for field in fields[1:]:
            pairs += f', {field} = %s'
        sql = f'UPDATE {self.TABLE_NAME} SET {pairs} WHERE id = %s'
        try:
            self._client.execute(sql, values)
        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')

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
