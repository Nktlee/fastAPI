import pytest

from tests.conftest import get_db_null_pool


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


@pytest.fixture(scope="module")
async def delete_all_bookings():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms", [
    (2, "2025-02-01", "2025-02-05", 1),
    (2, "2025-02-01", "2025-02-05", 2),
    (2, "2025-02-01", "2025-02-05", 3),
])
async def test_add_and_get_my_bookings(
    room_id,
    date_from,
    date_to,
    booked_rooms,
    delete_all_bookings,
    authenticated_ac,
):
    response = await authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == 200

    response_my_bookings = await authenticated_ac.get(
        "/bookings/me",
    )
    assert response_my_bookings.status_code == 200
    assert len(response_my_bookings.json()) == booked_rooms
