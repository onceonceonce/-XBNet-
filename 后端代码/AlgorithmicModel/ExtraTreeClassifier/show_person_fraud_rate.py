from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord, PatientInfo

async def get_person_fraud_rate(person_id: str):
    """
    返回个人欺诈，未欺诈比例
    :param person_id:
    :return:
    """
    try:
        stmt = select(PatientInfo.fraud_prob,PatientInfo.not_fraud_prob).where(PatientInfo.personal_id == person_id)
        async with managed_async_session() as session:
            res = await session.execute(stmt)
            # print(res)
            res_tuple = res.fetchall()
            # print(res_tuple)
            return res_tuple[0]
    except Exception as e:
        return "获取失败"