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


def get_prisoners(query_params: dict) -> dict:
    prisoners = {'prisoners': []}
    utils.validate_dto(query_params, schemas.PrisonersSchema)
    if query_params.get('id'):
        query_params['id'] = utils.decode_id(query_params['id'])
    prisoner_orm_vars = vars(schemas.Prisoner())

    try:
        for field, value in query_params.items():
            if isinstance(prisoner_orm_vars[field], datetime.date):
                normalised_value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
            else:
                normalised_value = str(value)
            query_params[field] = normalised_value
    except BaseException:
        raise exceptions.ServiceException(400, 'Bad request: invalid query param value type')

    columns = utils.get_flat_fields_from_schema(schemas.PrisonersColumns())
    results = prisoner_repository.find(query_params, columns)

    for result in results:
        utils.normalise_row(result)
        prisoners['prisoners'].append(result)

    return prisoners
