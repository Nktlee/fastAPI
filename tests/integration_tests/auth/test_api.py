from httpx import AsyncClient

import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "1234", 200),
        ("test@example.com", "password123", 200),
        ("test2@example.com", "password123", 200),
        ("test@test.ru", "1234", 400),
    ],
)
async def test_register_user(
    email: str,
    password: str,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    response_register = await authenticated_ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert response_register.status_code == status_code


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("test@test.com", "1234", 200),
        ("test@example.com", "password123", 200),
        ("test2@example.com", "password123", 200),
        ("nktlee@example.com", "password123", 401),
        ("test2@example.com", "password12", 401),
    ],
)
async def test_login_user(
    email: str,
    password: str,
    status_code: int,
    authenticated_ac: AsyncClient,
):
    response_login = await authenticated_ac.post(
        "/auth/login", json={"email": email, "password": password}
    )
    assert response_login.status_code == status_code
    if status_code == 200:
        assert "access_token" in response_login.json()

        response_get_me = await authenticated_ac.get("/auth/me")
        assert response_get_me.json()["email"] == email


async def test_logout_user(authenticated_ac: AsyncClient):
    response_logout = await authenticated_ac.post("/auth/logout")
    assert response_logout.status_code == 200

    response_get_me = await authenticated_ac.get("/auth/me")
    assert response_get_me.status_code == 401
