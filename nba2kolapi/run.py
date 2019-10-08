import json
import requests
from aiohttp import web
import urllib3
urllib3.disable_warnings()

routes = web.RouteTableDef()


@routes.get('/rosterList')
async def hello(request):
    query = dict(request.query)
    # print(query)
    # print(request.query_string)
    paras = {
        'page': query['page'],
        'lowPrice': query['lowPrice'],
        'highPrice': query['highPrice'],
        'collapseAll': query['collapseAll'],
        'orderBy': query['orderBy'],
        'orientation': query['orientation']
    }
    url = "https://nba2k2app.game.qq.com/game/trade/rosterList"
    json_result = requests.get(url, params=paras, verify=False).json()
    return web.json_response(json_result)

app = web.Application()
app.add_routes(routes)
web.run_app(app)
