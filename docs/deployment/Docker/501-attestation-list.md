url: https://docs.docker.com/reference/cli/docker/scout/attestation/list/
----

# docker scout attestation list

***

| Description                                                               | List attestations for image                   |
| ------------------------------------------------------------------------- | --------------------------------------------- |
| Usage                                                                     | `docker scout attestation list OPTIONS IMAGE` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker scout attest list`                    |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

The docker scout attestation list command lists attestations for images.

## [Options](#options)

| Option             | Default | Description                                                                                                                   |
| ------------------ | ------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `--format`         | `list`  | Output format: - list: list of attestations of the image - json: json representation of the attestation list (default "json") |
| `--org`            |         | Namespace of the Docker organization                                                                                          |
| `-o, --output`     |         | Write the report to a file                                                                                                    |
| `--platform`       |         | Platform of image to analyze                                                                                                  |
| `--predicate-type` |         | Predicate-type for attestations                                                                                               |
| `--ref`            |         | Reference to use if the provided tarball contains multiple references. Can only be used with archive                          |

----
