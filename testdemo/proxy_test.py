import requests

response = requests.get('http://www.baidu.com', proxies={
                'http': 'http://' + '183.166.160.78:8888',
                'https': 'https://' + '183.166.160.78:8888'
            }, timeout=20)
