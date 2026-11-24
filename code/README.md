# Companion code

For *Integration Architecture in Practice* by Stefan Živanović (Solution Architect, Prague), First Edition, 2026. Generated with AI assistance (Claude, by Anthropic), under the author's direction. MIT License (see `LICENSE`).

```bash
pip install -r requirements.txt
python3 -m pytest -q test_all.py test_more.py
python3 labserver.py --port 8080 --no-auth
```

| Module | Purpose | Chapter |
|---|---|---|
| `labserver.py` | Local order API with pagination, rate limiting, random failures, OAuth tokens, and idempotency keys | 1, 10 |
| `client.py` | Hardened HTTP client: timeouts, retries, backoff with jitter, `Retry-After`, cursor pagination | 14 |
| `tokens.py` | OAuth 2.0 client-credentials token provider | 13 |
| `poller.py` | Watermark poller with overlap window and atomic checkpoint | 14 |
| `ratelimit.py` | Token-bucket rate limiter | 14 |
| `runloop.py` | Run loop with quarantine and run summary | 14 |
| `webhook.py` | Webhook signature verification and event-ID ledger | 13 |
| `outbox.py` | Transactional outbox with an at-least-once relay | 7, 8 |
| `reconcile.py` | Reconciliation comparison and deletion guard | 15 |
| `openapi_recon.py` | OpenAPI analyzer that lists hints and gaps | 10 |
| `mapping.py` | Typed validation and mapping of an order | 12 |
| `test_all.py`, `test_more.py` | The test suite (18 tests) | 16 |
