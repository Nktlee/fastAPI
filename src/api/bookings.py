from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequestAdd, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def add_booking(
    user_id: UserIdDep,
    db: DBDep,
    booking_data: BookingRequestAdd
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price

    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()

    return {"status": "ok", "data": booking}