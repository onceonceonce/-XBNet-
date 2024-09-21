from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import PatientInfo


async def get_fraud_rate():
    """
    获得整体欺诈比例，和未欺诈比例
    :return:欺诈比例，未欺诈比例
    """
    try:
        stmt = select(PatientInfo.prob_res).where(PatientInfo.prob_res == 1)
        # print(stmt)
        async with managed_async_session() as session:
            res = await session.execute(stmt)
            res_tuple = res.fetchall()

            # print(res_tuple)

            personal_ids = [tuple[0] for tuple in res_tuple]
            fraud_num = len(personal_ids)
            not_fraud_num = 16000-fraud_num

            fraud_rate = round(fraud_num/16000*100,2)
            not_fraud_rate = round(not_fraud_num/16000*100,2)

            # print(fraud_rate,not_fraud_rate)
            return fraud_rate,not_fraud_rate
    except Exception as e:
        return "获取欺诈失败","获取未欺诈失败"

