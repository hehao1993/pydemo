import os
import time
import joblib
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
from sklearn import linear_model


def train(data):
    start = time.time()
    # 数据表的相关性：相关系数在-1到1之间，接近1为正相关，接近-1为负相关，0为不相关
    # print(data.corr())

    # 特征选择:使用与目标变量的相关性强的变量作为最终的特征变量
    x = data[['comment', 'like', 'share']]
    y = data['play']
    selectKBest = SelectKBest(f_regression, k=3)  # k=4或者k='all'
    bestFeature = selectKBest.fit_transform(x, y.values.ravel())
    features = data[x.columns[selectKBest.get_support()]]

    # 特征归一化
    scaler = StandardScaler().fit(features)
    # 持久化保存归一化，用于预测
    joblib.dump(scaler, 'scaler')
    features = scaler.transform(features)

    # 数据集拆分
    x_train, x_test, y_train, y_test = train_test_split(features, y, test_size=0.3, random_state=33)
    y_train = y_train.values.ravel()

    # 线性回归模型
    lr = linear_model.LinearRegression()
    lr_predict = cross_val_predict(lr, x_train, y_train, cv=5)
    lr_score = cross_val_score(lr, x_train, y_train, cv=5)
    lr_means_core = lr_score.mean()

    # 模型预测
    lr.fit(x_train, y_train)
    # 保存模型，用于预测
    joblib.dump(lr, 'lr.pkl')
    lr_y_predict = lr.predict(x_test)
    lr_y_predict_score = lr.score(x_test, y_test)

    end = time.time()
    print(f'模型评分：{lr_means_core}，模型预测评分：{lr_y_predict_score}，总耗时：{end - start}秒')


def predict(data):
    x = data[['comment', 'like', 'share']]

    # 加载特征归一化
    scaler = joblib.load('scaler')
    x = scaler.transform(x)

    # 加载模型
    lr = joblib.load('lr.pkl')

    y_predict = {
        'real_val': np.array(data['play']),
        'predict_val': lr.predict(x),
    }
    y_predict = pd.DataFrame(y_predict).applymap(lambda n: int(n))
    print(y_predict)


if __name__ == '__main__':
    fileList = os.listdir('data')
    merge_data = pd.DataFrame()
    for file in fileList:
        print(f'【{file}】')
        train_data = pd.DataFrame(pd.read_excel(f'data/{file}'))
        train(train_data)
        merge_data = merge_data.append(train_data, sort=False, ignore_index=True)
    print('【不分类合并】')
    train(merge_data)

    predict_data = pd.read_excel('data/二次元.xlsx')
    # predict_data = pd.DataFrame([[1597, 32487, 40, 332204]], columns=['comment', 'like', 'share', 'play'])
    predict(predict_data)
