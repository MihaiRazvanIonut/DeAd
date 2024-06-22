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


def schema_from_dto(dto: dict, schema):
    for field in vars(schema).keys():
        if not dto.get(field):
            raise exceptions.ServiceException(400, f'Bad request: {field} does not exist')
        else:
            vars(schema)[field] = dto[field]


def validate_dto(dto: dict, schema):
    schema_keys = list(vars(schema).keys())
    for field in dto.keys():
        if field not in schema_keys:
            raise exceptions.ServiceException(400, f'Bad request: unrecognised field {field}')


def get_flat_fields_from_schema(schema) -> str:
    schema_vars = list(vars(schema).keys())
    flat_fields = f'{schema_vars[0]}'
    for var in schema_vars:
        flat_fields += f', {var}'

    return flat_fields


def decode_id(entry_id: str):
    try:
        return str(shortener.decode(entry_id)[0])

    except BaseException:
        raise exceptions.ServiceException(400, 'Bad request: invalid id')


def encode_id(entry_id: str):
    return shortener.encode([int(entry_id)])


def dict_to_html(data):
    html_str = """
    <html>
    <head>
        <title>Statistics</title>
        <style>
            table {
                width: 50%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid black;
            }
            th, td {
                padding: 8px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
        </style>
    </head>
    <body>
        <h2>Statistics Data</h2>
        <table>
            <tr>
    """

    headers = data[0].keys()
    for header in headers:
        html_str += f"<th>{header}</th>"
    html_str += "</tr>"

    for row in data:
        html_str += "<tr>"
        for header in headers:
            html_str += f"<td>{row[header]}</td>"
        html_str += "</tr>"

    html_str += """
        </table>
    </body>
    </html>
    """

    return html_str
