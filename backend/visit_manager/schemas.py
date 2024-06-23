from dataclasses import dataclass


@dataclass
class VisitorSchema:
    first_name: str = ''
    last_name: str = ''
    nin: str = ''
    relationship: str | None = None
    visit_role: int = 1


@dataclass
class ItemSchema:
    name: str = ''
    action: int = 1


@dataclass
class MoodSchema:
    arousal: int = 0
    flow: int = 0
    control: int = 0
    relaxation: int = 0


@dataclass
class VisitSchema:
    prisoner_id: str = ''
    visitors: list = list
    date: str = ''
    start_time: str = ''
    end_time: str = ''
    purpose: str = ''
    items: list | None = None
    restricted: bool = False
    summary: str = ''
    mood: MoodSchema = None
