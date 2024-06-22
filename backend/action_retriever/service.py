import constants
import utils
from repository import *

actions_repository = ActionRepository(f'dbname={constants.DB_NAME}')


def get_actions() -> dict:
    actions = actions_repository.find_join_with_user('type, username, visit_id, time')
    actions_response = {'actions': []}
    for action in actions:
        action['visit_id'] = utils.encode_id(action['visit_id'])
        utils.normalise_row(action)
        actions_response['actions'].append(action)

    return actions_response


def get_user_actions(user_id: str):
    user_actions = actions_repository.find_by_conditions({'user_id': user_id}, 'type, visit_id, time')
    user_actions_response = {'actions': []}
    for action in user_actions:
        action['visit_id'] = utils.encode_id(action['visit_id'])
        utils.normalise_row(action)
        user_actions_response['actions'].append(action)

    return user_actions_response
