import joblib
import pandas as pd
import numpy as np
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


base_data = pd.read_csv('data.csv')
data = base_data[['comment', 'like', 'share']]


# 1597,32487,40,2352671,332204
# 2657,63429,195,2352671,768174
# data = [[1597, 32487, 40], [2657, 63429, 195]]

# 加载特征归一化
scaler = joblib.load('scaler')
data = scaler.transform(data)

# 加载模型
rbf_svr = joblib.load('rbf_svr.pkl')
knn = joblib.load('knn.pkl')
linear_svr = joblib.load('linear_svr.pkl')
poly_svr = joblib.load('poly_svr.pkl')
lr = joblib.load('lr.pkl')
dtr = joblib.load('dtr.pkl')

print(type(base_data['play']))
y_predict = {
    'real_val': np.array(base_data['play']),
    'rbf_svr': rbf_svr.predict(data),
    'knn': knn.predict(data),
    'poly_svr': poly_svr.predict(data),
    'dtr': dtr.predict(data),
    'lr': lr.predict(data),
    'linear_svr': linear_svr.predict(data)
}
y_predict = pd.DataFrame(y_predict).applymap(lambda x: int(x))
print(y_predict)

"""
模型评分
============================================
linear_svr    0.816617
rbf_svr       0.795186
lr            0.786579
dtr           0.721681
knn           0.705617
poly_svr      0.546776
dtype: float64
模型预测评分
============================================
               score
linear_svr  0.898740
lr          0.887091
rbf_svr     0.872514
knn         0.800739
dtr         0.773861
poly_svr    0.726463
"""
