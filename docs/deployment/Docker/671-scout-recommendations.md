url: https://docs.docker.com/reference/cli/docker/scout/recommendations/
----

# docker scout recommendations

***

| Description | Display available base image updates and remediation recommendations |
| ----------- | -------------------------------------------------------------------- |
| Usage       | `docker scout recommendations [IMAGE\|DIRECTORY\|ARCHIVE]`           |

## [Description](#description)

The `docker scout recommendations` command display recommendations for base images updates. It analyzes the image and display recommendations to refresh or update the base image. For each recommendation it shows a list of benefits, such as fewer vulnerabilities or smaller image size.

| Option           | Default | Description                                                                                          |
| ---------------- | ------- | ---------------------------------------------------------------------------------------------------- |
| `--only-refresh` |         | Only display base image refresh recommendations                                                      |
| `--only-update`  |         | Only display base image update recommendations                                                       |
| `--org`          |         | Namespace of the Docker organization                                                                 |
| `-o, --output`   |         | Write the report to a file                                                                           |
| `--platform`     |         | Platform of image to analyze                                                                         |
| `--ref`          |         | Reference to use if the provided tarball contains multiple references. Can only be used with archive |
| `--tag`          |         | Specify tag                                                                                          |

## [Examples](#examples)

### [Display base image update recommendations](#display-base-image-update-recommendations)

```console
$ docker scout recommendations golang:1.19.4
```

### [Display base image refresh only recommendations](#display-base-image-refresh-only-recommendations)

```console
$ docker scout recommendations --only-refresh golang:1.19.4
```

### [Display base image update only recommendations](#display-base-image-update-only-recommendations)

```console
$ docker scout recommendations --only-update golang:1.19.4
```

----
