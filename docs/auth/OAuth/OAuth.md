----
url: https://oauth.net/2/
----

# OAuth 2.0

OAuth 2.0 is the industry-standard protocol for authorization. It prioritizes developer simplicity and offers specific authorization flows for different application types (web apps, desktop clients, mobile devices, IoT devices). Developed within the IETF OAuth Working Group. (OAuth 2.1 is an in-progress consolidation of accumulated best practice.)

## Core Framework (RFC 6749)

- **Access Tokens** — credentials for resource access.
- **Refresh Tokens** — used to obtain new access tokens.
- **Scope** — defines the boundaries of what's authorized.

## Grant Types

- **Authorization Code** — the standard web-application flow.
- **PKCE** — Proof Key for Code Exchange, hardens the authorization code flow for public clients (SPAs, mobile/native apps).
- **Client Credentials** — service-to-service (no end user).
- **Device Code** — for devices lacking a browser/keyboard (RFC 8628).
- **Refresh Token** — exchange a refresh token for a new access token.
- **Implicit Flow** — legacy, discouraged (token returned directly, no code exchange).
- **Password Grant** — legacy, discouraged (client collects the user's password directly).

## Related Specs Worth Knowing

- **Bearer Tokens** (RFC 6750) — how a token is presented on API calls (`Authorization: Bearer <token>`).
- **Token Introspection** (RFC 7662) / **Token Revocation** (RFC 7009).
- **JWT Access Token Profile** (RFC 9068) — using JWTs as OAuth access tokens.
- **Authorization Server Metadata** (RFC 8414) — `/.well-known/oauth-authorization-server` discovery document.
- **Dynamic Client Registration** (RFC 7591/7592).
- **PKCE** (RFC 7636), **Native Apps BCP** (RFC 8252), **Device Authorization Grant** (RFC 8628).
- **Security BCP** (RFC 9700) and threat model (RFC 6819) — current guidance discourages the Implicit and Password grants entirely in favor of Authorization Code + PKCE.

OAuth 2.0 is the authorization foundation underneath OpenID Connect (which adds identity/authentication — ID tokens, `/userinfo`), UMA 2.0, and IndieAuth.

----
url: https://www.rfc-editor.org/rfc/rfc6749
----

# RFC 6749: The OAuth 2.0 Authorization Framework

## Abstract

OAuth 2.0 enables third-party applications to obtain limited access to an HTTP service, either on behalf of a resource owner via an approval interaction, or by letting the third-party app access resources it controls itself. Replaces OAuth 1.0 (RFC 5849).

## 1. Introduction

Sharing raw credentials with third parties is problematic: apps must store passwords (often plaintext), servers must support weak password auth, access can't be scoped or selectively revoked, and any compromised app compromises the whole password. OAuth adds an authorization layer that separates the client's role from the resource owner's: instead of credentials, the client gets an **access token** — a string denoting a specific scope, lifetime, and other access attributes — issued by an authorization server with the resource owner's approval.

### 1.1 Roles

- **Resource Owner** — entity (often an end user) able to grant access to a protected resource.
- **Resource Server** — hosts protected resources, accepts/responds to requests using access tokens.
- **Client** — application making protected-resource requests on the resource owner's behalf and with their authorization.
- **Authorization Server** — issues access tokens after authenticating the resource owner and obtaining authorization.

### 1.2 Protocol Flow

```
     +--------+                               +---------------+
     |        |--(A)- Authorization Request ->|   Resource    |
     |        |                               |     Owner     |
     |        |<-(B)-- Authorization Grant ---|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(C)-- Authorization Grant -->| Authorization |
     | Client |                               |     Server    |
     |        |<-(D)----- Access Token -------|               |
     |        |                               +---------------+
     |        |
     |        |                               +---------------+
     |        |--(E)----- Access Token ------>|    Resource   |
     |        |                               |     Server    |
     |        |<-(F)--- Protected Resource ---|               |
     +--------+                               +---------------+
```

(A) client requests authorization from the resource owner (usually indirectly, via the authorization server) → (B) client receives an authorization grant → (C) client presents the grant to the authorization server → (D) server issues an access token → (E) client uses the token to call the resource server → (F) resource server returns the protected resource.

### 1.3 Authorization Grant Types

- **Authorization Code** — obtained via the authorization server as an intermediary; the client never sees the resource owner's credentials, and the token is transmitted directly to the client without going through the user-agent. Best for confidential (server-side) clients.
- **Implicit** — simplified flow for browser/JS clients; access token returned directly instead of a code, no client authentication, token exposed in the redirect URI. No refresh token issued. **Legacy/discouraged today** — use Authorization Code + PKCE instead even for SPAs.
- **Resource Owner Password Credentials** — client collects username/password directly and exchanges them once for a token; only for highly-trusted clients (e.g. the OS's own app) when nothing else is viable. **Legacy/discouraged.**
- **Client Credentials** — client authenticates as itself, no resource owner involved; for service-to-service access to resources the client controls.

### 1.4 Access Token

A string representing the authorization issued to the client; may be opaque or self-contained (e.g. a JWT). Same token format is understood by the resource server, decoupling it from whatever internal authorization constructs the server uses.

### 1.5 Refresh Token

A credential (only ever sent to the *authorization* server, never the resource server) used to obtain new access tokens when the current one expires or to get a narrower-scoped one, without involving the resource owner again. Issued alongside an access token at the authorization server's discretion.

```
  +--------+                                           +---------------+
  |        |--(A)------- Authorization Grant --------->|               |
  |        |<-(B)----------- Access Token -------------|               |
  |        |               & Refresh Token             |               |
  |        |                            +----------+   |               |
  |        |--(C)---- Access Token ---->|          |   |               |
  |        |<-(D)- Protected Resource --| Resource |   | Authorization |
  | Client |                            |  Server  |   |     Server    |
  |        |--(E)---- Access Token ---->|          |   |               |
  |        |<-(F)- Invalid Token Error -|          |   |               |
  |        |                            +----------+   |               |
  |        |--(G)----------- Refresh Token ----------->|               |
  |        |<-(H)----------- Access Token -------------|               |
  +--------+           & Optional Refresh Token        +---------------+
```

## 2. Client Registration & Types

- **Confidential** clients can keep credentials secret (e.g. server-side web apps).
- **Public** clients cannot (native apps, browser-based apps) — must rely on PKCE and short-lived tokens instead of a client secret.

Profiles: **Web Application** (confidential, credentials stay server-side), **User-Agent-Based Application** (public, code runs in the browser), **Native Application** (public, installed on the device).

## 3. Protocol Endpoints

- **Authorization Endpoint** — resource owner interacts here (via user-agent redirect) to grant/deny access. Must use TLS; the authorization server must first verify the resource owner's identity.
- **Token Endpoint** — client exchanges a grant (or refresh token) for an access token; MUST use HTTP POST; MUST use TLS.
- **Redirection Endpoint** (client-side) — where the authorization server sends the resource owner back with the grant/token.

**Scope**: space-delimited, case-sensitive strings (`scope = scope-token *( SP scope-token )`). Server may narrow the requested scope; if the granted scope differs from what was requested, the response MUST include `scope` to say so.

## 4. Obtaining Authorization

### 4.1 Authorization Code Grant

```
     +----------+
     | Resource |
     |   Owner  |
     +----------+
          ^
         (B)
     +----|-----+          Client Identifier      +---------------+
     |         -+----(A)-- & Redirection URI ---->|               |
     |  User-   |                                 | Authorization |
     |  Agent  -+----(B)-- User authenticates -->|     Server    |
     |          |                                 |               |
     |         -+----(C)-- Authorization Code ---<|               |
     +-|----|---+                                 +---------------+
       |    |                                         ^      v
      (A)  (C)                                        |      |
       v    v                                         |      |
     +---------+                                      |      |
     |         |>---(D)-- Authorization Code ---------'      |
     |  Client |          & Redirection URI                  |
     |         |<---(E)----- Access Token -------------------'
     +---------+       (w/ Optional Refresh Token)
```

**4.1.1 Authorization Request** (`GET` to the authorization endpoint, `application/x-www-form-urlencoded` query):

| Param | Required | Notes |
|---|---|---|
| `response_type` | REQUIRED | `"code"` |
| `client_id` | REQUIRED | |
| `redirect_uri` | OPTIONAL | must match a registered URI |
| `scope` | OPTIONAL | |
| `state` | RECOMMENDED | opaque anti-CSRF value, echoed back verbatim |

```
GET /authorize?response_type=code&client_id=s6BhdRkqt3&state=xyz
    &redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb HTTP/1.1
Host: server.example.com
```

**4.1.2 Authorization Response**: `code` (REQUIRED, short-lived — 10 minutes max recommended, bound to client_id + redirect_uri, single use) and `state` (echoed) appended to the redirect URI's query:

```
HTTP/1.1 302 Found
Location: https://client.example.com/cb?code=SplxlOBeZQQYbYS6WxSbIA&state=xyz
```

Error codes: `invalid_request`, `unauthorized_client`, `access_denied`, `unsupported_response_type`, `invalid_scope`, `server_error`, `temporarily_unavailable` (plus `error_description`, `error_uri`, `state`).

**4.1.3 Access Token Request** (`POST` to token endpoint):

| Param | Required |
|---|---|
| `grant_type` | REQUIRED — `"authorization_code"` |
| `code` | REQUIRED |
| `redirect_uri` | REQUIRED if it was in the authorization request — must match exactly |
| `client_id` | REQUIRED if the client isn't otherwise authenticating |

```
POST /token HTTP/1.1
Host: server.example.com
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code&code=SplxlOBeZQQYbYS6WxSbIA
&redirect_uri=https%3A%2F%2Fclient%2Eexample%2Ecom%2Fcb
```

**4.1.4 Access Token Response**:

```
HTTP/1.1 200 OK
Content-Type: application/json;charset=UTF-8
Cache-Control: no-store
Pragma: no-cache

{
  "access_token":"2YotnFZFEjr1zCsicMWpAA",
  "token_type":"example",
  "expires_in":3600,
  "refresh_token":"tGzv3JOkF0XG5Qx2TlKWIA",
  "example_parameter":"example_value"
}
```

### 4.2 Implicit Grant

No client authentication; token returned straight in the redirect URI fragment (never sent through the server, only via the user-agent). No refresh token is ever issued.

```
response_type=token   → access_token in the fragment, e.g.:
HTTP/1.1 302 Found
Location: http://example.com/cb#access_token=2YotnFZFEjr1zCsicMWpAA
          &state=xyz&token_type=example&expires_in=3600
```

### 4.3 Resource Owner Password Credentials Grant

```
grant_type=password&username=johndoe&password=A3ddj3w
```

Client must discard the password immediately after exchanging it for a token. Authorization server MUST rate-limit / guard this endpoint against brute force.

### 4.4 Client Credentials Grant

Confidential clients only:

```
POST /token HTTP/1.1
Host: server.example.com
Authorization: Basic czZCaGRSa3F0MzpnWDFmQmF0M2JW
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
```

No refresh token (a new client-credentials request just gets a new token directly).

## 5. Issuing an Access Token

Success response fields: `access_token` (REQUIRED), `token_type` (REQUIRED, e.g. `Bearer`), `expires_in` (RECOMMENDED, seconds), `refresh_token` (OPTIONAL), `scope` (present if it differs from what was requested).

## 6. Refreshing an Access Token

```
grant_type=refresh_token&refresh_token=tGzv3JOkF0XG5Qx2TlKWIA
```

Optional `scope` — must not exceed the originally granted scope.

## 7. Accessing Protected Resources

`token_type` tells the client how to use the token (e.g. `Bearer`, RFC 6750: `Authorization: Bearer <token>`). If a request fails due to a missing/expired/invalid/insufficient token, the resource server responds with `WWW-Authenticate: Bearer ...` and an appropriate 4xx status.

