import pandas as pd

from db_connector.db_connector1.database import engine2


async def read_data():
    """
    从数据库中读取数据，返回医保所有数据
    :return: dataframe
    """
    try:
        df = pd.read_sql_table("medical_records1", engine2)
    except Exception as e:
        return "读取失败"

    return df


async def read_patient_data():
    """
    从数据库中读取数据，返回所有人具体信息
    :return: dataframe
    """
    try:
        df = pd.read_sql_table("patient_info", engine2)
    except Exception as e:
        return "读取失败"

    return df
