async def test_add_booking(db, authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2025-02-01",
            "date_to": "2025-02-05",
        }
    )

    assert response.status_code == 200
