url: https://docs.docker.com/reference/api/engine/version/v1.45/
----

# Docker Engine API (1.45)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.45.yaml)

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

If you omit the version-prefix, the current version of the API (v1.45) is used. For example, calling `/info` is the same as calling `/v1.45/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

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

/v1.45/containers/json

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

/v1.45/containers/create

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

/v1.45/containers/{id}/json

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

/v1.45/containers/{id}/top

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

/v1.45/containers/{id}/logs

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

/v1.45/containers/{id}/changes

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

/v1.45/containers/{id}/export

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

/v1.45/containers/{id}/stats

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

/v1.45/containers/{id}/resize

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

/v1.45/containers/{id}/start

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

/v1.45/containers/{id}/stop

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

/v1.45/containers/{id}/restart

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

/v1.45/containers/{id}/kill

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

/v1.45/containers/{id}/update

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

/v1.45/containers/{id}/rename

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

/v1.45/containers/{id}/pause

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

/v1.45/containers/{id}/unpause

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

/v1.45/containers/{id}/attach

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

/v1.45/containers/{id}/attach/ws

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

/v1.45/containers/{id}/wait

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

/v1.45/containers/{id}

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

/v1.45/containers/{id}/archive

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

/v1.45/containers/{id}/archive

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

/v1.45/containers/{id}/archive

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

/v1.45/containers/prune

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

### Responses

/v1.45/images/json

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
"Containers": 2
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

/v1.45/build

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

/v1.45/build/prune

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

/v1.45/images/create

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

/v1.45/images/{name}/json

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
"DockerVersion": "20.10.7",
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

/v1.45/images/{name}/history

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

|     |                                                                                                                                                                 |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tag | stringTag of the image to push. For example, `latest`. If no tag is provided, all tags of the given image that are present in the local image store are pushed. |

##### header Parameters

|                         |                                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| X-Registry-Authrequired | stringA base64url-encoded auth configuration.Refer to the [authentication section](#section/Authentication) for details. |

### Responses

/v1.45/images/{name}/push

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

/v1.45/images/{name}/tag

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

/v1.45/images/{name}

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

/v1.45/images/search

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

/v1.45/images/prune

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

/v1.45/commit

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

/v1.45/images/{name}/get

## [](#tag/Image/operation/ImageGetAll)Export several images

Get a tarball containing all images and metadata for several image repositories.

For each value of the `names` parameter: if it is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|       |                                          |
| ----- | ---------------------------------------- |
| names | Array of stringsImage names to filter by |

### Responses

/v1.45/images/get

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

/v1.45/images/load

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

/v1.45/networks

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

/v1.45/networks/{id}

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

/v1.45/networks/{id}

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

|                |                                                                                                                                                                                                                                        |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Namerequired   | stringThe network's name.                                                                                                                                                                                                              |
| CheckDuplicate | booleanDeprecated: CheckDuplicate is now always enabled.                                                                                                                                                                               |
| Driver         | stringDefault: "bridge"Name of the network driver plugin to use.                                                                                                                                                                       |
| Scope          | stringThe level at which the network exists (e.g. `swarm` for cluster-wide or `local` for machine level).                                                                                                                              |
| Internal       | booleanRestrict external access to the network.                                                                                                                                                                                        |
| Attachable     | booleanGlobally scoped network is manually attachable by regular containers from workers in swarm mode.                                                                                                                                |
| Ingress        | booleanIngress network is the network which provides the routing-mesh in swarm mode.                                                                                                                                                   |
| ConfigOnly     | booleanDefault: falseCreates a config-only network. Config-only networks are placeholder networks for network configurations to be used by other networks. Config-only networks cannot be used directly to run containers or services. |
|                | object (ConfigReference)The config-only network source to provide the configuration for this network.                                                                                                                                  |
|                | object (IPAM)                                                                                                                                                                                                                          |
| EnableIPv6     | booleanEnable IPv6 on the network.                                                                                                                                                                                                     |
|                | objectNetwork specific options to be used by the drivers.                                                                                                                                                                              |
|                | objectUser-defined key/value metadata.                                                                                                                                                                                                 |

### Responses

/v1.45/networks/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "my_network",
"CheckDuplicate": true,
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
"Id": "22be93d5babb089c5aab8dbc369042fad48ff791584ca2da2100db837a1c7c30",
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

/v1.45/networks/{id}/connect

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

/v1.45/networks/{id}/disconnect

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

/v1.45/networks/prune

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

/v1.45/volumes

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

/v1.45/volumes/create

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

/v1.45/volumes/{name}

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

/v1.45/volumes/{name}

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

/v1.45/volumes/{name}

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

/v1.45/volumes/prune

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

/v1.45/containers/{id}/exec

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

/v1.45/exec/{id}/start

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

/v1.45/exec/{id}/resize

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

/v1.45/exec/{id}/json

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

/v1.45/swarm

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

/v1.45/swarm/init

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

/v1.45/swarm/join

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

/v1.45/swarm/leave

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

/v1.45/swarm/update

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

/v1.45/swarm/unlockkey

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

/v1.45/swarm/unlock

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

/v1.45/nodes

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

/v1.45/nodes/{id}

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

/v1.45/nodes/{id}

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

/v1.45/nodes/{id}/update

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

/v1.45/services

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

/v1.45/services/create

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
"Mode": 0
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

/v1.45/services/{id}

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

/v1.45/services/{id}

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

/v1.45/services/{id}/update

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
"Mode": 0
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

/v1.45/services/{id}/logs

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

/v1.45/tasks

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

/v1.45/tasks/{id}

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

/v1.45/tasks/{id}/logs

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

/v1.45/secrets

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

/v1.45/secrets/create

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

/v1.45/secrets/{id}

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

/v1.45/secrets/{id}

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

/v1.45/secrets/{id}/update

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

/v1.45/configs

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

/v1.45/configs/create

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

/v1.45/configs/{id}

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

/v1.45/configs/{id}

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

/v1.45/configs/{id}/update

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

/v1.45/plugins

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

/v1.45/plugins/privileges

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

/v1.45/plugins/pull

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

/v1.45/plugins/{name}/json

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

/v1.45/plugins/{name}

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

/v1.45/plugins/{name}/enable

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

/v1.45/plugins/{name}/disable

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

/v1.45/plugins/{name}/upgrade

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

/v1.45/plugins/create

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

/v1.45/plugins/{name}/push

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

/v1.45/plugins/{name}/set

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

/v1.45/auth

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

/v1.45/info

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
"KernelVersion": "4.9.38-moby",
"OperatingSystem": "Alpine Linux v3.5",
"OSVersion": "16.04",
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
"ServerVersion": "24.0.2",
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
]
}`

## [](#tag/System/operation/SystemVersion)Get version

Returns the version of Docker that is running and various information about the system that Docker is running on.

### Responses

