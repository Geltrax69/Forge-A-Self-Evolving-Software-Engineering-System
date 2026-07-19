url: https://docs.docker.com/reference/cli/sbx/policy/allow/network/
----

# sbx policy allow network

| Description | Allow network access to specified hosts                          |
| ----------- | ---------------------------------------------------------------- |
| Usage       | `sbx policy allow network [--sandbox SANDBOX] RESOURCES [flags]` |

## [Description](#description)

Allow sandbox network access to the specified hosts.

RESOURCES is a comma-separated list of hostnames, domains, or IP addresses. Supports exact domains (example.com), wildcard subdomains (\*.example.com), and optional port suffixes (example.com:443). Use "\*\*" to allow all hosts.

The rule applies globally to all sandboxes by default. Use --sandbox to add the rule to policy "local" scoped to a single sandbox instead.

## [Options](#options)

| Option      | Default | Description                                                   |
| ----------- | ------- | ------------------------------------------------------------- |
| `--sandbox` |         | Scope the rule to a specific sandbox (default: all sandboxes) |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Allow access to a single host (all sandboxes)
sbx policy allow network api.example.com

# Allow access to multiple hosts
sbx policy allow network "api.example.com,cdn.example.com"

# Allow a host only for a specific sandbox
sbx policy allow network --sandbox my-sandbox api.example.com

# Allow all subdomains of a host
sbx policy allow network "*.npmjs.org"

# Allow all outbound traffic
sbx policy allow network "**"
```

----
