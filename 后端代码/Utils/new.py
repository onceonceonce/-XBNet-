import pandas as pd
from Utils.Dataset import selected_rows, columns
import joblib
import os
columns = columns[1:]

x_data = selected_rows[:, :-1]  # 未经过归一化的
y_data = selected_rows[:, -1]
x_data_pandas = pd.DataFrame(x_data, columns=columns)
pd.set_option('display.max_columns', None)
from imblearn.over_sampling import SMOTE
from collections import Counter
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# 计算一列的平均值
def calculate_mean(df, column_name):
    # if not all(item in set(df.columns.tolist()) for item in column_name):
    #     raise ValueError("Error: Column name not found in the DataFrame."
    selected_row = df.loc[:, column_name]
    mean_value = selected_row.mean()

    return mean_value


# 归一化，以防画图不明显
def normalize_columns(matrix):
    # 计算每列的最大值和最小值
    min_vals = np.min(matrix, axis=0)
    max_vals = np.max(matrix, axis=0)

    # 处理分母为零的情况
    divisor = max_vals - min_vals
    divisor[divisor==0] = 1e-10  # 将分母为零的位置替换为一个小的非零值

    # 列归一化
    normalized_matrix = (matrix - min_vals) / divisor

    return normalized_matrix


def count_hospitals_by_label(data):
    label_dict = {}

    for row in data:
        hospital_number = row[0]
        label = row[1]

        if label not in label_dict:
            label_dict[label] = {}

        if hospital_number not in label_dict[label]:
            label_dict[label][hospital_number] = 1
        else:
            label_dict[label][hospital_number] += 1

    return label_dict


def print_hospital_count(label_dict):
    for label, hospitals in label_dict.items():
        print(f"标签 {label}:")
        for hospital_number, count in hospitals.items():
            print(f"  医院标号 {hospital_number}: {count} 个")
        print()



# n_clusters是预估的簇的数量范围
feature_quantity = 15     # 特征重要程度的前多少

# 数据预处理
scaler = StandardScaler()
X_scaled = scaler.fit_transform(x_data)

# 使用TSNE降维
file_path_tsne = 'tsne.pkl'

if not os.path.exists(file_path_tsne):
    tsne = TSNE(n_components=2, random_state=42)

    joblib.dump(tsne, file_path_tsne)
else:
    tsne = joblib.load(file_path_tsne)

X_tsne_ = tsne.fit_transform(X_scaled)
# 使用HDBSCAN算法进行聚类
# from sklearn.cluster import DBSCAN
# import hdbscan

if __name__ == '__main__':
    file_path = 'dbscan_model1.pkl'

    if not os.path.exists(file_path):
        # 聚类
        db = DBSCAN(eps=4, min_samples=25)
        db.fit(X_tsne_)
        # clusterer = hdbscan.HDBSCAN(min_cluster_size=35)
        # clusterer.fit(X_pca)
        # joblib.dump(clusterer, file_path)
        joblib.dump(db, file_path)
    else:
        # clusterer = joblib.load(file_path)
        db = joblib.load(file_path)

    # 获取每个样本的簇标签，聚类的结果
    labels = db.labels_
    labels_ = db.fit_predict(X_tsne_)
    # labels = clusterer.labels_
    print(Counter(labels))
    print("11:", Counter(labels_))
    # 绘制聚类结果
    plt.figure(figsize=(8, 6))

    # X_pca = X_pca[labels != -1]
    # labels = labels[labels != -1]

    plt.colorbar(plt.scatter(X_tsne_[:, 0], X_tsne_[:, 1],  c=labels), ticks=np.arange(len(labels)+1))
    plt.title("原始数据降维聚类展示")
    plt.show()

    X_scaled = X_scaled[labels != -1]
    x_data = x_data[labels != -1]
    labels = labels
    hosiptal_number = x_data_pandas["医院编码_NN"].astype(int).to_numpy()
    h_n_label = np.concatenate((hosiptal_number.reshape(793, 1), labels.reshape(793, 1)), axis=1)
    h_n_label = h_n_label[labels != -1]
    h_tongji = np.zeros((max(labels)+1, max(hosiptal_number)))
    result = count_hospitals_by_label(h_n_label)
    print_hospital_count(result)
    y = labels[labels != -1]
    smote = SMOTE(random_state=42)
    x_data_smote, y = smote.fit_resample(x_data, y)
    X_new = scaler.fit_transform(x_data_smote)

    tsne = TSNE(n_components=2)
    X_tsne = tsne.fit_transform(X_new)

    X_ = []
    X_after_tsne = []
    X_before = []
    for i in range(max(labels)+1):
        X_.append(X_new[y == i])
        X_after_tsne.append(X_tsne[y == i])
        X_data_pandas = pd.DataFrame(data=x_data_smote[y == i], columns=columns)
        X_before.append(X_data_pandas)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X_new, y, test_size=0.3, random_state=42)
    print(Counter(y))

    plt.figure(figsize=(8, 6))
    plt.colorbar(plt.scatter(X_after_tsne[1][:, 0], X_after_tsne[1][:, 1]), ticks=np.arange(len(labels)+1))
    plt.title("经过smote后降维数据可视化")
    plt.show()

