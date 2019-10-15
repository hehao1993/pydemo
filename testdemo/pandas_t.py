import numpy as np
import pandas as pd

# 导入CSV或者xlsx文件
# =======================================================================================
df = pd.DataFrame(pd.read_csv('d.csv'))
df = pd.DataFrame(pd.read_excel('d.xlsx'))

# 用pandas创建数据表
# =======================================================================================
df = pd.DataFrame({"id": [1001, 1002, 1003, 1004, 1005, 1006],
                   "date": pd.date_range('20130102', periods=6),
                   "city": ['Beijing', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING  '],
                   "age": [23, 44, 54, 32, 34, 32],
                   "category": ['100-A', '100-B', '110-A', '110-C', '210-A', '130-F'],
                   "price": [1200, np.nan, 2133, 5433, np.nan, 4432]},
                  columns=['id', 'date', 'city', 'category', 'age', 'price'])
print('数据表df：\n', df)

# 数据表信息查看
# =======================================================================================
print('维度：', df.shape)
print('基本信息（维度、列名称、数据格式、所占空间等）：\n', df.info())
print('每一列数据的格式：\n', df.dtypes)
print('某一列数据的格式：', df['id'].dtype)
print('空值：\n', df.isnull())
print('某一列空值：\n', df['id'].isnull())
print('查看某一列的唯一值：\n', df['id'].unique())
print('查看数据表的值：\n', df.values)
print('查看列名称：', df.columns)
print('默认前5行数据：\n', df.head())
print('默认后5行数据：\n', df.tail())

# 数据表清洗（注意：需要对数据表或对应列重新赋值才能生效）
# =======================================================================================
print('用数字0填充空值：\n', df.fillna(value=0))
print('使用列prince的均值对NA进行填充：\n', df['price'].fillna(df['price'].mean()))
print('清除city字段的字符空格：\n', df['city'].map(str.strip))
print('大小写转换：\n', df['city'].str.lower())
df = df.fillna(value=0)
df['price'] = df['price'].astype('int64')
print('更改数据格式：\n', df['price'].astype('int64'))
print('更改列名称：\n', df.rename(columns={'date': 'birthday'}))
print('删除后出现的重复值：\n', df['price'].drop_duplicates())
print('删除先出现的重复值：\n', df['price'].drop_duplicates(keep='last'))
print('数据替换：\n', df['city'].replace('SH', 'shanghai'))

# 数据预处理（注意：需要对数据表或对应列重新赋值才能生效）
# =======================================================================================
df1 = pd.DataFrame({"id": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
                    "gender": ['male', 'female', 'male', 'female', 'male', 'female', 'male', 'female'],
                    "pay": ['Y', 'N', 'Y', 'Y', 'N', 'Y', 'N', 'Y', ],
                    "m-point": [10, 12, 20, 40, 40, 40, 30, 20]})
print('数据表df1：\n', df1)
print('匹配合并，交集：\n', pd.merge(df, df1, how='inner'))
print('匹配合并，按左：\n', pd.merge(df, df1, how='left'))
print('匹配合并，按右：\n', pd.merge(df, df1, how='right'))
print('匹配合并，并集：\n', pd.merge(df, df1, how='outer'))
print('按相同字段链接\n', df.join(df1, on='id', how='left', rsuffix='1'))
print('在末尾附加\n', df.append(df1, sort=False))
print('连接\n', pd.concat([df, df1], sort=False).reset_index())
print('设置索引列：\n', df.set_index('id'))
print('按照特定列的值排序：\n', df.sort_values(by=['age']))
print('按照索引列排序：\n', df.sort_index())
df['group'] = np.where(df['price'] > 3000, 'high', 'low')
print('如果price列的值>3000，group列显示high，否则显示low：\n', df['group'])
df.loc[(df['city'] == 'Shenzhen') & (df['price'] >= 3000), 'sign'] = 1
print('对复合多个条件的数据进行分组标记：\n', df['sign'])
df2 = pd.DataFrame((x.split('-') for x in df['category']), index=df.index, columns=['size', 'category'])
print('对category字段的值依次进行分列，并创建数据表，索引值为df的索引列，列名称为category和size\n', df2)
print('匹配合并，按索引：\n', pd.merge(df, df2, left_index=True, right_index=True))

# 数据提取
# =======================================================================================
print('按索引提取单行的数值\n', df.loc[3])  # 索引的标签为3
print('按索引提取区域行数值\n', df.iloc[0: 5])  # 前5行
print('重设索引\n', df.reset_index())
df = df.set_index('date')
print('设置日期为索引\n', df)
print('提取4日之前的所有数据\n', df[:'2013-01-04'])
print('使用iloc按位置区域提取数据\n', df.iloc[:3, :2])  # #冒号前后的数字不再是索引的标签名称，而是数据所在的位置，从0开始，前三行，前两列。
print('使用iloc按位置单独提取数据\n', df.iloc[[0, 2, 5], [4, 5]])  # 提取第0、2、5行，4、5列
print('使用ix按索引标签和位置混合提取数据\n', df.ix[:'2013-01-03', :4])  # 2013-01-03号之前，前四列数据
print('判断city列的值是否为北京\n', df['city'].isin(['Shenzhen']))
print('判断city列里是否包含beijing和shanghai，然后将符合条件的数据提取出来\n', df.loc[df['city'].isin(['Beijing', 'shanghai'])])
print('提取前三个字符，并生成数据表\n', pd.DataFrame(df['category'].str[:3]))

# 数据筛选
# =======================================================================================
print('使用“与”进行筛选\n', df.loc[(df['age'] > 20) & (df['city'] == 'Beijing'), ['id', 'city', 'age', 'category', 'price']])
print('使用“或”进行筛选\n', df.loc[(df['age'] > 40) | (df['city'] == 'Beijing'), ['id', 'city', 'age', 'category', 'price']].sort_values(['age']))
print('使用“非”条件进行筛选\n', df.loc[(df['city'] != 'Beijing'), ['id', 'city', 'age', 'category', 'price']].sort_values(['age']))
print('对筛选后的数据按city列进行计数\n', df.loc[(df['city'] != 'Beijing'), ['id', 'city', 'age', 'category', 'price']].sort_values(['age']).city.count())
print('使用query函数进行筛选\n', df.query('city == ["Beijing", "shanghai"]'))
print('对筛选后的结果按prince进行求和\n', df.query('city == ["Beijing", "shanghai"]').price.sum())

# 数据汇总
# =======================================================================================
df = df.reset_index()
print('按group对所有的列进行计数汇总\n', df.groupby('group').count())
print('按group对id字段进行计数\n',  df.groupby('group').id.count())
print('对两个字段进行汇总计数\n', df.groupby(['group', 'age']).count())
print('对group字段进行汇总，并分别计算prince的合计和均值\n', df.groupby('group').price.agg([len, np.sum, np.mean]))


# 数据统计
# =======================================================================================
print('简单的数据采样\n', df.sample(n=3))
print('手动设置采样权重\n', df.sample(n=2, weights=[0, 0, 0, 0, 0.5, 0.5]))
print('采样后不放回\n', df.sample(n=6, replace=False))
print('采样后放回\n', df.sample(n=6, replace=True))
print('数据表描述性统计\n', df.describe().round(2).T)  # round函数设置显示小数位，T表示转置
print('计算列的标准差\n', df['price'].std())
print('计算两个字段间的协方差\n', df['price'].cov(df['age']))
print('数据表中所有字段间的协方差\n', df.cov())
print('两个字段的相关性分析\n', df['price'].corr(df['age']))  # 相关系数在-1到1之间，接近1为正相关，接近-1为负相关，0为不相关
print('数据表的相关性分析\n', df.corr())

# 数据输出
# =======================================================================================
print('写入Excel\n', df.to_excel('df_to_excel.xlsx', sheet_name='bluewhale_cc'))
print('写入到CSV\n', df.to_csv('df_to_csv.csv'))

df_gp = df.groupby('group')
for i, j in df_gp:
    print('分组', i, '\n', j)
