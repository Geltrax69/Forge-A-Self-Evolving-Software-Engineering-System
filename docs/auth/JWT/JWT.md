----
url: https://jwt.io/introduction
----

# Introduction to JSON Web Tokens

## What is JSON Web Token?

JSON Web Token (JWT) is an open standard (RFC 7519) establishing a compact and self-contained way for securely transmitting information between parties as a JSON object. This information gains trustworthiness through digital signatures.

Token signing occurs via two mechanisms: the HMAC algorithm with a shared secret, or RSA/ECDSA using public/private key pairs. While encryption capability exists for secrecy, signed tokens verify claim integrity without necessarily hiding content from third parties.

## When should you use JSON Web Tokens?

**Authorization**: After user login, subsequent requests include the JWT, granting access to permitted routes, services, and resources. Single Sign-On implementations frequently leverage JWTs due to minimal overhead and cross-domain compatibility.

**Information Exchange**: JWTs facilitate secure party-to-party information transmission. Signed tokens using public/private key pairs confirm sender identity, while the signature (calculated over header + payload) enables content-tampering detection.

## What is the JSON Web Token structure?

A JWT consists of three dot-separated, Base64Url-encoded components: Header, Payload, and Signature:

```
xxxxx.yyyyy.zzzzz
```

### Header

Token type and signing algorithm:

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

Contains claims — statements about an entity plus supplementary data:

- **Registered claims**: predefined, optional but recommended, for interoperability — `iss` (issuer), `exp` (expiration time), `sub` (subject), `aud` (audience), etc. Kept to three characters to stay compact.
- **Public claims**: custom claims that should be registered in the IANA JSON Web Token Registry, or be collision-resistant URIs.
- **Private claims**: custom claims agreed between the parties, neither registered nor public.

```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "admin": true
}
```

**Important**: signed tokens (the common case) are readable by anyone — the signature only protects integrity, not confidentiality. Never put secrets in the payload/header unless you also encrypt the token (JWE).

### Signature

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

Verifies the token wasn't altered and, for private-key-signed tokens, confirms sender identity.

## How do JSON Web Tokens work?

After successful login, the authorization server returns a JWT. Minimize how long the token is stored, and avoid storing sensitive session data client-side.

The client sends the JWT in the `Authorization` header using the Bearer scheme:

```
Authorization: Bearer <token>
```

Protected routes validate the JWT from that header and grant access if valid — carrying the needed data inside the token can reduce database lookups, though not universally.

**Header size**: some servers reject headers over 8 KB — don't cram large claim sets (e.g. all user permissions) into the token.

**CORS**: using an `Authorization` header (rather than cookies) sidesteps CORS credential-transmission issues.

### Typical flow

1. The application requests authorization from the authorization server (e.g. via an authorization-code flow).
2. On grant, the server returns an access token (a JWT) to the application.
3. The application uses that token to call protected resources (APIs).

**Reminder**: signed tokens still expose all their claims to anyone holding the token — never put secrets inside them.

----
url: https://www.rfc-editor.org/rfc/rfc7519
----

# RFC 7519: JSON Web Token (JWT)

## Abstract

JSON Web Token (JWT) is a compact, URL-safe means of representing claims to be transferred between two parties. The claims in a JWT are encoded as a JSON object used as the payload of a JSON Web Signature (JWS) structure or as the plaintext of a JSON Web Encryption (JWE) structure, enabling the claims to be digitally signed, MACed, and/or encrypted.

## 1. Introduction

JWT is a compact claims representation format intended for space-constrained environments such as HTTP Authorization headers and URI query parameters. JWTs are always represented using either JWS Compact Serialization or JWE Compact Serialization. (Suggested pronunciation: "jot".)

## 2. Terminology

