url: https://docs.docker.com/build/release-notes/
----

[Skip to content](#start-of-content)

You signed in with another tab or window. [Reload]() to refresh your session. You signed out in another tab or window. [Reload]() to refresh your session. You switched accounts on another tab or window. [Reload]() to refresh your session. Dismiss alert

[docker ](/docker)/ **[buildx](/docker/buildx)&#x20;**&#x50;ublic

* [Notifications ](/login?return_to=%2Fdocker%2Fbuildx)You must be signed in to change notification settings
* [Fork 652](/login?return_to=%2Fdocker%2Fbuildx)
* [Star 4.4k](/login?return_to=%2Fdocker%2Fbuildx)

# Releases: docker/buildx

Releases · docker/buildx

## v0.35.0

17 Jun 23:18

[github-actions](/apps/github-actions)

[v0.35.0](/docker/buildx/tree/v0.35.0)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`a319e5b`](/docker/buildx/commit/a319e5b15052cf6557ceb666eb8ff6e32380b782)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.35.0](/docker/buildx/releases/tag/v0.35.0) [Latest](/docker/buildx/releases/latest)

[Latest](/docker/buildx/releases/latest)

buildx 0.35.0

Welcome to the v0.35.0 release of buildx!

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Tõnis Tiigi
* Sebastiaan van Stijn
* Areeb Ahmed
* Jiří Moravčík
* Sopho Merkviladze
* Akihiro Suda
* Jonathan A. Sternberg

### Notable Changes

* Local output now supports a `mode=delete` attribute for build and bake commands. This mode replaces the destination directory with the build result instead of merging it. Similar to the `--delete` flag in rsync. For safety, this mode is only allowed if the destination directory is a subdirectory of the working directory. To export to other destinations, `--allow=buildx.local.delete` needs to be provided or the action confirmed by the user in the TUI. When exporting multi-platform results, this mode requires BuildKit v0.31.0+. [#3883](https://github.com/docker/buildx/pull/3883)
* Source policies now support the new exec proxy feature of BuildKit v0.31.0+ that captures the network traffic of your build steps. To opt in to network proxy, your Dockerfile.rego source policy needs to return `caps: { "exec.proxy": true }` in the evaluation decision. After opting in, you can control what network requests are allowed to be made by the run steps with policy rules for regular `input.http` sources, similar to how this was done for direct HTTP build sources before. You can also opt in your whole builder with `--buildkitd-flags '--proxy-network'` in `buildx create`. [#3895](https://github.com/docker/buildx/pull/3895)
* Resource limits can now be set for CPU and memory using the `--resource` flag in `build` and the `resource` key in `bake` commands. This feature requires BuildKit v0.31.0+ and Dockerfile v1.25.0+. [#3876](https://github.com/docker/buildx/pull/3876) [#3900](https://github.com/docker/buildx/pull/3900)
* Fix possible "closed channel" panic. [#3886](https://github.com/docker/buildx/pull/3886)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.7 -> v1.42.0
* **github.com/aws/aws-sdk-go-v2/config** v1.32.17 -> v1.32.24
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.16 -> v1.19.23
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.23 -> v1.18.29
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.23 -> v1.4.29
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.23 -> v2.7.29
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.24 -> v1.4.30
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.9 -> v1.13.12
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.23 -> v1.13.29
* **github.com/containerd/platforms** v1.0.0-rc.2 -> v1.0.0-rc.4
* **github.com/containerd/typeurl/v2** v2.2.3 -> v2.3.0
* **github.com/docker/cli** v29.4.3 -> v29.5.3
* **github.com/docker/distribution** v2.8.3 ***new***
* **github.com/google/certificate-transparency-go** v1.3.2 -> v1.3.3
* **github.com/google/go-containerregistry** v0.20.7 -> v0.21.6
* **github.com/gorilla/mux** v1.8.1 ***new***
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.28.0 -> v2.29.0
* **github.com/in-toto/attestation** v1.1.2 -> v1.2.0
* **github.com/moby/buildkit** v0.30.0 -> v0.31.0
* **github.com/moby/policy-helpers** a39d60132186 -> d5411a945cfc
* **github.com/moby/sys/sequential** v0.6.0 -> v0.7.0
* **github.com/pelletier/go-toml/v2** v2.2.4 -> v2.3.1
* **github.com/prometheus/common** v0.66.1 -> v0.67.5
* **github.com/prometheus/procfs** v0.17.0 -> v0.20.1
* **github.com/secure-systems-lab/go-securesystemslib** v0.10.0 -> v0.11.0
* **github.com/sigstore/protobuf-specs** v0.5.0 -> v0.5.1
* **github.com/sigstore/rekor** v1.5.0 -> v1.5.2
* **github.com/sigstore/rekor-tiles/v2** v2.0.1 -> 5d098a2b6443
* **github.com/sigstore/sigstore** v1.10.5 -> v1.10.8
* **github.com/sigstore/sigstore-go** v1.1.4 -> v1.2.1
* **github.com/sigstore/timestamp-authority/v2** v2.0.6 -> v2.1.2
* **github.com/theupdateframework/go-tuf/v2** v2.4.1 -> v2.4.2
* **github.com/tonistiigi/fsutil** a2aa163d723f -> 0257b3308df4
* **github.com/transparency-dev/formats** 404c0d5b696c -> v0.1.1
* **github.com/youmark/pkcs8** a2c0da244d78 ***new***
* **go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc** v0.68.0 -> v0.69.0
* **go.opentelemetry.io/contrib/instrumentation/net/http/httptrace/otelhttptrace** v0.68.0 -> v0.69.0
* **go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp** v0.68.0 -> v0.69.0
* **go.opentelemetry.io/otel** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/exporters/stdout/stdouttrace** v1.42.0 -> v1.44.0
* **go.opentelemetry.io/otel/metric** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/sdk** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/sdk/metric** v1.43.0 -> v1.44.0
* **go.opentelemetry.io/otel/trace** v1.43.0 -> v1.44.0
* **go.yaml.in/yaml/v2** v2.4.3 -> v2.4.4
* **google.golang.org/genproto/googleapis/api** 6f92a...

[Read more](/docker/buildx/releases/tag/v0.35.0)

Assets 69

* [buildx-v0.35.0.darwin-amd64](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.darwin-amd64)

  sha256:7d53fd11deca2d4caebc5436c9eebece5c81c8bbc6d4b539cf30be5c133c38c7

  64.2 MB 2026-06-17T23:17:27Z

* [buildx-v0.35.0.darwin-amd64.provenance.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.darwin-amd64.provenance.json)

  sha256:83e1ea7b7e9fb85eb6d0b540d85f9b6d26434478a03b100867a0e397e815165e

  54.1 KB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.darwin-amd64.sbom.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.darwin-amd64.sbom.json)

  sha256:42e276c84eaa0d8160f4bbe14329079ab875f5c5842df3332be2ce78519cd7ed

  415 KB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.darwin-arm64](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.darwin-arm64)

  sha256:fedbcbd488dcdb46414c6119920d8186d406531a1157ceede4e857e25af77ff1

  59.9 MB 2026-06-17T23:17:53Z

* [buildx-v0.35.0.darwin-arm64.provenance.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.darwin-arm64.provenance.json)

  sha256:3e11ccc792acc1fb5f49884c30b91cd8975f736f84e910ce82f687b31b91f1f5

  54.1 KB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.darwin-arm64.sbom.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.darwin-arm64.sbom.json)

  sha256:98695e49c5e92099db6104cf6cfe456b63b2a29ab45ca61bfef41bbe1cc56984

  415 KB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.freebsd-amd64](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.freebsd-amd64)

  sha256:4ff6414c7f25c9ce48b91302977f59c1cac5b25e08ee51af9afa1a491531d175

  62.1 MB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.freebsd-amd64.provenance.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.freebsd-amd64.provenance.json)

  sha256:a250848929418c35d1b6e6ef1baede0988ed13349a86d25438610fe4c202327c

  54.1 KB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.freebsd-amd64.sbom.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.freebsd-amd64.sbom.json)

  sha256:a145253222be589cfe6b4a828869a6cd498e0ba1627664b8d4c10d34b7f96595

  416 KB 2026-06-17T20:44:15Z

