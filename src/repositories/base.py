from pydantic import BaseModel

from sqlalchemy import select, insert, update, delete

from src.repositories.mappers.base import DataMapper


class BaseRepository:
    model = None
    mapper: DataMapper = None

    def __init__(self, session):
        self.session = session

    async def get_filtered(self, *filter, **filter_by) -> BaseModel:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)

        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self, *args, **kwargs) -> BaseModel:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter: dict) -> BaseModel:
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()

        if model is None:
            return None
        return self.mapper.map_to_domain_entity(model)

    async def add(self, data: BaseModel) -> BaseModel:
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)
        model = result.scalars().one()

        return self.mapper.map_to_domain_entity(model)

    async def add_bulk(self, data: list[BaseModel]) -> BaseModel:
        add_data_stmt = insert(self.model).values([item.model_dump() for item in data])
        await self.session.execute(add_data_stmt)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by: dict) -> None:
        query = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(query)

    async def delete(self, **filter_by: dict) -> None:
        query = delete(self.model).filter_by(**filter_by)
        await self.session.execute(query)
