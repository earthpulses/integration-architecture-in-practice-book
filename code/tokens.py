"""OAuth 2.0 client-credentials token cache with early refresh."""
import threading, time
import requests

class TokenProvider:
    def __init__(self, token_url, client_id, client_secret, leeway=60):
        self.url, self.leeway = token_url, leeway
        self.cid, self.secret = client_id, client_secret
        self._token, self._expires = None, 0.0
        self._lock = threading.Lock()
        self.fetches = 0

    def get(self):
        with self._lock:                      # one thread refreshes; others wait
            if self._token is None or time.time() > self._expires - self.leeway:
                self._refresh()
            return self._token

    def invalidate(self):
        with self._lock:
            self._token = None

    def _refresh(self):
        r = requests.post(self.url, timeout=(5, 15), data={
            "grant_type": "client_credentials",
            "client_id": self.cid, "client_secret": self.secret})
        r.raise_for_status()
        body = r.json()
        self._token = body["access_token"]
        self._expires = time.time() + float(body.get("expires_in", 300))
        self.fetches += 1
