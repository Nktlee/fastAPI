from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=2, day=15),
        date_to=date(year=2025, month=2, day=20),
        price=1000
    )
    await db.bookings.add(booking_data)
    await db.commit()
