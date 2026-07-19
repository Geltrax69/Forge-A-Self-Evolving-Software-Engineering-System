url: https://nginx.org/en/docs/beginners_guide.html
----

# Beginner's Guide

## Starting, Stopping, and Reloading Configuration

```
nginx -s signal
```

`signal` is one of: `stop` (fast shutdown), `quit` (graceful shutdown), `reload` (reload config), `reopen` (reopen log files). Run under the same user that started nginx.

```
nginx -s quit
nginx -s reload
```

On reload, the master process validates the new config's syntax first; if valid, it starts new workers and asks old ones to finish in-flight requests then exit; if invalid, it rolls back and keeps running the old config.

You can also signal by PID (found in `nginx.pid`, typically under `/usr/local/nginx/logs` or `/var/run`):

```
kill -s QUIT 1628
ps -ax | grep nginx
```

## Configuration File's Structure

Directives are simple (`name params;`) or block (`name params { ... }`). A block directive that can itself hold other directives is called a *context* — e.g. `events`, `http`, `server`, `location`. Directives outside any context are in the `main` context. `#` starts a comment.

## Serving Static Content

```
http {
    server {
        location / {
            root /data/www;
        }

        location /images/ {
            root /data;
        }
    }
}
```

nginx picks the request's `server` block by listen address/port and `Host` header, then matches the URI against that server's `location` blocks — appending the URI to the matching `location`'s `root` to find the file. Among prefix matches, the **longest matching prefix wins**. `/images/1.gif` → `/data/images/1.gif`; anything else → under `/data/www`. Apply changes with `nginx -s reload`; check `access.log`/`error.log` (typically `/usr/local/nginx/logs` or `/var/log/nginx`) if something's off.

## Setting Up a Simple Proxy Server

Upstream/backend server:

```
server {
    listen 8080;
    root /data/up1;

    location / {
    }
}
```

Proxy in front of it, with a regex location carved out for images served locally:

```
server {
    location / {
        proxy_pass http://localhost:8080/;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
```

Regex locations are prefixed with `~` (case-sensitive) or `~*` (case-insensitive). Selection order: nginx first finds the longest-matching *prefix* location, then checks regex locations in configuration order and uses the first one that matches; if none match, it falls back to the remembered prefix location.

## Setting Up FastCGI Proxying

```
server {
    location / {
        fastcgi_pass  localhost:9000;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param QUERY_STRING    $query_string;
    }

    location ~ \.(gif|jpg|png)$ {
        root /data/images;
    }
}
```

Use `fastcgi_pass` (+ `fastcgi_param`) instead of `proxy_pass` to talk to a FastCGI app server (e.g. PHP-FPM) over the FastCGI protocol.

----
