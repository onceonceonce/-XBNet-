import numpy as np
from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord, PatientInfo

medicare_cost_columns = ['claimed_medicine_cost_sum','expensive_medicine_cost_sum','tcm_drug_cost_sum',
                         'herbal_medicine_cost_sum','claimed_examination_fee_sum','expensive_examination_fee',
                         'claimed_treatment_fee_sum','medical_materials_cost_sum']

async def get_person_expense_proportion():
    """
    返回各种药费占比
    :return:
    """
    try:
        stmt1 = select(MedicalRecord.claimed_medicine_cost_sum,MedicalRecord.expensive_medicine_cost_sum,MedicalRecord.tcm_drug_cost_sum,
                       MedicalRecord.herbal_medicine_cost_sum,MedicalRecord.claimed_examination_fee_sum,MedicalRecord.expensive_examination_fee,
                       MedicalRecord.claimed_treatment_fee_sum,MedicalRecord.medical_materials_cost_sum)

        async with managed_async_session() as session:
            res = await session.execute(stmt1)
            res_tuples = res.fetchall()
            all_person_medicine = [list(tuple) for tuple in res_tuples]
            # print(all_person_medicine)

            # print(res)
            # print(type(all_person_medicine))
            # temp = np.array(all_person_medicine)
            # print(temp)
            # print(type(temp))
            return all_person_medicine

        return "读取成功"
    except Exception as e:
        return "失败"






