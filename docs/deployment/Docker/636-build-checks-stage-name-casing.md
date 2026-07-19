url: https://docs.docker.com/reference/build-checks/stage-name-casing/
----

# StageNameCasing

***

Table of contents

***

## [Output](#output)

```text
Stage name 'BuilderBase' should be lowercase
```

## [Description](#description)

To help distinguish Dockerfile instruction keywords from identifiers, this rule forces names of stages in a multi-stage Dockerfile to be all lowercase.

## [Examples](#examples)

❌ Bad: mixing uppercase and lowercase characters in the stage name.

```dockerfile
FROM alpine AS BuilderBase
```

✅ Good: stage name is all in lowercase.

```dockerfile
FROM alpine AS builder-base
```

----