* [buildx-v0.35.0.freebsd-amd64.sigstore.json](/docker/buildx/releases/download/v0.35.0/buildx-v0.35.0.freebsd-amd64.sigstore.json)

  sha256:43350a2fe315d40b670565b580d948baa18a88a5cc42d5571b43f96a5e311b8e

  82.9 KB 2026-06-17T20:44:15Z

* [Source code (zip)](/docker/buildx/archive/refs/tags/v0.35.0.zip)

  2026-06-17T20:31:24Z

* [Source code (tar.gz)](/docker/buildx/archive/refs/tags/v0.35.0.tar.gz)

  2026-06-17T20:31:24Z

* Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

## v0.35.0-rc2

12 Jun 12:39

[github-actions](/apps/github-actions)

[v0.35.0-rc2](/docker/buildx/tree/v0.35.0-rc2)

This tag was signed with the committer’s **verified signature**.

[](/crazy-max)[crazy-max](/crazy-max) CrazyMax

GPG key ID: ADE44D8C9D44FBE4

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`73e5659`](/docker/buildx/commit/73e56595aae0f22dd2b123e092ac3eba28016590)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.35.0-rc2](/docker/buildx/releases/tag/v0.35.0-rc2) Pre-release

Pre-release

Welcome to the v0.35.0-rc2 release of buildx!\
*This is a pre-release of buildx*

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Jiří Moravčík

### Notable Changes

* Resource limit output for builds has been improved. [#3900](https://github.com/docker/buildx/pull/3900)

### Dependency Changes

* **github.com/docker/distribution** v2.8.3 ***new***
* **github.com/google/certificate-transparency-go** v1.3.2 -> v1.3.3
* **github.com/google/go-containerregistry** v0.20.7 -> v0.21.6
* **github.com/gorilla/mux** v1.8.1 ***new***
* **github.com/in-toto/attestation** v1.1.2 -> v1.2.0
* **github.com/moby/buildkit** v0.31.0-rc1 -> v0.31.0-rc2
* **github.com/moby/policy-helpers** a39d60132186 -> d5411a945cfc
* **github.com/prometheus/common** v0.66.1 -> v0.67.5
* **golang.org/x/tools** v0.44.0 -> v0.45.0
* **google.golang.org/grpc/cmd/protoc-gen-go-grpc** v1.5.1 -> v1.6.1
* **k8s.io/klog/v2** v2.130.1 -> v2.140.0

Previous release can be found at [v0.35.0-rc1](https://github.com/docker/buildx/releases/tag/v0.35.0-rc1)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v0.35.0-rc1

11 Jun 00:08

[github-actions](/apps/github-actions)

[v0.35.0-rc1](/docker/buildx/tree/v0.35.0-rc1)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`89b455a`](/docker/buildx/commit/89b455a9e38ca3808e94190ce5c54193c9cb2e06)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.35.0-rc1](/docker/buildx/releases/tag/v0.35.0-rc1) Pre-release

