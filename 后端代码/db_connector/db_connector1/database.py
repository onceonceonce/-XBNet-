from contextlib import asynccontextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from db_connector.db_connector1.models import Base

from configparser import ConfigParser

# conf = ConfigParser()  # 实例化一个ConfigParser对象
# conf.read('D:\DangerousDriving\DangerousDrivingAnalysisBackend\Modules\ThirdPartyPlatformInteractionModule\config.ini')

# print(conf['database']['DATABASE_URL'])
# 后期再修改
# DATABASE_URL = "sqlite+aiosqlite:///database.db"
# DATABASE_URL = conf['database']['DATABASE_URL']  mysql+aiomysql://root:123456@localhost/dangerousdriving
# 异步连接引擎（如果你的FastAPI应用是异步的）

DATABASE_URL = "mysql+aiomysql://medicare_fraud:ECKhZtrDzcaLstbr@47.100.173.31/medicare_fraud"
engine = create_async_engine(DATABASE_URL, future=True)

engine2 = create_engine('mysql+pymysql://medicare_fraud:ECKhZtrDzcaLstbr@47.100.173.31/medicare_fraud')
# 用于创建会话的异步会话工厂,async_session_maker这只是一个类
async_session_maker = sessionmaker(engine, class_=AsyncSession)


@asynccontextmanager
async def managed_async_session():
    """
    使用 @asynccontextmanager 创建一个异步上下文管理器，提供了对数据库会话的便捷管理，包括事务处理和资源释放
    从而简化了异步环境下数据库操作的编码逻辑。每个请求都有一个单独的session会话
    :return:
    """
    async_session = async_session_maker()
    try:
        yield async_session
        await async_session.commit()
    except Exception:
        await async_session.rollback()
    finally:
        await async_session.close()


async def third_create_tables():
    """
    创建数据库表
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


