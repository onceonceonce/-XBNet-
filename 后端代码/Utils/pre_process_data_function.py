import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from pandas import DataFrame

from scipy.spatial.distance import mahalanobis
from sklearn.covariance import EmpiricalCovariance
from sklearn.preprocessing import StandardScaler

async def fillna(fillMethod, df=None, val=0):
    # if df is None:
    #     df = medicareDataNew.copy()
    temp_df = df.copy()  # 创建df的副本

    if fillMethod == "solid":
        temp_df["discharge_diagnosis_length_max"] = temp_df["discharge_diagnosis_length_max"].fillna(val)
    elif fillMethod == "mean":
        temp_df["discharge_diagnosis_length_max"] = temp_df["discharge_diagnosis_length_max"].fillna(temp_df["discharge_diagnosis_length_max"].mean())
    elif fillMethod == "mode":
        temp_df["discharge_diagnosis_length_max"] = temp_df["discharge_diagnosis_length_max"].fillna(
            temp_df["discharge_diagnosis_length_max"].mode().iloc[0])  # mode() 返回一个 Series，需要取第一个值
    elif fillMethod == "forward_fill":
        temp_df["discharge_diagnosis_length_max"] = temp_df["discharge_diagnosis_length_max"].fillna(
            method='ffill')  # pad 是旧版pandas的用法，新版建议使用ffill
    elif fillMethod == "backward_fill":
        temp_df["discharge_diagnosis_length_max"] = temp_df["discharge_diagnosis_length_max"].fillna(method='bfill')
    elif fillMethod == "interpolate":
        temp_df["discharge_diagnosis_length_max"] = temp_df["discharge_diagnosis_length_max"].interpolate()
    else:
        raise ValueError("Invalid fill method specified")

    return temp_df
async def mashi_distance(df: DataFrame):

    # 假设 df 是你的 DataFrame，且只包含数值型特征
    numerical_df = df.select_dtypes(include=[np.number])

    # 首先对数据进行标准化，以便更好地计算协方差矩阵
    scaler = StandardScaler()
    scaled_df = scaler.fit_transform(numerical_df)

    # 计算均值向量和协方差矩阵
    cov_estimator = EmpiricalCovariance()
    cov_matrix = cov_estimator.fit(scaled_df).covariance_
    mean_vector = scaled_df.mean(axis=0)

    # 计算每个样本的马氏距离
    mahalanobis_distances = []

    for i in range(scaled_df.shape[0]):
        sample = scaled_df[i, :]  # 直接获取一维子数组
        mahalanobis_distance = mahalanobis(sample, mean_vector, cov_matrix)
        mahalanobis_distances.append(mahalanobis_distance)

    # 将计算出的马氏距离转换为 Series
    mahalanobis_distances = pd.Series(mahalanobis_distances, index=numerical_df.index)

    # 继续后面的代码，例如设定阈值和标记异常点
    threshold = np.percentile(mahalanobis_distances, 95)
    is_outlier = mahalanobis_distances > threshold

    # # 更新原始 DataFrame 中的一列来记录是否为异常点
    df['is_outlier'] = is_outlier
    final_df = df[df['is_outlier']==False]  #is_outlier表示是正常点
    return final_df


async def pre_process(df: DataFrame):
    """

    :param df:
    :return: 82列数据，最后两列是res，和is_outier
    """
    #填充空缺值
    fill_df = await fillna('mode',df)

    sm = SMOTE(random_state=666)
    #不把序号加入smote
    X_res,y_res = sm.fit_resample(fill_df.iloc[:,1:-1],fill_df.iloc[:,-1])
    #得到构造的数据
    concat_res = pd.concat([X_res,y_res],axis=1)
    #马氏距离去噪声
    final_df = await mashi_distance(concat_res)

    return final_df
