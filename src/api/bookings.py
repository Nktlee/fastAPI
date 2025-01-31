from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
)
from src.services.bookings import BookingService
from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingRequestAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get("", summary="Получение всех бронирований")
@cache(expire=10)
async def get_bookings(db: DBDep):
    return await BookingService(db).get_bookings()


@router.get("/me", summary="Получение всех бронирований пользователя")
@cache(expire=10)
async def get_my_bookings(db: DBDep, user_id: UserIdDep):
    return await BookingService(db).get_my_bookings(user_id)


@router.post("", summary="Добавление бронирований")
async def create_booking(user_id: UserIdDep, db: DBDep, booking_data: BookingRequestAdd):
    try:
        booking = await BookingService(db).create_booking(booking_data, user_id)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException

    return {"status": "ok", "data": booking}