Pre-release

Welcome to the v0.35.0-rc1 release of buildx!\
*This is a pre-release of buildx*

Note

This release is missing the version tag in the filenames and `--version` output. This issue will be fixed by the next test release.

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Tõnis Tiigi
* Sebastiaan van Stijn
* Areeb Ahmed
* Sopho Merkviladze
* Akihiro Suda
* Jiří Moravčík
* Jonathan A. Sternberg

### Notable Changes

* Local output now supports a `mode=delete` attribute for build and bake commands. This mode replaces the destination directory with the build result instead of merging it. Similar to the `--delete` flag in rsync. For safety, this mode is only allowed if the destination directory is a subdirectory of the working directory. To export to other destinations, `--allow=buildx.local.delete` needs to be provided or the action confirmed by the user in the TUI. When exporting multi-platform results, this mode requires BuildKit v0.31.0+. [#3883](https://github.com/docker/buildx/pull/3883)
* Source policies now support the new exec proxy feature of BuildKit v0.31.0+ that captures the network traffic of your build steps. To opt in to network proxy, your Dockerfile.rego source policy needs to return `caps: { "exec.proxy": true }` in the evaluation decision. After opting in, you can control what network requests are allowed to be made by the run steps with policy rules for regular `input.http` sources, similar to how this was done for direct HTTP build sources before. You can also opt in your whole builder with `--buildkitd-flags '--proxy-network'` in `buildx create`. [#3895](https://github.com/docker/buildx/pull/3895)
* Resource limits can now be set for CPU and memory using the `--resource` flag in `build` and the `resource` key in `bake` commands. This feature requires BuildKit v0.31.0+ and Dockerfile v0.25.0+. [#3876](https://github.com/docker/buildx/pull/3876)
* Fix possible "closed channel" panic. [#3886](https://github.com/docker/buildx/pull/3886)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.7 -> v1.42.0
* **github.com/aws/aws-sdk-go-v2/config** v1.32.17 -> v1.32.24
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.16 -> v1.19.23
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.23 -> v1.18.29
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.23 -> v1.4.29
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.23 -> v2.7.29
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.24 -> v1.4.30
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.9 -> v1.13.12
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.23 -> v1.13.29
* **github.com/containerd/platforms** v1.0.0-rc.2 -> v1.0.0-rc.4
* **github.com/containerd/typeurl/v2** v2.2.3 -> v2.3.0
* **github.com/docker/cli** v29.4.3 -> v29.5.3
* **github.com/docker/docker-credential-helpers** v0.9.5 -> v0.9.8
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.28.0 -> v2.29.0
* **github.com/moby/buildkit** v0.30.0 -> v0.31.0-rc1
* **github.com/moby/sys/sequential** v0.6.0 -> v0.7.0
* **github.com/pelletier/go-toml/v2** v2.2.4 -> v2.3.1
* **github.com/tonistiigi/fsutil** a2aa163d723f -> 0257b3308df4
* **google.golang.org/genproto/googleapis/api** 6f92a3bedf2d -> 3dc84a4a5aaa
* **google.golang.org/genproto/googleapis/rpc** 6f92a3bedf2d -> 3dc84a4a5aaa
* **google.golang.org/grpc** v1.80.0 -> v1.81.1

Previous release can be found at [v0.34.1](https://github.com/docker/buildx/releases/tag/v0.34.1)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v0.34.1

19 May 18:39

[github-actions](/apps/github-actions)

[v0.34.1](/docker/buildx/tree/v0.34.1)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`e0b0e77`](/docker/buildx/commit/e0b0e77d18d3379bc1e0d55f3b37de288d36fe47)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.34.1](/docker/buildx/releases/tag/v0.34.1)

buildx 0.34.1

Welcome to the v0.34.1 release of buildx!

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Jonathan A. Sternberg
* Tõnis Tiigi

### Notable Changes

* Fix regression in Bake command when building from Compose files with empty array value [#3849](https://github.com/docker/buildx/issues/3849) [#3852](https://github.com/docker/buildx/pull/3852)
* Fix possible panic in Kubernetes driver when using statefulset [#3853](https://github.com/docker/buildx/pull/3853)

### Dependency Changes

This release has no dependency changes

Previous release can be found at [v0.34.0](https://github.com/docker/buildx/releases/tag/v0.34.0)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v0.34.0

13 May 14:51

[github-actions](/apps/github-actions)

[v0.34.0](/docker/buildx/tree/v0.34.0)

This tag was signed with the committer’s **verified signature**.

[](/crazy-max)[crazy-max](/crazy-max) CrazyMax

GPG key ID: ADE44D8C9D44FBE4

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`3e73561`](/docker/buildx/commit/3e73561e39785683b31b05eeab1ef645be44ca42)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.34.0](/docker/buildx/releases/tag/v0.34.0)

Welcome to the v0.34.0 release of buildx!

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Tõnis Tiigi
* Sebastiaan van Stijn
* Jonathan A. Sternberg
* Guillaume Lours
* Hervé Le Meur
* Mateusz Gozdek

### Notable Changes

* Buildx now supports a default source policy for common build pipeline images that are provided by Docker Inc and signed by [Docker GitHub builder](https://github.com/docker/github-builder). These include `docker/dockerfile` frontend (including `docker/dockerfile-upstream` staging area) and `docker/buildkit-syft-scanner` image used for SBOM generation. These images are cryptographically verified to be authentic releases before they are used in builds. This feature is currently opt-in behind the `BUILDX_DEFAULT_POLICY` environment variable, but the intention is to enable it by default in a future release [#3807](https://github.com/docker/buildx/pull/3807)
* Add `--policy` flag to `bake` command to specify global policy evaluation options. [#3832](https://github.com/docker/buildx/pull/3832)
* Kubernetes driver now supports persistent storage options that change the deployment definition to use a StatefulSet and a persistent volume claim. [#3766](https://github.com/docker/buildx/pull/3766)
* Fix issue where progress policy errors may have been lost in progress output. [#3838](https://github.com/docker/buildx/pull/3838)
* Fix stopping `dial-stdio` command when the builder connection closes [#3790](https://github.com/docker/buildx/pull/3790)
* Fix possible panic in `buildx debug` command when solving fails [#3823](https://github.com/docker/buildx/pull/3823)
* Fix handling of Windows paths in local OCI layout definitions [#3825](https://github.com/docker/buildx/pull/3825) [#3820](https://github.com/docker/buildx/pull/3820) [#3812](https://github.com/docker/buildx/pull/3812)
* Fix possible incorrect error when using `rm` commands on Docker context based builders [#3817](https://github.com/docker/buildx/pull/3817)
* Fix possible cache miss due to nondeterministic ordering of extra hosts [#3789](https://github.com/docker/buildx/pull/3789)
* Fix mounting of WSL libraries for GPU devices only on local docker-container endpoints [#3784](https://github.com/docker/buildx/pull/3784)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.4 -> v1.41.7
* **github.com/aws/aws-sdk-go-v2/config** v1.32.12 -> v1.32.17
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.12 -> v1.19.16
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.20 -> v1.18.23
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.20 -> v1.4.23
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.20 -> v2.7.23
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.24 ***new***
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.7 -> v1.13.9
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.20 -> v1.13.23
* **github.com/aws/aws-sdk-go-v2/service/signin** v1.0.8 -> v1.0.11
* **github.com/aws/aws-sdk-go-v2/service/sso** v1.30.13 -> v1.30.17
* **github.com/aws/aws-sdk-go-v2/service/ssooidc** v1.35.17 -> v1.35.21
* **github.com/aws/aws-sdk-go-v2/service/sts** v1.41.9 -> v1.42.1
* **github.com/aws/smithy-go** v1.24.2 -> v1.25.1
* **github.com/clipperhouse/uax29/v2** v2.2.0 ***new***
* **github.com/compose-spec/compose-go/v2** v2.9.1 -> v2.10.2
* **github.com/containerd/containerd/v2** v2.2.2 -> v2.2.3
* **github.com/docker/cli** v29.3.1 -> v29.4.3
* **github.com/docker/go-connections** v0.6.0 -> v0.7.0
* **github.com/mattn/go-runewidth** v0.0.16 -> v0.0.23
* **github.com/moby/buildkit** v0.29.0 -> v0.30.0
* **github.com/moby/moby/api** v1.54.0 -> v1.54.2
* **github.com/moby/moby/client** v0.3.0 -> v0.4.1
* **github.com/moby/policy-helpers** b7c0b994300b -> a39d60132186
* **github.com/moby/spdystream** v0.5.0 -> v0.5.1
* **go.opentelemetry.io/otel/exporters/stdout/stdouttrace** v1.38.0 -> v1.42.0
* **go.opentelemetry.io/otel/metric** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/sdk** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/sdk/metric** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/trace** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/proto/otlp** v1.9.0 -> v1.10.0
* **go.yaml.in/yaml/v4** v4.0.0-rc.4 ***new***
* **golang.org/x/crypto** v0.48.0 -> v0.50.0
* **golang.org/x/mod** v0.33.0 -> v0.34.0
* **golang.org/x/net** v0.51.0 -> v0.53.0
* **golang.org/x/oauth2** v0.34.0 -> v0.36.0
* **golang.org/x/sync** v0.19.0 -> v0.20.0
* **golang.org/x/sys** v0.42.0 -> v0.43.0
* **golang.org/x/term** v0.41.0 -> v0.42.0
* **golang.org/x/text** v0.34.0 -> v0.36.0
* **golang.org/x/time** v0.14.0 -> v0.15.0
* **golang.org/x/tools** v0.41.0 -> v0.43.0
* **google.golang.org/genproto/googleapis/api** 8636f8732409 -> 6f92a3bedf2d
* **google.golang.org/genproto/googleapis/rpc** 8636f8732409 -> 6f92a3bedf2d
* **google.golang.org/grpc** v1.79.3 -> v1.80.0
* **k8s.io/api** v0.35.2 -> v0.35.4
* **k8s.io/apimachinery** v0.35.2 -> v0.35.4
* **k8s.io/client-go** v0.35.2 -> v0.35.4

Previous release can be found at [v0.33.0](https://github.com/docker/buildx/releases/tag/v0.33.0)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

2 people reacted

## v0.34.0-rc2

11 May 22:09

[github-actions](/apps/github-actions)

[v0.34.0-rc2](/docker/buildx/tree/v0.34.0-rc2)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`ee42096`](/docker/buildx/commit/ee42096f31cceca381335b00a010ca8eb14089d7)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.34.0-rc2](/docker/buildx/releases/tag/v0.34.0-rc2) Pre-release

Pre-release

buildx 0.34.0-rc2

Welcome to the v0.34.0-rc2 release of buildx!\
*This is a pre-release of buildx*

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* Tõnis Tiigi
* CrazyMax

### Notable Changes

* Add `--policy` flag to `bake` command to specify global policy evaluation options. [#3832](https://github.com/docker/buildx/pull/3832)
* Fix issue where progress policy errors may have been lost in progress output. [#3838](https://github.com/docker/buildx/pull/3838)

### Dependency Changes

* **github.com/go-openapi/runtime** v0.29.2 -> v0.29.3
* **github.com/go-openapi/swag** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/cmdutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/netutils** v0.25.4 -> v0.25.5
* **github.com/moby/buildkit** v0.30.0-rc1 -> v0.30.0-rc2
* **github.com/moby/policy-helpers** b7c0b994300b -> a39d60132186
* **github.com/sigstore/sigstore** v1.10.4 -> v1.10.5
* **github.com/sigstore/timestamp-authority/v2** v2.0.3 -> v2.0.6

Previous release can be found at [v0.34.0-rc1](https://github.com/docker/buildx/releases/tag/v0.34.0-rc1)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

## v0.34.0-rc1

07 May 01:33

[github-actions](/apps/github-actions)

[v0.34.0-rc1](/docker/buildx/tree/v0.34.0-rc1)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`9392590`](/docker/buildx/commit/9392590cfa63ce4065b32f9d1daa6844eedf00e4)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.34.0-rc1](/docker/buildx/releases/tag/v0.34.0-rc1) Pre-release

Pre-release

buildx 0.34.0-rc1

Welcome to the v0.34.0-rc1 release of buildx!\
*This is a pre-release of buildx*

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Tõnis Tiigi
* Sebastiaan van Stijn
* Jonathan A. Sternberg
* Guillaume Lours
* Hervé Le Meur
* Mateusz Gozdek

### Notable Changes

* Buildx now supports a default source policy for common build pipeline images that are provided by Docker Inc and signed by [Docker GitHub builder](https://github.com/docker/github-builder). These include `docker/dockerfile` frontend (including `docker/dockerfile-upstream` staging area) and `docker/buildkit-syft-scanner` image used for SBOM generation. These images are cryptographically verified to be authentic releases before they are used in builds. This feature is currently opt-in behind the `BUILDX_DEFAULT_POLICY` environment variable, but the intention is to enable it by default in a future release [#3807](https://github.com/docker/buildx/pull/3807)
* Kubernetes driver now supports persistent storage options that change the deployment definition to use a StatefulSet and a persistent volume claim. [#3766](https://github.com/docker/buildx/pull/3766)
* Fix stopping `dial-stdio` command when the builder connection closes [#3790](https://github.com/docker/buildx/pull/3790)
* Fix possible panic in `buildx debug` command when solving fails [#3823](https://github.com/docker/buildx/pull/3823)
* Fix handling of Windows paths in local OCI layout definitions [#3825](https://github.com/docker/buildx/pull/3825) [#3820](https://github.com/docker/buildx/pull/3820) [#3812](https://github.com/docker/buildx/pull/3812)
* Fix possible incorrect error when using `rm` commands on Docker context based builders [#3817](https://github.com/docker/buildx/pull/3817)
* Fix possible cache miss due to nondeterministic ordering of extra hosts [#3789](https://github.com/docker/buildx/pull/3789)
* Fix mounting of WSL libraries for GPU devices only on local docker-container endpoints [#3784](https://github.com/docker/buildx/pull/3784)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.4 -> v1.41.7
* **github.com/aws/aws-sdk-go-v2/config** v1.32.12 -> v1.32.17
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.12 -> v1.19.16
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.20 -> v1.18.23
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.20 -> v1.4.23
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.20 -> v2.7.23
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.24 ***new***
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.7 -> v1.13.9
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.20 -> v1.13.23
* **github.com/aws/aws-sdk-go-v2/service/signin** v1.0.8 -> v1.0.11
* **github.com/aws/aws-sdk-go-v2/service/sso** v1.30.13 -> v1.30.17
* **github.com/aws/aws-sdk-go-v2/service/ssooidc** v1.35.17 -> v1.35.21
* **github.com/aws/aws-sdk-go-v2/service/sts** v1.41.9 -> v1.42.1
* **github.com/aws/smithy-go** v1.24.2 -> v1.25.1
* **github.com/clipperhouse/uax29/v2** v2.2.0 ***new***
* **github.com/compose-spec/compose-go/v2** v2.9.1 -> v2.10.2
* **github.com/containerd/containerd/v2** v2.2.2 -> v2.2.3
* **github.com/docker/cli** v29.3.1 -> v29.4.2
* **github.com/docker/go-connections** v0.6.0 -> v0.7.0
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.27.7 -> v2.28.0
* **github.com/in-toto/in-toto-golang** v0.10.0 -> v0.11.0
* **github.com/klauspost/compress** v1.18.5 -> v1.18.6
* **github.com/mattn/go-runewidth** v0.0.16 -> v0.0.23
* **github.com/moby/buildkit** v0.29.0 -> v0.30.0-rc1
* **github.com/moby/moby/api** v1.54.0 -> v1.54.2
* **github.com/moby/moby/client** v0.3.0 -> v0.4.1
* **github.com/moby/spdystream** v0.5.0 -> v0.5.1
* **go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc** v0.63.0 -> v0.68.0
* **go.opentelemetry.io/contrib/instrumentation/net/http/httptrace/otelhttptrace** v0.63.0 -> v0.68.0
* **go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp** v0.63.0 -> v0.68.0
* **go.opentelemetry.io/otel** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/exporters/stdout/stdouttrace** v1.38.0 -> v1.42.0
* **go.opentelemetry.io/otel/metric** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/sdk** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/sdk/metric** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/trace** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/proto/otlp** v1.9.0 -> v1.10.0
* **go.yaml.in/yaml/v4** v4.0.0-rc.4 ***new***
* **google.golang.org/genproto/googleapis/api** 8636f8732409 -> 6f92a3bedf2d
* **google.golang.org/genproto/googleapis/rpc** 8636f8732409 -> 6f92a3bedf2d
* **google.golang.org/grpc** v1.79.3 -> v1.80.0
* **k8s.io/api** v0.35.2 -> v0.35.4
* **k8s.io/apimachinery** v0.35.2 -> v0.35.4
* **k8s.io/client-go** v0.35.2 -> v0.35.4

Previous release can be found at [v0.33.0](https://github.com/docker/buildx/releases/tag/v0.33.0)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

## v0.33.0

31 Mar 15:32

[github-actions](/apps/github-actions)

[v0.33.0](/docker/buildx/tree/v0.33.0)

[`f7897eb`](/docker/buildx/commit/f7897eba028583e0071642db3c011e860444f8cf)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.33.0](/docker/buildx/releases/tag/v0.33.0)

Welcome to the v0.33.0 release of buildx!

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* Tõnis Tiigi
* CrazyMax
* Jonathan A. Sternberg
* Sebastiaan van Stijn
* rishabh
* Akihiro Suda

### Notable Changes

* Imagetools `create` and `inspect` commands now support OCI layout paths as source and destination that can be used together with registry references [#3721](https://github.com/docker/buildx/pull/3721)
* Bake command supports new builtin functions `formattimestamp` and `unixtimestampparse` for better handling of time values [#3286](https://github.com/docker/buildx/pull/3286)
* DAP debugger support is now generally available without the need for the experimental features flag [#3736](https://github.com/docker/buildx/pull/3736)
* Policy evaluation now supports verifying HTTP sources with PGP signatures through the `verify_http_pgp_signature` builtin [#3677](https://github.com/docker/buildx/pull/3677)
* `policy eval` command now supports `--platform` flag to specify the platform for evaluated image sources [#3738](https://github.com/docker/buildx/pull/3738)
* `policy eval` can now read policy from stdin when `-f -` is used [#3738](https://github.com/docker/buildx/pull/3738)
* `policy eval` flag `--filename` has been renamed to `--file` for consistency with other commands. The previous flag is deprecated. [#3738](https://github.com/docker/buildx/pull/3738)
* Fix issue where `imagetools create` could in some cases upload the same (attestation) manifest multiple times, possibly causing `400` error in some registries [#3731](https://github.com/docker/buildx/pull/3731)
* Fix rejecting empty string values for `BUILDKIT_SYNTAX` build argument override [#3734](https://github.com/docker/buildx/pull/3734)
* Fix possible inconsistent build context contents when using remote bake builds with a subdirectory in context path [#3678](https://github.com/docker/buildx/pull/3678)
* Fix possible formatting issue in `imagetools inspect` based on whitespace in input [#3732](https://github.com/docker/buildx/pull/3732)
* Fix possible error when finalizing build history traces in multi-node builders [#3716](https://github.com/docker/buildx/pull/3716) [#3717](https://github.com/docker/buildx/pull/3717)
* Fix possible build errors when linking Bake multi-platform targets with session attributes like build secrets [#3696](https://github.com/docker/buildx/pull/3696)
* Fix remote Bake git contexts to preserve subdirectory paths [#3682](https://github.com/docker/buildx/pull/3682)
* Fix proxy build-arg override detection when argument casing differs [#3697](https://github.com/docker/buildx/pull/3697)
* Fix DAP breakpoints on the entrypoint line being skipped in some cases [#3691](https://github.com/docker/buildx/pull/3691)
* Fix DAP breakpoint detection on case-insensitive filesystems such as Windows [#3704](https://github.com/docker/buildx/pull/3704)
* Fix DAP source path mapping for Dockerfiles outside the context root or in subdirectories [#3709](https://github.com/docker/buildx/pull/3709)
* Fix DAP stepping by skipping internal build context load steps without source locations [#3712](https://github.com/docker/buildx/pull/3712)
* Fix over-eager DAP input evaluation while stepping through builds [#3687](https://github.com/docker/buildx/pull/3687)
* Fix DAP checks for whether an exec command can run successfully [#3701](https://github.com/docker/buildx/pull/3701)
* Fix DAP debugger exit status reporting and output delivery on session shutdown [#3735](https://github.com/docker/buildx/pull/3735)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.1 -> v1.41.4
* **github.com/aws/aws-sdk-go-v2/config** v1.32.7 -> v1.32.12
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.7 -> v1.19.12
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.17 -> v1.18.20
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.17 -> v1.4.20
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.17 -> v2.7.20
* **github.com/aws/aws-sdk-go-v2/internal/ini** v1.8.4 -> v1.8.6
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.4 -> v1.13.7
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.17 -> v1.13.20
* **github.com/aws/aws-sdk-go-v2/service/signin** v1.0.5 -> v1.0.8
* **github.com/aws/aws-sdk-go-v2/service/sso** v1.30.9 -> v1.30.13
* **github.com/aws/aws-sdk-go-v2/service/ssooidc** v1.35.13 -> v1.35.17
* **github.com/aws/aws-sdk-go-v2/service/sts** v1.41.6 -> v1.41.9
* **github.com/aws/smithy-go** v1.24.0 -> v1.24.2
* **github.com/containerd/containerd/v2** v2.2.1 -> v2.2.2
* **github.com/containerd/ttrpc** v1.2.7 -> v1.2.8
* **github.com/docker/cli** v29.2.1 -> v29.3.1
* **github.com/go-openapi/analysis** v0.24.1 -> v0.24.3
* **github.com/go-openapi/errors** v0.22.6 -> v0.22.7
* **github.com/go-openapi/jsonpointer** v0.22.4 -> v0.22.5
* **github.com/go-openapi/jsonreference** v0.21.4 -> v0.21.5
* **github.com/go-openapi/loads** v0.23.2 -> v0.23.3
* **github.com/go-openapi/spec** v0.22.3 -> v0.22.4
* **github.com/go-openapi/strfmt** v0.25.0 -> v0.26.1
* **github.com/go-openapi/swag/conv** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/fileutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/jsonname** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/jsonutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/loading** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/mangling** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/stringutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/typeutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/yamlutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/validate** v0.25.1 -> v0.25.2
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.27.3 -> v2.27.7
* **github.com/klauspost/compress** v1.18.4 -> v1.18.5
* **github.com/moby/buildkit** v0.28.0 -> v0.29.0
* **github.com/moby/moby/api** v1.53.0 -> v1.54.0
* **github.com/moby/moby/client** v0.2.2 -> v0.3.0
* **github.com/moby/patternmatcher** v0.6.0 -> v0.6.1
* **github.com/moby/policy-helpers** 824747bfdd3c -> b7c0b994300b
* **github.com/oklog/ulid/v2** v2.1.1 ***new***
* **go.opentelemetry.io/otel** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/metric** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/sdk** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/sdk/metric** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/trace** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/proto/otlp** v1.7.1 -> v1.9.0
* **golang.org/x/sys** v0.41.0 -> v0.42.0
* **golang.org/x/term** v0.40.0 -> v0.41.0
* **google.golang.org/genproto/googleapis/api** ff82c1b0f217 -> 8636f8732409
* **google.golang.org/genproto/googleapis/rpc** 0a764e51fe1b -> 8636f8732409
* **google.golang.org/grpc** v1.78.0 -> v1.79.3
* **k8s.io/api** v0.34.1 -> v0.35.2
* **k8s.io/apimachinery** v0.34.1 -> v0.35.2
* **k8s.io/client-go** v0.34.1 -> v0.35.2
* **k8s.io/kube-openapi** f3f2b991d03b -> 589584f1c912
* **k8s.io/utils** 4c0f3b243397 -> bc988d571ff4
* **sigs.k8s.io/json** cfa47c3a1cc8 -> 2d320260d730

Previous release can be found at [v0.32.1](https://github.com/docker/buildx/releases/tag/v0.32.1)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

4 people reacted

## v0.33.0-rc1

26 Mar 01:31

[github-actions](/apps/github-actions)

[v0.33.0-rc1](/docker/buildx/tree/v0.33.0-rc1)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`55e8fa3`](/docker/buildx/commit/55e8fa3b8ebb673f36bae3a4b9cffcaadfcfceb9)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.33.0-rc1](/docker/buildx/releases/tag/v0.33.0-rc1) Pre-release

Pre-release

buildx 0.33.0-rc1

Welcome to the v0.33.0-rc1 release of buildx!\
*This is a pre-release of buildx*

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* Tõnis Tiigi
* CrazyMax
* Jonathan A. Sternberg
* Sebastiaan van Stijn
* rishabh
* Akihiro Suda

### Notable Changes

* Imagetools `create` and `inspect` commands now support OCI layout paths as source and destination that can be used together with registry references [#3721](https://github.com/docker/buildx/pull/3721)
* Bake command supports new builtin functions `formattimestamp` and `unixtimestampparse` for better handling of time values [#3286](https://github.com/docker/buildx/pull/3286)
* DAP debugger support is now generally available without the need for the experimental features flag [#3736](https://github.com/docker/buildx/pull/3736)
* `policy eval` command now supports `--platform` flag to specify the platform for evaluated image sources [#3738](https://github.com/docker/buildx/pull/3738)
* `policy eval` can now read policy from stdin when `-f -` is used [#3738](https://github.com/docker/buildx/pull/3738)
* `policy eval` flag `--filename` has been renamed to `--file` for consistency with other commands. The previous flag is deprecated. [#3738](https://github.com/docker/buildx/pull/3738)
* Fix issue where `imagetools create` could in some cases upload the same (attestation) manifest multiple times, possibly causing `400` error in some registries [#3731](https://github.com/docker/buildx/pull/3731)
* Fix rejecting empty string values for `BUILDKIT_SYNTAX` build argument override [#3734](https://github.com/docker/buildx/pull/3734)
* Fix possible inconsistent build context contents when using remote bake builds with a subdirectory in context path [#3678](https://github.com/docker/buildx/pull/3678)
* Fix possible formatting issue in `imagetools inspect` based on whitespace in input [#3732](https://github.com/docker/buildx/pull/3732)
* Fix possible error when finalizing build history traces in multi-node builders [#3716](https://github.com/docker/buildx/pull/3716) [#3717](https://github.com/docker/buildx/pull/3717)
* Fix possible build errors when linking Bake multi-platform targets with session attributes like build secrets [#3696](https://github.com/docker/buildx/pull/3696)
* Fix remote Bake git contexts to preserve subdirectory paths [#3682](https://github.com/docker/buildx/pull/3682)
* Fix proxy build-arg override detection when argument casing differs [#3697](https://github.com/docker/buildx/pull/3697)
* Fix DAP breakpoints on the entrypoint line being skipped in some cases [#3691](https://github.com/docker/buildx/pull/3691)
* Fix DAP breakpoint detection on case-insensitive filesystems such as Windows [#3704](https://github.com/docker/buildx/pull/3704)
* Fix DAP source path mapping for Dockerfiles outside the context root or in subdirectories [#3709](https://github.com/docker/buildx/pull/3709)
* Fix DAP stepping by skipping internal build context load steps without source locations [#3712](https://github.com/docker/buildx/pull/3712)
* Fix over-eager DAP input evaluation while stepping through builds [#3687](https://github.com/docker/buildx/pull/3687)
* Fix DAP checks for whether an exec command can run successfully [#3701](https://github.com/docker/buildx/pull/3701)
* Fix DAP debugger exit status reporting and output delivery on session shutdown [#3735](https://github.com/docker/buildx/pull/3735)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.1 -> v1.41.4
* **github.com/aws/aws-sdk-go-v2/config** v1.32.7 -> v1.32.12
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.7 -> v1.19.12
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.17 -> v1.18.20
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.17 -> v1.4.20
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.17 -> v2.7.20
* **github.com/aws/aws-sdk-go-v2/internal/ini** v1.8.4 -> v1.8.6
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.4 -> v1.13.7
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.17 -> v1.13.20
* **github.com/aws/aws-sdk-go-v2/service/signin** v1.0.5 -> v1.0.8
* **github.com/aws/aws-sdk-go-v2/service/sso** v1.30.9 -> v1.30.13
* **github.com/aws/aws-sdk-go-v2/service/ssooidc** v1.35.13 -> v1.35.17
* **github.com/aws/aws-sdk-go-v2/service/sts** v1.41.6 -> v1.41.9
* **github.com/aws/smithy-go** v1.24.0 -> v1.24.2
* **github.com/containerd/containerd/v2** v2.2.1 -> v2.2.2
* **github.com/containerd/ttrpc** v1.2.7 -> v1.2.8
* **github.com/docker/cli** v29.2.1 -> v29.3.1
* **github.com/go-openapi/analysis** v0.24.1 -> v0.24.3
* **github.com/go-openapi/errors** v0.22.6 -> v0.22.7
* **github.com/go-openapi/jsonpointer** v0.22.4 -> v0.22.5
* **github.com/go-openapi/jsonreference** v0.21.4 -> v0.21.5
* **github.com/go-openapi/loads** v0.23.2 -> v0.23.3
* **github.com/go-openapi/spec** v0.22.3 -> v0.22.4
* **github.com/go-openapi/strfmt** v0.25.0 -> v0.26.1
* **github.com/go-openapi/swag/conv** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/fileutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/jsonname** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/jsonutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/loading** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/mangling** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/stringutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/typeutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/swag/yamlutils** v0.25.4 -> v0.25.5
* **github.com/go-openapi/validate** v0.25.1 -> v0.25.2
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.27.3 -> v2.27.7
* **github.com/klauspost/compress** v1.18.4 -> v1.18.5
* **github.com/moby/buildkit** v0.28.0 -> v0.29.0-rc1
* **github.com/moby/moby/api** v1.53.0 -> v1.54.0
* **github.com/moby/moby/client** v0.2.2 -> v0.3.0
* **github.com/moby/patternmatcher** v0.6.0 -> v0.6.1
* **github.com/moby/policy-helpers** 824747bfdd3c -> b7c0b994300b
* **github.com/oklog/ulid/v2** v2.1.1 ***new***
* **go.opentelemetry.io/otel** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetricgrpc** v1.38.0 -> v1.39.0
* **go.opentelemetry.io/otel/exporters/otlp/otlpmetric/otlpmetrichttp** v1.38.0 -> v1.39.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracegrpc** v1.38.0 -> v1.39.0
* **go.opentelemetry.io/otel/exporters/otlp/otlptrace/otlptracehttp** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/metric** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/sdk** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/sdk/metric** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/otel/trace** v1.38.0 -> v1.40.0
* **go.opentelemetry.io/proto/otlp** v1.7.1 -> v1.9.0
* **google.golang.org/genproto/googleapis/api** ff82c1b0f217 -> 8636f8732409
* **google.golang.org/genproto/googleapis/rpc** 0a764e51fe1b -> 8636f8732409
* **google.golang.org/grpc** v1.78.0 -> v1.79.3
* **k8s.io/api** v0.34.1 -> v0.35.2
* **k8s.io/apimachinery** v0.34.1 -> v0.35.2
* **k8s.io/client-go** v0.34.1 -> v0.35.2
* **k8s.io/kube-openapi** f3f2b991d03b -> 589584f1c912
* **k8s.io/utils** 4c0f3b243397 -> bc988d571ff4
* **sigs.k8s.io/json** cfa47c3a1cc8 -> 2d320260d730

Previous release can be found at [v0.32.1](https://github.com/docker/buildx/releases/tag/v0.32.1)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

## v0.32.1

04 Mar 20:36

[github-actions](/apps/github-actions)

[v0.32.1](/docker/buildx/tree/v0.32.1)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`d3bfb3f`](/docker/buildx/commit/d3bfb3f4e48a67dda56e957a6636f4fab6c5fcb2)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.32.1](/docker/buildx/releases/tag/v0.32.1)

buildx 0.32.1

Welcome to the v0.32.1 release of buildx!

Please try out the release binaries and report any issues at\
<https://github.com/docker/buildx/issues>.

### Contributors

* CrazyMax
* Tõnis Tiigi

### Notable Changes

* Fix possible error when building private Git repositories with secret credentials directly from remote source [#3694](https://github.com/docker/buildx/pull/3694)

### Dependency Changes

This release has no dependency changes

Previous release can be found at [v0.32.0](https://github.com/docker/buildx/releases/tag/v0.32.0)

Assets 69

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

You can’t perform that action at this time.

----
