    url: 'http://collector:4318/v1/traces',
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

## [Configure the OpenTelemetry Collector](#configure-the-opentelemetry-collector)

Create a collector-config.yaml file at the root:

```yaml
# collector-config.yaml
receivers:
  otlp:
    protocols:
      http:

exporters:
  logging:
    loglevel: debug
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      exporters: [logging, jaeger]
```

## [Add Docker Compose configuration](#add-docker-compose-configuration)

Create the `docker-compose.yaml` file:

```yaml
services:
  app:
    build: ./app
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    depends_on:
      - collector

  collector:
    image: otel/opentelemetry-collector:latest
    volumes:
      - ./collector-config.yaml:/etc/otelcol/config.yaml
    command: ["--config=/etc/otelcol/config.yaml"]
    ports:
      - "4318:4318" # OTLP

  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # UI
      - "14250:14250" # Collector gRPC
```

Now, add the `Dockerfile` inside the `app/` folder:

```dockerfile
# app/Dockerfile
FROM node:18

WORKDIR /usr/src/app
COPY . .
RUN npm install

CMD ["node", "app.js"]
```

## [Start the stack](#start-the-stack)

Start all services with Docker Compose:

```bash
docker compose up --build
```

Once the services are running:

Visit your app at <http://localhost:3000>

View traces at <http://localhost:16686> in the Jaeger UI

## [Verify traces in Jaeger](#verify-traces-in-jaeger)

After visiting your app's root endpoint, open Jaeger’s UI, search for the service (default is usually `unknown_service` unless explicitly named), and check the traces.

You should see spans for the HTTP request, middleware, and auto-instrumented libraries.

## [Conclusion](#conclusion)

You now have a fully functional OpenTelemetry setup using Docker Compose. You've instrumented a basic JavaScript app to export traces and visualized them using Jaeger. This architecture is extendable for more complex applications and observability pipelines using Prometheus, Grafana, or cloud-native exporters.

For advanced topics such as custom span creation, metrics, and logs, consult the OpenTelemetry JavaScript docs.

----
url: https://docs.docker.com/reference/cli/docker/scout/
----

# docker scout

***

| Description | Command line tool for Docker Scout |
| ----------- | ---------------------------------- |
| Usage       | `docker scout [command]`           |

## [Description](#description)

Command line tool for Docker Scout

## [Subcommands](#subcommands)

| Command                                                                                               | Description                                                                                 |
| ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| [`docker scout attestation`](https://docs.docker.com/reference/cli/docker/scout/attestation/)         | Manage attestations on images                                                               |
| [`docker scout cache`](https://docs.docker.com/reference/cli/docker/scout/cache/)                     | Manage Docker Scout cache and temporary files                                               |
| [`docker scout compare`](https://docs.docker.com/reference/cli/docker/scout/compare/)                 | Compare two images and display differences (experimental)                                   |
| [`docker scout config`](https://docs.docker.com/reference/cli/docker/scout/config/)                   | Manage Docker Scout configuration                                                           |
| [`docker scout cves`](https://docs.docker.com/reference/cli/docker/scout/cves/)                       | Display CVEs identified in a software artifact                                              |
| [`docker scout enroll`](https://docs.docker.com/reference/cli/docker/scout/enroll/)                   | Enroll an organization with Docker Scout                                                    |
| [`docker scout environment`](https://docs.docker.com/reference/cli/docker/scout/environment/)         | Manage environments (experimental)                                                          |
| [`docker scout help`](https://docs.docker.com/reference/cli/docker/scout/help/)                       | Display information about the available commands                                            |
| [`docker scout integration`](https://docs.docker.com/reference/cli/docker/scout/integration/)         | Commands to list, configure, and delete Docker Scout integrations                           |
| [`docker scout policy`](https://docs.docker.com/reference/cli/docker/scout/policy/)                   | Evaluate policies against an image and display the policy evaluation results (experimental) |
| [`docker scout push`](https://docs.docker.com/reference/cli/docker/scout/push/)                       | Push an image or image index to Docker Scout                                                |
| [`docker scout quickview`](https://docs.docker.com/reference/cli/docker/scout/quickview/)             | Quick overview of an image                                                                  |
| [`docker scout recommendations`](https://docs.docker.com/reference/cli/docker/scout/recommendations/) | Display available base image updates and remediation recommendations                        |
| [`docker scout repo`](https://docs.docker.com/reference/cli/docker/scout/repo/)                       | Commands to list, enable, and disable Docker Scout on repositories                          |
| [`docker scout sbom`](https://docs.docker.com/reference/cli/docker/scout/sbom/)                       | Generate or display SBOM of an image                                                        |
| [`docker scout stream`](https://docs.docker.com/reference/cli/docker/scout/stream/)                   | Manage streams (experimental)                                                               |
| [`docker scout version`](https://docs.docker.com/reference/cli/docker/scout/version/)                 | Show Docker Scout version information                                                       |
| [`docker scout vex`](https://docs.docker.com/reference/cli/docker/scout/vex/)                         | Manage VEX attestations on images                                                           |
| [`docker scout watch`](https://docs.docker.com/reference/cli/docker/scout/watch/)                     | Watch repositories in a registry and push images and indexes to Docker Scout                |

----
url: https://docs.docker.com/reference/cli/docker/buildx/create/
----

# docker buildx create

***

| Description | Create a new builder instance                        |
| ----------- | ---------------------------------------------------- |
| Usage       | `docker buildx create [OPTIONS] [CONTEXT\|ENDPOINT]` |

## [Description](#description)

Create makes a new builder instance pointing to a Docker context or endpoint, where context is the name of a context from `docker context ls` and endpoint is the address for Docker socket (eg. `DOCKER_HOST` value).

By default, the current Docker configuration is used for determining the context/endpoint value.

Builder instances are isolated environments where builds can be invoked. All Docker contexts also get the default builder instance.

## [Options](#options)

| Option                                    | Default | Description                                                            |
| ----------------------------------------- | ------- | ---------------------------------------------------------------------- |
| [`--append`](#append)                     |         | Append a node to builder instead of changing it                        |
| `--bootstrap`                             |         | Boot builder after creation                                            |
| [`--buildkitd-config`](#buildkitd-config) |         | BuildKit daemon config file                                            |
| [`--buildkitd-flags`](#buildkitd-flags)   |         | BuildKit daemon flags                                                  |
| [`--driver`](#driver)                     |         | Driver to use (available: `docker-container`, `kubernetes`, `remote`)  |
| [`--driver-opt`](#driver-opt)             |         | Options for the driver                                                 |
| [`--leave`](#leave)                       |         | Remove a node from builder instead of changing it                      |
| [`--name`](#name)                         |         | Builder instance name                                                  |
| [`--node`](#node)                         |         | Create/modify node with given name                                     |
| [`--platform`](#platform)                 |         | Fixed platforms for current node                                       |
| `--timeout`                               | `20s`   | Override the default timeout for loading builder status                |
| [`--use`](#use)                           |         | Set the current builder instance                                       |

## [Examples](#examples)

### [Append a new node to an existing builder (--append)](#append)

The `--append` flag changes the action of the command to append a new node to an existing builder specified by `--name`. Buildx will choose an appropriate node for a build based on the platforms it supports.

```console
$ docker buildx create mycontext1
eager_beaver

$ docker buildx create --name eager_beaver --append mycontext2
eager_beaver
```

### [Specify a configuration file for the BuildKit daemon (--buildkitd-config)](#buildkitd-config)

```text
--buildkitd-config FILE
```

Specifies the configuration file for the BuildKit daemon to use. The configuration can be overridden by [`--buildkitd-flags`](#buildkitd-flags). See an [example BuildKit daemon configuration file](https://github.com/moby/buildkit/blob/master/docs/buildkitd.toml.md).

If you don't specify a configuration file, Buildx looks for one by default in:

* `$BUILDX_CONFIG/buildkitd.default.toml`
* `$DOCKER_CONFIG/buildx/buildkitd.default.toml`
* `~/.docker/buildx/buildkitd.default.toml`

Note that if you create a `docker-container` builder and have specified certificates for registries in the `buildkitd.toml` configuration, the files will be copied into the container under `/etc/buildkit/certs` and configuration will be updated to reflect that.

### [Specify options for the BuildKit daemon (--buildkitd-flags)](#buildkitd-flags)

```text
--buildkitd-flags FLAGS
```

Adds flags when starting the BuildKit daemon. They take precedence over the configuration file specified by [`--buildkitd-config`](#buildkitd-config). See `buildkitd --help` for the available flags.

```text
--buildkitd-flags '--debug --debugaddr 0.0.0.0:6666'
```

#### [BuildKit daemon network mode](#buildkit-daemon-network-mode)

You can specify the network mode for the BuildKit daemon with either the configuration file specified by [`--buildkitd-config`](#buildkitd-config) using the `worker.oci.networkMode` option or `--oci-worker-net` flag here. The default value is `auto` and can be one of `bridge`, `cni`, `host`:

```text
--buildkitd-flags '--oci-worker-net bridge'
```

> Note
>
> Network mode "bridge" is supported since BuildKit v0.13 and will become the default in next v0.14.

### [Set the builder driver to use (--driver)](#driver)

```text
--driver DRIVER
```

Sets the builder driver to be used. A driver is a configuration of a BuildKit backend. Buildx supports the following drivers:

* `docker` (default)
* `docker-container`
* `kubernetes`
* `remote`

For more information about build drivers, see [here](/build/builders/drivers/).

#### [`docker` driver](#docker-driver)

Uses the builder that is built into the Docker daemon. With this driver, the [`--load`](/reference/cli/docker/buildx/build/#load) flag is implied by default on `buildx build`. However, building multi-platform images or exporting cache is not currently supported.

#### [`docker-container` driver](#docker-container-driver)

Uses a BuildKit container that will be spawned via Docker. With this driver, both building multi-platform images and exporting cache are supported.

Unlike `docker` driver, built images will not automatically appear in `docker images` and [`build --load`](/reference/cli/docker/buildx/build/#load) needs to be used to achieve that.

#### [`kubernetes` driver](#kubernetes-driver)

Uses Kubernetes pods. With this driver, you can spin up pods with defined BuildKit container image to build your images.

Unlike `docker` driver, built images will not automatically appear in `docker images` and [`build --load`](/reference/cli/docker/buildx/build/#load) needs to be used to achieve that.

#### [`remote` driver](#remote-driver)

Uses a remote instance of BuildKit daemon over an arbitrary connection. With this driver, you manually create and manage instances of buildkit yourself, and configure buildx to point at it.

Unlike `docker` driver, built images will not automatically appear in `docker images` and [`build --load`](/reference/cli/docker/buildx/build/#load) needs to be used to achieve that.

### [Set additional driver-specific options (--driver-opt)](#driver-opt)

```text
--driver-opt OPTIONS
```

Passes additional driver-specific options. For information about available driver options, refer to the detailed documentation for the specific driver:

* [`docker` driver](/build/builders/drivers/docker/)
* [`docker-container` driver](/build/builders/drivers/docker-container/)
* [`kubernetes` driver](/build/builders/drivers/kubernetes/)
* [`remote` driver](/build/builders/drivers/remote/)

### [Remove a node from a builder (--leave)](#leave)

The `--leave` flag changes the action of the command to remove a node from a builder. The builder needs to be specified with `--name` and node that is removed is set with `--node`.

```console
$ docker buildx create --name mybuilder --node mybuilder0 --leave
```

### [Specify the name of the builder (--name)](#name)

```text
--name NAME
```

The `--name` flag specifies the name of the builder to be created or modified. If none is specified, one will be automatically generated.

### [Specify the name of the node (--node)](#node)

```text
--node NODE
```

The `--node` flag specifies the name of the node to be created or modified. If you don't specify a name, the node name defaults to the name of the builder it belongs to, with an index number suffix.

### [Set the platforms supported by the node (--platform)](#platform)

```text
--platform PLATFORMS
```

The `--platform` flag sets the platforms supported by the node. It expects a comma-separated list of platforms of the form OS/architecture/variant. The node will also automatically detect the platforms it supports, but manual values take priority over the detected ones and can be used when multiple nodes support building for the same platform.

```console
$ docker buildx create --platform linux/amd64
$ docker buildx create --platform linux/arm64,linux/arm/v7
```

### [Automatically switch to the newly created builder (--use)](#use)

The `--use` flag automatically switches the current builder to the newly created one. Equivalent to running `docker buildx use $(docker buildx create ...)`.

----
url: https://docs.docker.com/reference/cli/docker/container/run/
----

# docker container run

***

| Description                                                               | Create and run a new container from an image              |
| ------------------------------------------------------------------------- | --------------------------------------------------------- |
| Usage                                                                     | `docker container run [OPTIONS] IMAGE [COMMAND] [ARG...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker run`                                              |

## [Description](#description)

The `docker run` command runs a command in a new container, pulling the image if needed and starting the container.

You can restart a stopped container with all its previous changes intact using `docker start`. Use `docker ps -a` to view a list of all containers, including those that are stopped.

## [Options](#options)

| Option                                        | Default   | Description                                                                                                                                                                                                                                                                               |
| --------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`--add-host`](#add-host)                     |           | Add a custom host-to-IP mapping (host:ip)                                                                                                                                                                                                                                                 |
| `--annotation`                                |           | API 1.43+ Add an annotation to the container (passed through to the OCI runtime)                                                                                                                                                                                                          |
| [`-a, --attach`](#attach)                     |           | Attach to STDIN, STDOUT or STDERR                                                                                                                                                                                                                                                         |
| `--blkio-weight`                              |           | Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)                                                                                                                                                                                                              |
| `--blkio-weight-device`                       |           | Block IO weight (relative device weight)                                                                                                                                                                                                                                                  |
| `--cap-add`                                   |           | Add Linux capabilities                                                                                                                                                                                                                                                                    |
| `--cap-drop`                                  |           | Drop Linux capabilities                                                                                                                                                                                                                                                                   |
| [`--cgroup-parent`](#cgroup-parent)           |           | Optional parent cgroup for the container                                                                                                                                                                                                                                                  |
| `--cgroupns`                                  |           | API 1.41+ Cgroup namespace to use (host\|private) 'host': Run the container in the Docker host's cgroup namespace 'private': Run the container in its own private cgroup namespace '': Use the cgroup namespace as configured by the default-cgroupns-mode option on the daemon (default) |
| [`--cidfile`](#cidfile)                       |           | Write the container ID to the file                                                                                                                                                                                                                                                        |
| `--cpu-count`                                 |           | CPU count (Windows only)                                                                                                                                                                                                                                                                  |
| `--cpu-percent`                               |           | CPU percent (Windows only)                                                                                                                                                                                                                                                                |
| `--cpu-period`                                |           | Limit CPU CFS (Completely Fair Scheduler) period                                                                                                                                                                                                                                          |
| `--cpu-quota`                                 |           | Limit CPU CFS (Completely Fair Scheduler) quota                                                                                                                                                                                                                                           |
| `--cpu-rt-period`                             |           | API 1.25+ Limit CPU real-time period in microseconds                                                                                                                                                                                                                                      |
| `--cpu-rt-runtime`                            |           | API 1.25+ Limit CPU real-time runtime in microseconds                                                                                                                                                                                                                                     |
| `-c, --cpu-shares`                            |           | CPU shares (relative weight)                                                                                                                                                                                                                                                              |
| `--cpus`                                      |           | API 1.25+ Number of CPUs                                                                                                                                                                                                                                                                  |
| `--cpuset-cpus`                               |           | CPUs in which to allow execution (0-3, 0,1)                                                                                                                                                                                                                                               |
| `--cpuset-mems`                               |           | MEMs in which to allow execution (0-3, 0,1)                                                                                                                                                                                                                                               |
| [`-d, --detach`](#detach)                     |           | Run container in background and print container ID                                                                                                                                                                                                                                        |
| [`--detach-keys`](#detach-keys)               |           | Override the key sequence for detaching a container                                                                                                                                                                                                                                       |
| [`--device`](#device)                         |           | Add a host device to the container                                                                                                                                                                                                                                                        |
| [`--device-cgroup-rule`](#device-cgroup-rule) |           | Add a rule to the cgroup allowed devices list                                                                                                                                                                                                                                             |
| `--device-read-bps`                           |           | Limit read rate (bytes per second) from a device                                                                                                                                                                                                                                          |
| `--device-read-iops`                          |           | Limit read rate (IO per second) from a device                                                                                                                                                                                                                                             |
| `--device-write-bps`                          |           | Limit write rate (bytes per second) to a device                                                                                                                                                                                                                                           |
| `--device-write-iops`                         |           | Limit write rate (IO per second) to a device                                                                                                                                                                                                                                              |
| `--dns`                                       |           | Set custom DNS servers                                                                                                                                                                                                                                                                    |
| `--dns-option`                                |           | Set DNS options                                                                                                                                                                                                                                                                           |
| `--dns-search`                                |           | Set custom DNS search domains                                                                                                                                                                                                                                                             |
| `--domainname`                                |           | Container NIS domain name                                                                                                                                                                                                                                                                 |
| `--entrypoint`                                |           | Overwrite the default ENTRYPOINT of the image                                                                                                                                                                                                                                             |
| [`-e, --env`](#env)                           |           | Set environment variables                                                                                                                                                                                                                                                                 |
| `--env-file`                                  |           | Read in a file of environment variables                                                                                                                                                                                                                                                   |
| `--expose`                                    |           | Expose a port or a range of ports                                                                                                                                                                                                                                                         |
| [`--gpus`](#gpus)                             |           | API 1.40+ GPU devices to add to the container ('all' to pass all GPUs)                                                                                                                                                                                                                    |
| `--group-add`                                 |           | Add additional groups to join                                                                                                                                                                                                                                                             |
| `--health-cmd`                                |           | Command to run to check health                                                                                                                                                                                                                                                            |
| `--health-interval`                           |           | Time between running the check (ms\|s\|m\|h) (default 0s)                                                                                                                                                                                                                                 |
| `--health-retries`                            |           | Consecutive failures needed to report unhealthy                                                                                                                                                                                                                                           |
| `--health-start-interval`                     |           | API 1.44+ Time between running the check during the start period (ms\|s\|m\|h) (default 0s)                                                                                                                                                                                               |
| `--health-start-period`                       |           | API 1.29+ Start period for the container to initialize before starting health-retries countdown (ms\|s\|m\|h) (default 0s)                                                                                                                                                                |
| `--health-timeout`                            |           | Maximum time to allow one check to run (ms\|s\|m\|h) (default 0s)                                                                                                                                                                                                                         |
| `--help`                                      |           | Print usage                                                                                                                                                                                                                                                                               |
| `-h, --hostname`                              |           | Container host name                                                                                                                                                                                                                                                                       |
| [`--init`](#init)                             |           | API 1.25+ Run an init inside the container that forwards signals and reaps processes                                                                                                                                                                                                      |
| [`-i, --interactive`](#interactive)           |           | Keep STDIN open even if not attached                                                                                                                                                                                                                                                      |
| `--io-maxbandwidth`                           |           | Maximum IO bandwidth limit for the system drive (Windows only)                                                                                                                                                                                                                            |
| `--io-maxiops`                                |           | Maximum IOps limit for the system drive (Windows only)                                                                                                                                                                                                                                    |
| `--ip`                                        | ``        | IPv4 address (e.g., 172.30.100.104)                                                                                                                                                                                                                                                       |
| `--ip6`                                       | ``        | IPv6 address (e.g., 2001:db8::33)                                                                                                                                                                                                                                                         |
| [`--ipc`](#ipc)                               |           | IPC mode to use                                                                                                                                                                                                                                                                           |
| [`--isolation`](#isolation)                   |           | Container isolation technology                                                                                                                                                                                                                                                            |
| [`-l, --label`](#label)                       |           | Set meta data on a container                                                                                                                                                                                                                                                              |
| `--label-file`                                |           | Read in a line delimited file of labels                                                                                                                                                                                                                                                   |
| `--link`                                      |           | Add link to another container                                                                                                                                                                                                                                                             |
| `--link-local-ip`                             |           | Container IPv4/IPv6 link-local addresses                                                                                                                                                                                                                                                  |
| [`--log-driver`](#log-driver)                 |           | Logging driver for the container                                                                                                                                                                                                                                                          |
| `--log-opt`                                   |           | Log driver options                                                                                                                                                                                                                                                                        |
| `--mac-address`                               |           | Container MAC address (e.g., 92:d0:c6:0a:29:33)                                                                                                                                                                                                                                           |
| [`-m, --memory`](#memory)                     |           | Memory limit                                                                                                                                                                                                                                                                              |
| `--memory-reservation`                        |           | Memory soft limit                                                                                                                                                                                                                                                                         |
| `--memory-swap`                               |           | Swap limit equal to memory plus swap: '-1' to enable unlimited swap                                                                                                                                                                                                                       |
| `--memory-swappiness`                         | `-1`      | Tune container memory swappiness (0 to 100)                                                                                                                                                                                                                                               |
| [`--mount`](#mount)                           |           | Attach a filesystem mount to the container                                                                                                                                                                                                                                                |
| [`--name`](#name)                             |           | Assign a name to the container                                                                                                                                                                                                                                                            |
| [`--network`](#network)                       |           | Connect a container to a network                                                                                                                                                                                                                                                          |
| `--network-alias`                             |           | Add network-scoped alias for the container                                                                                                                                                                                                                                                |
| `--no-healthcheck`                            |           | Disable any container-specified HEALTHCHECK                                                                                                                                                                                                                                               |
| `--oom-kill-disable`                          |           | Disable OOM Killer                                                                                                                                                                                                                                                                        |
| `--oom-score-adj`                             |           | Tune host's OOM preferences (-1000 to 1000)                                                                                                                                                                                                                                               |
| [`--pid`](#pid)                               |           | PID namespace to use                                                                                                                                                                                                                                                                      |
| `--pids-limit`                                |           | Tune container pids limit (set -1 for unlimited)                                                                                                                                                                                                                                          |
| `--platform`                                  |           | API 1.32+ Set platform if server is multi-platform capable                                                                                                                                                                                                                                |
| [`--privileged`](#privileged)                 |           | Give extended privileges to this container                                                                                                                                                                                                                                                |
| [`-p, --publish`](#publish)                   |           | Publish a container's port(s) to the host                                                                                                                                                                                                                                                 |
| [`-P, --publish-all`](#publish-all)           |           | Publish all exposed ports to random ports                                                                                                                                                                                                                                                 |
| [`--pull`](#pull)                             | `missing` | Pull image before running (`always`, `missing`, `never`)                                                                                                                                                                                                                                  |
| `-q, --quiet`                                 |           | Suppress the pull output                                                                                                                                                                                                                                                                  |
| [`--read-only`](#read-only)                   |           | Mount the container's root filesystem as read only                                                                                                                                                                                                                                        |
| [`--restart`](#restart)                       | `no`      | Restart policy to apply when a container exits                                                                                                                                                                                                                                            |
| [`--rm`](#rm)                                 |           | Automatically remove the container and its associated anonymous volumes when it exits                                                                                                                                                                                                     |
| `--runtime`                                   |           | Runtime to use for this container                                                                                                                                                                                                                                                         |
| [`--security-opt`](#security-opt)             |           | Security Options                                                                                                                                                                                                                                                                          |
| `--shm-size`                                  |           | Size of /dev/shm                                                                                                                                                                                                                                                                          |
| `--sig-proxy`                                 | `true`    | Proxy received signals to the process                                                                                                                                                                                                                                                     |
| [`--stop-signal`](#stop-signal)               |           | Signal to stop the container                                                                                                                                                                                                                                                              |
| [`--stop-timeout`](#stop-timeout)             |           | API 1.25+ Timeout (in seconds) to stop a container                                                                                                                                                                                                                                        |
| [`--storage-opt`](#storage-opt)               |           | Storage driver options for the container                                                                                                                                                                                                                                                  |
| [`--sysctl`](#sysctl)                         |           | Sysctl options                                                                                                                                                                                                                                                                            |
| [`--tmpfs`](#tmpfs)                           |           | Mount a tmpfs directory                                                                                                                                                                                                                                                                   |
| [`-t, --tty`](#tty)                           |           | Allocate a pseudo-TTY                                                                                                                                                                                                                                                                     |
| [`--ulimit`](#ulimit)                         |           | Ulimit options                                                                                                                                                                                                                                                                            |
| `--use-api-socket`                            |           | Bind mount Docker API socket and required auth                                                                                                                                                                                                                                            |
| `-u, --user`                                  |           | Username or UID (format: \<name\|uid>\[:\<group\|gid>])                                                                                                                                                                                                                                   |
| [`--userns`](#userns)                         |           | User namespace to use                                                                                                                                                                                                                                                                     |
| [`--uts`](#uts)                               |           | UTS namespace to use                                                                                                                                                                                                                                                                      |
| [`-v, --volume`](#volume)                     |           | Bind mount a volume                                                                                                                                                                                                                                                                       |
| `--volume-driver`                             |           | Optional volume driver for the container                                                                                                                                                                                                                                                  |
| [`--volumes-from`](#volumes-from)             |           | Mount volumes from the specified container(s)                                                                                                                                                                                                                                             |
| [`-w, --workdir`](#workdir)                   |           | Working directory inside the container                                                                                                                                                                                                                                                    |

## [Examples](#examples)

### [Assign name (--name)](#name)

The `--name` flag lets you specify a custom identifier for a container. The following example runs a container named `test` using the `nginx:alpine` image in [detached mode](#detach).

```console
$ docker run --name test -d nginx:alpine
4bed76d3ad428b889c56c1ecc2bf2ed95cb08256db22dc5ef5863e1d03252a19
$ docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS                  PORTS     NAMES
4bed76d3ad42   nginx:alpine   "/docker-entrypoint.…"   1 second ago   Up Less than a second   80/tcp    test
```

You can reference the container by name with other commands. For example, the following commands stop and remove a container named `test`:

```console
$ docker stop test
test
$ docker rm test
test
```

If you don't specify a custom name using the `--name` flag, the daemon assigns a randomly generated name, such as `vibrant_cannon`, to the container. Using a custom-defined name provides the benefit of having an easy-to-remember ID for a container.

Moreover, if you connect the container to a user-defined bridge network, other containers on the same network can refer to the container by name via DNS.

```console
$ docker network create mynet
cb79f45948d87e389e12013fa4d969689ed2c3316985dd832a43aaec9a0fe394
$ docker run --name test --net mynet -d nginx:alpine
58df6ecfbc2ad7c42d088ed028d367f9e22a5f834d7c74c66c0ab0485626c32a
$ docker run --net mynet busybox:latest ping test
PING test (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.073 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.411 ms
64 bytes from 172.18.0.2: seq=2 ttl=64 time=0.319 ms
64 bytes from 172.18.0.2: seq=3 ttl=64 time=0.383 ms
...
```

### [Capture container ID (--cidfile)](#cidfile)

To help with automation, you can have Docker write the container ID out to a file of your choosing. This is similar to how some programs might write out their process ID to a file (you might've seen them as PID files):

```console
$ docker run --cidfile /tmp/docker_test.cid ubuntu echo "test"
```

This creates a container and prints `test` to the console. The `cidfile` flag makes Docker attempt to create a new file and write the container ID to it. If the file exists already, Docker returns an error. Docker closes this file when `docker run` exits.

### [PID settings (--pid)](#pid)

```text
--pid=""  : Set the PID (Process) Namespace mode for the container,
             'container:<name|id>': joins another container's PID namespace
             'host': use the host's PID namespace inside the container
```

By default, all containers have the PID namespace enabled.

PID namespace provides separation of processes. The PID Namespace removes the view of the system processes, and allows process ids to be reused including PID 1.

In certain cases you want your container to share the host's process namespace, allowing processes within the container to see all of the processes on the system. For example, you could build a container with debugging tools like `strace` or `gdb`, but want to use these tools when debugging processes within the container.

#### [Example: run htop inside a container](#example-run-htop-inside-a-container)

To run `htop` in a container that shares the process namespac of the host:

1. Run an alpine container with the `--pid=host` option:

   ```console
   $ docker run --rm -it --pid=host alpine
   ```

2. Install `htop` in the container:

   ```console
   / # apk add --quiet htop
   ```

3. Invoke the `htop` command.

   ```console
   / # htop
   ```

#### [Example, join another container's PID namespace](#example-join-another-containers-pid-namespace)

Joining another container's PID namespace can be useful for debugging that container.

1. Start a container running a Redis server:

   ```console
   $ docker run --rm --name my-nginx -d nginx:alpine
   ```

2. Run an Alpine container that attaches the `--pid` namespace to the `my-nginx` container:

   ```console
   $ docker run --rm -it --pid=container:my-nginx \
     --cap-add SYS_PTRACE \
     --security-opt seccomp=unconfined \
     alpine
   ```

3. Install `strace` in the Alpine container:

   ```console
   / # apk add strace
   ```

4. Attach to process 1, the process ID of the `my-nginx` container:

   ```console
   / # strace -p 1
   strace: Process 1 attached
   ```

### [Disable namespace remapping for a container (--userns)](#userns)

If you enable user namespaces on the daemon, all containers are started with user namespaces enabled by default. To disable user namespace remapping for a specific container, you can set the `--userns` flag to `host`.

```console
docker run --userns=host hello-world
```

`host` is the only valid value for the `--userns` flag.

For more information, refer to [Isolate containers with a user namespace](/engine/security/userns-remap/).

### [UTS settings (--uts)](#uts)

```text
--uts=""  : Set the UTS namespace mode for the container
            'host': use the host's UTS namespace inside the container
```

The UTS namespace is for setting the hostname and the domain that's visible to running processes in that namespace. By default, all containers, including those with `--network=host`, have their own UTS namespace. Setting `--uts` to `host` results in the container using the same UTS namespace as the host.

> Note
>
> Docker disallows combining the `--hostname` and `--domainname` flags with `--uts=host`. This is to prevent containers running in the host's UTS namespace from attempting to change the hosts' configuration.

You may wish to share the UTS namespace with the host if you would like the hostname of the container to change as the hostname of the host changes. A more advanced use case would be changing the host's hostname from a container.

### [IPC settings (--ipc)](#ipc)

```text
--ipc="MODE"  : Set the IPC mode for the container
```

The `--ipc` flag accepts the following values:

| Value                      | Description                                                                      |
| -------------------------- | -------------------------------------------------------------------------------- |
| ""                         | Use daemon's default.                                                            |
| "none"                     | Own private IPC namespace, with /dev/shm not mounted.                            |
| "private"                  | Own private IPC namespace.                                                       |
| "shareable"                | Own private IPC namespace, with a possibility to share it with other containers. |
| "container:<*name-or-ID*>" | Join another ("shareable") container's IPC namespace.                            |
| "host"                     | Use the host system's IPC namespace.                                             |

If not specified, daemon default is used, which can either be `"private"` or `"shareable"`, depending on the daemon version and configuration.

[System V interprocess communication (IPC)](https://linux.die.net/man/5/ipc) namespaces provide separation of named shared memory segments, semaphores and message queues.

Shared memory segments are used to accelerate inter-process communication at memory speed, rather than through pipes or through the network stack. Shared memory is commonly used by databases and custom-built (typically C/OpenMPI, C++/using boost libraries) high performance applications for scientific computing and financial services industries. If these types of applications are broken into multiple containers, you might need to share the IPC mechanisms of the containers, using `"shareable"` mode for the main (i.e. "donor") container, and `"container:<donor-name-or-ID>"` for other containers.

### [Escalate container privileges (--privileged)](#privileged)

The `--privileged` flag gives the following capabilities to a container:

* Enables all Linux kernel capabilities
* Disables the default seccomp profile
* Disables the default AppArmor profile
* Disables the SELinux process label
* Grants access to all host devices
* Makes `/sys` read-write
* Makes cgroups mounts read-write

In other words, the container can then do almost everything that the host can do. This flag exists to allow special use-cases, like running Docker within Docker.

> Warning
>
> Use the `--privileged` flag with caution. A container with `--privileged` is not a securely sandboxed process. Containers in this mode can get a root shell on the host and take control over the system.
>
> For most use cases, this flag should not be the preferred solution. If your container requires escalated privileges, you should prefer to explicitly grant the necessary permissions, for example by adding individual kernel capabilities with `--cap-add`.
>
> For more information, see [Runtime privilege and Linux capabilities](/engine/containers/run/#runtime-privilege-and-linux-capabilities)

The following example doesn't work, because by default, Docker drops most potentially dangerous kernel capabilities, including `CAP_SYS_ADMIN `(which is required to mount filesystems).

```console
$ docker run -t -i --rm ubuntu bash
root@bc338942ef20:/# mount -t tmpfs none /mnt
mount: permission denied
```

It works when you add the `--privileged` flag:

```console
$ docker run -t -i --privileged ubuntu bash
root@50e3f57e16e6:/# mount -t tmpfs none /mnt
root@50e3f57e16e6:/# df -h
Filesystem      Size  Used Avail Use% Mounted on
none            1.9G     0  1.9G   0% /mnt
```

### [Set working directory (-w, --workdir)](#workdir)

```console
$ docker run -w /path/to/dir/ ubuntu pwd
```

The `-w` option runs the command executed inside the directory specified, in this example, `/path/to/dir/`. If the path doesn't exist, Docker creates it inside the container.

### [Set storage driver options per container (--storage-opt)](#storage-opt)

```console
$ docker run -it --storage-opt size=120G fedora /bin/bash
```

This (size) constraints the container filesystem size to 120G at creation time. This option is only available for the `btrfs`, `overlay2`, `windowsfilter`, and `zfs` storage drivers.

For the `overlay2` storage driver, the size option is only available if the backing filesystem is `xfs` and mounted with the `pquota` mount option. Under these conditions, you can pass any size less than the backing filesystem size.

For the `windowsfilter`, `btrfs`, and `zfs` storage drivers, you cannot pass a size less than the Default BaseFS Size.

### [Mount tmpfs (--tmpfs)](#tmpfs)

The `--tmpfs` flag lets you create a `tmpfs` mount.

The options that you can pass to `--tmpfs` are identical to the Linux `mount -t tmpfs -o` command. The following example mounts an empty `tmpfs` into the container with the `rw`, `noexec`, `nosuid`, `size=65536k` options.

```console
$ docker run -d --tmpfs /run:rw,noexec,nosuid,size=65536k my_image
```

For more information, see [tmpfs mounts](/storage/tmpfs/).

### [Mount volume (-v)](#volume)

```console
$ docker  run  -v $(pwd):$(pwd) -w $(pwd) -i -t  ubuntu pwd
```

The example above mounts the current directory into the container at the same path using the `-v` flag, sets it as the working directory, and then runs the `pwd` command inside the container.

As of Docker Engine version 23, you can use relative paths on the host.

```console
$ docker  run  -v ./content:/content -w /content -i -t  ubuntu pwd
```

The example above mounts the `content` directory in the current directory into the container at the `/content` path using the `-v` flag, sets it as the working directory, and then runs the `pwd` command inside the container.

```console
$ docker run -v /doesnt/exist:/foo -w /foo -i -t ubuntu bash
```

When the host directory of a bind-mounted volume doesn't exist, Docker automatically creates this directory on the host for you. In the example above, Docker creates the `/doesnt/exist` folder before starting your container.

### [Mount volume read-only (--read-only)](#read-only)

```console
$ docker run --read-only -v /icanwrite busybox touch /icanwrite/here
```

You can use volumes in combination with the `--read-only` flag to control where a container writes files. The `--read-only` flag mounts the container's root filesystem as read only prohibiting writes to locations other than the specified volumes for the container.

```console
$ docker run -t -i -v /var/run/docker.sock:/var/run/docker.sock -v /path/to/static-docker-binary:/usr/bin/docker busybox sh
```

By bind-mounting the Docker Unix socket and statically linked Docker binary (refer to [get the Linux binary](/engine/install/binaries/#install-static-binaries)), you give the container the full access to create and manipulate the host's Docker daemon.

On Windows, you must specify the paths using Windows-style path semantics.

```powershell
PS C:\> docker run -v c:\foo:c:\dest microsoft/nanoserver cmd /s /c type c:\dest\somefile.txt
Contents of file

PS C:\> docker run -v c:\foo:d: microsoft/nanoserver cmd /s /c type d:\somefile.txt
Contents of file
```

The following examples fails when using Windows-based containers, as the destination of a volume or bind mount inside the container must be one of: a non-existing or empty directory; or a drive other than `C:`. Further, the source of a bind mount must be a local directory, not a file.

```powershell
net use z: \\remotemachine\share
docker run -v z:\foo:c:\dest ...
docker run -v \\uncpath\to\directory:c:\dest ...
docker run -v c:\foo\somefile.txt:c:\dest ...
docker run -v c:\foo:c: ...
docker run -v c:\foo:c:\existing-directory-with-contents ...
```

For in-depth information about volumes, refer to [manage data in containers](/storage/volumes/)

### [Add bind mounts or volumes using the --mount flag](#mount)

The `--mount` flag allows you to mount volumes, host-directories, and `tmpfs` mounts in a container.

The `--mount` flag supports most options supported by the `-v` or the `--volume` flag, but uses a different syntax. For in-depth information on the `--mount` flag, and a comparison between `--volume` and `--mount`, refer to [Bind mounts](/storage/bind-mounts/).

Even though there is no plan to deprecate `--volume`, usage of `--mount` is recommended.

Examples:

```console
$ docker run --read-only --mount type=volume,target=/icanwrite busybox touch /icanwrite/here
```

```console
$ docker run -t -i --mount type=bind,src=/data,dst=/data busybox sh
```

### [Publish or expose port (-p, --expose)](#publish)

```console
$ docker run -p 127.0.0.1:80:8080/tcp nginx:alpine
```

This binds port `8080` of the container to TCP port `80` on `127.0.0.1` of the host. You can also specify `udp` and `sctp` ports. The [Networking overview page](/network/) explains in detail how to publish ports with Docker.

> Note
>
> If you don't specify an IP address (i.e., `-p 80:80` instead of `-p 127.0.0.1:80:80`) when publishing a container's ports, Docker publishes the port on all interfaces (address `0.0.0.0`) by default. These ports are externally accessible. This also applies if you configured UFW to block this specific port, as Docker manages its own iptables rules. [Read more](/network/packet-filtering-firewalls/)

```console
$ docker run --expose 80 nginx:alpine
```

This exposes port `80` of the container without publishing the port to the host system's interfaces.

### [Publish all exposed ports (-P, --publish-all)](#publish-all)

```console
$ docker run -P nginx:alpine
```

The `-P`, or `--publish-all`, flag publishes all the exposed ports to the host. Docker binds each exposed port to a random port on the host.

The `-P` flag only publishes port numbers that are explicitly flagged as exposed, either using the Dockerfile `EXPOSE` instruction or the `--expose` flag for the `docker run` command.

The range of ports are within an *ephemeral port range* defined by `/proc/sys/net/ipv4/ip_local_port_range`. Use the `-p` flag to explicitly map a single port or range of ports.

### [Set the pull policy (--pull)](#pull)

Use the `--pull` flag to set the image pull policy when creating (and running) the container.

The `--pull` flag can take one of these values:

| Value               | Description                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `missing` (default) | Pull the image if it was not found in the image cache, or use the cached image otherwise.                         |
| `never`             | Do not pull the image, even if it's missing, and produce an error if the image does not exist in the image cache. |
| `always`            | Always perform a pull before creating the container.                                                              |

When creating (and running) a container from an image, the daemon checks if the image exists in the local image cache. If the image is missing, an error is returned to the CLI, allowing it to initiate a pull.

The default (`missing`) is to only pull the image if it's not present in the daemon's image cache. This default allows you to run images that only exist locally (for example, images you built from a Dockerfile, but that have not been pushed to a registry), and reduces networking.

The `always` option always initiates a pull before creating the container. This option makes sure the image is up-to-date, and prevents you from using outdated images, but may not be suitable in situations where you want to test a locally built image before pushing (as pulling the image overwrites the existing image in the image cache).

The `never` option disables (implicit) pulling images when creating containers, and only uses images that are available in the image cache. If the specified image is not found, an error is produced, and the container is not created. This option is useful in situations where networking is not available, or to prevent images from being pulled implicitly when creating containers.

The following example shows `docker run` with the `--pull=never` option set, which produces en error as the image is missing in the image-cache:

```console
$ docker run --pull=never hello-world
docker: Error response from daemon: No such image: hello-world:latest.
```

### [Set environment variables (-e, --env, --env-file)](#env)

```console
$ docker run -e MYVAR1 --env MYVAR2=foo --env-file ./env.list ubuntu bash
```

Use the `-e`, `--env`, and `--env-file` flags to set simple (non-array) environment variables in the container you're running, or overwrite variables defined in the Dockerfile of the image you're running.

You can define the variable and its value when running the container:

```console
$ docker run --env VAR1=value1 --env VAR2=value2 ubuntu env | grep VAR
VAR1=value1
VAR2=value2
```

You can also use variables exported to your local environment:

```console
export VAR1=value1
export VAR2=value2

$ docker run --env VAR1 --env VAR2 ubuntu env | grep VAR
VAR1=value1
VAR2=value2
```

When running the command, the Docker CLI client checks the value the variable has in your local environment and passes it to the container. If no `=` is provided and that variable isn't exported in your local environment, the variable is unset in the container.

You can also load the environment variables from a file. This file should use the syntax `<variable>=value` (which sets the variable to the given value) or `<variable>` (which takes the value from the local environment), and `#` for comments. Lines beginning with `#` are treated as line comments and are ignored, whereas a `#` appearing anywhere else in a line is treated as part of the variable value.

```console
$ cat env.list
# This is a comment
VAR1=value1
VAR2=value2
USER

$ docker run --env-file env.list ubuntu env | grep -E 'VAR|USER'
VAR1=value1
VAR2=value2
USER=jonzeolla
```

### [Set metadata on container (-l, --label, --label-file)](#label)

A label is a `key=value` pair that applies metadata to a container. To label a container with two labels:

```console
$ docker run -l my-label --label com.example.foo=bar ubuntu bash
```

The `my-label` key doesn't specify a value so the label defaults to an empty string (`""`). To add multiple labels, repeat the label flag (`-l` or `--label`).

The `key=value` must be unique to avoid overwriting the label value. If you specify labels with identical keys but different values, each subsequent value overwrites the previous. Docker uses the last `key=value` you supply.

Use the `--label-file` flag to load multiple labels from a file. Delimit each label in the file with an EOL mark. The example below loads labels from a labels file in the current directory:

```console
$ docker run --label-file ./labels ubuntu bash
```

The label-file format is similar to the format for loading environment variables. (Unlike environment variables, labels are not visible to processes running inside a container.) The following example shows a label-file format:

```console
com.example.label1="a label"

# this is a comment
com.example.label2=another\ label
com.example.label3
```

You can load multiple label-files by supplying multiple `--label-file` flags.

For additional information on working with labels, see [Labels](/config/labels-custom-metadata/).

### [Connect a container to a network (--network)](#network)

To start a container and connect it to a network, use the `--network` option.

If you want to add a running container to a network use the `docker network connect` subcommand.

You can connect multiple containers to the same network. Once connected, the containers can communicate using only another container's IP address or name. For `overlay` networks or custom plugins that support multi-host connectivity, containers connected to the same multi-host network but launched from different Engines can also communicate in this way.

> Note
>
> The default bridge network only allows containers to communicate with each other using internal IP addresses. User-created bridge networks provide DNS resolution between containers using container names.

You can disconnect a container from a network using the `docker network disconnect` command.

The following commands create a network named `my-net` and add a `busybox` container to the `my-net` network.

```console
$ docker network create my-net
$ docker run -itd --network=my-net busybox
```

You can also choose the IP addresses for the container with `--ip` and `--ip6` flags when you start the container on a user-defined network. To assign a static IP to containers, you must specify subnet block for the network.

```console
$ docker network create --subnet 192.0.2.0/24 my-net
$ docker run -itd --network=my-net --ip=192.0.2.69 busybox
```

To connect the container to more than one network, repeat the `--network` option.

```console
$ docker network create --subnet 192.0.2.0/24 my-net1
$ docker network create --subnet 192.0.3.0/24 my-net2
$ docker run -itd --network=my-net1 --network=my-net2 busybox
```

To specify options when connecting to more than one network, use the extended syntax for the `--network` flag. Comma-separated options that can be specified in the extended `--network` syntax are:

| Option          | Top-level Equivalent                  | Description                                                                             |
| --------------- | ------------------------------------- | --------------------------------------------------------------------------------------- |
| `name`          |                                       | The name of the network (mandatory)                                                     |
| `alias`         | `--network-alias`                     | Add network-scoped alias for the container                                              |
| `ip`            | `--ip`                                | IPv4 address (e.g., 172.30.100.104)                                                     |
| `ip6`           | `--ip6`                               | IPv6 address (e.g., 2001:db8::33)                                                       |
| `mac-address`   | `--mac-address`                       | Container MAC address (e.g., 92:d0:c6:0a:29:33)                                         |
| `link-local-ip` | `--link-local-ip`                     | Container IPv4/IPv6 link-local addresses                                                |
| `driver-opt`    | `docker network connect --driver-opt` | Network driver options                                                                  |
| `gw-priority`   |                                       | Highest gw-priority provides the default gateway. Accepts positive and negative values. |

```console
$ docker network create --subnet 192.0.2.0/24 my-net1
$ docker network create --subnet 192.0.3.0/24 my-net2
$ docker run -itd --network=name=my-net1,ip=192.0.2.42 --network=name=my-net2,ip=192.0.3.42 busybox
```

`sysctl` settings that start with `net.ipv4.`, `net.ipv6.` or `net.mpls.` can be set per-interface using `driver-opt` label `com.docker.network.endpoint.sysctls`. The interface name must be the string `IFNAME`.

To set more than one `sysctl` for an interface, quote the whole `driver-opt` field, remembering to escape the quotes for the shell if necessary. For example, if the interface to `my-net` is given name `eth0`, the following example sets sysctls `net.ipv4.conf.eth0.log_martians=1` and `net.ipv4.conf.eth0.forwarding=0`, and assigns the IPv4 address `192.0.2.42`.

```console
$ docker network create --subnet 192.0.2.0/24 my-net
$ docker run -itd --network=name=my-net,\"driver-opt=com.docker.network.endpoint.sysctls=net.ipv4.conf.IFNAME.log_martians=1,net.ipv4.conf.IFNAME.forwarding=0\",ip=192.0.2.42 busybox
```

> Note
>
> Network drivers may restrict the sysctl settings that can be modified and, to protect the operation of the network, new restrictions may be added in the future.

For more information on connecting a container to a network when using the `run` command, see the [Docker network overview](/network/).

### [Mount volumes from container (--volumes-from)](#volumes-from)

```console
$ docker run --volumes-from 777f7dc92da7 --volumes-from ba8c0c54f0f2:ro -i -t ubuntu pwd
```

The `--volumes-from` flag mounts all the defined volumes from the referenced containers. You can specify more than one container by repetitions of the `--volumes-from` argument. The container ID may be optionally suffixed with `:ro` or `:rw` to mount the volumes in read-only or read-write mode, respectively. By default, Docker mounts the volumes in the same mode (read write or read only) as the reference container.

Labeling systems like SELinux require placing proper labels on volume content mounted into a container. Without a label, the security system might prevent the processes running inside the container from using the content. By default, Docker does not change the labels set by the OS.

To change the label in the container context, you can add either of two suffixes `:z` or `:Z` to the volume mount. These suffixes tell Docker to relabel file objects on the shared volumes. The `z` option tells Docker that two containers share the volume content. As a result, Docker labels the content with a shared content label. Shared volume labels allow all containers to read/write content. The `Z` option tells Docker to label the content with a private unshared label. Only the current container can use a private volume.

### [Detached mode (-d, --detach)](#detach)

The `--detach` (or `-d`) flag starts a container as a background process that doesn't occupy your terminal window. By design, containers started in detached mode exit when the root process used to run the container exits, unless you also specify the `--rm` option. If you use `-d` with `--rm`, the container is removed when it exits or when the daemon exits, whichever happens first.

Don't pass a `service x start` command to a detached container. For example, this command attempts to start the `nginx` service.

```console
$ docker run -d -p 80:80 my_image service nginx start
```

This succeeds in starting the `nginx` service inside the container. However, it fails the detached container paradigm in that, the root process (`service nginx start`) returns and the detached container stops as designed. As a result, the `nginx` service starts but can't be used. Instead, to start a process such as the `nginx` web server do the following:

```console
$ docker run -d -p 80:80 my_image nginx -g 'daemon off;'
```

To do input/output with a detached container use network connections or shared volumes. These are required because the container is no longer listening to the command line where `docker run` was run.

### [Add host device to container (--device)](#device)

```console
$ docker run -it --rm \
    --device=/dev/sdc:/dev/xvdc \
    --device=/dev/sdd \
    --device=/dev/zero:/dev/foobar \
    ubuntu ls -l /dev/{xvdc,sdd,foobar}

brw-rw---- 1 root disk 8, 2 Feb  9 16:05 /dev/xvdc
brw-rw---- 1 root disk 8, 3 Feb  9 16:05 /dev/sdd
crw-rw-rw- 1 root root 1, 5 Feb  9 16:05 /dev/foobar
```

It's often necessary to directly expose devices to a container. The `--device` option enables that. For example, adding a specific block storage device or loop device or audio device to an otherwise unprivileged container (without the `--privileged` flag) and have the application directly access it.

By default, the container is able to `read`, `write` and `mknod` these devices. This can be overridden using a third `:rwm` set of options to each `--device` flag. If the container is running in privileged mode, then Docker ignores the specified permissions.

```console
$ docker run --device=/dev/sda:/dev/xvdc --rm -it ubuntu fdisk  /dev/xvdc

Command (m for help): q
$ docker run --device=/dev/sda:/dev/xvdc:r --rm -it ubuntu fdisk  /dev/xvdc
You will not be able to write the partition table.

Command (m for help): q

$ docker run --device=/dev/sda:/dev/xvdc:rw --rm -it ubuntu fdisk  /dev/xvdc

Command (m for help): q

$ docker run --device=/dev/sda:/dev/xvdc:m --rm -it ubuntu fdisk  /dev/xvdc
fdisk: unable to open /dev/xvdc: Operation not permitted
```

> Note
>
> The `--device` option cannot be safely used with ephemeral devices. You shouldn't add block devices that may be removed to untrusted containers with `--device`.

For Windows, the format of the string passed to the `--device` option is in the form of `--device=<IdType>/<Id>`. Beginning with Windows Server 2019 and Windows 10 October 2018 Update, Windows only supports an IdType of `class` and the Id as a [device interface class GUID](https://docs.microsoft.com/en-us/windows-hardware/drivers/install/overview-of-device-interface-classes). Refer to the table defined in the [Windows container docs](https://docs.microsoft.com/en-us/virtualization/windowscontainers/deploy-containers/hardware-devices-in-containers) for a list of container-supported device interface class GUIDs.

If you specify this option for a process-isolated Windows container, Docker makes *all* devices that implement the requested device interface class GUID available in the container. For example, the command below makes all COM ports on the host visible in the container.

```powershell
PS C:\> docker run --device=class/86E0D1E0-8089-11D0-9CE4-08003E301F73 mcr.microsoft.com/windows/servercore:ltsc2019
```

> Note
>
> The `--device` option is only supported on process-isolated Windows containers, and produces an error if the container isolation is `hyperv`.

#### [CDI devices](#cdi-devices)

[Container Device Interface (CDI)](https://github.com/cncf-tags/container-device-interface/blob/main/SPEC.md) is a standardized mechanism for container runtimes to create containers which are able to interact with third party devices.

CDI is currently only supported for Linux containers and is enabled by default since Docker Engine 28.3.0.

With CDI, device configurations are declaratively defined using a JSON or YAML file. In addition to enabling the container to interact with the device node, it also lets you specify additional configuration for the device, such as environment variables, host mounts (such as shared objects), and executable hooks.

You can reference a CDI device with the `--device` flag using the fully-qualified name of the device, as shown in the following example:

```console
$ docker run --device=vendor.com/class=device-name --rm -it ubuntu
```

This starts an `ubuntu` container with access to the specified CDI device, `vendor.com/class=device-name`, assuming that:

* A valid CDI specification (JSON or YAML file) for the requested device is available on the system running the daemon, in one of the configured CDI specification directories.
* The CDI feature has been enabled in the daemon; see [Enable CDI devices](/reference/cli/dockerd/#configure-cdi-devices).

### [Attach to STDIN/STDOUT/STDERR (-a, --attach)](#attach)

The `--attach` (or `-a`) flag tells `docker run` to bind to the container's `STDIN`, `STDOUT` or `STDERR`. This makes it possible to manipulate the output and input as needed. You can specify to which of the three standard streams (`STDIN`, `STDOUT`, `STDERR`) you'd like to connect instead, as in:

```console
$ docker run -a stdin -a stdout -i -t ubuntu /bin/bash
```

The following example pipes data into a container and prints the container's ID by attaching only to the container's `STDIN`.

```console
$ echo "test" | docker run -i -a stdin ubuntu cat -
```

The following example doesn't print anything to the console unless there's an error because output is only attached to the `STDERR` of the container. The container's logs still store what's written to `STDERR` and `STDOUT`.

```console
$ docker run -a stderr ubuntu echo test
```

The following example shows a way of using `--attach` to pipe a file into a container. The command prints the container's ID after the build completes and you can retrieve the build logs using `docker logs`. This is useful if you need to pipe a file or something else into a container and retrieve the container's ID once the container has finished running.

```console
$ cat somefile | docker run -i -a stdin mybuilder dobuild
```

> Note
>
> A process running as PID 1 inside a container is treated specially by Linux: it ignores any signal with the default action. So, the process doesn't terminate on `SIGINT` or `SIGTERM` unless it's coded to do so.

See also [the `docker cp` command](/reference/cli/docker/container/cp/).

### [Keep STDIN open (-i, --interactive)](#interactive)

The `--interactive` (or `-i`) flag keeps the container's `STDIN` open, and lets you send input to the container through standard input.

```console
$ echo hello | docker run --rm -i busybox cat
hello
```

The `-i` flag is most often used together with the `--tty` flag to bind the I/O streams of the container to a pseudo terminal, creating an interactive terminal session for the container. See [Allocate a pseudo-TTY](#tty) for more examples.

```console
$ docker run -it debian
root@10a3e71492b0:/# factor 90
90: 2 3 3 5
root@10a3e71492b0:/# exit
exit
```

Using the `-i` flag on its own allows for composition, such as piping input to containers:

```console
$ docker run --rm -i busybox echo "foo bar baz" \
  | docker run --rm -i busybox awk '{ print $2 }' \
  | docker run --rm -i busybox rev
rab
```

### [Specify an init process](#init)

You can use the `--init` flag to indicate that an init process should be used as the PID 1 in the container. Specifying an init process ensures the usual responsibilities of an init system, such as reaping zombie processes, are performed inside the created container.

The default init process used is the first `docker-init` executable found in the system path of the Docker daemon process. This `docker-init` binary, included in the default installation, is backed by [tini](https://github.com/krallin/tini).

### [Allocate a pseudo-TTY (-t, --tty)](#tty)

The `--tty` (or `-t`) flag attaches a pseudo-TTY to the container, connecting your terminal to the I/O streams of the container. Allocating a pseudo-TTY to the container means that you get access to input and output feature that TTY devices provide.

For example, the following command runs the `passwd` command in a `debian` container, to set a new password for the `root` user.

```console
$ docker run -i debian passwd root
New password: karjalanpiirakka9
Retype new password: karjalanpiirakka9
passwd: password updated successfully
```

If you run this command with only the `-i` flag (which lets you send text to `STDIN` of the container), the `passwd` prompt displays the password in plain text. However, if you try the same thing but also adding the `-t` flag, the password is hidden:

```console
$ docker run -it debian passwd root
New password:
Retype new password:
passwd: password updated successfully
```

This is because `passwd` can suppress the output of characters to the terminal using the echo-off TTY feature.

You can use the `-t` flag without `-i` flag. This still allocates a pseudo-TTY to the container, but with no way of writing to `STDIN`. The only time this might be useful is if the output of the container requires a TTY environment.

### [Specify custom cgroups](#cgroup-parent)

Using the `--cgroup-parent` flag, you can pass a specific cgroup to run a container in. This allows you to create and manage cgroups on their own. You can define custom resources for those cgroups and put containers under a common parent group.

### [Using dynamically created devices (--device-cgroup-rule)](#device-cgroup-rule)

Docker assigns devices available to a container at creation time. The assigned devices are added to the cgroup.allow file and created into the container when it runs. This poses a problem when you need to add a new device to running container.

One solution is to add a more permissive rule to a container allowing it access to a wider range of devices. For example, supposing the container needs access to a character device with major `42` and any number of minor numbers (added as new devices appear), add the following rule:

```console
$ docker run -d --device-cgroup-rule='c 42:* rmw' --name my-container my-image
```

Then, a user could ask `udev` to execute a script that would `docker exec my-container mknod newDevX c 42 <minor>` the required device when it is added.

> Note
>
> You still need to explicitly add initially present devices to the `docker run` / `docker create` command.

### [Access an NVIDIA GPU](#gpus)

The `--gpus` flag allows you to access NVIDIA GPU resources. First you need to install the [nvidia-container-runtime](https://nvidia.github.io/nvidia-container-runtime/).

> Note
>
> You can also specify a GPU as a CDI device with the `--device` flag, see [CDI devices](#cdi-devices).

Read [Specify a container's resources](/config/containers/resource_constraints/) for more information.

To use `--gpus`, specify which GPUs (or all) to use. If you provide no value, Docker uses all available GPUs. The example below exposes all available GPUs.

```console
$ docker run -it --rm --gpus all ubuntu nvidia-smi
```

Use the `device` option to specify GPUs. The example below exposes a specific GPU.

```console
$ docker run -it --rm --gpus device=GPU-3a23c669-1f69-c64e-cf85-44e9b07e7a2a ubuntu nvidia-smi
```

The example below exposes the first and third GPUs.

```console
$ docker run -it --rm --gpus '"device=0,2"' ubuntu nvidia-smi
```

### [Restart policies (--restart)](#restart)

Use the `--restart` flag to specify a container's *restart policy*. A restart policy controls whether the Docker daemon restarts a container after exit. Docker supports the following restart policies:

| Flag                       | Description                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `no`                       | Don't automatically restart the container. (Default)                                                                                                                                                                                                                                                                                                                  |
| `on-failure[:max-retries]` | Restart the container if it exits due to an error, which manifests as a non-zero exit code. Optionally, limit the number of times the Docker daemon attempts to restart the container using the `:max-retries` option. The `on-failure` policy only prompts a restart if the container exits with a failure. It doesn't restart the container if the daemon restarts. |
| `always`                   | Always restart the container if it stops. If it's manually stopped, it's restarted only when Docker daemon restarts or the container itself is manually restarted.                                                                                                                                                                                                    |
| `unless-stopped`           | Similar to `always`, except that when the container is stopped (manually or otherwise), it isn't restarted even after Docker daemon restarts.                                                                                                                                                                                                                         |

```console
$ docker run --restart=always redis
```

This runs the `redis` container with a restart policy of **always**. If the container exits, Docker restarts it.

When a restart policy is active on a container, it shows as either `Up` or `Restarting` in [`docker ps`](/reference/cli/docker/container/ls/). It can also be useful to use [`docker events`](/reference/cli/docker/system/events/) to see the restart policy in effect.

An increasing delay (double the previous delay, starting at 100 milliseconds) is added before each restart to prevent flooding the server. This means the daemon waits for 100 ms, then 200 ms, 400, 800, 1600, and so on until either the `on-failure` limit, the maximum delay of 1 minute is hit, or when you `docker stop` or `docker rm -f` the container.

If a container is successfully restarted (the container is started and runs for at least 10 seconds), the delay is reset to its default value of 100 ms.

#### [Specify a limit for restart attempts](#specify-a-limit-for-restart-attempts)

You can specify the maximum amount of times Docker attempts to restart the container when using the **on-failure** policy. By default, Docker never stops attempting to restart the container.

The following example runs the `redis` container with a restart policy of **on-failure** and a maximum restart count of 10.

```console
$ docker run --restart=on-failure:10 redis
```

If the `redis` container exits with a non-zero exit status more than 10 times in a row, Docker stops trying to restart the container. Providing a maximum restart limit is only valid for the **on-failure** policy.

#### [Inspect container restarts](#inspect-container-restarts)

The number of (attempted) restarts for a container can be obtained using the [`docker inspect`](/reference/cli/docker/inspect/) command. For example, to get the number of restarts for container "my-container";

```console
$ docker inspect -f "{{ .RestartCount }}" my-container
2
```

Or, to get the last time the container was (re)started;

```console
$ docker inspect -f "{{ .State.StartedAt }}" my-container
2015-03-04T23:47:07.691840179Z
```

Combining `--restart` (restart policy) with the `--rm` (clean up) flag results in an error. On container restart, attached clients are disconnected.

### [Clean up (--rm)](#rm)

By default, a container's file system persists even after the container exits. This makes debugging a lot easier, since you can inspect the container's final state and you retain all your data.

If you are running short-term **foreground** processes, these container file systems can start to pile up. If you'd like Docker to automatically clean up the container and remove the file system when the container exits, use the `--rm` flag:

```text
--rm: Automatically remove the container and its associated anonymous volumes when it exits
```

> Note
>
> If you set the `--rm` flag, Docker also removes the anonymous volumes associated with the container when the container is removed. This is similar to running `docker rm -v my-container`. Only volumes that are specified without a name are removed. For example, when running the following command, volume `/foo` is removed, but not `/bar`:
>
> ```console
> $ docker run --rm -v /foo -v awesome:/bar busybox top
> ```
>
> Volumes inherited via `--volumes-from` are removed with the same logic: if the original volume was specified with a name it isn't removed.

### [Add entries to container hosts file (--add-host)](#add-host)

You can add other hosts into a container's `/etc/hosts` file by using one or more `--add-host` flags. This example adds a static address for a host named `my-hostname`:

```console
$ docker run --add-host=my-hostname=8.8.8.8 --rm -it alpine

/ # ping my-hostname
PING my-hostname (8.8.8.8): 56 data bytes
64 bytes from 8.8.8.8: seq=0 ttl=37 time=93.052 ms
64 bytes from 8.8.8.8: seq=1 ttl=37 time=92.467 ms
64 bytes from 8.8.8.8: seq=2 ttl=37 time=92.252 ms
^C
--- my-hostname ping statistics ---
4 packets transmitted, 4 packets received, 0% packet loss
round-trip min/avg/max = 92.209/92.495/93.052 ms
```

You can wrap an IPv6 address in square brackets:

```console
$ docker run --add-host my-hostname=[2001:db8::33] --rm -it alpine
```

The `--add-host` flag supports a special `host-gateway` value that resolves to the internal IP address of the host. This is useful when you want containers to connect to services running on the host machine.

It's conventional to use `host.docker.internal` as the hostname referring to `host-gateway`. Docker Desktop automatically resolves this hostname, see [Explore networking how-tos on Docker Desktop](/desktop/features/networking/networking-how-tos/#connect-a-container-to-a-service-on-the-host) and [Configure host gateway IP](/reference/cli/dockerd/#configure-host-gateway-ip).

The following example shows how the special `host-gateway` value works. The example runs an HTTP server that serves a file from host to container over the `host.docker.internal` hostname, which resolves to the host's internal IP.

```console
$ echo "hello from host!" > ./hello
$ python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
$ docker run \
  --add-host host.docker.internal=host-gateway \
  curlimages/curl -s host.docker.internal:8000/hello
hello from host!
```

The `--add-host` flag also accepts a `:` separator, for example:

```console
$ docker run --add-host=my-hostname:8.8.8.8 --rm -it alpine
```

### [Logging drivers (--log-driver)](#log-driver)

The container can have a different logging driver than the Docker daemon. Use the `--log-driver=<DRIVER>` with the `docker run` command to configure the container's logging driver.

To learn about the supported logging drivers and how to use them, refer to [Configure logging drivers](/engine/logging/configure/).

To disable logging for a container, set the `--log-driver` flag to `none`:

```console
$ docker run --log-driver=none -d nginx:alpine
5101d3b7fe931c27c2ba0e65fd989654d297393ad65ae238f20b97a020e7295b
$ docker logs 5101d3b
Error response from daemon: configured logging driver does not support reading
```

### [Set ulimits in container (--ulimit)](#ulimit)

Since setting `ulimit` settings in a container requires extra privileges not available in the default container, you can set these using the `--ulimit` flag. Specify `--ulimit` with a soft and hard limit in the format `<type>=<soft limit>[:<hard limit>]`. For example:

```console
$ docker run --ulimit nofile=1024:1024 --rm debian sh -c "ulimit -n"
1024
```

> Note
>
> If you don't provide a hard limit value, Docker uses the soft limit value for both values. If you don't provide any values, they are inherited from the default `ulimits` set on the daemon.

> Note
>
> The `as` option is deprecated. In other words, the following script is not supported:
>
> ```console
> $ docker run -it --ulimit as=1024 fedora /bin/bash
> ```

#### [Supported options for `--ulimit`:](#supported-options-for---ulimit)

| Option       | Description                                               |
| ------------ | --------------------------------------------------------- |
| `core`       | Maximum size of core files created (`RLIMIT_CORE`)        |
| `cpu`        | CPU time limit in seconds (`RLIMIT_CPU`)                  |
| `data`       | Maximum data segment size (`RLIMIT_DATA`)                 |
| `fsize`      | Maximum file size (`RLIMIT_FSIZE`)                        |
| `locks`      | Maximum number of file locks (`RLIMIT_LOCKS`)             |
| `memlock`    | Maximum locked-in-memory address space (`RLIMIT_MEMLOCK`) |
| `msgqueue`   | Maximum bytes in POSIX message queues (`RLIMIT_MSGQUEUE`) |
| `nice`       | Maximum nice priority adjustment (`RLIMIT_NICE`)          |
| `nofile`     | Maximum number of open file descriptors (`RLIMIT_NOFILE`) |
| `nproc`      | Maximum number of processes available (`RLIMIT_NPROC`)    |
| `rss`        | Maximum resident set size (`RLIMIT_RSS`)                  |
| `rtprio`     | Maximum real-time scheduling priority (`RLIMIT_RTPRIO`)   |
| `rttime`     | Maximum real-time execution time (`RLIMIT_RTTIME`)        |
| `sigpending` | Maximum number of pending signals (`RLIMIT_SIGPENDING`)   |
| `stack`      | Maximum stack size (`RLIMIT_STACK`)                       |

Docker sends the values to the appropriate OS `syscall` and doesn't perform any byte conversion. Take this into account when setting the values.

#### [For `nproc` usage](#for-nproc-usage)

Be careful setting `nproc` with the `ulimit` flag as Linux uses `nproc` to set the maximum number of processes available to a user, not to a container. For example, start four containers with `daemon` user:

```console
$ docker run -d -u daemon --ulimit nproc=3 busybox top

$ docker run -d -u daemon --ulimit nproc=3 busybox top

$ docker run -d -u daemon --ulimit nproc=3 busybox top

$ docker run -d -u daemon --ulimit nproc=3 busybox top
```

The 4th container fails and reports a "\[8] System error: resource temporarily unavailable" error. This fails because the caller set `nproc=3` resulting in the first three containers using up the three processes quota set for the `daemon` user.

### [Stop container with signal (--stop-signal)](#stop-signal)

The `--stop-signal` flag sends the system call signal to the container to exit. This signal can be a signal name in the format `SIG<NAME>`, for instance `SIGKILL`, or an unsigned number that matches a position in the kernel's syscall table, for instance `9`.

The default value is defined by [`STOPSIGNAL`](/reference/dockerfile/#stopsignal) in the image, or `SIGTERM` if the image has no `STOPSIGNAL` defined.

### [Optional security options (--security-opt)](#security-opt)

| Option                                    | Description                                                                                                                                                                                                      |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--security-opt="label=user:USER"`        | Set the label user for the container                                                                                                                                                                             |
| `--security-opt="label=role:ROLE"`        | Set the label role for the container                                                                                                                                                                             |
| `--security-opt="label=type:TYPE"`        | Set the label type for the container                                                                                                                                                                             |
| `--security-opt="label=level:LEVEL"`      | Set the label level for the container                                                                                                                                                                            |
| `--security-opt="label=disable"`          | Turn off label confinement for the container                                                                                                                                                                     |
| `--security-opt="apparmor=PROFILE"`       | Set the apparmor profile to be applied to the container                                                                                                                                                          |
| `--security-opt="no-new-privileges=true"` | Disable container processes from gaining new privileges                                                                                                                                                          |
| `--security-opt="seccomp=unconfined"`     | Turn off seccomp confinement for the container                                                                                                                                                                   |
| `--security-opt="seccomp=builtin"`        | Use the default (built-in) seccomp profile for the container. This can be used to enable seccomp for a container running on a daemon with a custom default profile set, or with seccomp disabled ("unconfined"). |
| `--security-opt="seccomp=profile.json"`   | White-listed syscalls seccomp Json file to be used as a seccomp filter                                                                                                                                           |
| `--security-opt="systempaths=unconfined"` | Turn off confinement for system paths (masked paths, read-only paths) for the container                                                                                                                          |

The `--security-opt` flag lets you override the default labeling scheme for a container. Specifying the level in the following command allows you to share the same content between containers.

```console
$ docker run --security-opt label=level:s0:c100,c200 -it fedora bash
```

> Note
>
> Automatic translation of MLS labels isn't supported.

To disable the security labeling for a container entirely, you can use `label=disable`:

```console
$ docker run --security-opt label=disable -it ubuntu bash
```

If you want a tighter security policy on the processes within a container, you can specify a custom `type` label. The following example runs a container that's only allowed to listen on Apache ports:

```console
$ docker run --security-opt label=type:svirt_apache_t -it ubuntu bash
```

> Note
>
> You would have to write policy defining a `svirt_apache_t` type.

To prevent your container processes from gaining additional privileges, you can use the following command:

```console
$ docker run --security-opt no-new-privileges -it ubuntu bash
```

This means that commands that raise privileges such as `su` or `sudo` no longer work. It also causes any seccomp filters to be applied later, after privileges have been dropped which may mean you can have a more restrictive set of filters. For more details, see the [kernel documentation](https://www.kernel.org/doc/Documentation/prctl/no_new_privs.txt).

On Windows, you can use the `--security-opt` flag to specify the `credentialspec` option. The `credentialspec` must be in the format `file://spec.txt` or `registry://keyname`.

### [Stop container with timeout (--stop-timeout)](#stop-timeout)

The `--stop-timeout` flag sets the number of seconds to wait for the container to stop after sending the pre-defined (see `--stop-signal`) system call signal. If the container does not exit after the timeout elapses, it's forcibly killed with a `SIGKILL` signal.

If you set `--stop-timeout` to `-1`, no timeout is applied, and the daemon waits indefinitely for the container to exit.

The Daemon determines the default, and is 10 seconds for Linux containers, and 30 seconds for Windows containers.

### [Specify isolation technology for container (--isolation)](#isolation)

This option is useful in situations where you are running Docker containers on Windows. The `--isolation=<value>` option sets a container's isolation technology. On Linux, the only supported is the `default` option which uses Linux namespaces. These two commands are equivalent on Linux:

```console
$ docker run -d busybox top
$ docker run -d --isolation default busybox top
```

On Windows, `--isolation` can take one of these values:

| Value     | Description                                                                                |
| --------- | ------------------------------------------------------------------------------------------ |
| `default` | Use the value specified by the Docker daemon's `--exec-opt` or system default (see below). |
| `process` | Shared-kernel namespace isolation.                                                         |
| `hyperv`  | Hyper-V hypervisor partition-based isolation.                                              |

The default isolation on Windows server operating systems is `process`, and `hyperv` on Windows client operating systems, such as Windows 10. Process isolation has better performance, but requires that the image and host use the same kernel version.

On Windows server, assuming the default configuration, these commands are equivalent and result in `process` isolation:

```powershell
PS C:\> docker run -d microsoft/nanoserver powershell echo process
PS C:\> docker run -d --isolation default microsoft/nanoserver powershell echo process
PS C:\> docker run -d --isolation process microsoft/nanoserver powershell echo process
```

If you have set the `--exec-opt isolation=hyperv` option on the Docker `daemon`, or are running against a Windows client-based daemon, these commands are equivalent and result in `hyperv` isolation:

```powershell
PS C:\> docker run -d microsoft/nanoserver powershell echo hyperv
PS C:\> docker run -d --isolation default microsoft/nanoserver powershell echo hyperv
PS C:\> docker run -d --isolation hyperv microsoft/nanoserver powershell echo hyperv
```

### [Specify hard limits on memory available to containers (-m, --memory)](#memory)

These parameters always set an upper limit on the memory available to the container. Linux sets this on the cgroup and applications in a container can query it at `/sys/fs/cgroup/memory/memory.limit_in_bytes`.

On Windows, this affects containers differently depending on what type of isolation you use.

* With `process` isolation, Windows reports the full memory of the host system, not the limit to applications running inside the container

  ```powershell
  PS C:\> docker run -it -m 2GB --isolation=process microsoft/nanoserver powershell Get-ComputerInfo *memory*

  CsTotalPhysicalMemory      : 17064509440
  CsPhyicallyInstalledMemory : 16777216
  OsTotalVisibleMemorySize   : 16664560
  OsFreePhysicalMemory       : 14646720
  OsTotalVirtualMemorySize   : 19154928
  OsFreeVirtualMemory        : 17197440
  OsInUseVirtualMemory       : 1957488
  OsMaxProcessMemorySize     : 137438953344
  ```

* With `hyperv` isolation, Windows creates a utility VM that is big enough to hold the memory limit, plus the minimal OS needed to host the container. That size is reported as "Total Physical Memory."

  ```powershell
  PS C:\> docker run -it -m 2GB --isolation=hyperv microsoft/nanoserver powershell Get-ComputerInfo *memory*

  CsTotalPhysicalMemory      : 2683355136
  CsPhyicallyInstalledMemory :
  OsTotalVisibleMemorySize   : 2620464
  OsFreePhysicalMemory       : 2306552
  OsTotalVirtualMemorySize   : 2620464
  OsFreeVirtualMemory        : 2356692
  OsInUseVirtualMemory       : 263772
  OsMaxProcessMemorySize     : 137438953344
  ```

### [Configure namespaced kernel parameters (sysctls) at runtime (--sysctl)](#sysctl)

The `--sysctl` sets namespaced kernel parameters (sysctls) in the container. For example, to turn on IP forwarding in the containers network namespace, run this command:

```console
$ docker run --sysctl net.ipv4.ip_forward=1 someimage
```

> Note
>
> Not all sysctls are namespaced. Docker does not support changing sysctls inside of a container that also modify the host system. As the kernel evolves we expect to see more sysctls become namespaced.

#### [Currently supported sysctls](#currently-supported-sysctls)

IPC Namespace:

* `kernel.msgmax`, `kernel.msgmnb`, `kernel.msgmni`, `kernel.sem`, `kernel.shmall`, `kernel.shmmax`, `kernel.shmmni`, `kernel.shm_rmid_forced`.
* Sysctls beginning with `fs.mqueue.*`
* If you use the `--ipc=host` option these sysctls are not allowed.

Network Namespace:

* Sysctls beginning with `net.*`
* If you use the `--network=host` option using these sysctls are not allowed.

----
url: https://docs.docker.com/engine/logging/drivers/fluentd/
----

# Fluentd logging driver

***

Table of contents

***

The `fluentd` logging driver sends container logs to the [Fluentd](https://www.fluentd.org) collector as structured log data. Then, users can use any of the [various output plugins of Fluentd](https://www.fluentd.org/plugins) to write these logs to various destinations.

In addition to the log message itself, the `fluentd` log driver sends the following metadata in the structured log message:

| Field            | Description                                                                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `container_id`   | The full 64-character container ID.                                                                                                                   |
| `container_name` | The container name at the time it was started. If you use `docker rename` to rename a container, the new name isn't reflected in the journal entries. |
| `source`         | `stdout` or `stderr`                                                                                                                                  |
| `log`            | The container log                                                                                                                                     |

## [Usage](#usage)

Some options are supported by specifying `--log-opt` as many times as needed:

* `fluentd-address`: specify a socket address to connect to the Fluentd daemon, ex `fluentdhost:24224` or `unix:///path/to/fluentd.sock`.
* `tag`: specify a tag for Fluentd messages. Supports some Go template markup, ex `{{.ID}}`, `{{.FullID}}` or `{{.Name}}` `docker.{{.ID}}`.

To use the `fluentd` driver as the default logging driver, set the `log-driver` and `log-opt` keys to appropriate values in the `daemon.json` file. For more about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

The following example sets the log driver to `fluentd` and sets the `fluentd-address` option.

```json
{
  "log-driver": "fluentd",
  "log-opts": {
    "fluentd-address": "fluentdhost:24224"
  }
}
```

Restart Docker for the changes to take effect.

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must be provided as strings. Boolean and numeric values (such as the value for `fluentd-async` or `fluentd-max-retries`) must therefore be enclosed in quotes (`"`).

To set the logging driver for a specific container, pass the `--log-driver` option to `docker run`:

```console
$ docker run --log-driver=fluentd ...
```

Before using this logging driver, launch a Fluentd daemon. The logging driver connects to this daemon through `localhost:24224` by default. Use the `fluentd-address` option to connect to a different address.

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
```

If container cannot connect to the Fluentd daemon, the container stops immediately unless the `fluentd-async` option is used.

## [Options](#options)

Users can use the `--log-opt NAME=VALUE` flag to specify additional Fluentd logging driver options.

### [fluentd-address](#fluentd-address)

By default, the logging driver connects to `localhost:24224`. Supply the `fluentd-address` option to connect to a different address. `tcp`(default) and `unix` sockets are supported.

```console
$ docker run --log-driver=fluentd --log-opt fluentd-address=fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=tcp://fluentdhost:24224
$ docker run --log-driver=fluentd --log-opt fluentd-address=unix:///path/to/fluentd.sock
```

Two of the above specify the same address, because `tcp` is default.

### [tag](#tag)

By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the [log tag option documentation](https://docs.docker.com/engine/logging/log_tags/) for customizing the log tag format.

### [labels, labels-regex, env, and env-regex](#labels-labels-regex-env-and-env-regex)

The `labels` and `env` options each take a comma-separated list of keys. If there is collision between `label` and `env` keys, the value of the `env` takes precedence. Both options add additional fields to the extra attributes of a logging message.

The `env-regex` and `labels-regex` options are similar to and compatible with respectively `env` and `labels`. Their values are regular expressions to match logging-related environment variables and labels. It is used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).

### [fluentd-async](#fluentd-async)

Docker connects to Fluentd in the background. Messages are buffered until the connection is established. Defaults to `false`.

### [fluentd-async-reconnect-interval](#fluentd-async-reconnect-interval)

When `fluentd-async` is enabled, the `fluentd-async-reconnect-interval` option defines the interval, in milliseconds, at which the connection to `fluentd-address` is re-established. This option is useful if the address resolves to one or more IP addresses, for example a Consul service address.

### [fluentd-buffer-limit](#fluentd-buffer-limit)

Sets the number of events buffered on the memory. Records will be stored in memory up to this number. If the buffer is full, the call to record logs will fail. The default is 1048576. (<https://github.com/fluent/fluent-logger-golang/tree/master#bufferlimit>)

### [fluentd-retry-wait](#fluentd-retry-wait)

How long to wait between retries. Defaults to 1 second.

### [fluentd-max-retries](#fluentd-max-retries)

The maximum number of retries. Defaults to `4294967295` (2\*\*32 - 1).

### [fluentd-sub-second-precision](#fluentd-sub-second-precision)

Generates event logs in nanosecond resolution. Defaults to `false`.

### [fluentd-write-timeout](#fluentd-write-timeout)

Sets the timeout for the write call to the `fluentd` daemon. By default, writes have no timeout and will block indefinitely.

## [Fluentd daemon management with Docker](#fluentd-daemon-management-with-docker)

About `Fluentd` itself, see [the project webpage](https://www.fluentd.org) and [its documents](https://docs.fluentd.org).

To use this logging driver, start the `fluentd` daemon on a host. We recommend that you use [the Fluentd docker image](https://hub.docker.com/r/fluent/fluentd/). This image is especially useful if you want to aggregate multiple container logs on each host then, later, transfer the logs to another Fluentd node to create an aggregate store.

### [Test container loggers](#test-container-loggers)

1. Write a configuration file (`test.conf`) to dump input logs:

   ```text
   <source>
     @type forward
   </source>

   <match *>
     @type stdout
   </match>
   ```

2. Launch Fluentd container with this configuration file:

   ```console
   $ docker run -it -p 24224:24224 -v /path/to/conf/test.conf:/fluentd/etc/test.conf -e FLUENTD_CONF=test.conf fluent/fluentd:latest
   ```

3. Start one or more containers with the `fluentd` logging driver:

   ```console
   $ docker run --log-driver=fluentd your/application
   ```

----
url: https://docs.docker.com/reference/cli/docker/scout/repo/list/
----

# docker scout repo list

***

| Description | List Docker Scout repositories |
| ----------- | ------------------------------ |
| Usage       | `docker scout repo list`       |

## [Description](#description)

The docker scout repo list command shows all repositories in an organization.

If ORG is not provided the default configured organization will be used.

## [Options](#options)

| Option            | Default | Description                                                          |
| ----------------- | ------- | -------------------------------------------------------------------- |
| `--filter`        |         | Regular expression to filter repositories by name                    |
| `--only-disabled` |         | Filter to disabled repositories only                                 |
| `--only-enabled`  |         | Filter to enabled repositories only                                  |
| `--only-registry` |         | Filter to a specific registry only: - hub.docker.com - ecr (AWS ECR) |
| `--org`           |         | Namespace of the Docker organization                                 |

----
url: https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/write-tests/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Write tests with Testcontainers

***

Table of contents

***

To test the secured API endpoints, you need a running Keycloak instance and a PostgreSQL database, plus a started Spring context. Testcontainers spins up both services in Docker containers and connects them to Spring through dynamic property registration.

## [Configure the test containers](#configure-the-test-containers)

Spring Boot's Testcontainers support lets you declare containers as beans. For Keycloak, `@ServiceConnection` isn't available, but you can use `DynamicPropertyRegistry` to set the JWT issuer URI dynamically.

Create `ContainersConfig.java` under `src/test/java`:

```java
package com.testcontainers.products;

import dasniko.testcontainers.keycloak.KeycloakContainer;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.boot.testcontainers.service.connection.ServiceConnection;
import org.springframework.context.annotation.Bean;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.testcontainers.postgresql.PostgreSQLContainer;

@TestConfiguration(proxyBeanMethods = false)
public class ContainersConfig {

  static String POSTGRES_IMAGE = "postgres:16-alpine";
  static String KEYCLOAK_IMAGE = "quay.io/keycloak/keycloak:25.0";
  static String realmImportFile = "/keycloaktcdemo-realm.json";
  static String realmName = "keycloaktcdemo";

  @Bean
  @ServiceConnection
  PostgreSQLContainer postgres() {
    return new PostgreSQLContainer(POSTGRES_IMAGE);
  }

  @Bean
  KeycloakContainer keycloak(DynamicPropertyRegistry registry) {
    var keycloak = new KeycloakContainer(KEYCLOAK_IMAGE)
      .withRealmImportFile(realmImportFile);
    registry.add(
      "spring.security.oauth2.resourceserver.jwt.issuer-uri",
      () -> keycloak.getAuthServerUrl() + "/realms/" + realmName
    );
    return keycloak;
  }
}
```

This configuration:

* Declares a `PostgreSQLContainer` bean with `@ServiceConnection`, which starts a PostgreSQL container and automatically registers the datasource properties.
* Declares a `KeycloakContainer` bean using the `quay.io/keycloak/keycloak:25.0` image, imports the realm configuration file, and dynamically registers the JWT issuer URI from the Keycloak container's auth server URL.

## [Write the test](#write-the-test)

Create `ProductControllerTests.java`:

```java
package com.testcontainers.products.api;

import static io.restassured.RestAssured.given;
import static io.restassured.RestAssured.when;
import static java.util.Collections.singletonList;
import static org.springframework.boot.test.context.SpringBootTest.WebEnvironment.RANDOM_PORT;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.testcontainers.products.ContainersConfig;
import io.restassured.RestAssured;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.autoconfigure.security.oauth2.resource.OAuth2ResourceServerProperties;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.context.annotation.Import;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

@SpringBootTest(webEnvironment = RANDOM_PORT)
@Import(ContainersConfig.class)
class ProductControllerTests {

  static final String GRANT_TYPE_CLIENT_CREDENTIALS = "client_credentials";
  static final String CLIENT_ID = "product-service";
  static final String CLIENT_SECRET = "jTJJqdzeCSt3DmypfHZa42vX8U9rQKZ9";

  @LocalServerPort
  private int port;

  @Autowired
  OAuth2ResourceServerProperties oAuth2ResourceServerProperties;

  @BeforeEach
  void setup() {
    RestAssured.port = port;
  }

  @Test
  void shouldGetProductsWithoutAuthToken() {
    when().get("/api/products").then().statusCode(200);
  }

  @Test
  void shouldGetUnauthorizedWhenCreateProductWithoutAuthToken() {
    given()
      .contentType("application/json")
      .body(
        """
            {
                "title": "New Product",
                "description": "Brand New Product"
            }
        """
      )
      .when()
      .post("/api/products")
      .then()
      .statusCode(401);
  }

  @Test
  void shouldCreateProductWithAuthToken() {
    String token = getToken();

    given()
      .header("Authorization", "Bearer " + token)
      .contentType("application/json")
      .body(
        """
            {
                "title": "New Product",
                "description": "Brand New Product"
            }
        """
      )
      .when()
      .post("/api/products")
      .then()
      .statusCode(201);
  }

  private String getToken() {
    RestTemplate restTemplate = new RestTemplate();
    HttpHeaders httpHeaders = new HttpHeaders();
    httpHeaders.setContentType(MediaType.APPLICATION_FORM_URLENCODED);

    MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
    map.put("grant_type", singletonList(GRANT_TYPE_CLIENT_CREDENTIALS));
    map.put("client_id", singletonList(CLIENT_ID));
    map.put("client_secret", singletonList(CLIENT_SECRET));

    String authServerUrl =
      oAuth2ResourceServerProperties.getJwt().getIssuerUri() +
      "/protocol/openid-connect/token";

    var request = new HttpEntity<>(map, httpHeaders);
    KeyCloakToken token = restTemplate.postForObject(
      authServerUrl,
      request,
      KeyCloakToken.class
    );

    assert token != null;
    return token.accessToken();
  }

  record KeyCloakToken(@JsonProperty("access_token") String accessToken) {}
}
```

Here's what the tests cover:

* `shouldGetProductsWithoutAuthToken()` invokes `GET /api/products` without an `Authorization` header. Because this endpoint is configured to permit unauthenticated access, the response status code is 200.
* `shouldGetUnauthorizedWhenCreateProductWithoutAuthToken()` invokes the secured `POST /api/products` endpoint without an `Authorization` header and asserts the response status code is 401 (Unauthorized).
* `shouldCreateProductWithAuthToken()` first obtains an `access_token` using the Client Credentials flow. It then includes the token as a Bearer token in the `Authorization` header when invoking `POST /api/products` and asserts the response status code is 201 (Created).

The `getToken()` helper method requests an access token from the Keycloak token endpoint using the client ID and client secret that were configured in the exported realm.

## [Use Testcontainers for local development](#use-testcontainers-for-local-development)

Spring Boot's Testcontainers support also works for local development. Create `TestApplication.java` under `src/test/java`:

```java
package com.testcontainers.products;

import org.springframework.boot.SpringApplication;

public class TestApplication {

  public static void main(String[] args) {
    SpringApplication
      .from(Application::main)
      .with(ContainersConfig.class)
      .run(args);
  }
}
```

Run `TestApplication.java` from your IDE instead of the main `Application.java`. It starts the containers defined in `ContainersConfig` and configures the application to use the dynamically registered properties, so you don't have to install or configure PostgreSQL and Keycloak manually.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/run-tests/)

----
url: https://docs.docker.com/guides/admin-set-up/deploy/
----

# Deploy your Docker setup

***

Table of contents

***

> Warning
>
> Communicate with your users before proceeding, and confirm that your IT and MDM teams are prepared to handle any unexpected issues, as these steps will affect all existing users signing into your Docker organization.

## [Enforce SSO](#enforce-sso)

Enforcing SSO means that anyone who has a Docker profile with an email address that matches your verified domain must sign in using your SSO connection. Make sure the Identity provider groups associated with your SSO connection cover all the developer groups that you want to have access to the Docker subscription.

For instructions on how to enforce SSO, see [Enforce SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/).

## [Deploy configuration settings and enforce sign-in to users](#deploy-configuration-settings-and-enforce-sign-in-to-users)

Have the MDM team deploy the configuration files for Docker to all users.

## [Next steps](#next-steps)

Congratulations, you've successfully completed the admin implementation process for Docker.

To continue optimizing your Docker environment:

* Review your [organization's usage data](https://docs.docker.com/admin/insights/) to track adoption
* Monitor [Docker Scout findings](https://docs.docker.com/scout/explore/analysis/) for security insights
* Explore [additional security features](https://docs.docker.com/enterprise/security/) to enhance your configuration

----
url: https://docs.docker.com/reference/cli/docker/desktop/disable/model-runner/
----

# docker desktop disable model-runner

***

| Description | Disable Docker Model Runner           |
| ----------- | ------------------------------------- |
| Usage       | `docker desktop disable model-runner` |

## [Description](#description)

Disable Docker Model Runner

----
url: https://docs.docker.com/reference/cli/docker/image/push/
----

# docker image push

***

| Description                                                               | Upload an image to a registry            |
| ------------------------------------------------------------------------- | ---------------------------------------- |
| Usage                                                                     | `docker image push [OPTIONS] NAME[:TAG]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker push`                            |

## [Description](#description)

Use `docker image push` to share your images to the [Docker Hub](https://hub.docker.com) registry or to a self-hosted one.

Refer to the [`docker image tag`](/reference/cli/docker/image/tag/) reference for more information about valid image and tag names.

Killing the `docker image push` process, for example by pressing `CTRL-c` while it is running in a terminal, terminates the push operation.

Progress bars are shown during docker push, which show the uncompressed size. The actual amount of data that's pushed will be compressed before sending, so the uploaded size will not be reflected by the progress bar.

Registry credentials are managed by [docker login](/reference/cli/docker/login/).

### [Concurrent uploads](#concurrent-uploads)

By default the Docker daemon will push five layers of an image at a time. If you are on a low bandwidth connection this may cause timeout issues and you may want to lower this via the `--max-concurrent-uploads` daemon option. See the [daemon documentation](/reference/cli/dockerd/) for more details.

## [Options](#options)

| Option                        | Default | Description                                                                                                                                                                                                                                                |
| ----------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-a, --all-tags`](#all-tags) |         | Push all tags of an image to the repository                                                                                                                                                                                                                |
| `--platform`                  |         | API 1.46+ Push a platform-specific manifest as a single-platform image to the registry. Image index won't be pushed, meaning that other manifests, including attestations won't be preserved. 'os\[/arch\[/variant]]': Explicit platform (eg. linux/amd64) |
| `-q, --quiet`                 |         | Suppress verbose output                                                                                                                                                                                                                                    |

## [Examples](#examples)

### [Push a new image to a registry](#push-a-new-image-to-a-registry)

First save the new image by finding the container ID (using [`docker container ls`](/reference/cli/docker/container/ls/)) and then committing it to a new image name. Note that only `a-z0-9-_.` are allowed when naming images:

```console
$ docker container commit c16378f943fe rhel-httpd:latest
```

Now, push the image to the registry using the image ID. In this example the registry is on host named `registry-host` and listening on port `5000`. To do this, tag the image with the host name or IP address, and the port of the registry:

```console
$ docker image tag rhel-httpd:latest registry-host:5000/myadmin/rhel-httpd:latest

$ docker image push registry-host:5000/myadmin/rhel-httpd:latest
```

Check that this worked by running:

```console
$ docker image ls
```

You should see both `rhel-httpd` and `registry-host:5000/myadmin/rhel-httpd` listed.

### [Push all tags of an image (-a, --all-tags)](#all-tags)

Use the `-a` (or `--all-tags`) option to push all tags of a local image.

The following example creates multiple tags for an image, and pushes all those tags to Docker Hub.

```console
$ docker image tag myimage registry-host:5000/myname/myimage:latest
$ docker image tag myimage registry-host:5000/myname/myimage:v1.0.1
$ docker image tag myimage registry-host:5000/myname/myimage:v1.0
$ docker image tag myimage registry-host:5000/myname/myimage:v1
```

The image is now tagged under multiple names:

```console
$ docker image ls

REPOSITORY                          TAG        IMAGE ID       CREATED      SIZE
myimage                             latest     6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   latest     6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   v1         6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   v1.0       6d5fcfe5ff17   2 hours ago  1.22MB
registry-host:5000/myname/myimage   v1.0.1     6d5fcfe5ff17   2 hours ago  1.22MB
```

When pushing with the `--all-tags` option, all tags of the `registry-host:5000/myname/myimage` image are pushed:

```console
$ docker image push --all-tags registry-host:5000/myname/myimage

The push refers to repository [registry-host:5000/myname/myimage]
195be5f8be1d: Pushed
latest: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
195be5f8be1d: Layer already exists
v1: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
195be5f8be1d: Layer already exists
v1.0: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
195be5f8be1d: Layer already exists
v1.0.1: digest: sha256:edafc0a0fb057813850d1ba44014914ca02d671ae247107ca70c94db686e7de6 size: 4527
```

----
url: https://docs.docker.com/extensions/extensions-sdk/
----

# Overview of the Extensions SDK

***

***

> Important
>
> New submissions to the Docker Extensions Marketplace are paused while Docker reviews Marketplace security. You can still update existing extensions, and private Marketplace extensions are unaffected. Contact <extensions@docker.com> if you have additional questions.

The resources in this section help you create your own Docker extension.

The Docker CLI tool provides a set of commands to help you build and publish your extension, packaged as a specially formatted Docker image.

At the root of the image filesystem is a `metadata.json` file which describes the content of the extension. It's a fundamental element of a Docker extension.

An extension can contain a UI part and backend parts that run either on the host or in the Desktop virtual machine. For further information, see [Architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).

You distribute extensions through Docker Hub. However, you can develop them locally without the need to push the extension to Docker Hub. See [Extensions distribution](https://docs.docker.com/extensions/extensions-sdk/extensions/DISTRIBUTION/) for further details.

> Already built an extension?
>
> Let us know about your experience using the [feedback form](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form).

### [The build and publish process](/extensions/extensions-sdk/process/)

[Understand the process for building and publishing an extension.](/extensions/extensions-sdk/process/)

### [Quickstart guide](/extensions/extensions-sdk/quickstart/)

[Follow the quickstart guide to create a basic Docker extension quickly.](/extensions/extensions-sdk/quickstart/)

### [View the design guidelines](/extensions/extensions-sdk/design/design-guidelines/)

[Ensure your extension aligns to Docker's design guidelines and principles.](/extensions/extensions-sdk/design/design-guidelines/)

### [Publish your extension](/extensions/extensions-sdk/extensions/)

[Understand how to publish your extension to the Marketplace.](/extensions/extensions-sdk/extensions/)

### [Interacting with Kubernetes](/extensions/extensions-sdk/guides/kubernetes/)

[Find information on how to interact indirectly with a Kubernetes cluster from your Docker extension.](/extensions/extensions-sdk/guides/kubernetes/)

### [Multi-arch extensions](/extensions/extensions-sdk/extensions/multi-arch/)

[Build your extension for multiple architectures.](/extensions/extensions-sdk/extensions/multi-arch/)

----
url: https://docs.docker.com/scout/policy/ci/
----

# Evaluate policy compliance in CI

***

Table of contents

***

Adding Policy Evaluation to your continuous integration pipelines helps you detect and prevent cases where code changes would cause policy compliance to become worse compared to your baseline.

The recommended strategy for Policy Evaluation in a CI setting involves evaluating a local image and comparing the results to a baseline. If the policy compliance for the local image is worse than the specified baseline, the CI run fails with an error. If policy compliance is better or unchanged, the CI run succeeds.

This comparison is relative, meaning that it's only concerned with whether your CI image is better or worse than your baseline. It's not an absolute check to pass or fail all policies. By measuring relative to a baseline that you define, you can quickly see if a change has a positive or negative impact on policy compliance.

## [How it works](#how-it-works)

When you do Policy Evaluation in CI, you run a local policy evaluation on the image you build in your CI pipeline. To run a local evaluation, the image that you evaluate must exist in the image store where your CI workflow is being run. Either build or pull the image, and then run the evaluation.

To run policy evaluation and trigger failure if compliance for your local image is worse than your comparison baseline, you need to specify the image version to use as a baseline. You can hard-code a specific image reference, but a better solution is to use [environments](https://docs.docker.com/scout/integrations/environment/) to automatically infer the image version from an environment. The example that follows uses environments to compare the CI image with the image in the `production` environment.

## [Example](#example)

The following example on how to run policy evaluation in CI uses the [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout) to execute the `compare` command on an image built in CI. The compare command has a `to-env` input, which will run the comparison against an environment called `production`. The `exit-on` input is set to `policy`, meaning that the comparison fails only if policy compliance has worsened.

This example doesn't assume that you're using Docker Hub as your container registry. As a result, this workflow uses the `docker/login-action` twice:

* Once for authenticating to your container registry.
* Once more for authenticating to Docker to pull the analysis results of your `production` image.

If you use Docker Hub as your container registry, you only need to authenticate once.

> Note
>
> Due to a limitation in the Docker Engine, loading multi-platform images or images with attestations to the image store isn't supported.
>
> For the policy evaluation to work, you must load the image to the local image store of the runner. Ensure that you're building a single-platform image without attestations, and that you're loading the build results. Otherwise, the policy evaluation fails.

Also note the `pull-requests: write` permission for the job. The Docker Scout GitHub Action adds a pull request comment with the evaluation results by default, which requires this permission. For details, see [Pull Request Comments](https://github.com/docker/scout-action#pull-request-comments).

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
  REGISTRY: docker.io
  IMAGE_NAME: IMAGE_NAME
  DOCKER_ORG: ORG

jobs:
  build:
    permissions:
      pull-requests: write

    runs-on: ubuntu-latest
    steps:
      - name: Log into registry ${{ env.REGISTRY }}
        uses: docker/login-action@v4
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ secrets.REGISTRY_USER }}
          password: ${{ secrets.REGISTRY_TOKEN }}
      
      - name: Setup Docker buildx
        uses: docker/setup-buildx-action@v4

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v6
        with:
          images: ${{ env.IMAGE_NAME }}

      - name: Build image
        id: build-and-push
        uses: docker/build-push-action@v7
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          sbom: ${{ github.event_name != 'pull_request' }}
          provenance: ${{ github.event_name != 'pull_request' }}
          push: ${{ github.event_name != 'pull_request' }}
          load: ${{ github.event_name == 'pull_request' }}

      - name: Authenticate with Docker
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKER_USER }}
          password: ${{ secrets.DOCKER_PAT }}

      - name: Compare
        if: ${{ github.event_name == 'pull_request' }}
        uses: docker/scout-action@v1
        with:
          command: compare
          image: ${{ steps.meta.outputs.tags }}
          to-env: production
          platform: "linux/amd64"
          ignore-unchanged: true
          only-severities: critical,high
          organization: ${{ env.DOCKER_ORG }}
          exit-on: policy
```

The following screenshot shows what the GitHub PR comment looks like when a policy evaluation check fails because policy has become worse in the PR image compared to baseline.

This example has demonstrated how to run policy evaluation in CI with GitHub Actions. Docker Scout also supports other CI platforms. For more information, see [Docker Scout CI integrations](https://docs.docker.com/scout/integrations/#continuous-integration).

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/config/
----

# Configure Docker socket exceptions and advanced settings

***

Table of contents

***

Subscription: Business

For: Administrators

This page shows you how to configure Docker socket exceptions and other advanced settings for Enhanced Container Isolation (ECI). These configurations enable trusted tools like Testcontainers to work with ECI while maintaining security.

## [Docker socket mount permissions](#docker-socket-mount-permissions)

By default, Enhanced Container Isolation blocks containers from mounting the Docker socket to prevent malicious access to Docker Engine. However, some tools require Docker socket access.

Common scenarios requiring Docker socket access include:

* Testing frameworks: Testcontainers, which manages test containers
* Build tools: Paketo buildpacks that create ephemeral build containers
* CI/CD tools: Tools that manage containers as part of deployment pipelines
* Development utilities: Docker CLI containers for container management

## [Configure socket exceptions](#configure-socket-exceptions)

Configure Docker socket exceptions using Settings Management:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.
2. Go to **Admin Console** > **Desktop Settings Management**.
3. [Create or edit a setting policy](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/).
4. Find **Enhanced Container Isolation** settings.
5. Configure **Docker socket access control** with your trusted images and command restrictions.

Create an [`admin-settings.json` file](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/) and add:

```json
{
  "configurationFileVersion": 2,
  "enhancedContainerIsolation": {
    "locked": true,
    "value": true,
    "dockerSocketMount": {
      "imageList": {
        "images": [
          "docker.io/localstack/localstack:*",
          "docker.io/testcontainers/ryuk:*",
          "docker:cli"
        ],
        "allowDerivedImages": true
      },
      "commandList": {
        "type": "deny",
        "commands": ["push", "build"]
      }
    }
  }
}
```

## [Image allowlist configuration](#image-allowlist-configuration)

The `imageList` defines which container images can mount the Docker socket.

### [Image reference formats](#image-reference-formats)

| Format                  | Description                                                                                                                                                                                     |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<image_name>[:<tag>]`  | Name of the image, with optional tag. If the tag is omitted, the `:latest` tag is used. If the tag is the wildcard `*`, then it means "any tag for that image."                                 |
| `<image_name>@<digest>` | Name of the image, with a specific repository digest (e.g., as reported by `docker buildx imagetools inspect <image>`). This means only the image that matches that name and digest is allowed. |

### [Example configurations](#example-configurations)

Basic allowlist for testing tools:

```json
"imageList": {
  "images": [
    "docker.io/testcontainers/ryuk:*",
    "docker:cli",
    "alpine:latest"
  ]
}
```

Wildcard allowlist (Docker Desktop 4.36 and later):

```json
"imageList": {
  "images": ["*"]
}
```

> Warning
>
> Using `"*"` allows all containers to mount the Docker socket, which reduces security. Only use this when explicitly listing allowed images isn't feasible.

### [Security validation](#security-validation)

Docker Desktop validates allowed images by:

1. Downloading image digests from registries for allowed images
2. Comparing container image digests against the allowlist when containers start
3. Blocking containers whose digests don't match allowed images

This prevents bypassing restrictions by re-tagging unauthorized images:

```console
$ docker tag malicious-image docker:cli
$ docker run -v /var/run/docker.sock:/var/run/docker.sock docker:cli
# This fails because the digest doesn't match the real docker:cli image
```

## [Derived images support](#derived-images-support)

For tools like Paketo buildpacks that create ephemeral local images, you can allow images derived from trusted base images.

### [Enable derived images](#enable-derived-images)

```json
"imageList": {
  "images": [
    "paketobuildpacks/builder:base"
  ],
  "allowDerivedImages": true
}
```

When `allowDerivedImages` is true, local images built from allowed base images (using `FROM` in Dockerfile) also gain Docker socket access.

### [Derived images requirements](#derived-images-requirements)

* Local images only: Derived images must not exist in remote registries
* Base image available: The parent image must be pulled locally first
* Performance impact: Adds up to 1 second to container startup for validation
* Version compatibility: Full wildcard support requires Docker Desktop 4.36+

## [Command restrictions](#command-restrictions)

### [Deny list (recommended)](#deny-list-recommended)

Blocks specified commands while allowing all others:

```json
"commandList": {
  "type": "deny",
  "commands": ["push", "build", "image*"]
}
```

### [Allow list](#allow-list)

Only allows specified commands while blocking all others:

```json
"commandList": {
  "type": "allow",
  "commands": ["ps", "container*", "volume*"]
}
```

### [Command wildcards](#command-wildcards)

| Wildcard        | Blocks/allows                       |
| --------------- | ----------------------------------- |
| `"container\*"` | All "docker container ..." commands |
| `"image\*"`     | All "docker image ..." commands     |
| `"volume\*"`    | All "docker volume ..." commands    |
| `"network\*"`   | All "docker network ..." commands   |
| `"build\*"`     | All "docker build ..." commands     |
| `"system\*"`    | All "docker system ..." commands    |

### [Command blocking example](#command-blocking-example)

When a blocked command is executed:

```console
/ # docker push myimage
Error response from daemon: enhanced container isolation: docker command "/v1.43/images/myimage/push?tag=latest" is blocked; if you wish to allow it, configure the docker socket command list in the Docker Desktop settings.
```

## [Common configuration examples](#common-configuration-examples)

### [Testcontainers setup](#testcontainers-setup)

For Java/Python testing with Testcontainers:

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker.io/testcontainers/ryuk:*",
      "testcontainers/*:*"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["push", "build"]
  }
}
```

### [CI/CD pipeline tools](#cicd-pipeline-tools)

For controlled CI/CD container management:

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:cli",
      "your-registry.com/ci-tools/*:*"
    ]
  },
  "commandList": {
    "type": "allow",
    "commands": ["ps", "container*", "image*"]
  }
}
```

### [Development environments](#development-environments)

For local development with Docker-in-Docker:

```json
"dockerSocketMount": {
  "imageList": {
    "images": [
      "docker:dind",
      "docker:cli"
    ]
  },
  "commandList": {
    "type": "deny",
    "commands": ["system*"]
  }
}
```

## [Security recommendations](#security-recommendations)

### [Image allowlist best practices](#image-allowlist-best-practices)

* Be restrictive: Only allow images you absolutely trust and need
* Use wildcards carefully: Tag wildcards (`*`) are convenient but less secure than specific tags
* Regular reviews: Periodically review and update your allowlist
* Digest pinning: Use digest references for maximum security in critical environments

### [Command restrictions](#command-restrictions-1)

* Default to deny: Start with a deny list blocking dangerous commands like `push` and `build`
* Principle of least privilege: Only allow commands your tools actually need
* Monitor usage: Track which commands are being blocked to refine your configuration

### [Monitoring and maintenance](#monitoring-and-maintenance)

* Regular validation: Test your configuration after Docker Desktop updates, as image digests may change.
* Handle digest mismatches: If allowed images are unexpectedly blocked:
  ```console
  $ docker image rm <image>
  $ docker pull <image>
  ```

This resolves digest mismatches when upstream images are updated.

## [Next steps](#next-steps)

* Review [Enhanced Container Isolation limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).
* Review [Enhanced Container Isolation FAQs](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/faq/).

----
url: https://docs.docker.com/reference/cli/docker/compose/commit/
----

# docker compose commit

***

| Description | Create a new image from a service container's changes        |
| ----------- | ------------------------------------------------------------ |
| Usage       | `docker compose commit [OPTIONS] SERVICE [REPOSITORY[:TAG]]` |

## [Description](#description)

Create a new image from a service container's changes

## [Options](#options)

| Option          | Default | Description                                                |
| --------------- | ------- | ---------------------------------------------------------- |
| `-a, --author`  |         | Author (e.g., "John Hannibal Smith <hannibal@a-team.com>") |
| `-c, --change`  |         | Apply Dockerfile instruction to the created image          |
| `--index`       |         | index of the container if service has multiple replicas.   |
| `-m, --message` |         | Commit message                                             |
| `-p, --pause`   | `true`  | Pause container during commit                              |

----
url: https://docs.docker.com/dhi/explore/malware-scanning/
----

# Malware scanning

***

Table of contents

***

The Docker Hardened Image (DHI) pipeline scans for viruses and malware as part of the build process. The scan results are embedded as a signed attestation, which you can independently retrieve and verify.

## [How it works](#how-it-works)

Docker uses [ClamAV](https://www.clamav.net/), an open source antivirus engine, to scan every layer of each image. The scan runs automatically during the build process and checks all files in the image, including files inside archives, for known viruses and malware signatures.

The scan results are published as a signed attestation attached to the image. The attestation includes the full ClamAV scan report, including the number of files scanned, the virus signature database version, and whether any infected files were detected.

## [View the malware scan attestation](#view-the-malware-scan-attestation)

You can retrieve the malware scan attestation using the Docker Scout CLI.

1. Use the `docker scout attest get` command with the virus scan predicate type:

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/virus/v0.1 \
     --predicate \
     dhi.io/<image>:<tag>
   ```

   > Note
   >
   > If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use `registry://dhi.io/python` instead of `dhi.io/python`.

   For example:

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/virus/v0.1 \
     --predicate \
     dhi.io/python:3.13
   ```

   The output is a JSON object containing the scanner used and the base64-encoded scan report:

   ```json
   {
     "scanner": {
       "report": "<base64-encoded ClamAV report>",
       "uri": "clamav/clamav:stable"
     }
   }
   ```

   Decoding the report shows the full ClamAV output, ending with a scan summary:

   ```text
   ----------- SCAN SUMMARY -----------
   Known viruses: 3627833
   Engine version: 1.5.2
   Scanned directories: 4
   Scanned files: 21
   Infected files: 0
   Data scanned: 44.90 MiB
   Data read: 23.88 MiB (ratio 1.88:1)
   Time: 11.473 sec (0 m 11 s)
   Start Date: 2026:04:12 02:36:19
   End Date:   2026:04:12 02:36:30
   ```

2. Verify the attestation signature. To ensure the attestation is authentic and signed by Docker, run:

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/virus/v0.1 \
     --verify \
     dhi.io/<image>:<tag> --platform <platform>
   ```

   If the attestation is valid, Docker Scout confirms the signature and shows the matching `cosign verify` command.

To view other attestations, such as SBOMs or test results, see [Verify an image](https://docs.docker.com/dhi/how-to/verify/).

----
url: https://docs.docker.com/engine/release-notes/20.10/
----

# Docker Engine 20.10 release notes

***

Table of contents

***

This document describes the latest changes, additions, known issues, and fixes for Docker Engine version 20.10.

## [20.10.24](#201024)

*2023-04-04*

### [Updates](#updates)

* Update Go runtime to [1.19.7](https://go.dev/doc/devel/release#go1.19.minor).
* Update Docker Buildx to [v0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4).
* Update containerd to [v1.6.20](https://github.com/containerd/containerd/releases/tag/v1.6.20).
* Update runc to [v1.1.5](https://github.com/opencontainers/runc/releases/tag/v1.1.5).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements)

* Fixed a number of issues that can cause Swarm encrypted overlay networks to fail to uphold their guarantees, addressing [CVE-2023-28841](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28841), [CVE-2023-28840](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28840), and [CVE-2023-28842](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-28842).

  * A lack of kernel support for encrypted overlay networks now reports as an error.
  * Encrypted overlay networks are eagerly set up, rather than waiting for multiple nodes to attach.
  * Encrypted overlay networks are now usable on Red Hat Enterprise Linux 9 through the use of the `xt_bpf` kernel module.
  * Users of Swarm overlay networks should review [GHSA-vwm3-crmr-xfxw](https://github.com/moby/moby/security/advisories/GHSA-vwm3-crmr-xfxw) to ensure that unintentional exposure has not occurred.

* Upgrade github.com/containerd/fifo to v1.1.0 to fix a potential panic [moby/moby#45216](https://github.com/moby/moby/pull/45242).

* Fix missing Bash completion for installed cli-plugins [docker/cli#4091](https://github.com/docker/cli/pull/4091).

## [20.10.23](#201023)

*2023-01-19*

This release of Docker Engine contains updated versions of Docker Compose, Docker Buildx, containerd, and some minor bug fixes and enhancements.

### [Updates](#updates-1)

* Update Docker Compose to [v2.15.1](https://github.com/docker/compose/releases/tag/v2.15.1).
* Update Docker Buildx to [v0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0).
* Update containerd (`containerd.io` package) to [v1.6.15](https://github.com/containerd/containerd/releases/tag/v1.6.15).
* Update the package versioning format for `docker-compose-cli` to allow distribution version updates [docker/docker-ce-packaging#822](https://github.com/docker/docker-ce-packaging/pull/822).
* Update Go runtime to [1.18.10](https://go.dev/doc/devel/release#go1.18.minor),

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-1)

* Fix an issue where `docker build` would fail when using `--add-host=host.docker.internal:host-gateway` with BuildKit enabled [moby/moby#44650](https://github.com/moby/moby/pull/44650).

* Revert seccomp: block socket calls to `AF_VSOCK` in default profile [moby/moby#44712](https://github.com/moby/moby/pull/44712).

  This change, while favorable from a security standpoint, caused a change in behavior for some use-cases. As such, we are reverting it to ensure stability and compatibility for the affected users.

  However, users of `AF_VSOCK` in containers should recognize that this (special) address family is not currently namespaced in any version of the Linux kernel, and may result in unexpected behavior, like containers communicating directly with host hypervisors.

  Future releases, will filter `AF_VSOCK`. Users who need to allow containers to communicate over the unnamespaced `AF_VSOCK` will need to turn off seccomp confinement or set a custom seccomp profile.

## [20.10.22](#201022)

*2022-12-16*

This release of Docker Engine contains updated versions of Docker Compose, Docker Scan, containerd, and some minor bug fixes and enhancements.

### [Updates](#updates-2)

* Update Docker Compose to [v2.14.1](https://github.com/docker/compose/releases/tag/v2.14.1).
* Update Docker Scan to [v0.23.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.23.0).
* Update containerd (`containerd.io` package) to [v1.6.13](https://github.com/containerd/containerd/releases/tag/v1.6.13), to include a fix for [CVE-2022-23471](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-23471).
* Update Go runtime to [1.18.9](https://go.dev/doc/devel/release#go1.18.minor), to include fixes for [CVE-2022-41716](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41716), [CVE-2022-41717](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41717), and [CVE-2022-41720](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41720).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-2)

* Improve error message when attempting to pull an unsupported image format or OCI artifact [moby/moby#44413](https://github.com/moby/moby/pull/44413), [moby/moby#44569](https://github.com/moby/moby/pull/44569).
* Fix an issue where the host's ephemeral port-range was ignored when selecting random ports for containers [moby/moby#44476](https://github.com/moby/moby/pull/44476).
* Fix `ssh: parse error in message type 27` errors during `docker build` on hosts using OpenSSH 8.9 or above [moby/moby#3862](https://github.com/moby/moby/pull/3862).
* seccomp: block socket calls to `AF_VSOCK` in default profile [moby/moby#44564](https://github.com/moby/moby/pull/44564).

## [20.10.21](#201021)

*2022-10-25*

This release of Docker Engine contains updated versions of Docker Compose, Docker Scan, containerd, added packages for Ubuntu 22.10, and some minor bug fixes and enhancements.

### [New](#new)

* Provide packages for Ubuntu 22.10 (Kinetic Kudu).
* Add support for `allow-nondistributable-artifacts` towards Docker Hub [moby/moby#44313](https://github.com/moby/moby/pull/44313).

### [Updates](#updates-3)

* Update Docker Compose to [v2.12.2](https://github.com/docker/compose/releases/tag/v2.12.2).
* Update Docker Scan to [v0.21.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.21.0).
* Update containerd (`containerd.io` package) to [v1.6.9](https://github.com/containerd/containerd/releases/tag/v1.6.9).
* Update bundled BuildKit version to fix `output clipped, log limit 1MiB reached` errors [moby/moby#44339](https://github.com/moby/moby/pull/44339).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-3)

* Remove experimental gate for `--platform` in bash completion [docker/cli#3824](https://github.com/docker/cli/pull/3824).
* Fix an `Invalid standard handle identifier` panic when registering the Docker Engine as a service from a legacy CLI on Windows [moby/moby#44326](https://github.com/moby/moby/pull/44326).
* Fix running Git commands in Cygwin on Windows [moby/moby#44332](https://github.com/moby/moby/pull/44332).

## [20.10.20](#201020)

*2022-10-18*

This release of Docker Engine contains partial mitigations for a Git vulnerability ([CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253)), and has updated handling of `image:tag@digest` image references.

The Git vulnerability allows a maliciously crafted Git repository, when used as a build context, to copy arbitrary filesystem paths into resulting containers/images; this can occur in both the daemon, and in API clients, depending on the versions and tools in use.

The mitigations available in this release and in other consumers of the daemon API are partial and only protect users who build a Git URL context (e.g. `git+protocol://`). As the vulnerability could still be exploited by manually run Git commands that interact with and check out submodules, users should immediately upgrade to a patched version of Git to protect against this vulnerability. Further details are available from the GitHub blog (["Git security vulnerabilities announced"](https://github.blog/2022-10-18-git-security-vulnerabilities-announced/)).

### [Updates](#updates-4)

* Update Docker Compose to [v2.12.0](https://github.com/docker/compose/releases/tag/v2.12.0).
* Updated handling of `image:tag@digest` references. When pulling an image using the `image:tag@digest` ("pull by digest"), image resolution happens through the content-addressable digest and the `image` and `tag` are not used. While this is expected, this could lead to confusing behavior, and could potentially be exploited through social engineering to run an image that is already present in the local image store. Docker now checks if the digest matches the repository name used to pull the image, and otherwise will produce an error.
* Updated handling of `image:tag@digest` references. Refer to the "Daemon" section above for details.

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-4)

* Added a mitigation for [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253), when using the classic Builder with a Git URL as the build context.
* Added a mitigation to the classic Builder and updated BuildKit to [v0.8.3-31-gc0149372](https://github.com/moby/buildkit/commit/c014937225cba29cfb1d5161fd134316c0e9bdaa), for [CVE-2022-39253](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-39253).

## [20.10.19](#201019)

*2022-10-14*

This release of Docker Engine comes with some bug-fixes, and an updated version of Docker Compose.

### [Updates](#updates-5)

* Update Docker Compose to [v2.11.2](https://github.com/docker/compose/releases/tag/v2.11.2).
* Update Go runtime to [1.18.7](https://go.dev/doc/devel/release#go1.18.minor), which contains fixes for [CVE-2022-2879](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2879), [CVE-2022-2880](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-2880), and [CVE-2022-41715](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-41715).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-5)

* Fix an issue that could result in a panic during `docker builder prune` or `docker system prune` [moby/moby#44122](https://github.com/moby/moby/pull/44122).
* Fix a bug where using `docker volume prune` would remove volumes that were still in use if the daemon was running with "live restore" and was restarted [moby/moby#44238](https://github.com/moby/moby/pull/44238).

## [20.10.18](#201018)

*2022-09-09*

This release of Docker Engine comes with a fix for a low-severity security issue, some minor bug fixes, and updated versions of Docker Compose, Docker Buildx, `containerd`, and `runc`.

### [Updates](#updates-6)

* Update Docker Buildx to [v0.9.1](https://github.com/docker/buildx/releases/tag/v0.9.1).
* Update Docker Compose to [v2.10.2](https://github.com/docker/compose/releases/tag/v2.10.2).
* Update containerd (`containerd.io` package) to [v1.6.8](https://github.com/containerd/containerd/releases/tag/v1.6.8).
* Update runc version to [v1.1.4](https://github.com/opencontainers/runc/releases/tag/v1.1.4).
* Update Go runtime to [1.18.6](https://go.dev/doc/devel/release#go1.18.minor), which contains fixes for [CVE-2022-27664](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-27664) and [CVE-2022-32190](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-32190).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-6)

* Add Bash completion for Docker Compose [docker/cli#3752](https://github.com/docker/cli/pull/3752).
* Fix an issue where file-capabilities were not preserved during build [moby/moby#43876](https://github.com/moby/moby/pull/43876).
* Fix an issue that could result in a panic caused by a concurrent map read and map write [moby/moby#44067](https://github.com/moby/moby/pull/44067).
* Fix a security vulnerability relating to supplementary group permissions, which could allow a container process to bypass primary group restrictions within the container [CVE-2022-36109](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-36109), [GHSA-rc4r-wh2q-q6c4](https://github.com/moby/moby/security/advisories/GHSA-rc4r-wh2q-q6c4).
* seccomp: add support for Landlock syscalls in default policy [moby/moby#43991](https://github.com/moby/moby/pull/43991).
* seccomp: update default policy to support new syscalls introduced in kernel 5.12 - 5.16 [moby/moby#43991](https://github.com/moby/moby/pull/43991).
* Fix an issue where cache lookup for image manifests would fail, resulting in a redundant round-trip to the image registry [moby/moby#44109](https://github.com/moby/moby/pull/44109).
* Fix an issue where `exec` processes and healthchecks were not terminated when they timed out [moby/moby#44018](https://github.com/moby/moby/pull/44018).

## [20.10.17](#201017)

*2022-06-06*

This release of Docker Engine comes with updated versions of Docker Compose and the `containerd`, and `runc` components, as well as some minor bug fixes.

### [Updates](#updates-7)

* Update Docker Compose to [v2.6.0](https://github.com/docker/compose/releases/tag/v2.6.0).
* Update containerd (`containerd.io` package) to [v1.6.6](https://github.com/containerd/containerd/releases/tag/v1.6.6), which contains a fix for [CVE-2022-31030](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-31030)
* Update runc version to [v1.1.2](https://github.com/opencontainers/runc/releases/tag/v1.1.2), which contains a fix for [CVE-2022-29162](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29162).
* Update Go runtime to [1.17.11](https://go.dev/doc/devel/release#go1.17.minor), which contains fixes for [CVE-2022-30634](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-30634), [CVE-2022-30629](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-30629), [CVE-2022-30580](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-30580) and [CVE-2022-29804](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29804)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-7)

* Remove asterisk from docker commands in zsh completion script [docker/cli#3648](https://github.com/docker/cli/pull/3648).
* Fix Windows port conflict with published ports in host mode for overlay [moby/moby#43644](https://github.com/moby/moby/pull/43644).
* Ensure performance tuning is always applied to libnetwork sandboxes [moby/moby#43683](https://github.com/moby/moby/pull/43683).

## [20.10.16](#201016)

*2022-05-12*

This release of Docker Engine fixes a regression in the Docker CLI builds for macOS, fixes an issue with `docker stats` when using containerd 1.5 and up, and updates the Go runtime to include a fix for [CVE-2022-29526](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29526).

### [Updates](#updates-8)

* Update golang.org/x/sys dependency which contains a fix for [CVE-2022-29526](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29526).
* Updated the `golang.org/x/sys` build-time dependency which contains a fix for [CVE-2022-29526](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29526).
* Updated Go runtime to [1.17.10](https://go.dev/doc/devel/release#go1.17.minor), which contains a fix for [CVE-2022-29526](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-29526).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-8)

* Fixed a regression in binaries for macOS introduced in [20.10.15](#201015), which resulted in a panic [docker/cli#43426](https://github.com/docker/cli/pull/3592).
* Fixed an issue where `docker stats` was showing empty stats when running with containerd 1.5.0 or up [moby/moby#43567](https://github.com/moby/moby/pull/43567).
* Used "weak" dependencies for the `docker scan` CLI plugin, to prevent a "conflicting requests" error when users performed an off-line installation from downloaded RPM packages [docker/docker-ce-packaging#659](https://github.com/docker/docker-ce-packaging/pull/659).

## [20.10.15](#201015)

*2022-05-05*

This release of Docker Engine comes with updated versions of the `compose`, `buildx`, `containerd`, and `runc` components, as well as some minor bug fixes.

### [Updates](#updates-9)

* Update Docker Compose to [v2.5.0](https://github.com/docker/compose/releases/tag/v2.5.0).
* Update Docker Buildx to [v0.8.2](https://github.com/docker/buildx/releases/tag/v0.8.2).
* Update Go runtime to [1.17.9](https://go.dev/doc/devel/release#go1.17.minor).
* Update containerd (`containerd.io` package) to [v1.6.4](https://github.com/containerd/containerd/releases/tag/v1.6.4).
* Update runc version to [v1.1.1](https://github.com/opencontainers/runc/releases/tag/v1.1.1).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-9)

* Use a RWMutex for stateCounter to prevent potential locking congestion [moby/moby#43426](https://github.com/moby/moby/pull/43426).
* Prevent an issue where the daemon was unable to find an available IP-range in some conditions [moby/moby#43360](https://github.com/moby/moby/pull/43360)
* Add packages for CentOS 9 stream and Fedora 36.

### [Known issues](#known-issues)

* We've identified an issue with the [macOS CLI binaries](https://download.docker.com/mac/static/stable/) in the 20.10.15 release. This issue has been resolved in the [20.10.16](#201016) release.

## [20.10.14](#201014)

*2022-03-23*

This release of Docker Engine updates the default inheritable capabilities for containers to address [CVE-2022-24769](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-24769), a new version of the `containerd.io` runtime is also included to address the same issue.

### [Updates](#updates-10)

* Update the default inheritable capabilities.
* Update the default inheritable capabilities for containers used during build.
* Update containerd (`containerd.io` package) to [v1.5.11](https://github.com/containerd/containerd/releases/tag/v1.5.11).
* Update `docker buildx` to [v0.8.1](https://github.com/docker/buildx/releases/tag/v0.8.1).

## [20.10.13](#201013)

*2022-03-10*

This release of Docker Engine contains some bug-fixes and packaging changes, updates to the `docker scan` and `docker buildx` commands, an updated version of the Go runtime, and new versions of the `containerd.io` runtime. Together with this release, we now also provide `.deb` and `.rpm` packages of Docker Compose V2, which can be installed using the (optional) `docker-compose-plugin` package.

### [New](#new-1)

* Provide `.deb` and `.rpm` packages for Docker Compose V2. [Docker Compose v2.3.3](https://github.com/docker/compose/releases/tag/v2.3.3) can now be installed on Linux using the `docker-compose-plugin` packages, which provides the `docker compose` subcommand on the Docker CLI. The Docker Compose plugin can also be installed and run standalone to be used as a drop-in replacement for `docker-compose` (Docker Compose V1) [docker/docker-ce-packaging#638](https://github.com/docker/docker-ce-packaging/pull/638). The `compose-cli-plugin` package can also be used on older version of the Docker CLI with support for CLI plugins (Docker CLI 18.09 and up).
* Provide packages for the upcoming Ubuntu 22.04 "Jammy Jellyfish" LTS release [docker/docker-ce-packaging#645](https://github.com/docker/docker-ce-packaging/pull/645), [docker/containerd-packaging#271](https://github.com/docker/containerd-packaging/pull/271).

### [Updates](#updates-11)

* Updated the bundled version of buildx to [v0.8.0](https://github.com/docker/buildx/releases/tag/v0.8.0).
* Update `docker buildx` to [v0.8.0](https://github.com/docker/buildx/releases/tag/v0.8.0).
* Update `docker scan` (`docker-scan-plugin`) to [v0.17.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.17.0).
* Update containerd (`containerd.io` package) to [v1.5.10](https://github.com/containerd/containerd/releases/tag/v1.5.10).
* Update the bundled runc version to [v1.0.3](https://github.com/opencontainers/runc/releases/tag/v1.0.3).
* Update Golang runtime to Go 1.16.15.
* Updates the fluentd log driver to prevent a potential daemon crash, and prevent containers from hanging when using the `fluentd-async-connect=true` and the remote server is unreachable [moby/moby#43147](https://github.com/moby/moby/pull/43147).

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-10)

* Fix a race condition when updating the container's state [moby/moby#43166](https://github.com/moby/moby/pull/43166).
* Update the etcd dependency to prevent the daemon from incorrectly holding file locks [moby/moby#43259](https://github.com/moby/moby/pull/43259)
* Fix detection of user-namespaces when configuring the default `net.ipv4.ping_group_range` sysctl [moby/moby#43084](https://github.com/moby/moby/pull/43084).
* Retry downloading image-manifests if a connection failure happens during image pull [moby/moby#43333](https://github.com/moby/moby/pull/43333).
* Various fixes in command-line reference and API documentation.
* Prevent an OOM when using the "local" logging driver with containers that produce a large amount of log messages [moby/moby#43165](https://github.com/moby/moby/pull/43165).

## [20.10.12](#201012)

2021-12-13

This release of Docker Engine contains changes in packaging only, and provides updates to the `docker scan` and `docker buildx` commands. Versions of `docker scan` before v0.11.0 are not able to detect the [Log4j 2 CVE-2021-44228](https://nvd.nist.gov/vuln/detail/CVE-2021-44228). We are shipping an updated version of `docker scan` in this release to help you scan your images for this vulnerability.

> Note
>
> The `docker scan` command on Linux is currently only supported on x86 platforms. We do not yet provide a package for other hardware architectures on Linux.

The `docker scan` feature is provided as a separate package and, depending on your upgrade or installation method, 'docker scan' may not be updated automatically to the latest version. Use the instructions below to update `docker scan` to the latest version. You can also use these instructions to install, or upgrade the `docker scan` package without upgrading the Docker Engine:

On `.deb` based distributions, such as Ubuntu and Debian:

```console
$ apt-get update && apt-get install docker-scan-plugin
```

On rpm-based distributions, such as CentOS or Fedora:

```console
$ yum install docker-scan-plugin
```

After upgrading, verify you have the latest version of `docker scan` installed:

```console
$ docker scan --accept-license --version
Version:    v0.12.0
Git commit: 1074dd0
Provider:   Snyk (1.790.0 (standalone))
```

[Read our blog post on CVE-2021-44228](https://www.docker.com/blog/apache-log4j-2-cve-2021-44228/) to learn how to use the `docker scan` command to check if images are vulnerable.

### [Packaging](#packaging)

* Update `docker scan` to [v0.12.0](https://github.com/docker/scan-cli-plugin/releases/tag/v0.12.0).
* Update `docker buildx` to [v0.7.1](https://github.com/docker/buildx/releases/tag/v0.7.1).
* Update Golang runtime to Go 1.16.12.

## [20.10.11](#201011)

2021-11-17

> Important
>
> Due to [net/http changes](https://github.com/golang/go/issues/40909) in [Go 1.16](https://golang.org/doc/go1.16#net/http), HTTP proxies configured through the `$HTTP_PROXY` environment variable are no longer used for TLS (`https://`) connections. Make sure you also set an `$HTTPS_PROXY` environment variable for handling requests to `https://` URLs. Refer to [Configure the daemon to use a proxy](https://docs.docker.com/engine/daemon/proxy/) to learn how to configure the Docker Daemon to use a proxy server.

### [Distribution](#distribution)

* Handle ambiguous OCI manifest parsing to mitigate [CVE-2021-41190](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41190) / [GHSA-mc8v-mgrf-8f4m](https://github.com/opencontainers/distribution-spec/security/advisories/GHSA-mc8v-mgrf-8f4m). See [GHSA-xmmx-7jpf-fx42](https://github.com/moby/moby/security/advisories/GHSA-xmmx-7jpf-fx42) for details.

### [Windows](#windows)

* Fix panic.log file having read-only attribute set [moby/moby#42987](https://github.com/moby/moby/pull/42987).

### [Packaging](#packaging-1)

* Update containerd to [v1.4.12](https://github.com/containerd/containerd/releases/tag/v1.4.12) to mitigate [CVE-2021-41190](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41190).
* Update Golang runtime to Go 1.16.10.

## [20.10.10](#201010)

2021-10-25

> Important
>
> Due to [net/http changes](https://github.com/golang/go/issues/40909) in [Go 1.16](https://golang.org/doc/go1.16#net/http), HTTP proxies configured through the `$HTTP_PROXY` environment variable are no longer used for TLS (`https://`) connections. Make sure you also set an `$HTTPS_PROXY` environment variable for handling requests to `https://` URLs. Refer to the [HTTP/HTTPS proxy section](https://docs.docker.com/engine/daemon/proxy/) to learn how to configure the Docker Daemon to use a proxy server.

### [Builder](#builder)

* Fix platform-matching logic to fix `docker build` using not finding images in the local image cache on Arm machines when using BuildKit [moby/moby#42954](https://github.com/moby/moby/pull/42954)

### [Runtime](#runtime)

* Add support for `clone3` syscall in the default seccomp policy to support running containers based on recent versions of Fedora and Ubuntu. [moby/moby/#42836](https://github.com/moby/moby/pull/42836).
* Windows: update hcsshim library to fix a bug in sparse file handling in container layers, which was exposed by recent changes in Windows [moby/moby#42944](https://github.com/moby/moby/pull/42944).
* Fix some situations where `docker stop` could hang forever [moby/moby#42956](https://github.com/moby/moby/pull/42956).

### [Swarm](#swarm)

* Fix an issue where updating a service did not roll back on failure [moby/moby#42875](https://github.com/moby/moby/pull/42875).

### [Packaging](#packaging-2)

* Add packages for Ubuntu 21.10 "Impish Indri" and Fedora 35.
* Update `docker scan` to v0.9.0
* Update Golang runtime to Go 1.16.9.

## [20.10.9](#20109)

2021-10-04

This release is a security release with security fixes in the CLI, runtime, as well as updated versions of the containerd.io package.

> Important
>
> Due to [net/http changes](https://github.com/golang/go/issues/40909) in [Go 1.16](https://golang.org/doc/go1.16#net/http), HTTP proxies configured through the `$HTTP_PROXY` environment variable are no longer used for TLS (`https://`) connections. Make sure you also set an `$HTTPS_PROXY` environment variable for handling requests to `https://` URLs. Refer to the [HTTP/HTTPS proxy section](https://docs.docker.com/engine/daemon/proxy/) to learn how to configure the Docker Daemon to use a proxy server.

### [Client](#client)

* [CVE-2021-41092](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41092) Ensure default auth config has address field set, to prevent credentials being sent to the default registry.

### [Runtime](#runtime-1)

* [CVE-2021-41089](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41089) Create parent directories inside a chroot during `docker cp` to prevent a specially crafted container from changing permissions of existing files in the host’s filesystem.
* [CVE-2021-41091](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41091) Lock down file permissions to prevent unprivileged users from discovering and executing programs in `/var/lib/docker`.

### [Packaging](#packaging-3)

> **Known issue**
>
> The `ctr` binary shipping with the static packages of this release is not statically linked, and will not run in Docker images using alpine as a base image. Users can install the `libc6-compat` package, or download a previous version of the `ctr` binary as a workaround. Refer to the containerd ticket related to this issue for more details: [containerd/containerd#5824](https://github.com/containerd/containerd/issues/5824).

* Update Golang runtime to Go 1.16.8, which contains fixes for [CVE-2021-36221](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-36221) and [CVE-2021-39293](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-39293)
* Update static binaries and containerd.io rpm and deb packages to containerd v1.4.11 and runc v1.0.2 to address [CVE-2021-41103](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-41103).
* Update the bundled buildx version to v0.6.3 for rpm and deb packages.

## [20.10.8](#20108)

2021-08-03

> Important
>
> Due to [net/http changes](https://github.com/golang/go/issues/40909) in [Go 1.16](https://golang.org/doc/go1.16#net/http), HTTP proxies configured through the `$HTTP_PROXY` environment variable are no longer used for TLS (`https://`) connections. Make sure you also set an `$HTTPS_PROXY` environment variable for handling requests to `https://` URLs. Refer to the [HTTP/HTTPS proxy section](https://docs.docker.com/engine/daemon/proxy/) to learn how to configure the Docker Daemon to use a proxy server.

### [Deprecation](#deprecation)

* Deprecate support for encrypted TLS private keys. Legacy PEM encryption as specified in RFC 1423 is insecure by design. Because it does not authenticate the ciphertext, it is vulnerable to padding oracle attacks that can let an attacker recover the plaintext. Support for encrypted TLS private keys is now marked as deprecated, and will be removed in an upcoming release. [docker/cli#3219](https://github.com/docker/cli/pull/3219)
* Deprecate Kubernetes stack support. Following the deprecation of [Compose on Kubernetes](https://github.com/docker/compose-on-kubernetes), support for Kubernetes in the `stack` and `context` commands in the Docker CLI is now marked as deprecated, and will be removed in an upcoming release [docker/cli#3174](https://github.com/docker/cli/pull/3174).

### [Client](#client-1)

* Fix `Invalid standard handle identifier` errors on Windows [docker/cli#3132](https://github.com/docker/cli/pull/3132).

### [Rootless](#rootless)

* Avoid `can't open lock file /run/xtables.lock: Permission denied` error on SELinux hosts [moby/moby#42462](https://github.com/moby/moby/pull/42462).
* Disable overlay2 when running with SELinux to prevent permission denied errors [moby/moby#42462](https://github.com/moby/moby/pull/42462).
* Fix `x509: certificate signed by unknown authority` error on openSUSE Tumbleweed [moby/moby#42462](https://github.com/moby/moby/pull/42462).

### [Runtime](#runtime-2)

* Print a warning when using the `--platform` option to pull a single-arch image that does not match the specified architecture [moby/moby#42633](https://github.com/moby/moby/pull/42633).
* Fix incorrect `Your kernel does not support swap memory limit` warning when running with cgroups v2 [moby/moby#42479](https://github.com/moby/moby/pull/42479).
* Windows: Fix a situation where containers were not stopped if `HcsShutdownComputeSystem` returned an `ERROR_PROC_NOT_FOUND` error [moby/moby#42613](https://github.com/moby/moby/pull/42613)

### [Swarm](#swarm-1)

* Fix a possibility where overlapping IP addresses could exist as a result of the node failing to clean up its old loadbalancer IPs [moby/moby#42538](https://github.com/moby/moby/pull/42538)
* Fix a deadlock in log broker ("dispatcher is stopped") [moby/moby#42537](https://github.com/moby/moby/pull/42537)

### [Packaging](#packaging-4)

> **Known issue**
>
> The `ctr` binary shipping with the static packages of this release is not statically linked, and will not run in Docker images using alpine as a base image. Users can install the `libc6-compat` package, or download a previous version of the `ctr` binary as a workaround. Refer to the containerd ticket related to this issue for more details: [containerd/containerd#5824](https://github.com/containerd/containerd/issues/5824).

* Remove packaging for Ubuntu 16.04 "Xenial" and Fedora 32, as they reached EOL [docker/docker-ce-packaging#560](https://github.com/docker/docker-ce-packaging/pull/560)
* Update Golang runtime to Go 1.16.6
* Update the bundled buildx version to v0.6.1 for rpm and deb packages [docker/docker-ce-packaging#562](https://github.com/docker/docker-ce-packaging/pull/562)
* Update static binaries and containerd.io rpm and deb packages to containerd v1.4.9 and runc v1.0.1: [docker/containerd-packaging#241](https://github.com/docker/containerd-packaging/pull/241), [docker/containerd-packaging#245](https://github.com/docker/containerd-packaging/pull/245), [docker/containerd-packaging#247](https://github.com/docker/containerd-packaging/pull/247).

## [20.10.7](#20107)

2021-06-02

### [Client](#client-2)

* Suppress warnings for deprecated cgroups [docker/cli#3099](https://github.com/docker/cli/pull/3099).
* Prevent sending `SIGURG` signals to container on Linux and macOS. The Go runtime (starting with Go 1.14) uses `SIGURG` signals internally as an interrupt to support preemptable syscalls. In situations where the Docker CLI was attached to a container, these interrupts were forwarded to the container. This fix changes the Docker CLI to ignore `SIGURG` signals [docker/cli#3107](https://github.com/docker/cli/pull/3107), [moby/moby#42421](https://github.com/moby/moby/pull/42421).

### [Builder](#builder-1)

* Update BuildKit to version v0.8.3-3-g244e8cde [moby/moby#42448](https://github.com/moby/moby/pull/42448):

  * Transform relative mountpoints for exec mounts in the executor to work around a breaking change in runc v1.0.0-rc94 and up. [moby/buildkit#2137](https://github.com/moby/buildkit/pull/2137).
  * Add retry on image push 5xx errors. [moby/buildkit#2043](https://github.com/moby/buildkit/pull/2043).
  * Fix build-cache not being invalidated when renaming a file that is copied using a `COPY` command with a wildcard. Note that this change invalidates existing build caches for copy commands that use a wildcard. [moby/buildkit#2018](https://github.com/moby/buildkit/pull/2018).
  * Fix build-cache not being invalidated when using mounts [moby/buildkit#2076](https://github.com/moby/buildkit/pull/2076).

* Fix build failures when `FROM` image is not cached when using legacy schema 1 images [moby/moby#42382](https://github.com/moby/moby/pull/42382).

### [Logging](#logging)

* Update the hcsshim SDK to make daemon logs on Windows less verbose [moby/moby#42292](https://github.com/moby/moby/pull/42292).

### [Rootless](#rootless-1)

* Fix capabilities not being honored when an image was built on a daemon with user-namespaces enabled [moby/moby#42352](https://github.com/moby/moby/pull/42352).

### [Networking](#networking)

* Update libnetwork to fix publishing ports on environments with kernel boot parameter `ipv6.disable=1`, and to fix a deadlock causing internal DNS lookups to fail [moby/moby#42413](https://github.com/moby/moby/pull/42413).

### [Contrib](#contrib)

* Update rootlesskit to v0.14.2 to fix a timeout when starting the userland proxy with the `slirp4netns` port driver [moby/moby#42294](https://github.com/moby/moby/pull/42294).
* Fix "Device or resource busy" errors when running docker-in-docker on a rootless daemon [moby/moby#42342](https://github.com/moby/moby/pull/42342).

### [Packaging](#packaging-5)

* Update containerd to v1.4.6, runc v1.0.0-rc95 to address [CVE-2021-30465](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-30465) [moby/moby#42398](https://github.com/moby/moby/pull/42398), [moby/moby#42395](https://github.com/moby/moby/pull/42395), [docker/containerd-packaging#234](https://github.com/docker/containerd-packaging/pull/234)
* Update containerd to v1.4.5, runc v1.0.0-rc94 [moby/moby#42372](https://github.com/moby/moby/pull/42372), [moby/moby#42388](https://github.com/moby/moby/pull/42388), [docker/containerd-packaging#232](https://github.com/docker/containerd-packaging/pull/232).
* Update Docker Scan plugin packages (`docker-scan-plugin`) to v0.8 [docker/docker-ce-packaging#545](https://github.com/docker/docker-ce-packaging/pull/545).

## [20.10.6](#20106)

2021-04-12

### [Client](#client-3)

* Apple Silicon (darwin/arm64) support for Docker CLI [docker/cli#3042](https://github.com/docker/cli/pull/3042)
* config: print deprecation warning when falling back to pre-v1.7.0 config file `~/.dockercfg`. Support for this file will be removed in a future release [docker/cli#3000](https://github.com/docker/cli/pull/3000)

### [Builder](#builder-2)

* Fix classic builder silently ignoring unsupported Dockerfile options and prompt to enable BuildKit instead [moby/moby#42197](https://github.com/moby/moby/pull/42197)

### [Logging](#logging-1)

* json-file: fix sporadic unexpected EOF errors [moby/moby#42174](https://github.com/moby/moby/pull/42174)

### [Networking](#networking-1)

* Fix a regression in docker 20.10, causing IPv6 addresses no longer to be bound by default when mapping ports [moby/moby#42205](https://github.com/moby/moby/pull/42205)
* Fix implicit IPv6 port-mappings not included in API response. Before docker 20.10, published ports were accessible through both IPv4 and IPv6 by default, but the API only included information about the IPv4 (0.0.0.0) mapping [moby/moby#42205](https://github.com/moby/moby/pull/42205)
* Fix a regression in docker 20.10, causing the docker-proxy to not be terminated in all cases [moby/moby#42205](https://github.com/moby/moby/pull/42205)
* Fix iptables forwarding rules not being cleaned up upon container removal [moby/moby#42205](https://github.com/moby/moby/pull/42205)

### [Packaging](#packaging-6)

* Update containerd to [v1.4.4](https://github.com/containerd/containerd/releases/tag/v1.4.4) for static binaries. The containerd.io package on apt/yum repos already had this update out of band. Includes a fix for [CVE-2021-21334](https://github.com/containerd/containerd/security/advisories/GHSA-6g2q-w5j3-fwh4). [moby/moby#42124](https://github.com/moby/moby/pull/42124)
* Packages for Debian/Raspbian 11 Bullseye, Ubuntu 21.04 Hirsute Hippo and Fedora 34 [docker/docker-ce-packaging#521](https://github.com/docker/docker-ce-packaging/pull/521) [docker/docker-ce-packaging#522](https://github.com/docker/docker-ce-packaging/pull/522) [docker/docker-ce-packaging#533](https://github.com/docker/docker-ce-packaging/pull/533)
* Provide the [Docker Scan CLI](https://github.com/docker/scan-cli-plugin) plugin on Linux amd64 via a `docker-scan-plugin` package as a recommended dependency for the `docker-ce-cli` package [docker/docker-ce-packaging#537](https://github.com/docker/docker-ce-packaging/pull/537)
* Include VPNKit binary for arm64 [moby/moby#42141](https://github.com/moby/moby/pull/42141)

### [Plugins](#plugins)

* Fix docker plugin create making plugins that were incompatible with older versions of Docker [moby/moby#42256](https://github.com/moby/moby/pull/42256)

### [Rootless](#rootless-2)

* Update RootlessKit to [v0.14.1](https://github.com/rootless-containers/rootlesskit/releases/tag/v0.14.1) (see also [v0.14.0](https://github.com/rootless-containers/rootlesskit/releases/tag/v0.14.0) [v0.13.2](https://github.com/rootless-containers/rootlesskit/releases/tag/v0.13.2)) [moby/moby#42186](https://github.com/moby/moby/pull/42186) [moby/moby#42232](https://github.com/moby/moby/pull/42232)
* dockerd-rootless-setuptool.sh: create CLI context "rootless" [moby/moby#42109](https://github.com/moby/moby/pull/42109)
* dockerd-rootless.sh: prohibit running as root [moby/moby#42072](https://github.com/moby/moby/pull/42072)
* Fix "operation not permitted" when bind mounting existing mounts [moby/moby#42233](https://github.com/moby/moby/pull/42233)
* overlay2: fix "createDirWithOverlayOpaque(...) ... input/output error" [moby/moby#42235](https://github.com/moby/moby/pull/42235)
* overlay2: support "userxattr" option (kernel 5.11) [moby/moby#42168](https://github.com/moby/moby/pull/42168)
* btrfs: allow unprivileged user to delete subvolumes (kernel >= 4.18) [moby/moby#42253](https://github.com/moby/moby/pull/42253)
* cgroup2: Move cgroup v2 out of experimental [moby/moby#42263](https://github.com/moby/moby/pull/42263)

## [20.10.5](#20105)

2021-03-02

### [Client](#client-4)

* Revert [docker/cli#2960](https://github.com/docker/cli/pull/2960) to fix hanging in `docker start --attach` and remove spurious `Unsupported signal: <nil>. Discarding` messages. [docker/cli#2987](https://github.com/docker/cli/pull/2987).

## [20.10.4](#20104)

2021-02-26

### [Builder](#builder-3)

* Fix incorrect cache match for inline cache import with empty layers [moby/moby#42061](https://github.com/moby/moby/pull/42061)

* Update BuildKit to v0.8.2 [moby/moby#42061](https://github.com/moby/moby/pull/42061)

  * resolver: avoid error caching on token fetch
  * fileop: fix checksum to contain indexes of inputs preventing certain cache misses
  * Fix reference count issues on typed errors with mount references (fixing `invalid mutable ref` errors)
  * git: set token only for main remote access allowing cloning submodules with different credentials

* Ensure blobs get deleted in /var/lib/docker/buildkit/content/blobs/sha256 after pull. To clean up old state run `builder prune` [moby/moby#42065](https://github.com/moby/moby/pull/42065)

* Fix parallel pull synchronization regression [moby/moby#42049](https://github.com/moby/moby/pull/42049)

* Ensure libnetwork state files do not leak [moby/moby#41972](https://github.com/moby/moby/pull/41972)

### [Client](#client-5)

* Fix a panic on `docker login` if no config file is present [docker/cli#2959](https://github.com/docker/cli/pull/2959)
* Fix `WARNING: Error loading config file: .dockercfg: $HOME is not defined` [docker/cli#2958](https://github.com/docker/cli/pull/2958)

### [Runtime](#runtime-3)

* docker info: silence unhandleable warnings [moby/moby#41958](https://github.com/moby/moby/pull/41958)
* Avoid creating parent directories for XGlobalHeader [moby/moby#42017](https://github.com/moby/moby/pull/42017)
* Use 0755 permissions when creating missing directories [moby/moby#42017](https://github.com/moby/moby/pull/42017)
* Fallback to manifest list when no platform matches in image config [moby/moby#42045](https://github.com/moby/moby/pull/42045) [moby/moby#41873](https://github.com/moby/moby/pull/41873)
* Fix a daemon panic on setups with a custom default runtime configured [moby/moby#41974](https://github.com/moby/moby/pull/41974)
* Fix a panic when daemon configuration is empty [moby/moby#41976](https://github.com/moby/moby/pull/41976)
* Fix daemon panic when starting container with invalid device cgroup rule [moby/moby#42001](https://github.com/moby/moby/pull/42001)
* Fix userns-remap option when username & UID match [moby/moby#42013](https://github.com/moby/moby/pull/42013)
* static: update runc binary to v1.0.0-rc93 [moby/moby#42014](https://github.com/moby/moby/pull/42014)

### [Logger](#logger)

* Honor `labels-regex` config even if `labels` is not set [moby/moby#42046](https://github.com/moby/moby/pull/42046)
* Handle long log messages correctly preventing awslogs in non-blocking mode to split events bigger than 16kB [mobymoby#41975](https://github.com/moby/moby/pull/41975)

### [Rootless](#rootless-3)

* Prevent the service hanging when stopping by setting systemd KillMode to mixed [moby/moby#41956](https://github.com/moby/moby/pull/41956)
* dockerd-rootless.sh: add typo guard [moby/moby#42070](https://github.com/moby/moby/pull/42070)
* Update rootlesskit to v0.13.1 to fix handling of IPv6 addresses [moby/moby#42025](https://github.com/moby/moby/pull/42025)
* allow mknodding FIFO inside userns [moby/moby#41957](https://github.com/moby/moby/pull/41957)

### [Security](#security)

* profiles: seccomp: update to Linux 5.11 syscall list [moby/moby#41971](https://github.com/moby/moby/pull/41971)

### [Swarm](#swarm-2)

* Fix issue with heartbeat not persisting upon restart [moby/moby#42060](https://github.com/moby/moby/pull/42060)
* Fix potential stalled tasks [moby/moby#42060](https://github.com/moby/moby/pull/42060)
* Fix `--update-order` and `--rollback-order` flags when only `--update-order` or `--rollback-order` is provided [docker/cli#2963](https://github.com/docker/cli/pull/2963)
* Fix `docker service rollback` returning a non-zero exit code in some situations [docker/cli#2964](https://github.com/docker/cli/pull/2964)
* Fix inconsistent progress-bar direction on `docker service rollback` [docker/cli#2964](https://github.com/docker/cli/pull/2964)

## [20.10.3](#20103)

2021-02-01

### [Security](#security-1)

* [CVE-2021-21285](https://github.com/moby/moby/security/advisories/GHSA-6fj5-m822-rqx8) Prevent an invalid image from crashing docker daemon
* [CVE-2021-21284](https://github.com/moby/moby/security/advisories/GHSA-7452-xqpj-6rpc) Lock down file permissions to prevent remapped root from accessing docker state
* Ensure AppArmor and SELinux profiles are applied when building with BuildKit

### [Client](#client-6)

* Check contexts before importing them to reduce risk of extracted files escaping context store
* Windows: prevent executing certain binaries from current directory [docker/cli#2950](https://github.com/docker/cli/pull/2950)

## [20.10.2](#20102)

2021-01-04

### [Runtime](#runtime-4)

* Fix a daemon start up hang when restoring containers with restart policies but that keep failing to start [moby/moby#41729](https://github.com/moby/moby/pull/41729)
* overlay2: fix an off-by-one error preventing to build or run containers when data-root is 24-bytes long [moby/moby#41830](https://github.com/moby/moby/pull/41830)
* systemd: send `sd_notify STOPPING=1` when shutting down [moby/moby#41832](https://github.com/moby/moby/pull/41832)

### [Networking](#networking-2)

* Fix IPv6 port forwarding [moby/moby#41805](https://github.com/moby/moby/pull/41805) [moby/libnetwork#2604](https://github.com/moby/libnetwork/pull/2604)

### [Swarm](#swarm-3)

* Fix filtering for `replicated-job` and `global-job` service modes [moby/moby#41806](https://github.com/moby/moby/pull/41806)

### [Packaging](#packaging-7)

* buildx updated to [v0.5.1](https://github.com/docker/buildx/releases/tag/v0.5.1) [docker/docker-ce-packaging#516](https://github.com/docker/docker-ce-packaging/pull/516)

## [20.10.1](#20101)

2020-12-14

### [Builder](#builder-4)

* buildkit: updated to [v0.8.1](https://github.com/moby/buildkit/releases/tag/v0.8.1) with various bugfixes [moby/moby#41793](https://github.com/moby/moby/pull/41793)

### [Packaging](#packaging-8)

* Revert a change in the systemd unit that could prevent docker from starting due to a startup order conflict [docker/docker-ce-packaging#514](https://github.com/docker/docker-ce-packaging/pull/514)
* buildx updated to [v0.5.0](https://github.com/docker/buildx/releases/tag/v0.5.0) [docker/docker-ce-packaging#515](https://github.com/docker/docker-ce-packaging/pull/515)

## [20.10.0](#20100)

2020-12-08

### [Deprecation / Removal](#deprecation--removal)

For an overview of all deprecated features, refer to the [Deprecated Engine Features](/engine/deprecated/) page.

* Warnings and deprecation notice when `docker pull`-ing from non-compliant registries not supporting pull-by-digest [docker/cli#2872](https://github.com/docker/cli/pull/2872)
* Sterner warnings and deprecation notice for unauthenticated tcp access [moby/moby#41285](https://github.com/moby/moby/pull/41285)
* Deprecate KernelMemory (`docker run --kernel-memory`) [moby/moby#41254](https://github.com/moby/moby/pull/41254) [docker/cli#2652](https://github.com/docker/cli/pull/2652)
* Deprecate `aufs` storage driver [docker/cli#1484](https://github.com/docker/cli/pull/1484)
* Deprecate host-discovery and overlay networks with external k/v stores [moby/moby#40614](https://github.com/moby/moby/pull/40614) [moby/moby#40510](https://github.com/moby/moby/pull/40510)
* Deprecate Dockerfile legacy 'ENV name value' syntax, use `ENV name=value` instead [docker/cli#2743](https://github.com/docker/cli/pull/2743)
* Remove deprecated "filter" parameter for API v1.41 and up [moby/moby#40491](https://github.com/moby/moby/pull/40491)
* Disable distribution manifest v2 schema 1 on push [moby/moby#41295](https://github.com/moby/moby/pull/41295)
* Remove hack MalformedHostHeaderOverride breaking old docker clients (<= 1.12) in which case, set `DOCKER_API_VERSION` [moby/moby#39076](https://github.com/moby/moby/pull/39076)
* Remove "docker engine" subcommands [docker/cli#2207](https://github.com/docker/cli/pull/2207)
* Remove experimental "deploy" from "dab" files [docker/cli#2216](https://github.com/docker/cli/pull/2216)
* Remove deprecated `docker search --automated` and `--stars` flags [docker/cli#2338](https://github.com/docker/cli/pull/2338)
* No longer allow reserved namespaces in engine labels [docker/cli#2326](https://github.com/docker/cli/pull/2326)

### [API](#api)

* Update API version to v1.41
* Do not require "experimental" for metrics API [moby/moby#40427](https://github.com/moby/moby/pull/40427)
* `GET /events` now returns `prune` events after pruning resources have completed [moby/moby#41259](https://github.com/moby/moby/pull/41259)
  * Prune events are returned for `container`, `network`, `volume`, `image`, and `builder`, and have a `reclaimed` attribute, indicating the amount of space reclaimed (in bytes)
* Add `one-shot` stats option to not prime the stats [moby/moby#40478](https://github.com/moby/moby/pull/40478)
* Adding OS version info to the system info's API (`/info`) [moby/moby#38349](https://github.com/moby/moby/pull/38349)
* Add DefaultAddressPools to docker info [moby/moby#40714](https://github.com/moby/moby/pull/40714)
* Add API support for PidsLimit on services [moby/moby#39882](https://github.com/moby/moby/pull/39882)

### [Builder](#builder-5)

* buildkit,dockerfile: Support for `RUN --mount` options without needing to specify experimental dockerfile `#syntax` directive. [moby/buildkit#1717](https://github.com/moby/buildkit/pull/1717)

* dockerfile: `ARG` command now supports defining multiple build args on the same line similarly to `ENV` [moby/buildkit#1692](https://github.com/moby/buildkit/pull/1692)

* dockerfile: `--chown` flag in `ADD` now allows parameter expansion [moby/buildkit#1473](https://github.com/moby/buildkit/pull/1473)

* buildkit: Fetching authorization tokens has been moved to client-side (if the client supports it). Passwords do not leak into the build daemon anymore and users can see from build output when credentials or tokens are accessed. [moby/buildkit#1660](https://github.com/moby/buildkit/pull/1660)

* buildkit: Connection errors while communicating with the registry for push and pull now trigger a retry [moby/buildkit#1791](https://github.com/moby/buildkit/pull/1791)

* buildkit: Git source now supports token authentication via build secrets [moby/moby#41234](https://github.com/moby/moby/pull/41234) [docker/cli#2656](https://github.com/docker/cli/pull/2656) [moby/buildkit#1533](https://github.com/moby/buildkit/pull/1533)

* buildkit: Building from git source now supports forwarding SSH socket for authentication [moby/buildkit#1782](https://github.com/moby/buildkit/pull/1782)

* buildkit: Avoid builds that generate excessive logs to cause a crash or slow down the build. Clipping is performed if needed. [moby/buildkit#1754](https://github.com/moby/buildkit/pull/1754)

* buildkit: Change default Seccomp profile to the one provided by Docker [moby/buildkit#1807](https://github.com/moby/buildkit/pull/1807)

* buildkit: Support for exposing SSH agent socket on Windows has been improved [moby/buildkit#1695](https://github.com/moby/buildkit/pull/1695)

* buildkit: Disable truncating by default when using --progress=plain [moby/buildkit#1435](https://github.com/moby/buildkit/pull/1435)

* buildkit: Allow better handling client sessions dropping while it is being shared by multiple builds [moby/buildkit#1551](https://github.com/moby/buildkit/pull/1551)

* buildkit: secrets: allow providing secrets with env [moby/moby#41234](https://github.com/moby/moby/pull/41234) [docker/cli#2656](https://github.com/docker/cli/pull/2656) [moby/buildkit#1534](https://github.com/moby/buildkit/pull/1534)

  * Support `--secret id=foo,env=MY_ENV` as an alternative for storing a secret value to a file.
  * `--secret id=GIT_AUTH_TOKEN` will load env if it exists and the file does not.

* buildkit: Support for mirrors fallbacks, insecure TLS and custom TLS config [moby/moby#40814](https://github.com/moby/moby/pull/40814)

* buildkit: remotecache: Only visit each item once when walking results [moby/moby#41234](https://github.com/moby/moby/pull/41234) [moby/buildkit#1577](https://github.com/moby/buildkit/pull/1577)
  * Improves performance and CPU use on bigger graphs

* buildkit: Check remote when local image platform doesn't match [moby/moby#40629](https://github.com/moby/moby/pull/40629)

* buildkit: image export: Use correct media type when creating new layer blobs [moby/moby#41234](https://github.com/moby/moby/pull/41234) [moby/buildkit#1541](https://github.com/moby/buildkit/pull/1541)

* buildkit: progressui: fix logs time formatting [moby/moby#41234](https://github.com/moby/moby/pull/41234) [docker/cli#2656](https://github.com/docker/cli/pull/2656) [moby/buildkit#1549](https://github.com/moby/buildkit/pull/1549)

* buildkit: mitigate containerd issue on parallel push [moby/moby#41234](https://github.com/moby/moby/pull/41234) [moby/buildkit#1548](https://github.com/moby/buildkit/pull/1548)

* buildkit: inline cache: fix handling of duplicate blobs [moby/moby#41234](https://github.com/moby/moby/pull/41234) [moby/buildkit#1568](https://github.com/moby/buildkit/pull/1568)

  * Fixes <https://github.com/moby/buildkit/issues/1388> cache-from working unreliably
  * Fixes <https://github.com/moby/moby/issues/41219> Image built from cached layers is missing data

* Allow ssh:// for remote context URLs [moby/moby#40179](https://github.com/moby/moby/pull/40179)

* builder: remove legacy build's session handling (was experimental) [moby/moby#39983](https://github.com/moby/moby/pull/39983)

### [Client](#client-7)

* Add swarm jobs support to CLI [docker/cli#2262](https://github.com/docker/cli/pull/2262)
* Add `-a/--all-tags` to docker push [docker/cli#2220](https://github.com/docker/cli/pull/2220)
* Add support for Kubernetes username/password auth [docker/cli#2308](https://github.com/docker/cli/pull/2308)
* Add `--pull=missing|always|never` to `run` and `create` commands [docker/cli#1498](https://github.com/docker/cli/pull/1498)
* Add `--env-file` flag to `docker exec` for parsing environment variables from a file [docker/cli#2602](https://github.com/docker/cli/pull/2602)
* Add shorthand `-n` for `--tail` option [docker/cli#2646](https://github.com/docker/cli/pull/2646)
* Add log-driver and options to service inspect "pretty" format [docker/cli#1950](https://github.com/docker/cli/pull/1950)
* docker run: specify cgroup namespace mode with `--cgroupns` [docker/cli#2024](https://github.com/docker/cli/pull/2024)
* `docker manifest rm` command to remove manifest list draft from local storage [docker/cli#2449](https://github.com/docker/cli/pull/2449)
* Add "context" to "docker version" and "docker info" [docker/cli#2500](https://github.com/docker/cli/pull/2500)
* Propagate platform flag to container create API [docker/cli#2551](https://github.com/docker/cli/pull/2551)
* The `docker ps --format` flag now has a `.State` placeholder to print the container's state without additional details about uptime and health check [docker/cli#2000](https://github.com/docker/cli/pull/2000)
* Add support for docker-compose schema v3.9 [docker/cli#2073](https://github.com/docker/cli/pull/2073)
* Add support for docker push `--quiet` [docker/cli#2197](https://github.com/docker/cli/pull/2197)
* Hide flags that are not supported by BuildKit, if BuildKit is enabled [docker/cli#2123](https://github.com/docker/cli/pull/2123)
* Update flag description for `docker rm -v` to clarify the option only removes anonymous (unnamed) volumes [docker/cli#2289](https://github.com/docker/cli/pull/2289)
* Improve tasks printing for docker services [docker/cli#2341](https://github.com/docker/cli/pull/2341)
* docker info: list CLI plugins alphabetically [docker/cli#2236](https://github.com/docker/cli/pull/2236)
* Fix order of processing of `--label-add/--label-rm`, `--container-label-add/--container-label-rm`, and `--env-add/--env-rm` flags on `docker service update` to allow replacing existing values [docker/cli#2668](https://github.com/docker/cli/pull/2668)
* Fix `docker rm --force` returning a non-zero exit code if one or more containers did not exist [docker/cli#2678](https://github.com/docker/cli/pull/2678)
* Improve memory stats display by using `total_inactive_file` instead of `cache` [docker/cli#2415](https://github.com/docker/cli/pull/2415)
* Mitigate against YAML files that has excessive aliasing [docker/cli#2117](https://github.com/docker/cli/pull/2117)
* Allow using advanced syntax when setting a config or secret with only the source field [docker/cli#2243](https://github.com/docker/cli/pull/2243)
* Fix reading config files containing `username` and `password` auth even if `auth` is empty [docker/cli#2122](https://github.com/docker/cli/pull/2122)
* docker cp: prevent NPE when failing to stat destination [docker/cli#2221](https://github.com/docker/cli/pull/2221)
* config: preserve ownership and permissions on configfile [docker/cli#2228](https://github.com/docker/cli/pull/2228)

### [Logging](#logging-2)

* Support reading `docker logs` with all logging drivers (best effort) [moby/moby#40543](https://github.com/moby/moby/pull/40543)
* Add `splunk-index-acknowledgment` log option to work with Splunk HECs with index acknowledgment enabled [moby/moby#39987](https://github.com/moby/moby/pull/39987)
* Add partial metadata to journald logs [moby/moby#41407](https://github.com/moby/moby/pull/41407)
* Reduce allocations for logfile reader [moby/moby#40796](https://github.com/moby/moby/pull/40796)
* Fluentd: add fluentd-async, fluentd-request-ack, and deprecate fluentd-async-connect [moby/moby#39086](https://github.com/moby/moby/pull/39086)

### [Runtime](#runtime-5)

* Support cgroup2 [moby/moby#40174](https://github.com/moby/moby/pull/40174) [moby/moby#40657](https://github.com/moby/moby/pull/40657) [moby/moby#40662](https://github.com/moby/moby/pull/40662)
* cgroup2: use "systemd" cgroup driver by default when available [moby/moby#40846](https://github.com/moby/moby/pull/40846)
* new storage driver: fuse-overlayfs [moby/moby#40483](https://github.com/moby/moby/pull/40483)
* Update containerd binary to v1.4.3 [moby/moby#41732](https://github.com/moby/moby/pull/41732)
* `docker push` now defaults to `latest` tag instead of all tags [moby/moby#40302](https://github.com/moby/moby/pull/40302)
* Added ability to change the number of reconnect attempts during connection loss while pulling an image by adding max-download-attempts to the config file [moby/moby#39949](https://github.com/moby/moby/pull/39949)
* Add support for containerd v2 shim by using the now default `io.containerd.runc.v2` runtime [moby/moby#41182](https://github.com/moby/moby/pull/41182)
* cgroup v1: change the default runtime to io.containerd.runc.v2. Requires containerd v1.3.0 or later. v1.3.5 or later is recommended [moby/moby#41210](https://github.com/moby/moby/pull/41210)
* Start containers in their own cgroup namespaces [moby/moby#38377](https://github.com/moby/moby/pull/38377)
* Enable DNS Lookups for CIFS Volumes [moby/moby#39250](https://github.com/moby/moby/pull/39250)
* Use MemAvailable instead of MemFree to estimate actual available memory [moby/moby#39481](https://github.com/moby/moby/pull/39481)
* The `--device` flag in `docker run` will now be honored when the container is started in privileged mode [moby/moby#40291](https://github.com/moby/moby/pull/40291)
* Enforce reserved internal labels [moby/moby#40394](https://github.com/moby/moby/pull/40394)
* Raise minimum memory limit to 6M, to account for higher memory use by runtimes during container startup [moby/moby#41168](https://github.com/moby/moby/pull/41168)
* vendor runc v1.0.0-rc92 [moby/moby#41344](https://github.com/moby/moby/pull/41344) [moby/moby#41317](https://github.com/moby/moby/pull/41317)
* info: add warnings about missing blkio cgroup support [moby/moby#41083](https://github.com/moby/moby/pull/41083)
* Accept platform spec on container create [moby/moby#40725](https://github.com/moby/moby/pull/40725)
* Fix handling of looking up user- and group-names with spaces [moby/moby#41377](https://github.com/moby/moby/pull/41377)

### [Networking](#networking-3)

* Support host.docker.internal in dockerd on Linux [moby/moby#40007](https://github.com/moby/moby/pull/40007)

* Include IPv6 address of linked containers in /etc/hosts [moby/moby#39837](https://github.com/moby/moby/pull/39837)

* `--ip6tables` enables IPv6 iptables rules (only if experimental) [moby/moby#41622](https://github.com/moby/moby/pull/41622)

* Add alias for hostname if hostname != container name [moby/moby#39204](https://github.com/moby/moby/pull/39204)

* Better selection of DNS server (with systemd) [moby/moby#41022](https://github.com/moby/moby/pull/41022)

* Add docker interfaces to firewalld docker zone [moby/moby#41189](https://github.com/moby/moby/pull/41189) [moby/libnetwork#2548](https://github.com/moby/libnetwork/pull/2548)

  * Fixes DNS issue on CentOS8 [docker/for-linux#957](https://github.com/docker/for-linux/issues/957)
  * Fixes Port Forwarding on RHEL 8 with Firewalld running with FirewallBackend=nftables [moby/libnetwork#2496](https://github.com/moby/libnetwork/issues/2496)

* Fix an issue reporting 'failed to get network during CreateEndpoint' [moby/moby#41189](https://github.com/moby/moby/pull/41189) [moby/libnetwork#2554](https://github.com/moby/libnetwork/pull/2554)

* Log error instead of disabling IPv6 router advertisement failed [moby/moby#41189](https://github.com/moby/moby/pull/41189) [moby/libnetwork#2563](https://github.com/moby/libnetwork/pull/2563)

* No longer ignore `--default-address-pool` option in certain cases [moby/moby#40711](https://github.com/moby/moby/pull/40711)

* Produce an error with invalid address pool [moby/moby#40808](https://github.com/moby/moby/pull/40808) [moby/libnetwork#2538](https://github.com/moby/libnetwork/pull/2538)

* Fix `DOCKER-USER` chain not created when IPTableEnable=false [moby/moby#40808](https://github.com/moby/moby/pull/40808) [moby/libnetwork#2471](https://github.com/moby/libnetwork/pull/2471)

* Fix panic on startup in systemd environments [moby/moby#40808](https://github.com/moby/moby/pull/40808) [moby/libnetwork#2544](https://github.com/moby/libnetwork/pull/2544)

* Fix issue preventing containers to communicate over macvlan internal network [moby/moby#40596](https://github.com/moby/moby/pull/40596) [moby/libnetwork#2407](https://github.com/moby/libnetwork/pull/2407)

* Fix InhibitIPv4 nil panic [moby/moby#40596](https://github.com/moby/moby/pull/40596)

* Fix VFP leak in Windows overlay network deletion [moby/moby#40596](https://github.com/moby/moby/pull/40596) [moby/libnetwork#2524](https://github.com/moby/libnetwork/pull/2524)

### [Packaging](#packaging-9)

* docker.service: Add multi-user.target to After= in unit file [moby/moby#41297](https://github.com/moby/moby/pull/41297)
* docker.service: Allow socket activation [moby/moby#37470](https://github.com/moby/moby/pull/37470)
* seccomp: Remove dependency in dockerd on libseccomp [moby/moby#41395](https://github.com/moby/moby/pull/41395)

### [Rootless](#rootless-4)

* rootless: graduate from experimental [moby/moby#40759](https://github.com/moby/moby/pull/40759)
* Add dockerd-rootless-setuptool.sh [moby/moby#40950](https://github.com/moby/moby/pull/40950)
* Support `--exec-opt native.cgroupdriver=systemd` [moby/moby#40486](https://github.com/moby/moby/pull/40486)

### [Security](#security-2)

* Fix CVE-2019-14271 loading of nsswitch based config inside chroot under Glibc [moby/moby#39612](https://github.com/moby/moby/pull/39612)
* seccomp: Whitelist `clock_adjtime`. `CAP_SYS_TIME` is still required for time adjustment [moby/moby#40929](https://github.com/moby/moby/pull/40929)
* seccomp: Add openat2 and faccessat2 to default seccomp profile [moby/moby#41353](https://github.com/moby/moby/pull/41353)
* seccomp: allow 'rseq' syscall in default seccomp profile [moby/moby#41158](https://github.com/moby/moby/pull/41158)
* seccomp: allow syscall membarrier [moby/moby#40731](https://github.com/moby/moby/pull/40731)
* seccomp: whitelist io-uring related system calls [moby/moby#39415](https://github.com/moby/moby/pull/39415)
* Add default sysctls to allow ping sockets and privileged ports with no capabilities [moby/moby#41030](https://github.com/moby/moby/pull/41030)
* Fix seccomp profile for clone syscall [moby/moby#39308](https://github.com/moby/moby/pull/39308)

### [Swarm](#swarm-4)

* Add support for swarm jobs [moby/moby#40307](https://github.com/moby/moby/pull/40307)
* Add capabilities support to stack/service commands [docker/cli#2687](https://github.com/docker/cli/pull/2687) [docker/cli#2709](https://github.com/docker/cli/pull/2709) [moby/moby#39173](https://github.com/moby/moby/pull/39173) [moby/moby#41249](https://github.com/moby/moby/pull/41249)
* Add support for sending down service Running and Desired task counts [moby/moby#39231](https://github.com/moby/moby/pull/39231)
* service: support `--mount type=bind,bind-nonrecursive` [moby/moby#38788](https://github.com/moby/moby/pull/38788)
* Support ulimits on Swarm services. [moby/moby#41284](https://github.com/moby/moby/pull/41284) [docker/cli#2712](https://github.com/docker/cli/pull/2712)
* Fixed an issue where service logs could leak goroutines on the worker [moby/moby#40426](https://github.com/moby/moby/pull/40426)

----
url: https://docs.docker.com/reference/api/engine/version/v1.44.yaml
----

basePath: "/v1.44"
info:
 title: "Docker Engine API"
 version: "1.44"

 If you omit the version-prefix, the current version of the API (v1.44) is used.
 For example, calling \`/info\` is the same as calling \`/v1.44/info\`. Using the

 (unless NonRecursive is set to true in conjunction).
 type: "boolean"
 default: false
 ReadOnlyForceRecursive:
 description: "Raise an error if the mount cannot be made recursively read-only."
 type: "boolean"
 default: false
 VolumeOptions:
 description: "Optional configuration for the \`volume\` type."
 type: "object"
 properties:
 NoCopy:
 description: "Populate volume with data from the target."
 type: "boolean"
 default: false
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 DriverConfig:
 description: "Map of driver specific options"
 type: "object"
 properties:
 Name:
 description: "Name of the driver to use to create the volume."
 type: "string"
 Options:
 description: "key/value map of driver specific options."
 type: "object"
 additionalProperties:
 type: "string"


 When used as \`ContainerConfig\` field in an image, \`ContainerConfig\` is an
 optional field containing the configuration of the container that was last
 committed when creating the image.

 Previous versions of Docker builder used this field to store build cache,
 and it is not in active use anymore.

 Container:
 description: \|
 The ID of the container that was used to create the image.

 Depending on how the image was created, this field may be empty.

 \*\*Deprecated\*\*: this field is kept for backward compatibility, but
 will be removed in API v1.45.
 type: "string"
 example: "65974bc86f1770ae4bff79f651ebdbce166ae9aada632ee3fa9af3a264911735"
 ContainerConfig:
 description: \|
 \*\*Deprecated\*\*: this field is kept for backward compatibility, but
 will be removed in API v1.45.
 $ref: "#/definitions/ContainerConfig"

 \> \*\*Deprecated\*\*: This field is deprecated and will always\
 \> be "false" in future.\
 type: "boolean"\
 example: false\
 name:\
 type: "string"\
 star\_count:\
 type: "integer"\
 examples:\
 application/json:\
 \- description: "A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size!"\
 is\_official: true\
 is\_automated: false\
 name: "alpine"\
 star\_count: 10093\
 \- description: "Busybox base image."\
 is\_official: true\
 is\_automated: false\
 name: "Busybox base image."\
 star\_count: 3037\
 \- description: "The PostgreSQL object-relational database system provides reliability and data integrity."\
 is\_official: true\
 is\_automated: false\
 name: "postgres"\
 star\_count: 12408\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "term"\
 in: "query"\
 description: "Term to search"\
 type: "string"\
 required: true\
 \- name: "limit"\
 in: "query"\
 description: "Maximum number of results to return"\
 type: "integer"\
 \- name: "filters"\
 in: "query"\
 description: \|\
 A JSON encoded value of the filters (a \`map\[string\]\[\]string\`) to process on the images list. Available filters:\
\
 \- \`is-automated=(true\|false)\` (deprecated, see below)\
 \- \`is-official=(true\|false)\`\
 \- \`stars=\` Matches images that has at least 'number' stars.\
\
 The \`is-automated\` filter is deprecated. The \`is\_automated\` field has\
 been deprecated by Docker Hub's search API. Consequently, searching\
 for \`is-automated=true\` will yield no results.\

----
url: https://docs.docker.com/reference/cli/docker/trust/signer/
----

# docker trust signer

***

| Description | Manage entities who can sign Docker images |
| ----------- | ------------------------------------------ |
| Usage       | `docker trust signer`                      |

## [Description](#description)

Manage entities who can sign Docker images

## [Subcommands](#subcommands)

| Command                                                                                           | Description     |
| ------------------------------------------------------------------------------------------------- | --------------- |
| [`docker trust signer add`](https://docs.docker.com/reference/cli/docker/trust/signer/add/)       | Add a signer    |
| [`docker trust signer remove`](https://docs.docker.com/reference/cli/docker/trust/signer/remove/) | Remove a signer |

----
url: https://docs.docker.com/scout/integrations/environment/
----

# Integrating Docker Scout with environments

***

Table of contents

***

You can integrate Docker Scout with your runtime environments, and get insights for your running workloads. This gives you a real-time view of your security status for your deployed artifacts.

Docker Scout lets you define multiple environments, and assign images to different environments. This gives you a complete overview of your software supply chain, and lets you view and compare deltas between environments, for example staging and production.

How you define and name your environments is up to you. You can use patterns that are meaningful to you and that matches how you ship your applications.

## [Assign to environments](#assign-to-environments)

Each environment contains references to a number of images. These references represent containers currently running in that particular environment.

For example, say you're running `myorg/webapp:3.1` in production, you can assign that tag to your `production` environment. You might be running a different version of the same image in staging, in which case you can assign that version of the image to the `staging` environment.

To add environments to Docker Scout, you can:

* Use the `docker scout env <environment> <image>` CLI command to record images to environments manually
* Enable a runtime integration to automatically detect images in your environments.

Docker Scout supports the following runtime integrations:

* [Docker Scout GitHub Action](https://github.com/marketplace/actions/docker-scout#record-an-image-deployed-to-an-environment)
* [CLI client](https://docs.docker.com/scout/integrations/environment/cli/)
* [Sysdig integration](https://docs.docker.com/scout/integrations/environment/sysdig/)

> Note
>
> Only organization owners can create new environments and set up integrations. Additionally, Docker Scout only assigns an image to an environment if the image [has been analyzed](https://docs.docker.com/scout/explore/analysis/), either manually or through a [registry integration](https://docs.docker.com/scout/integrations/#container-registries).

## [List environments](#list-environments)

To see all of the available environments for an organization, you can use the `docker scout env` command.

```console
$ docker scout env
```

By default, this prints all environments for your personal Docker organization. To list environments for another organization that you're a part of, use the `--org` flag.

```console
$ docker scout env --org <org>
```

You can use the `docker scout config` command to change the default organization. This changes the default organization for all `docker scout` commands, not just `env`.

```console
$ docker scout config organization <org>
```

## [Comparing between environments](#comparing-between-environments)

Assigning images to environments lets you make comparisons with and between environments. This is useful for things like GitHub pull requests, for comparing the image built from the code in the PR to the corresponding image in staging or production.

You can also compare with streams using the `--to-env` flag on the [`docker scout compare`](/reference/cli/docker/scout/compare/) CLI command:

```console
$ docker scout compare --to-env production myorg/webapp:latest
```

## [View images for an environment](#view-images-for-an-environment)

To view the images for an environment:

1. Go to the [Images page](https://scout.docker.com/) in the Docker Scout Dashboard.
2. Open the **Environments** drop-down menu.
3. Select the environment that you want to view.

The list displays all images that have been assigned to the selected environment. If you've deployed multiple versions of the same image in an environment, all versions of the image appear in the list.

Alternatively, you can use the `docker scout env` command to view the images from the terminal.

```console
$ docker scout env production
docker/scout-demo-service:main@sha256:ef08dca54c4f371e7ea090914f503982e890ec81d22fd29aa3b012351a44e1bc
```

### [Mismatching image tags](#mismatching-image-tags)

When you've selected an environment on the **Images** tab, tags in the list represent the tag that was used to deploy the image. Tags are mutable, meaning that you can change the image digest that a tag refers to. If Docker Scout detects that a tag refers to an outdated digest, a warning icon displays next to the image name.

----
url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/
----

# Docker MCP Catalog and Toolkit

***

Table of contents

***

Availability: Beta

[Model Context Protocol](https://modelcontextprotocol.io/introduction) (MCP) is an open protocol that standardizes how AI applications access external tools and data sources. By connecting LLMs to local development tools, databases, APIs, and other resources, MCP extends their capabilities beyond their base training.

The challenge is that running MCP servers locally creates operational friction. Each server requires separate installation and configuration for every application you use. You run untrusted code directly on your machine, manage updates manually, and troubleshoot dependency conflicts yourself. Configure a GitHub server for Claude, then configure it again for Cursor, and so on. Each time you manage credentials, permissions, and environment setup.

## [Docker MCP features](#docker-mcp-features)

The [MCP Toolkit](/ai/mcp-catalog-and-toolkit/toolkit/) and [MCP Gateway](/ai/mcp-catalog-and-toolkit/mcp-gateway/) solve these challenges through centralized management. Instead of configuring each server for every AI application separately, you set things up once and connect all your clients to it. The workflow centers on three concepts: catalogs, profiles, and clients.

[Catalogs](/ai/mcp-catalog-and-toolkit/catalog/) are curated collections of MCP servers. The Docker MCP Catalog provides 300+ verified servers packaged as container images with versioning, provenance, and security updates. Organizations can create [custom catalogs](/ai/mcp-catalog-and-toolkit/catalog/#custom-catalogs) with approved servers for their teams.

[Profiles](/ai/mcp-catalog-and-toolkit/profiles/) organize servers into named collections for different projects. Your "web-dev" profile might use GitHub and Playwright; your "backend" profile, database tools. Profiles support both containerized servers from catalogs and remote MCP servers. Configure a profile once, then share it across clients or with your team.

Clients are the AI applications that connect to your profiles. Claude Code, Cursor, Zed, and others connect through the MCP Gateway, which routes requests to the right server and handles authentication and lifecycle management.

## [Learn more](#learn-more)

### [Get started with MCP Toolkit](/ai/mcp-catalog-and-toolkit/get-started/)

[Learn how to quickly install and use the MCP Toolkit to set up servers and clients.](/ai/mcp-catalog-and-toolkit/get-started/)

### [MCP Catalog](/ai/mcp-catalog-and-toolkit/catalog/)

[Browse Docker's curated collection of verified MCP servers](/ai/mcp-catalog-and-toolkit/catalog/)

### [MCP Profiles](/ai/mcp-catalog-and-toolkit/profiles/)

[Organize servers into profiles for different projects and share configurations](/ai/mcp-catalog-and-toolkit/profiles/)

### [MCP Toolkit](/ai/mcp-catalog-and-toolkit/toolkit/)

[Use Docker Desktop's UI to discover, configure, and manage MCP servers](/ai/mcp-catalog-and-toolkit/toolkit/)

### [MCP Gateway](/ai/mcp-catalog-and-toolkit/mcp-gateway/)

[Use the CLI and Gateway to run MCP servers with custom configurations](/ai/mcp-catalog-and-toolkit/mcp-gateway/)

### [Dynamic MCP](/ai/mcp-catalog-and-toolkit/dynamic-mcp/)

[Discover and add MCP servers on-demand using natural language](/ai/mcp-catalog-and-toolkit/dynamic-mcp/)

### [Docker Hub MCP server](/ai/mcp-catalog-and-toolkit/hub-mcp/)

[Use the Docker Hub MCP server to search images and manage repositories](/ai/mcp-catalog-and-toolkit/hub-mcp/)

### [Security FAQs](/ai/mcp-catalog-and-toolkit/faqs/)

[Common questions about MCP security, credentials, and server verification](/ai/mcp-catalog-and-toolkit/faqs/)

### [E2B sandboxes](/ai/mcp-catalog-and-toolkit/e2b-sandboxes/)

[Cloud sandboxes for AI agents with built-in MCP Catalog access](/ai/mcp-catalog-and-toolkit/e2b-sandboxes/)

----
url: https://docs.docker.com/guides/admin-user-management/onboard/
----

# Onboarding and managing roles and permissions in Docker

***

Table of contents

***

This page guides you through onboarding owners and members, and using tools like SSO and SCIM to future-proof onboarding going forward.

## [Invite owners](#invite-owners)

When you create a Docker organization, you automatically become its sole owner. While optional, adding additional owners can significantly ease the process of onboarding and managing your organization by distributing administrative responsibilities. It also ensures continuity and prevents blockers if the primary owner is unavailable.

For detailed information on owners, see [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

## [Invite members and assign roles](#invite-members-and-assign-roles)

Members are granted controlled access to resources and enjoy enhanced organizational benefits. When you invite members to join your Docker organization, you immediately assign them a role.

### [Benefits of inviting members](#benefits-of-inviting-members)

* Enhanced visibility: Gain insights into user activity, making it easier to monitor access and enforce security policies.
* Streamlined collaboration: Help members collaborate effectively by granting access to shared resources and repositories.
* Improved resource management: Organize and track users within your organization, ensuring optimal allocation of resources.
* Access to enhanced features: Members benefit from organization-wide perks, such as increased pull limits and access to premium Docker features.
* Security control: Apply and enforce security settings at an organizational level, reducing risks associated with unmanaged accounts.

For detailed information, see [Manage organization members](https://docs.docker.com/admin/organization/manage/members/).

## [Future-proof user management](#future-proof-user-management)

A robust, future-proof approach to user management combines automated provisioning, centralized authentication, and dynamic access control. Implementing these practices ensures a scalable, secure, and efficient environment.

### [Secure user authentication with single sign-on (SSO)](#secure-user-authentication-with-single-sign-on-sso)

Integrating Docker with your identity provider streamlines user access and enhances security.

SSO:

* Simplifies sign in, as users sign in with their organizational credentials.
* Reduces password-related vulnerabilities.
* Simplifies onboarding as it works seamlessly with SCIM and group mapping for automated provisioning.

For more information, see the [SSO documentation](https://docs.docker.com/enterprise/security/single-sign-on/).

### [Automate onboarding with SCIM and JIT provisioning](#automate-onboarding-with-scim-and-jit-provisioning)

Streamline user provisioning and role management with [SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) and [Just-in-Time (JIT) provisioning](https://docs.docker.com/enterprise/security/provisioning/just-in-time/).

With SCIM you can:

* Sync users and roles automatically with your identity provider.
* Automate adding, updating, or removing users based on directory changes.

With JIT provisioning you can:

* Automatically add users upon first sign in based on [group mapping](#simplify-access-with-group-mapping).
* Reduce overhead by eliminating pre-invite steps.

### [Simplify access with group mapping](#simplify-access-with-group-mapping)

Group mapping automates permissions management by linking identity provider groups to Docker roles and teams.

It also:

* Reduces manual errors in role assignments.
* Ensures consistent access control policies.
* Help you scale permissions as teams grow or change.

For more information on how it works, see [Group mapping](https://docs.docker.com/enterprise/security/provisioning/scim/group-mapping/).

[Monitoring and insights »](https://docs.docker.com/guides/admin-user-management/audit-and-monitor/)

----
url: https://docs.docker.com/guides/cpp/configure-ci-cd/
----

# Configure CI/CD for your C++ application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize a C++ application](https://docs.docker.com/guides/cpp/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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

Set up your GitHub Actions workflow for building, testing, and pushing the image to Docker Hub.

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
         - name: Login to Docker Hub
           uses: docker/login-action@v4
           with:
             username: ${{ vars.DOCKER_USERNAME }}
             password: ${{ secrets.DOCKERHUB_TOKEN }}

         - name: Set up Docker Buildx
           uses: docker/setup-buildx-action@v4

         - name: Build and push
           uses: docker/build-push-action@v7
           with:
             platforms: linux/amd64,linux/arm64
             push: true
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

In this section, you learned how to set up a GitHub Actions workflow for your C++ application.

Related information:

* [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
* [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
* [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## [Next steps](#next-steps)

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

[Test your C++ deployment »](https://docs.docker.com/guides/cpp/deploy/)

----
url: https://docs.docker.com/engine/extend/legacy_plugins/
----

# Use Docker Engine plugins

***

Table of contents

***

This document describes the Docker Engine plugins generally available in Docker Engine. To view information on plugins managed by Docker, refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

> Note
>
> Legacy plugins are superseded by Docker Engine's managed plugin system. For plugins installed and managed by Docker, use [`docker plugin install`](https://docs.docker.com/reference/cli/docker/plugin/install/) and the [Docker Engine plugin system](https://docs.docker.com/engine/extend/). The third-party plugins listed on this page are provided for historical reference, and archived projects are marked accordingly.

You can extend the capabilities of the Docker Engine by loading third-party plugins. This page explains the types of plugins and provides links to several volume and network plugins for Docker.

## [Types of plugins](#types-of-plugins)

Plugins extend Docker's functionality. They come in specific types. For example, a [volume plugin](https://docs.docker.com/engine/extend/plugins_volume/) might enable Docker volumes to persist across multiple Docker hosts and a [network plugin](https://docs.docker.com/engine/extend/plugins_network/) might provide network plumbing.

Currently Docker supports authorization, volume and network driver plugins. In the future it will support additional plugin types.

## [Installing a plugin](#installing-a-plugin)

Follow the instructions in the plugin's documentation.

## [Finding a plugin](#finding-a-plugin)

The sections below provide an overview of third-party plugins that use the legacy plugin model.

### [Network plugins](#network-plugins)

| Plugin                                                                      | Description                                                                                                                                                                                                                                                                                              |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Contiv Networking](https://github.com/contiv/netplugin)                    | An open source network plugin to provide infrastructure and security policies for a multi-tenant micro services deployment, while providing an integration to physical network for non-container workload. Contiv Networking implements the remote driver and IPAM APIs available in Docker 1.9 onwards. |
| [Kuryr Network Plugin](https://github.com/openstack/kuryr)                  | A network plugin is developed as part of the OpenStack Kuryr project and implements the Docker networking (libnetwork) remote driver API by utilizing Neutron, the OpenStack networking service. It includes an IPAM driver as well.                                                                     |
| [Kathará Network Plugin](https://github.com/KatharaFramework/NetworkPlugin) | Docker Network Plugin used by Kathará, an open source container-based network emulation system for showing interactive demos/lessons, testing production networks in a sandbox environment, or developing new network protocols.                                                                         |

### [Volume plugins](#volume-plugins)

| Plugin                                                                                                     | Description                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Azure File Storage plugin](https://github.com/Azure/azurefile-dockervolumedriver) (archived)              | Lets you mount Microsoft [Azure File Storage](https://azure.microsoft.com/blog/azure-file-storage-now-generally-available/) shares to Docker containers as volumes using the SMB 3.0 protocol. [Learn more](https://azure.microsoft.com/blog/persistent-docker-volumes-with-azure-file-storage/).             |
| [BeeGFS Volume Plugin](https://github.com/RedCoolBeans/docker-volume-beegfs)                               | An open source volume plugin to create persistent volumes in a BeeGFS parallel file system.                                                                                                                                                                                                                   |
| [Blockbridge plugin](https://github.com/blockbridge/blockbridge-docker-volume)                             | A volume plugin that provides access to an extensible set of container-based persistent storage options. It supports single and multi-host Docker environments with features that include tenant isolation, automated provisioning, encryption, secure deletion, snapshots and QoS.                           |
| [Contiv Volume Plugin](https://github.com/contiv/volplugin)                                                | An open source volume plugin that provides multi-tenant, persistent, distributed storage with intent based consumption. It has support for Ceph and NFS.                                                                                                                                                      |
| [Convoy plugin](https://github.com/rancher/convoy) (archived)                                              | A volume plugin for a variety of storage back-ends including device mapper and NFS. It's a simple standalone executable written in Go and provides the framework to support vendor-specific extensions such as snapshots, backups and restore.                                                                |
| [DigitalOcean Block Storage plugin](https://github.com/omallo/docker-volume-plugin-dostorage)              | Integrates DigitalOcean's [block storage solution](https://www.digitalocean.com/products/storage/) into the Docker ecosystem by automatically attaching a given block storage volume to a DigitalOcean droplet and making the contents of the volume available to Docker containers running on that droplet.  |
| [DRBD plugin](https://www.drbd.org/en/supported-projects/docker)                                           | A volume plugin that provides highly available storage replicated by [DRBD](https://www.drbd.org). Data written to the docker volume is replicated in a cluster of DRBD nodes.                                                                                                                                |
| [Flocker plugin](https://github.com/ScatterHQ/flocker) (archived)                                          | A volume plugin that provides multi-host portable volumes for Docker, enabling you to run databases and other stateful containers and move them around across a cluster of machines.                                                                                                                          |
| [Fuxi Volume Plugin](https://github.com/openstack-archive/fuxi) (archived)                                 | A volume plugin that is developed as part of the OpenStack Kuryr project and implements the Docker volume plugin API by utilizing Cinder, the OpenStack block storage service.                                                                                                                                |
| [gce-docker plugin](https://github.com/mcuadros/gce-docker) (archived)                                     | A volume plugin able to attach, format and mount Google Compute [persistent-disks](https://cloud.google.com/compute/docs/disks/persistent-disks).                                                                                                                                                             |
| [GlusterFS plugin](https://github.com/calavera/docker-volume-glusterfs) (archived)                         | A volume plugin that provides multi-host volumes management for Docker using GlusterFS.                                                                                                                                                                                                                       |
| [Horcrux Volume Plugin](https://github.com/muthu-r/horcrux)                                                | A volume plugin that allows on-demand, version controlled access to your data. Horcrux is an open-source plugin, written in Go, and supports SCP, [Minio](https://www.minio.io) and Amazon S3.                                                                                                                |
| [HPE 3Par Volume Plugin](https://github.com/hpe-storage/python-hpedockerplugin/)                           | A volume plugin that supports HPE 3Par and StoreVirtual iSCSI storage arrays.                                                                                                                                                                                                                                 |
| [IPFS Volume Plugin](https://github.com/vdemeester/docker-volume-ipfs) (archived)                          | An open source volume plugin that allows using an [ipfs](https://ipfs.io/) filesystem as a volume.                                                                                                                                                                                                            |
| [Keywhiz plugin](https://github.com/calavera/docker-volume-keywhiz) (archived)                             | A plugin that provides credentials and secret management using Keywhiz as a central repository.                                                                                                                                                                                                               |
| [Linode Volume Plugin](https://github.com/linode/docker-volume-linode)                                     | A plugin that adds the ability to manage Linode Block Storage as Docker Volumes from within a Linode.                                                                                                                                                                                                         |
| [Local Persist Plugin](https://github.com/CWSpear/local-persist)                                           | A volume plugin that extends the default `local` driver's functionality by allowing you specify a mountpoint anywhere on the host, which enables the files to *always persist*, even if the volume is removed via `docker volume rm`.                                                                         |
| [NetApp Plugin](https://github.com/NetApp/netappdvp) (nDVP)                                                | A volume plugin that provides direct integration with the Docker ecosystem for the NetApp storage portfolio. The nDVP package supports the provisioning and management of storage resources from the storage platform to Docker hosts, with a robust framework for adding additional platforms in the future. |
| [Netshare plugin](https://github.com/ContainX/docker-volume-netshare)                                      | A volume plugin that provides volume management for NFS 3/4, AWS EFS and CIFS file systems.                                                                                                                                                                                                                   |
| [Nimble Storage Volume Plugin](https://scod.hpedev.io/docker_volume_plugins/hpe_nimble_storage/index.html) | A volume plug-in that integrates with Nimble Storage Unified Flash Fabric arrays. The plug-in abstracts array volume capabilities to the Docker administrator to allow self-provisioning of secure multi-tenant volumes and clones.                                                                           |
| [OpenStorage Plugin](https://github.com/libopenstorage/openstorage)                                        | A cluster-aware volume plugin that provides volume management for file and block storage solutions. It implements a vendor neutral specification for implementing extensions such as CoS, encryption, and snapshots. It has example drivers based on FUSE, NFS, NBD and EBS to name a few.                    |
| [Portworx Volume Plugin](https://github.com/portworx/px-dev)                                               | A volume plugin that turns any server into a scale-out converged compute/storage node, providing container granular storage and highly available volumes across any node, using a shared-nothing storage backend that works with any docker scheduler.                                                        |
| [Quobyte Volume Plugin](https://github.com/quobyte/docker-volume)                                          | A volume plugin that connects Docker to [Quobyte](https://www.quobyte.com/containers)'s data center file system, a general-purpose scalable and fault-tolerant storage platform.                                                                                                                              |
| [REX-Ray plugin](https://github.com/emccode/rexray)                                                        | A volume plugin which is written in Go and provides advanced storage functionality for many platforms including VirtualBox, EC2, Google Compute Engine, OpenStack, and EMC.                                                                                                                                   |
| [Virtuozzo Storage and Ploop plugin](https://github.com/virtuozzo/docker-volume-ploop)                     | A volume plugin with support for Virtuozzo Storage distributed cloud file system as well as ploop devices.                                                                                                                                                                                                    |
| [VMware vSphere Storage Plugin](https://github.com/vmware/docker-volume-vsphere)                           | Docker Volume Driver for vSphere enables customers to address persistent storage requirements for Docker containers in vSphere environments.                                                                                                                                                                  |

### [Authorization plugins](#authorization-plugins)

| Plugin                                                               | Description                                                                                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Casbin AuthZ Plugin](https://github.com/casbin/casbin-authz-plugin) | An authorization plugin based on [Casbin](https://github.com/casbin/casbin), which supports access control models like ACL, RBAC, ABAC. The access control model can be customized. The policy can be persisted into file or DB.                                                                                                     |
| [HBM plugin](https://github.com/kassisol/hbm)                        | An authorization plugin that prevents from executing commands with certains parameters.                                                                                                                                                                                                                                              |
| [Twistlock AuthZ Broker](https://github.com/twistlock/authz)         | A basic extendable authorization plugin that runs directly on the host or inside a container. This plugin allows you to define user policies that it evaluates during authorization. Basic authorization is provided if Docker daemon is started with the --tlsverify flag (username is extracted from the certificate common name). |

## [Troubleshooting a plugin](#troubleshooting-a-plugin)

If you are having problems with Docker after loading a plugin, ask the authors of the plugin for help. The Docker team may not be able to assist you.

## [Writing a plugin](#writing-a-plugin)

If you are interested in writing a plugin for Docker, or seeing how they work under the hood, see the [Docker plugins reference](https://docs.docker.com/engine/extend/plugin_api/).

----
url: https://docs.docker.com/build/bake/introduction/
----

# Introduction to Bake

***

Table of contents

***

Bake is an abstraction for the `docker build` command that lets you more easily manage your build configuration (CLI flags, environment variables, etc.) in a consistent way for everyone on your team.

Bake is a command built into the Buildx CLI, so as long as you have Buildx installed, you also have access to bake, via the `docker buildx bake` command.

## [Building a project with Bake](#building-a-project-with-bake)

Here's a simple example of a `docker build` command:

```console
$ docker build -f Dockerfile -t myapp:latest .
```

This command builds the Dockerfile in the current directory and tags the resulting image as `myapp:latest`.

To express the same build configuration using Bake:

docker-bake.hcl

```hcl
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
}
```

Bake provides a structured way to manage your build configuration, and it saves you from having to remember all the CLI flags for `docker build` every time. With this file, building the image is as simple as running:

```console
$ docker buildx bake myapp
```

For simple builds, the difference between `docker build` and `docker buildx bake` is minimal. However, as your build configuration grows more complex, Bake provides a more structured way to manage that complexity, that would be difficult to manage with CLI flags for the `docker build`. It also provides a way to share build configurations across your team, so that everyone is building images in a consistent way, with the same configuration.

## [The Bake file format](#the-bake-file-format)

You can write Bake files in HCL or JSON. Bake can also read [Docker Compose files](https://docs.docker.com/build/bake/compose-file/) and translate each service to a build target. HCL is the most expressive and flexible format, which is why you'll see it used in most of the examples in this documentation, and in projects that use Bake.

The properties that can be set for a target closely resemble the CLI flags for `docker build`. For instance, consider the following `docker build` command:

```console
$ docker build \
  -f Dockerfile \
  -t myapp:latest \
  --build-arg foo=bar \
  --no-cache \
  --platform linux/amd64,linux/arm64 \
  .
```

The Bake equivalent would be:

docker-bake.hcl

```hcl
target "myapp" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["myapp:latest"]
  args = {
    foo = "bar"
  }
  no-cache = true
  platforms = ["linux/amd64", "linux/arm64"]
}
```

> Tip
>
> Want a better editing experience for Bake files in VS Code? Check out the [Docker DX](https://marketplace.visualstudio.com/items?itemName=docker.docker) extension for linting, code navigation, and vulnerability scanning.

## [Next steps](#next-steps)

To learn more about using Bake, see the following topics:

* Learn how to define and use [targets](https://docs.docker.com/build/bake/targets/) in Bake
* To see all the properties that can be set for a target, refer to the [Bake file reference](/build/bake/reference/).

----
url: https://docs.docker.com/guides/angular/
----

# Angular language-specific guide

Table of contents

***

This guide explains how to containerize Angular applications using Docker.

**Time to complete** 20 minutes

The Angular language-specific guide shows you how to containerize an Angular application using Docker, following best practices for creating efficient, production-ready containers.

[Angular](https://angular.dev/) is a robust and widely adopted framework for building dynamic, enterprise-grade web applications. However, managing dependencies, environments, and deployments can become complex as applications scale. Docker streamlines these challenges by offering a consistent, isolated environment for development and production.

> **Acknowledgment**
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide. As a Docker Captain and experienced Front-end engineer, his expertise in Docker, DevOps, and modern web development has made this resource essential for the community, helping developers navigate and optimize their Docker workflows.

***

## [What will you learn?](#what-will-you-learn)

In this guide, you will learn how to:

* Containerize and run an Angular application using Docker.
* Set up a local development environment for Angular inside a container.
* Run tests for your Angular application within a Docker container.
* Configure a CI/CD pipeline using GitHub Actions for your containerized app.
* Deploy the containerized Angular application to a local Kubernetes cluster for testing and debugging.

You'll start by containerizing an existing Angular application and work your way up to production-level deployments.

***

## [Prerequisites](#prerequisites)

Before you begin, ensure you have a working knowledge of:

* Basic understanding of [TypeScript](https://www.typescriptlang.org/) and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
* Familiarity with [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm) for managing dependencies and running scripts.
* Familiarity with [Angular](https://angular.io/) fundamentals.
* Understanding of core Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

Once you've completed the Angular getting started modules, you’ll be fully prepared to containerize your own Angular application using the detailed examples and best practices outlined in this guide.

## [Modules](#modules)

1. [Containerize](https://docs.docker.com/guides/angular/containerize/)

   Learn how to containerize an Angular application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.

2. [Develop your app](https://docs.docker.com/guides/angular/develop/)

   Learn how to develop your Angular application locally using containers.

3. [Run your tests](https://docs.docker.com/guides/angular/run-tests/)

   Learn how to run your Angular tests in a container.

4. [GitHub Actions CI](https://docs.docker.com/guides/angular/configure-github-actions/)

   Learn how to configure CI/CD using GitHub Actions for your Angular application.

5. [Test your deployment](https://docs.docker.com/guides/angular/deploy/)

   Learn how to deploy locally to test and debug your Kubernetes deployment

----
url: https://docs.docker.com/scout/policy/
----

# Get started with Policy Evaluation in Docker Scout

***

Table of contents

***

In software supply chain management, maintaining the security and reliability of artifacts is a top priority. Policy Evaluation in Docker Scout introduces a layer of control, on top of existing analysis capabilities. It lets you define supply chain rules for your artifacts, and helps you track how your artifacts perform, relative to your rules and thresholds, over time.

Learn how you can use Policy Evaluation to ensure that your artifacts align with established best practices.

## [How Policy Evaluation works](#how-policy-evaluation-works)

When you activate Docker Scout for a repository, images that you push are [automatically analyzed](https://docs.docker.com/scout/explore/analysis/). The analysis gives you insights about the composition of your images, including what packages they contain and what vulnerabilities they're exposed to. Policy Evaluation builds on top of the image analysis feature, interpreting the analysis results against the rules defined by policies.

A policy defines image quality criteria that your artifacts should fulfill. For example, the **No AGPL v3 licenses** policy flags any image containing packages distributed under the AGPL v3 license. If an image contains such a package, that image is non-compliant with this policy. Some policies, such as the **No AGPL v3 licenses** policy, are configurable. Configurable policies let you adjust the criteria to better match your organization's needs.

In Docker Scout, policies are designed to help you ratchet forward your security and supply chain stature. Where other tools focus on providing a pass or fail status, Docker Scout policies visualizes how small, incremental changes affect policy status, even when your artifacts don't meet the policy requirements (yet). By tracking how the fail gap changes over time, you more easily see whether your artifact is improving or deteriorating relative to policy.

Policies don't necessarily have to be related to application security and vulnerabilities. You can use policies to measure and track other aspects of supply chain management as well, such as open-source license usage and base image up-to-dateness.

## [Policy types](#policy-types)

In Docker Scout, a *policy* is derived from a *policy type*. Policy types are templates that define the core parameters of a policy. You can compare policy types to classes in object-oriented programming, with each policy acting as an instance created from its corresponding policy type.

Docker Scout supports the following policy types:

* [Severity-Based Vulnerability](#severity-based-vulnerability)
* [Compliant Licenses](#compliant-licenses)
* [Up-to-Date Base Images](#up-to-date-base-images)
* [High-Profile Vulnerabilities](#high-profile-vulnerabilities)
* [Supply Chain Attestations](#supply-chain-attestations)
* [Default Non-Root User](#default-non-root-user)
* [Approved Base Images](#approved-base-images)
* [SonarQube Quality Gates](#sonarqube-quality-gates)
* [Valid Docker Hardened Image (DHI) or DHI base image](#valid-docker-hardened-image-dhi-or-dhi-base-image)

Docker Scout automatically provides default policies for repositories where it is enabled, except for the following policies, which are optional and must be configured:

* The **SonarQube Quality Gates** policy, which requires [integration with SonarQube](https://docs.docker.com/scout/integrations/code-quality/sonarqube/) before use.
* The **Valid Docker Hardened Image (DHI) or DHI base image** policy, which can be configured if you want to enforce the use of Docker Hardened Images.

You can create custom policies from any of the supported policy types, or delete a default policy if it isn't applicable to your project. For more information, refer to [Configure policies](https://docs.docker.com/scout/policy/configure/).

### [Severity-Based Vulnerability](#severity-based-vulnerability)

The **Severity-Based Vulnerability** policy type checks whether your artifacts are exposed to known vulnerabilities.

By default, this policy only flags critical and high severity vulnerabilities where there's a fix version available. Essentially, this means that there's an easy fix that you can deploy for images that fail this policy: upgrade the vulnerable package to a version containing a fix for the vulnerability.

Images are deemed non-compliant with this policy if they contain one or more vulnerabilities that fall outside the specified policy criteria.

You can configure the parameters of this policy by creating a custom version of the policy. The following policy parameters are configurable in a custom version:

* **Age**: The minimum number of days since the vulnerability was first published

  The rationale for only flagging vulnerabilities of a certain minimum age is that newly discovered vulnerabilities shouldn't cause your evaluations to fail until you've had a chance to address them.

- **Severities**: Severity levels to consider (default: `Critical, High`)

* **Fixable vulnerabilities only**: Whether or not to only report vulnerabilities with a fix version available (enabled by default).

* **Package types**: List of package types to consider.

  This option lets you specify the package types, as [PURL package type definitions](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst), that you want to include in the policy evaluation. By default, the policy considers all package types.

For more information about configuring policies, see [Configure policies](https://docs.docker.com/scout/policy/configure/).

### [Compliant Licenses](#compliant-licenses)

The **Compliant Licenses** policy type checks whether your images contain packages distributed under an inappropriate license. Images are considered non-compliant if they contain one or more packages with such a license.

You can configure the list of licenses that this policy should look out for, and add exceptions by specifying an allow-list (in the form of PURLs). See [Configure policies](https://docs.docker.com/scout/policy/configure/).

### [Up-to-Date Base Images](#up-to-date-base-images)

The **Up-to-Date Base Images** policy type checks whether the base images you use are up-to-date.

Images are considered non-compliant with this policy if the tag you used to build your image points to a different digest than what you're using. If there's a mismatch in digests, that means the base image you're using is out of date.

Your images need provenance attestations for this policy to successfully evaluate. For more information, see [No base image data](#no-base-image-data).

### [High-Profile Vulnerabilities](#high-profile-vulnerabilities)

The **High-Profile Vulnerabilities** policy type checks whether your images contain vulnerabilities from Docker Scout’s curated list. This list is kept up-to-date with newly disclosed vulnerabilities that are widely recognized to be risky.

The list includes the following vulnerabilities:

* [CVE-2014-0160 (OpenSSL Heartbleed)](https://scout.docker.com/v/CVE-2014-0160)
* [CVE-2021-44228 (Log4Shell)](https://scout.docker.com/v/CVE-2021-44228)
* [CVE-2023-38545 (cURL SOCKS5 heap buffer overflow)](https://scout.docker.com/v/CVE-2023-38545)
* [CVE-2023-44487 (HTTP/2 Rapid Reset)](https://scout.docker.com/v/CVE-2023-44487)
* [CVE-2024-3094 (XZ backdoor)](https://scout.docker.com/v/CVE-2024-3094)
* [CVE-2024-47176 (OpenPrinting - `cups-browsed`)](https://scout.docker.com/v/CVE-2024-47176)
* [CVE-2024-47076 (OpenPrinting - `libcupsfilters`)](https://scout.docker.com/v/CVE-2024-47076)
* [CVE-2024-47175 (OpenPrinting - `libppd`)](https://scout.docker.com/v/CVE-2024-47175)
* [CVE-2024-47177 (OpenPrinting - `cups-filters`)](https://scout.docker.com/v/CVE-2024-47177)

You can customize this policy to change which CVEs that are considered high-profile by configuring the policy. Custom configuration options include:

* **Excluded CVEs**: Specify the CVEs that you want this policy to ignore.

  Default: `[]` (none of the high-profile CVEs are ignored)

* **CISA KEV**: Enable tracking of vulnerabilities from CISA's Known Exploited Vulnerabilities (KEV) catalog

  The [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) includes vulnerabilities that are actively exploited in the wild. When enabled, the policy flags images that contain vulnerabilities from the CISA KEV catalog.

  Enabled by default.

For more information on policy configuration, see [Configure policies](https://docs.docker.com/scout/policy/configure/).

### [Supply Chain Attestations](#supply-chain-attestations)

The **Supply Chain Attestations** policy type checks whether your images have [SBOM](https://docs.docker.com/build/metadata/attestations/sbom/) and [provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) attestations.

Images are considered non-compliant if they lack either an SBOM attestation or a provenance attestation with *max mode* provenance. To ensure compliance, update your build command to attach these attestations at build-time:

```console
$ docker buildx build --provenance=true --sbom=true -t IMAGE --push .
```

For more information about building with attestations, see [Attestations](https://docs.docker.com/build/metadata/attestations/).

If you're using GitHub Actions to build and push your images, learn how you can [configure the action](https://docs.docker.com/build/ci/github-actions/attestations/) to apply SBOM and provenance attestations.

### [Default Non-Root User](#default-non-root-user)

By default, containers run as the `root` superuser with full system administration privileges inside the container, unless the Dockerfile specifies a different default user. Running containers as a privileged user weakens their runtime security, as it means any code that runs in the container can perform administrative actions.

The **Default Non-Root User** policy type detects images that are set to run as the default `root` user. To comply with this policy, images must specify a non-root user in the image configuration. Images are non-compliant with this policy if they don't specify a non-root default user for the runtime stage.

For non-compliant images, evaluation results show whether or not the `root` user was set explicitly for the image. This helps you distinguish between policy violations caused by images where the `root` user is implicit, and images where `root` is set on purpose.

The following Dockerfile runs as `root` by default despite not being explicitly set:

```Dockerfile
FROM alpine
RUN echo "Hi"
```

Whereas in the following case, the `root` user is explicitly set:

```Dockerfile
FROM alpine
USER root
RUN echo "Hi"
```

> Note
>
> This policy only checks for the default user of the image, as set in the image configuration blob. Even if you do specify a non-root default user, it's still possible to override the default user at runtime, for example by using the `--user` flag for the `docker run` command.

To make your images compliant with this policy, use the [`USER`](https://docs.docker.com/reference/dockerfile/#user) Dockerfile instruction to set a default user that doesn't have root privileges for the runtime stage.

The following Dockerfile snippets shows the difference between a compliant and non-compliant image.

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
ENTRYPOINT ["/app/production"]
```

```dockerfile
FROM alpine AS builder
COPY Makefile ./src /
RUN make build

FROM alpine AS runtime
COPY --from=builder bin/production /app
USER nonroot
ENTRYPOINT ["/app/production"]
```

### [Approved Base Images](#approved-base-images)

The **Approved Base Images** policy type ensures that the base images you use in your builds are maintained and secure.

This policy checks whether the base images used in your builds match any of the patterns specified in the policy configuration. The following table shows a few example patterns for this policy.

| Use case                                                        | Pattern                          |
| --------------------------------------------------------------- | -------------------------------- |
| Allow all images from Docker Hub                                | `docker.io/*`                    |
| Allow all Docker Official Images                                | `docker.io/library/*`            |
| Allow images from a specific organization                       | `docker.io/orgname/*`            |
| Allow tags of a specific repository                             | `docker.io/orgname/repository:*` |
| Allow images on a registry with hostname `registry.example.com` | `registry.example.com/*`         |
| Allow slim tags of NodeJS images                                | `docker.io/library/node:*-slim`  |

An asterisk (`*`) matches up until the character that follows, or until the end of the image reference. Note that the `docker.io` prefix is required in order to match Docker Hub images. This is the registry hostname of Docker Hub.

This policy is configurable with the following options:

* **Approved base image sources**

  Specify the image reference patterns that you want to allow. The policy evaluates the base image references against these patterns.

  Default: `[*]` (any reference is an allowed base image)

* **Only supported tags**

  Allow only supported tags when using Docker Official Images.

  When this option is enabled, images using unsupported tags of official images as their base image trigger a policy violation. Supported tags for official images are listed in the **Supported tags** section of the repository overview on Docker Hub.

  Enabled by default.

* **Only supported OS distributions**

  Allow only Docker Official Images of supported Linux distribution versions.

  When this option is enabled, images using unsupported Linux distributions that have reached end of life (such as `ubuntu:18.04`) trigger a policy violation.

  Enabling this option may cause the policy to report no data if the operating system version cannot be determined.

  Enabled by default.

Your images need provenance attestations for this policy to successfully evaluate. For more information, see [No base image data](#no-base-image-data).

### [SonarQube Quality Gates](#sonarqube-quality-gates)

The **SonarQube Quality Gates** policy type builds on the [SonarQube integration](https://docs.docker.com/scout/integrations/code-quality/sonarqube/) to assess the quality of your source code. This policy works by ingesting the SonarQube code analysis results into Docker Scout.

You define the criteria for this policy using SonarQube's [quality gates](https://docs.sonarsource.com/sonarqube/latest/user-guide/quality-gates/). SonarQube evaluates your source code against the quality gates you've defined in SonarQube. Docker Scout surfaces the SonarQube assessment as a Docker Scout policy.

Docker Scout uses [provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) attestations or the `org.opencontainers.image.revision` OCI annotation to link SonarQube analysis results with container images. In addition to enabling the SonarQube integration, you must also make sure that your images have either the attestation or the label.

Once you push an image and policy evaluation completes, the results from the SonarQube quality gates display as a policy in the Docker Scout Dashboard, and in the CLI.

> Note
>
> Docker Scout can only access SonarQube analyses created after the integration is enabled. Docker Scout doesn't have access to historic evaluations. Trigger a SonarQube analysis and policy evaluation after enabling the integration to view the results in Docker Scout.

### [Valid Docker Hardened Image (DHI) or DHI base image](#valid-docker-hardened-image-dhi-or-dhi-base-image)

The **Valid Docker Hardened Image (DHI) or DHI base image** policy type ensures that your images are either Docker Hardened Images (DHI) or are built using a DHI as the base image.

This policy validates images by checking for a valid Docker signed verification summary attestation. The policy considers an image compliant if either:

* The image itself is a Docker Hardened Image with a valid Docker signed verification summary attestation, or
* The base image used in the build (identified from SLSA provenance attestations) has a valid Docker signed verification summary attestation

Images are non-compliant with this policy if they lack the required Docker signed verification summary attestation and are not built from a base image with such an attestation.

This policy has no configurable parameters.

## [No base image data](#no-base-image-data)

There are cases when it's not possible to determine information about the base images used in your builds. In such cases, the **Up-to-Date Base Images** and **Approved Base Images** policies get flagged as having **No data**.

This "no data" state occurs when:

* Docker Scout doesn't know what base image tag you used
* The base image version you used has multiple tags, but not all tags are out of date

To make sure that Docker Scout always knows about your base image, you can attach [provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) at build-time. Docker Scout uses provenance attestations to find out the base image version.

----
url: https://docs.docker.com/reference/samples/minecraft/
----

# Minecraft samples

| Name                                                                                | Description                |
| ----------------------------------------------------------------------------------- | -------------------------- |
| [Minecraft server](https://github.com/docker/awesome-compose/tree/master/minecraft) | A sample Minecraft server. |

----
url: https://docs.docker.com/guides/vuejs/configure-github-actions/
----

# Automate your builds with GitHub Actions

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize an Vue.js application](https://docs.docker.com/guides/vuejs/containerize/).

You must also have:

* A [GitHub](https://github.com/signup) account.
* A verified [Docker Hub](https://hub.docker.com/signup) account.

***

## [Overview](#overview)

In this section, you'll set up a CI/CD pipeline using [GitHub Actions](https://docs.github.com/en/actions) to automatically:

* Build your Vue.js application inside a Docker container.
* Run tests in a consistent environment.
* Push the production-ready image to [Docker Hub](https://hub.docker.com).

***

## [Connect your GitHub repository to Docker Hub](#connect-your-github-repository-to-docker-hub)

To enable GitHub Actions to build and push Docker images, you’ll securely store your Docker Hub credentials in your new GitHub repository.

### [Step 1: Generate Docker Hub credentials and set GitHub secrets](#step-1-generate-docker-hub-credentials-and-set-github-secrets)

1. Create a Personal Access Token (PAT) from [Docker Hub](https://hub.docker.com)

   1. Go to your **Docker Hub account → Account Settings → Security**.
   2. Generate a new Access Token with **Read/Write** permissions.
   3. Name it something like `docker-vuejs-sample`.
   4. Copy and save the token — you’ll need it in Step 4.

2. Create a repository in [Docker Hub](https://hub.docker.com/repositories/)

   1. Go to your **Docker Hub account → Create a repository**.
   2. For the Repository Name, use something descriptive — for example: `vuejs-sample`.
   3. Once created, copy and save the repository name — you’ll need it in Step 4.

3. Create a new [GitHub repository](https://github.com/new) for your Vue.js project

4. Add Docker Hub credentials as GitHub repository secrets

   In your newly created GitHub repository:

   1. Navigate to: **Settings → Secrets and variables → Actions → New repository secret**.

   2. Add the following secrets:

   | Name                     | Value                                            |
   | ------------------------ | ------------------------------------------------ |
   | `DOCKER_USERNAME`        | Your Docker Hub username                         |
   | `DOCKERHUB_TOKEN`        | Your Docker Hub access token (created in Step 1) |
   | `DOCKERHUB_PROJECT_NAME` | Your Docker Project Name (created in Step 2)     |

   These secrets allow GitHub Actions to authenticate securely with Docker Hub during automated workflows.

5. Connect Your Local Project to GitHub

   Link your local project `docker-vuejs-sample` to the GitHub repository you just created by running the following command from your project root:

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   > Important
   >
   > Replace `{your-username}` and `{your-repository}` with your actual GitHub username and repository name.

   To confirm that your local project is correctly connected to the remote GitHub repository, run:

   ```console
   $ git remote -v
   ```

   You should see output similar to:

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   This confirms that your local repository is properly linked and ready to push your source code to GitHub.

6. Push your source code to GitHub

   Follow these steps to commit and push your local project to your GitHub repository:

   1. Stage all files for commit.

      ```console
      $ git add -A
      ```

      This command stages all changes — including new, modified, and deleted files — preparing them for commit.

   2. Commit the staged changes with a descriptive message.

      ```console
      $ git commit -m "Initial commit"
      ```

      This command creates a commit that snapshots the staged changes with a descriptive message.

   3. Push the code to the `main` branch.

      ```console
      $ git push -u origin main
      ```

      This command pushes your local commits to the `main` branch of the remote GitHub repository and sets the upstream branch.

Once completed, your code will be available on GitHub, and any GitHub Actions workflow you’ve configured will run automatically.

> Note
>
> Learn more about the Git commands used in this step:
>
> * [Git add](https://git-scm.com/docs/git-add) – Stage changes (new, modified, deleted) for commit
> * [Git commit](https://git-scm.com/docs/git-commit) – Save a snapshot of your staged changes
> * [Git push](https://git-scm.com/docs/git-push) – Upload local commits to your GitHub repository
> * [Git remote](https://git-scm.com/docs/git-remote) – View and manage remote repository URLs

***

### [Step 2: Set up the workflow](#step-2-set-up-the-workflow)

Now you'll create a GitHub Actions workflow that builds your Docker image, runs tests, and pushes the image to Docker Hub.

1. Go to your repository on GitHub and select the **Actions** tab in the top menu.

2. Select **Set up a workflow yourself** when prompted.

   This opens an inline editor to create a new workflow file. By default, it will be saved to: `.github/workflows/main.yml`

3. Add the following workflow configuration to the new file:

```yaml
name: CI/CD – Vue.js App with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-deploy:
    name: Build, Test & Deploy
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout the codebase
      - name: Checkout Code
        uses: actions/checkout@v6
        with:
          fetch-depth: 0

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      # 3. Cache Docker layers
      - name: Cache Docker Layers
        uses: actions/cache@v5
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: |
            ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm Dependencies
        uses: actions/cache@v5
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: |
            ${{ runner.os }}-npm-

      # 5. Generate build metadata
      - name: Generate Build Metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build Docker image for testing
      - name: Build Dev Docker Image
        uses: docker/build-push-action@v7
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run unit tests inside container
      - name: Run Vue.js Tests
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npm run test -- --ci --runInBand"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Log in to Docker Hub
      - name: Docker Hub Login
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push production image
      - name: Build and Push Production Image
        uses: docker/build-push-action@v7
        with:
          context: .
          file: Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
```

This workflow performs the following tasks for your Vue.js application:

> Note
>
> For more information about `docker/build-push-action`, refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

***

### [Step 3: Run the workflow](#step-3-run-the-workflow)

After you've added your workflow file, it's time to trigger and observe the CI/CD process in action.

1. Commit and push your workflow file

   * Select "Commit changes…" in the GitHub editor.

     * Repository name: `${your-repository-name}`

     * Tags include:

       * `latest` – represents the most recent successful build; ideal for quick testing or deployment.
       * `<short-sha>` – a unique identifier based on the commit hash, useful for version tracking, rollbacks, and traceability.

> Tip
>
> To maintain code quality and prevent accidental direct pushes, enable branch protection rules:
>
> * Navigate to your **GitHub repo → Settings → Branches**.
>
> * Under Branch protection rules, click **Add rule**.
>
> * Specify `main` as the branch name.
>
> * Enable options like:
>
>   * *Require a pull request before merging*.
>   * *Require status checks to pass before merging*.
>
> This ensures that only tested and reviewed code is merged into `main` branch.

***

## [Summary](#summary)

In this section, you set up a complete CI/CD pipeline for your containerized Vue.js application using GitHub Actions.

With this setup, your Vue.js application is now ready for automated testing and deployment across environments — increasing confidence, consistency, and team productivity.

***

***

## [Next steps](#next-steps)

Next, learn how you can locally test and debug your Vue.js workloads on Kubernetes before deploying. This helps you ensure your application behaves as expected in a production-like environment, reducing surprises during deployment.

[Test your Vue.js deployment »](https://docs.docker.com/guides/vuejs/deploy/)

----
url: https://docs.docker.com/reference/api/extensions-sdk/ServiceError/
----

# Interface: ServiceError

***

Table of contents

***

Error thrown when an HTTP response is received with a status code that falls out to the range of 2xx.

**`Since`**

0.2.0

## [Properties](#properties)

### [name](#name)

• **name**: `string`

***

### [message](#message)

• **message**: `string`

***

### [statusCode](#statuscode)

• **statusCode**: `number`

----
url: https://docs.docker.com/engine/cli/filter/
----

# Filter commands

***

Table of contents

***

You can use the `--filter` flag to scope your commands. When filtering, the commands only include entries that match the pattern you specify.

## [Using filters](#using-filters)

The `--filter` flag expects a key-value pair separated by an operator.

```console
$ docker COMMAND --filter "KEY=VALUE"
```

The key represents the field that you want to filter on. The value is the pattern that the specified field must match. The operator can be either equals (`=`) or not equals (`!=`).

For example, the command `docker images --filter reference=alpine` filters the output of the `docker images` command to only print `alpine` images.

```console
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
ubuntu       24.04     33a5cc25d22c   36 minutes ago   101MB
ubuntu       22.04     152dc042452c   36 minutes ago   88.1MB
alpine       3.21      a8cbb8c69ee7   40 minutes ago   8.67MB
alpine       latest    7144f7bab3d4   40 minutes ago   11.7MB
busybox      uclibc    3e516f71d880   48 minutes ago   2.4MB
busybox      glibc     7338d0c72c65   48 minutes ago   6.09MB
$ docker images --filter reference=alpine
REPOSITORY   TAG       IMAGE ID       CREATED          SIZE
alpine       3.21      a8cbb8c69ee7   40 minutes ago   8.67MB
alpine       latest    7144f7bab3d4   40 minutes ago   11.7MB
```

The available fields (`reference` in this case) depend on the command you run. Some filters expect an exact match. Others handle partial matches. Some filters let you use regular expressions.

Refer to the [CLI reference description](#reference) for each command to learn about the supported filtering capabilities for each command.

## [Combining filters](#combining-filters)

You can combine multiple filters by passing multiple `--filter` flags. The following example shows how to print all images that match `alpine:latest` or `busybox` - a logical `OR`.

```console
$ docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       24.04     33a5cc25d22c   2 hours ago   101MB
ubuntu       22.04     152dc042452c   2 hours ago   88.1MB
alpine       3.21      a8cbb8c69ee7   2 hours ago   8.67MB
alpine       latest    7144f7bab3d4   2 hours ago   11.7MB
busybox      uclibc    3e516f71d880   2 hours ago   2.4MB
busybox      glibc     7338d0c72c65   2 hours ago   6.09MB
$ docker images --filter reference=alpine:latest --filter=reference=busybox
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
alpine       latest    7144f7bab3d4   2 hours ago   11.7MB
busybox      uclibc    3e516f71d880   2 hours ago   2.4MB
busybox      glibc     7338d0c72c65   2 hours ago   6.09MB
```

### [Multiple negated filters](#multiple-negated-filters)

Some commands support negated filters on [labels](https://docs.docker.com/engine/manage-resources/labels/). Negated filters only consider results that don't match the specified patterns. The following command prunes all containers that aren't labeled `foo`.

```console
$ docker container prune --filter "label!=foo"
```

There's a catch in combining multiple negated label filters. Multiple negated filters create a single negative constraint - a logical `AND`. The following command prunes all containers except those labeled both `foo` and `bar`. Containers labeled either `foo` or `bar`, but not both, will be pruned.

```console
$ docker container prune --filter "label!=foo" --filter "label!=bar"
```

## [Reference](#reference)

For more information about filtering commands, refer to the CLI reference description for commands that support the `--filter` flag:

* [`docker config ls`](/reference/cli/docker/config/ls/)
* [`docker container prune`](/reference/cli/docker/container/prune/)
* [`docker image prune`](/reference/cli/docker/image/prune/)
* [`docker image ls`](/reference/cli/docker/image/ls/)
* [`docker network ls`](/reference/cli/docker/network/ls/)
* [`docker network prune`](/reference/cli/docker/network/prune/)
* [`docker node ls`](/reference/cli/docker/node/ls/)
* [`docker node ps`](/reference/cli/docker/node/ps/)
* [`docker plugin ls`](/reference/cli/docker/plugin/ls/)
* [`docker container ls`](/reference/cli/docker/container/ls/)
* [`docker search`](/reference/cli/docker/search/)
* [`docker secret ls`](/reference/cli/docker/secret/ls/)
* [`docker service ls`](/reference/cli/docker/service/ls/)
* [`docker service ps`](/reference/cli/docker/service/ps/)
* [`docker stack ps`](/reference/cli/docker/stack/ps/)
* [`docker system prune`](/reference/cli/docker/system/prune/)
* [`docker volume ls`](/reference/cli/docker/volume/ls/)
* [`docker volume prune`](/reference/cli/docker/volume/prune/)

----
url: https://docs.docker.com/desktop/setup/install/linux/fedora/
----

# Install Docker Desktop on Fedora

***

Table of contents

***

> **Docker Desktop terms**
>
> Commercial use of Docker Desktop in larger enterprises (more than 250 employees OR more than $10 million USD in annual revenue) requires a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopFedoraInstall).

This page contains information on how to install, launch and upgrade Docker Desktop on a Fedora distribution.

## [Prerequisites](#prerequisites)

To install Docker Desktop successfully, you must:

* Meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).

* Have a 64-bit version of Fedora 42 or Fedora 43.

* For a GNOME desktop environment you must install AppIndicator and KStatusNotifierItem [GNOME extensions](https://extensions.gnome.org/extension/615/appindicator-support/).

* If you're not using GNOME, you must install `gnome-terminal` to enable terminal access from Docker Desktop:

  ```console
  $ sudo dnf install gnome-terminal
  ```

## [Install Docker Desktop](#install-docker-desktop)

To install Docker Desktop on Fedora:

1. Set up [Docker's package repository](https://docs.docker.com/engine/install/fedora/#set-up-the-repository).

2. Download the latest [RPM package](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64.rpm?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-linux-amd64). For checksums, see the [Release notes](https://docs.docker.com/desktop/release-notes/).

3. Install the package with dnf as follows:

   ```console
   $ sudo dnf install ./docker-desktop-x86_64.rpm
   ```

   By default, Docker Desktop is installed at `/opt/docker-desktop`.

The RPM package includes a post-install script that completes additional setup steps automatically.

```console
$ systemctl --user start docker-desktop
```

When Docker Desktop starts, it creates a dedicated [context](/engine/context/working-with-contexts) that the Docker CLI can use as a target and sets it as the current context in use. This is to avoid a clash with a local Docker Engine that may be running on the Linux host and using the default context. On shutdown, Docker Desktop resets the current context to the previous one.

The Docker Desktop installer updates Docker Compose and the Docker CLI binaries on the host. It installs Docker Compose V2 and gives users the choice to link it as docker-compose from the Settings panel. Docker Desktop installs the new Docker CLI binary that includes cloud-integration capabilities in `/usr/local/bin/com.docker.cli` and creates a symlink to the classic Docker CLI at `/usr/local/bin`.

After you’ve successfully installed Docker Desktop, you can check the versions of these binaries by running the following commands:

```console
$ docker compose version
Docker Compose version v2.39.4

$ docker --version
Docker version 28.4.0, build d8eb465

$ docker version
Client:
 Version:           28.4.0
 API version:       1.51
 Go version:        go1.24.7
<...>
```

To enable Docker Desktop to start on sign in, from the Docker menu, select **Settings** > **General** > **Start Docker Desktop when you sign in to your computer**.

Alternatively, open a terminal and run:

```console
$ systemctl --user enable docker-desktop
```

To stop Docker Desktop, select the Docker menu icon to open the Docker menu and select **Quit Docker Desktop**.

Alternatively, open a terminal and run:

```console
$ systemctl --user stop docker-desktop
```

## [Upgrade Docker Desktop](#upgrade-docker-desktop)

Once a new version for Docker Desktop is released, the Docker UI shows a notification. You need to first remove the previous version and then download the new package each time you want to upgrade Docker Desktop. Run:

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-x86_64.rpm
```

## [Next steps](#next-steps)

* Explore [Docker's subscriptions](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopFedoraInstall) to see what Docker can offer you.
* Take a look at the [Docker workshop](https://docs.docker.com/get-started/workshop/) to learn how to build an image and run it as a containerized application.
* [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
* [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how to run and submit diagnostics, and submit issues.
* [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
* [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
* [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions on backing up and restoring data related to Docker.

----
url: https://docs.docker.com/compose/trust-model/
----

# Trust model for Compose files

***

Table of contents

***

Docker Compose treats every Compose file as trusted input. When a Compose file requests elevated privileges, host filesystem access, or any other configuration, Compose applies it as written. This is the same behavior as passing flags directly to `docker run`.

This means that any Compose file you run, whether it lives on your local filesystem, in a Git repository, or in an OCI registry, has full control over how containers interact with your host. The security boundary is not where the file comes from but whether you trust the author.

Evaluating trust means asking: Who authored this file? Has it changed since you last reviewed it? Do you understand every privilege it requests?

## [The dependency chain](#the-dependency-chain)

A Compose application can be assembled from multiple sources. The [`include`](https://docs.docker.com/reference/compose-file/include/) directive imports entire Compose files, while [`extends`](https://docs.docker.com/reference/compose-file/services/#extends) inherits configuration from a specific service in another file. Both support remote references and can be chained:

```text
Your command
  └─ compose.yaml                                    (local or remote)
       ├─ services, volumes, networks                (direct config)
       ├─ include:
       │    └─ oci://registry.example.com/base:v2   (remote dependency)
       │         └─ services, volumes, networks      (indirect config)
       └─ services:
            └─ app:
                 └─ extends:
                      └─ file: oci://registry.example.com/templates:v1
                           └─ service: webapp        (inherited config)
```

Each level has the same capabilities. The top-level file you inspect may appear safe while a nested `include` or `extends` introduces services with elevated privileges, host bind mounts, or untrusted images. These dependencies can also change independently. Risky settings can be introduced by a nested dependency that you never see unless you inspect the fully resolved output.

> Important
>
> Compose warns you when a configuration references remote sources. Do not accept this without understanding every reference in the chain.

## [Best practices](#best-practices)

### [Inspect the full configuration](#inspect-the-full-configuration)

To see exactly what Compose applies, including all resolved `includes`, `extends`, merged overrides, and interpolated variables, use:

```console
$ docker compose config
```

For remote references:

```console
$ docker compose -f oci://registry.example.com/myapp:latest config
```

Review this output before running `up` or `create`, especially when the configuration comes from a source you have not audited.

#### [Fields to look out for](#fields-to-look-out-for)

A Compose configuration has broad control over how containers interact with the host. The following is a non-exhaustive list of fields that carry security implications when set by an untrusted author:

| Field                   | Effect                                                      |
| ----------------------- | ----------------------------------------------------------- |
| `privileged`            | Grants the container full access to the host                |
| `cap_add`               | Adds Linux capabilities such as `SYS_ADMIN` or `NET_RAW`    |
| `security_opt`          | Configures security profiles including seccomp and AppArmor |
| `volumes` / bind mounts | Mounts host directories into the container                  |
| `network_mode: host`    | Shares the host network stack                               |
| `pid: host`             | Shares the host PID namespace                               |
| `devices`               | Exposes host devices to the container                       |
| `image`                 | Pulls and runs an arbitrary container image                 |

When in doubt, look up the effect of any unfamiliar field before running the configuration.

### [CI/CD environments](#cicd-environments)

Automated pipelines are particularly sensitive because they often run with access to credentials, cloud provider tokens, or Docker sockets.

* Avoid referencing public or unverified Compose configurations in automated pipelines.
* Gate updates behind your normal code review process.
* Use read-only Docker socket mounts where possible to limit your risk.

### [Pin remote references to digests](#pin-remote-references-to-digests)

Tags are mutable, meaning anyone with push access to a registry can overwrite a tag silently, so a reference you reviewed last week may point to different content today.

Digests are immutable. Instead of referencing by tag, pin to the digest.

```yaml
include:
  - oci://registry.example.com/base@sha256:a1b2c3d4...
```

Treat any update to a pinned digest as a code change. Make sure you review the new content before updating the reference.

### [Other](#other)

* Use a private registry: Host OCI artifacts on a registry your organization controls. Restrict who can push to it.
* Audit transitive dependencies: Check every remote `include` and `extends` reference in the chain, not just the top-level file.
* Review all Compose confirmation prompts: When loading remote Compose files, Compose displays confirmation prompts for interpolation variables, environment values, and remote includes. Review these before accepting.

## [Further reading](#further-reading)

* [OCI artifact applications](https://docs.docker.com/compose/how-tos/oci-artifact/)
* [Use Compose in production](https://docs.docker.com/compose/how-tos/production/)
* [`include` reference](https://docs.docker.com/reference/compose-file/include/)
* [`extends` reference](https://docs.docker.com/reference/compose-file/services/#extends)
* [Manage secrets in Compose](https://docs.docker.com/compose/how-tos/use-secrets/)

----
url: https://docs.docker.com/engine/extend/plugins_volume/
----

# Docker volume plugins

***

Table of contents

***

Docker Engine volume plugins enable Engine deployments to be integrated with external storage systems such as Amazon EBS, and enable data volumes to persist beyond the lifetime of a single Docker host. See the [plugin documentation](https://docs.docker.com/engine/extend/legacy_plugins/) for more information.

## [Changelog](#changelog)

### [1.13.0](#1130)

* If used as part of the v2 plugin architecture, mountpoints that are part of paths returned by the plugin must be mounted under the directory specified by `PropagatedMount` in the plugin configuration ([#26398](https://github.com/docker/docker/pull/26398))

### [1.12.0](#1120)

* Add `Status` field to `VolumeDriver.Get` response ([#21006](https://github.com/docker/docker/pull/21006#))
* Add `VolumeDriver.Capabilities` to get capabilities of the volume driver ([#22077](https://github.com/docker/docker/pull/22077))

### [1.10.0](#1100)

* Add `VolumeDriver.Get` which gets the details about the volume ([#16534](https://github.com/docker/docker/pull/16534))
* Add `VolumeDriver.List` which lists all volumes owned by the driver ([#16534](https://github.com/docker/docker/pull/16534))

### [1.8.0](#180)

* Initial support for volume driver plugins ([#14659](https://github.com/docker/docker/pull/14659))

## [Command-line changes](#command-line-changes)

To give a container access to a volume, use the `--volume` and `--volume-driver` flags on the `docker container run` command. The `--volume` (or `-v`) flag accepts a volume name and path on the host, and the `--volume-driver` flag accepts a driver type.

```console
$ docker volume create --driver=myplugin volumename

$ docker container run -it --volume volumename:/data busybox sh
```

### [`--volume`](#--volume)

The `--volume` (or `-v`) flag takes a value that is in the format `<volume_name>:<mountpoint>`. The two parts of the value are separated by a colon (`:`) character.

* The volume name is a human-readable name for the volume, and cannot begin with a `/` character. It is referred to as `volume_name` in the rest of this topic.
* The `Mountpoint` is the path on the host (v1) or in the plugin (v2) where the volume has been made available.

### [`--volume-driver`](#--volume-driver)

Specifying the `--volume-driver` flag together with a volume name (using `--volume`) allows you to use plugins to manage volumes for the container.

The `--volume-driver` flag is used as a default for all volumes created for the container, including anonymous volumes. Use the [`--mount`](https://docs.docker.com/reference/cli/docker/container/run/#mount) flag with the [`volume-driver`](https://docs.docker.com/engine/storage/volumes/#start-a-container-which-creates-a-volume-using-a-volume-driver) option to specify the driver to use for each volume individually.

## [Create a VolumeDriver](#create-a-volumedriver)

The container creation endpoint (`/containers/create`) accepts a `VolumeDriver` field of type `string` allowing to specify the name of the driver. If not specified, it defaults to `"local"` (the default driver for local volumes).

## [Volume plugin protocol](#volume-plugin-protocol)

If a plugin registers itself as a `VolumeDriver` when activated, it must provide the Docker Daemon with writeable paths on the host filesystem. The Docker daemon provides these paths to containers to consume. The Docker daemon makes the volumes available by bind-mounting the provided paths into the containers.

> Note
>
> Volume plugins should *not* write data to the `/var/lib/docker/` directory, including `/var/lib/docker/volumes`. The `/var/lib/docker/` directory is reserved for Docker.

### [`/VolumeDriver.Create`](#volumedrivercreate)

Request:

```json
{
    "Name": "volume_name",
    "Opts": {}
}
```

Instruct the plugin that the user wants to create a volume, given a user specified volume name. The plugin does not need to actually manifest the volume on the filesystem yet (until `Mount` is called). `Opts` is a map of driver specific options passed through from the user request.

Response:

```json
{
    "Err": ""
}
```

Respond with a string error if an error occurred.

### [`/VolumeDriver.Remove`](#volumedriverremove)

Request:

```json
{
    "Name": "volume_name"
}
```

Delete the specified volume from disk. This request is issued when a user invokes `docker rm -v` to remove volumes associated with a container.

Response:

```json
{
    "Err": ""
}
```

Respond with a string error if an error occurred.

### [`/VolumeDriver.Mount`](#volumedrivermount)

Request:

```json
{
    "Name": "volume_name",
    "ID": "b87d7442095999a92b65b3d9691e697b61713829cc0ffd1bb72e4ccd51aa4d6c"
}
```

Docker requires the plugin to provide a volume, given a user specified volume name. `Mount` is called once per container start. If the same `volume_name` is requested more than once, the plugin may need to keep track of each new mount request and provision at the first mount request and deprovision at the last corresponding unmount request.

`ID` is a unique ID for the caller that is requesting the mount.

Response:

* v1

  ```json
  {
      "Mountpoint": "/path/to/directory/on/host",
      "Err": ""
  }
  ```

* v2

  ```json
  {
      "Mountpoint": "/path/under/PropagatedMount",
      "Err": ""
  }
  ```

`Mountpoint` is the path on the host (v1) or in the plugin (v2) where the volume has been made available.

`Err` is either empty or contains an error string.

### [`/VolumeDriver.Path`](#volumedriverpath)

Request:

```json
{
    "Name": "volume_name"
}
```

Request the path to the volume with the given `volume_name`.

Response:

* v1

  ```json
  {
      "Mountpoint": "/path/to/directory/on/host",
      "Err": ""
  }
  ```

* v2

  ```json
  {
      "Mountpoint": "/path/under/PropagatedMount",
      "Err": ""
  }
  ```

Respond with the path on the host (v1) or inside the plugin (v2) where the volume has been made available, and/or a string error if an error occurred.

`Mountpoint` is optional. However, the plugin may be queried again later if one is not provided.

### [`/VolumeDriver.Unmount`](#volumedriverunmount)

Request:

```json
{
    "Name": "volume_name",
    "ID": "b87d7442095999a92b65b3d9691e697b61713829cc0ffd1bb72e4ccd51aa4d6c"
}
```

Docker is no longer using the named volume. `Unmount` is called once per container stop. Plugin may deduce that it is safe to deprovision the volume at this point.

`ID` is a unique ID for the caller that is requesting the mount.

Response:

```json
{
    "Err": ""
}
```

Respond with a string error if an error occurred.

### [`/VolumeDriver.Get`](#volumedriverget)

Request:

```json
{
    "Name": "volume_name"
}
```

Get info about `volume_name`.

Response:

* v1

  ```json
  {
    "Volume": {
      "Name": "volume_name",
      "Mountpoint": "/path/to/directory/on/host",
      "Status": {}
    },
    "Err": ""
  }
  ```

* v2

  ```json
  {
    "Volume": {
      "Name": "volume_name",
      "Mountpoint": "/path/under/PropagatedMount",
      "Status": {}
    },
    "Err": ""
  }
  ```

Respond with a string error if an error occurred. `Mountpoint` and `Status` are optional.

### [/VolumeDriver.List](#volumedriverlist)

Request:

```json
{}
```

Get the list of volumes registered with the plugin.

Response:

* v1

  ```json
  {
    "Volumes": [
      {
        "Name": "volume_name",
        "Mountpoint": "/path/to/directory/on/host"
      }
    ],
    "Err": ""
  }
  ```

* v2

  ```json
  {
    "Volumes": [
      {
        "Name": "volume_name",
        "Mountpoint": "/path/under/PropagatedMount"
      }
    ],
    "Err": ""
  }
  ```

Respond with a string error if an error occurred. `Mountpoint` is optional.

### [/VolumeDriver.Capabilities](#volumedrivercapabilities)

Request:

```json
{}
```

Get the list of capabilities the driver supports.

The driver is not required to implement `Capabilities`. If it is not implemented, the default values are used.

Response:

```json
{
  "Capabilities": {
    "Scope": "global"
  }
}
```

Supported scopes are `global` and `local`. Any other value in `Scope` will be ignored, and `local` is used. `Scope` allows cluster managers to handle the volume in different ways. For instance, a scope of `global`, signals to the cluster manager that it only needs to create the volume once instead of on each Docker host. More capabilities may be added in the future.

----
url: https://docs.docker.com/reference/cli/docker/mcp/secret/rm/
----

# docker mcp secret rm

***

| Description | Remove secrets from the local OS Keychain |
| ----------- | ----------------------------------------- |
| Usage       | `docker mcp secret rm name1 name2 ...`    |

## [Description](#description)

Remove secrets from the local OS Keychain

## [Options](#options)

| Option  | Default | Description        |
| ------- | ------- | ------------------ |
| `--all` |         | Remove all secrets |

----
url: https://docs.docker.com/build/builders/manage/
----

# Manage builders

***

Table of contents

***

You can create, inspect, and manage builders using `docker buildx` commands, or [using Docker Desktop](#manage-builders-with-docker-desktop).

## [Create a new builder](#create-a-new-builder)

The default builder uses the [`docker` driver](https://docs.docker.com/build/builders/drivers/docker/). You can't manually create new `docker` builders, but you can create builders that use other drivers, such as the [`docker-container` driver](https://docs.docker.com/build/builders/drivers/docker-container/), which runs the BuildKit daemon in a container.

Use the [`docker buildx create`](/reference/cli/docker/buildx/create/) command to create a builder.

```console
$ docker buildx create --name=<builder-name>
```

Buildx uses the `docker-container` driver by default if you omit the `--driver` flag. For more information about available drivers, see [Build drivers](https://docs.docker.com/build/builders/drivers/).

## [List available builders](#list-available-builders)

Use `docker buildx ls` to see builder instances available on your system, and the drivers they're using.

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT      STATUS   BUILDKIT PLATFORMS
default *       docker
  default       default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
my_builder      docker-container
  my_builder0   default              running  v0.11.6  linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
```

The asterisk (`*`) next to the builder name indicates the [selected builder](https://docs.docker.com/build/builders/#selected-builder).

## [Inspect a builder](#inspect-a-builder)

To inspect a builder with the CLI, use `docker buildx inspect <name>`. You can only inspect a builder if the builder is active. You can add the `--bootstrap` flag to the command to start the builder.

```console
$ docker buildx inspect --bootstrap my_builder
[+] Building 1.7s (1/1) FINISHED                                                                  
 => [internal] booting buildkit                                                              1.7s
 => => pulling image moby/buildkit:buildx-stable-1                                           1.3s
 => => creating container buildx_buildkit_my_builder0                                        0.4s
Name:          my_builder
Driver:        docker-container
Last Activity: 2023-06-21 18:28:37 +0000 UTC

Nodes:
Name:      my_builder0
Endpoint:  unix:///var/run/docker.sock
Status:    running
Buildkit:  v0.11.6
Platforms: linux/arm64, linux/amd64, linux/amd64/v2, linux/riscv64, linux/ppc64le, linux/s390x, linux/386, linux/mips64le, linux/mips64, linux/arm/v7, linux/arm/v6
```

If you want to see how much disk space a builder is using, use the `docker buildx du` command. By default, this command shows the total disk usage for all available builders. To see usage for a specific builder, use the `--builder` flag.

```console
$ docker buildx du --builder my_builder
ID                                        RECLAIMABLE SIZE        LAST ACCESSED
olkri5gq6zsh8q2819i69aq6l                 true        797.2MB     37 seconds ago
6km4kasxgsywxkm6cxybdumbb*                true        438.5MB     36 seconds ago
qh3wwwda7gx2s5u4hsk0kp4w7                 true        213.8MB     37 seconds ago
54qq1egqem8max3lxq6180cj8                 true        200.2MB     37 seconds ago
ndlp969ku0950bmrw9muolw0c*                true        116.7MB     37 seconds ago
u52rcsnfd1brwc0chwsesb3io*                true        116.7MB     37 seconds ago
rzoeay0s4nmss8ub59z6lwj7d                 true        46.25MB     4 minutes ago
itk1iibhmv7awmidiwbef633q                 true        33.33MB     37 seconds ago
4p78yqnbmgt6xhcxqitdieeln                 true        19.46MB     4 minutes ago
dgkjvv4ay0szmr9bl7ynla7fy*                true        19.24MB     36 seconds ago
tuep198kmcw299qc9e4d1a8q2                 true        8.663MB     4 minutes ago
n1wzhauk9rpmt6ib1es7dktvj                 true        20.7kB      4 minutes ago
0a2xfhinvndki99y69157udlm                 true        16.56kB     37 seconds ago
gf0z1ypz54npfererqfeyhinn                 true        16.38kB     37 seconds ago
nz505f12cnsu739dw2pw0q78c                 true        8.192kB     37 seconds ago
hwpcyq5hdfvioltmkxu7fzwhb*                true        8.192kB     37 seconds ago
acekq89snc7j6im1rjdizvsg1*                true        8.192kB     37 seconds ago
Reclaimable:  2.01GB
Total:        2.01GB
```

## [Remove a builder](#remove-a-builder)

Use the [`docker buildx remove`](/reference/cli/docker/buildx/create/) command to remove a builder.

```console
$ docker buildx rm <builder-name>
```

If you remove your currently selected builder, the default `docker` builder is automatically selected. You can't remove the default builder.

Local build cache for the builder is also removed.

### [Removing remote builders](#removing-remote-builders)

Removing a remote builder doesn't affect the remote build cache. It also doesn't stop the remote BuildKit daemon. It only removes your connection to the builder.

## [Manage builders with Docker Desktop](#manage-builders-with-docker-desktop)

If you have turned on the [Docker Desktop Builds view](https://docs.docker.com/desktop/use-desktop/builds/), you can inspect builders in [Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#builders).

----
url: https://docs.docker.com/reference/cli/docker/pass/get/
----

# docker pass get

***

| Description | Get a secret from a keystore. |
| ----------- | ----------------------------- |
| Usage       | `docker pass get NAME`        |

## [Description](#description)

Retrieves a named secret from the local OS keychain. The secret value is masked in output.

----
url: https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/
----

# Troubleshoot Docker Desktop

***

Table of contents

***

This page contains information on how to diagnose and troubleshoot Docker Desktop, and how to check the logs.

## [Troubleshoot menu](#troubleshoot-menu)

To navigate to **Troubleshoot** either:

* Select the Docker menu Docker menu and then **Troubleshoot**.
* Select the **Troubleshoot** icon near the top-right corner of Docker Dashboard.

The **Troubleshooting** menu contains the following options:

* **Restart Docker Desktop**.

* **Reset Kubernetes cluster**. Select to delete all stacks and Kubernetes resources. For more information, see [Kubernetes](https://docs.docker.com/desktop/settings-and-maintenance/settings/#kubernetes).

* **Clean / Purge data**. This option resets all Docker data without a reset to factory defaults. Selecting this option results in the loss of existing settings.

* **Reset to factory defaults**: Choose this option to reset all options on Docker Desktop to their initial state, the same as when Docker Desktop was first installed.

If you are a Mac or Linux user, you also have the option to **Uninstall** Docker Desktop from your system.

## [Diagnose](#diagnose)

> Tip
>
> If you do not find a solution in troubleshooting, browse the GitHub repositories or create a new issue on the [Docker Desktop issue tracker](https://github.com/docker/desktop-feedback).

### [Diagnose from the app](#diagnose-from-the-app)

1. From **Troubleshoot**, select **Get support**. This opens the in-app Support page and starts collecting the diagnostics.

   > Note
   >
   > Gathering diagnostics may take several minutes. Don't close Docker Desktop while the diagnostics are being collected.

2. When the diagnostics collection process is complete, select **Upload to get a Diagnostic ID**.

3. When the diagnostics are uploaded, Docker Desktop prints a diagnostic ID. Copy this ID.

4. Use your diagnostics ID to get help:

   * If you have a paid Docker subscription, select **Contact support**. This opens the Docker Desktop support form. Fill in the information required and add the ID you copied in step three to the **Diagnostics ID field**. Then, select **Submit ticket** to request Docker Desktop support.

     > Note
     >
     > You must be signed in to Docker Desktop to access the support form. For information on what's covered as part of Docker Desktop support, see [Support](https://docs.docker.com/support/).

   * If you don't have a paid Docker subscription, select **Report a Bug** to open a new Docker Desktop issue on GitHub. Complete the information required and ensure you add the diagnostic ID you copied in step three.

### [Diagnose from an error message](#diagnose-from-an-error-message)

1. When an error message appears, select **Gather diagnostics**.

   > Note
   >
   > Gathering diagnostics may take several minutes. Don't close Docker Desktop while the diagnostics are being collected.

2. When the diagnostics are uploaded, Docker Desktop prints a diagnostic ID. Copy this ID.

3. Use your diagnostics ID to get help:

   * If you have a paid Docker subscription, select **Contact support**. This opens the Docker Desktop support form. Fill in the information required and add the ID you copied in step three to the **Diagnostics ID field**. Then, select **Submit ticket** to request Docker Desktop support.

     > Note
     >
     > You must be signed in to Docker Desktop to access the support form. For information on what's covered as part of Docker Desktop support, see [Support](https://docs.docker.com/support/).

   * If you don't have a paid Docker subscription, you can open a new [Docker Desktop issue on GitHub](https://github.com/docker/desktop-feedback). Complete the information required and ensure you add the diagnostic ID printed in step two.

### [Diagnose from the terminal](#diagnose-from-the-terminal)

In some cases, it's useful to run the diagnostics yourself, for instance, if Docker Desktop cannot start.

> Note
>
> Gathering diagnostics may take several minutes. Wait for the process to complete before closing the terminal.

1. Locate the `com.docker.diagnose` tool:

   ```console
   # For all-user installations
   $ C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe

   # For per-user installations
   $ %LOCALAPPDATA%\Programs\DockerDesktop\resources\com.docker.diagnose.exe
   ```

2. Create and upload the diagnostics ID. In PowerShell, run:

   ```console
   # For all-user installations
   $ & "C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe" gather -upload

   # For per-user installations
   $ & %LOCALAPPDATA%\Programs\DockerDesktop\resources\com.docker.diagnose.exe" gather -upload
   ```

After the diagnostics have finished, the terminal displays your diagnostics ID and the path to the diagnostics file. The diagnostics ID is composed of your user ID and a timestamp. For example `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`.

1. Locate the `com.docker.diagnose` tool:

   ```console
   $ /Applications/Docker.app/Contents/MacOS/com.docker.diagnose
   ```

2. Create and upload the diagnostics ID. Run:

   ```console
   $ /Applications/Docker.app/Contents/MacOS/com.docker.diagnose gather -upload
   ```

After the diagnostics have finished, the terminal displays your diagnostics ID and the path to the diagnostics file. The diagnostics ID is composed of your user ID and a timestamp. For example `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`.

1. Locate the `com.docker.diagnose` tool:

   ```console
   $ /opt/docker-desktop/bin/com.docker.diagnose
   ```

2. Create and upload the diagnostics ID. Run:

   ```console
   $ /opt/docker-desktop/bin/com.docker.diagnose gather -upload
   ```

After the diagnostics have finished, the terminal displays your diagnostics ID and the path to the diagnostics file. The diagnostics ID is composed of your user ID and a timestamp. For example `BE9AFAAF-F68B-41D0-9D12-84760E6B8740/20190905152051`.

> Tip
>
> You can also use the [`docker desktop diagnose` command](https://docs.docker.com/desktop/features/desktop-cli/) to diagnose Docker Desktop and upload the diagnostics ID.

To view the contents of the diagnostic file:

1. Unzip the file. In PowerShell, copy and paste the path to the diagnostics file into the following command and then run it. It should be similar to the following example:

   ```powershell
   $ Expand-Archive -LiteralPath "C:\Users\testUser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602.zip" -DestinationPath "C:\Users\testuser\AppData\Local\Temp\5DE9978A-3848-429E-8776-950FC869186F\20230607101602"
   ```

2. Open the file in your preferred text editor. Run:

   ```powershell
   $ code <path-to-file>
   ```

Run:

```console
$ open /tmp/<your-diagnostics-ID>.zip
```

Run:

```console
$ unzip –l /tmp/<your-diagnostics-ID>.zip
```

#### [Use your diagnostics ID to get help](#use-your-diagnostics-id-to-get-help)

If you have a paid Docker subscription, select **Contact support**. This opens the Docker Desktop support form. Fill in the information required and add the ID you copied in step three to the **Diagnostics ID field**. Then, select **Submit ticket** to request Docker Desktop support.

If you don't have a paid Docker subscription, create an issue on [GitHub](https://github.com/docker/desktop-feedback).

### [Self-diagnose tool](#self-diagnose-tool)

> Important
>
> This tool has been deprecated.

## [Check the logs](#check-the-logs)

In addition to using the diagnose option to submit logs, you can browse the logs yourself.

In PowerShell, run:

```powershell
$ code $Env:LOCALAPPDATA\Docker\log
```

This opens up all the logs in your preferred text editor for you to explore.

### [From terminal](#from-terminal)

To watch the live flow of Docker Desktop logs in the command line, run the following script from your preferred shell.

```console
$ pred='process matches ".*(ocker|vpnkit).*" || (process in {"taskgated-helper", "launchservicesd", "kernel"} && eventMessage contains[c] "docker")'
$ /usr/bin/log stream --style syslog --level=debug --color=always --predicate "$pred"
```

Alternatively, to collect the last day of logs (`1d`) in a file, run:

```console
$ /usr/bin/log show --debug --info --style syslog --last 1d --predicate "$pred" >/tmp/logs.txt
```

### [From the Console app](#from-the-console-app)

Mac provides a built-in log viewer, named **Console**, which you can use to check Docker logs.

The Console lives in `/Applications/Utilities`. You can search for it with Spotlight Search.

To read the Docker app log messages, type `docker` in the Console window search bar and press Enter. Then select `ANY` to expand the drop-down list next to your `docker` search entry, and select `Process`.

You can use the Console Log Query to search logs, filter the results in various ways, and create reports.

You can access Docker Desktop logs by running the following command:

```console
$ journalctl --user --unit=docker-desktop
```

You can also find the logs for the internal components included in Docker Desktop at `$HOME/.docker/desktop/log/`.

## [View the Docker daemon logs](#view-the-docker-daemon-logs)

Refer to the [Read the daemon logs](https://docs.docker.com/engine/daemon/logs/) section to learn how to view the Docker Daemon logs.

## [Further resources](#further-resources)

* View specific [troubleshoot topics](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/).
* View information on [known issues](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/)
* [Fix "Docker.app is damaged" on macOS](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/) - Resolve macOS installation issues
* [Get support for Docker products](https://docs.docker.com/support/)

----
url: https://docs.docker.com/build-cloud/ci/
----

# Use Docker Build Cloud in CI

***

Table of contents

***

Using Docker Build Cloud in CI can speed up your build pipelines, which means less time spent waiting and context switching. You control your CI workflows as usual, and delegate the build execution to Docker Build Cloud.

Building with Docker Build Cloud in CI involves the following steps:

1. Sign in to a Docker account.
2. Set up Buildx and connect to the builder.
3. Run the build.

When using Docker Build Cloud in CI, it's recommended that you push the result to a registry directly, rather than loading the image and then pushing it. Pushing directly speeds up your builds and avoids unnecessary file transfers.

If you just want to build and discard the output, export the results to the build cache or build without tagging the image. When you use Docker Build Cloud, Buildx automatically loads the build result if you build a tagged image. See [Loading build results](https://docs.docker.com/build-cloud/usage/#loading-build-results) for details.

> Note
>
> Builds on Docker Build Cloud have a timeout limit of 90 minutes. Builds that run for longer than 90 minutes are automatically cancelled.

## [Setting up credentials for CI/CD](#setting-up-credentials-for-cicd)

To enable your CI/CD system to build and push images using Docker Build Cloud, provide both an access token and a username. The type of token and the username you use depend on your account type and permissions.

* If you are an organization administrator or have permission to create [organization access tokens (OAT)](https://docs.docker.com/enterprise/security/access-tokens/), use an OAT and set `DOCKER_ACCOUNT` to your Docker Hub organization name.
* If you do not have permission to create OATs or are using a personal account, use a [personal access token (PAT)](/security/access-tokens/) and set `DOCKER_ACCOUNT` to your Docker Hub username.

### [Creating access tokens](#creating-access-tokens)

#### [For organization accounts](#for-organization-accounts)

If you are an organization administrator:

* Create an [organization access token (OAT)](https://docs.docker.com/enterprise/security/access-tokens/). The token must have these permissions:

  1. **cloud-connect** scope

  2. **Read public repositories** permission

  3. **Repository access** with **Image push** permission for the target repository:

     * Expand the **Repository** drop-down.
     * Select **Add repository** and choose your target repository.
     * Set the **Image push** permission for the repository.

If you are not an organization administrator:

* Ask your organization administrator for an access token with the permissions listed above, or use a personal access token.

#### [For personal accounts](#for-personal-accounts)

* Create a [personal access token (PAT)](/security/access-tokens/) with the following permissions:
  1. **Read & write** access.
     * Note: Building with Docker Build Cloud only requires read access, but you need write access to push images to a Docker Hub repository.

## [CI platform examples](#ci-platform-examples)

> Note
>
> In your CI/CD configuration, set the following variables/secrets:
>
> * `DOCKER_ACCESS_TOKEN` — your access token (PAT or OAT). Use a secret to store the token.
> * `DOCKER_ACCOUNT` — your Docker Hub organization name (for OAT) or username (for PAT)
> * `CLOUD_BUILDER_NAME` — the name of the cloud builder you created in the [Docker Build Cloud Dashboard](https://app.docker.com/build/)
>
> This ensures your builds authenticate correctly with Docker Build Cloud.

### [GitHub Actions](#github-actions)

```yaml
name: ci

on:
  push:
    branches:
      - "main"

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKER_ACCOUNT }}
          password: ${{ secrets.DOCKER_ACCESS_TOKEN }}
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        with:
          driver: cloud
          endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}" # for example, "acme/default"
      
      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          tags: "IMAGE" # for example, "acme/my-image:latest"
          # For pull requests, export results to the build cache.
          # Otherwise, push to a registry.
          outputs: ${{ github.event_name == 'pull_request' && 'type=cacheonly' || 'type=registry' }}
```

The example above uses `docker/build-push-action`, which automatically uses the builder set up by `setup-buildx-action`. If you need to use the `docker build` command directly instead, you have two options:

* Use `docker buildx build` instead of `docker build`

* Set the `BUILDX_BUILDER` environment variable to use the cloud builder:

  ```yaml
  - name: Set up Docker Buildx
    id: builder
    uses: docker/setup-buildx-action@v4
    with:
      driver: cloud
      endpoint: "${{ vars.DOCKER_ACCOUNT }}/${{ vars.CLOUD_BUILDER_NAME }}"

  - name: Build
    run: |
      docker build .
    env:
      BUILDX_BUILDER: ${{ steps.builder.outputs.name }}
  ```

For more information about the `BUILDX_BUILDER` environment variable, see [Build variables](https://docs.docker.com/build/building/variables/#buildx_builder).

### [GitLab](#gitlab)

```yaml
default:
  image: docker:24-dind
  services:
    - docker:24-dind
  before_script:
    - docker info
    - echo "$DOCKER_ACCESS_TOKEN" | docker login --username "$DOCKER_ACCOUNT" --password-stdin
    - |
      apk add curl jq
      ARCH=${CI_RUNNER_EXECUTABLE_ARCH#*/}
      BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
      mkdir -vp ~/.docker/cli-plugins/
      curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
      chmod a+x ~/.docker/cli-plugins/docker-buildx
    - docker buildx create --use --driver cloud ${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}

variables:
  IMAGE_NAME: IMAGE
  DOCKER_ACCOUNT: DOCKER_ACCOUNT # your Docker Hub organization name (or username when using a personal account)
  CLOUD_BUILDER_NAME: CLOUD_BUILDER_NAME # the name of the cloud builder you created in the [Docker Build Cloud Dashboard](https://app.docker.com/build/)

# Build multi-platform image and push to a registry
build_push:
  stage: build
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}" \
        --push .

# Build an image and discard the result
build_cache:
  stage: build
  script:
    - |
      docker buildx build \
        --platform linux/amd64,linux/arm64 \
        --tag "${IMAGE_NAME}:${CI_COMMIT_SHORT_SHA}" \
        --output type=cacheonly \
        .
```

### [Circle CI](#circle-ci)

```yaml
version: 2.1

jobs:
  # Build multi-platform image and push to a registry
  build_push:
    machine:
      image: ubuntu-2204:current
    steps:
      - checkout

      - run: |
          mkdir -vp ~/.docker/cli-plugins/
          ARCH=amd64
          BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          chmod a+x ~/.docker/cli-plugins/docker-buildx

      - run: echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin
      - run: docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

      - run: |
          docker buildx build \
          --platform linux/amd64,linux/arm64 \
          --push \
          --tag "IMAGE" .

  # Build an image and discard the result
  build_cache:
    machine:
      image: ubuntu-2204:current
    steps:
      - checkout

      - run: |
          mkdir -vp ~/.docker/cli-plugins/
          ARCH=amd64
          BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          chmod a+x ~/.docker/cli-plugins/docker-buildx

      - run: echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin
      - run: docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

      - run: |
          docker buildx build \
          --tag temp \
          --output type=cacheonly \
          .

workflows:
  pull_request:
    jobs:
      - build_cache
  release:
    jobs:
      - build_push
```

### [Buildkite](#buildkite)

The following example sets up a Buildkite pipeline using Docker Build Cloud. The example assumes that the pipeline name is `build-push-docker` and that you manage the Docker access token using environment hooks, but feel free to adapt this to your needs.

Add the following `environment` hook agent's hook directory:

```bash
#!/bin/bash
set -euo pipefail

if [[ "$BUILDKITE_PIPELINE_NAME" == "build-push-docker" ]]; then
 export DOCKER_ACCESS_TOKEN="DOCKER_ACCESS_TOKEN"
fi
```

Create a `pipeline.yml` that uses the `docker-login` plugin:

```yaml
env:
  DOCKER_ACCOUNT: DOCKER_ACCOUNT # your Docker Hub organization name (or username when using a personal account)
  CLOUD_BUILDER_NAME: CLOUD_BUILDER_NAME # the name of the cloud builder you created in the [Docker Build Cloud Dashboard](https://app.docker.com/build/)
  IMAGE_NAME: IMAGE

steps:
  - command: ./build.sh
    key: build-push
    plugins:
      - docker-login#v2.1.0:
          username: DOCKER_ACCOUNT
          password-env: DOCKER_ACCESS_TOKEN # the variable name in the environment hook
```

Create the `build.sh` script:

```bash
DOCKER_DIR=/usr/libexec/docker

# Get download link for latest buildx binary.
# Set $ARCH to the CPU architecture (e.g. amd64, arm64)
UNAME_ARCH=`uname -m`
case $UNAME_ARCH in
  aarch64)
    ARCH="arm64";
    ;;
  amd64)
    ARCH="amd64";
    ;;
  *)
    ARCH="amd64";
    ;;
esac
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")

# Download docker buildx with Build Cloud support
curl --silent -L --output $DOCKER_DIR/cli-plugins/docker-buildx $BUILDX_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx

# Connect to your builder and set it as the default builder
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# Cache-only image build
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --tag "$IMAGE_NAME:$BUILDKITE_COMMIT" \
    --output type=cacheonly \
    .

# Build, tag, and push a multi-arch docker image
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag "$IMAGE_NAME:$BUILDKITE_COMMIT" \
    .
```

### [Jenkins](#jenkins)

```groovy
pipeline {
  agent any

  environment {
    ARCH = 'amd64'
    DOCKER_ACCESS_TOKEN = credentials('docker-access-token')
    DOCKER_ACCOUNT = credentials('docker-account')
    CLOUD_BUILDER_NAME = 'CLOUD_BUILDER_NAME'
    IMAGE_NAME = 'IMAGE'
  }

  stages {
    stage('Build') {
      environment {
        BUILDX_URL = sh (returnStdout: true, script: 'curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\\"linux-$ARCH\\"))"').trim()
      }
      steps {
        sh 'mkdir -vp ~/.docker/cli-plugins/'
        sh 'curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL'
        sh 'chmod a+x ~/.docker/cli-plugins/docker-buildx'
        sh 'echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin'
        sh 'docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"'
        // Cache-only build
        sh 'docker buildx build --platform linux/amd64,linux/arm64 --tag "$IMAGE_NAME" --output type=cacheonly .'
        // Build and push a multi-platform image
        sh 'docker buildx build --platform linux/amd64,linux/arm64 --push --tag "$IMAGE_NAME" .'
      }
    }
  }
}
```

### [Travis CI](#travis-ci)

```yaml
language: minimal 
dist: jammy 

services:
  - docker

env:
  global:
    - IMAGE_NAME=IMAGE # for example, "acme/my-image:latest"

before_install: |
  echo "$DOCKER_ACCESS_TOKEN" | docker login --username "$DOCKER_ACCOUNT" --password-stdin

install: |
  set -e 
  BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$TRAVIS_CPU_ARCH\"))")
  mkdir -vp ~/.docker/cli-plugins/
  curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
  chmod a+x ~/.docker/cli-plugins/docker-buildx
  docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

script: |
  docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --push \
  --tag "$IMAGE_NAME" .
```

### [BitBucket Pipelines](#bitbucket-pipelines)

```yaml
# Prerequisites: $DOCKER_ACCOUNT, $CLOUD_BUILDER_NAME, $DOCKER_ACCESS_TOKEN setup as deployment variables
# This pipeline assumes $BITBUCKET_REPO_SLUG as the image name

image: atlassian/default-image:3

pipelines:
  default:
    - step:
        name: Build multi-platform image
        script:
          - mkdir -vp ~/.docker/cli-plugins/
          - ARCH=amd64
          - BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
          - curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
          - chmod a+x ~/.docker/cli-plugins/docker-buildx
          - echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin
          - docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"
          - IMAGE_NAME=$BITBUCKET_REPO_SLUG
          - docker buildx build
            --platform linux/amd64,linux/arm64
            --push
            --tag "$IMAGE_NAME" .
        services:
          - docker
```

### [Shell script](#shell-script)

```bash
#!/bin/bash

# Get download link for latest buildx binary. Set $ARCH to the CPU architecture (e.g. amd64, arm64)
ARCH=amd64
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")

# Download docker buildx with Build Cloud support
mkdir -vp ~/.docker/cli-plugins/
curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx

# Login to Docker Hub with an access token. See https://docs.docker.com/build-cloud/ci/#creating-access-tokens
echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin

# Connect to your builder and set it as the default builder
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# Cache-only image build
docker buildx build \
    --tag temp \
    --output type=cacheonly \
    .

# Build, tag, and push a multi-arch docker image
docker buildx build \
    --platform linux/amd64,linux/arm64 \
    --push \
    --tag "IMAGE" \
    .
```

### [Docker Compose](#docker-compose)

Use this implementation if you want to use `docker compose build` with Docker Build Cloud in CI.

```bash
#!/bin/bash

# Get download link for latest buildx binary. Set $ARCH to the CPU architecture (e.g. amd64, arm64)
ARCH=amd64
BUILDX_URL=$(curl -s https://raw.githubusercontent.com/docker/actions-toolkit/main/.github/buildx-lab-releases.json | jq -r ".latest.assets[] | select(endswith(\"linux-$ARCH\"))")
COMPOSE_URL=$(curl -sL \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/docker/compose-desktop/releases \
  | jq "[ .[] | select(.prerelease==false and .draft==false) ] | .[0].assets.[] | select(.name | endswith(\"linux-${ARCH}\")) | .browser_download_url")

# Download docker buildx with Build Cloud support
mkdir -vp ~/.docker/cli-plugins/
curl --silent -L --output ~/.docker/cli-plugins/docker-buildx $BUILDX_URL
curl --silent -L --output ~/.docker/cli-plugins/docker-compose $COMPOSE_URL
chmod a+x ~/.docker/cli-plugins/docker-buildx
chmod a+x ~/.docker/cli-plugins/docker-compose

# Login to Docker Hub with an access token. See https://docs.docker.com/build-cloud/ci/#creating-access-tokens
echo "$DOCKER_ACCESS_TOKEN" | docker login --username $DOCKER_ACCOUNT --password-stdin

# Connect to your builder and set it as the default builder
docker buildx create --use --driver cloud "${DOCKER_ACCOUNT}/${CLOUD_BUILDER_NAME}"

# Build the image build
docker compose build
```

----
url: https://docs.docker.com/desktop/use-desktop/
----

# Explore Docker Desktop

***

Table of contents

***

When you open Docker Desktop, the Docker Desktop Dashboard displays.

It provides a centralized interface to manage your [containers](https://docs.docker.com/desktop/use-desktop/container/), [images](https://docs.docker.com/desktop/use-desktop/images/), [volumes](https://docs.docker.com/desktop/use-desktop/volumes/), [builds](https://docs.docker.com/desktop/use-desktop/builds/), [Kubernetes resources](https://docs.docker.com/desktop/use-desktop/kubernetes/), and [logs](https://docs.docker.com/desktop/use-desktop/logs/).

In addition, the Docker Desktop Dashboard lets you:

* Use [Gordon](https://docs.docker.com/ai/gordon/), a personal AI assistant embedded in Docker Desktop and the Docker CLI. It's designed to streamline your workflow and help you make the most of the Docker ecosystem.

* Navigate to the **Settings** menu to configure your Docker Desktop settings. Select the **Settings** icon in the Dashboard header.

* Access the **Troubleshoot** menu to debug and perform restart operations. Select the **Troubleshoot** icon in the Dashboard header.

* Be notified of new releases, installation progress updates, and more in the **Notifications center**. Select the bell icon in the bottom-right corner of the Docker Desktop Dashboard to access the notification center.

* Access the **Learning center** from the Dashboard header. It helps you get started with quick in-app walkthroughs and provides other resources for learning about Docker.

  For a more detailed guide about getting started, see [Get started](https://docs.docker.com/get-started/introduction/).

* Access [Docker Hub](https://docs.docker.com/docker-hub/) to search, browse, pull, run, or view details of images.

* Navigate to [Docker Extensions](https://docs.docker.com/extensions/) if you have enabled it.

> Tip
>
> You can customize the left-hand navigation to show only the tabs that matter to you, and hide the ones that don’t. Right-click the left-hand navigation, select **Customize**, and then select, deselect, or re-order the tabs.

## [Docker terminal](#docker-terminal)

From the Docker Dashboard footer, you can use the integrated terminal directly within Docker Desktop.

The integrated terminal:

* Persists your session if you navigate to another part of the Docker Desktop Dashboard and then return.
* Supports copy, paste, search, and clearing your session.

#### [Open the integrated terminal](#open-the-integrated-terminal)

To open the integrated terminal, either:

* Hover over your running container and under the **Actions** column, select the **Show container actions** menu. From the drop-down menu, select **Open in terminal**.
* Or, select the **Terminal** icon located in the bottom-right corner, next to the version number.

To use your external terminal, navigate to the **General** tab in **Settings** and select the **System default** option under **Choose your terminal**.

## [Quick search](#quick-search)

Use Quick Search, which is located in the Docker Dashboard header, to search for:

* Any container or Compose application on your local system. You can see an overview of associated environment variables or perform quick actions, such as start, stop, or delete.

* Public Docker Hub images, local images, and images from remote repositories (private repositories from organizations you're a part of in Hub). Depending on the type of image you select, you can either pull the image by tag, view documentation, go to Docker Hub for more details, or run a new container using the image.

* Extensions. From here, you can learn more about the extension and install it with a single click. Or, if you already have an extension installed, you can open it straight from the search results.

* Any volume. From here you can view the associated container.

* Docs. Find help from Docker's official documentation straight from Docker Desktop.

## [The Docker menu](#the-docker-menu)

Docker Desktop also includes a tray icon, referred to as the Docker menu for quick access.

Select the icon in your taskbar to open options such as:

* **Dashboard**. This takes you to the Docker Desktop Dashboard.
* **Sign in/Sign up**
* **Settings**
* **Check for updates**
* **Troubleshoot**
* **Give feedback**
* **Switch to Windows containers** (if you're on Windows)
* **About Docker Desktop**. Contains information on the versions you are running, and links to the Subscription Service Agreement for example.
* **Docker Hub**
* **Documentation**
* **Extensions**
* **Kubernetes**
* **Restart**
* **Quit Docker Desktop**

----
url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/cli/
----

# Use MCP Toolkit from the CLI

***

Table of contents

***

Availability: Beta

> Note
>
> The `docker mcp` commands documented here are available in Docker Desktop 4.62 and later. Earlier versions may not support all commands shown.

The `docker mcp` commands let you manage MCP profiles, servers, OAuth credentials, and catalogs from the terminal. Use the CLI for scripting, automation, and headless environments.

## [Profiles](#profiles)

### [Create a profile](#create-a-profile)

```console
$ docker mcp profile create --name <profile-id>
```

The profile ID is used to reference the profile in subsequent commands:

```console
$ docker mcp profile create --name web-dev
```

### [List profiles](#list-profiles)

```console
$ docker mcp profile list
```

### [View a profile](#view-a-profile)

```console
$ docker mcp profile show <profile-id>
```

### [Remove a profile](#remove-a-profile)

```console
$ docker mcp profile remove <profile-id>
```

> Caution
>
> Removing a profile deletes all its server configurations and settings. This action can't be undone.

## [Servers](#servers)

### [Browse the catalog](#browse-the-catalog)

List available servers and their IDs:

```console
$ docker mcp catalog server ls mcp/docker-mcp-catalog
```

The output lists each server by name. The name (for example, `playwright` or `github-official`) is the server ID to use in `catalog://` URIs.

To look up a server ID in Docker Desktop, open **MCP Toolkit** > **Catalog**, select a server, and check the **Server ID** field.

### [Add servers to a profile](#add-servers-to-a-profile)

Servers are referenced by URI. The URI format depends on where the server comes from:

| Format                                | Source                     |
| ------------------------------------- | -------------------------- |
| `catalog://<catalog-ref>/<server-id>` | An OCI catalog             |
| `docker://<image>:<tag>`              | A Docker image             |
| `https://<url>/v0/servers/<uuid>`     | The MCP community registry |
| `file://<path>`                       | A local YAML or JSON file  |

The most common format is `catalog://`, where `<catalog-ref>` matches the **Catalog** field and `<server-id>` matches the **Server ID** field shown in Docker Desktop or in the `catalog server ls` output:

```console
$ docker mcp profile server add <profile-id> \
  --server catalog://<catalog-ref>/<server-id>
```

Add multiple servers in one command:

```console
$ docker mcp profile server add web-dev \
  --server catalog://mcp/docker-mcp-catalog/github-official \
  --server catalog://mcp/docker-mcp-catalog/playwright
```

To add a server defined in a local YAML file:

```console
$ docker mcp profile server add my-profile \
  --server file://./my-server.yaml
```

The YAML file defines the server image and configuration:

```yaml
name: my-server
title: My Server
type: server
image: myimage:latest
description: Description of the server
```

If the server requires OAuth authentication, authorize it in Docker Desktop after adding. See [OAuth authentication](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#oauth-authentication).

### [List servers](#list-servers)

List all servers across all profiles:

```console
$ docker mcp profile server ls
```

Filter by profile:

```console
$ docker mcp profile server ls --filter profile=web-dev
```

### [Remove a server](#remove-a-server)

```console
$ docker mcp profile server remove <profile-id> --name <server-name>
```

Remove multiple servers at once:

```console
$ docker mcp profile server remove web-dev \
  --name github-official \
  --name playwright
```

### [Configure server settings](#configure-server-settings)

Set and retrieve configuration values for servers in a profile:

```console
$ docker mcp profile config <profile-id> --set <server-id>.<key>=<value>
$ docker mcp profile config <profile-id> --get-all
$ docker mcp profile config <profile-id> --del <server-id>.<key>
```

Server configuration keys and their expected values are defined by each server. Check the server's documentation or its entry in Docker Desktop under **MCP Toolkit** > **Catalog** > **Configuration**.

## [Gateway](#gateway)

Run the MCP Gateway with a specific profile:

```console
$ docker mcp gateway run --profile <profile-id>
```

Omit `--profile` to use the default profile.

### [Connect a client manually](#connect-a-client-manually)

To connect any client that isn't listed in Docker Desktop, configure it to run the gateway over `stdio`. For example, in a JSON-based client configuration:

```json
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "web-dev"],
      "type": "stdio"
    }
  }
}
```

For Claude Desktop, the format is:

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "web-dev"]
    }
  }
}
```

### [Connect a named client](#connect-a-named-client)

Connect a supported client to a profile:

```console
$ docker mcp client connect <client> --profile <profile-id>
```

For example, to connect VS Code to a project-specific profile:

```console
$ docker mcp client connect vscode --profile my-project
```

This creates a `.vscode/mcp.json` file in the current directory. Because this is a user-specific file, add it to `.gitignore`:

```console
$ echo ".vscode/mcp.json" >> .gitignore
```

## [Share profiles](#share-profiles)

Share profiles with your team using OCI registries or version control.

### [Share via OCI registry](#share-via-oci-registry)

Profiles are shared as OCI artifacts via any OCI-compatible registry. Credentials are not included for security reasons. Team members configure authentication credentials separately after pulling.

To push an existing profile called `web-dev` to an OCI registry:

```console
$ docker mcp profile push web-dev registry.example.com/profiles/web-dev:v1
```

To pull the same profile:

```console
$ docker mcp profile pull registry.example.com/profiles/team-standard:latest
```

### [Share via version control](#share-via-version-control)

For project-specific profiles, you can use the `export` and `import` commands and store the profiles in version control alongside your code. Team members can import the file to get the same configuration.

To export a profile to your project directory:

```console
$ mkdir -p .docker
$ docker mcp profile export web-dev .docker/mcp-profile.json
```

Team members who clone the repository can import the profile:

```console
$ docker mcp profile import .docker/mcp-profile.json
```

This creates a profile with the servers and configuration defined in the file. Any authentication credentials must be configured separately if needed.

## [Custom catalogs](#custom-catalogs)

Custom catalogs let you curate a focused collection of servers for your team or organization. For an overview of what custom catalogs are and when to use them, see [Custom catalogs](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/#custom-catalogs).

Catalogs are referenced by OCI reference, for example `registry.example.com/mcp/my-catalog:latest`. Servers within a catalog use the same URI schemes as when [adding servers to a profile](#add-servers-to-a-profile).

### [Customize the Docker catalog](#customize-the-docker-catalog)

Use the Docker catalog as a base, then add or remove servers to fit your organization's needs. Copy it first:

```console
$ docker mcp catalog tag mcp/docker-mcp-catalog \
  registry.example.com/mcp/company-tools:latest
```

List the servers it contains:

```console
$ docker mcp catalog server ls registry.example.com/mcp/company-tools:latest
```

Remove servers your organization doesn't approve:

```console
$ docker mcp catalog server remove \
  registry.example.com/mcp/company-tools:latest \
  --name <server-name>
```

Add your own private servers, packaged as Docker images:

```console
$ docker mcp catalog server add registry.example.com/mcp/company-tools:latest \
  --server docker://registry.example.com/mcp/internal-api:latest \
  --server docker://registry.example.com/mcp/data-pipeline:latest
```

Push when ready:

```console
$ docker mcp catalog push registry.example.com/mcp/company-tools:latest
```

### [Build a catalog from scratch](#build-a-catalog-from-scratch)

To include exactly what you choose and nothing else, create a catalog from scratch. You can include servers from the Docker catalog, your own private images, or both.

Create a catalog and specify which servers to include:

```console
$ docker mcp catalog create registry.example.com/mcp/data-tools:latest \
  --title "Data Analysis Tools" \
  --server catalog://mcp/docker-mcp-catalog/sequentialthinking \
  --server catalog://mcp/docker-mcp-catalog/brave \
  --server docker://registry.example.com/mcp/analytics:latest
```

View the result:

```console
$ docker mcp catalog show registry.example.com/mcp/data-tools:latest
```

Push to distribute:

```console
$ docker mcp catalog push registry.example.com/mcp/data-tools:latest
```

### [Distribute a catalog](#distribute-a-catalog)

Push your catalog so team members can import it:

```console
$ docker mcp catalog push <oci-reference>
```

Team members can pull it using the CLI:

```console
$ docker mcp catalog pull <oci-reference>
```

Or import it using Docker Desktop: select **MCP Toolkit** > **Catalog** > **Import catalog** and enter the OCI reference.

### [Use a custom catalog with the gateway](#use-a-custom-catalog-with-the-gateway)

Run the gateway with your catalog instead of the default Docker catalog:

```console
$ docker mcp gateway run --catalog <oci-reference>
```

For [Dynamic MCP](https://docs.docker.com/ai/mcp-catalog-and-toolkit/dynamic-mcp/), where agents discover and add servers during conversations, this limits what agents can find to your curated set.

To enable specific servers from your catalog without using a profile:

```console
$ docker mcp gateway run --catalog <oci-reference> \
  --servers <name1> --servers <name2>
```

## [Further reading](#further-reading)

* [Get started with MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/)
* [MCP Profiles](https://docs.docker.com/ai/mcp-catalog-and-toolkit/profiles/)
* [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
* [MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)

----
url: https://docs.docker.com/reference/cli/docker/scout/integration/delete/
----

# docker scout integration delete

***

| Description | Delete a new integration configuration        |
| ----------- | --------------------------------------------- |
| Usage       | `docker scout integration delete INTEGRATION` |

## [Description](#description)

The docker scout integration delete command deletes a new integration configuration for an organization.

## [Options](#options)

| Option   | Default | Description                                 |
| -------- | ------- | ------------------------------------------- |
| `--name` |         | Name of integration configuration to delete |
| `--org`  |         | Namespace of the Docker organization        |

----
url: https://docs.docker.com/reference/samples/dotnet/
----

# .NET samples

| Name                                                                                                | Description                                                                        |
| --------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| [ASP.NET / MS-SQL](https://github.com/docker/awesome-compose/tree/master/aspnet-mssql)              | A sample ASP.NET core application with MS SQL server database.                     |
| [NGINX / ASP.NET / MySQL](https://github.com/docker/awesome-compose/tree/master/nginx-aspnet-mysql) | A sample Nginx reverse proxy with a C# backend using ASP.NET.                      |
| [example-voting-app](https://github.com/dockersamples/example-voting-app)                           | A sample Docker Compose app.                                                       |
| [dotnet-album-viewer](https://github.com/dockersamples/dotnet-album-viewer)                         | West Wind Album Viewer ASP.NET Core and Angular sample.                            |
| [aspnet-monitoring](https://github.com/dockersamples/aspnet-monitoring)                             | Monitoring ASP.NET Fx applications in Windows Docker containers, using Prometheus. |

----
url: https://docs.docker.com/reference/cli/docker/mcp/feature/enable/
----

# docker mcp feature enable

***

| Description | Enable an experimental feature             |
| ----------- | ------------------------------------------ |
| Usage       | `docker mcp feature enable <feature-name>` |

## [Description](#description)

Enable an experimental feature.

Available features: oauth-interceptor Enable GitHub OAuth flow interception for automatic authentication mcp-oauth-dcr Enable Dynamic Client Registration (DCR) for automatic OAuth client setup dynamic-tools Enable internal MCP management tools (mcp-find, mcp-add, mcp-remove) profiles Enable profile management (docker mcp profile ) tool-name-prefix Prefix all tool names with server name to avoid conflicts

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/
----

# Configure Settings Management with the Admin Console

***

Table of contents

***

Subscription: Business

For: Administrators

Use the Docker Admin Console to create and manage settings policies for Docker Desktop across your organization. Settings policies let you standardize configurations, enforce security requirements, and maintain consistent Docker Desktop environments.

## [Prerequisites](#prerequisites)

Before you begin, make sure you have:

* [Docker Desktop](https://docs.docker.com/desktop/release-notes/) installed
* [A verified domain](/enterprise/security/single-sign-on/connect/#step-1-add-a-domain)
* [Enforced sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) for your organization
* A Docker Business subscription

> Important
>
> You can create settings management policies at any time, but your organization needs to verify a domain before the policies take effect.

## [Create a settings policy](#create-a-settings-policy)

To create a new settings policy:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.

2. Select **Admin Console**, then **Desktop Settings Management**.

3. Select **Create a settings policy**.

4. Provide a name and optional description.

   > Tip
   >
   > You can upload an existing `admin-settings.json` file to pre-fill the form. Admin Console policies override local `admin-settings.json` files.

5. Choose who the policy applies to:

   * All users

   * Specific users

     > Note
     >
     > User-specific policies override global default policies. Test your policy with a small group before applying it organization-wide.

6. Configure each setting using a state:

   | Admin Console state | Description                       | `admin-settings.json` equivalent    |
   | ------------------- | --------------------------------- | ----------------------------------- |
   | **User-defined**    | Users can change the setting      | Omit the setting                    |
   | **Always enabled**  | Setting is on and locked          | `"value": true`, `"locked": true`   |
   | **Enabled**         | Setting is on but can be changed  | `"value": true`, `"locked": false`  |
   | **Always disabled** | Setting is off and locked         | `"value": false`, `"locked": true`  |
   | **Disabled**        | Setting is off but can be changed | `"value": false`, `"locked": false` |

   > Tip
   >
   > For a complete list of configurable settings, supported platforms, and configuration methods, see the [Settings reference](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/settings-reference/).

7. Select **Create** to save your policy.

## [Apply the policy](#apply-the-policy)

Settings policies take effect after Docker Desktop restarts and users sign in.

For new installations:

1. Launch Docker Desktop.
2. Sign in with your Docker account.

For existing installations:

1. Quit Docker Desktop completely.
2. Relaunch Docker Desktop.

> Important
>
> Users must fully quit and reopen Docker Desktop. Restarting from the Docker Desktop menu isn't sufficient.

Docker Desktop checks for policy updates when it launches and every 60 minutes while running.

## [Verify applied settings](#verify-applied-settings)

After you apply policies:

* Docker Desktop displays most settings as greyed out
* Some settings, particularly Enhanced Container Isolation configurations, may not appear in the GUI
* You can verify all applied settings by checking the [`settings-store.json` file](https://docs.docker.com/desktop/settings-and-maintenance/settings/) on your system

## [Manage existing policies](#manage-existing-policies)

From the **Desktop Settings Management** page in the Admin Console, use the **Actions** menu to:

* Edit or delete an existing settings policy
* Export a settings policy as an `admin-settings.json` file
* Promote a user-specific policy to be the new global default

## [Roll back policies](#roll-back-policies)

To roll back a settings policy:

* Complete rollback: Delete the entire policy.
* Partial rollback: Set specific settings to **User-defined**.

When you roll back settings, users regain control over those settings configurations.

----
url: https://docs.docker.com/guides/postgresql/companions-for-postgresql/
----

# Companions for PostgreSQL

***

Table of contents

***

## [PostgreSQL ecosystem companions: pgAdmin, PgBouncer, and performance testing](#postgresql-ecosystem-companions-pgadmin-pgbouncer-and-performance-testing)

Running a standalone PostgreSQL container is often just the beginning. What happens when thousands of connections arrive, or when you need a visual interface to manage your database?

This is where **companion tools** come into play. These applications extend PostgreSQL with capabilities the core database engine doesn't provide natively: visual administration, connection pooling, and performance benchmarking. This guide covers how to deploy pgAdmin 4, PgBouncer, Pgpool-II, and `pgbench` in Docker, when to use each tool, and real-world benchmark results demonstrating their performance impact.

## [pgAdmin 4: Visual management platform](#pgadmin-4-visual-management-platform)

pgAdmin 4 is the industry-standard open source management tool for PostgreSQL. When deployed in Docker, it typically runs in **Server Mode**, providing a multi-user web interface to manage one or more database instances.

While you can accomplish everything from the command line using `psql`, a visual interface significantly simplifies writing complex queries, visualizing table structures, and exploring database objects.

### [Key considerations](#key-considerations)

When running pgAdmin in Docker, keep these points in mind:

* **Image**: Use the official `dpage/pgadmin4` image
* **Networking**: In a Docker Compose environment, pgAdmin connects to the database using the internal service name (for example, `db:5432`) rather than `localhost`

### [Docker Compose configuration](#docker-compose-configuration)

To quickly deploy pgAdmin:

```yaml
pgadmin:
  image: dpage/pgadmin4:8.14
  environment:
    PGADMIN_DEFAULT_EMAIL: admin@example.com
    PGADMIN_DEFAULT_PASSWORD: secure_password
  volumes:
    - pgadmin_data:/var/lib/pgadmin
  ports:
    - "8080:80"
```

With this configuration, access the pgAdmin interface at `http://localhost:8080`. Use the email and password specified in the environment variables for initial sign in.

> Important
>
> In production environments, pass `PGADMIN_DEFAULT_PASSWORD` as an external environment variable or use Docker secrets. Storing passwords in plain text within `docker-compose.yml` poses a security risk.

Now that you have visual database management in place, the next challenge in production environments is handling connection load. The following section explains how to manage high-volume database traffic.

## [PgBouncer: Lightweight connection pooling](#pgbouncer-lightweight-connection-pooling)

PostgreSQL creates a new process for every client connection, which consumes significant RAM. What happens when you have 1,000 concurrent users? PgBouncer solves exactly this problem.

PgBouncer is a lightweight proxy that pools connections, allowing thousands of applications to share a small number of actual database backends. Think of it as a traffic controller: everyone wants to pass through simultaneously, but the controller regulates the flow to prevent congestion.

### [Pooling modes](#pooling-modes)

PgBouncer offers three distinct pooling modes:

| Mode            | Description                                     | Use case                                        |
| --------------- | ----------------------------------------------- | ----------------------------------------------- |
| **Session**     | Connection assigned for entire session duration | Long-lived connections, session variables       |
| **Transaction** | Connection returned after each transaction ends | Web applications, microservices (most common)   |
| **Statement**   | Connection returned after every SQL statement   | Simple queries, no multi-statement transactions |

### [When to use PgBouncer](#when-to-use-pgbouncer)

PgBouncer becomes essential when you encounter:

* "too many connections" errors
* High memory consumption due to connection overhead
* Many short-lived connections (web applications, serverless functions)
* Need to serve thousands of clients with limited database connections

### [Complete Docker Compose setup](#complete-docker-compose-setup)

To run PostgreSQL and PgBouncer together, you need three files: `docker-compose.yml`, `pgbouncer.ini`, and `userlist.txt`.

First, create the PgBouncer configuration file (`pgbouncer.ini`):

```bash
[databases]
benchmark = host=postgres port=5432 dbname=benchmark user=postgres

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = trust
auth_file = /etc/pgbouncer/userlist.txt
admin_users = postgres
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 50
min_pool_size = 10
reserve_pool_size = 10
max_db_connections = 100
```

Next, create the user authentication file (`userlist.txt`):

```bash
"postgres" "postgres"
```

Finally, create the Docker Compose file (`docker-compose.yml`):

```yaml
services:
  postgres:
    image: postgres:18
    container_name: postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: benchmark
      POSTGRES_HOST_AUTH_METHOD: trust
    volumes:
      - postgres_data:/var/lib/postgresql
    ports:
      - "5432:5432"
    networks:
      - pgnet
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5

  pgbouncer:
    image: percona/percona-pgbouncer:1.25.0
    container_name: pgbouncer
    volumes:
      - ./pgbouncer.ini:/etc/pgbouncer/pgbouncer.ini
      - ./userlist.txt:/etc/pgbouncer/userlist.txt
    ports:
      - "6432:6432"
    networks:
      - pgnet
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:

networks:
  pgnet:
    driver: bridge
```

Key configuration notes:

* `PgBouncer` listens on port **6432**, avoiding confusion with the direct PostgreSQL connection on port 5432
* The `depends_on` directive with `service_healthy` condition ensures PgBouncer starts only after PostgreSQL is ready
* `pool_mode = transaction` is the optimal choice for most web applications
* The [Percona PgBouncer image](https://hub.docker.com/r/percona/percona-pgbouncer) requires mounted configuration files (without the `:ro` flag, as the entrypoint script needs to modify them)
* This example uses `trust` authentication for simplicity. In production, configure proper SCRAM-SHA-256 authentication

> Note
>
> The `Percona PgBouncer` entrypoint script processes the configuration files on startup. Mount them without the read-only flag to avoid permission errors.

## [`pgbench`: Performance benchmarking](#pgbench-performance-benchmarking)

`pgbench` is a benchmarking utility included with the official PostgreSQL image. It allows you to simulate heavy workloads and verify how your Docker configuration performs under pressure.

### [Initialize benchmark tables](#initialize-benchmark-tables)

First, create the test tables. The `-s` (scale) parameter determines data size—scale factor 50 creates approximately 5 million rows:

```bash
docker exec postgres pgbench -i -s 50 -U postgres benchmark
```

### [Run stress tests](#run-stress-tests)

Key parameters:

* `-c`: Number of simulated clients
* `-j`: Number of threads
* `-T`: Duration in seconds

Test with direct PostgreSQL connection:

```bash
docker exec postgres pgbench -h localhost -U postgres -c 50 -j 4 -T 60 benchmark
```

Test through PgBouncer:

```bash
docker exec postgres pgbench -h pgbouncer -p 6432 -U postgres -c 50 -j 4 -T 60 benchmark
```

## [Understanding benchmark results](#understanding-benchmark-results)

Does PgBouncer actually make a difference? Run the benchmarks yourself to find out. Your results will vary based on your hardware, Docker configuration, network setup, and system load.

### [What to expect](#what-to-expect)

When you run these benchmarks, you'll observe patterns rather than specific numbers. Think of it like comparing two different routes to work: the "faster" route depends on traffic conditions, time of day, and your vehicle.

### [Key observations](#key-observations)

When comparing direct connections versus PgBouncer, you'll typically notice:

#### [1. Connection overhead differs significantly](#1-connection-overhead-differs-significantly)

Direct connections require PostgreSQL to spawn a new process for each client. PgBouncer reuses existing connections. Watch the "initial connection time" metric in your results—PgBouncer often shows dramatically faster connection setup.

#### [2. Behavior under pressure reveals the real difference](#2-behavior-under-pressure-reveals-the-real-difference)

Try increasing the client count (`-c` parameter) gradually: 50, 100, 150, 200. At some point, direct connections will fail with "too many clients already" while PgBouncer continues handling requests. This is PgBouncer's primary value: **it prevents connection exhaustion**.

#### [3. Throughput varies by environment](#3-throughput-varies-by-environment)

On some systems, direct connections show higher transactions per second (TPS) at low concurrency. On others, PgBouncer wins even with few clients. The difference depends on:

* CPU and memory available
* Docker networking overhead
* Disk I/O speed
* Whether connections are being rapidly opened and closed

----
url: https://docs.docker.com/desktop/features/networking/networking-how-tos/
----

# Explore networking how-tos on Docker Desktop

***

Table of contents

***

This page explains how to configure and use networking features, connect containers to host services, work behind proxies or VPNs, and troubleshoot common issues.

For details on how Docker Desktop routes network traffic and file I/O between containers, the VM, and the host, see [Network overview](https://docs.docker.com/desktop/features/networking/#overview).

## [Core networking how-tos](#core-networking-how-tos)

### [Connect a container to a service on the host](#connect-a-container-to-a-service-on-the-host)

The host has a changing IP address, or none if you have no network access. To connect to services running on your host, use the special DNS name:

| Name                      | Description                                      |
| ------------------------- | ------------------------------------------------ |
| `host.docker.internal`    | Resolves to the internal IP address of your host |
| `gateway.docker.internal` | Resolves to the gateway IP of the Docker VM      |

#### [Example](#example)

Run a simple HTTP server on port `8000`:

```console
$ python -m http.server 8000
```

Then run a container, install `curl`, and try to connect to the host using the following commands:

```console
$ docker run --rm -it alpine sh
# apk add curl
# curl http://host.docker.internal:8000
# exit
```

### [Connect to a container from the host](#connect-to-a-container-from-the-host)

To access containerized services from your host or local network, publish ports with the `-p` or `--publish` flag. For example:

```console
$ docker run -d -p 80:80 --name webserver nginx
```

Docker Desktop makes whatever is running on port `80` in the container, in this case, `nginx`, available on port `80` of `localhost`.

> Tip
>
> The syntax for `-p` is `HOST_PORT:CLIENT_PORT`.

To publish all ports, use the `-P` flag. For example, the following command starts a container (in detached mode) and the `-P` flag publishes all exposed ports of the container to random ports on the host.

```console
$ docker run -d -P --name webserver nginx
```

Alternatively, you can also use [host networking](https://docs.docker.com/engine/network/drivers/host/#docker-desktop) to give the container direct access to the network stack of the host.

See the [run command](/reference/cli/docker/container/run/) for more details on publish options used with `docker run`.

All inbound connections pass through the Docker Desktop backend process (`com.docker.backend` (Mac), `com.docker.backend` (Windows), or `qemu` (Linux), which handles port forwarding into the VM. For more details, see [How exposed ports work](https://docs.docker.com/desktop/features/networking/#how-exposed-ports-work)

### [Working with VPNs](#working-with-vpns)

Docker Desktop networking can work when attached to a VPN.

To do this, Docker Desktop intercepts traffic from the containers and injects it into the host as if it originated from the Docker application.

For details about how this traffic appears to host firewalls and endpoint detection systems, see [Firewalls and endpoint visibility](https://docs.docker.com/desktop/features/networking/#firewalls-and-endpoint-visibility).

### [Working with proxies](#working-with-proxies)

Docker Desktop can use your system proxy or a manual configuration. To configure proxies:

1. Navigate to the **Resources** tab in **Settings**.
2. From the dropdown menu select **Proxies**.
3. Switch on the **Manual proxy configuration** toggle.
4. Enter your HTTP, HTTPS or SOCKS5 proxy URLS.

For more details on proxies and proxy configurations, see the [Proxy settings documentation](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

## [Network how-tos for Mac and Windows](#network-how-tos-for-mac-and-windows)

You can control how Docker handles container networking and DNS resolution to better support a range of environments — from IPv4-only to dual-stack and IPv6-only systems. These settings help prevent timeouts and connectivity issues caused by incompatible or misconfigured host networks.

You can set the following settings on the **Network** tab in the Docker Desktop Dashboard settings, or if you're an admin, with Settings Management via the [`admin-settings.json` file](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/#networking), or the [Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/)

> Note
>
> These settings can be overridden on a per-network basis using CLI flags or Compose file options.

### [Default networking mode](#default-networking-mode)

Choose the default IP protocol used when Docker creates new networks. This allows you to align Docker with your host’s network capabilities or organizational requirements, such as enforcing IPv6-only access.

| Mode                         | Description                                 |
| ---------------------------- | ------------------------------------------- |
| **Dual IPv4/IPv6 (default)** | Supports both IPv4 and IPv6. Most flexible. |
| **IPv4 only**                | Uses only IPv4 addressing.                  |
| **IPv6 only**                | Uses only IPv6 addressing.                  |

### [DNS resolution behavior](#dns-resolution-behavior)

Control how Docker filters DNS records returned to containers, improving reliability in environments where only IPv4 or IPv6 is supported. This setting is especially useful for preventing apps from trying to connect using IP families that aren't actually available, which can cause avoidable delays or failures.

| Option                         | Description                                                                 |
| ------------------------------ | --------------------------------------------------------------------------- |
| **Auto (recommended)**         | Automatically filters unsupported record types. (A for IPv4, AAAA for IPv6) |
| **Filter IPv4 (A records)**    | Blocks IPv4 lookups. Only available in dual-stack mode.                     |
| **Filter IPv6 (AAAA records)** | Blocks IPv6 lookups. Only available in dual-stack mode.                     |
| **No filtering**               | Returns both A and AAAA records.                                            |

> Important
>
> Switching the default networking mode resets the DNS filter to Auto.

## [Network how-tos for Mac and Linux](#network-how-tos-for-mac-and-linux)

### [SSH agent forwarding](#ssh-agent-forwarding)

Docker Desktop for Mac and Linux lets you use the host’s SSH agent inside a container. To do this:

1. Bind mount the SSH agent socket by adding the following parameter to your `docker run` command:

   ```console
   $--mount type=bind,src=/run/host-services/ssh-auth.sock,target=/run/host-services/ssh-auth.sock
   ```

2. Add the `SSH_AUTH_SOCK` environment variable in your container:

   ```console
   $ -e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock"
   ```

To enable the SSH agent in Docker Compose, add the following flags to your service:

```yaml
services:
 web:
   image: nginx:alpine
   volumes:
     - type: bind
       source: /run/host-services/ssh-auth.sock
       target: /run/host-services/ssh-auth.sock
   environment:
     - SSH_AUTH_SOCK=/run/host-services/ssh-auth.sock
```

## [Known limitations](#known-limitations)

### [Changing internal IP addresses](#changing-internal-ip-addresses)

The internal IP addresses used by Docker can be changed from **Settings**. After changing IPs, you need to reset the Kubernetes cluster and to leave any active Swarm.

### [There is no `docker0` bridge on the host](#there-is-no-docker0-bridge-on-the-host)

Because of the way networking is implemented in Docker Desktop, you cannot see a `docker0` interface on the host. This interface is actually within the virtual machine.

### [I cannot ping my containers](#i-cannot-ping-my-containers)

Docker Desktop can't route traffic to Linux containers. However if you're a Windows user, you can ping the Windows containers.

### [Per-container IP addressing is not possible](#per-container-ip-addressing-is-not-possible)

This is because the Docker `bridge` network is not reachable from the host. However if you are a Windows user, per-container IP addressing is possible with Windows containers.

----
url: https://docs.docker.com/guides/deno/deploy/
----

# Test your Deno deployment

***

Table of contents

***

## [Prerequisites](#prerequisites)

* Complete all the previous sections of this guide, starting with [Containerize a Deno application](https://docs.docker.com/guides/deno/containerize/).
* [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## [Overview](#overview)

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## [Create a Kubernetes YAML file](#create-a-kubernetes-yaml-file)

In your `deno-docker` directory, create a file named `docker-kubernetes.yml`. Open the file in an IDE or text editor and add the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker username and the name of the repository that you created in [Configure CI/CD for your Deno application](https://docs.docker.com/guides/deno/configure-ci-cd/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: docker-deno-demo
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: deno-api
  template:
    metadata:
      labels:
        app: deno-api
    spec:
      containers:
       - name: deno-api
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
    app: deno-api
  ports:
  - port: 8000
    targetPort: 8000
    nodePort: 30001
```

In this Kubernetes YAML file, there are two objects, separated by the `---`:

* A Deployment, describing a scalable group of identical pods. In this case, you'll get just one replica, or copy of your pod. That pod, which is described under `template`, has just one container in it. The container is created from the image built by GitHub Actions in [Configure CI/CD for your Deno application](https://docs.docker.com/guides/deno/configure-ci-cd/).
* A NodePort service, which will route traffic from port 30001 on your host to port 8000 inside the pods it routes to, allowing you to reach your app from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## [Deploy and check your application](#deploy-and-check-your-application)

1. In a terminal, navigate to `deno-docker` and deploy your application to Kubernetes.

   ```console
   $ kubectl apply -f docker-kubernetes.yml
   ```

   You should see output that looks like the following, indicating your Kubernetes objects were created successfully.

   ```text
   deployment.apps/docker-deno-demo created
   service/service-entrypoint created
   ```

2. Make sure everything worked by listing your deployments.

   ```console
   $ kubectl get deployments
   ```

   Your deployment should be listed as follows:

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE    AGE
   docker-deno-demo       1/1     1            1           10s
   ```

   This indicates all one of the pods you asked for in your YAML are up and running. Do the same check for your services.

   ```console
   $ kubectl get services
   ```

   You should get output like the following.

   ```shell
   NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   kubernetes           ClusterIP   10.96.0.1        <none>        443/TCP          88m
   service-entrypoint   NodePort    10.105.145.223   <none>        8000:30001/TCP   83s
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

In this section, you learned how to use Docker Desktop to deploy your Deno application to a fully-featured Kubernetes environment on your development machine.

----
url: https://docs.docker.com/engine/release-notes/25.0/
----

# Docker Engine 25.0 release notes

***

Table of contents

***

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 25.0.

For more information about:

* Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
* Changes to the Engine API, see [Engine API version history](/reference/api/engine/version-history/).

## [25.0.5](#2505)

*2024-03-19*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 25.0.5 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.5)
* [moby/moby, 25.0.5 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.5)

### [Security](#security)

This release contains a security fix for [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx), a potential data exfiltration from 'internal' networks via authoritative DNS servers.

### [Bug fixes and enhancements](#bug-fixes-and-enhancements)

* [CVE-2024-29018](https://github.com/moby/moby/security/advisories/GHSA-mq39-4gv4-mvpx): Do not forward requests to external DNS servers for a container that is only connected to an 'internal' network. Previously, requests were forwarded if the host's DNS server was running on a loopback address, like systemd's 127.0.0.53. [moby/moby#47589](https://github.com/moby/moby/pull/47589)

* plugin: fix mounting /etc/hosts when running in UserNS. [moby/moby#47588](https://github.com/moby/moby/pull/47588)

* rootless: fix `open /etc/docker/plugins: permission denied`. [moby/moby#47587](https://github.com/moby/moby/pull/47587)

* Fix multiple parallel `docker build` runs leaking disk space. [moby/moby#47527](https://github.com/moby/moby/pull/47527)

## [25.0.4](#2504)

*2024-03-07*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 25.0.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.4)
* [moby/moby, 25.0.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.4)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-1)

* Restore DNS names for containers in the default "nat" network on Windows. [moby/moby#47490](https://github.com/moby/moby/pull/47490)
* Fix `docker start` failing when used with `--checkpoint` [moby/moby#47466](https://github.com/moby/moby/pull/47466)
* Don't enforce new validation rules for existing swarm networks [moby/moby#47482](https://github.com/moby/moby/pull/47482)
* Restore IP connectivity between the host and containers on an internal bridge network. [moby/moby#47481](https://github.com/moby/moby/pull/47481)
* Fix a regression introduced in v25.0 that prevented the classic builder from adding tar archive with `xattrs` created on a non-Linux OS [moby/moby#47483](https://github.com/moby/moby/pull/47483)
* containerd image store: Fix image pull not emitting `Pulling fs layer status` [moby/moby#47484](https://github.com/moby/moby/pull/47484)
* API: To preserve backwards compatibility, make read-only mounts non-recursive by default when using older clients (API versions < v1.44). [moby/moby#47393](https://github.com/moby/moby/pull/47393)
* API: `GET /images/{id}/json` omits the `Created` field (previously it was `0001-01-01T00:00:00Z`) if the `Created` field was missing from the image config. [moby/moby#47451](https://github.com/moby/moby/pull/47451)
* API: Populate a missing `Created` field in `GET /images/{id}/json` with `0001-01-01T00:00:00Z` for API versions <= 1.43. [moby/moby#47387](https://github.com/moby/moby/pull/47387)
* API: Fix a regression that caused API socket connection failures to report an API version negotiation failure instead. [moby/moby#47470](https://github.com/moby/moby/pull/47470)
* API: Preserve supplied endpoint configuration in a container-create API request, when a container-wide MAC address is specified, but `NetworkMode` name or id is not the same as the name or id used in `NetworkSettings.Networks`. [moby/moby#47510](https://github.com/moby/moby/pull/47510)

### [Packaging updates](#packaging-updates)

* Upgrade Go runtime to 1.21.8. [moby/moby#47503](https://github.com/moby/moby/pull/47503)
* Upgrade RootlessKit to v2.0.2. [moby/moby#47508](https://github.com/moby/moby/pull/47508)
* Upgrade Compose to v2.24.7. [docker/docker-ce-packaging#998](https://github.com/moby/moby/pull/998)
* Upgrade Buildx to v0.13.0. [docker/docker-ce-packaging#997](https://github.com/moby/moby/pull/997)

## [25.0.3](#2503)

*2024-02-06*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 25.0.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.3)
* [moby/moby, 25.0.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.3)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-2)

* containerd image store: Fix a bug where `docker image history` would fail if a manifest wasn't found in the content store. [moby/moby#47348](https://github.com/moby/moby/pull/47348)

* Ensure that a generated MAC address is not restored when a container is restarted, but a configured MAC address is preserved. [moby/moby#47304](https://github.com/moby/moby/pull/47304)

  > Note
  >
  > * Containers created with Docker Engine version 25.0.0 may have duplicate MAC addresses. They must be re-created.
  > * Containers with user-defined MAC addresses created with Docker Engine versions 25.0.0 or 25.0.1 receive new MAC addresses when started using Docker Engine version 25.0.2. They must also be re-created.

* Fix `docker save <image>@<digest>` producing an OCI archive with index without manifests. [moby/moby#47294](https://github.com/moby/moby/pull/47294)

* Fix a bug preventing bridge networks from being created with an MTU higher than 1500 on RHEL and CentOS 7. [moby/moby#47308](https://github.com/moby/moby/issues/47308), [moby/moby#47311](https://github.com/moby/moby/pull/47311)

* Fix a bug where containers are unable to communicate over an `internal` network. [moby/moby#47303](https://github.com/moby/moby/pull/47303)

* Fix a bug where the value of the `ipv6` daemon option was ignored. [moby/moby#47310](https://github.com/moby/moby/pull/47310)

* Fix a bug where trying to install a pulling using a digest revision would cause a panic. [moby/moby#47323](https://github.com/moby/moby/pull/47323)

* Fix a potential race condition in the managed containerd supervisor. [moby/moby#47313](https://github.com/moby/moby/pull/47313)

* Fix an issue with the `journald` log driver preventing container logs from being followed correctly with systemd version 255. [moby/moby#47243](https://github.com/moby/moby/pull/47243)

* seccomp: Update the builtin seccomp profile to include syscalls added in kernel v5.17 - v6.7 to align the profile with the profile used by containerd. [moby/moby#47341](https://github.com/moby/moby/pull/47341)

* Windows: Fix cache not being used when building images based on Windows versions older than the host's version. [moby/moby#47307](https://github.com/moby/moby/pull/47307), [moby/moby#47337](https://github.com/moby/moby/pull/47337)

### [Packaging updates](#packaging-updates-1)

* Removed support for Ubuntu Lunar (23.04). [docker/ce-packaging#986](https://github.com/docker/docker-ce-packaging/pull/986)

## [25.0.2](#2502)

*2024-01-31*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 25.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.2)
* [moby/moby, 25.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.2)

### [Security](#security-1)

This release contains security fixes for the following CVEs affecting Docker Engine and its components.

| CVE                                                         | Component     | Fix version | Severity         |
| ----------------------------------------------------------- | ------------- | ----------- | ---------------- |
| [CVE-2024-21626](https://scout.docker.com/v/CVE-2024-21626) | runc          | 1.1.12      | High, CVSS 8.6   |
| [CVE-2024-23651](https://scout.docker.com/v/CVE-2024-23651) | BuildKit      | 1.12.5      | High, CVSS 8.7   |
| [CVE-2024-23652](https://scout.docker.com/v/CVE-2024-23652) | BuildKit      | 1.12.5      | High, CVSS 8.7   |
| [CVE-2024-23653](https://scout.docker.com/v/CVE-2024-23653) | BuildKit      | 1.12.5      | High, CVSS 7.7   |
| [CVE-2024-23650](https://scout.docker.com/v/CVE-2024-23650) | BuildKit      | 1.12.5      | Medium, CVSS 5.5 |
| [CVE-2024-24557](https://scout.docker.com/v/CVE-2024-24557) | Docker Engine | 25.0.2      | Medium, CVSS 6.9 |

The potential impacts of the above vulnerabilities include:

* Unauthorized access to the host filesystem
* Compromising the integrity of the build cache
* In the case of CVE-2024-21626, a scenario that could lead to full container escape

For more information about the security issues addressed in this release, refer to the [blog post](https://www.docker.com/blog/docker-security-advisory-multiple-vulnerabilities-in-runc-buildkit-and-moby/). For details about each vulnerability, see the relevant security advisory:

* [CVE-2024-21626](https://github.com/opencontainers/runc/security/advisories/GHSA-xr7r-f8xq-vfvv)
* [CVE-2024-23651](https://github.com/moby/buildkit/security/advisories/GHSA-m3r6-h7wv-7xxv)
* [CVE-2024-23652](https://github.com/moby/buildkit/security/advisories/GHSA-4v98-7qmw-rqr8)
* [CVE-2024-23653](https://github.com/moby/buildkit/security/advisories/GHSA-wr6v-9f75-vh2g)
* [CVE-2024-23650](https://github.com/moby/buildkit/security/advisories/GHSA-9p26-698r-w4hx)
* [CVE-2024-24557](https://github.com/moby/moby/security/advisories/GHSA-xw73-rw38-6vjc)

### [Packaging updates](#packaging-updates-2)

* Upgrade containerd to [v1.6.28](https://github.com/containerd/containerd/releases/tag/v1.6.28).
* Upgrade containerd to v1.7.13 (static binaries only). [moby/moby#47280](https://github.com/moby/moby/pull/47280)
* Upgrade runc to v1.1.12. [moby/moby#47269](https://github.com/moby/moby/pull/47269)
* Upgrade Compose to v2.24.5. [docker/docker-ce-packaging#985](https://github.com/docker/docker-ce-packaging/pull/985)
* Upgrade BuildKit to v0.12.5. [moby/moby#47273](https://github.com/moby/moby/pull/47273)

## [25.0.1](#2501)

*2024-01-23*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 25.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.1)
* [moby/moby, 25.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.1)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-3)

* API: Fix incorrect HTTP status code for containers with an invalid network configuration created before upgrading to Docker Engine v25.0. [moby/moby#47159](https://github.com/moby/moby/pull/47159)
* Ensure that a MAC address based on a container's IP address is re-generated when the container is stopped and restarted, in case the generated IP/MAC addresses have been reused. [moby/moby#47171](https://github.com/moby/moby/pull/47171)
* Fix `host-gateway-ip` not working during build when not set through configuration. [moby/moby#47192](https://github.com/moby/moby/pull/47192)
* Fix a bug that prevented a container from being renamed twice. [moby/moby#47196](https://github.com/moby/moby/pull/47196)
* Fix an issue causing containers to have their short ID added to their network alias when inspecting them. [moby/moby#47182](https://github.com/moby/moby/pull/47182)
* Fix an issue in detecting whether a remote build context is a Git repository. [moby/moby#47136](https://github.com/moby/moby/pull/47136)
* Fix an issue with layers order in OCI manifests. [moby/moby#47150](https://github.com/moby/moby/issues/47150)
* Fix volume mount error when passing an `addr` or `ip` mount option. [moby/moby#47185](https://github.com/moby/moby/pull/47185)
* Improve error message related to extended attributes that can't be set due to improperly namespaced attribute names. [moby/moby#47178](https://github.com/moby/moby/pull/47178)
* Swarm: Fixed `start_interval` not being passed to the container config. [moby/moby#47163](https://github.com/moby/moby/pull/47163)

### [Packaging updates](#packaging-updates-3)

* Upgrade Compose to `2.24.2`. [docker/docker-ce-packaging#981](https://github.com/docker/docker-ce-packaging/pull/981)

## [25.0.0](#2500)

*2024-01-19*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 25.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A25.0.0)
* [moby/moby, 25.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A25.0.0)

> Note
>
> In earlier versions of Docker Engine, recursive mounts (submounts) would always be mounted as writable, even when specifying a read-only mount. This behavior has changed in v25.0.0, for hosts running on kernel version 5.12 or later. Now, read-only bind mounts are **recursively read-only** by default.
>
> To get the same behavior as earlier releases, you can specify the `bind-recursive` option for the `--mount` flag.
>
> ```console
> $ docker run --mount type=bind,src=SRC,dst=DST,readonly,bind-recursive=writable IMAGE
> ```
>
> This option isn't supported with the `-v` or `--volume` flag. For more information, see [Recursive mounts](https://docs.docker.com/engine/storage/bind-mounts/#recursive-mounts).

### [New](#new)

* The daemon now uses systemd's default `LimitNOFILE`. In earlier versions of Docker Engine, this limit was set to `infinity`. This would cause issues with recent versions of systemd, where the hard limit was increased, causing programs that adjusted their behaviors based on ulimits to consume a high amount of memory. [moby/moby#45534](https://github.com/moby/moby/pull/45534)

  The new setting makes containers behave the same way as programs running on the host, but may cause programs that make incorrect assumptions based on the soft limit to misbehave. To get the previous behavior, you can set `LimitNOFILE=1048576`.

  This change currently only affects build containers created with `docker build` when using BuildKit with the `docker` driver. Starting with Docker Engine v29.0 (containerd v2.1.5), this limit applies to all containers, not only build containers.

  If you're experiencing issues with the higher ulimit in systemd v240 or later, consider adding a system `drop-in` or `override` file to configure the ulimit settings for your setup. The [Flatcar Container Linux documentation](https://www.flatcar.org/docs/latest/setup/systemd/drop-in-units/) has a great article covering this topic in detail.

* Add OpenTelemetry tracing. [moby/moby#45652](https://github.com/moby/moby/pull/45652), [moby/moby#45579](https://github.com/moby/moby/pull/45579)

* Add support for CDI devices under Linux. [moby/moby#45134](https://github.com/moby/moby/pull/45134), [docker/cli#4510](https://github.com/docker/cli/pull/4510), [moby/moby#46004](https://github.com/moby/moby/pull/46004)

* Add an additional interval to be used by healthchecks during the container start period. [moby/moby#40894](https://github.com/moby/moby/pull/40894), [docker/cli#4405](https://github.com/docker/cli/pull/4405), [moby/moby#45965](https://github.com/moby/moby/pull/45965)

* Add a `--log-format` flag to `dockerd` to control the logging format: text (default) or JSON. [moby/moby#45737](https://github.com/moby/moby/pull/45737)

* Add support for recursive read-only mounts. [moby/moby#45278](https://github.com/moby/moby/pull/45278), [moby/moby#46037](https://github.com/moby/moby/pull/46037)

* Add support for filtering images based on timestamp with `docker image ls --filter=until=<timestamp>`. [moby/moby#46577](https://github.com/moby/moby/pull/46577)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-4)

* API: Fix error message for invalid policies at `ValidateRestartPolicy`. [moby/moby#46352](https://github.com/moby/moby/pull/46352)
* API: Update `/info` endpoint to use singleflight. [moby/moby#45847](https://github.com/moby/moby/pull/45847)
* Add an error message for when specifying a Dockerfile filename with `-f`, and also using `stdin`. [docker/cli#4346](https://github.com/docker/cli/pull/4346)
* Add support for `mac-address` and `link-local-ip` fields in `--network` long format. [docker/cli#4419](https://github.com/docker/cli/pull/4419)
* Add support for specifying multiple `--network` flags with `docker container create` and `docker run`. [moby/moby#45906](https://github.com/moby/moby/pull/45906)
* Automatically enable IPv6 on a network when an IPv6 subnet is specified. [moby/moby#46455](https://github.com/moby/moby/pull/46455)
* Add support for overlay networks over IPv6 transport. [moby/moby#46790](https://github.com/moby/moby/pull/46790)
* Configuration reloading is now more robust: if there's an error during the configuration reload process, no configuration changes are applied. [moby/moby#43980](https://github.com/moby/moby/pull/43980)
* Live restore: Containers with auto remove (`docker run --rm`) are no longer forcibly removed on engine restart. [moby/moby#46857](https://github.com/moby/moby/pull/46857)
* Live restore: containers that are live-restored will now be given another health-check start period when the daemon restarts. [moby/moby#47051](https://github.com/moby/moby/pull/47051)
* Container health status is flushed to disk less frequently, reducing wear on flash storage. [moby/moby#47044](https://github.com/moby/moby/pull/47044)
* Ensure network names are unique. [moby/moby#46251](https://github.com/moby/moby/pull/46251)
* Ensure that overlay2 layer metadata is correct. [moby/moby#46471](https://github.com/moby/moby/pull/46471)
* Fix `Downloading` progress message on image pull. [moby/moby#46515](https://github.com/moby/moby/pull/46515)
* Fix `NetworkConnect` and `ContainerCreate` with improved data validation, and return all validation errors at once. [moby/moby#46183](https://github.com/moby/moby/pull/46183)
* Fix `com.docker.network.host_ipv4` option when IPv6 and ip6tables are enabled. [moby/moby#46446](https://github.com/moby/moby/pull/46446)
* Fix daemon's `cleanupContainer` if containerd is stopped. [moby/moby#46213](https://github.com/moby/moby/pull/46213)
* Fix returning incorrect HTTP status codes for libnetwork errors. [moby/moby#46146](https://github.com/moby/moby/pull/46146)
* Fix various issues with images/json API filters and image list. [moby/moby#46034](https://github.com/moby/moby/pull/46034)
* CIFS volumes now resolves FQDN correctly. [moby/moby#46863](https://github.com/moby/moby/pull/46863)
* Improve validation of the `userland-proxy-path` daemon configuration option. Validation now happens during daemon startup, instead of producing an error when starting a container with port-mapping. [moby/moby#47000](https://github.com/moby/moby/pull/47000)
* Set the MAC address of container's interface when network mode is a short network ID. [moby/moby#46406](https://github.com/moby/moby/pull/46406)
* Sort unconsumed build arguments before display in build output. [moby/moby#45917](https://github.com/moby/moby/pull/45917)
* The `docker image save` tarball output is now OCI compliant. [moby/moby#44598](https://github.com/moby/moby/pull/44598)
* The daemon no longer appends `ACCEPT` rules to the end of the `INPUT` iptables chain for encrypted overlay networks. Depending on firewall configuration, a rule may be needed to permit incoming encrypted overlay network traffic. [moby/moby#45280](https://github.com/moby/moby/pull/45280)
* Unpacking layers with extended attributes onto an incompatible filesystem will now fail instead of silently discarding extended attributes. [moby/moby#45464](https://github.com/moby/moby/pull/45464)
* Update daemon MTU option to BridgeConfig and display warning on Windows. [moby/moby#45887](https://github.com/moby/moby/pull/45887)
* Validate IPAM config when creating a network. Automatically fix networks created prior to this release where `--ip-range` is larger than `--subnet`. [moby/moby#45759](https://github.com/moby/moby/pull/45759)
* Containers connected only to internal networks will now have no default route set, making the `connect` syscall fail-fast. [moby/moby#46603](https://github.com/moby/moby/pull/46603)
* containerd image store: Add image events for `push`, `pull`, and `save`. [moby/moby#46405](https://github.com/moby/moby/pull/46405)
* containerd image store: Add support for pulling legacy schema1 images. [moby/moby#46513](https://github.com/moby/moby/pull/46513)
* containerd image store: Add support for pushing all tags. [moby/moby#46485](https://github.com/moby/moby/pull/46485)
* containerd image store: Add support for registry token. [moby/moby#46475](https://github.com/moby/moby/pull/46475)
* containerd image store: Add support for showing the number of containers that use an image. [moby/moby#46511](https://github.com/moby/moby/pull/46511)
* containerd image store: Fix a bug related to the `ONBUILD`, `MAINTAINER`, and `HEALTHCHECK` Dockerfile instructions. [moby/moby#46313](https://github.com/moby/moby/pull/46313)
* containerd image store: Fix `Pulling from` progress message. [moby/moby#46494](https://github.com/moby/moby/pull/46494)
* containerd image store: Add support for referencing images via the truncated ID with `sha256:` prefix. [moby/moby#46435](https://github.com/moby/moby/pull/46435)
* containerd image store: Fix `docker images` showing intermediate layers by default. [moby/moby#46423](https://github.com/moby/moby/pull/46423)
* containerd image store: Fix checking if the specified platform exists when getting an image. [moby/moby#46495](https://github.com/moby/moby/pull/46495)
* containerd image store: Fix errors when multiple `ADD` or `COPY` instructions were used with the classic builder. [moby/moby#46383](https://github.com/moby/moby/pull/46383)
* containerd image store: Fix stack overflow errors when importing an image. [moby/moby#46418](https://github.com/moby/moby/pull/46418)
* containerd image store: Improve `docker pull` progress output. [moby/moby#46412](https://github.com/moby/moby/pull/46412)
* containerd image store: Print the tag, digest, and size after pushing an image. [moby/moby#46384](https://github.com/moby/moby/pull/46384)
* containerd image store: Remove panic from `UpdateConfig`. [moby/moby#46433](https://github.com/moby/moby/pull/46433)
* containerd image store: Return an error when an image tag resembles a digest. [moby/moby#46492](https://github.com/moby/moby/pull/46492)
* containerd image store: `docker image ls` now shows the correct image creation time and date. [moby/moby#46719](https://github.com/moby/moby/pull/46719)
* containerd image store: Fix an issue handling user namespace settings. [moby/moby#46375](https://github.com/moby/moby/pull/46375)
* containerd image store: Add support for pulling all tags (`docker pull -a`). [moby/moby#46618](https://github.com/moby/moby/pull/46618)
* containerd image store: Use the domain name in the image reference as the default registry authentication domain. [moby/moby#46779](https://github.com/moby/moby/pull/46779)

### [Packaging updates](#packaging-updates-4)

* Upgrade API to v1.44. [moby/moby#45468](https://github.com/moby/moby/pull/45468)
* Upgrade Compose to `2.24.1`. [docker/docker-ce-packaging#980](https://github.com/docker/docker-ce-packaging/pull/980)
* Upgrade containerd to v1.7.12 (static binaries only). [moby/moby#47070](https://github.com/moby/moby/pull/47070)
* Upgrade Go runtime to [1.21.6](https://go.dev/doc/devel/release#go1.21.minor). [moby/moby#47053](https://github.com/moby/moby/pull/47053)
* Upgrade runc to v1.1.11. [moby/moby#47007](https://github.com/moby/moby/pull/47007)
* Upgrade BuildKit to v0.12.4. [moby/moby#46882](https://github.com/moby/moby/pull/46882)
* Upgrade Buildx to v0.12.1. [docker/docker-ce-packaging#979](https://github.com/docker/docker-ce-packaging/pull/979)

### [Removed](#removed)

* API: Remove VirtualSize field for the `GET /images/json` and `GET /images/{id}/json` endpoints. [moby/moby#45469](https://github.com/moby/moby/pull/45469)
* Remove deprecated `devicemapper` storage driver. [moby/moby#43637](https://github.com/moby/moby/pull/43637)
* Remove deprecated orchestrator options. [docker/cli#4366](https://github.com/docker/cli/pull/4366)
* Remove support for Debian Upstart init system. [moby/moby#45548](https://github.com/moby/moby/pull/45548), [moby/moby#45551](https://github.com/moby/moby/pull/45551)
* Remove the `--oom-score-adjust` daemon option. [moby/moby#45484](https://github.com/moby/moby/pull/45484)
* Remove warning for deprecated `~/.dockercfg` file. [docker/cli#4281](https://github.com/docker/cli/pull/4281)
* Remove `logentries` logging driver. [moby/moby#46925](https://github.com/moby/moby/pull/46925)

### [Deprecated](#deprecated)

* Deprecate API versions older than 1.24. [Deprecation notice](https://docs.docker.com/engine/deprecated/#deprecate-legacy-api-versions)
* Deprecate `IsAutomated` field and `is-automated` filter for `docker search`. [Deprecation notice](https://docs.docker.com/engine/deprecated/#isautomated-field-and-is-automated-filter-on-docker-search)
* API: Deprecate `Container` and `ContainerConfig` properties for `/images/{id}/json` (`docker image inspect`). [moby/moby#46939](https://github.com/moby/moby/pull/46939)

### [Known limitations](#known-limitations)

#### [Extended attributes for tar files](#extended-attributes-for-tar-files)

In this release, the code that handles `tar` archives was changed to be more strict and to produce an error when failing to write extended attributes (`xattr`). The `tar` implementation for macOS generates additional extended attributes by default when creating tar files. These attribute prefixes aren't valid Linux `xattr` namespace prefixes, which causes an error when Docker attempts to process these files. For example, if you try to use a tar file with an `ADD` Dockerfile instruction, you might see an error message similar to the following:

```text
failed to solve: lsetxattr /sftp_key.ppk: operation not supported
```

Error messages related to extended attribute validation were improved to include more context in [v25.0.1](#2501), but the limitation in Docker being unable to process the files remains. Tar files created with the macOS `tar` using default arguments will produce an error when the tar file is used with Docker.

As a workaround, if you need to use tar files with Docker generated on macOS, you can either:

* Use the `--no-xattr` flag for the macOS `tar` command to strip **all** the extended attributes. If you want to preserve extended attributes, this isn't a recommended option.

* Install and use `gnu-tar` to create the tarballs on macOS instead of the default `tar` implementation. To install `gnu-tar` using Homebrew:

  ```console
  $ brew install gnu-tar
  ```

  After installing, add the `gnu-tar` binary to your `PATH`, for example by updating your `.zshrc` file:

  ```console
  $ echo 'PATH="/opt/homebrew/opt/gnu-tar/libexec/gnubin:$PATH"' >> ~/.zshrc
  $ source ~/.zshrc
  ```

----
url: https://docs.docker.com/reference/cli/docker/scout/cache/prune/
----

# docker scout cache prune

***

| Description | Remove temporary or cached data |
| ----------- | ------------------------------- |
| Usage       | `docker scout cache prune`      |

## [Description](#description)

The `docker scout cache prune` command removes temporary data and SBOM cache.

By default, `docker scout cache prune` only deletes temporary data. To delete temporary data and clear the SBOM cache, use the `--sboms` flag.

## [Options](#options)

| Option        | Default | Description                    |
| ------------- | ------- | ------------------------------ |
| `-f, --force` |         | Do not prompt for confirmation |
| `--sboms`     |         | Prune cached SBOMs             |

## [Examples](#examples)

### [Delete temporary data](#delete-temporary-data)

```console
$ docker scout cache prune
? Are you sure to delete all temporary data? Yes
    ✓ temporary data deleted
```

### [Delete temporary and cache data](#delete-temporary-and-cache-data)

```console
$ docker scout cache prune --sboms
? Are you sure to delete all temporary data and all cached SBOMs? Yes
    ✓ temporary data deleted
    ✓ cached SBOMs deleted
```

----
url: https://docs.docker.com/reference/cli/docker/mcp/server/init/
----

# docker mcp server init

***

| Description | Initialize a new MCP server project  |
| ----------- | ------------------------------------ |
| Usage       | `docker mcp server init <directory>` |

## [Description](#description)

Initialize a new MCP server project in the specified directory with boilerplate code, Dockerfile, and compose.yaml

## [Options](#options)

| Option       | Default | Description                                                             |
| ------------ | ------- | ----------------------------------------------------------------------- |
| `--language` | `go`    | Programming language for the server (currently only 'go' is supported)  |
| `--template` | `basic` | Template to use (basic, chatgpt-app-basic)                              |

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/namespace-access/
----

# Namespace access control

***

Table of contents

***

Subscription: Business

For: Administrators

Namespace access control lets organization administrators control whether all members of an organization can push content to their personal namespaces on Docker Hub. This prevents organizations from accidentally publishing images outside of approved, governed locations.

When namespace access control is enabled, organization members can still view and pull images from their personal namespaces and continue accessing all existing repositories and content. However, they're unable to create new repositories or push new images to their personal namespace.

> Important
>
> For users in multiple organizations, if namespace access control is enabled in any organization, that user cannot push to their personal namespace and cannot create new repositories in their personal namespace.

### [Configure namespace access control](#configure-namespace-access-control)

To configure namespace access control:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization from the top-left account drop-down.
2. Select **Admin Console**, then **Namespace access**.
3. Use the toggle to enable or disable namespace access control.
4. Select **Save changes**.

Once namespace access control is enabled, organization members can still view their personal namespace and existing repositories but they are not able to create any new repositories or push any new images to existing repositories.

### [Verify access restrictions](#verify-access-restrictions)

After configuring namespace access control, test that restrictions work correctly.

After any attempt to push to an existing repository in your personal namespace, you'll see an error message like the following:

```console
$ docker push <personal-namespace>/<image>:<tag>
Unavailable
authentication required - namespace access restriction from an organization you belong to prevents pushing new content in your personal namespace. Restriction applied by: <organizations>. Please contact your organization administrator
```

----
url: https://docs.docker.com/scout/integrations/environment/sysdig/
----

# Integrate Docker Scout with Sysdig

***

Table of contents

***

The Sysdig integration enables Docker Scout to automatically detect the images you're using for your running workloads. Activating this integration gives you real-time insights about your security posture, and lets you compare your builds with what's running in production.

## [How it works](#how-it-works)

The Sysdig Agent captures the images of your container workloads. Docker Scout integrates with the Sysdig API to discover the images in your cluster. This integration uses Sysdig's Risk Spotlight feature. For more information, see [Risk Spotlight Integrations (Sysdig docs)](https://docs.sysdig.com/en/docs/sysdig-secure/integrations-for-sysdig-secure/risk-spotlight-integrations/).

> Tip
>
> Sysdig offers a free trial for Docker users to try out the new Docker Scout integration.
>
> [Sign up](https://sysdig.com/free-trial-for-docker-customers/)

Each Sysdig integration maps to an environment. When you enable a Sysdig integration, you specify the environment name for that cluster, such as `production` or `staging`. Docker Scout assigns the images in the cluster to the corresponding environment. This lets you use the environment filters to see vulnerability status and policy compliance for an environment.

Only images analyzed by Docker Scout can be assigned to an environment. The Sysdig runtime integration doesn't trigger image analysis by itself. To analyze images automatically, enable a [registry integration](https://docs.docker.com/scout/integrations/#container-registries).

Image analysis must not necessarily precede the runtime integration, but the environment assignment only takes place once Docker Scout has analyzed the image.

## [Prerequisites](#prerequisites)

* Install the Sysdig Agent in the cluster that you want to integrate, see [Install Sysdig Agent (Sysdig docs)](https://docs.sysdig.com/en/docs/installation/sysdig-monitor/install-sysdig-agent/).
* Enable profiling for Risk Spotlight Integrations in Sysdig, see [Profiling (Sysdig docs)](https://docs.sysdig.com/en/docs/sysdig-secure/policies/profiling/#enablement).
* You must be an organization owner to enable the integration in the Docker Scout Dashboard.

## [Integrate an environment](#integrate-an-environment)

1. Go to the [Sysdig integration page](https://scout.docker.com/settings/integrations/sysdig/) on the Docker Scout Dashboard.

2. In the **How to integrate** section, enter a configuration name for this integration. Docker Scout uses this label as a display name for the integration.

3. Select **Next**.

4. Enter a Risk Spotlight API token and select the region in the drop-down list.

   The Risk Spotlight API token is the Sysdig token that Docker Scout needs to integrate with Sysdig. For more instructions on how to generate a Risk Spotlight token, See [Risk Spotlight Integrations (Sysdig docs)](https://docs.sysdig.com/en/docs/sysdig-secure/integrations-for-sysdig-secure/risk-spotlight-integrations/docker-scout/#generate-a-token-for-the-integration).

   The region corresponds to the `global.sysdig.region` configuration parameter set when deploying the Sysdig Agent.

5. Select **Next**.

   After selecting **Next**, Docker Scout connects to Sysdig and retrieves the cluster names for your Sysdig account. Cluster names correspond to the `global.clusterConfig.name` configuration parameter set when deploying Sysdig Agents.

   An error displays if Docker Scout fails to connect to Sysdig using the provided token. If there's an error, you won't be able to continue the integration. Go back and verify that the configuration details are correct.

6. Select a cluster name in the drop-down list.

7. Select **Next**.

8. Assign an environment name for this cluster.

   You can reuse an existing environment or create a new one.

9. Select **Enable integration**.

After enabling the integration, Docker Scout automatically detects images running in the cluster, and assigns those images to the environment associated with the cluster. For more information about environments, see [Environment monitoring](https://docs.docker.com/scout/integrations/environment/).

> Note
>
> Docker Scout only detects images that have been analyzed. To trigger an image analysis, enable a [registry integration](https://docs.docker.com/scout/integrations/#container-registries) and push an image to your registry.
>
> If you created a new environment for this integration, the environment appears in Docker Scout when at least one image has been analyzed.

To integrate more clusters, go to the [Sysdig integrations page](https://scout.docker.com/settings/integrations/sysdig/) and select the **Add** button.

----
url: https://docs.docker.com/engine/storage/bind-mounts/
----

# Bind mounts

***

Table of contents

***

When you use a bind mount, a file or directory on the host machine is mounted from the host into a container. By contrast, when you use a volume, a new directory is created within Docker's storage directory on the host machine. Docker creates and maintains this storage location, but containers access it directly using standard filesystem operations.

## [When to use bind mounts](#when-to-use-bind-mounts)

Bind mounts are appropriate for the following types of use case:

* Sharing source code or build artifacts between a development environment on the Docker host and a container.

* When you want to create or generate files in a container and persist the files onto the host's filesystem.

* Sharing configuration files from the host machine to containers. This is how Docker provides DNS resolution to containers by default, by mounting `/etc/resolv.conf` from the host machine into each container.

Bind mounts are also available for builds: you can bind mount source code from the host into the build container to test, lint, or compile a project.

## [Bind-mounting over existing data](#bind-mounting-over-existing-data)

If you bind mount file or directory into a directory in the container in which files or directories exist, the pre-existing files are obscured by the mount. This is similar to if you were to save files into `/mnt` on a Linux host, and then mounted a USB drive into `/mnt`. The contents of `/mnt` would be obscured by the contents of the USB drive until the USB drive was unmounted.

With containers, there's no straightforward way of removing a mount to reveal the obscured files again. Your best option is to recreate the container without the mount.

## [Considerations and constraints](#considerations-and-constraints)

* Bind mounts have write access to files on the host by default.

  One side effect of using bind mounts is that you can change the host filesystem via processes running in a container, including creating, modifying, or deleting important system files or directories. This capability can have security implications. For example, it may affect non-Docker processes on the host system.

  You can use the `readonly` or `ro` option to prevent the container from writing to the mount.

* Bind mounts are created to the Docker daemon host, not the client.

  If you're using a remote Docker daemon, you can't create a bind mount to access files on the client machine in a container.

  For Docker Desktop, the daemon runs inside a Linux VM, not directly on the native host. Docker Desktop has built-in mechanisms that transparently handle bind mounts, allowing you to share native host filesystem paths with containers running in the virtual machine.

* Containers with bind mounts are strongly tied to the host.

  Bind mounts rely on the host machine's filesystem having a specific directory structure available. This reliance means that containers with bind mounts may fail if run on a different host without the same directory structure.

## [Syntax](#syntax)

To create a bind mount, you can use either the `--mount` or `--volume` flag.

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>
$ docker run --volume <host-path>:<container-path>
```

In general, `--mount` is preferred. The main difference is that the `--mount` flag is more explicit and supports all the available options.

If you use `--volume` to bind-mount a file or directory that does not yet exist on the Docker host, Docker automatically creates the directory on the host for you. It's always created as a directory.

By default, `--mount` does not automatically create a directory if the specified mount path does not exist on the host. Instead, it produces an error:

```console
$ docker run --mount type=bind,src=/dev/noexist,dst=/mnt/foo alpine
docker: Error response from daemon: invalid mount config for type "bind": bind source path does not exist: /dev/noexist.
```

You can use the `bind-create-src` option to automatically create the source directory on the host if it doesn't exist:

```console
$ docker run --mount type=bind,src=/home/user/mydir,dst=/mnt/foo,bind-create-src alpine
```

### [Options for --mount](#options-for---mount)

The `--mount` flag consists of multiple key-value pairs, separated by commas and each consisting of a `<key>=<value>` tuple. The order of the keys isn't significant.

```console
$ docker run --mount type=bind,src=<host-path>,dst=<container-path>[,<key>=<value>...]
```

Valid options for `--mount type=bind` include:

| Option                         | Description                                                                                                                                                         |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `source`, `src`                | The location of the file or directory on the host. This can be an absolute or relative path.                                                                        |
| `destination`, `dst`, `target` | The path where the file or directory is mounted in the container. Must be an absolute path.                                                                         |
| `readonly`, `ro`               | If present, causes the bind mount to be [mounted into the container as read-only](#use-a-read-only-bind-mount).                                                     |
| `bind-propagation`             | If present, changes the [bind propagation](#configure-bind-propagation).                                                                                            |
| `bind-create-src`              | Automatically creates the source directory on the host if it doesn't exist. By default, `--mount` produces an error if the source path doesn't exist on the daemon. |

Example

```console
$ docker run --mount type=bind,src=.,dst=/project,ro,bind-propagation=rshared
```

### [Options for --volume](#options-for---volume)

The `--volume` or `-v` flag consists of three fields, separated by colon characters (`:`). The fields must be in the correct order.

```console
$ docker run -v <host-path>:<container-path>[:opts]
```

The first field is the path on the host to bind mount into the container. The second field is the path where the file or directory is mounted in the container.

The third field is optional, and is a comma-separated list of options. Valid options for `--volume` with a bind mount include:

| Option               | Description                                                                                                        |
| -------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `readonly`, `ro`     | If present, causes the bind mount to be [mounted into the container as read-only](#use-a-read-only-bind-mount).    |
| `z`, `Z`             | Configures SELinux labeling. See [Configure the SELinux label](#configure-the-selinux-label)                       |
| `rprivate` (default) | Sets bind propagation to `rprivate` for this mount. See [Configure bind propagation](#configure-bind-propagation). |
| `private`            | Sets bind propagation to `private` for this mount. See [Configure bind propagation](#configure-bind-propagation).  |
| `rshared`            | Sets bind propagation to `rshared` for this mount. See [Configure bind propagation](#configure-bind-propagation).  |
| `shared`             | Sets bind propagation to `shared` for this mount. See [Configure bind propagation](#configure-bind-propagation).   |
| `rslave`             | Sets bind propagation to `rslave` for this mount. See [Configure bind propagation](#configure-bind-propagation).   |
| `slave`              | Sets bind propagation to `slave` for this mount. See [Configure bind propagation](#configure-bind-propagation).    |

Example

```console
$ docker run -v .:/project:ro,rshared
```

## [Start a container with a bind mount](#start-a-container-with-a-bind-mount)

Consider a case where you have a directory `source` and that when you build the source code, the artifacts are saved into another directory, `source/target/`. You want the artifacts to be available to the container at `/app/`, and you want the container to get access to a new build each time you build the source on your development host. Use the following command to bind-mount the `target/` directory into your container at `/app/`. Run the command from within the `source` directory. The `$(pwd)` sub-command expands to the current working directory on Linux or macOS hosts. If you're on Windows, see also [Path conversions on Windows](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/topics/).

The following `--mount` and `-v` examples produce the same result. You can't run them both unless you remove the `devtest` container after running the first one.

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  nginx:latest
```

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  nginx:latest
```

Use `docker inspect devtest` to verify that the bind mount was created correctly. Look for the `Mounts` section:

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "",
        "RW": true,
        "Propagation": "rprivate"
    }
],
```

This shows that the mount is a `bind` mount, it shows the correct source and destination, it shows that the mount is read-write, and that the propagation is set to `rprivate`.

Stop and remove the container:

```console
$ docker container rm -fv devtest
```

### [Mount into a non-empty directory on the container](#mount-into-a-non-empty-directory-on-the-container)

If you bind-mount a directory into a non-empty directory on the container, the directory's existing contents are obscured by the bind mount. This can be beneficial, such as when you want to test a new version of your application without building a new image. However, it can also be surprising and this behavior differs from that of [volumes](https://docs.docker.com/engine/storage/volumes/).

This example is contrived to be extreme, but replaces the contents of the container's `/usr/` directory with the `/tmp/` directory on the host machine. In most cases, this would result in a non-functioning container.

The `--mount` and `-v` examples have the same end result.

```console
$ docker run -d \
  -it \
  --name broken-container \
  --mount type=bind,source=/tmp,target=/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

```console
$ docker run -d \
  -it \
  --name broken-container \
  -v /tmp:/usr \
  nginx:latest

docker: Error response from daemon: oci runtime error: container_linux.go:262:
starting container process caused "exec: \"nginx\": executable file not found in $PATH".
```

The container is created but does not start. Remove it:

```console
$ docker container rm broken-container
```

## [Use a read-only bind mount](#use-a-read-only-bind-mount)

For some development applications, the container needs to write into the bind mount, so changes are propagated back to the Docker host. At other times, the container only needs read access.

This example modifies the previous one, but mounts the directory as a read-only bind mount, by adding `ro` to the (empty by default) list of options, after the mount point within the container. Where multiple options are present, separate them by commas.

The `--mount` and `-v` examples have the same result.

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app,readonly \
  nginx:latest
```

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:ro \
  nginx:latest
```

Use `docker inspect devtest` to verify that the bind mount was created correctly. Look for the `Mounts` section:

```json
"Mounts": [
    {
        "Type": "bind",
        "Source": "/tmp/source/target",
        "Destination": "/app",
        "Mode": "ro",
        "RW": false,
        "Propagation": "rprivate"
    }
],
```

Stop and remove the container:

```console
$ docker container rm -fv devtest
```

## [Recursive mounts](#recursive-mounts)

When you bind mount a path that itself contains mounts, those submounts are also included in the bind mount by default. This behavior is configurable, using the `bind-recursive` option for `--mount`. This option is only supported with the `--mount` flag, not with `-v` or `--volume`.

If the bind mount is read-only, the Docker Engine makes a best-effort attempt at making the submounts read-only as well. This is referred to as recursive read-only mounts. Recursive read-only mounts require Linux kernel version 5.12 or later. If you're running an older kernel version, submounts are automatically mounted as read-write by default. Attempting to set submounts to be read-only on a kernel version earlier than 5.12, using the `bind-recursive=readonly` option, results in an error.

Supported values for the `bind-recursive` option are:

| Value               | Description                                                                                                       |
| ------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `enabled` (default) | Read-only mounts are made recursively read-only if kernel is v5.12 or later. Otherwise, submounts are read-write. |
| `disabled`          | Submounts are ignored (not included in the bind mount).                                                           |
| `writable`          | Submounts are read-write.                                                                                         |
| `readonly`          | Submounts are read-only. Requires kernel v5.12 or later.                                                          |

## [Configure bind propagation](#configure-bind-propagation)

Bind propagation defaults to `rprivate` for both bind mounts and volumes. It is only configurable for bind mounts, and only on Linux host machines. Bind propagation is an advanced topic and many users never need to configure it.

Bind propagation refers to whether or not mounts created within a given bind-mount can be propagated to replicas of that mount. Consider a mount point `/mnt`, which is also mounted on `/tmp`. The propagation settings control whether a mount on `/tmp/a` would also be available on `/mnt/a`. Each propagation setting has a recursive counterpoint. In the case of recursion, consider that `/tmp/a` is also mounted as `/foo`. The propagation settings control whether `/mnt/a` and/or `/tmp/a` would exist.

> Note
>
> Mount propagation doesn't work with Docker Desktop.

| Propagation setting | Description                                                                                                                                                                                                         |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `shared`            | Sub-mounts of the original mount are exposed to replica mounts, and sub-mounts of replica mounts are also propagated to the original mount.                                                                         |
| `slave`             | similar to a shared mount, but only in one direction. If the original mount exposes a sub-mount, the replica mount can see it. However, if the replica mount exposes a sub-mount, the original mount cannot see it. |
| `private`           | The mount is private. Sub-mounts within it are not exposed to replica mounts, and sub-mounts of replica mounts are not exposed to the original mount.                                                               |
| `rshared`           | The same as shared, but the propagation also extends to and from mount points nested within any of the original or replica mount points.                                                                            |
| `rslave`            | The same as slave, but the propagation also extends to and from mount points nested within any of the original or replica mount points.                                                                             |
| `rprivate`          | The default. The same as private, meaning that no mount points anywhere within the original or replica mount points propagate in either direction.                                                                  |

Before you can set bind propagation on a mount point, the host filesystem needs to already support bind propagation.

For more information about bind propagation, see the [Linux kernel documentation for shared subtree](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt).

The following example mounts the `target/` directory into the container twice, and the second mount sets both the `ro` option and the `rslave` bind propagation option.

The `--mount` and `-v` examples have the same result.

```console
$ docker run -d \
  -it \
  --name devtest \
  --mount type=bind,source="$(pwd)"/target,target=/app \
  --mount type=bind,source="$(pwd)"/target,target=/app2,readonly,bind-propagation=rslave \
  nginx:latest
```

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app \
  -v "$(pwd)"/target:/app2:ro,rslave \
  nginx:latest
```

Now if you create `/app/foo/`, `/app2/foo/` also exists.

## [Configure the SELinux label](#configure-the-selinux-label)

If you use SELinux, you can add the `z` or `Z` options to modify the SELinux label of the host file or directory being mounted into the container. This affects the file or directory on the host machine itself and can have consequences outside of the scope of Docker.

* The `z` option indicates that the bind mount content is shared among multiple containers.
* The `Z` option indicates that the bind mount content is private and unshared.

Use extreme caution with these options. Bind-mounting a system directory such as `/home` or `/usr` with the `Z` option renders your host machine inoperable and you may need to relabel the host machine files by hand.

> Important
>
> When using bind mounts with services, SELinux labels (`:Z` and `:z`), as well as `:ro` are ignored. See [moby/moby #32579](https://github.com/moby/moby/issues/32579) for details.

This example sets the `z` option to specify that multiple containers can share the bind mount's contents:

It is not possible to modify the SELinux label using the `--mount` flag.

```console
$ docker run -d \
  -it \
  --name devtest \
  -v "$(pwd)"/target:/app:z \
  nginx:latest
```

## [Use a bind mount with Docker Compose](#use-a-bind-mount-with-docker-compose)

A single Docker Compose service with a bind mount looks like this:

```yaml
services:
  frontend:
    image: node:lts
    volumes:
      - type: bind
        source: ./static
        target: /opt/app/static
volumes:
  myapp:
```

For more information about using volumes of the `bind` type with Compose, see [Compose reference on the volumes top-level element](https://docs.docker.com/reference/compose-file/volumes/). and [Compose reference on the volume attribute](https://docs.docker.com/reference/compose-file/services/#volumes).

## [Next steps](#next-steps)

* Learn about [volumes](https://docs.docker.com/engine/storage/volumes/).
* Learn about [tmpfs mounts](https://docs.docker.com/engine/storage/tmpfs/).
* Learn about [storage drivers](/engine/storage/drivers/).

----
url: https://docs.docker.com/engine/cli/proxy/
----

# Use a proxy server with the Docker CLI

***

Table of contents

***

This page describes how to configure the Docker CLI to use proxies via environment variables in containers.

This page doesn't describe how to configure proxies for Docker Desktop. For instructions, see [configuring Docker Desktop to use HTTP/HTTPS proxies](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

If you're running Docker Engine without Docker Desktop, refer to [Configure the Docker daemon to use a proxy](https://docs.docker.com/engine/daemon/proxy/) to learn how to configure a proxy server for the Docker daemon (`dockerd`) itself.

If your container needs to use an HTTP, HTTPS, or FTP proxy server, you can configure it in different ways:

* [Configure the Docker client](#configure-the-docker-client)
* [Set proxy using the CLI](#set-proxy-using-the-cli)

> Note
>
> Unfortunately, there's no standard that defines how web clients should handle proxy environment variables, or the format for defining them.
>
> If you're interested in the history of these variables, check out this blog post on the subject, by the GitLab team: [We need to talk: Can we standardize NO\_PROXY?](https://about.gitlab.com/blog/2021/01/27/we-need-to-talk-no-proxy/).

## [Configure the Docker client](#configure-the-docker-client)

You can add proxy configurations for the Docker client using a JSON configuration file, located in `~/.docker/config.json`. Builds and containers use the configuration specified in this file.

```json
{
 "proxies": {
   "default": {
     "httpProxy": "http://proxy.example.com:3128",
     "httpsProxy": "https://proxy.example.com:3129",
     "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
   }
 }
}
```

> Warning
>
> Proxy settings may contain sensitive information. For example, some proxy servers require authentication information to be included in their URL, or their address may expose IP-addresses or hostnames of your company's environment.
>
> Environment variables are stored as plain text in the container's configuration, and as such can be inspected through the remote API or committed to an image when using `docker commit`.

The configuration becomes active after saving the file, you don't need to restart Docker. However, the configuration only applies to new containers and builds, and doesn't affect existing containers.

The following table describes the available configuration parameters.

| Property     | Description                                                                         |
| ------------ | ----------------------------------------------------------------------------------- |
| `httpProxy`  | Sets the `HTTP_PROXY` and `http_proxy` environment variables and build arguments.   |
| `httpsProxy` | Sets the `HTTPS_PROXY` and `https_proxy` environment variables and build arguments. |
| `ftpProxy`   | Sets the `FTP_PROXY` and `ftp_proxy` environment variables and build arguments.     |
| `noProxy`    | Sets the `NO_PROXY` and `no_proxy` environment variables and build arguments.       |
| `allProxy`   | Sets the `ALL_PROXY` and `all_proxy` environment variables and build arguments.     |

These settings are used to configure proxy environment variables for containers only, and not used as proxy settings for the Docker CLI or the Docker Engine itself. Refer to the [environment variables](/reference/cli/docker/#environment-variables) and [configure the Docker daemon to use a proxy server](https://docs.docker.com/engine/daemon/proxy/) sections for configuring proxy settings for the CLI and daemon.

### [Run containers with a proxy configuration](#run-containers-with-a-proxy-configuration)

When you start a container, its proxy-related environment variables are set to reflect your proxy configuration in `~/.docker/config.json`.

For example, assuming a proxy configuration like the example shown in the [earlier section](#configure-the-docker-client), environment variables for containers that you run are set as follows:

```console
$ docker run --rm alpine sh -c 'env | grep -i  _PROXY'
https_proxy=http://proxy.example.com:3129
HTTPS_PROXY=http://proxy.example.com:3129
http_proxy=http://proxy.example.com:3128
HTTP_PROXY=http://proxy.example.com:3128
no_proxy=*.test.example.com,.example.org,127.0.0.0/8
NO_PROXY=*.test.example.com,.example.org,127.0.0.0/8
```

### [Build with a proxy configuration](#build-with-a-proxy-configuration)

When you invoke a build, proxy-related build arguments are pre-populated automatically, based on the proxy settings in your Docker client configuration file.

Assuming a proxy configuration like the example shown in the [earlier section](#configure-the-docker-client), environment are set as follows during builds:

```console
$ docker build \
  --no-cache \
  --progress=plain \
  - <<EOF
FROM alpine
RUN env | grep -i _PROXY
EOF
```

```console
#5 [2/2] RUN env | grep -i _PROXY
#5 0.100 HTTPS_PROXY=https://proxy.example.com:3129
#5 0.100 no_proxy=*.test.example.com,.example.org,127.0.0.0/8
#5 0.100 NO_PROXY=*.test.example.com,.example.org,127.0.0.0/8
#5 0.100 https_proxy=https://proxy.example.com:3129
#5 0.100 http_proxy=http://proxy.example.com:3128
#5 0.100 HTTP_PROXY=http://proxy.example.com:3128
#5 DONE 0.1s
```

### [Configure proxy settings per daemon](#configure-proxy-settings-per-daemon)

The `default` key under `proxies` in `~/.docker/config.json` configures the proxy settings for all daemons that the client connects to. To configure the proxies for individual daemons, use the address of the daemon instead of the `default` key.

The following example configures both a default proxy config, and a no-proxy override for the Docker daemon on address `tcp://docker-daemon1.example.com`:

```json
{
 "proxies": {
   "default": {
     "httpProxy": "http://proxy.example.com:3128",
     "httpsProxy": "https://proxy.example.com:3129",
     "noProxy": "*.test.example.com,.example.org,127.0.0.0/8"
   },
   "tcp://docker-daemon1.example.com": {
     "noProxy": "*.internal.example.net"
   }
 }
}
```

## [Set proxy using the CLI](#set-proxy-using-the-cli)

Instead of [configuring the Docker client](#configure-the-docker-client), you can specify proxy configurations on the command-line when you invoke the `docker build` and `docker run` commands.

Proxy configuration on the command-line uses the `--build-arg` flag for builds, and the `--env` flag for when you want to run containers with a proxy.

```console
$ docker build --build-arg HTTP_PROXY="http://proxy.example.com:3128" .
$ docker run --env HTTP_PROXY="http://proxy.example.com:3128" redis
```

For a list of all the proxy-related build arguments that you can use with the `docker build` command, see [Predefined ARGs](https://docs.docker.com/reference/dockerfile/#predefined-args). These proxy values are only available in the build container. They're not included in the build output.

## [Proxy as environment variable for builds](#proxy-as-environment-variable-for-builds)

Don't use the `ENV` Dockerfile instruction to specify proxy settings for builds. Use build arguments instead.

Using environment variables for proxies embeds the configuration into the image. If the proxy is an internal proxy, it might not be accessible for containers created from that image.

Embedding proxy settings in images also poses a security risk, as the values may include sensitive information.

----
url: https://docs.docker.com/reference/cli/docker/buildx/policy/test/
----

# docker buildx policy test

***

| Description | Run policy tests                   |
| ----------- | ---------------------------------- |
| Usage       | `docker buildx policy test <path>` |

## [Description](#description)

Run policy tests

## [Options](#options)

| Option       | Default      | Description                                        |
| ------------ | ------------ | -------------------------------------------------- |
| `--filename` | `Dockerfile` | Name of the Dockerfile to validate                 |
| `--run`      |              | Run only tests with name containing this substring |

----
url: https://docs.docker.com/extensions/extensions-sdk/extensions/labels/
----

# Extension image labels

***

Table of contents

***

Extensions use image labels to provide additional information such as a title, description, screenshots, and more.

This information is then displayed as an overview of the extension, so users can choose to install it.

You can define [image labels](https://docs.docker.com/reference/dockerfile/#label) in the extension's `Dockerfile`.

> Important
>
> If any of the **required** labels are missing in the `Dockerfile`, Docker Desktop considers the extension invalid and doesn't list it in the Marketplace.

Here is the list of labels you can or need to specify when building your extension:

| Label                                       | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Example                                                                                                                                                                                                                                                         |
| ------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `org.opencontainers.image.title`            | Yes      | Human-readable title of the image (string). This appears in the UI for Docker Desktop.                                                                                                                                                                                                                                                                                                                                                                                                                                    | my-extension                                                                                                                                                                                                                                                    |
| `org.opencontainers.image.description`      | Yes      | Human-readable description of the software packaged in the image (string)                                                                                                                                                                                                                                                                                                                                                                                                                                                 | This extension is cool.                                                                                                                                                                                                                                         |
| `org.opencontainers.image.vendor`           | Yes      | Name of the distributing entity, organization, or individual.                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Acme, Inc.                                                                                                                                                                                                                                                      |
| `com.docker.desktop.extension.api.version`  | Yes      | Version of the Docker Extension manager that the extension is compatible with. It must follow [semantic versioning](https://semver.org/).                                                                                                                                                                                                                                                                                                                                                                                 | A specific version like `0.1.0` or, a constraint expression: `>= 0.1.0`, `>= 1.4.7, < 2.0` . For your first extension, you can use `docker extension version` to know the SDK API version and specify `>= <SDK_API_VERSION>`.                                   |
| `com.docker.desktop.extension.icon`         | Yes      | The extension icon (format: .svg .png .jpg)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `https://example.com/assets/image.svg`                                                                                                                                                                                                                          |
| `com.docker.extension.screenshots`          | Yes      | A JSON array of image URLs and an alternative text displayed to users (in the order they appear in your metadata) in your extension's details page. **Note:** The recommended size for screenshots is 2400x1600 pixels.                                                                                                                                                                                                                                                                                                   | `[{"alt":"alternative text for image 1",` `"url":"https://example.com/image1.png"},` `{"alt":"alternative text for image2",` `"url":"https://example.com/image2.jpg"}]`                                                                                         |
| `com.docker.extension.detailed-description` | Yes      | Additional information in plain text or HTML about the extension to display in the details dialog.                                                                                                                                                                                                                                                                                                                                                                                                                        | `My detailed description` or `<h1>My detailed description</h1>`                                                                                                                                                                                                 |
| `com.docker.extension.publisher-url`        | Yes      | The publisher website URL to display in the details dialog.                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `https://example.com`                                                                                                                                                                                                                                           |
| `com.docker.extension.additional-urls`      | No       | A JSON array of titles and additional URLs displayed to users (in the order they appear in your metadata) in your extension's details page. Docker recommends you display the following links if they apply: documentation, support, terms of service, and privacy policy links.                                                                                                                                                                                                                                          | `[{"title":"Documentation","url":"https://example.com/docs"},` `{"title":"Support","url":"https://example.com/bar/support"},` `{"title":"Terms of Service","url":"https://example.com/tos"},` `{"title":"Privacy policy","url":"https://example.com/privacy"}]` |
| `com.docker.extension.changelog`            | Yes      | Changelog in plain text or HTML containing the change for the current version only.                                                                                                                                                                                                                                                                                                                                                                                                                                       | `Extension changelog` or `<p>Extension changelog<ul>` `<li>New feature A</li>` `<li>Bug fix on feature B</li></ul></p>`                                                                                                                                         |
| `com.docker.extension.account-info`         | No       | Whether the user needs to register to a SaaS platform to use some features of the extension.                                                                                                                                                                                                                                                                                                                                                                                                                              | `required` in case it does, leave it empty otherwise.                                                                                                                                                                                                           |
| `com.docker.extension.categories`           | No       | The list of Marketplace categories that your extension belongs to: `ci-cd`, `container-orchestration`, `cloud-deployment`, `cloud-development`, `database`, `kubernetes`, `networking`, `image-registry`, `security`, `testing-tools`, `utility-tools`,`volumes`. If you don't specify this label, users won't be able to find your extension in the Extensions Marketplace when filtering by a category. Extensions published to the Marketplace before the 22nd of September 2022 have been auto-categorized by Docker. | Specified as comma separated values in case of having multiple categories e.g: `kubernetes,security` or a single value e.g. `kubernetes`.                                                                                                                       |

> Tip
>
> Docker Desktop applies CSS styles to the provided HTML content. You can make sure that it renders correctly [within the Marketplace](#preview-the-extension-in-the-marketplace). It is recommended that you follow the [styling guidelines](https://docs.docker.com/extensions/extensions-sdk/design/).

## [Preview the extension in the Marketplace](#preview-the-extension-in-the-marketplace)

You can validate that the image labels render as you expect.

When you create and install your unpublished extension, you can preview the extension in the Marketplace's **Managed** tab. You can see how the extension labels render in the list and in the details page of the extension.

> Preview extensions already listed in Marketplace
>
> When you install a local image of an extension already published in the Marketplace, for example with the tag `latest`, your local image is not detected as "unpublished".
>
> You can re-tag your image in order to have a different image name that's not listed as a published extension. Use `docker tag org/published-extension unpublished-extension` and then `docker extension install unpublished-extension`.

----
url: https://docs.docker.com/guides/golang/run-containers/
----

# Run your Go image as a container

***

Table of contents

***

## [Prerequisites](#prerequisites)

Work through the steps to containerize a Go application in [Build your Go image](https://docs.docker.com/guides/golang/build-images/).

## [Overview](#overview)

In the previous module you created a `Dockerfile` for your example application and then you created your Docker image using the command `docker build`. Now that you have the image, you can run that image and see if your application is running correctly.

A container is a normal operating system process except that this process is isolated and has its own file system, its own networking, and its own isolated process tree separate from the host.

To run an image inside of a container, you use the `docker run` command. It requires one parameter and that's the image name. Start your image and make sure it's running correctly. Run the following command in your terminal.

```console
$ docker run docker-gs-ping
```

```text
   ____    __
  / __/___/ /  ___
 / _// __/ _ \/ _ \
/___/\__/_//_/\___/ v4.10.2
High performance, minimalist Go web framework
https://echo.labstack.com
____________________________________O/_______
                                    O\
⇨ http server started on [::]:8080
```

When you run this command, you’ll notice that you weren't returned to the command prompt. This is because your application is a REST server and will run in a loop waiting for incoming requests without returning control back to the OS until you stop the container.

Make a GET request to the server using the curl command.

```console
$ curl http://localhost:8080/
curl: (7) Failed to connect to localhost port 8080: Connection refused
```

Your curl command failed because the connection to your server was refused. Meaning that you weren't able to connect to localhost on port 8080. This is expected because your container is running in isolation which includes networking. Stop the container and restart with port 8080 published on your local network.

To stop the container, press ctrl-c. This will return you to the terminal prompt.

To publish a port for your container, you’ll use the `--publish` flag (`-p` for short) on the `docker run` command. The format of the `--publish` command is `[host_port]:[container_port]`. So if you wanted to expose port `8080` inside the container to port `3000` outside the container, you would pass `3000:8080` to the `--publish` flag.

Start the container and expose port `8080` to port `8080` on the host.

```console
$ docker run --publish 8080:8080 docker-gs-ping
```

Now, rerun the curl command.

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

Success! You were able to connect to the application running inside of your container on port 8080. Switch back to the terminal where your container is running and you should see the `GET` request logged to the console.

Press `ctrl-c` to stop the container.

## [Run in detached mode](#run-in-detached-mode)

This is great so far, but your sample application is a web server and you shouldn't have to have your terminal connected to the container. Docker can run your container in detached mode in the background. To do this, you can use the `--detach` or `-d` for short. Docker will start your container the same as before but this time will detach from the container and return you to the terminal prompt.

```console
$ docker run -d -p 8080:8080 docker-gs-ping
d75e61fcad1e0c0eca69a3f767be6ba28a66625ce4dc42201a8a323e8313c14e
```

Docker started your container in the background and printed the container ID on the terminal.

Again, make sure that your container is running. Run the same `curl` command:

```console
$ curl http://localhost:8080/
Hello, Docker! <3
```

## [List containers](#list-containers)

Since you ran your container in the background, how do you know if your container is running or what other containers are running on your machine? Well, to see a list of containers running on your machine, run `docker ps`. This is similar to how the ps command is used to see a list of processes on a Linux machine.

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"   41 seconds ago   Up 40 seconds   0.0.0.0:8080->8080/tcp   inspiring_ishizaka
```

The `ps` command tells you a bunch of stuff about your running containers. You can see the container ID, the image running inside the container, the command that was used to start the container, when it was created, the status, ports that are exposed, and the names of the container.

You are probably wondering where the name of your container is coming from. Since you didn’t provide a name for the container when you started it, Docker generated a random name. You'll fix this in a minute but first you need to stop the container. To stop the container, run the `docker stop` command, passing the container's name or ID.

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

Now rerun the `docker ps` command to see a list of running containers.

```console
$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

## [Stop, start, and name containers](#stop-start-and-name-containers)

Docker containers can be started, stopped and restarted. When you stop a container, it's not removed but the status is changed to stopped and the process inside of the container is stopped. When you ran the `docker ps` command, the default output is to only show running containers. If you pass the `--all` or `-a` for short, you will see all containers on your system, including stopped containers and running containers.

```console
$ docker ps --all

CONTAINER ID   IMAGE            COMMAND                  CREATED              STATUS                      PORTS     NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        About a minute ago   Exited (2) 23 seconds ago             inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 2 minutes ago              wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        3 minutes ago        Exited (2) 3 minutes ago              magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        9 minutes ago        Exited (2) 3 minutes ago              gifted_mestorf
```

If you’ve been following along, you should see several containers listed. These are containers that you started and stopped but haven't removed yet.

Restart the container that you have just stopped. Locate the name of the container and replace the name of the container in the following `restart` command:

```console
$ docker restart inspiring_ishizaka
```

Now, list all the containers again using the `ps` command:

```console
$ docker ps -a

CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS                     PORTS                    NAMES
d75e61fcad1e   docker-gs-ping   "/docker-gs-ping"        2 minutes ago    Up 5 seconds               0.0.0.0:8080->8080/tcp   inspiring_ishizaka
f65dbbb9a548   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 2 minutes ago                            wizardly_joliot
aade1bf3d330   docker-gs-ping   "/docker-gs-ping"        4 minutes ago    Exited (2) 4 minutes ago                            magical_carson
52d5ce3c15f0   docker-gs-ping   "/docker-gs-ping"        10 minutes ago   Exited (2) 4 minutes ago                            gifted_mestorf
```

Notice that the container you just restarted has been started in detached mode and has port `8080` exposed. Also, note that the status of the container is `Up X seconds`. When you restart a container, it will be started with the same flags or commands that it was originally started with.

Stop and remove all of your containers and take a look at fixing the random naming issue.

Stop the container you just started. Find the name of your running container and replace the name in the following command with the name of the container on your system:

```console
$ docker stop inspiring_ishizaka
inspiring_ishizaka
```

Now that all of your containers are stopped, remove them. When a container is removed, it's no longer running nor is it in the stopped state. Instead, the process inside the container is terminated and the metadata for the container is removed.

To remove a container, run the `docker rm` command passing the container name. You can pass multiple container names to the command in one command.

Again, make sure you replace the containers names in the following command with the container names from your system:

```console
$ docker rm inspiring_ishizaka wizardly_joliot magical_carson gifted_mestorf

inspiring_ishizaka
wizardly_joliot
magical_carson
gifted_mestorf
```

Run the `docker ps --all` command again to verify that all containers are gone.

Now, address the pesky random name issue. Standard practice is to name your containers for the simple reason that it's easier to identify what's running in the container and what application or service it's associated with. Just like good naming conventions for variables in your code makes it simpler to read. So goes naming your containers.

To name a container, you must pass the `--name` flag to the `run` command:

```console
$ docker run -d -p 8080:8080 --name rest-server docker-gs-ping
3bbc6a3102ea368c8b966e1878a5ea9b1fc61187afaac1276c41db22e4b7f48f
```

```console
$ docker ps

CONTAINER ID   IMAGE            COMMAND             CREATED          STATUS          PORTS                    NAMES
3bbc6a3102ea   docker-gs-ping   "/docker-gs-ping"   25 seconds ago   Up 24 seconds   0.0.0.0:8080->8080/tcp   rest-server
```

Now, you can easily identify your container based on the name.

## [Next steps](#next-steps)

In this module, you learned how to run containers and publish ports. You also learned to manage the lifecycle of containers. You then learned the importance of naming your containers so that they're more easily identifiable. In the next module, you’ll learn how to run a database in a container and connect it to your application.

[Use containers for Go development »](https://docs.docker.com/guides/golang/develop/)

----
url: https://docs.docker.com/engine/containers/run/
----

# Running containers

***

Table of contents

***

Docker runs processes in isolated containers. A container is a process which runs on a host. The host may be local or remote. When you execute `docker run`, the container process that runs is isolated in that it has its own file system, its own networking, and its own isolated process tree separate from the host.

This page details how to use the `docker run` command to run containers.

## [General form](#general-form)

A `docker run` command takes the following form:

```console
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

The `docker run` command must specify an [image reference](#image-references) to create the container from.

### [Image references](#image-references)

The image reference is the name and version of the image. You can use the image reference to create or run a container based on an image.

* `docker run IMAGE[:TAG][@DIGEST]`
* `docker create IMAGE[:TAG][@DIGEST]`

An image tag is the image version, which defaults to `latest` when omitted. Use the tag to run a container from specific version of an image. For example, to run version `24.04` of the `ubuntu` image: `docker run ubuntu:24.04`.

#### [Image digests](#image-digests)

Images using the v2 or later image format have a content-addressable identifier called a digest. As long as the input used to generate the image is unchanged, the digest value is predictable.

The following example runs a container from the `alpine` image with the `sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0` digest:

```console
$ docker run alpine@sha256:9cacb71397b640eca97488cf08582ae4e4068513101088e9f96c9814bfda95e0 date
```

### [Options](#options)

`[OPTIONS]` let you configure options for the container. For example, you can give the container a name (`--name`), or run it as a background process (`-d`). You can also set options to control things like resource constraints and networking.

### [Commands and arguments](#commands-and-arguments)

You can use the `[COMMAND]` and `[ARG...]` positional arguments to specify commands and arguments for the container to run when it starts up. For example, you can specify `sh` as the `[COMMAND]`, combined with the `-i` and `-t` flags, to start an interactive shell in the container (if the image you select has an `sh` executable on `PATH`).

```console
$ docker run -it IMAGE sh
```

> Note
>
> Depending on your Docker system configuration, you may be required to preface the `docker run` command with `sudo`. To avoid having to use `sudo` with the `docker` command, your system administrator can create a Unix group called `docker` and add users to it. For more information about this configuration, refer to the Docker installation documentation for your operating system.

## [Foreground and background](#foreground-and-background)

When you start a container, the container runs in the foreground by default. If you want to run the container in the background instead, you can use the `--detach` (or `-d`) flag. This starts the container without occupying your terminal window.

```console
$ docker run -d IMAGE
```

While the container runs in the background, you can interact with the container using other CLI commands. For example, `docker logs` lets you view the logs for the container, and `docker attach` brings it to the foreground.

```console
$ docker run -d nginx
0246aa4d1448a401cabd2ce8f242192b6e7af721527e48a810463366c7ff54f1
$ docker ps
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS        PORTS     NAMES
0246aa4d1448   nginx     "/docker-entrypoint.…"   2 seconds ago   Up 1 second   80/tcp    pedantic_liskov
$ docker logs -n 5 0246aa4d1448
2023/11/06 15:58:23 [notice] 1#1: start worker process 33
2023/11/06 15:58:23 [notice] 1#1: start worker process 34
2023/11/06 15:58:23 [notice] 1#1: start worker process 35
2023/11/06 15:58:23 [notice] 1#1: start worker process 36
2023/11/06 15:58:23 [notice] 1#1: start worker process 37
$ docker attach 0246aa4d1448
^C
2023/11/06 15:58:40 [notice] 1#1: signal 2 (SIGINT) received, exiting
...
```

For more information about `docker run` flags related to foreground and background modes, see:

* [`docker run --detach`](https://docs.docker.com/reference/cli/docker/container/run/#detach): run container in background
* [`docker run --attach`](https://docs.docker.com/reference/cli/docker/container/run/#attach): attach to `stdin`, `stdout`, and `stderr`
* [`docker run --tty`](https://docs.docker.com/reference/cli/docker/container/run/#tty): allocate a pseudo-tty
* [`docker run --interactive`](https://docs.docker.com/reference/cli/docker/container/run/#interactive): keep `stdin` open even if not attached

For more information about re-attaching to a background container, see [`docker attach`](https://docs.docker.com/reference/cli/docker/container/attach/).

## [Container identification](#container-identification)

You can identify a container in three ways:

| Identifier type       | Example value                                                      |
| --------------------- | ------------------------------------------------------------------ |
| UUID long identifier  | `f78375b1c487e03c9438c729345e54db9d20cfa2ac1fc3494b6eb60872e74778` |
| UUID short identifier | `f78375b1c487`                                                     |
| Name                  | `evil_ptolemy`                                                     |

The UUID identifier is a random ID assigned to the container by the daemon.

The daemon generates a random string name for containers automatically. You can also define a custom name using [the `--name` flag](https://docs.docker.com/reference/cli/docker/container/run/#name). Defining a `name` can be a handy way to add meaning to a container. If you specify a `name`, you can use it when referring to the container in a user-defined network. This works for both background and foreground Docker containers.

A container identifier is not the same thing as an image reference. The image reference specifies which image to use when you run a container. You can't run `docker exec nginx:alpine sh` to open a shell in a container based on the `nginx:alpine` image, because `docker exec` expects a container identifier (name or ID), not an image.

While the image used by a container is not an identifier for the container, you find out the IDs of containers using an image by using the `--filter` flag. For example, the following `docker ps` command gets the IDs of all running containers based on the `nginx:alpine` image:

```console
$ docker ps -q --filter ancestor=nginx:alpine
```

For more information about using filters, see [Filtering](https://docs.docker.com/config/filter/).

## [Container networking](#container-networking)

Containers have networking enabled by default, and they can make outgoing connections. If you're running multiple containers that need to communicate with each other, you can create a custom network and attach the containers to the network.

When multiple containers are attached to the same custom network, they can communicate with each other using the container names as a DNS hostname. The following example creates a custom network named `my-net`, and runs two containers that attach to the network.

```console
$ docker network create my-net
$ docker run -d --name web --network my-net nginx:alpine
$ docker run --rm -it --network my-net busybox
/ # ping web
PING web (172.18.0.2): 56 data bytes
64 bytes from 172.18.0.2: seq=0 ttl=64 time=0.326 ms
64 bytes from 172.18.0.2: seq=1 ttl=64 time=0.257 ms
64 bytes from 172.18.0.2: seq=2 ttl=64 time=0.281 ms
^C
--- web ping statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 0.257/0.288/0.326 ms
```

For more information about container networking, see [Networking overview](https://docs.docker.com/network/)

## [Filesystem mounts](#filesystem-mounts)

By default, the data in a container is stored in an ephemeral, writable container layer. Removing the container also removes its data. If you want to use persistent data with containers, you can use filesystem mounts to store the data persistently on the host system. Filesystem mounts can also let you share data between containers and the host.

Docker supports two main categories of mounts:

* Volume mounts
* Bind mounts

Volume mounts are great for persistently storing data for containers, and for sharing data between containers. Bind mounts, on the other hand, are for sharing data between a container and the host.

You can add a filesystem mount to a container using the `--mount` flag for the `docker run` command.

The following sections show basic examples of how to create volumes and bind mounts. For more in-depth examples and descriptions, refer to the section of the [storage section](https://docs.docker.com/storage/) in the documentation.

### [Volume mounts](#volume-mounts)

To create a volume mount:

```console
$ docker run --mount source=VOLUME_NAME,target=[PATH] [IMAGE] [COMMAND...]
```

The `--mount` flag takes two parameters in this case: `source` and `target`. The value for the `source` parameter is the name of the volume. The value of `target` is the mount location of the volume inside the container. Once you've created the volume, any data you write to the volume is persisted, even if you stop or remove the container:

```console
$ docker run --rm --mount source=my_volume,target=/foo busybox \
  echo "hello, volume!" > /foo/hello.txt
$ docker run --mount source=my_volume,target=/bar busybox
  cat /bar/hello.txt
hello, volume!
```

The `target` must always be an absolute path, such as `/src/docs`. An absolute path starts with a `/` (forward slash). Volume names must start with an alphanumeric character, followed by `a-z0-9`, `_` (underscore), `.` (period) or `-` (hyphen).

### [Bind mounts](#bind-mounts)

To create a bind mount:

```console
$ docker run -it --mount type=bind,source=[PATH],target=[PATH] busybox
```

In this case, the `--mount` flag takes three parameters. A type (`bind`), and two paths. The `source` path is the location on the host that you want to bind mount into the container. The `target` path is the mount destination inside the container.

By default, bind mounts require the source path to exist on the daemon host. If the source path doesn't exist, an error is returned. To create the source path on the daemon host if it doesn't exist, use the `bind-create-src` option:

```console
$ docker run -it --mount type=bind,source=[PATH],target=[PATH],bind-create-src busybox
```

Bind mounts are read-write by default, meaning that you can both read and write files to and from the mounted location from the container. Changes that you make, such as adding or editing files, are reflected on the host filesystem:

```console
$ docker run -it --mount type=bind,source=.,target=/foo busybox
/ # echo "hello from container" > /foo/hello.txt
/ # exit
$ cat hello.txt
hello from container
```

## [Exit status](#exit-status)

The exit code from `docker run` gives information about why the container failed to run or why it exited. The following sections describe the meanings of different container exit codes values.

### [125](#125)

Exit code `125` indicates that the error is with Docker daemon itself.

```console
$ docker run --foo busybox; echo $?

flag provided but not defined: --foo
See 'docker run --help'.
125
```

### [126](#126)

Exit code `126` indicates that the specified contained command can't be invoked. The container command in the following example is: `/etc`.

```console
$ docker run busybox /etc; echo $?

docker: Error response from daemon: Container command '/etc' could not be invoked.
126
```

### [127](#127)

Exit code `127` indicates that the contained command can't be found.

```console
$ docker run busybox foo; echo $?

docker: Error response from daemon: Container command 'foo' not found or does not exist.
127
```

### [Other exit codes](#other-exit-codes)

Any exit code other than `125`, `126`, and `127` represent the exit code of the provided container command.

```console
$ docker run busybox /bin/sh -c 'exit 3'
$ echo $?
3
```

## [Runtime constraints on resources](#runtime-constraints-on-resources)

The operator can also adjust the performance parameters of the container:

| Option                     | Description                                                                                                                                                                                                                                                                              |
| -------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-m`, `--memory=""`        | Memory limit (format: `<number>[<unit>]`). Number is a positive integer. Unit can be one of `b`, `k`, `m`, or `g`. Minimum is 6M.                                                                                                                                                        |
| `--memory-swap=""`         | Total memory limit (memory + swap, format: `<number>[<unit>]`). Number is a positive integer. Unit can be one of `b`, `k`, `m`, or `g`.                                                                                                                                                  |
| `--memory-reservation=""`  | Memory soft limit (format: `<number>[<unit>]`). Number is a positive integer. Unit can be one of `b`, `k`, `m`, or `g`.                                                                                                                                                                  |
| `-c`, `--cpu-shares=0`     | CPU shares (relative weight)                                                                                                                                                                                                                                                             |
| `--cpus=0.000`             | Number of CPUs. Number is a fractional number. 0.000 means no limit.                                                                                                                                                                                                                     |
| `--cpu-period=0`           | Limit the CPU CFS (Completely Fair Scheduler) period                                                                                                                                                                                                                                     |
| `--cpuset-cpus=""`         | CPUs in which to allow execution (0-3, 0,1)                                                                                                                                                                                                                                              |
| `--cpuset-mems=""`         | Memory nodes (MEMs) in which to allow execution (0-3, 0,1). Only effective on NUMA systems.                                                                                                                                                                                              |
| `--cpu-quota=0`            | Limit the CPU CFS (Completely Fair Scheduler) quota                                                                                                                                                                                                                                      |
| `--cpu-rt-period=0`        | Limit the CPU real-time period. In microseconds. Requires parent cgroups be set and cannot be higher than parent. Also check rtprio ulimits.                                                                                                                                             |
| `--cpu-rt-runtime=0`       | Limit the CPU real-time runtime. In microseconds. Requires parent cgroups be set and cannot be higher than parent. Also check rtprio ulimits.                                                                                                                                            |
| `--blkio-weight=0`         | Block IO weight (relative weight) accepts a weight value between 10 and 1000.                                                                                                                                                                                                            |
| `--blkio-weight-device=""` | Block IO weight (relative device weight, format: `DEVICE_NAME:WEIGHT`)                                                                                                                                                                                                                   |
| `--device-read-bps=""`     | Limit read rate from a device (format: `<device-path>:<number>[<unit>]`). Number is a positive integer. Unit can be one of `kb`, `mb`, or `gb`.                                                                                                                                          |
| `--device-write-bps=""`    | Limit write rate to a device (format: `<device-path>:<number>[<unit>]`). Number is a positive integer. Unit can be one of `kb`, `mb`, or `gb`.                                                                                                                                           |
| `--device-read-iops=""`    | Limit read rate (IO per second) from a device (format: `<device-path>:<number>`). Number is a positive integer.                                                                                                                                                                          |
| `--device-write-iops=""`   | Limit write rate (IO per second) to a device (format: `<device-path>:<number>`). Number is a positive integer.                                                                                                                                                                           |
| `--oom-kill-disable=false` | Whether to disable OOM Killer for the container or not.                                                                                                                                                                                                                                  |
| `--oom-score-adj=0`        | Tune container's OOM preferences (-1000 to 1000)                                                                                                                                                                                                                                         |
| `--memory-swappiness=""`   | Tune a container's memory swappiness behavior. Accepts an integer between 0 and 100.                                                                                                                                                                                                     |
| `--shm-size=""`            | Size of `/dev/shm`. The format is `<number><unit>`. `number` must be greater than `0`. Unit is optional and can be `b` (bytes), `k` (kilobytes), `m` (megabytes), or `g` (gigabytes). If you omit the unit, the system uses bytes. If you omit the size entirely, the system uses `64m`. |

### [User memory constraints](#user-memory-constraints)

We have four ways to set user memory usage:

| Option                                      | Result                                                                                                                                                                                  |
| ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **memory=inf, memory-swap=inf** (default)   | There is no memory limit for the container. The container can use as much memory as needed.                                                                                             |
| **memory=L\<inf, memory-swap=inf**          | (specify memory and set memory-swap as `-1`) The container is not allowed to use more than L bytes of memory, but can use as much swap as is needed (if the host supports swap memory). |
| **memory=L\<inf, memory-swap=2\*L**         | (specify memory without memory-swap) The container is not allowed to use more than L bytes of memory, swap *plus* memory usage is double of that.                                       |
| **memory=L\<inf, memory-swap=S\<inf, L<=S** | (specify both memory and memory-swap) The container is not allowed to use more than L bytes of memory, swap *plus* memory usage is limited by S.                                        |

Examples:

```console
$ docker run -it ubuntu:24.04 /bin/bash
```

We set nothing about memory, this means the processes in the container can use as much memory and swap memory as they need.

```console
$ docker run -it -m 300M --memory-swap -1 ubuntu:24.04 /bin/bash
```

We set memory limit and disabled swap memory limit, this means the processes in the container can use 300M memory and as much swap memory as they need (if the host supports swap memory).

```console
$ docker run -it -m 300M ubuntu:24.04 /bin/bash
```

We set memory limit only, this means the processes in the container can use 300M memory and 300M swap memory, by default, the total virtual memory size (`--memory-swap`) will be set as double of memory, in this case, memory + swap would be 2\*300M, so processes can use 300M swap memory as well.

```console
$ docker run -it -m 300M --memory-swap 1G ubuntu:24.04 /bin/bash
```

We set both memory and swap memory, so the processes in the container can use 300M memory and 700M swap memory.

Memory reservation is a kind of memory soft limit that allows for greater sharing of memory. Under normal circumstances, containers can use as much of the memory as needed and are constrained only by the hard limits set with the `-m`/`--memory` option. When memory reservation is set, Docker detects memory contention or low memory and forces containers to restrict their consumption to a reservation limit.

Always set the memory reservation value below the hard limit, otherwise the hard limit takes precedence. A reservation of 0 is the same as setting no reservation. By default (without reservation set), memory reservation is the same as the hard memory limit.

Memory reservation is a soft-limit feature and does not guarantee the limit won't be exceeded. Instead, the feature attempts to ensure that, when memory is heavily contended for, memory is allocated based on the reservation hints/setup.

The following example limits the memory (`-m`) to 500M and sets the memory reservation to 200M.

```console
$ docker run -it -m 500M --memory-reservation 200M ubuntu:24.04 /bin/bash
```

Under this configuration, when the container consumes memory more than 200M and less than 500M, the next system memory reclaim attempts to shrink container memory below 200M.

The following example set memory reservation to 1G without a hard memory limit.

```console
$ docker run -it --memory-reservation 1G ubuntu:24.04 /bin/bash
```

The container can use as much memory as it needs. The memory reservation setting ensures the container doesn't consume too much memory for long time, because every memory reclaim shrinks the container's consumption to the reservation.

By default, kernel kills processes in a container if an out-of-memory (OOM) error occurs. To change this behaviour, use the `--oom-kill-disable` option. Only disable the OOM killer on containers where you have also set the `-m/--memory` option. If the `-m` flag is not set, this can result in the host running out of memory and require killing the host's system processes to free memory.

The following example limits the memory to 100M and disables the OOM killer for this container:

```console
$ docker run -it -m 100M --oom-kill-disable ubuntu:24.04 /bin/bash
```

The following example, illustrates a dangerous way to use the flag:

```console
$ docker run -it --oom-kill-disable ubuntu:24.04 /bin/bash
```

The container has unlimited memory which can cause the host to run out memory and require killing system processes to free memory. The `--oom-score-adj` parameter can be changed to select the priority of which containers will be killed when the system is out of memory, with negative scores making them less likely to be killed, and positive scores more likely.

### [Swappiness constraint](#swappiness-constraint)

By default, a container's kernel can swap out a percentage of anonymous pages. To set this percentage for a container, specify a `--memory-swappiness` value between 0 and 100. A value of 0 turns off anonymous page swapping. A value of 100 sets all anonymous pages as swappable. By default, if you are not using `--memory-swappiness`, memory swappiness value will be inherited from the parent.

For example, you can set:

```console
$ docker run -it --memory-swappiness=0 ubuntu:24.04 /bin/bash
```

Setting the `--memory-swappiness` option is helpful when you want to retain the container's working set and to avoid swapping performance penalties.

### [CPU share constraint](#cpu-share-constraint)

By default, all containers get the same proportion of CPU cycles. This proportion can be modified by changing the container's CPU share weighting relative to the weighting of all other running containers.

To modify the proportion from the default of 1024, use the `-c` or `--cpu-shares` flag to set the weighting to 2 or higher. If 0 is set, the system will ignore the value and use the default of 1024.

The proportion will only apply when CPU-intensive processes are running. When tasks in one container are idle, other containers can use the left-over CPU time. The actual amount of CPU time will vary depending on the number of containers running on the system.

For example, consider three containers, one has a cpu-share of 1024 and two others have a cpu-share setting of 512. When processes in all three containers attempt to use 100% of CPU, the first container would receive 50% of the total CPU time. If you add a fourth container with a cpu-share of 1024, the first container only gets 33% of the CPU. The remaining containers receive 16.5%, 16.5% and 33% of the CPU.

On a multi-core system, the shares of CPU time are distributed over all CPU cores. Even if a container is limited to less than 100% of CPU time, it can use 100% of each individual CPU core.

For example, consider a system with more than three cores. If you start one container `{C0}` with `-c=512` running one process, and another container `{C1}` with `-c=1024` running two processes, this can result in the following division of CPU shares:

```
PID    container	CPU	CPU share
100    {C0}		0	100% of CPU0
101    {C1}		1	100% of CPU1
102    {C1}		2	100% of CPU2
```

### [CPU period constraint](#cpu-period-constraint)

The default CPU CFS (Completely Fair Scheduler) period is 100ms. We can use `--cpu-period` to set the period of CPUs to limit the container's CPU usage. And usually `--cpu-period` should work with `--cpu-quota`.

Examples:

```console
$ docker run -it --cpu-period=50000 --cpu-quota=25000 ubuntu:24.04 /bin/bash
```

If there is 1 CPU, this means the container can get 50% CPU worth of run-time every 50ms.

In addition to use `--cpu-period` and `--cpu-quota` for setting CPU period constraints, it is possible to specify `--cpus` with a float number to achieve the same purpose. For example, if there is 1 CPU, then `--cpus=0.5` will achieve the same result as setting `--cpu-period=50000` and `--cpu-quota=25000` (50% CPU).

The default value for `--cpus` is `0.000`, which means there is no limit.

For more information, see the [CFS documentation on bandwidth limiting](https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt).

### [Cpuset constraint](#cpuset-constraint)

We can set cpus in which to allow execution for containers.

Examples:

```console
$ docker run -it --cpuset-cpus="1,3" ubuntu:24.04 /bin/bash
```

This means processes in container can be executed on cpu 1 and cpu 3.

```console
$ docker run -it --cpuset-cpus="0-2" ubuntu:24.04 /bin/bash
```

This means processes in container can be executed on cpu 0, cpu 1 and cpu 2.

We can set mems in which to allow execution for containers. Only effective on NUMA systems.

Examples:

```console
$ docker run -it --cpuset-mems="1,3" ubuntu:24.04 /bin/bash
```

This example restricts the processes in the container to only use memory from memory nodes 1 and 3.

```console
$ docker run -it --cpuset-mems="0-2" ubuntu:24.04 /bin/bash
```

This example restricts the processes in the container to only use memory from memory nodes 0, 1 and 2.

### [CPU quota constraint](#cpu-quota-constraint)

The `--cpu-quota` flag limits the container's CPU usage. The default 0 value allows the container to take 100% of a CPU resource (1 CPU). The CFS (Completely Fair Scheduler) handles resource allocation for executing processes and is default Linux Scheduler used by the kernel. Set this value to 50000 to limit the container to 50% of a CPU resource. For multiple CPUs, adjust the `--cpu-quota` as necessary. For more information, see the [CFS documentation on bandwidth limiting](https://www.kernel.org/doc/Documentation/scheduler/sched-bwc.txt).

### [Block IO bandwidth (Blkio) constraint](#block-io-bandwidth-blkio-constraint)

By default, all containers get the same proportion of block IO bandwidth (blkio). This proportion is 500. To modify this proportion, change the container's blkio weight relative to the weighting of all other running containers using the `--blkio-weight` flag.

> Note
>
> The blkio weight setting is only available for direct IO. Buffered IO is not currently supported.

The `--blkio-weight` flag can set the weighting to a value between 10 to 1000. For example, the commands below create two containers with different blkio weight:

```console
$ docker run -it --name c1 --blkio-weight 300 ubuntu:24.04 /bin/bash
$ docker run -it --name c2 --blkio-weight 600 ubuntu:24.04 /bin/bash
```

If you do block IO in the two containers at the same time, by, for example:

```console
$ time dd if=/mnt/zerofile of=test.out bs=1M count=1024 oflag=direct
```

You'll find that the proportion of time is the same as the proportion of blkio weights of the two containers.

The `--blkio-weight-device="DEVICE_NAME:WEIGHT"` flag sets a specific device weight. The `DEVICE_NAME:WEIGHT` is a string containing a colon-separated device name and weight. For example, to set `/dev/sda` device weight to `200`:

```console
$ docker run -it \
    --blkio-weight-device "/dev/sda:200" \
    ubuntu
```

If you specify both the `--blkio-weight` and `--blkio-weight-device`, Docker uses the `--blkio-weight` as the default weight and uses `--blkio-weight-device` to override this default with a new value on a specific device. The following example uses a default weight of `300` and overrides this default on `/dev/sda` setting that weight to `200`:

```console
$ docker run -it \
    --blkio-weight 300 \
    --blkio-weight-device "/dev/sda:200" \
    ubuntu
```

The `--device-read-bps` flag limits the read rate (bytes per second) from a device. For example, this command creates a container and limits the read rate to `1mb` per second from `/dev/sda`:

```console
$ docker run -it --device-read-bps /dev/sda:1mb ubuntu
```

The `--device-write-bps` flag limits the write rate (bytes per second) to a device. For example, this command creates a container and limits the write rate to `1mb` per second for `/dev/sda`:

```console
$ docker run -it --device-write-bps /dev/sda:1mb ubuntu
```

Both flags take limits in the `<device-path>:<limit>[unit]` format. Both read and write rates must be a positive integer. You can specify the rate in `kb` (kilobytes), `mb` (megabytes), or `gb` (gigabytes).

The `--device-read-iops` flag limits read rate (IO per second) from a device. For example, this command creates a container and limits the read rate to `1000` IO per second from `/dev/sda`:

```console
$ docker run -it --device-read-iops /dev/sda:1000 ubuntu
```

The `--device-write-iops` flag limits write rate (IO per second) to a device. For example, this command creates a container and limits the write rate to `1000` IO per second to `/dev/sda`:

```console
$ docker run -it --device-write-iops /dev/sda:1000 ubuntu
```

Both flags take limits in the `<device-path>:<limit>` format. Both read and write rates must be a positive integer.

## [Additional groups](#additional-groups)

```console
--group-add: Add additional groups to run as
```

By default, the docker container process runs with the supplementary groups looked up for the specified user. If one wants to add more to that list of groups, then one can use this flag:

```console
$ docker run --rm --group-add audio --group-add nogroup --group-add 777 busybox id

uid=0(root) gid=0(root) groups=10(wheel),29(audio),99(nogroup),777
```

## [Runtime privilege and Linux capabilities](#runtime-privilege-and-linux-capabilities)

| Option         | Description                                                                     |
| -------------- | ------------------------------------------------------------------------------- |
| `--cap-add`    | Add Linux capabilities                                                          |
| `--cap-drop`   | Drop Linux capabilities                                                         |
| `--privileged` | Give extended privileges to this container                                      |
| `--device=[]`  | Allows you to run devices inside the container without the `--privileged` flag. |

By default, Docker containers are "unprivileged" and cannot, for example, run a Docker daemon inside a Docker container. This is because by default a container is not allowed to access any devices, but a "privileged" container is given access to all devices (see the documentation on [cgroups devices](https://www.kernel.org/doc/Documentation/cgroup-v1/devices.txt)).

The `--privileged` flag gives all capabilities to the container. When the operator executes `docker run --privileged`, Docker enables access to all devices on the host, and reconfigures AppArmor or SELinux to allow the container nearly all the same access to the host as processes running outside containers on the host. Use this flag with caution. For more information about the `--privileged` flag, see the [`docker run` reference](https://docs.docker.com/reference/cli/docker/container/run/#privileged).

If you want to limit access to a specific device or devices you can use the `--device` flag. It allows you to specify one or more devices that will be accessible within the container.

```console
$ docker run --device=/dev/snd:/dev/snd ...
```

By default, the container will be able to `read`, `write`, and `mknod` these devices. This can be overridden using a third `:rwm` set of options to each `--device` flag:

```console
$ docker run --device=/dev/sda:/dev/xvdc --rm -it ubuntu fdisk  /dev/xvdc

Command (m for help): q
$ docker run --device=/dev/sda:/dev/xvdc:r --rm -it ubuntu fdisk  /dev/xvdc
You will not be able to write the partition table.

Command (m for help): q

$ docker run --device=/dev/sda:/dev/xvdc:w --rm -it ubuntu fdisk  /dev/xvdc
    crash....

$ docker run --device=/dev/sda:/dev/xvdc:m --rm -it ubuntu fdisk  /dev/xvdc
fdisk: unable to open /dev/xvdc: Operation not permitted
```

In addition to `--privileged`, the operator can have fine grain control over the capabilities using `--cap-add` and `--cap-drop`. By default, Docker has a default list of capabilities that are kept. The following table lists the Linux capability options which are allowed by default and can be dropped.

| Capability Key     | Capability Description                                                                                                        |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------- |
| AUDIT\_WRITE       | Write records to kernel auditing log.                                                                                         |
| CHOWN              | Make arbitrary changes to file UIDs and GIDs (see chown(2)).                                                                  |
| DAC\_OVERRIDE      | Bypass file read, write, and execute permission checks.                                                                       |
| FOWNER             | Bypass permission checks on operations that normally require the file system UID of the process to match the UID of the file. |
| FSETID             | Don't clear set-user-ID and set-group-ID permission bits when a file is modified.                                             |
| KILL               | Bypass permission checks for sending signals.                                                                                 |
| MKNOD              | Create special files using mknod(2).                                                                                          |
| NET\_BIND\_SERVICE | Bind a socket to internet domain privileged ports (port numbers less than 1024).                                              |
| NET\_RAW           | Use RAW and PACKET sockets.                                                                                                   |
| SETFCAP            | Set file capabilities.                                                                                                        |
| SETGID             | Make arbitrary manipulations of process GIDs and supplementary GID list.                                                      |
| SETPCAP            | Modify process capabilities.                                                                                                  |
| SETUID             | Make arbitrary manipulations of process UIDs.                                                                                 |
| SYS\_CHROOT        | Use chroot(2), change root directory.                                                                                         |

The next table shows the capabilities which are not granted by default and may be added.

| Capability Key      | Capability Description                                                                                                      |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| AUDIT\_CONTROL      | Enable and disable kernel auditing; change auditing filter rules; retrieve auditing status and filtering rules.             |
| AUDIT\_READ         | Allow reading the audit log via multicast netlink socket.                                                                   |
| BLOCK\_SUSPEND      | Allow preventing system suspends.                                                                                           |
| BPF                 | Allow creating BPF maps, loading BPF Type Format (BTF) data, retrieve JITed code of BPF programs, and more.                 |
| CHECKPOINT\_RESTORE | Allow checkpoint/restore related operations. Introduced in kernel 5.9.                                                      |
| DAC\_READ\_SEARCH   | Bypass file read permission checks and directory read and execute permission checks.                                        |
| IPC\_LOCK           | Lock memory (mlock(2), mlockall(2), mmap(2), shmctl(2)).                                                                    |
| IPC\_OWNER          | Bypass permission checks for operations on System V IPC objects.                                                            |
| LEASE               | Establish leases on arbitrary files (see fcntl(2)).                                                                         |
| LINUX\_IMMUTABLE    | Set the FS\_APPEND\_FL and FS\_IMMUTABLE\_FL i-node flags.                                                                  |
| MAC\_ADMIN          | Allow MAC configuration or state changes. Implemented for the Smack LSM.                                                    |
| MAC\_OVERRIDE       | Override Mandatory Access Control (MAC). Implemented for the Smack Linux Security Module (LSM).                             |
| NET\_ADMIN          | Perform various network-related operations.                                                                                 |
| NET\_BROADCAST      | Make socket broadcasts, and listen to multicasts.                                                                           |
| PERFMON             | Allow system performance and observability privileged operations using perf\_events, i915\_perf and other kernel subsystems |
| SYS\_ADMIN          | Perform a range of system administration operations.                                                                        |
| SYS\_BOOT           | Use reboot(2) and kexec\_load(2), reboot and load a new kernel for later execution.                                         |
| SYS\_MODULE         | Load and unload kernel modules.                                                                                             |
| SYS\_NICE           | Raise process nice value (nice(2), setpriority(2)) and change the nice value for arbitrary processes.                       |
| SYS\_PACCT          | Use acct(2), switch process accounting on or off.                                                                           |
| SYS\_PTRACE         | Trace arbitrary processes using ptrace(2).                                                                                  |
| SYS\_RAWIO          | Perform I/O port operations (iopl(2) and ioperm(2)).                                                                        |
| SYS\_RESOURCE       | Override resource Limits.                                                                                                   |
| SYS\_TIME           | Set system clock (settimeofday(2), stime(2), adjtimex(2)); set real-time (hardware) clock.                                  |
| SYS\_TTY\_CONFIG    | Use vhangup(2); employ various privileged ioctl(2) operations on virtual terminals.                                         |
| SYSLOG              | Perform privileged syslog(2) operations.                                                                                    |
| WAKE\_ALARM         | Trigger something that will wake up the system.                                                                             |

Further reference information is available on the [capabilities(7) - Linux man page](https://man7.org/linux/man-pages/man7/capabilities.7.html), and in the [Linux kernel source code](https://github.com/torvalds/linux/blob/124ea650d3072b005457faed69909221c2905a1f/include/uapi/linux/capability.h).

Both flags support the value `ALL`, so to allow a container to use all capabilities except for `MKNOD`:

```console
$ docker run --cap-add=ALL --cap-drop=MKNOD ...
```

The `--cap-add` and `--cap-drop` flags accept capabilities to be specified with a `CAP_` prefix. The following examples are therefore equivalent:

```console
$ docker run --cap-add=SYS_ADMIN ...
$ docker run --cap-add=CAP_SYS_ADMIN ...
```

For interacting with the network stack, instead of using `--privileged` they should use `--cap-add=NET_ADMIN` to modify the network interfaces.

```console
$ docker run -it --rm  ubuntu:24.04 ip link add dummy0 type dummy

RTNETLINK answers: Operation not permitted

$ docker run -it --rm --cap-add=NET_ADMIN ubuntu:24.04 ip link add dummy0 type dummy
```

To mount a FUSE based filesystem, you need to combine both `--cap-add` and `--device`:

```console
$ docker run --rm -it --cap-add SYS_ADMIN sshfs sshfs sven@10.10.10.20:/home/sven /mnt

fuse: failed to open /dev/fuse: Operation not permitted

$ docker run --rm -it --device /dev/fuse sshfs sshfs sven@10.10.10.20:/home/sven /mnt

fusermount: mount failed: Operation not permitted

$ docker run --rm -it --cap-add SYS_ADMIN --device /dev/fuse sshfs

# sshfs sven@10.10.10.20:/home/sven /mnt
The authenticity of host '10.10.10.20 (10.10.10.20)' can't be established.
ECDSA key fingerprint is 25:34:85:75:25:b0:17:46:05:19:04:93:b5:dd:5f:c6.
Are you sure you want to continue connecting (yes/no)? yes
sven@10.10.10.20's password:

root@30aa0cfaf1b5:/# ls -la /mnt/src/docker

total 1516
drwxrwxr-x 1 1000 1000   4096 Dec  4 06:08 .
drwxrwxr-x 1 1000 1000   4096 Dec  4 11:46 ..
-rw-rw-r-- 1 1000 1000     16 Oct  8 00:09 .dockerignore
-rwxrwxr-x 1 1000 1000    464 Oct  8 00:09 .drone.yml
drwxrwxr-x 1 1000 1000   4096 Dec  4 06:11 .git
-rw-rw-r-- 1 1000 1000    461 Dec  4 06:08 .gitignore
....
```

The default seccomp profile will adjust to the selected capabilities, in order to allow use of facilities allowed by the capabilities, so you should not have to adjust this.

## [Overriding image defaults](#overriding-image-defaults)

When you build an image from a [Dockerfile](https://docs.docker.com/reference/dockerfile/), or when committing it, you can set a number of default parameters that take effect when the image starts up as a container. When you run an image, you can override those defaults using flags for the `docker run` command.

* [Default entrypoint](#default-entrypoint)
* [Default command and options](#default-command-and-options)
* [Expose ports](#exposed-ports)
* [Environment variables](#environment-variables)
* [Healthcheck](#healthchecks)
* [User](#user)
* [Working directory](#working-directory)

### [Default command and options](#default-command-and-options)

The command syntax for `docker run` supports optionally specifying commands and arguments to the container's entrypoint, represented as `[COMMAND]` and `[ARG...]` in the following synopsis example:

```console
$ docker run [OPTIONS] IMAGE[:TAG|@DIGEST] [COMMAND] [ARG...]
```

This command is optional because whoever created the `IMAGE` may have already provided a default `COMMAND`, using the Dockerfile `CMD` instruction. When you run a container, you can override that `CMD` instruction just by specifying a new `COMMAND`.

If the image also specifies an `ENTRYPOINT` then the `CMD` or `COMMAND` get appended as arguments to the `ENTRYPOINT`.

### [Default entrypoint](#default-entrypoint)

```text
--entrypoint="": Overwrite the default entrypoint set by the image
```

The entrypoint refers to the default executable that's invoked when you run a container. A container's entrypoint is defined using the Dockerfile `ENTRYPOINT` instruction. It's similar to specifying a default command because it specifies, but the difference is that you need to pass an explicit flag to override the entrypoint, whereas you can override default commands with positional arguments. The defines a container's default behavior, with the idea that when you set an entrypoint you can run the container *as if it were that binary*, complete with default options, and you can pass in more options as commands. But there are cases where you may want to run something else inside the container. This is when overriding the default entrypoint at runtime comes in handy, using the `--entrypoint` flag for the `docker run` command.

The `--entrypoint` flag expects a string value, representing the name or path of the binary that you want to invoke when the container starts. The following example shows you how to run a Bash shell in a container that has been set up to automatically run some other binary (like `/usr/bin/redis-server`):

```console
$ docker run -it --entrypoint /bin/bash example/redis
```

The following examples show how to pass additional parameters to the custom entrypoint, using the positional command arguments:

```console
$ docker run -it --entrypoint /bin/bash example/redis -c ls -l
$ docker run -it --entrypoint /usr/bin/redis-cli example/redis --help
```

You can reset a containers entrypoint by passing an empty string, for example:

```console
$ docker run -it --entrypoint="" mysql bash
```

> Note
>
> Passing `--entrypoint` clears out any default command set on the image. That is, any `CMD` instruction in the Dockerfile used to build it.

### [Exposed ports](#exposed-ports)

By default, when you run a container, none of the container's ports are exposed to the host. This means you won't be able to access any ports that the container might be listening on. To make a container's ports accessible from the host, you need to publish the ports.

You can start the container with the `-P` or `-p` flags to expose its ports:

* The `-P` (or `--publish-all`) flag publishes all the exposed ports to the host. Docker binds each exposed port to a random port on the host.

  The `-P` flag only publishes port numbers that are explicitly flagged as exposed, either using the Dockerfile `EXPOSE` instruction or the `--expose` flag for the `docker run` command.

* The `-p` (or `--publish`) flag lets you explicitly map a single port or range of ports in the container to the host.

The port number inside the container (where the service listens) doesn't need to match the port number published on the outside of the container (where clients connect). For example, inside the container an HTTP service might be listening on port 80. At runtime, the port might be bound to 42800 on the host. To find the mapping between the host ports and the exposed ports, use the `docker port` command.

### [Environment variables](#environment-variables)

Docker automatically sets some environment variables when creating a Linux container. Docker doesn't set any environment variables when creating a Windows container.

The following environment variables are set for Linux containers:

| Variable   | Value                                                                                                |
| ---------- | ---------------------------------------------------------------------------------------------------- |
| `HOME`     | Set based on the value of `USER`                                                                     |
| `HOSTNAME` | The hostname associated with the container                                                           |
| `PATH`     | Includes popular directories, such as `/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin` |
| `TERM`     | `xterm` if the container is allocated a pseudo-TTY                                                   |

Additionally, you can set any environment variable in the container by using one or more `-e` flags. You can even override the variables mentioned above, or variables defined using a Dockerfile `ENV` instruction when building the image.

If you name an environment variable without specifying a value, the current value of the named variable on the host is propagated into the container's environment:

```console
$ export today=Wednesday
$ docker run -e "deep=purple" -e today --rm alpine env

PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
HOSTNAME=d2219b854598
deep=purple
today=Wednesday
HOME=/root
```

```powershell
PS C:\> docker run --rm -e "foo=bar" microsoft/nanoserver cmd /s /c set
ALLUSERSPROFILE=C:\ProgramData
APPDATA=C:\Users\ContainerAdministrator\AppData\Roaming
CommonProgramFiles=C:\Program Files\Common Files
CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
CommonProgramW6432=C:\Program Files\Common Files
COMPUTERNAME=C2FAEFCC8253
ComSpec=C:\Windows\system32\cmd.exe
foo=bar
LOCALAPPDATA=C:\Users\ContainerAdministrator\AppData\Local
NUMBER_OF_PROCESSORS=8
OS=Windows_NT
Path=C:\Windows\system32;C:\Windows;C:\Windows\System32\Wbem;C:\Windows\System32\WindowsPowerShell\v1.0\;C:\Users\ContainerAdministrator\AppData\Local\Microsoft\WindowsApps
PATHEXT=.COM;.EXE;.BAT;.CMD
PROCESSOR_ARCHITECTURE=AMD64
PROCESSOR_IDENTIFIER=Intel64 Family 6 Model 62 Stepping 4, GenuineIntel
PROCESSOR_LEVEL=6
PROCESSOR_REVISION=3e04
ProgramData=C:\ProgramData
ProgramFiles=C:\Program Files
ProgramFiles(x86)=C:\Program Files (x86)
ProgramW6432=C:\Program Files
PROMPT=$P$G
PUBLIC=C:\Users\Public
SystemDrive=C:
SystemRoot=C:\Windows
TEMP=C:\Users\ContainerAdministrator\AppData\Local\Temp
TMP=C:\Users\ContainerAdministrator\AppData\Local\Temp
USERDOMAIN=User Manager
USERNAME=ContainerAdministrator
USERPROFILE=C:\Users\ContainerAdministrator
windir=C:\Windows
```

### [Healthchecks](#healthchecks)

The following flags for the `docker run` command let you control the parameters for container healthchecks:

| Option                    | Description                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------- |
| `--health-cmd`            | Command to run to check health                                                        |
| `--health-interval`       | Time between running the check                                                        |
| `--health-retries`        | Consecutive failures needed to report unhealthy                                       |
| `--health-timeout`        | Maximum time to allow one check to run                                                |
| `--health-start-period`   | Start period for the container to initialize before starting health-retries countdown |
| `--health-start-interval` | Time between running the check during the start period                                |
| `--no-healthcheck`        | Disable any container-specified `HEALTHCHECK`                                         |

Example:

```console
$ docker run --name=test -d \
    --health-cmd='stat /etc/passwd || exit 1' \
    --health-interval=2s \
    busybox sleep 1d
$ sleep 2; docker inspect --format='{{.State.Health.Status}}' test
healthy
$ docker exec test rm /etc/passwd
$ sleep 2; docker inspect --format='{{json .State.Health}}' test
{
  "Status": "unhealthy",
  "FailingStreak": 3,
  "Log": [
    {
      "Start": "2016-05-25T17:22:04.635478668Z",
      "End": "2016-05-25T17:22:04.7272552Z",
      "ExitCode": 0,
      "Output": "  File: /etc/passwd\n  Size: 334       \tBlocks: 8          IO Block: 4096   regular file\nDevice: 32h/50d\tInode: 12          Links: 1\nAccess: (0664/-rw-rw-r--)  Uid: (    0/    root)   Gid: (    0/    root)\nAccess: 2015-12-05 22:05:32.000000000\nModify: 2015..."
    },
    {
      "Start": "2016-05-25T17:22:06.732900633Z",
      "End": "2016-05-25T17:22:06.822168935Z",
      "ExitCode": 0,
      "Output": "  File: /etc/passwd\n  Size: 334       \tBlocks: 8          IO Block: 4096   regular file\nDevice: 32h/50d\tInode: 12          Links: 1\nAccess: (0664/-rw-rw-r--)  Uid: (    0/    root)   Gid: (    0/    root)\nAccess: 2015-12-05 22:05:32.000000000\nModify: 2015..."
    },
    {
      "Start": "2016-05-25T17:22:08.823956535Z",
      "End": "2016-05-25T17:22:08.897359124Z",
      "ExitCode": 1,
      "Output": "stat: can't stat '/etc/passwd': No such file or directory\n"
    },
    {
      "Start": "2016-05-25T17:22:10.898802931Z",
      "End": "2016-05-25T17:22:10.969631866Z",
      "ExitCode": 1,
      "Output": "stat: can't stat '/etc/passwd': No such file or directory\n"
    },
    {
      "Start": "2016-05-25T17:22:12.971033523Z",
      "End": "2016-05-25T17:22:13.082015516Z",
      "ExitCode": 1,
      "Output": "stat: can't stat '/etc/passwd': No such file or directory\n"
    }
  ]
}
```

The health status is also displayed in the `docker ps` output.

### [User](#user)

The default user within a container is `root` (uid = 0). You can set a default user to run the first process with the Dockerfile `USER` instruction. When starting a container, you can override the `USER` instruction by passing the `-u` option.

```text
-u="", --user="": Sets the username or UID used and optionally the groupname or GID for the specified command.
```

The following examples are all valid:

```text
--user=[ user | user:group | uid | uid:gid | user:gid | uid:group ]
```

> Note
>
> If you pass a numeric user ID, it must be in the range of 0-2147483647. If you pass a username, the user must exist in the container.

### [Working directory](#working-directory)

The default working directory for running binaries within a container is the root directory (`/`). The default working directory of an image is set using the Dockerfile `WORKDIR` command. You can override the default working directory for an image using the `-w` (or `--workdir`) flag for the `docker run` command:

```text
$ docker run --rm -w /my/workdir alpine pwd
/my/workdir
```

If the directory doesn't already exist in the container, it's created.

----
url: https://docs.docker.com/dhi/
----

# Docker Hardened Images

***

***

Docker Hardened Images (DHI) provide minimal, secure, and production-ready container images, Helm charts, and system packages maintained by Docker. Designed to reduce vulnerabilities and simplify compliance, DHI integrates easily into your existing Docker-based workflows with little to no retooling required.

DHI is available in the following three subscriptions.

| Feature                                                         | Community | Select    | Enterprise                     |
| --------------------------------------------------------------- | --------- | --------- | ------------------------------ |
| Hardened, minimal images                                        | ✅         | ✅         | ✅                              |
| Near-zero CVEs                                                  | ✅         | ✅         | ✅                              |
| Verifiable SBOMs & SLSA Build L3 provenance                     | ✅         | ✅         | ✅                              |
| Full, unsuppressed CVE visibility                               | ✅         | ✅         | ✅                              |
| Drop-in adoption, no workflow changes                           | ✅         | ✅         | ✅                              |
| Full catalog of open source images under Apache 2.0             | ✅         | ✅         | ✅                              |
| Built with Docker Hardened System Packages                      | ✅         | ✅         | ✅                              |
| Upstream cadence for Docker-released patches                    | ✅         | ✅         | ✅                              |
| FIPS/STIG variants                                              | ❌         | ✅         | ✅                              |
| Critical CVE fixes < 7 days with SLA-backed continuous patching | ❌         | ✅         | ✅                              |
| Customizations                                                  | ❌         | ✅ Up to 5 | ✅ Unlimited                    |
| Access to Hardened System Packages repository                   | ❌         | ❌         | ✅                              |
| Full catalog access available                                   | ❌         | ❌         | ✅                              |
| Extended Lifecycle Support add-on available                     | ❌         | ❌         | ✅ +5 years of hardened updates |

For pricing and more details, see the [Docker Hardened Images subscription comparison](https://www.docker.com/products/hardened-images/#compare).

Explore the sections below to get started with Docker Hardened Images, integrate them into your workflow, and learn what makes them secure and enterprise-ready.

### [Quickstart](/dhi/get-started/)

[Follow a step-by-step guide to explore and run a Docker Hardened Image.](/dhi/get-started/)

### [Explore](/dhi/explore/)

[Learn what Docker Hardened Images are, how they're built, and what sets them apart from typical base images.](/dhi/explore/)

### [Features](/dhi/features/)

[Discover the security, compliance, and enterprise-readiness features built into Docker Hardened Images.](/dhi/features/)

### [How-tos](/dhi/how-to/)

[Step-by-step guides for using, verifying, scanning, and migrating to Docker Hardened Images.](/dhi/how-to/)

### [Core concepts](/dhi/core-concepts/)

[Understand the secure supply chain principles that make Docker Hardened Images production-ready.](/dhi/core-concepts/)

### [Troubleshoot](/dhi/troubleshoot/)

[Resolve common issues with building, running, or debugging Docker Hardened Images.](/dhi/troubleshoot/)

### [Additional resources](/dhi/resources/)

[Guides, Docker Hub catalog, GitHub repositories, and more.](/dhi/resources/)

### [Release notes](/dhi/release-notes/platform/)

[New features, improvements, and changes in Docker Hardened Images.](/dhi/release-notes/platform/)

----
url: https://docs.docker.com/reference/cli/docker/model/tag/
----

# docker model tag

***

| Description | Tag a model                      |
| ----------- | -------------------------------- |
| Usage       | `docker model tag SOURCE TARGET` |

## [Description](#description)

Specify a particular version or variant of the model. If no tag is provided, Docker defaults to `latest`.

----
url: https://docs.docker.com/guides/kafka/
----

[Developing event-driven applications with Kafka and Docker](https://docs.docker.com/guides/kafka/)

This guide explains how to run Apache Kafka in Docker containers.

JavaScript Distributed systems

20 minutes

[« Back to all guides](/guides/)

# Developing event-driven applications with Kafka and Docker

***

Table of contents

***

With the rise of microservices, event-driven architectures have become increasingly popular. [Apache Kafka](https://kafka.apache.org/), a distributed event streaming platform, is often at the heart of these architectures. Unfortunately, setting up and deploying your own Kafka instance for development is often tricky. Fortunately, Docker and containers make this much easier.

In this guide, you will learn how to:

1. Use Docker to launch up a Kafka cluster
2. Connect a non-containerized app to the cluster
3. Connect a containerized app to the cluster
4. Deploy Kafka-UI to help with troubleshooting and debugging

## [Prerequisites](#prerequisites)

The following prerequisites are required to follow along with this how-to guide:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Node.js](https://nodejs.org/en/download/package-manager) and [yarn](https://yarnpkg.com/)
* Basic knowledge of Kafka and Docker

## [Launching Kafka](#launching-kafka)

Beginning with [Kafka 3.3](https://www.confluent.io/blog/apache-kafka-3-3-0-new-features-and-updates/), the deployment of Kafka was greatly simplified by no longer requiring Zookeeper thanks to KRaft (Kafka Raft). With KRaft, setting up a Kafka instance for local development is much easier. Starting with the launch of [Kafka 3.8](https://www.confluent.io/blog/introducing-apache-kafka-3-8/), a new [kafka-native](https://hub.docker.com/r/apache/kafka-native) Docker image is now available, providing a significantly faster startup and lower memory footprint.

> Tip
>
> This guide will be using the apache/kafka image, as it includes many helpful scripts to manage and work with Kafka. However, you may want to use the apache/kafka-native image, as it starts more quickly and requires fewer resources.

### [Starting Kafka](#starting-kafka)

Start a basic Kafka cluster by doing the following steps. This example will launch a cluster, exposing port 9092 onto the host to let a native-running application to connect to it.

1. Start a Kafka container by running the following command:

   ```console
   $ docker run -d --name=kafka -p 9092:9092 apache/kafka
   ```

2. Once the image pulls, you’ll have a Kafka instance up and running within a second or two.

3. The apache/kafka image ships with several helpful scripts in the `/opt/kafka/bin` directory. Run the following command to verify the cluster is up and running and get its cluster ID:

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-cluster.sh cluster-id --bootstrap-server :9092
   ```

   Doing so will produce output similar to the following:

   ```plaintext
   Cluster ID: 5L6g3nShT-eMCtK--X86sw
   ```

4. Create a sample topic and produce (or publish) a few messages by running the following command:

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
   ```

   After running, you can enter a message per line. For example, enter a few messages, one per line. A few examples might be:

   ```plaintext
   First message
   ```

   And

   ```plaintext
   Second message
   ```

   Press `enter` to send the last message and then press ctrl+c when you’re done. The messages will be published to Kafka.

5. Confirm the messages were published into the cluster by consuming the messages:

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server :9092 --topic demo --from-beginning
   ```

   You should then see your messages in the output:

   ```plaintext
   First message
   Second message
   ```

   If you want, you can open another terminal and publish more messages and see them appear in the consumer.

   When you’re done, hit ctrl+c to stop consuming messages.

You have a locally running Kafka cluster and have validated you can connect to it.

## [Connecting to Kafka from a non-containerized app](#connecting-to-kafka-from-a-non-containerized-app)

Now that you’ve shown you can connect to the Kafka instance from a command line, it’s time to connect to the cluster from an application. In this example, you will use a simple Node project that uses the [KafkaJS](https://github.com/tulios/kafkajs) library.

Since the cluster is running locally and is exposed at port 9092, the app can connect to the cluster at localhost:9092 (since it’s running natively and not in a container right now). Once connected, this sample app will log messages it consumes from the `demo` topic. Additionally, when it runs in development mode, it will also create the topic if it isn’t found.

1. If you don’t have the Kafka cluster running from the previous step, run the following command to start a Kafka instance:

   ```console
   $ docker run -d --name=kafka -p 9092:9092 apache/kafka
   ```

2. Clone the [GitHub repository](https://github.com/dockersamples/kafka-development-node) locally.

   ```console
   $ git clone https://github.com/dockersamples/kafka-development-node.git
   ```

3. Navigate into the project.

   ```console
   cd kafka-development-node/app
   ```

4. Install the dependencies using yarn.

   ```console
   $ yarn install
   ```

5. Start the application using `yarn dev`. This will set the `NODE_ENV` environment variable to `development` and use `nodemon` to watch for file changes.

   ```console
   $ yarn dev
   ```

6. With the application now running, it will log received messages to the console. In a new terminal, publish a few messages using the following command:

   ```console
   $ docker exec -ti kafka /opt/kafka/bin/kafka-console-producer.sh --bootstrap-server :9092 --topic demo
   ```

   And then send a message to the cluster:

   ```plaintext
   Test message
   ```

   Remember to press `ctrl+c` when you’re done to stop producing messages.

## [Connecting to Kafka from both containers and native apps](#connecting-to-kafka-from-both-containers-and-native-apps)

Now that you have an application connecting to Kafka through its exposed port, it’s time to explore what changes are needed to connect to Kafka from another container. To do so, you will now run the application out of a container instead of natively.

But before you do that, it’s important to understand how Kafka listeners work and how those listeners help clients connect.

### [Understanding Kafka listeners](#understanding-kafka-listeners)

When a client connects to a Kafka cluster, it actually connects to a “broker”. While brokers have many roles, one of them is to support load balancing of clients. When a client connects, the broker returns a set of connection URLs the client should then use for the client to connect for the producing or consuming of messages. How are these connection URLs configured?

Each Kafka instance has a set of listeners and advertised listeners. The “listeners” are what Kafka binds to and the “advertised listeners” configure how clients should connect to the cluster. The connection URLs a client receives is based on which listener a client connects to.

### [Defining the listeners](#defining-the-listeners)

To help this make sense, let’s look at how Kafka needs to be configured to support two connection opportunities:

1. Host connections (those coming through the host’s mapped port) - these will need to connect using localhost
2. Docker connections (those coming from inside the Docker networks) - these can not connect using localhost, but the network alias (or DNS address) of the Kafka service

Since there are two different methods clients need to connect, two different listeners are required - `HOST` and `DOCKER`. The `HOST` listener will tell clients to connect using localhost:9092, while the `DOCKER` listener will inform clients to connect using `kafka:9093`. Notice this means Kafka is listening on both ports 9092 and 9093. But, only the host listener needs to be exposed to the host.

In order to set this up, the `compose.yaml` for Kafka needs some additional configuration. Once you start overriding some of the defaults, you also need to specify a few other options in order for KRaft mode to work.

```yaml
services:
  kafka:
    image: apache/kafka-native
    ports:
      - "9092:9092"
    environment:
      # Configure listeners for both docker and host communication
      KAFKA_LISTENERS: CONTROLLER://localhost:9091,HOST://0.0.0.0:9092,DOCKER://0.0.0.0:9093
      KAFKA_ADVERTISED_LISTENERS: HOST://localhost:9092,DOCKER://kafka:9093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: CONTROLLER:PLAINTEXT,DOCKER:PLAINTEXT,HOST:PLAINTEXT

      # Settings required for KRaft mode
      KAFKA_NODE_ID: 1
      KAFKA_PROCESS_ROLES: broker,controller
      KAFKA_CONTROLLER_LISTENER_NAMES: CONTROLLER
      KAFKA_CONTROLLER_QUORUM_VOTERS: 1@localhost:9091

      # Listener to use for broker-to-broker communication
      KAFKA_INTER_BROKER_LISTENER_NAME: DOCKER

      # Required for a single node cluster
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
```

Give it a try using the steps below.

1. If you have the Node app running from the previous step, go ahead and stop it by pressing `ctrl+c` in the terminal.

2. If you have the Kafka cluster running from the previous section, go ahead and stop that container using the following command:

   ```console
   $ docker rm -f kafka
   ```

3. Start the Compose stack by running the following command at the root of the cloned project directory:

   ```console
   $ docker compose up
   ```

   After a moment, the application will be up and running.

4. In the stack is another service that can be used to publish messages. Open it by going to <http://localhost:3000>. As you type in a message and submit the form, you should see the log message of the message being received by the app.

   This helps demonstrate how a containerized approach makes it easy to add additional services to help test and troubleshoot your application.

## [Adding cluster visualization](#adding-cluster-visualization)

Once you start using containers in your development environment, you start to realize the ease of adding additional services that are solely focused on helping development, such as visualizers and other supporting services. Since you have Kafka running, it might be helpful to visualize what’s going on in the Kafka cluster. To do so, you can run the [Kafbat UI web application](https://github.com/kafbat/kafka-ui).

To add it to your own project (it’s already in the demo application), you only need to add the following configuration to your Compose file:

```yaml
services:
  kafka-ui:
    image: kafbat/kafka-ui:main
    ports:
      - 8080:8080
    environment:
      DYNAMIC_CONFIG_ENABLED: "true"
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: kafka:9093
    depends_on:
      - kafka
```

Then, once the Compose stack starts, you can open your browser to <http://localhost:8080> and navigate around to view additional details about the cluster, check on consumers, publish test messages, and more.

## [Testing with Kafka](#testing-with-kafka)

If you’re interested in learning how you can integrate Kafka easily into your integration tests, check out the [Testing Spring Boot Kafka Listener using Testcontainers guide](https://testcontainers.com/guides/testing-spring-boot-kafka-listener-using-testcontainers/). This guide will teach you how to use Testcontainers to manage the lifecycle of Kafka containers in your tests.

## [Conclusion](#conclusion)

By using Docker, you can simplify the process of developing and testing event-driven applications with Kafka. Containers simplify the process of setting up and deploying the various services you need to develop. And once they’re defined in Compose, everyone on the team can benefit from the ease of use.

In case you missed it earlier, all of the sample app code can be found at dockersamples/kafka-development-node.

----
url: https://docs.docker.com/reference/cli/docker/plugin/push/
----

# docker plugin push

***

| Description | Push a plugin to a registry                 |
| ----------- | ------------------------------------------- |
| Usage       | `docker plugin push [OPTIONS] PLUGIN[:TAG]` |

## [Description](#description)

After you have created a plugin using `docker plugin create` and the plugin is ready for distribution, use `docker plugin push` to share your images to Docker Hub or a self-hosted registry.

Registry credentials are managed by [docker login](/reference/cli/docker/login/).

## [Examples](#examples)

The following example shows how to push a sample `user/plugin`.

```console
$ docker plugin ls

ID             NAME                    DESCRIPTION                  ENABLED
69553ca1d456   user/plugin:latest      A sample plugin for Docker   false

$ docker plugin push user/plugin
```

----
url: https://docs.docker.com/extensions/extensions-sdk/build/backend-extension-tutorial/
----

# Add a backend to your extension

***

Table of contents

***

Your extension can ship a backend part with which the frontend can interact with. This page provides information on why and how to add a backend.

Before you start, make sure you have installed the latest version of [Docker Desktop](https://www.docker.com/products/docker-desktop/).

> Tip
>
> Check the [Quickstart guide](https://docs.docker.com/extensions/extensions-sdk/quickstart/) and `docker extension init <my-extension>`. They provide a better base for your extension as it's more up-to-date and related to your install of Docker Desktop.

## [Why add a backend?](#why-add-a-backend)

Thanks to the Docker Extensions SDK, most of the time you should be able to do what you need from the Docker CLI directly from [the frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/#use-the-extension-apis-client).

Nonetheless, there are some cases where you might need to add a backend to your extension. So far, extension builders have used the backend to:

* Store data in a local database and serve them back with a REST API.
* Store the extension state, for example when a button starts a long-running process, so that if you navigate away from the extension user interface and comes back, the frontend can pick up where it left off.

For more information about extension backends, see [Architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/#the-backend).

## [Add a backend to the extension](#add-a-backend-to-the-extension)

If you created your extension using the `docker extension init` command, you already have a backend setup. Otherwise, you have to first create a `vm` directory that contains the code and updates the Dockerfile to containerize it.

Here is the extension folder structure with a backend:

```bash
.
├── Dockerfile # (1)
├── Makefile
├── metadata.json
├── ui
    └── index.html
└── vm # (2)
    ├── go.mod
    └── main.go
```

1. Contains everything required to build the backend and copy it in the extension's container filesystem.
2. The source folder that contains the backend code of the extension.

Although you can start from an empty directory or from the `vm-ui extension` [sample](https://github.com/docker/extensions-sdk/tree/main/samples), it is highly recommended that you start from the `docker extension init` command and change it to suit your needs.

> Tip
>
> The `docker extension init` generates a Go backend. But you can still use it as a starting point for your own extension and use any other language like Node.js, Python, Java, .Net, or any other language and framework.

In this tutorial, the backend service simply exposes one route that returns a JSON payload that says "Hello".

```json
{ "Message": "Hello" }
```

> Important
>
> We recommend that, the frontend and the backend communicate through sockets, and named pipes on Windows, instead of HTTP. This prevents port collision with any other running application or container running on the host. Also, some Docker Desktop users are running in constrained environments where they can't open ports on their machines. When choosing the language and framework for your backend, make sure it supports sockets connection.

```go
package main

import (
	"flag"
	"log"
	"net"
	"net/http"
	"os"

	"github.com/labstack/echo"
	"github.com/sirupsen/logrus"
)

func main() {
	var socketPath string
	flag.StringVar(&socketPath, "socket", "/run/guest/volumes-service.sock", "Unix domain socket to listen on")
	flag.Parse()

	os.RemoveAll(socketPath)

	logrus.New().Infof("Starting listening on %s\n", socketPath)
	router := echo.New()
	router.HideBanner = true

	startURL := ""

	ln, err := listen(socketPath)
	if err != nil {
		log.Fatal(err)
	}
	router.Listener = ln

	router.GET("/hello", hello)

	log.Fatal(router.Start(startURL))
}

func listen(path string) (net.Listener, error) {
	return net.Listen("unix", path)
}

func hello(ctx echo.Context) error {
	return ctx.JSON(http.StatusOK, HTTPMessageBody{Message: "hello world"})
}

type HTTPMessageBody struct {
	Message string
}
```

> Important
>
> We don't have a working example for Node yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=Node) and let us know if you'd like a sample for Node.

> Important
>
> We don't have a working example for Python yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=Python) and let us know if you'd like a sample for Python.

> Important
>
> We don't have a working example for Java yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=Java) and let us know if you'd like a sample for Java.

> Important
>
> We don't have a working example for .NET. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=.Net) and let us know if you'd like a sample for .NET.

## [Adapt the Dockerfile](#adapt-the-dockerfile)

> Note
>
> When using the `docker extension init`, it creates a `Dockerfile` that already contains what is needed for a Go backend.

To deploy your Go backend when installing the extension, you need first to configure the `Dockerfile`, so that it:

* Builds the backend application
* Copies the binary in the extension's container filesystem
* Starts the binary when the container starts listening on the extension socket

> Tip
>
> To ease version management, you can reuse the same image to build the frontend, build the backend service, and package the extension.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:17.7-alpine3.14 AS client-builder
# ... build frontend application

# Build the Go backend
FROM golang:1.17-alpine AS builder
ENV CGO_ENABLED=0
WORKDIR /backend
RUN --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache/go-build \
    --mount=type=bind,source=vm/.,target=. \
    go build -trimpath -ldflags="-s -w" -o bin/service

FROM alpine:3.15
# ... add labels and copy the frontend application

COPY --from=builder /backend/bin/service /
CMD /service -socket /run/guest-services/extension-allthethings-extension.sock
```

> Important
>
> We don't have a working Dockerfile for Node yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=Node) and let us know if you'd like a Dockerfile for Node.

> Important
>
> We don't have a working Dockerfile for Python yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=Python) and let us know if you'd like a Dockerfile for Python.

> Important
>
> We don't have a working Dockerfile for Java yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=Java) and let us know if you'd like a Dockerfile for Java.

> Important
>
> We don't have a working Dockerfile for .Net. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.25798127=.Net) and let us know if you'd like a Dockerfile for .Net.

## [Configure the metadata file](#configure-the-metadata-file)

To start the backend service of your extension inside the VM of Docker Desktop, you have to configure the image name in the `vm` section of the `metadata.json` file.

```json
{
  "vm": {
    "image": "${DESKTOP_PLUGIN_IMAGE}"
  },
  "icon": "docker.svg",
  "ui": {
    ...
  }
}
```

For more information on the `vm` section of the `metadata.json`, see [Metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/).

> Warning
>
> Do not replace the `${DESKTOP_PLUGIN_IMAGE}` placeholder in the `metadata.json` file. The placeholder is replaced automatically with the correct image name when the extension is installed.

## [Invoke the extension backend from your frontend](#invoke-the-extension-backend-from-your-frontend)

Using the [advanced frontend extension example](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/), we can invoke our extension backend.

Use the Docker Desktop Client object and then invoke the `/hello` route from the backend service with `ddClient. extension.vm.service.get` that returns the body of the response.

Replace the `ui/src/App.tsx` file with the following code:

```tsx

// ui/src/App.tsx
import React, { useEffect, useState } from 'react';
import { createDockerDesktopClient } from "@docker/extension-api-client";

//obtain docker desktop extension client
const ddClient = createDockerDesktopClient();

export function App() {
  const [hello, setHello] = useState<string>();

  useEffect(() => {
    const getHello = async () => {
      const result = await ddClient.extension.vm?.service?.get('/hello');
      setHello(JSON.stringify(result));
    }
    getHello()
  }, []);

  return (
    <Typography>{hello}</Typography>
  );
}
```

> Important
>
> We don't have an example for Vue yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.1333218187=Vue) and let us know if you'd like a sample with Vue.

> Important
>
> We don't have an example for Angular yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.1333218187=Angular) and let us know if you'd like a sample with Angular.

> Important
>
> We don't have an example for Svelte yet. [Fill out the form](https://docs.google.com/forms/d/e/1FAIpQLSdxJDGFJl5oJ06rG7uqtw1rsSBZpUhv_s9HHtw80cytkh2X-Q/viewform?usp=pp_url\&entry.1333218187=Svelte) and let us know if you'd like a sample with Svelte.

## [Re-build the extension and update it](#re-build-the-extension-and-update-it)

Since you have modified the configuration of the extension and added a stage in the Dockerfile, you must re-build the extension.

```bash
docker build --tag=awesome-inc/my-extension:latest .
```

Once built, you need to update it, or install it if you haven't already done so.

```bash
docker extension update awesome-inc/my-extension:latest
```

Now you can see the backend service running in the **Containers** view of the Docker Desktop Dashboard and watch the logs when you need to debug it.

> Tip
>
> You may need to turn on the **Show system containers** option in **Settings** to see the backend container running. See [Show extension containers](https://docs.docker.com/extensions/extensions-sdk/dev/test-debug/#show-the-extension-containers) for more information.

Open the Docker Desktop Dashboard and select the **Containers** tab. You should see the response from the backend service call displayed.

## [What's next?](#whats-next)

* Learn how to [share and publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).
* Learn more about extensions [architecture](https://docs.docker.com/extensions/extensions-sdk/architecture/).

----
url: https://docs.docker.com/reference/api/extensions-sdk/RequestConfigV0/
----

# Interface: RequestConfigV0

***

Table of contents

***

## [Properties](#properties)

### [url](#url)

• `Readonly` **url**: `string`

***

### [method](#method)

• `Readonly` **method**: `string`

***

### [headers](#headers)

• `Readonly` **headers**: `Record`<`string`, `string`>

***

### [data](#data)

• `Readonly` **data**: `any`

----
url: https://docs.docker.com/build-cloud/release-notes/
----

# Docker Build Cloud release notes

***

Table of contents

***

This page contains information about the new features, improvements, known issues, and bug fixes in Docker Build Cloud releases.

## [2025-02-24](#2025-02-24)

### [New](#new)

Added a new **Build settings** page where you can configure disk allocation, private resource access, and firewall settings for your cloud builders in your organization. These configurations help optimize storage, enable access to private registries, and secure outbound network traffic.

----
url: https://docs.docker.com/reference/api/extensions-sdk/Docker/
----

# Interface: Docker

***

Table of contents

***

**`Since`**

0.2.0

## [Properties](#properties)

### [cli](#cli)

• `Readonly` **cli**: [`DockerCommand`](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/)

You can also directly execute the Docker binary.

```typescript
const output = await ddClient.docker.cli.exec("volume", [
  "ls",
  "--filter",
  "dangling=true"
]);
```

Output:

```json
{
  "stderr": "...",
  "stdout": "..."
}
```

For convenience, the command result object also has methods to easily parse it depending on output format. See [ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/) instead.

***

Streams the output as a result of the execution of a Docker command. It is useful when the output of the command is too long, or you need to get the output as a stream.

```typescript
await ddClient.docker.cli.exec("logs", ["-f", "..."], {
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

## [Methods](#methods)

### [listContainers](#listcontainers)

▸ **listContainers**(`options?`): `Promise`<`unknown`>

Get the list of running containers (same as `docker ps`).

By default, this will not list stopped containers. You can use the option `{"all": true}` to list all the running and stopped containers.

```typescript
const containers = await ddClient.docker.listContainers();
```

#### [Parameters](#parameters)

| Name       | Type  | Description                                                                                                                                                                                                                                                                                                    |
| ---------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `options?` | `any` | (Optional). A JSON like `{ "all": true, "limit": 10, "size": true, "filters": JSON.stringify({ status: ["exited"] }), }` For more information about the different properties see [the Docker API endpoint documentation](https://docs.docker.com/reference/api/engine/version/v1.52/#operation/ContainerList). |

#### [Returns](#returns)

`Promise`<`unknown`>

***

### [listImages](#listimages)

▸ **listImages**(`options?`): `Promise`<`unknown`>

Get the list of local container images

```typescript
const images = await ddClient.docker.listImages();
```

#### [Parameters](#parameters-1)

| Name       | Type  | Description                                                                                                                                                                                                                                                                             |
| ---------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `options?` | `any` | (Optional). A JSON like `{ "all": true, "filters": JSON.stringify({ dangling: ["true"] }), "digests": true * }` For more information about the different properties see [the Docker API endpoint documentation](https://docs.docker.com/reference/api/engine/version/v1.52/#tag/Image). |

#### [Returns](#returns-1)

`Promise`<`unknown`>

----
url: https://docs.docker.com/reference/cli/docker/mcp/catalog/show/
----

# docker mcp catalog show

***

| Description | Show a catalog                                                   |
| ----------- | ---------------------------------------------------------------- |
| Usage       | `docker mcp catalog show <oci-reference> [--pull <pull-option>]` |

## [Description](#description)

Show a catalog

## [Options](#options)

| Option       | Default | Description                                                                                                                     |
| ------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `--format`   | `human` | Supported: json, yaml, human.                                                                                                   |
| `--no-tools` |         | Exclude tools from output (deprecated, use --yq instead)                                                                        |
| `--pull`     | `never` | Supported: missing, never, always, initial, exists, or duration (e.g. '1h', '1d'). Duration represents time since last update.  |
| `--yq`       |         | YQ expression to apply to the output                                                                                            |

----
url: https://docs.docker.com/reference/cli/docker/mcp/profile/server/ls/
----

# docker mcp profile server ls

***

| Description                                                               | List servers across profiles     |
| ------------------------------------------------------------------------- | -------------------------------- |
| Usage                                                                     | `docker mcp profile server ls`   |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker mcp profile server list` |

## [Description](#description)

List all servers grouped by profile.

Use --filter to search for servers matching a query (case-insensitive substring matching on server names). Filters use key=value format (e.g., name=github, profile=my-dev-env).

## [Options](#options)

| Option         | Default | Description                                           |
| -------------- | ------- | ----------------------------------------------------- |
| `-f, --filter` |         | Filter output (e.g., name=github, profile=my-dev-env) |
| `--format`     | `human` | Supported: json, yaml, human.                         |

## [Examples](#examples)

# [List all servers across all profiles](#list-all-servers-across-all-profiles)

docker mcp profile server ls

# [Filter servers by name](#filter-servers-by-name)

docker mcp profile server ls --filter name=github

# [Show servers from a specific profile](#show-servers-from-a-specific-profile)

docker mcp profile server ls --filter profile=my-dev-env

# [Combine multiple filters (using short flag)](#combine-multiple-filters-using-short-flag)

docker mcp profile server ls -f name=slack -f profile=my-dev-env

# [Output in JSON format](#output-in-json-format)

docker mcp profile server ls --format json

----
url: https://docs.docker.com/reference/cli/docker/config/
----

# docker config

***

| Description | Manage Swarm configs |
| ----------- | -------------------- |
| Usage       | `docker config`      |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Manage configs.

## [Subcommands](#subcommands)

| Command                                                                                 | Description                                         |
| --------------------------------------------------------------------------------------- | --------------------------------------------------- |
| [`docker config create`](https://docs.docker.com/reference/cli/docker/config/create/)   | Create a config from a file or STDIN                |
| [`docker config inspect`](https://docs.docker.com/reference/cli/docker/config/inspect/) | Display detailed information on one or more configs |
| [`docker config ls`](https://docs.docker.com/reference/cli/docker/config/ls/)           | List configs                                        |
| [`docker config rm`](https://docs.docker.com/reference/cli/docker/config/rm/)           | Remove one or more configs                          |

----
url: https://docs.docker.com/reference/cli/docker/stack/rm/
----

# docker stack rm

***

| Description                                                               | Remove one or more stacks                    |
| ------------------------------------------------------------------------- | -------------------------------------------- |
| Usage                                                                     | `docker stack rm [OPTIONS] STACK [STACK...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker stack remove` `docker stack down`    |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Remove the stack from the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option         | Default | Description                   |
| -------------- | ------- | ----------------------------- |
| `-d, --detach` | `true`  | Do not wait for stack removal |

## [Examples](#examples)

### [Remove a stack](#remove-a-stack)

This will remove the stack with the name `myapp`. Services, networks, and secrets associated with the stack will be removed.

```console
$ docker stack rm myapp

Removing service myapp_redis
Removing service myapp_web
Removing service myapp_lb
Removing network myapp_default
Removing network myapp_frontend
```

### [Remove multiple stacks](#remove-multiple-stacks)

This will remove all the specified stacks, `myapp` and `vossibility`. Services, networks, and secrets associated with all the specified stacks will be removed.

```console
$ docker stack rm myapp vossibility

Removing service myapp_redis
Removing service myapp_web
Removing service myapp_lb
Removing network myapp_default
Removing network myapp_frontend
Removing service vossibility_nsqd
Removing service vossibility_logstash
Removing service vossibility_elasticsearch
Removing service vossibility_kibana
Removing service vossibility_ghollector
Removing service vossibility_lookupd
Removing network vossibility_default
Removing network vossibility_vossibility
```

----
url: https://docs.docker.com/reference/samples/react/
----

# React samples

| Name                                                                                                     | Description                                                                                                                        |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| [React / Spring / MySQL](https://github.com/docker/awesome-compose/tree/master/react-java-mysql)         | A sample React application with a Spring backend and a MySQL database.                                                             |
| [React / Express / MySQL](https://github.com/docker/awesome-compose/tree/master/react-express-mysql)     | A sample React application with a Node.js backend and a MySQL database.                                                            |
| [React / Express / MongoDB](https://github.com/docker/awesome-compose/tree/master/react-express-mongodb) | A sample React application with a Node.js backend and a Mongo database.                                                            |
| [React / Rust / PostgreSQL](https://github.com/docker/awesome-compose/tree/master/react-rust-postgres)   | A sample React application with a Rust backend and a Postgres database.                                                            |
| [React / NGINX](https://github.com/docker/awesome-compose/tree/master/react-nginx)                       | A sample React application with Nginx.                                                                                             |
| [atsea-sample-shop-app](https://github.com/dockersamples/atsea-sample-shop-app)                          | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| [slack-clone-docker](https://github.com/dockersamples/slack-clone-docker)                                | A sample Slack Clone app built with the MERN stack.                                                                                |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/guides/vuejs/containerize/
----

# Containerize an Vue.js Application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Before you begin, make sure the following tools are installed and available on your system:

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
* You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

> **New to Docker?**\
> Start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide to get familiar with key concepts like images, containers, and Dockerfiles.

***

## [Overview](#overview)

This guide walks you through the complete process of containerizing an Vue.js application with Docker. You’ll learn how to create a production-ready Docker image using best practices that improve performance, security, scalability, and deployment efficiency.

By the end of this guide, you will:

* Containerize an Vue.js application using Docker.
* Create and optimize a Dockerfile for production builds.
* Use multi-stage builds to minimize image size.
* Serve the application efficiently with a custom Nginx configuration.
* Build secure and maintainable Docker images by following best practices.

***

## [Get the sample application](#get-the-sample-application)

Clone the sample application to use with this guide. Open a terminal, navigate to the directory where you want to work, and run the following command to clone the git repository:

```console
$ git clone https://github.com/kristiyan-velkov/docker-vuejs-sample
```

***

## [Build the Docker image](#build-the-docker-image)

Vue.js is a front-end framework that compiles into static assets, so the Dockerfile is customized to align with how Vue.js applications are built and efficiently served in a production environment.

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

### [Step 1: Create the Dockerfile](#step-1-create-the-dockerfile)

Before creating a Dockerfile, you need to choose a base image. You can either use the [Node.js Official Image](https://hub.docker.com/_/node) or a Docker Hardened Image (DHI) from the [Hardened Image catalog](https://hub.docker.com/hardened-images/catalog).

Choosing DHI offers the advantage of a production-ready image that is lightweight and secure. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

> Important
>
> This guide uses a stable Node.js LTS image tag that is considered secure when the guide is written. Because new releases and security patches are published regularly, the tag shown here may no longer be the safest option when you follow the guide. Always review the latest available image tags and select a secure, up-to-date version before building or deploying your application.
>
> Official Node.js Docker Images: <https://hub.docker.com/_/node>

Docker Hardened Images (DHIs) are available for Node.js in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/node). Docker Hardened Images are freely available to everyone with no subscription required. You can pull and use them like any other Docker image after signing in to the DHI registry. For more information, see the [DHI quickstart](/dhi/get-started/) guide.

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

In the following Dockerfile, the `FROM` instructions use `dhi.io/node:24-alpine3.22-dev` and `dhi.io/nginx:1.28.0-alpine3.21-dev` as the base images.

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
# Use a lightweight DHI Node.js image for building
FROM dhi.io/node:24-alpine3.22-dev AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80 
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

Create a file named `Dockerfile` with the following contents:

```dockerfile
# =========================================
# Stage 1: Build the Vue.js Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Vue.js application
RUN npm run build

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80 
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> Note
>
> We are using nginx-unprivileged instead of the standard Nginx image to follow security best practices. Running as a non-root user in the final image:
>
> * Reduces the attack surface
> * Aligns with Docker’s recommendations for container hardening
> * Helps comply with stricter security policies in production environments

### [Step 2: Create the compose.yaml file](#step-2-create-the-composeyaml-file)

Create a file named `compose.yaml` with the following contents:

compose.yaml

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
```

### [Step 3: Create the .dockerignore file](#step-3-create-the-dockerignore-file)

The `.dockerignore` file plays a crucial role in optimizing your Docker image by specifying which files and directories should be excluded from the build context.

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
# -------------------------------
# Dependency directories
# -------------------------------
node_modules/

# -------------------------------
# Production and build outputs
# -------------------------------
dist/
out/
build/
public/build/

# -------------------------------
# Vite, VuePress, and cache dirs
# -------------------------------
.vite/
.vitepress/
.cache/
.tmp/

# -------------------------------
# Test output and coverage
# -------------------------------
coverage/
reports/
jest/
cypress/
cypress/screenshots/
cypress/videos/

# -------------------------------
# Environment and config files
# -------------------------------
*.env*
!.env.production    # Keep production env if needed
*.local
*.log

# -------------------------------
# TypeScript artifacts
# -------------------------------
*.tsbuildinfo

# -------------------------------
# Editor and IDE config
# -------------------------------
.vscode/
.idea/
*.swp

# -------------------------------
# System files
# -------------------------------
.DS_Store
Thumbs.db

# -------------------------------
# Lockfiles (optional)
# -------------------------------
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# -------------------------------
# Git files
# -------------------------------
.git/
.gitignore

# -------------------------------
# Docker-related files
# -------------------------------
Dockerfile
.dockerignore
docker-compose.yml
docker-compose.override.yml
```

### [Step 4: Create the `nginx.conf` file](#step-4-create-the-nginxconf-file)

To serve your Vue.js application efficiently inside the container, you’ll configure Nginx with a custom setup. This configuration is optimized for performance, browser caching, gzip compression, and support for client-side routing.

Create a file named `nginx.conf` in the root of your project directory, and add the following content:

> Note
>
> To learn more about configuring Nginx, see the [official Nginx documentation](https://nginx.org/en/docs/).

```nginx
worker_processes auto;
pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;
    charset       utf-8;

    access_log    off;
    error_log     /dev/stderr warn;

    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    gzip on;
    gzip_comp_level 6;
    gzip_proxied any;
    gzip_min_length 256;
    gzip_vary on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript image/svg+xml;

    server {
        listen       8080;
        server_name  localhost;

        root   /usr/share/nginx/html;
        index  index.html;

        location / {
            try_files $uri $uri/ /index.html;
        }

        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }

        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
            add_header X-Content-Type-Options nosniff;
        }

        error_page 404 /index.html;
    }
}
```

### [Step 5: Build the Vue.js application image](#step-5-build-the-vuejs-application-image)

With your custom configuration in place, you're now ready to build the Docker image for your Vue.js application.

The updated setup includes:

* The updated setup includes a clean, production-ready Nginx configuration tailored specifically for Vue.js.
* Efficient multi-stage Docker build, ensuring a small and secure final image.

After completing the previous steps, your project directory should now contain the following files:

```text
├── docker-vuejs-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

Now that your Dockerfile is configured, you can build the Docker image for your Vue.js application.

> Note
>
> The `docker build` command packages your application into an image using the instructions in the Dockerfile. It includes all necessary files from the current directory (called the [build context](/build/concepts/context/#what-is-a-build-context)).

Run the following command from the root of your project:

```console
$ docker build --tag docker-vuejs-sample .
```

What this command does:

* Uses the Dockerfile in the current directory (.)
* Packages the application and its dependencies into a Docker image
* Tags the image as docker-vuejs-sample so you can reference it later

### [Step 6: View local images](#step-6-view-local-images)

After building your Docker image, you can check which images are available on your local machine using either the Docker CLI or [Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/). Since you're already working in the terminal, let's use the Docker CLI.

To list all locally available Docker images, run the following command:

```console
$ docker images
```

Example Output:

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-vuejs-sample       latest            8c9c199179d4   14 seconds ago   76.2MB
```

This output provides key details about your images:

* **Repository** – The name assigned to the image.
* **Tag** – A version label that helps identify different builds (e.g., latest).
* **Image ID** – A unique identifier for the image.
* **Created** – The timestamp indicating when the image was built.
* **Size** – The total disk space used by the image.

If the build was successful, you should see `docker-vuejs-sample` image listed.

***

## [Run the containerized application](#run-the-containerized-application)

In the previous step, you created a Dockerfile for your Vue.js application and built a Docker image using the docker build command. Now it’s time to run that image in a container and verify that your application works as expected.

Inside the `docker-vuejs-sample` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:8080>. You should see a simple Vue.js web application.

Press `ctrl+c` in the terminal to stop your application.

### [Run the application in the background](#run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option. Inside the `docker-vuejs-sample` directory, run the following command in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at <http://localhost:8080>. You should see your Vue.js application running in the browser.

To confirm that the container is running, use `docker ps` command:

```console
$ docker ps
```

This will list all active containers along with their ports, names, and status. Look for a container exposing port 8080.

Example Output:

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
37a1fa85e4b0   docker-vuejs-sample-server     "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-vuejs-sample-server-1
```

To stop the application, run:

```console
$ docker compose down
```

> Note
>
> For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

***

## [Summary](#summary)

In this guide, you learned how to containerize, build, and run an Vue.js application using Docker. By following best practices, you created a secure, optimized, and production-ready setup.

What you accomplished:

* Created a multi-stage `Dockerfile` that compiles the Vue.js application and serves the static files using Nginx.
* Created a `.dockerignore` file to exclude unnecessary files and keep the image clean and efficient.
* Built your Docker image using `docker build`.
* Ran the container using `docker compose up`, both in the foreground and in detached mode.
* Verified that the app was running by visiting <http://localhost:8080>.
* Learned how to stop the containerized application using `docker compose down`.

You now have a fully containerized Vue.js application, running in a Docker container, and ready for deployment across any environment with confidence and consistency.

***

***

## [Next steps](#next-steps)

With your Vue.js application now containerized, you're ready to move on to the next step.

In the next section, you'll learn how to develop your application using Docker containers, enabling a consistent, isolated, and reproducible development environment across any machine.

[Use containers for Vue.js development »](https://docs.docker.com/guides/vuejs/develop/)

----
url: https://docs.docker.com/reference/cli/docker/dhi/catalog/
----

# docker dhi catalog

***

| Description | Browse the Docker Hardened Images catalog |
| ----------- | ----------------------------------------- |

## [Description](#description)

Commands to browse available Docker Hardened Images and Helm charts

## [Options](#options)

| Option  | Default | Description                                |
| ------- | ------- | ------------------------------------------ |
| `--org` |         | Docker Hub organization (overrides config) |

## [Subcommands](#subcommands)

| Command                                                                                     | Description                            |
| ------------------------------------------------------------------------------------------- | -------------------------------------- |
| [`docker dhi catalog get`](https://docs.docker.com/reference/cli/docker/dhi/catalog/get/)   | Get details of a Docker Hardened Image |
| [`docker dhi catalog list`](https://docs.docker.com/reference/cli/docker/dhi/catalog/list/) | List available Docker Hardened Images  |

----
url: https://docs.docker.com/desktop/setup/install/mac-install/
----

# Install Docker Desktop on Mac

***

Table of contents

***

> **Docker Desktop terms**
>
> Commercial use of Docker Desktop in larger enterprises (more than 250 employees or more than $10 million USD in annual revenue) requires a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopMacInstall).

This page provides download links, system requirements, and step-by-step installation instructions for Docker Desktop on Mac.

[Docker Desktop for Mac with Apple silicon](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-mac-arm64) [Docker Desktop for Mac with Intel chip](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-mac-amd64)

*For checksums, see [Release notes](https://docs.docker.com/desktop/release-notes/).*

## [System requirements](#system-requirements)

* A supported version of macOS.

  > Important
  >
  > Docker Desktop is supported on the current and two previous major macOS releases. As new major versions of macOS are made generally available, Docker stops supporting the oldest version and supports the newest version of macOS (in addition to the previous two releases).

* At least 4 GB of RAM.

* For the best experience, it's recommended that you install Rosetta 2. Rosetta 2 is no longer strictly required, however there are a few optional command line tools that still require Rosetta 2 when using Darwin/AMD64. See [Known issues](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/). To install Rosetta 2 manually from the command line, run the following command:

  ```console
  $ softwareupdate --install-rosetta
  ```

- A supported version of macOS.

  > Important
  >
  > Docker Desktop is supported on the current and two previous major macOS releases. As new major versions of macOS are made generally available, Docker stops supporting the oldest version and supports the newest version of macOS (in addition to the previous two releases).

- At least 4 GB of RAM.

> **Before you install or update**
>
> * Quit tools that might call Docker in the background (Visual Studio Code, terminals, agent apps).
>
> * If you manage fleets or install via MDM, use the [**PKG installer**](https://docs.docker.com/enterprise/enterprise-deployment/pkg-install-and-configure/).
>
> * Keep the installer volume mounted until the installation completes.
>
> If you encounter a "Docker.app is damaged" dialog, see [Fix "Docker.app is damaged" on macOS](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/).

## [Install and run Docker Desktop on Mac](#install-and-run-docker-desktop-on-mac)

> Tip
>
> See the [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/#how-do-I-run-docker-desktop-without-administrator-privileges) on how to install and run Docker Desktop without needing administrator privileges.

### [Install interactively](#install-interactively)

1. Download the installer using the download buttons at the top of the page, or from the [release notes](https://docs.docker.com/desktop/release-notes/).

2. Double-click `Docker.dmg` to open the installer, then drag the Docker icon to the **Applications** folder. By default, Docker Desktop is installed at `/Applications/Docker.app`.

3. Double-click `Docker.app` in the **Applications** folder to start Docker.

4. The Docker menu displays the Docker Subscription Service Agreement.

   Here’s a summary of the key points:

   * Docker Desktop is free for small businesses (fewer than 250 employees AND less than $10 million in annual revenue), personal use, education, and non-commercial open source projects.
   * Otherwise, it requires a paid subscription for professional use.
   * Paid subscriptions are also required for government entities.
   * Docker Pro, Team, and Business subscriptions include commercial use of Docker Desktop.

5. Select **Accept** to continue.

   Note that Docker Desktop won't run if you do not agree to the terms. You can choose to accept the terms at a later date by opening Docker Desktop.

   For more information, see [Docker Desktop Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement). It is recommended that you also read the [FAQs](https://www.docker.com/pricing/faq).

6. From the installation window, select either:

   * **Use recommended settings (Requires password)**. This lets Docker Desktop automatically set the necessary configuration settings.
   * **Use advanced settings**. You can then set the location of the Docker CLI tools either in the system or user directory, enable the default Docker socket, and enable privileged port mapping. See [Settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#advanced), for more information and how to set the location of the Docker CLI tools.

7. Select **Finish**. If you have applied any of the previous configurations that require a password in step 6, enter your password to confirm your choice.

### [Install from the command line](#install-from-the-command-line)

After downloading `Docker.dmg` from either the download buttons at the top of the page or from the [release notes](https://docs.docker.com/desktop/release-notes/), run the following commands in a terminal to install Docker Desktop in the **Applications** folder:

```console
$ sudo hdiutil attach Docker.dmg
$ sudo /Volumes/Docker/Docker.app/Contents/MacOS/install
$ sudo hdiutil detach /Volumes/Docker
```

By default, Docker Desktop is installed at `/Applications/Docker.app`. As macOS typically performs security checks the first time an application is used, the `install` command can take several minutes to run.

#### [Installer flags](#installer-flags)

The `install` command accepts the following flags:

##### [Installation behavior](#installation-behavior)

* `--accept-license`: Accepts the [Docker Subscription Service Agreement](https://www.docker.com/legal/docker-subscription-service-agreement) now, rather than requiring it to be accepted when the application is first run.
* `--user=<username>`: Performs the privileged configurations once during installation. This removes the need for the user to grant root privileges on first run. For more information, see [Privileged helper permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#permission-requirements). To find the username, enter `ls /Users` in the CLI.

##### [Security and access](#security-and-access)

* `--allowed-org=<org name>`: Requires the user to sign in and be part of the specified Docker Hub organization when running the application

* `--user=<username>`: Performs the privileged configurations once during installation. This removes the need for the user to grant root privileges on first run. For more information, see [Privileged helper permission requirements](https://docs.docker.com/desktop/setup/install/mac-permission-requirements/#permission-requirements). To find the username, enter `ls /Users` in the CLI.

* `--admin-settings`: Automatically creates an `admin-settings.json` file which is used by administrators to control certain Docker Desktop settings on client machines within their organization. For more information, see [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/).

  * It must be used together with the `--allowed-org=<org name>` flag.
  * For example: `--allowed-org=<org name> --admin-settings="{'configurationFileVersion': 2, 'enhancedContainerIsolation': {'value': true, 'locked': false}}"`

##### [Proxy configuration](#proxy-configuration)

* `--proxy-http-mode=<mode>`: Sets the HTTP Proxy mode. The two modes are `system` (default) or `manual`.
* `--override-proxy-http=<URL>`: Sets the URL of the HTTP proxy that must be used for outgoing HTTP requests. It requires `--proxy-http-mode` to be `manual`.
* `--override-proxy-https=<URL>`: Sets the URL of the HTTP proxy that must be used for outgoing HTTPS requests, requires `--proxy-http-mode` to be `manual`
* `--override-proxy-exclude=<hosts/domains>`: Bypasses proxy settings for the hosts and domains. It's a comma-separated list.
* `--override-proxy-pac=<PAC file URL>`: Sets the PAC file URL. This setting takes effect only when using `manual` proxy mode.
* `--override-proxy-embedded-pac=<PAC script>`: Specifies an embedded PAC (Proxy Auto-Config) script. This setting takes effect only when using `manual` proxy mode and has precedence over the `--override-proxy-pac` flag.

###### [Example of specifying PAC file](#example-of-specifying-pac-file)

```console
$ sudo /Applications/Docker.app/Contents/MacOS/install --user testuser --proxy-http-mode="manual" --override-proxy-pac="http://localhost:8080/myproxy.pac"
```

###### [Example of specifying PAC script](#example-of-specifying-pac-script)

```console
$ sudo /Applications/Docker.app/Contents/MacOS/install --user testuser --proxy-http-mode="manual" --override-proxy-embedded-pac="function FindProxyForURL(url, host) { return \"DIRECT\"; }"
```

> Tip
>
> As an IT administrator, you can use endpoint management (MDM) software to identify the number of Docker Desktop instances and their versions within your environment. This can provide accurate license reporting, help ensure your machines use the latest version of Docker Desktop, and enable you to [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).
>
> * [Intune](https://learn.microsoft.com/en-us/mem/intune/apps/app-discovered-apps)
> * [Jamf](https://docs.jamf.com/10.25.0/jamf-pro/administrator-guide/Application_Usage.html)
> * [Kandji](https://support.kandji.io/support/solutions/articles/72000559793-view-a-device-application-list)
> * [Kolide](https://www.kolide.com/features/device-inventory/properties/mac-apps)
> * [Workspace One](https://blogs.vmware.com/euc/2022/11/how-to-use-workspace-one-intelligence-to-manage-app-licenses-and-reduce-costs.html)

## [Where to go next](#where-to-go-next)

* Explore [Docker's subscriptions](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopMacInstall) to see what Docker can offer you.
* [Get started with Docker](https://docs.docker.com/get-started/introduction/).
* [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
* [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how to run and submit diagnostics, and submit issues.
* [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
* [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
* [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions on backing up and restoring data related to Docker.

----
url: https://docs.docker.com/engine/containers/multi-service_container/
----

# Run multiple processes in a container

***

Table of contents

***

A container's main running process is the `ENTRYPOINT` and/or `CMD` at the end of the `Dockerfile`. It's best practice to separate areas of concern by using one service per container. That service may fork into multiple processes (for example, Apache web server starts multiple worker processes). It's ok to have multiple processes, but to get the most benefit out of Docker, avoid one container being responsible for multiple aspects of your overall application. You can connect multiple containers using user-defined networks and shared volumes.

The container's main process is responsible for managing all processes that it starts. In some cases, the main process isn't well-designed, and doesn't handle "reaping" (stopping) child processes gracefully when the container exits. If your process falls into this category, you can use the `--init` option when you run the container. The `--init` flag inserts a tiny init-process into the container as the main process, and handles reaping of all processes when the container exits. Handling such processes this way is superior to using a full-fledged init process such as `sysvinit` or `systemd` to handle process lifecycle within your container.

If you need to run more than one service within a container, you can achieve this in a few different ways.

## [Use a wrapper script](#use-a-wrapper-script)

Put all of your commands in a wrapper script, complete with testing and debugging information. Run the wrapper script as your `CMD`. The following is a naive example. First, the wrapper script:

```bash
#!/bin/bash

# Start the first process
./my_first_process &

# Start the second process
./my_second_process &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?
```

Next, the Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_first_process my_first_process
COPY my_second_process my_second_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## [Use Bash job controls](#use-bash-job-controls)

If you have one main process that needs to start first and stay running but you temporarily need to run some other processes (perhaps to interact with the main process) then you can use bash's job control. First, the wrapper script:

```bash
#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
./my_main_process &

# Start the helper process
./my_helper_process

# the my_helper_process might need to know how to wait on the
# primary process to start before it does its work and returns


# now we bring the primary process back into the foreground
# and leave it there
fg %1
```

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
COPY my_main_process my_main_process
COPY my_helper_process my_helper_process
COPY my_wrapper_script.sh my_wrapper_script.sh
CMD ./my_wrapper_script.sh
```

## [Use a process manager](#use-a-process-manager)

Use a process manager like `supervisord`. This is more involved than the other options, as it requires you to bundle `supervisord` and its configuration into your image (or base your image on one that includes `supervisord`), along with the different applications it manages. Then you start `supervisord`, which manages your processes for you.

The following Dockerfile example shows this approach. The example assumes that these files exist at the root of the build context:

* `supervisord.conf`
* `my_first_process`
* `my_second_process`

```dockerfile
# syntax=docker/dockerfile:1
FROM ubuntu:latest
RUN apt-get update && apt-get install -y supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY my_first_process my_first_process
COPY my_second_process my_second_process
CMD ["/usr/bin/supervisord"]
```

If you want to make sure both processes output their `stdout` and `stderr` to the container logs, you can add the following to the `supervisord.conf` file:

```ini
[supervisord]
nodaemon=true
logfile=/dev/null
logfile_maxbytes=0

[program:app]
stdout_logfile=/dev/fd/1
stdout_logfile_maxbytes=0
redirect_stderr=true
```

----
url: https://docs.docker.com/docker-hub/repos/manage/hub-images/push/
----

# Push images to a repository

***

***

To add content to a repository on Docker Hub, you need to tag your Docker image and then push it to your repository. This process lets you share your images with others or use them in different environments.

1. Tag your Docker image.

   The `docker tag` command assigns a tag to your Docker image, which includes your Docker Hub namespace and the repository name. The general syntax is:

   ```console
   $ docker tag [SOURCE_IMAGE[:TAG]] [NAMESPACE/REPOSITORY[:TAG]]
   ```

   Example:

   If your local image is called `my-app` and you want to tag it for the repository `my-namespace/my-repo` with the tag `v1.0`, run:

   ```console
   $ docker tag my-app my-namespace/my-repo:v1.0
   ```

2. Push the image to Docker Hub.

   Use the `docker push` command to upload your tagged image to the specified repository on Docker Hub.

   Example:

   ```console
   $ docker push my-namespace/my-repo:v1.0
   ```

   This command pushes the image tagged `v1.0` to the `my-namespace/my-repo` repository.

3. Verify the image on Docker Hub.

   Sign in to [Docker Hub](https://hub.docker.com) and navigate to your repository (`my-namespace/my-repo` in this example). Select the **Tags** tab to confirm that your tag (`v1.0` in this example) appears in the list.

----
url: https://docs.docker.com/guides/genai-pdf-bot/
----

# PDF analysis and chat

***

Learn how to build a PDF bot for parsing PDF documents and generating responses using Docker and generative AI.

**Time to complete** 20 minutes

The generative AI (GenAI) guide teaches you how to containerize an existing GenAI application using Docker. In this guide, you’ll learn how to:

* Containerize and run a Python-based GenAI application
* Set up a local environment to run the complete GenAI stack locally for development

Start by containerizing an existing GenAI application.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/genai-pdf-bot/containerize/)

   Learn how to containerize a generative AI (GenAI) application.

2. [Develop your app](https://docs.docker.com/guides/genai-pdf-bot/develop/)

   Learn how to develop your generative AI (GenAI) application locally.

----
url: https://docs.docker.com/engine/swarm/stack-deploy/
----

# Deploy a stack to a swarm

***

Table of contents

***

When running Docker Engine in swarm mode, you can use `docker stack deploy` to deploy a complete application stack to the swarm. The `deploy` command accepts a stack description in the form of a [Compose file](https://docs.docker.com/reference/compose-file/legacy-versions/).

> Note
>
> The `docker stack deploy` command uses the legacy [Compose file version 3](/reference/compose-file/legacy-versions/) format, used by Compose V1. The latest format, defined by the [Compose specification](/reference/compose-file/) isn't compatible with the `docker stack deploy` command.
>
> For more information about the evolution of Compose, see [History of Compose](/compose/history/).

To run through this tutorial, you need:

1. A Docker Engine running in [Swarm mode](https://docs.docker.com/engine/swarm/swarm-mode/). If you're not familiar with Swarm mode, you might want to read [Swarm mode key concepts](https://docs.docker.com/engine/swarm/key-concepts/) and [How services work](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/).

   > Note
   >
   > If you're trying things out on a local development environment, you can put your engine into Swarm mode with `docker swarm init`.
   >
   > If you've already got a multi-node swarm running, keep in mind that all `docker stack` and `docker service` commands must be run from a manager node.

2. A current version of [Docker Compose](https://docs.docker.com/compose/install/).

## [Set up a Docker registry](#set-up-a-docker-registry)

Because a swarm consists of multiple Docker Engines, a registry is required to distribute images to all of them. You can use the [Docker Hub](https://hub.docker.com) or maintain your own. Here's how to create a throwaway registry, which you can discard afterward.

1. Start the registry as a service on your swarm:

   ```console
   $ docker service create --name registry --publish published=5000,target=5000 registry:2
   ```

2. Check its status with `docker service ls`:

   ```console
   $ docker service ls

   ID            NAME      REPLICAS  IMAGE                                                                               COMMAND
   l7791tpuwkco  registry  1/1       registry:2@sha256:1152291c7f93a4ea2ddc95e46d142c31e743b6dd70e194af9e6ebe530f782c17
   ```

   Once it reads `1/1` under `REPLICAS`, it's running. If it reads `0/1`, it's probably still pulling the image.

3. Check that it's working with `curl`:

   ```console
   $ curl http://127.0.0.1:5000/v2/

   {}
   ```

## [Create the example application](#create-the-example-application)

The app used in this guide is based on the hit counter app in the [Get started with Docker Compose](https://docs.docker.com/compose/gettingstarted/) guide. It consists of a Python app which maintains a counter in a Redis instance and increments the counter whenever you visit it.

1. Create a directory for the project:

   ```console
   $ mkdir stackdemo
   $ cd stackdemo
   ```

2. Create a file called `app.py` in the project directory and paste this in:

   ```python
   from flask import Flask
   from redis import Redis

   app = Flask(__name__)
   redis = Redis(host='redis', port=6379)

   @app.route('/')
   def hello():
       count = redis.incr('hits')
       return 'Hello World! I have been seen {} times.\n'.format(count)

   if __name__ == "__main__":
       app.run(host="0.0.0.0", port=8000, debug=True)
   ```

3. Create a file called `requirements.txt` and paste these two lines in:

   ```text
   flask
   redis
   ```

4. Create a file called `Dockerfile` and paste this in:

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM python:3.4-alpine
   ADD . /code
   WORKDIR /code
   RUN pip install -r requirements.txt
   CMD ["python", "app.py"]
   ```

5. Create a file called `compose.yaml` and paste this in:

   ```yaml
     services:
       web:
         image: 127.0.0.1:5000/stackdemo
         build: .
         ports:
           - "8000:8000"
       redis:
         image: redis:alpine
   ```

   The image for the web app is built using the Dockerfile defined above. It's also tagged with `127.0.0.1:5000` - the address of the registry created earlier. This is important when distributing the app to the swarm.

## [Test the app with Compose](#test-the-app-with-compose)

1. Start the app with `docker compose up`. This builds the web app image, pulls the Redis image if you don't already have it, and creates two containers.

   You see a warning about the Engine being in swarm mode. This is because Compose doesn't take advantage of swarm mode, and deploys everything to a single node. You can safely ignore this.

   ```console
   $ docker compose up -d

   WARNING: The Docker Engine you're using is running in swarm mode.

   Compose does not use swarm mode to deploy services to multiple nodes in
   a swarm. All containers are scheduled on the current node.

   To deploy your application across the swarm, use `docker stack deploy`.

   Creating network "stackdemo_default" with the default driver
   Building web
   ...(build output)...
   Creating stackdemo_redis_1
   Creating stackdemo_web_1
   ```

2. Check that the app is running with `docker compose ps`:

   ```console
   $ docker compose ps

         Name                     Command               State           Ports
   -----------------------------------------------------------------------------------
   stackdemo_redis_1   docker-entrypoint.sh redis ...   Up      6379/tcp
   stackdemo_web_1     python app.py                    Up      0.0.0.0:8000->8000/tcp
   ```

   You can test the app with `curl`:

   ```console
   $ curl http://localhost:8000
   Hello World! I have been seen 1 times.

   $ curl http://localhost:8000
   Hello World! I have been seen 2 times.

   $ curl http://localhost:8000
   Hello World! I have been seen 3 times.
   ```

3. Bring the app down:

   ```console
   $ docker compose down --volumes

   Stopping stackdemo_web_1 ... done
   Stopping stackdemo_redis_1 ... done
   Removing stackdemo_web_1 ... done
   Removing stackdemo_redis_1 ... done
   Removing network stackdemo_default
   ```

## [Push the generated image to the registry](#push-the-generated-image-to-the-registry)

To distribute the web app's image across the swarm, it needs to be pushed to the registry you set up earlier. With Compose, this is very simple:

```console
$ docker compose push

Pushing web (127.0.0.1:5000/stackdemo:latest)...
The push refers to a repository [127.0.0.1:5000/stackdemo]
5b5a49501a76: Pushed
be44185ce609: Pushed
bd7330a79bcf: Pushed
c9fc143a069a: Pushed
011b303988d2: Pushed
latest: digest: sha256:a81840ebf5ac24b42c1c676cbda3b2cb144580ee347c07e1bc80e35e5ca76507 size: 1372
```

The stack is now ready to be deployed.

## [Deploy the stack to the swarm](#deploy-the-stack-to-the-swarm)

1. Create the stack with `docker stack deploy`:

   ```console
   $ docker stack deploy --compose-file compose.yaml stackdemo

   Ignoring unsupported options: build

   Creating network stackdemo_default
   Creating service stackdemo_web
   Creating service stackdemo_redis
   ```

   The last argument is a name for the stack. Each network, volume and service name is prefixed with the stack name.

2. Check that it's running with `docker stack services stackdemo`:

   ```console
   $ docker stack services stackdemo

   ID            NAME             MODE        REPLICAS  IMAGE
   orvjk2263y1p  stackdemo_redis  replicated  1/1       redis:3.2-alpine@sha256:f1ed3708f538b537eb9c2a7dd50dc90a706f7debd7e1196c9264edeea521a86d
   s1nf0xy8t1un  stackdemo_web    replicated  1/1       127.0.0.1:5000/stackdemo@sha256:adb070e0805d04ba2f92c724298370b7a4eb19860222120d43e0f6351ddbc26f
   ```

   Once it's running, you should see `1/1` under `REPLICAS` for both services. This might take some time if you have a multi-node swarm, as images need to be pulled.

   As before, you can test the app with `curl`:

   ```console
   $ curl http://localhost:8000
   Hello World! I have been seen 1 times.

   $ curl http://localhost:8000
   Hello World! I have been seen 2 times.

   $ curl http://localhost:8000
   Hello World! I have been seen 3 times.
   ```

   With Docker's built-in routing mesh, you can access any node in the swarm on port `8000` and get routed to the app:

   ```console
   $ curl http://address-of-other-node:8000
   Hello World! I have been seen 4 times.
   ```

3. Bring the stack down with `docker stack rm`:

   ```console
   $ docker stack rm stackdemo

   Removing service stackdemo_web
   Removing service stackdemo_redis
   Removing network stackdemo_default
   ```

4. Bring the registry down with `docker service rm`:

   ```console
   $ docker service rm registry
   ```

5. If you're just testing things out on a local machine and want to bring your Docker Engine out of Swarm mode, use `docker swarm leave`:

   ```console
   $ docker swarm leave --force

   Node left the swarm.
   ```

----
url: https://docs.docker.com/reference/cli/docker/service/scale/
----

# docker service scale

***

| Description | Scale one or multiple replicated services                     |
| ----------- | ------------------------------------------------------------- |
| Usage       | `docker service scale SERVICE=REPLICAS [SERVICE=REPLICAS...]` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

The scale command enables you to scale one or more replicated services either up or down to the desired number of replicas. This command cannot be applied on services which are global mode. The command will return immediately, but the actual scaling of the service may take some time. To stop all replicas of a service while keeping the service active in the swarm you can set the scale to 0.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option         | Default | Description                                                               |
| -------------- | ------- | ------------------------------------------------------------------------- |
| `-d, --detach` |         | API 1.29+ Exit immediately instead of waiting for the service to converge |

## [Examples](#examples)

### [Scale a single service](#scale-a-single-service)

The following command scales the "frontend" service to 50 tasks.

```console
$ docker service scale frontend=50

frontend scaled to 50
```

The following command tries to scale a global service to 10 tasks and returns an error.

```console
$ docker service create --mode global --name backend backend:latest

b4g08uwuairexjub6ome6usqh

$ docker service scale backend=10

backend: scale can only be used with replicated or replicated-job mode
```

Directly afterwards, run `docker service ls`, to see the actual number of replicas.

```console
$ docker service ls --filter name=frontend

ID            NAME      MODE        REPLICAS  IMAGE
3pr5mlvu3fh9  frontend  replicated  15/50     nginx:alpine
```

You can also scale a service using the [`docker service update`](/reference/cli/docker/service/update/) command. The following commands are equivalent:

```console
$ docker service scale frontend=50
$ docker service update --replicas=50 frontend
```

### [Scale multiple services](#scale-multiple-services)

The `docker service scale` command allows you to set the desired number of tasks for multiple services at once. The following example scales both the backend and frontend services:

```console
$ docker service scale backend=3 frontend=5

backend scaled to 3
frontend scaled to 5

$ docker service ls

ID            NAME      MODE        REPLICAS  IMAGE
3pr5mlvu3fh9  frontend  replicated  5/5       nginx:alpine
74nzcxxjv6fq  backend   replicated  3/3       redis:7.4.1
```

----
url: https://docs.docker.com/reference/api/engine/version/v1.48.yaml
----

basePath: "/v1.48"
info:
 title: "Docker Engine API"
 version: "1.48"

 If you omit the version-prefix, the current version of the API (v1.48) is used.
 For example, calling \`/info\` is the same as calling \`/v1.48/info\`. Using the

 Warnings:
 description: \|
 List of warnings / informational messages about missing features, or
 issues related to the daemon configuration.

 These messages can be printed by the client as information to the user.
 type: "array"
 items:
 type: "string"
 example:
 \- "WARNING: No memory limit support"
 CDISpecDirs:
 description: \|
 List of directories where (Container Device Interface) CDI
 specifications are located.

 These specifications define vendor-specific modifications to an OCI
 runtime specification for a container being created.

 An empty list indicates that CDI device injection is disabled.

 Note that since using CDI device injection requires the daemon to have
 experimental enabled. For non-experimental daemons an empty list will
 always be returned.
 type: "array"
 items:
 type: "string"
 example:
 \- "/etc/cdi"
 \- "/var/run/cdi"
 Containerd:
 $ref: "#/definitions/ContainerdInfo"

 ContainerdInfo:
 description: \|
 Information for connecting to the containerd instance that is used by the daemon.
 This is included for debugging purposes only.
 type: "object"
 x-nullable: true
 properties:
 Address:
 description: "The address of the containerd socket."
 type: "string"
 example: "/run/containerd/containerd.sock"
 Namespaces:
 description: \|
 The namespaces that the daemon uses for running containers and
 plugins in containerd. These namespaces can be configured in the
 daemon configuration, and are considered to be used exclusively
 by the daemon, Tampering with the containerd instance may cause
 unexpected behavior.

 As these namespaces are considered to be exclusively accessed
 by the daemon, it is not recommended to change these values,
 or to change them to a value that is used by other systems,
 such as cri-containerd.
 type: "object"
 properties:
 Containers:
 description: \|
 The default containerd namespace used for containers managed
 by the daemon.

 The default namespace for containers is "moby", but will be
 suffixed with the \`.\` of the remapped \`root\` if
 user-namespaces are enabled and the containerd image-store
 is used.
 type: "string"
 default: "moby"
 example: "moby"
 Plugins:
 description: \|
 The default containerd namespace used for plugins managed by
 the daemon.

 The default namespace for plugins is "plugins.moby", but will be
 suffixed with the \`.\` of the remapped \`root\` if
 user-namespaces are enabled and the containerd image-store
 is used.
 type: "string"
 default: "plugins.moby"
 example: "plugins.moby"

 # PluginsInfo is a temp struct holding Plugins name
 # registered with docker daemon. It is used by Info struct
 PluginsInfo:
 description: \|
 Available plugins per type.



 \> \*\*Note\*\*: Only unmanaged (V1) plugins are included in this list.
 \> V1 plugins are "lazily" loaded, and are not returned in this list
 \> if there is no resource using the plugin.
 type: "object"
 properties:
 Volume:
 description: "Names of available volume-drivers, and network-driver plugins."
 type: "array"
 items:
 type: "string"
 example: \["local"\]
 Network:
 description: "Names of available network-drivers, and network-driver plugins."
 type: "array"
 items:
 type: "string"
 example: \["bridge", "host", "ipvlan", "macvlan", "null", "overlay"\]
 Authorization:
 description: "Names of available authorization plugins."
 type: "array"
 items:
 type: "string"
 example: \["img-authz-plugin", "hbm"\]
 Log:
 description: "Names of available logging-drivers, and logging-driver plugins."
 type: "array"
 items:
 type: "string"
 example: \["awslogs", "fluentd", "gcplogs", "gelf", "journald", "json-file", "splunk", "syslog"\]

 RegistryServiceConfig:
 description: \|
 RegistryServiceConfig stores daemon registry services configuration.
 type: "object"
 x-nullable: true
 properties:
 AllowNondistributableArtifactsCIDRs:
 description: \|
 List of IP ranges to which nondistributable artifacts can be pushed,
 using the CIDR syntax \[RFC 4632\](https://tools.ietf.org/html/4632).



 \> \*\*Deprecated\*\*: Pushing nondistributable artifacts is now always enabled
 \> and this field is always \`null\`. This field will be removed in a API v1.49.
 type: "array"
 items:
 type: "string"
 example: \[\]
 AllowNondistributableArtifactsHostnames:
 description: \|
 List of registry hostnames to which nondistributable artifacts can be
 pushed, using the format \`\[:\]\` or \`\[:\]\`.



 \> \*\*Deprecated\*\*: Pushing nondistributable artifacts is now always enabled
 \> and this field is always \`null\`. This field will be removed in a API v1.49.
 type: "array"
 items:
 type: "string"
 example: \[\]
 InsecureRegistryCIDRs:
 description: \|
 List of IP ranges of insecure registries, using the CIDR syntax
 (\[RFC 4632\](https://tools.ietf.org/html/4632)). Insecure registries
 accept un-encrypted (HTTP) and/or untrusted (HTTPS with certificates
 from unknown CAs) communication.

 By default, local registries (\`::1/128\` and \`127.0.0.0/8\`) are configured as
 insecure. All other registries are secure. Communicating with an
 insecure registry is not possible if the daemon assumes that registry
 is secure.

 This configuration override this behavior, insecure communication with
 registries whose resolved IP address is within the subnet described by
 the CIDR syntax.

 Registries can also be marked insecure by hostname. Those registries
 are listed under \`IndexConfigs\` and have their \`Secure\` field set to
 \`false\`.

 \> \*\*Warning\*\*: Using this option can be useful when running a local
 \> registry, but introduces security vulnerabilities. This option
 \> should therefore ONLY be used for testing purposes. For increased
 \> security, users should add their CA to their system's list of trusted
 \> CAs instead of enabling this option.
 type: "array"
 items:
 type: "string"
 example: \["::1/128", "127.0.0.0/8"\]
 IndexConfigs:
 type: "object"
 additionalProperties:
 $ref: "#/definitions/IndexInfo"
 example:
 "127.0.0.1:5000":
 "Name": "127.0.0.1:5000"
 "Mirrors": \[\]
 "Secure": false
 "Official": false
 "\[2001:db8:a0b:12f0::1\]:80":
 "Name": "\[2001:db8:a0b:12f0::1\]:80"
 "Mirrors": \[\]
 "Secure": false
 "Official": false
 "docker.io":
 Name: "docker.io"
 Mirrors: \["https://hub-mirror.corp.example.com:5000/"\]
 Secure: true
 Official: true
 "registry.internal.corp.example.com:3000":
 Name: "registry.internal.corp.example.com:3000"
 Mirrors: \[\]
 Secure: false
 Official: false
 Mirrors:
 description: \|
 List of registry URLs that act as a mirror for the official
 (\`docker.io\`) registry.

 type: "array"
 items:
 type: "string"
 example:
 \- "https://hub-mirror.corp.example.com:5000/"
 \- "https://\[2001:db8:a0b:12f0::1\]/"

 IndexInfo:
 description:
 IndexInfo contains information about a registry.
 type: "object"
 x-nullable: true
 properties:
 Name:
 description: \|
 Name of the registry, such as "docker.io".
 type: "string"
 example: "docker.io"
 Mirrors:
 description: \|
 List of mirrors, expressed as URIs.
 type: "array"
 items:
 type: "string"
 example:
 \- "https://hub-mirror.corp.example.com:5000/"
 \- "https://registry-2.docker.io/"
 \- "https://registry-3.docker.io/"
 Secure:
 description: \|
 Indicates if the registry is part of the list of insecure
 registries.

 If \`false\`, the registry is insecure. Insecure registries accept
 un-encrypted (HTTP) and/or untrusted (HTTPS with certificates from
 unknown CAs) communication.

 \> \*\*Warning\*\*: Insecure registries can be useful when running a local
 \> registry. However, because its use creates security vulnerabilities
 \> it should ONLY be enabled for testing purposes. For increased
 \> security, users should add their CA to their system's list of
 \> trusted CAs instead of enabling this option.
 type: "boolean"
 example: true
 Official:
 description: \|
 Indicates whether this is an official registry (i.e., Docker Hub / docker.io)
 type: "boolean"
 example: true

 Runtime:
 description: \|
 Runtime describes an \[OCI compliant\](https://github.com/opencontainers/runtime-spec)
 runtime.

 The runtime is invoked by the daemon via the \`containerd\` daemon. OCI
 runtimes act as an interface to the Linux kernel namespaces, cgroups,
 and SELinux.
 type: "object"
 properties:
 path:
 description: \|
 Name and, optional, path, of the OCI executable binary.

 If the path is omitted, the daemon searches the host's \`$PATH\` for the
 binary and uses the first result.
 type: "string"
 example: "/usr/local/bin/my-oci-runtime"
 runtimeArgs:
 description: \|
 List of command-line arguments to pass to the runtime when invoked.
 type: "array"
 x-nullable: true
 items:
 type: "string"
 example: \["--debug", "--systemd-cgroup=false"\]
 status:
 description: \|
 Information specific to the runtime.

 While this API specification does not define data provided by runtimes,
 the following well-known properties may be provided by runtimes:

 \`org.opencontainers.runtime-spec.features\`: features structure as defined
 in the \[OCI Runtime Specification\](https://github.com/opencontainers/runtime-spec/blob/main/features.md),
 in a JSON string representation.



 \> \*\*Note\*\*: The information returned in this field, including the
 \> formatting of values and labels, should not be considered stable,
 \> and may change without notice.
 type: "object"
 x-nullable: true
 additionalProperties:
 type: "string"
 example:
 "org.opencontainers.runtime-spec.features": "{\\"ociVersionMin\\":\\"1.0.0\\",\\"ociVersionMax\\":\\"1.1.0\\",\\"...\\":\\"...\\"}"

 Commit:
 description: \|
 Commit holds the Git-commit (SHA1) that a binary was built from, as
 reported in the version-string of external tools, such as \`containerd\`,
 or \`runC\`.
 type: "object"
 properties:
 ID:
 description: "Actual commit ID of external tool."
 type: "string"
 example: "cfb82a876ecc11b5ca0977d1733adbe58599088a"
 Expected:
 description: \|
 Commit ID of external tool expected by dockerd as set at build time.

 \*\*Deprecated\*\*: This field is deprecated and will be omitted in a API v1.49.
 type: "string"
 example: "2d41c047c83e09a6d61d464906feb2a2f3c52aa4"

 description: "Include Manifests in the image summary."\
 type: "boolean"\
 default: false\
 required: false\

----
url: https://docs.docker.com/guides/azure-pipelines/
----

[Introduction to Azure Pipelines with Docker](https://docs.docker.com/guides/azure-pipelines/)

Learn how to automate Docker image build and push using Azure Pipelines.

DevOps

10 minutes

[« Back to all guides](/guides/)

# Introduction to Azure Pipelines with Docker

***

Table of contents

***

> This guide is a community contribution. Docker would like to thank [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for his valuable contribution.

## [Prerequisites](#prerequisites)

Before you begin, ensure you have the following requirements:

* A [Docker Hub account](https://hub.docker.com) with a generated access token.
* An active [Azure DevOps project](https://dev.azure.com/) with a connected [Git repository](https://learn.microsoft.com/en-us/azure/devops/repos/git/?view=azure-devops).
* A project that includes a valid [`Dockerfile`](https://docs.docker.com/engine/reference/builder/) at its root or appropriate build context.

## [Overview](#overview)

This guide walks you through building and pushing Docker images using [Azure Pipelines](https://azure.microsoft.com/en-us/products/devops/pipelines), enabling a streamlined and secure CI workflow for containerized applications. You’ll learn how to:

* Configure Docker authentication securely.
* Set up an automated pipeline to build and push images.

## [Set up Azure DevOps to work with Docker Hub](#set-up-azure-devops-to-work-with-docker-hub)

### [Step 1: Configure a Docker Hub service connection](#step-1-configure-a-docker-hub-service-connection)

To securely authenticate with Docker Hub using Azure Pipelines:

1. Navigate to **Project Settings > Service Connections** in your Azure DevOps project.
2. Select **New service connection > Docker Registry**.
3. Choose **Docker Hub** and provide your Docker Hub credentials or access token.
4. Give the service connection a recognizable name, such as `my-docker-registry`.
5. Grant access only to the specific pipeline(s) that require it for improved security and least privilege.

> Important
>
> Avoid selecting the option to grant access to all pipelines unless absolutely necessary. Always apply the principle of least privilege.

### [Step 2: Create your pipeline](#step-2-create-your-pipeline)

Add the following `azure-pipelines.yml` file to the root of your repository:

```yaml
# Trigger pipeline on commits to the main branch
trigger:
  - main

# Trigger pipeline on pull requests targeting the main branch
pr:
  - main

# Define variables for reuse across the pipeline
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'

stages:
  - stage: BuildAndPush
    displayName: Build and Push Docker Image
    jobs:
      - job: DockerJob
        displayName: Build and Push
        pool:
          vmImage: ubuntu-latest
          demands:
            - docker
        steps:
          - checkout: self
            displayName: Checkout Code

          - task: Docker@2
            displayName: Docker Login
            inputs:
              command: login
              containerRegistry: 'my-docker-registry'  # Service connection name

          - task: Docker@2
            displayName: Build Docker Image
            inputs:
              command: build
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)
              dockerfile: './Dockerfile'
              arguments: |
                --sbom=true
                --attest type=provenance
                --cache-from $(imageName):latest
            env:
              DOCKER_BUILDKIT: 1

          - task: Docker@2
            displayName: Push Docker Image
            condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
            inputs:
              command: push
              repository: $(imageName)
              tags: |
                $(buildTag)
                $(latestTag)

          # Optional: logout for self-hosted agents
          - script: docker logout
            displayName: Docker Logout (Self-hosted only)
            condition: ne(variables['Agent.OS'], 'Windows_NT')
```

## [What this pipeline does](#what-this-pipeline-does)

This pipeline automates the Docker image build and deployment process for the main branch. It ensures a secure and efficient workflow with best practices like caching, tagging, and conditional cleanup. Here's what it does:

* Triggers on commits and pull requests targeting the `main` branch.
* Authenticates securely with Docker Hub using an Azure DevOps service connection.
* Builds and tags the Docker image using Docker BuildKit for caching.
* Pushes both buildId and latest tags to Docker Hub.
* Logs out from Docker if running on a self-hosted Linux agent.

## [How the pipeline works](#how-the-pipeline-works)

### [Step 1: Define pipeline triggers](#step-1-define-pipeline-triggers)

```yaml
trigger:
  - main

pr:
  - main
```

This pipeline is triggered automatically on:

* Commits pushed to the `main` branch
* Pull requests targeting `main` main branch

> Tip
>
> Learn more: [Define pipeline triggers in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/build/triggers?view=azure-devops)

### [Step 2: Define common variables](#step-2-define-common-variables)

```yaml
variables:
  imageName: 'docker.io/$(dockerUsername)/my-image'
  buildTag: '$(Build.BuildId)'
  latestTag: 'latest'
```

These variables ensure consistent naming, versioning, and reuse throughout the pipeline steps:

* `imageName`: your image path on Docker Hub
* `buildTag`: a unique tag for each pipeline run
* `latestTag`: a stable alias for your most recent image

> Important
>
> The variable `dockerUsername` is not set automatically.\
> Set it securely in your Azure DevOps pipeline variables:
>
> 1. Go to **Pipelines > Edit > Variables**
> 2. Add `dockerUsername` with your Docker Hub username
>
> Learn more: [Define and use variables in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/variables?view=azure-devops\&tabs=yaml%2Cbatch)

### [Step 3: Define pipeline stages and jobs](#step-3-define-pipeline-stages-and-jobs)

```yaml
stages:
  - stage: BuildAndPush
    displayName: Build and Push Docker Image
```

This stage executes only if the source branch is `main`.

> Tip
>
> Learn more: [Stage conditions in Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/process/stages?view=azure-devops\&tabs=yaml)

### [Step 4: Job configuration](#step-4-job-configuration)

```yaml
jobs:
  - job: DockerJob
  displayName: Build and Push
  pool:
    vmImage: ubuntu-latest
    demands:
      - docker
```

This job utilizes the latest Ubuntu VM image with Docker support, provided by Microsoft-hosted agents. It can be replaced with a custom pool for self-hosted agents if necessary.

> Tip
>
> Learn more: [Specify a pool in your pipeline](https://learn.microsoft.com/en-us/azure/devops/pipelines/agents/pools-queues?view=azure-devops\&tabs=yaml%2Cbrowser)

#### [Step 4.1: Checkout code](#step-41-checkout-code)

```yaml
steps:
  - checkout: self
    displayName: Checkout Code
```

This step pulls your repository code into the build agent, so the pipeline can access the Dockerfile and application files.

> Tip
>
> Learn more: [checkout step documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/yaml-schema/steps-checkout?view=azure-pipelines)

#### [Step 4.2: Authenticate to Docker Hub](#step-42-authenticate-to-docker-hub)

```yaml
- task: Docker@2
  displayName: Docker Login
  inputs:
    command: login
    containerRegistry: 'my-docker-registry'  # Replace with your service connection name
```

Uses a pre-configured Azure DevOps Docker registry service connection to authenticate securely without exposing credentials directly.

> Tip
>
> Learn more: [Use service connections for Docker Hub](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops#docker-hub-or-others)

#### [Step 4.3: Build the Docker image](#step-43-build-the-docker-image)

```yaml
 - task: Docker@2
    displayName: Build Docker Image
    inputs:
      command: build
      repository: $(imageName)
      tags: |
          $(buildTag)
          $(latestTag)
      dockerfile: './Dockerfile'
      arguments: |
          --sbom=true
          --attest type=provenance
          --cache-from $(imageName):latest
    env:
      DOCKER_BUILDKIT: 1
```

This builds the image with:

* Two tags: one with the unique Build ID and one as latest
* Docker BuildKit enabled for faster builds and efficient layer caching
* Cache pull from the most recent pushed latest image
* Software Bill of Materials (SBOM) for supply chain transparency
* Provenance attestation to verify how and where the image was built

> Tip
>
> Learn more:
>
> * [Docker task for Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/reference/docker-v2?view=azure-pipelines\&tabs=yaml)
> * [Docker SBOM Attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/)

#### [Step 4.4: Push the Docker image](#step-44-push-the-docker-image)

```yaml
- task: Docker@2
  displayName: Push Docker Image
  condition: eq(variables['Build.SourceBranch'], 'refs/heads/main')
  inputs:
      command: push
      repository: $(imageName)
      tags: |
        $(buildTag)
        $(latestTag)
```

By applying this condition, the pipeline builds the Docker image on every run to ensure early detection of issues, but only pushes the image to the registry when changes are merged into the main branch—keeping your Docker Hub clean and focused

This uploads both tags to Docker Hub:

* `$(buildTag)` ensures traceability per run.
* `latest` is used for most recent image references.

#### [Step 4.5 Logout of Docker (self-hosted agents)](#step-45--logout-of-docker-self-hosted-agents)

```yaml
- script: docker logout
  displayName: Docker Logout (Self-hosted only)
  condition: ne(variables['Agent.OS'], 'Windows_NT')
```

Executes docker logout at the end of the pipeline on Linux-based self-hosted agents to proactively clean up credentials and enhance security posture.

## [Summary](#summary)

With this Azure Pipelines CI setup, you get:

* Secure Docker authentication using a built-in service connection.
* Automated image building and tagging triggered by code changes.
* Efficient builds leveraging Docker BuildKit cache.
* Safe cleanup with logout on persistent agents.
* Build images that meet modern software supply chain requirements with SBOM and attestation

## [Learn more](#learn-more)

* [Azure Pipelines Documentation](https://learn.microsoft.com/en-us/azure/devops/pipelines/?view=azure-devops): Comprehensive guide to configuring and managing CI/CD pipelines in Azure DevOps.
* [Docker Task for Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/tasks/build/docker): Detailed reference for using the Docker task in Azure Pipelines to build and push images.
* [Docker Buildx Bake](https://docs.docker.com/build/bake/): Explore Docker's advanced build tool for complex, multi-stage, and multi-platform build setups. See also the [Mastering Buildx Bake Guide](https://docs.docker.com/guides/bake/) for practical examples and best practices.
* [Docker Build Cloud](https://docs.docker.com/guides/docker-build-cloud/): Learn about Docker's managed build service for faster, scalable, and multi-platform image builds in the cloud.

----
url: https://docs.docker.com/compose/intro/history/
----

# History and development of Docker Compose

***

Table of contents

***

This page provides:

* A brief history of the development of the Docker Compose CLI
* A clear explanation of the major versions and file formats that make up Compose v1, v2, and v5
* The main differences between Compose v1, v2, and v5

## [Introduction](#introduction)

The diagram above highlights the key differences between Docker Compose v1, v2, and v5. Today, the supported Docker Compose CLI versions are Compose v2 and Compose v5, both of which are defined by the [Compose Specification](https://docs.docker.com/reference/compose-file/).

The diagram provides a high-level comparison of file formats, command-line syntax, and supported top-level elements. This is covered in more detail in the following sections.

### [Docker Compose CLI versioning](#docker-compose-cli-versioning)

Compose v1 was first released in 2014. It was written in Python and invoked with `docker-compose`. Typically, Compose v1 projects include a top-level `version` element in the `compose.yaml` file, with values ranging from `2.0` to `3.8`, which refer to the specific [file formats](#compose-file-format-versioning).

Compose v2, announced in 2020, is written in Go and is invoked with `docker compose`. Unlike v1, Compose v2 ignores the `version` top-level element in the `compose.yaml` file and relies entirely on the Compose Specification to interpret the file.

Compose v5, released in 2025, is functionally identical to Compose v2. Its primary distinction is the introduction of an official [Go SDK](https://docs.docker.com/compose/compose-sdk/). This SDK provides a comprehensive API that lets you integrate Compose functionality directly into your applications, allowing you to load, validate, and manage multi-container environments without relying on the Compose CLI. To avoid confusion with the legacy Compose file formats labeled “v2” and “v3,” the versioning was advanced directly to v5.

### [Compose file format versioning](#compose-file-format-versioning)

The Docker Compose CLIs are defined by specific file formats.

Three major versions of the Compose file format for Compose v1 were released:

* Compose file format 1 with Compose 1.0.0 in 2014
* Compose file format 2.x with Compose 1.6.0 in 2016
* Compose file format 3.x with Compose 1.10.0 in 2017

Compose file format 1 is substantially different to all the following formats as it lacks a top-level `services` key. Its usage is historical and files written in this format don't run with Compose v2 or v5.

Compose file format 2.x and 3.x are very similar to each other, but the latter introduced many new options targeted at Swarm deployments.

To address confusion around Compose CLI versioning, Compose file format versioning, and feature parity depending on whether Swarm mode was in use, file format 2.x and 3.x were merged into the [Compose Specification](https://docs.docker.com/reference/compose-file/).

Compose v2 and v5 uses the Compose Specification for project definition. Unlike the prior file formats, the Compose Specification is rolling and makes the `version` top-level element optional. Compose v2 and v5 also makes use of optional specifications - [Deploy](https://docs.docker.com/reference/compose-file/deploy/), [Develop](https://docs.docker.com/reference/compose-file/develop/), and [Build](https://docs.docker.com/reference/compose-file/build/).

To make migration easier, Compose v2 and v5 has backwards compatibility for certain elements that have been deprecated or changed between Compose file format 2.x/3.x and the Compose Specification.

## [What's next?](#whats-next)

* [How Compose works](https://docs.docker.com/compose/intro/compose-application-model/)
* [Compose Specification reference](https://docs.docker.com/reference/compose-file/)

----
url: https://docs.docker.com/admin/organization/manage/manage-licenses/
----

# Manage license assignment

***

Table of contents

***

Licenses let you selectively choose which of your organization members have access to supported Docker products. Organization owners can oversee who on their team has active licenses, or configure licenses to assign automatically when members access supported Docker products. Like Docker Core seats, licenses can be configured on a per member basis.

> Tip
>
> To learn more about product licenses, Docker Core seats, and other Docker add-ons see [scale your subscription](https://docs.docker.com/subscription/scale/), or [contact sales](https://www.docker.com/pricing/contact-sales/) to purchase licenses.

## [Manage licenses](#manage-licenses)

The **Members** page lets you track the number of available licenses for your organization and who currently holds a license. You can also assign or revoke licenses from this page.

To manage licenses for your organization:

1. Sign in to [Docker Home](https://app.docker.com), then choose your organization.
2. Select **Members** from the left navigation.
3. Select the action menu at the end of the row to assign or revoke an active license.
4. Optional. To bulk assign or revoke licenses, choose the members you want to bulk manage, then select the **Bulk actions** menu.
5. Optional. To manage automatic license assignment, turn off or turn on with the **Automatically assign licenses** toggle.

You must assign licenses manually, or configure automatic license assignment to consume a license. Inviting a new member to your organization consumes a seat or license if you select a product in **Licenses (optional)** during the [invite flow](https://docs.docker.com/admin/organization/manage/members/), but won't auto-assign product licenses by default. Conversely, purchasing a set of licenses won't trigger automatic assignment to existing members.

## [Automatic license assignment](#automatic-license-assignment)

Automatic license assignment gives members a product license when they use a supported product for the first time. Automatic license assignment is available for AI Governance licenses. Only organizations that purchase AI Governance can set up auto-assignment for Docker Core as well.

* When you purchase AI Governance, signing into [Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) with `login` command in `sbx` CLI (`sbx login`) automatically provisions AI Governance licenses on a first-come, first served basis.

* Similarly, logins to Docker Desktop will automatically provision Docker Core for AI Governance license-holding organizations that have available Docker Core seats.

* Licenses are assigned until exhausted.

  * Once the available licenses are exhausted, automatic license assignment will stop until you purchase more licenses or revoke assigned licenses.
  * Members can still use Docker Sandbox or Docker Desktop, but organization policies for those products won't affect their usage.

AI Governance licenses include single sign-on (SSO) and provisioning features regardless of your Docker Core subscription. Automatic license assignment requires [setting up SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/), then [provisioning](https://docs.docker.com/enterprise/security/provisioning/) with System for Cross-domain Identity Management (SCIM) or Just-in-Time (JIT).

## [What's next](#whats-next)

See these docs to explore Docker Core add-ons, or products that need licenses:

* [Scale your subscription](https://docs.docker.com/subscription/scale/) to learn about different add-ons
* [Manage seats](https://docs.docker.com/admin/organization/manage/manage-seats/) to add more seats to your Docker Core subscription
* [AI Governance](https://docs.docker.com/ai/sandboxes/governance/org/) to set up organization policies for your organization members
* [Docker Offload](https://docs.docker.com/offload/about/) to let your developers offload building and running containers to the cloud

----
url: https://docs.docker.com/reference/api/extensions-sdk/SpawnOptions/
----

# Interface: SpawnOptions

***

Table of contents

***

**`Since`**

0.3.0

## [Hierarchy](#hierarchy)

* [`ExecOptions`](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/)

  ↳ **`SpawnOptions`**

## [Properties](#properties)

### [cwd](#cwd)

• `Optional` **cwd**: `string`

#### [Inherited from](#inherited-from)

[ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/).[cwd](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/#cwd)

***

### [env](#env)

• `Optional` **env**: `ProcessEnv`

#### [Inherited from](#inherited-from-1)

[ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/).[env](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/#env)

***

### [stream](#stream)

• **stream**: [`ExecStreamOptions`](https://docs.docker.com/reference/api/extensions-sdk/ExecStreamOptions/)

----
url: https://docs.docker.com/dhi/migration/migrate-from-doi/
----

# Migrate from Alpine or Debian

***

Table of contents

***

Docker Hardened Images (DHI) come in both [Alpine-based and Debian-based variants](https://docs.docker.com/dhi/explore/available/). In many cases, migrating from another image based on these distributions is as simple as changing the base image in your Dockerfile.

This guide helps you migrate from an existing Alpine-based or Debian-based Docker Official Image (DOI) to DHI.

If you're currently using a Debian-based Docker Official Image, migrate to the Debian-based DHI variant. If you're using an Alpine-based image, migrate to the Alpine-based DHI variant. This minimizes changes to package management and dependencies during migration.

## [Key differences](#key-differences)

When migrating from non-hardened images to DHI, be aware of these key differences:

| Item               | Non-hardened images                                            | Docker Hardened Images                                                                                                                                                                                                                                 |
| ------------------ | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Package management | Package managers generally available in all images.            | Package managers generally only available in images with a `dev` tag. Runtime images don't contain package managers. Use multi-stage builds and copy necessary artifacts from the build stage to the runtime stage.                                    |
| Non-root user      | Usually runs as root by default                                | Runtime variants run as the nonroot user by default. Ensure that necessary files and directories are accessible to the nonroot user.                                                                                                                   |
| Multi-stage build  | Optional                                                       | Recommended. Use images with a `dev` or `sdk` tags for build stages and non-dev images for runtime.                                                                                                                                                    |
| TLS certificates   | May need to be installed                                       | Contain standard TLS certificates by default. There is no need to install TLS certificates.                                                                                                                                                            |
| Ports              | Can bind to privileged ports (below 1024) when running as root | Run as a nonroot user by default. Applications can't bind to privileged ports (below 1024) when running in Kubernetes or in Docker Engine versions older than 20.10. Configure your application to listen on port 1025 or higher inside the container. |
| Entry point        | Varies by image                                                | May have different entry points than Docker Official Images. Inspect entry points and update your Dockerfile if necessary.                                                                                                                             |
| Shell              | Shell generally available in all images                        | Runtime images don't contain a shell. Use `dev` images in build stages to run shell commands and then copy artifacts to the runtime stage.                                                                                                             |

## [Migration steps](#migration-steps)

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
- FROM golang:1.25

+ ## Updated to use hardened base image
+ FROM dhi.io/golang:1.25-debian12-dev
```

Note that DHI does not have a `latest` tag in order to promote best practices around image versioning. Ensure that you specify the appropriate version tag for your image. To find the right tag, explore the available tags in the [DHI Catalog](https://hub.docker.com/hardened-images/catalog/). In addition, the distribution base is specified in the tag (for example, `-alpine3.22` or `-debian12`), so be sure to select the correct variant for your application.

### [Step 2: Update the runtime image in your Dockerfile](#step-2-update-the-runtime-image-in-your-dockerfile)

> Note
>
> Multi-stage builds are recommended to keep your final image minimal and secure. Single-stage builds are supported, but they include the full `dev` image and therefore result in a larger image with a broader attack surface.

To ensure that your final image is as minimal as possible, you should use a [multi-stage build](https://docs.docker.com/build/building/multi-stage/). All stages in your Dockerfile should use a hardened image. While intermediary stages will typically use images tagged as `dev` or `sdk`, your final runtime stage should use a runtime image.

Utilize the build stage to compile your application and copy the resulting artifacts to the final runtime stage. This ensures that your final image is minimal and secure.

The following example shows a multi-stage Dockerfile with a build stage and runtime stage:

```dockerfile
# Build stage
FROM dhi.io/golang:1.25-debian12-dev AS builder
WORKDIR /app
COPY . .
RUN go build -o myapp

# Runtime stage
FROM dhi.io/golang:1.25-debian12
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
url: https://docs.docker.com/extensions/extensions-sdk/dev/usage/
----

# CLI reference

***

***

The Extensions CLI is an extension development tool that is used to manage Docker extensions. Actions include install, list, remove, and validate extensions.

* `docker extension enable` turns on Docker extensions.
* `docker extension dev` commands for extension development.
* `docker extension disable` turns off Docker extensions.
* `docker extension init` creates a new Docker extension.
* `docker extension install` installs a Docker extension with the specified image.
* `docker extension ls` list installed Docker extensions.
* `docker extension rm` removes a Docker extension.
* `docker extension update` removes and re-installs a Docker extension.
* `docker extension validate` validates the extension metadata file against the JSON schema.

----
url: https://docs.docker.com/desktop/features/usbip/
----

# Using USB/IP with Docker Desktop

***

Table of contents

***

For: Docker Desktop for Mac, Linux, and Windows with the Hyper-V backend

USB/IP enables you to share USB devices over the network, which can then be accessed from within Docker containers. This page focuses on sharing USB devices connected to the machine you run Docker Desktop on. You can repeat the following process to attach and use additional USB devices as needed.

> Note
>
> Docker Desktop includes built-in drivers for many common USB devices but Docker can't guarantee every possible USB device works with this setup.

## [Setup and use](#setup-and-use)

### [Step one: Run a USB/IP server](#step-one-run-a-usbip-server)

To use USB/IP, you need to run a USB/IP server. For this guide, the implementation provided by [jiegec/usbip](https://github.com/jiegec/usbip) will be used.

1. Clone the repository.

   ```console
   $ git clone https://github.com/jiegec/usbip
   $ cd usbip
   ```

2. Run the emulated Human Interface Device (HID) device example.

   ```console
   $ env RUST_LOG=info cargo run --example hid_keyboard
   ```

### [Step two: Start a privileged Docker container](#step-two-start-a-privileged-docker-container)

To attach the USB device, start a privileged Docker container with the PID namespace set to `host`:

```console
$ docker run --rm -it --privileged --pid=host alpine
```

`--privileged` gives the container full access to the host, and `--pid=host` allows it to share the host’s process namespace.

### [Step three: Enter the mount namespace of PID 1](#step-three-enter-the-mount-namespace-of-pid-1)

Inside the container, enter the mount namespace of the `init` process to gain access to the pre-installed USB/IP tools:

```console
$ nsenter -t 1 -m
```

### [Step four: Use the USB/IP tools](#step-four-use-the-usbip-tools)

Now you can use the USB/IP tools as you would on any other system:

#### [List USB devices](#list-usb-devices)

To list exportable USB devices from the host:

```console
$ usbip list -r host.docker.internal
```

Expected output:

```console
Exportable USB devices
======================
 - host.docker.internal
      0-0-0: unknown vendor : unknown product (0000:0000)
           : /sys/bus/0/0/0
           : (Defined at Interface level) (00/00/00)
           :  0 - unknown class / unknown subclass / unknown protocol (03/00/00)
```

#### [Attach a USB device](#attach-a-usb-device)

To attach a specific USB device, or the emulated keyboard in this case:

```console
$ usbip attach -r host.docker.internal -d 0-0-0
```

#### [Verify device attachment](#verify-device-attachment)

After attaching the emulated keyboard, check the `/dev/input` directory for the device node:

```console
$ ls /dev/input/
```

Example output:

```console
event0  mice
```

### [Step five: Access the device from another container](#step-five-access-the-device-from-another-container)

While the initial container remains running to keep the USB device operational, you can access the attached device from another container. For example:

1. Start a new container with the attached device.

   ```console
   $ docker run --rm -it --device "/dev/input/event0" alpine
   ```

2. Install a tool like `evtest` to test the emulated keyboard.

   ```console
   $ apk add evtest
   $ evtest /dev/input/event0
   ```

3. Interact with the device, and observe the output.

   Example output:

   ```console
   Input driver version is 1.0.1
   Input device ID: bus 0x3 vendor 0x0 product 0x0 version 0x111
   ...
   Properties:
   Testing ... (interrupt to exit)
   Event: time 1717575532.881540, type 4 (EV_MSC), code 4 (MSC_SCAN), value 7001e
   Event: time 1717575532.881540, type 1 (EV_KEY), code 2 (KEY_1), value 1
   Event: time 1717575532.881540, -------------- SYN_REPORT ------------
   ...
   ```

> Important
>
> The initial container must remain running to maintain the connection to the USB device. Exiting the container will stop the device from working.

----
url: https://docs.docker.com/engine/release-notes/18.03/
----

# Docker Engine 18.03 release notes

***

Table of contents

***

## [18.03.1-ce](#18031-ce)

2018-04-26

### [Client](#client)

* Fix error with merge compose file with networks [docker/cli#983](https://github.com/docker/cli/pull/983)

- Fix docker stack deploy re-deploying services after the service was updated with `--force` [docker/cli#963](https://github.com/docker/cli/pull/963)
- Fix docker version output alignment [docker/cli#965](https://github.com/docker/cli/pull/965)

### [Runtime](#runtime)

* Fix AppArmor profiles not being applied to `docker exec` processes [moby/moby#36466](https://github.com/moby/moby/pull/36466)
* Don't sort plugin mount slice [moby/moby#36711](https://github.com/moby/moby/pull/36711)
* Daemon/cluster: handle partial attachment entries during configure [moby/moby#36769](https://github.com/moby/moby/pull/36769)

- Bump Golang to 1.9.5 [moby/moby#36779](https://github.com/moby/moby/pull/36779) [docker/cli#986](https://github.com/docker/cli/pull/986)

* Daemon/stats: more resilient cpu sampling [moby/moby#36519](https://github.com/moby/moby/pull/36519)

- Containerd: update to 1.0.3 release [moby/moby#36749](https://github.com/moby/moby/pull/36749)

* Fix Windows layer leak when write fails [moby/moby#36728](https://github.com/moby/moby/pull/36728)

- Don't make container mount unbindable [moby/moby#36768](https://github.com/moby/moby/pull/36768)

* Fix Daemon panics on container export after a daemon restart [moby/moby/36586](https://github.com/moby/moby/pull/36586)
* Fix digest cache being removed on autherrors [moby/moby#36509](https://github.com/moby/moby/pull/36509)
* Make sure plugin container is removed on failure [moby/moby#36715](https://github.com/moby/moby/pull/36715)
* Copy: avoid using all system memory with authz plugins [moby/moby#36595](https://github.com/moby/moby/pull/36595)
* Relax some libcontainerd client locking [moby/moby#36848](https://github.com/moby/moby/pull/36848)
* Update `hcsshim` to v0.6.10 to address [CVE-2018-8115](https://portal.msrc.microsoft.com/en-us/security-guidance/advisory/CVE-2018-8115)

### [Swarm Mode](#swarm-mode)

* Increase raft Election tick to 10 times Heartbeat tick [moby/moby#36672](https://github.com/moby/moby/pull/36672)

### [Networking](#networking)

* Gracefully remove LB endpoints from services [docker/libnetwork#2112](https://github.com/docker/libnetwork/pull/2112)
* Retry other external DNS servers on ServFail [docker/libnetwork#2121](https://github.com/docker/libnetwork/pull/2121)
* Improve scalability of bridge network isolation rules [docker/libnetwork#2117](https://github.com/docker/libnetwork/pull/2117)
* Allow for larger preset property values, do not override [docker/libnetwork#2124](https://github.com/docker/libnetwork/pull/2124)
* Prevent panics on concurrent reads/writes when calling `changeNodeState` [docker/libnetwork#2136](https://github.com/docker/libnetwork/pull/2136)

## [18.03.0-ce](#18030-ce)

2018-03-21

### [Builder](#builder)

* Switch to -buildmode=pie [moby/moby#34369](https://github.com/moby/moby/pull/34369)
* Allow Dockerfile to be outside of build-context [docker/cli#886](https://github.com/docker/cli/pull/886)
* Builder: fix wrong cache hits building from tars [moby/moby#36329](https://github.com/moby/moby/pull/36329)

- Fixes files leaking to other images in a multi-stage build [moby/moby#36338](https://github.com/moby/moby/pull/36338)

### [Client](#client-1)

* Simplify the marshaling of compose types.Config [docker/cli#895](https://github.com/docker/cli/pull/895)

- Add support for multiple composefile when deploying [docker/cli#569](https://github.com/docker/cli/pull/569)

* Fix broken Kubernetes stack flags [docker/cli#831](https://github.com/docker/cli/pull/831)
* Fix stack marshaling for Kubernetes [docker/cli#890](https://github.com/docker/cli/pull/890)
* Fix and simplify bash completion for service env, mounts and labels [docker/cli#682](https://github.com/docker/cli/pull/682)
* Fix `before` and `since` filter for `docker ps` [moby/moby#35938](https://github.com/moby/moby/pull/35938)
* Fix `--label-file` weird behavior [docker/cli#838](https://github.com/docker/cli/pull/838)
* Fix compilation of defaultCredentialStore() on unsupported platforms [docker/cli#872](https://github.com/docker/cli/pull/872)

- Improve and fix bash completion for images [docker/cli#717](https://github.com/docker/cli/pull/717)

* Added check for empty source in bind mount [docker/cli#824](https://github.com/docker/cli/pull/824)

- Fix TLS from environment variables in client [moby/moby#36270](https://github.com/moby/moby/pull/36270)

* docker build now runs faster when registry-specific credential helper(s) are configured [docker/cli#840](https://github.com/docker/cli/pull/840)
* Update event filter zsh completion with `disable`, `enable`, `install` and `remove` [docker/cli#372](https://github.com/docker/cli/pull/372)
* Produce errors when empty ids are passed into inspect calls [moby/moby#36144](https://github.com/moby/moby/pull/36144)
* Marshall version for the k8s controller [docker/cli#891](https://github.com/docker/cli/pull/891)
* Set a non-zero timeout for HTTP client communication with plugin backend [docker/cli#883](https://github.com/docker/cli/pull/883)

- Add DOCKER\_TLS environment variable for --tls option [docker/cli#863](https://github.com/docker/cli/pull/863)
- Add --template-driver option for secrets/configs [docker/cli#896](https://github.com/docker/cli/pull/896)
- Move `docker trust` commands out of experimental [docker/cli#934](https://github.com/docker/cli/pull/934) [docker/cli#935](https://github.com/docker/cli/pull/935) [docker/cli#944](https://github.com/docker/cli/pull/944)

### [Logging](#logging)

* AWS logs - don't add new lines to maximum sized events [moby/moby#36078](https://github.com/moby/moby/pull/36078)
* Move log validator logic after plugins are loaded [moby/moby#36306](https://github.com/moby/moby/pull/36306)
* Support a proxy in Splunk log driver [moby/moby#36220](https://github.com/moby/moby/pull/36220)

- Fix log tail with empty logs [moby/moby#36305](https://github.com/moby/moby/pull/36305)

### [Networking](#networking-1)

* Libnetwork revendoring [moby/moby#36137](https://github.com/moby/moby/pull/36137)

- Fix for deadlock on exit with Memberlist revendor [docker/libnetwork#2040](https://github.com/docker/libnetwork/pull/2040)

* Fix user specified ndots option [docker/libnetwork#2065](https://github.com/docker/libnetwork/pull/2065)

- Fix to use ContainerID for Windows instead of SandboxID [docker/libnetwork#2010](https://github.com/docker/libnetwork/pull/2010)

* Verify NetworkingConfig to make sure EndpointSettings is not nil [moby/moby#36077](https://github.com/moby/moby/pull/36077)

- Fix `DockerNetworkInternalMode` issue [moby/moby#36298](https://github.com/moby/moby/pull/36298)
- Fix race in attachable network attachment [moby/moby#36191](https://github.com/moby/moby/pull/36191)
- Fix timeout issue of `InspectNetwork` on AArch64 [moby/moby#36257](https://github.com/moby/moby/pull/36257)

* Verbose info is missing for partial overlay ID [moby/moby#35989](https://github.com/moby/moby/pull/35989)
* Update `FindNetwork` to address network name duplications [moby/moby#30897](https://github.com/moby/moby/pull/30897)
* Disallow attaching ingress network [docker/swarmkit#2523](https://github.com/docker/swarmkit/pull/2523)

- Prevent implicit removal of the ingress network [moby/moby#36538](https://github.com/moby/moby/pull/36538)
- Fix stale HNS endpoints on Windows [moby/moby#36603](https://github.com/moby/moby/pull/36603)
- IPAM fixes for duplicate IP addresses [docker/libnetwork#2104](https://github.com/docker/libnetwork/pull/2104) [docker/libnetwork#2105](https://github.com/docker/libnetwork/pull/2105)

### [Runtime](#runtime-1)

* Enable HotAdd for Windows [moby/moby#35414](https://github.com/moby/moby/pull/35414)
* LCOW: Graphdriver fix deadlock in hotRemoveVHDs [moby/moby#36114](https://github.com/moby/moby/pull/36114)
* LCOW: Regular mount if only one layer [moby/moby#36052](https://github.com/moby/moby/pull/36052)
* Remove interim env var LCOW\_API\_PLATFORM\_IF\_OMITTED [moby/moby#36269](https://github.com/moby/moby/pull/36269)
* Revendor Microsoft/opengcs @ v0.3.6 [moby/moby#36108](https://github.com/moby/moby/pull/36108)

- Fix issue of ExitCode and PID not show up in Task.Status.ContainerStatus [moby/moby#36150](https://github.com/moby/moby/pull/36150)
- Fix issue with plugin scanner going too deep [moby/moby#36119](https://github.com/moby/moby/pull/36119)

* Do not make graphdriver homes private mounts [moby/moby#36047](https://github.com/moby/moby/pull/36047)
* Do not recursive unmount on cleanup of zfs/btrfs [moby/moby#36237](https://github.com/moby/moby/pull/36237)
* Don't restore image if layer does not exist [moby/moby#36304](https://github.com/moby/moby/pull/36304)
* Adjust minimum API version for templated configs/secrets [moby/moby#36366](https://github.com/moby/moby/pull/36366)
* Bump containerd to 1.0.2 (cfd04396dc68220d1cecbe686a6cc3aa5ce3667c) [moby/moby#36308](https://github.com/moby/moby/pull/36308)
* Bump Golang to 1.9.4 [moby/moby#36243](https://github.com/moby/moby/pull/36243)
* Ensure daemon root is unmounted on shutdown [moby/moby#36107](https://github.com/moby/moby/pull/36107)
* Update runc to 6c55f98695e902427906eed2c799e566e3d3dfb5 [moby/moby#36222](https://github.com/moby/moby/pull/36222)

- Fix container cleanup on daemon restart [moby/moby#36249](https://github.com/moby/moby/pull/36249)

* Support SCTP port mapping (bump up API to v1.37) [moby/moby#33922](https://github.com/moby/moby/pull/33922)
* Support SCTP port mapping [docker/cli#278](https://github.com/docker/cli/pull/278)

- Fix Volumes property definition in ContainerConfig [moby/moby#35946](https://github.com/moby/moby/pull/35946)

* Bump moby and dependencies [docker/cli#829](https://github.com/docker/cli/pull/829)
* C.RWLayer: check for nil before use [moby/moby#36242](https://github.com/moby/moby/pull/36242)

- Add `REMOVE` and `ORPHANED` to TaskState [moby/moby#36146](https://github.com/moby/moby/pull/36146)

* Fixed error detection using `IsErrNotFound` and `IsErrNotImplemented` for `ContainerStatPath`, `CopyFromContainer`, and `CopyToContainer` methods [moby/moby#35979](https://github.com/moby/moby/pull/35979)

- Add an integration/internal/container helper package [moby/moby#36266](https://github.com/moby/moby/pull/36266)
- Add canonical import path [moby/moby#36194](https://github.com/moby/moby/pull/36194)
- Add/use container.Exec() to integration [moby/moby#36326](https://github.com/moby/moby/pull/36326)

* Fix "--node-generic-resource" singular/plural [moby/moby#36125](https://github.com/moby/moby/pull/36125)

- Daemon.cleanupContainer: nullify container RWLayer upon release [moby/moby#36160](https://github.com/moby/moby/pull/36160)
- Daemon: passdown the `--oom-kill-disable` option to containerd [moby/moby#36201](https://github.com/moby/moby/pull/36201)
- Display a warn message when there is binding ports and net mode is host [moby/moby#35510](https://github.com/moby/moby/pull/35510)
- Refresh containerd remotes on containerd restarted [moby/moby#36173](https://github.com/moby/moby/pull/36173)
- Set daemon root to use shared propagation [moby/moby#36096](https://github.com/moby/moby/pull/36096)
- Optimizations for recursive unmount [moby/moby#34379](https://github.com/moby/moby/pull/34379)
- Perform plugin mounts in the runtime [moby/moby#35829](https://github.com/moby/moby/pull/35829)
- Graphdriver: Fix RefCounter memory leak [moby/moby#36256](https://github.com/moby/moby/pull/36256)
- Use continuity fs package for volume copy [moby/moby#36290](https://github.com/moby/moby/pull/36290)
- Use proc/exe for reexec [moby/moby#36124](https://github.com/moby/moby/pull/36124)

* Add API support for templated secrets and configs [moby/moby#33702](https://github.com/moby/moby/pull/33702) and [moby/moby#36366](https://github.com/moby/moby/pull/36366)

- Use rslave propagation for mounts from daemon root [moby/moby#36055](https://github.com/moby/moby/pull/36055)

* Add /proc/keys to masked paths [moby/moby#36368](https://github.com/moby/moby/pull/36368)

- Bump Runc to 1.0.0-rc5 [moby/moby#36449](https://github.com/moby/moby/pull/36449)

* Fixes `runc exec` on big-endian architectures [moby/moby#36449](https://github.com/moby/moby/pull/36449)

- Use chroot when mount namespaces aren't provided [moby/moby#36449](https://github.com/moby/moby/pull/36449)

* Fix systemd slice expansion so that it could be consumed by cAdvisor [moby/moby#36449](https://github.com/moby/moby/pull/36449)
* Fix devices mounted with wrong uid/gid [moby/moby#36449](https://github.com/moby/moby/pull/36449)
* Fix read-only containers with IPC private mounts `/dev/shm` read-only [moby/moby#36526](https://github.com/moby/moby/pull/36526)

### [Swarm Mode](#swarm-mode-1)

* Replace EC Private Key with PKCS#8 PEMs [docker/swarmkit#2246](https://github.com/docker/swarmkit/pull/2246)
* Fix IP overlap with empty EndpointSpec [docker/swarmkit #2505](https://github.com/docker/swarmkit/pull/2505)
* Add support for Support SCTP port mapping [docker/swarmkit#2298](https://github.com/docker/swarmkit/pull/2298)
* Do not reschedule tasks if only placement constraints change and are satisfied by the assigned node [docker/swarmkit#2496](https://github.com/docker/swarmkit/pull/2496)
* Ensure task reaper stopChan is closed no more than once [docker/swarmkit #2491](https://github.com/docker/swarmkit/pull/2491)
* Synchronization fixes [docker/swarmkit#2495](https://github.com/docker/swarmkit/pull/2495)
* Add log message to indicate message send retry if streaming unimplemented [docker/swarmkit#2483](https://github.com/docker/swarmkit/pull/2483)
* Debug logs for session, node events on dispatcher, heartbeats [docker/swarmkit#2486](https://github.com/docker/swarmkit/pull/2486)

- Add swarm types to bash completion event type filter [docker/cli#888](https://github.com/docker/cli/pull/888)

* Fix issue where network inspect does not show Created time for networks in swarm scope [moby/moby#36095](https://github.com/moby/moby/pull/36095)

----
url: https://docs.docker.com/reference/cli/docker/mcp/version/
----

# docker mcp version

***

| Description | Show the version information |
| ----------- | ---------------------------- |
| Usage       | `docker mcp version`         |

## [Description](#description)

Show the version information

----
url: https://docs.docker.com/scout/integrations/registry/ecr/
----

# Integrate Docker Scout with Amazon ECR

***

Table of contents

***

Integrating Docker Scout with Amazon Elastic Container Registry (ECR) lets you view image insights for images hosted in ECR repositories. After integrating Docker Scout with ECR and activating Docker Scout for a repository, pushing an image to the repository automatically triggers image analysis. You can view image insights using the Docker Scout Dashboard, or the `docker scout` CLI commands.

## [How it works](#how-it-works)

To help you integrate Docker Scout with ECR, you can use a CloudFormation stack template that creates and configures the necessary AWS resources for integrating Docker Scout with your ECR registry. For more details about the AWS resources, see [CloudFormation stack template](#cloudformation-stack-template).

The following diagram shows how the Docker Scout ECR integration works.

After the integration, Docker Scout automatically pulls and analyzes images that you push to the ECR registry. Metadata about your images are stored on the Docker Scout platform, but Docker Scout doesn't store the container images themselves. For more information about how Docker Scout handles image data, see [Data handling](https://docs.docker.com/scout/deep-dive/data-handling/).

### [CloudFormation stack template](#cloudformation-stack-template)

The following table describes the configuration resources.

> Note
>
> Creating these resources incurs a small, recurring cost on the AWS account. The **Cost** column in the table represents an estimated monthly cost of the resources, when integrating an ECR registry that gets 100 images pushed per day.
>
> Additionally, an egress cost also applies when Docker Scout pulls the images from ECR. The egress cost is around $0.09 per GB.

| Resource type                 | Resource name                | Description                                                                                | Cost  |
| ----------------------------- | ---------------------------- | ------------------------------------------------------------------------------------------ | ----- |
| `AWS::SNSTopic::Topic`        | `SNSTopic`                   | SNS topic for notifying Docker Scout when the AWS resources have been created.             | Free  |
| `AWS::SNS::TopicPolicy`       | `TopicPolicy`                | Defines the topic for the initial setup notification.                                      | Free  |
| `AWS::SecretsManager::Secret` | `ScoutAPICredentials`        | Stores the credentials used by EventBridge to fire events to Scout.                        | $0.42 |
| `AWS::Events::ApiDestination` | `ApiDestination`             | Sets up the EventBridge connection to Docker Scout for sending ECR push and delete events. | $0.01 |
| `AWS::Events::Connection`     | `Connection`                 | EventBridge connection credentials to Scout.                                               | Free  |
| `AWS::Events::Rule`           | `DockerScoutEcrRule`         | Defines the rule to send ECR pushes and deletes to Scout.                                  | Free  |
| `AWS::Events::Rule`           | `DockerScoutRepoDeletedRule` | Defines the rule to send ECR repository deletes to Scout.                                  | Free  |
| `AWS::IAM::Role`              | `InvokeApiRole`              | Internal role to grant the event access to `ApiDestination`.                               | Free  |
| `AWS::IAM::Role`              | `AssumeRoleEcrAccess`        | This role has access to `ScoutAPICredentials` for setting up the Docker Scout integration. | Free  |

## [Integrate your first registry](#integrate-your-first-registry)

Create the CloudFormation stack in your AWS account to enable the Docker Scout integration.

Prerequisites:

* You must have access to an AWS account with permission to create resources.
* You have be an owner of the Docker organization.

To create the stack:

1. Go to the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/) on the Docker Scout Dashboard.

2. Select the **Create on AWS** button.

   This opens the **Create stack** wizard in the AWS CloudFormation console in a new browser tab. If you're not already signed in to AWS, you're redirected to the sign-in page first.

   If the button is grayed-out, it means you're lacking the necessary permissions in the Docker organization.

3. Follow the steps in the **Create stack** wizard until the end. Choose the AWS region you want to integrate. Complete the procedure by creating the resources.

   The fields in the wizard are pre-populated by the CloudFormation template, so you don't need to edit any of the fields.

4. When the resources have been created (the CloudFormation status shows `CREATE_COMPLETE` in the AWS console), return to the ECR integrations page in the Docker Scout Dashboard.

   The **Integrated registries** list shows the account ID and region for the ECR registry that you just integrated. If successful, the integration status is **Connected**.

The ECR integration is now active. For Docker Scout to start analyzing images in the registry, you need to activate it for each repository in [Repository settings](https://scout.docker.com/settings/repos/).

After activating repositories, images that you push are analyzed by Docker Scout. The analysis results appear in the Docker Scout Dashboard. If your repository already contains images, Docker Scout pulls and analyzes the latest image version automatically.

## [Integrate additional registries](#integrate-additional-registries)

To add additional registries:

1. Go to the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/) on the Docker Scout Dashboard.

2. Select the **Add** button at the top of the list.

3. Complete the steps for creating the AWS resources.

4. When the resources have been created, return to the ECR integrations page in the Docker Scout Dashboard.

   The **Integrated registries** list shows the account ID and region for the ECR registry that you just integrated. If successful, the integration status is **Connected**.

Next, activate Docker Scout for the repositories that you want to analyze in [Repository settings](https://scout.docker.com/settings/repos/).

## [Remove integration](#remove-integration)

To remove an integrated ECR registry, you must be an owner of the Docker organization.

1. Go to the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/) on the Docker Scout Dashboard.

2. Find the registry that you want to remove in the list of integrated registries, and select the remove icon in the **Actions** column.

   If the remove icon is disabled, it means that you're lacking the necessary permissions in the Docker organization.

3. In the dialog that opens, confirm by selecting **Remove**.

> Important
>
> Removing the integration from the Docker Scout dashboard doesn't remove the AWS resources in your account.
>
> After removing the integration in Docker Scout, go to the AWS console and delete the **DockerScoutECRIntegration** CloudFormation stack for the integration that you want to remove.

## [Troubleshooting](#troubleshooting)

### [Unable to integrate registry](#unable-to-integrate-registry)

Check the **Status** of the integration on the [ECR integration page](https://scout.docker.com/settings/integrations/ecr/) in the Docker Scout Dashboard.

* If the status is **Pending** for a prolonged period of time, it's an indication that the integration was not yet completed on the AWS side. Select the **Pending** link to open the CloudFormation wizard, and complete all the steps.

* An **Error** status indicates that something's gone wrong in the back-end. You can try [removing the integration](#remove-integration) and recreating it again.

### [ECR images not showing in the dashboard](#ecr-images-not-showing-in-the-dashboard)

If image analysis results for your ECR images aren't showing up in the Docker Scout Dashboard:

* Ensure that you've activated Docker Scout for the repository. View and manage active repositories in [Repository settings](https://scout.docker.com/settings/repos/).

* Ensure that the AWS account ID and region for your registry is listed on the ECR integrations page.

  The account ID and region are included in the registry hostname: `<aws_account_id>.dkr.ecr.<region>.amazonaws.com/<image>`

----
url: https://docs.docker.com/engine/network/drivers/ipvlan/
----

# IPvlan network driver

***

Table of contents

***

The IPvlan driver gives users total control over both IPv4 and IPv6 addressing. The VLAN driver builds on top of that in giving operators complete control of layer 2 VLAN tagging and even IPvlan L3 routing for users interested in underlay network integration. For overlay deployments that abstract away physical constraints see the [multi-host overlay](https://docs.docker.com/engine/network/drivers/overlay/) driver.

IPvlan is a new twist on the tried and true network virtualization technique. The Linux implementations are extremely lightweight because rather than using the traditional Linux bridge for isolation, they are associated to a Linux Ethernet interface or sub-interface to enforce separation between networks and connectivity to the physical network.

IPvlan offers a number of unique features and plenty of room for further innovations with the various modes. Two high level advantages of these approaches are, the positive performance implications of bypassing the Linux bridge and the simplicity of having fewer moving parts. Removing the bridge that traditionally resides in between the Docker host NIC and container interface leaves a simple setup consisting of container interfaces, attached directly to the Docker host interface. This result is easy to access for external facing services as there is no need for port mappings in these scenarios.

## [Options](#options)

The following table describes the driver-specific options that you can pass to `--opt` when creating a network using the `ipvlan` driver.

| Option        | Default  | Description                                                           |
| ------------- | -------- | --------------------------------------------------------------------- |
| `ipvlan_mode` | `l2`     | Sets the IPvlan operating mode. Can be one of: `l2`, `l3`, `l3s`      |
| `ipvlan_flag` | `bridge` | Sets the IPvlan mode flag. Can be one of: `bridge`, `private`, `vepa` |
| `parent`      |          | Specifies the parent interface to use.                                |

## [Examples](#examples)

### [Prerequisites](#prerequisites)

* The examples on this page are all single host.
* All examples can be performed on a single host running Docker. Any example using a sub-interface like `eth0.10` can be replaced with `eth0` or any other valid parent interface on the Docker host. Sub-interfaces with a `.` are created on the fly. `-o parent` interfaces can also be left out of the `docker network create` all together and the driver will create a `dummy` interface that will enable local host connectivity to perform the examples.
* Kernel requirements:
  * IPvlan Linux kernel v4.2+ (support for earlier kernels exists but is buggy). To check your current kernel version, use `uname -r`

### [IPvlan L2 mode example usage](#ipvlan-l2-mode-example-usage)

An example of the IPvlan `L2` mode topology is shown in the following image. The driver is specified with `-d driver_name` option. In this case `-d ipvlan`.

The parent interface in the next example `-o parent=eth0` is configured as follows:

```console
$ ip addr show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

Use the network from the host's interface as the `--subnet` in the `docker network create`. The container will be attached to the same network as the host interface as set via the `-o parent=` option.

Create the IPvlan network and run a container attaching to it:

```console
# IPvlan  (-o ipvlan_mode= Defaults to L2 mode if not specified)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    --gateway=192.168.1.1 \
    -o ipvlan_mode=l2 \
    -o parent=eth0 db_net

# Start a container on the db_net network
$ docker run --net=db_net -it --rm alpine /bin/sh

# NOTE: the containers can NOT ping the underlying host interfaces as
# they are intentionally filtered by Linux for additional isolation.
```

The default mode for IPvlan is `l2`. If `-o ipvlan_mode=` is left unspecified, the default mode will be used. Similarly, if the `--gateway` is left empty, the first usable address on the network will be set as the gateway. For example, if the subnet provided in the network create is `--subnet=192.168.1.0/24` then the gateway the container receives is `192.168.1.1`.

To help understand how this mode interacts with other hosts, the following figure shows the same layer 2 segment between two Docker hosts that applies to and IPvlan L2 mode.

The following will create the exact same network as the network `db_net` created earlier, with the driver defaults for `--gateway=192.168.1.1` and `-o ipvlan_mode=l2`.

```console
# IPvlan  (-o ipvlan_mode= Defaults to L2 mode if not specified)
$ docker network create -d ipvlan \
    --subnet=192.168.1.0/24 \
    -o parent=eth0 db_net_ipv

# Start a container with an explicit name in daemon mode
$ docker run --net=db_net_ipv --name=ipv1 -itd alpine /bin/sh

# Start a second container and ping using the container name
# to see the docker included name resolution functionality
$ docker run --net=db_net_ipv --name=ipv2 -it --rm alpine /bin/sh
$ ping -c 4 ipv1

# NOTE: the containers can NOT ping the underlying host interfaces as
# they are intentionally filtered by Linux for additional isolation.
```

The drivers also support the `--internal` flag that will completely isolate containers on a network from any communications external to that network. Since network isolation is tightly coupled to the network's parent interface the result of leaving the `-o parent=` option off of a `docker network create` is the exact same as the `--internal` option. If the parent interface is not specified or the `--internal` flag is used, a netlink type `dummy` parent interface is created for the user and used as the parent interface effectively isolating the network completely.

The following two `docker network create` examples result in identical networks that you can attach container to:

```console
# Empty '-o parent=' creates an isolated network
$ docker network create -d ipvlan \
    --subnet=192.168.10.0/24 isolated1

# Explicit '--internal' flag is the same:
$ docker network create -d ipvlan \
    --subnet=192.168.11.0/24 --internal isolated2

# Even the '--subnet=' can be left empty and the default
# IPAM subnet of 172.18.0.0/16 will be assigned
$ docker network create -d ipvlan isolated3

$ docker run --net=isolated1 --name=cid1 -it --rm alpine /bin/sh
$ docker run --net=isolated2 --name=cid2 -it --rm alpine /bin/sh
$ docker run --net=isolated3 --name=cid3 -it --rm alpine /bin/sh

# To attach to any use `docker exec` and start a shell
$ docker exec -it cid1 /bin/sh
$ docker exec -it cid2 /bin/sh
$ docker exec -it cid3 /bin/sh
```

### [IPvlan 802.1Q trunk L2 mode example usage](#ipvlan-8021q-trunk-l2-mode-example-usage)

Architecturally, IPvlan L2 mode trunking is the same as Macvlan with regard to gateways and L2 path isolation. There are nuances that can be advantageous for CAM table pressure in ToR switches, one MAC per port and MAC exhaustion on a host's parent NIC to name a few. The 802.1Q trunk scenario looks the same. Both modes adhere to tagging standards and have seamless integration with the physical network for underlay integration and hardware vendor plugin integrations.

Hosts on the same VLAN are typically on the same subnet and almost always are grouped together based on their security policy. In most scenarios, a multi-tier application is tiered into different subnets because the security profile of each process requires some form of isolation. For example, hosting your credit card processing on the same virtual network as the frontend webserver would be a regulatory compliance issue, along with circumventing the long standing best practice of layered defense in depth architectures. VLANs or the equivocal VNI (Virtual Network Identifier) when using the Overlay driver, are the first step in isolating tenant traffic.

The Linux sub-interface tagged with a VLAN can either already exist or will be created when you call a `docker network create`. `docker network rm` will delete the sub-interface. Parent interfaces such as `eth0` are not deleted, only sub-interfaces with a netlink parent index > 0.

For the driver to add/delete the VLAN sub-interfaces the format needs to be `interface_name.vlan_tag`. Other sub-interface naming can be used as the specified parent, but the link will not be deleted automatically when `docker network rm` is invoked.

The option to use either existing parent VLAN sub-interfaces or let Docker manage them enables the user to either completely manage the Linux interfaces and networking or let Docker create and delete the VLAN parent sub-interfaces (netlink `ip link`) with no effort from the user.

For example: use `eth0.10` to denote a sub-interface of `eth0` tagged with the VLAN id of `10`. The equivalent `ip link` command would be `ip link add link eth0 name eth0.10 type vlan id 10`.

The example creates the VLAN tagged networks and then starts two containers to test connectivity between containers. Different VLANs cannot ping one another without a router routing between the two networks. The default namespace is not reachable per IPvlan design in order to isolate container namespaces from the underlying host.

#### [VLAN ID 20](#vlan-id-20)

In the first network tagged and isolated by the Docker host, `eth0.20` is the parent interface tagged with VLAN id `20` specified with `-o parent=eth0.20`. Other naming formats can be used, but the links need to be added and deleted manually using `ip link` or Linux configuration files. As long as the `-o parent` exists, anything can be used if it is compliant with Linux netlink.

```console
# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged
$ docker network create -d ipvlan \
    --subnet=192.168.20.0/24 \
    --gateway=192.168.20.1 \
    -o parent=eth0.20 ipvlan20

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan20 -it --name ivlan_test1 --rm alpine /bin/sh
$ docker run --net=ipvlan20 -it --name ivlan_test2 --rm alpine /bin/sh
```

#### [VLAN ID 30](#vlan-id-30)

In the second network, tagged and isolated by the Docker host, `eth0.30` is the parent interface tagged with VLAN id `30` specified with `-o parent=eth0.30`. The `ipvlan_mode=` defaults to l2 mode `ipvlan_mode=l2`. It can also be explicitly set with the same result as shown in the next example.

```console
# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged.
$ docker network create -d ipvlan \
    --subnet=192.168.30.0/24 \
    --gateway=192.168.30.1 \
    -o parent=eth0.30 \
    -o ipvlan_mode=l2 ipvlan30

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan30 -it --name ivlan_test3 --rm alpine /bin/sh
$ docker run --net=ipvlan30 -it --name ivlan_test4 --rm alpine /bin/sh
```

The gateway is set inside of the container as the default gateway. That gateway would typically be an external router on the network.

```console
$$ ip route
  default via 192.168.30.1 dev eth0
  192.168.30.0/24 dev eth0  src 192.168.30.2
```

Example: Multi-Subnet IPvlan L2 Mode starting two containers on the same subnet and pinging one another. In order for the `192.168.114.0/24` to reach `192.168.116.0/24` it requires an external router in L2 mode. L3 mode can route between subnets that share a common `-o parent=`.

Secondary addresses on network routers are common as an address space becomes exhausted to add another secondary to an L3 VLAN interface or commonly referred to as a "switched virtual interface" (SVI).

```console
$ docker network create -d ipvlan \
    --subnet=192.168.114.0/24 --subnet=192.168.116.0/24 \
    --gateway=192.168.114.254 --gateway=192.168.116.254 \
    -o parent=eth0.114 \
    -o ipvlan_mode=l2 ipvlan114

$ docker run --net=ipvlan114 --ip=192.168.114.10 -it --rm alpine /bin/sh
$ docker run --net=ipvlan114 --ip=192.168.114.11 -it --rm alpine /bin/sh
```

A key takeaway is, operators have the ability to map their physical network into their virtual network for integrating containers into their environment with no operational overhauls required. NetOps drops an 802.1Q trunk into the Docker host. That virtual link would be the `-o parent=` passed in the network creation. For untagged (non-VLAN) links, it is as simple as `-o parent=eth0` or for 802.1Q trunks with VLAN IDs each network gets mapped to the corresponding VLAN/Subnet from the network.

An example being, NetOps provides VLAN ID and the associated subnets for VLANs being passed on the Ethernet link to the Docker host server. Those values are plugged into the `docker network create` commands when provisioning the Docker networks. These are persistent configurations that are applied every time the Docker engine starts which alleviates having to manage often complex configuration files. The network interfaces can also be managed manually by being pre-created and Docker networking will never modify them, and use them as parent interfaces. Example mappings from NetOps to Docker network commands are as follows:

* VLAN: 10, Subnet: 172.16.80.0/24, Gateway: 172.16.80.1
  * `--subnet=172.16.80.0/24 --gateway=172.16.80.1 -o parent=eth0.10`
* VLAN: 20, IP subnet: 172.16.50.0/22, Gateway: 172.16.50.1
  * `--subnet=172.16.50.0/22 --gateway=172.16.50.1 -o parent=eth0.20`
* VLAN: 30, Subnet: 10.1.100.0/16, Gateway: 10.1.100.1
  * `--subnet=10.1.100.0/16 --gateway=10.1.100.1 -o parent=eth0.30`

### [IPvlan L3 mode example](#ipvlan-l3-mode-example)

IPvlan will require routes to be distributed to each endpoint. The driver only builds the IPvlan L3 mode port and attaches the container to the interface. Route distribution throughout a cluster is beyond the initial implementation of this single host scoped driver. In L3 mode, the Docker host is very similar to a router starting new networks in the container. They are on networks that the upstream network will not know about without route distribution. For those curious how IPvlan L3 will fit into container networking, see the following examples.

IPvlan L3 mode drops all broadcast and multicast traffic. This reason alone makes IPvlan L3 mode a prime candidate for those looking for massive scale and predictable network integrations. It is predictable and in turn will lead to greater uptimes because there is no bridging involved. Bridging loops have been responsible for high profile outages that can be hard to pinpoint depending on the size of the failure domain. This is due to the cascading nature of BPDUs (Bridge Port Data Units) that are flooded throughout a broadcast domain (VLAN) to find and block topology loops. Eliminating bridging domains, or at the least, keeping them isolated to a pair of ToRs (top of rack switches) will reduce hard to troubleshoot bridging instabilities. IPvlan L2 modes is well suited for isolated VLANs only trunked into a pair of ToRs that can provide a loop-free non-blocking fabric. The next step further is to route at the edge via IPvlan L3 mode that reduces a failure domain to a local host only.

* L3 mode needs to be on a separate subnet as the default namespace since it requires a netlink route in the default namespace pointing to the IPvlan parent interface.
* The parent interface used in this example is `eth0` and it is on the subnet `192.168.1.0/24`. Notice the `docker network` is not on the same subnet as `eth0`.
* Unlike IPvlan l2 modes, different subnets/networks can ping one another as long as they share the same parent interface `-o parent=`.

```console
$$ ip a show eth0
3: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 00:50:56:39:45:2e brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.250/24 brd 192.168.1.255 scope global eth0
```

* A traditional gateway doesn't mean much to an L3 mode IPvlan interface since there is no broadcast traffic allowed. Because of that, the container default gateway points to the containers `eth0` device. See below for CLI output of `ip route` or `ip -6 route` from inside an L3 container for details.

The mode `-o ipvlan_mode=l3` must be explicitly specified since the default IPvlan mode is `l2`.

The following example does not specify a parent interface. The network drivers will create a dummy type link for the user rather than rejecting the network creation and isolating containers from only communicating with one another.

```console
# Create the IPvlan L3 network
$ docker network create -d ipvlan \
    --subnet=192.168.214.0/24 \
    --subnet=10.1.214.0/24 \
    -o ipvlan_mode=l3 ipnet210

# Test 192.168.214.0/24 connectivity
$ docker run --net=ipnet210 --ip=192.168.214.10 -itd alpine /bin/sh
$ docker run --net=ipnet210 --ip=10.1.214.10 -itd alpine /bin/sh

# Test L3 connectivity from 10.1.214.0/24 to 192.168.214.0/24
$ docker run --net=ipnet210 --ip=192.168.214.9 -it --rm alpine ping -c 2 10.1.214.10

# Test L3 connectivity from 192.168.214.0/24 to 10.1.214.0/24
$ docker run --net=ipnet210 --ip=10.1.214.9 -it --rm alpine ping -c 2 192.168.214.10
```

> Note
>
> Notice that there is no `--gateway=` option in the network create. The field is ignored if one is specified `l3` mode. Take a look at the container routing table from inside of the container:
>
> ```console
> # Inside an L3 mode container
> $$ ip route
>  default dev eth0
>   192.168.214.0/24 dev eth0  src 192.168.214.10
> ```

In order to ping the containers from a remote Docker host or the container be able to ping a remote host, the remote host or the physical network in between need to have a route pointing to the host IP address of the container's Docker host eth interface.

### [Dual stack IPv4 IPv6 IPvlan L2 mode](#dual-stack-ipv4-ipv6-ipvlan-l2-mode)

* Not only does Libnetwork give you complete control over IPv4 addressing, but it also gives you total control over IPv6 addressing as well as feature parity between the two address families.

* The next example will start with IPv6 only. Start two containers on the same VLAN `139` and ping one another. Since the IPv4 subnet is not specified, the default IPAM will provision a default IPv4 subnet. That subnet is isolated unless the upstream network is explicitly routing it on VLAN `139`.

```console
# Create a v6 network
$ docker network create -d ipvlan \
    --ipv6 --subnet=2001:db8:abc2::/64 --gateway=2001:db8:abc2::22 \
    -o parent=eth0.139 v6ipvlan139

# Start a container on the network
$ docker run --net=v6ipvlan139 -it --rm alpine /bin/sh
```

View the container eth0 interface and v6 routing table:

```console
# Inside the IPv6 container
$$ ip a show eth0
75: eth0@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.2/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc2::1/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc2::/64 dev eth0  proto kernel  metric 256
default via 2001:db8:abc2::22 dev eth0  metric 1024
```

Start a second container and ping the first container's v6 address.

```console
# Test L2 connectivity over IPv6
$ docker run --net=v6ipvlan139 -it --rm alpine /bin/sh

# Inside the second IPv6 container
$$ ip a show eth0
75: eth0@if55: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 172.18.0.3/16 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link tentative dadfailed
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc2::2/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ping6 2001:db8:abc2::1
PING 2001:db8:abc2::1 (2001:db8:abc2::1): 56 data bytes
64 bytes from 2001:db8:abc2::1%eth0: icmp_seq=0 ttl=64 time=0.044 ms
64 bytes from 2001:db8:abc2::1%eth0: icmp_seq=1 ttl=64 time=0.058 ms

2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max/stddev = 0.044/0.051/0.058/0.000 ms
```

The next example with setup a dual stack IPv4/IPv6 network with an example VLAN ID of `140`.

Next create a network with two IPv4 subnets and one IPv6 subnets, all of which have explicit gateways:

```console
$ docker network create -d ipvlan \
    --subnet=192.168.140.0/24 --subnet=192.168.142.0/24 \
    --gateway=192.168.140.1 --gateway=192.168.142.1 \
    --subnet=2001:db8:abc9::/64 --gateway=2001:db8:abc9::22 \
    -o parent=eth0.140 \
    -o ipvlan_mode=l2 ipvlan140
```

Start a container and view eth0 and both v4 & v6 routing tables:

```console
$ docker run --net=ipvlan140 --ip6=2001:db8:abc2::51 -it --rm alpine /bin/sh

$ ip a show eth0
78: eth0@if77: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.140.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc9::1/64 scope link nodad
       valid_lft forever preferred_lft forever

$$ ip route
default via 192.168.140.1 dev eth0
192.168.140.0/24 dev eth0  proto kernel  scope link  src 192.168.140.2

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc9::/64 dev eth0  proto kernel  metric 256
default via 2001:db8:abc9::22 dev eth0  metric 1024
```

Start a second container with a specific `--ip4` address and ping the first host using IPv4 packets:

```console
$ docker run --net=ipvlan140 --ip=192.168.140.10 -it --rm alpine /bin/sh
```

> Note
>
> Different subnets on the same parent interface in IPvlan `L2` mode cannot ping one another. That requires a router to proxy-arp the requests with a secondary subnet. However, IPvlan `L3` will route the unicast traffic between disparate subnets as long as they share the same `-o parent` parent link.

### [Use router-assigned IPv6 addresses](#use-router-assigned-ipv6-addresses)

The previous examples assign IPv6 addresses from a subnet managed by Docker's IPAM. On an `ipvlan` network, you can instead let containers receive IPv6 addresses directly from a router on the parent network, using stateless address autoconfiguration (SLAAC).

When an `ipvlan` network has no IPv6 subnet, Docker disables IPv6 on the container's interface, so it can't accept the router advertisements that SLAAC relies on. To re-enable IPv6 on the interface, set its `disable_ipv6` sysctl to `0` when you connect the container to the network:

```console
$ docker network connect \
    --driver-opt="com.docker.network.endpoint.sysctls=net.ipv6.conf.IFNAME.disable_ipv6=0" \
    my-ipvlan-net my-container
```

Use the literal string `IFNAME` in the sysctl name. Docker replaces it with the name of the container's interface on this network. `disable_ipv6` is a per-interface sysctl, so it must be set with the `endpoint.sysctls` driver option rather than `docker run --sysctl`. For more details, see [`docker network connect`](/reference/cli/docker/network/connect/#sysctl).

### [Dual stack IPv4 IPv6 IPvlan L3 mode](#dual-stack-ipv4-ipv6-ipvlan-l3-mode)

Example: IPvlan L3 Mode Dual Stack IPv4/IPv6, Multi-Subnet w/ 802.1Q VLAN Tag:118

As in all of the examples, a tagged VLAN interface does not have to be used. The sub-interfaces can be swapped with `eth0`, `eth1`, `bond0` or any other valid interface on the host other then the `lo` loopback.

The primary difference you will see is that L3 mode does not create a default route with a next-hop but rather sets a default route pointing to `dev eth` only since ARP/Broadcasts/Multicast are all filtered by Linux as per the design. Since the parent interface is essentially acting as a router, the parent interface IP and subnet needs to be different from the container networks. That is the opposite of bridge and L2 modes, which need to be on the same subnet (broadcast domain) in order to forward broadcast and multicast packets.

```console
# Create an IPv6+IPv4 Dual Stack IPvlan L3 network
# Gateways for both v4 and v6 are set to a dev e.g. 'default dev eth0'
$ docker network create -d ipvlan \
    --subnet=192.168.110.0/24 \
    --subnet=192.168.112.0/24 \
    --ipv6 --subnet=2001:db8:abc6::/64 \
    -o parent=eth0 \
    -o ipvlan_mode=l3 ipnet110


# Start a few of containers on the network (ipnet110)
# in separate terminals and check connectivity
$ docker run --net=ipnet110 -it --rm alpine /bin/sh
# Start a second container specifying the v6 address
$ docker run --net=ipnet110 --ip6=2001:db8:abc6::10 -it --rm alpine /bin/sh
# Start a third specifying the IPv4 address
$ docker run --net=ipnet110 --ip=192.168.112.30 -it --rm alpine /bin/sh
# Start a 4th specifying both the IPv4 and IPv6 addresses
$ docker run --net=ipnet110 --ip6=2001:db8:abc6::50 --ip=192.168.112.50 -it --rm alpine /bin/sh
```

Interface and routing table outputs are as follows:

```console
$$ ip a show eth0
63: eth0@if59: <BROADCAST,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default
    link/ether 00:50:56:2b:29:40 brd ff:ff:ff:ff:ff:ff
    inet 192.168.112.2/24 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc4::250:56ff:fe2b:2940/64 scope link
       valid_lft forever preferred_lft forever
    inet6 2001:db8:abc6::10/64 scope link nodad
       valid_lft forever preferred_lft forever

# Note the default route is the eth device because ARPs are filtered.
$$ ip route
  default dev eth0  scope link
  192.168.112.0/24 dev eth0  proto kernel  scope link  src 192.168.112.2

$$ ip -6 route
2001:db8:abc4::/64 dev eth0  proto kernel  metric 256
2001:db8:abc6::/64 dev eth0  proto kernel  metric 256
default dev eth0  metric 1024
```

> Note
>
> There may be a bug when specifying `--ip6=` addresses when you delete a container with a specified v6 address and then start a new container with the same v6 address it throws the following like the address isn't properly being released to the v6 pool. It will fail to unmount the container and be left dead.

```console
docker: Error response from daemon: Address already in use.
```

### [Manually create 802.1Q links](#manually-create-8021q-links)

#### [VLAN ID 40](#vlan-id-40)

If a user does not want the driver to create the VLAN sub-interface, it needs to exist before running `docker network create`. If you have sub-interface naming that is not `interface.vlan_id` it is honored in the `-o parent=` option again as long as the interface exists and is up.

Links, when manually created, can be named anything as long as they exist when the network is created. Manually created links do not get deleted regardless of the name when the network is deleted with `docker network rm`.

```console
# create a new sub-interface tied to dot1q vlan 40
$ ip link add link eth0 name eth0.40 type vlan id 40

# enable the new sub-interface
$ ip link set eth0.40 up

# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged
$ docker network create -d ipvlan \
    --subnet=192.168.40.0/24 \
    --gateway=192.168.40.1 \
    -o parent=eth0.40 ipvlan40

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan40 -it --name ivlan_test5 --rm alpine /bin/sh
$ docker run --net=ipvlan40 -it --name ivlan_test6 --rm alpine /bin/sh
```

Example: VLAN sub-interface manually created with any name:

```console
# create a new sub interface tied to dot1q vlan 40
$ ip link add link eth0 name foo type vlan id 40

# enable the new sub-interface
$ ip link set foo up

# now add networks and hosts as you would normally by attaching to the master (sub)interface that is tagged
$ docker network create -d ipvlan \
    --subnet=192.168.40.0/24 --gateway=192.168.40.1 \
    -o parent=foo ipvlan40

# in two separate terminals, start a Docker container and the containers can now ping one another.
$ docker run --net=ipvlan40 -it --name ivlan_test5 --rm alpine /bin/sh
$ docker run --net=ipvlan40 -it --name ivlan_test6 --rm alpine /bin/sh
```

Manually created links can be cleaned up with:

```console
$ ip link del foo
```

As with all of the Libnetwork drivers, they can be mixed and matched, even as far as running 3rd party ecosystem drivers in parallel for maximum flexibility to the Docker user.

----
url: https://docs.docker.com/reference/cli/docker/context/ls/
----

# docker context ls

***

| Description                                                               | List contexts                 |
| ------------------------------------------------------------------------- | ----------------------------- |
| Usage                                                                     | `docker context ls [OPTIONS]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker context list`         |

## [Description](#description)

List contexts

## [Options](#options)

| Option        | Default | Description                                                                                                                                                                                                                                                                                                                                                                            |
| ------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--format`    |         | Format output using a custom template: 'table': Print output in table format with column headers (default) 'table TEMPLATE': Print output in table format using the given Go template 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `-q, --quiet` |         | Only show context names                                                                                                                                                                                                                                                                                                                                                                |

## [Examples](#examples)

Use `docker context ls` to print all contexts. The currently active context is indicated with an `*`:

```console
$ docker context ls

NAME                DESCRIPTION                               DOCKER ENDPOINT                      ORCHESTRATOR
default *           Current DOCKER_HOST based configuration   unix:///var/run/docker.sock          swarm
production                                                    tcp:///prod.corp.example.com:2376
staging                                                       tcp:///stage.corp.example.com:2376
```

----
url: https://docs.docker.com/reference/cli/docker/pass/set/
----

# docker pass set

***

| Description | Set a secret                         |
| ----------- | ------------------------------------ |
| Usage       | `docker pass set id[=value] [flags]` |

## [Description](#description)

Stores a secret in the local OS keychain. The secret value can be provided inline (`NAME=VALUE`) or piped via STDIN.

Behavior when a secret with the same id already exists is platform-dependent:

* macOS (Keychain): the command fails with a duplicate-item error.
* Linux (Secret Service) and Windows (Credential Manager): the existing value is silently overwritten.

Pass `--force` to overwrite an existing secret. On Linux and Windows the replacement is performed atomically. On macOS the Keychain API requires a delete-then-add sequence.

## [Options](#options)

| Option        | Default | Description                                    |
| ------------- | ------- | ---------------------------------------------- |
| `-f, --force` |         | Overwrite existing secret if it already exists |
| `--metadata`  |         | Non-sensitive key=value metadata (repeatable)  |

## [Examples](#examples)

### [Set a secret:](#set-a-secret)

```console
$ docker pass set POSTGRES_PASSWORD=my-secret-password
```

### [Or pass the secret via STDIN:](#or-pass-the-secret-via-stdin)

```console
$ echo my-secret-password > pwd.txt
$ cat pwd.txt | docker pass set POSTGRES_PASSWORD
```

### [Set a secret with metadata:](#set-a-secret-with-metadata)

```console
$ docker pass set POSTGRES_PASSWORD=my-secret-password --metadata owner=alice --metadata expiry=2027-03-01
```

### [Or pass a JSON payload with secret and metadata via STDIN:](#or-pass-a-json-payload-with-secret-and-metadata-via-stdin)

```console
$ echo '{"secret":"my-secret-password","metadata":{"owner":"alice"}}' | docker pass set POSTGRES_PASSWORD
```

### [Overwrite an existing secret:](#overwrite-an-existing-secret)

```console
$ docker pass set POSTGRES_PASSWORD=new-secret-password --force
```

----
url: https://docs.docker.com/reference/cli/docker/scout/vex/
----

# docker scout vex

***

| Description                                                               | Manage VEX attestations on images |
| ------------------------------------------------------------------------- | --------------------------------- |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker scout vex`                |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Manage VEX attestations on images

## [Subcommands](#subcommands)

| Command                                                                               | Description                   |
| ------------------------------------------------------------------------------------- | ----------------------------- |
| [`docker scout vex get`](https://docs.docker.com/reference/cli/docker/scout/vex/get/) | Get VEX attestation for image |

----
url: https://docs.docker.com/reference/api/extensions-sdk/DesktopUI/
----

# Interface: DesktopUI

***

Table of contents

***

**`Since`**

0.2.0

## [Properties](#properties)

### [toast](#toast)

• `Readonly` **toast**: [`Toast`](https://docs.docker.com/reference/api/extensions-sdk/Toast/)

***

### [dialog](#dialog)

• `Readonly` **dialog**: [`Dialog`](https://docs.docker.com/reference/api/extensions-sdk/Dialog/)

***

### [navigate](#navigate)

• `Readonly` **navigate**: [`NavigationIntents`](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/)

----
url: https://docs.docker.com/billing/
----

# Manage billing and payments

***

***

Use the resources in this section to manage billing and payments for your Docker subscriptions.

### [Add or update a payment method](/billing/payment-method/)

[Learn how to add or update a payment method for your personal account or organization.](/billing/payment-method/)

### [Update billing information](/billing/details/)

[Discover how to update the billing information for your personal account or organization.](/billing/details/)

### [View billing history](/billing/history/)

[Learn how to view billing history and download past invoices.](/billing/history/)

### [Billing FAQs](/billing/faqs/)

[Find the answers you need and explore common questions.](/billing/faqs/)

### [Register a tax certificate](/billing/tax-certificate/)

[Learn how to register a tax exemption certificate.](/billing/tax-certificate/)

### [3D Secure authentication](/billing/3d-secure/)

[Discover how Docker billing supports 3DS and how to troubleshoot potential issues.](/billing/3d-secure/)

----
url: https://docs.docker.com/guides/text-classification/
----

[Build a text recognition app](https://docs.docker.com/guides/text-classification/)

This guide details how to containerize text classification models using Docker.

Python AI

20 minutes

[« Back to all guides](/guides/)

# Build a text recognition app

***

Table of contents

***

## [Overview](#overview)

In this guide, you'll learn how to create and run a text recognition application. You'll build the application using Python with scikit-learn and the Natural Language Toolkit (NLTK). Then you'll set up the environment and run the application using Docker.

The application analyzes the sentiment of a user's input text using NLTK's SentimentIntensityAnalyzer. It lets the user input text, which is then processed to determine its sentiment, classifying it as either positive or negative. Also, it displays the accuracy and a detailed classification report of its sentiment analysis model based on a predefined dataset.

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

The source code for the text classification application is in the `Docker-NLP/03_text_classification.py` file. Open `03_text_classification.py` in a text or code editor to explore its contents in the following steps.

1. Import the required libraries.

   ```python
   import nltk
   from nltk.sentiment import SentimentIntensityAnalyzer
   from sklearn.metrics import accuracy_score, classification_report
   from sklearn.model_selection import train_test_split
   import ssl
   ```

   * `nltk`: A popular Python library for natural language processing (NLP).
   * `SentimentIntensityAnalyzer`: A component of `nltk` for sentiment analysis.
   * `accuracy_score`, `classification_report`: Functions from scikit-learn for evaluating the model.
   * `train_test_split`: Function from scikit-learn to split datasets into training and testing sets.
   * `ssl`: Used for handling SSL certificate issues which might occur while downloading data for `nltk`.

2. Handle SSL certificate verification.

   ```python
   try:
       _create_unverified_https_context = ssl._create_unverified_context
   except AttributeError:
       pass
   else:
       ssl._create_default_https_context = _create_unverified_https_context
   ```

   This block is a workaround for certain environments where downloading data through NLTK might fail due to SSL certificate verification issues. It's telling Python to ignore SSL certificate verification for HTTPS requests.

3. Download NLTK resources.

   ```python
   nltk.download('vader_lexicon')
   ```

   The `vader_lexicon` is a lexicon used by the `SentimentIntensityAnalyzer` for sentiment analysis.

4. Define text for testing and corresponding labels.

   ```python
   texts = [...]
   labels = [0, 1, 2, 0, 1, 2]
   ```

   This section defines a small dataset of texts and their corresponding labels (0 for positive, 1 for negative, and 2 for spam).

5. Split the test data.

   ```python
   X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)
   ```

   This part splits the dataset into training and testing sets, with 20% of data as the test set. As this application uses a pre-trained model, it doesn't train the model.

6. Set up sentiment analysis.

   ```python
   sia = SentimentIntensityAnalyzer()
   ```

   This code initializes the `SentimentIntensityAnalyzer` to analyze the sentiment of text.

7. Generate predictions and classifications for the test data.

   ```python
   vader_predictions = [sia.polarity_scores(text)["compound"] for text in X_test]
   threshold = 0.2
   vader_classifications = [0 if score > threshold else 1 for score in vader_predictions]
   ```

   This part generates sentiment scores for each text in the test set and classifies them as positive or negative based on a threshold.

8. Evaluate the model.

   ```python
   accuracy = accuracy_score(y_test, vader_classifications)
   report_vader = classification_report(y_test, vader_classifications, zero_division='warn')
   ```

   This part calculates the accuracy and classification report for the predictions.

9. Specify the main execution block.

   ```python
   if __name__ == "__main__":
   ```

   This Python idiom ensures that the following code block runs only if this script is the main program. It provides flexibility, allowing the script to function both as a standalone program and as an imported module.

10. Create an infinite loop for continuous input.

    ```python
       while True:
        input_text = input("Enter the text for classification (type 'exit' to end): ")

          if input_text.lower() == 'exit':
             print("Exiting...")
             break
    ```

    This while loop runs indefinitely until it's explicitly broken. It lets the user continuously enter text for entity recognition until they decide to exit.

11. Analyze the text.

    ```python
            input_text_score = sia.polarity_scores(input_text)["compound"]
            input_text_classification = 0 if input_text_score > threshold else 1
    ```

12. Print the VADER Classification Report and the sentiment analysis.

    ```python
            print(f"Accuracy: {accuracy:.2f}")
            print("\nVADER Classification Report:")
            print(report_vader)

            print(f"\nTest Text (Positive): '{input_text}'")
            print(f"Predicted Sentiment: {'Positive' if input_text_classification == 0 else 'Negative'}")
    ```

13. Create `requirements.txt`. The sample application already contains the `requirements.txt` file to specify the necessary packages that the application imports. Open `requirements.txt` in a code or text editor to explore its contents.

    ```text
    # 01 sentiment_analysis
    nltk==3.6.5

    ...

    # 03 text_classification
    scikit-learn==1.3.2

    ...
    ```

    Both the `nltk` and `scikit-learn` modules are required for the text classification application.

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

   The `COPY` command transfers the `requirements.txt` file from your local machine into the Docker image. This file lists all Python dependencies required by the application. Copying it into the container lets the next command (`RUN pip install`) install these dependencies inside the image environment.

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
   $ docker run -it basic-nlp 03_text_classification.py
   ```

   The following is a break down of the command:

   * `docker run`: This is the primary command used to run a new container from a Docker image.

   * `-it`: This is a combination of two options:

     * `-i` or `--interactive`: This keeps the standard input (STDIN) open even if not attached. It lets the container remain running in the foreground and be interactive.
     * `-t` or `--tty`: This allocates a pseudo-TTY, essentially simulating a terminal, like a command prompt or a shell. It's what lets you interact with the application inside the container.

   * `basic-nlp`: This specifies the name of the Docker image to use for creating the container. In this case, it's the image named `basic-nlp` that you created with the `docker build` command.

   * `03_text_classification.py`: This is the script you want to run inside the Docker container. It gets passed to the `entrypoint.sh` script, which runs it when the container starts.

   For more details, see the [docker run CLI reference](/reference/cli/docker/container/run/).

   > Note
   >
   > For Windows users, you may get an error when running the container. Verify that the line endings in the `entrypoint.sh` are `LF` (`\n`) and not `CRLF` (`\r\n`), then rebuild the image. For more details, see \[Avoid unexpected syntax errors, use Unix style line endings for files in containers]\(/desktop/troubleshoot-and-support/troubleshoot/topics/#Unexpected-syntax-errors-use-Unix-style-line endings-for-files-in-containers).

   You will see the following in your console after the container starts.

   ```console
   Enter the text for classification (type 'exit' to end):
   ```

3. Test the application.

   Enter some text to get the text classification.

   ```console
   Enter the text for classification (type 'exit' to end): I love containers!
   Accuracy: 1.00

   VADER Classification Report:
                 precision    recall  f1-score   support

              0       1.00      1.00      1.00         1
              1       1.00      1.00      1.00         1

       accuracy                           1.00         2
      macro avg       1.00      1.00      1.00         2
   weighted avg       1.00      1.00      1.00         2

   Test Text (Positive): 'I love containers!'
   Predicted Sentiment: Positive
   ```

## [Summary](#summary)

In this guide, you learned how to build and run a text classification application. You learned how to build the application using Python with scikit-learn and NLTK. Then you learned how to set up the environment and run the application using Docker.

Related information:

* [Docker CLI reference](/reference/cli/docker/)
* [Dockerfile reference](/reference/dockerfile/)
* [Natural Language Toolkit](https://www.nltk.org/)
* [Python documentation](https://docs.python.org/3/)
* [scikit-learn](https://scikit-learn.org/)

## [Next steps](#next-steps)

Explore more [natural language processing guides](https://docs.docker.com/guides/).

----
url: https://docs.docker.com/compose/install/uninstall/
----

# Uninstall Docker Compose

***

Table of contents

***

How you uninstall Docker Compose depends on how it was installed. This guide covers uninstallation instructions for:

* Docker Compose installed via Docker Desktop
* Docker Compose installed as a CLI plugin

## [Uninstalling Docker Compose with Docker Desktop](#uninstalling-docker-compose-with-docker-desktop)

If you want to uninstall Docker Compose and you have installed Docker Desktop, see [Uninstall Docker Desktop](https://docs.docker.com/desktop/uninstall/).

> Warning
>
> Unless you have other Docker instances installed on that specific environment, uninstalling Docker Desktop removes all Docker components, including Docker Engine, Docker CLI, and Docker Compose.

## [Uninstalling the Docker Compose CLI plugin](#uninstalling-the-docker-compose-cli-plugin)

If you installed Docker Compose via a package manager, run:

On Ubuntu or Debian:

```console
$ sudo apt-get remove docker-compose-plugin
```

On RPM-based distributions:

```console
$ sudo yum remove docker-compose-plugin
```

### [Manually installed](#manually-installed)

If you installed Docker Compose manually (using curl), remove it by deleting the binary:

```console
$ rm $DOCKER_CONFIG/cli-plugins/docker-compose
```

### [Remove for all users](#remove-for-all-users)

If installed for all users, remove it from the system directory:

```console
$ rm /usr/local/lib/docker/cli-plugins/docker-compose
```

> Note
>
> If you get a **Permission denied** error using either of the previous methods, you do not have the permissions needed to remove Docker Compose. To force the removal, prepend `sudo` to either of the previous instructions and run it again.

### [Inspect the location of the Compose CLI plugin](#inspect-the-location-of-the-compose-cli-plugin)

To check where Compose is installed, use:

```console
$ docker info --format '{{range .ClientInfo.Plugins}}{{if eq .Name "compose"}}{{.Path}}{{end}}{{end}}'
```

----
url: https://docs.docker.com/engine/logging/drivers/splunk/
----

# Splunk logging driver

***

Table of contents

***

The `splunk` logging driver sends container logs to [HTTP Event Collector](https://dev.splunk.com/enterprise/docs/devtools/httpeventcollector/) in Splunk Enterprise and Splunk Cloud.

## [Usage](#usage)

You can configure Docker logging to use the `splunk` driver by default or on a per-container basis.

To use the `splunk` driver as the default logging driver, set the keys `log-driver` and `log-opts` to appropriate values in the `daemon.json` configuration file and restart Docker. For example:

```json
{
  "log-driver": "splunk",
  "log-opts": {
    "splunk-token": "",
    "splunk-url": "",
    ...
  }
}
```

For more about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must be provided as strings. Boolean and numeric values (such as the value for `splunk-gzip` or `splunk-gzip-level`) must therefore be enclosed in quotes (`"`).

To use the `splunk` driver for a specific container, use the commandline flags `--log-driver` and `log-opt` with `docker run`:

```console
$ docker run --log-driver=splunk --log-opt splunk-token=VALUE --log-opt splunk-url=VALUE ...
```

## [Splunk options](#splunk-options)

The following properties let you configure the Splunk logging driver.

* To configure the `splunk` driver across the Docker environment, edit `daemon.json` with the key, `"log-opts": {"NAME": "VALUE", ...}`.
* To configure the `splunk` driver for an individual container, use `docker run` with the flag, `--log-opt NAME=VALUE ...`.

| Option                      | Required | Description                                                                                                                                                                                                                                                                                                                                |
| --------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `splunk-token`              | required | Splunk HTTP Event Collector token.                                                                                                                                                                                                                                                                                                         |
| `splunk-url`                | required | Path to your Splunk Enterprise, self-service Splunk Cloud instance, or Splunk Cloud managed cluster (including port and scheme used by HTTP Event Collector) in one of the following formats: `https://your_splunk_instance:8088`, `https://input-prd-p-XXXXXXX.cloud.splunk.com:8088`, or `https://http-inputs-XXXXXXXX.splunkcloud.com`. |
| `splunk-source`             | optional | Event source.                                                                                                                                                                                                                                                                                                                              |
| `splunk-sourcetype`         | optional | Event source type.                                                                                                                                                                                                                                                                                                                         |
| `splunk-index`              | optional | Event index.                                                                                                                                                                                                                                                                                                                               |
| `splunk-capath`             | optional | Path to root certificate.                                                                                                                                                                                                                                                                                                                  |
| `splunk-caname`             | optional | Name to use for validating server certificate; by default the hostname of the `splunk-url` is used.                                                                                                                                                                                                                                        |
| `splunk-insecureskipverify` | optional | Ignore server certificate validation.                                                                                                                                                                                                                                                                                                      |
| `splunk-format`             | optional | Message format. Can be `inline`, `json` or `raw`. Defaults to `inline`.                                                                                                                                                                                                                                                                    |
| `splunk-verify-connection`  | optional | Verify on start, that Docker can connect to Splunk server. Defaults to true.                                                                                                                                                                                                                                                               |
| `splunk-gzip`               | optional | Enable/disable gzip compression to send events to Splunk Enterprise or Splunk Cloud instance. Defaults to false.                                                                                                                                                                                                                           |
| `splunk-gzip-level`         | optional | Set compression level for gzip. Valid values are -1 (default), 0 (no compression), 1 (best speed) ... 9 (best compression). Defaults to [DefaultCompression](https://golang.org/pkg/compress/gzip/#DefaultCompression).                                                                                                                    |
| `tag`                       | optional | Specify tag for message, which interpret some markup. Default value is `{{.ID}}` (12 characters of the container ID). Refer to the [log tag option documentation](https://docs.docker.com/engine/logging/log_tags/) for customizing the log tag format.                                                                                    |
| `labels`                    | optional | Comma-separated list of keys of labels, which should be included in message, if these labels are specified for container.                                                                                                                                                                                                                  |
| `labels-regex`              | optional | Similar to and compatible with `labels`. A regular expression to match logging-related labels. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                                                                                                                                      |
| `env`                       | optional | Comma-separated list of keys of environment variables, which should be included in message, if these variables are specified for container.                                                                                                                                                                                                |
| `env-regex`                 | optional | Similar to and compatible with `env`. A regular expression to match logging-related environment variables. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                                                                                                                          |

If there is collision between the `label` and `env` keys, the value of the `env` takes precedence. Both options add additional fields to the attributes of a logging message.

Below is an example of the logging options specified for the Splunk Enterprise instance. The instance is installed locally on the same machine on which the Docker daemon is running.

The path to the root certificate and Common Name is specified using an HTTPS scheme. This is used for verification. The `SplunkServerDefaultCert` is automatically generated by Splunk certificates.

```console
$ docker run \
    --log-driver=splunk \
    --log-opt splunk-token=176FCEBF-4CF5-4EDF-91BC-703796522D20 \
    --log-opt splunk-url=https://splunkhost:8088 \
    --log-opt splunk-capath=/path/to/cert/cacert.pem \
    --log-opt splunk-caname=SplunkServerDefaultCert \
    --log-opt tag="{{.Name}}/{{.FullID}}" \
    --log-opt labels=location \
    --log-opt env=TEST \
    --env "TEST=false" \
    --label location=west \
    your/application
```

The `splunk-url` for Splunk instances hosted on Splunk Cloud is in a format like `https://http-inputs-XXXXXXXX.splunkcloud.com` and does not include a port specifier.

### [Message formats](#message-formats)

There are three logging driver messaging formats: `inline` (default), `json`, and `raw`.

The default format is `inline` where each log message is embedded as a string. For example:

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "my message"
}
```

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "{\"foo\": \"bar\"}"
}
```

To format messages as `json` objects, set `--log-opt splunk-format=json`. The driver attempts to parse every line as a JSON object and send it as an embedded object. If it can't parse the message, it's sent `inline`. For example:

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": "my message"
}
```

```json
{
  "attrs": {
    "env1": "val1",
    "label1": "label1"
  },
  "tag": "MyImage/MyContainer",
  "source": "stdout",
  "line": {
    "foo": "bar"
  }
}
```

To format messages as `raw`, set `--log-opt splunk-format=raw`. Attributes (environment variables and labels) and tags are prefixed to the message. For example:

```console
MyImage/MyContainer env1=val1 label1=label1 my message
MyImage/MyContainer env1=val1 label1=label1 {"foo": "bar"}
```

## [Advanced options](#advanced-options)

The Splunk logging driver lets you configure a few advanced options by setting environment variables for the Docker daemon.

| Environment variable name                        | Default value | Description                                                                                                                              |
| ------------------------------------------------ | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `SPLUNK_LOGGING_DRIVER_POST_MESSAGES_FREQUENCY`  | `5s`          | The time to wait for more messages to batch.                                                                                             |
| `SPLUNK_LOGGING_DRIVER_POST_MESSAGES_BATCH_SIZE` | `1000`        | The number of messages that should accumulate before sending them in one batch.                                                          |
| `SPLUNK_LOGGING_DRIVER_BUFFER_MAX`               | `10 * 1000`   | The maximum number of messages held in buffer for retries.                                                                               |
| `SPLUNK_LOGGING_DRIVER_CHANNEL_SIZE`             | `4 * 1000`    | The maximum number of pending messages that can be in the channel used to send messages to background logger worker, which batches them. |

----
url: https://docs.docker.com/reference/cli/docker/mcp/gateway/
----

# docker mcp gateway

***

| Description | Manage the MCP Server gateway |
| ----------- | ----------------------------- |

## [Description](#description)

Manage the MCP Server gateway

## [Subcommands](#subcommands)

| Command                                                                                   | Description     |
| ----------------------------------------------------------------------------------------- | --------------- |
| [`docker mcp gateway run`](https://docs.docker.com/reference/cli/docker/mcp/gateway/run/) | Run the gateway |

----
url: https://docs.docker.com/enterprise/enterprise-deployment/use-intune/
----

# Deploy with Intune

***

Table of contents

***

For: Administrators

Learn how to deploy Docker Desktop on Windows and macOS devices using Microsoft Intune. It covers app creation, installer configuration, and assignment to users or devices.

1. Sign in to your Intune admin center.

2. Add a new app. Select **Apps**, then **Windows**, then **Add**.

3. For the app type, select **Windows app (Win32)**

4. Select the `intunewin` package.

5. Fill in the required details, such as the description, publisher, or app version and then select **Next**.

6. Optional: On the **Program** tab, you can update the **Install command** field to suit your needs. The field is pre-populated with `msiexec /i "DockerDesktop.msi" /qn`. See the [Common installation scenarios](https://docs.docker.com/enterprise/enterprise-deployment/msi-install-and-configure/) for examples on the changes you can make.

   > Tip
   >
   > It's recommended you configure the Intune deployment to schedule a reboot of the machine on successful installs.
   >
   > This is because the Docker Desktop installer installs Windows features depending on your engine selection and also updates the membership of the `docker-users` local group.
   >
   > You may also want to set Intune to determine behaviour based on return codes and watch for a return code of `3010`. Return code 3010 means the installation succeeded but a reboot is required.

7. Complete the remaining tabs, then review and create the app.

First, upload the package:

1. Sign in to your Intune admin center.
2. Add a new app. Select **Apps**, then **macOS**, then **Add**.
3. Select **Line-of-business app** and then **Select**.
4. Upload the `Docker.pkg` file and fill in the required details.

Next, assign the app:

1. Once the app is added, navigate to **Assignments** in Intune.
2. Select **Add group** and choose the user or device groups you want to assign the app to.
3. Select **Save**.

## [Additional resources](#additional-resources)

* [Explore the FAQs](https://docs.docker.com/enterprise/enterprise-deployment/faq/).
* Learn how to [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) for your users.

----
url: https://docs.docker.com/engine/swarm/how-swarm-mode-works/swarm-task-states/
----

# Swarm task states

***

Table of contents

***

Docker lets you create services, which can start tasks. A service is a description of a desired state, and a task does the work. Work is scheduled on swarm nodes in this sequence:

1. Create a service by using `docker service create`.
2. The request goes to a Docker manager node.
3. The Docker manager node schedules the service to run on particular nodes.
4. Each service can start multiple tasks.
5. Each task has a life cycle, with states like `NEW`, `PENDING`, and `COMPLETE`.

Tasks are execution units that run once to completion. When a task stops, it isn't executed again, but a new task may take its place.

Tasks advance through a number of states until they complete or fail. Tasks are initialized in the `NEW` state. The task progresses forward through a number of states, and its state doesn't go backward. For example, a task never goes from `COMPLETE` to `RUNNING`.

Tasks go through the states in the following order:

| Task state  | Description                                                                                                 |
| ----------- | ----------------------------------------------------------------------------------------------------------- |
| `NEW`       | The task was initialized.                                                                                   |
| `PENDING`   | Resources for the task were allocated.                                                                      |
| `ASSIGNED`  | Docker assigned the task to nodes.                                                                          |
| `ACCEPTED`  | The task was accepted by a worker node. If a worker node rejects the task, the state changes to `REJECTED`. |
| `READY`     | The worker node is ready to start the task                                                                  |
| `PREPARING` | Docker is preparing the task.                                                                               |
| `STARTING`  | Docker is starting the task.                                                                                |
| `RUNNING`   | The task is executing.                                                                                      |
| `COMPLETE`  | The task exited without an error code.                                                                      |
| `FAILED`    | The task exited with an error code.                                                                         |
| `SHUTDOWN`  | Docker requested the task to shut down.                                                                     |
| `REJECTED`  | The worker node rejected the task.                                                                          |
| `ORPHANED`  | The node was down for too long.                                                                             |
| `REMOVE`    | The task is not terminal but the associated service was removed or scaled down.                             |

## [View task state](#view-task-state)

Run `docker service ps <service-name>` to get the state of a task. The `CURRENT STATE` field shows the task's state and how long it's been there.

```console
$ docker service ps webserver
ID             NAME              IMAGE    NODE        DESIRED STATE  CURRENT STATE            ERROR                              PORTS
owsz0yp6z375   webserver.1       nginx    UbuntuVM    Running        Running 44 seconds ago
j91iahr8s74p    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 50 seconds ago    "No such container: webserver.…"
7dyaszg13mw2    \_ webserver.1   nginx    UbuntuVM    Shutdown       Failed 5 hours ago       "No such container: webserver.…"
```

## [Where to go next](#where-to-go-next)

* [Learn about swarm tasks](https://github.com/moby/swarmkit/blob/master/design/task_model.md)

----
url: https://docs.docker.com/reference/cli/docker/model/run/
----

# docker model run

***

| Description | Run a model and interact with it using a submitted prompt or chat mode |
| ----------- | ---------------------------------------------------------------------- |
| Usage       | `docker model run MODEL [PROMPT]`                                      |

## [Description](#description)

When you run a model, Docker calls an inference server API endpoint hosted by the Model Runner through Docker Desktop. The model stays in memory until another model is requested, or until a pre-defined inactivity timeout is reached (currently 5 minutes).

You do not have to use Docker model run before interacting with a specific model from a host process or from within a container. Model Runner transparently loads the requested model on-demand, assuming it has been pulled and is locally available.

You can also use chat mode in the Docker Desktop Dashboard when you select the model in the **Models** tab.

## [Options](#options)

| Option         | Default | Description                                          |
| -------------- | ------- | ---------------------------------------------------- |
| `--color`      | `no`    | Use colored output (auto\|yes\|no)                   |
| `--debug`      |         | Enable debug logging                                 |
| `-d, --detach` |         | Load the model in the background without interaction |
| `--openaiurl`  |         | OpenAI-compatible API endpoint URL to chat with      |
| `--websearch`  |         | Enable web search tool during chat                   |

## [Examples](#examples)

### [One-time prompt](#one-time-prompt)

```console
docker model run ai/smollm2 "Hi"
```

Output:

```console
Hello! How can I assist you today?
```

### [Interactive chat](#interactive-chat)

```console
docker model run ai/smollm2
```

Output:

```console
> Hi
Hi there! It's SmolLM, AI assistant. How can I help you today?
> /bye
```

### [Pre-load a model](#pre-load-a-model)

```console
docker model run --detach ai/smollm2
```

This loads the model into memory without interaction, ensuring maximum performance for subsequent requests.

----
url: https://docs.docker.com/docker-hub/repos/manage/builds/
----

# Automated builds

***

***

Subscription: Pro Team Business

Availability: Deprecated

> Warning
>
> Docker Hub Automated Builds is a deprecated feature. It will be fully retired on April 1, 2027.

Docker Hub can automatically build images from source code in an external repository and automatically push the built image to your Docker repositories.

When you set up automated builds, also called autobuilds, you create a list of branches and tags that you want to build into Docker images. When you push code to a source-code branch, for example in GitHub, for one of those listed image tags, the push uses a webhook to trigger a new build, which produces a Docker image. The built image is then pushed to Docker Hub.

> Note
>
> You can still use `docker push` to push pre-built images to repositories with automated builds configured.

If you have automated tests configured, these run after building, but before pushing to the registry. You can use these tests to create a continuous integration workflow where a build that fails its tests doesn't push the built image. Automated tests don't push images to the registry on their own. [Learn about automated image testing](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/).

Depending on your [subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsHubRepoBuilds), you may get concurrent builds, which means that `N` autobuilds can be run at the same time. `N` is configured according to your subscription. Once `N+1` builds are running, any additional builds go into a queue to be run later.

The maximum number of pending builds in the queue is 30 and Docker Hub discards further requests. The number of concurrent builds for Pro is 5 and for Team and Business is 15. Automated builds can handle images of up to 10 GB in size.

----
url: https://docs.docker.com/reference/cli/sbx/secret/set-custom/
----

# sbx secret set-custom

| Description | Create or update a custom secret                |
| ----------- | ----------------------------------------------- |
| Usage       | `sbx secret set-custom [-g \| sandbox] [flags]` |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Create or update a custom secret for a service not built into sbx.

Custom secrets work via a placeholder: the sandbox sees the placeholder value instead of the real secret. When the sandbox makes an outbound request to the target host, the proxy replaces the placeholder with the real secret in the request headers — the secret never enters the sandbox directly.

\--host accepts an exact host, IP address, or wildcard pattern. Repeat --host to cover multiple unrelated domains with one secret. "*" matches a single label and "\*\*" matches any number of labels. For example "*.example.com" covers "cli.example.com" and "ide.example.com" with one entry.

Secrets can be scoped globally (shared across all sandboxes) or to a specific sandbox.

## [Options](#options)

| Option          | Default | Description                                                        |
| --------------- | ------- | ------------------------------------------------------------------ |
| `--env`         |         | Set this env var in the sandbox to the placeholder value           |
| `-g, --global`  |         | Use global secret scope                                            |
| `--host`        |         | Host, IP, or wildcard pattern (e.g. \*.example.com); repeatable    |
| `--placeholder` |         | Placeholder value; use {rand} for a random suffix (e.g. sk-{rand}) |
| `-t, --token`   |         | Secret value (less secure: visible in shell history)               |
| `--value`       |         | Secret value (less secure: visible in shell history)               |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Create a global custom secret. A unique placeholder is generated automatically.
# The sandbox env var API_KEY is set to the placeholder value; outbound requests
# to the host have the placeholder replaced with the real secret.
sbx secret set-custom -g --host api.example.com --env API_KEY --value secret123

# Use a wildcard host to cover multiple subdomains that share one key.
sbx secret set-custom -g --host '*.coderabbit.ai' --env CODERABBIT_API_KEY --value secret123

# Use multiple --host flags to cover unrelated domains with the same key.
sbx secret set-custom -g --host api.example.com --host api.other.io --env API_KEY --value secret123

# Scope to a specific sandbox instead of globally.
sbx secret set-custom my-sandbox --host api.example.com --env API_KEY --value secret123

# Custom placeholder with {rand} suffix; the CLI prints the generated value.
sbx secret set-custom -g --host api.example.com --placeholder sk-{rand} --value secret123
```

----
url: https://docs.docker.com/reference/build-checks/invalid-default-arg-in-from/
----

# InvalidDefaultArgInFrom

***

Table of contents

***

## [Output](#output)

```text
Using the global ARGs with default values should produce a valid build.
```

## [Description](#description)

An `ARG` used in an image reference should be valid when no build arguments are used. An image build should not require `--build-arg` to be used to produce a valid build.

## [Examples](#examples)

❌ Bad: don't rely on an ARG being set for an image reference to be valid

```dockerfile
ARG TAG
FROM busybox:${TAG}
```

✅ Good: include a default for the ARG

```dockerfile
ARG TAG=latest
FROM busybox:${TAG}
```

✅ Good: ARG can be empty if the image would be valid with it empty

```dockerfile
ARG VARIANT
FROM busybox:stable${VARIANT}
```

✅ Good: Use a default value if the build arg is not present

```dockerfile
ARG TAG
FROM alpine:${TAG:-3.14}
```

----
url: https://docs.docker.com/guides/testcontainers-java-micronaut-kafka/create-project/
----

# Create the Micronaut project

***

Table of contents

***

## [Set up the project](#set-up-the-project)

Create a Micronaut project from [Micronaut Launch](https://micronaut.io/launch) by selecting the **kafka**, **data-jpa**, **mysql**, **awaitility**, **assertj**, and **testcontainers** features.

Alternatively, clone the [guide repository](https://github.com/testcontainers/tc-guide-testing-micronaut-kafka-listener).

You'll use the [Awaitility](http://www.awaitility.org/) library to assert the expectations of an asynchronous process flow.

The key dependencies in `pom.xml` are:

```xml
<parent>
    <groupId>io.micronaut.platform</groupId>
    <artifactId>micronaut-parent</artifactId>
    <version>4.1.4</version>
</parent>
<dependencies>
    <dependency>
        <groupId>io.micronaut.data</groupId>
        <artifactId>micronaut-data-hibernate-jpa</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.kafka</groupId>
        <artifactId>micronaut-kafka</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.serde</groupId>
        <artifactId>micronaut-serde-jackson</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.sql</groupId>
        <artifactId>micronaut-jdbc-hikari</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.awaitility</groupId>
        <artifactId>awaitility</artifactId>
        <version>4.2.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-kafka</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-mysql</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

The Micronaut parent POM manages the Testcontainers BOM, so you don't need to specify versions for Testcontainers modules individually.

## [Create the JPA entity](#create-the-jpa-entity)

The application listens to a topic called `product-price-changes`. When a message arrives, it extracts the product code and price from the event payload and updates the price for that product in the MySQL database.

Create `Product.java`:

```java
package com.testcontainers.demo;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import java.math.BigDecimal;

@Entity
@Table(name = "products")
public class Product {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String code;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false)
    private BigDecimal price;

    public Product() {}

    public Product(Long id, String code, String name, BigDecimal price) {
        this.id = id;
        this.code = code;
        this.name = name;
        this.price = price;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getCode() {
        return code;
    }

    public void setCode(String code) {
        this.code = code;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }
}
```

## [Create the Micronaut Data JPA repository](#create-the-micronaut-data-jpa-repository)

Create a repository interface for the `Product` entity with a method to find a product by code and a method to update the price for a given product code:

```java
package com.testcontainers.demo;

import io.micronaut.data.annotation.Query;
import io.micronaut.data.annotation.Repository;
import io.micronaut.data.jpa.repository.JpaRepository;
import java.math.BigDecimal;
import java.util.Optional;

@Repository
public interface ProductRepository extends JpaRepository<Product, Long> {

    Optional<Product> findByCode(String code);

    @Query("update Product p set p.price = :price where p.code = :productCode")
    void updateProductPrice(String productCode, BigDecimal price);
}
```

Unlike Spring Data JPA, Micronaut Data uses compile-time annotation processing to implement repository methods, avoiding runtime reflection.

## [Create the event payload](#create-the-event-payload)

Create a record named `ProductPriceChangedEvent` that represents the structure of the event payload received from the Kafka topic:

```java
package com.testcontainers.demo;

import io.micronaut.serde.annotation.Serdeable;
import java.math.BigDecimal;

@Serdeable
public record ProductPriceChangedEvent(String productCode, BigDecimal price) {}
```

The `@Serdeable` annotation tells Micronaut Serialization that this type can be serialized and deserialized.

The sender and receiver agree on the following JSON format:

```json
{
  "productCode": "P100",
  "price": 25.0
}
```

## [Implement the Kafka listener](#implement-the-kafka-listener)

Create `ProductPriceChangedEventHandler.java`, which handles messages from the `product-price-changes` topic and updates the product price in the database:

```java
package com.testcontainers.demo;

import static io.micronaut.configuration.kafka.annotation.OffsetReset.EARLIEST;

import io.micronaut.configuration.kafka.annotation.KafkaListener;
import io.micronaut.configuration.kafka.annotation.Topic;
import jakarta.inject.Singleton;
import jakarta.transaction.Transactional;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Singleton
@Transactional
class ProductPriceChangedEventHandler {

    private static final Logger LOG = LoggerFactory.getLogger(ProductPriceChangedEventHandler.class);

    private final ProductRepository productRepository;

    ProductPriceChangedEventHandler(ProductRepository productRepository) {
        this.productRepository = productRepository;
    }

    @Topic("product-price-changes")
    @KafkaListener(offsetReset = EARLIEST, groupId = "demo")
    public void handle(ProductPriceChangedEvent event) {
        LOG.info("Received a ProductPriceChangedEvent with productCode:{}: ", event.productCode());
        productRepository.updateProductPrice(event.productCode(), event.price());
    }
}
```

Key details:

* The `@KafkaListener` annotation marks this class as a Kafka message listener. Setting `offsetReset` to `EARLIEST` makes the listener start consuming messages from the beginning of the partition, which is useful during testing.
* The `@Topic` annotation specifies which topic to subscribe to.
* Micronaut handles JSON deserialization of the `ProductPriceChangedEvent` automatically using Micronaut Serialization.

## [Configure the datasource](#configure-the-datasource)

Add the following properties to `src/main/resources/application.properties`:

```properties
micronaut.application.name=tc-guide-testing-micronaut-kafka-listener
datasources.default.db-type=mysql
datasources.default.dialect=MYSQL
jpa.default.properties.hibernate.hbm2ddl.auto=update
jpa.default.entity-scan.packages=com.testcontainers.demo
datasources.default.driver-class-name=com.mysql.cj.jdbc.Driver
```

Hibernate's `hbm2ddl.auto=update` creates and updates the database schema automatically. For testing, you'll override this to `create-drop` in the test properties file.

Create `src/test/resources/application-test.properties`:

```properties
jpa.default.properties.hibernate.hbm2ddl.auto=create-drop
```

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-java-micronaut-kafka/write-tests/)

----
url: https://docs.docker.com/enterprise/security/provisioning/scim/group-mapping/
----

# Group mapping

***

Table of contents

***

Subscription: Business

For: Administrators

Group mapping automatically synchronizes user groups from your identity provider (IdP) with teams in your Docker organization. For example, when you add a developer to the "backend-team" group in your IdP, they're automatically added to the corresponding team in Docker

This page explains how group mapping works, and how to set up group mapping.

> Tip
>
> Group mapping is ideal for adding users to multiple organizations or multiple teams within one organization. If you don't need to set up multi-organization or multi-team assignment, SCIM [user-level attributes](https://docs.docker.com/enterprise/security/provisioning/scim/provision-scim/#set-up-role-mapping) may be a better fit for your needs.

## [Prerequisites](#prerequisites)

Before you begin, you must have:

* SSO configured for your organization
* Administrator access to Docker Home and your identity provider

## [How group mapping works](#how-group-mapping-works)

Group mapping keeps your Docker Teams synchronized with your IdP groups through these key components:

* Authentication flow: When users sign in through SSO, your IdP shares user attributes with Docker including email, name, and group memberships.
* Automatic updates: Docker uses these attributes to create or update user profiles and manage team assignments based on IdP group changes.
* Unique identification: Docker uses email addresses as unique identifiers, so each Docker account must have a unique email address.
* Team synchronization: Users' team memberships in Docker automatically reflect changes made in your IdP groups.

## [Set up group mapping](#set-up-group-mapping)

Group mapping setup involves configuring your identity provider to share group information with Docker. This requires:

* Creating groups in your IdP using Docker's naming format
* Configuring attributes so your IdP sends group data during authentication
* Adding users to the appropriate groups
* Testing the connection to ensure groups sync properly

You can use group mapping with SSO only, or with both SSO and SCIM for enhanced user lifecycle management.

### [Group naming format](#group-naming-format)

Create groups in your IdP using the format: `organization:team`.

For example:

* For the "developers" team in the "moby" organization: `moby:developers`
* For multi-organization access: `moby:backend` and `whale:desktop`

Docker creates teams automatically if they don't already exist when groups sync.

### [Supported attributes](#supported-attributes)

| Attribute          | Description                                                                         |
| ------------------ | ----------------------------------------------------------------------------------- |
| `id`               | Unique ID of the group in UUID format. This attribute is read-only.                 |
| `displayName`      | Name of the group following the group mapping format: `organization:team`.          |
| `members`          | A list of users that are members of this group.                                     |
| `members(x).value` | Unique ID of the user that is a member of this group. Members are referenced by ID. |

## [Configure group mapping with SSO](#configure-group-mapping-with-sso)

Use group mapping with SSO connections that use the SAML authentication method.

> Note
>
> Group mapping with SSO isn't supported with the Azure AD (OIDC) authentication method. SCIM isn't required for these configurations.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Okta documentation](https://help.okta.com/oie/en-us/content/topics/apps/define-group-attribute-statements.htm) to verify.

To set up group mapping:

1. Sign in to Okta and open your application.

2. Navigate to the **SAML Settings** page for your application.

3. In the **Group Attribute Statements (optional)** section, configure like the following:

   * **Name**: `groups`
   * **Name format**: `Unspecified`
   * **Filter**: `Starts with` + `organization:` where `organization` is the name of your organization The filter option will filter out the groups that aren't affiliated with your Docker organization.

4. Create your groups by selecting **Directory**, then **Groups**.

5. Add your groups using the format `organization:team` that matches the names of your organization(s) and team(s) in Docker.

6. Assign users to the group(s) that you create.

The next time you sync your groups with Docker, your users will map to the Docker groups you defined.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Entra ID documentation](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) to verify.

To set up group mapping:

1. Sign in to Entra ID and open your application.

2. Select **Manage**, then **Single sign-on**.

3. Select **Add a group claim**.

4. In the Group Claims section, select **Groups assigned to the application** with the source attribute **Cloud-only group display names (Preview)**.

5. Select **Advanced options**, then the **Filter groups** option.

6. Configure the attribute like the following:

   * **Attribute to match**: `Display name`
   * **Match with**: `Contains`
   * **String**: `:`

7. Select **Save**.

8. Select **Groups**, **All groups**, then **New group** to create your group(s).

9. Assign users to the group(s) that you create.

The next time you sync your groups with Docker, your users will map to the Docker groups you defined.

## [Configure group mapping with SCIM](#configure-group-mapping-with-scim)

Use group mapping with SCIM for more advanced user lifecycle management. Before you begin, make sure you [set up SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/provision-scim/#enable-scim) first.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Okta documentation](https://help.okta.com/en-us/Content/Topics/users-groups-profiles/usgp-enable-group-push.htm) to verify.

To set up your groups:

1. Sign in to Okta and open your application.

2. Select **Applications**, then **Provisioning**, and **Integration**.

3. Select **Edit** to enable groups on your connection, then select **Push groups**.

4. Select **Save**. Saving this configuration will add the **Push Groups** tab to your application.

5. Create your groups by navigating to **Directory** and selecting **Groups**.

6. Add your groups using the format `organization:team` that matches the names of your organization(s) and team(s) in Docker.

7. Assign users to the group(s) that you create.

8. Return to the **Integration** page, then select the **Push Groups** tab to open the view where you can control and manage how groups are provisioned.

9. Select **Push Groups**, then **Find groups by rule**.

10. Configure the groups by rule like the following:

    * Enter a rule name, for example `Sync groups with Docker Hub`
    * Match group by name, for example starts with `docker:` or contains `:` for multi-organization
    * If you enable **Immediately push groups by rule**, sync will happen as soon as there's a change to the group or group assignments. Enable this if you don't want to manually push groups.

Find your new rule under **By rule** in the **Pushed Groups** column. The groups that match that rule are listed in the groups table on the right-hand side.

To push the groups from this table:

1. Select **Group in Okta**.
2. Select the **Push Status** drop-down.
3. Select **Push Now**.

The user interface for your IdP may differ slightly from the following steps. Refer to the [Entra ID documentation](https://learn.microsoft.com/en-us/azure/active-directory/app-provisioning/customize-application-attributes) to verify.

Complete the following before configuring group mapping:

1. Sign in to Entra ID and go to your application.
2. In your application, select **Provisioning**, then **Mappings**.
3. Select **Provision Microsoft Entra ID Groups**.
4. Select **Show advanced options**, then **Edit attribute list**.
5. Update the `externalId` type to `reference`, then select the **Multi-Value** checkbox and choose the referenced object attribute `urn:ietf:params:scim:schemas:core:2.0:Group`.
6. Select **Save**, then **Yes** to confirm.
7. Go to **Provisioning**.
8. Toggle **Provision Status** to **On**, then select **Save**.

Next, set up group mapping:

1. Go to the application overview page.
2. Under **Provision user accounts**, select **Get started**.
3. Select **Add user/group**.
4. Create your group(s) using the `organization:team` format.
5. Assign the group to the provisioning group.
6. Select **Start provisioning** to start the sync.

To verify, select **Monitor**, then **Provisioning logs** to see that your groups were provisioned successfully. In your Docker organization, you can check that the groups were correctly provisioned and the members were added to the appropriate teams.

Once complete, a user who signs in to Docker through SSO is automatically added to the organizations and teams mapped in the IdP.

> Tip
>
> [Enable SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/provision-scim/) to take advantage of automatic user provisioning and de-provisioning. If you don't enable SCIM users are only automatically provisioned. You have to de-provision them manually.

## [Next steps](#next-steps)

* [Assign roles](https://docs.docker.com/enterprise/security/roles-and-permissions/core-roles/) to members of your org.
* [Enforce sign in](https://docs.docker.com/enterprise/security/enforce-sign-in/), if needed.

----
url: https://docs.docker.com/engine/containers/resource_constraints/
----

# Resource constraints

***

Table of contents

***

By default, a container has no resource constraints and can use as much of a given resource as the host's kernel scheduler allows. Docker provides ways to control how much memory, or CPU a container can use, setting runtime configuration flags of the `docker run` command. This section provides details on when you should set such limits and the possible implications of setting them.

Many of these features require your kernel to support Linux capabilities. To check for support, you can use the [`docker info`](/reference/cli/docker/system/info/) command. If a capability is disabled in your kernel, you may see a warning at the end of the output like the following:

```console
WARNING: No swap limit support
```

Consult your operating system's documentation for enabling them. See also the [Docker Engine troubleshooting guide](https://docs.docker.com/engine/daemon/troubleshoot/#kernel-cgroup-swap-limit-capabilities) for more information.

## [Memory](#memory)

## [Understand the risks of running out of memory](#understand-the-risks-of-running-out-of-memory)

It's important not to allow a running container to consume too much of the host machine's memory. On Linux hosts, if the kernel detects that there isn't enough memory to perform important system functions, it throws an `OOME`, or `Out Of Memory Exception`, and starts killing processes to free up memory. Any process is subject to killing, including Docker and other important applications. This can effectively bring the entire system down if the wrong process is killed.

Docker attempts to mitigate these risks by adjusting the OOM priority on the Docker daemon so that it's less likely to be killed than other processes on the system. The OOM priority on containers isn't adjusted. This makes it more likely for an individual container to be killed than for the Docker daemon or other system processes to be killed. You shouldn't try to circumvent these safeguards by manually setting `--oom-score-adj` to an extreme negative number on the daemon or a container, or by setting `--oom-kill-disable` on a container.

For more information about the Linux kernel's OOM management, see [Out of Memory Management](https://www.kernel.org/doc/gorman/html/understand/understand016.html).

You can mitigate the risk of system instability due to OOME by:

* Perform tests to understand the memory requirements of your application before placing it into production.
* Ensure that your application runs only on hosts with adequate resources.
* Limit the amount of memory your container can use, as described below.
* Be mindful when configuring swap on your Docker hosts. Swap is slower than memory but can provide a buffer against running out of system memory.
* Consider converting your container to a [service](https://docs.docker.com/engine/swarm/services/), and using service-level constraints and node labels to ensure that the application runs only on hosts with enough memory

### [Limit a container's access to memory](#limit-a-containers-access-to-memory)

Docker can enforce hard or soft memory limits.

* Hard limits let the container use no more than a fixed amount of memory.
* Soft limits let the container use as much memory as it needs unless certain conditions are met, such as when the kernel detects low memory or contention on the host machine.

Some of these options have different effects when used alone or when more than one option is set.

Most of these options take a positive integer, followed by a suffix of `b`, `k`, `m`, `g`, to indicate bytes, kilobytes, megabytes, or gigabytes.

| Option                 | Description                                                                                                                                                                                                                                                                                                                                                                                     |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-m` or `--memory=`    | The maximum amount of memory the container can use. If you set this option, the minimum allowed value is `6m` (6 megabytes). That is, you must set the value to at least 6 megabytes.                                                                                                                                                                                                           |
| `--memory-swap`\*      | The amount of memory this container is allowed to swap to disk. See [`--memory-swap` details](#--memory-swap-details).                                                                                                                                                                                                                                                                          |
| `--memory-swappiness`  | By default, the host kernel can swap out a percentage of anonymous pages used by a container. You can set `--memory-swappiness` to a value between 0 and 100, to tune this percentage. See [`--memory-swappiness` details](#--memory-swappiness-details).                                                                                                                                       |
| `--memory-reservation` | Allows you to specify a soft limit smaller than `--memory` which is activated when Docker detects contention or low memory on the host machine. If you use `--memory-reservation`, it must be set lower than `--memory` for it to take precedence. Because it is a soft limit, it doesn't guarantee that the container doesn't exceed the limit.                                                |
| `--oom-kill-disable`   | By default, if an out-of-memory (OOM) error occurs, the kernel kills processes in a container. To change this behavior, use the `--oom-kill-disable` option. Only disable the OOM killer on containers where you have also set the `-m/--memory` option. If the `-m` flag isn't set, the host can run out of memory and the kernel may need to kill the host system's processes to free memory. |

For more information about cgroups and memory in general, see the documentation for [Memory Resource Controller](https://www.kernel.org/doc/Documentation/cgroup-v1/memory.txt).

### [`--memory-swap` details](#--memory-swap-details)

`--memory-swap` is a modifier flag that only has meaning if `--memory` is also set. Using swap allows the container to write excess memory requirements to disk when the container has exhausted all the RAM that's available to it. There is a performance penalty for applications that swap memory to disk often.

Its setting can have complicated effects:

* If `--memory-swap` is set to a positive integer, then both `--memory` and `--memory-swap` must be set. `--memory-swap` represents the total amount of memory and swap that can be used, and `--memory` controls the amount used by non-swap memory. So if `--memory="300m"` and `--memory-swap="1g"`, the container can use 300m of memory and 700m (`1g - 300m`) swap.

* If `--memory-swap` is set to `0`, the setting is ignored, and the value is treated as unset.

* If `--memory-swap` is set to the same value as `--memory`, and `--memory` is set to a positive integer, **the container doesn't have access to swap**. See [Prevent a container from using swap](#prevent-a-container-from-using-swap).

* If `--memory-swap` is unset, and `--memory` is set, the container can use as much swap as the `--memory` setting, if the host container has swap memory configured. For instance, if `--memory="300m"` and `--memory-swap` is not set, the container can use 600m in total of memory and swap.

* If `--memory-swap` is explicitly set to `-1`, the container is allowed to use unlimited swap, up to the amount available on the host system.

* Inside the container, tools like `free` report the host's available swap, not what's available inside the container. Don't rely on the output of `free` or similar tools to determine whether swap is present.

#### [Prevent a container from using swap](#prevent-a-container-from-using-swap)

If `--memory` and `--memory-swap` are set to the same value, this prevents containers from using any swap. This is because `--memory-swap` is the amount of combined memory and swap that can be used, while `--memory` is only the amount of physical memory that can be used.

### [`--memory-swappiness` details](#--memory-swappiness-details)

* A value of 0 turns off anonymous page swapping.
* A value of 100 sets all anonymous pages as swappable.
* By default, if you don't set `--memory-swappiness`, the value is inherited from the host machine.

## [CPU](#cpu)

By default, each container's access to the host machine's CPU cycles is unlimited. You can set various constraints to limit a given container's access to the host machine's CPU cycles. Most users use and configure the [default CFS scheduler](#configure-the-default-cfs-scheduler). You can also configure the [real-time scheduler](#configure-the-real-time-scheduler).

### [Configure the default CFS scheduler](#configure-the-default-cfs-scheduler)

The CFS is the Linux kernel CPU scheduler for normal Linux processes. Several runtime flags let you configure the amount of access to CPU resources your container has. When you use these settings, Docker modifies the settings for the container's cgroup on the host machine.

| Option                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--cpus=<value>`       | Specify how much of the available CPU resources a container can use. For instance, if the host machine has two CPUs and you set `--cpus="1.5"`, the container is guaranteed at most one and a half of the CPUs. This is the equivalent of setting `--cpu-period="100000"` and `--cpu-quota="150000"`.                                                                                                                                                                                                                                                                                              |
| `--cpu-period=<value>` | Specify the CPU CFS scheduler period, which is used alongside `--cpu-quota`. Defaults to 100000 microseconds (100 milliseconds). Most users don't change this from the default. For most use-cases, `--cpus` is a more convenient alternative.                                                                                                                                                                                                                                                                                                                                                     |
| `--cpu-quota=<value>`  | Impose a CPU CFS quota on the container. The number of microseconds per `--cpu-period` that the container is limited to before being throttled. As such acting as the effective ceiling. For most use-cases, `--cpus` is a more convenient alternative.                                                                                                                                                                                                                                                                                                                                            |
| `--cpuset-cpus`        | Limit the specific CPUs or cores a container can use. A comma-separated list or hyphen-separated range of CPUs a container can use, if you have more than one CPU. The first CPU is numbered 0. A valid value might be `0-3` (to use the first, second, third, and fourth CPU) or `1,3` (to use the second and fourth CPU).                                                                                                                                                                                                                                                                        |
| `--cpu-shares`         | Set this flag to a value greater or less than the default of 1024 to increase or reduce the container's weight, and give it access to a greater or lesser proportion of the host machine's CPU cycles. This is only enforced when CPU cycles are constrained. When plenty of CPU cycles are available, all containers use as much CPU as they need. In that way, this is a soft limit. `--cpu-shares` doesn't prevent containers from being scheduled in Swarm mode. It prioritizes container CPU resources for the available CPU cycles. It doesn't guarantee or reserve any specific CPU access. |

If you have 1 CPU, each of the following commands guarantees the container at most 50% of the CPU every second.

```console
$ docker run -it --cpus=".5" ubuntu /bin/bash
```

Which is the equivalent to manually specifying `--cpu-period` and `--cpu-quota`;

```console
$ docker run -it --cpu-period=100000 --cpu-quota=50000 ubuntu /bin/bash
```

### [Configure the real-time scheduler](#configure-the-real-time-scheduler)

You can configure your container to use the real-time scheduler, for tasks which can't use the CFS scheduler. You need to [make sure the host machine's kernel is configured correctly](#configure-the-host-machines-kernel) before you can [configure the Docker daemon](#configure-the-docker-daemon) or [configure individual containers](#configure-individual-containers).

> Warning
>
> CPU scheduling and prioritization are advanced kernel-level features. Most users don't need to change these values from their defaults. Setting these values incorrectly can cause your host system to become unstable or unusable.

#### [Configure the host machine's kernel](#configure-the-host-machines-kernel)

Verify that `CONFIG_RT_GROUP_SCHED` is enabled in the Linux kernel by running `zcat /proc/config.gz | grep CONFIG_RT_GROUP_SCHED` or by checking for the existence of the file `/sys/fs/cgroup/cpu.rt_runtime_us`. For guidance on configuring the kernel real-time scheduler, consult the documentation for your operating system.

#### [Configure the Docker daemon](#configure-the-docker-daemon)

To run containers using the real-time scheduler, run the Docker daemon with the `--cpu-rt-runtime` flag set to the maximum number of microseconds reserved for real-time tasks per runtime period. For instance, with the default period of 1000000 microseconds (1 second), setting `--cpu-rt-runtime=950000` ensures that containers using the real-time scheduler can run for 950000 microseconds for every 1000000-microsecond period, leaving at least 50000 microseconds available for non-real-time tasks. To make this configuration permanent on systems which use `systemd`, create a systemd unit file for the `docker` service. For example, see the instruction on how to configure the daemon to use a proxy with a [systemd unit file](https://docs.docker.com/engine/daemon/proxy/#systemd-unit-file).

#### [Configure individual containers](#configure-individual-containers)

You can pass several flags to control a container's CPU priority when you start the container using `docker run`. Consult your operating system's documentation or the `ulimit` command for information on appropriate values.

| Option                     | Description                                                                                                                                                                               |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--cap-add=sys_nice`       | Grants the container the `CAP_SYS_NICE` capability, which allows the container to raise process `nice` values, set real-time scheduling policies, set CPU affinity, and other operations. |
| `--cpu-rt-runtime=<value>` | The maximum number of microseconds the container can run at real-time priority within the Docker daemon's real-time scheduler period. You also need the `--cap-add=sys_nice` flag.        |
| `--ulimit rtprio=<value>`  | The maximum real-time priority allowed for the container. You also need the `--cap-add=sys_nice` flag.                                                                                    |

The following example command sets each of these three flags on a `debian:jessie` container.

```console
$ docker run -it \
    --cpu-rt-runtime=950000 \
    --ulimit rtprio=99 \
    --cap-add=sys_nice \
    debian:jessie
```

If the kernel or Docker daemon isn't configured correctly, an error occurs.

## [GPU](#gpu)

For information on how to access NVIDIA GPUs from a container, see [GPU access](https://docs.docker.com/engine/containers/gpu/).

----
url: https://docs.docker.com/guides/vuejs/
----

# Vue.js language-specific guide

Table of contents

***

This guide explains how to containerize Vue.js applications using Docker.

**Time to complete** 20 minutes

The Vue.js language-specific guide shows you how to containerize an Vue.js application using Docker, following best practices for creating efficient, production-ready containers.

[Vue.js](https://vuejs.org/) is a progressive and flexible framework for building modern, interactive web applications. However, as applications scale, managing dependencies, environments, and deployments can become complex. Docker simplifies these challenges by providing a consistent, isolated environment for both development and production.

> **Acknowledgment**
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide. As a Docker Captain and highly skilled Front-end engineer, Kristiyan brings exceptional expertise in modern web development, Docker, and DevOps. His hands-on approach and clear, actionable guidance make this guide an essential resource for developers aiming to build, optimize, and secure Vue.js applications with Docker.

***

## [What will you learn?](#what-will-you-learn)

In this guide, you will learn how to:

* Containerize and run an Vue.js application using Docker.
* Set up a local development environment for Vue.js inside a container.
* Run tests for your Vue.js application within a Docker container.
* Configure a CI/CD pipeline using GitHub Actions for your containerized app.
* Deploy the containerized Vue.js application to a local Kubernetes cluster for testing and debugging.

You'll start by containerizing an existing Vue.js application and work your way up to production-level deployments.

***

## [Prerequisites](#prerequisites)

Before you begin, ensure you have a working knowledge of:

* Basic understanding of [TypeScript](https://www.typescriptlang.org/) and [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript).
* Familiarity with [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm) for managing dependencies and running scripts.
* Familiarity with [Vue.js](https://vuejs.org/) fundamentals.
* Understanding of core Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

Once you've completed the Vue.js getting started modules, you’ll be fully prepared to containerize your own Vue.js application using the detailed examples and best practices outlined in this guide.

## [Modules](#modules)

1. [Containerize](https://docs.docker.com/guides/vuejs/containerize/)

   Learn how to containerize an Vue.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.

2. [Develop your app](https://docs.docker.com/guides/vuejs/develop/)

   Learn how to develop your Vue.js application locally using containers.

3. [Run your tests](https://docs.docker.com/guides/vuejs/run-tests/)

   Learn how to run your vue.js tests in a container.

4. [GitHub Actions CI](https://docs.docker.com/guides/vuejs/configure-github-actions/)

   Learn how to configure CI/CD using GitHub Actions for your Vue.js application.

5. [Test your deployment](https://docs.docker.com/guides/vuejs/deploy/)

   Learn how to deploy locally to test and debug your Kubernetes deployment

----
url: https://docs.docker.com/engine/storage/drivers/zfs-driver/
----

# ZFS storage driver

***

Table of contents

***

ZFS is a next generation filesystem that supports many advanced storage technologies such as volume management, snapshots, checksumming, compression and deduplication, replication and more.

It was created by Sun Microsystems (now Oracle Corporation) and is open sourced under the CDDL license. Due to licensing incompatibilities between the CDDL and GPL, ZFS cannot be shipped as part of the mainline Linux kernel. However, the ZFS On Linux (ZoL) project provides an out-of-tree kernel module and userspace tools which can be installed separately.

The ZFS on Linux (ZoL) port is healthy and maturing. However, at this point in time it is not recommended to use the `zfs` Docker storage driver for production use unless you have substantial experience with ZFS on Linux.

> Note
>
> There is also a FUSE implementation of ZFS on the Linux platform. This is not recommended. The native ZFS driver (ZoL) is more tested, has better performance, and is more widely used. The remainder of this document refers to the native ZoL port.

## [Prerequisites](#prerequisites)

* ZFS requires one or more dedicated block devices, preferably solid-state drives (SSDs).
* The `/var/lib/docker/` directory must be mounted on a ZFS-formatted filesystem.
* Changing the storage driver makes any containers you have already created inaccessible on the local system. Use `docker save` to save containers, and push existing images to Docker Hub or a private repository, so that you do not need to re-create them later.

> Note
>
> There is no need to use `MountFlags=slave` because `dockerd` and `containerd` are in different mount namespaces.

## [Configure Docker with the `zfs` storage driver](#configure-docker-with-the-zfs-storage-driver)

1. Stop Docker.

2. Copy the contents of `/var/lib/docker/` to `/var/lib/docker.bk` and remove the contents of `/var/lib/docker/`.

   ```console
   $ sudo cp -au /var/lib/docker /var/lib/docker.bk

   $ sudo rm -rf /var/lib/docker/*
   ```

3. Create a new `zpool` on your dedicated block device or devices, and mount it into `/var/lib/docker/`. Be sure you have specified the correct devices, because this is a destructive operation. This example adds two devices to the pool.

   ```console
   $ sudo zpool create -f zpool-docker -m /var/lib/docker /dev/xvdf /dev/xvdg
   ```

   The command creates the `zpool` and names it `zpool-docker`. The name is for display purposes only, and you can use a different name. Check that the pool was created and mounted correctly using `zfs list`.

   ```console
   $ sudo zfs list

   NAME           USED  AVAIL  REFER  MOUNTPOINT
   zpool-docker    55K  96.4G    19K  /var/lib/docker
   ```

4. Configure Docker to use `zfs`. Edit `/etc/docker/daemon.json` and set the `storage-driver` to `zfs`. If the file was empty before, it should now look like this:

   ```json
   {
     "storage-driver": "zfs"
   }
   ```

   Save and close the file.

5. Start Docker. Use `docker info` to verify that the storage driver is `zfs`.

   ```console
   $ sudo docker info
     Containers: 0
      Running: 0
      Paused: 0
      Stopped: 0
     Images: 0
     Server Version: 17.03.1-ce
     Storage Driver: zfs
      Zpool: zpool-docker
      Zpool Health: ONLINE
      Parent Dataset: zpool-docker
      Space Used By Parent: 249856
      Space Available: 103498395648
      Parent Quota: no
      Compression: off
   <...>
   ```

## [Manage `zfs`](#manage-zfs)

### [Increase capacity on a running device](#increase-capacity-on-a-running-device)

To increase the size of the `zpool`, you need to add a dedicated block device to the Docker host, and then add it to the `zpool` using the `zpool add` command:

```console
$ sudo zpool add zpool-docker /dev/xvdh
```

### [Limit a container's writable storage quota](#limit-a-containers-writable-storage-quota)

If you want to implement a quota on a per-image/dataset basis, you can set the `size` storage option to limit the amount of space a single container can use for its writable layer.

Edit `/etc/docker/daemon.json` and add the following:

```json
{
  "storage-driver": "zfs",
  "storage-opts": ["size=256M"]
}
```

See all storage options for each storage driver in the [daemon reference documentation](/reference/cli/dockerd/#daemon-storage-driver)

Save and close the file, and restart Docker.

## [How the `zfs` storage driver works](#how-the-zfs-storage-driver-works)

ZFS uses the following objects:

* **filesystems**: thinly provisioned, with space allocated from the `zpool` on demand.
* **snapshots**: read-only space-efficient point-in-time copies of filesystems.
* **clones**: Read-write copies of snapshots. Used for storing the differences from the previous layer.

The process of creating a clone:

1. A read-only snapshot is created from the filesystem.
2. A writable clone is created from the snapshot. This contains any differences from the parent layer.

Filesystems, snapshots, and clones all allocate space from the underlying `zpool`.

### [Image and container layers on-disk](#image-and-container-layers-on-disk)

Each running container's unified filesystem is mounted on a mount point in `/var/lib/docker/zfs/graph/`. Continue reading for an explanation of how the unified filesystem is composed.

### [Image layering and sharing](#image-layering-and-sharing)

The base layer of an image is a ZFS filesystem. Each child layer is a ZFS clone based on a ZFS snapshot of the layer below it. A container is a ZFS clone based on a ZFS Snapshot of the top layer of the image it's created from.

The diagram below shows how this is put together with a running container based on a two-layer image.

When you start a container, the following steps happen in order:

1. The base layer of the image exists on the Docker host as a ZFS filesystem.

2. Additional image layers are clones of the dataset hosting the image layer directly below it.

   In the diagram, "Layer 1" is added by taking a ZFS snapshot of the base layer and then creating a clone from that snapshot. The clone is writable and consumes space on-demand from the zpool. The snapshot is read-only, maintaining the base layer as an immutable object.

3. When the container is launched, a writable layer is added above the image.

   In the diagram, the container's read-write layer is created by making a snapshot of the top layer of the image (Layer 1) and creating a clone from that snapshot.

4. As the container modifies the contents of its writable layer, space is allocated for the blocks that are changed. By default, these blocks are 128k.

## [How container reads and writes work with `zfs`](#how-container-reads-and-writes-work-with-zfs)

### [Reading files](#reading-files)

Each container's writable layer is a ZFS clone which shares all its data with the dataset it was created from (the snapshots of its parent layers). Read operations are fast, even if the data being read is from a deep layer. This diagram illustrates how block sharing works:

### [Writing files](#writing-files)

**Writing a new file**: space is allocated on demand from the underlying `zpool` and the blocks are written directly into the container's writable layer.

**Modifying an existing file**: space is allocated only for the changed blocks, and those blocks are written into the container's writable layer using a copy-on-write (CoW) strategy. This minimizes the size of the layer and increases write performance.

**Deleting a file or directory**:

* When you delete a file or directory that exists in a lower layer, the ZFS driver masks the existence of the file or directory in the container's writable layer, even though the file or directory still exists in the lower read-only layers.
* If you create and then delete a file or directory within the container's writable layer, the blocks are reclaimed by the `zpool`.

## [ZFS and Docker performance](#zfs-and-docker-performance)

There are several factors that influence the performance of Docker using the `zfs` storage driver.

* **Memory**: Memory has a major impact on ZFS performance. ZFS was originally designed for large enterprise-grade servers with a large amount of memory.

* **ZFS Features**: ZFS includes a de-duplication feature. Using this feature may save disk space, but uses a large amount of memory. It is recommended that you disable this feature for the `zpool` you are using with Docker, unless you are using SAN, NAS, or other hardware RAID technologies.

* **ZFS Caching**: ZFS caches disk blocks in a memory structure called the adaptive replacement cache (ARC). The *Single Copy ARC* feature of ZFS allows a single cached copy of a block to be shared by multiple clones of a With this feature, multiple running containers can share a single copy of a cached block. This feature makes ZFS a good option for PaaS and other high-density use cases.

* **Fragmentation**: Fragmentation is a natural byproduct of copy-on-write filesystems like ZFS. ZFS mitigates this by using a small block size of 128k. The ZFS intent log (ZIL) and the coalescing of writes (delayed writes) also help to reduce fragmentation. You can monitor fragmentation using `zpool status`. However, there is no way to defragment ZFS without reformatting and restoring the filesystem.

* **Use the native ZFS driver for Linux**: The ZFS FUSE implementation is not recommended, due to poor performance.

### [Performance best practices](#performance-best-practices)

* **Use fast storage**: Solid-state drives (SSDs) provide faster reads and writes than spinning disks.

* **Use volumes for write-heavy workloads**: Volumes provide the best and most predictable performance for write-heavy workloads. This is because they bypass the storage driver and do not incur any of the potential overheads introduced by thin provisioning and copy-on-write. Volumes have other benefits, such as allowing you to share data among containers and persisting even when no running container is using them.

----
url: https://docs.docker.com/reference/cli/docker/dhi/auth/apk/
----

# docker dhi auth apk

***

| Description | Create authentication details for DHI APK repositories |
| ----------- | ------------------------------------------------------ |
| Usage       | `docker dhi auth apk`                                  |

## [Description](#description)

Create authentication details for DHI APK repositories

----
url: https://docs.docker.com/reference/cli/docker/model/context/use/
----

# docker model context use

***

| Description | Set the active Model Runner context |
| ----------- | ----------------------------------- |
| Usage       | `docker model context use NAME`     |

## [Description](#description)

Set the active Model Runner context. Pass "default" to revert to automatic backend detection.

----
url: https://docs.docker.com/reference/cli/docker/scout/cache/df/
----

# docker scout cache df

***

| Description | Show Docker Scout disk usage |
| ----------- | ---------------------------- |
| Usage       | `docker scout cache df`      |

## [Description](#description)

Docker Scout uses a temporary cache storage for generating image SBOMs. The cache helps avoid regenerating or fetching resources unnecessarily.

This `docker scout cache df` command shows the cached data on the host. Each cache entry is identified by the digest of the image.

You can use the `docker scout cache prune` command to delete cache data at any time.

## [Examples](#examples)

### [List temporary and cache files](#list-temporary-and-cache-files)

```console
$ docker scout cache df
Docker Scout temporary directory to generate SBOMs is located at:
   /var/folders/dw/d6h9w2sx6rv3lzwwgrnx7t5h0000gp/T/docker-scout
   this path can be configured using the DOCKER_SCOUT_CACHE_DIR environment variable

                               Image Digest                               │ Size
──────────────────────────────────────────────────────────────────────────┼────────
  sha256:c41ab5c992deb4fe7e5da09f67a8804a46bd0592bfdf0b1847dde0e0889d2bff │ 21 kB

Total: 21 kB


Docker Scout cached SBOMs are located at:
   /Users/user/.docker/scout/sbom

                               Image Digest                               │ Size of SBOM
──────────────────────────────────────────────────────────────────────────┼───────────────
  sha256:02bb6f428431fbc2809c5d1b41eab5a68350194fb508869a33cb1af4444c9b11 │ 42 kB
  sha256:03fc002fe4f370463a8f04d3a288cdffa861e462fc8b5be44ab62b296ad95183 │ 100 kB
  sha256:088134dd33e4a2997480a1488a41c11abebda465da5cf7f305a0ecf8ed494329 │ 194 kB
  sha256:0b80b2f17aff7ee5bfb135c69d0d6fe34070e89042b7aac73d1abcc79cfe6759 │ 852 kB
  sha256:0c9e8abe31a5f17d84d5c85d3853d2f948a4f126421e89e68753591f1b6fedc5 │ 930 kB
  sha256:0d49cae0723c8d310e413736b5e91e0c59b605ade2546f6e6ef8f1f3ddc76066 │ 510 kB
  sha256:0ef04748d071c2e631bb3edce8f805cb5512e746b682c83fdae6d8c0b243280b │ 1.0 MB
  sha256:13fd22925b638bb7d2131914bb8f8b0f5f582bee364aec682d9e7fe722bb486a │ 42 kB
  sha256:174c41d4fbc7f63e1f2bb7d2f7837318050406f2f27e5073a84a84f18b48b883 │ 115 kB

Total: 4 MB
```

----
url: https://docs.docker.com/guides/frameworks/laravel/
----

# Develop and Deploy Laravel applications with Docker Compose

Table of contents

***

Learn how to efficiently set up Laravel development and production environments using Docker Compose.

**Time to complete** 30 minutes

Laravel is a popular PHP framework that allows developers to build web applications quickly and effectively. Docker Compose simplifies the management of development and production environments by defining essential services, like PHP, a web server, and a database, in a single YAML file. This guide provides a streamlined approach to setting up a robust Laravel environment using Docker Compose, focusing on simplicity and efficiency.

> **Acknowledgment**
>
> Docker would like to thank [Sergei Shitikov](https://github.com/rw4lll) for his contribution to this guide.

The demonstrated examples can be found in [this GitHub repository](https://github.com/dockersamples/laravel-docker-examples). Docker Compose offers a straightforward approach to connecting multiple containers for Laravel, though similar setups can also be achieved using tools like Docker Swarm, Kubernetes, or individual Docker containers.

This guide is intended for educational purposes, helping developers adapt and optimize configurations for their specific use cases. Additionally, there are existing tools that support Laravel in containers:

* [Laravel Sail](https://laravel.com/docs/12.x/sail): An official package for easily starting Laravel in Docker.
* [Laradock](https://github.com/laradock/laradock): A community project that helps run Laravel applications in Docker.

## [What you’ll learn](#what-youll-learn)

* How to use Docker Compose to set up a Laravel development and production environment.
* Defining services that make Laravel development easier, including PHP-FPM, Nginx, and database containers.
* Best practices for managing Laravel environments using containerization.

## [Who’s this for?](#whos-this-for)

* Developers who work with Laravel and want to streamline environment management.
* DevOps engineers seeking efficient ways to manage and deploy Laravel applications.

## [Modules](#modules)

1. [Prerequisites for Setting Up Laravel with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/prerequisites/)

   Ensure you have the required tools and knowledge before setting up Laravel with Docker Compose.

2. [Laravel Production Setup with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/production-setup/)

   Set up a production-ready environment for Laravel using Docker Compose.

3. [Laravel Development Setup with Docker Compose](https://docs.docker.com/guides/frameworks/laravel/development-setup/)

   Set up a Laravel development environment using Docker Compose.

4. [Common Questions on Using Laravel with Docker](https://docs.docker.com/guides/frameworks/laravel/common-questions/)

   Find answers to common questions about setting up and managing Laravel environments with Docker Compose, including troubleshooting and best practices.

----
url: https://docs.docker.com/scout/how-tos/artifact-types/
----

# Use Scout with different artifact types

***

Table of contents

***

Some of the Docker Scout CLI commands support prefixes for specifying the location or type of artifact that you would like to analyze.

By default, image analysis with the `docker scout cves` command targets images in the local image store of the Docker Engine. The following command always uses a local image if it exists:

```console
$ docker scout cves <image>
```

If the image doesn't exist locally, Docker pulls the image before running the analysis. Analyzing the same image again would use the same local version by default, even if the tag has since changed in the registry.

By adding a `registry://` prefix to the image reference, you can force Docker Scout to analyze the registry version of the image:

```console
$ docker scout cves registry://<image>
```

## [Supported prefixes](#supported-prefixes)

The supported prefixes are:

| Prefix               | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| `image://` (default) | Use a local image, or fall back to a registry lookup                 |
| `local://`           | Use an image from the local image store (don't do a registry lookup) |
| `registry://`        | Use an image from a registry (don't use a local image)               |
| `oci-dir://`         | Use an OCI layout directory                                          |
| `archive://`         | Use a tarball archive, as created by `docker save`                   |
| `fs://`              | Use a local directory or file                                        |

You can use prefixes with the following commands:

* `docker scout compare`
* `docker scout cves`
* `docker scout quickview`
* `docker scout recommendations`
* `docker scout sbom`

## [Examples](#examples)

This section contains a few examples showing how you can use prefixes to specify artifacts for `docker scout` commands.

### [Analyze a local project](#analyze-a-local-project)

The `fs://` prefix lets you analyze local source code directly, without having to build it into a container image. The following `docker scout quickview` command gives you an at-a-glance vulnerability summary of the source code in the current working directory:

```console
$ docker scout quickview fs://.
```

To view the details of vulnerabilities found in your local source code, you can use the `docker scout cves --details fs://.` command. Combine it with other flags to narrow down the results to the packages and vulnerabilities that you're interested in.

```console
$ docker scout cves --details --only-severity high fs://.
    ✓ File system read
    ✓ Indexed 323 packages
    ✗ Detected 1 vulnerable package with 1 vulnerability

​## Overview

                    │        Analyzed path
────────────────────┼──────────────────────────────
  Path              │  /Users/david/demo/scoutfs
    vulnerabilities │    0C     1H     0M     0L

​## Packages and Vulnerabilities

   0C     1H     0M     0L  fastify 3.29.0
pkg:npm/fastify@3.29.0

    ✗ HIGH CVE-2022-39288 [OWASP Top Ten 2017 Category A9 - Using Components with Known Vulnerabilities]
      https://scout.docker.com/v/CVE-2022-39288

      fastify is a fast and low overhead web framework, for Node.js. Affected versions of
      fastify are subject to a denial of service via malicious use of the Content-Type
      header. An attacker can send an invalid Content-Type header that can cause the
      application to crash. This issue has been addressed in commit  fbb07e8d  and will be
      included in release version 4.8.1. Users are advised to upgrade. Users unable to
      upgrade may manually filter out http content with malicious Content-Type headers.

      Affected range : <4.8.1
      Fixed version  : 4.8.1
      CVSS Score     : 7.5
      CVSS Vector    : CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H

1 vulnerability found in 1 package
  LOW       0
  MEDIUM    0
  HIGH      1
  CRITICAL  0
```

### [Compare a local project to an image](#compare-a-local-project-to-an-image)

With `docker scout compare`, you can compare the analysis of source code on your local filesystem with the analysis of a container image. The following example compares local source code (`fs://.`) with a registry image `registry://docker/scout-cli:latest`. In this case, both the baseline and target for the comparison use prefixes.

```console
$ docker scout compare fs://. --to registry://docker/scout-cli:latest --ignore-unchanged
WARN 'docker scout compare' is experimental and its behaviour might change in the future
    ✓ File system read
    ✓ Indexed 268 packages
    ✓ SBOM of image already cached, 234 packages indexed


  ## Overview

                           │              Analyzed File System              │              Comparison Image
  ─────────────────────────┼────────────────────────────────────────────────┼─────────────────────────────────────────────
    Path / Image reference │  /Users/david/src/docker/scout-cli-plugin      │  docker/scout-cli:latest
                           │                                                │  bb0b01303584
      platform             │                                                │ linux/arm64
      provenance           │ https://github.com/dvdksn/scout-cli-plugin.git │ https://github.com/docker/scout-cli-plugin
                           │  6ea3f7369dbdfec101ac7c0fa9d78ef05ffa6315      │  67cb4ef78bd69545af0e223ba5fb577b27094505
      vulnerabilities      │    0C     0H     1M     1L                     │    0C     0H     1M     1L
                           │                                                │
      size                 │ 7.4 MB (-14 MB)                                │ 21 MB
      packages             │ 268 (+34)                                      │ 234
                           │                                                │


  ## Packages and Vulnerabilities


    +   55 packages added
    -   21 packages removed
       213 packages unchanged
```

The previous example is truncated for brevity.

### [View the SBOM of an image tarball](#view-the-sbom-of-an-image-tarball)

The following example shows how you can use the `archive://` prefix to get the SBOM of an image tarball, created with `docker save`. The image in this case is `docker/scout-cli:latest`, and the SBOM is exported to file `sbom.spdx.json` in SPDX format.

```console
$ docker pull docker/scout-cli:latest
latest: Pulling from docker/scout-cli
257973a141f5: Download complete 
1f2083724dd1: Download complete 
5c8125a73507: Download complete 
Digest: sha256:13318bb059b0f8b0b87b35ac7050782462b5d0ac3f96f9f23d165d8ed68d0894
$ docker save docker/scout-cli:latest -o scout-cli.tar
$ docker scout sbom --format spdx -o sbom.spdx.json archive://scout-cli.tar
```

## [Learn more](#learn-more)

Read about the commands and supported flags in the CLI reference documentation:

* [`docker scout quickview`](/reference/cli/docker/scout/quickview/)
* [`docker scout cves`](/reference/cli/docker/scout/cves/)
* [`docker scout compare`](/reference/cli/docker/scout/compare/)

----
url: https://docs.docker.com/reference/build-checks/multiple-instructions-disallowed/
----

# MultipleInstructionsDisallowed

***

Table of contents

***

## [Output](#output)

```text
Multiple CMD instructions should not be used in the same stage because only the last one will be used
```

## [Description](#description)

If you have multiple `CMD`, `HEALTHCHECK`, or `ENTRYPOINT` instructions in your Dockerfile, only the last occurrence is used. An image can only ever have one `CMD`, `HEALTHCHECK`, and `ENTRYPOINT`.

## [Examples](#examples)

❌ Bad: Duplicate instructions.

```dockerfile
FROM alpine
ENTRYPOINT ["echo", "Hello, Norway!"]
ENTRYPOINT ["echo", "Hello, Sweden!"]
# Only "Hello, Sweden!" will be printed
```

✅ Good: only one `ENTRYPOINT` instruction.

```dockerfile
FROM alpine
ENTRYPOINT ["echo", "Hello, Norway!\nHello, Sweden!"]
```

You can have both a regular, top-level `CMD` and a separate `CMD` for a `HEALTHCHECK` instruction.

✅ Good: only one top-level `CMD` instruction.

```dockerfile
FROM python:alpine
RUN apk add curl
HEALTHCHECK --interval=1s --timeout=3s \
  CMD ["curl", "-f", "http://localhost:8080"]
CMD ["python", "-m", "http.server", "8080"]
```

----
url: https://docs.docker.com/desktop/features/wsl/best-practices/
----

# WSL 2 best practices for Docker Desktop on Windows

***

Table of contents

***

This page covers recommendations when running Docker Desktop on Windows using WSL 2, including version requirements and file system performance.

## [Keep WSL up to date](#keep-wsl-up-to-date)

Always use the latest version of WSL.

At a minimum you must use WSL version 2.1.5, otherwise Docker Desktop may not work as expected. Additionally, if you intend to use Enhanced Container Isolation, ensure you’re using WSL version 2.6 or later. This is required because ECI depends on a Linux kernel version of at least 6.3.0, and WSL 2.6+ bundles Linux kernel version 6.6. Testing, development, and documentation is based on the newest kernel versions. Older versions of WSL can cause:

* Docker Desktop to hang periodically or when upgrading
* Deployment via SCCM to fail
* The `vmmem.exe` to consume all memory
* Network filter policies to be applied globally, not to specific objects
* GPU failures with containers

## [Optimise file system performance with bind mounts](#optimise-file-system-performance-with-bind-mounts)

To get the best out of the file system performance when bind-mounting files, store source code and other data that is bind-mounted into Linux containers. For instance, use `docker run -v <host-path>:<container-path>` in the Linux file system, rather than the Windows file system. You can also refer to [Microsoft's recommendation](https://learn.microsoft.com/en-us/windows/wsl/compare-versions).

Linux containers only receive file change events, “inotify events”, if the original files are stored in the Linux filesystem. For example, some web development workflows rely on inotify events for automatic reloading when files have changed.

Performance is much higher when files are bind-mounted from the Linux filesystem, rather than accessed from the Windows host filesystem. Therefore avoid `docker run -v /mnt/c/users:/users` where `/mnt/c` is mounted from Windows.

Instead, from a Linux shell use a command like `docker run -v ~/my-project:/sources <my-image>` where `~` is expanded by the Linux shell to `$HOME`.

## [Limit CPU and memory usage](#limit-cpu-and-memory-usage)

If you have concerns about CPU or memory usage, configure limits on the memory, CPU, and swap size allocated to the [WSL 2 utility VM](https://learn.microsoft.com/en-us/windows/wsl/wsl-config#global-configuration-options-with-wslconfig).

----
url: https://docs.docker.com/reference/samples/nginx/
----

# NGINX samples

| Name                                                                                                   | Description                                                                                                                        |
| ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| [Go / NGINX / MySQL](https://github.com/docker/awesome-compose/tree/master/nginx-golang-mysql)         | A sample Go application with an Nginx proxy and a MySQL database.                                                                  |
| [Go / NGINX / PostgreSQL](https://github.com/docker/awesome-compose/tree/master/nginx-golang-postgres) | A sample Go application with an Nginx proxy and a PostgreSQL database.                                                             |
| [NGINX / ASP.NET / MySQL](https://github.com/docker/awesome-compose/tree/master/nginx-aspnet-mysql)    | A sample Nginx reverse proxy with a C# backend using ASP.NET.                                                                      |
| [NGINX / Flask / MongoDB](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mongo)     | A sample Python/Flask application with Nginx proxy and a Mongo database.                                                           |
| [NGINX / Flask / MySQL](https://github.com/docker/awesome-compose/tree/master/nginx-flask-mysql)       | A sample Python/Flask application with an Nginx proxy and a MySQL database.                                                        |
| [NGINX / Node.js / Redis](https://github.com/docker/awesome-compose/tree/master/nginx-nodejs-redis)    | A sample Node.js application with Nginx proxy and a Redis database.                                                                |
| [NGINX / Go](https://github.com/docker/awesome-compose/tree/master/nginx-golang)                       | A sample Nginx proxy with a Go backend.                                                                                            |
| [NGINX / WSGI / Flask](https://github.com/docker/awesome-compose/tree/master/nginx-wsgi-flask)         | A sample Nginx reverse proxy with a Flask backend using WSGI.                                                                      |
| [React / NGINX](https://github.com/docker/awesome-compose/tree/master/react-nginx)                     | A sample React application with Nginx.                                                                                             |
| [atsea-sample-shop-app](https://github.com/dockersamples/atsea-sample-shop-app)                        | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| [linux\_tweet\_app](https://github.com/dockersamples/linux_tweet_app)                                  | A very simple webapp based on NGINX.                                                                                               |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/compose/how-tos/production/
----

# Use Compose in production

***

Table of contents

***

When you define your app with Compose in development, you can use this definition to run your application in different environments such as CI, staging, and production.

The easiest way to deploy an application is to run it on a single server, similar to how you would run your development environment. If you want to scale up your application, you can run Compose apps on a Swarm cluster.

### [Modify your Compose file for production](#modify-your-compose-file-for-production)

You may need to make changes to your app configuration to make it ready for production. These changes might include:

* Removing any volume bindings for application code, so that code stays inside the container and can't be changed from outside
* Binding to different ports on the host
* Setting environment variables differently, such as reducing the verbosity of logging, or to specify settings for external services such as an email server
* Specifying a restart policy like [`restart: always`](https://docs.docker.com/reference/compose-file/services/#restart)to avoid downtime
* Adding extra services such as a log aggregator

For this reason, consider defining an additional Compose file, for example `compose.production.yaml`, with production-specific configuration details. This configuration file only needs to include the changes you want to make from the original Compose file. The additional Compose file is then applied over the original `compose.yaml` to create a new configuration.

Once you have a second configuration file, you can use it with the `-f` option:

```console
$ docker compose -f compose.yaml -f compose.production.yaml up -d
```

See [Using multiple compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/) for a more complete example, and other options.

### [Deploying changes](#deploying-changes)

When you make changes to your app code, remember to rebuild your image and recreate your app's containers. To redeploy a service called `web`, use:

```console
$ docker compose build web
$ docker compose up --no-deps -d web
```

This first command rebuilds the image for `web` and then stops, destroys, and recreates just the `web` service. The `--no-deps` flag prevents Compose from also recreating any services that `web` depends on.

### [Running Compose on a single server](#running-compose-on-a-single-server)

You can use Compose to deploy an app to a remote Docker host by setting the `DOCKER_HOST`, `DOCKER_TLS_VERIFY`, and `DOCKER_CERT_PATH` environment variables appropriately. For more information, see [pre-defined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/).

Once you've set up your environment variables, all the normal `docker compose` commands work with no further configuration.

## [Next steps](#next-steps)

* [Familiarize yourself with Compose's trust model](https://docs.docker.com/compose/trust-model/)
* [Using multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/)

----
url: https://docs.docker.com/dhi/core-concepts/digests/
----

# Image digests

***

Table of contents

***

## [What are Docker image digests?](#what-are-docker-image-digests)

A Docker image digest is a unique, cryptographic identifier (SHA-256 hash) representing the content of a Docker image. Unlike tags, which can be reused or changed, a digest is immutable and ensures that the exact same image is pulled every time. This guarantees consistency across different environments and deployments.

For example, the digest for the `nginx:latest` image might look like:

```text
sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

This digest uniquely identifies the specific version of the `nginx:latest` image, ensuring that any changes to the image content result in a different digest.

## [Why are image digests important?](#why-are-image-digests-important)

Using image digests instead of tags offers several advantages:

* Immutability: Once an image is built and its digest is generated, the content tied to that digest cannot change. This means that if you pull an image using its digest, you can be confident that you are retrieving exactly the same image that was originally built.

* Security: Digests help prevent supply chain attacks by ensuring that the image content has not been tampered with. Even a small change in the image content will result in a completely different digest.

* Consistency: Using digests ensures that the same image is used across different environments, reducing the risk of discrepancies between development, staging, and production environments.

## [Docker Hardened Image digests](#docker-hardened-image-digests)

By using image digests to reference DHIs, you can ensure that your applications are always using the exact same secure image version, enhancing security and compliance

## [View an image digest](#view-an-image-digest)

### [Use the Docker CLI](#use-the-docker-cli)

To view the image digest of a Docker image, you can use the following command. Replace `<image-name>:<tag>` with the image name and tag.

```console
$ docker buildx imagetools inspect <image-name>:<tag>
```

### [Use the Docker Hub UI](#use-the-docker-hub-ui)

1. Go to [Docker Hub](https://hub.docker.com/) and sign in.
2. Navigate to your organization's namespace and open the mirrored DHI repository.
3. Select the **Tags** tab to view image variants.
4. Each tag in the list includes a **Digest** field showing the image's SHA-256 value.

## [Pull an image by digest](#pull-an-image-by-digest)

Pulling an image by digest ensures that you are pulling the exact image version identified by the specified digest.

To pull a Docker image using its digest, use the following command. Replace `<image-name>` with the image name and `<digest>` with the image digest.

```console
$ docker pull <image-name>@sha256:<digest>
```

For example, to pull a `docs/dhi-python:3.13` image using its digest of `94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a`, you would run:

```console
$ docker pull docs/dhi-python@sha256:94a00394bc5a8ef503fb59db0a7d0ae9e1110866e8aee8ba40cd864cea69ea1a
```

## [Multi-platform images and manifests](#multi-platform-images-and-manifests)

Docker Hardened Images are published as multi-platform images, which means a single image tag (like `docs/dhi-python:3.13`) can support multiple operating systems and CPU architectures, such as `linux/amd64`, `linux/arm64`, and more.

Instead of pointing to a single image, a multi-platform tag points to a manifest list (also called an index), which is a higher-level object that references multiple image digests, one for each supported platform.

When you inspect a multi-platform image using `docker buildx imagetools inspect`, you'll see something like this:

```text
Name:      docs/dhi-python:3.13
MediaType: application/vnd.docker.distribution.manifest.list.v2+json
Digest:    sha256:6e05...d231

Manifests:
  Name:        docs/dhi-python:3.13@sha256:94a0...ea1a
  Platform:    linux/amd64
  ...

  Name:        docs/dhi-python:3.13@sha256:7f1d...bc43
  Platform:    linux/arm64
  ...
```

* The manifest list digest (`sha256:6e05...d231`) identifies the overall multi-platform image.
* Each platform-specific image has its own digest (e.g., `sha256:94a0...ea1a` for `linux/amd64`).

### [Why this matters](#why-this-matters)

* Reproducibility: If you're building or running containers on different architectures, using a tag alone will resolve to the appropriate image digest for your platform.
* Verification: You can pull and verify a specific image digest for your platform to ensure you're using the exact image version, not just the manifest list.
* Policy enforcement: When enforcing digest-based policies with Docker Scout, each platform variant is evaluated individually using its digest.

----
url: https://docs.docker.com/reference/api/hub/deprecated/
----

# Deprecated Docker Hub API endpoints

***

Table of contents

***

This page provides an overview of endpoints that are deprecated in Docker Hub API.

***

| Status     | Feature                                                                                              | Date       |
| ---------- | ---------------------------------------------------------------------------------------------------- | ---------- |
| Deprecated | [Deprecate undocumented create/get repository](#deprecate-legacy-createrepository-and-getrepository) | 2025-09-19 |
| Deprecated | [Deprecate /v2/repositories/{namespace}](#deprecate-legacy-listnamespacerepositories)                | 2025-06-27 |
|            | [Create deprecation log table](#create-deprecation-log-table)                                        | 2025-06-27 |
| Removed    | [Docker Hub API v1 deprecation](#docker-hub-api-v1-deprecation)                                      | 2022-08-23 |

***

### [Deprecate legacy CreateRepository and GetRepository](#deprecate-legacy-createrepository-and-getrepository)

Deprecate undocumented endpoints :

* `POST /v2/repositories` and `POST /v2/repositories/{namespace}` replaced by [Create repository](/reference/api/hub/latest/#tag/repositories/operation/CreateRepository).
* `GET /v2/repositories/{namespace}/{repository}` replaced by [Get repository](/reference/api/hub/latest/#tag/repositories/operation/GetRepository).
* `HEAD /v2/repositories/{namespace}/{repository}` replaced by [Check repository](/reference/api/hub/latest/#tag/repositories/operation/CheckRepository).

***

### [Deprecate legacy ListNamespaceRepositories](#deprecate-legacy-listnamespacerepositories)

Deprecate undocumented endpoint `GET /v2/repositories/{namespace}` replaced by [List repositories](/reference/api/hub/latest/#tag/repositories/operation/listNamespaceRepositories).

***

### [Create deprecation log table](#create-deprecation-log-table)

Reformat page

***

### [Docker Hub API v1 deprecation](#docker-hub-api-v1-deprecation)

Docker Hub API v1 has been deprecated. Use Docker Hub API v2 instead.

The following API routes within the v1 path will no longer work and will return a 410 status code:

* `/v1/repositories/{name}/images`
* `/v1/repositories/{name}/tags`
* `/v1/repositories/{name}/tags/{tag_name}`
* `/v1/repositories/{namespace}/{name}/images`
* `/v1/repositories/{namespace}/{name}/tags`
* `/v1/repositories/{namespace}/{name}/tags/{tag_name}`

If you want to continue using the Docker Hub API in your current applications, update your clients to use v2 endpoints.

| **OLD**                                                                                                                                                               | **NEW**                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| [/v1/repositories/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#list-repository-tags)                                      | [/v2/namespaces/{namespace}/repositories/{repository}/tags](/reference/api/hub/latest/#tag/repositories/operation/ListRepositoryTags)     |
| [/v1/repositories/{namespace}/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#list-repository-tags)                          | [/v2/namespaces/{namespace}/repositories/{repository}/tags](/reference/api/hub/latest.md/#tag/repositories/operation/ListRepositoryTags)  |
| [/v1/repositories/{namespace}/{name}/tags](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#get-image-id-for-a-particular-tag)             | [/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}](/reference/api/hub/latest/#tag/repositories/operation/GetRepositoryTag) |
| [/v1/repositories/{namespace}/{name}/tags/{tag\_name}](https://github.com/moby/moby/blob/v1.8.3/docs/reference/api/registry_api.md#get-image-id-for-a-particular-tag) | [/v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}](/reference/api/hub/latest/#tag/repositories/operation/GetRepositoryTag) |

***

----
url: https://docs.docker.com/guides/docker-scout/why/
----

# Why Docker Scout?

***

***

Organizations face significant challenges from data breaches, including financial losses, operational disruptions, and long-term damage to brand reputation and customer trust. Docker Scout addresses critical problems such as identifying insecure container images, preventing security breaches, and reducing the risk of operational downtime due to vulnerabilities.

Docker Scout provides several benefits:

* Secure and trusted content
* A system of record for your Software Development Lifecycle (SDLC)
* Continuous security posture improvement

Docker Scout offers automated vulnerability detection and remediation, helping organizations identify and fix security issues in container images early in the development process. It also integrates with popular development tools like Docker Desktop and GitHub Actions, providing seamless security management and compliance checks within existing workflows.

[Docker Scout demo »](https://docs.docker.com/guides/docker-scout/demo/)

----
url: https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/known-issues/
----

# Known issues

***

***

* The Mac Activity Monitor reports that Docker is using twice the amount of memory it's actually using. This is due to a [bug in macOS](https://docs.google.com/document/d/17ZiQC1Tp9iH320K-uqVLyiJmk4DHJ3c4zgQetJiKYQM/edit?usp=sharing).

* **"Docker.app is damaged" dialog**: If you see a "Docker.app is damaged and can't be opened" dialog during installation or updates, this is typically caused by non-atomic copy operations when other applications are using the Docker CLI. See [Fix "Docker.app is damaged" on macOS](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/mac-damaged-dialog/) for resolution steps.

* Force-ejecting the `.dmg` after running `Docker.app` from it can cause the whale icon to become unresponsive, Docker tasks to show as not responding in the Activity Monitor, and for some processes to consume a large amount of CPU resources. Reboot and restart Docker to resolve these issues.

* Docker Desktop uses the `HyperKit` hypervisor (<https://github.com/docker/hyperkit>) in macOS 10.10 Yosemite and higher. If you are developing with tools that have conflicts with `HyperKit`, such as [Intel Hardware Accelerated Execution Manager (HAXM)](https://software.intel.com/en-us/android/articles/intel-hardware-accelerated-execution-manager/), the current workaround is not to run them at the same time. You can pause `HyperKit` by quitting Docker Desktop temporarily while you work with HAXM. This allows you to continue work with the other tools and prevent `HyperKit` from interfering.

* If you are working with applications like [Apache Maven](https://maven.apache.org/) that expect settings for `DOCKER_HOST` and `DOCKER_CERT_PATH` environment variables, specify these to connect to Docker instances through Unix sockets. For example:

  ```console
  $ export DOCKER_HOST=unix:///var/run/docker.sock
  ```

- Some command line tools do not work when Rosetta 2 is not installed.

  * The old version 1.x of `docker-compose`. Use Compose V2 instead - type `docker compose`.
  * The `docker-credential-ecr-login` credential helper.

- Some images do not support the ARM64 architecture. You can add `--platform linux/amd64` to run (or build) an Intel image using emulation.

  However, attempts to run Intel-based containers on Apple silicon machines under emulation can crash as QEMU sometimes fails to run the container. In addition, filesystem change notification APIs (`inotify`) do not work under QEMU emulation. Even when the containers do run correctly under emulation, they will be slower and use more memory than the native equivalent.

  In summary, running Intel-based containers on Arm-based machines should be regarded as "best effort" only. We recommend running `arm64` containers on Apple silicon machines whenever possible, and encouraging container authors to produce `arm64`, or multi-arch, versions of their containers. This issue should become less common over time, as more and more images are rebuilt [supporting multiple architectures](https://www.docker.com/blog/multi-arch-build-and-images-the-simple-way/).

- Users may occasionally experience data drop when a TCP stream is half-closed.

----
url: https://docs.docker.com/dhi/core-concepts/
----

# Core concepts

***

Table of contents

***

Docker Hardened Images (DHIs) are built on a foundation of secure software supply chain practices. This section explains the core concepts behind that foundation, from signed attestations and immutable digests to standards like SLSA and VEX.

Start here if you want to understand how Docker Hardened Images support compliance, transparency, and security.

## [Security metadata and attestations](#security-metadata-and-attestations)

### [Attestations](/dhi/core-concepts/attestations/)

[Review the full set of signed attestations included with each Docker Hardened Image, such as SBOMs, VEX, build provenance, and scan results.](/dhi/core-concepts/attestations/)

### [Software Bill of Materials (SBOMs)](/dhi/core-concepts/sbom/)

[Learn what SBOMs are, why they matter, and how Docker Hardened Images include signed SBOMs to support transparency and compliance.](/dhi/core-concepts/sbom/)

### [Supply-chain Levels for Software Artifacts (SLSA)](/dhi/core-concepts/slsa/)

[Learn how Docker Hardened Images comply with SLSA Build Level 3 and how to verify provenance for secure, tamper-resistant builds.](/dhi/core-concepts/slsa/)

### [Image provenance](/dhi/core-concepts/provenance/)

[Learn how build provenance metadata helps trace the origin of Docker Hardened Images and support compliance with SLSA.](/dhi/core-concepts/provenance/)

## [Compliance standards](#compliance-standards)

### [FIPS](/dhi/core-concepts/fips/)

[Learn how Docker Hardened Images support FIPS 140 by using validated cryptographic modules and providing signed attestations for compliance audits.](/dhi/core-concepts/fips/)

### [STIG](/dhi/core-concepts/stig/)

[Learn how Docker Hardened Images provide STIG-ready container images with verifiable security scan attestations for government and enterprise compliance requirements.](/dhi/core-concepts/stig/)

### [CIS Benchmarks](/dhi/core-concepts/cis/)

[Learn how Docker Hardened Images help you meet Center for Internet Security (CIS) Docker Benchmark requirements for secure container configuration and deployment.](/dhi/core-concepts/cis/)

## [Vulnerability and risk management](#vulnerability-and-risk-management)

### [Common Vulnerabilities and Exposures (CVEs)](/dhi/core-concepts/cves/)

[Understand what CVEs are, how Docker Hardened Images reduce exposure, and how to scan images for vulnerabilities using popular tools.](/dhi/core-concepts/cves/)

### [Vulnerability Exploitability eXchange (VEX)](/dhi/core-concepts/vex/)

[Learn how VEX helps you prioritize real risks by identifying which vulnerabilities in Docker Hardened Images are actually exploitable.](/dhi/core-concepts/vex/)

### [Software Supply Chain Security](/dhi/core-concepts/sscs/)

[Learn how Docker Hardened Images help secure every stage of your software supply chain with signed metadata, provenance, and minimal attack surface.](/dhi/core-concepts/sscs/)

### [Secure Software Development Lifecycle (SSDLC)](/dhi/core-concepts/ssdlc/)

[See how Docker Hardened Images support a secure SDLC by integrating with scanning, signing, and debugging tools.](/dhi/core-concepts/ssdlc/)

## [Image structure and behavior](#image-structure-and-behavior)

### [Distroless images](/dhi/core-concepts/distroless/)

[Learn how Docker Hardened Images use distroless variants to minimize attack surface and remove unnecessary components.](/dhi/core-concepts/distroless/)

### [glibc and musl support in Docker Hardened Images](/dhi/core-concepts/glibc-musl/)

[Compare glibc and musl variants of DHIs to choose the right base image for your application’s compatibility, size, and performance needs.](/dhi/core-concepts/glibc-musl/)

### [Image immutability](/dhi/core-concepts/immutability/)

[Understand how image digests, read-only containers, and signed metadata ensure Docker Hardened Images are tamper-resistant and immutable.](/dhi/core-concepts/immutability/)

### [Image hardening](/dhi/core-concepts/hardening/)

[Learn how Docker Hardened Images are designed for security, with minimal components, nonroot execution, and secure-by-default configurations.](/dhi/core-concepts/hardening/)

## [Verification and traceability](#verification-and-traceability)

### [Digests](/dhi/core-concepts/digests/)

[Learn how to use immutable image digests to guarantee consistency and verify the exact Docker Hardened Image you're running.](/dhi/core-concepts/digests/)

### [Code signing](/dhi/core-concepts/signatures/)

[Understand how Docker Hardened Images are cryptographically signed using Cosign to verify authenticity, integrity, and secure provenance.](/dhi/core-concepts/signatures/)

----
url: https://docs.docker.com/enterprise/security/provisioning/scim/migrate-scim/
----

# Migrate JIT to SCIM

***

Table of contents

***

If you already have users provisioned through Just-in-Time (JIT) and want to enable full SCIM lifecycle management, you need to migrate them. Users originally created by JIT cannot be automatically de-provisioned through SCIM, even after SCIM is enabled.

## [Why migrate](#why-migrate)

Organizations using JIT provisioning may encounter limitations with user lifecycle management, particularly around de-provisioning. Migrating to SCIM provides:

* Automatic user de-provisioning when users leave your organization. This is the primary benefit for large organizations that need full automation.
* Continuous synchronization of user attributes
* Centralized user management through your identity provider
* Enhanced security through automated access control

> Important
>
> Users originally created through JIT provisioning cannot be automatically de-provisioned by SCIM, even after SCIM is enabled. To enable full lifecycle management including automatic de-provisioning through your identity provider, you must manually remove these users so SCIM can re-create them with proper lifecycle management capabilities.

This migration is most critical for larger organizations that require fully automated user de-provisioning when employees leave the company.

## [Prerequisites](#prerequisites)

Before migrating, ensure you have:

* SCIM configured and tested in your organization
* A maintenance window for the migration

> Warning
>
> This migration temporarily disrupts user access. Plan to perform this migration during a low-usage window and communicate the timeline to affected users.

## [Prepare for migration](#prepare-for-migration)

### [Transfer ownership](#transfer-ownership)

Before removing users, ensure that any repositories, teams, or organization resources they own are transferred to another administrator or service account. When a user is removed from the organization, any resources they own may become inaccessible.

1. Review repositories, organization resources, and team ownership for affected users.
2. Transfer ownership to another administrator.

> Warning
>
> If ownership is not transferred, repositories owned by removed users may become inaccessible when the user is removed. Ensure all critical resources are transferred before proceeding.

### [Verify identity provider configuration](#verify-identity-provider-configuration)

1. Confirm all JIT-provisioned users are assigned to the Docker application in your identity provider.
2. Verify identity provider group to Docker Team mappings are configured and tested.

Users not assigned to the Docker application in your identity provider are not re-created by SCIM after removal.

### [Export user records](#export-user-records)

Export a list of JIT-provisioned users from Docker Admin Console:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.
2. Select **Admin Console**, then **Members**.
3. Select **Export members** to download the member list as CSV for backup and reference.

Keep this CSV list of JIT-provisioned users as a rollback reference if needed.

## [Complete the migration](#complete-the-migration)

### [Disable JIT provisioning](#disable-jit-provisioning)

> Important
>
> Before disabling JIT, ensure SCIM is fully configured and tested in your organization. Do not disable JIT until you have verified SCIM is working correctly.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.
2. Select **Admin Console**, then **SSO and SCIM**.
3. In the SSO connections table, select the **Actions** menu for your connection.
4. Select **Disable JIT provisioning**.
5. Select **Disable** to confirm.

Disabling JIT prevents new users from being automatically added through SSO during the migration.

### [Remove JIT-origin users](#remove-jit-origin-users)

> Important
>
> Users originally created through JIT provisioning cannot be automatically de-provisioned by SCIM, even after SCIM is enabled. To enable full lifecycle management including automatic de-provisioning through your identity provider, you must manually remove these users so SCIM can re-create them with proper lifecycle management capabilities.

This step is most critical for large organizations that require fully automated user de-provisioning when employees leave the company.

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.
2. Select **Admin Console**, then **Members**.
3. Identify and remove JIT-provisioned users in manageable batches.
4. Monitor for any errors during removal.

> Tip
>
> To efficiently identify JIT users, compare the member list exported before SCIM was enabled with the current member list. Users who existed before SCIM was enabled were likely provisioned via JIT.

### [Verify SCIM re-provisioning](#verify-scim-re-provisioning)

After removing JIT users, SCIM automatically re-creates user accounts:

1. In your identity provider system log, confirm "create app user" events for Docker.
2. In Docker Admin Console, confirm users reappear with SCIM provisioning.
3. Verify users are added to the correct teams via group mapping.

### [Validate user access](#validate-user-access)

Perform post-migration validation:

1. Select a subset of migrated users to test sign-in and access.
2. Verify team membership matches identity provider group assignments.
3. Confirm repository access is restored.
4. Test that de-provisioning works correctly by removing a test user from your identity provider.

Keep audit exports and logs for compliance purposes.

## [Migration results](#migration-results)

After completing the migration:

* All users in your organization are SCIM-provisioned
* User de-provisioning works reliably through your identity provider
* No new JIT users are created
* Consistent identity lifecycle management is maintained

## [Troubleshoot migration issues](#troubleshoot-migration-issues)

If a user fails to reappear after removal:

1. Check that the user is assigned to the Docker application in your identity provider.
2. Verify SCIM is enabled in both Docker and your identity provider.
3. Trigger a manual SCIM sync in your identity provider.
4. Check provisioning logs in your identity provider for errors.

For more troubleshooting guidance, see [Troubleshoot provisioning](https://docs.docker.com/enterprise/security/provisioning/troubleshoot-provisioning/).

## [Next steps](#next-steps)

* Set up [Group mapping](https://docs.docker.com/enterprise/security/provisioning/scim/group-mapping/).
* [Assign roles](https://docs.docker.com/enterprise/security/roles-and-permissions/core-roles/) to members of your org.
* [Enforce sign in](https://docs.docker.com/enterprise/security/enforce-sign-in/), if needed.

----
url: https://docs.docker.com/reference/cli/docker/desktop/
----

# docker desktop

***

| Description | Docker Desktop   |
| ----------- | ---------------- |
| Usage       | `docker desktop` |

## [Description](#description)

Control Docker Desktop from the CLI

## [Subcommands](#subcommands)

| Command                                                                                         | Description                                            |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------ |
| [`docker desktop diagnose`](https://docs.docker.com/reference/cli/docker/desktop/diagnose/)     | Diagnose Docker Desktop issues                         |
| [`docker desktop disable`](https://docs.docker.com/reference/cli/docker/desktop/disable/)       | Disable a feature                                      |
| [`docker desktop enable`](https://docs.docker.com/reference/cli/docker/desktop/enable/)         | Enable a feature                                       |
| [`docker desktop engine`](https://docs.docker.com/reference/cli/docker/desktop/engine/)         | Commands to list and switch containers (Windows only)  |
| [`docker desktop kubernetes`](https://docs.docker.com/reference/cli/docker/desktop/kubernetes/) | Manage Kubernetes settings                             |
| [`docker desktop logs`](https://docs.docker.com/reference/cli/docker/desktop/logs/)             | Print log entries for Docker Desktop                   |
| [`docker desktop restart`](https://docs.docker.com/reference/cli/docker/desktop/restart/)       | Restart Docker Desktop                                 |
| [`docker desktop start`](https://docs.docker.com/reference/cli/docker/desktop/start/)           | Start Docker Desktop                                   |
| [`docker desktop status`](https://docs.docker.com/reference/cli/docker/desktop/status/)         | Display Docker Desktop's status                        |
| [`docker desktop stop`](https://docs.docker.com/reference/cli/docker/desktop/stop/)             | Stop Docker Desktop                                    |
| [`docker desktop update`](https://docs.docker.com/reference/cli/docker/desktop/update/)         | Manage Docker Desktop updates                          |
| [`docker desktop version`](https://docs.docker.com/reference/cli/docker/desktop/version/)       | Show the Docker Desktop CLI plugin version information |

----
url: https://docs.docker.com/extensions/extensions-sdk/guides/use-docker-socket-from-backend/
----

# Use the Docker socket from the extension backend

***

***

Extensions can invoke Docker commands directly from the frontend with the SDK.

In some cases, it is useful to also interact with Docker Engine from the backend.

Extension backend containers can mount the Docker socket and use it to interact with Docker Engine from the extension backend logic. Learn more about the [Docker Engine socket](/reference/cli/dockerd/#examples)

However, when mounting the Docker socket from an extension container that lives in the Desktop virtual machine, you want to mount the Docker socket from inside the VM, and not mount `/var/run/docker.sock` from the host filesystem (using the Docker socket from the host can lead to permission issues in containers).

In order to do so, you can use `/var/run/docker.sock.raw`. Docker Desktop mounts the socket that lives in the Desktop VM, and not from the host.

```yaml
services:
  myExtension:
    image: ${DESKTOP_PLUGIN_IMAGE}
    volumes:
      - /var/run/docker.sock.raw:/var/run/docker.sock
```

----
url: https://docs.docker.com/reference/
----

# Reference documentation

***

***

This section includes the reference documentation for the Docker platform's various APIs, CLIs, drivers and specifications, and file formats.

## [File formats](#file-formats)

### [Dockerfile](/reference/dockerfile/)

[Defines the contents and startup behavior of a single container.](/reference/dockerfile/)

### [Compose file](/reference/compose-file/)

[Defines a multi-container application.](/reference/compose-file/)

## [Command-line interfaces (CLIs)](#command-line-interfaces-clis)

### [Docker CLI](/reference/cli/docker/)

[The main Docker CLI, includes all `docker` commands.](/reference/cli/docker/)

### [Compose CLI](/reference/cli/docker/compose/)

[The CLI for Docker Compose, for building and running multi-container applications.](/reference/cli/docker/compose/)

### [Daemon CLI (dockerd)](/reference/cli/dockerd/)

[Persistent process that manages containers.](/reference/cli/dockerd/)

## [Application programming interfaces (APIs)](#application-programming-interfaces-apis)

### [Engine API](/reference/api/engine/)

[The main API for Docker, provides programmatic access to a daemon.](/reference/api/engine/)

### [Docker Hub API](/reference/api/hub/latest/)

[API to interact with Docker Hub.](/reference/api/hub/latest/)

### [DVP Data API](/reference/api/dvp/latest/)

[API for Docker Verified Publishers to fetch analytics data.](/reference/api/dvp/latest/)

### [Registry API](/reference/api/registry/latest/)

[API for Docker Registry.](/reference/api/registry/latest/)

----
url: https://docs.docker.com/guides/bun/develop/
----

# Use containers for Bun development

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Containerize a Bun application](https://docs.docker.com/guides/bun/containerize/).

## [Overview](#overview)

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

* Configuring Compose to automatically update your running Compose services as you edit and save your code

## [Get the sample application](#get-the-sample-application)

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/dockersamples/bun-docker.git && cd bun-docker
```

## [Automatically update services](#automatically-update-services)

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yml` file in an IDE or text editor and then add the Compose Watch instructions. The following example shows how to add Compose Watch to your `compose.yml` file.

|                                             |                                                                                                                                                                                                                     |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ```
``` | ```yaml
services:
  server:
    image: bun-server
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    develop:
      watch:
        - action: rebuild
          path: .
``` |

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Now, if you modify your `server.js` you will see the changes in real time without re-building the image.

To test it out, open the `server.js` file in your favorite text editor and change the message from `{"Status" : "OK"}` to `{"Status" : "Updated"}`. Save the file and refresh your browser at `http://localhost:3000`. You should see the updated message.

[Configure CI/CD for your Bun application »](https://docs.docker.com/guides/bun/configure-ci-cd/)

----
url: https://docs.docker.com/build/building/variables/
----

# Build variables

***

Table of contents

***

In Docker Build, build arguments (`ARG`) and environment variables (`ENV`) both serve as a means to pass information into the build process. You can use them to parameterize the build, allowing for more flexible and configurable builds.

> Warning
>
> Build arguments and environment variables are inappropriate for passing secrets to your build, because they're exposed in the final image. Instead, use secret mounts or SSH mounts, which expose secrets to your builds securely.
>
> See [Build secrets](https://docs.docker.com/build/building/secrets/) for more information.

## [Similarities and differences](#similarities-and-differences)

Build arguments and environment variables are similar. They're both declared in the Dockerfile and can be set using flags for the `docker build` command. Both can be used to parameterize the build. But they each serve a distinct purpose.

### [Build arguments](#build-arguments)

Build arguments are variables for the Dockerfile itself. Use them to parameterize values of Dockerfile instructions. For example, you might use a build argument to specify the version of a dependency to install.

Build arguments have no effect on the build unless it's used in an instruction. They're not accessible or present in containers instantiated from the image unless explicitly passed through from the Dockerfile into the image filesystem or configuration. They may persist in the image metadata, as provenance attestations and in the image history, which is why they're not suitable for holding secrets.

They make Dockerfiles more flexible, and easier to maintain.

For an example on how you can use build arguments, see [`ARG` usage example](#arg-usage-example).

### [Environment variables](#environment-variables)

Environment variables are passed through to the build execution environment, and persist in containers instantiated from the image.

Environment variables are primarily used to:

* Configure the execution environment for builds
* Set default environment variables for containers

Environment variables, if set, can directly influence the execution of your build, and the behavior or configuration of the application.

You can't override or set an environment variable at build-time. Values for environment variables must be declared in the Dockerfile. You can combine environment variables and build arguments to allow environment variables to be configured at build-time.

For an example on how to use environment variables for configuring builds, see [`ENV` usage example](#env-usage-example).

## [`ARG` usage example](#arg-usage-example)

Build arguments are commonly used to specify versions of components, such as image variants or package versions, used in a build.

Specifying versions as build arguments lets you build with different versions without having to manually update the Dockerfile. It also makes it easier to maintain the Dockerfile, since it lets you declare versions at the top of the file.

Build arguments can also be a way to reuse a value in multiple places. For example, if you use multiple flavors of `alpine` in your build, you can ensure you're using the same version of `alpine` everywhere:

* `golang:1.22-alpine${ALPINE_VERSION}`
* `python:3.12-alpine${ALPINE_VERSION}`
* `nginx:1-alpine${ALPINE_VERSION}`

The following example defines the version of `node` and `alpine` using build arguments.

```dockerfile
# syntax=docker/dockerfile:1

ARG NODE_VERSION="24"
ARG ALPINE_VERSION="3.23"

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION} AS base
WORKDIR /src

FROM base AS build
COPY package*.json ./
RUN npm ci
RUN npm run build

FROM base AS production
COPY package*.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY --from=build /src/dist/ .
CMD ["node", "app.js"]
```

In this case, the build arguments have default values. Specifying their values when you invoke a build is optional. To override the defaults, you would use the `--build-arg` CLI flag:

```console
$ docker build --build-arg NODE_VERSION=current .
```

For more information on how to use build arguments, refer to:

* [`ARG` Dockerfile reference](https://docs.docker.com/reference/dockerfile/#arg)
* [`docker build --build-arg` reference](/reference/cli/docker/buildx/build/#build-arg)

## [`ENV` usage example](#env-usage-example)

Declaring an environment variable with `ENV` makes the variable available to all subsequent instructions in the build stage. The following example shows an example setting `NODE_ENV` to `production` before installing JavaScript dependencies with `npm`. Setting the variable makes `npm` omits packages needed only for local development.

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
WORKDIR /app
COPY package*.json ./
ENV NODE_ENV=production
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

Environment variables aren't configurable at build-time by default. If you want to change the value of an `ENV` at build-time, you can combine environment variables and build arguments:

```dockerfile
# syntax=docker/dockerfile:1

FROM node:20
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV
WORKDIR /app
COPY package*.json ./
RUN npm ci && npm cache clean --force
COPY . .
CMD ["node", "app.js"]
```

With this Dockerfile, you can use `--build-arg` to override the default value of `NODE_ENV`:

```console
$ docker build --build-arg NODE_ENV=development .
```

Note that, because the environment variables you set persist in containers, using them can lead to unintended side-effects for the application's runtime.

For more information on how to use environment variables in builds, refer to:

* [`ENV` Dockerfile reference](https://docs.docker.com/reference/dockerfile/#env)

## [Scoping](#scoping)

Build arguments declared in the global scope of a Dockerfile aren't automatically inherited into the build stages. They're only accessible in the global scope.

```dockerfile
# syntax=docker/dockerfile:1

# The following build argument is declared in the global scope:
ARG NAME="joe"

FROM alpine
# The following instruction doesn't have access to the $NAME build argument
# because the argument was defined in the global scope, not for this stage.
RUN echo "hello ${NAME}!"
```

The `echo` command in this example evaluates to `hello !` because the value of the `NAME` build argument is out of scope. To inherit global build arguments into a stage, you must consume them:

```dockerfile
# syntax=docker/dockerfile:1

# Declare the build argument in the global scope
ARG NAME="joe"

FROM alpine
# Consume the build argument in the build stage
ARG NAME
RUN echo $NAME
```

Once a build argument is declared or consumed in a stage, it's automatically inherited by child stages.

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine AS base
# Declare the build argument in the build stage
ARG NAME="joe"

# Create a new stage based on "base"
FROM base AS build
# The NAME build argument is available here
# since it's declared in a parent stage
RUN echo "hello $NAME!"
```

The following diagram further exemplifies how build argument and environment variable inheritance works for multi-stage builds.

## [Pre-defined build arguments](#pre-defined-build-arguments)

This section describes pre-defined build arguments available to all builds by default.

### [Multi-platform build arguments](#multi-platform-build-arguments)

Multi-platform build arguments describe the build and target platforms for the build.

The build platform is the operating system, architecture, and platform variant of the host system where the builder (the BuildKit daemon) is running.

* `BUILDPLATFORM`
* `BUILDOS`
* `BUILDARCH`
* `BUILDVARIANT`

The target platform arguments hold the same values for the target platforms for the build, specified using the `--platform` flag for the `docker build` command.

* `TARGETPLATFORM`
* `TARGETOS`
* `TARGETARCH`
* `TARGETVARIANT`

These arguments are useful for doing cross-compilation in multi-platform builds. They're available in the global scope of the Dockerfile, but they aren't automatically inherited by build stages. To use them inside stage, you must declare them:

```dockerfile
# syntax=docker/dockerfile:1

# Pre-defined build arguments are available in the global scope
FROM --platform=$BUILDPLATFORM golang
# To inherit them to a stage, declare them with ARG
ARG TARGETOS
RUN GOOS=$TARGETOS go build -o ./exe .
```

For more information about multi-platform build arguments, refer to [Multi-platform arguments](https://docs.docker.com/reference/dockerfile/#automatic-platform-args-in-the-global-scope)

### [Proxy arguments](#proxy-arguments)

Proxy build arguments let you specify proxies to use for your build. You don't need to declare or reference these arguments in the Dockerfile. Specifying a proxy with `--build-arg` is enough to make your build use the proxy.

Proxy arguments are automatically excluded from the build cache and the output of `docker history` by default. If you do reference the arguments in your Dockerfile, the proxy configuration ends up in the build cache.

The builder respects the following proxy build arguments. The variables are case insensitive.

* `HTTP_PROXY`
* `HTTPS_PROXY`
* `FTP_PROXY`
* `NO_PROXY`
* `ALL_PROXY`

To configure a proxy for your build:

```console
$ docker build --build-arg HTTP_PROXY=https://my-proxy.example.com .
```

For more information about proxy build arguments, refer to [Proxy arguments](https://docs.docker.com/reference/dockerfile/#predefined-args).

## [Build tool configuration variables](#build-tool-configuration-variables)

The following environment variables enable, disable, or change the behavior of Buildx and BuildKit. Note that these variables aren't used to configure the build container; they aren't available inside the build and they have no relation to the `ENV` instruction. They're used to configure the Buildx client, or the BuildKit daemon.

| Variable                                                                       | Type              | Description                                                     |
| ------------------------------------------------------------------------------ | ----------------- | --------------------------------------------------------------- |
| [BUILDKIT\_COLORS](#buildkit_colors)                                           | String            | Configure text color for the terminal output.                   |
| [BUILDKIT\_HOST](#buildkit_host)                                               | String            | Specify host to use for remote builders.                        |
| [BUILDKIT\_PROGRESS](#buildkit_progress)                                       | String            | Configure type of progress output.                              |
| [BUILDKIT\_TTY\_LOG\_LINES](#buildkit_tty_log_lines)                           | String            | Number of log lines (for active steps in TTY mode).             |
| [BUILDX\_BAKE\_FILE](#buildx_bake_file)                                        | String            | Specify the build definition file(s) for `docker buildx bake`.  |
| [BUILDX\_BAKE\_FILE\_SEPARATOR](#buildx_bake_file_separator)                   | String            | Specify the file-path separator for `BUILDX_BAKE_FILE`.         |
| [BUILDX\_BAKE\_GIT\_AUTH\_HEADER](#buildx_bake_git_auth_header)                | String            | HTTP authentication scheme for remote Bake files.               |
| [BUILDX\_BAKE\_GIT\_AUTH\_TOKEN](#buildx_bake_git_auth_token)                  | String            | HTTP authentication token for remote Bake files.                |
| [BUILDX\_BAKE\_GIT\_SSH](#buildx_bake_git_ssh)                                 | String            | SSH authentication for remote Bake files.                       |
| [BUILDX\_BUILDER](#buildx_builder)                                             | String            | Specify the builder instance to use.                            |
| [BUILDX\_CONFIG](#buildx_config)                                               | String            | Specify location for configuration, state, and logs.            |
| [BUILDX\_CPU\_PROFILE](#buildx_cpu_profile)                                    | String            | Generate a `pprof` CPU profile at the specified location.       |
| [BUILDX\_EXPERIMENTAL](#buildx_experimental)                                   | Boolean           | Turn on experimental features.                                  |
| [BUILDX\_GIT\_CHECK\_DIRTY](#buildx_git_check_dirty)                           | Boolean           | Enable dirty Git checkout detection.                            |
| [BUILDX\_GIT\_INFO](#buildx_git_info)                                          | Boolean           | Remove Git information in provenance attestations.              |
| [BUILDX\_GIT\_LABELS](#buildx_git_labels)                                      | String \| Boolean | Add Git provenance labels to images.                            |
| [BUILDX\_MEM\_PROFILE](#buildx_mem_profile)                                    | String            | Generate a `pprof` memory profile at the specified location.    |
| [BUILDX\_METADATA\_PROVENANCE](#buildx_metadata_provenance)                    | String \| Boolean | Customize provenance information included in the metadata file. |
| [BUILDX\_METADATA\_WARNINGS](#buildx_metadata_warnings)                        | String            | Include build warnings in the metadata file.                    |
| [BUILDX\_NO\_DEFAULT\_ATTESTATIONS](#buildx_no_default_attestations)           | Boolean           | Turn off default provenance attestations.                       |
| [BUILDX\_NO\_DEFAULT\_LOAD](#buildx_no_default_load)                           | Boolean           | Turn off loading images to image store by default.              |
| [EXPERIMENTAL\_BUILDKIT\_SOURCE\_POLICY](#experimental_buildkit_source_policy) | String            | Specify a BuildKit source policy file.                          |

BuildKit also supports a few additional configuration parameters. Refer to [BuildKit built-in build args](https://docs.docker.com/reference/dockerfile/#buildkit-built-in-build-args).

You can express Boolean values for environment variables in different ways. For example, `true`, `1`, and `T` all evaluate to true. Evaluation is done using the `strconv.ParseBool` function in the Go standard library. See the [reference documentation](https://pkg.go.dev/strconv#ParseBool) for details.

### [BUILDKIT\_COLORS](#buildkit_colors)

Changes the colors of the terminal output. Set `BUILDKIT_COLORS` to a CSV string in the following format:

```console
$ export BUILDKIT_COLORS="run=123,20,245:error=yellow:cancel=blue:warning=white"
```

Color values can be any valid RGB hex code, or one of the [BuildKit predefined colors](https://github.com/moby/buildkit/blob/master/util/progress/progressui/colors.go).

Setting `NO_COLOR` to anything turns off colorized output, as recommended by [no-color.org](https://no-color.org/).

### [BUILDKIT\_HOST](#buildkit_host)

Requires: Docker Buildx [0.9.0](https://github.com/docker/buildx/releases/tag/v0.9.0) and later

You use the `BUILDKIT_HOST` to specify the address of a BuildKit daemon to use as a remote builder. This is the same as specifying the address as a positional argument to `docker buildx create`.

Usage:

```console
$ export BUILDKIT_HOST=tcp://localhost:1234
$ docker buildx create --name=remote --driver=remote
```

If you specify both the `BUILDKIT_HOST` environment variable and a positional argument, the argument takes priority.

### [BUILDKIT\_PROGRESS](#buildkit_progress)

Sets the type of the BuildKit progress output. Valid values are:

* `auto` (default): automatically uses `tty` in interactive terminals, `plain` otherwise
* `plain`: displays build steps sequentially in simple text format
* `tty`: interactive output with formatted progress bars and build steps
* `quiet`: suppresses progress output, only shows errors and final image ID
* `none`: no progress output, only shows errors
* `rawjson`: outputs build progress as raw JSON (useful for parsing by other tools)

Usage:

```console
$ export BUILDKIT_PROGRESS=plain
```

### [BUILDKIT\_TTY\_LOG\_LINES](#buildkit_tty_log_lines)

You can change how many log lines are visible for active steps in TTY mode by setting `BUILDKIT_TTY_LOG_LINES` to a number (default to `6`).

```console
$ export BUILDKIT_TTY_LOG_LINES=8
```

### [EXPERIMENTAL\_BUILDKIT\_SOURCE\_POLICY](#experimental_buildkit_source_policy)

Lets you specify a [BuildKit source policy](https://github.com/moby/buildkit/blob/master/docs/build-repro.md#reproducing-the-pinned-dependencies) file for creating reproducible builds with pinned dependencies.

```console
$ export EXPERIMENTAL_BUILDKIT_SOURCE_POLICY=./policy.json
```

Example:

```json
{
  "rules": [
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "docker-image://docker.io/library/alpine:latest"
      },
      "updates": {
        "identifier": "docker-image://docker.io/library/alpine:latest@sha256:4edbd2beb5f78b1014028f4fbb99f3237d9561100b6881aabbf5acce2c4f9454"
      }
    },
    {
      "action": "CONVERT",
      "selector": {
        "identifier": "https://raw.githubusercontent.com/moby/buildkit/v0.10.1/README.md"
      },
      "updates": {
        "attrs": {"http.checksum": "sha256:6e4b94fc270e708e1068be28bd3551dc6917a4fc5a61293d51bb36e6b75c4b53"}
      }
    },
    {
      "action": "DENY",
      "selector": {
        "identifier": "docker-image://docker.io/library/golang*"
      }
    }
  ]
}
```

### [BUILDX\_BAKE\_FILE](#buildx_bake_file)

Requires: Docker Buildx [0.26.0](https://github.com/docker/buildx/releases/tag/v0.26.0) and later

Specify one or more build definition files for `docker buildx bake`.

This environment variable provides an alternative to the `-f` / `--file` command-line flag.

Multiple files can be specified by separating them with the system path separator (":" on Linux/macOS, ";" on Windows):

```console
export BUILDX_BAKE_FILE=file1.hcl:file2.hcl
```

Or with a custom separator defined by the [BUILDX\_BAKE\_FILE\_SEPARATOR](#buildx_bake_file_separator) variable:

```console
export BUILDX_BAKE_FILE_SEPARATOR=@
export BUILDX_BAKE_FILE=file1.hcl@file2.hcl
```

If both `BUILDX_BAKE_FILE` and the `-f` flag are set, only the files provided via `-f` are used.

If a listed file does not exist or is invalid, bake returns an error.

### [BUILDX\_BAKE\_FILE\_SEPARATOR](#buildx_bake_file_separator)

Requires: Docker Buildx [0.26.0](https://github.com/docker/buildx/releases/tag/v0.26.0) and later

Controls the separator used between file paths in the `BUILDX_BAKE_FILE` environment variable.

This is useful if your file paths contain the default separator character or if you want to standardize separators across different platforms.

```console
export BUILDX_BAKE_PATH_SEPARATOR=@
export BUILDX_BAKE_FILE=file1.hcl@file2.hcl
```

### [BUILDX\_BAKE\_GIT\_AUTH\_HEADER](#buildx_bake_git_auth_header)

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

Sets the HTTP authentication scheme when using a remote Bake definition in a private Git repository. This is equivalent to the [`GIT_AUTH_HEADER` secret](https://docs.docker.com/build/building/secrets/#http-authentication-scheme), but facilitates the pre-flight authentication in Bake when loading the remote Bake file. Supported values are `bearer` (default) and `basic`.

Usage:

```console
$ export BUILDX_BAKE_GIT_AUTH_HEADER=basic
```

### [BUILDX\_BAKE\_GIT\_AUTH\_TOKEN](#buildx_bake_git_auth_token)

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

Sets the HTTP authentication token when using a remote Bake definition in a private Git repository. This is equivalent to the [`GIT_AUTH_TOKEN` secret](https://docs.docker.com/build/building/secrets/#git-authentication-for-remote-contexts), but facilitates the pre-flight authentication in Bake when loading the remote Bake file.

Usage:

```console
$ export BUILDX_BAKE_GIT_AUTH_TOKEN=$(cat git-token.txt)
```

### [BUILDX\_BAKE\_GIT\_SSH](#buildx_bake_git_ssh)

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

Lets you specify a list of SSH agent socket filepaths to forward to Bake for authenticating to a Git server when using a remote Bake definition in a private repository. This is similar to SSH mounts for builds, but facilitates the pre-flight authentication in Bake when resolving the build definition.

Setting this environment is typically not necessary, because Bake will use the `SSH_AUTH_SOCK` agent socket by default. You only need to specify this variable if you want to use a socket with a different filepath. This variable can take multiple paths using a comma-separated string.

Usage:

```console
$ export BUILDX_BAKE_GIT_SSH=/run/foo/listener.sock,~/.creds/ssh.sock
```

### [BUILDX\_BUILDER](#buildx_builder)

Overrides the configured builder instance. Same as the `docker buildx --builder` CLI flag.

Usage:

```console
$ export BUILDX_BUILDER=my-builder
```

### [BUILDX\_CONFIG](#buildx_config)

You can use `BUILDX_CONFIG` to specify the directory to use for build configuration, state, and logs. The lookup order for this directory is as follows:

* `$BUILDX_CONFIG`
* `$DOCKER_CONFIG/buildx`
* `~/.docker/buildx` (default)

Usage:

```console
$ export BUILDX_CONFIG=/usr/local/etc
```

### [BUILDX\_CPU\_PROFILE](#buildx_cpu_profile)

Requires: Docker Buildx [0.18.0](https://github.com/docker/buildx/releases/tag/v0.18.0) and later

If specified, Buildx generates a `pprof` CPU profile at the specified location.

> Note
>
> This property is only useful for when developing Buildx. The profiling data is not relevant for analyzing a build's performance.

Usage:

```console
$ export BUILDX_CPU_PROFILE=buildx_cpu.prof
```

### [BUILDX\_EXPERIMENTAL](#buildx_experimental)

Enables experimental build features.

Usage:

```console
$ export BUILDX_EXPERIMENTAL=1
```

### [BUILDX\_GIT\_CHECK\_DIRTY](#buildx_git_check_dirty)

Requires: Docker Buildx [0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4) and later

When set to true, checks for dirty state in source control information for [provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/).

Usage:

```console
$ export BUILDX_GIT_CHECK_DIRTY=1
```

### [BUILDX\_GIT\_INFO](#buildx_git_info)

Requires: Docker Buildx [0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0) and later

When set to false, removes source control information from [provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/).

Usage:

```console
$ export BUILDX_GIT_INFO=0
```

### [BUILDX\_GIT\_LABELS](#buildx_git_labels)

Requires: Docker Buildx [0.10.0](https://github.com/docker/buildx/releases/tag/v0.10.0) and later

Adds provenance labels, based on Git information, to images that you build. The labels are:

* `com.docker.image.source.entrypoint`: Location of the Dockerfile relative to the project root
* `org.opencontainers.image.revision`: Git commit revision
* `org.opencontainers.image.source`: SSH or HTTPS address of the repository

Example:

```json
  "Labels": {
    "com.docker.image.source.entrypoint": "Dockerfile",
    "org.opencontainers.image.revision": "5734329c6af43c2ae295010778cd308866b95d9b",
    "org.opencontainers.image.source": "git@github.com:foo/bar.git"
  }
```

Usage:

* Set `BUILDX_GIT_LABELS=1` to include the `entrypoint` and `revision` labels.
* Set `BUILDX_GIT_LABELS=full` to include all labels.

If the repository is in a dirty state, the `revision` gets a `-dirty` suffix.

### [BUILDX\_MEM\_PROFILE](#buildx_mem_profile)

Requires: Docker Buildx [0.18.0](https://github.com/docker/buildx/releases/tag/v0.18.0) and later

If specified, Buildx generates a `pprof` memory profile at the specified location.

> Note
>
> This property is only useful for when developing Buildx. The profiling data is not relevant for analyzing a build's performance.

Usage:

```console
$ export BUILDX_MEM_PROFILE=buildx_mem.prof
```

### [BUILDX\_METADATA\_PROVENANCE](#buildx_metadata_provenance)

Requires: Docker Buildx [0.14.0](https://github.com/docker/buildx/releases/tag/v0.14.0) and later

By default, Buildx includes minimal provenance information in the metadata file through [`--metadata-file` flag](/reference/cli/docker/buildx/build/#metadata-file). This environment variable allows you to customize the provenance information included in the metadata file:

* `min` sets minimal provenance (default).
* `max` sets full provenance.
* `disabled`, `false` or `0` does not set any provenance.

### [BUILDX\_METADATA\_WARNINGS](#buildx_metadata_warnings)

Requires: Docker Buildx [0.16.0](https://github.com/docker/buildx/releases/tag/v0.16.0) and later

By default, Buildx does not include build warnings in the metadata file through [`--metadata-file` flag](/reference/cli/docker/buildx/build/#metadata-file). You can set this environment variable to `1` or `true` to include them.

### [BUILDX\_NO\_DEFAULT\_ATTESTATIONS](#buildx_no_default_attestations)

Requires: Docker Buildx [0.10.4](https://github.com/docker/buildx/releases/tag/v0.10.4) and later

By default, BuildKit v0.11 and later adds [provenance attestations](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) to images you build. Set `BUILDX_NO_DEFAULT_ATTESTATIONS=1` to disable the default provenance attestations.

Usage:

```console
$ export BUILDX_NO_DEFAULT_ATTESTATIONS=1
```

### [BUILDX\_NO\_DEFAULT\_LOAD](#buildx_no_default_load)

When you build an image using the `docker` driver, the image is automatically loaded to the image store when the build finishes. Set `BUILDX_NO_DEFAULT_LOAD` to disable automatic loading of images to the local container store.

Usage:

```console
$ export BUILDX_NO_DEFAULT_LOAD=1
```

----
url: https://docs.docker.com/guides/java/
----

# Java language-specific guide

***

This guide demonstrates how to containerize Java applications using Docker.

**Time to complete** 20 minutes

The Java getting started guide teaches you how to create a containerized Spring Boot application using Docker. In this module, you’ll learn how to:

* Containerize and run a Spring Boot application with Maven
* Set up a local development environment to connect a database to the container, configure a debugger, and use Compose Watch for live reload
* Run your unit tests inside a container
* Configure a CI/CD pipeline for your application using GitHub Actions
* Deploy your containerized application locally to Kubernetes to test and debug your deployment

After completing the Java getting started modules, you should be able to containerize your own Java application based on the examples and instructions provided in this guide.

Get started containerizing your first Java app.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/java/containerize/)

   Learn how to containerize a Java application.

2. [Develop your app](https://docs.docker.com/guides/java/develop/)

   Learn how to develop your application locally.

3. [Run your tests](https://docs.docker.com/guides/java/run-tests/)

   How to build and run your Java tests

4. [Configure CI/CD](https://docs.docker.com/guides/java/configure-ci-cd/)

   Learn how to Configure CI/CD for your Java application

5. [Test your deployment](https://docs.docker.com/guides/java/deploy/)

----
url: https://docs.docker.com/reference/cli/docker/container/stats/
----

# docker container stats

***

| Description                                                               | Display a live stream of container(s) resource usage statistics |
| ------------------------------------------------------------------------- | --------------------------------------------------------------- |
| Usage                                                                     | `docker container stats [OPTIONS] [CONTAINER...]`               |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker stats`                                                  |

## [Description](#description)

The `docker stats` command returns a live data stream for running containers. To limit data to one or more specific containers, specify a list of container names or ids separated by a space. You can specify a stopped container but stopped containers do not return any data.

If you need more detailed information about a container's resource usage, use the `/containers/(id)/stats` API endpoint.

> Note
>
> On Linux, the Docker CLI reports memory usage by subtracting cache usage from the total memory usage. The API does not perform such a calculation but rather provides the total memory usage and the amount from the cache so that clients can use the data as needed. The cache usage is defined as the value of `total_inactive_file` field in the `memory.stat` file on cgroup v1 hosts.
>
> On Docker 19.03 and older, the cache usage was defined as the value of `cache` field. On cgroup v2 hosts, the cache usage is defined as the value of `inactive_file` field.

> Note
>
> The `PIDS` column contains the number of processes and kernel threads created by that container. Threads is the term used by Linux kernel. Other equivalent terms are "lightweight process" or "kernel task", etc. A large number in the `PIDS` column combined with a small number of processes (as reported by `ps` or `top`) may indicate that something in the container is creating many threads.

## [Options](#options)

| Option                | Default | Description                                                                                                                                                                                                                                                                                                                                                                            |
| --------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-a, --all`           |         | Show all containers (default shows just running)                                                                                                                                                                                                                                                                                                                                       |
| [`--format`](#format) |         | Format output using a custom template: 'table': Print output in table format with column headers (default) 'table TEMPLATE': Print output in table format using the given Go template 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `--no-stream`         |         | Disable streaming stats and only pull the first result                                                                                                                                                                                                                                                                                                                                 |
| `--no-trunc`          |         | Do not truncate output                                                                                                                                                                                                                                                                                                                                                                 |

## [Examples](#examples)

Running `docker stats` on all running containers against a Linux daemon.

```console
$ docker stats

CONTAINER ID        NAME                                    CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
b95a83497c91        awesome_brattain                        0.28%               5.629MiB / 1.952GiB   0.28%               916B / 0B           147kB / 0B          9
67b2525d8ad1        foobar                                  0.00%               1.727MiB / 1.952GiB   0.09%               2.48kB / 0B         4.11MB / 0B         2
e5c383697914        test-1951.1.kay7x1lh1twk9c0oig50sd5tr   0.00%               196KiB / 1.952GiB     0.01%               71.2kB / 0B         770kB / 0B          1
4bda148efbc0        random.1.vnc8on831idyr42slu578u3cr      0.00%               1.672MiB / 1.952GiB   0.08%               110kB / 0B          578kB / 0B          2
```

If you don't [specify a format string using `--format`](#format), the following columns are shown.

| Column name               | Description                                                                                  |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| `CONTAINER ID` and `Name` | the ID and name of the container                                                             |
| `CPU %` and `MEM %`       | the percentage of the host's CPU and memory the container is using                           |
| `MEM USAGE / LIMIT`       | the total memory the container is using, and the total amount of memory it is allowed to use |
| `NET I/O`                 | The amount of data the container has received and sent over its network interface            |
| `BLOCK I/O`               | The amount of data the container has written to and read from block devices on the host      |
| `PIDs`                    | the number of processes or threads the container has created                                 |

Running `docker stats` on multiple containers by name and id against a Linux daemon.

```console
$ docker stats awesome_brattain 67b2525d8ad1

CONTAINER ID        NAME                CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
b95a83497c91        awesome_brattain    0.28%               5.629MiB / 1.952GiB   0.28%               916B / 0B           147kB / 0B          9
67b2525d8ad1        foobar              0.00%               1.727MiB / 1.952GiB   0.09%               2.48kB / 0B         4.11MB / 0B         2
```

Running `docker stats` on container with name `nginx` and getting output in `json` format.

```console
$ docker stats nginx --no-stream --format "{{ json . }}"
{"BlockIO":"0B / 13.3kB","CPUPerc":"0.03%","Container":"nginx","ID":"ed37317fbf42","MemPerc":"0.24%","MemUsage":"2.352MiB / 982.5MiB","Name":"nginx","NetIO":"539kB / 606kB","PIDs":"2"}
```

Running `docker stats` with customized format on all (running and stopped) containers.

```console
$ docker stats --all --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}" fervent_panini 5acfcb1b4fd1 humble_visvesvaraya big_heisenberg

CONTAINER                CPU %               MEM USAGE / LIMIT
fervent_panini           0.00%               56KiB / 15.57GiB
5acfcb1b4fd1             0.07%               32.86MiB / 15.57GiB
humble_visvesvaraya      0.00%               0B / 0B
big_heisenberg           0.00%               0B / 0B
```

`humble_visvesvaraya` and `big_heisenberg` are stopped containers in the above example.

Running `docker stats` on all running containers against a Windows daemon.

```powershell
PS E:\> docker stats
CONTAINER ID        CPU %               PRIV WORKING SET    NET I/O             BLOCK I/O
09d3bb5b1604        6.61%               38.21 MiB           17.1 kB / 7.73 kB   10.7 MB / 3.57 MB
9db7aa4d986d        9.19%               38.26 MiB           15.2 kB / 7.65 kB   10.6 MB / 3.3 MB
3f214c61ad1d        0.00%               28.64 MiB           64 kB / 6.84 kB     4.42 MB / 6.93 MB
```

Running `docker stats` on multiple containers by name and id against a Windows daemon.

```powershell
PS E:\> docker ps -a
CONTAINER ID        NAME                IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
3f214c61ad1d        awesome_brattain    nanoserver          "cmd"               2 minutes ago       Up 2 minutes                            big_minsky
9db7aa4d986d        mad_wilson          windowsservercore   "cmd"               2 minutes ago       Up 2 minutes                            mad_wilson
09d3bb5b1604        fervent_panini      windowsservercore   "cmd"               2 minutes ago       Up 2 minutes                            affectionate_easley

PS E:\> docker stats 3f214c61ad1d mad_wilson
CONTAINER ID        NAME                CPU %               PRIV WORKING SET    NET I/O             BLOCK I/O
3f214c61ad1d        awesome_brattain    0.00%               46.25 MiB           76.3 kB / 7.92 kB   10.3 MB / 14.7 MB
9db7aa4d986d        mad_wilson          9.59%               40.09 MiB           27.6 kB / 8.81 kB   17 MB / 20.1 MB
```

### [Format the output (--format)](#format)

The formatting option (`--format`) pretty prints container output using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder  | Description                                  |
| ------------ | -------------------------------------------- |
| `.Container` | Container name or ID (user input)            |
| `.Name`      | Container name                               |
| `.ID`        | Container ID                                 |
| `.CPUPerc`   | CPU percentage                               |
| `.MemUsage`  | Memory usage                                 |
| `.NetIO`     | Network IO                                   |
| `.BlockIO`   | Block IO                                     |
| `.MemPerc`   | Memory percentage (Not available on Windows) |
| `.PIDs`      | Number of PIDs (Not available on Windows)    |

When using the `--format` option, the `stats` command either outputs the data exactly as the template declares or, when using the `table` directive, includes column headers as well.

The following example uses a template without headers and outputs the `Container` and `CPUPerc` entries separated by a colon (`:`) for all images:

```console
$ docker stats --format "{{.Container}}: {{.CPUPerc}}"

09d3bb5b1604: 6.61%
9db7aa4d986d: 9.19%
3f214c61ad1d: 0.00%
```

To list all containers statistics with their name, CPU percentage and memory usage in a table format you can use:

```console
$ docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

CONTAINER           CPU %               PRIV WORKING SET
1285939c1fd3        0.07%               796 KiB / 64 MiB
9c76f7834ae2        0.07%               2.746 MiB / 64 MiB
d1ea048f04e4        0.03%               4.583 MiB / 64 MiB
```

The default format is as follows:

On Linux:

```
"table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.MemPerc}}\t{{.NetIO}}\t{{.BlockIO}}\t{{.PIDs}}"
```

On Windows:

```
"table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

----
url: https://docs.docker.com/reference/cli/sbx/completion/zsh/
----

# sbx completion zsh

| Description | Generate the autocompletion script for zsh |
| ----------- | ------------------------------------------ |
| Usage       | `sbx completion zsh [flags]`               |

## [Description](#description)

Generate the autocompletion script for the zsh shell.

If shell completion is not already enabled in your environment you will need to enable it. You can execute the following once:

```
echo "autoload -U compinit; compinit" >> ~/.zshrc
```

To load completions in your current shell session:

```
source <(sbx completion zsh)
```

To load completions for every new session, execute once:

#### [Linux:](#linux)

```
sbx completion zsh > "${fpath[1]}/_sbx"
```

#### [macOS:](#macos)

```
sbx completion zsh > $(brew --prefix)/share/zsh/site-functions/_sbx
```

You will need to start a new shell for this setup to take effect.

## [Options](#options)

| Option              | Default | Description                     |
| ------------------- | ------- | ------------------------------- |
| `--no-descriptions` |         | disable completion descriptions |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/engine/logging/
----

# View container logs

***

Table of contents

***

The `docker logs` command shows information logged by a running container. The `docker service logs` command shows information logged by all containers participating in a service. The information that's logged and the format of the log depends almost entirely on the container's endpoint command.

By default, `docker logs` or `docker service logs` shows the command's output just as it would appear if you ran the command interactively in a terminal. Unix and Linux commands typically open three I/O streams when they run, called `STDIN`, `STDOUT`, and `STDERR`. `STDIN` is the command's input stream, which may include input from the keyboard or input from another command. `STDOUT` is usually a command's normal output, and `STDERR` is typically used to output error messages. By default, `docker logs` shows the command's `STDOUT` and `STDERR`. To read more about I/O and Linux, see the [Linux Documentation Project article on I/O redirection](https://tldp.org/LDP/abs/html/io-redirection.html).

In some cases, `docker logs` may not show useful information unless you take additional steps.

* If you use a [logging driver](https://docs.docker.com/engine/logging/configure/) which sends logs to a file, an external host, a database, or another logging back-end, and have ["dual logging"](https://docs.docker.com/engine/logging/dual-logging/) disabled, `docker logs` may not show useful information.
* If your image runs a non-interactive process such as a web server or a database, that application may send its output to log files instead of `STDOUT` and `STDERR`.

In the first case, your logs are processed in other ways and you may choose not to use `docker logs`. In the second case, the official `nginx` image shows one workaround, and the official Apache `httpd` image shows another.

The official `nginx` image creates a symbolic link from `/var/log/nginx/access.log` to `/dev/stdout`, and creates another symbolic link from `/var/log/nginx/error.log` to `/dev/stderr`, overwriting the log files and causing logs to be sent to the relevant special device instead. See the [Dockerfile](https://github.com/nginxinc/docker-nginx/blob/8921999083def7ba43a06fabd5f80e4406651353/mainline/jessie/Dockerfile#L21-L23).

The official `httpd` driver changes the `httpd` application's configuration to write its normal output directly to `/proc/self/fd/1` (which is `STDOUT`) and its errors to `/proc/self/fd/2` (which is `STDERR`). See the [Dockerfile](https://github.com/docker-library/httpd/blob/b13054c7de5c74bbaa6d595dbe38969e6d4f860c/2.2/Dockerfile#L72-L75).

## [Next steps](#next-steps)

* Configure [logging drivers](https://docs.docker.com/engine/logging/configure/).
* Write a [Dockerfile](https://docs.docker.com/reference/dockerfile/).

----
url: https://docs.docker.com/reference/cli/docker/scout/compare/
----

# docker scout compare

***

| Description                                                               | Compare two images and display differences (experimental)                         |
| ------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| Usage                                                                     | `docker scout compare --to IMAGE\|DIRECTORY\|ARCHIVE [IMAGE\|DIRECTORY\|ARCHIVE]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker scout diff`                                                               |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

The `docker scout compare` command analyzes two images and displays a comparison.

> This command is **experimental** and its behaviour might change in the future

The intended use of this command is to compare two versions of the same image. For instance, when a new image is built and compared to the version running in production.

If no image is specified, the most recently built image is used as a comparison target.

The following artifact types are supported:

* Images
* OCI layout directories
* Tarball archives, as created by `docker save`
* Local directory or file

By default, the tool expects an image reference, such as:

* `redis`
* `curlimages/curl:7.87.0`
* `mcr.microsoft.com/dotnet/runtime:7.0`

If the artifact you want to analyze is an OCI directory, a tarball archive, a local file or directory, or if you want to control from where the image will be resolved, you must prefix the reference with one of the following:

* `image://` (default) use a local image, or fall back to a registry lookup
* `local://` use an image from the local image store (don't do a registry lookup)
* `registry://` use an image from a registry (don't use a local image)
* `oci-dir://` use an OCI layout directory
* `archive://` use a tarball archive, as created by `docker save`
* `fs://` use a local directory or file
* `sbom://` SPDX file or in-toto attestation file with SPDX predicate or `syft` json SBOM file

## [Options](#options)

| Option                | Default             | Description                                                                                                                                                          |
| --------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-x, --exit-on`       |                     | Comma separated list of conditions to fail the action step if worse or changed, options are: vulnerability, policy, package                                          |
| `--format`            | `text`              | Output format of the generated vulnerability report: - text: default output, plain text with or without colors depending on the terminal - markdown: Markdown output |
| `--hide-policies`     |                     | Hide policy status from the output                                                                                                                                   |
| `--ignore-base`       |                     | Filter out CVEs introduced from base image                                                                                                                           |
| `--ignore-suppressed` |                     | Filter CVEs found in Scout exceptions based on the specified exception scope                                                                                         |
| `--ignore-unchanged`  |                     | Filter out unchanged packages                                                                                                                                        |
| `--multi-stage`       |                     | Show packages from multi-stage Docker builds                                                                                                                         |
| `--only-fixed`        |                     | Filter to fixable CVEs                                                                                                                                               |
| `--only-package-type` |                     | Comma separated list of package types (like apk, deb, rpm, npm, pypi, golang, etc)                                                                                   |
| `--only-policy`       |                     | Comma separated list of policies to evaluate                                                                                                                         |
| `--only-severity`     |                     | Comma separated list of severities (critical, high, medium, low, unspecified) to filter CVEs by                                                                      |
| `--only-stage`        |                     | Comma separated list of multi-stage Docker build stage names                                                                                                         |
| `--only-unfixed`      |                     | Filter to unfixed CVEs                                                                                                                                               |
| `--only-vex-affected` |                     | Filter CVEs by VEX statements with status not affected                                                                                                               |
| `--org`               |                     | Namespace of the Docker organization                                                                                                                                 |
| `-o, --output`        |                     | Write the report to a file                                                                                                                                           |
| `--platform`          |                     | Platform of image to analyze                                                                                                                                         |
| `--ref`               |                     | Reference to use if the provided tarball contains multiple references. Can only be used with archive                                                                 |
| `--to`                |                     | Image, directory, or archive to compare to                                                                                                                           |
| `--to-env`            |                     | Name of environment to compare to                                                                                                                                    |
| `--to-latest`         |                     | Latest image processed to compare to                                                                                                                                 |
| `--to-ref`            |                     | Reference to use if the provided tarball contains multiple references. Can only be used with archive.                                                                |
| `--vex-author`        | `[<.*@docker.com>]` | List of VEX statement authors to accept                                                                                                                              |
| `--vex-location`      |                     | File location of directory or file containing VEX statements                                                                                                         |

## [Examples](#examples)

### [Compare the most recently built image to the latest tag](#compare-the-most-recently-built-image-to-the-latest-tag)

```console
$ docker scout compare --to namespace/repo:latest
```

### [Compare local build to the same tag from the registry](#compare-local-build-to-the-same-tag-from-the-registry)

```console
$ docker scout compare local://namespace/repo:latest --to registry://namespace/repo:latest
```

### [Ignore base images](#ignore-base-images)

```console
$ docker scout compare --ignore-base --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

### [Generate a markdown output](#generate-a-markdown-output)

```console
$ docker scout compare --format markdown --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

### [Only compare maven packages and only display critical vulnerabilities for maven packages](#only-compare-maven-packages-and-only-display-critical-vulnerabilities-for-maven-packages)

```console
$ docker scout compare --only-package-type maven --only-severity critical --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

### [Show all policy results for both images](#show-all-policy-results-for-both-images)

```console
docker scout compare --to namespace/repo:latest namespace/repo:v1.2.3-pre
```

----
url: https://docs.docker.com/ai/sandboxes/governance/sign-in-enforcement/
----

# Sign-in enforcement

***

Table of contents

***

Sign-in enforcement restricts Docker Sandboxes to users who are members of specific Docker organizations. An administrator deploys an enforcement configuration to managed endpoints, and `sbx login` verifies organization membership after the user authenticates. If the check fails, credentials are immediately revoked and the user can't run sandboxes.

Without this enforcement, a developer can sign in with a personal account and bypass organization [governance policies](https://docs.docker.com/ai/sandboxes/governance/org/). Sign-in enforcement closes that gap at the endpoint, where users can't override it.

> Note
>
> Sign-in enforcement is part of Docker's AI Governance offering. [Contact Docker Sales](https://www.docker.com/products/ai-governance/#contact-sales) to learn more.

## [How it works](#how-it-works)

1. An administrator deploys an enforcement configuration to managed endpoints through MDM, Group Policy, or configuration management, specifying one or more allowed Docker organization slugs.
2. When a user runs `sbx login`, they authenticate with Docker. Credentials are saved temporarily, then Docker Sandboxes calls the Docker API to verify organization membership.
3. If the user belongs to at least one allowed organization, login succeeds and the credentials are kept.
4. If not, Docker Sandboxes immediately revokes the saved credentials and the user receives an [error message](#error-messages) listing the required organizations.

`sbx login` and `sbx logout` always run regardless of organization membership. Other commands require a valid signed-in session, so they fail after a denied login until the user signs in with an allowed account.

## [Enforcement configuration](#enforcement-configuration)

All platforms express the same logical schema. The canonical JSON representation:

```json
{
  "allowedOrgs": ["docker", "acme-corp"],
  "adminEmail": "it-security@acme-corp.com",
  "adminURL": "https://acme-corp.atlassian.net/servicedesk/it",
  "adminName": "ACME IT Security Team"
}
```

| Field         | Type            | Required | Description                                                                                         |
| ------------- | --------------- | -------- | --------------------------------------------------------------------------------------------------- |
| `allowedOrgs` | list of strings | Yes      | Docker organization slugs. The user must be a member of at least one. Matching is case-insensitive. |
| `adminName`   | string          | No       | Administrator or team display name shown in the denial message.                                     |
| `adminEmail`  | string          | No       | Contact email shown in the denial message.                                                          |
| `adminURL`    | string          | No       | Help desk or access-request URL shown in the denial message.                                        |

If `allowedOrgs` is empty or missing, enforcement is inactive and any authenticated user can use Docker Sandboxes.

The optional `adminName`, `adminEmail`, and `adminURL` fields give denied users a path to resolution. Include the contact details your organization uses for access requests.

## [Deploy the configuration](#deploy-the-configuration)

Use your existing endpoint management tooling to deploy the configuration. Each platform reads it from a native location that ordinary users can't modify.

On macOS, the configuration is a managed preferences domain, `com.docker.sbx`.

Deploy it through any MDM solution, such as Jamf or Intune, as a custom configuration profile. MDM-deployed profiles take precedence over user-level preferences and can only be removed by removing the device from MDM management, so users can't override them.

The following `.mobileconfig` payload sets the allowed organization and admin contact details:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>PayloadContent</key>
  <array>
    <dict>
      <key>PayloadType</key>
      <string>com.apple.ManagedClient.preferences</string>
      <key>PayloadVersion</key>
      <integer>1</integer>
      <key>PayloadIdentifier</key>
      <string>com.docker.sbx.policy</string>
      <key>PayloadUUID</key>
      <string><!-- generate a UUID --></string>
      <key>PayloadEnabled</key>
      <true/>
      <key>PayloadDisplayName</key>
      <string>Docker Sandboxes Policy</string>
      <key>PayloadContent</key>
      <dict>
        <key>com.docker.sbx</key>
        <dict>
          <key>Forced</key>
          <array>
            <dict>
              <key>mcx_preference_settings</key>
              <dict>
                <key>allowedOrgs</key>
                <array>
                  <string>acme-corp</string>
                </array>
                <key>adminEmail</key>
                <string>it-security@acme-corp.com</string>
                <key>adminURL</key>
                <string>https://acme-corp.atlassian.net/servicedesk/it</string>
                <key>adminName</key>
                <string>ACME IT Security</string>
              </dict>
            </dict>
          </array>
        </dict>
      </dict>
    </dict>
  </array>
</dict>
</plist>
```

To test the configuration locally without MDM, write to the user preferences domain:

```console
$ defaults write com.docker.sbx allowedOrgs -array "acme-corp"
$ defaults write com.docker.sbx adminEmail "it@acme.com"
```

To remove the test configuration:

```console
$ defaults delete com.docker.sbx
```

`defaults write` uses the user preferences domain, not the managed-preferences domain. On a managed device, the MDM profile is authoritative and user-level settings in the same domain are ignored.

Deploy it through Group Policy, Intune, or any endpoint management tool that can write registry values.

| Value name    | Type           | Description                                         |
| ------------- | -------------- | --------------------------------------------------- |
| `allowedOrgs` | `REG_MULTI_SZ` | Multi-string list, one organization slug per string |
| `adminName`   | `REG_SZ`       | Administrator or team name (optional)               |
| `adminEmail`  | `REG_SZ`       | Contact email (optional)                            |
| `adminURL`    | `REG_SZ`       | Help desk URL (optional)                            |

To test the configuration locally, run the following in an elevated PowerShell session. Use `New-ItemProperty` to create values with an explicit type; `Set-ItemProperty` doesn't create new values.

```powershell
New-Item -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" -Force

New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" `
  -Name "allowedOrgs" -Value @("acme-corp") -PropertyType MultiString -Force
New-ItemProperty -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" `
  -Name "adminEmail" -Value "it@acme.com" -PropertyType String -Force
```

To remove the configuration:

```powershell
Remove-Item -Path "HKLM:\SOFTWARE\Policies\Docker\SBX" -Recurse -Force
```

On Linux, the configuration is a root-owned JSON file at `/etc/docker-sbx/config.json`.

Deploy it through configuration management such as Ansible, Puppet, Chef, or Salt. The file must be owned by root with `644` permissions.

```json
{
  "allowedOrgs": ["acme-corp"],
  "adminEmail": "it-security@acme-corp.com",
  "adminURL": "https://acme-corp.atlassian.net/servicedesk/it",
  "adminName": "ACME IT Security"
}
```

To deploy and set ownership:

```console
$ sudo mkdir -p /etc/docker-sbx
$ sudo tee /etc/docker-sbx/config.json <<'EOF'
{"allowedOrgs": ["acme-corp"], "adminEmail": "it@acme.com"}
EOF
$ sudo chown root:root /etc/docker-sbx/config.json
$ sudo chmod 644 /etc/docker-sbx/config.json
```

To remove the configuration:

```console
$ sudo rm -f /etc/docker-sbx/config.json
```

The Linux loader fails closed if the file is a symlink, isn't a regular file, isn't owned by root, or is writable by group or other. Any deviation is treated as a configuration error and `sbx login` is denied with a descriptive message. Deploying with the commands above passes these checks.

## [Error messages](#error-messages)

When a user signs in with an account that isn't a member of an allowed organization, they're signed out and shown a denial message. Only the contact fields you configure appear: if only `adminEmail` is set, the URL line is omitted.

When no admin contact details are configured:

```text
Access denied: Your administrator requires you to be logged into an account
that is a member of one of the following Docker organizations:
  - acme-corp

Sign in with an account that belongs to one of these organizations, or
contact your administrator for access.
```

When admin contact details are configured:

```text
Access denied: Your administrator requires you to be logged into an account
that is a member of one of the following Docker organizations:
  - acme-corp

For access, contact ACME IT Security:
  Email: it-security@acme-corp.com
