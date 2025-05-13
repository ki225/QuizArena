from sqlalchemy.orm import declarative_base

Base = declarative_base()

async def init_db(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)