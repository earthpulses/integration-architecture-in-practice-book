# Authentication and Authorization

Authentication answers "who are you?" Authorization answers "what may you do?" Integrations usually authenticate as a *machine identity*, not as a person, and the design of that identity is half of the security posture of the whole integration. A shared administrator password pasted into a configuration file is the most common integration vulnerability in enterprises, and it is also the most common cause of outages: the password expires, someone rotates it, an account is locked, and the integration quietly stops.

This chapter teaches the schemes you will meet, the flows that matter for unattended jobs, and the code that handles tokens correctly. It then covers the discipline around credentials that separates a demo from a production integration: where secrets live, how identities are scoped, how they are rotated, and how you verify callers who contact *you*.

!!! goals "In this chapter"
    * Compare the authentication schemes you will meet, and choose one for a given situation
    * Explain the OAuth 2.0 client-credentials flow and implement a token provider that refreshes early and is safe across threads
    * Describe authorization code with PKCE, JWT bearer grants, and mutual TLS, and when each applies
    * Keep secrets out of code and configuration, and rotate them without downtime
    * Design service accounts with least privilege, one identity per integration
    * Verify signed webhooks, and diagnose the common authentication failures

## The Schemes You Will Meet

Eight schemes cover almost everything. {{ref tbl:authschemes}} compares them; read it as a ladder from convenient and weak to strong and demanding.

{{tbl authschemes | Authentication schemes compared}}

| Scheme | How it works | Typical use | Strength | Weakness |
|---|---|---|---|---|
| Basic authentication | Username and password in an `Authorization: Basic` header, encoded but not encrypted | Older internal APIs and tools | Trivial to start | A long-lived secret; no scopes; must use TLS |
| API key | A static key in a header or query string | SaaS and simple partner APIs | Easy | Often over-privileged; leaks into logs if in the query string |
| Bearer token (opaque) | A token obtained elsewhere, sent in a header | Everywhere after login | Short-lived | Needs a token source and refresh logic |
| OAuth 2.0 client credentials | The application exchanges its client ID and secret for an access token | The default for service-to-service calls | Scoped, short-lived, rotatable | Token expiry must be handled |
| OAuth 2.0 authorization code with PKCE | A person signs in and the application receives a token on their behalf | User-facing apps; delegated access | Acts as the user | Refresh-token storage; unsuited to unattended jobs |
| OAuth 2.0 JWT bearer or private key | The application signs a JWT with its private key to obtain a token | Large SaaS platforms, cloud service accounts | No shared secret on the wire | Key management; clock skew |
| Mutual TLS (mTLS) | Both sides present certificates | Banking, regulated, internal meshes | Strong; can bind tokens to the client | Certificate lifecycle burden |
| HMAC signature | Each request or webhook is signed with a shared secret | Webhooks, cloud provider APIs | Tamper-evident | Canonicalization details are fiddly |

Single sign-on protocols such as SAML and OpenID Connect belong in the picture too, but they are for *people* using browsers; an unattended integration should never depend on one.

## OAuth 2.0 Client Credentials: The Workhorse

For service-to-service calls, the standard flow is OAuth 2.0 *client credentials*. {{ref fig:auth-oauth2-client-credentials-sequence}} shows it.

{{fig auth-oauth2-client-credentials-sequence | OAuth 2.0 client credentials: the standard flow for unattended integrations.}}

The integration is registered with an authorization server, which gives it a **client ID** and a **client secret**, along with the scopes it may request. When it needs to call an API, it sends those two values to the authorization server's token endpoint (step 1) and receives an **access token** and its lifetime (step 2). It then calls the target API with the token in an `Authorization: Bearer` header (step 3), and the API validates the token and responds (step 4).

The benefits over a password are significant. The token is *short-lived*, usually minutes to an hour, so a leaked token expires on its own. It is *scoped*: it grants only the permissions the client was registered for. And the long-lived secret is sent only to the token endpoint, never to every API. Access tokens may live for minutes or for hours depending on the provider and the tenant configuration, and some vendors support different schemes on different endpoints, so never assume a lifetime: read `expires_in`, refresh early, handle one surprise 401, and confirm which methods each endpoint you need supports.

### A Token Provider That Is Correct

The code that obtains and caches tokens is small and surprisingly easy to get wrong. The version below, from the book's companion code, handles the three requirements: it refreshes *before* expiry, it is safe when many threads ask at once, and it can be told to forget a token that the server rejected.

{{code tokens.py}}

