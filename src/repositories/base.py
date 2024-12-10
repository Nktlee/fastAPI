from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs) -> BaseModel:
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()
    
    async def get_one_or_none(self, **filter: dict) -> BaseModel:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()
    
    async def add(self, data: BaseModel) -> BaseModel:
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()
    
    async def edit(self, data: BaseModel, id: int) -> None:
        query = update(self.model).where(self.model.id == id).values(**data.model_dump())
        await self.session.execute(query)

    async def delete(self, id: int) -> None:
        query = delete(self.model).where(self.model.id == id)
        await self.session.execute(query)
