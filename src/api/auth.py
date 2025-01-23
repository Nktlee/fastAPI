from fastapi import APIRouter, HTTPException, Response

from src.repositories.users import UsersRepository
from src.schemas.users import UserAdd, UserRequestAdd
from src.database import async_session_maker_null_pool
from src.services.auth import AuthService
from src.api.dependencies import UserIdDep, DBDep


router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register")
async def register_user(db: DBDep, data: UserRequestAdd):
    users = await db.users.get_all()
    emails = [user.email for user in users]
    if data.email in emails:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker_null_pool() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "ok"}


@router.post("/login")
async def login_user(data: UserRequestAdd, response: Response):
    async with async_session_maker_null_pool() as session:
        try:
            user = await UsersRepository(session).get_user_with_hashed_password(
                email=data.email
            )
        except:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")

        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)

        return {"access_token": access_token}


@router.get("/me")
async def get_me(user_id: UserIdDep):
    async with async_session_maker_null_pool() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")

    return {"status": "ok"}
