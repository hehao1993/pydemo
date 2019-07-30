import itchat
import requests
from itchat.content import *


def get_response(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api' # http://openapi.tuling123.com/openapi/api/v2
    data = {
        'key': '2d84e38c318e451897ac2b79af6f9e09',
        'info': msg,
        'userid': '浩浩',
    }
    # 我们通过如下命令发送一个 post 请求
    r = requests.post(apiUrl, data=data).json()
    return r.get('text')


@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    users = itchat.search_friends("杜婷婷")
    print(users)
    userName = users[0]['UserName']
    if msg.get('FromUserName') == userName:
        return get_response(msg['Text'])
    else:
        return None


if __name__ == '__main__':
    itchat.auto_login(True)
    itchat.run()
