import psycopg
from psycopg.rows import dict_row


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

    def __del__(self):
        self._client.close()
        self._connection.close()


class PostgresRepository(BasePostgresRepository):
    TABLE_NAME: str = ""

    def find(self, columns: str | None = None, condition: str | None = None):
        if not columns:
            columns = "*"
        if not condition:
            sql = f"SELECT {columns} FROM {self.TABLE_NAME}"
        else:
            sql = f"SELECT {columns} FROM {self.TABLE_NAME} WHERE {condition}"

        return self._client.execute(sql).fetchall()

    def update(self, update_values: dict[str, str], columns: str | None = None, condition: str | None = None):
        pass

    def delete(self, condition: str):
        pass
