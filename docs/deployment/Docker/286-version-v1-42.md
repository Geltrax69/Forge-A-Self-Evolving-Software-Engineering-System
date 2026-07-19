url: https://docs.docker.com/reference/api/engine/version/v1.42/
----

# Docker Engine API (1.42)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.42.yaml)

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

If you omit the version-prefix, the current version of the API (v1.42) is used. For example, calling `/info` is the same as calling `/v1.42/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

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

/v1.42/containers/json

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

/v1.42/containers/create

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

/v1.42/containers/{id}/json

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

/v1.42/containers/{id}/top

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

/v1.42/containers/{id}/logs

### Response samples

* 404

Content type

application/vnd.docker.raw-stream

No sample

## [](#tag/Container/operation/ContainerChanges)Get changes on a container’s filesystem

Returns which files in a container's filesystem have been added, deleted, or modified. The `Kind` of modification can be one of:

* `0`: Modified
* `1`: Added
* `2`: Deleted

##### path Parameters

|            |                                   |
| ---------- | --------------------------------- |
| idrequired | stringID or name of the container |

### Responses

/v1.42/containers/{id}/changes

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

/v1.42/containers/{id}/export

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

/v1.42/containers/{id}/stats

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

/v1.42/containers/{id}/resize

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

/v1.42/containers/{id}/start

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

/v1.42/containers/{id}/stop

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

/v1.42/containers/{id}/restart

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

/v1.42/containers/{id}/kill

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

/v1.42/containers/{id}/update

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

/v1.42/containers/{id}/rename

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

/v1.42/containers/{id}/pause

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

/v1.42/containers/{id}/unpause

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

/v1.42/containers/{id}/attach

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

/v1.42/containers/{id}/attach/ws

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

/v1.42/containers/{id}/wait

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

/v1.42/containers/{id}

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

/v1.42/containers/{id}/archive

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

/v1.42/containers/{id}/archive

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

/v1.42/containers/{id}/archive

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

/v1.42/containers/prune

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

/v1.42/images/json

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

/v1.42/build

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

|              |                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| keep-storage | integer \<int64>Amount of disk space in bytes to keep for cache                                                                                                                                                                                                                                                                                                                    |
| all          | booleanRemove all types of build cache                                                                                                                                                                                                                                                                                                                                             |
| filters      | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the list of build cache objects.Available filters:- `until=<duration>`: duration relative to daemon's time, during which build cache was not used, in Go's duration format (e.g., '24h')
- `id=<id>`
- `parent=<id>`
- `type=<string>`
- `description=<string>`
- `inuse`
- `shared`
- `private` |

### Responses

/v1.42/build/prune

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

/v1.42/images/create

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

/v1.42/images/{name}/json

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

/v1.42/images/{name}/history

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

/v1.42/images/{name}/push

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

/v1.42/images/{name}/tag

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

/v1.42/images/{name}

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

/v1.42/images/search

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

/v1.42/images/prune

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

/v1.42/commit

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

/v1.42/images/{name}/get

## [](#tag/Image/operation/ImageGetAll)Export several images

Get a tarball containing all images and metadata for several image repositories.

For each value of the `names` parameter: if it is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|       |                                          |
| ----- | ---------------------------------------- |
| names | Array of stringsImage names to filter by |

### Responses

/v1.42/images/get

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

/v1.42/images/load

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

/v1.42/networks

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

/v1.42/networks/{id}

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

/v1.42/networks/{id}

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

/v1.42/networks/create

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

/v1.42/networks/{id}/connect

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

/v1.42/networks/{id}/disconnect

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

/v1.42/networks/prune

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

/v1.42/volumes

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

/v1.42/volumes/create

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

/v1.42/volumes/{name}

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

/v1.42/volumes/{name}

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

/v1.42/volumes/{name}

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

/v1.42/volumes/prune

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

/v1.42/containers/{id}/exec

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

/v1.42/exec/{id}/start

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

/v1.42/exec/{id}/resize

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

/v1.42/exec/{id}/json

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

/v1.42/swarm

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

/v1.42/swarm/init

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

/v1.42/swarm/join

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

/v1.42/swarm/leave

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

/v1.42/swarm/update

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

/v1.42/swarm/unlockkey

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

/v1.42/swarm/unlock

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

/v1.42/nodes

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

/v1.42/nodes/{id}

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

/v1.42/nodes/{id}

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

/v1.42/nodes/{id}/update

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

/v1.42/services

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

/v1.42/services/create

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

/v1.42/services/{id}

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

/v1.42/services/{id}

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

/v1.42/services/{id}/update

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

/v1.42/services/{id}/logs

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

/v1.42/tasks

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

/v1.42/tasks/{id}

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

/v1.42/tasks/{id}/logs

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

/v1.42/secrets

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

/v1.42/secrets/create

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

/v1.42/secrets/{id}

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

/v1.42/secrets/{id}

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

/v1.42/secrets/{id}/update

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

/v1.42/configs

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

/v1.42/configs/create

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

/v1.42/configs/{id}

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

/v1.42/configs/{id}

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

/v1.42/configs/{id}/update

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

/v1.42/plugins

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

/v1.42/plugins/privileges

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

/v1.42/plugins/pull

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

/v1.42/plugins/{name}/json

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

/v1.42/plugins/{name}

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

/v1.42/plugins/{name}/enable

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

/v1.42/plugins/{name}/disable

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

/v1.42/plugins/{name}/upgrade

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

/v1.42/plugins/create

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

/v1.42/plugins/{name}/push

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

/v1.42/plugins/{name}/set

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

/v1.42/auth

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

/v1.42/info

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
"ServerVersion": "23.0.0",
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

/v1.42/version

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

/v1.42/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.42/\_ping

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

/v1.42/events

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

/v1.42/system/df

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

/v1.42/distribution/{name}/json

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

/v1.42/session

----
url: https://docs.docker.com/guides/testcontainers-java-spring-boot-kafka/create-project/
----

# Create the Spring Boot project

***

Table of contents

***

## [Set up the project](#set-up-the-project)

Create a Spring Boot project from [Spring Initializr](https://start.spring.io) by selecting the **Spring for Apache Kafka**, **Spring Data JPA**, **MySQL Driver**, and **Testcontainers** starters.

Alternatively, clone the [guide repository](https://github.com/testcontainers/tc-guide-testing-spring-boot-kafka-listener).

After generating the application, add the Awaitility library as a test dependency. You'll use it later to assert the expectations of an asynchronous process flow.

The key dependencies in `pom.xml` are:

```xml
<properties>
    <java.version>17</java.version>
    <testcontainers.version>2.0.4</testcontainers.version>
</properties>
<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka</artifactId>
    </dependency>
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.kafka</groupId>
        <artifactId>spring-kafka-test</artifactId>
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
    <dependency>
        <groupId>org.awaitility</groupId>
        <artifactId>awaitility</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

Using the Testcontainers BOM (Bill of Materials) is recommended so that you don't have to repeat the version for every Testcontainers module dependency.

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
class Product {

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

## [Create the Spring Data JPA repository](#create-the-spring-data-jpa-repository)

Create a repository interface for the `Product` entity with a method to find a product by code and a method to update the price for a given product code:

```java
package com.testcontainers.demo;

import java.math.BigDecimal;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Modifying;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

interface ProductRepository extends JpaRepository<Product, Long> {
  Optional<Product> findByCode(String code);

  @Modifying
  @Query("update Product p set p.price = :price where p.code = :productCode")
  void updateProductPrice(
    @Param("productCode") String productCode,
    @Param("price") BigDecimal price
  );
}
```

## [Add a schema creation script](#add-a-schema-creation-script)

Because the application doesn't use an in-memory database, you need to create the MySQL tables. The recommended approach for production is a migration tool like Flyway or Liquibase, but for this guide the built-in Spring Boot schema initialization is sufficient.

Create `src/main/resources/schema.sql`:

```sql
create table products (
      id int NOT NULL AUTO_INCREMENT,
      code varchar(255) not null,
      name varchar(255) not null,
      price numeric(5,2) not null,
      PRIMARY KEY (id),
      UNIQUE (code)
);
```

Enable schema initialization in `src/main/resources/application.properties`:

```properties
spring.sql.init.mode=always
```

## [Create the event payload](#create-the-event-payload)

Create a record named `ProductPriceChangedEvent` that represents the structure of the event payload received from the Kafka topic:

```java
package com.testcontainers.demo;

import java.math.BigDecimal;

record ProductPriceChangedEvent(String productCode, BigDecimal price) {}
```

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

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

@Component
@Transactional
class ProductPriceChangedEventHandler {

  private static final Logger log = LoggerFactory.getLogger(
    ProductPriceChangedEventHandler.class
  );

  private final ProductRepository productRepository;

