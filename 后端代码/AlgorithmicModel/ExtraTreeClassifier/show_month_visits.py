import json
from collections import Counter

from pandas import DataFrame
from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord, PatientInfo


async def show_visits_by_month():
    """
    获取用户就诊月份
    :param
    :return: json
    """
    try:
        stmt = select(MedicalRecord.months_of_visits,MedicalRecord.reserved_field)
        async with managed_async_session() as session:
            res = await session.execute(stmt)
            # res_data = list(res)     这里特别神奇，用了list之后就好了，之前用all不行，现在也行了
            res_data = res.fetchall()
            # print(res_data)
            # for month in range(1,13):

            # print(res_data)
            # month_visits_list = [res[0] for res in res_data]

            counter = Counter(res_data)
            # print(counter)
            counter_dict = dict(counter)
            # 储存每个月欺诈，未欺诈人数
            statistics = {}

            for key, value in counter_dict.items():
                number, boolean = key
                num_str = str(number)
                if num_str not in statistics:
                    statistics[num_str] = {"True": 0, "False": 0}
                if boolean:
                    statistics[num_str]["True"] += value
                else:
                    statistics[num_str]["False"] += value

            # print(statistics)
            sorted_statistics = {key: statistics[key] for key in sorted(statistics)}
            return sorted_statistics

    except Exception as e:
        return "失败"

