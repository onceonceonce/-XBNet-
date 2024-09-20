import torch
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from XBNet.models import XBNETClassifier
from XBNet.run import run_XBNET
import matplotlib.pyplot as plt

data = pd.read_csv(r"fill_df.csv", encoding_errors='replace')

important_columns_first = ['基本统筹基金支付金额_SUM','本次审批金额_SUM','药品费申报金额_SUM','药品费发生金额_SUM',
                     '月药品金额_MAX','月统筹金额_AVG','治疗费申报金额_SUM','ALL_SUM']

important_columns_second = ['统筹支付金额_SUM','月就诊次数_MAX','就诊次数_SUM','起付标准以上自负比例金额_SUM',
                            '可用账户报销金额_SUM','非账户支付金额_SUM','医院_统筹金_AVG',
                            '月就诊天数_MAX','月就诊天数_AVG','月统筹金额_MAX']
important_columns_third = ['医院_统筹金_MAX','贵重药品发生金额_SUM','医疗救助个人按比例负担金额_SUM',
                           '医疗救助医院申请_SUM','个人账户金额_SUM','一天去两家医院的天数']

important_columns_total = important_columns_first + important_columns_second + important_columns_third

data = data[important_columns_total + ['RES']]
print("数据规模: ", data.shape)
x_data = data[data.columns[:-1]]
print("训练数据: ", x_data.shape)
y_data = data[data.columns[-1]]
le = LabelEncoder()
y_data = np.array(le.fit_transform(y_data))
print("标签: ", le.classes_)

X_train, X_test, y_train, y_test = train_test_split(x_data.to_numpy(), y_data, test_size=0.2, random_state=0)

print(X_train.shape,X_test.shape, y_train.shape, y_test.shape)
print(type(X_train), type(X_test), type(y_train), type(y_test))

from imblearn.over_sampling import SMOTE
sm = SMOTE(random_state=666)
X_res, y_res = sm.fit_resample(X_train, y_train)

result_X = np.vstack((X_test[y_test==1][:45,], X_test[y_test==0][:,]))
result_y = np.concatenate((y_test[y_test==1][:45],y_test[y_test==0][:]))


model = XBNETClassifier(X_train, y_train, num_layers=2)
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# m, acc, lo, val_ac, val_lo = run_XBNET(X_train, X_test, y_train, y_test, model, criterion, optimizer, 128, 100)
m, acc, lo, val_ac, val_lo = run_XBNET(X_train, result_X, y_train, result_y, model, criterion, optimizer, 128, 10)


def find_max_element_and_index(lst):
    max_element = max(lst)
    max_index = lst.index(max_element)
    return max_element, max_index

train_max_element, train_max_index = find_max_element_and_index(acc)
test_max_element, test_max_index = find_max_element_and_index(val_ac)
print("(验证集)准确率{} ".format(test_max_element))
# print("(训练集)在第{}个epoch获得最高准确率{} ".format(train_max_index, train_max_element))
# print("(验证集)在第{}个epoch获得最高准确率{} ".format(test_max_index, test_max_element))
# print("(训练集)准确率{} ".format(train_max_element))
# print("(验证集)准确率{} ".format(test_max_element))
# fig, axs = plt.subplots(2, 2, figsize=(10, 6))
# axs[0, 0].plot(lo)
# axs[0, 0].set_title('lo')
# axs[0, 1].plot(acc)
# axs[0, 1].set_title('acc')
# axs[1, 0].plot(val_lo)
# axs[1, 0].set_title('val_lo')
# axs[1, 1].plot(val_ac)
# axs[1, 1].set_title('val_ac')
# fig.suptitle('XBNETClassifier')
# plt.tight_layout()
# plt.show()

# 输出预测结果
# print(predict(m, x_data.to_numpy()))

# acc: 训练集上的准确率
# lo: 训练集上的损失
# val_ac: 验证集上的准确率
# val_lo: 验证集上的损失