from fastapi import APIRouter, HTTPException
from fastapi_cache.decorator import cache

from exceptions import AllRoomsAreBookedException, ObjectNotFoundException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequestAdd, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение всех бронирований")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me", summary="Получение всех бронирований пользователя")
@cache(expire=10)
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("", summary="Добавление бронирований")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingRequestAdd):
    try:
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    hotel = await db.hotels.get_one(id=room.hotel_id)
    room_price = room.price

    _booking_data = BookingAdd(user_id=user_id, price=room_price, **booking_data.model_dump())
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=hotel.id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()

    return {"status": "ok", "data": booking}
