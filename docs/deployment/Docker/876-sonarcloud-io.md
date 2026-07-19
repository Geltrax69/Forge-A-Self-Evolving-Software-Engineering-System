      url: "https://sonarcloud.io",
    },
  },
});
```

```python
# Include both servers even if only using one
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
```

## [Claude can't access private repositories](#claude-cant-access-private-repositories)

Issue: "I don't have access to that repository".

Solution:

1. Verify your GitHub token has `repo` scope (not just `public_repo`).

2. Test with a public repository first.

3. Ensure the repository owner and name are correct in your `.env`:

   ```plaintext
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

   ```plaintext
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   ```

## [Workflow times out or runs too long](#workflow-times-out-or-runs-too-long)

Issue: Workflow doesn't complete or Claude credits run out.

Solutions:

1. Use `timeoutMs: 0` (TypeScript) or `timeout_ms=0` (Python) for complex workflows to allow unlimited time:

   ```typescript
   await sbx.commands.run(
     `echo '${prompt}' | claude -p --dangerously-skip-permissions`,
     {
       timeoutMs: 0, // No timeout
       onStdout: console.log,
       onStderr: console.log,
     },
   );
   ```

   ```python
   await sbx.commands.run(
       f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
       timeout_ms=0,  # No timeout
       on_stdout=print,
       on_stderr=print,
   )
   ```

2. Break complex workflows into smaller, focused tasks.

3. Monitor your Anthropic API credit usage.

4. Add checkpoints in prompts: "After each step, show progress before continuing".

## [Sandbox cleanup errors](#sandbox-cleanup-errors)

Issue: Sandboxes aren't being cleaned up properly, leading to resource exhaustion.

Solution: Always use proper error handling with cleanup in the `finally` block:

```typescript
async function robustWorkflow() {
  let sbx: Sandbox | undefined;

  try {
    sbx = await Sandbox.betaCreate({
      // ... configuration
    });

    // ... workflow logic
  } catch (error) {
    console.error("Workflow failed:", error);
    process.exit(1);
  } finally {
    if (sbx) {
      console.log("Cleaning up sandbox...");
      await sbx.kill();
    }
  }
}
```

```python
async def robust_workflow():
    sbx = None

    try:
        sbx = await AsyncSandbox.beta_create(
            # ... configuration
        )

        # ... workflow logic

    except Exception as error:
        print(f"Workflow failed: {error}")
        sys.exit(1)
    finally:
        if sbx:
            print("Cleaning up sandbox...")
            await sbx.kill()
```

## [Environment variable not loading](#environment-variable-not-loading)

Issue: Script fails with "undefined" or "None" for environment variables.

Solution:

1. Ensure `dotenv` is loaded at the top of your file:

   ```typescript
   import "dotenv/config";
   ```

2. Verify the `.env` file is in the same directory as your script.

3. Check variable names match exactly (case-sensitive):

   ```typescript
   // .env file
   GITHUB_TOKEN = ghp_xxxxx;

   // In code
   process.env.GITHUB_TOKEN; // Correct
   process.env.github_token; // Wrong - case doesn't match
   ```

1) Ensure `dotenv` is loaded at the top of your file:

   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```

2) Verify the `.env` file is in the same directory as your script.

3) Check variable names match exactly (case-sensitive):

   ```python
   # .env file
   GITHUB_TOKEN=ghp_xxxxx

   # In code
   os.getenv("GITHUB_TOKEN")  # Correct
   os.getenv("github_token")  # Wrong - case doesn't match
   ```

## [SonarQube returns empty results](#sonarqube-returns-empty-results)

Issue: SonarQube analysis returns no projects or issues.

Solution:

1. Verify your SonarCloud organization key is correct.
2. Ensure you have at least one project configured in SonarCloud.
3. Check that your SonarQube token has the necessary permissions.
4. Confirm your project has been analyzed at least once in SonarCloud.

----
url: https://docs.docker.com/guides/testcontainers-go-getting-started/run-tests/
----

# Run tests and next steps

***

Table of contents

***

## [Run the tests](#run-the-tests)

Run all the tests using `go test ./...`. Optionally add the `-v` flag for verbose output:

```console
$ go test -v ./...
```

You should see two Postgres Docker containers start automatically: one for the suite and its two tests, and another for the initial standalone test. All tests should pass. After the tests finish, the containers are stopped and removed automatically.

## [Summary](#summary)

The Testcontainers for Go library helps you write integration tests by using the same type of database (Postgres) that you use in production, instead of mocks. Because you aren't using mocks and instead talk to real services, you're free to refactor code and still verify that the application works as expected.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Testcontainers for Go documentation](https://golang.testcontainers.org/)
* [Testcontainers for Go quickstart](https://golang.testcontainers.org/quickstart/)
* [Testcontainers Postgres module for Go](https://golang.testcontainers.org/modules/postgres/)

----
url: https://docs.docker.com/dhi/core-concepts/cves/
----

# Common Vulnerabilities and Exposures (CVEs)

***

Table of contents

***

## [What are CVEs?](#what-are-cves)

CVEs are publicly disclosed cybersecurity flaws in software or hardware. Each CVE is assigned a unique identifier (e.g., CVE-2024-12345) and includes a standardized description, allowing organizations to track and address vulnerabilities consistently.

In the context of Docker, CVEs often pertain to issues within base images, or application dependencies. These vulnerabilities can range from minor bugs to critical security risks, such as remote code execution or privilege escalation.

## [Why are CVEs important?](#why-are-cves-important)

Regularly scanning and updating Docker images to mitigate CVEs is crucial for maintaining a secure and compliant environment. Ignoring CVEs can lead to severe security breaches, including:

* Unauthorized access: Exploits can grant attackers unauthorized access to systems.
* Data breaches: Sensitive information can be exposed or stolen.
* Service disruptions: Vulnerabilities can be leveraged to disrupt services or cause downtime.
* Compliance violations: Failure to address known vulnerabilities can lead to non-compliance with industry regulations and standards.

## [How Docker Hardened Images help mitigate CVEs](#how-docker-hardened-images-help-mitigate-cves)

Docker Hardened Images (DHIs) are crafted to minimize the risk of CVEs from the outset. By adopting a security-first approach, DHIs offer several advantages in CVE mitigation:

* Reduced attack surface: DHIs are built using a distroless approach, stripping away unnecessary components and packages. This reduction in image size, up to 95% smaller than traditional images, limits the number of potential vulnerabilities, making it harder for attackers to exploit unneeded software.

* Faster CVE remediation: Maintained by Docker with an [enterprise-grade SLA](https://docs.docker.com/go/dhi-sla/), DHIs are continuously updated to address known vulnerabilities. Critical and high-severity CVEs are patched quickly, ensuring that your containers remain secure without manual intervention.

* Proactive vulnerability management: By utilizing DHIs, organizations can proactively manage vulnerabilities. The images come with CVE and Vulnerability Exposure (VEX) feeds, enabling teams to stay informed about potential threats and take necessary actions promptly.

## [Scan images for CVEs](#scan-images-for-cves)

Regularly scanning Docker images for CVEs is essential for maintaining a secure containerized environment. While Docker Scout is integrated into Docker Desktop and the Docker CLI, tools like Grype and Trivy offer alternative scanning capabilities. The following are instructions for using each tool to scan Docker images for CVEs.

### [Docker Scout](#docker-scout)

Docker Scout is integrated into Docker Desktop and the Docker CLI. It provides vulnerability insights, CVE summaries, and direct links to remediation guidance.

#### [Scan a DHI using Docker Scout](#scan-a-dhi-using-docker-scout)

To scan a Docker Hardened Image using Docker Scout, run the following command:

```console
$ docker scout cves dhi.io/<image>:<tag> --platform <platform>
```

Example output:

```plaintext
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v VEX statements obtained from attestation
    v No vulnerable package detected
    ...
```

For more detailed filtering and JSON output, see [Docker Scout CLI reference](/reference/cli/docker/scout/).

### [Grype](#grype)

[Grype](https://github.com/anchore/grype) is an open-source scanner that checks container images against vulnerability databases like the NVD and distro advisories.

#### [Scan a DHI using Grype](#scan-a-dhi-using-grype)

After installing Grype, you can scan a Docker Hardened Image by pulling the image and running the scan command. Grype requires you to export the VEX attestation to a file first:

```console
$ docker pull dhi.io/<image>:<tag>
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
$ grype dhi.io/<image>:<tag> --vex vex.json
```

Example output:

```plaintext
NAME               INSTALLED              FIXED-IN     TYPE  VULNERABILITY     SEVERITY    EPSS%  RISK
libperl5.36        5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl               5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
perl-base          5.36.0-7+deb12u2       (won't fix)  deb   CVE-2023-31484    High        79.45    1.1
...
```

### [Trivy](#trivy)

[Trivy](https://github.com/aquasecurity/trivy) is an open-source vulnerability scanner for containers and other artifacts. It detects vulnerabilities in OS packages and application dependencies.

#### [Scan a DHI using Trivy](#scan-a-dhi-using-trivy)

After installing Trivy, you can scan a Docker Hardened Image by pulling the image and running the scan command:

```console
$ docker pull dhi.io/<image>:<tag>
$ trivy image --scanners vuln --vex repo dhi.io/<image>:<tag>
```

Example output:

```plaintext
Report Summary

┌──────────────────────────────────────────────────────────────────────────────┬────────────┬─────────────────┬─────────┐
│                                    Target                                    │    Type    │ Vulnerabilities │ Secrets │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ dhi.io/<image>:<tag> (debian 12.11)                                          │   debian   │       66        │    -    │
├──────────────────────────────────────────────────────────────────────────────┼────────────┼─────────────────┼─────────┤
│ opt/python-3.13.4/lib/python3.13/site-packages/pip-25.1.1.dist-info/METADATA │ python-pkg │        0        │    -    │
└──────────────────────────────────────────────────────────────────────────────┴────────────┴─────────────────┴─────────┘
```

## [Use VEX to filter known non-exploitable CVEs](#use-vex-to-filter-known-non-exploitable-cves)

Docker Hardened Images include signed [VEX (Vulnerability Exploitability eXchange)](https://docs.docker.com/dhi/core-concepts/vex/) attestations that identify vulnerabilities not relevant to the image’s runtime behavior.

When using Docker Scout or Trivy, these VEX statements are automatically applied using the previous examples, and no manual configuration needed.

To manually retrieve the VEX attestation for tools that support it:

```console
$ docker scout vex get dhi.io/<image>:<tag> --output vex.json
```

> Note
>
> If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use `registry://dhi.io/python:3.13` instead of `dhi.io/python:3.13`.

For example:

```console
$ docker scout vex get dhi.io/python:3.13 --output vex.json
```

This creates a `vex.json` file containing the VEX statements for the specified image. You can then use this file with tools that support VEX to filter out known non-exploitable CVEs.

----
url: https://docs.docker.com/scout/explore/exceptions/
----

# Manage vulnerability exceptions

***

Table of contents

***

Vulnerabilities found in container images sometimes need additional context. Just because an image contains a vulnerable package, it doesn't mean that the vulnerability is exploitable. **Exceptions** in Docker Scout lets you acknowledge accepted risks or address false positives in image analysis.

By negating non-applicable vulnerabilities, you can make it easier for yourself and downstream consumers of your images to understand the security implications of a vulnerability in the context of an image.

In Docker Scout, exceptions are automatically factored into the results. If an image contains an exception that flags a CVE as non-applicable, then that CVE is excluded from analysis results.

## [Create exceptions](#create-exceptions)

To create an exception for an image, you can:

* Create an exception in the [GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/) of Docker Scout Dashboard or Docker Desktop.
* Create a [VEX](https://docs.docker.com/scout/how-tos/create-exceptions-vex/) document and attach it to the image.

The recommended way to create exceptions is to use Docker Scout Dashboard or Docker Desktop. The GUI provides a user-friendly interface for creating exceptions. It also lets you create exceptions for multiple images, or your entire organization, all at once.

## [View exceptions](#view-exceptions)

To view exceptions for images, you need to have the appropriate permissions.

* Exceptions created [using the GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/) are visible to members of your Docker organization. Unauthenticated users or users who aren't members of your organization cannot see these exceptions.
* Exceptions created [using VEX documents](https://docs.docker.com/scout/how-tos/create-exceptions-vex/) are visible to anyone who can pull the image, since the VEX document is stored in the image manifest or on filesystem of the image.

### [View exceptions in Docker Scout Dashboard or Docker Desktop](#view-exceptions-in-docker-scout-dashboard-or-docker-desktop)

The [**Exceptions** tab](https://scout.docker.com/reports/vulnerabilities/exceptions) of the Vulnerabilities page in Docker Scout Dashboard lists all exceptions for for all images in your organization. From here, you can see more details about each exception, the CVEs being suppressed, the images that exceptions apply to, the type of exception and how it was created, and more.

For exceptions created using the [GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/), selecting the action menu lets you edit or remove the exception.

To view all exceptions for a specific image tag:

1. Go to the [Images page](https://scout.docker.com/reports/images).
2. Select the tag that you want to inspect.
3. Open the **Exceptions** tab.

1) Open the **Images** view in Docker Desktop.
2) Open the **Hub** tab.
3) Select the tag you want to inspect.
4) Open the **Exceptions** tab.

### [View exceptions in the CLI](#view-exceptions-in-the-cli)

Availability: Experimental

Requires: Docker Scout CLI [1.15.0](https://docs.docker.com/scout/release-notes/cli/#1150) and later

Vulnerability exceptions are highlighted in the CLI when you run `docker scout cves <image>`. If a CVE is suppressed by an exception, a `SUPPRESSED` label appears next to the CVE ID. Details about the exception are also displayed.

> Important
>
> In order to view exceptions in the CLI, you must configure the CLI to use the same Docker organization that you used to create the exceptions.
>
> To configure an organization for the CLI, run:
>
> ```console
> $ docker scout configure organization <organization>
> ```
>
> Replace `<organization>` with the name of your Docker organization.
>
> You can also set the organization on a per-command basis by using the `--org` flag:
>
> ```console
> $ docker scout cves --org <organization> <image>
> ```

To exclude suppressed CVEs from the output, use the `--ignore-suppressed` flag:

```console
$ docker scout cves --ignore-suppressed <image>
```

----
url: https://docs.docker.com/reference/cli/docker/dhi/mirror/start/
----

# docker dhi mirror start

***

| Description | Start mirroring Docker Hardened Images |
| ----------- | -------------------------------------- |
| Usage       | `docker dhi mirror start`              |

## [Description](#description)

Start mirroring one or more Docker Hardened Images to your organization's registry.

Repository mappings are specified as arguments. The following formats are supported:

source Only the source repository; destination is auto-generated as /dhi- source,destination Source and destination; the destination namespace is filled from config if omitted ns/source,ns/dest Fully qualified source and destination

The source namespace defaults to "dhi" when not specified. The destination namespace defaults to the configured organization (--org or config).

Examples: docker dhi mirror start --org myorg dhi/golang,myorg/dhi-golang dhi/node,myorg/dhi-node docker dhi mirror start --org myorg golang,dhi-golang node,dhi-node docker dhi mirror start --org myorg golang node

## [Options](#options)

| Option               | Default | Description                       |
| -------------------- | ------- | --------------------------------- |
| `-d, --dependencies` |         | Mirrors any existing dependencies |
| `--json`             |         | Output in JSON format             |

----
url: https://docs.docker.com/reference/cli/docker/node/ls/
----

# docker node ls

***

| Description                                                               | List nodes in the swarm    |
| ------------------------------------------------------------------------- | -------------------------- |
| Usage                                                                     | `docker node ls [OPTIONS]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker node list`         |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Lists all the nodes that the Docker Swarm manager knows about. You can filter using the `-f` or `--filter` flag. Refer to the [filtering](#filter) section for more information about available filter options.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                    | Default | Description                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-f, --filter`](#filter) |         | Filter output based on conditions provided                                                                                                                                                                                                                                                                                                                                             |
| [`--format`](#format)     |         | Format output using a custom template: 'table': Print output in table format with column headers (default) 'table TEMPLATE': Print output in table format using the given Go template 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `-q, --quiet`             |         | Only display IDs                                                                                                                                                                                                                                                                                                                                                                       |

## [Examples](#examples)

```console
$ docker node ls

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0    swarm-worker2   Ready   Active
38ciaotwjuritcdtn9npbnkuz    swarm-worker1   Ready   Active
e216jshn25ckzbvmwlnh5jr3g *  swarm-manager1  Ready   Active        Leader
```

> Note
>
> In the above example output, there is a hidden column of `.Self` that indicates if the node is the same node as the current docker daemon. A `*` (e.g., `e216jshn25ckzbvmwlnh5jr3g *`) means this node is the current docker daemon.

### [Filtering (--filter)](#filter)

The filtering flag (`-f` or `--filter`) format is of "key=value". If there is more than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`)

The currently supported filters are:

* [id](#id)
* [label](#label)
* [node.label](#nodelabel)
* [membership](#membership)
* [name](#name)
* [role](#role)

#### [id](#id)

The `id` filter matches all or part of a node's id.

```console
$ docker node ls -f id=1

ID                         HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0  swarm-worker2  Ready   Active
```

#### [label](#label)

The `label` filter matches nodes based on engine labels and on the presence of a `label` alone or a `label` and a value. Engine labels are configured in the [daemon configuration](/reference/cli/dockerd/#daemon-configuration-file). To filter on Swarm `node` labels, use [`node.label` instead](#nodelabel).

The following filter matches nodes with the `foo` label regardless of its value.

```console
$ docker node ls -f "label=foo"

ID                         HOSTNAME       STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0  swarm-worker2  Ready   Active
```

#### [node.label](#nodelabel)

The `node.label` filter matches nodes based on node labels and on the presence of a `node.label` alone or a `node.label` and a value.

The following filter updates nodes to have a `region` node label:

```console
$ docker node update --label-add region=region-a swarm-test-01
$ docker node update --label-add region=region-a swarm-test-02
$ docker node update --label-add region=region-b swarm-test-03
$ docker node update --label-add region=region-b swarm-test-04
```

Show all nodes that have a `region` node label set:

```console
$ docker node ls --filter node.label=region

ID                            HOSTNAME        STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
yg550ettvsjn6g6t840iaiwgb *   swarm-test-01   Ready     Active         Leader           23.0.3
2lm9w9kbepgvkzkkeyku40e65     swarm-test-02   Ready     Active         Reachable        23.0.3
hc0pu7ntc7s4uvj4pv7z7pz15     swarm-test-03   Ready     Active         Reachable        23.0.3
n41b2cijmhifxxvz56vwrs12q     swarm-test-04   Ready     Active                          23.0.3
```

Show all nodes that have a `region` node label, with value `region-a`:

```console
$ docker node ls --filter node.label=region=region-a

ID                            HOSTNAME        STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
yg550ettvsjn6g6t840iaiwgb *   swarm-test-01   Ready     Active         Leader           23.0.3
2lm9w9kbepgvkzkkeyku40e65     swarm-test-02   Ready     Active         Reachable        23.0.3
```

#### [membership](#membership)

The `membership` filter matches nodes based on the presence of a `membership` and a value `accepted` or `pending`.

The following filter matches nodes with the `membership` of `accepted`.

```console
$ docker node ls -f "membership=accepted"

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
1bcef6utixb0l0ca7gxuivsj0    swarm-worker2   Ready   Active
38ciaotwjuritcdtn9npbnkuz    swarm-worker1   Ready   Active
```

#### [name](#name)

The `name` filter matches on all or part of a node hostname.

The following filter matches the nodes with a name equal to `swarm-master` string.

```console
$ docker node ls -f name=swarm-manager1

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
e216jshn25ckzbvmwlnh5jr3g *  swarm-manager1  Ready   Active        Leader
```

#### [role](#role)

The `role` filter matches nodes based on the presence of a `role` and a value `worker` or `manager`.

The following filter matches nodes with the `manager` role.

```console
$ docker node ls -f "role=manager"

ID                           HOSTNAME        STATUS  AVAILABILITY  MANAGER STATUS
e216jshn25ckzbvmwlnh5jr3g *  swarm-manager1  Ready   Active        Leader
```

### [Format the output (--format)](#format)

The formatting options (`--format`) pretty-prints nodes output using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder      | Description                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------- |
| `.ID`            | Node ID                                                                                               |
| `.Self`          | Node of the daemon (`true/false`, `true`indicates that the node is the same as current docker daemon) |
| `.Hostname`      | Node hostname                                                                                         |
| `.Status`        | Node status                                                                                           |
| `.Availability`  | Node availability ("active", "pause", or "drain")                                                     |
| `.ManagerStatus` | Manager status of the node                                                                            |
| `.TLSStatus`     | TLS status of the node ("Ready", or "Needs Rotation" has TLS certificate signed by an old CA)         |
| `.EngineVersion` | Engine version                                                                                        |

When using the `--format` option, the `node ls` command will either output the data exactly as the template declares or, when using the `table` directive, includes column headers as well.

The following example uses a template without headers and outputs the `ID`, `Hostname`, and `TLS Status` entries separated by a colon (`:`) for all nodes:

```console
$ docker node ls --format "{{.ID}}: {{.Hostname}} {{.TLSStatus}}"

e216jshn25ckzbvmwlnh5jr3g: swarm-manager1 Ready
35o6tiywb700jesrt3dmllaza: swarm-worker1 Needs Rotation
```

To list all nodes in JSON format, use the `json` directive:

```console
$ docker node ls --format json
{"Availability":"Active","EngineVersion":"23.0.3","Hostname":"docker-desktop","ID":"k8f4w7qtzpj5sqzclcqafw35g","ManagerStatus":"Leader","Self":true,"Status":"Ready","TLSStatus":"Ready"}
```

----
url: https://docs.docker.com/reference/cli/docker/plugin/rm/
----

# docker plugin rm

***

| Description                                                               | Remove one or more plugins                      |
| ------------------------------------------------------------------------- | ----------------------------------------------- |
| Usage                                                                     | `docker plugin rm [OPTIONS] PLUGIN [PLUGIN...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker plugin remove`                          |

## [Description](#description)

Removes a plugin. You cannot remove a plugin if it is enabled, you must disable a plugin using the [`docker plugin disable`](/reference/cli/docker/plugin/disable/) before removing it, or use `--force`. Use of `--force` is not recommended, since it can affect functioning of running containers using the plugin.

## [Options](#options)

| Option        | Default | Description                           |
| ------------- | ------- | ------------------------------------- |
| `-f, --force` |         | Force the removal of an active plugin |

## [Examples](#examples)

The following example disables and removes the `sample-volume-plugin:latest` plugin:

```console
$ docker plugin disable tiborvass/sample-volume-plugin

tiborvass/sample-volume-plugin

$ docker plugin rm tiborvass/sample-volume-plugin:latest

tiborvass/sample-volume-plugin
```

----
url: https://docs.docker.com/reference/cli/docker/scout/enroll/
----

# docker scout enroll

***

| Description | Enroll an organization with Docker Scout |
| ----------- | ---------------------------------------- |
| Usage       | `docker scout enroll ORG`                |

## [Description](#description)

The `docker scout enroll` command enrolls an organization with Docker Scout.

----
url: https://docs.docker.com/admin/organization/setup/onboard/
----

# Onboard your organization

***

Table of contents

***

Subscription: Team Business

For: Administrators

Learn how to onboard your organization using the Admin Console or Docker Hub.

Onboarding your organization includes:

* Identifying users to help you allocate your subscription seats
* Invite members and owners to your organization
* Secure authentication and authorization for your organization
* Enforce sign-in for Docker Desktop to ensure security best practices

These actions help administrators gain visibility into user activity and enforce security settings. Organization members also receive increased pull limits and other benefits when they are signed in.

## [Prerequisites](#prerequisites)

Before you start onboarding your organization, ensure you:

* Have a Docker Team or Business subscription. For more details, see [Docker subscriptions and features](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdminOnboard).

  > Note
  >
  > When purchasing a self-serve subscription, the on-screen instructions guide you through creating an organization. If you have purchased a subscription through Docker Sales and you have not yet created an organization, see [Create an organization](https://docs.docker.com/admin/organization/setup/orgs/).

* Familiarize yourself with Docker concepts and terminology in the [administration overview](https://docs.docker.com/admin/).

## [Onboard with guided setup](#onboard-with-guided-setup)

The Admin Console has a guided setup to help you onboard your organization. The guided setup's steps consist of basic onboarding tasks. If you want to onboard outside of the guided setup, see [Recommended onboarding steps](https://docs.docker.com/admin/organization/setup/onboard/#recommended-onboarding-steps).

To onboard using the guided setup, navigate to the [Admin Console](https://app.docker.com) and select **Guided setup** in the left-hand navigation.

The guided setup walks you through the following onboarding steps:

* **Invite your team**: Invite owners and members.
* **Manage user access**: Add and verify a domain, manage users with SSO, and enforce Docker Desktop sign-in.
* **Docker Desktop security**: Configure image access management, registry access management, and settings management.

## [Recommended onboarding steps](#recommended-onboarding-steps)

### [Step one: Identify your Docker users](#step-one-identify-your-docker-users)

Identifying your users helps you allocate seats efficiently and ensures they receive your Docker subscription benefits.

1. Identify the Docker users in your organization.

   * If your organization uses device management software, like MDM or Jamf, you can use the device management software to help identify Docker users. See your device management software's documentation for details. You can identify Docker users by checking if Docker Desktop is installed at the following location on each user's machine:

     * Mac: `/Applications/Docker.app`
     * Windows: `C:\Program Files\Docker\Docker`(all-user installation) or `%LOCALAPPDATA%\Programs\DockerDesktop` (per-user installation (Beta))
     * Linux: `/opt/docker-desktop`

   * If your organization doesn't use device management software or your users haven't installed Docker Desktop yet, you can survey your users to identify who is using Docker Desktop.

2. Ask users to update their Docker account's email address to one associated with your organization's domain, or create a new account with that email.

   * To update an account's email address, instruct your users to sign in to [Docker Hub](https://hub.docker.com), and update the email address to their email address in your organization's domain.
   * To create a new account, instruct your users to [sign up](https://hub.docker.com/signup) using their email address associated with your organization's domain. Ensure your users verify their email address.

3. Identify Docker accounts associated with your organization's domain:
   * Ask your Docker sales representative or [contact sales](https://www.docker.com/pricing/contact-sales/) to get a list of Docker accounts that use an email address in your organization's domain.

### [Step two: Invite owners](#step-two-invite-owners)

Owners can help you onboard and manage your organization.

When you create an organization, you are the only owner. It is optional to add additional owners.

To add an owner, invite a user and assign them the owner role. For more details, see [Invite members](https://docs.docker.com/admin/organization/manage/members/) and [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

### [Step three: Invite members](#step-three-invite-members)

When you add users to your organization, you gain visibility into their activity and you can enforce security settings. Your members also receive increased pull limits and other organization wide benefits when they are signed in.

To add a member, invite a user and assign them the member role. For more details, see [Invite members](https://docs.docker.com/admin/organization/manage/members/) and [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

### [Step four: Manage user access with SSO and SCIM](#step-four-manage-user-access-with-sso-and-scim)

Configuring SSO and SCIM is optional and only available to Docker Business subscribers. To upgrade a Docker Team subscription to a Docker Business subscription, see [Change your subscription](https://docs.docker.com/subscription/change/).

Use your identity provider (IdP) to manage members and provision them to Docker automatically via SSO and SCIM. See the following for more details:

* [Configure SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/) to authenticate and add members when they sign in to Docker through your identity provider.

* Optional. [Enforce SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/) to ensure that when users sign in to Docker, they must use SSO.

  > Note
  >
  > Enforcing single sign-on (SSO) and enforcing Docker Desktop sign in are different features. For more details, see [Enforcing sign-in versus enforcing single sign-on (SSO)](https://docs.docker.com/enterprise/security/enforce-sign-in/#enforcing-sign-in-versus-enforcing-single-sign-on-sso).

* [Configure SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) to automatically provision, add, and de-provision members to Docker through your identity provider.

### [Step five: Enforce sign-in for Docker Desktop](#step-five-enforce-sign-in-for-docker-desktop)

By default, members of your organization can use Docker Desktop without signing in. When users don’t sign in as a member of your organization, they don’t receive the [benefits of your organization’s subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdminOnboard) and they can circumvent [Docker’s security features](https://docs.docker.com/enterprise/security/hardened-desktop/).

There are multiple ways you can enforce sign-in, depending on your organization's Docker configuration:

* [Registry key method (Windows only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#registry-key-method-windows-only)
* [`.plist` method (Mac only)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#plist-method-mac-only)
* [`registry.json` method (All)](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#registryjson-method-all)

### [Step six: Manage Docker Desktop security](#step-six-manage-docker-desktop-security)

Docker offers the following security features to manage your organization's security posture:

* [Image Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/image-access-management/): Control which types of images your developers can pull from Docker Hub.
* [Registry Access Management](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/): Define which registries your developers can access.
* [Settings management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/): Set and control Docker Desktop settings for your users.

## [What's next](#whats-next)

* [Manage Docker products](https://docs.docker.com/admin/organization/manage/manage-products/) to configure access and view usage.
* Configure [Hardened Docker Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/) to improve your organization’s security posture for containerized development.
* [Manage your domains](https://docs.docker.com/enterprise/security/domain-management/) to ensure that all Docker users in your domain are part of your organization.

Your Docker subscription provides many more additional features. To learn more, see [Docker subscriptions and features](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdminOnboard).

----
url: https://docs.docker.com/guides/testcontainers-java-quarkus/write-tests/
----

# Write tests with Testcontainers

***

Table of contents

***

## [Quarkus Dev Services](#quarkus-dev-services)

Quarkus Dev Services automatically provisions unconfigured services in development and test mode. When you include an extension and don't configure it, Quarkus starts the relevant service using [Testcontainers](https://www.testcontainers.org/) behind the scenes and wires the application to use that service.

> Note
>
> Dev Services requires a [supported Docker environment](https://www.testcontainers.org/supported_docker_environment/).

Quarkus Dev Services supports most commonly used services like SQL databases, Kafka, RabbitMQ, Redis, and MongoDB. For more information, see the [Quarkus Dev Services guide](https://quarkus.io/guides/dev-services).

## [Write tests for the API endpoints](#write-tests-for-the-api-endpoints)

Test the `GET /api/customers` and `POST /api/customers` endpoints using REST Assured. The `io.rest-assured:rest-assured` library was already added as a test dependency when you generated the project.

Create `CustomerResourceTest.java` and annotate it with `@QuarkusTest`. This bootstraps the application along with the required services using Dev Services. Because you haven't configured datasource properties, Dev Services automatically starts a PostgreSQL database using Testcontainers.

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.junit.jupiter.api.Assertions.assertFalse;

import io.quarkus.test.junit.QuarkusTest;
import io.restassured.common.mapper.TypeRef;
import io.restassured.http.ContentType;
import java.util.List;
import org.junit.jupiter.api.Test;

@QuarkusTest
class CustomerResourceTest {

    @Test
    void shouldGetAllCustomers() {
        List<Customer> customers = given().when()
                .get("/api/customers")
                .then()
                .statusCode(200)
                .extract()
                .as(new TypeRef<>() {});
        assertFalse(customers.isEmpty());
    }

    @Test
    void shouldCreateCustomerSuccessfully() {
        Customer customer = new Customer(null, "John", "john@gmail.com");
        given().contentType(ContentType.JSON)
                .body(customer)
                .when()
                .post("/api/customers")
                .then()
                .statusCode(201)
                .body("name", is("John"))
                .body("email", is("john@gmail.com"));
    }
}
```

Here's what the test does:

* `@QuarkusTest` starts the full Quarkus application with Dev Services enabled.
* Dev Services starts a PostgreSQL container using Testcontainers and configures the datasource automatically.
* `shouldGetAllCustomers()` calls `GET /api/customers` and verifies that seeded data from the Flyway migration is returned.
* `shouldCreateCustomerSuccessfully()` sends a `POST /api/customers` request and verifies the response contains the created customer data.

## [Customize test configuration](#customize-test-configuration)

By default, the Quarkus test instance starts on port 8081 and uses a `postgres:14` Docker image. Customize both by adding these properties to `src/main/resources/application.properties`:

```properties
quarkus.http.test-port=0
quarkus.datasource.devservices.image-name=postgres:15.2-alpine
```

Setting `quarkus.http.test-port=0` starts the application on a random available port, avoiding port conflicts. The `devservices.image-name` property lets you pin the PostgreSQL image to a specific version that matches production.

## [Test with services not supported by Dev Services](#test-with-services-not-supported-by-dev-services)

Your application might use a service that Dev Services doesn't support out of the box. In that case, use `QuarkusTestResourceLifecycleManager` to start the service before the Quarkus application starts for testing.

For example, suppose the application uses CockroachDB. First, add the CockroachDB Testcontainers module dependency:

```xml
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>cockroachdb</artifactId>
    <scope>test</scope>
</dependency>
```

Create a `CockroachDBTestResource` that implements `QuarkusTestResourceLifecycleManager`:

```java
package com.testcontainers.demo;

import io.quarkus.test.common.QuarkusTestResourceLifecycleManager;
import java.util.HashMap;
import java.util.Map;
import org.testcontainers.containers.CockroachContainer;

public class CockroachDBTestResource implements QuarkusTestResourceLifecycleManager {

    CockroachContainer cockroachdb;

    @Override
    public Map<String, String> start() {
        cockroachdb = new CockroachContainer("cockroachdb/cockroach:v22.2.0");
        cockroachdb.start();
        Map<String, String> conf = new HashMap<>();
        conf.put("quarkus.datasource.jdbc.url", cockroachdb.getJdbcUrl());
        conf.put("quarkus.datasource.username", cockroachdb.getUsername());
        conf.put("quarkus.datasource.password", cockroachdb.getPassword());
        return conf;
    }

    @Override
    public void stop() {
        cockroachdb.stop();
    }
}
```

Use the `CockroachDBTestResource` with `@QuarkusTestResource` in a test class:

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.junit.jupiter.api.Assertions.assertFalse;

import io.quarkus.test.common.QuarkusTestResource;
import io.quarkus.test.junit.QuarkusTest;
import io.restassured.common.mapper.TypeRef;
import java.util.List;
import org.junit.jupiter.api.Test;

@QuarkusTest
@QuarkusTestResource(value = CockroachDBTestResource.class, restrictToAnnotatedClass = true)
class CockroachDBTest {

    @Test
    void shouldGetAllCustomers() {
        List<Customer> customers = given().when()
                .get("/api/customers")
                .then()
                .statusCode(200)
                .extract()
                .as(new TypeRef<>() {});
        assertFalse(customers.isEmpty());
    }
}
```

The `restrictToAnnotatedClass = true` attribute ensures the CockroachDB container only starts when running this specific test class, rather than being activated for all tests.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-java-quarkus/run-tests/)

----
url: https://docs.docker.com/guides/testcontainers-java-service-configuration/
----

# Configuration of services running in a container

Table of contents

***

Learn how to initialize and configure Docker containers for testing by copying files into containers and executing commands inside them.

**Time to complete** 15 minutes

In this guide, you will learn how to:

* Initialize containers by copying files into them
* Run commands inside running containers using `execInContainer()`
* Set up a PostgreSQL database with SQL scripts
* Create AWS S3 buckets in LocalStack containers

## [Prerequisites](#prerequisites)

* Java 17+
* Your preferred IDE
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Copy files](https://docs.docker.com/guides/testcontainers-java-service-configuration/copy-files/)

   Initialize containers by copying files into specific locations.

2. [Execute commands](https://docs.docker.com/guides/testcontainers-java-service-configuration/exec-in-container/)

   Run commands inside running containers to initialize services for testing.

----
url: https://docs.docker.com/engine/swarm/networking/
----

# Manage swarm service networks

***

Table of contents

***

This page describes networking for swarm services.

## [Swarm and types of traffic](#swarm-and-types-of-traffic)

A Docker swarm generates two different kinds of traffic:

* Control and management plane traffic: This includes swarm management messages, such as requests to join or leave the swarm. This traffic is always encrypted.

* Application data plane traffic: This includes container traffic and traffic to and from external clients.

## [Key network concepts](#key-network-concepts)

The following three network concepts are important to swarm services:

* Overlay networks manage communications among the Docker daemons participating in the swarm. You can create overlay networks, in the same way as user-defined networks for standalone containers. You can attach a service to one or more existing overlay networks as well, to enable service-to-service communication. Overlay networks are Docker networks that use the `overlay` network driver.

* The ingress network is a special overlay network that facilitates load balancing among a service's nodes. When any swarm node receives a request on a published port, it hands that request off to a module called `IPVS`. `IPVS` keeps track of all the IP addresses participating in that service, selects one of them, and routes the request to it, over the `ingress` network.

  The `ingress` network is created automatically when you initialize or join a swarm. Most users do not need to customize its configuration, but Docker allows you to do so.

* The docker\_gwbridge is a bridge network that connects the overlay networks (including the `ingress` network) to an individual Docker daemon's physical network. By default, each container a service is running is connected to its local Docker daemon host's `docker_gwbridge` network.

  The `docker_gwbridge` network is created automatically when you initialize or join a swarm. Most users do not need to customize its configuration, but Docker allows you to do so.

> Tip
>
> See also [Networking overview](https://docs.docker.com/engine/network/) for more details about Swarm networking in general.

## [Firewall considerations](#firewall-considerations)

Docker daemons participating in a swarm need the ability to communicate with each other over the following ports:

* Port `7946` TCP/UDP for container network discovery.
* Port `4789` UDP (configurable) for the overlay network (including ingress) data path.

When setting up networking in a Swarm, special care should be taken. Consult the [tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts) for an overview.

## [Overlay networking](#overlay-networking)

When you initialize a swarm or join a Docker host to an existing swarm, two new networks are created on that Docker host:

* An overlay network called `ingress`, which handles the control and data traffic related to swarm services. When you create a swarm service and do not connect it to a user-defined overlay network, it connects to the `ingress` network by default.
* A bridge network called `docker_gwbridge`, which connects the individual Docker daemon to the other daemons participating in the swarm.

### [Create an overlay network](#create-an-overlay-network)

To create an overlay network, specify the `overlay` driver when using the `docker network create` command:

```console
$ docker network create \
  --driver overlay \
  my-network
```

The above command doesn't specify any custom options, so Docker assigns a subnet and uses default options. You can see information about the network using `docker network inspect`.

When no containers are connected to the overlay network, its configuration is not very exciting:

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "0001-01-01T00:00:00Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": []
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": null,
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": null
    }
]
```

In the above output, notice that the driver is `overlay` and that the scope is `swarm`, rather than `local`, `host`, or `global` scopes you might see in other types of Docker networks. This scope indicates that only hosts which are participating in the swarm can access this network.

The network's subnet and gateway are dynamically configured when a service connects to the network for the first time. The following example shows the same network as above, but with three containers of a `redis` service connected to it.

```console
$ docker network inspect my-network
[
    {
        "Name": "my-network",
        "Id": "fsf1dmx3i9q75an49z36jycxd",
        "Created": "2017-05-31T18:35:58.877628262Z",
        "Scope": "swarm",
        "Driver": "overlay",
        "EnableIPv6": false,
        "IPAM": {
            "Driver": "default",
            "Options": null,
            "Config": [
                {
                    "Subnet": "10.0.0.0/24",
                    "Gateway": "10.0.0.1"
                }
            ]
        },
        "Internal": false,
        "Attachable": false,
        "Ingress": false,
        "Containers": {
            "0e08442918814c2275c31321f877a47569ba3447498db10e25d234e47773756d": {
                "Name": "my-redis.1.ka6oo5cfmxbe6mq8qat2djgyj",
                "EndpointID": "950ce63a3ace13fe7ef40724afbdb297a50642b6d47f83a5ca8636d44039e1dd",
                "MacAddress": "02:42:0a:00:00:03",
                "IPv4Address": "10.0.0.3/24",
                "IPv6Address": ""
            },
            "88d55505c2a02632c1e0e42930bcde7e2fa6e3cce074507908dc4b827016b833": {
                "Name": "my-redis.2.s7vlybipal9xlmjfqnt6qwz5e",
                "EndpointID": "dd822cb68bcd4ae172e29c321ced70b731b9994eee5a4ad1d807d9ae80ecc365",
                "MacAddress": "02:42:0a:00:00:05",
                "IPv4Address": "10.0.0.5/24",
                "IPv6Address": ""
            },
            "9ed165407384f1276e5cfb0e065e7914adbf2658794fd861cfb9b991eddca754": {
                "Name": "my-redis.3.hbz3uk3hi5gb61xhxol27hl7d",
                "EndpointID": "f62c686a34c9f4d70a47b869576c37dffe5200732e1dd6609b488581634cf5d2",
                "MacAddress": "02:42:0a:00:00:04",
                "IPv4Address": "10.0.0.4/24",
                "IPv6Address": ""
            }
        },
        "Options": {
            "com.docker.network.driver.overlay.vxlanid_list": "4097"
        },
        "Labels": {},
        "Peers": [
            {
                "Name": "moby-e57c567e25e2",
                "IP": "192.168.65.2"
            }
        ]
    }
]
```

### [Customize an overlay network](#customize-an-overlay-network)

There may be situations where you don't want to use the default configuration for an overlay network. For a full list of configurable options, run the command `docker network create --help`. The following are some of the most common options to change.

#### [Configure the subnet and gateway](#configure-the-subnet-and-gateway)

By default, the network's subnet and gateway are configured automatically when the first service is connected to the network. You can configure these when creating a network using the `--subnet` and `--gateway` flags. The following example extends the previous one by configuring the subnet and gateway.

```console
$ docker network create \
  --driver overlay \
  --subnet 10.0.9.0/24 \
  --gateway 10.0.9.99 \
  my-network
```

##### [Using custom default address pools](#using-custom-default-address-pools)

To customize subnet allocation for your Swarm networks, you can [optionally configure them](https://docs.docker.com/engine/swarm/swarm-mode/) during `swarm init`.

For example, the following command is used when initializing Swarm:

```console
$ docker swarm init --default-addr-pool 10.20.0.0/16 --default-addr-pool-mask-length 26
```

Whenever a user creates a network, but does not use the `--subnet` command line option, the subnet for this network will be allocated sequentially from the next available subnet from the pool. If the specified network is already allocated, that network will not be used for Swarm.

Multiple pools can be configured if discontiguous address space is required. However, allocation from specific pools is not supported. Network subnets will be allocated sequentially from the IP pool space and subnets will be reused as they are deallocated from networks that are deleted.

The default mask length can be configured and is the same for all networks. It is set to `/24` by default. To change the default subnet mask length, use the `--default-addr-pool-mask-length` command line option.

> Note
>
> Default address pools can only be configured on `swarm init` and cannot be altered after cluster creation.

##### [Overlay network size limitations](#overlay-network-size-limitations)

Docker recommends creating overlay networks with `/24` blocks. The `/24` overlay network blocks limit the network to 256 IP addresses.

This recommendation addresses [limitations with swarm mode](https://github.com/moby/moby/issues/30820). If you need more than 256 IP addresses, do not increase the IP block size. You can either use `dnsrr` endpoint mode with an external load balancer, or use multiple smaller overlay networks. See [Configure service discovery](#configure-service-discovery) for more information about different endpoint modes.

#### [Configure encryption of application data](#encryption)

Management and control plane data related to a swarm is always encrypted. For more details about the encryption mechanisms, see the [Docker swarm mode overlay network security model](https://docs.docker.com/engine/network/drivers/overlay/).

Application data among swarm nodes is not encrypted by default. To encrypt this traffic on a given overlay network, use the `--opt encrypted` flag on `docker network create`. This enables IPSEC encryption at the level of the vxlan. This encryption imposes a non-negligible performance penalty, so you should test this option before using it in production.

> Note
>
> You must [customize the automatically created ingress](#customize-ingress) to enable encryption. By default, all ingress traffic is unencrypted, as encryption is a network-level option.

## [Attach a service to an overlay network](#attach-a-service-to-an-overlay-network)

To attach a service to an existing overlay network, pass the `--network` flag to `docker service create`, or the `--network-add` flag to `docker service update`.

```console
$ docker service create \
  --replicas 3 \
  --name my-web \
  --network my-network \
  nginx
```

Service containers connected to an overlay network can communicate with each other across it.

To see which networks a service is connected to, use `docker service ls` to find the name of the service, then `docker service ps <service-name>` to list the networks. Alternately, to see which services' containers are connected to a network, use `docker network inspect <network-name>`. You can run these commands from any swarm node which is joined to the swarm and is in a `running` state.

### [Configure service discovery](#configure-service-discovery)

Service discovery is the mechanism Docker uses to route a request from your service's external clients to an individual swarm node, without the client needing to know how many nodes are participating in the service or their IP addresses or ports. You don't need to publish ports which are used between services on the same network. For instance, if you have a WordPress service that stores its data in a MySQL service, and they are connected to the same overlay network, you do not need to publish the MySQL port to the client, only the WordPress HTTP port.

Service discovery can work in two different ways: internal connection-based load-balancing at Layers 3 and 4 using the embedded DNS and a virtual IP (VIP), or external and customized request-based load-balancing at Layer 7 using DNS round robin (DNSRR). You can configure this per service.

* By default, when you attach a service to a network and that service publishes one or more ports, Docker assigns the service a virtual IP (VIP), which is the "front end" for clients to reach the service. Docker keeps a list of all worker nodes in the service, and routes requests between the client and one of the nodes. Each request from the client might be routed to a different node.

* If you configure a service to use DNS round-robin (DNSRR) service discovery, there is not a single virtual IP. Instead, Docker sets up DNS entries for the service such that a DNS query for the service name returns a list of IP addresses, and the client connects directly to one of these.

  DNS round-robin is useful in cases where you want to use your own load balancer, such as HAProxy. To configure a service to use DNSRR, use the flag `--endpoint-mode dnsrr` when creating a new service or updating an existing one.

### [Container discovery](#container-discovery)

For most situations, connect to the service name. Docker load-balances requests across all running tasks ("containers") backing the service. To resolve the IP addresses of all individual tasks backing a service directly, perform a DNS lookup for `tasks.<service-name>`. Docker returns a list of all task IP addresses for that service, one per running replica.

## [Customize the ingress network](#customize-ingress)

Most users never need to configure the `ingress` network, but Docker allows you to do so. This can be useful if the automatically-chosen subnet conflicts with one that already exists on your network, or you need to customize other low-level network settings such as the MTU, or if you want to [enable encryption](#encryption).

Customizing the `ingress` network involves removing and recreating it. This is usually done before you create any services in the swarm. If you have existing services which publish ports, those services need to be removed before you can remove the `ingress` network.

During the time that no `ingress` network exists, existing services which do not publish ports continue to function but are not load-balanced. This affects services which publish ports, such as a WordPress service which publishes port 80.

1. Inspect the `ingress` network using `docker network inspect ingress`, and remove any services whose containers are connected to it. These are services that publish ports, such as a WordPress service which publishes port 80. If all such services are not stopped, the next step fails.

2. Remove the existing `ingress` network:

   ```console
   $ docker network rm ingress

   WARNING! Before removing the routing-mesh network, make sure all the nodes
   in your swarm run the same docker engine version. Otherwise, removal may not
   be effective and functionality of newly created ingress networks will be
   impaired.
   Are you sure you want to continue? [y/N]
   ```

3. Create a new overlay network using the `--ingress` flag, along with the custom options you want to set. This example sets the MTU to 1200, sets the subnet to `10.11.0.0/16`, and sets the gateway to `10.11.0.2`.

   ```console
   $ docker network create \
     --driver overlay \
     --ingress \
     --subnet=10.11.0.0/16 \
     --gateway=10.11.0.2 \
     --opt com.docker.network.driver.mtu=1200 \
     my-ingress
   ```

   > Note
   >
   > You can name your `ingress` network something other than `ingress`, but you can only have one. An attempt to create a second one fails.

4. Restart the services that you stopped in the first step.

## [Customize the docker\_gwbridge](#customize-the-docker_gwbridge)

The `docker_gwbridge` is a virtual bridge that connects the overlay networks (including the `ingress` network) to an individual Docker daemon's physical network. Docker creates it automatically when you initialize a swarm or join a Docker host to a swarm, but it is not a Docker device. It exists in the kernel of the Docker host. If you need to customize its settings, you must do so before joining the Docker host to the swarm, or after temporarily removing the host from the swarm.

You need to have the `brctl` application installed on your operating system in order to delete an existing bridge. The package name is `bridge-utils`.

1. Stop Docker.

2. Use the `brctl show docker_gwbridge` command to check whether a bridge device exists called `docker_gwbridge`. If so, remove it using `brctl delbr docker_gwbridge`.

3. Start Docker. Do not join or initialize the swarm.

4. Create or re-create the `docker_gwbridge` bridge with your custom settings. This example uses the subnet `10.11.0.0/16`. For a full list of customizable options, see [Bridge driver options](/reference/cli/docker/network/create/#bridge-driver-options).

   ```console
   $ docker network create \
   --subnet 10.11.0.0/16 \
   --opt com.docker.network.bridge.name=docker_gwbridge \
   --opt com.docker.network.bridge.enable_icc=false \
   --opt com.docker.network.bridge.enable_ip_masquerade=true \
   docker_gwbridge
   ```

5. Initialize or join the swarm.

## [Use a separate interface for control and data traffic](#use-a-separate-interface-for-control-and-data-traffic)

By default, all swarm traffic is sent over the same interface, including control and management traffic for maintaining the swarm itself and data traffic to and from the service containers.

You can separate this traffic by passing the `--data-path-addr` flag when initializing or joining the swarm. If there are multiple interfaces, `--advertise-addr` must be specified explicitly, and `--data-path-addr` defaults to `--advertise-addr` if not specified. Traffic about joining, leaving, and managing the swarm is sent over the `--advertise-addr` interface, and traffic among a service's containers is sent over the `--data-path-addr` interface. These flags can take an IP address or a network device name, such as `eth0`.

This example initializes a swarm with a separate `--data-path-addr`. It assumes that your Docker host has two different network interfaces: 10.0.0.1 should be used for control and management traffic and 192.168.0.1 should be used for traffic relating to services.

```console
$ docker swarm init --advertise-addr 10.0.0.1 --data-path-addr 192.168.0.1
```

This example joins the swarm managed by host `192.168.99.100:2377` and sets the `--advertise-addr` flag to `eth0` and the `--data-path-addr` flag to `eth1`.

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2d7c \
  --advertise-addr eth0 \
  --data-path-addr eth1 \
  192.168.99.100:2377
```

## [Publish ports on an overlay network](#publish-ports-on-an-overlay-network)

Swarm services connected to the same overlay network effectively expose all ports to each other. For a port to be accessible outside of the service, that port must be *published* using the `-p` or `--publish` flag on `docker service create` or `docker service update`. Both the legacy colon-separated syntax and the newer comma-separated value syntax are supported. The longer syntax is preferred because it is somewhat self-documenting.

| Flag value                                                                                                             | Description                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `-p 8080:80` or `-p published=8080,target=80`                                                                          | Map TCP port 80 on the service to port 8080 on the routing mesh.                                                                              |
| `-p 8080:80/udp` or `-p published=8080,target=80,protocol=udp`                                                         | Map UDP port 80 on the service to port 8080 on the routing mesh.                                                                              |
| `-p 8080:80/tcp -p 8080:80/udp` or `-p published=8080,target=80,protocol=tcp -p published=8080,target=80,protocol=udp` | Map TCP port 80 on the service to TCP port 8080 on the routing mesh, and map UDP port 80 on the service to UDP port 8080 on the routing mesh. |

## [Learn more](#learn-more)

* [Deploy services to a swarm](https://docs.docker.com/engine/swarm/services/)
* [Swarm administration guide](https://docs.docker.com/engine/swarm/admin_guide/)
* [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)
* [Networking overview](https://docs.docker.com/engine/network/)
* [Docker CLI reference](/reference/cli/docker/)

----
url: https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/
----

# Package and release your extension

***

Table of contents

***

This page contains additional information on how to package and distribute extensions.

## [Package your extension](#package-your-extension)

Docker extensions are packaged as Docker images. The entire extension runtime including the UI, backend services (host or VM), and any necessary binary must be included in the extension image. Every extension image must contain a `metadata.json` file at the root of its filesystem that defines the [contents of the extension](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/).

The Docker image must have several [image labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/), providing information about the extension. See how to use [extension labels](https://docs.docker.com/extensions/extensions-sdk/extensions/labels/) to provide extension overview information.

To package and release an extension, you must build a Docker image (`docker build`), and push the image to [Docker Hub](https://hub.docker.com/) (`docker push`) with a specific tag that lets you manage versions of the extension.

## [Release your extension](#release-your-extension)

Docker image tags must follow semver conventions in order to allow fetching the latest version of the extension, and to know if there are updates available. See [semver.org](https://semver.org/) to learn more about semantic versioning.

Extension images must be multi-arch images so that users can install extensions on ARM/AMD hardware. These multi-arch images can include ARM/AMD specific binaries. Mac users will automatically use the right image based on their architecture. Extensions that install binaries on the host must also provide Windows binaries in the same extension image. See how to [build a multi-arch image](https://docs.docker.com/extensions/extensions-sdk/extensions/multi-arch/) for your extension.

You can implement extensions without any constraints on the code repository. Docker doesn't need access to the code repository in order to use the extension. Also, you can manage new releases of your extension, without any dependency on Docker Desktop releases.

## [New releases and updates](#new-releases-and-updates)

You can release a new version of your Docker extension by pushing a new image with a new tag to Docker Hub.

Any new image pushed to an image repository corresponding to an extension defines a new version of that extension. Image tags are used to identify version numbers. Extension versions must follow semver to make it easy to understand and compare versions.

Docker Desktop scans the list of extensions published in the marketplace for new versions, and provides notifications to users when they can upgrade a specific extension. Extensions that aren't part of the Marketplace don't have automatic update notifications at the moment.

Users can download and install the newer version of any extension without updating Docker Desktop itself.

## [Extension API dependencies](#extension-api-dependencies)

Extensions must specify the Extension API version they rely on. Docker Desktop checks the extension's required version, and only proposes to install extensions that are compatible with the current Docker Desktop version installed. Users might need to update Docker Desktop in order to install the latest extensions available.

Extension image labels must specify the API version that the extension relies upon. This allows Docker Desktop to inspect newer versions of extension images without downloading the full extension image upfront.

## [License on extensions and the extension SDK](#license-on-extensions-and-the-extension-sdk)

The [Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) is licensed under the Apache 2.0 License and is free to use.

There is no constraint on how each extension should be licensed, this is up to you to decide when creating a new extension.

----
url: https://docs.docker.com/reference/cli/docker/init/
----

# docker init

***

| Description | Creates Docker-related starter files for your project |
| ----------- | ----------------------------------------------------- |
| Usage       | `docker init [OPTIONS]`                               |

## [Description](#description)

Initialize a project with the files necessary to run the project in a container.

Docker Desktop provides the `docker init` CLI command. Run `docker init` in your project directory to be walked through the creation of the following files with sensible defaults for your project:

* .dockerignore
* Dockerfile
* compose.yaml
* README.Docker.md

If any of the files already exist, a prompt appears and provides a warning as well as giving you the option to overwrite all the files. If `docker-compose.yaml` already exists instead of `compose.yaml`, `docker init` can overwrite it, using `docker-compose.yaml` as the name for the Compose file.

> Warning
>
> You can't recover overwritten files. To back up an existing file before selecting to overwrite it, rename the file or copy it to another directory.

After running `docker init`, you can choose one of the following templates:

* ASP.NET Core: Suitable for an ASP.NET Core application.
* Go: Suitable for a Go server application.
* Java: suitable for a Java application that uses Maven and packages as an uber jar.
* Node: Suitable for a Node server application.
* PHP with Apache: Suitable for a PHP web application.
* Python: Suitable for a Python server application.
* Rust: Suitable for a Rust server application.
* Other: General purpose starting point for containerizing your application.

After `docker init` has completed, you may need to modify the created files and tailor them to your project. Visit the following topics to learn more about the files:

* [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
* [Dockerfile](https://docs.docker.com/reference/dockerfile/)
* [compose.yaml](https://docs.docker.com/compose/intro/compose-application-model/)

## [Options](#options)

| Option      | Default | Description                        |
| ----------- | ------- | ---------------------------------- |
| `--version` |         | Display version of the init plugin |

## [Examples](#examples)

### [Example of running `docker init`](#example-of-running-docker-init)

The following example shows the initial menu after running `docker init`. See the additional examples to view the options for each language or framework.

```console
$ docker init

Welcome to the Docker Init CLI!

This utility will walk you through creating the following files with sensible defaults for your project:
  - .dockerignore
  - Dockerfile
  - compose.yaml
  - README.Docker.md

Let's get started!

? What application platform does your project use?  [Use arrows to move, type to filter]
> PHP with Apache - (detected) suitable for a PHP web application
  Go - suitable for a Go server application
  Java - suitable for a Java application that uses Maven and packages as an uber jar
  Python - suitable for a Python server application
  Node - suitable for a Node server application
  Rust - suitable for a Rust server application
  ASP.NET Core - suitable for an ASP.NET Core application
  Other - general purpose starting point for containerizing your application
  Don't see something you need? Let us know!
  Quit
```

### [Example of selecting Go](#example-of-selecting-go)

The following example shows the prompts that appear after selecting `Go` and example input.

```console
? What application platform does your project use? Go
? What version of Go do you want to use? 1.20
? What's the relative directory (with a leading .) of your main package? .
? What port does your server listen on? 3333

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:3333

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting Node](#example-of-selecting-node)

The following example shows the prompts that appear after selecting `Node` and example input.

```console
? What application platform does your project use? Node
? What version of Node do you want to use? 18
? Which package manager do you want to use? yarn
? Do you want to run "yarn run build" before starting your server? Yes
? What directory is your build output to? (comma-separate if multiple) output
? What command do you want to use to start the app? node index.js
? What port does your server listen on? 8000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting Python](#example-of-selecting-python)

The following example shows the prompts that appear after selecting `Python` and example input.

```console
? What application platform does your project use? Python
? What version of Python do you want to use? 3.8
? What port do you want your app to listen on? 8000
? What is the command to run your app (e.g., gunicorn 'myapp.example:app' --bind=0.0.0.0:8000)? python ./app.py

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting Rust](#example-of-selecting-rust)

The following example shows the prompts that appear after selecting `Rust` and example input.

```console
? What application platform does your project use? Rust
? What version of Rust do you want to use? 1.70.0
? What port does your server listen on? 8000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting ASP.NET Core](#example-of-selecting-aspnet-core)

The following example shows the prompts that appear after selecting `ASP.NET Core` and example input.

```console
? What application platform does your project use? ASP.NET Core
? What's the name of your solution's main project? myapp
? What version of .NET do you want to use? 6.0
? What local port do you want to use to access your server? 8000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:8000

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting PHP with Apache](#example-of-selecting-php-with-apache)

The following example shows the prompts that appear after selecting `PHP with Apache` and example input. The PHP with Apache template is suitable for both pure PHP applications and applications using Composer as a dependency manager. After running `docker init`, you must manually add any PHP extensions that are required by your application to the Dockerfile.

```console
? What application platform does your project use? PHP with Apache
? What version of PHP do you want to use? 8.2
? What's the relative directory (with a leading .) for your app? ./src
? What local port do you want to use to access your server? 9000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

If your application requires specific PHP extensions, you can follow the instructions in the Dockerfile to add them.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:9000

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting Java](#example-of-selecting-java)

The following example shows the prompts that appear after selecting `Java` and example input.

```console
? What application platform does your project use? Java
? What version of Java do you want to use? 17
? What's the relative directory (with a leading .) for your app? ./src
? What port does your server listen on? 9000

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Your application will be available at http://localhost:9000

Consult README.Docker.md for more information about using the generated files.
```

### [Example of selecting Other](#example-of-selecting-other)

The following example shows the output after selecting `Other`.

```console
? What application platform does your project use? Other

CREATED: .dockerignore
CREATED: Dockerfile
CREATED: compose.yaml
CREATED: README.Docker.md

✔ Your Docker files are ready!

Take a moment to review them and tailor them to your application.

When you're ready, start your application by running: docker compose up --build

Consult README.Docker.md for more information about using the generated files.
```

----
url: https://docs.docker.com/build/cache/
----

# Docker build cache

***

Table of contents

***

When you build the same Docker image multiple times, knowing how to optimize the build cache is a great tool for making sure the builds run fast.

## [How the build cache works](#how-the-build-cache-works)

Understanding Docker's build cache helps you write better Dockerfiles that result in faster builds.

The following example shows a small Dockerfile for a program written in C.

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

Each instruction in this Dockerfile translates to a layer in your final image. You can think of image layers as a stack, with each layer adding more content on top of the layers that came before it:

Whenever a layer changes, that layer will need to be re-built. For example, suppose you make a change to your program in the `main.c` file. After this change, the `COPY` command will have to run again in order for those changes to appear in the image. In other words, Docker will invalidate the cache for this layer.

If a layer changes, all other layers that come after it are also affected. When the layer with the `COPY` command gets invalidated, all layers that follow will need to run again, too:

And that's the Docker build cache in a nutshell. Once a layer changes, then all downstream layers need to be rebuilt as well. Even if they wouldn't build anything differently, they still need to re-run.

## [Other resources](#other-resources)

For more information on using cache to do efficient builds, see:

* [Cache invalidation](https://docs.docker.com/build/cache/invalidation/)
* [Optimize build cache](https://docs.docker.com/build-cloud/optimization/)
* [Garbage collection](https://docs.docker.com/build/cache/garbage-collection/)
* [Cache storage backends](https://docs.docker.com/build/cache/backends/)

----
url: https://docs.docker.com/build/ci/github-actions/test-before-push/
----

# Test before push with GitHub Actions

***

***

In some cases, you might want to validate that the image works as expected before pushing it. The following workflow implements several steps to achieve this:

1. Build and export the image to Docker
2. Test your image
3. Multi-platform build and push the image

```yaml
name: ci

on:
  push:

env:
  TEST_TAG: user/app:test
  LATEST_TAG: user/app:latest

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and export to Docker
        uses: docker/build-push-action@v7
        with:
          load: true
          tags: ${{ env.TEST_TAG }}

      - name: Test
        run: |
          docker run --rm ${{ env.TEST_TAG }}

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          platforms: linux/amd64,linux/arm64
          push: true
          tags: ${{ env.LATEST_TAG }}
```

> Note
>
> The `linux/amd64` image is only built once in this workflow. The image is built once, and the following steps use the internal cache from the first `Build and push` step. The second `Build and push` step only builds `linux/arm64`.

----
url: https://docs.docker.com/reference/cli/sbx/create/copilot/
----

# sbx create copilot

| Description | Create a sandbox for copilot                |
| ----------- | ------------------------------------------- |
| Usage       | `sbx create copilot PATH [PATH...] [flags]` |

## [Description](#description)

Create a sandbox with access to a host workspace for copilot.

The workspace path is required and will be mounted inside the sandbox at the same path as on the host. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

Use "sbx run --name SANDBOX" to attach to the agent after creation.

## [Global options](#global-options)

| Option           | Default | Description                                                                                                                                                                                                            |
| ---------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--clone`        |         | Run the agent on a private in-container clone of the host Git repository (mounted read-only) instead of bind-mounting the workspace; the agent's commits are accessible via the sandbox-\<name> git remote on the host |
| `--cpus`         | `0`     | Number of CPUs to allocate to the sandbox (0 = auto: N-1 host CPUs, min 1)                                                                                                                                             |
| `-D, --debug`    |         | Enable debug logging                                                                                                                                                                                                   |
| `--kit`          |         | experimental Kit reference (directory, ZIP, or OCI). Can be specified multiple times                                                                                                                                   |
| `-m, --memory`   |         | Memory limit in binary units (e.g., 1024m, 8g). Default: 50% of host memory, max 32 GiB                                                                                                                                |
| `--name`         |         | Name for the sandbox (default: \<agent>-\<workdir>, letters, numbers, hyphens, periods, plus signs and minus signs only)                                                                                               |
| `-q, --quiet`    |         | Suppress verbose output                                                                                                                                                                                                |
| `-t, --template` |         | Container image to use for the sandbox (default: agent-specific image)                                                                                                                                                 |

## [Examples](#examples)

```console
# Create in the current directory
sbx create copilot .

# Create with a specific path
sbx create copilot /path/to/project

# Create with additional read-only workspaces
sbx create copilot . /path/to/docs:ro
```

----
url: https://docs.docker.com/guides/reactjs/
----

# React.js language-specific guide

Table of contents

***

This guide explains how to containerize React.js applications using Docker.

**Time to complete** 20 minutes

The React.js language-specific guide shows you how to containerize a React.js application using Docker, following best practices for creating efficient, production-ready containers.

[React.js](https://react.dev/) is a widely used library for building interactive user interfaces. However, managing dependencies, environments, and deployments efficiently can be complex. Docker simplifies this process by providing a consistent and containerized environment.

> **Acknowledgment**
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide. As a Docker Captain and experienced Front-end engineer, his expertise in Docker, DevOps, and modern web development has made this resource invaluable for the community, helping developers navigate and optimize their Docker workflows.

***

## [What will you learn?](#what-will-you-learn)

In this guide, you will learn how to:

* Containerize and run a React.js application using Docker.
* Set up a local development environment for React.js inside a container.
* Run tests for your React.js application within a Docker container.
* Configure a CI/CD pipeline using GitHub Actions for your containerized app.
* Deploy the containerized React.js application to a local Kubernetes cluster for testing and debugging.

To begin, you’ll start by containerizing an existing React.js application.

***

## [Prerequisites](#prerequisites)

Before you begin, make sure you're familiar with the following:

* Basic understanding of [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) or [TypeScript](https://www.typescriptlang.org/).
* Basic knowledge of [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm) for managing dependencies and running scripts.
* Familiarity with [React.js](https://react.dev/) fundamentals.
* Understanding of Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

Once you've completed the React.js getting started modules, you’ll be ready to containerize your own React.js application using the examples and instructions provided in this guide.

## [Modules](#modules)

1. [Containerize](https://docs.docker.com/guides/reactjs/containerize/)

   Learn how to containerize a React.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.

2. [Develop your app](https://docs.docker.com/guides/reactjs/develop/)

   Learn how to develop your React.js application locally using containers.

3. [Run your tests](https://docs.docker.com/guides/reactjs/run-tests/)

   Learn how to run your React.js tests in a container.

4. [GitHub Actions CI](https://docs.docker.com/guides/reactjs/configure-github-actions/)

   Learn how to configure CI/CD using GitHub Actions for your React.js application.

5. [Test your deployment](https://docs.docker.com/guides/reactjs/deploy/)

   Learn how to deploy locally to test and debug your Kubernetes deployment

----
url: https://docs.docker.com/docker-hub/repos/archive/
----

# Archive or unarchive a repository

***

Table of contents

***

You can archive a repository on Docker Hub to mark it as read-only and indicate that it's no longer actively maintained. This helps prevent the use of outdated or unsupported images in workflows. Archived repositories can also be unarchived if needed.

Docker Hub highlights repositories that haven't been updated in over a year by displaying an icon ( ) next to them on the [**Repositories** page](https://hub.docker.com/repositories/). Consider reviewing these highlighted repositories and archiving them if necessary.

When a repository is archived, the following occurs:

* The repository information can't be modified.
* New images can't be pushed to the repository.
* An **Archived** label is displayed on the public repository page.
* Users can still pull the images.

You can unarchive an archived repository to remove the archived state. When unarchived, the following occurs:

* The repository information can be modified.
* New images can be pushed to the repository.
* The **Archived** label is removed on the public repository page.

## [Archive a repository](#archive-a-repository)

1. Sign in to [Docker Hub](https://hub.docker.com).

2. Select **My Hub** > **Repositories**.

   A list of your repositories appears.

3. Select a repository.

   The **General** page for the repository appears.

4. Select the **Settings** tab.

5. Select **Archive repository**.

6. Enter the name of your repository to confirm.

7. Select **Archive**.

## [Unarchive a repository](#unarchive-a-repository)

1. Sign in to [Docker Hub](https://hub.docker.com).

2. Select **My Hub** > **Repositories**.

   A list of your repositories appears.

3. Select a repository.

   The **General** page for the repository appears.

4. Select the **Settings** tab.

5. Select **Unarchive repository**.

----
url: https://docs.docker.com/reference/cli/docker/dhi/catalog/get/
----

# docker dhi catalog get

***

| Description | Get details of a Docker Hardened Image |
| ----------- | -------------------------------------- |
| Usage       | `docker dhi catalog get <name>`        |

## [Description](#description)

Get detailed information about a Docker Hardened Image or Helm chart, including available tags and CVE counts

## [Options](#options)

| Option   | Default | Description           |
| -------- | ------- | --------------------- |
| `--json` |         | Output in JSON format |

----
url: https://docs.docker.com/reference/cli/docker/mcp/catalog/server/
----

# docker mcp catalog server

***

| Description | Manage servers in catalogs |
| ----------- | -------------------------- |

## [Description](#description)

Manage servers in catalogs

## [Subcommands](#subcommands)

| Command                                                                                                         | Description                       |
| --------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| [`docker mcp catalog server add`](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/add/)         | Add MCP servers to a catalog      |
| [`docker mcp catalog server inspect`](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/inspect/) | Inspect a server in a catalog     |
| [`docker mcp catalog server ls`](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/ls/)           | List servers in a catalog         |
| [`docker mcp catalog server remove`](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/remove/)   | Remove MCP servers from a catalog |

----
url: https://docs.docker.com/engine/security/apparmor/
----

# AppArmor security profiles for Docker

***

Table of contents

***

AppArmor (Application Armor) is a Linux security module that protects an operating system and its applications from security threats. To use it, a system administrator associates an AppArmor security profile with each program. Docker expects to find an AppArmor policy loaded and enforced.

Docker automatically generates and loads a default profile for containers named `docker-default`. The Docker binary generates this profile in `tmpfs` and then loads it into the kernel.

> Note
>
> This profile is used on containers, not on the Docker daemon.

A profile for the Docker Engine daemon exists but it is not currently installed with the `deb` packages. If you are interested in the source for the daemon profile, it is located in [contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) in the Docker Engine source repository.

## [Understand the policies](#understand-the-policies)

The `docker-default` profile is the default for running containers. It is moderately protective while providing wide application compatibility. The profile is generated from the following [template](https://github.com/moby/profiles/blob/main/apparmor/template.go).

When you run a container, it uses the `docker-default` policy unless you override it with the `security-opt` option. For example, the following explicitly specifies the default policy:

```console
$ docker run --rm -it --security-opt apparmor=docker-default hello-world
```

## [Load and unload profiles](#load-and-unload-profiles)

To load a new profile into AppArmor for use with containers:

```console
$ apparmor_parser -r -W /path/to/your_profile
```

Then, run the custom profile with `--security-opt`:

```console
$ docker run --rm -it --security-opt apparmor=your_profile hello-world
```

To unload a profile from AppArmor:

```console
# unload the profile
$ apparmor_parser -R /path/to/profile
```

### [Resources for writing profiles](#resources-for-writing-profiles)

The syntax for file globbing in AppArmor is a bit different than some other globbing implementations. It is highly suggested you take a look at some of the below resources with regard to AppArmor profile syntax.

* [Quick Profile Language](https://gitlab.com/apparmor/apparmor/wikis/QuickProfileLanguage)
* [Globbing Syntax](https://gitlab.com/apparmor/apparmor/wikis/AppArmor_Core_Policy_Reference#AppArmor_globbing_syntax)

## [Nginx example profile](#nginx-example-profile)

In this example, you create a custom AppArmor profile for Nginx. Below is the custom profile.

```c
#include <tunables/global>


profile docker-nginx flags=(attach_disconnected,mediate_deleted) {
  #include <abstractions/base>

  network inet tcp,
  network inet udp,
  network inet icmp,

  deny network raw,

  deny network packet,

  file,
  umount,

  deny /bin/** wl,
  deny /boot/** wl,
  deny /dev/** wl,
  deny /etc/** wl,
  deny /home/** wl,
  deny /lib/** wl,
  deny /lib64/** wl,
  deny /media/** wl,
  deny /mnt/** wl,
  deny /opt/** wl,
  deny /proc/** wl,
  deny /root/** wl,
  deny /sbin/** wl,
  deny /srv/** wl,
  deny /tmp/** wl,
  deny /sys/** wl,
  deny /usr/** wl,

  audit /** w,

  /var/run/nginx.pid w,

  /usr/sbin/nginx ix,

  deny /bin/dash mrwklx,
  deny /bin/sh mrwklx,
  deny /usr/bin/top mrwklx,


  capability chown,
  capability dac_override,
  capability setuid,
  capability setgid,
  capability net_bind_service,

  deny @{PROC}/* w,   # deny write for all files directly in /proc (not in a subdir)
  # deny write to files not in /proc/<number>/** or /proc/sys/**
  deny @{PROC}/{[^1-9],[^1-9][^0-9],[^1-9s][^0-9y][^0-9s],[^1-9][^0-9][^0-9][^0-9]*}/** w,
  deny @{PROC}/sys/[^k]** w,  # deny /proc/sys except /proc/sys/k* (effectively /proc/sys/kernel)
  deny @{PROC}/sys/kernel/{?,??,[^s][^h][^m]**} w,  # deny everything except shm* in /proc/sys/kernel/
  deny @{PROC}/sysrq-trigger rwklx,
  deny @{PROC}/mem rwklx,
  deny @{PROC}/kmem rwklx,
  deny @{PROC}/kcore rwklx,

  deny mount,

  deny /sys/[^f]*/** wklx,
  deny /sys/f[^s]*/** wklx,
  deny /sys/fs/[^c]*/** wklx,
  deny /sys/fs/c[^g]*/** wklx,
  deny /sys/fs/cg[^r]*/** wklx,
  deny /sys/firmware/** rwklx,
  deny /sys/kernel/security/** rwklx,
}
```

1. Save the custom profile to disk in the `/etc/apparmor.d/containers/docker-nginx` file.

   The file path in this example is not a requirement. In production, you could use another.

2. Load the profile.

   ```console
   $ sudo apparmor_parser -r -W /etc/apparmor.d/containers/docker-nginx
   ```

3. Run a container with the profile.

   To run nginx in detached mode:

   ```console
   $ docker run --security-opt "apparmor=docker-nginx" \
        -p 80:80 -d --name apparmor-nginx nginx
   ```

4. Exec into the running container.

   ```console
   $ docker container exec -it apparmor-nginx bash
   ```

5. Try some operations to test the profile.

   ```console
   root@6da5a2a930b9:~# ping 8.8.8.8
   ping: Lacking privilege for raw socket.

   root@6da5a2a930b9:/# top
   bash: /usr/bin/top: Permission denied

   root@6da5a2a930b9:~# touch ~/thing
   touch: cannot touch 'thing': Permission denied

   root@6da5a2a930b9:/# sh
   bash: /bin/sh: Permission denied

   root@6da5a2a930b9:/# dash
   bash: /bin/dash: Permission denied
   ```

You just deployed a container secured with a custom apparmor profile.

## [Debug AppArmor](#debug-apparmor)

You can use `dmesg` to debug problems and `aa-status` check the loaded profiles.

### [Use dmesg](#use-dmesg)

Here are some helpful tips for debugging any problems you might be facing with regard to AppArmor.

AppArmor sends quite verbose messaging to `dmesg`. Usually an AppArmor line looks like the following:

```text
[ 5442.864673] audit: type=1400 audit(1453830992.845:37): apparmor="ALLOWED" operation="open" profile="/usr/bin/docker" name="/home/jessie/docker/man/man1/docker-attach.1" pid=10923 comm="docker" requested_mask="r" denied_mask="r" fsuid=1000 ouid=0
```

In the above example, you can see `profile=/usr/bin/docker`. This means the user has the `docker-engine` (Docker Engine daemon) profile loaded.

Look at another log line:

```text
[ 3256.689120] type=1400 audit(1405454041.341:73): apparmor="DENIED" operation="ptrace" profile="docker-default" pid=17651 comm="docker" requested_mask="receive" denied_mask="receive"
```

This time the profile is `docker-default`, which is run on containers by default unless in `privileged` mode. This line shows that apparmor has denied `ptrace` in the container. This is exactly as expected.

### [Use aa-status](#use-aa-status)

If you need to check which profiles are loaded, you can use `aa-status`. The output looks like:

```console
$ sudo aa-status
apparmor module is loaded.
14 profiles are loaded.
1 profiles are in enforce mode.
   docker-default
13 profiles are in complain mode.
   /usr/bin/docker
   /usr/bin/docker///bin/cat
   /usr/bin/docker///bin/ps
   /usr/bin/docker///sbin/apparmor_parser
   /usr/bin/docker///sbin/auplink
   /usr/bin/docker///sbin/blkid
   /usr/bin/docker///sbin/iptables
   /usr/bin/docker///sbin/mke2fs
   /usr/bin/docker///sbin/modprobe
   /usr/bin/docker///sbin/tune2fs
   /usr/bin/docker///sbin/xtables-multi
   /usr/bin/docker///sbin/zfs
   /usr/bin/docker///usr/bin/xz
38 processes have profiles defined.
37 processes are in enforce mode.
   docker-default (6044)
   ...
   docker-default (31899)
1 processes are in complain mode.
   /usr/bin/docker (29756)
0 processes are unconfined but have a profile defined.
```

The above output shows that the `docker-default` profile running on various container PIDs is in `enforce` mode. This means AppArmor is actively blocking and auditing in `dmesg` anything outside the bounds of the `docker-default` profile.

The output above also shows the `/usr/bin/docker` (Docker Engine daemon) profile is running in `complain` mode. This means AppArmor only logs to `dmesg` activity outside the bounds of the profile. (Except in the case of Ubuntu Trusty, where some interesting behaviors are enforced.)

## [Contribute to Docker's AppArmor code](#contribute-to-dockers-apparmor-code)

Advanced users and package managers can find a profile for `/usr/bin/docker` (Docker Engine daemon) underneath [contrib/apparmor](https://github.com/moby/moby/tree/master/contrib/apparmor) in the Docker Engine source repository.

The `docker-default` profile for containers lives in [profiles/apparmor](https://github.com/moby/profiles/blob/main/apparmor).

----
url: https://docs.docker.com/guides/gha/
----

[Introduction to GitHub Actions with Docker](https://docs.docker.com/guides/gha/)

Learn how to automate image build and push with GitHub Actions.

DevOps

10 minutes

[« Back to all guides](/guides/)

# Introduction to GitHub Actions with Docker

***

Table of contents

***

This guide provides an introduction to building CI pipelines using Docker and GitHub Actions. You will learn how to use Docker's official GitHub Actions to build your application as a Docker image and push it to Docker Hub. By the end of the guide, you'll have a simple, functional GitHub Actions configuration for Docker builds. Use it as-is, or extend it further to fit your needs.

## [Prerequisites](#prerequisites)

If you want to follow along with the guide, ensure you have the following:

* A verified Docker account.
* Familiarity with Dockerfiles.

This guide assumes basic knowledge of Docker concepts but provides explanations for using Docker in GitHub Actions workflows.

## [Get the sample app](#get-the-sample-app)

This guide is project-agnostic and assumes you have an application with a Dockerfile.

If you need a sample project to follow along, you can use [this sample application](https://github.com/dvdksn/rpg-name-generator.git), which includes a Dockerfile for building a containerized version of the app. Alternatively, use your own GitHub project or create a new repository from the template.

```dockerfile
#syntax=docker/dockerfile:1

# builder installs dependencies and builds the node app
FROM node:lts-alpine AS builder
WORKDIR /src
RUN --mount=src=package.json,target=package.json \
    --mount=src=package-lock.json,target=package-lock.json \
    --mount=type=cache,target=/root/.npm \
    npm ci
COPY . .
RUN --mount=type=cache,target=/root/.npm \
    npm run build

# release creates the runtime image
FROM node:lts-alpine AS release
WORKDIR /app
COPY --from=builder /src/build .
EXPOSE 3000
CMD ["node", "."]
```

## [Configure your GitHub repository](#configure-your-github-repository)

The workflow in this guide pushes the image you build to Docker Hub. To do that, you must authenticate with your Docker credentials (username and access token) as part of the GitHub Actions workflow.

For instructions on how to create a Docker access token, see [Create and manage access tokens](https://docs.docker.com/security/access-tokens/).

Once you have your Docker credentials ready, add the credentials to your GitHub repository so you can use them in GitHub Actions:

1. Open your repository's **Settings**.
2. Under **Security**, go to **Secrets and variables > Actions**.
3. Under **Secrets**, create a new repository secret named `DOCKER_PASSWORD`, containing your Docker access token.
4. Next, under **Variables**, create a `DOCKER_USERNAME` repository variable containing your Docker Hub username.

## [Set up your GitHub Actions workflow](#set-up-your-github-actions-workflow)

GitHub Actions workflows define a series of steps to automate tasks, such as building and pushing Docker images, in response to triggers like commits or pull requests. In this guide, the workflow focuses on automating Docker builds and testing, ensuring your containerized application works correctly before publishing it.

Create a file named `docker-ci.yml` in the `.github/workflows/` directory of your repository. Start with the basic workflow configuration:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:
```

This configuration runs the workflow on pushes to the main branch and on pull requests. By including both triggers, you can ensure that the image builds correctly for a pull request before it's merged.

## [Extract metadata for tags and annotations](#extract-metadata-for-tags-and-annotations)

For the first step in your workflow, use the `docker/metadata-action` to generate metadata for your image. This action extracts information about your Git repository, such as branch names and commit SHAs, and generates image metadata such as tags and annotations.

Add the following YAML to your workflow file:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6
      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image
```

These steps prepare metadata to tag and annotate your images during the build and push process.

* The **Checkout** step clones the Git repository.
* The **Extract Docker image metadata** step extracts Git metadata and generates image tags and annotations for the Docker build.

## [Authenticate to your registry](#authenticate-to-your-registry)

Before you build the image, authenticate to your registry to ensure that you can push your built image to the registry.

To authenticate with Docker Hub, add the following step to your workflow:

```yaml
      - name: Log in to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
```

This step uses the Docker credentials [configured in the repository settings](#configure-your-github-repository).

## [Build and push the image](#build-and-push-the-image)

Finally, build the final production image and push it to your registry. The following configuration builds the image and pushes it directly to a registry.

```yaml
      - name: Build and push Docker image
        uses: docker/build-push-action@v7
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
```

In this configuration:

* `push: ${{ github.event_name != 'pull_request' }}` ensures that images are only pushed when the event is not a pull request. This way, the workflow builds and tests images for pull requests but only pushes images for commits to the main branch.
* `tags` and `annotations` use the outputs from the metadata action to apply consistent tags and [annotations](https://docs.docker.com/build/metadata/annotations/) to the image automatically.

## [Attestations](#attestations)

SBOM (Software Bill of Materials) and provenance attestations improve security and traceability, ensuring your images meet modern software supply chain requirements.

With a small amount of additional configuration, you can configure `docker/build-push-action` to generate Software Bill of Materials (SBOM) and provenance attestations for the image, at build-time.

To generate this additional metadata, you need to make two changes to your workflow:

* Before the build step, add a step that uses `docker/setup-buildx-action`. This action configures your Docker build client with additional capabilities that the default client doesn't support.
* Then, update the **Build and push Docker image** step to also enable SBOM and provenance attestations.

Here's the updated snippet:

```yaml
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v7
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

For more details about attestations, refer to [the documentation](https://docs.docker.com/build/metadata/attestations/).

## [Conclusion](#conclusion)

With all the steps outlined in the previous section, here's the full workflow configuration:

```yaml
name: Build and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Extract Docker image metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ vars.DOCKER_USERNAME }}/my-image

      - name: Log in to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v7
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          annotations: ${{ steps.meta.outputs.annotations }}
          provenance: true
          sbom: true
```

This workflow implements best practices for building and pushing Docker images using GitHub Actions. This configuration can be used as-is or extended with additional features based on your project's needs, such as [multi-platform](https://docs.docker.com/build/building/multi-platform/).

### [Further reading](#further-reading)

* Learn more about advanced configurations and examples in the [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/) section.
* For more complex build setups, you may want to consider [Bake](https://docs.docker.com/build/bake/). (See also the [Mastering Buildx Bake guide](https://docs.docker.com/guides/bake/).)
* Learn about Docker's managed build service, designed for faster, multi-platform builds, see [Docker Build Cloud](https://docs.docker.com/guides/docker-build-cloud/).

----
url: https://docs.docker.com/guides/claude-code-model-runner/
----

[Use Claude Code with Docker Model Runner](https://docs.docker.com/guides/claude-code-model-runner/)

Connect Claude Code to Docker Model Runner with the Anthropic-compatible API, package `gpt-oss` with a larger context window, and inspect requests.

AI

10 minutes

[« Back to all guides](/guides/)

# Use Claude Code with Docker Model Runner

***

Table of contents

***

This guide shows how to run Claude Code with Docker Model Runner as the backend model provider. You'll point Claude Code at the local Anthropic-compatible API, run a coding model, and package `gpt-oss` with a larger context window for longer repository prompts.

> **Acknowledgment**
>
> Docker would like to thank [Pradumna Saraf](https://twitter.com/pradumna_saraf) for his contribution to this guide.

In this guide, you'll learn how to:

* Pull a coding model and start Claude Code with Docker Model Runner
* Make the endpoint configuration persistent
* Verify the local API endpoint and inspect requests
* Package `gpt-oss` with a larger context window for longer prompts

## [Prerequisites](#prerequisites)

Before you start, make sure you have:

* [Docker Desktop](https://docs.docker.com/get-started/get-docker/) or Docker Engine installed
* [Docker Model Runner enabled](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner)
* [Claude Code installed](https://code.claude.com/docs/en/quickstart)

If you use Docker Desktop, turn on TCP access in **Settings** > **AI**, or run:

```console
$ docker desktop enable model-runner --tcp 12434
```

## [Step 1: Pull a coding model](#step-1-pull-a-coding-model)

Pull a model before you start Claude Code:

```console
$ docker model pull ai/devstral-small-2
```

You can also use `ai/qwen3-coder` if you want another coding-focused model with a large context window.

## [Step 2: Start Claude Code with Docker Model Runner](#step-2-start-claude-code-with-docker-model-runner)

Set `ANTHROPIC_BASE_URL` to your local Docker Model Runner endpoint when you run Claude Code.

On macOS or Linux:

```console
$ ANTHROPIC_BASE_URL=http://localhost:12434 claude --model ai/devstral-small-2
```

On Windows PowerShell:

```powershell
$env:ANTHROPIC_BASE_URL="http://localhost:12434"
claude --model ai/devstral-small-2
```

Claude Code now sends requests to Docker Model Runner instead of Anthropic's hosted API.

## [Step 3: Troubleshoot your first launch](#step-3-troubleshoot-your-first-launch)

If Claude Code can't connect, check Docker Model Runner status:

```console
$ docker model status
```

If Claude Code can't find the model, list local models:

```console
$ docker model ls
```

If the model is missing, pull it first. If needed, use the fully qualified model name, such as `ai/devstral-small-2`.

## [Step 4: Make the endpoint persistent](#step-4-make-the-endpoint-persistent)

To avoid setting the environment variable each time, add it to your shell profile:

\~/.bashrc or \~/.zshrc

```bash
export ANTHROPIC_BASE_URL=http://localhost:12434
```

On Windows PowerShell, add it to your PowerShell profile:

$PROFILE

```powershell
$env:ANTHROPIC_BASE_URL = "http://localhost:12434"
```

After you reload your shell, you can run Claude Code with only the model flag:

```console
$ claude --model ai/devstral-small-2
```

## [Step 5: Verify the API endpoint](#step-5-verify-the-api-endpoint)

Send a test request to confirm the Anthropic-compatible API is reachable:

```console
$ curl http://localhost:12434/v1/messages \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ai/devstral-small-2",
    "max_tokens": 32,
    "messages": [{"role": "user", "content": "Say hello"}]
  }'
```

For more details about the request format, see the [Anthropic-compatible API reference](https://docs.docker.com/ai/model-runner/api-reference/#anthropic-compatible-api).

## [Step 6: Inspect Claude Code requests](#step-6-inspect-claude-code-requests)

To inspect the requests Claude Code sends to Docker Model Runner, run:

```console
$ docker model requests --model ai/devstral-small-2 | jq .
```

This helps you debug prompts, context usage, and compatibility issues.

## [Step 7: Package `gpt-oss` with a larger context window](#step-7-package-gpt-oss-with-a-larger-context-window)

`ai/gpt-oss` defaults to a smaller context window than coding-focused models. If you want to use it for repository-scale prompts, package a larger variant:

```console
$ docker model pull ai/gpt-oss
$ docker model package --from ai/gpt-oss --context-size 32000 gpt-oss:32k
```

Then run Claude Code with the packaged model:

```console
$ ANTHROPIC_BASE_URL=http://localhost:12434 claude --model gpt-oss:32k
```

## [Learn more](#learn-more)

* [Docker Model Runner overview](https://docs.docker.com/ai/model-runner/)
* [Docker Model Runner API reference](https://docs.docker.com/ai/model-runner/api-reference/)
* [IDE and tool integrations](https://docs.docker.com/ai/model-runner/ide-integrations/)

----
url: https://docs.docker.com/dhi/core-concepts/fips/
----

# FIPS

***

Table of contents

***

Subscription: Docker Hardened Images Select or Enterprise

## [What is FIPS 140?](#what-is-fips-140)

[FIPS 140](https://csrc.nist.gov/publications/detail/fips/140/3/final) is a U.S. government standard that defines security requirements for cryptographic modules that protect sensitive information. It is widely used in regulated environments such as government, healthcare, and financial services.

FIPS certification is managed by the [NIST Cryptographic Module Validation Program (CMVP)](https://csrc.nist.gov/projects/cryptographic-module-validation-program), which ensures cryptographic modules meet rigorous security standards.

## [Why FIPS compliance matters](#why-fips-compliance-matters)

FIPS 140 compliance is required or strongly recommended in many regulated environments where sensitive data must be protected, such as government, healthcare, finance, and defense. These standards ensure that cryptographic operations are performed using vetted, trusted algorithms implemented in secure modules.

Using software components that rely on validated cryptographic modules can help organizations:

* Satisfy federal and industry mandates, such as FedRAMP, which require or strongly recommend FIPS 140-validated cryptography.
* Demonstrate audit readiness, with verifiable evidence of secure, standards-based cryptographic practices.
* Reduce security risk, by blocking unapproved or unsafe algorithms (e.g., MD5) and ensuring consistent behavior across environments.

## [How Docker Hardened Images support FIPS compliance](#how-docker-hardened-images-support-fips-compliance)

While Docker Hardened Images are available to all, the FIPS variant requires a paid Docker Hardened Images subscription.

Docker Hardened Images (DHIs) include variants that use cryptographic modules validated under FIPS 140. These images are intended to help organizations meet compliance requirements by incorporating components that meet the standard.

* FIPS image variants use cryptographic modules that are already validated under FIPS 140.
* These variants are built and maintained by Docker to support environments with regulatory or compliance needs.
* Docker provides signed test attestations that document the use of validated cryptographic modules. These attestations can support internal audits and compliance reporting.
* Entropy sources (random number generation for cryptographic operations) vary by base image. Debian-based images use the OpenSSL entropy source, while Alpine-based images source entropy from the host kernel.

> Note
>
> Using a FIPS image variant helps meet compliance requirements but does not make an application or system fully compliant. Compliance depends on how the image is integrated and used within the broader system.

## [Identify images that support FIPS](#identify-images-that-support-fips)

Docker Hardened Images that support FIPS are marked as **FIPS** compliant in the Docker Hardened Images catalog.

To find DHI repositories with FIPS image variants, [search the catalog](https://docs.docker.com/dhi/how-to/explore/) and:

* Use the **FIPS** filter on the catalog page
* Look for **FIPS** compliant on individual image listings

These indicators help you quickly locate repositories that support FIPS-based compliance needs. Image variants that include FIPS support will have a tag ending with `-fips`, such as `3.13-fips`.

## [Use a FIPS variant](#use-a-fips-variant)

To use a FIPS variant, you must [mirror](https://docs.docker.com/dhi/how-to/mirror/) the repository and then pull the FIPS image from your mirrored repository.

## [View the FIPS attestation](#view-the-fips-attestation)

The FIPS variants of Docker Hardened Images contain a FIPS attestation that lists the actual cryptographic modules included in the image.

You can retrieve and inspect the FIPS attestation using the Docker Scout CLI:

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/fips/v0.1 \
  --predicate \
  dhi.io/<image>:<tag>
```

For example:

```console
$ docker scout attest get \
  --predicate-type https://docker.com/dhi/fips/v0.1 \
  --predicate \
  dhi.io/python:3.13-fips
```

The attestation output is a JSON array describing the cryptographic modules included in the image and their compliance status. For example:

```json
[
  {
    "certification": "CMVP #4985",
    "certificationUrl": "https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4985",
    "name": "OpenSSL FIPS Provider",
    "package": "pkg:dhi/openssl-provider-fips@3.1.2",
    "standard": "FIPS 140-3",
    "status": "active",
    "sunsetDate": "2030-03-10",
    "version": "3.1.2"
  }
]
```

----
url: https://docs.docker.com/engine/storage/drivers/btrfs-driver/
----

# BTRFS storage driver

***

Table of contents

***

> Important
>
> In most cases you should use the `overlay2` storage driver - it's not required to use the `btrfs` storage driver simply because your system uses Btrfs as its root filesystem.
>
> Btrfs driver has known issues. See [Moby issue #27653](https://github.com/moby/moby/issues/27653) for more information.

Btrfs is a copy-on-write filesystem that supports many advanced storage technologies, making it a good fit for Docker. Btrfs is included in the mainline Linux kernel.

Docker's `btrfs` storage driver leverages many Btrfs features for image and container management. Among these features are block-level operations, thin provisioning, copy-on-write snapshots, and ease of administration. You can combine multiple physical block devices into a single Btrfs filesystem.

This page refers to Docker's Btrfs storage driver as `btrfs` and the overall Btrfs Filesystem as Btrfs.

> Note
>
> The `btrfs` storage driver is only supported with Docker Engine CE on SLES, Ubuntu, and Debian systems.

## [Prerequisites](#prerequisites)

`btrfs` is supported if you meet the following prerequisites:

* `btrfs` is only recommended with Docker CE on Ubuntu or Debian systems.

* Changing the storage driver makes any containers you have already created inaccessible on the local system. Use `docker save` to save containers, and push existing images to Docker Hub or a private repository, so that you do not need to re-create them later.

* `btrfs` requires a dedicated block storage device such as a physical disk. This block device must be formatted for Btrfs and mounted into `/var/lib/docker/`. The configuration instructions below walk you through this procedure. By default, the SLES `/` filesystem is formatted with Btrfs, so for SLES, you do not need to use a separate block device, but you can choose to do so for performance reasons.

* `btrfs` support must exist in your kernel. To check this, run the following command:

  ```console
  $ grep btrfs /proc/filesystems

  btrfs
  ```

* To manage Btrfs filesystems at the level of the operating system, you need the `btrfs` command. If you don't have this command, install the `btrfsprogs` package (SLES) or `btrfs-tools` package (Ubuntu).

## [Configure Docker to use the btrfs storage driver](#configure-docker-to-use-the-btrfs-storage-driver)

This procedure is essentially identical on SLES and Ubuntu.

1. Stop Docker.

2. Copy the contents of `/var/lib/docker/` to a backup location, then empty the contents of `/var/lib/docker/`:

   ```console
   $ sudo cp -au /var/lib/docker /var/lib/docker.bk
   $ sudo rm -rf /var/lib/docker/*
   ```

3. Format your dedicated block device or devices as a Btrfs filesystem. This example assumes that you are using two block devices called `/dev/xvdf` and `/dev/xvdg`. Double-check the block device names because this is a destructive operation.

   ```console
   $ sudo mkfs.btrfs -f /dev/xvdf /dev/xvdg
   ```

   There are many more options for Btrfs, including striping and RAID. See the [Btrfs documentation](https://btrfs.wiki.kernel.org/index.php/Using_Btrfs_with_Multiple_Devices).

4. Mount the new Btrfs filesystem on the `/var/lib/docker/` mount point. You can specify any of the block devices used to create the Btrfs filesystem.

   ```console
   $ sudo mount -t btrfs /dev/xvdf /var/lib/docker
   ```

   > Note
   >
   > Make the change permanent across reboots by adding an entry to `/etc/fstab`.

5. Copy the contents of `/var/lib/docker.bk` to `/var/lib/docker/`.

   ```console
   $ sudo cp -au /var/lib/docker.bk/* /var/lib/docker/
   ```

6. Configure Docker to use the `btrfs` storage driver. This is required even though `/var/lib/docker/` is now using a Btrfs filesystem. Edit or create the file `/etc/docker/daemon.json`. If it is a new file, add the following contents. If it is an existing file, add the key and value only, being careful to end the line with a comma if it isn't the final line before an ending curly bracket (`}`).

   ```json
   {
     "storage-driver": "btrfs"
   }
   ```

   See all storage options for each storage driver in the [daemon reference documentation](/reference/cli/dockerd/#options-per-storage-driver)

7. Start Docker. When it's running, verify that `btrfs` is being used as the storage driver.

   ```console
   $ docker info

   Containers: 0
    Running: 0
    Paused: 0
    Stopped: 0
   Images: 0
   Server Version: 17.03.1-ce
   Storage Driver: btrfs
    Build Version: Btrfs v4.4
    Library Version: 101
   <...>
   ```

8. When you are ready, remove the `/var/lib/docker.bk` directory.

## [Manage a Btrfs volume](#manage-a-btrfs-volume)

One of the benefits of Btrfs is the ease of managing Btrfs filesystems without the need to unmount the filesystem or restart Docker.

When space gets low, Btrfs automatically expands the volume in chunks of roughly 1 GB.

To add a block device to a Btrfs volume, use the `btrfs device add` and `btrfs filesystem balance` commands.

```console
$ sudo btrfs device add /dev/svdh /var/lib/docker

$ sudo btrfs filesystem balance /var/lib/docker
```

> Note
>
> While you can do these operations with Docker running, performance suffers. It might be best to plan an outage window to balance the Btrfs filesystem.

## [How the `btrfs` storage driver works](#how-the-btrfs-storage-driver-works)

The `btrfs` storage driver works differently from other storage drivers in that your entire `/var/lib/docker/` directory is stored on a Btrfs volume.

### [Image and container layers on-disk](#image-and-container-layers-on-disk)

Information about image layers and writable container layers is stored in `/var/lib/docker/btrfs/subvolumes/`. This subdirectory contains one directory per image or container layer, with the unified filesystem built from a layer plus all its parent layers. Subvolumes are natively copy-on-write and have space allocated to them on-demand from an underlying storage pool. They can also be nested and snapshotted. The diagram below shows 4 subvolumes. 'Subvolume 2' and 'Subvolume 3' are nested, whereas 'Subvolume 4' shows its own internal directory tree.

Only the base layer of an image is stored as a true subvolume. All the other layers are stored as snapshots, which only contain the differences introduced in that layer. You can create snapshots of snapshots as shown in the diagram below.

On disk, snapshots look and feel just like subvolumes, but in reality they are much smaller and more space-efficient. Copy-on-write is used to maximize storage efficiency and minimize layer size, and writes in the container's writable layer are managed at the block level. The following image shows a subvolume and its snapshot sharing data.

For maximum efficiency, when a container needs more space, it is allocated in chunks of roughly 1 GB in size.

Docker's `btrfs` storage driver stores every image layer and container in its own Btrfs subvolume or snapshot. The base layer of an image is stored as a subvolume whereas child image layers and containers are stored as snapshots. This is shown in the diagram below.

The high level process for creating images and containers on Docker hosts running the `btrfs` driver is as follows:

1. The image's base layer is stored in a Btrfs *subvolume* under `/var/lib/docker/btrfs/subvolumes`.

2. Subsequent image layers are stored as a Btrfs *snapshot* of the parent layer's subvolume or snapshot, but with the changes introduced by this layer. These differences are stored at the block level.

3. The container's writable layer is a Btrfs snapshot of the final image layer, with the differences introduced by the running container. These differences are stored at the block level.

## [How container reads and writes work with `btrfs`](#how-container-reads-and-writes-work-with-btrfs)

### [Reading files](#reading-files)

A container is a space-efficient snapshot of an image. Metadata in the snapshot points to the actual data blocks in the storage pool. This is the same as with a subvolume. Therefore, reads performed against a snapshot are essentially the same as reads performed against a subvolume.

### [Writing files](#writing-files)

As a general caution, writing and updating a large number of small files with Btrfs can result in slow performance.

Consider three scenarios where a container opens a file for write access with Btrfs.

#### [Writing new files](#writing-new-files)

Writing a new file to a container invokes an allocate-on-demand operation to allocate new data block to the container's snapshot. The file is then written to this new space. The allocate-on-demand operation is native to all writes with Btrfs and is the same as writing new data to a subvolume. As a result, writing new files to a container's snapshot operates at native Btrfs speeds.

#### [Modifying existing files](#modifying-existing-files)

Updating an existing file in a container is a copy-on-write operation (redirect-on-write is the Btrfs terminology). The original data is read from the layer where the file currently exists, and only the modified blocks are written into the container's writable layer. Next, the Btrfs driver updates the filesystem metadata in the snapshot to point to this new data. This behavior incurs minor overhead.

#### [Deleting files or directories](#deleting-files-or-directories)

If a container deletes a file or directory that exists in a lower layer, Btrfs masks the existence of the file or directory in the lower layer. If a container creates a file and then deletes it, this operation is performed in the Btrfs filesystem itself and the space is reclaimed.

## [Btrfs and Docker performance](#btrfs-and-docker-performance)

There are several factors that influence Docker's performance under the `btrfs` storage driver.

> Note
>
> Many of these factors are mitigated by using Docker volumes for write-heavy workloads, rather than relying on storing data in the container's writable layer. However, in the case of Btrfs, Docker volumes still suffer from these draw-backs unless `/var/lib/docker/volumes/` isn't backed by Btrfs.

### [Page caching](#page-caching)

Btrfs doesn't support page cache sharing. This means that each process accessing the same file copies the file into the Docker host's memory. As a result, the `btrfs` driver may not be the best choice for high-density use cases such as PaaS.

### [Small writes](#small-writes)

Containers performing lots of small writes (this usage pattern matches what happens when you start and stop many containers in a short period of time, as well) can lead to poor use of Btrfs chunks. This can prematurely fill the Btrfs filesystem and lead to out-of-space conditions on your Docker host. Use `btrfs filesys show` to closely monitor the amount of free space on your Btrfs device.

### [Sequential writes](#sequential-writes)

Btrfs uses a journaling technique when writing to disk. This can impact the performance of sequential writes, reducing performance by up to 50%.

### [Fragmentation](#fragmentation)

Fragmentation is a natural byproduct of copy-on-write filesystems like Btrfs. Many small random writes can compound this issue. Fragmentation can manifest as CPU spikes when using SSDs or head thrashing when using spinning disks. Either of these issues can harm performance.

If your Linux kernel version is 3.9 or higher, you can enable the `autodefrag` feature when mounting a Btrfs volume. Test this feature on your own workloads before deploying it into production, as some tests have shown a negative impact on performance.

### [SSD performance](#ssd-performance)

Btrfs includes native optimizations for SSD media. To enable these features, mount the Btrfs filesystem with the `-o ssd` mount option. These optimizations include enhanced SSD write performance by avoiding optimization such as seek optimizations that don't apply to solid-state media.

### [Balance Btrfs filesystems often](#balance-btrfs-filesystems-often)

Use operating system utilities such as a `cron` job to balance the Btrfs filesystem regularly, during non-peak hours. This reclaims unallocated blocks and helps to prevent the filesystem from filling up unnecessarily. You can't rebalance a totally full Btrfs filesystem unless you add additional physical block devices to the filesystem.

See the [Btrfs Wiki](https://btrfs.wiki.kernel.org/index.php/Balance_Filters#Balancing_to_fix_filesystem_full_errors).

### [Use fast storage](#use-fast-storage)

Solid-state drives (SSDs) provide faster reads and writes than spinning disks.

### [Use volumes for write-heavy workloads](#use-volumes-for-write-heavy-workloads)

Volumes provide the best and most predictable performance for write-heavy workloads. This is because they bypass the storage driver and don't incur any of the potential overheads introduced by thin provisioning and copy-on-write. Volumes have other benefits, such as allowing you to share data among containers and persisting even when no running container is using them.

## [Related Information](#related-information)

* [Volumes](https://docs.docker.com/engine/storage/volumes/)
* [Understand images, containers, and storage drivers](https://docs.docker.com/engine/storage/drivers/)
* [Select a storage driver](https://docs.docker.com/engine/storage/drivers/select-storage-driver/)

----
url: https://docs.docker.com/reference/cli/docker/scout/quickview/
----

# docker scout quickview

***

| Description                                                               | Quick overview of an image                           |
| ------------------------------------------------------------------------- | ---------------------------------------------------- |
| Usage                                                                     | `docker scout quickview [IMAGE\|DIRECTORY\|ARCHIVE]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker scout qv`                                    |

## [Description](#description)

The `docker scout quickview` command displays a quick overview of an image. It displays a summary of the vulnerabilities in the specified image and vulnerabilities from the base image. If available, it also displays base image refresh and update recommendations.

| Option                | Default             | Description                                                                                          |
| --------------------- | ------------------- | ---------------------------------------------------------------------------------------------------- |
| `--env`               |                     | Name of the environment                                                                              |
| `--ignore-suppressed` |                     | Filter CVEs found in Scout exceptions based on the specified exception scope                         |
| `--latest`            |                     | Latest indexed image                                                                                 |
| `--only-policy`       |                     | Comma separated list of policies to evaluate                                                         |
| `--only-vex-affected` |                     | Filter CVEs by VEX statements with status not affected                                               |
| `--org`               |                     | Namespace of the Docker organization                                                                 |
| `-o, --output`        |                     | Write the report to a file                                                                           |
| `--platform`          |                     | Platform of image to analyze                                                                         |
| `--ref`               |                     | Reference to use if the provided tarball contains multiple references. Can only be used with archive |
| `--vex-author`        | `[<.*@docker.com>]` | List of VEX statement authors to accept                                                              |
| `--vex-location`      |                     | File location of directory or file containing VEX statements                                         |

## [Examples](#examples)

### [Quick overview of an image](#quick-overview-of-an-image)

```console
$ docker scout quickview golang:1.19.4
    ...Pulling
    ✓ Pulled
    ✓ SBOM of image already cached, 278 packages indexed

  Your image  golang:1.19.4                          │    5C     3H     6M    63L
  Base image  buildpack-deps:bullseye-scm            │    5C     1H     3M    48L     6?
  Refreshed base image  buildpack-deps:bullseye-scm  │    0C     0H     0M    42L
                                                     │    -5     -1     -3     -6     -6
  Updated base image  buildpack-deps:sid-scm         │    0C     0H     1M    29L
                                                     │    -5     -1     -2    -19     -6
```

### [Quick overview of the most recently built image](#quick-overview-of-the-most-recently-built-image)

```console
$ docker scout qv
```

### [Quick overview from an SPDX file](#quick-overview-from-an-spdx-file)

```console
$  syft -o spdx-json alpine:3.16.1 | docker scout quickview sbom://
 ✔ Loaded image                                                                                                                              alpine:3.16.1
 ✔ Parsed image                                                                    sha256:3d81c46cd8756ddb6db9ec36fa06a6fb71c287fb265232ba516739dc67a5f07d
 ✔ Cataloged contents                                                                     274a317d88b54f9e67799244a1250cad3fe7080f45249fa9167d1f871218d35f
   ├── ✔ Packages                        [14 packages]
   ├── ✔ File digests                    [75 files]
   ├── ✔ File metadata                   [75 locations]
   └── ✔ Executables                     [16 executables]

  Target   │ <stdin>        │    1C     2H     8M     0L
    digest │  274a317d88b5  │
```

----
url: https://docs.docker.com/reference/cli/docker/mcp/catalog/tag/
----

# docker mcp catalog tag

***

| Description | Create a tagged copy of a catalog                              |
| ----------- | -------------------------------------------------------------- |
| Usage       | `docker mcp catalog tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]` |

## [Description](#description)

Create a new catalog by tagging an existing catalog with a new name or version. This creates a copy of the source catalog with a new reference, similar to Docker image tagging.

## [Examples](#examples)

# [Tag a catalog with a new version](#tag-a-catalog-with-a-new-version)

docker mcp catalog tag mcp/my-catalog:v1 mcp/my-catalog:v2

# [Create a tagged copy with a different name](#create-a-tagged-copy-with-a-different-name)

docker mcp catalog tag mcp/team-catalog:latest mcp/prod-catalog:v1.0

# [Tag without explicit version (uses latest)](#tag-without-explicit-version-uses-latest)

docker mcp catalog tag mcp/my-catalog mcp/my-catalog:backup

----
url: https://docs.docker.com/ai-overview/
----

# Docker AI overview

***

Table of contents

***

Docker provides tools for working with AI across your development workflow. Each tool serves a different purpose.

## [Which tool do I need?](#which-tool-do-i-need)

| I want to...                                                    | Use                                                                            | CLI command      |
| --------------------------------------------------------------- | ------------------------------------------------------------------------------ | ---------------- |
| Get AI help with Docker tasks (containers, images, Dockerfiles) | [Gordon](https://docs.docker.com/ai/gordon/)                                   | `docker ai`      |
| Run AI models locally with an OpenAI-compatible API             | [Model Runner](https://docs.docker.com/ai/model-runner/)                       | `docker model`   |
| Connect AI tools to external services via MCP                   | [MCP Catalog and Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/) | `docker mcp`     |
| Build and orchestrate custom multi-agent teams                  | [Docker Agent](https://docs.docker.com/ai/docker-agent/)                       | `docker agent`   |
| Run coding agents in isolated environments                      | [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/)                      | `docker sandbox` |

## [How these tools relate](#how-these-tools-relate)

**Gordon** is Docker's built-in AI assistant. It helps with Docker-specific tasks like debugging containers, writing Dockerfiles, and managing images. You interact with it through Docker Desktop or the `docker ai` command.

**Docker Agent** is an open-source framework for defining teams of AI agents in YAML. You configure agents with specific roles, models, and tools, then run them from your terminal. Docker Agent is a general-purpose agent runtime, not specific to Docker tasks.

**Docker Sandboxes** provides isolated microVM environments for running coding agents. It supports multiple agents including Claude Code, Codex, Copilot, Gemini, and Docker Agent. Sandboxes is the isolation layer — the agents themselves are separate tools.

**Model Runner** lets you run LLMs locally. Other tools like Docker Agent can use Model Runner as a model provider.

**MCP Catalog and Toolkit** manages connections between AI tools and external services using the Model Context Protocol. Gordon, Docker Agent, and third-party tools can all use MCP servers configured through the Toolkit.

----
url: https://docs.docker.com/engine/release-notes/17.11/
----

# Docker Engine 17.11 release notes

***

Table of contents

***

## [17.11.0-ce](#17110-ce)

2017-11-20

> Important
>
> Docker CE 17.11 is the first Docker release based on [containerd 1.0 beta](https://github.com/containerd/containerd/releases/tag/v1.0.0-beta.2). Docker CE 17.11 and later don't recognize containers started with previous Docker versions. If you use Live Restore, you must stop all containers before upgrading to Docker CE 17.11. If you don't, any containers started by Docker versions that predate 17.11 aren't recognized by Docker after the upgrade and keep running, un-managed, on the system.

### [Builder](#builder)

* Test & Fix build with rm/force-rm matrix [moby/moby#35139](https://github.com/moby/moby/pull/35139)

- Fix build with `--stream` with a large context [moby/moby#35404](https://github.com/moby/moby/pull/35404)

### [Client](#client)

* Hide help flag from help output [docker/cli#645](https://github.com/docker/cli/pull/645)
* Support parsing of named pipes for compose volumes [docker/cli#560](https://github.com/docker/cli/pull/560)
* \[Compose] Cast values to expected type after interpolating values [docker/cli#601](https://github.com/docker/cli/pull/601)

- Add output for "secrets" and "configs" on `docker stack deploy` [docker/cli#593](https://github.com/docker/cli/pull/593)

* Fix flag description for `--host-add` [docker/cli#648](https://github.com/docker/cli/pull/648)

- Do not truncate ID on docker service ps --quiet [docker/cli#579](https://github.com/docker/cli/pull/579)

### [Deprecation](#deprecation)

* Update bash completion and deprecation for synchronous service updates [docker/cli#610](https://github.com/docker/cli/pull/610)

### [Logging](#logging)

* copy to log driver's bufsize, fixes #34887 [moby/moby#34888](https://github.com/moby/moby/pull/34888)

- Add TCP support for GELF log driver [moby/moby#34758](https://github.com/moby/moby/pull/34758)
- Add credentials endpoint option for awslogs driver [moby/moby#35055](https://github.com/moby/moby/pull/35055)

### [Networking](#networking)

* Fix network name masking network ID on delete [moby/moby#34509](https://github.com/moby/moby/pull/34509)
* Fix returned error code for network creation from 500 to 409 [moby/moby#35030](https://github.com/moby/moby/pull/35030)
* Fix tasks fail with error "Unable to complete atomic operation, key modified" [docker/libnetwork#2004](https://github.com/docker/libnetwork/pull/2004)

### [Runtime](#runtime)

* Switch to Containerd 1.0 client [moby/moby#34895](https://github.com/moby/moby/pull/34895)
* Increase container default shutdown timeout on Windows [moby/moby#35184](https://github.com/moby/moby/pull/35184)
* LCOW: API: Add `platform` to /images/create and /build [moby/moby#34642](https://github.com/moby/moby/pull/34642)
* Stop filtering Windows manifest lists by version [moby/moby#35117](https://github.com/moby/moby/pull/35117)
* Use windows console mode constants from Azure/go-ansiterm [moby/moby#35056](https://github.com/moby/moby/pull/35056)
* Windows Daemon should respect DOCKER\_TMPDIR [moby/moby#35077](https://github.com/moby/moby/pull/35077)
* Windows: Fix startup logging [moby/moby#35253](https://github.com/moby/moby/pull/35253)

- Add support for Windows version filtering on pull [moby/moby#35090](https://github.com/moby/moby/pull/35090)

* Fixes LCOW after containerd 1.0 introduced regressions [moby/moby#35320](https://github.com/moby/moby/pull/35320)

- ContainerWait on remove: don't stuck on rm fail [moby/moby#34999](https://github.com/moby/moby/pull/34999)
- oci: obey CL\_UNPRIVILEGED for user namespaced daemon [moby/moby#35205](https://github.com/moby/moby/pull/35205)
- Don't abort when setting may\_detach\_mounts [moby/moby#35172](https://github.com/moby/moby/pull/35172)

* Fix panic on get container pid when live restore containers [moby/moby#35157](https://github.com/moby/moby/pull/35157)
* Mask `/proc/scsi` path for containers to prevent removal of devices (CVE-2017-16539) [moby/moby#35399](https://github.com/moby/moby/pull/35399)

- Update to <github.com/vbatts/tar-split@v0.10.2> (CVE-2017-14992) [moby/moby#35424](https://github.com/moby/moby/pull/35424)

### [Swarm Mode](#swarm-mode)

* Modifying integration test due to new ipam options in swarmkit [moby/moby#35103](https://github.com/moby/moby/pull/35103)

- Fix deadlock on getting swarm info [moby/moby#35388](https://github.com/moby/moby/pull/35388)

* Expand the scope of the `Err` field in `TaskStatus` to also cover non-terminal errors that block the task from progressing [docker/swarmkit#2287](https://github.com/docker/swarmkit/pull/2287)

### [Packaging](#packaging)

* Build packages for Debian 10 (Buster) [docker/docker-ce-packaging#50](https://github.com/docker/docker-ce-packaging/pull/50)
* Build packages for Ubuntu 17.10 (Artful) [docker/docker-ce-packaging#55](https://github.com/docker/docker-ce-packaging/pull/55)

----
url: https://docs.docker.com/reference/cli/docker/model/context/ls/
----

# docker model context ls

***

| Description                                                               | List Model Runner contexts  |
| ------------------------------------------------------------------------- | --------------------------- |
| Usage                                                                     | `docker model context ls`   |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker model context list` |

## [Description](#description)

List Model Runner contexts

----
url: https://docs.docker.com/reference/samples/agentic-ai/
----

# Agentic AI samples

| Name                                                                                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Agent-to-Agent](https://github.com/docker/compose-for-agents/tree/main/a2a)                                                          | This app is a modular AI agent runtime built on Google's Agent Development Kit (ADK) and the A2A (Agent-to-Agent) protocol. It wraps a large language model (LLM)-based agent in an HTTP API and uses structured execution flows with streaming responses, memory, and tools. It is designed to make agents callable as network services and composable with other agents.                                                                                                                                |
| [ADK Multi-Agent Fact Checker](https://github.com/docker/compose-for-agents/tree/main/adk)                                            | This project demonstrates a collaborative multi-agent system built with the Agent Development Kit (ADK), where a top-level Auditor agent coordinates the workflow to verify facts. The Critic agent gathers evidence via live internet searches using DuckDuckGo through the Model Context Protocol (MCP), while the Reviser agent analyzes and refines the conclusion using internal reasoning alone. The system showcases how agents with distinct roles and tools can collaborate under orchestration. |
| [DevDuck agents](https://github.com/docker/compose-for-agents/tree/main/adk-cerebras)                                                 | A multi-agent system for Go programming assistance built with Google Agent Development Kit (ADK). This project features a coordinating agent (DevDuck) that manages two specialized sub-agents (Bob and Cerebras) for different programming tasks.                                                                                                                                                                                                                                                        |
| [Agno](https://github.com/docker/compose-for-agents/tree/main/agno)                                                                   | This app is a multi-agent orchestration system powered by LLMs (like Qwen and OpenAI) and connected to tools via a Model Control Protocol (MCP) gateway. Its purpose is to retrieve, summarize, and document GitHub issues—automatically creating Notion pages from the summaries. It also supports file content summarization from GitHub.                                                                                                                                                               |
| [CrewAI](https://github.com/docker/compose-for-agents/tree/main/crew-ai)                                                              | This project showcases an autonomous, multi-agent virtual marketing team built with CrewAI. It automates the creation of a high-quality, end-to-end marketing strategy — from research to copywriting — using task delegation, web search, and creative synthesis.                                                                                                                                                                                                                                        |
| [SQL Agent with LangGraph](https://github.com/docker/compose-for-agents/tree/main/langgraph)                                          | This project demonstrates a zero-config AI agent that uses LangGraph to answer natural language questions by querying a SQL database — all orchestrated with Docker Compose.                                                                                                                                                                                                                                                                                                                              |
| [Langchaingo Brave Search Example - Model Context Protocol (MCP)](https://github.com/docker/compose-for-agents/tree/main/langchaingo) | This example demonstrates how to create a Go Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses the official Go SDK for Model Context Protocol servers and clients, to set up the MCP client.                                                         |
| [Spring AI Brave Search Example - Model Context Protocol (MCP)](https://github.com/docker/compose-for-agents/tree/main/spring-ai)     | This example demonstrates how to create a Spring AI Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses Spring Boot autoconfiguration to set up the MCP client through configuration files.                                                            |
| [MCP UI with Vercel AI SDK](https://github.com/docker/compose-for-agents/tree/main/vercel)                                            | Start an MCP UI application that uses the Vercel AI SDK to provide a chat interface for local models, provided by the Docker Model Runner, with access to MCPs from the Docker MCP Catalog.                                                                                                                                                                                                                                                                                                               |

----
url: https://docs.docker.com/ai/compose/models-and-compose/
----

# Define AI Models in Docker Compose applications

***

Table of contents

***

Requires: Docker Compose [2.38.0](https://github.com/docker/compose/releases/tag/v2.38.0) and later

Compose lets you define AI models as core components of your application, so you can declare model dependencies alongside services and run the application on any platform that supports the Compose Specification.

## [Prerequisites](#prerequisites)

* Docker Compose v2.38 or later
* A platform that supports Compose models such as [Docker Model Runner (DMR)](https://docs.docker.com/ai/model-runner/#requirements).

## [What are Compose models?](#what-are-compose-models)

Compose `models` are a standardized way to define AI model dependencies in your application. By using the [`models` top-level element](https://docs.docker.com/reference/compose-file/models/) in your Compose file, you can:

* Declare which AI models your application needs
* Specify model configurations and requirements
* Make your application portable across different platforms
* Let the platform handle model provisioning and lifecycle management

## [Basic model definition](#basic-model-definition)

To define models in your Compose application, use the `models` top-level element:

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
```

This example defines:

* A service called `chat-app` that uses a model named `llm`
* A model definition for `llm` that references the `ai/smollm2` model image

## [Model configuration options](#model-configuration-options)

Models support various configuration options:

```yaml
models:
  llm:
    model: ai/smollm2
    context_size: 1024
    runtime_flags:
      - "--a-flag"
      - "--another-flag=42"
```

Common configuration options include:

* `model` (required): The OCI artifact identifier for the model. This is what Compose pulls and runs via the model runner.

* `context_size`: Defines the maximum token context size for the model.

  > Note
  >
  > Each model has its own maximum context size. When increasing the context length, consider your hardware constraints. In general, try to keep context size as small as feasible for your specific needs.

* `runtime_flags`: A list of raw command-line flags passed to the inference engine when the model is started. See [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) for commonly used parameters and examples.

* Platform-specific options may also be available via extension attributes `x-*`

> Tip
>
> See more example in the [Common runtime configurations](#common-runtime-configurations) section.

## [Service model binding](#service-model-binding)

Services can reference models in two ways: short syntax and long syntax.

### [Short syntax](#short-syntax)

The short syntax is the simplest way to bind a model to a service:

```yaml
services:
  app:
    image: my-app
    models:
      - llm
      - embedding-model

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

With short syntax, the platform automatically generates environment variables based on the model name:

* `LLM_URL` - URL to access the LLM model
* `LLM_MODEL` - Model identifier for the LLM model
* `EMBEDDING_MODEL_URL` - URL to access the embedding-model
* `EMBEDDING_MODEL_MODEL` - Model identifier for the embedding-model

### [Long syntax](#long-syntax)

The long syntax allows you to customize environment variable names:

```yaml
services:
  app:
    image: my-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME
      embedding-model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_NAME

models:
  llm:
    model: ai/smollm2
  embedding-model:
    model: ai/all-minilm
```

With this configuration, your service receives:

* `AI_MODEL_URL` and `AI_MODEL_NAME` for the LLM model
* `EMBEDDING_URL` and `EMBEDDING_NAME` for the embedding model

## [Platform portability](#platform-portability)

One of the key benefits of using Compose models is portability across different platforms that support the Compose specification.

### [Docker Model Runner](#docker-model-runner)

When [Docker Model Runner is enabled](https://docs.docker.com/ai/model-runner/):

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      llm:
        endpoint_var: AI_MODEL_URL
        model_var: AI_MODEL_NAME

models:
  llm:
    model: ai/smollm2
    context_size: 4096
    runtime_flags:
      - "--no-prefill-assistant"
```

Docker Model Runner will:

* Pull and run the specified model locally
* Provide endpoint URLs for accessing the model
* Inject environment variables into the service

### [Cloud providers](#cloud-providers)

The Compose models specification is portable. Platforms that implement the Compose specification can support the `models` top-level element, allowing the same Compose file to run on different infrastructure. Cloud-specific behavior can be configured using extension attributes (`x-*`):

```yaml
services:
  chat-app:
    image: my-chat-app
    models:
      - llm

models:
  llm:
    model: ai/smollm2
    # Cloud-specific configurations
    x-cloud-options:
      - "cloud.instance-type=gpu-small"
      - "cloud.region=us-west-2"
```

How a platform handles model definitions depends on its implementation. A platform might:

* Use managed AI services instead of running models locally
* Apply platform-specific optimizations and scaling
* Provide additional monitoring and logging capabilities
* Handle model versioning and updates automatically

## [Common runtime configurations](#common-runtime-configurations)

Below are some example configurations for various use cases.

### [Development](#development)

```yaml
services:
  app:
    image: app
    models:
      dev_model:
        endpoint_var: DEV_URL
        model_var: DEV_MODEL

models:
  dev_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--verbose"                       # Set verbosity level to infinity
      - "--verbose-prompt"                # Print a verbose prompt before generation
      - "--log-prefix"                    # Enable prefix in log messages
      - "--log-timestamps"                # Enable timestamps in log messages
      - "--log-colors"                    # Enable colored logging
```

### [Conservative with disabled reasoning](#conservative-with-disabled-reasoning)

```yaml
services:
  app:
    image: app
    models:
      conservative_model:
        endpoint_var: CONSERVATIVE_URL
        model_var: CONSERVATIVE_MODEL

models:
  conservative_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "0.1"
      - "--top-k"               # Top-k sampling
      - "1"
      - "--reasoning-budget"    # Disable reasoning
      - "0"
```

### [Creative with high randomness](#creative-with-high-randomness)

```yaml
services:
  app:
    image: app
    models:
      creative_model:
        endpoint_var: CREATIVE_URL
        model_var: CREATIVE_MODEL

models:
  creative_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "1"
      - "--top-p"               # Top-p sampling
      - "0.9"
```

### [Highly deterministic](#highly-deterministic)

```yaml
services:
  app:
    image: app
    models:
      deterministic_model:
        endpoint_var: DET_URL
        model_var: DET_MODEL

models:
  deterministic_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "0"
      - "--top-k"               # Top-k sampling
      - "1"
```

### [Concurrent processing](#concurrent-processing)

```yaml
services:
  app:
    image: app
    models:
      concurrent_model:
        endpoint_var: CONCURRENT_URL
        model_var: CONCURRENT_MODEL

models:
  concurrent_model:
    model: ai/model
    context_size: 2048
    runtime_flags:
      - "--threads"             # Number of threads to use during generation
      - "8"
      - "--mlock"               # Lock memory to prevent swapping
```

### [Rich vocabulary model](#rich-vocabulary-model)

```yaml
services:
  app:
    image: app
    models:
      rich_vocab_model:
        endpoint_var: RICH_VOCAB_URL
        model_var: RICH_VOCAB_MODEL

models:
  rich_vocab_model:
    model: ai/model
    context_size: 4096
    runtime_flags:
      - "--temp"                # Temperature
      - "0.1"
      - "--top-p"               # Top-p sampling
      - "0.9"
```

### [Embeddings](#embeddings)

When using embedding models with the `/v1/embeddings` endpoint, you must include the `--embeddings` runtime flag for the model to be properly configured.

```yaml
services:
  app:
    image: app
    models:
      embedding_model:
        endpoint_var: EMBEDDING_URL
        model_var: EMBEDDING_MODEL

models:
  embedding_model:
    model: ai/all-minilm
    context_size: 2048
    runtime_flags:
      - "--embeddings"          # Required for embedding models
```

## [Reference](#reference)

* [`models` top-level element](https://docs.docker.com/reference/compose-file/models/)
* [`models` attribute](https://docs.docker.com/reference/compose-file/services/#models)
* [Docker Model Runner documentation](https://docs.docker.com/ai/model-runner/)
* [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Context size and runtime parameters
* [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - llama.cpp and vLLM details
* [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - OpenAI and Ollama-compatible APIs

----
url: https://docs.docker.com/guides/testcontainers-cloud/demo-ci/
----

# Configuring Testcontainers Cloud in the CI Pipeline

***

***

This demo shows how Testcontainers Cloud can be seamlessly integrated into a Continuous Integration (CI) pipeline using GitHub Workflows, providing a powerful solution for running containerized integration tests without overloading local or CI runner resources. By leveraging GitHub Actions, developers can automate the process of spinning up and managing containers for testing in the cloud, ensuring faster and more reliable test execution. With just a few configuration steps, including setting up Testcontainers Cloud authentication and adding it to your workflow, you can offload container orchestration to the cloud. This approach improves the scalability of your pipeline, ensures consistency across tests, and simplifies resource management, making it an ideal solution for modern, containerized development workflows.

* Understand how to set up a GitHub Actions workflow to automate the build and testing of a project.
* Learn how to configure Testcontainers Cloud within GitHub Actions to offload containerized testing to the cloud, improving efficiency and resource management.
* Explore how Testcontainers Cloud integrates with GitHub workflows to run integration tests that require containerized services, such as databases and message brokers.

[Common challenges and questions »](https://docs.docker.com/guides/testcontainers-cloud/common-questions/)

----
url: https://docs.docker.com/reference/cli/docker/swarm/leave/
----

# docker swarm leave

***

| Description | Leave the swarm                |
| ----------- | ------------------------------ |
| Usage       | `docker swarm leave [OPTIONS]` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

When you run this command on a worker, that worker leaves the swarm.

You can use the `--force` option on a manager to remove it from the swarm. However, this does not reconfigure the swarm to ensure that there are enough managers to maintain a quorum in the swarm. The safe way to remove a manager from a swarm is to demote it to a worker and then direct it to leave the quorum without using `--force`. Only use `--force` in situations where the swarm will no longer be used after the manager leaves, such as in a single-node swarm.

## [Options](#options)

| Option        | Default | Description                                           |
| ------------- | ------- | ----------------------------------------------------- |
| `-f, --force` |         | Force this node to leave the swarm, ignoring warnings |

## [Examples](#examples)

Consider the following swarm, as seen from the manager:

```console
$ docker node ls

ID                           HOSTNAME  STATUS  AVAILABILITY  MANAGER STATUS
7ln70fl22uw2dvjn2ft53m3q5    worker2   Ready   Active
dkp8vy1dq1kxleu9g4u78tlag    worker1   Ready   Active
dvfxp4zseq4s0rih1selh0d20 *  manager1  Ready   Active        Leader
```

To remove `worker2`, issue the following command from `worker2` itself:

```console
$ docker swarm leave

Node left the default swarm.
```

The node will still appear in the node list, and marked as `down`. It no longer affects swarm operation, but a long list of `down` nodes can clutter the node list. To remove an inactive node from the list, use the [`node rm`](/reference/cli/docker/node/rm/) command.

----
url: https://docs.docker.com/scout/integrations/ci/circle-ci/
----

# Integrate Docker Scout with Circle CI

***

***

The following examples runs when triggered in CircleCI. When triggered, it checks out the "docker/scout-demo-service:latest" image and tag and then uses Docker Scout to create a CVE report.

Add the following to a *.circleci/config.yml* file.

First, set up the rest of the workflow. Add the following to the YAML file:

```yaml
version: 2.1

jobs:
  build:
    docker:
      - image: cimg/base:stable
    environment:
      IMAGE_TAG: docker/scout-demo-service:latest
```

This defines the container image the workflow uses and an environment variable for the image.

Add the following to the YAML file to define the steps for the workflow:

```yaml
steps:
  # Checkout the repository files
  - checkout
  
  # Set up a separate Docker environment to run `docker` commands in
  - setup_remote_docker:
      version: 20.10.24

  # Install Docker Scout and login to Docker Hub
  - run:
      name: Install Docker Scout
      command: |
        env
        curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s -- -b /home/circleci/bin
        echo $DOCKER_HUB_PAT | docker login -u $DOCKER_HUB_USER --password-stdin

  # Build the Docker image
  - run:
      name: Build Docker image
      command: docker build -t $IMAGE_TAG .
  
  # Run Docker Scout          
  - run:
      name: Scan image for CVEs
      command: |
        docker scout cves $IMAGE_TAG --exit-code --only-severity critical,high
```

This checks out the repository files and then sets up a separate Docker environment to run commands in.

It installs Docker Scout, logs into Docker Hub, builds the Docker image, and then runs Docker Scout to generate a CVE report. It only shows critical or high-severity vulnerabilities.

Finally, add a name for the workflow and the workflow's jobs:

```yaml
workflows:
  build-docker-image:
    jobs:
      - build
```

----
url: https://docs.docker.com/engine/storage/drivers/select-storage-driver/
----

# Select a storage driver

***

Table of contents

***

Ideally, very little data is written to a container's writable layer, and you use Docker volumes to write data. However, some workloads require you to be able to write to the container's writable layer. This is where storage drivers come in.

> Note
>
> Docker Engine 29.0 and later uses the [containerd image store](https://docs.docker.com/engine/storage/containerd/) by default for fresh installations. If you upgraded from an earlier version, your daemon continues using the classic storage drivers described on this page. You can migrate to the containerd image store following the instructions in the [containerd image store](https://docs.docker.com/engine/storage/containerd/) documentation.

Docker supports several storage drivers, using a pluggable architecture. The storage driver controls how images and containers are stored and managed on your Docker host. After you have read the [storage driver overview](https://docs.docker.com/engine/storage/drivers/), the next step is to choose the best storage driver for your workloads. Use the storage driver with the best overall performance and stability in the most usual scenarios.

> Note
>
> This page discusses storage drivers for Docker Engine on Linux. If you're running the Docker daemon with Windows as the host OS, the only supported storage driver is windowsfilter. For more information, see [windowsfilter](https://docs.docker.com/engine/storage/drivers/windowsfilter-driver/).

The Docker Engine provides the following storage backends on Linux:

| Backend                     | Description                                                                                                                                                                                                                                                             |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `containerd` (snapshotters) | The default for Docker Engine 29.0 and later. Uses containerd snapshotters for image storage. Supports multi-platform images and attestations. See [containerd image store](https://docs.docker.com/engine/storage/containerd/) for details.                            |
| `overlay2`                  | Classic storage driver. Most widely compatible across all currently supported Linux distributions, and requires no extra configuration.                                                                                                                                 |
| `fuse-overlayfs`            | Preferred only for running Rootless Docker on hosts that don't support rootless `overlay2`. Not needed since Linux kernel 5.11, as `overlay2` works in rootless mode. See [rootless mode documentation](https://docs.docker.com/engine/security/rootless/) for details. |
| `btrfs` and `zfs`           | Allow for advanced options, such as creating snapshots, but require more maintenance and setup. Each relies on the backing filesystem being configured correctly.                                                                                                       |
| `vfs`                       | Intended for testing purposes, and for situations where no copy-on-write filesystem can be used. Performance is poor, and not generally recommended for production use.                                                                                                 |

The Docker Engine has a prioritized list of which storage driver to use if no storage driver is explicitly configured, assuming that the storage driver meets the prerequisites, and automatically selects a compatible storage driver. You can see the order in the [source code for Docker Engine 29.5.3](https://github.com/moby/moby/blob/docker-v29.5.3/daemon/graphdriver/driver_linux.go).

Some storage drivers require you to use a specific format for the backing filesystem. If you have external requirements to use a specific backing filesystem, this may limit your choices. See [Supported backing filesystems](#supported-backing-filesystems).

After you have narrowed down which storage drivers you can choose from, your choice is determined by the characteristics of your workload and the level of stability you need. See [Other considerations](#other-considerations) for help in making the final decision.

## [Supported storage drivers per Linux distribution](#supported-storage-drivers-per-linux-distribution)

> Note
>
> Modifying the storage driver by editing the daemon configuration file isn't supported on Docker Desktop. Docker Desktop uses the [containerd image store](https://docs.docker.com/desktop/features/containerd/) by default (version 4.34 and later for clean installs). The following table is also not applicable for the Docker Engine in rootless mode. For the drivers available in rootless mode, see the [Rootless mode documentation](https://docs.docker.com/engine/security/rootless/).

This section applies to classic storage drivers only. If you're using the containerd image store (the default for Docker Engine 29.0+), see the [containerd image store documentation](https://docs.docker.com/engine/storage/containerd/) instead.

Your operating system and kernel may not support every classic storage driver. For example, `btrfs` is only supported if your system uses `btrfs` as storage. In general, the following configurations work on recent versions of the Linux distribution:

| Linux distribution | Default classic driver | Alternative drivers |
| ------------------ | ---------------------- | ------------------- |
| Ubuntu             | `overlay2`             | `zfs`, `vfs`        |
| Debian             | `overlay2`             | `vfs`               |
| CentOS             | `overlay2`             | `zfs`, `vfs`        |
| Fedora             | `overlay2`             | `zfs`, `vfs`        |
| SLES 15            | `overlay2`             | `vfs`               |
| RHEL               | `overlay2`             | `vfs`               |

For systems using classic storage drivers, `overlay2` provides broad compatibility across Linux distributions. Use Docker volumes for write-heavy workloads instead of relying on writing data to the container's writable layer.

The `vfs` storage driver is usually not the best choice, and primarily intended for debugging purposes in situations where no other storage-driver is supported. Before using the `vfs` storage driver, be sure to read about [its performance and storage characteristics and limitations](https://docs.docker.com/engine/storage/drivers/vfs-driver/).

The recommendations in the table above are known to work for a large number of users. If you use a recommended configuration and find a reproducible issue, it's likely to be fixed very quickly. If the driver that you want to use is not recommended according to this table, you can run it at your own risk. You can and should still report any issues you run into. However, such issues have a lower priority than issues encountered when using a recommended configuration.

Depending on your Linux distribution, other storage-drivers, such as `btrfs` may be available. These storage drivers can have advantages for specific use-cases, but may require additional set-up or maintenance, which make them not recommended for common scenarios. Refer to the documentation for those storage drivers for details.

## [Supported backing filesystems](#supported-backing-filesystems)

With regard to Docker, the backing filesystem is the filesystem where `/var/lib/docker/` is located. Some storage drivers only work with specific backing filesystems.

| Storage driver   | Supported backing filesystems                   |
| ---------------- | ----------------------------------------------- |
| `overlay2`       | `xfs` with ftype=1, `ext4`, `btrfs`, (and more) |
| `fuse-overlayfs` | any filesystem                                  |
| `btrfs`          | `btrfs`                                         |
| `zfs`            | `zfs`                                           |
| `vfs`            | any filesystem                                  |

> Note
>
> Most filesystems should work if they have the required features. Consult [OverlayFS](https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html) for more information.

## [Other considerations](#other-considerations)

### [Suitability for your workload](#suitability-for-your-workload)

Among other things, each storage driver has its own performance characteristics that make it more or less suitable for different workloads. Consider the following generalizations:

* `overlay2` operates at the file level rather than the block level. This uses memory more efficiently, but the container's writable layer may grow quite large in write-heavy workloads.
* Block-level storage drivers such as `btrfs`, and `zfs` perform better for write-heavy workloads (though not as well as Docker volumes).
* `btrfs` and `zfs` require a lot of memory.
* `zfs` is a good choice for high-density workloads such as PaaS.

More information about performance, suitability, and best practices is available in the documentation for each storage driver.

### [Shared storage systems and the storage driver](#shared-storage-systems-and-the-storage-driver)

If you use SAN, NAS, hardware RAID, or other shared storage systems, those systems may provide high availability, increased performance, thin provisioning, deduplication, and compression. In many cases, Docker can work on top of these storage systems, but Docker doesn't closely integrate with them.

Each Docker storage driver is based on a Linux filesystem or volume manager. Be sure to follow existing best practices for operating your storage driver (filesystem or volume manager) on top of your shared storage system. For example, if using the ZFS storage driver on top of a shared storage system, be sure to follow best practices for operating ZFS filesystems on top of that specific shared storage system.

### [Stability](#stability)

For some users, stability is more important than performance. Though Docker considers all of the storage drivers mentioned here to be stable, some are newer and are still under active development. In general, `overlay2` provides the highest stability.

### [Test with your own workloads](#test-with-your-own-workloads)

You can test Docker's performance when running your own workloads on different storage drivers. Make sure to use equivalent hardware and workloads to match production conditions, so you can see which storage driver offers the best overall performance.

## [Check your current storage driver](#check-your-current-storage-driver)

The detailed documentation for each individual storage driver details all of the set-up steps to use a given storage driver.

To see what storage driver Docker is currently using, use `docker info` and look for the `Storage Driver` line:

```console
$ docker info

Containers: 0
Images: 0
Storage Driver: overlay2
 Backing Filesystem: xfs
<...>
```

To change the storage driver, see the specific instructions for the new storage driver. Some drivers require additional configuration, including configuration to physical or logical disks on the Docker host.

> Important
>
> When you change the storage driver, any existing images and containers become inaccessible. This is because their layers can't be used by the new storage driver. If you revert your changes, you can access the old images and containers again, but any that you pulled or created using the new driver are then inaccessible.

## [Related information](#related-information)

* [Storage drivers](https://docs.docker.com/engine/storage/drivers/)
* [`overlay2` storage driver](https://docs.docker.com/engine/storage/drivers/overlayfs-driver/)
* [`btrfs` storage driver](https://docs.docker.com/engine/storage/drivers/btrfs-driver/)
* [`zfs` storage driver](https://docs.docker.com/engine/storage/drivers/zfs-driver/)
* [`windowsfilter` storage driver](https://docs.docker.com/engine/storage/drivers/windowsfilter-driver/)

----
url: https://docs.docker.com/docker-hub/repos/manage/trusted-content/insights-analytics/
----

# Insights and analytics

***

Table of contents

***

Insights and analytics provides usage analytics for [Docker Verified Publisher (DVP)](https://www.docker.com/partners/programs/) and [Docker-Sponsored Open Source (DSOS)](https://www.docker.com/community/open-source/application/#) images on Docker Hub. This includes self-serve access to image and extension usage metrics for a desired time span. You can see the number of image pulls by tag or by digest, geolocation, cloud provider, client, and more.

> Note
>
> The Legacy DVP program applies to existing customers who have not yet renewed to DVP Core. The DVP Legacy program is deprecated and will be retired. Contact your Docker sales representative or [Docker](https://www.docker.com/partners/programs/) for more information.

All members of an organization have access to the analytics data. Members can access analytics data in the [Docker Hub](https://hub.docker.com/) web interface.

## [Available reports](#available-reports)

The following reports may be available for download as CSV files:

* [Summary](#summary-report)
* [Trends](#trends-report)
* [Technographic](#technographic-report)
* [Technographic companies](#technographic-companies-report)
* [Tracked companies](#tracked-companies-report)

The reports available for download may vary based on your organization's subscription. Contact your Docker sales representative or [Docker](https://www.docker.com/partners/programs/) for more information.

## [Configure DVP analytics settings](#configure-dvp-analytics-settings)

Organization owners and editors can configure DVP analytics settings through the Admin Console to control tracked companies and benchmark report allocations for your verified publisher namespaces.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.

2. Select **Admin Console** > **Verified Publisher**.

3. Configure the settings:

   * **Tracked companies**: Set the number of companies to track for reporting purposes. This setting determines how many company domains appear in your [Tracked companies report](#tracked-companies-report). You can only set this number up to the maximum included in your DVP subscription.
   * **Benchmark report allocations**: If your organization has benchmark reports enabled, enter the number of companies to include in the benchmark report for each namespace listed.

4. Select **Save** to apply your changes.

### [Summary report](#summary-report)

The summary report provides high-level usage metrics aggregated across all your Docker Hub content, organized by namespace and repository. This report gives you a comprehensive overview of your image portfolio performance, helping you understand which repositories, tags, and specific image versions are most popular with your users.

You can use this report to answer questions like:

* Which of my repositories are getting the most usage?
* How do different image tags compare in terms of adoption?
* What's the ratio of actual downloads versus version checks across my portfolio?
* Which specific image digests are being pulled most frequently?
* How has overall usage changed over time for my entire image collection?

To access the report:

1. Sign in to [Docker Hub](https://hub.docker.com/).

2. Select **My Hub** in the top navigation.

3. Select your organization in the left navigation.

4. Select **Analytics** > **Overview** in the left navigation.

5. Download the report by doing one of the following:

   * Select **Download Weekly Summary**.
   * Select the **Download Monthly Summary**.
   * Expand the **Summary reports for the year** drop-down and then select **Download report** for the desired week or month.

The summary report is a CSV file that contains the following data points:

| Field              | Description                                                                                                                                                           |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DATE_GRANULARITY` | Weekly or monthly granularity of the data. Indicates whether the data is aggregated by week or month.                                                                 |
| `DATE_REFERENCE`   | The start date of the week or month in YYYY-MM-DD format (e.g., `2025-09-29` for the week starting September 29, 2025).                                               |
| `PUBLISHER_NAME`   | The name of the Docker organization that owns the repository (e.g., `demonstrationorg`).                                                                              |
| `LEVEL`            | The aggregation level of the data - either `repository` (summary for entire repository), `tag` (summary for specific tag), or `digest` (summary for specific digest). |
| `REFERENCE`        | The specific reference being summarized - the repository name, tag name, or digest hash depending on the level.                                                       |
| `DATA_DOWNLOADS`   | The number of actual image downloads.                                                                                                                                 |
| `VERSION_CHECKS`   | The number of version checks performed (HEAD requests to check for updates without downloading the full image).                                                       |
| `EVENT_COUNT`      | The total number of events, calculated as the sum of data downloads and version checks.                                                                               |

### [Trends report](#trends-report)

The trends report helps you understand how adoption of your container images evolves over time. It provides visibility into pull activity across repositories and tags, enabling you to identify adoption patterns, version migration trends, and usage environments (e.g., local development, CI/CD, production).

You can use this report to answer questions like:

* Which versions are gaining or losing traction?
* Is a new release being adopted?
* How does usage vary across cloud providers?

To access the report:

1. Sign in to [Docker Hub](https://hub.docker.com/).
2. Select **My Hub** in the top navigation.
3. Select your organization in the left navigation.
4. Select **Analytics** > **Trends** in the left navigation.
5. Select **DATA BY WEEK** or **DATA BY MONTH** to choose the data granularity.
6. Select **Download report** for the desired week or month.

The trends report is a CSV file that contains the following data points:

| Field                          | Description                                                                                                             |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| `DATE_GRANULARITY`             | Weekly or monthly granularity of the data.                                                                              |
| `DATE_REFERENCE`               | The start date of the week or month.                                                                                    |
| `PUBLISHER_NAME`               | The name of the organization that owns the repository.                                                                  |
| `IMAGE_REPOSITORY`             | The full name of the image repository (e.g., `demonstrationorg/scout-demo`).                                            |
| `NAMESPACE`                    | The Docker organization or namespace that owns the repository.                                                          |
| `IP_COUNTRY`                   | The country code (ISO 3166-1 alpha-2) where the pull request originated from (e.g., `US`, `CA`).                        |
| `CLOUD_SERVICE_PROVIDER`       | The cloud service provider used for the pull request (e.g., `gcp`, `aws`, `azure`) or `no csp` for non-cloud providers. |
| `USER_AGENT`                   | The client application or tool used to pull the image (e.g., `docker`, `docker-scout`, `node-fetch`, `regclient`).      |
| `TAG`                          | The specific image tag that was pulled, or `\\N` if no specific tag was used.                                           |
| `DATA_DOWNLOADS`               | The number of data downloads for the specified criteria.                                                                |
| `VERSION_CHECKS`               | The number of version checks (HEAD requests) performed without downloading the full image.                              |
| `PULLS`                        | The total number of pull requests (data downloads + version checks).                                                    |
| `UNIQUE_AUTHENTICATED_USERS`   | The number of unique authenticated users who performed pulls.                                                           |
| `UNIQUE_UNAUTHENTICATED_USERS` | The number of unique unauthenticated users who performed pulls.                                                         |

### [Technographic report](#technographic-report)

The technographic report provides insights into how your Docker Verified Publisher (DVP) images are used alongside other container images in real-world technology stacks. This report helps you understand the technical ecosystem where your images operate and identify co-usage patterns with other images.

You can use this report to answer questions like:

* Which other images are commonly used together with your images?
* What percentage of your user base also uses specific complementary technologies?
* How many companies in your ecosystem use both your image and other popular images?
* What technology stacks are most popular among your users?

To access the report:

1. Sign in to [Docker Hub](https://hub.docker.com/).
2. Select **My Hub** in the top navigation.
3. Select your organization in the left navigation.
4. Select **Analytics** > **Technographic** in the left navigation.
5. Select **DATA BY WEEK** or **DATA BY MONTH** to choose the data granularity.
6. Select **Download report** for the desired week or month.

The technographic report is a CSV file that contains the following data points:

| Field              | Description                                                                                                 |
| ------------------ | ----------------------------------------------------------------------------------------------------------- |
| `DATE_GRANULARITY` | Weekly or monthly granularity of the data.                                                                  |
| `DATE_REFERENCE`   | The start date of the week or month in YYYY-MM-DD format.                                                   |
| `PUBLISHER_ID`     | The unique identifier for the publisher organization.                                                       |
| `PUBLISHER_NAME`   | The name of the organization that owns the DVP repository.                                                  |
| `DVPP_IMAGE`       | Your Docker Verified Publisher image repository name.                                                       |
| `PAIRED_IMAGE`     | The other image repository that is commonly used together with your DVP image.                              |
| `USERS`            | The number of unique users who pulled both your DVP image and the paired image within the time period.      |
| `TOTAL_PULLERS`    | The total number of unique users who pulled your DVP image during the time period.                          |
| `PCT_USERS`        | The percentage of your image's users who also use the paired image (users/total\_pullers).                  |
| `DOMAINS`          | The number of unique company domains that pulled both your DVP image and the paired image.                  |
| `TOTAL_DOMAINS`    | The total number of unique company domains that pulled your DVP image.                                      |
| `PCT_DOMAINS`      | The percentage of company domains using your image that also use the paired image (domains/total\_domains). |

> Note
>
> To protect user privacy and ensure statistical significance, the technographic report only includes image pairings that have at least 10 unique users. Personal, disposable, and university email domains are excluded from the company domain analysis.

### [Technographic companies report](#technographic-companies-report)

The technographic companies report provides a detailed view of which specific companies (identified by their domains) are using your Docker Verified Publisher (DVP) images together with other container images. This report gives you visibility into the actual organizations adopting your technology stack combinations, enabling targeted business development and partnership opportunities.

You can use this report to answer questions like:

* Which companies are using my image alongside specific complementary technologies?
* What technology stacks are adopted by enterprise customers in my target market?
* Which organizations might be good candidates for partnership discussions?
* How can I identify potential customers who are already using related technologies?

To access the report:

1. Sign in to [Docker Hub](https://hub.docker.com/).
2. Select **My Hub** in the top navigation.
3. Select your organization in the left navigation.
4. Select **Analytics** > **Technographic** in the left navigation.
5. Select **DATA BY WEEK** or **DATA BY MONTH** to choose the data granularity.
6. Select **Download report** for the desired week or month.

The technographic companies report is a CSV file that contains the following data points:

| Field              | Description                                                                                    |
| ------------------ | ---------------------------------------------------------------------------------------------- |
| `DATE_GRANULARITY` | Weekly or monthly granularity of the data.                                                     |
| `DATE_REFERENCE`   | The start date of the week or month in YYYY-MM-DD format.                                      |
| `PUBLISHER_NAME`   | The name of the organization that owns the DVP repository.                                     |
| `DOMAIN`           | The company domain that pulled both your DVP image and the paired image (e.g., `example.com`). |
| `DVPP_IMAGE`       | Your Docker Verified Publisher image repository name.                                          |
| `PAIRED_IMAGE`     | The other image repository that was used together with your DVP image by this company.         |

Each row represents a unique combination of a company domain, your DVP image, and another image that were used together during the specified time period.

> Note
>
> To protect privacy and ensure data quality, this report excludes personal email domains, disposable email services, and university domains. Only business and organizational domains are included in the analysis.

### [Tracked companies report](#tracked-companies-report)

The tracked companies report provides detailed insights into how specific companies are using your Docker Verified Publisher (DVP) images. This report helps you understand usage patterns, deployment environments, and adoption trends across your customer base and potential prospects.

You can use this report to answer questions like:

* How are specific companies using my images across different environments?
* What deployment patterns do I see across local development, CI/CD, and production?
* Which companies are heavy users of my images?
* How does usage vary by geography and cloud providers for tracked companies?

To access the report:

1. Sign in to [Docker Hub](https://hub.docker.com/).
2. Select **My Hub** in the top navigation.
3. Select your organization in the left navigation.
4. Select **Analytics** > **Tracked Companies** in the left navigation.
5. Select **DATA BY WEEK** or **DATA BY MONTH** to choose the data granularity.
6. Select **Download report** for the desired week or month.

The tracked companies report is a CSV file that contains the following data points:

| Field                        | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DATE_GRANULARITY`           | Weekly or monthly granularity of the data.                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `DATE_REFERENCE`             | The start date of the week or month in YYYY-MM-DD format.                                                                                                                                                                                                                                                                                                                                                                                                               |
| `PUBLISHER_NAME`             | The name of the organization that owns the DVP repository.                                                                                                                                                                                                                                                                                                                                                                                                              |
| `DOMAIN`                     | The company domain (e.g., `docker.com`) associated with the image pulls.                                                                                                                                                                                                                                                                                                                                                                                                |
| `IP_COUNTRY`                 | The country code (ISO 3166-1 alpha-2) where the pull request originated from.                                                                                                                                                                                                                                                                                                                                                                                           |
| `CLOUD_SERVICE_PROVIDER`     | The cloud service provider used for the pull request or `no csp` for non-cloud providers.                                                                                                                                                                                                                                                                                                                                                                               |
| `USER_AGENT`                 | The client application or tool used to pull the image.                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `INFERRED_USE_CASE`          | The inferred deployment environment based on user agent and cloud provider analysis. Values include: • `Local Dev`: Local development environment (e.g., Docker Desktop, direct `docker` commands) • `CI/CD`: Continuous integration/deployment pipelines (e.g., containerd, build tools, registry mirroring) • `Prod`: Production environments (e.g., Kubernetes, container orchestration platforms) • `Unknown`: Unable to determine the use case from available data |
| `IMAGE_REPOSITORY`           | The specific DVP image repository that was pulled.                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `DATA_DOWNLOADS`             | The number of actual image layer downloads for this combination.                                                                                                                                                                                                                                                                                                                                                                                                        |
| `VERSION_CHECKS`             | The number of version checks (HEAD requests) performed without downloading the full image.                                                                                                                                                                                                                                                                                                                                                                              |
| `PULLS`                      | The total number of pull requests (data downloads + version checks).                                                                                                                                                                                                                                                                                                                                                                                                    |
| `UNIQUE_AUTHENTICATED_USERS` | The number of unique authenticated users from this domain who performed pulls.                                                                                                                                                                                                                                                                                                                                                                                          |

> Note
>
> Use case inference is determined by analyzing user agent patterns and cloud service provider usage. Local development tools used on cloud infrastructure are reclassified as CI/CD, and CI/CD tools used on cloud infrastructure are reclassified as production to better reflect actual deployment patterns.

> Important
>
> The Legacy DVP program applies to existing customers who have not yet renewed to DVP Core. The DVP Legacy program is deprecated and will be retired. Contact your Docker sales representative or [Docker](https://www.docker.com/partners/programs/) for more information.

## [View the image's analytics data](#view-the-images-analytics-data)

You can find analytics data for your repositories on the **Insights and analytics** dashboard at the following URL: `https://hub.docker.com/orgs/{namespace}/insights/images`. The dashboard contains a visualization of the usage data and a table where you can download the data as CSV files.

To view data in the chart:

* Select the data granularity: weekly or monthly
* Select the time interval: 3, 6, or 12 months
* Select one or more repositories in the list

> Tip
>
> Hovering your cursor over the chart displays a tooltip, showing precise data for points in time.

### [Share analytics data](#share-analytics-data)

You can share the visualization with others using the **Share** icon at the top of the chart. This is a convenient way to share statistics with others in your organization.

Selecting the icon generates a link that's copied to your clipboard. The link preserves the display selections you made. When someone follows the link, the **Insights and analytics** page opens and displays the chart with the same configuration as you had set up when creating the link.

## [Extension analytics data](#extension-analytics-data)

If you have published Docker Extensions in the Extension marketplace, you can also get analytics about your extension usage, available as CSV files. You can download extension CSV reports from the **Insights and analytics** dashboard at the following URL: `https://hub.docker.com/orgs/{namespace}/insights/extensions`. If your Docker namespace contains extensions known in the marketplace, you will see an **Extensions** tab listing CSV files for your extension(s).

## [Exporting analytics data](#exporting-analytics-data)

You can export the analytics data either from the web dashboard, or using the [DVP Data API](https://docs.docker.com/reference/api/dvp/latest/). All members of an organization have access to the analytics data.

The data is available as a downloadable CSV file, in a weekly (Monday through Sunday) or monthly format. Monthly data is available from the first day of the following calendar month. You can import this data into your own systems, or you can analyze it manually as a spreadsheet.

### [Export data](#export-data)

Export usage data for your organization's images using the Docker Hub website by following these steps:

1. Sign in to [Docker Hub](https://hub.docker.com/) and select **My Hub**.

2. Choose your organization and select **Analytics**.

3. Set the time span for which you want to export analytics data.

   The downloadable CSV files for summary and raw data appear on the right-hand side.

### [Export data using the API](#export-data-using-the-api)

The HTTP API endpoints are available at: `https://hub.docker.com/api/publisher/analytics/v1`. Learn how to export data using the API in the [DVP Data API documentation](https://docs.docker.com/reference/api/dvp/latest/).

## [Data points](#data-points)

Export data in either raw or summary format. Each format contains different data points and with different structure.

The following sections describe the available data points for each format. The **Date added** column shows when the field was first introduced.

### [Image pulls raw data](#image-pulls-raw-data)

The raw data format contains the following data points. Each row in the CSV file represents an image pull.

| Data point                    | Description                                                                                                                                         | Date added        |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- |
| Action                        | Request type, see [Action classification rules](#image-pulls-action-classification-rules). One of `pull_by_tag`, `pull_by_digest`, `version_check`. | January 1, 2022   |
| Action day                    | The date part of the timestamp: `YYYY-MM-DD`.                                                                                                       | January 1, 2022   |
| Country                       | Request origin country.                                                                                                                             | January 1, 2022   |
| Digest                        | Image digest.                                                                                                                                       | January 1, 2022   |
| HTTP method                   | HTTP method used in the request, see [registry API documentation](/registry/spec/api/) for details.                                                 | January 1, 2022   |
| Host                          | The cloud service provider used in an event.                                                                                                        | January 1, 2022   |
| Namespace                     | Docker [organization](/admin/organization/setup/orgs/) (image namespace).                                                                           | January 1, 2022   |
| Reference                     | Image digest or tag used in the request.                                                                                                            | January 1, 2022   |
| Repository                    | Docker [repository](/docker-hub/repos/) (image name).                                                                                               | January 1, 2022   |
| Tag (included when available) | Tag name that's only available if the request referred to a tag.                                                                                    | January 1, 2022   |
| Timestamp                     | Date and time of the request: `YYYY-MM-DD 00:00:00`.                                                                                                | January 1, 2022   |
| Type                          | The industry from which the event originates. One of `business`, `isp`, `hosting`, `education`, `null`.                                             | January 1, 2022   |
| User agent tool               | The application a user used to pull an image (for example, `docker` or `containerd`).                                                               | January 1, 2022   |
| User agent version            | The version of the application used to pull an image.                                                                                               | January 1, 2022   |
| Domain                        | Request origin domain, see [Privacy](#privacy).                                                                                                     | October 11, 2022  |
| Owner                         | The name of the organization that owns the repository.                                                                                              | December 19, 2022 |

### [Image pulls summary data](#image-pulls-summary-data)

There are two levels of summary data available:

* Repository-level, a summary of every namespace and repository
* Tag- or digest-level, a summary of every namespace, repository, and reference (tag or digest)

The summary data formats contain the following data points for the selected time span:

| Data point        | Description                                             | Date added        |
| ----------------- | ------------------------------------------------------- | ----------------- |
| Unique IP address | Number of unique IP addresses, see [Privacy](#privacy). | January 1, 2022   |
| Pull by tag       | GET request, by digest or by tag.                       | January 1, 2022   |
| Pull by digest    | GET or HEAD request by digest, or HEAD by digest.       | January 1, 2022   |
| Version check     | HEAD by tag, not followed by a GET                      | January 1, 2022   |
| Owner             | The name of the organization that owns the repository.  | December 19, 2022 |

### [Image pulls action classification rules](#image-pulls-action-classification-rules)

An action represents the multiple request events associated with a `docker pull`. Pulls are grouped by category to make the data more meaningful for understanding user behavior and intent. The categories are:

* Version check
* Pull by tag
* Pull by digest

Automated systems frequently check for new versions of your images. Being able to distinguish between "version checks" in CI versus actual image pulls by a user grants you more insight into your users' behavior.

The following table describes the rules applied for determining intent behind pulls. To provide feedback or ask questions about these rules, [fill out the Google Form](https://forms.gle/nb7beTUQz9wzXy1b6).

| Starting event | Reference | Followed by                                                     | Resulting action | Use case(s)                                                                                                    | Notes                                                                                                                                                                                                                                                                                 |
| -------------- | --------- | --------------------------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HEAD           | tag       | N/A                                                             | Version check    | User already has all layers existing on local machine                                                          | This is similar to the use case of a pull by tag when the user already has all the image layers existing locally, however, it differentiates the user intent and classifies accordingly.                                                                                              |
| GET            | tag       | N/A                                                             | Pull by tag      | User already has all layers existing on local machine and/or the image is single-arch                          |                                                                                                                                                                                                                                                                                       |
| GET            | tag       | Get by different digest                                         | Pull by tag      | Image is multi-arch                                                                                            | Second GET by digest must be different from the first.                                                                                                                                                                                                                                |
| HEAD           | tag       | GET by same digest                                              | Pull by tag      | Image is multi-arch but some or all image layers already exist on the local machine                            | The HEAD by tag sends the most current digest, the following GET must be by that same digest. There may occur an additional GET, if the image is multi-arch (see the next row in this table). If the user doesn't want the most recent digest, then the user performs HEAD by digest. |
| HEAD           | tag       | GET by the same digest, then a second GET by a different digest | Pull by tag      | Image is multi-arch                                                                                            | The HEAD by tag sends the most recent digest, the following GET must be by that same digest. Since the image is multi-arch, there is a second GET by a different digest. If the user doesn't want the most recent digest, then the user performs HEAD by digest.                      |
| HEAD           | tag       | GET by same digest, then a second GET by different digest       | Pull by tag      | Image is multi-arch                                                                                            | The HEAD by tag sends the most current digest, the following GET must be by that same digest. Since the image is multi-arch, there is a second GET by a different digest. If the user doesn't want the most recent digest, then the user performs HEAD by digest.                     |
| GET            | digest    | N/A                                                             | Pull by digest   | User already has all layers existing on local machine and/or the image is single-arch                          |                                                                                                                                                                                                                                                                                       |
| HEAD           | digest    | N/A                                                             | Pull by digest   | User already has all layers existing on their local machine                                                    |                                                                                                                                                                                                                                                                                       |
| GET            | digest    | GET by different digest                                         | Pull by digest   | Image is multi-arch                                                                                            | The second GET by digest must be different from the first.                                                                                                                                                                                                                            |
| HEAD           | digest    | GET by same digest                                              | Pull by digest   | Image is single-arch and/or image is multi-arch but some part of the image already exists on the local machine |                                                                                                                                                                                                                                                                                       |
| HEAD           | digest    | GET by same digest, then a second GET by different digest       | Pull by Digest   | Image is multi-arch                                                                                            |                                                                                                                                                                                                                                                                                       |

### [Extension Summary data](#extension-summary-data)

There are two levels of extension summary data available:

* Core summary, with basic extension usage information: number of extension installs, uninstalls, and total install all times

The core-summary-data file contains the following data points for the selected time span:

| Data point      | Description                                      | Date added  |
| --------------- | ------------------------------------------------ | ----------- |
| Installs        | Number of installs for the extension             | Feb 1, 2024 |
| TotalInstalls   | Number of installs for the extension all times   | Feb 1, 2024 |
| Uninstalls      | Number of uninstalls for the extension           | Feb 1, 2024 |
| TotalUninstalls | Number of uninstalls for the extension all times | Feb 1, 2024 |
| Updates         | Number of updates for the extension              | Feb 1, 2024 |

* Premium summary, with advanced extension usage information: installs, uninstalls by unique users, extension opening by unique users.

The core-summary-data file contains the following data points for the selected time span:

| Data point       | Description                                       | Date added  |
| ---------------- | ------------------------------------------------- | ----------- |
| Installs         | Number of installs for the extension              | Feb 1, 2024 |
| UniqueInstalls   | Number of unique users installing the extension   | Feb 1, 2024 |
| Uninstalls       | Number of uninstalls for the extension            | Feb 1, 2024 |
| UniqueUninstalls | Number of unique users uninstalling the extension | Feb 1, 2024 |
| Usage            | Number of openings of the extension tab           | Feb 1, 2024 |
| UniqueUsers      | Number of unique users openings the extension tab | Feb 1, 2024 |

## [Changes in data over time](#changes-in-data-over-time)

The insights and analytics service is continuously improved to increase the value it brings to publishers. Some changes might include adding new data points, or improving existing data to make it more useful.

Changes in the dataset, such as added or removed fields, generally only apply from the date of when the field was first introduced, and going forward.

Refer to the tables in the [Data points](#data-points) section to see from which date a given data point is available.

## [Privacy](#privacy)

This section contains information about privacy-protecting measures that ensures consumers of content on Docker Hub remain completely anonymous.

> Important
>
> Docker never shares any Personally Identifiable Information (PII) as part of analytics data.

The image pulls summary dataset includes unique IP address count. This data point only includes the number of distinct unique IP addresses that request an image. Individual IP addresses are never shared.

The image pulls raw dataset includes user IP domains as a data point. This is the domain name associated with the IP address used to pull an image. If the IP type is `business`, the domain represents the company or organization associated with that IP address (for example, `docker.com`). For any other IP type that's not `business`, the domain represents the internet service provider or hosting provider used to make the request. On average, only about 30% of all pulls classify as the `business` IP type (this varies between publishers and images).

----
url: https://docs.docker.com/reference/build-checks/
----

# Build checks

***

***

BuildKit has built-in support for analyzing your build configuration based on a set of pre-defined rules for enforcing Dockerfile and building best practices. Adhering to these rules helps avoid errors and ensures good readability of your Dockerfile.

Checks run as a build invocation, but instead of producing a build output, it performs a series of checks to validate that your build doesn't violate any of the rules. To run a check, use the `--check` flag:

```console
$ docker build --check .
```

To learn more about how to use build checks, see [Checking your build configuration](https://docs.docker.com/build/checks/).

| Name                                                                             | Description                                                                                                                                                                                      |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [StageNameCasing](./stage-name-casing/)                                          | Stage names should be lowercase                                                                                                                                                                  |
| [FromAsCasing](./from-as-casing/)                                                | The 'as' keyword should match the case of the 'from' keyword                                                                                                                                     |
| [NoEmptyContinuation](./no-empty-continuation/)                                  | Empty continuation lines will become errors in a future release                                                                                                                                  |
| [ConsistentInstructionCasing](./consistent-instruction-casing/)                  | All commands within the Dockerfile should use the same casing (either upper or lower)                                                                                                            |
| [DuplicateStageName](./duplicate-stage-name/)                                    | Stage names should be unique                                                                                                                                                                     |
| [ReservedStageName](./reserved-stage-name/)                                      | Reserved words should not be used as stage names                                                                                                                                                 |
| [JSONArgsRecommended](./json-args-recommended/)                                  | JSON arguments recommended for ENTRYPOINT/CMD to prevent unintended behavior related to OS signals                                                                                               |
| [MaintainerDeprecated](./maintainer-deprecated/)                                 | The MAINTAINER instruction is deprecated, use a label instead to define an image author                                                                                                          |
| [UndefinedArgInFrom](./undefined-arg-in-from/)                                   | FROM command must use declared ARGs                                                                                                                                                              |
| [WorkdirRelativePath](./workdir-relative-path/)                                  | Relative workdir without an absolute workdir declared within the build can have unexpected results if the base image changes                                                                     |
| [UndefinedVar](./undefined-var/)                                                 | Variables should be defined before their use                                                                                                                                                     |
| [MultipleInstructionsDisallowed](./multiple-instructions-disallowed/)            | Multiple instructions of the same type should not be used in the same stage                                                                                                                      |
| [LegacyKeyValueFormat](./legacy-key-value-format/)                               | Legacy key/value format with whitespace separator should not be used                                                                                                                             |
| [RedundantTargetPlatform](./redundant-target-platform/)                          | Setting platform to predefined $TARGETPLATFORM in FROM is redundant as this is the default behavior                                                                                              |
| [SecretsUsedInArgOrEnv](./secrets-used-in-arg-or-env/)                           | Sensitive data should not be used in the ARG or ENV commands                                                                                                                                     |
| [InvalidDefaultArgInFrom](./invalid-default-arg-in-from/)                        | Default value for global ARG results in an empty or invalid base image name                                                                                                                      |
| [FromPlatformFlagConstDisallowed](./from-platform-flag-const-disallowed/)        | FROM --platform flag should not use a constant value                                                                                                                                             |
| [CopyIgnoredFile](./copy-ignored-file/)                                          | Attempting to Copy file that is excluded by .dockerignore                                                                                                                                        |
| [InvalidDefinitionDescription (experimental)](./invalid-definition-description/) | Comment for build stage or argument should follow the format: \`# \`. If this is not intended to be a description comment, add an empty line or comment between the instruction and the comment. |
| [ExposeProtoCasing](./expose-proto-casing/)                                      | Protocol in EXPOSE instruction should be lowercase                                                                                                                                               |
| [ExposeInvalidFormat](./expose-invalid-format/)                                  | IP address and host-port mapping should not be used in EXPOSE instruction. This will become an error in a future release                                                                         |

----
url: https://docs.docker.com/reference/api/registry/latest/
----

* General

  * Overview
  * Authentication
  * Pulling Images
  * Pushing Images
  * Deleting Images

* API

  * Manifests

    * getGet image manifest
    * putPut image manifest
    * headCheck if manifest exists
    * delDelete image manifest

  * Blobs

    * postInitiate blob upload or attempt cross-repository blob mount
    * headCheck existence of blob
    * getRetrieve blob
    * getGet blob upload status
    * putComplete blob upload
    * patchUpload blob chunk
    * delCancel blob upload

[API docs by Redocly](https://redocly.com/redoc/)

# Supported registry API for Docker Hub

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/registry/latest.yaml)

Docker Hub is an OCI-compliant registry, which means it adheres to the open standards defined by the Open Container Initiative (OCI) for distributing container images. This ensures compatibility with a wide range of tools and platforms in the container ecosystem.

This reference documents the Docker Hub-supported subset of the Registry HTTP API V2. It focuses on pulling, pushing, and deleting images. It does not cover the full OCI Distribution Specification.

For the complete OCI specification, see [OCI Distribution Specification](https://github.com/opencontainers/distribution-spec).

## [](#tag/overview)Overview

All endpoints in this API are prefixed by the version and repository name, for example:

```
/v2/<name>/
```

This format provides structured access control and URI-based scoping of image operations.

For example, to interact with the `library/ubuntu` repository, use:

```
/v2/library/ubuntu/
```

Repository names must meet these requirements:

1. Consist of path components matching `[a-z0-9]+(?:[._-][a-z0-9]+)*`
2. If more than one component, they must be separated by `/`
3. Full repository name must be fewer than 256 characters

## [](#tag/authentication)Authentication

Specifies registry authentication.

[Detailed authentication workflow and token usage](https://docs.docker.com/reference/api/registry/auth/)

## [](#tag/pull)Pulling Images

Pulling an image involves retrieving the manifest and downloading each of the image's layer blobs. This section outlines the general steps followed by a working example.

1. [Get a bearer token for the repository](https://docs.docker.com/reference/api/registry/auth/).

2. [Get the image manifest](#operation/GetImageManifest).

3. If the response in the previous step is a multi-architecture manifest list, you must do the following:

   * Parse the `manifests[]` array to locate the digest for your target platform (e.g., `linux/amd64`).
   * [Get the image manifest](#operation/GetImageManifest) using the located digest.

4. [Check if the blob exists](#operation/CheckBlobExists) before downloading. The client should send a `HEAD` request for each layer digest.

5. [Download each layer blob](#operation/GetBlob) using the digest obtained from the manifest. The client should send a `GET` request for each layer digest.

The following bash script example pulls `library/ubuntu:latest` from Docker Hub.

```bash
#!/bin/bash

# Step 1: Get a bearer token
TOKEN=$(curl -s "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/ubuntu:pull" | jq -r .token)

# Step 2: Get the image manifest. In this example, an image manifest list is returned.
curl -s -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.list.v2+json" \
     https://registry-1.docker.io/v2/library/ubuntu/manifests/latest \
     -o manifest-list.json

# Step 3a: Parse the `manifests[]` array to locate the digest for your target platform (e.g., `linux/amd64`).
IMAGE_MANIFEST_DIGEST=$(jq -r '.manifests[] | select(.platform.architecture == "amd64" and .platform.os == "linux") | .digest' manifest-list.json)

# Step 3b: Get the platform-specific image manifest
curl -s -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
     https://registry-1.docker.io/v2/library/ubuntu/manifests/$IMAGE_MANIFEST_DIGEST \
     -o manifest.json

# Step 4: Send a HEAD request to check if the layer blob exists
DIGEST=$(jq -r '.layers[0].digest' manifest.json)
curl -I -H "Authorization: Bearer $TOKEN" \
     https://registry-1.docker.io/v2/library/ubuntu/blobs/$DIGEST

# Step 5: Download the layer blob
curl -L -H "Authorization: Bearer $TOKEN" \
     https://registry-1.docker.io/v2/library/ubuntu/blobs/$DIGEST
```

This example pulls the manifest and the first layer for the `ubuntu:latest` image on the `linux/amd64` platform. Repeat steps 4 and 5 for each digest in the `.layers[]` array in the manifest.

## [](#tag/push)Pushing Images

Pushing an image involves uploading any image blobs (such as the config or layers), and then uploading the manifest that references those blobs.

This section outlines the basic steps to push an image using the registry API.

1. [Get a bearer token for the repository](https://docs.docker.com/reference/api/registry/auth/)

2. [Check if the blob exists](#operation/CheckBlobExists) using a `HEAD` request for each blob digest.

3. If the blob does not exist, [upload the blob](#operation/CompleteBlobUpload) using a monolithic `PUT` request:

   * First, [initiate the upload](#operation/InitiateBlobUpload) with `POST`.
   * Then [upload and complete](#operation/CompleteBlobUpload) with `PUT`.

   **Note**: Alternatively, you can upload the blob in multiple chunks by using `PATCH` requests to send each chunk, followed by a final `PUT` request to complete the upload. This is known as a [chunked upload](#operation/UploadBlobChunk) and is useful for large blobs or when resuming interrupted uploads.

4. [Upload the image manifest](#operation/PutImageManifest) using a `PUT` request to associate the config and layers.

The following bash script example pushes a dummy config blob and manifest to `yourusername/helloworld:latest` on Docker Hub. You can replace `yourusername` with your Docker Hub username and `dckr_pat` with your Docker Hub personal access token.

```bash
#!/bin/bash

USERNAME=yourusername
PASSWORD=dckr_pat
REPO=yourusername/helloworld
TAG=latest
CONFIG=config.json
MIME_TYPE=application/vnd.docker.container.image.v1+json

# Step 1: Get a bearer token
TOKEN=$(curl -s -u "$USERNAME:$PASSWORD" \
"https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:push,pull" \
| jq -r .token)

# Create a dummy config blob and compute its digest
echo '{"architecture":"amd64","os":"linux","config":{},"rootfs":{"type":"layers","diff_ids":[]}}' > $CONFIG
DIGEST="sha256:$(sha256sum $CONFIG | awk '{print $1}')"

# Step 2: Check if the blob exists
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -I \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/$REPO/blobs/$DIGEST)

if [ "$STATUS" != "200" ]; then
  # Step 3: Upload blob using monolithic upload
  LOCATION=$(curl -sI -X POST \
    -H "Authorization: Bearer $TOKEN" \
    https://registry-1.docker.io/v2/$REPO/blobs/uploads/ \
    | grep -i Location | tr -d '\r' | awk '{print $2}')

  curl -s -X PUT "$LOCATION&digest=$DIGEST" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/octet-stream" \
    --data-binary @$CONFIG
fi

# Step 4: Upload the manifest that references the config blob
MANIFEST=$(cat <<EOF
{
  "schemaVersion": 2,
  "mediaType": "application/vnd.docker.distribution.manifest.v2+json",
  "config": {
    "mediaType": "$MIME_TYPE",
    "size": $(stat -c%s $CONFIG),
    "digest": "$DIGEST"
  },
  "layers": []
}
EOF
)

curl -s -X PUT \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/vnd.docker.distribution.manifest.v2+json" \
  -d "$MANIFEST" \
  https://registry-1.docker.io/v2/$REPO/manifests/$TAG

echo "Pushed image to $REPO:$TAG"
```

This example pushes a minimal image with no layers. To push a complete image, repeat steps 2–3 for each layer and include the layer digests in the `layers[]` field of the manifest.

## [](#tag/delete)Deleting Images

Deleting an image involves removing its manifest by digest. You must first retrieve the manifest digest, then issue a `DELETE` request using that digest.

Only untagged manifests (or those not referenced by other tags or images) can be deleted. If a manifest is still referenced, the registry returns `403 Forbidden`.

> **Note**
>
> Manifest deletion operations may experience latency and could return a `500 Internal Server Error` during deletion. The system automatically retries the deletion in the background, so the manifest will eventually be removed. You do not need to manually retry the request.

This section outlines the basic steps to delete an image using the registry API.

1. [Get a bearer token for the repository](https://docs.docker.com/reference/api/registry/auth/).
2. [Get the manifest](#operation/GetImageManifest) using the image's tag.
3. Retrieve the `Docker-Content-Digest` header from the manifest response. This digest uniquely identifies the manifest.
4. [Delete the manifest](#operation/DeleteImageManifest) using a `DELETE` request and the digest.

The following bash script example deletes the `latest` tag from `yourusername/helloworld` on Docker Hub. Replace `yourusername` with your Docker Hub username and `dckr_pat` with your Docker Hub personal access token.

```bash
#!/bin/bash

USERNAME=yourusername
PASSWORD=dckr_pat
REPO=yourusername/helloworld
TAG=latest

# Step 1: Get a bearer token
TOKEN=$(curl -s -u "$USERNAME:$PASSWORD" \
  "https://auth.docker.io/token?service=registry.docker.io&scope=repository:$REPO:pull,push,delete" \
  | jq -r .token)

# Step 2 and 3: Get the manifest and extract the digest from response headers
DIGEST=$(curl -sI -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  https://registry-1.docker.io/v2/$REPO/manifests/$TAG \
  | grep -i Docker-Content-Digest | tr -d '\r' | awk '{print $2}')

echo "Deleting manifest with digest: $DIGEST"

# Step 4: Delete the manifest by digest
curl -s -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/$REPO/manifests/$DIGEST

echo "Deleted image: $REPO@$DIGEST"
```

This example deletes the manifest for the `latest` tag. To fully delete all references to an image, ensure no other tags or referrers point to the same manifest digest.

## [](#tag/Manifests)Manifests

Image manifests are JSON documents that describe an image: its configuration blob, the digests of each layer blob, and metadata such as media‑types and annotations.

## [](#tag/Manifests/operation/GetImageManifest)Get image manifest

Fetch the manifest identified by `name` and `reference`, where `reference` can be a tag (e.g., `latest`) or a digest (e.g., `sha256:...`).

The manifest contains metadata about the image, including configuration and layer digests. It is required for pulling images from the registry.

This endpoint requires authentication. Use the `Authorization: Bearer <token>` header.

##### path Parameters

|                   |                                                                                                     |
| ----------------- | --------------------------------------------------------------------------------------------------- |
| namerequired      | stringExample: library/ubuntuName of the target repository                                          |
| referencerequired | stringExamples:- latest - Tag
- sha256:abc123def456... - DigestTag or digest of the target manifest |

##### header Parameters

|                       |                                                                                                                                                                                                                                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Authorizationrequired | stringRFC7235-compliant authorization header (e.g., `Bearer <token>`).                                                                                                                                                                                                                                             |
| Accept                | stringMedia type(s) the client supports for the manifest.The registry supports the following media types:- application/vnd.docker.distribution.manifest.v2+json
- application/vnd.docker.distribution.manifest.list.v2+json
- application/vnd.oci.image.manifest.v1+json
- application/vnd.oci.image.index.v1+json |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/manifests/{reference}

### Request samples

* cURL

```
# GET a manifest (by tag or digest)
curl -H "Authorization: Bearer $TOKEN" \
     -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
     https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
```

### Response samples

* 200

Content type

application/vnd.docker.distribution.manifest.v2+json

`{
"schemaVersion": 2,
"mediaType": "application/vnd.docker.distribution.manifest.v2+json",
"config": {
"mediaType": "application/vnd.docker.container.image.v1+json",
"size": 7023,
"digest": "sha256:123456abcdef..."
},
"layers": [
{
"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
"size": 32654,
"digest": "sha256:abcdef123456..."
},
{
"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
"size": 16724,
"digest": "sha256:7890abcdef12..."
}
]
}`

## [](#tag/Manifests/operation/PutImageManifest)Put image manifest

Upload an image manifest for a given tag or digest. This operation registers a manifest in a repository, allowing it to be pulled using the specified reference.

This endpoint is typically used after all layer and config blobs have been uploaded to the registry.

The manifest must conform to the expected schema and media type. For Docker image manifest schema version 2, use: `application/vnd.docker.distribution.manifest.v2+json`

Requires authentication via a bearer token with `push` scope for the target repository.

##### path Parameters

|                   |                                                                                                                      |
| ----------------- | -------------------------------------------------------------------------------------------------------------------- |
| namerequired      | stringExample: library/ubuntuName of the target Repository                                                           |
| referencerequired | stringExamples:- latest - Tag
- sha256:abc123def456... - DigestTag or digest to associate with the uploaded Manifest |

##### header Parameters

|                       |                                                                                                               |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| Authorizationrequired | stringRFC7235-compliant authorization header (e.g., `Bearer <token>`).                                        |
| Content-Typerequired  | stringExample: application/vnd.docker.distribution.manifest.v2+jsonMedia type of the manifest being uploaded. |

##### Request Body schema: application/vnd.docker.distribution.manifest.v2+jsonrequired

|                       |                  |
| --------------------- | ---------------- |
| schemaVersionrequired | integer          |
| mediaTyperequired     | string           |
| required              | object           |
| required              | Array of objects |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/manifests/{reference}

### Request samples

* Payload
* cURL

Content type

application/vnd.docker.distribution.manifest.v2+json

`{
"schemaVersion": 2,
"mediaType": "application/vnd.docker.distribution.manifest.v2+json",
"config": {
"mediaType": "application/vnd.docker.container.image.v1+json",
"size": 7023,
"digest": "sha256:123456abcdef..."
},
"layers": [
{
"mediaType": "application/vnd.docker.image.rootfs.diff.tar.gzip",
"size": 32654,
"digest": "sha256:abcdef123456..."
}
]
}`

## [](#tag/Manifests/operation/HeadImageManifest)Check if manifest exists

Use this endpoint to verify whether a manifest exists by tag or digest.

This is a lightweight operation that returns only headers (no body). It is useful for:

* Checking for the existence of a specific image version
* Determining the digest or size of a manifest before downloading or deleting

This endpoint requires authentication with pull scope.

##### path Parameters

|                   |                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------- |
| namerequired      | stringExample: library/ubuntuName of the Repository                                   |
| referencerequired | stringExamples:- latest - Tag
- sha256:abc123def456... - DigestTag or digest to check |

##### header Parameters

|                       |                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Authorizationrequired | stringBearer token for authentication                                                                                                                      |
| Accept                | stringExample: application/vnd.docker.distribution.manifest.v2+jsonMedia type of the manifest to check. The response will match one of the accepted types. |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/manifests/{reference}

### Request samples

* cURL

```
# HEAD /v2/{name}/manifests/{reference}
curl -I \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  https://registry-1.docker.io/v2/library/ubuntu/manifests/latest
```

## [](#tag/Manifests/operation/DeleteImageManifest)Delete image manifest

Delete an image manifest from a repository by digest.

Only untagged or unreferenced manifests can be deleted. If the manifest is still referenced by a tag or another image, the registry will return `403 Forbidden`.

This operation requires `delete` access to the repository.

> **Note**
>
> Manifest deletion operations may take some time and could return a `500 Internal Server Error`. The system automatically retries the deletion in the background. Manual intervention is not required.

##### path Parameters

|                   |                                                                                            |
| ----------------- | ------------------------------------------------------------------------------------------ |
| namerequired      | stringExample: yourusername/helloworldName of the repository                               |
| referencerequired | stringExample: sha256:abc123def456...Digest of the manifest to delete (e.g., `sha256:...`) |

##### header Parameters

|                       |                                         |
| --------------------- | --------------------------------------- |
| Authorizationrequired | stringBearer token with `delete` access |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/manifests/{reference}

### Request samples

* cURL

```
# DELETE a manifest by digest
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/yourusername/helloworld/manifests/sha256:abc123def456...
```

## [](#tag/Blobs)Blobs

Blobs are the binary objects referenced from manifests: the config JSON and one or more compressed layer tarballs.

## [](#tag/Blobs/operation/InitiateBlobUpload)Initiate blob upload or attempt cross-repository blob mount

Initiate an upload session for a blob (layer or config) in a repository.

This is the first step in uploading a blob. It returns a `Location` URL where the blob can be uploaded using `PATCH` (chunked) or `PUT` (monolithic).

Instead of uploading a blob, a client may attempt to mount a blob from another repository (if it has read access) by including the `mount` and `from` query parameters.

If successful, the registry responds with `201 Created` and the blob is reused without re-upload.

If the mount fails, the upload proceeds as usual and returns a `202 Accepted`.

You must authenticate with `push` access to the target repository.

##### path Parameters

|              |                                                            |
| ------------ | ---------------------------------------------------------- |
| namerequired | stringExample: library/ubuntuName of the target repository |

##### query Parameters

|       |                                                                                                |
| ----- | ---------------------------------------------------------------------------------------------- |
| mount | stringExample: mount=sha256:abc123def456...Digest of the blob to mount from another repository |
| from  | stringExample: from=library/busyboxSource repository to mount the blob from                    |

##### header Parameters

|                       |                                                         |
| --------------------- | ------------------------------------------------------- |
| Authorizationrequired | stringBearer token for authentication with `push` scope |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/uploads/

### Request samples

* cURL (Initiate Standard Upload)
* cURL (Cross-Repository Blob Mount)

```
# Initiate a standard blob upload session
curl -i -X POST \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/
```

## [](#tag/Blobs/operation/CheckBlobExists)Check existence of blob

Check whether a blob (layer or config) exists in the registry.

This is useful before uploading a blob to avoid duplicates.

If the blob is present, the registry returns a `200 OK` response with headers like `Content-Length` and `Docker-Content-Digest`.

If the blob does not exist, the response will be `404 Not Found`.

##### path Parameters

|                |                                                             |
| -------------- | ----------------------------------------------------------- |
| namerequired   | stringExample: library/ubuntuName of the Repository         |
| digestrequired | stringExample: sha256:abc123def4567890...Digest of the blob |

##### header Parameters

|                       |                                                                                           |
| --------------------- | ----------------------------------------------------------------------------------------- |
| Authorizationrequired | stringExample: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6...Bearer token with pull or push scope |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/{digest}

### Request samples

* cURL

```
# HEAD to check if a blob exists
curl -I \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/sha256:abc123...
```

### Response samples

* 200

Content type

application/json

Example

Sample request

`{
"method": "HEAD",
"url": "/v2/library/ubuntu/blobs/sha256:abc123def4567890...",
"headers": {
"Authorization": "Bearer <token>",
"Accept": "*/*"
}
}`

## [](#tag/Blobs/operation/GetBlob)Retrieve blob

Download the blob identified by digest from the registry.

Blobs include image layers and configuration objects. Clients must use the digest from the manifest to retrieve a blob.

This endpoint may return a `307 Temporary Redirect` to a CDN or storage location. Clients must follow the redirect to obtain the actual blob content.

The blob content is typically a gzipped tarball (for layers) or JSON (for configs). The MIME type is usually `application/octet-stream`.

##### path Parameters

|                |                                                         |
| -------------- | ------------------------------------------------------- |
| namerequired   | stringExample: library/ubuntuRepository Name            |
| digestrequired | stringExample: sha256:abc123def456...Digest of the Blob |

##### header Parameters

|                       |                                                                                   |
| --------------------- | --------------------------------------------------------------------------------- |
| Authorizationrequired | stringExample: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6...Bearer token with pull scope |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/{digest}

### Request samples

* cURL

```
# GET (download) a blob
curl -L \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/sha256:abc123... \
  -o layer.tar.gz
```

### Response samples

* 200

Content type

application/octet-stream

```
<binary data not shown>
```

## [](#tag/Blobs/operation/GetBlobUploadStatus)Get blob upload status

Retrieve the current status of an in-progress blob upload.

This is useful for:

* Resuming an interrupted upload
* Determining how many bytes have been accepted so far
* Retrying from the correct offset in chunked uploads

The response includes the `Range` header indicating the byte range received so far, and a `Docker-Upload-UUID` for identifying the session.

##### path Parameters

|              |                                              |
| ------------ | -------------------------------------------- |
| namerequired | stringExample: library/ubuntuRepository Name |
| uuidrequired | stringExample: abc123Upload session UUID     |

##### header Parameters

|                       |                                     |
| --------------------- | ----------------------------------- |
| Authorizationrequired | stringExample: Bearer eyJhbGciOi... |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/uploads/{uuid}

### Request samples

* cURL

```
# GET upload status
curl -I \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123
```

## [](#tag/Blobs/operation/CompleteBlobUpload)Complete blob upload

Complete the upload of a blob by finalizing an upload session.

This request must include the `digest` query parameter and optionally the last chunk of data. When the registry receives this request, it verifies the digest and stores the blob.

This endpoint supports:

* Monolithic uploads (upload entire blob in this request)
* Finalizing chunked uploads (last chunk plus `digest`)

##### path Parameters

|              |                                                                         |
| ------------ | ----------------------------------------------------------------------- |
| namerequired | stringExample: library/ubuntuRepository name                            |
| uuidrequired | stringExample: abc123Upload session UUID returned from the POST request |

##### query Parameters

|                |                                                                     |
| -------------- | ------------------------------------------------------------------- |
| digestrequired | stringExample: digest=sha256:abcd1234...Digest of the uploaded blob |

##### header Parameters

|                       |                                     |
| --------------------- | ----------------------------------- |
| Authorizationrequired | stringExample: Bearer eyJhbGciOi... |

##### Request Body schema: application/octet-streamoptional

string \<binary>

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/uploads/{uuid}

### Request samples

* Payload
* cURL

Content type

application/octet-stream

```
<binary data not shown>
```

## [](#tag/Blobs/operation/UploadBlobChunk)Upload blob chunk

Upload a chunk of a blob to an active upload session.

Use this method for **chunked uploads**, especially for large blobs or when resuming interrupted uploads.

The client sends binary data using `PATCH`, optionally including a `Content-Range` header.

After each chunk is accepted, the registry returns a `202 Accepted` response with:

* `Range`: current byte range stored
* `Docker-Upload-UUID`: identifier for the upload session
* `Location`: URL to continue the upload or finalize with `PUT`

##### path Parameters

|              |                                              |
| ------------ | -------------------------------------------- |
| namerequired | stringExample: library/ubuntuRepository name |
| uuidrequired | stringExample: abc123Upload session UUID     |

##### header Parameters

|                       |                                                                          |
| --------------------- | ------------------------------------------------------------------------ |
| Authorizationrequired | stringExample: Bearer eyJhbGciOi...                                      |
| Content-Range         | stringExample: bytes 0-65535Optional. Byte range of the chunk being sent |

##### Request Body schema: application/octet-streamrequired

string \<binary>

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/uploads/{uuid}

### Request samples

* Payload
* cURL

Content type

application/octet-stream

```
<binary data not shown>
```

## [](#tag/Blobs/operation/CancelBlobUpload)Cancel blob upload

Cancel an in-progress blob upload session.

This operation discards any data that has been uploaded and invalidates the upload session.

Use this when:

* An upload fails or is aborted mid-process
* The client wants to clean up unused upload sessions

After cancellation, the UUID is no longer valid and a new `POST` must be issued to restart the upload.

##### path Parameters

|              |                                                     |
| ------------ | --------------------------------------------------- |
| namerequired | stringExample: library/ubuntuName of the repository |
| uuidrequired | stringExample: abc123Upload session UUID            |

##### header Parameters

|                       |                                     |
| --------------------- | ----------------------------------- |
| Authorizationrequired | stringExample: Bearer eyJhbGciOi... |

### Responses

Docker Hub registry API

https\://registry-1.docker.io/v2/{name}/blobs/uploads/{uuid}

### Request samples

* cURL

```
# DELETE – cancel an upload session
curl -X DELETE \
  -H "Authorization: Bearer $TOKEN" \
  https://registry-1.docker.io/v2/library/ubuntu/blobs/uploads/abc123`
```

----
url: https://docs.docker.com/reference/cli/sbx/secret/ls/
----

# sbx secret ls

| Description | List stored secrets               |
| ----------- | --------------------------------- |
| Usage       | `sbx secret ls [SANDBOX] [flags]` |

## [Options](#options)

| Option         | Default | Description                   |
| -------------- | ------- | ----------------------------- |
| `-g, --global` |         | Only list global secrets      |
| `--service`    |         | Filter by secret service name |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# List all secrets
sbx secret ls

# List only global secrets
sbx secret ls -g

# List secrets for a specific sandbox
sbx secret ls my-sandbox

# Filter by service
sbx secret ls --service github
```

----
url: https://docs.docker.com/reference/cli/docker/checkpoint/rm/
----

# docker checkpoint rm

***

| Description                                                               | Remove a checkpoint                                   |
| ------------------------------------------------------------------------- | ----------------------------------------------------- |
| Usage                                                                     | `docker checkpoint rm [OPTIONS] CONTAINER CHECKPOINT` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker checkpoint remove`                            |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Remove a checkpoint

## [Options](#options)

| Option             | Default | Description                               |
| ------------------ | ------- | ----------------------------------------- |
| `--checkpoint-dir` |         | Use a custom checkpoint storage directory |

----
url: https://docs.docker.com/testcontainers/
----

# Testcontainers

***

Table of contents

***

Testcontainers is a set of open source libraries that provides easy and lightweight APIs for bootstrapping local development and test dependencies with real services wrapped in Docker containers. Using Testcontainers, you can write tests that depend on the same services you use in production without mocks or in-memory services.

### [What is Testcontainers?](https://testcontainers.com/getting-started/#what-is-testcontainers)

[Learn about what Testcontainers does and its key benefits](https://testcontainers.com/getting-started/#what-is-testcontainers)

### [The Testcontainers workflow](https://testcontainers.com/getting-started/#testcontainers-workflow)

[Understand the Testcontainers workflow](https://testcontainers.com/getting-started/#testcontainers-workflow)

## [Quickstart](#quickstart)

### [Supported languages](#supported-languages)

Testcontainers provide support for the most popular languages, and Docker sponsors the development of the following Testcontainers implementations:

* [Go](https://golang.testcontainers.org/quickstart/)
* [Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

The rest are community-driven and maintained by independent contributors.

### [Prerequisites](#prerequisites)

Testcontainers requires a Docker-API compatible container runtime. During development, Testcontainers is actively tested against recent versions of Docker on Linux, as well as against Docker Desktop on Mac and Windows. These Docker environments are automatically detected and used by Testcontainers without any additional configuration being necessary.

It is possible to configure Testcontainers to work for other Docker setups, such as a remote Docker host or Docker alternatives. However, these are not actively tested in the main development workflow, so not all Testcontainers features might be available and additional manual configuration might be necessary.

If you have further questions about configuration details for your setup or whether it supports running Testcontainers-based tests, contact the Testcontainers team and other users from the Testcontainers community on [Slack](https://slack.testcontainers.org/).

### [Testcontainers for Go](https://golang.testcontainers.org/quickstart/)

[A Go package that makes it simple to create and clean up container-based dependencies for automated integration/smoke tests.](https://golang.testcontainers.org/quickstart/)

### [Testcontainers for Java](https://java.testcontainers.org/)

[A Java library that supports JUnit tests, providing lightweight, throwaway instances of anything that can run in a Docker container.](https://java.testcontainers.org/)

## [Guides](#guides)

Explore hands-on Testcontainers guides to learn how to use Testcontainers with different languages and popular frameworks:

* [Getting started with Testcontainers for .NET](/guides/testcontainers-dotnet-getting-started/)
* [Getting started with Testcontainers for Go](/guides/testcontainers-go-getting-started/)
* [Getting started with Testcontainers for Java](/guides/testcontainers-java-getting-started/)
* [Getting started with Testcontainers for Node.js](/guides/testcontainers-nodejs-getting-started/)
* [Getting started with Testcontainers for Python](/guides/testcontainers-python-getting-started/)
* [Testing a Spring Boot REST API with Testcontainers](/guides/testcontainers-java-spring-boot-rest-api/)
* [Testcontainers container lifecycle management](/guides/testcontainers-java-lifecycle/)
* [Replace H2 with a real database for testing](/guides/testcontainers-java-replace-h2/)
* [Configuration of services running in a container](/guides/testcontainers-java-service-configuration/)
* [Testing an ASP.NET Core web app](/guides/testcontainers-dotnet-aspnet-core/)
* [Testing Spring Boot Kafka Listener](/guides/testcontainers-java-spring-boot-kafka/)
* [Testing REST API integrations using MockServer](/guides/testcontainers-java-mockserver/)
* [Testing AWS service integrations using LocalStack](/guides/testcontainers-java-aws-localstack/)
* [Testing Quarkus applications with Testcontainers](/guides/testcontainers-java-quarkus/)
* [Working with jOOQ and Flyway using Testcontainers](/guides/testcontainers-java-jooq-flyway/)
* [Testing REST API integrations using WireMock](/guides/testcontainers-java-wiremock/)
* [Securing Spring Boot with Keycloak and Testcontainers](/guides/testcontainers-java-keycloak-spring-boot/)
* [Testing Micronaut REST API with WireMock](/guides/testcontainers-java-micronaut-wiremock/)
* [Testing Micronaut Kafka Listener](/guides/testcontainers-java-micronaut-kafka/)

----
url: https://docs.docker.com/reference/cli/docker/dhi/customization/list/
----

# docker dhi customization list

***

| Description | List all customizations         |
| ----------- | ------------------------------- |
| Usage       | `docker dhi customization list` |

## [Description](#description)

List all Docker Hardened Images customizations

## [Options](#options)

| Option         | Default | Description                                                          |
| -------------- | ------- | -------------------------------------------------------------------- |
| `--bulk-id`    |         | Filter by bulk customization ID (exact match)                        |
| `-f, --filter` |         | Filter by customization name (case-insensitive substring match)      |
| `--json`       |         | Output in JSON format                                                |
| `-r, --repo`   |         | Filter by destination repository (case-insensitive substring match)  |
| `--source`     |         | Filter by DHI source repository (case-insensitive substring match)   |

----
url: https://docs.docker.com/reference/cli/docker/compose/create/
----

# docker compose create

***

| Description | Creates containers for a service               |
| ----------- | ---------------------------------------------- |
| Usage       | `docker compose create [OPTIONS] [SERVICE...]` |

## [Description](#description)

Creates containers for a service

## [Options](#options)

| Option             | Default  | Description                                                                                    |
| ------------------ | -------- | ---------------------------------------------------------------------------------------------- |
| `--build`          |          | Build images before starting containers                                                        |
| `--force-recreate` |          | Recreate containers even if their configuration and image haven't changed                      |
| `--no-build`       |          | Don't build an image, even if it's policy                                                      |
| `--no-recreate`    |          | If containers already exist, don't recreate them. Incompatible with --force-recreate.          |
| `--pull`           | `policy` | Pull image before running ("always"\|"missing"\|"never"\|"build")                              |
| `--quiet-pull`     |          | Pull without printing progress information                                                     |
| `--remove-orphans` |          | Remove containers for services not defined in the Compose file                                 |
| `--scale`          |          | Scale SERVICE to NUM instances. Overrides the `scale` setting in the Compose file if present.  |
| `-y, --yes`        |          | Assume "yes" as answer to all prompts and run non-interactively                                |

----
url: https://docs.docker.com/reference/cli/sbx/run/
----

# sbx run

| Description | Run an agent in a sandbox                              |
| ----------- | ------------------------------------------------------ |
| Usage       | `sbx run [flags] [AGENT] [PATH...] [-- AGENT_ARGS...]` |

## [Description](#description)

Run an agent in a sandbox, creating the sandbox if it does not already exist.

The first positional argument is the agent to run. To re-attach to an existing sandbox by name, use --name; the agent positional is optional when the named sandbox already exists and is read from its spec.

Pass agent arguments after the "--" separator. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

To create a sandbox without attaching, use "sbx create" instead.

Available agents: claude, codex, copilot, cursor, docker-agent, droid, gemini, kiro, opencode, shell

## [Options](#options)

| Option           | Default | Description                                                                                                                                                                |
| ---------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--clone`        |         | Run the agent on a private in-container clone of the host Git repository; must be set at sandbox creation time (no-op when re-attaching to an existing clone-mode sandbox) |
| `--cpus`         | `0`     | Number of CPUs to allocate to the sandbox (0 = auto: N-1 host CPUs, min 1)                                                                                                 |
| `--kit`          |         | experimental Kit reference (directory, ZIP, or OCI). Can be specified multiple times                                                                                       |
| `-m, --memory`   |         | Memory limit in binary units (e.g., 1024m, 8g). Default: 50% of host memory, max 32 GiB                                                                                    |
| `--name`         |         | Name for the sandbox (default: \<agent>-\<workdir>)                                                                                                                        |
| `-t, --template` |         | Container image to use for the sandbox (default: agent-specific image)                                                                                                     |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Create and run a sandbox with claude in current directory
sbx run claude

# Create and run with additional workspaces (read-only)
sbx run claude . /path/to/docs:ro

# Re-attach to an existing sandbox by name (agent read from its spec)
sbx run --name existing-sandbox

# Re-attach to an existing sandbox by name and verify the expected agent
sbx run claude --name existing-sandbox

# Run a sandbox with agent arguments
sbx run claude -- --continue
```

----
url: https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/
----

# Troubleshoot topics for Docker Desktop

***

Table of contents

***

> Tip
>
> If you do not find a solution in troubleshooting, browse the GitHub repositories or [create a new issue](https://github.com/docker/desktop-feedback).

## [Topics for all platforms](#topics-for-all-platforms)

### [Certificates not set up correctly](#certificates-not-set-up-correctly)

#### [Error message](#error-message)

When attempting to pull from a registry using `docker run`, you may encounter the following error:

```console
Error response from daemon: Get http://192.168.203.139:5858/v2/: malformed HTTP response "\x15\x03\x01\x00\x02\x02"
```

Additionally, logs from the registry may show:

```console
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52882: tls: client didn't provide a certificate
2017/06/20 18:15:30 http: TLS handshake error from 192.168.203.139:52883: tls: first record does not look like a TLS handshake
```

#### [Possible causes](#possible-causes)

* Docker Desktop ignores certificates listed under insecure registries.
* Client certificates are not sent to insecure registries, causing handshake failures.

#### [Solution](#solution)

* Ensure that your registry is properly configured with valid SSL certificates.
* If your registry is self-signed, configure Docker to trust the certificate by adding it to Docker’s certificates directory (/etc/docker/certs.d/ on Linux).
* If the issue persists, check your Docker daemon configuration and enable TLS authentication.

### [Docker Desktop's UI appears green, distorted, or has visual artifacts](#docker-desktops-ui-appears-green-distorted-or-has-visual-artifacts)

#### [Cause](#cause)

Docker Desktop uses hardware-accelerated graphics by default, which may cause problems for some GPUs.

#### [Solution](#solution-1)

Disable hardware acceleration:

1. Edit Docker Desktop's `settings-store.json` file. You can find this file at:

   * Mac: `~/Library/Group Containers/group.com.docker/settings-store.json`
   * Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
   * Linux: `~/.docker/desktop/settings-store.json.`

2. Add the following entry:

   ```JSON
   $ "disableHardwareAcceleration": true
   ```

3. Save the file and restart Docker Desktop.

### [Using mounted volumes and getting runtime errors indicating an application file is not found, access to a volume mount is denied, or a service cannot start](#using-mounted-volumes-and-getting-runtime-errors-indicating-an-application-file-is-not-found-access-to-a-volume-mount-is-denied-or-a-service-cannot-start)

#### [Cause](#cause-1)

If your project directory is located outside your home directory (`/home/<user>`), Docker Desktop requires file sharing permissions to access it.

#### [Solution](#solution-2)

Enable file sharing in Docker Desktop for Mac and Linux:

1. Navigate to **Settings**, select **Resources** and then **File sharing**.
2. Add the drive or folder that contains the Dockerfile and volume mount paths.

Enable file sharing in Docker Desktop for Windows:

1. From **Settings**, select **Shared Folders**.
2. Share the folder that contains the Dockerfile and volume mount paths.

### [`port already allocated` errors](#port-already-allocated-errors)

#### [Error message](#error-message-1)

When starting a container, you may see an error like:

```text
Bind for 0.0.0.0:8080 failed: port is already allocated
```

Or

```text
listen tcp:0.0.0.0:8080: bind: address is already in use
```

#### [Cause](#cause-2)

* Another application on your system is already using the specified port.
* A previously running container was not stopped properly and is still bound to the port.

#### [Solution](#solution-3)

To discover the identity of this software, either:

* Use the `resmon.exe` GUI, select **Network** and then **Listening Ports**
* In PowerShell, use `netstat -aon | find /i "listening "` to discover the PID of the process currently using the port (the PID is the number in the rightmost column).

Then, decide whether to shut the other process down, or to use a different port in your Docker app.

## [Topics for Linux and Mac](#topics-for-linux-and-mac)

### [Docker Desktop fails to start on Mac or Linux platforms](#docker-desktop-fails-to-start-on-mac-or-linux-platforms)

#### [Error message](#error-message-2)

Docker fails to start due to Unix domain socket path length limitations:

```console
[vpnkit-bridge][F] listen unix HOME/Library/Containers/com.docker.docker/Data/http-proxy-control.sock: bind: invalid argument
```

```console
[com.docker.backend][E] listen(vsock:4099) failed: listen unix HOME/Library/Containers/com.docker.docker/Data/vms/0/00000002.00001003: bind: invalid argument
```

#### [Cause](#cause-3)

On Mac and Linux, Docker Desktop creates Unix domain sockets used for inter-process communication. These sockets are created under the user's home directory.

Unix domain sockets have a maximum path length:

* 104 characters on Mac
* 108 characters on Linux

If your home directory path is too long, Docker Desktop fails to create necessary sockets.

#### [Solution](#solution-4)

Ensure your username is short enough to keep paths within the allowed limit:

* Mac: Username should be ≤ 33 characters
* Linux: Username should be ≤ 55 characters

## [Topics for Mac](#topics-for-mac)

### [Upgrade requires administrator privileges](#upgrade-requires-administrator-privileges)

#### [Cause](#cause-4)

On macOS, users without administrator privileges cannot perform in-app upgrades from the Docker Desktop Dashboard.

#### [Solution](#solution-5)

> Important
>
> Do not uninstall the current version before upgrading. Doing so deletes all local Docker containers, images, and volumes.

To upgrade Docker Desktop:

* Ask an administrator to install the newer version over the existing one.
* Use the \[]`--user` install flag]\(/manuals/desktop/setup/install/mac-install.md#security-and-access) if appropriate for your setup.

### [Persistent notification telling me an application has changed my Desktop configurations](#persistent-notification-telling-me-an-application-has-changed-my-desktop-configurations)

#### [Cause](#cause-5)

You receive this notification because the Configuration integrity check feature has detected that a third-party application has altered your Docker Desktop configuration. This usually happens due to incorrect or missing symlinks. The notification ensures you are aware of these changes so you can review and repair any potential issues to maintain system reliability.

Opening the notification presents a pop-up window which provides detailed information about the detected integrity issues.

#### [Solution](#solution-6)

If you choose to ignore the notification, it will be shown again only at the next Docker Desktop startup. If you choose to repair your configuration, you won't be prompted again.

If you want to switch off Configuration integrity check notifications, navigate to Docker Desktop's settings and in the **General** tab, clear the **Automatically check configuration** setting.

### [`com.docker.vmnetd` is still running after I quit the app](#comdockervmnetd-is-still-running-after-i-quit-the-app)

The privileged helper process `com.docker.vmnetd` is started by `launchd` and runs in the background. The process does not consume any resources unless `Docker.app` connects to it, so it's safe to ignore.

### [Incompatible CPU detected](#incompatible-cpu-detected)

#### [Cause](#cause-6)

Docker Desktop requires a processor (CPU) that supports virtualization and, more specifically, the [Apple Hypervisor framework](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/).

#### [Solution](#solution-7)

Check that:

* You've installed the correct Docker Desktop for your architecture

* Your Mac supports Apple's Hypervisor framework. To check if your Mac supports the Hypervisor framework, run the following command in a terminal window.

  ```console
  $ sysctl kern.hv_support
  ```

  If your Mac supports the Hypervisor Framework, the command prints `kern.hv_support: 1`.

  If not, the command prints `kern.hv_support: 0`.

See also, [Hypervisor Framework Reference](https://developer.apple.com/library/mac/documentation/DriversKernelHardware/Reference/Hypervisor/) in the Apple documentation, and Docker Desktop [Mac system requirements](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements).

## [Topics for Windows](#topics-for-windows)

### [Docker Desktop fails to start when anti-virus software is installed](#docker-desktop-fails-to-start-when-anti-virus-software-is-installed)

#### [Cause](#cause-7)

Some anti-virus software may be incompatible with Hyper-V and Microsoft Windows builds. The conflict typically occurs after a Windows update and manifests as an error response from the Docker daemon and a Docker Desktop start failure.

#### [Solution](#solution-8)

For a temporary workaround, uninstall the anti-virus software, or add Docker to the exclusions/exceptions in your antivirus software.

### [Permissions errors on data directories for shared volumes](#permissions-errors-on-data-directories-for-shared-volumes)

#### [Cause](#cause-8)

When sharing files from Windows, Docker Desktop sets permissions on [shared volumes](https://docs.docker.com/desktop/settings-and-maintenance/settings/#file-sharing) to a default value of [0777](https://chmodcommand.com/chmod-0777/) (`read`, `write`, `execute` permissions for `user` and for `group`).

The default permissions on shared volumes are not configurable.

#### [Solution](#solution-9)

If you are working with applications that require different permissions, either:

* Use non-host-mounted volumes
* Find a way to make the applications work with the default file permissions

### [Unexpected syntax errors, use Unix style line endings for files in containers](#unexpected-syntax-errors-use-unix-style-line-endings-for-files-in-containers)

#### [Cause](#cause-9)

Docker containers expect Unix-style line `\n` endings, not Windows style: `\r\n`. This includes files referenced at the command line for builds and in RUN commands in Docker files.

Keep this in mind when authoring files such as shell scripts using Windows tools, where the default is likely to be Windows style line endings. These commands ultimately get passed to Unix commands inside a Unix based container (for example, a shell script passed to `/bin/sh`). If Windows style line endings are used, `docker run` fails with syntax errors.

#### [Solution](#solution-10)

* Convert files to Unix-style line endings using:

  ```console
  $ dos2unix script.sh
  ```

* In VS Code, set line endings to `LF` (Unix) instead of `CRLF` (Windows).

### [Path conversion errors on Windows](#path-conversion-errors-on-windows)

#### [Cause](#cause-10)

Unlike Linux, Windows requires explicit path conversion for volume mounting.

On Linux, the system takes care of mounting a path to another path. For example, when you run the following command on Linux:

```console
$ docker run --rm -ti -v /home/user/work:/work alpine
```

It adds a `/work` directory to the target container to mirror the specified path.

#### [Solution](#solution-11)

Update the source path. For example, if you are using the legacy Windows shell (`cmd.exe`), you can use the following command:

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
```

This starts the container and ensures the volume becomes usable. This is possible because Docker Desktop detects the Windows-style path and provides the appropriate conversion to mount the directory.

Docker Desktop also allows you to use Unix-style path to the appropriate format. For example:

```console
$ docker run --rm -ti -v /c/Users/user/work:/work alpine ls /work
```

### [Docker commands failing in Git Bash](#docker-commands-failing-in-git-bash)

#### [Error message](#error-message-3)

```console
$ docker run --rm -ti -v C:\Users\user\work:/work alpine
docker: Error response from daemon: mkdir C:UsersUserwork: Access is denied.
```

```console
$ docker run --rm -ti -v $(pwd):/work alpine
docker: Error response from daemon: OCI runtime create failed: invalid mount {Destination:\Program Files\Git\work Type:bind Source:/run/desktop/mnt/host/c/Users/user/work;C Options:[rbind rprivate]}: mount destination \Program Files\Git\work not absolute: unknown.
```

#### [Cause](#cause-11)

Git Bash (or MSYS) provides a Unix-like environment on Windows. These tools apply their own preprocessing on the command line.

This affects `$(pwd)`, colon-separated paths, and tilde (`~`)

Also, the `\` character has a special meaning in Git Bash.

#### [Solution](#solution-12)

* Disable Git Bash path conversion temporarily. For example, run the command with MSYS path conversion disable:
  ```console
  $ MSYS_NO_PATHCONV=1 docker run --rm -ti -v $(pwd):/work alpine
  ```

* Use proper path formatting:

  * Use double forward and backslashes (`\\` `//`) instead of single (`\` `/`).
  * If referencing `$(pwd)`, add an extra `/`:

Portability of the scripts is not affected as Linux treats multiple `/` as a single entry.

### [Docker Desktop fails due to Virtualization not working](#docker-desktop-fails-due-to-virtualization-not-working)

#### [Error message](#error-message-4)

A typical error message is "Docker Desktop - Unexpected WSL error" mentioning the error code `Wsl/Service/RegisterDistro/CreateVm/HCS/HCS_E_HYPERV_NOT_INSTALLED`. Manually executing `wsl` commands also fails with the same error code.

#### [Cause](#cause-12)

* Virtualization settings are disabled in the BIOS.
* Windows Hyper-V or WSL 2 components are missing.

Note some third-party software such as Android emulators will disable Hyper-V on install.

#### [Solutions](#solutions)

Your machine must have the following features for Docker Desktop to function correctly:

##### [WSL 2 and Windows Home](#wsl-2-and-windows-home)

1. Virtual Machine Platform
2. [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
3. [Virtualization enabled in the BIOS](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1) Note that many Windows devices already have virtualization enabled, so this may not apply.
4. Hypervisor enabled at Windows startup

It must be possible to run WSL 2 commands without error, for example:

```console
PS C:\users\> wsl -l -v
  NAME              STATE           VERSION
* Ubuntu            Running         2
  docker-desktop    Stopped         2
PS C:\users\> wsl -d docker-desktop echo WSL 2 is working
WSL 2 is working
```

If the features are enabled but the commands are not working, first check [Virtualization is turned on](#virtualization-must-be-turned-on) then [enable the Hypervisor at Windows startup](#hypervisor-enabled-at-windows-startup) if required. If running Docker Desktop in a Virtual Machine, ensure [the hypervisor has nested virtualization enabled](#turn-on-nested-virtualization).

##### [Hyper-V](#hyper-v)

On Windows 10 Pro or Enterprise, you can also use Hyper-V with the following features enabled:

1. [Hyper-V](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview) installed and working
2. [Virtualization enabled in the BIOS](https://support.microsoft.com/en-gb/windows/enable-virtualization-on-windows-c5578302-6e43-4b4b-a449-8ced115f58e1) Note that many Windows devices already have virtualization enabled, so this may not apply.
3. Hypervisor enabled at Windows startup

Docker Desktop requires Hyper-V as well as the Hyper-V Module for Windows PowerShell to be installed and enabled. The Docker Desktop installer enables it for you.

Docker Desktop also needs two CPU hardware features to use Hyper-V: Virtualization and Second Level Address Translation (SLAT), which is also called Rapid Virtualization Indexing (RVI). On some systems, Virtualization must be enabled in the BIOS. The steps required are vendor-specific, but typically the BIOS option is called `Virtualization Technology (VTx)` or something similar. Run the command `systeminfo` to check all required Hyper-V features. See [Pre-requisites for Hyper-V on Windows 10](https://docs.microsoft.com/en-us/virtualization/hyper-v-on-windows/reference/hyper-v-requirements) for more details.

To install Hyper-V manually, see [Install Hyper-V on Windows 10](https://msdn.microsoft.com/en-us/virtualization/hyperv_on_windows/quick_start/walkthrough_install). A reboot is *required* after installation. If you install Hyper-V without rebooting, Docker Desktop does not work correctly.

From the start menu, type **Turn Windows features on or off** and press enter. In the subsequent screen, verify that Hyper-V is enabled.

##### [Virtualization must be turned on](#virtualization-must-be-turned-on)

In addition to [Hyper-V](#hyper-v) or [WSL 2](https://docs.docker.com/desktop/features/wsl/), virtualization must be turned on. Check the Performance tab on the Task Manager. Alternatively, you can type `systeminfo` into your terminal. If you see `Hyper-V Requirements: A hypervisor has been detected. Features required for Hyper-V will not be displayed`, then virtualization is enabled.

If you manually uninstall Hyper-V, WSL 2 or turn off virtualization, Docker Desktop cannot start.

To turn on nested virtualization, see [Run Docker Desktop for Windows in a VM or VDI environment](https://docs.docker.com/desktop/setup/vm-vdi/#turn-on-nested-virtualization).

##### [Hypervisor enabled at Windows startup](#hypervisor-enabled-at-windows-startup)

If you have completed the previous steps and are still experiencing Docker Desktop startup issues, this could be because the Hypervisor is installed, but not launched during Windows startup. Some tools (such as older versions of Virtual Box) and video game installers turn off hypervisor on boot. To turn it back on:

1. Open an administrative console prompt.
2. Run `bcdedit /set hypervisorlaunchtype auto`.
3. Restart Windows.

You can also refer to the [Microsoft TechNet article](https://social.technet.microsoft.com/Forums/en-US/ee5b1d6b-09e2-49f3-a52c-820aafc316f9/hyperv-doesnt-work-after-upgrade-to-windows-10-1809?forum=win10itprovirt) on Code flow guard (CFG) settings.

##### [Turn on nested virtualization](#turn-on-nested-virtualization)

If you are using Hyper-V and you get the following error message when running Docker Desktop in a VDI environment:

```console
The Virtual Machine Management Service failed to start the virtual machine 'DockerDesktopVM' because one of the Hyper-V components is not running
```

Try [enabling nested virtualization](https://docs.docker.com/desktop/setup/vm-vdi/#turn-on-nested-virtualization).

### [Docker Desktop with Windows Containers fails with "The media is write protected""](#docker-desktop-with-windows-containers-fails-with-the-media-is-write-protected)

#### [Error message](#error-message-5)

`FSCTL_EXTEND_VOLUME \\?\Volume{GUID}: The media is write protected`

#### [Cause](#cause-13)

If you're encountering failures when running Docker Desktop with Windows Containers, it might be due to a specific Windows configuration policy: FDVDenyWriteAccess.

This policy, when enabled, causes Windows to mount all fixed drives not encrypted by BitLocker-encrypted as read-only. This also affects virtual machine volumes and as a result, Docker Desktop may not be able to start or run containers correctly because it requires read-write access to these volumes.

FDVDenyWriteAccess is a Windows Group Policy setting that, when enabled, prevents write access to fixed data drives that are not protected by BitLocker. This is often used in security-conscious environments but can interfere with development tools like Docker. In the Windows registry it can be found at `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Policies\Microsoft\FVE\FDVDenyWriteAccess`.

#### [Solutions](#solutions-1)

Docker Desktop does not support running Windows Containers on systems where FDVDenyWriteAccess is enabled. This setting interferes with the ability of Docker to mount volumes correctly, which is critical for container functionality.

To use Docker Desktop with Windows Containers, ensure that FDVDenyWriteAccess is disabled. You can check and change this setting in the registry or through Group Policy Editor (`gpedit.msc`) under:

**Computer Configuration** > **Administrative Templates** > **Windows Components** > **BitLocker Drive Encryption** > **Fixed Data Drives** > **Deny write access to fixed drives not protected by BitLocker**

> Note
>
> Modifying Group Policy settings may require administrator privileges and should comply with your organization's IT policies. If the setting gets reset after some time this usually means that it was overridden by the centralized configuration of your IT department. Talk to them before making any changes.

### [`Docker Desktop Access Denied` error message when starting Docker Desktop](#docker-desktop-access-denied-error-message-when-starting-docker-desktop)

#### [Error message](#error-message-6)

When starting Docker Desktop, the following error appears:

```text
Docker Desktop - Access Denied
```

#### [Cause](#cause-14)

The user is not part of the `docker-users` group, which is required for permissions.

#### [Solution](#solution-13)

If your admin account is different to your user account, add it:

1. Run **Computer Management** as an administrator.
2. Navigate to **Local Users and Groups** > **Groups** > **docker-users**.
3. Right-click to add the user to the group.
4. Sign out and sign back in for the changes to take effect

----
url: https://docs.docker.com/build/policies/examples/
----

# Policy templates and examples

***

Table of contents

***

This page provides complete, working policy examples you can copy and adapt. The examples are organized into two sections: getting started policies for quick adoption, and production templates for comprehensive security.

If you're new to policies, start with the tutorials: [Introduction](https://docs.docker.com/build/policies/intro/), [Image validation](https://docs.docker.com/build/policies/validate-images/), and [Git validation](https://docs.docker.com/build/policies/validate-git/). Those pages teach individual techniques. This page shows complete policies combining those techniques.

## [How to use these examples](#how-to-use-these-examples)

1. Copy the policy code into a `Dockerfile.rego` file next to your Dockerfile
2. Customize any todo comments with your specific values
3. Test by running `docker build .` and verifying the policy works as expected
4. Refine based on your team's needs

### [Using examples with bake](#using-examples-with-bake)

These policies work with both `docker buildx build` and `docker buildx bake`. For bake, place the policy alongside your Dockerfile and it loads automatically. To use additional policies:

```hcl
target "default" {
  dockerfile = "Dockerfile"
  policy = ["extra.rego"]
}
```

See the [Usage guide](https://docs.docker.com/build/policies/usage/) for complete bake integration details.

## [Getting started](#getting-started)

These policies work immediately with minimal or no customization. Use them to adopt policies quickly and demonstrate value to your team.

### [Development-friendly baseline](#development-friendly-baseline)

A permissive policy that allows typical development workflows while blocking obvious security issues.

```rego
package docker

default allow := false

allow if input.local
allow if input.git

# Allow common public registries
allow if {
  input.image.host == "docker.io"  # Docker Hub
}

allow if {
  input.image.host == "ghcr.io"  # GitHub Container Registry
}

allow if {
  input.image.host == "dhi.io"  # Docker Hardened Images
}

# Require HTTPS for all downloads
allow if {
  input.http.schema == "https"
}

decision := {"allow": allow}
```

This policy allows local and Git contexts, images from Docker Hub, GitHub Container Registry, and [Docker Hardened Images](/dhi/), and `ADD` downloads over HTTPS. It blocks HTTP downloads and non-standard registries.

When to use: Starting point for teams new to policies. Provides basic security without disrupting development workflows.

### [Registry allowlist](#registry-allowlist)

Control which registries your builds can pull images from.

```rego
package docker

default allow := false

allow if input.local

# TODO: Add your internal registry hostname
allowed_registries := ["docker.io", "ghcr.io", "dhi.io", "registry.company.com"]

allow if {
  input.image.host in allowed_registries
}

# Allow mirrored DHI images from Docker Hub (DHI Enterprise users)
# TODO: Replace with your organization namespace
allow if {
  input.image.host == "docker.io"
  startswith(input.image.repo, "myorg/dhi-")
}

deny_msg contains msg if {
  not allow
  input.image
  msg := sprintf("registry %s is not in the allowlist", [input.image.host])
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

This policy restricts image pulls to approved registries. Customize and add your internal registry to the list. If you have a DHI Enterprise subscription and have mirrored Docker Hardened Images to Docker Hub, add a rule to allow images from your organization's namespace.

When to use: Enforce corporate policies about approved image sources. Prevents developers from using arbitrary public registries.

### [Pin base images to digests](#pin-base-images-to-digests)

Require digest references for reproducible builds.

```rego
package docker

default allow := false

allow if input.local

# Require digest references for all images
allow if {
  input.image.isCanonical
}

deny_msg contains msg if {
  not allow
  input.image
  msg := sprintf("image %s must use digest reference (e.g., @sha256:...)", [input.image.ref])
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

This policy requires images use digest references like `alpine@sha256:abc123...` instead of tags like `alpine:3.19`. Digests are immutable - the same digest always resolves to the same image content.

When to use: Ensure build reproducibility. Prevents builds from breaking when upstream tags are updated. Required for compliance in some environments.

### [Control external dependencies](#control-external-dependencies)

Pin specific versions of dependencies downloaded during builds.

```rego
package docker

default allow := false

allow if input.local

# Allow any image (add restrictions as needed)
allow if input.image

# TODO: Add your allowed Git repositories and tags
allowed_repos := {
  "https://github.com/moby/buildkit.git": ["v0.26.1", "v0.27.0"],
}
# Only allow Git input from allowed_repos
allow if {
  some repo, versions in allowed_repos
  input.git.remote == repo
  input.git.tagName in versions
}

# TODO: Add your allowed downloads
allow if {
  input.http.url == "https://example.com/app-v1.0.tar.gz"
}

decision := {"allow": allow}
```

This policy creates allowlists for external dependencies. Add your Git repositories with approved version tags, and URLs.

When to use: Control which external dependencies can be used in builds. Prevents builds from pulling arbitrary versions or unverified downloads.

## [Production templates](#production-templates)

These templates demonstrate comprehensive security patterns. They require customization but show best practices for production environments.

### [Image attestation and provenance](#image-attestation-and-provenance)

Require images have provenance attestations from trusted builders.

```rego
package docker

default allow := false

allow if input.local

# TODO: Add your repository names
allowed_repos := ["myorg/backend", "myorg/frontend", "myorg/worker"]

# Production images need full attestations
allow if {
  some repo in allowed_repos
  input.image.repo == repo
  input.image.hasProvenance
  some sig in input.image.signatures
  trusted_github_builder(sig, repo)
}

# Helper to validate GitHub Actions build from main branch
trusted_github_builder(sig, repo) if {
  sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
  sig.signer.issuer == "https://token.actions.githubusercontent.com"
  startswith(sig.signer.buildSignerURI, sprintf("https://github.com/myorg/%s/.github/workflows/", [repo]))
  sig.signer.sourceRepositoryRef == "refs/heads/main"
  sig.signer.runnerEnvironment == "github-hosted"
}

# Allow Docker Hardened Images with built-in attestations
allow if {
  input.image.host == "dhi.io"
  input.image.isCanonical
  input.image.hasProvenance
}

# Allow official base images with digests
allow if {
  input.image.repo == "alpine"
  input.image.host == "docker.io"
  input.image.isCanonical
}

decision := {"allow": allow}
```

This template validates that your application images have provenance attestations, and were built by GitHub Actions from your main branch. Docker Hardened Images are allowed when using digests since they include comprehensive attestations by default. Other base images must use digests.

Customize:

* Replace `allowed_repos` with your image names
* Update the organization name in `trusted_github_builder()`
* Add rules for other base images you use

When to use: Enforce supply chain security for production deployments. Ensures images are built by trusted CI/CD pipelines with auditable provenance.

### [Signed Git releases](#signed-git-releases)

Enforce signed tags from trusted maintainers for Git dependencies.

```rego
package docker

default allow := false

allow if input.local

allow if input.image

# TODO: Replace with your repository URL
is_buildkit if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}

is_version_tag if {
    is_buildkit
    regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}

# Version tags must be signed
allow if {
    is_version_tag
    input.git.tagName != ""
    verify_git_signature(input.git.tag, "maintainers.asc")
}

# Allow unsigned refs for development
allow if {
    is_buildkit
    not is_version_tag
}

decision := {"allow": allow}
```

This template requires production release tags to be signed by trusted maintainers. Development branches and commits can be unsigned.

Setup:

1. Export maintainer PGP public keys to `maintainers.asc`:
   ```console
   $ gpg --export --armor user1@example.com user2@example.com > maintainers.asc
   ```
2. Place `maintainers.asc` in the same directory as your policy file

Customize:

* Replace the repository URL in `is_buildkit`
* Update the maintainers in the PGP keyring file
* Adjust the version tag regex pattern if needed

When to use: Validate that production dependencies come from signed releases. Protects against compromised releases or unauthorized updates.

### [Multi-registry policy](#multi-registry-policy)

Apply different validation rules for internal and external registries.

```rego
package docker

default allow := false

allow if input.local

# TODO: Replace with your internal registry hostname
internal_registry := "registry.company.com"

# Internal registry: basic validation
allow if {
  input.image.host == internal_registry
}

# External registries: strict validation
allow if {
  input.image.host != internal_registry
  input.image.host != ""
  input.image.isCanonical
  input.image.hasProvenance
}

# Docker Hub: allowlist specific images
allow if {
  input.image.host == "docker.io"
  # TODO: Add your approved base images
  input.image.repo in ["alpine", "golang", "node"]
  input.image.isCanonical
}

# Docker Hardened Images: trusted by default with built-in attestations
allow if {
  input.image.host == "dhi.io"
  input.image.isCanonical
}

decision := {"allow": allow}
```

This template defines a trust boundary between internal and external image sources. Internal images require minimal validation, while external images need digests and provenance. Docker Hardened Images from `dhi.io` are treated as trusted since they include comprehensive attestations and security guarantees.

Customize:

* Set your internal registry hostname
* Add your approved Docker Hub base images
* Adjust validation requirements based on your security policies

When to use: Organizations with internal registries that need different rules for internal and external sources. Balances security with practical workflow needs.

### [Multi-environment policy](#multi-environment-policy)

Apply different rules based on the build target or stage. For example,

```rego
package docker

default allow := false

allow if input.local

# TODO: Define your environment detection logic
is_production if {
  input.env.target == "production"
}

is_development if {
  input.env.target == "development"
}

# Production: strict rules - only digest images with provenance
allow if {
  is_production
  input.image.isCanonical
  input.image.hasProvenance
}

# Development: permissive rules - any image
allow if {
  is_development
  input.image
}

# Staging inherits production rules (default target detection)
allow if {
  not is_production
  not is_development
  input.image.isCanonical
}

decision := {"allow": allow}
```

This template uses build targets to apply different validation levels. Production requires attestations and digests, development is permissive, and staging uses moderate rules.

Customize:

* Update environment detection logic (target names, build args, etc.)
* Adjust validation requirements for each environment
* Add more environments as needed

When to use: Teams with separate build configurations for different deployment stages. Allows flexibility in development while enforcing strict rules for production.

### [Complete dependency pinning](#complete-dependency-pinning)

Pin all external dependencies to specific versions across all input types.

```rego
package docker

default allow := false

allow if input.local

# TODO: Add your pinned images with exact digests
# Docker Hub images use docker.io as host
allowed_dockerhub := {
  "alpine": "sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412",
  "golang": "sha256:abc123...",
}

allow if {
  input.image.host == "docker.io"
  some repo, digest in allowed_dockerhub
  input.image.repo == repo
  input.image.checksum == digest
}

# TODO: Add your pinned DHI images
allowed_dhi := {
  "python": "sha256:def456...",
  "node": "sha256:ghi789...",
}

allow if {
  input.image.host == "dhi.io"
  some repo, digest in allowed_dhi
  input.image.repo == repo
  input.image.checksum == digest
}

# TODO: Add your pinned Git dependencies
allowed_git := {
  "https://github.com/moby/buildkit.git": {
    "tag": "v0.26.1",
    "commit": "abc123...",
  },
}

allow if {
  some url, version in allowed_git
  input.git.remote == url
  input.git.tagName == version.tag
  input.git.commitChecksum == version.commit
}

# TODO: Add your pinned HTTP downloads
allowed_downloads := {
  "https://releases.example.com/app-v1.0.tar.gz": "sha256:def456...",
}

allow if {
  some url, checksum in allowed_downloads
  input.http.url == url
  input.http.checksum == checksum
}

decision := {"allow": allow}
```

This template pins every external dependency to exact versions with cryptographic verification. Images use digests, Git repos use commit SHAs, and downloads use checksums.

Customize:

* Add all your dependencies with exact versions/checksums
* Maintain this file when updating dependencies
* Consider automating updates through CI/CD

When to use: Maximum reproducibility and security. Ensures builds always use exact versions of all dependencies. Required for high-security or regulated environments.

### [Manual signature verification](#manual-signature-verification)

Verify image signatures by inspecting signature metadata fields.

```rego
package docker

default allow := false

allow if input.local

# Require valid GitHub Actions signatures
allow if {
    input.image
    input.image.hasProvenance
    some sig in input.image.signatures
    valid_github_signature(sig)
}

# Helper function to validate GitHub Actions signature
valid_github_signature(sig) if {
    # Sigstore keyless signing
    sig.signer.certificateIssuer == "CN=sigstore-intermediate,O=sigstore.dev"
    sig.signer.issuer == "https://token.actions.githubusercontent.com"

    # TODO: Replace with your organization
    startswith(sig.signer.buildSignerURI, "https://github.com/myorg/.github/workflows/")
    startswith(sig.signer.sourceRepositoryURI, "https://github.com/myorg/")

    # Verify GitHub hosted runner
    sig.signer.runnerEnvironment == "github-hosted"

    # Require timestamp
    count(sig.timestamps) > 0
}

decision := {"allow": allow}
```

This policy validates that images were built by GitHub Actions using Sigstore keyless signing.

Customize:

* Replace `myorg` with your GitHub organization
* Adjust workflow path restrictions
* Add additional signature field checks as needed

When to use: Enforce that images are built by CI/CD with verifiable signatures, not manually pushed by developers.

## [Next steps](#next-steps)

* Write unit tests for your policies: [Test build policies](https://docs.docker.com/build/policies/testing/)
* Review [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for signature verification and attestation checking
* Check the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available fields you can validate
* Read the tutorials for detailed explanations: [Introduction](https://docs.docker.com/build/policies/intro/), [Image validation](https://docs.docker.com/build/policies/validate-images/), [Git validation](https://docs.docker.com/build/policies/validate-git/)

----
url: https://docs.docker.com/dhi/core-concepts/vex/
----

# Vulnerability Exploitability eXchange (VEX)

***

Table of contents

***

## [What is VEX?](#what-is-vex)

Vulnerability Exploitability eXchange (VEX) is a specification for documenting the exploitability status of vulnerabilities within software components. VEX is primarily defined through industry standards such as CSAF (OASIS) and CycloneDX VEX, with the U.S. Cybersecurity and Infrastructure Security Agency (CISA) encouraging its adoption. VEX complements CVE (Common Vulnerabilities and Exposures) identifiers by adding producer-asserted status information, indicating whether a vulnerability is exploitable in the product as shipped. This helps organizations prioritize remediation efforts by identifying vulnerabilities that do not affect their specific product configurations.

For how VEX affects vulnerability counts and scanner selection, see [Scanner integrations](https://docs.docker.com/dhi/explore/scanner-integrations/). To scan a DHI with VEX support, see [Scan Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/).

## [VEX status reference](#vex-status-reference)

Each VEX statement includes a `status` field that records Docker's exploitability assessment for a given CVE and image. DHI uses three of the four OpenVEX status values.

| Status                | Meaning                                                                                                       |
| --------------------- | ------------------------------------------------------------------------------------------------------------- |
| `not_affected`        | The CVE was reported against a package in the image, but Docker has assessed it is not exploitable as shipped |
| `under_investigation` | Docker is aware of the CVE and is actively evaluating whether it affects the image                            |
| `affected`            | Docker has confirmed the CVE is exploitable in the image and a fix is not yet available                       |

You can view the VEX statements for any DHI using Docker Scout. See [Scan Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/).

### [`not_affected` justification codes](#not_affected-justification-codes)

`not_affected` statements include a machine-readable `justification` field explaining why the vulnerability does not apply:

| Justification                                       | Meaning                                                                                                    |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `component_not_present`                             | The vulnerable component is not present in this image; the CVE matched by name against a different package |
| `vulnerable_code_not_present`                       | The vulnerable code path was not compiled into this build                                                  |
| `vulnerable_code_not_in_execute_path`               | The vulnerable code exists in the package but is not called in this image's runtime configuration          |
| `vulnerable_code_cannot_be_controlled_by_adversary` | The vulnerable code exists but an attacker cannot trigger it in this configuration                         |
| `inline_mitigations_already_exist`                  | Docker has applied a backport or patch that addresses the CVE                                              |

### [Why DHI does not use `fixed`](#why-dhi-does-not-use-fixed)

DHI does not use `fixed`. VEX-enabled scanners may not handle `fixed` consistently, so when Docker backports an upstream patch where the version number alone would not reflect the fix, it uses `not_affected` with `inline_mitigations_already_exist` justification instead.

----
url: https://docs.docker.com/reference/samples/flask/
----

# Flask samples

| Name                                                                                               | Description                                                                 |
| -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| [NGINX / Flask / MongoDB](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mongo) | A sample Python/Flask application with Nginx proxy and a Mongo database.    |
| [NGINX / Flask / MySQL](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mysql)   | A sample Python/Flask application with an Nginx proxy and a MySQL database. |
| [NGINX / WSGI / Flask](https://github.com/docker/awesome-compose/tree/master/nginx-wsgi-flask)     | A sample Nginx reverse proxy with a Flask backend using WSGI.               |
| [Python / Flask / Redis](https://github.com/docker/awesome-compose/tree/master/flask-redis)        | A sample Python/Flask and a Redis database.                                 |
| [Flask](https://github.com/docker/awesome-compose/tree/master/flask)                               | A sample Flask application.                                                 |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/reference/api/engine/version/v1.53.yaml
----

basePath: "/v1.53"
info:
 title: "Docker Engine API"
 version: "1.53"

 Identity:
 description: \|-
 Identity holds information about the identity and origin of the image.
 This is trusted information verified by the daemon and cannot be modified
 by tagging an image to a different name.

----
url: https://docs.docker.com/get-started/workshop/08_using_compose/
----

# Use Docker Compose

***

Table of contents

***

[Docker Compose](https://docs.docker.com/compose/) is a tool that helps you define and share multi-container applications. With Compose, you can create a YAML file to define the services and with a single command, you can spin everything up or tear it all down.

The big advantage of using Compose is you can define your application stack in a file, keep it at the root of your project repository (it's now version controlled), and easily enable someone else to contribute to your project. Someone would only need to clone your repository and start the app using Compose. In fact, you might see quite a few projects on GitHub/GitLab doing exactly this now.

## [Create the Compose file](#create-the-compose-file)

In the `getting-started-app` directory, create a file named `compose.yaml`.

```text
├── getting-started-app/
│ ├── Dockerfile
│ ├── compose.yaml
│ ├── node_modules/
│ ├── package.json
│ ├── package-lock.json
│ ├── spec/
│ └── src/
```

## [Define the app service](#define-the-app-service)

In [part 6](https://docs.docker.com/get-started/workshop/07_multi_container/), you used the following command to start the application service.

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

You'll now define this service in the `compose.yaml` file.

1. Open `compose.yaml` in a text or code editor, and start by defining the name and image of the first service (or container) you want to run as part of your application. The name will automatically become a network alias, which will be useful when defining your MySQL service.

   ```yaml
   services:
     app:
       image: node:24-alpine
   ```

2. Typically, you will see `command` close to the `image` definition, although there is no requirement on ordering. Add the `command` to your `compose.yaml` file.

   ```yaml
   services:
     app:
       image: node:24-alpine
       command: sh -c "npm install && npm run dev"
   ```

3. Now migrate the `-p 127.0.0.1:3000:3000` part of the command by defining the `ports` for the service.

   ```yaml
   services:
     app:
       image: node:24-alpine
       command: sh -c "npm install && npm run dev"
       ports:
         - 127.0.0.1:3000:3000
   ```

4. Next, migrate both the working directory (`-w /app`) and the volume mapping (`-v ".:/app"`) by using the `working_dir` and `volumes` definitions.

   One advantage of Docker Compose volume definitions is you can use relative paths from the current directory.

   ```yaml
   services:
     app:
       image: node:24-alpine
       command: sh -c "npm install && npm run dev"
       ports:
         - 127.0.0.1:3000:3000
       working_dir: /app
       volumes:
         - ./:/app
   ```

5. Finally, you need to migrate the environment variable definitions using the `environment` key.

   ```yaml
   services:
     app:
       image: node:24-alpine
       command: sh -c "npm install && npm run dev"
       ports:
         - 127.0.0.1:3000:3000
       working_dir: /app
       volumes:
         - ./:/app
       environment:
         MYSQL_HOST: mysql
         MYSQL_USER: root
         MYSQL_PASSWORD: secret
         MYSQL_DB: todos
   ```

### [Define the MySQL service](#define-the-mysql-service)

Now, it's time to define the MySQL service. The command that you used for that container was the following:

```console
$ docker run -d \
  --network todo-app --network-alias mysql \
  -v todo-mysql-data:/var/lib/mysql \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=todos \
  mysql:8.0
```

1. First define the new service and name it `mysql` so it automatically gets the network alias. Also specify the image to use as well.

   ```yaml

   services:
     app:
       # The app service definition
     mysql:
       image: mysql:8.0
   ```

2. Next, define the volume mapping. When you ran the container with `docker run`, Docker created the named volume automatically. However, that doesn't happen when running with Compose. You need to define the volume in the top-level `volumes:` section and then specify the mountpoint in the service config. By simply providing only the volume name, the default options are used.

   ```yaml
   services:
     app:
       # The app service definition
     mysql:
       image: mysql:8.0
       volumes:
         - todo-mysql-data:/var/lib/mysql

   volumes:
     todo-mysql-data:
   ```

3. Finally, you need to specify the environment variables.

   ```yaml
   services:
     app:
       # The app service definition
     mysql:
       image: mysql:8.0
       volumes:
         - todo-mysql-data:/var/lib/mysql
       environment:
         MYSQL_ROOT_PASSWORD: secret
         MYSQL_DATABASE: todos

   volumes:
     todo-mysql-data:
   ```

At this point, your complete `compose.yaml` should look like this:

```yaml
services:
  app:
    image: node:24-alpine
    command: sh -c "npm install && npm run dev"
    ports:
      - 127.0.0.1:3000:3000
    working_dir: /app
    volumes:
      - ./:/app
    environment:
      MYSQL_HOST: mysql
      MYSQL_USER: root
      MYSQL_PASSWORD: secret
      MYSQL_DB: todos

  mysql:
    image: mysql:8.0
    volumes:
      - todo-mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: secret
      MYSQL_DATABASE: todos

volumes:
  todo-mysql-data:
```

## [Run the application stack](#run-the-application-stack)

Now that you have your `compose.yaml` file, you can start your application.

1. Make sure no other copies of the containers are running first. Use `docker ps` to list the containers and `docker rm -f <ids>` to remove them.

2. Start up the application stack using the `docker compose up` command. Add the `-d` flag to run everything in the background.

   ```console
   $ docker compose up -d
   ```

   When you run the previous command, you should see output like the following:

   ```plaintext
   Creating network "app_default" with the default driver
   Creating volume "app_todo-mysql-data" with default driver
   Creating app_app_1   ... done
   Creating app_mysql_1 ... done
   ```

   You'll notice that Docker Compose created the volume as well as a network. By default, Docker Compose automatically creates a network specifically for the application stack (which is why you didn't define one in the Compose file).

3. Look at the logs using the `docker compose logs -f` command. You'll see the logs from each of the services interleaved into a single stream. This is incredibly useful when you want to watch for timing-related issues. The `-f` flag follows the log, so will give you live output as it's generated.

   If you have run the command already, you'll see output that looks like this:

   ```plaintext
   mysql_1  | 2019-10-03T03:07:16.083639Z 0 [Note] mysqld: ready for connections.
   mysql_1  | Version: '8.0.31'  socket: '/var/run/mysqld/mysqld.sock'  port: 3306  MySQL Community Server (GPL)
   app_1    | Connected to mysql db at host mysql
   app_1    | Listening on port 3000
   ```

   The service name is displayed at the beginning of the line (often colored) to help distinguish messages. If you want to view the logs for a specific service, you can add the service name to the end of the logs command (for example, `docker compose logs -f app`).

4. At this point, you should be able to open your app in your browser on <http://localhost:3000> and see it running.

## [See the app stack in Docker Desktop Dashboard](#see-the-app-stack-in-docker-desktop-dashboard)

If you look at the Docker Desktop Dashboard, you'll see that there is a group named **getting-started-app**. This is the project name from Docker Compose and used to group the containers together. By default, the project name is simply the name of the directory that the `compose.yaml` was located in.

If you expand the stack, you'll see the two containers you defined in the Compose file. The names are also a little more descriptive, as they follow the pattern of `<service-name>-<replica-number>`. So, it's very easy to quickly see what container is your app and which container is the mysql database.

## [Tear it all down](#tear-it-all-down)

When you're ready to tear it all down, simply run `docker compose down` or hit the trash can on the Docker Desktop Dashboard for the entire app. The containers will stop and the network will be removed.

> Warning
>
> By default, named volumes in your compose file are not removed when you run `docker compose down`. If you want to remove the volumes, you need to add the `--volumes` flag.
>
> The Docker Desktop Dashboard does not remove volumes when you delete the app stack.

## [Summary](#summary)

In this section, you learned about Docker Compose and how it helps you simplify the way you define and share multi-service applications.

Related information:

* [Compose overview](https://docs.docker.com/compose/)
* [Compose file reference](https://docs.docker.com/reference/compose-file/)
* [Compose CLI reference](/reference/cli/docker/compose/)

## [Next steps](#next-steps)

Next, you'll learn about a few best practices you can use to improve your Dockerfile.

[Image-building best practices](https://docs.docker.com/get-started/workshop/09_image_best/)

----
url: https://docs.docker.com/reference/cli/docker/compose/run/
----

# docker compose run

***

| Description | Run a one-off command on a service                         |
| ----------- | ---------------------------------------------------------- |
| Usage       | `docker compose run [OPTIONS] SERVICE [COMMAND] [ARGS...]` |

## [Description](#description)

Runs a one-time command against a service.

The following command starts the `web` service and runs `bash` as its command:

```console
$ docker compose run web bash
```

Commands you use with run start in new containers with configuration defined by that of the service, including volumes, links, and other details. However, there are two important differences:

First, the command passed by `run` overrides the command defined in the service configuration. For example, if the `web` service configuration is started with `bash`, then `docker compose run web python app.py` overrides it with `python app.py`.

The second difference is that the `docker compose run` command does not create any of the ports specified in the service configuration. This prevents port collisions with already-open ports. If you do want the service’s ports to be created and mapped to the host, specify the `--service-ports`

```console
$ docker compose run --service-ports web python manage.py shell
```

Alternatively, manual port mapping can be specified with the `--publish` or `-p` options, just as when using docker run:

```console
$ docker compose run --publish 8080:80 -p 2022:22 -p 127.0.0.1:2021:21 web python manage.py shell
```

If you start a service configured with links, the run command first checks to see if the linked service is running and starts the service if it is stopped. Once all the linked services are running, the run executes the command you passed it. For example, you could run:

```console
$ docker compose run db psql -h db -U docker
```

This opens an interactive PostgreSQL shell for the linked `db` container.

If you do not want the run command to start linked containers, use the `--no-deps` flag:

```console
$ docker compose run --no-deps web python manage.py shell
```

If you want to remove the container after running while overriding the container’s restart policy, use the `--rm` flag:

```console
$ docker compose run --rm web python manage.py db upgrade
```

This runs a database upgrade script, and removes the container when finished running, even if a restart policy is specified in the service configuration.

## [Options](#options)

| Option                | Default  | Description                                                                       |
| --------------------- | -------- | --------------------------------------------------------------------------------- |
| `--build`             |          | Build image before starting container                                             |
| `--cap-add`           |          | Add Linux capabilities                                                            |
| `--cap-drop`          |          | Drop Linux capabilities                                                           |
| `-d, --detach`        |          | Run container in background and print container ID                                |
| `--entrypoint`        |          | Override the entrypoint of the image                                              |
| `-e, --env`           |          | Set environment variables                                                         |
| `--env-from-file`     |          | Set environment variables from file                                               |
| `-i, --interactive`   | `true`   | Keep STDIN open even if not attached                                              |
| `-l, --label`         |          | Add or override a label                                                           |
| `--name`              |          | Assign a name to the container                                                    |
| `-T, --no-TTY`        | `true`   | Disable pseudo-TTY allocation (default: auto-detected)                            |
| `--no-deps`           |          | Don't start linked services                                                       |
| `-p, --publish`       |          | Publish a container's port(s) to the host                                         |
| `--pull`              | `policy` | Pull image before running ("always"\|"missing"\|"never")                          |
| `-q, --quiet`         |          | Don't print anything to STDOUT                                                    |
| `--quiet-build`       |          | Suppress progress output from the build process                                   |
| `--quiet-pull`        |          | Pull without printing progress information                                        |
| `--remove-orphans`    |          | Remove containers for services not defined in the Compose file                    |
| `--rm`                |          | Automatically remove the container when it exits                                  |
| `-P, --service-ports` |          | Run command with all service's ports enabled and mapped to the host               |
| `--use-aliases`       |          | Use the service's network useAliases in the network(s) the container connects to  |
| `-u, --user`          |          | Run as specified username or uid                                                  |
| `-v, --volume`        |          | Bind mount a volume                                                               |
| `-w, --workdir`       |          | Working directory inside the container                                            |

----
url: https://docs.docker.com/engine/logging/drivers/etwlogs/
----

# ETW logging driver

***

Table of contents

***

The Event Tracing for Windows (ETW) logging driver forwards container logs as ETW events. ETW stands for Event Tracing in Windows, and is the common framework for tracing applications in Windows. Each ETW event contains a message with both the log and its context information. A client can then create an ETW listener to listen to these events.

The ETW provider that this logging driver registers with Windows, has the GUID identifier of: `{a3693192-9ed6-46d2-a981-f8226c8363bd}`. A client creates an ETW listener and registers to listen to events from the logging driver's provider. It doesn't matter the order in which the provider and listener are created. A client can create their ETW listener and start listening for events from the provider, before the provider has been registered with the system.

## [Usage](#usage)

Here is an example of how to listen to these events using the logman utility program included in most installations of Windows:

1. `logman start -ets DockerContainerLogs -p "{a3693192-9ed6-46d2-a981-f8226c8363bd}" 0x0 -o trace.etl`
2. Run your container(s) with the etwlogs driver, by adding `--log-driver=etwlogs` to the Docker run command, and generate log messages.
3. `logman stop -ets DockerContainerLogs`
4. This generates an etl file that contains the events. One way to convert this file into human-readable form is to run: `tracerpt -y trace.etl`.

Each ETW event contains a structured message string in this format:

```text
container_name: %s, image_name: %s, container_id: %s, image_id: %s, source: [stdout | stderr], log: %s
```

Details on each item in the message can be found below:

| Field            | Description                                    |
| ---------------- | ---------------------------------------------- |
| `container_name` | The container name at the time it was started. |
| `image_name`     | The name of the container's image.             |
| `container_id`   | The full 64-character container ID.            |
| `image_id`       | The full ID of the container's image.          |
| `source`         | `stdout` or `stderr`.                          |
| `log`            | The container log message.                     |

Here is an example event message (output formatted for readability):

```yaml
container_name: backstabbing_spence,
image_name: windowsservercore,
container_id: f14bb55aa862d7596b03a33251c1be7dbbec8056bbdead1da8ec5ecebbe29731,
image_id: sha256:2f9e19bd998d3565b4f345ac9aaf6e3fc555406239a4fb1b1ba879673713824b,
source: stdout,
log: Hello world!
```

A client can parse this message string to get both the log message, as well as its context information. The timestamp is also available within the ETW event.

> Note
>
> This ETW provider only emits a message string, and not a specially structured ETW event. Therefore, you don't have to register a manifest file with the system to read and interpret its ETW events.

----
url: https://docs.docker.com/build/building/cdi/
----

# Container Device Interface (CDI)

***

Table of contents

***

The [Container Device Interface (CDI)](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md) is a specification designed to standardize how devices (like GPUs, FPGAs, and other hardware accelerators) are exposed to and used by containers. The aim is to provide a more consistent and secure mechanism for using hardware devices in containerized environments, addressing the challenges associated with device-specific setups and configurations.

In addition to enabling the container to interact with the device node, CDI also lets you specify additional configuration for the device, such as environment variables, host mounts (such as shared objects), and executable hooks.

## [Getting started](#getting-started)

To get started with CDI, you need to have a compatible environment set up. This includes having Docker v27+ installed with [CDI configured](https://docs.docker.com/reference/cli/dockerd/#configure-cdi-devices) and Buildx v0.22+.

You also need to create the [device specifications using JSON or YAML files](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md#cdi-json-specification) in one of the following locations:

* `/etc/cdi`
* `/var/run/cdi`
* `/etc/buildkit/cdi`

> Note
>
> Location can be changed by setting the `specDirs` option in the `cdi` section of the [`buildkitd.toml` configuration file](https://docs.docker.com/build/buildkit/configure/) if you are using BuildKit directly. If you're building using the Docker Daemon with the `docker` driver, see [Configure CDI devices](https://docs.docker.com/reference/cli/dockerd/#configure-cdi-devices) documentation.

> Note
>
> If you are creating a container builder on WSL, you need to ensure that [Docker Desktop](https://docs.docker.com/desktop/) is installed and [WSL 2 GPU Paravirtualization](https://docs.docker.com/desktop/features/gpu/#prerequisites) is enabled. Buildx v0.27+ is also required to mount the WSL libraries in the container.

## [Building with a simple CDI specification](#building-with-a-simple-cdi-specification)

Let's start with a simple CDI specification that injects an environment variable into the build environment and write it to `/etc/cdi/foo.yaml`:

/etc/cdi/foo.yaml

```yaml
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
- name: foo
  containerEdits:
    env:
    - FOO=injected
```

Inspect the `default` builder to verify that `vendor1.com/device` is detected as a device:

```console
$ docker buildx inspect
Name:   default
Driver: docker

Nodes:
Name:             default
Endpoint:         default
Status:           running
BuildKit version: v0.23.2
Platforms:        linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/amd64/v4, linux/386
Labels:
 org.mobyproject.buildkit.worker.moby.host-gateway-ip: 172.17.0.1
Devices:
 Name:                  vendor1.com/device=foo
 Automatically allowed: false
GC Policy rule#0:
 All:            false
 Filters:        type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration:  48h0m0s
 Max Used Space: 658.9MiB
GC Policy rule#1:
 All:            false
 Keep Duration:  1440h0m0s
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
GC Policy rule#2:
 All:            false
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
GC Policy rule#3:
 All:            true
 Reserved Space: 4.657GiB
 Max Used Space: 953.7MiB
 Min Free Space: 2.794GiB
```

Now let's create a Dockerfile to use this device:

```dockerfile
# syntax=docker/dockerfile:1-labs
FROM busybox
RUN --device=vendor1.com/device \
  env | grep ^FOO=
```

Here we use the [`RUN --device` command](https://docs.docker.com/reference/dockerfile/#run---device) and set `vendor1.com/device` which requests the first device available in the specification. In this case it uses `foo`, which is the first device in `/etc/cdi/foo.yaml`.

> Note
>
> [`RUN --device` command](https://docs.docker.com/reference/dockerfile/#run---device) is only featured in [`labs` channel](https://docs.docker.com/build/buildkit/frontend/#labs-channel) since [Dockerfile frontend v1.14.0-labs](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.14.0-labs) and not yet available in stable syntax.

Now let's build this Dockerfile:

```console
$ docker buildx build .
[+] Building 0.4s (5/5) FINISHED                                                                                                        docker:default
 => [internal] load build definition from Dockerfile                                                                                    0.0s 
 => => transferring dockerfile: 155B                                                                                                    0.0s
 => resolve image config for docker-image://docker/dockerfile:1-labs                                                                    0.1s 
 => CACHED docker-image://docker/dockerfile:1-labs@sha256:9187104f31e3a002a8a6a3209ea1f937fb7486c093cbbde1e14b0fa0d7e4f1b5              0.0s
 => [internal] load metadata for docker.io/library/busybox:latest                                                                       0.1s 
 => [internal] load .dockerignore                                                                                                       0.0s
 => => transferring context: 2B                                                                                                         0.0s 
ERROR: failed to build: failed to solve: failed to load LLB: device vendor1.com/device=foo is requested by the build but not allowed
```

It fails because the device `vendor1.com/device=foo` is not automatically allowed by the build as shown in the `buildx inspect` output above:

```text
Devices:
 Name:                  vendor1.com/device=foo
 Automatically allowed: false
```

To allow the device, you can use the [`--allow` flag](/reference/cli/docker/buildx/build/#allow) with the `docker buildx build` command:

```console
$ docker buildx build --allow device .
```

Or you can set the `org.mobyproject.buildkit.device.autoallow` annotation in the CDI specification to automatically allow the device for all builds:

/etc/cdi/foo.yaml

```yaml
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
- name: foo
  containerEdits:
    env:
    - FOO=injected
annotations:
  org.mobyproject.buildkit.device.autoallow: true
```

Now running the build again with the `--allow device` flag:

```console
$ docker buildx build --progress=plain --allow device .
#0 building with "default" instance using docker driver

#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 159B done
#1 DONE 0.0s

#2 resolve image config for docker-image://docker/dockerfile:1-labs
#2 DONE 0.1s

#3 docker-image://docker/dockerfile:1-labs@sha256:9187104f31e3a002a8a6a3209ea1f937fb7486c093cbbde1e14b0fa0d7e4f1b5
#3 CACHED

#4 [internal] load metadata for docker.io/library/busybox:latest
#4 DONE 0.1s

#5 [internal] load .dockerignore
#5 transferring context: 2B done
#5 DONE 0.0s

#6 [1/2] FROM docker.io/library/busybox:latest@sha256:f85340bf132ae937d2c2a763b8335c9bab35d6e8293f70f606b9c6178d84f42b
#6 CACHED

#7 [2/2] RUN --device=vendor1.com/device   env | grep ^FOO=
#7 0.155 FOO=injected
#7 DONE 0.2s
```

The build is successful and the output shows that the `FOO` environment variable was injected into the build environment as specified in the CDI specification.

## [Set up a container builder with GPU support](#set-up-a-container-builder-with-gpu-support)

In this section, we will show you how to set up a [container builder](https://docs.docker.com/build/builders/drivers/docker-container/) using NVIDIA GPUs. Since Buildx v0.22, when creating a new container builder, a GPU request is automatically added to the container builder if the host has GPU drivers installed in the kernel. This is similar to using [`--gpus=all` with the `docker run`](/reference/cli/docker/container/run/#gpus) command.

Now let's create a container builder named `gpubuilder` using Buildx:

```console
$ docker buildx create --name gpubuilder --driver-opt "image=moby/buildkit:buildx-stable-1-gpu" --bootstrap
#1 [internal] booting buildkit
#1 pulling image moby/buildkit:buildx-stable-1-gpu
#1 pulling image moby/buildkit:buildx-stable-1-gpu 1.0s done
#1 creating container buildx_buildkit_gpubuilder0
#1 creating container buildx_buildkit_gpubuilder0 8.8s done
#1 DONE 9.8s
gpubuilder
```

> Note
>
> We made a specially crafted BuildKit image because the current BuildKit release image is based on Alpine that doesn't support NVIDIA drivers. The following image is based on Ubuntu and installs the NVIDIA client libraries and generates the CDI specification for your GPU in the container builder if a device is requested during a build.

Let's inspect this builder:

```console
$ docker buildx inspect gpubuilder
Name:          gpubuilder
Driver:        docker-container
Last Activity: 2025-07-10 08:18:09 +0000 UTC

Nodes:
Name:                  gpubuilder0
Endpoint:              unix:///var/run/docker.sock
Driver Options:        image="moby/buildkit:buildx-stable-1-gpu"
Status:                running
BuildKit daemon flags: --allow-insecure-entitlement=network.host
BuildKit version:      v0.26.2
Platforms:             linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/arm64, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/arm/v7, linux/arm/v6
Labels:
 org.mobyproject.buildkit.worker.executor:         oci
 org.mobyproject.buildkit.worker.hostname:         d6aa9cbe8462
 org.mobyproject.buildkit.worker.network:          host
 org.mobyproject.buildkit.worker.oci.process-mode: sandbox
 org.mobyproject.buildkit.worker.selinux.enabled:  false
 org.mobyproject.buildkit.worker.snapshotter:      overlayfs
Devices:
 Name:      nvidia.com/gpu
 On-Demand: true
GC Policy rule#0:
 All:            false
 Filters:        type==source.local,type==exec.cachemount,type==source.git.checkout
 Keep Duration:  48h0m0s
 Max Used Space: 488.3MiB
GC Policy rule#1:
 All:            false
 Keep Duration:  1440h0m0s
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
GC Policy rule#2:
 All:            false
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
GC Policy rule#3:
 All:            true
 Reserved Space: 9.313GiB
 Max Used Space: 93.13GiB
 Min Free Space: 188.1GiB
```

We can see `nvidia.com/gpu` vendor is detected as a device in the builder which means that drivers were detected.

Optionally you can check if NVIDIA GPU devices are available in the container using `nvidia-smi`:

```console
$ docker exec -it buildx_buildkit_gpubuilder0 nvidia-smi -L
GPU 0: Tesla T4 (UUID: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84)
```

## [Building with GPU support](#building-with-gpu-support)

Let's create a simple Dockerfile that will use the GPU device:

```dockerfile
# syntax=docker/dockerfile:1-labs
FROM ubuntu
RUN --device=nvidia.com/gpu nvidia-smi -L
```

Now run the build using the `gpubuilder` builder we created earlier:

```console
$ docker buildx --builder gpubuilder build --progress=plain .
#0 building with "gpubuilder" instance using docker-container driver
...

#7 preparing device nvidia.com/gpu
#7 0.000 > apt-get update
...
#7 4.872 > apt-get install -y gpg
...
#7 10.16 Downloading NVIDIA GPG key
#7 10.21 > apt-get update
...
#7 12.15 > apt-get install -y --no-install-recommends nvidia-container-toolkit-base
...
#7 17.80 time="2025-04-15T08:58:16Z" level=info msg="Generated CDI spec with version 0.8.0"
#7 DONE 17.8s

#8 [2/2] RUN --device=nvidia.com/gpu nvidia-smi -L
#8 0.527 GPU 0: Tesla T4 (UUID: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84)
#8 DONE 1.6s
```

As you might have noticed, the step `#7` is preparing the `nvidia.com/gpu` device by installing client libraries and the toolkit to generate the CDI specifications for the GPU.

The `nvidia-smi -L` command is then executed in the container using the GPU device. The output shows the GPU UUID.

You can check the generated CDI specification within the container builder with the following command:

```console
$ docker exec -it buildx_buildkit_gpubuilder0 cat /etc/cdi/nvidia.yaml
```

For the EC2 instance [`g4dn.xlarge`](https://aws.amazon.com/ec2/instance-types/g4/) used here, it looks like this:

```yaml
cdiVersion: 0.6.0
containerEdits:
  deviceNodes:
  - path: /dev/nvidia-modeset
  - path: /dev/nvidia-uvm
  - path: /dev/nvidia-uvm-tools
  - path: /dev/nvidiactl
  env:
  - NVIDIA_VISIBLE_DEVICES=void
  hooks:
  - args:
    - nvidia-cdi-hook
    - create-symlinks
    - --link
    - ../libnvidia-allocator.so.1::/usr/lib/x86_64-linux-gnu/gbm/nvidia-drm_gbm.so
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - create-symlinks
    - --link
    - libcuda.so.1::/usr/lib/x86_64-linux-gnu/libcuda.so
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - enable-cuda-compat
    - --host-driver-version=570.133.20
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  - args:
    - nvidia-cdi-hook
    - update-ldcache
    - --folder
    - /usr/lib/x86_64-linux-gnu
    hookName: createContainer
    path: /usr/bin/nvidia-cdi-hook
  mounts:
  - containerPath: /run/nvidia-persistenced/socket
    hostPath: /run/nvidia-persistenced/socket
    options:
    - ro
    - nosuid
    - nodev
    - bind
    - noexec
  - containerPath: /usr/bin/nvidia-cuda-mps-control
    hostPath: /usr/bin/nvidia-cuda-mps-control
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-cuda-mps-server
    hostPath: /usr/bin/nvidia-cuda-mps-server
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-debugdump
    hostPath: /usr/bin/nvidia-debugdump
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-persistenced
    hostPath: /usr/bin/nvidia-persistenced
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/bin/nvidia-smi
    hostPath: /usr/bin/nvidia-smi
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libcuda.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libcuda.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libcudadebugger.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libcudadebugger.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-allocator.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-cfg.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-cfg.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-gpucomp.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-gpucomp.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-ml.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-nscq.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-nscq.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-nvvm.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-nvvm.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-opencl.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11-openssl3.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11-openssl3.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-pkcs11.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.570.133.20
    hostPath: /usr/lib/x86_64-linux-gnu/libnvidia-ptxjitcompiler.so.570.133.20
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /lib/firmware/nvidia/570.133.20/gsp_ga10x.bin
    hostPath: /lib/firmware/nvidia/570.133.20/gsp_ga10x.bin
    options:
    - ro
    - nosuid
    - nodev
    - bind
  - containerPath: /lib/firmware/nvidia/570.133.20/gsp_tu10x.bin
    hostPath: /lib/firmware/nvidia/570.133.20/gsp_tu10x.bin
    options:
    - ro
    - nosuid
    - nodev
    - bind
devices:
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: "0"
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: GPU-6cf00fa7-59ac-16f2-3e83-d24ccdc56f84
- containerEdits:
    deviceNodes:
    - path: /dev/nvidia0
  name: all
kind: nvidia.com/gpu
```

Congrats on your first build using a GPU device with BuildKit and CDI.

----
url: https://docs.docker.com/build/builders/drivers/remote/
----

# Remote driver

***

Table of contents

***

The Buildx remote driver allows for more complex custom build workloads, allowing you to connect to externally managed BuildKit instances. This is useful for scenarios that require manual management of the BuildKit daemon, or where a BuildKit daemon is exposed from another source.

## [Synopsis](#synopsis)

```console
$ docker buildx create \
  --name remote \
  --driver remote \
  tcp://localhost:1234
```

The following table describes the available driver-specific options that you can pass to `--driver-opt`:

| Parameter      | Type    | Default            | Description                                                            |
| -------------- | ------- | ------------------ | ---------------------------------------------------------------------- |
| `key`          | String  |                    | Sets the TLS client key.                                               |
| `cert`         | String  |                    | Absolute path to the TLS client certificate to present to `buildkitd`. |
| `cacert`       | String  |                    | Absolute path to the TLS certificate authority used for validation.    |
| `servername`   | String  | Endpoint hostname. | TLS server name used in requests.                                      |
| `default-load` | Boolean | `false`            | Automatically load images to the Docker Engine image store.            |

## [Example: Remote BuildKit over Unix sockets](#example-remote-buildkit-over-unix-sockets)

This guide shows you how to create a setup with a BuildKit daemon listening on a Unix socket, and have Buildx connect through it.

1. Ensure that [BuildKit](https://github.com/moby/buildkit) is installed.

   For example, you can launch an instance of buildkitd with:

   ```console
   $ sudo ./buildkitd --group $(id -gn) --addr unix://$HOME/buildkitd.sock
   ```

   Alternatively, refer to the [Rootless Buildkit documentation](https://github.com/moby/buildkit/blob/master/docs/rootless.md) for running buildkitd in rootless mode, or [the BuildKit systemd examples](https://github.com/moby/buildkit/tree/master/examples/systemd) for running it as a systemd service.

2. Check that you have a Unix socket that you can connect to.

   ```console
   $ ls -lh /home/user/buildkitd.sock
   srw-rw---- 1 root user 0 May  5 11:04 /home/user/buildkitd.sock
   ```

3. Connect Buildx to it using the remote driver:

   ```console
   $ docker buildx create \
     --name remote-unix \
     --driver remote \
     unix://$HOME/buildkitd.sock
   ```

4. List available builders with `docker buildx ls`. You should then see `remote-unix` among them:

   ```console
   $ docker buildx ls
   NAME/NODE           DRIVER/ENDPOINT                        STATUS  PLATFORMS
   remote-unix         remote
     remote-unix0      unix:///home/.../buildkitd.sock        running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *           docker
     default           default                                running linux/amd64, linux/386
   ```

You can switch to this new builder as the default using `docker buildx use remote-unix`, or specify it per build using `--builder`:

```console
$ docker buildx build --builder=remote-unix -t test --load .
```

Remember that you need to use the `--load` flag if you want to load the build result into the Docker daemon.

## [Example: Remote BuildKit in Docker container](#example-remote-buildkit-in-docker-container)

This guide will show you how to create setup similar to the `docker-container` driver, by manually booting a BuildKit Docker container and connecting to it using the Buildx remote driver. This procedure will manually create a container and access it via it's exposed port. (You'd probably be better of just using the `docker-container` driver that connects to BuildKit through the Docker daemon, but this is for illustration purposes.)

1. Generate certificates for BuildKit.

   You can use this [bake definition](https://github.com/moby/buildkit/blob/master/examples/create-certs) as a starting point:

   ```console
   SAN="localhost 127.0.0.1" docker buildx bake "https://github.com/moby/buildkit.git#master:examples/create-certs"
   ```

   Note that while it's possible to expose BuildKit over TCP without using TLS, it's not recommended. Doing so allows arbitrary access to BuildKit without credentials.

2. With certificates generated in `.certs/`, startup the container:

   ```console
   $ docker run -d --rm \
     --name=remote-buildkitd \
     --privileged \
     -p 1234:1234 \
     -v $PWD/.certs:/etc/buildkit/certs \
     moby/buildkit:latest \
     --addr tcp://0.0.0.0:1234 \
     --tlscacert /etc/buildkit/certs/daemon/ca.pem \
     --tlscert /etc/buildkit/certs/daemon/cert.pem \
     --tlskey /etc/buildkit/certs/daemon/key.pem
   ```

   This command starts a BuildKit container and exposes the daemon's port 1234 to localhost.

3. Connect to this running container using Buildx:

   ```console
   $ docker buildx create \
     --name remote-container \
     --driver remote \
     --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem,servername=TLS_SERVER_NAME \
     tcp://localhost:1234
   ```

   Alternatively, use the `docker-container://` URL scheme to connect to the BuildKit container without specifying a port:

   ```console
   $ docker buildx create \
     --name remote-container \
     --driver remote \
     docker-container://remote-container
   ```

## [Example: Remote BuildKit in Kubernetes](#example-remote-buildkit-in-kubernetes)

This guide will show you how to create a setup similar to the `kubernetes` driver by manually creating a BuildKit `Deployment`. While the `kubernetes` driver will do this under-the-hood, it might sometimes be desirable to scale BuildKit manually. Additionally, when executing builds from inside Kubernetes pods, the Buildx builder will need to be recreated from within each pod or copied between them.

1. Create a Kubernetes deployment of `buildkitd` by following the instructions [in the BuildKit documentation](https://github.com/moby/buildkit/tree/master/examples/kubernetes).

   Create certificates for the BuildKit daemon and client using the [create-certs.sh](https://github.com/moby/buildkit/blob/master/examples/kubernetes/create-certs.sh), script and create a deployment of BuildKit pods with a service that connects to them.

2. Assuming that the service is called `buildkitd`, create a remote builder in Buildx, ensuring that the listed certificate files are present:

   ```console
   $ docker buildx create \
     --name remote-kubernetes \
     --driver remote \
     --driver-opt cacert=${PWD}/.certs/client/ca.pem,cert=${PWD}/.certs/client/cert.pem,key=${PWD}/.certs/client/key.pem \
     tcp://buildkitd.default.svc:1234
   ```

Note that this only works internally, within the cluster, since the BuildKit setup guide only creates a `ClusterIP` service. To access a builder remotely, you can set up and use an ingress, which is outside the scope of this guide.

### [Debug a remote builder in Kubernetes](#debug-a-remote-builder-in-kubernetes)

If you're having trouble accessing a remote builder deployed in Kubernetes, you can use the `kube-pod://` URL scheme to connect directly to a BuildKit pod through the Kubernetes API. Note that this method only connects to a single pod in the deployment.

```console
$ kubectl get pods --selector=app=buildkitd -o json | jq -r '.items[].metadata.name'
buildkitd-XXXXXXXXXX-xxxxx
$ docker buildx create \
  --name remote-container \
  --driver remote \
  kube-pod://buildkitd-XXXXXXXXXX-xxxxx
```

Alternatively, use the port forwarding mechanism of `kubectl`:

```console
$ kubectl port-forward svc/buildkitd 1234:1234
```

Then you can point the remote driver at `tcp://localhost:1234`.

----
url: https://docs.docker.com/reference/api/engine/
----

# Docker Engine API

***

Table of contents

***

Docker provides an API for interacting with the Docker daemon (called the Docker Engine API), as well as SDKs for Go and Python. The SDKs allow you to efficiently build and scale Docker apps and solutions. If Go or Python don't work for you, you can use the Docker Engine API directly.

For information about Docker Engine SDKs, see [Develop with Docker Engine SDKs](https://docs.docker.com/reference/api/engine/sdk/).

The Docker Engine API is a RESTful API accessed by an HTTP client such as `wget` or `curl`, or the HTTP library which is part of most modern programming languages.

## [View the API reference](#view-the-api-reference)

You can [view the reference for the latest version of the API](https://docs.docker.com/reference/api/engine/version/v1.54/) or [choose a specific version](/reference/api/engine/#api-version-matrix).

## [Versioned API and SDK](#versioned-api-and-sdk)

The version of the Docker Engine API you should use depends upon the version of your Docker daemon and Docker client.

A given version of the Docker Engine SDK supports a specific version of the Docker Engine API, as well as all earlier versions. If breaking changes occur, they are documented prominently.

> Note
>
> The Docker daemon and client don't necessarily need to be the same version at all times. However, keep the following in mind.
>
> * If the daemon is newer than the client, the client doesn't know about new features or deprecated API endpoints in the daemon.
>
> * If the client is newer than the daemon, the client can request API endpoints that the daemon doesn't know about.

A new version of the API is released when new features are added. The Docker API is backward-compatible, so you don't need to update code that uses the API unless you need to take advantage of new features.

To see the highest and lowest version of the API your Docker daemon and client support, use `docker version`:

```console
$ docker version
Client: Docker Engine - Community
 Version:           29.5.3
 API version:       1.54
 ...

Server: Docker Engine - Community
 Engine:
  Version:          29.5.3
  API version:      1.54 (minimum version 1.40)
  ...
```

You can specify the API version to use in any of the following ways:

* When using the SDK, use the latest version. At a minimum, use the version that incorporates the API version with the features you need.

* When using `curl` directly, specify the version as the first part of the URL. For instance, if the endpoint is `/containers/` you can use `/v1.54/containers/`.

* To force the Docker CLI or the Docker Engine SDKs to use an older version of the API than the version reported by `docker version`, set the environment variable `DOCKER_API_VERSION` to the correct version. This works on Linux, Windows, and macOS clients.

  ```console
  $ DOCKER_API_VERSION=1.53
  ```

  While the environment variable is set, that version of the API is used, even if the Docker daemon supports a newer version. This environment variable disables API version negotiation, so you should only use it if you must use a specific version of the API, or for debugging purposes.

* The Docker Go SDK allows you to enable API version negotiation, automatically selects an API version that's supported by both the client and the Docker Engine that's in use.

* For the SDKs, you can also specify the API version programmatically as a parameter to the `client` object. See the [Go constructor](https://pkg.go.dev/github.com/docker/docker/client#NewClientWithOpts) or the [Python SDK documentation for `client`](https://docker-py.readthedocs.io/en/stable/client.html).

### [Minimum API version](#minimum-api-version)

The Docker Engine API server and client support API-version negotiation. If a client connects to an older version of the Docker Engine, it negotiates the highest version of the API supported by both the client and daemon, downgrading to an older version of the API if necessary.

When downgrading to an older API version, features introduced in later API versions are disabled, and API requests and responses are adjusted for the API version negotiated.

API version negotiation allows tools that have not been upgraded yet to the latest API version specification to communicate with newer Docker Engines (and vice versa), but compatibility is "best effort"; while Docker strives to provide full compatibility, some functionality may not be available.

### [API version matrix](#api-version-matrix)

| Docker version | Maximum API version                          | Minimum API version                          | Change log                                                         |
| -------------- | -------------------------------------------- | -------------------------------------------- | ------------------------------------------------------------------ |
| 29.5           | [1.54](/reference/api/engine/version/v1.54/) | [1.40](/reference/api/engine/version/v1.40/) | [changes](/reference/api/engine/version-history/#v154-api-changes) |
| 29.4           | [1.54](/reference/api/engine/version/v1.54/) | [1.40](/reference/api/engine/version/v1.40/) | [changes](/reference/api/engine/version-history/#v154-api-changes) |
| 29.3           | [1.54](/reference/api/engine/version/v1.54/) | [1.40](/reference/api/engine/version/v1.40/) | [changes](/reference/api/engine/version-history/#v154-api-changes) |
| 29.2           | [1.53](/reference/api/engine/version/v1.53/) | [1.44](/reference/api/engine/version/v1.44/) | [changes](/reference/api/engine/version-history/#v153-api-changes) |
| 29.1           | [1.52](/reference/api/engine/version/v1.52/) | [1.44](/reference/api/engine/version/v1.44/) | [changes](/reference/api/engine/version-history/#v152-api-changes) |
| 29.0           | [1.52](/reference/api/engine/version/v1.52/) | [1.44](/reference/api/engine/version/v1.44/) | [changes](/reference/api/engine/version-history/#v152-api-changes) |
| 28.5           | [1.51](/reference/api/engine/version/v1.51/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v151-api-changes) |
| 28.4           | [1.51](/reference/api/engine/version/v1.51/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v151-api-changes) |
| 28.3           | [1.51](/reference/api/engine/version/v1.51/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v151-api-changes) |
| 28.2           | [1.50](/reference/api/engine/version/v1.50/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v150-api-changes) |
| 28.1           | [1.49](/reference/api/engine/version/v1.49/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v149-api-changes) |
| 28.0           | [1.48](/reference/api/engine/version/v1.48/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v148-api-changes) |
| 27.5           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v147-api-changes) |
| 27.4           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v147-api-changes) |
| 27.3           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v147-api-changes) |
| 27.2           | [1.47](/reference/api/engine/version/v1.47/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v147-api-changes) |
| 27.1           | [1.46](/reference/api/engine/version/v1.46/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v146-api-changes) |
| 27.0           | [1.46](/reference/api/engine/version/v1.46/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v146-api-changes) |
| 26.1           | [1.45](/reference/api/engine/version/v1.45/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v145-api-changes) |
| 26.0           | [1.45](/reference/api/engine/version/v1.45/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v145-api-changes) |
| 25.0           | [1.44](/reference/api/engine/version/v1.44/) | 1.24                                         | [changes](/reference/api/engine/version-history/#v144-api-changes) |
| 24.0           | [1.43](/reference/api/engine/version/v1.43/) | 1.12                                         | [changes](/reference/api/engine/version-history/#v143-api-changes) |
| 23.0           | [1.42](/reference/api/engine/version/v1.42/) | 1.12                                         | [changes](/reference/api/engine/version-history/#v142-api-changes) |
| 20.10          | [1.41](/reference/api/engine/version/v1.41/) | 1.12                                         | [changes](/reference/api/engine/version-history/#v141-api-changes) |
| 19.03          | [1.40](/reference/api/engine/version/v1.40/) | 1.12                                         | [changes](/reference/api/engine/version-history/#v140-api-changes) |

### [Deprecated API versions](#deprecated-api-versions)

API versions before v1.40 are deprecated and no longer supported by current versions of the Docker Engine and CLI. You can find archived documentation for deprecated versions of the API [in the code repository on GitHub](https://github.com/moby/moby/tree/docker-v29.5.3/api/docs):

| Docker version | Maximum API version | Minimum API version | Change log                                                         |
| -------------- | ------------------- | ------------------- | ------------------------------------------------------------------ |
| 18.09          | 1.39                | 1.12                | [changes](/reference/api/engine/version-history/#v139-api-changes) |
| 18.06          | 1.38                | 1.12                | [changes](/reference/api/engine/version-history/#v138-api-changes) |
| 18.05          | 1.37                | 1.12                | [changes](/reference/api/engine/version-history/#v137-api-changes) |
| 18.04          | 1.37                | 1.12                | [changes](/reference/api/engine/version-history/#v137-api-changes) |
| 18.03          | 1.37                | 1.12                | [changes](/reference/api/engine/version-history/#v137-api-changes) |
| 18.02          | 1.36                | 1.12                | [changes](/reference/api/engine/version-history/#v136-api-changes) |
| 17.12          | 1.35                | 1.12                | [changes](/reference/api/engine/version-history/#v135-api-changes) |
| 17.11          | 1.34                | 1.12                | [changes](/reference/api/engine/version-history/#v134-api-changes) |
| 17.10          | 1.33                | 1.12                | [changes](/reference/api/engine/version-history/#v133-api-changes) |
| 17.09          | 1.32                | 1.12                | [changes](/reference/api/engine/version-history/#v132-api-changes) |
| 17.07          | 1.31                | 1.12                | [changes](/reference/api/engine/version-history/#v131-api-changes) |
| 17.06          | 1.30                | 1.12                | [changes](/reference/api/engine/version-history/#v130-api-changes) |
| 17.05          | 1.29                | 1.12                | [changes](/reference/api/engine/version-history/#v129-api-changes) |
| 17.04          | 1.28                | 1.12                | [changes](/reference/api/engine/version-history/#v128-api-changes) |
| 17.03.1        | 1.27                | 1.12                | [changes](/reference/api/engine/version-history/#v127-api-changes) |
| 17.03          | 1.26                | 1.12                | [changes](/reference/api/engine/version-history/#v126-api-changes) |
| 1.13.1         | 1.26                | 1.12                | [changes](/reference/api/engine/version-history/#v126-api-changes) |
| 1.13           | 1.25                | 1.12                | [changes](/reference/api/engine/version-history/#v125-api-changes) |
| 1.12           | 1.24                | 1.12                | [changes](/reference/api/engine/version-history/#v124-api-changes) |
| 1.11           | 1.23                | 1.12                | [changes](/reference/api/engine/version-history/#v123-api-changes) |
| 1.10           | 1.22                | 1.12                | [changes](/reference/api/engine/version-history/#v122-api-changes) |
| 1.9            | 1.21                | 1.12                | [changes](/reference/api/engine/version-history/#v121-api-changes) |
| 1.8            | 1.20                | 1.12                | [changes](/reference/api/engine/version-history/#v120-api-changes) |
| 1.7            | 1.19                | 1.0                 | [changes](/reference/api/engine/version-history/#v119-api-changes) |
| 1.6            | 1.18                | 1.0                 | [changes](/reference/api/engine/version-history/#v118-api-changes) |
| 1.5            | 1.17                | 1.0                 | [changes](/reference/api/engine/version-history/#v117-api-changes) |
| 1.4            | 1.16                | 1.0                 | [changes](/reference/api/engine/version-history/#v116-api-changes) |
| 1.3            | 1.15                | 1.0                 | [changes](/reference/api/engine/version-history/#v115-api-changes) |
| 1.2            | 1.14                | 1.0                 | [changes](/reference/api/engine/version-history/#v114-api-changes) |
| 1.1            | 1.13                | 1.0                 | [changes](/reference/api/engine/version-history/#v113-api-changes) |
| 1.0            | 1.12                | 1.0                 | [changes](/reference/api/engine/version-history/#v112-api-changes) |
| 0.12           | 1.12                | 1.0                 | [changes](/reference/api/engine/version-history/#v112-api-changes) |
| 0.11           | 1.11                | 1.0                 | [changes](/reference/api/engine/version-history/#v111-api-changes) |
| 0.10           | 1.10                | 1.0                 | [changes](/reference/api/engine/version-history/#v110-api-changes) |
| 0.9            | 1.10                | 1.0                 | [changes](/reference/api/engine/version-history/#v110-api-changes) |
| 0.8            | 1.9                 | 1.0                 | [changes](/reference/api/engine/version-history/#v19-api-changes)  |
| 0.7.1          | 1.8                 | 1.0                 | [changes](/reference/api/engine/version-history/#v18-api-changes)  |
| 0.7            | 1.7                 | 1.0                 | [changes](/reference/api/engine/version-history/#v17-api-changes)  |
| 0.6.4          | 1.6                 | 1.0                 | [changes](/reference/api/engine/version-history/#v16-api-changes)  |
| 0.6.2          | 1.5                 | 1.0                 | [changes](/reference/api/engine/version-history/#v15-api-changes)  |
| 0.6            | 1.4                 | 1.0                 | [changes](/reference/api/engine/version-history/#v14-api-changes)  |
| 0.5            | 1.3                 | 1.0                 | [changes](/reference/api/engine/version-history/#v13-api-changes)  |
| 0.4.1          | 1.2                 | 1.0                 | [changes](/reference/api/engine/version-history/#v12-api-changes)  |
| 0.3.4          | 1.1                 | 1.0                 | [changes](/reference/api/engine/version-history/#v11-api-changes)  |
| 0.3.3          | 1.0                 | 1.0                 | [changes](/reference/api/engine/version-history/#v10-api-changes)  |
| 0.3.2          | -                   | -                   |                                                                    |
| 0.2            | -                   | -                   |                                                                    |
| 0.1            | -                   | -                   |                                                                    |

----
url: https://docs.docker.com/reference/api/engine/version/v1.50.yaml
----

basePath: "/v1.50"
info:
 title: "Docker Engine API"
 version: "1.50"

 For example, calling \`/info\` is the same as calling \`/v1.50/info\`. Using the

 description: "Docker Version used to create the plugin"
 type: "string"
 x-nullable: false
 example: "17.06.0-ce"

----
url: https://docs.docker.com/engine/install/debian/
----

# Install Docker Engine on Debian

***

Table of contents

***

To get started with Docker Engine on Debian, make sure you [meet the prerequisites](#prerequisites), and then follow the [installation steps](#installation-methods).

## [Prerequisites](#prerequisites)

### [Firewall limitations](#firewall-limitations)

> Warning
>
> Before you install Docker, make sure you consider the following security implications and firewall incompatibilities.

* If you use ufw or firewalld to manage firewall settings, be aware that when you expose container ports using Docker, these ports bypass your firewall rules. For more information, refer to [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw).
* Docker is only compatible with `iptables-nft` and `iptables-legacy`. Firewall rules created with `nft` are not supported on a system with Docker installed. Make sure that any firewall rulesets you use are created with `iptables` or `ip6tables`, and that you add them to the `DOCKER-USER` chain, see [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

### [OS requirements](#os-requirements)

To install Docker Engine, you need one of these Debian versions:

* Debian Trixie 13 (stable)
* Debian Bookworm 12 (oldstable)
* Debian Bullseye 11 (oldoldstable)

Docker Engine for Debian is compatible with x86\_64 (or amd64), armhf (arm/v7), arm64, and ppc64le (ppc64el) architectures.

```console
$ sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-doc podman-docker containerd runc | cut -f1)
```

   ```bash
   # Add Docker's official GPG key:
   sudo apt update
   sudo apt install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
   Types: deb
   URIs: https://download.docker.com/linux/debian
   Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
   Components: stable
   Architectures: $(dpkg --print-architecture)
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF

   sudo apt update
   ```

   > Note
   >
   > If you use Debian testing or a derivative distribution such as Kali Linux, you may need to substitute the part of this command that's expected to print the version codename:
   >
   > ```console
   > $(. /etc/os-release && echo "$VERSION_CODENAME")
   > ```
   >
   > Replace this part with the codename of the corresponding Debian release, such as `trixie`.

2. Install the Docker packages.

   To install the latest version, run:

   ```console
   $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   To install a specific version of Docker Engine, start by listing the available versions in the repository:

   ```console
   $ apt list --all-versions docker-ce

   docker-ce/bookworm 5:29.5.3-1~debian.12~bookworm <arch>
   docker-ce/bookworm 5:29.5.2-1~debian.12~bookworm <arch>
   ...
   ```

   Select the desired version and install:

   ```console
   $ VERSION_STRING=5:29.5.3-1~debian.12~bookworm
   $ sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   > Note
   >
   > After installation, verify that Docker is running:
   >
   > ```console
   > $ sudo systemctl status docker
   > ```
   >
   > If Docker is not running, start it manually:
   >
   > ```console
   > $ sudo systemctl start docker
   > ```

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

To upgrade Docker Engine, follow step 2 of the [installation instructions](#install-using-the-repository), choosing the new version you want to install.

### [Install from a package](#install-from-a-package)

If you can't use Docker's `apt` repository to install Docker Engine, you can download the `deb` file for your release and install it manually. You need to download a new file each time you want to upgrade Docker Engine.

1. Go to [`https://download.docker.com/linux/debian/dists/`](https://download.docker.com/linux/debian/dists/).

2. Select your Debian version in the list.

   ```console
   $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
     ./docker-ce_<version>_<arch>.deb \
     ./docker-ce-cli_<version>_<arch>.deb \
     ./docker-buildx-plugin_<version>_<arch>.deb \
     ./docker-compose-plugin_<version>_<arch>.deb
   ```

   > Note
   >
   > After installation, verify that Docker is running:
   >
   > ```console
   > $ sudo systemctl status docker
   > ```
   >
   > If Docker is not running, start it manually:
   >
   > ```console
   > $ sudo systemctl start docker
   > ```

6. Verify that the installation is successful by running the `hello-world` image:

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
   $ sudo apt purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

3. Remove source list and keyrings

   ```console
   $ sudo rm /etc/apt/sources.list.d/docker.sources
   $ sudo rm /etc/apt/keyrings/docker.asc
   ```

You have to delete any edited configuration files manually.

## [Next steps](#next-steps)

* Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).

----
url: https://docs.docker.com/reference/cli/docker/buildx/policy/eval/
----

# docker buildx policy eval

***

| Description | Evaluate policy for a source                 |
| ----------- | -------------------------------------------- |
| Usage       | `docker buildx policy eval [OPTIONS] source` |

## [Description](#description)

Evaluate policy for a source

## [Options](#options)

| Option       | Default      | Description                           |
| ------------ | ------------ | ------------------------------------- |
| `--fields`   |              | Fields to evaluate                    |
| `-f, --file` | `Dockerfile` | Policy filename to evaluate           |
| `--platform` |              | Target platform for policy evaluation |
| `--print`    |              | Print policy output                   |

----
url: https://docs.docker.com/reference/cli/docker/dhi/mirror/list/
----

# docker dhi mirror list

***

| Description | List all mirrored Docker Hardened Images |
| ----------- | ---------------------------------------- |
| Usage       | `docker dhi mirror list`                 |

## [Description](#description)

List all Docker Hardened Images currently being mirrored to your organization's registry.

Shows the source repositories, destination repositories, and mirroring status.

Examples:

# [List all mirrored repositories](#list-all-mirrored-repositories)

docker dhi mirror list --org myorg

# [List only image repositories](#list-only-image-repositories)

docker dhi mirror list --org myorg --type image

# [List only helm chart repositories](#list-only-helm-chart-repositories)

docker dhi mirror list --org myorg --type helm-chart

# [Search for a specific repository by name](#search-for-a-specific-repository-by-name)

docker dhi mirror list --org myorg --filter dhi-python

# [Output in JSON format](#output-in-json-format)

docker dhi mirror list --org myorg --json

## [Options](#options)

| Option         | Default | Description                                     |
| -------------- | ------- | ----------------------------------------------- |
| `-f, --filter` |         | Filter by repository name (partial match)       |
| `--json`       |         | Output in JSON format                           |
| `--type`       |         | Filter by repository type (image or helm-chart) |

----
url: https://docs.docker.com/guides/lab-compose-quickstart/
----

[Lab: Docker Compose Quickstart](https://docs.docker.com/guides/lab-compose-quickstart/)

Hands-on lab: Define and run a multi-container app with Docker Compose. Progress from a bare compose.yaml through health checks, live development with watch mode, data persistence, and modular Compose file composition.

Labs

45 minutes

Resources:

* [Docker Compose docs](/compose/)
* [Compose watch mode](/compose/how-tos/file-watch/)
* [Labspace repository](https://github.com/dockersamples/labspace-compose-quickstart)

[« Back to all guides](/guides/)

# Lab: Docker Compose Quickstart

***

Table of contents

***

Build a Python Flask and Redis hit-counter app using Docker Compose, starting from a bare `compose.yaml` and progressively adding production-quality features at each step.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-compose-quickstart up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Define a multi-service application in a `compose.yaml` file and manage it with Compose commands
* Control service startup order using health checks and `depends_on` conditions
* Iterate on code without manual rebuilds using Compose watch mode
* Persist data across container restarts with named volumes
* Modularize a stack across multiple files using the `include` directive
* Use `config`, `logs`, and `exec` to inspect and debug a running stack

## [Modules](#modules)

| # | Module                           | Description                                                           |
| - | -------------------------------- | --------------------------------------------------------------------- |
| 1 | Introduction                     | Tour the starter app and verify the environment                       |
| 2 | Defining Services                | Write the first `compose.yaml` and bring up the Flask and Redis stack |
| 3 | Health Checks & Startup Order    | Add a Redis healthcheck and `depends_on` to eliminate race conditions |
| 4 | Live Development with Watch Mode | Configure watch mode to sync code changes without manual rebuilds     |
| 5 | Persistence & Debugging          | Add a named volume so Redis data survives `docker compose down`       |
| 6 | Using Multiple Compose Files     | Extract Redis into `infra.yaml` and compose files with `include`      |
| 7 | Additional Commands              | Use `config`, `logs -f`, and `exec` to inspect the running stack      |
| 8 | Recap                            | Review what was built and explore next steps                          |

----
url: https://docs.docker.com/guides/java/containerize/
----

# Containerize a Java application

***

Table of contents

***

## [Prerequisites](#prerequisites)

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/). Docker adds new features regularly and some parts of this guide may work only with the latest version of Docker Desktop.

- You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## [Overview](#overview)

This section walks you through containerizing and running a Java application.

## [Get the sample applications](#get-the-sample-applications)

Clone the sample application that you'll be using to your local development machine. Run the following command in a terminal to clone the repository.

```console
$ git clone https://github.com/spring-projects/spring-petclinic.git
```

The sample application is a Spring Boot application built using Maven. For more details, see `readme.md` in the repository.

## [Create Docker assets](#create-docker-assets)

Now that you have an application, you can create the necessary Docker assets to containerize your application.

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

Create a file named `Dockerfile` with the following contents.

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

################################################################################

# Create a stage for resolving and downloading dependencies.
FROM eclipse-temurin:21-jdk-jammy as deps

WORKDIR /build

# Copy the mvnw wrapper with executable permissions.
COPY --chmod=0755 mvnw mvnw
COPY .mvn/ .mvn/

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.m2 so that subsequent builds don't have to
# re-download packages.
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 ./mvnw dependency:go-offline -DskipTests

################################################################################

# Create a stage for building the application based on the stage with downloaded dependencies.
# This Dockerfile is optimized for Java applications that output an uber jar, which includes
# all the dependencies needed to run your app inside a JVM. If your app doesn't output an uber
# jar and instead relies on an application server like Apache Tomcat, you'll need to update this
# stage with the correct filename of your package and update the base image of the "final" stage
# use the relevant app server, e.g., using tomcat (https://hub.docker.com/_/tomcat/) as a base image.
FROM deps as package

WORKDIR /build

COPY ./src src/
RUN --mount=type=bind,source=pom.xml,target=pom.xml \
    --mount=type=cache,target=/root/.m2 \
    ./mvnw package -DskipTests && \
    mv target/$(./mvnw help:evaluate -Dexpression=project.artifactId -q -DforceStdout)-$(./mvnw help:evaluate -Dexpression=project.version -q -DforceStdout).jar target/app.jar

################################################################################

# Create a stage for extracting the application into separate layers.
# Take advantage of Spring Boot's layer tools and Docker's caching by extracting
# the packaged application into separate layers that can be copied into the final stage.
# See Spring's docs for reference:
# https://docs.spring.io/spring-boot/docs/current/reference/html/container-images.html
FROM package as extract

WORKDIR /build

RUN java -Djarmode=layertools -jar target/app.jar extract --destination target/extracted

################################################################################

# Create a new stage for running the application that contains the minimal
# runtime dependencies for the application. This often uses a different base
# image from the install or build stage where the necessary files are copied
# from the install stage.
#
# The example below uses eclipse-turmin's JRE image as the foundation for running the app.
# By specifying the "17-jre-jammy" tag, it will also use whatever happens to be the
# most recent version of that tag when you build your Dockerfile.
# If reproducibility is important, consider using a specific digest SHA, like
# eclipse-temurin@sha256:99cede493dfd88720b610eb8077c8688d3cca50003d76d1d539b0efc8cca72b4.
FROM eclipse-temurin:21-jre-jammy AS final

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
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

# Copy the executable from the "package" stage.
COPY --from=extract build/target/extracted/dependencies/ ./
COPY --from=extract build/target/extracted/spring-boot-loader/ ./
COPY --from=extract build/target/extracted/snapshot-dependencies/ ./
COPY --from=extract build/target/extracted/application/ ./

EXPOSE 8080

ENTRYPOINT [ "java", "org.springframework.boot.loader.launch.JarLauncher" ]
```

> Note
>
> The sample repository includes a `docker-compose.yml` file. The following instructions use the preferred `compose.yaml` filename — both are supported by Docker Compose.

Create a file named `compose.yaml` with the following contents.

compose.yaml

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
# The commented out section below is an example of how to define a PostgreSQL
# database that your application can use. `depends_on` tells Docker Compose to
# start the database before your application. The `db-data` volume persists the
# database data between container restarts. The `db-password` secret is used
# to set the database password. You must create `db/password.txt` and add
# a password of your choosing to it before running `docker compose up`.
#     depends_on:
#       db:
#         condition: service_healthy
#   db:
#     image: postgres:18
#     restart: always
#     user: postgres
#     secrets:
#       - db-password
#     volumes:
#       - db-data:/var/lib/postgresql
#     environment:
#       - POSTGRES_DB=example
#       - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
#     expose:
#       - 5432
#     healthcheck:
#       test: [ "CMD", "pg_isready" ]
#       interval: 10s
#       timeout: 5s
#       retries: 5
# volumes:
#   db-data:
# secrets:
#   db-password:
#     file: db/password.txt
```

Create a file named `.dockerignore` with the following contents.

.dockerignore

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

**/.classpath
**/.dockerignore
**/.env
**/.git
**/.gitignore
**/.project
**/.settings
**/.toolstarget
**/.vs
**/.vscode
**/.next
**/.cache
**/*.*proj.user
**/*.dbmdl
**/*.jfm
**/charts
**/docker-compose*
**/compose.y*ml
**/target
**/Dockerfile*
**/node_modules
**/npm-debug.log
**/obj
**/secrets.dev.yaml
**/values.dev.yaml
**/vendor
LICENSE
README.md
```

You should now have the following three files in your `spring-petclinic` directory.

* [Dockerfile](/reference/dockerfile/)
* [.dockerignore](/reference/dockerfile/#dockerignore-file)
* [compose.yaml](https://docs.docker.com/reference/compose-file/)

## [Run the application](#run-the-application)

Inside the `spring-petclinic` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

The first time you build and run the app, Docker downloads dependencies and builds the app. It may take several minutes depending on your network connection.

Open a browser and view the application at <http://localhost:8080>. You should see a simple app for a pet clinic.

In the terminal, press `ctrl`+`c` to stop the application.

### [Run the application in the background](#run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option. Inside the `spring-petclinic` directory, run the following command in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at <http://localhost:8080>. You should see a simple app for a pet clinic.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

## [Summary](#summary)

In this section, you learned how you can containerize and run a Java application using Docker.

## [Next steps](#next-steps)

In the next section, you'll learn how you can develop your application using Docker containers.

[Use containers for Java development »](https://docs.docker.com/guides/java/develop/)

----
url: https://docs.docker.com/guides/rag-ollama/containerize/
----

# Containerize a RAG application

***

Table of contents

***

## [Overview](#overview)

This section walks you through containerizing a RAG application using Docker.

> Note
>
> You can see more samples of containerized GenAI applications in the [GenAI Stack](https://github.com/docker/genai-stack) demo applications.

## [Get the sample application](#get-the-sample-application)

The sample application used in this guide is an example of RAG application, made by three main components, which are the building blocks for every RAG application. A Large Language Model hosted somewhere, in this case it is hosted in a container and served via [Ollama](https://ollama.ai/). A vector database, [Qdrant](https://qdrant.tech/), to store the embeddings of local data, and a web application, using [Streamlit](https://streamlit.io/) to offer the best user experience to the user.

Clone the sample application. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/mfranzon/winy.git
```

You should now have the following files in your `winy` directory.

```text
├── winy/
│ ├── .gitignore
│ ├── app/
│ │ ├── main.py
│ │ ├── Dockerfile
| | └── requirements.txt
│ ├── tools/
│ │ ├── create_db.py
│ │ ├── create_embeddings.py
│ │ ├── requirements.txt
│ │ ├── test.py
| | └── download_model.sh
│ ├── docker-compose.yaml
│ ├── wine_database.db
│ ├── LICENSE
│ └── README.md
```

## [Containerizing your application: Essentials](#containerizing-your-application-essentials)

Containerizing an application involves packaging it along with its dependencies into a container, which ensures consistency across different environments. Here’s what you need to containerize an app like Winy :

1. Dockerfile: A Dockerfile that contains instructions on how to build a Docker image for your application. It specifies the base image, dependencies, configuration files, and the command to run your application.

2. Docker Compose File: Docker Compose is a tool for defining and running multi-container Docker applications. A Compose file allows you to configure your application's services, networks, and volumes in a single file.

## [Run the application](#run-the-application)

Inside the `winy` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

Docker builds and runs your application. Depending on your network connection, it may take several minutes to download all the dependencies. You'll see a message like the following in the terminal when the application is running.

```console
server-1  |   You can now view your Streamlit app in your browser.
server-1  |
server-1  |   URL: http://0.0.0.0:8501
server-1  |
```

Open a browser and view the application at <http://localhost:8501>. You should see a simple Streamlit application.

The application requires a Qdrant database service and an LLM service to work properly. If you have access to services that you ran outside of Docker, specify the connection information in the `docker-compose.yaml`.

```yaml
winy:
  build:
    context: ./app
    dockerfile: Dockerfile
  environment:
    - QDRANT_CLIENT=http://qdrant:6333 # Specifies the url for the qdrant database
    - OLLAMA=http://ollama:11434 # Specifies the url for the ollama service
  container_name: winy
  ports:
    - "8501:8501"
  depends_on:
    - qdrant
    - ollama
```

If you don't have the services running, continue with this guide to learn how you can run some or all of these services with Docker. Remember that the `ollama` service is empty; it doesn't have any model. For this reason you need to pull a model before starting to use the RAG application. All the instructions are in the following page.

In the terminal, press `ctrl`+`c` to stop the application.

## [Summary](#summary)

In this section, you learned how you can containerize and run your RAG application using Docker.

## [Next steps](#next-steps)

In the next section, you'll learn how to properly configure the application with your preferred LLM model, completely locally, using Docker.

[Use containers for RAG development »](https://docs.docker.com/guides/rag-ollama/develop/)

----
url: https://docs.docker.com/guides/testcontainers-java-mockserver/create-project/
----

# Create the Spring Boot project

***

Table of contents

***

## [Set up the project](#set-up-the-project)

Create a Spring Boot project from [Spring Initializr](https://start.spring.io) by selecting the **Spring Web**, **Spring Reactive Web**, and **Testcontainers** starters.

Alternatively, clone the [guide repository](https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-using-mockserver).

After generating the project, add the **REST Assured** and **MockServer** libraries as test dependencies. The key dependencies in `pom.xml` are:

```xml
<properties>
    <java.version>17</java.version>
    <testcontainers.version>2.0.4</testcontainers.version>
</properties>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-webflux</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-mockserver</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.mock-server</groupId>
        <artifactId>mockserver-netty</artifactId>
        <version>5.15.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

Using the Testcontainers BOM (Bill of Materials) is recommended so that you don't have to repeat the version for every Testcontainers module dependency.

This guide builds an application that manages video albums. A third-party REST API handles photo assets. For demonstration purposes, the application uses the publicly available [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API as a photo service.

The application exposes a `GET /api/albums/{albumId}` endpoint that calls the photo service to fetch photos for a given album. [MockServer](https://www.mock-server.com/) is a library for mocking HTTP-based services. Testcontainers provides a [MockServer module](https://java.testcontainers.org/modules/mockserver/) that runs MockServer as a Docker container.

## [Create the Album and Photo models](#create-the-album-and-photo-models)

Create `Album.java` using Java records:

```java
package com.testcontainers.demo;

import java.util.List;

public record Album(Long albumId, List<Photo> photos) {}

record Photo(Long id, String title, String url, String thumbnailUrl) {}
```

## [Create the PhotoServiceClient interface](#create-the-photoserviceclient-interface)

Spring Framework 6 introduced [declarative HTTP client support](https://docs.spring.io/spring-framework/reference/integration/rest-clients.html#rest-http-interface). Create an interface with a method that fetches photos for a given album ID:

```java
package com.testcontainers.demo;

import java.util.List;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.service.annotation.GetExchange;

interface PhotoServiceClient {
  @GetExchange("/albums/{albumId}/photos")
  List<Photo> getPhotos(@PathVariable Long albumId);
}
```

## [Register PhotoServiceClient as a bean](#register-photoserviceclient-as-a-bean)

To generate a runtime implementation of `PhotoServiceClient`, register it as a Spring bean using `HttpServiceProxyFactory`. The factory requires an `HttpClientAdapter` implementation. Spring Boot provides `WebClientAdapter` as part of the `spring-webflux` library:

```java
package com.testcontainers.demo;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

@Configuration
public class AppConfig {

  @Bean
  public PhotoServiceClient photoServiceClient(
    @Value("${photos.api.base-url}") String photosApiBaseUrl
  ) {
    WebClient client = WebClient.builder().baseUrl(photosApiBaseUrl).build();
    HttpServiceProxyFactory factory = HttpServiceProxyFactory
      .builder(WebClientAdapter.forClient(client))
      .build();
    return factory.createClient(PhotoServiceClient.class);
  }
}
```

The photo service base URL is externalized as a configuration property. Add the following entry to `src/main/resources/application.properties`:

```properties
photos.api.base-url=https://jsonplaceholder.typicode.com
```

## [Create the REST API endpoint](#create-the-rest-api-endpoint)

Create `AlbumController.java`:

```java
package com.testcontainers.demo;

import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.reactive.function.client.WebClientResponseException;

@RestController
@RequestMapping("/api")
class AlbumController {

  private static final Logger logger = LoggerFactory.getLogger(
    AlbumController.class
  );

  private final PhotoServiceClient photoServiceClient;

  AlbumController(PhotoServiceClient photoServiceClient) {
    this.photoServiceClient = photoServiceClient;
  }

  @GetMapping("/albums/{albumId}")
  public ResponseEntity<Album> getAlbumById(@PathVariable Long albumId) {
    try {
      List<Photo> photos = photoServiceClient.getPhotos(albumId);
      return ResponseEntity.ok(new Album(albumId, photos));
    } catch (WebClientResponseException e) {
      logger.error("Failed to get photos", e);
      return new ResponseEntity<>(e.getStatusCode());
    }
  }
}
```

This endpoint calls the photo service for a given album ID and returns a response like:

```json
{
  "albumId": 1,
  "photos": [
    {
      "id": 51,
      "title": "non sunt voluptatem placeat consequuntur rem incidunt",
      "url": "https://via.placeholder.com/600/8e973b",
      "thumbnailUrl": "https://via.placeholder.com/150/8e973b"
    },
    {
      "id": 52,
      "title": "eveniet pariatur quia nobis reiciendis laboriosam ea",
      "url": "https://via.placeholder.com/600/121fa4",
      "thumbnailUrl": "https://via.placeholder.com/150/121fa4"
    }
  ]
}
```

[Write tests with Testcontainers MockServer »](https://docs.docker.com/guides/testcontainers-java-mockserver/write-tests/)

----
url: https://docs.docker.com/reference/dockerfile/
----

# Dockerfile reference

***

Table of contents

***

Docker can build images automatically by reading the instructions from a Dockerfile. A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. This page describes the commands you can use in a Dockerfile.

## [Overview](#overview)

The Dockerfile supports the following instructions:

| Instruction                            | Description                                                 |
| -------------------------------------- | ----------------------------------------------------------- |
| [`ADD`](#add)                          | Add local or remote files and directories.                  |
| [`ARG`](#arg)                          | Use build-time variables.                                   |
| [`CMD`](#cmd)                          | Specify default commands.                                   |
| [`COPY`](#copy)                        | Copy files and directories.                                 |
| [`ENTRYPOINT`](#entrypoint)            | Specify default executable.                                 |
| [`ENV`](#env)                          | Set environment variables.                                  |
| [`EXPOSE`](#expose)                    | Describe which ports your application is listening on.      |
| [`FROM`](#from)                        | Create a new build stage from a base image.                 |
| [`HEALTHCHECK`](#healthcheck)          | Check a container's health on startup.                      |
| [`LABEL`](#label)                      | Add metadata to an image.                                   |
| [`MAINTAINER`](#maintainer-deprecated) | Specify the author of an image.                             |
| [`ONBUILD`](#onbuild)                  | Specify instructions for when the image is used in a build. |
| [`RUN`](#run)                          | Execute build commands.                                     |
| [`SHELL`](#shell)                      | Set the default shell of an image.                          |
| [`STOPSIGNAL`](#stopsignal)            | Specify the system call signal for exiting a container.     |
| [`USER`](#user)                        | Set user and group ID.                                      |
| [`VOLUME`](#volume)                    | Create volume mounts.                                       |
| [`WORKDIR`](#workdir)                  | Change working directory.                                   |

## [Format](#format)

Here is the format of the Dockerfile:

```dockerfile
# Comment
INSTRUCTION arguments
```

The instruction is not case-sensitive. However, convention is for them to be UPPERCASE to distinguish them from arguments more easily.

Docker runs instructions in a Dockerfile in order. A Dockerfile **must begin with a `FROM` instruction**. This may be after [parser directives](#parser-directives), [comments](#format), and globally scoped [ARGs](#arg). The `FROM` instruction specifies the [base image](https://docs.docker.com/glossary/#base-image) from which you are building. `FROM` may only be preceded by one or more `ARG` instructions, which declare arguments that are used in `FROM` lines in the Dockerfile.

BuildKit treats lines that begin with `#` as a comment, unless the line is a valid [parser directive](#parser-directives). A `#` marker anywhere else in a line is treated as an argument. This allows statements like:

```dockerfile
# Comment
RUN echo 'we are running some # of cool things'
```

Comment lines are removed before the Dockerfile instructions are executed. The comment in the following example is removed before the shell executes the `echo` command.

```dockerfile
RUN echo hello \
# comment
world
```

The following examples is equivalent.

```dockerfile
RUN echo hello \
world
```

Comments don't support line continuation characters.

> Note
>
> **Note on whitespace**
>
> For backward compatibility, leading whitespace before comments (`#`) and instructions (such as `RUN`) are ignored, but discouraged. Leading whitespace is not preserved in these cases, and the following examples are therefore equivalent:
>
> ```dockerfile
>         # this is a comment-line
>     RUN echo hello
> RUN echo world
> ```
>
> ```dockerfile
> # this is a comment-line
> RUN echo hello
> RUN echo world
> ```
>
> Whitespace in instruction arguments, however, isn't ignored. The following example prints `hello world` with leading whitespace as specified:
>
> ```dockerfile
> RUN echo "\
>      hello\
>      world"
> ```

## [Parser directives](#parser-directives)

Parser directives are optional, and affect the way in which subsequent lines in a Dockerfile are handled. Parser directives don't add layers to the build, and don't show up as build steps. Parser directives are written as a special type of comment in the form `# directive=value`. A single directive may only be used once.

The following parser directives are supported:

* [`syntax`](#syntax)
* [`escape`](#escape)
* [`check`](#check) (since Dockerfile v1.8.0)

Once a comment, empty line or builder instruction has been processed, BuildKit no longer looks for parser directives. Instead it treats anything formatted as a parser directive as a comment and doesn't attempt to validate if it might be a parser directive. Therefore, all parser directives must be at the top of a Dockerfile.

Parser directive keys, such as `syntax` or `check`, aren't case-sensitive, but they're lowercase by convention. Values for a directive are case-sensitive and must be written in the appropriate case for the directive. For example, `#check=skip=jsonargsrecommended` is invalid because the check name must use Pascal case, not lowercase. It's also conventional to include a blank line following any parser directives. Line continuation characters aren't supported in parser directives.

Due to these rules, the following examples are all invalid:

Invalid due to line continuation:

```dockerfile
# direc \
tive=value
```

Invalid due to appearing twice:

```dockerfile
# directive=value1
# directive=value2

FROM ImageName
```

Treated as a comment because it appears after a builder instruction:

```dockerfile
FROM ImageName
# directive=value
```

Treated as a comment because it appears after a comment that isn't a parser directive:

```dockerfile
# About my dockerfile
# directive=value
FROM ImageName
```

The following `unknowndirective` is treated as a comment because it isn't recognized. The known `syntax` directive is treated as a comment because it appears after a comment that isn't a parser directive.

```dockerfile
# unknowndirective=value
# syntax=value
```

Non line-breaking whitespace is permitted in a parser directive. Hence, the following lines are all treated identically:

```dockerfile
#directive=value
# directive =value
#	directive= value
# directive = value
#	  dIrEcTiVe=value
```

### [syntax](#syntax)

[]()

Use the `syntax` parser directive to declare the Dockerfile syntax version to use for the build. If unspecified, BuildKit uses a bundled version of the Dockerfile frontend. Declaring a syntax version lets you automatically use the latest Dockerfile version without having to upgrade BuildKit or Docker Engine, or even use a custom Dockerfile implementation.

Most users will want to set this parser directive to `docker/dockerfile:1`, which causes BuildKit to pull the latest stable version of the Dockerfile syntax before the build.

```dockerfile
# syntax=docker/dockerfile:1
```

For more information about how the parser directive works, see [Custom Dockerfile syntax](https://docs.docker.com/build/buildkit/dockerfile-frontend/).

### [escape](#escape)

```dockerfile
# escape=\
```

Or

```dockerfile
# escape=`
```

The `escape` directive sets the character used to escape characters in a Dockerfile. If not specified, the default escape character is `\`.

The escape character is used both to escape characters in a line, and to escape a newline. This allows a Dockerfile instruction to span multiple lines. Note that regardless of whether the `escape` parser directive is included in a Dockerfile, escaping is not performed in a `RUN` command, except at the end of a line.

Setting the escape character to `` ` `` is especially useful on `Windows`, where `\` is the directory path separator. `` ` `` is consistent with [Windows PowerShell](https://technet.microsoft.com/en-us/library/hh847755.aspx).

Consider the following example which would fail in a non-obvious way on Windows. The second `\` at the end of the second line would be interpreted as an escape for the newline, instead of a target of the escape from the first `\`. Similarly, the `\` at the end of the third line would, assuming it was actually handled as an instruction, cause it be treated as a line continuation. The result of this Dockerfile is that second and third lines are considered a single instruction:

```dockerfile
FROM microsoft/nanoserver
COPY testfile.txt c:\\
RUN dir c:\
```

Results in:

```console
PS E:\myproject> docker build -t cmd .

Sending build context to Docker daemon 3.072 kB
Step 1/2 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/2 : COPY testfile.txt c:\RUN dir c:
GetFileAttributesEx c:RUN: The system cannot find the file specified.
PS E:\myproject>
```

One solution to the above would be to use `/` as the target of both the `COPY` instruction, and `dir`. However, this syntax is, at best, confusing as it is not natural for paths on Windows, and at worst, error prone as not all commands on Windows support `/` as the path separator.

By adding the `escape` parser directive, the following Dockerfile succeeds as expected with the use of natural platform semantics for file paths on Windows:

```dockerfile
# escape=`

FROM microsoft/nanoserver
COPY testfile.txt c:\
RUN dir c:\
```

Results in:

```console
PS E:\myproject> docker build -t succeeds --no-cache=true .

Sending build context to Docker daemon 3.072 kB
Step 1/3 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/3 : COPY testfile.txt c:\
 ---> 96655de338de
Removing intermediate container 4db9acbb1682
Step 3/3 : RUN dir c:\
 ---> Running in a2c157f842f5
 Volume in drive C has no label.
 Volume Serial Number is 7E6D-E0F7

 Directory of c:\

10/05/2016  05:04 PM             1,894 License.txt
10/05/2016  02:22 PM    DIR          Program Files
10/05/2016  02:14 PM    DIR          Program Files (x86)
10/28/2016  11:18 AM                62 testfile.txt
10/28/2016  11:20 AM    DIR          Users
10/28/2016  11:20 AM    DIR          Windows
           2 File(s)          1,956 bytes
           4 Dir(s)  21,259,096,064 bytes free
 ---> 01c7f3bef04f
Removing intermediate container a2c157f842f5
Successfully built 01c7f3bef04f
PS E:\myproject>
```

### [check](#check)

```dockerfile
# check=skip=<checks|all>
# check=error=<boolean>
```

The `check` directive is used to configure how [build checks](https://docs.docker.com/build/checks/) are evaluated. By default, all checks are run, and failures are treated as warnings.

You can disable specific checks using `#check=skip=<check-name>`. To specify multiple checks to skip, separate them with a comma:

```dockerfile
# check=skip=JSONArgsRecommended,StageNameCasing
```

To disable all checks, use `#check=skip=all`.

By default, builds with failing build checks exit with a zero status code despite warnings. To make the build fail on warnings, set `#check=error=true`.

```dockerfile
# check=error=true
```

> Note
>
> When using the `check` directive, with `error=true` option, it is recommended to pin the [Dockerfile syntax](#syntax) to a specific version. Otherwise, your build may start to fail when new checks are added in the future versions.

To combine both the `skip` and `error` options, use a semi-colon to separate them:

```dockerfile
# check=skip=JSONArgsRecommended;error=true
```

To see all available checks, see the [build checks reference](https://docs.docker.com/reference/build-checks/). Note that the checks available depend on the Dockerfile syntax version. To make sure you're getting the most up-to-date checks, use the [`syntax`](#syntax) directive to specify the Dockerfile syntax version to the latest stable version.

## [Environment replacement](#environment-replacement)

Environment variables (declared with [the `ENV` statement](#env)) can also be used in certain instructions as variables to be interpreted by the Dockerfile. Escapes are also handled for including variable-like syntax into a statement literally.

Environment variables are notated in the Dockerfile either with `$variable_name` or `${variable_name}`. They are treated equivalently and the brace syntax is typically used to address issues with variable names with no whitespace, like `${foo}_bar`.

The `${variable_name}` syntax also supports a few of the standard `bash` modifiers as specified below:

* `${variable:-word}` indicates that if `variable` is set and non-empty then the result will be that value. If `variable` is unset or empty then `word` will be the result.
* `${variable-word}` indicates that if `variable` is set (even if empty) then the result will be that value. If `variable` is unset then `word` will be the result.
* `${variable:+word}` indicates that if `variable` is set and non-empty then `word` will be the result, otherwise the result is the empty string.
* `${variable+word}` indicates that if `variable` is set (even if empty) then `word` will be the result, otherwise the result is the empty string.

The following variable replacements are supported in a pre-release version of Dockerfile syntax, when using the `# syntax=docker/dockerfile-upstream:master` syntax directive in your Dockerfile:

* `${variable#pattern}` removes the shortest match of `pattern` from `variable`, seeking from the start of the string.

  ```bash
  str=foobarbaz echo ${str#f*b}     # arbaz
  ```

* `${variable##pattern}` removes the longest match of `pattern` from `variable`, seeking from the start of the string.

  ```bash
  str=foobarbaz echo ${str##f*b}    # az
  ```

* `${variable%pattern}` removes the shortest match of `pattern` from `variable`, seeking backwards from the end of the string.

  ```bash
  string=foobarbaz echo ${string%b*}    # foobar
  ```

* `${variable%%pattern}` removes the longest match of `pattern` from `variable`, seeking backwards from the end of the string.

  ```bash
  string=foobarbaz echo ${string%%b*}   # foo
  ```

* `${variable/pattern/replacement}` replace the first occurrence of `pattern` in `variable` with `replacement`

  ```bash
  string=foobarbaz echo ${string/ba/fo}  # fooforbaz
  ```

* `${variable//pattern/replacement}` replaces all occurrences of `pattern` in `variable` with `replacement`

  ```bash
  string=foobarbaz echo ${string//ba/fo}  # fooforfoz
  ```

In all cases, `word` can be any string, including additional environment variables.

`pattern` is a glob pattern where `?` matches any single character and `*` any number of characters (including zero). To match literal `?` and `*`, use a backslash escape: `\?` and `\*`.

You can escape whole variable names by adding a `\` before the variable: `\$foo` or `\${foo}`, for example, will translate to `$foo` and `${foo}` literals respectively.

Example (parsed representation is displayed after the `#`):

```dockerfile
FROM busybox
ENV FOO=/bar
WORKDIR ${FOO}   # WORKDIR /bar
ADD . $FOO       # ADD . /bar
COPY \$FOO /quux # COPY $FOO /quux
```

Environment variables are supported by the following list of instructions in the Dockerfile:

* `ADD`
* `COPY`
* `ENV`
* `EXPOSE`
* `FROM`
* `LABEL`
* `STOPSIGNAL`
* `USER`
* `VOLUME`
* `WORKDIR`
* `ONBUILD` (when combined with one of the supported instructions above)

You can also use environment variables with `RUN`, `CMD`, and `ENTRYPOINT` instructions, but in those cases the variable substitution is handled by the command shell, not the builder. Note that instructions using the exec form don't invoke a command shell automatically. See [Variable substitution](#variable-substitution).

Environment variable substitution use the same value for each variable throughout the entire instruction. Changing the value of a variable only takes effect in subsequent instructions. Consider the following example:

```dockerfile
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```

* The value of `def` becomes `hello`
* The value of `ghi` becomes `bye`

## [.dockerignore file](#dockerignore-file)

You can use `.dockerignore` file to exclude files and directories from the build context. For more information, see [.dockerignore file](https://docs.docker.com/build/building/context/#dockerignore-files).

## [Shell and exec form](#shell-and-exec-form)

The `RUN`, `CMD`, and `ENTRYPOINT` instructions all have two possible forms:

* `INSTRUCTION ["executable","param1","param2"]` (exec form)
* `INSTRUCTION command param1 param2` (shell form)

The exec form makes it possible to avoid shell string munging, and to invoke commands using a specific command shell, or any other executable. It uses a JSON array syntax, where each element in the array is a command, flag, or argument.

The shell form is more relaxed, and emphasizes ease of use, flexibility, and readability. The shell form automatically uses a command shell, whereas the exec form does not.

### [Exec form](#exec-form)

The exec form is parsed as a JSON array, which means that you must use double-quotes (") around words, not single-quotes (').

```dockerfile
ENTRYPOINT ["/bin/bash", "-c", "echo hello"]
```

The exec form is best used to specify an `ENTRYPOINT` instruction, combined with `CMD` for setting default arguments that can be overridden at runtime. For more information, see [ENTRYPOINT](#entrypoint).

#### [Variable substitution](#variable-substitution)

Using the exec form doesn't automatically invoke a command shell. This means that normal shell processing, such as variable substitution, doesn't happen. For example, `RUN [ "echo", "$HOME" ]` won't handle variable substitution for `$HOME`.

If you want shell processing then either use the shell form or execute a shell directly with the exec form, for example: `RUN [ "sh", "-c", "echo $HOME" ]`. When using the exec form and executing a shell directly, as in the case for the shell form, it's the shell that's doing the environment variable substitution, not the builder.

#### [Backslashes](#backslashes)

In exec form, you must escape backslashes. This is particularly relevant on Windows where the backslash is the path separator. The following line would otherwise be treated as shell form due to not being valid JSON, and fail in an unexpected way:

```dockerfile
RUN ["c:\windows\system32\tasklist.exe"]
```

The correct syntax for this example is:

```dockerfile
RUN ["c:\\windows\\system32\\tasklist.exe"]
```

### [Shell form](#shell-form)

Unlike the exec form, instructions using the shell form always use a command shell. The shell form doesn't use the JSON array format, instead it's a regular string. The shell form string lets you escape newlines using the [escape character](#escape) (backslash by default) to continue a single instruction onto the next line. This makes it easier to use with longer commands, because it lets you split them up into multiple lines. For example, consider these two lines:

```dockerfile
RUN source $HOME/.bashrc && \
echo $HOME
```

They're equivalent to the following line:

```dockerfile
RUN source $HOME/.bashrc && echo $HOME
```

You can also use heredocs with the shell form to break up supported commands.

```dockerfile
RUN <<EOF
  source $HOME/.bashrc
  echo $HOME
EOF
```

For more information about heredocs, see [Here-documents](#here-documents).

### [Use a different shell](#use-a-different-shell)

You can change the default shell using the `SHELL` command. For example:

```dockerfile
SHELL ["/bin/bash", "-c"]
RUN echo hello
```

For more information, see [SHELL](#shell).

## [FROM](#from)

```dockerfile
FROM [--platform=<platform>] <image> [AS <name>]
```

Or

```dockerfile
FROM [--platform=<platform>] <image>[:<tag>] [AS <name>]
```

Or

```dockerfile
FROM [--platform=<platform>] <image>[@<digest>] [AS <name>]
```

The `FROM` instruction initializes a new build stage and sets the [base image](https://docs.docker.com/glossary/#base-image) for subsequent instructions. As such, a valid Dockerfile must start with a `FROM` instruction. The image can be any valid image.

* `ARG` is the only instruction that may precede `FROM` in the Dockerfile. See [Understand how ARG and FROM interact](#understand-how-arg-and-from-interact).

* `FROM` can appear multiple times within a single Dockerfile to create multiple images or use one build stage as a dependency for another. Simply make a note of the last image ID output by the commit before each new `FROM` instruction. Each `FROM` instruction clears any state created by previous instructions.

* Optionally a name can be given to a new build stage by adding `AS name` to the `FROM` instruction. The name can be used in subsequent `FROM <name>`, [`COPY --from=<name>`](#copy---from), and [`RUN --mount=type=bind,from=<name>`](#run---mounttypebind) instructions to refer to the image built in this stage.

  Using a previous build stage as the base for a subsequent stage is a common pattern for sharing a common base environment:

  ```dockerfile
  FROM ubuntu AS base
  RUN apt-get update && apt-get install -y shared-tooling

  FROM base AS dev
  RUN apt-get install -y dev-tooling

  FROM base AS prod
  COPY --from=build /app /app
  ```

* The `tag` or `digest` values are optional. If you omit either of them, the builder assumes a `latest` tag by default. The builder returns an error if it can't find the `tag` value.

The optional `--platform` flag can be used to specify the platform of the image in case `FROM` references a multi-platform image. For example, `linux/amd64`, `linux/arm64`, or `windows/amd64`. By default, the target platform of the build request is used. Global build arguments can be used in the value of this flag, for example [automatic platform ARGs](#automatic-platform-args-in-the-global-scope) allow you to force a stage to native build platform (`--platform=$BUILDPLATFORM`), and use it to cross-compile to the target platform inside the stage.

### [Understand how ARG and FROM interact](#understand-how-arg-and-from-interact)

`FROM` instructions support variables that are declared by any `ARG` instructions that occur before the first `FROM`.

```dockerfile
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

An `ARG` declared before a `FROM` is outside of a build stage, so it can't be used in any instruction after a `FROM`. To use the default value of an `ARG` declared before the first `FROM` use an `ARG` instruction without a value inside of a build stage:

```dockerfile
ARG VERSION=latest
FROM busybox:$VERSION
ARG VERSION
RUN echo $VERSION > image_version
```

## [RUN](#run)

The `RUN` instruction will execute any commands to create a new layer on top of the current image. The added layer is used in the next step in the Dockerfile. `RUN` has two forms:

```dockerfile
# Shell form:
RUN [OPTIONS] <command> ...
# Exec form:
RUN [OPTIONS] [ "<command>", ... ]
```

For more information about the differences between these two forms, see [shell or exec forms](#shell-and-exec-form).

The shell form is most commonly used, and lets you break up longer instructions into multiple lines, either using newline [escapes](#escape), or with [heredocs](#here-documents):

```dockerfile
RUN <<EOF
apt-get update
apt-get install -y curl
EOF
```

The available `[OPTIONS]` for the `RUN` instruction are:

| Option                          | Minimum Dockerfile version |
| ------------------------------- | -------------------------- |
| [`--device`](#run---device)     | 1.14-labs                  |
| [`--mount`](#run---mount)       | 1.2                        |
| [`--network`](#run---network)   | 1.3                        |
| [`--security`](#run---security) | 1.20                       |

### [Cache invalidation for RUN instructions](#cache-invalidation-for-run-instructions)

The cache for `RUN` instructions isn't invalidated automatically during the next build. The cache for an instruction like `RUN apt-get dist-upgrade -y` will be reused during the next build. The cache for `RUN` instructions can be invalidated by using the `--no-cache` flag, for example `docker build --no-cache`.

See the [Dockerfile Best Practices guide](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/) for more information.

The cache for `RUN` instructions can be invalidated by [`ADD`](#add) and [`COPY`](#copy) instructions.

### [RUN --device](#run---device)

> Note
>
> Not yet available in stable syntax, use [`docker/dockerfile:1-labs`](#syntax) version. It also needs BuildKit 0.20.0 or later.

```dockerfile
RUN --device=name,[required]
```

`RUN --device` allows build to request [CDI devices](https://github.com/moby/buildkit/blob/master/docs/cdi.md) to be available to the build step.

> Warning
>
> The use of `--device` is protected by the `device` entitlement, which needs to be enabled when starting the buildkitd daemon with `--allow-insecure-entitlement device` flag or in [buildkitd config](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md), and for a build request with [`--allow device` flag](https://docs.docker.com/engine/reference/commandline/buildx_build/#allow).

The device `name` is provided by the CDI specification registered in BuildKit.

In the following example, multiple devices are registered in the CDI specification for the `vendor1.com/device` vendor.

```yaml
cdiVersion: "0.6.0"
kind: "vendor1.com/device"
devices:
  - name: foo
    containerEdits:
      env:
        - FOO=injected
  - name: bar
    annotations:
      org.mobyproject.buildkit.device.class: class1
    containerEdits:
      env:
        - BAR=injected
  - name: baz
    annotations:
      org.mobyproject.buildkit.device.class: class1
    containerEdits:
      env:
        - BAZ=injected
  - name: qux
    annotations:
      org.mobyproject.buildkit.device.class: class2
    containerEdits:
      env:
        - QUX=injected
annotations:
  org.mobyproject.buildkit.device.autoallow: true
```

The device name format is flexible and accepts various patterns to support multiple device configurations:

* `vendor1.com/device`: request the first device found for this vendor
* `vendor1.com/device=foo`: request a specific device
* `vendor1.com/device=*`: request all devices for this vendor
* `class1`: request devices by `org.mobyproject.buildkit.device.class` annotation

> Note
>
> Annotations are supported by the CDI specification since 0.6.0.

> Note
>
> To automatically allow all devices registered in the CDI specification, you can set the `org.mobyproject.buildkit.device.autoallow` annotation. You can also set this annotation for a specific device.

#### [Example: CUDA-Powered LLaMA Inference](#example-cuda-powered-llama-inference)

In this example we use the `--device` flag to run `llama.cpp` inference using an NVIDIA GPU device through CDI:

```dockerfile
# syntax=docker/dockerfile:1-labs

FROM scratch AS model
ADD https://huggingface.co/bartowski/Llama-3.2-1B-Instruct-GGUF/resolve/main/Llama-3.2-1B-Instruct-Q4_K_M.gguf /model.gguf

FROM scratch AS prompt
COPY <<EOF prompt.txt
Q: Generate  a list of 10 unique biggest countries by population in JSON with their estimated poulation in 1900 and 2024. Answer only newline formatted JSON with keys "country", "population_1900", "population_2024" with 10 items.
A:
[
    {

EOF

FROM ghcr.io/ggml-org/llama.cpp:full-cuda-b5124
RUN --device=nvidia.com/gpu=all \
    --mount=from=model,target=/models \
    --mount=from=prompt,target=/tmp \
    ./llama-cli -m /models/model.gguf -no-cnv -ngl 99 -f /tmp/prompt.txt
```

### [RUN --mount](#run---mount)

```dockerfile
RUN --mount=[type=TYPE][,option=<value>[,option=<value>]...]
```

`RUN --mount` allows you to create filesystem mounts that the build can access. This can be used to:

* Create bind mount to the host filesystem or other build stages
* Access build secrets or ssh-agent sockets
* Use a persistent package management cache to speed up your build

The supported mount types are:

| Type                                     | Description                                                                                                              |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [`bind`](#run---mounttypebind) (default) | Bind-mount context directories (read-only).                                                                              |
| [`cache`](#run---mounttypecache)         | Mount a temporary directory to cache directories for compilers and package managers.                                     |
| [`tmpfs`](#run---mounttypetmpfs)         | Mount a `tmpfs` in the build container.                                                                                  |
| [`secret`](#run---mounttypesecret)       | Allow the build container to access secure files such as private keys without baking them into the image or build cache. |
| [`ssh`](#run---mounttypessh)             | Allow the build container to access SSH keys via SSH agents, with support for passphrases.                               |

### [RUN --mount=type=bind](#run---mounttypebind)

This mount type allows binding files or directories to the build container. A bind mount is read-only by default.

| Option                                   | Description                                                                                                                                   |
| ---------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `target`, `dst`, `destination`[1](#fn:1) | Mount path.                                                                                                                                   |
| `source`                                 | Source path in the `from`. Defaults to the root of the `from`.                                                                                |
| `from`                                   | Build stage, context, or image name for the root of the source. Defaults to the build context.                                                |
| `rw`,`readwrite`                         | Allow writes on the mount. Written data will be discarded after the `RUN` instruction completes and will not be committed to the image layer. |

### [RUN --mount=type=cache](#run---mounttypecache)

This mount type allows the build container to cache directories for compilers and package managers.

| Option                                   | Description                                                                                                                                                                                                                                                                |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                                     | Optional ID to identify separate/different caches. Defaults to value of `target`.                                                                                                                                                                                          |
| `target`, `dst`, `destination`[1](#fn:1) | Mount path.                                                                                                                                                                                                                                                                |
| `ro`,`readonly`                          | Read-only if set.                                                                                                                                                                                                                                                          |
| `sharing`                                | One of `shared`, `private`, or `locked`. Defaults to `shared`. A `shared` cache mount can be used concurrently by multiple writers. `private` creates a new mount if there are multiple writers. `locked` pauses the second writer until the first one releases the mount. |
| `from`                                   | Build stage, context, or image name to use as a base of the cache mount. Defaults to empty directory.                                                                                                                                                                      |
| `source`                                 | Subpath in the `from` to mount. Defaults to the root of the `from`.                                                                                                                                                                                                        |
| `mode`                                   | File mode for new cache directory in octal. Default `0755`.                                                                                                                                                                                                                |
| `uid`                                    | User ID for new cache directory. Default `0`.                                                                                                                                                                                                                              |
| `gid`                                    | Group ID for new cache directory. Default `0`.                                                                                                                                                                                                                             |

Contents of the cache directories persists between builder invocations without invalidating the instruction cache. Cache mounts should only be used for better performance. Your build should work with any contents of the cache directory as another build may overwrite the files or GC may clean it if more storage space is needed.

#### [Example: cache Go packages](#example-cache-go-packages)

```dockerfile
# syntax=docker/dockerfile:1
FROM golang
RUN --mount=type=cache,target=/root/.cache/go-build \
  go build ...
```

#### [Example: cache apt packages](#example-cache-apt-packages)

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu
RUN rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt-get update && apt-get --no-install-recommends install -y gcc
```

Apt needs exclusive access to its data, so the caches use the option `sharing=locked`, which will make sure multiple parallel builds using the same cache mount will wait for each other and not access the same cache files at the same time. You could also use `sharing=private` if you prefer to have each build create another cache directory in this case.

### [RUN --mount=type=tmpfs](#run---mounttypetmpfs)

This mount type allows mounting `tmpfs` in the build container.

| Option                                   | Description                                           |
| ---------------------------------------- | ----------------------------------------------------- |
| `target`, `dst`, `destination`[1](#fn:1) | Mount path.                                           |
| `size`                                   | Specify an upper limit on the size of the filesystem. |

### [RUN --mount=type=secret](#run---mounttypesecret)

This mount type allows the build container to access secret values, such as tokens or private keys, without baking them into the image.

By default, the secret is mounted as a file. You can also mount the secret as an environment variable by setting the `env` option.

| Option                         | Description                                                                                                     |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| `id`                           | ID of the secret. Defaults to basename of the target path.                                                      |
| `target`, `dst`, `destination` | Mount the secret to the specified path. Defaults to `/run/secrets/` + `id` if unset and if `env` is also unset. |
| `env`                          | Mount the secret to an environment variable instead of a file, or both. (since Dockerfile v1.10.0)              |
| `required`                     | If set to `true`, the instruction errors out when the secret is unavailable. Defaults to `false`.               |
| `mode`                         | File mode for secret file in octal. Default `0400`.                                                             |
| `uid`                          | User ID for secret file. Default `0`.                                                                           |
| `gid`                          | Group ID for secret file. Default `0`.                                                                          |

#### [Example: access to S3](#example-access-to-s3)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3
RUN pip install awscli
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
  aws s3 cp s3://... ...
```

```console
$ docker buildx build --secret id=aws,src=$HOME/.aws/credentials .
```

#### [Example: Mount as environment variable](#example-mount-as-environment-variable)

The following example takes the secret `API_KEY` and mounts it as an environment variable with the same name.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=API_KEY,env=API_KEY \
    some-command --token-from-env $API_KEY
```

Assuming that the `API_KEY` environment variable is set in the build environment, you can build this with the following command:

```console
$ docker buildx build --secret id=API_KEY .
```

### [RUN --mount=type=ssh](#run---mounttypessh)

This mount type allows the build container to access SSH keys via SSH agents, with support for passphrases.

| Option                         | Description                                                                                    |
| ------------------------------ | ---------------------------------------------------------------------------------------------- |
| `id`                           | ID of SSH agent socket or key. Defaults to "default".                                          |
| `target`, `dst`, `destination` | SSH agent socket path. Defaults to `/run/buildkit/ssh_agent.${N}`.                             |
| `required`                     | If set to `true`, the instruction errors out when the key is unavailable. Defaults to `false`. |
| `mode`                         | File mode for socket in octal. Default `0600`.                                                 |
| `uid`                          | User ID for socket. Default `0`.                                                               |
| `gid`                          | Group ID for socket. Default `0`.                                                              |

#### [Example: access to GitLab](#example-access-to-gitlab)

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN apk add --no-cache openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
RUN --mount=type=ssh \
  ssh -q -T git@gitlab.com 2>&1 | tee /hello
# "Welcome to GitLab, @GITLAB_USERNAME_ASSOCIATED_WITH_SSHKEY" should be printed here
# with the type of build progress is defined as `plain`.
```

```console
$ eval $(ssh-agent)
$ ssh-add ~/.ssh/id_rsa
(Input your passphrase here)
$ docker buildx build --ssh default=$SSH_AUTH_SOCK .
```

You can also specify a path to `*.pem` file on the host directly instead of `$SSH_AUTH_SOCK`. However, pem files with passphrases are not supported.

### [RUN --network](#run---network)

```dockerfile
RUN --network=TYPE
```

`RUN --network` allows control over which networking environment the command is run in.

The supported network types are:

| Type                                         | Description                            |
| -------------------------------------------- | -------------------------------------- |
| [`default`](#run---networkdefault) (default) | Run in the default network.            |
| [`none`](#run---networknone)                 | Run with no network access.            |
| [`host`](#run---networkhost)                 | Run in the host's network environment. |

### [RUN --network=default](#run---networkdefault)

Equivalent to not supplying a flag at all, the command is run in the default network for the build.

### [RUN --network=none](#run---networknone)

The command is run with no network access (`lo` is still available, but is isolated to this process)

#### [Example: isolating external effects](#example-isolating-external-effects)

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.6
ADD mypackage.tgz wheels/
RUN --network=none pip install --find-links wheels mypackage
```

`pip` will only be able to install the packages provided in the tarfile, which can be controlled by an earlier build stage.

### [RUN --network=host](#run---networkhost)

The command is run in the host's network environment (similar to `docker build --network=host`, but on a per-instruction basis)

> Warning
>
> The use of `--network=host` is protected by the `network.host` entitlement, which needs to be enabled when starting the buildkitd daemon with `--allow-insecure-entitlement network.host` flag or in [buildkitd config](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md), and for a build request with [`--allow network.host` flag](https://docs.docker.com/engine/reference/commandline/buildx_build/#allow).

### [RUN --security](#run---security)

```dockerfile
RUN --security=<sandbox|insecure>
```

The default security mode is `sandbox`. With `--security=insecure`, the builder runs the command without sandbox in insecure mode, which allows to run flows requiring elevated privileges (e.g. containerd). This is equivalent to running `docker run --privileged`.

> Warning
>
> In order to access this feature, entitlement `security.insecure` should be enabled when starting the buildkitd daemon with `--allow-insecure-entitlement security.insecure` flag or in [buildkitd config](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md), and for a build request with [`--allow security.insecure` flag](https://docs.docker.com/engine/reference/commandline/buildx_build/#allow).

Default sandbox mode can be activated via `--security=sandbox`, but that is no-op.

#### [Example: check entitlements](#example-check-entitlements)

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu
RUN --security=insecure cat /proc/self/status | grep CapEff
```

```text
#84 0.093 CapEff:	0000003fffffffff
```

## [CMD](#cmd)

The `CMD` instruction sets the command to be executed when running a container from an image.

You can specify `CMD` instructions using [shell or exec forms](#shell-and-exec-form):

* `CMD ["executable","param1","param2"]` (exec form)
* `CMD ["param1","param2"]` (exec form, as default parameters to `ENTRYPOINT`)
* `CMD command param1 param2` (shell form)

There can only be one `CMD` instruction in a Dockerfile. If you list more than one `CMD`, only the last one takes effect.

The purpose of a `CMD` is to provide defaults for an executing container. These defaults can include an executable, or they can omit the executable, in which case you must specify an `ENTRYPOINT` instruction as well.

If you would like your container to run the same executable every time, then you should consider using `ENTRYPOINT` in combination with `CMD`. See [`ENTRYPOINT`](#entrypoint). If the user specifies arguments to `docker run` then they will override the default specified in `CMD`, but still use the default `ENTRYPOINT`.

If `CMD` is used to provide default arguments for the `ENTRYPOINT` instruction, both the `CMD` and `ENTRYPOINT` instructions should be specified in the [exec form](#exec-form).

> Note
>
> Don't confuse `RUN` with `CMD`. `RUN` actually runs a command and commits the result; `CMD` doesn't execute anything at build time, but specifies the intended command for the image.

## [LABEL](#label)

```dockerfile
LABEL <key>=<value> [<key>=<value>...]
```

The `LABEL` instruction adds metadata to an image. A `LABEL` is a key-value pair. To include spaces within a `LABEL` value, use quotes and backslashes as you would in command-line parsing. A few usage examples:

```dockerfile
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

An image can have more than one label. You can specify multiple labels on a single line. Prior to Docker 1.10, this decreased the size of the final image, but this is no longer the case. You may still choose to specify multiple labels in a single instruction, in one of the following two ways:

```dockerfile
LABEL multi.label1="value1" multi.label2="value2" other="value3"
```

```dockerfile
LABEL multi.label1="value1" \
      multi.label2="value2" \
      other="value3"
```

> Note
>
> Be sure to use double quotes and not single quotes. Particularly when you are using string interpolation (e.g. `LABEL example="foo-$ENV_VAR"`), single quotes will take the string as is without unpacking the variable's value.

Labels included in base images (images in the `FROM` line) are inherited by your image. If a label already exists but with a different value, the most-recently-applied value overrides any previously-set value.

In a multi-stage build, labels from intermediate stages are only present in the final image if the final stage is directly or indirectly based on them (via `FROM`). Labels from a stage that you only reference with `COPY --from` or `RUN --mount=from=` are not included in the output image. Labels from the base image specified in the final `FROM` instruction are always inherited.

To view an image's labels, use the `docker image inspect` command. You can use the `--format` option to show just the labels;

```console
$ docker image inspect --format='{{json .Config.Labels}}' myimage
```

```json
{
  "com.example.vendor": "ACME Incorporated",
  "com.example.label-with-value": "foo",
  "version": "1.0",
  "description": "This text illustrates that label-values can span multiple lines.",
  "multi.label1": "value1",
  "multi.label2": "value2",
  "other": "value3"
}
```

## [MAINTAINER (deprecated)](#maintainer-deprecated)

```dockerfile
MAINTAINER <name>
```

The `MAINTAINER` instruction sets the *Author* field of the generated images. The `LABEL` instruction is a much more flexible version of this and you should use it instead, as it enables setting any metadata you require, and can be viewed easily, for example with `docker inspect`. To set a label corresponding to the `MAINTAINER` field you could use:

```dockerfile
LABEL org.opencontainers.image.authors="SvenDowideit@home.org.au"
```

This will then be visible from `docker inspect` with the other labels.

## [EXPOSE](#expose)

```dockerfile
EXPOSE <port> [<port>/<protocol>...]
```

The `EXPOSE` instruction informs Docker that the container listens on the specified network ports at runtime. You can specify whether the port listens on TCP or UDP, and the default is TCP if you don't specify a protocol.

The `EXPOSE` instruction doesn't actually publish the port. It functions as a type of documentation between the person who builds the image and the person who runs the container, about which ports are intended to be published. To publish the port when running the container, use the `-p` flag on `docker run` to publish and map one or more ports, or the `-P` flag to publish all exposed ports and map them to high-order ports.

By default, `EXPOSE` assumes TCP. You can also specify UDP:

```dockerfile
EXPOSE 80/udp
```

To expose on both TCP and UDP, include two lines:

```dockerfile
EXPOSE 80/tcp
EXPOSE 80/udp
```

In this case, if you use `-P` with `docker run`, the port will be exposed once for TCP and once for UDP. Remember that `-P` uses an ephemeral high-ordered host port on the host, so TCP and UDP doesn't use the same port.

Regardless of the `EXPOSE` settings, you can override them at runtime by using the `-p` flag. For example

```console
$ docker run -p 80:80/tcp -p 80:80/udp ...
```

To set up port redirection on the host system, see [using the -P flag](https://docs.docker.com/reference/cli/docker/container/run/#publish). The `docker network` command supports creating networks for communication among containers without the need to expose or publish specific ports, because the containers connected to the network can communicate with each other over any port. For detailed information, see the [overview of this feature](https://docs.docker.com/engine/userguide/networking/).

## [ENV](#env)

```dockerfile
ENV <key>=<value> [<key>=<value>...]
```

The `ENV` instruction sets the environment variable `<key>` to the value `<value>`. This value will be in the environment for all subsequent instructions in the build stage and can be [replaced inline](#environment-replacement) in many as well. The value will be interpreted for other environment variables, so quote characters will be removed if they are not escaped. Like command line parsing, quotes and backslashes can be used to include spaces within values.

Example:

```dockerfile
ENV MY_NAME="John Doe"
ENV MY_DOG=Rex\ The\ Dog
ENV MY_CAT=fluffy
```

The `ENV` instruction allows for multiple `<key>=<value> ...` variables to be set at one time, and the example below will yield the same net results in the final image:

```dockerfile
ENV MY_NAME="John Doe" MY_DOG=Rex\ The\ Dog \
    MY_CAT=fluffy
```

The environment variables set using `ENV` will persist when a container is run from the resulting image. You can view the values using `docker inspect`, and change them using `docker run --env <key>=<value>`.

A stage inherits any environment variables that were set using `ENV` by its parent stage or any ancestor. Refer to the [multi-stage builds section](https://docs.docker.com/build/building/multi-stage/) in the manual for more information.

Environment variable persistence can cause unexpected side effects. For example, setting `ENV DEBIAN_FRONTEND=noninteractive` changes the behavior of `apt-get`, and may confuse users of your image.

If an environment variable is only needed during build, and not in the final image, consider setting a value for a single command instead:

```dockerfile
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y ...
```

Or using [`ARG`](#arg), which is not persisted in the final image:

```dockerfile
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y ...
```

> Note
>
> **Alternative syntax**
>
> The `ENV` instruction also allows an alternative syntax `ENV <key> <value>`, omitting the `=`. For example:
>
> ```dockerfile
> ENV MY_VAR my-value
> ```
>
> This syntax does not allow for multiple environment-variables to be set in a single `ENV` instruction, and can be confusing. For example, the following sets a single environment variable (`ONE`) with value `"TWO= THREE=world"`:
>
> ```dockerfile
> ENV ONE TWO= THREE=world
> ```
>
> The alternative syntax is supported for backward compatibility, but discouraged for the reasons outlined above, and may be removed in a future release.

## [ADD](#add)

ADD has two forms. The latter form is required for paths containing whitespace.

```dockerfile
ADD [OPTIONS] <src> ... <dest>
ADD [OPTIONS] ["<src>", ... "<dest>"]
```

The available `[OPTIONS]` are:

| Option                                  | Minimum Dockerfile version |
| --------------------------------------- | -------------------------- |
| [`--keep-git-dir`](#add---keep-git-dir) | 1.1                        |
| [`--checksum`](#add---checksum)         | 1.6                        |
| [`--chmod`](#add---chmod)               | 1.2                        |
| [`--chown`](#add---chown)               |                            |
| [`--link`](#add---link)                 | 1.4                        |
| [`--unpack`](#add---unpack)             | 1.17                       |
| [`--exclude`](#add---exclude)           | 1.19                       |

The `ADD` instruction copies new files or directories from `<src>` and adds them to the filesystem of the image at the path `<dest>`. Files and directories can be copied from the build context, a remote URL, or a Git repository.

The `ADD` and `COPY` instructions are functionally similar, but serve slightly different purposes. Learn more about the [differences between `ADD` and `COPY`](https://docs.docker.com/build/building/best-practices/#add-or-copy).

### [Source](#source)

You can specify multiple source files or directories with `ADD`. The last argument must always be the destination. For example, to add two files, `file1.txt` and `file2.txt`, from the build context to `/usr/src/things/` in the build container:

```dockerfile
ADD file1.txt file2.txt /usr/src/things/
```

If you specify multiple source files, either directly or using a wildcard, then the destination must be a directory (must end with a slash `/`).

To add files from a remote location, you can specify a URL or the address of a Git repository as the source. For example:

```dockerfile
ADD https://example.com/archive.zip /usr/src/things/
ADD git@github.com:user/repo.git /usr/src/things/
```

BuildKit detects the type of `<src>` and processes it accordingly.

* If `<src>` is a local file or directory, the contents of the directory are copied to the specified destination. See [Adding files from the build context](#adding-files-from-the-build-context).
* If `<src>` is a local tar archive, it is decompressed and extracted to the specified destination. See [Adding local tar archives](#adding-local-tar-archives).
* If `<src>` is a URL, the contents of the URL are downloaded and placed at the specified destination. See [Adding files from a URL](#adding-files-from-a-url).
* If `<src>` is a Git repository, the repository is cloned to the specified destination. See [Adding files from a Git repository](#adding-files-from-a-git-repository).

#### [Adding files from the build context](#adding-files-from-the-build-context)

Any relative or local path that doesn't begin with a `http://`, `https://`, or `git@` protocol prefix is considered a local file path. The local file path is relative to the build context. For example, if the build context is the current directory, `ADD file.txt /` adds the file at `./file.txt` to the root of the filesystem in the build container.

Specifying a source path with a leading slash or one that navigates outside the build context, such as `ADD ../something /something`, automatically removes any parent directory navigation (`../`). Trailing slashes in the source path are also disregarded, making `ADD something/ /something` equivalent to `ADD something /something`.

If the source is a directory, the contents of the directory are copied, including filesystem metadata. The directory itself isn't copied, only its contents. If it contains subdirectories, these are also copied, and merged with any existing directories at the destination. Any conflicts are resolved in favor of the content being added, on a file-by-file basis, except if you're trying to copy a directory onto an existing file, in which case an error is raised.

If the source is a file, the file and its metadata are copied to the destination. File permissions are preserved. If the source is a file and a directory with the same name exists at the destination, an error is raised.

If you pass a Dockerfile through stdin to the build (`docker build - < Dockerfile`), there is no build context. In this case, you can only use the `ADD` instruction to copy remote files. You can also pass a tar archive through stdin: (`docker build - < archive.tar`), the Dockerfile at the root of the archive and the rest of the archive will be used as the context of the build.

##### [Pattern matching](#pattern-matching)

For local files, each `<src>` may contain wildcards and matching will be done using Go's [filepath.Match](https://golang.org/pkg/path/filepath#Match) rules.

For example, to add all files and directories in the root of the build context ending with `.png`:

```dockerfile
ADD *.png /dest/
```

In the following example, `?` is a single-character wildcard, matching e.g. `index.js` and `index.ts`.

```dockerfile
ADD index.?s /dest/
```

When adding files or directories that contain special characters (such as `[` and `]`), you need to escape those paths following the Golang rules to prevent them from being treated as a matching pattern. For example, to add a file named `arr[0].txt`, use the following;

```dockerfile
ADD arr[[]0].txt /dest/
```

#### [Adding local tar archives](#adding-local-tar-archives)

When using a local tar archive as the source for `ADD`, and the archive is in a recognized compression format (`gzip`, `bzip2` or `xz`, or uncompressed), the archive is decompressed and extracted into the specified destination. Local tar archives are extracted by default, see the \[`ADD --unpack` flag].

When a directory is extracted, it has the same behavior as `tar -x`. The result is the union of:

1. Whatever existed at the destination path, and
2. The contents of the source tree, with conflicts resolved in favor of the content being added, on a file-by-file basis.

> Note
>
> Whether a file is identified as a recognized compression format or not is done solely based on the contents of the file, not the name of the file. For example, if an empty file happens to end with `.tar.gz` this isn't recognized as a compressed file and doesn't generate any kind of decompression error message, rather the file will simply be copied to the destination.

#### [Adding files from a URL](#adding-files-from-a-url)

In the case where source is a remote file URL, the destination will have permissions of 600. If the HTTP response contains a `Last-Modified` header, the timestamp from that header will be used to set the `mtime` on the destination file. However, like any other file processed during an `ADD`, `mtime` isn't included in the determination of whether or not the file has changed and the cache should be updated.

If remote file is a tar archive, the archive is not extracted by default. To download and extract the archive, use the \[`ADD --unpack` flag].

If the destination ends with a trailing slash, then the filename is inferred from the URL path. For example, `ADD http://example.com/foobar /` would create the file `/foobar`. The URL must have a nontrivial path so that an appropriate filename can be discovered (`http://example.com` doesn't work).

If the destination doesn't end with a trailing slash, the destination path becomes the filename of the file downloaded from the URL. For example, `ADD http://example.com/foo /bar` creates the file `/bar`.

If your URL files are protected using authentication, you need to use `RUN wget`, `RUN curl` or use another tool from within the container as the `ADD` instruction doesn't support authentication.

##### [Secrets](#secrets)

You can use the `HTTP_AUTH_HEADER_<host>` and `HTTP_AUTH_TOKEN_<host>` secrets to set credentials for remote sources. For more information, see [Build secrets](https://docs.docker.com/build/building/secrets/#http-authentication-for-add).

#### [Adding files from a Git repository](#adding-files-from-a-git-repository)

To use a Git repository as the source for `ADD`, you can reference the repository's HTTP or SSH address as the source. The repository is cloned to the specified destination in the image.

```dockerfile
ADD https://github.com/user/repo.git /mydir/
```

You can use URL fragments to specify a specific branch, tag, commit, or subdirectory. For example, to add the `docs` directory of the `v0.14.1` tag of the `buildkit` repository:

```dockerfile
ADD git@github.com:moby/buildkit.git#v0.14.1:docs /buildkit-docs
```

For more information about Git URL fragments, see [URL fragments](https://docs.docker.com/build/building/context/#url-fragments).

When adding from a Git repository, the permissions bits for files are 644. If a file in the repository has the executable bit set, it will have permissions set to 755. Directories have permissions set to 755.

When using a Git repository as the source, the repository must be accessible from the build context. To add a repository via SSH, whether public or private, you must pass an SSH key for authentication. For example, given the following Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@git.example.com:foo/bar.git /bar
```

To build this Dockerfile, pass the `--ssh` flag to the `docker build` to mount the SSH agent socket to the build. For example:

```console
$ docker build --ssh default .
```

For more information about building with secrets, see [Build secrets](https://docs.docker.com/build/building/secrets/).

### [Destination](#destination)

If the destination path begins with a forward slash, it's interpreted as an absolute path, and the source files are copied into the specified destination relative to the root of the current build stage.

```dockerfile
# create /abs/test.txt
ADD test.txt /abs/
```

Trailing slashes are significant. For example, `ADD test.txt /abs` creates a file at `/abs`, whereas `ADD test.txt /abs/` creates `/abs/test.txt`.

If the destination path doesn't begin with a leading slash, it's interpreted as relative to the working directory of the build container.

```dockerfile
WORKDIR /usr/src/app
# create /usr/src/app/rel/test.txt
ADD test.txt rel/
```

If destination doesn't exist, it's created, along with all missing directories in its path.

If the source is a file, and the destination doesn't end with a trailing slash, the source file will be written to the destination path as a file.

### [ADD --keep-git-dir](#add---keep-git-dir)

```dockerfile
ADD [--keep-git-dir=<boolean>] <src> ... <dir>
```

When `<src>` is the HTTP or SSH address of a remote Git repository, BuildKit adds the contents of the Git repository to the image excluding the `.git` directory by default.

The `--keep-git-dir=true` flag lets you preserve the `.git` directory.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD --keep-git-dir=true https://github.com/moby/buildkit.git#v0.10.1 /buildkit
```

### [ADD --checksum](#add---checksum)

```dockerfile
ADD [--checksum=<hash>] <src> ... <dir>
```

The `--checksum` flag lets you verify the checksum of a remote Git or HTTP resource:

* For Git sources, the checksum is the commit SHA. It can be the full commit SHA or match on the prefix (1 or more characters).
* For HTTP sources, the checksum is the SHA-256 content digest, formatted as `sha256:<hash>`. SHA-256 is the only supported hash algorithm.

```dockerfile
ADD --checksum=be1f38e https://github.com/moby/buildkit.git#v0.26.2 /
ADD --checksum=sha256:24454f830cdb571e2c4ad15481119c43b3cafd48dd869a9b2945d1036d1dc68d https://mirrors.edge.kernel.org/pub/linux/kernel/Historic/linux-0.01.tar.gz /
```

### [ADD --chmod](#add---chmod)

See [`COPY --chmod`](#copy---chmod).

### [ADD --chown](#add---chown)

See [`COPY --chown`](#copy---chown).

### [ADD --link](#add---link)

See [`COPY --link`](#copy---link).

### [ADD --unpack](#add---unpack)

```dockerfile
ADD [--unpack=<bool>] <src> ... <dir>
```

The `--unpack` flag controls whether or not to automatically unpack tar archives (including compressed formats like `gzip` or `bzip2`) when adding them to the image. Local tar archives are unpacked by default, whereas remote tar archives (where `src` is a URL) are downloaded without unpacking.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
# Download and unpack archive.tar.gz into /download:
ADD --unpack=true https://example.com/archive.tar.gz /download
# Add local tar without unpacking:
ADD --unpack=false my-archive.tar.gz .
```

### [ADD --exclude](#add---exclude)

See [`COPY --exclude`](#copy---exclude).

## [COPY](#copy)

COPY has two forms. The latter form is required for paths containing whitespace.

```dockerfile
COPY [OPTIONS] <src> ... <dest>
COPY [OPTIONS] ["<src>", ... "<dest>"]
```

The available `[OPTIONS]` are:

| Option                         | Minimum Dockerfile version |
| ------------------------------ | -------------------------- |
| [`--from`](#copy---from)       |                            |
| [`--chmod`](#copy---chmod)     | 1.2                        |
| [`--chown`](#copy---chown)     |                            |
| [`--link`](#copy---link)       | 1.4                        |
| [`--parents`](#copy---parents) | 1.20                       |
| [`--exclude`](#copy---exclude) | 1.19                       |

The `COPY` instruction copies new files or directories from `<src>` and adds them to the filesystem of the image at the path `<dest>`. Files and directories can be copied from the build context, build stage, named context, or an image.

The `ADD` and `COPY` instructions are functionally similar, but serve slightly different purposes. Learn more about the [differences between `ADD` and `COPY`](https://docs.docker.com/build/building/best-practices/#add-or-copy).

### [Source](#source-1)

You can specify multiple source files or directories with `COPY`. The last argument must always be the destination. For example, to copy two files, `file1.txt` and `file2.txt`, from the build context to `/usr/src/things/` in the build container:

```dockerfile
COPY file1.txt file2.txt /usr/src/things/
```

If you specify multiple source files, either directly or using a wildcard, then the destination must be a directory (must end with a slash `/`).

`COPY` accepts a flag `--from=<name>` that lets you specify the source location to be a build stage, context, or image. The following example copies files from a stage named `build`:

```dockerfile
FROM golang AS build
WORKDIR /app
RUN --mount=type=bind,target=. go build -o /myapp ./cmd

COPY --from=build /myapp /usr/bin/
```

For more information about copying from named sources, see the [`--from` flag](#copy---from).

#### [Copying from the build context](#copying-from-the-build-context)

When copying source files from the build context, paths are interpreted as relative to the root of the context.

Specifying a source path with a leading slash or one that navigates outside the build context, such as `COPY ../something /something`, automatically removes any parent directory navigation (`../`). Trailing slashes in the source path are also disregarded, making `COPY something/ /something` equivalent to `COPY something /something`.

If the source is a directory, the contents of the directory are copied, including filesystem metadata. The directory itself isn't copied, only its contents. If it contains subdirectories, these are also copied, and merged with any existing directories at the destination. Any conflicts are resolved in favor of the content being added, on a file-by-file basis, except if you're trying to copy a directory onto an existing file, in which case an error is raised.

If the source is a file, the file and its metadata are copied to the destination. File permissions are preserved. If the source is a file and a directory with the same name exists at the destination, an error is raised.

If you pass a Dockerfile through stdin to the build (`docker build - < Dockerfile`), there is no build context. In this case, you can only use the `COPY` instruction to copy files from other stages, named contexts, or images, using the [`--from` flag](#copy---from). You can also pass a tar archive through stdin: (`docker build - < archive.tar`), the Dockerfile at the root of the archive and the rest of the archive will be used as the context of the build.

When using a Git repository as the build context, the permissions bits for copied files are 644. If a file in the repository has the executable bit set, it will have permissions set to 755. Directories have permissions set to 755.

##### [Pattern matching](#pattern-matching-1)

For local files, each `<src>` may contain wildcards and matching will be done using Go's [filepath.Match](https://golang.org/pkg/path/filepath#Match) rules.

For example, to add all files and directories in the root of the build context ending with `.png`:

```dockerfile
COPY *.png /dest/
```

In the following example, `?` is a single-character wildcard, matching e.g. `index.js` and `index.ts`.

```dockerfile
COPY index.?s /dest/
```

When adding files or directories that contain special characters (such as `[` and `]`), you need to escape those paths following the Golang rules to prevent them from being treated as a matching pattern. For example, to add a file named `arr[0].txt`, use the following;

```dockerfile
COPY arr[[]0].txt /dest/
```

### [Destination](#destination-1)

If the destination path begins with a forward slash, it's interpreted as an absolute path, and the source files are copied into the specified destination relative to the root of the current build stage.

```dockerfile
# create /abs/test.txt
COPY test.txt /abs/
```

Trailing slashes are significant. For example, `COPY test.txt /abs` creates a file at `/abs`, whereas `COPY test.txt /abs/` creates `/abs/test.txt`.

If the destination path doesn't begin with a leading slash, it's interpreted as relative to the working directory of the build container.

```dockerfile
WORKDIR /usr/src/app
# create /usr/src/app/rel/test.txt
COPY test.txt rel/
```

If destination doesn't exist, it's created, along with all missing directories in its path.

If the source is a file, and the destination doesn't end with a trailing slash, the source file will be written to the destination path as a file.

### [COPY --from](#copy---from)

By default, the `COPY` instruction copies files from the build context. The `COPY --from` flag lets you copy files from an image, a build stage, or a named context instead.

```dockerfile
COPY [--from=<image|stage|context>] <src> ... <dest>
```

To copy from a build stage in a [multi-stage build](https://docs.docker.com/build/building/multi-stage/), specify the name of the stage you want to copy from. You specify stage names using the `AS` keyword with the `FROM` instruction.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS build
COPY . .
RUN apk add clang
RUN clang -o /hello hello.c

FROM scratch
COPY --from=build /hello /
```

You can also copy files directly from named contexts (specified with `--build-context <name>=<source>`) or images. The following example copies an `nginx.conf` file from the official Nginx image.

```dockerfile
COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
```

The source path of `COPY --from` is always resolved from filesystem root of the image or stage that you specify.

### [COPY --chmod](#copy---chmod)

```dockerfile
COPY [--chmod=<perms>] <src> ... <dest>
```

The `--chmod` flag supports octal notation (e.g., `755`, `644`) and symbolic notation (e.g., `+x`, `g=u`). Symbolic notation (added in Dockerfile version 1.14) is useful when octal isn't flexible enough. For example, `u=rwX,go=rX` sets directories to 755 and files to 644, while preserving the executable bit on files that already have it. (Capital `X` means "executable only if it's a directory or already executable.")

For more information about symbolic notation syntax, see the [chmod(1) manual](https://man.freebsd.org/cgi/man.cgi?chmod).

Examples using octal notation:

```dockerfile
COPY --chmod=755 app.sh /app/
COPY --chmod=644 file.txt /data/
ARG MODE=440
COPY --chmod=$MODE . .
```

Examples using symbolic notation:

```dockerfile
COPY --chmod=+x script.sh /app/
COPY --chmod=u=rwX,go=rX . /app/
COPY --chmod=g=u config/ /config/
```

The `--chmod` flag is not supported when building Windows containers.

### [COPY --chown](#copy---chown)

```dockerfile
COPY [--chown=<user>:<group>] <src> ... <dest>
```

Sets ownership of copied files. Without this flag, files are created with UID and GID of 0.

The flag accepts usernames, group names, UIDs, or GIDs in any combination. If you specify only a user, the GID is set to the same numeric value as the UID.

```dockerfile
COPY --chown=55:mygroup files* /somedir/
COPY --chown=bin files* /somedir/
COPY --chown=1 files* /somedir/
COPY --chown=10:11 files* /somedir/
COPY --chown=myuser:mygroup --chmod=644 files* /somedir/
```

When using names instead of numeric IDs, BuildKit resolves them using `/etc/passwd` and `/etc/group` in the container's root filesystem. If these files are missing or don't contain the specified names, the build fails. Numeric IDs don't require this lookup.

The `--chown` flag is not supported when building Windows containers.

### [COPY --link](#copy---link)

```dockerfile
COPY [--link[=<boolean>]] <src> ... <dest>
```

Enabling this flag in `COPY` or `ADD` commands allows you to copy files with enhanced semantics where your files remain independent on their own layer and don't get invalidated when commands on previous layers are changed.

When `--link` is used your source files are copied into an empty destination directory. That directory is turned into a layer that is linked on top of your previous state.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
COPY --link /foo /bar
```

Is equivalent of doing two builds:

```dockerfile
FROM alpine
```

and

```dockerfile
FROM scratch
COPY /foo /bar
```

and merging all the layers of both images together.

#### [Benefits of using `--link`](#benefits-of-using---link)

Use `--link` to reuse already built layers in subsequent builds with `--cache-from` even if the previous layers have changed. This is especially important for multi-stage builds where a `COPY --from` statement would previously get invalidated if any previous commands in the same stage changed, causing the need to rebuild the intermediate stages again. With `--link` the layer the previous build generated is reused and merged on top of the new layers. This also means you can easily rebase your images when the base images receive updates, without having to execute the whole build again. In backends that support it, BuildKit can do this rebase action without the need to push or pull any layers between the client and the registry. BuildKit will detect this case and only create new image manifest that contains the new layers and old layers in correct order.

The same behavior where BuildKit can avoid pulling down the base image can also happen when using `--link` and no other commands that would require access to the files in the base image. In that case BuildKit will only build the layers for the `COPY` commands and push them to the registry directly on top of the layers of the base image.

#### [Incompatibilities with `--link=false`](#incompatibilities-with---linkfalse)

When using `--link` the `COPY/ADD` commands are not allowed to read any files from the previous state. This means that if in previous state the destination directory was a path that contained a symlink, `COPY/ADD` can not follow it. In the final image the destination path created with `--link` will always be a path containing only directories.

If you don't rely on the behavior of following symlinks in the destination path, using `--link` is always recommended. The performance of `--link` is equivalent or better than the default behavior and, it creates much better conditions for cache reuse.

When copying a path into a subdirectory, `--link` will always copy from the root of the filesystem. When copying a directory, the existing mode is overridden with the new mode from the copied path. If you need a specific mode for a directory, such as the more permissive `/tmp` directory, you may need to either avoid using `--link`, unroll the copy into its base components, or use `--chmod` to ensure the overwriting directory contains the same permissions.

### [COPY --parents](#copy---parents)

```dockerfile
COPY [--parents[=<boolean>]] <src> ... <dest>
```

The `--parents` flag preserves parent directories for `src` entries. This flag defaults to `false`.

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch

COPY ./x/a.txt ./y/a.txt /no_parents/
COPY --parents ./x/a.txt ./y/a.txt /parents/

# /no_parents/a.txt
# /parents/x/a.txt
# /parents/y/a.txt
```

This behavior is similar to the [Linux `cp` utility's](https://www.man7.org/linux/man-pages/man1/cp.1.html) `--parents` or [`rsync`](https://man7.org/linux/man-pages/man1/rsync.1.html) `--relative` flag.

As with Rsync, it is possible to limit which parent directories are preserved by inserting a dot and a slash (`./`) into the source path. If such point exists, only parent directories after it will be preserved. This may be especially useful copies between stages with `--from` where the source paths need to be absolute.

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch

COPY --parents ./x/./y/*.txt /parents/

# Build context:
# ./x/y/a.txt
# ./x/y/b.txt
#
# Output:
# /parents/y/a.txt
# /parents/y/b.txt
```

The `**` wildcard matches any number of path components, including none, and can be used to recursively match files across directory levels:

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch

COPY --parents ./src/**/*.txt /parents/

# Build context:
# ./src/a.txt
# ./src/x/b.txt
# ./src/x/y/c.txt
#
# Output:
# /parents/src/a.txt
# /parents/src/x/b.txt
# /parents/src/x/y/c.txt
```

Note that, without the `--parents` flag specified, any filename collision will fail the Linux `cp` operation with an explicit error message (`cp: will not overwrite just-created './x/a.txt' with './y/a.txt'`), where the Buildkit will silently overwrite the target file at the destination.

While it is possible to preserve the directory structure for `COPY` instructions consisting of only one `src` entry, usually it is more beneficial to keep the layer count in the resulting image as low as possible. Therefore, with the `--parents` flag, the Buildkit is capable of packing multiple `COPY` instructions together, keeping the directory structure intact.

### [COPY --exclude](#copy---exclude)

```dockerfile
COPY [--exclude=<path> ...] <src> ... <dest>
```

The `--exclude` flag lets you specify a path expression for files to be excluded.

The path expression follows the same format as `<src>`, supporting wildcards and matching using Go's [filepath.Match](https://golang.org/pkg/path/filepath#Match) rules. For example, to add all files starting with "hom", excluding files with a `.txt` extension:

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch

COPY --exclude=*.txt hom* /mydir/
```

You can specify the `--exclude` option multiple times for a `COPY` instruction. Files matching any of the specified `--exclude` patterns are not copied, even if their paths match the pattern specified in `<src>`. To add all files starting with "hom", excluding files with either `.txt` or `.md` extensions:

```dockerfile
# syntax=docker/dockerfile:1
FROM scratch

COPY --exclude=*.txt --exclude=*.md hom* /mydir/
```

## [ENTRYPOINT](#entrypoint)

An `ENTRYPOINT` allows you to configure a container that will run as an executable.

`ENTRYPOINT` has two possible forms:

* The exec form, which is the preferred form:

  ```dockerfile
  ENTRYPOINT ["executable", "param1", "param2"]
  ```

* The shell form:

  ```dockerfile
  ENTRYPOINT command param1 param2
  ```

For more information about the different forms, see [Shell and exec form](#shell-and-exec-form).

The following command starts a container from the `nginx` with its default content, listening on port 80:

```console
$ docker run -i -t --rm -p 80:80 nginx
```

Command line arguments to `docker run <image>` will be appended after all elements in an exec form `ENTRYPOINT`, and will override all elements specified using `CMD`.

This allows arguments to be passed to the entry point, i.e., `docker run <image> -d` will pass the `-d` argument to the entry point. You can override the `ENTRYPOINT` instruction using the `docker run --entrypoint` flag.

The shell form of `ENTRYPOINT` ignores any `CMD` or `docker run` command line arguments. It also starts your `ENTRYPOINT` as a subcommand of `/bin/sh -c`, which does not pass signals. This means that the executable will not be the container's `PID 1`, and will not receive Unix signals. In this case, your executable doesn't receive a `SIGTERM` from `docker stop <container>`.

Only the last `ENTRYPOINT` instruction in the Dockerfile will have an effect.

### [Exec form ENTRYPOINT example](#exec-form-entrypoint-example)

You can use the exec form of `ENTRYPOINT` to set fairly stable default commands and arguments and then use `CMD` to set additional defaults that are more likely to be changed.

When combining exec form `ENTRYPOINT` with `CMD`, use the exec form of `CMD` as well. Using the shell form of `CMD` causes it to be wrapped in `/bin/sh -c`, which means the `ENTRYPOINT` receives a shell invocation as its argument rather than the bare command and parameters. See [Understand how CMD and ENTRYPOINT interact](#understand-how-cmd-and-entrypoint-interact).

```dockerfile
FROM ubuntu
ENTRYPOINT ["top", "-b"]
CMD ["-c"]
```

When you run the container, you can see that `top` is the only process:

```console
$ docker run -it --rm --name test  top -H

top - 08:25:00 up  7:27,  0 users,  load average: 0.00, 0.01, 0.05
Threads:   1 total,   1 running,   0 sleeping,   0 stopped,   0 zombie
%Cpu(s):  0.1 us,  0.1 sy,  0.0 ni, 99.7 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
KiB Mem:   2056668 total,  1616832 used,   439836 free,    99352 buffers
KiB Swap:  1441840 total,        0 used,  1441840 free.  1324440 cached Mem

  PID USER      PR  NI    VIRT    RES    SHR S %CPU %MEM     TIME+ COMMAND
    1 root      20   0   19744   2336   2080 R  0.0  0.1   0:00.04 top
```

To examine the result further, you can use `docker exec`:

```console
$ docker exec -it test ps aux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  2.6  0.1  19752  2352 ?        Ss+  08:24   0:00 top -b -H
root         7  0.0  0.1  15572  2164 ?        R+   08:25   0:00 ps aux
```

And you can gracefully request `top` to shut down using `docker stop test`.

The following Dockerfile shows using the `ENTRYPOINT` to run Apache in the foreground (i.e., as `PID 1`):

```dockerfile
FROM debian:stable
RUN apt-get update && apt-get install -y --force-yes apache2
EXPOSE 80 443
VOLUME ["/var/www", "/var/log/apache2", "/etc/apache2"]
ENTRYPOINT ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
```

If you need to write a starter script for a single executable, you can ensure that the final executable receives the Unix signals by using `exec` and `gosu` commands:

```bash
#!/usr/bin/env bash
set -e

if [ "$1" = 'postgres' ]; then
    chown -R postgres "$PGDATA"

    if [ -z "$(ls -A "$PGDATA")" ]; then
        gosu postgres initdb
    fi

    exec gosu postgres "$@"
fi

exec "$@"
```

Lastly, if you need to do some extra cleanup (or communicate with other containers) on shutdown, or are co-ordinating more than one executable, you may need to ensure that the `ENTRYPOINT` script receives the Unix signals, passes them on, and then does some more work:

```bash
#!/bin/sh
# Note: I've written this using sh so it works in the busybox container too

# USE the trap if you need to also do manual cleanup after the service is stopped,
#     or need to start multiple services in the one container
trap "echo TRAPed signal" HUP INT QUIT TERM

# start service in background here
/usr/sbin/apachectl start

echo "[hit enter key to exit] or run 'docker stop <container>'"
read

# stop service and clean up here
echo "stopping apache"
/usr/sbin/apachectl stop

echo "exited $0"
```

If you run this image with `docker run -it --rm -p 80:80 --name test apache`, you can then examine the container's processes with `docker exec`, or `docker top`, and then ask the script to stop Apache:

```console
$ docker exec -it test ps aux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.0   4448   692 ?        Ss+  00:42   0:00 /bin/sh /run.sh 123 cmd cmd2
root        19  0.0  0.2  71304  4440 ?        Ss   00:42   0:00 /usr/sbin/apache2 -k start
www-data    20  0.2  0.2 360468  6004 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
www-data    21  0.2  0.2 360468  6000 ?        Sl   00:42   0:00 /usr/sbin/apache2 -k start
root        81  0.0  0.1  15572  2140 ?        R+   00:44   0:00 ps aux

$ docker top test

PID                 USER                COMMAND
10035               root                {run.sh} /bin/sh /run.sh 123 cmd cmd2
10054               root                /usr/sbin/apache2 -k start
10055               33                  /usr/sbin/apache2 -k start
10056               33                  /usr/sbin/apache2 -k start

$ /usr/bin/time docker stop test

test
real	0m 0.27s
user	0m 0.03s
sys	0m 0.03s
```

> Note
>
> You can override the `ENTRYPOINT` setting using `--entrypoint`, but this can only set the binary to exec (no `sh -c` will be used).

### [Shell form ENTRYPOINT example](#shell-form-entrypoint-example)

You can specify a plain string for the `ENTRYPOINT` and it will execute in `/bin/sh -c`. This form will use shell processing to substitute shell environment variables, and will ignore any `CMD` or `docker run` command line arguments. To ensure that `docker stop` will signal any long running `ENTRYPOINT` executable correctly, you need to remember to start it with `exec`:

```dockerfile
FROM ubuntu
ENTRYPOINT exec top -b
```

When you run this image, you'll see the single `PID 1` process:

```console
$ docker run -it --rm --name test top

Mem: 1704520K used, 352148K free, 0K shrd, 0K buff, 140368121167873K cached
CPU:   5% usr   0% sys   0% nic  94% idle   0% io   0% irq   0% sirq
Load average: 0.08 0.03 0.05 2/98 6
  PID  PPID USER     STAT   VSZ %VSZ %CPU COMMAND
    1     0 root     R     3164   0%   0% top -b
```

Which exits cleanly on `docker stop`:

```console
$ /usr/bin/time docker stop test

test
real	0m 0.20s
user	0m 0.02s
sys	0m 0.04s
```

If you forget to add `exec` to the beginning of your `ENTRYPOINT`:

```dockerfile
FROM ubuntu
ENTRYPOINT top -b
CMD -- --ignored-param1
```

You can then run it (giving it a name for the next step):

```console
$ docker run -it --name test top --ignored-param2

top - 13:58:24 up 17 min,  0 users,  load average: 0.00, 0.00, 0.00
Tasks:   2 total,   1 running,   1 sleeping,   0 stopped,   0 zombie
%Cpu(s): 16.7 us, 33.3 sy,  0.0 ni, 50.0 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   1990.8 total,   1354.6 free,    231.4 used,    404.7 buff/cache
MiB Swap:   1024.0 total,   1024.0 free,      0.0 used.   1639.8 avail Mem

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
    1 root      20   0    2612    604    536 S   0.0   0.0   0:00.02 sh
    6 root      20   0    5956   3188   2768 R   0.0   0.2   0:00.00 top
```

You can see from the output of `top` that the specified `ENTRYPOINT` is not `PID 1`.

If you then run `docker stop test`, the container will not exit cleanly - the `stop` command will be forced to send a `SIGKILL` after the timeout:

```console
$ docker exec -it test ps waux

USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.4  0.0   2612   604 pts/0    Ss+  13:58   0:00 /bin/sh -c top -b --ignored-param2
root         6  0.0  0.1   5956  3188 pts/0    S+   13:58   0:00 top -b
root         7  0.0  0.1   5884  2816 pts/1    Rs+  13:58   0:00 ps waux

$ /usr/bin/time docker stop test

test
real	0m 10.19s
user	0m 0.04s
sys	0m 0.03s
```

### [Understand how CMD and ENTRYPOINT interact](#understand-how-cmd-and-entrypoint-interact)

Both `CMD` and `ENTRYPOINT` instructions define what command gets executed when running a container. There are few rules that describe their co-operation.

1. Dockerfile should specify at least one of `CMD` or `ENTRYPOINT` commands.

2. `ENTRYPOINT` should be defined when using the container as an executable.

3. `CMD` should be used as a way of defining default arguments for an `ENTRYPOINT` command or for executing an ad-hoc command in a container.

4. `CMD` will be overridden when running the container with alternative arguments.

The table below shows what command is executed for different `ENTRYPOINT` / `CMD` combinations:

|                                   | No ENTRYPOINT                | ENTRYPOINT exec\_entry p1\_entry | ENTRYPOINT \["exec\_entry", "p1\_entry"]           |
| --------------------------------- | ---------------------------- | -------------------------------- | -------------------------------------------------- |
| **No CMD**                        | error, not allowed           | /bin/sh -c exec\_entry p1\_entry | exec\_entry p1\_entry                              |
| **CMD \["exec\_cmd", "p1\_cmd"]** | exec\_cmd p1\_cmd            | /bin/sh -c exec\_entry p1\_entry | exec\_entry p1\_entry exec\_cmd p1\_cmd            |
| **CMD exec\_cmd p1\_cmd**         | /bin/sh -c exec\_cmd p1\_cmd | /bin/sh -c exec\_entry p1\_entry | exec\_entry p1\_entry /bin/sh -c exec\_cmd p1\_cmd |

> Note
>
> If `CMD` is defined from the base image, setting `ENTRYPOINT` will reset `CMD` to an empty value. In this scenario, `CMD` must be defined in the current image to have a value.

## [VOLUME](#volume)

```dockerfile
VOLUME ["/data"]
```

The `VOLUME` instruction creates a mount point with the specified name and marks it as holding externally mounted volumes from native host or other containers. The value can be a JSON array, `VOLUME ["/var/log/"]`, or a plain string with multiple arguments, such as `VOLUME /var/log` or `VOLUME /var/log /var/db`. For more information/examples and mounting instructions via the Docker client, refer to [*Share Directories via Volumes*](https://docs.docker.com/storage/volumes/) documentation.

The `docker run` command initializes the newly created volume with any data that exists at the specified location within the base image. For example, consider the following Dockerfile snippet:

```dockerfile
FROM ubuntu
RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol
```

This Dockerfile results in an image that causes `docker run` to create a new mount point at `/myvol` and copy the `greeting` file into the newly created volume.

### [Notes about specifying volumes](#notes-about-specifying-volumes)

Keep the following things in mind about volumes in the Dockerfile.

* **Volumes on Windows-based containers**: When using Windows-based containers, the destination of a volume inside the container must be one of:

  * a non-existing or empty directory
  * a drive other than `C:`

* **Changing the volume from within the Dockerfile**: If any build steps change the data within the volume after it has been declared, those changes will be discarded when using the legacy builder. When using Buildkit, the changes will instead be kept.

* **JSON formatting**: The list is parsed as a JSON array. You must enclose words with double quotes (`"`) rather than single quotes (`'`).

* **The host directory is declared at container run-time**: The host directory (the mountpoint) is, by its nature, host-dependent. This is to preserve image portability, since a given host directory can't be guaranteed to be available on all hosts. For this reason, you can't mount a host directory from within the Dockerfile. The `VOLUME` instruction does not support specifying a `host-dir` parameter. You must specify the mountpoint when you create or run the container.

## [USER](#user)

```dockerfile
USER <user>[:<group>]
```

or

```dockerfile
USER UID[:<GID>]
```

The `USER` instruction sets the user name (or UID) and optionally the user group (or GID) to use as the default user and group for the remainder of the current stage. The specified user is used for `RUN` instructions and at runtime runs the relevant `ENTRYPOINT` and `CMD` commands.

> Note that when specifying a group for the user, the user will have *only* the specified group membership. Any other configured group memberships will be ignored.

> Warning
>
> When the user doesn't have a primary group then the image (or the next instructions) will be run with the `root` group.
>
> On Windows, the user must be created first if it's not a built-in account. This can be done with the `net user` command called as part of a Dockerfile.

```dockerfile
FROM microsoft/windowsservercore
# Create Windows user in the container
RUN net user /add patrick
# Set it for subsequent commands
USER patrick
```

## [WORKDIR](#workdir)

```dockerfile
WORKDIR /path/to/workdir
```

The `WORKDIR` instruction sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY` and `ADD` instructions that follow it in the Dockerfile. If the `WORKDIR` doesn't exist, it will be created even if it's not used in any subsequent Dockerfile instruction.

The `WORKDIR` instruction can be used multiple times in a Dockerfile. If a relative path is provided, it will be relative to the path of the previous `WORKDIR` instruction. For example:

```dockerfile
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

The output of the final `pwd` command in this Dockerfile would be `/a/b/c`.

The `WORKDIR` instruction can resolve environment variables previously set using `ENV`. You can only use environment variables explicitly set in the Dockerfile. For example:

```dockerfile
ENV DIRPATH=/path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
```

The output of the final `pwd` command in this Dockerfile would be `/path/$DIRNAME`

If not specified, the default working directory is `/`. In practice, if you aren't building a Dockerfile from scratch (`FROM scratch`), the `WORKDIR` may likely be set by the base image you're using.

Therefore, to avoid unintended operations in unknown directories, it's best practice to set your `WORKDIR` explicitly.

## [ARG](#arg)

```dockerfile
ARG <name>[=<default value>] [<name>[=<default value>]...]
```

The `ARG` instruction defines a variable that users can pass at build time to the builder with the `docker build` command using the `--build-arg <varname>=<value>` flag. This variable can be used in subsequent instructions such as `FROM`, `ENV`, `WORKDIR`, and others using the `${VAR}` or `$VAR` template syntax. It is also passed to all subsequent `RUN` instructions as a build-time environment variable.

Unlike `ENV`, an `ARG` variable is not embedded in the image and is not available in the final container.

> Warning
>
> It isn't recommended to use build arguments for passing secrets such as user credentials, API tokens, etc. Build arguments are visible in the `docker history` command and in `max` mode provenance attestations, which are attached to the image by default if you use the Buildx GitHub Actions and your GitHub repository is public.
>
> Refer to the [`RUN --mount=type=secret`](#run---mounttypesecret) section to learn about secure ways to use secrets when building images.

A Dockerfile may include one or more `ARG` instructions. For example, the following is a valid Dockerfile:

```dockerfile
FROM busybox
ARG user1
ARG buildno
# ...
```

### [Default values](#default-values)

An `ARG` instruction can optionally include a default value:

```dockerfile
FROM busybox
ARG user1=someuser
ARG buildno=1
# ...
```

If an `ARG` instruction has a default value and if there is no value passed at build-time, the builder uses the default.

### [Scope](#scope)

An `ARG` variable comes into effect from the line on which it is declared in the Dockerfile. For example, consider this Dockerfile:

```dockerfile
FROM busybox
USER ${username:-some_user}
ARG username
USER $username
# ...
```

A user builds this file by calling:

```console
$ docker build --build-arg username=what_user .
```

* The `USER` instruction on line 2 evaluates to the `some_user` fallback, because the `username` variable is not yet declared.
* The `username` variable is declared on line 3, and available for reference in Dockerfile instruction from that point onwards.
* The `USER` instruction on line 4 evaluates to `what_user`, since at that point the `username` argument has a value of `what_user` which was passed on the command line. Prior to its definition by an `ARG` instruction, any use of a variable results in an empty string.

An `ARG` variable declared within a build stage is automatically inherited by other stages based on that stage. Unrelated build stages do not have access to the variable. To use an argument in multiple distinct stages, each stage must include the `ARG` instruction, or they must both be based on a shared base stage in the same Dockerfile where the variable is declared.

For more information, refer to [variable scoping](https://docs.docker.com/build/building/variables/#scoping).

### [Using ARG variables](#using-arg-variables)

You can use an `ARG` or an `ENV` instruction to specify variables that are available to the `RUN` instruction. Environment variables defined using the `ENV` instruction always override an `ARG` instruction of the same name. Consider this Dockerfile with an `ENV` and `ARG` instruction.

```dockerfile
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=v1.0.0
RUN echo $CONT_IMG_VER
```

Then, assume this image is built with this command:

```console
$ docker build --build-arg CONT_IMG_VER=v2.0.1 .
```

In this case, the `RUN` instruction uses `v1.0.0` instead of the `ARG` setting passed by the user:`v2.0.1` This behavior is similar to a shell script where a locally scoped variable overrides the variables passed as arguments or inherited from environment, from its point of definition.

Using the example above but a different `ENV` specification you can create more useful interactions between `ARG` and `ENV` instructions:

```dockerfile
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=${CONT_IMG_VER:-v1.0.0}
RUN echo $CONT_IMG_VER
```

Unlike an `ARG` instruction, `ENV` values are always persisted in the built image. Consider a docker build without the `--build-arg` flag:

```console
$ docker build .
```

Using this Dockerfile example, `CONT_IMG_VER` is still persisted in the image but its value would be `v1.0.0` as it is the default set in line 3 by the `ENV` instruction.

The variable expansion technique in this example allows you to pass arguments from the command line and persist them in the final image by leveraging the `ENV` instruction. Variable expansion is only supported for [a limited set of Dockerfile instructions.](#environment-replacement)

### [Predefined ARGs](#predefined-args)

Docker has a set of predefined `ARG` variables that you can use without a corresponding `ARG` instruction in the Dockerfile.

* `HTTP_PROXY`
* `http_proxy`
* `HTTPS_PROXY`
* `https_proxy`
* `FTP_PROXY`
* `ftp_proxy`
* `NO_PROXY`
* `no_proxy`
* `ALL_PROXY`
* `all_proxy`

To use these, pass them on the command line using the `--build-arg` flag, for example:

```console
$ docker build --build-arg HTTPS_PROXY=https://my-proxy.example.com .
```

By default, these pre-defined variables are excluded from the output of `docker history`. Excluding them reduces the risk of accidentally leaking sensitive authentication information in an `HTTP_PROXY` variable.

For example, consider building the following Dockerfile using `--build-arg HTTP_PROXY=http://user:pass@proxy.lon.example.com`

```dockerfile
FROM ubuntu
RUN echo "Hello World"
```

In this case, the value of the `HTTP_PROXY` variable is not available in the `docker history` and is not cached. If you were to change location, and your proxy server changed to `http://user:pass@proxy.sfo.example.com`, a subsequent build does not result in a cache miss.

If you need to override this behaviour then you may do so by adding an `ARG` statement in the Dockerfile as follows:

```dockerfile
FROM ubuntu
ARG HTTP_PROXY
RUN echo "Hello World"
```

When building this Dockerfile, the `HTTP_PROXY` is preserved in the `docker history`, and changing its value invalidates the build cache.

### [Automatic platform ARGs in the global scope](#automatic-platform-args-in-the-global-scope)

This feature is only available when using the [BuildKit](https://docs.docker.com/build/buildkit/) backend.

BuildKit supports a predefined set of `ARG` variables with information on the platform of the node performing the build (build platform) and on the platform of the resulting image (target platform). The target platform can be specified with the `--platform` flag on `docker build`.

The following `ARG` variables are set automatically:

* `TARGETPLATFORM` - platform of the build result. Eg `linux/amd64`, `linux/arm/v7`, `windows/amd64`.
* `TARGETOS` - OS component of TARGETPLATFORM
* `TARGETARCH` - architecture component of TARGETPLATFORM
* `TARGETVARIANT` - variant component of TARGETPLATFORM
* `BUILDPLATFORM` - platform of the node performing the build.
* `BUILDOS` - OS component of BUILDPLATFORM
* `BUILDARCH` - architecture component of BUILDPLATFORM
* `BUILDVARIANT` - variant component of BUILDPLATFORM

These arguments are defined in the global scope so are not automatically available inside build stages or for your `RUN` commands. To expose one of these arguments inside the build stage redefine it without value.

For example:

```dockerfile
FROM alpine
ARG TARGETPLATFORM
RUN echo "I'm building for $TARGETPLATFORM"
```

### [BuildKit built-in build args](#buildkit-built-in-build-args)

| Arg                               | Type   | Description                                                                                                                                                                                                      |
| --------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `BUILDKIT_BUILD_NAME`             | String | Override the build name shown in [`buildx history` command](https://docs.docker.com/reference/cli/docker/buildx/history/) and [Docker Desktop Builds view](https://docs.docker.com/desktop/use-desktop/builds/). |
| `BUILDKIT_CACHE_MOUNT_NS`         | String | Set optional cache ID namespace.                                                                                                                                                                                 |
| `BUILDKIT_CONTEXT_KEEP_GIT_DIR`   | Bool   | Trigger Git context to keep the `.git` directory.                                                                                                                                                                |
| `BUILDKIT_INLINE_CACHE`[2](#fn:2) | Bool   | Inline cache metadata to image config or not.                                                                                                                                                                    |
| `BUILDKIT_MULTI_PLATFORM`         | Bool   | Opt into deterministic output regardless of multi-platform output or not.                                                                                                                                        |
| `BUILDKIT_SANDBOX_HOSTNAME`       | String | Set the hostname (default `buildkitsandbox`)                                                                                                                                                                     |
| `BUILDKIT_SYNTAX`                 | String | Set frontend image. Set to `dockerfile.v0` to ignore the Dockerfile `# syntax=` directive and use the built-in frontend instead.                                                                                 |
| `SOURCE_DATE_EPOCH`               | Int    | Set the Unix timestamp for created image and layers. More info from [reproducible builds](https://reproducible-builds.org/docs/source-date-epoch/). Supported since Dockerfile 1.5, BuildKit 0.11                |

#### [Example: keep `.git` dir](#example-keep-git-dir)

When using a Git context, `.git` dir is not kept on checkouts. It can be useful to keep it around if you want to retrieve git information during your build:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
WORKDIR /src
RUN --mount=target=. \
  make REVISION=$(git rev-parse HEAD) build
```

```console
$ docker build --build-arg BUILDKIT_CONTEXT_KEEP_GIT_DIR=1 https://github.com/user/repo.git#main
```

### [Impact on build caching](#impact-on-build-caching)

`ARG` variables are not persisted into the built image as `ENV` variables are. However, `ARG` variables do impact the build cache in similar ways. If a Dockerfile defines an `ARG` variable whose value is different from a previous build, then a "cache miss" occurs upon its first usage, not its definition. In particular, all `RUN` instructions following an `ARG` instruction use the `ARG` variable implicitly (as an environment variable), thus can cause a cache miss. All predefined `ARG` variables are exempt from caching unless there is a matching `ARG` statement in the Dockerfile.

For example, consider these two Dockerfile:

```dockerfile
FROM ubuntu
ARG CONT_IMG_VER
RUN echo $CONT_IMG_VER
```

```dockerfile
FROM ubuntu
ARG CONT_IMG_VER
RUN echo hello
```

If you specify `--build-arg CONT_IMG_VER=<value>` on the command line, in both cases, the specification on line 2 doesn't cause a cache miss; line 3 does cause a cache miss. `ARG CONT_IMG_VER` causes the `RUN` line to be identified as the same as running `CONT_IMG_VER=<value> echo hello`, so if the `<value>` changes, you get a cache miss.

Consider another example under the same command line:

```dockerfile
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=$CONT_IMG_VER
RUN echo $CONT_IMG_VER
```

In this example, the cache miss occurs on line 3. The miss happens because the variable's value in the `ENV` references the `ARG` variable and that variable is changed through the command line. In this example, the `ENV` command causes the image to include the value.

If an `ENV` instruction overrides an `ARG` instruction of the same name, like this Dockerfile:

```dockerfile
FROM ubuntu
ARG CONT_IMG_VER
ENV CONT_IMG_VER=hello
RUN echo $CONT_IMG_VER
```

Line 3 doesn't cause a cache miss because the value of `CONT_IMG_VER` is a constant (`hello`). As a result, the environment variables and values used on the `RUN` (line 4) doesn't change between builds.

## [ONBUILD](#onbuild)

```dockerfile
ONBUILD INSTRUCTION
```

The `ONBUILD` instruction adds to the image a trigger instruction to be executed at a later time, when the image is used as the base for another build. The trigger will be executed in the context of the downstream build, as if it had been inserted immediately after the `FROM` instruction in the downstream Dockerfile.

This is useful if you are building an image which will be used as a base to build other images, for example an application build environment or a daemon which may be customized with user-specific configuration.

For example, if your image is a reusable Python application builder, it will require application source code to be added in a particular directory, and it might require a build script to be called after that. You can't just call `ADD` and `RUN` now, because you don't yet have access to the application source code, and it will be different for each application build. You could simply provide application developers with a boilerplate Dockerfile to copy-paste into their application, but that's inefficient, error-prone and difficult to update because it mixes with application-specific code.

The solution is to use `ONBUILD` to register advance instructions to run later, during the next build stage.

Here's how it works:

1. When it encounters an `ONBUILD` instruction, the builder adds a trigger to the metadata of the image being built. The instruction doesn't otherwise affect the current build.
2. At the end of the build, a list of all triggers is stored in the image manifest, under the key `OnBuild`. They can be inspected with the `docker inspect` command.
3. Later the image may be used as a base for a new build, using the `FROM` instruction. As part of processing the `FROM` instruction, the downstream builder looks for `ONBUILD` triggers, and executes them in the same order they were registered. If any of the triggers fail, the `FROM` instruction is aborted which in turn causes the build to fail. If all triggers succeed, the `FROM` instruction completes and the build continues as usual.
4. Triggers are cleared from the final image after being executed. In other words they aren't inherited by "grand-children" builds.

For example you might add something like this:

```dockerfile
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
```

### [Copy or mount from stage, image, or context](#copy-or-mount-from-stage-image-or-context)

As of Dockerfile syntax 1.11, you can use `ONBUILD` with instructions that copy or mount files from other stages, images, or build contexts. For example:

```dockerfile
# syntax=docker/dockerfile:1.11
FROM alpine AS baseimage
ONBUILD COPY --from=build /usr/bin/app /app
ONBUILD RUN --mount=from=config,target=/opt/appconfig ...
```

If the source of `from` is a build stage, the stage must be defined in the Dockerfile where `ONBUILD` gets triggered. If it's a named context, that context must be passed to the downstream build.

### [ONBUILD limitations](#onbuild-limitations)

* Chaining `ONBUILD` instructions using `ONBUILD ONBUILD` isn't allowed.
* The `ONBUILD` instruction may not trigger `FROM` or `MAINTAINER` instructions.

## [STOPSIGNAL](#stopsignal)

```dockerfile
STOPSIGNAL signal
```

The `STOPSIGNAL` instruction sets the system call signal that will be sent to the container to exit. This signal can be a signal name in the format `SIG<NAME>`, for instance `SIGKILL`, or an unsigned number that matches a position in the kernel's syscall table, for instance `9`. The default is `SIGTERM` if not defined.

`STOPSIGNAL` applies to the signal sent by `docker stop` (and by the Docker daemon when stopping a container). It does not affect signals sent by keyboard shortcuts such as Ctrl+C, which sends `SIGINT` directly to the process regardless of the `STOPSIGNAL` setting.

The image's default stopsignal can be overridden per container, using the `--stop-signal` flag on `docker run` and `docker create`.

## [HEALTHCHECK](#healthcheck)

The `HEALTHCHECK` instruction has two forms:

* `HEALTHCHECK [OPTIONS] CMD command` (check container health by running a command inside the container)
* `HEALTHCHECK NONE` (disable any healthcheck inherited from the base image)

The `HEALTHCHECK` instruction tells Docker how to test a container to check that it's still working. This can detect cases such as a web server stuck in an infinite loop and unable to handle new connections, even though the server process is still running.

When a container has a healthcheck specified, it has a health status in addition to its normal status. This status is initially `starting`. Whenever a health check passes, it becomes `healthy` (whatever state it was previously in). After a certain number of consecutive failures, it becomes `unhealthy`.

The options that can appear before `CMD` are:

* `--interval=DURATION` (default: `30s`)
* `--timeout=DURATION` (default: `30s`)
* `--start-period=DURATION` (default: `0s`)
* `--start-interval=DURATION` (default: `5s`)
* `--retries=N` (default: `3`)

The health check will first run **interval** seconds after the container is started, and then again **interval** seconds after each previous check completes. During the **start period**, health checks run at **start interval** frequency instead.

If a single run of the check takes longer than **timeout** seconds then the check is considered to have failed. The process performing the check is abruptly stopped with a `SIGKILL`.

It takes **retries** consecutive failures of the health check for the container to be considered `unhealthy`.

**start period** provides initialization time for containers that need time to bootstrap. Probe failure during that period will not be counted towards the maximum number of retries. However, if a health check succeeds during the start period, the container is considered started and all consecutive failures will be counted towards the maximum number of retries.

**start interval** is the time between health checks during the start period. This option requires Docker Engine version 25.0 or later.

There can only be one `HEALTHCHECK` instruction in a Dockerfile. If you list more than one then only the last `HEALTHCHECK` will take effect.

The command after the `CMD` keyword can be either a shell command (e.g. `HEALTHCHECK CMD /bin/check-running`) or an exec array (as with other Dockerfile commands; see e.g. `ENTRYPOINT` for details).

The command's exit status indicates the health status of the container. The possible values are:

* 0: success - the container is healthy and ready for use
* 1: unhealthy - the container isn't working correctly
* 2: reserved - don't use this exit code

For example, to check every five minutes or so that a web-server is able to serve the site's main page within three seconds:

```dockerfile
HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost/ || exit 1
```

To help debug failing probes, any output text (UTF-8 encoded) that the command writes on stdout or stderr will be stored in the health status and can be queried with `docker inspect`. Such output should be kept short (only the first 4096 bytes are stored currently).

When the health status of a container changes, a `health_status` event is generated with the new status.

## [SHELL](#shell)

```dockerfile
SHELL ["executable", "parameters"]
```

The `SHELL` instruction allows the default shell used for the shell form of commands to be overridden. The default shell on Linux is `["/bin/sh", "-c"]`, and on Windows is `["cmd", "/S", "/C"]`. The `SHELL` instruction must be written in JSON form in a Dockerfile.

The `SHELL` instruction is particularly useful on Windows where there are two commonly used and quite different native shells: `cmd` and `powershell`, as well as alternate shells available including `sh`.

The `SHELL` instruction can appear multiple times. Each `SHELL` instruction overrides all previous `SHELL` instructions, and affects all subsequent instructions. For example:

```dockerfile
FROM microsoft/windowsservercore

# Executed as cmd /S /C echo default
RUN echo default

# Executed as cmd /S /C powershell -command Write-Host default
RUN powershell -command Write-Host default

# Executed as powershell -command Write-Host hello
SHELL ["powershell", "-command"]
RUN Write-Host hello

# Executed as cmd /S /C echo hello
SHELL ["cmd", "/S", "/C"]
RUN echo hello
```

The following instructions can be affected by the `SHELL` instruction when the shell form of them is used in a Dockerfile: `RUN`, `CMD` and `ENTRYPOINT`.

The following example is a common pattern found on Windows which can be streamlined by using the `SHELL` instruction:

```dockerfile
RUN powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
```

The command invoked by the builder will be:

```powershell
cmd /S /C powershell -command Execute-MyCmdlet -param1 "c:\foo.txt"
```

This is inefficient for two reasons. First, there is an unnecessary `cmd.exe` command processor (aka shell) being invoked. Second, each `RUN` instruction in the shell form requires an extra `powershell -command` prefixing the command.

To make this more efficient, one of two mechanisms can be employed. One is to use the JSON form of the `RUN` command such as:

```dockerfile
RUN ["powershell", "-command", "Execute-MyCmdlet", "-param1 \"c:\\foo.txt\""]
```

While the JSON form is unambiguous and does not use the unnecessary `cmd.exe`, it does require more verbosity through double-quoting and escaping. The alternate mechanism is to use the `SHELL` instruction and the shell form, making a more natural syntax for Windows users, especially when combined with the `escape` parser directive:

```dockerfile
# escape=`

FROM microsoft/nanoserver
SHELL ["powershell","-command"]
RUN New-Item -ItemType Directory C:\Example
ADD Execute-MyCmdlet.ps1 c:\example\
RUN c:\example\Execute-MyCmdlet -sample 'hello world'
```

Resulting in:

```console
PS E:\myproject> docker build -t shell .

Sending build context to Docker daemon 4.096 kB
Step 1/5 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/5 : SHELL powershell -command
 ---> Running in 6fcdb6855ae2
 ---> 6331462d4300
Removing intermediate container 6fcdb6855ae2
Step 3/5 : RUN New-Item -ItemType Directory C:\Example
 ---> Running in d0eef8386e97


    Directory: C:\


Mode         LastWriteTime              Length Name
----         -------------              ------ ----
d-----       10/28/2016  11:26 AM              Example


 ---> 3f2fbf1395d9
Removing intermediate container d0eef8386e97
Step 4/5 : ADD Execute-MyCmdlet.ps1 c:\example\
 ---> a955b2621c31
Removing intermediate container b825593d39fc
Step 5/5 : RUN c:\example\Execute-MyCmdlet 'hello world'
 ---> Running in be6d8e63fe75
hello world
 ---> 8e559e9bf424
Removing intermediate container be6d8e63fe75
Successfully built 8e559e9bf424
PS E:\myproject>
```

The `SHELL` instruction could also be used to modify the way in which a shell operates. For example, using `SHELL cmd /S /C /V:ON|OFF` on Windows, delayed environment variable expansion semantics could be modified.

The `SHELL` instruction can also be used on Linux should an alternate shell be required such as `zsh`, `csh`, `tcsh` and others.

## [Here-Documents](#here-documents)

Here-documents allow redirection of subsequent Dockerfile lines to the input of `RUN` or `COPY` commands. If such command contains a [here-document](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_07_04) the Dockerfile considers the next lines until the line only containing a here-doc delimiter as part of the same command.

### [Example: Running a multi-line script](#example-running-a-multi-line-script)

```dockerfile
# syntax=docker/dockerfile:1
FROM debian
RUN <<EOT bash
  set -ex
  apt-get update
  apt-get install -y vim
EOT
```

If the command only contains a here-document, its contents is evaluated with the default shell.

```dockerfile
# syntax=docker/dockerfile:1
FROM debian
RUN <<EOT
  mkdir -p foo/bar
EOT
```

Alternatively, shebang header can be used to define an interpreter.

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.6
RUN <<EOT
#!/usr/bin/env python
print("hello world")
EOT
```

More complex examples may use multiple here-documents.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN <<FILE1 cat > file1 && <<FILE2 cat > file2
I am
first
FILE1
I am
second
FILE2
```

### [Example: Creating inline files](#example-creating-inline-files)

With `COPY` instructions, you can replace the source parameter with a here-doc indicator to write the contents of the here-document directly to a file. The following example creates a `greeting.txt` file containing `hello world` using a `COPY` instruction.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
COPY <<EOF greeting.txt
hello world
EOF
```

Regular here-doc [variable expansion and tab stripping rules](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_07_04) apply. The following example shows a small Dockerfile that creates a `hello.sh` script file using a `COPY` instruction with a here-document.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ARG FOO=bar
COPY <<-EOT /script.sh
  echo "hello ${FOO}"
EOT
ENTRYPOINT ash /script.sh
```

In this case, file script prints "hello bar", because the variable is expanded when the `COPY` instruction gets executed.

```console
$ docker build -t heredoc .
$ docker run heredoc
hello bar
```

If instead you were to quote any part of the here-document word `EOT`, the variable would not be expanded at build-time.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ARG FOO=bar
COPY <<-"EOT" /script.sh
  echo "hello ${FOO}"
EOT
ENTRYPOINT ash /script.sh
```

Note that `ARG FOO=bar` is excessive here, and can be removed. The variable gets interpreted at runtime, when the script is invoked:

```console
$ docker build -t heredoc .
$ docker run -e FOO=world heredoc
hello world
```

## [Dockerfile examples](#dockerfile-examples)

For examples of Dockerfiles, refer to:

* The [building best practices page](https://docs.docker.com/build/building/best-practices/)
* The ["get started" tutorials](https://docs.docker.com/get-started/)
* The [language-specific getting started guides](https://docs.docker.com/guides/language/)

***

1. Value required [↩︎](#fnref:1) [↩︎](#fnref1:1) [↩︎](#fnref2:1)

2. For Docker-integrated [BuildKit](https://docs.docker.com/build/buildkit/#getting-started) and `docker buildx build` [↩︎](#fnref:2)

----
url: https://docs.docker.com/desktop/settings-and-maintenance/settings/
----

# Change your Docker Desktop settings

***

Table of contents

***

Customize Docker Desktop behavior and optimize performance and resource usage with Docker Desktop's settings.

To open **Settings** either:

* Select the Docker menu and then **Settings**
* Select the **Settings** icon from the Docker Desktop Dashboard.

You can also locate the `settings-store.json` file at:

* Mac: `~/Library/Group\ Containers/group.com.docker/settings-store.json`
* Windows: `C:\Users\[USERNAME]\AppData\Roaming\Docker\settings-store.json`
* Linux: `~/.docker/desktop/settings-store.json`

For information on enforcing settings at an organization level, see [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/).

## [General](#general)

Configure startup behavior, UI appearance, terminal preferences, and feature defaults for Docker Desktop.

| Setting                                                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                 | Default                  | Platform                       | Notes                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Start Docker Desktop when you sign in to your computer**   | Automatically start Docker Desktop when you sign in to your machine.                                                                                                                                                                                                                                                                                                                                                                        | Disabled                 | All                            | Recommended for frequent users.                                                                                                                                                                                                                                                                                                                |
| **Open Docker Dashboard when Docker Desktop starts**         | Automatically open the dashboard when starting Docker Desktop.                                                                                                                                                                                                                                                                                                                                                                              | Disabled                 | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Choose theme for Docker Desktop**                          | Apply a **Light** or **Dark** theme to Docker Desktop.                                                                                                                                                                                                                                                                                                                                                                                      | **Use system settings**. | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Configure shell completions**                              | Edits your shell configuration to enable word completion for commands, flags, and Docker objects when you press `<Tab>` in your terminal. For more information, see [Completion](https://docs.docker.com/engine/cli/completion/).                                                                                                                                                                                                           | Disabled                 | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Choose container terminal**                                | Sets which terminal opens when you select a container terminal. Use the integrated terminal to run commands in a running container from the Dashboard. For more information, see [Explore containers](https://docs.docker.com/desktop/use-desktop/container/).                                                                                                                                                                              | Disabled                 | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Enable Docker terminal**.                                  | Interact with your host machine and execute commands directly from Docker Desktop.                                                                                                                                                                                                                                                                                                                                                          | Disabled                 | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Enable Docker Debug by default**                           | Use Docker Debug by default opening the integrated terminal. For more information, see [Explore containers](https://docs.docker.com/desktop/use-desktop/container/#integrated-terminal).                                                                                                                                                                                                                                                    | Disabled                 | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Include VM in Time Machine backups**                       | Back up the Docker Desktop virtual machine.                                                                                                                                                                                                                                                                                                                                                                                                 | Disabled                 | Mac                            |                                                                                                                                                                                                                                                                                                                                                |
| **Use containerd for pulling and storing images**            | Uses containerd image store instead of classic image store. For more information, see [containerd image store](https://docs.docker.com/desktop/features/containerd/).                                                                                                                                                                                                                                                                       | Enabled                  | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Expose daemon on tcp\://localhost:2375 without TLS**       | Allow legacy clients to connect to the Docker daemon. Use with caution as exposing the daemon without TLS can result in remote code execution attacks.                                                                                                                                                                                                                                                                                      | Disabled                 | Windows (Hyper-V backend only) |                                                                                                                                                                                                                                                                                                                                                |
| **Use the WSL 2 based engine**                               | WSL 2 provides better performance than the Hyper-V backend. For more information, see [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).                                                                                                                                                                                                                                                                        | Disabled                 | Windows                        |                                                                                                                                                                                                                                                                                                                                                |
| **Add \*.docker.internal to host file**                      | Adds internal DNS entries.                                                                                                                                                                                                                                                                                                                                                                                                                  | Enabled                  | Windows                        | Helps resolve Docker-internal domains                                                                                                                                                                                                                                                                                                          |
| **Choose Virtual Machine Manager (VMM)**                     | Choose the VMM for creating and managing the Docker Desktop Linux VM. For more information, see [Virtual Machine Manager](https://docs.docker.com/desktop/features/vmm/).                                                                                                                                                                                                                                                                   |                          | Mac                            | Select **Docker VMM** for the latest and most performant Hypervisor/Virtual Machine Manager. This option is available only on Apple Silicon Macs and is in Beta.                                                                                                                                                                               |
| **Choose file sharing implementation for your containers**   | Choose whether you want to share files using **VirtioFS**, **gRPC FUSE**, or **osxfs (Legacy)**                                                                                                                                                                                                                                                                                                                                             | **VirtioFS**             | Mac                            | Use VirtioFS for speedy file sharing. VirtioFS has reduced the time taken to complete filesystem operations by [up to 98%](https://github.com/docker/roadmap/issues/7#issuecomment-1044452206). It is the only file sharing implementation supported by Docker VMM.                                                                            |
| **Use Rosetta for x86\_64/amd64 emulation on Apple Silicon** | Accelerate x86/AMD64 binary emulation on Apple Silicon. This option is only available if you have selected **Apple Virtualization framework** as the Virtual Machine Manager.                                                                                                                                                                                                                                                               | Disabled                 | Mac                            |                                                                                                                                                                                                                                                                                                                                                |
| **Send usage statistics**                                    | Send diagnostics, crash reports, and usage data to Docker to improve and troubleshoot the application. Docker may periodically prompt you for more information.                                                                                                                                                                                                                                                                             | Enabled                  | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Use Enhanced Container Isolation**                         | Prevent containers from breaching the Linux VM. For more information, see [Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/).                                                                                                                                                                                                                                       | Disabled                 | All                            | Must be signed in and have a Docker Business subscription.                                                                                                                                                                                                                                                                                     |
| **Show CLI hints**                                           | Display helpful CLI suggestions in terminal.                                                                                                                                                                                                                                                                                                                                                                                                | Enabled                  | All                            | Improves discoverability                                                                                                                                                                                                                                                                                                                       |
| **Enable Docker Scout image analysis**                       | Show a **Start analysis** button when inspecting an image, which analyzes the image with Docker Scout.                                                                                                                                                                                                                                                                                                                                      | Enabled                  | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Enable background SBOM indexing**                          | Automatically analyze images that you build or pull.                                                                                                                                                                                                                                                                                                                                                                                        | Disabled                 | All                            |                                                                                                                                                                                                                                                                                                                                                |
| **Automatically check configuration**                        | Regularly check your configuration to ensure no unexpected changes have been made by another application. Notifies you if changes are found with the option to restore the configuration directly from the notification. For more information, see the [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/macfaqs/#why-do-i-keep-getting-a-notification-telling-me-an-application-has-changed-my-desktop-configurations). | Enabled                  | Mac                            | Docker Desktop checks if your setup, configured during installation, has been altered by external apps like Orbstack. Docker Desktop checks the symlinks of Docker binaries to `/usr/local/bin` and the symlink of the default Docker socket. Additionally, Docker Desktop ensures that the context is switched to `desktop-linux` on startup. |

## [Resources](#resources)

Control the CPU, memory, disk, file sharing, proxy, and network resources available to Docker Desktop.

### [Advanced](#advanced)

| Setting                 | Description                                                                                                                                                                                                                                     | Platform                    | Notes                                                                                                                                                                                                |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **CPU limit**           | Specify the maximum number of CPUs to be used by Docker Desktop.                                                                                                                                                                                | Mac, Linux, Windows Hyper-V |                                                                                                                                                                                                      |
| **Memory limit**        | RAM allocated to the Docker VM                                                                                                                                                                                                                  | Mac, Linux, Windows Hyper-V | Defaults to 50% of your host's memory.                                                                                                                                                               |
| **Swap**                | Configure swap file size as needed.                                                                                                                                                                                                             | Mac, Linux, Windows Hyper-V | 1 GB default.                                                                                                                                                                                        |
| **Disk usage limit**    | Specify the maximum amount of disk space the engine can use.                                                                                                                                                                                    | Mac, Linux, Windows Hyper-V |                                                                                                                                                                                                      |
| **Disk image location** | Specify the location of the Linux volume where containers and images are stored. On the **Advanced** tab, you can limit resources available to the Docker Linux VM.                                                                             | Mac, Linux, Windows Hyper-V | You can also move the disk image to a different location. If you attempt to move a disk image to a location that already has one, you are asked if you want to use the existing image or replace it. |
| **Resource Saver**      | Enable or disable [Resource Saver mode](https://docs.docker.com/desktop/use-desktop/resource-saver/), which significantly reduces CPU and memory utilization on the host by automatically turning off the Linux VM when Docker Desktop is idle. | Mac, Linux, Windows Hyper-V | Restarts automatically when containers run. Restart may take 3–10 seconds.                                                                                                                           |

In WSL 2 mode, configure memory, CPU, and swap limits on the [WSL 2 utility VM](https://docs.microsoft.com/en-us/windows/wsl/wsl-config#configure-global-options-with-wslconfig).

> Tip
>
> If you feel Docker Desktop starting to get slow or you're running multi-container workloads, increase the memory and disk image space allocation.

### [File sharing](#file-sharing)

Use File sharing to allow local directories on your machine to be shared with Linux containers. This is especially useful for editing source code in an IDE on the host while running and testing the code in a container.

| Setting                      | Description                                                                                                                                                                                                                                                                                                     | Platform                    | Notes                                                 |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- | ----------------------------------------------------- |
| **Synchronized file shares** | Fast and flexible host-to-VM file sharing, enhancing bind mount performance through the use of synchronized filesystem caches. To learn more, see [Synchronized file share](https://docs.docker.com/desktop/features/synchronized-file-sharing/).                                                               | Mac, Linux, Windows Hyper-V | Available with Pro, Team, and Business subscriptions. |
| **Virtual file shares**      | Share local directories with Linux containers. By default the `/Users`, `/Volumes`, `/private`, `/tmp` and `/var/folders` directory are shared. If your project is outside this directory then it must be added to the list, otherwise you may get `Mounts denied` or `cannot start service` errors at runtime. | Mac, Linux, Windows Hyper-V |                                                       |

* Share only the directories that you need with the container. File sharing introduces overhead as any changes to the files on the host need to be notified to the Linux VM. Sharing too many files can lead to high CPU load and slow filesystem performance.
* Shared folders are designed to allow application code to be edited on the host while being executed in containers. For non-code items such as cache directories or databases, the performance will be much better if they are stored in the Linux VM, using a [data volume](https://docs.docker.com/engine/storage/volumes/) (named volume) or [data container](https://docs.docker.com/engine/storage/volumes/).
* If you share the whole of your home directory into a container, Mac may prompt you to give Docker access to personal areas of your home directory such as your Reminders or Downloads.
* By default, Mac file systems are case-insensitive while Linux is case-sensitive. On Linux, it is possible to create two separate files: `test` and `Test`, while on Mac these filenames would actually refer to the same underlying file. This can lead to problems where an app works correctly on a developer's machine (where the file contents are shared) but fails when run in Linux in production (where the file contents are distinct). To avoid this, Docker Desktop insists that all shared files are accessed as their original case. Therefore, if a file is created called `test`, it must be opened as `test`. Attempts to open `Test` will fail with the error "No such file or directory". Similarly, once a file called `test` is created, attempts to create a second file called `Test` will fail.

For more information, see [Volume mounting requires file sharing for any project directories outside of `/Users`](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/).

### [Proxies](#proxies)

Docker Desktop supports HTTP/HTTPS and SOCKS5 proxies. SOCKS5 requires a Business subscription.

To prevent developers from accidentally changing the proxy settings, see [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/#what-features-can-i-configure-with-settings-management).

#### [Docker Desktop proxy](#docker-desktop-proxy)

Used for signing in to Docker, pulling and pushing images, fetching artifacts during image builds, and reporting error diagnostics.

| Proxy mode               | Description                                                                                                                                                                                                                                                                  |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **System proxy**         | Use the proxy configured on the host (static or Proxy Auto-Configuration (PAC)). Docker Desktop reads this automatically.                                                                                                                                                    |
| **No proxy**             | Connect directly without a proxy.                                                                                                                                                                                                                                            |
| **Manual configuration** | Enter a **Web Server (HTTP)** and **Secure Web Server (HTTPS)** URL manually. Use the format `http://proxy:port` or `https://proxy:port`. You can also specify hosts and domains that should bypass the proxy, for example: `registry-1.docker.com,*.docker.com,10.0.0.0/8`. |

> Note
>
> If you use a PAC file hosted on a web server, add the MIME type `application/x-ns-proxy-autoconfig` for the `.pac` extension. Without this, the PAC file may not parse correctly. See [Hardened Docker Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/air-gapped-containers/#proxy-auto-configuration-files).

#### [Containers proxy](#containers-proxy)

Used for outbound traffic from running containers.

| Proxy mode               | Description                                                                                                                                                                                                                                                                  |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Same as host proxy**   | Use the same proxy configuration as the Docker Desktop proxy.                                                                                                                                                                                                                |
| **System proxy**         | Use the proxy configured on the host.                                                                                                                                                                                                                                        |
| **No proxy**             | Connect directly without a proxy.                                                                                                                                                                                                                                            |
| **Manual configuration** | Enter a **Web Server (HTTP)** and **Secure Web Server (HTTPS)** URL manually. Use the format `http://proxy:port` or `https://proxy:port`. You can also specify hosts and domains that should bypass the proxy, for example: `registry-1.docker.com,*.docker.com,10.0.0.0/8`. |

> Note
>
> The HTTPS proxy used for image scanning is configured using the `HTTPS_PROXY` environment variable.

#### [Proxy authentication](#proxy-authentication)

| Method              | Behavior                                                                                                                                                                                                   | Notes                                                                                                                                                                                                                                                                               |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Basic**           | Docker Desktop prompts for credentials and caches them in the OS credential store.                                                                                                                         | Use an `https://` proxy URL to protect passwords in transit. Supports TLS 1.3.                                                                                                                                                                                                      |
| **Kerberos / NTLM** | Centralizes authentication — developers aren't prompted for credentials, reducing the risk of account lockouts. If the proxy returns multiple schemes in a 407 response, Docker Desktop defaults to Basic. | Requires a Business subscription. To enable Kerberos or NTLM proxy authentication you must pass the `--proxy-enable-kerberosntlm` installer flag during installation via the command line, and ensure your proxy server is properly configured for Kerberos or NTLM authentication. |

### [Network](#network)

> Note
>
> On Windows, the **Network** tab is not available in Windows container mode because Windows manages networking.

| Setting                           | Description                                                                                                                                                                                                      | Platform |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| **Docker subnet**                 | Set a custom subnet to avoid conflicts with IPs in your environment. Docker Desktop uses a private IPv4 network for internal services, including a DNS server and HTTP proxy. Default: `192.168.65.0/24`.        | All      |
| **Use kernel networking for UDP** | Use a more efficient kernel networking path for UDP traffic. May not be compatible with VPN software.                                                                                                            | Mac      |
| **Enable host networking**        | Allows containers started with `--net=host` to use `localhost` to connect to TCP and UDP services on the host. Also allows host software to use `localhost` to connect to TCP and UDP services in the container. | Mac      |

On Windows and Mac, you can also set the default networking mode and DNS resolution behavior. For more information, see [Networking](https://docs.docker.com/desktop/features/networking/networking-how-tos/#network-how-tos-for-mac-and-windows).

### [WSL integration (Windows only)](#wsl-integration-windows-only)

| Setting                      | Description                                                           | Notes                                                                                                                                                 |
| ---------------------------- | --------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| WSL distribution integration | Select which WSL 2 distributions have Docker WSL integration enabled. | Integration is enabled on your default WSL distribution by default. To change your default distribution, run `wsl --set-default <distribution name>`. |

For more details on configuring Docker Desktop to use WSL 2, see [Docker Desktop WSL 2 backend](https://docs.docker.com/desktop/features/wsl/).

## [Docker Engine](#docker-engine)

Configure the Docker daemon using a JSON configuration file.

The file is located at `$HOME/.docker/daemon.json`. Edit it directly in the Docker Desktop Dashboard or in a text editor.

To see the full list of possible configuration options, see the [dockerd command reference](/reference/cli/dockerd/).

## [Builders](#builders)

Use the **Builders** tab to inspect and manage builders in the Docker Desktop settings.

### [Inspect](#inspect)

To inspect builders, find the builder that you want to inspect and select the expand icon. You can only inspect active builders.

Inspecting an active builder shows:

* BuildKit version
* Status
* Driver type
* Supported capabilities and platforms
* Disk usage
* Endpoint address

### [Select a different builder](#select-a-different-builder)

The **Selected builder** section displays the selected builder. To select a different builder:

1. Find the builder that you want to use under **Available builders**
2. Open the drop-down menu next to the builder's name.
3. Select **Use** to switch to this builder.

Your build commands now use the selected builder by default.

### [Create a builder](#create-a-builder)

To create a builder, use the Docker CLI. See [Create a new builder](/build/builders/manage/#create-a-new-builder)

### [Remove a builder](#remove-a-builder)

You can remove a builder if:

* The builder isn't your [selected builder](/build/builders/#selected-builder)

* The builder isn't [associated with a Docker context](/build/builders/#default-builder).

  To remove builders associated with a Docker context, remove the context using the `docker context rm` command.

To remove a builder:

1. Find the builder that you want to remove under **Available builders**
2. Open the drop-down menu.
3. Select **Remove** to remove this builder.

If the builder uses the `docker-container` or `kubernetes` driver, the build cache is also removed, along with the builder.

### [Stop and start a builder](#stop-and-start-a-builder)

Builders that use the [`docker-container` driver](/build/builders/drivers/docker-container/) run the BuildKit daemon in a container. You can start and stop the BuildKit container using the drop-down menu.

Running a build automatically starts the container if it's stopped.

You can only start and stop builders using the `docker-container` driver.

## [AI](#ai)

From the AI tab, you can configure settings for:

* [Gordon](https://docs.docker.com/ai/gordon/), the AI-powered assistant that takes action on your Docker workflows.
* [Docker Model Runner](https://docs.docker.com/ai/model-runner/), which makes it easy to manage, run, and deploy AI models using Docker.

## [Kubernetes](#kubernetes)

> Note
>
> On Windows the **Kubernetes** tab is not available in Windows container mode.

Enable and configure the built-in standalone Kubernetes cluster for testing container deployments.

| Setting                               | Description                                                                                                                                                                   |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Enable Kubernetes**                 | Install and run a standalone Kubernetes server as a Docker container for testing deployments.                                                                                 |
| **Cluster provisioning method**       | Choose either **Kubeadm**, a single-node cluster with the version set by Docker Desktop, or **Kind**, a multi-node cluster where you can set the version and number of nodes. |
| **Show system containers (advanced)** | Show internal containers when using Docker commands.                                                                                                                          |
| **Reset Kubernetes cluster**          | Delete all stacks and Kubernetes resources.                                                                                                                                   |

For more information about using the Kubernetes integration with Docker Desktop, see [Explore the Kubernetes view](https://docs.docker.com/desktop/use-desktop/kubernetes/).

## [Software updates](#software-updates)

Manage how and when Docker Desktop checks for and downloads updates.

| Setting                             | Description                                                                                                                        | Default  |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | -------- |
| **Automatically check for updates** | Notifies you of available updates in the Docker menu and Dashboard footer.                                                         | Enabled  |
| **Always download updates**         | Automatically download new versions of Docker Desktop in the background.                                                           | Disabled |
| **Automatically update components** | Update Docker Desktop components (such as Docker Compose, Docker Scout, and the Docker CLI) independently, without a full restart. | Enabled  |

## [Extensions](#extensions)

Enable Docker Extensions and control which extensions are available to install and run.

| Setting                                                              | Description                                               |
| -------------------------------------------------------------------- | --------------------------------------------------------- |
| **Enable Docker Extensions**                                         | Turn Docker Extensions on or off. Turned off by default.  |
| **Allow only extensions distributed through the Docker Marketplace** | Restrict extensions to Marketplace-approved sources only. |
| **Show Docker Extensions system containers**                         | Show containers used by Docker Extensions.                |

For more information about Docker extensions, see [Docker Extensions](https://docs.docker.com/extensions/).

## [Beta features](#beta-features)

Beta features provide access to future product functionality. These features are intended for testing and feedback only as they may change between releases without warning or remove them entirely from a future release. Beta features must not be used in production environments. Docker doesn't offer support for beta features.

You can also sign up to the [Developer Preview program](https://www.docker.com/community/get-involved/developer-preview/) from the **Beta features** tab.

For a list of current experimental features in the Docker CLI, see [Docker CLI Experimental features](https://github.com/docker/cli/blob/master/experimental/README.md).

## [Notifications](#notifications)

Choose which types of Docker Desktop notifications you want to receive.

| Notification type                     | Default                            |
| ------------------------------------- | ---------------------------------- |
| Status updates on tasks and processes | Enabled                            |
| Recommendations from Docker           | Enabled                            |
| Docker announcements                  | Enabled                            |
| Docker surveys                        | Enabled                            |
| Error notifications                   | Always Enabled (cannot be changed) |
| New releases                          | Always Enabled (cannot be changed) |

Notifications appear briefly in the lower-right of the Docker Desktop Dashboard, then move to the **Notifications** drawer, accessible from the top-right of the Dashboard.

## [Advanced (Mac only)](#advanced-mac-only)

Reconfigure CLI tool installation paths and privileged system permissions set during initial install.

| Setting                                        | Description                                                                                                                                                                                                                                                              | Notes                                                                                                                                      |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| CLI tools installation — **System**            | Install Docker CLI tools to `/usr/local/bin`.                                                                                                                                                                                                                            |                                                                                                                                            |
| CLI tools installation — **User**              | Install Docker CLI tools to `$HOME/.docker/bin`                                                                                                                                                                                                                          | Add `$HOME/.docker/bin` to your PATH by appending `export PATH=$PATH:~/.docker/bin` to `~/.bashrc` or `~/.zshrc`, then restart your shell. |
| **Allow the default Docker socket to be used** | Creates `/var/run/docker.sock` which some third party clients may use to communicate with Docker Desktop. For more information, see [permission requirements for macOS](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#installing-symlinks). | Requires password                                                                                                                          |
| **Allow privileged port mapping**              | Starts the privileged helper process which binds the ports that are between 1 and 1024. For more information, see [permission requirements for macOS](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#binding-privileged-ports).              | Requires password                                                                                                                          |

## [Docker Offload](#docker-offload)

Enable Docker Offload and configure idle timeout and GPU support for cloud-based workloads.

| Setting                   | Description                                                                                                                                                                                                                         | Notes                                        |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| **Enable Docker Offload** | Run your containers in the cloud.                                                                                                                                                                                                   | Requires sign-in and an Offload subscription |
| **Idle timeout**          | Set the duration of time between no activity and Docker Offload entering idle mode. For details about idle timeout, see [Active and idle states](https://docs.docker.com/offload/configuration/#understand-active-and-idle-states). |                                              |
| **Enable GPU support**    | Let your workloads use cloud GPU if available.                                                                                                                                                                                      |                                              |

----
url: https://docs.docker.com/accounts/manage-account/
----

# Manage a Docker account

***

Table of contents

***

You can centrally manage your Docker account using Docker Home, including administrative and security settings.

> Tip
>
> If your account is associated with an organization that enforces single sign-on (SSO), you may not have permissions to update your account settings. You must contact your administrator to update your settings.

## [Update account information](#update-account-information)

Account information is visible on your **Account settings** page. You can update the following account information:

* Full name
* Company
* Location
* Website
* Gravatar email

To add or update your avatar using Gravatar:

1. Create a [Gravatar account](https://gravatar.com/).
2. Create your avatar.
3. Add your Gravatar email to your Docker account settings.

It may take some time for your avatar to update in Docker.

## [Update email address](#update-email-address)

To update your email address:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Go to **Settings**, then choose **Email**.
3. Enter your new email address and confirm your identity with your password. Select **Verify email**.
4. Go to the new Docker email and copy the 6-digit verification code.
5. Paste the verification code to complete updating your email.

Your verification session expires after 15 minutes.

> Note
>
> Docker accounts only support one verified email address at a time, which is used for account notifications and security-related communications. You can't add multiple verified email addresses to your account.

## [Change your password](#change-your-password)

You can change your password by initiating a password reset via email. To change your password:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Password**, then **Reset password**.
4. Docker will send you a password reset email with instructions to reset your password.

## [Manage two-factor authentication](#manage-two-factor-authentication)

To update your two-factor authentication (2FA) settings:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **2FA**.

For more information, see [Enable two-factor authentication](https://docs.docker.com/security/2fa/).

## [Manage personal access tokens](#manage-personal-access-tokens)

To manage personal access tokens:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Personal access tokens**.

For more information, see [Create and manage access tokens](https://docs.docker.com/security/access-tokens/).

## [Manage connected accounts](#manage-connected-accounts)

You can unlink connected Google or GitHub accounts:

1. Sign in to your [Docker account](https://app.docker.com/login).
2. Select your avatar in the top-right corner and select **Account settings**.
3. Select **Connected accounts**.
4. Select **Disconnect** on your connected account.

To fully unlink your Docker account, you must also unlink Docker from Google or GitHub. See Google or GitHub's documentation for more information:

* [Manage connections between your Google Account and third-parties](https://support.google.com/accounts/answer/13533235?hl=en)
* [Reviewing and revoking authorization of GitHub Apps](https://docs.github.com/en/apps/using-github-apps/reviewing-and-revoking-authorization-of-github-apps)

## [Convert your account](#convert-your-account)

For information on converting your account into an organization, see [Convert an account into an organization](https://docs.docker.com/admin/organization/setup/convert-account/).

## [Deactivate your account](#deactivate-your-account)

For information on deactivating your account, see [Deactivating a user account](https://docs.docker.com/accounts/deactivate-user-account/).

----
url: https://docs.docker.com/guides/ros2/turtlesim-example/
----

# Run a complete example with Turtlesim

***

Table of contents

***

## [Overview](#overview)

Turtlesim is a simple simulation tool that demonstrates fundamental ROS 2 concepts such as nodes, topics, and services. In this section, you'll run a complete example with Turtlesim, control the turtle, monitor topics, and visualize the system with rqt.

***

## [Configure display forwarding](#configure-display-forwarding)

### [Linux](#linux)

Allow Docker access to your X server:

```console
$ xhost +local:docker
```

### [macOS](#macos)

On macOS, use XQuartz to provide X11 support. Install XQuartz using Homebrew:

1. Install XQuartz using Homebrew:

   ```console
   $ brew install --cask xquartz
   ```

2. Open XQuartz from Applications, then navigate to `Preferences > Security` and enable `Allow connections from network clients`. Restart your computer to ensure the changes take effect.

3. After rebooting, open a terminal and allow local connections:

   ```console
   $ defaults write org.xquartz.X11 nolisten_tcp -bool false
   $ xhost +localhost
   $ xhost + 127.0.0.1
   ```

## [Start the container](#start-the-container)

Start the container using the same Docker Compose setup from the workspace section.

For Linux:

```console
$ cd ws_linux
$ docker compose up -d
$ docker compose exec ros2 /bin/bash
```

For macOS:

```console
$ cd ws_mac
$ docker compose up -d
$ docker compose exec ros2 /bin/bash
```

## [Install and run Turtlesim](#install-and-run-turtlesim)

Inside the container, install the Turtlesim package:

1. Update the package manager:

   ```console
   $ sudo apt update
   ```

2. Install the Turtlesim package:

   ```console
   $ sudo apt install -y ros-humble-turtlesim
   ```

3. Run the Turtlesim node:

   ```console
   $ ros2 run turtlesim turtlesim_node
   ```

A window should appear on your desktop showing a turtle in a grid.

## [Control the turtle](#control-the-turtle)

1. Open a new terminal and connect to the same container, then start the keyboard teleop node:

   ```console
   $ ros2 run turtlesim turtle_teleop_key
   ```

   This node allows you to control the turtle using your keyboard. Use the arrow keys to move the turtle forward, backward, left, and right. Press `Ctrl+C` to stop the teleop node.

2. Move the turtle around the window. You should see it draw a path as it moves.

## [Monitor topics](#monitor-topics)

1. Open another terminal and connect to the same container, then list all active topics:

   ```console
   $ ros2 topic list
   ```

   You should see output similar to the following:

   ```text
   /parameter_events
   /rosout
   /turtle1/cmd_vel
   /turtle1/color_sensor
   /turtle1/pose
   ```

2. Get information about a specific topic:

   ```console
   $ ros2 topic info /turtle1/pose
   ```

   You'll see the topic type and which nodes publish and subscribe to it.

## [Visualize the system with rqt](#visualize-the-system-with-rqt)

1. Open another terminal and connect to the same container, then update the package manager:

   ```console
   $ sudo apt update
   ```

2. Install rqt:

   ```console
   $ sudo apt install -y 'ros-humble-rqt*'
   ```

3. Start rqt:

   ```console
   $ ros2 run rqt_gui rqt_gui
   ```

An rqt window should appear. rqt provides several useful plugins for visualizing and monitoring ROS 2 systems.

### [Node Graph](#node-graph)

You can explore the node graph by navigating to **Plugins > Introspection > Node Graph**. A new tab opens showing nodes and topics with connections illustrated as lines. This visualization demonstrates how the teleop node sends velocity commands to the Turtlesim node, and how the Turtlesim node publishes position data back through topics.

### [Topic Monitor](#topic-monitor)

You can monitor active topics by navigating to **Plugins > Topics > Topic Monitor**. A new tab opens displaying all active topics and their current values. Select the eye icon next to `/turtle1/pose` to monitor it. As you move the turtle, watch the pose values update in real time, showing the position of the turtle and orientation changing based on your commands.

### [Service Caller](#service-caller)

You can call services from rqt using **Plugins > Services > Service Caller**. Select a service such as `/turtle1/teleport_absolute`, enter values for the request fields, and select **Call** to send the request.

### [Plots](#plots)

To plot topic data over time navigate to **Plugins > Visualization > Plot**. For example, in the Plot window, type `/turtle1/pose/x` in the Topic field and press Enter. Move the turtle and watch the X position displayed as a graph over time.

## [Call ROS 2 services](#call-ros-2-services)

Turtlesim provides services for actions such as repositioning the turtle and clearing the path.

1. List available services:

   ```console
   $ ros2 service list
   ```

   You should see services such as `/turtle1/set_pen` (to change pen color and width), `/turtle1/teleport_absolute` (to move the turtle to a specific position), and `/turtle1/teleport_relative` (to move the turtle relative to its current position).

2. Teleport the turtle to a new position:

   ```console
   $ ros2 service call /turtle1/teleport_absolute turtlesim/srv/TeleportAbsolute "
   x: 1.0
   y: 3.0
   theta: 0.0
   "
   ```

   The turtle should instantly move to the specified position (1.0, 3.0).

## [Create a simple publisher](#create-a-simple-publisher)

1. Create a Python script that publishes velocity commands to control the turtle programmatically. In a new terminal, create a file called `move_turtle.py`:

   ```python
   import rclpy
   from geometry_msgs.msg import Twist
   import time

   def main():
       rclpy.init()
       node = rclpy.create_node('turtle_mover')
       publisher = node.create_publisher(Twist, 'turtle1/cmd_vel', 10)

       # Create a twist message
       msg = Twist()
       msg.linear.x = 2.0  # Move forward at 2 m/s
       msg.angular.z = 1.0  # Rotate at 1 rad/s

       # Publish the message
       for i in range(50):
           publisher.publish(msg)
           time.sleep(0.1)

       # Stop the turtle
       msg.linear.x = 0.0
       msg.angular.z = 0.0
       publisher.publish(msg)

       node.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()
   ```

2. Run the script:

   ```console
   $ python3 move_turtle.py
   ```

   The turtle should move in a circular motion for 5 seconds and then stop.

## [Summary](#summary)

In this section, you configured display forwarding, used the Turtlesim nodes, inspected nodes and topics, and visualized the system using rqt. Finally, you interacted with ROS 2 services and created a simple publisher to move the turtle programmatically.

These fundamental concepts apply directly to real-world robotics applications with actual sensors and actuators.

## [Related resources](#related-resources)

* [ROS 2 Turtlesim tutorials](https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html)
* [ROS 2 Concepts](https://docs.ros.org/en/humble/Concepts.html)
* [Geometry Messages](https://github.com/ros2/geometry2/tree/humble/geometry_msgs)

----
url: https://docs.docker.com/engine/cli/formatting/
----

# Format command and log output

***

Table of contents

***

Docker supports [Go templates](https://golang.org/pkg/text/template/) which you can use to manipulate the output format of certain commands and log drivers.

Docker provides a set of basic functions to manipulate template elements. All of these examples use the `docker inspect` command, but many other CLI commands have a `--format` flag, and many of the CLI command references include examples of customizing the output format.

> Note
>
> When using the `--format` flag, you need to observe your shell environment. In a POSIX shell, you can run the following with a single quote:
>
> ```console
> $ docker inspect --format '{{join .Args " , "}}'
> ```
>
> Otherwise, in a Windows shell (for example, PowerShell), you need to use single quotes, but escape the double quotes inside the parameters as follows:
>
> ```console
> $ docker inspect --format '{{join .Args \" , \"}}'
> ```

## [join](#join)

`join` concatenates a list of strings to create a single string. It puts a separator between each element in the list.

```console
$ docker inspect --format '{{join .Args " , "}}' container
```

## [table](#table)

`table` specifies which fields you want to see its output.

```console
$ docker image list --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}\t{{.Size}}"
```

## [json](#json)

`json` encodes an element as a json string.

```console
$ docker inspect --format '{{json .Mounts}}' container
```

## [lower](#lower)

`lower` transforms a string into its lowercase representation.

```console
$ docker inspect --format "{{lower .Name}}" container
```

## [split](#split)

`split` slices a string into a list of strings separated by a separator.

```console
$ docker inspect --format '{{split .Image ":"}}' container
```

## [title](#title)

`title` capitalizes the first character of a string.

```console
$ docker inspect --format "{{title .Name}}" container
```

## [upper](#upper)

`upper` transforms a string into its uppercase representation.

```console
$ docker inspect --format "{{upper .Name}}" container
```

## [pad](#pad)

`pad` adds whitespace padding to a string. You can specify the number of spaces to add before and after the string.

```console
$ docker image list --format '{{pad .Repository 5 10}}'
```

This example adds 5 spaces before the image repository name and 10 spaces after.

## [truncate](#truncate)

`truncate` shortens a string to a specified length. If the string is shorter than the specified length, it remains unchanged.

```console
$ docker image list --format '{{truncate .Repository 15}}'
```

This example displays the image repository name, truncating it to the first 15 characters if it's longer.

## [`println`](#println)

`println` prints each value on a new line.

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{println .IPAddress}}{{end}}' container
```

## [Hint](#hint)

To find out what data can be printed, show all content as json:

```console
$ docker container ls --format='{{json .}}'
```

----
url: https://docs.docker.com/reference/cli/docker/mcp/catalog/
----

# docker mcp catalog

***

| Description                                                               | Manage MCP server OCI catalogs                  |
| ------------------------------------------------------------------------- | ----------------------------------------------- |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp catalogs` `docker mcp catalog-next` |

## [Description](#description)

Manage MCP server OCI catalogs

## [Subcommands](#subcommands)

| Command                                                                                         | Description                                                                |
| ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| [`docker mcp catalog create`](https://docs.docker.com/reference/cli/docker/mcp/catalog/create/) | Create a new catalog from a profile, legacy catalog, or community registry |
| [`docker mcp catalog list`](https://docs.docker.com/reference/cli/docker/mcp/catalog/list/)     | List catalogs                                                              |
| [`docker mcp catalog ls`](https://docs.docker.com/reference/cli/docker/mcp/catalog/ls/)         | List all configured catalogs                                               |
| [`docker mcp catalog pull`](https://docs.docker.com/reference/cli/docker/mcp/catalog/pull/)     | Pull a catalog from an OCI registry                                        |
| [`docker mcp catalog push`](https://docs.docker.com/reference/cli/docker/mcp/catalog/push/)     | Push a catalog to an OCI registry                                          |
| [`docker mcp catalog remove`](https://docs.docker.com/reference/cli/docker/mcp/catalog/remove/) | Remove a catalog                                                           |
| [`docker mcp catalog rm`](https://docs.docker.com/reference/cli/docker/mcp/catalog/rm/)         | Remove a catalog                                                           |
| [`docker mcp catalog server`](https://docs.docker.com/reference/cli/docker/mcp/catalog/server/) | Manage servers in catalogs                                                 |
| [`docker mcp catalog show`](https://docs.docker.com/reference/cli/docker/mcp/catalog/show/)     | Show a catalog                                                             |
| [`docker mcp catalog tag`](https://docs.docker.com/reference/cli/docker/mcp/catalog/tag/)       | Create a tagged copy of a catalog                                          |

----
url: https://docs.docker.com/engine/swarm/join-nodes/
----

# Join nodes to a swarm

***

Table of contents

***

When you first create a swarm, you place a single Docker Engine into Swarm mode. To take full advantage of Swarm mode you can add nodes to the swarm:

* Adding worker nodes increases capacity. When you deploy a service to a swarm, the engine schedules tasks on available nodes whether they are worker nodes or manager nodes. When you add workers to your swarm, you increase the scale of the swarm to handle tasks without affecting the manager raft consensus.
* Manager nodes increase fault-tolerance. Manager nodes perform the orchestration and cluster management functions for the swarm. Among manager nodes, a single leader node conducts orchestration tasks. If a leader node goes down, the remaining manager nodes elect a new leader and resume orchestration and maintenance of the swarm state. By default, manager nodes also run tasks.

Docker Engine joins the swarm depending on the **join-token** you provide to the `docker swarm join` command. The node only uses the token at join time. If you subsequently rotate the token, it doesn't affect existing swarm nodes. Refer to [Run Docker Engine in swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/#view-the-join-command-or-update-a-swarm-join-token).

## [Join as a worker node](#join-as-a-worker-node)

To retrieve the join command including the join token for worker nodes, run the following command on a manager node:

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
    192.168.99.100:2377
```

Run the command from the output on the worker to join the swarm:

```console
$ docker swarm join \
  --token SWMTKN-1-49nj1cmql0jkz5s954yi3oex3nedyz0fb0xx14ie39trti4wxv-8vxv8rssmk743ojnwacrr2e7c \
  192.168.99.100:2377

This node joined a swarm as a worker.
```

The `docker swarm join` command does the following:

* Switches Docker Engine on the current node into Swarm mode.
* Requests a TLS certificate from the manager.
* Names the node with the machine hostname.
* Joins the current node to the swarm at the manager listen address based upon the swarm token.
* Sets the current node to `Active` availability, meaning it can receive tasks from the scheduler.
* Extends the `ingress` overlay network to the current node.

## [Join as a manager node](#join-as-a-manager-node)

When you run `docker swarm join` and pass the manager token, Docker Engine switches into Swarm mode the same as for workers. Manager nodes also participate in the raft consensus. The new nodes should be `Reachable`, but the existing manager remains the swarm `Leader`.

Docker recommends three or five manager nodes per cluster to implement high availability. Because Swarm-mode manager nodes share data using Raft, there must be an odd number of managers. The swarm can continue to function after as long as a quorum of more than half of the manager nodes are available.

For more detail about swarm managers and administering a swarm, see [Administer and maintain a swarm of Docker Engines](https://docs.docker.com/engine/swarm/admin_guide/).

To retrieve the join command including the join token for manager nodes, run the following command on a manager node:

```console
$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
    192.168.99.100:2377
```

Run the command from the output on the new manager node to join it to the swarm:

```console
$ docker swarm join \
  --token SWMTKN-1-61ztec5kyafptydic6jfc1i33t37flcl4nuipzcusor96k7kby-5vy9t8u35tuqm7vh67lrz9xp6 \
  192.168.99.100:2377

This node joined a swarm as a manager.
```

## [Learn More](#learn-more)

* `swarm join` [command line reference](/reference/cli/docker/swarm/join/)
* [Swarm mode tutorial](https://docs.docker.com/engine/swarm/swarm-tutorial/)

----
url: https://docs.docker.com/reference/cli/docker/scout/watch/
----

# docker scout watch

***

| Description | Watch repositories in a registry and push images and indexes to Docker Scout |
| ----------- | ---------------------------------------------------------------------------- |
| Usage       | `docker scout watch`                                                         |

## [Description](#description)

The docker scout watch command watches repositories in a registry and pushes images or image indexes to Docker Scout.

## [Options](#options)

| Option               | Default | Description                                                                          |
| -------------------- | ------- | ------------------------------------------------------------------------------------ |
| `--all-images`       |         | Push all images instead of only the ones pushed during the watch command is running  |
| `--dry-run`          |         | Watch images and prepare them, but do not push them                                  |
| `--interval`         | `60`    | Interval in seconds between checks                                                   |
| `--org`              |         | Namespace of the Docker organization to which image will be pushed                   |
| `--refresh-registry` |         | Refresh the list of repositories of a registry at every run. Only with --registry.   |
| `--registry`         |         | Registry to watch                                                                    |
| `--repository`       |         | Repository to watch                                                                  |
| `--sbom`             | `true`  | Create and upload SBOMs                                                              |
| `--tag`              |         | Regular expression to match tags to watch                                            |
| `--workers`          | `3`     | Number of concurrent workers                                                         |

## [Examples](#examples)

### [Watch for new images from two repositories and push them](#watch-for-new-images-from-two-repositories-and-push-them)

```console
$ docker scout watch --org my-org --repository registry-1.example.com/repo-1 --repository registry-2.example.com/repo-2
```

### [Only push images with a specific tag](#only-push-images-with-a-specific-tag)

```console
$ docker scout watch --org my-org --repository registry.example.com/my-service --tag latest
```

### [Watch all repositories of a registry](#watch-all-repositories-of-a-registry)

```console
$ docker scout watch --org my-org --registry registry.example.com
```

### [Push all images and not just the new ones](#push-all-images-and-not-just-the-new-ones)

```console
$ docker scout watch --org my-org --repository registry.example.com/my-service --all-images
```

### [Configure Artifactory integration](#configure-artifactory-integration)

The following example creates a web hook endpoint for Artifactory to push new image events into:

```console
$ export DOCKER_SCOUT_ARTIFACTORY_API_USER=user
$ export DOCKER_SCOUT_ARTIFACTORY_API_PASSWORD=password
$ export DOCKER_SCOUT_ARTIFACTORY_WEBHOOK_SECRET=foo

$ docker scout watch --registry "type=artifactory,registry=example.jfrog.io,api=https://example.jfrog.io/artifactory,include=*/frontend*,exclude=*/dta/*,repository=docker-local,port=9000,subdomain-mode=true" --refresh-registry
```

This will launch an HTTP server on port `9000` that will receive all `component` web hook events, optionally validating the HMAC signature.

### [Configure Harbor integration](#configure-harbor-integration)

The following example creates a web hook endpoint for Harbor to push new image events into:

```console
$ export DOCKER_SCOUT_HARBOR_API_USER=admin
$ export DOCKER_SCOUT_HARBOR_API_PASSWORD=password
$ export DOCKER_SCOUT_HARBOR_WEBHOOK_AUTH="token foo"

$ docker scout watch --registry 'type=harbor,registry=demo.goharbor.io,api=https://demo.goharbor.io,include=*/foo/*,exclude=*/bar/*,port=9000' --refresh-registry
```

This will launch an HTTP server on port `9000` that will receive all `component` web hook events, optionally validating the HMAC signature.

### [Configure Nexus integration](#configure-nexus-integration)

The following example shows how to configure Sonartype Nexus integration:

```console
$ export DOCKER_SCOUT_NEXUS_API_USER=admin
$ export DOCKER_SCOUT_NEXUS_API_PASSWORD=admin124

$ docker scout watch --registry 'type=nexus,registry=localhost:8082,api=http://localhost:8081,include=*/foo/*,exclude=*/bar/*,"repository=docker-test1,docker-test2"' --refresh-registry
```

This ingests all images and tags in Nexus repositories called `docker-test1` and `docker-test2` that match the `*/foo/*` include and `*/bar/*` exclude glob pattern.

You can also create a web hook endpoint for Nexus to push new image events into:

```console
$ export DOCKER_SCOUT_NEXUS_API_USER=admin
$ export DOCKER_SCOUT_NEXUS_API_PASSWORD=admin124
$ export DOCKER_SCOUT_NEXUS_WEBHOOK_SECRET=mysecret

$ docker scout watch --registry 'type=nexus,registry=localhost:8082,api=http://localhost:8081,include=*/foo/*,exclude=*/bar/*,"repository=docker-test1,docker-test2",port=9000' --refresh-registry
```

This will launch an HTTP server on port `9000` that will receive all `component` web hook events, optionally validating the HMAC signature.

### [Configure integration for other OCI registries](#configure-integration-for-other-oci-registries)

The following example shows how to integrate an OCI registry that implements the `_catalog` endpoint:

```console
$ docker scout watch --registry 'type=oci,registry=registry.example.com,include=*/scout-artifact-registry/*'
```

----
url: https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/
----

# Testing REST API integrations in Micronaut apps using WireMock

Table of contents

***

Learn how to create a Micronaut application that integrates with external REST APIs, then test those integrations using WireMock and the Testcontainers WireMock module.

**Time to complete** 20 minutes

In this guide, you'll learn how to:

* Create a Micronaut application that talks to external REST APIs
* Test external API integrations using WireMock
* Use the Testcontainers WireMock module to run WireMock as a Docker container

## [Prerequisites](#prerequisites)

* Java 17+
* Maven or Gradle
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/create-project/)

   Set up a Micronaut project with an external REST API integration using declarative HTTP clients.

2. [Write tests](https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/write-tests/)

   Test external REST API integrations using WireMock and the Testcontainers WireMock module.

3. [Run tests](https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/run-tests/)

   Run your Testcontainers WireMock integration tests and explore next steps.

----
url: https://docs.docker.com/reference/build-checks/from-as-casing/
----

# FromAsCasing

***

Table of contents

***

## [Output](#output)

```text
'as' and 'FROM' keywords' casing do not match
```

## [Description](#description)

While Dockerfile keywords can be either uppercase or lowercase, mixing case styles is not recommended for readability. This rule reports violations where mixed case style occurs for a `FROM` instruction with an `AS` keyword declaring a stage name.

## [Examples](#examples)

❌ Bad: `FROM` is uppercase, `AS` is lowercase.

```dockerfile
FROM debian:latest as builder
```

✅ Good: `FROM` and `AS` are both uppercase

```dockerfile
FROM debian:latest AS deb-builder
```

✅ Good: `FROM` and `AS` are both lowercase.

```dockerfile
from debian:latest as deb-builder
```

## [Related errors](#related-errors)

* [`FileConsistentCommandCasing`](https://docs.docker.com/reference/build-checks/consistent-instruction-casing/)

----
url: https://docs.docker.com/guides/rust/build-images/
----

# Build your Rust image

***

Table of contents

***

## [Prerequisites](#prerequisites)

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
* You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

## [Overview](#overview)

This guide walks you through building your first Rust image. An image includes everything needed to run an application - the code or binary, runtime, dependencies, and any other file system objects required.

## [Get the sample application](#get-the-sample-application)

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/docker/docker-rust-hello && cd docker-rust-hello
```

## [Choose a base image](#choose-a-base-image)

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

Before editing your Dockerfile, you need to choose a base image. You can use the [Rust Docker Official Image](https://hub.docker.com/_/rust),\
or a [Docker Hardened Image (DHI)](https://hub.docker.com/hardened-images/catalog/dhi/rust).

Docker Hardened Images (DHIs) are minimal, secure, and production-ready base images maintained by Docker.\
They help reduce vulnerabilities and simplify compliance. For more details, see [Docker Hardened Images](/dhi/).

Docker Hardened Images (DHIs) are publicly available and can be used directly as base images. To pull Docker Hardened Images, authenticate once with Docker:

```bash
docker login dhi.io
```

Use DHIs from the dhi.io registry, for example:

```bash
FROM dhi.io/rust:${RUST_VERSION}-alpine3.22-dev AS build
```

The following Dockerfile uses a Rust DHI as the build base image:

Dockerfile

```dockerfile
# Make sure RUST_VERSION matches the Rust version
ARG RUST_VERSION=1.92
ARG APP_NAME=docker-rust-hello

################################################################################
# Create a stage for building the application.
################################################################################

FROM dhi.io/rust:${RUST_VERSION}-alpine3.22-dev AS build
ARG APP_NAME
WORKDIR /app

# Install host build dependencies.
RUN apk add --no-cache clang lld musl-dev git

# Build the application.
RUN --mount=type=bind,source=src,target=src \
    --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/git/db \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    cargo build --locked --release && \
    cp ./target/release/$APP_NAME /bin/server

################################################################################
# Create a new stage for running the application that contains the minimal
# We use dhi.io/static for the final stage because it’s a minimal Docker Hardened Image runtime (basically “just # enough OS to run the binary”), which helps keep the image small and with a lower attack surface compared to a # # full Alpine/Debian runtime.
################################################################################

FROM dhi.io/static:20250419 AS final

# Copy the executable from the "build" stage.
COPY --from=build /bin/server /bin/

# Configure rocket to listen on all interfaces.
ENV ROCKET_ADDRESS=0.0.0.0

# Expose the port that the application listens on.
EXPOSE 8000

# What the container should run when it is started.
CMD ["/bin/server"]
```

Dockerfile

```dockerfile
# Pin the Rust toolchain version used in the build stage.
ARG RUST_VERSION=1.92

# Name of the compiled binary produced by Cargo (must match Cargo.toml package name).
ARG APP_NAME=docker-rust-hello

################################################################################
# Build stage (DOI Rust image)
# This stage compiles the application.
################################################################################

FROM docker.io/library/rust:${RUST_VERSION}-alpine AS build

# Re-declare args inside the stage if you want to use them here.
ARG APP_NAME

# All build steps happen inside /app.
WORKDIR /app

# Install build dependencies needed to compile Rust crates on Alpine
RUN apk add --no-cache clang lld musl-dev git

# Build the application 
RUN --mount=type=bind,source=src,target=src \
    --mount=type=bind,source=Cargo.toml,target=Cargo.toml \
    --mount=type=bind,source=Cargo.lock,target=Cargo.lock \
    --mount=type=cache,target=/app/target/ \
    --mount=type=cache,target=/usr/local/cargo/git/db \
    --mount=type=cache,target=/usr/local/cargo/registry/ \
    cargo build --locked --release && \
    cp ./target/release/$APP_NAME /bin/server

################################################################################
# Runtime stage (DOI Alpine image)
# This stage runs the already-compiled binary with minimal dependencies.
################################################################################

FROM docker.io/library/alpine:3.18 AS final

# Create a non-privileged user (recommended best practice)
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Drop privileges for runtime.
USER appuser

# Copy only the compiled binary from the build stage.
COPY --from=build /bin/server /bin/

# Rocket: listen on all interfaces inside the container.
ENV ROCKET_ADDRESS=0.0.0.0

# Document the port your app listens on.
EXPOSE 8000

# Start the application.
CMD ["/bin/server"]
```

For building an image, only the Dockerfile is necessary. Open the Dockerfile in your favorite IDE or text editor and see what it contains. To learn more about Dockerfiles, see the [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

## [.dockerignore file](#dockerignore-file)

The [`.dockerignore`](https://docs.docker.com/reference/dockerfile/#dockerignore-file) file specifies patterns and paths that you don't want copied into the image in order to keep the image as small as possible. Open up the `.dockerignore` file in your favorite IDE or text editor to review its contents.

## [Build an image](#build-an-image)

Now that you’ve created the Dockerfile, you can build the image. To do this, use the `docker build` command. The `docker build` command builds Docker images from a Dockerfile and a context. A build's context is the set of files located in the specified PATH or URL. The Docker build process can access any of the files located in this context.

The build command optionally takes a `--tag` flag. The tag sets the name of the image and an optional tag in the format `name:tag`. If you don't pass a tag, Docker uses "latest" as its default tag.

Build the Docker image.

```console
$ docker build --tag docker-rust-image-dhi .
```

You should see output like the following.

```console
[+] Building 1.4s (13/13) FINISHED                                                                                                                                 docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                                                               0.0s
 => => transferring dockerfile: 1.67kB                                                                                                                                             0.0s
 => [internal] load metadata for dhi.io/static:20250419                                                                                                                            1.1s
 => [internal] load metadata for dhi.io/rust:1.92-alpine3.22-dev                                                                                                                   1.2s
 => [auth] static:pull token for dhi.io                                                                                                                                            0.0s
 => [auth] rust:pull token for dhi.io                                                                                                                                              0.0s
 => [internal] load .dockerignore                                                                                                                                                  0.0s
 => => transferring context: 646B                                                                                                                                                  0.0s
 => [build 1/3] FROM dhi.io/rust:1.92-alpine3.22-dev@sha256:49eb72825a9e15fe48f2c4875a63c7e7f52a5b430bb52b8254b91d132aa5bf38                                                       0.0s
 => => resolve dhi.io/rust:1.92-alpine3.22-dev@sha256:49eb72825a9e15fe48f2c4875a63c7e7f52a5b430bb52b8254b91d132aa5bf38                                                             0.0s
 => [final 1/2] FROM dhi.io/static:20250419@sha256:74fc43fa240887b8159970e434244039aab0c6efaaa9cf044004cdc22aa2a34d                                                                0.0s
 => => resolve dhi.io/static:20250419@sha256:74fc43fa240887b8159970e434244039aab0c6efaaa9cf044004cdc22aa2a34d                                                                      0.0s
 => [internal] load build context                                                                                                                                                  0.0s
 => => transferring context: 117B                                                                                                                                                  0.0s
 => CACHED [build 2/3] WORKDIR /build                                                                                                                                              0.0s
 => CACHED [build 3/3] RUN --mount=type=bind,source=src,target=src     --mount=type=bind,source=Cargo.toml,target=Cargo.toml     --mount=type=bind,source=Cargo.lock,target=Cargo  0.0s
 => CACHED [final 2/2] COPY --from=build /build/target/release/docker-rust-hello /server                                                                                           0.0s
 => exporting to image                                                                                                                                                             0.1s
 => => exporting layers                                                                                                                                                            0.0s
 => => exporting manifest sha256:cc937bbdd712ef6e5445501f77e02ef8455ef64c567598786d46b7b21a4d4fa8                                                                                  0.0s
 => => exporting config sha256:077507b483af4b5e1a928e527e4bb3a4aaf0557e1eea81cd39465f564c187669                                                                                    0.0s
 => => exporting attestation manifest sha256:11b60e7608170493da1fdd88c120e2d2957f2a72a22edbc9cfbdd0dd37d21f89                                                                      0.0s
 => => exporting manifest list sha256:99a1b925a8d6ebf80e376b8a1e50cd806ec42d194479a3375e1cd9d2911b4db9                                                                             0.0s
 => => naming to docker.io/library/docker-rust-image-dhi:latest                                                                                                                    0.0s
 => => unpacking to docker.io/library/docker-rust-image-dhi:latest                                                                                                                 0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/yczk0ijw8kc5g20e8nbc8r6lj
```

## [View local images](#view-local-images)

To see a list of images you have on your local machine, you have two options. One is to use the Docker CLI and the other is to use [Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/). As you are working in the terminal already, take a look at listing images using the CLI.

To list images, run the `docker images` command.

```console
$ docker images
IMAGE                          ID             DISK USAGE   CONTENT SIZE   EXTRA
docker-rust-image-dhi:latest   99a1b925a8d6       11.6MB         2.45MB    U   
```

You should see at least one image listed, including the image you just built `docker-rust-image-dhi:latest`.

## [Tag images](#tag-images)

As mentioned earlier, an image name is made up of slash-separated name components. Name components may contain lowercase letters, digits, and separators. A separator can include a period, one or two underscores, or one or more dashes. A name component may not start or end with a separator.

An image is made up of a manifest and a list of layers. Don't worry too much about manifests and layers at this point other than a "tag" points to a combination of these artifacts. You can have multiple tags for an image. Create a second tag for the image you built and take a look at its layers.

To create a new tag for the image you built, run the following command.

```console
$ docker tag docker-rust-image-dhi:latest docker-rust-image-dhi:v1.0.0
```

The `docker tag` command creates a new tag for an image. It doesn't create a new image. The tag points to the same image and is just another way to reference the image.

Now, run the `docker images` command to see a list of the local images.

```console
$ docker images
IMAGE                          ID             DISK USAGE   CONTENT SIZE   EXTRA
docker-rust-image-dhi:latest   99a1b925a8d6       11.6MB         2.45MB    U   
docker-rust-image-dhi:v1.0.0   99a1b925a8d6       11.6MB         2.45MB    U  
```

You can see that two images start with `docker-rust-image-dhi`. You know they're the same image because if you take a look at the `IMAGE ID` column, you can see that the values are the same for the two images.

Remove the tag you just created. To do this, use the `rmi` command. The `rmi` command stands for remove image.

```console
$ docker rmi docker-rust-image-dhi:v1.0.0
Untagged: docker-rust-image-dhi:v1.0.0
```

Note that the response from Docker tells you that Docker didn't remove the image, but only "untagged" it. You can check this by running the `docker images` command.

```console
$ docker images
IMAGE                          ID             DISK USAGE   CONTENT SIZE   EXTRA
docker-rust-image-dhi:latest   99a1b925a8d6       11.6MB         2.45MB    U   
```

Docker removed the image tagged with `:v1.0.0`, but the `docker-rust-image-dhi:latest` tag is available on your machine.

## [Summary](#summary)

This section showed how to create a Dockerfile and `.dockerignore` file for a Rust application, build an image, and tag and list images.

Related information:

* [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
* [.dockerignore file](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
* [docker build CLI reference](/reference/cli/docker/buildx/build/)
* [Docker Hardened Images](/dhi/)

## [Next steps](#next-steps)

In the next section learn how to run your image as a container.

[Run your Rust image as a container »](https://docs.docker.com/guides/rust/run-containers/)

----
url: https://docs.docker.com/guides/docker-scout/demo/
----

# Docker Scout demo

***

***

Docker Scout has powerful features for enhancing containerized application security and ensuring a robust software supply chain.

* Define vulnerability remediation
* Discuss why remediation is essential to maintain the security and integrity of containerized applications
* Discuss common vulnerabilities
* Implement remediation techniques: updating base images, applying patches, removing unnecessary packages
* Verify and validate remediation efforts using Docker Scout

[Software supply chain security »](https://docs.docker.com/guides/docker-scout/s3c/)

----
url: https://docs.docker.com/reference/cli/docker/compose/pull/
----

# docker compose pull

***

| Description | Pull service images                          |
| ----------- | -------------------------------------------- |
| Usage       | `docker compose pull [OPTIONS] [SERVICE...]` |

## [Description](#description)

Pulls an image associated with a service defined in a `compose.yaml` file, but does not start containers based on those images

## [Options](#options)

| Option                   | Default | Description                                            |
| ------------------------ | ------- | ------------------------------------------------------ |
| `--ignore-buildable`     |         | Ignore images that can be built                        |
| `--ignore-pull-failures` |         | Pull what it can and ignores images with pull failures |
| `--include-deps`         |         | Also pull services declared as dependencies            |
| `--policy`               |         | Apply pull policy ("missing"\|"always")                |
| `-q, --quiet`            |         | Pull without printing progress information             |

## [Examples](#examples)

Consider the following `compose.yaml`:

```yaml
services:
  db:
    image: postgres
  web:
    build: .
    command: bundle exec rails s -p 3000 -b '0.0.0.0'
    volumes:
      - .:/myapp
    ports:
      - "3000:3000"
    depends_on:
      - db
```

If you run `docker compose pull ServiceName` in the same directory as the `compose.yaml` file that defines the service, Docker pulls the associated image. For example, to call the postgres image configured as the db service in our example, you would run `docker compose pull db`.

```console
$ docker compose pull db
[+] Running 1/15
 ⠸ db Pulling                                                             12.4s
   ⠿ 45b42c59be33 Already exists                                           0.0s
   ⠹ 40adec129f1a Downloading  3.374MB/4.178MB                             9.3s
   ⠹ b4c431d00c78 Download complete                                        9.3s
   ⠹ 2696974e2815 Download complete                                        9.3s
   ⠹ 564b77596399 Downloading  5.622MB/7.965MB                             9.3s
   ⠹ 5044045cf6f2 Downloading  216.7kB/391.1kB                             9.3s
   ⠹ d736e67e6ac3 Waiting                                                  9.3s
   ⠹ 390c1c9a5ae4 Waiting                                                  9.3s
   ⠹ c0e62f172284 Waiting                                                  9.3s
   ⠹ ebcdc659c5bf Waiting                                                  9.3s
   ⠹ 29be22cb3acc Waiting                                                  9.3s
   ⠹ f63c47038e66 Waiting                                                  9.3s
   ⠹ 77a0c198cde5 Waiting                                                  9.3s
   ⠹ c8752d5b785c Waiting                                                  9.3s
```

`docker compose pull` tries to pull image for services with a build section. If pull fails, it lets you know this service image must be built. You can skip this by setting `--ignore-buildable` flag.

----
url: https://docs.docker.com/reference/cli/sbx/create/gemini/
----

# sbx create gemini

| Description | Create a sandbox for gemini                |
| ----------- | ------------------------------------------ |
| Usage       | `sbx create gemini PATH [PATH...] [flags]` |

## [Description](#description)

Create a sandbox with access to a host workspace for gemini.

The workspace path is required and will be mounted inside the sandbox at the same path as on the host. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

Use "sbx run --name SANDBOX" to attach to the agent after creation.

## [Global options](#global-options)

| Option           | Default | Description                                                                                                                                                                                                            |
| ---------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--clone`        |         | Run the agent on a private in-container clone of the host Git repository (mounted read-only) instead of bind-mounting the workspace; the agent's commits are accessible via the sandbox-\<name> git remote on the host |
| `--cpus`         | `0`     | Number of CPUs to allocate to the sandbox (0 = auto: N-1 host CPUs, min 1)                                                                                                                                             |
| `-D, --debug`    |         | Enable debug logging                                                                                                                                                                                                   |
| `--kit`          |         | experimental Kit reference (directory, ZIP, or OCI). Can be specified multiple times                                                                                                                                   |
| `-m, --memory`   |         | Memory limit in binary units (e.g., 1024m, 8g). Default: 50% of host memory, max 32 GiB                                                                                                                                |
| `--name`         |         | Name for the sandbox (default: \<agent>-\<workdir>, letters, numbers, hyphens, periods, plus signs and minus signs only)                                                                                               |
| `-q, --quiet`    |         | Suppress verbose output                                                                                                                                                                                                |
| `-t, --template` |         | Container image to use for the sandbox (default: agent-specific image)                                                                                                                                                 |

## [Examples](#examples)

```console
# Create in the current directory
sbx create gemini .

# Create with a specific path
sbx create gemini /path/to/project

# Create with additional read-only workspaces
sbx create gemini . /path/to/docs:ro
```

----
url: https://docs.docker.com/reference/cli/sbx/completion/powershell/
----

# sbx completion powershell

| Description | Generate the autocompletion script for powershell |
| ----------- | ------------------------------------------------- |
| Usage       | `sbx completion powershell [flags]`               |

## [Description](#description)

Generate the autocompletion script for powershell.

To load completions in your current shell session:

```
sbx completion powershell | Out-String | Invoke-Expression
```

To load completions for every new session, add the output of the above command to your powershell profile.

## [Options](#options)

| Option              | Default | Description                     |
| ------------------- | ------- | ------------------------------- |
| `--no-descriptions` |         | disable completion descriptions |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/reference/cli/sbx/ls/
----

# sbx ls

| Description | List sandboxes   |
| ----------- | ---------------- |
| Usage       | `sbx ls [flags]` |

## [Description](#description)

List all sandboxes with their agent, status, published ports, and workspace.

## [Options](#options)

| Option        | Default | Description                |
| ------------- | ------- | -------------------------- |
| `--json`      |         | Output in JSON format      |
| `-q, --quiet` |         | Only display sandbox names |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/reference/cli/docker/container/
----

# docker container

***

| Description | Manage containers  |
| ----------- | ------------------ |
| Usage       | `docker container` |

## [Description](#description)

Manage containers.

## [Subcommands](#subcommands)

| Command                                                                                       | Description                                                                   |
| --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [`docker container attach`](https://docs.docker.com/reference/cli/docker/container/attach/)   | Attach local standard input, output, and error streams to a running container |
| [`docker container commit`](https://docs.docker.com/reference/cli/docker/container/commit/)   | Create a new image from a container's changes                                 |
| [`docker container cp`](https://docs.docker.com/reference/cli/docker/container/cp/)           | Copy files/folders between a container and the local filesystem               |
| [`docker container create`](https://docs.docker.com/reference/cli/docker/container/create/)   | Create a new container                                                        |
| [`docker container diff`](https://docs.docker.com/reference/cli/docker/container/diff/)       | Inspect changes to files or directories on a container's filesystem           |
| [`docker container exec`](https://docs.docker.com/reference/cli/docker/container/exec/)       | Execute a command in a running container                                      |
| [`docker container export`](https://docs.docker.com/reference/cli/docker/container/export/)   | Export a container's filesystem as a tar archive                              |
| [`docker container inspect`](https://docs.docker.com/reference/cli/docker/container/inspect/) | Display detailed information on one or more containers                        |
| [`docker container kill`](https://docs.docker.com/reference/cli/docker/container/kill/)       | Kill one or more running containers                                           |
| [`docker container logs`](https://docs.docker.com/reference/cli/docker/container/logs/)       | Fetch the logs of a container                                                 |
| [`docker container ls`](https://docs.docker.com/reference/cli/docker/container/ls/)           | List containers                                                               |
| [`docker container pause`](https://docs.docker.com/reference/cli/docker/container/pause/)     | Pause all processes within one or more containers                             |
| [`docker container port`](https://docs.docker.com/reference/cli/docker/container/port/)       | List port mappings or a specific mapping for the container                    |
| [`docker container prune`](https://docs.docker.com/reference/cli/docker/container/prune/)     | Remove all stopped containers                                                 |
| [`docker container rename`](https://docs.docker.com/reference/cli/docker/container/rename/)   | Rename a container                                                            |
| [`docker container restart`](https://docs.docker.com/reference/cli/docker/container/restart/) | Restart one or more containers                                                |
| [`docker container rm`](https://docs.docker.com/reference/cli/docker/container/rm/)           | Remove one or more containers                                                 |
| [`docker container run`](https://docs.docker.com/reference/cli/docker/container/run/)         | Create and run a new container from an image                                  |
| [`docker container start`](https://docs.docker.com/reference/cli/docker/container/start/)     | Start one or more stopped containers                                          |
| [`docker container stats`](https://docs.docker.com/reference/cli/docker/container/stats/)     | Display a live stream of container(s) resource usage statistics               |
| [`docker container stop`](https://docs.docker.com/reference/cli/docker/container/stop/)       | Stop one or more running containers                                           |
| [`docker container top`](https://docs.docker.com/reference/cli/docker/container/top/)         | Display the running processes of a container                                  |
| [`docker container unpause`](https://docs.docker.com/reference/cli/docker/container/unpause/) | Unpause all processes within one or more containers                           |
| [`docker container update`](https://docs.docker.com/reference/cli/docker/container/update/)   | Update configuration of one or more containers                                |
| [`docker container wait`](https://docs.docker.com/reference/cli/docker/container/wait/)       | Block until one or more containers stop, then print their exit codes          |

----
url: https://docs.docker.com/engine/extend/
----

# Docker Engine managed plugin system

***

Table of contents

***

* [Installing and using a plugin](https://docs.docker.com/engine/extend/#installing-and-using-a-plugin)
* [Developing a plugin](https://docs.docker.com/engine/extend/#developing-a-plugin)
* [Debugging plugins](https://docs.docker.com/engine/extend/#debugging-plugins)

Docker Engine's plugin system lets you install, start, stop, and remove plugins using Docker Engine.

For information about legacy (non-managed) plugins, refer to [Understand legacy Docker Engine plugins](https://docs.docker.com/engine/extend/legacy_plugins/).

> Note
>
> Docker Engine managed plugins are currently not supported on Windows daemons.

## [Installing and using a plugin](#installing-and-using-a-plugin)

Plugins are distributed as Docker images and can be hosted on Docker Hub or on a private registry.

To install a plugin, use the `docker plugin install` command, which pulls the plugin from Docker Hub or your private registry, prompts you to grant permissions or capabilities if necessary, and enables the plugin.

To check the status of installed plugins, use the `docker plugin ls` command. Plugins that start successfully are listed as enabled in the output.

After a plugin is installed, you can use it as an option for another Docker operation, such as creating a volume.

In the following example, you install the [`rclone` plugin](https://rclone.org/docker/), verify that it is enabled, and use it to create a volume.

> Note
>
> This example is intended for instructional purposes only.

1. Set up the pre-requisite directories. By default they must exist on the host at the following locations:

   * `/var/lib/docker-plugins/rclone/config`. Reserved for the `rclone.conf` config file and must exist even if it's empty and the config file is not present.
   * `/var/lib/docker-plugins/rclone/cache`. Holds the plugin state file as well as optional VFS caches.

2. Install the `rclone` plugin.

   ```console
   $ docker plugin install rclone/docker-volume-rclone --alias rclone

   Plugin "rclone/docker-volume-rclone" is requesting the following privileges:
    - network: [host]
    - mount: [/var/lib/docker-plugins/rclone/config]
    - mount: [/var/lib/docker-plugins/rclone/cache]
    - device: [/dev/fuse]
    - capabilities: [CAP_SYS_ADMIN]
   Do you grant the above permissions? [y/N] 
   ```

   The plugin requests 5 privileges:

   * It needs access to the `host` network.

   * Access to pre-requisite directories to mount to store:

     * Your Rclone config files
     * Temporary cache data

   * Gives access to the FUSE (Filesystem in Userspace) device. This is required because Rclone uses FUSE to mount remote storage as if it were a local filesystem.

   * It needs the `CAP_SYS_ADMIN` capability, which allows the plugin to run the `mount` command.

3. Check that the plugin is enabled in the output of `docker plugin ls`.

   ```console
   $ docker plugin ls

   ID                    NAME                      DESCRIPTION                                ENABLED
   aede66158353          rclone:latest             Rclone volume plugin for Docker            true
   ```

4. Create a volume using the plugin. This example mounts the `/remote` directory on host `1.2.3.4` into a volume named `rclonevolume`.

   This volume can now be mounted into containers.

   ```console
   $ docker volume create \
     -d rclone \
     --name rclonevolume \
     -o type=sftp \
     -o path=remote \
     -o sftp-host=1.2.3.4 \
     -o sftp-user=user \
     -o "sftp-password=$(cat file_containing_password_for_remote_host)"
   ```

5. Verify that the volume was created successfully.

   ```console
   $ docker volume ls

   DRIVER              NAME
   rclone         rclonevolume
   ```

6. Start a container that uses the volume `rclonevolume`.

   ```console
   $ docker run --rm -v rclonevolume:/data busybox ls /data

   <content of /remote on machine 1.2.3.4>
   ```

7. Remove the volume `rclonevolume`

   ```console
   $ docker volume rm rclonevolume

   sshvolume
   ```

To disable a plugin, use the `docker plugin disable` command. To completely remove it, use the `docker plugin remove` command. For other available commands and options, see the [command line reference](https://docs.docker.com/reference/cli/docker/).

## [Developing a plugin](#developing-a-plugin)

#### [The rootfs directory](#the-rootfs-directory)

The `rootfs` directory represents the root filesystem of the plugin. In this example, it was created from a Dockerfile:

> Note
>
> The `/run/docker/plugins` directory is mandatory inside of the plugin's filesystem for Docker to communicate with the plugin.

```console
$ git clone https://github.com/vieux/docker-volume-sshfs
$ cd docker-volume-sshfs
$ docker build -t rootfsimage .
$ id=$(docker create rootfsimage true) # id was cd851ce43a403 when the image was created
$ sudo mkdir -p myplugin/rootfs
$ sudo docker export "$id" | sudo tar -x -C myplugin/rootfs
$ docker rm -vf "$id"
$ docker rmi rootfsimage
```

#### [The config.json file](#the-configjson-file)

The `config.json` file describes the plugin. See the [plugins config reference](https://docs.docker.com/engine/extend/config/).

Consider the following `config.json` file.

```json
{
  "description": "sshFS plugin for Docker",
  "documentation": "https://docs.docker.com/engine/extend/plugins/",
  "entrypoint": ["/docker-volume-sshfs"],
  "network": {
    "type": "host"
  },
  "interface": {
    "types": ["docker.volumedriver/1.0"],
    "socket": "sshfs.sock"
  },
  "linux": {
    "capabilities": ["CAP_SYS_ADMIN"]
  }
}
```

This plugin is a volume driver. It requires a `host` network and the `CAP_SYS_ADMIN` capability. It depends upon the `/docker-volume-sshfs` entrypoint and uses the `/run/docker/plugins/sshfs.sock` socket to communicate with Docker Engine. This plugin has no runtime parameters.

#### [Creating the plugin](#creating-the-plugin)

A new plugin can be created by running `docker plugin create <plugin-name> ./path/to/plugin/data` where the plugin data contains a plugin configuration file `config.json` and a root filesystem in subdirectory `rootfs`.

After that the plugin `<plugin-name>` will show up in `docker plugin ls`. Plugins can be pushed to remote registries with `docker plugin push <plugin-name>`.

## [Debugging plugins](#debugging-plugins)

Stdout of a plugin is redirected to dockerd logs. Such entries have a `plugin=<ID>` suffix. Here are a few examples of commands for pluginID `f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62` and their corresponding log entries in the docker daemon logs.

```console
$ docker plugin install tiborvass/sample-volume-plugin

INFO[0036] Starting...       Found 0 volumes on startup  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
```

```console
$ docker volume create -d tiborvass/sample-volume-plugin samplevol

INFO[0193] Create Called...  Ensuring directory /data/samplevol exists on host...  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0193] open /var/lib/docker/plugin-data/local-persist.json: no such file or directory  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0193]                   Created volume samplevol with mountpoint /data/samplevol  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0193] Path Called...    Returned path /data/samplevol  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
```

```console
$ docker run -v samplevol:/tmp busybox sh

INFO[0421] Get Called...     Found samplevol                plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0421] Mount Called...   Mounted samplevol              plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0421] Path Called...    Returned path /data/samplevol  plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
INFO[0421] Unmount Called... Unmounted samplevol            plugin=f52a3df433b9aceee436eaada0752f5797aab1de47e5485f1690a073b860ff62
```

#### [Using runc to obtain logfiles and shell into the plugin.](#using-runc-to-obtain-logfiles-and-shell-into-the-plugin)

Use `runc`, the default docker container runtime, for debugging plugins by collecting plugin logs redirected to a file.

```console
$ sudo runc --root /run/docker/runtime-runc/plugins.moby list

ID                                                                 PID         STATUS      BUNDLE                                                                                                                                       CREATED                          OWNER
93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25   15806       running     /run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby-plugins/93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25   2018-02-08T21:40:08.621358213Z   root
9b4606d84e06b56df84fadf054a21374b247941c94ce405b0a261499d689d9c9   14992       running     /run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby-plugins/9b4606d84e06b56df84fadf054a21374b247941c94ce405b0a261499d689d9c9   2018-02-08T21:35:12.321325872Z   root
c5bb4b90941efcaccca999439ed06d6a6affdde7081bb34dc84126b57b3e793d   14984       running     /run/docker/containerd/daemon/io.containerd.runtime.v1.linux/moby-plugins/c5bb4b90941efcaccca999439ed06d6a6affdde7081bb34dc84126b57b3e793d   2018-02-08T21:35:12.321288966Z   root
```

```console
$ sudo runc --root /run/docker/runtime-runc/plugins.moby exec 93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25 cat /var/log/plugin.log
```

If the plugin has a built-in shell, then exec into the plugin can be done as follows:

```console
$ sudo runc --root /run/docker/runtime-runc/plugins.moby exec -t 93f1e7dbfe11c938782c2993628c895cf28e2274072c4a346a6002446c949b25 sh
```

#### [Using curl to debug plugin socket issues.](#using-curl-to-debug-plugin-socket-issues)

To verify if the plugin API socket that the docker daemon communicates with is responsive, use curl. In this example, we will make API calls from the docker host to volume and network plugins using curl 7.47.0 to ensure that the plugin is listening on the said socket. For a well functioning plugin, these basic requests should work. Note that plugin sockets are available on the host under `/var/run/docker/plugins/<pluginID>`

```console
$ curl -H "Content-Type: application/json" -XPOST -d '{}' --unix-socket /var/run/docker/plugins/e8a37ba56fc879c991f7d7921901723c64df6b42b87e6a0b055771ecf8477a6d/plugin.sock http:/VolumeDriver.List

{"Mountpoint":"","Err":"","Volumes":[{"Name":"myvol1","Mountpoint":"/data/myvol1"},{"Name":"myvol2","Mountpoint":"/data/myvol2"}],"Volume":null}
```

```console
$ curl -H "Content-Type: application/json" -XPOST -d '{}' --unix-socket /var/run/docker/plugins/45e00a7ce6185d6e365904c8bcf62eb724b1fe307e0d4e7ecc9f6c1eb7bcdb70/plugin.sock http:/NetworkDriver.GetCapabilities

{"Scope":"local"}
```

When using curl 7.5 and above, the URL should be of the form `http://hostname/APICall`, where `hostname` is the valid hostname where the plugin is installed and `APICall` is the call to the plugin API.

For example, `http://localhost/VolumeDriver.List`

----
url: https://docs.docker.com/engine/security/trust/trust_sandbox/
----

# Play in a content trust sandbox

***

Table of contents

***

This page explains how to set up and use a sandbox for experimenting with trust. The sandbox allows you to configure and try trust operations locally without impacting your production images.

Before working through this sandbox, you should have read through the [trust overview](https://docs.docker.com/engine/security/trust/).

## [Prerequisites](#prerequisites)

These instructions assume you are running in Linux or macOS. You can run this sandbox on a local machine or on a virtual machine. You need to have privileges to run docker commands on your local machine or in the VM.

This sandbox requires you to install two Docker tools: Docker Engine >= 1.10.0 and Docker Compose >= 1.6.0. To install the Docker Engine, choose from the [list of supported platforms](https://docs.docker.com/engine/install/). To install Docker Compose, see the [detailed instructions here](https://docs.docker.com/compose/install/).

## [What is in the sandbox?](#what-is-in-the-sandbox)

If you are just using trust out-of-the-box you only need your Docker Engine client and access to the Docker Hub. The sandbox mimics a production trust environment, and sets up these additional components.

| Container       | Description                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| trustsandbox    | A container with the latest version of Docker Engine and with some preconfigured certificates. This is your sandbox where you can use the `docker` client to test trust operations. |
| Registry server | A local registry service.                                                                                                                                                           |
| Notary server   | The service that does all the heavy-lifting of managing trust                                                                                                                       |

This means you run your own content trust (Notary) server and registry. If you work exclusively with the Docker Hub, you would not need these components. They are built into the Docker Hub for you. For the sandbox, however, you build your own entire, mock production environment.

Within the `trustsandbox` container, you interact with your local registry rather than the Docker Hub. This means your everyday image repositories are not used. They are protected while you play.

When you play in the sandbox, you also create root and repository keys. The sandbox is configured to store all the keys and files inside the `trustsandbox` container. Since the keys you create in the sandbox are for play only, destroying the container destroys them as well.

By using a `docker-in-docker` image for the `trustsandbox` container, you also don't pollute your real Docker daemon cache with any images you push and pull. The images are stored in an anonymous volume attached to this container, and can be destroyed after you destroy the container.

## [Build the sandbox](#build-the-sandbox)

In this section, you use Docker Compose to specify how to set up and link together the `trustsandbox` container, the Notary server, and the Registry server.

1. Create a new `trustsandbox` directory and change into it.

   ```console
   $ mkdir trustsandbox
   $ cd trustsandbox
   ```

2. Create a file called `compose.yaml` with your favorite editor. For example, using vim:

   ```console
   $ touch compose.yaml
   $ vim compose.yaml
   ```

3. Add the following to the new file.

   ```yaml
   version: "2"
   services:
     notaryserver:
       image: dockersecurity/notary_autobuilds:server-v0.5.1
       volumes:
         - notarycerts:/var/lib/notary/fixtures
       networks:
         - sandbox
       environment:
         - NOTARY_SERVER_STORAGE_TYPE=memory
         - NOTARY_SERVER_TRUST_SERVICE_TYPE=local
     sandboxregistry:
       image: registry:3
       networks:
         - sandbox
       container_name: sandboxregistry
     trustsandbox:
       image: docker:dind
       networks:
         - sandbox
       volumes:
         - notarycerts:/notarycerts
       privileged: true
       container_name: trustsandbox
       entrypoint: ""
       command: |-
           sh -c '
               cp /notarycerts/root-ca.crt /usr/local/share/ca-certificates/root-ca.crt &&
               update-ca-certificates &&
               dockerd-entrypoint.sh --insecure-registry sandboxregistry:5000'
   volumes:
     notarycerts:
       external: false
   networks:
     sandbox:
       external: false
   ```

4. Save and close the file.

5. Run the containers on your local system.

   ```console
   $ docker compose up -d
   ```

   The first time you run this, the `docker-in-docker`, Notary server, and registry images are downloaded from Docker Hub.

## [Play in the sandbox](#play-in-the-sandbox)

Now that everything is setup, you can go into your `trustsandbox` container and start testing Docker content trust. From your host machine, obtain a shell in the `trustsandbox` container.

```console
$ docker container exec -it trustsandbox sh
/ #
```

### [Test some trust operations](#test-some-trust-operations)

Now, pull some images from within the `trustsandbox` container.

1. Download a `docker` image to test with.

   ```console
   / # docker pull docker/trusttest
   docker pull docker/trusttest
   Using default tag: latest
   latest: Pulling from docker/trusttest   
   b3dbab3810fc: Pull complete
   a9539b34a6ab: Pull complete
   Digest: sha256:d149ab53f8718e987c3a3024bb8aa0e2caadf6c0328f1d9d850b2a2a67f2819a
   Status: Downloaded newer image for docker/trusttest:latest
   ```

2. Tag it to be pushed to your sandbox registry:

   ```console
   / # docker tag docker/trusttest sandboxregistry:5000/test/trusttest:latest
   ```

3. Enable content trust.

   ```console
   / # export DOCKER_CONTENT_TRUST=1
   ```

4. Identify the trust server.

   ```console
   / # export DOCKER_CONTENT_TRUST_SERVER=https://notaryserver:4443
   ```

   This step is only necessary because the sandbox is using its own server. Normally, if you are using the Docker Public Hub this step isn't necessary.

5. Pull the test image.

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Error: remote trust data does not exist for sandboxregistry:5000/test/trusttest: notaryserver:4443 does not have trust data for      sandboxregistry:5000/test/trusttest
   ```

   You see an error, because this content doesn't exist on the `notaryserver` yet.

6. Push and sign the trusted image.

   ```console
   / # docker push sandboxregistry:5000/test/trusttest:latest
   The push refers to a repository [sandboxregistry:5000/test/trusttest]
   5f70bf18a086: Pushed
   c22f7bc058a9: Pushed
   latest: digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 size: 734
   Signing and pushing trust metadata
   You are about to create a new root signing key passphrase. This passphrase
   will be used to protect the most sensitive key in your signing system. Please
   choose a long, complex passphrase and be careful to keep the password and the
   key file itself secure and backed up. It is highly recommended that you use a
   password manager to generate the passphrase and keep it safe. There will be no
   way to recover this key. You can find the key in your config directory.
   Enter passphrase for new root key with ID 27ec255:
   Repeat passphrase for new root key with ID 27ec255:
   Enter passphrase for new repository key with ID 58233f9 (sandboxregistry:5000/test/trusttest):
   Repeat passphrase for new repository key with ID 58233f9 (sandboxregistry:5000/test/trusttest):
   Finished initializing "sandboxregistry:5000/test/trusttest"
   Successfully signed "sandboxregistry:5000/test/trusttest":latest
   ```

   Because you are pushing this repository for the first time, Docker creates new root and repository keys and asks you for passphrases with which to encrypt them. If you push again after this, it only asks you for repository passphrase so it can decrypt the key and sign again.

7. Try pulling the image you just pushed:

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926: Pulling from test/trusttest
   Digest: sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Status: Downloaded newer image for sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Tagging sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926 as sandboxregistry:5000   test/trusttest:latest
   ```

### [Test with malicious images](#test-with-malicious-images)

What happens when data is corrupted and you try to pull it when trust is enabled? In this section, you go into the `sandboxregistry` and tamper with some data. Then, you try and pull it.

1. Leave the `trustsandbox` shell and container running.

2. Open a new interactive terminal from your host, and obtain a shell into the `sandboxregistry` container.

   ```console
   $ docker container exec -it sandboxregistry bash
   root@65084fc6f047:/#
   ```

3. List the layers for the `test/trusttest` image you pushed:

   ```console
   root@65084fc6f047:/# ls -l /var/lib/registry/docker/registry/v2/repositories/test/trusttest/_layers/sha256
   total 12
   drwxr-xr-x 2 root root 4096 Jun 10 17:26 a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4
   drwxr-xr-x 2 root root 4096 Jun 10 17:26 aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
   drwxr-xr-x 2 root root 4096 Jun 10 17:26 cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
   ```

4. Change into the registry storage for one of those layers (this is in a different directory):

   ```console
   root@65084fc6f047:/# cd /var/lib/registry/docker/registry/v2/blobs/sha256/aa/aac0c133338db2b18ff054943cee3267fe50c75cdee969aed88b1992539ed042
   ```

5. Add malicious data to one of the `trusttest` layers:

   ```console
   root@65084fc6f047:/# echo "Malicious data" > data
   ```

6. Go back to your `trustsandbox` terminal.

7. List the `trusttest` image.

   ```console
   / # docker image ls | grep trusttest
   REPOSITORY                            TAG                 IMAGE ID            CREATED             SIZE
   docker/trusttest                      latest              cc7629d1331a        11 months ago       5.025 MB
   sandboxregistry:5000/test/trusttest   latest              cc7629d1331a        11 months ago       5.025 MB
   sandboxregistry:5000/test/trusttest   <none>              cc7629d1331a        11 months ago       5.025 MB
   ```

8. Remove the `trusttest:latest` image from your local cache.

   ```console
   / # docker image rm -f cc7629d1331a
   Untagged: docker/trusttest:latest
   Untagged: sandboxregistry:5000/test/trusttest:latest
   Untagged: sandboxregistry:5000/test/trusttest@sha256:ebf59c538accdf160ef435f1a19938ab8c0d6bd96aef8d4ddd1b379edf15a926
   Deleted: sha256:cc7629d1331a7362b5e5126beb5bf15ca0bf67eb41eab994c719a45de53255cd
   Deleted: sha256:2a1f6535dc6816ffadcdbe20590045e6cbf048d63fd4cc753a684c9bc01abeea
   Deleted: sha256:c22f7bc058a9a8ffeb32989b5d3338787e73855bf224af7aa162823da015d44c
   ```

   Docker does not re-download images that it already has cached, but you want Docker to attempt to download the tampered image from the registry and reject it because it is invalid.

9. Pull the image again. This downloads the image from the registry, because you don't have it cached.

   ```console
   / # docker pull sandboxregistry:5000/test/trusttest
   Using default tag: latest
   Pull (1 of 1): sandboxregistry:5000/test/trusttest:latest@sha256:35d5bc26fd358da8320c137784fe590d8fcf9417263ef261653e8e1c7f15672e
   sha256:35d5bc26fd358da8320c137784fe590d8fcf9417263ef261653e8e1c7f15672e: Pulling from test/trusttest

   aac0c133338d: Retrying in 5 seconds
   a3ed95caeb02: Download complete
   error pulling image configuration: unexpected EOF
   ```

   The pull did not complete because the trust system couldn't verify the image.

## [More play in the sandbox](#more-play-in-the-sandbox)

Now, you have a full Docker content trust sandbox on your local system, feel free to play with it and see how it behaves. If you find any security issues with Docker, feel free to send us an email at <security@docker.com>.

## [Clean up your sandbox](#clean-up-your-sandbox)

When you are done, and want to clean up all the services you've started and any anonymous volumes that have been created, just run the following command in the directory where you've created your Docker Compose file:

```console
$ docker compose down -v
```

----
url: https://docs.docker.com/reference/cli/docker/mcp/profile/server/
----

# docker mcp profile server

***

| Description | Manage servers in profiles |
| ----------- | -------------------------- |

## [Description](#description)

Manage servers in profiles

## [Subcommands](#subcommands)

| Command                                                                                                       | Description                       |
| ------------------------------------------------------------------------------------------------------------- | --------------------------------- |
| [`docker mcp profile server add`](https://docs.docker.com/reference/cli/docker/mcp/profile/server/add/)       | Add MCP servers to a profile      |
| [`docker mcp profile server ls`](https://docs.docker.com/reference/cli/docker/mcp/profile/server/ls/)         | List servers across profiles      |
| [`docker mcp profile server remove`](https://docs.docker.com/reference/cli/docker/mcp/profile/server/remove/) | Remove MCP servers from a profile |

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/
----

# Hardened Docker Desktop

***

Table of contents

***

Subscription: Business

For: Administrators

Hardened Docker Desktop provides a collection of security features designed to strengthen developer environments without compromising productivity or developer experience.

With Hardened Docker Desktop, you can enforce strict security policies that prevent developers and containers from bypassing organizational controls. You can also enhance container isolation to protect against security threats like malicious payloads that might breach the Docker Desktop Linux VM or underlying host system.

## [Who should use Hardened Docker Desktop?](#who-should-use-hardened-docker-desktop)

Hardened Docker Desktop is ideal for security-focused organizations that:

* Don't provide root or administrator access to developers' machines
* Want centralized control over Docker Desktop configurations
* Must meet specific compliance requirements

## [How Hardened Docker Desktop works](#how-hardened-docker-desktop-works)

Hardened Docker Desktop features work independently and together to create a defense-in-depth security strategy. They protect developer workstations against attacks across multiple layers, including Docker Desktop configuration, container image management, and container runtime security:

* Registry Access Management and Image Access Management prevent access to unauthorized container registries and image types, reducing exposure to malicious payloads
* Enhanced Container Isolation runs containers without root privileges inside a Linux user namespace, limiting the impact of malicious containers
* Air-gapped containers let you configure network restrictions for containers, preventing malicious containers from accessing your organization's internal network resources
* Namespace access controls whether organization members can push content to their personal Docker Hub namespaces, preventing accidental publication of images outside approved locations
* Settings Management locks down Docker Desktop configurations to enforce company policies and prevent developers from introducing insecure settings, whether intentionally or accidentally

## [Next steps](#next-steps)

Explore Hardened Docker Desktop features to understand how they can strengthen your organization's security posture:

### [Namespace access](/enterprise/security/hardened-desktop/namespace-access/)

[Control whether organization members can push content to their personal namespaces.](/enterprise/security/hardened-desktop/namespace-access/)

----
url: https://docs.docker.com/dhi/resources/
----

# Docker Hardened Images resources

***

Table of contents

***

This page provides links to additional resources related to Docker Hardened Images (DHI), including guides, Docker Hub resources, and GitHub repositories.

For product information and feature comparison, visit the [Docker Hardened Images product page](https://www.docker.com/products/hardened-images/).

## [Guides](#guides)

For guides that demonstrate how to use Docker Hardened Images in various scenarios, see the [guides section filtered by DHI](/guides/?tags=dhi).

## [Docker Hub](#docker-hub)

Docker Hardened Images are available on Docker Hub:

* [Docker Hardened Images Catalog](https://dhi.io): Browse and pull Docker Hardened Images from the official catalog
* [Docker Hub MCP Server](https://hub.docker.com/mcp/server/dockerhub/overview): MCP server to list Docker Hardened Images (DHIs) available in your organizations

## [GitHub repositories and resources](#github-repositories-and-resources)

Docker Hardened Images repositories are available in the [docker-hardened-images](https://github.com/docker-hardened-images) GitHub organization:

* [Catalog](https://github.com/docker-hardened-images/catalog): DHI definition files and catalog metadata
* [Advisories](https://github.com/docker-hardened-images/advisories): CVE advisories for OSS packages distributed with DHIs
  * [Scanner vendor integration guide](https://github.com/docker-hardened-images/advisories/tree/main/integration): Reference for scanner vendors integrating DHI VEX support
* [Keyring](https://github.com/docker-hardened-images/keyring): Public signing keys and verification tools
* [Log](https://github.com/docker-hardened-images/log): Log of references (tag > digest) for Docker Hardened Images
* [dhictl](https://github.com/docker-hardened-images/dhictl): Command-line interface for managing and interacting with Docker Hardened Images
* [Terraform Provider](https://github.com/docker-hardened-images/terraform-provider-dhi): Terraform provider for managing DHI resources ([Terraform Registry](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs))
* [Discussions](https://github.com/orgs/docker-hardened-images/discussions): Community forum and product discussions

## [Additional resources](#additional-resources)

* [Start a free trial](https://hub.docker.com/hardened-images/start-free-trial): Explore DHI Select and Enterprise features including FIPS/STIG variants, customization, and SLA-backed support
* [Support Service Level Agreement](https://docs.docker.com/go/dhi-sla/): Review the SLA commitments for DHI Select and Enterprise subscriptions
* [Request a demo](https://www.docker.com/products/hardened-images/#getstarted): Get a personalized demo and information about DHI Select and Enterprise subscriptions
* [Request an image](https://github.com/docker-hardened-images/catalog/issues): Submit a request for a specific Docker Hardened Image
* [Contact Sales](https://www.docker.com/pricing/contact-sales/): Connect with Docker sales team for enterprise inquiries
* [Docker Support](https://www.docker.com/support/): Access support resources for DHI Select and Enterprise customers

----
url: https://docs.docker.com/reference/cli/docker/container/kill/
----

# docker container kill

***

| Description                                                               | Kill one or more running containers                        |
| ------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Usage                                                                     | `docker container kill [OPTIONS] CONTAINER [CONTAINER...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker kill`                                              |

## [Description](#description)

The `docker kill` subcommand kills one or more containers. The main process inside the container is sent `SIGKILL` signal (default), or the signal that is specified with the `--signal` option. You can reference a container by its ID, ID-prefix, or name.

The `--signal` flag sets the system call signal that is sent to the container. This signal can be a signal name in the format `SIG<NAME>`, for instance `SIGINT`, or an unsigned number that matches a position in the kernel's syscall table, for instance `2`.

While the default (`SIGKILL`) signal will terminate the container, the signal set through `--signal` may be non-terminal, depending on the container's main process. For example, the `SIGHUP` signal in most cases will be non-terminal, and the container will continue running after receiving the signal.

> Note
>
> `ENTRYPOINT` and `CMD` in the *shell* form run as a child process of `/bin/sh -c`, which does not pass signals. This means that the executable is not the container’s PID 1 and does not receive Unix signals.

## [Options](#options)

| Option                    | Default | Description                     |
| ------------------------- | ------- | ------------------------------- |
| [`-s, --signal`](#signal) |         | Signal to send to the container |

## [Examples](#examples)

### [Send a KILL signal to a container](#send-a-kill-signal-to-a-container)

The following example sends the default `SIGKILL` signal to the container named `my_container`:

```console
$ docker kill my_container
```

### [Send a custom signal to a container (--signal)](#signal)

The following example sends a `SIGHUP` signal to the container named `my_container`:

```console
$ docker kill --signal=SIGHUP  my_container
```

You can specify a custom signal either by *name*, or *number*. The `SIG` prefix is optional, so the following examples are equivalent:

```console
$ docker kill --signal=SIGHUP my_container
$ docker kill --signal=HUP my_container
$ docker kill --signal=1 my_container
```

Refer to the [`signal(7)`](https://man7.org/linux/man-pages/man7/signal.7.html) man-page for a list of standard Linux signals.

----
url: https://docs.docker.com/guides/testcontainers-java-wiremock/run-tests/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

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

You built a Spring Boot application that integrates with an external REST API, then tested that integration using three different approaches:

* WireMock JUnit 5 extension with inline stubs
* WireMock JUnit 5 extension with JSON mapping files
* Testcontainers WireMock module running WireMock in a Docker container

Testing at the HTTP protocol level instead of mocking Java methods lets you catch serialization issues and simulate realistic failure scenarios.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Testcontainers WireMock module](https://testcontainers.com/modules/wiremock/)
* [WireMock documentation](https://wiremock.org/docs/)
* [Testcontainers JUnit 5 quickstart](https://java.testcontainers.org/quickstart/junit_5_quickstart/)

----
url: https://docs.docker.com/engine/network/drivers/host/
----

# Host network driver

***

Table of contents

***

If you use the `host` network mode for a container, that container's network stack isn't isolated from the Docker host (the container shares the host's networking namespace), and the container doesn't get its own IP-address allocated. For instance, if you run a container which binds to port 80 and you use `host` networking, the container's application is available on port 80 on the host's IP address.

> Note
>
> Given that the container does not have its own IP-address when using `host` mode networking, [port-mapping](https://docs.docker.com/engine/network/drivers/overlay/#publish-ports) doesn't take effect, and the `-p`, `--publish`, `-P`, and `--publish-all` option are ignored, producing a warning instead:
>
> ```console
> WARNING: Published ports are discarded when using host network mode
> ```

Host mode networking can be useful for the following use cases:

* To optimize performance
* In situations where a container needs to handle a large range of ports

This is because it doesn't require network address translation (NAT), and no "userland-proxy" is created for each port.

## [Platform support](#platform-support)

The host networking driver is supported on:

* Docker Engine on Linux
* Docker Desktop version 4.34 and later (requires enabling the feature in Settings)

> Note
>
> For Docker Desktop users, see the [Docker Desktop section](#docker-desktop) below for setup instructions.

You can also use a `host` network for a swarm service, by passing `--network host` to the `docker service create` command. In this case, control traffic (traffic related to managing the swarm and the service) is still sent across an overlay network, but the individual swarm service containers send data using the Docker daemon's host network and ports. This creates some extra limitations. For instance, if a service container binds to port 80, only one service container can run on a given swarm node.

## [Docker Desktop](#docker-desktop)

Host networking is supported on Docker Desktop version 4.34 and later. To enable this feature:

1. Sign in to your Docker account in Docker Desktop.
2. Navigate to **Settings**.
3. Under the **Resources** tab, select **Network**.
4. Check the **Enable host networking** option.
5. Select **Apply and restart**.

This feature works in both directions. This means you can access a server that is running in a container from your host and you can access servers running on your host from any container that is started with host networking enabled. TCP as well as UDP are supported as communication protocols.

### [Examples](#examples)

The following command starts netcat in a container that listens on port `8000`:

```console
$ docker run --rm -it --net=host nicolaka/netshoot nc -lkv 0.0.0.0 8000
```

Port `8000` will then be available on the host and you can connect to it with the following command from another terminal:

```console
$ nc localhost 8000
```

What you type in here will then appear on the terminal where the container is running.

To access a service running on the host from the container, you can start a container with host networking enabled with this command:

```console
$ docker run --rm -it --net=host nicolaka/netshoot
```

If you then want to access a service on your host from the container (in this example a web server running on port `80`), you can do it like this:

```console
$ nc localhost 80
```

### [Limitations](#limitations)

* Processes inside the container cannot bind to the IP addresses of the host because the container has no direct access to the interfaces of the host.
* The host network feature of Docker Desktop works on layer 4. This means that unlike with Docker on Linux, network protocols that operate below TCP or UDP are not supported.
* This feature doesn't work with Enhanced Container Isolation enabled, since isolating your containers from the host and allowing them access to the host network contradict each other.
* Only Linux containers are supported. Host networking does not work with Windows containers.

## [Usage example](#usage-example)

This example shows how to start an Nginx container that binds directly to port 80 on the Docker host. From a networking perspective, this provides the same level of isolation as if Nginx were running directly on the host, but the container remains isolated in all other aspects (storage, process namespace, user namespace).

### [Prerequisites](#prerequisites)

* Port 80 must be available on the Docker host. To make Nginx listen on a different port, see the [Nginx image documentation](https://hub.docker.com/_/nginx/).
* The host networking driver only works on Linux hosts, and as an opt-in feature in Docker Desktop version 4.34 and later.

### [Steps](#steps)

1. Create and start the container as a detached process. The `--rm` option removes the container when it exits. The `-d` flag starts it in the background:

   ```console
   $ docker run --rm -d --network host --name my_nginx nginx
   ```

2. Access Nginx by browsing to <http://localhost:80/>.

3. Examine your network stack:

   Check all network interfaces and verify that no new interface was created:

   ```console
   $ ip addr show
   ```

   Verify which process is bound to port 80 using `netstat`. You need `sudo` because the process is owned by the Docker daemon user:

   ```console
   $ sudo netstat -tulpn | grep :80
   ```

4. Stop the container. It's removed automatically because of the `--rm` option:

   ```console
   $ docker container stop my_nginx
   ```

## [Next steps](#next-steps)

* Learn about [networking from the container's point of view](https://docs.docker.com/engine/network/)
* Learn about [bridge networks](https://docs.docker.com/engine/network/drivers/bridge/)
* Learn about [overlay networks](https://docs.docker.com/engine/network/drivers/overlay/)
* Learn about [Macvlan networks](https://docs.docker.com/engine/network/drivers/macvlan/)

----
url: https://docs.docker.com/dhi/release-notes/platform/
----

# Docker Hardened Images release notes

***

Table of contents

***

This page contains information about the new features, improvements, and changes in the Docker Hardened Images (DHI) platform. Release notes are aggregated by quarter and include only notable product changes.

## [Q2 2026](#q2-2026)

New features and enhancements released in the second quarter of 2026.

* Debian Hardened System Packages: Added support for Debian-based Docker Hardened System Packages (HSP), including new CLI workflows for authenticating to the Debian HSP repository.
* Mend.io scanner integration: Mend.io is now a supported scanner for consuming DHI VEX data.
* Black Duck scanner integration: Black Duck is now a supported scanner for consuming DHI VEX data.
* DHI Select self-serve purchase: DHI Select is now available for self-serve purchase directly through the Docker website.
* Bulk customization: Apply customizations to multiple images in a single operation through the Docker Hub UI and the CLI.
* Terraform provider: Manage DHI resources, including customizations and mirrors, using the official Terraform provider.

## [Q1 2026](#q1-2026)

New features and enhancements released in the first quarter of 2026.

* Docker Hardened System Packages (HSP): Announced Docker Hardened System Packages, a new offering that provides individually hardened packages for use in your own base images. For more information, see the [announcement blog post](https://www.docker.com/blog/announcing-docker-hardened-system-packages/).
* Wiz scanner integration: Wiz is now a supported scanner for consuming DHI VEX data.

## [Q4 2025](#q4-2025)

New features and enhancements released in the fourth quarter of 2025.

* Docker Hardened Images Community (Free): Docker Hardened Images are now available for every developer through a Community subscription tier. The subscription tiers are now Community, Select, and Enterprise. For more information, see the [announcement blog post](https://www.docker.com/blog/docker-hardened-images-for-every-developer/).
* Independent security validation by SRLabs: SRLabs published an independent security validation of Docker Hardened Images. See the [validation announcement](https://www.docker.com/blog/docker-hardened-images-security-independently-validated-by-srlabs/).
* Docker Scout scoring for DHI: Docker Scout image scoring now accounts for the security improvements provided by DHI.
* Trivy VEX repository: VEX data for DHI is published in a Trivy-compatible OCI VEX repository, making it easier for Trivy and other scanners to consume.
* Docker Scout DHI policy: New Docker Scout policy that evaluates whether images use Docker Hardened Images.
* Hardened Helm charts (Beta): Beta release of Docker Hardened Helm Charts. For more information, see the [announcement blog post](https://www.docker.com/blog/docker-hardened-images-helm-charts-beta/).
* Mirroring UX: Updated the mirroring experience in Docker Hub with a refreshed UI and clearer flows.

## [Q3 2025](#q3-2025)

New features and enhancements released in the third quarter of 2025.

* Next evolution release: A major release that introduced customizations, FedRAMP-ready images, the AI Migration Agent, and deeper scanner integrations. See the [announcement blog post](https://www.docker.com/blog/the-next-evolution-of-docker-hardened-images/) and the [FedRAMP compliance blog post](https://www.docker.com/blog/fedramp-compliance-with-hardened-images/).
* DHI customizations: Customize DHI images directly from the Docker Hub UI, with options for adding packages, files, and configuration on top of a base hardened image.
* AI Migration Agent: AI-assisted Dockerfile migration to help convert existing Dockerfiles to use Docker Hardened Images.
* CIS compliance attestations: CIS benchmark compliance attestations are now included with DHI images.
* STIG variants: STIG-hardened image variants for U.S. Department of Defense compliance use cases.

## [Q2 2025](#q2-2025)

New features and enhancements released in the second quarter of 2025.

* Docker Hardened Images launch: Docker announced Docker Hardened Images, a new family of secure, minimal, and production-ready container images maintained by Docker. For more information, see the [launch blog post](https://www.docker.com/blog/introducing-docker-hardened-images/).
* FIPS variants: FIPS-validated image variants for Docker Hardened Images.

----
url: https://docs.docker.com/build/exporters/local-tar/
----

# Local and tar exporters

***

Table of contents

***

The `local` and `tar` exporters output the root filesystem of the build result into a local directory. They're useful for producing artifacts that aren't container images.

* `local` exports files and directories.
* `tar` exports the same, but bundles the export into a tarball.

## [Synopsis](#synopsis)

Build a container image using the `local` exporter:

```console
$ docker buildx build --output type=local[,parameters] .
$ docker buildx build --output type=tar[,parameters] .
```

The following table describes the available parameters:

| Parameter        | Type    | Default | Description                                                                       |
| ---------------- | ------- | ------- | --------------------------------------------------------------------------------- |
| `dest`           | String  |         | Path to copy files to                                                             |
| `platform-split` | Boolean | `true`  | `local` exporter only. Split multi-platform outputs into platform subdirectories. |

## [Multi-platform builds with local exporter](#multi-platform-builds-with-local-exporter)

The `platform-split` parameter controls how multi-platform build outputs are organized.

Consider this Dockerfile that creates platform-specific files:

```dockerfile
FROM busybox AS build
ARG TARGETOS
ARG TARGETARCH
RUN mkdir /out && echo foo > /out/hello-$TARGETOS-$TARGETARCH

FROM scratch
COPY --from=build /out /
```

### [Split by platform (default)](#split-by-platform-default)

By default, the local exporter creates a separate subdirectory for each platform:

```console
$ docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --output type=local,dest=./output \
  .
```

This produces the following directory structure:

```text
output/
├── linux_amd64/
│   └── hello-linux-amd64
└── linux_arm64/
    └── hello-linux-arm64
```

### [Merge all platforms](#merge-all-platforms)

To merge files from all platforms into the same directory, set `platform-split=false`:

```console
$ docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --output type=local,dest=./output,platform-split=false \
  .
```

This produces a flat directory structure:

```text
output/
├── hello-linux-amd64
└── hello-linux-arm64
```

Files from all platforms merge into a single directory. If multiple platforms produce files with identical names, the export fails with an error.

### [Single-platform builds](#single-platform-builds)

Single-platform builds export directly to the destination directory without creating a platform subdirectory:

```console
$ docker buildx build \
  --platform linux/amd64 \
  --output type=local,dest=./output \
  .
```

This produces:

```text
output/
└── hello-linux-amd64
```

To include the platform subdirectory even for single-platform builds, explicitly set `platform-split=true`:

```console
$ docker buildx build \
  --platform linux/amd64 \
  --output type=local,dest=./output,platform-split=true \
  .
```

This produces:

```text
output/
└── linux_amd64/
    └── hello-linux-amd64
```

## [Further reading](#further-reading)

For more information on the `local` or `tar` exporters, see the [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#local-directory).

----
url: https://docs.docker.com/scout/policy/view/
----

# View Docker Scout policy status

***

Table of contents

***

You can track policy status for your artifacts from the [Docker Scout Dashboard](#dashboard), or using the [CLI](#cli).

## [Dashboard](#dashboard)

The **Overview** tab of the [Docker Scout Dashboard](https://scout.docker.com/) displays a summary of recent changes in policy for your repositories. This summary shows images that have seen the most change in their policy evaluation between the most recent image and the previous image.

### [Policy status per repository](#policy-status-per-repository)

The **Images** tab shows the current policy status, and recent policy trend, for all images in the selected environment. The **Policy status** column in the list shows:

* Number of fulfilled policies versus the total number of policies
* Recent policy trends

The policy trend, denoted by the directional arrows, indicates whether an image is better, worse, or unchanged in terms of policy, compared to the previous image in the same environment.

* The green arrow pointing upwards shows the number of policies that got better in the latest pushed image.
* The red arrow pointing downwards shows the number of policies that got worse in the latest pushed image.
* The bidirectional gray arrow shows the number of policies that were unchanged in the latest version of this image.

If you select a repository, you can open the **Policy** tab for a detailed description of the policy delta for the most recently analyzed image and its predecessor.

### [Detailed results and remediation](#detailed-results-and-remediation)

To view the full evaluation results for an image, navigate to the image tag in the Docker Scout Dashboard and open the **Policy** tab. This shows a breakdown for all policy violations for the current image.

This view also provides recommendations on how to improve policy status for violated policies.

For vulnerability-related policies, the policy details view displays the fix version that removes the vulnerability, when a fix version is available. To fix the issue, upgrade the package version to the fix version.

For licensing-related policies, the list shows all packages whose license doesn't meet the policy criteria. To fix the issue, find a way to remove the dependency to the violating package, for example by looking for an alternative package distributed under a more appropriate license.

## [CLI](#cli)

To view policy status for an image from the CLI, use the `docker scout policy` command.

```console
$ docker scout policy \
  --org dockerscoutpolicy \
  --platform linux/amd64 \
  dockerscoutpolicy/email-api-service:0.0.2

    ✓ Pulled
    ✓ Policy evaluation results found


​## Overview
​
​             │               Analyzed Image
​─────────────┼──────────────────────────────────────────────
​  Target     │  dockerscoutpolicy/email-api-service:0.0.2
​    digest   │  17b1fde0329c
​    platform │ linux/amd64
​
​
​## Policies
​
​Policy status  FAILED  (2/8 policies met, 3 missing data)
​
​  Status │                  Policy                             │           Results
​─────────┼─────────────────────────────────────────────────────┼──────────────────────────────
​  ✓      │ No copyleft licenses                                │    0 packages
​  !      │ Default non-root user                               │
​  !      │ No fixable critical or high vulnerabilities         │    2C     1H     0M     0L
​  ✓      │ No high-profile vulnerabilities                     │    0C     0H     0M     0L
​  ?      │ No outdated base images                             │    No data
​         │                                                     │    Learn more ↗
​  ?      │ SonarQube quality gates passed                      │    No data
​         │                                                     │    Learn more ↗
​  !      │ Supply chain attestations                           │    2 deviations
​  ?      │ No unapproved base images                           │    No data

...
```

For more information about the command, refer to the [CLI reference](/reference/cli/docker/scout/policy/).

----
url: https://docs.docker.com/reference/samples/rust/
----

# Rust samples

| Name                                                                                                   | Description                                                             |
| ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- |
| [React / Rust / PostgreSQL](https://github.com/docker/awesome-compose/tree/master/react-rust-postgres) | A sample React application with a Rust backend and a Postgres database. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/admin/
----

# Administration

***

Table of contents

***

Administrators can manage companies and organizations using the [Docker Admin Console](https://app.docker.com/admin). The Admin Console provides centralized observability, access management, and security controls across Docker environments.

## [Company and organization hierarchy](#company-and-organization-hierarchy)

The [Docker Admin Console](https://app.docker.com/admin) provides administrators with centralized observability, access management, and controls for their company and organizations. To provide these features, Docker uses the following hierarchy and roles.

### [Company](#company)

A company groups multiple Docker organizations for centralized configuration. Companies have the company owner administrator role available.

The company owner:

* Can view and manage all organizations within the company
* Has full access to company-wide settings and inherits the same permissions as organization owners
* Does not occupy a seat

Companies are only available for Docker Business subscribers.

### [Organization](#organization)

Organization owners have the organization owner administrator role available. They can manage organization settings, users, and access controls, but occupy a [seat](https://docs.docker.com/admin/organization/organization-faqs/#what-is-the-difference-between-user-invitee-seat-and-member).

* An organization contains teams and repositories.
* All Docker Team and Business subscribers must have at least one organization.

> Tip
>
> [Upgrading to a Docker Business plan](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdmin) grants you the company owner role so you can manage multiple organizations.

### [Team](#team)

Teams are optional and let you group members to assign repository permissions collectively. Teams simplify permission management across projects or functions.

### [Member](#member)

A member is any Docker user added to an organization. Organization and company owners can assign roles to members to define their level of access.

## [Admin Console features](#admin-console-features)

Docker's [Admin Console](https://app.docker.com/admin) allows you to:

* Create and manage companies and organizations
* Assign roles and permissions to members
* Group members into teams to manage access by project or role
* Set company-wide policies, including SCIM provisioning and security enforcement

## [Manage companies and organizations](#manage-companies-and-organizations)

Learn how to manage companies and organizations in the following sections.

### [Company administration](/admin/company/)

[Explore how to manage a company.](/admin/company/)

### [Organization administration](/admin/organization/)

[Learn about organization administration.](/admin/organization/)

### [Onboard your organization](/admin/organization/setup/onboard)

[Learn how to onboard and secure your organization.](/admin/organization/setup/onboard)

### [Company FAQ](/faq/admin/company-faqs/)

[Discover common questions and answers about companies.](/faq/admin/company-faqs/)

### [Organization FAQ](/faq/admin/organization-faqs/)

[Explore popular FAQ topics about organizations.](/faq/admin/organization-faqs/)

### [Security](/security/)

[Explore security features for administrators.](/security/)

----
url: https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/
----

# How services work

***

Table of contents

***

To deploy an application image when Docker Engine is in Swarm mode, you create a service. Frequently a service is the image for a microservice within the context of some larger application. Examples of services might include an HTTP server, a database, or any other type of executable program that you wish to run in a distributed environment.

When you create a service, you specify which container image to use and which commands to execute inside running containers. You also define options for the service including:

* The port where the swarm makes the service available outside the swarm
* An overlay network for the service to connect to other services in the swarm
* CPU and memory limits and reservations
* A rolling update policy
* The number of replicas of the image to run in the swarm

## [Services, tasks, and containers](#services-tasks-and-containers)

When you deploy the service to the swarm, the swarm manager accepts your service definition as the desired state for the service. Then it schedules the service on nodes in the swarm as one or more replica tasks. The tasks run independently of each other on nodes in the swarm.

For example, imagine you want to load balance between three instances of an HTTP listener. The diagram below shows an HTTP listener service with three replicas. Each of the three instances of the listener is a task in the swarm.

A container is an isolated process. In the Swarm mode model, each task invokes exactly one container. A task is analogous to a “slot” where the scheduler places a container. Once the container is live, the scheduler recognizes that the task is in a running state. If the container fails health checks or terminates, the task terminates.

## [Tasks and scheduling](#tasks-and-scheduling)

A task is the atomic unit of scheduling within a swarm. When you declare a desired service state by creating or updating a service, the orchestrator realizes the desired state by scheduling tasks. For instance, you define a service that instructs the orchestrator to keep three instances of an HTTP listener running at all times. The orchestrator responds by creating three tasks. Each task is a slot that the scheduler fills by spawning a container. The container is the instantiation of the task. If an HTTP listener task subsequently fails its health check or crashes, the orchestrator creates a new replica task that spawns a new container.

A task is a one-directional mechanism. It progresses monotonically through a series of states: `ASSIGNED`, `PREPARING`, `RUNNING`, etc. If the task fails, the orchestrator removes the task and its container and then creates a new task to replace it according to the desired state specified by the service.

The underlying logic of Docker's Swarm mode is a general purpose scheduler and orchestrator. The service and task abstractions themselves are unaware of the containers they implement. Hypothetically, you could implement other types of tasks such as virtual machine tasks or non-containerized process tasks. The scheduler and orchestrator are agnostic about the type of the task. However, Docker only supports container tasks.

The diagram below shows how Swarm mode accepts service create requests and schedules tasks to worker nodes.

### [Pending services](#pending-services)

A service may be configured in such a way that no node currently in the swarm can run its tasks. In this case, the service remains in state `pending`. Here are a few examples of when a service might remain in state `pending`.

> Tip
>
> If your only intention is to prevent a service from being deployed, scale the service to 0 instead of trying to configure it in such a way that it remains in `pending`.

* If all nodes are paused or drained, and you create a service, it is pending until a node becomes available. In reality, the first node to become available gets all of the tasks, so this is not a good thing to do in a production environment.

* You can reserve a specific amount of memory for a service. If no node in the swarm has the required amount of memory, the service remains in a pending state until a node is available which can run its tasks. If you specify a very large value, such as 500 GB, the task stays pending forever, unless you really have a node which can satisfy it.

* You can impose placement constraints on the service, and the constraints may not be able to be honored at a given time.

This behavior illustrates that the requirements and configuration of your tasks are not tightly tied to the current state of the swarm. As the administrator of a swarm, you declare the desired state of your swarm, and the manager works with the nodes in the swarm to create that state. You do not need to micro-manage the tasks on the swarm.

## [Replicated and global services](#replicated-and-global-services)

There are two types of service deployments, replicated and global.

For a replicated service, you specify the number of identical tasks you want to run. For example, you decide to deploy an HTTP service with three replicas, each serving the same content.

A global service is a service that runs one task on every node. There is no pre-specified number of tasks. Each time you add a node to the swarm, the orchestrator creates a task and the scheduler assigns the task to the new node. Good candidates for global services are monitoring agents, anti-virus scanners or other types of containers that you want to run on every node in the swarm.

The diagram below shows a three-service replica in gray and a global service in black.

## [Learn more](#learn-more)

* Read about how Swarm mode [nodes](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/) work.
* Learn how [PKI](https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/) works in Swarm mode.

----
url: https://docs.docker.com/compose/install/standalone/
----

# Install the Docker Compose standalone (Legacy)

***

Table of contents

***

> Warning
>
> This install scenario is not recommended and is only supported for backward compatibility purposes. Use [Docker Desktop](https://docs.docker.com/desktop/) or the [Docker Compose plugin](https://docs.docker.com/compose/install/linux/) instead. Use the standalone binary only if you cannot use either of these options.

This page contains instructions on how to install Docker Compose standalone on Linux or Windows Server, from the command line.

> Warning
>
> The Docker Compose standalone uses the `-compose` syntax instead of the current standard syntax `compose`.\
> For example, you must type `docker-compose up` when using Docker Compose standalone, instead of `docker compose up`. Use it only for backward compatibility.

## [On Linux](#on-linux)

1. To download and install the Docker Compose standalone, run:

   ```console
   $ curl -SL https://github.com/docker/compose/releases/download/v5.1.2/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose
   ```

2. Apply executable permissions to the standalone binary in the target path for the installation.

   ```console
   $ chmod +x /usr/local/bin/docker-compose
   ```

3. Test and execute Docker Compose commands using `docker-compose`.

> Tip
>
> If the command `docker-compose` fails after installation, check your path. You can also create a symbolic link to `/usr/bin` or any other directory in your path. For example:
>
> ```console
> $ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
> ```

## [On Windows Server](#on-windows-server)

Follow these instructions if you are [running the Docker daemon directly on Microsoft Windows Server](https://docs.docker.com/engine/install/binaries/#install-server-and-client-binaries-on-windows) and want to install Docker Compose.

1. Run PowerShell as an administrator. In order to proceed with the installation, select **Yes** when asked if you want this app to make changes to your device.

2. Optional. Ensure TLS1.2 is enabled. GitHub requires TLS1.2 for secure connections. If you’re using an older version of Windows Server, for example 2016, or suspect that TLS1.2 is not enabled, run the following command in PowerShell:

   ```powershell
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   ```

3. Download the latest release of Docker Compose (v5.1.2). Run the following command:

   ```powershell
    Start-BitsTransfer -Source "https://github.com/docker/compose/releases/download/v5.1.2/docker-compose-windows-x86_64.exe" -Destination $Env:ProgramFiles\Docker\docker-compose.exe
   ```

   To install a different version of Docker Compose, substitute `v5.1.2` with the version of Compose you want to use.

   > Note
   >
   > On Windows Server 2019 you can add the Compose executable to `$Env:ProgramFiles\Docker`. Because this directory is registered in the system `PATH`, you can run the `docker-compose --version` command on the subsequent step with no additional configuration.

4. Test the installation.

   ```console
   $ docker-compose.exe version
   Docker Compose version v5.1.2
   ```

## [What's next?](#whats-next)

* [Understand how Compose works](https://docs.docker.com/compose/intro/compose-application-model/)
* [Try the Quickstart guide](https://docs.docker.com/compose/gettingstarted/)

----
url: https://docs.docker.com/guides/genai-leveraging-rag/
----

[Leveraging RAG in GenAI to teach new information](https://docs.docker.com/guides/genai-leveraging-rag/)

This guide explains setting up a GenAI stack with Retrieval-Augmented Generation (RAG) and Neo4j, covering key concepts, deployment steps, and a case study. It also includes troubleshooting tips for optimizing AI performance with real-time data.

AI

35 minutes

[« Back to all guides](/guides/)

# Leveraging RAG in GenAI to teach new information

***

Table of contents

***

## [Introduction](#introduction)

Retrieval-Augmented Generation (RAG) is a powerful framework that enhances large language models (LLMs) by integrating information retrieval from external knowledge sources. This guide focuses on a specialized RAG implementation using graph databases like Neo4j, which excel in managing highly connected, relational data. Unlike traditional RAG setups with vector databases, combining RAG with graph databases offers better context-awareness and relationship-driven insights.

In this guide, you will:

* Explore the advantages of integrating graph databases into a RAG framework.
* Configure a GenAI stack with Docker, incorporating Neo4j and an AI model.
* Analyze a real-world case study that highlights the effectiveness of this approach for handling specialized queries.

## [Understanding RAG](#understanding-rag)

RAG is a hybrid framework that enhances the capabilities of large language models by integrating information retrieval. It combines three core components:

* **Information retrieval** from an external knowledge base
* **Large Language Model (LLM)** for generating responses
* **Vector embeddings** to enable semantic search

In a RAG system, vector embeddings are used to represent the semantic meaning of text in a way that a machine can understand and process. For instance, the words "dog" and "puppy" will have similar embeddings because they share similar meanings. By integrating these embeddings into the RAG framework, the system can combine the generative power of large language models with the ability to pull in highly relevant, contextually-aware data from external sources.

The system operates as follows:

1. Questions get turned into mathematical patterns that capture their meaning
2. These patterns help find matching information in a database
3. The LLM generates responses that blend the model's inherent knowledge with the this extra information.

To hold this vector information in an efficient manner, you need a special type of database.

## [Introduction to Graph databases](#introduction-to-graph-databases)

Graph databases, such as Neo4j, are specifically designed for managing highly connected data. Unlike traditional relational databases, graph databases prioritize both the entities and the relationships between them, making them ideal for tasks where connections are as important as the data itself.

Graph databases stand out for their unique approach to data storage and querying. They use nodes (or vertices) to represent entities and edges to represent the relationships between these entities. This structure allows for efficient handling of highly connected data and complex queries, which are difficult to manage in traditional database systems.

SQL databases and graph databases differ significantly in their data models. SQL databases use a tabular structure with rows and columns, where relationships between entities are established using foreign keys. This approach works well for structured data and predefined relationships. In contrast, graph databases represent data as nodes (entities) and edges (relationships), making the representation of relationships more intuitive and flexible. This structure is particularly advantageous for complex, interconnected data.

Another key difference lies in schema flexibility. SQL databases operate on a rigid schema, meaning any changes to the data structure, such as adding new columns or altering relationships, typically require careful planning and migration processes. Graph databases, however, are schema-optional, allowing for much greater flexibility. New nodes, edges, or properties can be introduced without disrupting existing data, enabling faster adaptation to changing requirements.

## [Practical implementation: testing RAG effectiveness](#practical-implementation-testing-rag-effectiveness)

To illustrate the power of RAG systems in practice, let's examine a real-world implementation using Apache NiFi as our subject matter. This case study demonstrates how RAG can enhance an AI's ability to provide accurate, contextual information about specialized technical topics.

### [Teaching AI about new technologies](#teaching-ai-about-new-technologies)

Apache NiFi serves as an excellent example of the limitations of traditional LLMs and how RAG can overcome them. As a relatively recent technology, many LLMs have limited or outdated knowledge about it, making it a perfect candidate for demonstrating RAG's capabilities.

Without RAG, the LLM may provide broad responses or acknowledge its limited knowledge when asked about information that is beyond its cutoff date. The following example demonstrates this.

```text
Question: What important events happened in 2024?
RAG: Disabled
I'm happy to help! Unfortunately, I'm a large language model, I don't have access to real-time information or events that occurred after my training data cutoff in 2024. Therefore, I cannot provide you with any important events that happened in 2024. My apologize for any inconvenience this may cause. Is there anything else I can help you with?
```

## [Setting up GenAI stack with GPU acceleration on Linux](#setting-up-genai-stack-with-gpu-acceleration-on-linux)

To set up and run the GenAI stack on a Linux host, execute one of the following commands, either for GPU or CPU powered:

### [GPU powered](#gpu-powered)

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux-gpu up -d
mv env.example .env
nano .env
```

In the `.env` file, make sure following lines are commented out. Set your own credentials for security

```txt
  NEO4J_URI=neo4j://database:7687
  NEO4J_USERNAME=neo4j
  NEO4J_PASSWORD=password
  OLLAMA_BASE_URL=http://llm-gpu:11434
```

### [CPU powered](#cpu-powered)

```bash
git clone https://github.com/docker/genai-stack
docker compose --profile linux up -d
mv env.example .env
nano .env
```

In the `.env` file, make sure following lines are commented out. Set your own credentials for security

```txt
  NEO4J_URI=neo4j://database:7687
  NEO4J_USERNAME=neo4j
  NEO4J_PASSWORD=password
  OLLAMA_BASE_URL=http://llm:11434
```

### [Setting up on other platforms](#setting-up-on-other-platforms)

For instructions on how to set up the stack on other platforms, refer to [this page](https://github.com/docker/genai-stack).

### [Initial startup](#initial-startup)

The first startup may take some time because the system needs to download a large language model.

### [Monitoring progress](#monitoring-progress)

You can monitor the download and initialization progress by viewing the logs. Run the following command to view the logs:

```bash
docker compose logs
```

Wait for specific lines in the logs indicating that the download is complete and the stack is ready. These lines typically confirm successful setup and initialization.

```text
  pull-model-1 exited with code 0
  database-1    | 2024-12-29 09:35:53.269+0000 INFO  Started.
  pdf_bot-1     |   You can now view your Streamlit app in your browser.
  loader-1      |   You can now view your Streamlit app in your browser.
  bot-1         |   You can now view your Streamlit app in your browser.
```

You can now access the interface at <http://localhost:8501/> to ask questions. For example, you can try the sample question:

When those lines appear in the logs, the web apps are ready to use.

Since the goal is to teach AI about things it does not yet know, begin by asking it a simple question about NiFi at <http://localhost:8501/>.

```text
Question: What is Apache Nifi?
RAG: Disabled
Hello! I'm here to help you with your question about Apache NiFi. Unfortunately, I don't know the answer to that question. I'm just an AI and my knowledge cutoff is December 2022, so I may not be familiar with the latest technologies or software. Can you please provide more context or details about Apache NiFi? Maybe there's something I can help you with related to it.
```

As shown, the AI does not know anything about this subject because it did not exist during the time of its training, also known as the information cutoff point.

Now it's time to teach the AI some new tricks. First, connect to <http://localhost:8502/>. Instead of using the "neo4j" tag, change it to the "apache-nifi" tag, then select the **Import** button.

After the import is successful, you can access Neo4j to verify the data.

After logging in to <http://localhost:7474/> using the credentials from the `.env` file, you can run queries on Neo4j. Using the Neo4j Cypher query language, you can check for the data stored in the database.

To count the data, run the following query:

```text
MATCH (n)
RETURN DISTINCT labels(n) AS NodeTypes, count(*) AS Count
ORDER BY Count DESC;
```

To execute this query, write in the box on the top and select the blue run button.

Results will appear below. The information shown is downloaded from Stack Overflow and saved in the graph database. RAG will utilize this information to enhance its responses.

You can also run the following query to visualize the data:

```text
CALL db.schema.visualization()
```

To check the relationships in the database, run the following query:

```text
CALL db.relationshipTypes()
```

You're ready to enable the LLM to use this information. Go back to <http://localhost:8501/>, enable the **RAG** checkbox, and ask the same question again. The LLM will provide a more detailed answer.

The system delivers comprehensive, accurate information by pulling from current technical documentation.

```text
Question: What is Apache Nifi?
RAG: Enabled

Answer:
Apache NiFi is an open-source, distributed data processing system that allows you to collect, transform, and transport data across various sources and sinks. It provides a graphical user interface for designing and managing data flows, as well as a set of APIs for integrating with other systems.
According to this Stack Overflow question, the free Neo4J JDBC driver doesn't understand SQL, only Cypher, so you would need to use a non-free BI Connector to connect to Neo4j from Apache Drill.
Additionally, this Stack Overflow question suggests that Apache POI does work in a Neo4j User Defined Function. However, there may be an unknown glitch in the standalone UDF mentioned in the initial question.
To export data from Neo4j to Excel using APOC Extended procedures, you can use apoc.export.xls.query which takes a Cypher query and exports the results to an Excel file.

References:
How to connect and query Neo4j Database on Apache Drill?
Is a Neo4j UDF compatible with Apache POI?
```

Keep in mind that new questions will be added to Stack Overflow, and due to the inherent randomness in most AI models, the answers may vary and won't be identical to those in this example.

Feel free to start over with another [Stack Overflow tag](https://stackoverflow.com/tags). To drop all data in Neo4j, you can use the following command in the Neo4j Web UI:

```txt
MATCH (n)
DETACH DELETE n;
```

For optimal results, choose a tag that the LLM is not familiar with.

### [When to leverage RAG for optimal results](#when-to-leverage-rag-for-optimal-results)

Retrieval-Augmented Generation (RAG) is particularly effective in scenarios where standard Large Language Models (LLMs) fall short. The three key areas where RAG excels are knowledge limitations, business requirements, and cost efficiency. The following sections explore these aspects in more detail.

#### [Overcoming knowledge limitations](#overcoming-knowledge-limitations)

LLMs are trained on a fixed dataset up until a certain point in time. This means they lack access to:

* Real-time information: LLMs do not continuously update their knowledge, so they may not be aware of recent events, newly released research, or emerging technologies.
* Specialized knowledge: Many niche subjects, proprietary frameworks, or industry-specific best practices may not be well-documented in the model’s training corpus.
* Accurate contextual understanding: LLMs can struggle with nuances or evolving terminologies that frequently change within dynamic fields like finance, cybersecurity, or medical research.

By incorporating RAG with a graph database such as Neo4j, AI models can access and retrieve the latest, relevant, and highly connected data before generating a response. This ensures that answers are up-to-date and grounded in factual information rather than inferred approximations.

#### [Addressing business and compliance needs](#addressing-business-and-compliance-needs)

Organizations in industries like healthcare, legal services, and financial analysis require their AI-driven solutions to be:

* Accurate: Businesses need AI-generated content that is factual and relevant to their specific domain.
* Compliant: Many industries must adhere to strict regulations regarding data usage and security.
* Traceable: Enterprises often require AI responses to be auditable, meaning they need to reference source material.

By using RAG, AI-generated answers can be sourced from trusted databases, ensuring higher accuracy and compliance with industry standards. This mitigates risks such as misinformation or regulatory violations.

#### [Enhancing cost efficiency and performance](#enhancing-cost-efficiency-and-performance)

Training and fine-tuning large AI models can be computationally expensive and time-consuming. However, integrating RAG provides:

* Reduced fine-tuning needs: Instead of retraining an AI model every time new data emerges, RAG allows the model to fetch and incorporate updated information dynamically.
* Better performance with smaller models: With the right retrieval techniques, even compact AI models can perform well by leveraging external knowledge efficiently.
* Lower operational costs: Instead of investing in expensive infrastructure to support large-scale retraining, businesses can optimize resources by utilizing RAG’s real-time retrieval capabilities.

By following this guide, you now have the foundational knowledge to implement RAG with Neo4j, enabling your AI system to deliver more accurate, relevant, and insightful responses. The next step is experimentation—choose a dataset, configure your stack, and start enhancing your AI with the power of retrieval-augmented generation.

----
url: https://docs.docker.com/reference/cli/docker/container/exec/
----

# docker container exec

***

| Description                                                               | Execute a command in a running container                     |
| ------------------------------------------------------------------------- | ------------------------------------------------------------ |
| Usage                                                                     | `docker container exec [OPTIONS] CONTAINER COMMAND [ARG...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker exec`                                                |

## [Description](#description)

The `docker exec` command runs a new command in a running container.

The command you specify with `docker exec` only runs while the container's primary process (`PID 1`) is running, and it isn't restarted if the container is restarted.

The command runs in the default working directory of the container.

The command must be an executable. A chained or a quoted command doesn't work.

* This works: `docker exec -it my_container sh -c "echo a && echo b"`
* This doesn't work: `docker exec -it my_container "echo a && echo b"`

## [Options](#options)

| Option                        | Default | Description                                            |
| ----------------------------- | ------- | ------------------------------------------------------ |
| `-d, --detach`                |         | Detached mode: run command in the background           |
| `--detach-keys`               |         | Override the key sequence for detaching a container    |
| [`-e, --env`](#env)           |         | API 1.25+ Set environment variables                    |
| `--env-file`                  |         | API 1.25+ Read in a file of environment variables      |
| `-i, --interactive`           |         | Keep STDIN open even if not attached                   |
| [`--privileged`](#privileged) |         | Give extended privileges to the command                |
| `-t, --tty`                   |         | Allocate a pseudo-TTY                                  |
| `-u, --user`                  |         | Username or UID (format: `<name\|uid>[:<group\|gid>]`) |
| [`-w, --workdir`](#workdir)   |         | API 1.35+ Working directory inside the container       |

## [Examples](#examples)

### [Run `docker exec` on a running container](#run-docker-exec-on-a-running-container)

First, start a container.

```console
$ docker run --name mycontainer -d -i -t alpine /bin/sh
```

This creates and starts a container named `mycontainer` from an `alpine` image with an `sh` shell as its main process. The `-d` option (shorthand for `--detach`) sets the container to run in the background, in detached mode, with a pseudo-TTY attached (`-t`). The `-i` option is set to keep `STDIN` attached (`-i`), which prevents the `sh` process from exiting immediately.

Next, execute a command on the container.

```console
$ docker exec -d mycontainer touch /tmp/execWorks
```

This creates a new file `/tmp/execWorks` inside the running container `mycontainer`, in the background.

Next, execute an interactive `sh` shell on the container.

```console
$ docker exec -it mycontainer sh
```

This starts a new shell session in the container `mycontainer`.

### [Set environment variables for the exec process (--env, -e)](#env)

Next, set environment variables in the current bash session.

The `docker exec` command inherits the environment variables that are set at the time the container is created. Use the `--env` (or the `-e` shorthand) to override global environment variables, or to set additional environment variables for the process started by `docker exec`.

The following example creates a new shell session in the container `mycontainer`, with environment variables `$VAR_A` set to `1`, and `$VAR_B` set to `2`. These environment variables are only valid for the `sh` process started by that `docker exec` command, and aren't available to other processes running inside the container.

```console
$ docker exec -e VAR_A=1 -e VAR_B=2 mycontainer env
PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=f64a4851eb71
VAR_A=1
VAR_B=2
HOME=/root
```

### [Escalate container privileges (--privileged)](#privileged)

See [`docker run --privileged`](/reference/cli/docker/container/run/#privileged).

### [Set the working directory for the exec process (--workdir, -w)](#workdir)

By default `docker exec` command runs in the same working directory set when the container was created.

```console
$ docker exec -it mycontainer pwd
/
```

You can specify an alternative working directory for the command to execute using the `--workdir` option (or the `-w` shorthand):

```console
$ docker exec -it -w /root mycontainer pwd
/root
```

### [Try to run `docker exec` on a paused container](#try-to-run-docker-exec-on-a-paused-container)

If the container is paused, then the `docker exec` command fails with an error:

```console
$ docker pause mycontainer
mycontainer

$ docker ps

CONTAINER ID   IMAGE     COMMAND     CREATED          STATUS                   PORTS     NAMES
482efdf39fac   alpine    "/bin/sh"   17 seconds ago   Up 16 seconds (Paused)             mycontainer

$ docker exec mycontainer sh

Error response from daemon: Container mycontainer is paused, unpause the container before exec

$ echo $?
1
```

----
url: https://docs.docker.com/reference/cli/docker/dhi/auth/
----

# docker dhi auth

***

| Description | Authenticate with Docker Hub |
| ----------- | ---------------------------- |

## [Description](#description)

Commands to authenticate with Docker Hub

## [Subcommands](#subcommands)

| Command                                                                             | Description                                            |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [`docker dhi auth apk`](https://docs.docker.com/reference/cli/docker/dhi/auth/apk/) | Create authentication details for DHI APK repositories |
| [`docker dhi auth deb`](https://docs.docker.com/reference/cli/docker/dhi/auth/deb/) | Create authentication details for DHI DEB repositories |

----
url: https://docs.docker.com/engine/install/ubuntu/
----

# Install Docker Engine on Ubuntu

***

Table of contents

***

To get started with Docker Engine on Ubuntu, make sure you [meet the prerequisites](#prerequisites), and then follow the [installation steps](#installation-methods).

## [Prerequisites](#prerequisites)

### [Firewall limitations](#firewall-limitations)

> Warning
>
> Before you install Docker, make sure you consider the following security implications and firewall incompatibilities.

* If you use ufw or firewalld to manage firewall settings, be aware that when you expose container ports using Docker, these ports bypass your firewall rules. For more information, refer to [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw).
* Docker is only compatible with `iptables-nft` and `iptables-legacy`. Firewall rules created with `nft` are not supported on a system with Docker installed. Make sure that any firewall rulesets you use are created with `iptables` or `ip6tables`, and that you add them to the `DOCKER-USER` chain, see [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

### [OS requirements](#os-requirements)

To install Docker Engine, you need the 64-bit version of one of these Ubuntu versions:

* Ubuntu Resolute 26.04 (LTS)
* Ubuntu Questing 25.10
* Ubuntu Noble 24.04 (LTS)
* Ubuntu Jammy 22.04 (LTS)

Docker Engine for Ubuntu is compatible with x86\_64 (or amd64), armhf, arm64, s390x, and ppc64le (ppc64el) architectures.

> Note
>
> Installation on Ubuntu derivative distributions, such as Linux Mint, is not officially supported (though it may work).

### [Uninstall old versions](#uninstall-old-versions)

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict with the official packages provided by Docker. You must uninstall these packages before you install the official version of Docker Engine.

The unofficial packages to uninstall are:

* `docker.io`
* `docker-compose`
* `docker-compose-v2`
* `docker-doc`
* `podman-docker`

Moreover, Docker Engine depends on `containerd` and `runc`. Docker Engine bundles these dependencies as one bundle: `containerd.io`. If you have installed the `containerd` or `runc` previously, uninstall them to avoid conflicts with the versions bundled with Docker Engine.

Run the following command to uninstall all conflicting packages:

```console
$ sudo apt remove $(dpkg --get-selections docker.io docker-compose docker-compose-v2 docker-doc podman-docker containerd runc | cut -f1)
```

   ```bash
   # Add Docker's official GPG key:
   sudo apt update
   sudo apt install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
   Types: deb
   URIs: https://download.docker.com/linux/ubuntu
   Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
   Components: stable
   Architectures: $(dpkg --print-architecture)
   Signed-By: /etc/apt/keyrings/docker.asc
   EOF

   sudo apt update
   ```

2. Install the Docker packages.

   To install the latest version, run:

   ```console
   $ sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   To install a specific version of Docker Engine, start by listing the available versions in the repository:

   ```console
   $ apt list --all-versions docker-ce

   docker-ce/noble 5:29.5.3-1~ubuntu.24.04~noble <arch>
   docker-ce/noble 5:29.5.2-1~ubuntu.24.04~noble <arch>
   ...
   ```

   Select the desired version and install:

   ```console
   $ VERSION_STRING=5:29.5.3-1~ubuntu.24.04~noble
   $ sudo apt install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   > Note
   >
   > After installation, verify that Docker is running:
   >
   > ```console
   > $ sudo systemctl status docker
   > ```
   >
   > If Docker is not running, start it manually:
   >
   > ```console
   > $ sudo systemctl start docker
   > ```

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

To upgrade Docker Engine, follow step 2 of the [installation instructions](#install-using-the-repository), choosing the new version you want to install.

### [Install from a package](#install-from-a-package)

If you can't use Docker's `apt` repository to install Docker Engine, you can download the `deb` file for your release and install it manually. You need to download a new file each time you want to upgrade Docker Engine.

1. Go to [`https://download.docker.com/linux/ubuntu/dists/`](https://download.docker.com/linux/ubuntu/dists/).

2. Select your Ubuntu version in the list.

   ```console
   $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
     ./docker-ce_<version>_<arch>.deb \
     ./docker-ce-cli_<version>_<arch>.deb \
     ./docker-buildx-plugin_<version>_<arch>.deb \
     ./docker-compose-plugin_<version>_<arch>.deb
   ```

   > Note
   >
   > After installation, verify that Docker is running:
   >
   > ```console
   > $ sudo systemctl status docker
   > ```
   >
   > If Docker is not running, start it manually:
   >
   > ```console
   > $ sudo systemctl start docker
   > ```

6. Verify that the installation is successful by running the `hello-world` image:

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
   $ sudo apt purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

3. Remove source list and keyrings

   ```console
   $ sudo rm /etc/apt/sources.list.d/docker.sources
   $ sudo rm /etc/apt/keyrings/docker.asc
   ```

----
url: https://docs.docker.com/ai/sandboxes/agents/droid/
----

# Droid

***

Table of contents

***

This guide covers authentication, configuration, and usage of Droid, an AI coding agent by Factory, in a sandboxed environment.

Official documentation: [Droid](https://docs.factory.ai/)

## [Quick start](#quick-start)

Create a sandbox and run Droid for a project directory:

```console
$ sbx run droid ~/my-project
```

The workspace parameter is optional and defaults to the current directory:

```console
$ cd ~/my-project
$ sbx run droid
```

## [Authentication](#authentication)

Droid requires a [Factory account](https://factory.ai). Both authentication methods authenticate you to Factory's service directly — unlike other agents where you supply a model provider key, Factory manages model access through your Factory account.

**API key**: Store your Factory API key using [stored secrets](https://docs.docker.com/ai/sandboxes/security/credentials/#stored-secrets):

```console
$ sbx secret set -g droid
```

Alternatively, export the `FACTORY_API_KEY` environment variable in your shell before running the sandbox. See [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/) for details on both methods.

**OAuth**: If no API key is set, Droid prompts you to authenticate interactively on first run. The proxy handles the OAuth flow, so credentials aren't stored inside the sandbox.

## [Configuration](#configuration)

Sandboxes don't pick up user-level configuration from your host. Only project-level configuration in the working directory is available inside the sandbox. See [Why doesn't the sandbox use my user-level agent configuration?](https://docs.docker.com/ai/sandboxes/faq/#why-doesnt-the-sandbox-use-my-user-level-agent-configuration) for workarounds.

### [Default startup command](#default-startup-command)

The sandbox runs `droid` with no implicit flags. Args after `--` are passed straight through:

```console
$ sbx run droid -- exec "fix the build"
```

## [Base image](#base-image)

Template: `docker/sandbox-templates:droid-docker`

Preconfigured to run without approval prompts. Authentication state is persisted across sandbox restarts.

See [Customize](https://docs.docker.com/ai/sandboxes/customize/) to pre-install tools or customize this environment.

----
url: https://docs.docker.com/ai/docker-agent/integrations/a2a/
----

# A2A mode

***

Table of contents

***

A2A mode runs your agent as an HTTP server that other systems can call using the Agent-to-Agent protocol. This lets you expose your agent as a service that other agents or applications can discover and invoke over the network.

Use A2A when you want to make your agent callable by other systems over HTTP. For editor integration, see [ACP integration](https://docs.docker.com/ai/docker-agent/integrations/acp/). For using agents as tools in MCP clients, see [MCP integration](https://docs.docker.com/ai/docker-agent/integrations/mcp/).

## [Prerequisites](#prerequisites)

Before starting an A2A server, you need:

* Docker Agent installed - See the [installation guide](https://docs.docker.com/ai/docker-agent/#installation)
* Agent configuration - A YAML file defining your agent. See the [tutorial](https://docs.docker.com/ai/docker-agent/tutorial/)
* API keys configured - If using cloud model providers (see [Model providers](https://docs.docker.com/ai/docker-agent/model-providers/))

## [Starting an A2A server](#starting-an-a2a-server)

Basic usage:

```console
$ docker agent serve a2a ./agent.yaml
```

Your agent is now accessible via HTTP. Other A2A systems can discover your agent's capabilities and call it.

Custom port:

```console
$ docker agent serve a2a ./agent.yaml --port 8080
```

Specific agent in a team:

```console
$ docker agent serve a2a ./agent.yaml --agent engineer
```

From OCI registry:

```console
$ docker agent serve a2a agentcatalog/pirate --port 9000
```

## [HTTP endpoints](#http-endpoints)

When you start an A2A server, it exposes two HTTP endpoints:

### [Agent card: `/.well-known/agent-card`](#agent-card-well-knownagent-card)

The agent card describes your agent's capabilities:

```console
$ curl http://localhost:8080/.well-known/agent-card
```

```json
{
  "name": "agent",
  "description": "A helpful coding assistant",
  "skills": [
    {
      "id": "agent_root",
      "name": "root",
      "description": "A helpful coding assistant",
      "tags": ["llm", "dockeragent"]
    }
  ],
  "preferredTransport": "jsonrpc",
  "url": "http://localhost:8080/invoke",
  "capabilities": {
    "streaming": true
  },
  "version": "0.1.0"
}
```

### [Invoke endpoint: `/invoke`](#invoke-endpoint-invoke)

Call your agent by sending a JSON-RPC request:

```console
$ curl -X POST http://localhost:8080/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "req-1",
    "method": "message/send",
    "params": {
      "message": {
        "role": "user",
        "parts": [
          {
            "kind": "text",
            "text": "What is 2+2?"
          }
        ]
      }
    }
  }'
```

The response includes the agent's reply:

```json
{
  "jsonrpc": "2.0",
  "id": "req-1",
  "result": {
    "artifacts": [
      {
        "parts": [
          {
            "kind": "text",
            "text": "2+2 equals 4."
          }
        ]
      }
    ]
  }
}
```

## [Example: Multi-agent workflow](#example-multi-agent-workflow)

Here's a concrete scenario where A2A is useful. You have two agents:

1. A general-purpose agent that interacts with users
2. A specialized code review agent with access to your codebase

Run the specialist as an A2A server:

```console
$ docker agent serve a2a ./code-reviewer.yaml --port 8080
Listening on 127.0.0.1:8080
```

Configure your main agent to call it:

```yaml
agents:
  root:
    model: anthropic/claude-sonnet-4-5
    instruction: You are a helpful assistant
    toolsets:
      - type: a2a