/v1.45/version

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
"Version": "19.03.12",
"Details": { }
}
],
"Version": "19.03.12",
"ApiVersion": "1.40",
"MinAPIVersion": "1.12",
"GitCommit": "48a66213fe",
"GoVersion": "go1.13.14",
"Os": "linux",
"Arch": "amd64",
"KernelVersion": "4.19.76-linuxkit",
"Experimental": true,
"BuildTime": "2020-06-22T15:49:27.000000000+00:00"
}`

## [](#tag/System/operation/SystemPing)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.45/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.45/\_ping

## [](#tag/System/operation/SystemEvents)Monitor events

Stream real-time events from the server.

Various objects within Docker report events when something happens to them.

Containers report these events: `attach`, `commit`, `copy`, `create`, `destroy`, `detach`, `die`, `exec_create`, `exec_detach`, `exec_start`, `exec_die`, `export`, `health_status`, `kill`, `oom`, `pause`, `rename`, `resize`, `restart`, `start`, `stop`, `top`, `unpause`, `update`, and `prune`

Images report these events: `delete`, `import`, `load`, `pull`, `push`, `save`, `tag`, `untag`, and `prune`

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

/v1.45/events

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

/v1.45/system/df

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

/v1.45/distribution/{name}/json

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

/v1.45/session

----
url: https://docs.docker.com/reference/samples/typescript/
----

# TypeScript samples

| Name                                                                                    | Description                                                                    |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| [Angular](https://github.com/docker/awesome-compose/tree/master/angular)                | A sample Angular application.                                                  |
| [dotnet-album-viewer](https://github.com/dockersamples/dotnet-album-viewer)             | West Wind Album Viewer ASP.NET Core and Angular sample.                        |
| [link-shortener-typescript](https://github.com/dockersamples/link-shortener-typescript) | A Simple URL Shortener built using TypeScript and Nest.js powered with Docker. |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/dhi/explore/feedback/
----

# Give feedback

***

Table of contents

***

Committed to maintaining the quality, security, and reliability of the Docker Hardened Images (DHI) a repository has been created as a point of contact to encourage the community to collaborate in improving the Hardened Images ecosystem.

## [Questions or discussions](#questions-or-discussions)

You can use the [GitHub Discussions board](https://github.com/orgs/docker-hardened-images/discussions) to engage with the DHI team for:

* General questions about DHIs
* Best practices and recommendations
* Security tips and advice
* Show and tell your implementations
* Community announcements

## [Reporting bugs or issues](#reporting-bugs-or-issues)

You can [open a new issue](https://github.com/docker-hardened-images/catalog/issues) for topics such as:

* Bug reports
* Feature requests
* Documentation improvements
* Security vulnerabilities (see security policy)

It's encouraged to first search existing issues to see if it’s already been reported. The DHI team reviews reports regularly and appreciates clear, actionable feedback.

## [Responsible security disclosure](#responsible-security-disclosure)

It is forbidden to post details of vulnerabilities before coordinated disclosure and resolution.

If you discover a security vulnerability, report it responsibly by following Docker’s [security disclosure](https://www.docker.com/trust/vulnerability-disclosure-policy/).

----
url: https://docs.docker.com/scout/explore/image-details-view/
----

# Image details view

***

Table of contents

***

The image details view shows a breakdown of the Docker Scout analysis. You can access the image view from the Docker Scout Dashboard, the Docker Desktop **Images** view, and from the image tag page on Docker Hub. The image details show a breakdown of the image hierarchy (base images), image layers, packages, and vulnerabilities.

Docker Desktop first analyzes images locally, where it generates a software bill of materials (SBOM). Docker Desktop, Docker Hub, and the Docker Scout Dashboard and CLI all use the [package URL (PURL) links](https://github.com/package-url/purl-spec) in this SBOM to query for matching Common Vulnerabilities and Exposures (CVEs) in [Docker Scout's advisory database](https://docs.docker.com/scout/deep-dive/advisory-db-sources/).

## [Image hierarchy](#image-hierarchy)

The image you inspect may have one or more base images represented under **Image hierarchy**. This means the author of the image used other images as starting points when building the image. Often these base images are either operating system images such as Debian, Ubuntu, and Alpine, or programming language images such as PHP, Python, and Java.

Selecting each image in the chain lets you see which layers originate from each base image. Selecting the **ALL** row selects all layers and base images.

One or more of the base images may have updates available, which may include updated security patches that remove vulnerabilities from your image. Any base images with available updates are noted to the right of **Image hierarchy**.

## [Layers](#layers)

A Docker image consists of layers. Image layers are listed from top to bottom, with the earliest layer at the top and the most recent layer at the bottom. Often, the layers at the top of the list originate from a base image, and the layers towards the bottom added by the image author, often using commands in a Dockerfile. Selecting a base image under **Image hierarchy** highlights with layers originate from a base image.

Selecting individual or multiple layers filters the packages and vulnerabilities on the right-hand side to show what the selected layers added.

## [Vulnerabilities](#vulnerabilities)

The **Vulnerabilities** tab displays a list of vulnerabilities and exploits detected in the image. The list is grouped by package, and sorted in order of severity.

You can find further information on the vulnerability or exploit, including if a fix is available, by expanding the list item.

## [Remediation recommendations](#remediation-recommendations)

When you inspect an image in Docker Desktop or Docker Hub, Docker Scout can provide recommendations for improving the security of that image.

### [Recommendations in Docker Desktop](#recommendations-in-docker-desktop)

To view security recommendations for an image in Docker Desktop:

1. Go to the **Images** view in Docker Desktop.
2. Select the image tag that you want to view recommendations for.
3. Near the top, select the **Recommended fixes** drop-down button.

The drop-down menu lets you choose whether you want to see recommendations for the current image or any base images used to build it:

* [**Recommendations for this image**](#recommendations-for-current-image) provides recommendations for the current image that you're inspecting.
* [**Recommendations for base image**](#recommendations-for-base-image) provides recommendations for base images used to build the image.

If the image you're viewing has no associated base images, the drop-down menu only shows the option to view recommendations for the current image.

### [Recommendations in Docker Hub](#recommendations-in-docker-hub)

To view security recommendations for an image in Docker Hub:

1. Go to the repository page for an image where you have activated Docker Scout image analysis.

2. Open the **Tags** tab.

3. Select the tag that you want to view recommendations for.

4. Select the **View recommended base image fixes** button.

   This opens a window which gives you recommendations for you can improve the security of your image by using better base images. See [Recommendations for base image](#recommendations-for-base-image) for more details.

### [Recommendations for current image](#recommendations-for-current-image)

The recommendations for the current image view helps you determine whether the image version that you're using is out of date. If the tag you're using is referencing an old digest, the view shows a recommendation to update the tag by pulling the latest version.

Select the **Pull new image** button to get the updated version. Check the checkbox to remove the old version after pulling the latest.

### [Recommendations for base image](#recommendations-for-base-image)

The base image recommendations view contains two tabs for toggling between different types of recommendations:

* **Refresh base image**
* **Change base image**

These base image recommendations are only actionable if you're the author of the image you're inspecting. This is because changing the base image for an image requires you to update the Dockerfile and re-build the image.

#### [Refresh base image](#refresh-base-image)

This tab shows if the selected base image tag is the latest available version, or if it's outdated.

If the base image tag used to build the current image isn't the latest, then the delta between the two versions shows in this window. The delta information includes:

* The tag name, and aliases, of the recommended (newer) version
* The age of the current base image version
* The age of the latest available version
* The number of CVEs affecting each version

At the bottom of the window, you also receive command snippets that you can run to re-build the image using the latest version.

#### [Change base image](#change-base-image)

This tab shows different alternative tags that you can use, and outlines the benefits and disadvantages of each tag version. Selecting the base image shows recommended options for that tag.

For example, if the image you're inspecting is using an old version of `debian` as a base image, it shows recommendations for newer and more secure versions of `debian` to use. By providing more than one alternative to choose from, you can see for yourself how the options compare with each other, and decide which one to use.

Select a tag recommendation to see further details of the recommendation. It shows the benefits and potential disadvantages of the tag, why it's a recommended, and how to update your Dockerfile to use this version.

----
url: https://docs.docker.com/reference/cli/docker/sandbox/network/
----

# docker sandbox network

***

| Description | Manage sandbox networking |
| ----------- | ------------------------- |
| Usage       | `docker sandbox network`  |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Manage sandbox networking

## [Examples](#examples)

### [View network logs](#view-network-logs)

```console
$ docker sandbox network log
```

### [Configure proxy for a sandbox](#configure-proxy-for-a-sandbox)

```console
$ docker sandbox network proxy my-sandbox --block-host example.com
```

See the subcommands for more details:

* [`docker sandbox network log`](/reference/cli/docker/sandbox/network/log/) - Show network logs
* [`docker sandbox network proxy`](/reference/cli/docker/sandbox/network/proxy/) - Manage proxy configuration

## [Subcommands](#subcommands)

| Command                                                                                               | Description                              |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------- |
| [`docker sandbox network log`](https://docs.docker.com/reference/cli/docker/sandbox/network/log/)     | Show network logs                        |
| [`docker sandbox network proxy`](https://docs.docker.com/reference/cli/docker/sandbox/network/proxy/) | Manage proxy configuration for a sandbox |

----
url: https://docs.docker.com/docker-hub/usage/pulls/
----

# Docker Hub pull usage and limits

***

Table of contents

***

Unauthenticated and Docker Personal users are subject to a 6-hour pull rate limit on Docker Hub. In contrast, Docker Pro, Team, and Business users benefit from an unlimited pull rate.

The following pull usage and limits apply based on your subscription, subject to fair use:

| User type                | Pull rate limit per 6 hours             |
| ------------------------ | --------------------------------------- |
| Business (authenticated) | Unlimited                               |
| Team (authenticated)     | Unlimited                               |
| Pro (authenticated)      | Unlimited                               |
| Personal (authenticated) | 200                                     |
| Unauthenticated Users    | 100 per IPv4 address or IPv6 /64 subnet |

## [Pull definition](#pull-definition)

A pull is defined as the following:

* A Docker pull includes both a version check and any download that occurs as a result of the pull. Depending on the client, a `docker pull` can verify the existence of an image or tag without downloading it by performing a version check.
* Version checks do not count towards usage pricing.
* A pull for a normal image makes one pull for a [single manifest](https://github.com/opencontainers/image-spec/blob/main/manifest.md).
* A pull for a multi-arch image will count as one pull for each different architecture.

## [Pull attribution](#pull-attribution)

Pulls from authenticated users can be attributed to either a personal or an [organization namespace](https://docs.docker.com/accounts/general-faqs/#whats-an-organization-name-or-namespace).

Attribution is based on the following:

* Private pulls: Pulls for private repositories are attributed to the repository's namespace owner.

* Public pulls: When pulling images from a public repository, attribution is determined based on domain affiliation and organization membership.

* Verified domain ownership: When pulling an image from an account linked to a verified domain, the attribution is set to be the owner of that [domain](https://docs.docker.com/enterprise/security/single-sign-on/faqs/domain-faqs/).

* Single organization membership:

  * If the owner of the verified domain is a company and the user is part of only one organization within that [company](https://docs.docker.com/admin/company/company-faqs/), the pull is attributed to that specific organization.
  * If the user is part of only one organization, the pull is attributed to that specific organization.

* Multiple organization memberships: If the user is part of multiple organizations under the company, the pull is attributed to the user's personal namespace.

### [Authentication](#authentication)

To ensure correct attribution of your pulls, you must authenticate with Docker Hub. The following sections provide information on how to sign in to Docker Hub to authenticate your pulls.

#### [Docker Desktop](#docker-desktop)

If you are using Docker Desktop, you can sign in to Docker Hub from the Docker Desktop menu.

Select **Sign in / Create Docker ID** from the Docker Desktop menu and follow the on-screen instructions to complete the sign-in process.

#### [Docker Engine](#docker-engine)

If you're using a standalone version of Docker Engine, run the `docker login` command from a terminal to authenticate with Docker Hub. For information on how to use the command, see [docker login](/reference/cli/docker/login/).

#### [Docker Swarm](#docker-swarm)

If you're running Docker Swarm, you must use the `--with-registry-auth` flag to authenticate with Docker Hub. For more information, see [Create a service](/reference/cli/docker/service/create/#with-registry-auth). If you are using a Docker Compose file to deploy an application stack, see [docker stack deploy](/reference/cli/docker/stack/deploy/).

#### [GitHub Actions](#github-actions)

If you're using GitHub Actions to build and push Docker images to Docker Hub, see [login action](https://github.com/docker/login-action#dockerhub). If you are using another Action, you must add your username and access token in a similar way for authentication.

#### [Kubernetes](#kubernetes)

If you're running Kubernetes, follow the instructions in [Pull an Image from a Private Registry](https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/) for information on authentication.

#### [Third-party platforms](#third-party-platforms)

If you're using any third-party platforms, follow your provider’s instructions on using registry authentication.

> Note
>
> When pulling images via a third-party platform, the platform may use the same IPv4 address or IPv6 /64 subnet to pull images for multiple users. Even if you are authenticated, pulls attributed to a single IPv4 address or IPv6 /64 subnet may cause [abuse rate limiting](https://docs.docker.com/docker-hub/usage/#abuse-rate-limit).

* [Artifactory](https://www.jfrog.com/confluence/display/JFROG/Advanced+Settings#AdvancedSettings-RemoteCredentials)
* [AWS CodeBuild](https://aws.amazon.com/blogs/devops/how-to-use-docker-images-from-a-private-registry-in-aws-codebuild-for-your-build-environment/)
* [AWS ECS/Fargate](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/private-auth.html)
* [Azure Pipelines](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/service-endpoints?view=azure-devops\&tabs=yaml)
* [Chipper CI](https://docs.chipperci.com/builds/docker/#rate-limit-auth)
* [CircleCI](https://circleci.com/docs/guides/execution-managed/private-images/)
* [Codefresh](https://codefresh.io/docs/docs/docker-registries/external-docker-registries/docker-hub/)
* [Drone.io](https://docs.drone.io/pipeline/docker/syntax/images/#pulling-private-images)
* [GitLab](https://docs.gitlab.com/ee/user/packages/container_registry/#authenticate-with-the-container-registry)
* [LayerCI](https://layerci.com/docs/advanced-workflows#logging-in-to-docker)
* [TeamCity](https://www.jetbrains.com/help/teamcity/integrating-teamcity-with-docker.html#Conforming+with+Docker+download+rate+limits)

## [View monthly pulls and included usage](#view-monthly-pulls-and-included-usage)

You can view your monthly pulls on the [Usage page](https://hub.docker.com/usage/pulls) in Docker Hub.

On that page, you can also send a report to your email that contains a comma separated file with the following detailed information.

| CSV column           | Definition                                                                                                                                                                                                         | Usage guidance                                                                                                                                                                      |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `datehour`           | The date and hour (`yyyy/mm/dd/hh`) of the pull that resulted in the data transfer.                                                                                                                                | This helps in identifying peak usage times and patterns.                                                                                                                            |
| `user_name`          | The Docker ID of the user that pulled the image                                                                                                                                                                    | This lets organization owners track data consumption per user and manage resources effectively.                                                                                     |
| `repository`         | The name of the repository of the image that was pulled.                                                                                                                                                           | This lets you identify which repositories are most frequently accessed and consume most of the data transfer.                                                                       |
| `access_token_name`  | Name of the access token that was used for authentication with Docker CLI. `generated` tokens are automatically generated by the Docker client when a user signs in.                                               | Personal access tokens are usually used to authenticate automated tools (Docker Desktop, CI/CD tools, etc.). This is useful for identifying which automated system issued the pull. |
| `ips`                | The IP address that was used to pull the image. This field is aggregated, so more than one IP address may appear, representing all the IPs used to pull an image within the same date and hour.                    | This helps you understand the origin of the data transfer, which is useful for diagnosing and identifying patterns in automated or manual pulls.                                    |
| `repository_privacy` | The privacy state of the image repository that was pulled. This can either be `public` or `private`.                                                                                                               | This distinguishes between public and private repositories to identify which data transfer threshold the pull impacts.                                                              |
| `tag`                | The tag for the image. The tag is only available if the pull included a tag.                                                                                                                                       | This helps in identifying the image. Tags are often used to identify specific versions or variants of an image.                                                                     |
| `digest`             | The unique image digest for the image.                                                                                                                                                                             | This helps in identifying the image.                                                                                                                                                |
| `version_checks`     | The number of version checks accumulated for the date and hour of each image repository. Depending on the client, a pull can do a version check to verify the existence of an image or tag without downloading it. | This helps identify the frequency of version checks, which you can use to analyze usage trends and potential unexpected behaviors.                                                  |
| `pulls`              | The number of pulls accumulated for the date and hour of each image repository.                                                                                                                                    | This helps identify the frequency of repository pulls, which you can use to analyze usage trends and potential unexpected behaviors.                                                |

## [View pull rate and limit](#view-pull-rate-and-limit)

The pull rate limit is calculated on a 6-hour basis. There is no pull rate limit for users or automated systems with a paid subscription. Unauthenticated and Docker Personal users using Docker Hub will experience rate limits on image pulls.

When you issue a pull and you are over the limit, Docker Hub returns a `429` response code with the following body when the manifest is requested:

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

This error message appears in the Docker CLI or in the Docker Engine logs.

To view your current pull rate and limit:

> Note
>
> To check your limits, you need `curl` and `jq` installed.

1. Get a token.

   * To get a token anonymously, if you are pulling anonymously:

     ```console
     $ TOKEN=$(curl "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
     ```

   * To get a token with a user account, if you are authenticated, insert your username and password in the following command:

     ```console
     $ TOKEN=$(curl --user 'username:password' "https://auth.docker.io/token?service=registry.docker.io&scope=repository:ratelimitpreview/test:pull" | jq -r .token)
     ```

2. Get the headers that contain your limits. These headers are returned on both GET and HEAD requests. Using GET emulates a real pull and counts towards the limit. Using HEAD won't.

   ```console
   $ curl --head -H "Authorization: Bearer $TOKEN" https://registry-1.docker.io/v2/ratelimitpreview/test/manifests/latest
   ```

3. Examine the headers. You should see the following headers.

   ```text
   ratelimit-limit: 100;w=21600
   ratelimit-remaining: 20;w=21600
   docker-ratelimit-source: 192.0.2.1
   ```

   In the previous example, the pull limit is 100 pulls per 21600 seconds (6 hours), and there are 20 pulls remaining.

   If you don't see any `ratelimit` header, it could be because the image or your IP is unlimited in partnership with a publisher, provider, or an open source organization. It could also mean that the user you are pulling as is part of a paid Docker subscription. Pulling that image won't count toward pull rate limits if you don't see these headers.

----
url: https://docs.docker.com/guides/rust/run-containers/
----

# Run your Rust image as a container

***

Table of contents

***

## [Prerequisite](#prerequisite)

You have completed [Build your Rust image](https://docs.docker.com/guides/rust/build-images/) and you have built an image.

## [Overview](#overview)

A container is a normal operating system process except that Docker isolates this process so that it has its own file system, its own networking, and its own isolated process tree separate from the host.

To run an image inside of a container, you use the `docker run` command. The `docker run` command requires one parameter which is the name of the image.

## [Run an image](#run-an-image)

Use `docker run` to run the image you built in [Build your Rust image](https://docs.docker.com/guides/rust/build-images/).

```console
$ docker run docker-rust-image-dhi
```

After running this command, you’ll notice that you weren't returned to the command prompt. This is because your application is a server that runs in a loop waiting for incoming requests without returning control back to the OS until you stop the container.

Open a new terminal then make a request to the server using the `curl` command.

```console
$ curl http://localhost:8000
```

You should see output like the following.

```console
curl: (7) Failed to connect to localhost port 8000 after 2236 ms: Couldn't connect to server
```

As you can see, your `curl` command failed. This means you weren't able to connect to the localhost on port 8000. This is normal because your container is running in isolation which includes networking. Stop the container and restart with port 8000 published on your local network.

To stop the container, press ctrl-c. This will return you to the terminal prompt.

To publish a port for your container, you’ll use the `--publish` flag (`-p` for short) on the `docker run` command. The format of the `--publish` command is `[host port]:[container port]`. So, if you wanted to expose port 8000 inside the container to port 3001 outside the container, you would pass `3001:8000` to the `--publish` flag.

You didn't specify a port when running the application in the container and the default is 8000. If you want your previous request going to port 8000 to work, you can map the host's port 3001 to the container's port 8000:

```console
$ docker run --publish 3001:8000 docker-rust-image-dhi
```

Now, rerun the curl command. Remember to open a new terminal.

```console
$ curl http://localhost:3001
```

You should see output like the following.

```console
Hello, Docker!
```

Success! You were able to connect to the application running inside of your container on port 8000. Switch back to the terminal where your container is running and stop it.

Press ctrl-c to stop the container.

## [Run in detached mode](#run-in-detached-mode)

This is great so far, but your sample application is a web server and you don't have to be connected to the container. Docker can run your container in detached mode or in the background. To do this, you can use the `--detach` or `-d` for short. Docker starts your container the same as before but this time will "detach" from the container and return you to the terminal prompt.

```console
$ docker run -d -p 3001:8000 docker-rust-image-dhi
3e4830e7f01304811d97dd3469d47a0c7a916a8b6c28ce0ef19c6f689a521144
```

Docker started your container in the background and printed the Container ID on the terminal.

Again, make sure that your container is running properly. Run the curl command again.

```console
$ curl http://localhost:3001
```

You should see output like the following.

```console
Hello, Docker!
```

## [List containers](#list-containers)

Since you ran your container in the background, how do you know if your container is running or what other containers are running on your machine? Well, to see a list of containers running on your machine, run `docker ps`. This is similar to how you use the ps command in Linux to see a list of processes.

You should see output like the following.

```console
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                         NAMES
3e4830e7f013   docker-rust-image-dhi   "/server"                23 seconds ago   Up 22 seconds   0.0.0.0:3001->8000/tcp, [::]:3001->8000/tcp   youthful_lamport
```

The `docker ps` command provides a bunch of information about your running containers. You can see the container ID, the image running inside the container, the command that was used to start the container, when it was created, the status, ports that were exposed, and the name of the container.

You are probably wondering where the name of your container is coming from. Since you didn’t provide a name for the container when you started it, Docker generated a random name. You’ll fix this in a minute, but first you need to stop the container. To stop the container, run the `docker stop` command which does just that, stops the container. You need to pass the name of the container or you can use the container ID.

```console
$ docker stop youthful_lamport
youthful_lamport
```

Now, rerun the `docker ps` command to see a list of running containers.

```console
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

## [Stop, start, and name containers](#stop-start-and-name-containers)

You can start, stop, and restart Docker containers. When you stop a container, it's not removed, but the status is changed to stopped and the process inside the container is stopped. When you ran the `docker ps` command in the previous module, the default output only shows running containers. When you pass the `--all` or `-a` for short, you see all containers on your machine, irrespective of their start or stop status.

```console
$ docker ps -a
CONTAINER ID   IMAGE                   COMMAND                  CREATED              STATUS                          PORTS                                         NAMES
3e4830e7f013   docker-rust-image-dhi   "/server"                About a minute ago   Exited (0) 28 seconds ago                                                     youthful_lamport
60009b7eaf40   docker-rust-image-dhi   "/server"                2 minutes ago        Exited (0) About a minute ago                                                 sharp_noyce
152e1d7d9eea   docker-rust-image-dhi   "/server ."              4 minutes ago        Exited (0) 2 minutes ago                                                      magical_bhabha
```

You should now see several containers listed. These are containers that you started and stopped but you haven't removed.

Restart the container that you just stopped. Locate the name of the container you just stopped and replace the name of the container in following restart command.

```console
$ docker restart youthful_lamport
```

Now list all the containers again using the `docker ps --all` command.

```console
$ docker ps --all
CONTAINER ID   IMAGE                   COMMAND                  CREATED             STATUS                         PORTS                                         NAMES
3e4830e7f013   docker-rust-image-dhi   "/server"                3 minutes ago       Up 7 seconds                   0.0.0.0:3001->8000/tcp, [::]:3001->8000/tcp   youthful_lamport
60009b7eaf40   docker-rust-image-dhi   "/server"                4 minutes ago       Exited (0) 3 minutes ago                                                     sharp_noyce
152e1d7d9eea   docker-rust-image-dhi   "/server ."              5 minutes ago       Exited (0) 4 minutes ago                                                     magical_bhabha
```

Notice that the container you just restarted has been started in detached mode. Also, observe the status of the container is "Up X seconds". When you restart a container, it starts with the same flags or commands that it was originally started with.

Now, stop and remove all of your containers and take a look at fixing the random naming issue. Stop the container you just started. Find the name of your running container and replace the name in the following command with the name of the container on your system.

```console
$ docker stop youthful_lamport
youthful_lamport
```

Now that you have stopped all of your containers, remove them. When you remove a container, it's no longer running, nor is it in the stopped status, but the process inside the container has been stopped and the metadata for the container has been removed.

To remove a container, run the `docker rm` command with the container name. You can pass multiple container names to the command using a single command. Again, replace the container names in the following command with the container names from your system.

```console
$ docker rm youthful_lamport friendly_montalcini tender_bose
youthful_lamport
sharp_noyce
magical_bhabha
```

Run the `docker ps --all` command again to see that Docker removed all containers.

Now, it's time to address the random naming issue. Standard practice is to name your containers for the simple reason that it's easier to identify what's running in the container and what application or service it's associated with.

To name a container, pass the `--name` flag to the `docker run` command.

```console
$ docker run -d -p 3001:8000 --name docker-rust-container docker-rust-image-dhi
1aa5d46418a68705c81782a58456a4ccdb56a309cb5e6bd399478d01eaa5cdda
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED         STATUS         PORTS                                         NAMES
219b2e3c7c38   docker-rust-image-dhi   "/server"                6 seconds ago   Up 5 seconds   0.0.0.0:3001->8000/tcp, [::]:3001->8000/tcp   docker-rust-container
```

Now you can identify your container based on the name.

## [Summary](#summary)

In this section, you took a look at running containers. You also took a look at managing containers by starting, stopping, and restarting them. And finally, you looked at naming your containers so they are more identifiable.

Related information:

* [docker run CLI reference](/reference/cli/docker/container/run/)

## [Next steps](#next-steps)

In the next section, you’ll learn how to run a database in a container and connect it to a Rust application.

[Develop your Rust application »](https://docs.docker.com/guides/rust/develop/)

----
url: https://docs.docker.com/guides/php/develop/
----

# Use containers for PHP development

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Containerize a PHP application](https://docs.docker.com/guides/php/containerize/).

## [Overview](#overview)

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

* Adding a local database and persisting data
* Adding phpMyAdmin to interact with the database
* Configuring Compose to automatically update your running Compose services as you edit and save your code
* Creating a development container that contains the dev dependencies

## [Add a local database and persist data](#add-a-local-database-and-persist-data)

You can use containers to set up local services, like a database. To do this for the sample application, you'll need to do the following:

* Update the `Dockerfile` to install extensions to connect to the database
* Update the `compose.yaml` file to add a database service and volume to persist data

### [Update the Dockerfile to install extensions](#update-the-dockerfile-to-install-extensions)

To install PHP extensions, you need to update the `Dockerfile`. Open your Dockerfile in an IDE or text editor and then update the contents. The following `Dockerfile` includes one new line that installs the `pdo` and `pdo_mysql` extensions. All comments have been removed.

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

For more details about installing PHP extensions, see the [Official Docker Image for PHP](https://hub.docker.com/_/php).

### [Update the compose.yaml file to add a db and persist data](#update-the-composeyaml-file-to-add-a-db-and-persist-data)

Open the `compose.yaml` file in an IDE or text editor. You'll notice it already contains commented-out instructions for a PostgreSQL database and volume. For this application, you'll use MariaDB. For more details about MariaDB, see the [MariaDB Official Docker image](https://hub.docker.com/_/mariadb).

Open the `src/database.php` file in an IDE or text editor. You'll notice that it reads environment variables in order to connect to the database.

In the `compose.yaml` file, you'll need to update the following:

1. Uncomment and update the database instructions for MariaDB.
2. Add a secret to the server service to pass in the database password.
3. Add the database connection environment variables to the server service.
4. Uncomment the volume instructions to persist data.

The following is the updated `compose.yaml` file. All comments have been removed.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> Note
>
> To learn more about the instructions in the Compose file, see [Compose file reference](/reference/compose-file/).

Before you run the application using Compose, notice that this Compose file uses `secrets` and specifies a `password.txt` file to hold the database's password. You must create this file as it's not included in the source repository.

In the `docker-php-sample` directory, create a new directory named `db` and inside that directory create a file named `password.txt`. Open `password.txt` in an IDE or text editor and add the following password. The password must be on a single line, with no additional lines in the file.

```text
example
```

Save and close the `password.txt` file.

You should now have the following in your `docker-php-sample` directory.

```text
├── docker-php-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── composer.json
│ ├── composer.lock
│ ├── Dockerfile
│ └── README.md
```

Run the following command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:9000/database.php>. You should see a simple web application with text and a counter that increments every time you refresh.

Press `ctrl+c` in the terminal to stop your application.

## [Verify that data persists in the database](#verify-that-data-persists-in-the-database)

In the terminal, run `docker compose rm` to remove your containers and then run `docker compose up` to run your application again.

```console
$ docker compose rm
$ docker compose up --build
```

Refresh <http://localhost:9000/database.php> in your browser and verify that the previous count still exists. Without a volume, the database data wouldn't persist after you remove the container.

Press `ctrl+c` in the terminal to stop your application.

## [Add phpMyAdmin to interact with the database](#add-phpmyadmin-to-interact-with-the-database)

You can easily add services to your application stack by updating the `compose.yaml` file.

Update your `compose.yaml` to add a new service for phpMyAdmin. For more details, see the [phpMyAdmin Official Docker Image](https://hub.docker.com/_/phpmyadmin). The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

In the terminal, run `docker compose up` to run your application again.

```console
$ docker compose up --build
```

Open <http://localhost:8080> in your browser to access phpMyAdmin. Log in using `root` as the username and `example` as the password. You can now interact with the database through phpMyAdmin.

Press `ctrl+c` in the terminal to stop your application.

## [Automatically update services](#automatically-update-services)

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yaml` file in an IDE or text editor and then add the Compose Watch instructions. The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 9000:80
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    environment:
      - PASSWORD_FILE_PATH=/run/secrets/db-password
      - DB_HOST=db
      - DB_NAME=example
      - DB_USER=root
    develop:
      watch:
        - action: sync
          path: ./src
          target: /var/www/html
  db:
    image: mariadb
    restart: always
    user: root
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD_FILE=/run/secrets/db-password
      - MARIADB_DATABASE=example
    expose:
      - 3306
    healthcheck:
      test:
        [
          "CMD",
          "/usr/local/bin/healthcheck.sh",
          "--su-mysql",
          "--connect",
          "--innodb_initialized",
        ]
      interval: 10s
      timeout: 5s
      retries: 5
  phpmyadmin:
    image: phpmyadmin
    ports:
      - 8080:80
    depends_on:
      - db
    environment:
      - PMA_HOST=db
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Open a browser and verify that the application is running at <http://localhost:9000/hello.php>.

Any changes to the application's source files on your local machine will now be immediately reflected in the running container.

Open `hello.php` in an IDE or text editor and update the string `Hello, world!` to `Hello, Docker!`.

Save the changes to `hello.php` and then wait a few seconds for the application to sync. Refresh <http://localhost:9000/hello.php> in your browser and verify that the updated text appears.

Press `ctrl+c` in the terminal to stop Compose Watch. Run `docker compose down` in the terminal to stop the application.

## [Create a development container](#create-a-development-container)

At this point, when you run your containerized application, Composer isn't installing the dev dependencies. While this small image is good for production, it lacks the tools and dependencies you may need when developing and it doesn't include the `tests` directory. You can use multi-stage builds to build stages for both development and production in the same Dockerfile. For more details, see [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

In the `Dockerfile`, you'll need to update the following:

1. Split the `deps` staged into two stages. One stage for production (`prod-deps`) and one stage (`dev-deps`) to install development dependencies.
2. Create a common `base` stage.
3. Create a new `development` stage for development.
4. Update the `final` stage to copy dependencies from the new `prod-deps` stage.

The following is the `Dockerfile` before and after the changes.

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as deps
WORKDIR /app
RUN --mount=type=bind,source=composer.json,target=composer.json \
    --mount=type=bind,source=composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM php:8.2-apache as final
RUN docker-php-ext-install pdo pdo_mysql
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=deps app/vendor/ /var/www/html/vendor
COPY ./src /var/www/html
USER www-data
```

```dockerfile
# syntax=docker/dockerfile:1

FROM composer:lts as prod-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-dev --no-interaction

FROM composer:lts as dev-deps
WORKDIR /app
RUN --mount=type=bind,source=./composer.json,target=composer.json \
    --mount=type=bind,source=./composer.lock,target=composer.lock \
    --mount=type=cache,target=/tmp/cache \
    composer install --no-interaction

FROM php:8.2-apache as base
RUN docker-php-ext-install pdo pdo_mysql
COPY ./src /var/www/html

FROM base as development
COPY ./tests /var/www/html/tests
RUN mv "$PHP_INI_DIR/php.ini-development" "$PHP_INI_DIR/php.ini"
COPY --from=dev-deps app/vendor/ /var/www/html/vendor

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

Update your `compose.yaml` file by adding an instruction to target the development stage.

The following is the updated section of the `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: development
      # ...
```

Your containerized application will now install the dev dependencies.

Run the following command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:9000/hello.php>. You should still see the simple "Hello, Docker!" application.

Press `ctrl+c` in the terminal to stop your application.

While the application appears the same, you can now make use of the dev dependencies. Continue to the next section to learn how you can run tests using Docker.

## [Summary](#summary)

In this section, you took a look at setting up your Compose file to add a local database and persist data. You also learned how to use Compose Watch to automatically sync your application when you update your code. And finally, you learned how to create a development container that contains the dependencies needed for development.

Related information:

* [Compose file reference](/reference/compose-file/)
* [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
* [Dockerfile reference](https://docs.docker.com/reference/dockerfile/)
* [Official Docker Image for PHP](https://hub.docker.com/_/php)

## [Next steps](#next-steps)

In the next section, you'll learn how to run unit tests using Docker.

[Run PHP tests in a container »](https://docs.docker.com/guides/php/run-tests/)

----
url: https://docs.docker.com/reference/cli/docker/buildx/version/
----

# docker buildx version

***

| Description | Show buildx version information |
| ----------- | ------------------------------- |
| Usage       | `docker buildx version`         |

## [Description](#description)

View version information

```console
$ docker buildx version
github.com/docker/buildx v0.11.2 9872040b6626fb7d87ef7296fd5b832e8cc2ad17
```

----
url: https://docs.docker.com/reference/cli/docker/compose/bridge/
----

# docker compose bridge

***

| Description | Convert compose files into another model |
| ----------- | ---------------------------------------- |

## [Description](#description)

Convert compose files into another model

## [Subcommands](#subcommands)

| Command                                                                                                                 | Description                                                                  |
| ----------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| [`docker compose bridge convert`](https://docs.docker.com/reference/cli/docker/compose/bridge/convert/)                 | Convert compose files to Kubernetes manifests, Helm charts, or another model |
| [`docker compose bridge transformations`](https://docs.docker.com/reference/cli/docker/compose/bridge/transformations/) | Manage transformation images                                                 |

----
url: https://docs.docker.com/guides/nodejs/
----

# Node.js language-specific guide

Table of contents

***

This guide explains how to containerize Node.js applications using Docker.

**Time to complete** 20 minutes

[Node.js](https://nodejs.org/en) is a JavaScript runtime for building server-side applications. This guide shows you how to containerize a TypeScript Node.js application using Docker, starting from a simple Express API and progressively adding features like a database and CI/CD.

This guide focuses on a backend Node.js API. If you're building a standalone frontend application, Docker has dedicated guides for [React.js](/guides/reactjs/), [Vue.js](/guides/vuejs/), [Angular](/guides/angular/), and [Next.js](/guides/nextjs/).

> **Acknowledgment**
>
> Docker thanks [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for his contribution to this guide.

## [What will you learn?](#what-will-you-learn)

In this guide, you'll learn how to:

* Containerize and run a Node.js application using Docker.
* Set up a local development environment using containers.
* Run tests inside a Docker container.
* Configure GitHub Actions for CI/CD with Docker.
* Inspect and generate supply chain attestations for your image.
* Deploy your containerized Node.js application to Kubernetes.

Start by containerizing a Node.js application.

## [Prerequisites](#prerequisites)

* Basic understanding of [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) and [TypeScript](https://www.typescriptlang.org/).
* Basic knowledge of [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm).
* Familiarity with Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/nodejs/containerize/)

   Learn how to containerize a Node.js application with Docker.

2. [Develop your app](https://docs.docker.com/guides/nodejs/develop/)

   Learn how to develop your Node.js application locally using containers.

3. [Run your tests](https://docs.docker.com/guides/nodejs/run-tests/)

   Learn how to run your Node.js tests in a container.

4. [GitHub Actions CI](https://docs.docker.com/guides/nodejs/configure-github-actions/)

   Learn how to configure CI/CD using GitHub Actions for your Node.js application.

5. [Secure your supply chain](https://docs.docker.com/guides/nodejs/secure-supply-chain/)

   Learn how to inspect, generate, and verify supply chain attestations for your Node.js container image.

6. [Deploy your app](https://docs.docker.com/guides/nodejs/deploy/)

   Learn how to deploy your containerized Node.js application to Kubernetes.

----
url: https://docs.docker.com/enterprise/enterprise-deployment/use-jamf-pro/
----

# Deploy with Jamf Pro

***

Table of contents

***

For: Administrators

Learn how to deploy Docker Desktop for Mac using Jamf Pro, including uploading the installer and creating a deployment policy.

First, upload the package:

1. From the Jamf Pro console, navigate to **Computers** > **Management Settings** > **Computer Management** > **Packages**.
2. Select **New** to add a new package.
3. Upload the `Docker.pkg` file.

Next, create a policy for deployment:

1. Navigate to **Computers** > **Policies**.
2. Select **New** to create a new policy.
3. Enter a name for the policy, for example "Deploy Docker Desktop".
4. Under the **Packages** tab, add the Docker package you uploaded.
5. Configure the scope to target the devices or device groups on which you want to install Docker.
6. Save the policy and deploy.

For more information, see [Jamf Pro's official documentation](https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html).

## [Additional resources](#additional-resources)

* Learn how to [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/) for your users.

----
url: https://docs.docker.com/reference/cli/docker/pass/plugins/1password/purge/
----

# docker pass plugins 1password purge

***

| Description | Disable the plugin and remove the stored 1Password service account token. |
| ----------- | ------------------------------------------------------------------------- |
| Usage       | `docker pass plugins 1password purge`                                     |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Disable the `1password-sdk` plugin on the running secrets-engine daemon and remove the service account token from the local OS keychain.

After purge, the plugin no longer participates in secret resolution and the token is gone from local storage. Run `setup` again to re-enable it.

----
url: https://docs.docker.com/guides/nodejs/develop/
----

# Use containers for Node.js development

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Containerize a Node.js application](https://docs.docker.com/guides/nodejs/containerize/).

## [Overview](#overview)

Once your application runs in a container, the next step is making the container part of your everyday development workflow. Code changes should show up quickly, and services your app depends on, like databases, should run right alongside it.

In this section, you'll adapt the Dockerfile for local development by renaming the `builder` stage to `dev` and pointing Compose at it. You'll also update the application to connect to a PostgreSQL database, add a database service to `compose.yaml`, persist data in a named volume, enable Compose Watch so changes in your editor are picked up without a manual rebuild, and set up Node.js debugging so you can attach VS Code or Chrome DevTools to the running container.

## [Update the application](#update-the-application)

You'll update your application to connect to a PostgreSQL database. Continue working in your `nodejs-docker-example` directory.

Replace `src/index.ts` and `package.json` with the following contents. The file browser shows only the files that change in this step.

> Note
>
> The application won't run yet after this step. It tries to connect to a PostgreSQL database that doesn't exist. The next two sections add the database service and the Docker configuration needed to run everything together.

nodejs-docker-example

```typescript
// Express application backed by a PostgreSQL database.
// Creates a heroes table at startup.
// Endpoints: GET / (greeting), GET /health (health check), POST /heroes/ (create), GET /heroes/ (list).
// See https://expressjs.com/ and https://node-postgres.com/

import express, { type Request, type Response } from 'express';
import { Pool } from 'pg';
import { readFileSync } from 'fs';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.use(express.json());

function getPassword(): string {
  const passwordFile = process.env.POSTGRES_PASSWORD_FILE;
  if (passwordFile) {
    return readFileSync(passwordFile, 'utf8').trim();
  }
  return process.env.POSTGRES_PASSWORD ?? '';
}

const pool = new Pool({
  host: process.env.POSTGRES_SERVER,
  port: 5432,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: getPassword(),
});

pool
  .query(
    `CREATE TABLE IF NOT EXISTS heroes (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      secret_name TEXT NOT NULL,
      age INTEGER
    )`,
  )
  .catch(console.error);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' });
});

app.post('/heroes/', async (req: Request, res: Response) => {
  const { name, secret_name, age } = req.body as {
    name: string;
    secret_name: string;
    age?: number;
  };
  const result = await pool.query(
    'INSERT INTO heroes (name, secret_name, age) VALUES ($1, $2, $3) RETURNING *',
    [name, secret_name, age],
  );
  res.json(result.rows[0]);
});

app.get('/heroes/', async (_req: Request, res: Response) => {
  const result = await pool.query('SELECT * FROM heroes');
  res.json(result.rows);
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir -p nodejs-docker-example/src && cd nodejs-docker-example
cat > src/index.ts <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
// Express application backed by a PostgreSQL database.
// Creates a heroes table at startup.
// Endpoints: GET / (greeting), GET /health (health check), POST /heroes/ (create), GET /heroes/ (list).
// See https://expressjs.com/ and https://node-postgres.com/

import express, { type Request, type Response } from 'express';
import { Pool } from 'pg';
import { readFileSync } from 'fs';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.use(express.json());

function getPassword(): string {
  const passwordFile = process.env.POSTGRES_PASSWORD_FILE;
  if (passwordFile) {
    return readFileSync(passwordFile, 'utf8').trim();
  }
  return process.env.POSTGRES_PASSWORD ?? '';
}

const pool = new Pool({
  host: process.env.POSTGRES_SERVER,
  port: 5432,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: getPassword(),
});

pool
  .query(
    `CREATE TABLE IF NOT EXISTS heroes (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      secret_name TEXT NOT NULL,
      age INTEGER
    )`,
  )
  .catch(console.error);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' });
});

app.post('/heroes/', async (req: Request, res: Response) => {
  const { name, secret_name, age } = req.body as {
    name: string;
    secret_name: string;
    age?: number;
  };
  const result = await pool.query(
    'INSERT INTO heroes (name, secret_name, age) VALUES ($1, $2, $3) RETURNING *',
    [name, secret_name, age],
  );
  res.json(result.rows[0]);
});

app.get('/heroes/', async (_req: Request, res: Response) => {
  const result = await pool.query('SELECT * FROM heroes');
  res.json(result.rows);
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > package.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
New-Item -ItemType Directory -Force -Path nodejs-docker-example/src | Out-Null
Set-Location nodejs-docker-example
WriteFile 'src/index.ts' @'
// Express application backed by a PostgreSQL database.
// Creates a heroes table at startup.
// Endpoints: GET / (greeting), GET /health (health check), POST /heroes/ (create), GET /heroes/ (list).
// See https://expressjs.com/ and https://node-postgres.com/

import express, { type Request, type Response } from 'express';
import { Pool } from 'pg';
import { readFileSync } from 'fs';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.use(express.json());

function getPassword(): string {
  const passwordFile = process.env.POSTGRES_PASSWORD_FILE;
  if (passwordFile) {
    return readFileSync(passwordFile, 'utf8').trim();
  }
  return process.env.POSTGRES_PASSWORD ?? '';
}

const pool = new Pool({
  host: process.env.POSTGRES_SERVER,
  port: 5432,
  database: process.env.POSTGRES_DB,
  user: process.env.POSTGRES_USER,
  password: getPassword(),
});

pool
  .query(
    `CREATE TABLE IF NOT EXISTS heroes (
      id SERIAL PRIMARY KEY,
      name TEXT NOT NULL,
      secret_name TEXT NOT NULL,
      age INTEGER
    )`,
  )
  .catch(console.error);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.get('/health', (_req: Request, res: Response) => {
  res.json({ status: 'ok' });
});

app.post('/heroes/', async (req: Request, res: Response) => {
  const { name, secret_name, age } = req.body as {
    name: string;
    secret_name: string;
    age?: number;
  };
  const result = await pool.query(
    'INSERT INTO heroes (name, secret_name, age) VALUES ($1, $2, $3) RETURNING *',
    [name, secret_name, age],
  );
  res.json(result.rows[0]);
});

app.get('/heroes/', async (_req: Request, res: Response) => {
  const result = await pool.query('SELECT * FROM heroes');
  res.json(result.rows);
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
'@
WriteFile 'package.json' @'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
'@
```

## [Update Docker assets](#update-docker-assets)

Replace `Dockerfile` and `compose.yaml` with the following.

nodejs-docker-example

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Development stage: install all dependencies, compile TypeScript, and
# serve with hot-reload. Used directly in development via compose.yaml.
FROM dhi.io/node:24-alpine3.23-dev AS dev

WORKDIR /app

# Install dependencies as a separate step to take advantage of Docker's
# caching. Leverage a cache mount to /root/.npm to speed up subsequent
# builds. Leverage a bind mount to package.json to avoid having to copy
# it into this layer.
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# Copy the source code into the container and compile TypeScript.
COPY . .
RUN npm run build

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application in development mode.
CMD ["npm", "run", "dev"]


# Deps stage: install production dependencies only.
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# Runner stage: minimal runtime image with compiled app and production deps.
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=dev --chown=node:node /app/dist ./dist

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["node", "dist/index.js"]
```

```yaml
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir nodejs-docker-example && cd nodejs-docker-example
cat > Dockerfile <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Development stage: install all dependencies, compile TypeScript, and
# serve with hot-reload. Used directly in development via compose.yaml.
FROM dhi.io/node:24-alpine3.23-dev AS dev

WORKDIR /app

# Install dependencies as a separate step to take advantage of Docker's
# caching. Leverage a cache mount to /root/.npm to speed up subsequent
# builds. Leverage a bind mount to package.json to avoid having to copy
# it into this layer.
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# Copy the source code into the container and compile TypeScript.
COPY . .
RUN npm run build

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application in development mode.
CMD ["npm", "run", "dev"]


# Deps stage: install production dependencies only.
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# Runner stage: minimal runtime image with compiled app and production deps.
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=dev --chown=node:node /app/dist ./dist

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["node", "dist/index.js"]
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > compose.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
Set-Location nodejs-docker-example
WriteFile 'Dockerfile' @'
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Development stage: install all dependencies, compile TypeScript, and
# serve with hot-reload. Used directly in development via compose.yaml.
FROM dhi.io/node:24-alpine3.23-dev AS dev

WORKDIR /app

# Install dependencies as a separate step to take advantage of Docker's
# caching. Leverage a cache mount to /root/.npm to speed up subsequent
# builds. Leverage a bind mount to package.json to avoid having to copy
# it into this layer.
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# Copy the source code into the container and compile TypeScript.
COPY . .
RUN npm run build

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application in development mode.
CMD ["npm", "run", "dev"]


# Deps stage: install production dependencies only.
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# Runner stage: minimal runtime image with compiled app and production deps.
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=dev --chown=node:node /app/dist ./dist

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["node", "dist/index.js"]
'@
WriteFile 'compose.yaml' @'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
'@
```

### [About these changes](#about-these-changes)

The `builder` stage from containerize is renamed to `dev` and gains `EXPOSE 3000` and `CMD ["npm", "run", "dev"]`, which runs `tsx watch` for hot-reload. The `deps` and `runner` stages are unchanged.

In `compose.yaml`, the new `target: dev` line tells Compose to build and run the `dev` stage during development. Unlike the production image, the development image includes `tsx` and other dev tooling. If you need a shell in a running production container, use [Docker Debug](/reference/cli/docker/debug/) instead.

The build step runs `tsc`, which compiles each TypeScript file into a corresponding JavaScript file. [esbuild](https://esbuild.github.io/) is a popular alternative that bundles everything into a single output file and builds significantly faster. To switch, replace the `tsc` call in `package.json` with an esbuild command and update the `COPY --from=dev` path in the `runner` stage to match esbuild's output.

## [Add a local database and persist data](#add-a-local-database-and-persist-data)

You can use containers to set up local services, like a database. In this section, you'll update the `compose.yaml` file to define a database service and a volume to persist data, and add a `db/password.txt` file that holds the database password.

nodejs-docker-example

```yaml
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  # Database service. Reads the password from a Docker secret mounted at
  # /run/secrets/db-password. Compose waits for the healthcheck to pass
  # before starting the server, via the server's depends_on.
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

```text
mysecretpassword
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir -p nodejs-docker-example/db && cd nodejs-docker-example
cat > compose.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  # Database service. Reads the password from a Docker secret mounted at
  # /run/secrets/db-password. Compose waits for the healthcheck to pass
  # before starting the server, via the server's depends_on.
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > db/password.txt <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
mysecretpassword
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
New-Item -ItemType Directory -Force -Path nodejs-docker-example/db | Out-Null
Set-Location nodejs-docker-example
WriteFile 'compose.yaml' @'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
  # Database service. Reads the password from a Docker secret mounted at
  # /run/secrets/db-password. Compose waits for the healthcheck to pass
  # before starting the server, via the server's depends_on.
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
'@
WriteFile 'db/password.txt' @'
mysecretpassword
'@
```

> Note
>
> To learn more about the instructions in the Compose file, see [Compose file reference](/reference/compose-file/).

Now, run the following `docker compose up` command to start your application.

```console
$ docker compose up --build
```

Now test your API endpoint. Open a new terminal and make a request to the server using the curl commands.

Create an object with a POST request:

```console
$ curl -X 'POST' \
  'http://localhost:3000/heroes/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}'
```

You should receive the following response:

```json
{
  "id": 1,
  "name": "my hero",
  "secret_name": "austing",
  "age": 12
}
```

Now make a GET request:

```console
$ curl http://localhost:3000/heroes/
```

You should receive the same response because it's the only object in the database.

Press `ctrl`+`c` in the terminal to stop your application.

## [Automatically update services](#automatically-update-services)

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yaml` file in an IDE or text editor and add the highlighted Compose Watch instructions.

nodejs-docker-example

```yaml
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir nodejs-docker-example && cd nodejs-docker-example
cat > compose.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
Set-Location nodejs-docker-example
WriteFile 'compose.yaml' @'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
'@
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

In a terminal, curl the application to get a response.

```console
$ curl http://localhost:3000
{"message":"Hello World"}
```

Any changes to the application's source files on your local machine will now be immediately reflected in the running container.

Open `nodejs-docker-example/src/index.ts` in an IDE or text editor and update the `Hello World` string by adding a few more exclamation marks.

```diff
-  res.json({ message: 'Hello World' });
+  res.json({ message: 'Hello World!!!' });
```

Save the changes to `src/index.ts` and then wait a few seconds for the application to reload. Curl the application again and verify that the updated text appears.

```console
$ curl http://localhost:3000
{"message":"Hello World!!!"}
```

Press `ctrl`+`c` in the terminal to stop your application.

## [Debug your application](#debug-your-application)

`tsx watch` supports the Node.js inspector protocol, so you can attach a debugger from VS Code or Chrome DevTools and set breakpoints directly in your TypeScript source files.

Update the `dev` script in `package.json` to start the inspector. The `--inspect=0.0.0.0:9229` flag tells Node.js to listen for debugger connections on all network interfaces at port 9229. Using `0.0.0.0` rather than `localhost` is necessary so the debugger is reachable from outside the container. Also expose the debug port in `compose.yaml`, and add a `.vscode/launch.json` file that tells VS Code how to attach to the running inspector.

nodejs-docker-example

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch --inspect=0.0.0.0:9229 src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Docker Container",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "address": "localhost",
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app",
      "protocol": "inspector",
      "restart": true,
      "sourceMaps": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
```

```yaml
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
      - 9229:9229
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir -p nodejs-docker-example/.vscode && cd nodejs-docker-example
cat > package.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch --inspect=0.0.0.0:9229 src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > .vscode/launch.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Docker Container",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "address": "localhost",
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app",
      "protocol": "inspector",
      "restart": true,
      "sourceMaps": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > compose.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
      - 9229:9229
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
New-Item -ItemType Directory -Force -Path nodejs-docker-example/.vscode | Out-Null
Set-Location nodejs-docker-example
WriteFile 'package.json' @'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch --inspect=0.0.0.0:9229 src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2",
    "pg": "^8.16.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "@types/pg": "^8.11.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
'@
WriteFile '.vscode/launch.json' @'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Docker Container",
      "type": "node",
      "request": "attach",
      "port": 9229,
      "address": "localhost",
      "localRoot": "${workspaceFolder}",
      "remoteRoot": "/app",
      "protocol": "inspector",
      "restart": true,
      "sourceMaps": true,
      "skipFiles": ["<node_internals>/**"]
    }
  ]
}
'@
WriteFile 'compose.yaml' @'
services:
  # Application service. The `target: dev` line builds the development
  # image (includes tsx and dev tooling); the runner stage of the
  # Dockerfile is unused in development.
  server:
    build:
      context: .
      target: dev
    ports:
      - 3000:3000
      - 9229:9229
    environment:
      - POSTGRES_SERVER=db
      - POSTGRES_USER=postgres
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    depends_on:
      db:
        condition: service_healthy
    secrets:
      - db-password
    develop:
      watch:
        - action: sync
          path: ./src
          target: /app/src
        - action: rebuild
          path: package.json
  db:
    image: dhi.io/postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
'@
```

Rebuild and restart with the updated configuration:

```console
$ docker compose up --build
```

When the inspector is ready, you'll see a line like the following in the logs:

```text
Debugger listening on ws://0.0.0.0:9229/...
```

### [VS Code](#vs-code)

With `.vscode/launch.json` in place, attach the debugger using the Debug panel.

Open the Debug panel (`Ctrl+Shift+D` on Windows and Linux, `Cmd+Shift+D` on Mac), select **Attach to Docker Container**, and press `F5`. You can now set breakpoints in your TypeScript source files under `src/`.

### [Chrome DevTools](#chrome-devtools)

You can also use the built-in Node.js inspector in Chrome without any editor setup.

1. Open Chrome and go to `chrome://inspect`.

2. Select **Configure** and add `localhost:9229`.

3. When your Node.js target appears in the list, select **inspect**.

### [Troubleshoot the debugger](#troubleshoot-the-debugger)

If the debugger doesn't connect, verify the container is running and the port is mapped correctly:

```console
$ docker compose ps
$ docker compose logs server
```

The logs should include a line like:

```text
Debugger listening on ws://0.0.0.0:9229/...
```

If that line is missing, confirm the `dev` script in `package.json` includes `--inspect=0.0.0.0:9229` and that `9229:9229` appears in the `ports` list for the `server` service in `compose.yaml`.

For more details about Node.js debugging, see the [Node.js debugging guide](https://nodejs.org/en/docs/guides/debugging-getting-started).

## [Summary](#summary)

In this section, you set up a Compose file with a local database and persistent storage, set up Compose Watch to automatically sync code changes, and configured a debugger that attaches from VS Code and Chrome DevTools.

Related information:

* [Compose file reference](/reference/compose-file/)
* [Compose secrets](https://docs.docker.com/reference/compose-file/secrets/)
* [Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/)
* [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
* [Node.js debugging guide](https://nodejs.org/en/docs/guides/debugging-getting-started)

## [Next steps](#next-steps)

In the next section, you'll learn how to run tests using Docker.

[Run Node.js tests in a container »](https://docs.docker.com/guides/nodejs/run-tests/)

----
url: https://docs.docker.com/reference/cli/sbx/policy/reset/
----

# sbx policy reset

| Description | Reset policies to defaults |
| ----------- | -------------------------- |
| Usage       | `sbx policy reset [flags]` |

## [Description](#description)

Remove all custom policies and restart the daemon to restore defaults.

This deletes the local policy store and stops the daemon. When the daemon restarts (automatically on next command), the default policy is installed.

If sandboxes are currently running, they will be stopped when the daemon shuts down. You will be prompted for confirmation unless --force is used.

## [Options](#options)

| Option        | Default | Description              |
| ------------- | ------- | ------------------------ |
| `-f, --force` |         | Skip confirmation prompt |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Reset policies (prompts if sandboxes are running)
sbx policy reset

# Reset policies without confirmation
sbx policy reset --force
```

----
url: https://docs.docker.com/reference/samples/express/
----

# Express samples

| Name                                                                                                     | Description                                                             |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [React / Express / MySQL](https://github.com/docker/awesome-compose/tree/master/react-express-mysql)     | A sample React application with a Node.js backend and a MySQL database. |
| [React / Express / MongoDB](https://github.com/docker/awesome-compose/tree/master/react-express-mongodb) | A sample React application with a Node.js backend and a Mongo database. |
| [slack-clone-docker](https://github.com/dockersamples/slack-clone-docker)                                | A sample Slack Clone app built with the MERN stack.                     |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/engine/daemon/alternative-runtimes/
----

# Alternative container runtimes

***

Table of contents

***

Docker Engine uses containerd for managing the container lifecycle, which includes creating, starting, and stopping containers. By default, containerd uses runc as its container runtime.

## [What runtimes can I use?](#what-runtimes-can-i-use)

You can use any runtime that implements the containerd [shim API](https://github.com/containerd/containerd/blob/main/core/runtime/v2/README.md). Such runtimes ship with a containerd shim, and you can use them without any additional configuration. See [Use containerd shims](#use-containerd-shims).

Examples of runtimes that implement their own containerd shims include:

* [Wasmtime](https://wasmtime.dev/)
* [gVisor](https://github.com/google/gvisor)
* [Kata Containers](https://katacontainers.io/)

You can also use runtimes designed as drop-in replacements for runc. Such runtimes depend on the runc containerd shim for invoking the runtime binary. You must manually register such runtimes in the daemon configuration.

[youki](https://github.com/youki-dev/youki) is one example of a runtime that can function as a runc drop-in replacement. Refer to the [youki example](#youki) explaining the setup.

## [Use containerd shims](#use-containerd-shims)

containerd shims let you use alternative runtimes without having to change the configuration of the Docker daemon. To use a containerd shim, install the shim binary on `PATH` on the system where the Docker daemon is running.

To use a shim with `docker run`, specify the fully qualified name of the runtime as the value to the `--runtime` flag:

```console
$ docker run --runtime io.containerd.kata.v2 hello-world
```

### [Use a containerd shim without installing on PATH](#use-a-containerd-shim-without-installing-on-path)

You can use a shim without installing it on `PATH`, in which case you need to register the shim in the daemon configuration as follows:

```json
{
  "runtimes": {
    "foo": {
      "runtimeType": "/path/to/containerd-shim-foobar-v1"
    }
  }
}
```

To use the shim, specify the name that you assigned to it:

```console
$ docker run --runtime foo hello-world
```

### [Configure shims](#configure-shims)

If you need to pass additional configuration for a containerd shim, you can use the `runtimes` option in the daemon configuration file.

1. Edit the daemon configuration file by adding a `runtimes` entry for the shim you want to configure.

   * Specify the fully qualified name for the runtime in `runtimeType` key
   * Add your runtime configuration under the `options` key

   ```json
   {
     "runtimes": {
       "gvisor": {
         "runtimeType": "io.containerd.runsc.v1",
         "options": {
           "TypeUrl": "io.containerd.runsc.v1.options",
           "ConfigPath": "/etc/containerd/runsc.toml"
         }
       }
     }
   }
   ```

2. Reload the daemon's configuration.

   ```console
   # systemctl reload docker
   ```

3. Use the customized runtime using the `--runtime` flag for `docker run`.

   ```console
   $ docker run --runtime gvisor hello-world
   ```

For more information about the configuration options for containerd shims, see [Configure containerd shims](https://docs.docker.com/reference/cli/dockerd/#configure-containerd-shims).

## [Examples](#examples)

The following examples show you how to set up and use alternative container runtimes with Docker Engine.

* [youki](#youki)
* [Wasmtime](#wasmtime)

### [youki](#youki)

youki is a container runtime written in Rust. youki claims to be faster and use less memory than runc, making it a good choice for resource-constrained environments.

youki functions as a drop-in replacement for runc, meaning it relies on the runc shim to invoke the runtime binary. When you register runtimes acting as runc replacements, you configure the path to the runtime executable, and optionally a set of runtime arguments. For more information, see [Configure runc drop-in replacements](https://docs.docker.com/reference/cli/dockerd/#configure-runc-drop-in-replacements).

To add youki as a container runtime:

1. Install youki and its dependencies.

   For instructions, refer to the [official setup guide](https://youki-dev.github.io/youki/user/basic_setup.html).

2. Register youki as a runtime for Docker by editing the Docker daemon configuration file, located at `/etc/docker/daemon.json` by default.

   The `path` key should specify the path to wherever you installed youki.

   ```console
   # cat > /etc/docker/daemon.json <<EOF
   {
     "runtimes": {
       "youki": {
         "path": "/usr/local/bin/youki"
       }
     }
   }
   EOF
   ```

3. Reload the daemon's configuration.

   ```console
   # systemctl reload docker
   ```

Now you can run containers that use youki as a runtime.

```console
$ docker run --rm --runtime youki hello-world
```

### [Wasmtime](#wasmtime)

Availability: Experimental

Wasmtime is a [Bytecode Alliance](https://bytecodealliance.org/) project, and a Wasm runtime that lets you run Wasm containers. Running Wasm containers with Docker provides two layers of security. You get all the benefits from container isolation, plus the added sandboxing provided by the Wasm runtime environment.

To add Wasmtime as a container runtime, follow these steps:

1. Turn on the [containerd image store](https://docs.docker.com/engine/storage/containerd/) feature in the daemon configuration file.

   ```json
   {
     "features": {
       "containerd-snapshotter": true
     }
   }
   ```

2. Restart the Docker daemon.

   ```console
   # systemctl restart docker
   ```

3. Install the Wasmtime containerd shim on `PATH`.

   The following command Dockerfile builds the Wasmtime binary from source and exports it to `./containerd-shim-wasmtime-v1`.

   ```console
   $ docker build --output . - <<EOF
   FROM rust:latest as build
   RUN cargo install \
       --git https://github.com/containerd/runwasi.git \
       --bin containerd-shim-wasmtime-v1 \
       --root /out \
       containerd-shim-wasmtime
   FROM scratch
   COPY --from=build /out/bin /
   EOF
   ```

   Put the binary in a directory on `PATH`.

   ```console
   $ mv ./containerd-shim-wasmtime-v1 /usr/local/bin
   ```

Now you can run containers that use Wasmtime as a runtime.

```console
$ docker run --rm \
 --runtime io.containerd.wasmtime.v1 \
 --platform wasi/wasm32 \
 michaelirwin244/wasm-example
```

## [Related information](#related-information)

* To learn more about the configuration options for container runtimes, see [Configure container runtimes](https://docs.docker.com/reference/cli/dockerd/#configure-container-runtimes).
* You can configure which runtime that the daemon should use as its default. Refer to [Configure the default container runtime](https://docs.docker.com/reference/cli/dockerd/#configure-the-default-container-runtime).

----
url: https://docs.docker.com/build/ci/github-actions/named-contexts/
----

# Named contexts with GitHub Actions

***

Table of contents

***

You can define [additional build contexts](/reference/cli/docker/buildx/build/#build-context), and access them in your Dockerfile with `FROM name` or `--from=name`. When Dockerfile defines a stage with the same name it's overwritten.

This can be useful with GitHub Actions to reuse results from other builds or pin an image to a specific tag in your workflow.

## [Pin image to a tag](#pin-image-to-a-tag)

Replace `alpine:latest` with a pinned one:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build
        uses: docker/build-push-action@v7
        with:
          build-contexts: |
            alpine=docker-image://alpine:3.23
          tags: myimage:latest
```

## [Use image in subsequent steps](#use-image-in-subsequent-steps)

By default, the [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx) action uses `docker-container` as a build driver, so built Docker images aren't loaded automatically.

With named contexts you can reuse the built image:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        with:
          driver: docker

      - name: Build base image
        uses: docker/build-push-action@v7
        with:
          context: "{{defaultContext}}:base"
          load: true
          tags: my-base-image:latest

      - name: Build
        uses: docker/build-push-action@v7
        with:
          build-contexts: |
            alpine=docker-image://my-base-image:latest
          tags: myimage:latest
```

## [Using with a container builder](#using-with-a-container-builder)

As shown in the previous section we are not using the default [`docker-container` driver](https://docs.docker.com/build/builders/drivers/docker-container/) for building with named contexts. That's because this driver can't load an image from the Docker store as it's isolated. To solve this problem you can use a [local registry](https://docs.docker.com/build/ci/github-actions/local-registry/) to push your base image in your workflow:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN echo "Hello World"
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    services:
      registry:
        image: registry:3
        ports:
          - 5000:5000
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        with:
          # network=host driver-opt needed to push to local registry
          driver-opts: network=host

      - name: Build base image
        uses: docker/build-push-action@v7
        with:
          context: "{{defaultContext}}:base"
          tags: localhost:5000/my-base-image:latest
          push: true

      - name: Build
        uses: docker/build-push-action@v7
        with:
          build-contexts: |
            alpine=docker-image://localhost:5000/my-base-image:latest
          tags: myimage:latest
```

----
url: https://docs.docker.com/reference/cli/docker/volume/inspect/
----

# docker volume inspect

***

| Description | Display detailed information on one or more volumes  |
| ----------- | ---------------------------------------------------- |
| Usage       | `docker volume inspect [OPTIONS] VOLUME [VOLUME...]` |

## [Description](#description)

Returns information about a volume. By default, this command renders all results in a JSON array. You can specify an alternate format to execute a given template for each result. Go's [text/template](https://pkg.go.dev/text/template) package describes all the details of the format.

## [Options](#options)

| Option                    | Default | Description                                                                                                                                                                                                                             |
| ------------------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-f, --format`](#format) |         | Format output using a custom template: 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |

## [Examples](#examples)

```console
$ docker volume create myvolume

myvolume
```

Use the `docker volume inspect` comment to inspect the configuration of the volume:

```console
$ docker volume inspect myvolume
```

The output is in JSON format, for example:

```json
[
  {
    "CreatedAt": "2020-04-19T11:00:21Z",
    "Driver": "local",
    "Labels": {},
    "Mountpoint": "/var/lib/docker/volumes/8140a838303144125b4f54653b47ede0486282c623c3551fbc7f390cdc3e9cf5/_data",
    "Name": "myvolume",
    "Options": {},
    "Scope": "local"
  }
]
```

### [Format the output (--format)](#format)

Use the `--format` flag to format the output using a Go template, for example, to print the `Mountpoint` property:

```console
$ docker volume inspect --format '{{ .Mountpoint }}' myvolume

/var/lib/docker/volumes/myvolume/_data
```

----
url: https://docs.docker.com/guides/golang/build-images/
----

# Build your Go image

***

Table of contents

***

## [Overview](#overview)

In this section you're going to build a container image. The image includes everything you need to run your application – the compiled application binary file, the runtime, the libraries, and all other resources required by your application.

## [Required software](#required-software)

To complete this tutorial, you need the following:

* Docker running locally. Follow the [instructions to download and install Docker](https://docs.docker.com/desktop/).
* An IDE or a text editor to edit files. [Visual Studio Code](https://code.visualstudio.com/) is a free and popular choice but you can use anything you feel comfortable with.
* A Git client. This guide uses a command-line based `git` client, but you are free to use whatever works for you.
* A command-line terminal application. The examples shown in this module are from the Linux shell, but they should work in PowerShell, Windows Command Prompt, or OS X Terminal with minimal, if any, modifications.

## [Meet the example application](#meet-the-example-application)

The example application is a caricature of a microservice. It is purposefully trivial to keep focus on learning the basics of containerization for Go applications.

The application offers two HTTP endpoints:

* It responds with a string containing a heart symbol (`<3`) to requests to `/`.
* It responds with `{"Status" : "OK"}` JSON to a request to `/health`.

It responds with HTTP error 404 to any other request.

The application listens on a TCP port defined by the value of environment variable `PORT`. The default value is `8080`.

The application is stateless.

The complete source code for the application is on GitHub: [github.com/docker/docker-gs-ping](https://github.com/docker/docker-gs-ping). You are encouraged to fork it and experiment with it as much as you like.

To continue, clone the application repository to your local machine:

```console
$ git clone https://github.com/docker/docker-gs-ping
```

The application's `main.go` file is straightforward, if you are familiar with Go:

```go
package main

import (
	"net/http"
	"os"

	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {

	e := echo.New()

	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", func(c echo.Context) error {
		return c.HTML(http.StatusOK, "Hello, Docker! <3")
	})

	e.GET("/health", func(c echo.Context) error {
		return c.JSON(http.StatusOK, struct{ Status string }{Status: "OK"})
	})

	httpPort := os.Getenv("PORT")
	if httpPort == "" {
		httpPort = "8080"
	}

	e.Logger.Fatal(e.Start(":" + httpPort))
}

// Simple implementation of an integer minimum
// Adapted from: https://gobyexample.com/testing-and-benchmarking
func IntMin(a, b int) int {
	if a < b {
		return a
	}
	return b
}
```

## [Create a Dockerfile for the application](#create-a-dockerfile-for-the-application)

To build a container image with Docker, a `Dockerfile` with build instructions is required.

Begin your `Dockerfile` with the (optional) parser directive line that instructs BuildKit to interpret your file according to the grammar rules for the specified version of the syntax.

You then tell Docker what base image you would like to use for your application:

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19
```

Docker images can be inherited from other images. Therefore, instead of creating your own base image from scratch, you can use the official Go image that already has all necessary tools and libraries to compile and run a Go application.

> Note
>
> If you are curious about creating your own base images, you can check out the following section of this guide: [creating base images](https://docs.docker.com/build/building/base-images/#create-a-base-image). Note, however, that this isn't necessary to continue with your task at hand.

Now that you have defined the base image for your upcoming container image, you can begin building on top of it.

To make things easier when running the rest of your commands, create a directory inside the image that you're building. This also instructs Docker to use this directory as the default destination for all subsequent commands. This way you don't have to type out full file paths in the `Dockerfile`, the relative paths will be based on this directory.

```dockerfile
WORKDIR /app
```

Usually the very first thing you do once you’ve downloaded a project written in Go is to install the modules necessary to compile it. Note, that the base image has the toolchain already, but your source code isn't in it yet.

So before you can run `go mod download` inside your image, you need to get your `go.mod` and `go.sum` files copied into it. Use the `COPY` command to do this.

In its simplest form, the `COPY` command takes two parameters. The first parameter tells Docker what files you want to copy into the image. The last parameter tells Docker where you want that file to be copied to.

Copy the `go.mod` and `go.sum` file into your project directory `/app` which, owing to your use of `WORKDIR`, is the current directory (`./`) inside the image. Unlike some modern shells that appear to be indifferent to the use of trailing slash (`/`), and can figure out what the user meant (most of the time), Docker's `COPY` command is quite sensitive in its interpretation of the trailing slash.

```dockerfile
COPY go.mod go.sum ./
```

> Note
>
> If you'd like to familiarize yourself with the trailing slash treatment by the `COPY` command, see [Dockerfile reference](https://docs.docker.com/reference/dockerfile/#copy). This trailing slash can cause issues in more ways than you can imagine.

Now that you have the module files inside the Docker image that you are building, you can use the `RUN` command to run the command `go mod download` there as well. This works exactly the same as if you were running `go` locally on your machine, but this time these Go modules will be installed into a directory inside the image.

```dockerfile
RUN go mod download
```

At this point, you have a Go toolchain version 1.19.x and all your Go dependencies installed inside the image.

The next thing you need to do is to copy your source code into the image. You’ll use the `COPY` command just like you did with your module files before.

```dockerfile
COPY *.go ./
```

This `COPY` command uses a wildcard to copy all files with `.go` extension located in the current directory on the host (the directory where the `Dockerfile` is located) into the current directory inside the image.

Now, to compile your application, use the familiar `RUN` command:

```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping
```

This should be familiar. The result of that command will be a static application binary named `docker-gs-ping` and located in the root of the filesystem of the image that you are building. You could have put the binary into any other place you desire inside that image, the root directory has no special meaning in this regard. It's convenient to use it to keep the file paths short for improved readability.

Now, all that is left to do is to tell Docker what command to run when your image is used to start a container.

You do this with the `CMD` command:

```dockerfile
CMD ["/docker-gs-ping"]
```

Here's the complete `Dockerfile`:

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.19

# Set destination for COPY
WORKDIR /app

# Download Go modules
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code. Note the slash at the end, as explained in
# https://docs.docker.com/reference/dockerfile/#copy
COPY *.go ./

# Build
RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Optional:
# To bind to a TCP port, runtime parameters must be supplied to the docker command.
# But we can document in the Dockerfile what ports
# the application is going to listen on by default.
# https://docs.docker.com/reference/dockerfile/#expose
EXPOSE 8080

# Run
CMD ["/docker-gs-ping"]
```

The `Dockerfile` may also contain comments. They always begin with a `#` symbol, and must be at the beginning of a line. Comments are there for your convenience to allow documenting your `Dockerfile`.

There is also a concept of Dockerfile directives, such as the `syntax` directive you added. The directives must always be at the very top of the `Dockerfile`, so when adding comments, make sure that the comments follow after any directives that you may have used:

```dockerfile
# syntax=docker/dockerfile:1
# A sample microservice in Go packaged into a container image.

FROM golang:1.19

# ...
```

## [Build the image](#build-the-image)

Now that you've created your `Dockerfile`, build an image from it. The `docker build` command creates Docker images from the `Dockerfile` and a context. A build context is the set of files located in the specified path or URL. The Docker build process can access any of the files located in the context.

The build command optionally takes a `--tag` flag. This flag is used to label the image with a string value, which is easy for humans to read and recognize. If you don't pass a `--tag`, Docker will use `latest` as the default value.

Build your first Docker image.

```console
$ docker build --tag docker-gs-ping .
```

The build process will print some diagnostic messages as it goes through the build steps. The following is an example of what these messages may look like.

```console
[+] Building 2.2s (15/15) FINISHED
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => => transferring dockerfile: 701B                                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => => transferring context: 2B                                                                                                            0.0s
 => resolve image config for docker.io/docker/dockerfile:1                                                                                 1.1s
 => CACHED docker-image://docker.io/docker/dockerfile:1@sha256:39b85bbfa7536a5feceb7372a0817649ecb2724562a38360f4d6a7782a409b14            0.0s
 => [internal] load build definition from Dockerfile                                                                                       0.0s
 => [internal] load .dockerignore                                                                                                          0.0s
 => [internal] load metadata for docker.io/library/golang:1.19                                                                             0.7s
 => [1/6] FROM docker.io/library/golang:1.19@sha256:5d947843dde82ba1df5ac1b2ebb70b203d106f0423bf5183df3dc96f6bc5a705                       0.0s
 => [internal] load build context                                                                                                          0.0s
 => => transferring context: 6.08kB                                                                                                        0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                              0.0s
 => CACHED [3/6] COPY go.mod go.sum ./                                                                                                     0.0s
 => CACHED [4/6] RUN go mod download                                                                                                       0.0s
 => CACHED [5/6] COPY *.go ./                                                                                                              0.0s
 => CACHED [6/6] RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping                                                                  0.0s
 => exporting to image                                                                                                                     0.0s
 => => exporting layers                                                                                                                    0.0s
 => => writing image sha256:ede8ff889a0d9bc33f7a8da0673763c887a258eb53837dd52445cdca7b7df7e3                                               0.0s
 => => naming to docker.io/library/docker-gs-ping                                                                                          0.0s
```

Your exact output will vary, but provided there aren't any errors, you should see the word `FINISHED` in the first line of output. This means Docker has successfully built your image named `docker-gs-ping`.

## [View local images](#view-local-images)

To see the list of images you have on your local machine, you have two options. One is to use the CLI and the other is to use [Docker Desktop](https://docs.docker.com/desktop/). Since you're working in the terminal, take a look at listing images with the CLI.

To list images, run the `docker image ls`command (or the `docker images` shorthand):

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   2 minutes ago   1.11GB
...
```

Your exact output may vary, but you should see the `docker-gs-ping` image with the `latest` tag. Because you didn't specify a custom tag when you built your image, Docker assumed that the tag would be `latest`, which is a special value.

## [Tag images](#tag-images)

An image name is made up of slash-separated name components. Name components may contain lowercase letters, digits, and separators. A separator is defined as a period, one or two underscores, or one or more dashes. A name component may not start or end with a separator.

An image is made up of a manifest and a list of layers. In simple terms, a tag points to a combination of these artifacts. You can have multiple tags for the image and, in fact, most images have multiple tags. Create a second tag for the image you built and take a look at its layers.

Use the `docker image tag` (or `docker tag` shorthand) command to create a new tag for your image. This command takes two arguments; the first argument is the source image, and the second is the new tag to create. The following command creates a new `docker-gs-ping:v1.0` tag for the `docker-gs-ping:latest` you built:

```console
$ docker image tag docker-gs-ping:latest docker-gs-ping:v1.0
```

The Docker `tag` command creates a new tag for the image. It doesn't create a new image. The tag points to the same image and is another way to reference the image.

Now run the `docker image ls` command again to see the updated list of local images:

```console
$ docker image ls

REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   6 minutes ago   1.11GB
docker-gs-ping                   v1.0      7f153fbcc0a8   6 minutes ago   1.11GB
...
```

You can see that you have two images that start with `docker-gs-ping`. You know they're the same image because if you look at the `IMAGE ID` column, you can see that the values are the same for the two images. This value is a unique identifier Docker uses internally to identify the image.

Remove the tag that you just created. To do this, you’ll use the `docker image rm` command, or the shorthand `docker rmi` (which stands for "remove image"):

```console
$ docker image rm docker-gs-ping:v1.0
Untagged: docker-gs-ping:v1.0
```

Notice that the response from Docker tells you that the image hasn't been removed but only untagged.

Verify this by running the following command:

```console
$ docker image ls
```

You will see that the tag `v1.0` is no longer in the list of images kept by your Docker instance.

```text
REPOSITORY                       TAG       IMAGE ID       CREATED         SIZE
docker-gs-ping                   latest    7f153fbcc0a8   7 minutes ago   1.11GB
...
```

The tag `v1.0` has been removed but you still have the `docker-gs-ping:latest` tag available on your machine, so the image is there.

## [Multi-stage builds](#multi-stage-builds)

You may have noticed that your `docker-gs-ping` image weighs in at over a gigabyte, which is a lot for a tiny compiled Go application. You may also be wondering what happened to the full suite of Go tools, including the compiler, after you had built your image.

The answer is that the full toolchain is still there, in the container image. Not only this is inconvenient because of the large file size, but it may also present a security risk when the container is deployed.

These two issues can be solved by using [multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

In a nutshell, a multi-stage build can carry over the artifacts from one build stage into another, and every build stage can be instantiated from a different base image.

Thus, in the following example, you are going to use a full-scale official Go image to build your application. Then you'll copy the application binary into another image whose base is very lean and doesn't include the Go toolchain or other optional components.

The `Dockerfile.multistage` in the sample application's repository has the following content:

```dockerfile
# syntax=docker/dockerfile:1

# Build the application from source
FROM golang:1.19 AS build-stage

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY *.go ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /docker-gs-ping

# Run the tests in the container
FROM build-stage AS run-test-stage
RUN go test -v ./...

# Deploy the application binary into a lean image
FROM gcr.io/distroless/base-debian11 AS build-release-stage

WORKDIR /

COPY --from=build-stage /docker-gs-ping /docker-gs-ping

EXPOSE 8080

USER nonroot:nonroot

ENTRYPOINT ["/docker-gs-ping"]
```

Since you have two Dockerfiles now, you have to tell Docker what Dockerfile you'd like to use to build the image. Tag the new image with `multistage`. This tag (like any other, apart from `latest`) has no special meaning for Docker, it's something you chose.

```console
$ docker build -t docker-gs-ping:multistage -f Dockerfile.multistage .
```

Comparing the sizes of `docker-gs-ping:multistage` and `docker-gs-ping:latest` you see a few orders-of-magnitude difference.

```console
$ docker image ls
REPOSITORY       TAG          IMAGE ID       CREATED              SIZE
docker-gs-ping   multistage   e3fdde09f172   About a minute ago   28.1MB
docker-gs-ping   latest       336a3f164d0f   About an hour ago    1.11GB
```

This is so because the ["distroless"](https://github.com/GoogleContainerTools/distroless) base image that you have used in the second stage of the build is very barebones and is designed for lean deployments of static binaries.

There's much more to multi-stage builds, including the possibility of multi-architecture builds, so feel free to check out [multi-stage builds](https://docs.docker.com/build/building/multi-stage/). This is, however, not essential for your progress here.

## [Next steps](#next-steps)

In this module, you met your example application and built and container image for it.

In the next module, you’ll take a look at how to run your image as a container.

[Run your Go image as a container »](https://docs.docker.com/guides/golang/run-containers/)

----
url: https://docs.docker.com/dhi/explore/test/
----

# How Docker Hardened Images are tested

***

Table of contents

***

Docker Hardened Images (DHIs) are designed to be secure, minimal, and production-ready. To ensure their reliability and security, Docker employs a comprehensive testing strategy, which you can independently verify using signed attestations and open tooling.

Every image is tested for standards compliance, functionality, and security. The results of this testing are embedded as signed attestations, which can be [inspected and verified](#view-and-verify-the-test-attestation) programmatically using the Docker Scout CLI.

## [Testing strategy overview](#testing-strategy-overview)

The testing process for DHIs focuses on two main areas:

* Image standards compliance: Ensuring that each image adheres to strict size, security, and compatibility standards.
* Application functionality: Verifying that applications within the images function correctly.

## [Image standards compliance](#image-standards-compliance)

Each DHI undergoes rigorous checks to meet the following standards:

* Minimal attack surface: Images are built to be as small as possible, removing unnecessary components to reduce potential vulnerabilities.
* Near-zero known CVEs: Images are scanned using tools like Docker Scout to ensure they are free from known Common Vulnerabilities and Exposures (CVEs).
* Multi-architecture support: DHIs are built for multiple architectures (`linux/amd64` and `linux/arm64`) to ensure broad compatibility.
* Kubernetes compatibility: Images are tested to run seamlessly within Kubernetes clusters, ensuring they meet the requirements for container orchestration environments.

## [Application functionality testing](#application-functionality-testing)

Docker tests Docker Hardened Images to ensure they behave as expected in typical usage scenarios. This includes verifying that:

* Applications start and run successfully in containerized environments.
* Runtime behavior aligns with upstream expectations.
* Build variants (like `-dev` images) support common development and build tasks.

The goal is to ensure that DHIs work out of the box for the most common use cases while maintaining the hardened, minimal design.

## [Automated testing and CI/CD integration](#automated-testing-and-cicd-integration)

Docker integrates automated testing into its Continuous Integration/Continuous Deployment (CI/CD) pipelines:

* Automated scans: Each image build triggers automated scans for vulnerabilities and compliance checks.
* Reproducible builds: Build processes are designed to be reproducible, ensuring consistency across different environments.
* Continuous monitoring: Docker continuously monitors for new vulnerabilities and updates images accordingly to maintain security standards.

## [Testing attestation](#testing-attestation)

Docker provides a test attestation that details the testing and validation processes each DHI has undergone.

### [View and verify the test attestation](#view-and-verify-the-test-attestation)

You can view and verify this attestation using the Docker Scout CLI.

1. Use the `docker scout attest get` command with the test predicate type:

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/<image>:<tag>
   ```

   > Note
   >
   > If the image exists locally on your device, you must prefix the image name with `registry://`. For example, use `registry://dhi.io/python` instead of `dhi.io/python`.

   For example:

   ```console
   $ docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --predicate \
     dhi.io/python:3.13
   ```

   This contains a list of tests and their results.

   Example output:

   ```console
       v SBOM obtained from attestation, 101 packages found
       v Provenance obtained from attestation
       {
         "reportFormat": "CTRF",
         "results": {
           "summary": {
             "failed": 0,
             "passed": 1,
             "skipped": 0,
             "start": 1749216533,
             "stop": 1749216574,
             "tests": 1
           },
           "tests": [
             {
               ...
   ```

2. Verify the test attestation signature. To ensure the attestation is authentic and signed by Docker, run:

   ```console
   docker scout attest get \
     --predicate-type https://scout.docker.com/tests/v0.1 \
     --verify \
     dhi.io/<image>:<tag> --platform <platform>
   ```

   Example output:

   ```console
    v SBOM obtained from attestation, 101 packages found
    v Provenance obtained from attestation
    v cosign verify registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 \
        --key https://registry.scout.docker.com/keyring/dhi/latest.pub --experimental-oci11

      Verification for registry.scout.docker.com/docker/dhi-python@sha256:70c8299c4d3cb4d5432734773c45ae58d8acc2f2f07803435c65515f662136d5 --
      The following checks were performed on each of these signatures:
        - The cosign claims were validated
        - Existence of the claims in the transparency log was verified offline
        - The signatures were verified against the specified public key

    i Signature payload
    ...
   ```

If the attestation is valid, Docker Scout will confirm the signature and show the matching `cosign verify` command.

To view other attestations, such as SBOMs or vulnerability reports, see [Verify an image](https://docs.docker.com/dhi/how-to/verify/).

----
url: https://docs.docker.com/docker-hub/repos/manage/webhooks/
----

# Webhooks

***

Table of contents

***

You can use webhooks to cause an action in another service in response to a push event in the repository. Webhooks are POST requests sent to a URL you define in Docker Hub.

## [Create a webhook](#create-a-webhook)

To create a webhook:

1. In your chosen repository, select the **Webhooks** tab.
2. Provide a name for the webhook.
3. Provide a destination webhook URL. This is where webhook POST requests are delivered. The URL must be 255 characters or fewer.
4. Select **Create**.

## [View webhook delivery history](#view-webhook-delivery-history)

To view the history of the webhook:

1. Hover over your webhook under the **Current Webhooks section**.
2. Select the **Menu options** icon.
3. Select **View History**.

You can then view the delivery history, and whether delivering the POST request was successful or not.

## [Example webhook payload](#example-webhook-payload)

Webhook payloads have the following JSON format:

```json
{
  "callback_url": "https://registry.hub.docker.com/u/svendowideit/testhook/hook/2141b5bi5i5b02bec211i4eeih0242eg11000a/",
  "push_data": {
    "pushed_at": 1417566161,
    "pusher": "trustedbuilder",
    "tag": "latest"
  },
  "repository": {
    "comment_count": 0,
    "date_created": 1417494799,
    "description": "",
    "dockerfile": "#\n# BUILD\u0009\u0009docker build -t svendowideit/apt-cacher .\n# RUN\u0009\u0009docker run -d -p 3142:3142 -name apt-cacher-run apt-cacher\n#\n# and then you can run containers with:\n# \u0009\u0009docker run -t -i -rm -e http_proxy http://192.168.1.2:3142/ debian bash\n#\nFROM\u0009\u0009ubuntu\n\n\nVOLUME\u0009\u0009[/var/cache/apt-cacher-ng]\nRUN\u0009\u0009apt-get update ; apt-get install -yq apt-cacher-ng\n\nEXPOSE \u0009\u00093142\nCMD\u0009\u0009chmod 777 /var/cache/apt-cacher-ng ; /etc/init.d/apt-cacher-ng start ; tail -f /var/log/apt-cacher-ng/*\n",
    "full_description": "Docker Hub based automated build from a GitHub repo",
    "is_official": false,
    "is_private": true,
    "is_trusted": true,
    "name": "testhook",
    "namespace": "svendowideit",
    "owner": "svendowideit",
    "repo_name": "svendowideit/testhook",
    "repo_url": "https://registry.hub.docker.com/u/svendowideit/testhook/",
    "star_count": 0,
    "status": "Active"
  }
}
```

> Note
>
> The `callback_url` field is a legacy field and is no longer supported.

----
url: https://docs.docker.com/reference/cli/docker/service/create/
----

# docker service create

***

| Description | Create a new service                                       |
| ----------- | ---------------------------------------------------------- |
| Usage       | `docker service create [OPTIONS] IMAGE [COMMAND] [ARG...]` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Creates a service as described by the specified parameters.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                                              | Default      | Description                                                                                                    |
| --------------------------------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------- |
| `--cap-add`                                         |              | API 1.41+ Add Linux capabilities                                                                               |
| `--cap-drop`                                        |              | API 1.41+ Drop Linux capabilities                                                                              |
| [`--config`](#config)                               |              | API 1.30+ Specify configurations to expose to the service                                                      |
| [`--constraint`](#constraint)                       |              | Placement constraints                                                                                          |
| `--container-label`                                 |              | Container labels                                                                                               |
| `--credential-spec`                                 |              | API 1.29+ Credential spec for managed service account (Windows only)                                           |
| `-d, --detach`                                      |              | API 1.29+ Exit immediately instead of waiting for the service to converge                                      |
| `--dns`                                             |              | API 1.25+ Set custom DNS servers                                                                               |
| `--dns-option`                                      |              | API 1.25+ Set DNS options                                                                                      |
| `--dns-search`                                      |              | API 1.25+ Set custom DNS search domains                                                                        |
| `--endpoint-mode`                                   | `vip`        | Endpoint mode (vip or dnsrr)                                                                                   |
| `--entrypoint`                                      |              | Overwrite the default ENTRYPOINT of the image                                                                  |
| [`-e, --env`](#env)                                 |              | Set environment variables                                                                                      |
| `--env-file`                                        |              | Read in a file of environment variables                                                                        |
| `--generic-resource`                                |              | User defined resources                                                                                         |
| `--group`                                           |              | API 1.25+ Set one or more supplementary user groups for the container                                          |
| `--health-cmd`                                      |              | API 1.25+ Command to run to check health                                                                       |
| `--health-interval`                                 |              | API 1.25+ Time between running the check (ms\|s\|m\|h)                                                         |
| `--health-retries`                                  |              | API 1.25+ Consecutive failures needed to report unhealthy                                                      |
| `--health-start-interval`                           |              | API 1.44+ Time between running the check during the start period (ms\|s\|m\|h)                                 |
| `--health-start-period`                             |              | API 1.29+ Start period for the container to initialize before counting retries towards unstable (ms\|s\|m\|h)  |
| `--health-timeout`                                  |              | API 1.25+ Maximum time to allow one check to run (ms\|s\|m\|h)                                                 |
| `--host`                                            |              | API 1.25+ Set one or more custom host-to-IP mappings (host:ip)                                                 |
| [`--hostname`](#hostname)                           |              | API 1.25+ Container hostname                                                                                   |
| `--init`                                            |              | API 1.37+ Use an init inside each service container to forward signals and reap processes                      |
| [`--isolation`](#isolation)                         |              | API 1.35+ Service container isolation mode                                                                     |
| [`-l, --label`](#label)                             |              | Service labels                                                                                                 |
| `--limit-cpu`                                       |              | Limit CPUs                                                                                                     |
| `--limit-memory`                                    |              | Limit Memory                                                                                                   |
| `--limit-pids`                                      |              | API 1.41+ Limit maximum number of processes (default 0 = unlimited)                                            |
| `--log-driver`                                      |              | Logging driver for service                                                                                     |
| `--log-opt`                                         |              | Logging driver options                                                                                         |
| `--max-concurrent`                                  |              | API 1.41+ Number of job tasks to run concurrently (default equal to --replicas)                                |
| `--memory-swap`                                     |              | API 1.52+ Swap Bytes (-1 for unlimited)                                                                        |
| `--memory-swappiness`                               | `-1`         | API 1.52+ Tune memory swappiness (0-100), -1 to reset to default                                               |
| `--mode`                                            | `replicated` | Service mode (`replicated`, `global`, `replicated-job`, `global-job`)                                          |
| [`--mount`](#mount)                                 |              | Attach a filesystem mount to the service                                                                       |
| `--name`                                            |              | Service name                                                                                                   |
| [`--network`](#network)                             |              | Network attachments                                                                                            |
| `--no-healthcheck`                                  |              | API 1.25+ Disable any container-specified HEALTHCHECK                                                          |
| `--no-resolve-image`                                |              | API 1.30+ Do not query the registry to resolve image digest and supported platforms                            |
| `--oom-score-adj`                                   |              | API 1.46+ Tune host's OOM preferences (-1000 to 1000)                                                          |
| [`--placement-pref`](#placement-pref)               |              | API 1.28+ Add a placement preference                                                                           |
| [`-p, --publish`](#publish)                         |              | Publish a port as a node port                                                                                  |
| `-q, --quiet`                                       |              | Suppress progress output                                                                                       |
| `--read-only`                                       |              | API 1.28+ Mount the container's root filesystem as read only                                                   |
| [`--replicas`](#replicas)                           |              | Number of tasks                                                                                                |
| [`--replicas-max-per-node`](#replicas-max-per-node) |              | API 1.40+ Maximum number of tasks per node (default 0 = unlimited)                                             |
| `--reserve-cpu`                                     |              | Reserve CPUs                                                                                                   |
| [`--reserve-memory`](#reserve-memory)               |              | Reserve Memory                                                                                                 |
| `--restart-condition`                               |              | Restart when condition is met (`none`, `on-failure`, `any`) (default `any`)                                    |
| `--restart-delay`                                   |              | Delay between restart attempts (ns\|us\|ms\|s\|m\|h) (default 5s)                                              |
| `--restart-max-attempts`                            |              | Maximum number of restarts before giving up                                                                    |
| `--restart-window`                                  |              | Window used to evaluate the restart policy (ns\|us\|ms\|s\|m\|h)                                               |
| `--rollback-delay`                                  |              | API 1.28+ Delay between task rollbacks (ns\|us\|ms\|s\|m\|h) (default 0s)                                      |
| `--rollback-failure-action`                         |              | API 1.28+ Action on rollback failure (`pause`, `continue`) (default `pause`)                                   |
| `--rollback-max-failure-ratio`                      |              | API 1.28+ Failure rate to tolerate during a rollback (default 0)                                               |
| `--rollback-monitor`                                |              | API 1.28+ Duration after each task rollback to monitor for failure (ns\|us\|ms\|s\|m\|h) (default 5s)          |
| `--rollback-order`                                  |              | API 1.29+ Rollback order (`start-first`, `stop-first`) (default `stop-first`)                                  |
| `--rollback-parallelism`                            | `1`          | API 1.28+ Maximum number of tasks rolled back simultaneously (0 to roll back all at once)                      |
| [`--secret`](#secret)                               |              | API 1.25+ Specify secrets to expose to the service                                                             |
| `--stop-grace-period`                               |              | Time to wait before force killing a container (ns\|us\|ms\|s\|m\|h) (default 10s)                              |
| `--stop-signal`                                     |              | API 1.28+ Signal to stop the container                                                                         |
| `--sysctl`                                          |              | API 1.40+ Sysctl options                                                                                       |
| `-t, --tty`                                         |              | API 1.25+ Allocate a pseudo-TTY                                                                                |
| `--ulimit`                                          |              | API 1.41+ Ulimit options                                                                                       |
| [`--update-delay`](#update-delay)                   |              | Delay between updates (ns\|us\|ms\|s\|m\|h) (default 0s)                                                       |
| `--update-failure-action`                           |              | Action on update failure (`pause`, `continue`, `rollback`) (default `pause`)                                   |
| `--update-max-failure-ratio`                        |              | API 1.25+ Failure rate to tolerate during an update (default 0)                                                |
| `--update-monitor`                                  |              | API 1.25+ Duration after each task update to monitor for failure (ns\|us\|ms\|s\|m\|h) (default 5s)            |
| `--update-order`                                    |              | API 1.29+ Update order (`start-first`, `stop-first`) (default `stop-first`)                                    |
| `--update-parallelism`                              | `1`          | Maximum number of tasks updated simultaneously (0 to update all at once)                                       |
| `-u, --user`                                        |              | Username or UID (format: \<name\|uid>\[:\<group\|gid>])                                                        |
| [`--with-registry-auth`](#with-registry-auth)       |              | Send registry authentication details to swarm agents                                                           |
| `-w, --workdir`                                     |              | Working directory inside the container                                                                         |

## [Examples](#examples)

### [Create a service](#create-a-service)

```console
$ docker service create --name redis redis:7.4.1

dmu1ept4cxcfe8k8lhtux3ro3

$ docker service create --mode global --name redis2 redis:7.4.1

a8q9dasaafudfs8q8w32udass

$ docker service ls

ID            NAME    MODE        REPLICAS  IMAGE
dmu1ept4cxcf  redis   replicated  1/1       redis:7.4.1
a8q9dasaafud  redis2  global      1/1       redis:7.4.1
```

#### [Create a service using an image on a private registry (--with-registry-auth)](#with-registry-auth)

If your image is available on a private registry which requires login, use the `--with-registry-auth` flag with `docker service create`, after logging in. If your image is stored on `registry.example.com`, which is a private registry, use a command like the following:

```console
$ docker login registry.example.com

$ docker service  create \
  --with-registry-auth \
  --name my_service \
  registry.example.com/acme/my_image:latest
```

This passes the login token from your local client to the swarm nodes where the service is deployed, using the encrypted WAL logs. With this information, the nodes are able to log in to the registry and pull the image.

### [Create a service with 5 replica tasks (--replicas)](#replicas)

Use the `--replicas` flag to set the number of replica tasks for a replicated service. The following command creates a `redis` service with `5` replica tasks:

```console
$ docker service create --name redis --replicas=5 redis:7.4.1

4cdgfyky7ozwh3htjfw0d12qv
```

The above command sets the *desired* number of tasks for the service. Even though the command returns immediately, actual scaling of the service may take some time. The `REPLICAS` column shows both the actual and desired number of replica tasks for the service.

In the following example the desired state is `5` replicas, but the current number of `RUNNING` tasks is `3`:

```console
$ docker service ls

ID            NAME   MODE        REPLICAS  IMAGE
4cdgfyky7ozw  redis  replicated  3/5       redis:7.4.1
```

Once all the tasks are created and `RUNNING`, the actual number of tasks is equal to the desired number:

```console
$ docker service ls

ID            NAME   MODE        REPLICAS  IMAGE
4cdgfyky7ozw  redis  replicated  5/5       redis:7.4.1
```

### [Create a service with secrets (--secret)](#secret)

Use the `--secret` flag to give a container access to a [secret](/reference/cli/docker/secret/create/).

Create a service specifying a secret:

```console
$ docker service create --name redis --secret secret.json redis:7.4.1

4cdgfyky7ozwh3htjfw0d12qv
```

Create a service specifying the secret, target, user/group ID, and mode:

```console
$ docker service create --name redis \
    --secret source=ssh-key,target=ssh \
    --secret source=app-key,target=app,uid=1000,gid=1001,mode=0400 \
    redis:7.4.1

4cdgfyky7ozwh3htjfw0d12qv
```

To grant a service access to multiple secrets, use multiple `--secret` flags.

Secrets are located in `/run/secrets` in the container if no target is specified. If no target is specified, the name of the secret is used as the in memory file in the container. If a target is specified, that is used as the filename. In the example above, two files are created: `/run/secrets/ssh` and `/run/secrets/app` for each of the secret targets specified.

### [Create a service with configs (--config)](#config)

Use the `--config` flag to give a container access to a [config](/reference/cli/docker/config/create/).

Create a service with a config. The config will be mounted into `redis-config`, be owned by the user who runs the command inside the container (often `root`), and have file mode `0444` or world-readable. You can specify the `uid` and `gid` as numerical IDs or names. When using names, the provided group/user names must pre-exist in the container. The `mode` is specified as a 4-number sequence such as `0755`.

```console
$ docker service create --name=redis --config redis-conf redis:7.4.1
```

Create a service with a config and specify the target location and file mode:

```console
$ docker service create --name redis \
  --config source=redis-conf,target=/etc/redis/redis.conf,mode=0400 redis:7.4.1
```

To grant a service access to multiple configs, use multiple `--config` flags.

Configs are located in `/` in the container if no target is specified. If no target is specified, the name of the config is used as the name of the file in the container. If a target is specified, that is used as the filename.

### [Create a service with a rolling update policy](#update-delay)

```console
$ docker service create \
  --replicas 10 \
  --name redis \
  --update-delay 10s \
  --update-parallelism 2 \
  redis:7.4.1
```

When you run a [service update](/reference/cli/docker/service/update/), the scheduler updates a maximum of 2 tasks at a time, with `10s` between updates. For more information, refer to the [rolling updates tutorial](/engine/swarm/swarm-tutorial/rolling-update/).

### [Set environment variables (-e, --env)](#env)

This sets an environment variable for all tasks in a service. For example:

```console
$ docker service create \
  --name redis_2 \
  --replicas 5 \
  --env MYVAR=foo \
  redis:7.4.1
```

To specify multiple environment variables, specify multiple `--env` flags, each with a separate key-value pair.

```console
$ docker service create \
  --name redis_2 \
  --replicas 5 \
  --env MYVAR=foo \
  --env MYVAR2=bar \
  redis:7.4.1
```

### [Create a service with specific hostname (--hostname)](#hostname)

This option sets the docker service containers hostname to a specific string. For example:

```console
$ docker service create --name redis --hostname myredis redis:7.4.1
```

### [Set metadata on a service (-l, --label)](#label)

A label is a `key=value` pair that applies metadata to a service. To label a service with two labels:

```console
$ docker service create \
  --name redis_2 \
  --label com.example.foo="bar" \
  --label bar=baz \
  redis:7.4.1
```

For more information about labels, refer to [apply custom metadata](/config/labels-custom-metadata/).

### [Add bind mounts, volumes or memory filesystems (--mount)](#mount)

Docker supports three different kinds of mounts, which allow containers to read from or write to files or directories, either on the host operating system, or on memory filesystems. These types are data volumes (often referred to simply as volumes), bind mounts, tmpfs, and named pipes.

A **bind mount** makes a file or directory on the host available to the container it is mounted within. A bind mount may be either read-only or read-write. For example, a container might share its host's DNS information by means of a bind mount of the host's `/etc/resolv.conf` or a container might write logs to its host's `/var/log/myContainerLogs` directory. If you use bind mounts and your host and containers have different notions of permissions, access controls, or other such details, you will run into portability issues.

A **named volume** is a mechanism for decoupling persistent data needed by your container from the image used to create the container and from the host machine. Named volumes are created and managed by Docker, and a named volume persists even when no container is currently using it. Data in named volumes can be shared between a container and the host machine, as well as between multiple containers. Docker uses a *volume driver* to create, manage, and mount volumes. You can back up or restore volumes using Docker commands.

A **tmpfs** mounts a tmpfs inside a container for volatile data.

A **npipe** mounts a named pipe from the host into the container.

Consider a situation where your image starts a lightweight web server. You could use that image as a base image, copy in your website's HTML files, and package that into another image. Each time your website changed, you'd need to update the new image and redeploy all of the containers serving your website. A better solution is to store the website in a named volume which is attached to each of your web server containers when they start. To update the website, you just update the named volume.

For more information about named volumes, see [Data Volumes](/storage/volumes/).

The following table describes options which apply to both bind mounts and named volumes in a service:

| Option                                   | Required                         | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **type**                                 |                                  | The type of mount, can be either `volume`, `bind`, `tmpfs`, or `npipe`. Defaults to `volume` if no type is specified.- `volume`: mounts a [managed volume](/reference/cli/docker/volume/create/) into the container.
- `bind`: bind-mounts a directory or file from the host into the container.
- `tmpfs`: mount a tmpfs in the container
- `npipe`: mounts named pipe from the host into the container (Windows containers only).                                                                                                                                                                                                                                                                                                                                                 |
| **src** or **source**                    | for `type=bind` and `type=npipe` | * `type=volume`: `src` is an optional way to specify the name of the volume (for example, `src=my-volume`). If the named volume does not exist, it is automatically created. If no `src` is specified, the volume is assigned a random name which is guaranteed to be unique on the host, but may not be unique cluster-wide. A randomly-named volume has the same lifecycle as its container and is destroyed when the *container* is destroyed (which is upon `service update`, or when scaling or re-balancing the service)

* `type=bind`: `src` is required, and specifies an absolute path to the file or directory to bind-mount (for example, `src=/path/on/host/`). An error is produced if the file or directory does not exist.

* `type=tmpfs`: `src` is not supported. |
| **dst** or **destination** or **target** | yes                              | Mount path inside the container, for example `/some/path/in/container/`. If the path does not exist in the container's filesystem, the Engine creates a directory at the specified location before mounting the volume or bind mount.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **readonly** or **ro**                   |                                  | The Engine mounts binds and volumes `read-write` unless `readonly` option is given when mounting the bind or volume. Note that setting `readonly` for a bind-mount may not make its submounts `readonly` depending on the kernel version. See also `bind-recursive`.* `true` or `1` or no value: Mounts the bind or volume read-only.

* `false` or `0`: Mounts the bind or volume read-write.                                                                                                                                                                                                                                                                                                                                                                                      |

#### [Options for bind mounts](#options-for-bind-mounts)

The following options can only be used for bind mounts (`type=bind`):

| Option               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **bind-propagation** | See the [bind propagation section](#bind-propagation).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **consistency**      | The consistency requirements for the mount; one of- `default`: Equivalent to `consistent`.

- `consistent`: Full consistency. The container runtime and the host maintain an identical view of the mount at all times.

- `cached`: The host's view of the mount is authoritative. There may be delays before updates made on the host are visible within a container.

- `delegated`: The container runtime's view of the mount is authoritative. There may be delays before updates made in a container are visible on the host.                                                                                                                                                                                                                                                                                                                                                                                               |
| **bind-recursive**   | By default, submounts are recursively bind-mounted as well. However, this behavior can be confusing when a bind mount is configured with `readonly` option, because submounts may not be mounted as read-only, depending on the kernel version. Set `bind-recursive` to control the behavior of the recursive bind-mount. A value is one of: - <`enabled`: Enables recursive bind-mount. Read-only mounts are made recursively read-only if kernel is v5.12 or later. Otherwise they are not made recursively read-only.
- <`disabled`: Disables recursive bind-mount.
- <`writable`: Enables recursive bind-mount. Read-only mounts are not made recursively read-only.
- <`readonly`: Enables recursive bind-mount. Read-only mounts are made recursively read-only if kernel is v5.12 or later. Otherwise the Engine raises an error.When the option is not specified, the default behavior corresponds to setting `enabled`. |
| **bind-create-src**  | By default, bind mounts require the source path to exist on the daemon host. This is a significant difference from the `-v` flag, which creates the source path if it doesn't exist. Set `bind-create-src` to create the source path on the daemon host if it doesn't exist. A value is optional: - `true` or `1`: Create path on the daemon host if it doesn't exist.

- `false` or `0`: Default behavior. Produces an error if the source path doesn't exist on the daemon host.                                                                                                                                                                                                                                                                                                                                                                                                                                               |

##### [Bind propagation](#bind-propagation)

Bind propagation refers to whether or not mounts created within a given bind mount or named volume can be propagated to replicas of that mount. Consider a mount point `/mnt`, which is also mounted on `/tmp`. The propagation settings control whether a mount on `/tmp/a` would also be available on `/mnt/a`. Each propagation setting has a recursive counterpoint. In the case of recursion, consider that `/tmp/a` is also mounted as `/foo`. The propagation settings control whether `/mnt/a` and/or `/tmp/a` would exist.

The `bind-propagation` option defaults to `rprivate` for both bind mounts and volume mounts, and is only configurable for bind mounts. In other words, named volumes do not support bind propagation.

* **`shared`**: Sub-mounts of the original mount are exposed to replica mounts, and sub-mounts of replica mounts are also propagated to the original mount.
* **`slave`**: similar to a shared mount, but only in one direction. If the original mount exposes a sub-mount, the replica mount can see it. However, if the replica mount exposes a sub-mount, the original mount cannot see it.
* **`private`**: The mount is private. Sub-mounts within it are not exposed to replica mounts, and sub-mounts of replica mounts are not exposed to the original mount.
* **`rshared`**: The same as shared, but the propagation also extends to and from mount points nested within any of the original or replica mount points.
* **`rslave`**: The same as `slave`, but the propagation also extends to and from mount points nested within any of the original or replica mount points.
* **`rprivate`**: The default. The same as `private`, meaning that no mount points anywhere within the original or replica mount points propagate in either direction.

For more information about bind propagation, see the [Linux kernel documentation for shared subtree](https://www.kernel.org/doc/Documentation/filesystems/sharedsubtree.txt).

#### [Options for named volumes](#options-for-named-volumes)

The following options can only be used for named volumes (`type=volume`):

| Option            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **volume-driver** | Name of the volume-driver plugin to use for the volume. Defaults to `"local"`, to use the local volume driver to create the volume if the volume does not exist.                                                                                                                                                                                                                                                                                                                                          |
| **volume-label**  | One or more custom metadata ("labels") to apply to the volume upon creation. For example, `volume-label=mylabel=hello-world,my-other-label=hello-mars`. For more information about labels, refer to [apply custom metadata](/config/labels-custom-metadata/).                                                                                                                                                                                                                                             |
| **volume-nocopy** | By default, if you attach an empty volume to a container, and files or directories already existed at the mount-path in the container (`dst`), the Engine copies those files and directories into the volume, allowing the host to access them. Set `volume-nocopy` to disable copying files from the container's filesystem to the volume and mount the empty volume. A value is optional: - `true` or `1`: Default if you do not provide a value. Disables copying.

- `false` or `0`: Enables copying. |
| **volume-opt**    | Options specific to a given volume driver, which will be passed to the driver when creating the volume. Options are provided as a comma-separated list of key/value pairs, for example, `volume-opt=some-option=some-value,volume-opt=some-other-option=some-other-value`. For available options for a given driver, refer to that driver's documentation.                                                                                                                                                |

#### [Options for tmpfs](#options-for-tmpfs)

The following options can only be used for tmpfs mounts (`type=tmpfs`);

| Option         | Description                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------- |
| **tmpfs-size** | Size of the tmpfs mount in bytes. Unlimited by default in Linux.                            |
| **tmpfs-mode** | File mode of the tmpfs in octal. (e.g. `"700"` or `"0700"`.) Defaults to `"1777"` in Linux. |

#### [Differences between "--mount" and "--volume"](#differences-between---mount-and---volume)

The `--mount` flag supports most options that are supported by the `-v` or `--volume` flag for `docker run`, with some important exceptions:

* The `--mount` flag allows you to specify a volume driver and volume driver options *per volume*, without creating the volumes in advance. In contrast, `docker run` allows you to specify a single volume driver which is shared by all volumes, using the `--volume-driver` flag.

* The `--mount` flag allows you to specify custom metadata ("labels") for a volume, before the volume is created.

* When you use `--mount` with `type=bind`, the host-path must refer to an *existing* path on the host. The path will not be created for you and the service will fail with an error if the path does not exist. You can use `bind-create-src` to create the host path if it doesn't exist.

* The `--mount` flag does not allow you to relabel a volume with `Z` or `z` flags, which are used for `selinux` labeling.

#### [Create a service using a named volume](#create-a-service-using-a-named-volume)

The following example creates a service that uses a named volume:

```console
$ docker service create \
  --name my-service \
  --replicas 3 \
  --mount type=volume,source=my-volume,destination=/path/in/container,volume-label="color=red",volume-label="shape=round" \
  nginx:alpine
```

For each replica of the service, the engine requests a volume named "my-volume" from the default ("local") volume driver where the task is deployed. If the volume does not exist, the engine creates a new volume and applies the "color" and "shape" labels.

When the task is started, the volume is mounted on `/path/in/container/` inside the container.

Be aware that the default ("local") volume is a locally scoped volume driver. This means that depending on where a task is deployed, either that task gets a *new* volume named "my-volume", or shares the same "my-volume" with other tasks of the same service. Multiple containers writing to a single shared volume can cause data corruption if the software running inside the container is not designed to handle concurrent processes writing to the same location. Also take into account that containers can be re-scheduled by the Swarm orchestrator and be deployed on a different node.

#### [Create a service that uses an anonymous volume](#create-a-service-that-uses-an-anonymous-volume)

The following command creates a service with three replicas with an anonymous volume on `/path/in/container`:

```console
$ docker service create \
  --name my-service \
  --replicas 3 \
  --mount type=volume,destination=/path/in/container \
  nginx:alpine
```

In this example, no name (`source`) is specified for the volume, so a new volume is created for each task. This guarantees that each task gets its own volume, and volumes are not shared between tasks. Anonymous volumes are removed after the task using them is complete.

#### [Create a service that uses a bind-mounted host directory](#create-a-service-that-uses-a-bind-mounted-host-directory)

The following example bind-mounts a host directory at `/path/in/container` in the containers backing the service:

```console
$ docker service create \
  --name my-service \
  --mount type=bind,source=/path/on/host,destination=/path/in/container \
  nginx:alpine
```

### [Set service mode (--mode)](#set-service-mode---mode)

The service mode determines whether this is a *replicated* service or a *global* service. A replicated service runs as many tasks as specified, while a global service runs on each active node in the swarm.

The following command creates a global service:

```console
$ docker service create \
 --name redis_2 \
 --mode global \
 redis:7.4.1
```

### [Specify service constraints (--constraint)](#constraint)

You can limit the set of nodes where a task can be scheduled by defining constraint expressions. Constraint expressions can either use a *match* (`==`) or *exclude* (`!=`) rule. Multiple constraints find nodes that satisfy every expression (AND match). Constraints can match node or Docker Engine labels as follows:

| node attribute       | matches                        | example                                       |
| -------------------- | ------------------------------ | --------------------------------------------- |
| `node.id`            | Node ID                        | `node.id==2ivku8v2gvtg4`                      |
| `node.hostname`      | Node hostname                  | `node.hostname!=node-2`                       |
| `node.role`          | Node role (`manager`/`worker`) | `node.role==manager`                          |
| `node.platform.os`   | Node operating system          | `node.platform.os==windows`                   |
| `node.platform.arch` | Node architecture              | `node.platform.arch==x86_64`                  |
| `node.labels`        | User-defined node labels       | `node.labels.security==high`                  |
| `engine.labels`      | Docker Engine's labels         | `engine.labels.operatingsystem==ubuntu-24.04` |

`engine.labels` apply to Docker Engine labels like operating system, drivers, etc. Swarm administrators add `node.labels` for operational purposes by using the [`docker node update`](/reference/cli/docker/node/update/) command.

For example, the following limits tasks for the redis service to nodes where the node type label equals queue:

```console
$ docker service create \
  --name redis_2 \
  --constraint node.platform.os==linux \
  --constraint node.labels.type==queue \
  redis:7.4.1
```

If the service constraints exclude all nodes in the cluster, a message is printed that no suitable node is found, but the scheduler will start a reconciliation loop and deploy the service once a suitable node becomes available.

In the example below, no node satisfying the constraint was found, causing the service to not reconcile with the desired state:

```console
$ docker service create \
  --name web \
  --constraint node.labels.region==east \
  nginx:alpine

lx1wrhhpmbbu0wuk0ybws30bc
overall progress: 0 out of 1 tasks
1/1: no suitable node (scheduling constraints not satisfied on 5 nodes)

$ docker service ls
ID                  NAME     MODE         REPLICAS   IMAGE               PORTS
b6lww17hrr4e        web      replicated   0/1        nginx:alpine
```

After adding the `region=east` label to a node in the cluster, the service reconciles, and the desired number of replicas are deployed:

```console
$ docker node update --label-add region=east yswe2dm4c5fdgtsrli1e8ya5l
yswe2dm4c5fdgtsrli1e8ya5l

$ docker service ls
ID                  NAME     MODE         REPLICAS   IMAGE               PORTS
b6lww17hrr4e        web      replicated   1/1        nginx:alpine
```

### [Specify service placement preferences (--placement-pref)](#placement-pref)

You can set up the service to divide tasks evenly over different categories of nodes. One example of where this can be useful is to balance tasks over a set of datacenters or availability zones. The example below illustrates this:

```console
$ docker service create \
  --replicas 9 \
  --name redis_2 \
  --placement-pref spread=node.labels.datacenter \
  redis:7.4.1
```

This uses `--placement-pref` with a `spread` strategy (currently the only supported strategy) to spread tasks evenly over the values of the `datacenter` node label. In this example, we assume that every node has a `datacenter` node label attached to it. If there are three different values of this label among nodes in the swarm, one third of the tasks will be placed on the nodes associated with each value. This is true even if there are more nodes with one value than another. For example, consider the following set of nodes:

* Three nodes with `node.labels.datacenter=east`
* Two nodes with `node.labels.datacenter=south`
* One node with `node.labels.datacenter=west`

Since we are spreading over the values of the `datacenter` label and the service has 9 replicas, 3 replicas will end up in each datacenter. There are three nodes associated with the value `east`, so each one will get one of the three replicas reserved for this value. There are two nodes with the value `south`, and the three replicas for this value will be divided between them, with one receiving two replicas and another receiving just one. Finally, `west` has a single node that will get all three replicas reserved for `west`.

If the nodes in one category (for example, those with `node.labels.datacenter=south`) can't handle their fair share of tasks due to constraints or resource limitations, the extra tasks will be assigned to other nodes instead, if possible.

Both engine labels and node labels are supported by placement preferences. The example above uses a node label, because the label is referenced with `node.labels.datacenter`. To spread over the values of an engine label, use `--placement-pref spread=engine.labels.<labelname>`.

It is possible to add multiple placement preferences to a service. This establishes a hierarchy of preferences, so that tasks are first divided over one category, and then further divided over additional categories. One example of where this may be useful is dividing tasks fairly between datacenters, and then splitting the tasks within each datacenter over a choice of racks. To add multiple placement preferences, specify the `--placement-pref` flag multiple times. The order is significant, and the placement preferences will be applied in the order given when making scheduling decisions.

The following example sets up a service with multiple placement preferences. Tasks are spread first over the various datacenters, and then over racks (as indicated by the respective labels):

```console
$ docker service create \
  --replicas 9 \
  --name redis_2 \
  --placement-pref 'spread=node.labels.datacenter' \
  --placement-pref 'spread=node.labels.rack' \
  redis:7.4.1
```

When updating a service with `docker service update`, `--placement-pref-add` appends a new placement preference after all existing placement preferences. `--placement-pref-rm` removes an existing placement preference that matches the argument.

### [Specify memory requirements and constraints for a service (--reserve-memory and --limit-memory)](#reserve-memory)

If your service needs a minimum amount of memory in order to run correctly, you can use `--reserve-memory` to specify that the service should only be scheduled on a node with this much memory available to reserve. If no node is available that meets the criteria, the task is not scheduled, but remains in a pending state.

The following example requires that 4GB of memory be available and reservable on a given node before scheduling the service to run on that node.

```console
$ docker service create --reserve-memory=4GB --name=too-big nginx:alpine
```

The managers won't schedule a set of containers on a single node whose combined reservations exceed the memory available on that node.

After a task is scheduled and running, `--reserve-memory` does not enforce a memory limit. Use `--limit-memory` to ensure that a task uses no more than a given amount of memory on a node. This example limits the amount of memory used by the task to 4GB. The task will be scheduled even if each of your nodes has only 2GB of memory, because `--limit-memory` is an upper limit.

```console
$ docker service create --limit-memory=4GB --name=too-big nginx:alpine
```

Using `--reserve-memory` and `--limit-memory` does not guarantee that Docker will not use more memory on your host than you want. For instance, you could create many services, the sum of whose memory usage could exhaust the available memory.

You can prevent this scenario from exhausting the available memory by taking into account other (non-containerized) software running on the host as well. If `--reserve-memory` is greater than or equal to `--limit-memory`, Docker won't schedule a service on a host that doesn't have enough memory. `--limit-memory` will limit the service's memory to stay within that limit, so if every service has a memory-reservation and limit set, Docker services will be less likely to saturate the host. Other non-service containers or applications running directly on the Docker host could still exhaust memory.

There is a downside to this approach. Reserving memory also means that you may not make optimum use of the memory available on the node. Consider a service that under normal circumstances uses 100MB of memory, but depending on load can "peak" at 500MB. Reserving 500MB for that service (to guarantee can have 500MB for those "peaks") results in 400MB of memory being wasted most of the time.

In short, you can take a more conservative or more flexible approach:

* **Conservative**: reserve 500MB, and limit to 500MB. Basically you're now treating the service containers as VMs, and you may be losing a big advantage containers, which is greater density of services per host.

* **Flexible**: limit to 500MB in the assumption that if the service requires more than 500MB, it is malfunctioning. Reserve something between the 100MB "normal" requirement and the 500MB "peak" requirement". This assumes that when this service is at "peak", other services or non-container workloads probably won't be.

The approach you take depends heavily on the memory-usage patterns of your workloads. You should test under normal and peak conditions before settling on an approach.

On Linux, you can also limit a service's overall memory footprint on a given host at the level of the host operating system, using `cgroups` or other relevant operating system tools.

### [Specify maximum replicas per node (--replicas-max-per-node)](#replicas-max-per-node)

Use the `--replicas-max-per-node` flag to set the maximum number of replica tasks that can run on a node. The following command creates a nginx service with 2 replica tasks but only one replica task per node.

One example where this can be useful is to balance tasks over a set of data centers together with `--placement-pref` and let `--replicas-max-per-node` setting make sure that replicas are not migrated to another datacenter during maintenance or datacenter failure.

The example below illustrates this:

```console
$ docker service create \
  --name nginx \
  --replicas 2 \
  --replicas-max-per-node 1 \
  --placement-pref 'spread=node.labels.datacenter' \
  nginx
```

### [Attach a service to an existing network (--network)](#network)

You can use overlay networks to connect one or more services within the swarm.

First, create an overlay network on a manager node the docker network create command:

```console
$ docker network create --driver overlay my-network

etjpu59cykrptrgw0z0hk5snf
```

After you create an overlay network in swarm mode, all manager nodes have access to the network.

When you create a service and pass the `--network` flag to attach the service to the overlay network:

```console
$ docker service create \
  --replicas 3 \
  --network my-network \
  --name my-web \
  nginx

716thylsndqma81j6kkkb5aus
```

The swarm extends my-network to each node running the service.

Containers on the same network can access each other using [service discovery](/engine/network/drivers/overlay/#container-discovery).

Long form syntax of `--network` allows to specify list of aliases and driver options: `--network name=my-network,alias=web1,driver-opt=field1=value1`

### [Publish service ports externally to the swarm (-p, --publish)](#publish)

You can publish service ports to make them available externally to the swarm using the `--publish` flag. The `--publish` flag can take two different styles of arguments. The short version is positional, and allows you to specify the published port and target port separated by a colon (`:`).

```console
$ docker service create --name my_web --replicas 3 --publish 8080:80 nginx
```

There is also a long format, which is easier to read and allows you to specify more options. The long format is preferred. You cannot specify the service's mode when using the short format. Here is an example of using the long format for the same service as above:

```console
$ docker service create --name my_web --replicas 3 --publish published=8080,target=80 nginx
```

The options you can specify are:

| Option                    | Short syntax                            | Long syntax                                       | Description                                                                                                                                                                                                                                                            |
| ------------------------- | --------------------------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| published and target port | `--publish 8080:80`                     | `--publish published=8080,target=80`              | The target port within the container and the port to map it to on the nodes, using the routing mesh (`ingress`) or host-level networking. More options are available, later in this table. The key-value syntax is preferred, because it is somewhat self-documenting. |
| mode                      | Not possible to set using short syntax. | `--publish published=8080,target=80,mode=host`    | The mode to use for binding the port, either `ingress` or `host`. Defaults to `ingress` to use the routing mesh.                                                                                                                                                       |
| protocol                  | `--publish 8080:80/tcp`                 | `--publish published=8080,target=80,protocol=tcp` | The protocol to use, `tcp` , `udp`, or `sctp`. Defaults to `tcp`. To bind a port for both protocols, specify the `-p` or `--publish` flag twice.                                                                                                                       |

When you publish a service port using `ingress` mode, the swarm routing mesh makes the service accessible at the published port on every node regardless if there is a task for the service running on the node. If you use `host` mode, the port is only bound on nodes where the service is running, and a given port on a node can only be bound once. You can only set the publication mode using the long syntax. For more information refer to [Use swarm mode routing mesh](/engine/swarm/ingress/).

### [Provide credential specs for managed service accounts (--credentials-spec)](#credentials-spec)

This option is only used for services using Windows containers. The `--credential-spec` must be in the format `file://<filename>` or `registry://<value-name>`.

When using the `file://<filename>` format, the referenced file must be present in the `CredentialSpecs` subdirectory in the docker data directory, which defaults to `C:\ProgramData\Docker\` on Windows. For example, specifying `file://spec.json` loads `C:\ProgramData\Docker\CredentialSpecs\spec.json`.

When using the `registry://<value-name>` format, the credential spec is read from the Windows registry on the daemon's host. The specified registry value must be located in:

```
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization\Containers\CredentialSpecs
```

### [Create services using templates](#create-services-using-templates)

You can use templates for some flags of `service create`, using the syntax provided by the Go's [text/template](https://pkg.go.dev/text/template) package.

The supported flags are the following :

* `--hostname`
* `--mount`
* `--env`

Valid placeholders for the Go template are listed below:

| Placeholder       | Description    |
| ----------------- | -------------- |
| `.Service.ID`     | Service ID     |
| `.Service.Name`   | Service name   |
| `.Service.Labels` | Service labels |
| `.Node.ID`        | Node ID        |
| `.Node.Hostname`  | Node Hostname  |
| `.Task.ID`        | Task ID        |
| `.Task.Name`      | Task name      |
| `.Task.Slot`      | Task slot      |

#### [Template example](#template-example)

In this example, we are going to set the template of the created containers based on the service's name, the node's ID and hostname where it sits.

```console
$ docker service create \
    --name hosttempl \
    --hostname="{{.Node.Hostname}}-{{.Node.ID}}-{{.Service.Name}}"\
    busybox top

va8ew30grofhjoychbr6iot8c

$ docker service ps va8ew30grofhjoychbr6iot8c

ID            NAME         IMAGE                                                                                   NODE          DESIRED STATE  CURRENT STATE               ERROR  PORTS
wo41w8hg8qan  hosttempl.1  busybox:latest@sha256:29f5d56d12684887bdfa50dcd29fc31eea4aaf4ad3bec43daf19026a7ce69912  2e7a8a9c4da2  Running        Running about a minute ago

$ docker inspect --format="{{.Config.Hostname}}" 2e7a8a9c4da2-wo41w8hg8qanxwjwsg4kxpprj-hosttempl

x3ti0erg11rjpg64m75kej2mz-hosttempl
```

### [Specify isolation mode on Windows (--isolation)](#isolation)

By default, tasks scheduled on Windows nodes are run using the default isolation mode configured for this particular node. To force a specific isolation mode, you can use the `--isolation` flag:

```console
$ docker service create --name myservice --isolation=process microsoft/nanoserver
```

Supported isolation modes on Windows are:

* `default`: use default settings specified on the node running the task
* `process`: use process isolation (Windows server only)
* `hyperv`: use Hyper-V isolation

### [Create services requesting Generic Resources (--generic-resources)](#generic-resources)

You can narrow the kind of nodes your task can land on through the using the `--generic-resource` flag (if the nodes advertise these resources):

```console
$ docker service create \
    --name cuda \
    --generic-resource "NVIDIA-GPU=2" \
    --generic-resource "SSD=1" \
    nvidia/cuda
```

### [Running as a job](#running-as-a-job)

Jobs are a special kind of service designed to run an operation to completion and then stop, as opposed to running long-running daemons. When a Task belonging to a job exits successfully (return value 0), the Task is marked as "Completed", and is not run again.

Jobs are started by using one of two modes, `replicated-job` or `global-job`

```console
$ docker service create --name myjob \
                        --mode replicated-job \
                        bash "true"
```

This command will run one Task, which will, using the `bash` image, execute the command `true`, which will return 0 and then exit.

Though Jobs are ultimately a different kind of service, they a couple of caveats compared to other services:

* None of the update or rollback configuration options are valid. Jobs can be updated, but cannot be rolled out or rolled back, making these configuration options moot.
* Jobs are never restarted on reaching the `Complete` state. This means that for jobs, setting `--restart-condition` to `any` is the same as setting it to `on-failure`.

Jobs are available in both replicated and global modes.

#### [Replicated Jobs](#replicated-jobs)

A replicated job is like a replicated service. Setting the `--replicas` flag will specify total number of iterations of a job to execute.

By default, all replicas of a replicated job will launch at once. To control the total number of replicas that are executing simultaneously at any one time, the `--max-concurrent` flag can be used:

```console
$ docker service create \
    --name mythrottledjob \
    --mode replicated-job \
    --replicas 10 \
    --max-concurrent 2 \
    bash "true"
```

The above command will execute 10 Tasks in total, but only 2 of them will be run at any given time.

#### [Global Jobs](#global-jobs)

Global jobs are like global services, in that a Task is executed once on each node matching placement constraints. Global jobs are represented by the mode `global-job`.

Note that after a Global job is created, any new Nodes added to the cluster will have a Task from that job started on them. The Global Job does not as a whole have a "done" state, except insofar as every Node meeting the job's constraints has a Completed task.

----
url: https://docs.docker.com/ai/model-runner/get-started/
----

# Get started with DMR

***

Table of contents

***

Docker Model Runner (DMR) lets you run and manage AI models locally using Docker. This page shows you how to enable DMR, pull and run a model, configure model settings, and publish custom models.

## [Enable Docker Model Runner](#enable-docker-model-runner)

You can enable DMR using Docker Desktop or Docker Engine. Follow the instructions below based on your setup.

### [Docker Desktop](#docker-desktop)

1. In the settings view, go to the **AI** tab.

2. Select the **Enable Docker Model Runner** setting.

3. If you use Windows with a supported NVIDIA GPU, you also see and can select **Enable GPU-backed inference**.

4. Optional: To enable TCP support, select **Enable host-side TCP support**.

   1. In the **Port** field, type the port you want to use.
   2. If you interact with Model Runner from a local frontend web app, in **CORS Allows Origins**, select the origins that Model Runner should accept requests from. An origin is the URL where your web app runs, for example `http://localhost:3131`.

You can now use the `docker model` command in the CLI and view and interact with your local models in the **Models** tab in the Docker Desktop Dashboard.

### [Docker Engine](#docker-engine)

1. Ensure you have installed [Docker Engine](/engine/install/).

2. Docker Model Runner is available as a package. To install it, run:

   ```bash
   $ sudo apt-get update
   $ sudo apt-get install docker-model-plugin
   ```

   ```bash
   $ sudo dnf update
   $ sudo dnf install docker-model-plugin
   ```

3. Test the installation:

   ```bash
   $ docker model version
   $ docker model run ai/smollm2
   ```

> Note
>
> TCP support is enabled by default for Docker Engine on port `12434`.

### [Update DMR in Docker Engine](#update-dmr-in-docker-engine)

To update Docker Model Runner in Docker Engine, uninstall it with [`docker model uninstall-runner`](/reference/cli/docker/model/uninstall-runner/) then reinstall it:

```bash
docker model uninstall-runner --images && docker model install-runner
```

> Note
>
> With the above command, local models are preserved and only the Docker Model Runner images are removed. To also delete the local models during the upgrade, add the `--models` option to the `uninstall-runner` command.

## [Pull a model](#pull-a-model)

Models are cached locally.

> Note
>
> When you use the Docker CLI, you can also pull models directly from [HuggingFace](https://huggingface.co/).

1. Select **Models** and select the **Docker Hub** tab.
2. Find the model you want and select **Pull**.

Use the [`docker model pull` command](/reference/cli/docker/model/pull/). For example:

Pulling from Docker Hub

```bash
docker model pull ai/smollm2:360M-Q4_K_M
```

Pulling from HuggingFace

```bash
docker model pull hf.co/bartowski/Llama-3.2-1B-Instruct-GGUF
```

## [Run a model](#run-a-model)

1. Select **Models** and select the **Local** tab.
2. Select the play button. The interactive chat screen opens.

Use the [`docker model run` command](/reference/cli/docker/model/run/).

## [Configure a model](#configure-a-model)

You can configure a model, such as its maximum token limit and more, use Docker Compose. See [Models and Compose - Model configuration options](https://docs.docker.com/ai/compose/models-and-compose/#model-configuration-options).

## [Publish a model](#publish-a-model)

> Note
>
> This works for any Container Registry supporting OCI Artifacts, not only Docker Hub.

You can tag existing models with a new name and publish them under a different namespace and repository:

```bash
# Tag a pulled model under a new name
$ docker model tag ai/smollm2 myorg/smollm2

# Push it to Docker Hub
$ docker model push myorg/smollm2
```

For more details, see the [`docker model tag`](/reference/cli/docker/model/tag) and [`docker model push`](/reference/cli/docker/model/push) command documentation.

You can also package a model file in GGUF format as an OCI Artifact and publish it to Docker Hub.

```bash
# Download a model file in GGUF format, for example from HuggingFace
$ curl -L -o model.gguf https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf

# Package it as OCI Artifact and push it to Docker Hub
$ docker model package --gguf "$(pwd)/model.gguf" --push myorg/mistral-7b-v0.1:Q4_K_M
```

For more details, see the [`docker model package`](/reference/cli/docker/model/package/) command documentation.

## [Troubleshooting](#troubleshooting)

### [Display the logs](#display-the-logs)

To troubleshoot issues, display the logs:

Select **Models** and select the **Logs** tab.

Use the [`docker model logs` command](/reference/cli/docker/model/logs/).

### [Inspect requests and responses](#inspect-requests-and-responses)

Inspecting requests and responses helps you diagnose model-related issues. For example, you can evaluate context usage to verify you stay within the model's context window or display the full body of a request to control the parameters you are passing to your models when developing with a framework.

In Docker Desktop, to inspect the requests and responses for each model:

1. Select **Models** and select the **Requests** tab. This view displays all the requests to all models:

   * The time the request was sent.
   * The model name and version
   * The prompt/request
   * The context usage
   * The time it took for the response to be generated.

2. Select one of the requests to display further details:

   * In the **Overview** tab, view the token usage, response metadata and generation speed, and the actual prompt and response.
   * In the **Request** and **Response** tabs, view the full JSON payload of the request and the response.

> Note
>
> You can also display the requests for a specific model when you select a model and then select the **Requests** tab.

## [Related pages](#related-pages)

* [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - OpenAI and Ollama-compatible API documentation
* [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Context size and runtime parameters
* [Inference engines](https://docs.docker.com/ai/model-runner/inference-engines/) - llama.cpp and vLLM details
* [IDE integrations](https://docs.docker.com/ai/model-runner/ide-integrations/) - Connect Cline, Continue, Cursor, and more
* [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) - Set up a web chat interface
* [Models and Compose](https://docs.docker.com/ai/compose/models-and-compose/) - Use models in Compose applications
* [Docker Model Runner CLI reference](/reference/cli/docker/model) - Complete CLI documentation

----
url: https://docs.docker.com/admin/company/company-faqs/
----

# Company FAQs

***

Table of contents

***

### [Some of my organizations don’t have a Docker Business subscription. Can I still use a parent company?](#some-of-my-organizations-dont-have-a-docker-business-subscription-can-i-still-use-a-parent-company)

Yes, but you can only add organizations with a Docker Business subscription to a company.

### [What happens if one of my organizations downgrades from Docker Business, but I still need access as a company owner?](#what-happens-if-one-of-my-organizations-downgrades-from-docker-business-but-i-still-need-access-as-a-company-owner)

To access and manage child organizations, the organization must have a Docker Business subscription. If the organization isn’t included in this subscription, the owner of the organization must manage the organization outside of the company.

### [Do company owners occupy a subscription seat?](#do-company-owners-occupy-a-subscription-seat)

Company owners do not occupy a seat unless one of the following is true:

* They are added as a member of an organization under your company
* SSO is enabled and the company owner signs in via SSO, which automatically adds them as an organization member

Although company owners have the same access as organization owners across all organizations in the company, it's not necessary to add them to any organization. Doing so will cause them to occupy a seat.

When you first create a company, your account is both a company owner and an organization owner. In that case, your account will occupy a seat as long as you remain an organization owner.

To avoid occupying a seat, [assign another user as the organization owner](https://docs.docker.com/admin/organization/manage/members/#update-a-member-role) and remove yourself from the organization. You'll retain full administrative access as a company owner without using a subscription seat.

### [What permissions does the company owner have in the associated/nested organizations?](#what-permissions-does-the-company-owner-have-in-the-associatednested-organizations)

Company owners can navigate to the **Organizations** page to view all their nested organizations in a single location. They can also view or edit organization members and change single sign-on (SSO) and System for Cross-domain Identity Management (SCIM) settings. Changes to company settings impact all users in each organization under the company.

For more information, see [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

----
url: https://docs.docker.com/desktop/use-desktop/volumes/
----

# Explore the Volumes view in Docker Desktop

***

Table of contents

***

The **Volumes** view in Docker Desktop lets you create, inspect, delete, clone, empty, export, and import [Docker volumes](https://docs.docker.com/engine/storage/volumes/). You can also browse files and folders in volumes and see which containers are using them.

## [View your volumes](#view-your-volumes)

You can view the following information about your volumes:

* Name: The name of the volume.
* Status: Whether the volume is in-use by a container or not.
* Created: How long ago the volume was created.
* Size: The size of the volume.
* Scheduled exports: Whether a scheduled export is active or not.

By default, the **Volumes** view displays a list of all the volumes.

You can filter and sort volumes as well as modify which columns are displayed by doing the following:

* Filter volumes by name: Use the **Search** field.
* Filter volumes by status: To the right of the search bar, filter volumes by **In use** or **Unused**.
* Sort volumes: Select a column name to sort the volumes.
* Customize columns: To the right of the search bar, choose what volume information to display.

## [Create a volume](#create-a-volume)

You use the following steps to create an empty volume. Alternatively, if you [start a container with a volume](https://docs.docker.com/engine/storage/volumes/#start-a-container-with-a-volume) that doesn't yet exist, Docker creates the volume for you.

To create a volume:

1. In the **Volumes** view, select the **Create** button.
2. In the **New Volume** modal, specify a volume name, and then select **Create**.

To use the volume with a container, see [Use volumes](https://docs.docker.com/engine/storage/volumes/#start-a-container-with-a-volume).

## [Inspect a volume](#inspect-a-volume)

To explore the details of a specific volume, select a volume from the list. This opens the detailed view.

The **Container in-use** tab displays the name of the container using the volume, the image name, the port number used by the container, and the target. A target is a path inside a container that gives access to the files in the volume.

The **Stored data** tab displays the files and folders in the volume and the file size. To save a file or a folder, right-click on the file or folder to display the options menu, select **Save as...**, and then specify a location to download the file.

To delete a file or a folder from the volume, right-click on the file or folder to display the options menu, select **Delete**, and then select **Delete** again to confirm.

The **Exports** tab lets you [export the volume](#export-a-volume).

## [Clone a volume](#clone-a-volume)

Cloning a volume creates a new volume with a copy of all of the data from the cloned volume. When cloning a volume used by one or more running containers, the containers are temporarily stopped while Docker clones the data, and then restarted when the cloning process is completed.

To clone a volume:

1. Sign in to Docker Desktop. You must be signed in to clone a volume.
2. In the **Volumes** view, select the **Clone** icon in the **Actions** column for the volume you want to clone.
3. In the **Clone a volume** modal, specify a **Volume name**, and then select **Clone**.

## [Delete one or more volumes](#delete-one-or-more-volumes)

Deleting a volume deletes the volume and all its data. When a container is using a volume, you can't delete the volume, even if the container is stopped. You must first stop and remove any containers using the volume before you can delete the volume.

To delete a volume:

1. In the **Volumes** view, select **Delete** icon in the **Actions** column for the volume you want to delete.
2. In the **Delete volume?** modal, select **Delete forever**.

To delete multiple volumes:

1. In the **Volumes** view, select the checkbox next to all the volumes you want to delete.
2. Select **Delete**.
3. In the **Delete volumes?** modal, select **Delete forever**.

## [Empty a volume](#empty-a-volume)

Emptying a volume deletes all a volume's data, but doesn't delete the volume. When emptying a volume used by one or more running containers, the containers are temporarily stopped while Docker empties the data, and then restarted when the emptying process is completed.

To empty a volume:

1. Sign in to Docker Desktop. You must be signed in to empty a volume.
2. In the **Volumes** view, select the volume you want to empty.
3. Next to **Import**, select the **More volume actions** icon, and then select **Empty volume**.
4. In the **Empty a volume?** modal, select **Empty**.

## [Export a volume](#export-a-volume)

You can export the content of a volume to a local file, a local image, and to an image in Docker Hub, or to a supported cloud provider. When exporting content from a volume used by one or more running containers, the containers are temporarily stopped while Docker exports the content, and then restarted when the export process is completed.

You can either [export a volume now](#export-a-volume-now) or [schedule a recurring export](#schedule-a-volume-export).

### [Export a volume now](#export-a-volume-now)

1. Sign in to Docker Desktop. You must be signed in to export a volume.

2. In the **Volumes** view, select the volume you want to export.

3. Select the **Exports** tab.

4. Select **Quick export**.

5. Select whether to export the volume to **Local or Hub storage** or **External cloud storage**, then specify the following additional details depending on your selection.

   * **Local file**: Specify a file name and select a folder.
   * **Local image**: Select a local image to export the content to. Any existing data in the image will be replaced by the exported content.
   * **New image**: Specify a name for the new image.
   * **Registry**: Specify a Docker Hub repository.

   You must have a [Docker Business subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopVolumes) to export to an external cloud provider.

   Select your cloud provider and then specify the URL to upload to the storage. Refer to the following documentation for your cloud provider to learn how to obtain a URL.

   * Amazon Web Services: [Create a presigned URL of Amazon S3 using an AWS SDK](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   * Microsoft Azure: [Generate a SAS token and URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   * Google Cloud: [Create a signed URL to upload an object](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

6. Select **Save**.

### [Schedule a volume export](#schedule-a-volume-export)

1. Sign in to Docker Desktop. You must be signed in and have a paid [Docker subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopVolumes) to schedule a volume export.

2. In the **Volumes** view, select the volume you want to export.

3. Select the **Exports** tab.

4. Select **Schedule export**.

5. In **Recurrence**, select how often the export occurs, and then specify the following additional details based on your selection.

   * **Daily**: Specify the time that the backup occurs each day.
   * **Weekly**: Specify one or more days, and the time that the backup occurs each week.
   * **Monthly**: Specify which day of the month and the time that the backup occurs each month.

6. Select whether to export the volume to **Local or Hub storage** or **External cloud storage**, then specify the following additional details depending on your selection.

   * **Local file**: Specify a file name and select a folder.
   * **Local image**: Select a local image to export the content to. Any existing data in the image will be replaced by the exported content.
   * **New image**: Specify a name for the new image.
   * **Registry**: Specify a Docker Hub repository.

   You must have a [Docker Business subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopVolumes) to export to an external cloud provider.

   Select your cloud provider and then specify the URL to upload to the storage. Refer to the following documentation for your cloud provider to learn how to obtain a URL.

   * Amazon Web Services: [Create a presigned URL of Amazon S3 using an AWS SDK](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_Scenario_PresignedUrl_section.html)
   * Microsoft Azure: [Generate a SAS token and URL](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/api/connection-strings/generate-sas-token)
   * Google Cloud: [Create a signed URL to upload an object](https://cloud.google.com/storage/docs/access-control/signing-urls-with-helpers#upload-object)

7. Select **Save**.

## [Import a volume](#import-a-volume)

You can import a local file, a local image, or an image from Docker Hub. Any existing data in the volume is replaced by the imported content. When importing content to a volume used by one or more running containers, the containers are temporarily stopped while Docker imports the content, and then restarted when the import process is completed.

To import a volume:

1. Sign in to Docker Desktop. You must be signed in to import a volume.

2. Optionally, [create](#create-a-volume) a new volume to import the content into.

3. Select the volume you want to import content in to.

4. Select **Import**.

5. Select where the content is coming from and then specify the following additional details depending on your selection:

   * **Local file**: Select the file that contains the content.
   * **Local image**: Select the local image that contains the content.
   * **Registry**: Specify the image from Docker Hub that contains the content.

6. Select **Import**.

## [Additional resources](#additional-resources)

* [Persisting container data](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/)
* [Use volumes](https://docs.docker.com/engine/storage/volumes/)

----
url: https://docs.docker.com/reference/cli/docker/swarm/join-token/
----

# docker swarm join-token

***

| Description | Manage join tokens                                    |
| ----------- | ----------------------------------------------------- |
| Usage       | `docker swarm join-token [OPTIONS] (worker\|manager)` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Join tokens are secrets that allow a node to join the swarm. There are two different join tokens available, one for the worker role and one for the manager role. You pass the token using the `--token` flag when you run [swarm join](/reference/cli/docker/swarm/join/). Nodes use the join token only when they join the swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                  | Default | Description        |
| ----------------------- | ------- | ------------------ |
| [`-q, --quiet`](#quiet) |         | Only display token |
| [`--rotate`](#rotate)   |         | Rotate join token  |

## [Examples](#examples)

You can view or rotate the join tokens using `swarm join-token`.

As a convenience, you can pass `worker` or `manager` as an argument to `join-token` to print the full `docker swarm join` command to join a new node to the swarm:

```console
$ docker swarm join-token worker

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233... \
    172.17.0.2:2377

$ docker swarm join-token manager

To add a manager to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233... \
    172.17.0.2:2377
```

Use the `--rotate` flag to generate a new join token for the specified role:

```console
$ docker swarm join-token --rotate worker

Successfully rotated worker join token.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233... \
    172.17.0.2:2377
```

After using `--rotate`, only the new token will be valid for joining with the specified role.

The `-q` (or `--quiet`) flag only prints the token:

```console
$ docker swarm join-token -q worker

SWMTKN-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233...
```

### [`--rotate`](#rotate)

Because tokens allow new nodes to join the swarm, you should keep them secret. Be particularly careful with manager tokens since they allow new manager nodes to join the swarm. A rogue manager has the potential to disrupt the operation of your swarm.

Rotate your swarm's join token if a token gets checked-in to version control, stolen, or a node is compromised. You may also want to periodically rotate the token to ensure any unknown token leaks do not allow a rogue node to join the swarm.

To rotate the join token and print the newly generated token, run `docker swarm join-token --rotate` and pass the role: `manager` or `worker`.

Rotating a join-token means that no new nodes will be able to join the swarm using the old token. Rotation does not affect existing nodes in the swarm because the join token is only used for authorizing new nodes joining the swarm.

### [`--quiet`](#quiet)

Only print the token. Do not print a complete command for joining.

----
url: https://docs.docker.com/scout/release-notes/cli/
----

[Skip to content](#start-of-content)

You signed in with another tab or window. [Reload]() to refresh your session. You signed out in another tab or window. [Reload]() to refresh your session. You switched accounts on another tab or window. [Reload]() to refresh your session. Dismiss alert

[docker ](/docker)/ **[scout-cli](/docker/scout-cli)&#x20;**&#x50;ublic

* [Notifications ](/login?return_to=%2Fdocker%2Fscout-cli)You must be signed in to change notification settings
* [Fork 133](/login?return_to=%2Fdocker%2Fscout-cli)
* [Star 450](/login?return_to=%2Fdocker%2Fscout-cli)

# Releases: docker/scout-cli

Releases · docker/scout-cli

## v1.21.0

19 May 17:16

[docker-scout-ci](/apps/docker-scout-ci)

[v1.21.0](/docker/scout-cli/tree/v1.21.0)

[`0390daf`](/docker/scout-cli/commit/0390daf32edeaee9aca29829ac63aacde4e2ca9b)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.21.0](/docker/scout-cli/releases/tag/v1.21.0) [Latest](/docker/scout-cli/releases/latest)

[Latest](/docker/scout-cli/releases/latest)

## What's Changed

* Fix local DHI-derived image handling, including inherited VEX and quickview base-image display
* Improve SBOM package qualifier handling, including DHI distro qualifiers
* Update dependencies and Go toolchain

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.20.4

08 Apr 08:04

[docker-scout-ci](/apps/docker-scout-ci)

[v1.20.4](/docker/scout-cli/tree/v1.20.4)

[`0390daf`](/docker/scout-cli/commit/0390daf32edeaee9aca29829ac63aacde4e2ca9b)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.20.4](/docker/scout-cli/releases/tag/v1.20.4)

## What's Changed

* Add JSON output format for docker scout compare [@benja-M-1](https://github.com/benja-M-1)
* Add image config field changes to docker scout compare output [@benja-M-1](https://github.com/benja-M-1)
* Fix Docker Desktop proxy detection in WSL2 environments [@benja-M-1](https://github.com/benja-M-1)
* Update dependencies [@benja-M-1](https://github.com/benja-M-1)

### Contributors

* [](https://github.com/benja-M-1)

benja-M-1

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.20.3

20 Mar 12:06

[docker-scout-ci](/apps/docker-scout-ci)

[v1.20.3](/docker/scout-cli/tree/v1.20.3)

[`48f3372`](/docker/scout-cli/commit/48f3372dc714a91f8ec2635913d9b9ad1c299ada)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.20.3](/docker/scout-cli/releases/tag/v1.20.3)

## What's Changed

* Improve retries of temporary and network errors [@chrispatrick](https://github.com/chrispatrick)
* Fix handling of dockerfiles included in provenance attestations [@chrispatrick](https://github.com/chrispatrick)
* Fix handling of cosign sig tags [@chrispatrick](https://github.com/chrispatrick)
* Use Docker Desktop HTTP proxy transport when available [@benja-M-1](https://github.com/benja-M-1)

### Contributors

* [](https://github.com/benja-M-1)
* [](https://github.com/chrispatrick)

benja-M-1 and chrispatrick

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.20.2

09 Mar 17:44

[docker-scout-ci](/apps/docker-scout-ci)

[v1.20.2](/docker/scout-cli/tree/v1.20.2)

[`48f3372`](/docker/scout-cli/commit/48f3372dc714a91f8ec2635913d9b9ad1c299ada)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.20.2](/docker/scout-cli/releases/tag/v1.20.2)

## What's Changed

* Minor consistency fixes [@chrispatrick](https://github.com/chrispatrick)

### Contributors

* [](https://github.com/chrispatrick)

chrispatrick

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.20.1

06 Mar 10:41

[chrispatrick](/chrispatrick)

[v1.20.1](/docker/scout-cli/tree/v1.20.1)

[`48f3372`](/docker/scout-cli/commit/48f3372dc714a91f8ec2635913d9b9ad1c299ada)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.20.1](/docker/scout-cli/releases/tag/v1.20.1)

## What's Changed

* Fix VCS provenance parsing [@chrispatrick](https://github.com/chrispatrick)

### Contributors

* [](https://github.com/chrispatrick)

chrispatrick

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.20.0

24 Feb 12:24

[chrispatrick](/chrispatrick)

[v1.20.0](/docker/scout-cli/tree/v1.20.0)

[`83df7af`](/docker/scout-cli/commit/83df7afcb6afb06a9c0b13972172b1b63e8355c5)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.20.0](/docker/scout-cli/releases/tag/v1.20.0)

## What's Changed

* Documentation updates [@dvdksn](https://github.com/dvdksn)
* Fix vulnerabilities [@jpbriend](https://github.com/jpbriend)
* Fix apk version handling [@cdupuis](https://github.com/cdupuis)
* Support SLSA v1 Provenance [@chrispatrick](https://github.com/chrispatrick)
* Update dependencies [@cdupuis](https://github.com/cdupuis)
* Fix Go purl versioning [@cdupuis](https://github.com/cdupuis)

### Contributors

* [](https://github.com/cdupuis)
* [](https://github.com/jpbriend)
* [](https://github.com/chrispatrick)
* [](https://github.com/dvdksn)

cdupuis, jpbriend, and 2 other contributors

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.19.0

16 Dec 08:37

[chrispatrick](/chrispatrick)

[v1.19.0](/docker/scout-cli/tree/v1.19.0)

[`ae73b6e`](/docker/scout-cli/commit/ae73b6ea46d74261e26f3b9cf8b5375fb5d05951)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.19.0](/docker/scout-cli/releases/tag/v1.19.0)

# What's Changed

* CVE fixes [@cdupuis](https://github.com/cdupuis)
* Update dependencies [@cdupuis](https://github.com/cdupuis)
* Documentation updates [@craig-osterhout](https://github.com/craig-osterhout)
* Handle attestation source failures more gracefully [@chrispatrick](https://github.com/chrispatrick)
* Bug fixes including around VEX, versioning and indexing [@cdupuis](https://github.com/cdupuis)

### Contributors

* [](https://github.com/cdupuis)
* [](https://github.com/chrispatrick)
* [](https://github.com/craig-osterhout)

cdupuis, chrispatrick, and craig-osterhout

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.18.4

02 Oct 16:23

[chrispatrick](/chrispatrick)

[v1.18.4](/docker/scout-cli/tree/v1.18.4)

[`fc529c7`](/docker/scout-cli/commit/fc529c7bfb840839af93a4bec124be599e7a4901)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.18.4](/docker/scout-cli/releases/tag/v1.18.4)

## What's Changed

* Docs updates [@craig-osterhout](https://github.com/craig-osterhout)
* VEX and SPDX fixes [@cdupuis](https://github.com/cdupuis)

### Contributors

* [](https://github.com/cdupuis)
* [](https://github.com/craig-osterhout)

cdupuis and craig-osterhout

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.18.3

13 Aug 15:12

[cdupuis](/cdupuis)

[v1.18.3](/docker/scout-cli/tree/v1.18.3)

[`ff58efb`](/docker/scout-cli/commit/ff58efb9d2d249bdba20f241a6b25c94665bda97)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.18.3](/docker/scout-cli/releases/tag/v1.18.3)

## What's Changed

* Minor fixes for DHI by [@cdupuis](https://github.com/cdupuis)
* Add `docker scout vex get` command to a get merged VEX document from all VEX attestations [@cdupuis](https://github.com/cdupuis)

### Contributors

* [](https://github.com/cdupuis)

cdupuis

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v1.18.2

21 Jul 14:31

[cdupuis](/cdupuis)

[v1.18.2](/docker/scout-cli/tree/v1.18.2)

[`ff58efb`](/docker/scout-cli/commit/ff58efb9d2d249bdba20f241a6b25c94665bda97)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v1.18.2](/docker/scout-cli/releases/tag/v1.18.2)

## What's Changed

* Minor fixes for DHI by [@cdupuis](https://github.com/cdupuis)
* Add `--skip-tlog` for `docker scout attest get` to skip signature verification against the transparency log by [@cdupuis](https://github.com/cdupuis)
* Do not filter CVEs that are marked with a VEX `under_investigation` statement by [@cdupuis](https://github.com/cdupuis)
* Add predicate type human names for DHI FIPS and STIG attestations by [@cdupuis](https://github.com/cdupuis)

### Contributors

* [](https://github.com/cdupuis)

cdupuis

Assets 9

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

You can’t perform that action at this time.

----
url: https://docs.docker.com/admin/organization/setup/orgs/
----

# Create your organization

***

Table of contents

***

Subscription: Team Business

For: Administrators

There are multiple ways to create an organization. You can either:

* Create a new organization using the **Create Organization** option in the Admin Console or Docker Hub
* Convert an existing user account to an organization

These procedures walk you through creating an organization from the Admin Console.

## [Prerequisites](#prerequisites)

* Before you create an organization, you need a [Docker ID](https://docs.docker.com/accounts/create-account/).
* For prerequisites and detailed instructions on converting an existing user account to an organization, see [Convert an account into an organization](https://docs.docker.com/admin/organization/setup/convert-account/).

> Tip
>
> Need a different plan for your team's needs? Review different [Docker subscriptions and features](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdminOrgs) to choose a subscription for your organization.

## [Create an organization](#create-an-organization)

1. Sign in to [Docker Home](https://app.docker.com/) and navigate to the bottom of the organization list. Select **Create new organization**.

2. Choose a subscription for your organization, a billing cycle, and specify how many seats you need. See [Docker Pricing](https://www.docker.com/pricing?ref=Docs\&refAction=DocsAdminOrgs) for details on the features offered in the Team and Business subscription.

3. Select **Continue to profile**, then **Create an organization** to create a new organization.

4. Enter an **Organization namespace**. This is the official, unique name for your organization in Docker Hub.

   * It's not possible to change the name of the organization after you've created it.
   * Your Docker ID and organization can't share the same name.
   * If you want to use your Docker ID as the organization name, then you must first [convert your account into an organization](https://docs.docker.com/admin/organization/setup/convert-account/).

5. Enter your **Company name**. This is the full name of your company.

   * Docker displays the company name on your organization page and in the details of any public images you publish.
   * You can update the company name anytime by navigating to your organization's **Settings** page.

6. Select **Continue to billing** to continue, then enter your organization's billing information. Select **Continue to payment** to continue to the billing portal.

7. Provide your payment details and select **Purchase**.

You've now created an organization.

## [View an organization](#view-an-organization)

To view an organization in the Admin Console:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization.
2. From the left-hand navigation menu, select **Admin Console**.

The Admin Console contains many options that let you to configure your organization.

## [Merge organizations](#merge-organizations)

> Warning
>
> If you are merging organizations, it is recommended to do so at the *end* of your billing cycle. When you merge an organization and downgrade another, you will lose seats on your downgraded organization. Docker does not offer refunds for downgrades.

If you have multiple organizations that you want to merge into one, complete the following steps:

1. Based on the number of seats from the secondary organization, [purchase additional seats](https://docs.docker.com/admin/organization/manage/manage-seats/) for the primary organization account that you want to keep.
2. Manually add users to the primary organization and remove existing users from the secondary organization.
3. Manually move over your data, including all repositories.
4. Once you're done moving all of your users and data, [downgrade](https://docs.docker.com/subscription/change/) the secondary account to a free subscription. Note that Docker does not offer refunds for downgrading organizations mid-billing cycle.

If your organization has a Docker Business subscription with a purchase order, contact Support or your Account Manager at Docker.

## [More resources](#more-resources)

* [Video: Docker Hub Organizations](https://www.youtube.com/watch?v=WKlT1O-4Du8)

----
url: https://docs.docker.com/reference/cli/sbx/policy/rm/network/
----

# sbx policy rm network

| Description | Remove a network rule                               |
| ----------- | --------------------------------------------------- |
| Usage       | `sbx policy rm network [--sandbox SANDBOX] [flags]` |

## [Description](#description)

Remove a network rule by rule ID, resource, or both.

The rule is removed from the global policy by default. Use --sandbox to remove from policy "local" scoped to a single sandbox instead.

Use "sbx policy ls" to see active policies and their IDs/resources.

## [Options](#options)

| Option       | Default | Description                                                      |
| ------------ | ------- | ---------------------------------------------------------------- |
| `--id`       |         | Remove by rule ID                                                |
| `--resource` |         | Remove by resource value(s), comma-separated                     |
| `--sandbox`  |         | Scope the removal to a specific sandbox (default: global policy) |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# List policies to find the ID or resource to remove
sbx policy ls

# Remove a global rule by resource
sbx policy rm network --resource api.example.com

# Remove a global rule by ID
sbx policy rm network --id 2d3c1f0e-4a73-4e05-bc9d-f2f9a4b50d67

# Remove a sandbox-scoped rule by resource
sbx policy rm network --sandbox my-sandbox --resource api.example.com
```

----
url: https://docs.docker.com/reference/cli/sbx/login/
----

# sbx login

| Description | Sign in to Docker   |
| ----------- | ------------------- |
| Usage       | `sbx login [flags]` |

## [Options](#options)

| Option             | Default | Description                               |
| ------------------ | ------- | ----------------------------------------- |
| `--password-stdin` |         | Read password or access token from stdin  |
| `--username`       |         | Docker username for non-interactive login |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/dhi/troubleshoot/
----

# Troubleshoot

***

Table of contents

***

This page covers debugging techniques and common issues you may encounter while migrating to or using Docker Hardened Images (DHIs).

## [General debugging](#general-debugging)

Docker Hardened Images prioritize minimalism and security, which means they intentionally leave out many common debugging tools (like shells or package managers). This makes direct troubleshooting difficult without introducing risk. To address this, you can use [Docker Debug](/reference/cli/docker/debug/), a secure workflow that temporarily attaches an ephemeral debug container to a running service or image without modifying the original image.

This section shows how to debug Docker Hardened Images locally during development. With Docker Debug, you can also debug containers remotely using the `--host` option.

### [Use Docker Debug](#use-docker-debug)

#### [Step 1: Run a container from a Hardened Image](#step-1-run-a-container-from-a-hardened-image)

Start with a DHI-based container that simulates an issue:

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

This container doesn't include a shell or tools like `ps`, `top`, or `cat`.

If you try:

```console
$ docker exec -it myapp sh
```

You'll see:

```console
exec: "sh": executable file not found in $PATH
```

#### [Step 2: Use Docker Debug to inspect the container](#step-2-use-docker-debug-to-inspect-the-container)

Use the `docker debug` command to attach a temporary, tool-rich debug container to the running instance.

```console
$ docker debug myapp
```

From here, you can inspect running processes, network status, or mounted files.

For example, to check running processes:

```console
$ ps aux
```

Type `exit` to leave the container when done.

### [Alternative debugging approaches](#alternative-debugging-approaches)

In addition to using Docker Debug, you can also use the following approaches for debugging DHI containers.

#### [Use the -dev variant](#use-the--dev-variant)

Docker Hardened Images offer a `-dev` variant that includes a shell and a package manager to install debugging tools. Simply replace the image tag with `-dev`:

```console
$ docker run -it --rm dhi.io/python:3.13-dev sh
```

Type `exit` to leave the container when done. Note that using the `-dev` variant increases the attack surface and it is not recommended as a runtime for production environments.

#### [Mount debugging tools with image mounts](#mount-debugging-tools-with-image-mounts)

You can use the image mount feature to mount debugging tools into your container without modifying the base image.

##### [Step 1: Run a container from a hardened image](#step-1-run-a-container-from-a-hardened-image-1)

Start with a DHI-based container that simulates an issue:

```console
$ docker run -d --name myapp dhi.io/python:3.13 python -c "import time; time.sleep(300)"
```

##### [Step 2: Mount debugging tools into the container](#step-2-mount-debugging-tools-into-the-container)

Run a new container that mounts a tool-rich image (like `busybox`) into the running container's namespace:

```console
$ docker run --rm -it --pid container:myapp \
  --mount type=image,source=busybox,destination=/dbg,ro \
  dhi.io/python:3.13 /dbg/bin/sh
```

This mounts the BusyBox image at `/dbg`, giving you access to its tools while keeping your original container image unchanged. Since the hardened Python image doesn't include standard utilities, you need to use the full path to the mounted tools:

```console
$ /dbg/bin/ls /
$ /dbg/bin/ps aux
$ /dbg/bin/cat /etc/os-release
```

Type `exit` to leave the container when done.

## [Common issues](#common-issues)

The following are specific issues you may encounter when working with Docker Hardened Images, along with recommended solutions.

### [Permissions](#permissions)

DHIs run as a nonroot user by default for enhanced security. This can result in permission issues when accessing files or directories. Ensure your application files and runtime directories are owned by the expected UID/GID or have appropriate permissions.

To find out which user a DHI runs as, check the repository page for the image on Docker Hub. See [View image variant details](https://docs.docker.com/dhi/how-to/explore/#image-variant-details) for more information.

### [Privileged ports](#privileged-ports)

Nonroot containers cannot bind to ports below 1024 by default. This is enforced by both the container runtime and the kernel (especially in Kubernetes and Docker Engine < 20.10).

Inside the container, configure your application to listen on an unprivileged port (1025 or higher). For example `docker run -p 80:8080 my-image` maps port 8080 in the container to port 80 on the host, allowing you to access it without needing root privileges.

### [No shell](#no-shell)

Runtime DHIs omit interactive shells like `sh` or `bash`. If your build or tooling assumes a shell is present (e.g., for `RUN` instructions), use a `dev` variant of the image in an earlier build stage and copy the final artifact into the runtime image.

To find out which shell, if any, a DHI has, check the repository page for the image on Docker Hub. See [View image variant details](https://docs.docker.com/dhi/how-to/explore/#image-variant-details) for more information.

Also, use Docker Debug when you need shell access to a running container. For more details, see [General debugging](#general-debugging).

### [Entry point differences](#entry-point-differences)

DHIs may define different entry points compared to Docker Official Images (DOIs) or other community images.

To find out the ENTRYPOINT or CMD for a DHI, check the repository page for the image on Docker Hub. See [View image variant details](https://docs.docker.com/dhi/how-to/explore/#image-variant-details) for more information.

### [No package manager](#no-package-manager)

Runtime Docker Hardened Images are stripped down for security and minimal attack surface. As a result, they don't include a package manager such as `apk` or `apt`. This means you can't install additional software directly in the runtime image.

If your build or application setup requires installing packages (for example, to compile code, install runtime dependencies, or add diagnostic tools), use a `dev` variant of the image in a build stage. Then, copy only the necessary artifacts into the final runtime image.

----
url: https://docs.docker.com/desktop/use-desktop/logs/
----

# Explore the Logs view in Docker Desktop

***

Table of contents

***

Requires: Docker Desktop [4.65](https://docs.docker.com/desktop/release-notes/#4650) or later

The **Logs** view provides a unified, real-time log stream from all containers and recent builds in Docker Desktop. Unlike the logs accessible from the [**Containers** view](https://docs.docker.com/desktop/use-desktop/container/), the **Logs** view lets you monitor and search log output (up to a maximum of 100 000 entries) across your entire environment from a single interface.

## [Log entries](#log-entries)

Each log entry in the table view shows:

| Column        | Description                                                                    |
| ------------- | ------------------------------------------------------------------------------ |
| **Timestamp** | The date and time the log line was emitted, for example `2026-02-26 11:18:53`. |
| **Object**    | The container or build that produced the log line.                             |
| **Message**   | The full log message, including any status codes such as `[ OK ]`.             |

Selecting the expand arrow to the right of a row reveals the full message for that entry.

## [Search, filter, and export logs](#search-filter-and-export-logs)

Use the **Search** field at the top of the Logs view to find specific entries. The search bar supports:

* Plain-text terms for exact match searches
* Regular expressions (for example, `/error|warn/`)

You can save your search terms for easy-access later.

To refine the log stream further, select the **Filter** icon in the toolbar to open the container filter panel. From here you can:

* Check individual containers to show only their output
* Check Compose stacks to show or hide entire groups
* Use **Select all** or **Clear all** to quickly toggle every container at once

Use the **Export** button in the top-right corner (available with Docker Desktop version 4.77 and later) to export all logs or only the logs that match your filters.

## [Display settings](#display-settings)

Select the **Display settings** icon in the toolbar to toggle the following:

* **View build logs**: Include or exclude build-related log output in the stream
* **Wrap lines**
* **Show timestamps**

## [Feedback](#feedback)

Select **Give feedback** at the top of the view to share suggestions or report issues.

----
url: https://docs.docker.com/reference/cli/docker/dhi/attestation/get/
----

# docker dhi attestation get

***

| Description | Get attestation for a Docker Hardened Image   |
| ----------- | --------------------------------------------- |
| Usage       | `docker dhi attestation get <image> <digest>` |

## [Description](#description)

Get an attestation attached to a Docker Hardened Image.

Returns the in-toto statement extracted from the attestation referrer. The referrer digest must be provided to select which attestation to retrieve. Use 'docker dhi attestation list' to discover available attestation digests.

The image can be specified as:

* name:tag (e.g., nginx:1.27)
* namespace/name:tag (e.g., dhi/nginx:1.27)
* name\@sha256:digest (e.g., nginx\@sha256:abc123...)

Examples:

# [Get attestation by referrer digest](#get-attestation-by-referrer-digest)

docker dhi attestation get dhi/nginx:1.27 sha256:abc123...

# [Save attestation to a file](#save-attestation-to-a-file)

docker dhi attestation get dhi/nginx:1.27 sha256:abc123... -o provenance.json

# [Extract only the predicate using jq](#extract-only-the-predicate-using-jq)

docker dhi attestation get dhi/nginx:1.27 sha256:abc123... | jq .predicate

## [Options](#options)

| Option         | Default | Description                            |
| -------------- | ------- | -------------------------------------- |
| `-o, --output` |         | Write output to file instead of stdout |

----
url: https://docs.docker.com/reference/samples/vuejs/
----

# Vue.js samples

| Name                                                                 | Description                  |
| -------------------------------------------------------------------- | ---------------------------- |
| [VueJS](https://github.com/docker/awesome-compose/tree/master/vuejs) | A sample Vue.js application. |

----
url: https://docs.docker.com/guides/testcontainers-cloud/why/
----

# Why Testcontainers Cloud?

***

***

Testcontainers Cloud is a powerful cloud-based solution designed to optimize integration testing with Testcontainers by offloading container management to the cloud. It helps developers and teams overcome the limitations of traditional local and CI-based testing, ensuring consistent environments, faster test execution, and scalable workflows. Whether you're new to Testcontainers or looking to enhance your existing setup, Testcontainers Cloud offers a seamless way to manage containerized tests, improving efficiency and reliability in your development pipeline.

Testcontainers Cloud provides several benefits:

* **Offloading to the Cloud:** Frees up local resources by shifting container management to the cloud, keeping your laptop responsive.
* **Consistent Testing Environments:** Ensures that tests run in isolated, reliable environments, reducing inconsistencies across platforms from Dev to CI.
* **Scalability:** Allows running large numbers of containers simultaneously without being limited by local or CI resources.
* **Faster CI/CD Pipelines:** Reduces configuration bottlenecks and speeds up build times by offloading containers to multiple on-demand cloud workers with the Turbo-mode feature.

Testcontainers Cloud streamlines integration testing by offloading container management to the cloud, ensuring consistent environments and faster test execution resulting in reduced resource strain, making it an essential tool for improving the stability of your Testcontainers-based workflows.

[Setting up Testcontainers Cloud by Docker »](https://docs.docker.com/guides/testcontainers-cloud/demo-local/)

----
url: https://docs.docker.com/guides/postgresql/networking-and-connectivity/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Networking and connectivity

***

Table of contents

***

This guide covers two common ways to connect to PostgreSQL running in Docker:

* Container-to-container: Connect from your application container to PostgreSQL over a private Docker network. No ports need to be exposed to the host.
* Host-to-container: Connect from your laptop or development machine using `localhost` and a published port.

Prerequisite: This guide assumes you have PostgreSQL running with persistent storage. If you don't, follow the [Immediate Setup & Data Persistence](/guides/postgresql/immediate-setup-and-data-persistence/) guide first.

## [Internal network access (container-to-container)](#internal-network-access-container-to-container)

When your application runs in another container, connecting to PostgreSQL through a user-defined bridge network is the recommended approach. This setup provides automatic DNS resolution, so your application can connect to PostgreSQL using the container name as the hostname, without needing to track IP addresses.

> Note
>
> Why not use the default bridge network? While containers on the default bridge network can communicate, they can only do so by IP address. Since container IP addresses change when containers restart, this would require updating your PostgreSQL connection strings each time. User-defined bridge networks solve this by providing automatic DNS resolution, ensuring your PostgreSQL connection strings remain stable even if containers restart and receive new IP addresses.

Here's a quick comparison:

> Note
>
> The following examples show the difference in approach. To actually test this, follow the steps in this guide to set up containers on the appropriate networks first.

With the default bridge network, you'd need to find the IP address first:

```bash
# Get the container's IP address (changes on restart)
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres-dev
# Output: 172.17.0.2

# Then connect using that IP address from another container
# (No --network flag needed - containers default to bridge network)
docker run --rm -it \
  -e PGPASSWORD=mysecretpassword \
  postgres:18 \
  psql -h 172.17.0.2 -U postgres
```

With a user-defined network, you simply use the container name:

```bash
# Container name works directly - no IP lookup needed
docker run --rm -it \
  --network my-app-net \
  -e PGPASSWORD=mysecretpassword \
  postgres:18 \
  psql -h postgres-dev -U postgres
```

### [Step 1: Create a user-defined network](#step-1-create-a-user-defined-network)

```bash
docker network create my-app-net

# Example Output
ab7f984be43a0ca15534a9ee568716ddbe869a5875077fad3ef3192e3af7d288

docker network ls
# Output
ab7f984be43a   my-app-net    bridge    local
```

### [Step 2: Run PostgreSQL on that network (no port publishing)](#step-2-run-postgresql-on-that-network-no-port-publishing)

Notice there is no `-p 5432:5432` here. This keeps PostgreSQL internal to Docker and not accessible from the host machine, which is more secure for production environments.

```bash
docker run -d --name postgres-dev \
  --network my-app-net \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -v postgres_data:/var/lib/postgresql \
  postgres:18

  # Output
CONTAINER ID  IMAGE        COMMAND                 CREATED         STATUS        PORTS     NAMES
6d351ed89efc  postgres:18  "docker-entrypoint.s…"  9 seconds ago   Up 8 seconds  5432/tcp  postgres-dev
```

### [Step 3: Connect from another container using the Postgres container name](#step-3-connect-from-another-container-using-the-postgres-container-name)

You can test connectivity with a temporary `psql` client container:

```bash
docker run --rm -it \
  --network my-app-net \
  -e PGPASSWORD=mysecretpassword \
  postgres:18 \
  psql -h postgres-dev -U postgres
```

Key point: `-h postgres-dev` works because Docker DNS resolves the container name on a user-defined network. The container name acts as the hostname.

### [Connection string examples](#connection-string-examples)

When connecting from your application container, use these PostgreSQL connection strings:

* PostgreSQL URI format: This is the standard PostgreSQL connection URI format that combines all connection parameters into a single string, widely supported by PostgreSQL clients and libraries.

  ```bash
  postgresql://postgres:mysecretpassword@postgres-dev:5432/postgres
  ```

  This command demonstrates passing a PostgreSQL URI connection string as an environment variable to a container, which your application can then read to connect to the database.

  Example usage in a Docker run command:

  ```bash
  docker run --rm -it \
    --network my-app-net \
    -e DATABASE_URL="postgresql://postgres:mysecretpassword@postgres-dev:5432/postgres" \
    alpine:latest \
    sh -c 'echo "DATABASE_URL is set to: $DATABASE_URL"'
  ```

* PostgreSQL connection parameters: This format uses key-value pairs separated by spaces, which many PostgreSQL client libraries accept as an alternative to URI format.

  ```bash
  host=postgres-dev
  port=5432
  user=postgres
  password=mysecretpassword
  dbname=postgres
  ```

  Example usage in application code (Python with psycopg2):

  ```python
  conn = psycopg2.connect(
      host="postgres-dev",
      port=5432,
      user="postgres",
      password="mysecretpassword",
      dbname="postgres"
  )
  ```

* Connecting to a specific database: Replace the database name in the connection string to connect to a specific database instead of the default `postgres` database. If you created a custom database (e.g., `testdb`), use:

  ```bash
  postgresql://postgres:mysecretpassword@postgres-dev:5432/testdb
  ```

  Example with SSL disabled (common in Docker networks): Add `?sslmode=disable` to the connection string when connecting within a private Docker network where SSL encryption isn't required.

  ```bash
  postgresql://postgres:mysecretpassword@postgres-dev:5432/testdb?sslmode=disable
  ```

> Note
>
> The default port `5432` is used in these examples. If you're connecting to a different PostgreSQL instance or have changed the port, update the connection string accordingly. The container name (`postgres-dev`) is resolved by Docker DNS to the container's IP address on the network.

## [Connecting from the host (external access)](#connecting-from-the-host-external-access)

To connect to PostgreSQL from your host machine using tools like `psql`, `pgAdmin`, `DBeaver`, or database management scripts, you need to publish PostgreSQL's port (`5432`) to the host. This allows external tools to reach the PostgreSQL container.

### [Expose Postgres to localhost only (recommended for development)](#expose-postgres-to-localhost-only-recommended-for-development)

This binds to `127.0.0.1` so it's only reachable from your local machine, not from other devices on your network. This is the most secure option for development.

```bash
docker run -d --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 127.0.0.1:5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  postgres:18
```

Now connect from your host:

* Host: `localhost` or `127.0.0.1`
* Port: `5432`

If you have `psql` installed on your host:

```bash
psql -h localhost -p 5432 -U postgres
```

You'll be prompted for the password. Alternatively, you can use the `PGPASSWORD` environment variable:

```bash
PGPASSWORD=mysecretpassword psql -h localhost -p 5432 -U postgres
```

### [Connecting with PostgreSQL GUI tools](#connecting-with-postgresql-gui-tools)

Popular PostgreSQL GUI tools can connect using these common connection details: Host: `localhost`, Port: `5432`, User: `postgres`, Database: `postgres` (or your database name).

* pgAdmin: A web-based PostgreSQL administration and development platform
* DBeaver: A universal database tool that supports PostgreSQL and many other databases. Select PostgreSQL as the connection type
* TablePlus: A modern, native database management tool for macOS and Windows with a clean interface

All tools will prompt for the password you set with `POSTGRES_PASSWORD`.

### [Expose Postgres to all network interfaces (use with caution)](#expose-postgres-to-all-network-interfaces-use-with-caution)

To allow connections from other devices on your network, use `-p 5432:5432` instead of `-p 127.0.0.1:5432:5432`. This binds PostgreSQL to all network interfaces on your host, making it accessible from any device that can reach your host, not just localhost.

```bash
docker run -d --name postgres-dev \
  -e POSTGRES_PASSWORD=mysecretpassword \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql \
  postgres:18
```

> Warning
>
> Exposing PostgreSQL to all network interfaces (`0.0.0.0:5432`) makes it accessible from any device that can reach your host. Only use this in trusted network environments or behind a firewall. For production, consider using a reverse proxy or VPN instead.

### [PostgreSQL security considerations for external access](#postgresql-security-considerations-for-external-access)

When exposing PostgreSQL to external access, follow these PostgreSQL-specific security practices:

* Avoid using the `postgres` superuser: The default `postgres` user has full database privileges. Create dedicated users with only the permissions your application needs.
* Use strong passwords: PostgreSQL passwords should be complex. Consider using environment variables or secrets management instead of `hardcoding` passwords.
* Limit network exposure: Binding to `127.0.0.1` (localhost only) is safer than exposing to all interfaces (`0.0.0.0`).
* Consider SSL/TLS: For production, configure PostgreSQL to require SSL connections. The [Advanced Configuration and Initialization](/guides/postgresql/advanced-configuration-and-initialization/) guide shows how to configure PostgreSQL settings.
* Create application-specific users: Use initialization scripts to create users with limited privileges. For example, a read-only user for reporting or a user that can only access specific databases.

The [Advanced configuration and initialization](/guides/postgresql/advanced-configuration-and-initialization/) guide shows how to use initialization scripts to create users and roles automatically.

## [Using Docker Compose for networking](#using-docker-compose-for-networking)

Docker Compose automatically creates a network for your services, making networking configuration simpler. Here's an example that combines both internal and external access:

```yaml
services:
  db:
    image: postgres:18
    container_name: postgres-dev
    environment:
      POSTGRES_PASSWORD: mysecretpassword
    volumes:
      - postgres_data:/var/lib/postgresql
    ports:
      - "127.0.0.1:5432:5432"  # Expose to localhost only
    networks:
      - app-network

  app:
    build: ./my-app
    environment:
      DATABASE_URL: postgresql://postgres:mysecretpassword@db:5432/mydb
    networks:
      - app-network
    depends_on:
      - db

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

In this PostgreSQL-focused setup:

* The `app` service connects to PostgreSQL using the service name (`db`) as the hostname in the connection string
* PostgreSQL is accessible from your host at `localhost:5432` for external tools
* Both services are isolated on a custom network, providing network-level security
* The `depends_on` directive ensures PostgreSQL starts before your application

PostgreSQL connection details for the app service:

* Hostname: `db` (resolved by Docker DNS)
* Port: `5432` (PostgreSQL default port)
* Database: `mydb` (as specified in the connection string)
* User: `postgres` (or a custom user you've created)

> Note
>
> Docker Compose automatically creates a network for your project. Services can reach each other by service name without explicit network configuration, but defining a custom network gives you more control. For PostgreSQL, this means your application can always connect using the service name, regardless of container restarts or IP changes.

## [Troubleshooting](#troubleshooting)

This section covers common PostgreSQL connection issues and their solutions when working with Docker networking.

### ["Could not translate host name postgres-dev"](#could-not-translate-host-name-postgres-dev)

* Both containers must be on the same Docker network (`my-app-net`).
* Verify the network exists: `docker network ls`
* Check which network a container is on: `docker inspect postgres-dev | grep NetworkMode`
* Ensure you're using a user-defined network, not the default bridge network

### ["Connection refused" or "could not connect to server"](#connection-refused-or-could-not-connect-to-server)

* PostgreSQL may still be initializing: PostgreSQL takes a few seconds to start and initialize the database cluster. Wait 5-10 seconds after container start and retry.

* Check if the PostgreSQL container is running:

  ```bash
  docker ps --filter name=postgres-dev
  ```

* Check PostgreSQL logs for initialization or connection errors:

  ```bash
  docker logs postgres-dev
  ```

  Look for messages like "database system is ready to accept connections" to confirm PostgreSQL is fully started.

* Verify the port mapping is correct:

  ```bash
  docker port postgres-dev
  ```

  This should show `5432/tcp -> 127.0.0.1:5432` (or `0.0.0.0:5432` if bound to all interfaces).

* Test PostgreSQL connectivity from inside the container:

  ```bash
  docker exec -it postgres-dev psql -U postgres -c "SELECT version();"
  ```

  If this works but external connections fail, the issue is with port publishing, not PostgreSQL itself.

### ["Password authentication failed" or "FATAL: password authentication failed for user"](#password-authentication-failed-or-fatal-password-authentication-failed-for-user)

* Confirm the password: Verify you're using the same password set in `POSTGRES_PASSWORD` when you started the container.

* Existing volume with old credentials: If you reused an existing volume, the password from the original initialization is still in effect. The `POSTGRES_PASSWORD` environment variable only sets the password during the first database initialization. To reset:

  * Remove the volume: `docker volume rm postgres_data`
  * Or connect with the old password
  * Or change the password after connecting: `ALTER USER postgres WITH PASSWORD 'newpassword';`

* Try connecting with password prompt: `psql -h localhost -U postgres -W` (the `-W` flag forces a password prompt)

* Use PGPASSWORD environment variable: `PGPASSWORD=mysecretpassword psql -h localhost -U postgres`

* Check PostgreSQL authentication configuration: If you've customized `pg_hba.conf`, verify the authentication method allows password authentication

### ["Network not found"](#network-not-found)

* Ensure the network exists before starting containers: `docker network create my-app-net`
* If using Docker Compose, the network is created automatically when you run `docker compose up`

[Companions for PostgreSQL »](https://docs.docker.com/guides/postgresql/companions-for-postgresql/)

----
url: https://docs.docker.com/engine/security/
----

# Docker Engine security

***

Table of contents

***

There are four major areas to consider when reviewing Docker security:

* The intrinsic security of the kernel and its support for namespaces and cgroups
* The attack surface of the Docker daemon itself
* Loopholes in the container configuration profile, either by default, or when customized by users.
* The "hardening" security features of the kernel and how they interact with containers.

## [Kernel namespaces](#kernel-namespaces)

Docker containers are very similar to LXC containers, and they have similar security features. When you start a container with `docker run`, behind the scenes Docker creates a set of namespaces and control groups for the container.

Namespaces provide the first and most straightforward form of isolation. Processes running within a container cannot see, and even less affect, processes running in another container, or in the host system.

Each container also gets its own network stack, meaning that a container doesn't get privileged access to the sockets or interfaces of another container. Of course, if the host system is setup accordingly, containers can interact with each other through their respective network interfaces — just like they can interact with external hosts. When you specify public ports for your containers or use [links](https://docs.docker.com/engine/network/links/) then IP traffic is allowed between containers. They can ping each other, send/receive UDP packets, and establish TCP connections, but that can be restricted if necessary. From a network architecture point of view, all containers on a given Docker host are sitting on bridge interfaces. This means that they are just like physical machines connected through a common Ethernet switch; no more, no less.

How mature is the code providing kernel namespaces and private networking? Kernel namespaces were introduced [between kernel version 2.6.15 and 2.6.26](https://man7.org/linux/man-pages/man7/namespaces.7.html). This means that since July 2008 (date of the 2.6.26 release ), namespace code has been exercised and scrutinized on a large number of production systems. And there is more: the design and inspiration for the namespaces code are even older. Namespaces are actually an effort to reimplement the features of [OpenVZ](https://en.wikipedia.org/wiki/OpenVZ) in such a way that they could be merged within the mainstream kernel. And OpenVZ was initially released in 2005, so both the design and the implementation are pretty mature.

## [Control groups](#control-groups)

Control Groups are another key component of Linux containers. They implement resource accounting and limiting. They provide many useful metrics, but they also help ensure that each container gets its fair share of memory, CPU, disk I/O; and, more importantly, that a single container cannot bring the system down by exhausting one of those resources.

So while they do not play a role in preventing one container from accessing or affecting the data and processes of another container, they are essential to fend off some denial-of-service attacks. They are particularly important on multi-tenant platforms, like public and private PaaS, to guarantee a consistent uptime (and performance) even when some applications start to misbehave.

Control Groups have been around for a while as well: the code was started in 2006, and initially merged in kernel 2.6.24.

## [Docker daemon attack surface](#docker-daemon-attack-surface)

Running containers (and applications) with Docker implies running the Docker daemon. This daemon requires `root` privileges unless you opt-in to [Rootless mode](https://docs.docker.com/engine/security/rootless/), and you should therefore be aware of some important details.

First of all, only trusted users should be allowed to control your Docker daemon. This is a direct consequence of some powerful Docker features. Specifically, Docker allows you to share a directory between the Docker host and a guest container; and it allows you to do so without limiting the access rights of the container. This means that you can start a container where the `/host` directory is the `/` directory on your host; and the container can alter your host filesystem without any restriction. This is similar to how virtualization systems allow filesystem resource sharing. Nothing prevents you from sharing your root filesystem (or even your root block device) with a virtual machine.

This has a strong security implication: for example, if you instrument Docker from a web server to provision containers through an API, you should be even more careful than usual with parameter checking, to make sure that a malicious user cannot pass crafted parameters causing Docker to create arbitrary containers.

For this reason, the REST API endpoint (used by the Docker CLI to communicate with the Docker daemon) changed in Docker 0.5.2, and now uses a Unix socket instead of a TCP socket bound on 127.0.0.1 (the latter being prone to cross-site request forgery attacks if you happen to run Docker directly on your local machine, outside of a VM). You can then use traditional Unix permission checks to limit access to the control socket.

You can also expose the REST API over HTTP if you explicitly decide to do so. However, if you do that, be aware of the above mentioned security implications. Note that even if you have a firewall to limit accesses to the REST API endpoint from other hosts in the network, the endpoint can be still accessible from containers, and it can easily result in the privilege escalation. Therefore it is *mandatory* to secure API endpoints with [HTTPS and certificates](https://docs.docker.com/engine/security/protect-access/). Exposing the daemon API over HTTP without TLS is not permitted, and such a configuration causes the daemon to fail early on startup, see [Unauthenticated TCP connections](https://docs.docker.com/engine/deprecated/#unauthenticated-tcp-connections). It is also recommended to ensure that it is reachable only from a trusted network or VPN.

You can also use `DOCKER_HOST=ssh://USER@HOST` or `ssh -L /path/to/docker.sock:/var/run/docker.sock` instead if you prefer SSH over TLS.

The daemon is also potentially vulnerable to other inputs, such as image loading from either disk with `docker load`, or from the network with `docker pull`. As of Docker 1.3.2, images are now extracted in a chrooted subprocess on Linux/Unix platforms, being the first-step in a wider effort toward privilege separation. As of Docker 1.10.0, all images are stored and accessed by the cryptographic checksums of their contents, limiting the possibility of an attacker causing a collision with an existing image.

Finally, if you run Docker on a server, it is recommended to run exclusively Docker on the server, and move all other services within containers controlled by Docker. Of course, it is fine to keep your favorite admin tools (probably at least an SSH server), as well as existing monitoring/supervision processes, such as NRPE and collectd.

## [Linux kernel capabilities](#linux-kernel-capabilities)

By default, Docker starts containers with a restricted set of capabilities. What does that mean?

Capabilities turn the binary "root/non-root" dichotomy into a fine-grained access control system. Processes (like web servers) that just need to bind on a port below 1024 do not need to run as root: they can just be granted the `net_bind_service` capability instead. And there are many other capabilities, for almost all the specific areas where root privileges are usually needed. This means a lot for container security.

Typical servers run several processes as `root`, including the SSH daemon, `cron` daemon, logging daemons, kernel modules, network configuration tools, and more. A container is different, because almost all of those tasks are handled by the infrastructure around the container:

* SSH access are typically managed by a single server running on the Docker host
* `cron`, when necessary, should run as a user process, dedicated and tailored for the app that needs its scheduling service, rather than as a platform-wide facility
* Log management is also typically handed to Docker, or to third-party services like Loggly or Splunk
* Hardware management is irrelevant, meaning that you never need to run `udevd` or equivalent daemons within containers
* Network management happens outside of the containers, enforcing separation of concerns as much as possible, meaning that a container should never need to perform `ifconfig`, `route`, or ip commands (except when a container is specifically engineered to behave like a router or firewall, of course)

This means that in most cases, containers do not need "real" root privileges at all\* And therefore, containers can run with a reduced capability set; meaning that "root" within a container has much less privileges than the real "root". For instance, it is possible to:

* Deny all "mount" operations
* Deny access to raw sockets (to prevent packet spoofing)
* Deny access to some filesystem operations, like creating new device nodes, changing the owner of files, or altering attributes (including the immutable flag)
* Deny module loading

This means that even if an intruder manages to escalate to root within a container, it is much harder to do serious damage, or to escalate to the host.

This doesn't affect regular web apps, but reduces the vectors of attack by malicious users considerably. By default Docker drops all capabilities except [those needed](https://github.com/moby/moby/blob/master/daemon/pkg/oci/caps/defaults.go#L6-L19), an allowlist instead of a denylist approach. You can see a full list of available capabilities in [Linux manpages](https://man7.org/linux/man-pages/man7/capabilities.7.html).

One primary risk with running Docker containers is that the default set of capabilities and mounts given to a container may provide incomplete isolation, either independently, or when used in combination with kernel vulnerabilities.

Docker supports the addition and removal of capabilities, allowing use of a non-default profile. This may make Docker more secure through capability removal, or less secure through the addition of capabilities. The best practice for users would be to remove all capabilities except those explicitly required for their processes.

## [Docker Content Trust signature verification](#docker-content-trust-signature-verification)

Docker Engine can be configured to only run signed images. The Docker Content Trust signature verification feature is built directly into the `dockerd` binary.\
This is configured in the Dockerd configuration file.

To enable this feature, trustpinning can be configured in `daemon.json`, whereby only repositories signed with a user-specified root key can be pulled and run.

This feature provides more insight to administrators than previously available with the CLI for enforcing and performing image signature verification.

For more information on configuring Docker Content Trust Signature Verification, go to [Content trust in Docker](https://docs.docker.com/engine/security/trust/).

## [Other kernel security features](#other-kernel-security-features)

Capabilities are just one of the many security features provided by modern Linux kernels. It is also possible to leverage existing, well-known systems like TOMOYO, AppArmor, SELinux, GRSEC, etc. with Docker.

While Docker currently only enables capabilities, it doesn't interfere with the other systems. This means that there are many different ways to harden a Docker host. Here are a few examples.

* You can run a kernel with GRSEC and PAX. This adds many safety checks, both at compile-time and run-time; it also defeats many exploits, thanks to techniques like address randomization. It doesn't require Docker-specific configuration, since those security features apply system-wide, independent of containers.
* If your distribution comes with security model templates for Docker containers, you can use them out of the box. For instance, we ship a template that works with AppArmor and Red Hat comes with SELinux policies for Docker. These templates provide an extra safety net (even though it overlaps greatly with capabilities).
* You can define your own policies using your favorite access control mechanism.

Just as you can use third-party tools to augment Docker containers, including special network topologies or shared filesystems, tools exist to harden Docker containers without the need to modify Docker itself.

As of Docker 1.10 User Namespaces are supported directly by the docker daemon. This feature allows for the root user in a container to be mapped to a non uid-0 user outside the container, which can help to mitigate the risks of container breakout. This facility is available but not enabled by default.

Refer to the [daemon command](https://docs.docker.com/reference/cli/dockerd/#daemon-user-namespace-options) in the command line reference for more information on this feature. Additional information on the implementation of User Namespaces in Docker can be found in [this blog post](https://integratedcode.us/2015/10/13/user-namespaces-have-arrived-in-docker/).

## [Conclusions](#conclusions)

Docker containers are, by default, quite secure; especially if you run your processes as non-privileged users inside the container.

You can add an extra layer of safety by enabling AppArmor, SELinux, GRSEC, or another appropriate hardening system.

If you think of ways to make docker more secure, we welcome feature requests, pull requests, or comments on the Docker community forums.

## [Related information](#related-information)

* [Use trusted images](https://docs.docker.com/engine/security/trust/)
* [Seccomp security profiles for Docker](https://docs.docker.com/engine/security/seccomp/)
* [AppArmor security profiles for Docker](https://docs.docker.com/engine/security/apparmor/)
* [On the Security of Containers (2014)](https://medium.com/@ewindisch/on-the-security-of-containers-2c60ffe25a9e)
* [Docker swarm mode overlay network security model](https://docs.docker.com/engine/network/drivers/overlay/)

----
url: https://docs.docker.com/reference/cli/docker/manifest/push/
----

# docker manifest push

***

| Description | Push a manifest list to a repository           |
| ----------- | ---------------------------------------------- |
| Usage       | `docker manifest push [OPTIONS] MANIFEST_LIST` |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Push a manifest list to a repository

## [Options](#options)

| Option        | Default | Description                               |
| ------------- | ------- | ----------------------------------------- |
| `--insecure`  |         | Allow push to an insecure registry        |
| `-p, --purge` |         | Remove the local manifest list after push |

----
url: https://docs.docker.com/dhi/how-to/mirror/
----

# Mirror a Docker Hardened Image repository

***

Table of contents

***

Subscription: Docker Hardened Images Select or Enterprise

Mirroring requires a DHI Select or Enterprise subscription. Without a subscription, you can pull Docker Hardened Images directly from `dhi.io` without mirroring. With a DHI Select or Enterprise subscription, you must mirror to your organization to get:

* Compliance variants (FIPS-enabled or STIG-ready images)
* Extended Lifecycle Support (ELS) variants (requires add-on)
* Image or Helm chart customization
* Air-gapped or restricted network environments
* [SLA-backed security updates](https://docs.docker.com/go/dhi-sla/)

## [How to mirror](#how-to-mirror)

This topic covers two types of mirroring for Docker Hardened Image (DHI) repositories:

* [Mirror to your organization](#mirror-a-dhi-repository-to-your-organization): Mirror a DHI repository to your organization's namespace on Docker Hub.

* [Mirror to a third-party registry](#mirror-a-dhi-repository-to-a-third-party-registry): Mirror a repository to another container registry, such as Amazon ECR, Google Artifact Registry, or a private Harbor instance.

## [Mirror a DHI repository to your organization](#mirror-a-dhi-repository-to-your-organization)

To mirror repositories, you must be an organization owner or editor, or use a personal access token (PAT) or organization access token (OAT). See the CLI and Terraform tabs in the following sections for required permission scopes.

* Image repositories: Mirroring lets you customize images by adding packages, OCI artifacts (such as custom certificates or additional tools), environment variables, labels, and other configuration settings. For more details, see [Customize a Docker Hardened Image](https://docs.docker.com/dhi/how-to/customize/#customize-a-docker-hardened-image).

* Chart repositories: Mirroring lets you customize image references within the chart. This is particularly useful when using customized images or when you've mirrored images to a third-party registry and need the chart to reference those custom locations. For more details, see [Customize a Docker Hardened Helm chart](https://docs.docker.com/dhi/how-to/customize/#customize-a-docker-hardened-helm-chart).

1. Go to [Docker Hub](https://hub.docker.com) and sign in.

2. Select **My Hub**.

3. In the namespace drop-down, select your organization.

4. Select **Hardened Images** > **Catalog**.

5. Select a DHI repository to view its details.

6. Mirror the repository:

   * To mirror an image repository, select **Use this image** > **Mirror repository**, and then follow the on-screen instructions. If you have the ELS add-on, you can also select **Enable support for end-of-life versions**.
   * To mirror a Helm chart repository, select **Get Helm chart**, and then follow the on-screen instructions.

It may take a few minutes for all the tags to finish mirroring.

Authenticate with `docker login` using your Docker credentials, a [personal access token (PAT)](https://docs.docker.com/security/access-tokens/) with **Read & Write** permissions, or an [organization access token (OAT)](https://docs.docker.com/enterprise/security/access-tokens/). When using an OAT, the available operations depend on the token's permission scope:

* To list mirrored repositories, the OAT must have read (pull) access to the relevant repositories. Results are scoped to repositories the OAT can access.
* To create a mirror to an existing destination repository, the OAT must have push access to that repository. To create a mirror to a new destination repository that doesn't yet exist, the OAT must have org-wide repository access (for example, `<org>/*` with pull or push). Repository-scoped access to the future repository name is not sufficient.
* To stop mirroring, the OAT must have push access to the relevant repository.
* OATs with public repository read-only access cannot list or manage mirrored repositories.

Use the [`docker dhi mirror`](/reference/cli/docker/dhi/mirror/) command:

```console
$ docker dhi mirror start --org my-org \
  dhi/golang,my-org/dhi-golang \
  dhi/nginx,my-org/dhi-nginx \
  dhi/prometheus-chart,my-org/dhi-prometheus-chart
```

Mirror with dependencies:

```console
$ docker dhi mirror start --org my-org dhi/golang,my-org/dhi-golang --dependencies
```

List mirrored images in your organization:

```console
$ docker dhi mirror list --org my-org
```

Filter mirrored images by name or type:

```console
$ docker dhi mirror list --org my-org --filter python
$ docker dhi mirror list --org my-org --type image
$ docker dhi mirror list --org my-org --type helm-chart
```

You can manage DHI mirrors as infrastructure-as-code using the [DHI Terraform provider](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs).

First, install and configure the provider:

```hcl
terraform {
  required_providers {
    dhi = {
      source = "docker-hardened-images/dhi"
    }
  }
}

provider "dhi" {
  docker_hub_username = var.docker_username
  docker_hub_password = var.docker_password
  organization        = var.org_name
}
```

> Note
>
> Instead of specifying credentials in the provider block, you can set the `DOCKER_USERNAME`, `DOCKER_PASSWORD`, and `DHI_ORG` environment variables. You can also authenticate using an organization access token (OAT) in place of a password. Set `DOCKER_USERNAME` to your organization namespace and `DOCKER_PASSWORD` to the OAT. When using an OAT, the same permission scopes apply as with the CLI: read (pull) access is required to list mirrors, and push access is required to create or delete them.

Then, define a `dhi_mirror` resource for each repository you want to mirror:

```hcl
resource "dhi_mirror" "golang" {
  source_namespace = "dhi"
  source_name      = "golang"
  destination_name = "dhi-golang"
}

resource "dhi_mirror" "nginx" {
  source_namespace = "dhi"
  source_name      = "nginx"
  destination_name = "dhi-nginx"
}
```

To enable Extended Lifecycle Support (ELS) variants, set the `els` attribute:

```hcl
resource "dhi_mirror" "golang" {
  source_namespace = "dhi"
  source_name      = "golang"
  destination_name = "dhi-golang"
  els              = true
}
```

Run `terraform apply` to create the mirrors.

For the full list of resource attributes, see the [Terraform Registry documentation](https://registry.terraform.io/providers/docker-hardened-images/dhi/latest/docs/resources/mirror).

After mirroring, the repository appears in your organization's repository list, prefixed by `dhi-`, and continues to receive updated images. It behaves like any other Docker Hub repository, so you can manage access and permissions, configure webhooks, and use other standard Hub features. See [Docker Hub repositories](https://docs.docker.com/docker-hub/repos/) for details.

### [Stop mirroring a repository](#stop-mirroring-a-repository)

After you stop mirroring, the repository remains, but it no longer receives updates. You can still use the last images or charts that were mirrored.

> Note
>
> If you only want to stop mirroring ELS versions, you can clear the ELS option in the mirrored repository's **Settings** tab.

1. Go to [Docker Hub](https://hub.docker.com) and sign in.
2. Select **My Hub**.
3. In the namespace drop-down, select your organization that has access to DHI.
4. Select **Hardened Images** > **Manage**.
5. Select the **Mirrored Images** or **Mirrored Helm charts** tab.
6. In the far right column of the repository you want to stop mirroring, select the menu icon.
7. Select **Stop mirroring**.

Authenticate with `docker login` using your Docker credentials, a [personal access token (PAT)](https://docs.docker.com/security/access-tokens/) with **Read & Write** permissions, or an [organization access token (OAT)](https://docs.docker.com/enterprise/security/access-tokens/) with push access to the relevant repository.

Use the [`docker dhi mirror`](/reference/cli/docker/dhi/mirror/) command:

```console
$ docker dhi mirror stop --org my-org dhi-golang
```

To stop mirroring, remove the `dhi_mirror` resource from your Terraform configuration and run `terraform apply`. The repository remains in your organization but no longer receives updates.

## [Mirror a DHI repository to a third-party registry](#mirror-a-dhi-repository-to-a-third-party-registry)

After mirroring a DHI repository to your organization on Docker Hub, you can optionally mirror it to another container registry, such as Amazon ECR, Google Artifact Registry, GitHub Container Registry, or a private Harbor instance.

You can use any standard workflow to mirror the image, such as the [Docker CLI](/reference/cli/docker/), [Docker Hub Registry API](/reference/api/registry/latest/), third-party registry tools, or CI/CD automation.

However, to preserve the full security context, including attestations, you must also mirror its associated OCI artifacts. DHI repositories store the image layers on `dhi.io` (or `docker.io` for customized images) and the signed attestations in a separate registry (`registry.scout.docker.com`).

To copy both, you can use [`regctl`](https://regclient.org/cli/regctl/), an OCI-aware CLI that supports mirroring images along with attached artifacts such as SBOMs, vulnerability reports, and SLSA provenance. For ongoing synchronization, you can use [`regsync`](https://regclient.org/cli/regsync/).

### [Automate syncing with webhooks](#automate-syncing-with-webhooks)

To keep external registries or systems in sync with your mirrored Docker Hardened Images, and to receive notifications when updates occur, you can configure a [webhook](/docker-hub/repos/manage/webhooks/) on the mirrored repository in Docker Hub. A webhook sends a `POST` request to a URL you define whenever a new image tag is pushed or updated.

For example, you might configure a webhook to call a CI/CD system at `https://ci.example.com/hooks/dhi-sync` whenever a new tag is mirrored. The automation triggered by this webhook can pull the updated image from Docker Hub and push it to an internal registry such as Amazon ECR, Google Artifact Registry, or GitHub Container Registry.

Other common webhook use cases include:

* Triggering validation or vulnerability scanning workflows
* Signing or promoting images
* Sending notifications to downstream systems

#### [Example webhook payload](#example-webhook-payload)

When a webhook is triggered, Docker Hub sends a JSON payload like the following:

```json
{
  "callback_url": "https://registry.hub.docker.com/u/exampleorg/dhi-python/hook/abc123/",
  "push_data": {
    "pushed_at": 1712345678,
    "pusher": "trustedbuilder",
    "tag": "3.13-alpine3.21"
  },
  "repository": {
    "name": "dhi-python",
    "namespace": "exampleorg",
    "repo_name": "exampleorg/dhi-python",
    "repo_url": "https://hub.docker.com/r/exampleorg/dhi-python",
    "is_private": true,
    "status": "Active",
    ...
  }
}
```

### [Example mirroring with `regctl`](#example-mirroring-with-regctl)

The following example shows how to mirror a specific tag of a Docker Hardened Image from Docker Hub to another registry, along with its associated attestations using `regctl`. You must [install `regctl`](https://github.com/regclient/regclient) first.

The example assumes you have mirrored the DHI repository to your organization's namespace on Docker Hub as described in the previous section. You can apply the same steps to a non-mirrored image by updating the `SRC_ATT_REPO` and `SRC_REPO` variables accordingly.

1. Set environment variables for your specific environment. Replace the placeholders with your actual values.

   In this example, you authenticate as your Docker organization using an [organization access token (OAT)](https://docs.docker.com/enterprise/security/access-tokens/). The OAT must have at least pull access to every DHI repository you want to mirror. Only repositories in the token's scope are accessible. Alternatively, you can authenticate as a Docker Hub user with a [personal access token (PAT)](https://docs.docker.com/security/access-tokens/) that has `read only` access.

   > Warning
   >
   > The following examples export credentials directly on the command line for demonstration purposes. This exposes sensitive tokens in your shell history and process list. In production environments, use secure methods such as reading from files with restricted permissions, environment files loaded at runtime, or secret management tools.

   ```console
   $ export DOCKER_ORG="YOUR_DOCKER_ORG"
   $ export DOCKER_OAT="YOUR_DOCKER_OAT"
   $ export DEST_REG="registry.example.com"
   $ export DEST_REPO="mirror/dhi-python"
   $ export DEST_REG_USERNAME="YOUR_DESTINATION_REGISTRY_USERNAME"
   $ export DEST_REG_TOKEN="YOUR_DESTINATION_REGISTRY_TOKEN"
   $ export SRC_REPO="docker.io/${DOCKER_ORG}/dhi-python"
   $ export SRC_ATT_REPO="registry.scout.docker.com/${DOCKER_ORG}/dhi-python"
   $ export TAG="3.13-alpine3.21"
   ```

2. Sign in via `regctl` to Docker Hub, the Scout registry that contains the attestations, and your destination registry.

   ```console
   $ echo $DOCKER_OAT | regctl registry login -u "$DOCKER_ORG" --pass-stdin docker.io
   $ echo $DOCKER_OAT | regctl registry login -u "$DOCKER_ORG" --pass-stdin registry.scout.docker.com
   $ echo $DEST_REG_TOKEN | regctl registry login -u "$DEST_REG_USERNAME" --pass-stdin "$DEST_REG"
   ```

3. Mirror the image and attestations using `--referrers` and referrer endpoints:

   ```console
   $ regctl image copy \
        "${SRC_REPO}:${TAG}" \
        "${DEST_REG}/${DEST_REPO}:${TAG}" \
        --referrers \
        --referrers-src "${SRC_ATT_REPO}" \
        --referrers-tgt "${DEST_REG}/${DEST_REPO}" \
        --force-recursive
   ```

4. Verify that artifacts were preserved.

   First, get a digest for a specific tag and platform. For example, `linux/amd64`.

   ```console
   DIGEST="$(regctl manifest head "${DEST_REG}/${DEST_REPO}:${TAG}" --platform linux/amd64)"
   ```

   List attached artifacts (SBOM, provenance, VEX, vulnerability reports).

   ```console
   $ regctl artifact list "${DEST_REG}/${DEST_REPO}@${DIGEST}"
   ```

   Or, list attached artifacts with `docker scout`.

   ```console
   $ docker scout attest list "registry://${DEST_REG}/${DEST_REPO}@${DIGEST}"
   ```

### [Example ongoing mirroring with `regsync`](#example-ongoing-mirroring-with-regsync)

`regsync` automates pulling from your organizations mirrored DHI repositories on Docker Hub and pushing to your external registry including attestations. It reads a YAML configuration file and can filter tags.

The following example uses a `regsync.yaml` file that syncs Node 24 and Python 3.12 Debian 13 variants, excluding Alpine and Debian 12.

regsync.yaml

```yaml
version: 1
# Optional: inline creds if not relying on prior CLI logins
# creds:
#   - registry: docker.io
#     user: <your-docker-org>
#     pass: "{{file \"/run/secrets/docker_oat\"}}"
#   - registry: registry.scout.docker.com
#     user: <your-docker-org>
#     pass: "{{file \"/run/secrets/docker_oat\"}}"
#   - registry: registry.example.com
#     user: <service-user>
#     pass: "{{file \"/run/secrets/dest_token\"}}"

sync:
  - source: docker.io/<your-org>/dhi-node
    target: registry.example.com/mirror/dhi-node
    type: repository
    fastCopy: true
    referrers: true
    referrerSource: registry.scout.docker.com/<your-org>/dhi-node
    referrerTarget: registry.example.com/mirror/dhi-node
    tags:
      allow: [ "24.*" ]
      deny: [ ".*alpine.*", ".*debian12.*" ]

  - source: docker.io/<your-org>/dhi-python
    target: registry.example.com/mirror/dhi-python
    type: repository
    fastCopy: true
    referrers: true
    referrerSource: registry.scout.docker.com/<your-org>/dhi-python
    referrerTarget: registry.example.com/mirror/dhi-python
    tags:
      allow: [ "3.12.*" ]
      deny: [ ".*alpine.*", ".*debian12.*" ]
```

To do a dry run with the configuration file, you can run the following command. You must [install `regsync`](https://github.com/regclient/regclient) first.

```console
$ regsync check -c regsync.yaml
```

To run the sync with the configuration file:

```console
$ regsync once -c regsync.yaml
```

## [What next](#what-next)

After mirroring, see [Pull a DHI](https://docs.docker.com/dhi/how-to/use/#pull-a-dhi) to learn how to pull and use mirrored images.

----
url: https://docs.docker.com/reference/api/engine/version/v1.43/
----

# Docker Engine API (1.43)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.43.yaml)

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

If you omit the version-prefix, the current version of the API (v1.43) is used. For example, calling `/info` is the same as calling `/v1.43/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

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

/v1.43/containers/json

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
| MacAddress      | string or nullMAC address of the container.                                                                                                                                                                                                                                                           |
| OnBuild         | Array of strings or null`ONBUILD` metadata that were defined in the image's `Dockerfile`.                                                                                                                                                                                                             |
|                 | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                |
| StopSignal      | string or nullSignal to stop a container as a string or unsigned integer.                                                                                                                                                                                                                             |
| StopTimeout     | integer or nullDefault: 10Timeout to stop a container in seconds.                                                                                                                                                                                                                                     |
| Shell           | Array of strings or nullShell for when `RUN`, `CMD`, and `ENTRYPOINT` uses a shell.                                                                                                                                                                                                                   |
|                 | object (HostConfig)Container configuration that depends on the host we are running on                                                                                                                                                                                                                 |
|                 | object (NetworkingConfig)NetworkingConfig represents the container's networking configuration for each of its interfaces. It is used for the networking configs specified in the `docker create` and `docker network connect` commands.                                                               |

### Responses

/v1.43/containers/create

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
}
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

/v1.43/containers/{id}/json

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

/v1.43/containers/{id}/top

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

/v1.43/containers/{id}/logs

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

/v1.43/containers/{id}/changes

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

/v1.43/containers/{id}/export

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

/v1.43/containers/{id}/stats

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

/v1.43/containers/{id}/resize

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

/v1.43/containers/{id}/start

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

/v1.43/containers/{id}/stop

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

/v1.43/containers/{id}/restart

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

/v1.43/containers/{id}/kill

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

/v1.43/containers/{id}/update

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

/v1.43/containers/{id}/rename

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

/v1.43/containers/{id}/pause

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

/v1.43/containers/{id}/unpause

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

/v1.43/containers/{id}/attach

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

/v1.43/containers/{id}/attach/ws

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

/v1.43/containers/{id}/wait

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

/v1.43/containers/{id}

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

/v1.43/containers/{id}/archive

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

/v1.43/containers/{id}/archive

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

/v1.43/containers/{id}/archive

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

/v1.43/containers/prune

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

|             |                                                                                                                                                                                                                                                                                                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| all         | booleanDefault: falseShow all images. Only images from a final layer (no children) are shown by default.                                                                                                                                                                                                                                                                       |
| filters     | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the images list.Available filters:- `before`=(`<image-name>[:<tag>]`, `<image id>` or `<image@digest>`)
- `dangling=true`
- `label=key` or `label="key=value"` of an image label
- `reference`=(`<image-name>[:<tag>]`)
- `since`=(`<image-name>[:<tag>]`, `<image id>` or `<image@digest>`) |
| shared-size | booleanDefault: falseCompute and show shared size as a `SharedSize` field on each image.                                                                                                                                                                                                                                                                                       |
| digests     | booleanDefault: falseShow digest information as a `RepoDigests` field on each image.                                                                                                                                                                                                                                                                                           |

### Responses

/v1.43/images/json

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
"VirtualSize": 172064416,
"Labels": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"Containers": 2
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

/v1.43/build

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

/v1.43/build/prune

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

Create an image by either pulling it from a registry or importing it.

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

/v1.43/images/create

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

/v1.43/images/{name}/json

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
"Container": "65974bc86f1770ae4bff79f651ebdbce166ae9aada632ee3fa9af3a264911735",
"ContainerConfig": {
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
"StartPeriod": 0
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
},
"DockerVersion": "20.10.7",
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
"VirtualSize": 1239828,
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

/v1.43/images/{name}/history

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

|     |                                                                                                                                                                 |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| tag | stringTag of the image to push. For example, `latest`. If no tag is provided, all tags of the given image that are present in the local image store are pushed. |

##### header Parameters

|                         |                                                                                                                          |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| X-Registry-Authrequired | stringA base64url-encoded auth configuration.Refer to the [authentication section](#section/Authentication) for details. |

### Responses

/v1.43/images/{name}/push

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

/v1.43/images/{name}/tag

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

/v1.43/images/{name}

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

|              |                                                                                                                                                                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| termrequired | stringTerm to search                                                                                                                                                                                                                                  |
| limit        | integerMaximum number of results to return                                                                                                                                                                                                            |
| filters      | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the images list. Available filters:- `is-automated=(true\|false)`
- `is-official=(true\|false)`
- `stars=<number>` Matches images that has at least 'number' stars. |

### Responses

/v1.43/images/search

### Response samples

* 200
* 500

Content type

application/json

`[
{
"description": "",
"is_official": false,
"is_automated": false,
"name": "wma55/u1210sshd",
"star_count": 0
},
{
"description": "",
"is_official": false,
"is_automated": false,
"name": "jdswinbank/sshd",
"star_count": 0
},
{
"description": "",
"is_official": false,
"is_automated": false,
"name": "vgauthier/sshd",
"star_count": 0
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

/v1.43/images/prune

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
| MacAddress      | string or nullMAC address of the container.                                                                                                                                                                                                                                                           |
| OnBuild         | Array of strings or null`ONBUILD` metadata that were defined in the image's `Dockerfile`.                                                                                                                                                                                                             |
|                 | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                |
| StopSignal      | string or nullSignal to stop a container as a string or unsigned integer.                                                                                                                                                                                                                             |
| StopTimeout     | integer or nullDefault: 10Timeout to stop a container in seconds.                                                                                                                                                                                                                                     |
| Shell           | Array of strings or nullShell for when `RUN`, `CMD`, and `ENTRYPOINT` uses a shell.                                                                                                                                                                                                                   |

### Responses

/v1.43/commit

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
"StartPeriod": 0
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

An image tarball contains one directory per image layer (named using its long ID), each containing these files:

* `VERSION`: currently `1.0` - the file format version
* `json`: detailed layer information, similar to `docker inspect layer_id`
* `layer.tar`: A tarfile containing the filesystem changes in this layer

The `layer.tar` file contains `aufs` style `.wh..wh.aufs` files and directories for storing attribute changes and deletions.

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

/v1.43/images/{name}/get

## [](#tag/Image/operation/ImageGetAll)Export several images

Get a tarball containing all images and metadata for several image repositories.

For each value of the `names` parameter: if it is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|       |                                          |
| ----- | ---------------------------------------- |
| names | Array of stringsImage names to filter by |

### Responses

/v1.43/images/get

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

/v1.43/images/load

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

/v1.43/networks

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

/v1.43/networks/{id}

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

/v1.43/networks/{id}

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

|                |                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Namerequired   | stringThe network's name.                                                                                                                                                                                                                                                                                                                                                                                                                        |
| CheckDuplicate | booleanCheck for networks with duplicate names. Since Network is primarily keyed based on a random ID and not on the name, and network name is strictly a user-friendly alias to the network which is uniquely identified using ID, there is no guaranteed way to check for duplicates. CheckDuplicate is there to provide a best effort checking of any networks which has the same name but it is not guaranteed to catch all name collisions. |
| Driver         | stringDefault: "bridge"Name of the network driver plugin to use.                                                                                                                                                                                                                                                                                                                                                                                 |
| Scope          | stringThe level at which the network exists (e.g. `swarm` for cluster-wide or `local` for machine level).                                                                                                                                                                                                                                                                                                                                        |
| Internal       | booleanRestrict external access to the network.                                                                                                                                                                                                                                                                                                                                                                                                  |
| Attachable     | booleanGlobally scoped network is manually attachable by regular containers from workers in swarm mode.                                                                                                                                                                                                                                                                                                                                          |
| Ingress        | booleanIngress network is the network which provides the routing-mesh in swarm mode.                                                                                                                                                                                                                                                                                                                                                             |
| ConfigOnly     | booleanDefault: falseCreates a config-only network. Config-only networks are placeholder networks for network configurations to be used by other networks. Config-only networks cannot be used directly to run containers or services.                                                                                                                                                                                                           |
|                | object (ConfigReference)The config-only network source to provide the configuration for this network.                                                                                                                                                                                                                                                                                                                                            |
|                | object (IPAM)                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| EnableIPv6     | booleanEnable IPv6 on the network.                                                                                                                                                                                                                                                                                                                                                                                                               |
|                | objectNetwork specific options to be used by the drivers.                                                                                                                                                                                                                                                                                                                                                                                        |
|                | objectUser-defined key/value metadata.                                                                                                                                                                                                                                                                                                                                                                                                           |

### Responses

/v1.43/networks/create

### Request samples

* Payload

Content type

application/json

`{
"Name": "my_network",
"CheckDuplicate": true,
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
"Id": "22be93d5babb089c5aab8dbc369042fad48ff791584ca2da2100db837a1c7c30",
"Warning": ""
}`

## [](#tag/Network/operation/NetworkConnect)Connect a container to a network

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

/v1.43/networks/{id}/connect

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
}
}
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

/v1.43/networks/{id}/disconnect

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

/v1.43/networks/prune

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

/v1.43/volumes

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

/v1.43/volumes/create

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

/v1.43/volumes/{name}

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

/v1.43/volumes/{name}

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

/v1.43/volumes/{name}

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

/v1.43/volumes/prune

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

/v1.43/containers/{id}/exec

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

/v1.43/exec/{id}/start

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

/v1.43/exec/{id}/resize

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

/v1.43/exec/{id}/json

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

/v1.43/swarm

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

/v1.43/swarm/init

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

/v1.43/swarm/join

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

/v1.43/swarm/leave

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

/v1.43/swarm/update

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

/v1.43/swarm/unlockkey

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

/v1.43/swarm/unlock

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

/v1.43/nodes

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

/v1.43/nodes/{id}

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

/v1.43/nodes/{id}

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

/v1.43/nodes/{id}/update

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

/v1.43/services

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

|      |                                                                                                  |
| ---- | ------------------------------------------------------------------------------------------------ |
| Name | stringName of the service.                                                                       |
|      | objectUser-defined key/value metadata.                                                           |
|      | object (TaskSpec)User modifiable task configuration.                                             |
|      | objectScheduling mode for the service.                                                           |
|      | objectSpecification for the update strategy of the service.                                      |
|      | objectSpecification for the rollback strategy of the service.                                    |
|      | Array of objects (NetworkAttachmentConfig)Specifies which networks the service should attach to. |
|      | object (EndpointSpec)Properties that can be configured to access and load balance a service.     |

### Responses

/v1.43/services/create

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
}
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
"CreateMountpoint": false
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
}
},
"TmpfsOptions": {
"SizeBytes": 0,
"Mode": 0
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
"StartPeriod": 0
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
"Warning": "unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"
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

/v1.43/services/{id}

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

/v1.43/services/{id}

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

|      |                                                                                                  |
| ---- | ------------------------------------------------------------------------------------------------ |
| Name | stringName of the service.                                                                       |
|      | objectUser-defined key/value metadata.                                                           |
|      | object (TaskSpec)User modifiable task configuration.                                             |
|      | objectScheduling mode for the service.                                                           |
|      | objectSpecification for the update strategy of the service.                                      |
|      | objectSpecification for the rollback strategy of the service.                                    |
|      | Array of objects (NetworkAttachmentConfig)Specifies which networks the service should attach to. |
|      | object (EndpointSpec)Properties that can be configured to access and load balance a service.     |

### Responses

/v1.43/services/{id}/update

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
}
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
"CreateMountpoint": false
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
}
},
"TmpfsOptions": {
"SizeBytes": 0,
"Mode": 0
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
"StartPeriod": 0
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
"Warning": "unable to pin image doesnotexist:latest to digest: image library/doesnotexist:latest not found"
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

/v1.43/services/{id}/logs

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

/v1.43/tasks

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

/v1.43/tasks/{id}

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

/v1.43/tasks/{id}/logs

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

/v1.43/secrets

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

/v1.43/secrets/create

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

/v1.43/secrets/{id}

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

/v1.43/secrets/{id}

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

/v1.43/secrets/{id}/update

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

/v1.43/configs

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

/v1.43/configs/create

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

/v1.43/configs/{id}

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

/v1.43/configs/{id}

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

/v1.43/configs/{id}/update

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

/v1.43/plugins

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

/v1.43/plugins/privileges

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

/v1.43/plugins/pull

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

/v1.43/plugins/{name}/json

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

/v1.43/plugins/{name}

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

/v1.43/plugins/{name}/enable

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

/v1.43/plugins/{name}/disable

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

/v1.43/plugins/{name}/upgrade

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

/v1.43/plugins/create

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

/v1.43/plugins/{name}/push

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

/v1.43/plugins/{name}/set

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

/v1.43/auth

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

/v1.43/info

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
"KernelVersion": "4.9.38-moby",
"OperatingSystem": "Alpine Linux v3.5",
"OSVersion": "16.04",
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
"ServerVersion": "24.0.2",
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
]
}`

## [](#tag/System/operation/SystemVersion)Get version

Returns the version of Docker that is running and various information about the system that Docker is running on.

### Responses

/v1.43/version

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
"Version": "19.03.12",
"Details": { }
}
],
"Version": "19.03.12",
"ApiVersion": "1.40",
"MinAPIVersion": "1.12",
"GitCommit": "48a66213fe",
"GoVersion": "go1.13.14",
"Os": "linux",
"Arch": "amd64",
"KernelVersion": "4.19.76-linuxkit",
"Experimental": true,
"BuildTime": "2020-06-22T15:49:27.000000000+00:00"
}`

## [](#tag/System/operation/SystemPing)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.43/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.43/\_ping

## [](#tag/System/operation/SystemEvents)Monitor events

Stream real-time events from the server.

Various objects within Docker report events when something happens to them.

Containers report these events: `attach`, `commit`, `copy`, `create`, `destroy`, `detach`, `die`, `exec_create`, `exec_detach`, `exec_start`, `exec_die`, `export`, `health_status`, `kill`, `oom`, `pause`, `rename`, `resize`, `restart`, `start`, `stop`, `top`, `unpause`, `update`, and `prune`

Images report these events: `delete`, `import`, `load`, `pull`, `push`, `save`, `tag`, `untag`, and `prune`

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

/v1.43/events

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

/v1.43/system/df

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
"VirtualSize": 1092588,
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

/v1.43/distribution/{name}/json

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

/v1.43/session

----
