import datetime
import sys

import uuid6

import constants
import exceptions
import schemas
import utils
from repository import PrisonerRepository

prisoner_repository = PrisonerRepository(f'dbname={constants.DB_NAME}')


def get_prisoner(prisoner_id: str):
    prisoner_id = utils.decode_id(prisoner_id)
    prisoner = prisoner_repository.find_by_id(id_value=prisoner_id)

    if not prisoner:
        raise exceptions.ServiceException(404, 'Service error: No results found!')

    utils.normalise_row(prisoner)
    prisoner["id"] = utils.encode_id(prisoner["id"])

    return prisoner


def update_prisoner(prisoner_id: str, prisoner_dto: dict):
    prisoner_id = utils.decode_id(prisoner_id)
    utils.validate_dto(prisoner_dto, schemas.PrisonerSchema())
    prisoner_vars = vars(schemas.Prisoner)
    for field, value in prisoner_dto.items():
        normalised_value = value
        if isinstance(prisoner_vars[field], datetime.date):
            normalised_value = datetime.datetime.strptime(value, "%Y-%m-%d").date()

        prisoner_dto[field] = normalised_value

    prisoner_repository.update_by_id(prisoner_id, prisoner_dto)
    prisoner_repository.commit()


def new_prisoner(prisoner_dto: dict) -> str:
    prisoner_schema = schemas.PrisonerSchema()
    prisoner = schemas.Prisoner()
    utils.schema_from_dto(prisoner_dto, prisoner_schema)
    new_id = uuid6.uuid7().int % sys.maxsize
    prisoner.id = str(new_id)
    prisoner_vars = vars(prisoner)

    for field, value in vars(prisoner_schema).items():
        normalised_value = value
        if isinstance(prisoner_vars[field], datetime.date):
            normalised_value = datetime.datetime.strptime(value, "%Y-%m-%d").date()

        prisoner_vars[field] = normalised_value

    prisoner_repository.insert(prisoner_vars)
    prisoner_repository.commit()

    return constants.SERVICE_URI + f'/{utils.encode_id(prisoner.id)}' + '\n'
