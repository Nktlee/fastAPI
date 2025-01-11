from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomWithRels
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(self, hotel_id: int, date_from: date, date_to: date):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
    
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)

        return [RoomWithRels.model_validate(model) for model in result.scalars().all()]
