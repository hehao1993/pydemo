import os
from multiprocessing.pool import Pool
from urllib.parse import urlencode
from hashlib import md5
import requests


def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍',
        'autoload': 'true',
        'count': '20',
        'cur_tab': '1',
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None


def get_images(json):
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get('image_list')
            if title and images:
                for image in images:
                    yield {
                        'image': image.get('url'),
                        'title': title
                    }


def save_image(item):
    dir_path = '街拍/' + item.get('title')
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    try:
        response = requests.get('http:' + item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(dir_path, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to Save Image')


def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        save_image(item)


GROUP_START = 1
GROUP_END = 2

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()
