"""Transactional outbox: write the business change and the event together."""
import json, sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, status TEXT);
CREATE TABLE IF NOT EXISTS outbox (
  seq INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE,
  payload TEXT, sent INTEGER DEFAULT 0);
"""

def connect(path=":memory:"):
    db = sqlite3.connect(path)
    db.executescript(SCHEMA)
    return db

def place_order(db, order_id, status="CREATED"):
    with db:                          # one transaction: both rows or neither
        db.execute("INSERT OR REPLACE INTO orders VALUES (?, ?)",
                   (order_id, status))
        event = {"event_id": "%s:%s" % (order_id, status), "order_id": order_id,
                 "status": status}
        db.execute("INSERT OR IGNORE INTO outbox (event_id, payload) "
                   "VALUES (?, ?)", (event["event_id"], json.dumps(event)))

def relay(db, publish, batch=100):
    """Publish unsent events in order, then mark them sent. A crash between the
    two steps causes a re-publish: delivery is at-least-once, so consumers
    must dedupe."""
    rows = db.execute("SELECT seq, payload FROM outbox WHERE sent = 0 "
                      "ORDER BY seq LIMIT ?", (batch,)).fetchall()
    for seq, payload in rows:
        publish(json.loads(payload))
        with db:
            db.execute("UPDATE outbox SET sent = 1 WHERE seq = ?", (seq,))
    return len(rows)
