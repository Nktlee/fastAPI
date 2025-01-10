from src.schemas.facilities import Facility, RoomFacility
from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm
from src.models.facilities import RoomsFacilitiesOrm


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility
