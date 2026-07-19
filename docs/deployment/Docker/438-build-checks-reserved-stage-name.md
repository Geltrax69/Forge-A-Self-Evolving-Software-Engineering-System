url: https://docs.docker.com/reference/build-checks/reserved-stage-name/
----

# ReservedStageName

***

Table of contents

***

## [Output](#output)

```text
'scratch' is reserved and should not be used as a stage name
```

## [Description](#description)

Reserved words should not be used as names for stages in multi-stage builds. The reserved words are:

* `context`
* `scratch`

## [Examples](#examples)

❌ Bad: `scratch` and `context` are reserved names.

```dockerfile
FROM alpine AS scratch
FROM alpine AS context
```

✅ Good: the stage name `builder` is not reserved.

```dockerfile
FROM alpine AS builder
```

----
