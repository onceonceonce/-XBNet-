from sqlalchemy import select

from AlgorithmicModel.ExtraTreeClassifier.get_person_expense_proportion import get_person_expense_proportion
from AlgorithmicModel.ExtraTreeClassifier.medicare_cost_proportion import get_medicare_cost_proportion
from PydanticModel.patient_info import get_PatientInfoSchema
from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord, PatientInfo


async def get_fraud_message():
    """
    返回所有用户欺诈类型信息
    :param df:
    :return:
        """
    try:
        stmt = select(PatientInfo.personal_id,PatientInfo.prob_res,PatientInfo.fraud_prob,PatientInfo.fraud_types)
        async with managed_async_session() as session:
            res = await session.execute(stmt)
            res_tuple = res.fetchall()
            # print(res_tuple)
            # print(res_tuple)
            personal_list = []
            index = 0
            res = await get_person_expense_proportion()
            # print(res[0])
            for person_fraud_info in res_tuple:
                # 要加await关键字，这是一个协程对象
                # print(index)
                person = await get_PatientInfoSchema(personal_id=person_fraud_info[0],prob_res=person_fraud_info[1],
                                               fraud_prob=person_fraud_info[2],fraud_types=person_fraud_info[3],
                                            # pos = res[index],
                                           feature1=['基本统筹基金支付金额_SUM','本次审批金额_SUM','药品费申报金额_SUM','药品费发生金额_SUM'],
                                            feature2=['月药品金额_MAX','月统筹金额_AVG','治疗费申报金额_SUM','ALL_SUM']
                                            )

                # index += 1
                # print(person)
            # prohibit_list = [res[0] for res in res_tuple]
                personal_list.append(person)
            for index in range(len(res)):
                personal_list[index].pos = res[index]

            return personal_list
    except Exception as e:
        return "失败"