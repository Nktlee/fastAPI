from src.exceptions import (
    AllRoomsAreBookedException,
    AllRoomsAreBookedHTTPException,
    ObjectNotFoundException,
    RoomNotFoundException,
)
from src.schemas.bookings import BookingAdd, BookingRequestAdd
from src.services.base import BaseService
from src.api.dependencies import UserIdDep


class BookingService(BaseService):
    async def get_bookings(self):
        return await self.db.bookings.get_all()

    async def get_my_bookings(self, user_id: UserIdDep):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def create_booking(self, booking_data: BookingRequestAdd, user_id: UserIdDep):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        hotel = await self.db.hotels.get_one(id=room.hotel_id)
        room_price = room.price

        _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
        try:
            booking = await self.db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
        except AllRoomsAreBookedException:
            raise AllRoomsAreBookedHTTPException
        await self.db.commit()

        return booking
