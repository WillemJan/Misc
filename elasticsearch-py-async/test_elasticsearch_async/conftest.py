import asyncio
import json
from urllib.parse import urlparse, parse_qsl

from aiohttp.server import ServerHttpProtocol
from aiohttp import Response

from pytest import yield_fixture, fixture

from elasticsearch_async import AIOHttpConnection, AsyncElasticsearch


@yield_fixture
def connection(event_loop, server, port):
    connection = AIOHttpConnection(port=port, loop=event_loop)
    yield connection
    event_loop.run_until_complete(connection.close())

class DummyElasticsearch(ServerHttpProtocol):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._responses = {}
        self.calls = []

    def register_response(self, path, response={}, status=200):
        self._responses[path] = status, response

    @asyncio.coroutine
    def handle_request(self, message, payload):
        url = urlparse(message.path)

        params = dict(parse_qsl(url.query))
        body = yield from payload.read()
        body = json.loads(body.decode('utf-8')) if body else ''

        self.calls.append((message.method, url.path, body, params))

        if url.path in self._responses:
            status, body = self._responses.pop(url.path)
            if asyncio.iscoroutine(body):
                body = yield from body
        else:
            status = 200
            body = {
                'method': message.method,
                'params': params,
                'path': url.path,
                'body': body
            }

        out = json.dumps(body).encode('utf-8')

        response = Response(self.writer, status)
        response.send_headers()
        response.write(out)
        yield from response.write_eof()

i = 0
@fixture
def port():
    global i
    i += 1
    return 8080 + i

@fixture
def server(event_loop, port):
    server = DummyElasticsearch(debug=True, keep_alive=75)
    f = event_loop.create_server(lambda: server, '127.0.0.1', port)
    event_loop.run_until_complete(f)
    return server

@yield_fixture
def client(event_loop, server, port):
    c = AsyncElasticsearch([{'host': '127.0.0.1','port': port}], loop=event_loop)
    yield c
    c.transport.close()

@fixture
def sniff_data():
    return {
        "ok" : True,
        "cluster_name" : "super_cluster",
        "nodes" : {
            "node1" : {
                "name": "Thunderbird",
                "transport_address": "node1/127.0.0.1:9300",
                "host": "node1",
                "ip": "127.0.0.1",
                "version": "2.1.0",
                "build": "72cd1f1",
                "http_address": "node1/127.0.0.1:9200",
                "attributes": {
                    "testattr": "test"
                }
            }
        }
    }
