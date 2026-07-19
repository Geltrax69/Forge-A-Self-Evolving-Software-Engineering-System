          url: "https://sonarcloud.io",
        },
      },
    });

    const mcpUrl = sbx.betaGetMcpUrl();
    const mcpToken = await sbx.betaGetMcpToken();

    await new Promise((resolve) => setTimeout(resolve, 1000));

    await sbx.commands.run(
      `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
      { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
    );

    const repoPath = `${process.env.GITHUB_OWNER}/${process.env.GITHUB_REPO}`;

    console.log("\nRunning workflow with error handling...\n");

    const prompt = `Run a quality improvement workflow for "${repoPath}".

    ERROR HANDLING RULES:
    1. If SonarQube is unreachable, explain the error and stop gracefully
    2. If GitHub API fails, retry once, then explain and stop
    3. If no fixable issues are found, explain why and exit (this is not an error)
    4. If file modifications fail, explain which file and why
    5. At each step, check for errors before proceeding

    Run the workflow and handle any errors you encounter professionally.`;

    await sbx.commands.run(
      `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
      {
        timeoutMs: 0,
        onStdout: console.log,
        onStderr: console.log,
      },
    );

    console.log("\n Workflow completed");
  } catch (error) {
    const err = error as Error;
    console.error("\n Workflow failed:", err.message);

    if (err.message.includes("403")) {
      console.error("\n Check your E2B account has MCP gateway access");
    } else if (err.message.includes("401")) {
      console.error("\n Check your API tokens are valid");
    } else if (err.message.includes("Credit balance")) {
      console.error("\n Check your Anthropic API credit balance");
    }

    process.exit(1);
  } finally {
    if (sbx) {
      console.log("\n Cleaning up sandbox...");
      await sbx.kill();
    }
  }
}

robustWorkflow().catch(console.error);
```

Run the script:

```bash
npx tsx 07-robust-workflow.ts
```

Create `07_robust_workflow.py`:

```python
import os
import asyncio
import sys
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def robust_workflow():
    sbx = None

    try:
        print("Creating sandbox...\n")

        sbx = await AsyncSandbox.beta_create(
            envs={
                "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
                "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
                "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
            },
            mcp={
                "githubOfficial": {
                    "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
                },
                "sonarqube": {
                    "org": os.getenv("SONARQUBE_ORG"),
                    "token": os.getenv("SONARQUBE_TOKEN"),
                    "url": "https://sonarcloud.io",
                },
            },
        )

        mcp_url = sbx.beta_get_mcp_url()
        mcp_token = await sbx.beta_get_mcp_token()

        await asyncio.sleep(1)

        await sbx.commands.run(
            f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
            timeout=0,  # Fixed: was timeout_ms
            on_stdout=print,
            on_stderr=print,
        )

        repo_path = f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}"

        print("\nRunning workflow with error handling...\n")

        prompt = f"""Run a quality improvement workflow for "{repo_path}".

        ERROR HANDLING RULES:
        1. If SonarQube is unreachable, explain the error and stop gracefully
        2. If GitHub API fails, retry once, then explain and stop
        3. If no fixable issues are found, explain why and exit (this is not an error)
        4. If file modifications fail, explain which file and why
        5. At each step, check for errors before proceeding

        Run the workflow and handle any errors you encounter professionally."""

        await sbx.commands.run(
            f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
            timeout=0,
            on_stdout=print,
            on_stderr=print,
        )

        print("\n Workflow completed")

    except Exception as error:
        print(f"\n✗ Workflow failed: {str(error)}")

        error_msg = str(error)
        if "403" in error_msg:
            print("\n Check your E2B account has MCP gateway access")
        elif "401" in error_msg:
            print("\n Check your API tokens are valid")
        elif "Credit balance" in error_msg:
            print("\n Check your Anthropic API credit balance")

        sys.exit(1)

    finally:
        if sbx:
            print("\n Cleaning up sandbox...")
            await sbx.kill()

if __name__ == "__main__":
    asyncio.run(robust_workflow())
```

Run the script:

```bash
python 07_robust_workflow.py
```

Claude will run the entire workflow, and if it encounters an error, respond with robust error messaging.

## [Next steps](#next-steps)

In the next section, you'll customize your workflow for your needs.

[Customize a code quality check workflow »](https://docs.docker.com/guides/github-sonarqube-sandbox/customize/)

----
url: https://docs.docker.com/ai/sandboxes/agents/
----

# Supported agents

***

***

Docker Sandboxes runs the following agents out of the box:

* [Claude Code](https://docs.docker.com/ai/sandboxes/agents/claude-code/)
* [Codex](https://docs.docker.com/ai/sandboxes/agents/codex/)
* [Copilot](https://docs.docker.com/ai/sandboxes/agents/copilot/)
* [Cursor](https://docs.docker.com/ai/sandboxes/agents/cursor/)
* [Droid](https://docs.docker.com/ai/sandboxes/agents/droid/)
* [Gemini](https://docs.docker.com/ai/sandboxes/agents/gemini/)
* [Kiro](https://docs.docker.com/ai/sandboxes/agents/kiro/)
* [OpenCode](https://docs.docker.com/ai/sandboxes/agents/opencode/)
* [Docker Agent](https://docs.docker.com/ai/sandboxes/agents/docker-agent/)
* [Shell](https://docs.docker.com/ai/sandboxes/agents/shell/) — agent-less sandbox for manual setup or testing

Want to pre-install tools or customize an agent's environment? See [Customize](https://docs.docker.com/ai/sandboxes/customize/).

----
url: https://docs.docker.com/engine/security/trust/
----

# Content trust in Docker

***

Table of contents

***

When transferring data among networked systems, trust is a central concern. In particular, when communicating over an untrusted medium such as the internet, it is critical to ensure the integrity and the publisher of all the data a system operates on. You use Docker Engine to push and pull images (data) to a public or private registry. Content trust gives you the ability to verify both the integrity and the publisher of all the data received from a registry over any channel.

## [About Docker Content Trust (DCT)](#about-docker-content-trust-dct)

Docker Content Trust (DCT) provides the ability to use digital signatures for data sent to and received from remote Docker registries. These signatures allow client-side or runtime verification of the integrity and publisher of specific image tags.

Through DCT, image publishers can sign their images and image consumers can ensure that the images they pull are signed. Publishers could be individuals or organizations manually signing their content or automated software supply chains signing content as part of their release process.

> Warning
>
> Docker Content Trust (DCT) is being retired. The Notary v1 service at `notary.docker.io` will shut down on December 8, 2026. For more information, see [Docker Content Trust (DCT)](https://docs.docker.com/retired/#docker-content-trust-dct).

### [Image tags and DCT](#image-tags-and-dct)

An individual image record has the following identifier:

```text
[REGISTRY_HOST[:REGISTRY_PORT]/]REPOSITORY[:TAG]
```

A particular image `REPOSITORY` can have multiple tags. For example, `latest` and `3.1.2` are both tags on the `mongo` image. An image publisher can build an image and tag combination many times changing the image with each build.

DCT is associated with the `TAG` portion of an image. Each image repository has a set of keys that image publishers use to sign an image tag. Image publishers have discretion on which tags they sign.

An image repository can contain an image with one tag that is signed and another tag that is not. For example, consider [the Mongo image repository](https://hub.docker.com/_/mongo/tags/). The `latest` tag could be unsigned while the `3.1.6` tag could be signed. It is the responsibility of the image publisher to decide if an image tag is signed or not. In this representation, some image tags are signed, others are not:

Publishers can choose to sign a specific tag or not. As a result, the content of an unsigned tag and that of a signed tag with the same name may not match. For example, a publisher can push a tagged image `someimage:latest` and sign it. Later, the same publisher can push an unsigned `someimage:latest` image. This second push replaces the last unsigned tag `latest` but does not affect the signed `latest` version. The ability to choose which tags they can sign, allows publishers to iterate over the unsigned version of an image before officially signing it.

Image consumers can enable DCT to ensure that images they use were signed. If a consumer enables DCT, they can only pull, run, or build with trusted images. Enabling DCT is a bit like applying a "filter" to your registry. Consumers "see" only signed image tags and the less desirable, unsigned image tags are "invisible" to them.

To the consumer who has not enabled DCT, nothing about how they work with Docker images changes. Every image is visible regardless of whether it is signed or not.

### [Docker Content Trust Keys](#docker-content-trust-keys)

Trust for an image tag is managed through the use of signing keys. A key set is created when an operation using DCT is first invoked. A key set consists of the following classes of keys:

* An offline key that is the root of DCT for an image tag
* Repository or tagging keys that sign tags
* Server-managed keys such as the timestamp key, which provides freshness security guarantees for your repository

The following image depicts the various signing keys and their relationships:

> Warning
>
> The root key once lost is not recoverable. If you lose any other key, send an email to [Docker Hub Support](mailto:hub-support@docker.com). This loss also requires manual intervention from every consumer that used a signed tag from this repository prior to the loss.

You should back up the root key somewhere safe. Given that it is only required to create new repositories, it is a good idea to store it offline in hardware. For details on securing, and backing up your keys, make sure you read how to [manage keys for DCT](https://docs.docker.com/engine/security/trust/trust_key_mng/).

## [Signing images with Docker Content Trust](#signing-images-with-docker-content-trust)

Within the Docker CLI we can sign and push a container image with the `$ docker trust` command syntax. This is built on top of the Notary feature set. For more information, see the [Notary GitHub repository](https://github.com/theupdateframework/notary).

A prerequisite for signing an image is a Docker Registry with a Notary server (such as Docker Hub) attached. Refer to [Deploying Notary](/engine/security/trust/deploying_notary/) for instructions.

To sign a Docker Image you will need a delegation key pair. These keys can be generated locally using `$ docker trust key generate` or generated by a certificate authority.

First we will add the delegation private key to the local Docker trust repository. (By default this is stored in `~/.docker/trust/`). If you are generating delegation keys with `$ docker trust key generate`, the private key is automatically added to the local trust store. If you are importing a separate key, you will need to use the `$ docker trust key load` command.

```console
$ docker trust key generate jeff
Generating key for jeff...
Enter passphrase for new jeff key with ID 9deed25:
Repeat passphrase for new jeff key with ID 9deed25:
Successfully generated and loaded private key. Corresponding public key available: /home/ubuntu/Documents/mytrustdir/jeff.pub
```

Or if you have an existing key:

```console
$ docker trust key load key.pem --name jeff
Loading key from "key.pem"...
Enter passphrase for new jeff key with ID 8ae710e:
Repeat passphrase for new jeff key with ID 8ae710e:
Successfully imported key from key.pem
```

Next we will need to add the delegation public key to the Notary server; this is specific to a particular image repository in Notary known as a Global Unique Name (GUN). If this is the first time you are adding a delegation to that repository, this command will also initiate the repository, using a local Notary canonical root key. To understand more about initiating a repository, and the role of delegations, head to [delegations for content trust](https://docs.docker.com/engine/security/trust/trust_delegation/).

```console
$ docker trust signer add --key cert.pem jeff registry.example.com/admin/demo
Adding signer "jeff" to registry.example.com/admin/demo...
Enter passphrase for new repository key with ID 10b5e94:
```

Finally, we will use the delegation private key to sign a particular tag and push it up to the registry.

```console
$ docker trust sign registry.example.com/admin/demo:1
Signing and pushing trust data for local image registry.example.com/admin/demo:1, may overwrite remote trust data
The push refers to repository [registry.example.com/admin/demo]
7bff100f35cb: Pushed
1: digest: sha256:3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e size: 528
Signing and pushing trust metadata
Enter passphrase for signer key with ID 8ae710e:
Successfully signed registry.example.com/admin/demo:1
```

Alternatively, once the keys have been imported an image can be pushed with the `$ docker push` command, by exporting the DCT environmental variable.

```console
$ export DOCKER_CONTENT_TRUST=1

$ docker push registry.example.com/admin/demo:1
The push refers to repository [registry.example.com/admin/demo:1]
7bff100f35cb: Pushed
1: digest: sha256:3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e size: 528
Signing and pushing trust metadata
Enter passphrase for signer key with ID 8ae710e:
Successfully signed registry.example.com/admin/demo:1
```

Remote trust data for a tag or a repository can be viewed by the `$ docker trust inspect` command:

```console
$ docker trust inspect --pretty registry.example.com/admin/demo:1

Signatures for registry.example.com/admin/demo:1

SIGNED TAG          DIGEST                                                             SIGNERS
1                   3d2e482b82608d153a374df3357c0291589a61cc194ec4a9ca2381073a17f58e   jeff

List of signers and their keys for registry.example.com/admin/demo:1

SIGNER              KEYS
jeff                8ae710e3ba82

Administrative keys for registry.example.com/admin/demo:1

  Repository Key:	10b5e94c916a0977471cc08fa56c1a5679819b2005ba6a257aa78ce76d3a1e27
  Root Key:	84ca6e4416416d78c4597e754f38517bea95ab427e5f95871f90d460573071fc
```

Remote Trust data for a tag can be removed by the `$ docker trust revoke` command:

```console
$ docker trust revoke registry.example.com/admin/demo:1
Enter passphrase for signer key with ID 8ae710e:
Successfully deleted signature for registry.example.com/admin/demo:1
```

## [Client enforcement with Docker Content Trust](#client-enforcement-with-docker-content-trust)

Content trust is disabled by default in the Docker Client. To enable it, set the `DOCKER_CONTENT_TRUST` environment variable to `1`. This prevents users from working with tagged images unless they contain a signature.

When DCT is enabled in the Docker client, `docker` CLI commands that operate on tagged images must either have content signatures or explicit content hashes. The commands that operate with DCT are:

* `push`
* `build`
* `create`
* `pull`
* `run`

For example, with DCT enabled a `docker pull someimage:latest` only succeeds if `someimage:latest` is signed. However, an operation with an explicit content hash always succeeds as long as the hash exists:

```console
$ docker pull registry.example.com/user/image:1
Error: remote trust data does not exist for registry.example.com/user/image: registry.example.com does not have trust data for registry.example.com/user/image

$ docker pull registry.example.com/user/image@sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a
sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1: Pulling from user/image
ff3a5c916c92: Pull complete
a59a168caba3: Pull complete
Digest: sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1
Status: Downloaded newer image for registry.example.com/user/image@sha256:ee7491c9c31db1ffb7673d91e9fac5d6354a89d0e97408567e09df069a1687c1
```

## [Related information](#related-information)

* [Delegations for content trust](https://docs.docker.com/engine/security/trust/trust_delegation/)
* [Automation with content trust](https://docs.docker.com/engine/security/trust/trust_automation/)
* [Manage keys for content trust](https://docs.docker.com/engine/security/trust/trust_key_mng/)
* [Play in a content trust sandbox](https://docs.docker.com/engine/security/trust/trust_sandbox/)

----
url: https://docs.docker.com/build/metadata/annotations/
----

# Annotations

***

Table of contents

***

Annotations provide descriptive metadata for images. Use annotations to record arbitrary information and attach it to your image, which helps consumers and tools understand the origin, contents, and how to use the image.

Annotations are similar to, and in some sense overlap with, [labels](https://docs.docker.com/engine/manage-resources/labels/). Both serve the same purpose: to attach metadata to a resource. As a general principle, you can think of the difference between annotations and labels as follows:

* Annotations describe OCI image components, such as [manifests](https://github.com/opencontainers/image-spec/blob/main/manifest.md), [indexes](https://github.com/opencontainers/image-spec/blob/main/image-index.md), and [descriptors](https://github.com/opencontainers/image-spec/blob/main/descriptor.md).
* Labels describe Docker resources, such as images, containers, networks, and volumes.

The OCI image [specification](https://github.com/opencontainers/image-spec/blob/main/annotations.md) defines the format of annotations, as well as a set of pre-defined annotation keys. Adhering to the specified standards ensures that metadata about images can be surfaced automatically and consistently, by tools like Docker Scout.

Annotations are not to be confused with [attestations](https://docs.docker.com/build/metadata/attestations/):

* Attestations contain information about how an image was built and what it contains. An attestation is attached as a separate manifest on the image index. Attestations are not standardized by the Open Container Initiative.
* Annotations contain arbitrary metadata about an image. Annotations attach to the image [config](https://github.com/opencontainers/image-spec/blob/main/config.md) as labels, or on the image index or manifest as properties.

## [Add annotations](#add-annotations)

You can add annotations to an image at build-time, or when creating the image manifest or index.

> Note
>
> The Docker Engine image store doesn't support loading images with annotations. To build with annotations, make sure to push the image directly to a registry, using the `--push` CLI flag or the [registry exporter](https://docs.docker.com/build/exporters/image-registry/).

To specify annotations on the command line, use the `--annotation` flag for the `docker build` command:

```console
$ docker build --push --annotation "foo=bar" .
```

If you're using [Bake](https://docs.docker.com/build/bake/), you can use the `annotations` attribute to specify annotations for a given target:

```hcl
target "default" {
  output = ["type=registry"]
  annotations = ["foo=bar"]
}
```

For examples on how to add annotations to images built with GitHub Actions, see [Add image annotations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/annotations/)

You can also add annotations to an image created using `docker buildx imagetools create`. This command only supports adding annotations to an index or manifest descriptors, see [CLI reference](/reference/cli/docker/buildx/imagetools/create/#annotation).

## [Inspect annotations](#inspect-annotations)

To view annotations on an **image index**, use the `docker buildx imagetools inspect` command. This shows you any annotations for the index and descriptors (references to manifests) that the index contains. The following example shows an `org.opencontainers.image.documentation` annotation on a descriptor, and an `org.opencontainers.image.authors` annotation on the index.

```console
$ docker buildx imagetools inspect IMAGE --raw
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb",
      "size": 911,
      "annotations": {
        "org.opencontainers.image.documentation": "https://foo.example/docs",
      },
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
  ],
  "annotations": {
    "org.opencontainers.image.authors": "dvdksn"
  }
}
```

To inspect annotations on a manifest, use the `docker buildx imagetools inspect` command and specify `<IMAGE>@<DIGEST>`, where `<DIGEST>` is the digest of the manifest:

```console
$ docker buildx imagetools inspect IMAGE@sha256:d20246ef744b1d05a1dd69d0b3fa907db007c07f79fe3e68c17223439be9fefb --raw
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:4368b6959a78b412efa083c5506c4887e251f1484ccc9f0af5c406d8f76ece1d",
    "size": 850
  },
  "layers": [
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:2c03dbb20264f09924f9eab176da44e5421e74a78b09531d3c63448a7baa7c59",
      "size": 3333033
    },
    {
      "mediaType": "application/vnd.oci.image.layer.v1.tar+gzip",
      "digest": "sha256:4923ad480d60a548e9b334ca492fa547a3ce8879676685b6718b085de5aaf142",
      "size": 61887305
    }
  ],
  "annotations": {
    "index,manifest:org.opencontainers.image.vendor": "foocorp",
    "org.opencontainers.image.source": "https://git.example/foo.git",
  }
}
```

## [Specify annotation level](#specify-annotation-level)

By default, annotations are added to the image manifest. You can specify which level (OCI image component) to attach the annotation to by prefixing the annotation string with a special type declaration:

```console
$ docker build --annotation "TYPE:KEY=VALUE" .
```

The following types are supported:

* `manifest`: annotates manifests.
* `index`: annotates the root index.
* `manifest-descriptor`: annotates manifest descriptors in the index.
* `index-descriptor`: annotates the index descriptor in the image layout.

For example, to build an image with the annotation `foo=bar` attached to the image index:

```console
$ docker build --tag IMAGE --push --annotation "index:foo=bar" .
```

Note that the build must produce the component that you specify, or else the build will fail. For example, the following does not work, because the `docker` exporter does not produce an index:

```console
$ docker build --output type=docker --annotation "index:foo=bar" .
```

Likewise, the following example also does not work, because buildx creates a `docker` output by default under some circumstances, such as when provenance attestations are explicitly disabled:

```console
$ docker build --provenance=false --annotation "index:foo=bar" .
```

It is possible to specify types, separated by a comma, to add the annotation to more than one level. The following example creates an image with the annotation `foo=bar` on both the image index and the image manifest:

```console
$ docker build --tag IMAGE --push --annotation "index,manifest:foo=bar" .
```

You can also specify a platform qualifier within square brackets in the type prefix, to annotate only components matching specific OS and architectures. The following example adds the `foo=bar` annotation only to the `linux/amd64` manifest:

```console
$ docker build --tag IMAGE --push --annotation "manifest[linux/amd64]:foo=bar" .
```

## [Related information](#related-information)

Related articles:

* [Add image annotations with GitHub Actions](https://docs.docker.com/build/ci/github-actions/annotations/)
* [Annotations OCI specification](https://github.com/opencontainers/image-spec/blob/main/annotations.md)

Reference information:

* [`docker buildx build --annotation`](/reference/cli/docker/buildx/build/#annotation)
* [Bake file reference: `annotations`](https://docs.docker.com/build/bake/reference/#targetannotations)
* [`docker buildx imagetools create --annotation`](/reference/cli/docker/buildx/imagetools/create/#annotation)

----
url: https://docs.docker.com/reference/cli/sbx/secret/
----

# sbx secret

| Description | Manage stored secrets |
| ----------- | --------------------- |

## [Description](#description)

Manage stored secrets for sandbox environments.

SERVICE SECRETS (e.g. "github", "anthropic", "openai") When a sandbox starts, the proxy uses stored secrets to authenticate API requests on behalf of the agent. The secret is never exposed directly. Scoped globally (shared across all sandboxes) or to a specific sandbox.

REGISTRY SECRETS (e.g. "ghcr.io", "myregistry.azurecr.io") Used to pull private template images and kit artifacts before sandbox creation. Host-only secrets (no -g) are not injected into sandboxes; global secrets (-g) are written as \~/.docker/config.json in every new sandbox. Use "sbx secret set --registry --password-stdin" to store them.

## [Commands](#commands)

| Command                                                                                 | Description                                   |
| --------------------------------------------------------------------------------------- | --------------------------------------------- |
| [`sbx secret ls`](https://docs.docker.com/reference/cli/sbx/secret/ls/)                 | List stored secrets                           |
| [`sbx secret rm`](https://docs.docker.com/reference/cli/sbx/secret/rm/)                 | Remove a secret                               |
| [`sbx secret set`](https://docs.docker.com/reference/cli/sbx/secret/set/)               | Create or update a secret                     |
| [`sbx secret set-custom`](https://docs.docker.com/reference/cli/sbx/secret/set-custom/) | experimental Create or update a custom secret |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/reference/cli/docker/desktop/engine/
----

# docker desktop engine

***

| Description | Commands to list and switch containers (Windows only) |
| ----------- | ----------------------------------------------------- |
| Usage       | `docker desktop engine`                               |

## [Subcommands](#subcommands)

| Command                                                                                         | Description                                          |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [`docker desktop engine ls`](https://docs.docker.com/reference/cli/docker/desktop/engine/ls/)   | List available engines (Windows only)                |
| [`docker desktop engine use`](https://docs.docker.com/reference/cli/docker/desktop/engine/use/) | Switch to Windows or Linux containers (Windows only) |

----
url: https://docs.docker.com/reference/cli/docker/sandbox/version/
----

# docker sandbox version

***

| Description | Show sandbox version information |
| ----------- | -------------------------------- |
| Usage       | `docker sandbox version`         |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Show sandbox version information

## [Examples](#examples)

### [Show version information](#show-version-information)

```console
$ docker sandbox version
github.com/docker/sandboxes/cli-plugin v0.7.1 f00f0d6473647c2201cd0507ce31613345c48ae6
```

----
url: https://docs.docker.com/guides/rust/
----

# Rust language-specific guide

***

This guide covers how to containerize Rust applications using Docker.

**Time to complete** 20 minutes

The Rust language-specific guide teaches you how to create a containerized Rust application using Docker. In this guide, you'll learn how to:

* Containerize a Rust application
* Build an image and run the newly built image as a container
* Set up volumes and networking
* Orchestrate containers using Compose
* Use containers for development
* Configure a CI/CD pipeline for your application using GitHub Actions
* Deploy your containerized Rust application locally to Kubernetes to test and debug your deployment

After completing the Rust modules, you should be able to containerize your own Rust application based on the examples and instructions provided in this guide.

Start with building your first Rust image.

## [Modules](#modules)

1. [Build images](https://docs.docker.com/guides/rust/build-images/)

   Learn how to build your first Rust Docker image

2. [Run containers](https://docs.docker.com/guides/rust/run-containers/)

   Learn how to run your Rust image as a container.

3. [Develop your app](https://docs.docker.com/guides/rust/develop/)

   Learn how to develop your Rust application locally.

4. [Configure CI/CD](https://docs.docker.com/guides/rust/configure-ci-cd/)

   Learn how to Configure CI/CD for your application

5. [Test your deployment](https://docs.docker.com/guides/rust/deploy/)

   Learn how to test your Rust deployment locally using Kubernetes

----
url: https://docs.docker.com/compose/how-tos/provider-services/
----

# Use provider services

***

Table of contents

***

Requires: Docker Compose [2.36.0](https://github.com/docker/compose/releases/tag/v2.36.0) and later

Docker Compose supports provider services, which allow integration with services whose lifecycles are managed by third-party components rather than by Compose itself.\
This feature enables you to define and utilize platform-specific services without the need for manual setup or direct lifecycle management.

## [What are provider services?](#what-are-provider-services)

Provider services are a special type of service in Compose that represents platform capabilities rather than containers. They allow you to declare dependencies on specific platform features that your application needs.

When you define a provider service in your Compose file, Compose works with the platform to provision and configure the requested capability, making it available to your application services.

## [Using provider services](#using-provider-services)

To use a provider service in your Compose file, you need to:

1. Define a service with the `provider` attribute
2. Specify the `type` of provider you want to use
3. Configure any provider-specific options
4. Declare dependencies from your application services to the provider service

Here's a basic example:

```yaml
services:
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar  
  app:
    image: myapp 
    depends_on:
       - database
```

Notice the dedicated `provider` attribute in the `database` service. This attribute specifies that the service is managed by a provider and lets you define options specific to that provider type.

The `depends_on` attribute in the `app` service specifies that it depends on the `database` service. This means that the `database` service will be started before the `app` service, allowing the provider information to be injected into the `app` service.

## [How it works](#how-it-works)

During the `docker compose up` command execution, Compose identifies services relying on providers and works with them to provision the requested capabilities. The provider then populates Compose model with information about how to access the provisioned resource.

This information is passed to services that declare a dependency on the provider service, typically through environment variables. The naming convention for these variables is:

```env
<PROVIDER_SERVICE_NAME>_<VARIABLE_NAME>
```

For example, if your provider service is named `database`, your application service might receive environment variables like:

* `DATABASE_URL` with the URL to access the provisioned resource
* `DATABASE_TOKEN` with an authentication token
* Other provider-specific variables

Your application can then use these environment variables to interact with the provisioned resource.

## [Provider types](#provider-types)

The `type` field in a provider service references the name of either:

1. A Docker CLI plugin (e.g., `docker-model`)
2. A binary available in the user's PATH
3. A path to the binary or script to execute

When Compose encounters a provider service, it looks for a plugin or binary with the specified name to handle the provisioning of the requested capability.

For example, if you specify `type: model`, Compose will look for a Docker CLI plugin named `docker-model` or a binary named `model` in the PATH.

```yaml
services:
  ai-runner:
    provider:
      type: model  # Looks for docker-model plugin or model binary
      options:
        model: ai/example-model
