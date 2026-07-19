url: https://docs.docker.com/dhi/release-notes/cli/
----

# DHI CLI release notes

***

Table of contents

***

This page lists changes in recent stable releases of the DHI CLI (`docker dhi`). For the full release history, including pre-releases and downloads, see the [dhictl releases on GitHub](https://github.com/docker-hardened-images/dhictl/releases).

## [0.0.4](#004)

*2026-05-25*

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.4)

### [What's New](#whats-new)

* Adds `deb` subcommand for DHI DEB repositories that emits netrc-style credentials for authenticating against DHI DEB repositories

## [0.0.3](#003)

*2026-04-22*

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.3)

### [What's New](#whats-new-1)

* Adds attestation list and get commands for managing attestations
* Adds SBOM subcommand for software bill of materials attestation
* Adds bulk support to prepare command for customizations
* Adds compression field support for customizations
* Adds tag-definition-id column to catalog get output

### [Breaking change](#breaking-change)

We removed the `--output` flags from the few commands that had it (`customization prepare` and `customization get`) in favor of stdout redirections.

```console
# before
dhictl customization prepare --org my-org golang 1.25 --output my-customization.yaml

# after 
dhictl customization prepare --org my-org golang 1.25 > my-customization.yaml
```

## [0.0.2](#002)

*2026-03-19*

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.2)

This is a maintenance release focused on build system improvements.

### [Technical Changes](#technical-changes)

* Disables CGO globally to fix macOS 16 dyld crash and simplify build process

## [0.0.1](#001)

*2026-03-12*

[GitHub release](https://github.com/docker-hardened-images/dhictl/releases/tag/v0.0.1)

This release improves the mirroring functionality in dhictl by allowing command arguments.

### [Improvements](#improvements)

* Mirror start command now accepts arguments for more flexible mirroring operations

## [Earlier releases](#earlier-releases)

For older versions, see the [dhictl releases on GitHub](https://github.com/docker-hardened-images/dhictl/releases).

----
