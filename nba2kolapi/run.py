import requests
from aiohttp import web

routes = web.RouteTableDef()


@routes.get('/rosterList')
async def hello(request):
    print(request.query.get('page'))
    # url = "https://nba2k2app.game.qq.com/game/trade/rosterList"
    # json = requests.get(url, params=paras, verify=False).json()
    # print(json.dumps(json, indent=4, ensure_ascii=False))
    return web.json_response({'a': 1})

app = web.Application()
app.add_routes(routes)
web.run_app(app)
