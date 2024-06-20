import datetime

import exceptions


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
