url: https://docs.docker.com/reference/cli/docker/scout/attestation/add/
----

# docker scout attestation add

***

| Description                                                               | Add attestation to image                                |
| ------------------------------------------------------------------------- | ------------------------------------------------------- |
| Usage                                                                     | `docker scout attestation add OPTIONS IMAGE [IMAGE...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker scout attest add`                               |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

The docker scout attestation add command adds attestations to images.

## [Options](#options)

| Option                  | Default                     | Description                                  |
| ----------------------- | --------------------------- | -------------------------------------------- |
| `--file`                |                             | File location of attestations to attach      |
| `--org`                 |                             | Namespace of the Docker organization         |
| `--predicate-type`      |                             | Predicate-type for attestations              |
| `--referrer`            |                             | Use OCI referrer API for pushing attestation |
| `--referrer-repository` | `registry.scout.docker.com` | Repository to push referrer to               |

----
