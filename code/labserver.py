#!/usr/bin/env python3
"""A small order API for the exercises in this book (standard library only).

Run it:   python3 labserver.py --port 8080
Options:  --rate-limit N   allow N requests per second, then answer 429
          --flaky P        answer 503 for a fraction P of requests
          --token-ttl S    lifetime of OAuth tokens in seconds
          --no-auth        skip bearer-token checks
"""
import argparse, base64, json, random, threading, time, uuid
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

LOCK = threading.Lock()
ORDERS = {}          # id -> order dict
IDEMPOTENT = {}      # Idempotency-Key -> (status, body)
TOKENS = {}          # access token -> expiry (epoch seconds)
WINDOW = []          # request timestamps for the rate limiter
CFG = {"rate_limit": 0, "flaky": 0.0, "token_ttl": 3600, "auth": True}
CLIENT = ("larkspur-client", "s3cret")
BASE = datetime(2026, 11, 1, tzinfo=timezone.utc)

def iso(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def seed(n):
    for i in range(n):
        oid = "A%04d" % (1000 + i)
        ORDERS[oid] = {"id": oid, "sku": "TENT-%d" % (i % 7), "qty": 1 + i % 3,
                       "status": "CREATED",
                       "updatedAt": iso(BASE + timedelta(seconds=i * 30))}

def page(since, limit, cursor):
    rows = sorted(ORDERS.values(), key=lambda o: (o["updatedAt"], o["id"]))
    if cursor:
        ts, oid = base64.urlsafe_b64decode(cursor).decode().split("|")
        rows = [o for o in rows if (o["updatedAt"], o["id"]) > (ts, oid)]
    elif since:
        rows = [o for o in rows if o["updatedAt"] > since]
    chunk = rows[:limit]
    nxt = None
    if len(rows) > limit:
        last = chunk[-1]
        raw = ("%s|%s" % (last["updatedAt"], last["id"])).encode()
        nxt = base64.urlsafe_b64encode(raw).decode()
    return {"results": chunk, "nextCursor": nxt}

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    def send(self, status, body=None, headers=None):
        data = json.dumps(body).encode() if body is not None else b""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def chaos(self):
        """Rate limit and random failures; True if the request was answered."""
        now = time.time()
        with LOCK:
            WINDOW[:] = [t for t in WINDOW if now - t < 1.0]
            WINDOW.append(now)
            limited = CFG["rate_limit"] and len(WINDOW) > CFG["rate_limit"]
        if limited:
            self.send(429, {"error": "rate_limited"}, {"Retry-After": "1"})
            return True
        if CFG["flaky"] and random.random() < CFG["flaky"]:
            self.send(503, {"error": "unavailable"})
            return True
        return False

    def authorized(self):
        if not CFG["auth"]:
            return True
        token = self.headers.get("Authorization", "")[7:]
        if TOKENS.get(token, 0) > time.time():
            return True
        self.send(401, {"error": "invalid_token"}, {"WWW-Authenticate": "Bearer"})
        return False

    def body(self):
        n = int(self.headers.get("Content-Length") or 0)
        return self.rfile.read(n) if n else b""

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/oauth/token":
            form = parse_qs(self.body().decode())
            got = (form.get("client_id", [""])[0],
                   form.get("client_secret", [""])[0])
            if form.get("grant_type") != ["client_credentials"] or got != CLIENT:
                return self.send(401, {"error": "invalid_client"})
            token = uuid.uuid4().hex
            TOKENS[token] = time.time() + CFG["token_ttl"]
            return self.send(200, {"access_token": token, "token_type": "Bearer",
                                   "expires_in": CFG["token_ttl"]})
        if self.chaos() or not self.authorized():
            return
        if path == "/orders":
            key = self.headers.get("Idempotency-Key")
            if not key:
                return self.send(400, {"error": "Idempotency-Key required"})
            with LOCK:
                if key in IDEMPOTENT:
                    status, body = IDEMPOTENT[key]
                    return self.send(status, body, {"Idempotent-Replay": "true"})
                data = json.loads(self.body() or b"{}")
                oid = "A%04d" % (1000 + len(ORDERS))
                now = iso(datetime.now(timezone.utc))
                order = {"id": oid, "sku": data.get("sku", "?"),
                         "qty": data.get("qty", 1), "status": "CREATED",
                         "updatedAt": now}
                ORDERS[oid] = order
                IDEMPOTENT[key] = (201, order)
            return self.send(201, order, {"Location": "/orders/" + oid})
        if path.startswith("/admin/touch/"):
            oid = path.rsplit("/", 1)[1]
            with LOCK:
                if oid in ORDERS:
                    ORDERS[oid]["updatedAt"] = iso(datetime.now(timezone.utc))
                    return self.send(200, ORDERS[oid])
            return self.send(404, {"error": "not_found"})
        self.send(404, {"error": "not_found"})

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/health":
            return self.send(200, {"status": "ok"})
        if self.chaos() or not self.authorized():
            return
        q = parse_qs(url.query)
        if url.path == "/orders":
            limit = min(int(q.get("limit", ["50"])[0]), 500)
            with LOCK:
                out = page(q.get("updatedSince", [""])[0], limit,
                           q.get("cursor", [""])[0])
            return self.send(200, out)
        if url.path.startswith("/orders/"):
            order = ORDERS.get(url.path.rsplit("/", 1)[1])
            if order:
                return self.send(200, order)
            return self.send(404, {"error": "not_found"})
        self.send(404, {"error": "not_found"})

def make_server(port=8080, **cfg):
    CFG.update(cfg)
    return ThreadingHTTPServer(("127.0.0.1", port), Handler)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8080)
    ap.add_argument("--rate-limit", type=int, default=0)
    ap.add_argument("--flaky", type=float, default=0.0)
    ap.add_argument("--token-ttl", type=int, default=3600)
    ap.add_argument("--no-auth", action="store_true")
    a = ap.parse_args()
    seed(250)
    srv = make_server(a.port, rate_limit=a.rate_limit, flaky=a.flaky,
                      token_ttl=a.token_ttl, auth=not a.no_auth)
    print("lab server on http://127.0.0.1:%d" % a.port)
    print("client id / secret: %s / %s" % CLIENT)
    srv.serve_forever()
