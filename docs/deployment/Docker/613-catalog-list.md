url: https://docs.docker.com/reference/cli/docker/dhi/catalog/list/
----

# docker dhi catalog list

***

| Description | List available Docker Hardened Images |
| ----------- | ------------------------------------- |
| Usage       | `docker dhi catalog list`             |

## [Description](#description)

List all available Docker Hardened Images and Helm charts in the catalog

## [Options](#options)

| Option         | Default | Description                                                   |
| -------------- | ------- | ------------------------------------------------------------- |
| `-f, --filter` |         | Filter by name (case-insensitive substring match)             |
| `--fips`       |         | Filter to FIPS compliant images (use --fips=false to exclude) |
| `--json`       |         | Output in JSON format                                         |
| `--stig`       |         | Filter to STIG certified images (use --stig=false to exclude) |
| `--type`       |         | Filter by type (image, helm, chart, or helm-chart)            |

----
