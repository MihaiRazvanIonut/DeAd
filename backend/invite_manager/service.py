import datetime

import uuid6

import constants
import exceptions
import repository
import utils

users_repository = repository.UserRepository(f'dbname={constants.DB_NAME}')
invites_repository = repository.InviteRepository(f'dbname={constants.DB_NAME}')


def new_invite(user_id: str, query_param) -> dict:
    if not users_repository.find_by_id(user_id, 'admin').get('admin'):
        raise exceptions.ServiceException(403, 'Forbidden: User is not an admin')

    if not query_param.get('admin'):
        raise exceptions.ServiceException(400, 'Bad request: Invalid query param')

    if query_param['admin'] == 'true':
        query_param['admin'] = True
    elif query_param['admin'] == 'false':
        query_param['admin'] = False
    else:
        raise exceptions.ServiceException(400, 'Bad request: Invalid query param value')

    user_invites = list(invites_repository.find_by_conditions({'creator_id': user_id}))

    unconfirmed_user_invites = [user_invite for user_invite in user_invites if user_invite['status'] == 0]

    if len(unconfirmed_user_invites) > 5:
        raise exceptions.ServiceException(400, 'Bad request: Too many invites generated')

    invite_code = str(uuid6.uuid7())
    new_entry = {
        'id': invite_code,
        'creator_id': user_id,
        'status': 0,
        'expiry_date': datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1),
        'admin': query_param['admin']
    }

    try:
        invites_repository.insert(new_entry)

    except exceptions.ServiceException as e:
        invites_repository.rollback()
        raise e

    else:
        invites_repository.commit()

    return {'invite_code': invite_code}


def get_invites(user_id: str) -> dict:
    if not users_repository.find_by_id(user_id, 'admin').get('admin'):
        raise exceptions.ServiceException(403, 'Forbidden: User is not an admin')

    raw_invites = list(invites_repository.find_by_conditions({'creator_id': user_id}))
    for raw_invite in raw_invites:
        raw_invite.pop('creator_id')
        utils.normalise_row(raw_invite)

    invites = {'invites': raw_invites}

    return invites
