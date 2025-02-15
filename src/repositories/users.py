from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.exceptions import UserNotFoundException
from src.repositories.mappers.mappers import UserDataMapper
from src.schemas.users import UsersWithHashedPassword
from src.repositories.base import BaseRepository
from src.models.users import UsersOrm


class UsersRepository(BaseRepository):
    model = UsersOrm
    mapper = UserDataMapper

    async def get_user_with_hashed_password(self, email: EmailStr):
        query = select(self.model).filter_by(email=email)
        result = await self.session.execute(query)
        try:
            model = result.scalar_one()
        except NoResultFound:
            raise UserNotFoundException

        return UsersWithHashedPassword.model_validate(model, from_attributes=True)
