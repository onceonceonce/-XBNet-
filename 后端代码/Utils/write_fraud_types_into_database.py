import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import pairwise_distances
import joblib
import matplotlib

from db_connector.db_connector1.database import engine2
from Utils.new import X_tsne_

matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体
from pandas import DataFrame

async def write_fraud_types(df :DataFrame, df2:DataFrame):
    # print(df)
    # print(df2)
    # df1 是原数据  df2 是个人信息数据
    # data = pd.read_csv("./medical_records1.csv")
    try:
        columns = df.columns
        # 第一二列无用，删去
        x_data = df.to_numpy()[:, 2:-1]

        y = df.to_numpy()[:, -1]

        # 分类，yes为无欺诈类型，no为欺诈类型
        x_data_yes = x_data[y == 0]
        x_data_no = x_data[y == 1]

        # 标准化
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(x_data_no)

        # 读取训练过的文件，用来预测
        file_path_tsne = 'Utils/tsne2.pkl'
        file_path = 'Utils/dbscan_model2.pkl'

        # tsne非线性化
        tsne = joblib.load(file_path_tsne)
        X_tsne__ = tsne.fit_transform(X_scaled)

        # 用训练好的聚类结果去预测
        db = joblib.load(file_path)
        # labels = db.fit_predict(X_tsne__)
        labels_ = db.labels_

        # print(Counter(labels))


        # 用距离来判断数据集与核心点的位置，距离最近的归纳到同一标签
        distances = pairwise_distances(X_tsne__, X_tsne_[db.core_sample_indices_])

        # 找到最近的核心点
        nearest_core_index = np.argmin(distances, axis=1)
        # 将新数据点分配给最近的核心点所在的簇

        new_data_labels = labels_[db.core_sample_indices_][nearest_core_index]

        after_dbscan_yes = np.concatenate((df.to_numpy()[y == 0], 8 * np.ones((x_data_yes.shape[0], 1))), axis=1)
        after_dbscan_no = np.concatenate((df.to_numpy()[y == 1], new_data_labels.reshape(new_data_labels.shape[0], 1)), axis=1)

        map_ = {0: "虚假贫困户信息", 1: "倒卖药品", 2: "滥用医疗资源", 3: "虚假诊疗项目欺诈", 4: "联合欺诈", 5: "虚假就医",
                6: "滥用保险报销",
                7: "非法获取医疗补助", 8: "正常"}

        result = np.concatenate((after_dbscan_yes, after_dbscan_no), axis=0)

        # result[:, 0] = result[:, 0].astype(int)
        labels = result[:, -1]
        result = result[:, :-1]

        labels = [map_[label] for label in labels]
        # print(labels)
        result = pd.DataFrame(result, columns=columns)
        result["fraud_types"] = labels
        # 获得临时原数据表，加上最后一列欺诈类型
        # 排序

        result_up = result.sort_values(by='personal_id', axis=0)
        # result_up.to_csv("./result112.csv")

        df2_up = df2.sort_values(by='personal_id', axis=0)
        # df2_up.to_csv("./df2_up.csv")

        merged_df = df2_up.merge(result_up[['fraud_types', 'personal_id']], on='personal_id')

        # merged_df.to_csv("./merged_df.csv")
        # 使用merge方法将 df1 的某一列添加到 df2 中

        merged_df.to_sql(name='patient_info', con=engine2, if_exists='replace', index=False)

        # 得到完整的个人信息数据表
        return "个人数据写入成功"
    except Exception as e:
        print(e)
        return "欺诈类型写入数据库失败"
