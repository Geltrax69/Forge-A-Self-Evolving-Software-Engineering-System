url: https://docs.docker.com/reference/cli/docker/scout/sbom/
----

# docker scout sbom

***

| Description | Generate or display SBOM of an image            |
| ----------- | ----------------------------------------------- |
| Usage       | `docker scout sbom [IMAGE\|DIRECTORY\|ARCHIVE]` |

## [Description](#description)

The `docker scout sbom` command analyzes a software artifact to generate a Software Bill Of Materials (SBOM).

The SBOM contains a list of all packages in the image. You can use the `--format` flag to filter the output of the command to display only packages of a specific type.

| Option                | Default | Description                                                                                                                                                                             |
| --------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--format`            | `json`  | Output format: - list: list of packages of the image - json: json representation of the SBOM - spdx: spdx representation of the SBOM - cyclonedx: cyclone dx representation of the SBOM |
| `--only-package-type` |         | Comma separated list of package types (like apk, deb, rpm, npm, pypi, golang, etc) Can only be used with --format list                                                                  |
| `-o, --output`        |         | Write the report to a file                                                                                                                                                              |
| `--platform`          |         | Platform of image to analyze                                                                                                                                                            |
| `--ref`               |         | Reference to use if the provided tarball contains multiple references. Can only be used with archive                                                                                    |

## [Examples](#examples)

### [Display the list of packages](#display-the-list-of-packages)

```console
$ docker scout sbom --format list alpine
```

### [Only display packages of a specific type](#only-display-packages-of-a-specific-type)

```console
 $ docker scout sbom --format list --only-package-type apk alpine
```

### [Display the full SBOM in JSON format](#display-the-full-sbom-in-json-format)

```console
$ docker scout sbom alpine
```

### [Display the full SBOM of the most recently built image](#display-the-full-sbom-of-the-most-recently-built-image)

```console
$ docker scout sbom
```

### [Write SBOM to a file](#write-sbom-to-a-file)

```console
$ docker scout sbom --output alpine.sbom alpine
```

----
