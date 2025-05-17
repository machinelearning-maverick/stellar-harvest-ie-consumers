from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from ..settings import settings

engine = create_async_engine(settings.database_url, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def init_db():
    # auto-create -> call Base.metadata.create_all(engine)
    pass


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session