```

The plugin or binary is responsible for:

1. Interpreting the options provided in the provider service
2. Provisioning the requested capability
3. Returning information about how to access the provisioned resource

This information is then passed to dependent services as environment variables.

> Tip
>
> If you're working with AI models in Compose, use the [`models` top-level element](https://docs.docker.com/ai/compose/models-and-compose/) instead.

## [Benefits of using provider services](#benefits-of-using-provider-services)

Using provider services in your Compose applications offers several benefits:

1. Simplified configuration: You don't need to manually configure and manage platform capabilities
2. Declarative approach: You can declare all your application's dependencies in one place
3. Consistent workflow: You use the same Compose commands to manage your entire application, including platform capabilities

## [Creating your own provider](#creating-your-own-provider)

If you want to create your own provider to extend Compose with custom capabilities, you can implement a Compose plugin that registers provider types.

For detailed information on how to create and implement your own provider, refer to the [Compose Extensions documentation](https://github.com/docker/compose/blob/main/docs/extension.md).\
This guide explains the extension mechanism that allows you to add new provider types to Compose.

## [Reference](#reference)

* [Docker Model Runner documentation](https://docs.docker.com/ai/model-runner/)
* [Compose Extensions documentation](https://github.com/docker/compose/blob/main/docs/extension.md)

----
url: https://docs.docker.com/reference/build-checks/maintainer-deprecated/
----

# MaintainerDeprecated

***

Table of contents

***

## [Output](#output)

```text
MAINTAINER instruction is deprecated in favor of using label
```

## [Description](#description)

The `MAINTAINER` instruction, used historically for specifying the author of the Dockerfile, is deprecated. To set author metadata for an image, use the `org.opencontainers.image.authors` [OCI label](https://github.com/opencontainers/image-spec/blob/main/annotations.md#pre-defined-annotation-keys).

## [Examples](#examples)

❌ Bad: don't use the `MAINTAINER` instruction

```dockerfile
MAINTAINER moby@example.com
```

✅ Good: specify the author using the `org.opencontainers.image.authors` label

```dockerfile
LABEL org.opencontainers.image.authors="moby@example.com"
```

----
url: https://docs.docker.com/guides/java/develop/
----

# Use containers for Java development

***

Table of contents

***

## [Prerequisites](#prerequisites)

Work through the steps to containerize your application in [Containerize your app](https://docs.docker.com/guides/java/containerize/).

## [Overview](#overview)

In this section, you’ll walk through setting up a local development environment for the application you containerized in the previous section. This includes:

* Adding a local database and persisting data
* Creating a development container to connect a debugger
* Configuring Compose to automatically update your running Compose services as you edit and save your code

## [Add a local database and persist data](#add-a-local-database-and-persist-data)

You can use containers to set up local services, like a database. In this section, you'll update the `docker-compose.yaml` file to define a database service and a volume to persist data. Also, this particular application uses a system property to define the database type, so you'll need to update the `Dockerfile` to pass in the system property when starting the app.

In the cloned repository's directory, open the `docker-compose.yaml` file in an IDE or text editor. Your Compose file has an example database service, but it'll require a few changes for your unique app.

In the `docker-compose.yaml` file, you need to do the following:

* Uncomment all of the database instructions. You'll now use a database service instead of local storage for the data.
* Remove the top-level `secrets` element as well as the element inside the `db` service. This example uses the environment variable for the password rather than secrets.
* Remove the `user` element from the `db` service. This example specifies the user in the environment variable.
* Update the database environment variables. These are defined by the Postgres image. For more details, see the [Postgres Official Docker Image](https://hub.docker.com/_/postgres).
* Update the healthcheck test for the `db` service and specify the user. By default, the healthcheck uses the root user instead of the `petclinic` user you defined.
* Add the database URL as an environment variable in the `server` service. This overrides the default value defined in `spring-petclinic/src/main/resources/application-postgres.properties`.

The following is the updated `docker-compose.yaml` file. All comments have been removed.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

Open the `Dockerfile` in an IDE or text editor. In the `ENTRYPOINT` instruction, update the instruction to pass in the system property as specified in the `spring-petclinic/src/resources/db/postgres/petclinic_db_setup_postgres.txt` file.

```diff
- ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
+ ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

Save and close all the files.

Now, run the following `docker compose up` command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:8080>. You should see a simple app for a pet clinic. Browse around the application. Navigate to **Veterinarians** and verify that the application is connected to the database by being able to list veterinarians.

In the terminal, press `ctrl`+`c` to stop the application.

## [Dockerfile for development](#dockerfile-for-development)

The Dockerfile you have now is great for a small, secure production image with only the components necessary to run the application. When developing, you may want a different image that has a different environment.

For example, in the development image you may want to set up the image to start the application so that you can connect a debugger to the running Java process.

Rather than managing multiple Dockerfiles, you can add a new stage. Your Dockerfile can then produce a final image which is ready for production as well as a development image.

Replace the contents of your Dockerfile with the following.

```dockerfile
# syntax=docker/dockerfile:1

FROM eclipse-temurin:21-jdk-jammy as deps
WORKDIR /build
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

FROM deps as package
WORKDIR /build
COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

FROM package as extract
WORKDIR /build
RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

FROM extract as development
WORKDIR /build
RUN cp -r /build/target/extracted/dependencies/. ./
RUN cp -r /build/target/extracted/spring-boot-loader/. ./
RUN cp -r /build/target/extracted/snapshot-dependencies/. ./
RUN cp -r /build/target/extracted/application/. ./
ENV JAVA_TOOL_OPTIONS -agentlib:jdwp=transport=dt_socket,server=y,suspend=n,address=*:8000
CMD [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]

FROM eclipse-temurin:21-jre-jammy AS final
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./
EXPOSE 8080
ENTRYPOINT [ "java", "-Dspring.profiles.active=postgres", "org.springframework.boot.loader.launch.JarLauncher" ]
```

Save and close the `Dockerfile`.

In the `Dockerfile` you added a new stage labeled `development` based on the `extract` stage. In this stage, you copy the extracted files to a common directory, then run a command to start the application. In the command, you expose port 8000 and declare the debug configuration for the JVM so that you can attach a debugger.

## [Use Compose to develop locally](#use-compose-to-develop-locally)

The current Compose file doesn't start your development container. To do that, you must update your Compose file to target the development stage. Also, update the port mapping of the server service to provide access for the debugger.

Open the `docker-compose.yaml` and add the following instructions into the file.

```yaml
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

Now, start your application and to confirm that it's running.

```console
$ docker compose up --build
```

Finally, test your API endpoint. Run the following curl command:

```console
$ curl  --request GET \
  --url http://localhost:8080/vets \
  --header 'content-type: application/json'
