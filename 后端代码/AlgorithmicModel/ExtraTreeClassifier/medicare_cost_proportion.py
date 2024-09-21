from sqlalchemy import select

from db_connector.db_connector1.database import managed_async_session
from db_connector.db_connector1.models import MedicalRecord, PatientInfo

medicare_cost_columns = ['claimed_medicine_cost_sum','expensive_medicine_cost_sum','tcm_drug_cost_sum',
                         'herbal_medicine_cost_sum','claimed_examination_fee_sum','expensive_examination_fee',
                         'claimed_treatment_fee_sum','claimed_surgery_fee_sum','bed_fee_claimed_sum','medical_materials_cost_sum',
                         'high_cost_medical_materials_sum','self_paid_medical_materials_fee_sum','component_transfusion_claimed_sum',
                        'disposable_medical_materials_claimed_sum', 'other_costs_sum']

async def get_medicare_cost_proportion():
    """
    返回各种药费占比
    :return:
    """
    try:
        stmt1 = select(MedicalRecord.claimed_medicine_cost_sum)
        stmt2 = select(MedicalRecord.expensive_medicine_cost_sum)
        stmt3 = select(MedicalRecord.tcm_drug_cost_sum)
        stmt4 = select(MedicalRecord.herbal_medicine_cost_sum)
        stmt5 = select(MedicalRecord.claimed_examination_fee_sum)
        stmt6 = select(MedicalRecord.expensive_examination_fee)
        stmt7 = select(MedicalRecord.claimed_treatment_fee_sum)
        stmt8 = select(MedicalRecord.claimed_surgery_fee_sum)
        stmt9 = select(MedicalRecord.bed_fee_claimed_sum)
        stmt10 = select(MedicalRecord.medical_materials_cost_sum)
        stmt11 = select(MedicalRecord.high_cost_medical_materials_sum)
        stmt12 = select(MedicalRecord.self_paid_medical_materials_fee_sum)
        stmt13 = select(MedicalRecord.component_transfusion_claimed_sum)
        stmt14 = select(MedicalRecord.disposable_medical_materials_claimed_sum)
        stmt15 = select(MedicalRecord.other_costs_sum)

        data = []  # 装各种药品总费用
        async with managed_async_session() as session:
            res1 = await session.execute(stmt1)
            res2 = await session.execute(stmt2)
            res3 = await session.execute(stmt3)
            res4 = await session.execute(stmt4)
            res5 = await session.execute(stmt5)
            res6 = await session.execute(stmt6)
            res7 = await session.execute(stmt7)
            res8 = await session.execute(stmt8)
            res9 = await session.execute(stmt9)
            res10 = await session.execute(stmt10)
            res11 = await session.execute(stmt11)
            res12 = await session.execute(stmt12)
            res13 = await session.execute(stmt13)
            res14 = await session.execute(stmt14)
            res15 = await session.execute(stmt15)

            res_list = [res1,res2,res3,res4,res5,res6,res7,res8,res9,res10,res11,res12,res13,res14,res15]
            data = []  #装各种药品总费用
            for res in res_list:
                cost_sum = 0
                for res_tuple in res.fetchall():
                    cost_sum += res_tuple[0]
                data.append(cost_sum)

        print(data)
        total_cost = 0
        rate_list = []
        for cost in data:
            total_cost += cost
        #得到每种类型药费占比
        for cost in data:
            rate = round(cost/total_cost*100,2)
            rate_list.append(rate)

        cost_dict = {
            'claimed_medicine_cost_sum':rate_list[0],
            'expensive_medicine_cost_sum':rate_list[1],
            'tcm_drug_cost_sum':rate_list[2],
            'herbal_medicine_cost_sum':rate_list[3],
            'claimed_examination_fee_sum':rate_list[4],
            'expensive_examination_fee':rate_list[5],
            'claimed_treatment_fee_sum':rate_list[6],
            'claimed_surgery_fee_sum':rate_list[7],
            'bed_fee_claimed_sum':rate_list[8],
            'medical_materials_cost_sum':rate_list[9],
            'high_cost_medical_materials_sum':rate_list[10],
            'self_paid_medical_materials_fee_sum':rate_list[11],
            'component_transfusion_claimed_sum':rate_list[12],
            'disposable_medical_materials_claimed_sum':rate_list[13],
            'other_costs_sum':rate_list[14]
        }

        return cost_dict
    except Exception as e:
        return "失败"




