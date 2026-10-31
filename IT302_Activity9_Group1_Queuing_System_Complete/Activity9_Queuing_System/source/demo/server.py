"""Loopback classroom demo, not a production queuing implementation."""
import argparse
import hmac
import json
import os
import secrets
import threading
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

class State:
    def __init__(self, duplicate_bug=False):
        self.lock = threading.Lock()
        self.duplicate_bug = duplicate_bug
        self.reset()

    def reset(self):
        self.attempts = 0
        self.locked = False
        self.sessions = set()
        self.tickets = []
        self.next_number = 1

def build_server(host='127.0.0.1', port=0, duplicate_bug=False):
    if host != '127.0.0.1':
        raise ValueError('The classroom demo must bind to loopback only.')
    state = State(duplicate_bug)
    user = os.environ.get('DEMO_USER', 'staff.demo')
    password = os.environ.get('DEMO_PASSWORD', 'DemoQueue123!')
    reset_token = os.environ.get('TEST_RESET_TOKEN', 'local-demo-reset')

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass  # Avoid credential/request payload logging.

        def reply(self, status, body, cookie=None):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            if cookie:
                self.send_header('Set-Cookie', cookie)
            self.end_headers()
            self.wfile.write(data)

        def authorized(self):
            cookie = SimpleCookie()
            cookie.load(self.headers.get('Cookie', ''))
            sid = cookie.get('sid')
            return sid is not None and sid.value in state.sessions

        def do_GET(self):
            route = self.path.split('?')[0]
            if route in ('/', '/login', '/queue'):
                raw = Path(__file__).with_name('index.html').read_bytes()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)
            elif route == '/health':
                self.reply(200, {'app': 'Group 1 Queue Demo', 'build': 'Q-DEMO-1.0-bug' if state.duplicate_bug else 'Q-DEMO-1.1-fixed'})
            elif route == '/api/tickets':
                with state.lock:
                    if not self.authorized():
                        return self.reply(401, {'message': 'Authentication required'})
                    self.reply(200, {'tickets': list(state.tickets), 'username': user})
            else:
                self.reply(404, {'message': 'Not found'})

        def do_POST(self):
            try:
                body = json.loads(self.rfile.read(int(self.headers.get('Content-Length', '0'))) or b'{}')
            except (ValueError, json.JSONDecodeError):
                return self.reply(400, {'message': 'Invalid JSON'})
            with state.lock:
                if self.path == '/__test__/reset':
                    if not hmac.compare_digest(self.headers.get('X-Test-Token', ''), reset_token):
                        return self.reply(403, {'message': 'Reset denied'})
                    state.reset()
                    return self.reply(200, {'reset': True})
                if self.path == '/api/login':
                    supplied = str(body.get('password', ''))
                    if state.locked:
                        return self.reply(423, {'message': 'Account locked after 5 invalid attempts'})
                    if len(supplied) < 8:
                        return self.reply(400, {'message': 'Password must contain at least 8 characters'})
                    if body.get('username') == user and hmac.compare_digest(supplied, password):
                        sid = secrets.token_urlsafe(24)
                        state.sessions.add(sid)
                        state.attempts = 0
                        return self.reply(200, {'username': user}, f'sid={sid}; Path=/; HttpOnly; SameSite=Lax')
                    state.attempts += 1
                    state.locked = state.attempts >= 5
                    return self.reply(423 if state.locked else 401, {
                        'message': 'Account locked after 5 invalid attempts' if state.locked else f'Invalid credentials (attempt {state.attempts} of 5)'
                    })
                if self.path == '/api/tickets':
                    if not self.authorized():
                        return self.reply(401, {'message': 'Authentication required'})
                    customer = str(body.get('customer', '')).strip()
                    service = body.get('service')
                    if not customer or service not in ['Registrar', 'Cashier']:
                        return self.reply(400, {'message': 'Enter a customer and select a valid service'})
                    existing = next((t for t in state.tickets if t['customer'] == customer and t['service'] == service and t['status'] == 'Waiting'), None)
                    if existing and not state.duplicate_bug:
                        return self.reply(409, {'message': 'Customer already has an active ticket for this service', 'ticket': existing})
                    ticket = {'number': f'Q-{state.next_number:03d}', 'customer': customer, 'service': service, 'status': 'Waiting'}
                    state.next_number += 1
                    state.tickets.append(ticket)
                    return self.reply(201, {'message': f'Ticket {ticket["number"]} created', 'ticket': ticket})
                self.reply(404, {'message': 'Not found'})

    return ThreadingHTTPServer((host, port), Handler)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--duplicate-bug', action='store_true')
    args = parser.parse_args()
    server = build_server(port=args.port, duplicate_bug=args.duplicate_bug)
    print(f'Group 1 classroom demo: http://127.0.0.1:{server.server_port}', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