Study the details. The `get` method holds a lock, so if twenty workers all discover an expired token at once, one of them refreshes and the others wait, instead of twenty simultaneous token requests, which some providers treat as abuse. The `leeway` of 60 seconds means that a token is renewed a minute before it expires, so no request is ever sent with a token that dies in flight. And `invalidate` lets the HTTP client, on a 401 response, discard the token and force one refresh (Chapter {{ref ch:python}} shows the client side). The lab server in Appendix {{ref app:codelab}} implements the other end of this exchange, so you can run the whole flow, including a revoked token, on your own machine.

## Authorization Code with PKCE

When an application acts on behalf of a *person*, for example a dashboard that reads the user's calendar, the flow changes. The user is redirected to the identity provider, signs in, and consents, and the application receives a short-lived **authorization code** that it exchanges for a token. **PKCE** (Proof Key for Code Exchange, pronounced "pixie") adds a one-time secret to the exchange, so that an intercepted code is useless to an attacker. It is the recommended pattern for browser and mobile applications.

For unattended integrations this flow is usually wrong, because it ties the integration's authority to one person and to a refresh token that must be stored and renewed. A job that runs on a *user's* delegated grant stops the day the user leaves the company, changes role, or has their password reset. Use client credentials, or a signed JWT, for jobs; reserve the authorization code flow for software with a human at the keyboard.

## JWT Bearer and Mutual TLS

Two stronger options remove the shared secret entirely.

In the **JWT bearer** (or private-key) grant, the application holds a private key. To obtain a token it builds a small JSON Web Token, signs it with that key, and presents it to the token endpoint; the server, which holds the matching public key, verifies the signature. The secret never crosses the network, and the key can be rotated by publishing a new public key. The costs are key management and, because the token carries timestamps, sensitivity to clock skew: a server whose clock is five minutes wrong will reject every assertion.

In **mutual TLS**, both parties present certificates during the connection handshake, so the server knows exactly which client is calling before a single byte of the request is read. It is common in banking and other regulated settings and can be combined with tokens that are *bound* to the client certificate, so that a stolen token is useless without the matching key. Its cost is the certificate lifecycle: every certificate expires, and an expiry is an outage unless someone has automated renewal and alerting.

## Keeping Secrets Out of Code

A secret that lives in source control, in a configuration file on a shared drive, or in a container image will eventually leak. The rules are simple to state and surprisingly rarely followed.

* **Keep secrets in a vault.** A secrets manager (HashiCorp Vault, AWS Secrets Manager, Azure Key Vault, Google Secret Manager) stores them encrypted, logs every access, and can rotate them. The integration fetches the secret at start-up using its own workload identity, not another secret.
* **Pass references, not values.** Configuration should say `secret_ref: vault:kv/integrations/orders`, resolved at start-up, or inject the value into the environment at launch.
* **Never log a secret.** Scrub tokens and passwords from logs, error messages, and traces, including debug output and exception text.
* **Use workload identity where possible.** Cloud platforms can give a running service an identity (a managed identity, an IAM role) so it can call the vault and other services without any stored credential at all.
* **Scan for leaks.** Run a secret scanner in the delivery pipeline and on the repository's history, because a secret committed once and deleted is still in history.

!!! warning "A demo configuration is not a production configuration"
    A configuration file with `"username": "svc-int"` and `"password": "Pssw0rd!"` is acceptable in a tutorial and unacceptable in production. When you receive an integration package or example that stores credentials in plain text, treat the file as a *template* and replace the values with references before it goes anywhere near a real environment.

## Service Accounts Done Properly

The identity the integration runs as deserves the same care as the code.

* **One identity per integration**, never a shared administrator. Audit trails then say which job did what, and a compromised credential can be revoked without stopping everything else.
* **Least privilege.** Grant only the permissions the flow needs. A read-only synchronization should hold read-only rights. Where a platform filters what an account can see, scope deliberately, and test with the integration's real permissions.
* **Exclude the account from your own change feed.** Bidirectional integrations filter out changes made by their own user to avoid echo loops (Chapter {{ref ch:time}}). This works only if the integration has a dedicated identity.
* **A rotation plan.** Document who rotates the secret, how often, and how the running job picks up the new value without a redeploy. Overlapping validity (two valid secrets at once) makes rotation safe.
* **A break-glass procedure.** What happens when the account is locked or its password expires on a Sunday? Who can restore it, and how is that action recorded?

## Verifying Webhooks

When the *source* calls you, the roles reverse: you must verify the caller. A webhook endpoint is a public door, and anyone can post to it. The standard defense is an HMAC signature: the sender computes a keyed hash of a timestamp and the request body using a secret you share, and sends it in a header. You recompute the hash and compare. A timestamp window rejects replays of captured requests.

