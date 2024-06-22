from base_repository import *


class MoodIndexesRepository(PostgresRepository):
    TABLE_NAME = 'mood_indexes'

    def join_with_prisoners_and_fetch(self):
        sql = f"""
            SELECT p.id as prisoner_id, p.first_name || ' ' || p.last_name as full_name, arousal, flow, control, relaxation
            FROM {self.TABLE_NAME} m
            JOIN prisoners p on p.id = m.prisoner_id
        """
        try:
            return self._client.execute(sql).fetchall()
        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')


class ItemsRepository(PostgresRepository):
    TABLE_NAME = 'items'

    def join_with_prisoners_and_fetch(self):
        sql = f"""
            SELECT p.id as prisoner_id, p.first_name || ' ' || p.last_name as full_name, name as object, action
            FROM {self.TABLE_NAME} m
            JOIN prisoners p on p.id = m.prisoner_id
        """
        try:
            return self._client.execute(sql).fetchall()
        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')
