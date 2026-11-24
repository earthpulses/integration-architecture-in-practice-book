"""Verify signed webhooks and drop duplicates."""
import hashlib, hmac, sqlite3, time

def sign(secret, timestamp, body):
    msg = ("%s." % timestamp).encode() + body
    return hmac.new(secret.encode(), msg, hashlib.sha256).hexdigest()

def verify(secret, body, signature, timestamp, tolerance=300, now=None):
    """True only if the signature matches and the timestamp is recent."""
    now = time.time() if now is None else now
    try:
        if abs(now - float(timestamp)) > tolerance:
            return False                       # too old (replay) or too far ahead
    except (TypeError, ValueError):
        return False
    return hmac.compare_digest(sign(secret, timestamp, body), signature or "")

class Ledger:
    """Remember event IDs so a redelivered event is processed once."""
    def __init__(self, path=":memory:"):
        self.db = sqlite3.connect(path)
        self.db.execute("CREATE TABLE IF NOT EXISTS seen (id TEXT PRIMARY KEY)")

    def first_time(self, event_id):
        try:
            with self.db:
                self.db.execute("INSERT INTO seen (id) VALUES (?)", (event_id,))
            return True
        except sqlite3.IntegrityError:
            return False
