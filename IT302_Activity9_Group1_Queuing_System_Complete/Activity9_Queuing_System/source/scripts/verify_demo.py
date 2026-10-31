"""Dependency-free HTTP checks for the bundled sample; these are NOT Selenium evidence."""
import json
import threading
from http.cookiejar import CookieJar
from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.error import HTTPError
from demo.server import build_server

def verify(bug):
    server = build_server(duplicate_bug=bug)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    base = f'http://127.0.0.1:{server.server_port}'
    client = build_opener(HTTPCookieProcessor(CookieJar()))
    def call(path, body):
        request = Request(base + path, data=json.dumps(body).encode(), headers={'Content-Type':'application/json'}, method='POST')
        try:
            response = client.open(request, timeout=5)
        except HTTPError as error:
            response = error
        return response.code, json.loads(response.read())
    try:
        assert call('/api/login', {'username':'staff.demo','password':'Abc123!'})[0] == 400
        for n in range(5):
            assert call('/api/login', {'username':'staff.demo','password':'WrongPass123!'})[0] == (423 if n == 4 else 401)
        req = Request(base + '/__test__/reset', data=b'{}', headers={'X-Test-Token':'local-demo-reset'}, method='POST')
        client.open(req, timeout=5).close()
        assert call('/api/login', {'username':'staff.demo','password':'DemoQueue123!'})[0] == 200
        assert call('/api/tickets', {'customer':'CUST-001','service':'Registrar'})[0] == 201
        assert call('/api/tickets', {'customer':'CUST-001','service':'Registrar'})[0] == (201 if bug else 409)
        with client.open(base + '/api/tickets', timeout=5) as response:
            assert len(json.loads(response.read())['tickets']) == (2 if bug else 1)
        print(f'HTTP sample checks passed: duplicate_bug={bug}; records={2 if bug else 1}')
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=5)

if __name__ == '__main__':
    verify(True)
    verify(False)
