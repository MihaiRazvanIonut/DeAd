import datetime
import sys

import argon2
import uuid6

import constants
import exceptions
import repository

user_repository = repository.UserRepository(f'dbname={constants.DB_NAME}')
invite_repository = repository.InviteRepository(f'dbname={constants.DB_NAME}')
ph = argon2.PasswordHasher()


def register(body: dict):
    register_schema = ('admin', 'username', 'invite_code', 'password')

    for key in body.keys():
        if key not in register_schema:
            raise exceptions.ServiceException(400, f'Bad request: invalid field {key}')

    invite = invite_repository.find_by_id(body['invite_code'])

    if not invite:
        raise exceptions.ServiceException(401, 'Unauthorized access')

    if invite['status'] == 1:
        raise exceptions.ServiceException(401, 'Unauthorized access')

    if user_repository.find_by_conditions({'username': body['username']}):
        raise exceptions.ServiceException(409, 'Conflict')

    hashed_pass = ph.hash(body['password'])

    try:
        invite['expiry_date'] = invite['expiry_date'].replace(tzinfo=datetime.UTC)
        if datetime.datetime.now(datetime.UTC) > invite['expiry_date']:
            invite_repository.delete_by_conditions({'id': body['invite_code'], 'creator_id': invite['creator_id']})
            invite_repository.commit()
            raise exceptions.ServiceException(400, f'Bad request: Expired invite code')

        else:
            invite_repository.update_by_id(body['invite_code'], {'status': 1, 'expiry_date': None})
            user_repository.insert(
                {
                    'id': uuid6.uuid7().int % sys.maxsize,
                    'username': body['username'],
                    'hash': hashed_pass,
                    'admin': body['admin']
                }
            )

    except exceptions.ServiceException as e:
        invite_repository.rollback()
        user_repository.rollback()
        raise e
    else:
        invite_repository.commit()
        user_repository.commit()
