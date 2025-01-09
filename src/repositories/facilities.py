from src.schemas.facilities import Facility
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility
