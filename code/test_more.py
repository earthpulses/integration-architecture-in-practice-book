import json, subprocess, sys, pytest
import mapping, openapi_recon
from pydantic import ValidationError

SPEC = {
    "openapi": "3.1.0",
    "info": {"title": "Orders", "version": "2.4"},
    "servers": [{"url": "https://api.example.com/v2"}],
    "components": {
        "securitySchemes": {
            "oauth": {"type": "oauth2", "flows": {"clientCredentials": {}}}
        }
    },
    "paths": {
        "/orders": {
            "get": {
                "parameters": [
                    {"name": "updatedSince", "in": "query"},
                    {"name": "cursor", "in": "query"},
                ],
                "responses": {"200": {}, "429": {}},
            },
            "post": {"responses": {"201": {}}},
        },
        "/orders/{id}": {"get": {"responses": {"200": {}}}},
        "/orders/bulk": {
            "post": {
                "parameters": [{"name": "Idempotency-Key", "in": "header"}],
                "responses": {"202": {}},
            }
        },
    },
}


def test_recon_finds_hints_and_gaps():
    info = openapi_recon.analyze(SPEC)
    assert info["security"] == {"oauth": "oauth2 (clientCredentials)"}
    assert any("incremental" in h for h in info["hints"])
    assert any("asynchronous" in h for h in info["hints"])
    assert any("bulk candidate" in h for h in info["hints"])
    assert any("POST /orders has no Idempotency-Key" in g for g in info["gaps"])
    assert any("GET /orders/{id} documents no 429" in g for g in info["gaps"])
    assert not any("GET /orders is a list" in g for g in info["gaps"])


def test_recon_cli(tmp_path):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(SPEC))
    out = subprocess.run(
        [sys.executable, "openapi_recon.py", str(p)],
        capture_output=True,
        text=True,
    )
    assert out.returncode == 0 and "Gaps to ask about" in out.stdout


def test_mapping_happy_path_and_traps():
    o = mapping.OrderIn(
        id="00042",
        total="19.90",
        currency="EUR",
        status="3",
        created_at="2026-11-23T10:00:00+01:00",
    )
    t = mapping.to_target(o)
    assert (
        t["externalId"] == "00042"
        and t["amount"] == "19.90"
        and t["createdAt"].startswith("2026-11-23T09:00:00")
    )
    with pytest.raises(ValidationError):
        mapping.OrderIn(
            id="1",
            total="1",
            currency="EUR",
            status="1",
            created_at="2026-11-23T10:00:00",
        )  # no zone
    with pytest.raises(ValidationError):
        mapping.OrderIn(
            id="1",
            total="-1",
            currency="EUR",
            status="1",
            created_at="2026-11-23T10:00:00Z",
        )
    with pytest.raises(ValueError):
        mapping.to_target(
            mapping.OrderIn(
                id="1",
                total="1",
                currency="EUR",
                status="7",
                created_at="2026-11-23T10:00:00Z",
            )
        )


import ratelimit, runloop


def test_token_bucket_paces_calls():
    t = [0.0]
    slept = []

    def sleep(s):
        slept.append(s)
        t[0] += s

    b = ratelimit.TokenBucket(rate=2, burst=2, clock=lambda: t[0], sleep=sleep)
    for _ in range(6):
        b.acquire()
    assert (
        not slept[:0] and abs(sum(slept) - 2.0) < 1e-9
    )  # 2 burst free, then 4 at 2/s


def test_run_loop_quarantines_bad_data_but_stops_on_bugs(tmp_path):
    q = str(tmp_path / "q.jsonl")

    def upsert(rec):
        if rec["id"] == "bad":
            raise ValueError("unmapped status 7")
        if rec["id"] == "boom":
            raise RuntimeError("target down")

    counts = runloop.process(
        [{"id": "a"}, {"id": "bad"}, {"id": "b"}], upsert, q
    )
    assert (counts["read"], counts["written"], counts["quarantined"]) == (
        3,
        2,
        1,
    )
    line = json.loads(open(q).readline())
    assert (
        line["reason"] == "unmapped status 7" and line["record"]["id"] == "bad"
    )
    with pytest.raises(RuntimeError):
        runloop.process([{"id": "a"}, {"id": "boom"}], upsert, q)


import reconcile


def test_reconcile_report_and_deletion_guard():
    src = {"a": "1", "b": "2", "c": "3"}
    tgt = {"a": "1", "b": "X", "z": "9"}
    r = reconcile.compare(src, tgt)
    assert r["missing_in_target"] == ["c"] and r["orphans_in_target"] == ["z"]
    assert r["changed"] == ["b"]
    with pytest.raises(RuntimeError):
        reconcile.deletion_guard(r, max_fraction=0.05)  # 1 of 3 is too many
    assert reconcile.deletion_guard(r, max_fraction=0.5) == ["z"]
