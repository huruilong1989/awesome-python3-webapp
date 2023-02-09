import asyncio


import logging;logging.basicConfig(level=logging.INFO)

from aiohttp import web


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')


async def init(loop):
    host = '127.0.0.1'
    port = 9000
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    apprunner = web.AppRunner(app)
    await apprunner.setup()
    srv = await loop.create_server(apprunner.server, host, port)
    logging.info('server started at %s:%d...' % (host, port))
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
