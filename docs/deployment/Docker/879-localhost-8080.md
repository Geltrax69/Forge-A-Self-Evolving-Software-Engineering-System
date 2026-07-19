        url: http://localhost:8080
        name: specialist
        remote:
          headers:
            Authorization: Bearer token123
            X-Custom-Header: value
```

## [What's next](#whats-next)

* Review the [CLI reference](https://docs.docker.com/ai/docker-agent/reference/cli/#a2a) for all `docker agent serve a2a` options
* Learn about [MCP mode](https://docs.docker.com/ai/docker-agent/integrations/mcp/) to expose agents as tools in MCP clients
* Learn about [ACP mode](https://docs.docker.com/ai/docker-agent/integrations/acp/) for editor integration
* Share your agents with [OCI registries](https://docs.docker.com/ai/docker-agent/sharing-agents/)

----
url: https://docs.docker.com/reference/cli/docker/dhi/attestation/
----

# docker dhi attestation

***

| Description                                                               | View attestations for Docker Hardened Images |
| ------------------------------------------------------------------------- | -------------------------------------------- |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker dhi attest` `docker dhi a`           |

## [Description](#description)

Commands to list and inspect attestations attached to Docker Hardened Images

## [Options](#options)

| Option  | Default | Description                                |
| ------- | ------- | ------------------------------------------ |
| `--org` |         | Docker Hub organization (overrides config) |

## [Subcommands](#subcommands)

| Command                                                                                             | Description                                       |
| --------------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [`docker dhi attestation get`](https://docs.docker.com/reference/cli/docker/dhi/attestation/get/)   | Get attestation for a Docker Hardened Image       |
| [`docker dhi attestation list`](https://docs.docker.com/reference/cli/docker/dhi/attestation/list/) | List attestations for a Docker Hardened Image     |
| [`docker dhi attestation sbom`](https://docs.docker.com/reference/cli/docker/dhi/attestation/sbom/) | Display the SPDX SBOM for a Docker Hardened Image |

----
url: https://docs.docker.com/reference/cli/docker/mcp/profile/remove/
----

# docker mcp profile remove

***

| Description                                                               | Remove a profile                         |
| ------------------------------------------------------------------------- | ---------------------------------------- |
| Usage                                                                     | `docker mcp profile remove <profile-id>` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp profile rm`                  |

## [Description](#description)

Remove a profile

----
url: https://docs.docker.com/reference/cli/docker/node/inspect/
----

# docker node inspect

***

| Description | Display detailed information on one or more nodes    |
| ----------- | ---------------------------------------------------- |
| Usage       | `docker node inspect [OPTIONS] self\|NODE [NODE...]` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Returns information about a node. By default, this command renders all results in a JSON array. You can specify an alternate format to execute a given template for each result. Go's [text/template](https://pkg.go.dev/text/template) package describes all the details of the format.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                    | Default | Description                                                                                                                                                                                                                             |
| ------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-f, --format`](#format) |         | Format output using a custom template: 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `--pretty`                |         | Print the information in a human friendly format                                                                                                                                                                                        |

## [Examples](#examples)

### [Inspect a node](#inspect-a-node)

```console
$ docker node inspect swarm-manager
```

```json
[
  {
    "ID": "e216jshn25ckzbvmwlnh5jr3g",
    "Version": {
      "Index": 10
    },
    "CreatedAt": "2017-05-16T22:52:44.9910662Z",
    "UpdatedAt": "2017-05-16T22:52:45.230878043Z",
    "Spec": {
      "Role": "manager",
      "Availability": "active"
    },
    "Description": {
      "Hostname": "swarm-manager",
      "Platform": {
        "Architecture": "x86_64",
        "OS": "linux"
      },
      "Resources": {
        "NanoCPUs": 1000000000,
        "MemoryBytes": 1039843328
      },
      "Engine": {
        "EngineVersion": "17.06.0-ce",
        "Plugins": [
          {
            "Type": "Volume",
            "Name": "local"
          },
          {
            "Type": "Network",
            "Name": "overlay"
          },
          {
            "Type": "Network",
            "Name": "null"
          },
          {
            "Type": "Network",
            "Name": "host"
          },
          {
            "Type": "Network",
            "Name": "bridge"
          },
          {
            "Type": "Network",
            "Name": "overlay"
          }
        ]
      },
      "TLSInfo": {
        "TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBazCCARCgAwIBAgIUOzgqU4tA2q5Yv1HnkzhSIwGyIBswCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNTAyMDAyNDAwWhcNMzcwNDI3MDAy\nNDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABMbiAmET+HZyve35ujrnL2kOLBEQhFDZ5MhxAuYs96n796sFlfxTxC1lM/2g\nAh8DI34pm3JmHgZxeBPKUURJHKWjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBS3sjTJOcXdkls6WSY2rTx1KIJueTAKBggqhkjO\nPQQDAgNJADBGAiEAoeVWkaXgSUAucQmZ3Yhmx22N/cq1EPBgYHOBZmHt0NkCIQC3\nzONcJ/+WA21OXtb+vcijpUOXtNjyHfcox0N8wsLDqQ==\n-----END CERTIFICATE-----\n",
        "CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
        "CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAExuICYRP4dnK97fm6OucvaQ4sERCEUNnkyHEC5iz3qfv3qwWV/FPELWUz/aACHwMjfimbcmYeBnF4E8pRREkcpQ=="
      }
    },
    "Status": {
      "State": "ready",
      "Addr": "168.0.32.137"
    },
    "ManagerStatus": {
      "Leader": true,
      "Reachability": "reachable",
      "Addr": "168.0.32.137:2377"
    }
  }
]
```

### [Format the output (--format)](#format)

```console
$ docker node inspect --format '{{ .ManagerStatus.Leader }}' self

false
```

Use `--format=pretty` or the `--pretty` shorthand to pretty-print the output:

```console
$ docker node inspect --format=pretty self

ID:                     e216jshn25ckzbvmwlnh5jr3g
Hostname:               swarm-manager
Joined at:              2017-05-16 22:52:44.9910662 +0000 utc
Status:
 State:                 Ready
 Availability:          Active
 Address:               172.17.0.2
Manager Status:
 Address:               172.17.0.2:2377
 Raft Status:           Reachable
 Leader:                Yes
Platform:
 Operating System:      linux
 Architecture:          x86_64
Resources:
 CPUs:                  4
 Memory:                7.704 GiB
Plugins:
  Network:              overlay, bridge, null, host, overlay
  Volume:               local
Engine Version:         17.06.0-ce
TLS Info:
 TrustRoot:
-----BEGIN CERTIFICATE-----
MIIBazCCARCgAwIBAgIUOzgqU4tA2q5Yv1HnkzhSIwGyIBswCgYIKoZIzj0EAwIw
EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNTAyMDAyNDAwWhcNMzcwNDI3MDAy
NDAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
A0IABMbiAmET+HZyve35ujrnL2kOLBEQhFDZ5MhxAuYs96n796sFlfxTxC1lM/2g
Ah8DI34pm3JmHgZxeBPKUURJHKWjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
Af8EBTADAQH/MB0GA1UdDgQWBBS3sjTJOcXdkls6WSY2rTx1KIJueTAKBggqhkjO
PQQDAgNJADBGAiEAoeVWkaXgSUAucQmZ3Yhmx22N/cq1EPBgYHOBZmHt0NkCIQC3
zONcJ/+WA21OXtb+vcijpUOXtNjyHfcox0N8wsLDqQ==
-----END CERTIFICATE-----

 Issuer Public Key: MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAExuICYRP4dnK97fm6OucvaQ4sERCEUNnkyHEC5iz3qfv3qwWV/FPELWUz/aACHwMjfimbcmYeBnF4E8pRREkcpQ==
 Issuer Subject:    MBMxETAPBgNVBAMTCHN3YXJtLWNh
```

----
url: https://docs.docker.com/reference/cli/docker/node/update/
----

# docker node update

***

| Description | Update a node                       |
| ----------- | ----------------------------------- |
| Usage       | `docker node update [OPTIONS] NODE` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Update metadata about a node, such as its availability, labels, or roles.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                      | Default | Description                                           |
| --------------------------- | ------- | ----------------------------------------------------- |
| `--availability`            |         | Availability of the node (`active`, `pause`, `drain`) |
| [`--label-add`](#label-add) |         | Add or update a node label (`key=value`)              |
| `--label-rm`                |         | Remove a node label if exists                         |
| `--role`                    |         | Role of the node (`worker`, `manager`)                |

## [Examples](#examples)

### [Add label metadata to a node (--label-add)](#label-add)

Add metadata to a swarm node using node labels. You can specify a node label as a key with an empty value:

```bash
$ docker node update --label-add foo worker1
```

To add multiple labels to a node, pass the `--label-add` flag for each label:

```console
$ docker node update --label-add foo --label-add bar worker1
```

When you [create a service](/reference/cli/docker/service/create/), you can use node labels as a constraint. A constraint limits the nodes where the scheduler deploys tasks for a service.

For example, to add a `type` label to identify nodes where the scheduler should deploy message queue service tasks:

```bash
$ docker node update --label-add type=queue worker1
```

The labels you set for nodes using `docker node update` apply only to the node entity within the swarm. Do not confuse them with the docker daemon labels for [dockerd](/reference/cli/dockerd/).

For more information about labels, refer to [apply custom metadata](/engine/userguide/labels-custom-metadata/).

----
url: https://docs.docker.com/scout/integrations/ci/gha/
----

# Integrate Docker Scout with GitHub Actions

***

Table of contents

***

The following example shows how to set up a Docker Scout workflow with GitHub Actions. Triggered by a pull request, the action builds the image and uses Docker Scout to compare the new version to the version of that image running in production.

This workflow uses the [docker/scout-action](https://github.com/docker/scout-action) GitHub Action to run the `docker scout compare` command to visualize how images for pull request stack up against the image you run in production.

## [Prerequisites](#prerequisites)

* This example assumes that you have an existing image repository, in Docker Hub or in another registry, where you've enabled Docker Scout.
* This example makes use of [environments](https://docs.docker.com/scout/integrations/environment/), to compare the image built in the pull request with a different version of the same image in an environment called `production`.

## [Steps](#steps)

First, set up the GitHub Action workflow to build an image. This isn't specific to Docker Scout here, but you'll need to build an image to have something to compare with.

Add the following to a GitHub Actions YAML file:

```yaml
name: Docker

on:
  push:
    tags: ["*"]
    branches:
      - "main"
  pull_request:
    branches: ["**"]

env:
  # Hostname of your registry
  REGISTRY: docker.io
  # Image repository, without hostname and tag
  IMAGE_NAME: ${{ github.repository }}
  SHA: ${{ github.event.pull_request.head.sha || github.event.after }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write

    steps:
      # Authenticate to the container registry
      - name: Authenticate to registry ${{ env.REGISTRY }}
        uses: docker/login-action@v4
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}
      
      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v4

      # Extract metadata (tags, labels) for Docker
      - name: Extract Docker metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          labels: |
            org.opencontainers.image.revision=${{ env.SHA }}
          tags: |
            type=edge,branch=$repo.default_branch
            type=semver,pattern=v{{version}}
            type=sha,prefix=,suffix=,format=short

      # Build and push Docker image with Buildx
      # (don't push on PR, load instead)
      - name: Build and push Docker image
        id: build-and-push
        uses: docker/build-push-action@v7
        with:
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

This creates workflow steps to:

1. Set up Docker buildx.
2. Authenticate to the registry.
3. Extract metadata from Git reference and GitHub events.
4. Build and push the Docker image to the registry.

> Note
>
> This CI workflow runs a local analysis and evaluation of your image. To evaluate the image locally, you must ensure that the image is loaded the local image store of your runner.
>
> This comparison doesn't work if you push the image to a registry, or if you build an image that can't be loaded to the runner's local image store. For example, multi-platform images or images with SBOM or provenance attestation can't be loaded to the local image store.

With this setup out of the way, you can add the following steps to run the image comparison:

```yaml
      # You can skip this step if Docker Hub is your registry
      # and you already authenticated before
      - name: Authenticate to Docker
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      # Compare the image built in the pull request with the one in production
      - name: Docker Scout
        id: docker-scout
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          ignore-unchanged: true
          only-severities: critical,high
          github-token: ${{ secrets.GITHUB_TOKEN }}
```

The compare command analyzes the image and evaluates policy compliance, and cross-references the results with the corresponding image in the `production` environment. This example only includes critical and high-severity vulnerabilities, and excludes vulnerabilities that exist in both images, showing only what's changed.

The GitHub Action outputs the comparison results in a pull request comment by default.

Expand the **Policies** section to view the difference in policy compliance between the two images. Note that while the new image in this example isn't fully compliant, the output shows that the standing for the new image has improved compared to the baseline.

----
url: https://docs.docker.com/reference/cli/docker/dhi/customization/build/logs/
----

# docker dhi customization build logs

***

| Description | Get logs of a build                                                  |
| ----------- | -------------------------------------------------------------------- |
| Usage       | `docker dhi customization build logs <repository> <name> <build-id>` |

## [Description](#description)

Get the logs of a Docker Hardened Images customization build

## [Options](#options)

| Option   | Default | Description           |
| -------- | ------- | --------------------- |
| `--json` |         | Output in JSON format |

----
url: https://docs.docker.com/reference/cli/docker/mcp/catalog/list/
----

# docker mcp catalog list

***

| Description                                                               | List catalogs             |
| ------------------------------------------------------------------------- | ------------------------- |
| Usage                                                                     | `docker mcp catalog list` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp catalog ls`   |

## [Description](#description)

List catalogs

## [Options](#options)

| Option     | Default | Description                   |
| ---------- | ------- | ----------------------------- |
| `--format` | `human` | Supported: json, yaml, human. |

----
url: https://docs.docker.com/reference/compose-file/profiles/
----

# Learn how to use profiles in Docker Compose

***

Table of contents

***

With profiles you can define a set of active profiles so your Compose application model is adjusted for various usages and environments.

The [services](https://docs.docker.com/reference/compose-file/services/) top-level element supports a `profiles` attribute to define a list of named profiles. Services without a `profiles` attribute are always enabled.

A service is ignored by Compose when none of the listed `profiles` match the active ones, unless the service is explicitly targeted by a command. In that case its profile is added to the set of active profiles.

> Note
>
> All other top-level elements are not affected by `profiles` and are always active.

References to other services (by `links`, `extends` or shared resource syntax `service:xxx`) do not automatically enable a component that would otherwise have been ignored by active profiles. Instead Compose returns an error.

## [Illustrative example](#illustrative-example)

```yaml
services:
  web:
    image: web_image

  test_lib:
    image: test_lib_image
    profiles:
      - test

  coverage_lib:
    image: coverage_lib_image
    depends_on:
      - test_lib
    profiles:
      - test

  debug_lib:
    image: debug_lib_image
    depends_on:
      - test_lib
    profiles:
      - debug
```

In the above example:

* If the Compose application model is parsed when no profile is enabled, it only contains the `web` service.
* If the profile `test` is enabled, the model contains the services `test_lib` and `coverage_lib`, and service `web`, which is always enabled.
* If the profile `debug` is enabled, the model contains both `web` and `debug_lib` services, but not `test_lib` and `coverage_lib`, and as such the model is invalid regarding the `depends_on` constraint of `debug_lib`.
* If the profiles `debug` and `test` are enabled, the model contains all services; `web`, `test_lib`, `coverage_lib` and `debug_lib`.
* If Compose is executed with `test_lib` as the explicit service to run, `test_lib` and the `test` profile are active even if `test` profile is not enabled.
* If Compose is executed with `coverage_lib` as the explicit service to run, the service `coverage_lib` and the profile `test` are active and `test_lib` is pulled in by the `depends_on` constraint.
* If Compose is executed with `debug_lib` as the explicit service to run, again the model is invalid regarding the `depends_on` constraint of `debug_lib`, since `debug_lib` and `test_lib` have no common `profiles` listed.
* If Compose is executed with `debug_lib` as the explicit service to run and profile `test` is enabled, profile `debug` is automatically enabled and service `test_lib` is pulled in as a dependency starting both services `debug_lib` and `test_lib`.

Learn how to use `profiles` in [Docker Compose](https://docs.docker.com/compose/how-tos/profiles/).

----
url: https://docs.docker.com/dhi/migration/migrate-from-wolfi/
----

# Migrate from Wolfi

***

Table of contents

***

This guide helps you migrate from Wolfi-based images to Docker Hardened Images (DHI). Generally, the migration process is straightforward since Wolfi is Alpine-like and DHI provides an Alpine-based hardened image.

Like other hardened images, DHI provides comprehensive [attestations](/dhi/core-concepts/attestations/) including SBOMs and provenance, allowing you to [verify](https://docs.docker.com/dhi/how-to/verify/) image signatures and [scan](https://docs.docker.com/dhi/how-to/scan/) for vulnerabilities to ensure the security and integrity of your images.

## [Migration steps](#migration-steps)

The following example demonstrates how to migrate a Dockerfile from a Wolfi-based image to an Alpine-based Docker Hardened Image.

### [Step 1: Update the base image in your Dockerfile](#step-1-update-the-base-image-in-your-dockerfile)

Update the base image in your application's Dockerfile to a hardened image. This is typically going to be an image tagged as `dev` or `sdk` because it has the tools needed to install packages and dependencies.

The following example diff snippet from a Dockerfile shows the old base image replaced by the new hardened image.

> Note
>
> You must authenticate to `dhi.io` before you can pull Docker Hardened Images. Use your Docker ID credentials (the same username and password you use for Docker Hub). If you don't have a Docker account, [create one](https://docs.docker.com/accounts/create-account/) for free.
>
> Run `docker login dhi.io` to authenticate.

```diff
- ## Original base image
- FROM cgr.dev/chainguard/go:latest-dev

+ ## Updated to use hardened base image
+ FROM dhi.io/golang:1.25-alpine3.22-dev
```

Note that DHI does not have a `latest` tag in order to promote best practices around image versioning. Ensure that you specify the appropriate version tag for your image. To find the right tag, explore the available tags in the [DHI Catalog](https://hub.docker.com/hardened-images/catalog/).

### [Step 2: Update the runtime image in your Dockerfile](#step-2-update-the-runtime-image-in-your-dockerfile)

> Note
>
> Multi-stage builds are recommended to keep your final image minimal and secure. Single-stage builds are supported, but they include the full `dev` image and therefore result in a larger image with a broader attack surface.

To ensure that your final image is as minimal as possible, you should use a [multi-stage build](https://docs.docker.com/build/building/multi-stage/). All stages in your Dockerfile should use a hardened image. While intermediary stages will typically use images tagged as `dev` or `sdk`, your final runtime stage should use a runtime image.

Utilize the build stage to compile your application and copy the resulting artifacts to the final runtime stage. This ensures that your final image is minimal and secure.

The following example shows a multi-stage Dockerfile with a build stage and runtime stage:

```dockerfile
# Build stage
FROM dhi.io/golang:1.25-alpine3.22-dev AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM dhi.io/golang:1.25-alpine3.22
WORKDIR /app
COPY --from=builder /app/myapp .
ENTRYPOINT ["/app/myapp"]
```

After updating your Dockerfile, build and test your application. If you encounter issues, see the [Troubleshoot](https://docs.docker.com/dhi/troubleshoot/) guide for common problems and solutions.

## [Language-specific examples](#language-specific-examples)

See the examples section for language-specific migration examples:

* [Go](https://docs.docker.com/dhi/migration/examples/go/)
* [Python](https://docs.docker.com/dhi/migration/examples/python/)
* [Node.js](https://docs.docker.com/dhi/migration/examples/node/)

----
url: https://docs.docker.com/reference/cli/docker/compose/start/
----

# docker compose start

***

| Description | Start services                      |
| ----------- | ----------------------------------- |
| Usage       | `docker compose start [SERVICE...]` |

## [Description](#description)

Starts existing containers for a service

## [Options](#options)

| Option           | Default | Description                                                                 |
| ---------------- | ------- | --------------------------------------------------------------------------- |
| `--wait`         |         | Wait for services to be running\|healthy. Implies detached mode.            |
| `--wait-timeout` |         | Maximum duration in seconds to wait for the project to be running\|healthy  |

----
url: https://docs.docker.com/offload/configuration/
----

# Configure Docker Offload

***

Table of contents

***

Subscription: Docker Offload

Requires: Docker Desktop 4.68 or later

You can configure Docker Offload settings at different levels depending on your role. Organization owners can manage settings for all users in their organization, while individual developers can configure their own Docker Desktop settings when allowed by their organization.

## [Manage settings for your organization](#manage-settings-for-your-organization)

For organization owners, you can manage Docker Offload settings for all users in your organization. For more details, see [Manage Docker products](https://docs.docker.com/admin/organization/manage/manage-products/). To view usage for Docker Offload, see [Docker Offload usage](/offload/usage/).

## [Configure settings in Docker Desktop](#configure-settings-in-docker-desktop)

For developers, you can enable or disable Docker Offload in Docker Desktop if allowed by your organization. To manage this setting:

1. Open the Docker Desktop Dashboard and sign in.
2. Select the settings icon in the Docker Desktop Dashboard header.
3. In **Settings**, select **Docker Offload**.
4. Toggle **Enable Docker Offload**. When enabled, you can start Offload sessions.

----
url: https://docs.docker.com/guides/testcontainers-java-jooq-flyway/write-tests/
----

# Write tests with Testcontainers

***

Table of contents

***

Before writing the tests, create an SQL script to seed test data at `src/test/resources/test-data.sql`:

```sql
DELETE FROM comments;
DELETE FROM posts;
DELETE FROM users;

INSERT INTO users(id, name, email) VALUES
(1, 'Siva', 'siva@gmail.com'),
(2, 'Oleg', 'oleg@gmail.com');

INSERT INTO posts(id, title, content, created_by, created_at) VALUES
(1, 'Post 1 Title', 'Post 1 content', 1, CURRENT_TIMESTAMP),
(2, 'Post 2 Title', 'Post 2 content', 2, CURRENT_TIMESTAMP);

INSERT INTO comments(id, name, content, post_id, created_at) VALUES
(1, 'Ron', 'Comment 1', 1, CURRENT_TIMESTAMP),
(2, 'James', 'Comment 2', 1, CURRENT_TIMESTAMP),
(3, 'Robert', 'Comment 3', 2, CURRENT_TIMESTAMP);
```

## [Test with the @JooqTest slice](#test-with-the-jooqtest-slice)

The `@JooqTest` annotation loads only the persistence layer components and auto-configures jOOQ's `DSLContext`. Use the Testcontainers special JDBC URL to start a Postgres container.

Create `UserRepositoryJooqTest.java`:

```java
package com.testcontainers.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.jooq.DSLContext;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.jooq.JooqTest;
import org.springframework.test.context.jdbc.Sql;

@JooqTest(
  properties = {
    "spring.test.database.replace=none",
    "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db",
  }
)
@Sql("/test-data.sql")
class UserRepositoryJooqTest {

  @Autowired
  DSLContext dsl;

  UserRepository repository;

  @BeforeEach
  void setUp() {
    this.repository = new UserRepository(dsl);
  }

  @Test
  void shouldCreateUserSuccessfully() {
    User user = new User(null, "John", "john@gmail.com");

    User savedUser = repository.createUser(user);

    assertThat(savedUser.id()).isNotNull();
    assertThat(savedUser.name()).isEqualTo("John");
    assertThat(savedUser.email()).isEqualTo("john@gmail.com");
  }

  @Test
  void shouldGetUserByEmail() {
    User user = repository.getUserByEmail("siva@gmail.com").orElseThrow();

    assertThat(user.id()).isEqualTo(1L);
    assertThat(user.name()).isEqualTo("Siva");
    assertThat(user.email()).isEqualTo("siva@gmail.com");
  }
}
```

Here's what the test does:

* `@JooqTest` loads only the persistence layer and auto-configures `DSLContext`.
* The Testcontainers special JDBC URL (`jdbc:tc:postgresql:16-alpine:///db`) starts a PostgreSQL container automatically.
* Because `flyway-core` is on the classpath, Spring Boot runs the Flyway migrations from `src/main/resources/db/migration` on startup.
* `@Sql("/test-data.sql")` loads the test data before each test.
* The `UserRepository` is instantiated manually with the injected `DSLContext`.

## [Integration test with @SpringBootTest](#integration-test-with-springboottest)

For a full integration test, use `@SpringBootTest` with the Testcontainers `@ServiceConnection` support introduced in Spring Boot 3.1.

Create `UserRepositoryTest.java`:

```java
package com.testcontainers.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.test.context.jdbc.Sql;
import org.testcontainers.postgresql.PostgreSQLContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest
@Sql("/test-data.sql")
@Testcontainers
class UserRepositoryTest {

  @Container
  @ServiceConnection
  static PostgreSQLContainer postgres = new PostgreSQLContainer(
    "postgres:16-alpine"
  );

  @Autowired
  UserRepository repository;

  @Test
  void shouldCreateUserSuccessfully() {
    User user = new User(null, "John", "john@gmail.com");

    User savedUser = repository.createUser(user);

    assertThat(savedUser.id()).isNotNull();
    assertThat(savedUser.name()).isEqualTo("John");
    assertThat(savedUser.email()).isEqualTo("john@gmail.com");
  }

  @Test
  void shouldGetUserByEmail() {
    User user = repository.getUserByEmail("siva@gmail.com").orElseThrow();

    assertThat(user.id()).isEqualTo(1L);
    assertThat(user.name()).isEqualTo("Siva");
    assertThat(user.email()).isEqualTo("siva@gmail.com");
  }
}
```

Here's what the test does:

* `@SpringBootTest` loads the entire application context, so `UserRepository` is injected directly.
* `@Testcontainers` and `@Container` manage the PostgreSQL container lifecycle.
* `@ServiceConnection` auto-configures the datasource properties from the running container, replacing the need for `@DynamicPropertySource`.
* `@Sql("/test-data.sql")` initializes the test data.

## [Test PostRepository](#test-postrepository)

Test the `PostRepository` that fetches complex object graphs using the Testcontainers special JDBC URL.

Create `PostRepositoryTest.java`:

```java
package com.testcontainers.demo.domain;

import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.jdbc.Sql;

@SpringBootTest(
  properties = {
    "spring.test.database.replace=none",
    "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db",
  }
)
@Sql("/test-data.sql")
class PostRepositoryTest {

  @Autowired
  PostRepository repository;

  @Test
  void shouldGetPostById() {
    Post post = repository.getPostById(1L).orElseThrow();

    assertThat(post.id()).isEqualTo(1L);
    assertThat(post.title()).isEqualTo("Post 1 Title");
    assertThat(post.content()).isEqualTo("Post 1 content");
    assertThat(post.createdBy().id()).isEqualTo(1L);
    assertThat(post.createdBy().name()).isEqualTo("Siva");
    assertThat(post.createdBy().email()).isEqualTo("siva@gmail.com");
    assertThat(post.comments()).hasSize(2);
  }
}
```

This test verifies that `getPostById` loads the post along with its creator and comments in a single query using jOOQ's MULTISET feature.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-java-jooq-flyway/run-tests/)

----
url: https://docs.docker.com/reference/cli/docker/context/import/
----

# docker context import

***

| Description | Import a context from a tar or zip file |
| ----------- | --------------------------------------- |
| Usage       | `docker context import CONTEXT FILE\|-` |

## [Description](#description)

Imports a context previously exported with `docker context export`. To import from stdin, use a hyphen (`-`) as filename.

----
url: https://docs.docker.com/engine/install/centos/
----

# Install Docker Engine on CentOS

***

Table of contents

***

To get started with Docker Engine on CentOS, make sure you [meet the prerequisites](#prerequisites), and then follow the [installation steps](#installation-methods).

## [Prerequisites](#prerequisites)

### [OS requirements](#os-requirements)

To install Docker Engine, you need a maintained version of one of the following CentOS versions:

* CentOS Stream 10
* CentOS Stream 9

The `centos-extras` repository must be enabled. This repository is enabled by default. If you have disabled it, you need to re-enable it.

### [Uninstall old versions](#uninstall-old-versions)

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict with the official packages provided by Docker. You must uninstall these packages before you install the official version of Docker Engine.

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine
```

```console
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

#### [Install Docker Engine](#install-docker-engine)

1. Install the Docker packages.

   To install the latest version, run:

   ```console
   $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   If prompted to accept the GPG key, verify that the fingerprint matches `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`, and if so, accept it.

   This command installs Docker, but it doesn't start Docker. It also creates a `docker` group, however, it doesn't add any users to the group by default.

   To install a specific version, start by listing the available versions in the repository:

   ```console
   $ dnf list docker-ce --showduplicates | sort -r

   docker-ce.x86_64    3:29.5.3-1.el9    docker-ce-stable
   docker-ce.x86_64    3:29.5.2-1.el9    docker-ce-stable
   <...>
   ```

   The list returned depends on which repositories are enabled, and is specific to your version of CentOS (indicated by the `.el9` suffix in this example).

   Install a specific version by its fully qualified package name, which is the package name (`docker-ce`) plus the version string (2nd column), separated by a hyphen (`-`). For example, `docker-ce-3:29.5.3-1.el9`.

   Replace `<VERSION_STRING>` with the desired version and then run the following command to install:

   ```console
   $ sudo dnf install docker-ce-VERSION_STRING docker-ce-cli-VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   This command installs Docker, but it doesn't start Docker. It also creates a `docker` group, however, it doesn't add any users to the group by default.

2. Start Docker Engine.

   ```console
   $ sudo systemctl enable --now docker
   ```

   This configures the Docker systemd service to start automatically when you boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.

3. Verify that the installation is successful by running the `hello-world` image:

   ```console
   $ sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
> The `docker` user group exists but contains no users, which is why you’re required to use `sudo` to run Docker commands. Continue to [Linux postinstall](/engine/install/linux-postinstall) to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### [Upgrade Docker Engine](#upgrade-docker-engine)

To upgrade Docker Engine, follow the [installation instructions](#install-using-the-repository), choosing the new version you want to install.

### [Install from a package](#install-from-a-package)

If you can't use Docker's `rpm` repository to install Docker Engine, you can download the `.rpm` file for your release and install it manually. You need to download a new file each time you want to upgrade Docker Engine.

1. Go to <https://download.docker.com/linux/centos/> and choose your version of CentOS. Then browse to `x86_64/stable/Packages/` and download the `.rpm` file for the Docker version you want to install.

2. Install Docker Engine, changing the following path to the path where you downloaded the Docker package.

   ```console
   $ sudo dnf install /path/to/package.rpm
   ```

   Docker is installed but not started. The `docker` group is created, but no users are added to the group.

3. Start Docker Engine.

   ```console
   $ sudo systemctl enable --now docker
   ```

   This configures the Docker systemd service to start automatically when you boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.

4. Verify that the installation is successful by running the `hello-world` image:

   ```console
   $ sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
> The `docker` user group exists but contains no users, which is why you’re required to use `sudo` to run Docker commands. Continue to [Linux postinstall](/engine/install/linux-postinstall) to allow non-privileged users to run Docker commands and for other optional configuration steps.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the script will run when invoked:
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from <https://get.docker.com/> and runs it to install the latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker` service starts automatically on Debian based distributions. On `RPM` based distributions, such as CentOS, Fedora or RHEL, you need to start it manually using the appropriate `systemctl` or `service` command. As the message indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
> The installation script requires `root` or `sudo` privileges to install and use Docker. If you want to grant non-root users access to Docker, refer to the [post-installation steps for Linux](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user). You can also install Docker without `root` privileges, or configured to run in rootless mode. For instructions on running Docker in rootless mode, refer to [run the Docker daemon as a non-root user (rootless mode)](/engine/security/rootless/).

#### [Install pre-releases](#install-pre-releases)

Docker also provides a convenience script at <https://test.docker.com/> to install pre-releases of Docker on Linux. This script is equal to the script at `get.docker.com`, but configures your package manager to use the test channel of the Docker package repository. The test channel includes both stable and pre-releases (beta versions, release-candidates) of Docker. Use this script to get early access to new releases, and to evaluate them in a testing environment before they're released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### [Upgrade Docker after using the convenience script](#upgrade-docker-after-using-the-convenience-script)

If you installed Docker using the convenience script, you should upgrade Docker using your package manager directly. There's no advantage to re-running the convenience script. Re-running it can cause issues if it attempts to re-install repositories which already exist on the host machine.

## [Uninstall Docker Engine](#uninstall-docker-engine)

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:

   ```console
   $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

----
url: https://docs.docker.com/reference/cli/docker/dhi/customization/
----

# docker dhi customization

***

| Description                                                               | Manage Docker Hardened Images customizations |
| ------------------------------------------------------------------------- | -------------------------------------------- |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker dhi c` `docker dhi custo`            |

## [Description](#description)

Commands to list, create, edit, and delete Docker Hardened Images customizations

## [Options](#options)

| Option  | Default | Description                                |
| ------- | ------- | ------------------------------------------ |
| `--org` |         | Docker Hub organization (overrides config) |

## [Subcommands](#subcommands)

| Command                                                                                                       | Description                                                     |
| ------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| [`docker dhi customization build`](https://docs.docker.com/reference/cli/docker/dhi/customization/build/)     | Manage customization builds                                     |
| [`docker dhi customization create`](https://docs.docker.com/reference/cli/docker/dhi/customization/create/)   | Create a new customization from YAML file                       |
| [`docker dhi customization delete`](https://docs.docker.com/reference/cli/docker/dhi/customization/delete/)   | Delete one or more customizations                               |
| [`docker dhi customization edit`](https://docs.docker.com/reference/cli/docker/dhi/customization/edit/)       | Edit an existing customization from YAML file                   |
| [`docker dhi customization get`](https://docs.docker.com/reference/cli/docker/dhi/customization/get/)         | Get details of a specific customization                         |
| [`docker dhi customization list`](https://docs.docker.com/reference/cli/docker/dhi/customization/list/)       | List all customizations                                         |
| [`docker dhi customization prepare`](https://docs.docker.com/reference/cli/docker/dhi/customization/prepare/) | Prepare a new customization YAML file from a DHI base image tag |

----
url: https://docs.docker.com/guides/nodejs/secure-supply-chain/
----

# Secure your Node.js image supply chain

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Automate your builds with GitHub Actions](https://docs.docker.com/guides/nodejs/configure-github-actions/).

## [Overview](#overview)

When you ship a container image, what's inside it and where it came from matters. Supply chain attestations are signed records that answer questions like which packages are in the image, what vulnerabilities affect them, how the image was built, and what security checks it passed.

In this section, you'll inspect the attestations that ship with your Docker Hardened Image base, generate your own SBOM and provenance attestations during CI, and pin the base image by digest so your builds are reproducible.

The inspection commands in this topic are shown manually so you can see what each one returns. In a real workflow you'd automate these checks with [Docker Scout](/scout/), which runs the same scans on every push, enforces policies in CI, and surfaces results in your registry and pull requests.

## [Inspect the base image attestations](#inspect-the-base-image-attestations)

Docker Hardened Images are built to SLSA Build Level 3 and ship with a set of signed attestations covering bill-of-materials, vulnerabilities, build provenance, and security scans. See [DHI attestations](https://docs.docker.com/dhi/core-concepts/attestations/) for the full list of types and how to verify their signatures with Cosign.

List all the attestations available on the Node.js DHI:

```console
$ docker scout attest list registry://dhi.io/node:24-alpine3.23-dev
```

View the SBOM:

```console
$ docker scout sbom registry://dhi.io/node:24-alpine3.23-dev
```

Check known vulnerabilities:

```console
$ docker scout cves registry://dhi.io/node:24-alpine3.23-dev
```

> Note
>
> The `registry://` prefix forces `docker scout` to fetch the image and its attestations from the registry instead of reading a locally pulled copy. If you've already pulled or built against the base image, the local copy doesn't have the attached attestations, so the prefix is required to see them.

When you base your own image on a DHI image, these attestations stay attached to the base layer in the registry. Tools that inspect your image can follow the chain back to the DHI source.

## [Generate attestations for your image](#generate-attestations-for-your-image)

Update your GitHub Actions workflow to attach SBOM and provenance attestations to the image you push.

Edit `.github/workflows/build.yml` and update the build-and-push step:

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v7
  with:
    context: .
    push: true
    sbom: true
    provenance: mode=max
    tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

* `sbom: true` tells BuildKit to scan the built image and attach an SBOM attestation.
* `provenance: mode=max` records detailed build provenance, including the source repository, commit, and build parameters.

The next time your workflow runs, the pushed image will carry these attestations alongside the image manifest in the registry.

## [Inspect your pushed image's attestations](#inspect-your-pushed-images-attestations)

After your workflow pushes the image, inspect it the same way you inspected the base image:

```console
$ docker scout attest list registry://DOCKER_USERNAME/REPO_NAME:latest
$ docker scout sbom registry://DOCKER_USERNAME/REPO_NAME:latest
```

The SBOM includes packages from every layer, including those inherited from `dhi.io/node:24-alpine3.23-dev`. The provenance record references the DHI base image by digest, so consumers of your image can trace the build chain back to the DHI source.

## [Pin the base image by digest](#pin-the-base-image-by-digest)

Image tags like `dhi.io/node:24-alpine3.23-dev` move over time as new patches land. For reproducible builds, pin to an immutable digest.

Look up the digest for each image:

```console
$ docker buildx imagetools inspect dhi.io/node:24-alpine3.23-dev --format "{{ .Manifest.Digest }}"
sha256:2bf01111c7dfe429362f64b3977f0cd6e63ff39023012f88487dec7e83aa26ca
$ docker buildx imagetools inspect dhi.io/node:24-alpine3.23 --format "{{ .Manifest.Digest }}"
sha256:868827fd45c6a01f7f3337ba7ff3f48ebb14da10d8cf3d347f98ded5481317a5
```

Each digest is a 64-character hex string. Update your `Dockerfile` to reference each digest on its corresponding `FROM` line:

```dockerfile
FROM dhi.io/node:24-alpine3.23-dev@sha256:2bf01111c7dfe429362f64b3977f0cd6e63ff39023012f88487dec7e83aa26ca AS dev
# ...
FROM dhi.io/node:24-alpine3.23@sha256:868827fd45c6a01f7f3337ba7ff3f48ebb14da10d8cf3d347f98ded5481317a5 AS runner
```

> Tip
>
> Pinning by digest also pins you to that image's vulnerabilities. Use [Dependabot](https://docs.github.com/en/code-security/dependabot) or [Renovate](https://docs.renovatebot.com/) to automate digest updates so you get a PR when a new patched image is available, with a changelog to review before merging.

## [Summary](#summary)

In this section, you learned how to:

* Inspect the supply chain attestations that ship with the DHI base image, including SBOMs, CVE reports, and build provenance

[Deploy your Node.js application »](https://docs.docker.com/guides/nodejs/deploy/)

----
url: https://docs.docker.com/admin/organization/manage/members/
----

# Manage organization members

***

Table of contents

***

Learn how to manage members for your organization in Docker Hub and the Docker Admin Console.

## [Invite members](#invite-members)

Owners can invite new members to an organization via Docker ID, email address, or with a CSV file containing email addresses. If an invitee does not have a Docker account, they must create an account and verify their email address before they can accept an invitation to join the organization. When inviting members, their pending invitation occupies a seat.

### [Invite members via Docker ID or email address](#invite-members-via-docker-id-or-email-address)

Use the following steps to invite members to your organization via Docker ID or email address.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Select **Members**, then **Invite**.
3. Select **Emails or usernames**.
4. Follow the on-screen instructions to invite members. Invite a maximum of 1000 members and separate multiple entries by comma, semicolon, or space.

When you invite members, you assign them a role. See [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/) for details about the access permissions for each role.

Pending invitations appear in the table. Invitees receive an email with a link to Docker Hub where they can accept or decline the invitation.

### [Invite members via CSV file](#invite-members-via-csv-file)

To invite multiple members to an organization via a CSV file containing email addresses:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down. Select **Members** > **Invite** > **CSV upload**.

2. Optional. Select **Download the template CSV file** to download an example CSV file. The following is an example of the contents of a valid CSV file:

   ```text
   email
   docker.user-0@example.com
   docker.user-1@example.com
   ```

   The example file demonstrates CSV file requirements:

   * The file must contain a header row with at least one heading named email. Additional columns are allowed and are ignored in the import.
   * The file must contain a maximum of 1000 email addresses (rows). To invite more than 1000 users, create multiple CSV files and perform all steps in this task for each file.

3. Create a new CSV file or export a CSV file from another application.

   * To export a CSV file from another application, see the application’s documentation.
   * To create a new CSV file, open a new file in a text editor, type email on the first line, type the user email addresses one per line on the following lines, and then save the file with a .csv extension.

4. Select **Browse files** and then select your CSV file, or drag and drop the CSV file into the **Select a CSV file to upload** box. You can only select one CSV file at a time.

5. After the CSV file has been uploaded, select **Review** to identify any invalid email addresses, already invited users, invited users who are already members, or duplicated email addresses within the same CSV file.

6. Follow the on-screen instructions to invite members.

Pending invitations appear in the table. The invitees receive an email with a link to Docker Hub where they can accept or decline the invitation.

### [Invite members via API](#invite-members-via-api)

You can bulk invite members using the Docker Hub API. For more information, see the [Bulk create invites](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) API endpoint.

## [Accept invitation](#accept-invitation)

After receiving an email invitation, users can access a link to Docker Hub where they can accept or decline the invitation.

To accept an invitation:

1. Check your email inbox and open the Docker email with an invitation to join the Docker organization.
2. To open the link to Docker Hub, select the **click here** link.
3. The Docker create an account page will open. If you already have an account, select **Already have an account? Sign in**. If you do not have an account yet, create an account using the same email address you received the invitation through.
4. Optional. If you do not have an account and created one, you must navigate back to your email inbox and verify your email address using the Docker verification email.
5. Once you are signed in to Docker Hub, select **My Hub** from the top-level navigation menu.
6. Select **Accept** on your invitation.

After accepting an invitation, you are now a member of the organization.

Invitation email links expire after 14 days. If your email link has expired, you can sign in to [Docker Hub](https://hub.docker.com/) with the email address the link was sent to and accept the invitation from the **Notifications** panel.

## [Manage invitations](#manage-invitations)

After inviting members, you can resend or remove invitations as needed. Each invitee occupies one seat, so if the amount of email addresses in your CSV file exceeds the number of available seats in your organization, you won't be able to invite more members.

> Tip
>
> Need to manage more than 1,000 team members? [Upgrade to Docker Business for unlimited user invites](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdminMembers) and advanced role management. You can also [add seats](https://docs.docker.com/admin/organization/manage/manage-seats/) to your subscription.

### [Resend an invitation](#resend-an-invitation)

You can send individual invitations, or bulk invitations from the Admin Console.

To resend an individual invitation:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Members**.
3. Select the **action menu** next to the invitee and select **Resend**.
4. Select **Invite** to confirm.

To bulk resend invitations:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Members**.
3. Use the **checkboxes** next to **Usernames** to bulk select users.
4. Select **Resend invites**.
5. Select **Resend** to confirm.

### [Remove an invitation](#remove-an-invitation)

To remove an invitation from the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Members**.
3. Select the **action menu** next to the invitee and select **Remove invitee**.
4. Select **Remove** to confirm.

## [Manage members on a team](#manage-members-on-a-team)

Use Docker Hub or the Admin Console to add or remove team members. Organization owners can add a member to one or more teams within an organization.

### [Add a member to a team](#add-a-member-to-a-team)

To add a member to a team with the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Teams**.
3. Select the team name.
4. Select **Add member**. You can add the member by searching for their email address or username.

An invitee must first accept the invitation to join the organization before being added to the team.

### [Remove members from teams](#remove-members-from-teams)

If your organization uses single sign-on (SSO) with [SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) enabled, you should remove members from your identity provider (IdP). This automatically removes members from Docker. If SCIM is disabled, follow procedures in this doc to remove members manually in Docker.

Organization owners can remove a member from a team in Docker Hub or Admin Console. Removing the member from the team will revoke their access to the permitted resources. To remove a member from a specific team with the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Teams**, then choose the name of the team member you want to remove.
3. Select the **X** next to the user's name to remove them from the team.
4. When prompted, select **Remove** to confirm.

### [Update a member role](#update-a-member-role)

Organization owners can manage [roles](https://docs.docker.com/enterprise/security/roles-and-permissions/) within an organization. If an organization is part of a company, the company owner can also manage that organization's roles. If you have SSO enabled, you can use [SCIM for role mapping](https://docs.docker.com/enterprise/security/provisioning/scim/).

To update a member role in the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Members**.
3. Find the username of the member whose role you want to edit. Select the **Actions** menu, then **Edit role**.

If you're the only owner of an organization and you want to edit your role, assign a new owner for your organization so you can edit your role.

## [Export members CSV file](#export-members-csv-file)

Subscription: Team Business

For: Administrators

Owners can export a CSV file containing all members. The CSV file for a company contains the following fields:

* Name: The user's name
* Username: The user's Docker ID
* Email: The user's email address
* Member of Organizations: All organizations the user is a member of within a company
* Invited to Organizations: All organizations the user is an invitee of within a company
* Account Created: The time and date when the user account was created

To export a CSV file of your members:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Members**.
3. Select the **download** icon to export a CSV file of all members.

----
url: https://docs.docker.com/guides/bun/
----

# Bun language-specific guide

Table of contents

***

Learn how to containerize JavaScript applications with the Bun runtime.

**Time to complete** 10 minutes

The Bun getting started guide teaches you how to create a containerized Bun application using Docker.

> **Acknowledgment**
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

## [What will you learn?](#what-will-you-learn)

* Containerize and run a Bun application using Docker
* Set up a local environment to develop a Bun application using containers
* Configure a CI/CD pipeline for a containerized Bun application using GitHub Actions
* Deploy your containerized application locally to Kubernetes to test and debug your deployment

## [Prerequisites](#prerequisites)

* Basic understanding of JavaScript is assumed.
* You must have familiarity with Docker concepts like containers, images, and Dockerfiles. If you are new to Docker, you can start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

After completing the Bun getting started modules, you should be able to containerize your own Bun application based on the examples and instructions provided in this guide.

Start by containerizing an existing Bun application.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/bun/containerize/)

   Learn how to containerize a Bun application.

2. [Develop your app](https://docs.docker.com/guides/bun/develop/)

   Learn how to develop your Bun application locally.

3. [Configure CI/CD](https://docs.docker.com/guides/bun/configure-ci-cd/)

   Learn how to configure CI/CD using GitHub Actions for your Bun application.

4. [Test your deployment](https://docs.docker.com/guides/bun/deploy/)

   Learn how to develop locally using Kubernetes

----
url: https://docs.docker.com/guides/go-prometheus-monitoring/
----

# Monitor a Golang application with Prometheus and Grafana

Table of contents

***

Learn how to containerize a Golang application and monitor it with Prometheus and Grafana.

**Time to complete** 45 minutes

The guide teaches you how to containerize a Golang application and monitor it with Prometheus and Grafana.

> **Acknowledgment**
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

## [Overview](#overview)

To make sure your application is working as intended, monitoring is important. One of the most popular monitoring tools is Prometheus. Prometheus is an open-source monitoring and alerting toolkit that is designed for reliability and scalability. It collects metrics from monitored targets by scraping metrics HTTP endpoints on these targets. To visualize the metrics, you can use Grafana. Grafana is an open-source platform for monitoring and observability that allows you to query, visualize, alert on, and understand your metrics no matter where they are stored.

In this guide, you will be creating a Golang server with some endpoints to simulate a real-world application. Then you will expose metrics from the server using Prometheus. Finally, you will visualize the metrics using Grafana. You will containerize the Golang application, and using the Docker Compose file, you will connect all the services: Golang, Prometheus, and Grafana.

## [What will you learn?](#what-will-you-learn)

* Create a Golang application with custom Prometheus metrics.
* Containerize a Golang application.
* Use Docker Compose to run multiple services and connect them together to monitor a Golang application with Prometheus and Grafana.
* Visualize the metrics using Grafana dashboards.

## [Prerequisites](#prerequisites)

* A good understanding of Golang is assumed.
* You must me familiar with Prometheus and creating dashboards in Grafana.
* You must have familiarity with Docker concepts like containers, images, and Dockerfiles. If you are new to Docker, you can start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

## [Next steps](#next-steps)

You will create a Golang server and expose metrics using Prometheus.

## [Modules](#modules)

1. [Understand the application](https://docs.docker.com/guides/go-prometheus-monitoring/application/)

   Learn how to create a Golang server to register metrics with Prometheus.

2. [Containerize your app](https://docs.docker.com/guides/go-prometheus-monitoring/containerize/)

   Learn how to containerize a Golang application.

3. [Connect with Compose](https://docs.docker.com/guides/go-prometheus-monitoring/compose/)

   Learn how to connect services with Docker Compose to monitor a Golang application with Prometheus and Grafana.

4. [Develop your app](https://docs.docker.com/guides/go-prometheus-monitoring/develop/)

   Learn how to develop the Golang application with Docker.

----
url: https://docs.docker.com/enterprise/security/single-sign-on/troubleshoot-sso/
----

# Troubleshoot single sign-on

***

Table of contents

***

This page describes common single sign-on (SSO) errors and their solutions. Issues can stem from your identity provider (IdP) configuration or Docker settings.

## [Check for errors](#check-for-errors)

If you experience SSO issues, check both Docker and your identity provider for errors first.

### [Check Docker error logs](#check-docker-error-logs)

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Action** menu and then **View error logs**.
4. For more details on specific errors, select **View error details** next to an error message.
5. Note any errors you see on this page for further troubleshooting.

### [Check identity provider errors](#check-identity-provider-errors)

1. Review your IdP’s logs or audit trails for any failed authentication or provisioning attempts.
2. Confirm that your IdP’s SSO settings match the values provided in Docker.
3. If applicable, confirm that you have configured user provisioning correctly and that it is enabled in your IdP.
4. If applicable, verify that your IdP correctly maps Docker's required user attributes.
5. Try provisioning a test user from your IdP and verify if they appear in Docker.

For further troubleshooting, check your IdP's documentation or contact their support team.

## [Groups are not formatted correctly](#groups-are-not-formatted-correctly)

### [Error message](#error-message)

When this issue occurs, the following error message is common:

```text
Some of the groups assigned to the user are not formatted as '<organization name>:<team name>'. Directory groups will be ignored and user will be provisioned into the default organization and team.
```

### [Causes](#causes)

* Incorrect group name formatting in your identity provider (IdP): Docker requires groups to follow the format `<organization>:<team>`. If the groups assigned to a user do not follow this format, they will be ignored.
* Non-matching groups between IdP and Docker organization: If a group in your IdP does not have a corresponding team in Docker, it will not be recognized, and the user will be placed in the default organization and team.

### [Affected environments](#affected-environments)

* Docker single sign-on setup using IdPs such as Okta or Azure AD
* Organizations using group-based role assignments in Docker

### [Steps to replicate](#steps-to-replicate)

To replicate this issue:

1. Attempt to sign in to Docker using SSO.
2. The user is assigned groups in the IdP but does not get placed in the expected Docker Team.
3. Review Docker logs or IdP logs to find the error message.

### [Solutions](#solutions)

Update group names in your IdP:

1. Go to your IdP's group management section.
2. Check the groups assigned to the affected user.
3. Ensure each group follows the required format: `<organization>:<team>`
4. Update any incorrectly formatted groups to match this pattern.
5. Save changes and retry signing in with SSO.

## [User is not assigned to the organization](#user-is-not-assigned-to-the-organization)

### [Error message](#error-message-1)

When this issue occurs, the following error message is common:

```text
User '$username' is not assigned to this SSO organization. Contact your administrator. TraceID: XXXXXXXXXXXXX
```

### [Causes](#causes-1)

* User is not assigned to the organization: If Just-in-Time (JIT) provisioning is disabled, the user may not be assigned to your organization.
* User is not invited to the organization: If JIT is disabled and you do not want to enable it, the user must be manually invited.
* SCIM provisioning is misconfigured: If you use SCIM for user provisioning, it may not be correctly syncing users from your IdP.

### [Solutions](#solutions-1)

**Enable JIT provisioning**

JIT is enabled by default when you enable SSO. If you have JIT disabled and need to re-enable it:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Action** menu and then **Enable JIT provisioning**.
4. Select **Enable** to confirm.

**Manually invite users**

When JIT is disabled, users are not automatically added to your organization when they authenticate through SSO. To manually invite users, see [Invite members](https://docs.docker.com/admin/organization/manage/members/#invite-members).

**Configure SCIM provisioning**

If you have SCIM enabled, troubleshoot your SCIM connection using the following steps:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.

2. Select **Admin Console**, then **SSO and SCIM**.

3. In the SSO connections table, select the **Action** menu and then **View error logs**. For more details on specific errors, select **View error details** next to an error message. Note any errors you see on this page.

4. Navigate back to the **SSO and SCIM** page of the Admin Console and verify your SCIM configuration:

   * Ensure that the SCIM Base URL and API Token in your IdP match those provided in the Docker Admin Console.
   * Verify that SCIM is enabled in both Docker and your IdP.

5. Ensure that the attributes being synced from your IdP match Docker's [supported attributes](https://docs.docker.com/enterprise/security/provisioning/scim/provision-scim/#supported-attributes) for SCIM.

6. Test user provisioning by trying to provision a test user through your IdP and verify if they appear in Docker.

## [IdP-initiated sign in is not enabled for connection](#idp-initiated-sign-in-is-not-enabled-for-connection)

### [Error message](#error-message-2)

When this issue occurs, the following error message is common:

```text
IdP-Initiated sign in is not enabled for connection '$ssoConnection'.
```

### [Causes](#causes-2)

Docker does not support an IdP-initiated SAML flow. This error occurs when a user attempts to authenticate from your IdP, such as using the Docker SSO app tile on the sign in page.

### [Solutions](#solutions-2)

**Authenticate from Docker apps**

The user must initiate authentication from Docker applications (Hub, Desktop, etc). The user needs to enter their email address in a Docker app and they will get redirected to the configured SSO IdP for their domain.

**Hide the Docker SSO app**

You can hide the Docker SSO app from users in your IdP. This prevents users from attempting to start authentication from the IdP dashboard. You must hide and configure this in your IdP.

## [Not enough seats in organization](#not-enough-seats-in-organization)

### [Error message](#error-message-3)

When this issue occurs, the following error message is common:

```text
Not enough seats in organization '$orgName'. Add more seats or contact your administrator.
```

### [Causes](#causes-3)

This error occurs when the organization has no available seats for the user when provisioning via Just-in-Time (JIT) provisioning or SCIM.

### [Solutions](#solutions-3)

**Add more seats to the organization**

Purchase additional Docker Business subscription seats. For details, see [Manage subscription seats](https://docs.docker.com/admin/organization/manage/manage-seats/).

**Remove users or pending invitations**

Review your organization members and pending invitations. Remove inactive users or pending invitations to free up seats. For more details, see [Manage organization members](https://docs.docker.com/admin/organization/manage/members/).

## [Domain is not verified for SSO connection](#domain-is-not-verified-for-sso-connection)

### [Error message](#error-message-4)

When this issue occurs, the following error message is common:

```text
Domain '$emailDomain' is not verified for your SSO connection. Contact your company administrator. TraceID: XXXXXXXXXXXXXX
```

### [Causes](#causes-4)

This error occurs if the IdP authenticated a user through SSO and the User Principal Name (UPN) returned to Docker doesn’t match any of the verified domains associated to the SSO connection configured in Docker.

### [Solutions](#solutions-4)

**Verify UPN attribute mapping**

Ensure that the IdP SSO connection is returning the correct UPN value in the assertion attributes.

**Add and verify all domains**

Add and verify all domains and subdomains used as UPN by your IdP and associate them with your Docker SSO connection. For details, see [Configure single sign-on](https://docs.docker.com/enterprise/security/single-sign-on/connect/).

## [Unable to find session](#unable-to-find-session)

### [Error message](#error-message-5)

When this issue occurs, the following error message is common:

```text
We couldn't find your session. You may have pressed the back button, refreshed the page, opened too many sign-in dialogs, or there is some issue with cookies. Try signing in again. If the issue persists, contact your administrator.
```

### [Causes](#causes-5)

The following causes may create this issue:

* The user pressed the back or refresh button during authentication.
* The authentication flow lost track of the initial request, preventing completion.

### [Solutions](#solutions-5)

**Do not disrupt the authentication flow**

Do not press the back or refresh button during sign-in.

**Restart authentication**

Close the browser tab and restart the authentication flow from the Docker application (Desktop, Hub, etc).

## [Name ID is not an email address](#name-id-is-not-an-email-address)

### [Error message](#error-message-6)

When this issue occurs, the following error message is common:

```text
The name ID sent by the identity provider is not an email address. Contact your company administrator.
```

### [Causes](#causes-6)

The following causes may create this issue:

* The IdP sends a Name ID (UPN) that does not comply with the email format required by Docker.
* Docker SSO requires the Name ID to be the primary email address of the user.

### [Solutions](#solutions-6)

In your IdP, ensure the Name ID attribute format is correct:

1. Verify that the Name ID attribute format in your IdP is set to `EmailAddress`.
2. Adjust your IdP settings to return the correct Name ID format.

----
url: https://docs.docker.com/build/bake/reference/
----

# Bake file reference

***

Table of contents

***

The Bake file is a file for defining workflows that you run using `docker buildx bake`.

## [File format](#file-format)

You can define your Bake file in the following file formats:

* HashiCorp Configuration Language (HCL)
* JSON
* YAML (Compose file)

By default, Bake uses the following lookup order to find the configuration file:

You can specify the file location explicitly using the `--file` flag:

```console
$ docker buildx bake --file ../docker/bake.hcl --print
```

If you don't specify a file explicitly, Bake searches for the file in the current working directory. If more than one Bake file is found, all files are merged into a single definition. Files are merged according to the lookup order. That means that if your project contains both a `compose.yaml` file and a `docker-bake.hcl` file, Bake loads the `compose.yaml` file first, and then the `docker-bake.hcl` file.

If merged files contain duplicate attribute definitions, those definitions are either merged or overridden by the last occurrence, depending on the attribute. The following attributes are overridden by the last occurrence:

* `target.cache-to`
* `target.dockerfile-inline`
* `target.dockerfile`
* `target.outputs`
* `target.platforms`
* `target.pull`
* `target.tags`
* `target.target`

For example, if `compose.yaml` and `docker-bake.hcl` both define the `tags` attribute, the `docker-bake.hcl` is used.

```console
$ cat compose.yaml
services:
  webapp:
    build:
      context: .
      tags:
        - bar
$ cat docker-bake.hcl
target "webapp" {
  tags = ["foo"]
}
$ docker buildx bake --print webapp
{
  "group": {
    "default": {
      "targets": [
        "webapp"
      ]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": [
        "foo"
      ]
    }
  }
}
```

All other attributes are merged. For example, if `compose.yaml` and `docker-bake.hcl` both define unique entries for the `labels` attribute, all entries are included. Duplicate entries for the same label are overridden.

```console
$ cat compose.yaml
services:
  webapp:
    build:
      context: .
      labels: 
        com.example.foo: "foo"
        com.example.name: "Alice"
$ cat docker-bake.hcl
target "webapp" {
  labels = {
    "com.example.bar" = "bar"
    "com.example.name" = "Bob"
  }
}
$ docker buildx bake --print webapp
{
  "group": {
    "default": {
      "targets": [
        "webapp"
      ]
    }
  },
  "target": {
    "webapp": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "labels": {
        "com.example.foo": "foo",
        "com.example.bar": "bar",
        "com.example.name": "Bob"
      }
    }
  }
}
```

## [Syntax](#syntax)

The Bake file supports the following property types:

* `target`: build targets
* `group`: collections of build targets
* `variable`: build arguments and variables
* `function`: custom Bake functions

You define properties as hierarchical blocks in the Bake file. You can assign one or more attributes to a property.

The following snippet shows a JSON representation of a simple Bake file. This Bake file defines three properties: a variable, a group, and a target.

```json
{
  "variable": {
    "TAG": {
      "default": "latest"
    }
  },
  "group": {
    "default": {
      "targets": ["webapp"]
    }
  },
  "target": {
    "webapp": {
      "dockerfile": "Dockerfile",
      "tags": ["docker.io/username/webapp:${TAG}"]
    }
  }
}
```

In the JSON representation of a Bake file, properties are objects, and attributes are values assigned to those objects.

The following example shows the same Bake file in the HCL format:

```hcl
variable "TAG" {
  default = "latest"
}

group "default" {
  targets = ["webapp"]
}

target "webapp" {
  dockerfile = "Dockerfile"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

HCL is the preferred format for Bake files. Aside from syntactic differences, HCL lets you use features that the JSON and YAML formats don't support.

The examples in this document use the HCL format.

## [Target](#target)

A target reflects a single `docker build` invocation. Consider the following build command:

```console
$ docker build \
  --file=Dockerfile.webapp \
  --tag=docker.io/username/webapp:latest \
  https://github.com/username/webapp
```

You can express this command in a Bake file as follows:

```hcl
target "webapp" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

The following table shows the complete list of attributes that you can assign to a target:

| Name                                            | Type    | Description                                                          |
| ----------------------------------------------- | ------- | -------------------------------------------------------------------- |
| [`args`](#targetargs)                           | Map     | Build arguments                                                      |
| [`annotations`](#targetannotations)             | List    | Exporter annotations                                                 |
| [`attest`](#targetattest)                       | List    | Build attestations                                                   |
| [`cache-from`](#targetcache-from)               | List    | External cache sources                                               |
| [`cache-to`](#targetcache-to)                   | List    | External cache destinations                                          |
| [`call`](#targetcall)                           | String  | Specify the frontend method to call for the target.                  |
| [`context`](#targetcontext)                     | String  | Set of files located in the specified path or URL                    |
| [`contexts`](#targetcontexts)                   | Map     | Additional build contexts                                            |
| [`description`](#targetdescription)             | String  | Description of a target                                              |
| [`dockerfile-inline`](#targetdockerfile-inline) | String  | Inline Dockerfile string                                             |
| [`dockerfile`](#targetdockerfile)               | String  | Dockerfile location                                                  |
| [`entitlements`](#targetentitlements)           | List    | Permissions that the build process requires to run                   |
| [`extra-hosts`](#targetextra-hosts)             | List    | Customs host-to-IP mapping                                           |
| [`inherits`](#targetinherits)                   | List    | Inherit attributes from other targets                                |
| [`labels`](#targetlabels)                       | Map     | Metadata for images                                                  |
| [`matrix`](#targetmatrix)                       | Map     | Define a set of variables that forks a target into multiple targets. |
| [`name`](#targetname)                           | String  | Override the target name when using a matrix.                        |
| [`no-cache-filter`](#targetno-cache-filter)     | List    | Disable build cache for specific stages                              |
| [`no-cache`](#targetno-cache)                   | Boolean | Disable build cache completely                                       |
| [`output`](#targetoutput)                       | List    | Output destinations                                                  |
| [`policy`](#targetpolicy)                       | List    | Policies to validate build sources and metadata                      |
| [`platforms`](#targetplatforms)                 | List    | Target platforms                                                     |
| [`pull`](#targetpull)                           | Boolean | Always pull images                                                   |
| [`resources`](#targetresources)                 | Map     | Resource limits for build containers                                 |
| [`secret`](#targetsecret)                       | List    | Secrets to expose to the build                                       |
| [`shm-size`](#targetshm-size)                   | List    | Size of `/dev/shm`                                                   |
| [`ssh`](#targetssh)                             | List    | SSH agent sockets or keys to expose to the build                     |
| [`tags`](#targettags)                           | List    | Image names and tags                                                 |
| [`target`](#targettarget)                       | String  | Target build stage                                                   |
| [`ulimits`](#targetulimits)                     | List    | Ulimit options                                                       |

### [`target.args`](#targetargs)

Use the `args` attribute to define build arguments for the target. This has the same effect as passing a [`--build-arg`](https://docs.docker.com/reference/cli/docker/image/build/#build-arg) flag to the build command.

```hcl
target "default" {
  args = {
    VERSION = "0.0.0+unknown"
  }
}
```

You can set `args` attributes to use `null` values. Doing so forces the `target` to use the `ARG` value specified in the Dockerfile.

```hcl
variable "GO_VERSION" {
  default = "1.20.3"
}

target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp"]
}

target "db" {
  args = {
    GO_VERSION = null
  }
  dockerfile = "db.Dockerfile"
  tags = ["docker.io/username/db"]
}
```

### [`target.annotations`](#targetannotations)

The `annotations` attribute lets you add annotations to images built with bake. The key takes a list of annotations, in the format of `KEY=VALUE`.

```hcl
target "default" {
  output = [{ type = "image", name = "foo" }]
  annotations = ["org.opencontainers.image.authors=dvdksn"]
}
```

By default, the annotation is added to image manifests. You can configure the level of the annotations by adding a prefix to the annotation, containing a comma-separated list of all the levels that you want to annotate. The following example adds annotations to both the image index and manifests.

```hcl
target "default" {
  output = [
    {
      type = "image"
      name = "foo"
    }
  ]
  annotations = ["index,manifest:org.opencontainers.image.authors=dvdksn"]
}
```

Read about the supported levels in [Specifying annotation levels](https://docs.docker.com/build/building/annotations/#specifying-annotation-levels).

### [`target.attest`](#targetattest)

The `attest` attribute lets you apply [build attestations](https://docs.docker.com/build/attestations/) to the target. This attribute accepts the long-form CSV version of attestation parameters.

```hcl
target "default" {
  attest = [
    {
      type = "provenance"
      mode = "max"
    },
    {
      type = "sbom"
    }
  ]
}
```

### [`target.cache-from`](#targetcache-from)

Build cache sources. The builder imports cache from the locations you specify. It uses the [Buildx cache storage backends](https://docs.docker.com/build/cache/backends/), and it works the same way as the [`--cache-from`](https://docs.docker.com/reference/cli/docker/buildx/build/#cache-from) flag. This takes a list value, so you can specify multiple cache sources.

```hcl
target "app" {
  cache-from = [
    {
      type = "s3"
      region = "eu-west-1"
      bucket = "mybucket"
    },
    {
      type = "registry"
      ref = "user/repo:cache"
    }
  ]
}
```

### [`target.cache-to`](#targetcache-to)

Build cache export destinations. The builder exports its build cache to the locations you specify. It uses the [Buildx cache storage backends](https://docs.docker.com/build/cache/backends/), and it works the same way as the [`--cache-to` flag](https://docs.docker.com/reference/cli/docker/buildx/build/#cache-to). This takes a list value, so you can specify multiple cache export targets.

```hcl
target "app" {
  cache-to = [
    {
      type = "s3"
      region = "eu-west-1"
      bucket = "mybucket"
    },
    {
      type = "inline"
    }
  ]
}
```

### [`target.call`](#targetcall)

Specifies the frontend method to use. Frontend methods let you, for example, execute build checks only, instead of running a build. This is the same as the `--call` flag.

```hcl
target "app" {
  call = "check"
}
```

Supported values are:

* `build` builds the target (default)
* `check`: evaluates [build checks](https://docs.docker.com/build/checks/) for the target
* `outline`: displays the target's build arguments and their default values if available
* `targets`: lists all Bake targets in the loaded definition, along with its [description](#targetdescription).

For more information about frontend methods, refer to the CLI reference for [`docker buildx build --call`](https://docs.docker.com/reference/cli/docker/buildx/build/#call).

### [`target.context`](#targetcontext)

Specifies the location of the build context to use for this target. Accepts a URL or a directory path. This is the same as the [build context](https://docs.docker.com/reference/cli/docker/buildx/build/#build-context) positional argument that you pass to the build command.

```hcl
target "app" {
  context = "./src/www"
}
```

This resolves to the current working directory (`"."`) by default.

```console
$ docker buildx bake --print -f - <<< 'target "default" {}'
[+] Building 0.0s (0/0)
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile"
    }
  }
}
```

### [`target.contexts`](#targetcontexts)

Additional build contexts. This is the same as the [`--build-context` flag](https://docs.docker.com/reference/cli/docker/buildx/build/#build-context). This attribute takes a map, where keys result in named contexts that you can reference in your builds.

You can specify different types of contexts, such local directories, Git URLs, and even other Bake targets. Bake automatically determines the type of a context based on the pattern of the context value.

| Context type    | Example                                   |
| --------------- | ----------------------------------------- |
| Container image | `docker-image://alpine@sha256:0123456789` |
| Git URL         | `https://github.com/user/proj.git`        |
| HTTP URL        | `https://example.com/files`               |
| Local directory | `../path/to/src`                          |
| Bake target     | `target:base`                             |

#### [Pin an image version](#pin-an-image-version)

```hcl
# docker-bake.hcl
target "app" {
  contexts = {
    alpine = "docker-image://alpine:3.13"
  }
}
```

```Dockerfile
# Dockerfile
FROM alpine
RUN echo "Hello world"
```

#### [Use a local directory](#use-a-local-directory)

```hcl
# docker-bake.hcl
target "app" {
  contexts = {
    src = "../path/to/source"
  }
}
```

```Dockerfile
# Dockerfile
FROM scratch AS src
FROM golang
COPY --from=src . .
```

#### [Use another target as base](#use-another-target-as-base)

> Note
>
> You should prefer to use regular multi-stage builds over this option. You can Use this feature when you have multiple Dockerfiles that can't be easily merged into one.

```hcl
# docker-bake.hcl
target "base" {
  dockerfile = "baseapp.Dockerfile"
}

target "app" {
  contexts = {
    baseapp = "target:base"
  }
}
```

```Dockerfile
# Dockerfile
FROM baseapp
RUN echo "Hello world"
```

### [`target.description`](#targetdescription)

Defines a human-readable description for the target, clarifying its purpose or functionality.

```hcl
target "lint" {
  description = "Runs golangci-lint to detect style errors"
  args = {
    GOLANGCI_LINT_VERSION = null
  }
  dockerfile = "lint.Dockerfile"
}
```

This attribute is useful when combined with the `docker buildx bake --list=targets` option, providing a more informative output when listing the available build targets in a Bake file.

### [`target.dockerfile-inline`](#targetdockerfile-inline)

Uses the string value as an inline Dockerfile for the build target.

```hcl
target "default" {
  dockerfile-inline = "FROM alpine\nENTRYPOINT [\"echo\", \"hello\"]"
}
```

The `dockerfile-inline` takes precedence over the `dockerfile` attribute. If you specify both, Bake uses the inline version.

### [`target.dockerfile`](#targetdockerfile)

Name of the Dockerfile to use for the build. This is the same as the [`--file` flag](https://docs.docker.com/reference/cli/docker/image/build/#file) for the `docker build` command.

```hcl
target "default" {
  dockerfile = "./src/www/Dockerfile"
}
```

Resolves to `"Dockerfile"` by default.

```console
$ docker buildx bake --print -f - <<< 'target "default" {}'
[+] Building 0.0s (0/0)
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile"
    }
  }
}
```

### [`target.entitlements`](#targetentitlements)

Entitlements are permissions that the build process requires to run.

Currently supported entitlements are:

* `network.host`: Allows the build to use commands that access the host network. In Dockerfile, use [`RUN --network=host`](https://docs.docker.com/reference/dockerfile/#run---networkhost) to run a command with host network enabled.

* `security.insecure`: Allows the build to run commands in privileged containers that are not limited by the default security sandbox. Such container may potentially access and modify system resources. In Dockerfile, use [`RUN --security=insecure`](https://docs.docker.com/reference/dockerfile/#run---security) to run a command in a privileged container.

```hcl
target "integration-tests" {
  # this target requires privileged containers to run nested containers
  entitlements = ["security.insecure"]
}
```

Entitlements are enabled with a two-step process. First, a target must declare the entitlements it requires. Secondly, when invoking the `bake` command, the user must grant the entitlements by passing the `--allow` flag or confirming the entitlements when prompted in an interactive terminal. This is to ensure that the user is aware of the possibly insecure permissions they are granting to the build process.

### [`target.extra-hosts`](#targetextra-hosts)

Use the `extra-hosts` attribute to define customs host-to-IP mapping for the target. This has the same effect as passing a [`--add-host`](https://docs.docker.com/reference/cli/docker/buildx/build/#add-host) flag to the build command.

```hcl
target "default" {
  extra-hosts = {
    my_hostname = "8.8.8.8"
  }
}
```

### [`target.inherits`](#targetinherits)

A target can inherit attributes from other targets. Use `inherits` to reference from one target to another.

In the following example, the `app-dev` target specifies an image name and tag. The `app-release` target uses `inherits` to reuse the tag name.

```hcl
variable "TAG" {
  default = "latest"
}

target "app-dev" {
  tags = ["docker.io/username/myapp:${TAG}"]
}

target "app-release" {
  inherits = ["app-dev"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

The `inherits` attribute is a list, meaning you can reuse attributes from multiple other targets. In the following example, the `app-release` target reuses attributes from both the `app-dev` and `_release` targets.

```hcl
target "app-dev" {
  args = {
    GO_VERSION = "1.20"
    BUILDX_EXPERIMENTAL = 1
  }
  tags = ["docker.io/username/myapp"]
  dockerfile = "app.Dockerfile"
  labels = {
    "org.opencontainers.image.source" = "https://github.com/username/myapp"
  }
}

target "_release" {
  args = {
    BUILDKIT_CONTEXT_KEEP_GIT_DIR = 1
    BUILDX_EXPERIMENTAL = 0
  }
}

target "app-release" {
  inherits = ["app-dev", "_release"]
  platforms = ["linux/amd64", "linux/arm64"]
}
```

When inheriting attributes from multiple targets and there's a conflict, the target that appears last in the `inherits` list takes precedence. The previous example defines the `BUILDX_EXPERIMENTAL` argument twice for the `app-release` target. It resolves to `0` because the `_release` target appears last in the inheritance chain:

```console
$ docker buildx bake --print app-release
[+] Building 0.0s (0/0)
{
  "group": {
    "default": {
      "targets": [
        "app-release"
      ]
    }
  },
  "target": {
    "app-release": {
      "context": ".",
      "dockerfile": "app.Dockerfile",
      "args": {
        "BUILDKIT_CONTEXT_KEEP_GIT_DIR": "1",
        "BUILDX_EXPERIMENTAL": "0",
        "GO_VERSION": "1.20"
      },
      "labels": {
        "org.opencontainers.image.source": "https://github.com/username/myapp"
      },
      "tags": [
        "docker.io/username/myapp"
      ],
      "platforms": [
        "linux/amd64",
        "linux/arm64"
      ]
    }
  }
}
```

### [`target.labels`](#targetlabels)

Assigns image labels to the build. This is the same as the `--label` flag for `docker build`.

```hcl
target "default" {
  labels = {
    "org.opencontainers.image.source" = "https://github.com/username/myapp"
    "com.docker.image.source.entrypoint" = "Dockerfile"
  }
}
```

It's possible to use a `null` value for labels. If you do, the builder uses the label value specified in the Dockerfile.

### [`target.matrix`](#targetmatrix)

A matrix strategy lets you fork a single target into multiple different variants, based on parameters that you specify. This works in a similar way to \[Matrix strategies for GitHub Actions]. You can use this to reduce duplication in your bake definition.

The `matrix` attribute is a map of parameter names to lists of values. Bake builds each possible combination of values as a separate target.

Each generated target **must** have a unique name. To specify how target names should resolve, use the `name` attribute.

The following example resolves the `app` target to `app-foo` and `app-bar`. It also uses the matrix value to define the [target build stage](#targettarget).

```hcl
target "app" {
  name = "app-${tgt}"
  matrix = {
    tgt = ["foo", "bar"]
  }
  target = tgt
}
```

```console
$ docker buildx bake --print app
[+] Building 0.0s (0/0)
{
  "group": {
    "app": {
      "targets": [
        "app-foo",
        "app-bar"
      ]
    },
    "default": {
      "targets": [
        "app"
      ]
    }
  },
  "target": {
    "app-bar": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "target": "bar"
    },
    "app-foo": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "target": "foo"
    }
  }
}
```

#### [Multiple axes](#multiple-axes)

You can specify multiple keys in your matrix to fork a target on multiple axes. When using multiple matrix keys, Bake builds every possible variant.

The following example builds four targets:

* `app-foo-1-0`
* `app-foo-2-0`
* `app-bar-1-0`
* `app-bar-2-0`

```hcl
target "app" {
  name = "app-${tgt}-${replace(version, ".", "-")}"
  matrix = {
    tgt = ["foo", "bar"]
    version = ["1.0", "2.0"]
  }
  target = tgt
  args = {
    VERSION = version
  }
}
```

#### [Multiple values per matrix target](#multiple-values-per-matrix-target)

If you want to differentiate the matrix on more than just a single value, you can use maps as matrix values. Bake creates a target for each map, and you can access the nested values using dot notation.

The following example builds two targets:

* `app-foo-1-0`
* `app-bar-2-0`

```hcl
target "app" {
  name = "app-${item.tgt}-${replace(item.version, ".", "-")}"
  matrix = {
    item = [
      {
        tgt = "foo"
        version = "1.0"
      },
      {
        tgt = "bar"
        version = "2.0"
      }
    ]
  }
  target = item.tgt
  args = {
    VERSION = item.version
  }
}
```

### [`target.name`](#targetname)

Specify name resolution for targets that use a matrix strategy. The following example resolves the `app` target to `app-foo` and `app-bar`.

```hcl
target "app" {
  name = "app-${tgt}"
  matrix = {
    tgt = ["foo", "bar"]
  }
  target = tgt
}
```

### [`target.network`](#targetnetwork)

Specify the network mode for the whole build request. This will override the default network mode for all the `RUN` instructions in the Dockerfile. Accepted values are `default`, `host`, and `none`.

Usually, a better approach to set the network mode for your build steps is to instead use `RUN --network=<value>` in your Dockerfile. This way, you can set the network mode for individual build steps and everyone building the Dockerfile gets consistent behavior without needing to pass additional flags to the build command.

If you set network mode to `host` in your Bake file, you must also grant `network.host` entitlement when invoking the `bake` command. This is because `host` network mode requires elevated privileges and can be a security risk. You can pass `--allow=network.host` to the `docker buildx bake` command to grant the entitlement, or you can confirm the entitlement when prompted if you are using an interactive terminal.

```hcl
target "app" {
  # make sure this build does not access internet
  network = "none"
}
```

### [`target.no-cache-filter`](#targetno-cache-filter)

Don't use build cache for the specified stages. This is the same as the `--no-cache-filter` flag for `docker build`. The following example avoids build cache for the `foo` build stage.

```hcl
target "default" {
  no-cache-filter = ["foo"]
}
```

### [`target.no-cache`](#targetno-cache)

Don't use cache when building the image. This is the same as the `--no-cache` flag for `docker build`.

```hcl
target "default" {
  no-cache = true
}
```

### [`target.output`](#targetoutput)

Configuration for exporting the build output. This is the same as the [`--output` flag](https://docs.docker.com/reference/cli/docker/buildx/build/#output). The following example configures the target to use a cache-only output,

```hcl
target "default" {
  output = [{ type = "cacheonly" }]
}
```

> Note
>
> Local outputs with `mode=delete` require granting `--allow=buildx.local.delete` when invoking `docker buildx bake`.

### [`target.policy`](#targetpolicy)

Policies to validate build sources and metadata. Each entry uses the same keys as the `--policy` flag for `docker buildx build` (`filename`, `reset`, `disabled`, `strict`, `log-level`). Bake also automatically loads `Dockerfile.rego` alongside the target Dockerfile when present.

```hcl
target "default" {
  policy = [
    { filename = "extra.rego" },
  ]
}
```

### [`target.platforms`](#targetplatforms)

Set target platforms for the build target. This is the same as the [`--platform` flag](https://docs.docker.com/reference/cli/docker/buildx/build/#platform). The following example creates a multi-platform build for three architectures.

```hcl
target "default" {
  platforms = ["linux/amd64", "linux/arm64", "linux/arm/v7"]
}
```

### [`target.pull`](#targetpull)

Configures whether the builder should attempt to pull images when building the target. This is the same as the `--pull` flag for `docker build`. The following example forces the builder to always pull all images referenced in the build target.

```hcl
target "default" {
  pull = true
}
```

### [`target.resources`](#targetresources)

Sets cgroup resource limits for the containers that run `RUN` instructions during the build. The supported keys are `memory`, `memory-swap`, `cpu-shares`, `cpu-period`, `cpu-quota`, `cpuset-cpus`, and `cpuset-mems`. These map to the equivalent `docker build` flags and to the [`--resource`](https://docs.docker.com/reference/cli/docker/buildx/build/#resource) flag for `docker buildx build`.

```hcl
target "default" {
  resources = {
    memory      = "2g"
    memory-swap = "4g"
    cpu-quota   = 50000
  }
}
```

> Note
>
> These limits require a BuildKit daemon that supports per-step resource limits and only take effect on Linux. They don't affect the build cache key.

### [`target.secret`](#targetsecret)

Defines secrets to expose to the build target. This is the same as the [`--secret` flag](https://docs.docker.com/reference/cli/docker/buildx/build/#secret).

```hcl
variable "HOME" {
  default = null
}

target "default" {
  secret = [
    {
      type = "env"
      id = "KUBECONFIG"
    },
    {
      type = "file"
      id = "aws"
      src = "${HOME}/.aws/credentials"
    }
  ]
}
```

This lets you [mount the secret](https://docs.docker.com/reference/dockerfile/#run---mounttypesecret) in your Dockerfile.

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws cloudfront create-invalidation ...
RUN --mount=type=secret,id=KUBECONFIG,env=KUBECONFIG \
    helm upgrade --install
```

### [`target.shm-size`](#targetshm-size)

Sets the size of the shared memory allocated for build containers when using `RUN` instructions.

The format is `<number><unit>`. `number` must be greater than `0`. Unit is optional and can be `b` (bytes), `k` (kilobytes), `m` (megabytes), or `g` (gigabytes). If you omit the unit, the system uses bytes.

This is the same as the `--shm-size` flag for `docker build`.

```hcl
target "default" {
  shm-size = "128m"
}
```

> Note
>
> In most cases, it is recommended to let the builder automatically determine the appropriate configurations. Manual adjustments should only be considered when specific performance tuning is required for complex build scenarios.

### [`target.ssh`](#targetssh)

Defines SSH agent sockets or keys to expose to the build. This is the same as the [`--ssh` flag](https://docs.docker.com/reference/cli/docker/buildx/build/#ssh). This can be useful if you need to access private repositories during a build.

```hcl
target "default" {
  ssh = [{ id = "default" }]
}
```

```dockerfile
FROM alpine
RUN --mount=type=ssh \
    apk add git openssh-client \
    && install -m 0700 -d ~/.ssh \
    && ssh-keyscan github.com >> ~/.ssh/known_hosts \
    && git clone git@github.com:user/my-private-repo.git
```

### [`target.tags`](#targettags)

Image names and tags to use for the build target. This is the same as the [`--tag` flag](https://docs.docker.com/reference/cli/docker/image/build/#tag).

```hcl
target "default" {
  tags = [
    "org/repo:latest",
    "myregistry.azurecr.io/team/image:v1"
  ]
}
```

### [`target.target`](#targettarget)

Set the target build stage to build. This is the same as the [`--target` flag](https://docs.docker.com/reference/cli/docker/image/build/#target).

```hcl
target "default" {
  target = "binaries"
}
```

### [`target.ulimits`](#targetulimits)

Ulimits overrides the default ulimits of build's containers when using `RUN` instructions and are specified with a soft and hard limit as such: `<type>=<soft limit>[:<hard limit>]`, for example:

```hcl
target "app" {
  ulimits = [
    "nofile=1024:1024"
  ]
}
```

> Note
>
> If you do not provide a `hard limit`, the `soft limit` is used for both values. If no `ulimits` are set, they are inherited from the default `ulimits` set on the daemon.

> Note
>
> In most cases, it is recommended to let the builder automatically determine the appropriate configurations. Manual adjustments should only be considered when specific performance tuning is required for complex build scenarios.

## [Group](#group)

Groups allow you to invoke multiple builds (targets) at once.

```hcl
group "default" {
  targets = ["db", "webapp-dev"]
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
}

target "db" {
  dockerfile = "Dockerfile.db"
  tags = ["docker.io/username/db"]
}
```

Groups take precedence over targets, if both exist with the same name. The following bake file builds the `default` group. Bake ignores the `default` target.

```hcl
target "default" {
  dockerfile-inline = "FROM ubuntu"
}

group "default" {
  targets = ["alpine", "debian"]
}
target "alpine" {
  dockerfile-inline = "FROM alpine"
}
target "debian" {
  dockerfile-inline = "FROM debian"
}
```

## [Variable](#variable)

The HCL file format supports variable block definitions. You can use variables as build arguments in your Dockerfile, or interpolate them in attribute values in your Bake file.

```hcl
variable "TAG" {
  type = string
  default = "latest"
  description = "Tag to use for build"
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:${TAG}"]
}
```

You can assign a default value for a variable in the Bake file, or assign a `null` value to it. If you assign a `null` value, Buildx uses the default value from the Dockerfile instead.

You can also add a description of the variable's purpose with the `description` field. This attribute is useful when combined with the `docker buildx bake --list=variables` option, providing a more informative output when listing the available variables in a Bake file.

You can override variable defaults set in the Bake file using environment variables. The following example sets the `TAG` variable to `dev`, overriding the default `latest` value shown in the previous example.

```console
$ TAG=dev docker buildx bake webapp-dev
```

Variables can also be assigned an explicit type. If provided, it will be used to validate the default value (if set), as well as any overrides. This is particularly useful when using complex types which are intended to be overridden. The previous example could be expanded to apply an arbitrary series of tags.

```hcl
variable "TAGS" {
  default = ["latest"]
  type = list(string)
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = [for tag in TAGS: "docker.io/username/webapp:${tag}"]
}
```

This example shows how to generate three tags without changing the file or using custom functions/parsing:

```console
$ TAGS=dev,latest,2 docker buildx bake webapp-dev
```

### [Variable typing](#variable-typing)

The following primitive types are available:

* `string`
* `number`
* `bool`

The type is expressed like a keyword; it must be expressed as a literal:

```hcl
variable "OK" {
  type = string
}

# cannot be an actual string
variable "BAD" {
  type = "string"
}

# cannot be the result of an expression
variable "ALSO_BAD" {
  type = lower("string")
}
```

Specifying primitive types can be valuable to show intent (especially when a default is not provided), but bake will generally behave as expected without explicit typing.

Complex types are expressed with "type constructors"; they are:

* `tuple([<type>,...])`
* `list(<type>)`
* `set(<type>)`
* `map(<type>)`
* `object({<attr>=<type>},...})`

The following are examples of each of those, as well as how the (optional) default value would be expressed:

```hcl
# structured way to express "1.2.3-alpha"
variable "MY_VERSION" {
  type = tuple([number, number, number, string])
  default = [1, 2, 3, "alpha"]
}

# JDK versions used in a matrix build
variable "JDK_VERSIONS" {
  type = list(number)
  default = [11, 17, 21]
}

# better way to express the previous example; this will also
# enforce set semantics and allow use of set-based functions
variable "JDK_VERSIONS" {
  type = set(number)
  default = [11, 17, 21]
}

# with the help of lookup(), translate a 'feature' to a tag
variable "FEATURE_TO_NAME" {
  type = map(string)
  default = {featureA = "slim", featureB = "tiny"}
}

# map a branch name to a registry location
variable "PUSH_DESTINATION" {
  type = object({branch = string, registry = string})
  default = {branch = "main", registry = "prod-registry.invalid.com"}
}

# make the previous example more useful with composition
variable "PUSH_DESTINATIONS" {
  type = list(object({branch = string, registry = string}))
  default = [
    {branch = "develop", registry = "test-registry.invalid.com"},
    {branch = "main", registry = "prod-registry.invalid.com"},
  ]
}
```

Note that in each example, the default value would be valid even if typing was not present. If typing was omitted, the first three would all be considered `tuple`; you would be restricted to functions that operate on `tuple` and, for example, not be able to add elements. Similarly, the third and fourth would both be considered `object`, with the limits and semantics of that type. In short, in the absence of a type, any value delimited with `[]` is a `tuple` and value delimited with `{}` is an `object`. Explicit typing for complex types not only opens up the ability to use functions applicable to that specialized type, but is also a precondition for providing overrides.

> Note
>
> See [HCL Type Expressions](https://github.com/hashicorp/hcl/tree/main/ext/typeexpr) page for more details.

### [Overriding variables](#overriding-variables)

As mentioned in the [intro to variables](#variable), primitive types (`string`, `number`, and `bool`) can be overridden without typing and will generally behave as expected. (When explicit typing is not provided, a variable is assumed to be primitive when the default value lacks `{}` or `[]` delimiters; a variable with neither typing nor a default value is treated as `string`.) Naturally, these same overrides can be used alongside explicit typing too; they may help in edge cases where you want `VAR=true` to be a `string`, where without typing, it may be a `string` or a `bool` depending on how/where it's used. Overriding a variable with a complex type can only be done when the type is provided. This is still done via environment variables, but the values can be provided via CSV or JSON.

#### [CSV overrides](#csv-overrides)

This is considered the canonical method and is well suited to interactive usage. It is assumed that `list` and `set` will be the most common complex type, as well as the most common complex type designed to be overridden. Thus, there is full CSV support for `list` and `set` (and `tuple`; despite being considered a structural type, it is more like a collection type in this regard).

There is limited support for `map` and `object` and no support for composite types; for these advanced cases, an alternative mechanism [using JSON](#json-overrides) is available.

#### [JSON overrides](#json-overrides)

Overrides can also be provided via JSON. This is the only method available for providing some complex types and may be convenient if overrides are already JSON (for example, if they come from a JSON API). It can also be used when dealing with values are difficult or impossible to specify using CSV (e.g., values containing quotes or commas). To use JSON, simply append `_JSON` to the variable name. In this contrived example, CSV cannot handle the second value; despite being a supported CSV type, JSON must be used:

```hcl
variable "VALS" {
  type = list(string)
  default = ["some", "list"]
}
```

```console
$ cat data.json
["hello","with,comma","with\"quote"]
$ VALS_JSON=$(< data.json) docker buildx bake

# CSV equivalent, though the second value cannot be expressed at all 
$ VALS='hello,"with""quote"' docker buildx bake
```

This example illustrates some precedence and usage rules:

```hcl
variable "FOO" {
  type = string
  default = "foo"
}

variable "FOO_JSON" {
  type = string
  default = "foo"
}
```

The variable `FOO` can *only* be overridden using CSV because `FOO_JSON`, which would typically used for a JSON override, is already a defined variable. Since `FOO_JSON` is an actual variable, setting that environment variable would be expected to a CSV value. A JSON override *is* possible for this variable, using environment variable `FOO_JSON_JSON`.

```Console
# These three are all equivalent, setting variable FOO=bar
$ FOO=bar docker buildx bake <...>
$ FOO='bar' docker buildx bake <...>
$ FOO="bar" docker buildx bake <...>

# Sets *only* variable FOO_JSON; FOO is untouched
$ FOO_JSON=bar docker buildx bake <...>

# This also sets FOO_JSON, but will fail due to not being valid JSON
$ FOO_JSON_JSON=bar docker buildx bake <...>

# These are all equivalent
$ cat data.json
"bar"
$ FOO_JSON_JSON=$(< data.json) docker buildx bake <...>
$ FOO_JSON_JSON='"bar"' docker buildx bake <...>
$ FOO_JSON=bar docker buildx bake <...>

# This results in setting two different variables, both specified as CSV (FOO=bar and FOO_JSON="baz")
$ FOO=bar FOO_JSON='"baz"' docker buildx bake <...>

# These refer to the same variable with FOO_JSON_JSON having precedence and read as JSON (FOO_JSON=baz)
$ FOO_JSON=bar FOO_JSON_JSON='"baz"' docker buildx bake <...>
```

### [Built-in variables](#built-in-variables)

The following variables are built-ins that you can use with Bake without having to define them.

| Variable              | Description                                                                         |
| --------------------- | ----------------------------------------------------------------------------------- |
| `BAKE_CMD_CONTEXT`    | Holds the main context when building using a remote Bake file.                      |
| `BAKE_LOCAL_PLATFORM` | Returns the current platform’s default platform specification (e.g. `linux/amd64`). |

### [Use environment variable as default](#use-environment-variable-as-default)

If an environment variable exists with the same name as a declared Bake variable, Bake uses that environment variable value instead of the declared default.

To disable this environment-based variable lookup, set `BUILDX_BAKE_DISABLE_VARS_ENV_LOOKUP=1`.

```hcl
variable "HOME" {
  default = "/root"
}
```

### [Interpolate variables into attributes](#interpolate-variables-into-attributes)

To interpolate a variable into an attribute string value, you must use curly brackets. The following doesn't work:

```hcl
variable "HOME" {
  default = "$HOME"
}

target "default" {
  ssh = ["default=$HOME/.ssh/id_rsa"]
}
```

Wrap the variable in curly brackets where you want to insert it:

```diff
  variable "HOME" {
    default = "$HOME"
  }

  target "default" {
-   ssh = ["default=$HOME/.ssh/id_rsa"]
+   ssh = ["default=${HOME}/.ssh/id_rsa"]
  }
```

Before you can interpolate a variable into an attribute, first you must declare it in the bake file, as demonstrated in the following example.

```console
$ cat docker-bake.hcl
target "default" {
  dockerfile-inline = "FROM ${BASE_IMAGE}"
}
$ docker buildx bake
[+] Building 0.0s (0/0)
docker-bake.hcl:2
--------------------
   1 |     target "default" {
   2 | >>>   dockerfile-inline = "FROM ${BASE_IMAGE}"
   3 |     }
   4 |
--------------------
ERROR: docker-bake.hcl:2,31-41: Unknown variable; There is no variable named "BASE_IMAGE"., and 1 other diagnostic(s)
$ cat >> docker-bake.hcl

variable "BASE_IMAGE" {
  default = "alpine"
}

$ docker buildx bake
[+] Building 0.6s (5/5) FINISHED
```

## [Function](#function)

A [set of general-purpose functions](https://github.com/docker/buildx/blob/master/docs/bake-stdlib.md) provided by [go-cty](https://github.com/zclconf/go-cty/tree/main/cty/function/stdlib) are available for use in HCL files:

```hcl
# docker-bake.hcl
target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    buildno = "${add(123, 1)}"
  }
}
```

In addition, [user defined functions](https://github.com/hashicorp/hcl/tree/main/ext/userfunc) are also supported:

```hcl
# docker-bake.hcl
function "increment" {
  params = [number]
  result = number + 1
}

target "webapp-dev" {
  dockerfile = "Dockerfile.webapp"
  tags = ["docker.io/username/webapp:latest"]
  args = {
    buildno = "${increment(123)}"
  }
}
```

> Note
>
> See [User defined HCL functions](https://docs.docker.com/build/bake/hcl-funcs/) page for more details.

----
url: https://docs.docker.com/reference/api/engine/version/v1.52.yaml
----

basePath: "/v1.52"
info:
 title: "Docker Engine API"
 version: "1.52"

 items:
 type: "string"
 example:
 \- "example@sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb"
 \- "internal.registry.example.com:5000/example@sha256:b69959407d21e8a062e0416bf13405bb2b71ed7a84dde4158ebafacfa06f5578"
 Comment:
 description: \|
 Optional message that was set when committing or importing the image.
 type: "string"
 x-nullable: true
 example: ""
 Created:
 description: \|
 Date and time at which the image was created, formatted in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.

 This information is only available if present in the image,
 and omitted otherwise.
 type: "string"
 format: "dateTime"
 x-nullable: true
 example: "2022-02-04T21:20:12.497794809Z"
 Author:
 description: \|
 Name of the author that was specified when committing the image, or as
 specified through MAINTAINER (deprecated) in the Dockerfile.
 type: "string"
 x-nullable: true
 example: ""
 Config:
 $ref: "#/definitions/ImageConfig"
 Architecture:
 description: \|
 Hardware CPU architecture that the image runs on.
 type: "string"
 x-nullable: false
 example: "arm"
 Variant:
 description: \|
 CPU architecture variant (presently ARM-only).
 type: "string"
 x-nullable: true
 example: "v7"
 Os:
 description: \|
 Operating System the image is built to run on.
 type: "string"
 x-nullable: false
 example: "linux"
 OsVersion:
 description: \|
 Operating System version the image is built to run on (especially
 for Windows).
 type: "string"
 example: ""
 x-nullable: true
 Size:
 description: \|
 Total size of the image including all layers it is composed of.
 type: "integer"
 format: "int64"
 x-nullable: false
 example: 1239828
 GraphDriver:
 x-nullable: true


 ImagesDiskUsage:
 type: "object"
 x-go-name: "DiskUsage"
 x-go-package: "github.com/moby/moby/api/types/image"
 description: \|
 represents system data usage for image resources.
 properties:
 ActiveCount:
 description: \|
 Count of active images.
 type: "integer"
 format: "int64"
 example: 1
 TotalCount:
 description: \|
 Count of all images.
 type: "integer"
 format: "int64"
 example: 4
 Reclaimable:
 description: \|
 Disk space that can be reclaimed by removing unused images.
 type: "integer"
 format: "int64"
 example: 12345678
 TotalSize:
 description: \|
 Disk space in use by images.
 type: "integer"
 format: "int64"
 example: 98765432
 Items:
 description: \|
 List of image summaries.
 type: "array"
 x-omitempty: true
 items:
 x-go-type:
 type: Summary

 AuthConfig:
 type: "object"
 properties:
 username:
 type: "string"
 password:
 type: "string"
 serveraddress:
 type: "string"
 example:
 username: "hannibal"
 password: "xxxx"
 serveraddress: "https://index.docker.io/v1/"

 AuthResponse:
 description: \|
 An identity token was generated successfully.
 type: "object"
 required: \[Status\]
 properties:
 Status:
 description: "The status of the authentication"
 type: "string"
 example: "Login Succeeded"
 x-nullable: false
 IdentityToken:
 description: "An opaque token used to authenticate a user after a successful login"
 type: "string"
 example: "9cbaf023786cd7..."
 x-nullable: false

 ProcessConfig:
 type: "object"
 properties:
 privileged:
 type: "boolean"
 user:
 type: "string"
 tty:
 type: "boolean"
 entrypoint:
 type: "string"
 arguments:
 type: "array"
 items:
 type: "string"

 Volume:
 type: "object"
 required: \[Name, Driver, Mountpoint, Labels, Scope, Options\]
 x-nullable: false

 VolumesDiskUsage:
 type: "object"
 x-go-name: "DiskUsage"
 x-go-package: "github.com/moby/moby/api/types/volume"
 description: \|
 represents system data usage for volume resources.
 properties:
 ActiveCount:
 description: \|
 Count of active volumes.
 type: "integer"
 format: "int64"
 example: 1
 TotalCount:
 description: \|
 Count of all volumes.
 type: "integer"
 format: "int64"
 example: 4
 Reclaimable:
 description: \|
 Disk space that can be reclaimed by removing inactive volumes.
 type: "integer"
 format: "int64"
 example: 12345678
 TotalSize:
 description: \|
 Disk space in use by volumes.
 type: "integer"
 format: "int64"
 example: 98765432
 Items:
 description: \|
 List of volumes.
 type: "array"
 x-omitempty: true
 items:
 x-go-type:
 type: Volume

 VolumeCreateRequest:
 description: "Volume configuration"
 type: "object"
 title: "VolumeConfig"
 x-go-name: "CreateRequest"

 x-omitempty: false
 Id:
 description: \|
 ID that uniquely identifies a network on a single machine.
 type: "string"
 x-go-name: "ID"
 x-omitempty: false
 x-omitempty: false
 x-go-type:
 type: Time
 import:
 package: time
 hints:
 nullable: false
 example: "2016-10-19T04:33:30.360899459Z"
 Scope:
 description: \|
 The level at which the network exists (e.g. \`swarm\` for cluster-wide
 or \`local\` for machine level)
 type: "string"
 x-omitempty: false
 example: "local"
 Driver:
 description: \|
 The name of the driver used to create the network (e.g. \`bridge\`,
 \`overlay\`).
 type: "string"
 x-omitempty: false
 example: "overlay"
 EnableIPv4:
 description: \|
 Whether the network was created with IPv4 enabled.
 type: "boolean"
 x-omitempty: false
 example: true
 EnableIPv6:
 description: \|
 Whether the network was created with IPv6 enabled.
 type: "boolean"
 x-omitempty: false
 example: false
 IPAM:
 description: \|
 The network's IP Address Management.
 $ref: "#/definitions/IPAM"
 x-nullable: false
 x-omitempty: false
 Internal:
 description: \|
 Whether the network is created to only allow internal networking
 connectivity.
 type: "boolean"
 x-nullable: false
 x-omitempty: false
 x-nullable: false
 x-omitempty: false
 default: false
 example: false
 Ingress:
 description: \|
 Whether the network is providing the routing-mesh for the swarm cluster.
 type: "boolean"
 x-nullable: false
 x-omitempty: false
 default: false
 example: false
 ConfigFrom:
 $ref: "#/definitions/ConfigReference"
 x-nullable: false
 x-omitempty: false
 x-omitempty: false
 x-nullable: false
 default: false
 Options:
 description: \|
 Network-specific options uses when creating the network.
 type: "object"
 x-omitempty: false
 description: \|
 Metadata specific to the network being created.
 type: "object"
 x-omitempty: false
 x-omitempty: true
 items:
 $ref: "#/definitions/PeerInfo"

 NetworkSummary:
 description: "Network list response item"
 x-go-name: Summary
 type: "object"
 allOf:
 \- $ref: "#/definitions/Network"

 NetworkInspect:
 description: 'The body of the "get network" http response message.'
 x-go-name: Inspect
 type: "object"
 allOf:
 \- $ref: "#/definitions/Network"
 properties:
 Containers:
 description: \|
 Contains endpoints attached to the network.
 type: "object"
 x-omitempty: false
 additionalProperties:
 $ref: "#/definitions/EndpointResource"
 Services:
 description: \|
 List of services using the network. This field is only present for
 swarm scope networks, and omitted for local scope networks.
 type: "object"
 x-omitempty: true
 additionalProperties:
 x-go-type:
 type: ServiceInfo
 hints:
 nullable: false
 Status:
 description: >
 provides runtime information about the network
 such as the number of allocated IPs.
 $ref: "#/definitions/NetworkStatus"

 NetworkStatus:
 description: >
 provides runtime information about the network
 such as the number of allocated IPs.
 type: "object"
 x-go-name: Status
 properties:
 IPAM:
 $ref: "#/definitions/IPAMStatus"

 ServiceInfo:
 x-nullable: false
 x-omitempty: false
 description: >
 represents service parameters with the list of service's tasks
 type: "object"
 properties:
 VIP:
 type: "string"
 x-omitempty: false
 x-go-type:
 type: Addr
 import:
 package: net/netip
 Ports:
 type: "array"
 x-omitempty: false
 items:
 type: "string"
 LocalLBIndex:
 type: "integer"
 format: "int"
 x-omitempty: false
 x-go-type:
 type: int
 Tasks:
 type: "array"
 x-omitempty: false
 items:
 $ref: "#/definitions/NetworkTaskInfo"

 NetworkTaskInfo:
 x-nullable: false
 x-omitempty: false
 x-go-name: Task
 description: >
 carries the information about one backend task
 type: "object"
 properties:
 Name:
 type: "string"
 x-omitempty: false
 EndpointID:
 type: "string"
 x-omitempty: false
 EndpointIP:
 type: "string"
 x-omitempty: false
 x-go-type:
 type: Addr
 import:
 package: net/netip
 Info:
 type: "object"
 x-omitempty: false
 additionalProperties:
 type: "string"

 ConfigReference:
 x-nullable: false
 x-omitempty: false
 x-omitempty: false
 example: "config\_only\_network\_01"

 IPAM:
 type: "object"
 x-nullable: false
 x-omitempty: false

 IPAMStatus:
 type: "object"
 x-nullable: false
 x-omitempty: false
 properties:
 Subnets:
 type: "object"
 additionalProperties:
 $ref: "#/definitions/SubnetStatus"
 example:
 "172.16.0.0/16":
 IPsInUse: 3
 DynamicIPsAvailable: 65533
 "2001:db8:abcd:0012::0/96":
 IPsInUse: 5
 DynamicIPsAvailable: 4294967291
 x-go-type:
 type: SubnetStatuses
 kind: map

 SubnetStatus:
 type: "object"
 x-nullable: false
 x-omitempty: false
 properties:
 IPsInUse:
 description: >
 Number of IP addresses in the subnet that are in use or reserved and
 are therefore unavailable for allocation, saturating at 264 \- 1.
 type: integer
 format: uint64
 x-omitempty: false
 DynamicIPsAvailable:
 description: >
 Number of IP addresses within the network's IPRange for the subnet
 that are available for allocation, saturating at 264 \- 1.
 type: integer
 format: uint64
 x-omitempty: false

 EndpointResource:
 type: "object"
 description: >
 contains network resources allocated and used for a
 container in a network.
 properties:
 Name:
 type: "string"
 x-omitempty: false
 example: "container\_1"
 EndpointID:
 type: "string"
 x-omitempty: false
 example: "628cadb8bcb92de107b2a1e516cbffe463e321f548feb37697cce00ad694f21a"
 MacAddress:
 type: "string"
 x-omitempty: false
 example: "02:42:ac:13:00:02"
 x-go-type:
 type: HardwareAddr
 IPv4Address:
 type: "string"
 x-omitempty: false
 example: "172.19.0.2/16"
 x-go-type:
 type: Prefix
 import:
 package: net/netip
 IPv6Address:
 type: "string"
 x-omitempty: false
 example: ""
 x-go-type:
 type: Prefix
 import:
 package: net/netip

 PeerInfo:
 description: >
 represents one peer of an overlay network.
 type: "object"
 x-nullable: false
 properties:
 Name:
 description:
 ID of the peer-node in the Swarm cluster.
 type: "string"
 x-omitempty: false
 example: "6869d7c1732b"
 IP:
 description:
 IP-address of the peer-node in the Swarm cluster.
 type: "string"
 x-omitempty: false
 example: "10.133.77.91"
 x-go-type:
 type: Addr
 import:
 package: net/netip

 NetworkCreateResponse:
 description: "OK response to NetworkCreate operation"
 type: "object"
 title: "NetworkCreateResponse"
 x-go-name: "CreateResponse"
 required: \[Id, Warning\]
 properties:
 Id:
 description: "The ID of the created network."
 type: "string"
 x-nullable: false
 example: "b5c4fc71e8022147cd25de22b22173de4e3b170134117172eb595cb91b4e7e5d"
 Warning:
 description: "Warnings encountered when creating the container"
 type: "string"
 x-nullable: false
 example: ""

 BuildInfo:
 type: "object"
 properties:
 id:
 type: "string"
 stream:
 type: "string"
 errorDetail:
 $ref: "#/definitions/ErrorDetail"
 status:
 type: "string"
 progressDetail:
 $ref: "#/definitions/ProgressDetail"
 aux:
 $ref: "#/definitions/ImageID"

 BuildCache:
 type: "object"
 description: \|
 BuildCache contains information about a build cache record.
 properties:
 ID:
 type: "string"
 description: \|
 Unique ID of the build cache record.
 example: "ndlpt0hhvkqcdfkputsk4cq9c"
 Type:
 type: "string"
 description: \|
 Cache record type.
 example: "regular"
 # see https://github.com/moby/buildkit/blob/fce4a32258dc9d9664f71a4831d5de10f0670677/client/diskusage.go#L75-L84
 enum:
 \- "internal"
 \- "frontend"
 \- "source.local"
 \- "source.git.checkout"
 \- "exec.cachemount"
 \- "regular"
 Description:
 type: "string"
 description: \|
 Description of the build-step that produced the build cache.
 example: "mount / from exec /bin/sh -c echo 'Binary::apt::APT::Keep-Downloaded-Packages \\"true\\";' > /etc/apt/apt.conf.d/keep-cache"
 InUse:
 type: "boolean"
 description: \|
 Indicates if the build cache is in use.
 example: false
 Shared:
 type: "boolean"
 description: \|
 Indicates if the build cache is shared.
 example: true
 Size:
 description: \|
 Amount of disk space used by the build cache (in bytes).
 type: "integer"
 example: 51
 CreatedAt:
 description: \|
 Date and time at which the build cache was created in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 example: "2016-08-18T10:44:24.496525531Z"
 LastUsedAt:
 description: \|
 Date and time at which the build cache was last used in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 x-nullable: true
 example: "2017-08-09T07:09:37.632105588Z"
 UsageCount:
 type: "integer"
 example: 26

 BuildCacheDiskUsage:
 type: "object"
 x-go-name: "DiskUsage"
 x-go-package: "github.com/moby/moby/api/types/build"
 description: \|
 represents system data usage for build cache resources.
 properties:
 ActiveCount:
 description: \|
 Count of active build cache records.
 type: "integer"
 format: "int64"
 example: 1
 TotalCount:
 description: \|
 Count of all build cache records.
 type: "integer"
 format: "int64"
 example: 4
 Reclaimable:
 description: \|
 Disk space that can be reclaimed by removing inactive build cache records.
 type: "integer"
 format: "int64"
 example: 12345678
 TotalSize:
 description: \|
 Disk space in use by build cache records.
 type: "integer"
 format: "int64"
 example: 98765432
 Items:
 description: \|
 List of build cache records.
 type: "array"
 x-omitempty: true
 items:
 x-go-type:
 type: CacheRecord

 ImageID:
 type: "object"
 description: "Image ID or Digest"
 properties:
 ID:
 type: "string"
 example:
 ID: "sha256:85f05633ddc1c50679be2b16a0479ab6f7637f8884e0cfe0f4d20e1ebb3d6e7c"

 CreateImageInfo:
 type: "object"
 properties:
 id:
 type: "string"
 errorDetail:
 $ref: "#/definitions/ErrorDetail"
 status:
 type: "string"
 progressDetail:
 $ref: "#/definitions/ProgressDetail"

 PushImageInfo:
 type: "object"
 properties:
 errorDetail:
 $ref: "#/definitions/ErrorDetail"
 status:
 type: "string"
 progressDetail:
 $ref: "#/definitions/ProgressDetail"

 DeviceInfo:
 type: "object"
 description: \|
 DeviceInfo represents a device that can be used by a container.
 properties:
 Source:
 type: "string"
 example: "cdi"
 description: \|
 The origin device driver.
 ID:
 type: "string"
 example: "vendor.com/gpu=0"
 description: \|
 The unique identifier for the device within its source driver.
 For CDI devices, this would be an FQDN like "vendor.com/gpu=0".

 ErrorDetail:
 type: "object"
 properties:
 code:
 type: "integer"
 message:
 type: "string"

 ProgressDetail:
 type: "object"
 properties:
 current:
 type: "integer"
 total:
 type: "integer"

 ErrorResponse:
 description: "Represents an error."
 type: "object"
 required: \["message"\]
 properties:
 message:
 description: "The error message."
 type: "string"
 x-nullable: false
 example:
 message: "Something went wrong."

 IDResponse:
 description: "Response to an API call that returns just an Id"
 type: "object"
 x-go-name: "IDResponse"
 required: \["Id"\]
 properties:
 Id:
 description: "The id of the newly created object."
 type: "string"
 x-nullable: false

 NetworkConnectRequest:
 description: \|
 NetworkConnectRequest represents the data to be used to connect a container to a network.
 type: "object"
 x-go-name: "ConnectRequest"
 required: \["Container"\]
 properties:
 Container:
 type: "string"
 description: "The ID or name of the container to connect to the network."
 x-nullable: false
 example: "3613f73ba0e4"
 EndpointConfig:
 $ref: "#/definitions/EndpointSettings"
 x-nullable: true

 NetworkDisconnectRequest:
 description: \|
 NetworkDisconnectRequest represents the data to be used to disconnect a container from a network.
 type: "object"
 x-go-name: "DisconnectRequest"
 required: \["Container"\]
 properties:
 Container:
 type: "string"
 description: "The ID or name of the container to disconnect from the network."
 x-nullable: false
 example: "3613f73ba0e4"
 Force:
 type: "boolean"
 description: "Force the container to disconnect from the network."
 default: false
 x-nullable: false
 x-omitempty: false
 example: false

 EndpointSettings:
 description: "Configuration for a network endpoint."
 type: "object"
 properties:
 # Configurations
 IPAMConfig:
 $ref: "#/definitions/EndpointIPAMConfig"
 Links:
 type: "array"
 items:
 type: "string"
 example:
 \- "container\_1"
 \- "container\_2"
 MacAddress:
 description: \|
 MAC address for the endpoint on this network. The network driver might ignore this parameter.
 type: "string"
 example: "02:42:ac:11:00:04"
 x-go-type:
 type: HardwareAddr
 Aliases:
 type: "array"
 items:
 type: "string"
 example:
 \- "server\_x"
 \- "server\_y"
 DriverOpts:
 description: \|
 DriverOpts is a mapping of driver options and values. These options
 are passed directly to the driver and are driver specific.
 type: "object"
 x-nullable: true
 additionalProperties:
 type: "string"
 example:
 com.example.some-label: "some-value"
 com.example.some-other-label: "some-other-value"
 GwPriority:
 description: \|
 This property determines which endpoint will provide the default
 gateway for a container. The endpoint with the highest priority will
 be used. If multiple endpoints have the same priority, endpoints are
 lexicographically sorted based on their network name, and the one
 that sorts first is picked.
 type: "integer"
 format: "int64"
 example:
 \- 10

 # Operational data
 NetworkID:
 description: \|
 Unique ID of the network.
 type: "string"
 example: "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a"
 EndpointID:
 description: \|
 Unique ID for the service endpoint in a Sandbox.
 type: "string"
 example: "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b"
 Gateway:
 description: \|
 Gateway address for this network.
 type: "string"
 example: "172.17.0.1"
 IPAddress:
 description: \|
 IPv4 address.
 type: "string"
 example: "172.17.0.4"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 IPPrefixLen:
 description: \|
 Mask length of the IPv4 address.
 type: "integer"
 example: 16
 IPv6Gateway:
 description: \|
 IPv6 gateway address.
 type: "string"
 example: "2001:db8:2::100"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 GlobalIPv6Address:
 description: \|
 Global IPv6 address.
 type: "string"
 example: "2001:db8::5689"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 GlobalIPv6PrefixLen:
 description: \|
 Mask length of the global IPv6 address.
 type: "integer"
 format: "int64"
 example: 64
 DNSNames:
 description: \|
 List of all DNS names an endpoint has on a specific network. This
 list is based on the container name, network aliases, container short
 ID, and hostname.

 These DNS names are non-fully qualified but can contain several dots.
 You can get fully qualified DNS names by appending \`.\`.
 For instance, if container name is \`my.ctr\` and the network is named
 \`testnet\`, \`DNSNames\` will contain \`my.ctr\` and the FQDN will be
 \`my.ctr.testnet\`.
 type: array
 items:
 type: string
 example: \["foobar", "server\_x", "server\_y", "my.ctr"\]

 EndpointIPAMConfig:
 description: \|
 EndpointIPAMConfig represents an endpoint's IPAM configuration.
 type: "object"
 x-nullable: true
 properties:
 IPv4Address:
 type: "string"
 example: "172.20.30.33"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 IPv6Address:
 type: "string"
 example: "2001:db8:abcd::3033"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 LinkLocalIPs:
 type: "array"
 items:
 type: "string"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 example:
 \- "169.254.34.68"
 \- "fe80::3468"

 PluginMount:
 type: "object"
 x-go-name: "Mount"
 x-nullable: false
 required: \[Name, Description, Settable, Source, Destination, Type, Options\]
 properties:
 Name:
 type: "string"
 x-nullable: false
 example: "some-mount"
 Description:
 type: "string"
 x-nullable: false
 example: "This is a mount that's used by the plugin."
 Settable:
 type: "array"
 items:
 type: "string"
 Source:
 type: "string"
 example: "/var/lib/docker/plugins/"
 Destination:
 type: "string"
 x-nullable: false
 example: "/mnt/state"
 Type:
 type: "string"
 x-nullable: false
 example: "bind"
 Options:
 type: "array"
 items:
 type: "string"
 example:
 \- "rbind"
 \- "rw"

 PluginDevice:
 type: "object"
 x-go-name: "Device"
 required: \[Name, Description, Settable, Path\]
 x-nullable: false
 properties:
 Name:
 type: "string"
 x-nullable: false
 Description:
 type: "string"
 x-nullable: false
 Settable:
 type: "array"
 items:
 type: "string"
 Path:
 type: "string"
 example: "/dev/fuse"

 PluginEnv:
 type: "object"
 x-go-name: "Env"
 x-nullable: false
 required: \[Name, Description, Settable, Value\]
 properties:
 Name:
 x-nullable: false
 type: "string"
 Description:
 x-nullable: false
 type: "string"
 Settable:
 type: "array"
 items:
 type: "string"
 Value:
 type: "string"

 PluginPrivilege:
 description: \|
 Describes a permission the user has to accept upon installing
 the plugin.
 type: "object"
 x-go-name: "Privilege"
 properties:
 Name:
 type: "string"
 example: "network"
 Description:
 type: "string"
 Value:
 type: "array"
 items:
 type: "string"
 example:
 \- "host"

 Plugin:
 description: "A plugin for the Engine API"
 type: "object"
 x-go-name: "Plugin"
 required: \[Settings, Enabled, Config, Name\]
 properties:
 Id:
 type: "string"
 example: "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078"
 Name:
 type: "string"
 x-nullable: false
 example: "tiborvass/sample-volume-plugin"
 Enabled:
 description:
 True if the plugin is running. False if the plugin is not running,
 only installed.
 type: "boolean"
 x-nullable: false
 example: true
 Settings:
 description: "user-configurable settings for the plugin."
 type: "object"
 x-go-name: "Settings"
 x-nullable: false
 required: \[Args, Devices, Env, Mounts\]
 properties:
 Mounts:
 type: "array"
 items:
 $ref: "#/definitions/PluginMount"
 Env:
 type: "array"
 items:
 type: "string"
 example:
 \- "DEBUG=0"
 Args:
 type: "array"
 items:
 type: "string"
 Devices:
 type: "array"
 items:
 $ref: "#/definitions/PluginDevice"
 PluginReference:
 description: "plugin remote reference used to push/pull the plugin"
 type: "string"
 x-go-name: "PluginReference"
 x-nullable: false
 example: "localhost:5000/tiborvass/sample-volume-plugin:latest"
 Config:
 description: "The config of a plugin."
 type: "object"
 x-go-name: "Config"
 x-nullable: false
 required:
 \- Description
 \- Documentation
 \- Interface
 \- Entrypoint
 \- WorkDir
 \- Network
 \- Linux
 \- PidHost
 \- PropagatedMount
 \- IpcHost
 \- Mounts
 \- Env
 \- Args
 properties:
 Description:
 type: "string"
 x-nullable: false
 example: "A sample volume plugin for Docker"
 Documentation:
 type: "string"
 x-nullable: false
 example: "https://docs.docker.com/engine/extend/plugins/"
 Interface:
 description: "The interface between Docker and the plugin"
 x-nullable: false
 type: "object"
 x-go-name: "Interface"
 required: \[Types, Socket\]
 properties:
 Types:
 type: "array"
 items:
 type: "string"
 x-go-type:
 type: "CapabilityID"
 example:
 \- "docker.volumedriver/1.0"
 Socket:
 type: "string"
 x-nullable: false
 example: "plugins.sock"
 ProtocolScheme:
 type: "string"
 example: "some.protocol/v1.0"
 description: "Protocol to use for clients connecting to the plugin."
 enum:
 \- ""
 \- "moby.plugins.http/v1"
 Entrypoint:
 type: "array"
 items:
 type: "string"
 example:
 \- "/usr/bin/sample-volume-plugin"
 \- "/data"
 WorkDir:
 type: "string"
 x-nullable: false
 example: "/bin/"
 User:
 type: "object"
 x-go-name: "User"
 x-nullable: false
 properties:
 UID:
 type: "integer"
 format: "uint32"
 example: 1000
 GID:
 type: "integer"
 format: "uint32"
 example: 1000
 Network:
 type: "object"
 x-go-name: "NetworkConfig"
 x-nullable: false
 required: \[Type\]
 properties:
 Type:
 x-nullable: false
 type: "string"
 example: "host"
 Linux:
 type: "object"
 x-go-name: "LinuxConfig"
 x-nullable: false
 required: \[Capabilities, AllowAllDevices, Devices\]
 properties:
 Capabilities:
 type: "array"
 items:
 type: "string"
 example:
 \- "CAP\_SYS\_ADMIN"
 \- "CAP\_SYSLOG"
 AllowAllDevices:
 type: "boolean"
 x-nullable: false
 example: false
 Devices:
 type: "array"
 items:
 $ref: "#/definitions/PluginDevice"
 PropagatedMount:
 type: "string"
 x-nullable: false
 example: "/mnt/volumes"
 IpcHost:
 type: "boolean"
 x-nullable: false
 example: false
 PidHost:
 type: "boolean"
 x-nullable: false
 example: false
 Mounts:
 type: "array"
 items:
 $ref: "#/definitions/PluginMount"
 Env:
 type: "array"
 items:
 $ref: "#/definitions/PluginEnv"
 example:
 \- Name: "DEBUG"
 Description: "If set, prints debug messages"
 Settable: null
 Value: "0"
 Args:
 type: "object"
 x-go-name: "Args"
 x-nullable: false
 required: \[Name, Description, Settable, Value\]
 properties:
 Name:
 x-nullable: false
 type: "string"
 example: "args"
 Description:
 x-nullable: false
 type: "string"
 example: "command line arguments"
 Settable:
 type: "array"
 items:
 type: "string"
 Value:
 type: "array"
 items:
 type: "string"
 rootfs:
 type: "object"
 x-go-name: "RootFS"
 properties:
 type:
 type: "string"
 example: "layers"
 diff\_ids:
 type: "array"
 items:
 type: "string"
 example:
 \- "sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887"
 \- "sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"

 ObjectVersion:
 description: \|
 The version number of the object such as node, service, etc. This is needed
 to avoid conflicting writes. The client must send the version number along
 with the modified specification when updating these objects.

 This approach ensures safe concurrency and determinism in that the change
 on the object may not be applied if the version number has changed from the
 last read. In other words, if two update requests specify the same base
 version, only one of the requests can succeed. As a result, two separate
 update requests that happen at the same time will not unintentionally
 overwrite each other.
 type: "object"
 properties:
 Index:
 type: "integer"
 format: "uint64"
 example: 373531

 NodeSpec:
 type: "object"
 properties:
 Name:
 description: "Name for the node."
 type: "string"
 example: "my-node"
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 Role:
 description: "Role of the node."
 type: "string"
 enum:
 \- "worker"
 \- "manager"
 example: "manager"
 Availability:
 description: "Availability of the node."
 type: "string"
 enum:
 \- "active"
 \- "pause"
 \- "drain"
 example: "active"
 example:
 Availability: "active"
 Name: "node-name"
 Role: "manager"
 Labels:
 foo: "bar"

 Node:
 type: "object"
 properties:
 ID:
 type: "string"
 example: "24ifsmvkjbyhk"
 Version:
 $ref: "#/definitions/ObjectVersion"
 CreatedAt:
 description: \|
 Date and time at which the node was added to the swarm in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 example: "2016-08-18T10:44:24.496525531Z"
 UpdatedAt:
 description: \|
 Date and time at which the node was last updated in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 example: "2017-08-09T07:09:37.632105588Z"
 Spec:
 $ref: "#/definitions/NodeSpec"
 Description:
 $ref: "#/definitions/NodeDescription"
 Status:
 $ref: "#/definitions/NodeStatus"
 ManagerStatus:
 $ref: "#/definitions/ManagerStatus"

 NodeDescription:
 description: \|
 NodeDescription encapsulates the properties of the Node as reported by the
 agent.
 type: "object"
 properties:
 Hostname:
 type: "string"
 example: "bf3067039e47"
 Platform:
 $ref: "#/definitions/Platform"
 Resources:
 $ref: "#/definitions/ResourceObject"
 Engine:
 $ref: "#/definitions/EngineDescription"
 TLSInfo:
 $ref: "#/definitions/TLSInfo"

 Platform:
 description: \|
 Platform represents the platform (Arch/OS).
 type: "object"
 properties:
 Architecture:
 description: \|
 Architecture represents the hardware architecture (for example,
 \`x86\_64\`).
 type: "string"
 example: "x86\_64"
 OS:
 description: \|
 OS represents the Operating System (for example, \`linux\` or \`windows\`).
 type: "string"
 example: "linux"

 EngineDescription:
 description: "EngineDescription provides information about an engine."
 type: "object"
 properties:
 EngineVersion:
 type: "string"
 example: "17.06.0"
 Labels:
 type: "object"
 additionalProperties:
 type: "string"
 example:
 foo: "bar"
 Plugins:
 type: "array"
 items:
 type: "object"
 properties:
 Type:
 type: "string"
 Name:
 type: "string"
 example:
 \- Type: "Log"
 Name: "awslogs"
 \- Type: "Log"
 Name: "fluentd"
 \- Type: "Log"
 Name: "gcplogs"
 \- Type: "Log"
 Name: "gelf"
 \- Type: "Log"
 Name: "journald"
 \- Type: "Log"
 Name: "json-file"
 \- Type: "Log"
 Name: "splunk"
 \- Type: "Log"
 Name: "syslog"
 \- Type: "Network"
 Name: "bridge"
 \- Type: "Network"
 Name: "host"
 \- Type: "Network"
 Name: "ipvlan"
 \- Type: "Network"
 Name: "macvlan"
 \- Type: "Network"
 Name: "null"
 \- Type: "Network"
 Name: "overlay"
 \- Type: "Volume"
 Name: "local"
 \- Type: "Volume"
 Name: "localhost:5000/vieux/sshfs:latest"
 \- Type: "Volume"
 Name: "vieux/sshfs:latest"

 TLSInfo:
 description: \|
 Information about the issuer of leaf TLS certificates and the trusted root
 CA certificate.
 type: "object"
 properties:
 TrustRoot:
 description: \|
 The root CA certificate(s) that are used to validate leaf TLS
 certificates.
 type: "string"
 CertIssuerSubject:
 description:
 The base64-url-safe-encoded raw subject bytes of the issuer.
 type: "string"
 CertIssuerPublicKey:
 description: \|
 The base64-url-safe-encoded raw public key bytes of the issuer.
 type: "string"
 example:
 TrustRoot: \|
 -----BEGIN CERTIFICATE-----
 MIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw
 EzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0
 MzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH
 A0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf
 3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB
 Af8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO
 PQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz
 pxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H
 -----END CERTIFICATE-----
 CertIssuerSubject: "MBMxETAPBgNVBAMTCHN3YXJtLWNh"
 CertIssuerPublicKey: "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="

 NodeStatus:
 description: \|
 NodeStatus represents the status of a node.

 It provides the current status of the node, as seen by the manager.
 type: "object"
 properties:
 State:
 $ref: "#/definitions/NodeState"
 Message:
 type: "string"
 example: ""
 Addr:
 description: "IP address of the node."
 type: "string"
 example: "172.17.0.2"

 NodeState:
 description: "NodeState represents the state of a node."
 type: "string"
 enum:
 \- "unknown"
 \- "down"
 \- "ready"
 \- "disconnected"
 example: "ready"

 ManagerStatus:
 description: \|
 ManagerStatus represents the status of a manager.

 It provides the current status of a node's manager component, if the node
 is a manager.
 x-nullable: true
 type: "object"
 properties:
 Leader:
 type: "boolean"
 default: false
 example: true
 Reachability:
 $ref: "#/definitions/Reachability"
 Addr:
 description: \|
 The IP address and port at which the manager is reachable.
 type: "string"
 example: "10.0.0.46:2377"

 Reachability:
 description: "Reachability represents the reachability of a node."
 type: "string"
 enum:
 \- "unknown"
 \- "unreachable"
 \- "reachable"
 example: "reachable"

 SwarmSpec:
 description: "User modifiable swarm configuration."
 type: "object"
 properties:
 Name:
 description: "Name of the swarm."
 type: "string"
 example: "default"
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 example:
 com.example.corp.type: "production"
 com.example.corp.department: "engineering"
 Orchestration:
 description: "Orchestration configuration."
 type: "object"
 x-nullable: true
 properties:
 TaskHistoryRetentionLimit:
 description: \|
 The number of historic tasks to keep per instance or node. If
 negative, never remove completed or failed tasks.
 type: "integer"
 format: "int64"
 example: 10
 Raft:
 description: "Raft configuration."
 type: "object"
 properties:
 SnapshotInterval:
 description: "The number of log entries between snapshots."
 type: "integer"
 format: "uint64"
 example: 10000
 KeepOldSnapshots:
 description: \|
 The number of snapshots to keep beyond the current snapshot.
 type: "integer"
 format: "uint64"
 LogEntriesForSlowFollowers:
 description: \|
 The number of log entries to keep around to sync up slow followers
 after a snapshot is created.
 type: "integer"
 format: "uint64"
 example: 500
 ElectionTick:
 description: \|
 The number of ticks that a follower will wait for a message from
 the leader before becoming a candidate and starting an election.
 \`ElectionTick\` must be greater than \`HeartbeatTick\`.

 A tick currently defaults to one second, so these translate
 directly to seconds currently, but this is NOT guaranteed.
 type: "integer"
 example: 3
 HeartbeatTick:
 description: \|
 The number of ticks between heartbeats. Every HeartbeatTick ticks,
 the leader will send a heartbeat to the followers.

 A tick currently defaults to one second, so these translate
 directly to seconds currently, but this is NOT guaranteed.
 type: "integer"
 example: 1
 Dispatcher:
 description: "Dispatcher configuration."
 type: "object"
 x-nullable: true
 properties:
 HeartbeatPeriod:
 description: \|
 The delay for an agent to send a heartbeat to the dispatcher.
 type: "integer"
 format: "int64"
 example: 5000000000
 CAConfig:
 description: "CA configuration."
 type: "object"
 x-nullable: true
 properties:
 NodeCertExpiry:
 description: "The duration node certificates are issued for."
 type: "integer"
 format: "int64"
 example: 7776000000000000
 ExternalCAs:
 description: \|
 Configuration for forwarding signing requests to an external
 certificate authority.
 type: "array"
 items:
 type: "object"
 properties:
 Protocol:
 description: \|
 Protocol for communication with the external CA (currently
 only \`cfssl\` is supported).
 type: "string"
 enum:
 \- "cfssl"
 default: "cfssl"
 URL:
 description: \|
 URL where certificate signing requests should be sent.
 type: "string"
 Options:
 description: \|
 An object with key/value pairs that are interpreted as
 protocol-specific options for the external CA driver.
 type: "object"
 additionalProperties:
 type: "string"
 CACert:
 description: \|
 The root CA certificate (in PEM format) this external CA uses
 to issue TLS certificates (assumed to be to the current swarm
 root CA certificate if not provided).
 type: "string"
 SigningCACert:
 description: \|
 The desired signing CA certificate for all swarm node TLS leaf
 certificates, in PEM format.
 type: "string"
 SigningCAKey:
 description: \|
 The desired signing CA key for all swarm node TLS leaf certificates,
 in PEM format.
 type: "string"
 ForceRotate:
 description: \|
 An integer whose purpose is to force swarm to generate a new
 signing CA certificate and key, if none have been specified in
 \`SigningCACert\` and \`SigningCAKey\`
 format: "uint64"
 type: "integer"
 EncryptionConfig:
 description: "Parameters related to encryption-at-rest."
 type: "object"
 properties:
 AutoLockManagers:
 description: \|
 If set, generate a key and use it to lock data stored on the
 managers.
 type: "boolean"
 example: false
 TaskDefaults:
 description: "Defaults for creating tasks in this cluster."
 type: "object"
 properties:
 LogDriver:
 description: \|
 The log driver to use for tasks created in the orchestrator if
 unspecified by a service.

 Updating this value only affects new tasks. Existing tasks continue
 to use their previously configured log driver until recreated.
 type: "object"
 properties:
 Name:
 description: \|
 The log driver to use as a default for new tasks.
 type: "string"
 example: "json-file"
 Options:
 description: \|
 Driver-specific options for the selected log driver, specified
 as key/value pairs.
 type: "object"
 additionalProperties:
 type: "string"
 example:
 "max-file": "10"
 "max-size": "100m"

 # The Swarm information for \`GET /info\`. It is the same as \`GET /swarm\`, but
 # without \`JoinTokens\`.
 ClusterInfo:
 description: \|
 ClusterInfo represents information about the swarm as is returned by the
 "/info" endpoint. Join-tokens are not included.
 x-nullable: true
 type: "object"
 properties:
 ID:
 description: "The ID of the swarm."
 type: "string"
 example: "abajmipo7b4xz5ip2nrla6b11"
 Version:
 $ref: "#/definitions/ObjectVersion"
 CreatedAt:
 description: \|
 Date and time at which the swarm was initialised in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 example: "2016-08-18T10:44:24.496525531Z"
 UpdatedAt:
 description: \|
 Date and time at which the swarm was last updated in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 example: "2017-08-09T07:09:37.632105588Z"
 Spec:
 $ref: "#/definitions/SwarmSpec"
 TLSInfo:
 $ref: "#/definitions/TLSInfo"
 RootRotationInProgress:
 description: \|
 Whether there is currently a root CA rotation in progress for the swarm
 type: "boolean"
 example: false
 DataPathPort:
 description: \|
 DataPathPort specifies the data path port number for data traffic.
 Acceptable port range is 1024 to 49151.
 If no port is set or is set to 0, the default port (4789) is used.
 type: "integer"
 format: "uint32"
 default: 4789
 example: 4789
 DefaultAddrPool:
 description: \|
 Default Address Pool specifies default subnet pools for global scope
 networks.
 type: "array"
 items:
 type: "string"
 format: "CIDR"
 example: \["10.10.0.0/16", "20.20.0.0/16"\]
 SubnetSize:
 description: \|
 SubnetSize specifies the subnet size of the networks created from the
 default subnet pool.
 type: "integer"
 format: "uint32"
 maximum: 29
 default: 24
 example: 24

 JoinTokens:
 description: \|
 JoinTokens contains the tokens workers and managers need to join the swarm.
 type: "object"
 properties:
 Worker:
 description: \|
 The token workers can use to join the swarm.
 type: "string"
 example: "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx"
 Manager:
 description: \|
 The token managers can use to join the swarm.
 type: "string"
 example: "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2"

 Swarm:
 type: "object"
 allOf:
 \- $ref: "#/definitions/ClusterInfo"
 \- type: "object"
 properties:
 JoinTokens:
 $ref: "#/definitions/JoinTokens"

 TaskSpec:
 description: "User modifiable task configuration."
 type: "object"
 properties:
 PluginSpec:
 type: "object"
 description: \|
 Plugin spec for the service. \*(Experimental release only.)\*



 \> \*\*Note\*\*: ContainerSpec, NetworkAttachmentSpec, and PluginSpec are
 \> mutually exclusive. PluginSpec is only used when the Runtime field
 \> is set to \`plugin\`. NetworkAttachmentSpec is used when the Runtime
 \> field is set to \`attachment\`.
 properties:
 Name:
 description: "The name or 'alias' to use for the plugin."
 type: "string"
 Remote:
 description: "The plugin image reference to use."
 type: "string"
 Disabled:
 description: "Disable the plugin once scheduled."
 type: "boolean"
 PluginPrivilege:
 type: "array"
 items:
 $ref: "#/definitions/PluginPrivilege"
 ContainerSpec:
 type: "object"
 description: \|
 Container spec for the service.



 \> \*\*Note\*\*: ContainerSpec, NetworkAttachmentSpec, and PluginSpec are
 \> mutually exclusive. PluginSpec is only used when the Runtime field
 \> is set to \`plugin\`. NetworkAttachmentSpec is used when the Runtime
 \> field is set to \`attachment\`.
 properties:
 Image:
 description: "The image name to use for the container"
 type: "string"
 Labels:
 description: "User-defined key/value data."
 type: "object"
 additionalProperties:
 type: "string"
 Command:
 description: "The command to be run in the image."
 type: "array"
 items:
 type: "string"
 Args:
 description: "Arguments to the command."
 type: "array"
 items:
 type: "string"
 Hostname:
 description: \|
 The hostname to use for the container, as a valid
 \[RFC 1123\](https://tools.ietf.org/html/rfc1123) hostname.
 type: "string"
 Env:
 description: \|
 A list of environment variables in the form \`VAR=value\`.
 type: "array"
 items:
 type: "string"
 Dir:
 description: "The working directory for commands to run in."
 type: "string"
 User:
 description: "The user inside the container."
 type: "string"
 Groups:
 type: "array"
 description: \|
 A list of additional groups that the container process will run as.
 items:
 type: "string"
 Privileges:
 type: "object"
 description: "Security options for the container"
 properties:
 CredentialSpec:
 type: "object"
 description: "CredentialSpec for managed service account (Windows only)"
 properties:
 Config:
 type: "string"
 example: "0bt9dmxjvjiqermk6xrop3ekq"
 description: \|
 Load credential spec from a Swarm Config with the given ID.
 The specified config must also be present in the Configs
 field with the Runtime property set.



 \> \*\*Note\*\*: \`CredentialSpec.File\`, \`CredentialSpec.Registry\`,
 \> and \`CredentialSpec.Config\` are mutually exclusive.
 File:
 type: "string"
 example: "spec.json"
 description: \|
 Load credential spec from this file. The file is read by
 the daemon, and must be present in the \`CredentialSpecs\`
 subdirectory in the docker data directory, which defaults
 to \`C:\\ProgramData\\Docker\\\` on Windows.

 For example, specifying \`spec.json\` loads
 \`C:\\ProgramData\\Docker\\CredentialSpecs\\spec.json\`.



 \> \*\*Note\*\*: \`CredentialSpec.File\`, \`CredentialSpec.Registry\`,
 \> and \`CredentialSpec.Config\` are mutually exclusive.
 Registry:
 type: "string"
 description: \|
 Load credential spec from this value in the Windows
 registry. The specified registry value must be located in:

 \`HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Virtualization\\Containers\\CredentialSpecs\`



 \> \*\*Note\*\*: \`CredentialSpec.File\`, \`CredentialSpec.Registry\`,
 \> and \`CredentialSpec.Config\` are mutually exclusive.
 SELinuxContext:
 type: "object"
 description: "SELinux labels of the container"
 properties:
 Disable:
 type: "boolean"
 description: "Disable SELinux"
 User:
 type: "string"
 description: "SELinux user label"
 Role:
 type: "string"
 description: "SELinux role label"
 Type:
 type: "string"
 description: "SELinux type label"
 Level:
 type: "string"
 description: "SELinux level label"
 Seccomp:
 type: "object"
 description: "Options for configuring seccomp on the container"
 properties:
 Mode:
 type: "string"
 enum:
 \- "default"
 \- "unconfined"
 \- "custom"
 Profile:
 description: "The custom seccomp profile as a json object"
 type: "string"
 AppArmor:
 type: "object"
 description: "Options for configuring AppArmor on the container"
 properties:
 Mode:
 type: "string"
 enum:
 \- "default"
 \- "disabled"
 NoNewPrivileges:
 type: "boolean"
 description: "Configuration of the no\_new\_privs bit in the container"

 TTY:
 description: "Whether a pseudo-TTY should be allocated."
 type: "boolean"
 OpenStdin:
 description: "Open \`stdin\`"
 type: "boolean"
 ReadOnly:
 description: "Mount the container's root filesystem as read only."
 type: "boolean"
 Mounts:
 description: \|
 Specification for mounts to be added to containers created as part
 of the service.
 type: "array"
 items:
 $ref: "#/definitions/Mount"
 StopSignal:
 description: "Signal to stop the container."
 type: "string"
 StopGracePeriod:
 description: \|
 Amount of time to wait for the container to terminate before
 forcefully killing it.
 type: "integer"
 format: "int64"
 HealthCheck:
 $ref: "#/definitions/HealthConfig"
 Hosts:
 type: "array"
 description: \|
 A list of hostname/IP mappings to add to the container's \`hosts\`
 file. The format of extra hosts is specified in the
 \[hosts(5)\](http://man7.org/linux/man-pages/man5/hosts.5.html)
 man page:

 IP\_address canonical\_hostname \[aliases...\]
 items:
 type: "string"
 DNSConfig:
 description: \|
 Specification for DNS related configurations in resolver configuration
 file (\`resolv.conf\`).
 type: "object"
 properties:
 Nameservers:
 description: "The IP addresses of the name servers."
 type: "array"
 items:
 type: "string"
 Search:
 description: "A search list for host-name lookup."
 type: "array"
 items:
 type: "string"
 Options:
 description: \|
 A list of internal resolver variables to be modified (e.g.,
 \`debug\`, \`ndots:3\`, etc.).
 type: "array"
 items:
 type: "string"
 Secrets:
 description: \|
 Secrets contains references to zero or more secrets that will be
 exposed to the service.
 type: "array"
 items:
 type: "object"
 properties:
 File:
 description: \|
 File represents a specific target that is backed by a file.
 type: "object"
 properties:
 Name:
 description: \|
 Name represents the final filename in the filesystem.
 type: "string"
 UID:
 description: "UID represents the file UID."
 type: "string"
 GID:
 description: "GID represents the file GID."
 type: "string"
 Mode:
 description: "Mode represents the FileMode of the file."
 type: "integer"
 format: "uint32"
 SecretID:
 description: \|
 SecretID represents the ID of the specific secret that we're
 referencing.
 type: "string"
 SecretName:
 description: \|
 SecretName is the name of the secret that this references,
 but this is just provided for lookup/display purposes. The
 secret in the reference will be identified by its ID.
 type: "string"
 OomScoreAdj:
 type: "integer"
 format: "int64"
 description: \|
 An integer value containing the score given to the container in
 order to tune OOM killer preferences.
 example: 0
 Configs:
 description: \|
 Configs contains references to zero or more configs that will be
 exposed to the service.
 type: "array"
 items:
 type: "object"
 properties:
 File:
 description: \|
 File represents a specific target that is backed by a file.



\> \*\*Note\*\*: \`Configs.File\` and \`Configs.Runtime\` are mutually exclusive
type: "object"
properties:
Name:
description: \|
Name represents the final filename in the filesystem.
type: "string"
UID:
description: "UID represents the file UID."
type: "string"
GID:
description: "GID represents the file GID."
type: "string"
Mode:
description: "Mode represents the FileMode of the file."
type: "integer"
format: "uint32"
Runtime:
description: \|
Runtime represents a target that is not mounted into the
container but is used by the task



\> \*\*Note\*\*: \`Configs.File\` and \`Configs.Runtime\` are mutually
\> exclusive
type: "object"
ConfigID:
description: \|
ConfigID represents the ID of the specific config that we're
referencing.
type: "string"
ConfigName:
description: \|
ConfigName is the name of the config that this references,
but this is just provided for lookup/display purposes. The
config in the reference will be identified by its ID.
type: "string"
Isolation:
type: "string"
description: \|
Isolation technology of the containers running the service.
(Windows only)
enum:
\- "default"
\- "process"
\- "hyperv"
\- ""
Init:
description: \|
Run an init inside the container that forwards signals and reaps
processes. This field is omitted if empty, and the default (as
configured on the daemon) is used.
type: "boolean"
x-nullable: true
Sysctls:
description: \|
Set kernel namedspaced parameters (sysctls) in the container.
The Sysctls option on services accepts the same sysctls as the
are supported on containers. Note that while the same sysctls are
supported, no guarantees or checks are made about their
suitability for a clustered environment, and it's up to the user
to determine whether a given sysctl will work properly in a
Service.
type: "object"
additionalProperties:
type: "string"

 Reservations:
 description: "Define resources reservation."
 $ref: "#/definitions/ResourceObject"
 SwapBytes:
 description: \|
 Amount of swap in bytes - can only be used together with a memory limit.
 If not specified, the default behaviour is to grant a swap space twice
 as big as the memory limit.
 Set to -1 to enable unlimited swap.
 type: "integer"
 format: "int64"
 minimum: -1
 x-nullable: true
 x-omitempty: true
 MemorySwappiness:
 description: \|
 Tune the service's containers' memory swappiness (0 to 100).
 If not specified, defaults to the containers' OS' default, generally 60,
 or whatever value was predefined in the image.
 Set to -1 to unset a previously set value.
 type: "integer"
 format: "int64"
 minimum: -1
 maximum: 100
 x-nullable: true
 x-omitempty: true
 RestartPolicy:
 description: \|
 Specification for the restart policy which applies to containers
 created as part of this service.
 type: "object"
 properties:
 Condition:
 description: "Condition for restart."
 type: "string"
 enum:
 \- "none"
 \- "on-failure"
 \- "any"
 Delay:
 description: "Delay between restart attempts."
 type: "integer"
 format: "int64"
 MaxAttempts:
 description: \|
 Maximum attempts to restart a given container before giving up
 (default value is 0, which is ignored).
 type: "integer"
 format: "int64"
 default: 0
 Window:
 description: \|
 Windows is the time window used to evaluate the restart policy
 (default value is 0, which is unbounded).
 type: "integer"
 format: "int64"
 default: 0
 Placement:
 type: "object"
 properties:
 Constraints:
 description: \|
 An array of constraint expressions to limit the set of nodes where
 a task can be scheduled. Constraint expressions can either use a
 \_match\_ (\`==\`) or \_exclude\_ (\`!=\`) rule. Multiple constraints find
 nodes that satisfy every expression (AND match). Constraints can
 match node or Docker Engine labels as follows:

 node attribute \| matches \| example
 ---------------------\|--------------------------------\|-----------------------------------------------
 \`node.id\` \| Node ID \| \`node.id==2ivku8v2gvtg4\`
 \`node.hostname\` \| Node hostname \| \`node.hostname!=node-2\`
 \`node.role\` \| Node role (\`manager\`/\`worker\`) \| \`node.role==manager\`
 \`node.platform.os\` \| Node operating system \| \`node.platform.os==windows\`
 \`node.platform.arch\` \| Node architecture \| \`node.platform.arch==x86\_64\`
 \`node.labels\` \| User-defined node labels \| \`node.labels.security==high\`
 \`engine.labels\` \| Docker Engine's labels \| \`engine.labels.operatingsystem==ubuntu-24.04\`

 \`engine.labels\` apply to Docker Engine labels like operating system,
 drivers, etc. Swarm administrators add \`node.labels\` for operational
 purposes by using the \[\`node update endpoint\`\](#operation/NodeUpdate).

 type: "array"
 items:
 type: "string"
 example:
 \- "node.hostname!=node3.corp.example.com"
 \- "node.role!=manager"
 \- "node.labels.type==production"
 \- "node.platform.os==linux"
 \- "node.platform.arch==x86\_64"
 Preferences:
 description: \|
 Preferences provide a way to make the scheduler aware of factors
 such as topology. They are provided in order from highest to
 lowest precedence.
 type: "array"
 items:
 type: "object"
 properties:
 Spread:
 type: "object"
 properties:
 SpreadDescriptor:
 description: \|
 label descriptor, such as \`engine.labels.az\`.
 type: "string"
 example:
 \- Spread:
 SpreadDescriptor: "node.labels.datacenter"
 \- Spread:
 SpreadDescriptor: "node.labels.rack"
 MaxReplicas:
 description: \|
 Maximum number of replicas for per node (default value is 0, which
 is unlimited)
 type: "integer"
 format: "int64"
 default: 0
 Platforms:
 description: \|
 Platforms stores all the platforms that the service's image can
 run on. This field is used in the platform filter for scheduling.
 If empty, then the platform filter is off, meaning there are no
 scheduling restrictions.
 type: "array"
 items:
 $ref: "#/definitions/Platform"
 ForceUpdate:
 description: \|
 A counter that triggers an update even if no relevant parameters have
 been changed.
 type: "integer"
 format: "uint64"
 Runtime:
 description: \|
 Runtime is the type of runtime specified for the task executor.
 type: "string"
 Networks:
 description: "Specifies which networks the service should attach to."
 type: "array"
 items:
 $ref: "#/definitions/NetworkAttachmentConfig"
 LogDriver:
 description: \|
 Specifies the log driver to use for tasks created from this spec. If
 not present, the default one for the swarm will be used, finally
 falling back to the engine default if not specified.
 type: "object"
 properties:
 Name:
 type: "string"
 Options:
 type: "object"
 additionalProperties:
 type: "string"

 TaskState:
 type: "string"
 enum:
 \- "new"
 \- "allocated"
 \- "pending"
 \- "assigned"
 \- "accepted"
 \- "preparing"
 \- "ready"
 \- "starting"
 \- "running"
 \- "complete"
 \- "shutdown"
 \- "failed"
 \- "rejected"
 \- "remove"
 \- "orphaned"

 ContainerStatus:
 type: "object"
 description: "represents the status of a container."
 properties:
 ContainerID:
 type: "string"
 PID:
 type: "integer"
 ExitCode:
 type: "integer"

 PortStatus:
 type: "object"
 description: "represents the port status of a task's host ports whose service has published host ports"
 properties:
 Ports:
 type: "array"
 items:
 $ref: "#/definitions/EndpointPortConfig"

 TaskStatus:
 type: "object"
 description: "represents the status of a task."
 properties:
 Timestamp:
 type: "string"
 format: "dateTime"
 State:
 $ref: "#/definitions/TaskState"
 Message:
 type: "string"
 Err:
 type: "string"
 ContainerStatus:
 $ref: "#/definitions/ContainerStatus"
 PortStatus:
 $ref: "#/definitions/PortStatus"

 Task:
 type: "object"
 properties:
 ID:
 description: "The ID of the task."
 type: "string"
 Version:
 $ref: "#/definitions/ObjectVersion"
 CreatedAt:
 type: "string"
 format: "dateTime"
 UpdatedAt:
 type: "string"
 format: "dateTime"
 Name:
 description: "Name of the task."
 type: "string"
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 Spec:
 $ref: "#/definitions/TaskSpec"
 ServiceID:
 description: "The ID of the service this task is part of."
 type: "string"
 Slot:
 type: "integer"
 NodeID:
 description: "The ID of the node that this task is on."
 type: "string"
 AssignedGenericResources:
 $ref: "#/definitions/GenericResources"
 Status:
 $ref: "#/definitions/TaskStatus"

 description: \|
 Specifies which networks the service should attach to.

 Deprecated: This field is deprecated since v1.44. The Networks field in TaskSpec should be used instead.

 example:
 ID: "9mnpnzenvg8p8tdbtq4wvbkcz"
 Version:
 Index: 19
 CreatedAt: "2016-06-07T21:05:51.880065305Z"
 UpdatedAt: "2016-06-07T21:07:29.962229872Z"
 Spec:
 Name: "hopeful\_cori"
 TaskTemplate:
 ForceUpdate: 0
 Mode:
 Replicated:
 Replicas: 1
 UpdateConfig:
 Parallelism: 1
 Delay: 1000000000
 FailureAction: "pause"
 Monitor: 15000000000
 MaxFailureRatio: 0.15
 RollbackConfig:
 Parallelism: 1
 Delay: 1000000000
 FailureAction: "pause"
 Monitor: 15000000000
 MaxFailureRatio: 0.15
 EndpointSpec:
 Mode: "vip"
 Ports:
 -
 Protocol: "tcp"
 TargetPort: 6379
 PublishedPort: 30001
 Endpoint:
 Spec:
 Mode: "vip"
 Ports:
 -
 Protocol: "tcp"
 TargetPort: 6379
 PublishedPort: 30001
 Ports:
 -
 Protocol: "tcp"
 TargetPort: 6379
 PublishedPort: 30001
 VirtualIPs:
 -
 NetworkID: "4qvuz4ko70xaltuqbt8956gd1"
 Addr: "10.255.0.2/16"
 -
 NetworkID: "4qvuz4ko70xaltuqbt8956gd1"
 Addr: "10.255.0.3/16"

 ImageDeleteResponseItem:
 type: "object"
 x-go-name: "DeleteResponse"
 properties:
 Untagged:
 description: "The image ID of an image that was untagged"
 type: "string"
 Deleted:
 description: "The image ID of an image that was deleted"
 type: "string"

 ServiceCreateResponse:
 type: "object"
 description: \|
 contains the information returned to a client on the
 creation of a new service.
 properties:
 ID:
 description: "The ID of the created service."
 type: "string"
 x-nullable: false
 example: "ak7w3gjqoa3kuz8xcpnyy0pvl"
 Warnings:
 description: \|
 Optional warning message.

 FIXME(thaJeztah): this should have "omitempty" in the generated type.
 type: "array"
 x-nullable: true
 items:
 type: "string"
 example:
 \- "unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"

 ServiceUpdateResponse:
 type: "object"
 properties:
 Warnings:
 description: "Optional warning messages"
 type: "array"
 items:
 type: "string"
 example:
 Warnings:
 \- "unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"

 ContainerInspectResponse:
 type: "object"
 title: "ContainerInspectResponse"
 x-go-name: "InspectResponse"
 properties:
 Id:
 description: \|-
 The ID of this container as a 128-bit (64-character) hexadecimal string (32 bytes).
 type: "string"
 x-go-name: "ID"
 minLength: 64
 maxLength: 64
 pattern: "^\[0-9a-fA-F\]{64}$"
 example: "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf"
 Created:
 description: \|-
 Date and time at which the container was created, formatted in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 x-nullable: true
 example: "2025-02-17T17:43:39.64001363Z"
 Path:
 description: \|-
 The path to the command being run
 type: "string"
 example: "/bin/sh"
 Args:
 description: "The arguments to the command being run"
 type: "array"
 items:
 type: "string"
 example:
 \- "-c"
 \- "exit 9"
 State:
 $ref: "#/definitions/ContainerState"
 Image:
 description: \|-
 The ID (digest) of the image that this container was created from.
 type: "string"
 example: "sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782"
 ResolvConfPath:
 description: \|-
 Location of the \`/etc/resolv.conf\` generated for the container on the
 host.

 This file is managed through the docker daemon, and should not be
 accessed or modified by other tools.
 type: "string"
 example: "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/resolv.conf"
 HostnamePath:
 description: \|-
 Location of the \`/etc/hostname\` generated for the container on the
 host.

 This file is managed through the docker daemon, and should not be
 accessed or modified by other tools.
 type: "string"
 example: "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/hostname"
 HostsPath:
 description: \|-
 Location of the \`/etc/hosts\` generated for the container on the
 host.

 This file is managed through the docker daemon, and should not be
 accessed or modified by other tools.
 type: "string"
 example: "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/hosts"
 LogPath:
 description: \|-
 Location of the file used to buffer the container's logs. Depending on
 the logging-driver used for the container, this field may be omitted.

 This file is managed through the docker daemon, and should not be
 accessed or modified by other tools.
 type: "string"
 x-nullable: true
 example: "/var/lib/docker/containers/5b7c7e2b992aa426584ce6c47452756066be0e503a08b4516a433a54d2f69e59/5b7c7e2b992aa426584ce6c47452756066be0e503a08b4516a433a54d2f69e59-json.log"
 Name:
 description: \|-
 The name associated with this container.

 For historic reasons, the name may be prefixed with a forward-slash (\`/\`).
 type: "string"
 example: "/funny\_chatelet"
 RestartCount:
 description: \|-
 Number of times the container was restarted since it was created,
 or since daemon was started.
 type: "integer"
 example: 0
 Driver:
 description: \|-
 The storage-driver used for the container's filesystem (graph-driver
 or snapshotter).
 type: "string"
 example: "overlayfs"
 Platform:
 description: \|-
 The platform (operating system) for which the container was created.

 This field was introduced for the experimental "LCOW" (Linux Containers
 On Windows) features, which has been removed. In most cases, this field
 is equal to the host's operating system (\`linux\` or \`windows\`).
 type: "string"
 example: "linux"
 ImageManifestDescriptor:
 $ref: "#/definitions/OCIDescriptor"
 description: \|-
 OCI descriptor of the platform-specific manifest of the image
 the container was created from.

 Note: Only available if the daemon provides a multi-platform
 image store.
 MountLabel:
 description: \|-
 SELinux mount label set for the container.
 type: "string"
 example: ""
 ProcessLabel:
 description: \|-
 SELinux process label set for the container.
 type: "string"
 example: ""
 AppArmorProfile:
 description: \|-
 The AppArmor profile set for the container.
 type: "string"
 example: ""
 ExecIDs:
 description: \|-
 IDs of exec instances that are running in the container.
 type: "array"
 items:
 type: "string"
 x-nullable: true
 example:
 \- "b35395de42bc8abd327f9dd65d913b9ba28c74d2f0734eeeae84fa1c616a0fca"
 \- "3fc1232e5cd20c8de182ed81178503dc6437f4e7ef12b52cc5e8de020652f1c4"
 HostConfig:
 $ref: "#/definitions/HostConfig"
 GraphDriver:
 $ref: "#/definitions/DriverData"
 x-nullable: true
 Storage:
 $ref: "#/definitions/Storage"
 x-nullable: true
 SizeRw:
 description: \|-
 The size of files that have been created or changed by this container.

 This field is omitted by default, and only set when size is requested
 in the API request.
 type: "integer"
 format: "int64"
 x-nullable: true
 example: "122880"
 SizeRootFs:
 description: \|-
 The total size of all files in the read-only layers from the image
 that the container uses. These layers can be shared between containers.

 This field is omitted by default, and only set when size is requested
 in the API request.
 type: "integer"
 format: "int64"
 x-nullable: true
 example: "1653948416"
 Mounts:
 description: \|-
 List of mounts used by the container.
 type: "array"
 items:
 $ref: "#/definitions/MountPoint"
 Config:
 $ref: "#/definitions/ContainerConfig"
 NetworkSettings:
 $ref: "#/definitions/NetworkSettings"

 ContainerSummary:
 type: "object"
 properties:
 Id:
 description: \|-
 The ID of this container as a 128-bit (64-character) hexadecimal string (32 bytes).
 type: "string"
 x-go-name: "ID"
 minLength: 64
 maxLength: 64
 pattern: "^\[0-9a-fA-F\]{64}$"
 example: "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf"
 Names:
 description: \|-
 The names associated with this container. Most containers have a single
 name, but when using legacy "links", the container can have multiple
 names.

 For historic reasons, names are prefixed with a forward-slash (\`/\`).
 type: "array"
 items:
 type: "string"
 example:
 \- "/funny\_chatelet"
 Image:
 description: \|-
 The name or ID of the image used to create the container.

 This field shows the image reference as was specified when creating the container,
 which can be in its canonical form (e.g., \`docker.io/library/ubuntu:latest\`
 or \`docker.io/library/ubuntu@sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782\`),
 short form (e.g., \`ubuntu:latest\`)), or the ID(-prefix) of the image (e.g., \`72297848456d\`).

 The content of this field can be updated at runtime if the image used to
 create the container is untagged, in which case the field is updated to
 contain the the image ID (digest) it was resolved to in its canonical,
 non-truncated form (e.g., \`sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782\`).
 type: "string"
 example: "docker.io/library/ubuntu:latest"
 ImageID:
 description: \|-
 The ID (digest) of the image that this container was created from.
 type: "string"
 example: "sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782"
 ImageManifestDescriptor:
 $ref: "#/definitions/OCIDescriptor"
 x-nullable: true
 description: \|
 OCI descriptor of the platform-specific manifest of the image
 the container was created from.

 Note: Only available if the daemon provides a multi-platform
 image store.

 This field is not populated in the \`GET /system/df\` endpoint.
 Command:
 description: "Command to run when starting the container"
 type: "string"
 example: "/bin/bash"
 Created:
 description: \|-
 Date and time at which the container was created as a Unix timestamp
 (number of seconds since EPOCH).
 type: "integer"
 format: "int64"
 example: "1739811096"
 Ports:
 description: \|-
 Port-mappings for the container.
 type: "array"
 items:
 $ref: "#/definitions/PortSummary"
 SizeRw:
 description: \|-
 The size of files that have been created or changed by this container.

 This field is omitted by default, and only set when size is requested
 in the API request.
 type: "integer"
 format: "int64"
 x-nullable: true
 example: "122880"
 SizeRootFs:
 description: \|-
 The total size of all files in the read-only layers from the image
 that the container uses. These layers can be shared between containers.

 This field is omitted by default, and only set when size is requested
 in the API request.
 type: "integer"
 format: "int64"
 x-nullable: true
 example: "1653948416"
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 example:
 com.example.vendor: "Acme"
 com.example.license: "GPL"
 com.example.version: "1.0"
 State:
 description: \|
 The state of this container.
 type: "string"
 enum:
 \- "created"
 \- "running"
 \- "paused"
 \- "restarting"
 \- "exited"
 \- "removing"
 \- "dead"
 example: "running"
 Status:
 description: \|-
 Additional human-readable status of this container (e.g. \`Exit 0\`)
 type: "string"
 example: "Up 4 days"
 HostConfig:
 type: "object"
 description: \|-
 Summary of host-specific runtime information of the container. This
 is a reduced set of information in the container's "HostConfig" as
 available in the container "inspect" response.
 properties:
 NetworkMode:
 description: \|-
 Networking mode (\`host\`, \`none\`, \`container:\`) or name of the
 primary network the container is using.

 This field is primarily for backward compatibility. The container
 can be connected to multiple networks for which information can be
 found in the \`NetworkSettings.Networks\` field, which enumerates
 settings per network.
 type: "string"
 example: "mynetwork"
 Annotations:
 description: \|-
 Arbitrary key-value metadata attached to the container.
 type: "object"
 x-nullable: true
 additionalProperties:
 type: "string"
 example:
 io.kubernetes.docker.type: "container"
 io.kubernetes.sandbox.id: "3befe639bed0fd6afdd65fd1fa84506756f59360ec4adc270b0fdac9be22b4d3"
 NetworkSettings:
 description: \|-
 Summary of the container's network settings
 type: "object"
 properties:
 Networks:
 type: "object"
 description: \|-
 Summary of network-settings for each network the container is
 attached to.
 additionalProperties:
 $ref: "#/definitions/EndpointSettings"
 Mounts:
 type: "array"
 description: \|-
 List of mounts used by the container.
 items:
 $ref: "#/definitions/MountPoint"
 Health:
 type: "object"
 description: \|-
 Summary of health status

 Added in v1.52, before that version all container summary not include Health.
 After this attribute introduced, it includes containers with no health checks configured,
 or containers that are not running with none
 properties:
 Status:
 type: "string"
 description: \|-
 the health status of the container

 ContainersDiskUsage:
 type: "object"
 x-go-name: "DiskUsage"
 x-go-package: "github.com/moby/moby/api/types/container"
 description: \|
 represents system data usage information for container resources.
 properties:
 ActiveCount:
 description: \|
 Count of active containers.
 type: "integer"
 format: "int64"
 example: 1
 TotalCount:
 description: \|
 Count of all containers.
 type: "integer"
 format: "int64"
 example: 4
 Reclaimable:
 description: \|
 Disk space that can be reclaimed by removing inactive containers.
 type: "integer"
 format: "int64"
 example: 12345678
 TotalSize:
 description: \|
 Disk space in use by containers.
 type: "integer"
 format: "int64"
 example: 98765432
 Items:
 description: \|
 List of container summaries.
 type: "array"
 x-omitempty: true
 items:
 x-go-type:
 type: Summary

 Driver:
 description: "Driver represents a driver (network, logging, secrets)."
 type: "object"
 required: \[Name\]
 properties:
 Name:
 description: "Name of the driver."
 type: "string"
 x-nullable: false
 example: "some-driver"
 Options:
 description: "Key/value map of driver-specific options."
 type: "object"
 x-nullable: false
 additionalProperties:
 type: "string"
 example:
 OptionA: "value for driver-specific option A"
 OptionB: "value for driver-specific option B"

 SecretSpec:
 type: "object"
 properties:
 Name:
 description: "User-defined name of the secret."
 type: "string"
 Data:
 description: \|
 Data is the data to store as a secret, formatted as a standard base64-encoded
 (\[RFC 4648\](https://tools.ietf.org/html/rfc4648#section-4)) string.
 It must be empty if the Driver field is set, in which case the data is
 loaded from an external secret store. The maximum allowed size is 500KB,
 as defined in \[MaxSecretSize\](https://pkg.go.dev/github.com/moby/swarmkit/v2@v2.0.0/api/validation#MaxSecretSize).

 This field is only used to \_create\_ a secret, and is not returned by
 other endpoints.
 type: "string"
 example: ""
 Driver:
 description: \|
 Name of the secrets driver used to fetch the secret's value from an
 external secret store.
 $ref: "#/definitions/Driver"
 Templating:
 description: \|
 Templating driver, if applicable

 Templating controls whether and how to evaluate the config payload as
 a template. If no driver is set, no templating is used.
 $ref: "#/definitions/Driver"

 Secret:
 type: "object"
 properties:
 ID:
 type: "string"
 example: "blt1owaxmitz71s9v5zh81zun"
 Version:
 $ref: "#/definitions/ObjectVersion"
 CreatedAt:
 type: "string"
 format: "dateTime"
 example: "2017-07-20T13:55:28.678958722Z"
 UpdatedAt:
 type: "string"
 format: "dateTime"
 example: "2017-07-20T13:55:28.678958722Z"
 Spec:
 $ref: "#/definitions/SecretSpec"

 ConfigSpec:
 type: "object"
 properties:
 Name:
 description: "User-defined name of the config."
 type: "string"
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 Data:
 description: \|
 Data is the data to store as a config, formatted as a standard base64-encoded
 (\[RFC 4648\](https://tools.ietf.org/html/rfc4648#section-4)) string.
 The maximum allowed size is 1000KB, as defined in \[MaxConfigSize\](https://pkg.go.dev/github.com/moby/swarmkit/v2@v2.0.0-20250103191802-8c1959736554/manager/controlapi#MaxConfigSize).
 type: "string"
 Templating:
 description: \|
 Templating driver, if applicable

 Templating controls whether and how to evaluate the config payload as
 a template. If no driver is set, no templating is used.
 $ref: "#/definitions/Driver"

 Config:
 $ref: "#/definitions/ConfigSpec"

 ContainerState:
 description: \|
 ContainerState stores container's running state. It's part of ContainerJSONBase
 and will be returned by the "inspect" command.
 type: "object"
 x-nullable: true
 properties:
 Status:
 description: \|
 String representation of the container state. Can be one of "created",
 "running", "paused", "restarting", "removing", "exited", or "dead".
 type: "string"
 enum: \["created", "running", "paused", "restarting", "removing", "exited", "dead"\]
 example: "running"
 Running:
 description: \|
 Whether this container is running.

 Note that a running container can be \_paused\_. The \`Running\` and \`Paused\`
 booleans are not mutually exclusive:

 When pausing a container (on Linux), the freezer cgroup is used to suspend
 all processes in the container. Freezing the process requires the process to
 be running. As a result, paused containers are both \`Running\` \_and\_ \`Paused\`.

 Use the \`Status\` field instead to determine if a container's state is "running".
 type: "boolean"
 example: true
 Paused:
 description: "Whether this container is paused."
 type: "boolean"
 example: false
 Restarting:
 description: "Whether this container is restarting."
 type: "boolean"
 example: false
 OOMKilled:
 description: \|

 ContainerUpdateResponse:
 type: "object"
 title: "ContainerUpdateResponse"
 x-go-name: "UpdateResponse"
 description: \|-
 Response for a successful container-update.
 properties:
 Warnings:
 type: "array"
 description: \|-
 Warnings encountered when updating the container.
 items:
 type: "string"
 example: \["Published ports are discarded when using host network mode"\]

 ContainerStatsResponse:
 description: \|
 Statistics sample for a container.
 type: "object"
 x-go-name: "StatsResponse"
 title: "ContainerStatsResponse"
 properties:
 id:
 description: \|
 ID of the container for which the stats were collected.
 type: "string"
 x-nullable: true
 example: "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743"
 name:
 description: \|
 Name of the container for which the stats were collected.
 type: "string"
 x-nullable: true
 example: "boring\_wozniak"
 os\_type:
 description: \|
 OSType is the OS of the container ("linux" or "windows") to allow
 platform-specific handling of stats.
 type: "string"
 x-nullable: true
 example: "linux"
 read:
 description: \|
 Date and time at which this sample was collected.
 The value is formatted as \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt)
 with nano-seconds.
 type: "string"
 format: "date-time"
 example: "2025-01-16T13:55:22.165243637Z"
 cpu\_stats:
 $ref: "#/definitions/ContainerCPUStats"
 memory\_stats:
 $ref: "#/definitions/ContainerMemoryStats"
 networks:
 description: \|
 Network statistics for the container per interface.

 This field is omitted if the container has no networking enabled.
 x-nullable: true
 additionalProperties:
 $ref: "#/definitions/ContainerNetworkStats"
 example:
 eth0:
 rx\_bytes: 5338
 rx\_dropped: 0
 rx\_errors: 0
 rx\_packets: 36
 tx\_bytes: 648
 tx\_dropped: 0
 tx\_errors: 0
 tx\_packets: 8
 eth5:
 rx\_bytes: 4641
 rx\_dropped: 0
 rx\_errors: 0
 rx\_packets: 26
 tx\_bytes: 690
 tx\_dropped: 0
 tx\_errors: 0
 tx\_packets: 9
 pids\_stats:
 $ref: "#/definitions/ContainerPidsStats"
 blkio\_stats:
 $ref: "#/definitions/ContainerBlkioStats"
 num\_procs:
 description: \|
 The number of processors on the system.

 This field is Windows-specific and always zero for Linux containers.
 type: "integer"
 format: "uint32"
 example: 16
 storage\_stats:
 $ref: "#/definitions/ContainerStorageStats"
 preread:
 description: \|
 Date and time at which this first sample was collected. This field
 is not propagated if the "one-shot" option is set. If the "one-shot"
 option is set, this field may be omitted, empty, or set to a default
 date (\`0001-01-01T00:00:00Z\`).

 The value is formatted as \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt)
 with nano-seconds.
 type: "string"
 format: "date-time"
 example: "2025-01-16T13:55:21.160452595Z"
 precpu\_stats:
 $ref: "#/definitions/ContainerCPUStats"

 ContainerBlkioStats:
 description: \|
 BlkioStats stores all IO service stats for data read and write.

 This type is Linux-specific and holds many fields that are specific to cgroups v1.
 On a cgroup v2 host, all fields other than \`io\_service\_bytes\_recursive\`
 are omitted or \`null\`.

 This type is only populated on Linux and omitted for Windows containers.
 type: "object"
 x-go-name: "BlkioStats"
 x-nullable: true
 properties:
 io\_service\_bytes\_recursive:
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 io\_serviced\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 io\_queue\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 io\_service\_time\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 io\_wait\_time\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 io\_merged\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 io\_time\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 sectors\_recursive:
 description: \|
 This field is only available when using Linux containers with
 cgroups v1. It is omitted or \`null\` when using cgroups v2.
 x-nullable: true
 type: "array"
 items:
 $ref: "#/definitions/ContainerBlkioStatEntry"
 example:
 io\_service\_bytes\_recursive: \[\
 {"major": 254, "minor": 0, "op": "read", "value": 7593984},\
 {"major": 254, "minor": 0, "op": "write", "value": 100}\
 \]
 io\_serviced\_recursive: null
 io\_queue\_recursive: null
 io\_service\_time\_recursive: null
 io\_wait\_time\_recursive: null
 io\_merged\_recursive: null
 io\_time\_recursive: null
 sectors\_recursive: null

 ContainerBlkioStatEntry:
 description: \|
 Blkio stats entry.

 This type is Linux-specific and omitted for Windows containers.
 type: "object"
 x-go-name: "BlkioStatEntry"
 x-nullable: true
 properties:
 major:
 type: "integer"
 format: "uint64"
 example: 254
 minor:
 type: "integer"
 format: "uint64"
 example: 0
 op:
 type: "string"
 example: "read"
 value:
 type: "integer"
 format: "uint64"
 example: 7593984

 ContainerCPUStats:
 description: \|
 CPU related info of the container
 type: "object"
 x-go-name: "CPUStats"
 x-nullable: true
 properties:
 cpu\_usage:
 $ref: "#/definitions/ContainerCPUUsage"
 system\_cpu\_usage:
 description: \|
 System Usage.

 This field is Linux-specific and omitted for Windows containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 5
 online\_cpus:
 description: \|
 Number of online CPUs.

 This field is Linux-specific and omitted for Windows containers.
 type: "integer"
 format: "uint32"
 x-nullable: true
 example: 5
 throttling\_data:
 $ref: "#/definitions/ContainerThrottlingData"

 ContainerCPUUsage:
 description: \|
 All CPU stats aggregated since container inception.
 type: "object"
 x-go-name: "CPUUsage"
 x-nullable: true
 properties:
 total\_usage:
 description: \|
 Total CPU time consumed in nanoseconds (Linux) or 100's of nanoseconds (Windows).
 type: "integer"
 format: "uint64"
 example: 29912000
 percpu\_usage:
 description: \|
 Total CPU time (in nanoseconds) consumed per core (Linux).

 This field is Linux-specific when using cgroups v1. It is omitted
 when using cgroups v2 and Windows containers.
 type: "array"
 x-nullable: true
 items:
 type: "integer"
 format: "uint64"
 example: 29912000

 usage\_in\_kernelmode:
 description: \|
 Time (in nanoseconds) spent by tasks of the cgroup in kernel mode (Linux),
 or time spent (in 100's of nanoseconds) by all container processes in
 kernel mode (Windows).

 Not populated for Windows containers using Hyper-V isolation.
 type: "integer"
 format: "uint64"
 example: 21994000
 usage\_in\_usermode:
 description: \|
 Time (in nanoseconds) spent by tasks of the cgroup in user mode (Linux),
 or time spent (in 100's of nanoseconds) by all container processes in
 kernel mode (Windows).

 Not populated for Windows containers using Hyper-V isolation.
 type: "integer"
 format: "uint64"
 example: 7918000

 ContainerPidsStats:
 description: \|
 PidsStats contains Linux-specific stats of a container's process-IDs (PIDs).

 This type is Linux-specific and omitted for Windows containers.
 type: "object"
 x-go-name: "PidsStats"
 x-nullable: true
 properties:
 current:
 description: \|
 Current is the number of PIDs in the cgroup.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 5
 limit:
 description: \|
 Limit is the hard limit on the number of pids in the cgroup.
 A "Limit" of 0 means that there is no limit.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: "18446744073709551615"

 ContainerThrottlingData:
 description: \|
 CPU throttling stats of the container.

 This type is Linux-specific and omitted for Windows containers.
 type: "object"
 x-go-name: "ThrottlingData"
 x-nullable: true
 properties:
 periods:
 description: \|
 Number of periods with throttling active.
 type: "integer"
 format: "uint64"
 example: 0
 throttled\_periods:
 description: \|
 Number of periods when the container hit its throttling limit.
 type: "integer"
 format: "uint64"
 example: 0
 throttled\_time:
 description: \|
 Aggregated time (in nanoseconds) the container was throttled for.
 type: "integer"
 format: "uint64"
 example: 0

 ContainerMemoryStats:
 description: \|
 Aggregates all memory stats since container inception on Linux.
 Windows returns stats for commit and private working set only.
 type: "object"
 x-go-name: "MemoryStats"
 properties:
 usage:
 description: \|
 Current \`res\_counter\` usage for memory.

 This field is Linux-specific and omitted for Windows containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 0
 max\_usage:
 description: \|
 Maximum usage ever recorded.

 This field is Linux-specific and only supported on cgroups v1.
 It is omitted when using cgroups v2 and for Windows containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 0
 stats:
 description: \|
 All the stats exported via memory.stat.

 The fields in this object differ between cgroups v1 and v2.
 On cgroups v1, fields such as \`cache\`, \`rss\`, \`mapped\_file\` are available.
 On cgroups v2, fields such as \`file\`, \`anon\`, \`inactive\_file\` are available.

 This field is Linux-specific and omitted for Windows containers.
 type: "object"
 additionalProperties:
 type: "integer"
 format: "uint64"
 x-nullable: true
 example:
 {
 "active\_anon": 1572864,
 "active\_file": 5115904,
 "anon": 1572864,
 "anon\_thp": 0,
 "file": 7626752,
 "file\_dirty": 0,
 "file\_mapped": 2723840,
 "file\_writeback": 0,
 "inactive\_anon": 0,
 "inactive\_file": 2510848,
 "kernel\_stack": 16384,
 "pgactivate": 0,
 "pgdeactivate": 0,
 "pgfault": 2042,
 "pglazyfree": 0,
 "pglazyfreed": 0,
 "pgmajfault": 45,
 "pgrefill": 0,
 "pgscan": 0,
 "pgsteal": 0,
 "shmem": 0,
 "slab": 1180928,
 "slab\_reclaimable": 725576,
 "slab\_unreclaimable": 455352,
 "sock": 0,
 "thp\_collapse\_alloc": 0,
 "thp\_fault\_alloc": 1,
 "unevictable": 0,
 "workingset\_activate": 0,
 "workingset\_nodereclaim": 0,
 "workingset\_refault": 0
 }
 failcnt:
 description: \|
 Number of times memory usage hits limits.

 This field is Linux-specific and only supported on cgroups v1.
 It is omitted when using cgroups v2 and for Windows containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 0
 limit:
 description: \|
 This field is Linux-specific and omitted for Windows containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 8217579520
 commitbytes:
 description: \|
 Committed bytes.

 This field is Windows-specific and omitted for Linux containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 0
 commitpeakbytes:
 description: \|
 Peak committed bytes.

 This field is Windows-specific and omitted for Linux containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 0
 privateworkingset:
 description: \|
 Private working set.

 This field is Windows-specific and omitted for Linux containers.
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 0

 ContainerNetworkStats:
 description: \|
 Aggregates the network stats of one container
 type: "object"
 x-go-name: "NetworkStats"
 x-nullable: true
 properties:
 rx\_bytes:
 description: \|
 Bytes received. Windows and Linux.
 type: "integer"
 format: "uint64"
 example: 5338
 rx\_packets:
 description: \|
 Packets received. Windows and Linux.
 type: "integer"
 format: "uint64"
 example: 36
 rx\_errors:
 description: \|
 Received errors. Not used on Windows.

 This field is Linux-specific and always zero for Windows containers.
 type: "integer"
 format: "uint64"
 example: 0
 rx\_dropped:
 description: \|
 Incoming packets dropped. Windows and Linux.
 type: "integer"
 format: "uint64"
 example: 0
 tx\_bytes:
 description: \|
 Bytes sent. Windows and Linux.
 type: "integer"
 format: "uint64"
 example: 1200
 tx\_packets:
 description: \|
 Packets sent. Windows and Linux.
 type: "integer"
 format: "uint64"
 example: 12
 tx\_errors:
 description: \|
 Sent errors. Not used on Windows.

 This field is Linux-specific and always zero for Windows containers.
 type: "integer"
 format: "uint64"
 example: 0
 tx\_dropped:
 description: \|
 Outgoing packets dropped. Windows and Linux.
 type: "integer"
 format: "uint64"
 example: 0
 endpoint\_id:
 description: \|
 Endpoint ID. Not used on Linux.

 This field is Windows-specific and omitted for Linux containers.
 type: "string"
 x-nullable: true
 instance\_id:
 description: \|
 Instance ID. Not used on Linux.

 This field is Windows-specific and omitted for Linux containers.
 type: "string"
 x-nullable: true

 ContainerStorageStats:
 description: \|
 StorageStats is the disk I/O stats for read/write on Windows.

 This type is Windows-specific and omitted for Linux containers.
 type: "object"
 x-go-name: "StorageStats"
 x-nullable: true
 properties:
 read\_count\_normalized:
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 7593984
 read\_size\_bytes:
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 7593984
 write\_count\_normalized:
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 7593984
 write\_size\_bytes:
 type: "integer"
 format: "uint64"
 x-nullable: true
 example: 7593984

 ContainerTopResponse:
 type: "object"
 x-go-name: "TopResponse"
 title: "ContainerTopResponse"
 description: \|-
 Container "top" response.
 properties:
 Titles:
 description: "The ps column titles"
 type: "array"
 items:
 type: "string"
 example:
 Titles:
 \- "UID"
 \- "PID"
 \- "PPID"
 \- "C"
 \- "STIME"
 \- "TTY"
 \- "TIME"
 \- "CMD"
 Processes:
 description: \|-
 Each process running in the container, where each process
 is an array of values corresponding to the titles.
 type: "array"
 items:
 type: "array"
 items:
 type: "string"
 example:
 Processes:
 \-
 \- "root"
 \- "13642"
 \- "882"
 \- "0"
 \- "17:03"
 \- "pts/0"
 \- "00:00:00"
 \- "/bin/bash"
 \-
 \- "root"
 \- "13735"
 \- "13642"
 \- "0"
 \- "17:06"
 \- "pts/0"
 \- "00:00:00"
 \- "sleep 10"


 properties:
 Message:
 description: "Details of an error"
 type: "string"

 SystemVersion:
 type: "object"
 description: \|
 Response of Engine API: GET "/version"
 properties:
 Platform:
 type: "object"
 required: \[Name\]
 properties:
 Name:
 type: "string"
 Components:
 type: "array"
 description: \|
 Information about system components
 items:
 type: "object"
 x-go-name: ComponentVersion
 required: \[Name, Version\]
 properties:
 Name:
 description: \|
 Name of the component
 type: "string"
 example: "Engine"
 Version:
 description: \|
 Version of the component
 type: "string"
 x-nullable: false
 example: "27.0.1"
 Details:
 description: \|
 Key/value pairs of strings with additional information about the
 component. These values are intended for informational purposes
 only, and their content is not defined, and not part of the API
 specification.

 These messages can be printed by the client as information to the user.
 type: "object"
 x-nullable: true
 Version:
 description: "The version of the daemon"
 type: "string"
 example: "27.0.1"
 ApiVersion:
 description: \|
 The default (and highest) API version that is supported by the daemon
 type: "string"
 example: "go1.22.7"
 Os:
 description: \|
 The operating system that the daemon is running on ("linux" or "windows")
 type: "string"
 example: "linux"
 Arch:
 description: \|
 Architecture of the daemon, as returned by the Go runtime (\`GOARCH\`).

 A full list of possible values can be found in the \[Go documentation\](https://go.dev/doc/install/source#environment).
 type: "string"
 example: "amd64"
 KernelVersion:
 description: \|
 The kernel version (\`uname -r\`) that the daemon is running on.

 This field is omitted when empty.
 type: "string"
 example: "6.8.0-31-generic"
 Experimental:
 description: \|
 Indicates if the daemon is started with experimental features enabled.

 This field is omitted when empty / false.
 type: "boolean"
 example: true
 BuildTime:
 description: \|
 The date and time that the daemon was compiled.
 type: "string"
 example: "2020-06-22T15:49:27.000000000+00:00"

 SystemInfo:
 type: "object"
 properties:
 ID:
 description: \|
 Unique identifier of the daemon.



 \> \*\*Note\*\*: The format of the ID itself is not part of the API, and
 \> should not be considered stable.
 type: "string"
 example: "7TRN:IPZB:QYBB:VPBQ:UMPP:KARE:6ZNR:XE6T:7EWV:PKF4:ZOJD:TPYS"
 Containers:
 description: "Total number of containers on the host."
 type: "integer"
 example: 14
 ContainersRunning:
 description: \|
 Number of containers with status \`"running"\`.
 type: "integer"
 example: 3
 ContainersPaused:
 description: \|
 Number of containers with status \`"paused"\`.
 type: "integer"
 example: 1
 ContainersStopped:
 description: \|
 Number of containers with status \`"stopped"\`.
 type: "integer"
 example: 10
 Images:
 description: \|
 Total number of images on the host.

 Both \_tagged\_ and \_untagged\_ (dangling) images are counted.
 type: "integer"
 example: 508
 Driver:
 description: "Name of the storage driver in use."
 type: "string"
 example: "overlay2"
 DriverStatus:
 description: \|
 Information specific to the storage driver, provided as
 "label" / "value" pairs.

 This information is provided by the storage driver, and formatted
 in a way consistent with the output of \`docker info\` on the command
 line.



 \> \*\*Note\*\*: The information returned in this field, including the
 \> formatting of values and labels, should not be considered stable,
 \> and may change without notice.
 type: "array"
 items:
 type: "array"
 items:
 type: "string"
 example:
 \- \["Backing Filesystem", "extfs"\]
 \- \["Supports d\_type", "true"\]
 \- \["Native Overlay Diff", "true"\]
 DockerRootDir:
 description: \|
 Root directory of persistent Docker state.

 Defaults to \`/var/lib/docker\` on Linux, and \`C:\\ProgramData\\docker\`
 on Windows.
 type: "string"
 example: "/var/lib/docker"
 CpuCfsPeriod:
 description: \|
 Indicates if CPU CFS(Completely Fair Scheduler) period is supported by
 the host.
 type: "boolean"
 example: true
 CpuCfsQuota:
 description: \|
 Indicates if CPU CFS(Completely Fair Scheduler) quota is supported by
 the host.
 type: "boolean"
 example: true
 CPUShares:
 description: \|
 Indicates if CPU Shares limiting is supported by the host.
 type: "boolean"
 example: true
 CPUSet:
 description: \|
 Indicates if CPUsets (cpuset.cpus, cpuset.mems) are supported by the host.

 See \[cpuset(7)\](https://www.kernel.org/doc/Documentation/cgroup-v1/cpusets.txt)
 type: "boolean"
 example: true
 PidsLimit:
 description: "Indicates if the host kernel has PID limit support enabled."
 type: "boolean"
 example: true
 OomKillDisable:
 description: "Indicates if OOM killer disable is supported on the host."
 type: "boolean"
 IPv4Forwarding:
 description: "Indicates IPv4 forwarding is enabled."
 type: "boolean"
 example: true
 Debug:
 description: \|
 Indicates if the daemon is running in debug-mode / with debug-level
 logging enabled.
 type: "boolean"
 example: true
 NFd:
 description: \|
 The total number of file Descriptors in use by the daemon process.

 This information is only returned if debug-mode is enabled.
 type: "integer"
 example: 64
 NGoroutines:
 description: \|
 The number of goroutines that currently exist.

 This information is only returned if debug-mode is enabled.
 type: "integer"
 example: 174
 SystemTime:
 description: \|
 Current system-time in \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt)
 format with nano-seconds.
 type: "string"
 example: "2017-08-08T20:28:29.06202363Z"
 LoggingDriver:
 description: \|
 The logging driver to use as a default for new containers.
 type: "string"
 CgroupDriver:
 description: \|
 The driver to use for managing cgroups.
 type: "string"
 enum: \["cgroupfs", "systemd", "none"\]
 default: "cgroupfs"
 example: "cgroupfs"

 example: "6.8.0-31-generic"
 OperatingSystem:
 description: \|
 Name of the host's operating system, for example: "Ubuntu 24.04 LTS"
 or "Windows Server 2016 Datacenter"
 type: "string"
 example: "Ubuntu 24.04 LTS"

 example: "24.04"

 example: "27.0.1"

 FirewallBackend:
 $ref: "#/definitions/FirewallInfo"
 DiscoveredDevices:
 description: \|
 List of devices discovered by device drivers.

 Each device includes information about its source driver, kind, name,
 and additional driver-specific attributes.
 type: "array"
 items:
 $ref: "#/definitions/DeviceInfo"


 SwarmInfo:
 description: \|
 Represents generic information about swarm.
 type: "object"
 properties:
 NodeID:
 description: "Unique identifier of for this node in the swarm."
 type: "string"
 default: ""
 example: "k67qz4598weg5unwwffg6z1m1"
 NodeAddr:
 description: \|
 IP address at which this node can be reached by other nodes in the
 swarm.
 type: "string"
 default: ""
 example: "10.0.0.46"
 LocalNodeState:
 $ref: "#/definitions/LocalNodeState"
 ControlAvailable:
 type: "boolean"
 default: false
 example: true
 Error:
 type: "string"
 default: ""
 RemoteManagers:
 description: \|
 List of ID's and addresses of other managers in the swarm.
 type: "array"
 default: null
 x-nullable: true
 items:
 $ref: "#/definitions/PeerNode"
 example:
 \- NodeID: "71izy0goik036k48jg985xnds"
 Addr: "10.0.0.158:2377"
 \- NodeID: "79y6h1o4gv8n120drcprv5nmc"
 Addr: "10.0.0.159:2377"
 \- NodeID: "k67qz4598weg5unwwffg6z1m1"
 Addr: "10.0.0.46:2377"
 Nodes:
 description: "Total number of nodes in the swarm."
 type: "integer"
 x-nullable: true
 example: 4
 Managers:
 description: "Total number of managers in the swarm."
 type: "integer"
 x-nullable: true
 example: 3
 Cluster:
 $ref: "#/definitions/ClusterInfo"

 LocalNodeState:
 description: "Current local status of this node."
 type: "string"
 default: ""
 enum:
 \- ""
 \- "inactive"
 \- "pending"
 \- "active"
 \- "error"
 \- "locked"
 example: "active"

 PeerNode:
 description: "Represents a peer-node in the swarm"
 type: "object"
 properties:
 NodeID:
 description: "Unique identifier of for this node in the swarm."
 type: "string"
 Addr:
 description: \|
 IP address and ports at which this node can be reached.
 type: "string"

 NetworkAttachmentConfig:
 description: \|
 Specifies how a service should be attached to a particular network.
 type: "object"
 properties:
 Target:
 description: \|
 The target network for attachment. Must be a network name or ID.
 type: "string"
 Aliases:
 description: \|
 Discoverable alternate names for the service on this network.
 type: "array"
 items:
 type: "string"
 DriverOpts:
 description: \|
 Driver attachment options for the network target.
 type: "object"
 additionalProperties:
 type: "string"

 EventActor:
 description: \|
 Actor describes something that generates events, like a container, network,
 or a volume.
 type: "object"
 properties:
 ID:
 description: "The ID of the object emitting the event"
 type: "string"
 example: "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743"
 Attributes:
 description: \|
 Various key/value attributes of the object, depending on its type.
 type: "object"
 additionalProperties:
 type: "string"
 example:
 com.example.some-label: "some-label-value"
 image: "alpine:latest"
 name: "my-container"

 EventMessage:
 description: \|
 EventMessage represents the information an event contains.
 type: "object"
 title: "SystemEventsResponse"
 properties:
 Type:
 description: "The type of object emitting the event"
 type: "string"
 enum: \["builder", "config", "container", "daemon", "image", "network", "node", "plugin", "secret", "service", "volume"\]
 example: "container"
 Action:
 description: "The type of event"
 type: "string"
 example: "create"
 Actor:
 $ref: "#/definitions/EventActor"
 scope:
 description: \|
 Scope of the event. Engine events are \`local\` scope. Cluster (Swarm)
 events are \`swarm\` scope.
 type: "string"
 enum: \["local", "swarm"\]
 time:
 description: "Timestamp of event"
 type: "integer"
 format: "int64"
 example: 1629574695
 timeNano:
 description: "Timestamp of event, with nanosecond accuracy"
 type: "integer"
 format: "int64"
 example: 1629574695515050031

 OCIDescriptor:
 type: "object"
 x-go-name: Descriptor
 description: \|
 A descriptor struct containing digest, media type, and size, as defined in
 the \[OCI Content Descriptors Specification\](https://github.com/opencontainers/image-spec/blob/v1.0.1/descriptor.md).
 properties:
 mediaType:
 description: \|
 The media type of the object this schema refers to.
 type: "string"
 example: "application/vnd.oci.image.manifest.v1+json"
 digest:
 description: \|
 The digest of the targeted content.
 type: "string"
 example: "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96"
 size:
 description: \|
 The size in bytes of the blob.
 type: "integer"
 format: "int64"
 example: 424
 urls:
 description: \|-
 List of URLs from which this object MAY be downloaded.
 type: "array"
 items:
 type: "string"
 format: "uri"
 x-nullable: true
 annotations:
 description: \|-
 Arbitrary metadata relating to the targeted content.
 type: "object"
 x-nullable: true
 additionalProperties:
 type: "string"
 example:
 "com.docker.official-images.bashbrew.arch": "amd64"
 "org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8"
 "org.opencontainers.image.base.name": "scratch"
 "org.opencontainers.image.created": "2025-01-27T00:00:00Z"
 "org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79"
 "org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base"
 "org.opencontainers.image.url": "https://hub.docker.com/\_/ubuntu"
 "org.opencontainers.image.version": "24.04"
 data:
 type: string
 x-nullable: true
 description: \|-
 Data is an embedding of the targeted content. This is encoded as a base64
 string when marshalled to JSON (automatically, by encoding/json). If
 present, Data can be used directly to avoid fetching the targeted content.
 example: null
 platform:
 $ref: "#/definitions/OCIPlatform"
 artifactType:
 description: \|-
 ArtifactType is the IANA media type of this artifact.
 type: "string"
 x-nullable: true
 example: null

 OCIPlatform:
 type: "object"
 x-go-name: Platform
 x-nullable: true
 description: \|
 Describes the platform which the image in the manifest runs on, as defined
 in the \[OCI Image Index Specification\](https://github.com/opencontainers/image-spec/blob/v1.0.1/image-index.md).
 properties:
 architecture:
 description: \|
 The CPU architecture, for example \`amd64\` or \`ppc64\`.
 type: "string"
 example: "arm"
 os:
 description: \|
 The operating system, for example \`linux\` or \`windows\`.
 type: "string"
 example: "windows"
 os.version:
 description: \|
 Optional field specifying the operating system version, for example on
 Windows \`10.0.19041.1165\`.
 type: "string"
 example: "10.0.19041.1165"
 os.features:
 description: \|
 Optional field specifying an array of strings, each listing a required
 OS feature (for example on Windows \`win32k\`).
 type: "array"
 items:
 type: "string"
 example:
 \- "win32k"
 variant:
 description: \|
 Optional field specifying a variant of the CPU, for example \`v7\` to
 specify ARMv7 when architecture is \`arm\`.
 type: "string"
 example: "v7"

 DistributionInspect:
 type: "object"
 x-go-name: DistributionInspect
 title: "DistributionInspectResponse"
 required: \[Descriptor, Platforms\]
 description: \|
 Describes the result obtained from contacting the registry to retrieve
 image metadata.
 properties:
 Descriptor:
 $ref: "#/definitions/OCIDescriptor"
 Platforms:
 type: "array"
 description: \|
 An array containing all platforms supported by the image.
 items:
 $ref: "#/definitions/OCIPlatform"


 tags: \["Image"\]\
 /build:\
 post:\
 summary: "Build an image"\
 description: \|\
 Build an image from a tar archive with a \`Dockerfile\` in it.\
\
 The \`Dockerfile\` specifies how the image is built from the tar archive. It is typically in the archive's root, but can be at a different path or have a different name by specifying the \`dockerfile\` parameter. \[See the \`Dockerfile\` reference for more information\](https://docs.docker.com/engine/reference/builder/).\
\
 The Docker daemon performs a preliminary validation of the \`Dockerfile\` before starting the build, and returns an error if the syntax is incorrect. After that, each instruction is run one-by-one until the ID of the new image is output.\
\
 The build is canceled if the client drops the connection by quitting or being killed.\
 operationId: "ImageBuild"\
 consumes:\
 \- "application/octet-stream"\
 produces:\
 \- "application/json"\
 parameters:\
 \- name: "inputStream"\
 in: "body"\
 description: "A tar archive compressed with one of the following algorithms: identity (no compression), gzip, bzip2, xz."\
 schema:\
 type: "string"\
 format: "binary"\
 \- name: "dockerfile"\
 in: "query"\
 description: "Path within the build context to the \`Dockerfile\`. This is ignored if \`remote\` is specified and points to an external \`Dockerfile\`."\
 type: "string"\
 default: "Dockerfile"\
 \- name: "t"\
 in: "query"\
 description: "A name and optional tag to apply to the image in the \`name:tag\` format. If you omit the tag the default \`latest\` value is assumed. You can provide several \`t\` parameters."\
 type: "string"\
 \- name: "extrahosts"\
 in: "query"\
 description: "Extra hosts to add to /etc/hosts"\
 type: "string"\
 \- name: "remote"\
 in: "query"\
 description: "A Git repository URI or HTTP/HTTPS context URI. If the URI points to a single text file, the file’s contents are placed into a file called \`Dockerfile\` and the image is built from that file. If the URI points to a tarball, the file is downloaded by the daemon and the contents therein used as the context for the build. If the URI points to a tarball and the \`dockerfile\` parameter is also specified, there must be a file with the corresponding path inside the tarball."\
 type: "string"\
 \- name: "q"\
 in: "query"\
 description: "Suppress verbose build output."\
 type: "boolean"\
 default: false\
 \- name: "nocache"\
 in: "query"\
 description: "Do not use the cache when building the image."\
 type: "boolean"\
 default: false\
 \- name: "cachefrom"\
 in: "query"\
 description: "JSON array of images used for build cache resolution."\
 type: "string"\
 \- name: "pull"\
 in: "query"\
 description: "Attempt to pull the image even if an older image exists locally."\
 type: "string"\
 \- name: "rm"\
 in: "query"\
 description: "Remove intermediate containers after a successful build."\
 type: "boolean"\
 default: true\
 \- name: "forcerm"\
 in: "query"\
 description: "Always remove intermediate containers, even upon failure."\
 type: "boolean"\
 default: false\
 \- name: "memory"\
 in: "query"\
 description: "Set memory limit for build."\
 type: "integer"\
 \- name: "memswap"\
 in: "query"\
 description: "Total memory (memory + swap). Set as \`-1\` to disable swap."\
 type: "integer"\
 \- name: "cpushares"\
 in: "query"\
 description: "CPU shares (relative weight)."\
 type: "integer"\
 \- name: "cpusetcpus"\
 in: "query"\
 description: "CPUs in which to allow execution (e.g., \`0-3\`, \`0,1\`)."\
 type: "string"\
 \- name: "cpuperiod"\
 in: "query"\
 description: "The length of a CPU period in microseconds."\
 type: "integer"\
 \- name: "cpuquota"\
 in: "query"\
 description: "Microseconds of CPU time that the container can get in a CPU period."\
 type: "integer"\
 \- name: "buildargs"\
 in: "query"\
 description: >\
 JSON map of string pairs for build-time variables. Users pass these values at build-time. Docker\
 uses the buildargs as the environment context for commands run via the \`Dockerfile\` RUN\
 instruction, or for variable expansion in other \`Dockerfile\` instructions. This is not meant for\
 passing secret values.\
\
 For example, the build arg \`FOO=bar\` would become \`{"FOO":"bar"}\` in JSON. This would result in the\
 query parameter \`buildargs={"FOO":"bar"}\`. Note that \`{"FOO":"bar"}\` should be URI component encoded.\
\
 \[Read more about the buildargs instruction.\](https://docs.docker.com/engine/reference/builder/#arg)\
 type: "string"\
 \- name: "shmsize"\
 in: "query"\
 description: "Size of \`/dev/shm\` in bytes. The size must be greater than 0. If omitted the system uses 64MB."\
 type: "integer"\
 \- name: "squash"\
 in: "query"\
 description: "Squash the resulting images layers into a single layer. \*(Experimental release only.)\*"\
 type: "boolean"\
 \- name: "labels"\
 in: "query"\
 description: "Arbitrary key/value labels to set on the image, as a JSON map of string pairs."\
 type: "string"\
 \- name: "networkmode"\
 in: "query"\
 description: \|\
 Sets the networking mode for the run commands during build. Supported\
 standard values are: \`bridge\`, \`host\`, \`none\`, and \`container:\`.\
 Any other value is taken as a custom network's name or ID to which this\
 container should connect to.\
 type: "string"\
 \- name: "Content-type"\
 in: "header"\
 type: "string"\
 enum:\
 \- "application/x-tar"\
 default: "application/x-tar"\
 \- name: "X-Registry-Config"\
 in: "header"\
 description: \|\
 This is a base64-encoded JSON object with auth configurations for multiple registries that a build may refer to.\
\
 The key is a registry URL, and the value is an auth configuration object, \[as described in the authentication section\](#section/Authentication). For example:\
\
 \`\`\`\
 {\
 "docker.example.com": {\
 "username": "janedoe",\
 "password": "hunter2"\
 },\
 "https://index.docker.io/v1/": {\
 "username": "mobydock",\
 "password": "conta1n3rize14"\
 }\
 }\
 \`\`\`\
\
 Only the registry domain name (and port if not the default 443) are required. However, for legacy reasons, the Docker Hub registry must be specified with both a \`https://\` prefix and a \`/v1/\` suffix even though Docker will prefer to use the v2 registry API.\
 type: "string"\
 \- name: "platform"\
 in: "query"\
 description: "Platform in the format os\[/arch\[/variant\]\]"\
 type: "string"\
 default: ""\
 \- name: "target"\
 in: "query"\
 description: "Target build stage"\
 type: "string"\
 default: ""\
 \- name: "outputs"\
 in: "query"\
 description: \|\
 BuildKit output configuration in the format of a stringified JSON array of objects.\
 Each object must have two top-level properties: \`Type\` and \`Attrs\`.\
 The \`Type\` property must be set to 'moby'.\
 The \`Attrs\` property is a map of attributes for the BuildKit output configuration.\
 See https://docs.docker.com/build/exporters/oci-docker/ for more information.\
\
 Example:\
\
 \`\`\`\
 \[{"Type":"moby","Attrs":{"type":"image","force-compression":"true","compression":"zstd"}}\]\
 \`\`\`\
 type: "string"\
 default: ""\
 \- name: "version"\
 in: "query"\
 type: "string"\
 default: "1"\
 enum: \["1", "2"\]\
 description: \|\
 Version of the builder backend to use.\
\
 \- \`1\` is the first generation classic (deprecated) builder in the Docker daemon (default)\
 \- \`2\` is \[BuildKit\](https://github.com/moby/buildkit)\
 responses:\
 200:\
 description: "no error"\
 400:\
 description: "Bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Image"\]\
 /build/prune:\
 post:\
 summary: "Delete builder cache"\
 produces:\
 \- "application/json"\
 operationId: "BuildPrune"\
 parameters:\
 \- name: "reserved-space"\
 in: "query"\
 description: "Amount of disk space in bytes to keep for cache"\
 type: "integer"\
 format: "int64"\
 \- name: "max-used-space"\
 in: "query"\
 description: "Maximum amount of disk space allowed to keep for cache"\
 type: "integer"\
 format: "int64"\
 \- name: "min-free-space"\
 in: "query"\
 description: "Target amount of free disk space after pruning"\
 type: "integer"\
 format: "int64"\
 \- name: "all"\
 in: "query"\
 type: "boolean"\
 description: "Remove all types of build cache"\
 \- name: "filters"\
 in: "query"\
 type: "string"\
 description: \|\
 A JSON encoded value of the filters (a \`map\[string\]\[\]string\`) to\
 process on the list of build cache objects.\
\
 Available filters:\
\
 \- \`until=\` remove cache older than \`\`. The \`\` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. \`10m\`, \`1h30m\`) computed relative to the daemon's local time.\
 \- \`id=\`\
 \- \`parent=\`\
 \- \`type=\`\
 \- \`description=\`\
 \- \`inuse\`\
 \- \`shared\`\
 \- \`private\`\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "object"\
 title: "BuildPruneResponse"\
 properties:\
 CachesDeleted:\
 type: "array"\
 items:\
 description: "ID of build cache object"\
 type: "string"\
 SpaceReclaimed:\
 description: "Disk space reclaimed in bytes"\
 type: "integer"\
 format: "int64"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Image"\]\
 /images/create:\
 post:\
 summary: "Create an image"\
 description: "Pull or import an image."\
 operationId: "ImageCreate"\
 consumes:\
 \- "text/plain"\
 \- "application/octet-stream"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "no error"\
 404:\
 description: "repository does not exist or no read access"\
 \- name: "fromImage"\
 in: "query"\
 description: \|\
 Name of the image to pull. If the name includes a tag or digest, specific behavior applies:\
\
 \- If only \`fromImage\` includes a tag, that tag is used.\
 \- If both \`fromImage\` and \`tag\` are provided, \`tag\` takes precedence.\
 \- If \`fromImage\` includes a digest, the image is pulled by digest, and \`tag\` is ignored.\
 \- If neither a tag nor digest is specified, all tags are pulled.\
 type: "string"\
 \- name: "fromSrc"\
 in: "query"\
 description: "Source to import. The value may be a URL from which the image can be retrieved or \`-\` to read the image from the request body. This parameter may only be used when importing an image."\
 type: "string"\
 \- name: "repo"\
 in: "query"\
 description: "Repository name given to an image when it is imported. The repo may include a tag. This parameter may only be used when importing an image."\
 type: "string"\
 \- name: "tag"\
 in: "query"\
 description: "Tag or digest. If empty when pulling an image, this causes all tags for the given image to be pulled."\
 type: "string"\
 \- name: "message"\
 in: "query"\
 description: "Set commit message for imported image."\
 type: "string"\
 \- name: "inputImage"\
 in: "body"\
 description: "Image content if the value \`-\` has been specified in fromSrc query parameter"\
 schema:\
 type: "string"\
 required: false\
 \- name: "X-Registry-Auth"\
 in: "header"\
 description: \|\
 A base64url-encoded auth configuration.\
\
 Refer to the \[authentication section\](#section/Authentication) for\
 details.\
 type: "string"\
 \- name: "changes"\
 in: "query"\
 description: \|\
 Apply \`Dockerfile\` instructions to the image that is created,\
 for example: \`changes=ENV DEBUG=true\`.\
 Note that \`ENV DEBUG=true\` should be URI component encoded.\
\
 Supported \`Dockerfile\` instructions:\
 \`CMD\`\|\`ENTRYPOINT\`\|\`ENV\`\|\`EXPOSE\`\|\`ONBUILD\`\|\`USER\`\|\`VOLUME\`\|\`WORKDIR\`\
 type: "array"\
 items:\
 type: "string"\
 \- name: "platform"\
 in: "query"\
 type: "string"\
 default: ""\
 tags: \["Image"\]\
 /images/{name}/json:\
 get:\
 summary: "Inspect an image"\
 description: "Return low-level information about an image."\
 operationId: "ImageInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 $ref: "#/definitions/ImageInspect"\
 404:\
 description: "No such image"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 examples:\
 application/json:\
 message: "No such image: someimage (tag: latest)"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: "Image name or id"\
 type: "string"\
 required: true\
 \- name: "manifests"\
 in: "query"\
 tags: \["Image"\]\
 /images/{name}/history:\
 get:\
 summary: "Get the history of an image"\
 description: "Return parent layers of an image."\
 operationId: "ImageHistory"\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "List of image layers"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/ImageHistoryResponseItem"\
 examples:\
 application/json:\
 \- Id: "3db9c44f45209632d6050b35958829c3a2aa256d81b9a7be45b362ff85c54710"\
 Created: 1398108230\
 CreatedBy: "/bin/sh -c #(nop) ADD file:eb15dbd63394e063b805a3c32ca7bf0266ef64676d5a6fab4801f2e81e2a5148 in /"\
 Tags:\
 \- "ubuntu:lucid"\
 \- "ubuntu:10.04"\
 Size: 182964289\
 Comment: ""\
 \- Id: "6cfa4d1f33fb861d4d114f43b25abd0ac737509268065cdfd69d544a59c85ab8"\
 Created: 1398108222\
 CreatedBy: "/bin/sh -c #(nop) MAINTAINER Tianon Gravi  \- mkimage-debootstrap.sh -i iproute,iputils-ping,ubuntu-minimal -t lucid.tar.xz lucid http://archive.ubuntu.com/ubuntu/"\
 Tags: \[\]\
 Size: 0\
 Comment: ""\
 \- Id: "511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158"\
 Created: 1371157430\
 CreatedBy: ""\
 Tags:\
 \- "scratch12:latest"\
 \- "scratch:latest"\
 Size: 0\
 Comment: "Imported from -"\
 404:\
 description: "No such image"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: "Image name or ID"\
 type: "string"\
 required: true\
 \- name: "platform"\
 type: "string"\
 in: "query"\
 description: \|\
 JSON-encoded OCI platform to select the platform-variant.\
 If omitted, it defaults to any locally available platform,\
 prioritizing the daemon's host platform.\
\
 If the daemon provides a multi-platform image store, this selects\
 the platform-variant to show the history for. If the image is\
 a single-platform image, or if the multi-platform image does not\
 provide a variant matching the given platform, an error is returned.\
\
 Example: \`{"os": "linux", "architecture": "arm", "variant": "v5"}\`\
 tags: \["Image"\]\
 /images/{name}/push:\
 post:\
 summary: "Push an image"\
 description: \|\
 Push an image to a registry.\
\
 If you wish to push an image on to a private registry, that image must\
 already have a tag which references the registry. For example,\
 \`registry.example.com/myimage:latest\`.\
\
 The push is cancelled if the HTTP connection is closed.\
 operationId: "ImagePush"\
 consumes:\
 \- "application/octet-stream"\
 responses:\
 200:\
 description: "No error"\
 404:\
 description: "No such image"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: \|\
 Name of the image to push. For example, \`registry.example.com/myimage\`.\
 The image must be present in the local image store with the same name.\
\
 The name should be provided without tag; if a tag is provided, it\
 is ignored. For example, \`registry.example.com/myimage:latest\` is\
 considered equivalent to \`registry.example.com/myimage\`.\
\
 Use the \`tag\` parameter to specify the tag to push.\
 type: "string"\
 required: true\
 \- name: "tag"\
 in: "query"\
 description: \|\
 Tag of the image to push. For example, \`latest\`. If no tag is provided,\
 all tags of the given image that are present in the local image store\
 are pushed.\
 type: "string"\
 \- name: "platform"\
 type: "string"\
 in: "query"\
 description: \|\
 JSON-encoded OCI platform to select the platform-variant to push.\
 If not provided, all available variants will attempt to be pushed.\
\
 If the daemon provides a multi-platform image store, this selects\
 the platform-variant to push to the registry. If the image is\
 a single-platform image, or if the multi-platform image does not\
 provide a variant matching the given platform, an error is returned.\
\
 Example: \`{"os": "linux", "architecture": "arm", "variant": "v5"}\`\
 \- name: "X-Registry-Auth"\
 in: "header"\
 description: \|\
 A base64url-encoded auth configuration.\
\
 Refer to the \[authentication section\](#section/Authentication) for\
 details.\
 type: "string"\
 required: true\
 tags: \["Image"\]\
 /images/{name}/tag:\
 post:\
 summary: "Tag an image"\
 description: \|\
 Create a tag that refers to a source image.\
\
 This creates an additional reference (tag) to the source image. The tag\
 can include a different repository name and/or tag. If the repository\
 or tag already exists, it will be overwritten.\
 operationId: "ImageTag"\
 responses:\
 201:\
 description: "No error"\
 400:\
 description: "Bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "No such image"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 409:\
 description: "Conflict"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: "Image name or ID to tag."\
 type: "string"\
 required: true\
 \- name: "repo"\
 in: "query"\
 description: "The repository to tag in. For example, \`someuser/someimage\`."\
 type: "string"\
 \- name: "tag"\
 in: "query"\
 description: "The name of the new tag."\
 type: "string"\
 tags: \["Image"\]\
 /images/{name}:\
 delete:\
 summary: "Remove an image"\
 description: \|\
 Remove an image, along with any untagged parent images that were\
 referenced by that image.\
\
 Images can't be removed if they have descendant images, are being\
 used by a running container or are being used by a build.\
 operationId: "ImageDelete"\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "The image was deleted successfully"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/ImageDeleteResponseItem"\
 examples:\
 application/json:\
 \- Untagged: "3e2f21a89f"\
 \- Deleted: "3e2f21a89f"\
 \- Deleted: "53b4f83ac9"\
 404:\
 description: "No such image"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 409:\
 description: "Conflict"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: "Image name or ID"\
 type: "string"\
 required: true\
 \- name: "force"\
 in: "query"\
 description: "Remove the image even if it is being used by stopped containers or has other tags"\
 type: "boolean"\
 default: false\
 \- name: "noprune"\
 in: "query"\
 description: "Do not delete untagged parent images"\
 type: "boolean"\
 default: false\
 \- name: "platforms"\
 in: "query"\
 description: \|\
 Select platform-specific content to delete.\
 Multiple values are accepted.\
 Each platform is a OCI platform encoded as a JSON string.\
 type: "array"\
 items:\
 # This should be OCIPlatform\
 # but $ref is not supported for array in query in Swagger 2.0\
 # $ref: "#/definitions/OCIPlatform"\
 type: "string"\
 tags: \["Image"\]\
 /images/search:\
 get:\
 summary: "Search images"\
 description: "Search for an image on Docker Hub."\
 operationId: "ImageSearch"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "array"\
 items:\
 type: "object"\
 title: "ImageSearchResponseItem"\
 properties:\
 description:\
 type: "string"\
 is\_official:\
 type: "boolean"\
 is\_automated:\
 description: \|\
 Whether this repository has automated builds enabled.\
\
\
\
 type: "string"\
 tags: \["Image"\]\
 /images/prune:\
 post:\
 summary: "Delete unused images"\
 produces:\
 \- "application/json"\
 operationId: "ImagePrune"\
 parameters:\
 \- name: "filters"\
 in: "query"\
 description: \|\
 Filters to process on the prune list, encoded as JSON (a \`map\[string\]\[\]string\`). Available filters:\
\
 \- \`dangling=\` When set to \`true\` (or \`1\`), prune only\
 unused \*and\* untagged images. When set to \`false\`\
 (or \`0\`), all unused images are pruned.\
 \- \`until=\` Prune images created before this timestamp. The \`\` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. \`10m\`, \`1h30m\`) computed relative to the daemon machine’s time.\
 \- \`label\` (\`label=\`, \`label==\`, \`label!=\`, or \`label!==\`) Prune images with (or without, in case \`label!=...\` is used) the specified labels.\
 type: "string"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "object"\
 title: "ImagePruneResponse"\
 properties:\
 ImagesDeleted:\
 description: "Images that were deleted"\
 type: "array"\
 items:\
 $ref: "#/definitions/ImageDeleteResponseItem"\
 SpaceReclaimed:\
 description: "Disk space reclaimed in bytes"\
 type: "integer"\
 format: "int64"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Image"\]\
 /auth:\
 post:\
 summary: "Check auth configuration"\
 description: \|\
 Validate credentials for a registry and, if available, get an identity\
 token for accessing the registry without password.\
 operationId: "SystemAuth"\
 consumes: \["application/json"\]\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "An identity token was generated successfully."\
 schema:\
 $ref: "#/definitions/AuthResponse"\
 204:\
 description: "No error"\
 401:\
 description: "Auth error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "authConfig"\
 in: "body"\
 description: "Authentication to check"\
 schema:\
 $ref: "#/definitions/AuthConfig"\
 tags: \["System"\]\
 /info:\
 get:\
 summary: "Get system information"\
 operationId: "SystemInfo"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 $ref: "#/definitions/SystemInfo"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["System"\]\
 /version:\
 get:\
 summary: "Get version"\
 description: "Returns the version of Docker that is running and various information about the system that Docker is running on."\
 operationId: "SystemVersion"\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/SystemVersion"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["System"\]\
 /\_ping:\
 get:\
 summary: "Ping"\
 description: "This is a dummy endpoint you can use to test if the server is accessible."\
 operationId: "SystemPing"\
 produces: \["text/plain"\]\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "string"\
 example: "OK"\
 headers:\
 Api-Version:\
 type: "string"\
 description: "Max API Version the server supports"\
 Builder-Version:\
 type: "string"\
 $ref: "#/definitions/IDResponse"\
 Images report these events: \`create\`, \`delete\`, \`import\`, \`load\`, \`pull\`, \`push\`, \`save\`, \`tag\`, \`untag\`, and \`prune\`\
\
 operationId: "SystemEvents"\
 produces:\
 \- "application/x-ndjson"\
 \- "application/json-seq"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/EventMessage"\
 parameters:\
 \- name: "since"\
 in: "query"\
 description: "Show events created since this timestamp then stream new events."\
 type: "string"\
 \- name: "until"\
 in: "query"\
 description: "Show events created until this timestamp then stop streaming."\
 type: "string"\
 \- name: "filters"\
 in: "query"\
 description: \|\
 A JSON encoded value of filters (a \`map\[string\]\[\]string\`) to process on the event list. Available filters:\
\
 \- \`config=\` config name or ID\
 \- \`container=\` container name or ID\
 \- \`daemon=\` daemon name or ID\
 \- \`event=\` event type\
 \- \`image=\` image name or ID\
 \- \`label=\` image or container label\
 \- \`network=\` network name or ID\
 \- \`node=\` node ID\
 \- \`plugin\`= plugin name or ID\
 \- \`scope\`= local or swarm\
 \- \`secret=\` secret name or ID\
 \- \`service=\` service name or ID\
 \- \`type=\` object to filter by, one of \`container\`, \`image\`, \`volume\`, \`network\`, \`daemon\`, \`plugin\`, \`node\`, \`service\`, \`secret\` or \`config\`\
 \- \`volume=\` volume name\
 type: "string"\
 tags: \["System"\]\
 /system/df:\
 get:\
 summary: "Get data usage information"\
 operationId: "SystemDataUsage"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "object"\
 title: "SystemDataUsageResponse"\
 properties:\
 ImageUsage:\
 $ref: "#/definitions/ImagesDiskUsage"\
 ContainerUsage:\
 $ref: "#/definitions/ContainersDiskUsage"\
 VolumeUsage:\
 $ref: "#/definitions/VolumesDiskUsage"\
 BuildCacheUsage:\
 $ref: "#/definitions/BuildCacheDiskUsage"\
 \- name: "verbose"\
 in: "query"\
 description: \|\
 Show detailed information on space usage.\
 type: "boolean"\
 default: false\
 tags: \["System"\]\
 /images/{name}/get:\
 get:\
 summary: "Export an image"\
 description: \|\
 Get a tarball containing all images and metadata for a repository.\
\
 If \`name\` is a specific name and tag (e.g. \`ubuntu:latest\`), then only that image (and its parents) are returned. If \`name\` is an image ID, similarly only that image (and its parents) are returned, but with the exclusion of the \`repositories\` file in the tarball, as there were no image names referenced.\
\
 ### Image tarball format\
\
 An image tarball contains \[Content as defined in the OCI Image Layout Specification\](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-layout.md#content).\
\
 Additionally, includes the manifest.json file associated with a backwards compatible docker save format.\
\
 If the tarball defines a repository, the tarball should also include a \`repositories\` file at the root that contains a list of repository and tag names mapped to layer IDs.\
\
 \`\`\`json\
 {\
 "hello-world": {\
 "latest": "565a9d68a73f6706862bfe8409a7f659776d4d60a8d096eb4a3cbce6999cc2a1"\
 }\
 }\
 \`\`\`\
 operationId: "ImageGet"\
 produces:\
 \- "application/x-tar"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "string"\
 format: "binary"\
 description: "Image name or ID"\
 type: "string"\
 required: true\
 \- name: "platform"\
 type: "array"\
 items:\
 type: "string"\
 collectionFormat: "multi"\
 in: "query"\
 description: \|\
 JSON encoded OCI platform describing a platform which will be used\
 to select a platform-specific image to be saved if the image is\
 multi-platform.\
 If not provided, the full multi-platform image will be saved.\
\
 Example: \`{"os": "linux", "architecture": "arm", "variant": "v5"}\`\
 tags: \["Image"\]\
 /images/get:\
 get:\
 summary: "Export several images"\
 description: \|\
 Get a tarball containing all images and metadata for several image\
 repositories.\
\
 For each value of the \`names\` parameter: if it is a specific name and\
 tag (e.g. \`ubuntu:latest\`), then only that image (and its parents) are\
 returned; if it is an image ID, similarly only that image (and its parents)\
 are returned and there would be no names referenced in the 'repositories'\
 file for this image ID.\
\
 For details on the format, see the \[export image endpoint\](#operation/ImageGet).\
 operationId: "ImageGetAll"\
 produces:\
 \- "application/x-tar"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "string"\
 format: "binary"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "names"\
 in: "query"\
 description: "Image names to filter by"\
 type: "array"\
 items:\
 type: "string"\
 \- name: "platform"\
 type: "array"\
 items:\
 type: "string"\
 collectionFormat: "multi"\
 in: "query"\
 description: \|\
 JSON encoded OCI platform(s) which will be used to select the\
 platform-specific image(s) to be saved if the image is\
 multi-platform. If not provided, the full multi-platform image\
 will be saved.\
\
 Example: \`{"os": "linux", "architecture": "arm", "variant": "v5"}\`\
 tags: \["Image"\]\
 /images/load:\
 post:\
 summary: "Import images"\
 description: \|\
 Load a set of images and tags into a repository.\
\
 For details on the format, see the \[export image endpoint\](#operation/ImageGet).\
 operationId: "ImageLoad"\
 consumes:\
 \- "application/x-tar"\
 produces:\
 \- "application/json"\
 parameters:\
 \- name: "imagesTarball"\
 in: "body"\
 description: "Tar archive containing images"\
 schema:\
 type: "string"\
 format: "binary"\
 \- name: "quiet"\
 in: "query"\
 description: "Suppress progress details during load."\
 type: "boolean"\
 default: false\
 \- name: "platform"\
 type: "array"\
 items:\
 type: "string"\
 collectionFormat: "multi"\
 in: "query"\
 description: \|\
 JSON encoded OCI platform(s) which will be used to select the\
 platform-specific image(s) to load if the image is\
 multi-platform. If not provided, the full multi-platform image\
 will be loaded.\
\
 Example: \`{"os": "linux", "architecture": "arm", "variant": "v5"}\`\
 tags: \["Image"\]\
 /containers/{id}/exec:\
 post:\
 summary: "Create an exec instance"\
 description: "Run a command inside a running container."\
 operationId: "ContainerExec"\
 $ref: "#/definitions/IDResponse"\
 409:\
 description: "container is paused"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "execConfig"\
 in: "body"\
 description: "Exec configuration"\
 schema:\
 type: "object"\
 title: "ExecConfig"\
 properties:\
 AttachStdin:\
 type: "boolean"\
 description: "Attach to \`stdin\` of the exec command."\
 AttachStdout:\
 type: "boolean"\
 description: "Attach to \`stdout\` of the exec command."\
 AttachStderr:\
 type: "boolean"\
 description: "Attach to \`stderr\` of the exec command."\
 example: \[80, 64\]\
 example: false\
 Tty:\
 type: "boolean"\
 description: "Allocate a pseudo-TTY."\
 example: true\
 example: \[80, 64\]\
 \- name: "id"\
 in: "path"\
 description: "Exec instance ID"\
 required: true\
 type: "string"\
 tags: \["Exec"\]\
 /exec/{id}/resize:\
 post:\
 summary: "Resize an exec instance"\
 description: \|\
 Resize the TTY session used by an exec instance. This endpoint only works\
 if \`tty\` was specified as part of creating and starting the exec instance.\
 operationId: "ExecResize"\
 responses:\
 200:\
 description: "No error"\
 400:\
 description: "bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "No such exec instance"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "id"\
 in: "path"\
 description: "Exec instance ID"\
 required: true\
 type: "string"\
 \- name: "h"\
 in: "query"\
 required: true\
 description: "Height of the TTY session in characters"\
 type: "integer"\
 \- name: "w"\
 in: "query"\
 required: true\
 description: "Width of the TTY session in characters"\
 type: "integer"\
 tags: \["Exec"\]\
 /exec/{id}/json:\
 get:\
 summary: "Inspect an exec instance"\
 description: "Return low-level information about an exec instance."\
 operationId: "ExecInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "object"\
 title: "ExecInspectResponse"\
 properties:\
 CanRemove:\
 type: "boolean"\
 DetachKeys:\
 type: "string"\
 ID:\
 type: "string"\
 Running:\
 type: "boolean"\
 ExitCode:\
 type: "integer"\
 ProcessConfig:\
 $ref: "#/definitions/ProcessConfig"\
 OpenStdin:\
 type: "boolean"\
 OpenStderr:\
 type: "boolean"\
 OpenStdout:\
 type: "boolean"\
 ContainerID:\
 type: "string"\
 Pid:\
 type: "integer"\
 description: "The system process ID for the exec process."\
 examples:\
 application/json:\
 CanRemove: false\
 ContainerID: "b53ee82b53a40c7dca428523e34f741f3abc51d9f297a14ff874bf761b995126"\
 DetachKeys: ""\
 ExitCode: 2\
 ID: "f33bbfb39f5b142420f4759b2348913bd4a8d1a6d7fd56499cb41a1bb91d7b3b"\
 OpenStderr: true\
 OpenStdin: true\
 OpenStdout: true\
 ProcessConfig:\
 arguments:\
 \- "-c"\
 \- "exit 2"\
 entrypoint: "sh"\
 privileged: false\
 tty: true\
 user: "1000"\
 Running: false\
 Pid: 42000\
 404:\
 description: "No such exec instance"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "id"\
 in: "path"\
 description: "Exec instance ID"\
 required: true\
 type: "string"\
 tags: \["Exec"\]\
\
 /volumes:\
 get:\
 summary: "List volumes"\
 operationId: "VolumeList"\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "Summary volume data that matches the query"\
 schema:\
 $ref: "#/definitions/VolumeListResponse"\
 description: \|\
 JSON encoded value of the filters (a \`map\[string\]\[\]string\`) to\
 process on the volumes list. Available filters:\
\
 \- \`dangling=\` When set to \`true\` (or \`1\`), returns all\
 volumes that are not in use by a container. When set to \`false\`\
 (or \`0\`), only volumes that are in use by one or more\
 containers are returned.\
 \- \`driver=\` Matches volumes based on their driver.\
 \- \`label=\` or \`label=:\` Matches volumes based on\
 the presence of a \`label\` alone or a \`label\` and a value.\
 \- \`name=\` Matches all or part of a volume name.\
 type: "string"\
 format: "json"\
 tags: \["Volume"\]\
\
 /volumes/create:\
 post:\
 summary: "Create a volume"\
 operationId: "VolumeCreate"\
 consumes: \["application/json"\]\
 produces: \["application/json"\]\
 responses:\
 201:\
 description: "The volume was created successfully"\
 schema:\
 $ref: "#/definitions/Volume"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "volumeConfig"\
 in: "body"\
 required: true\
 description: "Volume configuration"\
 schema:\
 $ref: "#/definitions/VolumeCreateRequest"\
 tags: \["Volume"\]\
\
 /volumes/{name}:\
 get:\
 summary: "Inspect a volume"\
 operationId: "VolumeInspect"\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "No error"\
 schema:\
 $ref: "#/definitions/Volume"\
 404:\
 description: "No such volume"\
 tags: \["Volume"\]\
\
 type: "string"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "object"\
 title: "VolumePruneResponse"\
 properties:\
 VolumesDeleted:\
 description: "Volumes that were deleted"\
 type: "array"\
 items:\
 type: "string"\
 SpaceReclaimed:\
 description: "Disk space reclaimed in bytes"\
 type: "integer"\
 format: "int64"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Volume"\]\
 /networks:\
 get:\
 summary: "List networks"\
 description: \|\
 Returns a list of networks. For details on the format, see the\
 \[network inspect endpoint\](#operation/NetworkInspect).\
\
 Note that it uses a different, smaller representation of a network than\
 inspecting a single network. For example, the list of containers attached\
 to the network is not propagated in API versions 1.28 and up.\
 operationId: "NetworkList"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/NetworkSummary"\
 examples:\
 application/json:\
 \- Name: "bridge"\
 Id: "f2de39df4171b0dc801e8002d1d999b77256983dfc63041c0f34030aa3977566"\
 Created: "2016-10-19T06:21:00.416543526Z"\
 Scope: "local"\
 Driver: "bridge"\
 description: \|\
 JSON encoded value of the filters (a \`map\[string\]\[\]string\`) to process\
 on the networks list.\
\
 Available filters:\
\
 \- \`dangling=\` When set to \`true\` (or \`1\`), returns all\
 networks that are not in use by a container. When set to \`false\`\
 (or \`0\`), only networks that are in use by one or more\
 containers are returned.\
 \- \`driver=\` Matches a network's driver.\
 \- \`id=\` Matches all or part of a network ID.\
 \- \`label=\` or \`label==\` of a network label.\
 \- \`name=\` Matches all or part of a network name.\
 \- \`scope=\["swarm"\|"global"\|"local"\]\` Filters networks by scope (\`swarm\`, \`global\`, or \`local\`).\
 \- \`type=\["custom"\|"builtin"\]\` Filters networks by type. The \`custom\` keyword returns all user-defined networks.\
 type: "string"\
 tags: \["Network"\]\
\
 /networks/{id}:\
 get:\
 summary: "Inspect a network"\
 operationId: "NetworkInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 $ref: "#/definitions/NetworkInspect"\
 404:\
 description: "Network not found"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "id"\
 in: "path"\
 description: "Network ID or name"\
 required: true\
 type: "string"\
 \- name: "verbose"\
 in: "query"\
 description: "Detailed inspect output for troubleshooting"\
 type: "boolean"\
 default: false\
 \- name: "scope"\
 in: "query"\
 description: "Filter the network by scope (swarm, global, or local)"\
 type: "string"\
 tags: \["Network"\]\
\
 delete:\
 summary: "Remove a network"\
 operationId: "NetworkDelete"\
 responses:\
 204:\
 description: "No error"\
 403:\
 description: "operation not supported for pre-defined networks"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "no such network"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "id"\
 in: "path"\
 description: "Network ID or name"\
 required: true\
 type: "string"\
 tags: \["Network"\]\
\
 /networks/create:\
 post:\
 summary: "Create a network"\
 operationId: "NetworkCreate"\
 consumes:\
 \- "application/json"\
 produces:\
 \- "application/json"\
 responses:\
 201:\
 description: "Network created successfully"\
 schema:\
 $ref: "#/definitions/NetworkCreateResponse"\
 400:\
 description: "bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 403:\
 description: \|\
 Forbidden operation. This happens when trying to create a network named after a pre-defined network,\
 or when trying to create an overlay network on a daemon which is not part of a Swarm cluster.\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "plugin not found"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "networkConfig"\
 in: "body"\
 description: "Network configuration"\
 required: true\
 schema:\
 type: "object"\
 title: "NetworkCreateRequest"\
 required: \["Name"\]\
 properties:\
 Name:\
 description: "The network's name."\
 type: "string"\
 example: "my\_network"\
 EnableIPv4:\
 description: "Enable IPv4 on the network."\
 com.example.some-label: "some-value"\
 com.example.some-other-label: "some-other-value"\
 tags: \["Network"\]\
\
 /networks/{id}/connect:\
 post:\
 summary: "Connect a container to a network"\
 description: "The network must be either a local-scoped network or a swarm-scoped network with the \`attachable\` option set. A network cannot be re-attached to a running container"\
 operationId: "NetworkConnect"\
 consumes:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 400:\
 description: "bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 403:\
 description: "Operation forbidden"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "Network or container not found"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "id"\
 in: "path"\
 description: "Network ID or name"\
 required: true\
 type: "string"\
 \- name: "container"\
 in: "body"\
 required: true\
 schema:\
 $ref: "#/definitions/NetworkConnectRequest"\
 tags: \["Network"\]\
\
 /networks/{id}/disconnect:\
 post:\
 summary: "Disconnect a container from a network"\
 operationId: "NetworkDisconnect"\
 consumes:\
 \- "application/json"\
 responses:\
 200:\
 description: "No error"\
 403:\
 description: "Operation not supported for swarm scoped networks"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "Network or container not found"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "id"\
 in: "path"\
 description: "Network ID or name"\
 required: true\
 type: "string"\
 \- name: "container"\
 in: "body"\
 required: true\
 schema:\
 $ref: "#/definitions/NetworkDisconnectRequest"\
 $ref: "#/definitions/ServiceCreateResponse"\
 400:\
 description: "bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 403:\
 description: "network is not eligible for services"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 409:\
 description: "name conflicts with an existing service"\
 allOf:\
 \- $ref: "#/definitions/ServiceSpec"\
 \- type: "object"\
 example:\
 Name: "web"\
 TaskTemplate:\
 ContainerSpec:\
 Image: "nginx:alpine"\
 Mounts:\
 -\
 ReadOnly: true\
 Source: "web-data"\
 Target: "/usr/share/nginx/html"\
 Type: "volume"\
 VolumeOptions:\
 DriverConfig: {}\
 Labels:\
 com.example.something: "something-value"\
 Hosts: \["10.10.10.10 host1", "ABCD:EF01:2345:6789:ABCD:EF01:2345:6789 host2"\]\
 User: "33"\
 DNSConfig:\
 Nameservers: \["8.8.8.8"\]\
 Search: \["example.org"\]\
 Options: \["timeout:3"\]\
 Secrets:\
 -\
 File:\
 Name: "www.example.org.key"\
 UID: "33"\
 GID: "33"\
 Mode: 384\
 SecretID: "fpjqlhnwb19zds35k8wn80lq9"\
 SecretName: "example\_org\_domain\_key"\
 OomScoreAdj: 0\
 LogDriver:\
 Name: "json-file"\
 Options:\
 max-file: "3"\
 max-size: "10M"\
 Placement: {}\
 Resources:\
 Limits:\
 MemoryBytes: 104857600\
 Reservations: {}\
 RestartPolicy:\
 Condition: "on-failure"\
 Delay: 10000000000\
 MaxAttempts: 10\
 Mode:\
 Replicated:\
 Replicas: 4\
 Ports:\
 -\
 Protocol: "tcp"\
 PublishedPort: 8080\
 TargetPort: 80\
 Labels:\
 foo: "bar"\
 tags: \["Service"\]\
 /services/{id}:\
 get:\
 summary: "Inspect a service"\
 operationId: "ServiceInspect"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Service"\
 404:\
 description: "no such service"\
 description: "ID or name of service."\
 required: true\
 type: "string"\
 \- name: "insertDefaults"\
 in: "query"\
 description: "Fill empty fields with default values."\
 type: "boolean"\
 default: false\
 tags: \["Service"\]\
 delete:\
 summary: "Delete a service"\
 operationId: "ServiceDelete"\
 responses:\
 200:\
 description: "no error"\
 404:\
 description: "no such service"\
 description: "ID or name of service."\
 required: true\
 type: "string"\
 tags: \["Service"\]\
 /services/{id}/update:\
 post:\
 summary: "Update a service"\
 operationId: "ServiceUpdate"\
 consumes: \["application/json"\]\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/ServiceUpdateResponse"\
 400:\
 description: "bad parameter"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 404:\
 description: "no such service"\
 description: "ID or name of service."\
 required: true\
 type: "string"\
 \- name: "body"\
 in: "body"\
 required: true\
 schema:\
 allOf:\
 \- $ref: "#/definitions/ServiceSpec"\
 \- type: "object"\
 example:\
 Name: "top"\
 TaskTemplate:\
 ContainerSpec:\
 Image: "busybox"\
 Args:\
 \- "top"\
 OomScoreAdj: 0\
 description: "no such task"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 examples:\
 application/json:\
 message: "No such task: c2ada9df5af8"\
 description: "ID of the task"\
 type: "string"\
 \- name: "details"\
 in: "query"\
 description: "Show task context and extra details provided to logs."\
 tags: \["Task"\]\
 /secrets:\
 get:\
 summary: "List secrets"\
 operationId: "SecretList"\
 $ref: "#/definitions/Secret"\
 example:\
 \- ID: "blt1owaxmitz71s9v5zh81zun"\
 Version:\
 Index: 85\
 CreatedAt: "2017-07-20T13:55:28.678958722Z"\
 UpdatedAt: "2017-07-20T13:55:28.678958722Z"\
 Spec:\
 Name: "mysql-passwd"\
 Labels:\
 some.label: "some.value"\
 Driver:\
 Name: "secret-bucket"\
 Options:\
 OptionA: "value for driver option A"\
 OptionB: "value for driver option B"\
 \- ID: "ktnbjxoalbkvbvedmg1urrz8h"\
 Version:\
 Index: 11\
 CreatedAt: "2016-11-05T01:20:17.327670065Z"\
 UpdatedAt: "2016-11-05T01:20:17.327670065Z"\
 Spec:\
 Name: "app-dev.crt"\
 Labels:\
 foo: "bar"\
 process on the secrets list.\
\
 Available filters:\
\
 \- \`id=\`\
 \- \`label= or label==value\`\
 \- \`name=\`\
 \- \`names=\`\
 tags: \["Secret"\]\
 /secrets/create:\
 post:\
 summary: "Create a secret"\
 operationId: "SecretCreate"\
 $ref: "#/definitions/IDResponse"\
 409:\
 description: "name conflicts with an existing object"\
 parameters:\
 \- name: "body"\
 in: "body"\
 schema:\
 allOf:\
 \- $ref: "#/definitions/SecretSpec"\
 \- type: "object"\
 example:\
 Name: "app-key.crt"\
 Labels:\
 foo: "bar"\
 Data: "VEhJUyBJUyBOT1QgQSBSRUFMIENFUlRJRklDQVRFCg=="\
 Driver:\
 Name: "secret-bucket"\
 Options:\
 OptionA: "value for driver option A"\
 OptionB: "value for driver option B"\
 tags: \["Secret"\]\
 /secrets/{id}:\
 get:\
 summary: "Inspect a secret"\
 operationId: "SecretInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Secret"\
 examples:\
 application/json:\
 ID: "ktnbjxoalbkvbvedmg1urrz8h"\
 Version:\
 Index: 11\
 CreatedAt: "2016-11-05T01:20:17.327670065Z"\
 UpdatedAt: "2016-11-05T01:20:17.327670065Z"\
 Spec:\
 Name: "app-dev.crt"\
 Labels:\
 foo: "bar"\
 Driver:\
 Name: "secret-bucket"\
 Options:\
 OptionA: "value for driver option A"\
 OptionB: "value for driver option B"\
\
 404:\
 description: "secret not found"\
 required: true\
 type: "string"\
 description: "ID of the secret"\
 tags: \["Secret"\]\
 delete:\
 summary: "Delete a secret"\
 operationId: "SecretDelete"\
 produces:\
 \- "application/json"\
 responses:\
 204:\
 description: "no error"\
 404:\
 description: "secret not found"\
 required: true\
 type: "string"\
 description: "ID of the secret"\
 tags: \["Secret"\]\
 /secrets/{id}/update:\
 post:\
 summary: "Update a Secret"\
 operationId: "SecretUpdate"\
 description: "no such secret"\
 description: "The ID or name of the secret"\
 type: "string"\
 required: true\
 \- name: "body"\
 in: "body"\
 schema:\
 $ref: "#/definitions/SecretSpec"\
 description: \|\
 The spec of the secret to update. Currently, only the Labels field\
 can be updated. All other fields must remain unchanged from the\
 \[SecretInspect endpoint\](#operation/SecretInspect) response values.\
 \- name: "version"\
 in: "query"\
 description: \|\
 The version number of the secret object being updated. This is\
 required to avoid conflicting writes.\
 type: "integer"\
 format: "int64"\
 required: true\
 tags: \["Secret"\]\
 /configs:\
 get:\
 summary: "List configs"\
 operationId: "ConfigList"\
 $ref: "#/definitions/Config"\
 example:\
 \- ID: "ktnbjxoalbkvbvedmg1urrz8h"\
 Version:\
 Index: 11\
 CreatedAt: "2016-11-05T01:20:17.327670065Z"\
 UpdatedAt: "2016-11-05T01:20:17.327670065Z"\
 Spec:\
 Name: "server.conf"\
 process on the configs list.\
\
 Available filters:\
\
 \- \`id=\`\
 \- \`label= or label==value\`\
 \- \`name=\`\
 \- \`names=\`\
 tags: \["Config"\]\
 /configs/create:\
 post:\
 summary: "Create a config"\
 operationId: "ConfigCreate"\
 $ref: "#/definitions/IDResponse"\
 409:\
 description: "name conflicts with an existing object"\
 parameters:\
 \- name: "body"\
 in: "body"\
 schema:\
 allOf:\
 \- $ref: "#/definitions/ConfigSpec"\
 \- type: "object"\
 example:\
 Name: "server.conf"\
 Labels:\
 foo: "bar"\
 Data: "VEhJUyBJUyBOT1QgQSBSRUFMIENFUlRJRklDQVRFCg=="\
 tags: \["Config"\]\
 /configs/{id}:\
 get:\
 summary: "Inspect a config"\
 operationId: "ConfigInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Config"\
 examples:\
 application/json:\
 ID: "ktnbjxoalbkvbvedmg1urrz8h"\
 Version:\
 Index: 11\
 CreatedAt: "2016-11-05T01:20:17.327670065Z"\
 UpdatedAt: "2016-11-05T01:20:17.327670065Z"\
 Spec:\
 Name: "app-dev.crt"\
 404:\
 description: "config not found"\
 required: true\
 type: "string"\
 description: "ID of the config"\
 tags: \["Config"\]\
 delete:\
 summary: "Delete a config"\
 operationId: "ConfigDelete"\
 produces:\
 \- "application/json"\
 responses:\
 204:\
 description: "no error"\
 404:\
 description: "config not found"\
 required: true\
 type: "string"\
 description: "ID of the config"\
 tags: \["Config"\]\
 /configs/{id}/update:\
 post:\
 summary: "Update a Config"\
 operationId: "ConfigUpdate"\
 description: "no such config"\
 description: "The ID or name of the config"\
 type: "string"\
 required: true\
 \- name: "body"\
 in: "body"\
 schema:\
 $ref: "#/definitions/ConfigSpec"\
 description: \|\
 The spec of the config to update. Currently, only the Labels field\
 can be updated. All other fields must remain unchanged from the\
 \[ConfigInspect endpoint\](#operation/ConfigInspect) response values.\
 \- name: "version"\
 in: "query"\
 description: \|\
 The version number of the config object being updated. This is\
 required to avoid conflicting writes.\
 type: "integer"\
 format: "int64"\
 required: true\
 tags: \["Config"\]\
 /distribution/{name}/json:\
 get:\
 summary: "Get image information from the registry"\
 description: \|\
 Return image digest and platform information by contacting the registry.\
 operationId: "DistributionInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "descriptor and platform information"\
 schema:\
 $ref: "#/definitions/DistributionInspect"\
 401:\
 description: "Failed authentication or no image found"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 examples:\
 application/json:\
 message: "No such image: someimage (tag: latest)"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: "Image name or id"\
 type: "string"\
 required: true\
 tags: \["Distribution"\]\
 /session:\
 post:\
 summary: "Initialize interactive session"\
 description: \|\
 Start a new interactive session with a server. Session allows server to\
 call back to the client for advanced capabilities.\
\
 ### Hijacking\
\
 This endpoint hijacks the HTTP connection to HTTP2 transport that allows\
 the client to expose gPRC services on that connection.\
\
 For example, the client sends this request to upgrade the connection:\
\
 \`\`\`\
 POST /session HTTP/1.1\
 Upgrade: h2c\
 Connection: Upgrade\
 \`\`\`\
\
 The Docker daemon responds with a \`101 UPGRADED\` response follow with\
 the raw stream:\
\
 \`\`\`\
 HTTP/1.1 101 UPGRADED\
 Connection: Upgrade\
 Upgrade: h2c\
 \`\`\`\
 operationId: "Session"\
 produces:\
 \- "application/vnd.docker.raw-stream"\
 responses:\
 101:\
 description: "no error, hijacking successful"\
 tags: \["Session"\]

----
url: https://docs.docker.com/docker-hub/repos/manage/builds/link-source/
----

# Configure automated builds from GitHub and BitBucket

***

Table of contents

***

> Warning
>
> Docker Hub Automated Builds is a deprecated feature. It will be fully retired on April 1, 2027.

> Note
>
> Automated builds require a Docker Pro, Team, or Business subscription.

To automate building and testing of your images, you link to your hosted source code service to Docker Hub so that it can access your source code repositories. You can configure this link for user accounts or organizations.

If you are linking a source code provider to create autobuilds for a team, follow the instructions to [create a service account](https://docs.docker.com/docker-hub/repos/manage/builds/setup/#service-users-for-team-autobuilds) for the team before linking the account as described below.

## [Link to a GitHub user account](#link-to-a-github-user-account)

1. Sign in to Docker Hub.

2. Select **My Hub** > **Settings** > **Linked accounts**.

3. Select **Link provider** for the source provider you want to link.

   If you want to unlink your current GitHub account and relink to a new GitHub account, make sure to completely sign out of [GitHub](https://github.com/) before linking via Docker Hub.

4. Review the settings for the **Docker Hub Builder** OAuth application.

   > Note
   >
   > If you are the owner of any GitHub organizations, you might see options to grant Docker Hub access to them from this screen. You can also individually edit an organization's third-party access settings to grant or revoke Docker Hub's access. See [Grant access to a GitHub organization](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#grant-access-to-a-github-organization) to learn more.

5. Select **Authorize docker** to save the link.

### [Grant access to a GitHub organization](#grant-access-to-a-github-organization)

If you are the owner of a GitHub organization, you can grant or revoke Docker Hub's access to the organization's repositories. Depending on the GitHub organization's settings, you may need to be an organization owner.

If the organization has not had specific access granted or revoked before, you can often grant access at the same time as you link your user account. In this case, a **Grant access** button appears next to the organization name in the link accounts screen, as shown below. If this button does not appear, you must manually grant the application's access.

To manually grant Docker Hub access to a GitHub organization:

1. Link your user account using the instructions above.

2. From your GitHub Account settings, locate the **Organization settings** section at the lower left.

3. Select the organization you want to give Docker Hub access to.

4. Select **Third-party access**.

   The page displays a list of third party applications and their access status.

5. Select the pencil icon next to **Docker Hub Builder**.

6. Select **Grant access** next to the organization.

### [Revoke access to a GitHub organization](#revoke-access-to-a-github-organization)

To revoke Docker Hub's access to an organization's GitHub repositories:

1. From your GitHub Account settings, locate the **Organization settings** section at the lower left.

2. Select the organization you want to revoke Docker Hub's access to.

3. From the Organization Profile menu, select **Third-party access**. The page displays a list of third party applications and their access status.

4. Select the pencil icon next to Docker Hub Builder.

5. On the next page, select **Deny access**.

### [Unlink a GitHub user account](#unlink-a-github-user-account)

To revoke Docker Hub's access to your GitHub account, you must unlink it both from Docker Hub, and from your GitHub account.

1. Select **My Hub** > **Settings** > **Linked accounts**.

2. Select **Unlink provider** next to the source provider you want to remove.

3. Go to your GitHub account's **Settings** page.

4. Select **Applications** in the left navigation bar.

5. Select the `...` menu to the right of the Docker Hub Builder application and select **Revoke**.

> Note
>
> Each repository that is configured as an automated build source contains a webhook that notifies Docker Hub of changes in the repository. This webhook is not automatically removed when you revoke access to a source code provider.

## [Link to a Bitbucket user account](#link-to-a-bitbucket-user-account)

1. Sign in to Docker Hub using your Docker ID.

2. Select **My Hub** > **Settings** > **Linked accounts**.

3. Select **Link provider** for the source provider you want to link.

4. If necessary, sign in to Bitbucket.

5. On the page that appears, select **Grant access**.

### [Unlink a Bitbucket user account](#unlink-a-bitbucket-user-account)

To permanently revoke Docker Hub's access to your Bitbucket account, you must unlink it both from Docker Hub, and revoke authorization in your Bitbucket account.

1. Sign in to Docker Hub.

2. Select **My Hub** > **Settings** > **Linked accounts**.

3. Select **Unlink provider** next to the source provider you want to remove.

> Important
>
> After unlinking the account on Docker Hub, you must also revoke the authorization on the Bitbucket end.

To revoke authorization in your Bitbucket account:

1. Go to your Bitbucket account and navigate to [**Bitbucket settings**](https://bitbucket.org/account/settings/app-authorizations/).

2. On the page that appears, select **OAuth**.

3. Select **Revoke** next to the Docker Hub line.

> Note
>
> Each repository that is configured as an automated build source contains a webhook that notifies Docker Hub of changes in the repository. This webhook is not automatically removed when you revoke access to a source code provider.

----
url: https://docs.docker.com/engine/logging/drivers/journald/
----

# Journald logging driver

***

Table of contents

***

The `journald` logging driver sends container logs to the [`systemd` journal](https://www.freedesktop.org/software/systemd/man/systemd-journald.service.html). Log entries can be retrieved using the `journalctl` command, through use of the `journal` API, or using the `docker logs` command.

In addition to the text of the log message itself, the `journald` log driver stores the following metadata in the journal with each message:

| Field                                | Description                                                                                                                                           |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CONTAINER_ID`                       | The container ID truncated to 12 characters.                                                                                                          |
| `CONTAINER_ID_FULL`                  | The full 64-character container ID.                                                                                                                   |
| `CONTAINER_NAME`                     | The container name at the time it was started. If you use `docker rename` to rename a container, the new name isn't reflected in the journal entries. |
| `CONTAINER_TAG`, `SYSLOG_IDENTIFIER` | The container tag ([log tag option documentation](https://docs.docker.com/engine/logging/log_tags/)).                                                 |
| `CONTAINER_PARTIAL_MESSAGE`          | A field that flags log integrity. Improve logging of long log lines.                                                                                  |
| `IMAGE_NAME`                         | The name of the container image.                                                                                                                      |

## [Usage](#usage)

To use the `journald` driver as the default logging driver, set the `log-driver` and `log-opts` keys to appropriate values in the `daemon.json` file. For more about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

The following example sets the log driver to `journald`:

```json
{
  "log-driver": "journald"
}
```

Restart Docker for the changes to take effect.

To configure the logging driver for a specific container, use the `--log-driver` flag on the `docker run` command.

```console
$ docker run --log-driver=journald ...
```

## [Options](#options)

Use the `--log-opt NAME=VALUE` flag to specify additional `journald` logging driver options.

| Option         | Required | Description                                                                                                                                                                                                        |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `tag`          | optional | Specify template to set `CONTAINER_TAG` and `SYSLOG_IDENTIFIER` value in journald logs. Refer to [log tag option documentation](https://docs.docker.com/engine/logging/log_tags/) to customize the log tag format. |
| `labels`       | optional | Comma-separated list of keys of labels, which should be included in message, if these labels are specified for the container.                                                                                      |
| `labels-regex` | optional | Similar to and compatible with labels. A regular expression to match logging-related labels. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                |
| `env`          | optional | Comma-separated list of keys of environment variables, which should be included in message, if these variables are specified for the container.                                                                    |
| `env-regex`    | optional | Similar to and compatible with `env`. A regular expression to match logging-related environment variables. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                  |

If a collision occurs between `label` and `env` options, the value of the `env` takes precedence. Each option adds additional fields to the attributes of a logging message.

The following is an example of the logging options required to log to journald.

```console
$ docker run \
    --log-driver=journald \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    --label location=west \
    your/application
```

This configuration also directs the driver to include in the payload the label location, and the environment variable `TEST`. If the `--env "TEST=false"` or `--label location=west` arguments were omitted, the corresponding key would not be set in the journald log.

## [Note regarding container names](#note-regarding-container-names)

The value logged in the `CONTAINER_NAME` field is the name of the container that was set at startup. If you use `docker rename` to rename a container, the new name isn't reflected in the journal entries. Journal entries continue to use the original name.

## [Retrieve log messages with `journalctl`](#retrieve-log-messages-with-journalctl)

Use the `journalctl` command to retrieve log messages. You can apply filter expressions to limit the retrieved messages to those associated with a specific container:

```console
$ sudo journalctl CONTAINER_NAME=webserver
```

You can use additional filters to further limit the messages retrieved. The `-b` flag only retrieves messages generated since the last system boot:

```console
$ sudo journalctl -b CONTAINER_NAME=webserver
```

The `-o` flag specifies the format for the retrieved log messages. Use `-o json` to return the log messages in JSON format.

```console
$ sudo journalctl -o json CONTAINER_NAME=webserver
```

### [View logs for a container with a TTY enabled](#view-logs-for-a-container-with-a-tty-enabled)

If TTY is enabled on a container you may see `[10B blob data]` in the output when retrieving log messages. The reason for that is that `\r` is appended to the end of the line and `journalctl` doesn't strip it automatically unless `--all` is set:

```console
$ sudo journalctl -b CONTAINER_NAME=webserver --all
```

## [Retrieve log messages with the `journal` API](#retrieve-log-messages-with-the-journal-api)

This example uses the `systemd` Python module to retrieve container logs:

```python
import systemd.journal

reader = systemd.journal.Reader()
reader.add_match('CONTAINER_NAME=web')

for msg in reader:
    print '{CONTAINER_ID_FULL}: {MESSAGE}'.format(**msg)
```

----
url: https://docs.docker.com/reference/cli/docker/login/
----

# docker login

***

| Description | Authenticate to a registry        |
| ----------- | --------------------------------- |
| Usage       | `docker login [OPTIONS] [SERVER]` |

## [Description](#description)

Authenticate to a registry.

You can authenticate to any public or private registry for which you have credentials. Authentication may be required for pulling and pushing images. Other commands, such as `docker scout` and `docker build`, may also require authentication to access subscription-only features or data related to your Docker organization.

Authentication credentials are stored in the configured [credential store](#credential-stores). If you use Docker Desktop, credentials are automatically saved to the native keychain of your operating system. If you're not using Docker Desktop, you can configure the credential store in the Docker configuration file, which is located at `$HOME/.docker/config.json` on Linux or `%USERPROFILE%/.docker/config.json` on Windows. If you don't configure a credential store, Docker stores credentials in the `config.json` file in a base64-encoded format. This method is less secure than configuring and using a credential store.

`docker login` also supports [credential helpers](#credential-helpers) to help you handle credentials for specific registries.

### [Authentication methods](#authentication-methods)

You can authenticate to a registry using a username and access token or password. Docker Hub also supports a web-based sign-in flow, which signs you in to your Docker account without entering your password. For Docker Hub, the `docker login` command uses a device code flow by default, unless the `--username` flag is specified. The device code flow is a secure way to sign in. See [Authenticate to Docker Hub using device code](#authenticate-to-docker-hub-with-web-based-login).

### [Credential stores](#credential-stores)

The Docker Engine can keep user credentials in an external credential store, such as the native keychain of the operating system. Using an external store is more secure than storing credentials in the Docker configuration file.

To use a credential store, you need an external helper program to interact with a specific keychain or external store. Docker requires the helper program to be in the client's host `$PATH`.

You can download the helpers from the `docker-credential-helpers` [releases page](https://github.com/docker/docker-credential-helpers/releases). Helpers are available for the following credential stores:

* D-Bus Secret Service
* Apple macOS keychain
* Microsoft Windows Credential Manager
* [pass](https://www.passwordstore.org/)

With Docker Desktop, the credential store is already installed and configured for you. Unless you want to change the credential store used by Docker Desktop, you can skip the following steps.

#### [Configure the credential store](#configure-the-credential-store)

You need to specify the credential store in `$HOME/.docker/config.json` to tell the Docker Engine to use it. The value of the config property should be the suffix of the program to use (i.e. everything after `docker-credential-`). For example, to use `docker-credential-osxkeychain`:

```json
{
  "credsStore": "osxkeychain"
}
```

If you are currently logged in, run `docker logout` to remove the credentials from the file and run `docker login` again.

#### [Default behavior](#default-behavior)

By default, Docker looks for the native binary on each of the platforms, i.e. `osxkeychain` on macOS, `wincred` on Windows, and `pass` on Linux. A special case is that on Linux, Docker will fall back to the `secretservice` binary if it cannot find the `pass` binary. If none of these binaries are present, it stores the base64-encoded credentials in the `config.json` configuration file.

#### [Credential helper protocol](#credential-helper-protocol)

Credential helpers can be any program or script that implements the credential helper protocol. This protocol is inspired by Git, but differs in the information shared.

The helpers always use the first argument in the command to identify the action. There are only three possible values for that argument: `store`, `get`, and `erase`.

The `store` command takes a JSON payload from the standard input. That payload carries the server address, to identify the credential, the username, and either a password or an identity token.

```json
{
  "ServerURL": "https://index.docker.io/v1",
  "Username": "david",
  "Secret": "passw0rd1"
}
```

If the secret being stored is an identity token, the Username should be set to `<token>`.

The `store` command can write error messages to `STDOUT` that the Docker Engine will show if there was an issue.

The `get` command takes a string payload from the standard input. That payload carries the server address that the Docker Engine needs credentials for. This is an example of that payload: `https://index.docker.io/v1`.

The `get` command writes a JSON payload to `STDOUT`. Docker reads the user name and password from this payload:

```json
{
  "Username": "david",
  "Secret": "passw0rd1"
}
```

The `erase` command takes a string payload from `STDIN`. That payload carries the server address that the Docker Engine wants to remove credentials for. This is an example of that payload: `https://index.docker.io/v1`.

The `erase` command can write error messages to `STDOUT` that the Docker Engine will show if there was an issue.

### [Credential helpers](#credential-helpers)

Credential helpers are similar to [credential stores](#credential-stores), but act as the designated programs to handle credentials for specific registries. The default credential store will not be used for operations concerning credentials of the specified registries.

#### [Configure credential helpers](#configure-credential-helpers)

If you are currently logged in, run `docker logout` to remove the credentials from the default store.

Credential helpers are specified in a similar way to `credsStore`, but allow for multiple helpers to be configured at a time. Keys specify the registry domain, and values specify the suffix of the program to use (i.e. everything after `docker-credential-`). For example:

```json
{
  "credHelpers": {
    "myregistry.example.com": "secretservice",
    "docker.internal.example": "pass",
  }
}
```

## [Options](#options)

| Option                                | Default | Description                                                 |
| ------------------------------------- | ------- | ----------------------------------------------------------- |
| `-p, --password`                      |         | Password or Personal Access Token (PAT)                     |
| [`--password-stdin`](#password-stdin) |         | Take the Password or Personal Access Token (PAT) from stdin |
| [`-u, --username`](#username)         |         | Username                                                    |

## [Examples](#examples)

### [Authenticate to Docker Hub with web-based login](#authenticate-to-docker-hub-with-web-based-login)

By default, the `docker login` command authenticates to Docker Hub, using a device code flow. This flow lets you authenticate to Docker Hub without entering your password. Instead, you visit a URL in your web browser, enter a code, and authenticate.

```console
$ docker login

USING WEB-BASED LOGIN
To sign in with credentials on the command line, use 'docker login -u <username>'

Your one-time device confirmation code is: LNFR-PGCJ
Press ENTER to open your browser or submit your device code here: https://login.docker.com/activate

Waiting for authentication in the browser…
```

After entering the code in your browser, you are authenticated to Docker Hub using the account you're currently signed in with on the Docker Hub website or in Docker Desktop. If you aren't signed in, you are prompted to sign in after entering the device code.

### [Authenticate to a self-hosted registry](#authenticate-to-a-self-hosted-registry)

If you want to authenticate to a self-hosted registry you can specify this by adding the server name.

```console
$ docker login registry.example.com
```

By default, the `docker login` command assumes that the registry listens on port 443 or 80. If the registry listens on a different port, you can specify it by adding the port number to the server name.

```console
$ docker login registry.example.com:1337
```

> Note
>
> Registry addresses should not include URL path components, only the hostname and (optionally) the port. Registry addresses with URL path components may result in an error. For example, `docker login registry.example.com/foo/` is incorrect, while `docker login registry.example.com` is correct.
>
> The exception to this rule is the Docker Hub registry, which may use the `/v1/` path component in the address for historical reasons.

### [Authenticate to a registry with a username and password](#username)

To authenticate to a registry with a username and password, you can use the `--username` or `-u` flag. The following example authenticates to Docker Hub with the username `moby`. The password is entered interactively.

```console
$ docker login -u moby
```

### [Provide a password using STDIN (--password-stdin)](#password-stdin)

To run the `docker login` command non-interactively, you can set the `--password-stdin` flag to provide a password through `STDIN`. Using `STDIN` prevents the password from ending up in the shell's history, or log-files.

The following example reads a password from a file, and passes it to the `docker login` command using `STDIN`:

```console
$ cat ~/my_password.txt | docker login --username foo --password-stdin
```

----
url: https://docs.docker.com/ai/gordon/how-to/docker-desktop/
----

# Using Gordon in Docker Desktop

***

Table of contents

***

Requires: Docker Desktop [4.74.0](https://docs.docker.com/desktop/release-notes/#4740) or later

Gordon is integrated into Docker Desktop. Access it from the sidebar to open the Gordon view.

## [Basic usage](#basic-usage)

To access Gordon:

1. Open Docker Desktop and sign in to your Docker account.
2. Select **Gordon** in the sidebar.
3. Type your question or request in the input field.
4. Press `Enter` or select the send button.

Gordon responds in the chat view and maintains context throughout the session.

## [Working directory](#working-directory)

The working directory sets the default context for Gordon's file operations. Select your working directory when you start Gordon or use the directory icon to change it during a conversation:

1. Select the directory icon in the Gordon input area.
2. Browse and select a different directory.

## [Contextual help](#contextual-help)

The Gordon icon appears throughout Docker Desktop. Selecting it opens Gordon pre-loaded with context about the item you are working with, such as container logs or build output.

## [Usage indicator](#usage-indicator)

Docker Desktop shows a usage indicator so you can see how close you are to your tier limit. See [Usage limits and tiers](https://docs.docker.com/ai/gordon/usage-limits/) for details.

## [Disabling Gordon](#disabling-gordon)

To disable Gordon:

1. Open Docker Desktop Settings.
2. Navigate to the **AI** section.
3. Clear the **Enable Gordon** option.
4. Select **Apply**.

## [Configure tools](#configure-tools)

You can control which tools Gordon has access to. See [Configure tools](https://docs.docker.com/ai/gordon/how-to/configure-tools/) for details on enabling, disabling, and fine-tuning tool permissions.

----
url: https://docs.docker.com/reference/cli/docker/buildx/history/ls/
----

# docker buildx history ls

***

| Description | List build records                   |
| ----------- | ------------------------------------ |
| Usage       | `docker buildx history ls [OPTIONS]` |

## [Description](#description)

List completed builds recorded by the active builder. Each entry includes the build ID, name, status, timestamp, and duration.

By default, only records for the current builder are shown. You can filter results using flags.

## [Options](#options)

| Option                    | Default | Description                                  |
| ------------------------- | ------- | -------------------------------------------- |
| [`--filter`](#filter)     |         | Provide filter values (e.g., `status=error`) |
| [`--format`](#format)     | `table` | Format the output                            |
| [`--local`](#local)       |         | List records for current repository only     |
| [`--no-trunc`](#no-trunc) |         | Don't truncate output                        |

## [Examples](#examples)

### [List all build records for the current builder](#list-all-build-records-for-the-current-builder)

```console
$ docker buildx history ls
BUILD ID                    NAME           STATUS     CREATED AT        DURATION
qu2gsuo8ejqrwdfii23xkkckt   .dev/2850      Completed  3 days ago        1.4s
qsiifiuf1ad9pa9qvppc0z1l3   .dev/2850      Completed  3 days ago        1.3s
g9808bwrjrlkbhdamxklx660b   .dev/3120      Completed  5 days ago        2.1s
```

### [List failed builds (--filter)](#filter)

```console
docker buildx history ls --filter status=error
```

You can filter the list using the `--filter` flag. Supported filters include:

| Filter                                 | Supported comparisons                            | Example                    |
| -------------------------------------- | ------------------------------------------------ | -------------------------- |
| `ref`, `repository`, `status`          | Support `=` and `!=` comparisons                 | `--filter status!=success` |
| `startedAt`, `completedAt`, `duration` | Support `<` and `>` comparisons with time values | `--filter duration>30s`    |

You can combine multiple filters by repeating the `--filter` flag:

```console
docker buildx history ls --filter status=error --filter duration>30s
```

### [List builds from the current project (--local)](#local)

```console
docker buildx history ls --local
```

### [Display full output without truncation (--no-trunc)](#no-trunc)

```console
docker buildx history ls --no-trunc
```

### [Format output (--format)](#format)

#### [JSON output](#json-output)

```console
$ docker buildx history ls --format json
[
  {
    "ID": "qu2gsuo8ejqrwdfii23xkkckt",
    "Name": ".dev/2850",
    "Status": "Completed",
    "CreatedAt": "2025-04-15T12:33:00Z",
    "Duration": "1.4s"
  },
  {
    "ID": "qsiifiuf1ad9pa9qvppc0z1l3",
    "Name": ".dev/2850",
    "Status": "Completed",
    "CreatedAt": "2025-04-15T12:29:00Z",
    "Duration": "1.3s"
  }
]
```

#### [Go template output](#go-template-output)

```console
$ docker buildx history ls --format '{{.Name}} - {{.Duration}}'
.dev/2850 - 1.4s
.dev/2850 - 1.3s
.dev/3120 - 2.1s
```

----
url: https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/create-project/
----

# Set up the project

***

Table of contents

***

## [Background](#background)

This guide builds on top of Microsoft's [Integration tests in ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/test/integration-tests) documentation. The original sample uses an in-memory SQLite database as the backing store for integration tests. You'll replace SQLite with a real Microsoft SQL Server instance running in a Docker container using Testcontainers.

You can find the original code sample in the [dotnet/AspNetCore.Docs.Samples](https://github.com/dotnet/AspNetCore.Docs.Samples/tree/main/test/integration-tests/IntegrationTestsSample) repository.

## [Clone the repository](#clone-the-repository)

Clone the Testcontainers guide repository and change into the project directory:

```console
$ git clone https://github.com/testcontainers/tc-guide-testing-aspnet-core.git
$ cd tc-guide-testing-aspnet-core
```

## [Project structure](#project-structure)

The solution contains two projects:

```text
RazorPagesProject.sln
├── src/RazorPagesProject/              # ASP.NET Core Razor Pages app
└── tests/RazorPagesProject.Tests/      # xUnit integration tests
```

### [Application project](#application-project)

The application project (`src/RazorPagesProject/RazorPagesProject.csproj`) is a Razor Pages web app that uses Entity Framework Core with SQLite as its default database provider:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.UI" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="7.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

</Project>
```

The `ApplicationDbContext` stores `Message` entities and provides methods to query and manage them:

```csharp
public class ApplicationDbContext : IdentityDbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Message> Messages { get; set; }

    public async virtual Task<List<Message>> GetMessagesAsync()
    {
        return await Messages
            .OrderBy(message => message.Text)
            .AsNoTracking()
            .ToListAsync();
    }

    public async virtual Task AddMessageAsync(Message message)
    {
        await Messages.AddAsync(message);
        await SaveChangesAsync();
    }

    public async virtual Task DeleteAllMessagesAsync()
    {
        foreach (Message message in Messages)
        {
            Messages.Remove(message);
        }

        await SaveChangesAsync();
    }

    public async virtual Task DeleteMessageAsync(int id)
    {
        var message = await Messages.FindAsync(id);

        if (message != null)
        {
            Messages.Remove(message);
            await SaveChangesAsync();
        }
    }

    public void Initialize()
    {
        Messages.AddRange(GetSeedingMessages());
        SaveChanges();
    }

    public static List<Message> GetSeedingMessages()
    {
        return new List<Message>()
        {
            new Message(){ Text = "You're standing on my scarf." },
            new Message(){ Text = "Would you like a jelly baby?" },
            new Message(){ Text = "To the rational mind, nothing is inexplicable; only unexplained." }
        };
    }
}
```

### [Test project](#test-project)

The test project (`tests/RazorPagesProject.Tests/RazorPagesProject.Tests.csproj`) includes xUnit, the ASP.NET Core testing infrastructure, and the Testcontainers MSSQL module:

```xml
<Project Sdk="Microsoft.NET.Sdk.Web">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="AngleSharp" Version="0.17.1" />
    <PackageReference Include="Microsoft.AspNetCore.Diagnostics.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Identity.UI" Version="7.0.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="7.0.0" />
    <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="7.0.0">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>

    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.4.0" />

    <PackageReference Include="Testcontainers.MsSql" Version="3.0.0" />
    <PackageReference Include="xunit" Version="2.4.2" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.4.5">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
    </PackageReference>
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\RazorPagesProject\RazorPagesProject.csproj" />
  </ItemGroup>

  <ItemGroup>
    <Content Update="xunit.runner.json">
      <CopyToOutputDirectory>Always</CopyToOutputDirectory>
    </Content>
  </ItemGroup>

</Project>
```

The key dependencies are:

* `Microsoft.AspNetCore.Mvc.Testing` - provides `WebApplicationFactory` for bootstrapping the app in tests
* `Microsoft.EntityFrameworkCore.SqlServer` - the SQL Server database provider for Entity Framework Core
* `Testcontainers.MsSql` - the Testcontainers module for Microsoft SQL Server

### [Existing SQLite-based test factory](#existing-sqlite-based-test-factory)

The original project includes a `CustomWebApplicationFactory` that replaces the application's database with an in-memory SQLite instance:

```csharp
public class CustomWebApplicationFactory<TProgram>
    : WebApplicationFactory<TProgram> where TProgram : class
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            var dbContextDescriptor = services.SingleOrDefault(
                d => d.ServiceType ==
                    typeof(DbContextOptions<ApplicationDbContext>));

            services.Remove(dbContextDescriptor);

            var dbConnectionDescriptor = services.SingleOrDefault(
                d => d.ServiceType ==
                    typeof(DbConnection));

            services.Remove(dbConnectionDescriptor);

            // Create open SqliteConnection so EF won't automatically close it.
            services.AddSingleton<DbConnection>(container =>
            {
                var connection = new SqliteConnection("DataSource=:memory:");
                connection.Open();

                return connection;
            });

            services.AddDbContext<ApplicationDbContext>((container, options) =>
            {
                var connection = container.GetRequiredService<DbConnection>();
                options.UseSqlite(connection);
            });
        });

        builder.UseEnvironment("Development");
    }
}
```

While this approach works, SQLite has behavioral differences from the database you'd use in production. In the next section, you'll replace it with a Testcontainers-managed Microsoft SQL Server instance.

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/write-tests/)

----
url: https://docs.docker.com/guides/testcontainers-dotnet-getting-started/run-tests/
----

# Run tests and next steps

***

Table of contents

***

## [Run the tests](#run-the-tests)

Run the tests:

```console
$ dotnet test
```

You can see in the output that Testcontainers pulls the Postgres Docker image from Docker Hub (if not already available locally), starts the container, and runs the test.

Writing an integration test using Testcontainers works like writing a unit test that you can run from your IDE. Your teammates can clone the project and run tests without installing Postgres on their machines.

## [Summary](#summary)

The Testcontainers for .NET library helps you write integration tests using the same type of database (Postgres) that you use in production, instead of mocks. Because you aren't using mocks and instead talk to real services, you're free to refactor code and still verify that the application works as expected.

In addition to Postgres, Testcontainers provides dedicated [modules](https://www.nuget.org/profiles/Testcontainers) for many SQL databases, NoSQL databases, messaging queues, and more.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Testing an ASP.NET Core web app](https://testcontainers.com/guides/testing-an-aspnet-core-web-app/)

----
url: https://docs.docker.com/reference/cli/sbx/kit/
----

# sbx kit

| Description | Manage kit artifacts |
| ----------- | -------------------- |
| Usage       | `sbx kit COMMAND`    |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Manage kit artifacts.

Kits are declarative YAML artifacts that extend sandbox agents with additional credentials, network policies, environment variables, startup commands, and files.

## [Commands](#commands)

| Command                                                                       | Description                                           |
| ----------------------------------------------------------------------------- | ----------------------------------------------------- |
| [`sbx kit add`](https://docs.docker.com/reference/cli/sbx/kit/add/)           | experimental Add a kit to a running sandbox           |
| [`sbx kit inspect`](https://docs.docker.com/reference/cli/sbx/kit/inspect/)   | experimental Display details about a kit artifact     |
| [`sbx kit pack`](https://docs.docker.com/reference/cli/sbx/kit/pack/)         | experimental Package a directory as a kit artifact    |
| [`sbx kit pull`](https://docs.docker.com/reference/cli/sbx/kit/pull/)         | experimental Pull a kit artifact from an OCI registry |
| [`sbx kit push`](https://docs.docker.com/reference/cli/sbx/kit/push/)         | experimental Push a kit artifact to an OCI registry   |
| [`sbx kit validate`](https://docs.docker.com/reference/cli/sbx/kit/validate/) | experimental Validate a kit artifact                  |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/get-started/workshop/07_multi_container/
----

# Multi container apps

***

Table of contents

***

Up to this point, you've been working with single container apps. But, now you will add MySQL to the application stack. The following question often arises - "Where will MySQL run? Install it in the same container or run it separately?" In general, each container should do one thing and do it well. The following are a few reasons to run the container separately:

* There's a good chance you'd have to scale APIs and front-ends differently than databases.
* Separate containers let you version and update versions in isolation.
* While you may use a container for the database locally, you may want to use a managed service for the database in production. You don't want to ship your database engine with your app then.
* Running multiple processes will require a process manager (the container only starts one process), which adds complexity to container startup/shutdown.

And there are more reasons. So, like the following diagram, it's best to run your app in multiple containers.

## [Container networking](#container-networking)

Remember that containers, by default, run in isolation and don't know anything about other processes or containers on the same machine. So, how do you allow one container to talk to another? The answer is networking. If you place the two containers on the same network, they can talk to each other.

## [Start MySQL](#start-mysql)

There are two ways to put a container on a network:

* Assign the network when starting the container.
* Connect an already running container to a network.

In the following steps, you'll create the network first and then attach the MySQL container at startup.

1. Create the network.

   ```console
   $ docker network create todo-app
   ```

2. Start a MySQL container and attach it to the network. You're also going to define a few environment variables that the database will use to initialize the database. To learn more about the MySQL environment variables, see the "Environment Variables" section in the [MySQL Docker Hub listing](https://hub.docker.com/_/mysql/).

   ```console
   $ docker run -d \
       --network todo-app --network-alias mysql \
       -v todo-mysql-data:/var/lib/mysql \
       -e MYSQL_ROOT_PASSWORD=secret \
       -e MYSQL_DATABASE=todos \
       mysql:8.0
   ```

   ```powershell
   $ docker run -d `
       --network todo-app --network-alias mysql `
       -v todo-mysql-data:/var/lib/mysql `
       -e MYSQL_ROOT_PASSWORD=secret `
       -e MYSQL_DATABASE=todos `
       mysql:8.0
   ```

   ```console
   $ docker run -d ^
       --network todo-app --network-alias mysql ^
       -v todo-mysql-data:/var/lib/mysql ^
       -e MYSQL_ROOT_PASSWORD=secret ^
       -e MYSQL_DATABASE=todos ^
       mysql:8.0
   ```

   In the previous command, you can see the `--network-alias` flag. In a later section, you'll learn more about this flag.

   > Tip
   >
   > You'll notice a volume named `todo-mysql-data` in the above command that is mounted at `/var/lib/mysql`, which is where MySQL stores its data. However, you never ran a `docker volume create` command. Docker recognizes you want to use a named volume and creates one automatically for you.

3. To confirm you have the database up and running, connect to the database and verify that it connects.

   ```console
   $ docker exec -it <mysql-container-id> mysql -u root -p
   ```

   When the password prompt comes up, type in `secret`. In the MySQL shell, list the databases and verify you see the `todos` database.

   ```console
   mysql> SHOW DATABASES;
   ```

   You should see output that looks like this:

   ```plaintext
   +--------------------+
   | Database           |
   +--------------------+
   | information_schema |
   | mysql              |
   | performance_schema |
   | sys                |
   | todos              |
   +--------------------+
   5 rows in set (0.00 sec)
   ```

4. Exit the MySQL shell to return to the shell on your machine.

   ```console
   mysql> exit
   ```

   You now have a `todos` database and it's ready for you to use.

## [Connect to MySQL](#connect-to-mysql)

Now that you know MySQL is up and running, you can use it. But, how do you use it? If you run another container on the same network, how do you find the container? Remember that each container has its own IP address.

To answer the questions above and better understand container networking, you're going to make use of the [nicolaka/netshoot](https://github.com/nicolaka/netshoot) container, which ships with a lot of tools that are useful for troubleshooting or debugging networking issues.

1. Start a new container using the nicolaka/netshoot image. Make sure to connect it to the same network.

   ```console
   $ docker run -it --network todo-app nicolaka/netshoot
   ```

2. Inside the container, you're going to use the `dig` command, which is a useful DNS tool. You're going to look up the IP address for the hostname `mysql`.

   ```console
   $ dig mysql
   ```

   You should get output like the following.

   ```text
   ; <<>> DiG 9.18.8 <<>> mysql
   ;; global options: +cmd
   ;; Got answer:
   ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 32162
   ;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 0

   ;; QUESTION SECTION:
   ;mysql.				IN	A

   ;; ANSWER SECTION:
   mysql.			600	IN	A	172.23.0.2

   ;; Query time: 0 msec
   ;; SERVER: 127.0.0.11#53(127.0.0.11)
   ;; WHEN: Tue Oct 01 23:47:24 UTC 2019
   ;; MSG SIZE  rcvd: 44
   ```

   In the "ANSWER SECTION", you will see an `A` record for `mysql` that resolves to `172.23.0.2` (your IP address will most likely have a different value). While `mysql` isn't normally a valid hostname, Docker was able to resolve it to the IP address of the container that had that network alias. Remember, you used the `--network-alias` earlier.

   What this means is that your app only simply needs to connect to a host named `mysql` and it'll talk to the database.

## [Run your app with MySQL](#run-your-app-with-mysql)

The todo app supports the setting of a few environment variables to specify MySQL connection settings. They are:

* `MYSQL_HOST` - the hostname for the running MySQL server
* `MYSQL_USER` - the username to use for the connection
* `MYSQL_PASSWORD` - the password to use for the connection
* `MYSQL_DB` - the database to use once connected

> Note
>
> While using env vars to set connection settings is generally accepted for development, it's highly discouraged when running applications in production. Diogo Monica, a former lead of security at Docker, [wrote a fantastic blog post](https://blog.diogomonica.com/2017/03/27/why-you-shouldnt-use-env-variables-for-secret-data/) explaining why.
>
> A more secure mechanism is to use the secret support provided by your container orchestration framework. In most cases, these secrets are mounted as files in the running container. You'll see many apps (including the MySQL image and the todo app) also support env vars with a `_FILE` suffix to point to a file containing the variable.
>
> As an example, setting the `MYSQL_PASSWORD_FILE` var will cause the app to use the contents of the referenced file as the connection password. Docker doesn't do anything to support these env vars. Your app will need to know to look for the variable and get the file contents.

You can now start your dev-ready container.

1. Specify each of the previous environment variables, as well as connect the container to your app network. Make sure that you are in the `getting-started-app` directory when you run this command.

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
     -w /app -v ".:/app" \
     --network todo-app \
     -e MYSQL_HOST=mysql \
     -e MYSQL_USER=root \
     -e MYSQL_PASSWORD=secret \
     -e MYSQL_DB=todos \
     node:24-alpine \
     sh -c "npm install && npm run dev"
   ```

   In Windows, run this command in PowerShell.

   ```powershell
   $ docker run -dp 127.0.0.1:3000:3000 `
     -w /app -v ".:/app" `
     --network todo-app `
     -e MYSQL_HOST=mysql `
     -e MYSQL_USER=root `
     -e MYSQL_PASSWORD=secret `
     -e MYSQL_DB=todos `
     node:24-alpine `
     sh -c "npm install && npm run dev"
   ```

   In Windows, run this command in Command Prompt.

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 ^
     -w /app -v "%cd%:/app" ^
     --network todo-app ^
     -e MYSQL_HOST=mysql ^
     -e MYSQL_USER=root ^
     -e MYSQL_PASSWORD=secret ^
     -e MYSQL_DB=todos ^
     node:24-alpine ^
     sh -c "npm install && npm run dev"
   ```

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 \
     -w //app -v "/.:/app" \
     --network todo-app \
     -e MYSQL_HOST=mysql \
     -e MYSQL_USER=root \
     -e MYSQL_PASSWORD=secret \
     -e MYSQL_DB=todos \
     node:24-alpine \
     sh -c "npm install && npm run dev"
   ```

2. If you look at the logs for the container (`docker logs -f <container-id>`), you should see a message similar to the following, which indicates it's using the mysql database.

   ```console
   [nodemon] 3.1.11
   [nodemon] to restart at any time, enter `rs`
   [nodemon] watching path(s): *.*
   [nodemon] watching extensions: js,mjs,cjs,json
   [nodemon] starting `node src/index.js`
   Waiting for mysql:3306.
   Connected!
   Connected to mysql db at host mysql
   Listening on port 3000
   ```

3. Open the app in your browser and add a few items to your todo list.

4. Connect to the mysql database and prove that the items are being written to the database. Remember, the password is `secret`.

   ```console
   $ docker exec -it <mysql-container-id> mysql -p todos
   ```

   And in the mysql shell, run the following:

   ```console
   mysql> select * from todo_items;
   +--------------------------------------+--------------------+-----------+
   | id                                   | name               | completed |
   +--------------------------------------+--------------------+-----------+
   | c906ff08-60e6-44e6-8f49-ed56a0853e85 | Do amazing things! |         0 |
   | 2912a79e-8486-4bc3-a4c5-460793a575ab | Be awesome!        |         0 |
   +--------------------------------------+--------------------+-----------+
   ```

   Your table will look different because it has your items. But, you should see them stored there.

## [Summary](#summary)

At this point, you have an application that now stores its data in an external database running in a separate container. You learned a little bit about container networking and service discovery using DNS.

Related information:

* [docker CLI reference](/reference/cli/docker/)
* [Networking overview](https://docs.docker.com/engine/network/)

## [Next steps](#next-steps)

There's a good chance you are starting to feel a little overwhelmed with everything you need to do to start up this application. You have to create a network, start containers, specify all of the environment variables, expose ports, and more. That's a lot to remember and it's certainly making things harder to pass along to someone else.

In the next section, you'll learn about Docker Compose. With Docker Compose, you can share your application stacks in a much easier way and let others spin them up with a single, simple command.

[Use Docker Compose](https://docs.docker.com/get-started/workshop/08_using_compose/)

----
url: https://docs.docker.com/engine/security/rootless/uid-gid-mapping/
----

# UID/GID mapping

***

***

Rootless mode and [`userns-remap` mode](https://docs.docker.com/engine/security/userns-remap/) map container UIDs and GIDs to the host differently.

* In `userns-remap` mode, container UID `0` is mapped to the first subordinate UID listed in `/etc/subuid` for the remap user, and container UID `n` is mapped to `subuid + n`.
* In rootless mode, container UID `0` is mapped to the host UID of the user running rootless Docker (the result of `id -u`); container UID `n` (for `n >= 1`) is mapped to `subuid + (n - 1)`.

GIDs follow the same rules using `/etc/subgid`.

This difference matters when setting file permissions on bind-mounted directories: in rootless mode, files owned by your host user appear as owned by `root` inside the container.

----
url: https://docs.docker.com/billing/cycle/
----

# Change your billing cycle

***

Table of contents

***

You can choose between a monthly or annual billing cycle when purchasing a subscription. If you have a monthly billing cycle, you can choose to switch to an annual billing cycle.

If you're on a monthly plan, you can switch to a yearly plan at any time. However, switching from a yearly to a monthly cycle isn't supported.

When you change your billing cycle:

* Your next billing date reflects the new cycle. To find your next billing date, see [View renewal date](https://docs.docker.com/billing/history/#view-renewal-date).
* Your subscription's start date resets. For example, if the monthly subscription started on March 1 and ended on April 1, switching the billing duration on March 15, 2024, resets the new start date to March 15, 2024, with an end date of March 15, 2025.
* Any unused portion of your monthly subscription is prorated and applied as credit toward an annual subscription. For example, if your monthly cost is $10 and you're used value is $5, when you switch to an annual cycle ($100), the final charge is $95 ($100-$5).

## [Change personal account to an annual cycle](#change-personal-account-to-an-annual-cycle)

Pay by invoice is not available for subscription upgrades or changes.

To change your billing cycle:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Billing**.
3. On the plans and usage page, select **Switch to annual billing**.
4. Verify your billing information.
5. Select **Continue to payment**.
6. Verify payment information and select **Upgrade subscription**. If you choose to pay using a US bank account, you must verify the account. For more information, see [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).

The billing plans and usage page will now reflect your new annual plan details.

## [Change organization to an annual cycle](#change-organization-to-an-annual-cycle)

You must be an organization owner to make changes to the payment information.

Pay by invoice is not available for subscription upgrades or changes.

Follow these steps to switch from a monthly to annual billing cycle for your organization's Docker subscription:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Billing**.
3. On the plans and usage page, select **Switch to annual billing**.
4. Verify your billing information.
5. Select **Continue to payment**.
6. Verify payment information and select **Upgrade subscription**. If you choose to pay using a US bank account, you must verify the account. For more information, see [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).

----
url: https://docs.docker.com/engine/release-notes/26.1/
----

# Docker Engine 26.1 release notes

***

Table of contents

***

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 26.1.

For more information about:

* Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
* Changes to the Engine API, see [Engine API version history](/reference/api/engine/version-history/).

## [26.1.4](#2614)

*2024-06-05*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.1.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.4)
* [moby/moby, 26.1.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.4)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.4/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.4/docs/api/version-history.md).

### [Security](#security)

This release updates the Go runtime to 1.21.11 which contains security fixes for:

* [CVE-2024-24789](https://github.com/golang/go/issues/66869)
* [CVE-2024-24790](https://github.com/golang/go/issues/67680)
* A symlink time of check to time of use race condition during directory removal reported by [Addison Crump](https://github.com/addisoncrump).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements)

* Fixed an issue where promoting a node immediately after another node was demoted could cause the promotion to fail. [moby/moby#47870](https://github.com/moby/moby/pull/47870)
* Prevent the daemon log from being spammed with `superfluous response.WriteHeader call ...` messages. [moby/moby#47843](https://github.com/moby/moby/pull/47843)
* Don't show empty hints when plugins return an empty hook message. [docker/cli#5083](https://github.com/docker/cli/pull/5083)
* Fix a compatibility issue with Visual Studio Container Tools. [docker/cli#5095](https://github.com/docker/cli/pull/5095)

### [Packaging updates](#packaging-updates)

* Update containerd (static binaries only) to [v1.7.17](https://github.com/containerd/containerd/releases/tag/v1.7.17). [moby/moby#47841](https://github.com/moby/moby/pull/47841)
* [CVE-2024-24789](https://github.com/golang/go/issues/66869), [CVE-2024-24790](https://github.com/golang/go/issues/67680): Update Go runtime to 1.21.11. [moby/moby#47904](https://github.com/moby/moby/pull/47904)
* Update Compose to [v2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1). [docker/docker-ce-packages#1022](https://github.com/docker/docker-ce-packaging/pull/1022)
* Update Buildx to [v0.14.1](https://github.com/docker/buildx/releases/tag/v0.14.1). [docker/docker-ce-packages#1021](https://github.com/docker/docker-ce-packaging/pull/1021)

## [26.1.3](#2613)

*2024-05-16*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.1.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.3)
* [moby/moby, 26.1.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.3)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.3/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.3/docs/api/version-history.md).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-1)

* Fix a regression that prevented the use of DNS servers within a `--internal` network. [moby/moby#47832](https://github.com/moby/moby/pull/47832)
* When the internal DNS server's own address is supplied as an external server address, ignore it to avoid unproductive recursion. [moby/moby#47833](https://github.com/moby/moby/pull/47833)

### [Packaging updates](#packaging-updates-1)

* Allow runc to kill containers when confined to the runc profile in AppArmor version 4.0.0 and later. [moby/moby#47829](https://github.com/moby/moby/pull/47829)

## [26.1.2](#2612)

*2024-05-08*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.1.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.2)
* [moby/moby, 26.1.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.2)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.2/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.2/docs/api/version-history.md).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-2)

* Fix an issue where the CLI process would sometimes hang when a container failed to start. [docker/cli#5062](https://github.com/docker/cli/pull/5062)

### [Packaging updates](#packaging-updates-2)

* Update Go runtime to 1.21.10. [moby/moby#47806](https://github.com/moby/moby/pull/47806)

## [26.1.1](#2611)

*2024-04-30*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.1.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.1)
* [moby/moby, 26.1.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.1)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.1/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.1/docs/api/version-history.md).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-3)

* Fix `docker run -d` printing an `context canceled` spurious error when OpenTelemetry is configured. [docker/cli#5044](https://github.com/docker/cli/pull/5044)
* Experimental environment variable `DOCKER_BRIDGE_PRESERVE_KERNEL_LL=1` will prevent the daemon from removing the kernel-assigned link local address on a Linux bridge. [moby/moby#47775](https://github.com/moby/moby/pull/47775)
* Resolve an issue preventing container creation on hosts with a read-only `/proc/sys/net` filesystem. If IPv6 cannot be disabled on an interface due to this, either disable IPv6 by default on the host or ensure `/proc/sys/net` is read-write. To bypass the error, set the environment variable `DOCKER_ALLOW_IPV6_ON_IPV4_INTERFACE=1` before starting the Docker daemon. [moby/moby#47769](https://github.com/moby/moby/pull/47769)

> Note
>
> The `DOCKER_ALLOW_IPV6_ON_IPV4_INTERFACE` is added as a temporary fix and will be phased out in a future major release, when the IPv6 enablement process has been improved.

### [Packaging updates](#packaging-updates-3)

* Update BuildKit to [v0.13.2](https://github.com/moby/buildkit/releases/tag/v0.13.2). [moby/moby#47762](https://github.com/moby/moby/pull/47762)
* Update Compose to [v2.27.0](https://github.com/docker/compose/releases/tag/v2.27.0). [docker/docker-ce-packages#1017](https://github.com/docker/docker-ce-packaging/pull/1017)

## [26.1.0](#2610)

*2024-04-22*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.1.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.1.0)
* [moby/moby, 26.1.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.1.0)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.1.0/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.1.0/docs/api/version-history.md).

### [New](#new)

* Added configurable OpenTelemetry utilities and basic instrumentation to commands. For more information, see [OpenTelemetry for the Docker CLI](https://docs.docker.com/config/otel). [docker/cli#4889](https://github.com/docker/cli/pull/4889)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-4)

* Native Windows containers are configured with an internal DNS server for container name resolution, and external DNS servers for other lookups. Not all resolvers, including `nslookup`, fall back to the external resolvers when they get a `SERVFAIL` answer from the internal server. So, the internal DNS server can now be configured to forward requests to the external resolvers, by setting a `feature` option in the `daemon.json` file:

  ```json
  {
    "features": {
      "windows-dns-proxy": true
    }
  }
  ```

  [moby/moby#47584](https://github.com/moby/moby/pull/47584)

  > Note
  >
  > * This will be the new default behavior in Docker Engine 27.0.
  > * The `windows-dns-proxy` feature flag will be removed in a future release.

* Swarm: Fix `Subpath` not being passed to the container config. [moby/moby#47711](https://github.com/moby/moby/pull/47711)

* Classic builder: Fix cache miss on `WORKDIR <directory>/` build step (directory with a trailing slash). [moby/moby#47723](https://github.com/moby/moby/pull/47723)

* containerd image store: Fix `docker images` failing when any image in the store has unexpected target. [moby/moby#47738](https://github.com/moby/moby/pull/47738)

----
url: https://docs.docker.com/guides/testcontainers-java-lifecycle/create-project/
----

# Create the project and business logic

***

Table of contents

***

## [Set up the project](#set-up-the-project)

Create a Java project with Maven and add the required dependencies:

```xml
<dependencies>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <version>42.7.3</version>
    </dependency>
    <dependency>
        <groupId>ch.qos.logback</groupId>
        <artifactId>logback-classic</artifactId>
        <version>1.5.6</version>
    </dependency>
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.2</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <version>2.0.4</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-postgresql</artifactId>
        <version>2.0.4</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## [Create the business logic](#create-the-business-logic)

Create a `Customer` record:

```java
package com.testcontainers.demo;

public record Customer(Long id, String name) {}
```

Create a `CustomerService` class with methods to create, retrieve, and delete customers:

```java
package com.testcontainers.demo;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public class CustomerService {

  private final String url;
  private final String username;
  private final String password;

  public CustomerService(String url, String username, String password) {
    this.url = url;
    this.username = username;
    this.password = password;
    createCustomersTableIfNotExists();
  }

  public void createCustomer(Customer customer) {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        "insert into customers(id,name) values(?,?)"
      );
      pstmt.setLong(1, customer.id());
      pstmt.setString(2, customer.name());
      pstmt.execute();
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  public List<Customer> getAllCustomers() {
    List<Customer> customers = new ArrayList<>();
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        "select id,name from customers"
      );
      ResultSet rs = pstmt.executeQuery();
      while (rs.next()) {
        long id = rs.getLong("id");
        String name = rs.getString("name");
        customers.add(new Customer(id, name));
      }
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
    return customers;
  }

  public Optional<Customer> getCustomer(Long customerId) {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        "select id,name from customers where id = ?"
      );
      pstmt.setLong(1, customerId);
      ResultSet rs = pstmt.executeQuery();
      if (rs.next()) {
        long id = rs.getLong("id");
        String name = rs.getString("name");
        return Optional.of(new Customer(id, name));
      }
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
    return Optional.empty();
  }

  public void deleteAllCustomers() {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement("delete from customers");
      pstmt.execute();
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  private void createCustomersTableIfNotExists() {
    try (Connection conn = this.getConnection()) {
      PreparedStatement pstmt = conn.prepareStatement(
        """
        create table if not exists customers (
            id bigint not null,
            name varchar not null,
            primary key (id)
        )
        """
      );
      pstmt.execute();
    } catch (SQLException e) {
      throw new RuntimeException(e);
    }
  }

  private Connection getConnection() {
    try {
      return DriverManager.getConnection(url, username, password);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
```

[JUnit 5 lifecycle callbacks »](https://docs.docker.com/guides/testcontainers-java-lifecycle/lifecycle-callbacks/)

----
url: https://docs.docker.com/engine/network/port-publishing/
----

# Port publishing and mapping

***

Table of contents

***

By default, for both IPv4 and IPv6, the Docker daemon blocks access to ports that have not been published. Published container ports are mapped to host IP addresses. To do this, it uses firewall rules to perform Network Address Translation (NAT), Port Address Translation (PAT), and masquerading.

For example, `docker run -p 8080:80 [...]` creates a mapping between port 8080 on any address on the Docker host, and the container's port 80. Outgoing connections from the container will masquerade, using the Docker host's IP address.

## [Publishing ports](#publishing-ports)

When you create or run a container using `docker create` or `docker run`, all ports of containers on bridge networks are accessible from the Docker host and other containers connected to the same network. Ports are not accessible from outside the host or, with the default configuration, from containers in other networks.

Use the `--publish` or `-p` flag to make a port available outside the host, and to containers in other bridge networks.

This creates a firewall rule in the host, mapping a container port to a port on the Docker host to the outside world. Here are some examples:

| Flag value                      | Description                                                                                                                                             |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80`                    | Map port `8080` on the Docker host to TCP port `80` in the container.                                                                                   |
| `-p 192.168.1.100:8080:80`      | Map port `8080` on the Docker host IP `192.168.1.100` to TCP port `80` in the container.                                                                |
| `-p 8080:80/udp`                | Map port `8080` on the Docker host to UDP port `80` in the container.                                                                                   |
| `-p 8080:80/tcp -p 8080:80/udp` | Map TCP port `8080` on the Docker host to TCP port `80` in the container, and map UDP port `8080` on the Docker host to UDP port `80` in the container. |

> Important
>
> Publishing container ports is insecure by default. Meaning, when you publish a container's ports it becomes available not only to the Docker host, but to the outside world as well.
>
> If you include the localhost IP address (`127.0.0.1`, or `::1`) with the publish flag, only the Docker host can access the published container port.
>
> ```console
> $ docker run -p 127.0.0.1:8080:80 -p '[::1]:8080:80' nginx
> ```
>
> > Warning
> >
> > In releases older than 28.0.0, hosts within the same L2 segment (for example, hosts connected to the same network switch) can reach ports published to localhost. For more information, see [moby/moby#45610](https://github.com/moby/moby/issues/45610)

Ports on the host's IPv6 addresses will map to the container's IPv4 address if no host IP is given in a port mapping, the bridge network is IPv4-only, and `--userland-proxy=true` (default).

## [Direct routing](#direct-routing)

Port mapping ensures that published ports are accessible on the host's network addresses, which are likely to be routable for any external clients. No routes are normally set up in the host's network for container addresses that exist within a host.

But, particularly with IPv6 you may prefer to avoid using NAT and instead arrange for external routing to container addresses ("direct routing").

To access containers on a bridge network from outside the Docker host, you must first set up routing to the bridge network via an address on the Docker host. This can be achieved using static routes, Border Gateway Protocol (BGP), or any other means appropriate for your network. For example, within a local layer 2 network, remote hosts can set up static routes to a container network via the Docker daemon host's address on the local network.

### [Direct routing to containers in bridge networks](#direct-routing-to-containers-in-bridge-networks)

By default, remote hosts are not allowed direct access to container IP addresses in Docker's Linux bridge networks. They can only access ports published to host IP addresses.

To allow direct access to any published port, on any container, in any Linux bridge network, use daemon option `"allow-direct-routing": true` in `/etc/docker/daemon.json` or the equivalent `--allow-direct-routing`.

To allow direct routing from anywhere to containers in a specific bridge network, see [Gateway modes](#gateway-modes).

Or, to allow direct routing via specific host interfaces, to a specific bridge network, use the following option when creating the network:

* `com.docker.network.bridge.trusted_host_interfaces`

#### [Example](#example)

Create a network where published ports on container IP addresses can be accessed directly from interfaces `vxlan.1` and `eth3`:

```console
$ docker network create --subnet 192.0.2.0/24 --ip-range 192.0.2.0/29 -o com.docker.network.bridge.trusted_host_interfaces="vxlan.1:eth3" mynet
```

Run a container in that network, publishing its port 80 to port 8080 on the host's loopback interface:

```console
$ docker run -d --ip 192.0.2.100 -p 127.0.0.1:8080:80 nginx
```

The web server running on the container's port 80 can now be accessed from the Docker host at `http://127.0.0.1:8080`, or directly at `http://192.0.2.100:80`. If remote hosts on networks connected to interfaces `vxlan.1` and `eth3` have a route to the `192.0.2.0/24` network inside the Docker host, they can also access the web server via `http://192.0.2.100:80`.

## [Gateway modes](#gateway-modes)

The bridge network driver has the following options:

* `com.docker.network.bridge.gateway_mode_ipv6`
* `com.docker.network.bridge.gateway_mode_ipv4`

Each of these can be set to one of the gateway modes:

* `nat`
* `nat-unprotected`
* `routed`
* `isolated`

The default is `nat`, NAT and masquerading rules are set up for each published container port. Packets leaving the host will use a host address.

With mode `routed`, no NAT or masquerading rules are set up, but firewall rules are still set up so that only published container ports are accessible. Outgoing packets from the container will use the container's address, not a host address.

To access a published port in a `routed` network, remote hosts must have a route to the container network via an external address on the Docker host ("direct routing"). Hosts on the local layer-2 network can set up direct routing without needing any additional network configuration. Hosts outside the local network can only use direct routing to the container if the network's routers are configured to enable it.

In a `nat` mode network, publishing a port to an address on the loopback interface means remote hosts cannot access it. Other published container ports in `routed` and `nat` networks are always accessible from remote hosts using direct routing, unless the Docker host's firewall has additional restrictions.

> Note
>
> When a port is published to a specific host address in `nat` mode, if IP forwarding is enabled on the Docker host, the published port can be accessed via other host interfaces using direct routing to the host address.
>
> For example, a Docker host with IP forwarding enabled has two NICs with addresses `192.168.100.10/24` and `10.0.0.10/24`. When a port is published to `192.168.100.10`, a host in the `10.0.0.0/24` subnet can access that port by routing to `192.168.100.10` via `10.0.0.10`.

In `nat-unprotected` mode, unpublished container ports are also accessible using direct routing, no port filtering rules are set up. This mode is included for compatibility with legacy default behaviour.

The gateway mode also affects communication between containers that are connected to different Docker networks on the same host.

* In `nat` and `nat-unprotected` modes, containers in other bridge networks can only access published ports via the host addresses they are published to. Direct routing from other networks is not allowed.
* In `routed` mode containers in other networks can use direct routing to access ports, without going via a host address.

In `routed` mode, a host port in a `-p` or `--publish` port mapping is not used, and the host address is only used to decide whether to apply the mapping to IPv4 or IPv6. So, when a mapping only applies to `routed` mode, only addresses `0.0.0.0` or `::` should be used, and a host port should not be given. If a specific address or port is given, it will have no effect on the published port and a warning message will be logged.

Mode `isolated` can only be used when the network is also created with CLI flag `--internal`, or equivalent. An address is normally assigned to the bridge device in an `internal` network. So, processes on the Docker host can access the network, and containers in the network can access host services listening on that bridge address (including services listening on "any" host address, `0.0.0.0` or `::`). No address is assigned to the bridge when the network is created with gateway mode `isolated`.

### [Example](#example-1)

Create a network suitable for direct routing for IPv6, with NAT enabled for IPv4:

```console
$ docker network create --ipv6 --subnet 2001:db8::/64 -o com.docker.network.bridge.gateway_mode_ipv6=routed mynet
```

Create a container with a published port:

```console
$ docker run --network=mynet -p 8080:80 myimage
```

Then:

* Only container port 80 will be open, for IPv4 and IPv6.
* For IPv6, using `routed` mode, port 80 will be open on the container's IP address. Port 8080 will not be opened on the host's IP addresses, and outgoing packets will use the container's IP address.
* For IPv4, using the default `nat` mode, the container's port 80 will be accessible via port 8080 on the host's IP addresses, as well as directly from within the Docker host. But, container port 80 cannot be accessed directly from outside the host. Connections originating from the container will masquerade, using the host's IP address.

In `docker inspect`, this port mapping will be shown as follows. Note that there is no `HostPort` for IPv6, because it is using `routed` mode:

```console
$ docker container inspect <id> --format "{{json .NetworkSettings.Ports}}"
{"80/tcp":[{"HostIp":"0.0.0.0","HostPort":"8080"},{"HostIp":"::","HostPort":""}]}
```

Alternatively, to make the mapping IPv6-only, disabling IPv4 access to the container's port 80, use the unspecified IPv6 address `[::]` and do not include a host port number:

```console
$ docker run --network mynet -p '[::]::80'
```

## [Setting the default bind address for containers](#setting-the-default-bind-address-for-containers)

By default, when a container's ports are mapped without any specific host address, the Docker daemon publishes ports to all host addresses (`0.0.0.0` and `[::]`).

For example, the following command publishes port 8080 to all network interfaces on the host, on both IPv4 and IPv6 addresses, potentially making them available to the outside world.

```console
docker run -p 8080:80 nginx
```

You can change the default binding address for published container ports so that they're only accessible to the Docker host by default. To do that, you can configure the daemon to use the loopback address (`127.0.0.1`) instead.

> Warning
>
> In releases older than 28.0.0, hosts within the same L2 segment (for example, hosts connected to the same network switch) can reach ports published to localhost. For more information, see [moby/moby#45610](https://github.com/moby/moby/issues/45610)

To configure this setting for user-defined bridge networks, use the `com.docker.network.bridge.host_binding_ipv4` [driver option](https://docs.docker.com/engine/network/drivers/bridge/#default-host-binding-address) when you create the network. Despite the option name, it is possible to specify an IPv6 address.

```console
$ docker network create mybridge \
  -o "com.docker.network.bridge.host_binding_ipv4=127.0.0.1"
```

Or, to set the default binding address for containers in all user-defined bridge networks, use daemon configuration option `default-network-opts`. For example:

```json
{
  "default-network-opts": {
    "bridge": {
      "com.docker.network.bridge.host_binding_ipv4": "127.0.0.1"
    }
  }
}
```

> Note
>
> Setting the default binding address to `::` means port bindings with no host address specified will work for any IPv6 address on the host. But, `0.0.0.0` means any IPv4 or IPv6 address.
>
> Changing the default bind address doesn't have any effect on Swarm services. Swarm services are always exposed on the `0.0.0.0` network interface.

### [Masquerade or SNAT for outgoing packets](#masquerade-or-snat-for-outgoing-packets)

NAT is enabled by default for bridge networks, meaning outgoing packets from containers are masqueraded. The source address of packets leaving the Docker host is changed to an address on the host interface the packet is sent on.

Masquerading can be disabled for a user-defined bridge network by using the `com.docker.network.bridge.enable_ip_masquerade` driver option when creating the network. For example:

```console
$ docker network create mybridge \
  -o com.docker.network.bridge.enable_ip_masquerade=false ...
```

To use a specific source address for outgoing packets for a user-defined network, instead of letting masquerading select an address, use options `com.docker.network.host_ipv4` and `com.docker.network.host_ipv6` to specify the Source NAT (SNAT) address to use. The `com.docker.network.bridge.enable_ip_masquerade` option must be `true`, the default, for these options to have any effect.

### [Default bridge](#default-bridge)

To set the default binding for the default bridge network, configure the `"ip"` key in the `daemon.json` configuration file:

```json
{
  "ip": "127.0.0.1"
}
```

This changes the default binding address to `127.0.0.1` for published container ports on the default bridge network. Restart the daemon for this change to take effect. Alternatively, you can use the `dockerd --ip` flag when starting the daemon.

----
url: https://docs.docker.com/ai/sandboxes/faq/
----

# FAQ

***

Table of contents

***

## [Is Docker Sandboxes free? Can I use it commercially?](#is-docker-sandboxes-free-can-i-use-it-commercially)

Yes to both. The `sbx` CLI is free to use, including for commercial and professional work, with no per-seat fee. Install it, sign in with a free Docker account, and run sandboxes at no cost.

The only paid component is organization governance: centrally managed network and filesystem policies, [sign-in enforcement](https://docs.docker.com/ai/sandboxes/governance/sign-in-enforcement/), and [audit logs](https://docs.docker.com/ai/sandboxes/governance/audit/). These [organization governance features](https://docs.docker.com/ai/sandboxes/governance/) require a separate paid subscription — [contact Docker Sales](https://www.docker.com/products/ai-governance/#contact-sales) to get started. Everything else, including running agents in isolated sandboxes, is free.

## [Why do I need to sign in?](#why-do-i-need-to-sign-in)

Docker Sandboxes is built around the idea that you and your agents are a team. Signing in gives each sandbox a verified identity, which lets Docker:

* **Tie sandboxes to a real person.** Governance matters when agents can build containers, install packages, and push code. Your Docker identity is the anchor.
* **Enable team features.** Team-scale features like [organization governance](https://docs.docker.com/ai/sandboxes/governance/org/), shared environments, and audit logs need a concept of "who," and adding that later would be worse for everyone.
* **Authenticate against Docker infrastructure.** Sandboxes pull images, run daemons, and talk to Docker services. A Docker account authenticates those requests.

Your Docker account email is only used for authentication, not marketing.

## [Can I enforce sandbox policies across my organization?](#can-i-enforce-sandbox-policies-across-my-organization)

Yes. Admins can centrally manage network and filesystem policies from the Docker Admin Console. Rules defined there apply to every sandbox in the organization. When organization governance is active, it replaces local rules set with `sbx policy` — local rules are no longer evaluated.

See [Organization governance](https://docs.docker.com/ai/sandboxes/governance/org/). This feature requires a separate paid subscription — [contact Docker Sales](https://www.docker.com/products/ai-governance/#contact-sales) to get started.

## [Does the CLI collect telemetry?](#does-the-cli-collect-telemetry)

The `sbx` CLI collects basic usage data about CLI invocations:

* Which command you ran
* Whether it succeeded or failed
* How long it took
* If you're signed in, your Docker username is included

Docker Sandboxes doesn't monitor sessions, read your prompts, or access your code. Your code stays in the sandbox and on your host.

To opt out of all analytics, set the `SBX_NO_TELEMETRY` environment variable:

```console
$ export SBX_NO_TELEMETRY=1
```

## [How do I set custom environment variables inside a sandbox?](#how-do-i-set-custom-environment-variables-inside-a-sandbox)

The [`sbx secret`](/reference/cli/sbx/secret/) command only supports a fixed set of [services](https://docs.docker.com/ai/sandboxes/security/credentials/#built-in-services) (Anthropic, OpenAI, GitHub, and others). If your agent needs an environment variable that isn't tied to a supported service, such as `BRAVE_API_KEY` or a custom internal token, write it to `/etc/sandbox-persistent.sh` inside the sandbox. This file is sourced on every shell login, so the variable persists across agent sessions for the sandbox's lifetime.

Use `sbx exec` to append the export:

```console
$ sbx exec -d <sandbox-name> bash -c "echo 'export BRAVE_API_KEY=your_key' >> /etc/sandbox-persistent.sh"
```

The `bash -c` wrapper is required so the `>>` redirect runs inside the sandbox instead of on your host.

> Note
>
> Unlike `sbx secret`, which injects credentials through a host-side proxy without exposing them to the agent, this approach stores the value inside the sandbox. The agent process can read it directly. Only use this for credentials where proxy-based injection isn't available.

Variables in `/etc/sandbox-persistent.sh` are sourced automatically when bash runs inside the sandbox, including interactive sessions and agents started with `sbx run`. If you run a command directly with `sbx exec <name> <command>`, the command runs without a shell, so the persistent environment file is not sourced. Wrap the command in `bash -c` to load the environment:

```console
$ sbx exec <sandbox-name> bash -c "your-command"
```

To verify the variable is set, open a shell in the sandbox:

```console
$ sbx exec -it <sandbox-name> bash
$ echo $BRAVE_API_KEY
```

## [Why do agents run without approval prompts?](#why-do-agents-run-without-approval-prompts)

The sandbox itself is the safety boundary. Because agents run inside an isolated microVM with [network policies](https://docs.docker.com/ai/sandboxes/governance/), [credential isolation](https://docs.docker.com/ai/sandboxes/security/credentials/), and no access to your host system outside the workspace, the usual reasons for approval prompts (preventing destructive commands, network access, file modifications) are handled by the sandbox isolation layers instead.

If you prefer to re-enable approval prompts, change the permission mode inside the session. Most agents let you switch permission modes after startup. In Claude Code, use the `/permissions` command to change the mode interactively.

To make approval prompts the default for every session, define a custom sandbox kit that overrides the agent's entrypoint to drop the permission-skipping flag. For example, a kit that launches Claude Code without `--dangerously-skip-permissions`:

claude-safe/spec.yaml

```yaml
schemaVersion: "1"
kind: sandbox
name: claude-safe
sandbox:
  image: "docker/sandbox-templates:claude-code-docker"
  entrypoint:
    run: [claude]
```

Run it with `sbx run claude-safe --kit ./claude-safe/`. See [Sandbox kits](https://docs.docker.com/ai/sandboxes/customize/kits/#sandbox-kits) for the full pattern.

## [How do I know if my agent is running in a sandbox?](#how-do-i-know-if-my-agent-is-running-in-a-sandbox)

Ask the agent. The agent can see whether or not it's running inside a sandbox. In Claude Code, use the `/btw` slash command to ask without interrupting an in-progress task:

```text
/btw are you running in a sandbox?
```

## [Why doesn't the sandbox use my user-level agent configuration?](#why-doesnt-the-sandbox-use-my-user-level-agent-configuration)

Sandboxes don't pick up user-level agent configuration from your host. This includes directories like `~/.claude` for Claude Code or `~/.codex` for Codex, where hooks, skills, and other settings are stored. Only project-level configuration in the working directory is available inside the sandbox.

To make configuration available in a sandbox, copy or move what you need into your project directory before starting a session:

```console
$ cp -r ~/.claude/skills .claude/skills
```

Don't use symlinks — a sandboxed agent can't follow symlinks to paths outside the sandbox.

Collocating skills and other agent configuration with the project itself is a good practice regardless of sandboxes. It's versioned alongside the code and evolves with the project as it changes.

## [Can I paste images into an agent?](#can-i-paste-images-into-an-agent)

Yes, but it's off by default. Text paste already works, because the terminal sends it directly. Pasting an image or screenshot with `Ctrl+V` is different: the agent reads it from your host clipboard, and the sandbox blocks that access unless you opt in.

Turn it on with a local setting:

```console
$ sbx settings set clipboard.imagePaste true
```

`Ctrl+V` then pastes host images into agents that read the clipboard, including Claude Code and Codex. The setting takes effect within a few seconds, even for running sandboxes.

This is opt-in because it relaxes the sandbox's isolation: when enabled, a process inside the sandbox can read your host clipboard through the host-side proxy. The exposure is narrow — reads happen only on a paste, return image data only (`image/png`), and clipboard content is never cached or logged — but it's still host data crossing into the sandbox, so it stays off until you turn it on.

To turn it back off:

```console
$ sbx settings set clipboard.imagePaste false
```

## [Can I use Docker Sandboxes on headless Linux?](#can-i-use-docker-sandboxes-on-headless-linux)

Yes. On Linux, `sbx` stores secrets in the Secret Service exposed by your desktop keyring, such as GNOME Keyring or KDE Wallet. Headless servers and some WSL setups have no running Secret Service, so `sbx` falls back to an encrypted file under `$XDG_CONFIG_HOME/com.docker.sandboxes`, which defaults to `~/.config/com.docker.sandboxes` when `$XDG_CONFIG_HOME` is unset. No setup is required. When you store a secret on such a host, `sbx` prints a notice:

```text
No keychain detected - this secret will be stored in an encrypted file on disk
```

The file is encrypted at rest and protected by `0700` directory permissions, the same posture as `~/.docker/config.json`. It's weaker than an OS keychain, which also mediates access per application.

To keep secrets in a keyring instead, run a Secret Service on the host before storing them: install `gnome-keyring` and start `dbus-run-session`, or run the keyring daemon under a login session that unlocks it. Once a working Secret Service is available, `sbx` stores new secrets in the keychain again. For where each platform keeps secrets, see [Where secrets are stored](https://docs.docker.com/ai/sandboxes/security/credentials/#where-secrets-are-stored).

----
url: https://docs.docker.com/reference/cli/docker/container/inspect/
----

# docker container inspect

***

| Description | Display detailed information on one or more containers        |
| ----------- | ------------------------------------------------------------- |
| Usage       | `docker container inspect [OPTIONS] CONTAINER [CONTAINER...]` |

## [Description](#description)

Display detailed information on one or more containers

## [Options](#options)

| Option         | Default | Description                                                                                                                                                                                                                             |
| -------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-f, --format` |         | Format output using a custom template: 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `-s, --size`   |         | Display total file sizes                                                                                                                                                                                                                |

----
url: https://docs.docker.com/reference/cli/docker/sandbox/reset/
----

# docker sandbox reset

***

| Description | Reset all VM sandboxes and clean up state |
| ----------- | ----------------------------------------- |
| Usage       | `docker sandbox reset [OPTIONS]`          |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Reset all VM sandboxes and permanently delete all VM data.

This command will:

* Stop all running VMs gracefully (30s timeout)
* Delete all VM state directories in \~/.docker/sandboxes/vm/
* Clear image cache in \~/.docker/sandboxes/image-cache/
* Clear all internal registries

The daemon will continue running with fresh state after reset.

⚠️ WARNING: This is a destructive operation that cannot be undone! All running agents will be forcefully terminated and their work will be lost. Cached image tars will be deleted and will need to be recreated on next use.

By default, you will be prompted to confirm (y/N). Use --force to skip the confirmation prompt.

## [Options](#options)

| Option                  | Default | Description              |
| ----------------------- | ------- | ------------------------ |
| [`-f, --force`](#force) |         | Skip confirmation prompt |

## [Examples](#examples)

### [Reset with confirmation prompt](#reset-with-confirmation-prompt)

```console
$ docker sandbox reset
⚠️  WARNING: This will permanently delete all VM data and stop all running agents!
Are you sure you want to continue? (y/N): y
All VMs reset successfully
```

### [Force reset without confirmation (-f, --force)](#force)

Skip the confirmation prompt:

```console
$ docker sandbox reset --force
All VMs reset successfully
```

> Caution
>
> This is a destructive operation that cannot be undone! All running agents will be terminated and their work will be lost.

----
url: https://docs.docker.com/guides/rag-ollama/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Build a RAG application using Ollama and Docker

***

This guide demonstrates how to use Docker to deploy Retrieval-Augmented Generation (RAG) models with Ollama.

**Time to complete** 20 minutes

The Retrieval Augmented Generation (RAG) guide teaches you how to containerize an existing RAG application using Docker. The example application is a RAG that acts like a sommelier, giving you the best pairings between wines and food. In this guide, you’ll learn how to:

* Containerize and run a RAG application
* Set up a local environment to run the complete RAG stack locally for development

Start by containerizing an existing RAG application.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/rag-ollama/containerize/)

   Learn how to containerize a RAG application.

2. [Develop your app](https://docs.docker.com/guides/rag-ollama/develop/)

   Learn how to develop your generative RAG application locally.

----
url: https://docs.docker.com/guides/testcontainers-cloud/common-questions/
----

# Common challenges and questions

***

Table of contents

***

### [How is Testcontainers Cloud different from the open-source Testcontainers framework?](#how-is-testcontainers-cloud-different-from-the-open-source-testcontainers-framework)

While the open-source Testcontainers is a library that provides a lightweight APIs for bootstrapping local development and test dependencies with real services wrapped in Docker containers, Testcontainers Cloud provides a cloud runtime for these containers. This reduces the resource strain on local environments and provides more scalability, especially in CI/CD workflows, that enables consistent Testcontainers experience across the organization.

### [What types of containers can I run with Testcontainers Cloud?](#what-types-of-containers-can-i-run-with-testcontainers-cloud)

Testcontainers Cloud supports any containers you would typically use with the Testcontainers framework, including databases (PostgreSQL, MySQL, MongoDB), message brokers (Kafka, RabbitMQ), and other services required for integration testing.

### [Do I need to change my existing test code to use Testcontainers Cloud?](#do-i-need-to-change-my-existing-test-code-to-use-testcontainers-cloud)

No, you don't need to change your existing test code. Testcontainers Cloud integrates seamlessly with the open-source Testcontainers framework. Once the cloud configuration is set up, it automatically manages the containers in the cloud without requiring code changes.

### [How do I integrate Testcontainers Cloud into my project?](#how-do-i-integrate-testcontainers-cloud-into-my-project)

To integrate Testcontainers Cloud, you need to install the Testcontainers Desktop app and select run with Testcontainers Cloud option in the menu. In CI you’ll need to add a workflow step that downloads Testcontainers Cloud agent. No code changes are required beyond enabling Cloud runtime via the Testcontainers Desktop app locally or installing Testcontainers Cloud agent in CI.

### [Can I use Testcontainers Cloud in a CI/CD pipeline?](#can-i-use-testcontainers-cloud-in-a-cicd-pipeline)

Yes, Testcontainers Cloud is designed to work efficiently in CI/CD pipelines. It helps reduce build times and resource bottlenecks by offloading containers that you spin up with Testcontainers library to the cloud, making it a perfect fit for continuous testing environments.

### [What are the benefits of using Testcontainers Cloud?](#what-are-the-benefits-of-using-testcontainers-cloud)

The key benefits include reduced resource usage on local machines and CI servers, scalability (run more containers without performance degradation), consistent testing environments, centralized monitoring, ease of CI configuration with removed security concerns of running Docker-in-Docker or a privileged daemon.

### [Does Testcontainers Cloud support all programming languages?](#does-testcontainers-cloud-support-all-programming-languages)

Testcontainers Cloud supports any language that works with the open-source Testcontainers libraries, including Java, Python, Node.js, Go, and others. As long as your project uses Testcontainers, it can be offloaded to Testcontainers Cloud.

### [How is container cleanup handled in Testcontainers Cloud?](#how-is-container-cleanup-handled-in-testcontainers-cloud)

While Testcontainers library automatically handles container lifecycle management, Testcontainers Cloud manages the allocated cloud worker lifetime. This means that containers are spun up, monitored, and cleaned up after tests are completed by Testcontainers library, and the worker where these containers have being running will be removed automatically after the \~35 min idle period by Testcontainers Cloud. This approach frees developers from manually managing containers and associated cloud resources.

### [Is there a free tier or pricing model for Testcontainers Cloud?](#is-there-a-free-tier-or-pricing-model-for-testcontainers-cloud)

Pricing details for Testcontainers Cloud can be found on the [pricing page](https://testcontainers.com/cloud/pricing/).

----
url: https://docs.docker.com/guides/cpp/deploy/
----

# Test your C++ deployment

***

Table of contents

***

## [Prerequisites](#prerequisites)

* Complete all the previous sections of this guide, starting with [Containerize a C++ application](https://docs.docker.com/guides/cpp/containerize/).
* [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## [Overview](#overview)

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## [Create a Kubernetes YAML file](#create-a-kubernetes-yaml-file)

In your `c-plus-plus-docker` directory, create a file named `docker-kubernetes.yml`. Open the file in an IDE or text editor and add the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker username and the name of the repository that you created in [Configure CI/CD for your C++ application](https://docs.docker.com/guides/cpp/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-c-plus-plus-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: ok-api
  template:
    metadata:
      labels:
        service: ok-api
    spec:
      containers:
        - name: ok-api-service
          image: DOCKER_USERNAME/REPO_NAME
          imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: service-entrypoint
  namespace: default
spec:
  type: NodePort
  selector:
    service: ok-api
  ports:
    - port: 8080
      targetPort: 8080
      nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

* A Deployment, describing a scalable group of identical pods. In this case, you'll get just one replica, or copy of your pod. That pod, which is described under `template`, has just one container in it. The container is created from the image built by GitHub Actions in [Configure CI/CD for your C++ application](https://docs.docker.com/guides/cpp/configure-ci-cd/).
* A NodePort service, which will route traffic from port 30001 on your host to port 8080 inside the pods it routes to, allowing you to reach your app from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## [Deploy and check your application](#deploy-and-check-your-application)

1. In a terminal, navigate to `c-plus-plus-docker` and deploy your application to Kubernetes.

   ```console
   $ kubectl apply -f docker-kubernetes.yml
   ```

   You should see output that looks like the following, indicating your Kubernetes objects were created successfully.

   ```text
   deployment.apps/docker-c-plus-plus-demo created
   service/service-entrypoint created
   ```

2. Make sure everything worked by listing your deployments.

   ```console
   $ kubectl get deployments
   ```

   Your deployment should be listed as follows:

   ```shell
   NAME                     READY   UP-TO-DATE   AVAILABLE    AGE
   docker-c-plus-plus-demo   1/1     1            1           10s
   ```

   This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.

   ```console
   $ kubectl get services
   ```

   You should get output like the following.

   ```shell
   NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
   service-entrypoint   NodePort    10.105.145.223   <none>        8080:30001/TCP   83s
   ```

   In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP.

3. In a browser, visit the following address. You should see the message `{"Status" : "OK"}`.

   ```console
   http://localhost:30001/
   ```

4. Run the following command to tear down your application.

   ```console
   $ kubectl delete -f docker-kubernetes.yml
   ```

## [Summary](#summary)

In this section, you learned how to use Docker Desktop to deploy your C++ application to a fully-featured Kubernetes environment on your development machine.

Related information:

* [Kubernetes documentation](https://kubernetes.io/docs/home/)
* [Deploy on Kubernetes with Docker Desktop](https://docs.docker.com/desktop/use-desktop/kubernetes/)
* [Swarm mode overview](https://docs.docker.com/engine/swarm/)

[Supply-chain security for C++ Docker images »](https://docs.docker.com/guides/cpp/security/)

----
url: https://docs.docker.com/reference/cli/docker/sandbox/save/
----

# docker sandbox save

***

| Description | Save a snapshot of the sandbox as a template |
| ----------- | -------------------------------------------- |
| Usage       | `docker sandbox save SANDBOX TAG`            |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Save a snapshot of the sandbox as a template.

By default, the image is loaded into the host's Docker daemon (requires Docker to be running). Use --output to save the image to a tar file instead.

Examples:

# [Load into host Docker (requires host Docker running)](#load-into-host-docker-requires-host-docker-running)

docker sandbox save my-sandbox myimage:v1.0

# [Save to file (works without host Docker)](#save-to-file-works-without-host-docker)

docker sandbox save my-sandbox myimage:v1.0 --output /tmp/myimage.tar

## [Options](#options)

| Option         | Default | Description                                                           |
| -------------- | ------- | --------------------------------------------------------------------- |
| `-o, --output` |         | Save image to specified tar file instead of loading into host Docker  |

----
url: https://docs.docker.com/desktop/setup/install/linux/
----

# Install Docker Desktop on Linux

***

Table of contents

***

> **Docker Desktop terms**
>
> Commercial use of Docker Desktop in larger enterprises (more than 250 employees or more than $10 million USD in annual revenue) requires a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopLinuxInstall).

This page contains information about general system requirements, supported platforms, and instructions on how to install Docker Desktop for Linux.

> Important
>
> Docker Desktop on Linux runs a Virtual Machine (VM) which creates and uses a custom docker context, `desktop-linux`, on startup.
>
> This means images and containers deployed on the Linux Docker Engine (before installation) are not available in Docker Desktop for Linux.
>
> > Important
> >
> > For commercial use of Docker Engine obtained via Docker Desktop within larger enterprises (exceeding 250 employees or with annual revenue surpassing $10 million USD), a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopLinuxInstall) is required.
>
> Docker Desktop for Linux provides a user-friendly graphical interface that simplifies the management of containers and services. It includes Docker Engine as this is the core technology that powers Docker containers. Docker Desktop for Linux also comes with additional features like Docker Scout and Docker Extensions.
>
> ### [Installing Docker Desktop and Docker Engine](#installing-docker-desktop-and-docker-engine)
>
> Docker Desktop for Linux and Docker Engine can be installed side-by-side on the same machine. Docker Desktop for Linux stores containers and images in an isolated storage location within a VM and offers controls to restrict [its resources](https://docs.docker.com/desktop/settings-and-maintenance/settings/#resources). Using a dedicated storage location for Docker Desktop prevents it from interfering with a Docker Engine installation on the same machine.
>
> While it's possible to run both Docker Desktop and Docker Engine simultaneously, there may be situations where running both at the same time can cause issues. For example, when mapping network ports (`-p` / `--publish`) for containers, both Docker Desktop and Docker Engine may attempt to reserve the same port on your machine, which can lead to conflicts ("port already in use").
>
> We generally recommend stopping the Docker Engine while you're using Docker Desktop to prevent the Docker Engine from consuming resources and to prevent conflicts as described above.
>
> Use the following command to stop the Docker Engine service:
>
> ```console
> $ sudo systemctl stop docker docker.socket containerd
> ```
>
> Depending on your installation, the Docker Engine may be configured to automatically start as a system service when your machine starts. Use the following command to disable the Docker Engine service, and to prevent it from starting automatically:
>
> ```console
> $ sudo systemctl disable docker docker.socket containerd
> ```
>
> ### [Switching between Docker Desktop and Docker Engine](#switching-between-docker-desktop-and-docker-engine)
>
> The Docker CLI can be used to interact with multiple Docker Engines. For example, you can use the same Docker CLI to control a local Docker Engine and to control a remote Docker Engine instance running in the cloud. [Docker Contexts](https://docs.docker.com/engine/manage-resources/contexts/) allow you to switch between Docker Engines instances.
>
> When installing Docker Desktop, a dedicated "desktop-linux" context is created to interact with Docker Desktop. On startup, Docker Desktop automatically sets its own context (`desktop-linux`) as the current context. This means that subsequent Docker CLI commands target Docker Desktop. On shutdown, Docker Desktop resets the current context to the `default` context.
>
> Use the `docker context ls` command to view what contexts are available on your machine. The current context is indicated with an asterisk (`*`).
>
> ```console
> $ docker context ls
> NAME            DESCRIPTION                               DOCKER ENDPOINT                                  ...
> default *       Current DOCKER_HOST based configuration   unix:///var/run/docker.sock                      ...
> desktop-linux                                             unix:///home/<user>/.docker/desktop/docker.sock  ...
> ```
>
> If you have both Docker Desktop and Docker Engine installed on the same machine, you can run the `docker context use` command to switch between the Docker Desktop and Docker Engine contexts. For example, use the "default" context to interact with the Docker Engine:
>
> ```console
> $ docker context use default
> default
> Current context is now "default"
> ```
>
> And use the `desktop-linux` context to interact with Docker Desktop:
>
> ```console
> $ docker context use desktop-linux
> desktop-linux
> Current context is now "desktop-linux"
> ```
>
> Refer to the [Docker Context documentation](https://docs.docker.com/engine/manage-resources/contexts/) for more details.

## [Supported platforms](#supported-platforms)

Docker provides `.deb` and `.rpm` packages for the following Linux distributions and architectures:

| Platform                                                                                     | x86\_64 / amd64 |
| -------------------------------------------------------------------------------------------- | --------------- |
| [Ubuntu](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)                        | ✅               |
| [Debian](https://docs.docker.com/desktop/setup/install/linux/debian/)                        | ✅               |
| [Red Hat Enterprise Linux (RHEL)](https://docs.docker.com/desktop/setup/install/linux/rhel/) | ✅               |
| [Fedora](https://docs.docker.com/desktop/setup/install/linux/fedora/)                        | ✅               |

An experimental package is available for [Arch](https://docs.docker.com/desktop/setup/install/linux/archlinux/)-based distributions. Docker has not tested or verified the installation.

Docker supports Docker Desktop on the current and previous LTS releases of the aforementioned distributions, as well as the most recent version.

## [General system requirements](#general-system-requirements)

To install Docker Desktop successfully, your Linux host must meet the following general requirements:

* 64-bit kernel and CPU support for virtualization.
* KVM virtualization support. Follow the [KVM virtualization support instructions](#kvm-virtualization-support) to check if the KVM kernel modules are enabled and how to provide access to the KVM device.
* QEMU must be version 5.2 or later. We recommend upgrading to the latest version.
* systemd init system.
* GNOME, KDE, or MATE desktop environments are supported but others may work.
  * For many Linux distributions, the GNOME environment does not support tray icons. To add support for tray icons, you need to install a GNOME extension. For example, [AppIndicator](https://extensions.gnome.org/extension/615/appindicator-support/).
* At least 4 GB of RAM.
* Enable configuring ID mapping in user namespaces, see [File sharing](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/#how-do-i-enable-file-sharing). Note that for Docker Desktop version 4.35 and later, this is not required anymore.
* Recommended: [Initialize `pass`](https://docs.docker.com/desktop/setup/sign-in/#credentials-management-for-linux-users) for credentials management.

Docker Desktop for Linux runs a Virtual Machine (VM). For more information on why, see [Why Docker Desktop for Linux runs a VM](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/#why-does-docker-desktop-for-linux-run-a-vm).

> Note
>
> Docker does not provide support for running Docker Desktop for Linux in nested virtualization scenarios. We recommend that you run Docker Desktop for Linux natively on supported distributions.

### [KVM virtualization support](#kvm-virtualization-support)

Docker Desktop runs a VM that requires [KVM support](https://www.linux-kvm.org).

The `kvm` module should load automatically if the host has virtualization support. To load the module manually, run:

```console
$ modprobe kvm
```

Depending on the processor of the host machine, the corresponding module must be loaded:

```console
$ modprobe kvm_intel  # Intel processors

$ modprobe kvm_amd    # AMD processors
```

If the above commands fail, you can view the diagnostics by running:

```console
$ kvm-ok
```

To check if the KVM modules are enabled, run:

```console
$ lsmod | grep kvm
kvm_amd               167936  0
ccp                   126976  1 kvm_amd
kvm                  1089536  1 kvm_amd
irqbypass              16384  1 kvm
```

#### [Set up KVM device user permissions](#set-up-kvm-device-user-permissions)

To check ownership of `/dev/kvm`, run :

```console
$ ls -al /dev/kvm
```

Add your user to the kvm group in order to access the kvm device:

```console
$ sudo usermod -aG kvm $USER
```

Sign out and sign back in so that your group membership is re-evaluated.

## [Using Docker SDKs with Docker Desktop](#using-docker-sdks-with-docker-desktop)

Docker Desktop for Linux uses a per-user socket instead of the system-wide `/var/run/docker.sock`. Docker SDKs and tools that connect directly to the Docker daemon need the `DOCKER_HOST` environment variable set to connect to Docker Desktop. For configuration details, see [How do I use Docker SDKs with Docker Desktop for Linux?](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/#how-do-i-use-docker-sdks-with-docker-desktop-for-linux).

## [Where to go next](#where-to-go-next)

* Install Docker Desktop for Linux for your specific Linux distribution:

  * [Install on Ubuntu](https://docs.docker.com/desktop/setup/install/linux/ubuntu/)
  * [Install on Debian](https://docs.docker.com/desktop/setup/install/linux/debian/)
  * [Install on Red Hat Enterprise Linux (RHEL)](https://docs.docker.com/desktop/setup/install/linux/rhel/)
  * [Install on Fedora](https://docs.docker.com/desktop/setup/install/linux/fedora/)
  * [Install on Arch](https://docs.docker.com/desktop/setup/install/linux/archlinux/)

----
url: https://docs.docker.com/reference/cli/docker/desktop/disable/
----

# docker desktop disable

***

| Description | Disable a feature |
| ----------- | ----------------- |

## [Description](#description)

Disable an individual feature

## [Subcommands](#subcommands)

| Command                                                                                                             | Description                 |
| ------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| [`docker desktop disable model-runner`](https://docs.docker.com/reference/cli/docker/desktop/disable/model-runner/) | Disable Docker Model Runner |

----
url: https://docs.docker.com/extensions/extensions-sdk/architecture/security/
----

# Extension security

***

Table of contents

***

## [Extension capabilities](#extension-capabilities)

An extension can have the following optional parts:

* A user interface in HTML or JavaScript, displayed in Docker Desktop Dashboard
* A backend part that runs as a container
* Executables deployed on the host machine.

Extensions are executed with the same permissions as the Docker Desktop user. Extension capabilities include running any Docker commands (including running containers and mounting folders), running extension binaries, and accessing files on your machine that are accessible by the user running Docker Desktop. Note that extensions are not restricted to execute binaries that they list in the [host section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) of the extension metadata: since these binaries can contain any code running as user, they can in turn execute any other commands as long as the user has rights to execute them.

The Extensions SDK provides a set of JavaScript APIs to invoke commands or invoke these binaries from the extension UI code. Extensions can also provide a backend part that starts a long-lived running container in the background.

> Important
>
> Make sure you trust the publisher or author of the extension when you install it, as the extension has the same access rights as the user running Docker Desktop.

----
url: https://docs.docker.com/get-started/docker_cheatsheet.pdf
----

CLI Cheat Sheet  Build an Image from a Dockerfile  Build an Image from a Dockerfile without the cache  docker   build   -t   <image_name>   .   –no-cache  List local images  docker   images  Delete an Image  docker   rmi   <image_name>  Remove all unused images  docker   image   prune  Login into Docker  docker   login   -u   <username>  Publish an image to Docker Hub  docker   push   <username>/<image_name>  Search Hub for an image  docker   search   <image_name>  Pull an image from a Docker Hub  docker   pull   <image_name>  Create and run a container from an image, with a custom name:  docker   run   --name   <container_name>   <image_name>  Run a container with and publish a container’s port(s) to the host.  docker   run   -p   <host_port>:<container_port>   <image_name>  Run a container in the background  docker   run   -d   <image_name>  Start or stop an existing container:  docker   start|stop   <container_name>   (or   <container-id>)  Remove a stopped container:  docker   rm   <container_name>  Open a shell inside a running container:  docker   exec   -it   <container_name>   sh  Fetch and follow the logs of a container:  docker   logs   -f   <container_name>  To inspect a running container:  docker   inspect   <container_name>   (or   <container_id>)  To list currently running containers:  docker   ps  List all docker containers (running and stopped):  docker   ps   --all  View resource usage stats  docker   container   stats  GENERAL COMMANDS  Docker provides the ability to package and run an application in a loosely isolated environment called a container.  The isolation and security allows you to run many containers simultaneously on a given host. Containers are  lightweight and contain everything needed to run the application, so you do not need to rely on what is currently  installed on the host. You can easily share containers while you work, and be sure that everyone you share with gets  the same container that works in the same way.  IMAGES  Docker images are a lightweight, standalone, executable package  of software that includes everything needed to run an application:  code, runtime, system tools, system libraries and settings.  DOCKER HUB  Docker Hub is a service provided by Docker for finding and sharing  container images with your team. Learn more and find images  at https://hub.docker.com  CONTAINERS  A container is a runtime instance of a docker image. A container  will always run the same, regardless of the infrastructure.  Containers isolate software from its environment and ensure  that it works uniformly despite differences for instance between  development and staging.  Start the docker daemon  docker   -d  Get help with Docker. Can also use –help on all subcommands  docker   --help  Display system-wide information  docker   info  INSTALLATION  Docker Desktop is available for Mac, Linux and Windows  https://docs.docker.com/desktop  View example projects that use Docker  https://github.com/docker/awesome-compose  Check out our docs for information on using Docker  https://docs.docker.com  docker   build   -t   <image_name> .

----
url: https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/
----

# Persisting container data

***

Table of contents

***

## [Explanation](#explanation)

When a container starts, it uses the files and configuration provided by the image. Each container is able to create, modify, and delete files and does so without affecting any other containers. When the container is deleted, these file changes are also deleted.

While this ephemeral nature of containers is great, it poses a challenge when you want to persist the data. For example, if you restart a database container, you might not want to start with an empty database. So, how do you persist files?

### [Container volumes](#container-volumes)

Volumes are a storage mechanism that provide the ability to persist data beyond the lifecycle of an individual container. Think of it like providing a shortcut or symlink from inside the container to outside the container.

As an example, imagine you create a volume named `log-data`.

```console
$ docker volume create log-data
```

When starting a container with the following command, the volume will be mounted (or attached) into the container at `/logs`:

```console
$ docker run -d -p 80:80 -v log-data:/logs docker/welcome-to-docker
```

If the volume `log-data` doesn't exist, Docker will automatically create it for you.

When the container runs, all files it writes into the `/logs` folder will be saved in this volume, outside of the container. If you delete the container and start a new container using the same volume, the files will still be there.

> **Sharing files using volumes**
>
> You can attach the same volume to multiple containers to share files between containers. This might be helpful in scenarios such as log aggregation, data pipelines, or other event-driven applications.

### [Managing volumes](#managing-volumes)

Volumes have their own lifecycle beyond that of containers and can grow quite large depending on the type of data and applications you’re using. The following commands will be helpful to manage volumes:

* `docker volume ls` - list all volumes
* `docker volume rm <volume-name-or-id>` - remove a volume (only works when the volume is not attached to any containers)
* `docker volume prune` - remove all unused (unattached) volumes

## [Try it out](#try-it-out)

In this guide, you'll practice creating and using volumes to persist data created by a Postgres container. When the database runs, it stores files into the `/var/lib/postgresql` directory. By attaching the volume here, you will be able to restart the container multiple times while keeping the data.

### [Use volumes](#use-volumes)

1. [Download and install](/get-started/get-docker/) Docker Desktop.

2. Start a container using the [Postgres image](https://hub.docker.com/_/postgres) with the following command:

   ```console
   $ docker run --name=db -e POSTGRES_PASSWORD=secret -d -v postgres_data:/var/lib/postgresql postgres:18
   ```

   This will start the database in the background, configure it with a password, and attach a volume to the directory PostgreSQL will persist the database files.

3. Connect to the database by using the following command:

   ```console
   $ docker exec -ti db psql -U postgres
   ```

4. In the PostgreSQL command line, run the following to create a database table and insert two records:

   ```text
   CREATE TABLE tasks (
       id SERIAL PRIMARY KEY,
       description VARCHAR(100)
   );
   INSERT INTO tasks (description) VALUES ('Finish work'), ('Have fun');
   ```

5. Verify the data is in the database by running the following in the PostgreSQL command line:

   ```text
   SELECT * FROM tasks;
   ```

   You should get output that looks like the following:

   ```text
    id | description
   ----+-------------
     1 | Finish work
     2 | Have fun
   (2 rows)
   ```

6. Exit out of the PostgreSQL shell by running the following command:

   ```console
   \q
   ```

7. Stop and remove the database container. Remember that, even though the container has been deleted, the data is persisted in the `postgres_data` volume.

   ```console
   $ docker stop db
   $ docker rm db
   ```

8. Start a new container by running the following command, attaching the same volume with the persisted data:

   ```console
   $ docker run --name=new-db -d -v postgres_data:/var/lib/postgresql postgres:18
   ```

   You might have noticed that the `POSTGRES_PASSWORD` environment variable has been omitted. That’s because that variable is only used when bootstrapping a new database.

9. Verify the database still has the records by running the following command:

   ```console
   $ docker exec -ti new-db psql -U postgres -c "SELECT * FROM tasks"
   ```

### [View volume contents](#view-volume-contents)

The Docker Desktop Dashboard provides the ability to view the contents of any volume, as well as the ability to export, import, empty, delete and clone volumes.

1. Open the Docker Desktop Dashboard and navigate to the **Volumes** view. In this view, you should see the **postgres\_data** volume.

2. Select the **postgres\_data** volume’s name.

3. The **Stored Data** tab shows the contents of the volume and provides the ability to navigate the files. The **Container in-use** tab displays the name of the container using the volume, the image name, the port number used by the container, and the target. A target is a path inside a container that gives access to the files in the volume. The **Exports** tab lets you export the volume. Double-clicking on a file will let you see the contents and make changes.

4. Right-click on any file to save it or delete it.

### [Remove volumes](#remove-volumes)

Before removing a volume, it must not be attached to any containers. If you haven’t removed the previous container, do so with the following command (the `-f` will stop the container first and then remove it):

```console
$ docker rm -f new-db
```

There are a few methods to remove volumes, including the following:

* Select the **Delete Volume** option on a volume in the Docker Desktop Dashboard.

* Use the `docker volume rm` command:

  ```console
  $ docker volume rm postgres_data
  ```

* Use the `docker volume prune` command to remove all unused volumes:

  ```console
  $ docker volume prune
  ```

## [Additional resources](#additional-resources)

The following resources will help you learn more about volumes:

* [Manage data in Docker](/engine/storage)
* [Volumes](/engine/storage/volumes)
* [Volume mounts](/engine/containers/run/#volume-mounts)

## [Next steps](#next-steps)

Now that you have learned about persisting container data, it’s time to learn about sharing local files with containers.

[Sharing local files with containers](https://docs.docker.com/get-started/docker-concepts/running-containers/sharing-local-files/)

----
url: https://docs.docker.com/reference/compose-file/volumes/
----

# Define and manage volumes in Docker Compose

***

Table of contents

***

Volumes are persistent data stores implemented by the container engine. Compose offers a neutral way for services to mount volumes, and configuration parameters to allocate them to infrastructure. The top-level `volumes` declaration lets you configure named volumes that can be reused across multiple services.

To use a volume across multiple services, you must explicitly grant each service access by using the [volumes](https://docs.docker.com/reference/compose-file/services/#volumes) attribute within the `services` top-level element. The `volumes` attribute has additional syntax that provides more granular control.

> Tip
>
> Working with large repositories or monorepos, or with virtual file systems that are no longer scaling with your codebase? Compose now takes advantage of [Synchronized file shares](https://docs.docker.com/desktop/features/synchronized-file-sharing/) and automatically creates file shares for bind mounts. Ensure you're signed in to Docker with a paid subscription and have enabled both **Access experimental features** and **Manage Synchronized file shares with Compose** in Docker Desktop's settings.

## [Example](#example)

The following example shows a two-service setup where a database's data directory is shared with another service as a volume, named `db-data`, so that it can be periodically backed up.

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data:/etc/data

  backup:
    image: backup-service
    volumes:
      - db-data:/var/lib/backup/data

volumes:
  db-data:
```

The `db-data` volume is mounted at the `/var/lib/backup/data` and `/etc/data` container paths for backup and backend respectively.

Running `docker compose up` creates the volume if it doesn't already exist. Otherwise, the existing volume is used and is recreated if it's manually deleted outside of Compose.

## [Attributes](#attributes)

An entry under the top-level `volumes` section can be empty, in which case it uses the container engine's default configuration for creating a volume. Optionally, you can configure it with the following keys:

### [`driver`](#driver)

Specifies which volume driver should be used. If the driver is not available, Compose returns an error and doesn't deploy the application.

```yml
volumes:
  db-data:
    driver: foobar
```

### [`driver_opts`](#driver_opts)

`driver_opts` specifies a list of options as key-value pairs to pass to the driver for this volume. The options are driver-dependent.

```yml
volumes:
  example:
    driver_opts:
      type: "nfs"
      o: "addr=10.40.0.199,nolock,soft,rw"
      device: ":/docker/example"
```

If you want a named bind mount, use the `local` driver with `driver_opts`. This pattern gives a Compose volume a stable name while mapping it to a specific host path:

```yaml
volumes:
  app-data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: /srv/app-data # must be the absolute host path and already exist
```

The `type`, `o`, and `device` keys are passed through to the local driver. For a one-off host-path mount on a single service, see [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/).

### [`external`](#external)

If set to `true`:

* `external` specifies that this volume already exists on the platform and its lifecycle is managed outside of that of the application. Compose then doesn't create the volume and returns an error if the volume doesn't exist.
* All other attributes apart from `name` are irrelevant. If Compose detects any other attribute, it rejects the Compose file as invalid.

In the following example, instead of attempting to create a volume called `{project_name}_db-data`, Compose looks for an existing volume simply called `db-data` and mounts it into the `backend` service's containers.

```yml
services:
  backend:
    image: example/database
    volumes:
      - db-data:/etc/data

volumes:
  db-data:
    external: true
```

### [`labels`](#labels)

`labels` are used to add metadata to volumes. You can use either an array or a dictionary.

It's recommended that you use reverse-DNS notation to prevent your labels from conflicting with those used by other software.

```yml
volumes:
  db-data:
    labels:
      com.example.description: "Database volume"
      com.example.department: "IT/Ops"
      com.example.label-with-empty-value: ""
```

```yml
volumes:
  db-data:
    labels:
      - "com.example.description=Database volume"
      - "com.example.department=IT/Ops"
      - "com.example.label-with-empty-value"
```

Compose sets `com.docker.compose.project` and `com.docker.compose.volume` labels.

> Note
>
> Labels defined here apply to named volumes only. They’re stored on the volume resource and visible via `docker volume inspect`. They do not apply to bind mounts and do not change mount semantics.

### [`name`](#name)

`name` sets a custom name for a volume. The name field can be used to reference volumes that contain special characters. The name is used as is and is not scoped with the stack name.

```yml
volumes:
  db-data:
    name: "my-app-data"
```

This makes it possible to make this lookup name a parameter of the Compose file, so that the model ID for the volume is hard-coded but the actual volume ID on the platform is set at runtime during deployment.

For example, if `DATABASE_VOLUME=my_volume_001` is in your `.env` file:

```yml
volumes:
  db-data:
    name: ${DATABASE_VOLUME}
```

Running `docker compose up` uses the volume called `my_volume_001`.

It can also be used in conjunction with the `external` property. This means the name used to look up the actual volume on the platform is set separately from the name used to refer to the volume within the Compose file:

```yml
volumes:
  db-data:
    external: true
    name: actual-name-of-volume
```

----
url: https://docs.docker.com/engine/logging/plugins/
----

# Use a logging driver plugin

***

Table of contents

***

Docker logging plugins allow you to extend and customize Docker's logging capabilities beyond those of the [built-in logging drivers](https://docs.docker.com/engine/logging/configure/). A logging service provider can [implement their own plugins](https://docs.docker.com/engine/extend/plugins_logging/) and make them available on Docker Hub, or a private registry. This topic shows how a user of that logging service can configure Docker to use the plugin.

## [Install the logging driver plugin](#install-the-logging-driver-plugin)

To install a logging driver plugin, use `docker plugin install <org/image>`, using the information provided by the plugin developer.

You can list all installed plugins using `docker plugin ls`, and you can inspect a specific plugin using `docker inspect`.

## [Configure the plugin as the default logging driver](#configure-the-plugin-as-the-default-logging-driver)

When the plugin is installed, you can configure the Docker daemon to use it as the default by setting the plugin's name as the value of the `log-driver` key in the `daemon.json`, as detailed in the [logging overview](https://docs.docker.com/engine/logging/configure/#configure-the-default-logging-driver). If the logging driver supports additional options, you can set those as the values of the `log-opts` array in the same file.

## [Configure a container to use the plugin as the logging driver](#configure-a-container-to-use-the-plugin-as-the-logging-driver)

After the plugin is installed, you can configure a container to use the plugin as its logging driver by specifying the `--log-driver` flag to `docker run`, as detailed in the [logging overview](https://docs.docker.com/engine/logging/configure/#configure-the-logging-driver-for-a-container). If the logging driver supports additional options, you can specify them using one or more `--log-opt` flags with the option name as the key and the option value as the value.

----
url: https://docs.docker.com/reference/compose-file/secrets/
----

# Secrets

***

Table of contents

***

Secrets are a flavor of [Configs](https://docs.docker.com/reference/compose-file/configs/) focusing on sensitive data, with specific constraint for this usage.

Services can only access secrets when explicitly granted by a [`secrets` attribute](https://docs.docker.com/reference/compose-file/services/#secrets) within the `services` top-level element.

The top-level `secrets` declaration defines or references sensitive data that is granted to the services in your Compose application. The source of the secret is either `file` or `environment`.

* `file`: The secret is created with the contents of the file at the specified path.
* `environment`: The secret is created with the value of an environment variable on the host. This is only supported by Docker Compose. It is not supported when deploying with [`docker stack deploy`](https://docs.docker.com/engine/swarm/stack-deploy/).

## [Example 1](#example-1)

`server-certificate` secret is created as `<project_name>_server-certificate` when the application is deployed, by registering content of the `server.cert` as a platform secret.

```yml
secrets:
  server-certificate:
    file: ./server.cert
```

## [Example 2](#example-2)

`token` secret is created as `<project_name>_token` when the application is deployed, by registering the content of the `OAUTH_TOKEN` environment variable as a platform secret.

```yml
secrets:
  token:
    environment: "OAUTH_TOKEN"
```

> Note
>
> `environment` secrets are not supported when deploying with `docker stack deploy`. Use `file` or `external` as the secret source instead.

## [Additional resources](#additional-resources)

For more information, see [How to use secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/).

----
url: https://docs.docker.com/engine/release-notes/26.0/
----

# Docker Engine 26.0 release notes

***

Table of contents

***

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 26.0.

For more information about:

* Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
* Changes to the Engine API, see [Engine API version history](/reference/api/engine/version-history/).

## [26.0.2](#2602)

*2024-04-18*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.0.2)
* [moby/moby, 26.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.0.2)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.0.2/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.0.2/docs/api/version-history.md).

### [Security](#security)

This release contains a security fix for [CVE-2024-32473](https://github.com/moby/moby/security/advisories/GHSA-x84c-p2g9-rqv9), an unexpected configuration of IPv6 on IPv4-only interfaces.

### [Bug fixes and enhancements](#bug-fixes-and-enhancements)

* [CVE-2024-32473](https://github.com/moby/moby/security/advisories/GHSA-x84c-p2g9-rqv9): Ensure IPv6 is disabled on interfaces only allocated an IPv4 address by the engine. [moby#GHSA-x84c-p2g9-rqv9](https://github.com/moby/moby/security/advisories/GHSA-x84c-p2g9-rqv9)

## [26.0.1](#2601)

*2024-04-11*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.0.1)
* [moby/moby, 26.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.0.1)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.0.1/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.0.1/docs/api/version-history.md).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-1)

* Fix a regression that meant network interface specific `--sysctl` options prevented container startup. [moby/moby#47646](https://github.com/moby/moby/pull/47646)
* Remove erroneous `platform` from image `config` OCI descriptor in `docker save` output. [moby/moby#47694](https://github.com/moby/moby/pull/47694)
* containerd image store: OCI archives produced by `docker save` will now have a non-empty `mediaType` field in `index.json` [moby/moby#47701](https://github.com/moby/moby/pull/47701)
* Fix a regression that prevented the internal resolver from forwarding requests from IPvlan L3 networks to external resolvers. [moby/moby#47705](https://github.com/moby/moby/pull/47705)
* Prevent the use of external resolvers in IPvlan and Macvlan networks created with no parent interface specified. [moby/moby#47705](https://github.com/moby/moby/pull/47705)

### [Packaging updates](#packaging-updates)

* Update Go runtime to 1.21.9 [moby/moby#47671](https://github.com/moby/moby/pull/47671), [docker/cli#4987](https://github.com/docker/cli/pull/4987)
* Update Compose to [v1.26.1 ](https://github.com/docker/compose/releases/tag/v2.26.1), [docker/docker-ce-packaging#1009](https://github.com/docker/docker-ce-packaging/pull/1009)
* Update containerd to [v1.7.15](https://github.com/containerd/containerd/releases/tag/v1.7.15) (static binaries only) [moby/moby#47692](https://github.com/moby/moby/pull/47692)

## [26.0.0](#2600)

*2024-03-20*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 26.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A26.0.0)
* [moby/moby, 26.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A26.0.0)
* Deprecated and removed features, see [Deprecated Features](https://github.com/docker/cli/blob/v26.0.0/docs/deprecated.md).
* Changes to the Engine API, see [API version history](https://github.com/moby/moby/blob/v26.0.0/docs/api/version-history.md).

### [Security](#security-1)

This release contains a security fix for [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx), a potential data exfiltration from 'internal' networks via authoritative DNS servers.

### [New](#new)

* Add `Subpath` field to the `VolumeOptions` making it possible to mount a subpath of a volume. [moby/moby#45687](https://github.com/moby/moby/pull/45687)
* Add `volume-subpath` support to the mount flag (`--mount type=volume,...,volume-subpath=<subpath>`). [docker/cli#4331](https://github.com/docker/cli/pull/4331)
* Accept `=` separators and `[ipv6]` in compose files for `docker stack deploy`. [docker/cli#4860](https://github.com/docker/cli/pull/4860)
* rootless: Add support for enabling host loopback by setting the `DOCKERD_ROOTLESS_ROOTLESSKIT_DISABLE_HOST_LOOPBACK` environment variable to `false` (defaults to `true`). This lets containers connect to the host by using IP address `10.0.2.2`. [moby/moby#47352](https://github.com/moby/moby/pull/47352)
* containerd image store: `docker image ls` no longer creates duplicates entries for multi-platform images. [moby/moby#45967](https://github.com/moby/moby/pull/45967)
* containerd image store: Send Prometheus metrics. [moby/moby#47555](https://github.com/moby/moby/pull/47555)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-2)

* [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx): Do not forward requests to external DNS servers for a container that is only connected to an 'internal' network. Previously, requests were forwarded if the host's DNS server was running on a loopback address, like systemd's 127.0.0.53. [moby/moby#47589](https://github.com/moby/moby/pull/47589)

* Ensure that a generated MAC address is not restored when a container is restarted, but a configured MAC address is preserved. [moby/moby#47233](https://github.com/moby/moby/pull/47233)

  > Warning
  >
  > Containers created using Docker Engine 25.0.0 may have duplicate MAC addresses, they must be re-created. Containers created using version 25.0.0 or 25.0.1 with user-defined MAC addresses will get generated MAC addresses when they are started using 25.0.2. They must also be re-created.

* Always attempt to enable IPv6 on a container's loopback interface, and only include IPv6 in `/etc/hosts` if successful. [moby/moby#47062](https://github.com/moby/moby/pull/47062)

  > Note
  >
  > By default, IPv6 will remain enabled on a container's loopback interface when the container is not connected to an IPv6-enabled network. For example, containers that are only connected to an IPv4-only network now have the `::1` address on their loopback interface.
  >
  > To disable IPv6 in a container, use option `--sysctl net.ipv6.conf.all.disable_ipv6=1` in the `create` or `run` command, or the equivalent `sysctls` option in the service configuration section of a Compose file.
  >
  > If IPv6 is not available in a container because it has been explicitly disabled for the container, or the host's networking stack does not have IPv6 enabled (or for any other reason) the container's `/etc/hosts` file will not include IPv6 entries.

* Fix `ADD` Dockerfile instruction failing with `lsetxattr <file>: operation not supported` when unpacking archive with xattrs onto a filesystem that doesn't support them. [moby/moby#47175](https://github.com/moby/moby/pull/47175)

* Fix `docker container start` failing when used with `--checkpoint`. [moby/moby#47456](https://github.com/moby/moby/pull/47456)

* Restore IP connectivity between the host and containers on an internal bridge network. [moby/moby#47356](https://github.com/moby/moby/pull/47356)

* Do not enforce new validation rules for existing swarm networks. [moby/moby#47361](https://github.com/moby/moby/pull/47361)

* Restore DNS names for containers in the default "nat" network on Windows. [moby/moby#47375](https://github.com/moby/moby/pull/47375)

* Print hint when invoking `docker image ls` with ambiguous argument. [docker/cli#4849](https://github.com/docker/cli/pull/4849)

* Cleanup `@docker_cli_[UUID]` files on OpenBSD. [docker/cli#4862](https://github.com/docker/cli/pull/4862)

* Add explicit [deprecation notice](https://github.com/docker/cli/blob/v26.0.0/docs/deprecated.md#unauthenticated-tcp-connections) message when using remote TCP connections without TLS. [docker/cli#4928](https://github.com/docker/cli/pull/4928), [moby/moby#47556](https://github.com/moby/moby/pull/47556)

* Use IPv6 nameservers from the host's `resolv.conf` as upstream resolvers for Docker Engine's internal DNS, rather than listing them in the container's `resolv.conf`. [moby/moby#47512](https://github.com/moby/moby/pull/47512)

* containerd image store: Isolate images with different containerd namespaces when `--userns-remap` option is used. [moby/moby#46786](https://github.com/moby/moby/pull/46786)

* containerd image store: Fix image pull not emitting `Pulling fs layer` status. [moby/moby#47432](https://github.com/moby/moby/pull/47432)

### [API](#api)

* To preserve backwards compatibility, read-only mounts are not recursive by default when using older clients (API version < v1.44). [moby/moby#47391](https://github.com/moby/moby/pull/47391)
* `GET /images/{id}/json` omits the `Created` field (previously it was `0001-01-01T00:00:00Z`) if the `Created` field is missing from the image config. [moby/moby#47451](https://github.com/moby/moby/pull/47451)
* Populate a missing `Created` field in `GET /images/{id}/json` with `0001-01-01T00:00:00Z` for API version <= 1.43. [moby/moby#47387](https://github.com/moby/moby/pull/47387)
* The `is_automated` field in the `POST /images/search` endpoint results is always `false` now. Consequently, searching for `is-automated=true` will yield no results, while `is-automated=false` will be a no-op. [moby/moby#47465](https://github.com/moby/moby/pull/47465)
* Remove `Container` and `ContainerConfig` fields from the `GET /images/{name}/json` response. [moby/moby#47430](https://github.com/moby/moby/pull/47430)

### [Packaging updates](#packaging-updates-1)

* Update BuildKit to [v0.13.1](https://github.com/moby/buildkit/releases/tag/v0.13.1). [moby/moby#47582](https://github.com/moby/moby/pull/47582)
* Update Buildx to [v0.13.1](https://github.com/docker/buildx/releases/tag/v0.13.1). [docker/docker-ce-packaging#1000](https://github.com/docker/docker-ce-packaging/pull/1000)
* Update Compose to [v2.25.0](https://github.com/docker/compose/releases/tag/v2.25.0). [docker/docker-ce-packaging#1002](https://github.com/docker/docker-ce-packaging/pull/1002)
* Update Go runtime to [1.21.8](https://go.dev/doc/devel/release#go1.21.8). [moby/moby#47502](https://github.com/moby/moby/pull/47502)
* Update RootlessKit to [v2.0.2](https://github.com/rootless-containers/rootlesskit/releases/tag/v2.0.2). [moby/moby#47508](https://github.com/moby/moby/pull/47504)
* Update containerd to v1.7.13 (static binaries only) [moby/moby#47278](https://github.com/moby/moby/pull/47278)
* Update runc binary to v1.1.12 [moby/moby#47268](https://github.com/moby/moby/pull/47268)
* Update OTel to v0.46.1 / v1.21.0 [moby/moby#47245](https://github.com/moby/moby/pull/47245)

### [Removed](#removed)

* Remove `Container` and `ContainerConfig` fields from the `GET /images/{name}/json` response. [moby/moby#47430](https://github.com/moby/moby/pull/47430)

* Deprecate the ability to accept remote TCP connections without TLS. [Deprecation notice](https://github.com/docker/cli/tree/v26.0.0/deprecation.md#unauthenticated-tcp-connections) [docker/cli#4928](https://github.com/docker/cli/pull/4928) [moby/moby#47556](https://github.com/moby/moby/pull/47556).

* Remove deprecated API versions (API < v1.24) [moby/moby#47155](https://github.com/moby/moby/pull/47155)

* Disable pulling of deprecated image formats by default. These image formats are deprecated, and support will be removed in a future version. [moby/moby#47459](https://github.com/moby/moby/pull/47459)

* image: remove deprecated IDFromDigest [moby/moby#47198](https://github.com/moby/moby/pull/47198)

* Remove the deprecated `github.com/docker/docker/pkg/loopback` package. [moby/moby#47128](https://github.com/moby/moby/pull/47128)

* pkg/system: remove deprecated `ErrNotSupportedOperatingSystem`, `IsOSSupported` [moby/moby#47129](https://github.com/moby/moby/pull/47129)

* pkg/homedir: remove deprecated Key() and GetShortcutString() [moby/moby#47130](https://github.com/moby/moby/pull/47130)

* pkg/containerfs: remove deprecated ResolveScopedPath [moby/moby#47131](https://github.com/moby/moby/pull/47131)

* The daemon flag `--oom-score-adjust` was deprecated in v24.0 and is now removed. [moby/moby#46113](https://github.com/moby/moby/pull/46113)

* Remove deprecated aliases from the api/types package. These types were deprecated in v25.0.0, which provided temporary aliases. [moby/moby#47148](https://github.com/moby/moby/pull/47148) These aliases are now removed: `types.Info`, `types.Commit`, `types.PluginsInfo`, `types.NetworkAddressPool`, `types.Runtime`, `types.SecurityOpt`, `types.KeyValue`, `types.DecodeSecurityOptions`, `types.CheckpointCreateOptions`, `types.CheckpointListOptions`, `types.CheckpointDeleteOptions`, `types.Checkpoint`, `types.ImageDeleteResponseItem`, `types.ImageSummary`, `types.ImageMetadata`, `types.ServiceUpdateResponse`, `types.ServiceCreateResponse`, `types.ResizeOptions`, `types.ContainerAttachOptions`, `types.ContainerCommitOptions`, `types.ContainerRemoveOptions`, `types.ContainerStartOptions`, `types.ContainerListOptions`, `types.ContainerLogsOptions`

* cli/command/container: remove deprecated `NewStartOptions()` [docker/cli#4811](https://github.com/docker/cli/pull/4811)

* cli/command: remove deprecated `DockerCliOption`, `InitializeOpt` [docker/cli#4810](https://github.com/docker/cli/pull/4810)

----
url: https://docs.docker.com/build/cache/optimize/
----

# Optimize cache usage in builds

***

Table of contents

***

When building with Docker, a layer is reused from the build cache if the instruction and the files it depends on hasn't changed since it was previously built. Reusing layers from the cache speeds up the build process because Docker doesn't have to rebuild the layer again.

Here are a few techniques you can use to optimize build caching and speed up the build process:

* [Order your layers](#order-your-layers): Putting the commands in your Dockerfile into a logical order can help you avoid unnecessary cache invalidation.
* [Keep the context small](#keep-the-context-small): The context is the set of files and directories that are sent to the builder to process a build instruction. Keeping the context as small as possible reduces the amount of data that needs to be sent to the builder, and reduces the likelihood of cache invalidation.
* [Use bind mounts](#use-bind-mounts): Bind mounts let you mount a file or directory from the host machine into the build container. Using bind mounts can help you avoid unnecessary layers in the image, which can slow down the build process.
* [Use cache mounts](#use-cache-mounts): Cache mounts let you specify a persistent package cache to be used during builds. The persistent cache helps speed up build steps, especially steps that involve installing packages using a package manager. Having a persistent cache for packages means that even if you rebuild a layer, you only download new or changed packages.
* [Use an external cache](#use-an-external-cache): An external cache lets you store build cache at a remote location. The external cache image can be shared between multiple builds, and across different environments.

## [Order your layers](#order-your-layers)

Putting the commands in your Dockerfile into a logical order is a great place to start. Because a change causes a rebuild for steps that follow, try to make expensive steps appear near the beginning of the Dockerfile. Steps that change often should appear near the end of the Dockerfile, to avoid triggering rebuilds of layers that haven't changed.

Consider the following example. A Dockerfile snippet that runs a JavaScript build from the source files in the current directory:

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY . .          # Copy over all files in the current directory
RUN npm install   # Install dependencies
RUN npm build     # Run build
```

This Dockerfile is rather inefficient. Updating any file causes a reinstall of all dependencies every time you build the Docker image even if the dependencies didn't change since last time.

Instead, the `COPY` command can be split in two. First, copy over the package management files (in this case, `package.json` and `yarn.lock`). Then, install the dependencies. Finally, copy over the project source code, which is subject to frequent change.

```dockerfile
# syntax=docker/dockerfile:1
FROM node
WORKDIR /app
COPY package.json yarn.lock .    # Copy package management files
RUN npm install                  # Install dependencies
COPY . .                         # Copy over project files
RUN npm build                    # Run build
```

By installing dependencies in earlier layers of the Dockerfile, there is no need to rebuild those layers when a project file has changed.

## [Keep the context small](#keep-the-context-small)

The easiest way to make sure your context doesn't include unnecessary files is to create a `.dockerignore` file in the root of your build context. The `.dockerignore` file works similarly to `.gitignore` files, and lets you exclude files and directories from the build context.

Here's an example `.dockerignore` file that excludes the `node_modules` directory, all files and directories that start with `tmp`:

.dockerignore

```plaintext
node_modules
tmp*
```

Ignore-rules specified in the `.dockerignore` file apply to the entire build context, including subdirectories. This means it's a rather coarse-grained mechanism, but it's a good way to exclude files and directories that you know you don't need in the build context, such as temporary files, log files, and build artifacts.

## [Use bind mounts](#use-bind-mounts)

You might be familiar with bind mounts for when you run containers with `docker run` or Docker Compose. Bind mounts let you mount a file or directory from the host machine into a container.

```bash
# bind mount using the -v flag
docker run -v $(pwd):/path/in/container image-name
# bind mount using the --mount flag
docker run --mount=type=bind,src=.,dst=/path/in/container image-name
```

To use bind mounts in a build, you can use the `--mount` flag with the `RUN` instruction in your Dockerfile:

```dockerfile
FROM golang:latest
WORKDIR /build
RUN --mount=type=bind,target=. go build -o /app/hello
```

In this example, the current directory is mounted into the build container at `/build` before the `go build` command gets executed. The build output is written to `/app/hello`, which is outside the mount point. This distinction is important: the build output must be written outside the bind mount target, since the mount is read-only by default. The source code is available in the build container for the duration of that `RUN` instruction. When the instruction is done executing, the mounted files are not persisted in the final image, or in the build cache. Only the output of the `go build` command remains.

The `COPY` and `ADD` instructions in a Dockerfile lets you copy files from the build context into the build container. Using bind mounts is beneficial for build cache optimization because you're not adding unnecessary layers to the cache. If you have build context that's on the larger side, and it's only used to generate an artifact, you're better off using bind mounts to temporarily mount the source code required to generate the artifact into the build. If you use `COPY` to add the files to the build container, BuildKit will include all of those files in the cache, even if the files aren't used in the final image.

There are a few things to be aware of when using bind mounts in a build:

* Bind mounts are read-only by default. If you need to write to the mounted directory, you need to specify the `rw` option. However, even with the `rw` option, the changes are not persisted in the final image or the build cache. The file writes are sustained for the duration of the `RUN` instruction, and are discarded after the instruction is done.

* Mounted files are not persisted in the final image. Only the output of the `RUN` instruction is persisted in the final image. If you need to include files from the build context in the final image, you need to use the `COPY` or `ADD` instructions.

* If the target directory is not empty, the contents of the target directory are hidden by the mounted files. The original contents are restored after the `RUN` instruction is done.

  For example, given a build context with only a `Dockerfile` in it:

  ```plaintext
  .
  └── Dockerfile
  ```

  And a Dockerfile that mounts the current directory into the build container:

  ```dockerfile
  FROM alpine:latest
  WORKDIR /work
  RUN touch foo.txt
  RUN --mount=type=bind,target=. ls
  RUN ls
  ```

  The first `ls` command with the bind mount shows the contents of the mounted directory. The second `ls` lists the contents of the original build context.

  Build log

  ```plaintext
  #8 [stage-0 3/5] RUN touch foo.txt
  #8 DONE 0.1s

  #9 [stage-0 4/5] RUN --mount=target=. ls -1
  #9 0.040 Dockerfile
  #9 DONE 0.0s

  #10 [stage-0 5/5] RUN ls -1
  #10 0.046 foo.txt
  #10 DONE 0.1s
  ```

## [Use cache mounts](#use-cache-mounts)

Regular cache layers in Docker correspond to an exact match of the instruction and the files it depends on. If the instruction and the files it depends on have changed since the layer was built, the layer is invalidated, and the build process has to rebuild the layer.

Cache mounts are a way to specify a persistent cache location to be used during builds. The cache is cumulative across builds, so you can read and write to the cache multiple times. This persistent caching means that even if you need to rebuild a layer, you only download new or changed packages. Any unchanged packages are reused from the cache mount.

To use cache mounts in a build, you can use the `--mount` flag with the `RUN` instruction in your Dockerfile:

```dockerfile
FROM node:latest
WORKDIR /app
RUN --mount=type=cache,target=/root/.npm npm install
```

In this example, the `npm install` command uses a cache mount for the `/root/.npm` directory, the default location for the npm cache. The cache mount is persisted across builds, so even if you end up rebuilding the layer, you only download new or changed packages. Any changes to the cache are persisted across builds, and the cache is shared between multiple builds.

How you specify cache mounts depends on the build tool you're using. If you're unsure how to specify cache mounts, refer to the documentation for the build tool you're using. Here are a few examples:

```dockerfile
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    go build -o /app/hello
```

```dockerfile
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt-get --no-install-recommends install -y gcc
```

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

```dockerfile
RUN --mount=type=cache,target=/root/.gem \
    bundle install
```

```dockerfile
RUN --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/git/db \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    cargo build
```

```dockerfile
RUN --mount=type=cache,target=/root/.nuget/packages \
    dotnet restore
```

```dockerfile
RUN --mount=type=cache,target=/tmp/cache \
    composer install
```

It's important that you read the documentation for the build tool you're using to make sure you're using the correct cache mount options. Package managers have different requirements for how they use the cache, and using the wrong options can lead to unexpected behavior. For example, Apt needs exclusive access to its data, so the caches use the option `sharing=locked` to ensure parallel builds using the same cache mount wait for each other and not access the same cache files at the same time.

## [Use an external cache](#use-an-external-cache)

The default cache storage for builds is internal to the builder (BuildKit instance) you're using. Each builder uses its own cache storage. When you switch between different builders, the cache is not shared between them. Using an external cache lets you define a remote location for pushing and pulling cache data.

External caches are especially useful for CI/CD pipelines, where the builders are often ephemeral, and build minutes are precious. Reusing the cache between builds can drastically speed up the build process and reduce cost. You can even make use of the same cache in your local development environment.

To use an external cache, you specify the `--cache-to` and `--cache-from` options with the `docker buildx build` command.

* `--cache-to` exports the build cache to the specified location.
* `--cache-from` specifies remote caches for the build to use.

The following example shows how to set up a GitHub Actions workflow using `docker/build-push-action`, and push the build cache layers to an OCI registry image:

.github/workflows/ci.yml

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: user/app:latest
          cache-from: type=registry,ref=user/app:buildcache
          cache-to: type=registry,ref=user/app:buildcache,mode=max
```

This setup tells BuildKit to look for cache in the `user/app:buildcache` image. And when the build is done, the new build cache is pushed to the same image, overwriting the old cache.

This cache can be used locally as well. To pull the cache in a local build, you can use the `--cache-from` option with the `docker buildx build` command:

```console
$ docker buildx build --cache-from type=registry,ref=user/app:buildcache .
```

## [Summary](#summary)

Optimizing cache usage in builds can significantly speed up the build process. Keeping the build context small, using bind mounts, cache mounts, and external caches are all techniques you can use to make the most of the build cache and speed up the build process.

For more information about the concepts discussed in this guide, see:

* [.dockerignore files](https://docs.docker.com/build/concepts/context/#dockerignore-files)
* [Cache invalidation](https://docs.docker.com/build/cache/invalidation/)
* [Cache mounts](https://docs.docker.com/reference/dockerfile/#run---mounttypecache)
* [Cache backend types](https://docs.docker.com/build/cache/backends/)
* [Building best practices](https://docs.docker.com/build/building/best-practices/)

----
url: https://docs.docker.com/reference/samples/elasticsearch/
----

# Elasticsearch / Logstash / Kibana samples

| Name                                                                                                                     | Description                                         |
| ------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| [Elasticsearch / Logstash / Kibana](https://github.com/docker/awesome-compose/tree/master/elasticsearch-logstash-kibana) | A sample Elasticsearch, Logstash, and Kibana stack. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/build/builders/drivers/
----

# Build drivers

***

Table of contents

***

Build drivers are configurations for how and where the BuildKit backend runs. Driver settings are customizable and allow fine-grained control of the builder. Buildx supports the following drivers:

* `docker`: uses the BuildKit library bundled into the Docker daemon.
* `docker-container`: creates a dedicated BuildKit container using Docker.
* `kubernetes`: creates BuildKit pods in a Kubernetes cluster.
* `remote`: connects directly to a manually managed BuildKit daemon.

Different drivers support different use cases. The default `docker` driver prioritizes simplicity and ease of use. It has limited support for advanced features like caching and output formats, and isn't configurable. Other drivers provide more flexibility and are better at handling advanced scenarios.

The following table outlines some differences between drivers.

| Feature                      | `docker` | `docker-container` | `kubernetes` | `remote`           |
| ---------------------------- | -------- | ------------------ | ------------ | ------------------ |
| **Automatically load image** | ✅        |                    |              |                    |
| **Cache export**             | ✅\*      | ✅                  | ✅            | ✅                  |
| **Tarball output**           |          | ✅                  | ✅            | ✅                  |
| **Multi-arch images**        |          | ✅                  | ✅            | ✅                  |
| **BuildKit configuration**   |          | ✅                  | ✅            | Managed externally |

\* *The `docker` driver doesn't support all cache export options. See [Cache storage backends](https://docs.docker.com/build/cache/backends/) for more information.*

## [Loading to local image store](#loading-to-local-image-store)

Unlike when using the default `docker` driver, images built using other drivers aren't automatically loaded into the local image store. If you don't specify an output, the build result is exported to the build cache only.

To build an image using a non-default driver and load it to the image store, use the `--load` flag with the build command:

```console
$ docker buildx build --load -t <image> --builder=container .
...
=> exporting to oci image format                                                                                                      7.7s
=> => exporting layers                                                                                                                4.9s
=> => exporting manifest sha256:4e4ca161fa338be2c303445411900ebbc5fc086153a0b846ac12996960b479d3                                      0.0s
=> => exporting config sha256:adf3eec768a14b6e183a1010cb96d91155a82fd722a1091440c88f3747f1f53f                                        0.0s
=> => sending tarball                                                                                                                 2.8s
=> importing to docker
```

With this option, the image is available in the image store after the build finishes:

```console
$ docker image ls
REPOSITORY                       TAG               IMAGE ID       CREATED             SIZE
<image>                          latest            adf3eec768a1   2 minutes ago       197MB
```

### [Load by default](#load-by-default)

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

You can configure the custom build drivers to behave in a similar way to the default `docker` driver, and load images to the local image store by default. To do so, set the `default-load` driver option when creating the builder:

```console
$ docker buildx create --driver-opt default-load=true
```

Note that, just like with the `docker` driver, if you specify a different output format with `--output`, the result will not be loaded to the image store unless you also explicitly specify `--output type=docker` or use the `--load` flag.

## [What's next](#whats-next)

Read about each driver:

* [Docker driver](https://docs.docker.com/build/builders/drivers/docker/)
* [Docker container driver](https://docs.docker.com/build/builders/drivers/docker-container/)
* [Kubernetes driver](https://docs.docker.com/build/builders/drivers/kubernetes/)
* [Remote driver](https://docs.docker.com/build/builders/drivers/remote/)

----
url: https://docs.docker.com/guides/orchestration/
----

[Deployment and orchestration](https://docs.docker.com/guides/orchestration/)

Explore the essentials of container orchestration with Docker.

Deployment

10 minutes

[« Back to all guides](/guides/)

# Deployment and orchestration

***

Table of contents

***

Containerization provides an opportunity to move and scale applications to clouds and data centers. Containers effectively guarantee that those applications run the same way anywhere, allowing you to quickly and easily take advantage of all these environments. Additionally, as you scale your applications up, you need some tooling to help automate the maintenance of those applications, enable the replacement of failed containers automatically, and manage the roll-out of updates and reconfigurations of those containers during their lifecycle.

Tools to manage, scale, and maintain containerized applications are called orchestrators. Two of the most popular orchestration tools are Kubernetes and Docker Swarm. Docker Desktop provides development environments for both of these orchestrators.

The advanced modules teach you how to:

1. [Set up and use a Kubernetes environment on your development machine](https://docs.docker.com/guides/kube-deploy/)
2. [Set up and use a Swarm environment on your development machine](https://docs.docker.com/guides/swarm-deploy/)

## [Turn on Kubernetes](#turn-on-kubernetes)

Docker Desktop sets up Kubernetes for you quickly and easily. Follow the setup and validation instructions appropriate for your operating system:

### [Mac](#mac)

1. From the Docker Dashboard, navigate to **Settings**, and select the **Kubernetes** tab.

2. Select the checkbox labeled **Enable Kubernetes**, and select **Apply**. Docker Desktop automatically sets up Kubernetes for you. You'll know that Kubernetes has been successfully enabled when you see a green light beside 'Kubernetes *running*' in **Settings**.

3. To confirm that Kubernetes is up and running, create a text file called `pod.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: demo
   spec:
     containers:
       - name: testpod
         image: alpine:latest
         command: ["ping", "8.8.8.8"]
   ```

   This describes a pod with a single container, isolating a simple ping to 8.8.8.8.

4. In a terminal, navigate to where you created `pod.yaml` and create your pod:

   ```console
   $ kubectl apply -f pod.yaml
   ```

5. Check that your pod is up and running:

   ```console
   $ kubectl get pods
   ```

   You should see something like:

   ```shell
   NAME      READY     STATUS    RESTARTS   AGE
   demo      1/1       Running   0          4s
   ```

6. Check that you get the logs you'd expect for a ping process:

   ```console
   $ kubectl logs demo
   ```

   You should see the output of a healthy ping process:

   ```shell
   PING 8.8.8.8 (8.8.8.8): 56 data bytes
   64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
   64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
   64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
   ...
   ```

7. Finally, tear down your test pod:

   ```console
   $ kubectl delete -f pod.yaml
   ```

### [Windows](#windows)

1. From the Docker Dashboard, navigate to **Settings**, and select the **Kubernetes** tab.

2. Select the checkbox labeled **Enable Kubernetes**, and select **Apply**. Docker Desktop automatically sets up Kubernetes for you. You'll know that Kubernetes has been successfully enabled when you see a green light beside 'Kubernetes *running*' in the **Settings** menu.

3. To confirm that Kubernetes is up and running, create a text file called `pod.yaml` with the following content:

   ```yaml
   apiVersion: v1
   kind: Pod
   metadata:
     name: demo
   spec:
     containers:
       - name: testpod
         image: alpine:latest
         command: ["ping", "8.8.8.8"]
   ```

   This describes a pod with a single container, isolating a simple ping to 8.8.8.8.

4. In PowerShell, navigate to where you created `pod.yaml` and create your pod:

   ```console
   $ kubectl apply -f pod.yaml
   ```

5. Check that your pod is up and running:

   ```console
   $ kubectl get pods
   ```

   You should see something like:

   ```shell
   NAME      READY     STATUS    RESTARTS   AGE
   demo      1/1       Running   0          4s
   ```

6. Check that you get the logs you'd expect for a ping process:

   ```console
   $ kubectl logs demo
   ```

   You should see the output of a healthy ping process:

   ```shell
   PING 8.8.8.8 (8.8.8.8): 56 data bytes
   64 bytes from 8.8.8.8: seq=0 ttl=37 time=21.393 ms
   64 bytes from 8.8.8.8: seq=1 ttl=37 time=15.320 ms
   64 bytes from 8.8.8.8: seq=2 ttl=37 time=11.111 ms
   ...
   ```

7. Finally, tear down your test pod:

   ```console
   $ kubectl delete -f pod.yaml
   ```

## [Enable Docker Swarm](#enable-docker-swarm)

Docker Desktop runs primarily on Docker Engine, which has everything you need to run a Swarm built in. Follow the setup and validation instructions appropriate for your operating system:

### [Mac](#mac)

1. Open a terminal, and initialize Docker Swarm mode:

   ```console
   $ docker swarm init
   ```

   If all goes well, you should see a message similar to the following:

   ```shell
   Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377

   To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
   ```

2. Run a simple Docker service that uses an alpine-based filesystem, and isolates a ping to 8.8.8.8:

   ```console
   $ docker service create --name demo alpine:latest ping 8.8.8.8
   ```

3. Check that your service created one running container:

   ```console
   $ docker service ps demo
   ```

   You should see something like:

   ```shell
   ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
   463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
   ```

4. Check that you get the logs you'd expect for a ping process:

   ```console
   $ docker service logs demo
   ```

   You should see the output of a healthy ping process:

   ```shell
   demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
   ...
   ```

5. Finally, tear down your test service:

   ```console
   $ docker service rm demo
   ```

### [Windows](#windows)

1. Open a PowerShell, and initialize Docker Swarm mode:

   ```console
   $ docker swarm init
   ```

   If all goes well, you should see a message similar to the following:

   ```shell
   Swarm initialized: current node (tjjggogqpnpj2phbfbz8jd5oq) is now a manager.

   To add a worker to this swarm, run the following command:

       docker swarm join --token SWMTKN-1-3e0hh0jd5t4yjg209f4g5qpowbsczfahv2dea9a1ay2l8787cf-2h4ly330d0j917ocvzw30j5x9 192.168.65.3:2377

   To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.
   ```

2. Run a simple Docker service that uses an alpine-based filesystem, and isolates a ping to 8.8.8.8:

   ```console
   $ docker service create --name demo alpine:latest ping 8.8.8.8
   ```

3. Check that your service created one running container:

   ```console
   $ docker service ps demo
   ```

   You should see something like:

   ```shell
   ID                  NAME                IMAGE               NODE                DESIRED STATE       CURRENT STATE           ERROR               PORTS
   463j2s3y4b5o        demo.1              alpine:latest       docker-desktop      Running             Running 8 seconds ago
   ```

4. Check that you get the logs you'd expect for a ping process:

   ```console
   $ docker service logs demo
   ```

   You should see the output of a healthy ping process:

   ```shell
   demo.1.463j2s3y4b5o@docker-desktop    | PING 8.8.8.8 (8.8.8.8): 56 data bytes
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=0 ttl=37 time=13.005 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=1 ttl=37 time=13.847 ms
   demo.1.463j2s3y4b5o@docker-desktop    | 64 bytes from 8.8.8.8: seq=2 ttl=37 time=41.296 ms
   ...
   ```

5. Finally, tear down your test service:

   ```console
   $ docker service rm demo
   ```

## [Conclusion](#conclusion)

At this point, you've confirmed that you can run simple containerized workloads in Kubernetes and Swarm. The next step is to write a YAML file that describes how to run and manage these containers.

* [Deploy to Kubernetes](https://docs.docker.com/guides/kube-deploy/)
* [Deploy to Swarm](https://docs.docker.com/guides/swarm-deploy/)

## [CLI references](#cli-references)

Further documentation for all CLI commands used in this article are available here:

* [`kubectl apply`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#apply)
* [`kubectl get`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#get)
* [`kubectl logs`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#logs)
* [`kubectl delete`](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#delete)
* [`docker swarm init`](/reference/cli/docker/swarm/init/)
* [`docker service *`](/reference/cli/docker/service/)

----
url: https://docs.docker.com/reference/cli/docker/mcp/profile/server/remove/
----

# docker mcp profile server remove

***

| Description                                                               | Remove MCP servers from a profile                                                 |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Usage                                                                     | `docker mcp profile server remove <profile-id> --name <name1> --name <name2> ...` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp profile server rm`                                                    |

## [Description](#description)

Remove MCP servers from a profile by server name.

## [Options](#options)

| Option   | Default | Description                                             |
| -------- | ------- | ------------------------------------------------------- |
| `--name` |         | Server name to remove (can be specified multiple times) |

## [Examples](#examples)

# [Remove servers by name](#remove-servers-by-name)

docker mcp profile server remove dev-tools --name github --name slack

# [Remove a single server](#remove-a-single-server)

docker mcp profile server remove dev-tools --name github

----
url: https://docs.docker.com/reference/cli/sbx/cp/
----

# sbx cp

| Description | Copy files or directories between a sandbox and the host |
| ----------- | -------------------------------------------------------- |
| Usage       | `sbx cp [flags] SRC DST`                                 |

## [Description](#description)

Either SRC or DST must be a sandbox path, written as SANDBOX:PATH. The other must be a local path. Copying between two sandboxes is not supported.

When copying a directory, the directory itself is placed at the destination. If the destination path does not exist it is created; if it already exists as a directory, the source is placed inside it.

## [Options](#options)

| Option              | Default | Description                              |
| ------------------- | ------- | ---------------------------------------- |
| `-L, --follow-link` |         | Follow symbolic links in the source path |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Copy a file from host to sandbox
sbx cp ./config.json my-sandbox:/home/user/

# Copy a file from sandbox to host
sbx cp my-sandbox:/home/user/output.log ./

# Copy a directory
sbx cp ./src/ my-sandbox:/home/user/src
```

----
url: https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/run-tests/
----

# Run tests and next steps

***

Table of contents

***

## [Run the tests](#run-the-tests)

```console
$ ./mvnw test
```

Or with Gradle:

```console
$ ./gradlew test
```

You should see the WireMock Docker container start in the console output. It acts as the photo service, serving mock responses based on the configured expectations. All tests should pass.

## [Summary](#summary)

You built a Micronaut application that integrates with an external REST API using declarative HTTP clients, then tested that integration using WireMock and the Testcontainers WireMock module. Testing at the HTTP protocol level instead of mocking Java methods lets you catch serialization issues and simulate realistic failure scenarios.

> Tip
>
> Testcontainers WireMock modules are available for Go and Python as well.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Testcontainers WireMock module](https://testcontainers.com/modules/wiremock/)
* [WireMock documentation](https://wiremock.org/docs/)
* [Testcontainers JUnit 5 quickstart](https://java.testcontainers.org/quickstart/junit_5_quickstart/)
* [Testing REST API integrations in Spring Boot using WireMock](/guides/testcontainers-java-wiremock/)

----
url: https://docs.docker.com/reference/cli/docker/plugin/
----

# docker plugin

***

| Description | Manage plugins  |
| ----------- | --------------- |
| Usage       | `docker plugin` |

## [Description](#description)

Manage plugins.

## [Subcommands](#subcommands)

| Command                                                                                 | Description                                                                                                           |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| [`docker plugin create`](https://docs.docker.com/reference/cli/docker/plugin/create/)   | Create a plugin from a rootfs and configuration. Plugin data directory must contain config.json and rootfs directory. |
| [`docker plugin disable`](https://docs.docker.com/reference/cli/docker/plugin/disable/) | Disable a plugin                                                                                                      |
| [`docker plugin enable`](https://docs.docker.com/reference/cli/docker/plugin/enable/)   | Enable a plugin                                                                                                       |
| [`docker plugin inspect`](https://docs.docker.com/reference/cli/docker/plugin/inspect/) | Display detailed information on one or more plugins                                                                   |
| [`docker plugin install`](https://docs.docker.com/reference/cli/docker/plugin/install/) | Install a plugin                                                                                                      |
| [`docker plugin ls`](https://docs.docker.com/reference/cli/docker/plugin/ls/)           | List plugins                                                                                                          |
| [`docker plugin push`](https://docs.docker.com/reference/cli/docker/plugin/push/)       | Push a plugin to a registry                                                                                           |
| [`docker plugin rm`](https://docs.docker.com/reference/cli/docker/plugin/rm/)           | Remove one or more plugins                                                                                            |
| [`docker plugin set`](https://docs.docker.com/reference/cli/docker/plugin/set/)         | Change settings for a plugin                                                                                          |
| [`docker plugin upgrade`](https://docs.docker.com/reference/cli/docker/plugin/upgrade/) | Upgrade an existing plugin                                                                                            |

----
url: https://docs.docker.com/reference/cli/docker/scout/version/
----

# docker scout version

***

| Description | Show Docker Scout version information |
| ----------- | ------------------------------------- |
| Usage       | `docker scout version`                |

## [Description](#description)

Show Docker Scout version information

## [Examples](#examples)

```console
$ docker scout version

      ⢀⢀⢀             ⣀⣀⡤⣔⢖⣖⢽⢝
   ⡠⡢⡣⡣⡣⡣⡣⡣⡢⡀    ⢀⣠⢴⡲⣫⡺⣜⢞⢮⡳⡵⡹⡅
  ⡜⡜⡜⡜⡜⡜⠜⠈⠈        ⠁⠙⠮⣺⡪⡯⣺⡪⡯⣺
 ⢘⢜⢜⢜⢜⠜               ⠈⠪⡳⡵⣹⡪⠇
 ⠨⡪⡪⡪⠂    ⢀⡤⣖⢽⡹⣝⡝⣖⢤⡀    ⠘⢝⢮⡚       _____                 _
  ⠱⡱⠁    ⡴⡫⣞⢮⡳⣝⢮⡺⣪⡳⣝⢦    ⠘⡵⠁      / ____| Docker        | |
   ⠁    ⣸⢝⣕⢗⡵⣝⢮⡳⣝⢮⡺⣪⡳⣣    ⠁      | (___   ___ ___  _   _| |_
        ⣗⣝⢮⡳⣝⢮⡳⣝⢮⡳⣝⢮⢮⡳            \___ \ / __/ _ \| | | | __|
   ⢀    ⢱⡳⡵⣹⡪⡳⣝⢮⡳⣝⢮⡳⡣⡏    ⡀       ____) | (_| (_) | |_| | |_
  ⢀⢾⠄    ⠫⣞⢮⡺⣝⢮⡳⣝⢮⡳⣝⠝    ⢠⢣⢂     |_____/ \___\___/ \__,_|\__|
  ⡼⣕⢗⡄    ⠈⠓⠝⢮⡳⣝⠮⠳⠙     ⢠⢢⢣⢣
 ⢰⡫⡮⡳⣝⢦⡀              ⢀⢔⢕⢕⢕⢕⠅
 ⡯⣎⢯⡺⣪⡳⣝⢖⣄⣀        ⡀⡠⡢⡣⡣⡣⡣⡣⡃
⢸⢝⢮⡳⣝⢮⡺⣪⡳⠕⠗⠉⠁    ⠘⠜⡜⡜⡜⡜⡜⡜⠜⠈
⡯⡳⠳⠝⠊⠓⠉             ⠈⠈⠈⠈



version: v1.0.9 (go1.21.3 - darwin/arm64)
git commit: 8bf95bf60d084af341f70e8263342f71b0a3cd16
```

----
url: https://docs.docker.com/reference/cli/sbx/create/
----

# sbx create

| Description | Create a sandbox for an agent             |
| ----------- | ----------------------------------------- |
| Usage       | `sbx create [flags] AGENT PATH [PATH...]` |

## [Description](#description)

Create a sandbox with access to a host workspace for an agent.

Use "sbx run --name SANDBOX" to attach to the agent after creation.

## [Commands](#commands)

| Command                                                                                     | Description                       |
| ------------------------------------------------------------------------------------------- | --------------------------------- |
| [`sbx create claude`](https://docs.docker.com/reference/cli/sbx/create/claude/)             | Create a sandbox for claude       |
| [`sbx create codex`](https://docs.docker.com/reference/cli/sbx/create/codex/)               | Create a sandbox for codex        |
| [`sbx create copilot`](https://docs.docker.com/reference/cli/sbx/create/copilot/)           | Create a sandbox for copilot      |
| [`sbx create cursor`](https://docs.docker.com/reference/cli/sbx/create/cursor/)             | Create a sandbox for cursor       |
| [`sbx create docker-agent`](https://docs.docker.com/reference/cli/sbx/create/docker-agent/) | Create a sandbox for docker-agent |
| [`sbx create droid`](https://docs.docker.com/reference/cli/sbx/create/droid/)               | Create a sandbox for droid        |
| [`sbx create gemini`](https://docs.docker.com/reference/cli/sbx/create/gemini/)             | Create a sandbox for gemini       |
| [`sbx create kiro`](https://docs.docker.com/reference/cli/sbx/create/kiro/)                 | Create a sandbox for kiro         |
| [`sbx create opencode`](https://docs.docker.com/reference/cli/sbx/create/opencode/)         | Create a sandbox for opencode     |
| [`sbx create shell`](https://docs.docker.com/reference/cli/sbx/create/shell/)               | Create a sandbox for shell        |

## [Options](#options)

| Option           | Default | Description                                                                                                                                                                                                            |
| ---------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--clone`        |         | Run the agent on a private in-container clone of the host Git repository (mounted read-only) instead of bind-mounting the workspace; the agent's commits are accessible via the sandbox-\<name> git remote on the host |
| `--cpus`         | `0`     | Number of CPUs to allocate to the sandbox (0 = auto: N-1 host CPUs, min 1)                                                                                                                                             |
| `--kit`          |         | experimental Kit reference (directory, ZIP, or OCI). Can be specified multiple times                                                                                                                                   |
| `-m, --memory`   |         | Memory limit in binary units (e.g., 1024m, 8g). Default: 50% of host memory, max 32 GiB                                                                                                                                |
| `--name`         |         | Name for the sandbox (default: \<agent>-\<workdir>, letters, numbers, hyphens, periods, plus signs and minus signs only)                                                                                               |
| `-q, --quiet`    |         | Suppress verbose output                                                                                                                                                                                                |
| `-t, --template` |         | Container image to use for the sandbox (default: agent-specific image)                                                                                                                                                 |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Create a sandbox for Claude in the current directory
sbx create claude .

# Create a sandbox with a custom name
sbx create --name my-project claude /path/to/project

# Create with additional read-only workspaces
sbx create claude . /path/to/docs:ro

# Run the agent on an in-container clone of the host repo, wired back via a git-daemon
sbx create --clone claude .
```

----
url: https://docs.docker.com/guides/nextjs/containerize/
----

# Containerize a Next.js Application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Before you begin, make sure the following tools are installed and available on your system:

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
* You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

> Note
>
> New to Docker? Start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide to get familiar with key concepts like images, containers, and Dockerfiles.

***

## [Overview](#overview)

This guide walks you through containerizing a Next.js application with Docker. You'll learn how to create a production-ready Docker image using best practices that improve performance, security, scalability, and deployment efficiency.

By the end of this guide, you will:

* Containerize a Next.js application using Docker.
* Create and optimize a Dockerfile for production builds.
* Use multi-stage builds to minimize image size.
* Leverage Next.js standalone or export output for efficient containerization.
* Follow best practices for building secure and maintainable Docker images.

***

## [Get the sample application](#get-the-sample-application)

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the git repository:

```console
$ git clone https://github.com/kristiyan-velkov/docker-nextjs-sample
```

***

## [Build the Docker image](#build-the-docker-image)

Next.js has specific requirements for production deployments. This guide shows two approaches: `standalone` output (Node.js server) and `export` output (static files with Nginx).

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

### [Step 1: Configure Next.js and create the Dockerfile](#step-1-configure-nextjs-and-create-the-dockerfile)

Before creating a Dockerfile, choose a base image: the [Node.js Official Image](https://hub.docker.com/_/node) or a [Docker Hardened Image (DHI)](https://hub.docker.com/hardened-images/catalog) from the Hardened Image catalog. Choosing DHI gives you a production-ready, lightweight, and secure image. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

> Important
>
> This guide uses stable Node.js LTS image tags that are considered secure when the guide is written. Because new releases and security patches are published regularly, always review the [official Node.js Docker images](https://hub.docker.com/_/node) and select a secure, up-to-date version before building or deploying.

***

#### [1.1 Next.js with standalone output](#11-nextjs-with-standalone-output)

Standalone output (`output: "standalone"`) makes Next.js build a self-contained output that includes only the files and dependencies needed to run the application. A single `node server.js` can serve the app, which is ideal for Docker and supports server-side rendering, API routes, and incremental static regeneration. For details, see the [Next.js output configuration documentation](https://nextjs.org/docs/app/api-reference/config/next-config-js/output) (including the "standalone" option).

The container runs the Next.js server with Node.js on port 3000.

Configure Next.js — Open or create `next.config.ts` in your project root:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
};

export default nextConfig;
```

Choose either a Docker Hardened Image or the Docker Official Image, then create a `Dockerfile` using the content from the selected tab below.

Docker Hardened Images (DHIs) are available for Node.js in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/node). For more information, see the [DHI quickstart](/dhi/get-started/) guide.

1. Sign in to the DHI registry:

   ```console
   $ docker login dhi.io
   ```

2. Pull the Node.js DHI (check the catalog for available versions):

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. Create a file named `Dockerfile` with the following contents. The `FROM` instructions use `dhi.io/node:24-alpine3.22-dev`. Check the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog) for the latest versions and update the image tags as needed for security and compatibility.

   ```dockerfile
   # ============================================
   # Stage 1: Dependencies Installation Stage
   # ============================================

   # IMPORTANT: Docker Hardened Image (DHI) Version Maintenance
   # This Dockerfile uses dhi.io/node. Regularly validate and update to the latest DHI versions in the catalog for security and compatibility.

   FROM dhi.io/node:24-alpine3.22-dev AS dependencies

   # Set working directory
   WORKDIR /app

   # Copy package-related files first to leverage Docker's caching mechanism
   COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

   # Install project dependencies with frozen lockfile for reproducible builds
   RUN --mount=type=cache,target=/root/.npm \
       --mount=type=cache,target=/usr/local/share/.cache/yarn \
       --mount=type=cache,target=/root/.local/share/pnpm/store \
     if [ -f package-lock.json ]; then \
       npm ci --no-audit --no-fund; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn install --frozen-lockfile --production=false; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm install --frozen-lockfile; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # ============================================
   # Stage 2: Build Next.js application in standalone mode
   # ============================================

   FROM dhi.io/node:24-alpine3.22-dev AS builder

   # Set working directory
   WORKDIR /app

   # Copy project dependencies from dependencies stage
   COPY --from=dependencies /app/node_modules ./node_modules

   # Copy application source code
   COPY . .

   ENV NODE_ENV=production

   # Next.js collects completely anonymous telemetry data about general usage.
   # Learn more here: https://nextjs.org/telemetry
   # Uncomment the following line in case you want to disable telemetry during the build.
   # ENV NEXT_TELEMETRY_DISABLED=1

   # Build Next.js application
   # If you want to speed up Docker rebuilds, you can cache the build artifacts
   # by adding: --mount=type=cache,target=/app/.next/cache
   # This caches the .next/cache directory across builds, but it also prevents
   # .next/cache/fetch-cache from being included in the final image, meaning
   # cached fetch responses from the build won't be available at runtime.
   RUN if [ -f package-lock.json ]; then \
       npm run build; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn build; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm build; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # ============================================
   # Stage 3: Run Next.js application
   # ============================================

   FROM dhi.io/node:24-alpine3.22-dev AS runner

   # Set working directory
   WORKDIR /app

   # Set production environment variables
   ENV NODE_ENV=production
   ENV PORT=3000
   ENV HOSTNAME="0.0.0.0"

   # Next.js collects completely anonymous telemetry data about general usage.
   # Learn more here: https://nextjs.org/telemetry
   # Uncomment the following line in case you want to disable telemetry during the run time.
   # ENV NEXT_TELEMETRY_DISABLED=1

   # Copy production assets
   COPY --from=builder --chown=node:node /app/public ./public

   # Set the correct permission for prerender cache
   RUN mkdir .next
   RUN chown node:node .next

   # Automatically leverage output traces to reduce image size
   # https://nextjs.org/docs/advanced-features/output-file-tracing
   COPY --from=builder --chown=node:node /app/.next/standalone ./
   COPY --from=builder --chown=node:node /app/.next/static ./.next/static

   # If you want to persist the fetch cache generated during the build so that
   # cached responses are available immediately on startup, uncomment this line:
   # COPY --from=builder --chown=node:node /app/.next/cache ./.next/cache

   # Switch to non-root user for security best practices
   USER node

   # Expose port 3000 to allow HTTP traffic
   EXPOSE 3000

   # Start Next.js standalone server
   CMD ["node", "server.js"]
   ```

Create a file named `Dockerfile` with the following contents (uses `node`):

```dockerfile
  # ============================================
  # Stage 1: Dependencies Installation Stage
  # ============================================

  ARG NODE_VERSION=24.14.0-slim

  FROM node:${NODE_VERSION} AS dependencies

  # Set working directory
  WORKDIR /app

  # Copy package-related files first to leverage Docker's caching mechanism
  COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

  # Install project dependencies with frozen lockfile for reproducible builds
  RUN --mount=type=cache,target=/root/.npm \
      --mount=type=cache,target=/usr/local/share/.cache/yarn \
      --mount=type=cache,target=/root/.local/share/pnpm/store \
    if [ -f package-lock.json ]; then \
      npm ci --no-audit --no-fund; \
    elif [ -f yarn.lock ]; then \
      corepack enable yarn && yarn install --frozen-lockfile --production=false; \
    elif [ -f pnpm-lock.yaml ]; then \
      corepack enable pnpm && pnpm install --frozen-lockfile; \
    else \
      echo "No lockfile found." && exit 1; \
    fi

  # ============================================
  # Stage 2: Build Next.js application in standalone mode
  # ============================================

  FROM node:${NODE_VERSION} AS builder

  # Set working directory
  WORKDIR /app

  # Copy project dependencies from dependencies stage
  COPY --from=dependencies /app/node_modules ./node_modules

  # Copy application source code
  COPY . .

  ENV NODE_ENV=production

  # Next.js collects completely anonymous telemetry data about general usage.
  # Learn more here: https://nextjs.org/telemetry
  # Uncomment the following line in case you want to disable telemetry during the build.
  # ENV NEXT_TELEMETRY_DISABLED=1

  # Build Next.js application
  # If you want to speed up Docker rebuilds, you can cache the build artifacts
  # by adding: --mount=type=cache,target=/app/.next/cache
  # This caches the .next/cache directory across builds, but it also prevents
  # .next/cache/fetch-cache from being included in the final image, meaning
  # cached fetch responses from the build won't be available at runtime.
  RUN if [ -f package-lock.json ]; then \
      npm run build; \
    elif [ -f yarn.lock ]; then \
      corepack enable yarn && yarn build; \
    elif [ -f pnpm-lock.yaml ]; then \
      corepack enable pnpm && pnpm build; \
    else \
      echo "No lockfile found." && exit 1; \
    fi

  # ============================================
  # Stage 3: Run Next.js application
  # ============================================

  FROM node:${NODE_VERSION} AS runner

  # Set working directory
  WORKDIR /app

  # Set production environment variables
  ENV NODE_ENV=production
  ENV PORT=3000
  ENV HOSTNAME="0.0.0.0"

  # Next.js collects completely anonymous telemetry data about general usage.
  # Learn more here: https://nextjs.org/telemetry
  # Uncomment the following line in case you want to disable telemetry during the run time.
  # ENV NEXT_TELEMETRY_DISABLED=1

  # Copy production assets
  COPY --from=builder --chown=node:node /app/public ./public

  # Set the correct permission for prerender cache
  RUN mkdir .next
  RUN chown node:node .next

  # Automatically leverage output traces to reduce image size
  # https://nextjs.org/docs/advanced-features/output-file-tracing
  COPY --from=builder --chown=node:node /app/.next/standalone ./
  COPY --from=builder --chown=node:node /app/.next/static ./.next/static

  # If you want to persist the fetch cache generated during the build so that
  # cached responses are available immediately on startup, uncomment this line:
  # COPY --from=builder --chown=node:node /app/.next/cache ./.next/cache

  # Switch to non-root user for security best practices
  USER node

  # Expose port 3000 to allow HTTP traffic
  EXPOSE 3000

  # Start Next.js standalone server
  CMD ["node", "server.js"]
```

> Note
>
> This Dockerfile uses three stages: `dependencies`, `builder`, and `runner`. The final image runs `node server.js` and listens on port 3000.

***

#### [1.2 Next.js with export output](#12-nextjs-with-export-output)

Output export (`output: "export"`) makes Next.js build a fully static site at build time. It generates HTML, CSS, and JavaScript into an `out` directory that can be served by any static host or CDN—no Node.js server at runtime. Use this when you don't need server-side rendering or API routes. For details, see the [Next.js output configuration documentation](https://nextjs.org/docs/app/api-reference/config/next-config-js/output).

Configure Next.js — Open `next.config.ts` in your project root and add the following code:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
```

Choose either a Docker Hardened Image or the Docker Official Image, then create a `Dockerfile` using the content from the selected tab below.

Docker Hardened Images (DHIs) are available for Node.js and Nginx in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog). For more information, see the [DHI quickstart](/dhi/get-started/) guide.

1. Sign in to the DHI registry:

   ```console
   $ docker login dhi.io
   ```

2. Pull the Node.js DHI (check the catalog for available versions):

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

3. Pull the Nginx DHI (check the catalog for available versions):

   ```console
   $ docker pull dhi.io/nginx:1.28.0-alpine3.21-dev
   ```

4. Create a file named `Dockerfile` with the following contents. The `FROM` instructions use Docker Hardened Images: `dhi.io/node:24-alpine3.22-dev` and `dhi.io/nginx:1.28.0-alpine3.21-dev`. Check the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog) for the latest versions and update the image tags as needed for security and compatibility.

   ```dockerfile
   # ============================================
   # Stage 1: Dependencies Installation Stage
   # ============================================

   # IMPORTANT: Docker Hardened Image (DHI) Version Maintenance
   # This Dockerfile uses dhi.io/node and dhi.io/nginx. Regularly validate and update to the latest DHI versions in the catalog for security and compatibility.

   FROM dhi.io/node:24-alpine3.22-dev AS dependencies

   # Set the working directory
   WORKDIR /app

   # Copy package-related files first to leverage Docker's caching mechanism
   COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

   # Install project dependencies with frozen lockfile for reproducible builds
   RUN --mount=type=cache,target=/root/.npm \
       --mount=type=cache,target=/usr/local/share/.cache/yarn \
       --mount=type=cache,target=/root/.local/share/pnpm/store \
     if [ -f package-lock.json ]; then \
       npm ci --no-audit --no-fund; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn install --frozen-lockfile --production=false; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm install --frozen-lockfile; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # ============================================
   # Stage 2: Build Next.js Application
   # ============================================

   FROM dhi.io/node:24-alpine3.22-dev AS builder

   # Set the working directory
   WORKDIR /app

   # Copy project dependencies from dependencies stage
   COPY --from=dependencies /app/node_modules ./node_modules

   # Copy application source code
   COPY . .

   ENV NODE_ENV=production

   # Next.js collects completely anonymous telemetry data about general usage.
   # Learn more here: https://nextjs.org/telemetry
   # Uncomment the following line in case you want to disable telemetry during the build.
   # ENV NEXT_TELEMETRY_DISABLED=1

   # Build Next.js application
   RUN --mount=type=cache,target=/app/.next/cache \
     if [ -f package-lock.json ]; then \
       npm run build; \
     elif [ -f yarn.lock ]; then \
       corepack enable yarn && yarn build; \
     elif [ -f pnpm-lock.yaml ]; then \
       corepack enable pnpm && pnpm build; \
     else \
       echo "No lockfile found." && exit 1; \
     fi

   # =========================================
   # Stage 3: Serve Static Files with Nginx
   # =========================================

   FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

   # Set the working directory
   WORKDIR /app

   # Next.js collects completely anonymous telemetry data about general usage.
   # Learn more here: https://nextjs.org/telemetry
   # Uncomment the following line in case you want to disable telemetry during the run time.
   # ENV NEXT_TELEMETRY_DISABLED=1

   # Copy custom Nginx config
   COPY nginx.conf /etc/nginx/nginx.conf

   # Copy the static build output from the build stage to Nginx's default HTML serving directory
   COPY --chown=nginx:nginx --from=builder /app/out /usr/share/nginx/html

   # Non-root user for security best practices
   USER nginx

   # Expose port 8080 to allow HTTP traffic
   EXPOSE 8080

   # Start Nginx directly with custom config
   ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
   CMD ["-g", "daemon off;"]
   ```

Create a file named `Dockerfile` with the following contents (uses `node` and `nginxinc/nginx-unprivileged`):

```dockerfile
# ============================================
# Stage 1: Dependencies Installation Stage
# ============================================

ARG NODE_VERSION=24.14.0-slim
ARG NGINXINC_IMAGE_TAG=alpine3.22

FROM node:${NODE_VERSION} AS dependencies

# Set the working directory
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json yarn.lock* package-lock.json* pnpm-lock.yaml* .npmrc* ./

# Install project dependencies with frozen lockfile for reproducible builds
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=cache,target=/usr/local/share/.cache/yarn \
    --mount=type=cache,target=/root/.local/share/pnpm/store \
  if [ -f package-lock.json ]; then \
    npm ci --no-audit --no-fund; \
  elif [ -f yarn.lock ]; then \
    corepack enable yarn && yarn install --frozen-lockfile --production=false; \
  elif [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm install --frozen-lockfile; \
  else \
    echo "No lockfile found." && exit 1; \
  fi

# ============================================
# Stage 2: Build Next.js Application
# ============================================

FROM node:${NODE_VERSION} AS builder

# Set the working directory
WORKDIR /app

# Copy project dependencies from dependencies stage
COPY --from=dependencies /app/node_modules ./node_modules

# Copy application source code
COPY . .

ENV NODE_ENV=production

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the build.
# ENV NEXT_TELEMETRY_DISABLED=1

# Build Next.js application
RUN --mount=type=cache,target=/app/.next/cache \
  if [ -f package-lock.json ]; then \
    npm run build; \
  elif [ -f yarn.lock ]; then \
    corepack enable yarn && yarn build; \
  elif [ -f pnpm-lock.yaml ]; then \
    corepack enable pnpm && pnpm build; \
  else \
    echo "No lockfile found." && exit 1; \
  fi

# =========================================
# Stage 3: Serve Static Files with Nginx
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINXINC_IMAGE_TAG} AS runner

# Set the working directory
WORKDIR /app

# Next.js collects completely anonymous telemetry data about general usage.
# Learn more here: https://nextjs.org/telemetry
# Uncomment the following line in case you want to disable telemetry during the run time.
# ENV NEXT_TELEMETRY_DISABLED=1

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --from=builder /app/out /usr/share/nginx/html

# Non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> Note
>
> This guide uses [nginx-unprivileged](https://hub.docker.com/r/nginxinc/nginx-unprivileged) instead of the standard Nginx image to run as a non-root user, following security best practices.

1. Create `nginx.conf` (required for export output only) — Create a file named `nginx.conf` in the root of your project:

   ```nginx
   # Minimal Nginx config for static Next.js app
   worker_processes 1;

   # Store PID in /tmp (always writable)
   pid /tmp/nginx.pid;

   events {
       worker_connections 1024;
   }

   http {
       include       /etc/nginx/mime.types;
       default_type  application/octet-stream;

       # Disable logging to avoid permission issues
       access_log off;
       error_log  /dev/stderr;

       # Optimize static file serving
       sendfile        on;
       tcp_nopush      on;
       tcp_nodelay     on;
       keepalive_timeout  65;

       # Gzip compression
       gzip on;
       gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
       gzip_min_length 256;

       server {
           listen       8080;
           server_name  localhost;

           # Serve static files
           root /usr/share/nginx/html;
           index index.html;

           # Handle Next.js static export routing
           # See: https://nextjs.org/docs/app/guides/static-exports#deploying
           location / {
               try_files $uri $uri.html $uri/ =404;
           }

           # This is necessary when `trailingSlash: false` (default).
           # You can omit this when `trailingSlash: true` in next.config.
           # Handles nested routes like /blog/post -> /blog/post.html
           location ~ ^/(.+)/$ {
               rewrite ^/(.+)/$ /$1.html break;
           }

           # Serve Next.js static assets
           location ~ ^/_next/ {
               try_files $uri =404;
               expires 1y;
               add_header Cache-Control "public, immutable";
           }

           # Optional 404 handling
           error_page 404 /404.html;
           location = /404.html {
               internal;
           }
       }
   }
   ```

   > Note
   >
   > Export uses port 8080. For more details, see the [Next.js output configuration](https://nextjs.org/docs/app/api-reference/config/next-config-js/output) and [Nginx documentation](https://nginx.org/en/docs/).

### [Step 2: Create the compose.yaml file](#step-2-create-the-composeyaml-file)

Create a file named `compose.yaml` with the following contents:

compose.yaml

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 3000:3000
```

> Note
>
> If using export output (Nginx), change the port mapping to `8080:8080`.

### [Step 3: Create the .dockerignore file](#step-3-create-the-dockerignore-file)

The `.dockerignore` file tells Docker which files and folders to exclude when building the image.

> Note
>
> This helps:
>
> * Reduce image size
> * Speed up the build process
> * Prevent sensitive or unnecessary files (like `.env`, `.git`, or `node_modules`) from being added to the final image.
>
> To learn more, visit the [.dockerignore reference](https://docs.docker.com/reference/dockerfile/#dockerignore-file).

Create a file named `.dockerignore` with the following contents:

```dockerignore
# Dependencies (installed inside the image, never copy from host)
node_modules/
.pnp/
.pnp.js
.pnpm-store/

# Next.js build output (generated during the image build)
.next/
out/
dist/
build/
.vercel/

# Testing (not needed in the production image)
coverage/
.nyc_output/
__tests__/
__mocks__/
jest/
cypress/
playwright-report/
test-results/
.vitest/

# Environment files (avoid leaking secrets into the build context)
.env
.env*
.env.local
.env.development.local
.env.test.local
.env.production.local

# Debug and log files
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*
lerna-debug.log*
*.log

# IDE and editor files
.vscode/
.idea/
.cursor/
.cursorrules
.copilot/
*.swp
*.swo
*~

# Git
.git/
.gitignore
.gitattributes

# Docker files (reduce build context; not needed inside the image)
Dockerfile*
.dockerignore
docker-compose*.yml
compose*.yaml

# Documentation (not needed in the image)
*.md
docs/

# CI/CD (not needed in the image)
.github/
.gitlab-ci.yml
.travis.yml
.circleci/
Jenkinsfile

# TypeScript and build metadata
*.tsbuildinfo

# Cache and temporary directories
.cache/
.parcel-cache/
.eslintcache
.stylelintcache
.turbo/
.tmp/
.temp/

# Sensitive or dev-only config (optional; omit if your build needs these)
.pem
.editorconfig
.prettierrc*
.eslintrc*
.stylelintrc*
.babelrc*
*.iml

# OS-specific files
.DS_Store
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
Desktop.ini
```

### [Step 4: Build the Next.js application image](#step-4-build-the-nextjs-application-image)

With your custom configuration in place, you're now ready to build the Docker image. Use the Dockerfile you created in Step 1 (standalone or export).

The setup includes:

* Multi-stage builds for optimized image size
* Standalone: Node.js server on port 3000; Export: Nginx serving static files on port 8080
* Non-root user for enhanced security
* Proper file permissions and ownership

After completing the previous steps, your project directory should contain at least the following files (export also requires `nginx.conf`):

```text
├── docker-nextjs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── next.config.ts
```

Now that your Dockerfile is configured, you can build the Docker image for your Next.js application.

> Note
>
> The `docker build` command packages your application into an image using the instructions in the Dockerfile. It includes all necessary files from the current directory (called the [build context](/build/concepts/context/#what-is-a-build-context)).

Run the following command from the root of your project:

```console
$ docker build --tag nextjs-sample .
```

What this command does:

* Uses the Dockerfile in the current directory (.)
* Packages the application and its dependencies into a Docker image
* Tags the image as nextjs-sample so you can reference it later

### [Step 5: View local images](#step-5-view-local-images)

After building your Docker image, you can check which images are available on your local machine using either the Docker CLI or [Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/). Since you're already working in the terminal, let's use the Docker CLI.

To list all locally available Docker images, run the following command:

```console
$ docker images
```

Example Output:

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
nextjs-sample             latest            8c5fc80f098e   14 seconds ago   130MB
```

This output provides key details about your images:

* Repository – The name assigned to the image.
* Tag – A version label that helps identify different builds (e.g., latest).
* Image ID – A unique identifier for the image.
* Created – The timestamp indicating when the image was built.
* Size – The total disk space used by the image.

If the build was successful, you should see `nextjs-sample` image listed.

***

## [Run the containerized application](#run-the-containerized-application)

In the previous step, you created a Dockerfile for your Next.js application and built a Docker image using the docker build command. Now it's time to run that image in a container and verify that your application works as expected.

Run the following command in a terminal. Use the port that matches your setup: standalone uses port 3000, export uses port 8080.

```console
$ docker run -p 3000:3000 nextjs-sample
```

For export output, use port 8080 instead:

```console
$ docker run -p 8080:8080 nextjs-sample
```

Open a browser and view the application: <http://localhost:3000> for standalone or <http://localhost:8080> for export. You should see your Next.js web application.

Press `ctrl+c` in the terminal to stop your application.

### [Run the application in the background](#run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option and `--name` to give the container a name so you can stop it later:

```console
$ docker run -d -p 3000:3000 --name nextjs-app nextjs-sample
```

For export output, use port 8080:

```console
$ docker run -d -p 8080:8080 --name nextjs-app nextjs-sample
```

Open a browser and view the application: <http://localhost:3000> for standalone or <http://localhost:8080> for export. You should see your web application.

To confirm that the container is running, use the `docker ps` command:

```console
$ docker ps
```

This will list all active containers along with their ports, names, and status. Look for a container exposing port 3000 (standalone) or 8080 (export).

Example Output:

```shell
CONTAINER ID   IMAGE           COMMAND                  CREATED             STATUS             PORTS                    NAMES
f49b74736a9d   nextjs-sample   "node server.js"         About a minute ago   Up About a minute   0.0.0.0:3000->3000/tcp nextjs-app
```

To stop the application, run:

```console
$ docker stop nextjs-app
```

> Note
>
> For more information about running containers, see the [`docker run` CLI reference](/reference/cli/docker/container/run/) and the [`docker stop` CLI reference](/reference/cli/docker/container/stop/).

***

## [Summary](#summary)

In this guide, you learned how to containerize, build, and run a Next.js application using Docker. By following best practices, you created a secure, optimized, and production-ready setup.

What you accomplished:

* Configured Next.js for either standalone output (Node.js server) or export output (static files with Nginx).
* Added a multi-stage Dockerfile for your chosen approach: standalone (port 3000) or export (port 8080, with `nginx.conf`).
* Created a `.dockerignore` file to exclude unnecessary files and keep the image clean and efficient.
* Built your Docker image using `docker build`.
* Ran the container using `docker run` with the image name `nextjs-sample`, both in the foreground and in detached mode.
* Verified that the app was running by visiting <http://localhost:3000> (standalone) or <http://localhost:8080> (export).
* Learned how to stop the containerized application using `docker stop nextjs-app`.

You now have a fully containerized Next.js application, running in a Docker container, and ready for deployment across any environment with confidence and consistency.

***

## [Related resources](#related-resources)

Explore official references and best practices to sharpen your Docker workflow:

* [Multi-stage builds](/build/building/multi-stage/) – Learn how to separate build and runtime stages.
* [Best practices for writing Dockerfiles](/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
* [Build context in Docker](/build/concepts/context/) – Learn how context affects image builds.
* [Next.js output configuration](https://nextjs.org/docs/app/api-reference/config/next-config-js/output) – Learn about Next.js production optimization (standalone and export).
* [Next.js with Docker (standalone)](https://github.com/vercel/next.js/tree/canary/examples/with-docker) – Official Next.js example: standalone output with Node.js.
* [Next.js with Docker (export)](https://github.com/vercel/next.js/tree/canary/examples/with-docker-export-output) – Official Next.js example: static export with Nginx or serve.
* [`docker build` CLI reference](/reference/cli/docker/image/build/) – Build Docker images from a Dockerfile.
* [`docker images` CLI reference](/reference/cli/docker/image/ls/) – Manage and inspect local Docker images.
* [`docker run` CLI reference](/reference/cli/docker/container/run/) – Run a command in a new container.
* [`docker stop` CLI reference](/reference/cli/docker/container/stop/) – Stop one or more running containers.

***

## [Next steps](#next-steps)

With your Next.js application now containerized, you're ready to move on to the next step.

In the next section, you'll learn how to develop your application using Docker containers, enabling a consistent, isolated, and reproducible development environment across any machine.

[Use containers for Next.js development »](https://docs.docker.com/guides/nextjs/develop/)

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/faq/
----

# Enhanced Container Isolation FAQs

***

Table of contents

***

Subscription: Business

For: Administrators

This page answers common questions about Enhanced Container Isolation (ECI) that aren't covered in the main documentation.

## [Do I need to change the way I use Docker when ECI is switched on?](#do-i-need-to-change-the-way-i-use-docker-when-eci-is-switched-on)

No. ECI works automatically in the background by creating more secure containers. You can continue using all your existing Docker commands, workflows, and development tools without any changes.

## [Do all container workloads work well with ECI?](#do-all-container-workloads-work-well-with-eci)

Most container workloads run without issues when ECI is turned on. However, some advanced workloads that require specific kernel-level access may not work. For details about which workloads are affected, see [ECI limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

## [Why not just restrict usage of the `--privileged` flag?](#why-not-just-restrict-usage-of-the---privileged-flag)

Privileged containers serve legitimate purposes like Docker-in-Docker, Kubernetes-in-Docker, and accessing hardware devices. ECI provides a better solution by allowing these advanced workloads to run securely while preventing them from compromising the Docker Desktop VM.

## [Does ECI affect container performance?](#does-eci-affect-container-performance)

ECI has minimal impact on container performance. The only exception is containers that perform many `mount` and `umount` system calls, as these are inspected by the Sysbox runtime for security. Most development workloads see no noticeable performance difference.

## [Can I override the container runtime with ECI turned on?](#can-i-override-the-container-runtime-with-eci-turned-on)

No. When ECI is turned on, all containers use the Sysbox runtime regardless of any `--runtime` flags:

```console
$ docker run --runtime=runc alpine echo "test"
# This still uses sysbox-runc, not runc
```

The `--runtime` flag is ignored to prevent users from bypassing ECI security by running containers as true root in the Docker Desktop VM.

## [Does ECI protect containers created before turning it on?](#does-eci-protect-containers-created-before-turning-it-on)

No. ECI only protects containers created after it's turned on. Remove existing containers before turning on ECI:

```console
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -aq)
```

For more details, see [Enable Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/enable-eci/).

## [Which containers does ECI protect?](#which-containers-does-eci-protect)

ECI protection varies by container type and Docker Desktop version:

### [Always protected](#always-protected)

* Containers created with `docker run` and `docker create`
* Containers using the `docker-container` build driver
* Kubernetes with the Kind provisioner

### [Platform dependent](#platform-dependent)

* Docker Build: Protected in Docker Desktop for Mac, Linux, and Windows with Hyper-V backend

### [Not protected](#not-protected)

* Docker Extensions
* Docker Debug containers
* Kubernetes with Kubeadm provisioner

For complete details, see [ECI limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

## [Can I mount the Docker socket with ECI turned on?](#can-i-mount-the-docker-socket-with-eci-turned-on)

By default, no. ECI blocks Docker socket bind mounts for security. However, you can configure exceptions for trusted images like Testcontainers.

For configuration details, see [Configure Docker socket exceptions](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/).

## [What bind mounts does ECI restrict?](#what-bind-mounts-does-eci-restrict)

ECI restricts bind mounts of Docker Desktop VM directories but allows host directory mounts configured in Docker Desktop Settings.

----
url: https://docs.docker.com/reference/cli/docker/pass/plugins/1password/
----

# docker pass plugins 1password

***

| Description | Manage the 1Password SDK plugin. |
| ----------- | -------------------------------- |
| Usage       | `docker pass plugins 1password`  |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Manage the `1password-sdk` plugin, which resolves secret references against 1Password through the official 1Password SDK.

The plugin authenticates with a [service account token](https://developer.1password.com/docs/service-accounts/get-started/) scoped to the vaults you want to expose. The token is stored in the local OS keychain. Use the subcommands to install the token (and enable the plugin) or to remove it (and disable the plugin).

Items reachable through this plugin are matched under any of:

* the raw 1Password item ID,
* `<vault-id>/<title>`,
* `<vault-name>/<title>`,
* a native 1Password secret-reference path (`<vault>/<item>/<field>` or `<vault>/<item>/<section>/<field>`), resolved directly via the SDK as if prefixed with `op://`.

Matching for the title-based forms follows 1Password's normalization rules and is case-insensitive, so existing `op://` references can be reused as-is.

## [Examples](#examples)

Install the service account token and enable the plugin:

```sh
echo "$OP_SERVICE_ACCOUNT_TOKEN" | docker pass plugins 1password setup
```

Remove the token and disable the plugin:

```sh
docker pass plugins 1password purge
```

## [Subcommands](#subcommands)

| Command                                                                                                             | Description                                                               |
| ------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| [`docker pass plugins 1password purge`](https://docs.docker.com/reference/cli/docker/pass/plugins/1password/purge/) | Disable the plugin and remove the stored 1Password service account token. |
| [`docker pass plugins 1password setup`](https://docs.docker.com/reference/cli/docker/pass/plugins/1password/setup/) | Set the 1Password service account token and enable the plugin.            |

----
url: https://docs.docker.com/build/policies/built-ins/
----

# Built-in functions

***

Table of contents

***

Buildx provides built-in functions, in addition to the [Rego built-ins](#rego-built-in-functions), to extend Rego policies with Docker-specific operations like loading local files, verifying Git signatures, and pinning image digests.

## [Rego built-in functions](#rego-built-in-functions)

The functions [documented on this page](#buildx-built-in-functions) are Buildx-specific functions, distinct from [Rego's standard built-in functions](https://www.openpolicyagent.org/docs/policy-language#built-in-functions)

Buildx also supports standard Rego built-in functions, but only a subset. To see the exact list of supported functions, refer to the Buildx [source code](https://github.com/docker/buildx/blob/master/policy/builtins.go).

## [Buildx built-in functions](#buildx-built-in-functions)

Buildx provides the following custom built-in functions for policy development:

* [`print`](#print)
* [`load_json`](#load_json)
* [`verify_git_signature`](#verify_git_signature)
* [`pin_image`](#pin_image)

### [`print`](#print)

Outputs debug information during policy evaluation.

Parameters:

* Any number of values to print

Returns: The values (pass-through)

Example:

```rego
allow if {
    input.image.repo == "alpine"
    print("Allowing alpine image:", input.image.tag)
}
```

Debug output appears when building with `--progress=plain`.

### [`load_json`](#load_json)

Loads and parses JSON data from local files in the build context.

Parameters:

* `filename` (string) - Path to JSON file relative to policy directory

Returns: Parsed JSON data as Rego value

Example:

```rego
# Load approved versions from external file
approved_versions = load_json("versions.json")

allow if {
    input.image.repo == "alpine"
    some version in approved_versions.alpine
    input.image.tag == version
}
```

File structure:

```text
project/
├── Dockerfile
├── Dockerfile.rego
└── versions.json
```

versions.json:

```json
{
  "alpine": ["3.19", "3.20"],
  "golang": ["1.21", "1.22"]
}
```

The JSON file must be in the same directory as the policy or in a subdirectory accessible from the policy location.

### [`verify_git_signature`](#verify_git_signature)

Verifies PGP signatures on Git commits or tags.

Parameters:

* `git_object` (object) - Either `input.git.commit` or `input.git.tag`
* `keyfile` (string) - Path to PGP public key file (relative to policy directory)

Returns: Boolean - `true` if signature is valid, `false` otherwise

Example:

```rego
# Require signed Git tags
allow if {
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "maintainer.asc")
}

# Require signed commits
allow if {
    input.git.commit
    verify_git_signature(input.git.commit, "keys/team.asc")
}
```

Directory structure:

```text
project/
├── Dockerfile.rego
└── maintainer.asc          # PGP public key
```

Or with subdirectory:

```text
project/
├── Dockerfile.rego
└── keys/
    ├── maintainer.asc
    └── team.asc
```

Obtaining public keys:

```console
$ gpg --export --armor user@example.com > maintainer.asc
```

### [`pin_image`](#pin_image)

Pins an image to a specific digest, overriding the tag-based reference. Use this to force builds to use specific image versions.

Parameters:

* `image_object` (object) - Must be `input.image` (the current image being evaluated)
* `digest` (string) - Target digest in format `sha256:...`

Returns: Boolean - `true` if pinning succeeds

Example:

```rego
# Pin alpine 3.19 to specific digest
alpine_3_19_digest = "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412"

allow if {
    input.image.repo == "alpine"
    input.image.tag == "3.19"
    pin_image(input.image, alpine_3_19_digest)
}
```

Automatic digest replacement:

```rego
# Replace old digests with patched versions
replace_map = {
  "3.22.0": "3.22.2",
  "3.22.1": "3.22.2",
}

alpine_digests = {
  "3.22.0": "sha256:8a1f59ffb675680d47db6337b49d22281a139e9d709335b492be023728e11715",
  "3.22.2": "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412",
}

allow if {
    input.image.repo == "alpine"
    some old_version, new_version in replace_map
    input.image.checksum == alpine_digests[old_version]
    print("Replacing", old_version, "with", new_version)
    pin_image(input.image, alpine_digests[new_version])
}
```

This pattern automatically upgrades old image versions to patched releases.

## [Next steps](#next-steps)

* Browse complete examples: [Example policies](https://docs.docker.com/build/policies/examples/)
* Learn policy development workflow: [Using build policies](https://docs.docker.com/build/policies/usage/)
* Reference input fields: [Input reference](https://docs.docker.com/build/policies/inputs/)

----
url: https://docs.docker.com/enterprise/security/single-sign-on/faqs/general/
----

# General SSO FAQs

***

Table of contents

***

## [What SSO flows does Docker support?](#what-sso-flows-does-docker-support)

Docker supports Service Provider Initiated (SP-initiated) SSO flow. Users must sign in to Docker Hub or Docker Desktop to initiate the SSO authentication process.

## [Does Docker SSO support multi-factor authentication?](#does-docker-sso-support-multi-factor-authentication)

When an organization uses SSO, multi-factor authentication is controlled at the identity provider level, not on the Docker platform.

## [Can I retain my Docker ID when using SSO?](#can-i-retain-my-docker-id-when-using-sso)

Users with personal Docker IDs retain ownership of their repositories, images, and assets. When SSO is enforced, existing accounts with company domain emails are connected to the organization. Users signing in without existing accounts automatically have new accounts and Docker IDs created.

## [Are there any firewall rules required for SSO configuration?](#are-there-any-firewall-rules-required-for-sso-configuration)

No specific firewall rules are required as long as `login.docker.com` is accessible. This domain is commonly accessible by default, but some organizations may need to allow it in their firewall settings if SSO setup encounters issues.

## [Does Docker use my IdP's default session timeout?](#does-docker-use-my-idps-default-session-timeout)

Yes, Docker supports your IdP's session timeout using a custom `dockerSessionMinutes` SAML attribute instead of the standard `SessionNotOnOrAfter` element. See [SSO attributes](https://docs.docker.com/enterprise/security/provisioning/#sso-attributes) for more information.

----
url: https://docs.docker.com/engine/logging/drivers/awslogs/
----

# Amazon CloudWatch Logs logging driver

***

Table of contents

***

The `awslogs` logging driver sends container logs to [Amazon CloudWatch Logs](https://aws.amazon.com/cloudwatch/details/#log-monitoring). Log entries can be retrieved through the [AWS Management Console](https://console.aws.amazon.com/cloudwatch/home#logs:) or the [AWS SDKs and Command Line Tools](https://docs.aws.amazon.com/cli/latest/reference/logs/index.html).

## [Usage](#usage)

To use the `awslogs` driver as the default logging driver, set the `log-driver` and `log-opt` keys to appropriate values in the `daemon.json` file. For more about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

The following example sets the log driver to `awslogs` and sets the `awslogs-region` option.

```json
{
  "log-driver": "awslogs",
  "log-opts": {
    "awslogs-region": "us-east-1"
  }
}
```

Restart Docker for the changes to take effect.

You can set the logging driver for a specific container by using the `--log-driver` option to `docker run`:

```console
$ docker run --log-driver=awslogs ...
```

If you are using Docker Compose, set `awslogs` using the following declaration example:

```yaml
myservice:
  logging:
    driver: awslogs
    options:
      awslogs-region: us-east-1
```

## [Amazon CloudWatch Logs options](#amazon-cloudwatch-logs-options)

You can add logging options to the `daemon.json` to set Docker-wide defaults, or use the `--log-opt NAME=VALUE` flag to specify Amazon CloudWatch Logs logging driver options when starting a container.

### [awslogs-region](#awslogs-region)

The `awslogs` logging driver sends your Docker logs to a specific region. Use the `awslogs-region` log option or the `AWS_REGION` environment variable to set the region. By default, if your Docker daemon is running on an EC2 instance and no region is set, the driver uses the instance's region.

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 ...
```

### [awslogs-endpoint](#awslogs-endpoint)

By default, Docker uses either the `awslogs-region` log option or the detected region to construct the remote CloudWatch Logs API endpoint. Use the `awslogs-endpoint` log option to override the default endpoint with the provided endpoint.

> Note
>
> The `awslogs-region` log option or detected region controls the region used for signing. You may experience signature errors if the endpoint you've specified with `awslogs-endpoint` uses a different region.

### [awslogs-group](#awslogs-group)

You must specify a [log group](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) for the `awslogs` logging driver. You can specify the log group with the `awslogs-group` log option:

```console
$ docker run --log-driver=awslogs --log-opt awslogs-region=us-east-1 --log-opt awslogs-group=myLogGroup ...
```

### [awslogs-stream](#awslogs-stream)

To configure which [log stream](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html) should be used, you can specify the `awslogs-stream` log option. If not specified, the container ID is used as the log stream.

> Note
>
> Log streams within a given log group should only be used by one container at a time. Using the same log stream for multiple containers concurrently can cause reduced logging performance.

### [awslogs-create-group](#awslogs-create-group)

Log driver returns an error by default if the log group doesn't exist. However, you can set the `awslogs-create-group` to `true` to automatically create the log group as needed. The `awslogs-create-group` option defaults to `false`.

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-create-group=true \
    ...
```

> Note
>
> Your AWS IAM policy must include the `logs:CreateLogGroup` permission before you attempt to use `awslogs-create-group`.

### [awslogs-create-stream](#awslogs-create-stream)

By default, the log driver creates the AWS CloudWatch Logs stream used for container log persistence.

Set `awslogs-create-stream` to `false` to disable log stream creation. When disabled, the Docker daemon assumes the log stream already exists. A use case where this is beneficial is when log stream creation is handled by another process avoiding redundant AWS CloudWatch Logs API calls.

If `awslogs-create-stream` is set to `false` and the log stream does not exist, log persistence to CloudWatch fails during container runtime, resulting in `Failed to put log events` error messages in daemon logs.

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-stream=myLogStream \
    --log-opt awslogs-create-stream=false \
    ...
```

### [awslogs-datetime-format](#awslogs-datetime-format)

The `awslogs-datetime-format` option defines a multi-line start pattern in [Python `strftime` format](https://strftime.org). A log message consists of a line that matches the pattern and any following lines that don't match the pattern. Thus the matched line is the delimiter between log messages.

One example of a use case for using this format is for parsing output such as a stack dump, which might otherwise be logged in multiple entries. The correct pattern allows it to be captured in a single entry.

This option always takes precedence if both `awslogs-datetime-format` and `awslogs-multiline-pattern` are configured.

> Note
>
> Multi-line logging performs regular expression parsing and matching of all log messages, which may have a negative impact on logging performance.

Consider the following log stream, where new log messages start with a timestamp:

```console
[May 01, 2017 19:00:01] A message was logged
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words
[May 01, 2017 19:01:32] Another message was logged
```

The format can be expressed as a `strftime` expression of `[%b %d, %Y %H:%M:%S]`, and the `awslogs-datetime-format` value can be set to that expression:

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-datetime-format='\[%b %d, %Y %H:%M:%S\]' \
    ...
```

This parses the logs into the following CloudWatch log events:

```console
# First event
[May 01, 2017 19:00:01] A message was logged

# Second event
[May 01, 2017 19:00:04] Another multi-line message was logged
Some random message
with some random words

# Third event
[May 01, 2017 19:01:32] Another message was logged
```

The following `strftime` codes are supported:

| Code | Meaning                                                          | Example  |
| ---- | ---------------------------------------------------------------- | -------- |
| `%a` | Weekday abbreviated name.                                        | Mon      |
| `%A` | Weekday full name.                                               | Monday   |
| `%w` | Weekday as a decimal number where 0 is Sunday and 6 is Saturday. | 0        |
| `%d` | Day of the month as a zero-padded decimal number.                | 08       |
| `%b` | Month abbreviated name.                                          | Feb      |
| `%B` | Month full name.                                                 | February |
| `%m` | Month as a zero-padded decimal number.                           | 02       |
| `%Y` | Year with century as a decimal number.                           | 2008     |
| `%y` | Year without century as a zero-padded decimal number.            | 08       |
| `%H` | Hour (24-hour clock) as a zero-padded decimal number.            | 19       |
| `%I` | Hour (12-hour clock) as a zero-padded decimal number.            | 07       |
| `%p` | AM or PM.                                                        | AM       |
| `%M` | Minute as a zero-padded decimal number.                          | 57       |
| `%S` | Second as a zero-padded decimal number.                          | 04       |
| `%f` | Microseconds as a zero-padded decimal number.                    | 000345   |
| `%z` | UTC offset in the form +HHMM or -HHMM.                           | +1300    |
| `%Z` | Time zone name.                                                  | PST      |
| `%j` | Day of the year as a zero-padded decimal number.                 | 363      |

In addition, the following non-`strftime` codes are supported:

| Code | Meaning                                                              | Example |
| ---- | -------------------------------------------------------------------- | ------- |
| `%L` | Milliseconds as a zero-padded decimal number preceded with a period. | .123    |

### [awslogs-multiline-pattern](#awslogs-multiline-pattern)

The `awslogs-multiline-pattern` option defines a multi-line start pattern using a regular expression. A log message consists of a line that matches the pattern and any following lines that don't match the pattern. Thus the matched line is the delimiter between log messages.

This option is ignored if `awslogs-datetime-format` is also configured.

> Note
>
> Multi-line logging performs regular expression parsing and matching of all log messages. This may have a negative impact on logging performance.

Consider the following log stream, where each log message should start with the pattern `INFO`:

```console
INFO A message was logged
INFO Another multi-line message was logged
     Some random message
INFO Another message was logged
```

You can use the regular expression of `^INFO`:

```console
$ docker run \
    --log-driver=awslogs \
    --log-opt awslogs-region=us-east-1 \
    --log-opt awslogs-group=myLogGroup \
    --log-opt awslogs-multiline-pattern='^INFO' \
    ...
```

This parses the logs into the following CloudWatch log events:

```console
# First event
INFO A message was logged

# Second event
INFO Another multi-line message was logged
     Some random message

# Third event
INFO Another message was logged
```

### [tag](#tag)

Specify `tag` as an alternative to the `awslogs-stream` option. `tag` interprets Go template markup, such as `{{.ID}}`, `{{.FullID}}` or `{{.Name}}` `docker.{{.ID}}`. See the [tag option documentation](https://docs.docker.com/engine/logging/log_tags/) for details on supported template substitutions.

When both `awslogs-stream` and `tag` are specified, the value supplied for `awslogs-stream` overrides the template specified with `tag`.

If not specified, the container ID is used as the log stream.

> Note
>
> The CloudWatch log API doesn't support `:` in the log name. This can cause some issues when using the `{{ .ImageName }}` as a tag, since a Docker image has a format of `IMAGE:TAG`, such as `alpine:latest`. Template markup can be used to get the proper format. To get the image name and the first 12 characters of the container ID, you can use:
>
> ```bash
> --log-opt tag='{{ with split .ImageName ":" }}{{join . "_"}}{{end}}-{{.ID}}'
> ```
>
> the output is something like: `alpine_latest-bf0072049c76`

### [awslogs-force-flush-interval-seconds](#awslogs-force-flush-interval-seconds)

The `awslogs` driver periodically flushes logs to CloudWatch.

The `awslogs-force-flush-interval-seconds` option changes log flush interval seconds.

Default is 5 seconds.

### [awslogs-max-buffered-events](#awslogs-max-buffered-events)

The `awslogs` driver buffers logs.

The `awslogs-max-buffered-events` option changes log buffer size.

Default is 4K.

## [Credentials](#credentials)

You must provide AWS credentials to the Docker daemon to use the `awslogs` logging driver. You can provide these credentials with the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` environment variables, the default AWS shared credentials file (`~/.aws/credentials` of the root user), or if you are running the Docker daemon on an Amazon EC2 instance, the Amazon EC2 instance profile.

> Note
>
> Docker reads AWS credentials when the container starts. If you use a shared AWS credentials file with temporary credentials, updating the file later does not automatically update the credentials used by the running container. When the temporary credentials expire, log delivery to Amazon CloudWatch Logs can fail. Restart the container after refreshing the credentials so Docker can load the updated values.

Credentials must have a policy applied that allows the `logs:CreateLogStream` and `logs:PutLogEvents` actions, as shown in the following example.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
      "Effect": "Allow",
      "Resource": "*"
    }
  ]
}
```

----
url: https://docs.docker.com/enterprise/security/provisioning/just-in-time/
----

# Just-in-Time provisioning

***

Table of contents

***

Subscription: Business

For: Administrators

Just-in-Time (JIT) provisioning streamlines user onboarding by automatically creating and updating user accounts during SSO authentication. This eliminates manual account creation and ensures users have immediate access to your organization's resources. JIT verifies that users belong to the organization and assigns them to the appropriate teams based on your identity provider (IdP) configuration. When you create your SSO connection, JIT provisioning is turned on by default.

This page explains how JIT provisioning works, SSO authentication flows, and how to disable JIT provisioning.

## [Prerequisites](#prerequisites)

Before you begin, you must have:

* SSO configured for your organization
* Administrator access to Docker Home and your identity provider

## [SSO authentication with JIT provisioning enabled](#sso-authentication-with-jit-provisioning-enabled)

When a user signs in with SSO and you have JIT provisioning enabled, the following steps occur automatically:

1. The system checks if a Docker account exists for the user's email address.

   * If an account exists: The system uses the existing account and updates the user's full name if necessary.
   * If no account exists: A new Docker account is created using basic user attributes (email, name, and surname). A unique username is generated based on the user's email, name, and random numbers to ensure all usernames are unique across the platform.

2. The system checks for any pending invitations to the SSO organization.

   * Invitation found: The invitation is automatically accepted.
   * Invitation includes a specific group: The user is added to that group within the SSO organization.

3. The system verifies if the IdP has shared group mappings during authentication.

   * Group mappings provided: The user is assigned to the relevant organizations and teams.
   * No group mappings provided: The system checks if the user is already part of the organization. If not, the user is added to the default organization and team configured in the SSO connection.

The following graphic provides an overview of SSO authentication with JIT enabled:

## [SSO authentication with JIT provisioning disabled](#sso-authentication-with-jit-provisioning-disabled)

When JIT provisioning is disabled, the following actions occur during SSO authentication:

1. The system checks if a Docker account exists for the user's email address.

   * If an account exists: The system uses the existing account and updates the user's full name if necessary.
   * If no account exists: A new Docker account is created using basic user attributes (email, name, and surname). A unique username is generated based on the user's email, name, and random numbers to ensure all usernames are unique across the platform.

2. The system checks for any pending invitations to the SSO organization.

   * Invitation found: If the user is a member of the organization or has a pending invitation, sign-in is successful, and the invitation is automatically accepted.
   * No invitation found: If the user is not a member of the organization and has no pending invitation, the sign-in fails, and an `Access denied` error appears. The user must contact an administrator to be invited to the organization.

With JIT disabled, group mapping is only available if you have [SCIM enabled](https://docs.docker.com/enterprise/security/provisioning/scim/#enable-scim-in-docker). If SCIM is not enabled, users won't be auto-provisioned to groups.

The following graphic provides an overview of SSO authentication with JIT disabled:

## [Disable JIT provisioning](#disable-jit-provisioning)

> Warning
>
> Disabling JIT provisioning may disrupt your users' access and workflows. With JIT disabled, users will not be automatically added to your organization. Users must already be a member of the organization or have a pending invitation to successfully sign in through SSO. To auto-provision users with JIT disabled, [use SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/).

You may want to disable JIT provisioning for reasons such as the following:

* You have multiple organizations, have SCIM enabled, and want SCIM to be the source of truth for provisioning
* You want to control and restrict usage based on your organization's security configuration, and want to use SCIM to provision access

Users are provisioned with JIT by default. If you enable SCIM, you can disable JIT:

1. Go to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the **SSO connections** table, select the **Action** icon, then select **Disable JIT provisioning**.
4. Select **Disable** to confirm.

## [Next steps](#next-steps)

* Configure [SCIM provisioning](https://docs.docker.com/enterprise/security/provisioning/scim/) for advanced user management.
* Set up [group mapping](https://docs.docker.com/enterprise/security/provisioning/scim/group-mapping/) to automatically assign users to teams.
* Review [Troubleshoot provisioning](https://docs.docker.com/enterprise/security/provisioning/troubleshoot-provisioning/).

----
url: https://docs.docker.com/engine/release-notes/17.10/
----

# Docker Engine 17.10 release notes

***

Table of contents

***

## [17.10.0-ce](#17100-ce)

2017-10-17

> Important
>
> `docker service scale` and `docker service rollback` use non-detached mode as default, use `--detach` to keep the old behaviour.

### [Builder](#builder)

* Reset uid/gid to 0 in uploaded build context to share build cache with other clients [docker/cli#513](https://github.com/docker/cli/pull/513)

- Add support for `ADD` urls without any sub path [moby/moby#34217](https://github.com/moby/moby/pull/34217)

### [Client](#client)

* Move output of `docker stack rm` to stdout [docker/cli#491](https://github.com/docker/cli/pull/491)
* Use natural sort for secrets and configs in cli [docker/cli#307](https://github.com/docker/cli/pull/307)
* Use non-detached mode as default for `docker service` commands [docker/cli#525](https://github.com/docker/cli/pull/525)
* Set APIVersion on the client, even when Ping fails [docker/cli#546](https://github.com/docker/cli/pull/546)

- Fix loader error with different build syntax in `docker stack deploy` [docker/cli#544](https://github.com/docker/cli/pull/544)

* Change the default output format for `docker container stats` to show `CONTAINER ID` and `NAME` [docker/cli#565](https://github.com/docker/cli/pull/565)

- Add `--no-trunc` flag to `docker container stats` [docker/cli#565](https://github.com/docker/cli/pull/565)
- Add experimental `docker trust`: `view`, `revoke`, `sign` subcommands [docker/cli#472](https://github.com/docker/cli/pull/472)

* Various doc and shell completion fixes [docker/cli#610](https://github.com/docker/cli/pull/610) [docker/cli#611](https://github.com/docker/cli/pull/611) [docker/cli#618](https://github.com/docker/cli/pull/618) [docker/cli#580](https://github.com/docker/cli/pull/580) [docker/cli#598](https://github.com/docker/cli/pull/598) [docker/cli#603](https://github.com/docker/cli/pull/603)

### [Networking](#networking)

* Enabling ILB/ELB on windows using per-node, per-network LB endpoint [moby/moby#34674](https://github.com/moby/moby/pull/34674)
* Overlay fix for transient IP reuse [docker/libnetwork#1935](https://github.com/docker/libnetwork/pull/1935)
* Serializing bitseq alloc [docker/libnetwork#1788](https://github.com/docker/libnetwork/pull/1788)

- Disable hostname lookup on chain exists check [docker/libnetwork#1974](https://github.com/docker/libnetwork/pull/1974)

### [Runtime](#runtime)

* LCOW: Add UVM debuggability by grabbing logs before tear-down [moby/moby#34846](https://github.com/moby/moby/pull/34846)
* LCOW: Prepare work for bind mounts [moby/moby#34258](https://github.com/moby/moby/pull/34258)
* LCOW: Support for docker cp, ADD/COPY on build [moby/moby#34252](https://github.com/moby/moby/pull/34252)
* LCOW: VHDX boot to readonly [moby/moby#34754](https://github.com/moby/moby/pull/34754)
* Volume: evaluate symlinks before relabeling mount source [moby/moby#34792](https://github.com/moby/moby/pull/34792)

- Fixing ‘docker cp’ to allow new target file name in a host symlinked directory [moby/moby#31993](https://github.com/moby/moby/pull/31993)

* Add support for Windows version filtering on pull [moby/moby#35090](https://github.com/moby/moby/pull/35090)

### [Swarm mode](#swarm-mode)

* Produce an error if `docker swarm init --force-new-cluster` is executed on worker nodes [moby/moby#34881](https://github.com/moby/moby/pull/34881)

- Add support for `.Node.Hostname` templating in swarm services [moby/moby#34686](https://github.com/moby/moby/pull/34686)

* Increase gRPC request timeout to 20 seconds for sending snapshots [docker/swarmkit#2391](https://github.com/docker/swarmkit/pull/2391)

- Do not filter nodes if logdriver is set to `none` [docker/swarmkit#2396](https://github.com/docker/swarmkit/pull/2396)

* Adding ipam options to ipam driver requests [docker/swarmkit#2324](https://github.com/docker/swarmkit/pull/2324)

----
url: https://docs.docker.com/reference/cli/docker/service/update/
----

# docker service update

***

| Description | Update a service                          |
| ----------- | ----------------------------------------- |
| Usage       | `docker service update [OPTIONS] SERVICE` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Updates a service as described by the specified parameters. The parameters are the same as [`docker service create`](/reference/cli/docker/service/create/). Refer to the description there for further information.

Normally, updating a service will only cause the service's tasks to be replaced with new ones if a change to the service requires recreating the tasks for it to take effect. For example, only changing the `--update-parallelism` setting will not recreate the tasks, because the individual tasks are not affected by this setting. However, the `--force` flag will cause the tasks to be recreated anyway. This can be used to perform a rolling restart without any changes to the service parameters.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                                        | Default | Description                                                                                                    |
| --------------------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------- |
| `--args`                                      |         | Service command args                                                                                           |
| `--cap-add`                                   |         | API 1.41+ Add Linux capabilities                                                                               |
| `--cap-drop`                                  |         | API 1.41+ Drop Linux capabilities                                                                              |
| `--config-add`                                |         | API 1.30+ Add or update a config file on a service                                                             |
| `--config-rm`                                 |         | API 1.30+ Remove a configuration file                                                                          |
| `--constraint-add`                            |         | Add or update a placement constraint                                                                           |
| `--constraint-rm`                             |         | Remove a constraint                                                                                            |
| `--container-label-add`                       |         | Add or update a container label                                                                                |
| `--container-label-rm`                        |         | Remove a container label by its key                                                                            |
| `--credential-spec`                           |         | API 1.29+ Credential spec for managed service account (Windows only)                                           |
| `-d, --detach`                                |         | API 1.29+ Exit immediately instead of waiting for the service to converge                                      |
| `--dns-add`                                   |         | API 1.25+ Add or update a custom DNS server                                                                    |
| `--dns-option-add`                            |         | API 1.25+ Add or update a DNS option                                                                           |
| `--dns-option-rm`                             |         | API 1.25+ Remove a DNS option                                                                                  |
| `--dns-rm`                                    |         | API 1.25+ Remove a custom DNS server                                                                           |
| `--dns-search-add`                            |         | API 1.25+ Add or update a custom DNS search domain                                                             |
| `--dns-search-rm`                             |         | API 1.25+ Remove a DNS search domain                                                                           |
| `--endpoint-mode`                             |         | Endpoint mode (vip or dnsrr)                                                                                   |
| `--entrypoint`                                |         | Overwrite the default ENTRYPOINT of the image                                                                  |
| `--env-add`                                   |         | Add or update an environment variable                                                                          |
| `--env-rm`                                    |         | Remove an environment variable                                                                                 |
| `--force`                                     |         | API 1.25+ Force update even if no changes require it                                                           |
| `--generic-resource-add`                      |         | API 1.32+ Add a Generic resource                                                                               |
| `--generic-resource-rm`                       |         | API 1.32+ Remove a Generic resource                                                                            |
| `--group-add`                                 |         | API 1.25+ Add an additional supplementary user group to the container                                          |
| `--group-rm`                                  |         | API 1.25+ Remove a previously added supplementary user group from the container                                |
| `--health-cmd`                                |         | API 1.25+ Command to run to check health                                                                       |
| `--health-interval`                           |         | API 1.25+ Time between running the check (ms\|s\|m\|h)                                                         |
| `--health-retries`                            |         | API 1.25+ Consecutive failures needed to report unhealthy                                                      |
| `--health-start-interval`                     |         | API 1.44+ Time between running the check during the start period (ms\|s\|m\|h)                                 |
| `--health-start-period`                       |         | API 1.29+ Start period for the container to initialize before counting retries towards unstable (ms\|s\|m\|h)  |
| `--health-timeout`                            |         | API 1.25+ Maximum time to allow one check to run (ms\|s\|m\|h)                                                 |
| `--host-add`                                  |         | API 1.25+ Add a custom host-to-IP mapping (`host:ip`)                                                          |
| `--host-rm`                                   |         | API 1.25+ Remove a custom host-to-IP mapping (`host:ip`)                                                       |
| `--hostname`                                  |         | API 1.25+ Container hostname                                                                                   |
| `--image`                                     |         | Service image tag                                                                                              |
| `--init`                                      |         | API 1.37+ Use an init inside each service container to forward signals and reap processes                      |
| [`--isolation`](#isolation)                   |         | API 1.35+ Service container isolation mode                                                                     |
| `--label-add`                                 |         | Add or update a service label                                                                                  |
| `--label-rm`                                  |         | Remove a label by its key                                                                                      |
| `--limit-cpu`                                 |         | Limit CPUs                                                                                                     |
| `--limit-memory`                              |         | Limit Memory                                                                                                   |
| `--limit-pids`                                |         | API 1.41+ Limit maximum number of processes (default 0 = unlimited)                                            |
| `--log-driver`                                |         | Logging driver for service                                                                                     |
| `--log-opt`                                   |         | Logging driver options                                                                                         |
| `--max-concurrent`                            |         | API 1.41+ Number of job tasks to run concurrently (default equal to --replicas)                                |
| `--memory-swap`                               |         | API 1.52+ Swap Bytes (-1 for unlimited)                                                                        |
| `--memory-swappiness`                         | `-1`    | API 1.52+ Tune memory swappiness (0-100), -1 to reset to default                                               |
| [`--mount-add`](#mount-add)                   |         | Add or update a mount on a service                                                                             |
| `--mount-rm`                                  |         | Remove a mount by its target path                                                                              |
| [`--network-add`](#network-add)               |         | API 1.29+ Add a network                                                                                        |
| `--network-rm`                                |         | API 1.29+ Remove a network                                                                                     |
| `--no-healthcheck`                            |         | API 1.25+ Disable any container-specified HEALTHCHECK                                                          |
| `--no-resolve-image`                          |         | API 1.30+ Do not query the registry to resolve image digest and supported platforms                            |
| `--oom-score-adj`                             |         | API 1.46+ Tune host's OOM preferences (-1000 to 1000)                                                          |
| `--placement-pref-add`                        |         | API 1.28+ Add a placement preference                                                                           |
| `--placement-pref-rm`                         |         | API 1.28+ Remove a placement preference                                                                        |
| [`--publish-add`](#publish-add)               |         | Add or update a published port                                                                                 |
| `--publish-rm`                                |         | Remove a published port by its target port                                                                     |
| `-q, --quiet`                                 |         | Suppress progress output                                                                                       |
| `--read-only`                                 |         | API 1.28+ Mount the container's root filesystem as read only                                                   |
| `--replicas`                                  |         | Number of tasks                                                                                                |
| `--replicas-max-per-node`                     |         | API 1.40+ Maximum number of tasks per node (default 0 = unlimited)                                             |
| `--reserve-cpu`                               |         | Reserve CPUs                                                                                                   |
| `--reserve-memory`                            |         | Reserve Memory                                                                                                 |
| `--restart-condition`                         |         | Restart when condition is met (`none`, `on-failure`, `any`)                                                    |
| `--restart-delay`                             |         | Delay between restart attempts (ns\|us\|ms\|s\|m\|h)                                                           |
| `--restart-max-attempts`                      |         | Maximum number of restarts before giving up                                                                    |
| `--restart-window`                            |         | Window used to evaluate the restart policy (ns\|us\|ms\|s\|m\|h)                                               |
| [`--rollback`](#rollback)                     |         | API 1.25+ Rollback to previous specification                                                                   |
| `--rollback-delay`                            |         | API 1.28+ Delay between task rollbacks (ns\|us\|ms\|s\|m\|h)                                                   |
| `--rollback-failure-action`                   |         | API 1.28+ Action on rollback failure (`pause`, `continue`)                                                     |
| `--rollback-max-failure-ratio`                |         | API 1.28+ Failure rate to tolerate during a rollback                                                           |
| `--rollback-monitor`                          |         | API 1.28+ Duration after each task rollback to monitor for failure (ns\|us\|ms\|s\|m\|h)                       |
| `--rollback-order`                            |         | API 1.29+ Rollback order (`start-first`, `stop-first`)                                                         |
| `--rollback-parallelism`                      |         | API 1.28+ Maximum number of tasks rolled back simultaneously (0 to roll back all at once)                      |
| [`--secret-add`](#secret-add)                 |         | API 1.25+ Add or update a secret on a service                                                                  |
| `--secret-rm`                                 |         | API 1.25+ Remove a secret                                                                                      |
| `--stop-grace-period`                         |         | Time to wait before force killing a container (ns\|us\|ms\|s\|m\|h)                                            |
| `--stop-signal`                               |         | API 1.28+ Signal to stop the container                                                                         |
| `--sysctl-add`                                |         | API 1.40+ Add or update a Sysctl option                                                                        |
| `--sysctl-rm`                                 |         | API 1.40+ Remove a Sysctl option                                                                               |
| `-t, --tty`                                   |         | API 1.25+ Allocate a pseudo-TTY                                                                                |
| `--ulimit-add`                                |         | API 1.41+ Add or update a ulimit option                                                                        |
| `--ulimit-rm`                                 |         | API 1.41+ Remove a ulimit option                                                                               |
| `--update-delay`                              |         | Delay between updates (ns\|us\|ms\|s\|m\|h)                                                                    |
| `--update-failure-action`                     |         | Action on update failure (`pause`, `continue`, `rollback`)                                                     |
| `--update-max-failure-ratio`                  |         | API 1.25+ Failure rate to tolerate during an update                                                            |
| `--update-monitor`                            |         | API 1.25+ Duration after each task update to monitor for failure (ns\|us\|ms\|s\|m\|h)                         |
| `--update-order`                              |         | API 1.29+ Update order (`start-first`, `stop-first`)                                                           |
| [`--update-parallelism`](#update-parallelism) |         | Maximum number of tasks updated simultaneously (0 to update all at once)                                       |
| `-u, --user`                                  |         | Username or UID (format: \<name\|uid>\[:\<group\|gid>])                                                        |
| `--with-registry-auth`                        |         | Send registry authentication details to swarm agents                                                           |
| `-w, --workdir`                               |         | Working directory inside the container                                                                         |

## [Examples](#examples)

### [Update a service](#update-a-service)

```console
$ docker service update --limit-cpu 2 redis
```

### [Perform a rolling restart with no parameter changes](#update-parallelism)

```console
$ docker service update --force --update-parallelism 1 --update-delay 30s redis
```

In this example, the `--force` flag causes the service's tasks to be shut down and replaced with new ones even though none of the other parameters would normally cause that to happen. The `--update-parallelism 1` setting ensures that only one task is replaced at a time (this is the default behavior). The `--update-delay 30s` setting introduces a 30 second delay between tasks, so that the rolling restart happens gradually.

### [Add or remove mounts (--mount-add, --mount-rm)](#mount-add)

Use the `--mount-add` or `--mount-rm` options add or remove a service's bind mounts or volumes.

The following example creates a service which mounts the `test-data` volume to `/somewhere`. The next step updates the service to also mount the `other-volume` volume to `/somewhere-else`volume, The last step unmounts the `/somewhere` mount point, effectively removing the `test-data` volume. Each command returns the service name.

* The `--mount-add` flag takes the same parameters as the `--mount` flag on `service create`. Refer to the [volumes and bind mounts](/reference/cli/docker/service/create/#mount) section in the `service create` reference for details.

* The `--mount-rm` flag takes the `target` path of the mount.

```console
$ docker service create \
    --name=myservice \
    --mount type=volume,source=test-data,target=/somewhere \
    nginx:alpine

myservice

$ docker service update \
    --mount-add type=volume,source=other-volume,target=/somewhere-else \
    myservice

myservice

$ docker service update --mount-rm /somewhere myservice

myservice
```

### [Add or remove published service ports (--publish-add, --publish-rm)](#publish-add)

Use the `--publish-add` or `--publish-rm` flags to add or remove a published port for a service. You can use the short or long syntax discussed in the [docker service create](/reference/cli/docker/service/create/#publish) reference.

The following example adds a published service port to an existing service.

```console
$ docker service update \
  --publish-add published=8080,target=80 \
  myservice
```

### [Add or remove network (--network-add, --network-rm)](#network-add)

Use the `--network-add` or `--network-rm` flags to add or remove a network for a service. You can use the short or long syntax discussed in the [docker service create](/reference/cli/docker/service/create/#network) reference.

The following example adds a new alias name to an existing service already connected to network my-network:

```console
$ docker service update \
  --network-rm my-network \
  --network-add name=my-network,alias=web1 \
  myservice
```

### [Roll back to the previous version of a service (--rollback)](#rollback)

Use the `--rollback` option to roll back to the previous version of the service.

This will revert the service to the configuration that was in place before the most recent `docker service update` command.

The following example updates the number of replicas for the service from 4 to 5, and then rolls back to the previous configuration.

```console
$ docker service update --replicas=5 web

web

$ docker service ls

ID            NAME  MODE        REPLICAS  IMAGE
80bvrzp6vxf3  web   replicated  0/5       nginx:alpine
```

The following example rolls back the `web` service:

```console
$ docker service update --rollback web

web

$ docker service ls

ID            NAME  MODE        REPLICAS  IMAGE
80bvrzp6vxf3  web   replicated  0/4       nginx:alpine
```

Other options can be combined with `--rollback` as well, for example, `--update-delay 0s` to execute the rollback without a delay between tasks:

```console
$ docker service update \
  --rollback \
  --update-delay 0s
  web

web
```

Services can also be set up to roll back to the previous version automatically when an update fails. To set up a service for automatic rollback, use `--update-failure-action=rollback`. A rollback will be triggered if the fraction of the tasks which failed to update successfully exceeds the value given with `--update-max-failure-ratio`.

The rate, parallelism, and other parameters of a rollback operation are determined by the values passed with the following flags:

* `--rollback-delay`
* `--rollback-failure-action`
* `--rollback-max-failure-ratio`
* `--rollback-monitor`
* `--rollback-parallelism`

For example, a service set up with `--update-parallelism 1 --rollback-parallelism 3` will update one task at a time during a normal update, but during a rollback, 3 tasks at a time will get rolled back. These rollback parameters are respected both during automatic rollbacks and for rollbacks initiated manually using `--rollback`.

### [Add or remove secrets (--secret-add, --secret-rm)](#secret-add)

Use the `--secret-add` or `--secret-rm` options add or remove a service's secrets.

The following example adds a secret named `ssh-2` and removes `ssh-1`:

```console
$ docker service update \
    --secret-add source=ssh-2,target=ssh-2 \
    --secret-rm ssh-1 \
    myservice
```

### [Update services using templates](#update-services-using-templates)

Some flags of `service update` support the use of templating. See [`service create`](/reference/cli/docker/service/create/#create-services-using-templates) for the reference.

### [Specify isolation mode on Windows (--isolation)](#isolation)

`service update` supports the same `--isolation` flag as `service create` See [`service create`](/reference/cli/docker/service/create/) for the reference.

### [Updating Jobs](#updating-jobs)

When a service is created as a job, by setting its mode to `replicated-job` or to `global-job` when doing `service create`, options for updating it are limited.

Updating a Job immediately stops any Tasks that are in progress. The operation creates a new set of Tasks for the job and effectively resets its completion status. If any Tasks were running before the update, they are stopped, and new Tasks are created.

Jobs cannot be rolled out or rolled back. None of the flags for configuring update or rollback settings are valid with job modes.

To run a job again with the same parameters that it was run previously, it can be force updated with the `--force` flag.

----
url: https://docs.docker.com/guides/docker-build-cloud/
----

# Docker Build Cloud: Reclaim your time with fast, multi-architecture builds

Table of contents

***

Build applications up to 39x faster using cloud-based resources, shared team cache, and native multi-architecture support.

**Time to complete** 10 minutes

98% of developers spend up to an hour every day waiting for builds to finish ([Incredibuild: 2022 Big Dev Build Times](https://www.incredibuild.com/survey-report-2022)). Heavy, complex builds can become a major roadblock for development teams, slowing down both local development and CI/CD pipelines.

Docker Build Cloud speeds up image build times to improve developer productivity, reduce frustrations, and help you shorten the release cycle.

## [Who’s this for?](#whos-this-for)

* Anyone who wants to tackle common causes of slow image builds: limited local resources, slow emulation, and lack of build collaboration across a team.
* Developers working on older machines who want to build faster.
* Development teams working on the same repository who want to cut wait times with a shared cache.
* Developers performing multi-architecture builds who don’t want to spend hours configuring and rebuilding for emulators.

## [What you’ll learn](#what-youll-learn)

* Building container images faster locally and in CI
* Accelerating builds for multi-platform images
* Reusing pre-built images to expedite workflows

## [Tools integration](#tools-integration)

Works well with Docker Compose, GitHub Actions, and other CI solutions

## [Modules](#modules)

1. [Why Docker Build Cloud?](https://docs.docker.com/guides/docker-build-cloud/why/)

   Learn how Docker Build Cloud makes your builds faster.

2. [Demo: set up and use Docker Build Cloud in development](https://docs.docker.com/guides/docker-build-cloud/dev/)

   Learn how to use Docker Build Cloud for local builds.

3. [Demo: Using Docker Build Cloud in CI](https://docs.docker.com/guides/docker-build-cloud/ci/)

   Learn how to use Docker Build Cloud to build your app faster in CI.

4. [Common challenges and questions](https://docs.docker.com/guides/docker-build-cloud/common-questions/)

   Explore common challenges and questions related to Docker Build Cloud.

----
url: https://docs.docker.com/reference/cli/docker/model/
----

# docker model

***

| Description | Docker Model Runner |
| ----------- | ------------------- |

## [Description](#description)

Use Docker Model Runner to run and interact with AI models directly from the command line. For more information, see the [documentation](/ai/model-runner/)

## [Subcommands](#subcommands)

| Command                                                                                                 | Description                                                            |
| ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| [`docker model bench`](https://docs.docker.com/reference/cli/docker/model/bench/)                       | Benchmark a model's performance at different concurrency levels        |
| [`docker model context`](https://docs.docker.com/reference/cli/docker/model/context/)                   | Manage Docker Model Runner contexts                                    |
| [`docker model df`](https://docs.docker.com/reference/cli/docker/model/df/)                             | Show Docker Model Runner disk usage                                    |
| [`docker model gateway`](https://docs.docker.com/reference/cli/docker/model/gateway/)                   | Run an OpenAI-compatible LLM gateway                                   |
| [`docker model inspect`](https://docs.docker.com/reference/cli/docker/model/inspect/)                   | Display detailed information on one model                              |
| [`docker model install-runner`](https://docs.docker.com/reference/cli/docker/model/install-runner/)     | Install Docker Model Runner (Docker Engine only)                       |
| [`docker model launch`](https://docs.docker.com/reference/cli/docker/model/launch/)                     | Launch an app configured to use Docker Model Runner                    |
| [`docker model list`](https://docs.docker.com/reference/cli/docker/model/list/)                         | List the models pulled to your local environment                       |
| [`docker model logs`](https://docs.docker.com/reference/cli/docker/model/logs/)                         | Fetch the Docker Model Runner logs                                     |
| [`docker model package`](https://docs.docker.com/reference/cli/docker/model/package/)                   | Package a model into a Docker Model OCI artifact                       |
| [`docker model ps`](https://docs.docker.com/reference/cli/docker/model/ps/)                             | List running models                                                    |
| [`docker model pull`](https://docs.docker.com/reference/cli/docker/model/pull/)                         | Pull a model from Docker Hub or HuggingFace to your local environment  |
| [`docker model purge`](https://docs.docker.com/reference/cli/docker/model/purge/)                       | Remove all models                                                      |
| [`docker model push`](https://docs.docker.com/reference/cli/docker/model/push/)                         | Push a model to Docker Hub or Hugging Face                             |
| [`docker model reinstall-runner`](https://docs.docker.com/reference/cli/docker/model/reinstall-runner/) | Reinstall Docker Model Runner (Docker Engine only)                     |
| [`docker model requests`](https://docs.docker.com/reference/cli/docker/model/requests/)                 | Fetch requests+responses from Docker Model Runner                      |
| [`docker model restart-runner`](https://docs.docker.com/reference/cli/docker/model/restart-runner/)     | Restart Docker Model Runner (Docker Engine only)                       |
| [`docker model rm`](https://docs.docker.com/reference/cli/docker/model/rm/)                             | Remove local models downloaded from Docker Hub                         |
| [`docker model run`](https://docs.docker.com/reference/cli/docker/model/run/)                           | Run a model and interact with it using a submitted prompt or chat mode |
| [`docker model search`](https://docs.docker.com/reference/cli/docker/model/search/)                     | Search for models on Docker Hub and HuggingFace                        |
| [`docker model show`](https://docs.docker.com/reference/cli/docker/model/show/)                         | Show information for a model                                           |
| [`docker model skills`](https://docs.docker.com/reference/cli/docker/model/skills/)                     | Install Docker Model Runner skills for AI coding assistants            |
| [`docker model start-runner`](https://docs.docker.com/reference/cli/docker/model/start-runner/)         | Start Docker Model Runner (Docker Engine only)                         |
| [`docker model status`](https://docs.docker.com/reference/cli/docker/model/status/)                     | Check if the Docker Model Runner is running                            |
| [`docker model stop-runner`](https://docs.docker.com/reference/cli/docker/model/stop-runner/)           | Stop Docker Model Runner (Docker Engine only)                          |
| [`docker model tag`](https://docs.docker.com/reference/cli/docker/model/tag/)                           | Tag a model                                                            |
| [`docker model uninstall-runner`](https://docs.docker.com/reference/cli/docker/model/uninstall-runner/) | Uninstall Docker Model Runner (Docker Engine only)                     |
| [`docker model unload`](https://docs.docker.com/reference/cli/docker/model/unload/)                     | Unload running models                                                  |
| [`docker model version`](https://docs.docker.com/reference/cli/docker/model/version/)                   | Show the Docker Model Runner version                                   |

----
url: https://docs.docker.com/docker-hub/repos/manage/trusted-content/dsos-program/
----

# Docker-Sponsored Open Source Program

***

Table of contents

***

[Docker-Sponsored Open Source images](https://hub.docker.com/search?badges=open_source) are published and maintained by open-source projects sponsored by Docker through the program.

Images that are part of this program have a special badge on Docker Hub making it easier for users to identify projects that Docker has verified as trusted, secure, and active open-source projects.

The Docker-Sponsored Open Source (DSOS) Program provides several features and benefits to non-commercial open source developers.

The program grants the following perks to eligible projects:

* Repository logo
* Verified Docker-Sponsored Open Source badge
* Insights and analytics
* Access to [Docker Scout](#docker-scout) for software supply chain management
* Removal of rate limiting for developers
* Improved discoverability on Docker Hub

These benefits are valid for one year and publishers can renew annually if the project still meets the program requirements. Program members and all users pulling public images from the project namespace get access to unlimited pulls and unlimited egress.

### [Repository logo](#repository-logo)

DSOS organizations can upload custom images for individual repositories on Docker Hub. This lets you override the default organization-level logo on a per-repository basis.

Only a user with an owner or editor role for the organization can change the repository logo.

#### [Image requirements](#image-requirements)

* The supported filetypes for the logo image are JPEG and PNG.
* The minimum allowed image size in pixels is 120×120.
* The maximum allowed image size in pixels is 1000×1000.
* The maximum allowed image file size is 5MB.

#### [Set the repository logo](#set-the-repository-logo)

1. Sign in to [Docker Hub](https://hub.docker.com).
2. Go to the page of the repository that you want to change the logo for.
3. Select the upload logo button, represented by a camera icon ( ) overlaying the current repository logo.
4. In the dialog that opens, select the PNG image that you want to upload to set it as the logo for the repository.

#### [Remove the logo](#remove-the-logo)

Select the **Clear** button ( ) to remove a logo.

Removing the logo makes the repository default to using the organization logo, if set, or the following default logo if not.

### [Verified Docker-Sponsored Open Source badge](#verified-docker-sponsored-open-source-badge)

Docker verifies that developers can trust images with this badge on Docker Hub as an active open source project.

### [Insights and analytics](#insights-and-analytics)

The [insights and analytics](/docker-hub/publish/insights-analytics) service provides usage metrics for how the community uses Docker images, granting insight into user behavior.

The usage metrics show the number of image pulls by tag or by digest, and breakdowns by geolocation, cloud provider, client, and more.

You can select the time span for which you want to view analytics data. You can also export the data in either a summary or raw format.

### [Docker Scout](#docker-scout)

DSOS projects can enable Docker Scout on up to 100 repositories for free. Docker Scout provides automatic image analysis, policy evaluation for improved supply chain management, integrations with third-party systems like CI platforms and source code management, and more.

You can enable Docker Scout on a per-repository basis. For information about how to use this product, refer to the [Docker Scout documentation](/scout/).

### [Who's eligible for the Docker-Sponsored Open Source program?](#whos-eligible-for-the-docker-sponsored-open-source-program)

To qualify for the program, a publisher must share the project namespace in public repositories, meet [the Open Source Initiative definition](https://opensource.org/docs/osd), and be in active development with no pathway to commercialization.

Find out more by heading to the [Docker-Sponsored Open Source Program](https://www.docker.com/community/open-source/application/) application page.

----
url: https://docs.docker.com/engine/security/trust/trust_key_mng/
----

# Manage keys for content trust

***

Table of contents

***

Trust for an image tag is managed through the use of keys. Docker's content trust makes use of five different types of keys:

| Key        | Description                                                                                                                                                                                                                         |
| ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| root key   | Root of content trust for an image tag. When content trust is enabled, you create the root key once. Also known as the offline key, because it should be kept offline.                                                              |
| targets    | This key allows you to sign image tags, to manage delegations including delegated keys or permitted delegation paths. Also known as the repository key, since this key determines what tags can be signed into an image repository. |
| snapshot   | This key signs the current collection of image tags, preventing mix and match attacks.                                                                                                                                              |
| timestamp  | This key allows Docker image repositories to have freshness security guarantees without requiring periodic content refreshes on the client's side.                                                                                  |
| delegation | Delegation keys are optional tagging keys and allow you to delegate signing image tags to other publishers without having to share your targets key.                                                                                |

When doing a `docker push` with Content Trust enabled for the first time, the root, targets, snapshot, and timestamp keys are generated automatically for the image repository:

* The root and targets key are generated and stored locally client-side.

* The timestamp and snapshot keys are safely generated and stored in a signing server that is deployed alongside the Docker registry. These keys are generated in a backend service that isn't directly exposed to the internet and are encrypted at rest. Use the Notary CLI to [manage your snapshot key locally](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#rotate-keys).

Delegation keys are optional, and not generated as part of the normal `docker` workflow. They need to be [manually generated and added to the repository](https://docs.docker.com/engine/security/trust/trust_delegation/#creating-delegation-keys).

## [Choose a passphrase](#choose-a-passphrase)

The passphrases you chose for both the root key and your repository key should be randomly generated and stored in a password manager. Having the repository key allows users to sign image tags on a repository. Passphrases are used to encrypt your keys at rest and ensure that a lost laptop or an unintended backup doesn't put the private key material at risk.

## [Back up your keys](#back-up-your-keys)

All the Docker trust keys are stored encrypted using the passphrase you provide on creation. Even so, you should still take care of the location where you back them up. Good practice is to create two encrypted USB keys.

> Warning
>
> It is very important that you back up your keys to a safe, secure location. The loss of the repository key is recoverable, but the loss of the root key is not.

The Docker client stores the keys in the `~/.docker/trust/private` directory. Before backing them up, you should `tar` them into an archive:

```console
$ umask 077; tar -zcvf private_keys_backup.tar.gz ~/.docker/trust/private; umask 022
```

## [Hardware storage and signing](#hardware-storage-and-signing)

Docker Content Trust can store and sign with root keys from a Yubikey 4. The Yubikey is prioritized over keys stored in the filesystem. When you initialize a new repository with content trust, Docker Engine looks for a root key locally. If a key is not found and the Yubikey 4 exists, Docker Engine creates a root key in the Yubikey 4. Consult the [Notary documentation](https://github.com/theupdateframework/notary/blob/master/docs/advanced_usage.md#use-a-yubikey) for more details.

Prior to Docker Engine 1.11, this feature was only in the experimental branch.

## [Key loss](#key-loss)

> Warning
>
> If a publisher loses keys it means losing the ability to sign images for the repositories in question. If you lose a key, send an email to [Docker Hub Support](mailto:hub-support@docker.com). As a reminder, the loss of a root key is not recoverable.

This loss also requires manual intervention from every consumer that used a signed tag from this repository prior to the loss.\
Image consumers get the following error for content previously downloaded from the affected repo(s):

```console
Warning: potential malicious behavior - trust data has insufficient signatures for remote repository docker.io/my/image: valid signatures did not meet threshold
```

To correct this, they need to download a new image tag that is signed with the new key.

## [Related information](#related-information)

* [Content trust in Docker](https://docs.docker.com/engine/security/trust/)
* [Automation with content trust](https://docs.docker.com/engine/security/trust/trust_automation/)
* [Delegations for content trust](https://docs.docker.com/engine/security/trust/trust_delegation/)

----
url: https://docs.docker.com/engine/swarm/admin_guide/
----

# Administer and maintain a swarm of Docker Engines

***

Table of contents

***

When you run a swarm of Docker Engines, manager nodes are the key components for managing the swarm and storing the swarm state. It is important to understand some key features of manager nodes to properly deploy and maintain the swarm.

Refer to [How nodes work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/) for a brief overview of Docker Swarm mode and the difference between manager and worker nodes.

## [Operate manager nodes in a swarm](#operate-manager-nodes-in-a-swarm)

Swarm manager nodes use the [Raft Consensus Algorithm](https://docs.docker.com/engine/swarm/raft/) to manage the swarm state. You only need to understand some general concepts of Raft in order to manage a swarm.

There is no limit on the number of manager nodes. The decision about how many manager nodes to implement is a trade-off between performance and fault-tolerance. Adding manager nodes to a swarm makes the swarm more fault-tolerant. However, additional manager nodes reduce write performance because more nodes must acknowledge proposals to update the swarm state. This means more network round-trip traffic.

Raft requires a majority of managers, also called the quorum, to agree on proposed updates to the swarm, such as node additions or removals. Membership operations are subject to the same constraints as state replication.

### [Maintain the quorum of managers](#maintain-the-quorum-of-managers)

If the swarm loses the quorum of managers, the swarm cannot perform management tasks. If your swarm has multiple managers, always have more than two. To maintain quorum, a majority of managers must be available. An odd number of managers is recommended, because the next even number does not make the quorum easier to keep. For instance, whether you have 3 or 4 managers, you can still only lose 1 manager and maintain the quorum. If you have 5 or 6 managers, you can still only lose two.

Even if a swarm loses the quorum of managers, swarm tasks on existing worker nodes continue to run. However, swarm nodes cannot be added, updated, or removed, and new or existing tasks cannot be started, stopped, moved, or updated.

See [Recovering from losing the quorum](#recover-from-losing-the-quorum) for troubleshooting steps if you do lose the quorum of managers.

## [Configure the manager to advertise on a static IP address](#configure-the-manager-to-advertise-on-a-static-ip-address)

When initiating a swarm, you must specify the `--advertise-addr` flag to advertise your address to other manager nodes in the swarm. For more information, see [Run Docker Engine in swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/#configure-the-advertise-address). Because manager nodes are meant to be a stable component of the infrastructure, you should use a *fixed IP address* for the advertise address to prevent the swarm from becoming unstable on machine reboot.

If the whole swarm restarts and every manager node subsequently gets a new IP address, there is no way for any node to contact an existing manager. Therefore the swarm is hung while nodes try to contact one another at their old IP addresses.

Dynamic IP addresses are OK for worker nodes.

## [Add manager nodes for fault tolerance](#add-manager-nodes-for-fault-tolerance)

You should maintain an odd number of managers in the swarm to support manager node failures. Having an odd number of managers ensures that during a network partition, there is a higher chance that the quorum remains available to process requests if the network is partitioned into two sets. Keeping the quorum is not guaranteed if you encounter more than two network partitions.

| Swarm Size | Majority | Fault Tolerance |
| ---------- | -------- | --------------- |
| 1          | 1        | 0               |
| 2          | 2        | 0               |
| **3**      | 2        | **1**           |
| 4          | 3        | 1               |
| **5**      | 3        | **2**           |
| 6          | 4        | 2               |
| **7**      | 4        | **3**           |
| 8          | 5        | 3               |
| **9**      | 5        | **4**           |

For example, in a swarm with *5 nodes*, if you lose *3 nodes*, you don't have a quorum. Therefore you can't add or remove nodes until you recover one of the unavailable manager nodes or recover the swarm with disaster recovery commands. See [Recover from disaster](#recover-from-disaster).

While it is possible to scale a swarm down to a single manager node, it is impossible to demote the last manager node. This ensures you maintain access to the swarm and that the swarm can still process requests. Scaling down to a single manager is an unsafe operation and is not recommended. If the last node leaves the swarm unexpectedly during the demote operation, the swarm becomes unavailable until you reboot the node or restart with `--force-new-cluster`.

You manage swarm membership with the `docker swarm` and `docker node` subsystems. Refer to [Add nodes to a swarm](https://docs.docker.com/engine/swarm/join-nodes/) for more information on how to add worker nodes and promote a worker node to be a manager.

### [Distribute manager nodes](#distribute-manager-nodes)

In addition to maintaining an odd number of manager nodes, pay attention to datacenter topology when placing managers. For optimal fault-tolerance, distribute manager nodes across a minimum of 3 availability-zones to support failures of an entire set of machines or common maintenance scenarios. If you suffer a failure in any of those zones, the swarm should maintain the quorum of manager nodes available to process requests and rebalance workloads.

| Swarm manager nodes | Repartition (on 3 Availability zones) |
| ------------------- | ------------------------------------- |
| 3                   | 1-1-1                                 |
| 5                   | 2-2-1                                 |
| 7                   | 3-2-2                                 |
| 9                   | 3-3-3                                 |

### [Run manager-only nodes](#run-manager-only-nodes)

By default manager nodes also act as a worker nodes. This means the scheduler can assign tasks to a manager node. For small and non-critical swarms assigning tasks to managers is relatively low-risk as long as you schedule services using resource constraints for cpu and memory.

However, because manager nodes use the Raft consensus algorithm to replicate data in a consistent way, they are sensitive to resource starvation. You should isolate managers in your swarm from processes that might block swarm operations like swarm heartbeat or leader elections.

To avoid interference with manager node operation, you can drain manager nodes to make them unavailable as worker nodes:

```console
$ docker node update --availability drain NODE
```

When you drain a node, the scheduler reassigns any tasks running on the node to other available worker nodes in the swarm. It also prevents the scheduler from assigning tasks to the node.

## [Add worker nodes for load balancing](#add-worker-nodes-for-load-balancing)

[Add nodes to the swarm](https://docs.docker.com/engine/swarm/join-nodes/) to balance your swarm's load. Replicated service tasks are distributed across the swarm as evenly as possible over time, as long as the worker nodes are matched to the requirements of the services. When limiting a service to run on only specific types of nodes, such as nodes with a specific number of CPUs or amount of memory, remember that worker nodes that do not meet these requirements cannot run these tasks.

## [Monitor swarm health](#monitor-swarm-health)

You can monitor the health of manager nodes by querying the docker `nodes` API in JSON format through the `/nodes` HTTP endpoint. Refer to the [nodes API documentation](/reference/api/engine/version/v1.25/#tag/Node) for more information.

From the command line, run `docker node inspect <id-node>` to query the nodes. For instance, to query the reachability of the node as a manager:

```console
$ docker node inspect manager1 --format "{{ .ManagerStatus.Reachability }}"
reachable
```

To query the status of the node as a worker that accept tasks:

```console
$ docker node inspect manager1 --format "{{ .Status.State }}"
ready
```

From those commands, we can see that `manager1` is both at the status `reachable` as a manager and `ready` as a worker.

An `unreachable` health status means that this particular manager node is unreachable from other manager nodes. In this case you need to take action to restore the unreachable manager:

* Restart the daemon and see if the manager comes back as reachable.
* Reboot the machine.
* If neither restarting nor rebooting works, you should add another manager node or promote a worker to be a manager node. You also need to cleanly remove the failed node entry from the manager set with `docker node demote <NODE>` and `docker node rm <id-node>`.

Alternatively you can also get an overview of the swarm health from a manager node with `docker node ls`:

```console
$ docker node ls
ID                           HOSTNAME  MEMBERSHIP  STATUS  AVAILABILITY  MANAGER STATUS
1mhtdwhvsgr3c26xxbnzdc3yp    node05    Accepted    Ready   Active
516pacagkqp2xc3fk9t1dhjor    node02    Accepted    Ready   Active        Reachable
9ifojw8of78kkusuc4a6c23fx *  node01    Accepted    Ready   Active        Leader
ax11wdpwrrb6db3mfjydscgk7    node04    Accepted    Ready   Active
bb1nrq2cswhtbg4mrsqnlx1ck    node03    Accepted    Ready   Active        Reachable
di9wxgz8dtuh9d2hn089ecqkf    node06    Accepted    Ready   Active
```

## [Troubleshoot a manager node](#troubleshoot-a-manager-node)

You should never restart a manager node by copying the `raft` directory from another node. The data directory is unique to a node ID. A node can only use a node ID once to join the swarm. The node ID space should be globally unique.

To cleanly re-join a manager node to a cluster:

1. Demote the node to a worker using `docker node demote <NODE>`.
2. Remove the node from the swarm using `docker node rm <NODE>`.
3. Re-join the node to the swarm with a fresh state using `docker swarm join`.

For more information on joining a manager node to a swarm, refer to [Join nodes to a swarm](https://docs.docker.com/engine/swarm/join-nodes/).

## [Forcibly remove a node](#forcibly-remove-a-node)

In most cases, you should shut down a node before removing it from a swarm with the `docker node rm` command. If a node becomes unreachable, unresponsive, or compromised you can forcefully remove the node without shutting it down by passing the `--force` flag. For instance, if `node9` becomes compromised:

```console
$ docker node rm node9

Error response from daemon: rpc error: code = 9 desc = node node9 is not down and can't be removed

$ docker node rm --force node9

Node node9 removed from swarm
```

Before you forcefully remove a manager node, you must first demote it to the worker role. Make sure that you always have an odd number of manager nodes if you demote or remove a manager.

## [Back up the swarm](#back-up-the-swarm)

Docker manager nodes store the swarm state and manager logs in the `/var/lib/docker/swarm/` directory. This data includes the keys used to encrypt the Raft logs. Without these keys, you cannot restore the swarm.

You can back up the swarm using any manager. Use the following procedure.

1. If the swarm has auto-lock enabled, you need the unlock key to restore the swarm from backup. Retrieve the unlock key if necessary and store it in a safe location. If you are unsure, read [Lock your swarm to protect its encryption key](https://docs.docker.com/engine/swarm/swarm_manager_locking/).

2. Stop Docker on the manager before backing up the data, so that no data is being changed during the backup. It is possible to take a backup while the manager is running (a "hot" backup), but this is not recommended and your results are less predictable when restoring. While the manager is down, other nodes continue generating swarm data that is not part of this backup.

   > Note
   >
   > Be sure to maintain the quorum of swarm managers. During the time that a manager is shut down, your swarm is more vulnerable to losing the quorum if further nodes are lost. The number of managers you run is a trade-off. If you regularly take down managers to do backups, consider running a five manager swarm, so that you can lose an additional manager while the backup is running, without disrupting your services.

3. Back up the entire `/var/lib/docker/swarm` directory.

4. Restart the manager.

To restore, see [Restore from a backup](#restore-from-a-backup).

## [Recover from disaster](#recover-from-disaster)

### [Restore from a backup](#restore-from-a-backup)

After backing up the swarm as described in [Back up the swarm](#back-up-the-swarm), use the following procedure to restore the data to a new swarm.

1. Shut down Docker on the target host machine for the restored swarm.

2. Remove the contents of the `/var/lib/docker/swarm` directory on the new swarm.

3. Restore the `/var/lib/docker/swarm` directory with the contents of the backup.

   > Note
   >
   > The new node uses the same encryption key for on-disk storage as the old one. It is not possible to change the on-disk storage encryption keys at this time.
   >
   > In the case of a swarm with auto-lock enabled, the unlock key is also the same as on the old swarm, and the unlock key is needed to restore the swarm.

4. Start Docker on the new node. Unlock the swarm if necessary. Re-initialize the swarm using the following command, so that this node does not attempt to connect to nodes that were part of the old swarm, and presumably no longer exist.

   ```console
   $ docker swarm init --force-new-cluster
   ```

5. Verify that the state of the swarm is as expected. This may include application-specific tests or simply checking the output of `docker service ls` to be sure that all expected services are present.

6. If you use auto-lock, [rotate the unlock key](https://docs.docker.com/engine/swarm/swarm_manager_locking/#rotate-the-unlock-key).

7. Add manager and worker nodes to bring your new swarm up to operating capacity.

8. Reinstate your previous backup regimen on the new swarm.

### [Recover from losing the quorum](#recover-from-losing-the-quorum)

Swarm is resilient to failures and can recover from any number of temporary node failures (machine reboots or crash with restart) or other transient errors. However, a swarm cannot automatically recover if it loses a quorum. Tasks on existing worker nodes continue to run, but administrative tasks are not possible, including scaling or updating services and joining or removing nodes from the swarm. The best way to recover is to bring the missing manager nodes back online. If that is not possible, continue reading for some options for recovering your swarm.

In a swarm of `N` managers, a quorum (a majority) of manager nodes must always be available. For example, in a swarm with five managers, a minimum of three must be operational and in communication with each other. In other words, the swarm can tolerate up to `(N-1)/2` permanent failures beyond which requests involving swarm management cannot be processed. These types of failures include data corruption or hardware failures.

If you lose the quorum of managers, you cannot administer the swarm. If you have lost the quorum and you attempt to perform any management operation on the swarm, an error occurs:

```text
Error response from daemon: rpc error: code = 4 desc = context deadline exceeded
```

The best way to recover from losing the quorum is to bring the failed nodes back online. If you can't do that, the only way to recover from this state is to use the `--force-new-cluster` action from a manager node. This removes all managers except the manager the command was run from. The quorum is achieved because there is now only one manager. Promote nodes to be managers until you have the desired number of managers.

From the node to recover, run:

```console
$ docker swarm init --force-new-cluster --advertise-addr node01:2377
```

When you run the `docker swarm init` command with the `--force-new-cluster` flag, the Docker Engine where you run the command becomes the manager node of a single-node swarm which is capable of managing and running services. The manager has all the previous information about services and tasks, worker nodes are still part of the swarm, and services are still running. You need to add or re-add manager nodes to achieve your previous task distribution and ensure that you have enough managers to maintain high availability and prevent losing the quorum.

## [Force the swarm to rebalance](#force-the-swarm-to-rebalance)

Generally, you do not need to force the swarm to rebalance its tasks. When you add a new node to a swarm, or a node reconnects to the swarm after a period of unavailability, the swarm does not automatically give a workload to the idle node. This is a design decision. If the swarm periodically shifted tasks to different nodes for the sake of balance, the clients using those tasks would be disrupted. The goal is to avoid disrupting running services for the sake of balance across the swarm. When new tasks start, or when a node with running tasks becomes unavailable, those tasks are given to less busy nodes. The goal is eventual balance, with minimal disruption to the end user.

You can use the `--force` or `-f` flag with the `docker service update` command to force the service to redistribute its tasks across the available worker nodes. This causes the service tasks to restart. Client applications may be disrupted. If you have configured it, your service uses a [rolling update](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/).

If you use an earlier version and you want to achieve an even balance of load across workers and don't mind disrupting running tasks, you can force your swarm to re-balance by temporarily scaling the service upward. Use `docker service inspect --pretty <servicename>` to see the configured scale of a service. When you use `docker service scale`, the nodes with the lowest number of tasks are targeted to receive the new workloads. There may be multiple under-loaded nodes in your swarm. You may need to scale the service up by modest increments a few times to achieve the balance you want across all the nodes.

When the load is balanced to your satisfaction, you can scale the service back down to the original scale. You can use `docker service ps` to assess the current balance of your service across nodes.

See also [`docker service scale`](/reference/cli/docker/service/scale/) and [`docker service ps`](/reference/cli/docker/service/ps/).

----
url: https://docs.docker.com/guides/dotnet/deploy/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Test your .NET deployment

***

Table of contents

***

## [Prerequisites](#prerequisites)

* Complete all the previous sections of this guide, starting with [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/).
* [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## [Overview](#overview)

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## [Create a Kubernetes YAML file](#create-a-kubernetes-yaml-file)

In your `docker-dotnet-sample` directory, create a file named `docker-dotnet-kubernetes.yaml`. Open the file in an IDE or text editor and add the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker username and the name of the repository that you created in [Configure CI/CD for your .NET application](https://docs.docker.com/guides/dotnet/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: server
  strategy: {}
  template:
    metadata:
      labels:
        service: server
    spec:
      initContainers:
        - name: wait-for-db
          image: busybox:1.28
          command:
            [
              "sh",
              "-c",
              'until nc -zv db 5432; do echo "waiting for db"; sleep 2; done;',
            ]
      containers:
        - image: DOCKER_USERNAME/REPO_NAME
          name: server
          imagePullPolicy: Always
          ports:
            - containerPort: 8080
              hostPort: 8080
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      service: db
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        service: db
    spec:
      containers:
        - env:
            - name: POSTGRES_DB
              value: example
            - name: POSTGRES_PASSWORD
              value: example
          image: postgres:18
          name: db
          ports:
            - containerPort: 5432
              protocol: TCP
          resources: {}
      restartPolicy: Always
status: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: server
  name: server
  namespace: default
spec:
  type: NodePort
  ports:
    - name: "8080"
      port: 8080
      targetPort: 8080
      nodePort: 30001
  selector:
    service: server
status:
  loadBalancer: {}
---
apiVersion: v1
kind: Service
metadata:
  labels:
    service: db
  name: db
  namespace: default
spec:
  ports:
    - name: "5432"
      port: 5432
      targetPort: 5432
  selector:
    service: db
status:
  loadBalancer: {}
```

In this Kubernetes YAML file, there are four objects, separated by the `---`. In addition to a Service and Deployment for the database, the other two objects are:

* A Deployment, describing a scalable group of identical pods. In this case, you'll get just one replica, or copy of your pod. That pod, which is described under `template`, has just one container in it. The container is created from the image built by GitHub Actions in [Configure CI/CD for your .NET application](https://docs.docker.com/guides/dotnet/configure-ci-cd/).
* A NodePort service, which will route traffic from port 30001 on your host to port 8080 inside the pods it routes to, allowing you to reach your app from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## [Deploy and check your application](#deploy-and-check-your-application)

1. In a terminal, navigate to the `docker-dotnet-sample` directory and deploy your application to Kubernetes.

   ```console
   $ kubectl apply -f docker-dotnet-kubernetes.yaml
   ```

   You should see output that looks like the following, indicating your Kubernetes objects were created successfully.

   ```shell
   deployment.apps/db created
   service/db created
   deployment.apps/server created
   service/server created
   ```

2. Make sure everything worked by listing your deployments.

   ```console
   $ kubectl get deployments
   ```

   Your deployment should be listed as follows:

   ```shell
   NAME     READY   UP-TO-DATE   AVAILABLE   AGE
   db       1/1     1            1           76s
   server   1/1     1            1           76s
   ```

   This indicates all of the pods are up and running. Do the same check for your services.

   ```console
   $ kubectl get services
   ```

   You should get output like the following.

   ```shell
   NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
   db           ClusterIP   10.96.156.90    <none>        5432/TCP         2m8s
   kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP          164m
   server       NodePort    10.102.94.225   <none>        8080:30001/TCP   2m8s
   ```

   In addition to the default `kubernetes` service, you can see your `server` service and `db` service. The `server` service is accepting traffic on port 30001/TCP.

3. Open a browser and visit your app at `localhost:30001`. You should see your application.

4. Run the following command to tear down your application.

   ```console
   $ kubectl delete -f docker-dotnet-kubernetes.yaml
   ```

----
url: https://docs.docker.com/reference/cli/docker/service/rollback/
----

# docker service rollback

***

| Description | Revert changes to a service's configuration |
| ----------- | ------------------------------------------- |
| Usage       | `docker service rollback [OPTIONS] SERVICE` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Roll back a specified service to its previous version from the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option         | Default | Description                                                               |
| -------------- | ------- | ------------------------------------------------------------------------- |
| `-d, --detach` |         | API 1.29+ Exit immediately instead of waiting for the service to converge |
| `-q, --quiet`  |         | Suppress progress output                                                  |

## [Examples](#examples)

### [Roll back to the previous version of a service](#roll-back-to-the-previous-version-of-a-service)

Use the `docker service rollback` command to roll back to the previous version of a service. After executing this command, the service is reverted to the configuration that was in place before the most recent `docker service update` command.

The following example creates a service with a single replica, updates the service to use three replicas, and then rolls back the service to the previous version, having one replica.

Create a service with a single replica:

```console
$ docker service create --name my-service -p 8080:80 nginx:alpine
```

Confirm that the service is running with a single replica:

```console
$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
xbw728mf6q0d        my-service          replicated          1/1                 nginx:alpine        *:8080->80/tcp
```

Update the service to use three replicas:

```console
$ docker service update --replicas=3 my-service

$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
xbw728mf6q0d        my-service          replicated          3/3                 nginx:alpine        *:8080->80/tcp
```

Now roll back the service to its previous version, and confirm it is running a single replica again:

```console
$ docker service rollback my-service

$ docker service ls

ID                  NAME                MODE                REPLICAS            IMAGE               PORTS
xbw728mf6q0d        my-service          replicated          1/1                 nginx:alpine        *:8080->80/tcp
```

----
url: https://docs.docker.com/guides/vuejs/run-tests/
----

# Run vue.js tests in a container

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize Vue.js application](https://docs.docker.com/guides/vuejs/containerize/).

## [Overview](#overview)

Testing is a critical part of the development process. In this section, you'll learn how to:

* Run unit tests using Vitest inside a Docker container.
* Use Docker Compose to run tests in an isolated, reproducible environment.

You’ll use [Vitest](https://vitest.dev) — a blazing fast test runner designed for Vite — together with [@vue/test-utils](https://test-utils.vuejs.org/) to write unit tests that validate your component logic, props, events, and reactive behavior.

This setup ensures your Vue.js components are tested in an environment that mirrors how users actually interact with your application.

***

## [Run tests during development](#run-tests-during-development)

`docker-vuejs-sample` application includes a sample test file at location:

```console
$ src/components/__tests__/HelloWorld.spec.ts
```

This test uses Vitest and Vue Test Utils to verify the behavior of the HelloWorld component.

***

### [Step 1: Update compose.yaml](#step-1-update-composeyaml)

Add a new service named `vuejs-test` to your `compose.yaml` file. This service allows you to run your test suite in an isolated containerized environment.

|                                                                                       |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ```
``` | ```yaml
services:
  vuejs-prod:
    build:
      context: .
      dockerfile: Dockerfile
    image: docker-vuejs-sample
    ports:
      - "8080:8080"

  vuejs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    ports:
      - "5173:5173"
    develop:
      watch:
        - action: sync
          path: .
          target: /app
          
  vuejs-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    command: ["npm", "run", "test:unit"]
``` |

The vuejs-test service reuses the same `Dockerfile.dev` used for [development](https://docs.docker.com/guides/vuejs/develop/) and overrides the default command to run tests with `npm run test`. This setup ensures a consistent test environment that matches your local development configuration.

After completing the previous steps, your project directory should contain the following files:

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

### [Step 2: Run the tests](#step-2-run-the-tests)

To execute your test suite inside the container, run the following command from your project root:

```console
$ docker compose run --rm vuejs-test
```

This command will:

* Start the `vuejs-test` service defined in your `compose.yaml` file.
* Execute the `npm run test` script using the same environment as development.
* Automatically remove the container after the tests complete [`docker compose run --rm`](/reference/cli/docker/compose/run/) command.

You should see output similar to the following:

```shell
Test Files: 1 passed (1)
Tests:      1 passed (1)
Start at:   16:50:55
Duration:   718ms
```

> Note
>
> For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

***

## [Summary](#summary)

In this section, you learned how to run unit tests for your Vue.js application inside a Docker container using Vitest and Docker Compose.

What you accomplished:

* Created a `vuejs-test` service in `compose.yaml` to isolate test execution.
* Reused the development `Dockerfile.dev` to ensure consistency between dev and test environments.
* Ran tests inside the container using `docker compose run --rm vuejs-test`.
* Ensured reliable, repeatable testing across environments without depending on your local machine setup.

***

## [Related resources](#related-resources)

Explore official references and best practices to sharpen your Docker testing workflow:

* [Dockerfile reference](/reference/dockerfile/) – Understand all Dockerfile instructions and syntax.
* [Best practices for writing Dockerfiles](/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
* [Compose file reference](/compose/compose-file/) – Learn the full syntax and options available for configuring services in `compose.yaml`.
* [`docker compose run` CLI reference](/reference/cli/docker/compose/run/) – Run one-off commands in a service container.

***

## [Next steps](#next-steps)

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions to automatically build and test your Vue.js application in a containerized environment. This ensures your code is validated on every push or pull request, maintaining consistency and reliability across your development workflow.

[Automate your builds with GitHub Actions »](https://docs.docker.com/guides/vuejs/configure-github-actions/)

----
url: https://docs.docker.com/offload/feedback/
----

Start a new chat

Answers are generated based on the documentation.

[Manuals](https://docs.docker.com/manuals/)

* [Get started](/get-started/)
* [Guides](/guides/)
* [Reference](/reference/)

# Give feedback

***

Table of contents

***

There are several ways you can provide feedback on Docker Offload.

## [Quick survey](#quick-survey)

The fastest way to share your thoughts is to fill out this short [Docker Offload feedback survey](https://docker.qualtrics.com/jfe/form/SV_br8Ki4CCdqeIYl0). It only takes a minute and helps the Docker Team improve your experience.

## [In-product feedback](#in-product-feedback)

On each Docker Desktop Dashboard view, there is a **Give feedback** link. This opens a feedback form where you can share ideas directly with the Docker Team.

## [Report bugs or problems on GitHub](#report-bugs-or-problems-on-github)

To report bugs or problems, visit the [Docker Desktop issue tracker](https://github.com/docker/desktop-feedback).

----
url: https://docs.docker.com/guides/admin-set-up/testing/
----

# Testing

***

Table of contents

***

## [SSO and SCIM testing](#sso-and-scim-testing)

Test SSO and SCIM by signing in to Docker Desktop or Docker Hub with the email address linked to a Docker account that is part of the verified domain. Developers who sign in using their Docker usernames remain unaffected by the SSO and SCIM setup.

> Important
>
> Some users may need CLI based logins to Docker Hub, and for this they will need a [personal access token (PAT)](https://docs.docker.com/security/access-tokens/).

## [Test Registry Access Management and Image Access Management](#test-registry-access-management-and-image-access-management)

> Warning
>
> Communicate with your users before proceeding, as this step will impact all existing users signing into your Docker organization.

If you plan to use [Registry Access Management (RAM)](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) and/or [Image Access Management (IAM)](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/):

1. Ensure your test developer signs in to Docker Desktop using their organization credentials
2. Have them attempt to pull an unauthorized image or one from a disallowed registry via the Docker CLI
3. Verify they receive an error message indicating that the registry is restricted by the organization

## [Deploy settings and enforce sign in to test group](#deploy-settings-and-enforce-sign-in-to-test-group)

Deploy the Docker settings and enforce sign-in for a small group of test users via MDM. Have this group test their development workflows with containers on Docker Desktop and Docker Hub to ensure all settings and the sign-in enforcement function as expected.

## [Test Docker Build Cloud capabilities](#test-docker-build-cloud-capabilities)

Have one of your Docker Desktop testers [connect to the cloud builder you created and use it to build](https://docs.docker.com/build-cloud/usage/).

## [Test Testcontainers Cloud](#test-testcontainers-cloud)

Have a test developer [connect to Testcontainers Cloud](https://testcontainers.com/cloud/docs/#getting-started) and run a container in the cloud to verify the setup is working correctly.

## [Verify Docker Scout monitoring of repositories](#verify-docker-scout-monitoring-of-repositories)

Check the [Docker Scout dashboard](https://scout.docker.com/) to confirm that data is being properly received for the repositories where Docker Scout has been enabled.

## [Verify access to Docker Hardened Images](#verify-access-to-docker-hardened-images)

Have a test developer attempt to [pull a Docker Hardened Image](https://docs.docker.com/dhi/get-started/) to confirm that the team has proper access and can integrate these images into their workflows.

[Deploy your Docker setup »](https://docs.docker.com/guides/admin-set-up/deploy/)

----
url: https://docs.docker.com/reference/cli/docker/compose/events/
----

# docker compose events

***

| Description | Receive real time events from containers       |
| ----------- | ---------------------------------------------- |
| Usage       | `docker compose events [OPTIONS] [SERVICE...]` |

## [Description](#description)

Stream container events for every container in the project.

With the `--json` flag, a json object is printed one per line with the format:

```json
{
    "time": "2015-11-20T18:01:03.615550",
    "type": "container",
    "action": "create",
    "id": "213cf7...5fc39a",
    "service": "web",
    "attributes": {
      "name": "application_web_1",
      "image": "alpine:edge"
    }
}
```

The events that can be received using this can be seen [here](/reference/cli/docker/system/events/#object-types).

## [Options](#options)

| Option    | Default | Description                               |
| --------- | ------- | ----------------------------------------- |
| `--json`  |         | Output events as a stream of json objects |
| `--since` |         | Show all events created since timestamp   |
| `--until` |         | Stream events until this timestamp        |

----
url: https://docs.docker.com/guides/docker-scout/s3c/
----

# Software supply chain security

***

Table of contents

***

The term "software supply chain" refers to the end-to-end process of developing and delivering software, from the development to deployment and maintenance. Software supply chain security, or "S3C" for short, is the practice for protecting the components and processes of the supply chain.

S3C is a fundamental change in how organizations approach software security. Traditionally in the software industry, security and compliance has been mostly an afterthought, left to the software delivery or release phase. With S3C, security is integrated into the entire software development lifecycle, from the inner loop of development and testing, to the outer loop of shipping and monitoring.

Following industry best practices for software supply chain conduct is important because it helps organizations protect their software from security threats, compliance risks, and other vulnerabilities. Implementing a software supply chain security framework improves visibility, collaboration, and traceability of a project across stakeholders. This helps organizations detect, respond to, and remediate threats more effectively.

## [Securing the software supply chain](#securing-the-software-supply-chain)

Building a secure software supply chain involves several key steps, such as:

* Identify the software components and dependencies you use to build and run your applications.
* Automate security testing throughout the software development lifecycle.
* Monitor your software supply chain for security threats.
* Implement security policies that govern how software is built, and the components it contains.

Managing the software supply chain is a complex task, especially in the modern day where software is built using multiple components from different sources. Organizations need to have a clear understanding of the software components they use, and the security risks associated with them.

## [How Docker Scout is different](#how-docker-scout-is-different)

Docker Scout is a platform designed to help organizations secure their software supply chain. It provides tools and services for identifying and managing software assets and policies, and automated remediation of security threats.

Unlike traditional security tools that focus on scheduled, point-in-time scans at specific stages in the software development lifecycle, Docker Scout uses a modern event-driven model that spans the entire software supply chain. This means that when a new vulnerability affecting your images is disclosed, your updated risk assessment is available within seconds, and earlier in the development process.

Docker Scout works by analyzing the composition of your images to create a Software Bill of Materials (SBOM). The SBOM is cross-referenced against the security advisories to identify CVEs that affect your images. Docker Scout integrates with [over 20 different security advisories](https://docs.docker.com/scout/deep-dive/advisory-db-sources/), and updates its vulnerability database in real-time. This ensures that your security posture is represented using the latest available information.

[Software Bill of Materials »](https://docs.docker.com/guides/docker-scout/sbom/)

----
url: https://docs.docker.com/engine/swarm/swarm-tutorial/delete-service/
----

# Delete the service running on the swarm

***

***

The remaining steps in the tutorial don't use the `helloworld` service, so now you can delete the service from the swarm.

1. If you haven't already, open a terminal and ssh into the machine where you run your manager node. For example, the tutorial uses a machine named `manager1`.

2. Run `docker service rm helloworld` to remove the `helloworld` service.

   ```console
   $ docker service rm helloworld

   helloworld
   ```

3. Run `docker service inspect <SERVICE-ID>` to verify that the swarm manager removed the service. The CLI returns a message that the service is not found:

   ```console
   $ docker service inspect helloworld
   []
   Status: Error: no such service: helloworld, Code: 1
   ```

4. Even though the service no longer exists, the task containers take a few seconds to clean up. You can use `docker ps` on the nodes to verify when the tasks have been removed.

   ```console
   $ docker ps

   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES
   db1651f50347        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.5.9lkmos2beppihw95vdwxy1j3w
   43bf6e532a92        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.3.a71i8rp6fua79ad43ycocl4t2
   5a0fb65d8fa7        alpine:latest       "ping docker.com"        44 minutes ago      Up 45 seconds                 helloworld.2.2jpgensh7d935qdc857pxulfr
   afb0ba67076f        alpine:latest       "ping docker.com"        44 minutes ago      Up 46 seconds                 helloworld.4.1c47o7tluz7drve4vkm2m5olx
   688172d3bfaa        alpine:latest       "ping docker.com"        45 minutes ago      Up About a minute             helloworld.1.74nbhb3fhud8jfrhigd7s29we

   $ docker ps
   CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS     NAMES
   ```

## [Next steps](#next-steps)

Next, you'll set up a new service and apply a rolling update.

[Apply rolling updates](https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/)

----
url: https://docs.docker.com/engine/release-notes/prior-releases/
----

# Docker Engine prior releases

***

Table of contents

***

## [1.13.1 (2017-02-08)](#1131-2017-02-08)

> Important
>
> On Linux distributions where `devicemapper` was the default storage driver, the `overlay2`, or `overlay` is now used by default (if the kernel supports it). To use devicemapper, you can manually configure the storage driver to use through the `--storage-driver` daemon option, or by setting "storage-driver" in the `daemon.json` configuration file.

> Important
>
> In Docker 1.13, the managed plugin api changed, as compared to the experimental version introduced in Docker 1.12. You must **uninstall** plugins which you installed with Docker 1.12 *before* upgrading to Docker 1.13. You can uninstall plugins using the `docker plugin rm` command.

If you have already upgraded to Docker 1.13 without uninstalling previously-installed plugins, you may see this message when the Docker daemon starts:

```
Error starting daemon: json: cannot unmarshal string into Go value of type types.PluginEnv
```

To manually remove all plugins and resolve this problem, take the following steps:

1. Remove plugins.json from: `/var/lib/docker/plugins/`.
2. Restart Docker. Verify that the Docker daemon starts with no errors.
3. Reinstall your plugins.

### [Contrib](#contrib)

* Do not require a custom build of tini [#28454](https://github.com/docker/docker/pull/28454)
* Upgrade to Go 1.7.5 [#30489](https://github.com/docker/docker/pull/30489)

### [Remote API (v1.26) & Client](#remote-api-v126--client)

* Support secrets in docker stack deploy with compose file [#30144](https://github.com/docker/docker/pull/30144)

### [Runtime](#runtime)

* Fix size issue in `docker system df` [#30378](https://github.com/docker/docker/pull/30378)
* Fix error on `docker inspect` when Swarm certificates were expired. [#29246](https://github.com/docker/docker/pull/29246)
* Fix deadlock on v1 plugin with activate error [#30408](https://github.com/docker/docker/pull/30408)
* Fix SELinux regression [#30649](https://github.com/docker/docker/pull/30649)

### [Plugins](#plugins)

* Support global scoped network plugins (v2) in swarm mode [#30332](https://github.com/docker/docker/pull/30332)

- Add `docker plugin upgrade` [#29414](https://github.com/docker/docker/pull/29414)

### [Windows](#windows)

* Fix small regression with old plugins in Windows [#30150](https://github.com/docker/docker/pull/30150)
* Fix warning on Windows [#30730](https://github.com/docker/docker/pull/30730)

## [1.13.0 (2017-01-18)](#1130-2017-01-18)

> Important
>
> On Linux distributions where `devicemapper` was the default storage driver, the `overlay2`, or `overlay` is now used by default (if the kernel supports it). To use devicemapper, you can manually configure the storage driver to use through the `--storage-driver` daemon option, or by setting "storage-driver" in the `daemon.json` configuration file.

> Important
>
> In Docker 1.13, the managed plugin api changed, as compared to the experimental version introduced in Docker 1.12. You must **uninstall** plugins which you installed with Docker 1.12 *before* upgrading to Docker 1.13. You can uninstall plugins using the `docker plugin rm` command.

If you have already upgraded to Docker 1.13 without uninstalling previously-installed plugins, you may see this message when the Docker daemon starts:

```
Error starting daemon: json: cannot unmarshal string into Go value of type types.PluginEnv
```

To manually remove all plugins and resolve this problem, take the following steps:

1. Remove plugins.json from: `/var/lib/docker/plugins/`.
2. Restart Docker. Verify that the Docker daemon starts with no errors.
3. Reinstall your plugins.

### [Builder](#builder)

* Add capability to specify images used as a cache source on build. These images do not need to have local parent chain and can be pulled from other registries [#26839](https://github.com/docker/docker/pull/26839)
* (experimental) Add option to squash image layers to the FROM image after successful builds [#22641](https://github.com/docker/docker/pull/22641)

- Fix dockerfile parser with empty line after escape [#24725](https://github.com/docker/docker/pull/24725)

* Add step number on `docker build` [#24978](https://github.com/docker/docker/pull/24978)

- Add support for compressing build context during image build [#25837](https://github.com/docker/docker/pull/25837)
- add `--network` to `docker build` [#27702](https://github.com/docker/docker/pull/27702)

* Fix inconsistent behavior between `--label` flag on `docker build` and `docker run` [#26027](https://github.com/docker/docker/issues/26027)
* Fix image layer inconsistencies when using the overlay storage driver [#27209](https://github.com/docker/docker/pull/27209)

- Unused build-args are now allowed. A warning is presented instead of an error and failed build [#27412](https://github.com/docker/docker/pull/27412)

* Fix builder cache issue on Windows [#27805](https://github.com/docker/docker/pull/27805)

- Allow `USER` in builder on Windows [#28415](https://github.com/docker/docker/pull/28415)
- Handle env case-insensitive on Windows [#28725](https://github.com/docker/docker/pull/28725)

### [Contrib](#contrib-1)

* Add support for building docker debs for Ubuntu 16.04 Xenial on PPC64LE [#23438](https://github.com/docker/docker/pull/23438)
* Add support for building docker debs for Ubuntu 16.04 Xenial on s390x [#26104](https://github.com/docker/docker/pull/26104)
* Add support for building docker debs for Ubuntu 16.10 Yakkety Yak on PPC64LE [#28046](https://github.com/docker/docker/pull/28046)

- Add RPM builder for VMWare Photon OS [#24116](https://github.com/docker/docker/pull/24116)

* Add shell completions to tgz [#27735](https://github.com/docker/docker/pull/27735)

- Update the install script to allow using the mirror in China [#27005](https://github.com/docker/docker/pull/27005)

* Add DEB builder for Ubuntu 16.10 Yakkety Yak [#27993](https://github.com/docker/docker/pull/27993)
* Add RPM builder for Fedora 25 [#28222](https://github.com/docker/docker/pull/28222)
* Add `make deb` support for aarch64 [#27625](https://github.com/docker/docker/pull/27625)

### [Distribution](#distribution)

* Update notary dependency to 0.4.2 (full changelogs [here](https://github.com/docker/notary/releases/tag/v0.4.2)) [#27074](https://github.com/docker/docker/pull/27074)

  * Support for compilation on windows [docker/notary#970](https://github.com/docker/notary/pull/970)
  * Improved error messages for client authentication errors [docker/notary#972](https://github.com/docker/notary/pull/972)
  * Support for finding keys that are anywhere in the `~/.docker/trust/private` directory, not just under `~/.docker/trust/private/root_keys` or `~/.docker/trust/private/tuf_keys` [docker/notary#981](https://github.com/docker/notary/pull/981)
  * Previously, on any error updating, the client would fall back on the cache. Now we only do so if there is a network error or if the server is unavailable or missing the TUF data. Invalid TUF data will cause the update to fail - for example if there was an invalid root rotation. [docker/notary#982](https://github.com/docker/notary/pull/982)
  * Improve root validation and yubikey debug logging [docker/notary#858](https://github.com/docker/notary/pull/858) [docker/notary#891](https://github.com/docker/notary/pull/891)
  * Warn if certificates for root or delegations are near expiry [docker/notary#802](https://github.com/docker/notary/pull/802)
  * Warn if role metadata is near expiry [docker/notary#786](https://github.com/docker/notary/pull/786)
  * Fix passphrase retrieval attempt counting and terminal detection [docker/notary#906](https://github.com/docker/notary/pull/906)

- Avoid unnecessary blob uploads when different users push same layers to authenticated registry [#26564](https://github.com/docker/docker/pull/26564)

* Allow external storage for registry credentials [#26354](https://github.com/docker/docker/pull/26354)

### [Logging](#logging)

* Standardize the default logging tag value in all logging drivers [#22911](https://github.com/docker/docker/pull/22911)

- Improve performance and memory use when logging of long log lines [#22982](https://github.com/docker/docker/pull/22982)

* Enable syslog driver for windows [#25736](https://github.com/docker/docker/pull/25736)
* Add Logentries Driver [#27471](https://github.com/docker/docker/pull/27471)
* Update of AWS log driver to support tags [#27707](https://github.com/docker/docker/pull/27707)
* Unix socket support for fluentd [#26088](https://github.com/docker/docker/pull/26088)

- Enable fluentd logging driver on Windows [#28189](https://github.com/docker/docker/pull/28189)

* Sanitize docker labels when used as journald field names [#23725](https://github.com/docker/docker/pull/23725)
* Fix an issue where `docker logs --tail` returned less lines than expected [#28203](https://github.com/docker/docker/pull/28203)
* Splunk Logging Driver: performance and reliability improvements [#26207](https://github.com/docker/docker/pull/26207)
* Splunk Logging Driver: configurable formats and skip for verifying connection [#25786](https://github.com/docker/docker/pull/25786)

### [Networking](#networking)

* Add `--attachable` network support to enable `docker run` to work in swarm-mode overlay network [#25962](https://github.com/docker/docker/pull/25962)
* Add support for host port PublishMode in services using the `--publish` option in `docker service create` [#27917](https://github.com/docker/docker/pull/27917) and [#28943](https://github.com/docker/docker/pull/28943)
* Add support for Windows server 2016 overlay network driver (requires upcoming ws2016 update) [#28182](https://github.com/docker/docker/pull/28182)

- Change the default `FORWARD` policy to `DROP` [#28257](https://github.com/docker/docker/pull/28257)

* Add support for specifying static IP addresses for predefined network on windows [#22208](https://github.com/docker/docker/pull/22208)

- Fix `--publish` flag on `docker run` not working with IPv6 addresses [#27860](https://github.com/docker/docker/pull/27860)
- Fix inspect network show gateway with mask [#25564](https://github.com/docker/docker/pull/25564)
- Fix an issue where multiple addresses in a bridge may cause `--fixed-cidr` to not have the correct addresses [#26659](https://github.com/docker/docker/pull/26659)

* Add creation timestamp to `docker network inspect` [#26130](https://github.com/docker/docker/pull/26130)

- Show peer nodes in `docker network inspect` for swarm overlay networks [#28078](https://github.com/docker/docker/pull/28078)
- Enable ping for service VIP address [#28019](https://github.com/docker/docker/pull/28019)

### [Plugins](#plugins-1)

* Move plugins out of experimental [#28226](https://github.com/docker/docker/pull/28226)
* Add `--force` on `docker plugin remove` [#25096](https://github.com/docker/docker/pull/25096)

- Add support for dynamically reloading authorization plugins [#22770](https://github.com/docker/docker/pull/22770)

* Add description in `docker plugin ls` [#25556](https://github.com/docker/docker/pull/25556)
* Add `-f`/`--format` to `docker plugin inspect` [#25990](https://github.com/docker/docker/pull/25990)
* Add `docker plugin create` command [#28164](https://github.com/docker/docker/pull/28164)

- Send request's TLS peer certificates to authorization plugins [#27383](https://github.com/docker/docker/pull/27383)
- Support for global-scoped network and ipam plugins in swarm-mode [#27287](https://github.com/docker/docker/pull/27287)
- Split `docker plugin install` into two API call `/privileges` and `/pull` [#28963](https://github.com/docker/docker/pull/28963)

### [Remote API (v1.25) & Client](#remote-api-v125--client)

* Support `docker stack deploy` from a Compose file [#27998](https://github.com/docker/docker/pull/27998)
* (experimental) Implement checkpoint and restore [#22049](https://github.com/docker/docker/pull/22049)
* Add `--format` flag to `docker info` [#23808](https://github.com/docker/docker/pull/23808)

- Remove `--name` from `docker volume create` [#23830](https://github.com/docker/docker/pull/23830)

* Add `docker stack ls` [#23886](https://github.com/docker/docker/pull/23886)
* Add a new `is-task` ps filter [#24411](https://github.com/docker/docker/pull/24411)
* Add `--env-file` flag to `docker service create` [#24844](https://github.com/docker/docker/pull/24844)
* Add `--format` on `docker stats` [#24987](https://github.com/docker/docker/pull/24987)
* Make `docker node ps` default to `self` in swarm node [#25214](https://github.com/docker/docker/pull/25214)
* Add `--group` in `docker service create` [#25317](https://github.com/docker/docker/pull/25317)
* Add `--no-trunc` to service/node/stack ps output [#25337](https://github.com/docker/docker/pull/25337)
* Add Logs to `ContainerAttachOptions` so go clients can request to retrieve container logs as part of the attach process [#26718](https://github.com/docker/docker/pull/26718)
* Allow client to talk to an older server [#27745](https://github.com/docker/docker/pull/27745)

- Inform user client-side that a container removal is in progress [#26074](https://github.com/docker/docker/pull/26074)

* Add `Isolation` to the /info endpoint [#26255](https://github.com/docker/docker/pull/26255)
* Add `userns` to the /info endpoint [#27840](https://github.com/docker/docker/pull/27840)

- Do not allow more than one mode be requested at once in the services endpoint [#26643](https://github.com/docker/docker/pull/26643)

* Add capability to /containers/create API to specify mounts in a more granular and safer way [#22373](https://github.com/docker/docker/pull/22373)
* Add `--format` flag to `network ls` and `volume ls` [#23475](https://github.com/docker/docker/pull/23475)

- Allow the top-level `docker inspect` command to inspect any kind of resource [#23614](https://github.com/docker/docker/pull/23614)

* Add --cpus flag to control cpu resources for `docker run` and `docker create`, and add `NanoCPUs` to `HostConfig` [#27958](https://github.com/docker/docker/pull/27958)

- Allow unsetting the `--entrypoint` in `docker run` or `docker create` [#23718](https://github.com/docker/docker/pull/23718)

* Restructure CLI commands by adding `docker image` and `docker container` commands for more consistency [#26025](https://github.com/docker/docker/pull/26025)

- Remove `COMMAND` column from `service ls` output [#28029](https://github.com/docker/docker/pull/28029)

* Add `--format` to `docker events` [#26268](https://github.com/docker/docker/pull/26268)

- Allow specifying multiple nodes on `docker node ps` [#26299](https://github.com/docker/docker/pull/26299)
- Restrict fractional digits to 2 decimals in `docker images` output [#26303](https://github.com/docker/docker/pull/26303)

* Add `--dns-option` to `docker run` [#28186](https://github.com/docker/docker/pull/28186)
* Add Image ID to container commit event [#28128](https://github.com/docker/docker/pull/28128)
* Add external binaries version to docker info [#27955](https://github.com/docker/docker/pull/27955)
* Add information for `Manager Addresses` in the output of `docker info` [#28042](https://github.com/docker/docker/pull/28042)
* Add a new reference filter for `docker images` [#27872](https://github.com/docker/docker/pull/27872)

### [Runtime](#runtime-1)

* Add `--experimental` daemon flag to enable experimental features, instead of shipping them in a separate build [#27223](https://github.com/docker/docker/pull/27223)
* Add a `--shutdown-timeout` daemon flag to specify the default timeout (in seconds) to stop containers gracefully before daemon exit [#23036](https://github.com/docker/docker/pull/23036)
* Add `--stop-timeout` to specify the timeout value (in seconds) for individual containers to stop [#22566](https://github.com/docker/docker/pull/22566)
* Add a new daemon flag `--userland-proxy-path` to allow configuring the userland proxy instead of using the hardcoded `docker-proxy` from `$PATH` [#26882](https://github.com/docker/docker/pull/26882)
* Add boolean flag `--init` on `dockerd` and on `docker run` to use [tini](https://github.com/krallin/tini) a zombie-reaping init process as PID 1 [#26061](https://github.com/docker/docker/pull/26061) [#28037](https://github.com/docker/docker/pull/28037)
* Add a new daemon flag `--init-path` to allow configuring the path to the `docker-init` binary [#26941](https://github.com/docker/docker/pull/26941)
* Add support for live reloading insecure registry in configuration [#22337](https://github.com/docker/docker/pull/22337)
* Add support for storage-opt size on Windows daemons [#23391](https://github.com/docker/docker/pull/23391)

- Improve reliability of `docker run --rm` by moving it from the client to the daemon [#20848](https://github.com/docker/docker/pull/20848)

* Add support for `--cpu-rt-period` and `--cpu-rt-runtime` flags, allowing containers to run real-time threads when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel [#23430](https://github.com/docker/docker/pull/23430)

- Allow parallel stop, pause, unpause [#24761](https://github.com/docker/docker/pull/24761) / [#26778](https://github.com/docker/docker/pull/26778)
- Implement XFS quota for overlay2 [#24771](https://github.com/docker/docker/pull/24771)

* Fix partial/full filter issue in `service tasks --filter` [#24850](https://github.com/docker/docker/pull/24850)
* Allow engine to run inside a user namespace [#25672](https://github.com/docker/docker/pull/25672)
* Fix a race condition between device deferred removal and resume device, when using the devicemapper graphdriver [#23497](https://github.com/docker/docker/pull/23497)
* Add `docker stats` support in Windows [#25737](https://github.com/docker/docker/pull/25737)
* Allow using `--pid=host` and `--net=host` when `--userns=host` [#25771](https://github.com/docker/docker/pull/25771)

- (experimental) Add metrics (Prometheus) output for basic `container`, `image`, and `daemon` operations [#25820](https://github.com/docker/docker/pull/25820)

* Fix issue in `docker stats` with `NetworkDisabled=true` [#25905](https://github.com/docker/docker/pull/25905)

- Add `docker top` support in Windows [#25891](https://github.com/docker/docker/pull/25891)
- Record pid of exec'd process [#27470](https://github.com/docker/docker/pull/27470)
- Add support for looking up user/groups via `getent` [#27599](https://github.com/docker/docker/pull/27599)
- Add new `docker system` command with `df` and `prune` subcommands for system resource management, as well as `docker {container,image,volume,network} prune` subcommands [#26108](https://github.com/docker/docker/pull/26108) [#27525](https://github.com/docker/docker/pull/27525) / [#27525](https://github.com/docker/docker/pull/27525)

* Fix an issue where containers could not be stopped or killed by setting xfs max\_retries to 0 upon ENOSPC with devicemapper [#26212](https://github.com/docker/docker/pull/26212)
* Fix `docker cp` failing to copy to a container's volume dir on CentOS with devicemapper [#28047](https://github.com/docker/docker/pull/28047)

- Promote overlay(2) graphdriver [#27932](https://github.com/docker/docker/pull/27932)

* Add `--seccomp-profile` daemon flag to specify a path to a seccomp profile that overrides the default [#26276](https://github.com/docker/docker/pull/26276)

- Fix ulimits in `docker inspect` when `--default-ulimit` is set on daemon [#26405](https://github.com/docker/docker/pull/26405)
- Add workaround for overlay issues during build in older kernels [#28138](https://github.com/docker/docker/pull/28138)

* Add `TERM` environment variable on `docker exec -t` [#26461](https://github.com/docker/docker/pull/26461)

- Honor a container’s `--stop-signal` setting upon `docker kill` [#26464](https://github.com/docker/docker/pull/26464)

### [Swarm Mode](#swarm-mode)

* Add secret management [#27794](https://github.com/docker/docker/pull/27794)
* Add support for templating service options (hostname, mounts, and environment variables) [#28025](https://github.com/docker/docker/pull/28025)

- Display the endpoint mode in the output of `docker service inspect --pretty` [#26906](https://github.com/docker/docker/pull/26906)
- Make `docker service ps` output more bearable by shortening service IDs in task names [#28088](https://github.com/docker/docker/pull/28088)
- Make `docker node ps` default to the current node [#25214](https://github.com/docker/docker/pull/25214)

* Add `--dns`, -`-dns-opt`, and `--dns-search` to service create. [#27567](https://github.com/docker/docker/pull/27567)
* Add `--force` to `docker service update` [#27596](https://github.com/docker/docker/pull/27596)
* Add `--health-*` and `--no-healthcheck` flags to `docker service create` and `docker service update` [#27369](https://github.com/docker/docker/pull/27369)
* Add `-q` to `docker service ps` [#27654](https://github.com/docker/docker/pull/27654)

- Display number of global services in `docker service ls` [#27710](https://github.com/docker/docker/pull/27710)

* Remove `--name` flag from `docker service update`. This flag is only functional on `docker service create`, so was removed from the `update` command [#26988](https://github.com/docker/docker/pull/26988)
* Fix worker nodes failing to recover because of transient networking issues [#26646](https://github.com/docker/docker/issues/26646)

- Add support for health aware load balancing and DNS records [#27279](https://github.com/docker/docker/pull/27279)

* Add `--hostname` to `docker service create` [#27857](https://github.com/docker/docker/pull/27857)
* Add `--host` to `docker service create`, and `--host-add`, `--host-rm` to `docker service update` [#28031](https://github.com/docker/docker/pull/28031)
* Add `--tty` flag to `docker service create`/`update` [#28076](https://github.com/docker/docker/pull/28076)

- Autodetect, store, and expose node IP address as seen by the manager [#27910](https://github.com/docker/docker/pull/27910)
- Encryption at rest of manager keys and raft data [#27967](https://github.com/docker/docker/pull/27967)

* Add `--update-max-failure-ratio`, `--update-monitor` and `--rollback` flags to `docker service update` [#26421](https://github.com/docker/docker/pull/26421)

- Fix an issue with address autodiscovery on `docker swarm init` running inside a container [#26457](https://github.com/docker/docker/pull/26457)

* (experimental) Add `docker service logs` command to view logs for a service [#28089](https://github.com/docker/docker/pull/28089)
* Pin images by digest for `docker service create` and `update` [#28173](https://github.com/docker/docker/pull/28173)

- Add short (`-f`) flag for `docker node rm --force` and `docker swarm leave --force` [#28196](https://github.com/docker/docker/pull/28196)

* Add options to customize Raft snapshots (`--max-snapshots`, `--snapshot-interval`) [#27997](https://github.com/docker/docker/pull/27997)

- Don't repull image if pinned by digest [#28265](https://github.com/docker/docker/pull/28265)

* Swarm-mode support for Windows [#27838](https://github.com/docker/docker/pull/27838)
* Allow hostname to be updated on service [#28771](https://github.com/docker/docker/pull/28771)
* Support v2 plugins [#29433](https://github.com/docker/docker/pull/29433)
* Add content trust for services [#29469](https://github.com/docker/docker/pull/29469)

### [Volume](#volume)

* Add support for labels on volumes [#21270](https://github.com/docker/docker/pull/21270)
* Add support for filtering volumes by label [#25628](https://github.com/docker/docker/pull/25628)

- Add a `--force` flag in `docker volume rm` to forcefully purge the data of the volume that has already been deleted [#23436](https://github.com/docker/docker/pull/23436)
- Enhance `docker volume inspect` to show all options used when creating the volume [#26671](https://github.com/docker/docker/pull/26671)
- Add support for local NFS volumes to resolve hostnames [#27329](https://github.com/docker/docker/pull/27329)

### [Security](#security)

* Fix selinux labeling of volumes shared in a container [#23024](https://github.com/docker/docker/pull/23024)
* Prohibit `/sys/firmware/**` from being accessed with apparmor [#26618](https://github.com/docker/docker/pull/26618)

### [Deprecation](#deprecation)

* Marked the `docker daemon` command as deprecated. The daemon is moved to a separate binary (`dockerd`), and should be used instead [#26834](https://github.com/docker/docker/pull/26834)
* Deprecate unversioned API endpoints [#28208](https://github.com/docker/docker/pull/28208)
* Remove Ubuntu 15.10 (Wily Werewolf) as supported platform. Ubuntu 15.10 is EOL, and no longer receives updates [#27042](https://github.com/docker/docker/pull/27042)
* Remove Fedora 22 as supported platform. Fedora 22 is EOL, and no longer receives updates [#27432](https://github.com/docker/docker/pull/27432)
* Remove Fedora 23 as supported platform. Fedora 23 is EOL, and no longer receives updates [#29455](https://github.com/docker/docker/pull/29455)
* Deprecate the `repo:shortid` syntax on `docker pull` [#27207](https://github.com/docker/docker/pull/27207)
* Deprecate backing filesystem without `d_type` for overlay and overlay2 storage drivers [#27433](https://github.com/docker/docker/pull/27433)
* Deprecate `MAINTAINER` in Dockerfile [#25466](https://github.com/docker/docker/pull/25466)
* Deprecate `filter` param for endpoint `/images/json` [#27872](https://github.com/docker/docker/pull/27872)
* Deprecate setting duplicate engine labels [#24533](https://github.com/docker/docker/pull/24533)
* Deprecate "top-level" network information in `NetworkSettings` [#28437](https://github.com/docker/docker/pull/28437)

## [1.12.6 (2017-01-10)](#1126-2017-01-10)

> Important
>
> Docker 1.12 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the `docker service` if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

> Note
>
> Docker 1.12.5 will correctly validate that either an IPv6 subnet is provided or that the IPAM driver can provide one when you specify the `--ipv6` option.

If you are currently using the `--ipv6` option *without* specifying the `--fixed-cidr-v6` option, the Docker daemon will refuse to start with the following message:

```text
Error starting daemon: Error initializing network controller: Error creating
                       default "bridge" network: failed to parse pool request
                       for address space "LocalDefault" pool " subpool ":
                       could not find an available, non-overlapping IPv6 address
                       pool among the defaults to assign to the network
```

To resolve this error, either remove the `--ipv6` flag (to preserve the same behavior as in Docker 1.12.3 and earlier), or provide an IPv6 subnet as the value of the `--fixed-cidr-v6` flag.

In a similar way, if you specify the `--ipv6` flag when creating a network with the default IPAM driver, without providing an IPv6 `--subnet`, network creation will fail with the following message:

```text
Error response from daemon: failed to parse pool request for address space
                            "LocalDefault" pool "" subpool "": could not find an
                            available, non-overlapping IPv6 address pool among
                            the defaults to assign to the network
```

To resolve this, either remove the `--ipv6` flag (to preserve the same behavior as in Docker 1.12.3 and earlier), or provide an IPv6 subnet as the value of the `--subnet` flag.

The network creation will instead succeed if you use an external IPAM driver which supports automatic allocation of IPv6 subnets.

### [Runtime](#runtime-2)

* Fix runC privilege escalation (CVE-2016-9962)

## [1.12.5 (2016-12-15)](#1125-2016-12-15)

> Important
>
> Docker 1.12 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the `docker service` if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

> Note
>
> Docker 1.12.5 will correctly validate that either an IPv6 subnet is provided or that the IPAM driver can provide one when you specify the `--ipv6` option.

If you are currently using the `--ipv6` option *without* specifying the `--fixed-cidr-v6` option, the Docker daemon will refuse to start with the following message:

```text
Error starting daemon: Error initializing network controller: Error creating
                       default "bridge" network: failed to parse pool request
                       for address space "LocalDefault" pool " subpool ":
                       could not find an available, non-overlapping IPv6 address
                       pool among the defaults to assign to the network
```

To resolve this error, either remove the `--ipv6` flag (to preserve the same behavior as in Docker 1.12.3 and earlier), or provide an IPv6 subnet as the value of the `--fixed-cidr-v6` flag.

In a similar way, if you specify the `--ipv6` flag when creating a network with the default IPAM driver, without providing an IPv6 `--subnet`, network creation will fail with the following message:

```text
Error response from daemon: failed to parse pool request for address space
                            "LocalDefault" pool "" subpool "": could not find an
                            available, non-overlapping IPv6 address pool among
                            the defaults to assign to the network
```

To resolve this, either remove the `--ipv6` flag (to preserve the same behavior as in Docker 1.12.3 and earlier), or provide an IPv6 subnet as the value of the `--subnet` flag.

The network network creation will instead succeed if you use an external IPAM driver which supports automatic allocation of IPv6 subnets.

### [Runtime](#runtime-3)

* Fix race on sending stdin close event [#29424](https://github.com/docker/docker/pull/29424)

### [Networking](#networking-1)

* Fix panic in docker network ls when a network was created with `--ipv6` and no ipv6 `--subnet` in older docker versions [#29416](https://github.com/docker/docker/pull/29416)

### [Contrib](#contrib-2)

* Fix compilation on Darwin [#29370](https://github.com/docker/docker/pull/29370)

## [1.12.4 (2016-12-12)](#1124-2016-12-12)

> Important
>
> Docker 1.12 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the `docker service` if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

### [Runtime](#runtime-4)

* Fix issue where volume metadata was not removed [#29083](https://github.com/docker/docker/pull/29083)
* Asynchronously close streams to prevent holding container lock [#29050](https://github.com/docker/docker/pull/29050)
* Fix selinux labels for newly created container volumes [#29050](https://github.com/docker/docker/pull/29050)
* Remove hostname validation [#28990](https://github.com/docker/docker/pull/28990)
* Fix deadlocks caused by IO races [#29095](https://github.com/docker/docker/pull/29095) [#29141](https://github.com/docker/docker/pull/29141)
* Return an empty stats if the container is restarting [#29150](https://github.com/docker/docker/pull/29150)
* Fix volume store locking [#29151](https://github.com/docker/docker/pull/29151)
* Ensure consistent status code in API [#29150](https://github.com/docker/docker/pull/29150)
* Fix incorrect opaque directory permission in overlay2 [#29093](https://github.com/docker/docker/pull/29093)
* Detect plugin content and error out on `docker pull` [#29297](https://github.com/docker/docker/pull/29297)

### [Swarm Mode](#swarm-mode-1)

* Update Swarmkit [#29047](https://github.com/docker/docker/pull/29047)

  * orchestrator/global: Fix deadlock on updates [docker/swarmkit#1760](https://github.com/docker/swarmkit/pull/1760)
  * on leader switchover preserve the vxlan id for existing networks [docker/swarmkit#1773](https://github.com/docker/swarmkit/pull/1773)

- Refuse swarm spec not named "default" [#29152](https://github.com/docker/docker/pull/29152)

### [Networking](#networking-2)

* Update libnetwork [#29004](https://github.com/docker/docker/pull/29004) [#29146](https://github.com/docker/docker/pull/29146)

  * Fix panic in embedded DNS [docker/libnetwork#1561](https://github.com/docker/libnetwork/pull/1561)
  * Fix unmarhalling panic when passing --link-local-ip on global scope network [docker/libnetwork#1564](https://github.com/docker/libnetwork/pull/1564)
  * Fix panic when network plugin returns nil StaticRoutes [docker/libnetwork#1563](https://github.com/docker/libnetwork/pull/1563)
  * Fix panic in `osl.(*networkNamespace).DeleteNeighbor` [docker/libnetwork#1555](https://github.com/docker/libnetwork/pull/1555)
  * Fix panic in swarm networking concurrent map read/write [docker/libnetwork#1570](https://github.com/docker/libnetwork/pull/1570)

  - Allow encrypted networks when running docker inside a container [docker/libnetwork#1502](https://github.com/docker/libnetwork/pull/1502)

  * Do not block autoallocation of IPv6 pool [docker/libnetwork#1538](https://github.com/docker/libnetwork/pull/1538)
  * Set timeout for netlink calls [docker/libnetwork#1557](https://github.com/docker/libnetwork/pull/1557)
  * Increase networking local store timeout to one minute [docker/libkv#140](https://github.com/docker/libkv/pull/140)
  * Fix a panic in `libnetwork.(*sandbox).execFunc` [docker/libnetwork#1556](https://github.com/docker/libnetwork/pull/1556)
  * Honor icc=false for internal networks [docker/libnetwork#1525](https://github.com/docker/libnetwork/pull/1525)

### [Logging](#logging-1)

* Update syslog log driver [#29150](https://github.com/docker/docker/pull/29150)

### [Contrib](#contrib-3)

* Run "dnf upgrade" before installing in fedora [#29150](https://github.com/docker/docker/pull/29150)
* Add build-date back to RPM packages [#29150](https://github.com/docker/docker/pull/29150)
* deb package filename changed to include distribution to distinguish between distribution code names [#27829](https://github.com/docker/docker/pull/27829)

## [1.12.3 (2016-10-26)](#1123-2016-10-26)

> Important
>
> Docker 1.12 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the Docker service if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

### [Runtime](#runtime-5)

* Fix ambient capability usage in containers (CVE-2016-8867) [#27610](https://github.com/docker/docker/pull/27610)
* Prevent a deadlock in libcontainerd for Windows [#27136](https://github.com/docker/docker/pull/27136)
* Fix error reporting in CopyFileWithTar [#27075](https://github.com/docker/docker/pull/27075)

- Reset health status to starting when a container is restarted [#27387](https://github.com/docker/docker/pull/27387)
- Properly handle shared mount propagation in storage directory [#27609](https://github.com/docker/docker/pull/27609)

* Fix docker exec [#27610](https://github.com/docker/docker/pull/27610)
* Fix backward compatibility with containerd’s events log [#27693](https://github.com/docker/docker/pull/27693)

### [Swarm Mode](#swarm-mode-2)

* Fix conversion of restart-policy [#27062](https://github.com/docker/docker/pull/27062)

- Update Swarmkit [#27554](https://github.com/docker/docker/pull/27554)
- Avoid restarting a task that has already been restarted [docker/swarmkit#1305](https://github.com/docker/swarmkit/pull/1305)
- Allow duplicate published ports when they use different protocols [docker/swarmkit#1632](https://github.com/docker/swarmkit/pull/1632)
- Allow multiple randomly assigned published ports on service [docker/swarmkit#1657](https://github.com/docker/swarmkit/pull/1657)

* Fix panic when allocations happen at init time [docker/swarmkit#1651](https://github.com/docker/swarmkit/pull/1651)

### [Networking](#networking-3)

* Update libnetwork [#27559](https://github.com/docker/docker/pull/27559)

- Fix race in serializing sandbox to string [docker/libnetwork#1495](https://github.com/docker/libnetwork/pull/1495)
- Fix race during deletion [docker/libnetwork#1503](https://github.com/docker/libnetwork/pull/1503)

* Reset endpoint port info on connectivity revoke in bridge driver [docker/libnetwork#1504](https://github.com/docker/libnetwork/pull/1504)

- Fix a deadlock in networking code [docker/libnetwork#1507](https://github.com/docker/libnetwork/pull/1507)
- Fix a race in load balancer state [docker/libnetwork#1512](https://github.com/docker/libnetwork/pull/1512)

### [Logging](#logging-2)

* Update fluent-logger-golang to v1.2.1 [#27474](https://github.com/docker/docker/pull/27474)

### [Contrib](#contrib-4)

* Update buildtags for armhf ubuntu-trusty [#27327](https://github.com/docker/docker/pull/27327)
* Add AppArmor to runc buildtags for armhf [#27421](https://github.com/docker/docker/pull/27421)

## [1.12.2 (2016-10-11)](#1122-2016-10-11)

> Important
>
> Docker 1.12 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the `docker service` if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

### [Runtime](#runtime-6)

* Fix a panic due to a race condition filtering `docker ps` [#26049](https://github.com/docker/docker/pull/26049)

- Implement retry logic to prevent "Unable to remove filesystem" errors when using the aufs storage driver [#26536](https://github.com/docker/docker/pull/26536)
- Prevent devicemapper from removing device symlinks if `dm.use_deferred_removal` is enabled [#24740](https://github.com/docker/docker/pull/24740)

* Fix an issue where the CLI did not return correct exit codes if a command was run with invalid options [#26777](https://github.com/docker/docker/pull/26777)
* Fix a panic due to a bug in stdout / stderr processing in health checks [#26507](https://github.com/docker/docker/pull/26507)
* Fix exec's children handling [#26874](https://github.com/docker/docker/pull/26874)
* Fix exec form of HEALTHCHECK CMD [#26208](https://github.com/docker/docker/pull/26208)

### [Networking](#networking-4)

* Fix a daemon start panic on armv5 [#24315](https://github.com/docker/docker/issues/24315)

- Vendor libnetwork [#26879](https://github.com/docker/docker/pull/26879) [#26953](https://github.com/docker/docker/pull/26953)
- Avoid returning early on agent join failures [docker/libnetwork#1473](https://github.com/docker/libnetwork/pull/1473)

* Fix service published port cleanup issues [docker/libetwork#1432](https://github.com/docker/libnetwork/pull/1432) [docker/libnetwork#1433](https://github.com/docker/libnetwork/pull/1433)

- Recover properly from transient gossip failures [docker/libnetwork#1446](https://github.com/docker/libnetwork/pull/1446)
- Disambiguate node names known to gossip cluster to avoid node name collision [docker/libnetwork#1451](https://github.com/docker/libnetwork/pull/1451)
- Honor user provided listen address for gossip [docker/libnetwork#1460](https://github.com/docker/libnetwork/pull/1460)
- Allow reachability via published port across services on the same host [docker/libnetwork#1398](https://github.com/docker/libnetwork/pull/1398)
- Change the ingress sandbox name from random id to just `ingress_sbox` [docker/libnetwork#1449](https://github.com/docker/libnetwork/pull/1449)

* Disable service discovery in ingress network [docker/libnetwork#1489](https://github.com/docker/libnetwork/pull/1489)

### [Swarm Mode](#swarm-mode-3)

* Fix remote detection of a node's address when it joins the cluster [#26211](https://github.com/docker/docker/pull/26211)
* Vendor SwarmKit [#26765](https://github.com/docker/docker/pull/26765)
* Bounce session after failed status update [docker/swarmkit#1539](https://github.com/docker/swarmkit/pull/1539)

- Fix possible raft deadlocks [docker/swarmkit#1537](https://github.com/docker/swarmkit/pull/1537)
- Fix panic and endpoint leak when a service is updated with no endpoints [docker/swarmkit#1481](https://github.com/docker/swarmkit/pull/1481)

* Produce an error if the same port is published twice on `service create` or `service update` [docker/swarmkit#1495](https://github.com/docker/swarmkit/pull/1495)

- Fix an issue where changes to a service were not detected, resulting in the service not being updated [docker/swarmkit#1497](https://github.com/docker/swarmkit/pull/1497)
- Do not allow service creation on ingress network [docker/swarmkit#1600](https://github.com/docker/swarmkit/pull/1600)

### [Contrib](#contrib-5)

* Update the debian sysv-init script to use `dockerd` instead of `docker daemon` [#25869](https://github.com/docker/docker/pull/25869)
* Improve stability when running the docker client on MacOS Sierra [#26875](https://github.com/docker/docker/pull/26875)

- Fix installation on debian stretch [#27184](https://github.com/docker/docker/pull/27184)

### [Windows](#windows-1)

* Fix an issue where arrow-navigation did not work when running the docker client in ConEmu [#25578](https://github.com/docker/docker/pull/25578)

## [1.12.1 (2016-08-18)](#1121-2016-08-18)

> Important
>
> Docker 1.12 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the `docker service` if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

### [Client](#client)

* Add `Joined at` information in `node inspect --pretty` [#25512](https://github.com/docker/docker/pull/25512)

- Fix a crash on `service inspect` [#25454](https://github.com/docker/docker/pull/25454)
- Fix issue preventing `service update --env-add` to work as intended [#25427](https://github.com/docker/docker/pull/25427)
- Fix issue preventing `service update --publish-add` to work as intended [#25428](https://github.com/docker/docker/pull/25428)
- Remove `service update --network-add` and `service update --network-rm` flags because this feature is not yet implemented in 1.12, but was inadvertently added to the client in 1.12.0 [#25646](https://github.com/docker/docker/pull/25646)

### [Contrib](#contrib-6)

* Official ARM installation for Debian Jessie, Ubuntu Trusty, and Raspbian Jessie [#24815](https://github.com/docker/docker/pull/24815) [#25591](https://github.com/docker/docker/pull/25637)

- Add selinux policy per distribution/version, fixing issue preventing successful installation on Fedora 24, and Oracle Linux [#25334](https://github.com/docker/docker/pull/25334) [#25593](https://github.com/docker/docker/pull/25593)

### [Networking](#networking-5)

* Fix issue that prevented containers to be accessed by hostname with Docker overlay driver in Swarm Mode [#25603](https://github.com/docker/docker/pull/25603) [#25648](https://github.com/docker/docker/pull/25648)
* Fix random network issues on service with published port [#25603](https://github.com/docker/docker/pull/25603)
* Fix unreliable inter-service communication after scaling down and up [#25603](https://github.com/docker/docker/pull/25603)
* Fix issue where removing all tasks on a node and adding them back breaks connectivity with other services [#25603](https://github.com/docker/docker/pull/25603)
* Fix issue where a task that fails to start results in a race, causing a `network xxx not found` error that masks the actual error [#25550](https://github.com/docker/docker/pull/25550)
* Relax validation of SRV records for external services that use SRV records not formatted according to RFC 2782 [#25739](https://github.com/docker/docker/pull/25739)

### [Plugins (experimental)](#plugins-experimental)

* Make daemon events listen for plugin lifecycle events [#24760](https://github.com/docker/docker/pull/24760)
* Check for plugin state before enabling plugin [#25033](https://github.com/docker/docker/pull/25033)

- Remove plugin root from filesystem on `plugin rm` [#25187](https://github.com/docker/docker/pull/25187)
- Prevent deadlock when more than one plugin is installed [#25384](https://github.com/docker/docker/pull/25384)

### [Runtime](#runtime-7)

* Mask join tokens in daemon logs [#25346](https://github.com/docker/docker/pull/25346)

- Fix `docker ps --filter` causing the results to no longer be sorted by creation time [#25387](https://github.com/docker/docker/pull/25387)
- Fix various crashes [#25053](https://github.com/docker/docker/pull/25053)

### [Security](#security-1)

* Add `/proc/timer_list` to the masked paths list to prevent information leak from the host [#25630](https://github.com/docker/docker/pull/25630)
* Allow systemd to run with only `--cap-add SYS_ADMIN` rather than having to also add `--cap-add DAC_READ_SEARCH` or disabling seccomp filtering [#25567](https://github.com/docker/docker/pull/25567)

### [Swarm](#swarm)

* Fix an issue where the swarm can get stuck electing a new leader after quorum is lost [#25055](https://github.com/docker/docker/issues/25055)
* Fix unwanted rescheduling of containers after a leader failover [#25017](https://github.com/docker/docker/issues/25017)
* Change swarm root CA key to P256 curve [swarmkit#1376](https://github.com/docker/swarmkit/pull/1376)
* Allow forced removal of a node from a swarm [#25159](https://github.com/docker/docker/pull/25159)
* Fix connection leak when a node leaves a swarm [swarmkit/#1277](https://github.com/docker/swarmkit/pull/1277)
* Backdate swarm certificates by one hour to tolerate more clock skew [swarmkit/#1243](https://github.com/docker/swarmkit/pull/1243)
* Avoid high CPU use with many unschedulable tasks [swarmkit/#1287](https://github.com/docker/swarmkit/pull/1287)
* Fix issue with global tasks not starting up [swarmkit/#1295](https://github.com/docker/swarmkit/pull/1295)
* Garbage collect raft logs [swarmkit/#1327](https://github.com/docker/swarmkit/pull/1327)

### [Volume](#volume-1)

* Persist local volume options after a daemon restart [#25316](https://github.com/docker/docker/pull/25316)
* Fix an issue where the mount ID was not returned on volume unmount [#25333](https://github.com/docker/docker/pull/25333)
* Fix an issue where a volume mount could inadvertently create a bind mount [#25309](https://github.com/docker/docker/pull/25309)
* `docker service create --mount type=bind,...` now correctly validates if the source path exists, instead of creating it [#25494](https://github.com/docker/docker/pull/25494)

## [1.12.0 (2016-07-28)](#1120-2016-07-28)

> Important
>
> Docker 1.12.0 ships with an updated systemd unit file for rpm based installs (which includes RHEL, Fedora, CentOS, and Oracle Linux 7). When upgrading from an older version of Docker, the upgrade process may not automatically install the updated version of the unit file, or fail to start the `docker service` if;
>
> * the systemd unit file (`/usr/lib/systemd/system/docker.service`) contains local changes, or
> * a systemd drop-in file is present, and contains `-H fd://` in the `ExecStart` directive

Starting the `docker service` will produce an error:

```
Failed to start docker.service: Unit docker.socket failed to load: No such file or directory.
```

or

```
no sockets found via socket activation: make sure the service was started by systemd.
```

To resolve this:

* Backup the current version of the unit file, and replace the file with the [version that ships with docker 1.12](https://raw.githubusercontent.com/docker/docker/v1.12.0/contrib/init/systemd/docker.service.rpm)
* Remove the `Requires=docker.socket` directive from the `/usr/lib/systemd/system/docker.service` file if present
* Remove `-H fd://` from the `ExecStart` directive (both in the main unit file, and in any drop-in files present).

After making those changes, run `sudo systemctl daemon-reload`, and `sudo systemctl restart docker` to reload changes and (re)start the docker daemon.

> Important
>
> With Docker 1.12, a Linux `docker` installation now has two additional binaries; `dockerd`, and `docker-proxy`. If you have scripts for installing `docker`, make sure to update them accordingly.

### [Builder](#builder-1)

* New `HEALTHCHECK` Dockerfile instruction to support user-defined healthchecks [#23218](https://github.com/docker/docker/pull/23218)
* New `SHELL` Dockerfile instruction to specify the default shell when using the shell form for commands in a Dockerfile [#22489](https://github.com/docker/docker/pull/22489)
* Add `#escape=` Dockerfile directive to support platform-specific parsing of file paths in Dockerfile [#22268](https://github.com/docker/docker/pull/22268)
* Add support for comments in `.dockerignore` [#23111](https://github.com/docker/docker/pull/23111)

- Support for UTF-8 in Dockerfiles [#23372](https://github.com/docker/docker/pull/23372)
- Skip UTF-8 BOM bytes from `Dockerfile` and `.dockerignore` if exist [#23234](https://github.com/docker/docker/pull/23234)
- Windows: support for `ARG` to match Linux [#22508](https://github.com/docker/docker/pull/22508)

* Fix error message when building using a daemon with the bridge network disabled [#22932](https://github.com/docker/docker/pull/22932)

### [Contrib](#contrib-7)

* Enable seccomp for Centos 7 and Oracle Linux 7 [#22344](https://github.com/docker/docker/pull/22344)

- Remove MountFlags in systemd unit to allow shared mount propagation [#22806](https://github.com/docker/docker/pull/22806)

### [Distribution](#distribution-1)

* Add `--max-concurrent-downloads` and `--max-concurrent-uploads` daemon flags useful for situations where network connections don't support multiple downloads/uploads [#22445](https://github.com/docker/docker/pull/22445)

- Registry operations now honor the `ALL_PROXY` environment variable [#22316](https://github.com/docker/docker/pull/22316)
- Provide more information to the user on `docker load` [#23377](https://github.com/docker/docker/pull/23377)
- Always save registry digest metadata about images pushed and pulled [#23996](https://github.com/docker/docker/pull/23996)

### [Logging](#logging-3)

* Syslog logging driver now supports DGRAM sockets [#21613](https://github.com/docker/docker/pull/21613)
* Add `--details` option to `docker logs` to also display log tags [#21889](https://github.com/docker/docker/pull/21889)
* Enable syslog logger to have access to env and labels [#21724](https://github.com/docker/docker/pull/21724)
* An additional syslog-format option `rfc5424micro` to allow microsecond resolution in syslog timestamp [#21844](https://github.com/docker/docker/pull/21844)

- Inherit the daemon log options when creating containers [#21153](https://github.com/docker/docker/pull/21153)
- Remove `docker/` prefix from log messages tag and replace it with `{{.DaemonName}}` so that users have the option of changing the prefix [#22384](https://github.com/docker/docker/pull/22384)

### [Networking](#networking-6)

* Built-in Virtual-IP based internal and ingress load-balancing using IPVS [#23361](https://github.com/docker/docker/pull/23361)
* Routing Mesh using ingress overlay network [#23361](https://github.com/docker/docker/pull/23361)
* Secured multi-host overlay networking using encrypted control-plane and Data-plane [#23361](https://github.com/docker/docker/pull/23361)
* MacVlan driver is out of experimental [#23524](https://github.com/docker/docker/pull/23524)
* Add `driver` filter to `network ls` [#22319](https://github.com/docker/docker/pull/22319)
* Adding `network` filter to `docker ps --filter` [#23300](https://github.com/docker/docker/pull/23300)
* Add `--link-local-ip` flag to `create`, `run` and `network connect` to specify a container's link-local address [#23415](https://github.com/docker/docker/pull/23415)
* Add network label filter support [#21495](https://github.com/docker/docker/pull/21495)

- Removed dependency on external KV-Store for Overlay networking in Swarm-Mode [#23361](https://github.com/docker/docker/pull/23361)
- Add container's short-id as default network alias [#21901](https://github.com/docker/docker/pull/21901)
- `run` options `--dns` and `--net=host` are no longer mutually exclusive [#22408](https://github.com/docker/docker/pull/22408)

* Fix DNS issue when renaming containers with generated names [#22716](https://github.com/docker/docker/pull/22716)
* Allow both `network inspect -f {{.Id}}` and `network inspect -f {{.ID}}` to address inconsistency with inspect output [#23226](https://github.com/docker/docker/pull/23226)

### [Plugins (experimental)](#plugins-experimental-1)

* New `plugin` command to manager plugins with `install`, `enable`, `disable`, `rm`, `inspect`, `set` subcommands [#23446](https://github.com/docker/docker/pull/23446)

### [Remote API (v1.24) & Client](#remote-api-v124--client)

* Split the binary into two: `docker` (client) and `dockerd` (daemon) [#20639](https://github.com/docker/docker/pull/20639)
* Add `before` and `since` filters to `docker images --filter` [#22908](https://github.com/docker/docker/pull/22908)
* Add `--limit` option to `docker search` [#23107](https://github.com/docker/docker/pull/23107)
* Add `--filter` option to `docker search` [#22369](https://github.com/docker/docker/pull/22369)
* Add security options to `docker info` output [#21172](https://github.com/docker/docker/pull/21172) [#23520](https://github.com/docker/docker/pull/23520)
* Add insecure registries to `docker info` output [#20410](https://github.com/docker/docker/pull/20410)
* Extend Docker authorization with TLS user information [#21556](https://github.com/docker/docker/pull/21556)
* devicemapper: expose Minimum Thin Pool Free Space through `docker info` [#21945](https://github.com/docker/docker/pull/21945)

- API now returns a JSON object when an error occurs making it more consistent [#22880](https://github.com/docker/docker/pull/22880)

* Prevent `docker run -i --restart` from hanging on exit [#22777](https://github.com/docker/docker/pull/22777)
* Fix API/CLI discrepancy on hostname validation [#21641](https://github.com/docker/docker/pull/21641)
* Fix discrepancy in the format of sizes in `stats` from HumanSize to BytesSize [#21773](https://github.com/docker/docker/pull/21773)
* authz: when request is denied return forbidden exit code (403) [#22448](https://github.com/docker/docker/pull/22448)
* Windows: fix tty-related displaying issues [#23878](https://github.com/docker/docker/pull/23878)

### [Runtime](#runtime-8)

* Split the userland proxy to a separate binary (`docker-proxy`) [#23312](https://github.com/docker/docker/pull/23312)
* Add `--live-restore` daemon flag to keep containers running when daemon shuts down, and regain control on startup [#23213](https://github.com/docker/docker/pull/23213)
* Ability to add OCI-compatible runtimes (via `--add-runtime` daemon flag) and select one with `--runtime` on `create` and `run` [#22983](https://github.com/docker/docker/pull/22983)
* New `overlay2` graphdriver for Linux 4.0+ with multiple lower directory support [#22126](https://github.com/docker/docker/pull/22126)
* New load/save image events [#22137](https://github.com/docker/docker/pull/22137)
* Add support for reloading daemon configuration through systemd [#22446](https://github.com/docker/docker/pull/22446)
* Add disk quota support for btrfs [#19651](https://github.com/docker/docker/pull/19651)
* Add disk quota support for zfs [#21946](https://github.com/docker/docker/pull/21946)
* Add support for `docker run --pid=container:<id>` [#22481](https://github.com/docker/docker/pull/22481)
* Align default seccomp profile with selected capabilities [#22554](https://github.com/docker/docker/pull/22554)
* Add a `daemon reload` event when the daemon reloads its configuration [#22590](https://github.com/docker/docker/pull/22590)
* Add `trace` capability in the pprof profiler to show execution traces in binary form [#22715](https://github.com/docker/docker/pull/22715)
* Add a `detach` event [#22898](https://github.com/docker/docker/pull/22898)
* Add support for setting sysctls with `--sysctl` [#19265](https://github.com/docker/docker/pull/19265)
* Add `--storage-opt` flag to `create` and `run` allowing to set `size` on devicemapper [#19367](https://github.com/docker/docker/pull/19367)
* Add `--oom-score-adjust` daemon flag with a default value of `-500` making the daemon less likely to be killed before containers [#24516](https://github.com/docker/docker/pull/24516)

- Undeprecate the `-c` short alias of `--cpu-shares` on `run`, `build`, `create`, `update` [#22621](https://github.com/docker/docker/pull/22621)
- Prevent from using aufs and overlay graphdrivers on an eCryptfs mount [#23121](https://github.com/docker/docker/pull/23121)

* Fix issues with tmpfs mount ordering [#22329](https://github.com/docker/docker/pull/22329)
* Created containers are no longer listed on `docker ps -a -f exited=0` [#21947](https://github.com/docker/docker/pull/21947)
* Fix an issue where containers are stuck in a "Removal In Progress" state [#22423](https://github.com/docker/docker/pull/22423)
* Fix bug that was returning an HTTP 500 instead of a 400 when not specifying a command on run/create [#22762](https://github.com/docker/docker/pull/22762)
* Fix bug with `--detach-keys` whereby input matching a prefix of the detach key was not preserved [#22943](https://github.com/docker/docker/pull/22943)
* SELinux labeling is now disabled when using `--privileged` mode [#22993](https://github.com/docker/docker/pull/22993)
* If volume-mounted into a container, `/etc/hosts`, `/etc/resolv.conf`, `/etc/hostname` are no longer SELinux-relabeled [#22993](https://github.com/docker/docker/pull/22993)
* Fix inconsistency in `--tmpfs` behavior regarding mount options [#22438](https://github.com/docker/docker/pull/22438)
* Fix an issue where daemon hangs at startup [#23148](https://github.com/docker/docker/pull/23148)
* Ignore SIGPIPE events to prevent journald restarts to crash docker in some cases [#22460](https://github.com/docker/docker/pull/22460)
* Containers are not removed from stats list on error [#20835](https://github.com/docker/docker/pull/20835)
* Fix `on-failure` restart policy when daemon restarts [#20853](https://github.com/docker/docker/pull/20853)
* Fix an issue with `stats` when a container is using another container's network [#21904](https://github.com/docker/docker/pull/21904)

### [Swarm Mode](#swarm-mode-4)

* New `swarm` command to manage swarms with `init`, `join`, `join-token`, `leave`, `update` subcommands [#23361](https://github.com/docker/docker/pull/23361) [#24823](https://github.com/docker/docker/pull/24823)
* New `service` command to manage swarm-wide services with `create`, `inspect`, `update`, `rm`, `ps` subcommands [#23361](https://github.com/docker/docker/pull/23361) [#25140](https://github.com/docker/docker/pull/25140)
* New `node` command to manage nodes with `accept`, `promote`, `demote`, `inspect`, `update`, `ps`, `ls` and `rm` subcommands [#23361](https://github.com/docker/docker/pull/23361) [#25140](https://github.com/docker/docker/pull/25140)
* (experimental) New `stack` and `deploy` commands to manage and deploy multi-service applications [#23522](https://github.com/docker/docker/pull/23522) [#25140](https://github.com/docker/docker/pull/25140)

### [Volume](#volume-2)

* Add support for local and global volume scopes (analogous to network scopes) [#22077](https://github.com/docker/docker/pull/22077)
* Allow volume drivers to provide a `Status` field [#21006](https://github.com/docker/docker/pull/21006)
* Add name/driver filter support for volume [#21361](https://github.com/docker/docker/pull/21361)

- Mount/Unmount operations now receives an opaque ID to allow volume drivers to differentiate between two callers [#21015](https://github.com/docker/docker/pull/21015)

* Fix issue preventing to remove a volume in a corner case [#22103](https://github.com/docker/docker/pull/22103)
* Windows: Enable auto-creation of host-path to match Linux [#22094](https://github.com/docker/docker/pull/22094)

### [Deprecation](#deprecation-1)

* Environment variables `DOCKER_CONTENT_TRUST_OFFLINE_PASSPHRASE` and `DOCKER_CONTENT_TRUST_TAGGING_PASSPHRASE` have been renamed to `DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE` and `DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE` respectively [#22574](https://github.com/docker/docker/pull/22574)
* Remove deprecated `syslog-tag`, `gelf-tag`, `fluentd-tag` log option in favor of the more generic `tag` one [#22620](https://github.com/docker/docker/pull/22620)
* Remove deprecated feature of passing HostConfig at API container start [#22570](https://github.com/docker/docker/pull/22570)
* Remove deprecated `-f`/`--force` flag on docker tag [#23090](https://github.com/docker/docker/pull/23090)
* Remove deprecated `/containers/<id|name>/copy` endpoint [#22149](https://github.com/docker/docker/pull/22149)
* Remove deprecated `docker ps` flags `--since` and `--before` [#22138](https://github.com/docker/docker/pull/22138)
* Deprecate the old 3-args form of `docker import` [#23273](https://github.com/docker/docker/pull/23273)

## [1.11.2 (2016-05-31)](#1112-2016-05-31)

### [Networking](#networking-7)

* Fix a stale endpoint issue on overlay networks during ungraceful restart ([#23015](https://github.com/docker/docker/pull/23015))
* Fix an issue where the wrong port could be reported by `docker inspect/ps/port` ([#22997](https://github.com/docker/docker/pull/22997))

### [Runtime](#runtime-9)

* Fix a potential panic when running `docker build` ([#23032](https://github.com/docker/docker/pull/23032))
* Fix interpretation of `--user` parameter ([#22998](https://github.com/docker/docker/pull/22998))
* Fix a bug preventing container statistics to be correctly reported ([#22955](https://github.com/docker/docker/pull/22955))
* Fix an issue preventing container to be restarted after daemon restart ([#22947](https://github.com/docker/docker/pull/22947))
* Fix issues when running 32 bit binaries on Ubuntu 16.04 ([#22922](https://github.com/docker/docker/pull/22922))
* Fix a possible deadlock on image deletion and container attach ([#22918](https://github.com/docker/docker/pull/22918))
* Fix an issue where containers fail to start after a daemon restart if they depend on a containerized cluster store ([#22561](https://github.com/docker/docker/pull/22561))
* Fix an issue causing `docker ps` to hang on CentOS when using devicemapper ([#22168](https://github.com/docker/docker/pull/22168), [#23067](https://github.com/docker/docker/pull/23067))
* Fix a bug preventing to `docker exec` into a container when using devicemapper ([#22168](https://github.com/docker/docker/pull/22168), [#23067](https://github.com/docker/docker/pull/23067))

## [1.11.1 (2016-04-26)](#1111-2016-04-26)

### [Distribution](#distribution-2)

* Fix schema2 manifest media type to be of type `application/vnd.docker.container.image.v1+json` ([#21949](https://github.com/docker/docker/pull/21949))

### [Documentation](#documentation)

* Add missing API documentation for changes introduced with 1.11.0 ([#22048](https://github.com/docker/docker/pull/22048))

### [Builder](#builder-2)

* Append label passed to `docker build` as arguments as an implicit `LABEL` command at the end of the processed `Dockerfile` ([#22184](https://github.com/docker/docker/pull/22184))

### [Networking](#networking-8)

* Fix a panic that would occur when forwarding DNS query ([#22261](https://github.com/docker/docker/pull/22261))
* Fix an issue where OS threads could end up within an incorrect network namespace when using user defined networks ([#22261](https://github.com/docker/docker/pull/22261))

### [Runtime](#runtime-10)

* Fix a bug preventing labels configuration to be reloaded via the config file ([#22299](https://github.com/docker/docker/pull/22299))
* Fix a regression where container mounting `/var/run` would prevent other containers from being removed ([#22256](https://github.com/docker/docker/pull/22256))
* Fix an issue where it would be impossible to update both `memory-swap` and `memory` value together ([#22255](https://github.com/docker/docker/pull/22255))
* Fix a regression from 1.11.0 where the `/auth` endpoint would not initialize `serveraddress` if it is not provided ([#22254](https://github.com/docker/docker/pull/22254))
* Add missing cleanup of container temporary files when cancelling a schedule restart ([#22237](https://github.com/docker/docker/pull/22237))
* Remove scary error message when no restart policy is specified ([#21993](https://github.com/docker/docker/pull/21993))
* Fix a panic that would occur when the plugins were activated via the json spec ([#22191](https://github.com/docker/docker/pull/22191))
* Fix restart backoff logic to correctly reset delay if container ran for at least 10secs ([#22125](https://github.com/docker/docker/pull/22125))
* Remove error message when a container restart get cancelled ([#22123](https://github.com/docker/docker/pull/22123))
* Fix an issue where `docker` would not correctly clean up after `docker exec` ([#22121](https://github.com/docker/docker/pull/22121))
* Fix a panic that could occur when serving concurrent `docker stats` commands ([#22120](https://github.com/docker/docker/pull/22120))\`
* Revert deprecation of non-existent host directories auto-creation ([#22065](https://github.com/docker/docker/pull/22065))
* Hide misleading rpc error on daemon shutdown ([#22058](https://github.com/docker/docker/pull/22058))

## [1.11.0 (2016-04-13)](#1110-2016-04-13)

> Important
>
> With Docker 1.11, a Linux Docker installation is now made of 4 binaries (`docker`, [`docker-containerd`](https://github.com/docker/containerd), [`docker-containerd-shim`](https://github.com/docker/containerd) and [`docker-runc`](https://github.com/opencontainers/runc)). If you have scripts relying on `docker` being a single static binaries, make sure to update them. Interaction with the daemon stay the same otherwise, the usage of the other binaries should be transparent. A Windows Docker installation remains a single binary, `docker.exe`.

### [Builder](#builder-3)

* Fix a bug where Docker would not use the correct uid/gid when processing the `WORKDIR` command ([#21033](https://github.com/docker/docker/pull/21033))
* Fix a bug where copy operations with userns would not use the proper uid/gid ([#20782](https://github.com/docker/docker/pull/20782), [#21162](https://github.com/docker/docker/pull/21162))

### [Client](#client-1)

* Usage of the `:` separator for security option has been deprecated. `=` should be used instead ([#21232](https://github.com/docker/docker/pull/21232))

- The client user agent is now passed to the registry on `pull`, `build`, `push`, `login` and `search` operations ([#21306](https://github.com/docker/docker/pull/21306), [#21373](https://github.com/docker/docker/pull/21373))

* Allow setting the Domainname and Hostname separately through the API ([#20200](https://github.com/docker/docker/pull/20200))
* Docker info will now warn users if it can not detect the kernel version or the operating system ([#21128](https://github.com/docker/docker/pull/21128))

- Fix an issue where `docker stats --no-stream` output could be all 0s ([#20803](https://github.com/docker/docker/pull/20803))
- Fix a bug where some newly started container would not appear in a running `docker stats` command ([#20792](https://github.com/docker/docker/pull/20792))

* Post processing is no longer enabled for linux-cgo terminals ([#20587](https://github.com/docker/docker/pull/20587))

- Values to `--hostname` are now refused if they do not comply with [RFC1123](https://tools.ietf.org/html/rfc1123) ([#20566](https://github.com/docker/docker/pull/20566))

* Docker learned how to use a SOCKS proxy ([#20366](https://github.com/docker/docker/pull/20366), [#18373](https://github.com/docker/docker/pull/18373))
* Docker now supports external credential stores ([#20107](https://github.com/docker/docker/pull/20107))

- `docker ps` now supports displaying the list of volumes mounted inside a container ([#20017](https://github.com/docker/docker/pull/20017))
- `docker info` now also reports Docker's root directory location ([#19986](https://github.com/docker/docker/pull/19986))

* Docker now prohibits login in with an empty username (spaces are trimmed) ([#19806](https://github.com/docker/docker/pull/19806))

- Docker events attributes are now sorted by key ([#19761](https://github.com/docker/docker/pull/19761))
- `docker ps` no longer shows exported port for stopped containers ([#19483](https://github.com/docker/docker/pull/19483))

* Docker now cleans after itself if a save/export command fails ([#17849](https://github.com/docker/docker/pull/17849))

- Docker load learned how to display a progress bar ([#17329](https://github.com/docker/docker/pull/17329), [#120078](https://github.com/docker/docker/pull/20078))

### [Distribution](#distribution-3)

* Fix a panic that occurred when pulling an image with 0 layers ([#21222](https://github.com/docker/docker/pull/21222))
* Fix a panic that could occur on error while pushing to a registry with a misconfigured token service ([#21212](https://github.com/docker/docker/pull/21212))

- All first-level delegation roles are now signed when doing a trusted push ([#21046](https://github.com/docker/docker/pull/21046))
- OAuth support for registries was added ([#20970](https://github.com/docker/docker/pull/20970))

* `docker login` now handles token using the implementation found in [docker/distribution](https://github.com/docker/distribution) ([#20832](https://github.com/docker/docker/pull/20832))
* `docker login` will no longer prompt for an email ([#20565](https://github.com/docker/docker/pull/20565))
* Docker will now fallback to registry V1 if no basic auth credentials are available ([#20241](https://github.com/docker/docker/pull/20241))
* Docker will now try to resume layer download where it left off after a network error/timeout ([#19840](https://github.com/docker/docker/pull/19840))

- Fix generated manifest mediaType when pushing cross-repository ([#19509](https://github.com/docker/docker/pull/19509))
- Fix docker requesting additional push credentials when pulling an image if Content Trust is enabled ([#20382](https://github.com/docker/docker/pull/20382))

### [Logging](#logging-4)

* Fix a race in the journald log driver ([#21311](https://github.com/docker/docker/pull/21311))

- Docker syslog driver now uses the RFC-5424 format when emitting logs ([#20121](https://github.com/docker/docker/pull/20121))
- Docker GELF log driver now allows to specify the compression algorithm and level via the `gelf-compression-type` and `gelf-compression-level` options ([#19831](https://github.com/docker/docker/pull/19831))
- Docker daemon learned to output uncolorized logs via the `--raw-logs` options ([#19794](https://github.com/docker/docker/pull/19794))

* Docker, on Windows platform, now includes an ETW (Event Tracing in Windows) logging driver named `etwlogs` ([#19689](https://github.com/docker/docker/pull/19689))

- Journald log driver learned how to handle tags ([#19564](https://github.com/docker/docker/pull/19564))

* The fluentd log driver learned the following options: `fluentd-address`, `fluentd-buffer-limit`, `fluentd-retry-wait`, `fluentd-max-retries` and `fluentd-async-connect` ([#19439](https://github.com/docker/docker/pull/19439))
* Docker learned to send log to Google Cloud via the new `gcplogs` logging driver. ([#18766](https://github.com/docker/docker/pull/18766))

### [Misc](#misc)

* When saving linked images together with `docker save` a subsequent `docker load` will correctly restore their parent/child relationship ([#21385](https://github.com/docker/docker/pull/21385))
* Support for building the Docker cli for OpenBSD was added ([#21325](https://github.com/docker/docker/pull/21325))
* Labels can now be applied at network, volume and image creation ([#21270](https://github.com/docker/docker/pull/21270))

- The `dockremap` is now created as a system user ([#21266](https://github.com/docker/docker/pull/21266))

* Fix a few response body leaks ([#21258](https://github.com/docker/docker/pull/21258))
* Docker, when run as a service with systemd, will now properly manage its processes cgroups ([#20633](https://github.com/docker/docker/pull/20633))

- `docker info` now reports the value of cgroup KernelMemory or emits a warning if it is not supported ([#20863](https://github.com/docker/docker/pull/20863))
- `docker info` now also reports the cgroup driver in use ([#20388](https://github.com/docker/docker/pull/20388))
- Docker completion is now available on PowerShell ([#19894](https://github.com/docker/docker/pull/19894))
- `dockerinit` is no more ([#19490](https://github.com/docker/docker/pull/19490),[#19851](https://github.com/docker/docker/pull/19851))

* Support for building Docker on arm64 was added ([#19013](https://github.com/docker/docker/pull/19013))
* Experimental support for building docker.exe in a native Windows Docker installation ([#18348](https://github.com/docker/docker/pull/18348))

### [Networking](#networking-9)

* Fix panic if a node is forcibly removed from the cluster ([#21671](https://github.com/docker/docker/pull/21671))
* Fix "error creating vxlan interface" when starting a container in a Swarm cluster ([#21671](https://github.com/docker/docker/pull/21671))

- `docker network inspect` will now report all endpoints whether they have an active container or not ([#21160](https://github.com/docker/docker/pull/21160))

* Experimental support for the MacVlan and IPVlan network drivers has been added ([#21122](https://github.com/docker/docker/pull/21122))

- Output of `docker network ls` is now sorted by network name ([#20383](https://github.com/docker/docker/pull/20383))

* Fix a bug where Docker would allow a network to be created with the reserved `default` name ([#19431](https://github.com/docker/docker/pull/19431))

- `docker network inspect` returns whether a network is internal or not ([#19357](https://github.com/docker/docker/pull/19357))

* Control IPv6 via explicit option when creating a network (`docker network create --ipv6`). This shows up as a new `EnableIPv6` field in `docker network inspect` ([#17513](https://github.com/docker/docker/pull/17513))

- Support for AAAA Records (aka IPv6 Service Discovery) in embedded DNS Server ([#21396](https://github.com/docker/docker/pull/21396))

* Fix to not forward docker domain IPv6 queries to external servers ([#21396](https://github.com/docker/docker/pull/21396))

- Multiple A/AAAA records from embedded DNS Server for DNS Round robin ([#21019](https://github.com/docker/docker/pull/21019))

* Fix endpoint count inconsistency after an ungraceful daemon restart ([#21261](https://github.com/docker/docker/pull/21261))
* Move the ownership of exposed ports and port-mapping options from Endpoint to Sandbox ([#21019](https://github.com/docker/docker/pull/21019))
* Fixed a bug which prevents docker reload when host is configured with ipv6.disable=1 ([#21019](https://github.com/docker/docker/pull/21019))
* Added inbuilt nil IPAM driver ([#21019](https://github.com/docker/docker/pull/21019))
* Fixed bug in iptables.Exists() logic [#21019](https://github.com/docker/docker/pull/21019)
* Fixed a Veth interface leak when using overlay network ([#21019](https://github.com/docker/docker/pull/21019))
* Fixed a bug which prevents docker reload after a network delete during shutdown ([#20214](https://github.com/docker/docker/pull/20214))
* Make sure iptables chains are recreated on firewalld reload ([#20419](https://github.com/docker/docker/pull/20419))
* Allow to pass global datastore during config reload ([#20419](https://github.com/docker/docker/pull/20419))
* For anonymous containers use the alias name for IP to name mapping, ie:DNS PTR record ([#21019](https://github.com/docker/docker/pull/21019))
* Fix a panic when deleting an entry from /etc/hosts file ([#21019](https://github.com/docker/docker/pull/21019))
* Source the forwarded DNS queries from the container net namespace ([#21019](https://github.com/docker/docker/pull/21019))
* Fix to retain the network internal mode config for bridge networks on daemon reload (\[#21780] (<https://github.com/docker/docker/pull/21780>))
* Fix to retain IPAM driver option configs on daemon reload (\[#21914] (<https://github.com/docker/docker/pull/21914>))

### [Plugins](#plugins-2)

* Fix a file descriptor leak that would occur every time plugins were enumerated ([#20686](https://github.com/docker/docker/pull/20686))
* Fix an issue where Authz plugin would corrupt the payload body when faced with a large amount of data ([#20602](https://github.com/docker/docker/pull/20602))

### [Runtime](#runtime-11)

* Fix a panic that could occur when cleanup after a container started with invalid parameters ([#21716](https://github.com/docker/docker/pull/21716))
* Fix a race with event timers stopping early ([#21692](https://github.com/docker/docker/pull/21692))
* Fix race conditions in the layer store, potentially corrupting the map and crashing the process ([#21677](https://github.com/docker/docker/pull/21677))
* Un-deprecate auto-creation of host directories for mounts. This feature was marked deprecated in ([#21666](https://github.com/docker/docker/pull/21666)) Docker 1.9, but was decided to be too much of a backward-incompatible change, so it was decided to keep the feature.

- It is now possible for containers to share the NET and IPC namespaces when `userns` is enabled ([#21383](https://github.com/docker/docker/pull/21383))
- `docker inspect <image-id>` will now expose the rootfs layers ([#21370](https://github.com/docker/docker/pull/21370))
- Docker Windows gained a minimal `top` implementation ([#21354](https://github.com/docker/docker/pull/21354))

* Docker learned to report the faulty exe when a container cannot be started due to its condition ([#21345](https://github.com/docker/docker/pull/21345))
* Docker with device mapper will now refuse to run if `udev sync` is not available ([#21097](https://github.com/docker/docker/pull/21097))

- Fix a bug where Docker would not validate the config file upon configuration reload ([#21089](https://github.com/docker/docker/pull/21089))
- Fix a hang that would happen on attach if initial start was to fail ([#21048](https://github.com/docker/docker/pull/21048))
- Fix an issue where registry service options in the daemon configuration file were not properly taken into account ([#21045](https://github.com/docker/docker/pull/21045))
- Fix a race between the exec and resize operations ([#21022](https://github.com/docker/docker/pull/21022))
- Fix an issue where nanoseconds were not correctly taken in account when filtering Docker events ([#21013](https://github.com/docker/docker/pull/21013))
- Fix the handling of Docker command when passed a 64 bytes id ([#21002](https://github.com/docker/docker/pull/21002))

* Docker will now return a `204` (i.e http.StatusNoContent) code when it successfully deleted a network ([#20977](https://github.com/docker/docker/pull/20977))

- Fix a bug where the daemon would wait indefinitely in case the process it was about to killed had already exited on its own ([#20967](https://github.com/docker/docker/pull/20967)

* The devmapper driver learned the `dm.min_free_space` option. If the mapped device free space reaches the passed value, new device creation will be prohibited. ([#20786](https://github.com/docker/docker/pull/20786))

- Docker can now prevent processes in container to gain new privileges via the `--security-opt=no-new-privileges` flag ([#20727](https://github.com/docker/docker/pull/20727))

* Starting a container with the `--device` option will now correctly resolves symlinks ([#20684](https://github.com/docker/docker/pull/20684))

- Docker now relies on [`containerd`](https://github.com/docker/containerd) and [`runc`](https://github.com/opencontainers/runc) to spawn containers. ([#20662](https://github.com/docker/docker/pull/20662))

* Fix docker configuration reloading to only alter value present in the given config file ([#20604](https://github.com/docker/docker/pull/20604))

- Docker now allows setting a container hostname via the `--hostname` flag when `--net=host` ([#20177](https://github.com/docker/docker/pull/20177))
- Docker now allows executing privileged container while running with `--userns-remap` if both `--privileged` and the new `--userns=host` flag are specified ([#20111](https://github.com/docker/docker/pull/20111))

* Fix Docker not cleaning up correctly old containers upon restarting after a crash ([#19679](https://github.com/docker/docker/pull/19679))

- Docker will now error out if it doesn't recognize a configuration key within the config file ([#19517](https://github.com/docker/docker/pull/19517))

* Fix container loading, on daemon startup, when they depends on a plugin running within a container ([#19500](https://github.com/docker/docker/pull/19500))

- `docker update` learned how to change a container restart policy ([#19116](https://github.com/docker/docker/pull/19116))
- `docker inspect` now also returns a new `State` field containing the container state in a human readable way (i.e. one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`)([#18966](https://github.com/docker/docker/pull/18966))

* Docker learned to limit the number of active pids (i.e. processes) within the container via the `pids-limit` flags. NOTE: This requires `CGROUP_PIDS=y` to be in the kernel configuration. ([#18697](https://github.com/docker/docker/pull/18697))

- `docker load` now has a `--quiet` option to suppress the load output ([#20078](https://github.com/docker/docker/pull/20078))
- Fix a bug in neighbor discovery for IPv6 peers ([#20842](https://github.com/docker/docker/pull/20842))
- Fix a panic during cleanup if a container was started with invalid options ([#21802](https://github.com/docker/docker/pull/21802))
- Fix a situation where a container cannot be stopped if the terminal is closed ([#21840](https://github.com/docker/docker/pull/21840))

### [Security](#security-2)

* Object with the `pcp_pmcd_t` selinux type were given management access to `/var/lib/docker(/.*)?` ([#21370](https://github.com/docker/docker/pull/21370))
* `restart_syscall`, `copy_file_range`, `mlock2` joined the list of allowed calls in the default seccomp profile ([#21117](https://github.com/docker/docker/pull/21117), [#21262](https://github.com/docker/docker/pull/21262))
* `send`, `recv` and `x32` were added to the list of allowed syscalls and arch in the default seccomp profile ([#19432](https://github.com/docker/docker/pull/19432))
* Docker Content Trust now requests the server to perform snapshot signing ([#21046](https://github.com/docker/docker/pull/21046))
* Support for using YubiKeys for Content Trust signing has been moved out of experimental ([#21591](https://github.com/docker/docker/pull/21591))

### [Volumes](#volumes)

* Output of `docker volume ls` is now sorted by volume name ([#20389](https://github.com/docker/docker/pull/20389))
* Local volumes can now accept options similar to the unix `mount` tool ([#20262](https://github.com/docker/docker/pull/20262))

- Fix an issue where one letter directory name could not be used as source for volumes ([#21106](https://github.com/docker/docker/pull/21106))

* `docker run -v` now accepts a new flag `nocopy`. This tells the runtime not to copy the container path content into the volume (which is the default behavior) ([#21223](https://github.com/docker/docker/pull/21223))

## [1.10.3 (2016-03-10)](#1103-2016-03-10)

### [Runtime](#runtime-12)

* Fix Docker client exiting with an "Unrecognized input header" error [#20706](https://github.com/docker/docker/pull/20706)
* Fix Docker exiting if Exec is started with both `AttachStdin` and `Detach` [#20647](https://github.com/docker/docker/pull/20647)

### [Distribution](#distribution-4)

* Fix a crash when pushing multiple images sharing the same layers to the same repository in parallel [#20831](https://github.com/docker/docker/pull/20831)
* Fix a panic when pushing images to a registry which uses a misconfigured token service [#21030](https://github.com/docker/docker/pull/21030)

### [Plugin system](#plugin-system)

* Fix issue preventing volume plugins to start when SELinux is enabled [#20834](https://github.com/docker/docker/pull/20834)
* Prevent Docker from exiting if a volume plugin returns a null response for Get requests [#20682](https://github.com/docker/docker/pull/20682)
* Fix plugin system leaking file descriptors if a plugin has an error [#20680](https://github.com/docker/docker/pull/20680)

### [Security](#security-3)

* Fix linux32 emulation to fail during docker build [#20672](https://github.com/docker/docker/pull/20672) It was due to the `personality` syscall being blocked by the default seccomp profile.
* Fix Oracle XE 10g failing to start in a container [#20981](https://github.com/docker/docker/pull/20981) It was due to the `ipc` syscall being blocked by the default seccomp profile.
* Fix user namespaces not working on Linux From Scratch [#20685](https://github.com/docker/docker/pull/20685)
* Fix issue preventing daemon to start if userns is enabled and the `subuid` or `subgid` files contain comments [#20725](https://github.com/docker/docker/pull/20725)

## [1.10.2 (2016-02-22)](#1102-2016-02-22)

### [Runtime](#runtime-13)

* Prevent systemd from deleting containers' cgroups when its configuration is reloaded [#20518](https://github.com/docker/docker/pull/20518)
* Fix SELinux issues by disregarding `--read-only` when mounting `/dev/mqueue` [#20333](https://github.com/docker/docker/pull/20333)
* Fix chown permissions used during `docker cp` when userns is used [#20446](https://github.com/docker/docker/pull/20446)
* Fix configuration loading issue with all booleans defaulting to `true` [#20471](https://github.com/docker/docker/pull/20471)
* Fix occasional panic with `docker logs -f` [#20522](https://github.com/docker/docker/pull/20522)

### [Distribution](#distribution-5)

* Keep layer reference if deletion failed to avoid a badly inconsistent state [#20513](https://github.com/docker/docker/pull/20513)
* Handle gracefully a corner case when canceling migration [#20372](https://github.com/docker/docker/pull/20372)
* Fix docker import on compressed data [#20367](https://github.com/docker/docker/pull/20367)
* Fix tar-split files corruption during migration that later cause docker push and docker save to fail [#20458](https://github.com/docker/docker/pull/20458)

### [Networking](#networking-10)

* Fix daemon crash if embedded DNS is sent garbage [#20510](https://github.com/docker/docker/pull/20510)

### [Volumes](#volumes-1)

* Fix issue with multiple volume references with same name [#20381](https://github.com/docker/docker/pull/20381)

### [Security](#security-4)

* Fix potential cache corruption and delegation conflict issues [#20523](https://github.com/docker/docker/pull/20523)

## [1.10.1 (2016-02-11)](#1101-2016-02-11)

### [Runtime](#runtime-14)

* Do not stop daemon on migration hard failure [#20156](https://github.com/docker/docker/pull/20156)

- Fix various issues with migration to content-addressable images [#20058](https://github.com/docker/docker/pull/20058)
- Fix ZFS permission bug with user namespaces [#20045](https://github.com/docker/docker/pull/20045)
- Do not leak /dev/mqueue from the host to all containers, keep it container-specific [#19876](https://github.com/docker/docker/pull/19876) [#20133](https://github.com/docker/docker/pull/20133)
- Fix `docker ps --filter before=...` to not show stopped containers without providing `-a` flag [#20135](https://github.com/docker/docker/pull/20135)

### [Security](#security-5)

* Fix issue preventing docker events to work properly with authorization plugin [#20002](https://github.com/docker/docker/pull/20002)

### [Distribution](#distribution-6)

* Add additional verifications and prevent from uploading invalid data to registries [#20164](https://github.com/docker/docker/pull/20164)

- Fix regression preventing uppercase characters in image reference hostname [#20175](https://github.com/docker/docker/pull/20175)

### [Networking](#networking-11)

* Fix embedded DNS for user-defined networks in the presence of firewalld [#20060](https://github.com/docker/docker/pull/20060)
* Fix issue where removing a network during shutdown left Docker inoperable [#20181](https://github.com/docker/docker/issues/20181) [#20235](https://github.com/docker/docker/issues/20235)
* Embedded DNS is now able to return compressed results [#20181](https://github.com/docker/docker/issues/20181)
* Fix port-mapping issue with `userland-proxy=false` [#20181](https://github.com/docker/docker/issues/20181)

### [Logging](#logging-5)

* Fix bug where tcp+tls protocol would be rejected [#20109](https://github.com/docker/docker/pull/20109)

### [Volumes](#volumes-2)

* Fix issue whereby older volume drivers would not receive volume options [#19983](https://github.com/docker/docker/pull/19983)

### [Misc](#misc-1)

* Remove TasksMax from Docker systemd service [#20167](https://github.com/docker/docker/pull/20167)

## [1.10.0 (2016-02-04)](#1100-2016-02-04)

> Important
>
> Docker 1.10 uses a new content-addressable storage for images and layers.

A migration is performed the first time `docker` is run, and can take a significant amount of time depending on the number of images present. Refer to this page on the wiki for more information: <https://github.com/docker/docker/wiki/Engine-v1.10.0-content-addressability-migration> We also released a cool migration utility that enables you to perform the migration before updating to reduce downtime. Engine 1.10 migrator can be found on Docker Hub: <https://hub.docker.com/r/docker/v1.10-migrator/>

### [Runtime](#runtime-15)

* New `docker update` command that allows updating resource constraints on running containers [#15078](https://github.com/docker/docker/pull/15078)
* Add `--tmpfs` flag to `docker run` to create a tmpfs mount in a container [#13587](https://github.com/docker/docker/pull/13587)
* Add `--format` flag to `docker images` command [#17692](https://github.com/docker/docker/pull/17692)
* Allow to set daemon configuration in a file and hot-reload it with the `SIGHUP` signal [#18587](https://github.com/docker/docker/pull/18587)
* Updated docker events to include more meta-data and event types [#18888](https://github.com/docker/docker/pull/18888) This change is backward compatible in the API, but not on the CLI.
* Add `--blkio-weight-device` flag to `docker run` [#13959](https://github.com/docker/docker/pull/13959)
* Add `--device-read-bps` and `--device-write-bps` flags to `docker run` [#14466](https://github.com/docker/docker/pull/14466)
* Add `--device-read-iops` and `--device-write-iops` flags to `docker run` [#15879](https://github.com/docker/docker/pull/15879)
* Add `--oom-score-adj` flag to `docker run` [#16277](https://github.com/docker/docker/pull/16277)
* Add `--detach-keys` flag to `attach`, `run`, `start` and `exec` commands to override the default key sequence that detaches from a container [#15666](https://github.com/docker/docker/pull/15666)
* Add `--shm-size` flag to `run`, `create` and `build` to set the size of `/dev/shm` [#16168](https://github.com/docker/docker/pull/16168)
* Show the number of running, stopped, and paused containers in `docker info` [#19249](https://github.com/docker/docker/pull/19249)
* Show the `OSType` and `Architecture` in `docker info` [#17478](https://github.com/docker/docker/pull/17478)
* Add `--cgroup-parent` flag on `daemon` to set cgroup parent for all containers [#19062](https://github.com/docker/docker/pull/19062)
* Add `-L` flag to docker cp to follow symlinks [#16613](https://github.com/docker/docker/pull/16613)
* New `status=dead` filter for `docker ps` [#17908](https://github.com/docker/docker/pull/17908)

- Change `docker run` exit codes to distinguish between runtime and application errors [#14012](https://github.com/docker/docker/pull/14012)
- Enhance `docker events --since` and `--until` to support nanoseconds and timezones [#17495](https://github.com/docker/docker/pull/17495)
- Add `--all`/`-a` flag to `stats` to include both running and stopped containers [#16742](https://github.com/docker/docker/pull/16742)
- Change the default cgroup-driver to `cgroupfs` [#17704](https://github.com/docker/docker/pull/17704)
- Emit a "tag" event when tagging an image with `build -t` [#17115](https://github.com/docker/docker/pull/17115)
- Best effort for linked containers' start order when starting the daemon [#18208](https://github.com/docker/docker/pull/18208)
- Add ability to add multiple tags on `build` [#15780](https://github.com/docker/docker/pull/15780)
- Permit `OPTIONS` request against any url, thus fixing issue with CORS [#19569](https://github.com/docker/docker/pull/19569)

* Fix the `--quiet` flag on `docker build` to actually be quiet [#17428](https://github.com/docker/docker/pull/17428)
* Fix `docker images --filter dangling=false` to now show all non-dangling images [#19326](https://github.com/docker/docker/pull/19326)
* Fix race condition causing autorestart turning off on restart [#17629](https://github.com/docker/docker/pull/17629)
* Recognize GPFS filesystems [#19216](https://github.com/docker/docker/pull/19216)
* Fix obscure bug preventing to start containers [#19751](https://github.com/docker/docker/pull/19751)
* Forbid `exec` during container restart [#19722](https://github.com/docker/docker/pull/19722)
* devicemapper: Increasing `--storage-opt dm.basesize` will now increase the base device size on daemon restart [#19123](https://github.com/docker/docker/pull/19123)

### [Security](#security-6)

* Add `--userns-remap` flag to `daemon` to support user namespaces (previously in experimental) [#19187](https://github.com/docker/docker/pull/19187)
* Add support for custom seccomp profiles in `--security-opt` [#17989](https://github.com/docker/docker/pull/17989)
* Add default seccomp profile [#18780](https://github.com/docker/docker/pull/18780)
* Add `--authorization-plugin` flag to `daemon` to customize ACLs [#15365](https://github.com/docker/docker/pull/15365)
* Docker Content Trust now supports the ability to read and write user delegations [#18887](https://github.com/docker/docker/pull/18887) This is an optional, opt-in feature that requires the explicit use of the Notary command-line utility in order to be enabled. Enabling delegation support in a specific repository will break the ability of Docker 1.9 and 1.8 to pull from that repository, if content trust is enabled.

- Allow SELinux to run in a container when using the BTRFS storage driver [#16452](https://github.com/docker/docker/pull/16452)

### [Distribution](#distribution-7)

* Use content-addressable storage for images and layers [#17924](https://github.com/docker/docker/pull/17924) A migration is performed the first time docker is run; it can take a significant amount of time depending on the number of images and containers present. Images no longer depend on the parent chain but contain a list of layer references. `docker load`/`docker save` tarballs now also contain content-addressable image configurations. For more information: <https://github.com/docker/docker/wiki/Engine-v1.10.0-content-addressability-migration>
* Add support for the new [manifest format ("schema2")](https://github.com/docker/distribution/blob/master/docs/spec/manifest-v2-2.md) [#18785](https://github.com/docker/docker/pull/18785)
* Lots of improvements for push and pull: performance++, retries on failed downloads, cancelling on client disconnect [#18353](https://github.com/docker/docker/pull/18353), [#18418](https://github.com/docker/docker/pull/18418), [#19109](https://github.com/docker/docker/pull/19109), [#18353](https://github.com/docker/docker/pull/18353)
* Limit v1 protocol fallbacks [#18590](https://github.com/docker/docker/pull/18590)

- Fix issue where docker could hang indefinitely waiting for a nonexistent process to pull an image [#19743](https://github.com/docker/docker/pull/19743)

### [Networking](#networking-12)

* Use DNS-based discovery instead of `/etc/hosts` [#19198](https://github.com/docker/docker/pull/19198)
* Support for network-scoped alias using `--net-alias` on `run` and `--alias` on `network connect` [#19242](https://github.com/docker/docker/pull/19242)
* Add `--ip` and `--ip6` on `run` and `network connect` to support custom IP addresses for a container in a network [#19001](https://github.com/docker/docker/pull/19001)
* Add `--ipam-opt` to `network create` for passing custom IPAM options [#17316](https://github.com/docker/docker/pull/17316)
* Add `--internal` flag to `network create` to restrict external access to and from the network [#19276](https://github.com/docker/docker/pull/19276)
* Add `kv.path` option to `--cluster-store-opt` [#19167](https://github.com/docker/docker/pull/19167)
* Add `discovery.heartbeat` and `discovery.ttl` options to `--cluster-store-opt` to configure discovery TTL and heartbeat timer [#18204](https://github.com/docker/docker/pull/18204)
* Add `--format` flag to `network inspect` [#17481](https://github.com/docker/docker/pull/17481)
* Add `--link` to `network connect` to provide a container-local alias [#19229](https://github.com/docker/docker/pull/19229)
* Support for Capability exchange with remote IPAM plugins [#18775](https://github.com/docker/docker/pull/18775)
* Add `--force` to `network disconnect` to force container to be disconnected from network [#19317](https://github.com/docker/docker/pull/19317)

- Support for multi-host networking using built-in overlay driver for all engine supported kernels: 3.10+ [#18775](https://github.com/docker/docker/pull/18775)
- `--link` is now supported on `docker run` for containers in user-defined network [#19229](https://github.com/docker/docker/pull/19229)
- Enhance `docker network rm` to allow removing multiple networks [#17489](https://github.com/docker/docker/pull/17489)
- Include container names in `network inspect` [#17615](https://github.com/docker/docker/pull/17615)
- Include auto-generated subnets for user-defined networks in `network inspect` [#17316](https://github.com/docker/docker/pull/17316)
- Add `--filter` flag to `network ls` to hide predefined networks [#17782](https://github.com/docker/docker/pull/17782)
- Add support for network connect/disconnect to stopped containers [#18906](https://github.com/docker/docker/pull/18906)
- Add network ID to container inspect [#19323](https://github.com/docker/docker/pull/19323)

* Fix MTU issue where Docker would not start with two or more default routes [#18108](https://github.com/docker/docker/pull/18108)
* Fix duplicate IP address for containers [#18106](https://github.com/docker/docker/pull/18106)
* Fix issue preventing sometimes docker from creating the bridge network [#19338](https://github.com/docker/docker/pull/19338)
* Do not substitute 127.0.0.1 name server when using `--net=host` [#19573](https://github.com/docker/docker/pull/19573)

### [Logging](#logging-6)

* New logging driver for Splunk [#16488](https://github.com/docker/docker/pull/16488)
* Add support for syslog over TCP+TLS [#18998](https://github.com/docker/docker/pull/18998)

- Enhance `docker logs --since` and `--until` to support nanoseconds and time [#17495](https://github.com/docker/docker/pull/17495)
- Enhance AWS logs to auto-detect region [#16640](https://github.com/docker/docker/pull/16640)

### [Volumes](#volumes-3)

* Add support to set the mount propagation mode for a volume [#17034](https://github.com/docker/docker/pull/17034)

- Add `ls` and `inspect` endpoints to volume plugin API [#16534](https://github.com/docker/docker/pull/16534) Existing plugins need to make use of these new APIs to satisfy users' expectation For that, use the new MIME type `application/vnd.docker.plugins.v1.2+json` [#19549](https://github.com/docker/docker/pull/19549)

* Fix data not being copied to named volumes [#19175](https://github.com/docker/docker/pull/19175)
* Fix issues preventing volume drivers from being containerized [#19500](https://github.com/docker/docker/pull/19500)
* Fix `docker volumes ls --dangling=false` to now show all non-dangling volumes [#19671](https://github.com/docker/docker/pull/19671)
* Do not remove named volumes on container removal [#19568](https://github.com/docker/docker/pull/19568)
* Allow external volume drivers to host anonymous volumes [#19190](https://github.com/docker/docker/pull/19190)

### [Builder](#builder-4)

* Add support for `**` in `.dockerignore` to wildcard multiple levels of directories [#17090](https://github.com/docker/docker/pull/17090)

- Fix handling of UTF-8 characters in Dockerfiles [#17055](https://github.com/docker/docker/pull/17055)
- Fix permissions problem when reading from STDIN [#19283](https://github.com/docker/docker/pull/19283)

### [Client](#client-2)

* Add support for overriding the API version to use via an `DOCKER_API_VERSION` environment-variable [#15964](https://github.com/docker/docker/pull/15964)

- Fix a bug preventing Windows clients to log in to Docker Hub [#19891](https://github.com/docker/docker/pull/19891)

### [Misc](#misc-2)

* systemd: Set TasksMax in addition to LimitNPROC in systemd service file [#19391](https://github.com/docker/docker/pull/19391)

### [Deprecations](#deprecations)

* Remove LXC support. The LXC driver was deprecated in Docker 1.8, and has now been removed [#17700](https://github.com/docker/docker/pull/17700)
* Remove `--exec-driver` daemon flag, because it is no longer in use [#17700](https://github.com/docker/docker/pull/17700)
* Remove old deprecated single-dashed long CLI flags (such as `-rm`; use `--rm` instead) [#17724](https://github.com/docker/docker/pull/17724)
* Deprecate HostConfig at API container start [#17799](https://github.com/docker/docker/pull/17799)
* Deprecate docker packages for newly EOL'd Linux distributions: Fedora 21 and Ubuntu 15.04 (Vivid) [#18794](https://github.com/docker/docker/pull/18794), [#18809](https://github.com/docker/docker/pull/18809)
* Deprecate `-f` flag for docker tag [#18350](https://github.com/docker/docker/pull/18350)

## [1.9.1 (2015-11-21)](#191-2015-11-21)

### [Runtime](#runtime-16)

* Do not prevent daemon from booting if images could not be restored (#17695)
* Force IPC mount to unmount on daemon shutdown/init (#17539)
* Turn IPC unmount errors into warnings (#17554)
* Fix `docker stats` performance regression (#17638)
* Clarify cryptic error message upon `docker logs` if `--log-driver=none` (#17767)
* Fix seldom panics (#17639, #17634, #17703)
* Fix opq whiteouts problems for files with dot prefix (#17819)
* devicemapper: try defaulting to xfs instead of ext4 for performance reasons (#17903, #17918)
* devicemapper: fix displayed fs in docker info (#17974)
* selinux: only relabel if user requested so with the `z` option (#17450, #17834)
* Do not make network calls when normalizing names (#18014)

### [Client](#client-3)

* Fix `docker login` on windows (#17738)
* Fix bug with `docker inspect` output when not connected to daemon (#17715)
* Fix `docker inspect -f {{.HostConfig.Dns}} somecontainer` (#17680)

### [Builder](#builder-5)

* Fix regression with symlink behavior in ADD/COPY (#17710)

### [Networking](#networking-13)

* Allow passing a network ID as an argument for `--net` (#17558)
* Fix connect to host and prevent disconnect from host for `host` network (#17476)
* Fix `--fixed-cidr` issue when gateway ip falls in ip-range and ip-range is not the first block in the network (#17853)
* Restore deterministic `IPv6` generation from `MAC` address on default `bridge` network (#17890)
* Allow port-mapping only for endpoints created on docker run (#17858)
* Fixed an endpoint delete issue with a possible stale sbox (#18102)

### [Distribution](#distribution-8)

* Correct parent chain in v2 push when v1Compatibility files on the disk are inconsistent (#18047)

## [1.9.0 (2015-11-03)](#190-2015-11-03)

### [Runtime](#runtime-17)

* `docker stats` now returns block IO metrics (#15005)
* `docker stats` now details network stats per interface (#15786)
* Add `ancestor=<image>` filter to `docker ps --filter` flag to filter containers based on their ancestor images (#14570)
* Add `label=<somelabel>` filter to `docker ps --filter` to filter containers based on label (#16530)
* Add `--kernel-memory` flag to `docker run` (#14006)
* Add `--message` flag to `docker import` allowing to specify an optional message (#15711)
* Add `--privileged` flag to `docker exec` (#14113)
* Add `--stop-signal` flag to `docker run` allowing to replace the container process stopping signal (#15307)
* Add a new `unless-stopped` restart policy (#15348)
* Inspecting an image now returns tags (#13185)
* Add container size information to `docker inspect` (#15796)
* Add `RepoTags` and `RepoDigests` field to `/images/{name:.*}/json` (#17275)

- Remove the deprecated `/container/ps` endpoint from the API (#15972)
- Send and document correct HTTP codes for `/exec/<name>/start` (#16250)
- Share shm and mqueue between containers sharing IPC namespace (#15862)
- Event stream now shows OOM status when `--oom-kill-disable` is set (#16235)
- Ensure special network files (/etc/hosts etc.) are read-only if bind-mounted with `ro` option (#14965)
- Improve `rmi` performance (#16890)
- Do not update /etc/hosts for the default bridge network, except for links (#17325)
- Fix conflict with duplicate container names (#17389)
- Fix an issue with incorrect template execution in `docker inspect` (#17284)
- DEPRECATE `-c` short flag variant for `--cpu-shares` in docker run (#16271)

### [Client](#client-4)

* Allow `docker import` to import from local files (#11907)

### [Builder](#builder-6)

* Add a `STOPSIGNAL` Dockerfile instruction allowing to set a different stop-signal for the container process (#15307)
* Add an `ARG` Dockerfile instruction and a `--build-arg` flag to `docker build` that allows to add build-time environment variables (#15182)

- Improve cache miss performance (#16890)

### [Storage](#storage)

* devicemapper: Implement deferred deletion capability (#16381)

### [Networking](#networking-14)

* `docker network` exits experimental and is part of standard release (#16645)
* New network top-level concept, with associated subcommands and API (#16645) WARNING: the API is different from the experimental API
* Support for multiple isolated/micro-segmented networks (#16645)
* Built-in multihost networking using VXLAN based overlay driver (#14071)
* Support for third-party network plugins (#13424)
* Ability to dynamically connect containers to multiple networks (#16645)
* Support for user-defined IP address management via pluggable IPAM drivers (#16910)
* Add daemon flags `--cluster-store` and `--cluster-advertise` for built-in nodes discovery (#16229)
* Add `--cluster-store-opt` for setting up TLS settings (#16644)
* Add `--dns-opt` to the daemon (#16031)

- DEPRECATE following container `NetworkSettings` fields in API v1.21: `EndpointID`, `Gateway`, `GlobalIPv6Address`, `GlobalIPv6PrefixLen`, `IPAddress`, `IPPrefixLen`, `IPv6Gateway` and `MacAddress`. Those are now specific to the `bridge` network. Use `NetworkSettings.Networks` to inspect the networking settings of a container per network.

### [Volumes](#volumes-4)

* New top-level `volume` subcommand and API (#14242)

- Move API volume driver settings to host-specific config (#15798)
- Print an error message if volume name is not unique (#16009)
- Ensure volumes created from Dockerfiles always use the local volume driver (#15507)
- DEPRECATE auto-creating missing host paths for bind mounts (#16349)

### [Logging](#logging-7)

* Add `awslogs` logging driver for Amazon CloudWatch (#15495)
* Add generic `tag` log option to allow customizing container/image information passed to driver (#15384)

- Implement the `docker logs` endpoint for the journald driver (#13707)
- DEPRECATE driver-specific log tags (#15384)

### [Distribution](#distribution-9)

* `docker search` now works with partial names (#16509)

- Push optimization: avoid buffering to file (#15493)
- The daemon will display progress for images that were already being pulled by another client (#15489)
- Only permissions required for the current action being performed are requested (#)

* Renaming trust keys (and respective environment variables) from `offline` to `root` and `tagging` to `repository` (#16894)

- DEPRECATE trust key environment variables `DOCKER_CONTENT_TRUST_OFFLINE_PASSPHRASE` and `DOCKER_CONTENT_TRUST_TAGGING_PASSPHRASE` (#16894)

### [Security](#security-7)

* Add SELinux profiles to the rpm package (#15832)

- Fix various issues with AppArmor profiles provided in the deb package (#14609)
- Add AppArmor policy that prevents writing to /proc (#15571)

## [1.8.3 (2015-10-12)](#183-2015-10-12)

### [Distribution](#distribution-10)

* Fix layer IDs lead to local graph poisoning (CVE-2014-8178)
* Fix manifest validation and parsing logic errors allow pull-by-digest validation bypass (CVE-2014-8179)

- Add `--disable-legacy-registry` to prevent a daemon from using a v1 registry

## [1.8.2 (2015-09-10)](#182-2015-09-10)

### [Distribution](#distribution-11)

* Fixes rare edge case of handling GNU LongLink and LongName entries.
* Fix ^C on docker pull.
* Fix docker pull issues on client disconnection.
* Fix issue that caused the daemon to panic when loggers weren't configured properly.
* Fix goroutine leak pulling images from registry V2.

### [Runtime](#runtime-18)

* Fix a bug mounting cgroups for docker daemons running inside docker containers.
* Initialize log configuration properly.

### [Client:](#client-5)

* Handle `-q` flag in `docker ps` properly when there is a default format.

### [Networking](#networking-15)

* Fix several corner cases with netlink.

### [Contrib](#contrib-8)

* Fix several issues with bash completion.

## [1.8.1 (2015-08-12)](#181-2015-08-12)

### [Distribution](#distribution-12)

* Fix a bug where pushing multiple tags would result in invalid images

## [1.8.0 (2015-08-11)](#180-2015-08-11)

### [Distribution](#distribution-13)

* Trusted pull, push and build, disabled by default

- Make tar layers deterministic between registries
- Don't allow deleting the image of running containers
- Check if a tag name to load is a valid digest
- Allow one character repository names
- Add a more accurate error description for invalid tag name
- Make build cache ignore mtime

### [Cli](#cli)

* Add support for DOCKER\_CONFIG/--config to specify config file dir
* Add --type flag for docker inspect command
* Add formatting options to `docker ps` with `--format`
* Replace `docker -d` with new subcommand `docker daemon`

- Zsh completion updates and improvements
- Add some missing events to bash completion
- Support daemon urls with base paths in `docker -H`
- Validate status= filter to docker ps
- Display when a container is in --net=host in docker ps
- Extend docker inspect to export image metadata related to graph driver
- Restore --default-gateway{,-v6} daemon options
- Add missing unpublished ports in docker ps
- Allow duration strings in `docker events` as --since/--until
- Expose more mounts information in `docker inspect`

### [Runtime](#runtime-19)

* Add new Fluentd logging driver
* Allow `docker import` to load from local files
* Add logging driver for GELF via UDP
* Allow to copy files from host to containers with `docker cp`
* Promote volume drivers from experimental to master
* Add rollover options to json-file log driver, and --log-driver-opts flag
* Add memory swappiness tuning options

- Remove cgroup read-only flag when privileged
- Make /proc, /sys, & /dev readonly for readonly containers
- Add cgroup bind mount by default
- Overlay: Export metadata for container and image in `docker inspect`
- Devicemapper: external device activation
- Devicemapper: Compare uuid of base device on startup
- Remove RC4 from the list of registry cipher suites
- Add syslog-facility option
- LXC execdriver compatibility with recent LXC versions
- Mark LXC execriver as deprecated (to be removed with the migration to runc)

### [Plugins](#plugins-3)

* Separate plugin sockets and specs locations
* Allow TLS connections to plugins

### [Bug fixes](#bug-fixes)

* Add missing 'Names' field to /containers/json API output
* Make `docker rmi` of dangling images safe while pulling
* Devicemapper: Change default basesize to 100G
* Go Scheduler issue with sync.Mutex and gcc
* Fix issue where Search API endpoint would panic due to empty AuthConfig
* Set image canonical names correctly
* Check dockerinit only if lxc driver is used
* Fix ulimit usage of nproc
* Always attach STDIN if -i,--interactive is specified
* Show error messages when saving container state fails
* Fixed incorrect assumption on --bridge=none treated as disable network
* Check for invalid port specifications in host configuration
* Fix endpoint leave failure for --net=host mode
* Fix goroutine leak in the stats API if the container is not running
* Check for apparmor file before reading it
* Fix DOCKER\_TLS\_VERIFY being ignored
* Set umask to the default on startup
* Correct the message of pause and unpause a non-running container
* Adjust disallowed CpuShares in container creation
* ZFS: correctly apply selinux context
* Display empty string instead of when IP opt is nil
* `docker kill` returns error when container is not running
* Fix COPY/ADD quoted/json form
* Fix goroutine leak on logs -f with no output
* Remove panic in nat package on invalid hostport
* Fix container linking in Fedora 22
* Fix error caused using default gateways outside of the allocated range
* Format times in inspect command with a template as RFC3339Nano
* Make registry client to accept 2xx and 3xx http status responses as successful
* Fix race issue that caused the daemon to crash with certain layer downloads failed in a specific order.
* Fix error when the docker ps format was not valid.
* Remove redundant ip forward check.
* Fix issue trying to push images to repository mirrors.
* Fix error cleaning up network entrypoints when there is an initialization issue.

## [1.7.1 (2015-07-14)](#171-2015-07-14)

### [Runtime](#runtime-20)

* Fix default user spawning exec process with `docker exec`
* Make `--bridge=none` not to configure the network bridge
* Publish networking stats properly
* Fix implicit devicemapper selection with static binaries
* Fix socket connections that hung intermittently
* Fix bridge interface creation on CentOS/RHEL 6.6
* Fix local dns lookups added to resolv.conf
* Fix copy command mounting volumes
* Fix read/write privileges in volumes mounted with --volumes-from

### [Remote API](#remote-api)

* Fix unmarshalling of Command and Entrypoint
* Set limit for minimum client version supported
* Validate port specification
* Return proper errors when attach/reattach fail

### [Distribution](#distribution-14)

* Fix pulling private images
* Fix fallback between registry V2 and V1

## [1.7.0 (2015-06-16)](#170-2015-06-16)

### [Runtime](#runtime-21)

* Experimental feature: support for out-of-process volume plugins

- The userland proxy can be disabled in favor of hairpin NAT using the daemon’s `--userland-proxy=false` flag
- The `exec` command supports the `-u|--user` flag to specify the new process owner

* Default gateway for containers can be specified daemon-wide using the `--default-gateway` and `--default-gateway-v6` flags
* The CPU CFS (Completely Fair Scheduler) quota can be set in `docker run` using `--cpu-quota`
* Container block IO can be controlled in `docker run` using`--blkio-weight`
* ZFS support
* The `docker logs` command supports a `--since` argument
* UTS namespace can be shared with the host with `docker run --uts=host`

### [Quality](#quality)

* Networking stack was entirely rewritten as part of the libnetwork effort
* Engine internals refactoring
* Volumes code was entirely rewritten to support the plugins effort

- Sending SIGUSR1 to a daemon will dump all goroutines stacks without exiting

### [Build](#build)

* Support ${variable:-value} and ${variable:+value} syntax for environment variables
* Support resource management flags `--cgroup-parent`, `--cpu-period`, `--cpu-quota`, `--cpuset-cpus`, `--cpuset-mems`
* git context changes with branches and directories

- The .dockerignore file support exclusion rules

### [Distribution](#distribution-15)

* Client support for v2 mirroring support for the official registry

### [Bugfixes](#bugfixes)

* Firewalld is now supported and will automatically be used when available
* mounting --device recursively

## [1.6.2 (2015-05-13)](#162-2015-05-13)

### [Runtime](#runtime-22)

* Revert change prohibiting mounting into /sys

## [1.6.1 (2015-05-07)](#161-2015-05-07)

### [Security](#security-8)

* Fix read/write /proc paths (CVE-2015-3630)
* Prohibit VOLUME /proc and VOLUME / (CVE-2015-3631)
* Fix opening of file-descriptor 1 (CVE-2015-3627)
* Fix symlink traversal on container respawn allowing local privilege escalation (CVE-2015-3629)
* Prohibit mount of /sys

### [Runtime](#runtime-23)

* Update AppArmor policy to not allow mounts

## [1.6.0 (2015-04-07)](#160-2015-04-07)

### [Builder](#builder-7)

* Building images from an image ID
* Build containers with resource constraints, ie `docker build --cpu-shares=100 --memory=1024m...`
* `commit --change` to apply specified Dockerfile instructions while committing the image
* `import --change` to apply specified Dockerfile instructions while importing the image
* Builds no longer continue in the background when canceled with CTRL-C

### [Client](#client-6)

* Windows Support

### [Runtime](#runtime-24)

* Container and image Labels
* `--cgroup-parent` for specifying a parent cgroup to place container cgroup within
* Logging drivers, `json-file`, `syslog`, or `none`
* Pulling images by ID
* `--ulimit` to set the ulimit on a container
* `--default-ulimit` option on the daemon which applies to all created containers (and overwritten by `--ulimit` on run)

## [1.5.0 (2015-02-10)](#150-2015-02-10)

### [Builder](#builder-8)

* Dockerfile to use for a given `docker build` can be specified with the `-f` flag

- Dockerfile and .dockerignore files can be themselves excluded as part of the .dockerignore file, thus preventing modifications to these files invalidating ADD or COPY instructions cache
- ADD and COPY instructions accept relative paths
- Dockerfile `FROM scratch` instruction is now interpreted as a no-base specifier
- Improve performance when exposing a large number of ports

### [Hack](#hack)

* Allow client-side only integration tests for Windows

- Include docker-py integration tests against Docker daemon as part of our test suites

### [Packaging](#packaging)

* Support for the new version of the registry HTTP API

- Speed up `docker push` for images with a majority of already existing layers

* Fixed contacting a private registry through a proxy

### [Remote API](#remote-api-1)

* A new endpoint will stream live container resource metrics and can be accessed with the `docker stats` command
* Containers can be renamed using the new `rename` endpoint and the associated `docker rename` command

- Container `inspect` endpoint show the ID of `exec` commands running in this container
- Container `inspect` endpoint show the number of times Docker auto-restarted the container
- New types of event can be streamed by the `events` endpoint: ‘OOM’ (container died with out of memory), ‘exec\_create’, and ‘exec\_start'

* Fixed returned string fields which hold numeric characters incorrectly omitting surrounding double quotes

### [Runtime](#runtime-25)

* Docker daemon has full IPv6 support
* The `docker run` command can take the `--pid=host` flag to use the host PID namespace, which makes it possible for example to debug host processes using containerized debugging tools
* The `docker run` command can take the `--read-only` flag to make the container’s root filesystem mounted as readonly, which can be used in combination with volumes to force a container’s processes to only write to locations that will be persisted
* Container total memory usage can be limited for `docker run` using the `--memory-swap` flag

- Major stability improvements for devicemapper storage driver
- Better integration with host system: containers will reflect changes to the host's `/etc/resolv.conf` file when restarted
- Better integration with host system: per-container iptable rules are moved to the DOCKER chain

* Fixed container exiting on out of memory to return an invalid exit code

### [Other](#other)

* The HTTP\_PROXY, HTTPS\_PROXY, and NO\_PROXY environment variables are properly taken into account by the client when connecting to the Docker daemon

## [1.4.1 (2014-12-15)](#141-2014-12-15)

### [Runtime](#runtime-26)

* Fix issue with volumes-from and bind mounts not being honored after create

## [1.4.0 (2014-12-11)](#140-2014-12-11)

### [Notable Features since 1.3.0](#notable-features-since-130)

* Set key=value labels to the daemon (displayed in `docker info`), applied with new `-label` daemon flag
* Add support for `ENV` in Dockerfile of the form: `ENV name=value name2=value2...`
* New Overlayfs Storage Driver
* `docker info` now returns an `ID` and `Name` field
* Filter events by event name, container, or image
* `docker cp` now supports copying from container volumes

- Fixed `docker tag`, so it honors `--force` when overriding a tag for existing image.

## [1.3.3 (2014-12-11)](#133-2014-12-11)

### [Security](#security-9)

* Fix path traversal vulnerability in processing of absolute symbolic links (CVE-2014-9356)
* Fix decompression of xz image archives, preventing privilege escalation (CVE-2014-9357)
* Validate image IDs (CVE-2014-9358)

### [Runtime](#runtime-27)

* Fix an issue when image archives are being read slowly

### [Client](#client-7)

* Fix a regression related to stdin redirection
* Fix a regression with `docker cp` when destination is the current directory

## [1.3.2 (2014-11-20)](#132-2014-11-20)

### [Security](#security-10)

* Fix tar breakout vulnerability

- Extractions are now sandboxed chroot

* Security options are no longer committed to images

### [Runtime](#runtime-28)

* Fix deadlock in `docker ps -f exited=1`
* Fix a bug when `--volumes-from` references a container that failed to start

### [Registry](#registry)

* `--insecure-registry` now accepts CIDR notation such as 10.1.0.0/16

- Private registries whose IPs fall in the 127.0.0.0/8 range do no need the `--insecure-registry` flag

* Skip the experimental registry v2 API when mirroring is enabled

## [1.3.1 (2014-10-28)](#131-2014-10-28)

### [Security](#security-11)

* Prevent fallback to SSL protocols < TLS 1.0 for client, daemon and registry

- Secure HTTPS connection to registries with certificate verification and without HTTP fallback unless `--insecure-registry` is specified

### [Runtime](#runtime-29)

* Fix issue where volumes would not be shared

### [Client](#client-8)

* Fix issue with `--iptables=false` not automatically setting `--ip-masq=false`
* Fix docker run output to non-TTY stdout

### [Builder](#builder-9)

* Fix escaping `$` for environment variables
* Fix issue with lowercase `onbuild` Dockerfile instruction
* Restrict environment variable expansion to `ENV`, `ADD`, `COPY`, `WORKDIR`, `EXPOSE`, `VOLUME` and `USER`

## [1.3.0 (2014-10-14)](#130-2014-10-14)

### [Notable features since 1.2.0](#notable-features-since-120)

* Docker `exec` allows you to run additional processes inside existing containers
* Docker `create` gives you the ability to create a container via the CLI without executing a process
* `--security-opts` options to allow user to customize container labels and apparmor profiles
* Docker `ps` filters

- Wildcard support to COPY/ADD

* Move production URLs to get.docker.com from get.docker.io
* Allocate IP address on the bridge inside a valid CIDR
* Use drone.io for PR and CI testing
* Ability to setup an official registry mirror
* Ability to save multiple images with docker `save`

## [1.2.0 (2014-08-20)](#120-2014-08-20)

### [Runtime](#runtime-30)

* Make /etc/hosts /etc/resolv.conf and /etc/hostname editable at runtime
* Auto-restart containers using policies
* Use /var/lib/docker/tmp for large temporary files
* `--cap-add` and `--cap-drop` to tweak what linux capability you want
* `--device` to use devices in containers

### [Client](#client-9)

* `docker search` on private registries
* Add `exited` filter to `docker ps --filter`

- `docker rm -f` now kills instead of stop

* Support for IPv6 addresses in `--dns` flag

### [Proxy](#proxy)

* Proxy instances in separate processes

- Small bug fix on UDP proxy

## [1.1.2 (2014-07-23)](#112-2014-07-23)

### [Runtime](#runtime-31)

* Fix port allocation for existing containers
* Fix containers restart on daemon restart

### [Packaging](#packaging-1)

* Fix /etc/init.d/docker issue on Debian

## [1.1.1 (2014-07-09)](#111-2014-07-09)

### [Builder](#builder-10)

* Fix issue with ADD

## [1.1.0 (2014-07-03)](#110-2014-07-03)

### [Notable features since 1.0.1](#notable-features-since-101)

* Add `.dockerignore` support
* Pause containers during `docker commit`
* Add `--tail` to `docker logs`

### [Builder](#builder-11)

* Allow a tar file as context for `docker build`

- Fix issue with white-spaces and multi-lines in `Dockerfiles`

### [Runtime](#runtime-32)

* Overall performance improvements
* Allow `/` as source of `docker run -v`
* Fix port allocation
* Fix bug in `docker save`
* Add links information to `docker inspect`

### [Client](#client-10)

* Improve command line parsing for `docker commit`

### [Remote API](#remote-api-2)

* Improve status code for the `start` and `stop` endpoints

## [1.0.1 (2014-06-19)](#101-2014-06-19)

### [Notable features since 1.0.0](#notable-features-since-100)

* Enhance security for the LXC driver

### [Builder](#builder-12)

* Fix `ONBUILD` instruction passed to grandchildren

### [Runtime](#runtime-33)

* Fix events subscription
* Fix /etc/hostname file with host networking
* Allow `-h` and `--net=none`
* Fix issue with hotplug devices in `--privileged`

### [Client](#client-11)

* Fix artifacts with events
* Fix a panic with empty flags
* Fix `docker cp` on Mac OS X

### [Miscellaneous](#miscellaneous)

* Fix compilation on Mac OS X
* Fix several races

## [1.0.0 (2014-06-09)](#100-2014-06-09)

### [Notable features since 0.12.0](#notable-features-since-0120)

* Production support

## [0.12.0 (2014-06-05)](#0120-2014-06-05)

### [Notable features since 0.11.0](#notable-features-since-0110)

* 40+ various improvements to stability, performance and usability
* New `COPY` Dockerfile instruction to allow copying a local file from the context into the container without ever extracting if the file is a tar file
* Inherit file permissions from the host on `ADD`
* New `pause` and `unpause` commands to allow pausing and unpausing of containers using cgroup freezer
* The `images` command has a `-f`/`--filter` option to filter the list of images
* Add `--force-rm` to clean up after a failed build
* Standardize JSON keys in Remote API to CamelCase
* Pull from a docker run now assumes `latest` tag if not specified
* Enhance security on Linux capabilities and device nodes

## [0.11.1 (2014-05-07)](#0111-2014-05-07)

### [Registry](#registry-1)

* Fix push and pull to private registry

## [0.11.0 (2014-05-07)](#0110-2014-05-07)

### [Notable features since 0.10.0](#notable-features-since-0100)

* SELinux support for mount and process labels
* Linked containers can be accessed by hostname
* Use the net `--net` flag to allow advanced network configuration such as host networking so that containers can use the host's network interfaces
* Add a ping endpoint to the Remote API to do healthchecks of your docker daemon
* Logs can now be returned with an optional timestamp
* Docker now works with registries that support SHA-512
* Multiple registry endpoints are supported to allow registry mirrors

## [0.10.0 (2014-04-08)](#0100-2014-04-08)

### [Builder](#builder-13)

* Fix printing multiple messages on a single line. Fixes broken output during builds.
* Follow symlinks inside container's root for ADD build instructions.
* Fix EXPOSE caching.

### [Documentation](#documentation-1)

* Add the new options of `docker ps` to the documentation.
* Add the options of `docker restart` to the documentation.
* Update daemon docs and help messages for --iptables and --ip-forward.
* Updated apt-cacher-ng docs example.
* Remove duplicate description of --mtu from docs.
* Add missing -t and -v for `docker images` to the docs.
* Add fixes to the cli docs.
* Update libcontainer docs.
* Update images in docs to remove references to AUFS and LXC.
* Update the nodejs\_web\_app in the docs to use the new epel RPM address.
* Fix external link on security of containers.
* Update remote API docs.
* Add image size to history docs.
* Be explicit about binding to all interfaces in redis example.
* Document DisableNetwork flag in the 1.10 remote api.
* Document that `--lxc-conf` is lxc only.
* Add chef usage documentation.
* Add example for an image with multiple for `docker load`.
* Explain what `docker run -a` does in the docs.

### [Contrib](#contrib-9)

* Add variable for DOCKER\_LOGFILE to sysvinit and use append instead of overwrite in opening the logfile.
* Fix init script cgroup mounting workarounds to be more similar to cgroupfs-mount and thus work properly.
* Remove inotifywait hack from the upstart host-integration example because it's not necessary any more.
* Add check-config script to contrib.
* Fix fish shell completion.

### [Hack](#hack-1)

* Clean up "go test" output from "make test" to be much more readable/scannable.
* Exclude more "definitely not unit tested Go source code" directories from hack/make/test.

- Generate md5 and sha256 hashes when building, and upload them via hack/release.sh.

* Include contributed completions in Ubuntu PPA.

- Add cli integration tests.

* Add tweaks to the hack scripts to make them simpler.

### [Remote API](#remote-api-3)

* Add TLS auth support for API.

- Move git clone from daemon to client.

* Fix content-type detection in docker cp.

- Split API into 2 go packages.

### [Runtime](#runtime-34)

* Support hairpin NAT without going through Docker server.

- devicemapper: succeed immediately when removing non-existent devices.
- devicemapper: improve handling of devicemapper devices (add per device lock, increase sleep time and unlock while sleeping).
- devicemapper: increase timeout in waitClose to 10 seconds.
- devicemapper: ensure we shut down thin pool cleanly.
- devicemapper: pass info, rather than hash to activateDeviceIfNeeded, deactivateDevice, setInitialized, deleteDevice.
- devicemapper: avoid AB-BA deadlock.
- devicemapper: make shutdown better/faster.
- improve alpha sorting in mflag.
- Remove manual http cookie management because the cookiejar is being used.
- Use BSD raw mode on Darwin. Fixes nano, tmux and others.
- Add FreeBSD support for the client.
- Merge auth package into registry.
- Add deprecation warning for -t on `docker pull`.
- Remove goroutine leak on error.
- Update parseLxcInfo to comply with new lxc1.0 format.
- Fix attach exit on darwin.
- Improve deprecation message.
- Retry to retrieve the layer metadata up to 5 times for `docker pull`.
- Only unshare the mount namespace for execin.
- Merge existing config when committing.
- Disable daemon startup timeout.
- Fix issue #4681: add loopback interface when networking is disabled.
- Add failing test case for issue #4681.
- Send SIGTERM to child, instead of SIGKILL.
- Show the driver and the kernel version in `docker info` even when not in debug mode.
- Always symlink /dev/ptmx for libcontainer. This fixes console related problems.
- Fix issue caused by the absence of /etc/apparmor.d.
- Don't leave empty cidFile behind when failing to create the container.
- Mount cgroups automatically if they're not mounted already.
- Use mock for search tests.
- Update to double-dash everywhere.
- Move .dockerenv parsing to lxc driver.
- Move all bind-mounts in the container inside the namespace.
- Don't use separate bind mount for container.
- Always symlink /dev/ptmx for libcontainer.
- Don't kill by pid for other drivers.
- Add initial logging to libcontainer.

* Sort by port in `docker ps`.

- Move networking drivers into runtime top level package.

* Add --no-prune to `docker rmi`.
* Add time since exit in `docker ps`.

- graphdriver: add build tags.
- Prevent allocation of previously allocated ports & prevent improve port allocation.

* Add support for --since/--before in `docker ps`.

- Clean up container stop.

* Add support for configurable dns search domains.

- Add support for relative WORKDIR instructions.
- Add --output flag for docker save.
- Remove duplication of DNS entries in config merging.
- Add cpuset.cpus to cgroups and native driver options.
- Remove docker-ci.
- Promote btrfs. btrfs is no longer considered experimental.
- Add --input flag to `docker load`.
- Return error when existing bridge doesn't match IP address.
- Strip comments before parsing line continuations to avoid interpreting instructions as comments.
- Fix TestOnlyLoopbackExistsWhenUsingDisableNetworkOption to ignore "DOWN" interfaces.
- Add systemd implementation of cgroups and make containers show up as systemd units.
- Fix commit and import when no repository is specified.
- Remount /var/lib/docker as --private to fix scaling issue.
- Use the environment's proxy when pinging the remote registry.
- Reduce error level from harmless errors.

* Allow --volumes-from to be individual files.

- Fix expanding buffer in StdCopy.
- Set error regardless of attach or stdin. This fixes #3364.
- Add support for --env-file to load environment variables from files.
- Symlink /etc/mtab and /proc/mounts.
- Allow pushing a single tag.
- Shut down containers cleanly at shutdown and wait forever for the containers to shut down. This makes container shutdown on daemon shutdown work properly via SIGTERM.
- Don't throw error when starting an already running container.
- Fix dynamic port allocation limit.
- remove setupDev from libcontainer.
- Add API version to `docker version`.
- Return correct exit code when receiving signal and make SIGQUIT quit without cleanup.
- Fix --volumes-from mount failure.
- Allow non-privileged containers to create device nodes.
- Skip login tests because of external dependency on a hosted service.
- Deprecate `docker images --tree` and `docker images --viz`.
- Deprecate `docker insert`.
- Include base abstraction for apparmor. This fixes some apparmor related problems on Ubuntu 14.04.
- Add specific error message when hitting 401 over HTTP on push.
- Fix absolute volume check.
- Remove volumes-from from the config.
- Move DNS options to hostconfig.
- Update the apparmor profile for libcontainer.
- Add deprecation notice for `docker commit -run`.

## [0.9.1 (2014-03-24)](#091-2014-03-24)

### [Builder](#builder-14)

* Fix printing multiple messages on a single line. Fixes broken output during builds.

### [Documentation](#documentation-2)

* Fix external link on security of containers.

### [Contrib](#contrib-10)

* Fix init script cgroup mounting workarounds to be more similar to cgroupfs-mount and thus work properly.
* Add variable for DOCKER\_LOGFILE to sysvinit and use append instead of overwrite in opening the logfile.

### [Hack](#hack-2)

* Generate md5 and sha256 hashes when building, and upload them via hack/release.sh.

### [Remote API](#remote-api-4)

* Fix content-type detection in `docker cp`.

### [Runtime](#runtime-35)

* Use BSD raw mode on Darwin. Fixes nano, tmux and others.
* Only unshare the mount namespace for execin.
* Retry to retrieve the layer metadata up to 5 times for `docker pull`.
* Merge existing config when committing.
* Fix panic in monitor.
* Disable daemon startup timeout.
* Fix issue #4681: add loopback interface when networking is disabled.
* Add failing test case for issue #4681.
* Send SIGTERM to child, instead of SIGKILL.
* Show the driver and the kernel version in `docker info` even when not in debug mode.
* Always symlink /dev/ptmx for libcontainer. This fixes console related problems.
* Fix issue caused by the absence of /etc/apparmor.d.
* Don't leave empty cidFile behind when failing to create the container.
* Improve deprecation message.
* Fix attach exit on darwin.
* devicemapper: improve handling of devicemapper devices (add per device lock, increase sleep time, unlock while sleeping).
* devicemapper: succeed immediately when removing non-existent devices.
* devicemapper: increase timeout in waitClose to 10 seconds.
* Remove goroutine leak on error.
* Update parseLxcInfo to comply with new lxc1.0 format.

## [0.9.0 (2014-03-10)](#090-2014-03-10)

### [Builder](#builder-15)

* Avoid extra mount/unmount during build. This fixes mount/unmount related errors during build.
* Add error to docker build --rm. This adds missing error handling.
* Forbid chained onbuild, `onbuild from` and `onbuild maintainer` triggers.
* Make `--rm` the default for `docker build`.

### [Documentation](#documentation-3)

* Download the docker client binary for Mac over https.
* Update the titles of the install instructions & descriptions.

- Add instructions for upgrading boot2docker.
- Add port forwarding example in OS X install docs.

* Attempt to disentangle repository and registry.
* Update docs to explain more about `docker ps`.
* Update sshd example to use a Dockerfile.
* Rework some examples, including the Python examples.
* Update docs to include instructions for a container's lifecycle.
* Update docs documentation to discuss the docs branch.
* Don't skip cert check for an example & use HTTPS.
* Bring back the memory and swap accounting section which was lost when the kernel page was removed.
* Explain DNS warnings and how to fix them on systems running and using a local nameserver.

### [Contrib](#contrib-11)

* Add Tanglu support for mkimage-debootstrap.
* Add SteamOS support for mkimage-debootstrap.

### [Hack](#hack-3)

* Get package coverage when running integration tests.
* Remove the Vagrantfile. This is being replaced with boot2docker.
* Fix tests on systems where aufs isn't available.
* Update packaging instructions and remove the dependency on lxc.

### [Remote API](#remote-api-5)

* Move code specific to the API to the api package.

- Fix header content type for the API. Makes all endpoints use proper content type.
- Fix registry auth & remove ping calls from CmdPush and CmdPull.
- Add newlines to the JSON stream functions.

### [Runtime](#runtime-36)

* Do not ping the registry from the CLI. All requests to registries flow through the daemon.

- Check for nil information return in the lxc driver. This fixes panics with older lxc versions.
- Devicemapper: cleanups and fix for unmount. Fixes two problems which were causing unmount to fail intermittently.
- Devicemapper: remove directory when removing device. Directories don't get left behind when removing the device.

* Devicemapper: enable skip\_block\_zeroing. Improves performance by not zeroing blocks.

- Devicemapper: fix shutdown warnings. Fixes shutdown warnings concerning pool device removal.
- Ensure docker cp stream is closed properly. Fixes problems with files not being copied by `docker cp`.
- Stop making `tcp://` default to `127.0.0.1:4243` and remove the default port for tcp.
- Fix `--run` in `docker commit`. This makes `docker commit --run` work again.
- Fix custom bridge related options. This makes custom bridges work again.

* Mount-bind the PTY as container console. This allows tmux/screen to run.
* Add the pure Go libcontainer library to make it possible to run containers using only features of the Linux kernel.
* Add native exec driver which uses libcontainer and make it the default exec driver.

- Add support for handling extended attributes in archives.

* Set the container MTU to be the same as the host MTU.

- Add simple sha256 checksums for layers to speed up `docker push`.

* Improve kernel version parsing.
* Allow flag grouping (`docker run -it`).

- Remove chroot exec driver.
- Fix divide by zero to fix panic.
- Rewrite `docker rmi`.
- Fix docker info with lxc 1.0.0.
- Fix fedora tty with apparmor.

* Don't always append env vars, replace defaults with vars from config.
* Fix a goroutine leak.
* Switch to Go 1.2.1.

- Fix unique constraint error checks.

* Handle symlinks for Docker's data directory and for TMPDIR.

- Add deprecation warnings for flags (-flag is deprecated in favor of --flag)
- Add apparmor profile for the native execution driver.

* Move system specific code from archive to pkg/system.

- Fix duplicate signal for `docker run -i -t` (issue #3336).
- Return correct process pid for lxc.
- Add a -G option to specify the group which unix sockets belong to.

* Add `-f` flag to `docker rm` to force removal of running containers.
* Kill ghost containers and restart all ghost containers when the docker daemon restarts.
* Add `DOCKER_RAMDISK` environment variable to make Docker work when the root is on a ramdisk.

## [0.8.1 (2014-02-18)](#081-2014-02-18)

### [Builder](#builder-16)

* Avoid extra mount/unmount during build. This removes an unneeded mount/unmount operation which was causing problems with devicemapper
* Fix regression with ADD of tar files. This stops Docker from decompressing tarballs added via ADD from the local file system
* Add error to `docker build --rm`. This adds a missing error check to ensure failures to remove containers are detected and reported

### [Documentation](#documentation-4)

* Update issue filing instructions
* Warn against the use of symlinks for Docker's storage folder
* Replace the Firefox example with an IceWeasel example
* Rewrite the PostgreSQL example using a Dockerfile and add more details to it
* Improve the OS X documentation

### [Remote API](#remote-api-6)

* Fix broken images API for version less than 1.7
* Use the right encoding for all API endpoints which return JSON
* Move remote api client to api/
* Queue calls to the API using generic socket wait

### [Runtime](#runtime-37)

* Fix the use of custom settings for bridges and custom bridges
* Refactor the devicemapper code to avoid many mount/unmount race conditions and failures
* Remove two panics which could make Docker crash in some situations
* Don't ping registry from the CLI client
* Enable skip\_block\_zeroing for devicemapper. This stops devicemapper from always zeroing entire blocks
* Fix --run in `docker commit`. This makes docker commit store `--run` in the image configuration
* Remove directory when removing devicemapper device. This cleans up leftover mount directories
* Drop NET\_ADMIN capability for non-privileged containers. Unprivileged containers can't change their network configuration
* Ensure `docker cp` stream is closed properly
* Avoid extra mount/unmount during container registration. This removes an unneeded mount/unmount operation which was causing problems with devicemapper
* Stop allowing tcp\:// as a default tcp bin address which binds to 127.0.0.1:4243 and remove the default port

- Mount-bind the PTY as container console. This allows tmux and screen to run in a container

* Clean up archive closing. This fixes and improves archive handling
* Fix engine tests on systems where temp directories are symlinked
* Add test methods for save and load
* Avoid temporarily unmounting the container when restarting it. This fixes a race for devicemapper during restart
* Support submodules when building from a GitHub repository
* Quote volume path to allow spaces
* Fix remote tar ADD behavior. This fixes a regression which was causing Docker to extract tarballs

## [0.8.0 (2014-02-04)](#080-2014-02-04)

### [Notable features since 0.7.0](#notable-features-since-070)

* Images and containers can be removed much faster

* Building an image from source with docker build is now much faster

* The Docker daemon starts and stops much faster

* The memory footprint of many common operations has been reduced, by streaming files instead of buffering them in memory, fixing memory leaks, and fixing various suboptimal memory allocations

* Several race conditions were fixed, making Docker more stable under very high concurrency load. This makes Docker more stable and less likely to crash and reduces the memory footprint of many common operations

* All packaging operations are now built on the Go language’s standard tar implementation, which is bundled with Docker itself. This makes packaging more portable across host distributions, and solves several issues caused by quirks and incompatibilities between different distributions of tar

* Docker can now create, remove and modify larger numbers of containers and images graciously thanks to more aggressive releasing of system resources. For example the storage driver API now allows Docker to do reference counting on mounts created by the drivers With the ongoing changes to the networking and execution subsystems of docker testing these areas have been a focus of the refactoring. By moving these subsystems into separate packages we can test, analyze, and monitor coverage and quality of these packages

* Many components have been separated into smaller sub-packages, each with a dedicated test suite. As a result the code is better-tested, more readable and easier to change

* The ADD instruction now supports caching, which avoids unnecessarily re-uploading the same source content again and again when it hasn’t changed

* The new ONBUILD instruction adds to your image a “trigger” instruction to be executed at a later time, when the image is used as the base for another build

* Docker now ships with an experimental storage driver which uses the BTRFS filesystem for copy-on-write

* Docker is officially supported on Mac OS X

* The Docker daemon supports systemd socket activation

## [0.7.6 (2014-01-14)](#076-2014-01-14)

### [Builder](#builder-17)

* Do not follow symlink outside of build context

### [Runtime](#runtime-38)

* Remount bind mounts when ro is specified

- Use https for fetching docker version

### [Other](#other-1)

* Inline the test.docker.io fingerprint
* Add ca-certificates to packaging documentation

## [0.7.5 (2014-01-09)](#075-2014-01-09)

### [Builder](#builder-18)

* Disable compression for build. More space usage but a much faster upload

- Fix ADD caching for certain paths
- Do not compress archive from git build

### [Documentation](#documentation-5)

* Fix error in GROUP add example

- Make sure the GPG fingerprint is inline in the documentation
- Give more specific advice on setting up signing of commits for DCO

### [Runtime](#runtime-39)

* Fix misspelled container names
* Do not add hostname when networking is disabled

- Return most recent image from the cache by date

* Return all errors from docker wait

- Add Content-Type Header "application/json" to GET /version and /info responses

### [Other](#other-2)

* Update DCO to version 1.1

- Update Makefile to use "docker:GIT\_BRANCH" as the generated image name

* Update Travis to check for new 1.1 DCO version

## [0.7.4 (2014-01-07)](#074-2014-01-07)

### [Builder](#builder-19)

* Fix ADD caching issue with . prefixed path
* Fix docker build on devicemapper by reverting sparse file tar option
* Fix issue with file caching and prevent wrong cache hit

- Use same error handling while unmarshalling CMD and ENTRYPOINT

### [Documentation](#documentation-6)

* Simplify and streamline Amazon Quickstart
* Install instructions use unprefixed Fedora image
* Update instructions for mtu flag for Docker on GCE

- Add Ubuntu Saucy to installation

* Fix for wrong version warning on master instead of latest

### [Runtime](#runtime-40)

* Only get the image's rootfs when we need to calculate the image size
* Correctly handle unmapping UDP ports

- Make CopyFileWithTar use a pipe instead of a buffer to save memory on docker build

* Fix login message to say pull instead of push
* Fix "docker load" help by removing "SOURCE" prompt and mentioning STDIN

- Make blank -H option default to the same as no -H was sent
- Extract cgroups utilities to own submodule

### [Other](#other-3)

* Add Travis CI configuration to validate DCO and gofmt requirements
* Add Developer Certificate of Origin Text

- Upgrade VBox Guest Additions
- Check standalone header when pinging a registry server

## [0.7.3 (2014-01-02)](#073-2014-01-02)

### [Builder](#builder-20)

* Update ADD to use the image cache, based on a hash of the added content

- Add error message for empty Dockerfile

### [Documentation](#documentation-7)

* Fix outdated link to the "Introduction" on [www.docker.io](https://www.docker.io)

- Update the docs to get wider when the screen does

* Add information about needing to install LXC when using raw binaries

- Update Fedora documentation to disentangle the docker and docker.io conflict
- Add a note about using the new `-mtu` flag in several GCE zones

* Add FrugalWare installation instructions
* Add a more complete example of `docker run`

- Fix API documentation for creating and starting Privileged containers
- Add missing "name" parameter documentation on "/containers/create"

* Add a mention of `lxc-checkconfig` as a way to check for some of the necessary kernel configuration

- Update the 1.8 API documentation with some additions that were added to the docs for 1.7

### [Hack](#hack-4)

* Add missing libdevmapper dependency to the packagers documentation

- Update minimum Go requirement to a hard line at Go 1.2+
- Many minor improvements to the Vagrantfile

* Add ability to customize dockerinit search locations when compiling (to be used very sparingly only by packagers of platforms who require a nonstandard location)
* Add coverprofile generation reporting

- Add `-a` to our Go build flags, removing the need for recompiling the stdlib manually

* Update Dockerfile to be more canonical and have less spurious warnings during build

- Fix some miscellaneous `docker pull` progress bar display issues

* Migrate more miscellaneous packages under the "pkg" folder
* Update TextMate highlighting to automatically be enabled for files named "Dockerfile"
* Reorganize syntax highlighting files under a common "contrib/syntax" directory
* Update install.sh script (<https://get.docker.io/>) to not fail if busybox fails to download or run at the end of the Ubuntu/Debian installation
* Add support for container names in bash completion

### [Packaging](#packaging-2)

* Add an official Docker client binary for Darwin (Mac OS X)

- Remove empty "Vendor" string and added "License" on deb package

* Add a stubbed version of "/etc/default/docker" in the deb package

### [Runtime](#runtime-41)

* Update layer application to extract tars in place, avoiding file churn while handling whiteouts

- Fix permissiveness of mtime comparisons in tar handling (since GNU tar and Go tar do not yet support sub-second mtime precision)

* Reimplement `docker top` in pure Go to work more consistently, and even inside Docker-in-Docker (thus removing the shell injection vulnerability present in some versions of `lxc-ps`)

- Update `-H unix://` to work similarly to `-H tcp://` by inserting the default values for missing portions

* Fix more edge cases regarding dockerinit and deleted or replaced docker or dockerinit files

- Update container name validation to include '.'

* Fix use of a symlink or non-absolute path as the argument to `-g` to work as expected

- Update to handle external mounts outside of LXC, fixing many small mounting quirks and making future execution backends and other features simpler
- Update to use proper box-drawing characters everywhere in `docker images -tree`
- Move MTU setting from LXC configuration to directly use netlink
- Add `-S` option to external tar invocation for more efficient spare file handling

* Add arch/os info to User-Agent string, especially for registry requests
* Add `-mtu` option to Docker daemon for configuring MTU

- Fix `docker build` to exit with a non-zero exit code on error

* Add `DOCKER_HOST` environment variable to configure the client `-H` flag without specifying it manually for every invocation

## [0.7.2 (2013-12-16)](#072-2013-12-16)

### [Runtime](#runtime-42)

* Validate container names on creation with standard regex

- Increase maximum image depth to 127 from 42
- Continue to move api endpoints to the job api

* Add -bip flag to allow specification of dynamic bridge IP via CIDR

- Allow bridge creation when ipv6 is not enabled on certain systems

* Set hostname and IP address from within dockerinit
* Drop capabilities from within dockerinit

- Fix volumes on host when symlink is present the image
- Prevent deletion of image if ANY container is depending on it even if the container is not running

* Update docker push to use new progress display
* Use os.Lstat to allow mounting unix sockets when inspecting volumes

- Adjust handling of inactive user login
- Add missing defines in devicemapper for older kernels
- Allow untag operations with no container validation
- Add auth config to docker build

### [Documentation](#documentation-8)

* Add more information about Docker logging

- Add RHEL documentation

* Add a direct example for changing the CMD that is run in a container
* Update Arch installation documentation

- Add section on Trusted Builds
- Add Network documentation page

### [Other](#other-4)

* Add new cover bundle for providing code coverage reporting

- Separate integration tests in bundles
- Make Tianon the hack maintainer
- Update mkimage-debootstrap with more tweaks for keeping images small
- Use https to get the install script
- Remove vendored dotcloud/tar now that Go 1.2 has been released

## [0.7.1 (2013-12-05)](#071-2013-12-05)

### [Documentation](#documentation-9)

* Add @SvenDowideit as documentation maintainer
* Add links example
* Add documentation regarding ambassador pattern
* Add Google Cloud Platform docs
* Add dockerfile best practices

- Update doc for RHEL
- Update doc for registry
- Update Postgres examples
- Update doc for Ubuntu install
- Improve remote api doc

### [Runtime](#runtime-43)

* Add hostconfig to docker inspect
* Implement `docker log -f` to stream logs
* Add env variable to disable kernel version warning
* Add -format to `docker inspect`
* Support bind-mount for files

- Fix bridge creation on RHEL
- Fix image size calculation
- Make sure iptables are called even if the bridge already exists
- Fix issue with stderr only attach
- Remove init layer when destroying a container
- Fix same port binding on different interfaces
- `docker build` now returns the correct exit code
- Fix `docker port` to display correct port
- `docker build` now check that the dockerfile exists client side
- `docker attach` now returns the correct exit code
- Remove the name entry when the container does not exist

### [Registry](#registry-2)

* Improve progress bars, add ETA for downloads
* Simultaneous pulls now waits for the first to finish instead of failing

- Tag only the top-layer image when pushing to registry
- Fix issue with offline image transfer
- Fix issue preventing using ':' in password for registry

### [Other](#other-5)

* Add pprof handler for debug
* Create a Makefile

- Use stdlib tar that now includes fix
- Improve make.sh test script
- Handle SIGQUIT on the daemon
- Disable verbose during tests
- Upgrade to go1.2 for official build
- Improve unit tests
- The test suite now runs all tests even if one fails
- Refactor C in Go (Devmapper)

* Fix OS X compilation

## [0.7.0 (2013-11-25)](#070-2013-11-25)

### [Notable features since 0.6.0](#notable-features-since-060)

* Storage drivers: choose from aufs, device-mapper, or vfs.
* Standard Linux support: docker now runs on unmodified Linux kernels and all major distributions.
* Links: compose complex software stacks by connecting containers to each other.
* Container naming: organize your containers by giving them memorable names.
* Advanced port redirects: specify port redirects per interface, or keep sensitive ports private.
* Offline transfer: push and pull images to the filesystem without losing information.
* Quality: numerous bugfixes and small usability improvements. Significant increase in test coverage.

## [0.6.7 (2013-11-21)](#067-2013-11-21)

### [Runtime](#runtime-44)

* Improve stability, fixes some race conditions
* Skip the volumes mounted when deleting the volumes of container.
* Fix layer size computation: handle hard links correctly
* Use the work Path for docker cp CONTAINER:PATH
* Fix tmp dir never cleanup
* Speedup docker ps
* More informative error message on name collisions
* Fix nameserver regex
* Always return long id's
* Fix container restart race condition
* Keep published ports on docker stop;docker start
* Fix container networking on Fedora
* Correctly express "any address" to iptables
* Fix network setup when reconnecting to ghost container
* Prevent deletion if image is used by a running container
* Lock around read operations in graph

### [RemoteAPI](#remoteapi)

* Return full ID on docker rmi

### [Client](#client-12)

* Add -tree option to images
* Offline image transfer

- Exit with status 2 on usage error and display usage on stderr
- Do not forward SIGCHLD to container
- Use string timestamp for docker events -since

### [Other](#other-6)

* Update to go 1.2rc5

- Add /etc/default/docker support to upstart

## [0.6.6 (2013-11-06)](#066-2013-11-06)

### [Runtime](#runtime-45)

* Ensure container name on register
* Fix regression in /etc/hosts

- Add lock around write operations in graph

* Check if port is valid
* Fix restart runtime error with ghost container networking

- Add some more colors and animals to increase the pool of generated names

* Fix issues in docker inspect

- Escape apparmor confinement
- Set environment variables using a file.

* Prevent docker insert to erase something

- Prevent DNS server conflicts in CreateBridgeIface
- Validate bind mounts on the server side
- Use parent image config in docker build

* Fix regression in /etc/hosts

### [Client](#client-13)

* Add -P flag to publish all exposed ports
* Add -notrunc and -q flags to docker history

- Fix docker commit, tag and import usage

* Add stars, trusted builds and library flags in docker search

- Fix docker logs with tty

### [RemoteAPI](#remoteapi-1)

* Make /events API send headers immediately
* Do not split last column docker top

- Add size to history

### [Other](#other-7)

* Contrib: Desktop integration. Firefox usecase.
* Dockerfile: bump to go1.2rc3

## [0.6.5 (2013-10-29)](#065-2013-10-29)

### [Runtime](#runtime-46)

* Containers can now be named
* Containers can now be linked together for service discovery
* 'run -a', 'start -a' and 'attach' can forward signals to the container for better integration with process supervisors
* Automatically start crashed containers after a reboot
* Expose IP, port, and proto as separate environment vars for container links

- Allow ports to be published to specific ips
- Prohibit inter-container communication by default

* Ignore ErrClosedPipe for stdin in Container.Attach
* Remove unused field kernelVersion

- Fix issue when mounting subdirectories of /mnt in container

* Fix untag during removal of images

- Check return value of syscall.Chdir when changing working directory inside dockerinit

### [Client](#client-14)

* Only pass stdin to hijack when needed to avoid closed pipe errors

- Use less reflection in command-line method invocation

* Monitor the tty size after starting the container, not prior
* Remove useless os.Exit() calls after log.Fatal

### [Hack](#hack-5)

* Add initial init scripts library and a safer Ubuntu packaging script that works for Debian

- Add -p option to invoke debootstrap with http\_proxy

* Update install.sh with $sh\_c to get sudo/su for modprobe

- Update all the mkimage scripts to use --numeric-owner as a tar argument
- Update hack/release.sh process to automatically invoke hack/make.sh and bail on build and test issues

### [Other](#other-8)

* Documentation: Fix the flags for nc in example
* Testing: Remove warnings and prevent mount issues

- Testing: Change logic for tty resize to avoid warning in tests
- Builder: Fix race condition in docker build with verbose output
- Registry: Fix content-type for PushImageJSONIndex method

* Contrib: Improve helper tools to generate debian and Arch linux server images

## [0.6.4 (2013-10-16)](#064-2013-10-16)

### [Runtime](#runtime-47)

* Add cleanup of container when Start() fails

- Add better comments to utils/stdcopy.go
- Add utils.Errorf for error logging

* Add -rm to docker run for removing a container on exit

- Remove error messages which are not actually errors
- Fix `docker rm` with volumes
- Fix some error cases where an HTTP body might not be closed
- Fix panic with wrong dockercfg file
- Fix the attach behavior with -i

* Record termination time in state.

- Use empty string so TempDir uses the OS's temp dir automatically
- Make sure to close the network allocators

* Autorestart containers by default

- Bump vendor kr/pty to commit 3b1f6487b `(syscall.O_NOCTTY)`
- lxc: Allow set\_file\_cap capability in container

* Move run -rm to the cli only

- Split stdout stderr
- Always create a new session for the container

### [Testing](#testing)

* Add aggregated docker-ci email report
* Add cleanup to remove leftover containers

- Add nightly release to docker-ci
- Add more tests around auth.ResolveAuthConfig

* Remove a few errors in tests
* Catch errClosing error when TCP and UDP proxies are terminated

- Only run certain tests with TESTFLAGS='-run TestName' make.sh
- Prevent docker-ci to test closing PRs
- Replace panic by log.Fatal in tests

* Increase TestRunDetach timeout

### [Documentation](#documentation-10)

* Add initial draft of the Docker infrastructure doc
* Add devenvironment link to CONTRIBUTING.md
* Add `apt-get install curl` to Ubuntu docs
* Add explanation for export restrictions
* Add .dockercfg doc
* Remove Gentoo install notes about #1422 workaround
* Fix help text for -v option
* Fix Ping endpoint documentation

- Fix parameter names in docs for ADD command
- Fix ironic typo in changelog

* Various command fixes in postgres example
* Document how to edit and release docs

- Minor updates to `postgresql_service.rst`

* Clarify LGTM process to contributors

- Corrected error in the package name

* Document what `vagrant up` is actually doing

- improve doc search results

* Cleanup whitespace in API 1.5 docs
* use angle brackets in MAINTAINER example email
* Update archlinux.rst

- Changes to a new style for the docs. Includes version switcher.

* Formatting, add information about multiline json
* Improve registry and index REST API documentation

- Replace deprecated upgrading reference to docker-latest.tgz, which hasn't been updated since 0.5.3

* Update Gentoo installation documentation now that we're in the portage tree proper
* Cleanup and reorganize docs and tooling for contributors and maintainers

- Minor spelling correction of protocoll -> protocol

### [Contrib](#contrib-12)

* Add vim syntax highlighting for Dockerfiles from @honza
* Add mkimage-arch.sh
* Reorganize contributed completion scripts to add zsh completion

### [Hack](#hack-6)

* Add vagrant user to the docker group
* Add proper bash completion for "docker push"
* Add xz utils as a runtime dep
* Add cleanup/refactor portion of #2010 for hack and Dockerfile updates

- Add contrib/mkimage-centos.sh back (from #1621), and associated documentation link

* Add several of the small make.sh fixes from #1920, and make the output more consistent and contributor-friendly

- Add @tianon to hack/MAINTAINERS

* Improve network performance for VirtualBox
* Revamp install.sh to be usable by more people, and to use official install methods whenever possible (apt repo, portage tree, etc.)

- Fix contrib/mkimage-debian.sh apt caching prevention

* Add Dockerfile.tmLanguage to contrib

- Configured FPM to make /etc/init/docker.conf a config file
- Enable SSH Agent forwarding in Vagrant VM
- Several small tweaks/fixes for contrib/mkimage-debian.sh

### [Other](#other-9)

* Builder: Abort build if mergeConfig returns an error and fix duplicate error message
* Packaging: Remove deprecated packaging directory
* Registry: Use correct auth config when logging in.
* Registry: Fix the error message so it is the same as the regex

## [0.6.3 (2013-09-23)](#063-2013-09-23)

### [Packaging](#packaging-3)

* Add 'docker' group on install for ubuntu package
* Update tar vendor dependency
* Download apt key over HTTPS

### [Runtime](#runtime-48)

* Only copy and change permissions on non-bindmount volumes

- Allow multiple volumes-from

* Fix HTTP imports from STDIN

### [Documentation](#documentation-11)

* Update section on extracting the docker binary after build
* Update development environment docs for new build process
* Remove 'base' image from documentation

### [Other](#other-10)

* Client: Fix detach issue
* Registry: Update regular expression to match index

## [0.6.2 (2013-09-17)](#062-2013-09-17)

### [Runtime](#runtime-49)

* Add domainname support
* Implement image filtering with path.Match

- Remove unnecessary warnings
- Remove os/user dependency
- Only mount the hostname file when the config exists
- Handle signals within the `docker login` command

* UID and GID are now also applied to volumes
* `docker start` set error code upon error
* `docker run` set the same error code as the process started

### [Builder](#builder-21)

* Add -rm option in order to remove intermediate containers

- Allow multiline for the RUN instruction

### [Registry](#registry-3)

* Implement login with private registry

- Fix push issues

### [Other](#other-11)

* Hack: Vendor all dependencies

- Remote API: Bump to v1.5
- Packaging: Break down hack/make.sh into small scripts, one per 'bundle': test, binary, ubuntu etc.
- Documentation: General improvements

## [0.6.1 (2013-08-23)](#061-2013-08-23)

### [Registry](#registry-4)

* Pass "meta" headers in API calls to the registry

### [Packaging](#packaging-4)

* Use correct upstart script with new build tool
* Use libffi-dev, don't build it from sources
* Remove duplicate mercurial install command

## [0.6.0 (2013-08-22)](#060-2013-08-22)

### [Runtime](#runtime-50)

* Add lxc-conf flag to allow custom lxc options
* Add an option to set the working directory

- Add Image name to LogEvent tests

* Add -privileged flag and relevant tests, docs, and examples

- Add websocket support to /container//attach/ws
- Add warning when net.ipv4.ip\_forwarding = 0
- Add hostname to environment
- Add last stable version in `docker version`

* Fix race conditions in parallel pull
* Fix Graph ByParent() to generate list of child images per parent image.
* Fix typo: fmt.Sprint -> fmt.Sprintf
* Fix small \n error un docker build

- Fix to "Inject dockerinit at /.dockerinit"
- Fix #910. print user name to docker info output
- Use Go 1.1.2 for dockerbuilder
- Use ranged for loop on channels

* Use utils.ParseRepositoryTag instead of strings.Split(name, ":") in server.ImageDelete
* Improve CMD, ENTRYPOINT, and attach docs.
* Improve connect message with socket error
* Load authConfig only when needed and fix useless WARNING
* Show tag used when image is missing

- Apply volumes-from before creating volumes

* Make docker run handle SIGINT/SIGTERM
* Prevent crash when .dockercfg not readable
* Install script should be fetched over https, not http.

- API, issue 1471: Use groups for socket permissions

* Correctly detect IPv4 forwarding

- Mount /dev/shm as a tmpfs

* Switch from http to https for get.docker.io

- Let userland proxy handle container-bound traffic
- Update the Docker CLI to specify a value for the "Host" header.

* Change network range to avoid conflict with EC2 DNS
* Reduce connect and read timeout when pinging the registry

- Parallel pull

* Handle ip route showing mask-less IP addresses

- Allow ENTRYPOINT without CMD

* Always consider localhost as a domain name when parsing the FQN repos name

- Refactor checksum

### [Documentation](#documentation-12)

* Add MongoDB image example
* Add instructions for creating and using the docker group
* Add sudo to examples and installation to documentation
* Add ufw doc
* Add a reference to ps -a
* Add information about Docker's high level tools over LXC.
* Fix typo in docs for docker run -dns
* Fix a typo in the ubuntu installation guide
* Fix to docs regarding adding docker groups
* Update default -H docs
* Update readme with dependencies for building
* Update amazon.rst to explain that Vagrant is not necessary for running Docker on ec2
* PostgreSQL service example in documentation
* Suggest installing linux-headers by default.
* Change the twitter handle
* Clarify Amazon EC2 installation
* 'Base' image is deprecated and should no longer be referenced in the docs.
* Move note about officially supported kernel

- Solved the logo being squished in Safari

### [Builder](#builder-22)

* Add USER instruction do Dockerfile
* Add workdir support for the Buildfile

- Add no cache for docker build

* Fix docker build and docker events output
* Only count known instructions as build steps
* Make sure ENV instruction within build perform a commit each time
* Forbid certain paths within docker build ADD
* Repository name (and optionally a tag) in build usage
* Make sure ADD will create everything in 0755

### [Remote API](#remote-api-7)

* Sort Images by most recent creation date.
* Reworking opaque requests in registry module
* Add image name in /events
* Use mime pkg to parse Content-Type
* 650 http utils and user agent field

### [Hack](#hack-7)

* Bash Completion: Limit commands to containers of a relevant state

- Add docker dependencies coverage testing into docker-ci

### [Packaging](#packaging-5)

* Docker-brew 0.5.2 support and memory footprint reduction

- Add new docker dependencies into docker-ci

* Revert "docker.upstart: avoid spawning a `sh` process"

- Docker-brew and Docker standard library
- Release docker with docker

* Fix the upstart script generated by get.docker.io
* Enabled the docs to generate manpages.
* Revert Bind daemon to 0.0.0.0 in Vagrant.

### [Register](#register)

* Improve auth push
* Registry unit tests + mock registry

### [Tests](#tests)

* Improve TestKillDifferentUser to prevent timeout on buildbot

- Fix typo in TestBindMounts (runContainer called without image)

* Improve TestGetContainersTop so it does not rely on sleep
* Relax the lo interface test to allow iface index != 1
* Add registry functional test to docker-ci
* Add some tests in server and utils

### [Other](#other-12)

* Contrib: bash completion script
* Client: Add docker cp command and copy api endpoint to copy container files/folders to the host
* Don't read from stdout when only attached to stdin

## [0.5.3 (2013-08-13)](#053-2013-08-13)

### [Runtime](#runtime-51)

* Use docker group for socket permissions

- Spawn shell within upstart script
- Handle ip route showing mask-less IP addresses
- Add hostname to environment

### [Builder](#builder-23)

* Make sure ENV instruction within build perform a commit each time

## [0.5.2 (2013-08-08)](#052-2013-08-08)

* Builder: Forbid certain paths within docker build ADD

- Runtime: Change network range to avoid conflict with EC2 DNS

* API: Change daemon to listen on unix socket by default

## [0.5.1 (2013-07-30)](#051-2013-07-30)

### [Runtime](#runtime-52)

* Add `ps` args to `docker top`
* Add support for container ID files (pidfile like)
* Add container=lxc in default env
* Support networkless containers with `docker run -n` and `docker -d -b=none`

- Stdout/stderr logs are now stored in the same file as JSON
- Allocate a /16 IP range by default, with fallback to /24. Try 12 ranges instead of 3.
- Change .dockercfg format to json and support multiple auth remote

* Do not override volumes from config
* Fix issue with EXPOSE override

### [API](#api)

* Docker client now sets useragent (RFC 2616)
* Add /events endpoint

### [Builder](#builder-24)

* ADD command now understands URLs
* CmdAdd and CmdEnv now respect Dockerfile-set ENV variables

- Create directories with 755 instead of 700 within ADD instruction

### [Hack](#hack-8)

* Simplify unit tests with helpers
* Improve docker.upstart event
* Add coverage testing into docker-ci

## [0.5.0 (2013-07-17)](#050-2013-07-17)

### [Runtime](#runtime-53)

* List all processes running inside a container with 'docker top'
* Host directories can be mounted as volumes with 'docker run -v'
* Containers can expose public UDP ports (eg, '-p 123/udp')
* Optionally specify an exact public port (eg. '-p 80:4500')

- 'docker login' supports additional options

* Don't save a container's hostname when committing an image.

### [Registry](#registry-5)

* New image naming scheme inspired by Go packaging convention allows arbitrary combinations of registries

- Fix issues when uploading images to a private registry

### [Builder](#builder-25)

* ENTRYPOINT instruction sets a default binary entry point to a container
* VOLUME instruction marks a part of the container as persistent data

- 'docker build' displays the full output of a build by default

## [0.4.8 (2013-07-01)](#048-2013-07-01)

* Builder: New build operation ENTRYPOINT adds an executable entry point to the container. - Runtime: Fix a bug which caused 'docker run -d' to no longer print the container ID.

- Tests: Fix issues in the test suite

## [0.4.7 (2013-06-28)](#047-2013-06-28)

### [Remote API](#remote-api-8)

* The progress bar updates faster when downloading and uploading large files

- Fix a bug in the optional unix socket transport

### [Runtime](#runtime-54)

* Improve detection of kernel version

- Host directories can be mounted as volumes with 'docker run -b'

* fix an issue when only attaching to stdin

- Use 'tar --numeric-owner' to avoid uid mismatch across multiple hosts

### [Hack](#hack-9)

* Improve test suite and dev environment
* Remove dependency on unit tests on 'os/user'

### [Other](#other-13)

* Registry: easier push/pull to a custom registry

- Documentation: add terminology section

## [0.4.6 (2013-06-22)](#046-2013-06-22)

* Runtime: fix a bug which caused creation of empty images (and volumes) to crash.

## [0.4.5 (2013-06-21)](#045-2013-06-21)

* Builder: 'docker build git://URL' fetches and builds a remote git repository

- Runtime: 'docker ps -s' optionally prints container size
- Tests: improved and simplified

* Runtime: fix a regression introduced in 0.4.3 which caused the logs command to fail.
* Builder: fix a regression when using ADD with single regular file.

## [0.4.4 (2013-06-19)](#044-2013-06-19)

* Builder: fix a regression introduced in 0.4.3 which caused builds to fail on new clients.

## [0.4.3 (2013-06-19)](#043-2013-06-19)

### [Builder](#builder-26)

* ADD of a local file will detect tar archives and unpack them

- ADD improvements: use tar for copy + automatically unpack local archives
- ADD uses tar/untar for copies instead of calling 'cp -ar'
- Fix the behavior of ADD to be (mostly) reverse-compatible, predictable and well-documented.

* Fix a bug which caused builds to fail if ADD was the first command

- Nicer output for 'docker build'

### [Runtime](#runtime-55)

* Remove bsdtar dependency
* Add unix socket and multiple -H support
* Prevent rm of running containers
* Use go1.1 cookiejar

- Fix issue detaching from running TTY container
- Forbid parallel push/pull for a single image/repo. Fixes `#311`
- Fix race condition within Run command when attaching.

### [Client](#client-15)

* HumanReadable ProgressBar sizes in pull
* Fix docker version's git commit output

### [API](#api-1)

* Send all tags on History API call
* Add tag lookup to history command. Fixes #882

### [Documentation](#documentation-13)

* Fix missing command in irc bouncer example

## [0.4.2 (2013-06-17)](#042-2013-06-17)

* Packaging: Bumped version to work around an Ubuntu bug

## [0.4.1 (2013-06-17)](#041-2013-06-17)

### [Remote Api](#remote-api-9)

* Add flag to enable cross domain requests
* Add images and containers sizes in docker ps and docker images

### [Runtime](#runtime-56)

* Configure dns configuration host-wide with 'docker -d -dns'
* Detect faulty DNS configuration and replace it with a public default
* Allow docker run :
* You can now specify public port (ex: -p 80:4500)

- Improve image removal to garbage-collect unreferenced parents

### [Client](#client-16)

* Allow multiple params in inspect
* Print the container id before the hijack in `docker run`

### [Registry](#registry-6)

* Add regexp check on repo's name
* Move auth to the client

- Remove login check on pull

### [Other](#other-14)

* Vagrantfile: Add the rest api port to vagrantfile's port\_forward
* Upgrade to Go 1.1

- Builder: don`t ignore last line in Dockerfile when it doesn`t end with \n

## [0.4.0 (2013-06-03)](#040-2013-06-03)

### [Builder](#builder-27)

* Introducing Builder
* 'docker build' builds a container, layer by layer, from a source repository containing a Dockerfile

### [Remote API](#remote-api-10)

* Introducing Remote API
* control Docker programmatically using a simple HTTP/json API

### [Runtime](#runtime-57)

* Various reliability and usability improvements

## [0.3.4 (2013-05-30)](#034-2013-05-30)

### [Builder](#builder-28)

* 'docker build' builds a container, layer by layer, from a source repository containing a Dockerfile
* 'docker build -t FOO' applies the tag FOO to the newly built container.

### [Runtime](#runtime-58)

* Interactive TTYs correctly handle window resize

- Fix how configuration is merged between layers

### [Remote API](#remote-api-11)

* Split stdout and stderr on 'docker run'
* Optionally listen on a different IP and port (use at your own risk)

### [Documentation](#documentation-14)

* Improve install instructions.

## [0.3.3 (2013-05-23)](#033-2013-05-23)

* Registry: Fix push regression
* Various bugfixes

## [0.3.2 (2013-05-09)](#032-2013-05-09)

### [Registry](#registry-7)

* Improve the checksum process
* Use the size to have a good progress bar while pushing
* Use the actual archive if it exists in order to speed up the push

- Fix error 400 on push

### [Runtime](#runtime-59)

* Store the actual archive on commit

## [0.3.1 (2013-05-08)](#031-2013-05-08)

### [Builder](#builder-29)

* Implement the autorun capability within docker builder
* Add caching to docker builder
* Add support for docker builder with native API as top level command
* Implement ENV within docker builder

- Check the command existence prior create and add Unit tests for the case

* use any whitespaces instead of tabs

### [Runtime](#runtime-60)

* Add go version to debug infos

- Kernel version - don't show the dash if flavor is empty

### [Registry](#registry-8)

* Add docker search top level command in order to search a repository

- Fix pull for official images with specific tag
- Fix issue when login in with a different user and trying to push

* Improve checksum - async calculation

### [Images](#images)

* Output graph of images to dot (graphviz)

- Fix ByParent function

### [Documentation](#documentation-15)

* New introduction and high-level overview
* Add the documentation for docker builder

- CSS fix for docker documentation to make REST API docs look better.
- Fix CouchDB example page header mistake
- Fix README formatting

* Update [www.docker.io](https://www.docker.io) website.

### [Other](#other-15)

* Website: new high-level overview

- Makefile: Swap "go get" for "go get -d", especially to compile on go1.1rc

* Packaging: packaging ubuntu; issue #510: Use golang-stable PPA package to build docker

## [0.3.0 (2013-05-06)](#030-2013-05-06)

### [Runtime](#runtime-61)

* Fix the command existence check
* strings.Split may return an empty string on no match
* Fix an index out of range crash if cgroup memory is not

### [Documentation](#documentation-16)

* Various improvements

- New example: sharing data between 2 couchdb databases

### [Other](#other-16)

* Vagrant: Use only one deb line in /etc/apt

- Registry: Implement the new registry

## [0.2.2 (2013-05-03)](#022-2013-05-03)

* Support for data volumes ('docker run -v=PATH')
* Share data volumes between containers ('docker run -volumes-from')
* Improve documentation

- Upgrade to Go 1.0.3
- Various upgrades to the dev environment for contributors

## [0.2.1 (2013-05-01)](#021-2013-05-01)

* 'docker commit -run' bundles a layer with default runtime options: command, ports etc.

- Improve install process on Vagrant

* New Dockerfile operation: "maintainer"
* New Dockerfile operation: "expose"
* New Dockerfile operation: "cmd"
* Contrib script to build a Debian base layer
* 'docker -d -r': restart crashed containers at daemon startup

- Runtime: improve test coverage

## [0.2.0 (2013-04-23)](#020-2013-04-23)

* Runtime: ghost containers can be killed and waited for

- Documentation: update install instructions

* Packaging: fix Vagrantfile
* Development: automate releasing binaries and ubuntu packages

- Add a changelog

* Various bugfixes

## [0.1.8 (2013-04-22)](#018-2013-04-22)

* Dynamically detect cgroup capabilities
* Issue stability warning on kernels <3.8
* 'docker push' buffers on disk instead of memory
* Fix 'docker diff' for removed files
* Fix 'docker stop' for ghost containers
* Fix handling of pidfile
* Various bugfixes and stability improvements

## [0.1.7 (2013-04-18)](#017-2013-04-18)

* Container ports are available on localhost
* 'docker ps' shows allocated TCP ports
* Contributors can run 'make hack' to start a continuous integration VM
* Streamline ubuntu packaging & uploading
* Various bugfixes and stability improvements

## [0.1.6 (2013-04-17)](#016-2013-04-17)

* Record the author an image with 'docker commit -author'

## [0.1.5 (2013-04-17)](#015-2013-04-17)

* Disable standalone mode
* Use a custom DNS resolver with 'docker -d -dns'
* Detect ghost containers
* Improve diagnosis of missing system capabilities
* Allow disabling memory limits at compile time
* Add debian packaging
* Documentation: installing on Arch Linux
* Documentation: running Redis on docker
* Fix lxc 0.9 compatibility
* Automatically load aufs module
* Various bugfixes and stability improvements

## [0.1.4 (2013-04-09)](#014-2013-04-09)

* Full support for TTY emulation
* Detach from a TTY session with the escape sequence `C-p C-q`
* Various bugfixes and stability improvements
* Minor UI improvements
* Automatically create our own bridge interface 'docker0'

## [0.1.3 (2013-04-04)](#013-2013-04-04)

* Choose TCP frontend port with '-p :PORT'
* Layer format is versioned
* Major reliability improvements to the process manager
* Various bugfixes and stability improvements

## [0.1.2 (2013-04-03)](#012-2013-04-03)

* Set container hostname with 'docker run -h'
* Selective attach at run with 'docker run -a \[stdin\[,stdout\[,stderr]]]'
* Various bugfixes and stability improvements
* UI polish
* Progress bar on push/pull
* Use XZ compression by default
* Make IP allocator lazy

## [0.1.1 (2013-03-31)](#011-2013-03-31)

* Display shorthand IDs for convenience
* Stabilize process management
* Layers can include a commit message
* Simplified 'docker attach'
* Fix support for re-attaching
* Various bugfixes and stability improvements
* Auto-download at run
* Auto-login on push
* Beefed up documentation

## [0.1.0 (2013-03-23)](#010-2013-03-23)

Initial public release

* Implement registry in order to push/pull images
* TCP port allocation
* Fix termcaps on Linux
* Add documentation
* Add Vagrant support with Vagrantfile
* Add unit tests
* Add repository/tags to ease image management
* Improve the layer implementation

----
url: https://docs.docker.com/ai/model-runner/api-reference/
----

# DMR REST API

***

Table of contents

***

Once Model Runner is enabled, new API endpoints are available. You can use these endpoints to interact with a model programmatically. Docker Model Runner provides compatibility with OpenAI, Anthropic, and Ollama API formats.

## [Determine the base URL](#determine-the-base-url)

The base URL to interact with the endpoints depends on how you run Docker and which API format you're using.

| Access from          | Base URL                              |
| -------------------- | ------------------------------------- |
| Containers           | `http://model-runner.docker.internal` |
| Host processes (TCP) | `http://localhost:12434`              |

> Note
>
> TCP host access must be enabled. See [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner-in-docker-desktop).

| Access from    | Base URL                  |
| -------------- | ------------------------- |
| Containers     | `http://172.17.0.1:12434` |
| Host processes | `http://localhost:12434`  |

> Note
>
> The `172.17.0.1` interface may not be available by default to containers within a Compose project. In this case, add an `extra_hosts` directive to your Compose service YAML:
>
> ```yaml
> extra_hosts:
>   - "model-runner.docker.internal:host-gateway"
> ```
>
> Then you can access the Docker Model Runner APIs at `http://model-runner.docker.internal:12434/`

### [Base URLs for third-party tools](#base-urls-for-third-party-tools)

When configuring third-party tools that expect OpenAI-compatible APIs, use these base URLs:

| Tool type                 | Base URL format                     |
| ------------------------- | ----------------------------------- |
| OpenAI SDK / clients      | `http://localhost:12434/engines/v1` |
| Anthropic SDK / clients   | `http://localhost:12434`            |
| Ollama-compatible clients | `http://localhost:12434`            |

See [IDE and tool integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) for specific configuration examples.

## [Supported APIs](#supported-apis)

Docker Model Runner supports multiple API formats:

| API                                                     | Description                                    | Use case                            |
| ------------------------------------------------------- | ---------------------------------------------- | ----------------------------------- |
| [OpenAI API](#openai-compatible-api)                    | OpenAI-compatible chat completions, embeddings | Most AI frameworks and tools        |
| [Anthropic API](#anthropic-compatible-api)              | Anthropic-compatible messages endpoint         | Tools built for Claude              |
| [Ollama API](#ollama-compatible-api)                    | Ollama-compatible endpoints                    | Tools built for Ollama              |
| [Image Generation API](#image-generation-api-diffusers) | Diffusers-based image generation               | Generating images from text prompts |
| [DMR API](#dmr-native-endpoints)                        | Native Docker Model Runner endpoints           | Model management                    |

## [OpenAI-compatible API](#openai-compatible-api)

DMR implements the OpenAI API specification for maximum compatibility with existing tools and frameworks.

### [Endpoints](#endpoints)

| Endpoint                                | Method | Description                                                                            |
| --------------------------------------- | ------ | -------------------------------------------------------------------------------------- |
| `/engines/v1/models`                    | GET    | [List models](https://platform.openai.com/docs/api-reference/models/list)              |
| `/engines/v1/models/{namespace}/{name}` | GET    | [Retrieve model](https://platform.openai.com/docs/api-reference/models/retrieve)       |
| `/engines/v1/chat/completions`          | POST   | [Create chat completion](https://platform.openai.com/docs/api-reference/chat/create)   |
| `/engines/v1/completions`               | POST   | [Create completion](https://platform.openai.com/docs/api-reference/completions/create) |
| `/engines/v1/embeddings`                | POST   | [Create embeddings](https://platform.openai.com/docs/api-reference/embeddings/create)  |

> Note
>
> You can optionally include the engine name in the path: `/engines/llama.cpp/v1/chat/completions`. This is useful when running multiple inference engines.

### [Model name format](#model-name-format)

When specifying a model in API requests, use the full model identifier including the namespace:

```json
{
  "model": "ai/smollm2",
  "messages": [...]
}
```

Common model name formats:

* Docker Hub models: `ai/smollm2`, `ai/llama3.2`, `ai/qwen2.5-coder`
* Tagged versions: `ai/smollm2:360M-Q4_K_M`
* Custom models: `myorg/mymodel`

### [Supported parameters](#supported-parameters)

The following OpenAI API parameters are supported:

| Parameter           | Type         | Description                                              |
| ------------------- | ------------ | -------------------------------------------------------- |
| `model`             | string       | Required. The model identifier.                          |
| `messages`          | array        | Required for chat completions. The conversation history. |
| `prompt`            | string       | Required for completions. The prompt text.               |
| `max_tokens`        | integer      | Maximum tokens to generate.                              |
| `temperature`       | float        | Sampling temperature (0.0-2.0).                          |
| `top_p`             | float        | Nucleus sampling parameter (0.0-1.0).                    |
| `stream`            | Boolean      | Enable streaming responses.                              |
| `stop`              | string/array | Stop sequences.                                          |
| `presence_penalty`  | float        | Presence penalty (-2.0 to 2.0).                          |
| `frequency_penalty` | float        | Frequency penalty (-2.0 to 2.0).                         |

### [Limitations and differences from OpenAI](#limitations-and-differences-from-openai)

Be aware of these differences when using DMR's OpenAI-compatible API:

| Feature          | DMR behavior                                                           |
| ---------------- | ---------------------------------------------------------------------- |
| API key          | Not required. DMR ignores the `Authorization` header.                  |
| Function calling | Supported with llama.cpp for compatible models.                        |
| Vision           | Supported for multi-modal models (e.g., LLaVA).                        |
| JSON mode        | Supported via `response_format: {"type": "json_object"}`.              |
| Logprobs         | Supported.                                                             |
| Token counting   | Uses the model's native token encoder, which may differ from OpenAI's. |

## [Anthropic-compatible API](#anthropic-compatible-api)

DMR provides [Anthropic Messages API](https://platform.claude.com/docs/en/api/messages) compatibility for tools and frameworks built for Claude.

### [Endpoints](#endpoints-1)

| Endpoint                              | Method | Description                                                                 |
| ------------------------------------- | ------ | --------------------------------------------------------------------------- |
| `/anthropic/v1/messages`              | POST   | [Create a message](https://platform.claude.com/docs/en/api/messages/create) |
| `/anthropic/v1/messages/count_tokens` | POST   | [Count tokens](https://docs.anthropic.com/en/api/messages-count-tokens)     |

### [Supported parameters](#supported-parameters-1)

The following Anthropic API parameters are supported:

| Parameter        | Type    | Description                          |
| ---------------- | ------- | ------------------------------------ |
| `model`          | string  | Required. The model identifier.      |
| `messages`       | array   | Required. The conversation messages. |
| `max_tokens`     | integer | Maximum tokens to generate.          |
| `temperature`    | float   | Sampling temperature (0.0-1.0).      |
| `top_p`          | float   | Nucleus sampling parameter.          |
| `top_k`          | integer | Top-k sampling parameter.            |
| `stream`         | Boolean | Enable streaming responses.          |
| `stop_sequences` | array   | Custom stop sequences.               |
| `system`         | string  | System prompt.                       |

### [Example: Chat with Anthropic API](#example-chat-with-anthropic-api)

```bash
curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### [Example: Streaming response](#example-streaming-response)

```bash
curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "max_tokens": 1024,
    "stream": true,
    "messages": [
      {"role": "user", "content": "Count from 1 to 10"}
    ]
  }'
```

## [Ollama-compatible API](#ollama-compatible-api)

DMR also provides Ollama-compatible endpoints for tools and frameworks built for Ollama.

### [Endpoints](#endpoints-2)

| Endpoint          | Method | Description              |
| ----------------- | ------ | ------------------------ |
| `/api/tags`       | GET    | List available models    |
| `/api/show`       | POST   | Show model information   |
| `/api/chat`       | POST   | Generate chat completion |
| `/api/generate`   | POST   | Generate completion      |
| `/api/embeddings` | POST   | Generate embeddings      |

### [Example: Chat with Ollama API](#example-chat-with-ollama-api)

```bash
curl http://localhost:12434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/smollm2",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### [Example: List models](#example-list-models)

```bash
curl http://localhost:12434/api/tags
```

## [Image generation API (Diffusers)](#image-generation-api-diffusers)

DMR supports image generation through the Diffusers backend, enabling you to generate images from text prompts using models like Stable Diffusion.

> Note
>
> The Diffusers backend requires an NVIDIA GPU with CUDA support and is only available on Linux (x86\_64 and ARM64). See [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/#diffusers) for setup instructions.

### [Endpoint](#endpoint)

| Endpoint                                   | Method | Description                          |
| ------------------------------------------ | ------ | ------------------------------------ |
| `/engines/diffusers/v1/images/generations` | POST   | Generate an image from a text prompt |

### [Supported parameters](#supported-parameters-2)

| Parameter | Type   | Description                                                   |
| --------- | ------ | ------------------------------------------------------------- |
| `model`   | string | Required. The model identifier (e.g., `stable-diffusion:Q4`). |
| `prompt`  | string | Required. The text description of the image to generate.      |
| `size`    | string | Image dimensions in `WIDTHxHEIGHT` format (e.g., `512x512`).  |

### [Response format](#response-format)

The API returns a JSON response with the generated image encoded in base64:

```json
{
  "data": [
    {
      "b64_json": "<base64-encoded-image-data>"
    }
  ]
}
```

### [Example: Generate an image](#example-generate-an-image)

```bash
curl -s -X POST http://localhost:12434/engines/diffusers/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stable-diffusion:Q4",
    "prompt": "A picture of a nice cat",
    "size": "512x512"
  }' | jq -r '.data[0].b64_json' | base64 -d > image.png
```

This command:

1. Sends a POST request to the Diffusers image generation endpoint
2. Specifies the model, prompt, and output image size
3. Extracts the base64-encoded image from the response using `jq`
4. Decodes the base64 data and saves it as `image.png`

## [DMR native endpoints](#dmr-native-endpoints)

These endpoints are specific to Docker Model Runner for model management:

| Endpoint                     | Method | Description          |
| ---------------------------- | ------ | -------------------- |
| `/models/create`             | POST   | Pull/create a model  |
| `/models`                    | GET    | List local models    |
| `/models/{namespace}/{name}` | GET    | Get model details    |
| `/models/{namespace}/{name}` | DELETE | Delete a local model |

## [REST API examples](#rest-api-examples)

### [Request from within a container](#request-from-within-a-container)

To call the `chat/completions` OpenAI endpoint from within another container using `curl`:

```bash
#!/bin/sh

curl http://model-runner.docker.internal/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

### [Request from the host using TCP](#request-from-the-host-using-tcp)

To call the `chat/completions` OpenAI endpoint from the host via TCP:

1. Enable the host-side TCP support from the Docker Desktop GUI, or via the [Docker Desktop CLI](https://docs.docker.com/desktop/features/desktop-cli/). For example: `docker desktop enable model-runner --tcp <port>`.

   If you are running on Windows, also enable GPU-backed inference. See [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner-in-docker-desktop).

2. Interact with it as documented in the previous section using `localhost` and the correct port.

```bash
#!/bin/sh

curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "ai/smollm2",
      "messages": [
          {
              "role": "system",
              "content": "You are a helpful assistant."
          },
          {
              "role": "user",
              "content": "Please write 500 words about the fall of Rome."
          }
      ]
  }'
```

### [Request from the host using a Unix socket](#request-from-the-host-using-a-unix-socket)

To call the `chat/completions` OpenAI endpoint through the Docker socket from the host using `curl`:

```bash
#!/bin/sh

curl --unix-socket $HOME/.docker/run/docker.sock \
    localhost/exp/vDD4.40/engines/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ai/smollm2",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Please write 500 words about the fall of Rome."
            }
        ]
    }'
```

### [Streaming responses](#streaming-responses)

To receive streaming responses, set `stream: true`:

```bash
curl http://localhost:12434/engines/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
      "model": "ai/smollm2",
      "stream": true,
      "messages": [
          {"role": "user", "content": "Count from 1 to 10"}
      ]
  }'
```

## [Using with OpenAI SDKs](#using-with-openai-sdks)

### [Python](#python)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed"  # DMR doesn't require an API key
)

response = client.chat.completions.create(
    model="ai/smollm2",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### [Node.js](#nodejs)

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  baseURL: 'http://localhost:12434/engines/v1',
  apiKey: 'not-needed',
});

const response = await client.chat.completions.create({
  model: 'ai/smollm2',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(response.choices[0].message.content);
```

## [What's next](#whats-next)

* [IDE and tool integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) - Configure Cline, Continue, Cursor, and other tools
* [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Adjust context size and runtime parameters
* [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - Learn about llama.cpp, vLLM, and Diffusers options

----
url: https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/
----

# docker compose bridge transformations

***

| Description | Manage transformation images |
| ----------- | ---------------------------- |

## [Description](#description)

Manage transformation images

## [Subcommands](#subcommands)

| Command                                                                                                                               | Description                    |
| ------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| [`docker compose bridge transformations create`](https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/create/) | Create a new transformation    |
| [`docker compose bridge transformations list`](https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/list/)     | List available transformations |

----
url: https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/
----

# Securing Spring Boot microservice using Keycloak and Testcontainers

Table of contents

***

Learn how to create an OAuth 2.0 Resource Server using Spring Boot, secure API endpoints with Keycloak, and test the application using the Testcontainers Keycloak module.

**Time to complete** 30 minutes

In this guide, you'll learn how to:

* Create an OAuth 2.0 Resource Server using Spring Boot
* Secure API endpoints using Keycloak
* Test the APIs using the Testcontainers Keycloak module
* Run the application locally using the Testcontainers Keycloak module

## [Prerequisites](#prerequisites)

* Java 17+
* Maven or Gradle
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/create-project/)

   Set up a Spring Boot OAuth 2.0 Resource Server with Keycloak, PostgreSQL, and Testcontainers.

2. [Write tests](https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/write-tests/)

   Test the secured Spring Boot API endpoints using Testcontainers Keycloak and PostgreSQL modules.

3. [Run tests](https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/run-tests/)

   Run your Testcontainers-based Spring Boot Keycloak integration tests and explore next steps.

----
url: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/
----

# What is Docker Compose?

***

Table of contents

***

## [Explanation](#explanation)

If you've been following the guides so far, you've been working with single container applications. But, now you're wanting to do something more complicated - run databases, message queues, caches, or a variety of other services. Do you install everything in a single container? Run multiple containers? If you run multiple, how do you connect them all together?

One best practice for containers is that each container should do one thing and do it well. While there are exceptions to this rule, avoid the tendency to have one container do multiple things.

You can use multiple `docker run` commands to start multiple containers. But, you'll soon realize you'll need to manage networks, all of the flags needed to connect containers to those networks, and more. And when you're done, cleanup is a little more complicated.

With Docker Compose, you can define all of your containers and their configurations in a single YAML file. If you include this file in your code repository, anyone that clones your repository can get up and running with a single command.

It's important to understand that Compose is a declarative tool - you simply define it and go. You don't always need to recreate everything from scratch. If you make a change, run `docker compose up` again and Compose will reconcile the changes in your file and apply them intelligently.

> **Dockerfile versus Compose file**
>
> A Dockerfile provides instructions to build a container image while a Compose file defines your running containers. Quite often, a Compose file references a Dockerfile to build an image to use for a particular service.

## [Try it out](#try-it-out)

In this hands-on, you will learn how to use a Docker Compose to run a multi-container application. You'll use a simple to-do list app built with Node.js and MySQL as a database server.

### [Start the application](#start-the-application)

Follow the instructions to run the to-do list app on your system.

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.

2. Open a terminal and [clone this sample application](https://github.com/dockersamples/todo-list-app).

   ```console
   git clone https://github.com/dockersamples/todo-list-app 
   ```

3. Navigate into the `todo-list-app` directory:

   ```console
   cd todo-list-app
   ```

   Inside this directory, you'll find a file named `compose.yaml`. This YAML file is where all the magic happens! It defines all the services that make up your application, along with their configurations. Each service specifies its image, ports, volumes, networks, and any other settings necessary for its functionality. Take some time to explore the YAML file and familiarize yourself with its structure.

4. Use the [`docker compose up`](/reference/cli/docker/compose/up/) command to start the application:

   ```console
   docker compose up -d --build
   ```

   When you run this command, you should see an output like this:

   ```console
   [+] Running 5/5
   ✔ app 3 layers [⣿⣿⣿]      0B/0B            Pulled          7.1s
     ✔ e6f4e57cc59e Download complete                          0.9s
     ✔ df998480d81d Download complete                          1.0s
     ✔ 31e174fedd23 Download complete                          2.5s
     ✔ 43c47a581c29 Download complete                          2.0s
   [+] Running 4/4
     ⠸ Network todo-list-app_default           Created         0.3s
     ⠸ Volume "todo-list-app_todo-mysql-data"  Created         0.3s
     ✔ Container todo-list-app-app-1           Started         0.3s
     ✔ Container todo-list-app-mysql-1         Started         0.3s
   ```

   A lot happened here! A couple of things to call out:

   * Two container images were downloaded from Docker Hub - node and MySQL
   * A network was created for your application
   * A volume was created to persist the database files between container restarts
   * Two containers were started with all of their necessary config

   If this feels overwhelming, don't worry! You'll get there!

5. With everything now up and running, you can open <http://localhost:3000> in your browser to see the site. Note that the application may take 10-15 seconds to fully start. If the page doesn't load right away, wait a moment and refresh. Feel free to add items to the list, check them off, and remove them.

6. If you look at the Docker Desktop GUI, you can see the containers and dive deeper into their configuration.

### [Tear it down](#tear-it-down)

Since this application was started using Docker Compose, it's easy to tear it all down when you're done.

1. In the CLI, use the [`docker compose down`](/reference/cli/docker/compose/down/) command to remove everything:

   ```console
   docker compose down
   ```

   You'll see output similar to the following:

   ```console
   [+] Running 3/3
   ✔ Container todo-list-app-mysql-1  Removed        2.9s
   ✔ Container todo-list-app-app-1    Removed        0.1s
   ✔ Network todo-list-app_default    Removed        0.1s
   ```

   > **Volume persistence**
   >
   > By default, volumes *aren't* automatically removed when you tear down a Compose stack. The idea is that you might want the data back if you start the stack again.
   >
   > If you do want to remove the volumes, add the `--volumes` flag when running the `docker compose down` command:
   >
   > ```console
   > docker compose down --volumes
   > [+] Running 1/0
   > ✔ Volume todo-list-app_todo-mysql-data  Removed
   > ```

2. Alternatively, you can use the Docker Desktop GUI to remove the containers by selecting the application stack and selecting the **Delete** button.

   > **Using the GUI for Compose stacks**
   >
   > Note that if you remove the containers for a Compose app in the GUI, it's removing only the containers. You'll have to manually remove the network and volumes if you want to do so.

In this walkthrough, you learned how to use Docker Compose to start and stop a multi-container application.

## [Additional resources](#additional-resources)

This page was a brief introduction to Compose. In the following resources, you can dive deeper into Compose and how to write Compose files.

* [Overview of Docker Compose](/compose/)
* [Overview of Docker Compose CLI](/reference/cli/docker/compose/)
* [How Compose works](/compose/intro/compose-application-model/)

----
url: https://docs.docker.com/reference/cli/docker/image/pull/
----

# docker image pull

***

| Description                                                               | Download an image from a registry                 |
| ------------------------------------------------------------------------- | ------------------------------------------------- |
| Usage                                                                     | `docker image pull [OPTIONS] NAME[:TAG\|@DIGEST]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker pull`                                     |

## [Description](#description)

Most of your images will be created on top of a base image from the [Docker Hub](https://hub.docker.com) registry.

[Docker Hub](https://hub.docker.com) contains many pre-built images that you can `pull` and try without needing to define and configure your own.

To download a particular image, or set of images (i.e., a repository), use `docker pull`.

### [Proxy configuration](#proxy-configuration)

If you are behind an HTTP proxy server, for example in corporate settings, you may have to configure the Docker daemon to use the proxy server for operations such as pulling and pushing images. Refer to the [dockerd command-line reference](/reference/cli/dockerd/#proxy-configuration) for details.

### [Concurrent downloads](#concurrent-downloads)

By default the Docker daemon downloads three layers of an image at a time. If you are on a low bandwidth connection this may cause timeout issues and you may want to lower this via the `--max-concurrent-downloads` daemon option. See the [daemon documentation](/reference/cli/dockerd/) for more details.

## [Options](#options)

| Option                        | Default | Description                                                |
| ----------------------------- | ------- | ---------------------------------------------------------- |
| [`-a, --all-tags`](#all-tags) |         | Download all tagged images in the repository               |
| `--platform`                  |         | API 1.32+ Set platform if server is multi-platform capable |
| `-q, --quiet`                 |         | Suppress verbose output                                    |

## [Examples](#examples)

### [Pull an image from Docker Hub](#pull-an-image-from-docker-hub)

To download a particular image, or set of images (i.e., a repository), use `docker image pull` (or the `docker pull` shorthand). If no tag is provided, Docker Engine uses the `:latest` tag as a default. This example pulls the `debian:latest` image:

```console
$ docker image pull debian

Using default tag: latest
latest: Pulling from library/debian
e756f3fdd6a3: Pull complete
Digest: sha256:3f1d6c17773a45c97bd8f158d665c9709d7b29ed7917ac934086ad96f92e4510
Status: Downloaded newer image for debian:latest
docker.io/library/debian:latest
```

Docker images can consist of multiple layers. In the example above, the image consists of a single layer; `e756f3fdd6a3`.

Layers can be reused by images. For example, the `debian:bookworm` image shares its layer with the `debian:latest`. Pulling the `debian:bookworm` image therefore only pulls its metadata, but not its layers, because the layer is already present locally:

```console
$ docker image pull debian:bookworm

bookworm: Pulling from library/debian
Digest: sha256:3f1d6c17773a45c97bd8f158d665c9709d7b29ed7917ac934086ad96f92e4510
Status: Downloaded newer image for debian:bookworm
docker.io/library/debian:bookworm
```

To see which images are present locally, use the [`docker images`](/reference/cli/docker/image/ls/) command:

```console
$ docker images

REPOSITORY   TAG        IMAGE ID       CREATED        SIZE
debian       bookworm   4eacea30377a   8 days ago     124MB
debian       latest     4eacea30377a   8 days ago     124MB
```

Docker uses a content-addressable image store, and the image ID is a SHA256 digest covering the image's configuration and layers. In the example above, `debian:bookworm` and `debian:latest` have the same image ID because they are the same image tagged with different names. Because they are the same image, their layers are stored only once and do not consume extra disk space.

For more information about images, layers, and the content-addressable store, refer to [understand images, containers, and storage drivers](/engine/storage/drivers/).

### [Pull an image by digest (immutable identifier)](#pull-an-image-by-digest-immutable-identifier)

So far, you've pulled images by their name (and "tag"). Using names and tags is a convenient way to work with images. When using tags, you can `docker pull` an image again to make sure you have the most up-to-date version of that image. For example, `docker pull ubuntu:24.04` pulls the latest version of the Ubuntu 24.04 image.

In some cases you don't want images to be updated to newer versions, but prefer to use a fixed version of an image. Docker enables you to pull an image by its digest. When pulling an image by digest, you specify exactly which version of an image to pull. Doing so, allows you to "pin" an image to that version, and guarantee that the image you're using is always the same.

To know the digest of an image, pull the image first. Let's pull the latest `ubuntu:24.04` image from Docker Hub:

```console
$ docker pull ubuntu:24.04

24.04: Pulling from library/ubuntu
125a6e411906: Pull complete
Digest: sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
Status: Downloaded newer image for ubuntu:24.04
docker.io/library/ubuntu:24.04
```

Docker prints the digest of the image after the pull has finished. In the example above, the digest of the image is:

```console
sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
```

Docker also prints the digest of an image when pushing to a registry. This may be useful if you want to pin to a version of the image you just pushed.

A digest takes the place of the tag when pulling an image, for example, to pull the above image by digest, run the following command:

```console
$ docker pull ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30

docker.io/library/ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30: Pulling from library/ubuntu
Digest: sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
Status: Image is up to date for ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
docker.io/library/ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
```

Digest can also be used in the `FROM` of a Dockerfile, for example:

```dockerfile
FROM ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
LABEL org.opencontainers.image.authors="some maintainer <maintainer@example.com>"
```

> Note
>
> Using this feature "pins" an image to a specific version in time. Docker does therefore not pull updated versions of an image, which may include security updates. If you want to pull an updated image, you need to change the digest accordingly.

### [Pull from a different registry](#pull-from-a-different-registry)

By default, `docker pull` pulls images from [Docker Hub](https://hub.docker.com). It is also possible to manually specify the path of a registry to pull from. For example, if you have set up a local registry, you can specify its path to pull from it. A registry path is similar to a URL, but does not contain a protocol specifier (`https://`).

The following command pulls the `testing/test-image` image from a local registry listening on port 5000 (`myregistry.local:5000`):

```console
$ docker image pull myregistry.local:5000/testing/test-image
```

Registry credentials are managed by [docker login](/reference/cli/docker/login/).

Docker uses the `https://` protocol to communicate with a registry, unless the registry is allowed to be accessed over an insecure connection. Refer to the [insecure registries](/reference/cli/dockerd/#insecure-registries) section for more information.

### [Pull a repository with multiple images (-a, --all-tags)](#all-tags)

By default, `docker pull` pulls a single image from the registry. A repository can contain multiple images. To pull all images from a repository, provide the `-a` (or `--all-tags`) option when using `docker pull`.

This command pulls all images from the `ubuntu` repository:

```console
$ docker image pull --all-tags ubuntu

Pulling repository ubuntu
ad57ef8d78d7: Download complete
105182bb5e8b: Download complete
511136ea3c5a: Download complete
73bd853d2ea5: Download complete
....

Status: Downloaded newer image for ubuntu
```

After the pull has completed use the `docker image ls` command (or the `docker images` shorthand) to see the images that were pulled. The example below shows all the `ubuntu` images that are present locally:

```console
$ docker image ls --filter reference=ubuntu
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
ubuntu       22.04     8a3cdc4d1ad3   3 weeks ago    77.9MB
ubuntu       jammy     8a3cdc4d1ad3   3 weeks ago    77.9MB
ubuntu       24.04     35a88802559d   6 weeks ago    78.1MB
ubuntu       latest    35a88802559d   6 weeks ago    78.1MB
ubuntu       noble     35a88802559d   6 weeks ago    78.1MB
```

### [Cancel a pull](#cancel-a-pull)

Killing the `docker pull` process, for example by pressing `CTRL-c` while it is running in a terminal, will terminate the pull operation.

```console
$ docker pull ubuntu

Using default tag: latest
latest: Pulling from library/ubuntu
a3ed95caeb02: Pulling fs layer
236608c7b546: Pulling fs layer
^C
```

The Engine terminates a pull operation when the connection between the daemon and the client (initiating the pull) is cut or lost for any reason or the command is manually terminated.

----
url: https://docs.docker.com/reference/cli/docker/scout/vex/get/
----

# docker scout vex get

***

| Description | Get VEX attestation for image        |
| ----------- | ------------------------------------ |
| Usage       | `docker scout vex get OPTIONS IMAGE` |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

The docker scout vex get command gets a VEX attestation for images.

## [Options](#options)

| Option         | Default                                                    | Description                                                                                          |
| -------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `--key`        | `https://registry.scout.docker.com/keyring/dhi/latest.pub` | Signature key to use for verification                                                                |
| `--org`        |                                                            | Namespace of the Docker organization                                                                 |
| `-o, --output` |                                                            | Write the report to a file                                                                           |
| `--platform`   |                                                            | Platform of image to analyze                                                                         |
| `--ref`        |                                                            | Reference to use if the provided tarball contains multiple references. Can only be used with archive |
| `--skip-tlog`  |                                                            | Skip signature verification against public transaction log                                           |
| `--verify`     |                                                            | Verify the signature on the attestation                                                              |

----
url: https://docs.docker.com/guides/docker-scout/remediation/
----

# Remediation

***

***

Docker Scout's [remediation feature](https://docs.docker.com/scout/policy/remediation/) helps you address supply chain and security issues by offering tailored recommendations based on policy evaluations. These recommendations guide you in improving policy compliance or enhancing image metadata, allowing Docker Scout to perform more accurate evaluations in the future.

You can use this feature to ensure that your base images are up-to-date and that your supply chain attestations are complete. When a violation occurs, Docker Scout provides recommended fixes, such as updating your base image or adding missing attestations. If there isn’t enough information to determine compliance, Docker Scout suggests actions to help resolve the issue.

In the Docker Scout Dashboard, you can view and act on these recommendations by reviewing violations or compliance uncertainties. With integrations like GitHub, you can even automate updates, directly fixing issues from the dashboard.

[Common challenges and questions »](https://docs.docker.com/guides/docker-scout/common-questions/)

----
url: https://docs.docker.com/build/concepts/overview/
----

# Docker Build Overview

***

Table of contents

***

Docker Build implements a client-server architecture, where:

* Client: Buildx is the client and the user interface for running and managing builds.
* Server: BuildKit is the server, or builder, that handles the build execution.

When you invoke a build, the Buildx client sends a build request to the BuildKit backend. BuildKit resolves the build instructions and executes the build steps. The build output is either sent back to the client or uploaded to a registry, such as Docker Hub.

Buildx and BuildKit are both installed with Docker Desktop and Docker Engine out-of-the-box. When you invoke the `docker build` command, you're using Buildx to run a build using the default BuildKit bundled with Docker.

## [Buildx](#buildx)

Buildx is the CLI tool that you use to run builds. The `docker build` command is a wrapper around Buildx. When you invoke `docker build`, Buildx interprets the build options and sends a build request to the BuildKit backend.

The Buildx client can do more than just run builds. You can also use Buildx to create and manage BuildKit backends, referred to as builders. It also supports features for managing images in registries, and for running multiple builds concurrently.

Docker Buildx is installed by default with Docker Desktop. You can also build the CLI plugin from source, or grab a binary from the GitHub repository and install it manually. See [Buildx README](https://github.com/docker/buildx#manual-download) on GitHub for more information.

> Note
>
> While `docker build` invokes Buildx under the hood, there are subtle differences between this command and the canonical `docker buildx build`. For details, see [Difference between `docker build` and `docker buildx build`](https://docs.docker.com/build/builders/#difference-between-docker-build-and-docker-buildx-build).

## [BuildKit](#buildkit)

BuildKit is the daemon process that executes the build workloads.

A build execution starts with the invocation of a `docker build` command. Buildx interprets your build command and sends a build request to the BuildKit backend. The build request includes:

* The Dockerfile
* Build arguments
* Export options
* Caching options

BuildKit resolves the build instructions and executes the build steps. While BuildKit is executing the build, Buildx monitors the build status and prints the progress to the terminal.

If the build requires resources from the client, such as local files or build secrets, BuildKit requests the resources that it needs from Buildx.

This is one way in which BuildKit is more efficient compared to the legacy builder used in earlier versions of Docker. BuildKit only requests the resources that the build needs when they're needed. The legacy builder, in comparison, always takes a copy of the local filesystem.

Examples of resources that BuildKit can request from Buildx include:

* Local filesystem build contexts
* Build secrets
* SSH sockets
* Registry authentication tokens

For more information about BuildKit, see [BuildKit](https://docs.docker.com/build/buildkit/).

----
url: https://docs.docker.com/docker-hub/image-library/trusted-content/
----

# Trusted content

***

Table of contents

***

Docker Hub's trusted content provides a curated selection of high-quality, secure images designed to give developers confidence in the reliability and security of the resources they use. These images are stable, regularly updated, and adhere to industry best practices, making them a strong foundation for building and deploying applications. Docker Hub's trusted content includes Docker Official Images, Docker Hardened Images and charts, Verified Publisher images, and Docker-Sponsored Open Source Software images.

## [Docker Official Images](#docker-official-images)

The Docker Official Images are a curated set of Docker repositories hosted on Docker Hub.

Docker recommends you use the Docker Official Images in your projects. These images have clear documentation, promote best practices, and are regularly updated. Docker Official Images support most common use cases, making them perfect for new Docker users. Advanced users can benefit from more specialized image variants as well as review Docker Official Images as part of your `Dockerfile` learning process.

> Note
>
> Use of Docker Official Images is subject to [Docker's Terms of Service](https://www.docker.com/legal/docker-terms-service/).

These images provide essential base repositories that serve as the starting point for the majority of users.

These include operating systems such as [Ubuntu](https://hub.docker.com/_/ubuntu/) and [Alpine](https://hub.docker.com/_/alpine/), programming language runtimes such as [Python](https://hub.docker.com/_/python) and [Node](https://hub.docker.com/_/node), and other essential tools such as [memcached](https://hub.docker.com/_/memcached) and [MySQL](https://hub.docker.com/_/mysql).

The images are some of the [most secure images](https://www.docker.com/blog/enhancing-security-and-transparency-with-docker-official-images/) on Docker Hub. This is particularly important as Docker Official Images are some of the most popular on Docker Hub. Typically, Docker Official images have few or no packages containing CVEs.

The images exemplify [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/) and provide clear documentation to serve as a reference for other Dockerfile authors.

Images that are part of this program have a special badge on Docker Hub making it easier for you to identify projects that are part of Docker Official Images.

### [Supported tags and respective Dockerfile links](#supported-tags-and-respective-dockerfile-links)

The repository description for each Docker Official Image contains a **Supported tags and respective Dockerfile links** section that lists all the current tags with links to the Dockerfiles that created the image with those tags. The purpose of this section is to show what image variants are available.

Tags listed on the same line all refer to the same underlying image. Multiple tags can point to the same image. For example, in the previous screenshot taken from the `ubuntu` Docker Official Images repository, the tags `24.04`, `noble-20240225`, `noble`, and `devel` all refer to the same image.

The `latest` tag for a Docker Official Image is often optimized for ease of use and includes a wide variety of useful software, such as developer and build tools. By tagging an image as `latest`, the image maintainers are essentially suggesting that image be used as the default. In other words, if you do not know what tag to use or are unfamiliar with the underlying software, you should probably start with the `latest` image. As your understanding of the software and image variants advances, you may find other image variants better suit your needs.

### [Slim images](#slim-images)

A number of language stacks such as [Node.js](https://hub.docker.com/_/node/), [Python](https://hub.docker.com/_/python/), and [Ruby](https://hub.docker.com/_/ruby/) have `slim` tag variants designed to provide a lightweight, production-ready base image with fewer packages.

A typical consumption pattern for `slim` images is as the base image for the final stage of a [multi-staged build](https://docs.docker.com/build/building/multi-stage/). For example, you build your application in the first stage of the build using the `latest` variant and then copy your application into the final stage based upon the `slim` variant. Here is an example `Dockerfile`.

```dockerfile
FROM node:latest AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . ./
FROM node:slim
WORKDIR /app
COPY --from=build /app /app
CMD ["node", "app.js"]
```

### [Alpine images](#alpine-images)

Many Docker Official Images repositories also offer `alpine` variants. These images are built on top of the [Alpine Linux](https://www.alpinelinux.org/) distribution rather than Debian or Ubuntu. Alpine Linux is focused on providing a small, simple, and secure base for container images, and Docker Official Images `alpine` variants typically aim to install only necessary packages. As a result, Docker Official Images `alpine` variants are typically even smaller than `slim` variants.

The main caveat to note is that Alpine Linux uses [musl libc](https://musl.libc.org/) instead of [glibc](https://www.gnu.org/software/libc/). Additionally, to minimize image size, it's uncommon for Alpine-based images to include tools such as Git or Bash by default. Depending on the depth of libc requirements or assumptions in your programs, you may find yourself running into issues due to missing libraries or tools.

When you use Alpine images as a base, consider the following options in order to make your program compatible with Alpine Linux and musl:

* Compile your program against musl libc
* Statically link glibc libraries into your program
* Avoid C dependencies altogether (for example, build Go programs without CGO)
* Add the software you need yourself in your Dockerfile.

Refer to the `alpine` image [description](https://hub.docker.com/_/alpine) on Docker Hub for examples on how to install packages if you are unfamiliar.

### [Codenames](#codenames)

Tags with words that look like Toy Story characters (for example, `bookworm`, `bullseye`, and `trixie`) or adjectives (such as `jammy`, and `noble`), indicate the codename of the Linux distribution they use as a base image. Debian release codenames are [based on Toy Story characters](https://en.wikipedia.org/wiki/Debian_version_history#Naming_convention), and Ubuntu's take the form of "Adjective Animal". For example, the codename for Ubuntu 24.04 is "Noble Numbat".

Linux distribution indicators are helpful because many Docker Official Images provide variants built upon multiple underlying distribution versions (for example, `postgres:bookworm` and `postgres:bullseye`).

### [Other tags](#other-tags)

Docker Official Images tags may contain other hints to the purpose of their image variant in addition to those described here. Often these tag variants are explained in the Docker Official Images repository documentation. Reading through the "How to use this image" and "Image Variants" sections will help you to understand how to use these variants.

### [Troubleshooting failed pulls](#troubleshooting-failed-pulls)

If you're experiencing failed pulls of Docker Official Images, check whether the `DOCKER_CONTENT_TRUST` environment variable is set to `1`. Docker Content Trust is being retired and the service is no longer reliable for pulls. To resolve pull failures, unset `DOCKER_CONTENT_TRUST`. For more information, see [Docker Content Trust (DCT)](https://docs.docker.com/retired/#docker-content-trust-dct).

## [Docker Hardened Images](#docker-hardened-images)

Docker Hardened Images (DHI) are minimal, secure, and production-ready container base and application images maintained by Docker. DHI also includes Docker-provided hardened Helm charts built from upstream sources and published as OCI artifacts in Docker Hub.

DHI is designed to reduce vulnerabilities and simplify compliance while fitting into existing Docker workflows with little to no retooling required. Docker maintains near-zero CVEs in DHI images, and DHI images and charts include signed security metadata such as SBOMs and provenance attestations.

Image and chart repositories have special badges on Docker Hub, making it easier to identify trusted DHI content.

To browse available repositories, see the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog). For implementation guidance, see [Docker Hardened Images](/dhi/).

## [Verified Publisher images](#verified-publisher-images)

The Docker Verified Publisher program provides high-quality images from commercial publishers verified by Docker.

These images help development teams build secure software supply chains, minimizing exposure to malicious content early in the process to save time and money later.

Images that are part of this program have a special badge on Docker Hub making it easier for users to identify projects that Docker has verified as high-quality commercial publishers.

## [Docker-Sponsored Open Source Software images](#docker-sponsored-open-source-software-images)

The Docker-Sponsored Open Source Software (OSS) program provides images that are published and maintained by open-source projects sponsored by Docker.

Images that are part of this program have a special badge on Docker Hub making it easier for users to identify projects that Docker has verified as trusted, secure, and active open-source projects.

----
url: https://docs.docker.com/reference/cli/docker/buildx/imagetools/create/
----

# docker buildx imagetools create

***

| Description | Create a new image based on source images               |
| ----------- | ------------------------------------------------------- |
| Usage       | `docker buildx imagetools create [OPTIONS] [SOURCE...]` |

## [Description](#description)

Create a new manifest list based on source manifests. The source manifests can be manifest lists or single platform distribution manifests and must already exist in the registry where the new manifest is created.

If only one source is specified and that source is a manifest list or image index, create performs a carbon copy. If one source is specified and that source is *not* a list or index, the output will be a manifest list, however you can disable this behavior with `--prefer-index=false` which attempts to preserve the source manifest format in the output.

## [Options](#options)

| Option                              | Default | Description                                                                                                                    |
| ----------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [`--annotation`](#annotation)       |         | Add annotation to the image                                                                                                    |
| [`--append`](#append)               |         | Append to existing manifest                                                                                                    |
| [`--dry-run`](#dry-run)             |         | Show final image instead of pushing                                                                                            |
| [`-f, --file`](#file)               |         | Read source descriptor from file                                                                                               |
| [`--metadata-file`](#metadata-file) |         | Write create result metadata to a file                                                                                         |
| `-p, --platform`                    |         | Filter specified platforms of target image                                                                                     |
| `--prefer-index`                    | `true`  | When only a single source is specified, prefer outputting an image index or manifest list instead of performing a carbon copy  |
| `--progress`                        | `auto`  | Set type of progress output (`auto`, `none`, `plain`, `rawjson`, `tty`). Use plain to show container output                    |
| [`-t, --tag`](#tag)                 |         | Set reference for new image                                                                                                    |

## [Examples](#examples)

### [Add annotations to an image (--annotation)](#annotation)

The `--annotation` flag lets you add annotations the image index, manifest, and descriptors when creating a new image.

The following command creates a `foo/bar:latest` image with the `org.opencontainers.image.authors` annotation on the image index.

```console
$ docker buildx imagetools create \
  --annotation "index:org.opencontainers.image.authors=dvdksn" \
  --tag foo/bar:latest \
  foo/bar:alpha foo/bar:beta foo/bar:gamma
```

> Note
>
> The `imagetools create` command supports adding annotations to the image index and descriptor, using the following type prefixes:
>
> * `index:`
> * `manifest-descriptor:`
>
> It doesn't support annotating manifests or OCI layouts.

For more information about annotations, see [Annotations](/build/building/annotations/).

### [Append new sources to an existing manifest list (--append)](#append)

Use the `--append` flag to append the new sources to an existing manifest list in the destination.

### [Override the configured builder instance (--builder)](#builder)

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).

### [Show final image instead of pushing (--dry-run)](#dry-run)

Use the `--dry-run` flag to not push the image, just show it.

### [Read source descriptor from a file (-f, --file)](#file)

```text
-f FILE or --file FILE
```

Reads source from files. A source can be a manifest digest, manifest reference, or a JSON of OCI descriptor object.

In order to define annotations or additional platform properties like `os.version` and `os.features` you need to add them in the OCI descriptor object encoded in JSON.

```console
$ docker buildx imagetools inspect --raw alpine | jq '.manifests[0] | .platform."os.version"="10.1"' > descr.json
$ docker buildx imagetools create -f descr.json myuser/image
```

The descriptor in the file is merged with existing descriptor in the registry if it exists.

The supported fields for the descriptor are defined in [OCI spec](https://github.com/opencontainers/image-spec/blob/master/descriptor.md#properties) .

### [Write create result metadata to a file (--metadata-file)](#metadata-file)

To output metadata such as the image digest, pass the `--metadata-file` flag. The metadata will be written as a JSON object to the specified file. The directory of the specified file must already exist and be writable.

```console
$ docker buildx imagetools create -t user/app:latest -f image1 -f image2 --metadata-file metadata.json
$ cat metadata.json
```

```json
{
  "containerimage.descriptor": {
    "mediaType": "application/vnd.oci.image.index.v1+json",
    "digest": "sha256:19ffeab6f8bc9293ac2c3fdf94ebe28396254c993aea0b5a542cfb02e0883fa3",
    "size": 4654
  },
  "image.name": "docker.io/user/app"
}
```

### [Set reference for new image (-t, --tag)](#tag)

```text
-t IMAGE or --tag IMAGE
```

Use the `-t` or `--tag` flag to set the name of the image to be created.

```console
$ docker buildx imagetools create --dry-run alpine@sha256:5c40b3c27b9f13c873fefb2139765c56ce97fd50230f1f2d5c91e55dec171907 sha256:c4ba6347b0e4258ce6a6de2401619316f982b7bcc529f73d2a410d0097730204
$ docker buildx imagetools create -t tonistiigi/myapp -f image1 -f image2
```

----
url: https://docs.docker.com/reference/cli/docker/container/cp/
----

# docker container cp

***

| Description                                                               | Copy files/folders between a container and the local filesystem                                                     |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Usage                                                                     | `docker container cp [OPTIONS] CONTAINER:SRC_PATH DEST_PATH\|- docker cp [OPTIONS] SRC_PATH\|- CONTAINER:DEST_PATH` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker cp`                                                                                                         |

## [Description](#description)

The `docker cp` utility copies the contents of `SRC_PATH` to the `DEST_PATH`. You can copy from the container's file system to the local machine or the reverse, from the local filesystem to the container. If `-` is specified for either the `SRC_PATH` or `DEST_PATH`, you can also stream a tar archive from `STDIN` or to `STDOUT`. The `CONTAINER` can be a running or stopped container. The `SRC_PATH` or `DEST_PATH` can be a file or directory.

The `docker cp` command assumes container paths are relative to the container's `/` (root) directory. This means supplying the initial forward slash is optional; The command sees `compassionate_darwin:/tmp/foo/myfile.txt` and `compassionate_darwin:tmp/foo/myfile.txt` as identical. Local machine paths can be an absolute or relative value. The command interprets a local machine's relative paths as relative to the current working directory where `docker cp` is run.

The `cp` command behaves like the Unix `cp -a` command in that directories are copied recursively with permissions preserved if possible. Ownership is set to the user and primary group at the destination. For example, files copied to a container are created with `UID:GID` of the root user. Files copied to the local machine are created with the `UID:GID` of the user which invoked the `docker cp` command. However, if you specify the `-a` option, `docker cp` sets the ownership to the user and primary group at the source. If you specify the `-L` option, `docker cp` follows any symbolic link in the `SRC_PATH`. `docker cp` doesn't create parent directories for `DEST_PATH` if they don't exist.

Assuming a path separator of `/`, a first argument of `SRC_PATH` and second argument of `DEST_PATH`, the behavior is as follows:

* `SRC_PATH` specifies a file

  * `DEST_PATH` does not exist
    * the file is saved to a file created at `DEST_PATH`
  * `DEST_PATH` does not exist and ends with `/`
    * Error condition: the destination directory must exist.
  * `DEST_PATH` exists and is a file
    * the destination is overwritten with the source file's contents
  * `DEST_PATH` exists and is a directory
    * the file is copied into this directory using the basename from `SRC_PATH`

* `SRC_PATH` specifies a directory

  * `DEST_PATH` does not exist
    * `DEST_PATH` is created as a directory and the *contents* of the source directory are copied into this directory

  * `DEST_PATH` exists and is a file
    * Error condition: cannot copy a directory to a file

  * `DEST_PATH` exists and is a directory

    * `SRC_PATH` does not end with `/.` (that is: *slash* followed by *dot*)
      * the source directory is copied into this directory
    * `SRC_PATH` does end with `/.` (that is: *slash* followed by *dot*)
      * the *content* of the source directory is copied into this directory

The command requires `SRC_PATH` and `DEST_PATH` to exist according to the above rules. If `SRC_PATH` is local and is a symbolic link, the symbolic link, not the target, is copied by default. To copy the link target and not the link, specify the `-L` option.

A colon (`:`) is used as a delimiter between `CONTAINER` and its path. You can also use `:` when specifying paths to a `SRC_PATH` or `DEST_PATH` on a local machine, for example `file:name.txt`. If you use a `:` in a local machine path, you must be explicit with a relative or absolute path, for example:

```
`/path/to/file:name.txt` or `./file:name.txt`
```

## [Options](#options)

| Option              | Default | Description                                                                                                   |
| ------------------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| `-a, --archive`     |         | Archive mode (copy all uid/gid information)                                                                   |
| `-L, --follow-link` |         | Always follow symlinks in SRC\_PATH                                                                           |
| `-q, --quiet`       |         | Suppress progress output during copy. Progress output is automatically suppressed if no terminal is attached  |

## [Examples](#examples)

Copy a local file into container

```console
$ docker cp ./some_file CONTAINER:/work
```

Copy files from container to local path

```console
$ docker cp CONTAINER:/var/logs/ /tmp/app_logs
```

Copy a file from container to stdout. Note `cp` command produces a tar stream

```console
$ docker cp CONTAINER:/var/logs/app.log - | tar x -O | grep "ERROR"
```

### [Corner cases](#corner-cases)

It isn't possible to copy certain system files such as resources under `/proc`, `/sys`, `/dev`, [tmpfs](/reference/cli/docker/container/run/#tmpfs), and mounts created by the user in the container. However, you can still copy such files by manually running `tar` in `docker exec`. Both of the following examples do the same thing in different ways (consider `SRC_PATH` and `DEST_PATH` are directories):

```console
$ docker exec CONTAINER tar Ccf $(dirname SRC_PATH) - $(basename SRC_PATH) | tar Cxf DEST_PATH -
```

```console
$ tar Ccf $(dirname SRC_PATH) - $(basename SRC_PATH) | docker exec -i CONTAINER tar Cxf DEST_PATH -
```

Using `-` as the `SRC_PATH` streams the contents of `STDIN` as a tar archive. The command extracts the content of the tar to the `DEST_PATH` in container's filesystem. In this case, `DEST_PATH` must specify a directory. Using `-` as the `DEST_PATH` streams the contents of the resource as a tar archive to `STDOUT`.

----
url: https://docs.docker.com/guides/testcontainers-java-wiremock/
----

# Testing REST API integrations using WireMock

Table of contents

***

Learn how to create a Spring Boot application that integrates with external REST APIs, then test those integrations using Testcontainers and WireMock.

**Time to complete** 20 minutes

In this guide, you'll learn how to:

* Create a Spring Boot application that talks to external REST APIs
* Test external API integrations using WireMock with both the JUnit 5 extension and the Testcontainers WireMock module

## [Prerequisites](#prerequisites)

* Java 17+
* Maven or Gradle
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-java-wiremock/create-project/)

   Set up a Spring Boot project with an external REST API integration using WireMock and Testcontainers.

2. [Write tests](https://docs.docker.com/guides/testcontainers-java-wiremock/write-tests/)

   Test external REST API integrations using WireMock with both the JUnit 5 extension and the Testcontainers WireMock module.

3. [Run tests](https://docs.docker.com/guides/testcontainers-java-wiremock/run-tests/)

   Run your Testcontainers WireMock integration tests and explore next steps.

----
url: https://docs.docker.com/reference/cli/docker/model/start-runner/
----

# docker model start-runner

***

| Description | Start Docker Model Runner (Docker Engine only) |
| ----------- | ---------------------------------------------- |
| Usage       | `docker model start-runner`                    |

## [Description](#description)

This command starts the Docker Model Runner without pulling container images. Use this command to start the runner when you already have the required images locally.

For the first-time setup or to ensure you have the latest images, use `docker model install-runner` instead.

## [Options](#options)

| Option           | Default     | Description                                                                                             |
| ---------------- | ----------- | ------------------------------------------------------------------------------------------------------- |
| `--backend`      |             | Specify backend (llama.cpp\|vllm\|diffusers). Default: llama.cpp                                        |
| `--debug`        |             | Enable debug logging                                                                                    |
| `--do-not-track` |             | Do not track models usage in Docker Model Runner                                                        |
| `--gpu`          | `auto`      | Specify GPU support (none\|auto\|cuda\|rocm\|musa\|cann)                                                |
| `--host`         | `127.0.0.1` | Host address to bind Docker Model Runner                                                                |
| `--port`         |             | Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode)  |
| `--proxy-cert`   |             | Path to a CA certificate file for proxy SSL inspection                                                  |
| `--tls`          |             | Enable TLS/HTTPS for Docker Model Runner API                                                            |
| `--tls-cert`     |             | Path to TLS certificate file (auto-generated if not provided)                                           |
| `--tls-key`      |             | Path to TLS private key file (auto-generated if not provided)                                           |
| `--tls-port`     |             | TLS port for Docker Model Runner (default: 12444 for Docker Engine, 12445 for Cloud mode)               |

----
url: https://docs.docker.com/reference/api/dvp/latest.yaml
----

openapi: 3.0.0
info:
 title: DVP Data API
 version: 1.0.0
 x-logo:
 url: https://docs.docker.com/assets/images/logo-docker-main.png
 href: /reference
 description: \|
 The Docker DVP Data API allows \[Docker Verified Publishers\](https://docs.docker.com/docker-hub/publish/) to view image pull analytics data for their namespaces. Analytics data can be retrieved in a CSV as raw data, or in a summary format.

 #### Summary data

 In your summary data CSV, you will have access to the data points listed below. You can request summary data for a complete week (Monday through Sunday) or for a complete month (available on the first day of the following month).

 There are two levels of summary data:

 \- Repository-level, a summary of every namespace and repository
 \- Tag- or digest-level, a summary of every namespace, repository, and reference
 (tag or digest)

 The summary data formats contain the following data points:

 \- Unique IP address count
 \- Pulls by tag count
 \- Pulls by digest count
 \- Version check count

 #### Raw data

 In your raw data CSV you will have access to the data points listed below. You can request raw data for a complete week (Monday through Sunday) or for a complete month (available on the first day of the following month). \*\*Note:\*\* each action is represented as a single row.

 \- Type (industry)
 \- Host (cloud provider)
 \- Country (geolocation)
 \- Timestamp
 \- Namespace
 \- Repository
 \- Reference (digest is always included, tag is provided when available)
 \- HTTP request method
 \- Action, one of the following:
 \- Pull by tag
 \- Pull by digest
 \- Version check
 \- User-Agent

servers:
 \- url: https://hub.docker.com/api/publisher/analytics/v1
security:
 \- HubAuth: \[\]

features.openapi:
 schemaDefinitionsTagName: Schemas

tags:
 \- name: authentication
 x-displayName: Authentication Endpoints
 \- name: namespaces
 x-displayName: Namespace data
 \- name: discovery
 x-displayName: Discovery
 \- name: responseDataFile
 x-displayName: ResponseDataFile
 description: \|

 \- name: yearModel
 x-displayName: Year Data Model
 description: \|

 \- name: monthModel
 x-displayName: Month Data Model
 description: \|

 \- name: weekModel
 x-displayName: Week Data Model
 description: \|


x-tagGroups:
 \- name: API
 tags:
 \- authentication
 \- discovery
 \- namespaces
 \- name: Models
 tags:
 \- responseDataFile
 \- yearModel
 \- monthModel
 \- weekModel

paths:
 /v2/users/login:
 security: \[\]
 servers:
 \- url: https://hub.docker.com
 post:
 security: \[\]
 tags:
 \- authentication
 summary: Create an authentication token
 operationId: PostUsersLogin
 description: \|
 Creates and returns a bearer token in JWT format that you can use to
 authenticate with Docker Hub APIs.

 The returned token is used in the HTTP Authorization header like \`Authorization: Bearer {TOKEN}\`.

 Most Docker Hub APIs require this token either to consume or to get detailed information. For example, to list images in a private repository.
 requestBody:
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/UsersLoginRequest"
 description: Login details.
 required: true
 responses:
 200:
 description: Authentication successful
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/PostUsersLoginSuccessResponse"
 401:
 description: Authentication failed or second factor required
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/PostUsersLoginErrorResponse"
 /v2/users/2fa-login:
 security: \[\]
 servers:
 \- url: https://hub.docker.com
 post:
 security: \[\]
 tags:
 \- authentication
 summary: Second factor authentication
 operationId: PostUsers2FALogin
 description: \|
 When a user has 2FA enabled, this is the second call to perform after
 \`/v2/users/login\` call.

 Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs.

 The returned token is used in the HTTP Authorization header like \`Authorization: Bearer {TOKEN}\`.

 Most Docker Hub APIs require this token either to consume or to get detailed information. For example, to list images in a private repository.
 requestBody:
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Users2FALoginRequest"
 description: Login details.
 required: true
 responses:
 200:
 description: Authentication successful
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/PostUsersLoginSuccessResponse"
 401:
 description: Authentication failed or second factor required
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/PostUsers2FALoginErrorResponse"

 /:
 get:
 tags: \[discovery\]
 summary: Get namespaces and repos
 description: Gets a list of your namespaces and repos which have data available.
 operationId: getNamespaces
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/NamespaceData'
 /namespaces:
 get:
 tags: \[discovery\]
 summary: Get user's namespaces
 description: Get metadata associated with the namespaces the user has access to, including extra repos associated with the namespaces.
 operationId: getUserNamespaces
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 type: array
 items:
 $ref: '#/components/schemas/NamespaceMetadata'
 '401':
 description: Authentication failed or second factor required
 /namespaces/{namespace}:
 get:
 tags: \[discovery\]
 summary: Get namespace
 description: Gets metadata associated with specified namespace, including extra repos associated with the namespace.
 operationId: getNamespace
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/NamespaceMetadata'
 /namespaces/{namespace}/pulls:
 get:
 tags: \[namespaces\]
 summary: Get pull data
 description: Gets pulls for the given namespace.
 operationId: getNamespacePulls
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 \- in: query
 name: timespan
 schema:
 $ref: '#/components/schemas/TimespanType'
 required: false
 description: Timespan type for fetching data
 \- in: query
 name: period
 schema:
 $ref: '#/components/schemas/PeriodType'
 required: false
 description: Relative period of the period to fetch data
 \- in: query
 name: group
 schema:
 $ref: '#/components/schemas/GroupType'
 required: false
 description: Field to group the data by
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/PullData'
 '404':
 description: Not found - namespace doesn't exist or user does not have permission to access it
 /namespaces/{namespace}/repos/{repo}/pulls:
 get:
 tags: \[namespaces\]
 summary: Get pull data
 description: Gets pulls for the given repo.
 operationId: getRepoPulls
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 \- in: path
 name: repo
 schema:
 type: string
 required: true
 description: Repository to fetch data for
 \- in: query
 name: timespan
 schema:
 $ref: '#/components/schemas/TimespanType'
 required: false
 description: Timespan type for fetching data
 \- in: query
 name: period
 schema:
 $ref: '#/components/schemas/PeriodType'
 required: false
 description: Relative period of the period to fetch data
 \- in: query
 name: group
 schema:
 $ref: '#/components/schemas/GroupType'
 required: false
 description: Field to group the data by
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/PullData'
 '404':
 description: Not found - repo doesn't exist or user does not have permission to access it
 /namespaces/{namespace}/pulls/exports/years:
 get:
 tags: \[namespaces\]
 summary: Get years with data
 description: Gets a list of years that have data for the given namespace.
 operationId: getNamespaceYears
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/YearData'
 /namespaces/{namespace}/pulls/exports/years/{year}/{timespantype}:
 get:
 tags: \[namespaces\]
 summary: Get timespans with data
 description: Gets a list of timespans of the given type that have data for the given namespace and year.
 operationId: getNamespaceTimespans
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 \- in: path
 name: year
 schema:
 type: integer
 required: true
 description: Year to fetch data for
 \- in: path
 name: timespantype
 schema:
 $ref: '#/components/schemas/TimespanType'
 required: true
 description: Type of timespan to fetch data for
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/TimespanData'
 /namespaces/{namespace}/pulls/exports/years/{year}/{timespantype}/{timespan}:
 get:
 tags: \[namespaces\]
 summary: Get namespace metadata for timespan
 description: Gets info about data for the given namespace and timespan.
 operationId: getNamespaceTimespanMetadata
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 \- in: path
 name: year
 schema:
 type: integer
 required: true
 description: Year to fetch data for
 \- in: path
 name: timespantype
 schema:
 $ref: '#/components/schemas/TimespanType'
 required: true
 description: Type of timespan to fetch data for
 \- in: path
 name: timespan
 schema:
 type: integer
 required: true
 description: Timespan to fetch data for
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/TimespanModel'
 '404':
 description: Not Found
 /namespaces/{namespace}/pulls/exports/years/{year}/{timespantype}/{timespan}/{dataview}:
 get:
 tags: \[namespaces\]
 summary: Get namespace data for timespan
 description: Gets a list of URLs that can be used to download the pull data for the given namespace and timespan.
 operationId: getNamespaceDataByTimespan
 parameters:
 \- in: path
 name: namespace
 schema:
 type: string
 required: true
 description: Namespace to fetch data for
 \- in: path
 name: year
 schema:
 type: integer
 required: true
 description: Year to fetch data for
 \- in: path
 name: timespantype
 schema:
 $ref: '#/components/schemas/TimespanType'
 required: true
 description: Type of timespan to fetch data for
 \- in: path
 name: timespan
 schema:
 type: integer
 required: true
 description: Timespan to fetch data for
 \- in: path
 name: dataview
 schema:
 $ref: '#/components/schemas/DataviewType'
 required: true
 description: Type of data to fetch
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/ResponseData'
 /repos/pulls:
 get:
 tags: \[namespaces\]
 summary: Get pull data for multiple repos
 description: Gets pull for the given repos.
 operationId: getManyReposPulls
 parameters:
 \- in: query
 name: repos
 schema:
 type: array
 items:
 type: string
 required: true
 description: Repositories to fetch data for (maximum of 50 repositories per request).
 \- in: query
 name: timespan
 schema:
 $ref: '#/components/schemas/TimespanType'
 required: false
 description: Timespan type for fetching data
 \- in: query
 name: period
 schema:
 $ref: '#/components/schemas/PeriodType'
 required: false
 description: Relative period of the period to fetch data
 \- in: query
 name: group
 schema:
 $ref: '#/components/schemas/GroupType'
 required: false
 description: Field to group the data by
 responses:
 '200':
 description: Success
 content:
 application/json:
 schema:
 $ref: '#/components/schemas/ReposPullData'

components:
 schemas:
 UsersLoginRequest:
 description: User login details
 type: object
 required:
 \- username
 \- password
 properties:
 username:
 description: The username of the Docker Hub account to authenticate with.
 type: string
 example: myusername
 password:
 description:
 The password or personal access token (PAT) of the Docker Hub
 account to authenticate with.
 type: string
 example: hunter2
 PostUsersLoginSuccessResponse:
 description: successful user login response
 type: object
 properties:
 token:
 description: \|
 Created authentication token.

 This token can be used in the HTTP Authorization header as a JWT to authenticate with the Docker Hub APIs.
 type: string
 example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c
 nullable: false
 PostUsersLoginErrorResponse:
 description: failed user login response or second factor required
 type: object
 required:
 \- detail
 properties:
 detail:
 description: Description of the error.
 type: string
 example: Incorrect authentication credentials
 nullable: false
 login\_2fa\_token:
 description:
 Short-lived token to be used on \`/v2/users/2fa-login\` to
 complete the authentication. This field is present only if 2FA is
 enabled.
 type: string
 example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c
 nullable: true
 Users2FALoginRequest:
 description: Second factor user login details
 type: object
 required:
 \- login\_2fa\_token
 \- code
 properties:
 login\_2fa\_token:
 description: The intermediate 2FA token returned from \`/v2/users/login\` API.
 type: string
 example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c
 code:
 description:
 The Time-based One-Time Password of the Docker Hub account to
 authenticate with.
 type: string
 example: 123456
 PostUsers2FALoginErrorResponse:
 description: failed second factor login response.
 type: object
 properties:
 detail:
 description: Description of the error.
 type: string
 example: Incorrect authentication credentials
 nullable: false

 ResponseData:
 properties:
 data:
 type: array
 description: \|
 List of urls to download the data. When the data is large, the data will be split into multiple files.
 items:
 $ref: '#/components/schemas/ResponseDataFile'
 ResponseDataFile:
 properties:
 url:
 type: string
 size:
 type: integer
 format: int64
 NamespaceData:
 properties:
 namespaces:
 type: array
 items:
 type: string
 NamespaceMetadata:
 properties:
 namespace:
 type: string
 extraRepos:
 type: array
 items:
 type: string
 datasets:
 type: array
 items:
 $ref: '#/components/schemas/DatasetModel'
 DatasetModel:
 properties:
 name:
 $ref: '#/components/schemas/DatasetType'
 views:
 type: array
 items:
 $ref: '#/components/schemas/DataviewType'
 timespans:
 type: array
 items:
 $ref: '#/components/schemas/TimespanType'
 PullData:
 properties:
 pulls:
 type: array
 items:
 $ref: '#/components/schemas/PullModel'
 ReposPullData:
 properties:
 repos:
 type: object
 additionalProperties:
 $ref: '#/components/schemas/PullData'
 PullModel:
 properties:
 start:
 type: string
 end:
 type: string
 repo:
 type: string
 namespace:
 type: string
 pullCount:
 type: integer
 ipCount:
 type: integer
 country:
 type: string

 YearData:
 properties:
 years:
 type: array
 items:
 $ref: '#/components/schemas/YearModel'
 YearModel:
 properties:
 year:
 type: integer
 MonthData:
 properties:
 months:
 type: array
 items:
 $ref: '#/components/schemas/MonthModel'
 MonthModel:
 properties:
 month:
 type: integer
 WeekData:
 properties:
 weeks:
 type: array
 items:
 $ref: '#/components/schemas/WeekModel'
 WeekModel:
 properties:
 week:
 type: integer
 TimespanType:
 type: string
 enum: \[months,weeks\]
 PeriodType:
 type: string
 enum: \[last-2-months,last-3-months,last-6-months,last-12-months\]
 DataviewType:
 type: string
 enum: \[raw,summary,repo-summary,namespace-summary\]
 DatasetType:
 type: string
 enum: \[pulls\]
 TimespanModel:
 oneOf:
 \- $ref: '#/components/schemas/MonthModel'
 \- $ref: '#/components/schemas/WeekModel'
 TimespanData:
 oneOf:
 \- $ref: '#/components/schemas/MonthData'
 \- $ref: '#/components/schemas/WeekData'
 GroupType:
 type: string
 enum: \[repo,namespace\]
 securitySchemes:
 HubAuth:
 type: https
 scheme: bearer
 bearerFormat: JWT
 description: \|
 JWT Bearer Authentication is required to access the Docker DVP Data API.

 This authentication documentation is duplicated from the \[Hub API Authentication docs\](https://docs.docker.com/reference/api/hub/#tag/authentication)
 x-displayName: Docker Hub Authentication

----
url: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/
----

# What is an image?

***

Table of contents

***

## [Explanation](#explanation)

Seeing as a [container](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) is an isolated process, where does it get its files and configuration? How do you share those environments?

That's where container images come in. A container image is a standardized package that includes all of the files, binaries, libraries, and configurations to run a container.

For a [PostgreSQL](https://hub.docker.com/_/postgres) image, that image will package the database binaries, config files, and other dependencies. For a Python web app, it'll include the Python runtime, your app code, and all of its dependencies.

There are two important principles of images:

1. Images are immutable. Once an image is created, it can't be modified. You can only make a new image or add changes on top of it.

2. Container images are composed of layers. Each layer represents a set of file system changes that add, remove, or modify files.

These two principles let you to extend or add to existing images. For example, if you are building a Python app, you can start from the [Python image](https://hub.docker.com/_/python) and add additional layers to install your app's dependencies and add your code. This lets you focus on your app, rather than Python itself.

### [Finding images](#finding-images)

[Docker Hub](https://hub.docker.com) is the default global marketplace for storing and distributing images. It has over 100,000 images created by developers that you can run locally. You can search for Docker Hub images and run them directly from Docker Desktop.

Docker Hub provides a variety of Docker-supported and endorsed images known as Docker Trusted Content. These provide fully managed services or great starters for your own images. These include:

* [Docker Official Images](https://hub.docker.com/search?badges=official) - a curated set of Docker repositories, serve as the starting point for the majority of users, and are some of the most secure on Docker Hub
* [Docker Hardened Images](https://hub.docker.com/hardened-images/catalog) - minimal, secure, production-ready images with near-zero CVEs, designed to reduce attack surface and simplify compliance. Free and open source under Apache 2.0
* [Docker Verified Publishers](https://hub.docker.com/search?badges=verified_publisher) - high-quality images from commercial publishers verified by Docker
* [Docker-Sponsored Open Source](https://hub.docker.com/search?badges=open_source) - images published and maintained by open-source projects sponsored by Docker through Docker's open source program

For example, [Redis](https://hub.docker.com/_/redis) and [Memcached](https://hub.docker.com/_/memcached) are a few popular ready-to-go Docker Official Images. You can download these images and have these services up and running in a matter of seconds. There are also base images, like the [Node.js](https://hub.docker.com/_/node) Docker image, that you can use as a starting point and add your own files and configurations. For production workloads requiring enhanced security, Docker Hardened Images offer minimal variants of popular images like Node.js, Python, and Go.

## [Try it out](#try-it-out)

In this hands-on, you will learn how to search and pull a container image using the Docker Desktop GUI.

### [Search for and download an image](#search-for-and-download-an-image)

1. Open the Docker Desktop Dashboard and select the **Images** view in the left-hand navigation menu.

2. Select the **Search images to run** button. If you don't see it, select the *global search bar* at the top of the screen.

3. In the **Search** field, enter "welcome-to-docker". Once the search has completed, select the `docker/welcome-to-docker` image.

4. Select **Pull** to download the image.

### [Learn about the image](#learn-about-the-image)

Once you have an image downloaded, you can learn quite a few details about the image either through the GUI or the CLI.

1. In the Docker Desktop Dashboard, select the **Images** view.

2. Select the **docker/welcome-to-docker** image to open details about the image.

3. The image details page presents you with information regarding the layers of the image, the packages and libraries installed in the image, and any discovered vulnerabilities.

Follow the instructions to search and pull a Docker image using CLI to view its layers.

### [Search for and download an image](#search-for-and-download-an-image)

1. Open a terminal and search for images using the [`docker search`](/reference/cli/docker/search/) command:

   ```console
   docker search docker/welcome-to-docker
   ```

   You will see output like the following:

   ```console
   NAME                       DESCRIPTION                                     STARS     OFFICIAL
   docker/welcome-to-docker   Docker image for new users getting started w…   20
   ```

   This output shows you information about relevant images available on Docker Hub.

2. Pull the image using the [`docker pull`](/reference/cli/docker/image/pull/) command.

   ```console
   docker pull docker/welcome-to-docker
   ```

   You will see output like the following:

   ```console
   Using default tag: latest
   latest: Pulling from docker/welcome-to-docker
   579b34f0a95b: Download complete
   d11a451e6399: Download complete
   1c2214f9937c: Download complete
   b42a2f288f4d: Download complete
   54b19e12c655: Download complete
   1fb28e078240: Download complete
   94be7e780731: Download complete
   89578ce72c35: Download complete
   Digest: sha256:eedaff45e3c78538087bdd9dc7afafac7e110061bbdd836af4104b10f10ab693
   Status: Downloaded newer image for docker/welcome-to-docker:latest
   docker.io/docker/welcome-to-docker:latest
   ```

   Each of line represents a different downloaded layer of the image. Remember that each layer is a set of filesystem changes and provides functionality of the image.

### [Learn about the image](#learn-about-the-image)

1. List your downloaded images using the [`docker image ls`](/reference/cli/docker/image/ls/) command:

   ```console
   docker image ls
   ```

   You will see output like the following:

   ```console
   REPOSITORY                 TAG       IMAGE ID       CREATED        SIZE
   docker/welcome-to-docker   latest    eedaff45e3c7   4 months ago   29.7MB
   ```

   The command shows a list of Docker images currently available on your system. The `docker/welcome-to-docker` has a total size of approximately 29.7MB.

   > **Image size**
   >
   > The image size represented here reflects the uncompressed size of the image, not the download size of the layers.

2. List the image's layers using the [`docker image history`](/reference/cli/docker/image/history/) command:

   ```console
   docker image history docker/welcome-to-docker
   ```

   You will see output like the following:

   ```console
   IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
   648f93a1ba7d   4 months ago   COPY /app/build /usr/share/nginx/html # buil…   1.6MB     buildkit.dockerfile.v0
   <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["nginx" "-g" "daemon…   0B
   <missing>      5 months ago   /bin/sh -c #(nop)  STOPSIGNAL SIGQUIT           0B
   <missing>      5 months ago   /bin/sh -c #(nop)  EXPOSE 80                    0B
   <missing>      5 months ago   /bin/sh -c #(nop)  ENTRYPOINT ["/docker-entr…   0B
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:9e3b2b63db9f8fc7…   4.62kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:57846632accc8975…   3.02kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:3b1b9915b7dd898a…   298B
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:caec368f5a54f70a…   2.12kB
   <missing>      5 months ago   /bin/sh -c #(nop) COPY file:01e75c6dd0ce317d…   1.62kB
   <missing>      5 months ago   /bin/sh -c set -x     && addgroup -g 101 -S …   9.7MB
   <missing>      5 months ago   /bin/sh -c #(nop)  ENV PKG_RELEASE=1            0B
   <missing>      5 months ago   /bin/sh -c #(nop)  ENV NGINX_VERSION=1.25.3     0B
   <missing>      5 months ago   /bin/sh -c #(nop)  LABEL maintainer=NGINX Do…   0B
   <missing>      5 months ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      5 months ago   /bin/sh -c #(nop) ADD file:ff3112828967e8004…   7.66MB
   ```

   This output shows you all of the layers, their sizes, and the command used to create the layer.

   > **Viewing the full command**
   >
   > If you add the `--no-trunc` flag to the command, you will see the full command. Note that, since the output is in a table-like format, longer commands will cause the output to be very difficult to navigate.

In this walkthrough, you searched and pulled a Docker image. In addition to pulling a Docker image, you also learned about the layers of a Docker Image.

## [Additional resources](#additional-resources)

The following resources will help you learn more about exploring, finding, and building images:

* [Docker trusted content](https://docs.docker.com/docker-hub/image-library/trusted-content/)
* [Explore the Image view in Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/)
* [Docker Build overview](https://docs.docker.com/build/concepts/overview/)
* [Docker Hub](https://hub.docker.com)

## [Next steps](#next-steps)

Now that you have learned the basics of images, it's time to learn about distributing images through registries.

[What is a registry?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/)

----
url: https://docs.docker.com/engine/security/trust/trust_automation/
----

# Automation with content trust

***

Table of contents

***

It is very common for Docker Content Trust to be built into existing automation systems. To allow tools to wrap Docker and push trusted content, there are environment variables that can be passed through to the client.

This guide follows the steps as described in [Signing images with Docker Content Trust](https://docs.docker.com/engine/security/trust/#signing-images-with-docker-content-trust). Make sure you understand and follow the prerequisites.

When working directly with the Notary client, it uses its [own set of environment variables](https://github.com/theupdateframework/notary/blob/master/docs/reference/client-config.md#environment-variables-optional).

## [Add a delegation private key](#add-a-delegation-private-key)

To automate importing a delegation private key to the local Docker trust store, we need to pass a passphrase for the new key. This passphrase will be required every time that delegation signs a tag.

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust key load delegation.key --name jeff
Loading key from "delegation.key"...
Successfully imported key from delegation.key
```

## [Add a delegation public key](#add-a-delegation-public-key)

If you initialize a repository at the same time as adding a delegation public key, then you will need to use the local Notary Canonical Root Key's passphrase to create the repositories trust data. If the repository has already been initiated then you only need the repositories passphrase.

```console
# Export the Local Root Key Passphrase if required.
$ export DOCKER_CONTENT_TRUST_ROOT_PASSPHRASE="rootpassphrase123"

# Export the Repository Passphrase
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="repopassphrase123"

# Initialize Repo and Push Delegation
$ docker trust signer add --key delegation.crt jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Initializing signed repository for registry.example.com/admin/demo...
Successfully initialized "registry.example.com/admin/demo"
Successfully added signer: registry.example.com/admin/demo
```

## [Sign an image](#sign-an-image)

Finally when signing an image, we will need to export the passphrase of the signing key. This was created when the key was loaded into the local Docker trust store with `$ docker trust key load`.

```console
$ export DOCKER_CONTENT_TRUST_REPOSITORY_PASSPHRASE="mypassphrase123"

$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
428c97da766c: Layer already exists
2: digest: sha256:1a6fd470b9ce10849be79e99529a88371dff60c60aab424c077007f6979b4812 size: 524
Signing and pushing trust metadata
Successfully signed registry.example.com/admin/demo:1
```

## [Build with content trust](#build-with-content-trust)

You can also build with content trust. Before running the `docker build` command, you should set the environment variable `DOCKER_CONTENT_TRUST` either manually or in a scripted fashion. Consider the simple Dockerfile below.

```dockerfile
# syntax=docker/dockerfile:1
FROM docker/trusttest:latest
RUN echo
```

The `FROM` tag is pulling a signed image. You cannot build an image that has a `FROM` that is not either present locally or signed. Given that content trust data exists for the tag `latest`, the following build should succeed:

```console
$  docker build -t docker/trusttest:testing .
Using default tag: latest
latest: Pulling from docker/trusttest

b3dbab3810fc: Pull complete
a9539b34a6ab: Pull complete
Digest: sha256:d149ab53f871
```

If content trust is enabled, building from a Dockerfile that relies on tag without trust data, causes the build command to fail:

```console
$  docker build -t docker/trusttest:testing .
unable to process Dockerfile: No trust data for notrust
```

## [Related information](#related-information)

* [Delegations for content trust](https://docs.docker.com/engine/security/trust/trust_delegation/)
* [Content trust in Docker](https://docs.docker.com/engine/security/trust/)
* [Manage keys for content trust](https://docs.docker.com/engine/security/trust/trust_key_mng/)
* [Play in a content trust sandbox](https://docs.docker.com/engine/security/trust/trust_sandbox/)

----
url: https://docs.docker.com/reference/compose-file/version-and-name/
----

# Version and name top-level elements

***

Table of contents

***

## [Version top-level element (obsolete)](#version-top-level-element-obsolete)

> Important
>
> The top-level `version` property is defined by the Compose Specification for backward compatibility. It is only informative and you'll receive a warning message that it is obsolete if used.

Compose always uses the most recent schema to validate the Compose file, regardless of the `version` field.

Compose validates whether it can fully parse the Compose file. If some fields are unknown, typically because the Compose file was written with fields defined by a newer version of the Specification, you'll receive a warning message.

## [Name top-level element](#name-top-level-element)

The top-level `name` property is defined by the Compose Specification as the project name to be used if you don't set one explicitly.

Compose offers a way for you to override this name, and sets a default project name to be used if the top-level `name` element is not set.

Whenever a project name is defined by top-level `name` or by some custom mechanism, it is exposed for [interpolation](https://docs.docker.com/reference/compose-file/interpolation/) and environment variable resolution as `COMPOSE_PROJECT_NAME`

```yml
name: myapp

services:
  foo:
    image: busybox
    command: echo "I'm running ${COMPOSE_PROJECT_NAME}"
```

For more information on other ways to name Compose projects, see [Specify a project name](https://docs.docker.com/compose/how-tos/project-name/).

----
url: https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/write-tests/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Write tests with Testcontainers

***

Table of contents

***

The existing tests use an in-memory SQLite database. While convenient, this doesn't match production behavior. You can replace it with a real Microsoft SQL Server instance managed by Testcontainers.

## [Add dependencies](#add-dependencies)

Change to the test project directory and add the SQL Server Entity Framework provider and the Testcontainers MSSQL module:

```console
$ cd tests/RazorPagesProject.Tests
$ dotnet add package Microsoft.EntityFrameworkCore.SqlServer --version 7.0.0
$ dotnet add package Testcontainers.MsSql --version 3.0.0
```

> Note
>
> Testcontainers for .NET offers a range of [modules](https://www.nuget.org/profiles/Testcontainers) that follow best practice configurations.

## [Create the test class](#create-the-test-class)

Create a `MsSqlTests.cs` file in the `IntegrationTests` directory. This class manages the SQL Server container lifecycle and contains a nested test class.

```csharp
using System.Data.Common;
using System.Net;
using AngleSharp.Html.Dom;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using RazorPagesProject.Data;
using RazorPagesProject.Tests.Helpers;
using Testcontainers.MsSql;
using Xunit;

namespace RazorPagesProject.Tests.IntegrationTests;

public sealed class MsSqlTests : IAsyncLifetime
{
    private readonly MsSqlContainer _msSqlContainer = new MsSqlBuilder().Build();

    public Task InitializeAsync()
    {
        return _msSqlContainer.StartAsync();
    }

    public Task DisposeAsync()
    {
        return _msSqlContainer.DisposeAsync().AsTask();
    }

    public sealed class IndexPageTests : IClassFixture<MsSqlTests>, IDisposable
    {
        private readonly WebApplicationFactory<Program> _webApplicationFactory;

        private readonly HttpClient _httpClient;

        public IndexPageTests(MsSqlTests fixture)
        {
            var clientOptions = new WebApplicationFactoryClientOptions();
            clientOptions.AllowAutoRedirect = false;

            _webApplicationFactory = new CustomWebApplicationFactory(fixture);
            _httpClient = _webApplicationFactory.CreateClient(clientOptions);
        }

        public void Dispose()
        {
            _webApplicationFactory.Dispose();
        }

        [Fact]
        public async Task Post_DeleteAllMessagesHandler_ReturnsRedirectToRoot()
        {
            // Arrange
            var defaultPage = await _httpClient.GetAsync("/")
                .ConfigureAwait(false);

            var document = await HtmlHelpers.GetDocumentAsync(defaultPage)
                .ConfigureAwait(false);

            // Act
            var form = (IHtmlFormElement)document.QuerySelector("form[id='messages']");
            var submitButton = (IHtmlButtonElement)document.QuerySelector("button[id='deleteAllBtn']");

            var response = await _httpClient.SendAsync(form, submitButton)
                .ConfigureAwait(false);

            // Assert
            Assert.Equal(HttpStatusCode.OK, defaultPage.StatusCode);
            Assert.Equal(HttpStatusCode.Redirect, response.StatusCode);
            Assert.Equal("/", response.Headers.Location.OriginalString);
        }

        private sealed class CustomWebApplicationFactory : WebApplicationFactory<Program>
        {
            private readonly string _connectionString;

            public CustomWebApplicationFactory(MsSqlTests fixture)
            {
                _connectionString = fixture._msSqlContainer.GetConnectionString();
            }

            protected override void ConfigureWebHost(IWebHostBuilder builder)
            {
                builder.ConfigureServices(services =>
                {
                    services.Remove(services.SingleOrDefault(service => typeof(DbContextOptions<ApplicationDbContext>) == service.ServiceType));
                    services.Remove(services.SingleOrDefault(service => typeof(DbConnection) == service.ServiceType));
                    services.AddDbContext<ApplicationDbContext>((_, option) => option.UseSqlServer(_connectionString));
                });
            }
        }
    }
}
```

## [Understand the test structure](#understand-the-test-structure)

### [Container lifecycle with IAsyncLifetime](#container-lifecycle-with-iasynclifetime)

The outer `MsSqlTests` class implements `IAsyncLifetime`. xUnit calls `InitializeAsync()` right after creating the class instance, which starts the SQL Server container. After all tests complete, `DisposeAsync()` stops and removes the container.

```csharp
private readonly MsSqlContainer _msSqlContainer = new MsSqlBuilder().Build();
```

`MsSqlBuilder().Build()` creates a pre-configured Microsoft SQL Server container. Testcontainers modules follow best practices, so you don't need to configure ports, passwords, or startup wait strategies yourself.

### [Nested test class with IClassFixture](#nested-test-class-with-iclassfixture)

The `IndexPageTests` class is nested inside `MsSqlTests` and implements `IClassFixture<MsSqlTests>`. This gives the test class access to the container's private field and creates a clean hierarchy in the test explorer.

### [Custom WebApplicationFactory](#custom-webapplicationfactory)

Instead of using the SQLite-based factory, the nested `CustomWebApplicationFactory` retrieves the connection string from the running SQL Server container and passes it to `UseSqlServer()`:

```csharp
private sealed class CustomWebApplicationFactory : WebApplicationFactory<Program>
{
    private readonly string _connectionString;

    public CustomWebApplicationFactory(MsSqlTests fixture)
    {
        _connectionString = fixture._msSqlContainer.GetConnectionString();
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            services.Remove(services.SingleOrDefault(service => typeof(DbContextOptions<ApplicationDbContext>) == service.ServiceType));
            services.Remove(services.SingleOrDefault(service => typeof(DbConnection) == service.ServiceType));
            services.AddDbContext<ApplicationDbContext>((_, option) => option.UseSqlServer(_connectionString));
        });
    }
}
```

This factory:

1. Removes the existing `DbContextOptions<ApplicationDbContext>` registration
2. Removes the existing `DbConnection` registration
3. Adds a new `ApplicationDbContext` configured with the SQL Server connection string from the Testcontainers-managed container

> Note
>
> The Microsoft SQL Server Docker image isn't compatible with ARM devices, such as Macs with Apple Silicon. You can use the [SqlEdge](https://www.nuget.org/packages/Testcontainers.SqlEdge) module or [Testcontainers Cloud](https://www.testcontainers.cloud/) as alternatives.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/run-tests/)

----
url: https://docs.docker.com/dhi/how-to/hardened-packages/
----

# Use Hardened System Packages

***

Table of contents

***

Docker Hardened System Packages are built from source by Docker. This ensures supply chain integrity throughout your entire image stack by eliminating risks from potentially compromised public packages.

Access to hardened packages varies by subscription:

* **DHI Community**: Includes hardened packages in base images. Can configure the public package repository to access the same packages in custom images.
* **DHI Select**: Includes all Community packages, plus access to additional compliance-specific packages (such as FIPS variants) and Docker-patched packages through the image customization UI.
* **DHI Enterprise**: Includes all Select packages, plus the ability to configure the enterprise package repository directly in your own images for full access to compliance and security-patched packages.

## [Built-in packages](#built-in-packages)

Supported distributions of Docker Hardened Images (DHI) automatically include hardened system packages. No additional configuration is required. Simply pull and use the images as normal.

All packages in these images are built by Docker from source, maintaining the same security standards as the base images themselves.

## [Add hardened packages to your images](#add-hardened-packages-to-your-images)

You can add hardened packages to your own images in the following two ways.

### [Add packages through image customization](#add-packages-through-image-customization)

Subscription: Docker Hardened Images Select or Enterprise

When customizing Docker Hardened Images with DHI Select or DHI Enterprise, you can add hardened packages for Alpine-based images through the customization interface. Follow the steps to [create an image customization](https://docs.docker.com/dhi/how-to/customize/#create-an-image-customization) and select hardened packages during the customization process.

### [Configure the package manager](#configure-the-package-manager)

You can configure your package manager to pull from Docker's hardened package repositories. This lets you install hardened packages in your own images.

#### [Public repository](#public-repository)

To use Docker's public hardened package repository in your own images, configure your package manager in your Dockerfile to install the DHI signing key and add the DHI repository.

The configuration process involves three steps:

1. Install the [signing key](https://github.com/docker-hardened-images/keyring)
2. Configure the package repository
3. Update and install packages

The following example shows how to configure the Alpine package manager in your Dockerfile to use Docker's public hardened package repository:

```dockerfile
FROM alpine:3.23

# Install the signing key
RUN cd /etc/apk/keys && \
    wget https://dhi.io/keyring/dhi-apk@docker-0F81AD7700D99184.rsa.pub

# Replace the default repositories with the hardened package repository
RUN echo "https://dhi.io/apk/alpine/v3.23/main" > /etc/apk/repositories

# Update and install packages
RUN apk update && \
    apk add libpng
```

Replace `3.23` with your Alpine version in both the base image tag and repository URL. Supported versions include Alpine 3.23 and 3.24.

To verify the configuration, build and run the image:

```console
$ docker build -t myapp:latest .
$ docker run -it myapp:latest sh
```

Inside the container, check the configured repositories:

```console
/ # cat /etc/apk/repositories
https://dhi.io/apk/alpine/v3.23/main
```

This ensures all packages are installed from Docker's hardened repository.

The following example shows how to configure the Debian package manager in your Dockerfile to use Docker's public hardened package repository:

```dockerfile
FROM debian:trixie-slim

# Install the signing key
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://dhi.io/keyring/dhi-deb-gpg.D46852F6925E9F71.key \
    | gpg --dearmor -o /usr/share/keyrings/dhi-deb.gpg

# Add the hardened package repository
RUN echo "deb [signed-by=/usr/share/keyrings/dhi-deb.gpg] https://dhi.io/deb/debian/main trixie main" \
    > /etc/apt/sources.list.d/dhi.list

# Update and install packages
RUN apt-get update && apt-get install -y jq \
    && rm -rf /var/lib/apt/lists/*
```

To verify the configuration, build and run the image:

```console
$ docker build -t myapp:latest .
$ docker run -it myapp:latest bash
```

Inside the container, check the configured repository:

```console
root@myapp:/# cat /etc/apt/sources.list.d/dhi.list
deb [signed-by=/usr/share/keyrings/dhi-deb.gpg] https://dhi.io/deb/debian/main trixie main
```

When the DHI repository carries a hardened version of a package, `apt` prefers it over the upstream Debian version automatically. You can confirm this with `apt-cache policy <package>`, which shows a candidate with a `+dhi` or `dhi` version suffix sourced from `https://dhi.io/deb/debian/main`.

Not every Debian package is available as a hardened system package. When a package is not in the DHI repository, `apt` transparently falls back to the upstream Debian mirrors configured in the base image.

All packages installed from the Docker Hardened Images repository are built from source by Docker and include full provenance.

#### [Enterprise repository](#enterprise-repository)

Subscription: Docker Hardened Images Enterprise

With DHI Enterprise, you have access to an additional package repository that includes hardened packages for compliance variants such as FIPS, as well as additional security patches.

The configuration process involves five steps:

1. Install the [signing keys](https://github.com/docker-hardened-images/keyring)
2. Configure the base package repository
3. Add the enterprise security repository
4. Configure package installation with authentication
5. Build the image passing credentials as a secret using the DHI CLI

The following example shows how to configure the Alpine package manager in your Dockerfile to use Docker's enterprise hardened package repository:

```dockerfile
FROM alpine:3.23

# Install the signing key
RUN cd /etc/apk/keys && \
    wget https://dhi.io/keyring/dhi-apk@docker-0F81AD7700D99184.rsa.pub

# Replace the default repositories with the hardened package repository
RUN echo "https://dhi.io/apk/alpine/v3.23/main" > /etc/apk/repositories

# Update and install the enterprise configuration package to add the security repository
RUN apk update && \
    apk add dhi-enterprise-conf

# Install packages from the security repository with authentication
RUN --mount=type=secret,id=http_auth \
    HTTP_AUTH="$(cat /run/secrets/http_auth)" \
    apk update && \
    apk add openssl-fips
```

Build the image with authentication passed securely as a build secret:

```console
$ docker dhi auth apk > http_auth.txt
$ docker build --secret id=http_auth,src=http_auth.txt -t myapp-enterprise:latest .
$ rm http_auth.txt
```

The `--secret` flag securely mounts the authentication credentials during build without storing them in the image layers or metadata.

The following example shows how to configure the Debian package manager in your Dockerfile to use Docker's enterprise hardened package repository. Mount credentials at `/etc/apt/auth.conf.d/dhi.conf`; `apt` reads files in `/etc/apt/auth.conf.d/` automatically when they have mode `0600`:

```dockerfile
FROM debian:trixie-slim

# Install the signing keys
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://dhi.io/keyring/dhi-deb-gpg.D46852F6925E9F71.key \
    | gpg --dearmor -o /usr/share/keyrings/dhi-deb.gpg
RUN curl -fsSL https://dhi.io/keyring/dhi-deb-sec-gpg.D46852F6925E9F71.key \
    | gpg --dearmor -o /usr/share/keyrings/dhi-deb-sec.gpg

# Add the hardened package repository and the enterprise security repository
RUN echo "deb [signed-by=/usr/share/keyrings/dhi-deb.gpg] https://dhi.io/deb/debian/main trixie main" \
    > /etc/apt/sources.list.d/dhi.list
RUN echo "deb [signed-by=/usr/share/keyrings/dhi-deb-sec.gpg] https://dhi.io/deb/debian/security trixie main" \
    > /etc/apt/sources.list.d/dhi-sec.list

# Install packages from the security repository with authentication
RUN --mount=type=secret,id=netrc,target=/etc/apt/auth.conf.d/dhi.conf,mode=0600 \
    apt-get update && apt-get install -y openssl \
    && rm -rf /var/lib/apt/lists/*
```

Build the image, passing credentials securely as a build secret through an environment variable:

```console
$ NETRC=$(docker dhi auth deb) docker build \
    --secret id=netrc,env=NETRC \
    -t myapp-enterprise:latest .
```

The `--secret id=netrc,env=NETRC` form securely mounts the authentication credentials during build without storing them in the image layers or metadata.

## [Verify packages](#verify-packages)

Every hardened package is cryptographically signed and includes metadata that proves its provenance and build integrity. You can verify the signatures and view the metadata to ensure your packages come from Docker's trusted build infrastructure.

### [View package metadata](#view-package-metadata)

To view information about a hardened package:

```console
$ apk info -L <package-name>
```

```console
$ dpkg -L <package-name>
```

This shows the files included in the package and its metadata.

### [Verify package signatures](#verify-package-signatures)

Hardened packages are cryptographically signed by Docker. When you install the signing keys and configure your package manager as described previously, the package manager automatically verifies signatures during installation.

If a package fails signature verification, the package manager will refuse to install it, protecting you from tampered or compromised packages.

### [Build provenance and cryptographic verification](#build-provenance-and-cryptographic-verification)

Docker hardened packages are built by Docker's trusted infrastructure and include verifiable metadata and cryptographic signatures.

To view this metadata for an installed package:

```console
$ apk info -a <package-name>
```

```console
$ apt-cache show <package-name>
```

Or to view metadata for a package before installing:

```console
$ apk fetch --stdout <package-name> | tar -xzO .PKGINFO
```

```console
$ apt-get download <package-name>
$ dpkg-deb -I <package-name>_*.deb
```

The package signing keys ensure that packages haven't been tampered with after being built. When you install the signing key and configure your package manager, all packages are automatically verified before installation.

### [Package attestations](#package-attestations)

Each hardened package includes its own attestations, similar to [image attestations](https://docs.docker.com/dhi/how-to/verify/). These attestations provide provenance and build information for individual packages, allowing you to trace the supply chain down to the package level.

You can retrieve package attestations by first extracting package information from the image's SLSA provenance, then using the package digest to access its attestations.

#### [Extract package information from image attestations](#extract-package-information-from-image-attestations)

To get provenance information for a specific package from an image's SLSA provenance attestation, you first need to retrieve the image's provenance and then filter for the specific package you're interested in.

The SLSA provenance attestation includes a `materials` array that lists all build inputs, including packages. You can use `jq` to filter this array for a specific package:

```console
$ docker scout attest get dhi.io/golang:1.26-alpine3.23 \
    --predicate-type https://slsa.dev/provenance/v0.2 | \
    jq '.predicate.materials[] | select( .uri == "https://dhi.io/apk/alpine/v3.23/main/aarch64/golang-1.26-1.26.0-r0.apk" )'
```

Replace the package URI in the `select()` filter with the specific package you're looking for. You can find available packages by first running the command without the `select()` filter to see all materials.

This returns the package URI and its SHA-256 digest:

```json
{
  "uri": "https://dhi.io/apk/alpine/v3.23/main/aarch64/golang-1.26-1.26.0-r0.apk",
  "digest": {
    "sha256": "4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838"
  }
}
```

#### [List attestations for a package](#list-attestations-for-a-package)

Using the package digest from the previous section, you can list all available attestations for that package:

```console
$ curl -s https://dhi.io/apk/alpine/v3.23/main/sha256:4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838/attestations/list | jq .
```

This returns information about the package and its available attestations:

```json
{
  "subject": {
    "name": "pkg:apk/alpine/golang-1.26@1.26.0-r0?os_name=&os_version=",
    "digest": {
      "sha256": "4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838"
    }
  },
  "attestations": [
    {
      "predicate_type": "https://slsa.dev/provenance/v1",
      "digest": {
        "sha256": "97c919cf0edb27087739bbabeea4c1ef88d069cd41791476ba64b69280d63a32"
      },
      "url": "https://dhi.io/apk/alpine/v3.23/main/sha256:4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838/attestations/sha256:97c919cf0edb27087739bbabeea4c1ef88d069cd41791476ba64b69280d63a32"
    }
  ]
}
```

#### [Retrieve package attestations](#retrieve-package-attestations)

To retrieve the actual attestation content, use the URL provided in the attestation list:

```console
$ curl -s https://dhi.io/apk/alpine/v3.23/main/sha256:4082a2500abc2e7b8435f9398d3514d760044fa52ca3d10cf80015469124a838/attestations/sha256:97c919cf0edb27087739bbabeea4c1ef88d069cd41791476ba64b69280d63a32 | jq .
```

This returns the full SLSA provenance attestation for the package, which includes information about how the package was built, its dependencies, and other build materials.

You can continue this process recursively to trace the supply chain all the way down to the compiler and other build tools used to create the package.

----
url: https://docs.docker.com/dhi/explore/responsibility/
----

# Understanding roles and responsibilities for Docker Hardened Images

***

Table of contents

***

Docker Hardened Images (DHIs) are curated and maintained by Docker, and built using upstream open source components. To deliver security, reliability, and compliance, responsibilities are shared among three groups:

* Upstream maintainers: the developers and communities responsible for the open source software included in each image.
* Docker: the provider of hardened, signed, and maintained container images.
* You (the customer): the consumer who runs and, optionally, customizes DHIs in your environment.

This topic outlines who handles what, so you can use DHIs effectively and securely.

## [Releases](#releases)

* Upstream: Publishes and maintains official releases of the software components included in DHIs. This includes versioning, changelogs, and deprecation notices.
* Docker: Builds, hardens, and signs Docker Hardened Images based on upstream versions. Docker maintains these images in line with upstream release timelines and internal policies.
* You: Ensure you're staying on supported versions of DHIs and upstream projects. Using outdated or unsupported components can introduce security risk.

## [Patching](#patching)

* Upstream: Maintains and updates the source code for each component, including fixing vulnerabilities in libraries and dependencies.
* Docker: Rebuilds and re-releases images with upstream patches applied. Docker monitors for vulnerabilities and publishes updates to affected images. DHI Select and DHI Enterprise include [SLA commitments](https://docs.docker.com/go/dhi-sla/). DHI Community offers a secure baseline but no guaranteed remediation timelines.
* You: Apply DHI updates in your environments and patch any software or dependencies you install on top of the base image.

## [Testing](#testing)

* Upstream: Defines the behavior and functionality of the original software, and is responsible for validating core features.
* Docker: Validates that DHIs start, run, and behave consistently with upstream expectations. Docker also runs security scans and includes a [testing attestation](https://docs.docker.com/dhi/core-concepts/attestations/) with each image.
* You: Test your application on top of DHIs and validate that any changes or customizations function as expected in your environment.

## [Security and compliance](#security-and-compliance)

* Docker: Publishes signed SBOMs, VEX documents, provenance data, and CVE scan results with each image to support compliance and supply chain security.

  * For DHI Community users: All security metadata and transparency features are included at no cost.
  * For DHI Select and Enterprise users: Additional compliance variants (like FIPS and STIG) and customization capabilities are available, with automatic rebuilds when base images are patched.

* You: Integrate DHIs into your security and compliance workflows, including vulnerability management and auditing.

## [Support](#support)

* Docker:

  * For DHI Community users: Community support and public documentation are available.
  * For DHI Select and DHI Enterprise users: Access to Docker's enterprise support team for mission-critical applications.

* You: Monitor Docker's release notes, security advisories, and documentation for updates and best practices.

## [Summary](#summary)

Docker Hardened Images give you a secure foundation, complete with signed metadata and upstream transparency. Your role is to make informed use of these images, apply updates promptly, and validate that your configurations and applications meet your internal requirements.

----
url: https://docs.docker.com/reference/api/extensions-sdk/ExtensionVM/
----

# Interface: ExtensionVM

***

Table of contents

***

**`Since`**

0.2.0

## [Properties](#properties)

### [cli](#cli)

• `Readonly` **cli**: [`ExtensionCli`](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/)

Executes a command in the backend container.

Example: Execute the command `ls -l` inside the backend container:

```typescript
await ddClient.extension.vm.cli.exec(
  "ls",
  ["-l"]
);
```

Streams the output of the command executed in the backend container.

When the extension defines its own `compose.yaml` file with multiple containers, the command is executed on the first container defined. Change the order in which containers are defined to execute commands on another container.

Example: Spawn the command `ls -l` inside the backend container:

```typescript
await ddClient.extension.vm.cli.exec("ls", ["-l"], {
           stream: {
             onOutput(data): void {
                 // As we can receive both `stdout` and `stderr`, we wrap them in a JSON object
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```

**`Param`**

Command to execute.

**`Param`**

Arguments of the command to execute.

**`Param`**

The callback function where to listen from the command output data and errors.

***

### [service](#service)

• `Optional` `Readonly` **service**: [`HttpService`](https://docs.docker.com/reference/api/extensions-sdk/HttpService/)

----
url: https://docs.docker.com/reference/api/engine/version/v1.49.yaml
----

basePath: "/v1.49"
info:
 title: "Docker Engine API"
 version: "1.49"

 If you omit the version-prefix, the current version of the API (v1.49) is used.
 For example, calling \`/info\` is the same as calling \`/v1.49/info\`. Using the

 FirewallBackend:
 $ref: "#/definitions/FirewallInfo"

----
url: https://docs.docker.com/reference/cli/sbx/template/ls/
----

# sbx template ls

| Description | List template images      |
| ----------- | ------------------------- |
| Usage       | `sbx template ls [flags]` |

## [Description](#description)

List all template images stored in the sandbox runtime's image store.

## [Options](#options)

| Option   | Default | Description           |
| -------- | ------- | --------------------- |
| `--json` |         | Output in JSON format |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# List all template images
sbx template ls

# Output in JSON format
sbx template ls --json
```

----
url: https://docs.docker.com/extensions/extensions-sdk/dev/continuous-integration/
----

# Continuous Integration (CI)

***

Table of contents

***

In order to help validate your extension and ensure it's functional, the Extension SDK provides tools to help you setup continuous integration for your extension.

> Important
>
> The [Docker Desktop Action](https://github.com/docker/desktop-action) and the [extension-test-helper library](https://www.npmjs.com/package/@docker/extension-test-helper) are both [experimental](https://docs.docker.com/release-lifecycle/#experimental).

## [Setup CI environment with GitHub Actions](#setup-ci-environment-with-github-actions)

You need Docker Desktop to be able to install and validate your extension. You can start Docker Desktop in GitHub Actions using the [Docker Desktop Action](https://github.com/docker/desktop-action), by adding the following to a workflow file:

```yaml
steps:
  - id: start_desktop
    uses: docker/desktop-action/start@v0.1.0
```

> Note
>
> This action supports only GitHub Actions macOS runners at the moment. You need to specify `runs-on: macOS-latest` for your end to end tests.

Once the step has executed, the next steps use Docker Desktop and the Docker CLI to install and test the extension.

## [Validating your extension with Puppeteer](#validating-your-extension-with-puppeteer)

Once Docker Desktop starts in CI, you can build, install, and validate your extension with Jest and Puppeteer.

First, build and install the extension from your test:

```ts
import { DesktopUI } from "@docker/extension-test-helper";
import { exec as originalExec } from "child_process";
import * as util from "util";

export const exec = util.promisify(originalExec);

// keep a handle on the app to stop it at the end of tests
let dashboard: DesktopUI;

beforeAll(async () => {
  await exec(`docker build -t my/extension:latest .`, {
    cwd: "my-extension-src-root",
  });

  await exec(`docker extension install -f my/extension:latest`);
});
```

Then open the Docker Desktop Dashboard and run some tests in your extension's UI:

```ts
describe("Test my extension", () => {
  test("should be functional", async () => {
    dashboard = await DesktopUI.start();

    const eFrame = await dashboard.navigateToExtension("my/extension");

    // use puppeteer APIs to manipulate the UI, click on buttons, expect visual display and validate your extension
    await eFrame.waitForSelector("#someElementId");
  });
});
```

Finally, close the Docker Desktop Dashboard and uninstall your extension:

```ts
afterAll(async () => {
  dashboard?.stop();
  await exec(`docker extension uninstall my/extension`);
});
```

## [What's next](#whats-next)

* Build an [advanced frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) extension.
* Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).
* Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

----
url: https://docs.docker.com/guides/github-sonarqube-sandbox/
----

# How to build an AI-powered code quality workflow with SonarQube and E2B

Table of contents

***

Build AI-powered code quality workflows using E2B sandboxes with Docker's MCP catalog to automate GitHub and SonarQube integration.

**Time to complete** 40 minutes

This guide demonstrates how to build an AI-powered code quality workflow using [E2B sandboxes](https://e2b.dev/docs) with Docker’s MCP catalog. You’ll create a system that automatically analyzes code quality issues in GitHub repositories using SonarQube, then generate pull requests with fixes.

## [What you'll build](#what-youll-build)

You’ll build a Node.js script that spins up an E2B sandbox, connects GitHub and SonarQube MCP servers, and uses Claude Code to analyze code quality and propose improvements. The MCP servers are containerized and run as part of the E2B sandbox.

## [What you'll learn](#what-youll-learn)

In this guide, you'll learn:

* How to create E2B sandboxes with multiple MCP servers
* How to configure GitHub and SonarQube MCP servers for AI workflows
* How to use Claude Code inside sandboxes to interact with external tools
* How to build automated code review workflows that create quality-gated pull requests

## [Why use E2B sandboxes?](#why-use-e2b-sandboxes)

Running this workflow in E2B sandboes provides several advantages over local execution:

* Security: AI-generated code runs in isolated containers, protecting your local environment and credentials
* Zero setup: No need to install SonarQube, GitHub CLI, or manage dependencies locally
* Scalability: Resource-intensive operations like code scanning run in the cloud without consuming local resources

## [Learn more](#learn-more)

Read Docker's blog post: [Docker + E2B: Building the Future of Trusted AI](https://www.docker.com/blog/docker-e2b-building-the-future-of-trusted-ai/).

## [Modules](#modules)

1. [Build workflow](https://docs.docker.com/guides/github-sonarqube-sandbox/workflow/)

   Create E2B sandboxes, discover MCP tools, test individual operations, and build complete quality-gated PR workflows.

2. [Customize workflow](https://docs.docker.com/guides/github-sonarqube-sandbox/customize/)

   Learn how to customize prompts for specific quality issues, filter by file patterns, set quality thresholds, and integrate your workflow with GitHub Actions for automated code quality checks.

3. [Troubleshoot](https://docs.docker.com/guides/github-sonarqube-sandbox/troubleshoot/)

   Solutions for MCP tools not loading, authentication errors, permission issues, workflow timeouts, and other common problems when building code quality workflows with E2B.

----
url: https://docs.docker.com/guides/opentelemetry/
----

[Instrumenting a JavaScript App with OpenTelemetry](https://docs.docker.com/guides/opentelemetry/)

Learn how to instrument a JavaScript application using OpenTelemetry in a Dockerized environment.

JavaScript App development Observability

10 minutes

[« Back to all guides](/guides/)

# Instrumenting a JavaScript App with OpenTelemetry

***

Table of contents

***

OpenTelemetry (OTel) is an open-source observability framework that provides a set of APIs, SDKs, and tools for collecting telemetry data, such as metrics, logs, and traces, from applications. With OpenTelemetry, developers can obtain valuable insights into how their services perform in production or during local development.

A key component of OpenTelemetry is the OpenTelemetry Protocol (OTLP) a general-purpose, vendor-agnostic protocol designed to transmit telemetry data efficiently and reliably. OTLP supports multiple data types (traces, metrics, logs) over HTTP or gRPC, making it the default and recommended protocol for communication between instrumented applications, the OpenTelemetry Collector, and backends such as Jaeger or Prometheus.

This guide walks you through how to instrument a simple Node.js application with OpenTelemetry and run both the app and a collector using Docker. This setup is ideal for local development and testing observability before integrating with external observability platforms like Prometheus, Jaeger, or Grafana.

In this guide, you'll learn how to:

* How to set up OpenTelemetry in a Node.js app.
* How to run an OpenTelemetry Collector in Docker.
* How to visualize traces with Jaeger.
* How to use Docker Compose to manage the full observability stack.

## [Using OpenTelemetry with Docker](#using-opentelemetry-with-docker)

The [Docker Official Image for OpenTelemetry](https://hub.docker.com/r/otel/opentelemetry-collector-contrib) provides a convenient way to deploy and manage Dex instances. OpenTelemetry is available for various CPU architectures, including amd64, armv7, and arm64, ensuring compatibility with different devices and platforms. Same for the [Jaeger Docker image](https://hub.docker.com/r/jaegertracing/jaeger).

## [Prerequisites](#prerequisites)

[Docker Compose](/compose/): Recommended for managing multi-container Docker applications.

Basic knowledge of Node.js and Docker.

## [Project structure](#project-structure)

Create the project directory:

```bash
mkdir otel-js-app
cd otel-js-app
```

```bash
otel-js-app/
├── docker-compose.yaml
├── collector-config.yaml
├── app/
│   ├── package.json
│   ├── app.js
│   └── tracer.js
```

## [Create a simple Node.js app](#create-a-simple-nodejs-app)

Initialize a basic Node.js app:

```bash
mkdir app && cd app
npm init -y
npm install express @opentelemetry/api @opentelemetry/sdk-node \
            @opentelemetry/auto-instrumentations-node \
            @opentelemetry/exporter-trace-otlp-http
```

Now, add the application logic:

```js
// app/app.js
const express = require('express');
require('./tracer'); // Initialize OpenTelemetry

const app = express();

app.get('/', (req, res) => {
  res.send('Hello from OpenTelemetry demo app!');
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`App listening at http://localhost:${PORT}`);
});
```

## [Configure OpenTelemetry tracing](#configure-opentelemetry-tracing)

Create the tracer configuration file:

```js
// app/tracer.js
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-http');

const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
