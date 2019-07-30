import datetime
import time

from dateutil.relativedelta import relativedelta

print(int(time.time()), str(int(time.time())))


def create_assist_date(datestart=None, dateend=None):
    # 创建日期辅助表
    if datestart is None:
        datestart = '2019-04-01'
    if dateend is None:
        print(datetime.datetime.now())
        dateend = datetime.datetime.now().strftime('%Y-%m-%d')
    # 转为日期格式
    datestart = datetime.datetime.strptime(datestart, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dateend, '%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        # 日期叠加一天
        print(datetime.timedelta(days=+1))
        datestart += datetime.timedelta(days=+1)
        # 日期转字符串存入列表
        date_list.append(datestart.strftime('%Y-%m-%d'))
    print(date_list)


# create_assist_date()

end_date = datetime.datetime.now()
start_date = end_date - relativedelta(years=1)
print(start_date)
start_date.strftime('%Y%m%d')
start_date = start_date.strftime('%Y%m%d')
print(start_date, type(start_date))
start_date = datetime.datetime.strptime(start_date, '%Y%m%d')
print(start_date)
