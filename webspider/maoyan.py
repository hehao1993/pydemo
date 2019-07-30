import csv
import json
import re
import pymongo
import pymysql
import requests
import time
from pyquery import PyQuery
from redis import StrictRedis
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/67.0.3396.79 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    # 一、正则解析
    # pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a'
    #                      '.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>'
    #                      '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    # items = re.findall(pattern, html)
    # for item in items:
    #     yield {
    #         'index': item[0],
    #         'image': item[1],
    #         'title': item[2],
    #         'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
    #         'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
    #         'score': item[5].strip() + item[6].strip()
    #     }

    # 二、PyQuery解析
    doc = PyQuery(html)
    for item in doc.find("dd").items():
        yield {
            'rank': item.find("i.board-index").text(),
            'cover': item.find("img.board-img").attr("data-src"),
            'title': item.find("p.name").text(),
            'actor': item.find("p.star").text()[3:],
            'release_time': item.find("p.releasetime").text()[5:],
            'score': item.find("p.score i.integer").text() + item.find("p.score i.fraction").text()
        }


def write_to_file(data):
    # 一、
    # with open('result.txt', 'a', encoding='utf-8') as f:
    #     f.write(json.dumps(data, ensure_ascii=False, indent=4) + '\n')

    # 二、
    # json.dump(data, open('result.txt', 'a', encoding='utf-8'), ensure_ascii=False)

    # 三、
    # with open('result.csv', 'a', encoding='utf-8') as f:
    #     fieldnames = ['排行', '封面', '名字', '主演', '时间（地区）', '评分']
    #     writer = csv.DictWriter(f, fieldnames=fieldnames)
    #     writer.writeheader()
    #     writer.writerow(data)

    # 四、
    # table = 'movie'
    # keys = ', '.join(data.keys())
    # values = ', '.join(['%s'] * len(data))
    # sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
    # sql += ','.join([" {key} = %s".format(key=key) for key in data])
    # try:
    #     if cursor.execute(sql, tuple(data.values()) * 2):
    #         mysql_db.commit()
    # except:
    #     mysql_db.rollback()

    # 五、
    # collection = mongodb.movie
    # collection.insert_one(data)

    # 六、
    redis = StrictRedis(host='localhost', port=6379, db=0, password='123456')
    redis.hmset(data['rank'], data)


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_to_file(item)


if __name__ == '__main__':
    # mysql
    mysql_db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='webspider')
    cursor = mysql_db.cursor()
    # mongodb
    client = pymongo.MongoClient(host='localhost', port=27017)
    mongodb = client.spider
    print("请稍等，正在写入...")
    for i in range(10):
        main(i * 10)
        time.sleep(1)
    mysql_db.close()
    print("写入完成！")
