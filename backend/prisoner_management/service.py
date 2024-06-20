import datetime
import sys

import sqids
import uuid6

import constants
import exceptions
import schemas
import utils
from repository import PrisonerRepository

prisoner_repository = PrisonerRepository(f'dbname={constants.DB_NAME}')
shortener = sqids.Sqids(min_length=8)


def get_prisoner(prisoner_id: str):
    try:
        prisoner_id = str(shortener.decode(prisoner_id)[0])

    except BaseException:
        raise exceptions.ServiceException(400, 'Bad request: invalid id')

    prisoner = prisoner_repository.find_by_id(condition_value=prisoner_id)

    if not prisoner:
        raise exceptions.ServiceException(404, 'Service error: No results found!')

    utils.normalise_row(prisoner)
    prisoner["id"] = shortener.encode([int(prisoner["id"])])

    return prisoner


def new_prisoner(prisoner_dto: dict) -> str:
    prisoner_schema = schemas.PrisonerSchema()
    prisoner = schemas.Prisoner()
    utils.map_schema(prisoner_dto, prisoner_schema)
    new_id = uuid6.uuid7().int % sys.maxsize
    prisoner.id = str(new_id)
    prisoner_vars = vars(prisoner)

    for field, value in vars(prisoner_schema).items():
        normalised_value = value
        if isinstance(prisoner_vars[field], datetime.date):
            normalised_value = datetime.datetime.strptime(value, "%Y-%m-%d").date()

        prisoner_vars[field] = normalised_value

    fields = str(list(prisoner_vars.keys())[0])
    values = list()
    values.append(list(prisoner_vars.items())[0][1])
    for key, value in list(prisoner_vars.items())[1:]:
        fields += f', {key}'
        values.append(value)

    prisoner_repository.insert(fields, values)
    prisoner_repository.commit()

    return constants.SERVICE_URI + f'/{shortener.encode([new_id])}' + '\n'
