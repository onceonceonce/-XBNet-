import matplotlib.pyplot as plt
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sqlalchemy import select
from Utils.pre_process_data_function import pre_process
from Utils.write_fraud_types_into_database import write_fraud_types

plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题
import warnings
warnings.filterwarnings('ignore')

important_columns_first = ['basic_coordinated_fund_payment_sum', 'current_approval_amount_sum',
                           'claimed_medicine_cost_sum', 'medicine_cost_sum',
                           'max_medicine_amount_per_month', 'avg_total_amount_per_month', 'claimed_treatment_fee_sum',
                           'all_sum']
# 月药品金额_MAX(医院_药品_MAX和这个差不多，要稍微差一点)

important_columns_second = ['coordinated_payment_sum', 'max_visits_per_month', 'total_visits_count',
                            'amount_above_deductible_self_paid_sum',
                            'available_account_reimbursement_sum', 'non_account_payment_sum',
                            'hospital_avg_coordinated_fund',
                            'max_days_visited_per_month', 'avg_days_visited_per_month', 'max_total_amount_per_month']
important_columns_third = ['hospital_max_coordinated_fund', 'expensive_medicine_cost_sum',
                           'individual_proportion_burden_sum',
                           'hospital_medical_assistance_application_sum', 'personal_account_balance_sum',
                           'days_visiting_two_hospitals']

important_columns_total = important_columns_first + important_columns_second + important_columns_third

import numpy as np
from pandas import DataFrame

from db_connector.db_connector1.database import engine2, managed_async_session
from db_connector.db_connector1.models import MedicalRecord


async def write_data_into_database(df: DataFrame):

    try:
        # 原来的csv基础之上增加一列id用来标识
        personal_id = np.arange(1, len(df) + 1)
        # 假设 personal_id 已经被定义为一个数组
        string_personal_id = personal_id.astype(str)

        df.insert(0, 'personal_id', string_personal_id)
        # 调整编号
        df['personal_id'] = '2024' + df['personal_id'].str.zfill(5)
        # 获得dataframe列表名
        chinese_columns = df.columns.tolist()
        # 获得数据库相应字段名
        database_columns = []
        for column in MedicalRecord.__table__.columns:
            database_columns.append(column.name)
        mapper = dict(zip(chinese_columns, database_columns))  # 创建列名映射字典
        # 将原来的中文名映射为英文
        exchange_columns_df = df[list(mapper.keys())].rename(columns=mapper)
        # print(exchange_columns_df)
        # print(personal_id)

        # 将原数据中的数据写道数据库中
        exchange_columns_df.to_sql(name='medical_records1', con=engine2, if_exists='replace', index=False)

        # 将原数据析处理过 即病人信息返回
        res = await write_patient_info_into_database(exchange_columns_df)
        # 将病人信息写入数据库中

        res2 = await write_fraud_types(exchange_columns_df,res)

        return res2
    except Exception as e:
        print(e)
        return "出现错误，医疗原数据上传数据失败"

    return "上传数据成功"

async def write_patient_info_into_database(df: DataFrame):
    """
    传入原始的dataframe，使用得到的clf，依次判断每个人的信息
    :param df:
    :return:
    """
    # clf = return_clf(df)
    # 最后两列res，is_outier
    try:
        process_df = await pre_process(df)

        # 使用smote的数据构建模型，原数据测试
        X_train_important, X_valid_important, y_train_important, y_valid_important = train_test_split(
            process_df.loc[:, important_columns_total].values, process_df.iloc[:, -2].values, test_size=0.2,
            random_state=66)

        extraTree_clf = ExtraTreesClassifier(random_state=66)
        clf = extraTree_clf.fit(X_train_important, y_train_important)

        #获得每个人的,易知结果的序号与测试数据集序号是一一对应的
        predict_res = clf.predict(df.loc[:,important_columns_total].values)  #结果
        predict_prob = clf.predict_proba(df.loc[:,important_columns_total].values)  #欺诈可能性

        person_ids = df.iloc[:,0]
        #将数据依次插入到表中
        personal_id_list = list(person_ids)
        personal_id_list_str = [str(id_) for id_ in personal_id_list]

        prob_res_list = list(predict_res)
        fraud_prob_list = []
        not_fraud_prob_list = []
        for array in predict_prob:
            fraud_prob_list.append(array[1])
            not_fraud_prob_list.append(array[0])

        data = {"personal_id": personal_id_list_str,
                "fraud_prob": fraud_prob_list,
                "not_fraud_prob": not_fraud_prob_list,
                "prob_res": prob_res_list
                }
        patient_info_df = pd.DataFrame(data)
        # print(patient_info_df)
        # patient_info_df.to_sql(name='patient_info',con=engine2,if_exists='replace',index=False)
        return patient_info_df
    except Exception as e:
        return "个人信息写入数据库失败"

    return "success"











