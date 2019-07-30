import requests

proxy = '127.0.0.1:9743'
# SOCKS5代理（需要额外安装模块 pip3 install 'requests[socks]'）
proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy,
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
