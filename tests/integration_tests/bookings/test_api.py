import pytest


@pytest.mark.parametrize("room_id, date_from, date_to, status_code", [
    (2, "2025-02-01", "2025-02-05", 200),
    (2, "2025-02-01", "2025-02-05", 200),
    (2, "2025-02-01", "2025-02-05", 200),
    (2, "2025-02-01", "2025-02-05", 200),
    (2, "2025-02-01", "2025-02-05", 200),
    (2, "2025-02-01", "2025-02-05", 500),
    (2, "2025-03-01", "2025-03-05", 200),
])
async def test_add_booking(
    room_id,
    date_from,
    date_to,
    status_code,
    db,
    authenticated_ac,
):
    # room_id = (await db.rooms.get_all())[0].id
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )

    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(res, dict)
        assert res["status"] == "ok"
        assert "data" in res
