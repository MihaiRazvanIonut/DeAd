import constants
import exceptions
import repository

sessions_repository = repository.SessionRepository(f'dbname={constants.DB_NAME}')


def get_user_id_from_session(session_id: str) -> dict:
    response = {'user_id': ''}
    row = sessions_repository.find_by_conditions({'id': session_id}, 'user_id')
    if not row:
        raise exceptions.ServiceException(404, 'Not found')

    response['user_id'] = row[0]['user_id']

    return response
