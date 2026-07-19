url: https://nginx.org/en/docs/http/ngx_http_core_module.html
----

# Module ngx_http_core_module (selected directives and variables)

### server

```
server { ... }
```
Context: `http`. Configuration for a virtual server; `listen` decides which addresses/ports it accepts on, `server_name` which hostnames it matches.

### listen

```
listen address[:port] [default_server] [ssl] [http2 | quic] [proxy_protocol] [backlog=number] [reuseport] [so_keepalive=on|off|...] ...;
listen port [default_server] ...;
listen unix:path ...;
```
Default: `listen *:80 | *:8000;` — Context: `server`.

Examples:
```
listen 127.0.0.1:8000;
listen [::]:8000;
listen unix:/var/run/nginx.sock;
```
`default_server` makes this the default virtual server for the address:port pair. `ssl` marks the port as always-TLS. `reuseport` gives each worker its own listening socket (kernel load-balances accepts across workers, Linux 3.9+/FreeBSD 12+). `backlog` sets the pending-connection queue length (default 511, or -1 on BSD/macOS).

### server_name

```
server_name name ...;
```
Default: `server_name "";` — Context: `server`.

```
server {
    server_name example.com www.example.com;
}
server {
    server_name example.com *.example.com www.example.*;   # wildcards
}
server {
    server_name .example.com;                               # combines example.com + *.example.com
}
server {
    server_name ~^(www\.)?(?<domain>.+)$;                   # regex with named capture
    location / { root /sites/$domain; }
}
```

**Selection priority**: (1) exact name, (2) longest wildcard starting with `*`, (3) longest wildcard ending with `*`, (4) first matching regex in file order.

### location

```
location [ = | ~ | ~* | ^~ ] uri { ... }
location @name { ... }
```
Context: `server`, `location`.

Matching: nginx finds the prefix location with the longest matching prefix, remembers it, then checks regex locations (`~` case-sensitive, `~*` case-insensitive) in file order and uses the first regex match; otherwise it falls back to the remembered prefix location. `^~` on a prefix location means: if it's the longest-matching prefix, skip regex checking entirely. `=` requires an exact URI match and, if found, stops the search immediately (fastest option for hot exact-match paths like `/`).

```
location = / {          # configuration A — exact match for "/"
}
location / {            # configuration B — catch-all prefix
}
location /documents/ {  # configuration C
}
location ^~ /images/ {  # configuration D — prefix match, skips regex checking
}
location ~* \.(gif|jpg|jpeg)$ {  # configuration E — case-insensitive regex
}
```
`/` → A, `/index.html` → B, `/documents/document.html` → C, `/images/1.gif` → D, `/documents/1.jpg` → E.

`@name` defines a **named location**, used only for internal redirection (e.g. from `error_page`, `try_files`), never matched directly by client requests, and can't be nested.

If a prefix location ends in `/` and is proxied (`proxy_pass`, `fastcgi_pass`, etc.), a request for the same URI *without* the trailing slash gets a 301 redirect to the slash-suffixed URI — define an exact-match location to opt out:
```
location /user/ { proxy_pass http://user.example.com; }
location = /user { proxy_pass http://login.example.com; }
```

### root / alias

```
root path;      # http, server, location, if-in-location — default: root html;
alias path;     # location only
```
`root` appends the URI to the path (`location /i/ { root /data/w3; }` → `/i/top.gif` serves `/data/w3/i/top.gif`). `alias` *replaces* the location prefix instead of appending (`location /i/ { alias /data/w3/images/; }` → `/i/top.gif` serves `/data/w3/images/top.gif`). Inside a regex location, `alias` must reference regex captures:
```
location ~ ^/users/(.+\.(?:gif|jpe?g|png))$ {
    alias /data/w3/images/$1;
}
```

### try_files

```
try_files file ... uri;
try_files file ... =code;
```
Context: `server`, `location`. Tries each file candidate in order (paths built via `root`/`alias`); a trailing `/` checks for a directory. Falls back to an internal redirect to the final `uri` (or named location, or a literal status code) if none exist.

```
location / {
    try_files $uri $uri/index.html $uri.html =404;
}
```
Classic PHP-app pattern:
```
location / {
    try_files $uri $uri/ @drupal;
}
location ~ \.php$ {
    try_files $uri @drupal;
    fastcgi_pass ...;
    fastcgi_param SCRIPT_FILENAME /path/to$fastcgi_script_name;
}
location @drupal {
    fastcgi_pass ...;
    fastcgi_param SCRIPT_FILENAME /path/to/index.php;
    fastcgi_param QUERY_STRING q=$uri&$args;
}
```

### error_page

```
error_page code ... [=[response]] uri;
```
Context: `http`, `server`, `location`, `if-in-location`.

```
error_page 404             /404.html;
error_page 500 502 503 504 /50x.html;
error_page 404 =200 /empty.gif;         # rewrite the status code too
error_page 404 = /404.php;              # "=" with no code: pass through whatever the backend returned
error_page 403      http://example.com/forbidden.html;   # external redirect (302 by default)
error_page 404 =301 http://example.com/notfound.html;
```
Can target a named location for backend fallback:
```
location / { error_page 404 = @fallback; }
location @fallback { proxy_pass http://backend; }
```
Inherited from the parent context only if the current level defines no `error_page` at all.

### client_max_body_size

```
client_max_body_size size;   # default 1m — http, server, location
```
Requests with a body over this size get `413 Request Entity Too Large`. `0` disables the check.

### keepalive_timeout

```
keepalive_timeout timeout [header_timeout];   # default 75s — http, server, location
```
How long a keep-alive client connection stays open server-side; `0` disables keep-alive. The optional second value sets the `Keep-Alive: timeout=` response header (recognized by some browsers).

## Useful Embedded Variables

`$uri` (normalized current URI, may change across internal redirects), `$request_uri` (raw original URI+args), `$args`/`$query_string`, `$arg_name` (one query arg), `$http_name` (a request header, e.g. `$http_user_agent`), `$sent_http_name` (a response header), `$cookie_name`, `$host`, `$scheme`, `$request_method`, `$remote_addr`/`$remote_port`, `$server_addr`/`$server_name`/`$server_port`, `$status`, `$request_time`, `$request_length`, `$body_bytes_sent`/`$bytes_sent`, `$document_root`, `$request_body`/`$request_body_file`, `$ssl_...`/`$https`, `$proxy_protocol_addr`, `$time_local`/`$time_iso8601`.

----