{{code webhook.py}}

The `verify` function rejects a request whose timestamp is more than five minutes from now, which stops an attacker from replaying a captured message later. It uses `hmac.compare_digest` for a *constant-time* comparison, because an ordinary string comparison returns earlier when the first byte differs, leaking information about the correct signature to a patient attacker. And it never raises on malformed input; it simply returns `False`. The `Ledger` class addresses the other half of the problem, the sender's legitimate retries: it records each event ID and answers whether this is the first time. Signature schemes vary by vendor (what exactly is signed, how the header is formatted), so follow the vendor's documentation, but keep the structure: verify, reject stale, deduplicate.

## Authorization: What the Caller May Do

Authentication establishes identity; **authorization** decides what that identity may do, and most real breaches exploit authorization, not authentication. The relevant ideas for integrators are these.

**Scopes** limit what a token may be used for: `read:orders` but not `write:orders`. Request the narrowest scope that works. **Object-level authorization** checks that the caller may access *this particular record*, not merely the type of record; an API that returns any order when given its ID, regardless of whose it is, has a classic and serious flaw (Chapter {{ref ch:security}} covers it). **Permission filtering** means that an integration user may see only some of the data: fields hidden by role, records outside its tenant. This produces a subtle failure, where the integration reads *less* than the documentation promises, with no error. Always test with the integration's real permissions, and compare counts with what an administrator sees.

## Troubleshooting Authentication

Authentication failures follow a few patterns. {{ref tbl:authtrouble}} lists the most common, with likely causes and fixes.

{{tbl authtrouble | Authentication symptoms, causes, and fixes}}

| Symptom | Likely cause | Fix |
|---|---|---|
| 401 right after obtaining a token | Wrong audience or scope; a token for the wrong environment | Decode the token (a JWT is readable) and compare `aud`, `scope`, and `iss` |
| 401 after exactly N minutes | The token expired and nothing refreshed it | Refresh before expiry; retry once on 401 |
| 403 on some endpoints only | A missing scope or role | Compare the service account's role with the endpoint's documented permission |
| Works locally, 401 from the server | A corporate proxy rewrites headers; clock skew breaks a JWT assertion | Test with `curl` from the server; synchronize time with NTP |
| TLS handshake errors | Corporate TLS inspection with a private certificate authority | Add the authority to the runtime's trust store; never disable verification |
| Intermittent 401 with parallel workers | Each worker refreshes its own token, invalidating the others' | Share one token provider with a lock |

## Choosing a Scheme

When the vendor gives you a choice, a short decision procedure helps. For a *person*, use single sign-on with the authorization code flow and PKCE. For an unattended *job*, prefer OAuth 2.0 client credentials with short tokens and the secret in a vault; if that is unavailable, a JWT bearer grant or mutual TLS; then a scoped, rotated API key; and as a last resort, basic authentication over TLS with one service account and a vault. For an incoming *webhook*, an HMAC signature with a timestamp plus deduplication by event ID. Whatever you choose, record it in the reconnaissance sheet, and write down who approves the account, because that approval is often the longest wait of the whole project.

## Summary

Integrations authenticate as machine identities, and the design of that identity is half the security of the integration. Basic authentication and API keys are easy and weak; OAuth 2.0 client credentials is the default for service-to-service calls; JWT bearer grants and mutual TLS remove the shared secret at the cost of key and certificate management; authorization code with PKCE is for people, not jobs.

A correct token provider refreshes before expiry, holds a lock so parallel workers refresh once, and discards a rejected token exactly once. Secrets live in a vault and are passed by reference; each integration has its own least-privilege service account, a rotation plan, and a break-glass procedure. Incoming webhooks are verified by signature and timestamp with a constant-time comparison and deduplicated by event ID. And because breaches exploit authorization more often than authentication, test with the integration's real permissions and the narrowest scopes that work.

## Exercises

1. **Run the flow.** Start the lab server with authentication enabled (omit `--no-auth`), request a token with `curl`, and use it. Then restart the server and observe the 401. Which line of your client handles it?
2. **Audit a configuration.** Find a configuration file in your organization that stores a credential. Replace it with a reference, and describe how the running job would obtain the value.
3. **Break the webhook.** Using `webhook.py`, send a request with a valid signature but a timestamp one hour old, then one with a tampered body. Confirm both are rejected.
4. **Plan a rotation.** Write the steps to rotate an integration's client secret with zero downtime. Where does the overlap period appear?
