import requests
import socks
import socket

# SOCKS5代理，此方法是全局设置（需要额外安装模块 pip3 install 'requests[socks]'）
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 9742)
socket.socket = socks.socksocket
try:
    response = requests.get('http://httpbin.org/get')
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)