from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.config import settings


engine = create_async_engine(settings.DB_URL)

assync_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)