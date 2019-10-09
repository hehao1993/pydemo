import joblib
import pandas as pd
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn import linear_model
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor


data = pd.read_csv('yanzhi.csv')
data.isnull().any().sum()
# scatter_matrix(data, alpha=0.7, diagonal='kde')
corr = data.corr()

# 特征选择:使用与目标变量的相关性强的变量作为最终的特征变量
x = data[['comment', 'like', 'share', 'follower']]
y = data[['play']]
SelectKBest = SelectKBest(f_regression, k=3)  # k=4或者k='all'
bestFeature = SelectKBest.fit_transform(x, y.values.ravel())
print(x.columns[SelectKBest.get_support()])
features = data[x.columns[SelectKBest.get_support()]]
# scatter_matrix(features, alpha=0.7, diagonal='hist')
# plt.show()

# 特征归一化
scaler = StandardScaler().fit(features)
joblib.dump(scaler, 'scaler')
features = scaler.transform(features)

# 散点可视化，查看特征归一化后的数据
font = {
    'family': 'SimHei'
}
# matplotlib.rc('font', **font)
# scatter_matrix(features, alpha=0.7, diagonal='hist')

# 数据集拆分
x_train, x_test, y_train, y_test = train_test_split(features, y, test_size=0.3, random_state=33)

# 模型选择
y_train = y_train.values.ravel()

# 线性回归
lr = linear_model.LinearRegression()
lr_predict = cross_val_predict(lr, x_train, y_train, cv=5)
lr_score = cross_val_score(lr, x_train, y_train, cv=5)
lr_meanscore = lr_score.mean()

# SVR模型预测房价：尝试三种核，'linear', 'poly', 'rbf'
# 更改惩罚系数C来查看对模型的影响
# lSVR_score = []
# for i in [1, 10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10]:
#     linear_svr = SVR(kernel='linear', C=i)
#     linear_svr_predict = cross_val_predict(linear_svr, x_train, y_train, cv=5)
#     linear_svr_score = cross_val_score(linear_svr, x_train, y_train, cv=5)
#     linear_svr_meanscore = linear_svr_score.mean()
#     lSVR_score.append(linear_svr_meanscore)
# plt.plot(lSVR_score)
# plt.show()

linear_svr = SVR(kernel='linear', C=1e9)
linear_svr_predict = cross_val_predict(linear_svr, x_train, y_train, cv=5)
linear_svr_score = cross_val_score(linear_svr, x_train, y_train, cv=5)
linear_svr_meanscore = linear_svr_score.mean()

# 尝试修改惩罚系数C和degree
# for i in [1, 10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8]:
#     polySVR_score = []
#     for j in np.linspace(1, 10, 10):
#         poly_svr = SVR(kernel='poly', C=i, degree=j)
#         poly_svr_predict = cross_val_predict(poly_svr, x_train, y_train, cv=5)
#         poly_svr_score = cross_val_score(poly_svr, x_train, y_train, cv=5)
#         poly_svr_meanscore = poly_svr_score.mean()
#         polySVR_score.append(poly_svr_meanscore)
#     plt.plot(np.linspace(1, 10, 10), polySVR_score, label='C=' + str(i))
#     plt.legend()
# plt.xlabel('degree')
# plt.ylabel('score')
# plt.show()

poly_svr = SVR(kernel='poly', C=1e6, degree=2)
poly_svr_predict = cross_val_predict(poly_svr, x_train, y_train, cv=5)
poly_svr_score = cross_val_score(poly_svr, x_train, y_train, cv=5)
poly_svr_meanscore = poly_svr_score.mean()

# 优化惩罚系数C和gamma
# for i in [1e8, 1e9, 1e10, 1e11]:
#     rbfSVR_score = []
#     for j in np.linspace(0.0001, 0.002, 20):
#         rbf_svr = SVR(kernel='rbf', C=i, gamma=j)
#         rbf_svr_predict = cross_val_predict(rbf_svr, x_train, y_train, cv=5)
#         rbf_svr_score = cross_val_score(rbf_svr, x_train, y_train, cv=5)
#         rbf_svr_meanscore = rbf_svr_score.mean()
#         rbfSVR_score.append(rbf_svr_meanscore)
#     plt.plot(np.linspace(0.0001, 0.002, 20), rbfSVR_score, label='C='+str(i))
#     plt.legend()
# plt.xlabel('gamma')
# plt.ylabel('score')
# plt.show()

rbf_svr = SVR(kernel='rbf', C=1e10, gamma=0.001)
rbf_svr_predict = cross_val_predict(rbf_svr, x_train, y_train, cv=5)
rbf_svr_score = cross_val_score(rbf_svr, x_train, y_train, cv=5)
rbf_svr_meanscore = rbf_svr_score.mean()

# KNN模型
# 在KNN的回归模型当中，我们没法确定n_neighbors，因此需要最优化这个参数。
# 分别计算n_neighbors=[1,2,...,10,11]
# score = []
# for n_neighbors in range(1, 20):
#     knn = KNeighborsRegressor(n_neighbors, weights='uniform')
#     knn_predict = cross_val_predict(knn, x_train, y_train, cv=5)
#     knn_score = cross_val_score(knn, x_train, y_train, cv=5)
#     knn_meanscore = knn_score.mean()
#     score.append(knn_meanscore)
# plt.plot(score)
# plt.xlabel('n-neighbors')
# plt.ylabel('mean-score')
# plt.show()

