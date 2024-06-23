import datetime
import sys

import uuid6

import constants
import exceptions
import repository
import schemas
import utils

mood_repository = repository.MoodRepository(f'dbname={constants.DB_NAME}')
visit_repository = repository.VisitRepository(f'dbname={constants.DB_NAME}')
visitor_repository = repository.VisitorsRepository(f'dbname={constants.DB_NAME}')
visitation_repository = repository.VisitationsRepository(f'dbname={constants.DB_NAME}')
action_repository = repository.ActionRepository(f'dbname={constants.DB_NAME}')
items_repository = repository.ItemsRepository(f'dbname={constants.DB_NAME}')

datetime_format = "%Y-%m-%d %H:%M:%S.%f"
date_format = "%Y-%m-%d"


def get_visit(visit_id: str):
    long_visit_id = utils.decode_id(visit_id)
    visit = visit_repository.find_by_id(long_visit_id)
    if not visit:
        raise exceptions.ServiceException(404, 'Not found')

    visit['id'] = utils.encode_id(visit['id'])
    visit['prisoner_id'] = utils.encode_id(visit['prisoner_id'])

    utils.normalise_row(visit)

    mood = mood_repository.find_by_conditions(
        {'visit_id': long_visit_id},
        'arousal, flow, control, relaxation'
    )
    if mood:
        visit['mood'] = mood[0]

    items = items_repository.find_by_conditions(
        {'visit_id': long_visit_id},
        'name, action'
    )
    if items:
        visit['items'] = list(items)
    visit['visitors'] = list(visitation_repository
                             .join_find_by_visit_id(long_visit_id,
                                                    'visit_role, nin, first_name, last_name, relationship'))
    return visit


def update_visit(visit_id: str, user_id: str, body: dict):
    __validation_helper(schemas.VisitSchema(), body)
    visit_id = utils.decode_id(visit_id)
    old_visit = visit_repository.find_by_id(visit_id)
    if not old_visit:
        raise exceptions.ServiceException(404, 'Not found')

    visitors = body.pop('visitors')
    mood = body.pop('mood')
    items = body.pop('items')

    try:
        visit_repository.update_by_id(visit_id, body)
        visit_repository.commit()

        if visitors:
            old_visitors = list(visitation_repository.join_find_by_visit_id(visit_id, 'vis.id'))
            visitation_repository.delete_by_conditions({'visit_id': visit_id})
            visitation_repository.commit()
            for old_visitor in old_visitors:
                visitor_repository.delete_by_conditions({'id': old_visitor['id']})
            visitation_repository.commit()
            for visitor in visitors:
                __validation_helper(schemas.VisitorSchema(), visitor)
                visitor_role = visitor.pop('visit_role')
                visitor['id'] = __generate_id()
                visitor_repository.insert(visitor)
                visitor_repository.commit()
                visitation_repository.insert(
                    {
                        'id': __generate_id(),
                        'visitor_id': visitor['id'],
                        'visit_id': visit_id,
                        'visit_role': visitor_role
                    }
                )
                visitation_repository.commit()

        if mood:
            __validation_helper(schemas.MoodSchema(), mood)
            mood_id = mood_repository.find_by_conditions({'visit_id': visit_id}, 'id')
            if mood_id:
                mood_id = mood_id[0]['id']
                mood_repository.update_by_id(mood_id, mood)
                mood_repository.commit()

        if items:
            items_repository.delete_by_conditions({'visit_id': visit_id})
            items_repository.commit()
            for item in items:
                __validation_helper(schemas.ItemSchema(), item)
                item['id'] = __generate_id()
                item['prisoner_id'] = old_visit['prisoner_id']
                item['visit_id'] = visit_id
                items_repository.insert(item)
                items_repository.commit()

        action_repository.insert({
            'id': __generate_id(),
            'type': 'update',
            'user_id': user_id,
            'visit_id': visit_id,
            'time': datetime.datetime.now(datetime.UTC)
        })
        action_repository.commit()

    except exceptions.ServiceException as e:
        action_repository.rollback()
        items_repository.rollback()
        mood_repository.rollback()
        visitation_repository.rollback()
        visitor_repository.rollback()
        visit_repository.rollback()
        raise e


