# Companion Code

The companion code is a small set of Python modules that the chapters use and discuss, each exercised by automated tests. It needs Python 3.9 or later. The lab server uses only the standard library; the client and tests need two packages and the mapping module a third:

```bash
pip install requests pytest pydantic
python3 -m pytest -q test_all.py test_more.py
```

The code is copyright 2026 Stefan Živanović and is licensed under the MIT License, which is included in the archive. Like the rest of this book, it was generated with AI assistance (Claude, by Anthropic) under the author's direction, and each file in the archive says so in its header. It is provided as is, without warranty.

All tests run in a few seconds and need no external services. They include crash tests (a poller killed mid-batch), failure injection (a server that is rate-limited or randomly unavailable), and idempotency tests (a duplicate request, a duplicate event). The listings in the Kafka, OpenTelemetry, and platform chapters are sketches that need external services, and are not part of this set.

{{tbl codefiles | The companion modules and where the book discusses them}}

| Module | Purpose | Chapter |
|---|---|---|
| `labserver.py` | A local order API with pagination, rate limiting, random failures, OAuth tokens, and idempotency keys | 1, 10, and throughout |
| `client.py` | A hardened HTTP client with retries, backoff, jitter, and cursor pagination | 14 |
| `tokens.py` | An OAuth 2.0 client-credentials token provider | 13 |
| `poller.py` | A watermark poller with an overlap window and atomic checkpoints | 14 |
| `ratelimit.py` | A token-bucket rate limiter | 14 |
| `runloop.py` | A run loop that quarantines bad data and reports a summary | 14 |
| `webhook.py` | Webhook signature verification and an event-ID ledger | 13 |
| `outbox.py` | A transactional outbox with an at-least-once relay | 7, 8 |
| `reconcile.py` | A reconciliation comparison and a deletion guard | 15 |
| `openapi_recon.py` | An OpenAPI analyzer that lists hints and gaps | 10 |
| `mapping.py` | Typed validation and mapping of an order | 12 |

The modules discussed in full in a chapter are not repeated here. The lab server, the outbox, and the tests follow.

## The Lab Server

{{code labserver.py}}

## The Transactional Outbox

{{code outbox.py}}

## Tests, Part One

{{code test_all.py}}

## Tests, Part Two

{{code test_more.py}}
