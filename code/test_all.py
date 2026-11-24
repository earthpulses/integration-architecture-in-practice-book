import json, os, threading, time
import pytest, requests
import labserver, client, tokens, poller, webhook, outbox


@pytest.fixture(scope="module")
def server():
    labserver.ORDERS.clear()
    labserver.seed(250)
    srv = labserver.make_server(
        0, rate_limit=0, flaky=0.0, token_ttl=3600, auth=False
    )
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    yield "http://127.0.0.1:%d" % srv.server_address[1]
    srv.shutdown()


def no_sleep(_):
    pass


def test_pagination_returns_every_record_once(server):
    s = client.build_session()
    ids = [
        r["id"] for r in client.iter_records(s, server + "/orders", limit=40)
    ]
    assert len(ids) == 250 and len(set(ids)) == 250


def test_retry_after_is_honored(server):
    labserver.CFG.update(rate_limit=3)
    waits = []
    s = client.build_session()
    try:
        for _ in range(8):
            client.request(
                s,
                "GET",
                server + "/orders",
                params={"limit": 1},
                sleep=lambda w: (waits.append(w), time.sleep(w)),
            )
    finally:
        labserver.CFG.update(rate_limit=0)
    assert waits and all(w == 1.0 for w in waits)  # the server said 1 second


def test_flaky_server_eventually_succeeds(server):
    labserver.CFG.update(flaky=0.5)
    s = client.build_session()
    try:
        r = client.request(
            s, "GET", server + "/orders/A1000", max_attempts=12, sleep=no_sleep
        )
    finally:
        labserver.CFG.update(flaky=0.0)
    assert r.json()["id"] == "A1000"


def test_post_without_idempotency_key_is_not_retried(server):
    labserver.CFG.update(flaky=1.0)
    s = client.build_session()
    calls = []
    real = s.request
    s.request = lambda *a, **k: (calls.append(1), real(*a, **k))[1]
    try:
        with pytest.raises(client.ApiError):
            client.request(
                s, "POST", server + "/orders", json={"sku": "X"}, sleep=no_sleep
            )
    finally:
        labserver.CFG.update(flaky=0.0)
    assert len(calls) == 1


def test_idempotent_post_replays(server):
    s = client.build_session()
    h = {"Idempotency-Key": "k-123"}
    a = client.request(
        s, "POST", server + "/orders", json={"sku": "T", "qty": 2}, headers=h
    )
    b = client.request(
        s, "POST", server + "/orders", json={"sku": "T", "qty": 2}, headers=h
    )
    assert a.status_code == 201 and a.json()["id"] == b.json()["id"]
    assert b.headers["Idempotent-Replay"] == "true"


def test_backoff_bounds():
    for attempt in range(10):
        d = client.backoff_delay(attempt, base=0.5, cap=30)
        assert 0 <= d <= min(30, 0.5 * 2**attempt)


def test_parse_retry_after():
    assert client.parse_retry_after("3") == 3.0
    assert client.parse_retry_after(None) is None
    assert client.parse_retry_after("garbage") is None


def test_token_refresh_and_401_recovery():
    labserver.ORDERS.clear()
    labserver.seed(10)
    srv = labserver.make_server(
        0, rate_limit=0, flaky=0.0, token_ttl=3600, auth=True
    )
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:%d" % srv.server_address[1]
    try:
        tp = tokens.TokenProvider(base + "/oauth/token", *labserver.CLIENT)
        s = client.build_session(tp)
        assert client.request(s, "GET", base + "/orders").status_code == 200
        assert tp.fetches == 1
        labserver.TOKENS.clear()  # server forgets the token: surprise 401
        assert client.request(s, "GET", base + "/orders").status_code == 200
        assert tp.fetches == 2  # exactly one refresh
        bad = tokens.TokenProvider(base + "/oauth/token", "x", "y")
        with pytest.raises(requests.HTTPError):
            bad.get()
    finally:
        srv.shutdown()
        labserver.CFG.update(auth=False)


def test_watermark_poller_resumes_without_loss(server, tmp_path):
    labserver.ORDERS.clear()
    labserver.seed(100)
    state = str(tmp_path / "wm.json")
    got = {}

    def upsert(rec):
        got[rec["id"]] = rec

    s = client.build_session()
    assert poller.run_once(s, server, state, upsert) == 100
    # a record changes during the next window; one older record sits
    # inside the overlap
    requests.post(server + "/admin/touch/A1005")
    n = poller.run_once(s, server, state, upsert)
    assert (
        got["A1005"]["updatedAt"] > "2026-11-01T01:00"
    )  # the change was captured
    assert 1 <= n <= 6  # overlap re-reads only a few
    # crash safety: failing mid-batch must not move the watermark
    before = poller.load_watermark(state)
    requests.post(server + "/admin/touch/A1010")

    def boom(rec):
        raise RuntimeError("crash")

    with pytest.raises(RuntimeError):
        poller.run_once(s, server, state, boom)
    assert poller.load_watermark(state) == before
    poller.run_once(s, server, state, upsert)
    assert got["A1010"]["updatedAt"] > before


def test_webhook_signature_and_replay_window():
    body = b'{"event_id":"e1"}'
    ts = str(int(time.time()))
    sig = webhook.sign("topsecret", ts, body)
    assert webhook.verify("topsecret", body, sig, ts)
    assert not webhook.verify("wrong", body, sig, ts)
    assert not webhook.verify("topsecret", body + b" ", sig, ts)
    old = str(int(time.time()) - 3600)
    assert not webhook.verify(
        "topsecret", body, webhook.sign("topsecret", old, body), old
    )
    assert not webhook.verify("topsecret", body, None, ts)
    assert not webhook.verify("topsecret", body, sig, "not-a-number")


def test_ledger_drops_duplicates():
    led = webhook.Ledger()
    assert (
        led.first_time("e1")
        and not led.first_time("e1")
        and led.first_time("e2")
    )


def test_outbox_is_at_least_once_and_dedupe_fixes_it():
    db = outbox.connect()
    outbox.place_order(db, "A1", "CREATED")
    outbox.place_order(db, "A2", "CREATED")
    sent = []

    # crash after publishing the first event but before marking it sent
    def flaky_publish(ev):
        sent.append(ev["event_id"])
        if len(sent) == 1:
            raise RuntimeError("crash after publish")

    with pytest.raises(RuntimeError):
        outbox.relay(db, flaky_publish)
    outbox.relay(
        db, sent.append if False else (lambda ev: sent.append(ev["event_id"]))
    )
    assert sent.count("A1:CREATED") == 2  # duplicate publish: at-least-once
    led = webhook.Ledger()
    processed = [e for e in sent if led.first_time(e)]
    assert sorted(processed) == ["A1:CREATED", "A2:CREATED"]
    assert (
        db.execute("SELECT COUNT(*) FROM outbox WHERE sent=0").fetchone()[0]
        == 0
    )