```

You should receive the following response:

```json
{
  "vetList": [
    {
      "id": 1,
      "firstName": "James",
      "lastName": "Carter",
      "specialties": [],
      "nrOfSpecialties": 0,
      "new": false
    },
    {
      "id": 2,
      "firstName": "Helen",
      "lastName": "Leary",
      "specialties": [{ "id": 1, "name": "radiology", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 3,
      "firstName": "Linda",
      "lastName": "Douglas",
      "specialties": [
        { "id": 3, "name": "dentistry", "new": false },
        { "id": 2, "name": "surgery", "new": false }
      ],
      "nrOfSpecialties": 2,
      "new": false
    },
    {
      "id": 4,
      "firstName": "Rafael",
      "lastName": "Ortega",
      "specialties": [{ "id": 2, "name": "surgery", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 5,
      "firstName": "Henry",
      "lastName": "Stevens",
      "specialties": [{ "id": 1, "name": "radiology", "new": false }],
      "nrOfSpecialties": 1,
      "new": false
    },
    {
      "id": 6,
      "firstName": "Sharon",
      "lastName": "Jenkins",
      "specialties": [],
      "nrOfSpecialties": 0,
      "new": false
    }
  ]
}
```

## [Connect a Debugger](#connect-a-debugger)

You’ll use the debugger that comes with the IntelliJ IDEA. You can use the community version of this IDE. Open your project in IntelliJ IDEA, go to the **Run** menu, and then **Edit Configuration**. Add a new Remote JVM Debug configuration similar to the following:

Set a breakpoint.

Open `src/main/java/org/springframework/samples/petclinic/vet/VetController.java` and add a breakpoint inside the `showResourcesVetList` function.

To start your debug session, select the **Run** menu and then **Debug *NameOfYourConfiguration***.

You should now see the connection in the logs of your Compose application.

You can now call the server endpoint.

```console
$ curl --request GET --url http://localhost:8080/vets
```

You should have seen the code break on the marked line and now you are able to use the debugger just like you would normally. You can also inspect and watch variables, set conditional breakpoints, view stack traces and a do bunch of other stuff.

Press `ctrl+c` in the terminal to stop your application.

## [Automatically update services](#automatically-update-services)

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `docker-compose.yaml` file in an IDE or text editor and then add the Compose Watch instructions. The following is the updated `docker-compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
      - 8000:8000
    depends_on:
      db:
        condition: service_healthy
    environment:
      - POSTGRES_URL=jdbc:postgresql://db:5432/petclinic
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=petclinic
      - POSTGRES_USER=petclinic
      - POSTGRES_PASSWORD=petclinic
    ports:
      - 5432:5432
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "petclinic"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Open a web browser and view the application at <http://localhost:8080>. You should see the Spring Pet Clinic home page.

Any changes to the application's source files on your local machine will now be automatically reflected in the running container.

Open `spring-petclinic/src/main/resources/templates/fragments/layout.html` in an IDE or text editor and update the `Home` navigation string by adding an exclamation mark.

```diff
-   <li th:replace="~{::menuItem ('/','home','home page','home','Home')}">
+   <li th:replace="~{::menuItem ('/','home','home page','home','Home!')}">
```

Save the changes to `layout.html` and then you can continue developing while the container automatically rebuilds.

After the container is rebuilt and running, refresh <http://localhost:8080> and then verify that **Home!** now appears in the menu.

Press `ctrl+c` in the terminal to stop Compose Watch.

## [Summary](#summary)

In this section, you took a look at running a database locally and persisting the data. You also created a development image that contains the JDK and lets you attach a debugger. Finally, you set up your Compose file to expose the debugging port and configured Compose Watch to live reload your changes.

Related information:

* [Compose file reference](/reference/compose-file/)
* [Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/)
* [Dockerfile reference](/reference/dockerfile/)

## [Next steps](#next-steps)

In the next section, you’ll take a look at how to run unit tests in Docker.

[Run your Java tests »](https://docs.docker.com/guides/java/run-tests/)

----
url: https://docs.docker.com/guides/claude-code-sandbox-model-runner/
----

[Run Claude Code in a Docker Sandbox with Docker Model Runner](https://docs.docker.com/guides/claude-code-sandbox-model-runner/)

Combine Docker Sandboxes with Docker Model Runner to run Claude Code in an isolated microVM that talks to a local model on your host through the Anthropic-compatible API.

AI

15 minutes

[« Back to all guides](/guides/)

# Run Claude Code in a Docker Sandbox with Docker Model Runner

***

Table of contents

***

This guide shows how to run Claude Code inside a Docker Sandbox with Docker Model Runner as the backend model provider. You'll keep the agent isolated from your host in a microVM, point it at a local model on your machine, and keep all model traffic on-device.

> **Acknowledgment**
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

In this guide, you'll learn how to:

* Pull a coding model and start Docker Model Runner with TCP enabled
* Allow the sandbox to reach Docker Model Runner on your host
* Create a Claude Code sandbox and set the local endpoint persistently
* Launch Claude Code with a local model and verify the connection
* Package `gpt-oss` with a larger context window for longer prompts

## [How the pieces fit together](#how-the-pieces-fit-together)

Three components cooperate at runtime:

* **Docker Model Runner** runs on your host and serves an Anthropic-compatible API at `http://localhost:12434`.
* **The Docker Sandbox** runs Claude Code inside an isolated microVM. The microVM has its own network and can't reach your host's `localhost` directly.
* **The sandbox proxy** sits on your host and brokers every outbound request from the sandbox. It enforces network policy and translates the special hostname `host.docker.internal` to `localhost`.

Claude Code inside the sandbox sends requests to `http://host.docker.internal:12434`. The proxy rewrites the destination to `localhost:12434`, which Docker Model Runner answers. No model traffic leaves your machine.

## [Prerequisites](#prerequisites)

Before you start, make sure you have:

* [Docker Desktop](https://docs.docker.com/get-started/get-docker/) or Docker Engine installed
* [Docker Model Runner enabled](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner)
* [Docker Sandboxes (`sbx`) installed and signed in](https://docs.docker.com/ai/sandboxes/get-started/#install-and-sign-in)

If you use Docker Desktop, turn on TCP access in **Settings** > **AI**, or run:

```console
$ docker desktop enable model-runner --tcp 12434
```

## [Step 1: Pull a coding model](#step-1-pull-a-coding-model)

Pull a model on your host before you create the sandbox:

```console
$ docker model pull ai/devstral-small-2
```

You can also use `ai/qwen3-coder` if you want another coding-focused model with a large context window.

## [Step 2: Allow the sandbox to reach Docker Model Runner](#step-2-allow-the-sandbox-to-reach-docker-model-runner)

Sandboxes are network-isolated by default, so you need a policy rule before the sandbox can reach Docker Model Runner.

The rule is matched against the destination the proxy forwards to, not the hostname the sandbox uses. Because the proxy rewrites `host.docker.internal` to `localhost` before forwarding, the rule allows `localhost:12434` even though Claude Code will use `host.docker.internal` in its requests:

```console
$ sbx policy allow network localhost:12434
```

For background on host access from sandboxes, see [Accessing host services from a sandbox](https://docs.docker.com/ai/sandboxes/usage/#accessing-host-services-from-a-sandbox).

## [Step 3: Create a Claude Code sandbox](#step-3-create-a-claude-code-sandbox)

From your project directory, create a sandbox without launching the agent:

```console
$ cd ~/my-project
$ sbx create claude --name claude-dmr .
```

`sbx run` would also work, but it launches Claude Code immediately. Without `ANTHROPIC_BASE_URL` set, Claude Code points at `api.anthropic.com` and either prompts for OAuth or errors out before you can fix the endpoint. Creating the sandbox first lets you write the local endpoint into it before the agent starts.

You don't need to set an Anthropic API key or run `sbx secret set anthropic`. Docker Model Runner doesn't authenticate the local endpoint, and the sandbox proxy only injects credentials for requests bound for `api.anthropic.com`. See [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/) for the full list of services the proxy authenticates.

## [Step 4: Set the local endpoint inside the sandbox](#step-4-set-the-local-endpoint-inside-the-sandbox)

Append `ANTHROPIC_BASE_URL` to the sandbox's persistent environment file so Claude Code reads it on every launch:

```console
$ sbx exec -d claude-dmr bash -c "echo 'export ANTHROPIC_BASE_URL=http://host.docker.internal:12434' >> /etc/sandbox-persistent.sh"
```

The `bash -c` wrapper ensures the `>>` redirect runs inside the sandbox, not on your host. For details on this approach, see [How do I set custom environment variables inside a sandbox?](https://docs.docker.com/ai/sandboxes/faq/#how-do-i-set-custom-environment-variables-inside-a-sandbox).

To confirm the variable is set, open a shell in the sandbox:

```console
$ sbx exec -it claude-dmr bash
$ echo $ANTHROPIC_BASE_URL
http://host.docker.internal:12434
```

## [Step 5: Verify connectivity to Docker Model Runner](#step-5-verify-connectivity-to-docker-model-runner)

Still inside the sandbox shell, send a test request to the host endpoint:

```console
$ curl http://host.docker.internal:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/devstral-small-2",
    "max_tokens": 32,
    "messages": [{"role": "user", "content": "Say hello"}]
  }'
```

A successful response confirms the policy rule and base URL are correct. Type `exit` to leave the shell. For more details about the request format, see the [Anthropic-compatible API reference](https://docs.docker.com/ai/model-runner/api-reference/#anthropic-compatible-api).

## [Step 6: Launch Claude Code with the local model](#step-6-launch-claude-code-with-the-local-model)

Run Claude Code in the sandbox and pass the model flag through to the agent:

```console
$ sbx run claude-dmr -- --model ai/devstral-small-2
```

Everything after `--` is forwarded to the Claude Code CLI. Because `ANTHROPIC_BASE_URL` is set in the sandbox's persistent environment, Claude Code routes requests to Docker Model Runner on your host instead of `api.anthropic.com`.

## [Step 7: Inspect Claude Code requests](#step-7-inspect-claude-code-requests)

To inspect the requests Claude Code sends, run on your host:

```console
$ docker model requests --model ai/devstral-small-2 | jq .
```

This helps you debug prompts, context usage, and compatibility issues without attaching to the sandbox.

## [Step 8: Package `gpt-oss` with a larger context window](#step-8-package-gpt-oss-with-a-larger-context-window)

`ai/gpt-oss` defaults to a smaller context window than coding-focused models. To use it for repository-scale prompts, package a larger variant on the host:

```console
$ docker model pull ai/gpt-oss
$ docker model package --from ai/gpt-oss --context-size 32000 gpt-oss:32k
```

Then point Claude Code at the packaged model the next time you run the sandbox:

```console
$ sbx run claude-dmr -- --model gpt-oss:32k
```

## [Clean up](#clean-up)

Sandboxes persist after Claude Code exits. To stop the sandbox without deleting it:

```console
$ sbx stop claude-dmr
```

To remove the sandbox and everything inside, including the persistent environment file:

```console
$ sbx rm claude-dmr
```

Files in your workspace are unaffected.

## [Learn more](#learn-more)

* [Use Claude Code with Docker Model Runner](https://docs.docker.com/guides/claude-code-model-runner/)
* [Get started with Docker Sandboxes](https://docs.docker.com/ai/sandboxes/get-started/)
* [Claude Code in Docker Sandboxes](https://docs.docker.com/ai/sandboxes/agents/claude-code/)
* [Docker Model Runner overview](https://docs.docker.com/ai/model-runner/)
* [Docker Model Runner API reference](https://docs.docker.com/ai/model-runner/api-reference/)

----
url: https://docs.docker.com/guides/text-summarization/
----

[Build a text summarization app](https://docs.docker.com/guides/text-summarization/)

This guide shows how to containerize text summarization models with Docker.

Python AI

20 minutes

[« Back to all guides](/guides/)

# Build a text summarization app

***

Table of contents

***

## [Overview](#overview)

In this guide, you'll learn how to build and run a text summarization application. You'll build the application using Python with the Bert Extractive Summarizer, and then set up the environment and run the application using Docker.

The sample text summarization application uses the Bert Extractive Summarizer. This tool utilizes the HuggingFace Pytorch transformers library to run extractive summarizations. This works by first embedding the sentences, then running a clustering algorithm, finding the sentences that are closest to the cluster's centroids.

## [Prerequisites](#prerequisites)

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/). Docker adds new features regularly and some parts of this guide may work only with the latest version of Docker Desktop.
* You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## [Get the sample application](#get-the-sample-application)

1. Open a terminal, and clone the sample application's repository using the following command.

   ```console
   $ git clone https://github.com/harsh4870/Docker-NLP.git
   ```

2. Verify that you cloned the repository.

   You should see the following files in your `Docker-NLP` directory.

   ```text
   01_sentiment_analysis.py
   02_name_entity_recognition.py
   03_text_classification.py
   04_text_summarization.py
   05_language_translation.py
   entrypoint.sh
   requirements.txt
   Dockerfile
   README.md
   ```

## [Explore the application code](#explore-the-application-code)

The source code for the text summarization application is in the `Docker-NLP/04_text_summarization.py` file. Open `04_text_summarization.py` in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.

   ```python
   from summarizer import Summarizer
   ```

   This line of code imports the `Summarizer` class from the `summarizer` package, essential for your text summarization application. The summarizer module implements the Bert Extractive Summarizer, leveraging the HuggingFace Pytorch transformers library, renowned in the NLP (Natural Language Processing) domain. This library offers access to pre-trained models like BERT, which revolutionized language understanding tasks, including text summarization.

   The BERT model, or Bidirectional Encoder Representations from Transformers, excels in understanding context in language, using a mechanism known as "attention" to determine the significance of words in a sentence. For summarization, the model embeds sentences and then uses a clustering algorithm to identify key sentences, those closest to the centroids of these clusters, effectively capturing the main ideas of the text.

2. Specify the main execution block.

   ```python
   if __name__ == "__main__":
   ```

   This Python idiom ensures that the following code block runs only if this script is the main program. It provides flexibility, allowing the script to function both as a standalone program and as an imported module.

3. Create an infinite loop for continuous input.

   ```python
      while True:
         input_text = input("Enter the text for summarization (type 'exit' to end): ")

         if input_text.lower() == 'exit':
            print("Exiting...")
            break
   ```

   An infinite loop continuously prompts you for text input, ensuring interactivity. The loop breaks when you type `exit`, allowing you to control the application flow effectively.

4. Create an instance of Summarizer.

   ```python
         bert_model = Summarizer()
   ```

   Here, you create an instance of the Summarizer class named `bert_model`. This instance is now ready to perform the summarization task using the BERT model, simplifying the complex processes of embedding sentences and clustering into an accessible interface.

5. Generate and print a summary.

   ```python
   summary = bert_model(input_text)
   print(summary)
   ```

   Your input text is processed by the bert\_model instance, which then returns a summarized version. This demonstrates the power of Python's high-level libraries in enabling complex operations with minimal code.

6. Create `requirements.txt`. The sample application already contains the `requirements.txt` file to specify the necessary modules that the application imports. Open `requirements.txt` in a code or text editor to explore its contents.

   ```text
   ...

   # 04 text_summarization
   bert-extractive-summarizer==0.10.1

   ...

   torch==2.1.2
   ```

   The `bert-extractive-summarizer` and `torch` modules are required for the text summarization application. The summarizer module generates a summary of the input text. This requires PyTorch because the underlying BERT model, which is used for generating the summary, is implemented in PyTorch.

## [Explore the application environment](#explore-the-application-environment)

You'll use Docker to run the application in a container. Docker lets you containerize the application, providing a consistent and isolated environment for running it. This means the application will operate as intended within its Docker container, regardless of the underlying system differences.

To run the application in a container, a Dockerfile is required. A Dockerfile is a text document that contains all the commands you would call on the command line to assemble an image. An image is a read-only template with instructions for creating a Docker container.

The sample application already contains a `Dockerfile`. Open the `Dockerfile` in a code or text editor to explore its contents.

The following steps explain each part of the `Dockerfile`. For more details, see the [Dockerfile reference](/reference/dockerfile/).

1. Specify the base image.

   ```dockerfile
   FROM python:3.8-slim
   ```

   This command sets the foundation for the build. `python:3.8-slim` is a lightweight version of the Python 3.8 image, optimized for size and speed. Using this slim image reduces the overall size of your Docker image, leading to quicker downloads and less surface area for security vulnerabilities. This is particularly useful for a Python-based application where you might not need the full standard Python image.

2. Set the working directory.

   ```dockerfile
   WORKDIR /app
   ```

   `WORKDIR` sets the current working directory within the Docker image. By setting it to `/app`, you ensure that all subsequent commands in the Dockerfile (like `COPY` and `RUN`) are executed in this directory. This also helps in organizing your Docker image, as all application-related files are contained in a specific directory.

3. Copy the requirements file into the image.

   ```dockerfile
   COPY requirements.txt /app
   ```

   The `COPY` command transfers the `requirements.txt` file from your local machine into the Docker image. This file lists all Python dependencies required by the application. Copying it into the container lets the next command (`RUN pip install`) to install these dependencies inside the image environment.

4. Install the Python dependencies in the image.

   ```dockerfile
   RUN pip install --no-cache-dir -r requirements.txt
   ```

   This line uses `pip`, Python's package installer, to install the packages listed in `requirements.txt`. The `--no-cache-dir` option disables the cache, which reduces the size of the Docker image by not storing the unnecessary cache data.

5. Run additional commands.

   ```dockerfile
   RUN python -m spacy download en_core_web_sm
   ```

   This step is specific to NLP applications that require the spaCy library. It downloads the `en_core_web_sm` model, which is a small English language model for spaCy. While not needed for this app, it's included for compatibility with other NLP applications that might use this Dockerfile.

6. Copy the application code into the image.

   ```dockerfile
   COPY *.py /app
   COPY entrypoint.sh /app
   ```

   These commands copy your Python scripts and the `entrypoint.sh` script into the image's `/app` directory. This is crucial because the container needs these scripts to run the application. The `entrypoint.sh` script is particularly important as it dictates how the application starts inside the container.

7. Set permissions for the `entrypoint.sh` script.

   ```dockerfile
   RUN chmod +x /app/entrypoint.sh
   ```

   This command modifies the file permissions of `entrypoint.sh`, making it executable. This step is necessary to ensure that the Docker container can run this script to start the application.

8. Set the entry point.

   ```dockerfile
   ENTRYPOINT ["/app/entrypoint.sh"]
   ```

   The `ENTRYPOINT` instruction configures the container to run `entrypoint.sh` as its default executable. This means that when the container starts, it automatically executes the script.

   You can explore the `entrypoint.sh` script by opening it in a code or text editor. As the sample contains several applications, the script lets you specify which application to run when the container starts.

## [Run the application](#run-the-application)

To run the application using Docker:

1. Build the image.

   In a terminal, run the following command inside the directory of where the `Dockerfile` is located.

   ```console
   $ docker build -t basic-nlp .
   ```

   ```console
   $ docker run -it basic-nlp 04_text_summarization.py
   ```

   The following is a break down of the command:

   * `docker run`: This is the primary command used to run a new container from a Docker image.

   * `-it`: This is a combination of two options:

     * `-i` or `--interactive`: This keeps the standard input (STDIN) open even if not attached. It lets the container remain running in the foreground and be interactive.
     * `-t` or `--tty`: This allocates a pseudo-TTY, essentially simulating a terminal, like a command prompt or a shell. It's what lets you interact with the application inside the container.

   * `basic-nlp`: This specifies the name of the Docker image to use for creating the container. In this case, it's the image named `basic-nlp` that you created with the `docker build` command.

   * `04_text_summarization.py`: This is the script you want to run inside the Docker container. It gets passed to the `entrypoint.sh` script, which runs it when the container starts.

   For more details, see the [docker run CLI reference](/reference/cli/docker/container/run/).

   > Note
   >
   > For Windows users, you may get an error when running the container. Verify that the line endings in the `entrypoint.sh` are `LF` (`\n`) and not `CRLF` (`\r\n`), then rebuild the image. For more details, see \[Avoid unexpected syntax errors, use Unix style line endings for files in containers]\(/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers).

   You will see the following in your console after the container starts.

   ```console
   Enter the text for summarization (type 'exit' to end):
   ```

3. Test the application.

   Enter some text to get the text summarization.

   ```console
   Enter the text for summarization (type 'exit' to end): Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making. AI technologies can be classified into two main types: narrow or weak AI, which is designed for a particular task, and general or strong AI, which possesses the ability to understand, learn, and apply knowledge across various domains. One of the most popular approaches in AI is machine learning, where algorithms are trained on large datasets to recognize patterns and make predictions.

   Artificial intelligence (AI) is a branch of computer science that aims to create machines capable of intelligent behavior. These machines are designed to mimic human cognitive functions such as learning, problem-solving, and decision-making.
   ```

## [Summary](#summary)

In this guide, you learned how to build and run a text summarization application. You learned how to build the application using Python with Bert Extractive Summarizer, and then set up the environment and run the application using Docker.

Related information:

* [Docker CLI reference](/reference/cli/docker/)
* [Dockerfile reference](/reference/dockerfile/)
* [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer)
* [PyTorch](https://pytorch.org/)
* [Python documentation](https://docs.python.org/3/)

## [Next steps](#next-steps)

Explore more [natural language processing guides](https://docs.docker.com/guides/).

----
url: https://docs.docker.com/reference/cli/docker/mcp/gateway/run/
----

# docker mcp gateway run

***

| Description | Run the gateway          |
| ----------- | ------------------------ |
| Usage       | `docker mcp gateway run` |

## [Description](#description)

Run the gateway

## [Options](#options)

| Option                      | Default          | Description                                                                                                                                    |
| --------------------------- | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| `--additional-catalog`      |                  | Additional catalog paths to append to the default catalogs                                                                                     |
| `--additional-config`       |                  | Additional config paths to merge with the default config.yaml                                                                                  |
| `--additional-registry`     |                  | Additional registry paths to merge with the default registry.yaml                                                                              |
| `--additional-tools-config` |                  | Additional tools paths to merge with the default tools.yaml                                                                                    |
| `--block-network`           |                  | Block tools from accessing forbidden network resources                                                                                         |
| `--block-secrets`           | `true`           | Block secrets from being/received sent to/from tools                                                                                           |
| `--catalog`                 |                  | Paths to docker catalogs (absolute or relative to \~/.docker/mcp/catalogs/)                                                                    |
| `--config`                  |                  | Paths to the config files (absolute or relative to \~/.docker/mcp/)                                                                            |
| `--cpus`                    | `1`              | CPUs allocated to each MCP Server (default is 1)                                                                                               |
| `--debug-dns`               |                  | Debug DNS resolution                                                                                                                           |
| `--dry-run`                 |                  | Start the gateway but do not listen for connections (useful for testing the configuration)                                                     |
| `--enable-all-servers`      |                  | Enable all servers in the catalog (instead of using individual --servers options)                                                              |
| `--interceptor`             |                  | List of interceptors to use (format: when:type:path, e.g. 'before:exec:/bin/path')                                                             |
| `--log-calls`               | `true`           | Log calls to the tools                                                                                                                         |
| `--long-lived`              |                  | Containers are long-lived and will not be removed until the gateway is stopped, useful for stateful servers                                    |
| `--mcp-registry`            |                  | MCP registry URLs to fetch servers from (can be repeated)                                                                                      |
| `--memory`                  | `2Gb`            | Memory allocated to each MCP Server (default is 2Gb)                                                                                           |
| `--oci-ref`                 |                  | OCI image references to use                                                                                                                    |
| `--port`                    |                  | TCP port to listen on (default is to listen on stdio)                                                                                          |
| `--profile`                 |                  | Profile ID to use (mutually exclusive with --servers and --enable-all-servers)                                                                 |
| `--registry`                |                  | Paths to the registry files (absolute or relative to \~/.docker/mcp/)                                                                          |
| `--secrets`                 | `docker-desktop` | Colon separated paths to search for secrets. Can be `docker-desktop` or a path to a .env file (default to using Docker Desktop's secrets API)  |
| `--servers`                 |                  | Names of the servers to enable (if non empty, ignore --registry flag)                                                                          |
| `--static`                  |                  | Enable static mode (aka pre-started servers)                                                                                                   |
| `--tools`                   |                  | List of tools to enable                                                                                                                        |
| `--tools-config`            |                  | Paths to the tools files (absolute or relative to \~/.docker/mcp/)                                                                             |
| `--transport`               | `stdio`          | stdio, sse or streaming. Uses MCP\_GATEWAY\_AUTH\_TOKEN environment variable for localhost authentication to prevent dns rebinding attacks.    |
| `--verbose`                 |                  | Verbose output                                                                                                                                 |
| `--verify-signatures`       |                  | Verify signatures of the server images                                                                                                         |
| `--watch`                   | `true`           | Watch for changes and reconfigure the gateway                                                                                                  |

----
url: https://docs.docker.com/build/cache/backends/s3/
----

# Amazon S3 cache

***

Table of contents

***

Availability: Experimental

The `s3` cache storage uploads your resulting build cache to [Amazon S3 file storage service](https://aws.amazon.com/s3/) or other S3-compatible services, such as [MinIO](https://min.io/).

This cache storage backend is not supported with the default `docker` driver. To use this feature, create a new builder using a different driver. See [Build drivers](https://docs.docker.com/build/builders/drivers/) for more information.

## [Synopsis](#synopsis)

```console
$ docker buildx build --push -t <user>/<image> \
  --cache-to type=s3,region=<region>,bucket=<bucket>,name=<cache-image>[,parameters...] \
  --cache-from type=s3,region=<region>,bucket=<bucket>,name=<cache-image> .
```

The following table describes the available CSV parameters that you can pass to `--cache-to` and `--cache-from`.

| Name                 | Option                  | Type        | Default      | Description                                                                                         |
| -------------------- | ----------------------- | ----------- | ------------ | --------------------------------------------------------------------------------------------------- |
| `region`             | `cache-to`,`cache-from` | String      |              | Required. Geographic location.                                                                      |
| `bucket`             | `cache-to`,`cache-from` | String      |              | Required. Name of the S3 bucket.                                                                    |
| `name`               | `cache-to`,`cache-from` | String      | `buildkit`   | Name of the cache image.                                                                            |
| `endpoint_url`       | `cache-to`,`cache-from` | String      |              | Endpoint of the S3 bucket.                                                                          |
| `prefix`             | `cache-to`,`cache-from` | String      |              | Prefix to prepend to all filenames.                                                                 |
| `blobs_prefix`       | `cache-to`,`cache-from` | String      | `blobs/`     | Prefix to prepend to blob filenames.                                                                |
| `upload_parallelism` | `cache-to`              | Integer     | `4`          | Number of parallel layer uploads.                                                                   |
| `touch_refresh`      | `cache-to`              | Time        | `24h`        | Interval for updating the timestamp of unchanged cache layers.                                      |
| `manifests_prefix`   | `cache-to`,`cache-from` | String      | `manifests/` | Prefix to prepend to manifest filenames.                                                            |
| `use_path_style`     | `cache-to`,`cache-from` | Boolean     | `false`      | When `true`, uses `bucket` in the URL instead of hostname.                                          |
| `access_key_id`      | `cache-to`,`cache-from` | String      |              | See [authentication](#authentication).                                                              |
| `secret_access_key`  | `cache-to`,`cache-from` | String      |              | See [authentication](#authentication).                                                              |
| `session_token`      | `cache-to`,`cache-from` | String      |              | See [authentication](#authentication).                                                              |
| `mode`               | `cache-to`              | `min`,`max` | `min`        | Cache layers to export, see [cache mode](https://docs.docker.com/build/cache/backends/#cache-mode). |
| `ignore-error`       | `cache-to`              | Boolean     | `false`      | Ignore errors caused by failed cache exports.                                                       |

## [Authentication](#authentication)

Buildx can reuse existing AWS credentials, configured either using a credentials file or environment variables, for pushing and pulling cache to S3. Alternatively, you can use the `access_key_id`, `secret_access_key`, and `session_token` attributes to specify credentials directly on the CLI.

Refer to [AWS Go SDK, Specifying Credentials](https://docs.aws.amazon.com/sdk-for-go/v2/developer-guide/configure-gosdk.html#specifying-credentials) for details about authentication using environment variables and credentials file.

## [Further reading](#further-reading)

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `s3` cache backend, see the [BuildKit README](https://github.com/moby/buildkit#s3-cache-experimental).

----
url: https://docs.docker.com/reference/cli/sbx/template/
----

# sbx template

| Description | Manage sandbox templates |
| ----------- | ------------------------ |
| Usage       | `sbx template COMMAND`   |

## [Description](#description)

Manage sandbox templates.

Templates are saved snapshots of sandboxes that can be reused to create new sandboxes with: sbx run -t TAG AGENT \[WORKSPACE]

## [Commands](#commands)

| Command                                                                         | Description                                            |
| ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [`sbx template load`](https://docs.docker.com/reference/cli/sbx/template/load/) | Load an image from a tar file into the sandbox runtime |
| [`sbx template ls`](https://docs.docker.com/reference/cli/sbx/template/ls/)     | List template images                                   |
| [`sbx template rm`](https://docs.docker.com/reference/cli/sbx/template/rm/)     | Remove a template image                                |
| [`sbx template save`](https://docs.docker.com/reference/cli/sbx/template/save/) | Save a snapshot of the sandbox as a template           |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/engine/network/drivers/
----

# Network drivers

***

Table of contents

***

Docker's networking subsystem is pluggable, using drivers. Several drivers exist by default, and provide core networking functionality:

* `bridge`: The default network driver. If you don't specify a driver, this is the type of network you are creating. Bridge networks are commonly used when your application runs in a container that needs to communicate with other containers on the same host. See [Bridge network driver](https://docs.docker.com/engine/network/drivers/bridge/).

* `host`: Remove network isolation between the container and the Docker host, and use the host's networking directly. See [Host network driver](https://docs.docker.com/engine/network/drivers/host/).

* `overlay`: Overlay networks connect multiple Docker daemons together and enable Swarm services and containers to communicate across nodes. This strategy removes the need to do OS-level routing. See [Overlay network driver](https://docs.docker.com/engine/network/drivers/overlay/).

* `ipvlan`: IPvlan networks give users total control over both IPv4 and IPv6 addressing. The VLAN driver builds on top of that in giving operators complete control of layer 2 VLAN tagging and even IPvlan L3 routing for users interested in underlay network integration. See [IPvlan network driver](https://docs.docker.com/engine/network/drivers/ipvlan/).

* `macvlan`: Macvlan networks allow you to assign a MAC address to a container, making it appear as a physical device on your network. The Docker daemon routes traffic to containers by their MAC addresses. Using the `macvlan` driver is sometimes the best choice when dealing with legacy applications that expect to be directly connected to the physical network, rather than routed through the Docker host's network stack. See [Macvlan network driver](https://docs.docker.com/engine/network/drivers/macvlan/).

* `none`: Completely isolate a container from the host and other containers. `none` is not available for Swarm services. See [None network driver](https://docs.docker.com/engine/network/drivers/none/).

* [Network plugins](/engine/extend/plugins_network/): You can install and use third-party network plugins with Docker.

### [Network driver summary](#network-driver-summary)

* The default bridge network is good for running containers that don't require special networking capabilities.
* User-defined bridge networks enable containers on the same Docker host to communicate with each other. A user-defined network typically defines an isolated network for multiple containers belonging to a common project or component.
* Host network shares the host's network with the container. When you use this driver, the container's network isn't isolated from the host.
* Overlay networks are best when you need containers running on different Docker hosts to communicate, or when multiple applications work together using Swarm services.
* Macvlan networks are best when you are migrating from a VM setup or need your containers to look like physical hosts on your network, each with a unique MAC address.
* IPvlan is similar to Macvlan, but doesn't assign unique MAC addresses to containers. Consider using IPvlan when there's a restriction on the number of MAC addresses that can be assigned to a network interface or port.
* Third-party network plugins allow you to integrate Docker with specialized network stacks.

## [Next steps](#next-steps)

Each driver page includes detailed explanations, configuration options, and hands-on usage examples to help you work with that driver effectively.

----
url: https://docs.docker.com/engine/network/drivers/none/
----

# None network driver

***

Table of contents

***

If you want to completely isolate the networking stack of a container, you can use the `--network none` flag when starting the container. Within the container, only the loopback device is created.

The following example shows the output of `ip link show` in an `alpine` container using the `none` network driver.

```console
$ docker run --rm --network none alpine:latest ip link show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
```

No IPv6 loopback address is configured for containers using the `none` driver.

```console
$ docker run --rm --network none --name no-net-alpine alpine:latest ip addr show
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
```

## [Next steps](#next-steps)

* Learn about [networking from the container's point of view](https://docs.docker.com/engine/network/)
* Learn about [host networking](https://docs.docker.com/engine/network/drivers/host/)
* Learn about [bridge networks](https://docs.docker.com/engine/network/drivers/bridge/)
* Learn about [overlay networks](https://docs.docker.com/engine/network/drivers/overlay/)
* Learn about [Macvlan networks](https://docs.docker.com/engine/network/drivers/macvlan/)

----
url: https://docs.docker.com/compose/how-tos/dependent-images/
----

# Build dependent images

***

Table of contents

***

Requires: Docker Compose [2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0) and later

To reduce push/pull time and image weight, a common practice for Compose applications is to have services share base layers as much as possible. You typically select the same operating system base image for all services. But you can also get one step further by sharing image layers when your images share the same system packages. The challenge to address is then to avoid repeating the exact same Dockerfile instruction in all services.

For illustration, this page assumes you want all your services to be built with an `alpine` base image and install the system package `openssl`.

## [Multi-stage Dockerfile](#multi-stage-dockerfile)

The recommended approach is to group the shared declaration in a single Dockerfile, and use multi-stage features so that service images are built from this shared declaration.

Dockerfile:

```dockerfile
FROM alpine as base
RUN /bin/sh -c apk add --update --no-cache openssl

FROM base as service_a
# build service a
...

FROM base as service_b
# build service b
...
```

Compose file:

```yaml
services:
  a:
     build:
       target: service_a
  b:
     build:
       target: service_b
```

## [Use another service's image as the base image](#use-another-services-image-as-the-base-image)

A popular pattern is to reuse a service image as a base image in another service. As Compose does not parse the Dockerfile, it can't automatically detect this dependency between services to correctly order the build execution.

a.Dockerfile:

```dockerfile
FROM alpine
RUN /bin/sh -c apk add --update --no-cache openssl
```

b.Dockerfile:

```dockerfile
FROM service_a
# build service b
```

Compose file:

```yaml
services:
  a:
     image: service_a 
     build:
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
```

Legacy Docker Compose v1 used to build images sequentially, which made this pattern usable out of the box. Compose v2 uses BuildKit to optimise builds and build images in parallel and requires an explicit declaration.

The recommended approach is to declare the dependent base image as an additional build context:

Compose file:

```yaml
services:
  a:
     image: service_a
     build: 
       dockerfile: a.Dockerfile
  b:
     image: service_b
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM service_a` will be resolved as a dependency on service "a" which has to be built first
         service_a: "service:a"
```

With the `additional_contexts` attribute, you can refer to an image built by another service without needing to explicitly name it:

b.Dockerfile:

```dockerfile

FROM base_image  
# `base_image` doesn't resolve to an actual image. This is used to point to a named additional context

# build service b
```

Compose file:

```yaml
services:
  a:
     build: 
       dockerfile: a.Dockerfile
       # built image will be tagged <project_name>_a
  b:
     build:
       dockerfile: b.Dockerfile
       additional_contexts:
         # `FROM base_image` will be resolved as a dependency on service "a" which has to be built first
         base_image: "service:a"
```

## [Build with Bake](#build-with-bake)

Using [Bake](https://docs.docker.com/build/bake/) let you pass the complete build definition for all services and to orchestrate build execution in the most efficient way.

To enable this feature, run Compose with the `COMPOSE_BAKE=true` variable set in your environment.

```console
$ COMPOSE_BAKE=true docker compose build
[+] Building 0.0s (0/1)                                                         
 => [internal] load local bake definitions                                 0.0s
...
[+] Building 2/2 manifest list sha256:4bd2e88a262a02ddef525c381a5bdb08c83  0.0s
 ✔ service_b  Built                                                        0.7s 
 ✔ service_a  Built    
```

Bake can also be selected as the default builder by editing your `$HOME/.docker/config.json` config file:

```json
{
  ...
  "plugins": {
    "compose": {
      "build": "bake"
    }
  }
  ...
}
```

## [Additional resources](#additional-resources)

* [Docker Compose build reference](/reference/cli/docker/compose/build/)
* [Learn about multi-stage Dockerfiles](https://docs.docker.com/build/building/multi-stage/)

----
url: https://docs.docker.com/engine/swarm/
----

# Swarm mode

***

Table of contents

***

> Note
>
> Swarm mode is an advanced feature for managing a cluster of Docker daemons.
>
> Use Swarm mode if you intend to use Swarm as a production runtime environment.
>
> If you're not planning on deploying with Swarm, use [Docker Compose](/compose/) instead. If you're developing for a Kubernetes deployment, consider using the [integrated Kubernetes feature](https://docs.docker.com/desktop/use-desktop/kubernetes/) in Docker Desktop.

Current versions of Docker include Swarm mode for natively managing a cluster of Docker Engines called a swarm. Use the Docker CLI to create a swarm, deploy application services to a swarm, and manage swarm behavior.

Docker Swarm mode is built into the Docker Engine. Do not confuse Docker Swarm mode with [Docker Classic Swarm](https://github.com/docker/classicswarm) which is no longer actively developed.

## [Feature highlights](#feature-highlights)

### [Cluster management integrated with Docker Engine](#cluster-management-integrated-with-docker-engine)

Use the Docker Engine CLI to create a swarm of Docker Engines where you can deploy application services. You don't need additional orchestration software to create or manage a swarm.

### [Decentralized design](#decentralized-design)

Instead of handling differentiation between node roles at deployment time, the Docker Engine handles any specialization at runtime. You can deploy both kinds of nodes, managers and workers, using the Docker Engine. This means you can build an entire swarm from a single disk image.

### [Declarative service model](#declarative-service-model)

Docker Engine uses a declarative approach to let you define the desired state of the various services in your application stack. For example, you might describe an application comprised of a web front end service with message queueing services and a database backend.

### [Scaling](#scaling)

For each service, you can declare the number of tasks you want to run. When you scale up or down, the swarm manager automatically adapts by adding or removing tasks to maintain the desired state.

### [Desired state reconciliation](#desired-state-reconciliation)

The swarm manager node constantly monitors the cluster state and reconciles any differences between the actual state and your expressed desired state. For example, if you set up a service to run 10 replicas of a container, and a worker machine hosting two of those replicas crashes, the manager creates two new replicas to replace the replicas that crashed. The swarm manager assigns the new replicas to workers that are running and available.

### [Multi-host networking](#multi-host-networking)

You can specify an overlay network for your services. The swarm manager automatically assigns addresses to the containers on the overlay network when it initializes or updates the application.

### [Service discovery](#service-discovery)

Swarm manager nodes assign each service in the swarm a unique DNS name and load balance running containers. You can query every container running in the swarm through a DNS server embedded in the swarm.

### [Load balancing](#load-balancing)

You can expose the ports for services to an external load balancer. Internally, the swarm lets you specify how to distribute service containers between nodes.

### [Secure by default](#secure-by-default)

Each node in the swarm enforces TLS mutual authentication and encryption to secure communications between itself and all other nodes. You have the option to use self-signed root certificates or certificates from a custom root CA.

### [Rolling updates](#rolling-updates)

At rollout time you can apply service updates to nodes incrementally. The swarm manager lets you control the delay between service deployment to different sets of nodes. If anything goes wrong, you can roll back to a previous version of the service.

## [What's next?](#whats-next)

* Learn Swarm mode [key concepts](https://docs.docker.com/engine/swarm/key-concepts/).

* Get started with the [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/).

* Explore Swarm mode CLI commands

  * [swarm init](/reference/cli/docker/swarm/init/)
  * [swarm join](/reference/cli/docker/swarm/join/)
  * [service create](/reference/cli/docker/service/create/)
  * [service inspect](/reference/cli/docker/service/inspect/)
  * [service ls](/reference/cli/docker/service/ls/)
  * [service rm](/reference/cli/docker/service/rm/)
  * [service scale](/reference/cli/docker/service/scale/)
  * [service ps](/reference/cli/docker/service/ps/)
  * [service update](/reference/cli/docker/service/update/)

----
url: https://docs.docker.com/reference/api/registry/latest.yaml
----

openapi: 3.0.3
info:
 title: Supported registry API for Docker Hub
 description: \|
 Docker Hub is an OCI-compliant registry, which means it adheres to the open
 standards defined by the Open Container Initiative (OCI) for distributing
 container images. This ensures compatibility with a wide range of tools and
 platforms in the container ecosystem.

 This reference documents the Docker Hub-supported subset of the Registry HTTP API V2.
 It focuses on pulling, pushing, and deleting images. It does not cover the full OCI Distribution Specification.

 For the complete OCI specification, see \[OCI Distribution Specification\](https://github.com/opencontainers/distribution-spec).
servers:
 \- description: Docker Hub registry API
 x-audience: public
 url: https://registry-1.docker.io

tags:
 \- name: overview
 x-displayName: Overview
 description: \|
 All endpoints in this API are prefixed by the version and repository name, for example:

 \`\`\`
 /v2//
 \`\`\`

 This format provides structured access control and URI-based scoping of image operations.

 For example, to interact with the \`library/ubuntu\` repository, use:

 \`\`\`
 /v2/library/ubuntu/
 \`\`\`

 Repository names must meet these requirements:
 1\. Consist of path components matching \`\[a-z0-9\]+(?:\[.\_-\]\[a-z0-9\]+)\*\`
 2\. If more than one component, they must be separated by \`/\`
 3\. Full repository name must be fewer than 256 characters

 \- name: authentication
 x-displayName: Authentication
 description: \|
 Specifies registry authentication.
 externalDocs:
 description: Detailed authentication workflow and token usage
 url: https://docs.docker.com/reference/api/registry/auth/

 \- name: Manifests
 x-displayName: Manifests
 description: \|
 Image manifests are JSON documents that describe an image: its configuration blob, the digests of each layer blob, and metadata such as media‑types and annotations.

 \- name: Blobs
 x-displayName: Blobs
 description: \|
 Blobs are the binary objects referenced from manifests:
 the config JSON and one or more compressed layer tarballs.

 \- name: pull
 x-displayName: Pulling Images
 description: \|
 Pulling an image involves retrieving the manifest and downloading each of the image's layer blobs. This section outlines the general steps followed by a working example.

 1\. \[Get a bearer token for the repository\](https://docs.docker.com/reference/api/registry/auth/).
 2\. \[Get the image manifest\](#operation/GetImageManifest).
 3\. If the response in the previous step is a multi-architecture manifest list, you must do the following:
 \- Parse the \`manifests\[\]\` array to locate the digest for your target platform (e.g., \`linux/amd64\`).
 \- \[Get the image manifest\](#operation/GetImageManifest) using the located digest.
 4\. \[Check if the blob exists\](#operation/CheckBlobExists) before downloading. The client should send a \`HEAD\` request for each layer digest.
 5\. \[Download each layer blob\](#operation/GetBlob) using the digest obtained from the manifest. The client should send a \`GET\` request for each layer digest.

 The following bash script example pulls \`library/ubuntu:latest\` from Docker Hub.

 \`\`\`bash
 #!/bin/bash

 # Step 1: Get a bearer token
 TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/ubuntu:pull" \| jq -r .token)

 # Step 2: Get the image manifest. In this example, an image manifest list is returned.
 curl -s -H "Authorization: Bearer $TOKEN" \
 -H "Accept: application/vnd.docker.distribution.manifest.list.v2+json" \
 https://registry-1.docker.io/v2/library/ubuntu/manifests/latest \
 -o manifest-list.json

 # Step 3a: Parse the \`manifests\[\]\` array to locate the digest for your target platform (e.g., \`linux/amd64\`).
 IMAGE\_MANIFEST\_DIGEST=$(jq -r '.manifests\[\] \| select(.platform.architecture == "amd64" and .platform.os == "linux") \| .digest' manifest-list.json)

 # Step 3b: Get the platform-specific image manifest
 curl -s -H "Authorization: Bearer $TOKEN" \
 -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
 https://registry-1.docker.io/v2/library/ubuntu/manifests/$IMAGE\_MANIFEST\_DIGEST \
 -o manifest.json

 # Step 4: Send a HEAD request to check if the layer blob exists
 DIGEST=$(jq -r '.layers\[0\].digest' manifest.json)
 curl -I -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/$DIGEST

 # Step 5: Download the layer blob
 curl -L -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/$DIGEST
 \`\`\`

 This example pulls the manifest and the first layer for the \`ubuntu:latest\` image on the \`linux/amd64\` platform. Repeat steps 4 and 5 for each digest in the \`.layers\[\]\` array in the manifest.

 \- name: push
 x-displayName: Pushing Images
 description: \|
 Pushing an image involves uploading any image blobs (such as the config or layers), and then uploading the manifest that references those blobs.

 This section outlines the basic steps to push an image using the registry API.

 1\. \[Get a bearer token for the repository\](https://docs.docker.com/reference/api/registry/auth/)

 2\. \[Check if the blob exists\](#operation/CheckBlobExists) using a \`HEAD\` request for each blob digest.

 3\. If the blob does not exist, \[upload the blob\](#operation/CompleteBlobUpload) using a monolithic \`PUT\` request:
 \- First, \[initiate the upload\](#operation/InitiateBlobUpload) with \`POST\`.
 \- Then \[upload and complete\](#operation/CompleteBlobUpload) with \`PUT\`.

 \*\*Note\*\*: Alternatively, you can upload the blob in multiple chunks by using \`PATCH\` requests to send each chunk, followed by a final \`PUT\` request to complete the upload. This is known as a \[chunked upload\](#operation/UploadBlobChunk) and is useful for large blobs or when resuming interrupted uploads.


 4\. \[Upload the image manifest\](#operation/PutImageManifest) using a \`PUT\` request to associate the config and layers.

 The following bash script example pushes a dummy config blob and manifest to \`yourusername/helloworld:latest\` on Docker Hub. You can replace \`yourusername\` with your Docker Hub username and \`dckr\_pat\` with your Docker Hub personal access token.

 \`\`\`bash
 #!/bin/bash

 USERNAME=yourusername
 PASSWORD=dckr\_pat
 REPO=yourusername/helloworld
 TAG=latest
 CONFIG=config.json
 MIME\_TYPE=application/vnd.docker.container.image.v1+json

 # Step 1: Get a bearer token
 TOKEN=$(curl -s -u "$USERNAME:$PASSWORD" \
 "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:push,pull" \
 \| jq -r .token)

 # Create a dummy config blob and compute its digest
 echo '{"architecture":"amd64","os":"linux","config":{},"rootfs":{"type":"layers","diff\_ids":\[\]}}' > $CONFIG
 DIGEST="sha256:$(sha256sum $CONFIG \| awk '{print $1}')"

 # Step 2: Check if the blob exists
 STATUS=$(curl -s -o /dev/null -w "%{http\_code}" -I \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/$REPO/blobs/$DIGEST)

 if \[ "$STATUS" != "200" \]; then
 # Step 3: Upload blob using monolithic upload
 LOCATION=$(curl -sI -X POST \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/$REPO/blobs/uploads/ \
 \| grep -i Location \| tr -d '\\r' \| awk '{print $2}')

 curl -s -X PUT "$LOCATION&digest=$DIGEST" \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/octet-stream" \
 --data-binary @$CONFIG
 fi

 # Step 4: Upload the manifest that references the config blob
 MANIFEST=$(cat < \*\*Note\*\*
 >
 \> Manifest deletion operations may experience latency and could return a \`500 Internal Server Error\` during deletion. The system automatically retries the deletion in the background, so the manifest will eventually be removed. You do not need to manually retry the request.

 This section outlines the basic steps to delete an image using the registry API.

 1\. \[Get a bearer token for the repository\](https://docs.docker.com/reference/api/registry/auth/).
 2\. \[Get the manifest\](#operation/GetImageManifest) using the image's tag.
 3\. Retrieve the \`Docker-Content-Digest\` header from the manifest response. This digest uniquely identifies the manifest.
 4\. \[Delete the manifest\](#operation/DeleteImageManifest) using a \`DELETE\` request and the digest.

 The following bash script example deletes the \`latest\` tag from \`yourusername/helloworld\` on Docker Hub. Replace \`yourusername\` with your Docker Hub username and \`dckr\_pat\` with your Docker Hub personal access token.

 \`\`\`bash
 #!/bin/bash

 USERNAME=yourusername
 PASSWORD=dckr\_pat
 REPO=yourusername/helloworld
 TAG=latest

 # Step 1: Get a bearer token
 TOKEN=$(curl -s -u "$USERNAME:$PASSWORD" \
 "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:pull,push,delete" \
 \| jq -r .token)

 # Step 2 and 3: Get the manifest and extract the digest from response headers
 DIGEST=$(curl -sI -H "Authorization: Bearer $TOKEN" \
 -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
 https://registry-1.docker.io/v2/$REPO/manifests/$TAG \
 \| grep -i Docker-Content-Digest \| tr -d '\\r' \| awk '{print $2}')

 echo "Deleting manifest with digest: $DIGEST"

 # Step 4: Delete the manifest by digest
 curl -s -X DELETE \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/$REPO/manifests/$DIGEST

 echo "Deleted image: $REPO@$DIGEST"
 \`\`\`

 This example deletes the manifest for the \`latest\` tag. To fully delete all references to an image, ensure no other tags or referrers point to the same manifest digest.

paths:
 /v2/{name}/manifests/{reference}:
 get:
 tags:
 \- Manifests
 x-displayName: Manifests
 summary: Get image manifest
 operationId: GetImageManifest
 description: \|
 Fetch the manifest identified by \`name\` and \`reference\`, where \`reference\` can be a tag (e.g., \`latest\`) or a digest (e.g., \`sha256:...\`).

 The manifest contains metadata about the image, including configuration and layer digests. It is required for pulling images from the registry.

 This endpoint requires authentication. Use the \`Authorization: Bearer \` header.

 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # GET a manifest (by tag or digest)
 curl -H "Authorization: Bearer $TOKEN" \
 -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
 https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the target repository
 example: library/ubuntu
 schema:
 type: string
 \- name: reference
 in: path
 required: true
 description: Tag or digest of the target manifest
 examples:
 by-tag:
 summary: Tag
 value: latest
 by-digest:
 summary: Digest
 value: sha256:abc123def456...
 schema:
 type: string
 \- name: Authorization
 in: header
 required: true
 description: RFC7235-compliant authorization header (e.g., \`Bearer \`).
 schema:
 type: string
 \- name: Accept
 in: header
 required: false
 description: \|
 Media type(s) the client supports for the manifest.

 The registry supports the following media types:
 \- application/vnd.docker.distribution.manifest.v2+json
 \- application/vnd.docker.distribution.manifest.list.v2+json
 \- application/vnd.oci.image.manifest.v1+json
 \- application/vnd.oci.image.index.v1+json
 schema:
 type: string

 responses:
 "200":
 description: Manifest fetched successfully.
 headers:
 Docker-Content-Digest:
 description: Digest of the returned manifest content.
 schema:
 type: string
 Content-Type:
 description: Media type of the returned manifest.
 schema:
 type: string
 content:
 application/vnd.docker.distribution.manifest.v2+json:
 schema:
 type: object
 required:
 \- schemaVersion
 \- mediaType
 \- config
 \- layers
 properties:
 schemaVersion:
 type: integer
 example: 2
 mediaType:
 type: string
 example: application/vnd.docker.distribution.manifest.v2+json
 config:
 type: object
 properties:
 mediaType:
 type: string
 example: application/vnd.docker.container.image.v1+json
 size:
 type: integer
 example: 7023
 digest:
 type: string
 example: sha256:a3f3e...c1234
 layers:
 type: array
 items:
 type: object
 properties:
 mediaType:
 type: string
 example: application/vnd.docker.image.rootfs.diff.tar.gzip
 size:
 type: integer
 example: 32654
 digest:
 type: string
 example: sha256:bcf2...78901
 examples:
 docker-manifest:
 summary: Docker image manifest (schema v2)
 value:
 {
 "schemaVersion": 2,
 "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
 "config": {
 "mediaType": "application/vnd.docker.container.image.v1+json",
 "size": 7023,
 "digest": "sha256:123456abcdef..."
 },
 "layers": \[\
 {\
 "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",\
 "size": 32654,\
 "digest": "sha256:abcdef123456..."\
 },\
 {\
 "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",\
 "size": 16724,\
 "digest": "sha256:7890abcdef12..."\
 }\
 \]
 }

 "400":
 description: Invalid name or reference.
 "401":
 description: Authentication required.
 "403":
 description: Access denied.
 "404":
 description: Repository or manifest not found.
 "429":
 description: Too many requests.

 put:
 tags:
 \- Manifests
 summary: Put image manifest
 operationId: PutImageManifest
 description: \|
 Upload an image manifest for a given tag or digest. This operation registers a manifest in a repository, allowing it to be pulled using the specified reference.

 This endpoint is typically used after all layer and config blobs have been uploaded to the registry.

 The manifest must conform to the expected schema and media type. For Docker image manifest schema version 2, use:
 \`application/vnd.docker.distribution.manifest.v2+json\`

 Requires authentication via a bearer token with \`push\` scope for the target repository.
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # PUT a manifest (tag = latest)
 curl -X PUT \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/vnd.docker.distribution.manifest.v2+json" \
 --data-binary @manifest.json \
 https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the target Repository
 example: library/ubuntu
 schema:
 type: string
 \- name: reference
 in: path
 required: true
 description: Tag or digest to associate with the uploaded Manifest
 examples:
 by-tag:
 summary: Tag
 value: latest
 by-digest:
 summary: Digest
 value: sha256:abc123def456...
 schema:
 type: string
 \- name: Authorization
 in: header
 required: true
 description: RFC7235-compliant authorization header (e.g., \`Bearer \`).
 schema:
 type: string
 \- name: Content-Type
 in: header
 required: true
 description: Media type of the manifest being uploaded.
 schema:
 type: string
 example: application/vnd.docker.distribution.manifest.v2+json

 requestBody:
 required: true
 content:
 application/vnd.docker.distribution.manifest.v2+json:
 schema:
 type: object
 required:
 \- schemaVersion
 \- mediaType
 \- config
 \- layers
 properties:
 schemaVersion:
 type: integer
 example: 2
 mediaType:
 type: string
 example: application/vnd.docker.distribution.manifest.v2+json
 config:
 type: object
 required:
 \- mediaType
 \- size
 \- digest
 properties:
 mediaType:
 type: string
 example: application/vnd.docker.container.image.v1+json
 size:
 type: integer
 example: 7023
 digest:
 type: string
 example: sha256:123456abcdef...
 layers:
 type: array
 items:
 type: object
 required:
 \- mediaType
 \- size
 \- digest
 properties:
 mediaType:
 type: string
 example: application/vnd.docker.image.rootfs.diff.tar.gzip
 size:
 type: integer
 example: 32654
 digest:
 type: string
 example: sha256:abcdef123456...

 examples:
 sample-manifest:
 summary: Sample Docker image manifest (schema v2)
 value:
 {
 "schemaVersion": 2,
 "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
 "config": {
 "mediaType": "application/vnd.docker.container.image.v1+json",
 "size": 7023,
 "digest": "sha256:123456abcdef..."
 },
 "layers": \[\
 {\
 "mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",\
 "size": 32654,\
 "digest": "sha256:abcdef123456..."\
 }\
 \]
 }

 responses:
 "201":
 description: Manifest created successfully.
 headers:
 Docker-Content-Digest:
 description: Digest of the stored manifest.
 schema:
 type: string
 example: sha256:abcdef123456...
 Location:
 description: Canonical location of the uploaded manifest.
 schema:
 type: string
 example: /v2/library/ubuntu/manifests/latest
 Content-Length:
 description: Always zero.
 schema:
 type: integer
 example: 0
 "400":
 description: Invalid name, reference, or manifest.
 "401":
 description: Authentication required.
 "403":
 description: Access denied.
 "404":
 description: Repository not found.
 "405":
 description: Operation not allowed.
 "429":
 description: Too many requests.
 head:
 tags:
 \- Manifests
 summary: Check if manifest exists
 operationId: HeadImageManifest
 description: \|
 Use this endpoint to verify whether a manifest exists by tag or digest.

 This is a lightweight operation that returns only headers (no body). It is useful for:
 \- Checking for the existence of a specific image version
 \- Determining the digest or size of a manifest before downloading or deleting

 This endpoint requires authentication with pull scope.

 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the Repository
 example: library/ubuntu
 schema:
 type: string
 \- name: reference
 in: path
 required: true
 description: Tag or digest to check
 examples:
 by-tag:
 summary: Tag
 value: latest
 by-digest:
 summary: Digest
 value: sha256:abc123def456...
 schema:
 type: string
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 description: Bearer token for authentication
 \- name: Accept
 in: header
 required: false
 schema:
 type: string
 example: application/vnd.docker.distribution.manifest.v2+json
 description: \|
 Media type of the manifest to check. The response will match one of the accepted types.
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # HEAD /v2/{name}/manifests/{reference}
 curl -I \
 -H "Authorization: Bearer $TOKEN" \
 -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
 https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
 responses:
 "200":
 description: Manifest exists.
 headers:
 Content-Length:
 description: Size of the manifest in bytes
 schema:
 type: integer
 example: 7082
 Docker-Content-Digest:
 description: Digest of the manifest
 schema:
 type: string
 example: sha256:abc123...
 Content-Type:
 description: Media type of the manifest
 schema:
 type: string
 example: application/vnd.docker.distribution.manifest.v2+json
 "404":
 description: Manifest not found.
 "401":
 description: Authentication required.
 "403":
 description: Access denied.
 "429":
 description: Too many requests.
 delete:
 tags:
 \- Manifests
 summary: Delete image manifest
 operationId: DeleteImageManifest
 description: \|
 Delete an image manifest from a repository by digest.

 Only untagged or unreferenced manifests can be deleted. If the manifest is still referenced by a tag or another image, the registry will return \`403 Forbidden\`.

 This operation requires \`delete\` access to the repository.

 \> \*\*Note\*\*
 >
 \> Manifest deletion operations may take some time and could return a \`500 Internal Server Error\`. The system automatically retries the deletion in the background. Manual intervention is not required.
 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the repository
 example: yourusername/helloworld
 schema:
 type: string
 \- name: reference
 in: path
 required: true
 description: Digest of the manifest to delete (e.g., \`sha256:...\`)
 example: sha256:abc123def456...
 schema:
 type: string
 \- name: Authorization
 in: header
 required: true
 description: Bearer token with \`delete\` access
 schema:
 type: string
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # DELETE a manifest by digest
 curl -X DELETE \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/yourusername/helloworld/manifests/sha256:abc123def456...
 responses:
 "202":
 description: Manifest deleted successfully. No content returned.
 "401":
 description: Authentication required.
 "403":
 description: Access denied. The manifest may still be referenced.
 "404":
 description: Manifest or repository not found.
 "405":
 description: Only digest-based deletion is allowed.
 "429":
 description: Too many requests.
 /v2/{name}/blobs/uploads/:
 post:
 tags:
 \- Blobs
 summary: Initiate blob upload or attempt cross-repository blob mount
 operationId: InitiateBlobUpload
 description: \|
 Initiate an upload session for a blob (layer or config) in a repository.

 This is the first step in uploading a blob. It returns a \`Location\` URL where the blob can be uploaded using \`PATCH\` (chunked) or \`PUT\` (monolithic).

 Instead of uploading a blob, a client may attempt to mount a blob from another repository (if it has read access) by including the \`mount\` and \`from\` query parameters.

 If successful, the registry responds with \`201 Created\` and the blob is reused without re-upload.

 If the mount fails, the upload proceeds as usual and returns a \`202 Accepted\`.

 You must authenticate with \`push\` access to the target repository.
 x-codeSamples:
 \- lang: Bash
 label: cURL (Initiate Standard Upload)
 source: \|
 # Initiate a standard blob upload session
 curl -i -X POST \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/

 \- lang: Bash
 label: cURL (Cross-Repository Blob Mount)
 source: \|
 # Attempt a cross-repository blob mount
 curl -i -X POST \
 -H "Authorization: Bearer $TOKEN" \
 "https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/?mount=sha256:abc123def456...&from=library/busybox"

 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the target repository
 example: library/ubuntu
 schema:
 type: string
 \- name: mount
 in: query
 required: false
 description: Digest of the blob to mount from another repository
 schema:
 type: string
 example: sha256:abc123def456...
 \- name: from
 in: query
 required: false
 description: Source repository to mount the blob from
 schema:
 type: string
 example: library/busybox
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 description: Bearer token for authentication with \`push\` scope

 responses:
 "201":
 description: Blob successfully mounted from another repository.
 headers:
 Location:
 description: URL where the mounted blob is accessible
 schema:
 type: string
 example: /v2/library/ubuntu/blobs/sha256:abc123...
 Docker-Content-Digest:
 description: Canonical digest of the mounted blob
 schema:
 type: string
 example: sha256:abc123...
 Content-Length:
 description: Always zero
 schema:
 type: integer
 example: 0
 "202":
 description: Upload initiated successfully (fallback if mount fails).
 headers:
 Location:
 description: Upload location URL for \`PATCH\` or \`PUT\` requests
 schema:
 type: string
 example: /v2/library/ubuntu/blobs/uploads/abc123
 Docker-Upload-UUID:
 description: Server-generated UUID for the upload session
 schema:
 type: string
 example: abc123
 Range:
 description: Current upload byte range (typically \`0-0\` at init)
 schema:
 type: string
 example: 0-0
 Content-Length:
 description: Always zero
 schema:
 type: integer
 example: 0
 "401":
 description: Authentication required.
 "403":
 description: Access denied.
 "404":
 description: Repository not found.
 "429":
 description: Too many requests.
 /v2/{name}/blobs/{digest}:
 head:
 tags:
 \- Blobs
 summary: Check existence of blob
 operationId: CheckBlobExists
 description: \|
 Check whether a blob (layer or config) exists in the registry.

 This is useful before uploading a blob to avoid duplicates.

 If the blob is present, the registry returns a \`200 OK\` response with headers like \`Content-Length\` and \`Docker-Content-Digest\`.

 If the blob does not exist, the response will be \`404 Not Found\`.
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # HEAD to check if a blob exists
 curl -I \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/sha256:abc123...
 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the Repository
 example: library/ubuntu
 schema:
 type: string
 \- name: digest
 in: path
 required: true
 description: Digest of the blob
 schema:
 type: string
 example: sha256:abc123def4567890...
 \- name: Authorization
 in: header
 required: true
 description: Bearer token with pull or push scope
 schema:
 type: string
 example: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6...

 responses:
 "200":
 description: Blob exists
 headers:
 Content-Length:
 description: Size of the blob in bytes
 schema:
 type: integer
 example: 32654
 Docker-Content-Digest:
 description: Digest of the blob
 schema:
 type: string
 example: sha256:abc123def4567890...
 Content-Type:
 description: MIME type of the blob content
 schema:
 type: string
 example: application/octet-stream
 content:
 application/json:
 examples:
 blob-check-request:
 summary: Sample request
 value:
 method: HEAD
 url: /v2/library/ubuntu/blobs/sha256:abc123def4567890...
 headers:
 Authorization: Bearer
 Accept: '\*/\*'
 blob-check-response:
 summary: Sample 200 response headers
 value:
 status: 200 OK
 headers:
 Docker-Content-Digest: sha256:abc123def4567890...
 Content-Length: 32654
 Content-Type: application/octet-stream

 "404":
 description: Blob not found
 "401":
 description: Authentication required
 "403":
 description: Access denied
 "429":
 description: Too many requests
 get:
 tags:
 \- Blobs
 summary: Retrieve blob
 operationId: GetBlob
 description: \|
 Download the blob identified by digest from the registry.

 Blobs include image layers and configuration objects. Clients must use the digest from the manifest to retrieve a blob.

 This endpoint may return a \`307 Temporary Redirect\` to a CDN or storage location. Clients must follow the redirect to obtain the actual blob content.

 The blob content is typically a gzipped tarball (for layers) or JSON (for configs). The MIME type is usually \`application/octet-stream\`.
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # GET (download) a blob
 curl -L \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/sha256:abc123... \
 -o layer.tar.gz
 parameters:
 \- name: name
 in: path
 required: true
 description: Repository Name
 example: library/ubuntu
 schema:
 type: string
 \- name: digest
 in: path
 required: true
 description: Digest of the Blob
 schema:
 type: string
 example: sha256:abc123def456...
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 description: Bearer token with pull scope
 example: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6...

 responses:
 "200":
 description: Blob content returned directly
 headers:
 Content-Length:
 description: Size of the blob in bytes
 schema:
 type: integer
 example: 32768
 Content-Type:
 description: MIME type of the blob
 schema:
 type: string
 example: application/octet-stream
 Docker-Content-Digest:
 description: Digest of the returned blob
 schema:
 type: string
 example: sha256:abc123def456...
 content:
 application/octet-stream:
 schema:
 type: string
 format: binary
 examples:
 small-layer:
 summary: Example binary blob (gzipped tar layer)
 value: ""

 "307":
 description: Temporary redirect to blob location
 headers:
 Location:
 description: Redirect URL for blob download (e.g., S3 or CDN)
 schema:
 type: string
 example: https://cdn.docker.io/blobs/library/ubuntu/abc123...
 "401":
 description: Authentication required
 "403":
 description: Access denied
 "404":
 description: Blob not found
 "429":
 description: Too many requests
 /v2/{name}/blobs/uploads/{uuid}:
 get:
 tags:
 \- Blobs
 summary: Get blob upload status
 operationId: GetBlobUploadStatus
 description: \|
 Retrieve the current status of an in-progress blob upload.

 This is useful for:
 \- Resuming an interrupted upload
 \- Determining how many bytes have been accepted so far
 \- Retrying from the correct offset in chunked uploads

 The response includes the \`Range\` header indicating the byte range received so far, and a \`Docker-Upload-UUID\` for identifying the session.
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # GET upload status
 curl -I \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123
 parameters:
 \- name: name
 in: path
 required: true
 description: Repository Name
 example : library/ubuntu
 schema:
 type: string
 \- name: uuid
 in: path
 required: true
 description: Upload session UUID
 schema:
 type: string
 example: abc123
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 example: Bearer eyJhbGciOi...

 responses:
 "204":
 description: Upload in progress. No body is returned.
 headers:
 Range:
 description: Current byte range uploaded (inclusive)
 schema:
 type: string
 example: 0-16383
 Docker-Upload-UUID:
 description: UUID of the upload session
 schema:
 type: string
 example: abc123
 Location:
 description: URL to continue or complete the upload
 schema:
 type: string
 example: /v2/library/ubuntu/blobs/uploads/abc123
 "401":
 description: Authentication required
 "403":
 description: Access denied
 "404":
 description: Upload session not found
 "429":
 description: Too many requests

 put:
 tags:
 \- Blobs
 summary: Complete blob upload
 operationId: CompleteBlobUpload
 description: \|
 Complete the upload of a blob by finalizing an upload session.

 This request must include the \`digest\` query parameter and optionally the last chunk of data. When the registry receives this request, it verifies the digest and stores the blob.

 This endpoint supports:
 \- Monolithic uploads (upload entire blob in this request)
 \- Finalizing chunked uploads (last chunk plus \`digest\`)

 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # PUT – complete upload (monolithic or final chunk)
 curl -X PUT \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/octet-stream" \
 --data-binary @layer.tar.gz \
 "https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123?digest=sha256:abcd1234..."

 parameters:
 \- name: name
 in: path
 required: true
 description: Repository name
 schema:
 type: string
 example: library/ubuntu
 \- name: uuid
 in: path
 required: true
 description: Upload session UUID returned from the POST request
 schema:
 type: string
 example: abc123
 \- name: digest
 in: query
 required: true
 description: Digest of the uploaded blob
 schema:
 type: string
 example: sha256:abcd1234...
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 example: Bearer eyJhbGciOi...

 requestBody:
 required: false
 content:
 application/octet-stream:
 schema:
 type: string
 format: binary
 examples:
 layer-upload:
 summary: Layer tarball blob
 value: ""

 responses:
 "201":
 description: Upload completed successfully
 headers:
 Docker-Content-Digest:
 description: Canonical digest of the stored blob
 schema:
 type: string
 example: sha256:abcd1234...
 Location:
 description: URL where the blob is now accessible
 schema:
 type: string
 example: /v2/library/ubuntu/blobs/sha256:abcd1234...
 Content-Length:
 description: Always zero for completed uploads
 schema:
 type: integer
 example: 0
 "400":
 description: Invalid digest or missing parameters
 "401":
 description: Authentication required
 "403":
 description: Access denied
 "404":
 description: Upload session not found
 "416":
 description: Requested range not satisfiable (if used in chunked mode)
 "429":
 description: Too many requests

 patch:
 tags:
 \- Blobs
 summary: Upload blob chunk
 operationId: UploadBlobChunk
 description: \|
 Upload a chunk of a blob to an active upload session.

 Use this method for \*\*chunked uploads\*\*, especially for large blobs or when resuming interrupted uploads.

 The client sends binary data using \`PATCH\`, optionally including a \`Content-Range\` header.

 After each chunk is accepted, the registry returns a \`202 Accepted\` response with:
 \- \`Range\`: current byte range stored
 \- \`Docker-Upload-UUID\`: identifier for the upload session
 \- \`Location\`: URL to continue the upload or finalize with \`PUT\`
 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # PATCH – upload a chunk (first 64 KiB)
 curl -X PATCH \
 -H "Authorization: Bearer $TOKEN" \
 -H "Content-Type: application/octet-stream" \
 --data-binary @chunk-0.bin \
 "https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123"
 parameters:
 \- name: name
 in: path
 required: true
 description: Repository name
 schema:
 type: string
 example: library/ubuntu
 \- name: uuid
 in: path
 required: true
 description: Upload session UUID
 schema:
 type: string
 example: abc123
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 example: Bearer eyJhbGciOi...
 \- name: Content-Range
 in: header
 required: false
 schema:
 type: string
 example: bytes 0-65535
 description: Optional. Byte range of the chunk being sent

 requestBody:
 required: true
 content:
 application/octet-stream:
 schema:
 type: string
 format: binary
 examples:
 chunk-0:
 summary: Upload chunk 0 of a blob
 value: ""

 responses:
 "202":
 description: Chunk accepted and stored
 headers:
 Location:
 description: URL to continue or finalize the upload
 schema:
 type: string
 example: /v2/library/ubuntu/blobs/uploads/abc123
 Range:
 description: Byte range uploaded so far (inclusive)
 schema:
 type: string
 example: 0-65535
 Docker-Upload-UUID:
 description: Upload session UUID
 schema:
 type: string
 example: abc123
 "400":
 description: Malformed content or range
 "401":
 description: Authentication required
 "403":
 description: Access denied
 "404":
 description: Upload session not found
 "416":
 description: Range error (e.g., chunk out of order)
 "429":
 description: Too many requests
 delete:
 tags:
 \- Blobs
 summary: Cancel blob upload
 operationId: CancelBlobUpload
 description: \|
 Cancel an in-progress blob upload session.

 This operation discards any data that has been uploaded and invalidates the upload session.

 Use this when:
 \- An upload fails or is aborted mid-process
 \- The client wants to clean up unused upload sessions

 After cancellation, the UUID is no longer valid and a new \`POST\` must be issued to restart the upload.

 x-codeSamples:
 \- lang: Bash
 label: cURL
 source: \|
 # DELETE – cancel an upload session
 curl -X DELETE \
 -H "Authorization: Bearer $TOKEN" \
 https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123\`

 parameters:
 \- name: name
 in: path
 required: true
 description: Name of the repository
 schema:
 type: string
 example: library/ubuntu
 \- name: uuid
 in: path
 required: true
 description: Upload session UUID
 schema:
 type: string
 example: abc123
 \- name: Authorization
 in: header
 required: true
 schema:
 type: string
 example: Bearer eyJhbGciOi...

 responses:
 "204":
 description: Upload session cancelled successfully. No body is returned.
 headers:
 Content-Length:
 description: Always zero
 schema:
 type: integer
 example: 0
 "401":
 description: Authentication required
 "403":
 description: Access denied
 "404":
 description: Upload session not found
 "429":
 description: Too many requests

x-tagGroups:
 \- name: General
 tags:
 \- overview
 \- authentication
 \- pull
 \- push
 \- delete
 \- name: API
 tags:
 \- Manifests
 \- Blobs

----
url: https://docs.docker.com/reference/compose-file/legacy-versions/
----

# Legacy versions

***

***

The legacy versions of the Compose file reference has moved to the [V1 branch of the Compose repository](https://github.com/docker/compose/tree/v1/docs). They are no longer being actively maintained.

The latest and recommended version of the Compose file format is defined by the [Compose Specification](https://docs.docker.com/reference/compose-file/). This format merges the 2.x and 3.x versions and is implemented by **Compose 1.27.0+**. For more information, see the [History and development of Docker Compose](https://docs.docker.com/compose/intro/history/).

----
url: https://docs.docker.com/reference/cli/docker/compose/logs/
----

# docker compose logs

***

| Description | View output from containers                  |
| ----------- | -------------------------------------------- |
| Usage       | `docker compose logs [OPTIONS] [SERVICE...]` |

## [Description](#description)

Displays log output from services

## [Options](#options)

| Option             | Default | Description                                                                                     |
| ------------------ | ------- | ----------------------------------------------------------------------------------------------- |
| `-f, --follow`     |         | Follow log output                                                                               |
| `--index`          |         | index of the container if service has multiple replicas                                         |
| `--no-color`       |         | Produce monochrome output                                                                       |
| `--no-log-prefix`  |         | Don't print prefix in logs                                                                      |
| `--since`          |         | Show logs since timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)     |
| `-n, --tail`       | `all`   | Number of lines to show from the end of the logs for each container                             |
| `-t, --timestamps` |         | Show timestamps                                                                                 |
| `--until`          |         | Show logs before a timestamp (e.g. 2013-01-02T13:23:37Z) or relative (e.g. 42m for 42 minutes)  |

----
url: https://docs.docker.com/engine/release-notes/24.0/
----

# Docker Engine 24.0 release notes

***

Table of contents

***

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 24.0.

For more information about:

* Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
* Changes to the Engine API, see [Engine API version history](/reference/api/engine/version-history/).

## [24.0.9](#2409)

*2024-01-31*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.9 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.9)
* [moby/moby, 24.0.9 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.9)

## [Security](#security)

This release contains security fixes for the following CVEs affecting Docker Engine and its components.

| CVE                                                         | Component     | Fix version | Severity         |
| ----------------------------------------------------------- | ------------- | ----------- | ---------------- |
| [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) | runc          | 1.1.12      | High, CVSS 8.6   |
| [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557) | Docker Engine | 24.0.9      | Medium, CVSS 6.9 |

> Important
>
> Note that this release of Docker Engine doesn't include fixes for the following known vulnerabilities in BuildKit:
>
> * [CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651)
> * [CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652)
> * [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653)
> * [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650)
>
> To address these vulnerabilities, upgrade to [Docker Engine v25.0.2](https://docs.docker.com/engine/release-notes/25.0/#2502).

For more information about the security issues addressed in this release, and the unaddressed vulnerabilities in BuildKit, refer to the [blog post](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/).

For details about each vulnerability, see the relevant security advisory:

* [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
* [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

### [Packaging updates](#packaging-updates)

* Upgrade runc to [v1.1.12](https://github.com/opencontainers/runc/releases/tag/v1.1.12). [moby/moby#47269](https://github.com/moby/moby/pull/47269)
* Upgrade containerd to [v1.7.13](https://github.com/containerd/containerd/releases/tag/v1.7.13) (static binaries only). [moby/moby#47280](https://github.com/moby/moby/pull/47280)

## [24.0.8](#2408)

*2024-01-25*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.8 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.8)
* [moby/moby, 24.0.8 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.8)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements)

* Live restore: Containers with auto remove (`docker run --rm`) are no longer forcibly removed on engine restart. [moby/moby#46857](https://github.com/moby/moby/pull/46869)

### [Packaging updates](#packaging-updates-1)

* Upgrade Go to `go1.20.13`. [moby/moby#47054](https://github.com/moby/moby/pull/47054), [docker/cli#4826](https://github.com/docker/cli/pull/4826), [docker/docker-ce-packaging#975](https://github.com/docker/docker-ce-packaging/pull/975)
* Upgrade containerd (static binaries only) to [v1.7.12](https://github.com/containerd/containerd/releases/tag/v1.7.12) [moby/moby#47096](https://github.com/moby/moby/pull/47096)
* Upgrade runc to v1.1.11. [moby/moby#47010](https://github.com/moby/moby/pull/47010)

## [24.0.7](#2407)

*2023-10-27*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.7 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.7)
* [moby/moby, 24.0.7 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.7)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-1)

* Write overlay2 layer metadata atomically. [moby/moby#46703](https://github.com/moby/moby/pull/46703)
* Fix "Rootful-in-Rootless" Docker-in-Docker on systemd version 250 and later. [moby/moby#46626](https://github.com/moby/moby/pull/46626)
* Fix `dockerd-rootless-setuptools.sh` when username contains a backslash. [moby/moby#46407](https://github.com/moby/moby/pull/46407)
* Fix a bug that would prevent network sandboxes to be fully deleted when stopping containers with no network attachments and when `dockerd --bridge=none` is used. [moby/moby#46702](https://github.com/moby/moby/pull/46702)
* Fix a bug where cancelling an API request could interrupt container restart. [moby/moby#46697](https://github.com/moby/moby/pull/46697)
* Fix an issue where containers would fail to start when providing `--ip-range` with a range larger than the subnet. [docker/for-mac#6870](https://github.com/docker/for-mac/issues/6870)
* Fix data corruption with zstd output. [moby/moby#46709](https://github.com/moby/moby/pull/46709)
* Fix the conditions under which the container's MAC address is applied. [moby/moby#46478](https://github.com/moby/moby/pull/46478)
* Improve the performance of the stats collector. [moby/moby#46448](https://github.com/moby/moby/pull/46448)
* Fix an issue with source policy rules ending up in the wrong order. [moby/moby#46441](https://github.com/moby/moby/pull/46441)

### [Packaging updates](#packaging-updates-2)

* Add support for Fedora 39 and Ubuntu 23.10. [docker/docker-ce-packaging#940](https://github.com/docker/docker-ce-packaging/pull/940), [docker/docker-ce-packaging#955](https://github.com/docker/docker-ce-packaging/pull/955)
* Fix `docker.socket` not getting disabled when uninstalling the `docker-ce` RPM package. [docker/docker-ce-packaging#852](https://github.com/docker/docker-ce-packaging/pull/852)
* Upgrade Go to `go1.20.10`. [docker/docker-ce-packaging#951](https://github.com/docker/docker-ce-packaging/pull/951)
* Upgrade containerd to `v1.7.6` (static binaries only). [moby/moby#46103](https://github.com/moby/moby/pull/46103)
* Upgrade the `containerd.io` package to [`v1.6.24`](https://github.com/containerd/containerd/releases/tag/v1.6.24).

### [Security](#security-1)

* Deny containers access to `/sys/devices/virtual/powercap` by default. This change hardens against [CVE-2020-8694](https://scout.docker.com/v/CVE-2020-8694), [CVE-2020-8695](https://scout.docker.com/v/CVE-2020-8695), and [CVE-2020-12912](https://scout.docker.com/v/CVE-2020-12912), and an attack known as [the PLATYPUS attack](https://platypusattack.com/).

  For more details, see [advisory](https://github.com/moby/moby/security/advisories/GHSA-jq35-85cj-fj4p), [commit](https://github.com/moby/moby/commit/c9ccbfad11a60e703e91b6cca4f48927828c7e35).

## [24.0.6](#2406)

*2023-09-05*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.6 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.6)
* [moby/moby, 24.0.6 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.6)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-2)

* containerd storage backend: Fix `docker ps` failing when a container image is no longer present in the content store. [moby/moby#46095](https://github.com/moby/moby/pull/46095)
* containerd storage backend: Fix `docker ps -s -a` and `docker container prune` failing when a container image config is no longer present in the content store. [moby/moby#46097](https://github.com/moby/moby/pull/46097)
* containerd storage backend: Fix `docker inspect` failing when a container image config is no longer (or was never) present in the content store. [moby/moby#46244](https://github.com/moby/moby/pull/46244)
* containerd storage backend: Fix diff and export with the `overlayfs` snapshotter by using reference-counted rootfs mounts. [moby/moby#46266](https://github.com/moby/moby/pull/46266)
* containerd storage backend: Fix a misleading error message when the image platforms available locally do not match the desired platform. [moby/moby#46300](https://github.com/moby/moby/pull/46300)
* containerd storage backend: Fix the `FROM scratch` Dockerfile instruction with the classic builder. [moby/moby#46302](https://github.com/moby/moby/pull/46302)
* containerd storage backend: Fix `mismatched image rootfs and manifest layers` errors with the classic builder. [moby/moby#46310](https://github.com/moby/moby/pull/46310)
* Warn when pulling Docker Image Format v1, and Docker Image manifest version 2, schema 1 images from all registries. [moby/moby#46290](https://github.com/moby/moby/pull/46290)
* Fix live-restore of volumes with custom volume options. [moby/moby#46366](https://github.com/moby/moby/pull/46366)
* Fix incorrectly dropping capabilities bits when running a container as a non-root user (note: this change was already effectively present due to a regression). [moby/moby#46221](https://github.com/moby/moby/pull/46221)
* Fix network isolation iptables rules preventing IPv6 Neighbor Solicitation packets from being exchanged between containers. [moby/moby#46214](https://github.com/moby/moby/pull/46214)
* Fix `dockerd.exe --register-service` not working when the binary is in the current directory on Windows. [moby/moby#46215](https://github.com/moby/moby/pull/46215)
* Add a hint suggesting the use of a PAT to `docker login` against Docker Hub. [docker/cli#4500](https://github.com/docker/cli/pull/4500)
* Improve shell startup time for users of Bash completion for the CLI. [docker/cli#4517](https://github.com/docker/cli/pull/4517)
* Improve the speed of some commands by skipping `GET /_ping` when possible. [docker/cli#4508](https://github.com/docker/cli/pull/4508)
* Fix credential scopes when using a PAT to `docker manifest inspect` an image on Docker Hub. [docker/cli#4512](https://github.com/docker/cli/pull/4512)
* Fix `docker events` not supporting `--format=json`. [docker/cli#4544](https://github.com/docker/cli/pull/4544)

### [Packaging updates](#packaging-updates-3)

* Upgrade Go to `go1.20.7`. [moby/moby#46140](https://github.com/moby/moby/pull/46140), [docker/cli#4476](https://github.com/docker/cli/pull/4476), [docker/docker-ce-packaging#932](https://github.com/docker/docker-ce-packaging/pull/932)
* Upgrade containerd to `v1.7.3` (static binaries only). [moby/moby#46103](https://github.com/moby/moby/pull/46103)
* Upgrade Compose to `v2.21.0`. [docker/docker-ce-packaging#936](https://github.com/docker/docker-ce-packaging/pull/936)

## [24.0.5](#2405)

*2023-07-24*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.5 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.5)
* [moby/moby, 24.0.5 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.5)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-3)

* The Go client now avoids using UNIX socket paths in the HTTP `Host:` header, in order to be compatible with changes introduced in `go1.20.6`. [moby/moby#45962](https://github.com/moby/moby/pull/45962), [moby/moby#45990](https://github.com/moby/moby/pull/45990)
* containerd storage backend: Fix `Variant` not being included in `docker image inspect` and `GET /images/{name}/json`. [moby/moby#46025](https://github.com/moby/moby/pull/46025)
* containerd storage backend: Prevent potential garbage collection of content during image export. [moby/moby#46021](https://github.com/moby/moby/pull/46021)
* containerd storage backend: Prevent duplicate digest entries in `RepoDigests`. [moby/moby#46014](https://github.com/moby/moby/pull/46014)
* containerd storage backend: Fix operations taking place against the incorrect tag when working with an image referenced by tag and digest. [moby/moby#46013](https://github.com/moby/moby/pull/46013)
* containerd storage backend: Fix a panic caused by `EXPOSE` when building containers with the legacy builder. [moby/moby#45921](https://github.com/moby/moby/pull/45921)
* Fix a regression causing unintuitive errors to be returned when attempting to create an `overlay` network on a non-Swarm node. [moby/moby#45974](https://github.com/moby/moby/pull/45974)
* Properly report errors parsing volume specifications from the command line. [docker/cli#4423](https://github.com/docker/cli/pull/4423)
* Fix a panic caused when `auths: null` is found in the CLI config file. [docker/cli#4450](https://github.com/docker/cli/pull/4450)

### [Packaging updates](#packaging-updates-4)

* Use init scripts as provided by in moby/moby `contrib/init`. [docker/docker-ce-packaging#914](https://github.com/docker/docker-ce-packaging/pull/914), [docker/docker-ce-packaging#926](https://github.com/docker/docker-ce-packaging/pull/926)
* Drop Upstart from `contrib/init`. [moby/moby#46044](https://github.com/moby/moby/pull/46044)
* Upgrade Go to `go1.20.6`. [docker/cli#4428](https://github.com/docker/cli/pull/4428), [moby/moby#45970](https://github.com/moby/moby/pull/45970), [docker/docker-ce-packaging#921](https://github.com/docker/docker-ce-packaging/pull/921)
* Upgrade Compose to `v2.20.2`. [docker/docker-ce-packaging#924](https://github.com/docker/docker-ce-packaging/pull/924)
* Upgrade buildx to `v0.11.2`. [docker/docker-ce-packaging#922](https://github.com/docker/docker-ce-packaging/pull/922)

## [24.0.4](#2404)

*2023-07-07*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.4)
* [moby/moby, 24.0.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.4)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-4)

* Fix a regression introduced during 24.0.3 that causes a panic during live-restore of containers with bind mounts. [moby/moby#45903](https://github.com/moby/moby/pull/45903)

## [24.0.3](#2403)

*2023-07-06*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.3)
* [moby/moby, 24.0.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.3)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-5)

* containerd image store: Fix an issue where multi-platform images that did not include a manifest for the default platform could not be interacted with. [moby/moby#45849](https://github.com/moby/moby/pull/45849)
* containerd image store: Fix specious attempts to cache `FROM scratch` in container builds. [moby/moby#45822](https://github.com/moby/moby/pull/45822)
* containerd image store: Fix `docker cp` with snapshotters that cannot mount the same content multiple times. [moby/moby#45780](https://github.com/moby/moby/pull/45780), [moby/moby#45786](https://github.com/moby/moby/pull/45786)
* containerd image store: Fix builds with `type=image` not being correctly unpacked/stored. [moby/moby#45692](https://github.com/moby/moby/pull/45692)
* containerd image store: Fix incorrectly attempting to unpack pseudo-images (including attestations) in `docker load`. [moby/moby#45688](https://github.com/moby/moby/pull/45688)
* containerd image store: Correctly set the user agent, and include additional information like the snapshotter when interacting with registries. [moby/moby#45671](https://github.com/moby/moby/pull/45671), [moby/moby#45684](https://github.com/moby/moby/pull/45684)
* containerd image store: Fix a failure to unpack already-pulled content after switching between snapshotters. [moby/moby#45678](https://github.com/moby/moby/pull/45678)
* containerd image store: Fix images that have been re-tagged or with all tags removed being pruned while still in use. [moby/moby#45857](https://github.com/moby/moby/pull/45857)
* Fix a Swarm CSI issue where the Topology field was not propagated into NodeCSIInfo. [moby/moby#45810](https://github.com/moby/moby/pull/45810)
* Fix failures to add new Swarm managers caused by a very large raft log. [moby/moby#45703](https://github.com/moby/moby/pull/45703), [moby/swarmkit#3122](https://github.com/moby/swarmkit/pull/3122), [moby/swarmkit#3128](https://github.com/moby/swarmkit/pull/3128)
* `name_to_handle_at(2)` is now always allowed in the default seccomp profile. [moby/moby#45833](https://github.com/moby/moby/pull/45833)
* Fix an issue that prevented encrypted Swarm overlay networks from working on ports other than the default (4789). [moby/moby#45637](https://github.com/moby/moby/pull/45637)
* Fix a failure to restore mount reference-counts during live-restore. [moby/moby#45824](https://github.com/moby/moby/pull/45824)
* Fix various networking-related failures during live-restore. [moby/moby#45658](https://github.com/moby/moby/pull/45658), [moby/moby#45659](https://github.com/moby/moby/pull/45659)
* Fix running containers restoring with a zero (successful) exit status when the daemon is unexpectedly terminated. [moby/moby#45801](https://github.com/moby/moby/pull/45801)
* Fix a potential panic while executing healthcheck probes. [moby/moby#45798](https://github.com/moby/moby/pull/45798)
* Fix a panic caused by a race condition in container exec start. [moby/moby#45794](https://github.com/moby/moby/pull/45794)
* Fix an exception caused by attaching a terminal to an exec with a non-existent command. [moby/moby#45643](https://github.com/moby/moby/pull/45643)
* Fix `host-gateway` with BuildKit by passing the IP as a label (also requires [docker/buildx#1894](https://github.com/docker/buildx/pull/1894)). [moby/moby#45790](https://github.com/moby/moby/pull/45790)
* Fix an issue where `POST /containers/{id}/stop` would forcefully terminate the container when the request was canceled, instead of waiting until the specified timeout for a 'graceful' stop. [moby/moby#45774](https://github.com/moby/moby/pull/45774)
* Fix an issue where `docker cp -a` from the root (`/`) directory would fail. [moby/moby#45748](https://github.com/moby/moby/pull/45748)
* Improve compatibility with non-runc container runtimes by more correctly setting resource constraint parameters in the OCI config. [moby/moby#45746](https://github.com/moby/moby/pull/45746)
* Fix an issue caused by overlapping subuid/subgid ranges in certain configurations (e.g. LDAP) in rootless mode. [moby/moby#45747](https://github.com/moby/moby/pull/45747), [rootless-containers/rootlesskit#369](https://github.com/rootless-containers/rootlesskit/pull/369)
* Greatly reduce CPU and memory usage while populating the Debug section of `GET /info`. [moby/moby#45856](https://github.com/moby/moby/pull/45856)
* Fix an issue where debug information was not correctly printed during `docker info` when only the client is in debug mode. [docker/cli#4393](https://github.com/docker/cli/pull/4393)
* Fix issues related to hung connections when connecting to hosts over a SSH connection. [docker/cli#4395](https://github.com/docker/cli/pull/4395)

### [Packaging updates](#packaging-updates-5)

* Upgrade Go to `go1.20.5`. [moby/moby#45745](https://github.com/moby/moby/pull/45745), [docker/cli#4351](https://github.com/docker/cli/pull/4351), [docker/docker-ce-packaging#904](https://github.com/docker/docker-ce-packaging/pull/904)
* Upgrade Compose to `v2.19.1`. [docker/docker-ce-packaging#916](https://github.com/docker/docker-ce-packaging/pull/916)
* Upgrade buildx to `v0.11.1`. [docker/docker-ce-packaging#918](https://github.com/docker/docker-ce-packaging/pull/918)

## [24.0.2](#2402)

*2023-05-26*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.2)
* [moby/moby, 24.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.2)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-6)

* Fix a panic during build when referencing locally tagged images. [moby/buildkit#3899](https://github.com/moby/buildkit/pull/3899), [moby/moby#45582](https://github.com/moby/moby/pull/45582)
* Fix builds potentially failing with `exit code: 4294967295` when performing many concurrent build stages. [moby/moby#45620](https://github.com/moby/moby/pull/45620)
* Fix DNS resolution on Windows ignoring `etc/hosts` (`%WINDIR%\System32\Drivers\etc\hosts`), including resolution of `localhost`. [moby/moby#45562](https://github.com/moby/moby/pull/45562)
* Apply a workaround for a containerd bug that causes concurrent `docker exec` commands to take significantly longer than expected. [moby/moby#45625](https://github.com/moby/moby/pull/45625)
* containerd image store: Fix an issue where the image `Created` field would contain an incorrect value. [moby/moby#45623](https://github.com/moby/moby/pull/45623)
* containerd image store: Adjust the output of image pull progress so that the output has the same format regardless of whether the containerd image store is enabled. [moby/moby#45602](https://github.com/moby/moby/pull/45602)
* containerd image store: Switching between the default and containerd image store now requires a daemon restart. [moby/moby#45616](https://github.com/moby/moby/pull/45616)

### [Packaging updates](#packaging-updates-6)

* Upgrade Buildx to `v0.10.5`. [docker/docker-ce-packaging#900](https://github.com/docker/docker-ce-packaging/pull/900)

## [24.0.1](#2401)

*2023-05-19*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.1)
* [moby/moby, 24.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.1)

### [Removed](#removed)

* Remove CLI completions for storage drivers removed in the 24.0 major release. [docker/cli#4302](https://github.com/docker/cli/pull/4302)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-7)

* Fix an issue where DNS query NXDOMAIN replies from external servers were forwarded to the client as SERVFAIL. [moby/moby#45573](https://github.com/moby/moby/pull/45573)
* Fix an issue where `docker pull --platform` would report `No such image` regarding another tag pointing to the same image. [moby/moby#45562](https://github.com/moby/moby/pull/45562)
* Fix an issue where insecure registry configuration would be forgotten during config reload. [moby/moby#45571](https://github.com/moby/moby/pull/45571)
* containerd image store: Fix an issue where images which have no layers would not be listed in `docker images -a` [moby/moby#45588](https://github.com/moby/moby/pull/45588)
* API: Fix an issue where `GET /images/{id}/json` would return `null` instead of empty `RepoTags` and `RepoDigests`. [moby/moby#45564](https://github.com/moby/moby/pull/45564)
* API: Fix an issue where `POST /commit` did not accept an empty request body. [moby/moby#45568](https://github.com/moby/moby/pull/45568)

### [Packaging updates](#packaging-updates-7)

* Upgrade Compose to `v2.18.1`. [docker/docker-ce-packaging#896](https://github.com/docker/docker-ce-packaging/pull/896)

## [24.0.0](#2400)

*2023-05-16*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 24.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A24.0.0)
* [moby/moby, 24.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A24.0.0)

### [New](#new)

* Introduce experimental support for containerd as the content store (replacing the existing storage drivers). [moby/moby#43735](https://github.com/moby/moby/pull/43735), [other moby/moby pull requests](https://github.com/moby/moby/pulls?q=is%3Apr+is%3Amerged+milestone%3A24.0.0+-label%3Aprocess%2Fcherry-picked+label%3Acontainerd-integration+)
* The `--host` CLI flag now supports a path component in a `ssh://` host address, allowing use of an alternate socket path without configuration on the remote host. [docker/cli#4073](https://github.com/docker/cli/pull/4073)
* The `docker info` CLI command now reports a version and platform field. [docker/cli#4180](https://github.com/docker/cli/pull/4180)
* Introduce the daemon flag `--default-network-opt` to configure options for newly created networks. [moby/moby#43197](https://github.com/moby/moby/pull/43197)
* Restrict access to `AF_VSOCK` in the `socket(2)` family of syscalls in the default seccomp profile. [moby/moby#44562](https://github.com/moby/moby/pull/44562)
* Introduce support for setting OCI runtime annotations on containers. [docker/cli#4156](https://github.com/docker/cli/pull/4156), [moby/moby#45025](https://github.com/moby/moby/pull/45025)
* Alternative runtimes can now be configured in `daemon.json`, enabling runtime names to be aliased and options to be passed. [moby/moby#45032](https://github.com/moby/moby/pull/45032)
* The `docker-init` binary will now be discovered in FHS-compliant libexec directories, in addition to the `PATH`. [moby/moby#45198](https://github.com/moby/moby/pull/45198)
* API: Surface the daemon-level `--no-new-privileges` in `GET /info`. [moby/moby#45320](https://github.com/moby/moby/pull/45320)

### [Removed](#removed-1)

* `docker info` no longer reports `IndexServiceAddress`. [docker/cli#4204](https://github.com/docker/cli/pull/4204)
* libnetwork: Remove fallback code for obsolete kernel versions. [moby/moby#44684](https://github.com/moby/moby/pull/44684), [moby/moby#44802](https://github.com/moby/moby/pull/44802)
* libnetwork: Remove unused code related to classic Swarm. [moby/moby#44965](https://github.com/moby/moby/pull/44965)
* libnetwork: Remove usage of the `xt_u32` kernel module from encrypted Swarm overlay networks. [moby/moby#45281](https://github.com/moby/moby/pull/45281)
* Remove support for BuildKit's deprecated `buildinfo` in favor of standard provenance attestations. [moby/moby#45097](https://github.com/moby/moby/pull/45097)
* Remove the deprecated AUFS and legacy `overlay` storage drivers. [moby/moby#45342](https://github.com/moby/moby/pull/45342), [moby/moby#45359](https://github.com/moby/moby/pull/45359)
* Remove the deprecated `overlay2.override_kernel_check` storage driver option. [moby/moby#45368](https://github.com/moby/moby/pull/45368)
* Remove workarounds for obsolete versions of `apparmor_parser` from the AppArmor profiles. [moby/moby#45500](https://github.com/moby/moby/pull/45500)
* API: `GET /images/json` no longer represents empty RepoTags and RepoDigests as`<none>:<none>`/`<none>@<none>`. Empty arrays are returned instead on API >= 1.43. [moby/moby#45068](https://github.com/moby/moby/pull/45068)

### [Deprecated](#deprecated)

* Deprecate the `--oom-score-adjust` daemon option. [moby/moby#45315](https://github.com/moby/moby/pull/45315)
* API: Deprecate the `VirtualSize` field in `GET /images/json` and `GET /images/{id}/json`. [moby/moby#45346](https://github.com/moby/moby/pull/45346)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-8)

* The `docker stack` command no longer validates the `build` section of Compose files. [docker/cli#4214](https://github.com/docker/cli/pull/4214)
* Fix lingering healthcheck processes after the timeout is reached. [moby/moby#43739](https://github.com/moby/moby/pull/43739)
* Reduce the overhead of container startup when using the `overlay2` storage driver. [moby/moby#44285](https://github.com/moby/moby/pull/44285)
* API: Handle multiple `before=` and `since=` filters in `GET /images`. [moby/moby#44503](https://github.com/moby/moby/pull/44503)
* Fix numerous bugs in the embedded DNS resolver implementation used by user-defined networks. [moby/moby#44664](https://github.com/moby/moby/pull/44664)
* Add `execDuration` field to the map of event attributes. [moby/moby#45494](https://github.com/moby/moby/pull/45494)
* Swarm-level networks can now be created with the Windows `internal`, `l2bridge`, and `nat` drivers. [moby/swarmkit#3121](https://github.com/moby/swarmkit/pull/3121), [moby/moby#45291](https://github.com/moby/moby/pull/45291)

### [Packaging updates](#packaging-updates-8)

* Update Go to `1.20.4`. [docker/cli#4253](https://github.com/docker/cli/pull/4253), [moby/moby#45456](https://github.com/moby/moby/pull/45456), [docker/docker-ce-packaging#888](https://github.com/docker/docker-ce-packaging/pull/888)
* Update `containerd` to [`v1.7.1`](https://github.com/containerd/containerd/releases/tag/v1.7.1). [moby/moby#45537](https://github.com/moby/moby/pull/45537)
* Update `buildkit` to [`v0.11.6`](https://github.com/moby/buildkit/releases/v0.11.6). [moby/moby#45367](https://github.com/moby/moby/pull/45367)

----
url: https://docs.docker.com/reference/cli/docker/stack/ps/
----

# docker stack ps

***

| Description | List the tasks in the stack       |
| ----------- | --------------------------------- |
| Usage       | `docker stack ps [OPTIONS] STACK` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Lists the tasks that are running as part of the specified stack.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                        | Default | Description                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-f, --filter`](#filter)     |         | Filter output based on conditions provided                                                                                                                                                                                                                                                                                                                                             |
| [`--format`](#format)         |         | Format output using a custom template: 'table': Print output in table format with column headers (default) 'table TEMPLATE': Print output in table format using the given Go template 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| [`--no-resolve`](#no-resolve) |         | Do not map IDs to Names                                                                                                                                                                                                                                                                                                                                                                |
| [`--no-trunc`](#no-trunc)     |         | Do not truncate output                                                                                                                                                                                                                                                                                                                                                                 |
| [`-q, --quiet`](#quiet)       |         | Only display task IDs                                                                                                                                                                                                                                                                                                                                                                  |

## [Examples](#examples)

### [List the tasks that are part of a stack](#list-the-tasks-that-are-part-of-a-stack)

The following command shows all the tasks that are part of the `voting` stack:

```console
$ docker stack ps voting

ID                  NAME                  IMAGE                                          NODE   DESIRED STATE  CURRENT STATE          ERROR  PORTS
xim5bcqtgk1b        voting_worker.1       dockersamples/examplevotingapp_worker:latest   node2  Running        Running 2 minutes ago
q7yik0ks1in6        voting_result.1       dockersamples/examplevotingapp_result:before   node1  Running        Running 2 minutes ago
rx5yo0866nfx        voting_vote.1         dockersamples/examplevotingapp_vote:before     node3  Running        Running 2 minutes ago
tz6j82jnwrx7        voting_db.1           postgres:9.4                                   node1  Running        Running 2 minutes ago
w48spazhbmxc        voting_redis.1        redis:alpine                                   node2  Running        Running 3 minutes ago
6jj1m02freg1        voting_visualizer.1   dockersamples/visualizer:stable                node1  Running        Running 2 minutes ago
kqgdmededccb        voting_vote.2         dockersamples/examplevotingapp_vote:before     node2  Running        Running 2 minutes ago
t72q3z038jeh        voting_redis.2        redis:alpine                                   node3  Running        Running 3 minutes ago
```

```console
$ docker stack ps -f "id=t" voting

ID                  NAME                IMAGE               NODE         DESIRED STATE       CURRENTSTATE            ERROR  PORTS
tz6j82jnwrx7        voting_db.1         postgres:9.4        node1        Running             Running 14 minutes ago
t72q3z038jeh        voting_redis.2      redis:alpine        node3        Running             Running 14 minutes ago
```

#### [name](#name)

The `name` filter matches on task names.

```console
$ docker stack ps -f "name=voting_redis" voting

ID                  NAME                IMAGE               NODE         DESIRED STATE       CURRENTSTATE            ERROR  PORTS
w48spazhbmxc        voting_redis.1      redis:alpine        node2        Running             Running 17 minutes ago
t72q3z038jeh        voting_redis.2      redis:alpine        node3        Running             Running 17 minutes ago
```

#### [node](#node)

The `node` filter matches on a node name or a node ID.

```console
$ docker stack ps -f "node=node1" voting

ID                  NAME                  IMAGE                                          NODE   DESIRED STATE  CURRENT STATE          ERROR  PORTS
q7yik0ks1in6        voting_result.1       dockersamples/examplevotingapp_result:before   node1  Running        Running 18 minutes ago
tz6j82jnwrx7        voting_db.1           postgres:9.4                                   node1  Running        Running 18 minutes ago
6jj1m02freg1        voting_visualizer.1   dockersamples/visualizer:stable                node1  Running        Running 18 minutes ago
```

#### [desired-state](#desired-state)

The `desired-state` filter can take the values `running`, `shutdown`, `ready` or `accepted`.

```console
$ docker stack ps -f "desired-state=running" voting

ID                  NAME                  IMAGE                                          NODE   DESIRED STATE  CURRENT STATE           ERROR  PORTS
xim5bcqtgk1b        voting_worker.1       dockersamples/examplevotingapp_worker:latest   node2  Running        Running 21 minutes ago
q7yik0ks1in6        voting_result.1       dockersamples/examplevotingapp_result:before   node1  Running        Running 21 minutes ago
rx5yo0866nfx        voting_vote.1         dockersamples/examplevotingapp_vote:before     node3  Running        Running 21 minutes ago
tz6j82jnwrx7        voting_db.1           postgres:9.4                                   node1  Running        Running 21 minutes ago
w48spazhbmxc        voting_redis.1        redis:alpine                                   node2  Running        Running 21 minutes ago
6jj1m02freg1        voting_visualizer.1   dockersamples/visualizer:stable                node1  Running        Running 21 minutes ago
kqgdmededccb        voting_vote.2         dockersamples/examplevotingapp_vote:before     node2  Running        Running 21 minutes ago
t72q3z038jeh        voting_redis.2        redis:alpine                                   node3  Running        Running 21 minutes ago
```

### [Format the output (--format)](#format)

The formatting options (`--format`) pretty-prints tasks output using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder     | Description                                                      |
| --------------- | ---------------------------------------------------------------- |
| `.ID`           | Task ID                                                          |
| `.Name`         | Task name                                                        |
| `.Image`        | Task image                                                       |
| `.Node`         | Node ID                                                          |
| `.DesiredState` | Desired state of the task (`running`, `shutdown`, or `accepted`) |
| `.CurrentState` | Current state of the task                                        |
| `.Error`        | Error                                                            |
| `.Ports`        | Task published ports                                             |

When using the `--format` option, the `stack ps` command will either output the data exactly as the template declares or, when using the `table` directive, includes column headers as well.

The following example uses a template without headers and outputs the `Name` and `Image` entries separated by a colon (`:`) for all tasks:

```console
$ docker stack ps --format "{{.Name}}: {{.Image}}" voting

voting_worker.1: dockersamples/examplevotingapp_worker:latest
voting_result.1: dockersamples/examplevotingapp_result:before
voting_vote.1: dockersamples/examplevotingapp_vote:before
voting_db.1: postgres:9.4
voting_redis.1: redis:alpine
voting_visualizer.1: dockersamples/visualizer:stable
voting_vote.2: dockersamples/examplevotingapp_vote:before
voting_redis.2: redis:alpine
```

To list all tasks in JSON format, use the `json` directive:

```console
$ docker stack ps --format json myapp
{"CurrentState":"Preparing 23 seconds ago","DesiredState":"Running","Error":"","ID":"2ufjubh79tn0","Image":"localstack/localstack:latest","Name":"myapp_localstack.1","Node":"docker-desktop","Ports":""}
{"CurrentState":"Running 20 seconds ago","DesiredState":"Running","Error":"","ID":"roee387ngf5r","Image":"redis:6.0.9-alpine3.12","Name":"myapp_redis.1","Node":"docker-desktop","Ports":""}
{"CurrentState":"Preparing 13 seconds ago","DesiredState":"Running","Error":"","ID":"yte68ouq7glh","Image":"postgres:13.2-alpine","Name":"myapp_repos-db.1","Node":"docker-desktop","Ports":""}
```

### [Do not map IDs to Names (--no-resolve)](#no-resolve)

The `--no-resolve` option shows IDs for task name, without mapping IDs to Names.

```console
$ docker stack ps --no-resolve voting

ID                  NAME                          IMAGE                                          NODE                        DESIRED STATE  CURRENT STATE            ERROR  PORTS
xim5bcqtgk1b        10z9fjfqzsxnezo4hb81p8mqg.1   dockersamples/examplevotingapp_worker:latest   qaqt4nrzo775jrx6detglho01   Running        Running 30 minutes ago
q7yik0ks1in6        hbxltua1na7mgqjnidldv5m65.1   dockersamples/examplevotingapp_result:before   mxpaef1tlh23s052erw88a4w5   Running        Running 30 minutes ago
rx5yo0866nfx        qyprtqw1g5nrki557i974ou1d.1   dockersamples/examplevotingapp_vote:before     kanqcxfajd1r16wlnqcblobmm   Running        Running 31 minutes ago
tz6j82jnwrx7        122f0xxngg17z52be7xspa72x.1   postgres:9.4                                   mxpaef1tlh23s052erw88a4w5   Running        Running 31 minutes ago
w48spazhbmxc        tg61x8myx563ueo3urmn1ic6m.1   redis:alpine                                   qaqt4nrzo775jrx6detglho01   Running        Running 31 minutes ago
6jj1m02freg1        8cqlyi444kzd3panjb7edh26v.1   dockersamples/visualizer:stable                mxpaef1tlh23s052erw88a4w5   Running        Running 31 minutes ago
kqgdmededccb        qyprtqw1g5nrki557i974ou1d.2   dockersamples/examplevotingapp_vote:before     qaqt4nrzo775jrx6detglho01   Running        Running 31 minutes ago
t72q3z038jeh        tg61x8myx563ueo3urmn1ic6m.2   redis:alpine                                   kanqcxfajd1r16wlnqcblobmm   Running        Running 31 minutes ago
```

### [Do not truncate output (--no-trunc)](#no-trunc)

When deploying a service, docker resolves the digest for the service's image, and pins the service to that digest. The digest is not shown by default, but is printed if `--no-trunc` is used. The `--no-trunc` option also shows the non-truncated task IDs, and error-messages, as can be seen below:

```console
$ docker stack ps --no-trunc voting

ID                          NAME                  IMAGE                                                                                                                 NODE   DESIRED STATE  CURREN STATE           ERROR  PORTS
xim5bcqtgk1bxqz91jzo4a1s5   voting_worker.1       dockersamples/examplevotingapp_worker:latest@sha256:3e4ddf59c15f432280a2c0679c4fc5a2ee5a797023c8ef0d3baf7b1385e9fed   node2  Running        Running 32 minutes ago
q7yik0ks1in6kv32gg6y6yjf7   voting_result.1       dockersamples/examplevotingapp_result:before@sha256:83b56996e930c292a6ae5187fda84dd6568a19d97cdb933720be15c757b7463   node1  Running        Running 32 minutes ago
rx5yo0866nfxc58zf4irsss6n   voting_vote.1         dockersamples/examplevotingapp_vote:before@sha256:8e64b182c87de902f2b72321c89b4af4e2b942d76d0b772532ff27ec4c6ebf6     node3  Running        Running 32 minutes ago
tz6j82jnwrx7n2offljp3mn03   voting_db.1           postgres:9.4@sha256:6046af499eae34d2074c0b53f9a8b404716d415e4a03e68bc1d2f8064f2b027                                   node1  Running        Running 32 minutes ago
w48spazhbmxcmbjfi54gs7x90   voting_redis.1        redis:alpine@sha256:9cd405cd1ec1410eaab064a1383d0d8854d1ef74a54e1e4a92fb4ec7bdc3ee7                                   node2  Running        Running 32 minutes ago
6jj1m02freg1n3z9n1evrzsbl   voting_visualizer.1   dockersamples/visualizer:stable@sha256:f924ad66c8e94b10baaf7bdb9cd491ef4e982a1d048a56a17e02bf5945401e5                node1  Running        Running 32 minutes ago
kqgdmededccbhz2wuc0e9hx7g   voting_vote.2         dockersamples/examplevotingapp_vote:before@sha256:8e64b182c87de902f2b72321c89b4af4e2b942d76d0b772532ff27ec4c6ebf6     node2  Running        Running 32 minutes ago
t72q3z038jehe1wbh9gdum076   voting_redis.2        redis:alpine@sha256:9cd405cd1ec1410eaab064a1383d0d8854d1ef74a54e1e4a92fb4ec7bdc3ee7                                   node3  Running        Running 32 minutes ago
```

### [Only display task IDs (-q, --quiet)](#quiet)

The `-q `or `--quiet` option only shows IDs of the tasks in the stack. This example outputs all task IDs of the `voting` stack:

```console
$ docker stack ps -q voting
xim5bcqtgk1b
q7yik0ks1in6
rx5yo0866nfx
tz6j82jnwrx7
w48spazhbmxc
6jj1m02freg1
kqgdmededccb
t72q3z038jeh
```

This option can be used to perform batch operations. For example, you can use the task IDs as input for other commands, such as `docker inspect`. The following example inspects all tasks of the `voting` stack:

```console
$ docker inspect $(docker stack ps -q voting)

[
    {
        "ID": "xim5bcqtgk1b1gk0krq1",
        "Version": {
<...>
```

----
url: https://docs.docker.com/ai/sandboxes/get-started/
----

# Get started with Docker Sandboxes

***

Table of contents

***

Docker Sandboxes run AI coding agents in isolated microVM sandboxes. Each sandbox gets its own Docker daemon, filesystem, and network — the agent can build containers, install packages, and modify files without touching your host system.

This page walks through a typical first session: installing the CLI, authenticating your agent, running a sandbox, isolating the agent's workspace, and cleaning up.

## [Prerequisites](#prerequisites)

* macOS Sonoma (version 14) or later
* Apple silicon

- 64-bit Intel or AMD (x86\_64)
- Windows 11
- Windows Hypervisor Platform enabled. Open an elevated PowerShell prompt (Run as Administrator) and run:
  ```powershell
  Enable-WindowsOptionalFeature -Online -FeatureName HypervisorPlatform -All
  ```

* Ubuntu 24.04 or later
* 64-bit Intel or AMD (x86\_64)
* KVM hardware virtualization supported and enabled by the CPU. If you're running inside a VM, nested virtualization must be turned on. Verify that KVM is available:
  ```console
  $ lsmod | grep kvm
  ```
  A working setup shows `kvm_intel` or `kvm_amd` in the output. If the output is empty, run `kvm-ok` for diagnostics. If KVM is unavailable, `sbx` will not start.
* Your user in the `kvm` group:
  ```console
  $ sudo usermod -aG kvm $USER
  ```
  Log out and back in (or run `newgrp kvm`) for the group change to take effect.

An API key or authentication method for the agent you want to use. Most agents require an API key for their model provider (Anthropic, OpenAI, Google, and others). See the [agent pages](https://docs.docker.com/ai/sandboxes/agents/) for provider-specific instructions.

Docker Desktop is not required to use `sbx`.

## [Install and sign in](#install-and-sign-in)

```console
$ brew install docker/tap/sbx
$ sbx login
```

```powershell
> winget install -h Docker.sbx
> sbx login
```

```console
$ curl -fsSL https://get.docker.com | sudo REPO_ONLY=1 sh
$ sudo apt-get install docker-sbx
$ sbx login
```

The first command adds Docker's `apt` repository to your system.

If you need to install `sbx` manually, download a binary directly from the [sbx-releases](https://github.com/docker/sbx-releases/releases) repository.

`sbx login` opens a browser for Docker OAuth. On first login (and after `sbx policy reset`), the CLI prompts you to choose a default network policy for your sandboxes:

```plaintext
Choose a default network policy:

     1. Open         — All network traffic allowed, no restrictions.
     2. Balanced     — Default deny, with common dev sites allowed.
     3. Locked Down  — All network traffic blocked unless you allow it.

Use ↑/↓ to navigate, Enter to select, or press 1–3.
```

**Balanced** is a good starting point — it permits traffic to common development services while blocking everything else. You can adjust individual rules later. See [Policies](https://docs.docker.com/ai/sandboxes/governance/local/) for a full description of each option.

> Note
>
> See the [FAQ](https://docs.docker.com/ai/sandboxes/faq/) for details on why sign-in is required and what happens with your data.

## [Authenticate your agent](#authenticate-your-agent)

Agents need credentials for their model provider. How you provide them depends on the agent.

For Claude Code with a Claude subscription (Max, Team, or Enterprise), no upfront setup is needed — use the `/login` command inside the sandbox to sign in with OAuth. The session token stays on your host and is injected by a proxy, not stored inside the sandbox.

For agents that use API keys (or if you prefer API key authentication for Claude Code), store the key before starting a sandbox:

```console
$ sbx secret set -g anthropic
```

This prompts for the secret value and stores it in your OS keychain. A proxy on your host injects the key into outbound API requests so it's never exposed inside the sandbox. See [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/) for details on scoping, supported services, and alternative methods.

To give the agent access to GitHub for creating pull requests or interacting with repositories:

```console
$ sbx secret set -g github -t "$(gh auth token)"
```

## [Run your first sandbox](#run-your-first-sandbox)

Pick a project directory and launch an agent with [`sbx run`](/reference/cli/sbx/run/):

```console
$ cd ~/my-project
$ sbx run --name my-sandbox claude
```

Replace `claude` with the agent you want to use — see [Agents](https://docs.docker.com/ai/sandboxes/agents/) for the full list.

The first run takes a little longer while the agent image is pulled. Subsequent runs reuse the cached image and start in seconds.

You can check what's running at any time:

```console
$ sbx ls
SANDBOX       AGENT    STATUS    PORTS   WORKSPACE
my-sandbox    claude   running           ~/my-project
```

You can also run `sbx` with no arguments to open an interactive dashboard. The dashboard shows your sandboxes with live status, lets you attach to agents, open shells, and manage network rules from one place. See [Interactive mode](https://docs.docker.com/ai/sandboxes/usage/#interactive-mode) for details.

## [Use clone mode](#use-clone-mode)

By default, the agent edits your working tree directly. To give the agent an isolated copy of your repository, use `--clone`. Because `--clone` is a create-time flag, remove the existing sandbox first:

```console
$ sbx rm my-sandbox
$ sbx run --clone --name my-sandbox claude
```

In clone mode, the sandbox keeps a private Git clone inside the microVM and mounts your host repository read-only. The sandbox exposes its clone as a `sandbox-<sandbox-name>` remote on your host, so you review the agent's commits the same way you'd fetch from any other remote:

```console
$ git fetch sandbox-my-sandbox
$ git log sandbox-my-sandbox/main
$ git diff main..sandbox-my-sandbox/main
```

When you're ready to create a pull request:

```console
$ git checkout -b my-feature sandbox-my-sandbox/main
$ git push -u origin my-feature
$ gh pr create
```

For Claude Code, pair `--clone` with the [agents view](https://docs.docker.com/ai/sandboxes/agents/claude-code/#agents-view) to dispatch tasks to subagents that each work on their own branch inside the same sandbox:

```console
$ sbx run --clone --name my-sandbox claude -- agents
```

Clone mode is especially useful when running multiple agents on the same repository in parallel — each works in its own isolated clone without touching your host working tree. See [Clone mode](https://docs.docker.com/ai/sandboxes/usage/#clone-mode) for the full workflow, including how to have the agent commit to a dedicated branch.

## [Manage network access](#manage-network-access)

Your network policy controls what the sandbox can reach. If the agent fails to connect to an API or service, it's likely blocked by the policy.

Check which rules are in effect:

```console
$ sbx policy ls
```

To allow a specific host:

```console
$ sbx policy allow network registry.npmjs.org
```

With **Locked Down**, even your model provider API is blocked unless you explicitly allow it. With **Balanced**, common development services are permitted by default. See [Policies](https://docs.docker.com/ai/sandboxes/governance/local/) for the full rule set and how to customize it.

## [Clean up](#clean-up)

Sandboxes persist after the agent exits. To stop a sandbox without deleting it:

```console
$ sbx stop my-sandbox
```

Installed packages, Docker images, and configuration changes are preserved across restarts. When you're done with a sandbox, remove it to reclaim disk space:

```console
$ sbx rm my-sandbox
```

Removing a sandbox deletes everything inside it — installed packages, Docker images, and the in-sandbox Git clone if you used clone mode. Files in your host working tree are unaffected.

## [Next steps](#next-steps)

* [Usage guide](https://docs.docker.com/ai/sandboxes/usage/) — sandbox management, reconnecting, multiple workspaces, port forwarding, and more
* [Agents](https://docs.docker.com/ai/sandboxes/agents/) — supported agents and configuration
* [Customize](https://docs.docker.com/ai/sandboxes/customize/) — build reusable templates or declare capabilities with kits
* [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/) — credential storage and management
* [Workspace isolation](https://docs.docker.com/ai/sandboxes/security/isolation/#workspace-isolation) — what the agent can affect on your host, and how to review changes
* [Governance](https://docs.docker.com/ai/sandboxes/governance/) — control outbound access

----
url: https://docs.docker.com/enterprise/security/roles-and-permissions/core-roles/
----

# Core roles

***

Table of contents

***

For: Administrators

Core roles are Docker's built-in roles with predefined permission sets. This page provides an overview of Docker's core roles and permissions for each role.

## [What are core roles?](#what-are-core-roles)

Docker organizations have three core roles:

* **Member**: Non-administrative role with basic access. Members can view other organization members and pull images from repositories they have access to.
* **Editor**: Partial administrative access. Editors can create, edit, and delete repositories. They can also manage team permissions for repositories.
* **Owner**: Full administrative access. Owners can manage all organization settings, including repositories, teams, members, billing, and security features.

A company owner has the same organization management permissions as an organization owner, but there are some content and registry permissions that company owners don't have (for example, repository pull/push). For more information, see [Company overview](https://docs.docker.com/admin/company/).

### [Content and registry permissions](#content-and-registry-permissions)

These permissions apply organization-wide.

| Permission                                            | Member | Editor | Owner |
| ----------------------------------------------------- | ------ | ------ | ----- |
| Explore images and extensions                         | ✅      | ✅      | ✅     |
| Star, favorite, vote, and comment on content          | ✅      | ✅      | ✅     |
| Pull images                                           | ✅      | ✅      | ✅     |
| Create and publish an extension                       | ✅      | ✅      | ✅     |
| Become a Verified, Official, or Open Source publisher | ❌      | ❌      | ✅     |
| Edit and delete publisher repository logos            | ❌      | ✅      | ✅     |
| Configure DVP analytics settings                      | ❌      | ✅      | ✅     |
| Observe content engagement as a publisher             | ❌      | ❌      | ✅     |
| Create public and private repositories                | ❌      | ✅      | ✅     |
| Disable public repositories                           | ❌      | ✅      | ✅     |
| Edit and delete repositories                          | ❌      | ✅      | ✅     |
| Manage tags                                           | ❌      | ✅      | ✅     |
| View repository activity                              | ❌      | ❌      | ✅     |
| Set up Automated builds                               | ❌      | ❌      | ✅     |
| Edit build settings                                   | ❌      | ❌      | ✅     |
| View teams                                            | ✅      | ✅      | ✅     |
| Assign team permissions to repositories               | ❌      | ✅      | ✅     |

You can grant repository permissions to members beyond their organization role:

* Role permissions: Applied organization-wide (member or editor)
* Team permissions: Additional permissions for specific repositories

To extend access to private repositories, assign a custom role to organization members or configure team permissions.

### [Organization management permissions](#organization-management-permissions)

| Permission                                                        | Member | Editor | Owner |
| ----------------------------------------------------------------- | ------ | ------ | ----- |
| Create teams                                                      | ❌      | ❌      | ✅     |
| Manage teams (including delete)                                   | ❌      | ❌      | ✅     |
| Configure the organization's settings (including linked services) | ❌      | ❌      | ✅     |
| Add organizations to a company                                    | ❌      | ❌      | ✅     |
| Invite members                                                    | ❌      | ❌      | ✅     |
| Manage members                                                    | ❌      | ❌      | ✅     |
| Manage member roles and permissions                               | ❌      | ❌      | ✅     |
| View member activity                                              | ❌      | ❌      | ✅     |
| Export and reporting                                              | ❌      | ❌      | ✅     |
| Image Access Management                                           | ❌      | ❌      | ✅     |
| Registry Access Management                                        | ❌      | ❌      | ✅     |
| Namespace access control                                          | ❌      | ❌      | ✅     |
| Set up Single Sign-On (SSO) and SCIM                              | ❌      | ❌      | ✅ \*  |
| Require Docker Desktop sign-in                                    | ❌      | ❌      | ✅ \*  |
| Manage billing information (for example, billing address)         | ❌      | ❌      | ✅     |
| Manage payment methods (for example, credit card or invoice)      | ❌      | ❌      | ✅     |
| View billing history                                              | ❌      | ❌      | ✅     |
| Manage subscriptions                                              | ❌      | ❌      | ✅     |
| Manage seats                                                      | ❌      | ❌      | ✅     |
| Upgrade and downgrade plans                                       | ❌      | ❌      | ✅     |

> Tip
>
> If you want more granular access control, you can [upgrade to a Docker Business plan](https://www.docker.com/pricing?ref=Docs\&refAction=DocsEnterpriseCoreRoles) for custom roles and advanced permissions.

*\* If not part of a company*

### [Docker Scout permissions](#docker-scout-permissions)

| Permission                                            | Member | Editor | Owner |
| ----------------------------------------------------- | ------ | ------ | ----- |
| View and compare analysis results                     | ✅      | ✅      | ✅     |
| Upload analysis records                               | ✅      | ✅      | ✅     |
| Activate and deactivate Docker Scout for a repository | ❌      | ✅      | ✅     |
| Create environments                                   | ❌      | ❌      | ✅     |
| Manage registry integrations                          | ❌      | ❌      | ✅     |

### [Docker Build Cloud permissions](#docker-build-cloud-permissions)

| Permission                 | Member | Editor | Owner |
| -------------------------- | ------ | ------ | ----- |
| Use a cloud builder        | ✅      | ✅      | ✅     |
| Create and remove builders | ✅      | ✅      | ✅     |
| Configure builder settings | ✅      | ✅      | ✅     |
| Buy minutes                | ❌      | ❌      | ✅     |
| Manage subscription        | ❌      | ❌      | ✅     |

----
url: https://docs.docker.com/reference/samples/portainer/
----

# Portainer samples

| Name                                                                         | Description               |
| ---------------------------------------------------------------------------- | ------------------------- |
| [Portainer](https://github.com/docker/awesome-compose/tree/master/portainer) | A sample Portainer setup. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/build/policies/usage/
----

# Using build policies

***

Table of contents

***

Build policies validate inputs before builds execute. This guide covers how to develop policies iteratively and apply them to real builds with `docker buildx build` and `docker buildx bake`.

## [Prerequisites](#prerequisites)

* Buildx 0.31.0 or later - Check your version: `docker buildx version`
* BuildKit 0.26.0 or later - Verify with: `docker buildx inspect --bootstrap`

If you're using Docker Desktop, ensure you're on a version that includes these updates.

## [Policy development workflow](#policy-development-workflow)

Buildx automatically loads policies that match your Dockerfile name. When you build with `Dockerfile`, Buildx looks for `Dockerfile.rego` in the same directory. For a file named `app.Dockerfile`, it looks for `app.Dockerfile.rego`. See the [Advanced: Policy configuration](#advanced-policy-configuration) section for configuration options and manual policy loading.

Writing policies is an iterative process:

1. Start with a basic deny-all policy.
2. Build with debug logging to see what inputs your Dockerfile uses.
3. Add rules to allow specific sources based on the debug output.
4. Test and refine.

### [Viewing inputs from your Dockerfile](#viewing-inputs-from-your-dockerfile)

To see the inputs that your Dockerfile references (images, Git repos, HTTP downloads), build with debug logging:

```console
$ docker buildx build --progress=plain --policy log-level=debug .
```

Example output for an image source:

```text
#1 0.010 checking policy for source docker-image://alpine:3.19 (linux/arm64)
#1 0.011 policy input: {
#1 0.011   "env": {
#1 0.011     "filename": "."
#1 0.011   },
#1 0.011   "image": {
#1 0.011     "ref": "docker.io/library/alpine:3.19",
#1 0.011     "host": "docker.io",
#1 0.011     "repo": "alpine",
#1 0.011     "tag": "3.19",
#1 0.011     "platform": "linux/arm64"
#1 0.011   }
#1 0.011 }
#1 0.011 unknowns for policy evaluation: [input.image.checksum input.image.labels ...]
#1 0.012 policy decision for source docker-image://alpine:3.19: ALLOW
```

This shows the complete input structure, which fields are unresolved, and the policy decision for each source. See [Input reference](https://docs.docker.com/build/policies/inputs/) for all available fields.

### [Testing policies with policy eval](#testing-policies-with-policy-eval)

Use [`docker buildx policy eval`](/reference/cli/docker/buildx/policy/eval/) to test whether your policy allows a specific source without running a full build.

Note: `docker buildx policy eval` tests the source specified as the argument. It doesn't parse your Dockerfile to evaluate all inputs - for that, [build with --progress=plain](#viewing-inputs-from-your-dockerfile).

Test if your policy allows the local context:

```console
$ docker buildx policy eval .
```

No output means the policy allowed the source. If denied, you see:

```console
ERROR: policy denied
```

Test other sources:

```console
$ docker buildx policy eval https://example.com              # Test HTTP
$ docker buildx policy eval https://github.com/org/repo.git  # Test Git
```

By default, `--print` shows reference information parsed from the source string (like `repo`, `tag`, `host`) without fetching from registries. To inspect metadata that requires fetching the source (like `labels`, `checksum`, or `hasProvenance`), specify which fields to fetch with `--fields`:

```console
$ docker buildx policy eval --print --fields image.labels docker-image://alpine:3.19
```

Multiple fields can be specified as a comma-separated list.

### [Iterative development example](#iterative-development-example)

Here's a practical workflow for developing policies:

1. Start with basic deny-all policy:

   Dockerfile.rego

   ```rego
   package docker

   default allow := false

   allow if input.local

   decision := {"allow": allow}
   ```

2. Build with debug logging to see what inputs your Dockerfile uses:

   ```console
   $ docker buildx build --progress=plain --policy log-level=debug .
   ```

   The output shows the denied image and its input structure:

   ```text
   #1 0.026 checking policy for source docker-image://docker.io/library/alpine:3.19
   #1 0.027 policy input: {
   #1 0.027   "image": {
   #1 0.027     "repo": "alpine",
   #1 0.027     "tag": "3.19",
   #1 0.027     ...
   #1 0.027   }
   #1 0.027 }
   #1 0.028 policy decision for source docker-image://alpine:3.19: DENY
   #1 ERROR: source "docker-image://alpine:3.19" not allowed by policy
   ```

3. Add a rule allowing the alpine image:

   ```rego
   allow if {
       input.image.repo == "alpine"
   }
   ```

4. Build again to verify the policy works:

   ```console
   $ docker buildx build .
   ```

If it fails, see [Debugging](https://docs.docker.com/build/policies/debugging/) for troubleshooting guidance.

## [Using policies with `docker build`](#using-policies-with-docker-build)

Once you've developed and tested your policy, apply it to real builds.

### [Basic usage](#basic-usage)

Create a policy alongside your Dockerfile:

Dockerfile

```dockerfile
FROM alpine:3.19
RUN echo "hello"
```

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local

allow if {
    input.image.repo == "alpine"
}

decision := {"allow": allow}
```

Build normally:

```console
$ docker buildx build .
```

Buildx loads the policy automatically and validates the `alpine:3.19` image before building.

### [Build with different Dockerfile names](#build-with-different-dockerfile-names)

Specify the Dockerfile with `-f`:

```console
$ docker buildx build -f app.Dockerfile .
```

Buildx looks for `app.Dockerfile.rego` in the same directory.

### [Build with manual policy](#build-with-manual-policy)

Add an extra policy to the automatic one:

```console
$ docker buildx build --policy filename=extra-checks.rego .
```

Both `Dockerfile.rego` (automatic) and `extra-checks.rego` (manual) must pass.

### [Build without automatic policy](#build-without-automatic-policy)

Use only your specified policy:

```console
$ docker buildx build --policy reset=true,filename=strict.rego .
```

## [Using policies with bake](#using-policies-with-bake)

[Bake](/build/bake/) supports automatic policy loading just like `docker buildx build`. Place `Dockerfile.rego` alongside your Dockerfile and run:

```console
$ docker buildx bake
```

### [Manual policy in bake files](#manual-policy-in-bake-files)

Specify additional policies in your `docker-bake.hcl`:

docker-bake.hcl

```hcl
target "default" {
  dockerfile = "Dockerfile"
  policy = ["extra.rego"]
}
```

The `policy` attribute takes a list of policy files. Bake loads these in addition to the automatic `Dockerfile.rego` (if it exists).

### [Multiple policies in bake](#multiple-policies-in-bake)

docker-bake.hcl

```hcl
target "webapp" {
  dockerfile = "Dockerfile"
  policy = [
    "shared/base-policy.rego",
    "security/image-signing.rego"
  ]
}
```

All policies must pass for the target to build successfully.

### [Different policies per target](#different-policies-per-target)

Apply different validation rules to different targets:

docker-bake.hcl

```hcl
target "development" {
  dockerfile = "dev.Dockerfile"
  policy = ["policies/permissive.rego"]
}

target "production" {
  dockerfile = "prod.Dockerfile"
  policy = ["policies/strict.rego", "policies/signing-required.rego"]
}
```

Build with the appropriate target:

```console
$ docker buildx bake development  # Uses permissive policy
$ docker buildx bake production   # Uses strict policies
```

### [Bake with policy options](#bake-with-policy-options)

Currently, bake doesn't support policy options (reset, strict, disabled) in the HCL file. Use command-line flags instead:

```console
$ docker buildx bake --policy disabled=true production
```

## [Testing in CI/CD](#testing-in-cicd)

Validate policies in continuous integration by running builds with the `--policy` flag. For unit testing policies before running builds, see [Test build policies](https://docs.docker.com/build/policies/testing/).

Test policies during CI builds:

.github/workflows/test-policies.yml

```yaml
name: Test Build Policies
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: docker/setup-buildx-action@v4
      - name: Test build with policy
        run: docker buildx build --policy strict=true .
```

This ensures policy changes don't break builds and that new rules work as intended. The `strict=true` flag fails the build if policies aren't loaded (for example, if the BuildKit instance used by the build is too old and doesn't support policies).

## [Advanced: Policy configuration](#advanced-policy-configuration)

This section covers advanced policy loading mechanisms and configuration options.

### [Automatic policy loading](#automatic-policy-loading)

Buildx automatically loads policies that match your Dockerfile name. When you build with `Dockerfile`, Buildx looks for `Dockerfile.rego` in the same directory. For a file named `app.Dockerfile`, it looks for `app.Dockerfile.rego`.

```text
project/
├── Dockerfile
├── Dockerfile.rego          # Loaded automatically for Dockerfile
├── app.Dockerfile
├── app.Dockerfile.rego      # Loaded automatically for app.Dockerfile
└── src/
```

This automatic loading means you don't need command-line flags in most cases. Create the policy file alongside your Dockerfile and build:

```console
$ docker buildx build .
```

Buildx detects `Dockerfile.rego` and evaluates it before running the build.

> Note
>
> Policy files must be in the same directory as the Dockerfile they validate. Buildx doesn't search parent directories or subdirectories.

### [When policies don't load](#when-policies-dont-load)

If buildx can't find a matching `.rego` file, the build proceeds without policy evaluation. To require policies and fail if none are found, use strict mode:

```console
$ docker buildx build --policy strict=true .
```

This fails the build if no policy loads or if the BuildKit daemon doesn't support policies.

### [Manual policy configuration](#manual-policy-configuration)

The `--policy` flag lets you specify additional policies, override automatic loading, or control policy behavior.

Basic syntax:

```console
$ docker buildx build --policy filename=custom.rego .
```

This loads `custom.rego` in addition to the automatic `Dockerfile.rego` (if it exists).

Multiple policies:

```console
$ docker buildx build --policy filename=policy1.rego --policy filename=policy2.rego .
```

All policies must pass for the build to succeed. Use this to enforce layered requirements (base policy + project-specific rules).

Available options:

| Option              | Description                                                                                                           | Example                |
| ------------------- | --------------------------------------------------------------------------------------------------------------------- | ---------------------- |
| `filename=<path>`   | Load policy from specified file                                                                                       | `filename=custom.rego` |
| `reset=true`        | Ignore automatic policies, use only specified ones                                                                    | `reset=true`           |
| `disabled=true`     | Disable all policy evaluation                                                                                         | `disabled=true`        |
| `strict=true`       | Fail if BuildKit doesn't support policies                                                                             | `strict=true`          |
| `log-level=<level>` | Control policy logging (error, warn, info, debug, none). Use `debug` to see complete input JSON and unresolved fields | `log-level=debug`      |

Combine options with commas:

```console
$ docker buildx build --policy filename=extra.rego,strict=true .
```

### [Exploring sources with policy eval](#exploring-sources-with-policy-eval)

The `docker buildx policy eval` command lets you quickly explore and test sources without running a build.

#### [Inspect input structure with --print](#inspect-input-structure-with---print)

Use `--print` to see the input structure for any source without running policy evaluation:

```console
$ docker buildx policy eval --print https://github.com/moby/buildkit.git
```

```json
{
  "git": {
    "schema": "https",
    "host": "github.com",
    "remote": "https://github.com/moby/buildkit.git"
  }
}
```

Test different source types:

```console
# HTTP downloads
$ docker buildx policy eval --print https://releases.hashicorp.com/terraform/1.5.0/terraform.zip

# Images (requires docker-image:// prefix)
$ docker buildx policy eval --print docker-image://alpine:3.19

# Local context
$ docker buildx policy eval --print .
```

Shows information parsed from the source without fetching. Use `--fields` to fetch specific metadata (see [above](#testing-policies-with-policy-eval)).

#### [Test with specific policy files](#test-with-specific-policy-files)

The `--filename` flag specifies which policy file to load by providing the base Dockerfile name (without the `.rego` extension). This is useful for testing sources against policies associated with different Dockerfiles.

For example, to test a source against the policy for `app.Dockerfile`:

```console
$ docker buildx policy eval --filename app.Dockerfile .
```

This loads `app.Dockerfile.rego` and tests whether it allows the source `.` (the local directory). The flag defaults to `Dockerfile` if not specified.

Test different sources against your policy:

```console
$ docker buildx policy eval --filename app.Dockerfile https://github.com/org/repo.git
$ docker buildx policy eval --filename app.Dockerfile docker-image://alpine:3.19
```

### [Reset automatic loading](#reset-automatic-loading)

To use only your specified policies and ignore automatic `.rego` files:

```console
$ docker buildx build --policy reset=true,filename=custom.rego .
```

This skips `Dockerfile.rego` and loads only `custom.rego`.

### [Disable policies temporarily](#disable-policies-temporarily)

Disable policy evaluation for testing or emergencies:

```console
$ docker buildx build --policy disabled=true .
```

The build proceeds without any policy checks. Use this carefully - you're bypassing security controls.

## [Next steps](#next-steps)

* Write unit tests for your policies: [Test build policies](https://docs.docker.com/build/policies/testing/)
* Debug policy failures: [Debugging](https://docs.docker.com/build/policies/debugging/)
* Browse working examples: [Example policies](https://docs.docker.com/build/policies/examples/)
* Reference all input fields: [Input reference](https://docs.docker.com/build/policies/inputs/)

----
url: https://docs.docker.com/guides/genai-video-bot/
----

[GenAI video transcription and chat](https://docs.docker.com/guides/genai-video-bot/)

Learn how to build and deploy a generative AI video analysis and transcription bot using Docker.

AI

20 minutes

[« Back to all guides](/guides/)

# GenAI video transcription and chat

***

Table of contents

***

## [Overview](#overview)

This guide presents a project on video transcription and analysis using a set of technologies related to the [GenAI Stack](https://www.docker.com/blog/introducing-a-new-genai-stack/).

The project showcases the following technologies:

* [Docker and Docker Compose](#docker-and-docker-compose)
* [OpenAI](#openai-api)
* [Whisper](#whisper)
* [Embeddings](#embeddings)
* [Chat completions](#chat-completions)
* [Pinecone](#pinecone)
* [Retrieval-Augmented Generation](#retrieval-augmented-generation)

> **Acknowledgment**
>
> This guide is a community contribution. Docker would like to thank [David Cardozo](https://www.davidcardozo.com/) for his contribution to this guide.

## [Prerequisites](#prerequisites)

* You have an [OpenAI API Key](https://platform.openai.com/api-keys).

  > Note
  >
  > OpenAI is a third-party hosted service and [charges](https://openai.com/pricing) may apply.

* You have a [Pinecone API Key](https://app.pinecone.io/).

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/). Docker adds new features regularly and some parts of this guide may work only with the latest version of Docker Desktop.

* You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## [About the application](#about-the-application)

The application is a chatbot that can answer questions from a video. In addition, it provides timestamps from the video that can help you find the sources used to answer your question.

## [Get and run the application](#get-and-run-the-application)

1. Clone the sample application's repository. In a terminal, run the following command.

   ```console
   $ git clone https://github.com/Davidnet/docker-genai.git
   ```

   The project contains the following directories and files:

   ```text
   ├── docker-genai/
   │ ├── docker-bot/
   │ ├── yt-whisper/
   │ ├── .env.example
   │ ├── .gitignore
   │ ├── LICENSE
   │ ├── README.md
   │ └── docker-compose.yaml
   ```

2. Specify your API keys. In the `docker-genai` directory, create a text file called `.env` and specify your API keys inside. The following is the contents of the `.env.example` file that you can refer to as an example.

   ```text
   #----------------------------------------------------------------------------
   # OpenAI
   #----------------------------------------------------------------------------
   OPENAI_TOKEN=your-api-key # Replace your-api-key with your personal API key

   #----------------------------------------------------------------------------
   # Pinecone
   #----------------------------------------------------------------------------
   PINECONE_TOKEN=your-api-key # Replace your-api-key with your personal API key
   ```

3. Build and run the application. In a terminal, change directory to your `docker-genai` directory and run the following command.

   ```console
   $ docker compose up --build
   ```

   Docker Compose builds and runs the application based on the services defined in the `docker-compose.yaml` file. When the application is running, you'll see the logs of 2 services in the terminal.

   In the logs, you'll see the services are exposed on ports `8503` and `8504`. The two services are complimentary to each other.

   The `yt-whisper` service is running on port `8503`. This service feeds the Pinecone database with videos that you want to archive in your knowledge database. The following section explores this service.

## [Using the yt-whisper service](#using-the-yt-whisper-service)

The yt-whisper service is a YouTube video processing service that uses the OpenAI Whisper model to generate transcriptions of videos and stores them in a Pinecone database. The following steps show how to use the service.

1. Open a browser and access the yt-whisper service at <http://localhost:8503>.

2. Once the application appears, in the **Youtube URL** field specify a Youtube video URL and select **Submit**. The following example uses <https://www.youtube.com/watch?v=yaQZFhrW0fU>.

   The yt-whisper service downloads the audio of the video, uses Whisper to transcribe it into a WebVTT (`*.vtt`) format (which you can download), then uses the text-embedding-3-small model to create embeddings, and finally uploads those embeddings in to the Pinecone database.

   After processing the video, a video list appears in the web app that informs you which videos have been indexed in Pinecone. It also provides a button to download the transcript.

   You can now access the dockerbot service on port `8504` and ask questions about the videos.

## [Using the dockerbot service](#using-the-dockerbot-service)

The dockerbot service is a question-answering service that leverages both the Pinecone database and an AI model to provide responses. The following steps show how to use the service.

> Note
>
> You must process at least one video via the [yt-whisper service](#using-the-yt-whisper-service) before using the dockerbot service.

1. Open a browser and access the service at <http://localhost:8504>.

2. In the **What do you want to know about your videos?** text box, ask the Dockerbot a question about a video that was processed by the yt-whisper service. The following example asks the question, "What is a sugar cookie?". The answer to that question exists in the video processed in the previous example, <https://www.youtube.com/watch?v=yaQZFhrW0fU>.

   In this example, the Dockerbot answers the question and provides links to the video with timestamps, which may contain more information about the answer.

   The dockerbot service takes the question, turns it into an embedding using the text-embedding-3-small model, queries the Pinecone database to find similar embeddings, and then passes that context into the gpt-4-turbo-preview to generate an answer.

3. Select the first link to see what information it provides. Based on the previous example, select <https://www.youtube.com/watch?v=yaQZFhrW0fU&t=553s>.

   In the example link, you can see that the section of video perfectly answers the question, "What is a sugar cookie?".

## [Explore the application architecture](#explore-the-application-architecture)

The following image shows the application's high-level service architecture, which includes:

* yt-whisper: A local service, ran by Docker Compose, that interacts with the remote OpenAI and Pinecone services.
* dockerbot: A local service, ran by Docker Compose, that interacts with the remote OpenAI and Pinecone services.
* OpenAI: A remote third-party service.
* Pinecone: A remote third-party service.

## [Explore the technologies used and their role](#explore-the-technologies-used-and-their-role)

### [Docker and Docker Compose](#docker-and-docker-compose)

The application uses Docker to run the application in containers, providing a consistent and isolated environment for running it. This means the application will operate as intended within its Docker containers, regardless of the underlying system differences. To learn more about Docker, see the [Getting started overview](https://docs.docker.com/get-started/introduction/).

Docker Compose is a tool for defining and running multi-container applications. Compose makes it easy to run this application with a single command, `docker compose up`. For more details, see the [Compose overview](https://docs.docker.com/compose/).

### [OpenAI API](#openai-api)

The OpenAI API provides an LLM service that's known for its cutting-edge AI and machine learning technologies. In this application, OpenAI's technology is used to generate transcriptions from audio (using the Whisper model) and to create embeddings for text data, as well as to generate responses to user queries (using GPT and chat completions). For more details, see [openai.com](https://openai.com/product).

### [Whisper](#whisper)

Whisper is an automatic speech recognition system developed by OpenAI, designed to transcribe spoken language into text. In this application, Whisper is used to transcribe the audio from YouTube videos into text, enabling further processing and analysis of the video content. For more details, see [Introducing Whisper](https://openai.com/research/whisper).

### [Embeddings](#embeddings)

Embeddings are numerical representations of text or other data types, which capture their meaning in a way that can be processed by machine learning algorithms. In this application, embeddings are used to convert video transcriptions into a vector format that can be queried and analyzed for relevance to user input, facilitating efficient search and response generation in the application. For more details, see OpenAI's [Embeddings](https://platform.openai.com/docs/guides/embeddings) documentation.

### [Chat completions](#chat-completions)

Chat completion, as utilized in this application through OpenAI's API, refers to the generation of conversational responses based on a given context or prompt. In the application, it is used to provide intelligent, context-aware answers to user queries by processing and integrating information from video transcriptions and other inputs, enhancing the chatbot's interactive capabilities. For more details, see OpenAI's [Chat Completions API](https://platform.openai.com/docs/guides/text-generation) documentation.

### [Pinecone](#pinecone)

Pinecone is a vector database service optimized for similarity search, used for building and deploying large-scale vector search applications. In this application, Pinecone is employed to store and retrieve the embeddings of video transcriptions, enabling efficient and relevant search functionality within the application based on user queries. For more details, see [pincone.io](https://www.pinecone.io/).

### [Retrieval-Augmented Generation](#retrieval-augmented-generation)

Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with a language model to generate responses based on retrieved documents or data. In RAG, the system retrieves relevant information (in this case, via embeddings from video transcriptions) and then uses a language model to generate responses based on this retrieved data. For more details, see OpenAI's cookbook for [Retrieval Augmented Generative Question Answering with Pinecone](https://cookbook.openai.com/examples/vector_databases/pinecone/gen_qa).

## [Next steps](#next-steps)

Explore how to [create a PDF bot application](https://docs.docker.com/guides/genai-pdf-bot/) using generative AI, or view more GenAI samples in the [GenAI Stack](https://github.com/docker/genai-stack) repository.

----
url: https://docs.docker.com/scout/integrations/ci/jenkins/
----

# Integrate Docker Scout with Jenkins

***

***

You can add the following stage and steps definition to a `Jenkinsfile` to run Docker Scout as part of a Jenkins pipeline. The pipeline needs a `DOCKER_HUB` credential containing the username and password for authenticating to Docker Hub. It also needs an environment variable defined for the image and tag.

```groovy
pipeline {
    agent {
        // Agent details
    }

    environment {
        DOCKER_HUB = credentials('jenkins-docker-hub-credentials')
        IMAGE_TAG  = 'myorg/scout-demo-service:latest'
    }

    stages {
        stage('Analyze image') {
            steps {
                // Install Docker Scout
                sh 'curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /usr/local/bin'

                // Log into Docker Hub
                sh 'echo $DOCKER_HUB_PSW | docker login -u $DOCKER_HUB_USR --password-stdin'

                // Analyze and fail on critical or high vulnerabilities
                sh 'docker scout cves $IMAGE_TAG --exit-code --only-severity critical,high'
            }
        }
    }
}
```

This installs Docker Scout, logs into Docker Hub, and then runs Docker Scout to generate a CVE report for an image and tag. It only shows critical or high-severity vulnerabilities.

> Note
>
> If you're seeing a `permission denied` error related to the image cache, try setting the [`DOCKER_SCOUT_CACHE_DIR`](https://docs.docker.com/scout/how-tos/configure-cli/) environment variable to a writable directory. Or alternatively, disable local caching entirely with `DOCKER_SCOUT_NO_CACHE=true`.

----
url: https://docs.docker.com/ai/model-runner/configuration/
----

# Configuration options

***

Table of contents

***

Docker Model Runner provides several configuration options to tune model behavior, memory usage, and inference performance. This guide covers the key settings and how to apply them.

## [Context size (context length)](#context-size-context-length)

The context size determines the maximum number of tokens a model can process in a single request, including both the input prompt and generated output. This is one of the most important settings affecting memory usage and model capabilities.

### [Default context size](#default-context-size)

By default, Docker Model Runner uses a context size that balances capability with resource efficiency:

| Engine    | Default behavior                              |
| --------- | --------------------------------------------- |
| llama.cpp | 4096 tokens                                   |
| vLLM      | Uses the model's maximum trained context size |

> Note
>
> The actual default varies by model. Most models support between 2,048 and 8,192 tokens by default. Some newer models support 32K, 128K, or even larger contexts.

### [Configure context size](#configure-context-size)

You can adjust context size per model using the `docker model configure` command:

```console
$ docker model configure --context-size 8192 ai/qwen2.5-coder
```

Or in a Compose file:

```yaml
models:
  llm:
    model: ai/qwen2.5-coder
    context_size: 8192
```

### [Context size guidelines](#context-size-guidelines)

| Context size | Typical use case                          | Memory impact |
| ------------ | ----------------------------------------- | ------------- |
| 2,048        | Simple queries, short code snippets       | Low           |
| 4,096        | Standard conversations, medium code files | Moderate      |
| 8,192        | Long conversations, larger code files     | Higher        |
| 16,384+      | Extended documents, multi-file context    | High          |

> Important
>
> Larger context sizes require more memory (RAM/VRAM). If you experience out-of-memory errors, reduce the context size. As a rough guide, each additional 1,000 tokens requires approximately 100-500 MB of additional memory, depending on the model size.

### [Check a model's maximum context](#check-a-models-maximum-context)

To see a model's configuration including context size:

```console
$ docker model inspect ai/qwen2.5-coder
```

> Note
>
> The `docker model inspect` command shows the model's maximum supported context length (e.g., `gemma3.context_length`), not the configured context size. The configured context size is what you set with `docker model configure --context-size` and represents the actual limit used during inference, which should be less than or equal to the model's maximum supported context length.

## [Runtime flags](#runtime-flags)

Runtime flags let you pass parameters directly to the underlying inference engine. This provides fine-grained control over model behavior.

### [Using runtime flags](#using-runtime-flags)

Runtime flags can be provided through multiple mechanisms:

#### [Using Docker Compose](#using-docker-compose)

In a Compose file:

```yaml
models:
  llm:
    model: ai/qwen2.5-coder
    context_size: 4096
    runtime_flags:
      - "--temp"
      - "0.7"
      - "--top-p"
      - "0.9"
```

#### [Using Command Line](#using-command-line)

With the `docker model configure` command:

```console
$ docker model configure ai/qwen2.5-coder -- --temp 0.7 --top-p 0.9
```

### [Common llama.cpp parameters](#common-llamacpp-parameters)

These are the most commonly used llama.cpp parameters. You don't need to look up the llama.cpp documentation for typical use cases.

#### [Sampling parameters](#sampling-parameters)

| Flag               | Description                                                                  | Default | Range   |
| ------------------ | ---------------------------------------------------------------------------- | ------- | ------- |
| `--temp`           | Temperature for sampling. Lower = more deterministic, higher = more creative | 0.8     | 0.0-2.0 |
| `--top-k`          | Limit sampling to top K tokens. Lower = more focused                         | 40      | 1-100   |
| `--top-p`          | Nucleus sampling threshold. Lower = more focused                             | 0.9     | 0.0-1.0 |
| `--min-p`          | Minimum probability threshold                                                | 0.05    | 0.0-1.0 |
| `--repeat-penalty` | Penalty for repeating tokens                                                 | 1.1     | 1.0-2.0 |

**Example: Deterministic output (for code generation)**

```yaml
runtime_flags:
  - "--temp"
  - "0"
  - "--top-k"
  - "1"
```

**Example: Creative output (for storytelling)**

```yaml
runtime_flags:
  - "--temp"
  - "1.2"
  - "--top-p"
  - "0.95"
```

#### [Performance parameters](#performance-parameters)

| Flag              | Description                      | Default | Notes                                      |
| ----------------- | -------------------------------- | ------- | ------------------------------------------ |
| `--threads`       | CPU threads for generation       | Auto    | Set to number of performance cores         |
| `--threads-batch` | CPU threads for batch processing | Auto    | Usually same as `--threads`                |
| `--batch-size`    | Batch size for prompt processing | 512     | Higher = faster prompt processing          |
| `--mlock`         | Lock model in memory             | Off     | Prevents swapping, requires sufficient RAM |
| `--no-mmap`       | Disable memory mapping           | Off     | May improve performance on some systems    |

**Example: Optimized for multi-core CPU**

```yaml
runtime_flags:
  - "--threads"
  - "8"
  - "--batch-size"
  - "1024"
```

#### [GPU parameters](#gpu-parameters)

| Flag             | Description                | Default                | Notes                           |
| ---------------- | -------------------------- | ---------------------- | ------------------------------- |
| `--n-gpu-layers` | Layers to offload to GPU   | All (if GPU available) | Reduce if running out of VRAM   |
| `--main-gpu`     | GPU to use for computation | 0                      | For multi-GPU systems           |
| `--split-mode`   | How to split across GPUs   | layer                  | Options: `none`, `layer`, `row` |

**Example: Partial GPU offload (limited VRAM)**

```yaml
runtime_flags:
  - "--n-gpu-layers"
  - "20"
```

#### [Advanced parameters](#advanced-parameters)

| Flag                     | Description                       | Default       |
| ------------------------ | --------------------------------- | ------------- |
| `--rope-scaling`         | RoPE scaling method               | Auto          |
| `--rope-freq-base`       | RoPE base frequency               | Model default |
| `--rope-freq-scale`      | RoPE frequency scale              | Model default |
| `--no-prefill-assistant` | Disable assistant pre-fill        | Off           |
| `--reasoning-budget`     | Token budget for reasoning models | 0 (disabled)  |

### [vLLM parameters](#vllm-parameters)

When using the vLLM backend, different parameters are available.

Use `--hf_overrides` to pass HuggingFace model config overrides as JSON:

```console
$ docker model configure --hf_overrides '{"rope_scaling": {"type": "dynamic", "factor": 2.0}}' ai/model-vllm
```

## [Configuration presets](#configuration-presets)

Here are complete configuration examples for common use cases.

### [Code completion (fast, deterministic)](#code-completion-fast-deterministic)

```yaml
models:
  coder:
    model: ai/qwen2.5-coder
    context_size: 4096
    runtime_flags:
      - "--temp"
      - "0.1"
      - "--top-k"
      - "1"
      - "--batch-size"
      - "1024"
```

### [Chat assistant (balanced)](#chat-assistant-balanced)

```yaml
models:
  assistant:
    model: ai/llama3.2
    context_size: 8192
    runtime_flags:
      - "--temp"
      - "0.7"
      - "--top-p"
      - "0.9"
      - "--repeat-penalty"
      - "1.1"
```

### [Creative writing (high temperature)](#creative-writing-high-temperature)

```yaml
models:
  writer:
    model: ai/llama3.2
    context_size: 8192
    runtime_flags:
      - "--temp"
      - "1.2"
      - "--top-p"
      - "0.95"
      - "--repeat-penalty"
      - "1.0"
```

### [Long document analysis (large context)](#long-document-analysis-large-context)

```yaml
models:
  analyzer:
    model: ai/qwen2.5-coder:14B
    context_size: 32768
    runtime_flags:
      - "--mlock"
      - "--batch-size"
      - "2048"
```

### [Low memory system](#low-memory-system)

```yaml
models:
  efficient:
    model: ai/smollm2:360M-Q4_K_M
    context_size: 2048
    runtime_flags:
      - "--threads"
      - "4"
```

## [Environment-based configuration](#environment-based-configuration)

You can also configure models via environment variables in containers:

| Variable    | Description                             |
| ----------- | --------------------------------------- |
| `LLM_URL`   | Auto-injected URL of the model endpoint |
| `LLM_MODEL` | Auto-injected model identifier          |

See [Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/) for details on how these are populated.

## [Reset configuration](#reset-configuration)

Configuration set via `docker model configure` persists until the model is removed. To reset configuration:

```console
$ docker model configure --context-size -1 ai/qwen2.5-coder
```

Using `-1` resets to the default value.

## [What's next](#whats-next)

* [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - Learn about llama.cpp and vLLM
* [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - API parameters for per-request configuration
* [Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/) - Configure models in Compose applications

----
url: https://docs.docker.com/scout/how-tos/configure-cli/
----

# Configure Docker Scout with environment variables

***

Table of contents

***

The following environment variables are available to configure the Docker Scout CLI commands, and the corresponding `docker/scout-cli` container image:

| Name                                        | Format  | Description                                                                                 |
| ------------------------------------------- | ------- | ------------------------------------------------------------------------------------------- |
| DOCKER\_SCOUT\_CACHE\_FORMAT                | String  | Format of the local image cache; can be `oci` or `tar` (default: `oci`)                     |
| DOCKER\_SCOUT\_CACHE\_DIR                   | String  | Directory where the local SBOM cache is stored (default: `$HOME/.docker/scout`)             |
| DOCKER\_SCOUT\_NO\_CACHE                    | Boolean | When set to `true`, disables the use of local SBOM cache                                    |
| DOCKER\_SCOUT\_OFFLINE                      | Boolean | Use [offline mode](#offline-mode) when indexing SBOM                                        |
| DOCKER\_SCOUT\_REGISTRY\_TOKEN              | String  | Token for authenticating to a registry when pulling images                                  |
| DOCKER\_SCOUT\_REGISTRY\_USER               | String  | Username for authenticating to a registry when pulling images                               |
| DOCKER\_SCOUT\_REGISTRY\_PASSWORD           | String  | Password or personal access token for authenticating to a registry when pulling images      |
| DOCKER\_SCOUT\_HUB\_USER                    | String  | Docker Hub username for authenticating to the Docker Scout backend                          |
| DOCKER\_SCOUT\_HUB\_PASSWORD                | String  | Docker Hub password or personal access token for authenticating to the Docker Scout backend |
| DOCKER\_SCOUT\_NEW\_VERSION\_WARN           | Boolean | Warn about new versions of the Docker Scout CLI                                             |
| DOCKER\_SCOUT\_EXPERIMENTAL\_WARN           | Boolean | Warn about experimental features                                                            |
| DOCKER\_SCOUT\_EXPERIMENTAL\_POLICY\_OUTPUT | Boolean | Disable experimental output for policy evaluation                                           |

## [Offline mode](#offline-mode)

Under normal operation, Docker Scout cross-references external systems, such as npm, NuGet, or proxy.golang.org, to retrieve additional information about packages found in your image.

When `DOCKER_SCOUT_OFFLINE` is set to `true`, Docker Scout image analysis runs in offline mode. Offline mode means Docker Scout doesn't make outbound requests to external systems.

To use offline mode:

```console
$ export DOCKER_SCOUT_OFFLINE=true
```

----
url: https://docs.docker.com/guides/testcontainers-go-getting-started/create-project/
----

# Create the Go project

***

Table of contents

***

## [Initialize the project](#initialize-the-project)

Start by creating a Go project.

```console
$ mkdir testcontainers-go-demo
$ cd testcontainers-go-demo
$ go mod init github.com/testcontainers/testcontainers-go-demo
```

This guide uses the [jackc/pgx](https://github.com/jackc/pgx) PostgreSQL driver to interact with the Postgres database and the testcontainers-go [Postgres module](https://golang.testcontainers.org/modules/postgres/) to spin up a Postgres Docker instance for testing. It also uses [testify](https://github.com/stretchr/testify) for running multiple tests as a suite and for writing assertions.

Install these dependencies:

```console
$ go get github.com/jackc/pgx/v5
$ go get github.com/testcontainers/testcontainers-go
$ go get github.com/testcontainers/testcontainers-go/modules/postgres
$ go get github.com/stretchr/testify
```

## [Create Customer struct](#create-customer-struct)

Create a `types.go` file in the `customer` package and define the `Customer` struct to model the customer details:

```go
package customer

type Customer struct {
	Id    int
	Name  string
	Email string
}
```

## [Create Repository](#create-repository)

Next, create `customer/repo.go`, define the `Repository` struct, and add methods to create a customer and get a customer by email:

```go
package customer

import (
	"context"
	"fmt"
	"os"

	"github.com/jackc/pgx/v5"
)

type Repository struct {
	conn *pgx.Conn
}

func NewRepository(ctx context.Context, connStr string) (*Repository, error) {
	conn, err := pgx.Connect(ctx, connStr)
	if err != nil {
		_, _ = fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
		return nil, err
	}
	return &Repository{
		conn: conn,
	}, nil
}

func (r Repository) CreateCustomer(ctx context.Context, customer Customer) (Customer, error) {
	err := r.conn.QueryRow(ctx,
		"INSERT INTO customers (name, email) VALUES ($1, $2) RETURNING id",
		customer.Name, customer.Email).Scan(&customer.Id)
	return customer, err
}

func (r Repository) GetCustomerByEmail(ctx context.Context, email string) (Customer, error) {
	var customer Customer
	query := "SELECT id, name, email FROM customers WHERE email = $1"
	err := r.conn.QueryRow(ctx, query, email).
		Scan(&customer.Id, &customer.Name, &customer.Email)
	if err != nil {
		return Customer{}, err
	}
	return customer, nil
}
```

Here's what the code does:

* `Repository` holds a `*pgx.Conn` for performing database operations.
* `NewRepository(connStr)` takes a database connection string and initializes a `Repository`.
* `CreateCustomer()` and `GetCustomerByEmail()` are methods on the `Repository` receiver that insert and query customer records.

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-go-getting-started/write-tests/)

----
url: https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/
----

# FAQs for Docker Desktop for Mac

***

Table of contents

***

### [What is HyperKit?](#what-is-hyperkit)

HyperKit is a hypervisor built on top of the Hypervisor.framework in macOS. It runs entirely in userspace and has no other dependencies.

Docker uses HyperKit to eliminate the need for other VM products, such as Oracle VirtualBox or VMware Fusion.

### [What is the benefit of HyperKit?](#what-is-the-benefit-of-hyperkit)

HyperKit is thinner than VirtualBox and VMware fusion, and the version included is customized for Docker workloads on Mac.

### [Where does Docker Desktop store Linux containers and images?](#where-does-docker-desktop-store-linux-containers-and-images)

Docker Desktop stores Linux containers and images in a single, large "disk image" file in the Mac filesystem. This is different from Docker on Linux, which usually stores containers and images in the `/var/lib/docker` directory.

#### [Where is the disk image file?](#where-is-the-disk-image-file)

To locate the disk image file, select **Settings** from the Docker Desktop Dashboard then **Advanced** from the **Resources** tab.

The **Advanced** tab displays the location of the disk image. It also displays the maximum size of the disk image and the actual space the disk image is consuming. Note that other tools might display space usage of the file in terms of the maximum file size, and not the actual file size.

#### [What if the file is too big?](#what-if-the-file-is-too-big)

If the disk image file is too big, you can:

> Important
>
> Do not move the file directly in Finder as this can cause Docker Desktop to lose track of the file.

##### [How do I delete unnecessary containers and images?](#how-do-i-delete-unnecessary-containers-and-images)

Check whether you have any unnecessary containers and images. If your client and daemon API are running version 1.25 or later (use the `docker version` command on the client to check your client and daemon API versions), you can see the detailed space usage information by running:

```console
$ docker system df -v
```

Alternatively, to list images, run:

```console
$ docker image ls
```

To list containers, run:

```console
$ docker container ls -a
```

If there are lots of redundant objects, run the command:

```console
$ docker system prune
```

This command removes all stopped containers, unused networks, dangling images, and build cache.

It might take a few minutes to reclaim space on the host depending on the format of the disk image file. If the file is named:

* `Docker.raw`, space on the host is reclaimed within a few seconds.
* `Docker.qcow2`, space is freed by a background process after a few minutes.

Space is only freed when images are deleted. Space is not freed automatically when files are deleted inside running containers. To trigger a space reclamation at any point, run the command:

```console
$ docker run --privileged --pid=host docker/desktop-reclaim-space
```

Note that many tools report the maximum file size, not the actual file size. To query the actual size of the file on the host from a terminal, run:

```console
$ cd ~/Library/Containers/com.docker.docker/Data/vms/0/data
$ ls -klsh Docker.raw
2333548 -rw-r--r--@ 1 username  staff    64G Dec 13 17:42 Docker.raw
```

In this example, the actual size of the disk is `2333548` KB, whereas the maximum size of the disk is `64` GB.

##### [How do I reduce the maximum size of the file?](#how-do-i-reduce-the-maximum-size-of-the-file)

To reduce the maximum size of the disk image file:

1. Select **Settings** then **Advanced** from the **Resources** tab.

2. The **Disk image size** section contains a slider that allows you to change the maximum size of the disk image. Adjust the slider to set a lower limit.

3. Select **Apply**.

When you reduce the maximum size, the current disk image file is deleted, and therefore, all containers and images are lost.

### [How do I add TLS certificates?](#how-do-i-add-tls-certificates)

You can add trusted Certificate Authorities (CAs) (used to verify registry server certificates) and client certificates (used to authenticate to registries) to your Docker daemon.

#### [Add custom CA certificates (server side)](#add-custom-ca-certificates-server-side)

All trusted CAs (root or intermediate) are supported. Docker Desktop creates a certificate bundle of all user-trusted CAs based on the Mac Keychain, and appends it to Moby trusted certificates. So if an enterprise SSL certificate is trusted by the user on the host, it is trusted by Docker Desktop.

To manually add a custom, self-signed certificate, start by adding the certificate to the macOS keychain, which is picked up by Docker Desktop. Here is an example:

```console
$ sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain ca.crt
```

Or, if you prefer to add the certificate to your own local keychain only (rather than for all users), run this command instead:

```console
$ security add-trusted-cert -d -r trustRoot -k ~/Library/Keychains/login.keychain ca.crt
```

See also, [Directory structures for certificates](#directory-structures-for-certificates).

> Note
>
> You need to restart Docker Desktop after making any changes to the keychain or to the `~/.docker/certs.d` directory in order for the changes to take effect.

For a complete explanation of how to do this, see the blog post [Adding Self-signed Registry Certs to Docker & Docker Desktop for Mac](https://blog.container-solutions.com/adding-self-signed-registry-certs-docker-mac).

#### [Add client certificates](#add-client-certificates)

You can put your client certificates in `~/.docker/certs.d/<MyRegistry>:<Port>/client.cert` and `~/.docker/certs.d/<MyRegistry>:<Port>/client.key`.

When the Docker Desktop application starts, it copies the `~/.docker/certs.d` folder on your Mac to the `/etc/docker/certs.d` directory on Moby (the Docker Desktop `xhyve` virtual machine).

> Note
>
> * You need to restart Docker Desktop after making any changes to the keychain or to the `~/.docker/certs.d` directory in order for the changes to take effect.
>
> * The registry cannot be listed as an *insecure registry*. Docker Desktop ignores certificates listed under insecure registries, and does not send client certificates. Commands like `docker run` that attempt to pull from the registry produce error messages on the command line, as well as on the registry.

#### [Directory structures for certificates](#directory-structures-for-certificates)

If you have this directory structure, you do not need to manually add the CA certificate to your Mac OS system login:

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
   ├── ca.crt
   ├── client.cert
   └── client.key
```

The following further illustrates and explains a configuration with custom certificates:

```text
/etc/docker/certs.d/        <-- Certificate directory
└── localhost:5000          <-- Hostname:port
   ├── client.cert          <-- Client certificate
   ├── client.key           <-- Client key
   └── ca.crt               <-- Certificate authority that signed
                                the registry certificate
```

You can also have this directory structure, as long as the CA certificate is also in your keychain.

```text
/Users/<user>/.docker/certs.d/
└── <MyRegistry>:<Port>
    ├── client.cert
    └── client.key
```

To learn more about how to install a CA root certificate for the registry and how to set the client TLS certificate for verification, see [Verify repository client with certificates](https://docs.docker.com/engine/security/certificates/) in the Docker Engine topics.

----
url: https://docs.docker.com/reference/api/ai-governance/api.yaml
----

openapi: "3.1.0"

info:
 title: Docker AI Governance Policy API
 version: "1"
 description: \|
 HTTP+JSON API for managing Docker governance policies and rules.

 \*\*Resource model.\*\* An organization owns one or more policies. Each policy
 contains a list of rules grouped into a single domain: either \`network\` or
 \`filesystem\`. A policy's domain is derived from its rule actions; mixing
 domains within a single policy is not permitted.

 \*\*Lifecycle.\*\* Create a policy with CreatePolicy, then add rules with
 CreateRule. Rules can be updated in place with UpdateRule or removed with
 DeleteRule. Deleting all rules does not delete the policy itself.

 \*\*Rule evaluation.\*\* All rules in a policy are tested against every request.
 \`deny\` always wins: if any rule matches with \`decision: deny\`, the request
 is denied regardless of any \`allow\` rules.

 \*\*Enforcement.\*\* Organization policies take precedence over local sandbox
 policies and cannot be overridden by individual users.

 \*\*Propagation.\*\* Policy changes take up to five minutes to reach developer
 machines after being written.

 See https://docs.docker.com/ai/sandboxes/governance/ for product
 documentation.
 contact:
 name: Docker
 url: https://www.docker.com/products/ai-governance/

tags:
 \- name: policies
 description: Policy lifecycle management
 \- name: rules
 description: Rule management within an allowlist policy

servers:
 \- url: https://hub.docker.com/v2

security:
 \- bearerAuth: \[\]

paths:
 /orgs/{org\_name}/governance/policies:
 parameters:
 \- $ref: "#/components/parameters/OrgName"
 get:
 operationId: listPolicies
 tags: \[policies\]
 summary: List policies
 description: >
 Returns a shallow summary of all policies for the org.
 The rule set is not included; use GetPolicy to fetch the full object.
 responses:
 "200":
 description: Object wrapping an array of policy summaries under \`data\`. Rule sets are not included; use GetPolicy to fetch a full policy.
 content:
 application/json:
 schema:
 type: object
 required: \[data\]
 properties:
 data:
 type: array
 items:
 $ref: "#/components/schemas/PolicySummary"
 examples:
 default:
 value:
 data:
 \- id: pol\_06evsmp24r1pg71cm8500546pkbn
 name: "Security Research — hardened"
 org: my-org
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 created\_at: "2026-04-22T00:00:00Z"
 updated\_at: "2026-04-22T00:00:00Z"
 type: allowlist\_v0
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/PermissionDenied"
 "404":
 $ref: "#/components/responses/NotFound"
 "500":
 $ref: "#/components/responses/InternalError"

 post:
 operationId: createPolicy
 tags: \[policies\]
 summary: Create policy
 description: >
 Creates a new policy with an empty rule set. Rules are added separately
 via the rules sub-resource.
 requestBody:
 description: Policy name and optional scope.
 required: true
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/CreatePolicyRequest"
 examples:
 default:
 value:
 name: "Security Research — hardened"
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 responses:
 "201":
 description: Policy created. Returns the new policy without its rule set.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Policy"
 examples:
 default:
 value:
 id: pol\_06evsmp24r1pg71cm8500546pkbn
 name: "Security Research — hardened"
 org: my-org
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 created\_at: "2026-04-22T00:00:00Z"
 updated\_at: "2026-04-22T00:00:00Z"
 "400":
 $ref: "#/components/responses/InvalidArgument"
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/Forbidden"
 "404":
 $ref: "#/components/responses/NotFound"
 "409":
 $ref: "#/components/responses/Conflict"
 "500":
 $ref: "#/components/responses/InternalError"

 /orgs/{org\_name}/governance/policies/{policy\_id}:
 parameters:
 \- $ref: "#/components/parameters/OrgName"
 \- $ref: "#/components/parameters/PolicyID"
 get:
 operationId: getPolicy
 tags: \[policies\]
 summary: Get policy
 description: Returns the full policy including its \`allowlist\_v0\` rule set.
 responses:
 "200":
 description: Full policy including its \`allowlist\_v0\` rule set.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Policy"
 examples:
 default:
 value:
 id: pol\_06evsmp24r1pg71cm8500546pkbn
 name: "Security Research — hardened"
 org: my-org
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 created\_at: "2026-04-22T00:00:00Z"
 updated\_at: "2026-04-22T00:00:00Z"
 allowlist\_v0:
 domain: network
 rules:
 \- id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/PermissionDenied"
 "404":
 $ref: "#/components/responses/NotFound"
 "500":
 $ref: "#/components/responses/InternalError"
 patch:
 operationId: updatePolicy
 tags: \[policies\]
 summary: Update policy
 description: \|
 Partially updates a policy's metadata. Only fields present in the
 request body are updated; absent fields are left unchanged. The \`scope\`
 object is patched per sub-field: sending \`teams\` replaces that list,
 while an omitted sub-field is left untouched and an empty list clears
 it (org-wide).

 The rule set is not modified here — use the rule endpoints for that.
 At least one field must be present. Returns the policy in both its old
 and new states. Changes may take up to five minutes to reach developer
 machines.
 requestBody:
 description: Fields to update. Absent fields are left unchanged.
 required: true
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/UpdatePolicyRequest"
 examples:
 rename:
 summary: Rename the policy
 value:
 name: Security Research
 scope:
 summary: Restrict to a team
 value:
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 responses:
 "200":
 description: Policy updated, returns old and new states.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/UpdatePolicyResponse"
 examples:
 default:
 value:
 old:
 id: pol\_06evsmp24r1pg71cm8500546pkbn
 name: "Security Research — hardened"
 org: my-org
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 created\_at: "2026-04-22T00:00:00Z"
 updated\_at: "2026-04-22T00:00:00Z"
 allowlist\_v0:
 domain: network
 rules:
 \- id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 new:
 id: pol\_06evsmp24r1pg71cm8500546pkbn
 name: Security Research
 org: my-org
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 created\_at: "2026-04-22T00:00:00Z"
 updated\_at: "2026-04-22T10:00:00Z"
 allowlist\_v0:
 domain: network
 rules:
 \- id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 "400":
 $ref: "#/components/responses/InvalidArgument"
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/Forbidden"
 "404":
 $ref: "#/components/responses/NotFound"
 "409":
 $ref: "#/components/responses/Conflict"
 "500":
 $ref: "#/components/responses/InternalError"
 delete:
 operationId: deletePolicy
 tags: \[policies\]
 summary: Delete policy
 description: \|
 Permanently deletes the policy and its rule set. Returns the deleted
 policy as a courtesy; its \`updated\_at\` is unchanged by the deletion.
 Changes may take up to five minutes to reach developer machines.
 responses:
 "200":
 description: Policy deleted, returns the deleted policy.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/DeletePolicyResponse"
 examples:
 default:
 value:
 deleted:
 id: pol\_06evsmp24r1pg71cm8500546pkbn
 name: "Security Research — hardened"
 org: my-org
 scope:
 teams: \[d290f1ee-6c54-4b01-90e6-d701748f0851\]
 created\_at: "2026-04-22T00:00:00Z"
 updated\_at: "2026-04-22T00:00:00Z"
 allowlist\_v0:
 domain: network
 rules:
 \- id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/PermissionDenied"
 "404":
 $ref: "#/components/responses/NotFound"
 "500":
 $ref: "#/components/responses/InternalError"

 /orgs/{org\_name}/governance/policies/{policy\_id}/rules:
 parameters:
 \- $ref: "#/components/parameters/OrgName"
 \- $ref: "#/components/parameters/PolicyID"
 post:
 operationId: createRule
 tags: \[rules\]
 summary: Create rule
 description: \|
 Adds a rule to the policy's rule set. All rules in a policy must share
 the same domain (network or filesystem); mixing domains is rejected.

 \*\*Network\*\* actions: \`connect:tcp\`, \`connect:udp\`. Resources are
 hostnames (for example, \`example.com\`), wildcard subdomains (\`\*.example.com\`
 for one level, \`\*\*.example.com\` for any depth), hostnames with an optional
 port (for example, \`example.com:443\`), or CIDRs in IPv4 or IPv6 notation
 (for example, \`10.0.0.0/8\` or \`2001:db8::/32\`).

 \*\*Filesystem\*\* actions: \`read\`, \`write\`. Resources are paths (for example,
 \`/data\`). Use \`\*\` to match within a single path segment and \`\*\*\` to match
 recursively across segments (for example, \`/data/\*\*\`).

 Changes may take up to five minutes to reach developer machines.
 requestBody:
 description: Rule definition including actions, resources, and decision.
 required: true
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/CreateRuleRequest"
 examples:
 network:
 summary: Network rule
 value:
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 filesystem:
 summary: Filesystem rule
 value:
 name: allow data directory
 actions: \[read, write\]
 resources: \[/data\]
 decision: allow
 responses:
 "201":
 description: Rule created and added to the policy's rule set.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Rule"
 examples:
 network:
 summary: Network rule
 value:
 id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 filesystem:
 summary: Filesystem rule
 value:
 id: rule\_07fwtnr0kn2qetl1b9olfbyz8kob
 name: allow data directory
 actions: \[read, write\]
 resources: \[/data\]
 decision: allow
 "400":
 $ref: "#/components/responses/InvalidArgument"
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/Forbidden"
 "404":
 $ref: "#/components/responses/NotFound"
 "409":
 $ref: "#/components/responses/Conflict"
 "500":
 $ref: "#/components/responses/InternalError"

 /orgs/{org\_name}/governance/policies/{policy\_id}/rules/{rule\_id}:
 parameters:
 \- $ref: "#/components/parameters/OrgName"
 \- $ref: "#/components/parameters/PolicyID"
 \- $ref: "#/components/parameters/RuleID"
 patch:
 operationId: updateRule
 tags: \[rules\]
 summary: Update rule
 description: \|
 Partially updates a rule. Only fields present in the request body are
 updated; absent fields are left unchanged. Returns the rule in both its
 old and new states.

 Changing \`actions\` across domains (for example, from network actions to
 filesystem actions) is rejected. Changes may take up to five minutes to
 reach developer machines.
 requestBody:
 description: Fields to update. Absent fields are left unchanged.
 required: true
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/UpdateRuleRequest"
 examples:
 default:
 value:
 resources: \["research.mitre.org"\]
 responses:
 "200":
 description: Rule updated, returns old and new states.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/UpdateRuleResponse"
 examples:
 default:
 value:
 old:
 id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 new:
 id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org\]
 decision: allow
 "400":
 $ref: "#/components/responses/InvalidArgument"
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/PermissionDenied"
 "404":
 $ref: "#/components/responses/NotFound"
 "409":
 $ref: "#/components/responses/Conflict"
 "500":
 $ref: "#/components/responses/InternalError"

 delete:
 operationId: deleteRule
 tags: \[rules\]
 summary: Delete rule
 description: \|
 Deletes a rule from the policy. Returns the deleted rule. Changes may
 take up to five minutes to reach developer machines.
 responses:
 "200":
 description: Rule deleted, returns the deleted rule.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/DeleteRuleResponse"
 examples:
 default:
 value:
 deleted:
 id: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name: allow research mirrors
 actions: \[connect:tcp, connect:udp\]
 resources: \[research.mitre.org, cve.mitre.org\]
 decision: allow
 "401":
 $ref: "#/components/responses/Unauthenticated"
 "403":
 $ref: "#/components/responses/PermissionDenied"
 "404":
 $ref: "#/components/responses/NotFound"
 "500":
 $ref: "#/components/responses/InternalError"

components:
 securitySchemes:
 bearerAuth:
 type: http
 scheme: bearer
 bearerFormat: JWT
 description: \|
 Short-lived JWT obtained by exchanging Docker Hub credentials at
 \`POST https://hub.docker.com/v2/auth/token\`. Pass the JWT in the
 \`Authorization: Bearer \` header. Tokens expire after a short
 period; request a fresh one when you receive a \`401\`.

 The \`password\` field of the token request accepts any of the following
 credential types:

 \| Type \| Format \| Notes \|
 \|------\|--------\|-------\|
 \| Password \| Plain text \| Your Docker Hub account password. \|
 \| Personal Access Token (PAT) \| \`dckr\_pat\_\*\` \| Recommended over passwords. Create one under Account Settings → Security. \|
 \| Organization Access Token (OAT) \| \`dckr\_oat\_\*\` \| Scoped to an organization. Create one under Organization Settings → Access Tokens. \|

 PAT and OAT strings can't be used directly as a bearer token. They must
 be exchanged at the token endpoint first.

 See \[Docker Hub authentication\](https://docs.docker.com/reference/api/hub/latest/#tag/authentication-api/operation/AuthCreateAccessToken)
 for full details.

 parameters:
 OrgName:
 name: org\_name
 in: path
 required: true
 description: Docker Hub organization name.
 schema:
 type: string
 examples:
 default:
 value: my-org

 PolicyID:
 name: policy\_id
 in: path
 required: true
 description: Unique policy identifier.
 schema:
 type: string
 examples:
 default:
 value: pol\_06evsmp24r1pg71cm8500546pkbn

 RuleID:
 name: rule\_id
 in: path
 required: true
 description: Unique rule identifier within the policy.
 schema:
 type: string
 examples:
 default:
 value: rule\_06evsm9qjm1pdsk0a8nkfaxy7jna

 schemas:
 PolicySummary:
 type: object
 description: Shallow policy representation returned by ListPolicies. Excludes the rule set.
 required: \[id, name, org, scope, created\_at, updated\_at, type\]
 properties:
 id:
 type: string
 examples:
 \- pol\_06evsmp24r1pg71cm8500546pkbn
 name:
 type: string
 description: Human-readable label, unique within the organization.
 examples:
 \- "Security Research — hardened"
 org:
 type: string
 examples:
 \- my-org
 scope:
 $ref: "#/components/schemas/Scope"
 created\_at:
 type: string
 format: date-time
 examples:
 \- "2026-04-22T00:00:00Z"
 updated\_at:
 type: string
 format: date-time
 examples:
 \- "2026-04-22T00:00:00Z"
 type:
 type: string
 description: >
 Identifies the rule-set format. Always \`allowlist\_v0\`, corresponding
 to the \`allowlist\_v0\` property on the full Policy object.
 examples:
 \- allowlist\_v0

 Policy:
 type: object
 description: Full policy representation including the allowlist rule set.
 required: \[id, name, org, scope, created\_at, updated\_at\]
 properties:
 id:
 type: string
 examples:
 \- pol\_06evsmp24r1pg71cm8500546pkbn
 name:
 type: string
 description: Human-readable label, unique within the organization.
 examples:
 \- "Security Research — hardened"
 org:
 type: string
 examples:
 \- my-org
 scope:
 $ref: "#/components/schemas/Scope"
 created\_at:
 type: string
 format: date-time
 examples:
 \- "2026-04-22T00:00:00Z"
 updated\_at:
 type: string
 format: date-time
 examples:
 \- "2026-04-22T00:00:00Z"
 allowlist\_v0:
 $ref: "#/components/schemas/AllowlistV0"

 Scope:
 type: object
 description: Restricts the policy to specific teams. An empty or absent list means the policy applies org-wide.
 properties:
 teams:
 type: array
 items:
 type: string
 description: Team UUIDs the policy applies to. Each must be a valid team in the org.
 examples:
 \- \["d290f1ee-6c54-4b01-90e6-d701748f0851"\]

 AllowlistV0:
 type: object
 description: \|
 Network or filesystem allowlist containing a list of rules. Present on
 Policy when \`PolicySummary.type\` is \`allowlist\_v0\`; omitted when the
 policy has no rules yet. All rules in an allowlist share the same domain.
 All rules are evaluated on every request: \`deny\` always wins over \`allow\`.
 required: \[rules\]
 properties:
 domain:
 type: string
 description: >
 The access-control domain shared by all rules in this allowlist.
 Derived from rule actions: network actions (\`connect:tcp\`,
 \`connect:udp\`) produce \`network\`; filesystem actions (\`read\`,
 \`write\`) produce \`filesystem\`. Present when \`rules\` is non-empty;
 absent when the allowlist has no rules.
 enum: \[network, filesystem\]
 examples:
 \- network
 rules:
 type: array
 items:
 $ref: "#/components/schemas/Rule"

 Rule:
 type: object
 description: A single allow or deny rule within an allowlist policy.
 required: \[id, name, actions, resources, decision\]
 properties:
 id:
 type: string
 examples:
 \- rule\_06evsm9qjm1pdsk0a8nkfaxy7jna
 name:
 type: string
 description: Human-readable label for the rule.
 examples:
 \- allow research mirrors
 actions:
 $ref: "#/components/schemas/RuleActions"
 resources:
 $ref: "#/components/schemas/RuleResources"
 decision:
 $ref: "#/components/schemas/RuleDecision"

 CreatePolicyRequest:
 type: object
 description: Fields required to create a new policy.
 required: \[name\]
 properties:
 name:
 type: string
 description: Policy name, unique within the organization.
 examples:
 \- "Security Research — hardened"
 scope:
 $ref: "#/components/schemas/Scope"

 CreateRuleRequest:
 type: object
 description: Fields required to create a new rule within a policy's rule set.
 required: \[name, actions, resources, decision\]
 properties:
 name:
 type: string
 description: Human-readable label for the rule.
 examples:
 \- allow research mirrors
 actions:
 $ref: "#/components/schemas/RuleActions"
 resources:
 $ref: "#/components/schemas/RuleResources"
 decision:
 $ref: "#/components/schemas/RuleDecision"

 UpdateRuleRequest:
 type: object
 description: Partial update. Only fields present in the body are updated; absent fields are left unchanged.
 properties:
 name:
 type: string
 description: Human-readable label for the rule.
 examples:
 \- allow research mirrors
 actions:
 $ref: "#/components/schemas/RuleActions"
 resources:
 $ref: "#/components/schemas/RuleResources"
 decision:
 $ref: "#/components/schemas/RuleDecision"

 UpdateRuleResponse:
 type: object
 description: The rule state before and after the update.
 required: \[old, new\]
 properties:
 old:
 $ref: "#/components/schemas/Rule"
 new:
 $ref: "#/components/schemas/Rule"

 DeleteRuleResponse:
 type: object
 description: The deleted rule.
 required: \[deleted\]
 properties:
 deleted:
 $ref: "#/components/schemas/Rule"

 UpdatePolicyRequest:
 type: object
 description: >
 Partial update of a policy's metadata. Only fields present in the body
 are updated; the rule set is not modified here. At least one field must
 be present.
 properties:
 name:
 type: string
 minLength: 1
 description: Policy name, unique within the organization.
 examples:
 \- Security Research
 scope:
 $ref: "#/components/schemas/ScopePatch"

 ScopePatch:
 type: object
 description: >
 Per-sub-field patch of a policy's scope. An omitted sub-field is left
 unchanged; a present list replaces that dimension, and an empty list
 clears it (making the policy org-wide for that dimension).
 properties:
 teams:
 type: array
 items:
 type: string
 examples:
 \- \["d290f1ee-6c54-4b01-90e6-d701748f0851"\]

 UpdatePolicyResponse:
 type: object
 description: The full policy before and after the update.
 required: \[old, new\]
 properties:
 old:
 $ref: "#/components/schemas/Policy"
 new:
 $ref: "#/components/schemas/Policy"

 DeletePolicyResponse:
 type: object
 description: The full deleted policy.
 required: \[deleted\]
 properties:
 deleted:
 $ref: "#/components/schemas/Policy"

 RuleActions:
 type: array
 items:
 type: string
 enum: \[connect:tcp, connect:udp, read, write\]
 minItems: 1
 description: >
 Network actions: \`connect:tcp\`, \`connect:udp\`.
 Filesystem actions: \`read\`, \`write\`.
 All actions in a rule must belong to the same domain; mixing network
 and filesystem actions in one rule is rejected.
 examples:
 \- \["connect:tcp", "connect:udp"\]

 RuleResources:
 type: array
 items:
 type: string
 minItems: 1
 description: >
 Network domain: hostnames (for example, \`example.com\`), wildcard
 subdomains (\`\*.example.com\` or \`\*\*.example.com\`), hostnames with port
 (for example, \`example.com:443\`), or CIDRs in IPv4 or IPv6 notation
 (for example, \`10.0.0.0/8\` or \`2001:db8::/32\`). Filesystem domain:
 paths (for example, \`/data\`); \`\*\` matches within one path segment,
 \`\*\*\` matches recursively (for example, \`/data/\*\*\`).
 examples:
 \- \["research.mitre.org", "cve.mitre.org"\]

 RuleDecision:
 type: string
 enum: \[allow, deny\]
 description: >
 Outcome applied when this rule matches a request. \`deny\` always
 wins: if any rule in the policy matches with \`decision: deny\`, the
 request is denied even if other rules match with \`decision: allow\`.
 examples:
 \- allow

 Error:
 type: object
 description: Error envelope returned on all non-2xx responses.
 required: \[error\]
 properties:
 error:
 type: object
 description: Error detail.
 required: \[code, message\]
 examples:
 \- code: not\_found
 message: policy not found
 properties:
 code:
 type: string
 description: >
 Machine-readable error code. \`not\_found\`: the requested resource
 does not exist, the org does not exist, or the caller is not a
 member of the org (the org's existence is not revealed to callers
 who cannot access it). \`conflict\`: a resource with the same name
 already exists. \`invalid\_argument\`: the request body is malformed
 or fails validation. \`unauthenticated\`: missing or invalid
 credentials. \`permission\_denied\`: the org is not entitled to use
 governance. \`limit\_exceeded\`: the org has reached its maximum
 number of policies, or the policy has reached its maximum number
 of rules. \`unimplemented\`: the endpoint or feature is not yet
 available. \`internal\`: unexpected server error.
 enum:
 \- not\_found
 \- conflict
 \- invalid\_argument
 \- unauthenticated
 \- permission\_denied
 \- limit\_exceeded
 \- unimplemented
 \- internal
 message:
 type: string

 responses:
 NotFound:
 description: Not found
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 default:
 value:
 error:
 code: not\_found
 message: policy not found

 Conflict:
 description: Conflict
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 default:
 value:
 error:
 code: conflict
 message: policy name already in use

 InvalidArgument:
 description: Bad request
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 default:
 value:
 error:
 code: invalid\_argument
 message: "name is required"

 Unauthenticated:
 description: Missing or invalid credentials
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 default:
 value:
 error:
 code: unauthenticated
 message: unauthenticated

 PermissionDenied:
 description: >
 Caller lacks the required permission for this org, or the org is not
 entitled to use governance.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 default:
 value:
 error:
 code: permission\_denied
 message: permission denied

 Forbidden:
 description: >
 Caller lacks the required permission for this org, the org is not
 entitled to use governance (\`permission\_denied\`), or a creation limit
 has been reached (\`limit\_exceeded\`): the org already has the maximum
 number of policies, or the policy already has the maximum number of
 rules.
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 permission\_denied:
 value:
 error:
 code: permission\_denied
 message: permission denied
 limit\_exceeded:
 value:
 error:
 code: limit\_exceeded
 message: organization has reached the maximum of 100 policies

 InternalError:
 description: Internal server error
 content:
 application/json:
 schema:
 $ref: "#/components/schemas/Error"
 examples:
 default:
 value:
 error:
 code: internal
 message: internal error

----
url: https://docs.docker.com/guides/deno/configure-ci-cd/
----

# Configure CI/CD for your Deno application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize a Deno application](https://docs.docker.com/guides/deno/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. Run the following commands to stage, commit, and push your local repository to GitHub.

   ```console
   $ git add -A
   $ git commit -m "my commit"
   $ git push -u origin main
   ```

## [Step two: Set up the workflow](#step-two-set-up-the-workflow)

Set up your GitHub Actions workflow for building and pushing the image to Docker Hub.

1. Go to your repository on GitHub and then select the **Actions** tab.

2. Select **set up a workflow yourself**.

   This takes you to a page for creating a new GitHub actions workflow file in your repository, under `.github/workflows/main.yml` by default.

3. In the editor window, copy and paste the following YAML configuration and commit the changes.

   ```yaml
   name: ci

   on:
     push:
       branches:
         - main

   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         -
           name: Login to Docker Hub
           uses: docker/login-action@v4
           with:
             username: ${{ vars.DOCKER_USERNAME }}
             password: ${{ secrets.DOCKERHUB_TOKEN }}
         -
           name: Set up Docker Buildx
           uses: docker/setup-buildx-action@v4
         -
           name: Build and push
           uses: docker/build-push-action@v7
           with:
             platforms: linux/amd64,linux/arm64
             push: true
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

In this section, you learned how to set up a GitHub Actions workflow for your Deno application.

Related information:

* [Introduction to GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
* [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## [Next steps](#next-steps)

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

[Test your Deno deployment »](https://docs.docker.com/guides/deno/deploy/)