n_neighbors = 4
knn = KNeighborsRegressor(n_neighbors, weights='uniform')
knn_predict = cross_val_predict(knn, x_train, y_train, cv=5)
knn_score = cross_val_score(knn, x_train, y_train, cv=5)
knn_meanscore = knn_score.mean()

# 决策树
# 和KNN类似，这里没法确定决策树的深度，因此令最大深度分别是1至10。
# score = []
# for n in range(1, 11):
#     dtr = DecisionTreeRegressor(max_depth = n)
#     dtr_predict = cross_val_predict(dtr, x_train, y_train, cv=5)
#     dtr_score = cross_val_score(dtr, x_train, y_train, cv=5)
#     dtr_meanscore = dtr_score.mean()
#     score.append(dtr_meanscore)
# plt.plot(np.linspace(1, 10, 10), score)
# plt.xlabel('max_depth')
# plt.ylabel('mean-score')
# plt.show()

n = 4
dtr = DecisionTreeRegressor(max_depth=n)
dtr_predict = cross_val_predict(dtr, x_train, y_train, cv=5)
dtr_score = cross_val_score(dtr, x_train, y_train, cv=5)
dtr_meanscore = dtr_score.mean()

# 汇总下评分
evaluating = {
        'lr': lr_score,
        'linear_svr': linear_svr_score,
        'poly_svr': poly_svr_score,
        'rbf_svr': rbf_svr_score,
        'knn': knn_score,
        'dtr': dtr_score
        }
evaluating = pd.DataFrame(evaluating)
# evaluating.plot.kde(alpha=0.6, figsize=(8, 7))
# evaluating.hist(color='k', alpha=0.6, figsize=(8, 7))

# 最优模型确定
print("模型评分")
print("============================================")
print(evaluating.mean().sort_values(ascending=False))

# 模型预测
rbf_svr.fit(x_train, y_train)
# 保存模型
joblib.dump(rbf_svr, 'rbf_svr.pkl')
rbf_svr_y_predict = rbf_svr.predict(x_test)
rbf_svr_y_predict_score = rbf_svr.score(x_test, y_test)
# KNN
knn.fit(x_train, y_train)
# 保存模型
joblib.dump(knn, 'knn.pkl')
knn_y_predict = knn.predict(x_test)
knn_y_predict_score = knn.score(x_test, y_test)
# poly_svr
poly_svr.fit(x_train, y_train)
# 保存模型
joblib.dump(poly_svr, 'poly_svr.pkl')
poly_svr_y_predict = poly_svr.predict(x_test)
poly_svr_y_predict_score = poly_svr.score(x_test, y_test)
# dtr
dtr.fit(x_train, y_train)
# 保存模型
joblib.dump(dtr, 'dtr.pkl')
dtr_y_predict = dtr.predict(x_test)
dtr_y_predict_score = dtr.score(x_test, y_test)
# lr
lr.fit(x_train, y_train)
# 保存模型
joblib.dump(lr, 'lr.pkl')
lr_y_predict = lr.predict(x_test)
lr_y_predict_score = lr.score(x_test, y_test)
# linear_svr
linear_svr.fit(x_train, y_train)
# 保存模型
joblib.dump(linear_svr, 'linear_svr.pkl')
linear_svr_y_predict = linear_svr.predict(x_test)
linear_svr_y_predict_score = linear_svr.score(x_test, y_test)
predict_score = {
    'lr': lr_y_predict_score,
    'linear_svr': linear_svr_y_predict_score,
    'poly_svr': poly_svr_y_predict_score,
    'rbf_svr': rbf_svr_y_predict_score,
    'knn': knn_y_predict_score,
    'dtr': dtr_y_predict_score
}
predict_score = pd.DataFrame(predict_score, index=['score']).transpose()
# 预测结果排名
print("模型预测评分")
print("============================================")
print(predict_score.sort_values(by='score', ascending=False))

# 对各个模型的预测值整理
plt.scatter(np.linspace(0, len(y_test) - 1, len(y_test)), y_test, label='predict data')
labelname = [
        'rbf_svr_y_predict',
        'knn_y_predict',
        'poly_svr_y_predict',
        'dtr_y_predict',
        'lr_y_predict',
        'linear_svr_y_predict']
y_predict = {
        'rbf_svr_y_predict': rbf_svr_y_predict,
        'knn_y_predict': knn_y_predict,
        'poly_svr_y_predict': poly_svr_y_predict,
        'dtr_y_predict': dtr_y_predict,
        'lr_y_predict': lr_y_predict,
        'linear_svr_y_predict': linear_svr_y_predict
        }
y_predict = pd.DataFrame(y_predict)
for name in labelname:
    plt.plot(y_predict[name], label=name)
plt.xlabel('predict data index')
plt.ylabel('target')
plt.legend()

# 渲染图表
# plt.show()
