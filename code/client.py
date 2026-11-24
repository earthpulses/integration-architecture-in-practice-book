"""A hardened HTTP client: timeouts, bounded retries, backoff with jitter,
Retry-After, and cursor pagination."""
import random, time
from email.utils import parsedate_to_datetime
import requests

RETRY_STATUS = {429, 500, 502, 503, 504}
SAFE_METHODS = {"GET", "HEAD", "PUT", "DELETE", "OPTIONS"}
TIMEOUT = (5, 30)                       # (connect, read) seconds

class ApiError(Exception):
    def __init__(self, status, body, url):
        super().__init__("%s from %s: %s" % (status, url, body[:200]))
        self.status, self.body, self.url = status, body, url

def build_session(token_provider=None):
    s = requests.Session()
    s.headers["User-Agent"] = "orders-sync/1.0"
    s.token_provider = token_provider
    return s

def parse_retry_after(value):
    """Seconds to wait, from either '3' or an HTTP date; None if absent."""
    if not value:
        return None
    if value.isdigit():
        return float(value)
    try:
        when = parsedate_to_datetime(value)
        return max(0.0, when.timestamp() - time.time())
    except (TypeError, ValueError):
        return None

def backoff_delay(attempt, base=0.5, cap=30.0):
    """Full jitter: a random wait between 0 and min(cap, base * 2^attempt)."""
    return random.uniform(0, min(cap, base * 2 ** attempt))

def request(session, method, url, *, max_attempts=6, sleep=time.sleep, **kw):
    kw.setdefault("timeout", TIMEOUT)
    headers = dict(kw.pop("headers", {}) or {})
    retryable = method.upper() in SAFE_METHODS or "Idempotency-Key" in headers
    refreshed = False
    for attempt in range(max_attempts):
        if session.token_provider:
            headers["Authorization"] = "Bearer " + session.token_provider.get()
        try:
            r = session.request(method, url, headers=headers, **kw)
        except (requests.ConnectionError, requests.Timeout):
            if not retryable or attempt == max_attempts - 1:
                raise
            sleep(backoff_delay(attempt))
            continue
        if r.status_code == 401 and session.token_provider and not refreshed:
            session.token_provider.invalidate()      # one refresh, then give up
            refreshed = True
            continue
        last = attempt == max_attempts - 1
        if r.status_code in RETRY_STATUS and retryable and not last:
            wait = parse_retry_after(r.headers.get("Retry-After"))
            sleep(wait if wait is not None else backoff_delay(attempt))
            continue
        if r.status_code >= 400:
            raise ApiError(r.status_code, r.text, url)
        return r
    raise RuntimeError("unreachable")

def iter_records(session, url, params=None, limit=100, max_pages=10_000):
    """Yield every record from a cursor-paginated endpoint."""
    params = dict(params or {}, limit=limit)
    for _ in range(max_pages):                 # guard against endless loops
        body = request(session, "GET", url, params=params).json()
        yield from body["results"]
        cursor = body.get("nextCursor")
        if not cursor:
            return
        params = {"cursor": cursor, "limit": limit}   # cursor replaces filters
    raise RuntimeError("pagination did not finish in %d pages" % max_pages)
