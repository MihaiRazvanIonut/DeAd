from base_repository import *


class VisitRepository(PostgresRepository):
    TABLE_NAME = 'visits'


class VisitationsRepository(PostgresRepository):
    TABLE_NAME = 'visitations'

    def join_find_by_visit_id(self, visit_id: str):
        sql = f"""
            SELECT visit_role, nin, first_name, last_name, relationship
            FROM {self.TABLE_NAME} vis
            JOIN visits vt ON vt.id = vis.visit_id
            JOIN visitors vs ON vs.id = vis.visitor_id
            WHERE vis.visit_id = %s
        """
        try:
            return self._client.execute(sql, (visit_id,)).fetchall()

        except BaseException as e:
            raise exceptions.ServiceException(500, f'Database error: {e}')


class VisitorsRepository(PostgresRepository):
    TABLE_NAME = 'visitors'


class ActionRepository(PostgresRepository):
    TABLE_NAME = 'actions'


class MoodRepository(PostgresRepository):
    TABLE_NAME = 'mood_indexes'


class ItemsRepository(PostgresRepository):
    TABLE_NAME = 'items'
