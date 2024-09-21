from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord, PatientInfo

async def prohibit_service():
    """

    :return:
    """
    try:
        stmt = select(PatientInfo.personal_id).where(PatientInfo.fraud_prob>0.9)
        async with managed_async_session() as session:
            res = await session.execute(stmt)
            res_tuple = res.fetchall()
            prohibit_list = [res[0] for res in res_tuple]
            prohibit_list_id = [{'id': id} for id in prohibit_list]
            return prohibit_list_id
    except Exception as e:
        return "失败"
