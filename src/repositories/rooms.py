from src.schemas.rooms import Room
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    # async def get_all(
    #         self,
    #         hotel_id: int,
    #         title: str,
    # ) -> list[Room]:
    #     query = select(RoomsOrm)
    #     if hotel_id:
    #         query = query.filter(RoomsOrm.hotel_id == hotel_id)
    #     if title:
    #         query = query.filter(func.lower(RoomsOrm.title).contains(title.strip().lower()))
    #     result = await self.session.execute(query)

    #     return [Room.model_validate(room, from_attributes=True) for room in result.scalars().all()]
