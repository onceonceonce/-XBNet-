import json
from fastapi import APIRouter
from AlgorithmicModel.ExtraTreeClassifier.get_fraud_proportion import  get_fraud_rate
from AlgorithmicModel.ExtraTreeClassifier.get_patient_fraud_message import get_fraud_message
from AlgorithmicModel.ExtraTreeClassifier.get_person_data import get_one_person
from AlgorithmicModel.ExtraTreeClassifier.get_person_expense_proportion import get_person_expense_proportion
from AlgorithmicModel.ExtraTreeClassifier.medicare_cost_proportion import get_medicare_cost_proportion
from AlgorithmicModel.ExtraTreeClassifier.prohibit_medicare_service import prohibit_service
from AlgorithmicModel.ExtraTreeClassifier.show_month_visits import show_visits_by_month
from AlgorithmicModel.ExtraTreeClassifier.show_person_fraud_rate import get_person_fraud_rate
from PydanticModel.patient_info import PatientInfoSchema
from Utils.read_data_from_database import read_data
from Utils.write_data_database import write_patient_info_into_database
from Utils.write_fraud_types_into_database import write_fraud_types
from db_connector.db_connector1.models import PatientInfo

query_router = APIRouter(prefix="/query")


@query_router.get("/whole-data-analysis")
async def get_whole_fraud_proportion():
    """
    获取整体数据欺诈比例
    :return:
    """
    # df = await read_data()
    # fraud_proportion,not_fraud_proportion = await get_proportion(df)
    # print(fraud_proportion,not_fraud_proportion)
    # print(df)
    # res1 = await write_patient_info_into_database(df)

    fraud_rate,not_fraud_rate = await get_fraud_rate()
    return {"fraud_rate":fraud_rate,"not_fraud_rate":not_fraud_rate}

@query_router.get("/person-fraud-info")
async def get_whole_person_info():
    """
    获取所有个人欺诈信息表的信息
    :return:
    """
    res = await get_fraud_message()
    return res

@query_router.get("/month-visits")
async def get_visits_by_month():
    """
    获取每月的就诊人数
    :return:每个月的就诊人数
    """
    # df = await read_data()
    # print(df)
    res = await show_visits_by_month()
    # print(month_json)
    # month_json = json.loads(res)
    return res


@query_router.get("/whole-person-info")
async def get_whoel_person_info(person_id: str):
    """
    获取所有个人的信息
    :return:
    """
    person = await get_one_person(person_id)
    return person

@query_router.get("/person-fraud-prob")
async def get_person_fraud_prob(person_id: str):
    """
    获取某个人欺诈，未欺诈概率
    :return:
    """
    res_tuple = await get_person_fraud_rate(person_id)

    return {"fraud_rate": res_tuple[0],"not_fraud_rate": res_tuple[1]}

@query_router.get("/expense-proportion")
async def get_expense_proportion():
    """
    获取整体所有费用所占比例
    :return:
    """
    medical_cost_rate_json = await get_medicare_cost_proportion()

    return medical_cost_rate_json



@query_router.get("/person-expense-proportion")
async def get_expense_proportion():
    """
    获取所有个人 所有费用所占比例
    :return:
    """
    res = await get_person_expense_proportion()

    return res


@query_router.get("/prohibit-list")
async def get_prohibit_list():
    """
    获取禁止参保名单
    :return:
    """
    lists = await prohibit_service()

    return lists