def new_visit(user_id: str, body: dict):
    __validation_helper(schemas.VisitSchema(), body)
    body['prisoner_id'] = utils.decode_id(body['prisoner_id'])
    body['date'] = datetime.datetime.strptime(body['date'], date_format).date()
    body['start_time'] = datetime.datetime.strptime(body['start_time'], datetime_format)
    body['end_time'] = datetime.datetime.strptime(body['end_time'], datetime_format)

    visitors = body.pop('visitors')
    mood = body.pop('mood')
    items = body.pop('items')

    try:
        new_visit_id = __generate_id()
        body['id'] = new_visit_id
        visit_repository.insert(body)
        visit_repository.commit()

        if visitors:
            for visitor in visitors:
                __validation_helper(schemas.VisitorSchema(), visitor)
                visitor_role = visitor.pop('visit_role')
                visitor['id'] = __generate_id()
                visitor_repository.insert(visitor)
                visitor_repository.commit()
                visitation_repository.insert(
                    {
                        'id': __generate_id(),
                        'visitor_id': visitor['id'],
                        'visit_id': new_visit_id,
                        'visit_role': visitor_role
                    }
                )
                visitation_repository.commit()

        else:
            raise exceptions.ServiceException(400, 'Bad request: a visit should have at least one visitor')

        if mood:
            __validation_helper(schemas.MoodSchema(), mood)
            mood['id'] = __generate_id()
            mood['prisoner_id'] = body['prisoner_id']
            mood['visit_id'] = new_visit_id
            mood_repository.insert(mood)
            mood_repository.commit()
        else:
            raise exceptions.ServiceException(400, 'Bad request: a visit should have a mood index')

        if items:
            for item in items:
                __validation_helper(schemas.ItemSchema(), item)
                item['id'] = __generate_id()
                item['prisoner_id'] = body['prisoner_id']
                item['visit_id'] = new_visit_id
                items_repository.insert(item)
                items_repository.commit()

        action_repository.insert({
            'id': __generate_id(),
            'type': 'create',
            'user_id': user_id,
            'visit_id': new_visit_id,
            'time': datetime.datetime.now(datetime.UTC)
        })
        action_repository.commit()

    except exceptions.ServiceException as e:
        action_repository.rollback()
        items_repository.rollback()
        mood_repository.rollback()
        visitation_repository.rollback()
        visitor_repository.rollback()
        visit_repository.rollback()
        raise e

    return constants.SERVICE_URI + f'/{utils.encode_id(new_visit_id)}'


def get_visit_search(query_params: dict):
    search_field_value_schema = ('id', 'purpose', 'date')
    if len(query_params) != 1:
        raise exceptions.ServiceException(400, 'Bad request: invalid query params')

    if list(query_params.items())[0][0] not in search_field_value_schema:
        raise exceptions.ServiceException(400, 'Bad request: invalid query params')

    if query_params.get('id'):
        query_params['id'] = utils.decode_id(query_params['id'])

    results = list(visit_repository.find_by_conditions(query_params, 'id, purpose, date'))

    for result in results:
        result['id'] = utils.encode_id(result['id'])
        utils.normalise_row(result)

    return {'visits': results}


def get_visits():
    results = list(visit_repository.find('id, purpose, date'))
    for result in results:
        utils.normalise_row(result)
        result['id'] = utils.encode_id(result['id'])

    return {'visits': results}


def __validation_helper(schema, body):
    schema = list(vars(schema).keys())
    for key in body.keys():
        if key not in schema:
            raise exceptions.ServiceException(
                400,
                f'Bad request: invalid post body for field {key}'
            )


def __generate_id():
    return str(uuid6.uuid7().int % sys.maxsize)
