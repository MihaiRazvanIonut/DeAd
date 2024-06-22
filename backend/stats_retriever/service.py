import csv
import io
import json

import constants
import exceptions
import repository
import utils

mood_repository = repository.MoodIndexesRepository(f'dbname={constants.DB_NAME}')
item_repository = repository.ItemsRepository(f'dbname={constants.DB_NAME}')


def get_moods(query_param) -> bytes:
    __validate_query_param(query_param)
    results = list(mood_repository.join_with_prisoners_and_fetch())

    if not results:
        raise exceptions.ServiceException(404, 'Not found')

    for result in results:
        result['prisoner_id'] = utils.encode_id(result['prisoner_id'])

    stats = __generate_stats(results, query_param['format'])

    return stats


def get_moods_specific(path_id, query_param) -> bytes:
    __validate_query_param(query_param)

    path_id = utils.decode_id(path_id)

    results = (mood_repository.
               find_by_conditions({'prisoner_id': path_id}, 'arousal, flow, control, relaxation'))

    if not results:
        raise exceptions.ServiceException(404, 'Not found')

    stats = __generate_stats(results, query_param['format'])

    return stats


def get_items(query_param) -> bytes:
    __validate_query_param(query_param)
    results = item_repository.join_with_prisoners_and_fetch()

    if not results:
        raise exceptions.ServiceException(404, 'Not found')

    for result in results:
        result['prisoner_id'] = utils.encode_id(result['prisoner_id'])

    stats = __generate_stats(results, query_param['format'])

    return stats


def get_items_specific(path_id, query_param) -> bytes:
    __validate_query_param(query_param)

    path_id = utils.decode_id(path_id)

    results = item_repository.find_by_conditions({'prisoner_id': path_id}, 'name as object, action')

    if not results:
        raise exceptions.ServiceException(404, 'Not found')

    stats = __generate_stats(results, query_param['format'])

    return stats


def __validate_query_param(query_param: dict):
    if not query_param.get('format'):
        raise exceptions.ServiceException(400, 'Bad request: invalid query param')


def __generate_stats(stats_list: list, stats_format: str) -> bytes:
    match stats_format:
        case 'json':
            return json.dumps({'stats': stats_list}).encode('utf-8')

        case 'csv':
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=stats_list[0].keys())
            writer.writeheader()
            writer.writerows(stats_list)
            csv_output = output.getvalue().encode('utf-8')
            output.close()
            return csv_output

        case 'html':
            return utils.dict_to_html(stats_list).encode('utf-8')

        case _:
            raise exceptions.ServiceException(400, 'Bad request: invalid format')
