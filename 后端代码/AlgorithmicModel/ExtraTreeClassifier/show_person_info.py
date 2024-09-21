from pandas import DataFrame
from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord


async def show_person(df: DataFrame,id: str):
    """
    根据·id，返回指定用户信息
    :param df:
    :return:
    """
    try:
        stmt = select(MedicalRecord).where(MedicalRecord.personal_id == id)
        async with managed_async_session() as session:
            res = await session.excute(stmt)
            person_info = res.scalars().first()
            #返回个人信息，可能错误
            return person_info
    except Exception as e:
        return "获取个人信息失败"





