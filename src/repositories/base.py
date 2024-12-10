from sqlalchemy import select, insert


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()
    
    async def get_one_or_none(self, **filter):
        query = select(self.model).filter_by(**filter)
        result = await self.session.execute(query)

        return result.scalars().one_or_none()
    
    async def add(self, data):
        add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(add_data_stmt)

        return result.scalars().one()
