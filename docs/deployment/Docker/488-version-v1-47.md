url: https://docs.docker.com/reference/api/engine/version/v1.47/
----

# Docker Engine API (1.47)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.47.yaml)

The Engine API is an HTTP API served by Docker Engine. It is the API the Docker client uses to communicate with the Engine, so everything the Docker client can do can be done with the API.

Most of the client's commands map directly to API endpoints (e.g. `docker ps` is `GET /containers/json`). The notable exception is running containers, which consists of several API calls.

## [](#section/Errors)Errors

The API uses standard HTTP status codes to indicate the success or failure of the API call. The body of the response will be JSON in the following format:

```
{
  "message": "page not found"
}
```

## [](#section/Versioning)Versioning

The API is usually changed in each release, so API calls are versioned to ensure that clients don't break. To lock to a specific version of the API, you prefix the URL with its version, for example, call `/v1.30/info` to use the v1.30 version of the `/info` endpoint. If the API version specified in the URL is not supported by the daemon, a HTTP `400 Bad Request` error message is returned.

If you omit the version-prefix, the current version of the API (v1.47) is used. For example, calling `/info` is the same as calling `/v1.47/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

Engine releases in the near future should support this version of the API, so your client will continue to work even if it is talking to a newer Engine.

The API uses an open schema model, which means server may add extra properties to responses. Likewise, the server will ignore any extra query parameters and request body properties. When you write clients, you need to ignore additional properties in responses to ensure they do not break when talking to newer daemons.

## [](#section/Authentication)Authentication

Authentication for registries is handled client side. The client has to send authentication details to various endpoints that need to communicate with registries, such as `POST /images/(name)/push`. These are sent as `X-Registry-Auth` header as a [base64url encoded](https://tools.ietf.org/html/rfc4648#section-5) (JSON) string with the following structure:

```
{
  "username": "string",
  "password": "string",
  "serveraddress": "string"
}
```

The `serveraddress` is a domain/IP without a protocol. Throughout this structure, double quotes are required.

If you have already got an identity token from the [`/auth` endpoint](#operation/SystemAuth), you can just pass this instead of credentials:

```
{
  "identitytoken": "9cbaf023786cd7..."
}
```

## [](#tag/Container)Containers

Create and manage containers.

## [](#tag/Container/operation/ContainerList)List containers

Returns a list of containers. For details on the format, see the [inspect endpoint](#operation/ContainerInspect).

Note that it uses a different, smaller representation of a container than inspecting a single container. For example, the list of linked containers is not propagated .

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| all     | booleanDefault: falseReturn all containers. By default, only running containers are shown.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| limit   | integerReturn this number of most recently created containers, including non-running ones.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| size    | booleanDefault: falseReturn the size of container as fields `SizeRw` and `SizeRootFs`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| filters | stringFilters to process on the container list, encoded as JSON (a `map[string][]string`). For example, `{"status": ["paused"]}` will only return paused containers.Available filters:- `ancestor`=(`<image-name>[:<tag>]`, `<image id>`, or `<image@digest>`)

/v1.47/containers/json

|          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name     | string^/?\[a-zA-Z0-9]\[a-zA-Z0-9\_.-]+$Assign the specified name to the container. Must match `/?[a-zA-Z0-9][a-zA-Z0-9_.-]+`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| platform | stringDefault: ""Platform in the format `os[/arch[/variant]]` used for image lookup.When specified, the daemon checks if the requested image is present in the local image cache with the given OS and Architecture, and otherwise returns a `404` status.If the option is not set, the host's native OS and Architecture are used to look up the image in the image cache. However, if no platform is passed and the given image does exist in the local image cache, but its OS or architecture does not match, the container is created with the available image, and a warning is added to the `Warnings` field in the response, for example;```
WARNING: The requested image's platform (linux/arm64/v8) does not
         match the detected host platform (linux/amd64) and no
         specific platform was requested
``` |

##### Request Body schema:application/jsonrequired

Container to create

|                 |                                                                                                                                                                                                                                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hostname        | stringThe hostname to use for the container, as a valid RFC 1123 hostname.                                                                                                                                                                                                                            |
| Domainname      | stringThe domain name to use for the container.                                                                                                                                                                                                                                                       |
| User            | stringThe user that commands are run as inside the container.                                                                                                                                                                                                                                         |
| AttachStdin     | booleanDefault: falseWhether to attach to `stdin`.                                                                                                                                                                                                                                                    |
| AttachStdout    | booleanDefault: trueWhether to attach to `stdout`.                                                                                                                                                                                                                                                    |
| AttachStderr    | booleanDefault: trueWhether to attach to `stderr`.                                                                                                                                                                                                                                                    |
|                 | object or nullAn object mapping ports to an empty object in the form:`{"<port>/<tcp\|udp\|sctp>": {}}`                                                                                                                                                                                                |
| Tty             | booleanDefault: falseAttach standard streams to a TTY, including `stdin` if it is not closed.                                                                                                                                                                                                         |
| OpenStdin       | booleanDefault: falseOpen `stdin`                                                                                                                                                                                                                                                                     |
| StdinOnce       | booleanDefault: falseClose `stdin` after one attached client disconnects                                                                                                                                                                                                                              |
| Env             | Array of stringsA list of environment variables to set inside the container in the form `["VAR=value", ...]`. A variable without `=` is removed from the environment, rather than to have an empty value.                                                                                             |
| Cmd             | Array of stringsCommand to run specified as a string or an array of strings.                                                                                                                                                                                                                          |
|                 | object (HealthConfig)A test to perform to check that the container is healthy. Healthcheck commands should be side-effect free.                                                                                                                                                                       |
| ArgsEscaped     | boolean or nullDefault: falseCommand is already escaped (Windows only)                                                                                                                                                                                                                                |
| Image           | stringThe name (or reference) of the image to use when creating the container, or which was used when the container was created.                                                                                                                                                                      |
|                 | objectAn object mapping mount point paths inside the container to empty objects.                                                                                                                                                                                                                      |
| WorkingDir      | stringThe working directory for commands to run in.                                                                                                                                                                                                                                                   |
| Entrypoint      | Array of stringsThe entry point for the container as a string or an array of strings.If the array consists of exactly one empty string (`[""]`) then the entry point is reset to system default (i.e., the entry point used by docker when there is no `ENTRYPOINT` instruction in the `Dockerfile`). |
| NetworkDisabled | boolean or nullDisable networking for the container.                                                                                                                                                                                                                                                  |
| MacAddress      | string or nullMAC address of the container.Deprecated: this field is deprecated in API v1.44 and up. Use EndpointSettings.MacAddress instead.                                                                                                                                                         |
| OnBuild         | Array of strings or null`ONBUILD` metadata that were defined in the image's `Dockerfile`.                                                                                                                                                                                                             |
|                 | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                |
| StopSignal      | string or nullSignal to stop a container as a string or unsigned integer.                                                                                                                                                                                                                             |
| StopTimeout     | integer or nullDefault: 10Timeout to stop a container in seconds.                                                                                                                                                                                                                                     |
| Shell           | Array of strings or nullShell for when `RUN`, `CMD`, and `ENTRYPOINT` uses a shell.                                                                                                                                                                                                                   |
|                 | object (HostConfig)Container configuration that depends on the host we are running on                                                                                                                                                                                                                 |
|                 | object (NetworkingConfig)NetworkingConfig represents the container's networking configuration for each of its interfaces. It is used for the networking configs specified in the `docker create` and `docker network connect` commands.                                                               |

### Responses

/v1.47/containers/create

### Request samples

* Payload

Content type

application/json

`{
"Hostname": "",
"Domainname": "",
"User": "",
"AttachStdin": false,
"AttachStdout": true,
"AttachStderr": true,
"Tty": false,
"OpenStdin": false,
"StdinOnce": false,
"Env": [
"FOO=bar",
"BAZ=quux"
],
"Cmd": [
"date"
],
"Entrypoint": "",
"Image": "ubuntu",
"Labels": {
"com.example.vendor": "Acme",
"com.example.license": "GPL",
"com.example.version": "1.0"
},
"Volumes": {
"/volumes/data": { }
},
"WorkingDir": "",
"NetworkDisabled": false,
"MacAddress": "12:34:56:78:9a:bc",
"ExposedPorts": {
"22/tcp": { }
},
"StopSignal": "SIGTERM",
"StopTimeout": 10,
"HostConfig": {
"Binds": [
"/tmp:/tmp"
],
"Links": [
"redis3:redis"
],
"Memory": 0,
"MemorySwap": 0,
"MemoryReservation": 0,
"NanoCpus": 500000,
"CpuPercent": 80,
"CpuShares": 512,
"CpuPeriod": 100000,
"CpuRealtimePeriod": 1000000,
"CpuRealtimeRuntime": 10000,
"CpuQuota": 50000,
"CpusetCpus": "0,1",
"CpusetMems": "0,1",
"MaximumIOps": 0,
"MaximumIOBps": 0,
"BlkioWeight": 300,
"BlkioWeightDevice": [
{ }
],
"BlkioDeviceReadBps": [
{ }
],
"BlkioDeviceReadIOps": [
{ }
],
"BlkioDeviceWriteBps": [
{ }
],
"BlkioDeviceWriteIOps": [
{ }
],
"DeviceRequests": [
{
"Driver": "nvidia",
"Count": -1,
"DeviceIDs"": [
"0",
"1",
"GPU-fef8089b-4820-abfc-e83e-94318197576e"
],
"Capabilities": [ [
"gpu",
"nvidia",
"compute"
]
],
"Options": {
"property1": "string",
"property2": "string"
}
}
],
"MemorySwappiness": 60,
"OomKillDisable": false,
"OomScoreAdj": 500,
"PidMode": "",
"PidsLimit": 0,
"PortBindings": {
"22/tcp": [
{
"HostPort": "11022"
}
]
},
"PublishAllPorts": false,
"Privileged": false,
"ReadonlyRootfs": false,
"Dns": [
"8.8.8.8"
],
"DnsOptions": [
""
],
"DnsSearch": [
""
],
"VolumesFrom": [
"parent",
"other:ro"
],
"CapAdd": [
"NET_ADMIN"
],
"CapDrop": [
"MKNOD"
],
"GroupAdd": [
"newgroup"
],
"RestartPolicy": {
"Name": "",
"MaximumRetryCount": 0
},
"AutoRemove": true,
"NetworkMode": "bridge",
"Devices": [ ],
"Ulimits": [
{ }
],
"LogConfig": {
"Type": "json-file",
"Config": { }
},
"SecurityOpt": [ ],
"StorageOpt": { },
"CgroupParent": "",
"VolumeDriver": "",
"ShmSize": 67108864
},
"NetworkingConfig": {
"EndpointsConfig": {
"isolated_nw": {
"IPAMConfig": {
"IPv4Address": "172.20.30.33",
"IPv6Address": "2001:db8:abcd::3033",
"LinkLocalIPs": [
"169.254.34.68",
"fe80::3468"
]
},
"Links": [
"container_1",
"container_2"
],
"Aliases": [
"server_x",
"server_y"
]
},
"database_nw": { }
}
}
}`

### Response samples

* 201
* 400
* 404
* 409
* 500

Content type

application/json

`{
"Id": "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743",
"Warnings": [ ]
}`

## [](#tag/Container/operation/ContainerInspect)Inspect a container

Return low-level information about a container.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|      |                                                                                       |
| ---- | ------------------------------------------------------------------------------------- |
| size | booleanDefault: falseReturn the size of container as fields `SizeRw` and `SizeRootFs` |

### Responses

/v1.47/containers/{id}/json

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"AppArmorProfile": "",
"Args": [
"-c",
"exit 9"
],
"Config": {
"AttachStderr": true,
"AttachStdin": false,
"AttachStdout": true,
"Cmd": [
"/bin/sh",
"-c",
"exit 9"
],
"Domainname": "",
"Env": [
"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
],
"Healthcheck": {
"Test": [
"CMD-SHELL",
"exit 0"
]
},
"Hostname": "ba033ac44011",
"Image": "ubuntu",
"Labels": {
"com.example.vendor": "Acme",
"com.example.license": "GPL",
"com.example.version": "1.0"
},
"MacAddress": "",
"NetworkDisabled": false,
"OpenStdin": false,
"StdinOnce": false,
"Tty": false,
"User": "",
"Volumes": {
"/volumes/data": { }
},
"WorkingDir": "",
"StopSignal": "SIGTERM",
"StopTimeout": 10
},
"Created": "2015-01-06T15:47:31.485331387Z",
"Driver": "overlay2",
"ExecIDs": [
"b35395de42bc8abd327f9dd65d913b9ba28c74d2f0734eeeae84fa1c616a0fca",
"3fc1232e5cd20c8de182ed81178503dc6437f4e7ef12b52cc5e8de020652f1c4"
],
"HostConfig": {
"MaximumIOps": 0,
"MaximumIOBps": 0,
"BlkioWeight": 0,
"BlkioWeightDevice": [
{ }
],
"BlkioDeviceReadBps": [
{ }
],
"BlkioDeviceWriteBps": [
{ }
],
"BlkioDeviceReadIOps": [
{ }
],
"BlkioDeviceWriteIOps": [
{ }
],
"ContainerIDFile": "",
"CpusetCpus": "",
"CpusetMems": "",
"CpuPercent": 80,
"CpuShares": 0,
"CpuPeriod": 100000,
"CpuRealtimePeriod": 1000000,
"CpuRealtimeRuntime": 10000,
"Devices": [ ],
"DeviceRequests": [
{
"Driver": "nvidia",
"Count": -1,
"DeviceIDs"": [
"0",
"1",
"GPU-fef8089b-4820-abfc-e83e-94318197576e"
],
"Capabilities": [ [
"gpu",
"nvidia",
"compute"
]
],
"Options": {
"property1": "string",
"property2": "string"
}
}
],
"IpcMode": "",
"Memory": 0,
"MemorySwap": 0,
"MemoryReservation": 0,
"OomKillDisable": false,
"OomScoreAdj": 500,
"NetworkMode": "bridge",
"PidMode": "",
"PortBindings": { },
"Privileged": false,
"ReadonlyRootfs": false,
"PublishAllPorts": false,
"RestartPolicy": {
"MaximumRetryCount": 2,
"Name": "on-failure"
},
"LogConfig": {
"Type": "json-file"
},
"Sysctls": {
"net.ipv4.ip_forward": "1"
},
"Ulimits": [
{ }
],
"VolumeDriver": "",
"ShmSize": 67108864
},
"HostnamePath": "/var/lib/docker/containers/ba033ac4401106a3b513bc9d639eee123ad78ca3616b921167cd74b20e25ed39/hostname",
"HostsPath": "/var/lib/docker/containers/ba033ac4401106a3b513bc9d639eee123ad78ca3616b921167cd74b20e25ed39/hosts",
"LogPath": "/var/lib/docker/containers/1eb5fabf5a03807136561b3c00adcd2992b535d624d5e18b6cdc6a6844d9767b/1eb5fabf5a03807136561b3c00adcd2992b535d624d5e18b6cdc6a6844d9767b-json.log",
"Id": "ba033ac4401106a3b513bc9d639eee123ad78ca3616b921167cd74b20e25ed39",
"Image": "04c5d3b7b0656168630d3ba35d8889bd0e9caafcaeb3004d2bfbc47e7c5d35d2",
"MountLabel": "",
"Name": "/boring_euclid",
"NetworkSettings": {
"Bridge": "",
"SandboxID": "",
"HairpinMode": false,
"LinkLocalIPv6Address": "",
"LinkLocalIPv6PrefixLen": 0,
"SandboxKey": "",
"EndpointID": "",
"Gateway": "",
"GlobalIPv6Address": "",
"GlobalIPv6PrefixLen": 0,
"IPAddress": "",
"IPPrefixLen": 0,
"IPv6Gateway": "",
"MacAddress": "",
"Networks": {
"bridge": {
"NetworkID": "7ea29fc1412292a2d7bba362f9253545fecdfa8ce9a6e37dd10ba8bee7129812",
"EndpointID": "7587b82f0dada3656fda26588aee72630c6fab1536d36e394b2bfbcf898c971d",
"Gateway": "172.17.0.1",
"IPAddress": "172.17.0.2",
"IPPrefixLen": 16,
"IPv6Gateway": "",
"GlobalIPv6Address": "",
"GlobalIPv6PrefixLen": 0,
"MacAddress": "02:42:ac:12:00:02"
}
}
},
"Path": "/bin/sh",
"ProcessLabel": "",
"ResolvConfPath": "/var/lib/docker/containers/ba033ac4401106a3b513bc9d639eee123ad78ca3616b921167cd74b20e25ed39/resolv.conf",
"RestartCount": 1,
"State": {
"Error": "",
"ExitCode": 9,
"FinishedAt": "2015-01-06T15:47:32.080254511Z",
"Health": {
"Status": "healthy",
"FailingStreak": 0,
"Log": [
{
"Start": "2019-12-22T10:59:05.6385933Z",
"End": "2019-12-22T10:59:05.8078452Z",
"ExitCode": 0,
"Output": ""
}
]
},
"OOMKilled": false,
"Dead": false,
"Paused": false,
"Pid": 0,
"Restarting": false,
"Running": true,
"StartedAt": "2015-01-06T15:47:32.072697474Z",
"Status": "running"
},
"Mounts": [
{
"Name": "fac362...80535",
"Source": "/data",
"Destination": "/data",
"Driver": "local",
"Mode": "ro,Z",
"RW": false,
"Propagation": ""
}
]
}`

## [](#tag/Container/operation/ContainerTop)List processes running inside a container

On Unix systems, this is done by running the `ps` command. This endpoint is not supported on Windows.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|          |                                                                       |
| -------- | --------------------------------------------------------------------- |
| ps\_args | stringDefault: "-ef"The arguments to pass to `ps`. For example, `aux` |

### Responses

/v1.47/containers/{id}/top

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Titles": [
"UID",
"PID",
"PPID",
"C",
"STIME",
"TTY",
"TIME",
"CMD"
],
"Processes": [ [
"root",
"13642",
"882",
"0",
"17:03",
"pts/0",
"00:00:00",
"/bin/bash"
], [
"root",
"13735",
"13642",
"0",
"17:06",
"pts/0",
"00:00:00",
"sleep 10"
]
]
}`

## [](#tag/Container/operation/ContainerLogs)Get container logs

Get `stdout` and `stderr` logs from a container.

Note: This endpoint works only for containers with the `json-file` or `journald` logging driver.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|            |                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| follow     | booleanDefault: falseKeep connection after returning logs.                                                                                 |
| stdout     | booleanDefault: falseReturn logs from `stdout`                                                                                             |
| stderr     | booleanDefault: falseReturn logs from `stderr`                                                                                             |
| since      | integerDefault: 0Only return logs since this time, as a UNIX timestamp                                                                     |
| until      | integerDefault: 0Only return logs before this time, as a UNIX timestamp                                                                    |
| timestamps | booleanDefault: falseAdd timestamps to every log line                                                                                      |
| tail       | stringDefault: "all"Only return this number of log lines from the end of the logs. Specify as an integer or `all` to output all log lines. |

### Responses

/v1.47/containers/{id}/logs

### Response samples

* 404

Content type

application/vnd.docker.raw-stream

No sample

## [](#tag/Container/operation/ContainerChanges)Get changes on a container’s filesystem

Returns which files in a container's filesystem have been added, deleted, or modified. The `Kind` of modification can be one of:

* `0`: Modified ("C")
* `1`: Added ("A")
* `2`: Deleted ("D")

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

### Responses

/v1.47/containers/{id}/changes

### Response samples

* 200
* 404
* 500

Content type

application/json

`[
{
"Path": "/dev",
"Kind": 0
},
{
"Path": "/dev/kmsg",
"Kind": 1
},
{
"Path": "/test",
"Kind": 1
}
]`

## [](#tag/Container/operation/ContainerExport)Export a container

Export the contents of a container as a tarball.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

### Responses

/v1.47/containers/{id}/export

### Response samples

* 404

Content type

application/octet-stream

No sample

## [](#tag/Container/operation/ContainerStats)Get container stats based on resource usage

This endpoint returns a live stream of a container’s resource usage statistics.

The `precpu_stats` is the CPU statistic of the *previous* read, and is used to calculate the CPU usage percentage. It is not an exact copy of the `cpu_stats` field.

If either `precpu_stats.online_cpus` or `cpu_stats.online_cpus` is nil then for compatibility with older daemons the length of the corresponding `cpu_usage.percpu_usage` array should be used.

On a cgroup v2 host, the following fields are not set

* `blkio_stats`: all fields other than `io_service_bytes_recursive`
* `cpu_stats`: `cpu_usage.percpu_usage`
* `memory_stats`: `max_usage` and `failcnt` Also, `memory_stats.stats` fields are incompatible with cgroup v1.

To calculate the values shown by the `stats` command of the docker cli tool the following formulas can be used:

* used\_memory = `memory_stats.usage - memory_stats.stats.cache` (cgroups v1)
* used\_memory = `memory_stats.usage - memory_stats.stats.inactive_file` (cgroups v2)
* available\_memory = `memory_stats.limit`
* Memory usage % = `(used_memory / available_memory) * 100.0`
* cpu\_delta = `cpu_stats.cpu_usage.total_usage - precpu_stats.cpu_usage.total_usage`
* system\_cpu\_delta = `cpu_stats.system_cpu_usage - precpu_stats.system_cpu_usage`
* number\_cpus = `length(cpu_stats.cpu_usage.percpu_usage)` or `cpu_stats.online_cpus`
* CPU usage % = `(cpu_delta / system_cpu_delta) * number_cpus * 100.0`

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|          |                                                                                                                |
| -------- | -------------------------------------------------------------------------------------------------------------- |
| stream   | booleanDefault: trueStream the output. If false, the stats will be output once and then it will disconnect.    |
| one-shot | booleanDefault: falseOnly get a single stat instead of waiting for 2 cycles. Must be used with `stream=false`. |

### Responses

/v1.47/containers/{id}/stats

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"read": "2015-01-08T22:57:31.547920715Z",
"pids_stats": {
"current": 3
},
"networks": {
"eth0": {
"rx_bytes": 5338,
"rx_dropped": 0,
"rx_errors": 0,
"rx_packets": 36,
"tx_bytes": 648,
"tx_dropped": 0,
"tx_errors": 0,
"tx_packets": 8
},
"eth5": {
"rx_bytes": 4641,
"rx_dropped": 0,
"rx_errors": 0,
"rx_packets": 26,
"tx_bytes": 690,
"tx_dropped": 0,
"tx_errors": 0,
"tx_packets": 9
}
},
"memory_stats": {
"stats": {
"total_pgmajfault": 0,
"cache": 0,
"mapped_file": 0,
"total_inactive_file": 0,
"pgpgout": 414,
"rss": 6537216,
"total_mapped_file": 0,
"writeback": 0,
"unevictable": 0,
"pgpgin": 477,
"total_unevictable": 0,
"pgmajfault": 0,
"total_rss": 6537216,
"total_rss_huge": 6291456,
"total_writeback": 0,
"total_inactive_anon": 0,
"rss_huge": 6291456,
"hierarchical_memory_limit": 67108864,
"total_pgfault": 964,
"total_active_file": 0,
"active_anon": 6537216,
"total_active_anon": 6537216,
"total_pgpgout": 414,
"total_cache": 0,
"inactive_anon": 0,
"active_file": 0,
"pgfault": 964,
"inactive_file": 0,
"total_pgpgin": 477
},
"max_usage": 6651904,
"usage": 6537216,
"failcnt": 0,
"limit": 67108864
},
"blkio_stats": { },
"cpu_stats": {
"cpu_usage": {
"percpu_usage": [
8646879,
24472255,
36438778,
30657443
],
"usage_in_usermode": 50000000,
"total_usage": 100215355,
"usage_in_kernelmode": 30000000
},
"system_cpu_usage": 739306590000000,
"online_cpus": 4,
"throttling_data": {
"periods": 0,
"throttled_periods": 0,
"throttled_time": 0
}
},
"precpu_stats": {
"cpu_usage": {
"percpu_usage": [
8646879,
24350896,
36438778,
30657443
],
"usage_in_usermode": 50000000,
"total_usage": 100093996,
"usage_in_kernelmode": 30000000
},
"system_cpu_usage": 9492140000000,
"online_cpus": 4,
"throttling_data": {
"periods": 0,
"throttled_periods": 0,
"throttled_time": 0
}
}
}`

## [](#tag/Container/operation/ContainerResize)Resize a container TTY

Resize the TTY for a container.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|           |                                                |
| --------- | ---------------------------------------------- |
| hrequired | integerHeight of the TTY session in characters |
| wrequired | integerWidth of the TTY session in characters  |

### Responses

/v1.47/containers/{id}/resize

### Response samples

* 404

Content type

text/plain

No sample

## [](#tag/Container/operation/ContainerStart)Start a container

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|            |                                                                                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| detachKeys | stringOverride the key sequence for detaching a container. Format is a single character `[a-Z]` or `ctrl-<value>` where `<value>` is one of: `a-z`, `@`, `^`, `[`, `,` or `_`. |

### Responses

/v1.47/containers/{id}/start

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerStop)Stop a container

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|        |                                                                                |
| ------ | ------------------------------------------------------------------------------ |
| signal | stringSignal to send to the container as an integer or string (e.g. `SIGINT`). |
| t      | integerNumber of seconds to wait before killing the container                  |

### Responses

/v1.47/containers/{id}/stop

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerRestart)Restart a container

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|        |                                                                                |
| ------ | ------------------------------------------------------------------------------ |
| signal | stringSignal to send to the container as an integer or string (e.g. `SIGINT`). |
| t      | integerNumber of seconds to wait before killing the container                  |

### Responses

/v1.47/containers/{id}/restart

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerKill)Kill a container

Send a POSIX signal to a container, defaulting to killing to the container.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|        |                                                                                                  |
| ------ | ------------------------------------------------------------------------------------------------ |
| signal | stringDefault: "SIGKILL"Signal to send to the container as an integer or string (e.g. `SIGINT`). |

### Responses

/v1.47/containers/{id}/kill

### Response samples

* 404
* 409
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerUpdate)Update a container

Change various configuration options of a container without having to recreate it.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### Request Body schema: application/jsonrequired

|                    |                                                                                                                                                                                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| CpuShares          | integerAn integer value representing this container's relative CPU weight versus other containers.                                                                                                                                                     |
| Memory             | integer \<int64>Default: 0Memory limit in bytes.                                                                                                                                                                                                       |
| CgroupParent       | stringPath to `cgroups` under which the container's `cgroup` is created. If the path is not absolute, the path is considered to be relative to the `cgroups` path of the init process. Cgroups are created if they do not already exist.               |
| BlkioWeight        | integer \[ 0 .. 1000 ]Block IO weight (relative weight).                                                                                                                                                                                               |
|                    | Array of objectsBlock IO weight (relative device weight) in the form:```
[{"Path": "device_path", "Weight": weight}]
```                                                                                                                               |
|                    | Array of objects (ThrottleDevice)Limit read rate (bytes per second) from a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                         |
|                    | Array of objects (ThrottleDevice)Limit write rate (bytes per second) to a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                          |
|                    | Array of objects (ThrottleDevice)Limit read rate (IO per second) from a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                            |
|                    | Array of objects (ThrottleDevice)Limit write rate (IO per second) to a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                             |
| CpuPeriod          | integer \<int64>The length of a CPU period in microseconds.                                                                                                                                                                                            |
| CpuQuota           | integer \<int64>Microseconds of CPU time that the container can get in a CPU period.                                                                                                                                                                   |
| CpuRealtimePeriod  | integer \<int64>The length of a CPU real-time period in microseconds. Set to 0 to allocate no time allocated to real-time tasks.                                                                                                                       |
| CpuRealtimeRuntime | integer \<int64>The length of a CPU real-time runtime in microseconds. Set to 0 to allocate no time allocated to real-time tasks.                                                                                                                      |
| CpusetCpus         | stringCPUs in which to allow execution (e.g., `0-3`, `0,1`).                                                                                                                                                                                           |
| CpusetMems         | stringMemory nodes (MEMs) in which to allow execution (0-3, 0,1). Only effective on NUMA systems.                                                                                                                                                      |
|                    | Array of objects (DeviceMapping)A list of devices to add to the container.                                                                                                                                                                             |
| DeviceCgroupRules  | Array of stringsa list of cgroup rules to apply to the container                                                                                                                                                                                       |
|                    | Array of objects (DeviceRequest)A list of requests for devices to be sent to device drivers.                                                                                                                                                           |
| KernelMemoryTCP    | integer \<int64>Hard limit for kernel TCP buffer memory (in bytes). Depending on the OCI runtime in use, this option may be ignored. It is no longer supported by the default (runc) runtime.This field is omitted when empty.                         |
| MemoryReservation  | integer \<int64>Memory soft limit in bytes.                                                                                                                                                                                                            |
| MemorySwap         | integer \<int64>Total memory limit (memory + swap). Set as `-1` to enable unlimited swap.                                                                                                                                                              |
| MemorySwappiness   | integer \<int64> \[ 0 .. 100 ]Tune a container's memory swappiness behavior. Accepts an integer between 0 and 100.                                                                                                                                     |
| NanoCpus           | integer \<int64>CPU quota in units of 10-9 CPUs.                                                                                                                                                                                                       |
| OomKillDisable     | booleanDisable OOM Killer for the container.                                                                                                                                                                                                           |
| Init               | boolean or nullRun an init inside the container that forwards signals and reaps processes. This field is omitted if empty, and the default (as configured on the daemon) is used.                                                                      |
| PidsLimit          | integer or null \<int64>Tune a container's PIDs limit. Set `0` or `-1` for unlimited, or `null` to not change.                                                                                                                                         |
|                    | Array of objectsA list of resource limits to set in the container. For example:```
{"Name": "nofile", "Soft": 1024, "Hard": 2048}
```                                                                                                                  |
| CpuCount           | integer \<int64>The number of usable CPUs (Windows only).On Windows Server containers, the processor resource controls are mutually exclusive. The order of precedence is `CPUCount` first, then `CPUShares`, and `CPUPercent` last.                   |
| CpuPercent         | integer \<int64>The usable percentage of the available CPUs (Windows only).On Windows Server containers, the processor resource controls are mutually exclusive. The order of precedence is `CPUCount` first, then `CPUShares`, and `CPUPercent` last. |
| IOMaximumIOps      | integer \<int64>Maximum IOps for the container system drive (Windows only)                                                                                                                                                                             |
| IOMaximumBandwidth | integer \<int64>Maximum IO in bytes per second for the container system drive (Windows only).                                                                                                                                                          |
|                    | object (RestartPolicy)The behavior to apply when the container exits. The default is not to restart.An ever increasing delay (double the previous delay, starting at 100ms) is added before each restart to prevent flooding the server.               |

### Responses

/v1.47/containers/{id}/update

### Request samples

* Payload

Content type

application/json

`{
"BlkioWeight": 300,
"CpuShares": 512,
"CpuPeriod": 100000,
"CpuQuota": 50000,
"CpuRealtimePeriod": 1000000,
"CpuRealtimeRuntime": 10000,
"CpusetCpus": "0,1",
"CpusetMems": "0",
"Memory": 314572800,
"MemorySwap": 514288000,
"MemoryReservation": 209715200,
"RestartPolicy": {
"MaximumRetryCount": 4,
"Name": "on-failure"
}
}`

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Warnings": [
"string"
]
}`

## [](#tag/Container/operation/ContainerRename)Rename a container

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|              |                                  |
| ------------ | -------------------------------- |
| namerequired | stringNew name for the container |

### Responses

/v1.47/containers/{id}/rename

### Response samples

* 404
* 409
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerPause)Pause a container

Use the freezer cgroup to suspend all processes in a container.

Traditionally, when suspending a process the `SIGSTOP` signal is used, which is observable by the process being suspended. With the freezer cgroup the process is unaware, and unable to capture, that it is being suspended, and subsequently resumed.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

### Responses

/v1.47/containers/{id}/pause

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerUnpause)Unpause a container

Resume a container which has been paused.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

### Responses

/v1.47/containers/{id}/unpause

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "No such container: c2ada9df5af8"
}`

## [](#tag/Container/operation/ContainerAttach)Attach to a container

Attach to a container to read its output or send it input. You can attach to the same container multiple times and you can reattach to containers that have been detached.

Either the `stream` or `logs` parameter must be `true` for this endpoint to do anything.

See the [documentation for the `docker attach` command](https://docs.docker.com/engine/reference/commandline/attach/) for more details.

### Hijacking

This endpoint hijacks the HTTP connection to transport `stdin`, `stdout`, and `stderr` on the same socket.

This is the response from the daemon for an attach request:

```
HTTP/1.1 200 OK
Content-Type: application/vnd.docker.raw-stream

[STREAM]
```

After the headers and two new lines, the TCP connection can now be used for raw, bidirectional communication between the client and server.

To hint potential proxies about connection hijacking, the Docker client can also optionally send connection upgrade headers.

For example, the client sends this request to upgrade the connection:

```
POST /containers/16253994b7c4/attach?stream=1&stdout=1 HTTP/1.1
Upgrade: tcp
Connection: Upgrade
```

The Docker daemon will respond with a `101 UPGRADED` response, and will similarly follow with the raw stream:

```
HTTP/1.1 101 UPGRADED
Content-Type: application/vnd.docker.raw-stream
Connection: Upgrade
Upgrade: tcp

[STREAM]
```

### Stream format

When the TTY setting is disabled in [`POST /containers/create`](#operation/ContainerCreate), the HTTP Content-Type header is set to application/vnd.docker.multiplexed-stream and the stream over the hijacked connected is multiplexed to separate out `stdout` and `stderr`. The stream consists of a series of frames, each containing a header and a payload.

The header contains the information which the stream writes (`stdout` or `stderr`). It also contains the size of the associated frame encoded in the last four bytes (`uint32`).

It is encoded on the first eight bytes like this:

```go
header := [8]byte{STREAM_TYPE, 0, 0, 0, SIZE1, SIZE2, SIZE3, SIZE4}
```

`STREAM_TYPE` can be:

* 0: `stdin` (is written on `stdout`)
* 1: `stdout`
* 2: `stderr`

`SIZE1, SIZE2, SIZE3, SIZE4` are the four bytes of the `uint32` size encoded as big endian.

Following the header is the payload, which is the specified number of bytes of `STREAM_TYPE`.

The simplest way to implement this protocol is the following:

1. Read 8 bytes.
2. Choose `stdout` or `stderr` depending on the first byte.
3. Extract the frame size from the last four bytes.
4. Read the extracted size and output it on the correct output.
5. Goto 1.

### Stream format when using a TTY

When the TTY setting is enabled in [`POST /containers/create`](#operation/ContainerCreate), the stream is not multiplexed. The data exchanged over the hijacked connection is simply the raw data from the process PTY and client's `stdin`.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|            |                                                                                                                                                                                                                                                                                                                                   |
| ---------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| detachKeys | stringOverride the key sequence for detaching a container.Format is a single character `[a-Z]` or `ctrl-<value>` where `<value>` is one of: `a-z`, `@`, `^`, `[`, `,` or `_`.                                                                                                                                                     |
| logs       | booleanDefault: falseReplay previous logs from the container.This is useful for attaching to a container that has started and you want to output everything since the container started.If `stream` is also enabled, once all the previous output has been returned, it will seamlessly transition into streaming current output. |
| stream     | booleanDefault: falseStream attached streams from the time the request was made onwards.                                                                                                                                                                                                                                          |
| stdin      | booleanDefault: falseAttach to `stdin`                                                                                                                                                                                                                                                                                            |
| stdout     | booleanDefault: falseAttach to `stdout`                                                                                                                                                                                                                                                                                           |
| stderr     | booleanDefault: falseAttach to `stderr`                                                                                                                                                                                                                                                                                           |

### Responses

/v1.47/containers/{id}/attach

### Response samples

* 404

Content type

application/vnd.docker.raw-stream

No sample

## [](#tag/Container/operation/ContainerAttachWebsocket)Attach to a container via a websocket

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|            |                                                                                                                                                                                |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| detachKeys | stringOverride the key sequence for detaching a container.Format is a single character `[a-Z]` or `ctrl-<value>` where `<value>` is one of: `a-z`, `@`, `^`, `[`, `,`, or `_`. |
| logs       | booleanDefault: falseReturn logs                                                                                                                                               |
| stream     | booleanDefault: falseReturn stream                                                                                                                                             |
| stdin      | booleanDefault: falseAttach to `stdin`                                                                                                                                         |
| stdout     | booleanDefault: falseAttach to `stdout`                                                                                                                                        |
| stderr     | booleanDefault: falseAttach to `stderr`                                                                                                                                        |

### Responses

/v1.47/containers/{id}/attach/ws

### Response samples

* 400
* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Container/operation/ContainerWait)Wait for a container

Block until a container stops, then returns the exit code.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|           |                                                                                                                                                                              |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| condition | stringDefault: "not-running"Enum: "not-running" "next-exit" "removed"Wait until a container state reaches the given condition.Defaults to `not-running` if omitted or empty. |

### Responses

/v1.47/containers/{id}/wait

### Response samples

* 200
* 400
* 404
* 500

Content type

application/json

`{
"StatusCode": 0,
"Error": {
"Message": "string"
}
}`

## [](#tag/Container/operation/ContainerDelete)Remove a container

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|       |                                                                               |
| ----- | ----------------------------------------------------------------------------- |
| v     | booleanDefault: falseRemove anonymous volumes associated with the container.  |
| force | booleanDefault: falseIf the container is running, kill it before removing it. |
| link  | booleanDefault: falseRemove the specified link associated with the container. |

### Responses

/v1.47/containers/{id}

### Response samples

* 400
* 404
* 409
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Container/operation/ContainerArchiveInfo)Get information about files in a container

A response header `X-Docker-Container-Path-Stat` is returned, containing a base64 - encoded JSON object with some filesystem header information about the path.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|              |                                                          |
| ------------ | -------------------------------------------------------- |
| pathrequired | stringResource in the container’s filesystem to archive. |

### Responses

/v1.47/containers/{id}/archive

### Response samples

* 400
* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Container/operation/ContainerArchive)Get an archive of a filesystem resource in a container

Get a tar archive of a resource in the filesystem of container id.

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|              |                                                          |
| ------------ | -------------------------------------------------------- |
| pathrequired | stringResource in the container’s filesystem to archive. |

### Responses

/v1.47/containers/{id}/archive

### Response samples

* 404

Content type

application/x-tar

No sample

## [](#tag/Container/operation/PutContainerArchive)Extract an archive of files or folders to a directory in a container

Upload a tar archive to be extracted to a path in the filesystem of container id. `path` parameter is asserted to be a directory. If it exists as a file, 400 error will be returned with message "not a directory".

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

##### query Parameters

|                      |                                                                                                                                                                               |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| pathrequired         | stringPath to a directory in the container to extract the archive’s contents into.                                                                                            |
| noOverwriteDirNonDir | stringIf `1`, `true`, or `True` then it will be an error if unpacking the given content would cause an existing directory to be replaced with a non-directory and vice versa. |
| copyUIDGID           | stringIf `1`, `true`, then it will copy UID/GID maps to the dest file or dir                                                                                                  |

##### Request Body schema:application/x-tarrequired

The input stream must be a tar archive compressed with one of the following algorithms: `identity` (no compression), `gzip`, `bzip2`, or `xz`.

string \<binary>

### Responses

/v1.47/containers/{id}/archive

### Response samples

* 400
* 403
* 404
* 500

Content type

application/json

`{
"message": "not a directory"
}`

## [](#tag/Container/operation/ContainerPrune)Delete stopped containers

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringFilters to process on the prune list, encoded as JSON (a `map[string][]string`).Available filters:- `until=<timestamp>` Prune containers created before this timestamp. The `<timestamp>` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. `10m`, `1h30m`) computed relative to the daemon machine’s time.
- `label` (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) Prune containers with (or without, in case `label!=...` is used) the specified labels. |

### Responses

/v1.47/containers/prune

### Response samples

* 200
* 500

Content type

application/json

`{
"ContainersDeleted": [
"string"
],
"SpaceReclaimed": 0
}`

## [](#tag/Image)Images

## [](#tag/Image/operation/ImageList)List Images

Returns a list of images on the server. Note that it uses a different, smaller representation of an image than inspecting a single image.

##### query Parameters

|             |                                                                                                                                                                                                                                                                                                                                                                                                      |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| all         | booleanDefault: falseShow all images. Only images from a final layer (no children) are shown by default.                                                                                                                                                                                                                                                                                             |
| filters     | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the images list.Available filters:- `before`=(`<image-name>[:<tag>]`, `<image id>` or `<image@digest>`)
- `dangling=true`
- `label=key` or `label="key=value"` of an image label
- `reference`=(`<image-name>[:<tag>]`)
- `since`=(`<image-name>[:<tag>]`, `<image id>` or `<image@digest>`)
- `until=<timestamp>` |
| shared-size | booleanDefault: falseCompute and show shared size as a `SharedSize` field on each image.                                                                                                                                                                                                                                                                                                             |
| digests     | booleanDefault: falseShow digest information as a `RepoDigests` field on each image.                                                                                                                                                                                                                                                                                                                 |
| manifests   | booleanDefault: falseInclude `Manifests` in the image summary.                                                                                                                                                                                                                                                                                                                                       |

### Responses

/v1.47/images/json

### Response samples

* 200
* 500

Content type

application/json

`[
{
"Id": "sha256:ec3f0931a6e6b6855d76b2d7b0be30e81860baccd891b2e243280bf1cd8ad710",
"ParentId": "",
"RepoTags": [
"example:1.0",
"example:latest",
"example:stable",
"internal.registry.example.com:5000/example:1.0"
],
"RepoDigests": [
"example@sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb",
"internal.registry.example.com:5000/example@sha256:b69959407d21e8a062e0416bf13405bb2b71ed7a84dde4158ebafacfa06f5578"
],
"Created": "1644009612",
"Size": 172064416,
"SharedSize": 1239828,
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Containers": 2,
"Manifests": [
{
"ID": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f",
"Descriptor": {
"mediaType": "application/vnd.docker.distribution.manifest.v2+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 3987495
},
"Available": true,
"Size": {
"Total": 8213251,
"Content": 3987495
},
"Kind": "image",
"ImageData": {
"Platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"Containers": [
"ede54ee1fda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c7430",
"abadbce344c096744d8d6071a90d474d28af8f1034b5ea9fb03c3f4bfc6d005e"
],
"Size": {
"Unpacked": 3987495
}
},
"AttestationData": {
"For": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f"
}
}
]
}
]`

## [](#tag/Image/operation/ImageBuild)Build an image

Build an image from a tar archive with a `Dockerfile` in it.

The `Dockerfile` specifies how the image is built from the tar archive. It is typically in the archive's root, but can be at a different path or have a different name by specifying the `dockerfile` parameter. [See the `Dockerfile` reference for more information](https://docs.docker.com/engine/reference/builder/).

The Docker daemon performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. After that, each instruction is run one-by-one until the ID of the new image is output.

The build is canceled if the client drops the connection by quitting or being killed.

##### query Parameters

|             |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| dockerfile  | stringDefault: "Dockerfile"Path within the build context to the `Dockerfile`. This is ignored if `remote` is specified and points to an external `Dockerfile`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| t           | stringA name and optional tag to apply to the image in the `name:tag` format. If you omit the tag the default `latest` value is assumed. You can provide several `t` parameters.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| extrahosts  | stringExtra hosts to add to /etc/hosts                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| remote      | stringA Git repository URI or HTTP/HTTPS context URI. If the URI points to a single text file, the file’s contents are placed into a file called `Dockerfile` and the image is built from that file. If the URI points to a tarball, the file is downloaded by the daemon and the contents therein used as the context for the build. If the URI points to a tarball and the `dockerfile` parameter is also specified, there must be a file with the corresponding path inside the tarball.                                                                                                                                        |
| q           | booleanDefault: falseSuppress verbose build output.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| nocache     | booleanDefault: falseDo not use the cache when building the image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| cachefrom   | stringJSON array of images used for build cache resolution.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| pull        | stringAttempt to pull the image even if an older image exists locally.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| rm          | booleanDefault: trueRemove intermediate containers after a successful build.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| forcerm     | booleanDefault: falseAlways remove intermediate containers, even upon failure.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| memory      | integerSet memory limit for build.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| memswap     | integerTotal memory (memory + swap). Set as `-1` to disable swap.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| cpushares   | integerCPU shares (relative weight).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| cpusetcpus  | stringCPUs in which to allow execution (e.g., `0-3`, `0,1`).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| cpuperiod   | integerThe length of a CPU period in microseconds.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| cpuquota    | integerMicroseconds of CPU time that the container can get in a CPU period.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| buildargs   | stringJSON map of string pairs for build-time variables. Users pass these values at build-time. Docker uses the buildargs as the environment context for commands run via the `Dockerfile` RUN instruction, or for variable expansion in other `Dockerfile` instructions. This is not meant for passing secret values.For example, the build arg `FOO=bar` would become `{"FOO":"bar"}` in JSON. This would result in the query parameter `buildargs={"FOO":"bar"}`. Note that `{"FOO":"bar"}` should be URI component encoded.[Read more about the buildargs instruction.](https://docs.docker.com/engine/reference/builder/#arg) |
| shmsize     | integerSize of `/dev/shm` in bytes. The size must be greater than 0. If omitted the system uses 64MB.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| squash      | booleanSquash the resulting images layers into a single layer. *(Experimental release only.)*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| labels      | stringArbitrary key/value labels to set on the image, as a JSON map of string pairs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| networkmode | stringSets the networking mode for the run commands during build. Supported standard values are: `bridge`, `host`, `none`, and `container:<name\|id>`. Any other value is taken as a custom network's name or ID to which this container should connect to.                                                                                                                                                                                                                                                                                                                                                                        |
| platform    | stringDefault: ""Platform in the format os\[/arch\[/variant]]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| target      | stringDefault: ""Target build stage                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| outputs     | stringDefault: ""BuildKit output configuration in the format of a stringified JSON array of objects. Each object must have two top-level properties: `Type` and `Attrs`. The `Type` property must be set to 'moby'. The `Attrs` property is a map of attributes for the BuildKit output configuration. See <https://docs.docker.com/build/exporters/oci-docker/> for more information.Example:```
[{"Type":"moby","Attrs":{"type":"image","force-compression":"true","compression":"zstd"}}]
```                                                                                                                                   |
| version     | stringDefault: "1"Enum: "1" "2"Version of the builder backend to use.- `1` is the first generation classic (deprecated) builder in the Docker daemon (default)
- `2` is [BuildKit](https://github.com/moby/buildkit)                                                                                                                                                                                                                                                                                                                                                                                                               |

##### header Parameters

|                   |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Content-type      | stringDefault: application/x-tarValue: "application/x-tar"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| X-Registry-Config | stringThis is a base64-encoded JSON object with auth configurations for multiple registries that a build may refer to.The key is a registry URL, and the value is an auth configuration object, [as described in the authentication section](#section/Authentication). For example:```
{
  "docker.example.com": {
    "username": "janedoe",
    "password": "hunter2"
  },
  "https://index.docker.io/v1/": {
    "username": "mobydock",
    "password": "conta1n3rize14"
  }
}
```Only the registry domain name (and port if not the default 443) are required. However, for legacy reasons, the Docker Hub registry must be specified with both a `https://` prefix and a `/v1/` suffix even though Docker will prefer to use the v2 registry API. |

##### Request Body schema: application/octet-stream

A tar archive compressed with one of the following algorithms: identity (no compression), gzip, bzip2, xz.

string \<binary>

### Responses

/v1.47/build

### Response samples

* 400
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Image/operation/BuildPrune)Delete builder cache

##### query Parameters

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| keep-storage | integer \<int64>Amount of disk space in bytes to keep for cache                                                                                                                                                                                                                                                                                                                                                                                                          |
| all          | booleanRemove all types of build cache                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| filters      | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the list of build cache objects.Available filters:- `until=<timestamp>` remove cache older than `<timestamp>`. The `<timestamp>` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. `10m`, `1h30m`) computed relative to the daemon's local time.
- `id=<id>`
- `parent=<id>`
- `type=<string>`
- `description=<string>`
- `inuse`
- `shared`
- `private` |

### Responses

/v1.47/build/prune

### Response samples

* 200
* 500

Content type

application/json

`{
"CachesDeleted": [
"string"
],
"SpaceReclaimed": 0
}`

## [](#tag/Image/operation/ImageCreate)Create an image

Pull or import an image.

##### query Parameters

|           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| fromImage | stringName of the image to pull. The name may include a tag or digest. This parameter may only be used when pulling an image. The pull is cancelled if the HTTP connection is closed.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| fromSrc   | stringSource to import. The value may be a URL from which the image can be retrieved or `-` to read the image from the request body. This parameter may only be used when importing an image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| repo      | stringRepository name given to an image when it is imported. The repo may include a tag. This parameter may only be used when importing an image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| tag       | stringTag or digest. If empty when pulling an image, this causes all tags for the given image to be pulled.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| message   | stringSet commit message for imported image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| changes   | Array of stringsApply `Dockerfile` instructions to the image that is created, for example: `changes=ENV DEBUG=true`. Note that `ENV DEBUG=true` should be URI component encoded.Supported `Dockerfile` instructions: `CMD`\|`ENTRYPOINT`\|`ENV`\|`EXPOSE`\|`ONBUILD`\|`USER`\|`VOLUME`\|`WORKDIR`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| platform  | stringDefault: ""Platform in the format os\[/arch\[/variant]].When used in combination with the `fromImage` option, the daemon checks if the given image is present in the local image cache with the given OS and Architecture, and otherwise attempts to pull the image. If the option is not set, the host's native OS and Architecture are used. If the given image does not exist in the local image cache, the daemon attempts to pull the image with the host's native OS and Architecture. If the given image does exists in the local image cache, but its OS or architecture does not match, a warning is produced.When used with the `fromSrc` option to import an image from an archive, this option sets the platform information for the imported image. If the option is not set, the host's native OS and Architecture are used for the imported image. |

##### header Parameters

|                 |                                                                                                                          |
| --------------- | ------------------------------------------------------------------------------------------------------------------------ |
| X-Registry-Auth | stringA base64url-encoded auth configuration.Refer to the [authentication section](#section/Authentication) for details. |

##### Request Body schema:text/plain

Image content if the value `-` has been specified in fromSrc query parameter

string

### Responses

/v1.47/images/create

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Image/operation/ImageInspect)Inspect an image

Return low-level information about an image.

##### path Parameters

|              |                        |
| ------------ | ---------------------- |
| namerequired | stringImage name or id |

### Responses

/v1.47/images/{name}/json

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Id": "sha256:ec3f0931a6e6b6855d76b2d7b0be30e81860baccd891b2e243280bf1cd8ad710",
"RepoTags": [
"example:1.0",
"example:latest",
"example:stable",
"internal.registry.example.com:5000/example:1.0"
],
"RepoDigests": [
"example@sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb",
"internal.registry.example.com:5000/example@sha256:b69959407d21e8a062e0416bf13405bb2b71ed7a84dde4158ebafacfa06f5578"
],
"Parent": "",
"Comment": "",
"Created": "2022-02-04T21:20:12.497794809Z",
"DockerVersion": "27.0.1",
"Author": "",
"Config": {
"Hostname": "",
"Domainname": "",
"User": "web:web",
"AttachStdin": false,
"AttachStdout": false,
"AttachStderr": false,
"ExposedPorts": {
"80/tcp": { },
"443/tcp": { }
},
"Tty": false,
"OpenStdin": false,
"StdinOnce": false,
"Env": [
"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
],
"Cmd": [
"/bin/sh"
],
"Healthcheck": {
"Test": [
"string"
],
"Interval": 0,
"Timeout": 0,
"Retries": 0,
"StartPeriod": 0,
"StartInterval": 0
},
"ArgsEscaped": true,
"Image": "",
"Volumes": {
"/app/data": { },
"/app/config": { }
},
"WorkingDir": "/public/",
"Entrypoint": [ ],
"OnBuild": [ ],
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"StopSignal": "SIGTERM",
"Shell": [
"/bin/sh",
"-c"
]
},
"Architecture": "arm",
"Variant": "v7",
"Os": "linux",
"OsVersion": "",
"Size": 1239828,
"GraphDriver": {
"Name": "overlay2",
"Data": {
"MergedDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/merged",
"UpperDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/diff",
"WorkDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/work"
}
},
"RootFS": {
"Type": "layers",
"Layers": [
"sha256:1834950e52ce4d5a88a1bbd131c537f4d0e56d10ff0dd69e66be3b7dfa9df7e6",
"sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef"
]
},
"Metadata": {
"LastTagTime": "2022-02-28T14:40:02.623929178Z"
}
}`

## [](#tag/Image/operation/ImageHistory)Get the history of an image

Return parent layers of an image.

##### path Parameters

|              |                        |
| ------------ | ---------------------- |
| namerequired | stringImage name or ID |

### Responses

/v1.47/images/{name}/history

### Response samples

* 200
* 404
* 500

Content type

application/json

`[
{
"Id": "3db9c44f45209632d6050b35958829c3a2aa256d81b9a7be45b362ff85c54710",
"Created": 1398108230,
"CreatedBy": "/bin/sh -c #(nop) ADD file:eb15dbd63394e063b805a3c32ca7bf0266ef64676d5a6fab4801f2e81e2a5148 in /",
"Tags": [
"ubuntu:lucid",
"ubuntu:10.04"
],
"Size": 182964289,
"Comment": ""
},
{
"Id": "6cfa4d1f33fb861d4d114f43b25abd0ac737509268065cdfd69d544a59c85ab8",
"Created": 1398108222,
"CreatedBy": "/bin/sh -c #(nop) MAINTAINER Tianon Gravi <admwiggin@gmail.com> - mkimage-debootstrap.sh -i iproute,iputils-ping,ubuntu-minimal -t lucid.tar.xz lucid http://archive.ubuntu.com/ubuntu/",
"Tags": [ ],
"Size": 0,
"Comment": ""
},
{
"Id": "511136ea3c5a64f264b78b5433614aec563103b4d4702f3ba7d4d2698e22c158",
"Created": 1371157430,
"CreatedBy": "",
"Tags": [
"scratch12:latest",
"scratch:latest"
],
"Size": 0,
"Comment": "Imported from -"
}
]`

## [](#tag/Image/operation/ImagePush)Push an image

Push an image to a registry.

If you wish to push an image on to a private registry, that image must already have a tag which references the registry. For example, `registry.example.com/myimage:latest`.

The push is cancelled if the HTTP connection is closed.

##### path Parameters

|              |                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| namerequired | stringName of the image to push. For example, `registry.example.com/myimage`. The image must be present in the local image store with the same name.The name should be provided without tag; if a tag is provided, it is ignored. For example, `registry.example.com/myimage:latest` is considered equivalent to `registry.example.com/myimage`.Use the `tag` parameter to specify the tag to push. |

##### query Parameters

|          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tag      | stringTag of the image to push. For example, `latest`. If no tag is provided, all tags of the given image that are present in the local image store are pushed.                                                                                                                                                                                                                                                                                                                   |
| platform | stringJSON-encoded OCI platform to select the platform-variant to push. If not provided, all available variants will attempt to be pushed.If the daemon provides a multi-platform image store, this selects the platform-variant to push to the registry. If the image is a single-platform image, or if the multi-platform image does not provide a variant matching the given platform, an error is returned.Example: `{"os": "linux", "architecture": "arm", "variant": "v5"}` |

##### header Parameters

|                         |                                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| X-Registry-Authrequired | stringA base64url-encoded auth configuration.Refer to the [authentication section](#section/Authentication) for details. |

### Responses

/v1.47/images/{name}/push

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Image/operation/ImageTag)Tag an image

Create a tag that refers to a source image.

This creates an additional reference (tag) to the source image. The tag can include a different repository name and/or tag. If the repository or tag already exists, it will be overwritten.

##### path Parameters

|              |                                |
| ------------ | ------------------------------ |
| namerequired | stringImage name or ID to tag. |

##### query Parameters

|      |                                                                    |
| ---- | ------------------------------------------------------------------ |
| repo | stringThe repository to tag in. For example, `someuser/someimage`. |
| tag  | stringThe name of the new tag.                                     |

### Responses

/v1.47/images/{name}/tag

### Response samples

* 400
* 404
* 409
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Image/operation/ImageDelete)Remove an image

Remove an image, along with any untagged parent images that were referenced by that image.

Images can't be removed if they have descendant images, are being used by a running container or are being used by a build.

##### path Parameters

|              |                        |
| ------------ | ---------------------- |
| namerequired | stringImage name or ID |

##### query Parameters

|         |                                                                                                        |
| ------- | ------------------------------------------------------------------------------------------------------ |
| force   | booleanDefault: falseRemove the image even if it is being used by stopped containers or has other tags |
| noprune | booleanDefault: falseDo not delete untagged parent images                                              |

### Responses

/v1.47/images/{name}

### Response samples

* 200
* 404
* 409
* 500

Content type

application/json

`[
{
"Untagged": "3e2f21a89f"
},
{
"Deleted": "3e2f21a89f"
},
{
"Deleted": "53b4f83ac9"
}
]`

## [](#tag/Image/operation/ImageSearch)Search images

Search for an image on Docker Hub.

##### query Parameters

|              |                                                                                                                                                                                                                        |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| termrequired | stringTerm to search                                                                                                                                                                                                   |
| limit        | integerMaximum number of results to return                                                                                                                                                                             |
| filters      | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the images list. Available filters:- `is-official=(true\|false)`
- `stars=<number>` Matches images that has at least 'number' stars. |

### Responses

/v1.47/images/search

### Response samples

* 200
* 500

Content type

application/json

`[
{
"description": "A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size!",
"is_official": true,
"is_automated": false,
"name": "alpine",
"star_count": 10093
},
{
"description": "Busybox base image.",
"is_official": true,
"is_automated": false,
"name": "Busybox base image.",
"star_count": 3037
},
{
"description": "The PostgreSQL object-relational database system provides reliability and data integrity.",
"is_official": true,
"is_automated": false,
"name": "postgres",
"star_count": 12408
}
]`

## [](#tag/Image/operation/ImagePrune)Delete unused images

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringFilters to process on the prune list, encoded as JSON (a `map[string][]string`). Available filters:- `dangling=<boolean>` When set to `true` (or `1`), prune only unused *and* untagged images. When set to `false` (or `0`), all unused images are pruned.
- `until=<string>` Prune images created before this timestamp. The `<timestamp>` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. `10m`, `1h30m`) computed relative to the daemon machine’s time.
- `label` (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) Prune images with (or without, in case `label!=...` is used) the specified labels. |

### Responses

/v1.47/images/prune

### Response samples

* 200
* 500

Content type

application/json

`{
"ImagesDeleted": [
{
"Untagged": "string",
"Deleted": "string"
}
],
"SpaceReclaimed": 0
}`

## [](#tag/Image/operation/ImageCommit)Create a new image from a container

##### query Parameters

|           |                                                                               |
| --------- | ----------------------------------------------------------------------------- |
| container | stringThe ID or name of the container to commit                               |
| repo      | stringRepository name for the created image                                   |
| tag       | stringTag name for the create image                                           |
| comment   | stringCommit message                                                          |
| author    | stringAuthor of the image (e.g., `John Hannibal Smith <hannibal@a-team.com>`) |
| pause     | booleanDefault: trueWhether to pause the container before committing          |
| changes   | string`Dockerfile` instructions to apply while committing                     |

##### Request Body schema: application/json

The container configuration

|                 |                                                                                                                                                                                                                                                                                                       |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hostname        | stringThe hostname to use for the container, as a valid RFC 1123 hostname.                                                                                                                                                                                                                            |
| Domainname      | stringThe domain name to use for the container.                                                                                                                                                                                                                                                       |
| User            | stringThe user that commands are run as inside the container.                                                                                                                                                                                                                                         |
| AttachStdin     | booleanDefault: falseWhether to attach to `stdin`.                                                                                                                                                                                                                                                    |
| AttachStdout    | booleanDefault: trueWhether to attach to `stdout`.                                                                                                                                                                                                                                                    |
| AttachStderr    | booleanDefault: trueWhether to attach to `stderr`.                                                                                                                                                                                                                                                    |
|                 | object or nullAn object mapping ports to an empty object in the form:`{"<port>/<tcp\|udp\|sctp>": {}}`                                                                                                                                                                                                |
| Tty             | booleanDefault: falseAttach standard streams to a TTY, including `stdin` if it is not closed.                                                                                                                                                                                                         |
| OpenStdin       | booleanDefault: falseOpen `stdin`                                                                                                                                                                                                                                                                     |
| StdinOnce       | booleanDefault: falseClose `stdin` after one attached client disconnects                                                                                                                                                                                                                              |
| Env             | Array of stringsA list of environment variables to set inside the container in the form `["VAR=value", ...]`. A variable without `=` is removed from the environment, rather than to have an empty value.                                                                                             |
| Cmd             | Array of stringsCommand to run specified as a string or an array of strings.                                                                                                                                                                                                                          |
|                 | object (HealthConfig)A test to perform to check that the container is healthy. Healthcheck commands should be side-effect free.                                                                                                                                                                       |
| ArgsEscaped     | boolean or nullDefault: falseCommand is already escaped (Windows only)                                                                                                                                                                                                                                |
| Image           | stringThe name (or reference) of the image to use when creating the container, or which was used when the container was created.                                                                                                                                                                      |
|                 | objectAn object mapping mount point paths inside the container to empty objects.                                                                                                                                                                                                                      |
| WorkingDir      | stringThe working directory for commands to run in.                                                                                                                                                                                                                                                   |
| Entrypoint      | Array of stringsThe entry point for the container as a string or an array of strings.If the array consists of exactly one empty string (`[""]`) then the entry point is reset to system default (i.e., the entry point used by docker when there is no `ENTRYPOINT` instruction in the `Dockerfile`). |
| NetworkDisabled | boolean or nullDisable networking for the container.                                                                                                                                                                                                                                                  |
| MacAddress      | string or nullMAC address of the container.Deprecated: this field is deprecated in API v1.44 and up. Use EndpointSettings.MacAddress instead.                                                                                                                                                         |
| OnBuild         | Array of strings or null`ONBUILD` metadata that were defined in the image's `Dockerfile`.                                                                                                                                                                                                             |
|                 | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                |
| StopSignal      | string or nullSignal to stop a container as a string or unsigned integer.                                                                                                                                                                                                                             |
| StopTimeout     | integer or nullDefault: 10Timeout to stop a container in seconds.                                                                                                                                                                                                                                     |
| Shell           | Array of strings or nullShell for when `RUN`, `CMD`, and `ENTRYPOINT` uses a shell.                                                                                                                                                                                                                   |

### Responses

/v1.47/commit

### Request samples

* Payload

Content type

application/json

`{
"Hostname": "439f4e91bd1d",
"Domainname": "string",
"User": "string",
"AttachStdin": false,
"AttachStdout": true,
"AttachStderr": true,
"ExposedPorts": {
"80/tcp": { },
"443/tcp": { }
},
"Tty": false,
"OpenStdin": false,
"StdinOnce": false,
"Env": [
"PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
],
"Cmd": [
"/bin/sh"
],
"Healthcheck": {
"Test": [
"string"
],
"Interval": 0,
"Timeout": 0,
"Retries": 0,
"StartPeriod": 0,
"StartInterval": 0
},
"ArgsEscaped": false,
"Image": "example-image:1.0",
"Volumes": {
"property1": { },
"property2": { }
},
"WorkingDir": "/public/",
"Entrypoint": [ ],
"NetworkDisabled": true,
"MacAddress": "string",
"OnBuild": [ ],
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"StopSignal": "SIGTERM",
"StopTimeout": 10,
"Shell": [
"/bin/sh",
"-c"
]
}`

### Response samples

* 201
* 404
* 500

Content type

application/json

`{
"Id": "string"
}`

## [](#tag/Image/operation/ImageGet)Export an image

Get a tarball containing all images and metadata for a repository.

If `name` is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned. If `name` is an image ID, similarly only that image (and its parents) are returned, but with the exclusion of the `repositories` file in the tarball, as there were no image names referenced.

### Image tarball format

An image tarball contains [Content as defined in the OCI Image Layout Specification](https://github.com/opencontainers/image-spec/blob/v1.1.1/image-layout.md#content).

Additionally, includes the manifest.json file associated with a backwards compatible docker save format.

If the tarball defines a repository, the tarball should also include a `repositories` file at the root that contains a list of repository and tag names mapped to layer IDs.

```json
{
  "hello-world": {
    "latest": "565a9d68a73f6706862bfe8409a7f659776d4d60a8d096eb4a3cbce6999cc2a1"
  }
}
```

##### path Parameters

|              |                        |
| ------------ | ---------------------- |
| namerequired | stringImage name or ID |

### Responses

/v1.47/images/{name}/get

## [](#tag/Image/operation/ImageGetAll)Export several images

Get a tarball containing all images and metadata for several image repositories.

For each value of the `names` parameter: if it is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|       |                                          |
| ----- | ---------------------------------------- |
| names | Array of stringsImage names to filter by |

### Responses

/v1.47/images/get

## [](#tag/Image/operation/ImageLoad)Import images

Load a set of images and tags into a repository.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|       |                                                             |
| ----- | ----------------------------------------------------------- |
| quiet | booleanDefault: falseSuppress progress details during load. |

##### Request Body schema: application/x-tar

Tar archive containing images

string \<binary>

### Responses

/v1.47/images/load

### Response samples

* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Network)Networks

Networks are user-defined networks that containers can be attached to. See the [networking documentation](https://docs.docker.com/network/) for more information.

## [](#tag/Network/operation/NetworkList)List networks

Returns a list of networks. For details on the format, see the [network inspect endpoint](#operation/NetworkInspect).

Note that it uses a different, smaller representation of a network than inspecting a single network. For example, the list of containers attached to the network is not propagated in API versions 1.28 and up.

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringJSON encoded value of the filters (a `map[string][]string`) to process on the networks list.Available filters:- `dangling=<boolean>` When set to `true` (or `1`), returns all networks that are not in use by a container. When set to `false` (or `0`), only networks that are in use by one or more containers are returned.
- `driver=<driver-name>` Matches a network's driver.
- `id=<network-id>` Matches all or part of a network ID.
- `label=<key>` or `label=<key>=<value>` of a network label.
- `name=<network-name>` Matches all or part of a network name.
- `scope=["swarm"\|"global"\|"local"]` Filters networks by scope (`swarm`, `global`, or `local`).
- `type=["custom"\|"builtin"]` Filters networks by type. The `custom` keyword returns all user-defined networks. |

### Responses

/v1.47/networks

### Response samples

* 200
* 500

Content type

application/json

`[
{
"Name": "bridge",
"Id": "f2de39df4171b0dc801e8002d1d999b77256983dfc63041c0f34030aa3977566",
"Created": "2016-10-19T06:21:00.416543526Z",
"Scope": "local",
"Driver": "bridge",
"EnableIPv4": true,
"EnableIPv6": false,
"Internal": false,
"Attachable": false,
"Ingress": false,
"IPAM": {
"Driver": "default",
"Config": [
{
"Subnet": "172.17.0.0/16"
}
]
},
"Options": {
"com.docker.network.bridge.default_bridge": "true",
"com.docker.network.bridge.enable_icc": "true",
"com.docker.network.bridge.enable_ip_masquerade": "true",
"com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
"com.docker.network.bridge.name": "docker0",
"com.docker.network.driver.mtu": "1500"
}
},
{
"Name": "none",
"Id": "e086a3893b05ab69242d3c44e49483a3bbbd3a26b46baa8f61ab797c1088d794",
"Created": "0001-01-01T00:00:00Z",
"Scope": "local",
"Driver": "null",
"EnableIPv4": false,
"EnableIPv6": false,
"Internal": false,
"Attachable": false,
"Ingress": false,
"IPAM": {
"Driver": "default",
"Config": [ ]
},
"Containers": { },
"Options": { }
},
{
"Name": "host",
"Id": "13e871235c677f196c4e1ecebb9dc733b9b2d2ab589e30c539efeda84a24215e",
"Created": "0001-01-01T00:00:00Z",
"Scope": "local",
"Driver": "host",
"EnableIPv4": false,
"EnableIPv6": false,
"Internal": false,
"Attachable": false,
"Ingress": false,
"IPAM": {
"Driver": "default",
"Config": [ ]
},
"Containers": { },
"Options": { }
}
]`

## [](#tag/Network/operation/NetworkInspect)Inspect a network

##### path Parameters

|            |                          |
| ---------- | ------------------------ |
| idrequired | stringNetwork ID or name |

##### query Parameters

|         |                                                                  |
| ------- | ---------------------------------------------------------------- |
| verbose | booleanDefault: falseDetailed inspect output for troubleshooting |
| scope   | stringFilter the network by scope (swarm, global, or local)      |

### Responses

/v1.47/networks/{id}

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Name": "my_network",
"Id": "7d86d31b1478e7cca9ebed7e73aa0fdeec46c5ca29497431d3007d2d9e15ed99",
"Created": "2016-10-19T04:33:30.360899459Z",
"Scope": "local",
"Driver": "overlay",
"EnableIPv4": true,
"EnableIPv6": false,
"IPAM": {
"Driver": "default",
"Config": [
{
"Subnet": "172.20.0.0/16",
"IPRange": "172.20.10.0/24",
"Gateway": "172.20.10.11",
"AuxiliaryAddresses": {
"property1": "string",
"property2": "string"
}
}
],
"Options": {
"foo": "bar"
}
},
"Internal": false,
"Attachable": false,
"Ingress": false,
"ConfigFrom": {
"Network": "config_only_network_01"
},
"ConfigOnly": false,
"Containers": {
"19a4d5d687db25203351ed79d478946f861258f018fe384f229f2efa4b23513c": {
"Name": "test",
"EndpointID": "628cadb8bcb92de107b2a1e516cbffe463e321f548feb37697cce00ad694f21a",
"MacAddress": "02:42:ac:13:00:02",
"IPv4Address": "172.19.0.2/16",
"IPv6Address": ""
}
},
"Options": {
"com.docker.network.bridge.default_bridge": "true",
"com.docker.network.bridge.enable_icc": "true",
"com.docker.network.bridge.enable_ip_masquerade": "true",
"com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
"com.docker.network.bridge.name": "docker0",
"com.docker.network.driver.mtu": "1500"
},
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Peers": [
{
"Name": "6869d7c1732b",
"IP": "10.133.77.91"
}
]
}`

## [](#tag/Network/operation/NetworkDelete)Remove a network

##### path Parameters

|            |                          |
| ---------- | ------------------------ |
| idrequired | stringNetwork ID or name |

### Responses

/v1.47/networks/{id}

### Response samples

* 403
* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Network/operation/NetworkCreate)Create a network

##### Request Body schema: application/jsonrequired

Network configuration

|              |                                                                                                                                                                                                                                        |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Namerequired | stringThe network's name.                                                                                                                                                                                                              |
| Driver       | stringDefault: "bridge"Name of the network driver plugin to use.                                                                                                                                                                       |
| Scope        | stringThe level at which the network exists (e.g. `swarm` for cluster-wide or `local` for machine level).                                                                                                                              |
| Internal     | booleanRestrict external access to the network.                                                                                                                                                                                        |
| Attachable   | booleanGlobally scoped network is manually attachable by regular containers from workers in swarm mode.                                                                                                                                |
| Ingress      | booleanIngress network is the network which provides the routing-mesh in swarm mode.                                                                                                                                                   |
| ConfigOnly   | booleanDefault: falseCreates a config-only network. Config-only networks are placeholder networks for network configurations to be used by other networks. Config-only networks cannot be used directly to run containers or services. |
|              | object (ConfigReference)The config-only network source to provide the configuration for this network.                                                                                                                                  |
|              | object (IPAM)                                                                                                                                                                                                                          |
| EnableIPv4   | booleanEnable IPv4 on the network. To disable IPv4, the daemon must be started with experimental features enabled.                                                                                                                     |
| EnableIPv6   | booleanEnable IPv6 on the network.                                                                                                                                                                                                     |
|              | objectNetwork specific options to be used by the drivers.                                                                                                                                                                              |
|              | objectUser-defined key/value metadata.                                                                                                                                                                                                 |

### Responses

/v1.47/networks/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "my_network",
"Driver": "bridge",
"Scope": "string",
"Internal": true,
"Attachable": true,
"Ingress": false,
"ConfigOnly": false,
"ConfigFrom": {
"Network": "config_only_network_01"
},
"IPAM": {
"Driver": "default",
"Config": [
{
"Subnet": "172.20.0.0/16",
"IPRange": "172.20.10.0/24",
"Gateway": "172.20.10.11",
"AuxiliaryAddresses": {
"property1": "string",
"property2": "string"
}
}
],
"Options": {
"foo": "bar"
}
},
"EnableIPv4": true,
"EnableIPv6": true,
"Options": {
"com.docker.network.bridge.default_bridge": "true",
"com.docker.network.bridge.enable_icc": "true",
"com.docker.network.bridge.enable_ip_masquerade": "true",
"com.docker.network.bridge.host_binding_ipv4": "0.0.0.0",
"com.docker.network.bridge.name": "docker0",
"com.docker.network.driver.mtu": "1500"
},
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
}
}`

### Response samples

* 201
* 400
* 403
* 404
* 500

Content type

application/json

`{
"Id": "b5c4fc71e8022147cd25de22b22173de4e3b170134117172eb595cb91b4e7e5d",
"Warning": ""
}`

## [](#tag/Network/operation/NetworkConnect)Connect a container to a network

The network must be either a local-scoped network or a swarm-scoped network with the `attachable` option set. A network cannot be re-attached to a running container

##### path Parameters

|            |                          |
| ---------- | ------------------------ |
| idrequired | stringNetwork ID or name |

##### Request Body schema: application/jsonrequired

|           |                                                                  |
| --------- | ---------------------------------------------------------------- |
| Container | stringThe ID or name of the container to connect to the network. |
|           | object (EndpointSettings)Configuration for a network endpoint.   |

### Responses

/v1.47/networks/{id}/connect

### Request samples

* Payload

Content type

application/json

`{
"Container": "3613f73ba0e4",
"EndpointConfig": {
"IPAMConfig": {
"IPv4Address": "172.24.56.89",
"IPv6Address": "2001:db8::5689"
},
"MacAddress": "02:42:ac:12:05:02"
}
}`

### Response samples

* 400
* 403
* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Network/operation/NetworkDisconnect)Disconnect a container from a network

##### path Parameters

|            |                          |
| ---------- | ------------------------ |
| idrequired | stringNetwork ID or name |

##### Request Body schema: application/jsonrequired

|           |                                                                       |
| --------- | --------------------------------------------------------------------- |
| Container | stringThe ID or name of the container to disconnect from the network. |
| Force     | booleanForce the container to disconnect from the network.            |

### Responses

/v1.47/networks/{id}/disconnect

### Request samples

* Payload

Content type

application/json

`{
"Container": "string",
"Force": true
}`

### Response samples

* 403
* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Network/operation/NetworkPrune)Delete unused networks

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| filters | stringFilters to process on the prune list, encoded as JSON (a `map[string][]string`).Available filters:- `until=<timestamp>` Prune networks created before this timestamp. The `<timestamp>` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. `10m`, `1h30m`) computed relative to the daemon machine’s time.
- `label` (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) Prune networks with (or without, in case `label!=...` is used) the specified labels. |

### Responses

/v1.47/networks/prune

### Response samples

* 200
* 500

Content type

application/json

`{
"NetworksDeleted": [
"string"
]
}`

## [](#tag/Volume)Volumes

Create and manage persistent storage that can be attached to containers.

## [](#tag/Volume/operation/VolumeList)List volumes

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | string \<json>JSON encoded value of the filters (a `map[string][]string`) to process on the volumes list. Available filters:- `dangling=<boolean>` When set to `true` (or `1`), returns all volumes that are not in use by a container. When set to `false` (or `0`), only volumes that are in use by one or more containers are returned.
- `driver=<volume-driver-name>` Matches volumes based on their driver.
- `label=<key>` or `label=<key>:<value>` Matches volumes based on the presence of a `label` alone or a `label` and a value.
- `name=<volume-name>` Matches all or part of a volume name. |

### Responses

/v1.47/volumes

### Response samples

* 200
* 500

Content type

application/json

`{
"Volumes": [
{
"Name": "tardis",
"Driver": "custom",
"Mountpoint": "/var/lib/docker/volumes/tardis",
"CreatedAt": "2016-06-07T20:31:11.853781916Z",
"Status": {
"hello": "world"
},
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Scope": "local",
"ClusterVolume": {
"ID": "string",
"Version": {
"Index": 373531
},
"CreatedAt": "string",
"UpdatedAt": "string",
"Spec": {
"Group": "string",
"AccessMode": {
"Scope": "single",
"Sharing": "none",
"MountVolume": { },
"Secrets": [
{
"Key": "string",
"Secret": "string"
}
],
"AccessibilityRequirements": {
"Requisite": [
{
"Segments": {
"property1": null,
"property2": null
}
}
],
"Preferred": [
{
"Segments": {
"property1": null,
"property2": null
}
}
]
},
"CapacityRange": {
"RequiredBytes": 0,
"LimitBytes": 0
},
"Availability": "active"
}
},
"Info": {
"CapacityBytes": 0,
"VolumeContext": {
"property1": "string",
"property2": "string"
},
"VolumeID": "string",
"AccessibleTopology": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"PublishStatus": [
{
"NodeID": "string",
"State": "pending-publish",
"PublishContext": {
"property1": "string",
"property2": "string"
}
}
]
},
"Options": {
"device": "tmpfs",
"o": "size=100m,uid=1000",
"type": "tmpfs"
},
"UsageData": {
"Size": -1,
"RefCount": -1
}
}
],
"Warnings": [ ]
}`

## [](#tag/Volume/operation/VolumeCreate)Create a volume

##### Request Body schema: application/jsonrequired

Volume configuration

|        |                                                                                                                        |
| ------ | ---------------------------------------------------------------------------------------------------------------------- |
| Name   | stringThe new volume's name. If not specified, Docker generates a name.                                                |
| Driver | stringDefault: "local"Name of the volume driver to use.                                                                |
|        | objectA mapping of driver options and values. These options are passed directly to the driver and are driver specific. |
|        | objectUser-defined key/value metadata.                                                                                 |
|        | object (ClusterVolumeSpec)Cluster-specific options used to create the volume.                                          |

### Responses

/v1.47/volumes/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "tardis",
"Driver": "custom",
"DriverOpts": {
"device": "tmpfs",
"o": "size=100m,uid=1000",
"type": "tmpfs"
},
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"ClusterVolumeSpec": {
"Group": "string",
"AccessMode": {
"Scope": "single",
"Sharing": "none",
"MountVolume": { },
"Secrets": [
{
"Key": "string",
"Secret": "string"
}
],
"AccessibilityRequirements": {
"Requisite": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
],
"Preferred": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"CapacityRange": {
"RequiredBytes": 0,
"LimitBytes": 0
},
"Availability": "active"
}
}
}`

### Response samples

* 201
* 500

Content type

application/json

`{
"Name": "tardis",
"Driver": "custom",
"Mountpoint": "/var/lib/docker/volumes/tardis",
"CreatedAt": "2016-06-07T20:31:11.853781916Z",
"Status": {
"hello": "world"
},
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Scope": "local",
"ClusterVolume": {
"ID": "string",
"Version": {
"Index": 373531
},
"CreatedAt": "string",
"UpdatedAt": "string",
"Spec": {
"Group": "string",
"AccessMode": {
"Scope": "single",
"Sharing": "none",
"MountVolume": { },
"Secrets": [
{
"Key": "string",
"Secret": "string"
}
],
"AccessibilityRequirements": {
"Requisite": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
],
"Preferred": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"CapacityRange": {
"RequiredBytes": 0,
"LimitBytes": 0
},
"Availability": "active"
}
},
"Info": {
"CapacityBytes": 0,
"VolumeContext": {
"property1": "string",
"property2": "string"
},
"VolumeID": "string",
"AccessibleTopology": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"PublishStatus": [
{
"NodeID": "string",
"State": "pending-publish",
"PublishContext": {
"property1": "string",
"property2": "string"
}
}
]
},
"Options": {
"device": "tmpfs",
"o": "size=100m,uid=1000",
"type": "tmpfs"
},
"UsageData": {
"Size": -1,
"RefCount": -1
}
}`

## [](#tag/Volume/operation/VolumeInspect)Inspect a volume

##### path Parameters

|              |                         |
| ------------ | ----------------------- |
| namerequired | stringVolume name or ID |

### Responses

/v1.47/volumes/{name}

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Name": "tardis",
"Driver": "custom",
"Mountpoint": "/var/lib/docker/volumes/tardis",
"CreatedAt": "2016-06-07T20:31:11.853781916Z",
"Status": {
"hello": "world"
},
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Scope": "local",
"ClusterVolume": {
"ID": "string",
"Version": {
"Index": 373531
},
"CreatedAt": "string",
"UpdatedAt": "string",
"Spec": {
"Group": "string",
"AccessMode": {
"Scope": "single",
"Sharing": "none",
"MountVolume": { },
"Secrets": [
{
"Key": "string",
"Secret": "string"
}
],
"AccessibilityRequirements": {
"Requisite": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
],
"Preferred": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"CapacityRange": {
"RequiredBytes": 0,
"LimitBytes": 0
},
"Availability": "active"
}
},
"Info": {
"CapacityBytes": 0,
"VolumeContext": {
"property1": "string",
"property2": "string"
},
"VolumeID": "string",
"AccessibleTopology": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"PublishStatus": [
{
"NodeID": "string",
"State": "pending-publish",
"PublishContext": {
"property1": "string",
"property2": "string"
}
}
]
},
"Options": {
"device": "tmpfs",
"o": "size=100m,uid=1000",
"type": "tmpfs"
},
"UsageData": {
"Size": -1,
"RefCount": -1
}
}`

## [](#tag/Volume/operation/VolumeUpdate)"Update a volume. Valid only for Swarm cluster volumes"

##### path Parameters

|              |                                    |
| ------------ | ---------------------------------- |
| namerequired | stringThe name or ID of the volume |

##### query Parameters

|                 |                                                                                                                                                            |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| versionrequired | integer \<int64>The version number of the volume being updated. This is required to avoid conflicting writes. Found in the volume's `ClusterVolume` field. |

##### Request Body schema: application/json

The spec of the volume to update. Currently, only Availability may change. All other fields must remain unchanged.

|   |                                                                               |
| - | ----------------------------------------------------------------------------- |
|   | object (ClusterVolumeSpec)Cluster-specific options used to create the volume. |

### Responses

/v1.47/volumes/{name}

### Request samples

* Payload

Content type

application/json

`{
"Spec": {
"Group": "string",
"AccessMode": {
"Scope": "single",
"Sharing": "none",
"MountVolume": { },
"Secrets": [
{
"Key": "string",
"Secret": "string"
}
],
"AccessibilityRequirements": {
"Requisite": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
],
"Preferred": [
{
"Segments": {
"property1": "string",
"property2": "string"
}
}
]
},
"CapacityRange": {
"RequiredBytes": 0,
"LimitBytes": 0
},
"Availability": "active"
}
}
}`

### Response samples

* 400
* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Volume/operation/VolumeDelete)Remove a volume

Instruct the driver to remove the volume.

##### path Parameters

|              |                         |
| ------------ | ----------------------- |
| namerequired | stringVolume name or ID |

##### query Parameters

|       |                                                      |
| ----- | ---------------------------------------------------- |
| force | booleanDefault: falseForce the removal of the volume |

### Responses

/v1.47/volumes/{name}

### Response samples

* 404
* 409
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Volume/operation/VolumePrune)Delete unused volumes

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                         |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringFilters to process on the prune list, encoded as JSON (a `map[string][]string`).Available filters:- `label` (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) Prune volumes with (or without, in case `label!=...` is used) the specified labels.
- `all` (`all=true`) - Consider all (local) volumes for pruning and not just anonymous volumes. |

### Responses

/v1.47/volumes/prune

### Response samples

* 200
* 500

Content type

application/json

`{
"VolumesDeleted": [
"string"
],
"SpaceReclaimed": 0
}`

## [](#tag/Exec)Exec

Run new commands inside running containers. Refer to the [command-line reference](https://docs.docker.com/engine/reference/commandline/exec/) for more information.

To exec a command in a container, you first need to create an exec instance, then start it. These two API endpoints are wrapped up in a single command-line command, `docker exec`.

## [](#tag/Exec/operation/ContainerExec)Create an exec instance

Run a command inside a running container.

##### path Parameters

|            |                               |
| ---------- | ----------------------------- |
| idrequired | stringID or name of container |

##### Request Body schema: application/jsonrequired

Exec configuration

|              |                                                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| AttachStdin  | booleanAttach to `stdin` of the exec command.                                                                                                                                  |
| AttachStdout | booleanAttach to `stdout` of the exec command.                                                                                                                                 |
| AttachStderr | booleanAttach to `stderr` of the exec command.                                                                                                                                 |
| ConsoleSize  | Array of integers or null = 2 items \[ items >= 0 ]Initial console size, as an `[height, width]` array.                                                                        |
| DetachKeys   | stringOverride the key sequence for detaching a container. Format is a single character `[a-Z]` or `ctrl-<value>` where `<value>` is one of: `a-z`, `@`, `^`, `[`, `,` or `_`. |
| Tty          | booleanAllocate a pseudo-TTY.                                                                                                                                                  |
| Env          | Array of stringsA list of environment variables in the form `["VAR=value", ...]`.                                                                                              |
| Cmd          | Array of stringsCommand to run, as a string or array of strings.                                                                                                               |
| Privileged   | booleanDefault: falseRuns the exec process with extended privileges.                                                                                                           |
| User         | stringThe user, and optionally, group to run the exec process inside the container. Format is one of: `user`, `user:group`, `uid`, or `uid:gid`.                               |
| WorkingDir   | stringThe working directory for the exec process inside the container.                                                                                                         |

### Responses

/v1.47/containers/{id}/exec

### Request samples

* Payload

Content type

application/json

`{
"AttachStdin": false,
"AttachStdout": true,
"AttachStderr": true,
"DetachKeys": "ctrl-p,ctrl-q",
"Tty": false,
"Cmd": [
"date"
],
"Env": [
"FOO=bar",
"BAZ=quux"
]
}`

### Response samples

* 201
* 404
* 409
* 500

Content type

application/json

`{
"Id": "string"
}`

## [](#tag/Exec/operation/ExecStart)Start an exec instance

Starts a previously set up exec instance. If detach is true, this endpoint returns immediately after starting the command. Otherwise, it sets up an interactive session with the command.

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringExec instance ID |

##### Request Body schema: application/json

|             |                                                                                                         |
| ----------- | ------------------------------------------------------------------------------------------------------- |
| Detach      | booleanDetach from the command.                                                                         |
| Tty         | booleanAllocate a pseudo-TTY.                                                                           |
| ConsoleSize | Array of integers or null = 2 items \[ items >= 0 ]Initial console size, as an `[height, width]` array. |

### Responses

/v1.47/exec/{id}/start

### Request samples

* Payload

Content type

application/json

`{
"Detach": false,
"Tty": true,
"ConsoleSize": [
80,
64
]
}`

## [](#tag/Exec/operation/ExecResize)Resize an exec instance

Resize the TTY session used by an exec instance. This endpoint only works if `tty` was specified as part of creating and starting the exec instance.

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringExec instance ID |

##### query Parameters

|           |                                                |
| --------- | ---------------------------------------------- |
| hrequired | integerHeight of the TTY session in characters |
| wrequired | integerWidth of the TTY session in characters  |

### Responses

/v1.47/exec/{id}/resize

### Response samples

* 400
* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Exec/operation/ExecInspect)Inspect an exec instance

Return low-level information about an exec instance.

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringExec instance ID |

### Responses

/v1.47/exec/{id}/json

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"CanRemove": false,
"ContainerID": "b53ee82b53a40c7dca428523e34f741f3abc51d9f297a14ff874bf761b995126",
"DetachKeys": "",
"ExitCode": 2,
"ID": "f33bbfb39f5b142420f4759b2348913bd4a8d1a6d7fd56499cb41a1bb91d7b3b",
"OpenStderr": true,
"OpenStdin": true,
"OpenStdout": true,
"ProcessConfig": {
"arguments": [
"-c",
"exit 2"
],
"entrypoint": "sh",
"privileged": false,
"tty": true,
"user": "1000"
},
"Running": false,
"Pid": 42000
}`

## [](#tag/Swarm)Swarm

Engines can be clustered together in a swarm. Refer to the [swarm mode documentation](https://docs.docker.com/engine/swarm/) for more information.

## [](#tag/Swarm/operation/SwarmInspect)Inspect swarm

### Responses

/v1.47/swarm

### Response samples

* 200
* 404
* 500
* 503

Content type

application/json

`{
"ID": "abajmipo7b4xz5ip2nrla6b11",
"Version": {
"Index": 373531
},
"CreatedAt": "2016-08-18T10:44:24.496525531Z",
"UpdatedAt": "2017-08-09T07:09:37.632105588Z",
"Spec": {
"Name": "default",
"Labels": {
"com.example.corp.type": "production",
"com.example.corp.department": "engineering"
},
"Orchestration": {
"TaskHistoryRetentionLimit": 10
},
"Raft": {
"SnapshotInterval": 10000,
"KeepOldSnapshots": 0,
"LogEntriesForSlowFollowers": 500,
"ElectionTick": 3,
"HeartbeatTick": 1
},
"Dispatcher": {
"HeartbeatPeriod": 5000000000
},
"CAConfig": {
"NodeCertExpiry": 7776000000000000,
"ExternalCAs": [
{
"Protocol": "cfssl",
"URL": "string",
"Options": {
"property1": "string",
"property2": "string"
},
"CACert": "string"
}
],
"SigningCACert": "string",
"SigningCAKey": "string",
"ForceRotate": 0
},
"EncryptionConfig": {
"AutoLockManagers": false
},
"TaskDefaults": {
"LogDriver": {
"Name": "json-file",
"Options": {
"max-file": "10",
"max-size": "100m"
}
}
}
},
"TLSInfo": {
"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n",
"CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
"CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="
},
"RootRotationInProgress": false,
"DataPathPort": 4789,
"DefaultAddrPool": [ [
"10.10.0.0/16",
"20.20.0.0/16"
]
],
"SubnetSize": 24,
"JoinTokens": {
"Worker": "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-1awxwuwd3z9j1z3puu7rcgdbx",
"Manager": "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2"
}
}`

## [](#tag/Swarm/operation/SwarmInit)Initialize a new swarm

##### Request Body schema:application/jsonrequired

|                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ListenAddr      | stringListen address used for inter-manager communication, as well as determining the networking interface used for the VXLAN Tunnel Endpoint (VTEP). This can either be an address/port combination in the form `192.168.1.1:4567`, or an interface followed by a port number, like `eth0:4567`. If the port number is omitted, the default swarm listening port is used.                                                                                                                                             |
| AdvertiseAddr   | stringExternally reachable address advertised to other nodes. This can either be an address/port combination in the form `192.168.1.1:4567`, or an interface followed by a port number, like `eth0:4567`. If the port number is omitted, the port number from the listen address is used. If `AdvertiseAddr` is not specified, it will be automatically detected when possible.                                                                                                                                        |
| DataPathAddr    | stringAddress or interface to use for data path traffic (format: `<ip\|interface>`), for example, `192.168.1.1`, or an interface, like `eth0`. If `DataPathAddr` is unspecified, the same address as `AdvertiseAddr` is used.The `DataPathAddr` specifies the address that global scope network drivers will publish towards other nodes in order to reach the containers running on this node. Using this parameter it is possible to separate the container data traffic from the management traffic of the cluster. |
| DataPathPort    | integer \<uint32>DataPathPort specifies the data path port number for data traffic. Acceptable port range is 1024 to 49151. if no port is set or is set to 0, default port 4789 will be used.                                                                                                                                                                                                                                                                                                                          |
| DefaultAddrPool | Array of stringsDefault Address Pool specifies default subnet pools for global scope networks.                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ForceNewCluster | booleanForce creation of a new swarm.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| SubnetSize      | integer \<uint32>SubnetSize specifies the subnet size of the networks created from the default subnet pool.                                                                                                                                                                                                                                                                                                                                                                                                            |
|                 | object (SwarmSpec)User modifiable swarm configuration.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |

### Responses

/v1.47/swarm/init

### Request samples

* Payload

Content type

application/json

`{
"ListenAddr": "0.0.0.0:2377",
"AdvertiseAddr": "192.168.1.1:2377",
"DataPathPort": 4789,
"DefaultAddrPool": [
"10.10.0.0/8",
"20.20.0.0/8"
],
"SubnetSize": 24,
"ForceNewCluster": false,
"Spec": {
"Orchestration": { },
"Raft": { },
"Dispatcher": { },
"CAConfig": { },
"EncryptionConfig": {
"AutoLockManagers": false
}
}
}`

### Response samples

* 200
* 400
* 500
* 503

Content type

application/json

`"7v2t30z9blmxuhnyo6s4cpenp"`

## [](#tag/Swarm/operation/SwarmJoin)Join an existing swarm

##### Request Body schema:application/jsonrequired

|               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ListenAddr    | stringListen address used for inter-manager communication if the node gets promoted to manager, as well as determining the networking interface used for the VXLAN Tunnel Endpoint (VTEP).                                                                                                                                                                                                                                                                                                                             |
| AdvertiseAddr | stringExternally reachable address advertised to other nodes. This can either be an address/port combination in the form `192.168.1.1:4567`, or an interface followed by a port number, like `eth0:4567`. If the port number is omitted, the port number from the listen address is used. If `AdvertiseAddr` is not specified, it will be automatically detected when possible.                                                                                                                                        |
| DataPathAddr  | stringAddress or interface to use for data path traffic (format: `<ip\|interface>`), for example, `192.168.1.1`, or an interface, like `eth0`. If `DataPathAddr` is unspecified, the same address as `AdvertiseAddr` is used.The `DataPathAddr` specifies the address that global scope network drivers will publish towards other nodes in order to reach the containers running on this node. Using this parameter it is possible to separate the container data traffic from the management traffic of the cluster. |
| RemoteAddrs   | Array of stringsAddresses of manager nodes already participating in the swarm.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| JoinToken     | stringSecret token for joining this swarm.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

### Responses

/v1.47/swarm/join

### Request samples

* Payload

Content type

application/json

`{
"ListenAddr": "0.0.0.0:2377",
"AdvertiseAddr": "192.168.1.1:2377",
"DataPathAddr": "192.168.1.1",
"RemoteAddrs": [
"node1:2377"
],
"JoinToken": "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2"
}`

### Response samples

* 400
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Swarm/operation/SwarmLeave)Leave a swarm

##### query Parameters

|       |                                                                                                             |
| ----- | ----------------------------------------------------------------------------------------------------------- |
| force | booleanDefault: falseForce leave swarm, even if this is the last manager or that it will break the cluster. |

### Responses

/v1.47/swarm/leave

### Response samples

* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Swarm/operation/SwarmUpdate)Update a swarm

##### query Parameters

|                        |                                                                                                                     |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------- |
| versionrequired        | integer \<int64>The version number of the swarm object being updated. This is required to avoid conflicting writes. |
| rotateWorkerToken      | booleanDefault: falseRotate the worker join token.                                                                  |
| rotateManagerToken     | booleanDefault: falseRotate the manager join token.                                                                 |
| rotateManagerUnlockKey | booleanDefault: falseRotate the manager unlock key.                                                                 |

##### Request Body schema:application/jsonrequired

|      |                                                    |
| ---- | -------------------------------------------------- |
| Name | stringName of the swarm.                           |
|      | objectUser-defined key/value metadata.             |
|      | object or nullOrchestration configuration.         |
|      | objectRaft configuration.                          |
|      | object or nullDispatcher configuration.            |
|      | object or nullCA configuration.                    |
|      | objectParameters related to encryption-at-rest.    |
|      | objectDefaults for creating tasks in this cluster. |

### Responses

/v1.47/swarm/update

### Request samples

* Payload

Content type

application/json

`{
"Name": "default",
"Labels": {
"com.example.corp.type": "production",
"com.example.corp.department": "engineering"
},
"Orchestration": {
"TaskHistoryRetentionLimit": 10
},
"Raft": {
"SnapshotInterval": 10000,
"KeepOldSnapshots": 0,
"LogEntriesForSlowFollowers": 500,
"ElectionTick": 3,
"HeartbeatTick": 1
},
"Dispatcher": {
"HeartbeatPeriod": 5000000000
},
"CAConfig": {
"NodeCertExpiry": 7776000000000000,
"ExternalCAs": [
{
"Protocol": "cfssl",
"URL": "string",
"Options": {
"property1": "string",
"property2": "string"
},
"CACert": "string"
}
],
"SigningCACert": "string",
"SigningCAKey": "string",
"ForceRotate": 0
},
"EncryptionConfig": {
"AutoLockManagers": false
},
"TaskDefaults": {
"LogDriver": {
"Name": "json-file",
"Options": {
"max-file": "10",
"max-size": "100m"
}
}
}
}`

### Response samples

* 400
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Swarm/operation/SwarmUnlockkey)Get the unlock key

### Responses

/v1.47/swarm/unlockkey

### Response samples

* 200
* 500
* 503

Content type

application/json

`{
"UnlockKey": "SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8"
}`

## [](#tag/Swarm/operation/SwarmUnlock)Unlock a locked manager

##### Request Body schema: application/jsonrequired

|           |                               |
| --------- | ----------------------------- |
| UnlockKey | stringThe swarm's unlock key. |

### Responses

/v1.47/swarm/unlock

### Request samples

* Payload

Content type

application/json

`{
"UnlockKey": "SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8"
}`

### Response samples

* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Node)Nodes

Nodes are instances of the Engine participating in a swarm. Swarm mode must be enabled for these endpoints to work.

## [](#tag/Node/operation/NodeList)List nodes

##### query Parameters

|         |                                                                                                                                                                                                                                                                              |
| ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringFilters to process on the nodes list, encoded as JSON (a `map[string][]string`).Available filters:- `id=<node id>`
- `label=<engine label>`
- `membership=`(`accepted`\|`pending`)\`
- `name=<node name>`
- `node.label=<node label>`
- `role=`(`manager`\|`worker`)\` |

### Responses

/v1.47/nodes

### Response samples

* 200
* 500
* 503

Content type

application/json

`[
{
"ID": "24ifsmvkjbyhk",
"Version": {
"Index": 373531
},
"CreatedAt": "2016-08-18T10:44:24.496525531Z",
"UpdatedAt": "2017-08-09T07:09:37.632105588Z",
"Spec": {
"Availability": "active",
"Name": "node-name",
"Role": "manager",
"Labels": {
"foo": "bar"
}
},
"Description": {
"Hostname": "bf3067039e47",
"Platform": {
"Architecture": "x86_64",
"OS": "linux"
},
"Resources": {
"NanoCPUs": 4000000000,
"MemoryBytes": 8272408576,
"GenericResources": [
{
"DiscreteResourceSpec": {
"Kind": "SSD",
"Value": 3
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID1"
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID2"
}
}
]
},
"Engine": {
"EngineVersion": "17.06.0",
"Labels": {
"foo": "bar"
},
"Plugins": [
{
"Type": "Log",
"Name": "awslogs"
},
{
"Type": "Log",
"Name": "fluentd"
},
{
"Type": "Log",
"Name": "gcplogs"
},
{
"Type": "Log",
"Name": "gelf"
},
{
"Type": "Log",
"Name": "journald"
},
{
"Type": "Log",
"Name": "json-file"
},
{
"Type": "Log",
"Name": "splunk"
},
{
"Type": "Log",
"Name": "syslog"
},
{
"Type": "Network",
"Name": "bridge"
},
{
"Type": "Network",
"Name": "host"
},
{
"Type": "Network",
"Name": "ipvlan"
},
{
"Type": "Network",
"Name": "macvlan"
},
{
"Type": "Network",
"Name": "null"
},
{
"Type": "Network",
"Name": "overlay"
},
{
"Type": "Volume",
"Name": "local"
},
{
"Type": "Volume",
"Name": "localhost:5000/vieux/sshfs:latest"
},
{
"Type": "Volume",
"Name": "vieux/sshfs:latest"
}
]
},
"TLSInfo": {
"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n",
"CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
"CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="
}
},
"Status": {
"State": "ready",
"Message": "",
"Addr": "172.17.0.2"
},
"ManagerStatus": {
"Leader": true,
"Reachability": "reachable",
"Addr": "10.0.0.46:2377"
}
}
]`

## [](#tag/Node/operation/NodeInspect)Inspect a node

##### path Parameters

|            |                                  |
| ---------- | -------------------------------- |
| idrequired | stringThe ID or name of the node |

### Responses

/v1.47/nodes/{id}

### Response samples

* 200
* 404
* 500
* 503

Content type

application/json

`{
"ID": "24ifsmvkjbyhk",
"Version": {
"Index": 373531
},
"CreatedAt": "2016-08-18T10:44:24.496525531Z",
"UpdatedAt": "2017-08-09T07:09:37.632105588Z",
"Spec": {
"Availability": "active",
"Name": "node-name",
"Role": "manager",
"Labels": {
"foo": "bar"
}
},
"Description": {
"Hostname": "bf3067039e47",
"Platform": {
"Architecture": "x86_64",
"OS": "linux"
},
"Resources": {
"NanoCPUs": 4000000000,
"MemoryBytes": 8272408576,
"GenericResources": [
{
"DiscreteResourceSpec": {
"Kind": "SSD",
"Value": 3
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID1"
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID2"
}
}
]
},
"Engine": {
"EngineVersion": "17.06.0",
"Labels": {
"foo": "bar"
},
"Plugins": [
{
"Type": "Log",
"Name": "awslogs"
},
{
"Type": "Log",
"Name": "fluentd"
},
{
"Type": "Log",
"Name": "gcplogs"
},
{
"Type": "Log",
"Name": "gelf"
},
{
"Type": "Log",
"Name": "journald"
},
{
"Type": "Log",
"Name": "json-file"
},
{
"Type": "Log",
"Name": "splunk"
},
{
"Type": "Log",
"Name": "syslog"
},
{
"Type": "Network",
"Name": "bridge"
},
{
"Type": "Network",
"Name": "host"
},
{
"Type": "Network",
"Name": "ipvlan"
},
{
"Type": "Network",
"Name": "macvlan"
},
{
"Type": "Network",
"Name": "null"
},
{
"Type": "Network",
"Name": "overlay"
},
{
"Type": "Volume",
"Name": "local"
},
{
"Type": "Volume",
"Name": "localhost:5000/vieux/sshfs:latest"
},
{
"Type": "Volume",
"Name": "vieux/sshfs:latest"
}
]
},
"TLSInfo": {
"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n",
"CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
"CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="
}
},
"Status": {
"State": "ready",
"Message": "",
"Addr": "172.17.0.2"
},
"ManagerStatus": {
"Leader": true,
"Reachability": "reachable",
"Addr": "10.0.0.46:2377"
}
}`

## [](#tag/Node/operation/NodeDelete)Delete a node

##### path Parameters

|            |                                  |
| ---------- | -------------------------------- |
| idrequired | stringThe ID or name of the node |

##### query Parameters

|       |                                                         |
| ----- | ------------------------------------------------------- |
| force | booleanDefault: falseForce remove a node from the swarm |

### Responses

/v1.47/nodes/{id}

### Response samples

* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Node/operation/NodeUpdate)Update a node

##### path Parameters

|            |                          |
| ---------- | ------------------------ |
| idrequired | stringThe ID of the node |

##### query Parameters

|                 |                                                                                                                    |
| --------------- | ------------------------------------------------------------------------------------------------------------------ |
| versionrequired | integer \<int64>The version number of the node object being updated. This is required to avoid conflicting writes. |

##### Request Body schema:application/json

|              |                                                               |
| ------------ | ------------------------------------------------------------- |
| Name         | stringName for the node.                                      |
|              | objectUser-defined key/value metadata.                        |
| Role         | stringEnum: "worker" "manager"Role of the node.               |
| Availability | stringEnum: "active" "pause" "drain"Availability of the node. |

### Responses

/v1.47/nodes/{id}/update

### Request samples

* Payload

Content type

application/json

`{
"Availability": "active",
"Name": "node-name",
"Role": "manager",
"Labels": {
"foo": "bar"
}
}`

### Response samples

* 400
* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Service)Services

Services are the definitions of tasks to run on a swarm. Swarm mode must be enabled for these endpoints to work.

## [](#tag/Service/operation/ServiceList)List services

##### query Parameters

|         |                                                                                                                                                                                                                               |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the services list.Available filters:- `id=<service id>`
- `label=<service label>`
- `mode=["replicated"\|"global"]`
- `name=<service name>` |
| status  | booleanInclude service status, with count of running and desired tasks.                                                                                                                                                       |

### Responses

/v1.47/services

### Response samples

* 200
* 500
* 503

Content type

application/json

`[
{
"ID": "9mnpnzenvg8p8tdbtq4wvbkcz",
"Version": {
"Index": 19
},
"CreatedAt": "2016-06-07T21:05:51.880065305Z",
"UpdatedAt": "2016-06-07T21:07:29.962229872Z",
"Spec": {
"Name": "hopeful_cori",
"TaskTemplate": {
"ContainerSpec": {
"Image": "redis"
},
"Resources": {
"Limits": { },
"Reservations": { }
},
"RestartPolicy": {
"Condition": "any",
"MaxAttempts": 0
},
"Placement": { },
"ForceUpdate": 0
},
"Mode": {
"Replicated": {
"Replicas": 1
}
},
"UpdateConfig": {
"Parallelism": 1,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15
},
"RollbackConfig": {
"Parallelism": 1,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15
},
"EndpointSpec": {
"Mode": "vip",
"Ports": [
{
"Protocol": "tcp",
"TargetPort": 6379,
"PublishedPort": 30001
}
]
}
},
"Endpoint": {
"Spec": {
"Mode": "vip",
"Ports": [
{
"Protocol": "tcp",
"TargetPort": 6379,
"PublishedPort": 30001
}
]
},
"Ports": [
{
"Protocol": "tcp",
"TargetPort": 6379,
"PublishedPort": 30001
}
],
"VirtualIPs": [
{
"NetworkID": "4qvuz4ko70xaltuqbt8956gd1",
"Addr": "10.255.0.2/16"
},
{
"NetworkID": "4qvuz4ko70xaltuqbt8956gd1",
"Addr": "10.255.0.3/16"
}
]
}
}
]`

## [](#tag/Service/operation/ServiceCreate)Create a service

##### header Parameters

|                 |                                                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| X-Registry-Auth | stringA base64url-encoded auth configuration for pulling from private registries.Refer to the [authentication section](#section/Authentication) for details. |

##### Request Body schema: application/jsonrequired

|      |                                                                                                                                                                                                          |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name | stringName of the service.                                                                                                                                                                               |
|      | objectUser-defined key/value metadata.                                                                                                                                                                   |
|      | object (TaskSpec)User modifiable task configuration.                                                                                                                                                     |
|      | objectScheduling mode for the service.                                                                                                                                                                   |
|      | objectSpecification for the update strategy of the service.                                                                                                                                              |
|      | objectSpecification for the rollback strategy of the service.                                                                                                                                            |
|      | Array of objects (NetworkAttachmentConfig)Specifies which networks the service should attach to.Deprecated: This field is deprecated since v1.44. The Networks field in TaskSpec should be used instead. |
|      | object (EndpointSpec)Properties that can be configured to access and load balance a service.                                                                                                             |

### Responses

/v1.47/services/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "web",
"Labels": {
"property1": "string",
"property2": "string",
"foo": "bar"
},
"TaskTemplate": {
"PluginSpec": {
"Name": "string",
"Remote": "string",
"Disabled": true,
"PluginPrivilege": [
{
"Name": "network",
"Description": "string",
"Value": [
"host"
]
}
]
},
"ContainerSpec": {
"Image": "nginx:alpine",
"Labels": {
"property1": "string",
"property2": "string"
},
"Command": [
"string"
],
"Args": [
"string"
],
"Hostname": "string",
"Env": [
"string"
],
"Dir": "string",
"User": "33",
"Groups": [
"string"
],
"Privileges": {
"CredentialSpec": {
"Config": "0bt9dmxjvjiqermk6xrop3ekq",
"File": "spec.json",
"Registry": "string"
},
"SELinuxContext": {
"Disable": true,
"User": "string",
"Role": "string",
"Type": "string",
"Level": "string"
},
"Seccomp": {
"Mode": "default",
"Profile": "string"
},
"AppArmor": {
"Mode": "default"
},
"NoNewPrivileges": true
},
"TTY": true,
"OpenStdin": true,
"ReadOnly": true,
"Mounts": [
{
"Target": "/usr/share/nginx/html",
"Source": "web-data",
"Type": "volume",
"ReadOnly": true,
"Consistency": "string",
"BindOptions": {
"Propagation": "private",
"NonRecursive": false,
"CreateMountpoint": false,
"ReadOnlyNonRecursive": false,
"ReadOnlyForceRecursive": false
},
"VolumeOptions": {
"NoCopy": false,
"Labels": {
"property1": "string",
"property2": "string",
"com.example.something": "something-value"
},
"DriverConfig": {
"Name": "string",
"Options": {
"property1": "string",
"property2": "string"
}
},
"Subpath": "dir-inside-volume/subdirectory"
},
"TmpfsOptions": {
"SizeBytes": 0,
"Mode": 0,
"Options": [ [
"noexec"
]
]
}
}
],
"StopSignal": "string",
"StopGracePeriod": 0,
"HealthCheck": {
"Test": [
"string"
],
"Interval": 0,
"Timeout": 0,
"Retries": 0,
"StartPeriod": 0,
"StartInterval": 0
},
"Hosts": [
"10.10.10.10 host1",
"ABCD:EF01:2345:6789:ABCD:EF01:2345:6789 host2"
],
"DNSConfig": {
"Nameservers": [
"8.8.8.8"
],
"Search": [
"example.org"
],
"Options": [
"timeout:3"
]
},
"Secrets": [
{
"File": {
"Name": "www.example.org.key",
"UID": "33",
"GID": "33",
"Mode": 384
},
"SecretID": "fpjqlhnwb19zds35k8wn80lq9",
"SecretName": "example_org_domain_key"
}
],
"OomScoreAdj": 0,
"Configs": [
{
"File": {
"Name": "string",
"UID": "string",
"GID": "string",
"Mode": 0
},
"Runtime": { },
"ConfigID": "string",
"ConfigName": "string"
}
],
"Isolation": "default",
"Init": true,
"Sysctls": {
"property1": "string",
"property2": "string"
},
"CapabilityAdd": [
"CAP_NET_RAW",
"CAP_SYS_ADMIN",
"CAP_SYS_CHROOT",
"CAP_SYSLOG"
],
"CapabilityDrop": [
"CAP_NET_RAW"
],
"Ulimits": [
{
"Name": "string",
"Soft": 0,
"Hard": 0
}
]
},
"NetworkAttachmentSpec": {
"ContainerID": "string"
},
"Resources": {
"Limits": {
"NanoCPUs": 4000000000,
"MemoryBytes": 104857600,
"Pids": 100
},
"Reservations": {
"NanoCPUs": 4000000000,
"MemoryBytes": 8272408576,
"GenericResources": [
{
"DiscreteResourceSpec": {
"Kind": "SSD",
"Value": 3
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID1"
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID2"
}
}
]
}
},
"RestartPolicy": {
"Condition": "on-failure",
"Delay": 10000000000,
"MaxAttempts": 10,
"Window": 0
},
"Placement": {
"Constraints": [
"node.hostname!=node3.corp.example.com",
"node.role!=manager",
"node.labels.type==production",
"node.platform.os==linux",
"node.platform.arch==x86_64"
],
"Preferences": [
{
"Spread": {
"SpreadDescriptor": "node.labels.datacenter"
}
},
{
"Spread": {
"SpreadDescriptor": "node.labels.rack"
}
}
],
"MaxReplicas": 0,
"Platforms": [
{
"Architecture": "x86_64",
"OS": "linux"
}
]
},
"ForceUpdate": 0,
"Runtime": "string",
"Networks": [
{
"Target": "string",
"Aliases": [
"string"
],
"DriverOpts": {
"property1": "string",
"property2": "string"
}
}
],
"LogDriver": {
"Name": "json-file",
"Options": {
"property1": "string",
"property2": "string",
"max-file": "3",
"max-size": "10M"
}
}
},
"Mode": {
"Replicated": {
"Replicas": 4
},
"Global": { },
"ReplicatedJob": {
"MaxConcurrent": 1,
"TotalCompletions": 0
},
"GlobalJob": { }
},
"UpdateConfig": {
"Parallelism": 2,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15,
"Order": "stop-first"
},
"RollbackConfig": {
"Parallelism": 1,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15,
"Order": "stop-first"
},
"Networks": [
{
"Target": "string",
"Aliases": [
"string"
],
"DriverOpts": {
"property1": "string",
"property2": "string"
}
}
],
"EndpointSpec": {
"Mode": "vip",
"Ports": [
{
"Name": "string",
"Protocol": "tcp",
"TargetPort": 80,
"PublishedPort": 8080,
"PublishMode": "ingress"
}
]
}
}`

### Response samples

* 201
* 400
* 403
* 409
* 500
* 503

Content type

application/json

`{
"ID": "ak7w3gjqoa3kuz8xcpnyy0pvl",
"Warnings": [
"unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"
]
}`

## [](#tag/Service/operation/ServiceInspect)Inspect a service

##### path Parameters

|            |                              |
| ---------- | ---------------------------- |
| idrequired | stringID or name of service. |

##### query Parameters

|                |                                                             |
| -------------- | ----------------------------------------------------------- |
| insertDefaults | booleanDefault: falseFill empty fields with default values. |

### Responses

/v1.47/services/{id}

### Response samples

* 200
* 404
* 500
* 503

Content type

application/json

`{
"ID": "9mnpnzenvg8p8tdbtq4wvbkcz",
"Version": {
"Index": 19
},
"CreatedAt": "2016-06-07T21:05:51.880065305Z",
"UpdatedAt": "2016-06-07T21:07:29.962229872Z",
"Spec": {
"Name": "hopeful_cori",
"TaskTemplate": {
"ContainerSpec": {
"Image": "redis"
},
"Resources": {
"Limits": { },
"Reservations": { }
},
"RestartPolicy": {
"Condition": "any",
"MaxAttempts": 0
},
"Placement": { },
"ForceUpdate": 0
},
"Mode": {
"Replicated": {
"Replicas": 1
}
},
"UpdateConfig": {
"Parallelism": 1,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15
},
"RollbackConfig": {
"Parallelism": 1,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15
},
"EndpointSpec": {
"Mode": "vip",
"Ports": [
{
"Protocol": "tcp",
"TargetPort": 6379,
"PublishedPort": 30001
}
]
}
},
"Endpoint": {
"Spec": {
"Mode": "vip",
"Ports": [
{
"Protocol": "tcp",
"TargetPort": 6379,
"PublishedPort": 30001
}
]
},
"Ports": [
{
"Protocol": "tcp",
"TargetPort": 6379,
"PublishedPort": 30001
}
],
"VirtualIPs": [
{
"NetworkID": "4qvuz4ko70xaltuqbt8956gd1",
"Addr": "10.255.0.2/16"
},
{
"NetworkID": "4qvuz4ko70xaltuqbt8956gd1",
"Addr": "10.255.0.3/16"
}
]
}
}`

## [](#tag/Service/operation/ServiceDelete)Delete a service

##### path Parameters

|            |                              |
| ---------- | ---------------------------- |
| idrequired | stringID or name of service. |

### Responses

/v1.47/services/{id}

### Response samples

* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Service/operation/ServiceUpdate)Update a service

##### path Parameters

|            |                              |
| ---------- | ---------------------------- |
| idrequired | stringID or name of service. |

##### query Parameters

|                  |                                                                                                                                                                                                                                                                            |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| versionrequired  | integerThe version number of the service object being updated. This is required to avoid conflicting writes. This version number should be the value as currently set on the service *before* the update. You can find the current version by calling `GET /services/{id}` |
| registryAuthFrom | stringDefault: "spec"Enum: "spec" "previous-spec"If the `X-Registry-Auth` header is not specified, this parameter indicates where to find registry authorization credentials.                                                                                              |
| rollback         | stringSet to this parameter to `previous` to cause a server-side rollback to the previous service spec. The supplied spec will be ignored in this case.                                                                                                                    |

##### header Parameters

|                 |                                                                                                                                                              |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| X-Registry-Auth | stringA base64url-encoded auth configuration for pulling from private registries.Refer to the [authentication section](#section/Authentication) for details. |

##### Request Body schema: application/jsonrequired

|      |                                                                                                                                                                                                          |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name | stringName of the service.                                                                                                                                                                               |
|      | objectUser-defined key/value metadata.                                                                                                                                                                   |
|      | object (TaskSpec)User modifiable task configuration.                                                                                                                                                     |
|      | objectScheduling mode for the service.                                                                                                                                                                   |
|      | objectSpecification for the update strategy of the service.                                                                                                                                              |
|      | objectSpecification for the rollback strategy of the service.                                                                                                                                            |
|      | Array of objects (NetworkAttachmentConfig)Specifies which networks the service should attach to.Deprecated: This field is deprecated since v1.44. The Networks field in TaskSpec should be used instead. |
|      | object (EndpointSpec)Properties that can be configured to access and load balance a service.                                                                                                             |

### Responses

/v1.47/services/{id}/update

### Request samples

* Payload

Content type

application/json

`{
"Name": "top",
"Labels": {
"property1": "string",
"property2": "string"
},
"TaskTemplate": {
"PluginSpec": {
"Name": "string",
"Remote": "string",
"Disabled": true,
"PluginPrivilege": [
{
"Name": "network",
"Description": "string",
"Value": [
"host"
]
}
]
},
"ContainerSpec": {
"Image": "busybox",
"Labels": {
"property1": "string",
"property2": "string"
},
"Command": [
"string"
],
"Args": [
"top"
],
"Hostname": "string",
"Env": [
"string"
],
"Dir": "string",
"User": "string",
"Groups": [
"string"
],
"Privileges": {
"CredentialSpec": {
"Config": "0bt9dmxjvjiqermk6xrop3ekq",
"File": "spec.json",
"Registry": "string"
},
"SELinuxContext": {
"Disable": true,
"User": "string",
"Role": "string",
"Type": "string",
"Level": "string"
},
"Seccomp": {
"Mode": "default",
"Profile": "string"
},
"AppArmor": {
"Mode": "default"
},
"NoNewPrivileges": true
},
"TTY": true,
"OpenStdin": true,
"ReadOnly": true,
"Mounts": [
{
"Target": "string",
"Source": "string",
"Type": "volume",
"ReadOnly": true,
"Consistency": "string",
"BindOptions": {
"Propagation": "private",
"NonRecursive": false,
"CreateMountpoint": false,
"ReadOnlyNonRecursive": false,
"ReadOnlyForceRecursive": false
},
"VolumeOptions": {
"NoCopy": false,
"Labels": {
"property1": "string",
"property2": "string"
},
"DriverConfig": {
"Name": "string",
"Options": {
"property1": "string",
"property2": "string"
}
},
"Subpath": "dir-inside-volume/subdirectory"
},
"TmpfsOptions": {
"SizeBytes": 0,
"Mode": 0,
"Options": [ [
"noexec"
]
]
}
}
],
"StopSignal": "string",
"StopGracePeriod": 0,
"HealthCheck": {
"Test": [
"string"
],
"Interval": 0,
"Timeout": 0,
"Retries": 0,
"StartPeriod": 0,
"StartInterval": 0
},
"Hosts": [
"string"
],
"DNSConfig": {
"Nameservers": [
"string"
],
"Search": [
"string"
],
"Options": [
"string"
]
},
"Secrets": [
{
"File": {
"Name": "string",
"UID": "string",
"GID": "string",
"Mode": 0
},
"SecretID": "string",
"SecretName": "string"
}
],
"OomScoreAdj": 0,
"Configs": [
{
"File": {
"Name": "string",
"UID": "string",
"GID": "string",
"Mode": 0
},
"Runtime": { },
"ConfigID": "string",
"ConfigName": "string"
}
],
"Isolation": "default",
"Init": true,
"Sysctls": {
"property1": "string",
"property2": "string"
},
"CapabilityAdd": [
"CAP_NET_RAW",
"CAP_SYS_ADMIN",
"CAP_SYS_CHROOT",
"CAP_SYSLOG"
],
"CapabilityDrop": [
"CAP_NET_RAW"
],
"Ulimits": [
{
"Name": "string",
"Soft": 0,
"Hard": 0
}
]
},
"NetworkAttachmentSpec": {
"ContainerID": "string"
},
"Resources": {
"Limits": {
"NanoCPUs": 4000000000,
"MemoryBytes": 8272408576,
"Pids": 100
},
"Reservations": {
"NanoCPUs": 4000000000,
"MemoryBytes": 8272408576,
"GenericResources": [
{
"DiscreteResourceSpec": {
"Kind": "SSD",
"Value": 3
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID1"
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID2"
}
}
]
}
},
"RestartPolicy": {
"Condition": "any",
"Delay": 0,
"MaxAttempts": 0,
"Window": 0
},
"Placement": {
"Constraints": [
"node.hostname!=node3.corp.example.com",
"node.role!=manager",
"node.labels.type==production",
"node.platform.os==linux",
"node.platform.arch==x86_64"
],
"Preferences": [
{
"Spread": {
"SpreadDescriptor": "node.labels.datacenter"
}
},
{
"Spread": {
"SpreadDescriptor": "node.labels.rack"
}
}
],
"MaxReplicas": 0,
"Platforms": [
{
"Architecture": "x86_64",
"OS": "linux"
}
]
},
"ForceUpdate": 0,
"Runtime": "string",
"Networks": [
{
"Target": "string",
"Aliases": [
"string"
],
"DriverOpts": {
"property1": "string",
"property2": "string"
}
}
],
"LogDriver": {
"Name": "string",
"Options": {
"property1": "string",
"property2": "string"
}
}
},
"Mode": {
"Replicated": {
"Replicas": 1
},
"Global": { },
"ReplicatedJob": {
"MaxConcurrent": 1,
"TotalCompletions": 0
},
"GlobalJob": { }
},
"UpdateConfig": {
"Parallelism": 2,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15,
"Order": "stop-first"
},
"RollbackConfig": {
"Parallelism": 1,
"Delay": 1000000000,
"FailureAction": "pause",
"Monitor": 15000000000,
"MaxFailureRatio": 0.15,
"Order": "stop-first"
},
"Networks": [
{
"Target": "string",
"Aliases": [
"string"
],
"DriverOpts": {
"property1": "string",
"property2": "string"
}
}
],
"EndpointSpec": {
"Mode": "vip",
"Ports": [
{
"Name": "string",
"Protocol": "tcp",
"TargetPort": 0,
"PublishedPort": 0,
"PublishMode": "ingress"
}
]
}
}`

### Response samples

* 200
* 400
* 404
* 500
* 503

Content type

application/json

`{
"Warnings": [
"unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"
]
}`

## [](#tag/Service/operation/ServiceLogs)Get service logs

Get `stdout` and `stderr` logs from a service. See also [`/containers/{id}/logs`](#operation/ContainerLogs).

**Note**: This endpoint works only for services with the `local`, `json-file` or `journald` logging drivers.

##### path Parameters

|            |                                 |
| ---------- | ------------------------------- |
| idrequired | stringID or name of the service |

##### query Parameters

|            |                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| details    | booleanDefault: falseShow service context and extra details provided to logs.                                                              |
| follow     | booleanDefault: falseKeep connection after returning logs.                                                                                 |
| stdout     | booleanDefault: falseReturn logs from `stdout`                                                                                             |
| stderr     | booleanDefault: falseReturn logs from `stderr`                                                                                             |
| since      | integerDefault: 0Only return logs since this time, as a UNIX timestamp                                                                     |
| timestamps | booleanDefault: falseAdd timestamps to every log line                                                                                      |
| tail       | stringDefault: "all"Only return this number of log lines from the end of the logs. Specify as an integer or `all` to output all log lines. |

### Responses

/v1.47/services/{id}/logs

### Response samples

* 404

Content type

application/vnd.docker.raw-stream

No sample

## [](#tag/Task)Tasks

A task is a container running on a swarm. It is the atomic scheduling unit of swarm. Swarm mode must be enabled for these endpoints to work.

## [](#tag/Task/operation/TaskList)List tasks

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                         |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the tasks list.Available filters:- `desired-state=(running \| shutdown \| accepted)`
- `id=<task id>`
- `label=key` or `label="key=value"`
- `name=<task name>`
- `node=<node id or name>`
- `service=<service name>` |

### Responses

/v1.47/tasks

### Response samples

* 200
* 500
* 503

Content type

application/json

`[
{
"ID": "0kzzo1i0y4jz6027t0k7aezc7",
"Version": {
"Index": 71
},
"CreatedAt": "2016-06-07T21:07:31.171892745Z",
"UpdatedAt": "2016-06-07T21:07:31.376370513Z",
"Spec": {
"ContainerSpec": {
"Image": "redis"
},
"Resources": {
"Limits": { },
"Reservations": { }
},
"RestartPolicy": {
"Condition": "any",
"MaxAttempts": 0
},
"Placement": { }
},
"ServiceID": "9mnpnzenvg8p8tdbtq4wvbkcz",
"Slot": 1,
"NodeID": "60gvrl6tm78dmak4yl7srz94v",
"Status": {
"Timestamp": "2016-06-07T21:07:31.290032978Z",
"State": "running",
"Message": "started",
"ContainerStatus": {
"ContainerID": "e5d62702a1b48d01c3e02ca1e0212a250801fa8d67caca0b6f35919ebc12f035",
"PID": 677
}
},
"DesiredState": "running",
"NetworksAttachments": [
{
"Network": {
"ID": "4qvuz4ko70xaltuqbt8956gd1",
"Version": {
"Index": 18
},
"CreatedAt": "2016-06-07T20:31:11.912919752Z",
"UpdatedAt": "2016-06-07T21:07:29.955277358Z",
"Spec": {
"Name": "ingress",
"Labels": {
"com.docker.swarm.internal": "true"
},
"DriverConfiguration": { },
"IPAMOptions": {
"Driver": { },
"Configs": [
{
"Subnet": "10.255.0.0/16",
"Gateway": "10.255.0.1"
}
]
}
},
"DriverState": {
"Name": "overlay",
"Options": {
"com.docker.network.driver.overlay.vxlanid_list": "256"
}
},
"IPAMOptions": {
"Driver": {
"Name": "default"
},
"Configs": [
{
"Subnet": "10.255.0.0/16",
"Gateway": "10.255.0.1"
}
]
}
},
"Addresses": [
"10.255.0.10/16"
]
}
]
},
{
"ID": "1yljwbmlr8er2waf8orvqpwms",
"Version": {
"Index": 30
},
"CreatedAt": "2016-06-07T21:07:30.019104782Z",
"UpdatedAt": "2016-06-07T21:07:30.231958098Z",
"Name": "hopeful_cori",
"Spec": {
"ContainerSpec": {
"Image": "redis"
},
"Resources": {
"Limits": { },
"Reservations": { }
},
"RestartPolicy": {
"Condition": "any",
"MaxAttempts": 0
},
"Placement": { }
},
"ServiceID": "9mnpnzenvg8p8tdbtq4wvbkcz",
"Slot": 1,
"NodeID": "60gvrl6tm78dmak4yl7srz94v",
"Status": {
"Timestamp": "2016-06-07T21:07:30.202183143Z",
"State": "shutdown",
"Message": "shutdown",
"ContainerStatus": {
"ContainerID": "1cf8d63d18e79668b0004a4be4c6ee58cddfad2dae29506d8781581d0688a213"
}
},
"DesiredState": "shutdown",
"NetworksAttachments": [
{
"Network": {
"ID": "4qvuz4ko70xaltuqbt8956gd1",
"Version": {
"Index": 18
},
"CreatedAt": "2016-06-07T20:31:11.912919752Z",
"UpdatedAt": "2016-06-07T21:07:29.955277358Z",
"Spec": {
"Name": "ingress",
"Labels": {
"com.docker.swarm.internal": "true"
},
"DriverConfiguration": { },
"IPAMOptions": {
"Driver": { },
"Configs": [
{
"Subnet": "10.255.0.0/16",
"Gateway": "10.255.0.1"
}
]
}
},
"DriverState": {
"Name": "overlay",
"Options": {
"com.docker.network.driver.overlay.vxlanid_list": "256"
}
},
"IPAMOptions": {
"Driver": {
"Name": "default"
},
"Configs": [
{
"Subnet": "10.255.0.0/16",
"Gateway": "10.255.0.1"
}
]
}
},
"Addresses": [
"10.255.0.5/16"
]
}
]
}
]`

## [](#tag/Task/operation/TaskInspect)Inspect a task

##### path Parameters

|            |                      |
| ---------- | -------------------- |
| idrequired | stringID of the task |

### Responses

/v1.47/tasks/{id}

### Response samples

* 200
* 404
* 500
* 503

Content type

application/json

`{
"ID": "0kzzo1i0y4jz6027t0k7aezc7",
"Version": {
"Index": 71
},
"CreatedAt": "2016-06-07T21:07:31.171892745Z",
"UpdatedAt": "2016-06-07T21:07:31.376370513Z",
"Spec": {
"ContainerSpec": {
"Image": "redis"
},
"Resources": {
"Limits": { },
"Reservations": { }
},
"RestartPolicy": {
"Condition": "any",
"MaxAttempts": 0
},
"Placement": { }
},
"ServiceID": "9mnpnzenvg8p8tdbtq4wvbkcz",
"Slot": 1,
"NodeID": "60gvrl6tm78dmak4yl7srz94v",
"Status": {
"Timestamp": "2016-06-07T21:07:31.290032978Z",
"State": "running",
"Message": "started",
"ContainerStatus": {
"ContainerID": "e5d62702a1b48d01c3e02ca1e0212a250801fa8d67caca0b6f35919ebc12f035",
"PID": 677
}
},
"DesiredState": "running",
"NetworksAttachments": [
{
"Network": {
"ID": "4qvuz4ko70xaltuqbt8956gd1",
"Version": {
"Index": 18
},
"CreatedAt": "2016-06-07T20:31:11.912919752Z",
"UpdatedAt": "2016-06-07T21:07:29.955277358Z",
"Spec": {
"Name": "ingress",
"Labels": {
"com.docker.swarm.internal": "true"
},
"DriverConfiguration": { },
"IPAMOptions": {
"Driver": { },
"Configs": [
{
"Subnet": "10.255.0.0/16",
"Gateway": "10.255.0.1"
}
]
}
},
"DriverState": {
"Name": "overlay",
"Options": {
"com.docker.network.driver.overlay.vxlanid_list": "256"
}
},
"IPAMOptions": {
"Driver": {
"Name": "default"
},
"Configs": [
{
"Subnet": "10.255.0.0/16",
"Gateway": "10.255.0.1"
}
]
}
},
"Addresses": [
"10.255.0.10/16"
]
}
],
"AssignedGenericResources": [
{
"DiscreteResourceSpec": {
"Kind": "SSD",
"Value": 3
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID1"
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID2"
}
}
]
}`

## [](#tag/Task/operation/TaskLogs)Get task logs

Get `stdout` and `stderr` logs from a task. See also [`/containers/{id}/logs`](#operation/ContainerLogs).

**Note**: This endpoint works only for services with the `local`, `json-file` or `journald` logging drivers.

##### path Parameters

|            |                      |
| ---------- | -------------------- |
| idrequired | stringID of the task |

##### query Parameters

|            |                                                                                                                                            |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| details    | booleanDefault: falseShow task context and extra details provided to logs.                                                                 |
| follow     | booleanDefault: falseKeep connection after returning logs.                                                                                 |
| stdout     | booleanDefault: falseReturn logs from `stdout`                                                                                             |
| stderr     | booleanDefault: falseReturn logs from `stderr`                                                                                             |
| since      | integerDefault: 0Only return logs since this time, as a UNIX timestamp                                                                     |
| timestamps | booleanDefault: falseAdd timestamps to every log line                                                                                      |
| tail       | stringDefault: "all"Only return this number of log lines from the end of the logs. Specify as an integer or `all` to output all log lines. |

### Responses

/v1.47/tasks/{id}/logs

### Response samples

* 404

Content type

application/vnd.docker.raw-stream

No sample

## [](#tag/Secret)Secrets

Secrets are sensitive data that can be used by services. Swarm mode must be enabled for these endpoints to work.

## [](#tag/Secret/operation/SecretList)List secrets

##### query Parameters

|         |                                                                                                                                                                                                                             |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the secrets list.Available filters:- `id=<secret id>`
- `label=<key> or label=<key>=value`
- `name=<secret name>`
- `names=<secret name>` |

### Responses

/v1.47/secrets

### Response samples

* 200
* 500
* 503

Content type

application/json

`[
{
"ID": "blt1owaxmitz71s9v5zh81zun",
"Version": {
"Index": 85
},
"CreatedAt": "2017-07-20T13:55:28.678958722Z",
"UpdatedAt": "2017-07-20T13:55:28.678958722Z",
"Spec": {
"Name": "mysql-passwd",
"Labels": {
"some.label": "some.value"
},
"Driver": {
"Name": "secret-bucket",
"Options": {
"OptionA": "value for driver option A",
"OptionB": "value for driver option B"
}
}
}
},
{
"ID": "ktnbjxoalbkvbvedmg1urrz8h",
"Version": {
"Index": 11
},
"CreatedAt": "2016-11-05T01:20:17.327670065Z",
"UpdatedAt": "2016-11-05T01:20:17.327670065Z",
"Spec": {
"Name": "app-dev.crt",
"Labels": {
"foo": "bar"
}
}
}
]`

## [](#tag/Secret/operation/SecretCreate)Create a secret

##### Request Body schema: application/json

|      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name | stringUser-defined name of the secret.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|      | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Data | stringData is the data to store as a secret, formatted as a standard base64-encoded ([RFC 4648](https://tools.ietf.org/html/rfc4648#section-4)) string. It must be empty if the Driver field is set, in which case the data is loaded from an external secret store. The maximum allowed size is 500KB, as defined in [MaxSecretSize](https://pkg.go.dev/github.com/moby/swarmkit/v2@v2.0.0/api/validation#MaxSecretSize).This field is only used to *create* a secret, and is not returned by other endpoints. |
|      | object (Driver)Driver represents a driver (network, logging, secrets).                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|      | object (Driver)Driver represents a driver (network, logging, secrets).                                                                                                                                                                                                                                                                                                                                                                                                                                          |

### Responses

/v1.47/secrets/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "app-key.crt",
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value",
"foo": "bar"
},
"Data": "VEhJUyBJUyBOT1QgQSBSRUFMIENFUlRJRklDQVRFCg==",
"Driver": {
"Name": "secret-bucket",
"Options": {
"OptionA": "value for driver option A",
"OptionB": "value for driver option B"
}
},
"Templating": {
"Name": "some-driver",
"Options": {
"OptionA": "value for driver-specific option A",
"OptionB": "value for driver-specific option B"
}
}
}`

### Response samples

* 201
* 409
* 500
* 503

Content type

application/json

`{
"Id": "string"
}`

## [](#tag/Secret/operation/SecretInspect)Inspect a secret

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringID of the secret |

### Responses

/v1.47/secrets/{id}

### Response samples

* 200
* 404
* 500
* 503

Content type

application/json

`{
"ID": "ktnbjxoalbkvbvedmg1urrz8h",
"Version": {
"Index": 11
},
"CreatedAt": "2016-11-05T01:20:17.327670065Z",
"UpdatedAt": "2016-11-05T01:20:17.327670065Z",
"Spec": {
"Name": "app-dev.crt",
"Labels": {
"foo": "bar"
},
"Driver": {
"Name": "secret-bucket",
"Options": {
"OptionA": "value for driver option A",
"OptionB": "value for driver option B"
}
}
}
}`

## [](#tag/Secret/operation/SecretDelete)Delete a secret

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringID of the secret |

### Responses

/v1.47/secrets/{id}

### Response samples

* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Secret/operation/SecretUpdate)Update a Secret

##### path Parameters

|            |                                    |
| ---------- | ---------------------------------- |
| idrequired | stringThe ID or name of the secret |

##### query Parameters

|                 |                                                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------------------------------- |
| versionrequired | integer \<int64>The version number of the secret object being updated. This is required to avoid conflicting writes. |

##### Request Body schema:application/json

The spec of the secret to update. Currently, only the Labels field can be updated. All other fields must remain unchanged from the [SecretInspect endpoint](#operation/SecretInspect) response values.

|      |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name | stringUser-defined name of the secret.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|      | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| Data | stringData is the data to store as a secret, formatted as a standard base64-encoded ([RFC 4648](https://tools.ietf.org/html/rfc4648#section-4)) string. It must be empty if the Driver field is set, in which case the data is loaded from an external secret store. The maximum allowed size is 500KB, as defined in [MaxSecretSize](https://pkg.go.dev/github.com/moby/swarmkit/v2@v2.0.0/api/validation#MaxSecretSize).This field is only used to *create* a secret, and is not returned by other endpoints. |
|      | object (Driver)Driver represents a driver (network, logging, secrets).                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|      | object (Driver)Driver represents a driver (network, logging, secrets).                                                                                                                                                                                                                                                                                                                                                                                                                                          |

### Responses

/v1.47/secrets/{id}/update

### Request samples

* Payload

Content type

application/json

`{
"Name": "string",
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Data": "",
"Driver": {
"Name": "some-driver",
"Options": {
"OptionA": "value for driver-specific option A",
"OptionB": "value for driver-specific option B"
}
},
"Templating": {
"Name": "some-driver",
"Options": {
"OptionA": "value for driver-specific option A",
"OptionB": "value for driver-specific option B"
}
}
}`

### Response samples

* 400
* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Config)Configs

Configs are application configurations that can be used by services. Swarm mode must be enabled for these endpoints to work.

## [](#tag/Config/operation/ConfigList)List configs

##### query Parameters

|         |                                                                                                                                                                                                                             |
| ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the configs list.Available filters:- `id=<config id>`
- `label=<key> or label=<key>=value`
- `name=<config name>`
- `names=<config name>` |

### Responses

/v1.47/configs

### Response samples

* 200
* 500
* 503

Content type

application/json

`[
{
"ID": "ktnbjxoalbkvbvedmg1urrz8h",
"Version": {
"Index": 11
},
"CreatedAt": "2016-11-05T01:20:17.327670065Z",
"UpdatedAt": "2016-11-05T01:20:17.327670065Z",
"Spec": {
"Name": "server.conf"
}
}
]`

## [](#tag/Config/operation/ConfigCreate)Create a config

##### Request Body schema: application/json

|      |                                                                                                                                                                                                                                                                                                                                                |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name | stringUser-defined name of the config.                                                                                                                                                                                                                                                                                                         |
|      | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                                                         |
| Data | stringData is the data to store as a config, formatted as a standard base64-encoded ([RFC 4648](https://tools.ietf.org/html/rfc4648#section-4)) string. The maximum allowed size is 1000KB, as defined in [MaxConfigSize](https://pkg.go.dev/github.com/moby/swarmkit/v2@v2.0.0-20250103191802-8c1959736554/manager/controlapi#MaxConfigSize). |
|      | object (Driver)Driver represents a driver (network, logging, secrets).                                                                                                                                                                                                                                                                         |

### Responses

/v1.47/configs/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "server.conf",
"Labels": {
"property1": "string",
"property2": "string",
"foo": "bar"
},
"Data": "VEhJUyBJUyBOT1QgQSBSRUFMIENFUlRJRklDQVRFCg==",
"Templating": {
"Name": "some-driver",
"Options": {
"OptionA": "value for driver-specific option A",
"OptionB": "value for driver-specific option B"
}
}
}`

### Response samples

* 201
* 409
* 500
* 503

Content type

application/json

`{
"Id": "string"
}`

## [](#tag/Config/operation/ConfigInspect)Inspect a config

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringID of the config |

### Responses

/v1.47/configs/{id}

### Response samples

* 200
* 404
* 500
* 503

Content type

application/json

`{
"ID": "ktnbjxoalbkvbvedmg1urrz8h",
"Version": {
"Index": 11
},
"CreatedAt": "2016-11-05T01:20:17.327670065Z",
"UpdatedAt": "2016-11-05T01:20:17.327670065Z",
"Spec": {
"Name": "app-dev.crt"
}
}`

## [](#tag/Config/operation/ConfigDelete)Delete a config

##### path Parameters

|            |                        |
| ---------- | ---------------------- |
| idrequired | stringID of the config |

### Responses

/v1.47/configs/{id}

### Response samples

* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Config/operation/ConfigUpdate)Update a Config

##### path Parameters

|            |                                    |
| ---------- | ---------------------------------- |
| idrequired | stringThe ID or name of the config |

##### query Parameters

|                 |                                                                                                                      |
| --------------- | -------------------------------------------------------------------------------------------------------------------- |
| versionrequired | integer \<int64>The version number of the config object being updated. This is required to avoid conflicting writes. |

##### Request Body schema:application/json

The spec of the config to update. Currently, only the Labels field can be updated. All other fields must remain unchanged from the [ConfigInspect endpoint](#operation/ConfigInspect) response values.

|      |                                                                                                                                                                                                                                                                                                                                                |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name | stringUser-defined name of the config.                                                                                                                                                                                                                                                                                                         |
|      | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                                                         |
| Data | stringData is the data to store as a config, formatted as a standard base64-encoded ([RFC 4648](https://tools.ietf.org/html/rfc4648#section-4)) string. The maximum allowed size is 1000KB, as defined in [MaxConfigSize](https://pkg.go.dev/github.com/moby/swarmkit/v2@v2.0.0-20250103191802-8c1959736554/manager/controlapi#MaxConfigSize). |
|      | object (Driver)Driver represents a driver (network, logging, secrets).                                                                                                                                                                                                                                                                         |

### Responses

/v1.47/configs/{id}/update

### Request samples

* Payload

Content type

application/json

`{
"Name": "string",
"Labels": {
"property1": "string",
"property2": "string"
},
"Data": "string",
"Templating": {
"Name": "some-driver",
"Options": {
"OptionA": "value for driver-specific option A",
"OptionB": "value for driver-specific option B"
}
}
}`

### Response samples

* 400
* 404
* 500
* 503

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin)Plugins

## [](#tag/Plugin/operation/PluginList)List plugins

Returns information about installed plugins.

##### query Parameters

|         |                                                                                                                                                                                 |
| ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| filters | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the plugin list.Available filters:- `capability=<capability name>`
- `enable=<true>\|<false>` |

### Responses

/v1.47/plugins

### Response samples

* 200
* 500

Content type

application/json

`[
{
"Id": "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078",
"Name": "tiborvass/sample-volume-plugin",
"Enabled": true,
"Settings": {
"Mounts": [
{
"Name": "some-mount",
"Description": "This is a mount that's used by the plugin.",
"Settable": [
"string"
],
"Source": "/var/lib/docker/plugins/",
"Destination": "/mnt/state",
"Type": "bind",
"Options": [
"rbind",
"rw"
]
}
],
"Env": [
"DEBUG=0"
],
"Args": [
"string"
],
"Devices": [
{
"Name": "string",
"Description": "string",
"Settable": [
"string"
],
"Path": "/dev/fuse"
}
]
},
"PluginReference": "localhost:5000/tiborvass/sample-volume-plugin:latest",
"Config": {
"DockerVersion": "17.06.0-ce",
"Description": "A sample volume plugin for Docker",
"Documentation": "https://docs.docker.com/engine/extend/plugins/",
"Interface": {
"Types": [
"docker.volumedriver/1.0"
],
"Socket": "plugins.sock",
"ProtocolScheme": "some.protocol/v1.0"
},
"Entrypoint": [
"/usr/bin/sample-volume-plugin",
"/data"
],
"WorkDir": "/bin/",
"User": {
"UID": 1000,
"GID": 1000
},
"Network": {
"Type": "host"
},
"Linux": {
"Capabilities": [
"CAP_SYS_ADMIN",
"CAP_SYSLOG"
],
"AllowAllDevices": false,
"Devices": [
{
"Name": "string",
"Description": "string",
"Settable": [
"string"
],
"Path": "/dev/fuse"
}
]
},
"PropagatedMount": "/mnt/volumes",
"IpcHost": false,
"PidHost": false,
"Mounts": [
{
"Name": "some-mount",
"Description": "This is a mount that's used by the plugin.",
"Settable": [
"string"
],
"Source": "/var/lib/docker/plugins/",
"Destination": "/mnt/state",
"Type": "bind",
"Options": [
"rbind",
"rw"
]
}
],
"Env": [
{
"Name": "DEBUG",
"Description": "If set, prints debug messages",
"Settable": null,
"Value": "0"
}
],
"Args": {
"Name": "args",
"Description": "command line arguments",
"Settable": [
"string"
],
"Value": [
"string"
]
},
"rootfs": {
"type": "layers",
"diff_ids": [
"sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887",
"sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"
]
}
}
}
]`

## [](#tag/Plugin/operation/GetPluginPrivileges)Get plugin privileges

##### query Parameters

|                |                                                                                             |
| -------------- | ------------------------------------------------------------------------------------------- |
| remoterequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

### Responses

/v1.47/plugins/privileges

### Response samples

* 200
* 500

Content type

application/json

`[
{
"Name": "network",
"Description": "",
"Value": [
"host"
]
},
{
"Name": "mount",
"Description": "",
"Value": [
"/data"
]
},
{
"Name": "device",
"Description": "",
"Value": [
"/dev/cpu_dma_latency"
]
}
]`

## [](#tag/Plugin/operation/PluginPull)Install a plugin

Pulls and installs a plugin. After the plugin is installed, it can be enabled using the [`POST /plugins/{name}/enable` endpoint](#operation/PostPluginsEnable).

##### query Parameters

|                |                                                                                                                    |
| -------------- | ------------------------------------------------------------------------------------------------------------------ |
| remoterequired | stringRemote reference for plugin to install.The `:latest` tag is optional, and is used as the default if omitted. |
| name           | stringLocal name for the pulled plugin.The `:latest` tag is optional, and is used as the default if omitted.       |

##### header Parameters

|                 |                                                                                                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-Registry-Auth | stringA base64url-encoded auth configuration to use when pulling a plugin from a registry.Refer to the [authentication section](#section/Authentication) for details. |

##### Request Body schema:application/json

Array

|             |                  |
| ----------- | ---------------- |
| Name        | string           |
| Description | string           |
| Value       | Array of strings |

### Responses

/v1.47/plugins/pull

### Request samples

* Payload

Content type

application/json

`[
{
"Name": "network",
"Description": "",
"Value": [
"host"
]
},
{
"Name": "mount",
"Description": "",
"Value": [
"/data"
]
},
{
"Name": "device",
"Description": "",
"Value": [
"/dev/cpu_dma_latency"
]
}
]`

### Response samples

* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin/operation/PluginInspect)Inspect a plugin

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

### Responses

/v1.47/plugins/{name}/json

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Id": "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078",
"Name": "tiborvass/sample-volume-plugin",
"Enabled": true,
"Settings": {
"Mounts": [
{
"Name": "some-mount",
"Description": "This is a mount that's used by the plugin.",
"Settable": [
"string"
],
"Source": "/var/lib/docker/plugins/",
"Destination": "/mnt/state",
"Type": "bind",
"Options": [
"rbind",
"rw"
]
}
],
"Env": [
"DEBUG=0"
],
"Args": [
"string"
],
"Devices": [
{
"Name": "string",
"Description": "string",
"Settable": [
"string"
],
"Path": "/dev/fuse"
}
]
},
"PluginReference": "localhost:5000/tiborvass/sample-volume-plugin:latest",
"Config": {
"DockerVersion": "17.06.0-ce",
"Description": "A sample volume plugin for Docker",
"Documentation": "https://docs.docker.com/engine/extend/plugins/",
"Interface": {
"Types": [
"docker.volumedriver/1.0"
],
"Socket": "plugins.sock",
"ProtocolScheme": "some.protocol/v1.0"
},
"Entrypoint": [
"/usr/bin/sample-volume-plugin",
"/data"
],
"WorkDir": "/bin/",
"User": {
"UID": 1000,
"GID": 1000
},
"Network": {
"Type": "host"
},
"Linux": {
"Capabilities": [
"CAP_SYS_ADMIN",
"CAP_SYSLOG"
],
"AllowAllDevices": false,
"Devices": [
{
"Name": "string",
"Description": "string",
"Settable": [
"string"
],
"Path": "/dev/fuse"
}
]
},
"PropagatedMount": "/mnt/volumes",
"IpcHost": false,
"PidHost": false,
"Mounts": [
{
"Name": "some-mount",
"Description": "This is a mount that's used by the plugin.",
"Settable": [
"string"
],
"Source": "/var/lib/docker/plugins/",
"Destination": "/mnt/state",
"Type": "bind",
"Options": [
"rbind",
"rw"
]
}
],
"Env": [
{
"Name": "DEBUG",
"Description": "If set, prints debug messages",
"Settable": null,
"Value": "0"
}
],
"Args": {
"Name": "args",
"Description": "command line arguments",
"Settable": [
"string"
],
"Value": [
"string"
]
},
"rootfs": {
"type": "layers",
"diff_ids": [
"sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887",
"sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"
]
}
}
}`

## [](#tag/Plugin/operation/PluginDelete)Remove a plugin

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

##### query Parameters

|       |                                                                                                                            |
| ----- | -------------------------------------------------------------------------------------------------------------------------- |
| force | booleanDefault: falseDisable the plugin before removing. This may result in issues if the plugin is in use by a container. |

### Responses

/v1.47/plugins/{name}

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Id": "5724e2c8652da337ab2eedd19fc6fc0ec908e4bd907c7421bf6a8dfc70c4c078",
"Name": "tiborvass/sample-volume-plugin",
"Enabled": true,
"Settings": {
"Mounts": [
{
"Name": "some-mount",
"Description": "This is a mount that's used by the plugin.",
"Settable": [
"string"
],
"Source": "/var/lib/docker/plugins/",
"Destination": "/mnt/state",
"Type": "bind",
"Options": [
"rbind",
"rw"
]
}
],
"Env": [
"DEBUG=0"
],
"Args": [
"string"
],
"Devices": [
{
"Name": "string",
"Description": "string",
"Settable": [
"string"
],
"Path": "/dev/fuse"
}
]
},
"PluginReference": "localhost:5000/tiborvass/sample-volume-plugin:latest",
"Config": {
"DockerVersion": "17.06.0-ce",
"Description": "A sample volume plugin for Docker",
"Documentation": "https://docs.docker.com/engine/extend/plugins/",
"Interface": {
"Types": [
"docker.volumedriver/1.0"
],
"Socket": "plugins.sock",
"ProtocolScheme": "some.protocol/v1.0"
},
"Entrypoint": [
"/usr/bin/sample-volume-plugin",
"/data"
],
"WorkDir": "/bin/",
"User": {
"UID": 1000,
"GID": 1000
},
"Network": {
"Type": "host"
},
"Linux": {
"Capabilities": [
"CAP_SYS_ADMIN",
"CAP_SYSLOG"
],
"AllowAllDevices": false,
"Devices": [
{
"Name": "string",
"Description": "string",
"Settable": [
"string"
],
"Path": "/dev/fuse"
}
]
},
"PropagatedMount": "/mnt/volumes",
"IpcHost": false,
"PidHost": false,
"Mounts": [
{
"Name": "some-mount",
"Description": "This is a mount that's used by the plugin.",
"Settable": [
"string"
],
"Source": "/var/lib/docker/plugins/",
"Destination": "/mnt/state",
"Type": "bind",
"Options": [
"rbind",
"rw"
]
}
],
"Env": [
{
"Name": "DEBUG",
"Description": "If set, prints debug messages",
"Settable": null,
"Value": "0"
}
],
"Args": {
"Name": "args",
"Description": "command line arguments",
"Settable": [
"string"
],
"Value": [
"string"
]
},
"rootfs": {
"type": "layers",
"diff_ids": [
"sha256:675532206fbf3030b8458f88d6e26d4eb1577688a25efec97154c94e8b6b4887",
"sha256:e216a057b1cb1efc11f8a268f37ef62083e70b1b38323ba252e25ac88904a7e8"
]
}
}
}`

## [](#tag/Plugin/operation/PluginEnable)Enable a plugin

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

##### query Parameters

|         |                                                           |
| ------- | --------------------------------------------------------- |
| timeout | integerDefault: 0Set the HTTP client timeout (in seconds) |

### Responses

/v1.47/plugins/{name}/enable

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin/operation/PluginDisable)Disable a plugin

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

##### query Parameters

|       |                                                     |
| ----- | --------------------------------------------------- |
| force | booleanForce disable a plugin even if still in use. |

### Responses

/v1.47/plugins/{name}/disable

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin/operation/PluginUpgrade)Upgrade a plugin

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

##### query Parameters

|                |                                                                                                            |
| -------------- | ---------------------------------------------------------------------------------------------------------- |
| remoterequired | stringRemote reference to upgrade to.The `:latest` tag is optional, and is used as the default if omitted. |

##### header Parameters

|                 |                                                                                                                                                                       |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| X-Registry-Auth | stringA base64url-encoded auth configuration to use when pulling a plugin from a registry.Refer to the [authentication section](#section/Authentication) for details. |

##### Request Body schema:application/json

Array

|             |                  |
| ----------- | ---------------- |
| Name        | string           |
| Description | string           |
| Value       | Array of strings |

### Responses

/v1.47/plugins/{name}/upgrade

### Request samples

* Payload

Content type

application/json

`[
{
"Name": "network",
"Description": "",
"Value": [
"host"
]
},
{
"Name": "mount",
"Description": "",
"Value": [
"/data"
]
},
{
"Name": "device",
"Description": "",
"Value": [
"/dev/cpu_dma_latency"
]
}
]`

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin/operation/PluginCreate)Create a plugin

##### query Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

##### Request Body schema: application/x-tar

Path to tar containing plugin rootfs and manifest

string \<binary>

### Responses

/v1.47/plugins/create

### Response samples

* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin/operation/PluginPush)Push a plugin

Push a plugin to the registry.

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

### Responses

/v1.47/plugins/{name}/push

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/Plugin/operation/PluginSet)Configure a plugin

##### path Parameters

|              |                                                                                             |
| ------------ | ------------------------------------------------------------------------------------------- |
| namerequired | stringThe name of the plugin. The `:latest` tag is optional, and is the default if omitted. |

##### Request Body schema: application/json

Array

string

### Responses

/v1.47/plugins/{name}/set

### Request samples

* Payload

Content type

application/json

`[
"DEBUG=1"
]`

### Response samples

* 404
* 500

Content type

application/json

`{
"message": "Something went wrong."
}`

## [](#tag/System)System

## [](#tag/System/operation/SystemAuth)Check auth configuration

Validate credentials for a registry and, if available, get an identity token for accessing the registry without password.

##### Request Body schema: application/json

Authentication to check

|               |                                                                                                                                                                                 |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| username      | string                                                                                                                                                                          |
| password      | string                                                                                                                                                                          |
| email         | stringEmail is an optional value associated with the username.> **Deprecated**: This field is deprecated since docker 1.11 (API v1.23) and will be removed in a future release. |
| serveraddress | string                                                                                                                                                                          |

### Responses

/v1.47/auth

### Request samples

* Payload

Content type

application/json

`{
"username": "hannibal",
"password": "xxxx",
"serveraddress": "https://index.docker.io/v1/"
}`

### Response samples

* 200
* 401
* 500

Content type

application/json

`{
"Status": "Login Succeeded",
"IdentityToken": "9cbaf023786cd7..."
}`

## [](#tag/System/operation/SystemInfo)Get system information

### Responses

/v1.47/info

### Response samples

* 200
* 500

Content type

application/json

`{
"ID": "7TRN:IPZB:QYBB:VPBQ:UMPP:KARE:6ZNR:XE6T:7EWV:PKF4:ZOJD:TPYS",
"Containers": 14,
"ContainersRunning": 3,
"ContainersPaused": 1,
"ContainersStopped": 10,
"Images": 508,
"Driver": "overlay2",
"DriverStatus": [ [
"Backing Filesystem",
"extfs"
], [
"Supports d_type",
"true"
], [
"Native Overlay Diff",
"true"
]
],
"DockerRootDir": "/var/lib/docker",
"Plugins": {
"Volume": [
"local"
],
"Network": [
"bridge",
"host",
"ipvlan",
"macvlan",
"null",
"overlay"
],
"Authorization": [
"img-authz-plugin",
"hbm"
],
"Log": [
"awslogs",
"fluentd",
"gcplogs",
"gelf",
"journald",
"json-file",
"splunk",
"syslog"
]
},
"MemoryLimit": true,
"SwapLimit": true,
"KernelMemoryTCP": true,
"CpuCfsPeriod": true,
"CpuCfsQuota": true,
"CPUShares": true,
"CPUSet": true,
"PidsLimit": true,
"OomKillDisable": true,
"IPv4Forwarding": true,
"BridgeNfIptables": true,
"BridgeNfIp6tables": true,
"Debug": true,
"NFd": 64,
"NGoroutines": 174,
"SystemTime": "2017-08-08T20:28:29.06202363Z",
"LoggingDriver": "string",
"CgroupDriver": "cgroupfs",
"CgroupVersion": "1",
"NEventsListener": 30,
"KernelVersion": "6.8.0-31-generic",
"OperatingSystem": "Ubuntu 24.04 LTS",
"OSVersion": "24.04",
"OSType": "linux",
"Architecture": "x86_64",
"NCPU": 4,
"MemTotal": 2095882240,
"IndexServerAddress": "https://index.docker.io/v1/",
"RegistryConfig": {
"AllowNondistributableArtifactsCIDRs": [ ],
"AllowNondistributableArtifactsHostnames": [ ],
"InsecureRegistryCIDRs": [
"::1/128",
"127.0.0.0/8"
],
"IndexConfigs": {
"127.0.0.1:5000": {
"Name": "127.0.0.1:5000",
"Mirrors": [ ],
"Secure": false,
"Official": false
},
"[2001:db8:a0b:12f0::1]:80": {
"Name": "[2001:db8:a0b:12f0::1]:80",
"Mirrors": [ ],
"Secure": false,
"Official": false
},
"docker.io": {
"Name": "docker.io",
"Mirrors": [
"https://hub-mirror.corp.example.com:5000/"
],
"Secure": true,
"Official": true
},
"registry.internal.corp.example.com:3000": {
"Name": "registry.internal.corp.example.com:3000",
"Mirrors": [ ],
"Secure": false,
"Official": false
}
},
"Mirrors": [
"https://hub-mirror.corp.example.com:5000/",
"https://[2001:db8:a0b:12f0::1]/"
]
},
"GenericResources": [
{
"DiscreteResourceSpec": {
"Kind": "SSD",
"Value": 3
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID1"
}
},
{
"NamedResourceSpec": {
"Kind": "GPU",
"Value": "UUID2"
}
}
],
"HttpProxy": "http://xxxxx:xxxxx@proxy.corp.example.com:8080",
"HttpsProxy": "https://xxxxx:xxxxx@proxy.corp.example.com:4443",
"NoProxy": "*.local, 169.254/16",
"Name": "node5.corp.example.com",
"Labels": [
"storage=ssd",
"production"
],
"ExperimentalBuild": true,
"ServerVersion": "27.0.1",
"Runtimes": {
"runc": {
"path": "runc"
},
"runc-master": {
"path": "/go/bin/runc"
},
"custom": {
"path": "/usr/local/bin/my-oci-runtime",
"runtimeArgs": [
"--debug",
"--systemd-cgroup=false"
]
}
},
"DefaultRuntime": "runc",
"Swarm": {
"NodeID": "k67qz4598weg5unwwffg6z1m1",
"NodeAddr": "10.0.0.46",
"LocalNodeState": "active",
"ControlAvailable": true,
"Error": "",
"RemoteManagers": [
{
"NodeID": "71izy0goik036k48jg985xnds",
"Addr": "10.0.0.158:2377"
},
{
"NodeID": "79y6h1o4gv8n120drcprv5nmc",
"Addr": "10.0.0.159:2377"
},
{
"NodeID": "k67qz4598weg5unwwffg6z1m1",
"Addr": "10.0.0.46:2377"
}
],
"Nodes": 4,
"Managers": 3,
"Cluster": {
"ID": "abajmipo7b4xz5ip2nrla6b11",
"Version": {
"Index": 373531
},
"CreatedAt": "2016-08-18T10:44:24.496525531Z",
"UpdatedAt": "2017-08-09T07:09:37.632105588Z",
"Spec": {
"Name": "default",
"Labels": {
"com.example.corp.type": "production",
"com.example.corp.department": "engineering"
},
"Orchestration": {
"TaskHistoryRetentionLimit": 10
},
"Raft": {
"SnapshotInterval": 10000,
"KeepOldSnapshots": 0,
"LogEntriesForSlowFollowers": 500,
"ElectionTick": 3,
"HeartbeatTick": 1
},
"Dispatcher": {
"HeartbeatPeriod": 5000000000
},
"CAConfig": {
"NodeCertExpiry": 7776000000000000,
"ExternalCAs": [
{
"Protocol": "cfssl",
"URL": "string",
"Options": {
"property1": "string",
"property2": "string"
},
"CACert": "string"
}
],
"SigningCACert": "string",
"SigningCAKey": "string",
"ForceRotate": 0
},
"EncryptionConfig": {
"AutoLockManagers": false
},
"TaskDefaults": {
"LogDriver": {
"Name": "json-file",
"Options": {
"max-file": "10",
"max-size": "100m"
}
}
}
},
"TLSInfo": {
"TrustRoot": "-----BEGIN CERTIFICATE-----\nMIIBajCCARCgAwIBAgIUbYqrLSOSQHoxD8CwG6Bi2PJi9c8wCgYIKoZIzj0EAwIw\nEzERMA8GA1UEAxMIc3dhcm0tY2EwHhcNMTcwNDI0MjE0MzAwWhcNMzcwNDE5MjE0\nMzAwWjATMREwDwYDVQQDEwhzd2FybS1jYTBZMBMGByqGSM49AgEGCCqGSM49AwEH\nA0IABJk/VyMPYdaqDXJb/VXh5n/1Yuv7iNrxV3Qb3l06XD46seovcDWs3IZNV1lf\n3Skyr0ofcchipoiHkXBODojJydSjQjBAMA4GA1UdDwEB/wQEAwIBBjAPBgNVHRMB\nAf8EBTADAQH/MB0GA1UdDgQWBBRUXxuRcnFjDfR/RIAUQab8ZV/n4jAKBggqhkjO\nPQQDAgNIADBFAiAy+JTe6Uc3KyLCMiqGl2GyWGQqQDEcO3/YG36x7om65AIhAJvz\npxv6zFeVEkAEEkqIYi0omA9+CjanB/6Bz4n1uw8H\n-----END CERTIFICATE-----\n",
"CertIssuerSubject": "MBMxETAPBgNVBAMTCHN3YXJtLWNh",
"CertIssuerPublicKey": "MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEmT9XIw9h1qoNclv9VeHmf/Vi6/uI2vFXdBveXTpcPjqx6i9wNazchk1XWV/dKTKvSh9xyGKmiIeRcE4OiMnJ1A=="
},
"RootRotationInProgress": false,
"DataPathPort": 4789,
"DefaultAddrPool": [ [
"10.10.0.0/16",
"20.20.0.0/16"
]
],
"SubnetSize": 24
}
},
"LiveRestoreEnabled": false,
"Isolation": "default",
"InitBinary": "docker-init",
"ContainerdCommit": {
"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a",
"Expected": "2d41c047c83e09a6d61d464906feb2a2f3c52aa4"
},
"RuncCommit": {
"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a",
"Expected": "2d41c047c83e09a6d61d464906feb2a2f3c52aa4"
},
"InitCommit": {
"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a",
"Expected": "2d41c047c83e09a6d61d464906feb2a2f3c52aa4"
},
"SecurityOptions": [
"name=apparmor",
"name=seccomp,profile=default",
"name=selinux",
"name=userns",
"name=rootless"
],
"ProductLicense": "Community Engine",
"DefaultAddressPools": [
{
"Base": "10.10.0.0/16",
"Size": "24"
}
],
"Warnings": [
"WARNING: No memory limit support"
],
"CDISpecDirs": [
"/etc/cdi",
"/var/run/cdi"
],
"Containerd": {
"Address": "/run/containerd/containerd.sock",
"Namespaces": {
"Containers": "moby",
"Plugins": "plugins.moby"
}
}
}`

## [](#tag/System/operation/SystemVersion)Get version

Returns the version of Docker that is running and various information about the system that Docker is running on.

### Responses

/v1.47/version

### Response samples

* 200
* 500

Content type

application/json

`{
"Platform": {
"Name": "string"
},
"Components": [
{
"Name": "Engine",
"Version": "27.0.1",
"Details": { }
}
],
"Version": "27.0.1",
"ApiVersion": "1.47",
"MinAPIVersion": "1.24",
"GitCommit": "48a66213fe",
"GoVersion": "go1.21.13",
"Os": "linux",
"Arch": "amd64",
"KernelVersion": "6.8.0-31-generic",
"Experimental": true,
"BuildTime": "2020-06-22T15:49:27.000000000+00:00"
}`

## [](#tag/System/operation/SystemPing)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.47/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.47/\_ping

## [](#tag/System/operation/SystemEvents)Monitor events

Stream real-time events from the server.

Various objects within Docker report events when something happens to them.

Containers report these events: `attach`, `commit`, `copy`, `create`, `destroy`, `detach`, `die`, `exec_create`, `exec_detach`, `exec_start`, `exec_die`, `export`, `health_status`, `kill`, `oom`, `pause`, `rename`, `resize`, `restart`, `start`, `stop`, `top`, `unpause`, `update`, and `prune`

Images report these events: `create`, `delete`, `import`, `load`, `pull`, `push`, `save`, `tag`, `untag`, and `prune`

Volumes report these events: `create`, `mount`, `unmount`, `destroy`, and `prune`

Networks report these events: `create`, `connect`, `disconnect`, `destroy`, `update`, `remove`, and `prune`

The Docker daemon reports these events: `reload`

Services report these events: `create`, `update`, and `remove`

Nodes report these events: `create`, `update`, and `remove`

Secrets report these events: `create`, `update`, and `remove`

Configs report these events: `create`, `update`, and `remove`

The Builder reports `prune` events

##### query Parameters

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| since   | stringShow events created since this timestamp then stream new events.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| until   | stringShow events created until this timestamp then stop streaming.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| filters | stringA JSON encoded value of filters (a `map[string][]string`) to process on the event list. Available filters:- `config=<string>` config name or ID
- `container=<string>` container name or ID
- `daemon=<string>` daemon name or ID
- `event=<string>` event type
- `image=<string>` image name or ID
- `label=<string>` image or container label
- `network=<string>` network name or ID
- `node=<string>` node ID
- `plugin`= plugin name or ID
- `scope`= local or swarm
- `secret=<string>` secret name or ID
- `service=<string>` service name or ID
- `type=<string>` object to filter by, one of `container`, `image`, `volume`, `network`, `daemon`, `plugin`, `node`, `service`, `secret` or `config`
- `volume=<string>` volume name |

### Responses

/v1.47/events

### Response samples

* 200
* 400
* 500

Content type

application/json

`{
"Type": "container",
"Action": "create",
"Actor": {
"ID": "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743",
"Attributes": {
"com.example.some-label": "some-label-value",
"image": "alpine:latest",
"name": "my-container"
}
},
"scope": "local",
"time": 1629574695,
"timeNano": 1629574695515050000
}`

## [](#tag/System/operation/SystemDataUsage)Get data usage information

##### query Parameters

|      |                                                                                                                           |
| ---- | ------------------------------------------------------------------------------------------------------------------------- |
| type | Array of stringsItems Enum: "container" "image" "volume" "build-cache"Object types, for which to compute and return data. |

### Responses

/v1.47/system/df

### Response samples

* 200
* 500

Content type

application/json

`{
"LayersSize": 1092588,
"Images": [
{
"Id": "sha256:2b8fd9751c4c0f5dd266fcae00707e67a2545ef34f9a29354585f93dac906749",
"ParentId": "",
"RepoTags": [
"busybox:latest"
],
"RepoDigests": [
"busybox@sha256:a59906e33509d14c036c8678d687bd4eec81ed7c4b8ce907b888c607f6a1e0e6"
],
"Created": 1466724217,
"Size": 1092588,
"SharedSize": 0,
"Labels": { },
"Containers": 1
}
],
"Containers": [
{
"Id": "e575172ed11dc01bfce087fb27bee502db149e1a0fad7c296ad300bbff178148",
"Names": [
"/top"
],
"Image": "busybox",
"ImageID": "sha256:2b8fd9751c4c0f5dd266fcae00707e67a2545ef34f9a29354585f93dac906749",
"Command": "top",
"Created": 1472592424,
"Ports": [ ],
"SizeRootFs": 1092588,
"Labels": { },
"State": "exited",
"Status": "Exited (0) 56 minutes ago",
"HostConfig": {
"NetworkMode": "default"
},
"NetworkSettings": {
"Networks": {
"bridge": {
"IPAMConfig": null,
"Links": null,
"Aliases": null,
"NetworkID": "d687bc59335f0e5c9ee8193e5612e8aee000c8c62ea170cfb99c098f95899d92",
"EndpointID": "8ed5115aeaad9abb174f68dcf135b49f11daf597678315231a32ca28441dec6a",
"Gateway": "172.18.0.1",
"IPAddress": "172.18.0.2",
"IPPrefixLen": 16,
"IPv6Gateway": "",
"GlobalIPv6Address": "",
"GlobalIPv6PrefixLen": 0,
"MacAddress": "02:42:ac:12:00:02"
}
}
},
"Mounts": [ ]
}
],
"Volumes": [
{
"Name": "my-volume",
"Driver": "local",
"Mountpoint": "/var/lib/docker/volumes/my-volume/_data",
"Labels": null,
"Scope": "local",
"Options": null,
"UsageData": {
"Size": 10920104,
"RefCount": 2
}
}
],
"BuildCache": [
{
"ID": "hw53o5aio51xtltp5xjp8v7fx",
"Parents": [ ],
"Type": "regular",
"Description": "pulled from docker.io/library/debian@sha256:234cb88d3020898631af0ccbbcca9a66ae7306ecd30c9720690858c1b007d2a0",
"InUse": false,
"Shared": true,
"Size": 0,
"CreatedAt": "2021-06-28T13:31:01.474619385Z",
"LastUsedAt": "2021-07-07T22:02:32.738075951Z",
"UsageCount": 26
},
{
"ID": "ndlpt0hhvkqcdfkputsk4cq9c",
"Parents": [
"ndlpt0hhvkqcdfkputsk4cq9c"
],
"Type": "regular",
"Description": "mount / from exec /bin/sh -c echo 'Binary::apt::APT::Keep-Downloaded-Packages \"true\";' > /etc/apt/apt.conf.d/keep-cache",
"InUse": false,
"Shared": true,
"Size": 51,
"CreatedAt": "2021-06-28T13:31:03.002625487Z",
"LastUsedAt": "2021-07-07T22:02:32.773909517Z",
"UsageCount": 26
}
]
}`

## [](#tag/Distribution)Distribution

## [](#tag/Distribution/operation/DistributionInspect)Get image information from the registry

Return image digest and platform information by contacting the registry.

##### path Parameters

|              |                        |
| ------------ | ---------------------- |
| namerequired | stringImage name or id |

### Responses

/v1.47/distribution/{name}/json

### Response samples

* 200
* 401
* 500

Content type

application/json

`{
"Descriptor": {
"mediaType": "application/vnd.docker.distribution.manifest.v2+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 3987495
},
"Platforms": [
{
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
}
]
}`

## [](#tag/Session)Session

## [](#tag/Session/operation/Session)Initialize interactive session

Start a new interactive session with a server. Session allows server to call back to the client for advanced capabilities.

### Hijacking

This endpoint hijacks the HTTP connection to HTTP2 transport that allows the client to expose gPRC services on that connection.

For example, the client sends this request to upgrade the connection:

```
POST /session HTTP/1.1
Upgrade: h2c
Connection: Upgrade
```

The Docker daemon responds with a `101 UPGRADED` response follow with the raw stream:

```
HTTP/1.1 101 UPGRADED
Connection: Upgrade
Upgrade: h2c
```

### Responses

/v1.47/session

----
url: https://docs.docker.com/reference/cli/docker/context/use/
----

# docker context use

***

| Description | Set the default docker context |
| ----------- | ------------------------------ |
| Usage       | `docker context use CONTEXT`   |

## [Description](#description)

The `docker context use` command sets the default context for the Docker CLI.

The `docker context use` command sets the Docker CLI’s default context by updating your CLI config (`~/.docker/config.json`). This change is persistent, affecting all shells and sessions that share that config, not just the current terminal.

For one-off commands or per-shell usage, use `--context` or the `DOCKER_CONTEXT` environment variable instead.

## [Examples](#examples)

### [Set the default (sticky) context](#set-the-default-sticky-context)

This updates the CLI configuration and applies to new terminal sessions:

```bash
$ docker context use my-context
my-context

$ docker context show
my-context
```

### [Use a context for a single command](#use-a-context-for-a-single-command)

Use the global `--context` flag to avoid changing the default:

```bash
$ docker --context my-context ps
```

### [Use a context for the current shell session](#use-a-context-for-the-current-shell-session)

Set `DOCKER_CONTEXT` to override the configured default in the current shell:

```bash
$ export DOCKER_CONTEXT=my-context
$ docker context show
my-context
```

To stop overriding:

```bash
$ unset DOCKER_CONTEXT
```

### [Switch back to the default context](#switch-back-to-the-default-context)

```bash
$ docker context use default
default
```

----
url: https://docs.docker.com/reference/api/engine/version-history/
----

# Engine API version history

***

Table of contents

***

## [v1.54 API changes](#v154-api-changes)

* `GET /images/json` now supports an `identity` query parameter. When set, the response includes manifest summaries and may include an `Identity` field for each manifest with trusted identity and origin information.
* `POST /networks/{id}/connect` now correctly applies the `MacAddress` field in `EndpointSettings`. This field was added in API v1.44, but was previously ignored.

## [v1.53 API changes](#v153-api-changes)

* `GET /info` now includes an `NRI` field. If the Node Resource Interface (NRI) is enabled, this field contains information describing it.
* `GET /events` now also supports [`application/jsonl`](https://jsonlines.org/) when negotiating content-type.
* `GET /images/{name}/json` now includes an `Identity` field with trusted identity and origin information for the image.
* Deprecated: The `POST /grpc` and `POST /session` endpoints are deprecated and will be removed in a future version.

## [v1.52 API changes](#v152-api-changes)

* `GET /images/{name}/get` now accepts multiple `platform` query-arguments to allow selecting which platform(s) of a multi-platform image must be saved.
* `POST /images/load` now accepts multiple `platform` query-arguments to allow selecting which platform(s) of a multi-platform image to load.
* `GET /events` no longer includes the deprecated `status`, `id`, and `from` fields. These fields were removed in API v1.22, but still included in the response.
* `GET /networks/{id}` now includes a `Status` field, providing statistics about IPAM allocations for the subnets assigned to the network.
* Deprecated: the Engine was automatically backfilling empty `PortBindings` lists with a PortBinding with an empty HostIP and HostPort when calling `POST /containers/{id}/start`. This behavior is now deprecated, and a warning is returned by `POST /containers/create`. A future API version will drop empty `PortBindings` list altogether.
* `GET /images/{name}/json` now omits the following `Config` fields when not set, to closer align with the implementation of the [OCI Image Specification](https://github.com/opencontainers/image-spec/blob/v1.1.1/specs-go/v1/config.go#L23-L62) `Cmd`, `Entrypoint`, `Env`, `Labels`, `OnBuild`, `User`, `Volumes`, and `WorkingDir`.
* `GET /images/{name}/json` now omits the following fields if their value is empty: `Parent`, `Comment`, `DockerVersion`, `Author`. The `Parent` and `DockerVersion` fields were set by the legacy builder, and are no longer set when using BuildKit. The `Author` field is set through the `MAINTAINER` Dockerfile instruction, which is deprecated, and the `Comment` field is option, and may not be set depending on how the image was created.
* `GET /container/{id}/json` now omits `Config.OnBuild` if its value is empty.
* `GET /containers/{id}/json`: the `NetworkSettings` no longer returns the deprecated `Bridge`, `HairpinMode`, `LinkLocalIPv6Address`, `LinkLocalIPv6PrefixLen`, `SecondaryIPAddresses`, `SecondaryIPv6Addresses`, `EndpointID`, `Gateway`, `GlobalIPv6Address`, `GlobalIPv6PrefixLen`, `IPAddress`, `IPPrefixLen`, `IPv6Gateway`, and `MacAddress` fields. These fields were deprecated in API v1.21 (docker v1.9.0) but kept around for backward compatibility.
* Removed the `KernelMemoryTCP` field from the `POST /containers/{id}/update` and `GET /containers/{id}/json` endpoints, any value it is set to will be ignored on API version `v1.52` and up. Older API versions still accept this field, but may take no effect, depending on the kernel version and OCI runtime in use.
* Removed the `KernelMemoryTCP` field from the `GET /info` endpoint.
* `GET /events` supports content-type negotiation and can produce either `application/x-ndjson` (Newline delimited JSON object stream) or `application/json-seq` (RFC7464).
* `POST /containers/create` no longer supports configuring a container-wide MAC address via the container's `Config.MacAddress` field. A container's MAC address can now only be configured via endpoint settings when connecting to a network.
* `GET /services` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements.
* `GET /services/{id}` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements.
* `POST /services/create` now accepts `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements.
* `POST /services/{id}/update` now accepts `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements.
* `GET /tasks` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements.
* `GET /tasks/{id}` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements.
* `GET /containers/{id}/stats` now returns an `os_type` field to allow platform- specific handling of the stats.
* `GET /system/df` returns `ImagesUsage`, `ContainersUsage`, `VolumesUsage`, and `BuildCacheUsage` fields with brief system disk usage data for each system object type. The endpoint supports the `?verbose=1` query to return verbose system disk usage information.
* Deprecated: `GET /system/df` response fields `LayersSize`, `Images`, `Containers`, `Volumes`, and `BuildCache` have been removed in favor of the-type specific usage fields. API v1.52 returns both the legacy and current fields to help existing integrations to transition to the new response. The legacy fields are not populated if the `verbose` query parameter is used. Starting with API v1.53, the legacy fields will no longer be returned.

## [v1.51 API changes](#v151-api-changes)

* `GET /images/json` now sets the value of `Containers` field for all images to the count of containers using the image. This field was previously always -1.
* Deprecated: The field `NetworkSettings.Bridge` returned by `GET /containers/{id}/json` is deprecated and will be removed in the next API version.
* Deprecated: The field `KernelMemoryTCP` as part of `POST /containers/{id}/update` and returned by `GET /containers/{id}/json` is deprecated and will be removed in the next API version.
* Deprecated: The field `KernelMemoryTCP` as part of `GET /info` is deprecated and will be removed in the next API version.
* Deprecated: the `Parent` and `DockerVersion` fields returned by the `GET /images/{name}/json` endpoint are deprecated. These fields are set by the legacy builder, and are no longer set when using BuildKit. The API continues returning these fields when set for informational purposes, but they should not be depended on as they will be omitted once the legacy builder is removed.
* Deprecated: the `Config.DockerVersion` field returned by the `GET /plugins` and `GET /images/{name}/json` endpoints is deprecated. The field is no longer set, and is omitted when empty.

## [v1.50 API changes](#v150-api-changes)

* `GET /info` now includes a `DiscoveredDevices` field. This is an array of `DeviceInfo` objects, each providing details about a device discovered by a device driver. Currently only the CDI device driver is supported.
* `DELETE /images/{name}` now supports a `platforms` query parameter. It accepts an array of JSON-encoded OCI Platform objects, allowing for selecting specific platforms to delete content for.
* Deprecated: The `BridgeNfIptables` and `BridgeNfIp6tables` fields in the `GET /info` response were deprecated in API v1.48, and are now omitted in API v1.50.
* Deprecated: `GET /images/{name}/json` no longer returns the following `Config` fields; `Hostname`, `Domainname`, `AttachStdin`, `AttachStdout`, `AttachStderr` `Tty`, `OpenStdin`, `StdinOnce`, `Image`, `NetworkDisabled` (already omitted unless set), `MacAddress` (already omitted unless set), `StopTimeout` (already omitted unless set). These additional fields were included in the response due to an implementation detail but not part of the image's Configuration. These fields were marked deprecated in API v1.46, and are now omitted. Older versions of the API still return these fields, but they are always empty.

## [v1.49 API changes](#v149-api-changes)

* `GET /images/{name}/json` now supports a `platform` parameter (JSON encoded OCI Platform type) allowing to specify a platform of the multi-platform image to inspect. This option is mutually exclusive with the `manifests` option.
* `GET /info` now returns a `FirewallBackend` containing information about the daemon's firewalling configuration.
* Deprecated: The `AllowNondistributableArtifactsCIDRs` and `AllowNondistributableArtifactsHostnames` fields in the `RegistryConfig` struct in the `GET /info` response are omitted in API v1.49.
* Deprecated: The `ContainerdCommit.Expected`, `RuncCommit.Expected`, and `InitCommit.Expected` fields in the `GET /info` endpoint were deprecated in API v1.48, and are now omitted in API v1.49.

## [v1.48 API changes](#v148-api-changes)

* Deprecated: The "error" and "progress" fields in streaming responses for endpoints that return a JSON progress response, such as `POST /images/create`, `POST /images/{name}/push`, and `POST /build` are deprecated. These fields were marked deprecated in API v1.4 (docker v0.6.0) and API v1.8 (docker v0.7.1) respectively, but still returned. These fields will be left empty or will be omitted in a future API version. Users should use the information in the `errorDetail` and `progressDetail` fields instead.
* Deprecated: The "allow-nondistributable-artifacts" daemon configuration is deprecated and enabled by default. The `AllowNondistributableArtifactsCIDRs` and `AllowNondistributableArtifactsHostnames` fields in the `RegistryConfig` struct in the `GET /info` response will now always be `null` and will be omitted in API v1.49.
* Deprecated: The `BridgeNfIptables` and `BridgeNfIp6tables` fields in the `GET /info` response are now always be `false` and will be omitted in API v1.49. The netfilter module is now loaded on-demand, and no longer during daemon startup, making these fields obsolete.
* Deprecated: The `POST /build/prune` `keep-storage` query parameter has been renamed to `reserved-space`. `keep-storage` support will be removed in API v1.52.
* `GET /images/{name}/history` now supports a `platform` parameter (JSON encoded OCI Platform type) that allows to specify a platform to show the history of.
* `POST /images/{name}/load` and `GET /images/{name}/get` now support a `platform` parameter (JSON encoded OCI Platform type) that allows to specify a platform to load/save. Not passing this parameter will result in loading/saving the full multi-platform image.
* `POST /containers/create` now includes a warning in the response when setting the container-wide `Config.VolumeDriver` option in combination with volumes defined through `Mounts` because the `VolumeDriver` option has no effect on those volumes. This warning was previously generated by the CLI, but now moved to the daemon so that other clients can also get this warning.
* `POST /containers/create` now supports `Mount` of type `image` for mounting an image inside a container.
* Deprecated: The `ContainerdCommit.Expected`, `RuncCommit.Expected`, and `InitCommit.Expected` fields in the `GET /info` endpoint are deprecated and will be omitted in API v1.49.
* `Sysctls` in `HostConfig` (top level `--sysctl` settings) for `eth0` are no longer migrated to `DriverOpts`, as described in the changes for v1.46.
* `GET /images/json` and `GET /images/{name}/json` responses now include `Descriptor` field, which contains an OCI descriptor of the image target. The new field will only be populated if the daemon provides a multi-platform image store. WARNING: This is experimental and may change at any time without any backward compatibility.
* `GET /images/{name}/json` response now will return the `Manifests` field containing information about the sub-manifests contained in the image index. This includes things like platform-specific manifests and build attestations. The new field will only be populated if the request also sets the `manifests` query parameter to `true`. This acts the same as in the `GET /images/json` endpoint. WARNING: This is experimental and may change at any time without any backward compatibility.
* `GET /containers/{name}/json` now returns an `ImageManifestDescriptor` field containing the OCI descriptor of the platform-specific image manifest of the image that was used to create the container. This field is only populated if the daemon provides a multi-platform image store.
* `POST /networks/create` now has an `EnableIPv4` field. Setting it to `false` disables IPv4 IPAM for the network. It can only be set to `false` if the daemon has experimental features enabled.
* `GET /networks/{id}` now returns an `EnableIPv4` field showing whether the network has IPv4 IPAM enabled.
* `POST /networks/{id}/connect` and `POST /containers/create` now accept a `GwPriority` field in `EndpointsConfig`. This value is used to determine which network endpoint provides the default gateway for the container. The endpoint with the highest priority is selected. If multiple endpoints have the same priority, endpoints are sorted lexicographically by their network name, and the one that sorts first is picked.
* `GET /containers/json` now returns a `GwPriority` field in `NetworkSettings` for each network endpoint.
* API debug endpoints (`GET /debug/vars`, `GET /debug/pprof/`, `GET /debug/pprof/cmdline`, `GET /debug/pprof/profile`, `GET /debug/pprof/symbol`, `GET /debug/pprof/trace`, `GET /debug/pprof/{name}`) are now also accessible through the versioned-API paths (`/v<API-version>/<endpoint>`).
* `POST /build/prune` renames `keep-storage` to `reserved-space` and now supports additional prune parameters `max-used-space` and `min-free-space`.
* `GET /containers/json` now returns an `ImageManifestDescriptor` field matching the same field in `/containers/{name}/json`. This field is only populated if the daemon provides a multi-platform image store.

## [v1.47 API changes](#v147-api-changes)

* `GET /images/json` response now includes `Manifests` field, which contains information about the sub-manifests included in the image index. This includes things like platform-specific manifests and build attestations. The new field will only be populated if the request also sets the `manifests` query parameter to `true`. WARNING: This is experimental and may change at any time without any backward compatibility.
* `GET /info` no longer includes warnings when `bridge-nf-call-iptables` or `bridge-nf-call-ip6tables` are disabled when the daemon was started. The `br_netfilter` module is now attempted to be loaded when needed, making those warnings inaccurate. This change is not versioned, and affects all API versions if the daemon has this patch.

## [v1.46 API changes](#v146-api-changes)

* `GET /info` now includes a `Containerd` field containing information about the location of the containerd API socket and containerd namespaces used by the daemon to run containers and plugins.
* `POST /containers/create` field `NetworkingConfig.EndpointsConfig.DriverOpts`, and `POST /networks/{id}/connect` field `EndpointsConfig.DriverOpts`, now support label `com.docker.network.endpoint.sysctls` for setting per-interface sysctls. The value is a comma separated list of sysctl assignments, the interface name must be "IFNAME". For example, to set `net.ipv4.config.eth0.log_martians=1`, use `net.ipv4.config.IFNAME.log_martians=1`. In API versions up-to 1.46, top level `--sysctl` settings for `eth0` will be migrated to `DriverOpts` when possible. This automatic migration will be removed in a future release.
* `GET /containers/json` now returns the annotations of containers.
* `POST /images/{name}/push` now supports a `platform` parameter (JSON encoded OCI Platform type) that allows selecting a specific platform manifest from the multi-platform image.
* `POST /containers/create` now takes `Options` as part of `HostConfig.Mounts.TmpfsOptions` to set options for tmpfs mounts.
* `POST /services/create` now takes `Options` as part of `ContainerSpec.Mounts.TmpfsOptions`, to set options for tmpfs mounts.
* `GET /events` now supports image `create` event that is emitted when a new image is built regardless if it was tagged or not.

#### [Deprecated Config fields in `GET /images/{name}/json` response](#deprecated-config-fields-in-get-imagesnamejson-response)

The `Config` field returned by this endpoint (used for "image inspect") returns additional fields that are not part of the image's configuration and not part of the [Docker Image Spec](https://github.com/moby/docker-image-spec/blob/v1.3.1/specs-go/v1/image.go#L19-L32) and the [OCI Image Spec](https://github.com/opencontainers/image-spec/blob/v1.1.0/specs-go/v1/config.go#L24-L62).

These additional fields are included in the response, due to an implementation detail, where the [api/types.ImageInspec](https://github.com/moby/moby/blob/v26.1.4/api/types/types.go#L87-L104) type used for the response is using the [container.Config](https://github.com/moby/moby/blob/v26.1.4/api/types/container/config.go#L47-L82) type.

The [container.Config](https://github.com/moby/moby/blob/v26.1.4/api/types/container/config.go#L47-L82) type is a superset of the image config, and while the image's Config is used as a *template* for containers created from the image, the additional fields are set at runtime (from options passed when creating the container) and not taken from the image Config.

These fields are never set (and always return the default value for the type), but are not omitted in the response when left empty. As these fields were not intended to be part of the image configuration response, they are deprecated, and will be removed from the API.

The following fields are currently included in the API response, but are not part of the underlying image's Config, and deprecated:

- `POST /services/create` and `POST /services/{id}/update` now support OomScoreAdj

## [v1.45 API changes](#v145-api-changes)

* `POST /containers/create` now supports `VolumeOptions.Subpath` which allows a subpath of a named volume to be mounted.
* `POST /images/search` will always assume a `false` value for the `is-automated` field. Consequently, searching for `is-automated=true` will yield no results, while `is-automated=false` will be a no-op.
* `GET /images/{name}/json` no longer includes the `Container` and `ContainerConfig` fields. To access image configuration, use `Config` field instead.
* The `Aliases` field returned in calls to `GET /containers/{name:.*}/json` no longer contains the short container ID, but instead will reflect exactly the values originally submitted to the `POST /containers/create` endpoint. The newly introduced `DNSNames` should now be used instead when short container IDs are needed.

## [v1.44 API changes](#v144-api-changes)

* GET `/images/json` now accepts an `until` filter. This accepts a timestamp and lists all images created before it. The `<timestamp>` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. `10m`, `1h30m`) computed relative to the daemon machine’s time. This change is not versioned, and affects all API versions if the daemon has this patch.
* The `VirtualSize` field in the `GET /images/{name}/json`, `GET /images/json`, and `GET /system/df` responses is now omitted. Use the `Size` field instead, which contains the same information.
* Deprecated: The `is_automated` field in the `GET /images/search` response has been deprecated and will always be set to false in the future because Docker Hub is deprecating the `is_automated` field in its search API. The deprecation is not versioned, and applies to all API versions.
* Deprecated: The `is-automated` filter for the `GET /images/search` endpoint. The `is_automated` field has been deprecated by Docker Hub's search API. Consequently, searching for `is-automated=true` will yield no results. The deprecation is not versioned, and applies to all API versions.
* Read-only bind mounts are now made recursively read-only on kernel >= 5.12 with runtimes which support the feature. `POST /containers/create`, `GET /containers/{id}/json`, and `GET /containers/json` now supports `BindOptions.ReadOnlyNonRecursive` and `BindOptions.ReadOnlyForceRecursive` to customize the behavior.
* `POST /containers/create` now accepts a `HealthConfig.StartInterval` to set the interval for health checks during the start period.
* `GET /info` now includes a `CDISpecDirs` field indicating the configured CDI specifications directories. The use of the applied setting requires the daemon to have experimental enabled, and for non-experimental daemons an empty list is always returned.
* `POST /networks/create` now returns a 400 if the `IPAMConfig` has invalid values. Note that this change is *unversioned* and applied to all API versions on daemon that support version 1.44.
* `POST /networks/create` with a duplicated name now fails systematically. As such, the `CheckDuplicate` field is now deprecated. Note that this change is *unversioned* and applied to all API versions on daemon that support version 1.44.
* `POST /containers/create` now accepts multiple `EndpointSettings` in `NetworkingConfig.EndpointSettings`.
* `POST /containers/create` and `POST /networks/{id}/connect` will now catch validation errors that were previously only returned during `POST /containers/{id}/start`. These endpoints will also return the full set of validation errors they find, instead of returning only the first one. Note that this change is *unversioned* and applies to all API versions.
* `POST /services/create` and `POST /services/{id}/update` now accept `Seccomp` and `AppArmor` fields in the `ContainerSpec.Privileges` object. This allows some configuration of Seccomp and AppArmor in Swarm services.
* A new endpoint-specific `MacAddress` field has been added to `NetworkSettings.EndpointSettings` on `POST /containers/create`, and to `EndpointConfig` on `POST /networks/{id}/connect`. The container-wide `MacAddress` field in `Config`, on `POST /containers/create`, is now deprecated.
* The field `Networks` in the `POST /services/create` and `POST /services/{id}/update` requests is now deprecated. You should instead use the field `TaskTemplate.Networks`.
* The `Container` and `ContainerConfig` fields in the `GET /images/{name}/json` response are deprecated and will no longer be included in API v1.45.
* `GET /info` now includes `status` properties in `Runtimes`.
* A new field named `DNSNames` and containing all non-fully qualified DNS names a container takes on a specific network has been added to `GET /containers/{name:.*}/json`.
* The `Aliases` field returned in calls to `GET /containers/{name:.*}/json` in v1.44 and older versions contains the short container ID. This will change in the next API version, v1.45. Starting with that API version, this specific value will be removed from the `Aliases` field such that this field will reflect exactly the values originally submitted to the `POST /containers/create` endpoint. The newly introduced `DNSNames` should now be used instead.
* The fields `HairpinMode`, `LinkLocalIPv6Address`, `LinkLocalIPv6PrefixLen`, `SecondaryIPAddresses`, `SecondaryIPv6Addresses` available in `NetworkSettings` when calling `GET /containers/{id}/json` are deprecated and will be removed in a future release. You should instead look for the default network in `NetworkSettings.Networks`.
* `GET /images/{id}/json` omits the `Created` field (previously it was `0001-01-01T00:00:00Z`) if the `Created` field is missing from the image config.

## [v1.43 API changes](#v143-api-changes)

* `POST /containers/create` now accepts `Annotations` as part of `HostConfig`. Can be used to attach arbitrary metadata to the container, which will also be passed to the runtime when the container is started.
* `GET /images/json` no longer includes hardcoded `<none>:<none>` and `<none>@<none>` in `RepoTags` and`RepoDigests` for untagged images. In such cases, empty arrays will be produced instead.
* The `VirtualSize` field in the `GET /images/{name}/json`, `GET /images/json`, and `GET /system/df` responses is deprecated and will no longer be included in API v1.44. Use the `Size` field instead, which contains the same information.
* `GET /info` now includes `no-new-privileges` in the `SecurityOptions` string list when this option is enabled globally. This change is not versioned, and affects all API versions if the daemon has this patch.

## [v1.42 API changes](#v142-api-changes)

* Removed the `BuilderSize` field on the `GET /system/df` endpoint. This field was introduced in API 1.31 as part of an experimental feature, and no longer used since API 1.40. Use field `BuildCache` instead to track storage used by the builder component.

* `POST /containers/{id}/stop` and `POST /containers/{id}/restart` now accept a `signal` query parameter, which allows overriding the container's default stop- signal.

* `GET /images/json` now accepts query parameter `shared-size`. When set `true`, images returned will include `SharedSize`, which provides the size on disk shared with other images present on the system.

* `GET /system/df` now accepts query parameter `type`. When set, computes and returns data only for the specified object type. The parameter can be specified multiple times to select several object types. Supported values are: `container`, `image`, `volume`, `build-cache`.

* `GET /system/df` can now be used concurrently. If a request is made while a previous request is still being processed, the request will receive the result of the already running calculation, once completed. Previously, an error (`a disk usage operation is already running`) would be returned in this situation. This change is not versioned, and affects all API versions if the daemon has this patch.

* The `POST /images/create` now supports both the operating system and architecture that is passed through the `platform` query parameter when using the `fromSrc` option to import an image from an archive. Previously, only the operating system was used and the architecture was ignored. If no `platform` option is set, the host's operating system and architecture as used as default. This change is not versioned, and affects all API versions if the daemon has this patch.

* The `POST /containers/{id}/wait` endpoint now returns a `400` status code if an invalid `condition` is provided (on API 1.30 and up).

* Removed the `KernelMemory` field from the `POST /containers/create` and `POST /containers/{id}/update` endpoints, any value it is set to will be ignored on API version `v1.42` and up. Older API versions still accept this field, but may take no effect, depending on the kernel version and OCI runtime in use.

* `GET /containers/{id}/json` now omits the `KernelMemory` and `KernelMemoryTCP` if they are not set.

* `GET /info` now omits the `KernelMemory` and `KernelMemoryTCP` if they are not supported by the host or host's configuration (if cgroups v2 are in use).

* `GET /_ping` and `HEAD /_ping` now return `Builder-Version` by default. This header contains the default builder to use, and is a recommendation as advertised by the daemon. However, it is up to the client to choose which builder to use.

  The default value on Linux is version "2" (BuildKit), but the daemon can be configured to recommend version "1" (classic Builder). Windows does not yet support BuildKit for native Windows images, and uses "1" (classic builder) as a default.

  This change is not versioned, and affects all API versions if the daemon has this patch.

* `GET /_ping` and `HEAD /_ping` now return a `Swarm` header, which allows a client to detect if Swarm is enabled on the daemon, without having to call additional endpoints. This change is not versioned, and affects all API versions if the daemon has this patch. Clients must consider this header "optional", and fall back to using other endpoints to get this information if the header is not present.

  The `Swarm` header can contain one of the following values:

  * "inactive"
  * "pending"
  * "error"
  * "locked"
  * "active/worker"
  * "active/manager"

* `POST /containers/create` for Windows containers now accepts a new syntax in `HostConfig.Resources.Devices.PathOnHost`. As well as the existing `class/<GUID>` syntax, `<IDType>://<ID>` is now recognised. Support for specific `<IDType>` values depends on the underlying implementation and Windows version. This change is not versioned, and affects all API versions if the daemon has this patch.

* `GET /containers/{id}/attach`, `GET /exec/{id}/start`, `GET /containers/{id}/logs` `GET /services/{id}/logs` and `GET /tasks/{id}/logs` now set Content-Type header to `application/vnd.docker.multiplexed-stream` when a multiplexed stdout/stderr stream is sent to client, `application/vnd.docker.raw-stream` otherwise.

* `POST /volumes/create` now accepts a new `ClusterVolumeSpec` to create a cluster volume (CNI). This option can only be used if the daemon is a Swarm manager. The Volume response on creation now also can contain a `ClusterVolume` field with information about the created volume.

* The `BuildCache.Parent` field, as returned by `GET /system/df` is deprecated and is now omitted. API versions before v1.42 continue to include this field.

* `GET /system/df` now includes a new `Parents` field, for "build-cache" records, which contains a list of parent IDs for the build-cache record.

* Volume information returned by `GET /volumes/{name}`, `GET /volumes` and `GET /system/df` can now contain a `ClusterVolume` if the volume is a cluster volume (requires the daemon to be a Swarm manager).

* The `Volume` type, as returned by `Added new `ClusterVolume\` fields

* Added a new `PUT /volumes{name}` endpoint to update cluster volumes (CNI). Cluster volumes are only supported if the daemon is a Swarm manager.

* `GET /containers/{name}/attach/ws` endpoint now accepts `stdin`, `stdout` and `stderr` query parameters to only attach to configured streams.

  NOTE: These parameters were documented before in older API versions, but not actually supported. API versions before v1.42 continue to ignore these parameters and default to attaching to all streams. To preserve the pre-v1.42 behavior, set all three query parameters (`?stdin=1,stdout=1,stderr=1`).

* `POST /containers/create` on Linux now respects the `HostConfig.ConsoleSize` property. Container is immediately created with the desired terminal size and clients no longer need to set the desired size on their own.

* `POST /containers/create` allow to set `CreateMountpoint` for host path to be created if missing. This brings parity with `Binds`

* `POST /containers/create` rejects request if BindOptions|VolumeOptions|TmpfsOptions is set with a non-matching mount Type.

* `POST /containers/{id}/exec` now accepts an optional `ConsoleSize` parameter. It allows to set the console size of the executed process immediately when it's created.

* `POST /volumes/prune` will now only prune "anonymous" volumes (volumes which were not given a name) by default. A new filter parameter `all` can be set to a truth-y value (`true`, `1`) to get the old behavior.

## [v1.41 API changes](#v141-api-changes)

* `GET /events` now returns `prune` events after pruning resources have completed. Prune events are returned for `container`, `network`, `volume`, `image`, and `builder`, and have a `reclaimed` attribute, indicating the amount of space reclaimed (in bytes).

* `GET /info` now returns a `CgroupVersion` field, containing the cgroup version.

* `GET /info` now returns a `DefaultAddressPools` field, containing a list of custom default address pools for local networks, which can be specified in the `daemon.json` file or `--default-address-pool` dockerd option.

* `POST /services/create` and `POST /services/{id}/update` now supports `BindOptions.NonRecursive`.

* The `ClusterStore` and `ClusterAdvertise` fields in `GET /info` are deprecated and are now omitted if they contain an empty value. This change is not versioned, and affects all API versions if the daemon has this patch.

* The `filter` (singular) query parameter, which was deprecated in favor of the `filters` option in Docker 1.13, has now been removed from the `GET /images/json` endpoint. The parameter remains available when using API version 1.40 or below.

* `GET /services` now returns `CapAdd` and `CapDrop` as part of the `ContainerSpec`.

* `GET /services/{id}` now returns `CapAdd` and `CapDrop` as part of the `ContainerSpec`.

* `POST /services/create` now accepts `CapAdd` and `CapDrop` as part of the `ContainerSpec`.

* `POST /services/{id}/update` now accepts `CapAdd` and `CapDrop` as part of the `ContainerSpec`.

* `GET /tasks` now returns `CapAdd` and `CapDrop` as part of the `ContainerSpec`.

* `GET /tasks/{id}` now returns `CapAdd` and `CapDrop` as part of the `ContainerSpec`.

* `GET /services` now returns `Pids` in `TaskTemplate.Resources.Limits`.

* `GET /services/{id}` now returns `Pids` in `TaskTemplate.Resources.Limits`.

* `POST /services/create` now accepts `Pids` in `TaskTemplate.Resources.Limits`.

* `POST /services/{id}/update` now accepts `Pids` in `TaskTemplate.Resources.Limits` to limit the maximum number of PIDs.

* `GET /tasks` now returns `Pids` in `TaskTemplate.Resources.Limits`.

* `GET /tasks/{id}` now returns `Pids` in `TaskTemplate.Resources.Limits`.

* `POST /containers/create` now accepts a `platform` query parameter in the format `os[/arch[/variant]]`.

  When set, the daemon checks if the requested image is present in the local image cache with the given OS and Architecture, and otherwise returns a `404` status.

  If the option is *not* set, the host's native OS and Architecture are used to look up the image in the image cache. However, if no platform is passed and the given image *does* exist in the local image cache, but its OS or architecture do not match, the container is created with the available image, and a warning is added to the `Warnings` field in the response, for example;

  ```
  WARNING: The requested image's platform (linux/arm64/v8) does not
           match the detected host platform (linux/amd64) and no
           specific platform was requested
  ```

* `POST /containers/create` on Linux now accepts the `HostConfig.CgroupnsMode` property. Set the property to `host` to create the container in the daemon's cgroup namespace, or `private` to create the container in its own private cgroup namespace. The per-daemon default is `host`, and can be changed by using the`CgroupNamespaceMode` daemon configuration parameter.

* `GET /info` now returns an `OSVersion` field, containing the operating system's version. This change is not versioned, and affects all API versions if the daemon has this patch.

* `GET /info` no longer returns the `SystemStatus` field if it does not have a value set. This change is not versioned, and affects all API versions if the daemon has this patch.

* `GET /services` now accepts query parameter `status`. When set `true`, services returned will include `ServiceStatus`, which provides Desired, Running, and Completed task counts for the service.

* `GET /services` may now include `ReplicatedJob` or `GlobalJob` as the `Mode` in a `ServiceSpec`.

* `GET /services/{id}` may now include `ReplicatedJob` or `GlobalJob` as the `Mode` in a `ServiceSpec`.

* `POST /services/create` now accepts `ReplicatedJob or `GlobalJob`as the`Mode`in the`ServiceSpec.

* `POST /services/{id}/update` accepts updating the fields of the `ReplicatedJob` object in the `ServiceSpec.Mode`. The service mode still cannot be changed, however.

* `GET /services` now includes `JobStatus` on Services with mode `ReplicatedJob` or `GlobalJob`.

* `GET /services/{id}` now includes `JobStatus` on Services with mode `ReplicatedJob` or `GlobalJob`.

* `GET /tasks` now includes `JobIteration` on Tasks spawned from a job-mode service.

* `GET /tasks/{id}` now includes `JobIteration` on the task if spawned from a job-mode service.

* `GET /containers/{id}/stats` now accepts a query param (`one-shot`) which, when used with `stream=false` fetches a single set of stats instead of waiting for two collection cycles to have 2 CPU stats over a 1 second period.

* The `KernelMemory` field in `HostConfig.Resources` is now deprecated.

* The `KernelMemory` field in `Info` is now deprecated.

* `GET /services` now returns `Ulimits` as part of `ContainerSpec`.

* `GET /services/{id}` now returns `Ulimits` as part of `ContainerSpec`.

* `POST /services/create` now accepts `Ulimits` as part of `ContainerSpec`.

* `POST /services/{id}/update` now accepts `Ulimits` as part of `ContainerSpec`.

## [v1.40 API changes](#v140-api-changes)

* The `/_ping` endpoint can now be accessed both using `GET` or `HEAD` requests. when accessed using a `HEAD` request, all headers are returned, but the body is empty (`Content-Length: 0`). This change is not versioned, and affects all API versions if the daemon has this patch. Clients are recommended to try using `HEAD`, but fallback to `GET` if the `HEAD` requests fails.
* `GET /_ping` and `HEAD /_ping` now set `Cache-Control` and `Pragma` headers to prevent the result from being cached. This change is not versioned, and affects all API versions if the daemon has this patch.
* `GET /services` now returns `Sysctls` as part of the `ContainerSpec`.
* `GET /services/{id}` now returns `Sysctls` as part of the `ContainerSpec`.
* `POST /services/create` now accepts `Sysctls` as part of the `ContainerSpec`.
* `POST /services/{id}/update` now accepts `Sysctls` as part of the `ContainerSpec`.
* `POST /services/create` now accepts `Config` as part of `ContainerSpec.Privileges.CredentialSpec`.
* `POST /services/{id}/update` now accepts `Config` as part of `ContainerSpec.Privileges.CredentialSpec`.
* `POST /services/create` now includes `Runtime` as an option in `ContainerSpec.Configs`
* `POST /services/{id}/update` now includes `Runtime` as an option in `ContainerSpec.Configs`
* `GET /tasks` now returns `Sysctls` as part of the `ContainerSpec`.
* `GET /tasks/{id}` now returns `Sysctls` as part of the `ContainerSpec`.
* `GET /networks` now supports a `dangling` filter type. When set to `true` (or `1`), the endpoint returns all networks that are not in use by a container. When set to `false` (or `0`), only networks that are in use by one or more containers are returned.
* `GET /nodes` now supports a filter type `node.label` filter to filter nodes based on the node.label. The format of the label filter is `node.label=<key>`/`node.label=<key>=<value>` to return those with the specified labels, or `node.label!=<key>`/`node.label!=<key>=<value>` to return those without the specified labels.
* `POST /containers/create` now accepts a `fluentd-async` option in `HostConfig.LogConfig.Config` when using the Fluentd logging driver. This option deprecates the `fluentd-async-connect` option, which remains functional, but will be removed in a future release. Users are encouraged to use the `fluentd-async` option going forward. This change is not versioned, and affects all API versions if the daemon has this patch.
* `POST /containers/create` now accepts a `fluentd-request-ack` option in `HostConfig.LogConfig.Config` when using the Fluentd logging driver. If enabled, the Fluentd logging driver sends the chunk option with a unique ID. The server will respond with an acknowledgement. This option improves the reliability of the message transmission. This change is not versioned, and affects all API versions if the daemon has this patch.
* `POST /containers/create`, `GET /containers/{id}/json`, and `GET /containers/json` now supports `BindOptions.NonRecursive`.
* `POST /swarm/init` now accepts a `DataPathPort` property to set data path port number.
* `GET /info` now returns information about `DataPathPort` that is currently used in swarm
* `GET /info` now returns `PidsLimit` boolean to indicate if the host kernel has PID limit support enabled.
* `GET /info` now includes `name=rootless` in `SecurityOptions` when the daemon is running in rootless mode. This change is not versioned, and affects all API versions if the daemon has this patch.
* `GET /info` now returns `none` as `CgroupDriver` when the daemon is running in rootless mode. This change is not versioned, and affects all API versions if the daemon has this patch.
* `POST /containers/create` now accepts `DeviceRequests` as part of `HostConfig`. Can be used to set Nvidia GPUs.
* `GET /swarm` endpoint now returns DataPathPort info
* `POST /containers/create` now takes `KernelMemoryTCP` field to set hard limit for kernel TCP buffer memory.
* `GET /service` now returns `MaxReplicas` as part of the `Placement`.
* `GET /service/{id}` now returns `MaxReplicas` as part of the `Placement`.
* `POST /service/create` and `POST /services/(id or name)/update` now take the field `MaxReplicas` as part of the service `Placement`, allowing to specify maximum replicas per node for the service.
* `POST /containers/create` on Linux now creates a container with `HostConfig.IpcMode=private` by default, if IpcMode is not explicitly specified. The per-daemon default can be changed back to `shareable` by using `DefaultIpcMode` daemon configuration parameter.
* `POST /containers/{id}/update` now accepts a `PidsLimit` field to tune a container's PID limit. Set `0` or `-1` for unlimited. Leave `null` to not change the current value.
* `POST /build` now accepts `outputs` key for configuring build outputs when using BuildKit mode.

## [V1.39 API changes](#v139-api-changes)

* `GET /info` now returns an empty string, instead of `<unknown>` for `KernelVersion` and `OperatingSystem` if the daemon was unable to obtain this information.
* `GET /info` now returns information about the product license, if a license has been applied to the daemon.
* `GET /info` now returns a `Warnings` field, containing warnings and informational messages about missing features, or issues related to the daemon configuration.
* `POST /swarm/init` now accepts a `DefaultAddrPool` property to set global scope default address pool
* `POST /swarm/init` now accepts a `SubnetSize` property to set global scope networks by giving the length of the subnet masks for every such network
* `POST /session` (added in [V1.31](#v131-api-changes) is no longer experimental. This endpoint can be used to run interactive long-running protocols between the client and the daemon.

## [V1.38 API changes](#v138-api-changes)

* `GET /tasks` and `GET /tasks/{id}` now return a `NetworkAttachmentSpec` field, containing the `ContainerID` for non-service containers connected to "attachable" swarm-scoped networks.

## [v1.37 API changes](#v137-api-changes)

* `POST /containers/create` and `POST /services/create` now supports exposing SCTP ports.
* `POST /configs/create` and `POST /configs/{id}/create` now accept a `Templating` driver.
* `GET /configs` and `GET /configs/{id}` now return the `Templating` driver of the config.
* `POST /secrets/create` and `POST /secrets/{id}/create` now accept a `Templating` driver.
* `GET /secrets` and `GET /secrets/{id}` now return the `Templating` driver of the secret.

## [v1.36 API changes](#v136-api-changes)

* `Get /events` now return `exec_die` event when an exec process terminates.

## [v1.35 API changes](#v135-api-changes)

* `POST /services/create` and `POST /services/(id)/update` now accepts an `Isolation` field on container spec to set the Isolation technology of the containers running the service (`default`, `process`, or `hyperv`). This configuration is only used for Windows containers.
* `GET /containers/(name)/logs` now supports an additional query parameter: `until`, which returns log lines that occurred before the specified timestamp.
* `POST /containers/{id}/exec` now accepts a `WorkingDir` property to set the work-dir for the exec process, independent of the container's work-dir.
* `Get /version` now returns a `Platform.Name` field, which can be used by products using Moby as a foundation to return information about the platform.
* `Get /version` now returns a `Components` field, which can be used to return information about the components used. Information about the engine itself is now included as a "Component" version, and contains all information from the top-level `Version`, `GitCommit`, `APIVersion`, `MinAPIVersion`, `GoVersion`, `Os`, `Arch`, `BuildTime`, `KernelVersion`, and `Experimental` fields. Going forward, the information from the `Components` section is preferred over their top-level counterparts.

## [v1.34 API changes](#v134-api-changes)

* `POST /containers/(name)/wait?condition=removed` now also also returns in case of container removal failure. A pointer to a structure named `Error` added to the response JSON in order to indicate a failure. If `Error` is `null`, container removal has succeeded, otherwise the test of an error message indicating why container removal has failed is available from `Error.Message` field.

## [v1.33 API changes](#v133-api-changes)

* `GET /events` now supports filtering 4 more kinds of events: `config`, `node`, `secret` and `service`.

## [v1.32 API changes](#v132-api-changes)

* `POST /images/create` now accepts a `platform` parameter in the form of `os[/arch[/variant]]`.
* `POST /containers/create` now accepts additional values for the `HostConfig.IpcMode` property. New values are `private`, `shareable`, and `none`.
* `DELETE /networks/{id or name}` fixed issue where a `name` equal to another network's name was able to mask that `id`. If both a network with the given *name* exists, and a network with the given *id*, the network with the given *id* is now deleted. This change is not versioned, and affects all API versions if the daemon has this patch.

## [v1.31 API changes](#v131-api-changes)

* `DELETE /secrets/(name)` now returns status code 404 instead of 500 when the secret does not exist.
* `POST /secrets/create` now returns status code 409 instead of 500 when creating an already existing secret.
* `POST /secrets/create` now accepts a `Driver` struct, allowing the `Name` and driver-specific `Options` to be passed to store a secrets in an external secrets store. The `Driver` property can be omitted if the default (internal) secrets store is used.
* `GET /secrets/(id)` and `GET /secrets` now return a `Driver` struct, containing the `Name` and driver-specific `Options` of the external secrets store used to store the secret. The `Driver` property is omitted if no external store is used.
* `POST /secrets/(name)/update` now returns status code 400 instead of 500 when updating a secret's content which is not the labels.
* `POST /nodes/(name)/update` now returns status code 400 instead of 500 when demoting last node fails.
* `GET /networks/(id or name)` now takes an optional query parameter `scope` that will filter the network based on the scope (`local`, `swarm`, or `global`).
* `POST /session` is a new endpoint that can be used for running interactive long-running protocols between client and the daemon. This endpoint is experimental and only available if the daemon is started with experimental features enabled.
* `GET /images/(name)/get` now includes an `ImageMetadata` field which contains image metadata that is local to the engine and not part of the image config.
* `POST /services/create` now accepts a `PluginSpec` when `TaskTemplate.Runtime` is set to `plugin`
* `GET /events` now supports config events `create`, `update` and `remove` that are emitted when users create, update or remove a config
* `GET /volumes/` and `GET /volumes/{name}` now return a `CreatedAt` field, containing the date/time the volume was created. This field is omitted if the creation date/time for the volume is unknown. For volumes with scope "global", this field represents the creation date/time of the local *instance* of the volume, which may differ from instances of the same volume on different nodes.
* `GET /system/df` now returns a `CreatedAt` field for `Volumes`. Refer to the `/volumes/` endpoint for a description of this field.

## [v1.30 API changes](#v130-api-changes)

* `GET /info` now returns the list of supported logging drivers, including plugins.
* `GET /info` and `GET /swarm` now returns the cluster-wide swarm CA info if the node is in a swarm: the cluster root CA certificate, and the cluster TLS leaf certificate issuer's subject and public key. It also displays the desired CA signing certificate, if any was provided as part of the spec.
* `POST /build/` now (when not silent) produces an `Aux` message in the JSON output stream with payload `types.BuildResult` for each image produced. The final such message will reference the image resulting from the build.
* `GET /nodes` and `GET /nodes/{id}` now returns additional information about swarm TLS info if the node is part of a swarm: the trusted root CA, and the issuer's subject and public key.
* `GET /distribution/(name)/json` is a new endpoint that returns a JSON output stream with payload `types.DistributionInspect` for an image name. It includes a descriptor with the digest, and supported platforms retrieved from directly contacting the registry.
* `POST /swarm/update` now accepts 3 additional parameters as part of the swarm spec's CA configuration; the desired CA certificate for the swarm, the desired CA key for the swarm (if not using an external certificate), and an optional parameter to force swarm to generate and rotate to a new CA certificate/key pair.
* `POST /service/create` and `POST /services/(id or name)/update` now take the field `Platforms` as part of the service `Placement`, allowing to specify platforms supported by the service.
* `POST /containers/(name)/wait` now accepts a `condition` query parameter to indicate which state change condition to wait for. Also, response headers are now returned immediately to acknowledge that the server has registered a wait callback for the client.
* `POST /swarm/init` now accepts a `DataPathAddr` property to set the IP-address or network interface to use for data traffic
* `POST /swarm/join` now accepts a `DataPathAddr` property to set the IP-address or network interface to use for data traffic
* `GET /events` now supports service, node and secret events which are emitted when users create, update and remove service, node and secret
* `GET /events` now supports network remove event which is emitted when users remove a swarm scoped network
* `GET /events` now supports a filter type `scope` in which supported value could be swarm and local
* `PUT /containers/(name)/archive` now accepts a `copyUIDGID` parameter to allow copy UID/GID maps to dest file or dir.

## [v1.29 API changes](#v129-api-changes)

* `DELETE /networks/(name)` now allows to remove the ingress network, the one used to provide the routing-mesh.
* `POST /networks/create` now supports creating the ingress network, by specifying an `Ingress` boolean field. As of now this is supported only when using the overlay network driver.
* `GET /networks/(name)` now returns an `Ingress` field showing whether the network is the ingress one.
* `GET /networks/` now supports a `scope` filter to filter networks based on the network mode (`swarm`, `global`, or `local`).
* `POST /containers/create`, `POST /service/create` and `POST /services/(id or name)/update` now takes the field `StartPeriod` as a part of the `HealthConfig` allowing for specification of a period during which the container should not be considered unhealthy even if health checks do not pass.
* `GET /services/(id)` now accepts an `insertDefaults` query-parameter to merge default values into the service inspect output.
* `POST /containers/prune`, `POST /images/prune`, `POST /volumes/prune`, and `POST /networks/prune` now support a `label` filter to filter containers, images, volumes, or networks based on the label. The format of the label filter could be `label=<key>`/`label=<key>=<value>` to remove those with the specified labels, or `label!=<key>`/`label!=<key>=<value>` to remove those without the specified labels.
* `POST /services/create` now accepts `Privileges` as part of `ContainerSpec`. Privileges currently include `CredentialSpec` and `SELinuxContext`.

## [v1.28 API changes](#v128-api-changes)

* `POST /containers/create` now includes a `Consistency` field to specify the consistency level for each `Mount`, with possible values `default`, `consistent`, `cached`, or `delegated`.
* `GET /containers/create` now takes a `DeviceCgroupRules` field in `HostConfig` allowing to set custom device cgroup rules for the created container.
* Optional query parameter `verbose` for `GET /networks/(id or name)` will now list all services with all the tasks, including the non-local tasks on the given network.
* `GET /containers/(id or name)/attach/ws` now returns WebSocket in binary frame format for API version >= v1.28, and returns WebSocket in text frame format for API version< v1.28, for the purpose of backward-compatibility.
* `GET /networks` is optimised only to return list of all networks and network specific information. List of all containers attached to a specific network is removed from this API and is only available using the network specific `GET /networks/{network-id}`.
* `GET /containers/json` now supports `publish` and `expose` filters to filter containers that expose or publish certain ports.
* `POST /services/create` and `POST /services/(id or name)/update` now accept the `ReadOnly` parameter, which mounts the container's root filesystem as read only.
* `POST /build` now accepts `extrahosts` parameter to specify a host to ip mapping to use during the build.
* `POST /services/create` and `POST /services/(id or name)/update` now accept a `rollback` value for `FailureAction`.
* `POST /services/create` and `POST /services/(id or name)/update` now accept an optional `RollbackConfig` object which specifies rollback options.
* `GET /services` now supports a `mode` filter to filter services based on the service mode (either `global` or `replicated`).
* `POST /containers/(name)/update` now supports updating `NanoCpus` that represents CPU quota in units of 10-9 CPUs.
* `POST /plugins/{name}/disable` now accepts a `force` query-parameter to disable a plugin even if still in use.

## [v1.27 API changes](#v127-api-changes)

* `GET /containers/(id or name)/stats` now includes an `online_cpus` field in both `precpu_stats` and `cpu_stats`. If this field is `nil` then for compatibility with older daemons the length of the corresponding `cpu_usage.percpu_usage` array should be used.

## [v1.26 API changes](#v126-api-changes)

* `POST /plugins/(plugin name)/upgrade` upgrade a plugin.

## [v1.25 API changes](#v125-api-changes)

* The API version is now required in all API calls. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`.
* `GET /version` now returns `MinAPIVersion`.
* `POST /build` accepts `networkmode` parameter to specify network used during build.
* `GET /images/(name)/json` now returns `OsVersion` if populated
* `GET /images/(name)/json` no longer contains the `RootFS.BaseLayer` field. This field was used for Windows images that used a base-image that was pre-installed on the host (`RootFS.Type` `layers+base`), which is no longer supported, and the `RootFS.BaseLayer` field has been removed.
* `GET /info` now returns `Isolation`.
* `POST /containers/create` now takes `AutoRemove` in HostConfig, to enable auto-removal of the container on daemon side when the container's process exits.
* `GET /containers/json` and `GET /containers/(id or name)/json` now return `"removing"` as a value for the `State.Status` field if the container is being removed. Previously, "exited" was returned as status.
* `GET /containers/json` now accepts `removing` as a valid value for the `status` filter.
* `GET /containers/json` now supports filtering containers by `health` status.
* `DELETE /volumes/(name)` now accepts a `force` query parameter to force removal of volumes that were already removed out of band by the volume driver plugin.
* `POST /containers/create/` and `POST /containers/(name)/update` now validates restart policies.
* `POST /containers/create` now validates IPAMConfig in NetworkingConfig, and returns error for invalid IPv4 and IPv6 addresses (`--ip` and `--ip6` in `docker create/run`).
* `POST /containers/create` now takes a `Mounts` field in `HostConfig` which replaces `Binds`, `Volumes`, and `Tmpfs`. *note*: `Binds`, `Volumes`, and `Tmpfs` are still available and can be combined with `Mounts`.
* `POST /build` now performs a preliminary validation of the `Dockerfile` before starting the build, and returns an error if the syntax is incorrect. Note that this change is *unversioned* and applied to all API versions.
* `POST /build` accepts `cachefrom` parameter to specify images used for build cache.
* `GET /networks/` endpoint now correctly returns a list of *all* networks, instead of the default network if a trailing slash is provided, but no `name` or `id`.
* `DELETE /containers/(name)` endpoint now returns an error of `removal of container name is already in progress` with status code of 400, when container name is in a state of removal in progress.
* `GET /containers/json` now supports a `is-task` filter to filter containers that are tasks (part of a service in swarm mode).
* `POST /containers/create` now takes `StopTimeout` field.
* `POST /services/create` and `POST /services/(id or name)/update` now accept `Monitor` and `MaxFailureRatio` parameters, which control the response to failures during service updates.
* `POST /services/(id or name)/update` now accepts a `ForceUpdate` parameter inside the `TaskTemplate`, which causes the service to be updated even if there are no changes which would ordinarily trigger an update.
* `POST /services/create` and `POST /services/(id or name)/update` now return a `Warnings` array.
* `GET /networks/(name)` now returns field `Created` in response to show network created time.
* `POST /containers/(id or name)/exec` now accepts an `Env` field, which holds a list of environment variables to be set in the context of the command execution.
* `GET /volumes`, `GET /volumes/(name)`, and `POST /volumes/create` now return the `Options` field which holds the driver specific options to use for when creating the volume.
* `GET /exec/(id)/json` now returns `Pid`, which is the system pid for the exec'd process.
* `POST /containers/prune` prunes stopped containers.
* `POST /images/prune` prunes unused images.
* `POST /volumes/prune` prunes unused volumes.
* `POST /networks/prune` prunes unused networks.
* Every API response now includes a `Docker-Experimental` header specifying if experimental features are enabled (value can be `true` or `false`).
* Every API response now includes a `API-Version` header specifying the default API version of the server.
* The `hostConfig` option now accepts the fields `CpuRealtimePeriod` and `CpuRtRuntime` to allocate cpu runtime to rt tasks when `CONFIG_RT_GROUP_SCHED` is enabled in the kernel.
* The `SecurityOptions` field within the `GET /info` response now includes `userns` if user namespaces are enabled in the daemon.
* `GET /nodes` and `GET /node/(id or name)` now return `Addr` as part of a node's `Status`, which is the address that that node connects to the manager from.
* The `HostConfig` field now includes `NanoCpus` that represents CPU quota in units of 10-9 CPUs.
* `GET /info` now returns more structured information about security options.
* The `HostConfig` field now includes `CpuCount` that represents the number of CPUs available for execution by the container. Windows daemon only.
* `POST /services/create` and `POST /services/(id or name)/update` now accept the `TTY` parameter, which allocate a pseudo-TTY in container.
* `POST /services/create` and `POST /services/(id or name)/update` now accept the `DNSConfig` parameter, which specifies DNS related configurations in resolver configuration file (resolv.conf) through `Nameservers`, `Search`, and `Options`.
* `POST /services/create` and `POST /services/(id or name)/update` now support `node.platform.arch` and `node.platform.os` constraints in the services `TaskSpec.Placement.Constraints` field.
* `GET /networks/(id or name)` now includes IP and name of all peers nodes for swarm mode overlay networks.
* `GET /plugins` list plugins.
* `POST /plugins/pull?name=<plugin name>` pulls a plugin.
* `GET /plugins/(plugin name)` inspect a plugin.
* `POST /plugins/(plugin name)/set` configure a plugin.
* `POST /plugins/(plugin name)/enable` enable a plugin.
* `POST /plugins/(plugin name)/disable` disable a plugin.
* `POST /plugins/(plugin name)/push` push a plugin.
* `POST /plugins/create?name=(plugin name)` create a plugin.
* `DELETE /plugins/(plugin name)` delete a plugin.
* `POST /node/(id or name)/update` now accepts both `id` or `name` to identify the node to update.
* `GET /images/json` now support a `reference` filter.
* `GET /secrets` returns information on the secrets.
* `POST /secrets/create` creates a secret.
* `DELETE /secrets/{id}` removes the secret `id`.
* `GET /secrets/{id}` returns information on the secret `id`.
* `POST /secrets/{id}/update` updates the secret `id`.
* `POST /services/(id or name)/update` now accepts service name or prefix of service id as a parameter.
* `POST /containers/create` added 2 built-in log-opts that work on all logging drivers, `mode` (`blocking`|`non-blocking`), and `max-buffer-size` (e.g. `2m`) which enables a non-blocking log buffer.
* `POST /containers/create` now takes `HostConfig.Init` field to run an init inside the container that forwards signals and reaps processes.

## [v1.24 API changes](#v124-api-changes)

* `POST /containers/create` now takes `StorageOpt` field.
* `GET /info` now returns `SecurityOptions` field, showing if `apparmor`, `seccomp`, or `selinux` is supported.
* `GET /info` no longer returns the `ExecutionDriver` property. This property was no longer used after integration with ContainerD in Docker 1.11.
* `GET /networks` now supports filtering by `label` and `driver`.
* `GET /containers/json` now supports filtering containers by `network` name or id.
* `POST /containers/create` now takes `IOMaximumBandwidth` and `IOMaximumIOps` fields. Windows daemon only.
* `POST /containers/create` now returns an HTTP 400 "bad parameter" message if no command is specified (instead of an HTTP 500 "server error")
* `GET /images/search` now takes a `filters` query parameter.
* `GET /events` now supports a `reload` event that is emitted when the daemon configuration is reloaded.
* `GET /events` now supports filtering by daemon name or ID.
* `GET /events` now supports a `detach` event that is emitted on detaching from container process.
* `GET /events` now supports an `exec_detach `event that is emitted on detaching from exec process.
* `GET /images/json` now supports filters `since` and `before`.
* `POST /containers/(id or name)/start` no longer accepts a `HostConfig`.
* `POST /images/(name)/tag` no longer has a `force` query parameter.
* `GET /images/search` now supports maximum returned search results `limit`.
* `POST /containers/{name:.*}/copy` is now removed and errors out starting from this API version.
* API errors are now returned as JSON instead of plain text.
* `POST /containers/create` and `POST /containers/(id)/start` allow you to configure kernel parameters (sysctls) for use in the container.
* `POST /containers/<container ID>/exec` and `POST /exec/<exec ID>/start` no longer expects a "Container" field to be present. This property was not used and is no longer sent by the docker client.
* `POST /containers/create/` now validates the hostname (should be a valid RFC 1123 hostname).
* `POST /containers/create/` `HostConfig.PidMode` field now accepts `container:<name|id>`, to have the container join the PID namespace of an existing container.

## [v1.23 API changes](#v123-api-changes)

* `GET /containers/json` returns the state of the container, one of `created`, `restarting`, `running`, `paused`, `exited` or `dead`.
* `GET /containers/json` returns the mount points for the container.
* `GET /networks/(name)` now returns an `Internal` field showing whether the network is internal or not.
* `GET /networks/(name)` now returns an `EnableIPv6` field showing whether the network has ipv6 enabled or not.
* `POST /containers/(name)/update` now supports updating container's restart policy.
* `POST /networks/create` now supports enabling ipv6 on the network by setting the `EnableIPv6` field (doing this with a label will no longer work).
* `GET /info` now returns `CgroupDriver` field showing what cgroup driver the daemon is using; `cgroupfs` or `systemd`.
* `GET /info` now returns `KernelMemory` field, showing if "kernel memory limit" is supported.
* `POST /containers/create` now takes `PidsLimit` field, if the kernel is >= 4.3 and the pids cgroup is supported.
* `GET /containers/(id or name)/stats` now returns `pids_stats`, if the kernel is >= 4.3 and the pids cgroup is supported.
* `POST /containers/create` now allows you to override usernamespaces remapping and use privileged options for the container.
* `POST /containers/create` now allows specifying `nocopy` for named volumes, which disables automatic copying from the container path to the volume.
* `POST /auth` now returns an `IdentityToken` when supported by a registry.
* `POST /containers/create` with both `Hostname` and `Domainname` fields specified will result in the container's hostname being set to `Hostname`, rather than `Hostname.Domainname`.
* `GET /volumes` now supports more filters, new added filters are `name` and `driver`.
* `GET /containers/(id or name)/logs` now accepts a `details` query parameter to stream the extra attributes that were provided to the containers `LogOpts`, such as environment variables and labels, with the logs.
* `POST /images/load` now returns progress information as a JSON stream, and has a `quiet` query parameter to suppress progress details.

## [v1.22 API changes](#v122-api-changes)

* The `HostConfig.LxcConf` field has been removed, and is no longer available on `POST /containers/create` and `GET /containers/(id)/json`.
* `POST /container/(name)/update` updates the resources of a container.
* `GET /containers/json` supports filter `isolation` on Windows.
* `GET /containers/json` now returns the list of networks of containers.
* `GET /info` Now returns `Architecture` and `OSType` fields, providing information about the host architecture and operating system type that the daemon runs on.
* `GET /networks/(name)` now returns a `Name` field for each container attached to the network.
* `GET /version` now returns the `BuildTime` field in RFC3339Nano format to make it consistent with other date/time values returned by the API.
* `AuthConfig` now supports a `registrytoken` for token based authentication
* `POST /containers/create` now has a 4M minimum value limit for `HostConfig.KernelMemory`
* Pushes initiated with `POST /images/(name)/push` and pulls initiated with `POST /images/create` will be cancelled if the HTTP connection making the API request is closed before the push or pull completes.
* `POST /containers/create` now allows you to set a read/write rate limit for a device (in bytes per second or IO per second).
* `GET /networks` now supports filtering by `name`, `id` and `type`.
* `POST /containers/create` now allows you to set the static IPv4 and/or IPv6 address for the container.
* `POST /networks/(id)/connect` now allows you to set the static IPv4 and/or IPv6 address for the container.
* `GET /info` now includes the number of containers running, stopped, and paused.
* `POST /networks/create` now supports restricting external access to the network by setting the `Internal` field.
* `POST /networks/(id)/disconnect` now includes a `Force` option to forcefully disconnect a container from network
* `GET /containers/(id)/json` now returns the `NetworkID` of containers.
* `POST /networks/create` Now supports an options field in the IPAM config that provides options for custom IPAM plugins.
* `GET /networks/{network-id}` Now returns IPAM config options for custom IPAM plugins if any are available.
* `GET /networks/<network-id>` now returns subnets info for user-defined networks.
* `GET /info` can now return a `SystemStatus` field useful for returning additional information about applications that are built on top of engine.

## [v1.21 API changes](#v121-api-changes)

* `GET /volumes` lists volumes from all volume drivers.
* `POST /volumes/create` to create a volume.
* `GET /volumes/(name)` get low-level information about a volume.
* `DELETE /volumes/(name)` remove a volume with the specified name.
* `VolumeDriver` was moved from `config` to `HostConfig` to make the configuration portable.
* `GET /images/(name)/json` now returns information about an image's `RepoTags` and `RepoDigests`.
* The `config` option now accepts the field `StopSignal`, which specifies the signal to use to kill a container.
* `GET /containers/(id)/stats` will return networking information respectively for each interface.
* The `HostConfig` option now includes the `DnsOptions` field to configure the container's DNS options.
* `POST /build` now optionally takes a serialized map of build-time variables.
* `GET /events` now includes a `timenano` field, in addition to the existing `time` field.
* `GET /events` now supports filtering by image and container labels.
* `GET /info` now lists engine version information and return the information of `CPUShares` and `Cpuset`.
* `GET /containers/json` will return `ImageID` of the image used by container.
* `POST /exec/(name)/start` will now return an HTTP 409 when the container is either stopped or paused.
* `POST /containers/create` now takes `KernelMemory` in HostConfig to specify kernel memory limit.
* `GET /containers/(name)/json` now accepts a `size` parameter. Setting this parameter to '1' returns container size information in the `SizeRw` and `SizeRootFs` fields.
* `GET /containers/(name)/json` now returns a `NetworkSettings.Networks` field, detailing network settings per network. This field deprecates the `NetworkSettings.EndpointID`, `NetworkSettings.Gateway`, `NetworkSettings.GlobalIPv6Address`, `NetworkSettings.GlobalIPv6PrefixLen` `NetworkSettings.IPAddress`, `NetworkSettings.IPPrefixLen`, `NetworkSettings.IPv6Gateway`, `NetworkSettings.MacAddress` fields, which are still returned for backward-compatibility, but will be removed in a future version.
* `GET /exec/(id)/json` now returns a `NetworkSettings.Networks` field, detailing networksettings per network. This field deprecates the `NetworkSettings.Gateway`, `NetworkSettings.IPAddress`, `NetworkSettings.IPPrefixLen`, and `NetworkSettings.MacAddress` fields, which are still returned for backward-compatibility, but will be removed in a future version.
* The `HostConfig` option now includes the `OomScoreAdj` field for adjusting the badness heuristic. This heuristic selects which processes the OOM killer kills under out-of-memory conditions.

## [v1.20 API changes](#v120-api-changes)

* `GET /containers/(id)/archive` get an archive of filesystem content from a container.
* `PUT /containers/(id)/archive` upload an archive of content to be extracted to an existing directory inside a container's filesystem.
* `POST /containers/(id)/copy` is deprecated in favor of the above `archive` endpoint which can be used to download files and directories from a container.
* The `hostConfig` option now accepts the field `GroupAdd`, which specifies a list of additional groups that the container process will run as.

## [v1.19 API changes](#v119-api-changes)

* When the daemon detects a version mismatch with the client, usually when the client is newer than the daemon, an HTTP 400 is now returned instead of a 404.
* `GET /containers/(id)/stats` now accepts `stream` bool to get only one set of stats and disconnect.
* `GET /containers/(id)/logs` now accepts a `since` timestamp parameter.
* `GET /info` The fields `Debug`, `IPv4Forwarding`, `MemoryLimit`, and `SwapLimit` are now returned as boolean instead of as an int. In addition, the end point now returns the new boolean fields `CpuCfsPeriod`, `CpuCfsQuota`, and `OomKillDisable`.
* The `hostConfig` option now accepts the fields `CpuPeriod` and `CpuQuota`
* `POST /build` accepts `cpuperiod` and `cpuquota` options

## [v1.18 API changes](#v118-api-changes)

* `GET /version` now returns `Os`, `Arch` and `KernelVersion`.
* `POST /containers/create` and `POST /containers/(id)/start`allow you to set ulimit settings for use in the container.
* `GET /info` now returns `SystemTime`, `HttpProxy`,`HttpsProxy` and `NoProxy`.
* `GET /images/json` added a `RepoDigests` field to include image digest information.
* `POST /build` can now set resource constraints for all containers created for the build.
* `CgroupParent` can be passed in the host config to setup container cgroups under a specific cgroup.
* `POST /build` closing the HTTP request cancels the build
* `POST /containers/(id)/exec` includes `Warnings` field to response.

### [v1.17 API changes](#v117-api-changes)

* The build supports `LABEL` command. Use this to add metadata to an image. For example you could add data describing the content of an image. `LABEL "com.example.vendor"="ACME Incorporated"`
* `POST /containers/(id)/attach` and `POST /exec/(id)/start`
* The Docker client now hints potential proxies about connection hijacking using HTTP Upgrade headers.
* `POST /containers/create` sets labels on container create describing the container.
* `GET /containers/json` returns the labels associated with the containers (`Labels`).
* `GET /containers/(id)/json` returns the list current execs associated with the container (`ExecIDs`). This endpoint now returns the container labels (`Config.Labels`).
* `POST /containers/(id)/rename` renames a container `id` to a new name.\*
* `POST /containers/create` and `POST /containers/(id)/start` callers can pass `ReadonlyRootfs` in the host config to mount the container's root filesystem as read only.
* `GET /containers/(id)/stats` returns a live stream of a container's resource usage statistics.
* `GET /images/json` returns the labels associated with each image (`Labels`).

### [v1.16 API changes](#v116-api-changes)

* `GET /info` returns the number of CPUs available on the machine (`NCPU`), total memory available (`MemTotal`), a user-friendly name describing the running Docker daemon (`Name`), a unique ID identifying the daemon (`ID`), and a list of daemon labels (`Labels`).
* `POST /containers/create` callers can set the new container's MAC address explicitly.
* Volumes are now initialized when the container is created.
* `POST /containers/(id)/copy` copies data which is contained in a volume.

### [v1.15 API changes](#v115-api-changes)

* `POST /containers/create` can now set a container's `HostConfig` when creating a container. Previously this was only available when starting a container.

### [v1.14 API changes](#v114-api-changes)

* `DELETE /containers/(id)` when using `force`, the container will be immediately killed with SIGKILL.
* `POST /containers/(id)/start` the `HostConfig` option accepts the field `CapAdd`, which specifies a list of capabilities to add, and the field `CapDrop`, which specifies a list of capabilities to drop.
* `POST /images/create` th `fromImage` and `repo` parameters support the `repo:tag` format. Consequently, the `tag` parameter is now obsolete. Using the new format and the `tag` parameter at the same time will return an error.

## [v1.13 API changes](#v113-api-changes)

* `GET /containers/(name)/json`

**New!** The `HostConfig.Links` field is now filled correctly

**New!** `Sockets` parameter added to the `/info` endpoint listing all the sockets the daemon is configured to listen on.

`POST /containers/(name)/start` `POST /containers/(name)/stop`

**New!** `start` and `stop` will now return 304 if the container's status is not modified

`POST /commit`

**New!** Added a `pause` parameter (default `true`) to pause the container during commit

## [v1.12 API changes](#v112-api-changes)

* `POST /build` now supports a `forcerm` parameter to always remove containers.
* `GET /containers/(name)/json`,`GET /images/(name)/json`: JSON keys are now in CamelCase.
* `GET /images/search`: Trusted builds are now Automated Builds, and the `is_trusted` field was renamed to `is_automated`.
* The `POST /images/(name)/insert` endpoint has been removed.

## [v1.11 API changes](#v111-api-changes)

### [What's new](#whats-new)

* Add new `GET /_ping` endpoint to check if the API server is ready to accept connections.
* `GET /events` now supports an `until` parameter to close connection after the given timestamp.
* `GET /containers/(id)/logs` is now the preferred method for getting container logs.

## [v1.10 API changes](#v110-api-changes)

* `DELETE /images/(name)` now provides a `force` parameter to force delete of an image, even if it's tagged in multiple repositories.
* `DELETE /images/(name)` now provides a `noprune` parameter to prevent the deletion of parent images.
* `DELETE /containers/(id)` now provides a `force` parameter to force deleting a container, even if it is currently running.

## [v1.9 API changes](#v19-api-changes)

* `POST /build` now takes a serialized ConfigFile which it uses to resolve the proper registry auth credentials for pulling the base image. Clients which previously implemented the version accepting an AuthConfig object must be updated.

## [v1.8 API changes](#v18-api-changes)

* `POST /build` now returns build status as JSON stream. In case of a build error, it returns the exit status of the failed command.
* `GET /containers/(id)/json` now returns the host config for the container.
* `POST /images/create`, `POST /images/(name)/insert` and `POST /images/(name)/push` now include a `progressDetail` object in the JSON. It's now possible to get the current value and the total of the progress without having to parse the string.

## [v1.7 API changes](#v17-api-changes)

* The `GET /images/viz` endpoint was removed. The `images --viz` output is now generated in the client, using the `GET /images/json` endpoint.
* The `GET /images/json` response now returns a single entry per image with a nested attribute indicating the repo/tags that apply to that image.

Instead of:

```
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "VirtualSize": 131506275,
    "Size": 131506275,
    "Created": 1365714795,
    "Id": "8dbd9e392a964056420e5d58ca5cc376ef18e2de93b5cc90e868a1bbc8318c1c",
    "Tag": "12.04",
    "Repository": "ubuntu"
  },
  {
    "VirtualSize": 131506275,
    "Size": 131506275,
    "Created": 1365714795,
    "Id": "8dbd9e392a964056420e5d58ca5cc376ef18e2de93b5cc90e868a1bbc8318c1c",
    "Tag": "latest",
    "Repository": "ubuntu"
  }
]
```

The returned json looks like this:

```
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
     "RepoTags": [
       "ubuntu:12.04",
       "ubuntu:latest"
     ],
     "Id": "8dbd9e392a964056420e5d58ca5cc376ef18e2de93b5cc90e868a1bbc8318c1c",
     "Created": 1365714795,
     "Size": 131506275,
     "VirtualSize": 131506275
  }
]
```

## [v1.6 API changes](#v16-api-changes)

### [What's new](#whats-new-1)

* `POST /containers/(id)/attach` now provides a multiplexed response to allow splitting stderr from stdout. This is done by prefixing a header to each transmission. See the `POST /containers/(id)/attach` endpoint. The WebSocket attach is unchanged. Note that attach calls on the previous API version didn't change. Stdout and stderr are merged.

## [v1.5 API changes](#v15-api-changes)

* `POST /images/create` now accepts registry credentials via an AuthConfig object sent through the `X-Registry-Auth` header.
* `POST /images/(name)/push` now requires the `AuthConfig` object to be passed through the `X-Registry-Auth` instead of the request body.
* `GET /containers/json` changed the format of the Ports entry to a list of dicts, each containing PublicPort, PrivatePort and Type describing a port mapping.

## [v1.4 API changes](#v14-api-changes)

* `POST /images/create` now downloads all images in parallel when pulling a repo.
* `GET /containers/(id)/top` now accepts `ps` args, which is used by `docker top`, for example, `docker top <container_id> aux`.
* `GET /events` now includes the image's name.

## [v1.3 API changes](#v13-api-changes)

* Add `GET /containers/(id)/top` endpoint to list the processes running inside the container.

* Add `GET /events` endpoint to monitor docker's events via streaming or via polling.

* `GET /containers/json` now provides a `size=1` option to get the size of the containers.

* `POST /containers/<id>/start` now accepts host-specific configuration (e.g., bind mounts) in the POST body for start calls.

* `POST /build`:

  * Simplify the upload of the build context
  * Simply stream a tarball instead of multipart upload with 4 intermediary buffers
  * Simpler, less memory usage, less disk usage and faster

> **Warning**: The `POST /build` improvements are not reverse-compatible. Pre 1.3 clients will break on `POST /build`.

## [v1.2 API changes](#v12-api-changes)

* The auth configuration is now handled by the client, and clients must send authConfig as body on `POST /images/(name)/push`.
* `GET /auth` is now deprecated.
* `POST /auth` now only checks the configuration but doesn't store it on the server
* `POST /images/<name>/delete` now only untags the image if it has children and removes all the untagged parents if has any.
* `POST /images/<name>/delete` now returns a JSON structure with the list of images deleted/untagged.

## [v1.1 API changes](#v11-api-changes)

`POST /images/create`, `POST /images/(name)/insert`, and `POST /images/(name)/push` now use a JSON stream instead of HTML hijack, it looks like this:

```
HTTP/1.1 200 OK
Content-Type: application/json

{"status":"Pushing..."}
{"status":"Pushing", "progress":"1/? (n/a)"}
{"error":"Invalid..."}
...
```

## [v1.0 API changes](#v10-api-changes)

Initial version (docker [v0.3.3](https://github.com/docker/docker/commit/822056094aa31c224e78cd568e02fe5458a0eecc))

----
url: https://docs.docker.com/reference/api/dvp/deprecated/
----

# Deprecated Docker Verified Publisher API endpoints

***

Table of contents

***

This page provides an overview of endpoints that are deprecated in Docker Verified Publisher API.

***

| Status | Feature                                                       | Date       |
| ------ | ------------------------------------------------------------- | ---------- |
|        | [Create deprecation log table](#create-deprecation-log-table) | 2025-06-27 |

***

### [Create deprecation log table](#create-deprecation-log-table)

Reformat page

***

----
url: https://docs.docker.com/guides/testcontainers-java-aws-localstack/write-tests/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Write tests with Testcontainers

***

Table of contents

***

To test the application, you need a running LocalStack instance that emulates the AWS S3 and SQS services. Testcontainers spins up LocalStack in a Docker container and `@DynamicPropertySource` connects it to Spring Cloud AWS.

## [Configure the test container](#configure-the-test-container)

You can start a LocalStack container and configure the Spring Cloud AWS properties to talk to it instead of actual AWS services. The properties you need to set are:

```properties
spring.cloud.aws.s3.endpoint=http://localhost:4566
spring.cloud.aws.sqs.endpoint=http://localhost:4566
spring.cloud.aws.credentials.access-key=noop
spring.cloud.aws.credentials.secret-key=noop
spring.cloud.aws.region.static=us-east-1
```

For testing, use an ephemeral container that starts on a random available port so that you can run multiple builds in CI in parallel without port conflicts.

## [Write the test](#write-the-test)

Create `MessageListenerTest.java`:

```java
package com.testcontainers.demo;

import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;
import static org.testcontainers.containers.localstack.LocalStackContainer.Service.S3;
import static org.testcontainers.containers.localstack.LocalStackContainer.Service.SQS;

import java.io.IOException;
import java.time.Duration;
import java.util.UUID;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.containers.localstack.LocalStackContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;
import org.testcontainers.utility.DockerImageName;

@SpringBootTest
@Testcontainers
class MessageListenerTest {

  @Container
  static LocalStackContainer localStack = new LocalStackContainer(
    DockerImageName.parse("localstack/localstack:3.0")
  );

  static final String BUCKET_NAME = UUID.randomUUID().toString();
  static final String QUEUE_NAME = UUID.randomUUID().toString();

  @DynamicPropertySource
  static void overrideProperties(DynamicPropertyRegistry registry) {
    registry.add("app.bucket", () -> BUCKET_NAME);
    registry.add("app.queue", () -> QUEUE_NAME);
    registry.add(
      "spring.cloud.aws.region.static",
      () -> localStack.getRegion()
    );
    registry.add(
      "spring.cloud.aws.credentials.access-key",
      () -> localStack.getAccessKey()
    );
    registry.add(
      "spring.cloud.aws.credentials.secret-key",
      () -> localStack.getSecretKey()
    );
    registry.add(
      "spring.cloud.aws.s3.endpoint",
      () -> localStack.getEndpointOverride(S3).toString()
    );
    registry.add(
      "spring.cloud.aws.sqs.endpoint",
      () -> localStack.getEndpointOverride(SQS).toString()
    );
  }

  @BeforeAll
  static void beforeAll() throws IOException, InterruptedException {
    localStack.execInContainer("awslocal", "s3", "mb", "s3://" + BUCKET_NAME);
    localStack.execInContainer(
      "awslocal",
      "sqs",
      "create-queue",
      "--queue-name",
      QUEUE_NAME
    );
  }

  @Autowired
  StorageService storageService;

  @Autowired
  MessageSender publisher;

  @Autowired
  ApplicationProperties properties;

  @Test
  void shouldHandleMessageSuccessfully() {
    Message message = new Message(UUID.randomUUID(), "Hello World");
    publisher.publish(properties.queue(), message);

    await()
      .pollInterval(Duration.ofSeconds(2))
      .atMost(Duration.ofSeconds(10))
      .ignoreExceptions()
      .untilAsserted(() -> {
        String msg = storageService.downloadAsString(
          properties.bucket(),
          message.uuid().toString()
        );
        assertThat(msg).isEqualTo("Hello World");
      });
  }
}
```

Here's what the test does:

* `@SpringBootTest` starts the full Spring application context.
* The Testcontainers JUnit 5 annotations `@Testcontainers` and `@Container` manage the lifecycle of a `LocalStackContainer` instance.
* `@DynamicPropertySource` obtains the dynamic S3 and SQS endpoint URLs, region, access key, and secret key from the container, and registers them as Spring Cloud AWS configuration properties.
* `@BeforeAll` creates the required SQS queue and S3 bucket using the `awslocal` CLI tool that comes pre-installed in the LocalStack Docker image. The `localStack.execInContainer()` API runs commands inside the container.
* `shouldHandleMessageSuccessfully()` publishes a `Message` to the SQS queue. The listener receives the message and stores its content in the S3 bucket with the UUID as the key. Awaitility waits up to 10 seconds for the expected content to appear in the bucket.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-java-aws-localstack/run-tests/)

----
url: https://docs.docker.com/billing/details/
----

# Manage your billing information

***

Table of contents

***

You can update the billing information for your personal account or for an organization. When you update your billing information, these changes apply to future billing invoices. The email address you provide for a billing account is where Docker sends all invoices and other billing related communications.

> Note
>
> Existing invoices, whether paid or unpaid, cannot be updated. Changes only apply to future invoices.

## [Manage billing information](#manage-billing-information)

### [Personal account](#personal-account)

To update your billing information:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.

2. Select **Billing**.

3. Select **Billing information** from the left-hand navigation.

4. On your billing information card, select **Change**.

5. Update your billing contact and billing address information.

6. Optional. To add or update a VAT ID, select the **I'm purchasing as a business** checkbox and enter your Tax ID.

   > Important
   >
   > Your VAT number must include your country prefix. For example, if you are entering a VAT number for Germany, you would enter `DE123456789`.

7. Select **Update**.

### [Organization](#organization)

> Note
>
> You must be an organization owner to make changes to the billing information.

To update your billing information:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.

2. Select **Billing**.

3. Select **Billing information** from the left-hand navigation.

4. On your billing information card, select **Change**.

5. Update your billing contact and billing address information.

6. Optional. To add or update a VAT ID, select the **I'm purchasing as a business** checkbox and enter your Tax ID.

   > Important
   >
   > Your VAT number must include your country prefix. For example, if you are entering a VAT number for Germany, you would enter `DE123456789`.

7. Select **Update**.

## [Update your billing email address](#update-your-billing-email-address)

Docker sends the following billing-related emails:

* Confirmations (new subscriptions, paid invoices)
* Notifications (card failure, card expiration)
* Reminders (subscription renewal)

You can update the email address that receives billing invoices at any time.

### [Personal account](#personal-account-1)

To update your billing email address:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand navigation.
4. On your billing information card, select **Change**.
5. Update your billing contact information and select **Update**.

### [Organizations](#organizations)

To update your billing email address:

1. Sign in to [Docker Home](https://app.docker.com/) and select your organization.
2. Select **Billing**.
3. Select **Billing information** from the left-hand navigation.
4. On your billing information card, select **Change**.
5. Update your billing contact information and select **Update**.

----
url: https://docs.docker.com/reference/cli/docker/sandbox/create/
----

# docker sandbox create

***

| Description | Create a sandbox for an agent                     |
| ----------- | ------------------------------------------------- |
| Usage       | `docker sandbox create [OPTIONS] AGENT WORKSPACE` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Create a sandbox with access to a host workspace for an agent.

Available agents are provided as subcommands. Use "create AGENT --help" for agent-specific options.

## [Options](#options)

| Option                        | Default   | Description                                                                                                                        |
| ----------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `--name`                      |           | Name for the sandbox (default: -, letters, numbers, hyphens, underscores, periods, plus signs and minus signs only)                |
| `--pull-template`             | `missing` | Template image pull policy: always (always pull from registry), missing (pull only if not cached), never (use only cached images)  |
| `-q, --quiet`                 |           | Suppress verbose output                                                                                                            |
| [`-t, --template`](#template) |           | Container image to use for the sandbox (default: agent-specific image)                                                             |

## [Examples](#examples)

### [Create a Claude sandbox](#create-a-claude-sandbox)

```console
$ docker sandbox create claude ~/my-project
```

### [Create with a custom name](#create-with-a-custom-name)

```console
$ docker sandbox create --name my-sandbox claude ~/my-project
```

### [Use a custom base image (-t, --template)](#template)

```text
--template IMAGE
```

Specify a custom container image to use as the sandbox base:

```console
$ docker sandbox create --template python:3-alpine claude ~/my-project
```

By default, each agent uses a pre-configured image.

### [Create and run immediately](#create-and-run-immediately)

After creating a sandbox, use `run` to start the agent:

```console
$ docker sandbox create --name my-sandbox claude ~/my-project
$ docker sandbox run my-sandbox
```

Or use `docker sandbox run` directly to create and run in one step:

```console
$ docker sandbox run claude ~/my-project
```

## [Subcommands](#subcommands)

| Command                                                                                                   | Description                   |
| --------------------------------------------------------------------------------------------------------- | ----------------------------- |
| [`docker sandbox create cagent`](https://docs.docker.com/reference/cli/docker/sandbox/create/cagent/)     | Create a sandbox for cagent   |
| [`docker sandbox create claude`](https://docs.docker.com/reference/cli/docker/sandbox/create/claude/)     | Create a sandbox for claude   |
| [`docker sandbox create codex`](https://docs.docker.com/reference/cli/docker/sandbox/create/codex/)       | Create a sandbox for codex    |
| [`docker sandbox create copilot`](https://docs.docker.com/reference/cli/docker/sandbox/create/copilot/)   | Create a sandbox for copilot  |
| [`docker sandbox create gemini`](https://docs.docker.com/reference/cli/docker/sandbox/create/gemini/)     | Create a sandbox for gemini   |
| [`docker sandbox create kiro`](https://docs.docker.com/reference/cli/docker/sandbox/create/kiro/)         | Create a sandbox for kiro     |
| [`docker sandbox create opencode`](https://docs.docker.com/reference/cli/docker/sandbox/create/opencode/) | Create a sandbox for opencode |
| [`docker sandbox create shell`](https://docs.docker.com/reference/cli/docker/sandbox/create/shell/)       | Create a sandbox for shell    |

----
url: https://docs.docker.com/extensions/extensions-sdk/dev/api/overview/
----

# Extension UI API

***

***

The extensions UI runs in a sandboxed environment and doesn't have access to any electron or nodejs APIs.

The extension UI API provides a way for the frontend to perform different actions and communicate with the Docker Desktop dashboard or the underlying system.

JavaScript API libraries, with Typescript support, are available in order to get all the API definitions in to your extension code.

* [@docker/extension-api-client](https://www.npmjs.com/package/@docker/extension-api-client) gives access to the extension API entrypoint `DockerDesktopClient`.
* [@docker/extension-api-client-types](https://www.npmjs.com/package/@docker/extension-api-client-types) can be added as a dev dependency in order to get types auto-completion in your IDE.

```Typescript
import { createDockerDesktopClient } from '@docker/extension-api-client';

export function App() {
  // obtain Docker Desktop client
  const ddClient = createDockerDesktopClient();
  // use ddClient to perform extension actions
}
```

The `ddClient` object gives access to various APIs:

* [Extension Backend](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/)
* [Docker](https://docs.docker.com/extensions/extensions-sdk/dev/api/docker/)
* [Dashboard](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard/)
* [Navigation](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard-routes-navigation/)

See also the [Extensions API reference](https://docs.docker.com/reference/api/extensions-sdk/).

----
url: https://docs.docker.com/reference/api/engine/version/v1.54.yaml
----

basePath: "/v1.54"
info:
 title: "Docker Engine API"
 version: "1.54"

 For example, calling \`/info\` is the same as calling \`/v1.52/info\`. Using the
 API without a version-prefix is deprecated and will be removed in a future release.

 Engine releases in the near future should support this version of the API,
 so your client will continue to work even if it is talking to a newer Engine.

 The API uses an open schema model, which means the server may add extra properties
 to responses. Likewise, the server will ignore any extra query parameters and
 request body properties. When you write clients, you need to ignore additional
 properties in responses to ensure they do not break when talking to newer
 daemons.

 # Authentication

 Authentication for registries is handled client side. The client has to send
 authentication details to various endpoints that need to communicate with
 registries, such as \`POST /images/(name)/push\`. These are sent as
 \`X-Registry-Auth\` header as a \[base64url encoded\](https://tools.ietf.org/html/rfc4648#section-5)
 (JSON) string with the following structure:

 \`\`\`
 {
 "username": "string",
 "password": "string",
 "serveraddress": "string"
 }
 \`\`\`

 The \`serveraddress\` is a domain/IP without a protocol. Throughout this
 structure, double quotes are required.

 If you have already got an identity token from the \[\`/auth\` endpoint\](#operation/SystemAuth),
 you can just pass this instead of credentials:

 \`\`\`
 {
 "identitytoken": "9cbaf023786cd7..."
 }
 \`\`\`

\# The tags on paths define the menu sections in the ReDoc documentation, so
\# the usage of tags must make sense for that:
\# - They should be singular, not plural.
\# - There should not be too many tags, or the menu becomes unwieldy. For
\# example, it is preferable to add a path to the "System" tag instead of
\# creating a tag with a single path in it.
\# - The order of tags in this list defines the order in the menu.
tags:
 # Primary objects
 \- name: "Container"
 x-displayName: "Containers"
 description: \|
 Create and manage containers.
 \- name: "Image"
 x-displayName: "Images"
 \- name: "Network"
 x-displayName: "Networks"
 description: \|
 Networks are user-defined networks that containers can be attached to.
 See the \[networking documentation\](https://docs.docker.com/network/)
 for more information.
 \- name: "Volume"
 x-displayName: "Volumes"
 description: \|
 Create and manage persistent storage that can be attached to containers.
 \- name: "Exec"
 x-displayName: "Exec"
 description: \|
 Run new commands inside running containers. Refer to the
 \[command-line reference\](https://docs.docker.com/engine/reference/commandline/exec/)
 for more information.

 To exec a command in a container, you first need to create an exec instance,
 then start it. These two API endpoints are wrapped up in a single command-line
 command, \`docker exec\`.

 # Swarm things
 \- name: "Swarm"
 x-displayName: "Swarm"
 description: \|
 Engines can be clustered together in a swarm. Refer to the
 \[swarm mode documentation\](https://docs.docker.com/engine/swarm/)
 for more information.
 \- name: "Node"
 x-displayName: "Nodes"
 description: \|
 Nodes are instances of the Engine participating in a swarm. Swarm mode
 must be enabled for these endpoints to work.
 \- name: "Service"
 x-displayName: "Services"
 description: \|
 Services are the definitions of tasks to run on a swarm. Swarm mode must
 be enabled for these endpoints to work.
 \- name: "Task"
 x-displayName: "Tasks"
 description: \|
 A task is a container running on a swarm. It is the atomic scheduling unit
 of swarm. Swarm mode must be enabled for these endpoints to work.
 \- name: "Secret"
 x-displayName: "Secrets"
 description: \|
 Secrets are sensitive data that can be used by services. Swarm mode must
 be enabled for these endpoints to work.
 \- name: "Config"
 x-displayName: "Configs"
 description: \|
 Configs are application configurations that can be used by services. Swarm
 mode must be enabled for these endpoints to work.
 # System things
 \- name: "Plugin"
 x-displayName: "Plugins"
 \- name: "System"
 x-displayName: "System"

definitions:
 ImageHistoryResponseItem:
 type: "object"
 x-go-name: HistoryResponseItem
 title: "HistoryResponseItem"
 description: "individual image layer information in response to ImageHistory operation"
 required: \[Id, Created, CreatedBy, Tags, Size, Comment\]
 properties:
 Id:
 type: "string"
 x-nullable: false
 Created:
 type: "integer"
 format: "int64"
 x-nullable: false
 CreatedBy:
 type: "string"
 x-nullable: false
 Tags:
 type: "array"
 items:
 type: "string"
 Size:
 type: "integer"
 format: "int64"
 x-nullable: false
 Comment:
 type: "string"
 x-nullable: false
 PortSummary:
 type: "object"
 description: \|
 Describes a port-mapping between the container and the host.
 required: \[PrivatePort, Type\]
 properties:
 IP:
 type: "string"
 format: "ip-address"
 description: "Host IP address that the container's port is mapped to"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 PrivatePort:
 type: "integer"
 format: "uint16"
 x-nullable: false
 description: "Port on the container"
 PublicPort:
 type: "integer"
 format: "uint16"
 description: "Port exposed on the host"
 Type:
 type: "string"
 x-nullable: false
 enum: \["tcp", "udp", "sctp"\]
 example:
 PrivatePort: 8080
 PublicPort: 80
 Type: "tcp"

 MountType:
 description: \|-
 The mount type. Available types:

 \- \`bind\` a mount of a file or directory from the host into the container.
 \- \`cluster\` a Swarm cluster volume.
 \- \`image\` an OCI image.
 \- "image"

 \- \`image\` an OCI image.
 \- \`npipe\` a named pipe from the host into the container.
 \- \`tmpfs\` a \`tmpfs\`.
 \- \`volume\` a docker volume with the given \`Name\`.
 allOf:
 \- $ref: "#/definitions/MountType"
 example: "volume"
 Name:
 description: \|
 Name is the name reference to the underlying data defined by \`Source\`
 e.g., the volume name.
 type: "string"
 example: "myvolume"
 Source:
 description: \|
 Source location of the mount.

 For volumes, this contains the storage location of the volume (within
 \`/var/lib/docker/volumes/\`). For bind-mounts, and \`npipe\`, this contains
 the source (host) part of the bind-mount. For \`tmpfs\` mount points, this
 field is empty.
 type: "string"
 example: "/var/lib/docker/volumes/myvolume/\_data"
 Destination:
 description: \|
 Destination is the path relative to the container root (\`/\`) where
 the \`Source\` is mounted inside the container.
 type: "string"
 example: "/usr/share/nginx/html/"
 Driver:
 description: \|
 Driver is the volume driver used to create the volume (if it is a volume).
 type: "string"
 example: "local"
 Mode:
 description: \|
 Mode is a comma separated list of options supplied by the user when
 creating the bind/volume mount.

 The default is platform-specific (\`"z"\` on Linux, empty on Windows).
 type: "string"
 example: "z"
 RW:
 description: \|
 Whether the mount is mounted writable (read-write).
 type: "boolean"
 example: true
 Propagation:
 description: \|
 Propagation describes how mounts are propagated from the host into the
 mount point, and vice-versa. Refer to the \[Linux kernel documentation\](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt)
 for details. This field is not used on Windows.
 type: "string"
 example: ""

 DeviceMapping:
 type: "object"
 description: "A device mapping between the host and container"
 properties:
 PathOnHost:
 type: "string"
 PathInContainer:
 type: "string"
 CgroupPermissions:
 type: "string"
 example:
 PathOnHost: "/dev/deviceName"
 PathInContainer: "/dev/deviceName"
 CgroupPermissions: "mrw"

 DeviceRequest:
 type: "object"
 description: "A request for devices to be sent to device drivers"
 properties:
 Driver:
 description: \|
 The name of the device driver to use for this request.

 Note that if this is specified the capabilities are ignored when
 selecting a device driver.
 type: "string"
 example: "nvidia"
 Count:
 type: "integer"
 example: -1
 DeviceIDs:
 type: "array"
 items:
 type: "string"
 example:
 \- "0"
 \- "1"
 \- "GPU-fef8089b-4820-abfc-e83e-94318197576e"
 Capabilities:
 description: \|
 A list of capabilities; an OR list of AND lists of capabilities.

 Note that if a driver is specified the capabilities have no effect on
 selecting a driver as the driver name is used directly.

 Note that if no driver is specified the capabilities are used to
 select a driver with the required capabilities.
 type: "array"
 items:
 type: "array"
 items:
 type: "string"
 example:
 # gpu AND nvidia AND compute
 \- \["gpu", "nvidia", "compute"\]
 Options:
 description: \|
 Driver-specific options, specified as a key/value pairs. These options
 are passed directly to the driver.
 type: "object"
 additionalProperties:
 type: "string"

 ThrottleDevice:
 type: "object"
 properties:
 Path:
 description: "Device path"
 type: "string"
 Rate:
 description: "Rate"
 type: "integer"
 format: "int64"
 minimum: 0

 Mount:
 type: "object"
 properties:
 Target:
 description: "Container path."
 type: "string"
 Source:
 description: \|-
 Mount source (e.g. a volume name, a host path). The source cannot be
 specified when using \`Type=tmpfs\`. For \`Type=bind\`, the source path

 \- \`image\` Mounts an image.
 type: "boolean"
 default: false
 ReadOnlyNonRecursive:
 description: \|
 Make the mount non-recursively read-only, but still leave the mount recursive

 ImageOptions:
 description: "Optional configuration for the \`image\` type."
 type: "object"
 properties:
 Subpath:
 description: "Source path inside the image. Must be relative without any back traversals."
 type: "string"
 example: "dir-inside-image/subdirectory"
 TmpfsOptions:
 description: "Optional configuration for the \`tmpfs\` type."
 type: "object"
 properties:
 SizeBytes:
 description: "The size for the tmpfs mount in bytes."
 type: "integer"
 format: "int64"
 Mode:
 description: \|
 The permission mode for the tmpfs mount in an integer.
 The value must not be in octal format (e.g. 755) but rather
 the decimal representation of the octal value (e.g. 493).
 type: "integer"
 Options:
 description: \|
 The options to be passed to the tmpfs mount. An array of arrays.
 Flag options should be provided as 1-length arrays. Other types
 should be provided as as 2-length arrays, where the first item is
 the key and the second the value.
 type: "array"
 items:
 type: "array"
 minItems: 1
 maxItems: 2
 items:
 type: "string"
 example:
 \[\["noexec"\]\]

 RestartPolicy:
 description: \|
 The behavior to apply when the container exits. The default is not to
 restart.

 An ever increasing delay (double the previous delay, starting at 100ms) is
 added before each restart to prevent flooding the server.
 type: "object"
 properties:
 Name:
 type: "string"
 description: \|
 \- Empty string means not to restart
 \- \`no\` Do not automatically restart
 \- \`always\` Always restart
 \- \`unless-stopped\` Restart always except when the user has manually stopped the container
 \- \`on-failure\` Restart only when the container exit code is non-zero
 enum:
 \- ""
 \- "no"
 \- "always"
 \- "unless-stopped"
 \- "on-failure"
 MaximumRetryCount:
 type: "integer"
 description: \|
 If \`on-failure\` is used, the number of times to retry before giving up.

 Resources:
 description: "A container's resources (cgroups config, ulimits, etc)"
 type: "object"
 properties:
 # Applicable to all platforms
 CpuShares:
 description: \|
 An integer value representing this container's relative CPU weight
 versus other containers.
 type: "integer"
 Memory:
 description: "Memory limit in bytes."
 type: "integer"
 format: "int64"
 default: 0
 # Applicable to UNIX platforms
 CgroupParent:
 description: \|
 Path to \`cgroups\` under which the container's \`cgroup\` is created. If
 the path is not absolute, the path is considered to be relative to the
 \`cgroups\` path of the init process. Cgroups are created if they do not
 already exist.
 type: "string"
 BlkioWeight:
 description: "Block IO weight (relative weight)."
 type: "integer"
 minimum: 0
 maximum: 1000
 BlkioWeightDevice:
 description: \|
 Block IO weight (relative device weight) in the form:

 \`\`\`
 \[{"Path": "device\_path", "Weight": weight}\]
 \`\`\`
 type: "array"
 items:
 type: "object"
 properties:
 Path:
 type: "string"
 Weight:
 type: "integer"
 minimum: 0
 BlkioDeviceReadBps:
 description: \|
 Limit read rate (bytes per second) from a device, in the form:

 \`\`\`
 \[{"Path": "device\_path", "Rate": rate}\]
 \`\`\`
 type: "array"
 items:
 $ref: "#/definitions/ThrottleDevice"
 BlkioDeviceWriteBps:
 description: \|
 Limit write rate (bytes per second) to a device, in the form:

 \`\`\`
 \[{"Path": "device\_path", "Rate": rate}\]
 \`\`\`
 type: "array"
 items:
 $ref: "#/definitions/ThrottleDevice"
 BlkioDeviceReadIOps:
 description: \|
 Limit read rate (IO per second) from a device, in the form:

 \`\`\`
 \[{"Path": "device\_path", "Rate": rate}\]
 \`\`\`
 type: "array"
 items:
 $ref: "#/definitions/ThrottleDevice"
 BlkioDeviceWriteIOps:
 description: \|
 Limit write rate (IO per second) to a device, in the form:

 \`\`\`
 \[{"Path": "device\_path", "Rate": rate}\]
 \`\`\`
 type: "array"
 items:
 $ref: "#/definitions/ThrottleDevice"
 CpuPeriod:
 description: "The length of a CPU period in microseconds."
 type: "integer"
 format: "int64"
 CpuQuota:
 description: \|
 Microseconds of CPU time that the container can get in a CPU period.
 type: "integer"
 format: "int64"
 CpuRealtimePeriod:
 description: \|
 The length of a CPU real-time period in microseconds. Set to 0 to
 allocate no time allocated to real-time tasks.
 type: "integer"
 format: "int64"
 CpuRealtimeRuntime:
 description: \|
 The length of a CPU real-time runtime in microseconds. Set to 0 to
 allocate no time allocated to real-time tasks.
 type: "integer"
 format: "int64"
 CpusetCpus:
 description: \|
 CPUs in which to allow execution (e.g., \`0-3\`, \`0,1\`).
 type: "string"
 example: "0-3"
 CpusetMems:
 description: \|
 Memory nodes (MEMs) in which to allow execution (0-3, 0,1). Only
 effective on NUMA systems.
 type: "string"
 Devices:
 description: "A list of devices to add to the container."
 type: "array"
 items:
 $ref: "#/definitions/DeviceMapping"
 DeviceCgroupRules:
 description: "a list of cgroup rules to apply to the container"
 type: "array"
 items:
 type: "string"
 example: "c 13:\* rwm"
 DeviceRequests:
 description: \|
 A list of requests for devices to be sent to device drivers.
 type: "array"
 items:
 $ref: "#/definitions/DeviceRequest"


 ResourceObject:
 description: \|
 An object describing the resources which can be advertised by a node and
 requested by a task.
 type: "object"
 properties:
 NanoCPUs:
 type: "integer"
 format: "int64"
 example: 4000000000
 MemoryBytes:
 type: "integer"
 format: "int64"
 example: 8272408576
 GenericResources:
 $ref: "#/definitions/GenericResources"

 GenericResources:
 description: \|
 User-defined resources can be either Integer resources (e.g, \`SSD=3\`) or
 String resources (e.g, \`GPU=UUID1\`).
 type: "array"
 items:
 type: "object"
 properties:
 NamedResourceSpec:
 type: "object"
 properties:
 Kind:
 type: "string"
 Value:
 type: "string"
 DiscreteResourceSpec:
 type: "object"
 properties:
 Kind:
 type: "string"
 Value:
 type: "integer"
 format: "int64"
 example:

 HealthConfig:
 description: \|
 A test to perform to check that the container is healthy.
 Healthcheck commands should be side-effect free.
 type: "object"
 properties:
 Test:
 description: \|
 The test to perform. Possible values are:

 \- \`\[\]\` inherit healthcheck from image or parent image
 \- \`\["NONE"\]\` disable healthcheck
 \- \`\["CMD", args...\]\` exec arguments directly
 \- \`\["CMD-SHELL", command\]\` run command with system's default shell

 A non-zero exit code indicates a failed healthcheck:
 \- \`0\` healthy
 \- \`1\` unhealthy
 \- \`2\` reserved (treated as unhealthy)
 \- other values: error running probe
 type: "array"
 items:
 type: "string"
 Interval:
 description: \|
 The time to wait between checks in nanoseconds. It should be 0 or at
 least 1000000 (1 ms). 0 means inherit.
 type: "integer"
 format: "int64"
 Timeout:
 description: \|
 The time to wait before considering the check to have hung. It should
 be 0 or at least 1000000 (1 ms). 0 means inherit.

 If the health check command does not complete within this timeout,
 the check is considered failed and the health check process is
 forcibly terminated without a graceful shutdown.
 type: "integer"
 format: "int64"
 Retries:
 description: \|
 The number of consecutive failures needed to consider a container as
 unhealthy. 0 means inherit.
 type: "integer"
 StartPeriod:
 description: \|
 Start period for the container to initialize before starting
 health-retries countdown in nanoseconds. It should be 0 or at least
 1000000 (1 ms). 0 means inherit.
 type: "integer"
 format: "int64"
 StartInterval:
 description: \|
 The time to wait between checks in nanoseconds during the start period.
 It should be 0 or at least 1000000 (1 ms). 0 means inherit.
 type: "integer"
 format: "int64"

 Health:
 description: \|
 Health stores information about the container's healthcheck results.
 type: "object"
 x-nullable: true
 properties:
 Status:
 description: \|
 Status is one of \`none\`, \`starting\`, \`healthy\` or \`unhealthy\`

 \- "none" Indicates there is no healthcheck
 \- "starting" Starting indicates that the container is not yet ready
 \- "healthy" Healthy indicates that the container is running correctly
 \- "unhealthy" Unhealthy indicates that the container has a problem
 type: "string"
 Log:
 type: "array"
 description: \|
 Log contains the last few results (oldest first)
 items:
 $ref: "#/definitions/HealthcheckResult"

 HealthcheckResult:
 description: \|
 HealthcheckResult stores information about a single run of a healthcheck probe
 type: "object"
 x-nullable: true
 properties:
 Start:
 description: \|
 Date and time at which this check started in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "date-time"
 example: "2020-01-04T10:44:24.496525531Z"
 End:
 description: \|
 Date and time at which this check ended in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.
 type: "string"
 format: "dateTime"
 example: "2020-01-04T10:45:21.364524523Z"
 ExitCode:
 description: \|
 ExitCode meanings:

 \- \`0\` healthy
 \- \`1\` unhealthy
 \- \`2\` reserved (considered unhealthy)
 \- other values: error running probe
 type: "integer"
 example: 0
 Output:
 description: "Output from last check"
 type: "string"

 HostConfig:
 description: "Container configuration that depends on the host we are running on"
 allOf:
 \- $ref: "#/definitions/Resources"
 \- type: "object"
 properties:
 # Applicable to all platforms
 Binds:
 type: "array"
 description: \|
 A list of volume bindings for this container. Each volume binding
 is a string in one of these forms:

 \- \`host-src:container-dest\[:options\]\` to bind-mount a host path
 into the container. Both \`host-src\`, and \`container-dest\` must
 be an \_absolute\_ path.
 \- \`volume-name:container-dest\[:options\]\` to bind-mount a volume
 managed by a volume driver into the container. \`container-dest\`
 must be an \_absolute\_ path.

 \`options\` is an optional, comma-delimited list of:

 \- \`nocopy\` disables automatic copying of data from the container
 path to the volume. The \`nocopy\` flag only applies to named volumes.
 \- \`\[ro\|rw\]\` mounts a volume read-only or read-write, respectively.
 If omitted or set to \`rw\`, volumes are mounted read-write.
 \- \`\[z\|Z\]\` applies SELinux labels to allow or deny multiple containers
 to read and write to the same volume.
 \- \`z\`: a \_shared\_ content label is applied to the content. This
 label indicates that multiple containers can share the volume
 content, for both reading and writing.
 \- \`Z\`: a \_private unshared\_ label is applied to the content.
 This label indicates that only the current container can use
 a private volume. Labeling systems such as SELinux require
 proper labels to be placed on volume content that is mounted
 into a container. Without a label, the security system can
 prevent a container's processes from using the content. By
 default, the labels set by the host operating system are not
 modified.
 \- \`\[\[r\]shared\|\[r\]slave\|\[r\]private\]\` specifies mount
 \[propagation behavior\](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt).
 This only applies to bind-mounted volumes, not internal volumes
 or named volumes. Mount propagation requires the source mount
 point (the location where the source directory is mounted in the
 host operating system) to have the correct propagation properties.
 For shared volumes, the source mount point must be set to \`shared\`.
 For slave volumes, the mount must be set to either \`shared\` or
 \`slave\`.
 items:
 type: "string"
 ContainerIDFile:
 type: "string"
 description: "Path to a file where the container ID is written"
 example: ""
 LogConfig:
 type: "object"
 description: "The logging configuration for this container"
 properties:
 Type:
 description: \|-
 Name of the logging driver used for the container or "none"
 if logging is disabled.
 type: "string"
 enum:
 \- "local"
 \- "json-file"
 \- "syslog"
 \- "journald"
 \- "gelf"
 \- "fluentd"
 \- "awslogs"
 \- "splunk"
 \- "etwlogs"
 \- "none"
 Config:
 description: \|-
 Driver-specific configuration options for the logging driver.
 type: "object"
 additionalProperties:
 type: "string"
 example:
 "max-file": "5"
 "max-size": "10m"
 NetworkMode:
 type: "string"
 description: \|
 Network mode to use for this container. Supported standard values
 are: \`bridge\`, \`host\`, \`none\`, and \`container:\`. Any
 other value is taken as a custom network's name to which this
 container should connect to.
 PortBindings:
 $ref: "#/definitions/PortMap"
 RestartPolicy:
 $ref: "#/definitions/RestartPolicy"
 AutoRemove:
 type: "boolean"
 description: \|
 Automatically remove the container when the container's process
 exits. This has no effect if \`RestartPolicy\` is set.
 VolumeDriver:
 type: "string"
 description: "Driver that this container uses to mount volumes."
 VolumesFrom:
 type: "array"
 description: \|
 A list of volumes to inherit from another container, specified in
 the form \`\[:\]\`.
 items:
 type: "string"
 Mounts:
 description: \|
 Specification for mounts to be added to the container.
 type: "array"
 items:
 $ref: "#/definitions/Mount"
 example: \[80, 64\]

 Dns:
 type: "array"
 description: "A list of DNS servers for the container to use."
 items:
 type: "string"
 format: "ip-address"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 DnsOptions:
 type: "array"
 description: "A list of DNS options."
 items:
 type: "string"
 DnsSearch:
 type: "array"
 description: "A list of DNS search domains."
 items:
 type: "string"
 ExtraHosts:
 type: "array"
 description: \|
 A list of hostnames/IP mappings to add to the container's \`/etc/hosts\`
 file. Specified in the form \`\["hostname:IP"\]\`.
 items:
 type: "string"
 GroupAdd:
 type: "array"
 description: \|
 A list of additional groups that the container process will run as.
 items:
 type: "string"
 IpcMode:
 type: "string"
 description: \|
 IPC sharing mode for the container. Possible values are:

 \- \`"none"\`: own private IPC namespace, with /dev/shm not mounted
 \- \`"private"\`: own private IPC namespace
 \- \`"shareable"\`: own private IPC namespace, with a possibility to share it with other containers
 \- \`"container:"\`: join another (shareable) container's IPC namespace
 \- \`"host"\`: use the host system's IPC namespace

 If not specified, daemon default is used, which can either be \`"private"\`
 or \`"shareable"\`, depending on daemon version and configuration.
 Cgroup:
 type: "string"
 description: "Cgroup to use for the container."
 Links:
 type: "array"
 description: \|
 A list of links for the container in the form \`container\_name:alias\`.
 items:
 type: "string"
 OomScoreAdj:
 type: "integer"
 description: \|
 An integer value containing the score given to the container in
 order to tune OOM killer preferences.
 example: 500
 PidMode:
 type: "string"
 description: \|
 Set the PID (Process) Namespace mode for the container. It can be
 either:

 \- \`"container:"\`: joins another container's PID namespace
 \- \`"host"\`: use the host's PID namespace inside the container
 Privileged:
 type: "boolean"
 description: \|-
 Gives the container full access to the host.
 PublishAllPorts:
 type: "boolean"
 description: \|
 Allocates an ephemeral host port for all of a container's
 exposed ports.

 Ports are de-allocated when the container stops and allocated when
 the container starts. The allocated port might be changed when
 restarting the container.

 The port is selected from the ephemeral port range that depends on
 the kernel. For example, on Linux the range is defined by
 \`/proc/sys/net/ipv4/ip\_local\_port\_range\`.
 ReadonlyRootfs:
 type: "boolean"
 description: "Mount the container's root filesystem as read only."
 SecurityOpt:
 type: "array"
 description: \|
 A list of string values to customize labels for MLS systems, such
 as SELinux.
 items:
 type: "string"
 StorageOpt:
 type: "object"
 description: \|
 Storage driver options for this container, in the form \`{"size": "120G"}\`.
 additionalProperties:
 type: "string"
 Tmpfs:
 type: "object"
 description: \|
 A map of container directories which should be replaced by tmpfs
 mounts, and their corresponding mount options. For example:

 \`\`\`
 { "/run": "rw,noexec,nosuid,size=65536k" }
 \`\`\`
 additionalProperties:
 type: "string"
 UTSMode:
 type: "string"
 description: "UTS namespace to use for the container."
 UsernsMode:
 type: "string"
 description: \|
 Sets the usernamespace mode for the container when usernamespace
 remapping option is enabled.
 ShmSize:
 type: "integer"
 format: "int64"
 description: \|
 Size of \`/dev/shm\` in bytes. If omitted, the system uses 64MB.
 minimum: 0
 Sysctls:
 type: "object"
 x-nullable: true
 description: \|-
 A list of kernel parameters (sysctls) to set in the container.

 This field is omitted if not set.
 additionalProperties:
 type: "string"
 example:
 "net.ipv4.ip\_forward": "1"
 Runtime:
 type: "string"
 x-nullable: true
 description: \|-
 Runtime to use with this container.
 # Applicable to Windows
 Isolation:
 type: "string"
 description: \|
 Isolation technology of the container. (Windows only)
 enum:
 \- "default"
 \- "process"
 \- "hyperv"
 \- ""
 MaskedPaths:
 type: "array"
 description: \|
 The list of paths to be masked inside the container (this overrides
 the default set of paths).
 items:
 type: "string"
 example:
 \- "/proc/asound"
 \- "/proc/acpi"
 \- "/proc/kcore"
 \- "/proc/keys"
 \- "/proc/latency\_stats"
 \- "/proc/timer\_list"
 \- "/proc/timer\_stats"
 \- "/proc/sched\_debug"
 \- "/proc/scsi"
 \- "/sys/firmware"
 \- "/sys/devices/virtual/powercap"
 ReadonlyPaths:
 type: "array"
 description: \|
 The list of paths to be set as read-only inside the container
 (this overrides the default set of paths).
 items:
 type: "string"
 example:
 \- "/proc/bus"
 \- "/proc/fs"
 \- "/proc/irq"
 \- "/proc/sys"
 \- "/proc/sysrq-trigger"

 ContainerConfig:
 description: \|
 Configuration for a container that is portable between hosts.
 type: "object"
 properties:
 Hostname:
 description: \|
 The hostname to use for the container, as a valid RFC 1123 hostname.
 type: "string"
 example: "439f4e91bd1d"
 Domainname:
 description: \|
 The domain name to use for the container.
 type: "string"
 User:
 description: \|-
 Commands run as this user inside the container. If omitted, commands
 run as the user specified in the image the container was started from.

 Can be either user-name or UID, and optional group-name or GID,
 separated by a colon (\`\[<:group-name\|GID>\]\`).
 type: "string"
 example: "123:456"
 AttachStdin:
 description: "Whether to attach to \`stdin\`."
 type: "boolean"
 default: false
 AttachStdout:
 description: "Whether to attach to \`stdout\`."
 type: "boolean"
 default: true
 AttachStderr:
 description: "Whether to attach to \`stderr\`."
 type: "boolean"
 default: true
 ExposedPorts:
 description: \|
 An object mapping ports to an empty object in the form:

 \`{"/": {}}\`
 type: "object"
 x-nullable: true
 additionalProperties:
 type: "object"
 enum:
 \- {}
 default: {}
 example: {
 "80/tcp": {},
 "443/tcp": {}
 }
 Tty:
 description: \|
 Attach standard streams to a TTY, including \`stdin\` if it is not closed.
 type: "boolean"
 default: false
 OpenStdin:
 description: "Open \`stdin\`"
 type: "boolean"
 default: false
 StdinOnce:
 description: "Close \`stdin\` after one attached client disconnects"
 type: "boolean"
 default: false
 Env:
 description: \|
 A list of environment variables to set inside the container in the
 form \`\["VAR=value", ...\]\`. A variable without \`=\` is removed from the
 environment, rather than to have an empty value.
 type: "array"
 items:
 type: "string"
 example:
 \- "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
 Cmd:
 description: \|
 Command to run specified as a string or an array of strings.
 type: "array"
 items:
 type: "string"
 example: \["/bin/sh"\]
 Healthcheck:
 $ref: "#/definitions/HealthConfig"
 ArgsEscaped:
 description: "Command is already escaped (Windows only)"
 type: "boolean"
 default: false
 example: false
 x-nullable: true
 Image:
 description: \|
 The name (or reference) of the image to use when creating the container,
 or which was used when the container was created.
 type: "string"
 example: "example-image:1.0"
 Volumes:
 description: \|
 An object mapping mount point paths inside the container to empty
 objects.
 type: "object"
 additionalProperties:
 type: "object"
 enum:
 \- {}
 default: {}
 WorkingDir:
 description: "The working directory for commands to run in."
 type: "string"
 example: "/public/"
 Entrypoint:
 description: \|
 The entry point for the container as a string or an array of strings.

 If the array consists of exactly one empty string (\`\[""\]\`) then the
 entry point is reset to system default (i.e., the entry point used by
 docker when there is no \`ENTRYPOINT\` instruction in the \`Dockerfile\`).
 type: "array"
 items:
 type: "string"
 example: \[\]
 NetworkDisabled:
 description: "Disable networking for the container."
 type: "boolean"
 x-nullable: true
 OnBuild:
 description: \|
 \`ONBUILD\` metadata that were defined in the image's \`Dockerfile\`.
 type: "array"
 x-nullable: true
 items:
 type: "string"
 example: \[\]
 StopSignal:
 description: \|
 Signal to stop a container as a string or unsigned integer.
 type: "string"
 example: "SIGTERM"
 x-nullable: true
 StopTimeout:
 description: "Timeout to stop a container in seconds."
 type: "integer"
 default: 10
 x-nullable: true
 Shell:
 description: \|
 Shell for when \`RUN\`, \`CMD\`, and \`ENTRYPOINT\` uses a shell.
 type: "array"
 x-nullable: true
 items:
 type: "string"
 example: \["/bin/sh", "-c"\]

 ImageConfig:
 description: \|
 Configuration of the image. These fields are used as defaults
 when starting a container from the image.
 type: "object"
 properties:
 User:
 description: "The user that commands are run as inside the container."
 type: "string"
 example: "web:web"
 ExposedPorts:
 description: \|
 An object mapping ports to an empty object in the form:

 \`{"/": {}}\`
 type: "object"
 x-nullable: true
 additionalProperties:
 type: "object"
 enum:
 \- {}
 default: {}
 example: {
 "80/tcp": {},
 "443/tcp": {}
 }
 Env:
 description: \|
 A list of environment variables to set inside the container in the
 form \`\["VAR=value", ...\]\`. A variable without \`=\` is removed from the
 environment, rather than to have an empty value.
 type: "array"
 items:
 type: "string"
 example:
 \- "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
 Cmd:
 description: \|
 Command to run specified as a string or an array of strings.
 type: "array"
 items:
 type: "string"
 example: \["/bin/sh"\]
 Healthcheck:
 $ref: "#/definitions/HealthConfig"
 ArgsEscaped:
 description: "Command is already escaped (Windows only)"
 type: "boolean"
 default: false
 example: false
 x-nullable: true
 Volumes:
 description: \|
 An object mapping mount point paths inside the container to empty
 objects.
 type: "object"
 additionalProperties:
 type: "object"
 enum:
 \- {}
 default: {}
 example:
 "/app/data": {}
 "/app/config": {}
 WorkingDir:
 description: "The working directory for commands to run in."
 type: "string"
 example: "/public/"
 Entrypoint:
 description: \|
 The entry point for the container as a string or an array of strings.

 If the array consists of exactly one empty string (\`\[""\]\`) then the
 entry point is reset to system default (i.e., the entry point used by
 docker when there is no \`ENTRYPOINT\` instruction in the \`Dockerfile\`).
 type: "array"
 items:
 type: "string"
 example: \[\]
 OnBuild:
 description: \|
 \`ONBUILD\` metadata that were defined in the image's \`Dockerfile\`.
 type: "array"
 x-nullable: true
 items:
 type: "string"
 example: \[\]
 StopSignal:
 description: \|
 Signal to stop a container as a string or unsigned integer.
 type: "string"
 example: "SIGTERM"
 x-nullable: true
 Shell:
 description: \|
 Shell for when \`RUN\`, \`CMD\`, and \`ENTRYPOINT\` uses a shell.
 type: "array"
 x-nullable: true
 items:
 type: "string"
 example: \["/bin/sh", "-c"\]

 NetworkingConfig:
 description: \|
 NetworkingConfig represents the container's networking configuration for
 each of its interfaces.
 It is used for the networking configs specified in the \`docker create\`
 and \`docker network connect\` commands.
 type: "object"
 properties:
 EndpointsConfig:
 description: \|
 A mapping of network name to endpoint configuration for that network.
 The endpoint configuration can be left empty to connect to that
 network with no particular endpoint configuration.
 type: "object"
 additionalProperties:
 $ref: "#/definitions/EndpointSettings"
 example:
 # putting an example here, instead of using the example values from
 # /definitions/EndpointSettings, because EndpointSettings contains
 # operational data returned when inspecting a container that we don't
 # accept here.
 EndpointsConfig:
 isolated\_nw:
 IPAMConfig:
 IPv4Address: "172.20.30.33"
 IPv6Address: "2001:db8:abcd::3033"
 LinkLocalIPs:
 \- "169.254.34.68"
 \- "fe80::3468"
 MacAddress: "02:42:ac:12:05:02"
 Links:
 \- "container\_1"
 \- "container\_2"
 Aliases:
 \- "server\_x"
 \- "server\_y"
 database\_nw: {}

 NetworkSettings:
 description: "NetworkSettings exposes the network settings in the API"
 type: "object"
 properties:
 SandboxID:
 description: SandboxID uniquely represents a container's network stack.
 type: "string"
 example: "9d12daf2c33f5959c8bf90aa513e4f65b561738661003029ec84830cd503a0c3"
 SandboxKey:
 description: SandboxKey is the full path of the netns handle
 type: "string"
 example: "/var/run/docker/netns/8ab54b426c38"
 Ports:
 $ref: "#/definitions/PortMap"
 Networks:
 description: \|
 Information about all networks that the container is connected to.
 type: "object"
 additionalProperties:
 $ref: "#/definitions/EndpointSettings"

 Address:
 description: Address represents an IPv4 or IPv6 IP address.
 type: "object"
 properties:
 Addr:
 description: IP address.
 type: "string"
 PrefixLen:
 description: Mask length of the IP address.
 type: "integer"

 PortMap:
 description: \|
 PortMap describes the mapping of container ports to host ports, using the
 container's port-number and protocol as key in the format \`/\`,
 for example, \`80/udp\`.

 If a container's port is mapped for multiple protocols, separate entries
 are added to the mapping table.
 type: "object"
 additionalProperties:
 type: "array"
 x-nullable: true
 items:
 $ref: "#/definitions/PortBinding"
 example:
 "443/tcp":
 \- HostIp: "127.0.0.1"
 HostPort: "4443"
 "80/tcp":
 \- HostIp: "0.0.0.0"
 HostPort: "80"
 \- HostIp: "0.0.0.0"
 HostPort: "8080"
 "80/udp":
 \- HostIp: "0.0.0.0"
 HostPort: "80"
 "53/udp":
 \- HostIp: "0.0.0.0"
 HostPort: "53"
 "2377/tcp": null

 PortBinding:
 description: \|
 PortBinding represents a binding between a host IP address and a host
 port.
 type: "object"
 properties:
 HostIp:
 description: "Host IP address that the container's port is mapped to."
 type: "string"
 example: "127.0.0.1"
 x-go-type:
 type: Addr
 import:
 package: net/netip
 HostPort:
 description: "Host port number that the container's port is mapped to."
 type: "string"
 example: "4443"

 DriverData:
 description: \|
 Information about the storage driver used to store the container's and
 image's filesystem.
 type: "object"
 required: \[Name, Data\]
 properties:
 Name:
 description: "Name of the storage driver."
 type: "string"
 x-nullable: false
 example: "overlay2"
 Data:
 description: \|
 Low-level storage metadata, provided as key/value pairs.

 This information is driver-specific, and depends on the storage-driver
 in use, and should be used for informational purposes only.
 type: "object"
 x-nullable: false
 additionalProperties:
 type: "string"
 example: {
 "MergedDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/merged",
 "UpperDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/diff",
 "WorkDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/work"
 }

 Storage:
 description: \|
 Information about the storage used by the container.
 type: "object"
 properties:
 RootFS:
 description: \|
 Information about the storage used for the container's root filesystem.
 type: "object"
 x-nullable: true
 $ref: "#/definitions/RootFSStorage"

 RootFSStorage:
 description: \|
 Information about the storage used for the container's root filesystem.
 type: "object"
 x-go-name: RootFSStorage
 properties:
 Snapshot:
 description: \|
 Information about the snapshot used for the container's root filesystem.
 type: "object"
 x-nullable: true
 $ref: "#/definitions/RootFSStorageSnapshot"

 RootFSStorageSnapshot:
 description: \|
 Information about a snapshot backend of the container's root filesystem.
 type: "object"
 x-go-name: RootFSStorageSnapshot
 properties:
 Name:
 description: "Name of the snapshotter."
 type: "string"
 x-nullable: false


 ImageInspect:
 description: \|
 Information about an image in the local image cache.
 type: "object"

 Identity:
 description: \|-
 Identity holds information about the identity and origin of the image.
 This is trusted information verified by the daemon and cannot be modified
 by tagging an image to a different name.
 x-nullable: true
 $ref: "#/definitions/Identity"
 Manifests:
 description: \|
 Manifests is a list of image manifests available in this image. It
 provides a more detailed view of the platform-specific image manifests or
 other image-attached data like build attestations.

 Only available if the daemon provides a multi-platform image store
 and the \`manifests\` option is set in the inspect request.

 WARNING: This is experimental and may change at any time without any backward
 compatibility.
 type: "array"
 x-nullable: true
 items:
 $ref: "#/definitions/ImageManifestSummary"

 Identity:
 description: \|
 Identity holds information about the identity and origin of this image.
 For image list responses, this can duplicate Build/Pull fields across
 image manifests, because those parts are image-level metadata.

 \- name: "identity"\
 in: "query"\
 description: "Include \`Identity\` in each manifest summary. Requires \`manifests=1\`."\

----
url: https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/
----

# Interface: DockerCommand

***

Table of contents

***

**`Since`**

0.2.0

## [Properties](#properties)

### [exec](#exec)

• **exec**: [`Exec`](https://docs.docker.com/reference/api/extensions-sdk/Exec/)

----
url: https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/
----

# Writing a Dockerfile

***

Table of contents

***

## [Explanation](#explanation)

A Dockerfile is a text-based document that's used to create a container image. It provides instructions to the image builder on the commands to run, files to copy, startup command, and more.

As an example, the following Dockerfile would produce a ready-to-run Python application:

```dockerfile
FROM python:3.13
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### [Common instructions](#common-instructions)

Some of the most common instructions in a `Dockerfile` include:

* `FROM <image>` - this specifies the base image that the build will extend.
* `WORKDIR <path>` - this instruction specifies the "working directory" or the path in the image where files will be copied and commands will be executed.
* `COPY <host-path> <image-path>` - this instruction tells the builder to copy files from the host and put them into the container image.
* `RUN <command>` - this instruction tells the builder to run the specified command.
* `ENV <name> <value>` - this instruction sets an environment variable that a running container will use.
* `EXPOSE <port-number>` - this instruction sets configuration on the image that indicates a port the image would like to expose.
* `USER <user-or-uid>` - this instruction sets the default user for all subsequent instructions.
* `CMD ["<command>", "<arg1>"]` - this instruction sets the default command a container using this image will run.

To read through all of the instructions or go into greater detail, check out the [Dockerfile reference](https://docs.docker.com/engine/reference/builder/).

## [Try it out](#try-it-out)

Just as you saw with the previous example, a Dockerfile typically follows these steps:

1. Determine your base image
2. Install application dependencies
3. Copy in any relevant source code and/or binaries
4. Configure the final image

In this quick hands-on guide, you'll write a Dockerfile that builds a simple Node.js application. If you're not familiar with JavaScript-based applications, don't worry. It isn't necessary for following along with this guide.

### [Set up](#set-up)

[Download this ZIP file](https://github.com/docker/getting-started-todo-app/archive/refs/heads/build-image-from-scratch.zip) and extract the contents into a directory on your machine.

If you'd rather not download a ZIP file, clone the <https://github.com/docker/getting-started-todo-app> project and checkout the `build-image-from-scratch` branch.

### [Creating the Dockerfile](#creating-the-dockerfile)

Now that you have the project, you’re ready to create the `Dockerfile`.

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.

2. Examine the project.

   Explore the contents of `getting-started-todo-app/app/`. You'll notice that a `Dockerfile` already exists. It is a simple text file that you can open in any text or code editor.

3. Delete the existing `Dockerfile`.

   For this exercise, you'll pretend you're starting from scratch and will create a new `Dockerfile`.

4. Create a file named `Dockerfile` in the `getting-started-todo-app/app/` folder.

   > **Dockerfile file extensions**
   >
   > It's important to note that the `Dockerfile` has *no* file extension. Some editors will automatically add an extension to the file (or complain it doesn't have one).

5. In the `Dockerfile`, define your base image by adding the following line:

   ```dockerfile
   FROM node:22-alpine
   ```

6. Now, define the working directory by using the `WORKDIR` instruction. This will specify where future commands will run and the directory files will be copied inside the container image.

   ```dockerfile
   WORKDIR /app
   ```

7. Copy all of the files from your project on your machine into the container image by using the `COPY` instruction:

   ```dockerfile
   COPY . .
   ```

8. Install the app's dependencies by using the `yarn` CLI and package manager. To do so, run a command using the `RUN` instruction:

   ```dockerfile
   RUN yarn install --production
   ```

9. Finally, specify the default command to run by using the `CMD` instruction:

   ```dockerfile
   CMD ["node", "./src/index.js"]
   ```

   And with that, you should have the following Dockerfile:

   ```dockerfile
   FROM node:22-alpine
   WORKDIR /app
   COPY . .
   RUN yarn install --production
   CMD ["node", "./src/index.js"]
   ```

> **This Dockerfile isn't production-ready yet**
>
> It's important to note that this Dockerfile is *not* following all of the best practices yet (by design). It will build the app, but the builds won't be as fast, or the images as secure, as they could be.
>
> Keep reading to learn more about how to make the image maximize the build cache, run as a non-root user, and multi-stage builds.

## [Additional resources](#additional-resources)

To learn more about writing a Dockerfile, visit the following resources:

* [Dockerfile reference](/reference/dockerfile/)
* [Dockerfile best practices](/develop/develop-images/dockerfile_best-practices/)
* [Base images](/build/building/base-images/)
* [Gordon](/ai/gordon/) — Docker's AI assistant can generate a Dockerfile for your project. Ask Gordon to analyze your code and suggest a Dockerfile optimized for your language and framework.

## [Next steps](#next-steps)

Now that you have created a Dockerfile and learned the basics, it's time to learn about building, tagging, and pushing the images.

[Build, tag and publish the Image](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/)

----
url: https://docs.docker.com/admin/organization/setup/general-settings/
----

# Change general organization information

***

Table of contents

***

Learn how to update your organization information using the Admin Console.

## [Update organization information](#update-organization-information)

General organization information appears on your organization landing page in the Admin Console.

This information includes:

* Organization Name
* Company
* Location
* Website
* Gravatar email: To add an avatar to your Docker account, create a [Gravatar account](https://gravatar.com/) and upload an avatar. Next, add your Gravatar email to your Docker account settings. It may take some time for your avatar to update in Docker.

To edit this information:

1. Sign in to the [Admin Console](https://app.docker.com/admin) and select your organization from the top-left account drop-down.
2. Enter or update your organization’s details, then select **Save**.

## [Next steps](#next-steps)

After configuring your organization information, you can:

* [Configure single sign-on (SSO)](https://docs.docker.com/enterprise/security/single-sign-on/connect/)
* [Set up SCIM provisioning](https://docs.docker.com/enterprise/security/provisioning/scim/)
* [Manage domains](https://docs.docker.com/enterprise/security/domain-management/)
* [Create a company](https://docs.docker.com/admin/company/new-company/)

----
url: https://docs.docker.com/ai/sandboxes/governance/audit/
----

# Audit logging

***

Table of contents

***

The sandbox daemon records a structured audit event for every policy decision it makes. Each record captures who triggered the evaluation, when it happened, which rule matched, and whether the resource was allowed or denied. Records are written to disk as JSON Lines (`.jsonl`) so existing SIEM and log-shipping tools can collect them. The records stay on the machine that produced them. Docker doesn't collect or ingest audit data.

> Note
>
> Audit logging is part of Docker AI Governance and requires a separate paid subscription. [Contact Docker Sales](https://www.docker.com/products/ai-governance/#contact-sales) to request access.

Audit logging is active only while your organization enforces a centralized governance policy. The subscription alone doesn't produce records. If your organization hasn't configured and enforced an [organization policy](https://docs.docker.com/ai/sandboxes/governance/org/), the daemon writes no audit logs. To confirm governance is active, run `sbx policy ls` — the output begins with a `Governance: managed by <org>` header when an organization policy is in effect.

Audit logging complements [monitoring](https://docs.docker.com/ai/sandboxes/governance/monitoring/). Monitoring with `sbx policy ls` and `sbx policy log` is for live, interactive debugging. Audit logging produces a durable trail for security review and compliance.

## [What gets recorded](#what-gets-recorded)

The daemon writes two categories of record:

* Evaluation records capture each policy decision: the resource, the action, the verdict, and the reason for a denial.
* Session lifecycle records mark the start and end of each daemon run. Evaluation records share the run's `audit_session_id`, so you can correlate every decision back to a single daemon session.

A network evaluation record looks like this:

```json
{
  "audit_event_id": "95e7257f-93c9-4f29-bde7-88830e2dae80",
  "timestamp": "2026-05-28T19:15:00.728933Z",
  "schema_version": "1.82.0",
  "category": "AUDIT_CATEGORY_EVALUATION",
  "decision": "AUDIT_DECISION_DENY",
  "username": "jordandoe",
  "user_email": "jordandoe@example.com",
  "org_id": "9f8e7d6c-5b4a-3210-fedc-ba9876543210",
  "org_name": "Acme Inc",
  "audit_session_id": "8a3bc076-79d0-4502-baf3-cc6ad35fb578",
  "resource_id": "example.com:443",
  "os": "macos",
  "app_version": "v0.31.0",
  "client_name": "sbx",
  "hostname": "host-machine",
  "deny_reason": [
    "no applicable policies for op(action=net:connect:tcp, resource=net:domain:example.com:443)"
  ],
  "action_type": "network_egress",
  "network_egress": { "protocol": "tcp" },
  "agent": "claude"
}
```

Common fields include:

| Field              | Description                                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------ |
| `timestamp`        | UTC time of the decision.                                                                                    |
| `schema_version`   | Version of the record schema. Pin your SIEM field mappings to it, as the format is a stable contract.        |
| `category`         | `AUDIT_CATEGORY_EVALUATION` for policy decisions, `AUDIT_CATEGORY_MANAGEMENT` for session lifecycle records. |
| `audit_session_id` | Identifies the daemon run that produced the record.                                                          |
| `username`         | The signed-in Docker user's Docker Hub username.                                                             |
| `user_email`       | The signed-in Docker user's email address.                                                                   |
| `org_id`           | ID of the organization whose governance policy is in effect.                                                 |
| `org_name`         | Display name of the organization whose governance policy is in effect.                                       |
| `action_type`      | The kind of access evaluated, such as `network_egress`.                                                      |
| `resource_id`      | The target of the evaluation, such as a host and port.                                                       |
| `decision`         | `AUDIT_DECISION_ALLOW` or `AUDIT_DECISION_DENY`.                                                             |
| `deny_reason`      | Why a denied request was blocked. Present on deny decisions.                                                 |
| `agent`            | The AI agent driving the sandbox (for example, `claude`, `codex`). Omitted when the agent is unknown.        |

Each record is attributed to the signed-in Docker user and the organization whose governance policy is in effect.

## [Where records are stored](#where-records-are-stored)

The daemon writes audit records, not the CLI. Running a command such as `sbx create` sends a request to the daemon, and the daemon emits the resulting record to its own audit directory.

The default location depends on your operating system:

| OS      | Default path                                                      |
| ------- | ----------------------------------------------------------------- |
| macOS   | `~/Library/Logs/com.docker.sandboxes/sandboxes/auditkit/`         |
| Linux   | `${XDG_STATE_HOME:-~/.local/state}/sandboxes/sandboxes/auditkit/` |
| Windows | `%LOCALAPPDATA%\DockerSandboxes\sandboxes\logs\auditkit\`         |

The directory layout differs by platform because each operating system places application logs in its own conventional location.

Files are named `audit-<utc-timestamp>-<process-uuid>-<seq>.jsonl`.

The daemon writes in-progress records to a temporary `.tmp` file and seals it into a final `.jsonl` file by atomic rename. Sealing happens at a rotation threshold (by default 5 minutes, 1000 events, or 50 MiB, whichever comes first) or when the daemon shuts down cleanly. Only sealed `.jsonl` files are complete. Treat `.tmp` files as incomplete and don't collect them.

Sandboxes never delete sealed files. Retention and cleanup are the responsibility of your log shipper or your own housekeeping.

## [Collect records with a SIEM](#collect-records-with-a-siem)

Point your log shipper at the audit directory and configure it to collect sealed `.jsonl` files only. Tools such as the Splunk Universal Forwarder, Filebeat, and CrowdStrike Falcon LogScale read the directory and forward each line as an event. Because in-progress records live in `.tmp` files until they are sealed, collectors never see partial records.

----
url: https://docs.docker.com/scout/release-notes/platform/
----

# Docker Scout release notes

***

Table of contents

***

This page contains information about the new features, improvements, known issues, and bug fixes in Docker Scout releases. These release notes cover the Docker Scout platform, including the Dashboard. For CLI release notes, refer to [Docker Scout CLI release notes](https://docs.docker.com/scout/release-notes/cli/).

## [Q4 2024](#q4-2024)

New features and enhancements released in the fourth quarter of 2024.

### [2024-10-09](#2024-10-09)

Policy Evaluation has graduated from Early Access to General Availability.

Docker Scout Dashboard UI changes:

* On the Docker Scout Dashboard, selecting a policy card now opens the policy details page instead of the policy results page.
* The policy results page and the policy details side panel are now read-only. Policy actions (edit, disable, delete) are now accessible from the policy details page.

## [Q3 2024](#q3-2024)

New features and enhancements released in the third quarter of 2024.

### [2024-09-30](#2024-09-30)

In this release, we've changed how custom policies work. Before, custom policies were created by copying an out-of-the-box policy. Now, you can customize policies either by editing the default policy from a **policy type** which acts as a template. The default policies in Docker Scout are also implemented based on these types.

For more information, refer to [policy types](https://docs.docker.com/scout/policy/#policy-types).

### [2024-09-09](#2024-09-09)

This release changes how [health scores](https://docs.docker.com/scout/policy/scores/) are calculated in Docker Scout. The health score calculation now considers optional and custom policies that you have configured for your organization.

This means that if you have enabled, disabled, or customized any of the default policies, Docker Scout will now take those policies into account when calculating the health score for your organization's images.

If you haven't yet enabled Docker Scout for your organization, the health score calculation will be based on the out-of-the-box policies.

### [2024-08-13](#2024-08-13)

This release changes the out-of-the-box policies to align with the policy configurations used to evaluate Docker Scout [health scores](https://docs.docker.com/scout/policy/scores/).

The default out-of-the-box policies are now:

* **No high-profile vulnerabilities**
* **No fixable critical or high vulnerabilities**
* **Approved Base Images**
* **Default non-root user**
* **Supply chain attestations**
* **Up-to-Date Base Images**
* **No AGPL v3 licenses**

The configurations for these policies are now the same as the configurations used to calculate health scores. Previously, the out-of-the-box policies had different configurations than the health score policies.

## [Q2 2024](#q2-2024)

New features and enhancements released in the second quarter of 2024.

### [2024-06-27](#2024-06-27)

This release introduces initial support for **Exceptions** in the Docker Scout Dashboard. Exceptions let you suppress vulnerabilities found in your images (false positives), using VEX documents. Attach VEX documents to images as attestations, or embed them on image filesystems, and Docker Scout will automatically detect and incorporate the VEX statements into the image analysis results.

The new [Exceptions page](https://scout.docker.com/reports/vex/) lists all exceptions affecting images in your organization. You can also go to the image view in the Docker Scout Dashboard to see all exceptions that apply to a given image.

For more information, see [Manage vulnerability exceptions](https://docs.docker.com/scout/explore/exceptions/).

### [2024-05-06](#2024-05-06)

New HTTP endpoint that lets you scrape data from Docker Scout with Prometheus, to create your own vulnerability and policy dashboards with Grafana. For more information, see [Docker Scout metrics exporter](https://docs.docker.com/scout/explore/metrics-exporter/).

## [Q1 2024](#q1-2024)

New features and enhancements released in the first quarter of 2024.

### [2024-03-29](#2024-03-29)

The **No high-profile vulnerabilities** policy now reports the `xz` backdoor vulnerability [CVE-2024-3094](https://scout.docker.com/v/CVE-2024-3094). Any images in your Docker organization containing the version of `xz/liblzma` with the backdoor will be non-compliant with the **No high-profile vulnerabilities** policy.

### [2024-03-20](#2024-03-20)

The **No fixable critical or high vulnerabilities** policy now supports a **Fixable vulnerabilities only** configuration option, which lets you decide whether or not to only flag vulnerabilities with an available fix version.

### [2024-03-14](#2024-03-14)

The **All critical vulnerabilities** policy has been removed. The **No fixable critical or high vulnerabilities** policy provides similar functionality, and will be updated in the future to allow for more extensive customization, making the now-removed **All critical vulnerabilities** policy redundant.

### [2024-01-26](#2024-01-26)

**Azure Container Registry** integration graduated from [Early Access](https://docs.docker.com/release-lifecycle/#early-access-ea) to [General Availability](https://docs.docker.com/release-lifecycle/#general-availability-ga).

For more information and setup instructions, see [Integrate Azure Container Registry](https://docs.docker.com/scout/integrations/registry/acr/).

### [2024-01-23](#2024-01-23)

New **Approved Base Images** policy, which lets you restrict which base images you allow in your builds. You define the allowed base images using a pattern. Base images whose image reference don't match the specified patterns cause the policy to fail.

### [2024-01-12](#2024-01-12)

New **Default non-root user** policy, which flags images that would run as the `root` superuser with full system administration privileges by default. Specifying a non-root default user for your images can help strengthen your runtime security.

### [2024-01-11](#2024-01-11)

[Beta](https://docs.docker.com/release-lifecycle/#beta) launch of a new GitHub app for integrating Docker Scout with your source code management, and a remediation feature for helping you improve policy compliance.

Remediation is a new capability for Docker Scout to provide contextual, recommended actions based on policy evaluation results on how you can improve compliance.

The GitHub integration enhances the remediation feature. With the integration enabled, Docker Scout is able to connect analysis results to the source. This additional context about how your images are built is used to generate better, more precise recommendations.

For more information about the types of recommendations that Docker Scout can provide to help you improve policy compliance, see [Remediation](https://docs.docker.com/scout/policy/remediation/).

For more information about how to authorize the Docker Scout GitHub app on your source repositories, see [Integrate Docker Scout with GitHub](https://docs.docker.com/scout/integrations/source-code-management/github/).

## [Q4 2023](#q4-2023)

New features and enhancements released in the fourth quarter of 2023.

### [2023-12-20](#2023-12-20)

**Azure Container Registry** integration graduated from [Beta](https://docs.docker.com/release-lifecycle/#beta) to [Early Access](https://docs.docker.com/release-lifecycle/#early-access-ea).

For more information and setup instructions, see [Integrate Azure Container Registry](https://docs.docker.com/scout/integrations/registry/acr/).

### [2023-12-06](#2023-12-06)

New [SonarQube](https://www.sonarsource.com/products/sonarqube/) integration and related policy. SonarQube is an open-source platform for continuous inspection of code quality. This integration lets you add SonarQube's quality gates as a policy evaluation in Docker Scout. Enable the integration, push your images, and see the SonarQube quality gate conditions surfaced in the new **SonarQube quality gates passed** policy.

### [2023-12-01](#2023-12-01)

[Beta](https://docs.docker.com/release-lifecycle/#beta) release of a new **Azure Container Registry** (ACR) integration, which lets Docker Scout pull and analyze images in ACR repositories automatically.

To learn more about the integration and how to get started, see [Integrate Azure Container Registry](https://docs.docker.com/scout/integrations/registry/acr/).

### [2023-11-21](#2023-11-21)

New **configurable policies** feature, which enables you to tweak the out-of-the-box policies according to your preferences, or disable them entirely if they don't quite match your needs. Some examples of how you can adapt policies for your organization include:

* Change the severity-thresholds that vulnerability-related policies use
* Customize the list of "high-profile vulnerabilities"
* Add or remove software licenses to flag as "copyleft"

For more information, see [Configurable policies](https://docs.docker.com/scout/policy/configure/).

### [2023-11-10](#2023-11-10)

New **Supply chain attestations** policy for helping you track whether your images are built with SBOM and provenance attestations. Adding attestations to images is a good first step in improving your supply chain conduct, and is often a prerequisite for doing more.

### [2023-11-01](#2023-11-01)

New **No high-profile vulnerabilities** policy, which ensures your artifacts are free from a curated list of vulnerabilities widely recognized to be risky.

### [2023-10-04](#2023-10-04)

This marks the General Availability (GA) release of Docker Scout.

The following new features are included in this release:

* [Policy Evaluation](#policy-evaluation) (Early Access)
* [Amazon ECR integration](#amazon-ecr-integration)
* [Sysdig integration](#sysdig-integration)
* [JFrog Artifactory integration](#jfrog-artifactory-integration)

#### [Policy evaluation](#policy-evaluation)

Policy Evaluation is an early access feature that helps you ensure software integrity and track how your artifacts are doing over time. This release ships with four out-of-the-box policies, enabled by default for all organizations.

* **Base images not up-to-date** evaluates whether the base images are out of date, and require updating. Up-to-date base images help you ensure that your environments are reliable and secure.
* **Critical and high vulnerabilities with fixes** reports if there are vulnerabilities with critical or high severity in your images, and where there's a fix version available that you can upgrade to.
* **All critical vulnerabilities** looks out for any vulnerabilities of critical severity found in your images.
* **Packages with AGPLv3, GPLv3 license** helps you catch possibly unwanted copyleft licenses used in your images.

You can view and evaluate policy status for images using the Docker Scout Dashboard and the `docker scout policy` CLI command. For more information, refer to the [Policy Evaluation documentation](/scout/policy/).

#### [Amazon ECR integration](#amazon-ecr-integration)

The new Amazon Elastic Container Registry (ECR) integration enables image analysis for images hosted in ECR repositories.

You set up the integration using a pre-configured CloudFormation stack template that bootstraps the necessary AWS resources in your account. Docker Scout automatically analyzes images that you push to your registry, storing only the metadata about the image contents, and not the container images themselves.

The integration offers a straightforward process for adding additional repositories, activating Docker Scout for specific repositories, and removing the integration if needed. To learn more, refer to the [Amazon ECR integration documentation](https://docs.docker.com/scout/integrations/registry/ecr/).

#### [Sysdig integration](#sysdig-integration)

The new Sysdig integration gives you real-time security insights for your Kubernetes runtime environments.

Enabling this integration helps you address and prioritize risks for images used to run your production workloads. It also helps reduce monitoring noise, by automatically excluding vulnerabilities in programs that are never loaded into memory, using VEX documents.

For more information and getting started, see [Sysdig integration documentation](https://docs.docker.com/scout/integrations/environment/sysdig/).

#### [JFrog Artifactory integration](#jfrog-artifactory-integration)

The new JFrog Artifactory integration enables automatic image analysis on Artifactory registries.

The integration involves deploying a Docker Scout Artifactory agent that polls for new images, performs analysis, and uploads results to Docker Scout, all while preserving the integrity of image data.

#### [Known limitations](#known-limitations)

* Image analysis only works for Linux images
* Docker Scout can't process images larger than 12GB in compressed size
* Creating an image SBOM (part of image analysis) has a timeout limit of 4 minutes

----
url: https://docs.docker.com/reference/cli/sbx/ports/
----

# sbx ports

| Description | Manage sandbox port publishing |
| ----------- | ------------------------------ |
| Usage       | `sbx ports SANDBOX [flags]`    |

## [Description](#description)

Manage sandbox port publishing.

List, publish, or unpublish ports for a running sandbox. Without --publish or --unpublish flags, lists all published ports.

Port spec format: \[\[HOST\_IP:]HOST\_PORT:]SANDBOX\_PORT\[/PROTOCOL] If HOST\_PORT is omitted, an ephemeral port is allocated automatically. If HOST\_IP is omitted, the port is bound on loopback, expanded based on PROTOCOL and the sandbox's address families: tcp/udp binds both 127.0.0.1 and ::1 (or only 127.0.0.1 if the sandbox is IPv4-only); tcp4/udp4 binds only 127.0.0.1; tcp6/udp6 binds only ::1. PROTOCOL defaults to tcp. Supported protocols: tcp, tcp4, tcp6, udp, udp4, udp6.

## [Options](#options)

| Option        | Default | Description                                                                           |
| ------------- | ------- | ------------------------------------------------------------------------------------- |
| `--json`      |         | Output in JSON format (for port listing)                                              |
| `--publish`   |         | Publish a port (can be repeated): \[\[HOST\_IP:]HOST\_PORT:]SANDBOX\_PORT\[/PROTOCOL] |
| `--unpublish` |         | Unpublish a port (can be repeated): \[HOST\_IP:]HOST\_PORT:SANDBOX\_PORT\[/PROTOCOL]  |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# List published ports
sbx ports my-sandbox

# Publish sandbox port 8080 to an ephemeral host port
sbx ports my-sandbox --publish 8080

# Publish with a specific host port
sbx ports my-sandbox --publish 3000:8080

# Unpublish a port
sbx ports my-sandbox --unpublish 3000:8080
```

----
url: https://docs.docker.com/reference/samples/rails/
----

# Rails samples

| Name                                                                                                             | Description                                                                                         |
| ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Compose and Rails](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/rails/) | This Quickstart guide shows you how to use Docker Compose to set up and run a Rails/PostgreSQL app. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/desktop/setup/install/linux/rhel/
----

# Install Docker Desktop on RHEL

***

Table of contents

***

> **Docker Desktop terms**
>
> Commercial use of Docker Desktop in larger enterprises (more than 250 employees or more than $10 million USD in annual revenue) requires a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopRhelInstall).

This page contains information on how to install, launch and upgrade Docker Desktop on a Red Hat Enterprise Linux (RHEL) distribution.

## [Prerequisites](#prerequisites)

To install Docker Desktop successfully, you must:

* Meet the [general system requirements](https://docs.docker.com/desktop/setup/install/linux/#general-system-requirements).

* Have a 64-bit version of either RHEL 9 or RHEL 10.

* If `pass` is not installed, or it can't be installed, you must enable [CodeReady Linux Builder (CRB) repository](https://access.redhat.com/articles/4348511) and [Extra Packages for Enterprise Linux (EPEL)](https://docs.fedoraproject.org/en-US/epel/).

  ```console
  $ sudo subscription-manager repos --enable codeready-builder-for-rhel-10-$(arch)-rpms
  $ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-10.noarch.rpm
  $ sudo dnf install pass
  ```

  ```console
  $ sudo subscription-manager repos --enable codeready-builder-for-rhel-9-$(arch)-rpms
  $ sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
  $ sudo dnf install pass
  ```

* For a GNOME desktop environment you must install AppIndicator and KStatusNotifierItem [GNOME extensions](https://extensions.gnome.org/extension/615/appindicator-support/). You must also enable EPEL.

  ```console
  $ # enable EPEL as described above
  $ sudo dnf install gnome-shell-extension-appindicator
  $ sudo gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
  ```

  ```console
  $ # enable EPEL as described above
  $ sudo dnf install gnome-shell-extension-appindicator
  $ sudo gnome-extensions enable appindicatorsupport@rgcjonas.gmail.com
  ```

* If you're not using GNOME, you must install `gnome-terminal` to enable terminal access from Docker Desktop:

  ```console
  $ sudo dnf install gnome-terminal
  ```

## [Install Docker Desktop](#install-docker-desktop)

To install Docker Desktop on RHEL:

1. Set up Docker's package repository as follows:

   ```console
   $ sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
   ```

2. Download the latest [RPM package](https://desktop.docker.com/linux/main/amd64/docker-desktop-x86_64-rhel.rpm?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-linux-amd64).

3. Install the package with dnf as follows:

   ```console
   $ sudo dnf install ./docker-desktop-x86_64-rhel.rpm
   ```

The RPM package includes a post-install script that completes additional setup steps automatically.

The post-install script:

* Sets the capability on the Docker Desktop binary to map privileged ports and set resource limits.
* Adds a DNS name for Kubernetes to `/etc/hosts`.
* Creates a symlink from `/usr/local/bin/com.docker.cli` to `/usr/bin/docker`. This is because the classic Docker CLI is installed at `/usr/bin/docker`. The Docker Desktop installer also installs a Docker CLI binary that includes cloud-integration capabilities and is essentially a wrapper for the Compose CLI, at `/usr/local/bin/com.docker.cli`. The symlink ensures that the wrapper can access the classic Docker CLI.
* Creates a symlink from `/usr/libexec/qemu-kvm` to `/usr/local/bin/qemu-system-x86_64`.

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

> Tip
>
> To attach Red Hat subscription data to containers, see [Red Hat verified solution](https://access.redhat.com/solutions/5870841).
>
> For example:
>
> ```console
> $ docker run --rm -it -v "/etc/pki/entitlement:/etc/pki/entitlement" -v "/etc/rhsm:/etc/rhsm-host" -v "/etc/yum.repos.d/redhat.repo:/etc/yum.repos.d/redhat.repo" registry.access.redhat.com/ubi9
> ```

## [Upgrade Docker Desktop](#upgrade-docker-desktop)

Once a new version for Docker Desktop is released, the Docker UI shows a notification. You need to first remove the previous version and then download the new package each time you want to upgrade Docker Desktop. Run:

```console
$ sudo dnf remove docker-desktop
$ sudo dnf install ./docker-desktop-<arch>-rhel.rpm
```

## [Next steps](#next-steps)

* Review [Docker's subscriptions](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopRhelInstall) to see what Docker can offer you.
* Take a look at the [Docker workshop](https://docs.docker.com/get-started/workshop/) to learn how to build an image and run it as a containerized application.
* [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and all its features.
* [Troubleshooting](https://docs.docker.com/desktop/troubleshoot-and-support/troubleshoot/) describes common problems, workarounds, how to run and submit diagnostics, and submit issues.
* [FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/) provide answers to frequently asked questions.
* [Release notes](https://docs.docker.com/desktop/release-notes/) lists component updates, new features, and improvements associated with Docker Desktop releases.
* [Back up and restore data](https://docs.docker.com/desktop/settings-and-maintenance/backup-and-restore/) provides instructions on backing up and restoring data related to Docker.

----
url: https://docs.docker.com/guides/frameworks/laravel/development-setup/
----

# Laravel Development Setup with Docker Compose

***

Table of contents

***

This guide demonstrates how to configure a **development** environment for a Laravel application using Docker and Docker Compose. It builds **on top of** the production image for PHP-FPM and then adds developer-focused features—like Xdebug—to streamline debugging. By basing the development container on a known production image, you keep both environments closely aligned.

This setup includes PHP-FPM, Nginx, and PostgreSQL services (although you can easily swap PostgreSQL for another database, like MySQL or MariaDB). Everything runs in containers, so you can develop in isolation without altering your host system.

> Note
>
> To experiment with a ready-to-run configuration, download the [Laravel Docker Examples](https://github.com/dockersamples/laravel-docker-examples) repository. It contains pre-configured setups for both development and production.

## [Project structure](#project-structure)

```plaintext
my-laravel-app/
├── app/
├── bootstrap/
├── config/
├── database/
├── public/
├── docker/
│   ├── common/
│   │   └── php-fpm/
│   │       └── Dockerfile
│   ├── development/
│   │   ├── php-fpm/
│   │   │   └── entrypoint.sh
│   │   ├── workspace/
│   │   │   └── Dockerfile
│   │   └── nginx
│   │       ├── Dockerfile
│   │       └── nginx.conf
│   └── production/
├── compose.dev.yaml
├── compose.prod.yaml
├── .dockerignore
├── .env
├── vendor/
├── ...
```

This layout represents a typical Laravel project, with Docker configurations stored in a unified `docker` directory. You’ll find **two** Compose files — `compose.dev.yaml` (for development) and `compose.prod.yaml` (for production) — to keep your environments separate and manageable.

The environment includes a `workspace` service, a sidecar container for tasks like building front-end assets, running Artisan commands, and other CLI tools your project may require. While this extra container may seem unusual, it’s a familiar pattern in solutions like **Laravel Sail** and **Laradock**. It also includes **Xdebug** to aid in debugging.

## [Create a Dockerfile for PHP-FPM](#create-a-dockerfile-for-php-fpm)

This Dockerfile **extends** the production image by installing Xdebug and adjusting user permissions to ease local development. That way, your development environment stays consistent with production while still offering extra debug features and improved file mounting.

```dockerfile
# Builds a dev-only layer on top of the production image
FROM production AS development

# Use ARGs to define environment variables passed from the Docker build command or Docker Compose.
ARG XDEBUG_ENABLED=true
ARG XDEBUG_MODE=develop,coverage,debug,profile
ARG XDEBUG_HOST=host.docker.internal
ARG XDEBUG_IDE_KEY=DOCKER
ARG XDEBUG_LOG=/dev/stdout
ARG XDEBUG_LOG_LEVEL=0

USER root

# Configure Xdebug if enabled
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    pecl install xdebug && \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
fi

# Add ARGs for syncing permissions
ARG UID=1000
ARG GID=1000

# Create a new user with the specified UID and GID, reusing an existing group if GID exists
RUN if getent group ${GID}; then \
      group_name=$(getent group ${GID} | cut -d: -f1); \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
      group_name=www; \
    fi

# Dynamically update php-fpm to use the new user and group
RUN sed -i "s/user = www-data/user = www/g" /usr/local/etc/php-fpm.d/www.conf && \
    sed -i "s/group = www-data/group = $group_name/g" /usr/local/etc/php-fpm.d/www.conf


# Set the working directory
WORKDIR /var/www

# Copy the entrypoint script
COPY ./docker/development/php-fpm/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Switch back to the non-privileged user to run the application
USER www-data

# Change the default command to run the entrypoint script
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Expose port 9000 and start php-fpm server
EXPOSE 9000
CMD ["php-fpm"]
```

## [Create a Dockerfile for Workspace](#create-a-dockerfile-for-workspace)

A workspace container provides a dedicated shell for asset compilation, Artisan/Composer commands, and other CLI tasks. This approach follows patterns from Laravel Sail and Laradock, consolidating all development tools into one container for convenience.

```dockerfile
# docker/development/workspace/Dockerfile
# Use the official PHP CLI image as the base
FROM php:8.5-cli

# Set environment variables for user and group ID
ARG UID=1000
ARG GID=1000
ARG NODE_VERSION=22.0.0

# Install system dependencies and build libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    libpq-dev \
    libonig-dev \
    libssl-dev \
    libxml2-dev \
    libcurl4-openssl-dev \
    libicu-dev \
    libzip-dev \
    && docker-php-ext-install -j$(nproc) \
    pdo_mysql \
    pdo_pgsql \
    pgsql \
    intl \
    zip \
    bcmath \
    soap \
    && pecl install redis \
    && docker-php-ext-enable redis \
    && curl -sS https://getcomposer.org/installer | php -- --install-dir=/usr/local/bin --filename=composer \
    && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Use ARG to define environment variables passed from the Docker build command or Docker Compose.
ARG XDEBUG_ENABLED
ARG XDEBUG_MODE
ARG XDEBUG_HOST
ARG XDEBUG_IDE_KEY
ARG XDEBUG_LOG
ARG XDEBUG_LOG_LEVEL

# Configure Xdebug if enabled
RUN if [ "${XDEBUG_ENABLED}" = "true" ]; then \
    pecl install xdebug && \
    docker-php-ext-enable xdebug && \
    echo "xdebug.mode=${XDEBUG_MODE}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.idekey=${XDEBUG_IDE_KEY}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log=${XDEBUG_LOG}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.log_level=${XDEBUG_LOG_LEVEL}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini && \
    echo "xdebug.client_host=${XDEBUG_HOST}" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
    echo "xdebug.start_with_request=yes" >> /usr/local/etc/php/conf.d/docker-php-ext-xdebug.ini ; \
fi

# If the group already exists, use it; otherwise, create the 'www' group
RUN if getent group ${GID}; then \
      useradd -m -u ${UID} -g ${GID} -s /bin/bash www; \
    else \
      groupadd -g ${GID} www && \
      useradd -m -u ${UID} -g www -s /bin/bash www; \
    fi && \
    usermod -aG sudo www && \
    echo 'www ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Switch to the non-root user to install NVM and Node.js
USER www

# Install NVM (Node Version Manager) as the www user
RUN export NVM_DIR="$HOME/.nvm" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm alias default ${NODE_VERSION} && \
    nvm use default

# Ensure NVM is available for all future shells
RUN echo 'export NVM_DIR="$HOME/.nvm"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/www/.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /home/www/.bashrc

# Set the working directory
WORKDIR /var/www

# Override the entrypoint to avoid the default php entrypoint
ENTRYPOINT []

# Default command to keep the container running
CMD ["bash"]
```

> Note
>
> If you prefer a **one-service-per-container** approach, simply omit the workspace container and run separate containers for each task. For example, you could use a dedicated `php-cli` container for your PHP scripts, and a `node` container to handle the asset building.

## [Create a Docker Compose configuration for development](#create-a-docker-compose-configuration-for-development)

Here's the `compose.yaml` file to set up the development environment:

```yaml
services:
  web:
    image: nginx:latest # Using the default Nginx image with custom configuration.
    volumes:
      # Mount the application code for live updates
      - ./:/var/www
      # Mount the Nginx configuration file
      - ./docker/development/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    ports:
      # Map port 80 inside the container to the port specified by 'NGINX_PORT' on the host machine
      - "80:80"
    environment:
      - NGINX_HOST=localhost
    networks:
      - laravel-development
    depends_on:
      php-fpm:
        condition: service_started # Wait for php-fpm to start

  php-fpm:
    # For the php-fpm service, we will use our common PHP-FPM Dockerfile with the development target
    build:
      context: .
      dockerfile: ./docker/common/php-fpm/Dockerfile
      target: development
      args:
        UID: ${UID:-1000}
        GID: ${GID:-1000}
        XDEBUG_ENABLED: ${XDEBUG_ENABLED:-true}
        XDEBUG_MODE: develop,coverage,debug,profile
        XDEBUG_HOST: ${XDEBUG_HOST:-host.docker.internal}
        XDEBUG_IDE_KEY: ${XDEBUG_IDE_KEY:-DOCKER}
        XDEBUG_LOG: /dev/stdout
        XDEBUG_LOG_LEVEL: 0
    env_file:
      # Load the environment variables from the Laravel application
      - .env
    user: "${UID:-1000}:${GID:-1000}"
    volumes:
      # Mount the application code for live updates
      - ./:/var/www
    networks:
      - laravel-development
    depends_on:
      postgres:
        condition: service_started # Wait for postgres to start

  workspace:
    # For the workspace service, we will also create a custom image to install and setup all the necessary stuff.
    build:
      context: .
      dockerfile: ./docker/development/workspace/Dockerfile
      args:
        UID: ${UID:-1000}
        GID: ${GID:-1000}
        XDEBUG_ENABLED: ${XDEBUG_ENABLED:-true}
        XDEBUG_MODE: develop,coverage,debug,profile
        XDEBUG_HOST: ${XDEBUG_HOST:-host.docker.internal}
        XDEBUG_IDE_KEY: ${XDEBUG_IDE_KEY:-DOCKER}
        XDEBUG_LOG: /dev/stdout
        XDEBUG_LOG_LEVEL: 0
    tty: true # Enables an interactive terminal
    stdin_open: true # Keeps standard input open for 'docker exec'
    env_file:
      - .env
    volumes:
      - ./:/var/www
    networks:
      - laravel-development

  postgres:
    image: postgres:18
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    environment:
      - POSTGRES_DB=app
      - POSTGRES_USER=laravel
      - POSTGRES_PASSWORD=secret
    volumes:
      - postgres-data-development:/var/lib/postgresql
    networks:
      - laravel-development

  redis:
    image: redis:alpine
    networks:
      - laravel-development

networks:
  laravel-development:

volumes:
  postgres-data-development:
```

> Note
>
> Ensure you have an `.env` file at the root of your Laravel project with the necessary configurations. You can use the `.env.example` file as a template.

## [Run your development environment](#run-your-development-environment)

To start the development environment, use:

```console
$ docker compose -f compose.dev.yaml up --build -d
```

Run this command to build and start the development environment in detached mode. When the containers finish initializing, visit <http://localhost/> to see your Laravel app in action.

## [Summary](#summary)

By building on top of the production image and adding debug tools like Xdebug, you create a Laravel development workflow that closely mirrors production. The optional workspace container simplifies tasks like asset building and running Artisan commands. If you prefer a separate container for every service (e.g., a dedicated `php-cli` and `node` container), you can skip the workspace approach. Either way, Docker Compose provides an efficient, consistent way to develop your Laravel project.

[Common Questions on Using Laravel with Docker »](https://docs.docker.com/guides/frameworks/laravel/common-questions/)

----
url: https://docs.docker.com/reference/cli/docker/compose/port/
----

# docker compose port

***

| Description | Print the public port for a port binding             |
| ----------- | ---------------------------------------------------- |
| Usage       | `docker compose port [OPTIONS] SERVICE PRIVATE_PORT` |

## [Description](#description)

Prints the public port for a port binding

## [Options](#options)

| Option       | Default | Description                                             |
| ------------ | ------- | ------------------------------------------------------- |
| `--index`    |         | Index of the container if service has multiple replicas |
| `--protocol` | `tcp`   | tcp or udp                                              |

----
url: https://docs.docker.com/reference/cli/docker/desktop/kubernetes/images/
----

# docker desktop kubernetes images

***

| Description | List Kubernetes images used by Docker Desktop |
| ----------- | --------------------------------------------- |
| Usage       | `docker desktop kubernetes images`            |

## [Options](#options)

| Option     | Default  | Description                                          |
| ---------- | -------- | ---------------------------------------------------- |
| `--format` | `pretty` | Format the output. Accepted values are: pretty, json |

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/
----

# Registry Access Management

***

Table of contents

***

Subscription: Business

For: Administrators

Registry Access Management (RAM) lets administrators control which container registries developers can access through Docker Desktop. This DNS-level filtering ensures developers only pull and push images from approved registries, improving supply chain security.

RAM works with all registry types including cloud services, on-premises registries, and registry mirrors. You can allow any hostname or domain, but must include redirect domains (like `s3.amazonaws.com` for some registries) in your allowlist.

## [Supported registries](#supported-registries)

Registry Access Management works with any container registry, including:

* Docker Hub (allowed by default)
* Cloud registries: Amazon ECR, Google Artifact Registry, Azure Container Registry
* Git-based registries: GitHub Container Registry, GitLab Container Registry
* On-premises solutions: Nexus, Artifactory, Harbor
* Registry mirrors: Including Docker Hub mirrors

## [Prerequisites](#prerequisites)

Before configuring Registry Access Management, you must:

* [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/). Registry Access Management only takes effect when users are signed in to Docker Desktop with organization credentials.
* Use [personal access tokens (PATs)](https://docs.docker.com/security/access-tokens/) for authentication (Organization access tokens aren't supported)
* Have a Docker Business subscription

## [Configure registry permissions](#configure-registry-permissions)

To configure registry permissions:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization from the top-left account drop-down.

2. Select **Admin Console**, then **Registry access**.

3. Use the **toggle** to enable registry access. By default, Docker Hub is enabled in the registry list.

4. To add additional registries, select **Add registry** and provide a **Registry address** and **Registry nickname**.

5. Select **Create**. You can add up to 100 registries.

6. Verify your registry appears in the registry list and select **Save changes**.

   > Note
   >
   > Policy changes can take up to 24 hours to propagate. To apply changes immediately, ask developers to sign out and back in to Docker Desktop.

If a developer belongs to multiple organizations with different RAM policies, only the policy for the first organization in the configuration file is enforced.

> Tip
>
> RAM restrictions also apply to Dockerfile `ADD` instructions that fetch content via URL. Include trusted registry domains in your allowlist when using `ADD` with URLs.
>
> RAM is designed for container registries, not general-purpose URLs like package mirrors or storage services. Adding too many domains may cause errors or hit system limits.

## [Verify restrictions are working](#verify-restrictions-are-working)

After users sign in to Docker Desktop with their organization credentials, Registry Access Management takes effect immediately.

When users try to pull from a blocked registry:

```console
$ docker pull blocked-registry.com/image:tag
Error response from daemon: registry access to blocked-registry.com is not allowed
```

Allowed registry access works normally:

```console
$ docker pull allowed-registry.com/image:tag
# Pull succeeds
```

Registry restrictions apply to all Docker operations including pulls, pushes, and builds that reference external registries.

## [Registry limits and platform constraints](#registry-limits-and-platform-constraints)

Registry Access Management has these limits and platform-specific behaviors:

* Maximum allowlist size: 100 registries or domains per organization
* DNS-based filtering: Restrictions work at the hostname level, not IP addresses
* Redirect domains required: Must include all domains a registry redirects to (CDN endpoints, storage services)
* Windows containers: Windows image operations aren't restricted by default. Turn on **Use proxy for Windows Docker daemon** in Docker Desktop settings to apply restrictions
* WSL 2 requirements: Requires Linux kernel 5.4 or later, restrictions apply to all WSL 2 distributions

## [Build and deployment restrictions](#build-and-deployment-restrictions)

These scenarios are not restricted by Registry Access Management:

* Docker buildx with Kubernetes driver
* Docker buildx with custom Docker-container driver
* Some Docker Debug and Kubernetes image pulls (even if Docker Hub is blocked)
* Images previously cached by registry mirrors may still be blocked if the source registry is restricted

## [Security bypass considerations](#security-bypass-considerations)

Users can potentially bypass Registry Access Management through:

* Local proxies or DNS manipulation
* Signing out of Docker Desktop (unless sign-in is enforced)
* Network-level modifications outside Docker Desktop's control

To maximize security effectiveness:

* [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) to prevent bypass through sign-out
* Implement additional network-level controls for complete protection
* Use Registry Access Management as part of a broader security strategy

## [Registry allowlist best practices](#registry-allowlist-best-practices)

* Include all registry domains: Some registries redirect to multiple domains. For AWS ECR, include:

  ```text
  your-account.dkr.ecr.us-west-2.amazonaws.com
  amazonaws.com
  s3.amazonaws.com
  ```

* Practice regular allowlist maintenance:

  * Remove unused registries periodically
  * Add newly approved registries as needed
  * Update domain names that may have changed
  * Monitor registry usage through Docker Desktop analytics

* Test configuration changes:

  * Verify registry access after making allowlist updates
  * Check that all necessary redirect domains are included
  * Ensure development workflows aren't disrupted
  * Combine with [Enhanced Container Isolation](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) for comprehensive protection

----
url: https://docs.docker.com/build/ci/github-actions/build-summary/
----

# GitHub Actions build summary

***

Table of contents

***

Docker's GitHub Actions for building and pushing images generate a job summary for your build that outlines the execution and materials used:

* A summary showing the Dockerfile used, the build duration, and cache utilization
* Inputs for the build, such as build arguments, tags, labels, and build contexts
* For builds with [Bake](https://docs.docker.com/build/bake/), the full bake definition for the build

Job summaries for Docker builds appear automatically if you use the following versions of the [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images) or [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake) GitHub Actions:

* `docker/build-push-action@v7`
* `docker/bake-action@v7`

To view the job summary, open the details page for the job in GitHub after the job has finished. The summary is available for both failed and successful builds. In the case of a failed build, the summary also displays the error message that caused the build to fail:

## [Import build records to Docker Desktop](#import-build-records-to-docker-desktop)

The job summary includes a link for downloading a build record archive for the run. The build record archive is a ZIP file containing the details about a build (or builds, if you use `docker/bake-action` to build multiple targets). You can import this build record archive into Docker Desktop, which gives you a powerful, graphical interface for further analyzing the build's performance via the [Docker Desktop **Builds** view](https://docs.docker.com/desktop/use-desktop/builds/).

To import the build record archive into Docker Desktop:

1. Download and install [Docker Desktop](https://docs.docker.com/get-started/get-docker/).

2. Download the build record archive from the job summary in GitHub Actions.

3. Open the **Builds** view in Docker Desktop.

4. Select the **Import build** button, and then browse for the `.zip` archive job summary that you downloaded. Alternatively, you can drag-and-drop the build record archive ZIP file onto the Docker Desktop window after opening the import build dialog.

5. Select **Import** to add the build records.

After a few seconds, the builds from the GitHub Actions run appear under the **Completed builds** tab in the Builds view. To inspect a build and see a detailed view of all the inputs, results, build steps, and cache utilization, select the item in the list.

## [Disable job summary](#disable-job-summary)

To disable job summaries, set the `DOCKER_BUILD_SUMMARY` environment variable in the YAML configuration for your build step:

```yaml
      - name: Build
        uses: docker/build-push-action@v7
        env:
          DOCKER_BUILD_SUMMARY: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

## [Disable build record upload](#disable-build-record-upload)

To disable the upload of the build record archive to GitHub, set the `DOCKER_BUILD_RECORD_UPLOAD` environment variable in the YAML configuration for your build step:

```yaml
      - name: Build
        uses: docker/build-push-action@v7
        env:
          DOCKER_BUILD_RECORD_UPLOAD: false
        with:
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
```

With this configuration, the build summary is still generated, but does not contain a link to download the build record archive.

## [Limitations](#limitations)

Build summaries are currently not supported for:

* Repositories hosted on GitHub Enterprise Servers. Summaries can only be viewed for repositories hosted on GitHub.com.

----
url: https://docs.docker.com/reference/cli/docker/offload/status/
----

# docker offload status

***

| Description | Show the status of the Docker Offload connection |
| ----------- | ------------------------------------------------ |
| Usage       | `docker offload status [OPTIONS]`                |

## [Options](#options)

| Option         | Default  | Description                                              |
| -------------- | -------- | -------------------------------------------------------- |
| `-f, --format` | `pretty` | Format of output (default: pretty, one of: pretty\|json) |
| `-w, --watch`  |          | Watch for status updates                                 |

----
url: https://docs.docker.com/reference/build-checks/duplicate-stage-name/
----

# DuplicateStageName

***

Table of contents

***

## [Output](#output)

```text
Duplicate stage name 'foo-base', stage names should be unique
```

## [Description](#description)

Defining multiple stages with the same name results in an error because the builder is unable to uniquely resolve the stage name reference.

## [Examples](#examples)

❌ Bad: `builder` is declared as a stage name twice.

```dockerfile
FROM debian:latest AS builder
RUN apt-get update; apt-get install -y curl

FROM golang:latest AS builder
```

✅ Good: stages have unique names.

```dockerfile
FROM debian:latest AS deb-builder
RUN apt-get update; apt-get install -y curl

FROM golang:latest AS go-builder
```

----
url: https://docs.docker.com/reference/cli/docker/buildx/rm/
----

# docker buildx rm

***

| Description | Remove one or more builder instances   |
| ----------- | -------------------------------------- |
| Usage       | `docker buildx rm [OPTIONS] [NAME...]` |

## [Description](#description)

Removes the specified or current builder. It is a no-op attempting to remove the default builder.

## [Options](#options)

| Option                            | Default | Description                                             |
| --------------------------------- | ------- | ------------------------------------------------------- |
| [`--all-inactive`](#all-inactive) |         | Remove all inactive builders                            |
| [`-f, --force`](#force)           |         | Do not prompt for confirmation                          |
| [`--keep-daemon`](#keep-daemon)   |         | Keep the BuildKit daemon running                        |
| [`--keep-state`](#keep-state)     |         | Keep BuildKit state                                     |
| `--timeout`                       | `20s`   | Override the default timeout for loading builder status |

## [Examples](#examples)

### [Remove all inactive builders (--all-inactive)](#all-inactive)

Remove builders that are not in running state.

```console
$ docker buildx rm --all-inactive
WARNING! This will remove all builders that are not in running state. Are you sure you want to continue? [y/N] y
```

### [Override the configured builder instance (--builder)](#builder)

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).

### [Do not prompt for confirmation (--force)](#force)

Do not prompt for confirmation before removing inactive builders.

```console
$ docker buildx rm --all-inactive --force
```

### [Keep the BuildKit daemon running (--keep-daemon)](#keep-daemon)

Keep the BuildKit daemon running after the buildx context is removed. This is useful when you manage BuildKit daemons and buildx contexts independently. Only supported by the [`docker-container`](/build/drivers/docker-container/) and [`kubernetes`](/build/drivers/kubernetes/) drivers.

### [Keep BuildKit state (--keep-state)](#keep-state)

Keep BuildKit state, so it can be reused by a new builder with the same name. Currently, only supported by the [`docker-container` driver](/build/drivers/docker-container/).

----
url: https://docs.docker.com/reference/cli/docker/mcp/tools/count/
----

# docker mcp tools count

***

| Description | Count tools              |
| ----------- | ------------------------ |
| Usage       | `docker mcp tools count` |

## [Description](#description)

Count tools

----
url: https://docs.docker.com/reference/cli/docker/network/inspect/
----

# docker network inspect

***

| Description | Display detailed information on one or more networks    |
| ----------- | ------------------------------------------------------- |
| Usage       | `docker network inspect [OPTIONS] NETWORK [NETWORK...]` |

## [Description](#description)

Returns information about one or more networks. By default, this command renders all results in a JSON object.

## [Options](#options)

| Option          | Default | Description                                                                                                                                                                                                                             |
| --------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `-f, --format`  |         | Format output using a custom template: 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `-v, --verbose` |         | Verbose output for diagnostics                                                                                                                                                                                                          |

----
url: https://docs.docker.com/build/exporters/oci-docker/
----

# OCI and Docker exporters

***

Table of contents

***

The `oci` exporter outputs the build result into an [OCI image layout](https://github.com/opencontainers/image-spec/blob/main/image-layout.md) tarball. The `docker` exporter behaves the same way, except it exports a Docker image layout instead.

The [`docker` driver](https://docs.docker.com/build/builders/drivers/docker/) doesn't support these exporters. You must use `docker-container` or some other driver if you want to generate these outputs.

## [Synopsis](#synopsis)

Build a container image using the `oci` and `docker` exporters:

```console
$ docker buildx build --output type=oci[,parameters] .
```

```console
$ docker buildx build --output type=docker[,parameters] .
```

The following table describes the available parameters:

| Parameter           | Type                                   | Default | Description                                                                                                                                                                                                   |
| ------------------- | -------------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | String                                 |         | Specify image name(s)                                                                                                                                                                                         |
| `dest`              | String                                 |         | Path                                                                                                                                                                                                          |
| `tar`               | `true`,`false`                         | `true`  | Bundle the output into a tarball layout                                                                                                                                                                       |
| `compression`       | `uncompressed`,`gzip`,`estargz`,`zstd` | `gzip`  | Compression type, see [compression](https://docs.docker.com/build/exporters/#compression)                                                                                                                     |
| `compression-level` | `0..22`                                |         | Compression level, see [compression](https://docs.docker.com/build/exporters/#compression)                                                                                                                    |
| `force-compression` | `true`,`false`                         | `false` | Forcefully apply compression, see [compression](https://docs.docker.com/build/exporters/#compression)                                                                                                         |
| `oci-mediatypes`    | `true`,`false`                         |         | Use OCI media types in exporter manifests. Defaults to `true` for `type=oci`, and `false` for `type=docker`. See [OCI Media types](https://docs.docker.com/build/exporters/#oci-media-types)                  |
| `annotation.<key>`  | String                                 |         | Attach an annotation with the respective `key` and `value` to the built image,see [annotations](#annotations)                                                                                                 |
| `rewrite-timestamp` | `true`,`false`                         | `false` | Rewrite the file timestamps to the `SOURCE_DATE_EPOCH` value. See [build reproducibility](https://github.com/moby/buildkit/blob/master/docs/build-repro.md) for how to specify the `SOURCE_DATE_EPOCH` value. |

## [Annotations](#annotations)

These exporters support adding OCI annotation using `annotation` parameter, followed by the annotation name using dot notation. The following example sets the `org.opencontainers.image.title` annotation:

```console
$ docker buildx build \
    --output "type=<type>,name=<registry>/<image>,annotation.org.opencontainers.image.title=<title>" .
```

For more information about annotations, see [BuildKit documentation](https://github.com/moby/buildkit/blob/master/docs/annotations.md).

## [Further reading](#further-reading)

For more information on the `oci` or `docker` exporters, see the [BuildKit README](https://github.com/moby/buildkit/blob/master/README.md#docker-tarball).

----
url: https://docs.docker.com/reference/samples/ruby/
----

# Ruby samples

| Name                                                                                                             | Description                                                                                         |
| ---------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| [Compose and Rails](https://github.com/docker/awesome-compose/tree/master/official-documentation-samples/rails/) | This Quickstart guide shows you how to use Docker Compose to set up and run a Rails/PostgreSQL app. |

----
url: https://docs.docker.com/desktop/
----

# Docker Desktop

***

Table of contents

***

Docker Desktop is a one-click-install application for your Mac, Linux, or Windows environment that lets you build, share, and run containerized applications and microservices.

It provides a straightforward GUI (Graphical User Interface) that lets you manage your containers, applications, and images directly from your machine.

Docker Desktop reduces the time spent on complex setups so you can focus on writing code. It takes care of port mappings, file system concerns, and other default settings, and is regularly updated with bug fixes and security updates.

Docker Desktop integrates with your preferred development tools and languages, and gives you access to a vast ecosystem of trusted images and templates via Docker Hub. This empowers teams to accelerate development, automate builds, enable CI/CD workflows, and collaborate securely through shared repositories.

## [Key features](#key-features)

* Ability to containerize and share any application on any cloud platform, in multiple languages and frameworks.
* Quick installation and setup of a complete Docker development environment.
* Includes the latest version of Kubernetes.
* On Windows, the ability to toggle between Linux and Windows containers to build applications.
* Fast and reliable performance with native Windows Hyper-V virtualization.
* Ability to work natively on Linux through WSL 2 on Windows machines.
* Volume mounting for code and data, including file change notifications and easy access to running containers on the localhost network.

## [Products inside Docker Desktop](#products-inside-docker-desktop)

* [Docker MCP Toolkit and Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/)
* [Docker Model Runner](https://docs.docker.com/ai/model-runner/)
* [Gordon](https://docs.docker.com/ai/gordon/)
* [Docker Offload](https://docs.docker.com/offload/)
* [Docker Engine](https://docs.docker.com/engine/)
* Docker CLI client
* [Docker Build](https://docs.docker.com/build/)
* [Docker Compose](https://docs.docker.com/compose/)
* [Docker Scout](https://docs.docker.com/scout/)
* [Kubernetes](https://github.com/kubernetes/kubernetes/)

## [Next steps](#next-steps)

### Install Docker Desktop

Install Docker Desktop on [Mac](/desktop/setup/install/mac-install/), [Windows](/desktop/setup/install/windows-install/), or [Linux](/desktop/setup/install/linux/).

### [Learn about Docker Desktop](/desktop/use-desktop/)

[Navigate Docker Desktop.](/desktop/use-desktop/)

### Explore its key features

Find information about [Networking](/desktop/features/networking/), [Docker VMM](/desktop/features/vmm/), [WSL](/desktop/features/wsl/), and more.

### [View the release notes](/desktop/release-notes/)

[Find out about new features, improvements, and bug fixes.](/desktop/release-notes/)

### [Browse common FAQs](/desktop/troubleshoot-and-support/faqs/general/)

[Explore general FAQs or FAQs for specific platforms.](/desktop/troubleshoot-and-support/faqs/general/)

### [Give feedback](/desktop/troubleshoot-and-support/feedback/)

[Provide feedback on Docker Desktop or Docker Desktop features.](/desktop/troubleshoot-and-support/feedback/)

----
url: https://docs.docker.com/engine/daemon/proxy/
----

# Daemon proxy configuration

***

Table of contents

***

[]()

If your organization uses a proxy server to connect to the internet, you may need to configure the Docker daemon to use the proxy server. The daemon uses a proxy server to access images stored on Docker Hub and other registries, and to reach other nodes in a Docker swarm.

This page describes how to configure a proxy for the Docker daemon. For instructions on configuring proxy settings for the Docker CLI, see [Configure Docker CLI to use a proxy server](https://docs.docker.com/engine/cli/proxy/).

> Important
>
> Proxy configurations specified in the `daemon.json` are ignored by Docker Desktop. If you use Docker Desktop, you can configure proxies using the [Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#proxies).

There are two ways you can configure these settings:

* [Configuring the daemon](#daemon-configuration) through a configuration file or CLI flags
* Setting [environment variables](#environment-variables) on the system

Configuring the daemon directly takes precedence over environment variables.

## [Daemon configuration](#daemon-configuration)

You may configure proxy behavior for the daemon in the `daemon.json` file, or using CLI flags for the `--http-proxy` or `--https-proxy` flags for the `dockerd` command. Configuration using `daemon.json` is recommended.

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "http://proxy.example.com:3128",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }
}
```

After changing the configuration file, restart the daemon for the proxy configuration to take effect:

```console
$ sudo systemctl restart docker
```

## [Environment variables](#environment-variables)

The Docker daemon checks the following environment variables in its start-up environment to configure HTTP or HTTPS proxy behavior:

* `HTTP_PROXY`
* `http_proxy`
* `HTTPS_PROXY`
* `https_proxy`
* `NO_PROXY`
* `no_proxy`

### [systemd unit file](#systemd-unit-file)

If you're running the Docker daemon as a systemd service, you can create a systemd drop-in file that sets the variables for the `docker` service.

> **Note for rootless mode**
>
> The location of systemd configuration files are different when running Docker in [rootless mode](https://docs.docker.com/engine/security/rootless/). When running in rootless mode, Docker is started as a user-mode systemd service, and uses files stored in each users' home directory in `~/.config/systemd/<user>/docker.service.d/`. In addition, `systemctl` must be executed without `sudo` and with the `--user` flag. Select the "Rootless mode" tab if you are running Docker in rootless mode.

1. Create a systemd drop-in directory for the `docker` service:

   ```console
   $ sudo mkdir -p /etc/systemd/system/docker.service.d
   ```

2. Create a file named `/etc/systemd/system/docker.service.d/http-proxy.conf` that adds the `HTTP_PROXY` environment variable:

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   ```

   To proxy HTTPS requests, set the `HTTPS_PROXY` environment variable:

   ```systemd
   [Service]
   Environment="HTTPS_PROXY=http://proxy.example.com:3128"
   ```

   Multiple environment variables can be set; to set both an HTTP and an HTTPS proxy;

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=http://proxy.example.com:3128"
   ```

   > Note
   >
   > Special characters in the proxy value, such as `#?!()[]{}`, must be double escaped using `%%`. For example:
   >
   > ```systemd
   > [Service]
   > Environment="HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/"
   > ```

3. If you have internal Docker registries that you need to contact without proxying, you can specify them via the `NO_PROXY` environment variable.

   The `NO_PROXY` variable specifies a string that contains comma-separated values for hosts that should be excluded from proxying. These are the options you can specify to exclude hosts:

   * IP address prefix (`1.2.3.4`)

   * Domain name, or a special DNS label (`*`)

   * A domain name matches that name and all subdomains. A domain name with a leading "." matches subdomains only. For example, given the domains `foo.example.com` and `example.com`:

     * `example.com` matches `example.com` and `foo.example.com`, and
     * `.example.com` matches only `foo.example.com`

   * A single asterisk (`*`) indicates that no proxying should be done

   * Literal port numbers are accepted by IP address prefixes (`1.2.3.4:80`) and domain names (`foo.example.com:80`)

   Example:

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=http://proxy.example.com:3128"
   Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
   ```

4. Flush changes and restart Docker

   ```console
   $ sudo systemctl daemon-reload
   $ sudo systemctl restart docker
   ```

5. Verify that the configuration has been loaded and matches the changes you made, for example:

   ```console
   $ sudo systemctl show --property=Environment docker

   Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=http://proxy.example.com:3128 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
   ```

1) Create a systemd drop-in directory for the `docker` service:

   ```console
   $ mkdir -p ~/.config/systemd/user/docker.service.d
   ```

2) Create a file named `~/.config/systemd/user/docker.service.d/http-proxy.conf` that adds the `HTTP_PROXY` environment variable:

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   ```

   To proxy HTTPS requests, set the `HTTPS_PROXY` environment variable:

   ```systemd
   [Service]
   Environment="HTTPS_PROXY=http://proxy.example.com:3128"
   ```

   Multiple environment variables can be set; to set both an HTTP and an HTTPS proxy;

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=http://proxy.example.com:3128"
   ```

   > Note
   >
   > Special characters in the proxy value, such as `#?!()[]{}`, must be double escaped using `%%`. For example:
   >
   > ```systemd
   > [Service]
   > Environment="HTTP_PROXY=http://domain%%5Cuser:complex%%23pass@proxy.example.com:3128/"
   > ```

3) If you have internal Docker registries that you need to contact without proxying, you can specify them via the `NO_PROXY` environment variable.

   The `NO_PROXY` variable specifies a string that contains comma-separated values for hosts that should be excluded from proxying. These are the options you can specify to exclude hosts:

   * IP address prefix (`1.2.3.4`)

   * Domain name, or a special DNS label (`*`)

   * A domain name matches that name and all subdomains. A domain name with a leading "." matches subdomains only. For example, given the domains `foo.example.com` and `example.com`:

     * `example.com` matches `example.com` and `foo.example.com`, and
     * `.example.com` matches only `foo.example.com`

   * A single asterisk (`*`) indicates that no proxying should be done

   * Literal port numbers are accepted by IP address prefixes (`1.2.3.4:80`) and domain names (`foo.example.com:80`)

   Example:

   ```systemd
   [Service]
   Environment="HTTP_PROXY=http://proxy.example.com:3128"
   Environment="HTTPS_PROXY=http://proxy.example.com:3128"
   Environment="NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp"
   ```

4) Flush changes and restart Docker

   ```console
   $ systemctl --user daemon-reload
   $ systemctl --user restart docker
   ```

5) Verify that the configuration has been loaded and matches the changes you made, for example:

   ```console
   $ systemctl --user show --property=Environment docker

   Environment=HTTP_PROXY=http://proxy.example.com:3128 HTTPS_PROXY=http://proxy.example.com:3128 NO_PROXY=localhost,127.0.0.1,docker-registry.example.com,.corp
   ```

----
url: https://docs.docker.com/guides/testcontainers-java-spring-boot-kafka/run-tests/
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

You should see the Kafka and MySQL Docker containers start and all tests pass. After the tests finish, the containers stop and are removed automatically.

## [Summary](#summary)

Testing with real Kafka and MySQL instances gives you more confidence in the correctness of your code than mocks or embedded alternatives. The Testcontainers library manages the container lifecycle so that your integration tests run against the same services you use in production.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Getting started with Testcontainers in a Java Spring Boot project](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
* [The simplest way to replace H2 with a real database for testing](https://testcontainers.com/guides/replace-h2-with-real-database-for-testing/)
* [Awaitility](http://www.awaitility.org/)
* [Testcontainers Kafka module](https://java.testcontainers.org/modules/kafka/)
* [Testcontainers MySQL module](https://java.testcontainers.org/modules/databases/mysql/)

----
url: https://docs.docker.com/reference/cli/docker/sandbox/create/shell/
----

# docker sandbox create shell

***

| Description | Create a sandbox for shell                                   |
| ----------- | ------------------------------------------------------------ |
| Usage       | `docker sandbox create shell WORKSPACE [EXTRA_WORKSPACE...]` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Create a sandbox with access to a host workspace for shell.

The workspace path is required and will be exposed inside the sandbox at the same path as on the host. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

Use 'docker sandbox run SANDBOX' to start shell after creation.

----
url: https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/create-project/
----

# Create the Micronaut project

***

Table of contents

***

## [Set up the project](#set-up-the-project)

Create a Micronaut project from [Micronaut Launch](https://micronaut.io/launch) by selecting the **http-client**, **micronaut-test-rest-assured**, and **testcontainers** features.

Alternatively, clone the [guide repository](https://github.com/testcontainers/tc-guide-testing-rest-api-integrations-in-micronaut-apps-using-wiremock).

After generating the project, add the **WireMock** and **Testcontainers WireMock** libraries as test dependencies. The key dependencies in `pom.xml` are:

```xml
<parent>
    <groupId>io.micronaut.platform</groupId>
    <artifactId>micronaut-parent</artifactId>
    <version>4.1.2</version>
</parent>

<properties>
    <jdk.version>17</jdk.version>
    <micronaut.version>4.1.2</micronaut.version>
    <micronaut.runtime>netty</micronaut.runtime>
</properties>

<repositories>
    <repository>
        <id>jitpack.io</id>
        <url>https://jitpack.io</url>
    </repository>
</repositories>

<dependencies>
    <dependency>
        <groupId>io.micronaut</groupId>
        <artifactId>micronaut-http-client</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut</groupId>
        <artifactId>micronaut-http-server-netty</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.serde</groupId>
        <artifactId>micronaut-serde-jackson</artifactId>
        <scope>compile</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.test</groupId>
        <artifactId>micronaut-test-junit5</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.micronaut.test</groupId>
        <artifactId>micronaut-test-rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.wiremock</groupId>
        <artifactId>wiremock-standalone</artifactId>
        <version>3.2.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.wiremock.integrations.testcontainers</groupId>
        <artifactId>wiremock-testcontainers-module</artifactId>
        <version>1.0-alpha-13</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

This guide builds an application that manages video albums. A third-party REST API handles photo assets. For demonstration purposes, the application uses the publicly available [JSONPlaceholder](https://jsonplaceholder.typicode.com/) API as a photo service.

The application exposes a `GET /api/albums/{albumId}` endpoint that calls the photo service to fetch photos for a given album. [WireMock](https://wiremock.org/) is a tool for building mock APIs. Testcontainers provides a [WireMock module](https://testcontainers.com/modules/wiremock/) that runs WireMock as a Docker container.

## [Create the Album and Photo models](#create-the-album-and-photo-models)

Create `Album.java` using Java records. Annotate both records with `@Serdeable` to allow serialization and deserialization:

```java
package com.testcontainers.demo;

import io.micronaut.serde.annotation.Serdeable;
import java.util.List;

@Serdeable
public record Album(Long albumId, List<Photo> photos) {}

@Serdeable
record Photo(Long id, String title, String url, String thumbnailUrl) {}
```

## [Create the PhotoServiceClient](#create-the-photoserviceclient)

Micronaut provides [declarative HTTP client](https://docs.micronaut.io/latest/guide/#httpClient) support. Create an interface with a method that fetches photos for a given album ID:

```java
package com.testcontainers.demo;

import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.http.client.annotation.Client;
import java.util.List;

@Client(id = "photosapi")
interface PhotoServiceClient {

    @Get("/albums/{albumId}/photos")
    List<Photo> getPhotos(@PathVariable Long albumId);
}
```

The `@Client(id = "photosapi")` annotation ties this client to a named configuration. Add the following property to `src/main/resources/application.properties` to set the base URL:

```properties
micronaut.http.services.photosapi.url=https://jsonplaceholder.typicode.com
```

## [Create the REST API endpoint](#create-the-rest-api-endpoint)

Create `AlbumController.java`:

```java
package com.testcontainers.demo;

import static io.micronaut.scheduling.TaskExecutors.BLOCKING;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.http.annotation.PathVariable;
import io.micronaut.scheduling.annotation.ExecuteOn;

@Controller("/api")
class AlbumController {

    private final PhotoServiceClient photoServiceClient;

    AlbumController(PhotoServiceClient photoServiceClient) {
        this.photoServiceClient = photoServiceClient;
    }

    @ExecuteOn(BLOCKING)
    @Get("/albums/{albumId}")
    public Album getAlbumById(@PathVariable Long albumId) {
        return new Album(albumId, photoServiceClient.getPhotos(albumId));
    }
}
```

Here's what this controller does:

* `@Controller("/api")` maps the controller to the `/api` path.
* Constructor injection provides a `PhotoServiceClient` bean.
* `@ExecuteOn(BLOCKING)` offloads blocking I/O to a separate thread pool so it doesn't block the event loop.
* `@Get("/albums/{albumId}")` maps the `getAlbumById()` method to an HTTP GET request.

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

[Write tests with WireMock and Testcontainers »](https://docs.docker.com/guides/testcontainers-java-micronaut-wiremock/write-tests/)

----
url: https://docs.docker.com/guides/golang/deploy/
----

# Test your Go deployment

***

Table of contents

***

## [Prerequisites](#prerequisites)

* Complete all the previous sections of this guide, starting with [Build your Go image](https://docs.docker.com/guides/golang/build-images/).
* [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## [Overview](#overview)

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This allows you to test and debug your workloads on Kubernetes locally before deploying.

## [Create a Kubernetes YAML file](#create-a-kubernetes-yaml-file)

In your project directory, create a file named `docker-go-kubernetes.yaml`. Open the file in an IDE or text editor and add the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker username and the name of the repository that you created in [Configure CI/CD for your Go application](https://docs.docker.com/guides/golang/configure-ci-cd/).

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
        - env:
            - name: PGDATABASE
              value: mydb
            - name: PGPASSWORD
              value: whatever
            - name: PGHOST
              value: db
            - name: PGPORT
              value: "5432"
            - name: PGUSER
              value: postgres
          image: DOCKER_USERNAME/REPO_NAME
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
              value: mydb
            - name: POSTGRES_PASSWORD
              value: whatever
            - name: POSTGRES_USER
              value: postgres
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

* A Deployment, describing a scalable group of identical pods. In this case, you'll get just one replica, or copy of your pod. That pod, which is described under `template`, has just one container in it. The container is created from the image built by GitHub Actions in [Configure CI/CD for your Go application](https://docs.docker.com/guides/golang/configure-ci-cd/).
* A NodePort service, which will route traffic from port 30001 on your host to port 8080 inside the pods it routes to, allowing you to reach your app from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## [Deploy and check your application](#deploy-and-check-your-application)

1. In a terminal, navigate to the project directory and deploy your application to Kubernetes.

   ```console
   $ kubectl apply -f docker-go-kubernetes.yaml
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

3. Open a terminal and curl your application to verify that it's working.

   ```console
   $ curl --request POST \
     --url http://localhost:30001/send \
     --header 'content-type: application/json' \
     --data '{"value": "Hello, Oliver!"}'
   ```

   You should get the following message back.

   ```json
   { "value": "Hello, Oliver!" }
   ```

4. Run the following command to tear down your application.

   ```console
   $ kubectl delete -f docker-go-kubernetes.yaml
   ```

----
url: https://docs.docker.com/reference/compose-file/build/
----

# Compose Build Specification

***

Table of contents

***

Build is an optional part of the Compose Specification. It tells Compose how to (re)build an application from source and lets you define the build process within a Compose file in a portable way. `build` can be either specified as a single string defining a context path, or as a detailed build definition.

When `build` is specified as a string, the whole path is used as a Docker context to execute a Docker build, looking for a canonical `Dockerfile` at the root of the directory.

When `build` is specified as a detailed structure, build arguments can be specified, including an alternate `Dockerfile` location.

In both cases, the path can be absolute or relative. If it is relative, it is resolved from the directory containing your Compose file. If it is absolute, the path prevents the Compose file from being portable so Compose displays a warning.

## [Using `build` and `image`](#using-build-and-image)

When Compose is confronted with both a `build` subsection for a service and an `image` attribute, it follows the rules defined by the [`pull_policy`](https://docs.docker.com/reference/compose-file/services/#pull_policy) attribute.

If `pull_policy` is missing from the service definition, Compose attempts to pull the image first and then builds from source if the image isn't found in the registry or platform cache.

## [Publishing built images](#publishing-built-images)

Compose with `build` support offers an option to push built images to a registry. When doing so, it doesn't try to push service images without an `image` attribute. Compose warns you about the missing `image` attribute which prevents images being pushed.

## [Illustrative example](#illustrative-example)

The following example illustrates Compose Build Specification concepts with a concrete sample application. The sample is non-normative.

```yaml
services:
  frontend:
    image: example/webapp
    build: ./webapp

  backend:
    image: example/database
    build:
      context: backend
      dockerfile: ../backend.Dockerfile

  custom:
    build: ~/custom
```

When used to build service images from source, the Compose file creates three Docker images:

* `example/webapp`: A Docker image is built using `webapp` sub-directory, within the Compose file's folder, as the Docker build context. Lack of a `Dockerfile` within this folder returns an error.
* `example/database`: A Docker image is built using `backend` sub-directory within the Compose file's folder. `backend.Dockerfile` file is used to define build steps, this file is searched relative to the context path, which means `..` resolves to the Compose file's folder, so `backend.Dockerfile` is a sibling file.
* A Docker image is built using the `custom` directory with the user's `$HOME` as the Docker context. Compose displays a warning about the non-portable path used to build image.

On push, both `example/webapp` and `example/database` Docker images are pushed to the default registry. The `custom` service image is skipped as no `image` attribute is set and Compose displays a warning about this missing attribute.

## [Attributes](#attributes)

The `build` subsection defines configuration options that are applied by Compose to build Docker images from source. `build` can be specified either as a string containing a path to the build context or as a detailed structure:

Using the string syntax, only the build context can be configured as either:

* A relative path to the Compose file's folder. This path must be a directory and must contain a `Dockerfile`

  ```yml
  services:
    webapp:
      build: ./dir
  ```

* A Git repository URL. Git URLs accept context configuration in their fragment section, separated by a colon (`:`). The first part represents the reference that Git checks out, and can be either a branch, a tag, or a remote reference. The second part represents a subdirectory inside the repository that is used as a build context.

  ```yml
  services:
    webapp:
      build: https://github.com/mycompany/example.git#branch_or_tag:subdirectory
  ```

Alternatively `build` can be an object with fields defined as follows:

### [`additional_contexts`](#additional_contexts)

Requires: Docker Compose [2.17.0](https://github.com/docker/compose/releases/tag/v2.17.0) and later

`additional_contexts` defines a list of named contexts the image builder should use during image build.

`additional_contexts` can be a mapping or a list:

```yml
build:
  context: .
  additional_contexts:
    - resources=/path/to/resources
    - app=docker-image://my-app:latest
    - source=https://github.com/myuser/project.git
```

```yml
build:
  context: .
  additional_contexts:
    resources: /path/to/resources
    app: docker-image://my-app:latest
    source: https://github.com/myuser/project.git
```

When used as a list, the syntax follows the `NAME=VALUE` format, where `VALUE` is a string. Validation beyond that is the responsibility of the image builder (and is builder specific). Compose supports at least absolute and relative paths to a directory and Git repository URLs, like [context](#context) does. Other context flavours must be prefixed to avoid ambiguity with a `type://` prefix.

Compose warns you if the image builder does not support additional contexts and may list the unused contexts.

Refer to the reference documentation for [`docker buildx build --build-context`](https://github.com/docker/buildx/blob/master/docs/reference/buildx_build.md#-additional-build-contexts---build-context) for example usage.

`additional_contexts` can also refer to an image built by another service. This allows a service image to be built using another service image as a base image, and to share layers between service images.

```yaml
services:
  base:
    build:
      context: .
      dockerfile_inline: |
        FROM alpine
        RUN ...
  my-service:
    build:
      context: .
      dockerfile_inline: |
        FROM base # image built for service base
        RUN ...
      additional_contexts:
        base: service:base
```

### [`args`](#args)

`args` define build arguments, that is Dockerfile `ARG` values.

Using the following Dockerfile as an example:

```Dockerfile
ARG GIT_COMMIT
RUN echo "Based on commit: $GIT_COMMIT"
```

`args` can be set in the Compose file under the `build` key to define `GIT_COMMIT`. `args` can be set as a mapping or a list:

```yml
build:
  context: .
  args:
    GIT_COMMIT: cdc3b19
```

```yml
build:
  context: .
  args:
    - GIT_COMMIT=cdc3b19
```

Values can be omitted when specifying a build argument, in which case its value at build time must be obtained by user interaction, otherwise the build argument won't be set when building the Docker image.

```yml
args:
  - GIT_COMMIT
```

### [`cache_from`](#cache_from)

`cache_from` defines a list of sources the image builder should use for cache resolution.

Cache location syntax follows the global format `[NAME|type=TYPE[,KEY=VALUE]]`. Simple `NAME` is actually a shortcut notation for `type=registry,ref=NAME`.

Compose Build implementations may support custom types, the Compose Specification defines canonical types which must be supported:

* `registry` to retrieve build cache from an OCI image set by key `ref`

```yml
build:
  context: .
  cache_from:
    - alpine:latest
    - type=local,src=path/to/cache
    - type=gha
```

Unsupported caches are ignored and don't prevent you from building images.

### [`cache_to`](#cache_to)

`cache_to` defines a list of export locations to be used to share build cache with future builds.

```yml
build:
  context: .
  cache_to:
    - user/app:cache
    - type=local,dest=path/to/cache
```

Cache target is defined using the same `type=TYPE[,KEY=VALUE]` syntax defined by [`cache_from`](#cache_from).

Unsupported caches are ignored and don't prevent you from building images.

### [`context`](#context)

`context` defines either a path to a directory containing a Dockerfile, or a URL to a Git repository.

When the value supplied is a relative path, it is interpreted as relative to the project directory. Compose warns you about the absolute path used to define the build context as those prevent the Compose file from being portable.

```yml
build:
  context: ./dir
```

```yml
services:
  webapp:
    build: https://github.com/mycompany/webapp.git
```

If not set explicitly, `context` defaults to project directory (`.`).

### [`dockerfile`](#dockerfile)

`dockerfile` sets an alternate Dockerfile. A relative path is resolved from the build context. Compose warns you about the absolute path used to define the Dockerfile as it prevents Compose files from being portable.

When set, `dockerfile_inline` attribute is not allowed and Compose rejects any Compose file having both set.

```yml
build:
  context: .
  dockerfile: webapp.Dockerfile
```

### [`dockerfile_inline`](#dockerfile_inline)

Requires: Docker Compose [2.17.0](https://github.com/docker/compose/releases/tag/v2.17.0) and later

`dockerfile_inline` defines the Dockerfile content as an inlined string in a Compose file. When set, the `dockerfile` attribute is not allowed and Compose rejects any Compose file having both set.

Use of YAML multi-line string syntax is recommended to define the Dockerfile content:

```yml
build:
  context: .
  dockerfile_inline: |
    FROM baseimage
    RUN some command
```

### [`entitlements`](#entitlements)

Requires: Docker Compose [2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1) and later

`entitlements` defines extra privileged entitlements to be allowed during the build.

```yaml
entitlements:
  - network.host
  - security.insecure
```

### [`extra_hosts`](#extra_hosts)

`extra_hosts` adds hostname mappings at build-time. Use the same syntax as [`extra_hosts`](https://docs.docker.com/reference/compose-file/services/#extra_hosts).

```yml
extra_hosts:
  - "somehost=162.242.195.82"
  - "otherhost=50.31.209.229"
  - "myhostv6=::1"
```

IPv6 addresses can be enclosed in square brackets, for example:

```yml
extra_hosts:
  - "myhostv6=[::1]"
```

The separator `=` is preferred, but `:` can also be used. Introduced in Docker Compose version [2.24.1](https://github.com/docker/compose/releases/tag/v2.24.1). For example:

```yml
extra_hosts:
  - "somehost:162.242.195.82"
  - "myhostv6:::1"
```

Compose creates matching entry with the IP address and hostname in the container's network configuration, which means for Linux `/etc/hosts` will get extra lines:

```text
162.242.195.82  somehost
50.31.209.229   otherhost
::1             myhostv6
```

### [`isolation`](#isolation)

`isolation` specifies a build’s container isolation technology. Like [isolation](https://docs.docker.com/reference/compose-file/services/#isolation), supported values are platform specific.

### [`labels`](#labels)

`labels` add metadata to the resulting image. `labels` can be set either as an array or a map.

It's recommended that you use reverse-DNS notation to prevent your labels from conflicting with other software.

```yml
build:
  context: .
  labels:
    com.example.description: "Accounting webapp"
    com.example.department: "Finance"
    com.example.label-with-empty-value: ""
```

```yml
build:
  context: .
  labels:
    - "com.example.description=Accounting webapp"
    - "com.example.department=Finance"
    - "com.example.label-with-empty-value"
```

### [`network`](#network)

Set the network containers connect to for the `RUN` instructions during build.

```yaml
build:
  context: .
  network: host
```

```yaml
build:
  context: .
  network: custom_network_1
```

Use `none` to disable networking during build:

```yaml
build:
  context: .
  network: none
```

### [`no_cache`](#no_cache)

`no_cache` disables image builder cache and enforces a full rebuild from source for all image layers. This only applies to layers declared in the Dockerfile, referenced images can be retrieved from local image store whenever tag has been updated on registry (see [pull](#pull)).

### [`platforms`](#platforms)

`platforms` defines a list of target [platforms](https://docs.docker.com/reference/compose-file/services/#platform).

```yml
build:
  context: "."
  platforms:
    - "linux/amd64"
    - "linux/arm64"
```

When the `platforms` attribute is omitted, Compose includes the service's platform in the list of the default build target platforms.

When the `platforms` attribute is defined, Compose includes the service's platform, otherwise users won't be able to run images they built.

Composes reports an error in the following cases:

* When the list contains multiple platforms but the implementation is incapable of storing multi-platform images.

* When the list contains an unsupported platform.

  ```yml
  build:
    context: "."
    platforms:
      - "linux/amd64"
      - "unsupported/unsupported"
  ```

* When the list is non-empty and does not contain the service's platform.

  ```yml
  services:
    frontend:
      platform: "linux/amd64"
      build:
        context: "."
        platforms:
          - "linux/arm64"
  ```

### [`privileged`](#privileged)

Requires: Docker Compose [2.15.0](https://github.com/docker/compose/releases/tag/v2.15.0) and later

`privileged` configures the service image to build with elevated privileges. Support and actual impacts are platform specific.

```yml
build:
  context: .
  privileged: true
```

### [`provenance`](#provenance)

Requires: Docker Compose [2.39.0](https://github.com/docker/compose/releases/tag/v2.39.0) and later

`provenance` configures the builder to add a [provenance attestation](https://slsa.dev/provenance/v0.2#schema) to the published image.

The value can be either a boolean to enable/disable provenance attestation, or a key=value string to set provenance configuration. You can use this to select the level of detail to be included in the provenance attestation by setting the `mode` parameter.

```yaml
build:
  context: .
  provenance: true
```

```yaml
build:
  context: .
  provenance: mode=max
```

### [`pull`](#pull)

`pull` requires the image builder to pull referenced images (`FROM` Dockerfile directive), even if those are already available in the local image store.

### [`sbom`](#sbom)

Requires: Docker Compose [2.39.0](https://github.com/docker/compose/releases/tag/v2.39.0) and later

`sbom` configures the builder to add a [provenance attestation](https://slsa.dev/provenance/v0.2#schema) to the published image. The value can be either a boolean to enable/disable sbom attestation, or a key=value string to set SBOM generator configuration. This let you select an alternative SBOM generator image (see <https://github.com/moby/buildkit/blob/master/docs/attestations/sbom-protocol.md>)

```yaml
build:
  context: .
  sbom: true
```

```yaml
build:
  context: .
  sbom: generator=docker/scout-sbom-indexer:latest # Use an alternative SBOM generator
```

### [`secrets`](#secrets)

`secrets` grants access to sensitive data defined by [secrets](https://docs.docker.com/reference/compose-file/services/#secrets) on a per-service build basis. Two different syntax variants are supported: the short syntax and the long syntax.

Compose reports an error if the secret isn't defined in the [`secrets`](https://docs.docker.com/reference/compose-file/secrets/) section of this Compose file.

#### [Short syntax](#short-syntax)

The short syntax variant only specifies the secret name. This grants the container access to the secret and mounts it as read-only to `/run/secrets/<secret_name>` within the container. The source name and destination mountpoint are both set to the secret name.

The following example uses the short syntax to grant the build of the `frontend` service access to the `server-certificate` secret. The value of `server-certificate` is set to the contents of the file `./server.cert`.

```yml
services:
  frontend:
    build:
      context: .
      secrets:
        - server-certificate
secrets:
  server-certificate:
    file: ./server.cert
```

#### [Long syntax](#long-syntax)

The long syntax provides more granularity in how the secret is created within the service's containers.

* `source`: The name of the secret as it exists on the platform.
* `target`: The ID of the secret as declared in the Dockerfile. Defaults to `source` if not specified.
* `uid` and `gid`: The numeric uid or gid that owns the file within `/run/secrets/` in the service's task containers. Default value is `USER`.
* `mode`: The [permissions](https://wintelguy.com/permissions-calc.pl) for the file to be mounted in `/run/secrets/` in the service's task containers, in octal notation. Default value is world-readable permissions (mode `0444`). The writable bit must be ignored if set. The executable bit may be set.

The following example sets the name of the `server-certificate` secret file to `server.crt` within the container, sets the mode to `0440` (group-readable) and sets the user and group to `103`. The value of `server-certificate` secret is provided by the platform through a lookup and the secret lifecycle not directly managed by Compose.

```yml
services:
  frontend:
    build:
      context: .
      secrets:
        - source: server-certificate
          target: cert # secret ID in Dockerfile
          uid: "103"
          gid: "103"
          mode: 0440
secrets:
  server-certificate:
    external: true
```

```dockerfile
# Dockerfile
FROM nginx
RUN --mount=type=secret,id=cert,required=true,target=/root/cert ...
```

Service builds may be granted access to multiple secrets. Long and short syntax for secrets may be used in the same Compose file. Defining a secret in the top-level `secrets` must not imply granting any service build access to it. Such grant must be explicit within service specification as [secrets](https://docs.docker.com/reference/compose-file/services/#secrets) service element.

### [`ssh`](#ssh)

`ssh` defines SSH authentications that the image builder should use during image build (e.g., cloning private repository).

`ssh` property syntax can be either:

* `default`: Let the builder connect to the SSH-agent.
* `ID=path`: A key/value definition of an ID and the associated path. It can be either a [PEM](https://en.wikipedia.org/wiki/Privacy-Enhanced_Mail) file, or path to ssh-agent socket.

```yaml
build:
  context: .
  ssh:
    - default # mount the default SSH agent
```

or

```yaml
build:
  context: .
  ssh: ["default"] # mount the default SSH agent
```

Using a custom id `myproject` with path to a local SSH key:

```yaml
build:
  context: .
  ssh:
    - myproject=~/.ssh/myproject.pem
```

The image builder can then rely on this to mount the SSH key during build.

For illustration, [SSH mounts](https://github.com/moby/buildkit/blob/master/frontend/dockerfile/docs/reference.md#run---mounttypessh) can be used to mount the SSH key set by ID and access a secured resource:

```console
RUN --mount=type=ssh,id=myproject git clone ...
```

### [`shm_size`](#shm_size)

`shm_size` sets the size of the shared memory (`/dev/shm` partition on Linux) allocated for building Docker images. Specify as an integer value representing the number of bytes or as a string expressing a [byte value](https://docs.docker.com/reference/compose-file/extension/#specifying-byte-values).

```yml
build:
  context: .
  shm_size: "2gb"
```

```yaml
build:
  context: .
  shm_size: 10000000
```

### [`tags`](#tags)

`tags` defines a list of tag mappings that must be associated to the build image. This list comes in addition to the `image` [property defined in the service section](https://docs.docker.com/reference/compose-file/services/#image)

```yml
tags:
  - "myimage:mytag"
  - "registry/username/myrepos:my-other-tag"
```

### [`target`](#target)

`target` defines the stage to build as defined inside a multi-stage `Dockerfile`.

```yml
build:
  context: .
  target: prod
```

### [`ulimits`](#ulimits)

Requires: Docker Compose [2.23.1](https://github.com/docker/compose/releases/tag/v2.23.1) and later

`ulimits` overrides the default `ulimits` for a container. It's specified either as an integer for a single limit or as mapping for soft/hard limits.

```yml
services:
  frontend:
    build:
      context: .
      ulimits:
        nproc: 65535
        nofile:
          soft: 20000
          hard: 40000
```

----
url: https://docs.docker.com/reference/cli/docker/image/save/
----

# docker image save

***

| Description                                                               | Save one or more images to a tar archive (streamed to STDOUT by default) |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Usage                                                                     | `docker image save [OPTIONS] IMAGE [IMAGE...]`                           |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker save`                                                            |

## [Description](#description)

Produces a tarred repository to the standard output stream. Contains all parent layers, and all tags + versions, or specified `repo:tag`, for each argument provided.

## [Options](#options)

| Option                    | Default | Description                                                                                                                                   |
| ------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `-o, --output`            |         | Write to a file, instead of STDOUT                                                                                                            |
| [`--platform`](#platform) |         | API 1.48+ Save only the given platform(s). Formatted as a comma-separated list of `os[/arch[/variant]]` (e.g., `linux/amd64,linux/arm64/v8`)  |

## [Examples](#examples)

### [Create a backup that can then be used with `docker load`.](#create-a-backup-that-can-then-be-used-with-docker-load)

```console
$ docker save busybox > busybox.tar

$ ls -sh busybox.tar

2.7M busybox.tar

$ docker save --output busybox.tar busybox

$ ls -sh busybox.tar

2.7M busybox.tar

$ docker save -o fedora-all.tar fedora

$ docker save -o fedora-latest.tar fedora:latest
```

### [Save an image to a tar.gz file using gzip](#save-an-image-to-a-targz-file-using-gzip)

You can use gzip to save the image file and make the backup smaller.

```console
$ docker save myimage:latest | gzip > myimage_latest.tar.gz
```

### [Cherry-pick particular tags](#cherry-pick-particular-tags)

You can even cherry-pick particular tags of an image repository.

```console
$ docker save -o ubuntu.tar ubuntu:lucid ubuntu:saucy
```

### [Save a specific platform (--platform)](#platform)

The `--platform` option allows you to specify which platform variant of the image to save. By default, `docker save` saves all platform variants that are present in the daemon's image store. Use the `--platform` option to specify which platform variant of the image to save. An error is produced if the given platform is not present in the local image store.

The platform option takes the `os[/arch[/variant]]` format; for example, `linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional, and default to the daemon's native architecture if omitted.

The following example pulls the RISC-V variant of the `alpine:latest` image and saves it to a tar archive.

```console
$ docker pull --platform=linux/riscv64 alpine:latest
latest: Pulling from library/alpine
8c4a05189a5f: Download complete
Digest: sha256:beefdbd8a1da6d2915566fde36db9db0b524eb737fc57cd1367effd16dc0d06d
Status: Downloaded newer image for alpine:latest
docker.io/library/alpine:latest

$ docker image save --platform=linux/riscv64 -o alpine-riscv.tar alpine:latest

$ ls -lh image.tar
-rw-------  1 thajeztah  staff   3.9M Oct  7 11:06 alpine-riscv.tar
```

The following example attempts to save a platform variant of `alpine:latest` that doesn't exist in the local image store, resulting in an error.

```console
$ docker image ls --tree
IMAGE                   ID             DISK USAGE   CONTENT SIZE   IN USE
alpine:latest           beefdbd8a1da       10.6MB         3.37MB
├─ linux/riscv64        80cde017a105       10.6MB         3.37MB
├─ linux/amd64          33735bd63cf8           0B             0B
├─ linux/arm/v6         50f635c8b04d           0B             0B
├─ linux/arm/v7         f2f82d424957           0B             0B
├─ linux/arm64/v8       9cee2b382fe2           0B             0B
├─ linux/386            b3e87f642f5c           0B             0B
├─ linux/ppc64le        c7a6800e3dc5           0B             0B
└─ linux/s390x          2b5b26e09ca2           0B             0B

$ docker image save --platform=linux/s390x -o alpine-s390x.tar alpine:latest
Error response from daemon: no suitable export target found for platform linux/s390x
```

----
url: https://docs.docker.com/reference/cli/docker/compose/rm/
----

# docker compose rm

***

| Description | Removes stopped service containers         |
| ----------- | ------------------------------------------ |
| Usage       | `docker compose rm [OPTIONS] [SERVICE...]` |

## [Description](#description)

Removes stopped service containers.

By default, anonymous volumes attached to containers are not removed. You can override this with `-v`. To list all volumes, use `docker volume ls`.

Any data which is not in a volume is lost.

Running the command with no options also removes one-off containers created by `docker compose run`:

```console
$ docker compose rm
Going to remove djangoquickstart_web_run_1
Are you sure? [yN] y
Removing djangoquickstart_web_run_1 ... done
```

## [Options](#options)

| Option          | Default | Description                                         |
| --------------- | ------- | --------------------------------------------------- |
| `-f, --force`   |         | Don't ask to confirm removal                        |
| `-s, --stop`    |         | Stop the containers, if required, before removing   |
| `-v, --volumes` |         | Remove any anonymous volumes attached to containers |

----
url: https://docs.docker.com/build/bake/expressions/
----

# Expression evaluation in Bake

***

Table of contents

***

Bake files in the HCL format support expression evaluation, which lets you perform arithmetic operations, conditionally set values, and more.

## [Arithmetic operations](#arithmetic-operations)

You can perform arithmetic operations in expressions. The following example shows how to multiply two numbers.

docker-bake.hcl

```hcl
sum = 7*6

target "default" {
  args = {
    answer = sum
  }
}
```

Printing the Bake file with the `--print` flag shows the evaluated value for the `answer` build argument.

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "answer": "42"
      }
    }
  }
}
```

## [Ternary operators](#ternary-operators)

You can use ternary operators to conditionally register a value.

The following example adds a tag only when a variable is not empty, using the built-in `notequal` [function](https://docs.docker.com/build/bake/funcs/).

docker-bake.hcl

```hcl
variable "TAG" {}

target "default" {
  context="."
  dockerfile="Dockerfile"
  tags = [
    "my-image:latest",
    notequal("",TAG) ? "my-image:${TAG}": ""
  ]
}
```

In this case, `TAG` is an empty string, so the resulting build configuration only contains the hard-coded `my-image:latest` tag.

```console
$ docker buildx bake --print
```

```json
{
  "target": {
    "default": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "tags": ["my-image:latest"]
    }
  }
}
```

## [Expressions with variables](#expressions-with-variables)

You can use expressions with [variables](https://docs.docker.com/build/bake/variables/) to conditionally set values, or to perform arithmetic operations.

The following example uses expressions to set values based on the value of variables. The `v1` build argument is set to "higher" if the variable `FOO` is greater than 5, otherwise it is set to "lower". The `v2` build argument is set to "yes" if the `IS_FOO` variable is true, otherwise it is set to "no".

docker-bake.hcl

```hcl
variable "FOO" {
  default = 3
}

variable "IS_FOO" {
  default = true
}

target "app" {
  args = {
    v1 = FOO > 5 ? "higher" : "lower"
    v2 = IS_FOO ? "yes" : "no"
  }
}
```

Printing the Bake file with the `--print` flag shows the evaluated values for the `v1` and `v2` build arguments.

```console
$ docker buildx bake --print app
```

```json
{
  "group": {
    "default": {
      "targets": ["app"]
    }
  },
  "target": {
    "app": {
      "context": ".",
      "dockerfile": "Dockerfile",
      "args": {
        "v1": "lower",
        "v2": "yes"
      }
    }
  }
}
```

----
url: https://docs.docker.com/reference/cli/docker/inspect/
----

# docker inspect

***

| Description | Return low-level information on Docker objects    |
| ----------- | ------------------------------------------------- |
| Usage       | `docker inspect [OPTIONS] NAME\|ID [NAME\|ID...]` |

## [Description](#description)

Docker inspect provides detailed information on constructs controlled by Docker.

By default, `docker inspect` will render results in a JSON array.

## [Options](#options)

| Option                    | Default | Description                                                                                                                                                                                                                             |
| ------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-f, --format`](#format) |         | Format output using a custom template: 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| [`-s, --size`](#size)     |         | Display total file sizes if the type is container                                                                                                                                                                                       |
| [`--type`](#type)         |         | Only inspect objects of the given type                                                                                                                                                                                                  |

## [Examples](#examples)

### [Format the output (--format)](#format)

If a format is specified, the given template will be executed for each result.

Go's [text/template](https://pkg.go.dev/text/template) package describes all the details of the format.

### [Specify target type (--type)](#type)

`--type config|container|image|node|network|secret|service|volume|task|plugin`

The `docker inspect` command matches any type of object by either ID or name. In some cases multiple type of objects (for example, a container and a volume) exist with the same name, making the result ambiguous.

To restrict `docker inspect` to a specific type of object, use the `--type` option.

The following example inspects a volume named `myvolume`.

```console
$ docker inspect --type=volume myvolume
```

### [Inspect the size of a container (-s, --size)](#size)

The `--size`, or short-form `-s`, option adds two additional fields to the `docker inspect` output. This option only works for containers. The container doesn't have to be running, it also works for stopped containers.

```console
$ docker inspect --size mycontainer
```

The output includes the full output of a regular `docker inspect` command, with the following additional fields:

* `SizeRootFs`: the total size of all the files in the container, in bytes.
* `SizeRw`: the size of the files that have been created or changed in the container, compared to it's image, in bytes.

```console
$ docker run --name database -d redis
3b2cbf074c99db4a0cad35966a9e24d7bc277f5565c17233386589029b7db273
$ docker inspect --size database -f '{{ .SizeRootFs }}'
123125760
$ docker inspect --size database -f '{{ .SizeRw }}'
8192
$ docker exec database fallocate -l 1000 /newfile
$ docker inspect --size database -f '{{ .SizeRw }}'
12288
```

### [Get an instance's IP address](#get-an-instances-ip-address)

For the most part, you can pick out any field from the JSON in a fairly straightforward manner.

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $INSTANCE_ID
```

### [Get an instance's MAC address](#get-an-instances-mac-address)

```console
$ docker inspect --format='{{range .NetworkSettings.Networks}}{{.MacAddress}}{{end}}' $INSTANCE_ID
```

### [Get an instance's log path](#get-an-instances-log-path)

```console
$ docker inspect --format='{{.LogPath}}' $INSTANCE_ID
```

### [Get an instance's image name](#get-an-instances-image-name)

```console
$ docker inspect --format='{{.Config.Image}}' $INSTANCE_ID
```

### [List all port bindings](#list-all-port-bindings)

You can loop over arrays and maps in the results to produce simple text output:

```console
$ docker inspect --format='{{range $p, $conf := .NetworkSettings.Ports}} {{$p}} -> {{with $conf}}{{(index . 0).HostPort}}{{else}}none{{end}} {{end}}' $INSTANCE_ID
```

### [Find a specific port mapping](#find-a-specific-port-mapping)

The `.Field` syntax doesn't work when the field name begins with a number, but the template language's `index` function does. The `.NetworkSettings.Ports` section contains a map of the internal port mappings to a list of external address/port objects. To grab just the numeric public port, you use `index` to find the specific port map, and then `index` 0 contains the first object inside of that. Then, specify the `HostPort` field to get the public address.

```console
$ docker inspect --format='{{(index (index .NetworkSettings.Ports "8787/tcp") 0).HostPort}}' $INSTANCE_ID
```

### [Get a subsection in JSON format](#get-a-subsection-in-json-format)

If you request a field which is itself a structure containing other fields, by default you get a Go-style dump of the inner values. Docker adds a template function, `json`, which can be applied to get results in JSON format.

```console
$ docker inspect --format='{{json .Config}}' $INSTANCE_ID
```

----
url: https://docs.docker.com/reference/cli/docker/model/restart-runner/
----

# docker model restart-runner

***

| Description | Restart Docker Model Runner (Docker Engine only) |
| ----------- | ------------------------------------------------ |
| Usage       | `docker model restart-runner`                    |

## [Description](#description)

This command restarts the Docker Model Runner without pulling container images. Use this command to restart the runner when you already have the required images locally.

For the first-time setup or to ensure you have the latest images, use `docker model install-runner` instead.

## [Options](#options)

| Option           | Default     | Description                                                                                             |
| ---------------- | ----------- | ------------------------------------------------------------------------------------------------------- |
| `--debug`        |             | Enable debug logging                                                                                    |
| `--do-not-track` |             | Do not track models usage in Docker Model Runner                                                        |
| `--gpu`          | `auto`      | Specify GPU support (none\|auto\|cuda\|rocm\|musa\|cann)                                                |
| `--host`         | `127.0.0.1` | Host address to bind Docker Model Runner                                                                |
| `--port`         |             | Docker container port for Docker Model Runner (default: 12434 for Docker Engine, 12435 for Cloud mode)  |
| `--proxy-cert`   |             | Path to a CA certificate file for proxy SSL inspection                                                  |

----
url: https://docs.docker.com/reference/cli/sbx/template/rm/
----

# sbx template rm

| Description | Remove a template image           |
| ----------- | --------------------------------- |
| Usage       | `sbx template rm TAG\|ID [flags]` |

## [Description](#description)

Remove a template image from the sandbox runtime's image store.

The image can be identified by tag (e.g. "myimage:v1.0") or by image ID (full or prefix, e.g. "abc123"). Use "sbx template ls" to see available images and their IDs.

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Remove by tag
sbx template rm myimage:v1.0

# Remove by image ID (prefix)
sbx template rm abc123
```

----
url: https://docs.docker.com/get-started/introduction/build-and-push-first-image/
----

# Build and push your first image

***

Table of contents

***

## [Explanation](#explanation)

Now that you've updated the [to-do list app](https://docs.docker.com/get-started/introduction/develop-with-containers/), you’re ready to create a container image for the application and share it on Docker Hub. To do so, you will need to do the following:

1. Sign in with your Docker account
2. Create an image repository on Docker Hub
3. Build the container image
4. Push the image to Docker Hub

Before you dive into the hands-on guide, the following are a few core concepts that you should be aware of.

### [Container images](#container-images)

If you’re new to container images, think of them as a standardized package that contains everything needed to run an application, including its files, configuration, and dependencies. These packages can then be distributed and shared with others.

### [Docker Hub](#docker-hub)

To share your Docker images, you need a place to store them. This is where registries come in. While there are many registries, Docker Hub is the default and go-to registry for images. Docker Hub provides both a place for you to store your own images and to find images from others to either run or use as the bases for your own images.

When choosing base images, Docker Hub offers two categories of trusted, Docker-maintained images:

* [Docker Official Images (DOI)](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images) – Curated images for popular software, following best practices and regularly updated.
* [Docker Hardened Images (DHI)](https://docs.docker.com/dhi/) – Minimal, secure, production-ready images with near-zero CVEs, designed to reduce attack surface and simplify compliance. DHI images are free and open source under Apache 2.0.

In [Develop with containers](https://docs.docker.com/get-started/introduction/develop-with-containers/), you used the following images that came from Docker Hub, each of which are [Docker Official Images](https://docs.docker.com/docker-hub/image-library/trusted-content/#docker-official-images):

* [node](https://hub.docker.com/_/node) - provides a Node environment and is used as the base of your development efforts. This image is also used as the base for the final application image.
* [mysql](https://hub.docker.com/_/mysql) - provides a MySQL database to store the to-do list items
* [phpmyadmin](https://hub.docker.com/_/phpmyadmin) - provides phpMyAdmin, a web-based interface to the MySQL database
* [traefik](https://hub.docker.com/_/traefik) - provides Traefik, a modern HTTP reverse proxy and load balancer that routes requests to the appropriate container based on routing rules

Explore the full catalog of trusted content on Docker Hub:

* [Docker Official Images](https://hub.docker.com/search?badges=official) – Curated images for popular software
* [Docker Hardened Images](https://hub.docker.com/hardened-images/catalog) – Security-hardened, minimal production images (also available at [dhi.io](https://dhi.io))
* [Docker Verified Publishers](https://hub.docker.com/search?badges=verified_publisher) – Images from verified software vendors
* [Docker Sponsored Open Source](https://hub.docker.com/search?badges=open_source) – Images from sponsored OSS projects

## [Try it out](#try-it-out)

In this hands-on guide, you'll learn how to sign in to Docker Hub and push images to Docker Hub repository.

## [Sign in with your Docker account](#sign-in-with-your-docker-account)

To push images to Docker Hub, you will need to sign in with a Docker account.

1. Open the Docker Dashboard.

2. Select **Sign in** at the top-right corner.

3. If needed, create an account and then complete the sign-in flow.

Once you're done, you should see the **Sign in** button turn into a profile picture.

## [Create an image repository](#create-an-image-repository)

Now that you have an account, you can create an image repository. Just as a Git repository holds source code, an image repository stores container images.

1. Go to [Docker Hub](https://hub.docker.com).

2. Select **Create repository**.

3. On the **Create repository** page, enter the following information:

   * **Repository name** - `getting-started-todo-app`
   * **Short description** - feel free to enter a description if you'd like
   * **Visibility** - select **Public** to allow others to pull your customized to-do app

4. Select **Create** to create the repository.

## [Build and push the image](#build-and-push-the-image)

Now that you have a repository, you are ready to build and push your image. An important note is that the image you are building extends the Node image, meaning you don't need to install or configure Node, yarn, etc. You can simply focus on what makes your application unique.

> **What is an image/Dockerfile?**
>
> Without going too deep yet, think of a container image as a single package that contains everything needed to run a process. In this case, it will contain a Node environment, the backend code, and the compiled React code.
>
> Any machine that runs a container using the image, will then be able to run the application as it was built without needing anything else pre-installed on the machine.
>
> A `Dockerfile` is a text-based script that provides the instruction set on how to build the image. For this quick start, the repository already contains the Dockerfile.

1. To get started, either clone or [download the project as a ZIP file](https://github.com/docker/getting-started-todo-app/archive/refs/heads/main.zip) to your local machine.

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   And after the project is cloned, navigate into the new directory created by the clone:

   ```console
   $ cd getting-started-todo-app
   ```

2. Build the project by running the following command, swapping out `DOCKER_USERNAME` with your username.

   ```console
   $ docker build -t DOCKER_USERNAME/getting-started-todo-app .
   ```

   For example, if your Docker username was `mobydock`, you would run the following:

   ```console
   $ docker build -t mobydock/getting-started-todo-app .
   ```

3. To verify the image exists locally, you can use the `docker image ls` command:

   ```console
   $ docker image ls
   ```

   You will see output similar to the following:

   ```console
   REPOSITORY                          TAG       IMAGE ID       CREATED          SIZE
   mobydock/getting-started-todo-app   latest    1543656c9290   2 minutes ago    1.12GB
   ...
   ```

4. To push the image, use the `docker push` command. Be sure to replace `DOCKER_USERNAME` with your username:

   ```console
   $ docker push DOCKER_USERNAME/getting-started-todo-app
   ```

   Depending on your upload speeds, this may take a moment to push.

1) Open Visual Studio Code. Ensure you have the **Docker extension for VS Code** installed from [Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker).

2) In the **File** menu, select **Open Folder**. Choose **Clone Git Repository** and paste this URL: <https://github.com/docker/getting-started-todo-app>

3) Right-click the `Dockerfile` and select the **Build Image...** menu item.

4) In the dialog that appears, enter a name of `DOCKER_USERNAME/getting-started-todo-app`, replacing `DOCKER_USERNAME` with your Docker username.

5) After pressing **Enter**, you'll see a terminal appear where the build will occur. Once it's completed, feel free to close the terminal.

6) Open the Docker Extension for VS Code by selecting the Docker logo in the left nav menu.

7) Find the image you created. It'll have a name of `docker.io/DOCKER_USERNAME/getting-started-todo-app`.

8) Expand the image to view the tags (or different versions) of the image. You should see a tag named `latest`, which is the default tag given to an image.

9) Right-click on the **latest** item and select the **Push...** option.

10) Press **Enter** to confirm and then watch as your image is pushed to Docker Hub. Depending on your upload speeds, it might take a moment to push the image.

    Once the upload is finished, feel free to close the terminal.

## [Recap](#recap)

Before you move on, take a moment and reflect on what happened here. Within a few moments, you were able to build a container image that packages your application and push it to Docker Hub.

Going forward, you’ll want to remember that:

* Docker Hub is the go-to registry for finding trusted content. Docker provides a collection of trusted content, composed of Docker Official Images, Docker Verified Publishers, and Docker Sponsored Open Source Software, to use directly or as bases for your own images.

* Docker Hub provides a marketplace to distribute your own applications. Anyone can create an account and distribute images. While you are publicly distributing the image you created, private repositories can ensure your images are accessible to only authorized users.

> **Usage of other registries**
>
> While Docker Hub is the default registry, registries are standardized and made interoperable through the [Open Container Initiative](https://opencontainers.org/). This allows companies and organizations to run their own private registries. Quite often, trusted content is mirrored (or copied) from Docker Hub into these private registries.

## [Next steps](#next-steps)

Now that you’ve built an image, it's time to discuss why you as a developer should learn more about Docker and how it will help you in your day-to-day tasks.

[What's Next](https://docs.docker.com/get-started/introduction/whats-next/)

----
url: https://docs.docker.com/guides/rust/configure-ci-cd/
----

# Configure CI/CD for your Rust application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete the previous sections of this guide, starting with [Develop your Rust application](https://docs.docker.com/guides/rust/develop/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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

3. In the editor window, copy and paste the following YAML configuration.

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
             push: true
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

In this section, you learned how to set up a GitHub Actions workflow for your Rust application.

Related information:

* [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
* [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
* [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## [Next steps](#next-steps)

Next, learn how you can locally test and debug your workloads on Kubernetes before deploying.

[Test your Rust deployment »](https://docs.docker.com/guides/rust/deploy/)

----
url: https://docs.docker.com/engine/extend/plugin_api/
----

# Docker Plugin API

***

Table of contents

***

Docker plugins are out-of-process extensions which add capabilities to the Docker Engine.

This document describes the Docker Engine plugin API. To view information on plugins managed by Docker Engine, refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

This page is intended for people who want to develop their own Docker plugin. If you just want to learn about or use Docker plugins, look [here](https://docs.docker.com/engine/extend/legacy_plugins/).

## [What plugins are](#what-plugins-are)

A plugin is a process running on the same or a different host as the Docker daemon, which registers itself by placing a file on the daemon host in one of the plugin directories described in [Plugin discovery](#plugin-discovery).

Plugins have human-readable names, which are short, lowercase strings. For example, `myplugin`.

Plugins can run inside or outside containers. Currently running them outside containers is recommended.

## [Plugin discovery](#plugin-discovery)

Docker discovers plugins by looking for them in the plugin directory whenever a user or container tries to use one by name.

There are three types of files which can be put in the plugin directory.

* `.sock` files are Unix domain sockets.
* `.spec` files are text files containing a URL, such as `unix:///other.sock` or `tcp://localhost:8080`.
* `.json` files are text files containing a full json specification for the plugin.

Plugins with Unix domain socket files must run on the same host as the Docker daemon. Plugins with `.spec` or `.json` files can run on a different host if you specify a remote URL.

Unix domain socket files must be located under `/run/docker/plugins`, whereas spec files can be located either under `/etc/docker/plugins` or `/usr/lib/docker/plugins`.

The name of the file (excluding the extension) determines the plugin name.

For example, a plugin named `myplugin` might create a Unix socket at `/run/docker/plugins/myplugin.sock`.

You can define each plugin into a separated subdirectory if you want to isolate definitions from each other. For example, you can create the `myplugin` socket under `/run/docker/plugins/myplugin/myplugin.sock` and only mount `/run/docker/plugins/myplugin` inside the `myplugin` container.

Docker always searches for Unix sockets in `/run/docker/plugins` first. It checks for spec or json files under `/etc/docker/plugins` and `/usr/lib/docker/plugins` if the socket doesn't exist. The directory scan stops as soon as it finds the first plugin definition with the given name.

### [JSON specification](#json-specification)

This is the JSON format for a plugin:

```json
{
  "Name": "plugin-example",
  "Addr": "https://example.com/docker/plugin",
  "TLSConfig": {
    "InsecureSkipVerify": false,
    "CAFile": "/usr/shared/docker/certs/example-ca.pem",
    "CertFile": "/usr/shared/docker/certs/example-cert.pem",
    "KeyFile": "/usr/shared/docker/certs/example-key.pem"
  }
}
```

The `TLSConfig` field is optional and TLS will only be verified if this configuration is present.

## [Plugin lifecycle](#plugin-lifecycle)

Plugins should be started before Docker, and stopped after Docker. For example, when packaging a plugin for a platform which supports `systemd`, you might use [`systemd` dependencies](https://www.freedesktop.org/software/systemd/man/systemd.unit.html#Before=) to manage startup and shutdown order.

When upgrading a plugin, you should first stop the Docker daemon, upgrade the plugin, then start Docker again.

## [Plugin activation](#plugin-activation)

When a plugin is first referred to -- either by a user referring to it by name (e.g. `docker run --volume-driver=foo`) or a container already configured to use a plugin being started -- Docker looks for the named plugin in the plugin directory and activates it with a handshake. See Handshake API below.

Plugins are not activated automatically at Docker daemon startup. Rather, they are activated only lazily, or on-demand, when they are needed.

## [Systemd socket activation](#systemd-socket-activation)

Plugins may also be socket activated by `systemd`. The official [Plugins helpers](https://github.com/docker/go-plugins-helpers) natively supports socket activation. In order for a plugin to be socket activated it needs a `service` file and a `socket` file.

The `service` file (for example `/lib/systemd/system/your-plugin.service`):

```systemd
[Unit]
Description=Your plugin
Before=docker.service
After=network.target your-plugin.socket
Requires=your-plugin.socket docker.service

[Service]
ExecStart=/usr/lib/docker/your-plugin

[Install]
WantedBy=multi-user.target
```

The `socket` file (for example `/lib/systemd/system/your-plugin.socket`):

```systemd
[Unit]
Description=Your plugin

[Socket]
ListenStream=/run/docker/plugins/your-plugin.sock

[Install]
WantedBy=sockets.target
```

This will allow plugins to be actually started when the Docker daemon connects to the sockets they're listening on (for instance the first time the daemon uses them or if one of the plugin goes down accidentally).

## [API design](#api-design)

The Plugin API is RPC-style JSON over HTTP, much like webhooks.

Requests flow from the Docker daemon to the plugin. The plugin needs to implement an HTTP server and bind this to the Unix socket mentioned in the "plugin discovery" section.

All requests are HTTP `POST` requests.

The API is versioned via an Accept header, which currently is always set to `application/vnd.docker.plugins.v1+json`.

## [Handshake API](#handshake-api)

Plugins are activated via the following "handshake" API call.

### [/Plugin.Activate](#pluginactivate)

Request: empty body

Response:

```json
{
    "Implements": ["VolumeDriver"]
}
```

Responds with a list of Docker subsystems which this plugin implements. After activation, the plugin will then be sent events from this subsystem.

Possible values are:

* [`authz`](https://docs.docker.com/engine/extend/plugins_authorization/)
* [`NetworkDriver`](https://docs.docker.com/engine/extend/plugins_network/)
* [`VolumeDriver`](https://docs.docker.com/engine/extend/plugins_volume/)

## [Plugin retries](#plugin-retries)

Attempts to call a method on a plugin are retried with an exponential backoff for up to 30 seconds. This may help when packaging plugins as containers, since it gives plugin containers a chance to start up before failing any user containers which depend on them.

## [Plugins helpers](#plugins-helpers)

To ease plugins development, we're providing an `sdk` for each kind of plugins currently supported by Docker at [docker/go-plugins-helpers](https://github.com/docker/go-plugins-helpers).

----
url: https://docs.docker.com/guides/rust/deploy/
----

# Test your Rust deployment

***

Table of contents

***

## [Prerequisites](#prerequisites)

* Complete the previous sections of this guide, starting with [Develop your Rust application](https://docs.docker.com/guides/rust/develop/).
* [Turn on Kubernetes](https://docs.docker.com/desktop/use-desktop/kubernetes/#enable-kubernetes) in Docker Desktop.

## [Overview](#overview)

In this section, you'll learn how to use Docker Desktop to deploy your application to a fully-featured Kubernetes environment on your development machine. This lets you to test and debug your workloads on Kubernetes locally before deploying.

## [Create a Kubernetes YAML file](#create-a-kubernetes-yaml-file)

In your `docker-rust-postgres` directory, create a file named `docker-rust-kubernetes.yaml`. Open the file in an IDE or text editor and add the following contents. Replace `DOCKER_USERNAME/REPO_NAME` with your Docker username and the name of the repository that you created in [Configure CI/CD for your Rust application](https://docs.docker.com/guides/rust/configure-ci-cd/).

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
            - containerPort: 8000
              hostPort: 5000
              protocol: TCP
          env:
            - name: ADDRESS
              value: 0.0.0.0:8000
            - name: PG_DBNAME
              value: example
            - name: PG_HOST
              value: db
            - name: PG_PASSWORD
              value: mysecretpassword
            - name: PG_USER
              value: postgres
            - name: RUST_LOG
              value: debug
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
              value: mysecretpassword
            - name: POSTGRES_USER
              value: postgres
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
    - name: "5000"
      port: 5000
      targetPort: 8000
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

* A Deployment, describing a scalable group of identical pods. In this case, you'll get just one replica, or copy of your pod. That pod, which is described under `template`, has just one container in it. The container is created from the image built by GitHub Actions in [Configure CI/CD for your Rust application](https://docs.docker.com/guides/rust/configure-ci-cd/).
* A NodePort service, which will route traffic from port 30001 on your host to port 5000 inside the pods it routes to, allowing you to reach your app from the network.

To learn more about Kubernetes objects, see the [Kubernetes documentation](https://kubernetes.io/docs/home/).

## [Deploy and check your application](#deploy-and-check-your-application)

1. In a terminal, navigate to `docker-rust-postgres` and deploy your application to Kubernetes.

   ```console
   $ kubectl apply -f docker-rust-kubernetes.yaml
   ```

   You should see output that looks like the following, indicating your Kubernetes objects were created successfully.

   ```shell
   deployment.apps/server created
   deployment.apps/db created
   service/server created
   service/db created
   ```

2. Make sure everything worked by listing your deployments.

   ```console
   $ kubectl get deployments
   ```

   Your deployment should be listed as follows:

   ```shell
   NAME                 READY   UP-TO-DATE   AVAILABLE   AGE
   db       1/1     1            1           2m21s
   server   1/1     1            1           2m21s
   ```

   This indicates all of the pods you asked for in your YAML are up and running. Do the same check for your services.

   ```console
   $ kubectl get services
   ```

   You should get output like the following.

   ```shell
   NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
   db           ClusterIP   10.105.167.81    <none>        5432/TCP         109s
   kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          9d
   server       NodePort    10.101.235.213   <none>        5000:30001/TCP   109s
   ```

   In addition to the default `kubernetes` service, you can see your `service-entrypoint` service, accepting traffic on port 30001/TCP.

3. In a terminal, curl the service.

   ```console
   $ curl http://localhost:30001/users
   [{"id":1,"login":"root"}]
   ```

4. Run the following command to tear down your application.

   ```console
   $ kubectl delete -f docker-rust-kubernetes.yaml
   ```

----
url: https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/
----

# Design guidelines for Docker extensions

***

Table of contents

***

At Docker, we aim to build tools that integrate into a user's existing workflows rather than requiring them to adopt new ones. We strongly recommend that you follow these guidelines when creating extensions. We review and approve your Marketplace publication based on these requirements.

Here is a simple checklist to go through when creating your extension:

* Is it easy to get started?
* Is it easy to use?
* Is it easy to get help when needed?

## [Create a consistent experience with Docker Desktop](#create-a-consistent-experience-with-docker-desktop)

Use the [Docker Material UI Theme](https://www.npmjs.com/package/@docker/docker-mui-theme) and the [Docker Extensions Styleguide](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771) to ensure that your extension feels like it is part of Docker Desktop to create a seamless experience for users.

* Ensure the extension has both a light and dark theme. Using the components and styles as per the Docker style guide ensures that your extension meets the [level AA accessibility standard.](https://www.w3.org/WAI/WCAG2AA-Conformance).

* Ensure that your extension icon is visible both in light and dark mode.

* Ensure that the navigational behavior is consistent with the rest of Docker Desktop. Add a header to set the context for the extension.

* Avoid embedding terminal windows. The advantage we have with Docker Desktop over the CLI is that we have the opportunity to provide rich information to users. Make use of this interface as much as possible.

## [Build features natively](#build-features-natively)

* In order not to disrupt the flow of users, avoid scenarios where the user has to navigate outside Docker Desktop, to the CLI or a webpage for example, in order to carry out certain functionalities. Instead, build features that are native to Docker Desktop.

## [Break down complicated user flows](#break-down-complicated-user-flows)

* If a flow is too complicated or the concept is abstract, break down the flow into multiple steps with one simple call-to-action in each step. This helps when onboarding novice users to your extension

* Where there are multiple call-to-actions, ensure you use the primary (filled button style) and secondary buttons (outline button style) to convey the importance of each action.

## [Onboarding new users](#onboarding-new-users)

When creating your extension, ensure that first time users of the extension and your product can understand its value-add and adopt it easily. Ensure you include contextual help within the extension.

* Ensure that all necessary information is added to the extensions Marketplace as well as the extensions detail page. This should include:

  * Screenshots of the extension. Note that the recommended size for screenshots is 2400x1600 pixels.
  * A detailed description that covers what the purpose of the extension is, who would find it useful and how it works.
  * Link to necessary resources such as documentation.

* If your extension has particularly complex functionality, add a demo or video to the start page. This helps onboard a first time user quickly.

## [What's next?](#whats-next)

* Explore our [design principles](https://docs.docker.com/extensions/extensions-sdk/design/design-principles/).
* Take a look at our [UI styling guidelines](https://docs.docker.com/extensions/extensions-sdk/design/).
* Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

----
url: https://docs.docker.com/get-started/docker-concepts/building-images/
----

# Building images

Table of contents

***

Building container images is both technical and an art. You want to keep the image small and focused to increase your security posture, but also need to balance potential tradeoffs, such as caching impacts. In this series, you’ll deep dive into the secrets of images, how they are built and best practices.

**Skill level** Beginner

**Time to complete** 25 minutes

**Prerequisites** None

## [About this series](#about-this-series)

Learn how to build production-ready images that are lean and efficient Docker images, essential for minimizing overhead and enhancing deployment in production environments.

## [What you'll learn](#what-youll-learn)

* Understanding image layers
* Writing a Dockerfile
* Build, tag and publish an image
* Using the build cache
* Multi-stage builds

## [Modules](#modules)

1. [Understanding the image layers](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/)

   This concept page will teach you about the layers of container image.

2. [Writing a Dockerfile](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)

   This concept page will teach you how to create image using Dockerfile.

3. [Build, tag, and publish an image](https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/)

   This concept page will teach you how to build, tag, and publish an image to Docker Hub or any other registry

4. [Using the build cache](https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/)

   This concept page will teach you about the build cache, what changes invalidate the cache and how to effectively use the build cache.

5. [Multi-stage builds](https://docs.docker.com/get-started/docker-concepts/building-images/multi-stage-builds/)

   This concept page will teach you about the purpose of the multi-stage build and its benefits

----
url: https://docs.docker.com/guides/go-prometheus-monitoring/compose/
----

# Connecting services with Docker Compose

***

Table of contents

***

Now that you have containerized the Golang application, you will use Docker Compose to connect your services together. You will connect the Golang application, Prometheus, and Grafana services together to monitor the Golang application with Prometheus and Grafana.

## [Creating a Docker Compose file](#creating-a-docker-compose-file)

Create a new file named `compose.yml` in the root directory of your Golang application. The Docker Compose file contains instructions to run multiple services and connect them together.

Here is a Docker Compose file for a project that uses Golang, Prometheus, and Grafana. You will also find this file in the `go-prometheus-monitoring` directory.

```yaml
services:
  api:
    container_name: go-api
    build:
      context: .
      dockerfile: Dockerfile
    image: go-api:latest
    ports:
      - 8000:8000
    networks:
      - go-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
    develop:
      watch:
        - path: .
          action: rebuild
      
  prometheus:
    container_name: prometheus
    image: prom/prometheus:v2.55.0
    volumes:
      - ./Docker/prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - 9090:9090
    networks:
      - go-network
  
  grafana:
    container_name: grafana
    image: grafana/grafana:11.3.0
    volumes:
      - ./Docker/grafana.yml:/etc/grafana/provisioning/datasources/datasource.yaml
      - grafana-data:/var/lib/grafana
    ports:
      - 3000:3000
    networks:
      - go-network
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=password

volumes:
  grafana-data:

networks:
  go-network:
    driver: bridge
```

## [Understanding the Docker Compose file](#understanding-the-docker-compose-file)

The Docker Compose file consists of three services:

* **Golang application service**: This service builds the Golang application using the Dockerfile and runs it in a container. It exposes the application's port `8000` and connects to the `go-network` network. It also defines a health check to monitor the application's health. You have also used `healthcheck` to monitor the health of the application. The health check runs every 30 seconds and retries 5 times if the health check fails. The health check uses the `curl` command to check the `/health` endpoint of the application. Apart from the health check, you have also added a `develop` section to watch the changes in the application's source code and rebuild the application using the Docker Compose Watch feature.

* **Prometheus service**: This service runs the Prometheus server in a container. It uses the official Prometheus image `prom/prometheus:v2.55.0`. It exposes the Prometheus server on port `9090` and connects to the `go-network` network. You have also mounted the `prometheus.yml` file from the `Docker` directory which is present in the root directory of your project. The `prometheus.yml` file contains the Prometheus configuration to scrape the metrics from the Golang application. This is how you connect the Prometheus server to the Golang application.

  ```yaml
  global:
    scrape_interval: 10s
    evaluation_interval: 10s

  scrape_configs:
    - job_name: myapp
      static_configs:
        - targets: ["api:8000"]
  ```

  In the `prometheus.yml` file, you have defined a job named `myapp` to scrape the metrics from the Golang application. The `targets` field specifies the target to scrape the metrics from. In this case, the target is the Golang application running on port `8000`. The `api` is the service name of the Golang application in the Docker Compose file. The Prometheus server will scrape the metrics from the Golang application every 10 seconds.

* **Grafana service**: This service runs the Grafana server in a container. It uses the official Grafana image `grafana/grafana:11.3.0`. It exposes the Grafana server on port `3000` and connects to the `go-network` network. You have also mounted the `grafana.yml` file from the `Docker` directory which is present in the root directory of your project. The `grafana.yml` file contains the Grafana configuration to add the Prometheus data source. This is how you connect the Grafana server to the Prometheus server. In the environment variables, you have set the Grafana admin user and password, which will be used to log in to the Grafana dashboard.

  ```yaml
  apiVersion: 1
  datasources:
  - name: Prometheus (Main)
    type: prometheus
