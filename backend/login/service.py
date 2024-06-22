import datetime

import argon2
import uuid6

import constants
import exceptions
import repository

user_repository = repository.UserRepository(f'dbname={constants.DB_NAME}')
session_repository = repository.SessionRepository(f'dbname={constants.DB_NAME}')

ph = argon2.PasswordHasher()


def login(body: dict):
    response = {'session_id': ''}
    login_schema = ('username', 'password')

    for key in body.keys():
        if key not in login_schema:
            raise exceptions.ServiceException(400, f'Bad request: invalid field {key}')

    user = user_repository.find_by_conditions({'username': body['username']})

    if not user:
        raise exceptions.ServiceException(404, 'Not found')

    user = user[0]

    try:
        ph.verify(user['hash'], body['password'])

    except argon2.exceptions.VerifyMismatchError:
        raise exceptions.ServiceException(404, 'Not found')

    try:
        session = session_repository.find_by_conditions({'user_id': user['id']})
        new_session_flag = True
        if not session:
            response['session_id'] = uuid6.uuid7()
        else:
            session = session[0]
            session['expiry_date'] = session['expiry_date'].replace(tzinfo=datetime.UTC)
            if datetime.datetime.now(datetime.UTC) > session['expiry_date']:
                response['session_id'] = uuid6.uuid7()
                session_repository.delete_by_conditions({'id': session['id'], 'user_id': user['id']})
            else:
                new_session_flag = False
                response['session_id'] = session['id']

        if new_session_flag:
            session_repository.insert(
                {
                    'id': response['session_id'],
                    'user_id': user['id'],
                    'expiry_date': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)
                }
            )

    except exceptions.ServiceException as e:
        session_repository.rollback()
        raise e

    else:
        session_repository.commit()

    return response
