url: https://docs.docker.com/reference/build-checks/redundant-target-platform/
----

# RedundantTargetPlatform

***

Table of contents

***

## [Output](#output)

```text
Setting platform to predefined $TARGETPLATFORM in FROM is redundant as this is the default behavior
```

## [Description](#description)

A custom platform can be used for a base image. The default platform is the same platform as the target output so setting the platform to `$TARGETPLATFORM` is redundant and unnecessary.

## [Examples](#examples)

❌ Bad: this usage of `--platform` is redundant since `$TARGETPLATFORM` is the default.

```dockerfile
FROM --platform=$TARGETPLATFORM alpine AS builder
RUN apk add --no-cache git
```

✅ Good: omit the `--platform` argument.

```dockerfile
FROM alpine AS builder
RUN apk add --no-cache git
```

----