  ProductPriceChangedEventHandler(ProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @KafkaListener(topics = "product-price-changes", groupId = "demo")
  public void handle(ProductPriceChangedEvent event) {
    log.info(
      "Received a ProductPriceChangedEvent with productCode:{}: ",
      event.productCode()
    );
    productRepository.updateProductPrice(event.productCode(), event.price());
  }
}
```

The `@KafkaListener` annotation specifies the topic name to listen to. Spring Kafka handles serialization and deserialization based on the properties configured in `application.properties`.

## [Configure Kafka serialization](#configure-kafka-serialization)

Add the following Kafka properties to `src/main/resources/application.properties`:

```properties
######## Kafka Configuration  #########
spring.kafka.bootstrap-servers=localhost:9092
spring.kafka.producer.key-serializer=org.apache.kafka.common.serialization.StringSerializer
spring.kafka.producer.value-serializer=org.springframework.kafka.support.serializer.JsonSerializer

spring.kafka.consumer.group-id=demo
spring.kafka.consumer.auto-offset-reset=latest
spring.kafka.consumer.key-deserializer=org.apache.kafka.common.serialization.StringDeserializer
spring.kafka.consumer.value-deserializer=org.springframework.kafka.support.serializer.JsonDeserializer
spring.kafka.consumer.properties.spring.json.trusted.packages=com.testcontainers.demo
```

The `productCode` key is (de)serialized using `StringSerializer`/`StringDeserializer`, and the `ProductPriceChangedEvent` value is (de)serialized using `JsonSerializer`/`JsonDeserializer`.

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-java-spring-boot-kafka/write-tests/)

----
url: https://docs.docker.com/scout/install/
----

# Install Docker Scout

***

Table of contents

***

The Docker Scout CLI plugin comes pre-installed with Docker Desktop.

If you run Docker Engine without Docker Desktop, Docker Scout doesn't come pre-installed, but you can install it as a standalone binary.

## [Installation script](#installation-script)

To install the latest version of the plugin, run the following commands:

```console
$ curl -fsSL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh -o install-scout.sh
$ sh install-scout.sh
```

> Note
>
> Always examine scripts downloaded from the internet before running them locally. Before installing, make yourself familiar with potential risks and limitations of the convenience script.

## [Manual installation](#manual-installation)

1. Download the latest release from the [releases page](https://github.com/docker/scout-cli/releases).

2. Create a subdirectory under `$HOME/.docker` called `scout`.

   ```console
   $ mkdir -p $HOME/.docker/scout
   ```

3. Extract the archive and move the `docker-scout` binary to the `$HOME/.docker/scout` directory.

4. Make the binary executable: `chmod +x $HOME/.docker/scout/docker-scout`.

5. Add the `scout` subdirectory to your `.docker/config.json` as a plugin directory:

   ```json
   {
     "cliPluginsExtraDirs": [
       "/home/USER/.docker/scout"
     ]
   }
   ```

   Substitute `<USER>` with your username on the system.

   > Note
   >
   > The path for `cliPluginsExtraDirs` must be an absolute path.

1) Download the latest release from the [releases page](https://github.com/docker/scout-cli/releases).

2) Create a subdirectory under `$HOME/.docker` called `scout`.

   ```console
   $ mkdir -p $HOME/.docker/scout
   ```

3) Extract the archive and move the `docker-scout` binary to the `$HOME/.docker/scout` directory.

4) Make the binary executable:

   ```console
   $ chmod +x $HOME/.docker/scout/docker-scout
   ```

5) Authorize the binary to be executable on macOS:

   ```console
   xattr -d com.apple.quarantine $HOME/.docker/scout/docker-scout
   ```

6) Add the `scout` subdirectory to your `.docker/config.json` as a plugin directory:

   ```json
   {
     "cliPluginsExtraDirs": [
       "/Users/USER/.docker/scout"
     ]
   }
   ```

   Substitute `<USER>` with your username on the system.

   > Note
   >
   > The path for `cliPluginsExtraDirs` must be an absolute path.

1. Download the latest release from the [releases page](https://github.com/docker/scout-cli/releases).

2. Create a subdirectory under `%USERPROFILE%/.docker` called `scout`.

   ```console
   % mkdir %USERPROFILE%\.docker\scout
   ```

3. Extract the archive and move the `docker-scout.exe` binary to the `%USERPROFILE%\.docker\scout` directory.

4. Add the `scout` subdirectory to your `.docker\config.json` as a plugin directory:

   ```json
   {
     "cliPluginsExtraDirs": [
       "C:\Users\USER\.docker\scout"
     ]
   }
   ```

   Substitute `<USER>` with your username on the system.

   > Note
   >
   > The path for `cliPluginsExtraDirs` must be an absolute path.

## [Container image](#container-image)

The Docker Scout CLI plugin is also available as a [container image](https://hub.docker.com/r/docker/scout-cli). Use the `docker/scout-cli` to run `docker scout` commands without installing the CLI plugin on your host.

```console
$ docker run -it \
  -e DOCKER_SCOUT_HUB_USER=<your Docker Hub user name> \
  -e DOCKER_SCOUT_HUB_PASSWORD=<your Docker Hub PAT>  \
  docker/scout-cli <command>
```

## [GitHub Action](#github-action)

The Docker Scout CLI plugin is also available as a [GitHub action](https://github.com/docker/scout-action). You can use it in your GitHub workflows to automatically analyze images and evaluate policy compliance with each push.

Docker Scout also integrates with many more CI/CD tools, such as Jenkins, GitLab, and Azure DevOps. Learn more about the [integrations](https://docs.docker.com/scout/integrations/) available for Docker Scout.

----
url: https://docs.docker.com/reference/cli/docker/network/
----

# docker network

***

| Description | Manage networks  |
| ----------- | ---------------- |
| Usage       | `docker network` |

## [Description](#description)

Manage networks. You can use subcommands to create, inspect, list, remove, prune, connect, and disconnect networks.

## [Subcommands](#subcommands)

| Command                                                                                         | Description                                          |
| ----------------------------------------------------------------------------------------------- | ---------------------------------------------------- |
| [`docker network connect`](https://docs.docker.com/reference/cli/docker/network/connect/)       | Connect a container to a network                     |
| [`docker network create`](https://docs.docker.com/reference/cli/docker/network/create/)         | Create a network                                     |
| [`docker network disconnect`](https://docs.docker.com/reference/cli/docker/network/disconnect/) | Disconnect a container from a network                |
| [`docker network inspect`](https://docs.docker.com/reference/cli/docker/network/inspect/)       | Display detailed information on one or more networks |
| [`docker network ls`](https://docs.docker.com/reference/cli/docker/network/ls/)                 | List networks                                        |
| [`docker network prune`](https://docs.docker.com/reference/cli/docker/network/prune/)           | Remove all unused networks                           |
| [`docker network rm`](https://docs.docker.com/reference/cli/docker/network/rm/)                 | Remove one or more networks                          |

----
url: https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard/
----

# Dashboard

***

Table of contents

***

## [User notifications](#user-notifications)

Toasts provide a brief notification to the user. They appear temporarily and shouldn't interrupt the user experience. They also don't require user input to disappear.

### [success](#success)

▸ **success**(`msg`): `void`

Use to display a toast message of type success.

```typescript
ddClient.desktopUI.toast.success("message");
```

### [warning](#warning)

▸ **warning**(`msg`): `void`

Use to display a toast message of type warning.

```typescript
ddClient.desktopUI.toast.warning("message");
```

### [error](#error)

▸ **error**(`msg`): `void`

Use to display a toast message of type error.

```typescript
ddClient.desktopUI.toast.error("message");
```

For more details about method parameters and the return types available, see [Toast API reference](https://docs.docker.com/reference/api/extensions-sdk/Toast/).

> Deprecated user notifications
>
> These methods are deprecated and will be removed in a future version. Use the methods specified above.

```typescript
window.ddClient.toastSuccess("message");
window.ddClient.toastWarning("message");
window.ddClient.toastError("message");
```

## [Open a file selection dialog](#open-a-file-selection-dialog)

This function opens a file selector dialog that asks the user to select a file or folder.

▸ **showOpenDialog**(`dialogProperties`): `Promise`< [`OpenDialogResult`](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)>:

The `dialogProperties` parameter is a list of flags passed to Electron to customize the dialog's behaviour. For example, you can pass `multiSelections` to allow a user to select multiple files. See [Electron's documentation](https://www.electronjs.org/docs/latest/api/dialog) for a full list.

```typescript
const result = await ddClient.desktopUI.dialog.showOpenDialog({
  properties: ["openDirectory"],
});
if (!result.canceled) {
  console.log(result.paths);
}
```

## [Open a URL](#open-a-url)

This function opens an external URL with the system default browser.

▸ **openExternal**(`url`): `void`

```typescript
ddClient.host.openExternal("https://docker.com");
```

> The URL must have the protocol `http` or `https`.

For more details about method parameters and the return types available, see [Desktop host API reference](https://docs.docker.com/reference/api/extensions-sdk/Host/).

> Deprecated external URL opening
>
> This method is deprecated and will be removed in a future version. Use the methods specified above.

```typescript
window.ddClient.openExternal("https://docker.com");
```

## [Navigation to Dashboard routes](#navigation-to-dashboard-routes)

From your extension, you can also [navigate](https://docs.docker.com/extensions/extensions-sdk/dev/api/dashboard-routes-navigation/) to other parts of the Docker Desktop Dashboard.

----
url: https://docs.docker.com/admin/company/manage/organizations/
----

# Manage company organizations

***

Table of contents

***

Subscription: Business

For: Administrators

Learn to manage the organizations in a company using the Docker Admin Console.

## [View all organizations](#view-all-organizations)

1. Sign in to the [Docker Home](https://app.docker.com) and choose your company.
2. Select **Admin Console**, then **Organizations**.

The **Organizations** view displays all organizations under your company.

## [Add seats to an organization](#add-seats-to-an-organization)

If you have a self-serve subscription that has no pending subscription changes, you can add seats using Docker Home. For more information about adding seats, see [Manage seats](https://docs.docker.com/admin/organization/manage/manage-seats/#add-seats-to-your-subscription).

If you have a sales-assisted subscription, you must contact Docker support or sales to add seats.

## [Add organizations to a company](#add-organizations-to-a-company)

To add an organization to a company, ensure the following:

* You are a company owner.
* You are an organization owner of the organization you want to add.
* The organization has a Docker Business subscription.
* There’s no limit to how many organizations can exist under a company.

> Important
>
> Once you add an organization to a company, you can't remove it from the company.

1. Sign in to [Docker Home](https://app.docker.com) and select your company from the top-left account drop-down.
2. Select **Admin Console**, then **Organizations**.
3. Select **Add organization**.
4. Choose the organization you want to add from the drop-down menu.
5. Select **Add organization** to confirm.

## [Manage an organization](#manage-an-organization)

1. Sign in to [Docker Home](https://app.docker.com) and select your company from the top-left account drop-down.
2. Select **Admin Console**, then **Organizations**.
3. Select the organization you want to manage.

For more details about managing an organization, see [Organization administration](https://docs.docker.com/admin/organization/).

## [More resources](#more-resources)

* [Video: Managing a company and nested organizations](https://youtu.be/XZ5_i6qiKho?feature=shared\&t=229)
* [Video: Adding nested organizations to a company](https://youtu.be/XZ5_i6qiKho?feature=shared\&t=454)

----
url: https://docs.docker.com/reference/cli/docker/model/df/
----

# docker model df

***

| Description | Show Docker Model Runner disk usage |
| ----------- | ----------------------------------- |
| Usage       | `docker model df`                   |

## [Description](#description)

Show Docker Model Runner disk usage

----
url: https://docs.docker.com/offload/quickstart/
----

# Docker Offload quickstart

***

Table of contents

***

Subscription: Docker Offload

Requires: Docker Desktop 4.68 or later

[Docker Offload](https://docs.docker.com/offload/about/) lets you build and run containers in the cloud while using your local Docker Desktop tools and workflow. This means faster builds, access to powerful cloud resources, and a seamless development experience.

This quickstart covers the steps developers need to get started with Docker Offload.

> Note
>
> If you're an organization owner, to get started you must [contact sales](https://www.docker.com/pricing/contact-sales/) and subscribe your organization to use Docker Offload. After subscribing, see [Manage Docker products](https://docs.docker.com/admin/organization/manage/manage-products/) to learn how to manage access for the developers in your organization.

## [Prerequisites](#prerequisites)

* You must have [Docker Desktop](/desktop/) installed. Docker recommends using the latest version of Docker Desktop to access the newest features and improvements in Docker Offload.
* You must have a Docker Business subscription and a Docker Offload subscription.

## [Step 1: Verify access to Docker Offload](#step-1-verify-access-to-docker-offload)

To access Docker Offload, you must be part of an organization that has subscribed to Docker Offload. As a developer, you can verify this by checking if the Docker Offload toggle appears in the Docker Desktop Dashboard header.

1. Start Docker Desktop and sign in.
2. In the Docker Desktop Dashboard header, look for the Docker Offload toggle.

If you see the Docker Offload toggle, you have access to Docker Offload and can proceed to the next step. If you don't see the Docker Offload toggle, check if Docker Offload is disabled in your [Docker Desktop settings](https://docs.docker.com/offload/configuration/), and then contact your administrator to verify that your organization has subscribed to Docker Offload and that they have enabled access for your organization.

## [Step 2: Start Docker Offload](#step-2-start-docker-offload)

You can start Docker Offload from the CLI or in the header of the Docker Desktop Dashboard. The following steps describe how to start Docker Offload using the CLI.

1. Start Docker Desktop and sign in.

2. Open a terminal and run the following command to start Docker Offload:

   ```console
   $ docker offload start
   ```

   > Tip
   >
   > To learn more about the Docker Offload CLI commands, see the [Docker Offload CLI reference](/reference/cli/docker/offload/).

3. If you are a member of multiple organizations that have access to Docker Offload, you have the option to select a profile. Your usage will be associated with the organization of the selected profile.

When Docker Offload is started, you'll see a cloud icon ( ) in the Docker Desktop Dashboard header, and the Docker Desktop Dashboard appears purple. You can run `docker offload status` in a terminal to check the status of Docker Offload.

## [Step 3: Run a container with Docker Offload](#step-3-run-a-container-with-docker-offload)

After starting Docker Offload, Docker Desktop connects to a secure cloud environment that mirrors your local experience. When you run builds or containers, they execute remotely, but behave just like local ones.

To verify that Docker Offload is working, run a container:

```console
$ docker run --rm hello-world
```

If Docker Offload is working, you'll see `Hello from Docker!` in the terminal output.

## [Step 4: Monitor your Offload session](#step-4-monitor-your-offload-session)

When Docker Offload is started and you have started session (for example, you've ran a container), then you can see current session duration estimate in the Docker Desktop Dashboard footer next to the hourglass icon ( ).

Also, when Docker Offload is started, you can view detailed session information by selecting **Docker Offload** > **Insights** in the left navigation of the Docker Desktop Dashboard.

## [Step 5: Stop Docker Offload](#step-5-stop-docker-offload)

Docker Offload automatically [idles](https://docs.docker.com/offload/about/#session-management-and-idle-state) if you do not respond to periodic prompts that appear in the Docker Desktop Dashboard. You can stop your Docker Offload session at any time. To stop Docker Offload:

```console
$ docker offload stop
```

When you stop Docker Offload, the cloud environment is terminated and all running containers and images are removed. When Docker Offload has been idle for 5 minutes, the environment is also terminated and all running containers and images are removed.

To start Docker Offload again, run the `docker offload start` command.

----
url: https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/run-tests/
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

You should see the Keycloak and PostgreSQL Docker containers start with the realm settings imported and the tests pass. After the tests finish, the containers stop and are removed automatically.

## [Summary](#summary)

The Testcontainers Keycloak module lets you develop and test applications using a real Keycloak server instead of mocks. Testing against a real OAuth 2.0 provider that mirrors your production setup gives you more confidence in your security configuration and token-based authentication flows.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Getting started with Testcontainers in a Java Spring Boot project](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)
* [Testcontainers Keycloak module](https://testcontainers.com/modules/keycloak/)
* [testcontainers-keycloak GitHub repository](https://github.com/dasniko/testcontainers-keycloak)
* [Spring Boot OAuth 2.0 Resource Server](https://docs.spring.io/spring-security/reference/servlet/oauth2/resource-server/index.html)

----
url: https://docs.docker.com/reference/cli/docker/compose/kill/
----

# docker compose kill

***

| Description | Force stop service containers                |
| ----------- | -------------------------------------------- |
| Usage       | `docker compose kill [OPTIONS] [SERVICE...]` |

## [Description](#description)

Forces running containers to stop by sending a `SIGKILL` signal. Optionally the signal can be passed, for example:

```console
$ docker compose kill -s SIGINT
```

## [Options](#options)

| Option             | Default   | Description                                                    |
| ------------------ | --------- | -------------------------------------------------------------- |
| `--remove-orphans` |           | Remove containers for services not defined in the Compose file |
| `-s, --signal`     | `SIGKILL` | SIGNAL to send to the container                                |

----
url: https://docs.docker.com/reference/cli/docker/desktop/logs/
----

# docker desktop logs

***

| Description | Print log entries for Docker Desktop |
| ----------- | ------------------------------------ |
| Usage       | `docker desktop logs [OPTIONS]`      |

## [Options](#options)

| Option             | Default         | Description                                                                                                                    |
| ------------------ | --------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `-b, --boot`       |                 | Show logs from a specified boot. Zero means the current or boot, one the second last boot, and so on                           |
| `-c, --color`      |                 | Enable colored output. Priority levels are highlighted.                                                                        |
| `-m, --color-mode` |                 | Color mode to use. Can be `default` or `priority`                                                                              |
| `-D, --directory`  |                 | Specifies a custom directory to search for log entries                                                                         |
| `-p, --priority`   | `%!s(int64=-1)` | Filter output by log priorities. `-1` is all, `0` is info or above, `1` filters for warnings or above, `2` filters for errors. |
| `-S, --since`      |                 | Start showing entries on or newer than the specified date and time. Uses the systemd.time(7) format.                           |
| `-u, --unit`       |                 | Filter by one or more categories (e.g. `--unit=com.docker.backend.ipc`, `com.docker.backend.apiproxy`)                         |
| `-U, --until`      |                 | Start showing entries on or before the specified date and time. Uses the systemd.time(7) format.                               |

----
url: https://docs.docker.com/guides/golang/configure-ci-cd/
----

# Configure CI/CD for your Go application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete the previous sections of this guide, starting with [Build your Go image](https://docs.docker.com/guides/golang/build-images/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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

[Test your Go deployment »](https://docs.docker.com/guides/golang/deploy/)

----
url: https://docs.docker.com/reference/cli/docker/debug/
----

# docker debug

***

| Description | Get a shell into any container or image. An alternative to debugging with \`docker exec\`. |
| ----------- | ------------------------------------------------------------------------------------------ |
| Usage       | `debug [OPTIONS] {CONTAINER\|IMAGE}`                                                       |

## [Description](#description)

Docker Debug is a CLI command that helps you follow best practices by keeping your images small and secure. With Docker Debug, you can debug your images while they contain the bare minimum to run your application. It does this by letting you create and work with slim images or containers that are often difficult to debug because all tools have been removed. For example, while typical debug approaches like `docker exec -it my-app bash` may not work on a slim container, `docker debug` will work.

With `docker debug` you can get a debug shell into any container or image, even if they don't contain a shell. You don't need to modify the image to use Docker Debug. However, using Docker Debug still won't modify your image. Docker Debug brings its own toolbox that you can easily customize. The toolbox comes with many standard Linux tools pre-installed, such as `vim`, `nano`, `htop`, and `curl`. Use the builtin `install` command to add additional tools available on <https://search.nixos.org/packages>. Docker Debug supports `bash`, `fish`, and `zsh`. By default it tries to auto-detect your shell.

Custom builtin tools:

* `install [tool1] [tool2]`: Add Nix packages from: <https://search.nixos.org/packages>, see [example](#managing-your-toolbox-using-the-install-command).
* `uninstall [tool1] [tool2]`: Uninstall Nix packages.
* `entrypoint`: Print, lint, or run the entrypoint, see [example](#understanding-the-default-startup-command-of-a-container-entry-points).
* `builtins`: Show custom builtin tools.

> Note
>
> For images and stopped containers, all changes are discarded when leaving the shell. At no point, do changes affect the actual image or container. When accessing running or paused containers, all filesystem changes are directly visible to the container. The `/nix` directory is never visible to the actual image or container.

## [Options](#options)

| Option          | Default | Description                                                                                                                                                    |
| --------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--shell`       | `auto`  | Select a shell. Supported: `bash`, `fish`, `zsh`, `auto`.                                                                                                      |
| `-c, --command` |         | Evaluate the specified commands instead of starting an interactive session, see [example](#running-commands-directly-eg-for-scripting).                        |
| `--host`        |         | Daemon docker socket to connect to. E.g.: `ssh://root@example.org`, `unix:///some/path/docker.sock`, see [example](#remote-debugging-using-the---host-option). |

## [Examples](#examples)

### [Debugging containers that have no shell (slim containers)](#debugging-containers-that-have-no-shell-slim-containers)

The `hello-world` image is very simple and only contains the `/hello` binary. It's a good example of a slim image. There are no other tools and no shell.

Run a container from the `hello-world` image:

```console
$ docker run --name my-app hello-world
```

The container exits immediately. To get a debug shell inside, run:

```console
$ docker debug my-app
```

The debug shell allows you to inspect the filesystem:

```console
docker > ls
dev  etc  hello  nix  proc  sys
```

The file `/hello` is the binary that was executed when running the container. You can confirm this by running it directly:

```console
docker > /hello
```

After running the binary, it produces the same output.

### [Debugging (slim) images](#debugging-slim-images)

You can debug images directly by running:

```console
$ docker debug hello-world
...
docker > ls
dev  etc  hello  nix  proc  sys
```

You don't even need to pull the image as `docker debug` will do this automatically like the `docker run` command.

### [Modifying files of a running container](#modifying-files-of-a-running-container)

Docker debug lets you modify files in any running container. The toolbox comes with `vim` and `nano` pre-installed.

Run an nginx container and change the default `index.html`:

```console
$ docker run -d --name web-app -p 8080:80 nginx
d3d6074d0ea901c96cac8e49e6dad21359616bef3dc0623b3c2dfa536c31dfdb
```

To confirm nginx is running, open a browser and navigate to http\://localhost:8080. You should see the default nginx page. Now, change it using vim:

```console
vim /usr/share/nginx/html/index.html
```

Change the title to "Welcome to my app!" and save the file. Now, reload the page in the browser and you should see the updated page.

### [Managing your toolbox using the `install` command](#managing-your-toolbox-using-the-install-command)

The builtin `install` command lets you add any tool from <https://search.nixos.org/packages> to the toolbox. Keep in mind adding a tool never modifies the actual image or container. Tools get added to only your toolbox. Run `docker debug` and then install `nmap`:

```console
$ docker debug nginx
...
docker > install nmap
Tip: You can install any package available at: https://search.nixos.org/packages.
installing 'nmap-7.93'
these 2 paths will be fetched (5.58 MiB download, 26.27 MiB unpacked):
/nix/store/brqjf4i23fagizaq2gn4d6z0f406d0kg-lua-5.3.6
/nix/store/xqd17rhgmn6pg85a3g18yqxpcya6d06r-nmap-7.93
copying path '/nix/store/brqjf4i23fagizaq2gn4d6z0f406d0kg-lua-5.3.6' from 'https://cache.nixos.org'...
copying path '/nix/store/xqd17rhgmn6pg85a3g18yqxpcya6d06r-nmap-7.93' from 'https://cache.nixos.org'...
building '/nix/store/k8xw5wwarh8dc1dvh5zx8rlwamxfsk3d-user-environment.drv'...

docker > nmap --version
Nmap version 7.93 ( https://nmap.org )
Platform: x86_64-unknown-linux-gnu
Compiled with: liblua-5.3.6 openssl-3.0.11 libssh2-1.11.0 nmap-libz-1.2.12 libpcre-8.45 libpcap-1.10.4 nmap-libdnet-1.12 ipv6
Compiled without:
Available nsock engines: epoll poll select
```

You can confirm `nmap` is now part of your toolbox by getting a debug shell into a different image:

```console
$ docker debug hello-world
...
docker > nmap --version

Nmap version 7.93 ( https://nmap.org )
Platform: x86_64-unknown-linux-gnu
Compiled with: liblua-5.3.6 openssl-3.0.11 libssh2-1.11.0 nmap-libz-1.2.12 libpcre-8.45 libpcap-1.10.4 nmap-libdnet-1.12 ipv6
Compiled without:
Available nsock engines: epoll poll select

docker > exit
```

`nmap` is still there.

### [Understanding the default startup command of a container (entry points)](#understanding-the-default-startup-command-of-a-container-entry-points)

Docker Debug comes with a builtin tool, `entrypoint`. Enter the `hello-world` image and confirm the entrypoint is `/hello`:

```console
$ docker debug hello-world
...
docker > entrypoint --print
/hello
```

The `entrypoint` command evaluates the `ENTRYPOINT` and `CMD` statement of the underlying image and lets you print, lint, or run the resulting entrypoint. However, it can be difficult to understand all the corner cases from [Understand how CMD and ENTRYPOINT interact](/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact). In these situations, `entrypoint` can help.

Use `entrypoint` to investigate what actually happens when you run a container from the Nginx image:

```console
$ docker debug nginx
...
docker > entrypoint
Understand how ENTRYPOINT/CMD work and if they are set correctly.
From CMD in Dockerfile:
 ['nginx', '-g', 'daemon off;']

From ENTRYPOINT in Dockerfile:
 ['/docker-entrypoint.sh']

By default, any container from this image will be started with following   command:

/docker-entrypoint.sh nginx -g daemon off;

path: /docker-entrypoint.sh
args: nginx -g daemon off;
cwd:
PATH: /usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

Lint results:
 PASS: '/docker-entrypoint.sh' found
 PASS: no mixing of shell and exec form
 PASS: no double use of shell form

Docs:
- https://docs.docker.com/reference/dockerfile/#cmd
- https://docs.docker.com/reference/dockerfile/#entrypoint
- https://docs.docker.com/reference/dockerfile/#understand-how-cmd-and-entrypoint-interact
```

The output tells you that on startup of the nginx image, a script `/docker-entrypoint.sh` is executed with the arguments `nginx -g daemon off;`. You can test the entrypoint by using the `--run` option:

```console
$ docker debug nginx
...
docker > entrypoint --run
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/01/19 17:34:39 [notice] 50#50: using the "epoll" event method
2024/01/19 17:34:39 [notice] 50#50: nginx/1.25.3
2024/01/19 17:34:39 [notice] 50#50: built by gcc 12.2.0 (Debian 12.2.0-14)
2024/01/19 17:34:39 [notice] 50#50: OS: Linux 5.15.133.1-microsoft-standard-WSL2
2024/01/19 17:34:39 [notice] 50#50: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/01/19 17:34:39 [notice] 50#50: start worker processes
2024/01/19 17:34:39 [notice] 50#50: start worker process 77
...
```

This starts nginx in your debug shell without having to actually run a container. You can shutdown nginx by pressing `Ctrl`+`C`.

### [Running commands directly (e.g., for scripting)](#running-commands-directly-eg-for-scripting)

Use the `--command` option to evaluate a command directly instead of starting an interactive session. For example, this is similar to `bash -c "arg1 arg2 ..."`. The following example runs the `cat` command in the nginx image without starting an interactive session.

```console
$ docker debug --command "cat /usr/share/nginx/html/index.html" nginx

<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### [Remote debugging using the --host option](#remote-debugging-using-the---host-option)

The following examples shows how to use the `--host` option. The first example uses SSH to connect to a remote Docker instance at `example.org` as the `root` user, and get a shell into the `my-container` container.

```console
$ docker debug --host ssh://root@example.org my-container
```

The following example connects to a different local Docker Engine, and gets a shell into the `my-container` container.

```console
$ docker debug --host=unix:///some/path/docker.sock my-container
```

----
url: https://docs.docker.com/compose/intro/compose-application-model/
----

# How Compose works

***

Table of contents

***

With Docker Compose you use a YAML configuration file, known as the [Compose file](#the-compose-file), to configure your application’s services, and then you create and start all the services from your configuration with the [Compose CLI](#cli).

The Compose file, or `compose.yaml` file, follows the rules provided by the [Compose Specification](https://docs.docker.com/reference/compose-file/) in how to define multi-container applications. This is the Docker Compose implementation of the formal [Compose Specification](https://github.com/compose-spec/compose-spec).

Computing components of an application are defined as [services](https://docs.docker.com/reference/compose-file/services/). A service is an abstract concept implemented on platforms by running the same container image, and configuration, one or more times.

Services communicate with each other through [networks](https://docs.docker.com/reference/compose-file/networks/). In the Compose Specification, a network is a platform capability abstraction to establish an IP route between containers within services connected together.

Services store and share persistent data into [volumes](https://docs.docker.com/reference/compose-file/volumes/). The Specification describes such a persistent data as a high-level filesystem mount with global options.

Some services require configuration data that is dependent on the runtime or platform. For this, the Specification defines a dedicated [configs](https://docs.docker.com/reference/compose-file/configs/) concept. From inside the container, configs behave like volumes—they’re mounted as files. However, configs are defined differently at the platform level.

A [secret](https://docs.docker.com/reference/compose-file/secrets/) is a specific flavor of configuration data for sensitive data that should not be exposed without security considerations. Secrets are made available to services as files mounted into their containers, but the platform-specific resources to provide sensitive data are specific enough to deserve a distinct concept and definition within the Compose Specification.

> Note
>
> With volumes, configs and secrets you can have a simple declaration at the top-level and then add more platform-specific information at the service level.

A project is an individual deployment of an application specification on a platform. A project's name, set with the top-level [`name`](https://docs.docker.com/reference/compose-file/version-and-name/) attribute, is used to group resources together and isolate them from other applications or other installation of the same Compose-specified application with distinct parameters. If you are creating resources on a platform, you must prefix resource names by project and set the label `com.docker.compose.project`.

Compose offers a way for you to set a custom project name and override this name, so that the same `compose.yaml` file can be deployed twice on the same infrastructure, without changes, by just passing a distinct name.

## [The Compose file](#the-compose-file)

The default path for a Compose file is `compose.yaml` (preferred) or `compose.yml` that is placed in the working directory. Compose also supports `docker-compose.yaml` and `docker-compose.yml` for backwards compatibility of earlier versions. If both files exist, Compose prefers the canonical `compose.yaml`.

You can use [fragments](https://docs.docker.com/reference/compose-file/fragments/) and [extensions](https://docs.docker.com/reference/compose-file/extension/) to keep your Compose file efficient and easy to maintain.

Multiple Compose files can be [merged](https://docs.docker.com/reference/compose-file/merge/) together to define the application model. The combination of YAML files is implemented by appending or overriding YAML elements based on the Compose file order you set. Simple attributes and maps get overridden by the highest order Compose file, lists get merged by appending. Relative paths are resolved based on the first Compose file's parent folder, whenever complementary files being merged are hosted in other folders. As some Compose file elements can both be expressed as single strings or complex objects, merges apply to the expanded form. For more information, see [Working with multiple Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/).

If you want to reuse other Compose files, or factor out parts of your application model into separate Compose files, you can also use [`include`](https://docs.docker.com/reference/compose-file/include/). This is useful if your Compose application is dependent on another application which is managed by a different team, or needs to be shared with others.

## [CLI](#cli)

The Docker CLI lets you interact with your Docker Compose applications through the `docker compose` command and its subcommands. If you're using Docker Desktop, the Docker Compose CLI is included by default.

Using the CLI, you can manage the lifecycle of your multi-container applications defined in the `compose.yaml` file. The CLI commands enable you to start, stop, and configure your applications effortlessly.

### [Key commands](#key-commands)

To start all the services defined in your `compose.yaml` file:

```console
$ docker compose up
```

To stop and remove the running services:

```console
$ docker compose down 
```

If you want to monitor the output of your running containers and debug issues, you can view the logs with:

```console
$ docker compose logs
```

To list all the services along with their current status:

```console
$ docker compose ps
```

For a full list of all the Compose CLI commands, see the [reference documentation](/reference/cli/docker/compose/).

## [Illustrative example](#illustrative-example)

The following example illustrates the Compose concepts outlined above. The example is non-normative.

Consider an application split into a frontend web application and a backend service.

The frontend is configured at runtime with an HTTP configuration file managed by infrastructure, providing an external domain name, and an HTTPS server certificate injected by the platform's secured secret store.

The backend stores data in a persistent volume.

Both services communicate with each other on an isolated back-tier network, while the frontend is also connected to a front-tier network and exposes port 443 for external usage.

The example application is composed of the following parts:

* Two services, backed by Docker images: `webapp` and `database`
* One secret (HTTPS certificate), injected into the frontend
* One configuration (HTTP), injected into the frontend
* One persistent volume, attached to the backend
* Two networks

```yml
services:
  frontend:
    image: example/webapp
    ports:
      - "443:8043"
    networks:
      - front-tier
      - back-tier
    configs:
      - httpd-config
    secrets:
      - server-certificate

  backend:
    image: example/database
    volumes:
      - db-data:/etc/data
    networks:
      - back-tier

volumes:
  db-data:
    driver: flocker
    driver_opts:
      size: "10GiB"

configs:
  httpd-config:
    external: true

secrets:
  server-certificate:
    external: true

networks:
  # The presence of these objects is sufficient to define them
  front-tier: {}
  back-tier: {}
```

The `docker compose up` command starts the `frontend` and `backend` services, creates the necessary networks and volumes, and injects the configuration and secret into the frontend service.

`docker compose ps` provides a snapshot of the current state of your services, making it easy to see which containers are running, their status, and the ports they are using:

```text
$ docker compose ps

NAME                IMAGE                COMMAND                  SERVICE             CREATED             STATUS              PORTS
example-frontend-1  example/webapp       "nginx -g 'daemon of…"   frontend            2 minutes ago       Up 2 minutes        0.0.0.0:443->8043/tcp
example-backend-1   example/database     "docker-entrypoint.s…"   backend             2 minutes ago       Up 2 minutes
```

## [What's next](#whats-next)

* [Try the Quickstart guide](https://docs.docker.com/compose/gettingstarted/)
* [Explore some sample applications](https://github.com/docker/awesome-compose)
* [Familiarize yourself with the Compose Specification](https://docs.docker.com/reference/compose-file/)

----
url: https://docs.docker.com/reference/cli/docker/scout/attestation/get/
----

# docker scout attestation get

***

| Description                                                               | Get attestation for image                             |
| ------------------------------------------------------------------------- | ----------------------------------------------------- |
| Usage                                                                     | `docker scout attestation get OPTIONS IMAGE [DIGEST]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker scout attest get`                             |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

The docker scout attestation get command gets attestations for images.

## [Options](#options)

| Option             | Default                                                    | Description                                                                                          |
| ------------------ | ---------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `--key`            | `https://registry.scout.docker.com/keyring/dhi/latest.pub` | Signature key to use for verification                                                                |
| `--org`            |                                                            | Namespace of the Docker organization                                                                 |
| `-o, --output`     |                                                            | Write the report to a file                                                                           |
| `--platform`       |                                                            | Platform of image to analyze                                                                         |
| `--predicate`      |                                                            | Get in-toto predicate only dropping the subject                                                      |
| `--predicate-type` |                                                            | Predicate-type for attestation                                                                       |
| `--ref`            |                                                            | Reference to use if the provided tarball contains multiple references. Can only be used with archive |
| `--skip-tlog`      |                                                            | Skip signature verification against public transaction log                                           |
| `--verify`         |                                                            | Verify the signature on the attestation                                                              |

----
url: https://docs.docker.com/reference/cli/sbx/logout/
----

# sbx logout

| Description | Stop all running sandboxes and sign out of Docker |
| ----------- | ------------------------------------------------- |
| Usage       | `sbx logout [flags]`                              |

## [Options](#options)

| Option      | Default | Description              |
| ----------- | ------- | ------------------------ |
| `-y, --yes` |         | Skip confirmation prompt |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/engine/extend/plugins_authorization/
----

# Access authorization plugin

***

Table of contents

***

This document describes the Docker Engine plugins available in Docker Engine. To view information on plugins managed by Docker Engine, refer to [Docker Engine plugin system](https://docs.docker.com/engine/extend/).

Docker's out-of-the-box authorization model is all or nothing. Any user with permission to access the Docker daemon can run any Docker client command. The same is true for callers using Docker's Engine API to contact the daemon. If you require greater access control, you can create authorization plugins and add them to your Docker daemon configuration. Using an authorization plugin, a Docker administrator can configure granular access policies for managing access to the Docker daemon.

Anyone with the appropriate skills can develop an authorization plugin. These skills, at their most basic, are knowledge of Docker, understanding of REST, and sound programming knowledge. This document describes the architecture, state, and methods information available to an authorization plugin developer.

## [Basic principles](#basic-principles)

Docker's [plugin infrastructure](https://docs.docker.com/engine/extend/plugin_api/) enables extending Docker by loading, removing and communicating with third-party components using a generic API. The access authorization subsystem was built using this mechanism.

Using this subsystem, you don't need to rebuild the Docker daemon to add an authorization plugin. You can add a plugin to an installed Docker daemon. You do need to restart the Docker daemon to add a new plugin.

An authorization plugin approves or denies requests to the Docker daemon based on both the current authentication context and the command context. The authentication context contains all user details and the authentication method. The command context contains all the relevant request data.

Authorization plugins must follow the rules described in [Docker Plugin API](https://docs.docker.com/engine/extend/plugin_api/). Each plugin must reside within directories described under the [Plugin discovery](https://docs.docker.com/engine/extend/plugin_api/#plugin-discovery) section.

> Note
>
> The abbreviations `AuthZ` and `AuthN` mean authorization and authentication respectively.

## [Default user authorization mechanism](#default-user-authorization-mechanism)

If TLS is enabled in the [Docker daemon](https://docs.docker.com/engine/security/https/), the default user authorization flow extracts the user details from the certificate subject name. That is, the `User` field is set to the client certificate subject common name, and the `AuthenticationMethod` field is set to `TLS`.

## [Basic architecture](#basic-architecture)

You are responsible for registering your plugin as part of the Docker daemon startup. You can install multiple plugins and chain them together. This chain can be ordered. Each request to the daemon passes in order through the chain. Only when all the plugins grant access to the resource, is the access granted.

When an HTTP request is made to the Docker daemon through the CLI or via the Engine API, the authentication subsystem passes the request to the installed authentication plugin(s). The request contains the user (caller) and command context. The plugin is responsible for deciding whether to allow or deny the request.

The sequence diagrams below depict an allow and deny authorization flow:

Each request sent to the plugin includes the authenticated user, the HTTP headers, and the request/response body. Only the user name and the authentication method used are passed to the plugin. Most importantly, no user credentials or tokens are passed.

> Note
>
> Authorization plugins enforce requests to the Docker daemon's HTTP API only. gRPC method calls, whether dispatched natively or upgraded through `POST /grpc`, are not subject to authorization. Furthermore, HTTP request/response bodies where the `Content-Type` is `application/json` are forwarded; bodies of any other type are not visible to the plugin and cannot be used for enforcement, even though the daemon acts on this data.

For commands that can potentially hijack the HTTP connection (`HTTP Upgrade`), such as `exec`, the authorization plugin is only called for the initial HTTP requests. Once the plugin approves the command, authorization is not applied to the rest of the flow. Specifically, the streaming data is not passed to the authorization plugins. For commands that return chunked HTTP response, such as `logs` and `events`, only the HTTP request is sent to the authorization plugins.

The Engine's authorization middleware fails closed: when a plugin returns an error or returns `Allow: false`, the request is denied and the error is surfaced to the client. Plugins should also fail closed: if the plugin cannot confidently evaluate a request, it should return an error or `Allow: false`.

### [Response body size and partial buffering](#response-body-size-and-partial-buffering)

The internal buffer that holds the response body between the daemon's HTTP handler and the plugin's response authorization callback (`responseModifier`, defined in [`pkg/authorization/response.go`](https://github.com/moby/moby/blob/master/pkg/authorization/response.go)) has a fixed capacity of 64 KiB (`maxBufferSize`).

For most non-streaming endpoints the full response is buffered for plugin inspection regardless of total size, because Go's `encoding/json` encoder serializes the complete payload into a single underlying write. The streaming-response exclusion noted above (for example, `logs` and `events`) is the practical effect of this 64 KiB threshold combined with the `io.WriteFlusher` write pattern used by streaming handlers, where each write is immediately drained to the client and is therefore no longer available for plugin inspection by the time the handler returns.

> Note
>
> Plugins that depend on `ResponseBody` inspection for redaction or content-filtering should restrict their policies to endpoints whose response is produced as a single write (typical of REST-style API responses). For commands whose responses are streamed or are likely to exceed the buffer through multiple writes, do not rely on `ResponseBody` for security-relevant decisions; perform the filtering in a separate layer in front of the daemon.

During request/response processing, some authorization flows might need to do additional queries to the Docker daemon. To complete such flows, plugins can call the daemon API similar to a regular user. To enable these additional queries, the plugin must provide the means for an administrator to configure proper authentication and security policies.

## [Docker client flows](#docker-client-flows)

To enable and configure the authorization plugin, the plugin developer must support the Docker client interactions detailed in this section.

### [Setting up Docker daemon](#setting-up-docker-daemon)

Enable the authorization plugin with a dedicated command line flag in the `--authorization-plugin=PLUGIN_ID` format. The flag supplies a `PLUGIN_ID` value. This value can be the plugin’s socket or a path to a specification file. Authorization plugins can be loaded without restarting the daemon. Refer to the [`dockerd` documentation](https://docs.docker.com/reference/cli/dockerd/#configuration-reload-behavior) for more information.

```console
$ dockerd --authorization-plugin=plugin1 --authorization-plugin=plugin2,...
```

Docker's authorization subsystem supports multiple `--authorization-plugin` parameters.

### [Calling authorized command (allow)](#calling-authorized-command-allow)

```console
$ docker pull centos
<...>
f1b10cd84249: Pull complete
<...>
```

### [Calling unauthorized command (deny)](#calling-unauthorized-command-deny)

```console
$ docker pull centos
<...>
docker: Error response from daemon: authorization denied by plugin PLUGIN_NAME: volumes are not allowed.
```

### [Error from plugins](#error-from-plugins)

```console
$ docker pull centos
<...>
docker: Error response from daemon: plugin PLUGIN_NAME failed with error: AuthZPlugin.AuthZReq: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.
```

## [API schema and implementation](#api-schema-and-implementation)

In addition to Docker's standard plugin registration method, each plugin should implement the following two methods:

* `/AuthZPlugin.AuthZReq` This authorize request method is called before the Docker daemon processes the client request.

* `/AuthZPlugin.AuthZRes` This authorize response method is called before the response is returned from Docker daemon to the client.

#### [/AuthZPlugin.AuthZReq](#authzpluginauthzreq)

Request

```json
{
    "User":              "The user identification",
    "UserAuthNMethod":   "The authentication method used",
    "RequestMethod":     "The HTTP method",
    "RequestURI":        "The HTTP request URI",
    "RequestBody":       "Byte array containing the raw HTTP request body",
    "RequestHeader":     "Byte array containing the raw HTTP request header as a map[string][]string "
}
```

Response

```json
{
    "Allow": "Determined whether the user is allowed or not",
    "Msg":   "The authorization message",
    "Err":   "The error message if things go wrong"
}
```

#### [/AuthZPlugin.AuthZRes](#authzpluginauthzres)

Request:

```json
{
    "User":              "The user identification",
    "UserAuthNMethod":   "The authentication method used",
    "RequestMethod":     "The HTTP method",
    "RequestURI":        "The HTTP request URI",
    "RequestBody":       "Byte array containing the raw HTTP request body",
    "RequestHeader":     "Byte array containing the raw HTTP request header as a map[string][]string",
    "ResponseBody":      "Byte array containing the raw HTTP response body",
    "ResponseHeader":    "Byte array containing the raw HTTP response header as a map[string][]string",
    "ResponseStatusCode":"Response status code"
}
```

Response:

```json
{
   "Allow":              "Determined whether the user is allowed or not",
   "Msg":                "The authorization message",
   "Err":                "The error message if things go wrong"
}
```

### [Request authorization](#request-authorization)

Each plugin must support two request authorization messages formats, one from the daemon to the plugin and then from the plugin to the daemon. The tables below detail the content expected in each message.

#### [Daemon -> Plugin](#daemon---plugin)

| Name                  | Type               | Description                                                                                      |
| --------------------- | ------------------ | ------------------------------------------------------------------------------------------------ |
| User                  | string             | The user identification                                                                          |
| Authentication method | string             | The authentication method used                                                                   |
| Request method        | enum               | The HTTP method (GET/DELETE/POST)                                                                |
| Request URI           | string             | The HTTP request URI including API version, as sent by the client (e.g., v.1.17/containers/json) |
| Request headers       | map\[string]string | Request headers as key value pairs (without the authorization header)                            |
| Request body          | \[]byte            | Raw request body                                                                                 |

#### [Plugin -> Daemon](#plugin---daemon)

| Name  | Type   | Description                                                                                                                                                                        |
| ----- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Allow | bool   | Boolean value indicating whether the request is allowed or denied                                                                                                                  |
| Msg   | string | Authorization message (will be returned to the client in case the access is denied)                                                                                                |
| Err   | string | Error message (will be returned to the client in case the plugin encounter an error. The string value supplied may appear in logs, so should not include confidential information) |

### [Response authorization](#response-authorization)

The plugin must support two authorization messages formats, one from the daemon to the plugin and then from the plugin to the daemon. The tables below detail the content expected in each message.

#### [Daemon -> Plugin](#daemon---plugin-1)

| Name                  | Type               | Description                                                                                      |
| --------------------- | ------------------ | ------------------------------------------------------------------------------------------------ |
| User                  | string             | The user identification                                                                          |
| Authentication method | string             | The authentication method used                                                                   |
| Request method        | string             | The HTTP method (GET/DELETE/POST)                                                                |
| Request URI           | string             | The HTTP request URI including API version, as sent by the client (e.g., v.1.17/containers/json) |
| Request headers       | map\[string]string | Request headers as key value pairs (without the authorization header)                            |
| Request body          | \[]byte            | Raw request body                                                                                 |
| Response status code  | int                | Status code from the Docker daemon                                                               |
| Response headers      | map\[string]string | Response headers as key value pairs                                                              |
| Response body         | \[]byte            | Raw Docker daemon response body                                                                  |

#### [Plugin -> Daemon](#plugin---daemon-1)

| Name  | Type   | Description                                                                                                                                                                        |
| ----- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Allow | bool   | Boolean value indicating whether the response is allowed or denied                                                                                                                 |
| Msg   | string | Authorization message (will be returned to the client in case the access is denied)                                                                                                |
| Err   | string | Error message (will be returned to the client in case the plugin encounter an error. The string value supplied may appear in logs, so should not include confidential information) |

----
url: https://docs.docker.com/accounts/deactivate-user-account/
----

# Deactivate a Docker account

***

Table of contents

***

Learn how to deactivate an individual Docker account, including prerequisites required for deactivation.

For information on deactivating an organization, see [Deactivating an organization](https://docs.docker.com/admin/organization/deactivate-account/).

> Warning
>
> All Docker products and services that use your Docker account are inaccessible after deactivating your account.

## [Prerequisites](#prerequisites)

Before deactivating your Docker account, ensure you meet the following requirements:

* If you are an organization or company owner, you must leave your organization or company before deactivating your Docker account:

  1. Sign in to [Docker Home](https://app.docker.com/admin) and choose your organization.
  2. Select **Members** and find your username.
  3. Select the **Actions** menu and then select **Leave organization**.

* If you are the sole owner of an organization, you must assign the owner role to another member of the organization and then remove yourself from the organization, or deactivate the organization. Similarly, if you are the sole owner of a company, either add someone else as a company owner and then remove yourself, or deactivate the company.

* If you have an active Docker subscription, [downgrade it to a Docker Personal subscription](https://docs.docker.com/subscription/change/).

* Download any images and tags you want to keep. Use `docker pull -a <image>` to pull all tags, or `docker pull <image>:<tag>` to pull a specific tag.

* If you linked a GitHub or Bitbucket account for automated builds, unlink it. See [Unlink a GitHub user account](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#unlink-a-github-user-account) or [Unlink a Bitbucket user account](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#unlink-a-bitbucket-user-account).

## [Deactivate](#deactivate)

Once you have completed all the previous steps, you can deactivate your account.

> Warning
>
> Deactivating your account is permanent and can't be undone. Make sure to back up any important data.

1. Sign in to [Docker Home](https://app.docker.com/login).
2. Select your avatar to open the drop-down menu.
3. Select **Account settings**.
4. Select **Deactivate**.
5. Select **Deactivate account**, then select again to confirm.

## [Delete personal data](#delete-personal-data)

Deactivating your account does not delete your personal data. To request personal data deletion, fill out Docker's [Privacy request form](https://preferences.docker.com/).

----
url: https://docs.docker.com/engine/manage-resources/labels/
----

# Docker object labels

***

Table of contents

***

Labels are a mechanism for applying metadata to Docker objects, including:

* Images
* Containers
* Local daemons
* Volumes
* Networks
* Swarm nodes
* Swarm services

You can use labels to organize your images, record licensing information, annotate relationships between containers, volumes, and networks, or in any way that makes sense for your business or application.

## [Label keys and values](#label-keys-and-values)

A label is a key-value pair, stored as a string. You can specify multiple labels for an object, but each key must be unique within an object. If the same key is given multiple values, the most-recently-written value overwrites all previous values.

### [Key format recommendations](#key-format-recommendations)

A label key is the left-hand side of the key-value pair. Keys are alphanumeric strings which may contain periods (`.`), underscores (`_`), slashes (`/`), and hyphens (`-`). Most Docker users use images created by other organizations, and the following guidelines help to prevent inadvertent duplication of labels across objects, especially if you plan to use labels as a mechanism for automation.

* Authors of third-party tools should prefix each label key with the reverse DNS notation of a domain they own, such as `com.example.some-label`.

* Don't use a domain in your label key without the domain owner's permission.

* The `com.docker.*`, `io.docker.*`, and `org.dockerproject.*` namespaces are reserved by Docker for internal use.

* Label keys should begin and end with a lower-case letter and should only contain lower-case alphanumeric characters, the period character (`.`), and the hyphen character (`-`). Consecutive periods or hyphens aren't allowed.

* The period character (`.`) separates namespace "fields". Label keys without namespaces are reserved for CLI use, allowing users of the CLI to interactively label Docker objects using shorter typing-friendly strings.

These guidelines aren't currently enforced and additional guidelines may apply to specific use cases.

### [Value guidelines](#value-guidelines)

Label values can contain any data type that can be represented as a string, including (but not limited to) JSON, XML, CSV, or YAML. The only requirement is that the value be serialized to a string first, using a mechanism specific to the type of structure. For instance, to serialize JSON into a string, you might use the `JSON.stringify()` JavaScript method.

Since Docker doesn't deserialize the value, you can't treat a JSON or XML document as a nested structure when querying or filtering by label value unless you build this functionality into third-party tooling.

## [Manage labels on objects](#manage-labels-on-objects)

Each type of object with support for labels has mechanisms for adding and managing them and using them as they relate to that type of object.

Labels on images, containers, local daemons, volumes, and networks are static for the lifetime of the object. To change these labels you must recreate the object. Labels on Swarm nodes and services can be updated dynamically.

### [Images](#images)

Add labels to images using the [`LABEL` instruction](https://docs.docker.com/reference/dockerfile/#label) in a Dockerfile:

```dockerfile
LABEL com.example.version="1.0"
LABEL com.example.description="Web application"
```

You can also set labels at build time with the `--label` flag, without needing a `LABEL` instruction in the Dockerfile:

```console
$ docker build --label "com.example.version=1.0" -t myapp .
```

Inspect labels on an image using `docker inspect`:

```console
$ docker inspect --format='{{json .Config.Labels}}' myapp
```

Filter images by label with [`docker image ls --filter`](/reference/cli/docker/image/ls/#filter):

```console
$ docker image ls --filter "label=com.example.version"
```

### [Containers](#containers)

Override or add labels when starting a container with [`docker run --label`](/reference/cli/docker/container/run/#label):

```console
$ docker run --label "com.example.env=prod" myapp
```

Inspect labels on a container:

```console
$ docker inspect --format='{{json .Config.Labels}}' mycontainer
```

Filter containers by label with [`docker container ls --filter`](/reference/cli/docker/container/ls/#filter):

```console
$ docker container ls --filter "label=com.example.env=prod"
```

### [Local Docker daemons](#local-docker-daemons)

Add labels to the Docker daemon by passing `--label` flags when starting `dockerd`, or by setting `"labels"` in the [daemon configuration file](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file):

```json
{
  "labels": ["com.example.environment=production"]
}
```

View daemon labels with `docker system info`.

### [Volumes](#volumes)

Add labels when [creating a volume](/reference/cli/docker/volume/create/):

```console
$ docker volume create --label "com.example.purpose=database" myvolume
```

Inspect volume labels:

```console
$ docker volume inspect myvolume --format='{{json .Labels}}'
```

Filter volumes by label with [`docker volume ls --filter`](/reference/cli/docker/volume/ls/#filter):

```console
$ docker volume ls --filter "label=com.example.purpose"
```

### [Networks](#networks)

Add labels when [creating a network](/reference/cli/docker/network/create/):

```console
$ docker network create --label "com.example.purpose=frontend" mynetwork
```

Inspect network labels:

```console
$ docker network inspect mynetwork --format='{{json .Labels}}'
```

Filter networks by label with [`docker network ls --filter`](/reference/cli/docker/network/ls/#filter):

```console
$ docker network ls --filter "label=com.example.purpose"
```

### [Swarm nodes](#swarm-nodes)

* [Adding or updating a Swarm node's labels](/reference/cli/docker/node/update/#label-add)
* [Filtering Swarm nodes by label](/reference/cli/docker/node/ls/#filter)

### [Swarm services](#swarm-services)

* [Adding labels when creating a Swarm service](/reference/cli/docker/service/create/#label)
* [Updating a Swarm service's labels](/reference/cli/docker/service/update/)
* [Filtering Swarm services by label](/reference/cli/docker/service/ls/#filter)

----
url: https://docs.docker.com/reference/cli/sbx/completion/fish/
----

# sbx completion fish

| Description | Generate the autocompletion script for fish |
| ----------- | ------------------------------------------- |
| Usage       | `sbx completion fish [flags]`               |

## [Description](#description)

Generate the autocompletion script for the fish shell.

To load completions in your current shell session:

```
sbx completion fish | source
```

To load completions for every new session, execute once:

```
sbx completion fish > ~/.config/fish/completions/sbx.fish
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
url: https://docs.docker.com/reference/api/engine/version/v1.44/
----

# Docker Engine API (1.44)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.44.yaml)

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

If you omit the version-prefix, the current version of the API (v1.44) is used. For example, calling `/info` is the same as calling `/v1.44/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

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

/v1.44/containers/json

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

/v1.44/containers/create

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

/v1.44/containers/{id}/json

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

/v1.44/containers/{id}/top

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

/v1.44/containers/{id}/logs

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

/v1.44/containers/{id}/changes

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

/v1.44/containers/{id}/export

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

/v1.44/containers/{id}/stats

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

/v1.44/containers/{id}/resize

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

/v1.44/containers/{id}/start

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

/v1.44/containers/{id}/stop

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

/v1.44/containers/{id}/restart

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

/v1.44/containers/{id}/kill

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

/v1.44/containers/{id}/update

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

/v1.44/containers/{id}/rename

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

/v1.44/containers/{id}/pause

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

/v1.44/containers/{id}/unpause

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

/v1.44/containers/{id}/attach

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

/v1.44/containers/{id}/attach/ws

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

/v1.44/containers/{id}/wait

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

/v1.44/containers/{id}

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

/v1.44/containers/{id}/archive

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

/v1.44/containers/{id}/archive

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

/v1.44/containers/{id}/archive

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

/v1.44/containers/prune

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

/v1.44/images/json

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

/v1.44/build

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

/v1.44/build/prune

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

/v1.44/images/create

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

/v1.44/images/{name}/json

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

/v1.44/images/{name}/history

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

/v1.44/images/{name}/push

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

/v1.44/images/{name}/tag

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

/v1.44/images/{name}

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

|              |                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| termrequired | stringTerm to search                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| limit        | integerMaximum number of results to return                                                                                                                                                                                                                                                                                                                                                                                                                            |
| filters      | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the images list. Available filters:- `is-automated=(true\|false)` (deprecated, see below)
- `is-official=(true\|false)`
- `stars=<number>` Matches images that has at least 'number' stars.The `is-automated` filter is deprecated. The `is_automated` field has been deprecated by Docker Hub's search API. Consequently, searching for `is-automated=true` will yield no results. |

### Responses

/v1.44/images/search

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

/v1.44/images/prune

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

/v1.44/commit

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

/v1.44/images/{name}/get

## [](#tag/Image/operation/ImageGetAll)Export several images

Get a tarball containing all images and metadata for several image repositories.

For each value of the `names` parameter: if it is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|       |                                          |
| ----- | ---------------------------------------- |
| names | Array of stringsImage names to filter by |

### Responses

/v1.44/images/get

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

/v1.44/images/load

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

/v1.44/networks

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

/v1.44/networks/{id}

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

/v1.44/networks/{id}

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

/v1.44/networks/create

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

/v1.44/networks/{id}/connect

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

/v1.44/networks/{id}/disconnect

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

/v1.44/networks/prune

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

/v1.44/volumes

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

/v1.44/volumes/create

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

/v1.44/volumes/{name}

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

/v1.44/volumes/{name}

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

/v1.44/volumes/{name}

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

/v1.44/volumes/prune

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

/v1.44/containers/{id}/exec

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

/v1.44/exec/{id}/start

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

/v1.44/exec/{id}/resize

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

/v1.44/exec/{id}/json

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

/v1.44/swarm

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

/v1.44/swarm/init

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

/v1.44/swarm/join

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

/v1.44/swarm/leave

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

/v1.44/swarm/update

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

/v1.44/swarm/unlockkey

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

/v1.44/swarm/unlock

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

/v1.44/nodes

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

/v1.44/nodes/{id}

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

/v1.44/nodes/{id}

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

/v1.44/nodes/{id}/update

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

/v1.44/services

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

/v1.44/services/create

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

/v1.44/services/{id}

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

/v1.44/services/{id}

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

/v1.44/services/{id}/update

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

/v1.44/services/{id}/logs

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

/v1.44/tasks

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

/v1.44/tasks/{id}

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

/v1.44/tasks/{id}/logs

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

/v1.44/secrets

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

/v1.44/secrets/create

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

/v1.44/secrets/{id}

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

/v1.44/secrets/{id}

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

/v1.44/secrets/{id}/update

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

/v1.44/configs

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

/v1.44/configs/create

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

/v1.44/configs/{id}

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

/v1.44/configs/{id}

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

/v1.44/configs/{id}/update

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

/v1.44/plugins

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

/v1.44/plugins/privileges

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

/v1.44/plugins/pull

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

/v1.44/plugins/{name}/json

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

/v1.44/plugins/{name}

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

/v1.44/plugins/{name}/enable

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

/v1.44/plugins/{name}/disable

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

/v1.44/plugins/{name}/upgrade

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

/v1.44/plugins/create

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

/v1.44/plugins/{name}/push

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

/v1.44/plugins/{name}/set

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

/v1.44/auth

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

/v1.44/info

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

/v1.44/version

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

/v1.44/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.44/\_ping

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

/v1.44/events

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

/v1.44/system/df

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

/v1.44/distribution/{name}/json

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

/v1.44/session

----
