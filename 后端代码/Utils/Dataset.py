import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

from collections import Counter
from sklearn.utils import shuffle

from sklearn.preprocessing import LabelEncoder

from sklearn.model_selection import train_test_split

from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体为黑体

data1 = pd.read_csv(r"Utils/medical_records1.csv", encoding='GB2312', encoding_errors='replace')
data = pd.read_csv(r"Utils/medical_records1.csv", encoding='GB2312', encoding_errors='replace')
print("数据规模: ", data.shape)
x_data = data[data.columns[:-1]]
columns = data.columns[:-1]
print("训练数据: ", x_data.shape)
y_data = data[data.columns[-1]]
print("before:", Counter(y_data))
le = LabelEncoder()
# smote = SMOTE(random_state=123)
# x_data, y_data = smote.fit_resample(x_data, y_data)
# StandardScaler().fit_transform(x_data)
y_data = np.array(le.fit_transform(y_data))

print("after:", Counter(y_data))
print("标签: ", le.classes_)

# 打乱
x_data, y_data = shuffle(x_data, y_data, random_state=42)
StandardScaler().fit_transform(x_data)
print("x_data.shape:", x_data.shape)
y_data = y_data.reshape(y_data.shape[0], -1)
x_data_pandas = x_data.copy()
combined_matrix = np.concatenate((x_data.to_numpy()[:, 1:], y_data), axis=1)
print(combined_matrix.shape)
# 挑选出最后一列数值为1的行形成新矩阵
selected_rows = combined_matrix[combined_matrix[:, -1] == 1]
if __name__ == '__main__':
    # 分训练验证集
    X_train, X_test, y_train, y_test = train_test_split(x_data.to_numpy(), y_data, test_size=0.25, random_state=0)
    # y_train = to_categorical(y_train)

    # 可视化
    X_embedded = TSNE(n_components=2).fit_transform(x_data.to_numpy()[:, :])

    # dbscan = DBSCAN(eps=0.14, min_samples=5)
    # clusters = dbscan.fit_predict(X_embedded)
    # print(Counter(clusters))
    # 可视化聚类结果
    # plt.figure(figsize=(8, 6))
    # plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=clusters, cmap='viridis', s=50, alpha=0.5)
    # plt.title('t-SNE + DBSCAN Clustering')
    # plt.colorbar(label='Cluster')
    # plt.show()
    #
    plt.scatter(X_embedded[:, 0], X_embedded[:, 1], c=y_data[:])
    plt.colorbar()
    plt.title("原始数据")
    plt.show()
