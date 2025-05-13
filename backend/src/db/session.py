from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+asyncmy://kahoot_user:your_password@localhost/kahoot_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 取得非同步資料庫 Session 的 Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session