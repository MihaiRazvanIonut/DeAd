import datetime
from dataclasses import dataclass


@dataclass
class PrisonerSchema:
    nin: str = ""
    first_name: str = ""
    last_name: str = ""
    date_of_birth: str = ""
    nationality: str = ""
    image: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: str | None = None
    emergency_contact: str = ""
    arrest_date: str = ""
    conviction_date: str = ""
    crime_committed: str = ""
    case_number: int = 0
    release_date: str = ""
    repeated_felon: bool = False


@dataclass
class PrisonersSchema:
    id: str = ""
    first_name: str = ""
    nin: str = ""
    case_number: int = 0
    release_date: str = ""


@dataclass
class PrisonersColumns:
    id: str = ""
    first_name: str = ""
    case_number: int = 0
    release_date: str = ""


@dataclass
class Prisoner:
    id: str = ""
    nin: str = ""
    first_name: str = ""
    last_name: str = ""
    date_of_birth: datetime.date = datetime.date.min
    nationality: str = ""
    image: str | None = None
    address: str | None = None
    phone_number: str | None = None
    email: str | None = None
    emergency_contact: str = ""
    arrest_date: datetime.date = datetime.date.min
    conviction_date: str = ""
    crime_committed: str = ""
    case_number: int = 0
    release_date: datetime.date = datetime.date.min
    repeated_felon: bool = False
