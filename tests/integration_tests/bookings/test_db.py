from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    add_booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=2, day=15),
        date_to=date(year=2025, month=2, day=20),
        price=1000,
    )
    new_booking = await db.bookings.add(add_booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id

    update_booking_data = BookingAdd(
        room_id=room_id,
        user_id=user_id,
        date_from=date(year=2025, month=2, day=15),
        date_to=date(year=2025, month=2, day=25),
        price=1000,
    )
    await db.bookings.edit(update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == update_booking_data.date_to

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

    await db.commit()