- **JSON Web Token (JWT)**: a string representing a set of claims as a JSON object encoded in a JWS or JWE.
- **JWT Claims Set**: the JSON object containing the claims.
- **Claim / Claim Name / Claim Value**: a name/value pair asserting information about a subject.
- **Nested JWT**: a JWT used as the payload/plaintext of an enclosing JWS/JWE (nested signing and/or encryption).
- **Unsecured JWT**: a JWT whose claims are not integrity-protected or encrypted.
- **Collision-Resistant Name**: a name unlikely to collide with others (e.g. a domain name, OID, or UUID).
- **StringOrURI**: a JSON string; any value containing `:` MUST be a URI. Compared as case-sensitive strings with no normalization.
- **NumericDate**: seconds since 1970-01-01T00:00:00Z UTC, ignoring leap seconds.

## 3. JWT Overview

A JWT is a sequence of URL-safe parts separated by `.`, each a base64url-encoded value. The number of parts depends on JWS vs JWE compact serialization.

### 3.1 Example JWT

JOSE Header (HMAC SHA-256):

```json
{"typ":"JWT","alg":"HS256"}
```

Claims Set:

```json
{"iss":"joe","exp":1300819380,"http://example.com/is_root":true}
```

Complete JWT (line breaks for display only):

```
eyJ0eXAiOiJKV1QiLA0KICJhbGciOiJIUzI1NiJ9
.
eyJpc3MiOiJqb2UiLA0KICJleHAiOjEzMDA4MTkzODAsDQogImh0dHA6Ly9leGFt
cGxlLmNvbS9pc19yb290Ijp0cnVlfQ
.
dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
```

## 4. JWT Claims

Claim Names within a Claims Set MUST be unique; parsers MUST reject duplicates or use only the lexically-last one. Any claim not understood by an implementation MUST be ignored (absent app-specific requirements). Three classes:

### 4.1 Registered Claim Names

None are mandatory to use — they're a starting point for interoperable claims:

- **`iss` (Issuer)** — OPTIONAL, case-sensitive `StringOrURI` identifying who issued the JWT.
- **`sub` (Subject)** — OPTIONAL, `StringOrURI`, identifies the principal the claims are about; must be locally or globally unique in the issuer's context.
- **`aud` (Audience)** — OPTIONAL. Array of case-sensitive `StringOrURI` values (or a single string if there's only one audience). Each intended recipient MUST match one of these; otherwise the JWT MUST be rejected.
- **`exp` (Expiration Time)** — OPTIONAL, `NumericDate`. Current time MUST be before `exp`; small clock-skew leeway (a few minutes) is allowed.
- **`nbf` (Not Before)** — OPTIONAL, `NumericDate`. Current time MUST be at/after `nbf`.
- **`iat` (Issued At)** — OPTIONAL, `NumericDate`. Used to determine token age.
- **`jti` (JWT ID)** — OPTIONAL, case-sensitive string. A unique identifier with negligible collision probability; useful for preventing replay.

### 4.2 Public Claim Names

Definable at will; to avoid collisions, register in the IANA "JSON Web Token Claims" registry or use a Collision-Resistant (URI-style) name.

### 4.3 Private Claim Names

Names agreed between producer and consumer that are neither registered nor public — use with caution, they're subject to collision.

## 5. JOSE Header

Describes the cryptographic operations applied. Applies to both JWS- and JWE-based JWTs.

- **`typ` (Type)** — OPTIONAL. If present, RECOMMENDED value `"JWT"`. Ignored by JWT implementations themselves; used by the surrounding application to disambiguate object kinds. Typically omitted once it's already known the object is a JWT.
- **`cty` (Content Type)** — NOT RECOMMENDED for ordinary (non-nested) JWTs. MUST be present and equal to `"JWT"` when nested signing/encryption is used, signaling a Nested JWT.
- **Replicating claims as Header Parameters** — for JWEs, some claims may be duplicated unencrypted in the header so an app can decide how to process the token before decrypting it. If replicated, the receiving app SHOULD verify the header and payload copies match. Only claims safe to expose unencrypted should be replicated this way.

