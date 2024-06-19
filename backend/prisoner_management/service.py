import constants
import exceptions
import utils
from repository import PrisonerRepository

prisoner_repository = PrisonerRepository(f"dbname={constants.DB_NAME}")


def get_prisoner(prisoner_id: str):
    prisoner = prisoner_repository.find_by_id(condition_value=prisoner_id)
    if not prisoner:
        raise exceptions.ServiceException(404, 'Service error: No results found!')

    utils.normalise_row(prisoner)

    return prisoner
