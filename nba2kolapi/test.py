import json
import requests
import urllib3

urllib3.disable_warnings()


paras = {
    'page': 1,
    'lowPrice': 0,
    'highPrice': 0,
    'collapseAll': False,
    'openid': '112D1F37C43B195B0B95611CDC3DE5AE',
    'access_token': 'A5F3F343C8646667B9A9B2CC383163C1',
    'orderBy': 'OverAll',
    'orientation': 'desc'
}
url = "https://nba2k2app.game.qq.com/game/trade/rosterList"
r = requests.get(url, params=paras, verify=False)
print(r.json())
print(len(r.json()['data']['rosterList']))
print(json.dumps(r.json(), indent=4, ensure_ascii=False))

url = "https://nba2k2app.game.qq.com/rosterDetail?ids=4101&level=20&grade=7&mode=1"
# r = requests.get(url, params=paras, verify=False)
# print(json.dumps(r.json(), indent=4, ensure_ascii=False))
