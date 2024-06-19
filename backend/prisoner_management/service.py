import constants
from repository import PrisonerRepository

prisoner_repository = PrisonerRepository(f"dbname={constants.DB_NAME}")


def get_all_prisoners():
    result = prisoner_repository.find()
    return result
