url: https://docs.docker.com/reference/cli/docker/pass/rm/
----

# docker pass rm

***

| Description | Remove secrets from local keychain.      |
| ----------- | ---------------------------------------- |
| Usage       | `docker pass rm name1 name2 ... [flags]` |

## [Description](#description)

Removes one or more named secrets from the local OS keychain. Use `--all` to remove every stored secret at once.

## [Options](#options)

| Option  | Default | Description        |
| ------- | ------- | ------------------ |
| `--all` |         | Remove all secrets |

## [Examples](#examples)

### [Remove a specific secret:](#remove-a-specific-secret)

```console
$ docker pass rm GH_TOKEN
```

### [Remove multiple secrets:](#remove-multiple-secrets)

```console
$ docker pass rm GH_TOKEN NPM_TOKEN
```

### [Remove all secrets:](#remove-all-secrets)

```console
$ docker pass rm --all
```

----