# --------------------------------------------------------------------------------
    # 初始化随机森林分类器(本来是想用随机森林再预测的，但是结果不太好，后面的图也是画随机森林给出的前15个特征)
    if os.path.exists("random_forest_model1.pkl"):
        rf_clf = joblib.load('random_forest_model1.pkl')

    else:
        rf_clf = RandomForestClassifier(n_estimators=int(5e4), random_state=42)

        rf_clf.fit(X_train, y_train)
        joblib.dump(rf_clf, 'random_forest_model1.pkl')

    feature_importance = rf_clf.feature_importances_

    # 获取前十个最重要的特征的索引
    top_ten_indices = np.argsort(feature_importance)[::-1][:feature_quantity]
    print(columns[top_ten_indices])

    # 在测试集上做预测
    y_pred = rf_clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    print("Accuracy: {:.2f}%".format(accuracy * 100))

# -------------------------------------------------------------------------------------

    # 创建示例数据：7个组，每个组5个特征值
    data = np.zeros((max(labels)+1, feature_quantity))
    data_total = np.zeros((max(labels)+1, 80))
    # data_total_hospital = np.zeros((max(labels)+1, 80))

    print("共有", data.shape[0], "组")
    print("共有", data.shape[1], "特征")

    for i in range(max(labels)+1):
        data[i, :] = calculate_mean(X_before[i], columns[top_ten_indices].tolist())
        data_total[i, :] = calculate_mean(X_before[i], columns)
    # data_ = pd.DataFrame(data, columns=columns[top_ten_indices])
    data_ = pd.DataFrame(data_total, columns=columns)

    data_hospital_pandas = pd.DataFrame(data_total, columns=columns)
    # for _, i in enumerate(data_hospital_pandas.columns):
    #     if i == '医院编码_NN':
    #         data_total_hospital[_, :] = int(data_hospital_pandas[i])
    #         for j in data_hospital_pandas[i]:
    #             if data_hospital_pandas[i][j] > 9:
    #                 data_hospital_pandas[i][j] = 9
    #             elif data_hospital_pandas[i][j] < 1:
    #                 data_hospital_pandas[i][j] = 1
    #     else:
    #         print(i)
    #         data_total_hospital[_, :] = calculate_mean(data_hospital_pandas, i)

    # print(data_total_hospital)
    data = normalize_columns(data)
    print(data_)

    # 设置组名和特征名
    groups = [f"Group{i + 1}" for i in range(max(labels) + 1)]

    features = columns[top_ten_indices].tolist()

    # 画图， 创建一个包含1x3的子图布局
    fig, axs = plt.subplots(3, 1, figsize=(18, 8))

    bar_width = 0.12
    index = np.arange(len(groups))
    print(index)
    # 每个子图绘制不同范围的特征
    for i in range(3):
        start_feature = i * 5
        end_feature = start_feature + 5

        for j in range(start_feature, end_feature):
            axs[i].bar(index + (j % 5) * bar_width, data[:, j], bar_width, label=features[j])

        axs[i].set_xlabel('Groups')
        axs[i].set_ylabel('Values')
        axs[i].set_title(f'Bar Chart of Groups with Features {start_feature + 1} to {end_feature}')
        axs[i].set_xticks(index + 2 * bar_width)
        axs[i].set_xticklabels(groups)
        axs[i].legend()

    # 设置整体图的标题
    plt.suptitle('Comparison of Different Feature Sets')

    # 调整布局
    plt.tight_layout()

    # 显示图形
    plt.show()
