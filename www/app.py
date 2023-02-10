import asyncio

import logging;

logging.basicConfig(level=logging.INFO)

from aiohttp import web


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')


async def init(loop):
    host = '127.0.0.1'
    port = 9000
    app = web.Application(loop=loop, middlewares=[logger_factory, response_factory])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'handlers')
    add_static(app)
    app.router.add_route('GET', '/', index)
    apprunner = web.AppRunner(app)
    await apprunner.setup()
    srv = await loop.create_server(apprunner.server, host, port)
    logging.info('server started at %s:%d...' % (host, port))
    return srv


loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()


async def logger_factory(app, handler):
    async def logger(request):
        # 记录日记
        logging.info('Request: %s %s' % (request.method, request.path))
        # 继续处理请求
        return (await handler(request))

    return logger


async def response_factory(app, handler):
    async def response(request):
        # 结果
        r = await handler(request)
        if isinstance(r,web.StreamResponse):
            return r
        if isinstance(r,bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r,str):
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type='text/html;charset=utf-8'
            return resp

