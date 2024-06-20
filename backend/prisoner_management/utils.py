import datetime

from sqids import sqids

import exceptions

shortener = sqids.Sqids(min_length=8)


def normalise_row(row: dict):
    for key, value in row.items():
        normalised_value = value
        if isinstance(value, datetime.date):
            normalised_value = str(value)

        row[key] = normalised_value


def map_schema(request_data: dict, schema):
    for field in vars(schema).keys():
        if not request_data.get(field):
            raise exceptions.ServiceException(400, f'Bad request: {field} does not exist')
        else:
            vars(schema)[field] = request_data[field]


def decode_id(entry_id: str):
    try:
        return str(shortener.decode(entry_id)[0])

    except BaseException:
        raise exceptions.ServiceException(400, 'Bad request: invalid id')


def encode_id(entry_id: str):
    return shortener.encode([int(entry_id)])
