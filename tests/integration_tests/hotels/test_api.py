async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2025-02-01",
            "date_to": "2025-02-05",
        },
    )
    assert response.status_code == 200
