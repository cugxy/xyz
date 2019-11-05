# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：       1_6_WSGI.py
   Description :
   Author :          cugxy
   date：            2019/11/1
-------------------------------------------------
   Change Activity:
                     2019/11/1
-------------------------------------------------
问题:
WSGI 最大的问题是原生同步性. 对于每个传入的请求, 都会调用下面代码中的 app 函数一次, 当函数返回时, 必须发出响应. 这意味着, 每次调用
app 函数时, 在响应准备好之前, 都会阻塞.
对于这种情况下编写的微服务, 代码总是需要等待各种网络资源的响应. 换句话说, 这是你的应用时停顿的, 在所有东西准备好之前, 客户端都会被阻塞.
对于 HTTP API 来说, 这样做的问题不大. 我们并非讨论构建双向应用(如基于 Web 嵌套字的应用). 但是, 当你的应用同事收到多个调用请求时会
发生什么呢?
WSGI 服务器运行运行一个线程池, 来并发服务多个请求, 但你不可能运行几千个线程; 一旦线程池耗尽, 即便微服务除等待后端服务响应外无所事事,
下一个请求还是会阻塞客户访问.

解决思路:
出于上述原因及其他因素, 诸如 Twisted 或 Tornado 的非 WSGI 框架, 以及 JavaScript 领域的 Node.js 都大获成功, 因为他们完全时异步框架.
在编写 Twisted 应用时, 可使用回调来暂停和回复生成响应的工作. 此时, 可接受一个新请求并开始处理. 该模型极大地缩短了进程的停顿时间. 可
服务数千个并发请求. 当然, 这并非说应用会更快的返回每个响应, 只是说一个进程可接受更多的并发请求, 在数据准备好之前, 能在请求间进行切换.

在 WSGI 标准中没有一个简单方式可以做到同样的事情, 虽然社区争论了多年, 但最终没能达成共识. 社区最终可能放弃 WSGI 标准.

不过还有一个诀窍来提升同步的 Web 应用, 这就是 greenlet.

异步编程的一般原则是, 让进程处理多个并发执行的上下文来模拟并行处理方式. 异步应用使用一个事件循环, 当一个时间触发时暂停或恢复执行上下文;
只有一个上下文处于活动状态, 上下文之间进行轮替. 代码中的显式指令将告诉事件循环, 哪里可以暂停执行. 这时, 进程将查找其他待处理的线程进行
恢复. 最终, 进程将回到函数暂停的地方并继续运行. 从一个执行上下文移动到另一个称为 '切换'.

"""


import json
import time
from greenlet import greenlet
from gevent import monkey; monkey.patch_all()
from twisted.web import server, resource
from twisted.internet import reactor, endpoints
from aiohttp import web

# ------------------------- WSGI ----------------------------------------

def app(environ, start_response):
    headers = [('Content-type', 'application/json')]
    start_response('200 OK', headers)
    return [bytes(json.dumps({'time': time.time()}), 'utf8')]


# ------------------------- greenlet ----------------------------------------

def test1(x, y):
    z = gr2.switch


def test2(u):
    print(u)
    gr1.switch(42)


gr1 = greenlet(test1)
gr2 = greenlet(test2)


# ------------------------- twisted ----------------------------------------

class Simple(resource.Resource):
    isLeaf = True

    def render_GET(self, request):
        request.responseHeaders.addRawHeader(b"content-type", b"application/json")
        return bytes(json.dumps({'time': time.time()}), 'utf8')


# ------------------------- aiohttp ----------------------------------------

async def handle(request):
    return web.json_response({'time': time.time()})


if __name__ == '__main__':
    if 0:
        site = server.Site(Simple())
        endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
        endpoint.listen(site)
        reactor.run()
    if 1:
        app = web.Application()
        app.router.add_get('/', handle)
        web.run_app(app)

