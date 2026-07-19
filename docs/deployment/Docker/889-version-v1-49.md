url: https://docs.docker.com/reference/api/engine/version/v1.49/
----

# Docker Engine API (1.49)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.49.yaml)

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

If you omit the version-prefix, the current version of the API (v1.49) is used. For example, calling `/info` is the same as calling `/v1.49/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

Engine releases in the near future should support this version of the API, so your client will continue to work even if it is talking to a newer Engine.

The API uses an open schema model, which means the server may add extra properties to responses. Likewise, the server will ignore any extra query parameters and request body properties. When you write clients, you need to ignore additional properties in responses to ensure they do not break when talking to newer daemons.

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

/v1.49/containers/json

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
| User            | stringCommands run as this user inside the container. If omitted, commands run as the user specified in the image the container was started from.Can be either user-name or UID, and optional group-name or GID, separated by a colon (`<user-name\|UID>[<:group-name\|GID>]`).                       |
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

/v1.49/containers/create

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

/v1.49/containers/{id}/json

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Id": "aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf",
"Created": "2025-02-17T17:43:39.64001363Z",
"Path": "/bin/sh",
"Args": [
"-c",
"exit 9"
],
"State": {
"Status": "running",
"Running": true,
"Paused": false,
"Restarting": false,
"OOMKilled": false,
"Dead": false,
"Pid": 1234,
"ExitCode": 0,
"Error": "string",
"StartedAt": "2020-01-06T09:06:59.461876391Z",
"FinishedAt": "2020-01-06T09:07:59.461876391Z",
"Health": {
"Status": "healthy",
"FailingStreak": 0,
"Log": [
{
"Start": "2020-01-04T10:44:24.496525531Z",
"End": "2020-01-04T10:45:21.364524523Z",
"ExitCode": 0,
"Output": "string"
}
]
}
},
"Image": "sha256:72297848456d5d37d1262630108ab308d3e9ec7ed1c3286a32fe09856619a782",
"ResolvConfPath": "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/resolv.conf",
"HostnamePath": "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/hostname",
"HostsPath": "/var/lib/docker/containers/aa86eacfb3b3ed4cd362c1e88fc89a53908ad05fb3a4103bca3f9b28292d14bf/hosts",
"LogPath": "/var/lib/docker/containers/5b7c7e2b992aa426584ce6c47452756066be0e503a08b4516a433a54d2f69e59/5b7c7e2b992aa426584ce6c47452756066be0e503a08b4516a433a54d2f69e59-json.log",
"Name": "/funny_chatelet",
"RestartCount": 0,
"Driver": "overlayfs",
"Platform": "linux",
"ImageManifestDescriptor": {
"mediaType": "application/vnd.oci.image.manifest.v1+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 424,
"urls": [
"http://example.com"
],
"annotations": {
"com.docker.official-images.bashbrew.arch": "amd64",
"org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8",
"org.opencontainers.image.base.name": "scratch",
"org.opencontainers.image.created": "2025-01-27T00:00:00Z",
"org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79",
"org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base",
"org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu",
"org.opencontainers.image.version": "24.04"
},
"data": null,
"platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"artifactType": null
},
"MountLabel": "",
"ProcessLabel": "",
"AppArmorProfile": "",
"ExecIDs": [
"b35395de42bc8abd327f9dd65d913b9ba28c74d2f0734eeeae84fa1c616a0fca",
"3fc1232e5cd20c8de182ed81178503dc6437f4e7ef12b52cc5e8de020652f1c4"
],
"HostConfig": {
"CpuShares": 0,
"Memory": 0,
"CgroupParent": "string",
"BlkioWeight": 1000,
"BlkioWeightDevice": [
{
"Path": "string",
"Weight": 0
}
],
"BlkioDeviceReadBps": [
{
"Path": "string",
"Rate": 0
}
],
"BlkioDeviceWriteBps": [
{
"Path": "string",
"Rate": 0
}
],
"BlkioDeviceReadIOps": [
{
"Path": "string",
"Rate": 0
}
],
"BlkioDeviceWriteIOps": [
{
"Path": "string",
"Rate": 0
}
],
"CpuPeriod": 0,
"CpuQuota": 0,
"CpuRealtimePeriod": 0,
"CpuRealtimeRuntime": 0,
"CpusetCpus": "0-3",
"CpusetMems": "string",
"Devices": [
{
"PathOnHost": "/dev/deviceName",
"PathInContainer": "/dev/deviceName",
"CgroupPermissions": "mrw"
}
],
"DeviceCgroupRules": [
"c 13:* rwm"
],
"DeviceRequests": [
{
"Driver": "nvidia",
"Count": -1,
"DeviceIDs": [
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
"KernelMemoryTCP": 0,
"MemoryReservation": 0,
"MemorySwap": 0,
"MemorySwappiness": 100,
"NanoCpus": 0,
"OomKillDisable": true,
"Init": true,
"PidsLimit": 0,
"Ulimits": [
{
"Name": "string",
"Soft": 0,
"Hard": 0
}
],
"CpuCount": 0,
"CpuPercent": 0,
"IOMaximumIOps": 0,
"IOMaximumBandwidth": 0,
"Binds": [
"string"
],
"ContainerIDFile": "",
"LogConfig": {
"Type": "local",
"Config": {
"max-file": "5",
"max-size": "10m"
}
},
"NetworkMode": "string",
"PortBindings": {
"443/tcp": [
{
"HostIp": "127.0.0.1",
"HostPort": "4443"
}
],
"80/tcp": [
{
"HostIp": "0.0.0.0",
"HostPort": "80"
},
{
"HostIp": "0.0.0.0",
"HostPort": "8080"
}
],
"80/udp": [
{
"HostIp": "0.0.0.0",
"HostPort": "80"
}
],
"53/udp": [
{
"HostIp": "0.0.0.0",
"HostPort": "53"
}
],
"2377/tcp": null
},
"RestartPolicy": {
"Name": "",
"MaximumRetryCount": 0
},
"AutoRemove": true,
"VolumeDriver": "string",
"VolumesFrom": [
"string"
],
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
"ImageOptions": {
"Subpath": "dir-inside-image/subdirectory"
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
"ConsoleSize": [
80,
64
],
"Annotations": {
"property1": "string",
"property2": "string"
},
"CapAdd": [
"string"
],
"CapDrop": [
"string"
],
"CgroupnsMode": "private",
"Dns": [
"string"
],
"DnsOptions": [
"string"
],
"DnsSearch": [
"string"
],
"ExtraHosts": [
"string"
],
"GroupAdd": [
"string"
],
"IpcMode": "string",
"Cgroup": "string",
"Links": [
"string"
],
"OomScoreAdj": 500,
"PidMode": "string",
"Privileged": true,
"PublishAllPorts": true,
"ReadonlyRootfs": true,
"SecurityOpt": [
"string"
],
"StorageOpt": {
"property1": "string",
"property2": "string"
},
"Tmpfs": {
"property1": "string",
"property2": "string"
},
"UTSMode": "string",
"UsernsMode": "string",
"ShmSize": 0,
"Sysctls": {
"net.ipv4.ip_forward": "1"
},
"Runtime": "string",
"Isolation": "default",
"MaskedPaths": [
"/proc/asound",
"/proc/acpi",
"/proc/kcore",
"/proc/keys",
"/proc/latency_stats",
"/proc/timer_list",
"/proc/timer_stats",
"/proc/sched_debug",
"/proc/scsi",
"/sys/firmware",
"/sys/devices/virtual/powercap"
],
"ReadonlyPaths": [
"/proc/bus",
"/proc/fs",
"/proc/irq",
"/proc/sys",
"/proc/sysrq-trigger"
]
},
"GraphDriver": {
"Name": "overlay2",
"Data": {
"MergedDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/merged",
"UpperDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/diff",
"WorkDir": "/var/lib/docker/overlay2/ef749362d13333e65fc95c572eb525abbe0052e16e086cb64bc3b98ae9aa6d74/work"
}
},
"SizeRw": "122880",
"SizeRootFs": "1653948416",
"Mounts": [
{
"Type": "volume",
"Name": "myvolume",
"Source": "/var/lib/docker/volumes/myvolume/_data",
"Destination": "/usr/share/nginx/html/",
"Driver": "local",
"Mode": "z",
"RW": true,
"Propagation": ""
}
],
"Config": {
"Hostname": "439f4e91bd1d",
"Domainname": "string",
"User": "123:456",
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
"NetworkSettings": {
"Bridge": "docker0",
"SandboxID": "9d12daf2c33f5959c8bf90aa513e4f65b561738661003029ec84830cd503a0c3",
"HairpinMode": false,
"LinkLocalIPv6Address": "",
"LinkLocalIPv6PrefixLen": "",
"Ports": {
"443/tcp": [
{
"HostIp": "127.0.0.1",
"HostPort": "4443"
}
],
"80/tcp": [
{
"HostIp": "0.0.0.0",
"HostPort": "80"
},
{
"HostIp": "0.0.0.0",
"HostPort": "8080"
}
],
"80/udp": [
{
"HostIp": "0.0.0.0",
"HostPort": "80"
}
],
"53/udp": [
{
"HostIp": "0.0.0.0",
"HostPort": "53"
}
],
"2377/tcp": null
},
"SandboxKey": "/var/run/docker/netns/8ab54b426c38",
"SecondaryIPAddresses": [
{
"Addr": "string",
"PrefixLen": 0
}
],
"SecondaryIPv6Addresses": [
{
"Addr": "string",
"PrefixLen": 0
}
],
"EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b",
"Gateway": "172.17.0.1",
"GlobalIPv6Address": "2001:db8::5689",
"GlobalIPv6PrefixLen": 64,
"IPAddress": "172.17.0.4",
"IPPrefixLen": 16,
"IPv6Gateway": "2001:db8:2::100",
"MacAddress": "02:42:ac:11:00:04",
"Networks": {
"property1": {
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
"MacAddress": "02:42:ac:11:00:04",
"Aliases": [
"server_x",
"server_y"
],
"DriverOpts": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"GwPriority": [
10
],
"NetworkID": "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a",
"EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b",
"Gateway": "172.17.0.1",
"IPAddress": "172.17.0.4",
"IPPrefixLen": 16,
"IPv6Gateway": "2001:db8:2::100",
"GlobalIPv6Address": "2001:db8::5689",
"GlobalIPv6PrefixLen": 64,
"DNSNames": [
"foobar",
"server_x",
"server_y",
"my.ctr"
]
},
"property2": {
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
"MacAddress": "02:42:ac:11:00:04",
"Aliases": [
"server_x",
"server_y"
],
"DriverOpts": {
"com.example.some-label": "some-value",
"com.example.some-other-label": "some-other-value"
},
"GwPriority": [
10
],
"NetworkID": "08754567f1f40222263eab4102e1c733ae697e8e354aa9cd6e18d7402835292a",
"EndpointID": "b88f5b905aabf2893f3cbc4ee42d1ea7980bbc0a92e2c8922b1e1795298afb0b",
"Gateway": "172.17.0.1",
"IPAddress": "172.17.0.4",
"IPPrefixLen": 16,
"IPv6Gateway": "2001:db8:2::100",
"GlobalIPv6Address": "2001:db8::5689",
"GlobalIPv6PrefixLen": 64,
"DNSNames": [
"foobar",
"server_x",
"server_y",
"my.ctr"
]
}
}
}
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

/v1.49/containers/{id}/top

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Titles": {
"Titles": [
"UID",
"PID",
"PPID",
"C",
"STIME",
"TTY",
"TIME",
"CMD"
]
},
"Processes": {
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
}
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

/v1.49/containers/{id}/logs

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

/v1.49/containers/{id}/changes

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

/v1.49/containers/{id}/export

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

/v1.49/containers/{id}/stats

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"name": "boring_wozniak",
"id": "ede54ee1afda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c743",
"read": "2025-01-16T13:55:22.165243637Z",
"preread": "2025-01-16T13:55:21.160452595Z",
"pids_stats": {
"current": 5,
"limit": "18446744073709551615"
},
"blkio_stats": {
"io_service_bytes_recursive": [
{
"major": 254,
"minor": 0,
"op": "read",
"value": 7593984
},
{
"major": 254,
"minor": 0,
"op": "write",
"value": 100
}
],
"io_serviced_recursive": null,
"io_queue_recursive": null,
"io_service_time_recursive": null,
"io_wait_time_recursive": null,
"io_merged_recursive": null,
"io_time_recursive": null,
"sectors_recursive": null
},
"num_procs": 16,
"storage_stats": {
"read_count_normalized": 7593984,
"read_size_bytes": 7593984,
"write_count_normalized": 7593984,
"write_size_bytes": 7593984
},
"cpu_stats": {
"cpu_usage": {
"total_usage": 29912000,
"percpu_usage": [
29912000
],
"usage_in_kernelmode": 21994000,
"usage_in_usermode": 7918000
},
"system_cpu_usage": 5,
"online_cpus": 5,
"throttling_data": {
"periods": 0,
"throttled_periods": 0,
"throttled_time": 0
}
},
"precpu_stats": {
"cpu_usage": {
"total_usage": 29912000,
"percpu_usage": [
29912000
],
"usage_in_kernelmode": 21994000,
"usage_in_usermode": 7918000
},
"system_cpu_usage": 5,
"online_cpus": 5,
"throttling_data": {
"periods": 0,
"throttled_periods": 0,
"throttled_time": 0
}
},
"memory_stats": {
"usage": 0,
"max_usage": 0,
"stats": {
"active_anon": 1572864,
"active_file": 5115904,
"anon": 1572864,
"anon_thp": 0,
"file": 7626752,
"file_dirty": 0,
"file_mapped": 2723840,
"file_writeback": 0,
"inactive_anon": 0,
"inactive_file": 2510848,
"kernel_stack": 16384,
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
"slab_reclaimable": 725576,
"slab_unreclaimable": 455352,
"sock": 0,
"thp_collapse_alloc": 0,
"thp_fault_alloc": 1,
"unevictable": 0,
"workingset_activate": 0,
"workingset_nodereclaim": 0,
"workingset_refault": 0
},
"failcnt": 0,
"limit": 8217579520,
"commitbytes": 0,
"commitpeakbytes": 0,
"privateworkingset": 0
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

/v1.49/containers/{id}/resize

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

/v1.49/containers/{id}/start

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

/v1.49/containers/{id}/stop

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

/v1.49/containers/{id}/restart

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

/v1.49/containers/{id}/kill

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

/v1.49/containers/{id}/update

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
"Published ports are discarded when using host network mode"
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

/v1.49/containers/{id}/rename

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

/v1.49/containers/{id}/pause

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

/v1.49/containers/{id}/unpause

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

/v1.49/containers/{id}/attach

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

/v1.49/containers/{id}/attach/ws

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

/v1.49/containers/{id}/wait

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

/v1.49/containers/{id}

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

/v1.49/containers/{id}/archive

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

/v1.49/containers/{id}/archive

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

/v1.49/containers/{id}/archive

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

/v1.49/containers/prune

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

/v1.49/images/json

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
"mediaType": "application/vnd.oci.image.manifest.v1+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 424,
"urls": [
"http://example.com"
],
"annotations": {
"com.docker.official-images.bashbrew.arch": "amd64",
"org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8",
"org.opencontainers.image.base.name": "scratch",
"org.opencontainers.image.created": "2025-01-27T00:00:00Z",
"org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79",
"org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base",
"org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu",
"org.opencontainers.image.version": "24.04"
},
"data": null,
"platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"artifactType": null
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
],
"Descriptor": {
"mediaType": "application/vnd.oci.image.manifest.v1+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 424,
"urls": [
"http://example.com"
],
"annotations": {
"com.docker.official-images.bashbrew.arch": "amd64",
"org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8",
"org.opencontainers.image.base.name": "scratch",
"org.opencontainers.image.created": "2025-01-27T00:00:00Z",
"org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79",
"org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base",
"org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu",
"org.opencontainers.image.version": "24.04"
},
"data": null,
"platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"artifactType": null
}
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

/v1.49/build

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

|                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| keep-storage   | integer \<int64>Amount of disk space in bytes to keep for cache> **Deprecated**: This parameter is deprecated and has been renamed to "reserved-space". It is kept for backward compatibility and will be removed in API v1.52.                                                                                                                                                                                                                                          |
| reserved-space | integer \<int64>Amount of disk space in bytes to keep for cache                                                                                                                                                                                                                                                                                                                                                                                                          |
| max-used-space | integer \<int64>Maximum amount of disk space allowed to keep for cache                                                                                                                                                                                                                                                                                                                                                                                                   |
| min-free-space | integer \<int64>Target amount of free disk space after pruning                                                                                                                                                                                                                                                                                                                                                                                                           |
| all            | booleanRemove all types of build cache                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| filters        | stringA JSON encoded value of the filters (a `map[string][]string`) to process on the list of build cache objects.Available filters:- `until=<timestamp>` remove cache older than `<timestamp>`. The `<timestamp>` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. `10m`, `1h30m`) computed relative to the daemon's local time.
- `id=<id>`
- `parent=<id>`
- `type=<string>`
- `description=<string>`
- `inuse`
- `shared`
- `private` |

### Responses

/v1.49/build/prune

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
| fromImage | stringName of the image to pull. If the name includes a tag or digest, specific behavior applies:- If only `fromImage` includes a tag, that tag is used.
- If both `fromImage` and `tag` are provided, `tag` takes precedence.
- If `fromImage` includes a digest, the image is pulled by digest, and `tag` is ignored.
- If neither a tag nor digest is specified, all tags are pulled.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
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

/v1.49/images/create

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

##### query Parameters

|           |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| manifests | booleanDefault: falseInclude Manifests in the image summary.The `manifests` and `platform` options are mutually exclusive, and an error is produced if both are set.                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| platform  | stringJSON-encoded OCI platform to select the platform-variant. If omitted, it defaults to any locally available platform, prioritizing the daemon's host platform.If the daemon provides a multi-platform image store, this selects the platform-variant to show inspect. If the image is a single-platform image, or if the multi-platform image does not provide a variant matching the given platform, an error is returned.The `platform` and `manifests` options are mutually exclusive, and an error is produced if both are set.Example: `{"os": "linux", "architecture": "arm", "variant": "v5"}` |

### Responses

/v1.49/images/{name}/json

### Response samples

* 200
* 404
* 500

Content type

application/json

`{
"Id": "sha256:ec3f0931a6e6b6855d76b2d7b0be30e81860baccd891b2e243280bf1cd8ad710",
"Descriptor": {
"mediaType": "application/vnd.oci.image.manifest.v1+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 424,
"urls": [
"http://example.com"
],
"annotations": {
"com.docker.official-images.bashbrew.arch": "amd64",
"org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8",
"org.opencontainers.image.base.name": "scratch",
"org.opencontainers.image.created": "2025-01-27T00:00:00Z",
"org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79",
"org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base",
"org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu",
"org.opencontainers.image.version": "24.04"
},
"data": null,
"platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"artifactType": null
},
"Manifests": [
{
"ID": "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f",
"Descriptor": {
"mediaType": "application/vnd.oci.image.manifest.v1+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 424,
"urls": [
"http://example.com"
],
"annotations": {
"com.docker.official-images.bashbrew.arch": "amd64",
"org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8",
"org.opencontainers.image.base.name": "scratch",
"org.opencontainers.image.created": "2025-01-27T00:00:00Z",
"org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79",
"org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base",
"org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu",
"org.opencontainers.image.version": "24.04"
},
"data": null,
"platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"artifactType": null
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
],
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

##### query Parameters

|          |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| platform | stringJSON-encoded OCI platform to select the platform-variant. If omitted, it defaults to any locally available platform, prioritizing the daemon's host platform.If the daemon provides a multi-platform image store, this selects the platform-variant to show the history for. If the image is a single-platform image, or if the multi-platform image does not provide a variant matching the given platform, an error is returned.Example: `{"os": "linux", "architecture": "arm", "variant": "v5"}` |

### Responses

/v1.49/images/{name}/history

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

/v1.49/images/{name}/push

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

/v1.49/images/{name}/tag

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

/v1.49/images/{name}

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

/v1.49/images/search

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

/v1.49/images/prune

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
| User            | stringCommands run as this user inside the container. If omitted, commands run as the user specified in the image the container was started from.Can be either user-name or UID, and optional group-name or GID, separated by a colon (`<user-name\|UID>[<:group-name\|GID>]`).                       |
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

/v1.49/commit

### Request samples

* Payload

Content type

application/json

`{
"Hostname": "439f4e91bd1d",
"Domainname": "string",
"User": "123:456",
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

##### query Parameters

|          |                                                                                                                                                                                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| platform | stringJSON encoded OCI platform describing a platform which will be used to select a platform-specific image to be saved if the image is multi-platform. If not provided, the full multi-platform image will be saved.Example: `{"os": "linux", "architecture": "arm", "variant": "v5"}` |

### Responses

/v1.49/images/{name}/get

## [](#tag/Image/operation/ImageGetAll)Export several images

Get a tarball containing all images and metadata for several image repositories.

For each value of the `names` parameter: if it is a specific name and tag (e.g. `ubuntu:latest`), then only that image (and its parents) are returned; if it is an image ID, similarly only that image (and its parents) are returned and there would be no names referenced in the 'repositories' file for this image ID.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|          |                                                                                                                                                                                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| names    | Array of stringsImage names to filter by                                                                                                                                                                                                                                                 |
| platform | stringJSON encoded OCI platform describing a platform which will be used to select a platform-specific image to be saved if the image is multi-platform. If not provided, the full multi-platform image will be saved.Example: `{"os": "linux", "architecture": "arm", "variant": "v5"}` |

### Responses

/v1.49/images/get

## [](#tag/Image/operation/ImageLoad)Import images

Load a set of images and tags into a repository.

For details on the format, see the [export image endpoint](#operation/ImageGet).

##### query Parameters

|          |                                                                                                                                                                                                                                                                                          |
| -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| quiet    | booleanDefault: falseSuppress progress details during load.                                                                                                                                                                                                                              |
| platform | stringJSON encoded OCI platform describing a platform which will be used to select a platform-specific image to be load if the image is multi-platform. If not provided, the full multi-platform image will be loaded.Example: `{"os": "linux", "architecture": "arm", "variant": "v5"}` |

##### Request Body schema: application/x-tar

Tar archive containing images

string \<binary>

### Responses

/v1.49/images/load

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

/v1.49/networks

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

/v1.49/networks/{id}

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

/v1.49/networks/{id}

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
| EnableIPv4   | booleanEnable IPv4 on the network.                                                                                                                                                                                                     |
| EnableIPv6   | booleanEnable IPv6 on the network.                                                                                                                                                                                                     |
|              | objectNetwork specific options to be used by the drivers.                                                                                                                                                                              |
|              | objectUser-defined key/value metadata.                                                                                                                                                                                                 |

### Responses

/v1.49/networks/create

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

/v1.49/networks/{id}/connect

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
"MacAddress": "02:42:ac:12:05:02",
"Priority": 100
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

/v1.49/networks/{id}/disconnect

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

/v1.49/networks/prune

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

/v1.49/volumes

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

/v1.49/volumes/create

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

/v1.49/volumes/{name}

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

/v1.49/volumes/{name}

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

/v1.49/volumes/{name}

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

/v1.49/volumes/prune

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

/v1.49/containers/{id}/exec

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

/v1.49/exec/{id}/start

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

/v1.49/exec/{id}/resize

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

/v1.49/exec/{id}/json

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

/v1.49/swarm

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

/v1.49/swarm/init

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

/v1.49/swarm/join

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

/v1.49/swarm/leave

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

/v1.49/swarm/update

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

/v1.49/swarm/unlockkey

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

/v1.49/swarm/unlock

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

/v1.49/nodes

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

/v1.49/nodes/{id}

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

/v1.49/nodes/{id}

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

/v1.49/nodes/{id}/update

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

/v1.49/services

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

/v1.49/services/create

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
"ImageOptions": {
"Subpath": "dir-inside-image/subdirectory"
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

/v1.49/services/{id}

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

/v1.49/services/{id}

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

/v1.49/services/{id}/update

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
"ImageOptions": {
"Subpath": "dir-inside-image/subdirectory"
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

/v1.49/services/{id}/logs

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

/v1.49/tasks

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

/v1.49/tasks/{id}

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

/v1.49/tasks/{id}/logs

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

/v1.49/secrets

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

/v1.49/secrets/create

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

/v1.49/secrets/{id}

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

/v1.49/secrets/{id}

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

/v1.49/secrets/{id}/update

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

/v1.49/configs

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

/v1.49/configs/create

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

/v1.49/configs/{id}

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

/v1.49/configs/{id}

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

/v1.49/configs/{id}/update

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

/v1.49/plugins

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

/v1.49/plugins/privileges

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

/v1.49/plugins/pull

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

/v1.49/plugins/{name}/json

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

/v1.49/plugins/{name}

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

/v1.49/plugins/{name}/enable

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

/v1.49/plugins/{name}/disable

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

/v1.49/plugins/{name}/upgrade

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

/v1.49/plugins/create

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

/v1.49/plugins/{name}/push

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

/v1.49/plugins/{name}/set

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

/v1.49/auth

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

/v1.49/info

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
"BridgeNfIptables": false,
"BridgeNfIp6tables": false,
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
"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a"
},
"RuncCommit": {
"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a"
},
"InitCommit": {
"ID": "cfb82a876ecc11b5ca0977d1733adbe58599088a"
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
"FirewallBackend": {
"Driver": "nftables",
"Info": [ [
"ReloadedAt",
"2025-01-01T00:00:00Z"
]
]
},
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

/v1.49/version

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
"GoVersion": "go1.22.7",
"Os": "linux",
"Arch": "amd64",
"KernelVersion": "6.8.0-31-generic",
"Experimental": true,
"BuildTime": "2020-06-22T15:49:27.000000000+00:00"
}`

## [](#tag/System/operation/SystemPing)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.49/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.49/\_ping

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

/v1.49/events

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

/v1.49/system/df

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

/v1.49/distribution/{name}/json

### Response samples

* 200
* 401
* 500

Content type

application/json

`{
"Descriptor": {
"mediaType": "application/vnd.oci.image.manifest.v1+json",
"digest": "sha256:c0537ff6a5218ef531ece93d4984efc99bbf3f7497c0a7726c88e2bb7584dc96",
"size": 424,
"urls": [
"http://example.com"
],
"annotations": {
"com.docker.official-images.bashbrew.arch": "amd64",
"org.opencontainers.image.base.digest": "sha256:0d0ef5c914d3ea700147da1bd050c59edb8bb12ca312f3800b29d7c8087eabd8",
"org.opencontainers.image.base.name": "scratch",
"org.opencontainers.image.created": "2025-01-27T00:00:00Z",
"org.opencontainers.image.revision": "9fabb4bad5138435b01857e2fe9363e2dc5f6a79",
"org.opencontainers.image.source": "https://git.launchpad.net/cloud-images/+oci/ubuntu-base",
"org.opencontainers.image.url": "https://hub.docker.com/_/ubuntu",
"org.opencontainers.image.version": "24.04"
},
"data": null,
"platform": {
"architecture": "arm",
"os": "windows",
"os.version": "10.0.19041.1165",
"os.features": [
"win32k"
],
"variant": "v7"
},
"artifactType": null
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

/v1.49/session

----
url: https://docs.docker.com/guides/cpp/multistage/
----

# Create a multi-stage build for your C++ application

***

Table of contents

***

## [Prerequisites](#prerequisites)

* You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## [Overview](#overview)

This section walks you through creating a multi-stage Docker build for a C++ application. A multi-stage build is a Docker feature that allows you to use different base images for different stages of the build process, so you can optimize the size of your final image and separate build dependencies from runtime dependencies.

The standard practice for compiled languages like C++ is to have a build stage that compiles the code and a runtime stage that runs the compiled binary, because the build dependencies are not needed at runtime.

## [Get the sample application](#get-the-sample-application)

Let's use a simple C++ application that prints `Hello, World!` to the terminal. To do so, clone the sample repository to use with this guide:

```bash
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

The example for this section is under the `hello` directory in the repository. Get inside it and take a look at the files:

```bash
$ cd c-plus-plus-docker/hello
$ ls
```

You should see the following files:

```text
Dockerfile  hello.cpp
```

## [Check the Dockerfile](#check-the-dockerfile)

Open the `Dockerfile` in an IDE or text editor. The `Dockerfile` contains the instructions for building the Docker image.

```Dockerfile
# Stage 1: Build stage
FROM ubuntu:latest AS build

# Install build-essential for compiling C++ code
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Copy the source code into the container
COPY hello.cpp .

# Compile the C++ code statically to ensure it doesn't depend on runtime libraries
RUN g++ -o hello hello.cpp -static

# Stage 2: Runtime stage
FROM scratch

# Copy the static binary from the build stage
COPY --from=build /app/hello /hello

# Command to run the binary
CMD ["/hello"]
```

The `Dockerfile` has two stages:

1. **Build stage**: This stage uses the `ubuntu:latest` image to compile the C++ code and create a static binary.
2. **Runtime stage**: This stage uses the `scratch` image, which is an empty image, to copy the static binary from the build stage and run it.

## [Build the Docker image](#build-the-docker-image)

To build the Docker image, run the following command in the `hello` directory:

```bash
$ docker build -t hello .
```

The `-t` flag tags the image with the name `hello`.

## [Run the Docker container](#run-the-docker-container)

To run the Docker container, use the following command:

```bash
$ docker run hello
```

You should see the output `Hello, World!` in the terminal.

## [Summary](#summary)

In this section, you learned how to create a multi-stage build for a C++ application. Multi-stage builds help you optimize the size of your final image and separate build dependencies from runtime dependencies. In this example, the final image only contains the static binary and doesn't include any build dependencies.

As the image has an empty base, the usual OS tools are also absent. So, for example, you can't run a simple `ls` command in the container:

```bash
$ docker run hello ls
```

This makes the image very lightweight and secure.

[Containerize a C++ application »](https://docs.docker.com/guides/cpp/containerize/)

----
url: https://docs.docker.com/reference/cli/docker/container/export/
----

# docker container export

***

| Description                                                               | Export a container's filesystem as a tar archive |
| ------------------------------------------------------------------------- | ------------------------------------------------ |
| Usage                                                                     | `docker container export [OPTIONS] CONTAINER`    |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker export`                                  |

## [Description](#description)

The `docker export` command doesn't export the contents of volumes associated with the container. If a volume is mounted on top of an existing directory in the container, `docker export` exports the contents of the underlying directory, not the contents of the volume.

Refer to [Backup, restore, or migrate data volumes](/engine/storage/volumes/#back-up-restore-or-migrate-data-volumes) in the user guide for examples on exporting data in a volume.

## [Options](#options)

| Option         | Default | Description                        |
| -------------- | ------- | ---------------------------------- |
| `-o, --output` |         | Write to a file, instead of STDOUT |

## [Examples](#examples)

The following commands produce the same result.

```console
$ docker export red_panda > latest.tar
```

```console
$ docker export --output="latest.tar" red_panda
```

----
url: https://docs.docker.com/reference/cli/sbx/policy/log/
----

# sbx policy log

| Description | Show sandbox policy logs           |
| ----------- | ---------------------------------- |
| Usage       | `sbx policy log [SANDBOX] [flags]` |

## [Description](#description)

Show policy logs for all sandboxes, or filter by a specific sandbox name.

Displays which hosts were allowed or blocked by the proxy, along with the matching rule, proxy type, and request count. Useful for debugging connectivity issues or auditing network activity.

## [Options](#options)

| Option        | Default | Description                                             |
| ------------- | ------- | ------------------------------------------------------- |
| `--json`      |         | Output in JSON format                                   |
| `--limit`     | `0`     | Maximum number of log entries to show                   |
| `-q, --quiet` |         | Only display log entries                                |
| `--type`      | `all`   | Filter logs by type: "all" or "network" (default "all") |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Examples](#examples)

```console
# Show all policy logs
sbx policy log

# Show logs for a specific sandbox
sbx policy log my-sandbox

# Output in JSON format
sbx policy log --json

# Show the last 20 entries
sbx policy log --limit 20
```

----
url: https://docs.docker.com/build/buildkit/dockerfile-release-notes/
----

[Skip to content](#start-of-content)

You signed in with another tab or window. [Reload]() to refresh your session. You signed out in another tab or window. [Reload]() to refresh your session. You switched accounts on another tab or window. [Reload]() to refresh your session. Dismiss alert

[moby ](/moby)/ **[buildkit](/moby/buildkit)&#x20;**&#x50;ublic

* [Notifications ](/login?return_to=%2Fmoby%2Fbuildkit)You must be signed in to change notification settings
* [Fork 1.4k](/login?return_to=%2Fmoby%2Fbuildkit)
* [Star 10.1k](/login?return_to=%2Fmoby%2Fbuildkit)

# Releases: moby/buildkit

Releases · moby/buildkit

## v0.31.0

17 Jun 23:13

[github-actions](/apps/github-actions)

[v0.31.0](/moby/buildkit/tree/v0.31.0)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`c411f0a`](/moby/buildkit/commit/c411f0ac55a2c56d3d68b7d92d257538d5d6f464)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.31.0](/moby/buildkit/releases/tag/v0.31.0) [Latest](/moby/buildkit/releases/latest)

[Latest](/moby/buildkit/releases/latest)

buildkit 0.31.0

Welcome to the v0.31.0 release of buildkit!

Please try out the release binaries and report any issues at\
<https://github.com/moby/buildkit/issues>.

### Contributors

* Tõnis Tiigi
* CrazyMax
* Sebastiaan van Stijn
* Bjorn Neergaard
* Jonathan A. Sternberg
* Akihiro Suda
* Bryce Gibson
* Ava Barron
* Brian Goff
* Jiří Moravčík
* ZRHann
* Kevin NZUGUEM
* Maya Chen
* Natnael Gebremariam
* Sai Kiran Maggidi
* okhowang(王沛文)

### Notable Changes

* Built-in Dockerfile frontend has been updated to v1.25.0 [changelog](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.25.0)
* Exec steps now support a network proxy feature where all container traffic will be routed through an HTTP proxy server. This allows capturing the network traffic for inspection in build progress and provenance attestation. Source policies can define the requests that build containers are allowed to make and the ones that should be blocked. Network proxy can be enabled for the whole BuildKit daemon or enabled on a per-build basis. [#6858](https://github.com/moby/buildkit/pull/6858) [#6816](https://github.com/moby/buildkit/pull/6816) [#6740](https://github.com/moby/buildkit/pull/6740) [#6863](https://github.com/moby/buildkit/pull/6863)
* The local exporter now supports a `mode=delete` attribute which will replace the destination directory with the contents of the build result instead of merging it. Similar to the `--delete` flag in rsync. [#6561](https://github.com/moby/buildkit/pull/6561) [#6864](https://github.com/moby/buildkit/pull/6864)
* LLB APIs now support per-step resource limits for CPU and memory. [#6569](https://github.com/moby/buildkit/pull/6569)
* LLB APIs support a new Passthrough operation that allows defining dependency build graph branches that are required to be built but do not add any outputs to the final result. The `state.Requires()` client helper can be used to define such dependencies in the build graph. [#6829](https://github.com/moby/buildkit/pull/6829)
* All image results now default to using OCI media types. Previously this was applied based on whether annotations or attestations were needed. `oci-mediatypes=false` can be used for legacy Docker media types. This change raises the compatibility version of BuildKit v0.31.0 to 30. [#6824](https://github.com/moby/buildkit/pull/6824)
* Local cache exporter now supports the `reset` option to clear the unreferenced existing cache. [#6612](https://github.com/moby/buildkit/pull/6612)
* The local build result outputs now use a new implementation with better security guarantees in case the destination directory is mutated externally during the transfer. [#6561](https://github.com/moby/buildkit/pull/6561)
* New build metrics about build counts and durations have been added to the OTEL provider. [#6736](https://github.com/moby/buildkit/pull/6736)
* Parallel request limits for registry connections can now be set via configuration file. [#6776](https://github.com/moby/buildkit/pull/6776)
* In special modes where the client does not expose the session connection to transfer credentials, builds can now still fall back to anonymous registry auth instead of erroring. [#6760](https://github.com/moby/buildkit/pull/6760)
* Embedded binfmt emulators in the release image have been updated to QEMU v10.2.3. [#6846](https://github.com/moby/buildkit/pull/6846)
* Runc container runtime has been updated to v1.3.6
* Created attestations now use in-toto v1 statement format. [#6823](https://github.com/moby/buildkit/pull/6823)
* Due to the upgraded CLI library, the internal `buildctl` completion scripts flag `--generate-bash-completion` is no longer supported and has been replaced with `--generate-shell-completion`. [#6848](https://github.com/moby/buildkit/pull/6848)
* Fix an issue in default GC policy rules where the first rule for prioritizing releasing cache mounts and local sources did not apply. [#6856](https://github.com/moby/buildkit/pull/6856)
* Fix an issue where parent directories could be created with incorrect permissions due to system umask when using BuildKit embedded in Dockerd. [#6828](https://github.com/moby/buildkit/pull/6828)
* Fix possible segfault from race condition when HTTP server returned 401 error. [#6791](https://github.com/moby/buildkit/pull/6791)
* Fix source policy exact match rules losing the destination value during conversion. [#6861](https://github.com/moby/buildkit/pull/6861)
* Fix potential deadlock race conditions on stdin close. [#6810](https://github.com/moby/buildkit/pull/6810) [#6815](https://github.com/moby/buildkit/pull/6815)
* Fix premature ref release possibly causing "snapshot does not exist" error. [#6821](https://github.com/moby/buildkit/pull/6821)
* Fix OTLP shutdown stalling buildctl and buildkitd when the trace collector is unreachable. [#6757](https://github.com/moby/buildkit/pull/6757)
* Fix possible reference counting issues. [#6820](https://github.com/moby/buildkit/pull/6820)
* Fix possible hang in local progress writer. [#6811](https://github.com/moby/buildkit/pull/6811)
* Fix a data race when reading worker platform information. [#6867](https://github.com/moby/buildkit/pull/6867)
* Fix possible early release in case of cache computation error. [#6818](https://github.com/moby/buildkit/pull/6818)
* Improve stability of how runc kills build container processes. [#6779](https://github.com/moby/buildkit/pull/6779)

### Dependency Changes

* **github.com/Azure/azure-sdk-for-go/sdk/azcore** v1.21.0 -> v1.21.1
* **github.com/Azure/azure-sdk-for-go/sdk/internal** v1.11.2 -> v1.12.0
* **github.com/AzureAD/microsoft-authentication-library-for-go** v1.6.0 -> v1.7.0
* **github.com/aws/aws-sdk-go-v2** v1.41.7 -> v1.42.0
* **github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream** v1.7.8 -> v1.7.13
* **github.com/aws/aws-sdk-go-v2/config** v1.32.17 -> v1.32.24
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.16 -> v1.19.23
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.23 -> v1.18.29
* **github.com/aws/aws-sdk-go-v2/feature/s3/transfermanager** v0.2.9 ***new***
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.23 -> v1.4.29
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.23 -> v2.7.29
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.24 -> v1.4.30
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.9 -> v1.13.12
* **github.com/aws/aws-sdk-go-v2/service/internal/checksum** v1.9.12 -> v1.9.22
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.23 -> v1.13.29
* **github.com/aws/aws-sdk-go-v2/service/internal/s3shared** v1.19.20 -> v1.19.29
* **github.com/aws/aws-sdk-go-v2/service/s3** v1.89.1 -> v1.103.3
* **github.com/containerd/nydus-snapshotter** v0.15.13 -> v0.15.15
* **github.com/containerd/platforms** v1.0.0-rc.2 -> v1.0.0-rc.4
* **github.com/containerd/typeurl/v2** v2.2.3 -> v2.3.0
* **github.com/docker/cli** v29.4.3 -> v29.5.3
* **github.com/golang-jwt/jwt/v5** v5.3.0 -> v5.3.1
* **github.com/google/certificate-transparency-go** v1.3.2 -> v1.3.3
* **github.com/google/go-containerregistry** v0.20.7 -> v0.21.6
* **github.com/google/pprof** f64d9cf942d6 -> 545e8a4df936
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.28.0 -> v2.29.0
* **github.com/in-toto/attestation** v1.1.2 -> v1.2.0
* **github.com/moby/policy-helpers** a39d60132186 -> d5411a945cfc
* **github.com/moby/sys/mount** ...

[Read more](/moby/buildkit/releases/tag/v0.31.0)

Assets 42

* [buildkit-v0.31.0.darwin-amd64.provenance.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-amd64.provenance.json)

  sha256:6c5beb2fb7b89a961f9ecdc7b9c3d1d0424f3452d578136900f0689bf46e9f4c

  77 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-amd64.sbom.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-amd64.sbom.json)

  sha256:96973183b59690086870ce70ea80aec99efd3a5bc2fd69973eeacac8b14f9f2f

  152 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-amd64.sigstore.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-amd64.sigstore.json)

  sha256:47a8bec7e63a6119772774d08d31bf9cd054e7cc6591c2ae539e411d0250578e

  114 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-amd64.tar.gz](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-amd64.tar.gz)

  sha256:f4cd46317a48b4b8bbf28138ebdf541cb66f8e0e1cc6813f45518a6fae7689b6

  16.5 MB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-arm64.provenance.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-arm64.provenance.json)

  sha256:c5b298e8d2902d9fe06d298df33d62b9de3264c5f432d8582fab7830ca2295fc

  77 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-arm64.sbom.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-arm64.sbom.json)

  sha256:8ded981bf59376eaebd3edab005652d6120dc1e9226d8155899cf5562f9be10a

  152 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-arm64.sigstore.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-arm64.sigstore.json)

  sha256:b62dc44221131791469a093a53e661bd76822fd55e7cee6feebede95a51adc8d

  114 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.darwin-arm64.tar.gz](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.darwin-arm64.tar.gz)

  sha256:ce0e69ea070394ff4297401f8d8f66a2f76eab317e37821594009b674ba4c37f

  15.5 MB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.linux-amd64.provenance.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.linux-amd64.provenance.json)

  sha256:c984b82152c529cacbb88da5a32c7d6621bba816137ac2917c51ec1d187e574e

  144 KB 2026-06-17T19:01:08Z

* [buildkit-v0.31.0.linux-amd64.sbom.json](/moby/buildkit/releases/download/v0.31.0/buildkit-v0.31.0.linux-amd64.sbom.json)

  sha256:35d0cecb22ac87f9ceef92ba767b80cc01a1fe8508a5abe21108ef65e567429b

  667 KB 2026-06-17T19:01:08Z

* [Source code (zip)](/moby/buildkit/archive/refs/tags/v0.31.0.zip)

  2026-06-17T18:33:31Z

* [Source code (tar.gz)](/moby/buildkit/archive/refs/tags/v0.31.0.tar.gz)

  2026-06-17T18:33:31Z

* Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## dockerfile/1.25.0-labs

17 Jun 23:14

[github-actions](/apps/github-actions)

[dockerfile/1.25.0-labs](/moby/buildkit/tree/dockerfile/1.25.0-labs)

[`c411f0a`](/moby/buildkit/commit/c411f0ac55a2c56d3d68b7d92d257538d5d6f464)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[dockerfile/1.25.0-labs](/moby/buildkit/releases/tag/dockerfile%2F1.25.0-labs)

### Usage

```
# syntax=docker.io/docker/dockerfile-upstream:1.25.0-labs
```

Assets 2

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

## dockerfile/1.25.0

17 Jun 23:14

[github-actions](/apps/github-actions)

[dockerfile/1.25.0](/moby/buildkit/tree/dockerfile/1.25.0)

[`c411f0a`](/moby/buildkit/commit/c411f0ac55a2c56d3d68b7d92d257538d5d6f464)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[dockerfile/1.25.0](/moby/buildkit/releases/tag/dockerfile%2F1.25.0)

### Usage

```
# syntax=docker.io/docker/dockerfile-upstream:1.25.0
```

### Notable changes

* Resource limits for CPU and memory can now be set on build invocation and are applied to all `RUN` steps in the Dockerfile. Requires BuildKit v0.31.0+ [#6569](https://github.com/moby/buildkit/pull/6569)

Assets 2

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v0.31.0-rc2

12 Jun 12:08

[github-actions](/apps/github-actions)

[v0.31.0-rc2](/moby/buildkit/tree/v0.31.0-rc2)

This tag was signed with the committer’s **verified signature**.

[](/crazy-max)[crazy-max](/crazy-max) CrazyMax

GPG key ID: ADE44D8C9D44FBE4

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`d31ba4a`](/moby/buildkit/commit/d31ba4a7e79d1de97793201e7f012925ba7d6eeb)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.31.0-rc2](/moby/buildkit/releases/tag/v0.31.0-rc2) Pre-release

Pre-release

Welcome to the v0.31.0-rc2 release of buildkit!\
*This is a pre-release of buildkit*

Please try out the release binaries and report any issues at\
<https://github.com/moby/buildkit/issues>.

### Contributors

* CrazyMax
* Tõnis Tiigi
* ZRHann
* okhowang(王沛文)

### Notable Changes

* Local exports now detect whether multi-platform transfer support is available before using it. [#6864](https://github.com/moby/buildkit/pull/6864)
* Fix HTTPS and CNI networking regressions in the exec proxy feature. [#6862](https://github.com/moby/buildkit/pull/6862) [#6863](https://github.com/moby/buildkit/pull/6863)
* Fix source policy exact match rules losing the destination value during conversion. [#6861](https://github.com/moby/buildkit/pull/6861)
* Fix a data race when reading worker platform information. [#6867](https://github.com/moby/buildkit/pull/6867)

### Dependency Changes

* **github.com/Azure/azure-sdk-for-go/sdk/azcore** v1.21.0 -> v1.21.1
* **github.com/Azure/azure-sdk-for-go/sdk/internal** v1.11.2 -> v1.12.0
* **github.com/AzureAD/microsoft-authentication-library-for-go** v1.6.0 -> v1.7.0
* **github.com/golang-jwt/jwt/v5** v5.3.0 -> v5.3.1
* **github.com/google/certificate-transparency-go** v1.3.2 -> v1.3.3
* **github.com/google/go-containerregistry** v0.20.7 -> v0.21.6
* **github.com/google/pprof** f64d9cf942d6 -> 545e8a4df936
* **github.com/in-toto/attestation** v1.1.2 -> v1.2.0
* **github.com/moby/policy-helpers** a39d60132186 -> d5411a945cfc
* **github.com/prometheus/common** v0.66.1 -> v0.67.5
* **github.com/prometheus/otlptranslator** v0.0.2 -> v1.0.0
* **go.opentelemetry.io/otel/exporters/prometheus** v0.60.0 -> v0.65.0
* **google.golang.org/grpc/cmd/protoc-gen-go-grpc** v1.5.1 -> v1.6.1
* **k8s.io/klog/v2** v2.140.0 ***new***

Previous release can be found at [v0.31.0-rc1](https://github.com/moby/buildkit/releases/tag/v0.31.0-rc1)

Assets 42

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## dockerfile/1.25.0-rc2-labs

12 Jun 12:07

[github-actions](/apps/github-actions)

[dockerfile/1.25.0-rc2-labs](/moby/buildkit/tree/dockerfile/1.25.0-rc2-labs)

This tag was signed with the committer’s **verified signature**.

[](/crazy-max)[crazy-max](/crazy-max) CrazyMax

GPG key ID: ADE44D8C9D44FBE4

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`d31ba4a`](/moby/buildkit/commit/d31ba4a7e79d1de97793201e7f012925ba7d6eeb)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[dockerfile/1.25.0-rc2-labs](/moby/buildkit/releases/tag/dockerfile%2F1.25.0-rc2-labs) Pre-release

Pre-release

### Usage

```
# syntax=docker.io/docker/dockerfile-upstream:1.25.0-rc2-labs
```

Assets 2

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## dockerfile/1.25.0-rc2

12 Jun 12:07

[github-actions](/apps/github-actions)

[dockerfile/1.25.0-rc2](/moby/buildkit/tree/dockerfile/1.25.0-rc2)

This tag was signed with the committer’s **verified signature**.

[](/crazy-max)[crazy-max](/crazy-max) CrazyMax

GPG key ID: ADE44D8C9D44FBE4

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`d31ba4a`](/moby/buildkit/commit/d31ba4a7e79d1de97793201e7f012925ba7d6eeb)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[dockerfile/1.25.0-rc2](/moby/buildkit/releases/tag/dockerfile%2F1.25.0-rc2) Pre-release

Pre-release

### Usage

```
# syntax=docker.io/docker/dockerfile-upstream:1.25.0-rc2
```

Assets 2

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v0.31.0-rc1

11 Jun 00:09

[github-actions](/apps/github-actions)

[v0.31.0-rc1](/moby/buildkit/tree/v0.31.0-rc1)

This tag was signed with the committer’s **verified signature**. The key has expired.

[](/tonistiigi)[tonistiigi](/tonistiigi) Tõnis Tiigi

GPG key ID: AFA9DE5F8AB7AF39

Expired

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`e7b395c`](/moby/buildkit/commit/e7b395c2e142dfee4e7b280b32fc18870c8c98ed)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.31.0-rc1](/moby/buildkit/releases/tag/v0.31.0-rc1) Pre-release

Pre-release

buildkit 0.31.0-rc1

Welcome to the v0.31.0-rc1 release of buildkit!\
*This is a pre-release of buildkit*

Note

This release is missing the version tag in the filenames and `--version` output. This issue will be fixed by the next test release.

Please try out the release binaries and report any issues at\
<https://github.com/moby/buildkit/issues>.

### Contributors

* Tõnis Tiigi
* CrazyMax
* Sebastiaan van Stijn
* Bjorn Neergaard
* Jonathan A. Sternberg
* Bryce Gibson
* Akihiro Suda
* Ava Barron
* Brian Goff
* Jiří Moravčík
* Kevin NZUGUEM
* Maya Chen
* Natnael Gebremariam
* Sai Kiran Maggidi
* ZRHann

### Notable Changes

* Built-in Dockerfile frontend has been updated to v1.25.0-rc1 [changelog](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.25.0-rc1)
* The local exporter now supports a `mode=delete` attribute which will replace the destination directory with the contents of the build result instead of merging it. Similar to the `--delete` flag in rsync. [#6561](https://github.com/moby/buildkit/pull/6561)
* LLB APIs now support per-step resource limits for CPU and memory. [#6569](https://github.com/moby/buildkit/pull/6569)
* LLB APIs support a new Passthrough operation that allows defining dependency build graph branches that are required to be built but do not add any outputs to the final result. The `state.Requires()` client helper can be used to define such dependencies in the build graph. [#6829](https://github.com/moby/buildkit/pull/6829)
* All image results now default to using OCI media types. Previously, this was applied based on whether annotations or attestations were needed. `oci-mediatypes=false` can be used for legacy Docker media types. This change raises the compatibility version of BuildKit v0.31.0 to 30. [#6824](https://github.com/moby/buildkit/pull/6824)
* Exec steps now support a network proxy feature where all container traffic will be routed through an HTTP proxy server. This allows capturing the network traffic for inspection in build progress and provenance attestation. Source policies can define the requests that build containers are allowed to make and the ones that should be blocked. Network proxy can be enabled for the whole BuildKit daemon or enabled on a per-build basis. *There are some known issues with this feature in RC1, you might have better results testing with [this dev build](https://gist.github.com/tonistiigi/ced43318d7eaaea4a966de2ccff999ae)* [#6858](https://github.com/moby/buildkit/pull/6858) [#6816](https://github.com/moby/buildkit/pull/6816) [#6740](https://github.com/moby/buildkit/pull/6740)
* Local cache exporter now supports the `reset` option to clear the unreferenced existing cache. [#6612](https://github.com/moby/buildkit/pull/6612)
* The local build result outputs now use a new implementation with better security guarantees in case the destination directory is mutated externally during the transfer. [#6561](https://github.com/moby/buildkit/pull/6561)
* New build metrics about build counts and durations have been added to the OTEL provider. [#6736](https://github.com/moby/buildkit/pull/6736)
* Parallel request limits for registry connections can now be set via configuration file. [#6776](https://github.com/moby/buildkit/pull/6776)
* In special modes where the client does not expose the session connection to transfer credentials, builds can now still fall back to anonymous registry auth instead of erroring. [#6760](https://github.com/moby/buildkit/pull/6760)
* Embedded binfmt emulators in the release image have been updated to QEMU v10.2.3. [#6846](https://github.com/moby/buildkit/pull/6846)
* Created attestations now use in-toto v1 statement format. [#6823](https://github.com/moby/buildkit/pull/6823)
* Due to the upgraded CLI library, the internal `buildctl` completion scripts flag `--generate-bash-completion` is no longer supported and has been replaced with `--generate-shell-completion`. [#6848](https://github.com/moby/buildkit/pull/6848)
* Fix an issue in default GC policy rules where the first rule for prioritizing releasing cache mounts and local sources did not apply. [#6856](https://github.com/moby/buildkit/pull/6856)
* Fix an issue where parent directories could be created with incorrect permissions due to system umask when using BuildKit embedded in Dockerd. [#6828](https://github.com/moby/buildkit/pull/6828)
* Fix possible segfault from race condition when HTTP server returned 401 error. [#6791](https://github.com/moby/buildkit/pull/6791)
* Fix potential deadlock race conditions on stdin close. [#6810](https://github.com/moby/buildkit/pull/6810) [#6815](https://github.com/moby/buildkit/pull/6815)
* Fix premature ref release possibly causing "snapshot does not exist" error. [#6821](https://github.com/moby/buildkit/pull/6821)
* Fix OTLP shutdown stalling buildctl and buildkitd when the trace collector is unreachable. [#6757](https://github.com/moby/buildkit/pull/6757)
* Fix possible reference counting issues. [#6820](https://github.com/moby/buildkit/pull/6820)
* Fix possible hang in local progress writer. [#6811](https://github.com/moby/buildkit/pull/6811)
* Fix possible early release in case of cache computation error. [#6818](https://github.com/moby/buildkit/pull/6818)
* Improve stability of how runc kills build container processes. [#6779](https://github.com/moby/buildkit/pull/6779)

### Dependency Changes

* **github.com/aws/aws-sdk-go-v2** v1.41.7 -> v1.42.0
* **github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream** v1.7.8 -> v1.7.13
* **github.com/aws/aws-sdk-go-v2/config** v1.32.17 -> v1.32.24
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.16 -> v1.19.23
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.23 -> v1.18.29
* **github.com/aws/aws-sdk-go-v2/feature/s3/transfermanager** v0.2.9 ***new***
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.23 -> v1.4.29
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.23 -> v2.7.29
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.24 -> v1.4.30
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.9 -> v1.13.12
* **github.com/aws/aws-sdk-go-v2/service/internal/checksum** v1.9.12 -> v1.9.22
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.23 -> v1.13.29
* **github.com/aws/aws-sdk-go-v2/service/internal/s3shared** v1.19.20 -> v1.19.29
* **github.com/aws/aws-sdk-go-v2/service/s3** v1.89.1 -> v1.103.3
* **github.com/containerd/nydus-snapshotter** v0.15.13 -> v0.15.15
* **github.com/containerd/platforms** v1.0.0-rc.2 -> v1.0.0-rc.4
* **github.com/containerd/typeurl/v2** v2.2.3 -> v2.3.0
* **github.com/docker/cli** v29.4.3 -> v29.5.3
* **github.com/docker/docker-credential-helpers** v0.9.5 -> v0.9.8
* **github.com/grpc-ecosystem/grpc-gateway/v2** v2.28.0 -> v2.29.0
* **github.com/moby/sys/mount** v0.3.4 -> fc52b7222d0b
* **github.com/moby/sys/sequential** v0.6.0 -> v0.7.0
* **github.com/opencontainers/selinux** v1.13.1 -> v1.15.1
* **github.com/pelletier/go-toml/v2** v2.2.4 -> v2.3.1
* **github.com/tonistiigi/fsutil** a2aa163d723f -> 0257b3308df4
* **github.com/urfave/cli/v3** v3.9.0 ***new***
* **github.com/vbatts/tar-split** v0.12.2 -> v0.12.3
* **golang.org/x/exp** df9299821621 -> 055de637280b
* **google.golang.org/genproto/googleapis/api** 6f92a3bedf2d -> 3dc84a4a5aaa
* **google.golang.org/genproto/googleapis/rpc** 6f92a3bedf2d -> 3dc84a4a5aaa
* **google.golang.org/grpc** v1.80.0 -> v1.81.1

Previous release can be found at [v0.30.0](https://github.com/moby/buildkit/releases/tag/v0.30.0)

Assets 42

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## dockerfile/1.25.0-rc1-labs

11 Jun 00:10

[github-actions](/apps/github-actions)

[dockerfile/1.25.0-rc1-labs](/moby/buildkit/tree/dockerfile/1.25.0-rc1-labs)

[`e7b395c`](/moby/buildkit/commit/e7b395c2e142dfee4e7b280b32fc18870c8c98ed)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[dockerfile/1.25.0-rc1-labs](/moby/buildkit/releases/tag/dockerfile%2F1.25.0-rc1-labs) Pre-release

Pre-release

### Usage

```
# syntax=docker.io/docker/dockerfile-upstream:1.25.0-rc1-labs
```

Assets 2

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

1 person reacted

## dockerfile/1.25.0-rc1

11 Jun 00:10

[github-actions](/apps/github-actions)

[dockerfile/1.25.0-rc1](/moby/buildkit/tree/dockerfile/1.25.0-rc1)

[`e7b395c`](/moby/buildkit/commit/e7b395c2e142dfee4e7b280b32fc18870c8c98ed)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[dockerfile/1.25.0-rc1](/moby/buildkit/releases/tag/dockerfile%2F1.25.0-rc1) Pre-release

Pre-release

### Usage

```
# syntax=docker.io/docker/dockerfile-upstream:1.25.0-rc1
```

### Notable changes

* Resource limits for CPU and memory can now be set on build invocation and are applied to all `RUN` steps in the Dockerfile. Requires BuildKit v0.31.0+ [#6569](https://github.com/moby/buildkit/pull/6569)

Assets 2

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

## v0.30.0

13 May 13:16

[github-actions](/apps/github-actions)

[v0.30.0](/moby/buildkit/tree/v0.30.0)

This tag was signed with the committer’s **verified signature**.

[](/crazy-max)[crazy-max](/crazy-max) CrazyMax

GPG key ID: ADE44D8C9D44FBE4

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[`dd2170e`](/moby/buildkit/commit/dd2170e156c9633da1b2d1a58a6188e3f7d36fa4)

This commit was created on GitHub.com and signed with GitHub’s **verified signature**.

GPG key ID: B5690EEEBB952194

Verified

[Learn about vigilant mode](https://docs.github.com/github/authenticating-to-github/displaying-verification-statuses-for-all-of-your-commits).

[v0.30.0](/moby/buildkit/releases/tag/v0.30.0)

Welcome to the v0.30.0 release of buildkit!

Please try out the release binaries and report any issues at\
<https://github.com/moby/buildkit/issues>.

### Contributors

* Tõnis Tiigi
* CrazyMax
* Sebastiaan van Stijn
* Jonathan A. Sternberg
* Natnael Gebremariam
* Akihiro Suda
* Dawei Wei
* Dmitrii Kostyrev
* Jiří Moravčík
* Vladimir Kuznichenkov

### Notable Changes

* Builtin Dockerfile frontend has been updated to v1.24.0 [changelog](https://github.com/moby/buildkit/releases/tag/dockerfile%2F1.24.0)
* BuildKit now supports the concept of "compatibility version" for improved reproducible builds support across different BuildKit versions. This allows users to specify a version for which the build should be compatible with, and BuildKit will attempt to maintain compatibility with that version when possible. Compatibility version will be stored in the provenance attestation of the build and can be used to independently verify the artifacts of the build on other BuildKit versions. The current compatibility version and backward compatibility with old versions are defined in [Build reproducibility docs](https://github.com/moby/buildkit/blob/v0.30.0-rc1/docs/build-repro.md#compatibility-version) [#6681](https://github.com/moby/buildkit/pull/6681)
* Git sources now support `fetch-by-commit` option where commit is fetched by the SHA and then associated with the reference. This is useful when checking out mutable references `refs/NR/merge` where the commit SHA may change during invocation and cause checksum mismatch error [#6708](https://github.com/moby/buildkit/pull/6708)
* The LLB API now supports Git bundle format. Git bundles can be loaded from registry or OCI layout blobs and Git sources can be checked out into bundle format for snapshotting [#6711](https://github.com/moby/buildkit/pull/6711)
* Provenance attestations for multi-pass or chained builds now include request details for root requests and individual input requests, allowing full reconstruction of such complex builds [#6739](https://github.com/moby/buildkit/pull/6739)
* The version of the built-in Dockerfile frontend that was used is now included in the provenance metadata and reported via worker info APIs. [#6705](https://github.com/moby/buildkit/pull/6705)
* Improve error reporting for registry errors on cache export [#6762](https://github.com/moby/buildkit/pull/6762)
* S3 cache now supports additional options `retry_mode` and `retry_max_attempts` to configure retry behavior of S3 client [#6657](https://github.com/moby/buildkit/pull/6657)
* S3 cache now supports `disable_accept_encoding` option for GCS interoperability [#6642](https://github.com/moby/buildkit/pull/6642)
* Reduce potential lock contention in gateway forwarder for improved performance on parallel builds [#6741](https://github.com/moby/buildkit/pull/6741)
* A new log level option has been added to the buildkitd TOML configuration; previous "debug" and "trace" options have been deprecated [#6732](https://github.com/moby/buildkit/pull/6732)
* Allow gateway frontend requests to forward to the built-in Dockerfile frontend the same way as to external frontends [#6643](https://github.com/moby/buildkit/pull/6643)
* Session connection health checks have been improved to better detect loss of connectivity and avoid stuck builds [#6649](https://github.com/moby/buildkit/pull/6649)
* Fix issue with Git subdirectory value not being included in ConfigSource section of SLSA provenance for builds from Git sources [#6724](https://github.com/moby/buildkit/pull/6724)
* Avoid potential deadlock if the credential helper in the client is misbehaving and never returns credentials [#6709](https://github.com/moby/buildkit/pull/6709)
* Fix possible data race in provenance computation on parallel builds [#6758](https://github.com/moby/buildkit/pull/6758)
* Fix possible provenance capture race in concurrent no-cache builds that could leave source pins empty and fail with an invalid checksum digest error [#6764](https://github.com/moby/buildkit/pull/6764)
* Fix possible data race in progress writer [#6679](https://github.com/moby/buildkit/pull/6679)
* Fix data race in S3 cache reader [#6675](https://github.com/moby/buildkit/pull/6675)
* Fix possible Git config lookup errors on Windows [#6639](https://github.com/moby/buildkit/pull/6639)
* Fix build cancellation not working properly when blocked on credential callback [#6641](https://github.com/moby/buildkit/pull/6641)

### Dependency Changes

* **github.com/Azure/azure-sdk-for-go/sdk/azcore** v1.20.0 -> v1.21.0
* **github.com/Microsoft/hcsshim** v0.14.0-rc.1 -> v0.14.1
* **github.com/aws/aws-sdk-go-v2** v1.41.4 -> v1.41.7
* **github.com/aws/aws-sdk-go-v2/aws/protocol/eventstream** v1.7.5 -> v1.7.8
* **github.com/aws/aws-sdk-go-v2/config** v1.32.12 -> v1.32.17
* **github.com/aws/aws-sdk-go-v2/credentials** v1.19.12 -> v1.19.16
* **github.com/aws/aws-sdk-go-v2/feature/ec2/imds** v1.18.20 -> v1.18.23
* **github.com/aws/aws-sdk-go-v2/internal/configsources** v1.4.20 -> v1.4.23
* **github.com/aws/aws-sdk-go-v2/internal/endpoints/v2** v2.7.20 -> v2.7.23
* **github.com/aws/aws-sdk-go-v2/internal/v4a** v1.4.12 -> v1.4.24
* **github.com/aws/aws-sdk-go-v2/service/internal/accept-encoding** v1.13.7 -> v1.13.9
* **github.com/aws/aws-sdk-go-v2/service/internal/checksum** v1.9.3 -> v1.9.12
* **github.com/aws/aws-sdk-go-v2/service/internal/presigned-url** v1.13.20 -> v1.13.23
* **github.com/aws/aws-sdk-go-v2/service/internal/s3shared** v1.19.12 -> v1.19.20
* **github.com/aws/aws-sdk-go-v2/service/signin** v1.0.8 -> v1.0.11
* **github.com/aws/aws-sdk-go-v2/service/sso** v1.30.13 -> v1.30.17
* **github.com/aws/aws-sdk-go-v2/service/ssooidc** v1.35.17 -> v1.35.21
* **github.com/aws/aws-sdk-go-v2/service/sts** v1.41.9 -> v1.42.1
* **github.com/aws/smithy-go** v1.24.2 -> v1.25.1
* **github.com/containerd/containerd/v2** v2.2.2 -> v2.2.3
* **github.com/docker/cli** v29.3.1 -> v29.4.3
* **github.com/moby/policy-helpers** b7c0b994300b -> a39d60132186
* **github.com/moby/profiles/seccomp** v0.1.0 -> v0.2.3
* **go.opentelemetry.io/otel/metric** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/sdk** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/sdk/metric** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/otel/trace** v1.40.0 -> v1.43.0
* **go.opentelemetry.io/proto/otlp** v1.9.0 -> v1.10.0
* **golang.org/x/crypto** v0.48.0 -> v0.50.0
* **golang.org/x/mod** v0.33.0 -> v0.34.0
* **golang.org/x/net** v0.51.0 -> v0.53.0
* **golang.org/x/sync** v0.19.0 -> v0.20.0
* **golang.org/x/sys** v0.42.0 -> v0.43.0
* **golang.org/x/term** v0.41.0 -> v0.42.0
* **golang.org/x/text** v0.34.0 -> v0.36.0
* **golang.org/x/time** v0.14.0 -> v0.15.0
* **google.golang.org/genproto/googleapis/api** 8636f8732409 -> 6f92a3bedf2d
* **google.golang.org/genproto/googleapis/rpc** 8636f8732409 -> 6f92a3bedf2d
* **google.golang.org/grpc** v1.79.3 -> v1.80.0
* **kernel.org/pub/linux/libs/security/libcap/cap** v1.2.77 -> v1.2.78
* **kernel.org/pub/linux/libs/security/libcap/psx** v1.2.77 -> v1.2.78

Previous release can be found at [v0.29.0](https://github.com/moby/buildkit/releases/tag/v0.29.0)

Assets 42

Loading

### Uh oh!

There was an error while loading. [Please reload this page]().

3 people reacted

You can’t perform that action at this time.

----
url: https://docs.docker.com/ai/sandboxes/security/defaults/
----

# Default security posture

***

Table of contents

***

A sandbox created with `sbx run` and no additional flags has the following security posture.

## [Network defaults](#network-defaults)

All outbound HTTP and HTTPS traffic is blocked unless an explicit rule allows it (deny-by-default). All non-HTTP protocols (raw TCP, UDP including DNS, and ICMP) are blocked at the network layer. Traffic to private IP ranges, loopback addresses, and link-local addresses is also blocked.

Run `sbx policy ls` to see the active network rules for your installation. Rules can be customized per machine with the `sbx policy` CLI, or managed centrally across your organization from the Admin Console. Org-level rules take precedence over local rules. See [Governance](https://docs.docker.com/ai/sandboxes/governance/).

## [Workspace defaults](#workspace-defaults)

Sandboxes use a direct mount by default. The agent sees and modifies your working tree directly, and changes appear on your host immediately.

The agent can read, write, and delete any file within the workspace directory, including hidden files, configuration files, build scripts, and Git hooks. See [Workspace isolation](https://docs.docker.com/ai/sandboxes/security/isolation/#workspace-isolation) for what to review after an agent session.

## [Credential defaults](#credential-defaults)

No credentials are available to the sandbox unless you provide them using `sbx secret` or environment variables. When credentials are provided, the host-side proxy injects them into outbound HTTP headers. The agent cannot read the raw credential values.

See [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/) for setup instructions.

## [Agent capabilities inside the sandbox](#agent-capabilities-inside-the-sandbox)

The agent runs with full control inside the sandbox VM:

* `sudo` access (the agent runs as a non-root user with sudo privileges)
* A private Docker Engine for building images and running containers
* Package installation through `apt`, `pip`, `npm`, and other package managers
* Full read and write access to the VM filesystem

Everything the agent installs or creates inside the VM, including packages, Docker images, and configuration changes, persists across stop and restart cycles. When you remove the sandbox with `sbx rm`, the VM and its contents are deleted. Only workspace files remain on the host.

## [What is blocked by default](#what-is-blocked-by-default)

The following are blocked for all sandboxes and cannot be changed through policy configuration:

* Host filesystem access outside the workspace directory
* Host Docker daemon
* Host network and localhost
* Communication between sandboxes
* Raw TCP, UDP, and ICMP connections
* Traffic to private IP ranges and link-local addresses

Outbound HTTP/HTTPS to domains not in the allow list is also blocked by default, but you can add allow rules with `sbx policy allow`.

----
url: https://docs.docker.com/reference/cli/docker/image/tag/
----

# docker image tag

***

| Description                                                               | Create a tag TARGET\_IMAGE that refers to SOURCE\_IMAGE  |
| ------------------------------------------------------------------------- | -------------------------------------------------------- |
| Usage                                                                     | `docker image tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker tag`                                             |

## [Description](#description)

A Docker image reference consists of several components that describe where the image is stored and its identity. These components are:

```text
[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
```

* `HOST`

  Specifies the registry location where the image resides. If omitted, Docker defaults to Docker Hub (`docker.io`).

* `PORT`

  An optional port number for the registry, if necessary (for example, `:5000`).

* `NAMESPACE/REPOSITORY`

  The namespace (optional) usually represents a user or organization. The repository is required and identifies the specific image. If the namespace is omitted, Docker defaults to `library`, the namespace reserved for Docker Official Images.

* `TAG`

  An optional identifier used to specify a particular version or variant of the image. If no tag is provided, Docker defaults to `latest`.

### [Example image references](#example-image-references)

`example.com:5000/team/my-app:2.0`

* Host: `example.com`
* Port: `5000`
* Namespace: `team`
* Repository: `my-app`
* Tag: `2.0`

`alpine`

* Host: `docker.io` (default)
* Namespace: `library` (default)
* Repository: `alpine`
* Tag: `latest` (default)

For more information on the structure and rules of image naming, refer to the [Distribution reference](https://pkg.go.dev/github.com/distribution/reference#pkg-overview) as the canonical definition of the format.

## [Examples](#examples)

### [Tag an image referenced by ID](#tag-an-image-referenced-by-id)

To tag a local image with ID `0e5574283393` as `fedora/httpd` with the tag `version1.0`:

```console
$ docker tag 0e5574283393 fedora/httpd:version1.0
```

### [Tag an image referenced by Name](#tag-an-image-referenced-by-name)

To tag a local image `httpd` as `fedora/httpd` with the tag `version1.0`:

```console
$ docker tag httpd fedora/httpd:version1.0
```

Note that since the tag name isn't specified, the alias is created for an existing local version `httpd:latest`.

### [Tag an image referenced by Name and Tag](#tag-an-image-referenced-by-name-and-tag)

To tag a local image with the name `httpd` and the tag `test` as `fedora/httpd` with the tag `version1.0.test`:

```console
$ docker tag httpd:test fedora/httpd:version1.0.test
```

### [Tag an image for a private registry](#tag-an-image-for-a-private-registry)

To push an image to a private registry and not the public Docker registry you must include the registry hostname and port (if needed).

```console
$ docker tag 0e5574283393 myregistryhost:5000/fedora/httpd:version1.0
```

----
url: https://docs.docker.com/build-cloud/setup/
----

# Docker Build Cloud setup

***

Table of contents

***

Before you can start using Docker Build Cloud, you must add the builder to your local environment.

## [Prerequisites](#prerequisites)

To get started with Docker Build Cloud, you need to:

* Download and install Docker Desktop version 4.26.0 or later.
* Create a cloud builder on the [Docker Build Cloud Dashboard](https://app.docker.com/build/).
  * When you create the builder, choose a name for it (for example, `default`). You will use this name as `BUILDER_NAME` in the CLI steps below.

### [Use Docker Build Cloud without Docker Desktop](#use-docker-build-cloud-without-docker-desktop)

To use Docker Build Cloud without Docker Desktop, you must download and install a version of Buildx with support for Docker Build Cloud (the `cloud` driver). You can find compatible Buildx binaries on the releases page of [this repository](https://github.com/docker/buildx-desktop).

If you plan on building with Docker Build Cloud using the `docker compose build` command, you also need a version of Docker Compose that supports Docker Build Cloud. You can find compatible Docker Compose binaries on the releases page of [this repository](https://github.com/docker/compose-desktop).

## [Steps](#steps)

You can add a cloud builder using the CLI, with the `docker buildx create` command, or using the Docker Desktop settings GUI.

1. Sign in to your Docker account.

   ```console
   $ docker login
   ```

2. Connect Buildx to your cloud builder.

   ```console
   $ docker buildx create --driver cloud ORG/BUILDER_NAME
   ```

   Replace `<ORG>` with the Docker Hub namespace of your Docker organization (or your username if you are using a personal account), and `<BUILDER_NAME>` with the name you chose when creating the builder in the dashboard.

   This registers a local endpoint for the cloud builder named `cloud-ORG-BUILDER_NAME`.

   > Note
   >
   > This command connects Buildx to an existing Docker Build Cloud builder. It does not create a new cloud builder. To add a new builder, use the [Docker Build Cloud Dashboard](https://app.docker.com/build/).

   > Note
   >
   > If your organization is `acme` and you named your builder `default`, use:
   >
   > ```console
   > $ docker buildx create --driver cloud acme/default
   > ```

1) Sign in to your Docker account using the **Sign in** button in Docker Desktop.

2) Open the Docker Desktop settings and navigate to the **Builders** tab.

3) Under **Available builders**, select **Connect to builder**.

The builder has native support for the `linux/amd64` and `linux/arm64` architectures. This gives you a high-performance build cluster for building multi-platform images natively.

## [Firewall configuration](#firewall-configuration)

To use Docker Build Cloud behind a firewall, ensure that your firewall allows traffic to the following addresses:

* 3.211.38.21
* <https://auth.docker.io>
* <https://build-cloud.docker.com>
* <https://hub.docker.com>

## [What's next](#whats-next)

* See [Building with Docker Build Cloud](https://docs.docker.com/build-cloud/usage/) for examples on how to use Docker Build Cloud.
* See [Use Docker Build Cloud in CI](https://docs.docker.com/build-cloud/ci/) for examples on how to use Docker Build Cloud with CI systems.

----
url: https://docs.docker.com/reference/cli/docker/buildx/dap/build/
----

# docker buildx dap build

***

| Description | Start a build                                        |
| ----------- | ---------------------------------------------------- |
| Usage       | `docker buildx dap build [OPTIONS] PATH \| URL \| -` |

## [Description](#description)

Start a debug session using the [debug adapter protocol](https://microsoft.github.io/debug-adapter-protocol/overview) to communicate with the debugger UI.

Arguments are the same as the `build`

> Note
>
> `buildx dap build` command may receive backwards incompatible features in the future if needed. We are looking for feedback on improving the command and extending the functionality further.

## [Options](#options)

| Option              | Default | Description                                                                                                                                       |
| ------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--add-host`        |         | Add a custom host-to-IP mapping (format: `host:ip`)                                                                                               |
| `--allow`           |         | Allow extra privileged entitlement (e.g., `network.host`, `security.insecure`, `device`, `buildx.local.delete`)                                   |
| `--annotation`      |         | Add annotation to the image                                                                                                                       |
| `--attest`          |         | Attestation parameters (format: `type=sbom,generator=image`)                                                                                      |
| `--build-arg`       |         | Set build-time variables                                                                                                                          |
| `--build-context`   |         | Additional build contexts (e.g., name=path)                                                                                                       |
| `--cache-from`      |         | External cache sources (e.g., `user/app:cache`, `type=local,src=path/to/dir`)                                                                     |
| `--cache-to`        |         | Cache export destinations (e.g., `user/app:cache`, `type=local,dest=path/to/dir`)                                                                 |
| `--call`            | `build` | Set method for evaluating build (`check`, `outline`, `targets`)                                                                                   |
| `--cgroup-parent`   |         | Set the parent cgroup for the `RUN` instructions during build                                                                                     |
| `--check`           |         | Shorthand for `--call=check`                                                                                                                      |
| `-f, --file`        |         | Name of the Dockerfile (default: `PATH/Dockerfile`)                                                                                               |
| `--iidfile`         |         | Write the image ID to a file                                                                                                                      |
| `--label`           |         | Set metadata for an image                                                                                                                         |
| `--load`            |         | Shorthand for `--output=type=docker`                                                                                                              |
| `--metadata-file`   |         | Write build result metadata to a file                                                                                                             |
| `--network`         |         | Set the networking mode for the `RUN` instructions during build                                                                                   |
| `--no-cache`        |         | Do not use cache when building the image                                                                                                          |
| `--no-cache-filter` |         | Do not cache specified stages                                                                                                                     |
| `-o, --output`      |         | Output destination (format: `type=local,dest=path`)                                                                                               |
| `--platform`        |         | Set target platform for build                                                                                                                     |
| `--policy`          |         | Policy configuration (format: `filename=path[,filename=path][,reset=true\|false][,disabled=true\|false][,strict=true\|false][,log-level=level]`)  |
| `--progress`        | `auto`  | Set type of progress output (`auto`, `none`, `plain`, `quiet`, `rawjson`, `tty`). Use plain to show container output                              |
| `--provenance`      |         | Shorthand for `--attest=type=provenance`                                                                                                          |
| `--pull`            |         | Always attempt to pull all referenced images                                                                                                      |
| `--push`            |         | Shorthand for `--output=type=registry,unpack=false`                                                                                               |
| `-q, --quiet`       |         | Suppress the build output and print image ID on success                                                                                           |
| `--resource`        |         | Resource limits for build containers (format: `memory=2g`, `cpu-quota=50000`)                                                                     |
| `--sbom`            |         | Shorthand for `--attest=type=sbom`                                                                                                                |
| `--secret`          |         | Secret to expose to the build (format: `id=mysecret[,src=/local/secret]`)                                                                         |
| `--shm-size`        |         | Shared memory size for build containers                                                                                                           |
| `--ssh`             |         | SSH agent socket or keys to expose to the build (format: `default\|<id>[=<socket>\|<key>[,<key>]]`)                                               |
| `-t, --tag`         |         | Image identifier (format: `[registry/]repository[:tag]`)                                                                                          |
| `--target`          |         | Set the target build stage to build                                                                                                               |
| `--ulimit`          |         | Ulimit options                                                                                                                                    |

## [Examples](#examples)

### [Launch request arguments](#launch-config)

The following [launch request arguments](https://microsoft.github.io/debug-adapter-protocol/specification#Requests_Launch) are supported. These are sent as a JSON body as part of the launch request.

| Name          | Type      | Default      | Description                                                                 |
| ------------- | --------- | ------------ | --------------------------------------------------------------------------- |
| `dockerfile`  | `string`  | `Dockerfile` | Name of the Dockerfile                                                      |
| `contextPath` | `string`  | `.`          | Set the context path for the build (normally the first positional argument) |
| `target`      | `string`  |              | Set the target build stage to build                                         |
| `stopOnEntry` | `boolean` | `false`      | Stop on the first instruction                                               |

### [Additional Arguments](#additional-args)

Command line arguments may be passed to the debug adapter the same way they would be passed to the normal build command and they will set the value. Launch request arguments that are set will override command line arguments if they are present.

A debug extension should include an `args` and `builder` entry in the launch configuration. These will modify the arguments passed to the binary for the tool invocation. `builder` will add `--builder <arg>` directly after the executable and `args` will append to the end of the tool invocation. For example, a launch configuration in Visual Studio Code with the following:

```json
{
    "args": ["--build-arg", "FOO=AAA"]
    "builder": ["mybuilder"]
}
```

This should cause the debug adapter to be invoked as `docker buildx --builder mybuilder dap build --build-arg FOO=AAA`.

----
url: https://docs.docker.com/reference/cli/docker/compose/export/
----

# docker compose export

***

| Description | Export a service container's filesystem as a tar archive |
| ----------- | -------------------------------------------------------- |
| Usage       | `docker compose export [OPTIONS] SERVICE`                |

## [Description](#description)

Export a service container's filesystem as a tar archive

## [Options](#options)

| Option         | Default | Description                                              |
| -------------- | ------- | -------------------------------------------------------- |
| `--index`      |         | index of the container if service has multiple replicas. |
| `-o, --output` |         | Write to a file, instead of STDOUT                       |

----
url: https://docs.docker.com/engine/logging/drivers/gcplogs/
----

# Google Cloud Logging driver

***

Table of contents

***

The Google Cloud Logging driver sends container logs to [Google Cloud Logging](https://cloud.google.com/logging/docs/) Logging.

## [Usage](#usage)

To use the `gcplogs` driver as the default logging driver, set the `log-driver` and `log-opt` keys to appropriate values in the `daemon.json` file. For more about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

The following example sets the log driver to `gcplogs` and sets the `gcp-meta-name` option.

```json
{
  "log-driver": "gcplogs",
  "log-opts": {
    "gcp-meta-name": "example-instance-12345"
  }
}
```

Restart Docker for the changes to take effect.

You can set the logging driver for a specific container by using the `--log-driver` option to `docker run`:

```console
$ docker run --log-driver=gcplogs ...
```

If Docker detects that it's running in a Google Cloud Project, it discovers configuration from the [instance metadata service](https://cloud.google.com/compute/docs/metadata). Otherwise, the user must specify which project to log to using the `--gcp-project` log option and Docker attempts to obtain credentials from the [Google Application Default Credential](https://developers.google.com/identity/protocols/application-default-credentials). The `--gcp-project` flag takes precedence over information discovered from the metadata server, so a Docker daemon running in a Google Cloud project can be overridden to log to a different project using `--gcp-project`.

Docker fetches the values for zone, instance name and instance ID from Google Cloud metadata server. Those values can be provided via options if metadata server isn't available. They don't override the values from metadata server.

## [gcplogs options](#gcplogs-options)

You can use the `--log-opt NAME=VALUE` flag to specify these additional Google Cloud Logging driver options:

| Option          | Required | Description                                                                                                                                                                                       |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `gcp-project`   | optional | Which Google Cloud project to log to. Defaults to discovering this value from the Google Cloud metadata server.                                                                                   |
| `gcp-log-cmd`   | optional | Whether to log the command that the container was started with. Defaults to false.                                                                                                                |
| `labels`        | optional | Comma-separated list of keys of labels, which should be included in message, if these labels are specified for the container.                                                                     |
| `labels-regex`  | optional | Similar to and compatible with `labels`. A regular expression to match logging-related labels. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).             |
| `env`           | optional | Comma-separated list of keys of environment variables, which should be included in message, if these variables are specified for the container.                                                   |
| `env-regex`     | optional | Similar to and compatible with `env`. A regular expression to match logging-related environment variables. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/). |
| `gcp-meta-zone` | optional | Zone name for the instance.                                                                                                                                                                       |
| `gcp-meta-name` | optional | Instance name.                                                                                                                                                                                    |
| `gcp-meta-id`   | optional | Instance ID.                                                                                                                                                                                      |

If there is collision between `label` and `env` keys, the value of the `env` takes precedence. Both options add additional fields to the attributes of a logging message.

The following is an example of the logging options required to log to the default logging destination which is discovered by querying the Google Cloud metadata server.

```console
$ docker run \
    --log-driver=gcplogs \
    --log-opt labels=location \
    --log-opt env=TEST \
    --log-opt gcp-log-cmd=true \
    --env "TEST=false" \
    --label location=west \
    your/application
```

This configuration also directs the driver to include in the payload the label `location`, the environment variable `ENV`, and the command used to start the container.

The following example shows logging options for running outside of Google Cloud. The `GOOGLE_APPLICATION_CREDENTIALS` environment variable must be set for the daemon, for example via systemd:

```ini
[Service]
Environment="GOOGLE_APPLICATION_CREDENTIALS=uQWVCPkMTI34bpssr1HI"
```

```console
$ docker run \
    --log-driver=gcplogs \
    --log-opt gcp-project=test-project \
    --log-opt gcp-meta-zone=west1 \
    --log-opt gcp-meta-name=`hostname` \
    your/application
```

----
url: https://docs.docker.com/reference/cli/docker/compose/ls/
----

# docker compose ls

***

| Description | List running compose projects |
| ----------- | ----------------------------- |
| Usage       | `docker compose ls [OPTIONS]` |

## [Description](#description)

Lists running Compose projects

## [Options](#options)

| Option        | Default | Description                                 |
| ------------- | ------- | ------------------------------------------- |
| `-a, --all`   |         | Show all stopped Compose projects           |
| `--filter`    |         | Filter output based on conditions provided  |
| `--format`    | `table` | Format the output. Values: \[table \| json] |
| `-q, --quiet` |         | Only display project names                  |

----
url: https://docs.docker.com/guides/nextjs/run-tests/
----

# Run Next.js tests in a container

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize Next.js application](https://docs.docker.com/guides/nextjs/containerize/).

## [Overview](#overview)

Testing is a critical part of the development process. In this section, you'll learn how to:

* Run unit tests using Vitest (or Jest) inside a Docker container.
* Run lint (e.g. ESLint) inside a Docker container.
* Use Docker Compose to run tests and lint in an isolated, reproducible environment.

The [sample project](https://github.com/kristiyan-velkov/docker-nextjs-sample) uses [Vitest](https://vitest.dev/) with [Testing Library](https://testing-library.com/) for component testing. You can use the same setup or follow the alternative Jest configuration later.

***

## [Run tests during development](#run-tests-during-development)

The [sample project](https://github.com/kristiyan-velkov/docker-nextjs-sample) already includes lint (ESLint) and sample tests (Vitest, `app/page.test.tsx`) in place. If you're using the sample app, you can skip to **Step 3: Update compose.yaml** and run tests or lint with the commands below. If you're using your own project, follow the install and configuration steps to add the packages and scripts.

The sample includes a test file at:

```text
app/page.test.tsx
```

This file uses Vitest and React Testing Library to verify the behavior of page components.

### [Step 1: Install Vitest and React Testing Library (custom projects)](#step-1-install-vitest-and-react-testing-library-custom-projects)

If you're using a custom project and haven't already added the necessary testing tools, install them by running:

```console
$ npm install --save-dev vitest @vitejs/plugin-react @testing-library/react @testing-library/dom jsdom
```

Then, update the scripts section of your `package.json` file to include:

```json
"scripts": {
  "test": "vitest",
  "test:run": "vitest run"
}
```

For lint, add a `lint` script (and optionally `lint:fix`). For example, with [ESLint](https://eslint.org/):

```json
"scripts": {
  "test": "vitest",
  "test:run": "vitest run",
  "lint": "eslint .",
  "lint:fix": "eslint . --fix"
}
```

The sample project uses `eslint` and `eslint-config-next` for Next.js. Install them in a custom project with:

```console
$ npm install --save-dev eslint eslint-config-next @eslint/eslintrc
```

Create an ESLint config file (e.g. `eslint.config.cjs`) in your project root with Next.js rules and global ignores:

```js
const { defineConfig, globalIgnores } = require("eslint/config");
const { FlatCompat } = require("@eslint/eslintrc");

const compat = new FlatCompat({ baseDirectory: __dirname });

module.exports = defineConfig([
  ...compat.extends(
    "eslint-config-next/core-web-vitals",
    "eslint-config-next/typescript"
  ),
  globalIgnores([
    ".next/**",
    "out/**",
    "build/**",
    "next-env.d.ts",
    "node_modules/**",
    "eslint.config.cjs",
  ]),
]);
```

***

### [Step 2: Configure Vitest (custom projects)](#step-2-configure-vitest-custom-projects)

If you're using a custom project, create a `vitest.config.ts` file in your project root (matching the [sample project](https://github.com/kristiyan-velkov/docker-nextjs-sample)):

```ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: "./vitest.setup.ts",
    globals: true,
  },
});
```

Create a `vitest.setup.ts` file in your project root:

```ts
import "@testing-library/jest-dom/vitest";
```

> Note
>
> Vitest works well with Next.js and provides fast execution and ESM support. For more details, see the [Next.js testing documentation](https://nextjs.org/docs/app/building-your-application/testing) and [Vitest docs](https://vitest.dev/).

### [Step 3: Update compose.yaml](#step-3-update-composeyaml)

Add `nextjs-test` and `nextjs-lint` services to your `compose.yaml` file. In the sample project these services use the `tools` profile so they don't start with a normal `docker compose up`. Both reuse `Dockerfile.dev` and run the test or lint command:

```yaml
services:
  nextjs-prod-standalone:
    build:
      context: .
      dockerfile: Dockerfile
    image: nextjs-sample:prod
    container_name: nextjs-sample-prod
    ports:
      - "3000:3000"

  nextjs-dev:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-dev
    ports:
      - "3000:3000"
    environment:
      - WATCHPACK_POLLING=true
    develop:
      watch:
        - action: sync
          path: .
          target: /app
          ignore:
            - node_modules/
            - .next/
        - action: rebuild
          path: package.json

  nextjs-test:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-test
    command:
      [
        "sh",
        "-c",
        "if [ -f package-lock.json ]; then npm run test:run 2>/dev/null || npm run test -- --run; elif [ -f yarn.lock ]; then yarn test:run 2>/dev/null || yarn test --run; elif [ -f pnpm-lock.yaml ]; then pnpm run test:run; else npm run test -- --run; fi",
      ]
    profiles:
      - tools

  nextjs-lint:
    build:
      context: .
      dockerfile: Dockerfile.dev
    image: nextjs-sample:dev
    container_name: nextjs-sample-lint
    command:
      [
        "sh",
        "-c",
        "if [ -f package-lock.json ]; then npm run lint; elif [ -f yarn.lock ]; then yarn lint; elif [ -f pnpm-lock.yaml ]; then pnpm lint; else npm run lint; fi",
      ]
    profiles:
      - tools
```

The `nextjs-test` and `nextjs-lint` services reuse the same `Dockerfile.dev` used for [development](https://docs.docker.com/guides/nextjs/develop/) and override the default command to run tests or lint. The `profiles: [tools]` means these services only run when you use the `--profile tools` option.

After completing the previous steps, your project directory should contain:

```text
├── docker-nextjs-sample/
│ ├── Dockerfile
│ ├── Dockerfile.dev
│ ├── .dockerignore
│ ├── compose.yaml
│ ├── vitest.config.ts
│ ├── vitest.setup.ts
│ └── next.config.ts
```

### [Step 4: Run the tests](#step-4-run-the-tests)

To execute your test suite inside the container, run from your project root:

```console
$ docker compose --profile tools run --rm nextjs-test
```

This command will:

* Start the `nextjs-test` service (because of `--profile tools`).
* Run your test script (`test:run` or `test -- --run`) in the same environment as development.
* Remove the container after the tests complete ( [`docker compose run --rm`](/reference/cli/docker/compose/run/)).

> Note
>
> For more information about Compose commands and profiles, see the [Compose CLI reference](/reference/cli/docker/compose/).

### [Step 5: Run lint in the container](#step-5-run-lint-in-the-container)

To run your linter (e.g. ESLint) inside the container, use the `nextjs-lint` service with the same `tools` profile:

```console
$ docker compose --profile tools run --rm nextjs-lint
```

This command will:

* Start the `nextjs-lint` service (because of `--profile tools`).
* Run your lint script (`npm run lint`, `yarn lint`, or `pnpm lint` depending on your lockfile) in the same environment as development.
* Remove the container after lint completes.

Ensure your `package.json` includes a `lint` script. The sample project already has `"lint": "eslint ."` and `"lint:fix": "eslint . --fix"`; for a custom project, add the same and install `eslint` and `eslint-config-next` if needed.

***

## [Summary](#summary)

In this section, you learned how to run unit tests for your Next.js application inside a Docker container using Vitest and Docker Compose.

What you accomplished:

* Installed and configured Vitest and React Testing Library for testing Next.js components.
* Created `nextjs-test` and `nextjs-lint` services in `compose.yaml` (with `tools` profile) to isolate test and lint execution.
* Reused the development `Dockerfile.dev` to ensure consistency between dev, test, and lint environments.
* Ran tests inside the container using `docker compose --profile tools run --rm nextjs-test`.
* Ran lint inside the container using `docker compose --profile tools run --rm nextjs-lint`.
* Ensured reliable, repeatable testing and linting across environments without relying on local machine setup.

***

## [Related resources](#related-resources)

Explore official references and best practices to sharpen your Docker testing workflow:

* [Dockerfile reference](/reference/dockerfile/) – Understand all Dockerfile instructions and syntax.
* [Best practices for writing Dockerfiles](/develop/develop-images/dockerfile_best-practices/) – Write efficient, maintainable, and secure Dockerfiles.
* [Compose file reference](/compose/compose-file/) – Learn the full syntax and options available for configuring services in `compose.yaml`.
* [`docker compose run` CLI reference](/reference/cli/docker/compose/run/) – Run one-off commands in a service container.
* [Next.js Testing Documentation](https://nextjs.org/docs/app/building-your-application/testing) – Official Next.js testing guide.

***

## [Next steps](#next-steps)

Next, you'll learn how to set up a CI/CD pipeline using GitHub Actions to automatically build and test your Next.js application in a containerized environment. This ensures your code is validated on every push or pull request, maintaining consistency and reliability across your development workflow.

[Automate your builds with GitHub Actions »](https://docs.docker.com/guides/nextjs/configure-github-actions/)

----
url: https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/
----

# Manage swarm security with public key infrastructure (PKI)

***

Table of contents

***

The Swarm mode public key infrastructure (PKI) system built into Docker makes it simple to securely deploy a container orchestration system. The nodes in a swarm use mutual Transport Layer Security (TLS) to authenticate, authorize, and encrypt the communications with other nodes in the swarm.

When you create a swarm by running `docker swarm init`, Docker designates itself as a manager node. By default, the manager node generates a new root Certificate Authority (CA) along with a key pair, which are used to secure communications with other nodes that join the swarm. If you prefer, you can specify your own externally-generated root CA, using the `--external-ca` flag of the [docker swarm init](/reference/cli/docker/swarm/init/) command.

The manager node also generates two tokens to use when you join additional nodes to the swarm: one worker token and one manager token. Each token includes the digest of the root CA's certificate and a randomly generated secret. When a node joins the swarm, the joining node uses the digest to validate the root CA certificate from the remote manager. The remote manager uses the secret to ensure the joining node is an approved node.

Each time a new node joins the swarm, the manager issues a certificate to the node. The certificate contains a randomly generated node ID to identify the node under the certificate common name (CN) and the role under the organizational unit (OU). The node ID serves as the cryptographically secure node identity for the lifetime of the node in the current swarm.

The diagram below illustrates how manager nodes and worker nodes encrypt communications using a minimum of TLS 1.2.

The example below shows the information from a certificate from a worker node:

```text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            3b:1c:06:91:73:fb:16:ff:69:c3:f7:a2:fe:96:c1:73:e2:80:97:3b
        Signature Algorithm: ecdsa-with-SHA256
        Issuer: CN=swarm-ca
        Validity
            Not Before: Aug 30 02:39:00 2016 GMT
            Not After : Nov 28 03:39:00 2016 GMT
        Subject: O=ec2adilxf4ngv7ev8fwsi61i7, OU=swarm-worker, CN=dw02poa4vqvzxi5c10gm4pq2g
...snip...
```

By default, each node in the swarm renews its certificate every three months. You can configure this interval by running the `docker swarm update --cert-expiry <TIME PERIOD>` command. The minimum rotation value is 1 hour. Refer to the [docker swarm update](/reference/cli/docker/swarm/update/) CLI reference for details.

## [Rotating the CA certificate](#rotating-the-ca-certificate)

> Note
>
> Mirantis Kubernetes Engine (MKE), formerly known as Docker UCP, provides an external certificate manager service for the swarm. If you run swarm on MKE, you shouldn't rotate the CA certificates manually. Instead, contact Mirantis support if you need to rotate a certificate.

In the event that a cluster CA key or a manager node is compromised, you can rotate the swarm root CA so that none of the nodes trust certificates signed by the old root CA anymore.

Run `docker swarm ca --rotate` to generate a new CA certificate and key. If you prefer, you can pass the `--ca-cert` and `--external-ca` flags to specify the root certificate and to use a root CA external to the swarm. Alternately, you can pass the `--ca-cert` and `--ca-key` flags to specify the exact certificate and key you would like the swarm to use.

When you issue the `docker swarm ca --rotate` command, the following things happen in sequence:

1. Docker generates a cross-signed certificate. This means that a version of the new root CA certificate is signed with the old root CA certificate. This cross-signed certificate is used as an intermediate certificate for all new node certificates. This ensures that nodes that still trust the old root CA can still validate a certificate signed by the new CA.

2. Docker also tells all nodes to immediately renew their TLS certificates. This process may take several minutes, depending on the number of nodes in the swarm.

3. After every node in the swarm has a new TLS certificate signed by the new CA, Docker forgets about the old CA certificate and key material, and tells all the nodes to trust the new CA certificate only.

   This also causes a change in the swarm's join tokens. The previous join tokens are no longer valid.

From this point on, all new node certificates issued are signed with the new root CA, and do not contain any intermediates.

## [Learn More](#learn-more)

* Read about how [nodes](https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/) work.
* Learn how Swarm mode [services](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/) work.

----
url: https://docs.docker.com/build/building/secrets/
----

# Build secrets

***

Table of contents

***

A build secret is any piece of sensitive information, such as a password or API token, consumed as part of your application's build process.

Build arguments and environment variables are inappropriate for passing secrets to your build, because they persist in the final image. Instead, you should use secret mounts or SSH mounts, which expose secrets to your builds securely.

## [Types of build secrets](#types-of-build-secrets)

* [Secret mounts](#secret-mounts) are general-purpose mounts for passing secrets into your build. A secret mount takes a secret from the build client and makes it temporarily available inside the build container, for the duration of the build instruction. This is useful if, for example, your build needs to communicate with a private artifact server or API.
* [SSH mounts](#ssh-mounts) are special-purpose mounts for making SSH sockets or keys available inside builds. They're commonly used when you need to fetch private Git repositories in your builds.
* [Git authentication for remote contexts](#git-authentication-for-remote-contexts) is a set of pre-defined secrets for when you build with a remote Git context that's also a private repository. These secrets are "pre-flight" secrets: they are not consumed within your build instruction, but they're used to provide the builder with the necessary credentials to fetch the context.

## [Using build secrets](#using-build-secrets)

For secret mounts and SSH mounts, using build secrets is a two-step process. First you need to pass the secret into the `docker build` command, and then you need to consume the secret in your Dockerfile.

To pass a secret to a build, use the [`docker build --secret` flag](/reference/cli/docker/buildx/build/#secret), or the equivalent options for [Bake](https://docs.docker.com/build/bake/reference/#targetsecret).

```console
$ docker build --secret id=aws,src=$HOME/.aws/credentials .
```

```hcl
variable "HOME" {
  default = null
}

target "default" {
  secret = [
    "id=aws,src=${HOME}/.aws/credentials"
  ]
}
```

To consume a secret in a build and make it accessible to the `RUN` instruction, use the [`--mount=type=secret`](https://docs.docker.com/reference/dockerfile/#run---mounttypesecret) flag in the Dockerfile.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

## [Secret mounts](#secret-mounts)

Secret mounts expose secrets to the build containers, as files or environment variables. You can use secret mounts to pass sensitive information to your builds, such as API tokens, passwords, or SSH keys.

### [Sources](#sources)

The source of a secret can be either a [file](/reference/cli/docker/buildx/build/#file) or an [environment variable](/reference/cli/docker/buildx/build/#typeenv). When you use the CLI or Bake, the type can be detected automatically. You can also specify it explicitly with `type=file` or `type=env`.

The following example mounts the environment variable `KUBECONFIG` to secret ID `kube`, as a file in the build container at `/run/secrets/kube`.

```console
$ docker build --secret id=kube,env=KUBECONFIG .
```

When you use secrets from environment variables, you can omit the `env` parameter to bind the secret to a file with the same name as the variable. In the following example, the value of the `API_TOKEN` variable is mounted to `/run/secrets/API_TOKEN` in the build container.

```console
$ docker build --secret id=API_TOKEN .
```

### [Target](#target)

When consuming a secret in a Dockerfile, the secret is mounted to a file by default. The default file path of the secret, inside the build container, is `/run/secrets/<id>`. You can customize how the secrets get mounted in the build container using the `target` and `env` options for the `RUN --mount` flag in the Dockerfile.

The following example takes secret id `aws` and mounts it to a file at `/run/secrets/aws` in the build container.

```dockerfile
RUN --mount=type=secret,id=aws \
    AWS_SHARED_CREDENTIALS_FILE=/run/secrets/aws \
    aws s3 cp ...
```

To mount a secret as a file with a different name, use the `target` option in the `--mount` flag.

```dockerfile
RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp ...
```

To mount a secret as an environment variable instead of a file, use the `env` option in the `--mount` flag.

```dockerfile
RUN --mount=type=secret,id=aws-key-id,env=AWS_ACCESS_KEY_ID \
    --mount=type=secret,id=aws-secret-key,env=AWS_SECRET_ACCESS_KEY \
    --mount=type=secret,id=aws-session-token,env=AWS_SESSION_TOKEN \
    aws s3 cp ...
```

It's possible to use the `target` and `env` options together to mount a secret as both a file and an environment variable.

## [SSH mounts](#ssh-mounts)

If the credential you want to use in your build is an SSH agent socket or key, you can use the SSH mount instead of a secret mount. Cloning private Git repositories is a common use case for SSH mounts.

The following example clones a private GitHub repository using a [Dockerfile SSH mount](https://docs.docker.com/reference/dockerfile/#run---mounttypessh).

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
ADD git@github.com:me/myprivaterepo.git /src/
```

To pass an SSH socket the build, you use the [`docker build --ssh` flag](/reference/cli/docker/buildx/build/#ssh), or equivalent options for [Bake](https://docs.docker.com/build/bake/reference/#targetssh).

```console
$ docker buildx build --ssh default .
```

## [Git authentication for remote contexts](#git-authentication-for-remote-contexts)

BuildKit supports two pre-defined build secrets, `GIT_AUTH_TOKEN` and `GIT_AUTH_HEADER`. Use them to specify HTTP authentication parameters when building with remote, private Git repositories, including:

* Building with a private Git repository as build context
* Fetching private Git repositories in a build with `ADD`

For example, say you have a private GitHub repository at `https://github.com/example/todo-app.git`, and you want to run a build using that repository as the build context. An unauthenticated `docker build` command fails because the builder isn't authorized to pull the repository:

```console
$ docker build https://github.com/example/todo-app.git
[+] Building 0.4s (1/1) FINISHED
 => ERROR [internal] load git source https://github.com/example/todo-app.git
------
 > [internal] load git source https://github.com/example/todo-app.git:
0.313 fatal: could not read Username for 'https://github.com': terminal prompts disabled
------
```

To authenticate the builder to GitHub, set the `GIT_AUTH_TOKEN` environment variable to contain a valid GitHub access token, and pass it as a secret to the build:

```console
$ GIT_AUTH_TOKEN=$(gh auth token) docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/example/todo-app.git
```

The `GIT_AUTH_TOKEN` also works with `ADD` to fetch private Git repositories as part of your build:

```dockerfile
FROM alpine
ADD https://github.com/example/todo-app.git /src
```

### [HTTP authentication scheme](#http-authentication-scheme)

BuildKit supports two Git authentication secrets:

* **`GIT_AUTH_TOKEN`**: Uses Basic authentication with a fixed username of `x-access-token` (the GitHub-style default)
* **`GIT_AUTH_HEADER`**: Uses the raw authorization header value you provide (works with any Git provider)

#### [Using GIT\_AUTH\_TOKEN (for example, GitHub)](#using-git_auth_token-for-example-github)

When you use `GIT_AUTH_TOKEN`, BuildKit constructs a Basic authentication header using `x-access-token` as the user:

```http
Authorization: Basic <base64("x-access-token:GIT_AUTH_TOKEN")>
```

This method works for providers that accept the `x-access-token` Basic auth pattern, such as GitHub. Example usage:

```console
$ export GIT_AUTH_TOKEN=$(gh auth token)
$ docker build \
  --secret id=GIT_AUTH_TOKEN \
  https://github.com/example/todo-app.git
```

#### [Using GIT\_AUTH\_HEADER (custom authorization header)](#using-git_auth_header-custom-authorization-header)

When you use `GIT_AUTH_HEADER`, BuildKit uses the exact value you provide as the `Authorization` header:

```http
Authorization: GIT_AUTH_HEADER
```

Example usage with GitLab CI/CD token:

```console
$ export GIT_AUTH_HEADER="Basic $(echo -n "gitlab-ci-token:${CI_JOB_TOKEN}" | base64)"
$ docker build \
  --secret id=GIT_AUTH_HEADER \
  https://gitlab.com/example/todo-app.git
```

### [Multiple hosts](#multiple-hosts)

You can set the `GIT_AUTH_TOKEN` and `GIT_AUTH_HEADER` secrets on a per-host basis, which lets you use different authentication parameters for different hostnames. To specify a hostname, append the hostname as a suffix to the secret ID:

```console
$ export GITHUB_TOKEN=$(gh auth token)
$ export GITLAB_AUTH_HEADER="Basic $(echo -n "gitlab-ci-token:${CI_JOB_TOKEN}" | base64)"
$ docker build \
  --secret id=GIT_AUTH_TOKEN.github.com,env=GITHUB_TOKEN \
  --secret id=GIT_AUTH_HEADER.gitlab.com,env=GITLAB_AUTH_HEADER \
  https://github.com/example/todo-app.git
```

## [HTTP authentication for `COPY` and `ADD`](#http-authentication-for-copy-and-add)

To use secrets in `COPY` or `ADD` commands, you can create `HTTP_AUTH_TOKEN_<host>` or `HTTP_AUTH_HEADER_<host>` secrets for use when accessing the specified host. For example `HTTP_AUTH_TOKEN_127.0.0.1=token` will make requests to `127.0.0.1` add a header `Authorization: Bearer token`.

These variables follow the same convention as the [Git HTTP authentication scheme](#http-authentication-scheme) handling.

----
url: https://docs.docker.com/ai/sandboxes/architecture/
----

# Architecture

***

Table of contents

***

This page explains how Docker Sandboxes work under the hood. For the security properties of the architecture, see [Sandbox isolation](https://docs.docker.com/ai/sandboxes/security/isolation/).

## [Workspace mounting](#workspace-mounting)

Your workspace is mounted directly into the sandbox through a filesystem passthrough. The sandbox sees your actual host files, so changes in either direction are instant with no sync process involved.

Your workspace is mounted at the same absolute path as on your host. Preserving absolute paths means error messages, configuration files, and build outputs all reference paths you can find on your host. The agent sees exactly the directory structure you see, which reduces confusion when debugging or reviewing changes.

> Warning
>
> Avoid mounting network-attached or remote storage (network drives, SMB/NFS shares, or cloud-synced folders) as a workspace. The sandbox accesses workspaces through a filesystem passthrough, so every file read and write goes over the network. This adds latency and slows agent performance.

## [Storage and persistence](#storage-and-persistence)

When you create a sandbox, everything inside it persists until you remove it: Docker images and containers built or pulled by the agent, installed packages, agent state and history, and workspace changes.

Sandboxes are isolated from each other. Each one maintains its own Docker daemon state, image cache, and package installations. Multiple sandboxes don't share images or layers.

Each sandbox consumes disk space for its VM image, Docker images, container layers, and volumes, and this grows as you build images and install packages.

## [Networking](#networking)

All outbound traffic from the sandbox routes through an HTTP/HTTPS proxy on your host. Agents are configured to use the proxy automatically. The proxy enforces [network access policies](https://docs.docker.com/ai/sandboxes/governance/) and handles [credential injection](https://docs.docker.com/ai/sandboxes/security/credentials/). See [Network isolation](https://docs.docker.com/ai/sandboxes/security/isolation/#network-isolation) for how this works and [Default security posture](https://docs.docker.com/ai/sandboxes/security/defaults/) for what is allowed out of the box.

### [Upstream proxy](#upstream-proxy)

The host-side proxy makes its outbound connections using your host's network configuration and routing. When a destination is reachable through a direct route, traffic follows that route. When reaching a destination requires an upstream proxy, the host-side proxy forwards the request to it. Chaining to an upstream proxy means sandbox traffic respects the same egress controls as other applications on your host.

The sandbox daemon makes these upstream requests, and it reads the proxy environment variables `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY`, along with their lowercase equivalents. Set `NO_PROXY` to list hosts that should be reached directly instead of through the upstream proxy.

To route sandbox traffic through a different proxy, set `DOCKER_SANDBOXES_PROXY` to the proxy URL. It applies only to sandbox traffic and sets the upstream proxy for both HTTP and HTTPS to that URL. Unlike `HTTP_PROXY` and `HTTPS_PROXY`, it doesn't affect image pulls or the daemon's own requests.

Set these variables in the environment where the sandbox daemon starts. The daemon starts automatically the first time a command needs it, so set the variables before you run a `sbx` command. If the daemon is already running, restart it for a change to take effect.

Two limitations apply:

* Only HTTP and HTTPS traffic can be forwarded to an upstream proxy. Other TCP traffic can't be redirected to a proxy.
* Proxy auto-configuration files, such as `proxy.pac`, aren't supported. Set the `HTTP_PROXY`, `HTTPS_PROXY`, or `DOCKER_SANDBOXES_PROXY` environment variables explicitly.

## [Lifecycle](#lifecycle)

`sbx run` initializes a VM with a workspace for a specified agent and starts the agent. You can stop and restart without recreating the VM, preserving installed packages and Docker images.

Sandboxes persist until explicitly removed. Stopping an agent doesn't delete the VM; environment setup carries over between runs. Use `sbx rm` to delete the sandbox, its VM, and all of its contents. If the sandbox used [`--clone`](https://docs.docker.com/ai/sandboxes/usage/#clone-mode), the `sandbox-<name>` Git remote is also removed from your host repository.

## [Comparison to alternatives](#comparison-to-alternatives)

| Approach                                            | Isolation            | Docker access      | Use case           |
| --------------------------------------------------- | -------------------- | ------------------ | ------------------ |
| Sandboxes (microVMs)                                | Full (hypervisor)    | Isolated daemon    | Autonomous agents  |
| Container with socket mount                         | Partial (namespaces) | Shared host daemon | Trusted tools      |
| [Docker-in-Docker](https://hub.docker.com/_/docker) | Partial (privileged) | Nested daemon      | CI/CD pipelines    |
| Host execution                                      | None                 | Host daemon        | Manual development |

Sandboxes trade higher resource overhead (a VM plus its own daemon) for complete isolation. Use containers when you need lightweight packaging without Docker access. Use sandboxes when you need to give something autonomous full Docker capabilities without trusting it with your host environment.

----
url: https://docs.docker.com/reference/cli/sbx/create/claude/
----

# sbx create claude

| Description | Create a sandbox for claude                |
| ----------- | ------------------------------------------ |
| Usage       | `sbx create claude PATH [PATH...] [flags]` |

## [Description](#description)

Create a sandbox with access to a host workspace for claude.

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
sbx create claude .

# Create with a specific path
sbx create claude /path/to/project

# Create with additional read-only workspaces
sbx create claude . /path/to/docs:ro
```

----
url: https://docs.docker.com/reference/cli/docker/compose/pause/
----

# docker compose pause

***

| Description | Pause services                      |
| ----------- | ----------------------------------- |
| Usage       | `docker compose pause [SERVICE...]` |

## [Description](#description)

Pauses running containers of a service. They can be unpaused with `docker compose unpause`.

----
url: https://docs.docker.com/guides/testcontainers-java-getting-started/create-project/
----

# Create the Java project

***

Table of contents

***

## [Set up the Maven project](#set-up-the-maven-project)

Create a Java project with Maven from your preferred IDE. This guide uses Maven, but you can use Gradle if you prefer. Add the following dependencies to `pom.xml`:

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
</dependencies>

<build>
    <plugins>
        <plugin>
            <groupId>org.apache.maven.plugins</groupId>
            <artifactId>maven-surefire-plugin</artifactId>
            <version>3.2.5</version>
        </plugin>
    </plugins>
</build>
```

This adds the Postgres JDBC driver, logback for logging, JUnit 5 for testing, and the latest `maven-surefire-plugin` for JUnit 5 support.

## [Implement the business logic](#implement-the-business-logic)

Create a `Customer` record:

```java
package com.testcontainers.demo;

public record Customer(Long id, String name) {}
```

Create a `DBConnectionProvider` class to hold JDBC connection parameters and provide a database `Connection`:

```java
package com.testcontainers.demo;

import java.sql.Connection;
import java.sql.DriverManager;

class DBConnectionProvider {

  private final String url;
  private final String username;
  private final String password;

  public DBConnectionProvider(String url, String username, String password) {
    this.url = url;
    this.username = username;
    this.password = password;
  }

  Connection getConnection() {
    try {
      return DriverManager.getConnection(url, username, password);
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
}
```

Create the `CustomerService` class:

```java
package com.testcontainers.demo;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

public class CustomerService {

  private final DBConnectionProvider connectionProvider;

  public CustomerService(DBConnectionProvider connectionProvider) {
    this.connectionProvider = connectionProvider;
    createCustomersTableIfNotExists();
  }

  public void createCustomer(Customer customer) {
    try (Connection conn = this.connectionProvider.getConnection()) {
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

    try (Connection conn = this.connectionProvider.getConnection()) {
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

  private void createCustomersTableIfNotExists() {
    try (Connection conn = this.connectionProvider.getConnection()) {
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
}
```

Here's what `CustomerService` does:

* The constructor calls `createCustomersTableIfNotExists()` to ensure the table exists.
* `createCustomer()` inserts a customer record into the database.
* `getAllCustomers()` fetches all rows from the `customers` table and returns a list of `Customer` objects.

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-java-getting-started/write-tests/)

----
url: https://docs.docker.com/guides/github-sonarqube-sandbox/customize/
----

# Customize a code quality check workflow

***

Table of contents

***

Now that you understand the basics of automating code quality workflows with GitHub and SonarQube in E2B sandboxes, you can customize the workflow for your needs.

## [Focus on specific quality issues](#focus-on-specific-quality-issues)

Modify the prompt to prioritize certain issue types:

```typescript
const prompt = `Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "${repoPath}" and fix the highest priority issues first.`;
```

```python
prompt = f"""Using SonarQube and GitHub MCP tools:

Focus only on:
- Security vulnerabilities (CRITICAL priority)
- Bugs (HIGH priority)
- Skip code smells for this iteration

Analyze "{repo_path}" and fix the highest priority issues first."""
```

## [Integrate with CI/CD](#integrate-with-cicd)

Add this workflow to GitHub Actions to run automatically on pull requests:

```yaml
name: Automated quality checks
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-node@v5
        with:
          node-version: "24"
      - run: npm install
      - run: npx tsx 06-quality-gated-pr.ts
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

```yaml
name: Automated quality checks
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: actions/setup-python@v6
        with:
          python-version: "3.14"
      - run: pip install e2b python-dotenv
      - run: python 06_quality_gated_pr.py
        env:
          E2B_API_KEY: ${{ secrets.E2B_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONARQUBE_TOKEN: ${{ secrets.SONARQUBE_TOKEN }}
          GITHUB_OWNER: ${{ github.repository_owner }}
          GITHUB_REPO: ${{ github.event.repository.name }}
          SONARQUBE_ORG: your-org-key
```

## [Filter by file patterns](#filter-by-file-patterns)

Target specific parts of your codebase:

```typescript
const prompt = `Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only.`;
```

```python
prompt = """Analyze code quality but only consider:
- Files in src/**/*.js
- Exclude test files (*.test.js, *.spec.js)
- Exclude build artifacts in dist/

Focus on production code only."""
```

## [Set quality thresholds](#set-quality-thresholds)

Define when PRs should be created:

```typescript
const prompt = `Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation.`;
```

```python
prompt = """Quality gate thresholds:
- Only create PR if:
  * Bug count decreases by at least 1
  * No new security vulnerabilities introduced
  * Code coverage does not decrease
  * Technical debt reduces by at least 15 minutes

If changes do not meet these thresholds, explain why and skip PR creation."""
```

## [Next steps](#next-steps)

Learn how to troubleshoot common issues.

[Troubleshoot code quality workflows »](https://docs.docker.com/guides/github-sonarqube-sandbox/troubleshoot/)

----
url: https://docs.docker.com/build/policies/validate-git/
----

# Validating Git repositories

***

Table of contents

***

Git repositories often appear in Docker builds as source code inputs. The `ADD` instruction can clone repositories, and build contexts can reference Git URLs. Validating these inputs ensures you're building from trusted sources with verified versions.

This guide teaches you to write policies that validate Git inputs, from basic version pinning to verifying signed commits and tags.

## [Prerequisites](#prerequisites)

You should understand the policy basics from the [Introduction](https://docs.docker.com/build/policies/intro/): creating policy files, basic Rego syntax, and how policies evaluate during builds.

## [What are Git inputs?](#what-are-git-inputs)

Git inputs come from `ADD` instructions that reference Git repositories:

```dockerfile
# Clone a specific tag
ADD https://github.com/moby/buildkit.git#v0.26.1 /buildkit

# Clone a branch
ADD https://github.com/user/repo.git#main /src

# Clone a commit
ADD https://github.com/user/repo.git#abcde123 /src
```

The build context can also be a Git repository when you build with:

```console
$ docker build https://github.com/user/repo.git#main
```

Each Git reference triggers a policy evaluation. Your policy can inspect repository URLs, validate versions, check commit metadata, and verify signatures.

## [Match specific repositories](#match-specific-repositories)

The simplest Git policy restricts which repositories can be used:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/moby/buildkit.git"
}

decision := {"allow": allow}
```

This policy:

* Denies all inputs by default
* Allows local build context
* Allows only the BuildKit repository from GitHub

The `host` field contains the Git server hostname, and `remote` contains the full repository URL. Test it:

Dockerfile

```dockerfile
FROM scratch
ADD https://github.com/moby/buildkit.git#v0.26.1 /
```

```console
$ docker build .
```

The build succeeds. Try a different repository and it fails.

You can match multiple repositories with additional rules:

```rego
allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/moby/buildkit.git"
}

allow if {
  input.git.host == "github.com"
  input.git.remote == "https://github.com/docker/cli.git"
}

decision := {"allow": allow}
```

## [Pin to specific versions](#pin-to-specific-versions)

Tags and branches can change over time. Pin to specific versions to ensure reproducible builds:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tagName == "v0.26.1"
}

decision := {"allow": allow}
```

The `tagName` field contains the tag name when the Git reference points to a tag. Use `branch` for branches:

```rego
allow if {
  input.git.remote == "https://github.com/user/repo.git"
  input.git.branch == "main"
}
```

Or use `ref` for any type of reference (branch, tag, or commit SHA):

```rego
allow if {
  input.git.ref == "v0.26.1"
}
```

## [Use version allowlists](#use-version-allowlists)

For repositories you trust but want to control versions, maintain an allowlist:

```rego
package docker

default allow := false

allowed_versions = [
    {"tag": "v0.26.1", "annotated": true, "sha": "abc123"},
]

is_buildkit if {
    input.git.remote == "https://github.com/moby/buildkit.git"
}

allow if {
    not is_buildkit
}

allow if {
    is_buildkit
    some version in allowed_versions
    input.git.tagName == version.tag
    input.git.isAnnotatedTag == version.annotated
    startswith(input.git.commitChecksum, version.sha)
}

decision := {"allow": allow}
```

This policy:

* Defines an allowlist of approved versions with metadata
* Uses a helper rule (`is_buildkit`) for readability
* Allows all non-BuildKit inputs
* For BuildKit, checks the tag name, whether it's an annotated tag, and the commit SHA against the allowlist

The helper rule makes complex policies more maintainable. You can expand the allowlist as new versions are approved:

```rego
allowed_versions = [
    {"tag": "v0.26.1", "annotated": true, "sha": "abc123"},
    {"tag": "v0.27.0", "annotated": true, "sha": "def456"},
    {"tag": "v0.27.1", "annotated": true, "sha": "789abc"},
]
```

## [Validate with regex patterns](#validate-with-regex-patterns)

Use pattern matching for semantic versioning:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  regex.match(`^v[0-9]+\.[0-9]+\.[0-9]+$`, input.git.tagName)
}

decision := {"allow": allow}
```

This allows any BuildKit tag matching the pattern `vX.Y.Z` where X, Y, and Z are numbers. The regex ensures you're using release versions, not pre-release tags like `v0.26.0-rc1`.

Match major versions:

```rego
# Only allow v0.x releases
allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  regex.match(`^v0\.[0-9]+\.[0-9]+$`, input.git.tagName)
}
```

## [Inspect commit metadata](#inspect-commit-metadata)

The `commit` object provides detailed information about commits:

```rego
package docker

default allow := false

allow if input.local

# Check commit author
allow if {
  input.git.remote == "https://github.com/user/repo.git"
  input.git.commit.author.email == "trusted@example.com"
}

decision := {"allow": allow}
```

The `commit` object includes:

* `author.name`: Author's name
* `author.email`: Author's email
* `author.when`: When the commit was authored
* `committer.name`: Committer's name
* `committer.email`: Committer's email
* `committer.when`: When the commit was committed
* `message`: Commit message

Validate commit messages:

```rego
allow if {
  input.git.commit
  contains(input.git.commit.message, "Signed-off-by:")
}
```

Pin to specific commit SHA:

```rego
allow if {
  input.git.commitChecksum == "abc123def456..."
}
```

## [Require signed commits](#require-signed-commits)

GPG-signed commits prove authenticity. Check for commit signatures:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.commit.pgpSignature != null
}

decision := {"allow": allow}
```

The `pgpSignature` field is `null` for unsigned commits. For signed commits, it contains signature details.

SSH signatures work similarly:

```rego
allow if {
  input.git.commit.sshSignature != null
}
```

## [Require signed tags](#require-signed-tags)

Annotated tags can be signed, providing a cryptographic guarantee of the release:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tag.pgpSignature != null
}

decision := {"allow": allow}
```

The `tag` object is only available for annotated tags. It includes:

* `tagger.name`: Who created the tag
* `tagger.email`: Tagger's email
* `tagger.when`: When the tag was created
* `message`: Tag message
* `pgpSignature`: GPP signature (if signed)
* `sshSignature`: SSH signature (if signed)

Lightweight tags don't have a `tag` object, so this policy effectively requires annotated, signed tags.

## [Verify signatures with public keys](#verify-signatures-with-public-keys)

Use the `verify_git_signature()` function to cryptographically verify Git signatures against trusted public keys:

```rego
package docker

default allow := false

allow if input.local

allow if {
  input.git.remote == "https://github.com/moby/buildkit.git"
  input.git.tagName != ""
  verify_git_signature(input.git.tag, "keys.asc")
}

decision := {"allow": allow}
```

This verifies that Git tags are signed by keys in the `keys.asc` public key file. To set this up:

1. Export maintainer public keys:
   ```console
   $ curl https://github.com/user.gpg > keys.asc
   ```
2. Place `keys.asc` alongside your policy file

The function verifies PGP signatures on commits or tags. See [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for more details.

## [Apply conditional rules](#apply-conditional-rules)

Use different rules for different contexts. Allow unsigned refs during development but require signing for production:

```rego
package docker

default allow := false

allow if input.local

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
    verify_git_signature(input.git.tag, "keys.asc")
}

# Non-version refs allowed in development
allow if {
    is_buildkit
    not is_version_tag
    input.env.target != "release"
}

decision := {"allow": allow}
```

This policy:

* Defines helper rules for readability
* Requires signed version tags from maintainers
* Allows unsigned refs (branches, commits) unless building the release target
* Uses `input.env.target` to detect the build target

Build a development target without signatures:

```console
$ docker buildx build --target=dev .
```

Build the release target, and signing is enforced:

```console
$ docker buildx build --target=release .
```

## [Next steps](#next-steps)

You now understand how to validate Git repositories in build policies. To continue learning:

* Browse [Example policies](https://docs.docker.com/build/policies/examples/) for complete policy patterns
* Read [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for Git signature verification functions
* Check the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available Git fields

----
url: https://docs.docker.com/build/bake/remote-definition/
----

# Remote Bake file definition

***

Table of contents

***

You can build Bake files directly from a remote Git repository or HTTPS URL:

```console
$ docker buildx bake "https://github.com/docker/cli.git#v20.10.11" --print
#1 [internal] load git source https://github.com/docker/cli.git#v20.10.11
#1 0.745 e8f1871b077b64bcb4a13334b7146492773769f7       refs/tags/v20.10.11
#1 2.022 From https://github.com/docker/cli
#1 2.022  * [new tag]         v20.10.11  -> v20.10.11
#1 DONE 2.9s
```

This fetches the Bake definition from the specified remote location and executes the groups or targets defined in that file. If the remote Bake definition doesn't specify a build context, the context is automatically set to the Git remote. For example, [this case](https://github.com/docker/cli/blob/2776a6d694f988c0c1df61cad4bfac0f54e481c8/docker-bake.hcl#L17-L26) uses `https://github.com/docker/cli.git`:

```json
{
  "group": {
    "default": {
      "targets": ["binary"]
    }
  },
  "target": {
    "binary": {
      "context": "https://github.com/docker/cli.git#v20.10.11",
      "dockerfile": "Dockerfile",
      "args": {
        "BASE_VARIANT": "alpine",
        "GO_STRIP": "",
        "VERSION": ""
      },
      "target": "binary",
      "platforms": ["local"],
      "output": ["build"]
    }
  }
}
```

## [Use the local context with a remote definition](#use-the-local-context-with-a-remote-definition)

When building with a remote Bake definition, you may want to consume local files relative to the directory where the Bake command is executed. You can define contexts as relative to the command context using a `cwd://` prefix.

https\://github.com/dvdksn/buildx/blob/bake-remote-example/docker-bake.hcl

```hcl
target "default" {
  context = "cwd://"
  dockerfile-inline = <<EOT
FROM alpine
WORKDIR /src
COPY . .
RUN ls -l && stop
EOT
}
```

```console
$ touch foo bar
$ docker buildx bake "https://github.com/dvdksn/buildx.git#bake-remote-example"
```

```text
...
 > [4/4] RUN ls -l && stop:
#8 0.101 total 0
#8 0.102 -rw-r--r--    1 root     root             0 Jul 27 18:47 bar
#8 0.102 -rw-r--r--    1 root     root             0 Jul 27 18:47 foo
#8 0.102 /bin/sh: stop: not found
```

You can append a path to the `cwd://` prefix if you want to use a specific local directory as a context. Note that if you do specify a path, it must be within the working directory where the command gets executed. If you use an absolute path, or a relative path leading outside of the working directory, Bake will throw an error.

### [Local named contexts](#local-named-contexts)

You can also use the `cwd://` prefix to define local directories in the Bake execution context as named contexts.

The following example defines the `docs` context as `./src/docs/content`, relative to the current working directory where Bake is run as a named context.

docker-bake.hcl

```hcl
target "default" {
  contexts = {
    docs = "cwd://src/docs/content"
  }
  dockerfile = "Dockerfile"
}
```

By contrast, if you omit the `cwd://` prefix, the path would be resolved relative to the build context.

## [Specify the Bake definition to use](#specify-the-bake-definition-to-use)

When loading a Bake file from a remote Git repository, if the repository contains more than one Bake file, you can specify which Bake definition to use with the `--file` or `-f` flag:

```console
docker buildx bake -f bake.hcl "https://github.com/crazy-max/buildx.git#remote-with-local"
```

```text
...
#4 [2/2] RUN echo "hello world"
#4 0.270 hello world
#4 DONE 0.3s
```

## [Combine local and remote Bake definitions](#combine-local-and-remote-bake-definitions)

You can also combine remote definitions with local ones using the `cwd://` prefix with `-f`.

Given the following local Bake definition in the current working directory:

```hcl
# local.hcl
target "default" {
  args = {
    HELLO = "foo"
  }
}
```

The following example uses `-f` to specify two Bake definitions:

* `-f bake.hcl`: this definition is loaded relative to the Git URL.
* `-f cwd://local.hcl`: this definition is loaded relative to the current working directory where the Bake command is executed.

```console
docker buildx bake -f bake.hcl -f cwd://local.hcl "https://github.com/crazy-max/buildx.git#remote-with-local" --print
```

```json
{
  "target": {
    "default": {
      "context": "https://github.com/crazy-max/buildx.git#remote-with-local",
      "dockerfile": "Dockerfile",
      "args": {
        "HELLO": "foo"
      },
      "target": "build",
      "output": [
        {
          "type": "cacheonly"
        }
      ]
    }
  }
}
```

One case where combining local and remote Bake definitions becomes necessary is when you're building with a remote Bake definition in GitHub Actions and want to use the [metadata-action](https://github.com/docker/metadata-action) to generate tags, annotations, or labels. The metadata action generates a Bake file available in the runner's local Bake execution context. To use both the remote definition and the local "metadata-only" Bake file, specify both files and use the `cwd://` prefix for the metadata Bake file:

```yml
      - name: Build
        uses: docker/bake-action@v7
        with:
          files: |
            ./docker-bake.hcl
            cwd://${{ steps.meta.outputs.bake-file }}
          targets: build
```

## [Remote definition in a private repository](#remote-definition-in-a-private-repository)

If you want to use a remote definition that lives in a private repository, you may need to specify credentials for Bake to use when fetching the definition.

If you can authenticate to the private repository using the default `SSH_AUTH_SOCK`, then you don't need to specify any additional authentication parameters for Bake. Bake automatically uses your default agent socket.

For authentication using an HTTP token, or custom SSH agents, use the following environment variables to configure Bake's authentication strategy:

* [`BUILDX_BAKE_GIT_AUTH_TOKEN`](https://docs.docker.com/build/building/variables/#buildx_bake_git_auth_token)
* [`BUILDX_BAKE_GIT_AUTH_HEADER`](https://docs.docker.com/build/building/variables/#buildx_bake_git_auth_header)
* [`BUILDX_BAKE_GIT_SSH`](https://docs.docker.com/build/building/variables/#buildx_bake_git_ssh)

----
url: https://docs.docker.com/reference/cli/docker/model/reinstall-runner/
----

# docker model reinstall-runner

***

| Description | Reinstall Docker Model Runner (Docker Engine only) |
| ----------- | -------------------------------------------------- |
| Usage       | `docker model reinstall-runner`                    |

## [Description](#description)

This command removes the existing Docker Model Runner container and reinstalls it with the specified configuration. Models and images are preserved during reinstallation.

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
url: https://docs.docker.com/engine/swarm/raft/
----

# Raft consensus in swarm mode

***

***

When Docker Engine runs in Swarm mode, manager nodes implement the [Raft Consensus Algorithm](http://thesecretlivesofdata.com/raft/) to manage the global cluster state.

The reason why Swarm mode is using a consensus algorithm is to make sure that all the manager nodes that are in charge of managing and scheduling tasks in the cluster are storing the same consistent state.

Having the same consistent state across the cluster means that in case of a failure, any Manager node can pick up the tasks and restore the services to a stable state. For example, if the Leader Manager which is responsible for scheduling tasks in the cluster dies unexpectedly, any other Manager can pick up the task of scheduling and re-balance tasks to match the desired state.

Systems using consensus algorithms to replicate logs in a distributed systems do require special care. They ensure that the cluster state stays consistent in the presence of failures by requiring a majority of nodes to agree on values.

Raft tolerates up to `(N-1)/2` failures and requires a majority or quorum of `(N/2)+1` members to agree on values proposed to the cluster. This means that in a cluster of 5 Managers running Raft, if 3 nodes are unavailable, the system cannot process any more requests to schedule additional tasks. The existing tasks keep running but the scheduler cannot rebalance tasks to cope with failures if the manager set is not healthy.

The implementation of the consensus algorithm in Swarm mode means it features the properties inherent to distributed systems:

* Agreement on values in a fault tolerant system. (Refer to [FLP impossibility theorem](https://www.the-paper-trail.org/post/2008-08-13-a-brief-tour-of-flp-impossibility/) and the [Raft Consensus Algorithm paper](https://www.usenix.org/system/files/conference/atc14/atc14-paper-ongaro.pdf))
* Mutual exclusion through the leader election process
* Cluster membership management
* Globally consistent object sequencing and CAS (compare-and-swap) primitives

----
url: https://docs.docker.com/reference/cli/docker/mcp/secret/set/
----

# docker mcp secret set

***

| Description | Set a secret in the local OS Keychain |
| ----------- | ------------------------------------- |
| Usage       | `docker mcp secret set key[=value]`   |

## [Description](#description)

Set a secret in the local OS Keychain

## [Examples](#examples)

### [Pass the secret via STDIN](#pass-the-secret-via-stdin)

```console
echo my-secret-password > pwd.txt
cat pwd.txt | docker mcp secret set postgres_password
```

----
url: https://docs.docker.com/reference/compose-file/extension/
----

# Extensions

***

Table of contents

***

Extensions can be used to make your Compose file more efficient and easier to maintain.

Use the prefix `x-` as a top-level element to modularize configurations that you want to reuse. Compose ignores any fields that start with `x-`, this is the sole exception where Compose silently ignores unrecognized fields.

Extensions can also be used with [anchors and aliases](https://docs.docker.com/reference/compose-file/fragments/).

They also can be used within any structure in a Compose file where user-defined keys are not expected. Compose uses those to enable experimental features, the same way browsers add support for [custom CSS features](https://www.w3.org/TR/2011/REC-CSS2-20110607/syndata.html#vendor-keywords)

## [Example 1](#example-1)

```yml
x-custom:
  foo:
    - bar
    - zot

services:
  webapp:
    image: example/webapp
    x-foo: bar
```

```yml
service:
  backend:
    deploy:
      placement:
        x-aws-role: "arn:aws:iam::XXXXXXXXXXXX:role/foo"
        x-aws-region: "eu-west-3"
        x-azure-region: "france-central"
```

## [Example 2](#example-2)

```yml
x-env: &env
  environment:
    - CONFIG_KEY
    - EXAMPLE_KEY
 
services:
  first:
    <<: *env
    image: my-image:latest
  second:
    <<: *env
    image: another-image:latest
```

In this example, the environment variables do not belong to either of the services. They’ve been lifted out completely into the `x-env` extension field. This defines a new node which contains the environment field. The `&env` YAML anchor is used so both services can reference the extension field’s value as `*env`.

## [Example 3](#example-3)

```yml
x-function: &function
 labels:
   function: "true"
 depends_on:
   - gateway
 networks:
   - functions
 deploy:
   placement:
     constraints:
       - 'node.platform.os == linux'
services:
 # Node.js gives OS info about the node (Host)
 nodeinfo:
   <<: *function
   image: functions/nodeinfo:latest
   environment:
     no_proxy: "gateway"
     https_proxy: $https_proxy
 # Uses `cat` to echo back response, fastest function to execute.
 echoit:
   <<: *function
   image: functions/alpine:health
   environment:
     fprocess: "cat"
     no_proxy: "gateway"
     https_proxy: $https_proxy
```

The `nodeinfo` and `echoit` services both include the `x-function` extension via the `&function` anchor, then set their specific image and environment.

## [Example 4](#example-4)

Using [YAML merge](https://yaml.org/type/merge.html) it is also possible to use multiple extensions and share and override additional attributes for specific needs:

```yml
x-environment: &default-environment
  FOO: BAR
  ZOT: QUIX
x-keys: &keys
  KEY: VALUE
services:
  frontend:
    image: example/webapp
    environment: 
      << : [*default-environment, *keys]
      YET_ANOTHER: VARIABLE
```

> Note
>
> [YAML merge](https://yaml.org/type/merge.html) only applies to mappings, and can't be used with sequences.
>
> In the example above, the environment variables are declared using the `FOO: BAR` mapping syntax, while the sequence syntax `- FOO=BAR` is only valid when no fragments are involved.

## [Informative historical notes](#informative-historical-notes)

This section is informative. At the time of writing, the following prefixes are known to exist:

| Prefix     | Vendor/Organization |
| ---------- | ------------------- |
| docker     | Docker              |
| kubernetes | Kubernetes          |

## [Specifying byte values](#specifying-byte-values)

Values express a byte value as a string in `{amount}{byte unit}` format: The supported units are `b` (bytes), `k` or `kb` (kilo bytes), `m` or `mb` (mega bytes) and `g` or `gb` (giga bytes).

```text
    2b
    1024kb
    2048k
    300m
    1gb
```

## [Specifying durations](#specifying-durations)

Values express a duration as a string in the form of `{value}{unit}`. The supported units are `us` (microseconds), `ms` (milliseconds), `s` (seconds), `m` (minutes) and `h` (hours). Values can combine multiple values without separator.

```text
  10ms
  40s
  1m30s
  1h5m30s20ms
```

----
url: https://docs.docker.com/guides/docker-build-cloud/why/
----

# Why Docker Build Cloud?

***

***

Docker Build Cloud is a service that lets you build container images faster, both locally and in CI. Builds run on cloud infrastructure optimally dimensioned for your workloads, with no configuration required. The service uses a remote build cache, ensuring fast builds anywhere and for all team members.

Docker Build Cloud provides several benefits over local builds:

* Improved build speed
* Shared build cache
* Native multi-platform builds

There’s no need to worry about managing builders or infrastructure — simply connect to your builders and start building. Each cloud builder provisioned to an organization is completely isolated to a single Amazon EC2 instance, with a dedicated EBS volume for build cache and encryption in transit. That means there are no shared processes or data between cloud builders.

[Demo: set up and use Docker Build Cloud in development »](https://docs.docker.com/guides/docker-build-cloud/dev/)

----
url: https://docs.docker.com/ai/docker-agent/integrations/mcp/
----

# MCP mode

***

Table of contents

***

When you run Docker Agent in MCP mode, your agents show up as tools in Claude Desktop and other MCP clients. Instead of switching to a terminal to run your security agent, you ask Claude to use it and Claude calls it for you.

This guide covers setup for Claude Desktop and Claude Code. If you want agents embedded in your editor instead, see [ACP integration](https://docs.docker.com/ai/docker-agent/integrations/acp/).

## [How it works](#how-it-works)

You configure Claude Desktop (or another MCP client) to connect to Docker Agent. Your agents appear in Claude's tool list. When you ask Claude to use one, it calls that agent through the MCP protocol.

Say you have a security agent configured. Ask Claude Desktop "Use the security agent to audit this authentication code" and Claude calls it. The agent runs with its configured tools (filesystem, shell, whatever you gave it), then returns results to Claude.

If your configuration has multiple agents, each one becomes a separate tool. A config with `root`, `designer`, and `engineer` agents gives Claude three tools to choose from. Claude might call the engineer directly or use the root coordinator—depends on your agent descriptions and what you ask for.

## [MCP Gateway](#mcp-gateway)

Docker provides an [MCP Gateway](/ai/mcp-catalog-and-toolkit/mcp-gateway/) that gives agents access to a catalog of pre-configured MCP servers. Instead of configuring individual MCP servers, agents can use the gateway to access tools like web search, database queries, and more.

Configure MCP toolset with gateway reference:

```yaml
agents:
  root:
    toolsets:
      - type: mcp
        ref: docker:duckduckgo # Uses Docker MCP Gateway
```

The `docker:` prefix tells Docker Agent to use the MCP Gateway for this server. See the [MCP Catalog](/ai/mcp-catalog-and-toolkit/catalog/) for available servers and the [MCP Gateway documentation](/ai/mcp-catalog-and-toolkit/mcp-gateway/) for configuration options.

You can also use the [MCP Toolkit](/ai/mcp-catalog-and-toolkit/) to explore and manage MCP servers interactively.

## [Prerequisites](#prerequisites)

Before configuring MCP integration, you need:

* **Docker Agent installed** - See the [installation guide](https://docs.docker.com/ai/docker-agent/#installation)
* **Agent configuration** - A YAML file defining your agent. See the [tutorial](https://docs.docker.com/ai/docker-agent/tutorial/) or [example configurations](https://github.com/docker/docker-agent/tree/main/examples)
* **MCP client** - Claude Desktop, Claude Code, or another MCP-compatible application
* **API keys** - Environment variables for any model providers your agents use (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.)

## [MCP client configuration](#mcp-client-configuration)

Your MCP client needs to know how to start Docker Agent and communicate with it. This typically involves adding Docker Agent as an MCP server in your client's configuration.

### [Claude Desktop](#claude-desktop)

Add Docker Agent to your Claude Desktop MCP settings file:

* macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
* Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Example configuration:

```json
{
  "mcpServers": {
    "myagent": {
      "command": "docker",
      "args": [
        "agent",
        "serve",
        "mcp",
        "/path/to/agent.yml",
        "--working-dir",
        "/Users/yourname/projects"
      ],
      "env": {
        "ANTHROPIC_API_KEY": "your_anthropic_key_here",
        "OPENAI_API_KEY": "your_openai_key_here"
      }
    }
  }
}
```

Configuration breakdown:

* `command`: Full path to your `docker` binary (use `which docker` to find it), or path to `docker-agent` if not using the Docker CLI plugin

* `args`: MCP command arguments:

  * `mcp`: The subcommand to run `docker agent` in MCP mode
  * `dockereng/myagent`: Your agent configuration (local file path or OCI reference)
  * `--working-dir`: Optional working directory for agent execution

* `env`: Environment variables your agents need:

  * Model provider API keys (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, etc.)
  * Any other environment variables your agents reference

After updating the configuration, restart Claude Desktop. Your agents will appear as available tools.

### [Claude Code](#claude-code)

Add Docker Agent as an MCP server using the `claude mcp add` command:

```console
$ claude mcp add --transport stdio myagent \
  --env OPENAI_API_KEY=$OPENAI_API_KEY \
  --env ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  -- docker agent serve mcp /path/to/agent.yml --working-dir $(pwd)
```

Command breakdown:

* `claude mcp add`: Claude Code command to register an MCP server
* `--transport stdio`: Use stdio transport (standard for local MCP servers)
* `myagent`: Name for this MCP server in Claude Code
* `--env`: Pass environment variables (repeat for each variable)
* `--`: Separates Claude Code options from the MCP server command
* `docker agent serve mcp /path/to/agent.yml`: The Docker Agent MCP command with the path to your agent configuration
* `--working-dir $(pwd)`: Set the working directory for agent execution

After adding the server, your agents will be available as tools in Claude Code sessions.

### [Other MCP clients](#other-mcp-clients)

For other MCP-compatible clients, you need to:

1. Start Docker Agent with `docker agent serve mcp /path/to/agent.yml --working-dir /project/path`
2. Configure the client to communicate with Docker Agent over stdio
3. Pass required environment variables (API keys, etc.)

Consult your MCP client's documentation for specific configuration steps.

## [Agent references](#agent-references)

You can specify your agent configuration as a local file path or OCI registry reference:

```console
# Local file path
$ docker agent serve mcp ./agent.yml

# OCI registry reference
$ docker agent serve mcp agentcatalog/pirate
$ docker agent serve mcp dockereng/myagent:v1.0.0
```

Use the same syntax in MCP client configurations:

```json
{
  "mcpServers": {
    "myagent": {
      "command": "docker",
      "args": ["agent", "serve", "mcp", "agentcatalog/pirate"]
    }
  }
}
```

Registry references let your team use the same agent configuration without managing local files. See [Sharing agents](https://docs.docker.com/ai/docker-agent/sharing-agents/) for details.

## [Designing agents for MCP](#designing-agents-for-mcp)

MCP clients see each of your agents as a separate tool and can call any of them directly. This changes how you should think about agent design compared to running agents with `docker agent run`.

### [Write good descriptions](#write-good-descriptions)

The `description` field tells the MCP client what the agent does. This is how the client decides when to call it. "Analyzes code for security vulnerabilities and compliance issues" is specific. "A helpful security agent" doesn't say what it actually does.

```yaml
agents:
  security_auditor:
    description: Analyzes code for security vulnerabilities and compliance issues
    # Not: "A helpful security agent"
```

### [MCP clients call agents directly](#mcp-clients-call-agents-directly)

The MCP client can call any of your agents, not just root. If you have `root`, `designer`, and `engineer` agents, the client might call the engineer directly instead of going through root. Design each agent to work on its own:

```yaml
agents:
  engineer:
    description: Implements features and writes production code
    instruction: |
      You implement code based on requirements provided.
      You can work independently without a coordinator.
    toolsets:
      - type: filesystem
      - type: shell
```

If an agent needs others to work properly, say so in the description: "Coordinates design and engineering agents to implement complete features."

### [Test each agent on its own](#test-each-agent-on-its-own)

MCP clients call agents individually, so test them that way:

```console
$ docker agent run agent.yml --agent engineer
```

Make sure the agent works without going through root first. Check that it has the right tools and that its instructions make sense when it's called directly.

## [Testing your setup](#testing-your-setup)

Verify your MCP integration works:

1. Restart your MCP client after configuration changes
2. Check that agents appear as available tools
3. Invoke an agent with a simple test prompt
4. Verify the agent can access its configured tools (filesystem, shell, etc.)

If agents don't appear or fail to execute, check:

* `docker agent` command is available and executable
* Agent configuration file exists and is valid
* All required API keys are set in environment variables
* Working directory path exists and has appropriate permissions
* MCP client logs for connection or execution errors

## [Common workflows](#common-workflows)

### [Call specialist agents](#call-specialist-agents)

You have a security agent that knows your compliance rules and common vulnerabilities. In Claude Desktop, paste some authentication code and ask "Use the security agent to review this." The agent checks the code and reports what it finds. You stay in Claude's interface the whole time.

### [Work with agent teams](#work-with-agent-teams)

Your configuration has a coordinator that delegates to designer and engineer agents. Ask Claude Code "Use the coordinator to implement a login form" and the coordinator hands off UI work to the designer and code to the engineer. You get a complete implementation without running `docker agent run` yourself.

### [Run domain-specific tools](#run-domain-specific-tools)

You built an infrastructure agent with custom deployment scripts and monitoring queries. Ask any MCP client "Use the infra agent to check production status" and it runs your tools and returns results. Your deployment knowledge is now available wherever you use MCP clients.

### [Share agents](#share-agents)

Your team keeps agents in an OCI registry. Everyone adds `agentcatalog/security-expert` to their MCP client config. When you update the agent, they get the new version on their next restart. No YAML files to pass around.

## [What's next](#whats-next)

* Use the [MCP Gateway](/ai/mcp-catalog-and-toolkit/mcp-gateway/) to give your agents access to pre-configured MCP servers
* Explore MCP servers interactively with the [MCP Toolkit](/ai/mcp-catalog-and-toolkit/)
* Review the [configuration reference](https://docs.docker.com/ai/docker-agent/reference/config/) for advanced agent setup
* Explore the [toolsets reference](https://docs.docker.com/ai/docker-agent/reference/toolsets/) to learn what tools agents can use
* Add [RAG for codebase search](https://docs.docker.com/ai/docker-agent/rag/) to your agent
* Check the [CLI reference](https://docs.docker.com/ai/docker-agent/reference/cli/) for all `docker agent serve mcp` options
* Browse [example configurations](https://github.com/docker/docker-agent/tree/main/examples) for different agent types

----
url: https://docs.docker.com/docker-hub/repos/delete/
----

# Delete a repository

***

***

> Warning
>
> Deleting a repository deletes all the images it contains and its build settings. This action can't be undone.

1. Sign in to [Docker Hub](https://hub.docker.com).

2. Select **My Hub** > **Repositories**.

   A list of your repositories appears.

3. Select a repository.

   The **General** page for the repository appears.

4. Select the **Settings** tab.

5. Select **Delete repository**.

6. Enter the name of your repository to confirm.

7. Select **Delete Repository Forever**.

----
url: https://docs.docker.com/extensions/extensions-sdk/design/
----

# UI styling overview for Docker extensions

***

Table of contents

***

Our Design System is a constantly evolving set of specifications that aim to ensure visual consistency across Docker products, and meet [level AA accessibility standards](https://www.w3.org/WAI/WCAG2AA-Conformance). We've opened parts of it to extension authors, documenting basic styles (color, typography) and components. See: [Docker Extensions Styleguide](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771).

We require extensions to match the wider Docker Desktop UI to a certain degree, and reserve the right to make this stricter in the future.

To get started on your UI, follow the steps below.

## [Step one: Choose your framework](#step-one-choose-your-framework)

### [Recommended: React+MUI, using our theme](#recommended-reactmui-using-our-theme)

Docker Desktop's UI is written in React and [MUI](https://mui.com/) (using Material UI specifically). This is the only officially supported framework for building extensions, and the one that the `init` command automatically configures for you. Using it brings significant benefits to authors:

* You can use our [Material UI theme](https://www.npmjs.com/package/@docker/docker-mui-theme) to automatically replicate Docker Desktop's look and feel.
* In future, we'll release utilities and components specifically targeting this combination (e.g. custom MUI components, or React hooks for interacting with Docker).

Read our [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/) guide to learn future-proof ways to use MUI with Docker Desktop.

### [Not recommended: Some other framework](#not-recommended-some-other-framework)

You may prefer to use another framework, perhaps because you or your team are more familiar with it or because you have existing assets you want to reuse. This is possible, but highly discouraged. It means that:

* You'll need to manually replicate the look and feel of Docker Desktop. This takes a lot of effort, and if you don't match our theme closely enough, users will find your extension jarring and we may ask you to make changes during a review process.
* You'll have a higher maintenance burden. Whenever Docker Desktop's theme changes (which could happen in any release), you'll need to manually change your extension to match it.
* If your extension is open-source, deliberately avoiding common conventions will make it harder for the community to contribute to it.

## [Step two: Follow the below recommendations](#step-two-follow-the-below-recommendations)

### [Follow our MUI best practices (if applicable)](#follow-our-mui-best-practices-if-applicable)

See our [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/) article.

### [Only use colors from our palette](#only-use-colors-from-our-palette)

With minor exceptions, displaying your logo for example, you should only use colors from our palette. These can be found in our [style guide document](https://www.figma.com/file/U7pLWfEf6IQKUHLhdateBI/Docker-Design-Guidelines?node-id=1%3A28771), and will also soon be available in our MUI theme and via CSS variables.

### [Use counterpart colors in light/dark mode](#use-counterpart-colors-in-lightdark-mode)

Our colors have been chosen so that the counterpart colors in each variant of the palette should have the same essential characteristics. Anywhere you use `red-300` in light mode, you should use `red-300` in dark mode too.

## [What's next?](#whats-next)

* Take a look at our [MUI best practices](https://docs.docker.com/extensions/extensions-sdk/design/mui-best-practices/).
* Learn how to [publish your extension](https://docs.docker.com/extensions/extensions-sdk/extensions/).

----
url: https://docs.docker.com/compose/how-tos/file-watch/
----

# Use Compose Watch

***

Table of contents

***

Requires: Docker Compose [2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0) and later

The `watch` attribute automatically updates and previews your running Compose services as you edit and save your code. For many projects, this enables a hands-off development workflow once Compose is running, as services automatically update themselves when you save your work.

`watch` adheres to the following file path rules:

* All paths are relative to the project directory, apart from ignore file patterns

* Directories are watched recursively

* Glob patterns aren't supported

* Rules from `.dockerignore` apply

  * Use `ignore` option to define additional paths to be ignored (same syntax)
  * Temporary/backup files for common IDEs (Vim, Emacs, JetBrains, & more) are ignored automatically
  * `.git` directories are ignored automatically

You don't need to switch on `watch` for all services in a Compose project. In some instances, only part of the project, for example the Javascript frontend, might be suitable for automatic updates.

Compose Watch is designed to work with services built from local source code using the `build` attribute. It doesn't track changes for services that rely on pre-built images specified by the `image` attribute.

## [Compose Watch versus bind mounts](#compose-watch-versus-bind-mounts)

Compose supports sharing a host directory inside service containers. Watch mode does not replace this functionality but exists as a companion specifically suited to developing in containers.

More importantly, `watch` allows for greater granularity than is practical with a bind mount. Watch rules let you ignore specific files or entire directories within the watched tree.

For example, in a JavaScript project, ignoring the `node_modules/` directory has two benefits:

* Performance. File trees with many small files can cause a high I/O load in some configurations
* Multi-platform. Compiled artifacts cannot be shared if the host OS or architecture is different from the container

For example, in a Node.js project, it's not recommended to sync the `node_modules/` directory. Even though JavaScript is interpreted, `npm` packages can contain native code that is not portable across platforms.

## [Configuration](#configuration)

The `watch` attribute defines a list of rules that control automatic service updates based on local file changes.

Each rule requires a `path` pattern and `action` to take when a modification is detected. There are two possible actions for `watch` and depending on the `action`, additional fields might be accepted or required.

Watch mode can be used with many different languages and frameworks. The specific paths and rules will vary from project to project, but the concepts remain the same.

### [Prerequisites](#prerequisites)

In order to work properly, `watch` relies on common executables. Make sure your service image contains the following binaries:

* stat
* mkdir
* rmdir

`watch` also requires that the container's `USER` can write to the target path so it can update files. A common pattern is for initial content to be copied into the container using the `COPY` instruction in a Dockerfile. To ensure such files are owned by the configured user, use the `COPY --chown` flag:

```dockerfile
# Run as a non-privileged user
FROM node:18
RUN useradd -ms /bin/sh -u 1001 app
USER app

# Install dependencies
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install

# Copy source files into application directory
COPY --chown=app:app . /app
```

### [`action`](#action)

#### [Sync](#sync)

If `action` is set to `sync`, Compose makes sure any changes made to files on your host automatically match with the corresponding files within the service container.

`sync` is ideal for frameworks that support "Hot Reload" or equivalent functionality.

More generally, `sync` rules can be used in place of bind mounts for many development use cases.

#### [Rebuild](#rebuild)

If `action` is set to `rebuild`, Compose automatically builds a new image with BuildKit and replaces the running service container.

The behavior is the same as running `docker compose up --build <svc>`.

Rebuild is ideal for compiled languages or as a fallback for modifications to particular files that require a full image rebuild (e.g. `package.json`).

#### [Sync + Restart](#sync--restart)

If `action` is set to `sync+restart`, Compose synchronizes your changes with the service containers and restarts them.

`sync+restart` is ideal when the config file changes, and you don't need to rebuild the image but just restart the main process of the service containers. It will work well when you update a database configuration or your `nginx.conf` file, for example.

> Tip
>
> Optimize your `Dockerfile` for speedy incremental rebuilds with [image layer caching](/build/cache) and [multi-stage builds](/build/building/multi-stage/).

### [`path` and `target`](#path-and-target)

The `target` field controls how the path is mapped into the container.

For `path: ./app/html` and a change to `./app/html/index.html`:

* `target: /app/html` -> `/app/html/index.html`
* `target: /app/static` -> `/app/static/index.html`
* `target: /assets` -> `/assets/index.html`

### [`ignore`](#ignore)

The `ignore` patterns are relative to the `path` defined in the current `watch` action, not to the project directory. In the following Example 1, the ignore path would be relative to the `./web` directory specified in the `path` attribute.

### [`initial_sync`](#initial_sync)

When using a `sync+x` action, the `initial_sync` attribute tells Compose to ensure files that are part of the defined `path` are up to date before starting a new watch session.

## [Example 1](#example-1)

This minimal example targets a Node.js application with the following structure:

```text
myproject/
├── web/
│   ├── App.jsx
│   ├── index.js
│   └── node_modules/
├── Dockerfile
├── compose.yaml
└── package.json
```

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /src/web
          initial_sync: true
          ignore:
            - node_modules/
        - action: rebuild
          path: package.json
```

In this example, when running `docker compose up --watch`, a container for the `web` service is launched using an image built from the `Dockerfile` in the project's root. The `web` service runs `npm start` for its command, which then launches a development version of the application with Hot Module Reload enabled in the bundler (Webpack, Vite, Turbopack, etc).

After the service is up, the watch mode starts monitoring the target directories and files. Then, whenever a source file in the `web/` directory is changed, Compose syncs the file to the corresponding location under `/src/web` inside the container. For example, `./web/App.jsx` is copied to `/src/web/App.jsx`.

Once copied, the bundler updates the running application without a restart.

And in this case, the `ignore` rule would apply to `myproject/web/node_modules/`, not `myproject/node_modules/`.

Unlike source code files, adding a new dependency can’t be done on-the-fly, so whenever `package.json` is changed, Compose rebuilds the image and recreates the `web` service container.

This pattern can be followed for many languages and frameworks, such as Python with Flask: Python source files can be synced while a change to `requirements.txt` should trigger a rebuild.

## [Example 2](#example-2)

Adapting the previous example to demonstrate `sync+restart`:

```yaml
services:
  web:
    build: .
    command: npm start
    develop:
      watch:
        - action: sync
          path: ./web
          target: /app/web
          ignore:
            - node_modules/
        - action: sync+restart
          path: ./proxy/nginx.conf
          target: /etc/nginx/conf.d/default.conf

  backend:
    build:
      context: backend
      target: builder
```

This setup demonstrates how to use the `sync+restart` action in Docker Compose to efficiently develop and test a Node.js application with a frontend web server and backend service. The configuration ensures that changes to the application code and configuration files are quickly synchronized and applied, with the `web` service restarting as needed to reflect the changes.

## [Use `watch`](#use-watch)

1. Add `watch` sections to one or more services in `compose.yaml`.
2. Run `docker compose up --watch` to build and launch a Compose project and start the file watch mode.
3. Edit service source files using your preferred IDE or editor.

> Note
>
> Watch can also be used with the dedicated `docker compose watch` command if you don't want to get the application logs mixed with the (re)build logs and filesystem sync events.

> Tip
>
> Check out [`dockersamples/avatars`](https://github.com/dockersamples/avatars), or [local setup for Docker docs](https://github.com/docker/docs/blob/main/CONTRIBUTING.md) for a demonstration of Compose `watch`.

## [Reference](#reference)

* [Compose Develop Specification](https://docs.docker.com/reference/compose-file/develop/)

----
url: https://docs.docker.com/reference/cli/sbx/completion/
----

# sbx completion

| Description | Generate the autocompletion script for the specified shell |
| ----------- | ---------------------------------------------------------- |

## [Description](#description)

Generate the autocompletion script for sbx for the specified shell. See each sub-command's help for details on how to use the generated script.

## [Commands](#commands)

| Command                                                                                         | Description                                       |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------- |
| [`sbx completion bash`](https://docs.docker.com/reference/cli/sbx/completion/bash/)             | Generate the autocompletion script for bash       |
| [`sbx completion fish`](https://docs.docker.com/reference/cli/sbx/completion/fish/)             | Generate the autocompletion script for fish       |
| [`sbx completion powershell`](https://docs.docker.com/reference/cli/sbx/completion/powershell/) | Generate the autocompletion script for powershell |
| [`sbx completion zsh`](https://docs.docker.com/reference/cli/sbx/completion/zsh/)               | Generate the autocompletion script for zsh        |

## [Global options](#global-options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

----
url: https://docs.docker.com/dhi/get-started/
----

# Docker Hardened Images quickstart

***

Table of contents

***

This guide shows you how to go from zero to running a Docker Hardened Image (DHI) using a real example. At the end, you'll compare the DHI to a standard Docker image to better understand the differences. While the steps use a specific image as an example, they can be applied to any DHI.

This quickstart uses DHI Community images from `dhi.io`. You sign in with your Docker account, pull and run an image, and compare it with a Docker Official Image.

> Note
>
> If you have a DHI Select or Enterprise subscription, see [Get started with DHI Select and Enterprise](https://docs.docker.com/dhi/how-to/select-enterprise/) instead. Select and Enterprise use mirrored repositories in your organization namespace on Docker Hub to enable customization, SLA-backed security updates, and access to compliance variants.

## [Step 1: Find an image to use](#step-1-find-an-image-to-use)

1. Go to the Hardened Images catalog in [Docker Hub](https://hub.docker.com/hardened-images/catalog).
2. Use the search bar or filters to find an image (for example, `python`, `node`, or `golang`). For this example, search for `python`.
3. Select the Python repository to view its details.

Continue to the next step to pull and run the image. To dive deeper into searching and evaluating images, see [Search and evaluate Docker Hardened Images](https://docs.docker.com/dhi/how-to/explore/).

## [Step 2: Pull and run the image](#step-2-pull-and-run-the-image)

You can pull and run a DHI like any other Docker image. Note that Docker Hardened Images are designed to be minimal and secure, so they may not include all the tools or libraries you expect in a typical image. You can view the typical differences in [Considerations when adopting DHIs](https://docs.docker.com/dhi/how-to/use/#considerations-when-adopting-dhis).

The following example demonstrates that you can run the Python image and execute a simple Python command just like you would with any other Docker image:

1. Open a terminal and sign in to the Docker Hardened Images registry using your Docker account credentials.

   ```console
   $ docker login dhi.io
   ```

   > Tip
   >
   > If you don't have a Docker account, [create a free account](https://hub.docker.com/signup) to get started.

2. Pull the image:

   ```console
   $ docker pull dhi.io/python:3.13
   ```

3. Run the image to confirm everything works:

   ```console
   $ docker run --rm dhi.io/python:3.13 python -c "print('Hello from DHI')"
   ```

   This starts a container from the `python:3.13` image and runs a simple Python script that prints `Hello from DHI`.

To dive deeper into using images, see:

* [Use a Docker Hardened Image](https://docs.docker.com/dhi/how-to/use/) for general usage
* [Use a Helm chart](https://docs.docker.com/dhi/how-to/helm/) for deploying with Helm

## [Step 3: Compare with other images](#step-3-compare-with-other-images)

You can quickly compare DHIs with other images to see the security improvements and differences. This comparison helps you understand the value of using hardened images.

Run the following command to compare the Docker Hardened Image for Python with the non-hardened Docker Official Image for Python from Docker Hub. Look for the `## Overview` section in the output for a summary comparison.

```console
$ docker scout compare dhi.io/python:3.13 \
    --to python:3.13 \
    --platform linux/amd64 \
    --ignore-unchanged
```

The `## Overview` section of the output looks similar to the following:

```plaintext
  ## Overview

                      │                    Analyzed Image                     │               Comparison Image
  ────────────────────┼───────────────────────────────────────────────────────┼───────────────────────────────────────────────
    Target            │  dhi.io/python:3.13                                   │  python:3.13
      digest          │  c215e9da9f84                                         │  7f48e892134c
      tag             │  3.13                                                 │  3.13
      platform        │ linux/amd64                                           │ linux/amd64
      provenance      │ https://github.com/docker-hardened-images/definitions │ https://github.com/docker-library/python.git
                      │  77a629b3d0db035700206c2a4e7ed904e5902ea8             │  3f2d7e4c339ab883455b81a873519f1d0f2cd80a
      vulnerabilities │    0C     0H     0M     0L                            │    0C     1H     5M   141L     2?
                      │           -1     -5   -141     -2                     │
      size            │ 35 MB (-377 MB)                                       │ 412 MB
      packages        │ 80 (-530)                                             │ 610
                      │                                                       │
```

> Note
>
> This is example output. Your results may vary depending on newly discovered CVEs and image updates.

Docker maintains near-zero CVEs in Docker Hardened Images. For DHI Select and Enterprise subscriptions, when new CVEs are discovered, the CVEs are remediated within the industry-leading SLA time frame. Learn more about the [SLA-backed security features](https://docs.docker.com/dhi/features/#sla-backed-security).

This comparison shows that the Docker Hardened Image:

* Removes vulnerabilities: 1 high, 5 medium, 141 low, and 2 unspecified severity CVEs removed
* Reduces size: From 412 MB down to 35 MB (91% reduction)
* Minimizes packages: From 610 packages down to 80 (87% reduction)

To dive deeper into comparing images see [Search and evaluate Docker Hardened Images](https://docs.docker.com/dhi/how-to/explore/#compare-and-evaluate-images).

## [What's next](#whats-next)

You've pulled and run your first Docker Hardened Image. Here are a few ways to keep going:

* [Migrate existing applications to DHIs](https://docs.docker.com/dhi/migration/migrate-with-ai/): Use Gordon to update your Dockerfiles to use Docker Hardened Images as the base.

* [Start a trial](https://hub.docker.com/hardened-images/start-free-trial) to explore the benefits of a DHI subscription, such as access to FIPS and STIG variants, customized images, and SLA-backed updates.

* [Get started with DHI Select and Enterprise](https://docs.docker.com/dhi/how-to/select-enterprise/): After subscribing to a DHI subscription or starting a trial, learn how to mirror repositories, customize images, and access compliance variants.

* [Verify DHIs](https://docs.docker.com/dhi/how-to/verify/): Use tools like [Docker Scout](/scout/) or Cosign to inspect and verify signed attestations, like SBOMs and provenance.

* [Scan DHIs](https://docs.docker.com/dhi/how-to/scan/): Analyze the image with Docker Scout or other scanners to identify known CVEs.

----
url: https://docs.docker.com/reference/cli/docker/mcp/server/
----

# docker mcp server

***

| Description | Manage servers |
| ----------- | -------------- |

## [Description](#description)

Manage servers

## [Subcommands](#subcommands)

| Command                                                                                   | Description                         |
| ----------------------------------------------------------------------------------------- | ----------------------------------- |
| [`docker mcp server init`](https://docs.docker.com/reference/cli/docker/mcp/server/init/) | Initialize a new MCP server project |

----
url: https://docs.docker.com/engine/release-notes/17.07/
----

# Docker Engine 17.07 release notes

***

Table of contents

***

## [17.07.0-ce](#17070-ce)

2017-08-29

### [API & Client](#api--client)

* Add support for proxy configuration in config.json [docker/cli#93](https://github.com/docker/cli/pull/93)
* Enable pprof/debug endpoints by default [moby/moby#32453](https://github.com/moby/moby/pull/32453)
* Passwords can now be passed using `STDIN` using the new `--password-stdin` flag on `docker login` [docker/cli#271](https://github.com/docker/cli/pull/271)

- Add `--detach` to docker scale [docker/cli#243](https://github.com/docker/cli/pull/243)

* Prevent `docker logs --no-stream` from hanging due to non-existing containers [moby/moby#34004](https://github.com/moby/moby/pull/34004)

- Fix `docker stack ps` printing error to `stdout` instead of `stderr` [docker/cli#298](https://github.com/docker/cli/pull/298)

* Fix progress bar being stuck on `docker service create` if an error occurs during deploy [docker/cli#259](https://github.com/docker/cli/pull/259)
* Improve presentation of progress bars in interactive mode [docker/cli#260](https://github.com/docker/cli/pull/260) [docker/cli#237](https://github.com/docker/cli/pull/237)
* Print a warning if `docker login --password` is used, and recommend `--password-stdin` [docker/cli#270](https://github.com/docker/cli/pull/270)
* Make API version negotiation more robust [moby/moby#33827](https://github.com/moby/moby/pull/33827)
* Hide `--detach` when connected to daemons older than Docker 17.05 [docker/cli#219](https://github.com/docker/cli/pull/219)

- Add `scope` filter in `GET /networks/(id or name)` [moby/moby#33630](https://github.com/moby/moby/pull/33630)

### [Builder](#builder)

* Implement long running interactive session and sending build context incrementally [moby/moby#32677](https://github.com/moby/moby/pull/32677) [docker/cli#231](https://github.com/docker/cli/pull/231) [moby/moby#33859](https://github.com/moby/moby/pull/33859)
* Warn on empty continuation lines [moby/moby#33719](https://github.com/moby/moby/pull/33719)

- Fix `.dockerignore` entries with a leading `/` not matching anything [moby/moby#32088](https://github.com/moby/moby/pull/32088)

### [Logging](#logging)

* Fix wrong filemode for rotate log files [moby/moby#33926](https://github.com/moby/moby/pull/33926)
* Fix stderr logging for journald and syslog [moby/moby#33832](https://github.com/moby/moby/pull/33832)

### [Runtime](#runtime)

* Allow stopping of paused container [moby/moby#34027](https://github.com/moby/moby/pull/34027)

- Add quota support for the overlay2 storage driver [moby/moby#32977](https://github.com/moby/moby/pull/32977)

* Remove container locks on `docker ps` [moby/moby#31273](https://github.com/moby/moby/pull/31273)
* Store container names in memdb [moby/moby#33886](https://github.com/moby/moby/pull/33886)
* Fix race condition between `docker exec` and `docker pause` [moby/moby#32881](https://github.com/moby/moby/pull/32881)
* Devicemapper: Rework logging and add `--storage-opt dm.libdm_log_level` [moby/moby#33845](https://github.com/moby/moby/pull/33845)
* Devicemapper: Prevent "device in use" errors if deferred removal is enabled, but not deferred deletion [moby/moby#33877](https://github.com/moby/moby/pull/33877)
* Devicemapper: Use KeepAlive to prevent tasks being garbage-collected while still in use [moby/moby#33376](https://github.com/moby/moby/pull/33376)
* Report intermediate prune results if prune is cancelled [moby/moby#33979](https://github.com/moby/moby/pull/33979)

- Fix run `docker rename <container-id> new_name` concurrently resulting in the having multiple names [moby/moby#33940](https://github.com/moby/moby/pull/33940)

* Fix file-descriptor leak and error handling [moby/moby#33713](https://github.com/moby/moby/pull/33713)

- Fix SIGSEGV when running containers [docker/cli#303](https://github.com/docker/cli/pull/303)

* Prevent a goroutine leak when healthcheck gets stopped [moby/moby#33781](https://github.com/moby/moby/pull/33781)

* Image: Improve store locking [moby/moby#33755](https://github.com/moby/moby/pull/33755)

* Fix Btrfs quota groups not being removed when container is destroyed [moby/moby#29427](https://github.com/moby/moby/pull/29427)

* Libcontainerd: fix defunct containerd processes not being properly reaped [moby/moby#33419](https://github.com/moby/moby/pull/33419)

* Preparations for Linux Containers on Windows

  * LCOW: Dedicated scratch space for service VM utilities [moby/moby#33809](https://github.com/moby/moby/pull/33809)
  * LCOW: Support most operations excluding remote filesystem [moby/moby#33241](https://github.com/moby/moby/pull/33241) [moby/moby#33826](https://github.com/moby/moby/pull/33826)
  * LCOW: Change directory from lcow to "Linux Containers" [moby/moby#33835](https://github.com/moby/moby/pull/33835)
  * LCOW: pass command arguments without extra quoting [moby/moby#33815](https://github.com/moby/moby/pull/33815)
  * LCOW: Updates necessary due to platform schema change [moby/moby#33785](https://github.com/moby/moby/pull/33785)

### [Swarm mode](#swarm-mode)

* Initial support for pluggable secret backends [moby/moby#34157](https://github.com/moby/moby/pull/34157) [moby/moby#34123](https://github.com/moby/moby/pull/34123)
* Sort swarm stacks and nodes using natural sorting [docker/cli#315](https://github.com/docker/cli/pull/315)
* Make engine support cluster config event [moby/moby#34032](https://github.com/moby/moby/pull/34032)
* Only pass a join address when in the process of joining a cluster [moby/moby#33361](https://github.com/moby/moby/pull/33361)
* Fix error during service creation if a network with the same name exists both as "local" and "swarm" scoped network [docker/cli#184](https://github.com/docker/cli/pull/184)
* (experimental) Add support for plugins on swarm [moby/moby#33575](https://github.com/moby/moby/pull/33575)

----
url: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-registry/
----

# What is a registry?

***

Table of contents

***

## [Explanation](#explanation)

Now that you know what a container image is and how it works, you might wonder - where do you store these images?

Well, you can store your container images on your computer system, but what if you want to share them with your friends or use them on another machine? That's where the image registry comes in.

An image registry is a centralized location for storing and sharing your container images. It can be either public or private. [Docker Hub](https://hub.docker.com) is a public registry that anyone can use and is the default registry.

While Docker Hub is a popular option, there are many other available container registries available today, including [Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/), [Azure Container Registry (ACR)](https://azure.microsoft.com/en-in/products/container-registry), and [Google Container Registry (GCR)](https://cloud.google.com/artifact-registry). You can even run your private registry on your local system or inside your organization. For example, Harbor, JFrog Artifactory, GitLab Container registry etc.

### [Registry vs. repository](#registry-vs-repository)

While you're working with registries, you might hear the terms *registry* and *repository* as if they're interchangeable. Even though they're related, they're not quite the same thing.

A *registry* is a centralized location that stores and manages container images, whereas a *repository* is a collection of related container images within a registry. Think of it as a folder where you organize your images based on projects. Each repository contains one or more container images.

The following diagram shows the relationship between a registry, repositories, and images.

```
```

> Tip
>
> A Docker Personal plan gives you one private repository and unlimited public repositories. To get unlimited private repositories, upgrade to the [Docker Team plan](https://www.docker.com/pricing?ref=Docs\&refAction=DocsConceptsRegistry).

## [Try it out](#try-it-out)

In this hands-on, you will learn how to build and push a Docker image to the Docker Hub repository.

### [Sign up for a free Docker account](#sign-up-for-a-free-docker-account)

1. If you haven't created one yet, head over to the [Docker Hub](https://hub.docker.com) page to sign up for a new Docker account. Be sure to finish the verification steps sent to your email.

   You can use your Google or GitHub account to authenticate.

### [Create your first repository](#create-your-first-repository)

1. Sign in to [Docker Hub](https://hub.docker.com).

2. Select the **Create repository** button in the top-right corner.

3. Select your namespace (most likely your username) and enter `docker-quickstart` as the repository name.

4. Set the visibility to **Public**.

5. Select the **Create** button to create the repository.

That's it. You've successfully created your first repository. 🎉

This repository is empty right now. You'll now fix this by pushing an image to it.

### [Sign in with Docker Desktop](#sign-in-with-docker-desktop)

1. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop, if not already installed.
2. In the Docker Desktop GUI, select the **Sign in** button in the top-right corner

### [Clone sample Node.js code](#clone-sample-nodejs-code)

In order to create an image, you first need a project. To get you started quickly, you'll use a sample Node.js project found at [github.com/dockersamples/helloworld-demo-node](https://github.com/dockersamples/helloworld-demo-node). This repository contains a pre-built Dockerfile necessary for building a Docker image.

Don't worry about the specifics of the Dockerfile, as you'll learn about that in later sections.

1. Clone the GitHub repository using the following command:

   ```console
   git clone https://github.com/dockersamples/helloworld-demo-node
   ```

2. Navigate into the newly created directory.

   ```console
   cd helloworld-demo-node
   ```

3. Run the following command to build a Docker image, swapping out `YOUR_DOCKER_USERNAME` with your username.

   ```console
   docker build -t YOUR_DOCKER_USERNAME/docker-quickstart .
   ```

   > Note
   >
   > Make sure you include the dot (.) at the end of the `docker build` command. This tells Docker where to find the Dockerfile.

4. Run the following command to list the newly created Docker image:

   ```console
   docker images
   ```

   You will see output like the following:

   ```console
   REPOSITORY                                 TAG       IMAGE ID       CREATED         SIZE
   YOUR_DOCKER_USERNAME/docker-quickstart   latest    476de364f70e   2 minutes ago   170MB
   ```

5. Start a container to test the image by running the following command (swap out the username with your own username):

   ```console
   docker run -d -p 8080:8080 YOUR_DOCKER_USERNAME/docker-quickstart
   ```

   You can verify if the container is working by visiting <http://localhost:8080> with your browser.

6. Use the [`docker tag`](/reference/cli/docker/image/tag/) command to tag the Docker image. Docker tags allow you to label and version your images.

   ```console
   docker tag YOUR_DOCKER_USERNAME/docker-quickstart YOUR_DOCKER_USERNAME/docker-quickstart:1.0
   ```

7. Finally, it's time to push the newly built image to your Docker Hub repository by using the [`docker push`](/reference/cli/docker/image/push/) command:

   ```console
   docker push YOUR_DOCKER_USERNAME/docker-quickstart:1.0
   ```

8. Open [Docker Hub](https://hub.docker.com) and navigate to your repository. Navigate to the **Tags** section and see your newly pushed image.

In this walkthrough, you signed up for a Docker account, created your first Docker Hub repository, and built, tagged, and pushed a container image to your Docker Hub repository.

## [Additional resources](#additional-resources)

* [Docker Hub Quickstart](/docker-hub/quickstart/)
* [Manage Docker Hub Repositories](/docker-hub/repos/)

## [Next steps](#next-steps)

Now that you understand the basics of containers and images, you're ready to learn about Docker Compose.

[What is Docker Compose?](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-docker-compose/)

----
url: https://docs.docker.com/desktop/use-desktop/pause/
----

# Pause Docker Desktop

***

***

Pausing Docker Desktop temporarily suspends the Linux VM running Docker Engine. This saves the current state of all containers in memory and freezes all running processes, significantly reducing CPU and memory usage which is helpful for conserving battery on laptops.

To pause Docker Desktop, select the **Pause** icon to the left of the footer in the Docker Dashboard. To manually resume Docker Desktop, select the **Resume** option in the Docker menu, or run any Docker CLI command.

When you manually pause Docker Desktop, a paused status displays on the Docker menu and on the Docker Desktop Dashboard. You can still access the **Settings** and the **Troubleshoot** menu.

> Tip
>
> The Resource Saver feature is enabled by default and provides better CPU and memory savings than the manual Pause feature. See [Resource Saver mode](https://docs.docker.com/desktop/use-desktop/resource-saver/) for more info.

----
url: https://docs.docker.com/extensions/extensions-sdk/architecture/
----

# Extension architecture

***

Table of contents

***

Extensions are applications that run inside the Docker Desktop. They're packaged as Docker images, distributed through Docker Hub, and installed by users either through the Marketplace within the Docker Desktop Dashboard or the Docker Extensions CLI.

Extensions can be composed of three (optional) components:

* A frontend (or User Interface): A web application displayed in a tab of the dashboard in Docker Desktop
* A backend: One or many containerized services running in the Docker Desktop VM
* Executables: Shell scripts or binaries that Docker Desktop copies on the host when installing the extension

An extension doesn't necessarily need to have all these components, but at least one of them depending on the extension features. To configure and run those components, Docker Desktop uses a `metadata.json` file. See the [metadata](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/) section for more details.

## [The frontend](#the-frontend)

The frontend is basically a web application made from HTML, Javascript, and CSS. It can be built with a simple HTML file, some vanilla Javascript or any frontend framework, such as React or Vue.js.

When Docker Desktop installs the extension, it extracts the UI folder from the extension image, as defined by the `ui` section in the `metadata.json`. See the [ui metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#ui-section) for more details.

Every time users click on the **Extensions** tab, Docker Desktop initializes the extension's UI as if it was the first time. When they navigate away from the tab, both the UI itself and all the sub-processes started by it (if any) are terminated.

The frontend can invoke `docker` commands, communicate with the extension backend, or invoke extension executables deployed on the host, through the [Extensions SDK](https://www.npmjs.com/package/@docker/extension-api-client).

> Tip
>
> The `docker extension init` generates a React based extension. But you can still use it as a starting point for your own extension and use any other frontend framework, like Vue, Angular, Svelte, etc. or event stay with vanilla Javascript.

Learn more about [building a frontend](https://docs.docker.com/extensions/extensions-sdk/build/frontend-extension-tutorial/) for your extension.

## [The backend](#the-backend)

Alongside a frontend application, extensions can also contain one or many backend services. In most cases, the Extension does not need a backend, and features can be implemented just by invoking docker commands through the SDK. However, there are some cases when an extension requires a backend service, for example:

* To run long-running processes that must outlive the frontend
* To store data in a local database and serve them back with a REST API
* To store the extension state, like when a button starts a long-running process, so that if you navigate away from the extension and come back, the frontend can pick up where it left off
* To access specific resources in the Docker Desktop VM, for example by mounting folders in the compose file

> Tip
>
> The `docker extension init` generates a Go backend. But you can still use it as a starting point for your own extension and use any other language like Node.js, Python, Java, .Net, or any other language and framework.

Usually, the backend is made of one container that runs within the Docker Desktop VM. Internally, Docker Desktop creates a Docker Compose project, creates the container from the `image` option of the `vm` section of the `metadata.json`, and attaches it to the Compose project. See the [`vm` metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#vm-section) for more details.

In some cases, a `compose.yaml` file can be used instead of an `image`. This is useful when the backend container needs more specific options, such as mounting volumes or requesting [capabilities](https://docs.docker.com/engine/reference/run/#runtime-privilege-and-linux-capabilities) that can't be expressed just with a Docker image. The `compose.yaml` file can also be used to add multiple containers needed by the extension, like a database or a message broker. Note that, if the Compose file defines many services, the SDK can only contact the first of them.

> Note
>
> In some cases, it is useful to also interact with the Docker engine from the backend. See [How to use the Docker socket](https://docs.docker.com/extensions/extensions-sdk/guides/use-docker-socket-from-backend/) from the backend.

To communicate with the backend, the Extension SDK provides [functions](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/#get) to make `GET`, `POST`, `PUT`, `HEAD`, and `DELETE` requests from the frontend. Under the hood, the communication is done through a socket or named pipe, depending on the operating system. If the backend was listening to a port, it would be difficult to prevent collision with other applications running on the host or in a container already. Also, some users are running Docker Desktop in constrained environments where they can't open ports on their machines.

Finally, the backend can be built with any technology, as long as it can run in a container and listen on a socket.

Learn more about [adding a backend](https://docs.docker.com/extensions/extensions-sdk/build/backend-extension-tutorial/) to your extension.

## [Executables](#executables)

In addition to the frontend and the backend, extensions can also contain executables. Executables are binaries or shell scripts that are installed on the host when the extension is installed. The frontend can invoke them with [the extension SDK](https://docs.docker.com/extensions/extensions-sdk/dev/api/backend/#invoke-an-extension-binary-on-the-host).

These executables are useful when the extension needs to interact with a third-party CLI tool, like AWS, `kubectl`, etc. Shipping those executables with the extension ensure that the CLI tool is always available, at the right version, on the users' machine.

When Docker Desktop installs the extension, it copies the executables on the host as defined by the `host` section in the `metadata.json`. See the [`host` metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) for more details.

However, since they're executed on the users' machine, they have to be available to the platform they're running on. For example, if you want to ship the `kubectl` executable, you need to provide a different version for Windows, Mac, and Linux. Multi arch images will also need to include binaries built for the right arch (AMD / ARM)

See the [host metadata section](https://docs.docker.com/extensions/extensions-sdk/architecture/metadata/#host-section) for more details.

Learn how to [invoke host binaries](https://docs.docker.com/extensions/extensions-sdk/guides/invoke-host-binaries/).

----
url: https://docs.docker.com/docker-hub/repos/manage/hub-images/
----

# Image management

***

***

Docker Hub provides powerful features for managing and organizing your repository content, ensuring that your images and artifacts are accessible, version-controlled, and easy to share. This section covers key image management tasks, including tagging, pushing images, transferring images between repositories, and supported software artifacts.

* [Tags](https://docs.docker.com/docker-hub/repos/manage/hub-images/tags/): Tags help you version and organize different iterations of your images within a single repository. This topic explains tagging and provides guidance on how to create, view, and delete tags in Docker Hub.
* [Image Management](https://docs.docker.com/docker-hub/repos/manage/hub-images/manage/): View, filter, and delete images and image indexes in your repository.
* [Software artifacts](https://docs.docker.com/docker-hub/repos/manage/hub-images/oci-artifacts/): Docker Hub supports OCI (Open Container Initiative) artifacts, allowing you to store, manage, and distribute a range of content beyond standard Docker images, including Helm charts, vulnerability reports, and more. This section provides an overview of OCI artifacts as well as some examples of pushing them to Docker Hub.
* [Push images to Hub](https://docs.docker.com/docker-hub/repos/manage/hub-images/push/): Docker Hub enables you to push local images to it, making them available for your team or the Docker community. Learn how to configure your images and use the `docker push` command to upload them to Docker Hub.
* [Move images between repositories](https://docs.docker.com/docker-hub/repos/manage/hub-images/move/): Organizing content across different repositories can help streamline collaboration and resource management. This topic details how to move images from one Docker Hub repository to another, whether for personal consolidation or to share images with an organization.

----
url: https://docs.docker.com/reference/cli/docker/search/
----

# docker search

***

| Description | Search Docker Hub for images   |
| ----------- | ------------------------------ |
| Usage       | `docker search [OPTIONS] TERM` |

## [Description](#description)

Search [Docker Hub](https://hub.docker.com) for images

## [Options](#options)

| Option                    | Default | Description                                |
| ------------------------- | ------- | ------------------------------------------ |
| [`-f, --filter`](#filter) |         | Filter output based on conditions provided |
| [`--format`](#format)     |         | Pretty-print search using a Go template    |
| [`--limit`](#limit)       |         | Max number of search results               |
| [`--no-trunc`](#no-trunc) |         | Don't truncate output                      |

## [Examples](#examples)

### [Search images by name](#search-images-by-name)

This example displays images with a name containing 'busybox':

```console
$ docker search busybox

NAME                             DESCRIPTION                                     STARS     OFFICIAL
busybox                          Busybox base image.                             316       [OK]
progrium/busybox                                                                 50
radial/busyboxplus               Full-chain, Internet enabled, busybox made...   8
odise/busybox-python                                                             2
azukiapp/busybox                 This image is meant to be used as the base...   2
ofayau/busybox-jvm               Prepare busybox to install a 32 bits JVM.       1
shingonoide/archlinux-busybox    Arch Linux, a lightweight and flexible Lin...   1
odise/busybox-curl                                                               1
ofayau/busybox-libc32            Busybox with 32 bits (and 64 bits) libs         1
peelsky/zulu-openjdk-busybox                                                     1
skomma/busybox-data              Docker image suitable for data volume cont...   1
elektritter/busybox-teamspeak    Lightweight teamspeak3 container based on...    1
socketplane/busybox                                                              1
oveits/docker-nginx-busybox      This is a tiny NginX docker image based on...   0
ggtools/busybox-ubuntu           Busybox ubuntu version with extra goodies       0
nikfoundas/busybox-confd         Minimal busybox based distribution of confd     0
openshift/busybox-http-app                                                       0
jllopis/busybox                                                                  0
swyckoff/busybox                                                                 0
powellquiring/busybox                                                            0
williamyeh/busybox-sh            Docker image for BusyBox's sh                   0
simplexsys/busybox-cli-powered   Docker busybox images, with a few often us...   0
fhisamoto/busybox-java           Busybox java                                    0
scottabernethy/busybox                                                           0
marclop/busybox-solr
```

### [Display non-truncated description (--no-trunc)](#no-trunc)

This example displays images with a name containing 'busybox', at least 3 stars and the description isn't truncated in the output:

```console
$ docker search --filter=stars=3 --no-trunc busybox

NAME                 DESCRIPTION                                                                               STARS     OFFICIAL
busybox              Busybox base image.                                                                       325       [OK]
progrium/busybox                                                                                               50
radial/busyboxplus   Full-chain, Internet enabled, busybox made from scratch. Comes in git and cURL flavors.   8
```

### [Limit search results (--limit)](#limit)

The flag `--limit` is the maximum number of results returned by a search. If no value is set, the default is set by the daemon.

### [Filtering (--filter)](#filter)

The filtering flag (`-f` or `--filter`) format is a `key=value` pair. If there is more than one filter, then pass multiple flags (e.g. `--filter is-official=true --filter stars=3`).

The currently supported filters are:

* stars (int - number of stars the image has)
* is-automated (boolean - true or false) - is the image automated or not (deprecated)
* is-official (boolean - true or false) - is the image official or not

#### [stars](#stars)

This example displays images with a name containing 'busybox' and at least 3 stars:

```console
$ docker search --filter stars=3 busybox

NAME                 DESCRIPTION                                     STARS     OFFICIAL
busybox              Busybox base image.                             325       [OK]
progrium/busybox                                                     50
radial/busyboxplus   Full-chain, Internet enabled, busybox made...   8
```

#### [is-official](#is-official)

This example displays images with a name containing 'busybox', at least 3 stars and are official builds:

```console
$ docker search --filter is-official=true --filter stars=3 busybox

NAME      DESCRIPTION           STARS     OFFICIAL
busybox   Busybox base image.   325       [OK]
```

### [Format the output (--format)](#format)

The formatting option (`--format`) pretty-prints search output using a Go template.

Valid placeholders for the Go template are:

| Placeholder    | Description                   |
| -------------- | ----------------------------- |
| `.Name`        | Image Name                    |
| `.Description` | Image description             |
| `.StarCount`   | Number of stars for the image |
| `.IsOfficial`  | "OK" if image is official     |

When you use the `--format` option, the `search` command will output the data exactly as the template declares. If you use the `table` directive, column headers are included as well.

The following example uses a template without headers and outputs the `Name` and `StarCount` entries separated by a colon (`:`) for all images:

```console
$ docker search --format "{{.Name}}: {{.StarCount}}" nginx

nginx: 5441
jwilder/nginx-proxy: 953
richarvey/nginx-php-fpm: 353
million12/nginx-php: 75
webdevops/php-nginx: 70
h3nrik/nginx-ldap: 35
bitnami/nginx: 23
evild/alpine-nginx: 14
million12/nginx: 9
maxexcloo/nginx: 7
```

This example outputs a table format:

```console
$ docker search --format "table {{.Name}}\t{{.IsOfficial}}" nginx

NAME                                     OFFICIAL
nginx                                    [OK]
jwilder/nginx-proxy
richarvey/nginx-php-fpm
jrcs/letsencrypt-nginx-proxy-companion
million12/nginx-php
webdevops/php-nginx
```

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/
----

# Enhanced Container Isolation limitations

***

Table of contents

***

Subscription: Business

For: Administrators

Enhanced Container Isolation has some platform-specific limitations and feature constraints. Understanding these limitations helps you plan your security strategy and set appropriate expectations.

## [WSL 2 security considerations](#wsl-2-security-considerations)

> Note
>
> Docker Desktop requires WSL 2 version 2.1.5 or later. ECI on the WSL 2 backend requires WSL version 2.6 or later because ECI depends on a Linux kernel version of at least 6.3.0. Check your version with `wsl --version` and update with `wsl --update` if needed.

Enhanced Container Isolation provides different security levels depending on your Windows backend configuration.

The following table compares ECI on WSL 2 and ECI on Hyper-V:

| Security feature                                   | ECI on WSL | ECI on Hyper-V | Comment                                                                                           |
| -------------------------------------------------- | ---------- | -------------- | ------------------------------------------------------------------------------------------------- |
| Strongly secure containers                         | Yes        | Yes            | Makes it harder for malicious container workloads to breach the Docker Desktop Linux VM and host. |
| Docker Desktop Linux VM protected from user access | No         | Yes            | On WSL, users can access Docker Engine directly or bypass Docker Desktop security settings.       |
| Docker Desktop Linux VM has a dedicated kernel     | No         | Yes            | On WSL, Docker Desktop can't guarantee the integrity of kernel level configs.                     |

WSL 2 security gaps include:

* Direct VM access: Users can bypass Docker Desktop security by accessing the VM directly: `wsl -d docker-desktop`. This gives users root access to modify Docker Engine settings and bypass Settings Management configurations.
* Shared kernel vulnerability: All WSL 2 distributions share the same Linux kernel instance. Other WSL distributions can modify kernel settings that affect Docker Desktop's security.

### [Recommendation](#recommendation)

Use Hyper-V backend for maximum security. WSL 2 offers better performance and resource utilization, but provides reduced security isolation.

## [Windows containers not supported](#windows-containers-not-supported)

ECI only works with Linux containers (Docker Desktop's default mode). Native Windows containers mode isn't supported.

## [Docker Build protection varies](#docker-build-protection-varies)

Docker Build protection depends on the driver and Docker Desktop version:

| Build drive        | Protection       | Version requirements                         |
| ------------------ | ---------------- | -------------------------------------------- |
| `docker` (default) | Protected        | Docker Desktop 4.30 and later (except WSL 2) |
| `docker` (legacy)  | Not protected    | Docker Desktop versions before 4.30          |
| `docker-container` | Always protected | All Docker Desktop versions                  |

The following Docker Build features don't work with ECI:

* `docker build --network=host`
* Docker Buildx entitlements: `network.host`, `security.insecure`

### [Recommendation](#recommendation-1)

Use `docker-container` build driver for builds requiring these features:

```console
$ docker buildx create --driver docker-container --use
$ docker buildx build --network=host .
```

## [Docker Desktop Kubernetes not protected in Kubeadm mode](#docker-desktop-kubernetes-not-protected-in-kubeadm-mode)

The integrated Kubernetes feature, when used with the legacy Kubeadm provisioner, doesn't benefit from ECI protection. Malicious or privileged pods can compromise the Docker Desktop VM and bypass security controls.

### [Recommendation](#recommendation-2)

Use the newer Docker Desktop Kubernetes "KinD" provisioner (see [Cluster provisioning method](https://docs.docker.com/desktop/use-desktop/kubernetes/#cluster-provisioning-method)). In this mode, and with ECI turned on, each Kubernetes node runs in an ECI-protected container, providing stronger isolation from the Docker Desktop VM. The KinD provisioner is also faster and allows for multi-node Kubernetes clusters.

## [Unprotected container types](#unprotected-container-types)

These container types currently don't benefit from ECI protection:

* Docker Extensions: Extension containers run without ECI protection
* Kubernetes pods: When using Docker Desktop's integrated Kubernetes with the old Kubeadm provisioner.

### [Recommendation](#recommendation-3)

Only use extensions from trusted sources in security-sensitive environments.

## [Global command restrictions](#global-command-restrictions)

Command lists apply to all containers allowed to mount the Docker socket. You can't configure different command restrictions per container image.

## [Local-only images not supported](#local-only-images-not-supported)

You can't allow arbitrary local-only images (images not in a registry) to mount the Docker socket, unless they're:

* Derived from an allowed base image (with `allowDerivedImages: true`)
* Using the wildcard allowlist (`"*"`, Docker Desktop 4.36 and later)

## [Unsupported Docker commands](#unsupported-docker-commands)

These Docker commands aren't yet supported in command list restrictions:

* `compose`: Docker Compose commands
* `dev`: Development environment commands
* `extension`: Docker Extensions management
* `feedback`: Docker feedback submission
* `init`: Docker initialization commands
* `manifest`: Image manifest management
* `plugin`: Plugin management
* `sbom`: Software Bill of Materials
* `scout`: Docker Scout commands
* `trust`: Image trust management

## [Performance considerations](#performance-considerations)

### [Derived images impact](#derived-images-impact)

Enabling `allowDerivedImages: true` adds approximately 1 second to container startup time for image validation.

### [Registry dependencies](#registry-dependencies)

* Docker Desktop periodically fetches image digests from registries for validation
* Initial container starts require registry access to validate allowed images
* Network connectivity issues may cause delays in container startup

### [Image digest validation](#image-digest-validation)

When allowed images are updated in registries, local containers may be unexpectedly blocked until you refresh the local image:

```console
$ docker image rm <image>
$ docker pull <image>
```

## [Production compatibility](#production-compatibility)

### [Container behavior differences](#container-behavior-differences)

Most containers run identically with and without ECI. However, some advanced workloads may behave differently:

* Containers requiring kernel module loading
* Workloads modifying global kernel settings (BPF, sysctl)
* Applications expecting specific privilege escalation behavior
* Tools requiring direct hardware device access

Test advanced workloads with ECI in development environments before production deployment to ensure compatibility.

### [Runtime considerations](#runtime-considerations)

Containers using the Sysbox runtime (with ECI) may have subtle differences compared to standard OCI runc runtime in production. These differences typically only affect privileged or system-level operations.

----
url: https://docs.docker.com/reference/cli/docker/buildx/stop/
----

# docker buildx stop

***

| Description | Stop builder instance       |
| ----------- | --------------------------- |
| Usage       | `docker buildx stop [NAME]` |

## [Description](#description)

Stops the specified or current builder. This does not prevent buildx build to restart the builder. The implementation of stop depends on the driver.

## [Examples](#examples)

### [Override the configured builder instance (--builder)](#builder)

Same as [`buildx --builder`](/reference/cli/docker/buildx/#builder).

----
url: https://docs.docker.com/engine/swarm/swarm_manager_locking/
----

# Lock your swarm to protect its encryption key

***

Table of contents

***

The Raft logs used by swarm managers are encrypted on disk by default. This at-rest encryption protects your service's configuration and data from attackers who gain access to the encrypted Raft logs. One of the reasons this feature was introduced was in support of the [Docker secrets](https://docs.docker.com/engine/swarm/secrets/) feature.

When Docker restarts, both the TLS key used to encrypt communication among swarm nodes and the key used to encrypt and decrypt Raft logs on disk are loaded into each manager node's memory. Docker has the ability to protect the mutual TLS encryption key and the key used to encrypt and decrypt Raft logs at rest, by allowing you to take ownership of these keys and to require manual unlocking of your managers. This feature is called autolock.

When Docker restarts, you must [unlock the swarm](#unlock-a-swarm) first, using a key encryption key generated by Docker when the swarm was locked. You can rotate this key encryption key at any time.

> Note
>
> You don't need to unlock the swarm when a new node joins the swarm, because the key is propagated to it over mutual TLS.

## [Initialize a swarm with autolocking enabled](#initialize-a-swarm-with-autolocking-enabled)

When you initialize a new swarm, you can use the `--autolock` flag to enable autolocking of swarm manager nodes when Docker restarts.

```console
$ docker swarm init --autolock

Swarm initialized: current node (k1q27tfyx9rncpixhk69sa61v) is now a manager.

To add a worker to this swarm, run the following command:

    docker swarm join \
    --token SWMTKN-1-0j52ln6hxjpxk2wgk917abcnxywj3xed0y8vi1e5m9t3uttrtu-7bnxvvlz2mrcpfonjuztmtts9 \
    172.31.46.109:2377

To add a manager to this swarm, run 'docker swarm join-token manager' and follow the instructions.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-WuYH/IX284+lRcXuoVf38viIDK3HJEKY13MIHX+tTt8
```

Store the key in a safe place, such as in a password manager.

When Docker restarts, you need to [unlock the swarm](#unlock-a-swarm). A locked swarm causes an error like the following when you try to start or restart a service:

```console
$ sudo service docker restart

$ docker service ls

Error response from daemon: Swarm is encrypted and needs to be unlocked before it can be used. Use "docker swarm unlock" to unlock it.
```

## [Enable or disable autolock on an existing swarm](#enable-or-disable-autolock-on-an-existing-swarm)

To enable autolock on an existing swarm, set the `autolock` flag to `true`.

```console
$ docker swarm update --autolock=true

Swarm updated.
To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-+MrE8NgAyKj5r3NcR4FiQMdgu+7W72urH0EZeSmP/0Y

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

To disable autolock, set `--autolock` to `false`. The mutual TLS key and the encryption key used to read and write Raft logs are stored unencrypted on disk. There is a trade-off between the risk of storing the encryption key unencrypted at rest and the convenience of restarting a swarm without needing to unlock each manager.

```console
$ docker swarm update --autolock=false
```

Keep the unlock key around for a short time after disabling autolocking, in case a manager goes down while it is still configured to lock using the old key.

## [Unlock a swarm](#unlock-a-swarm)

To unlock a locked swarm, use `docker swarm unlock`.

```console
$ docker swarm unlock

Please enter unlock key:
```

Enter the encryption key that was generated and shown in the command output when you locked the swarm or rotated the key, and the swarm unlocks.

## [View the current unlock key for a running swarm](#view-the-current-unlock-key-for-a-running-swarm)

Consider a situation where your swarm is running as expected, then a manager node becomes unavailable. You troubleshoot the problem and bring the physical node back online, but you need to unlock the manager by providing the unlock key to read the encrypted credentials and Raft logs.

If the key has not been rotated since the node left the swarm, and you have a quorum of functional manager nodes in the swarm, you can view the current unlock key using `docker swarm unlock-key` without any arguments.

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

If the key was rotated after the swarm node became unavailable and you do not have a record of the previous key, you may need to force the manager to leave the swarm and join it back to the swarm as a new manager.

## [Rotate the unlock key](#rotate-the-unlock-key)

You should rotate the locked swarm's unlock key on a regular schedule.

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-8jDgbUNlJtUe5P/lcr9IXGVxqZpZUXPzd+qzcGp4ZYA

Please remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

> Warning
>
> When you rotate the unlock key, keep a record of the old key around for a few minutes, so that if a manager goes down before it gets the new key, it may still be unlocked with the old one.

----
url: https://docs.docker.com/reference/cli/docker/compose/restart/
----

# docker compose restart

***

| Description | Restart service containers                      |
| ----------- | ----------------------------------------------- |
| Usage       | `docker compose restart [OPTIONS] [SERVICE...]` |

## [Description](#description)

Restarts all stopped and running services, or the specified services only.

If you make changes to your `compose.yml` configuration, these changes are not reflected after running this command. For example, changes to environment variables (which are added after a container is built, but before the container's command is executed) are not updated after restarting.

If you are looking to configure a service's restart policy, refer to [restart](https://github.com/compose-spec/compose-spec/blob/main/spec.md#restart) or [restart\_policy](https://github.com/compose-spec/compose-spec/blob/main/deploy.md#restart_policy).

## [Options](#options)

| Option          | Default | Description                           |
| --------------- | ------- | ------------------------------------- |
| `--no-deps`     |         | Don't restart dependent services      |
| `-t, --timeout` |         | Specify a shutdown timeout in seconds |

----
url: https://docs.docker.com/reference/samples/nodejs/
----

# Node.js samples

| Name                                                                                                     | Description                                                             |
| -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| [NGINX / Node.js / Redis](https://github.com/docker/awesome-compose/tree/master/nginx-nodejs-redis)      | A sample Node.js application with Nginx proxy and a Redis database.     |
| [React / Express / MySQL](https://github.com/docker/awesome-compose/tree/master/react-express-mysql)     | A sample React application with a Node.js backend and a MySQL database. |
| [React / Express / MongoDB](https://github.com/docker/awesome-compose/tree/master/react-express-mongodb) | A sample React application with a Node.js backend and a Mongo database. |
| [example-voting-app](https://github.com/dockersamples/example-voting-app)                                | A sample Docker Compose app.                                            |
| [slack-clone-docker](https://github.com/dockersamples/slack-clone-docker)                                | A sample Slack Clone app built with the MERN stack.                     |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/reference/cli/docker/buildx/
----

# docker buildx

***

| Description | Docker Buildx   |
| ----------- | --------------- |
| Usage       | `docker buildx` |

## [Description](#description)

Extended build capabilities with BuildKit

## [Options](#options)

| Option                  | Default | Description                              |
| ----------------------- | ------- | ---------------------------------------- |
| [`--builder`](#builder) |         | Override the configured builder instance |
| `-D, --debug`           |         | Enable debug logging                     |

## [Examples](#examples)

### [Override the configured builder instance (--builder)](#builder)

You can also use the `BUILDX_BUILDER` environment variable.

## [Subcommands](#subcommands)

| Command                                                                                       | Description                                      |
| --------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| [`docker buildx bake`](https://docs.docker.com/reference/cli/docker/buildx/bake/)             | Build from a file                                |
| [`docker buildx build`](https://docs.docker.com/reference/cli/docker/buildx/build/)           | Start a build                                    |
| [`docker buildx create`](https://docs.docker.com/reference/cli/docker/buildx/create/)         | Create a new builder instance                    |
| [`docker buildx dap`](https://docs.docker.com/reference/cli/docker/buildx/dap/)               | Start debug adapter protocol compatible debugger |
| [`docker buildx debug`](https://docs.docker.com/reference/cli/docker/buildx/debug/)           | Start debugger                                   |
| [`docker buildx dial-stdio`](https://docs.docker.com/reference/cli/docker/buildx/dial-stdio/) | Proxy current stdio streams to builder instance  |
| [`docker buildx du`](https://docs.docker.com/reference/cli/docker/buildx/du/)                 | Disk usage                                       |
| [`docker buildx history`](https://docs.docker.com/reference/cli/docker/buildx/history/)       | Commands to work on build records                |
| [`docker buildx imagetools`](https://docs.docker.com/reference/cli/docker/buildx/imagetools/) | Commands to work on images in registry           |
| [`docker buildx inspect`](https://docs.docker.com/reference/cli/docker/buildx/inspect/)       | Inspect current builder instance                 |
| [`docker buildx ls`](https://docs.docker.com/reference/cli/docker/buildx/ls/)                 | List builder instances                           |
| [`docker buildx policy`](https://docs.docker.com/reference/cli/docker/buildx/policy/)         | Commands for working with build policies         |
| [`docker buildx prune`](https://docs.docker.com/reference/cli/docker/buildx/prune/)           | Remove build cache                               |
| [`docker buildx rm`](https://docs.docker.com/reference/cli/docker/buildx/rm/)                 | Remove one or more builder instances             |
| [`docker buildx stop`](https://docs.docker.com/reference/cli/docker/buildx/stop/)             | Stop builder instance                            |
| [`docker buildx use`](https://docs.docker.com/reference/cli/docker/buildx/use/)               | Set the current builder instance                 |
| [`docker buildx version`](https://docs.docker.com/reference/cli/docker/buildx/version/)       | Show buildx version information                  |

----
url: https://docs.docker.com/get-started/docker-concepts/building-images/build-tag-and-publish-an-image/
----

# Build, tag, and publish an image

***

Table of contents

***

## [Explanation](#explanation)

In this guide, you will learn the following:

* Building images - the process of building an image based on a `Dockerfile`
* Tagging images - the process of giving an image a name, which also determines where the image can be distributed
* Publishing images - the process to distribute or share the newly created image using a container registry

### [Building images](#building-images)

Most often, images are built using a Dockerfile. The most basic `docker build` command might look like the following:

```bash
docker build .
```

The final `.` in the command provides the path or URL to the [build context](https://docs.docker.com/build/concepts/context/#what-is-a-build-context). At this location, the builder will find the `Dockerfile` and other referenced files.

When you run a build, the builder pulls the base image, if needed, and then runs the instructions specified in the Dockerfile.

With the previous command, the image will have no name, but the output will provide the ID of the image. As an example, the previous command might produce the following output:

```console
$ docker build .
[+] Building 3.5s (11/11) FINISHED                                              docker:desktop-linux
 => [internal] load build definition from Dockerfile                                            0.0s
 => => transferring dockerfile: 308B                                                            0.0s
 => [internal] load metadata for docker.io/library/python:3.12                                  0.0s
 => [internal] load .dockerignore                                                               0.0s
 => => transferring context: 2B                                                                 0.0s
 => [1/6] FROM docker.io/library/python:3.12                                                    0.0s
 => [internal] load build context                                                               0.0s
 => => transferring context: 123B                                                               0.0s
 => [2/6] WORKDIR /usr/local/app                                                                0.0s
 => [3/6] RUN useradd app                                                                       0.1s
 => [4/6] COPY ./requirements.txt ./requirements.txt                                            0.0s
 => [5/6] RUN pip install --no-cache-dir --upgrade -r requirements.txt                          3.2s
 => [6/6] COPY ./app ./app                                                                      0.0s
 => exporting to image                                                                          0.1s
 => => exporting layers                                                                         0.1s
 => => writing image sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00    0.0s
```

With the previous output, you could start a container by using the referenced image:

```console
docker run sha256:9924dfd9350407b3df01d1a0e1033b1e543523ce7d5d5e2c83a724480ebe8f00
```

That name certainly isn't memorable, which is where tagging becomes useful.

### [Tagging images](#tagging-images)

Tagging images is the method to provide an image with a memorable name. However, there is a structure to the name of an image. A full image name has the following structure:

```text
[HOST[:PORT_NUMBER]/]PATH[:TAG]
```

* `HOST`: The optional registry hostname where the image is located. If no host is specified, Docker's public registry at `docker.io` is used by default.
* `PORT_NUMBER`: The registry port number if a hostname is provided
* `PATH`: The path of the image, consisting of slash-separated components. For Docker Hub, the format follows `[NAMESPACE/]REPOSITORY`, where namespace is either a user's or organization's name. If no namespace is specified, `library` is used, which is the namespace for Docker Official Images.
* `TAG`: A custom, human-readable identifier that's typically used to identify different versions or variants of an image. If no tag is specified, `latest` is used by default.

Some examples of image names include:

* `nginx`, equivalent to `docker.io/library/nginx:latest`: this pulls an image from the `docker.io` registry, the `library` namespace, the `nginx` image repository, and the `latest` tag.
* `docker/welcome-to-docker`, equivalent to `docker.io/docker/welcome-to-docker:latest`: this pulls an image from the `docker.io` registry, the `docker` namespace, the `welcome-to-docker` image repository, and the `latest` tag
* `ghcr.io/dockersamples/example-voting-app-vote:pr-311`: this pulls an image from the GitHub Container Registry, the `dockersamples` namespace, the `example-voting-app-vote` image repository, and the `pr-311` tag

To tag an image during a build, add the `-t` or `--tag` flag:

```console
docker build -t my-username/my-image .
```

If you've already built an image, you can add another tag to the image by using the [`docker image tag`](https://docs.docker.com/engine/reference/commandline/image_tag/) command:

```console
docker image tag my-username/my-image another-username/another-image:v1
```

### [Publishing images](#publishing-images)

Once you have an image built and tagged, you're ready to push it to a registry. To do so, use the [`docker push`](https://docs.docker.com/engine/reference/commandline/image_push/) command:

```console
docker push my-username/my-image
```

Within a few seconds, all of the layers for your image will be pushed to the registry.

> **Requiring authentication**
>
> Before you're able to push an image to a repository, you will need to be authenticated. To do so, simply use the [docker login](https://docs.docker.com/engine/reference/commandline/login/) command.

## [Try it out](#try-it-out)

In this hands-on guide, you will build a simple image using a provided Dockerfile and push it to Docker Hub.

### [Set up](#set-up)

1. Get the sample application.

   If you have Git, you can clone the repository for the sample application. Otherwise, you can download the sample application. Choose one of the following options.

   Use the following command in a terminal to clone the sample application repository.

   ```console
   $ git clone https://github.com/docker/getting-started-todo-app
   ```

   Download the source and extract it.

   [Download the source](https://github.com/docker/getting-started-todo-app/raw/cd61f824da7a614a8298db503eed6630eeee33a3/app.zip)

2. [Download and install](https://www.docker.com/products/docker-desktop/) Docker Desktop.

3. If you don't have a Docker account yet, [create one now](https://hub.docker.com/). Once you've done that, sign in to Docker Desktop using that account.

### [Build an image](#build-an-image)

Now that you have a repository on Docker Hub, it's time for you to build an image and push it to the repository.

1. Using a terminal in the root of the sample app repository, run the following command. Replace `YOUR_DOCKER_USERNAME` with your Docker Hub username:

   ```console
   $ docker build -t YOUR_DOCKER_USERNAME/concepts-build-image-demo .
   ```

   As an example, if your username is `mobywhale`, you would run the command:

   ```console
   $ docker build -t mobywhale/concepts-build-image-demo .
   ```

2. Once the build has completed, you can view the image by using the following command:

   ```console
   $ docker image ls
   ```

   The command will produce output similar to the following:

   ```plaintext
   REPOSITORY                             TAG       IMAGE ID       CREATED          SIZE
   mobywhale/concepts-build-image-demo    latest    746c7e06537f   24 seconds ago   354MB
   ```

3. You can actually view the history (or how the image was created) by using the [docker image history](/reference/cli/docker/image/history/) command:

   ```console
   $ docker image history mobywhale/concepts-build-image-demo
   ```

   You'll then see output similar to the following:

   ```plaintext
   IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
   f279389d5f01   8 seconds ago   CMD ["node" "./src/index.js"]                   0B        buildkit.dockerfile.v0
   <missing>      8 seconds ago   EXPOSE map[3000/tcp:{}]                         0B        buildkit.dockerfile.v0 
   <missing>      8 seconds ago   WORKDIR /app                                    8.19kB    buildkit.dockerfile.v0
   <missing>      4 days ago      /bin/sh -c #(nop)  CMD ["node"]                 0B
   <missing>      4 days ago      /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B
   <missing>      4 days ago      /bin/sh -c #(nop) COPY file:4d192565a7220e13…   20.5kB
   <missing>      4 days ago      /bin/sh -c apk add --no-cache --virtual .bui…   7.92MB
   <missing>      4 days ago      /bin/sh -c #(nop)  ENV YARN_VERSION=1.22.19     0B
   <missing>      4 days ago      /bin/sh -c addgroup -g 1000 node     && addu…   126MB
   <missing>      4 days ago      /bin/sh -c #(nop)  ENV NODE_VERSION=20.12.0     0B
   <missing>      2 months ago    /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
   <missing>      2 months ago    /bin/sh -c #(nop) ADD file:d0764a717d1e9d0af…   8.42MB
   ```

   This output shows the layers of the image, highlighting the layers you added and those that were inherited from your base image.

### [Push the image](#push-the-image)

Now that you have an image built, it's time to push the image to a registry.

1. Push the image using the [docker push](/reference/cli/docker/image/push/) command:

   ```console
   $ docker push YOUR_DOCKER_USERNAME/concepts-build-image-demo
   ```

   If you receive a `requested access to the resource is denied`, make sure you are both logged in and that your Docker username is correct in the image tag.

   After a moment, your image should be pushed to Docker Hub.

## [Additional resources](#additional-resources)

To learn more about building, tagging, and publishing images, visit the following resources:

* [What is a build context?](/build/concepts/context/#what-is-a-build-context)
* [docker build reference](/reference/cli/docker/buildx/build/)
* [docker image tag reference](/reference/cli/docker/image/tag/)
* [docker push reference](/reference/cli/docker/image/push/)
* [What is a registry?](/get-started/docker-concepts/the-basics/what-is-a-registry/)

## [Next steps](#next-steps)

Now that you have learned about building and publishing images, it's time to learn how to speed up the build process using the Docker build cache.

[Using the build cache](https://docs.docker.com/get-started/docker-concepts/building-images/using-the-build-cache/)

----
url: https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/
----

# Set environment variables within your container's environment

***

Table of contents

***

A container's environment is not set until there's an explicit entry in the service configuration to make this happen. With Compose, there are two ways you can set environment variables in your containers with your Compose file.

> Tip
>
> Don't use environment variables to pass sensitive information, such as passwords, in to your containers. Use [secrets](https://docs.docker.com/compose/how-tos/use-secrets/) instead.

## [Use the `environment` attribute](#use-the-environment-attribute)

You can set environment variables directly in your container's environment with the [`environment` attribute](https://docs.docker.com/reference/compose-file/services/#environment) in your `compose.yaml`.

It supports both list and mapping syntax:

```yaml
services:
  webapp:
    environment:
      DEBUG: "true"
```

is equivalent to

```yaml
services:
  webapp:
    environment:
      - DEBUG=true
```

See [`environment` attribute](https://docs.docker.com/reference/compose-file/services/#environment) for more examples on how to use it.

### [Additional information](#additional-information)

* You can choose not to set a value and pass the environment variables from your shell straight through to your containers. It works in the same way as `docker run -e VARIABLE ...`:
  ```yaml
  web:
    environment:
      - DEBUG
  ```

The value of the `DEBUG` variable in the container is taken from the value for the same variable in the shell in which Compose is run. Note that in this case no warning is issued if the `DEBUG` variable in the shell environment is not set.

* You can also take advantage of [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#interpolation-syntax). In the following example, the result is similar to the one above but Compose gives you a warning if the `DEBUG` variable is not set in the shell environment or in an `.env` file in the project directory.

  ```yaml
  web:
    environment:
      - DEBUG=${DEBUG}
  ```

## [Use the `env_file` attribute](#use-the-env_file-attribute)

A container's environment can also be set using [`.env` files](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/#env-file) along with the [`env_file` attribute](https://docs.docker.com/reference/compose-file/services/#env_file).

```yaml
services:
  webapp:
    env_file: "webapp.env"
```

Using an `.env` file lets you use the same file for use by a plain `docker run --env-file ...` command, or to share the same `.env` file within multiple services without the need to duplicate a long `environment` YAML block.

It can also help you keep your environment variables separate from your main configuration file, providing a more organized and secure way to manage sensitive information, as you do not need to place your `.env` file in the root of your project's directory.

The [`env_file` attribute](https://docs.docker.com/reference/compose-file/services/#env_file) also lets you use multiple `.env` files in your Compose application.

The paths to your `.env` file, specified in the `env_file` attribute, are relative to the location of your `compose.yaml` file.

> Important
>
> Interpolation in `.env` files is a Docker Compose CLI feature.
>
> It is not supported when running `docker run --env-file ...`.

### [Additional information](#additional-information-1)

* If multiple files are specified, they are evaluated in order and can override values set in previous files.
* As of Docker Compose version 2.24.0, you can set your `.env` file, defined by the `env_file` attribute, to be optional by using the `required` field. When `required` is set to `false` and the `.env` file is missing, Compose silently ignores the entry.
  ```yaml
  env_file:
    - path: ./default.env
      required: true # default
    - path: ./override.env
      required: false
  ```
* As of Docker Compose version 2.30.0, you can use an alternative file format for the `env_file` with the `format` attribute. For more information, see [`format`](https://docs.docker.com/reference/compose-file/services/#format).
* Values in your `.env` file can be overridden from the command line by using [`docker compose run -e`](#set-environment-variables-with-docker-compose-run---env).

## [Set environment variables with `docker compose run --env`](#set-environment-variables-with-docker-compose-run---env)

Similar to `docker run --env`, you can set environment variables temporarily with `docker compose run --env` or its short form `docker compose run -e`:

```console
$ docker compose run -e DEBUG=1 web python console.py
```

### [Additional information](#additional-information-2)

* You can also pass a variable from the shell or your environment files by not giving it a value:

  ```console
  $ docker compose run -e DEBUG web python console.py
  ```

The value of the `DEBUG` variable in the container is taken from the value for the same variable in the shell in which Compose is run or from the environment files.

## [Further resources](#further-resources)

* [Understand environment variable precedence](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/).
* [Set or change predefined environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars/)
* [Explore best practices](https://docs.docker.com/compose/how-tos/environment-variables/best-practices/)
* [Understand interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/)

----
url: https://docs.docker.com/guides/admin-set-up/finalize-plans-and-setup/
----

# Finalize plans and begin setup

***

Table of contents

***

## [Send finalized settings files to the MDM team](#send-finalized-settings-files-to-the-mdm-team)

After reaching an agreement with the relevant teams about your baseline and security configurations as outlined in the previous section, configure Settings Management using either the [Docker Admin Console](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-admin-console/) or an [`admin-settings.json` file](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/configure-json-file/).

Once the file is ready, collaborate with your MDM team to deploy your chosen settings, along with your chosen method for [enforcing sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

> Important
>
> Test this first with a small number of Docker Desktop developers to verify the functionality works as expected before deploying more widely.

## [Manage your organizations](#manage-your-organizations)

If you have more than one organization, consider either [consolidating them into one organization](https://docs.docker.com/admin/organization/setup/orgs/) or creating a [Docker company](https://docs.docker.com/admin/company/) to manage multiple organizations.

## [Begin setup](#begin-setup)

### [Set up single sign-on and domain verification](#set-up-single-sign-on-and-domain-verification)

Single sign-on (SSO) lets developers authenticate using their identity providers (IdPs) to access Docker. SSO is available for a whole company and all associated organizations, or an individual organization that has a Docker Business subscription. For more information, see the [documentation](https://docs.docker.com/enterprise/security/single-sign-on/).

You can also enable [SCIM](https://docs.docker.com/enterprise/security/provisioning/scim/) for further automation of provisioning and deprovisioning of users.

### [Set up Docker product entitlements included in the subscription](#set-up-docker-product-entitlements-included-in-the-subscription)

[Docker Build Cloud](https://docs.docker.com/build-cloud/) significantly reduces build times, both locally and in CI, by providing a dedicated remote builder and shared cache. Powered by the cloud, developer time and local resources are freed up so your team can focus on more important things, like innovation. To get started, [set up a cloud builder](https://app.docker.com/build/).

[Docker Scout](https://docs.docker.com/scout/) is a solution for proactively enhancing your software supply chain security. By analyzing your images, Docker Scout compiles an inventory of components, also known as a Software Bill of Materials (SBOM). The SBOM is matched against a continuously updated vulnerability database to pinpoint security weaknesses. To get started, see [Quickstart](https://docs.docker.com/scout/quickstart/).

[Testcontainers Cloud](https://testcontainers.com/cloud/docs/) allows developers to run containers in the cloud, removing the need to run heavy containers on your local machine.

[Docker Hardened Images](https://docs.docker.com/dhi/) are minimal, secure, and production-ready container base and application images maintained by Docker. Designed to reduce vulnerabilities and simplify compliance, DHIs integrate easily into your existing Docker-based workflows with little to no retooling required.

### [Ensure you're running a supported version of Docker Desktop](#ensure-youre-running-a-supported-version-of-docker-desktop)

> Warning
>
> This step could affect the experience for users on older versions of Docker Desktop.

Existing users may be running outdated or unsupported versions of Docker Desktop. All users should update to a supported version. Docker Desktop versions released within the past 6 months from the latest release are supported.

Use an MDM solution to manage the version of Docker Desktop for users. Users may also get Docker Desktop directly from Docker or through a company software portal.

[Testing »](https://docs.docker.com/guides/admin-set-up/testing/)

----
url: https://docs.docker.com/reference/cli/docker/sandbox/network/proxy/
----

# docker sandbox network proxy

***

| Description | Manage proxy configuration for a sandbox           |
| ----------- | -------------------------------------------------- |
| Usage       | `docker sandbox network proxy <sandbox> [OPTIONS]` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Manage proxy configuration for a sandbox

## [Options](#options)

| Option                          | Default | Description                                                                                           |
| ------------------------------- | ------- | ----------------------------------------------------------------------------------------------------- |
| `--allow-cidr`                  |         | Remove an IP range in CIDR notation from the block or bypass lists (can be specified multiple times)  |
| [`--allow-host`](#allow-host)   |         | Permit access to a domain or IP (can be specified multiple times)                                     |
| [`--block-cidr`](#block-cidr)   |         | Block access to an IP range in CIDR notation (can be specified multiple times)                        |
| `--block-host`                  |         | Block access to a domain or IP (can be specified multiple times)                                      |
| [`--bypass-cidr`](#bypass-cidr) |         | Bypass MITM proxy for an IP range in CIDR notation (can be specified multiple times)                  |
| [`--bypass-host`](#bypass-host) |         | Bypass MITM proxy for a domain or IP (can be specified multiple times)                                |
| [`--policy`](#policy)           |         | Set the default policy                                                                                |

## [Examples](#examples)

### [Block access to a domain](#block-access-to-a-domain)

```console
$ docker sandbox network proxy my-sandbox --block-host example.com
```

### [Block multiple domains](#block-multiple-domains)

```console
$ docker sandbox network proxy my-sandbox \
  --block-host example.com \
  --block-host malicious.site
```

### [Block IP range (--block-cidr)](#block-cidr)

```text
--block-cidr CIDR
```

Block access to an IP range in CIDR notation:

```console
$ docker sandbox network proxy my-sandbox --block-cidr 192.168.1.0/24
```

### [Allow specific domain (--allow-host)](#allow-host)

```text
--allow-host DOMAIN
```

Permit access to a domain (useful with deny-by-default policy):

```console
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.trusted-service.com
```

### [Bypass MITM proxy for domain (--bypass-host)](#bypass-host)

```text
--bypass-host DOMAIN
```

Bypass MITM proxy for specific domains:

```console
$ docker sandbox network proxy my-sandbox --bypass-host localhost
```

### [Bypass MITM proxy for IP range (--bypass-cidr)](#bypass-cidr)

```text
--bypass-cidr CIDR
```

Bypass MITM proxy for an IP range:

```console
$ docker sandbox network proxy my-sandbox --bypass-cidr 127.0.0.0/8
```

### [Set default policy (--policy)](#policy)

```text
--policy allow|deny
```

Set the default policy for network access:

```console
# Allow by default, block specific hosts
$ docker sandbox network proxy my-sandbox \
  --policy allow \
  --block-host dangerous.example

# Deny by default, allow specific hosts
$ docker sandbox network proxy my-sandbox \
  --policy deny \
  --allow-host api.trusted.com \
  --allow-host cdn.trusted.com
```

### [Remove rules](#remove-rules)

Use `--allow-cidr` to remove IP ranges from block or bypass lists:

```console
$ docker sandbox network proxy my-sandbox --allow-cidr 192.168.1.0/24
```

----
url: https://docs.docker.com/reference/compose-file/develop/
----

# Compose Develop Specification

***

Table of contents

***

> Note
>
> Develop is an optional part of the Compose Specification. It is available with Docker Compose version 2.22.0 and later.

Develop lets Compose focus on the development use-case of running applications on a local machine. It also supports some development hooks to improve the velocity of your local workflow, also known as your "inner loop".

This page defines how Compose behaves to efficiently assist you and defines the development constraints and workflows set by Compose. Only a subset of Compose file services may require a `develop` subsection.

## [Illustrative example](#illustrative-example)

```yaml
services:
  frontend:
    image: example/webapp
    build: ./webapp
    develop:
      watch: 
        # sync static content
        - path: ./webapp/html
          action: sync
          target: /var/www
          ignore:
            - node_modules/

  backend:
    image: example/backend
    build: ./backend
    develop:
      watch: 
        # rebuild image and recreate service
        - path: ./backend/src
          action: rebuild
```

## [Attributes](#attributes)

The `develop` subsection defines configuration options that are applied by Compose to assist you during development of a service with optimized workflows.

### [`watch`](#watch)

The `watch` attribute defines a list of rules that control automatic service updates based on local file changes. `watch` is a sequence, each individual item in the sequence defines a rule to be applied by Compose to monitor source code for changes. For more information, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

#### [`action`](#action)

`action` defines the action to take when changes are detected. If `action` is set to:

* `rebuild`: Compose rebuilds the service image based on the `build` section and recreates the service with the updated image.
* `restart`: Compose restarts the service container. Available with Docker Compose version 2.32.0 and later.
* `sync`: Compose keeps the existing service container(s) running, but synchronizes source files with container content according to the `target` attribute.
* `sync+restart`: Compose synchronizes source files with container content according to the `target` attribute, and then restarts the container. Available with Docker Compose version 2.23.0 and later.
* `sync+exec`: Compose synchronizes source files with container content according to the `target` attribute, and then executes a command inside the container. Available with Docker Compose version 2.32.0 and later.

#### [`exec`](#exec)

Requires: Docker Compose [2.32.2](https://github.com/docker/compose/releases/tag/v2.32.2) and later

`exec` is only relevant when `action` is set to `sync+exec`. Like [service hooks](https://docs.docker.com/reference/compose-file/services/#post_start), `exec` is used to define the command to be run inside the container once it has started.

* `command`: Specifies the command to run once the container starts. This attribute is required, and you can choose to use either the shell form or the exec form.
* `user`: The user to run the command. If not set, the command is run with the same user as the main service command.
* `privileged`: Lets the command run with privileged access.
* `working_dir`: The working directory in which to run the command. If not set, it is run in the same working directory as the main service command.
* `environment`: Sets the environment variables to run the command. While the command inherits the environment variables defined for the service’s main command, this section lets you add new variables or override existing ones.

```yaml
services:
  frontend:
    image: ...
    develop:
      watch: 
        # sync content then run command to reload service without interruption
        - path: ./etc/config
          action: sync+exec
          target: /etc/config/
          exec:
            command: app reload
```

#### [`ignore`](#ignore)

The `ignore` attribute is used to define a list of patterns for paths to be ignored. Any updated file that matches a pattern, or belongs to a folder that matches a pattern, won't trigger services to be re-created. The syntax is the same as `.dockerignore` file:

* `*` matches 0 or more characters in a filename.
* `?` matches a single character in filename.
* `*/*` matches two nested folders with arbitrary names
* `**` matches an arbitrary number of nested folders

If the build context includes a `.dockerignore` file, the patterns in this file is loaded as implicit content for the `ignores` file, and values set in the Compose model are appended.

#### [`include`](#include)

It is sometimes easier to select files to be watched instead of declaring those that shouldn't be watched with `ignore`.

The `include` attribute is used to define a pattern, or a list of patterns, for paths to be considered for watching. Only files that match these patterns will be considered when applying a watch rule. The syntax is the same as `ignore`.

```yaml
services:
  backend:
    image: example/backend
    develop:
      watch: 
        # rebuild image and recreate service
        - path: ./src
          include: "*.go"  
          action: rebuild
```

> Note
>
> In many cases `include` patterns start with a wildcard (`*`) character. This has special meaning in YAML syntax to define an [alias node](https://yaml.org/spec/1.2.2/#alias-nodes) so you have to wrap pattern expression with quotes.

#### [`initial_sync`](#initial_sync)

When using `sync+x` actions, it can be useful to ensure that files inside containers are up to date at the start of a new watch session.

The `initial_sync` attribute instructs the Compose runtime, if containers for the service already exist, to check that the files from the path attribute are in sync within the service containers.

#### [`path`](#path)

`path` attribute defines the path to source code (relative to the project directory) to monitor for changes. Updates to any file inside the path, which doesn't match any `ignore` rule, triggers the configured action.

#### [`target`](#target)

`target` attribute only applies when `action` is configured for `sync`. Files within `path` that have changes are synchronized with the container's filesystem, so that the latter is always running with up-to-date content.

----
url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/
----

# Get started with Docker MCP Toolkit

***

Table of contents

***

Availability: Beta

> Note
>
> This page describes the MCP Toolkit interface in Docker Desktop 4.62 and later. Earlier versions have a different UI. Upgrade to follow these instructions exactly.

The Docker MCP Toolkit makes it easy to set up, manage, and run containerized Model Context Protocol (MCP) servers in profiles, and connect them to AI agents. It provides secure defaults and support for a growing ecosystem of LLM-based clients. This page shows you how to get started quickly with the Docker MCP Toolkit.

## [Setup](#setup)

Before you begin, make sure you meet the following requirements to get started with Docker MCP Toolkit.

1. Download and install the latest version of [Docker Desktop](/get-started/get-docker/).
2. Open the Docker Desktop settings and select **Beta features**.
3. Select **Enable Docker MCP Toolkit**.
4. Select **Apply**.

The **Learning center** in Docker Desktop provides walkthroughs and resources to help you get started with Docker products and features. On the **MCP Toolkit** page, the **Get started** walkthrough guides you through installing an MCP server, connecting a client, and testing your setup.

Alternatively, follow the step-by-step instructions on this page:

* [Create a profile](#create-a-profile) - Your workspace for organizing servers
* [Add MCP servers to your profile](#add-mcp-servers) - Select tools from the catalog
* [Connect clients](#connect-clients) - Link AI applications to your profile
* [Verify connections](#verify-connections) - Test that everything works

Once configured, your AI applications can use all the servers in your profile.

> Tip
>
> Prefer working from the terminal? See [Use MCP Toolkit from the CLI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/cli/) for instructions on using the `docker mcp` commands.

## [Create a profile](#create-a-profile)

Profiles organize your MCP servers into collections. Create a profile for your work:

> Note
>
> If you're upgrading from a previous version of MCP Toolkit, your existing server configurations are already in a `default` profile. You can continue using the default profile or create new profiles for different projects.

1. In Docker Desktop, select **MCP Toolkit** and select the **Profiles** tab.
2. Select **Create profile**.
3. Enter a name for your profile (e.g., "Frontend development").
4. Optionally, add servers and clients now, or add them later.
5. Select **Create**.

Your new profile appears in the profiles list.

## [Add MCP servers](#add-mcp-servers)

1. In Docker Desktop, select **MCP Toolkit** and select the **Catalog** tab.
2. Browse the catalog and select the servers you want to add.
3. Select the **Add to** button and choose whether you want to add the servers to an existing profile, or create a new profile.

If a server requires configuration, a **Configuration Required** badge appears next to the server's name. You must complete the mandatory configuration before you can use the server.

You've now successfully added MCP servers to your profile. Next, connect an MCP client to use the servers in your profile.

## [Connect clients](#connect-clients)

To connect a client to MCP Toolkit:

1. In Docker Desktop, select **MCP Toolkit** and select the **Clients** tab.
2. Find your application in the list.
3. Select **Connect** to configure the client.

If your client isn't listed, you can connect the MCP Toolkit manually over `stdio` by configuring your client to run the gateway with your profile:

```plaintext
docker mcp gateway run --profile my_profile
```

For example, if your client uses a JSON file to configure MCP servers, you may add an entry like:

```json
{
  "servers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "my_profile"],
      "type": "stdio"
    }
  }
}
```

Consult the documentation of the application you're using for instructions on how to set up MCP servers manually.

## [Verify connections](#verify-connections)

Refer to the relevant section for instructions on how to verify that your setup is working:

* [Claude Code](#claude-code)
* [Claude Desktop](#claude-desktop)
* [OpenAI Codex](#codex)
* [Continue](#continue)
* [Cursor](#cursor)
* [Gemini](#gemini)
* [Goose](#goose)
* [LM Studio](#lm-studio)
* [OpenCode](#opencode)
* [Sema4.ai](#sema4)
* [Visual Studio Code](#vscode)
* [Zed](#zed)

### [Claude Code](#claude-code)

If you configured the MCP Toolkit for a specific project, navigate to the relevant project directory. Then run `claude mcp list`. The output should show `MCP_DOCKER` with a "connected" status:

```console
$ claude mcp list
Checking MCP server health...

MCP_DOCKER: docker mcp gateway run - ✓ Connected
```

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```console
$ claude "Use the GitHub MCP server to show me my open pull requests"
```

### [Claude Desktop](#claude-desktop)

Restart Claude Desktop and check the **Search and tools** menu in the chat input. You should see the `MCP_DOCKER` server listed and enabled:

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### [Codex](#codex)

Run `codex mcp list` to view active MCP servers and their statuses. The `MCP_DOCKER` server should appear in the list with an "enabled" status:

```console
$ codex mcp list
Name        Command  Args             Env  Cwd  Status   Auth
MCP_DOCKER  docker   mcp gateway run  -    -    enabled  Unsupported
```

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```console
$ codex "Use the GitHub MCP server to show me my open pull requests"
```

### [Continue](#continue)

Launch the Continue terminal UI by running `cn`. Use the `/mcp` command to view active MCP servers and their statuses. The `MCP_DOCKER` server should appear in the list with a "connected" status:

```plaintext
   MCP Servers

   ➤ 🟢 MCP_DOCKER (🔧75 📝3)
     🔄 Restart all servers
     ⏹️ Stop all servers
     🔍 Explore MCP Servers
     Back

   ↑/↓ to navigate, Enter to select, Esc to go back
```

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```console
$ cn "Use the GitHub MCP server to show me my open pull requests"
```

### [Cursor](#cursor)

Open Cursor. If you configured the MCP Toolkit for a specific project, open the relevant project directory. Then navigate to **Cursor Settings > Tools & MCP**. You should see `MCP_DOCKER` under **Installed MCP Servers**:

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### [Gemini](#gemini)

Run `gemini mcp list` to view active MCP servers and their statuses. The `MCP_DOCKER` should appear in the list with a "connected" status.

```console
$ gemini mcp list
Configured MCP servers:

✓ MCP_DOCKER: docker mcp gateway run (stdio) - Connected
```

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```console
$ gemini "Use the GitHub MCP server to show me my open pull requests"
```

### [Goose](#goose)

Open the Goose desktop application and select **Extensions** in the sidebar. Under **Enabled Extensions**, you should see an extension named `Mcpdocker`:

Run `goose info -v` and look for an entry named `mcpdocker` under extensions. The status should show `enabled: true`:

```console
$ goose info -v
…
    mcpdocker:
      args:
      - mcp
      - gateway
      - run
      available_tools: []
      bundled: null
      cmd: docker
      description: The Docker MCP Toolkit allows for easy configuration and consumption of MCP servers from the Docker MCP Catalog
      enabled: true
      env_keys: []
      envs: {}
      name: mcpdocker
      timeout: 300
      type: stdio
```

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### [LM Studio](#lm-studio)

Restart LM Studio and start a new chat. Open the integrations menu and look for an entry named `mcp/mcp-docker`. Use the toggle to enable the server:

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### [OpenCode](#opencode)

The OpenCode configuration file (at `~/.config/opencode/opencode.json` by default) contains the setup for MCP Toolkit:

```json
{
  "mcp": {
    "MCP_DOCKER": {
      "type": "local",
      "command": ["docker", "mcp", "gateway", "run"],
      "enabled": true
    }
  },
  "$schema": "https://opencode.ai/config.json"
}
```

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```console
$ opencode "Use the GitHub MCP server to show me my open pull requests"
```

### [Sema4.ai Studio](#sema4)

In Sema4.ai Studio, select **Actions** in the sidebar, then select the **MCP Servers** tab. You should see Docker MCP Toolkit in the list:

To use MCP Toolkit with Sema4.ai, add it as an agent action. Find the agent you want to connect to the MCP Toolkit and open the agent editor. Select **Add Action**, enable Docker MCP Toolkit in the list, then save your agent:

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### [Visual Studio Code](#vscode)

Open Visual Studio Code. If you configured the MCP Toolkit for a specific project, open the relevant project directory. Then open the **Extensions** pane. You should see the `MCP_DOCKER` server listed under installed MCP servers.

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

### [Zed](#zed)

Launch Zed and open agent settings:

Ensure that `MCP_DOCKER` is listed and enabled in the MCP Servers section:

Test the connection by submitting a prompt that invokes one of your installed MCP servers:

```plaintext
Use the GitHub MCP server to show me my open pull requests
```

## [Further reading](#further-reading)

* [MCP Profiles](https://docs.docker.com/ai/mcp-catalog-and-toolkit/profiles/)
* [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)
* [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
* [MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)

----
url: https://docs.docker.com/get-started/introduction/
----

# Introduction

Table of contents

***

Embark on a comprehensive learning path to understand Docker and containerization, beginning with foundational concepts and installation procedures. Progress through hands-on exercises that cover essential Docker commands, image creation, and container orchestration.

**Skill level** Beginner

**Time to complete** 15 minutes

**Prerequisites** None

## [About this series](#about-this-series)

In this guide series, you will gain hands-on experience with Docker, starting with installing and setting up Docker Desktop on your local machine. You will learn how to run your first container, understanding the basics of containerization and its benefits. This series guides you through building your first Docker image, providing insights into creating efficient and reusable images. Finally, you will explore how to publish your image on Docker Hub, enabling you to share your work with the broader community and leverage Docker's powerful ecosystem for collaborative development and deployment.

## [What you'll learn](#what-youll-learn)

* Set up Docker Desktop
* Run your first container
* Build your first image
* Publish your image on Docker Hub

## [Modules](#modules)

1. [Get Docker Desktop](https://docs.docker.com/get-started/introduction/get-docker-desktop/)

   This concept page will teach you download Docker Desktop and install it on Windows, Mac, and Linux

2. [Develop with containers](https://docs.docker.com/get-started/introduction/develop-with-containers/)

   This concept page will teach you how to develop with containers

3. [Build and push your first image](https://docs.docker.com/get-started/introduction/build-and-push-first-image/)

   This concept page will teach you how to build and push your first image

4. [What's next](https://docs.docker.com/get-started/introduction/whats-next/)

   Explore step-by-step guides to help you understand core Docker concepts, building images, and running containers.

----
url: https://docs.docker.com/reference/cli/docker/buildx/policy/
----

# docker buildx policy

***

| Description | Commands for working with build policies |
| ----------- | ---------------------------------------- |

## [Description](#description)

Commands for working with build policies

## [Subcommands](#subcommands)

| Command                                                                                         | Description                  |
| ----------------------------------------------------------------------------------------------- | ---------------------------- |
| [`docker buildx policy eval`](https://docs.docker.com/reference/cli/docker/buildx/policy/eval/) | Evaluate policy for a source |
| [`docker buildx policy test`](https://docs.docker.com/reference/cli/docker/buildx/policy/test/) | Run policy tests             |

----
url: https://docs.docker.com/reference/samples/javascript/
----

# JavaScript samples

| Name                                                                                                     | Description                                                                                                                        |
| -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| [NGINX / Node.js / Redis](https://github.com/docker/awesome-compose/tree/master/nginx-nodejs-redis)      | A sample Node.js application with Nginx proxy and a Redis database.                                                                |
| [React / Spring / MySQL](https://github.com/docker/awesome-compose/tree/master/react-java-mysql)         | A sample React application with a Spring backend and a MySQL database.                                                             |
| [React / Express / MySQL](https://github.com/docker/awesome-compose/tree/master/react-express-mysql)     | A sample React application with a Node.js backend and a MySQL database.                                                            |
| [React / Express / MongoDB](https://github.com/docker/awesome-compose/tree/master/react-express-mongodb) | A sample React application with a Node.js backend and a Mongo database.                                                            |
| [React / Rust / PostgreSQL](https://github.com/docker/awesome-compose/tree/master/react-rust-postgres)   | A sample React application with a Rust backend and a Postgres database.                                                            |
| [React / NGINX](https://github.com/docker/awesome-compose/tree/master/react-nginx)                       | A sample React application with Nginx.                                                                                             |
| [VueJS](https://github.com/docker/awesome-compose/tree/master/vuejs)                                     | A sample Vue.js application.                                                                                                       |
| [docker-swarm-visualizer](https://github.com/dockersamples/docker-swarm-visualizer)                      | A visualizer for Docker Swarm Mode using the Docker Remote API, Node.JS, and D3.                                                   |
| [atsea-sample-shop-app](https://github.com/dockersamples/atsea-sample-shop-app)                          | A sample app that uses a Java Spring Boot backend connected to a database to display a fictitious art shop with a React front-end. |
| [dotnet-album-viewer](https://github.com/dockersamples/dotnet-album-viewer)                              | West Wind Album Viewer ASP.NET Core and Angular sample.                                                                            |
| [aspnet-monitoring](https://github.com/dockersamples/aspnet-monitoring)                                  | Monitoring ASP.NET Fx applications in Windows Docker containers, using Prometheus.                                                 |
| [slack-clone-docker](https://github.com/dockersamples/slack-clone-docker)                                | A sample Slack Clone app built with the MERN stack.                                                                                |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/guides/wiremock/
----

[Mocking API services in development and testing with WireMock](https://docs.docker.com/guides/wiremock/)

Mocking API services in development and testing with WireMock

JavaScript App development Distributed systems

20 minutes

[« Back to all guides](/guides/)

# Mocking API services in development and testing with WireMock

***

Table of contents

***

During local development and testing, it's quite common to encounter situations where your app is dependent on the remote APIs. Network issues, rate limits, or even downtime of the API provider can halt your progress. This can significantly hinder your productivity and make testing more challenging. This is where WireMock comes into play.

WireMock is an open-source tool that helps developers to create a mock server that simulates the behavior of real APIs, providing a controlled environment for development and testing.

Imagine you have both an API and a frontend app, and you want to test how the frontend interacts with the API. Using WireMock, you can set up a mock server to simulate the API's responses, allowing you to test the frontend behavior without relying on the actual API. This can be particularly helpful when the API is still under development or when you want to test different scenarios without affecting the actual API. WireMock supports both HTTP and HTTPS protocols and can simulate various response scenarios, including delays, errors, and different HTTP status codes.

In this guide, you'll learn how to:

* Use Docker to launch up a WireMock container.
* Use mock data in the local development without relying on an external API
* Use a Live API in production to fetch real-time weather data from AccuWeather.

## [Using WireMock with Docker](#using-wiremock-with-docker)

The official [Docker image for WireMock](https://hub.docker.com/r/wiremock/wiremock) provides a convenient way to deploy and manage WireMock instances. WireMock is available for various CPU architectures, including amd64, armv7, and armv8, ensuring compatibility with different devices and platforms. You can learn more about WireMock standalone on the [WireMock docs site](https://wiremock.org/docs/standalone/docker/).

### [Prerequisites](#prerequisites)

The following prerequisites are required to follow along with this how-to guide:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)

### [Launching WireMock](#launching-wiremock)

Launch a quick demo of WireMock by using the following steps:

1. Clone the [GitHub repository](https://github.com/dockersamples/wiremock-node-docker) locally.

   ```console
   $ git clone https://github.com/dockersamples/wiremock-node-docker
   ```

2. Navigate to the `wiremock-endpoint` directory

   ```console
   $ cd wiremock-node-docker/
   ```

   WireMock acts as the mock API that your backend will communicate with to retrieve data. The mock API responses have already been created for you in the mappings directory.

3. Start the Compose stack by running the following command at the root of the cloned project directory

   ```console
   $ docker compose up -d
   ```

   After a moment, the application will be up and running.

   You can check the logs by selecting the `wiremock-node-docker` container:

4. Test the Mock API.

   ```console
   $ curl http://localhost:8080/api/v1/getWeather\?city\=Bengaluru
   ```

   It will return the following canned response with mock data:

   ```plaintext
   {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}
   ```

   With WireMock, you define canned responses using mapping files. For this request, the mock data is defined in the JSON file at `wiremock-endpoint/mappings/getWeather/getWeatherBengaluru.json`.

   For more information about stubbing canned responses, refer to the [WireMock documentation](https://wiremock.org/docs/stubbing/).

## [Using WireMock in development](#using-wiremock-in-development)

Now that you have tried WireMock, let’s use it in development and testing. In this example, you will use a sample application that has a Node.js backend. This app stack has the following configuration:

* Local Development Environment: The context in which the Node.js backend and WireMock are running.
* Node.js Backend: Represents the backend application that handles HTTP requests.
* External AccuWeather API: The real API from which live weather data is fetched.
* WireMock: The mock server that simulates the API responses during testing. It runs as a Docker container.

- In development, the Node.js backend sends a request to WireMock instead of the actual AccuWeather API.
- In production, it connects directly to the live AccuWeather API for real data.

## [Use mock data in local development](#use-mock-data-in-local-development)

Let’s set up a Node app to send requests to the WireMock container instead of the actual AccuWeather API.

### [Prerequisite](#prerequisite)

* Install [Node.js and npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)
* Ensure that WireMock container is up and running (see [Launching Wiremock](#launching-wiremock)

Follow the steps to setup a non-containerized Node application:

1. Navigate to the `accuweather-api` directory

   Make sure you're in the directory where your `package.json` file is located.

2. Set the environment variable.

   Open `.env` file placed under `accuweather-api/` directory. Remove the old entries and ensure that it just contains the following single line.

   ```plaintext
   API_ENDPOINT_BASE=http://localhost:8080
   ```

   This will tell your Node.js application to use the WireMock server for API calls.

3. Examine the Application Entry Point

   * The main file for the application is `index.js`, located in the `accuweather-api/src/api` directory.
   * This file starts the `getWeather.js` module, which is essential for your Node.js application. It uses the `dotenv` package to load environment variables from the`.env` file.
   * Based on the value of `API_ENDPOINT_BASE`, the application routes requests either to the WireMock server (`http://localhost:8080`) or the AccuWeather API. In this setup, it uses the WireMock server.
   * The code ensures that the `ACCUWEATHER_API_KEY` is required only if the application is not using WireMock, enhancing efficiency and avoiding errors.

   ```javascript
   require("dotenv").config();

   const express = require("express");
   const axios = require("axios");

   const router = express.Router();
   const API_ENDPOINT_BASE = process.env.API_ENDPOINT_BASE;
   const API_KEY = process.env.ACCUWEATHER_API_KEY;

   console.log('API_ENDPOINT_BASE:', API_ENDPOINT_BASE);  // Log after it's defined
   console.log('ACCUWEATHER_API_KEY is set:', !!API_KEY); // Log boolean instead of actual key

   if (!API_ENDPOINT_BASE) {
     throw new Error("API_ENDPOINT_BASE is not defined in environment variables");
   }

   // Only check for API key if not using WireMock
   if (API_ENDPOINT_BASE !== 'http://localhost:8080' && !API_KEY) {
     throw new Error("ACCUWEATHER_API_KEY is not defined in environment variables");
   }
   // Function to fetch the location key for the city
   async function fetchLocationKey(townName) {
     const { data: locationData } = await
   axios.get(`${API_ENDPOINT_BASE}/locations/v1/cities/search`, {
       params: { q: townName, details: false, apikey: API_KEY },
     });
     return locationData[0]?.Key;
   }
   ```

4. Start the Node server

   Before you start the Node server, ensure that you have already installed the node packages listed in the package.json file by running `npm install`.

   ```console
   npm install 
   npm run start
   ```

   You should see the following output:

   ```plaintext
   > express-api-starter@1.2.0 start
   > node src/index.js

   API_ENDPOINT_BASE: http://localhost:8080
   ..
   Listening: http://localhost:5001
   ```

   The output indicates that your Node application has successfully started. Keep this terminal window open.

5. Test the Mocked API

   Open a new terminal window and run the following command to test the mocked API:

   ```console
   $ curl "http://localhost:5001/api/v1/getWeather?city=Bengaluru"
   ```

   You should see the following output:

   ```plaintext
   {"city":"Bengaluru","temperature":27.1,"conditions":"Mostly cloudy","forecasts":[{"date":"2024-09-02T07:00:00+05:30","temperature":83,"conditions":"Partly sunny w/ t-storms"},{"date":"2024-09-03T07:00:00+05:30","temperature":83,"conditions":"Thunderstorms"},{"date":"2024-09-04T07:00:00+05:30","temperature":83,"conditions":"Intermittent clouds"},{"date":"2024-09-05T07:00:00+05:30","temperature":82,"conditions":"Dreary"},{"date":"2024-09-06T07:00:00+05:30","temperature":82,"conditions":"Dreary"}]}%
   ```

   This indicates that your Node.js application is now successfully routing requests to the WireMock container and receiving the mocked responses

   You might have noticed that you’re trying to use `http://localhost:5001` as the URL instead of port `8080`. This is because your Node.js application is running on port `5001`, and it's routing requests to the WireMock container that's listening on port `8080`.

   > Tip
   >
   > Before you proceed to the next step, ensure that you stop the node application service.

## [Use a live API in production to fetch real-time weather data from AccuWeather](#use-a-live-api-in-production-to-fetch-real-time-weather-data-from-accuweather)

To enhance your Node.js application with real-time weather data, you can seamlessly integrate the AccuWeather API. This section of the guide will walk you through the steps involved in setting up a non-containerized Node.js application and fetching weather information directly from the AccuWeather API.

1. Create an AccuWeather API Key

   Sign up for a free AccuWeather developer account at<https://developer.accuweather.com/>. Within your account, create a new app by selecting `MY APPS` on the top navigation menu to get your unique API key.

   [AccuWeather API](https://developer.accuweather.com/) is a web API that provides real-time weather data and forecasts. Developers can use this API to integrate weather information into their applications, websites, or other projects.

2. Change directory to `accuweather-api`

   ```console
   $ cd accuweather-api
   ```

3. Set your AccuWeather API key using the `.env` file:

   > Tip
   >
   > To prevent conflicts, ensure that any existing environment variables named `API_ENDPOINT_BASE` or `ACCUWEATHER_API_KEY` are removed before modifying the `.env` file.

   Run the following command on your terminal:

   ```console
   unset API_ENDPOINT_BASE
   unset ACCUWEATHER_API_KEY
   ```

   It’s time to set the environment variables in the `.env` file:

   ```plaintext
   ACCUWEATHER_API_KEY=XXXXXX
   API_ENDPOINT_BASE=http://dataservice.accuweather.com
   ```

   Make sure to populate `ACCUWEATHER_API_KEY` with the correct value.

4. Install the dependencies

   Run the following command to install the required packages:

   ```console
   $ npm install
   ```

   This will install all the packages listed in your `package.json` file. These packages are essential for the project to function correctly.

   If you encounter any warnings related to deprecated packages, you can ignore them for now for this demonstration.

5. Assuming that you don’t have a pre-existing Node server running on your system, go ahead and start the Node server by running the following command:

   ```console
   $ npm run start
   ```

   You should see the following output:

   ```plaintext
   > express-api-starter@1.2.0 start
   > node src/index.js

   API_ENDPOINT_BASE: http://dataservice.accuweather.com
   ACCUWEATHER_API_KEY is set: true 
   Listening: http://localhost:5001
   ```

   Keep this terminal window open.

6. Run the curl command to send a GET request to the server URL.

   In the new terminal window, enter the following command:

   ```console
   $ curl "http://localhost:5000/api/v1/getWeather?city=Bengaluru"
   ```

   By running the command, you're essentially telling your local server to provide you with weather data for a city named `Bengaluru`. The request is specifically targeting the `/api/v1/getWeather` endpoint, and you're providing the query parameter `city=Bengaluru`. Once you execute the command, the server processes this request, fetches the data and returns it as a response, which `curl` will display in your terminal.

   When fetching data from the external AccuWeather API, you're interacting with live data that reflects the latest weather conditions.

## [Recap](#recap)

This guide has walked you through setting up WireMock using Docker. You’ve learned how to create stubs to simulate API endpoints, allowing you to develop and test your application without relying on external services. By using WireMock, you can create reliable and consistent test environments, reproduce edge cases, and speed up your development workflow.

----
url: https://docs.docker.com/engine/logging/drivers/syslog/
----

# Syslog logging driver

***

Table of contents

***

The `syslog` logging driver routes logs to a `syslog` server. The `syslog` protocol uses a raw string as the log message and supports a limited set of metadata. The syslog message must be formatted in a specific way to be valid. From a valid message, the receiver can extract the following information:

* Priority: the logging level, such as `debug`, `warning`, `error`, `info`.
* Timestamp: when the event occurred.
* Hostname: where the event happened.
* Facility: which subsystem logged the message, such as `mail` or `kernel`.
* Process name and process ID (PID): The name and ID of the process that generated the log.

The format is defined in [RFC 5424](https://tools.ietf.org/html/rfc5424) and Docker's syslog driver implements the [ABNF reference](https://tools.ietf.org/html/rfc5424#section-6) in the following way:

```text
                TIMESTAMP SP HOSTNAME SP APP-NAME SP PROCID SP MSGID
                    +          +             +           |        +
                    |          |             |           |        |
                    |          |             |           |        |
       +------------+          +----+        |           +----+   +---------+
       v                            v        v                v             v
2017-04-01T17:41:05.616647+08:00 a.vm {taskid:aa,version:} 1787791 {taskid:aa,version:}
```

## [Usage](#usage)

To use the `syslog` driver as the default logging driver, set the `log-driver` and `log-opt` keys to appropriate values in the `daemon.json` file. For more about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

The following example sets the log driver to `syslog` and sets the `syslog-address` option. The `syslog-address` options supports both UDP and TCP; this example uses UDP.

```json
{
  "log-driver": "syslog",
  "log-opts": {
    "syslog-address": "udp://1.2.3.4:1111"
  }
}
```

Restart Docker for the changes to take effect.

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must be provided as strings. Numeric and Boolean values (such as the value for `syslog-tls-skip-verify`) must therefore be enclosed in quotes (`"`).

You can set the logging driver for a specific container by using the `--log-driver` flag to `docker container create` or `docker run`:

```console
$ docker run \
      --log-driver syslog --log-opt syslog-address=udp://1.2.3.4:1111 \
      alpine echo hello world
```

## [Options](#options)

The following logging options are supported as options for the `syslog` logging driver. They can be set as defaults in the `daemon.json`, by adding them as key-value pairs to the `log-opts` JSON array. They can also be set on a given container by adding a `--log-opt <key>=<value>` flag for each option when starting the container.

| Option                   | Description                                                                                                                                                                                                                                                                                                      | Example value                                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| `syslog-address`         | The address of an external `syslog` server. The URI specifier may be `[tcp\|udp\|tcp+tls]://host:port`, `unix://path`, or `unixgram://path`. If the transport is `tcp`, `udp`, or `tcp+tls`, the default port is `514`.                                                                                          | `--log-opt syslog-address=tcp+tls://192.168.1.3:514`, `--log-opt syslog-address=unix:///tmp/syslog.sock` |
| `syslog-facility`        | The `syslog` facility to use. Can be the number or name for any valid `syslog` facility. See the [syslog documentation](https://tools.ietf.org/html/rfc5424#section-6.2.1).                                                                                                                                      | `--log-opt syslog-facility=daemon`                                                                       |
| `syslog-tls-ca-cert`     | The absolute path to the trust certificates signed by the CA. Ignored if the address protocol isn't `tcp+tls`.                                                                                                                                                                                                   | `--log-opt syslog-tls-ca-cert=/etc/ca-certificates/custom/ca.pem`                                        |
| `syslog-tls-cert`        | The absolute path to the TLS certificate file. Ignored if the address protocol isn't `tcp+tls`.                                                                                                                                                                                                                  | `--log-opt syslog-tls-cert=/etc/ca-certificates/custom/cert.pem`                                         |
| `syslog-tls-key`         | The absolute path to the TLS key file. Ignored if the address protocol isn't `tcp+tls`.                                                                                                                                                                                                                          | `--log-opt syslog-tls-key=/etc/ca-certificates/custom/key.pem`                                           |
| `syslog-tls-skip-verify` | If set to `true`, TLS verification is skipped when connecting to the `syslog` daemon. Defaults to `false`. Ignored if the address protocol isn't `tcp+tls`.                                                                                                                                                      | `--log-opt syslog-tls-skip-verify=true`                                                                  |
| `tag`                    | A string that's appended to the `APP-NAME` in the `syslog` message. By default, Docker uses the first 12 characters of the container ID to tag log messages. Refer to the [log tag option documentation](https://docs.docker.com/engine/logging/log_tags/) for customizing the log tag format.                   | `--log-opt tag=mailer`                                                                                   |
| `syslog-format`          | The `syslog` message format to use. If not specified the local Unix syslog format is used, without a specified hostname. Specify `rfc3164` for the RFC-3164 compatible format, `rfc5424` for RFC-5424 compatible format, or `rfc5424micro` for RFC-5424 compatible format with microsecond timestamp resolution. | `--log-opt syslog-format=rfc5424micro`                                                                   |
| `labels`                 | Applies when starting the Docker daemon. A comma-separated list of logging-related labels this daemon accepts. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                                                                                            | `--log-opt labels=production_status,geo`                                                                 |
| `labels-regex`           | Applies when starting the Docker daemon. Similar to and compatible with `labels`. A regular expression to match logging-related labels. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                                                                   | `--log-opt labels-regex=^(production_status\|geo)`                                                       |
| `env`                    | Applies when starting the Docker daemon. A comma-separated list of logging-related environment variables this daemon accepts. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                                                                             | `--log-opt env=os,customer`                                                                              |
| `env-regex`              | Applies when starting the Docker daemon. Similar to and compatible with `env`. A regular expression to match logging-related environment variables. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                                                       | `--log-opt env-regex=^(os\|customer)`                                                                    |

----
url: https://docs.docker.com/build/builders/drivers/kubernetes/
----

Start a new chat

Answers are generated based on the documentation.

[Manuals](https://docs.docker.com/manuals/)

* [Get started](/get-started/)
* [Guides](/guides/)
* [Reference](/reference/)

# Kubernetes driver

***

Table of contents

***

The Kubernetes driver lets you connect your local development or CI environments to builders in a Kubernetes cluster to allow access to more powerful compute resources, optionally on multiple native architectures.

## [Synopsis](#synopsis)

Run the following command to create a new builder, named `kube`, that uses the Kubernetes driver:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=[key=value,...]
```

The following table describes the available driver-specific options that you can pass to `--driver-opt`:

| Parameter                                  | Type         | Default                                 | Description                                                                                                                                                                                                   |
| ------------------------------------------ | ------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `image`                                    | String       |                                         | Sets the image to use for running BuildKit.                                                                                                                                                                   |
| `namespace`                                | String       | Namespace in current Kubernetes context | Sets the Kubernetes namespace.                                                                                                                                                                                |
| `default-load`                             | Boolean      | `false`                                 | Automatically load images to the Docker Engine image store.                                                                                                                                                   |
| `replicas`                                 | Integer      | 1                                       | Sets the number of Pod replicas to create. See [scaling BuildKit](#scaling-buildkit)                                                                                                                          |
| `requests.cpu`                             | CPU units    |                                         | Sets the request CPU value specified in units of Kubernetes CPU. For example `requests.cpu=100m` or `requests.cpu=2`                                                                                          |
| `requests.memory`                          | Memory size  |                                         | Sets the request memory value specified in bytes or with a valid suffix. For example `requests.memory=500Mi` or `requests.memory=4G`                                                                          |
| `requests.ephemeral-storage`               | Storage size |                                         | Sets the request ephemeral-storage value specified in bytes or with a valid suffix. For example `requests.ephemeral-storage=2Gi`                                                                              |
| `persistent-volume-claim.requests.storage` | Storage size |                                         | Sets the requested size for a persistent volume claim. When set, Buildx creates a `StatefulSet` and stores the BuildKit build cache in the claim. For example `persistent-volume-claim.requests.storage=20Gi` |
| `limits.cpu`                               | CPU units    |                                         | Sets the limit CPU value specified in units of Kubernetes CPU. For example `requests.cpu=100m` or `requests.cpu=2`                                                                                            |
| `limits.memory`                            | Memory size  |                                         | Sets the limit memory value specified in bytes or with a valid suffix. For example `requests.memory=500Mi` or `requests.memory=4G`                                                                            |
| `limits.ephemeral-storage`                 | Storage size |                                         | Sets the limit ephemeral-storage value specified in bytes or with a valid suffix. For example `requests.ephemeral-storage=100M`                                                                               |
| `buildkit-root-volume-memory`              | Memory size  | Using regular file system               | Mounts `/var/lib/buildkit` on an `emptyDir` memory-backed volume, with `SizeLimit` as the value. For example, `buildkit-root-folder-memory=6G`                                                                |
| `nodeselector`                             | CSV string   |                                         | Sets the pod's `nodeSelector` label(s). See [node assignment](#node-assignment).                                                                                                                              |
| `annotations`                              | CSV string   |                                         | Sets additional annotations on the `Deployment` or `StatefulSet` and pods.                                                                                                                                    |
| `labels`                                   | CSV string   |                                         | Sets additional labels on the `Deployment` or `StatefulSet` and pods.                                                                                                                                         |
| `tolerations`                              | CSV string   |                                         | Configures the pod's taint toleration. See [node assignment](#node-assignment).                                                                                                                               |
| `serviceaccount`                           | String       |                                         | Sets the pod's `serviceAccountName`.                                                                                                                                                                          |
| `schedulername`                            | String       |                                         | Sets the scheduler responsible for scheduling the pod.                                                                                                                                                        |
| `timeout`                                  | Time         | `120s`                                  | Set the timeout limit that determines how long Buildx will wait for pods to be provisioned before a build.                                                                                                    |
| `rootless`                                 | Boolean      | `false`                                 | Run the container as a non-root user. See [rootless mode](#rootless-mode).                                                                                                                                    |
| `loadbalance`                              | String       | `sticky`                                | Load-balancing strategy (`sticky` or `random`). If set to `sticky`, the pod is chosen using the hash of the context path.                                                                                     |
| `qemu.install`                             | Boolean      | `false`                                 | Install QEMU emulation for multi platforms support. See [QEMU](#qemu).                                                                                                                                        |
| `qemu.image`                               | String       | `tonistiigi/binfmt:latest`              | Sets the QEMU emulation image. See [QEMU](#qemu).                                                                                                                                                             |

## [Scaling BuildKit](#scaling-buildkit)

One of the main advantages of the Kubernetes driver is that you can scale the number of builder replicas up and down to handle increased build load. Scaling is configurable using the following driver options:

* `replicas=N`

  This scales the number of BuildKit pods to the desired size. By default, it only creates a single pod. Increasing the number of replicas lets you take advantage of multiple nodes in your cluster.

* `requests.cpu`, `requests.memory`, `requests.ephemeral-storage`, `limits.cpu`, `limits.memory`, `limits.ephemeral-storage`

  These options allow requesting and limiting the resources available to each BuildKit pod [according to the official Kubernetes documentation](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

For example, to create 4 replica BuildKit pods:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4
```

Listing the pods, you get this:

```console
$ kubectl -n buildkit get deployments
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
kube0   4/4     4            4           8s

$ kubectl -n buildkit get pods
NAME                     READY   STATUS    RESTARTS   AGE
kube0-6977cdcb75-48ld2   1/1     Running   0          8s
kube0-6977cdcb75-rkc6b   1/1     Running   0          8s
kube0-6977cdcb75-vb4ks   1/1     Running   0          8s
kube0-6977cdcb75-z4fzs   1/1     Running   0          8s
```

Additionally, you can use the `loadbalance=(sticky|random)` option to control the load-balancing behavior when there are multiple replicas. `random` selects random nodes from the node pool, providing an even workload distribution across replicas. `sticky` (the default) attempts to connect the same build performed multiple times to the same node each time, ensuring better use of local cache.

For more information on scalability, see the options for [`docker buildx create`](/reference/cli/docker/buildx/create/#driver-opt).

## [Persistent storage](#persistent-storage)

Set the `persistent-volume-claim.requests.storage` driver option to store the BuildKit build cache in a persistent volume claim instead of the pod filesystem. When you set this option, Buildx creates a `StatefulSet` instead of a `Deployment`.

If you also set `replicas`, each replica gets its own persistent volume claim. This keeps the build cache local to each pod across restarts.

For example, to create a builder with 20 GiB of persistent storage per replica:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,replicas=4,persistent-volume-claim.requests.storage=20Gi
```

## [Node assignment](#node-assignment)

The Kubernetes driver allows you to control the scheduling of BuildKit pods using the `nodeSelector` and `tolerations` driver options. You can also set the `schedulername` option if you want to use a custom scheduler altogether.

You can use the `annotations` and `labels` driver options to apply additional metadata to the `Deployment` or `StatefulSet` and the pods hosting your builders.

The value of the `nodeSelector` parameter is a comma-separated string of key-value pairs, where the key is the node label and the value is the label text. For example: `"nodeselector=kubernetes.io/arch=arm64"`

The `tolerations` parameter is a semicolon-separated list of taints. It accepts the same values as the Kubernetes manifest. Each `tolerations` entry specifies a taint key and the value, operator, or effect. For example: `"tolerations=key=foo,value=bar;key=foo2,operator=exists;key=foo3,effect=NoSchedule"`

These options accept CSV-delimited strings as values. Due to quoting rules for shell commands, you must wrap the values in single quotes. You can even wrap all of `--driver-opt` in single quotes, for example:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  '--driver-opt="nodeselector=label1=value1,label2=value2","tolerations=key=key1,value=value1"'
```

## [Multi-platform builds](#multi-platform-builds)

The Kubernetes driver has support for creating [multi-platform images](https://docs.docker.com/build/building/multi-platform/), either using QEMU or by leveraging the native architecture of nodes.

### [QEMU](#qemu)

Like the `docker-container` driver, the Kubernetes driver also supports using [QEMU](https://www.qemu.org/) (user mode) to build images for non-native platforms. Include the `--platform` flag and specify which platforms you want to output to.

For example, to build a Linux image for `amd64` and `arm64`:

```console
$ docker buildx build \
  --builder=kube \
  --platform=linux/amd64,linux/arm64 \
  -t <user>/<image> \
  --push .
```

> Warning
>
> QEMU performs full-CPU emulation of non-native platforms, which is much slower than native builds. Compute-heavy tasks like compilation and compression/decompression will likely take a large performance hit.

Using a custom BuildKit image or invoking non-native binaries in builds may require that you explicitly turn on QEMU using the `qemu.install` option when creating the builder:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,qemu.install=true
```

### [Native](#native)

If you have access to cluster nodes of different architectures, the Kubernetes driver can take advantage of these for native builds. To do this, use the `--append` flag of `docker buildx create`.

First, create your builder with explicit support for a single architecture, for example `amd64`:

```console
$ docker buildx create \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/amd64 \
  --node=builder-amd64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=amd64"
```

This creates a Buildx builder named `kube`, containing a single builder node named `builder-amd64`. Assigning a node name using `--node` is optional. Buildx generates a random node name if you don't provide one.

Note that the Buildx concept of a node isn't the same as the Kubernetes concept of a node. A Buildx node in this case could connect multiple Kubernetes nodes of the same architecture together.

With the `kube` builder created, you can now introduce another architecture into the mix using `--append`. For example, to add `arm64`:

```console
$ docker buildx create \
  --append \
  --bootstrap \
  --name=kube \
  --driver=kubernetes \
  --platform=linux/arm64 \
  --node=builder-arm64 \
  --driver-opt=namespace=buildkit,nodeselector="kubernetes.io/arch=arm64"
```

Listing your builders shows both nodes for the `kube` builder:

```console
$ docker buildx ls
NAME/NODE       DRIVER/ENDPOINT                                         STATUS   PLATFORMS
kube            kubernetes
  builder-amd64 kubernetes:///kube?deployment=builder-amd64&kubeconfig= running  linux/amd64*, linux/amd64/v2, linux/amd64/v3, linux/386
  builder-arm64 kubernetes:///kube?deployment=builder-arm64&kubeconfig= running  linux/arm64*
```

You can now build multi-arch `amd64` and `arm64` images, by specifying those platforms together in your build command:

```console
$ docker buildx build --builder=kube --platform=linux/amd64,linux/arm64 -t <user>/<image> --push .
```

You can repeat the `buildx create --append` command for as many architectures that you want to support.

## [Rootless mode](#rootless-mode)

The Kubernetes driver supports rootless mode. For more information on how rootless mode works, and its requirements, refer to the [Rootless Buildkit documentation](https://github.com/moby/buildkit/blob/master/docs/rootless.md).

To turn it on in your cluster, you can use the `rootless=true` driver option:

```console
$ docker buildx create \
  --name=kube \
  --driver=kubernetes \
  --driver-opt=namespace=buildkit,rootless=true
```

This will create your pods without `securityContext.privileged`.

Requires Kubernetes version 1.19 or later. Using Ubuntu as the host kernel is recommended.

## [Example: Creating a Buildx builder in Kubernetes](#example-creating-a-buildx-builder-in-kubernetes)

This guide shows you how to:

* Create a namespace for your Buildx resources
* Create a Kubernetes builder.
* List the available builders
* Build an image using your Kubernetes builders

Prerequisites:

* You have an existing Kubernetes cluster. If you don't already have one, you can follow along by installing [minikube](https://minikube.sigs.k8s.io/docs/).
* The cluster you want to connect to is accessible via the `kubectl` command, with the `KUBECONFIG` environment variable [set appropriately](https://kubernetes.io/docs/tasks/access-application-cluster/configure-access-multiple-clusters/#set-the-kubeconfig-environment-variable) if necessary.

1. Create a `buildkit` namespace.

   Creating a separate namespace helps keep your Buildx resources separate from other resources in the cluster.

   ```console
   $ kubectl create namespace buildkit
   namespace/buildkit created
   ```

2. Create a new builder with the Kubernetes driver:

   ```console
   $ docker buildx create \
     --bootstrap \
     --name=kube \
     --driver=kubernetes \
     --driver-opt=namespace=buildkit
   ```

   > Note
   >
   > Remember to specify the namespace in driver options.

3. List available builders using `docker buildx ls`

   ```console
   $ docker buildx ls
   NAME/NODE                DRIVER/ENDPOINT STATUS  PLATFORMS
   kube                     kubernetes
     kube0-6977cdcb75-k9h9m                 running linux/amd64, linux/amd64/v2, linux/amd64/v3, linux/386
   default *                docker
     default                default         running linux/amd64, linux/386
   ```

4. Inspect the running pods created by the build driver with `kubectl`.

   ```console
   $ kubectl -n buildkit get deployments
   NAME    READY   UP-TO-DATE   AVAILABLE   AGE
   kube0   1/1     1            1           32s

   $ kubectl -n buildkit get pods
   NAME                     READY   STATUS    RESTARTS   AGE
   kube0-6977cdcb75-k9h9m   1/1     Running   0          32s
   ```

   The build driver creates the necessary resources on your cluster in the specified namespace (in this case, `buildkit`), while keeping your driver configuration locally.

5. Use your new builder by including the `--builder` flag when running buildx commands. For example: :

   ```console
   # Replace <registry> with your Docker username
   # and <image> with the name of the image you want to build
   docker buildx build \
     --builder=kube \
     -t <registry>/<image> \
     --push .
   ```

That's it: you've now built an image from a Kubernetes pod, using Buildx.

## [Further reading](#further-reading)

For more information on the Kubernetes driver, see the [buildx reference](/reference/cli/docker/buildx/create/#driver).

----
url: https://docs.docker.com/build/policies/testing/
----

# Test build policies

***

Table of contents

***

The [`docker buildx policy test`](/reference/cli/docker/buildx/policy/test/) command runs unit tests for build policies using OPA's [standard test framework](https://www.openpolicyagent.org/docs/policy-testing).

```console
$ docker buildx policy test <path>
```

This validates policy logic with mocked inputs.

For testing against real sources (actual image metadata, Git repositories), use [`docker buildx policy eval`](/reference/cli/docker/buildx/policy/eval/) instead. You can use the `eval --print` option to resolve input for a specific source for writing a test case.

## [Basic example](#basic-example)

Start with a simple policy that only allows `alpine` images:

Dockerfile.rego

```rego
package docker

default allow = false

allow if {
    input.image.repo == "alpine"
}

decision := {"allow": allow}
```

Create a test file with the `*_test.rego` suffix. Test functions must start with `test_`:

Dockerfile\_test.rego

```rego
package docker

test_alpine_allowed if {
    decision.allow with input as {"image": {"repo": "alpine"}}
}

test_ubuntu_denied if {
    not decision.allow with input as {"image": {"repo": "ubuntu"}}
}
```

Run the tests:

```console
$ docker buildx policy test .
test_alpine_allowed: PASS (allow=true)
test_ubuntu_denied: PASS (allow=false)
```

`PASS` indicates that the tests defined in `Dockerfile_test.rego` executed successfully and all assertions were satisfied.

## [Command options](#command-options)

Filter tests by name with `--run`:

```console
$ docker buildx policy test --run alpine .
test_alpine_allowed: PASS (allow=true)
```

Test policies with non-default filenames using `--filename`:

```console
$ docker buildx policy test --filename app.Dockerfile .
```

This loads `app.Dockerfile.rego` and runs `*_test.rego` files against it.

## [Test output](#test-output)

Passed tests show the allow status and any deny messages:

```console
test_alpine_allowed: PASS (allow=true)
test_ubuntu_denied: PASS (allow=false, deny_msg=only alpine images are allowed)
```

Failed tests show input, decision output, and missing fields:

```console
test_invalid: FAIL (allow=false)
input:
  {
    "image": {}
  }
decision:
  {
    "allow": false,
    "deny_msg": [
      "only alpine images are allowed"
    ]
  }
missing_input: input.image.repo
```

## [Test deny messages](#test-deny-messages)

To test custom error messages, capture the full decision result and assert on the `deny_msg` field.

For a policy with deny messages:

Dockerfile.rego

```rego
package docker

default allow = false

allow if {
    input.image.repo == "alpine"
}

deny_msg contains msg if {
    not allow
    msg := "only alpine images are allowed"
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

Test the deny message:

Dockerfile\_test.rego

```rego
test_deny_message if {
    result := decision with input as {"image": {"repo": "ubuntu"}}
    not result.allow
    "only alpine images are allowed" in result.deny_msg
}
```

## [Test patterns](#test-patterns)

**Test environment-specific rules:**

```rego
test_production_requires_digest if {
    decision.allow with input as {
        "env": {"target": "production"},
        "image": {"isCanonical": true}
    }
}

test_development_allows_tags if {
    decision.allow with input as {
        "env": {"target": "development"},
        "image": {"isCanonical": false}
    }
}
```

**Test multiple registries:**

```rego
test_dockerhub_allowed if {
    decision.allow with input as {
        "image": {
            "ref": "docker.io/library/alpine",
            "host": "docker.io",
            "repo": "alpine"
        }
    }
}

test_ghcr_allowed if {
    decision.allow with input as {
        "image": {
            "ref": "ghcr.io/myorg/myapp",
            "host": "ghcr.io",
            "repo": "myorg/myapp"
        }
    }
}
```

For available input fields, see the [Input reference](https://docs.docker.com/build/policies/inputs/).

## [Organize test files](#organize-test-files)

The test runner discovers all `*_test.rego` files recursively:

```plaintext
build-policies/
├── Dockerfile.rego
├── Dockerfile_test.rego
└── tests/
    ├── registries_test.rego
    ├── signatures_test.rego
    └── environments_test.rego
```

Run all tests:

```console
$ docker buildx policy test .
```

Or test specific files:

```console
$ docker buildx policy test tests/registries_test.rego
```

----
url: https://docs.docker.com/build/metadata/attestations/attestation-storage/
----

# Image attestation storage

***

Table of contents

***

Buildkit supports creating and attaching attestations to build artifacts. These attestations can provide valuable information from the build process, including, but not limited to: [SBOMs](https://en.wikipedia.org/wiki/Software_supply_chain), [SLSA Provenance](https://slsa.dev/provenance), build logs, etc.

This document describes the current custom format used to store attestations, which is designed to be compatible with current registry implementations today. In the future, we may support exporting attestations in additional formats.

Attestations are stored as manifest objects in the image index, similar in style to OCI artifacts.

## [Properties](#properties)

### [Attestation Manifest](#attestation-manifest)

Attestation manifests are attached to the root image index object, under a separate [OCI image manifest](https://github.com/opencontainers/image-spec/blob/main/manifest.md). Each attestation manifest can contain multiple [attestation blobs](#attestation-blob), with all the of the attestations in a manifest applying to a single platform manifest. All properties of standard OCI and Docker manifests continue to apply.

The image `config` descriptor will point to a valid [image config](https://github.com/opencontainers/image-spec/blob/main/config.md), however, it will not contain attestation-specific details, and should be ignored as it is only included for compatibility purposes.

Each image layer in `layers` will contain a descriptor for a single [attestation blob](#attestation-blob). The `mediaType` of each layer will be set in accordance to its contents, one of:

* `application/vnd.in-toto+json` (currently, the only supported option)

  Indicates an in-toto attestation blob

Any unknown `mediaType`s should be ignored.

To assist attestation traversal, the following annotations may be set on each layer descriptor:

* `in-toto.io/predicate-type`

  This annotation will be set if the enclosed attestation is an in-toto attestation (currently, the only supported option). The annotation will be set to contain the same value as the `predicateType` property present inside the attestation.

  When present, this annotation may be used to find the specific attestation(s) they are looking for to avoid pulling the contents of the others.

### [Attestation Blob](#attestation-blob)

The contents of each layer will be a blob dependent on its `mediaType`.

* `application/vnd.in-toto+json`

  The blob contents will contain a full [in-toto attestation statement](https://github.com/in-toto/attestation/blob/main/spec/README.md#statement):

  ```json
  {
    "_type": "https://in-toto.io/Statement/v1",
    "subject": [
      {
        "name": "NAME",
        "digest": {"ALGORITHM": "HEX_VALUE"}
      },
      ...
    ],
    "predicateType": "URI",
    "predicate": { ... }
  }
  ```

  The subject of the attestation should be set to be the same digest as the target manifest described in the [Attestation Manifest Descriptor](#attestation-manifest-descriptor), or some object within.

### [Attestation Manifest Descriptor](#attestation-manifest-descriptor)

Attestation manifests are attached to the root [image index](https://github.com/opencontainers/image-spec/blob/main/image-index.md), in the `manifests` key, after all the original runnable manifests. All properties of standard OCI and Docker manifest descriptors continue to apply.

To prevent container runtimes from accidentally pulling or running the image described in the manifest, the `platform` property of the attestation manifest will be set to `unknown/unknown`, as follows:

```json
"platform": {
  "architecture": "unknown",
  "os": "unknown"
}
```

To assist index traversal, the following annotations will be set on the manifest descriptor descriptor:

* `vnd.docker.reference.type`

  This annotation describes the type of the artifact, and will be set to `attestation-manifest`. If any other value is specified, the entire manifest should be ignored.

* `vnd.docker.reference.digest`

  This annotation will contain the digest of the object in the image index that the attestation manifest refers to.

  When present, this annotation can be used to find the matching attestation manifest for a selected image manifest.

## [Examples](#examples)

*Example showing an SBOM attestation attached to a `linux/amd64` image*

#### [Image index (`sha256:94acc2ca70c40f3f6291681f37ce9c767e3d251ce01c7e4e9b98ccf148c26260`):](#image-index-sha25694acc2ca70c40f3f6291681f37ce9c767e3d251ce01c7e4e9b98ccf148c26260)

This image index defines two descriptors: an AMD64 image `sha256:23678f31..` and an attestation manifest `sha256:02cb9aa7..` for that image.

```json
{
  "mediaType": "application/vnd.oci.image.index.v1+json",
  "schemaVersion": 2,
  "manifests": [
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:23678f31b3b3586c4fb318aecfe64a96a1f0916ba8faf9b2be2abee63fa9e827",
      "size": 1234,
      "platform": {
        "architecture": "amd64",
        "os": "linux"
      }
    },
    {
      "mediaType": "application/vnd.oci.image.manifest.v1+json",
      "digest": "sha256:02cb9aa7600e73fcf41ee9f0f19cc03122b2d8be43d41ce4b21335118f5dd943",
      "size": 1234,
      "annotations": {
        "vnd.docker.reference.digest": "sha256:23678f31b3b3586c4fb318aecfe64a96a1f0916ba8faf9b2be2abee63fa9e827",
        "vnd.docker.reference.type": "attestation-manifest"
      },
      "platform": {
         "architecture": "unknown",
         "os": "unknown"
      }
    }
  ]
}
```

#### [Attestation manifest (`sha256:02cb9aa7600e73fcf41ee9f0f19cc03122b2d8be43d41ce4b21335118f5dd943`):](#attestation-manifest-sha25602cb9aa7600e73fcf41ee9f0f19cc03122b2d8be43d41ce4b21335118f5dd943)

This attestation manifest contains one attestation that is an in-toto attestation that contains a "https\://spdx.dev/Document" predicate, signifying that it is defining a SBOM for the image.

```json
{
  "mediaType": "application/vnd.oci.image.manifest.v1+json",
  "schemaVersion": 2,
  "config": {
    "mediaType": "application/vnd.oci.image.config.v1+json",
    "digest": "sha256:a781560066f20ec9c28f2115a95a886e5e71c7c7aa9d8fd680678498b82f3ea3",
    "size": 123
  },
  "layers": [
    {
      "mediaType": "application/vnd.in-toto+json",
      "digest": "sha256:133ae3f9bcc385295b66c2d83b28c25a9f294ce20954d5cf922dda860429734a",
      "size": 1234,
      "annotations": {
        "in-toto.io/predicate-type": "https://spdx.dev/Document"
      }
    }
  ]
}
```

#### [Image config (`sha256:a781560066f20ec9c28f2115a95a886e5e71c7c7aa9d8fd680678498b82f3ea3`):](#image-config-sha256a781560066f20ec9c28f2115a95a886e5e71c7c7aa9d8fd680678498b82f3ea3)

```json
{
  "architecture": "unknown",
  "os": "unknown",
  "config": {},
  "rootfs": {
    "type": "layers",
    "diff_ids": [
      "sha256:133ae3f9bcc385295b66c2d83b28c25a9f294ce20954d5cf922dda860429734a"
    ]
  }
}
```

#### [Layer content (`sha256:1ea07d5e55eb47ad0e6bbfa2ec180fb580974411e623814e519064c88f022f5c`):](#layer-content-sha2561ea07d5e55eb47ad0e6bbfa2ec180fb580974411e623814e519064c88f022f5c)

Attestation body containing the SBOM data listing the packages used during the build in SPDX format.

```json
{
  "_type": "https://in-toto.io/Statement/v1",
  "predicateType": "https://spdx.dev/Document",
  "subject": [
    {
      "name": "_",
      "digest": {
        "sha256": "23678f31b3b3586c4fb318aecfe64a96a1f0916ba8faf9b2be2abee63fa9e827"
      }
    }
  ],
  "predicate": {
    "SPDXID": "SPDXRef-DOCUMENT",
    "spdxVersion": "SPDX-2.2",
    ...
```

----
url: https://docs.docker.com/admin/company/manage/owners/
----

# Manage company owners

***

Table of contents

***

Subscription: Business

For: Administrators

A company can have multiple owners. Company owners have visibility across the entire company and can manage settings that apply to all organizations under that company. They also have the same access rights as organization owners but don’t need to be members of any individual organization.

> Important
>
> Company owners do not occupy a seat unless they are added as a member of an organization under your company, or SSO is enabled and the company owner signs in via SSO (which automatically adds them as an organization member).

## [Add a company owner](#add-a-company-owner)

1. Sign in to [Docker Home](https://app.docker.com) and select your company from the top-left account drop-down.
2. Select **Admin Console**, then **Company owners**.
3. Select **Add owner**.
4. Specify the user's Docker ID to search for the user.
5. After you find the user, select **Add company owner**.

## [Remove a company owner](#remove-a-company-owner)

1. Sign in to [Docker Home](https://app.docker.com) and select your company from the top-left account drop-down.
2. Select **Admin Console**, then **Company owners**.
3. Locate the company owner you want to remove and select the **Actions** menu.
4. Select **Remove as company owner**.

----
url: https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/
----

# Interface: RawExecResult

***

Table of contents

***

**`Since`**

0.2.0

## [Hierarchy](#hierarchy)

* **`RawExecResult`**

  ↳ [`ExecResult`](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)

## [Properties](#properties)

### [cmd](#cmd)

• `Optional` `Readonly` **cmd**: `string`

***

### [killed](#killed)

• `Optional` `Readonly` **killed**: `boolean`

***

### [signal](#signal)

• `Optional` `Readonly` **signal**: `string`

***

### [code](#code)

• `Optional` `Readonly` **code**: `number`

***

### [stdout](#stdout)

• `Readonly` **stdout**: `string`

***

### [stderr](#stderr)

• `Readonly` **stderr**: `string`

----
url: https://docs.docker.com/enterprise/enterprise-deployment/pkg-install-and-configure/
----

# PKG installer

***

Table of contents

***

Subscription: Business

For: Administrators

The PKG package supports various MDM (Mobile Device Management) solutions, making it ideal for bulk installations and eliminating the need for manual setups by individual users. With this package, IT administrators can ensure standardized, policy-driven installations of Docker Desktop, enhancing efficiency and software management across their organizations.

## [Install interactively](#install-interactively)

1. In [Docker Home](http://app.docker.com), choose your organization.

2. Select **Admin Console**, then **Enterprise deployment**.

3. From the **macOS** tab, select the **Download PKG installer** button.

4. Once downloaded, double-click `Docker.pkg` to run the installer.

5. Follow the instructions on the installation wizard to authorize the installer and proceed with the installation.

   * **Introduction**: Select **Continue**.
   * **License**: Review the license agreement and select **Agree**.
   * **Destination Select**: This step is optional. It is recommended that you keep the default installation destination (usually `Macintosh HD`). Select **Continue**.
   * **Installation Type**: Select **Install**.
   * **Installation**: Authenticate using your administrator password or Touch ID.
   * **Summary**: When the installation completes, select **Close**.

> Note
>
> When installing Docker Desktop with the PKG, in-app updates are automatically disabled. This ensures organizations can maintain version consistency and prevent unapproved updates. For Docker Desktop installed with the `.dmg` installer, in-app updates remain supported.
>
> Docker Desktop notifies you when an update is available. To update Docker Desktop, download the latest installer from the Docker Admin Console. Navigate to the **Enterprise deployment** page.
>
> To keep up to date with new releases, check the [release notes](https://docs.docker.com/desktop/release-notes/) page.

## [Install from the command line](#install-from-the-command-line)

1. In [Docker Home](http://app.docker.com), choose your organization.

2. Select **Admin Console**, then **Enterprise deployment**.

3. From the **macOS** tab, select the **Download PKG installer** button.

4. From your terminal, run the following command:

   ```console
   $ sudo installer -pkg "/path/to/Docker.pkg" -target /Applications
   ```

## [Additional resources](#additional-resources)

* See how you can deploy Docker Desktop for Mac using [Intune](https://docs.docker.com/enterprise/enterprise-deployment/use-intune/) or [Jamf Pro](https://docs.docker.com/enterprise/enterprise-deployment/use-jamf-pro/)
* Explore how to [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/methods/#plist-method-mac-only) for your users.

----
url: https://docs.docker.com/guides/testcontainers-python-getting-started/run-tests/
----

# Run tests and next steps

***

Table of contents

***

## [Run the tests](#run-the-tests)

Run the tests using pytest:

```console
$ pytest -v
```

You should see output similar to:

```text
============================= test session starts ==============================
platform linux -- Python 3.13.x, pytest-9.x.x
collected 2 items

tests/test_customers.py::test_get_all_customers PASSED                   [ 50%]
tests/test_customers.py::test_get_customer_by_email PASSED               [100%]

============================== 2 passed in 1.90s ===============================
```

The tests run against a real PostgreSQL database instead of mocks, which gives more confidence in the implementation.

## [Summary](#summary)

The Testcontainers for Python library helps you write integration tests using the same type of database (Postgres) that you use in production, instead of mocks. Because you aren't using mocks and instead talk to real services, you're free to refactor code and still verify that the application works as expected.

In addition to PostgreSQL, Testcontainers for Python provides modules for many SQL databases, NoSQL databases, messaging queues, and more. You can use Testcontainers to run any containerized dependency for your tests.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [testcontainers-python documentation](https://testcontainers-python.readthedocs.io/)
* [Getting started with Testcontainers for Go](/guides/testcontainers-go-getting-started/)
* [Getting started with Testcontainers for Java](https://testcontainers.com/guides/getting-started-with-testcontainers-for-java/)
* [Getting started with Testcontainers for Node.js](https://testcontainers.com/guides/getting-started-with-testcontainers-for-nodejs/)

----
url: https://docs.docker.com/dhi/explore/available/
----

# Available types of Docker Hardened Images

***

Table of contents

***

Docker Hardened Images (DHI) is a comprehensive catalog of security-hardened container images built to meet diverse development and production needs.

You can explore the DHI catalog on [Docker Hub](https://hub.docker.com/hardened-images/catalog) or use the [DHI CLI](https://docs.docker.com/dhi/how-to/cli/) to browse available images, tags, and metadata from the command line.

## [Framework and application images](#framework-and-application-images)

DHI includes a selection of popular frameworks and application images, each hardened and maintained to ensure security and compliance. These images integrate seamlessly into existing workflows, allowing developers to focus on building applications without compromising on security.

For example, you might find repositories like the following in the DHI catalog:

* `node`: framework for Node.js applications
* `python`: framework for Python applications
* `nginx`: web server image

## [Base image distributions](#base-image-distributions)

Docker Hardened Images are available in different base image options, giving you flexibility to choose the best match for your environment and workload requirements:

* Debian-based images: A good fit if you're already working in glibc-based environments. Debian is widely used and offers strong compatibility across many language ecosystems and enterprise systems.

* Alpine-based images: A smaller and more lightweight option using musl libc. These images tend to be small and are therefore faster to pull and have a reduced footprint.

Each image maintains a minimal and secure runtime layer by removing non-essential components like shells, package managers, and debugging tools. This helps reduce the attack surface while retaining compatibility with common runtime environments. To maintain this lean, secure foundation, DHI standardizes on Debian for glibc-based images, which provides broad compatibility while minimizing complexity and maintenance overhead.

Example tags include:

* `3.9.23-alpine3.21`: Alpine-based image for Python 3.9.23
* `3.9.23-debian12`: Debian-based image for Python 3.9.23

If you're not sure which to choose, start with the base you're already familiar with. Debian tends to offer the broadest compatibility.

## [Development and runtime variants](#development-and-runtime-variants)

To accommodate different stages of the application lifecycle, DHI offers all language framework images and select application images in two variants:

* Development (dev) images: Equipped with necessary development tools and libraries, these images facilitate the building and testing of applications in a secure environment. They include a shell, package manager, a root user, and other tools needed for development.

* Runtime images: Stripped of development tools, these images contain only the essential components needed to run applications, ensuring a minimal attack surface in production.

This separation supports multi-stage builds, enabling developers to compile code in a secure build environment and deploy it using a lean runtime image.

For example, you might find tags like the following in a DHI repository:

* `3.9.23-debian12`: runtime image for Python 3.9.23
* `3.9.23-debian12-dev`: development image for Python 3.9.23

## [FIPs and STIG variants](#fips-and-stig-variants)

Subscription: Docker Hardened Images Select or Enterprise

Some Docker Hardened Images include a `-fips` variant. These variants use cryptographic modules that have been validated under [FIPS 140](https://docs.docker.com/dhi/core-concepts/fips/), a U.S. government standard for secure cryptographic operations.

FIPS variants are designed to help organizations meet regulatory and compliance requirements related to cryptographic use in sensitive or regulated environments.

You can recognize FIPS variants by their tag that includes `-fips`.

For example:

* `3.13-fips`: FIPS variant of the Python 3.13 image
* `3.9.23-debian12-fips`: FIPS variant of the Debian-based Python 3.9.23 image

FIPS variants can be used in the same way as any other Docker Hardened Image and are ideal for teams operating in regulated industries or under compliance frameworks that require cryptographic validation.

In addition to FIPS variants, some Docker Hardened Images also include STIG-ready variants. These images are scanned against custom STIG-based profiles and come with signed STIG scan attestations to support audits and compliance reporting. To identify STIG-ready variants, look for the **STIG** in the **Compliance** column of the image tags list in the Docker Hub catalog.

## [Compatibility variants](#compatibility-variants)

Some Docker Hardened Images include a compatibility variant. These variants provide additional tools and configurations for specific use cases without bloating the minimal base images.

Compatibility variants are created to support:

* Helm chart compatibility: Applications deployed via Helm charts and Kubernetes that require specific runtime configurations or utilities for seamless integration with popular Helm charts.

* Special application use-cases: Applications that need optional tools not included in the minimal image.

By offering these as separate image flavors, DHI ensures that the minimal images remain lean and secure, while providing the tools you need in dedicated variants. This approach maintains a minimal attack surface for standard deployments while supporting specialized requirements when needed.

You can recognize compatibility variants by their tag that includes `-compat`.

Use compatibility variants when your deployment requires additional tools beyond the minimal runtime, such as when using Helm charts or applications with specific tooling requirements.

## [Socket Firewall variants](#socket-firewall-variants)

Some Docker Hardened Images include Socket Firewall variants. These are `dev` variants that come with [Socket](https://socket.dev/) preinstalled to monitor package manager activity and block malicious packages during development and CI builds.

Two tiers are available, identified by their tag suffix:

* `-sfw-dev`: Socket Firewall Free. No API key required.
* `-sfw-ent-dev`: Socket Firewall Enterprise. Requires an API key from Socket.

Not all images offer both tiers.

## [Image-specific variants](#image-specific-variants)

Some images include variants that go beyond the general `dev`, `compat`, and `sfw` patterns. These represent distinct editions, bundled tooling, or runtime configurations specific to that image. Examples include a PHP-FPM variant for web server integration, a native binary build for faster startup, or a specific edition of a database.

You can identify these variants by their tag suffix. The image name in the tag suffix typically reflects what's included or different.

----
url: https://docs.docker.com/guides/testcontainers-nodejs-getting-started/create-project/
----

# Create the Node.js project

***

Table of contents

***

## [Initialize the project](#initialize-the-project)

Create a new Node.js project:

```console
$ npm init -y
```

Add `pg`, `jest`, and `@testcontainers/postgresql` as dependencies:

```console
$ npm install pg --save
$ npm install jest @testcontainers/postgresql --save-dev
```

## [Implement the customer repository](#implement-the-customer-repository)

Create `src/customer-repository.js` with functions to manage customers in PostgreSQL:

```javascript
async function createCustomerTable(client) {
  const sql =
    "CREATE TABLE IF NOT EXISTS customers (id INT NOT NULL, name VARCHAR NOT NULL, PRIMARY KEY (id))";
  await client.query(sql);
}

async function createCustomer(client, customer) {
  const sql = "INSERT INTO customers (id, name) VALUES($1, $2)";
  await client.query(sql, [customer.id, customer.name]);
}

async function getCustomers(client) {
  const sql = "SELECT * FROM customers";
  const result = await client.query(sql);
  return result.rows;
}

module.exports = { createCustomerTable, createCustomer, getCustomers };
```

The module provides three functions:

* `createCustomerTable()` creates the `customers` table if it doesn't exist.
* `createCustomer()` inserts a customer record.
* `getCustomers()` fetches all customer records.

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-nodejs-getting-started/write-tests/)

----
url: https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/create-project/
----

# Create the Spring Boot project

***

Table of contents

***

## [Set up the project](#set-up-the-project)

Create a Spring Boot project from [Spring Initializr](https://start.spring.io) by selecting the **Spring Web**, **Validation**, **JDBC API**, **PostgreSQL Driver**, **Spring Security**, **OAuth2 Resource Server**, and **Testcontainers** starters.

Alternatively, clone the [guide repository](https://github.com/testcontainers/tc-guide-securing-spring-boot-microservice-using-keycloak-and-testcontainers).

After generating the application, add the [testcontainers-keycloak](https://github.com/dasniko/testcontainers-keycloak) community module and [REST Assured](https://rest-assured.io/) as test dependencies.

The key dependencies in `pom.xml` are:

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
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <dependency>
        <groupId>org.postgresql</groupId>
        <artifactId>postgresql</artifactId>
        <scope>runtime</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-security</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.security</groupId>
        <artifactId>spring-security-test</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-testcontainers</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-junit-jupiter</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>org.testcontainers</groupId>
        <artifactId>testcontainers-postgresql</artifactId>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>com.github.dasniko</groupId>
        <artifactId>testcontainers-keycloak</artifactId>
        <version>3.4.0</version>
        <scope>test</scope>
    </dependency>
    <dependency>
        <groupId>io.rest-assured</groupId>
        <artifactId>rest-assured</artifactId>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## [Create the domain model](#create-the-domain-model)

Create a `Product` record that represents the domain object:

```java
package com.testcontainers.products.domain;

import jakarta.validation.constraints.NotEmpty;

public record Product(Long id, @NotEmpty String title, String description) {}
```

## [Create the repository](#create-the-repository)

Implement `ProductRepository` using Spring `JdbcClient` to interact with a PostgreSQL database:

```java
package com.testcontainers.products.domain;

import java.util.List;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.jdbc.support.GeneratedKeyHolder;
import org.springframework.jdbc.support.KeyHolder;
import org.springframework.stereotype.Repository;

@Repository
public class ProductRepository {

  private final JdbcClient jdbcClient;

  public ProductRepository(JdbcClient jdbcClient) {
    this.jdbcClient = jdbcClient;
  }

  public List<Product> getAll() {
    return jdbcClient.sql("SELECT * FROM products").query(Product.class).list();
  }

  public Product create(Product product) {
    String sql =
      "INSERT INTO products(title, description) VALUES (:title,:description) RETURNING id";
    KeyHolder keyHolder = new GeneratedKeyHolder();
    jdbcClient
      .sql(sql)
      .param("title", product.title())
      .param("description", product.description())
      .update(keyHolder);
    Long id = keyHolder.getKeyAs(Long.class);
    return new Product(id, product.title(), product.description());
  }
}
```

## [Add a schema creation script](#add-a-schema-creation-script)

Create `src/main/resources/schema.sql` to initialize the `products` table:

```sql
CREATE TABLE products (
    id bigserial primary key,
    title varchar not null,
    description text
);
```

Enable schema initialization in `src/main/resources/application.properties`:

```properties
spring.sql.init.mode=always
```

For production applications, use a database migration tool like Flyway or Liquibase instead.

## [Implement the API endpoints](#implement-the-api-endpoints)

Create `ProductController` with endpoints to fetch all products and create a product:

```java
package com.testcontainers.products.api;

import com.testcontainers.products.domain.Product;
import com.testcontainers.products.domain.ProductRepository;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/products")
class ProductController {

  private final ProductRepository productRepository;

  ProductController(ProductRepository productRepository) {
    this.productRepository = productRepository;
  }

  @GetMapping
  List<Product> getAll() {
    return productRepository.getAll();
  }

  @PostMapping
  @ResponseStatus(HttpStatus.CREATED)
  Product createProduct(@RequestBody @Valid Product product) {
    return productRepository.create(product);
  }
}
```

## [Configure OAuth 2.0 security](#configure-oauth-20-security)

Create a `SecurityConfig` class that protects the API endpoints using JWT token-based authentication:

```java
package com.testcontainers.products.config;

import static org.springframework.security.config.Customizer.withDefaults;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpMethod;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configurers.CorsConfigurer;
import org.springframework.security.config.annotation.web.configurers.CsrfConfigurer;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@EnableWebSecurity
class SecurityConfig {

  @Bean
  SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    http
      .authorizeHttpRequests(c ->
        c
          .requestMatchers(HttpMethod.GET, "/api/products")
          .permitAll()
          .requestMatchers(HttpMethod.POST, "/api/products")
          .authenticated()
          .anyRequest()
          .authenticated()
      )
      .sessionManagement(c ->
        c.sessionCreationPolicy(SessionCreationPolicy.STATELESS)
      )
      .cors(CorsConfigurer::disable)
      .csrf(CsrfConfigurer::disable)
      .oauth2ResourceServer(oauth2 -> oauth2.jwt(withDefaults()));
    return http.build();
  }
}
```

This configuration:

* Permits unauthenticated access to `GET /api/products`.
* Requires authentication for `POST /api/products` and all other endpoints.
* Configures the OAuth 2.0 Resource Server with JWT token-based authentication.
* Disables CORS and CSRF because this is a stateless API.

Add the JWT issuer URI to `application.properties`:

```properties
spring.security.oauth2.resourceserver.jwt.issuer-uri=http://localhost:9090/realms/keycloaktcdemo
```

## [Export the Keycloak realm configuration](#export-the-keycloak-realm-configuration)

Before writing the tests, export a Keycloak realm configuration so that the test environment can import it automatically. Start a temporary Keycloak instance:

```console
$ docker run -p 9090:8080 \
    -e KEYCLOAK_ADMIN=admin \
    -e KEYCLOAK_ADMIN_PASSWORD=admin \
    quay.io/keycloak/keycloak:25 start-dev
```

Open `http://localhost:9090` and sign in to the Admin Console with `admin/admin`. Then set up the realm:

1. In the top-left corner, select the realm drop-down and create a realm named `keycloaktcdemo`.

2. Under the `keycloaktcdemo` realm, create a client with the following settings:

   * **Client ID**: `product-service`
   * **Client Authentication**: `On`
   * **Authentication flow**: select only **Service accounts roles**

3. On the **Client details** screen, go to the **Credentials** tab and copy the **Client secret** value.

Export the realm configuration:

```console
$ docker ps
# copy the keycloak container id

$ docker exec -it <container-id> /bin/bash

$ /opt/keycloak/bin/kc.sh export --dir /opt/keycloak/data/import --realm keycloaktcdemo

$ exit

$ docker cp <container-id>:/opt/keycloak/data/import/keycloaktcdemo-realm.json keycloaktcdemo-realm.json
```

Copy the exported `keycloaktcdemo-realm.json` file into `src/test/resources`.

[Write tests with Testcontainers »](https://docs.docker.com/guides/testcontainers-java-keycloak-spring-boot/write-tests/)

----
url: https://docs.docker.com/engine/swarm/how-swarm-mode-works/nodes/
----

# How nodes work

***

Table of contents

***

Swarm mode lets you create a cluster of one or more Docker Engines called a swarm. A swarm consists of one or more nodes: physical or virtual machines running Docker Engine.

There are two types of nodes: [managers](#manager-nodes) and [workers](#worker-nodes).

If you haven't already, read through the [Swarm mode overview](https://docs.docker.com/engine/swarm/) and [key concepts](https://docs.docker.com/engine/swarm/key-concepts/).

## [Manager nodes](#manager-nodes)

Manager nodes handle cluster management tasks:

* Maintaining cluster state
* Scheduling services
* Serving Swarm mode [HTTP API endpoints](https://docs.docker.com/reference/api/engine/)

Using a [Raft](https://raft.github.io/raft.pdf) implementation, the managers maintain a consistent internal state of the entire swarm and all the services running on it. For testing purposes it is OK to run a swarm with a single manager. If the manager in a single-manager swarm fails, your services continue to run, but you need to create a new cluster to recover.

To take advantage of Swarm mode's fault-tolerance features, we recommend you implement an odd number of nodes according to your organization's high-availability requirements. When you have multiple managers you can recover from the failure of a manager node without downtime.

* A three-manager swarm tolerates a maximum loss of one manager.

* A five-manager swarm tolerates a maximum simultaneous loss of two manager nodes.

* An odd number `N` of manager nodes in the cluster tolerates the loss of at most `(N-1)/2` managers. Docker recommends a maximum of seven manager nodes for a swarm.

  > Important
  >
  > Adding more managers does NOT mean increased scalability or higher performance. In general, the opposite is true.

## [Worker nodes](#worker-nodes)

Worker nodes are also instances of Docker Engine whose sole purpose is to execute containers. Worker nodes don't participate in the Raft distributed state, make scheduling decisions, or serve the swarm mode HTTP API.

You can create a swarm of one manager node, but you cannot have a worker node without at least one manager node. By default, all managers are also workers. In a single manager node cluster, you can run commands like `docker service create` and the scheduler places all tasks on the local engine.

To prevent the scheduler from placing tasks on a manager node in a multi-node swarm, set the availability for the manager node to `Drain`. The scheduler gracefully stops tasks on nodes in `Drain` mode and schedules the tasks on an `Active` node. The scheduler does not assign new tasks to nodes with `Drain` availability.

Refer to the [`docker node update`](/reference/cli/docker/node/update/) command line reference to see how to change node availability.

## [Change roles](#change-roles)

You can promote a worker node to be a manager by running `docker node promote`. For example, you may want to promote a worker node when you take a manager node offline for maintenance. See [node promote](/reference/cli/docker/node/promote/).

You can also demote a manager node to a worker node. See [node demote](/reference/cli/docker/node/demote/).

## [Learn more](#learn-more)

* Read about how Swarm mode [services](https://docs.docker.com/engine/swarm/how-swarm-mode-works/services/) work.
* Learn how [PKI](https://docs.docker.com/engine/swarm/how-swarm-mode-works/pki/) works in Swarm mode.

----
url: https://docs.docker.com/guides/docker-compose/why/
----

# Why Docker Compose?

***

***

Docker Compose is an essential tool for defining and running multi-container Docker applications. Docker Compose simplifies the Docker experience, making it easier for developers to create, manage, and deploy applications by using YAML files to configure application services.

Docker Compose provides several benefits:

* Lets you define multi-container applications in a single YAML file.
* Ensures consistent environments across development, testing, and production.
* Manages the startup and linking of multiple containers effortlessly.
* Streamlines development workflows and reduces setup time.
* Ensures that each service runs in its own container, avoiding conflicts.

[Demo: set up and use Docker Compose »](https://docs.docker.com/guides/docker-compose/setup/)

----
url: https://docs.docker.com/guides/admin-user-management/
----

# Mastering user and access management

Table of contents

***

Simplify user access while ensuring security and efficiency in Docker.

**Time to complete** 20 minutes

Managing roles and permissions is key to securing your Docker environment while enabling easy collaboration and operational efficiency. This guide walks IT administrators through the essentials of user and access management, offering strategies for assigning roles, provisioning users, and using tools like activity logs and Insights to monitor and optimize Docker usage.

## [Who's this for?](#whos-this-for)

* IT teams tasked with configuring and maintaining secure user access
* Security professionals focused on enforcing secure access practices
* Project managers overseeing team collaboration and resource management

## [What you'll learn](#what-youll-learn)

* How to assess and manage Docker user access and align accounts with organizational needs
* When to use team configurations for scalable access control
* How to automate and streamline user provisioning with SSO, SCIM, and JIT
* How to get the most out of Docker's monitoring tools

## [Tools integration](#tools-integration)

This guide covers integration with:

* Okta
* Entra ID SAML 2.0
* Azure Connect (OIDC)

## [Modules](#modules)

1. [Setting up roles and permissions in Docker](https://docs.docker.com/guides/admin-user-management/setup/)

   A guide to securely managing access and collaboration in Docker through roles and teams.

2. [Onboarding and managing roles and permissions in Docker](https://docs.docker.com/guides/admin-user-management/onboard/)

   Learn how to manage roles, invite members, and implement scalable access control in Docker for secure and efficient collaboration.

3. [Monitoring and insights](https://docs.docker.com/guides/admin-user-management/audit-and-monitor/)

   Track user actions, team workflows, and organizational trends with Activity logs and Insights to enhance security and productivity in Docker.

----
url: https://docs.docker.com/reference/cli/docker/stack/config/
----

# docker stack config

***

| Description | Outputs the final config file, after doing merges and interpolations |
| ----------- | -------------------------------------------------------------------- |
| Usage       | `docker stack config [OPTIONS]`                                      |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Outputs the final Compose file, after doing the merges and interpolations of the input Compose files.

## [Options](#options)

| Option                 | Default | Description                                       |
| ---------------------- | ------- | ------------------------------------------------- |
| `-c, --compose-file`   |         | Path to a Compose file, or `-` to read from stdin |
| `--skip-interpolation` |         | Skip interpolation and output only merged config  |

## [Examples](#examples)

The following command outputs the result of the merge and interpolation of two Compose files.

```console
$ docker stack config --compose-file docker-compose.yml --compose-file docker-compose.prod.yml
```

The Compose file can also be provided as standard input with `--compose-file -`:

```console
$ cat docker-compose.yml | docker stack config --compose-file -
```

### [Skipping interpolation](#skipping-interpolation)

In some cases, it might be useful to skip interpolation of environment variables. For example, when you want to pipe the output of this command back to `stack deploy`.

If you have a regex for a redirect route in an environment variable for your webserver you would use two `$` signs to prevent `stack deploy` from interpolating `${1}`.

```yaml
  service: webserver
  environment:
    REDIRECT_REGEX=http://host/redirect/$${1}
```

With interpolation, the `stack config` command will replace the environment variable in the Compose file with `REDIRECT_REGEX=http://host/redirect/${1}`, but then when piping it back to the `stack deploy` command it will be interpolated again and result in undefined behavior. That is why, when piping the output back to `stack deploy` one should always prefer the `--skip-interpolation` option.

```console
$ docker stack config --compose-file web.yml --compose-file web.prod.yml --skip-interpolation | docker stack deploy --compose-file -
```

----
url: https://docs.docker.com/guides/testcontainers-java-replace-h2/jdbc-url-approach/
----

# Replace H2 with the Testcontainers JDBC URL

***

Table of contents

***

Replacing H2 with a real PostgreSQL database requires two test properties:

```java
@DataJpaTest
@TestPropertySource(properties = {
  "spring.test.database.replace=none",
  "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db"
})
class ProductRepositoryWithJdbcUrlTest {

  @Autowired
  ProductRepository productRepository;

  @Test
  @Sql("classpath:/sql/seed-data.sql")
  void shouldGetAllProducts() {
    List<Product> products = productRepository.findAll();
    assertEquals(2, products.size());
  }
}
```

That's it — two properties and your tests run against a real PostgreSQL database.

## [How the special JDBC URL works](#how-the-special-jdbc-url-works)

A standard PostgreSQL JDBC URL looks like:

```text
jdbc:postgresql://localhost:5432/postgres
```

The Testcontainers special JDBC URL inserts `tc:` after `jdbc:`:

```text
jdbc:tc:postgresql:///db
```

The hostname, port, and database name are ignored — Testcontainers manages them automatically. You can specify the Docker image tag after the database name:

```text
jdbc:tc:postgresql:16-alpine:///db
```

This creates a container from the `postgres:16-alpine` image.

## [Initialize the database with a script](#initialize-the-database-with-a-script)

Pass `TC_INITSCRIPT` to run an SQL script when the container starts:

```text
jdbc:tc:postgresql:16-alpine:///db?TC_INITSCRIPT=sql/init-db.sql
```

Testcontainers runs the script automatically. For production applications, use a database migration tool like Flyway or Liquibase instead.

The special JDBC URL also works for MySQL, MariaDB, PostGIS, YugabyteDB, CockroachDB, and other databases with Testcontainers JDBC support.

## [Testing JdbcTemplate-based repositories](#testing-jdbctemplate-based-repositories)

The same approach works for `JdbcTemplate`-based repositories. Use `@JdbcTest` instead of `@DataJpaTest`:

```java
@JdbcTest
@TestPropertySource(properties = {
  "spring.test.database.replace=none",
  "spring.datasource.url=jdbc:tc:postgresql:16-alpine:///db?TC_INITSCRIPT=sql/init-db.sql"
})
class JdbcProductRepositoryTest {

  @Autowired
  private JdbcTemplate jdbcTemplate;

  private JdbcProductRepository productRepository;

  @BeforeEach
  void setUp() {
    productRepository = new JdbcProductRepository(jdbcTemplate);
  }

  @Test
  @Sql("/sql/seed-data.sql")
  void shouldGetAllProducts() {
    List<Product> products = productRepository.getAllProducts();
    assertEquals(2, products.size());
  }
}
```

[Use the JUnit 5 extension for more control »](https://docs.docker.com/guides/testcontainers-java-replace-h2/junit-extension-approach/)

----
url: https://docs.docker.com/engine/security/seccomp/
----

# Seccomp security profiles for Docker

***

Table of contents

***

Secure computing mode (`seccomp`) is a Linux kernel feature. You can use it to restrict the actions available within the container. The `seccomp()` system call operates on the seccomp state of the calling process. You can use this feature to restrict your application's access.

This feature is available only if Docker has been built with `seccomp` and the kernel is configured with `CONFIG_SECCOMP` enabled. To check if your kernel supports `seccomp`:

```console
$ grep CONFIG_SECCOMP= /boot/config-$(uname -r)
CONFIG_SECCOMP=y
```

## [Pass a profile for a container](#pass-a-profile-for-a-container)

The [default `seccomp` profile](https://github.com/moby/profiles/blob/main/seccomp/default.json) provides a sane default for running containers with seccomp and disables around 44 system calls out of 300+. It is moderately protective while providing wide application compatibility.

In effect, the profile is an allowlist that denies access to system calls by default and then allows specific system calls. The profile works by defining a `defaultAction` of `SCMP_ACT_ERRNO` and overriding that action only for specific system calls. The effect of `SCMP_ACT_ERRNO` is to cause a `Permission Denied` error. Next, the profile defines a specific list of system calls which are fully allowed, because their `action` is overridden to be `SCMP_ACT_ALLOW`. Finally, some specific rules are for individual system calls such as `personality`, and others, to allow variants of those system calls with specific arguments.

`seccomp` is instrumental for running Docker containers with least privilege. It is not recommended to change the default `seccomp` profile.

When you run a container, it uses the default profile unless you override it with the `--security-opt` option. For example, the following explicitly specifies a policy:

```console
$ docker run --rm \
             -it \
             --security-opt seccomp=/path/to/seccomp/profile.json \
             hello-world
```

### [Significant syscalls blocked by the default profile](#significant-syscalls-blocked-by-the-default-profile)

Docker's default seccomp profile is an allowlist which specifies the calls that are allowed. The table below lists the significant (but not all) syscalls that are effectively blocked because they are not on the allowlist. The table includes the reason each syscall is blocked rather than white-listed.

| Syscall             | Description                                                                                                                                                                                                                                                          |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `acct`              | Accounting syscall which could let containers disable their own resource limits or process accounting. Also gated by `CAP_SYS_PACCT`.                                                                                                                                |
| `add_key`           | Prevent containers from using the kernel keyring, which is not namespaced.                                                                                                                                                                                           |
| `bpf`               | Deny loading potentially persistent BPF programs into kernel, already gated by `CAP_SYS_ADMIN`.                                                                                                                                                                      |
| `clock_adjtime`     | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                                                                                                                                                                           |
| `clock_settime`     | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                                                                                                                                                                           |
| `clone`             | Deny cloning new namespaces. Also gated by `CAP_SYS_ADMIN` for CLONE\_\* flags, except `CLONE_NEWUSER`.                                                                                                                                                              |
| `create_module`     | Deny manipulation and functions on kernel modules. Obsolete. Also gated by `CAP_SYS_MODULE`.                                                                                                                                                                         |
| `delete_module`     | Deny manipulation and functions on kernel modules. Also gated by `CAP_SYS_MODULE`.                                                                                                                                                                                   |
| `finit_module`      | Deny manipulation and functions on kernel modules. Also gated by `CAP_SYS_MODULE`.                                                                                                                                                                                   |
| `get_kernel_syms`   | Deny retrieval of exported kernel and module symbols. Obsolete.                                                                                                                                                                                                      |
| `get_mempolicy`     | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                                                                                                                                                                              |
| `init_module`       | Deny manipulation and functions on kernel modules. Also gated by `CAP_SYS_MODULE`.                                                                                                                                                                                   |
| `ioperm`            | Prevent containers from modifying kernel I/O privilege levels. Already gated by `CAP_SYS_RAWIO`.                                                                                                                                                                     |
| `iopl`              | Prevent containers from modifying kernel I/O privilege levels. Already gated by `CAP_SYS_RAWIO`.                                                                                                                                                                     |
| `io_uring_enter`    | Blocked due to security vulnerabilities that can be exploited to break out of containers. See [moby/moby#46762](https://github.com/moby/moby/pull/46762).                                                                                                            |
| `io_uring_register` | Blocked due to security vulnerabilities that can be exploited to break out of containers. See [moby/moby#46762](https://github.com/moby/moby/pull/46762).                                                                                                            |
| `io_uring_setup`    | Blocked due to security vulnerabilities that can be exploited to break out of containers. See [moby/moby#46762](https://github.com/moby/moby/pull/46762).                                                                                                            |
| `kcmp`              | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                                                                                                                                                                              |
| `kexec_file_load`   | Sister syscall of `kexec_load` that does the same thing, slightly different arguments. Also gated by `CAP_SYS_BOOT`.                                                                                                                                                 |
| `kexec_load`        | Deny loading a new kernel for later execution. Also gated by `CAP_SYS_BOOT`.                                                                                                                                                                                         |
| `keyctl`            | Prevent containers from using the kernel keyring, which is not namespaced.                                                                                                                                                                                           |
| `lookup_dcookie`    | Tracing/profiling syscall, which could leak a lot of information on the host. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                         |
| `mbind`             | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                                                                                                                                                                              |
| `mount`             | Deny mounting, already gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                                                     |
| `move_pages`        | Syscall that modifies kernel memory and NUMA settings.                                                                                                                                                                                                               |
| `nfsservctl`        | Deny interaction with the kernel NFS daemon. Obsolete since Linux 3.1.                                                                                                                                                                                               |
| `open_by_handle_at` | Cause of an old container breakout. Also gated by `CAP_DAC_READ_SEARCH`.                                                                                                                                                                                             |
| `perf_event_open`   | Tracing/profiling syscall, which could leak a lot of information on the host.                                                                                                                                                                                        |
| `personality`       | Prevent container from enabling BSD emulation. Not inherently dangerous, but poorly tested, potential for a lot of kernel vulnerabilities.                                                                                                                           |
| `pivot_root`        | Deny `pivot_root`, should be privileged operation.                                                                                                                                                                                                                   |
| `process_vm_readv`  | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                                                                                                                                                                              |
| `process_vm_writev` | Restrict process inspection capabilities, already blocked by dropping `CAP_SYS_PTRACE`.                                                                                                                                                                              |
| `ptrace`            | Tracing/profiling syscall. Blocked in Linux kernel versions before 4.8 to avoid seccomp bypass. Tracing/profiling arbitrary processes is already blocked by dropping `CAP_SYS_PTRACE`, because it could leak a lot of information on the host.                       |
| `query_module`      | Deny manipulation and functions on kernel modules. Obsolete.                                                                                                                                                                                                         |
| `quotactl`          | Quota syscall which could let containers disable their own resource limits or process accounting. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                     |
| `reboot`            | Don't let containers reboot the host. Also gated by `CAP_SYS_BOOT`.                                                                                                                                                                                                  |
| `request_key`       | Prevent containers from using the kernel keyring, which is not namespaced.                                                                                                                                                                                           |
| `set_mempolicy`     | Syscall that modifies kernel memory and NUMA settings. Already gated by `CAP_SYS_NICE`.                                                                                                                                                                              |
| `setns`             | Deny associating a thread with a namespace. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                           |
| `settimeofday`      | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                                                                                                                                                                           |
| `stime`             | Time/date is not namespaced. Also gated by `CAP_SYS_TIME`.                                                                                                                                                                                                           |
| `socket`            | Blocked for `AF_ALG` to prevent in-container privilege escalation via the kernel cryptographic API ([CVE-2026-31431](https://nvd.nist.gov/vuln/detail/CVE-2026-31431)). Also blocked for `AF_VSOCK`. See [moby/moby#52494](https://github.com/moby/moby/pull/52494). |
| `socketcall`        | Denied to prevent bypassing socket address family filters on architectures with the legacy `socketcall` multiplexer (i386, s390, MIPS o32). See [moby/moby#52494](https://github.com/moby/moby/pull/52494).                                                          |
| `swapon`            | Deny start/stop swapping to file/device. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                              |
| `swapoff`           | Deny start/stop swapping to file/device. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                              |
| `sysfs`             | Obsolete syscall.                                                                                                                                                                                                                                                    |
| `_sysctl`           | Obsolete, replaced by /proc/sys.                                                                                                                                                                                                                                     |
| `umount`            | Should be a privileged operation. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                                     |
| `umount2`           | Should be a privileged operation. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                                     |
| `unshare`           | Deny cloning new namespaces for processes. Also gated by `CAP_SYS_ADMIN`, with the exception of `unshare --user`.                                                                                                                                                    |
| `uselib`            | Older syscall related to shared libraries, unused for a long time.                                                                                                                                                                                                   |
| `userfaultfd`       | Userspace page fault handling, largely needed for process migration.                                                                                                                                                                                                 |
| `ustat`             | Obsolete syscall.                                                                                                                                                                                                                                                    |
| `vm86`              | In kernel x86 real mode virtual machine. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                              |
| `vm86old`           | In kernel x86 real mode virtual machine. Also gated by `CAP_SYS_ADMIN`.                                                                                                                                                                                              |

## [Run without the default seccomp profile](#run-without-the-default-seccomp-profile)

You can pass `unconfined` to run a container without the default seccomp profile.

```console
$ docker run --rm -it --security-opt seccomp=unconfined debian:latest \
    unshare --map-root-user --user sh -c whoami
```

----
url: https://docs.docker.com/dhi/how-to/policies/
----

# Enforce Docker Hardened Image usage with policies

***

Table of contents

***

When you have a Docker Hardened Images Enterprise subscription, mirroring a Docker Hardened Image (DHI) repository automatically enables [Docker Scout](/scout/), allowing you to start enforcing security and compliance policies for your images without additional setup. Using Docker Scout policies, you can define and apply rules that ensure only approved and secure images, such as those based on DHIs, are used across your environments.

Docker Scout includes a dedicated [**Valid Docker Hardened Image (DHI) or DHI base image**](https://docs.docker.com/scout/policy/#valid-docker-hardened-image-dhi-or-dhi-base-image) policy type that validates whether your images are Docker Hardened Images or are built using a DHI as the base image. This policy checks for valid Docker signed verification summary attestations.

With policy evaluation built into Docker Scout, you can monitor image compliance in real time, integrate checks into your CI/CD workflows, and maintain consistent standards for image security and provenance.

## [View existing policies](#view-existing-policies)

To see the current policies applied to a mirrored DHI repository:

1. Go to the mirrored DHI repository in [Docker Hub](https://hub.docker.com).

2. Select **View on Scout**.

   This opens the [Docker Scout dashboard](https://scout.docker.com), where you can see which policies are currently active and whether your images meet the policy criteria.

Docker Scout automatically evaluates policy compliance when new images are pushed. Each policy includes a compliance result and a link to the affected images and layers.

## [Evaluate DHI policy compliance for your images](#evaluate-dhi-policy-compliance-for-your-images)

When you enable Docker Scout for your repositories, you can configure the [**Valid Docker Hardened Image (DHI) or DHI base image**](https://docs.docker.com/scout/policy/#valid-docker-hardened-image-dhi-or-dhi-base-image) policy. This optional policy validates whether your images are DHIs or built with DHI base images by checking for Docker signed verification summary attestations.

The following example shows how to build an image using a DHI base image and evaluate its compliance with the DHI policy.

### [Example: Build and evaluate a DHI-based image](#example-build-and-evaluate-a-dhi-based-image)

#### [Step 1: Use a DHI base image in your Dockerfile](#step-1-use-a-dhi-base-image-in-your-dockerfile)

Create a Dockerfile that uses a Docker Hardened Image mirrored repository as the base. For example:

```dockerfile
# Dockerfile
FROM <your-namespace>/dhi-python:3.13-alpine3.21

ENTRYPOINT ["python", "-c", "print('Hello from a DHI-based image')"]
```

#### [Step 2: Build and push the image](#step-2-build-and-push-the-image)

Open a terminal and navigate to the directory containing your Dockerfile. Then, build and push the image to your Docker Hub repository:

```console
$ docker build \
  --push \
  -t <your-namespace>/my-dhi-app:v1 .
```

#### [Step 3: Enable Docker Scout](#step-3-enable-docker-scout)

To enable Docker Scout for your organization and the repository, run the following commands in your terminal:

```console
$ docker login
$ docker scout enroll <your-namespace>
$ docker scout repo enable --org <your-namespace> <your-namespace>/my-dhi-app
```

#### [Step 4: Configure the DHI policy](#step-4-configure-the-dhi-policy)

Once Docker Scout is enabled, you can configure the **Valid Docker Hardened Image (DHI) or DHI base image** policy for your organization:

1. Go to the [Docker Scout dashboard](https://scout.docker.com).
2. Select your organization and navigate to **Policies**.
3. Configure the **Valid Docker Hardened Image (DHI) or DHI base image** policy to enable it for your repositories.

For more information on configuring policies, see [Configure policies](https://docs.docker.com/scout/policy/configure/).

#### [Step 5: View policy compliance](#step-5-view-policy-compliance)

Once the DHI policy is configured and active, you can view compliance results:

1. Go to the [Docker Scout dashboard](https://scout.docker.com).
2. Select your organization and navigate to **Images**.
3. Find your image, `<your-namespace>/my-dhi-app:v1`, and select the link in the **Compliance** column.

This shows the policy compliance results for your image. The **Valid Docker Hardened Image (DHI) or DHI base image** policy evaluates whether your image has a valid Docker signed verification summary attestation or if its base image has such an attestation.

You can now [evaluate policy compliance in your CI](/scout/policy/ci/).

----
url: https://docs.docker.com/reference/cli/docker/network/create/
----

# docker network create

***

| Description | Create a network                          |
| ----------- | ----------------------------------------- |
| Usage       | `docker network create [OPTIONS] NETWORK` |

## [Description](#description)

Creates a new network. The `DRIVER` accepts `bridge` or `overlay` which are the built-in network drivers. If you have installed a third party or your own custom network driver you can specify that `DRIVER` here also. If you don't specify the `--driver` option, the command automatically creates a `bridge` network for you. When you install Docker Engine it creates a `bridge` network automatically. This network corresponds to the `docker0` bridge that Docker Engine has traditionally relied on. When you launch a new container with `docker run` it automatically connects to this bridge network. You cannot remove this default bridge network, but you can create new ones using the `network create` command.

```console
$ docker network create -d bridge my-bridge-network
```

Bridge networks are isolated networks on a single Docker Engine installation. If you want to create a network that spans multiple Docker hosts each running Docker Engine, you must enable Swarm mode, and create an `overlay` network. To read more about overlay networks with Swarm mode, see ["*use overlay networks*"](/network/overlay/).

Once you have enabled swarm mode, you can create a swarm-scoped overlay network:

```console
$ docker network create --scope=swarm --attachable -d overlay my-multihost-network
```

By default, swarm-scoped networks do not allow manually started containers to be attached. This restriction is added to prevent someone that has access to a non-manager node in the swarm cluster from running a container that is able to access the network stack of a swarm service.

The `--attachable` option used in the example above disables this restriction, and allows for both swarm services and manually started containers to attach to the overlay network.

Network names must be unique. The Docker daemon attempts to identify naming conflicts but this is not guaranteed. It is the user's responsibility to avoid name conflicts.

### [Overlay network limitations](#overlay-network-limitations)

You should create overlay networks with `/24` blocks (the default), which limits you to 256 IP addresses, when you create networks using the default VIP-based endpoint-mode. This recommendation addresses [limitations with swarm mode](https://github.com/moby/moby/issues/30820). If you need more than 256 IP addresses, do not increase the IP block size. You can either use `dnsrr` endpoint mode with an external load balancer, or use multiple smaller overlay networks. See [Configure service discovery](/engine/swarm/networking/#configure-service-discovery) for more information about different endpoint modes.

## [Options](#options)

| Option                    | Default  | Description                                                |
| ------------------------- | -------- | ---------------------------------------------------------- |
| `--attachable`            |          | API 1.25+ Enable manual container attachment               |
| `--aux-address`           |          | Auxiliary IPv4 or IPv6 addresses used by Network driver    |
| `--config-from`           |          | API 1.30+ The network from which to copy the configuration |
| `--config-only`           |          | API 1.30+ Create a configuration only network              |
| `-d, --driver`            | `bridge` | Driver to manage the Network                               |
| `--gateway`               |          | IPv4 or IPv6 Gateway for the master subnet                 |
| [`--ingress`](#ingress)   |          | API 1.29+ Create swarm routing-mesh network                |
| [`--internal`](#internal) |          | Restrict external access to the network                    |
| `--ip-range`              |          | Allocate container ip from a sub-range                     |
| `--ipam-driver`           |          | IP Address Management Driver                               |
| `--ipam-opt`              |          | Set IPAM driver specific options                           |
| `--ipv4`                  | `true`   | Enable or disable IPv4 address assignment                  |
| `--ipv6`                  |          | Enable or disable IPv6 address assignment                  |
| `--label`                 |          | Set metadata on a network                                  |
| `-o, --opt`               |          | Set driver specific options                                |
| `--scope`                 |          | API 1.30+ Control the network's scope                      |
| `--subnet`                |          | Subnet in CIDR format that represents a network segment    |

## [Examples](#examples)

### [Connect containers](#connect-containers)

When you start a container, use the `--network` flag to connect it to a network. This example adds the `busybox` container to the `mynet` network:

```console
$ docker run -itd --network=mynet busybox
```

If you want to add a container to a network after the container is already running, use the `docker network connect` subcommand.

You can connect multiple containers to the same network. Once connected, the containers can communicate using only another container's IP address or name. For `overlay` networks or custom plugins that support multi-host connectivity, containers connected to the same multi-host network but launched from different daemons can also communicate in this way.

You can disconnect a container from a network using the `docker network disconnect` command.

### [Specify advanced options](#specify-advanced-options)

When you create a network, Docker Engine creates a non-overlapping subnetwork for the network by default. This subnetwork is not a subdivision of an existing network. It is purely for ip-addressing purposes. You can override this default and specify subnetwork values directly using the `--subnet` option. On a `bridge` network you can only create a single subnet:

```console
$ docker network create --driver=bridge --subnet=192.168.0.0/16 br0
```

Additionally, you also specify the `--gateway` `--ip-range` and `--aux-address` options.

```console
$ docker network create \
  --driver=bridge \
  --subnet=172.28.0.0/16 \
  --ip-range=172.28.5.0/24 \
  --gateway=172.28.5.254 \
  br0
```

If you omit the `--gateway` flag, Docker Engine selects one for you from inside a preferred pool. For `overlay` networks and for network driver plugins that support it you can create multiple subnetworks. This example uses two `/25` subnet mask to adhere to the current guidance of not having more than 256 IPs in a single overlay network. Each of the subnetworks has 126 usable addresses.

```console
$ docker network create -d overlay \
  --subnet=192.168.10.0/25 \
  --subnet=192.168.20.0/25 \
  --gateway=192.168.10.100 \
  --gateway=192.168.20.100 \
  --aux-address="my-router=192.168.10.5" --aux-address="my-switch=192.168.10.6" \
  --aux-address="my-printer=192.168.20.5" --aux-address="my-nas=192.168.20.6" \
  my-multihost-network
```

Be sure that your subnetworks do not overlap. If they do, the network create fails and Docker Engine returns an error.

### [Bridge driver options](#bridge-driver-options)

When creating a custom `bridge` network, the following additional options can be passed. Some of these have equivalent flags that can be used on the dockerd command line or in `daemon.json` to configure the default bridge, `docker0`:

| Network create option                            | Daemon option for `docker0` | Description                                           |
| ------------------------------------------------ | --------------------------- | ----------------------------------------------------- |
| `com.docker.network.bridge.name`                 | -                           | Bridge name to be used when creating the Linux bridge |
| `com.docker.network.bridge.enable_ip_masquerade` | `--ip-masq`                 | Enable IP masquerading                                |
| `com.docker.network.bridge.enable_icc`           | `--icc`                     | Enable or Disable Inter Container Connectivity        |
| `com.docker.network.bridge.host_binding_ipv4`    | `--ip`                      | Default IP when binding container ports               |
| `com.docker.network.driver.mtu`                  | `--mtu`                     | Set the containers network MTU                        |
| `com.docker.network.container_iface_prefix`      | -                           | Set a custom prefix for container interfaces          |

The following arguments can be passed to `docker network create` for any network driver, again with their approximate equivalents to Docker daemon flags used for the `docker0` bridge:

| Network create option | Daemon option for `docker0`       | Description                                |
| --------------------- | --------------------------------- | ------------------------------------------ |
| `--gateway`           | -                                 | IPv4 or IPv6 Gateway for the master subnet |
| `--ip-range`          | `--fixed-cidr`, `--fixed-cidr-v6` | Allocate IP addresses from a range         |
| `--internal`          | -                                 | Restrict external access to the network    |
| `--ipv4`              | -                                 | Enable or disable IPv4 address assignment  |
| `--ipv6`              | `--ipv6`                          | Enable or disable IPv6 address assignment  |
| `--subnet`            | `--bip`, `--bip6`                 | Subnet for network                         |

For example, let's use `-o` or `--opt` options to specify an IP address binding when publishing ports:

```console
$ docker network create \
    -o "com.docker.network.bridge.host_binding_ipv4"="172.19.0.1" \
    simple-network
```

### [Network internal mode (--internal)](#internal)

Containers on an internal network may communicate between each other, but not with any other network, as no default route is configured and firewall rules are set up to drop all traffic to or from other networks. Communication with the gateway IP address (and thus appropriately configured host services) is possible, and the host may communicate with any container IP directly.

By default, when you connect a container to an `overlay` network, Docker also connects a bridge network to it to provide external connectivity. If you want to create an externally isolated `overlay` network, you can specify the `--internal` option.

### [Network ingress mode (--ingress)](#ingress)

You can create the network which will be used to provide the routing-mesh in the swarm cluster. You do so by specifying `--ingress` when creating the network. Only one ingress network can be created at the time. The network can be removed only if no services depend on it. Any option available when creating an overlay network is also available when creating the ingress network, besides the `--attachable` option.

```console
$ docker network create -d overlay \
  --subnet=10.11.0.0/16 \
  --ingress \
  --opt com.docker.network.driver.mtu=9216 \
  --opt encrypted=true \
  my-ingress-network
```

### [Run services on predefined networks](#run-services-on-predefined-networks)

You can create services on the predefined Docker networks `bridge` and `host`.

```console
$ docker service create --name my-service \
  --network host \
  --replicas 2 \
  busybox top
```

### [Swarm networks with local scope drivers](#swarm-networks-with-local-scope-drivers)

You can create a swarm network with local scope network drivers. You do so by promoting the network scope to `swarm` during the creation of the network. You will then be able to use this network when creating services.

```console
$ docker network create -d bridge \
  --scope swarm \
  --attachable \
  swarm-network
```

For network drivers which provide connectivity across hosts (ex. macvlan), if node specific configurations are needed in order to plumb the network on each host, you will supply that configuration via a configuration only network. When you create the swarm scoped network, you will then specify the name of the network which contains the configuration.

```console
node1$ docker network create --config-only --subnet 192.168.100.0/24 --gateway 192.168.100.115 mv-config
node2$ docker network create --config-only --subnet 192.168.200.0/24 --gateway 192.168.200.202 mv-config
node1$ docker network create -d macvlan --scope swarm --config-from mv-config --attachable swarm-network
```

----
url: https://docs.docker.com/guides/testcontainers-python-getting-started/write-tests/
----

# Write tests with Testcontainers

***

Table of contents

***

You'll create a PostgreSQL container using Testcontainers and use it for all the tests. Before each test, you'll delete all customer records so that tests run with a clean database.

## [Set up pytest fixtures](#set-up-pytest-fixtures)

This guide uses [pytest fixtures](https://pytest.org/en/stable/how-to/fixtures.html) for setup and teardown logic. A recommended approach is to use [finalizers](https://pytest.org/en/stable/how-to/fixtures.html#adding-finalizers-directly) to guarantee cleanup runs even if setup fails:

```python
@pytest.fixture
def setup(request):
    # setup code

    def cleanup():
        # teardown code

    request.addfinalizer(cleanup)
    return some_value
```

## [Create the test file](#create-the-test-file)

Create a `tests/__init__.py` file with empty content to enable pytest [auto-discovery](https://pytest.org/explanation/goodpractices.html#test-discovery).

Then create `tests/test_customers.py` with the fixtures:

```python
import os
import pytest
from testcontainers.postgres import PostgresContainer

from customers import customers

postgres = PostgresContainer("postgres:16-alpine")


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def remove_container():
        postgres.stop()

    request.addfinalizer(remove_container)
    os.environ["DB_CONN"] = postgres.get_connection_url()
    os.environ["DB_HOST"] = postgres.get_container_host_ip()
    os.environ["DB_PORT"] = str(postgres.get_exposed_port(5432))
    os.environ["DB_USERNAME"] = postgres.username
    os.environ["DB_PASSWORD"] = postgres.password
    os.environ["DB_NAME"] = postgres.dbname
    customers.create_table()


@pytest.fixture(scope="function", autouse=True)
def setup_data():
    customers.delete_all_customers()
```

Here's what the fixtures do:

* The `setup` fixture has `scope="module"`, so it runs once for all tests in the file. It starts a PostgreSQL container, sets environment variables with the connection details, and creates the `customers` table. A cleanup function removes the container after all tests complete.
* The `setup_data` fixture has `scope="function"`, so it runs before every test. It deletes all records to give each test a clean database.

## [Write the tests](#write-the-tests)

Add the test functions to the same file:

```python
def test_get_all_customers():
    customers.create_customer("Siva", "siva@gmail.com")
    customers.create_customer("James", "james@gmail.com")
    customers_list = customers.get_all_customers()
    assert len(customers_list) == 2


def test_get_customer_by_email():
    customers.create_customer("John", "john@gmail.com")
    customer = customers.get_customer_by_email("john@gmail.com")
    assert customer.name == "John"
    assert customer.email == "john@gmail.com"
```

* `test_get_all_customers()` inserts two customer records, fetches all customers, and asserts the count.
* `test_get_customer_by_email()` inserts a customer, fetches it by email, and asserts the details.

Because `setup_data` deletes all records before each test, the tests can run in any order.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-python-getting-started/run-tests/)

----
url: https://docs.docker.com/build/ci/github-actions/secrets/
----

# Using secrets with GitHub Actions

***

Table of contents

***

A build secret is sensitive information, such as a password or API token, consumed as part of the build process. Docker Build supports two forms of secrets:

* [Secret mounts](#secret-mounts) add secrets as files in the build container (under `/run/secrets` by default).
* [SSH mounts](#ssh-mounts) add SSH agent sockets or keys into the build container.

This page shows how to use secrets with GitHub Actions. For an introduction to secrets in general, see [Build secrets](https://docs.docker.com/build/building/secrets/).

## [Secret mounts](#secret-mounts)

In the following example uses and exposes the [`GITHUB_TOKEN` secret](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#about-the-github_token-secret) as provided by GitHub in your workflow.

First, create a `Dockerfile` that uses the secret:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine
RUN --mount=type=secret,id=github_token,env=GITHUB_TOKEN ...
```

In this example, the secret name is `github_token`. The following workflow exposes this secret using the `secrets` input:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build
        uses: docker/build-push-action@v7
        with:
          platforms: linux/amd64,linux/arm64
          tags: user/app:latest
          secrets: |
            "github_token=${{ secrets.GITHUB_TOKEN }}"
```

> Note
>
> Secrets are mounted as files in the build container. By default, they're available at `/run/secrets/<id>`. You can also use the `env` option to load a secret into an environment variable, or the `target` option to customize the mount path. For details on secret mounts, see [Build secrets](https://docs.docker.com/build/building/secrets/).

### [Secret sources](#secret-sources)

The `docker/build-push-action` inputs for secret mounts define where the secret value comes from. The Dockerfile `RUN --mount=type=secret` options define how the build step consumes the secret.

| Action input                           | Source                             | Equivalent Buildx option                 |
| -------------------------------------- | ---------------------------------- | ---------------------------------------- |
| `secrets: MY_SECRET=value`             | Inline value from the workflow     | `--secret id=MY_SECRET,src=<temp-file>`  |
| `secret-envs: MY_SECRET=MY_ENV_VAR`    | Environment variable on the runner | `--secret id=MY_SECRET,env=MY_ENV_VAR`   |
| `secret-files: MY_SECRET=./secret.txt` | File on the runner                 | `--secret id=MY_SECRET,src=./secret.txt` |

For example, `RUN --mount=type=secret,id=MY_SECRET` mounts the secret as a file at `/run/secrets/MY_SECRET`. To expose the same secret as an environment variable for a `RUN` instruction, use the `env` option in the Dockerfile: `RUN --mount=type=secret,id=MY_SECRET,env=MY_SECRET`.

### [Using environment variables as secret sources](#using-environment-variables-as-secret-sources)

The `secret-envs` input reads secrets from environment variables on the GitHub Actions runner. Use it when a previous workflow step sets an environment variable, or when you want to map a runner environment variable to a different secret ID for the build.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build
        uses: docker/build-push-action@v7
        env:
          SENTRY_AUTH_TOKEN: ${{ secrets.SENTRY_AUTH_TOKEN }}
        with:
          context: .
          secret-envs: |
            sentry_token=SENTRY_AUTH_TOKEN
          tags: user/app:latest
```

In your Dockerfile, mount the secret and expose it as an environment variable for the command that needs it:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

RUN --mount=type=secret,id=sentry_token,env=SENTRY_AUTH_TOKEN \
    npm run build
```

### [Using secret files](#using-secret-files)

The `secret-files` input lets you mount existing files as secrets in your build. This is useful when you need to use credential files that are generated during your workflow, or when you need to mount configuration files like `.npmrc` or `.pypirc` that are already in the expected format.

The key difference between `secrets`, `secret-envs`, and `secret-files`:

* `secrets`: Pass secret values as strings from the workflow.
* `secret-envs`: Read secret values from environment variables on the runner.
* `secret-files`: Mount existing files from the runner's filesystem.

#### [Example: Using .npmrc for private npm packages](#example-using-npmrc-for-private-npm-packages)

If your build needs to install packages from a private npm registry, you can create an `.npmrc` file and mount it as a secret:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Create .npmrc file
        run: |
          echo "//registry.npmjs.org/:_authToken=${{ secrets.NPM_TOKEN }}" > .npmrc

      - name: Build
        uses: docker/build-push-action@v7
        with:
          context: .
          secret-files: |
            npmrc=./.npmrc
          tags: user/app:latest
```

In your Dockerfile, mount the secret file to the expected location:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./

RUN --mount=type=secret,id=npmrc,target=/root/.npmrc \
    npm ci

COPY . .

RUN npm run build
```

If a `RUN` instruction uses a non-root user, set `uid`, `gid`, or `mode` on the secret mount so the user can read the mounted file:

```dockerfile
RUN --mount=type=secret,id=npmrc,target=/home/node/.npmrc,uid=1000,gid=1000 \
    npm ci
```

#### [Example: Using dynamically generated credentials](#example-using-dynamically-generated-credentials)

You can generate credential files from multiple secrets and mount them:

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v6

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Create credentials file
        run: |
          cat <<EOF > aws-credentials
          [default]
          aws_access_key_id = ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key = ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          EOF

      - name: Build
        uses: docker/build-push-action@v7
        with:
          context: .
          secret-files: |
            aws=./aws-credentials
          tags: user/app:latest
```

In your Dockerfile:

```dockerfile
# syntax=docker/dockerfile:1
FROM alpine

RUN apk add --no-cache aws-cli

RUN --mount=type=secret,id=aws,target=/root/.aws/credentials \
    aws s3 cp s3://my-private-bucket/data.tar.gz /tmp/
```

### [Multi-line secrets](#multi-line-secrets)

If you're using [GitHub secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets) and need to handle multi-line value, you will need to place the key-value pair between quotes:

```yaml
secrets: |
  "MYSECRET=${{ secrets.GPG_KEY }}"
  GIT_AUTH_TOKEN=abcdefghi,jklmno=0123456789
  "MYSECRET=aaaaaaaa
  bbbbbbb
  ccccccccc"
  FOO=bar
  "EMPTYLINE=aaaa

  bbbb
  ccc"
  "JSON_SECRET={""key1"":""value1"",""key2"":""value2""}"
```

| Key              | Value                               |
| ---------------- | ----------------------------------- |
| `MYSECRET`       | `***********************`           |
| `GIT_AUTH_TOKEN` | `abcdefghi,jklmno=0123456789`       |
| `MYSECRET`       | `aaaaaaaa\nbbbbbbb\nccccccccc`      |
| `FOO`            | `bar`                               |
| `EMPTYLINE`      | `aaaa\n\nbbbb\nccc`                 |
| `JSON_SECRET`    | `{"key1":"value1","key2":"value2"}` |

> Note
>
> Double escapes are needed for quote signs.

## [SSH mounts](#ssh-mounts)

SSH mounts let you authenticate with SSH servers. For example to perform a `git clone`, or to fetch application packages from a private repository.

The following Dockerfile example uses an SSH mount to fetch Go modules from a private GitHub repository.

```dockerfile
# syntax=docker/dockerfile:1

ARG GO_VERSION="1.25"

FROM golang:${GO_VERSION}-alpine AS base
ENV CGO_ENABLED=0
ENV GOPRIVATE="github.com/foo/*"
RUN apk add --no-cache file git rsync openssh-client
RUN mkdir -p -m 0700 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
WORKDIR /src

FROM base AS vendor
# this step configure git and checks the ssh key is loaded
RUN --mount=type=ssh <<EOT
  set -e
  echo "Setting Git SSH protocol"
  git config --global url."git@github.com:".insteadOf "https://github.com/"
  (
    set +e
    ssh -T git@github.com
    if [ ! "$?" = "1" ]; then
      echo "No GitHub SSH key loaded exiting..."
      exit 1
    fi
  )
EOT
# this one download go modules
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=ssh \
    go mod download -x

FROM vendor AS build
RUN --mount=type=bind,target=. \
    --mount=type=cache,target=/go/pkg/mod \
    --mount=type=cache,target=/root/.cache \
    go build ...
```

To build this Dockerfile, you must specify an SSH mount that the builder can use in the steps with `--mount=type=ssh`.

The following GitHub Action workflow uses the `MrSquaare/ssh-setup-action` third-party action to bootstrap SSH setup on the GitHub runner. The action creates a private key defined by the GitHub Action secret `SSH_GITHUB_PPK` and adds it to the SSH agent socket file at `SSH_AUTH_SOCK`. The SSH mount in the build step assume `SSH_AUTH_SOCK` by default, so there's no need to specify the ID or path for the SSH agent socket explicitly.

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          ssh: default
          push: true
          tags: user/app:latest
```

```yaml
name: ci

on:
  push:

jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Set up SSH
        uses: MrSquaare/ssh-setup-action@2d028b70b5e397cf8314c6eaea229a6c3e34977a # v3.1.0
        with:
          host: github.com
          private-key: ${{ secrets.SSH_GITHUB_PPK }}
          private-key-name: github-ppk

      - name: Build
        uses: docker/bake-action@v7
        with:
          set: |
            *.ssh=default
```

----
url: https://docs.docker.com/dhi/explore/scanner-integrations/
----

# Scanner integrations

***

Table of contents

***

Docker Hardened Images work with various vulnerability scanners. However, to get accurate results that reflect the actual security posture of these images, your scanner needs to understand the VEX (Vulnerability Exploitability eXchange) attestations included with each image.

## [Scanners with VEX support](#scanners-with-vex-support)

The following scanners can read and apply VEX attestations included with Docker Hardened Images:

| Scanner                                                                                              | VEX application                         |
| ---------------------------------------------------------------------------------------------------- | --------------------------------------- |
| [Docker Scout](/scout/)                                                                              | Automatic, zero configuration           |
| [Trivy](https://trivy.dev/)                                                                          | VEX Hub (recommended) or local VEX file |
| [Grype](https://github.com/anchore/grype)                                                            | Via `--vex` flag with local VEX file    |
| [Wiz](https://docs.wiz.io/)                                                                          | Automatic, zero configuration           |
| [Mend.io](https://docs.mend.io/platform/latest/docker-hardened-images)                               | Automatic, zero configuration           |
| [Black Duck](https://documentation.blackduck.com/bundle/bd-hub/page/Reporting/vexReport_global.html) | Automatic, zero configuration           |
| [Aikido](https://help.aikido.dev/container-image-scanning/standalone-registries/docker-hub-images)   | Automatic, zero configuration           |

For step-by-step instructions for Docker Scout, Trivy, and Grype, see [Scan Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/). For Wiz, Mend.io, Black Duck, and Aikido, refer to their respective documentation.

## [Choosing a scanner for Docker Hardened Images](#choosing-a-scanner-for-docker-hardened-images)

When selecting a scanner for use with Docker Hardened Images, whether it supports open standards like OpenVEX is the key differentiator.

Docker Hardened Images include signed VEX attestations that follow the [OpenVEX standard](https://openvex.dev/). OpenVEX is an open standard that meets the minimum requirements for VEX defined by CISA (Cybersecurity and Infrastructure Security Agency), the U.S. government agency responsible for cybersecurity guidance. These attestations document which vulnerabilities don't apply to the image and why, helping you focus on real risks. To understand what VEX is and how it works, see the [VEX core concept](https://docs.docker.com/dhi/core-concepts/vex/).

Because OpenVEX is an open standard with government backing, it has strong industry momentum and any tool can implement it without vendor-specific integrations. This matters when you bring in third-party auditors with their own scanning tools, or when you want to use multiple security tools in your pipeline. With VEX, these tools can all read and verify the same vulnerability data directly from your images.

Without open standards like VEX, vendors make exploitability decisions using proprietary methods, making it difficult to verify claims or compare results across tools. This fragments your security toolchain and creates inconsistent vulnerability assessments across different scanning tools.

### [Benefits of scanners with VEX support](#benefits-of-scanners-with-vex-support)

Scanners that support open standards like OpenVEX and can interpret VEX attestations from Docker Hardened Images offer the following benefits:

* Accurate vulnerability counts: Automatically filter out vulnerabilities that don't apply to your specific image, often reducing false positives dramatically.
* Transparency and auditability: Verify exactly why vulnerabilities are or aren't flagged; security teams and compliance officers can review the reasoning rather than trusting a vendor's black box.
* Scanner flexibility: Switch between any VEX-enabled scanner (Docker Scout, Trivy, Grype, etc.) without losing vulnerability context or rebuilding exclusion lists.
* Consistent results: VEX-enabled scanners interpret the same data the same way, eliminating discrepancies between tools.
* Faster workflows: Focus on real risks rather than researching why reported CVEs don't actually affect your deployment.

### [Scanners without VEX support](#scanners-without-vex-support)

Scanners that can't read VEX attestations will report vulnerabilities that don't apply to Docker Hardened Images. This creates operational challenges:

* Manual filtering required: You'll need to maintain scanner-specific ignore lists to replicate what VEX statements already document.
* Higher false positive rates: Expect to see more reported vulnerabilities that don't represent real risks.
* Increased investigation time: Security teams spend time researching why CVEs don't apply instead of addressing actual vulnerabilities. With Docker Hardened Images, security experts at Docker manage this investigation for you, thoroughly vetting each justification before adding it to a VEX statement.
* CI/CD friction: Build pipelines may fail on vulnerabilities that aren't exploitable in your images.

### [VEX-based vulnerability handling versus proprietary approaches](#vex-based-vulnerability-handling-versus-proprietary-approaches)

Docker Hardened Images use VEX attestations based on the OpenVEX open standard to document vulnerability exploitability. OpenVEX is an open standard that is recognized by government agencies such as CISA. This open standards approach differs from how some other image vendors handle vulnerabilities using proprietary methods.

#### [Docker Hardened Images with VEX](#docker-hardened-images-with-vex)

The image includes signed attestations that explain which vulnerabilities don't apply and why. Any VEX-enabled scanner can read these attestations, giving you:

* Tool flexibility: Use any scanner that supports OpenVEX (Docker Scout, Trivy, Grype, etc.)
* Complete transparency: Review the exact reasoning for each vulnerability assessment
* Full auditability: Security teams and compliance officers can independently verify all vulnerability assessments and reasoning
* Historical visibility: VEX statements remain with the image, so you can always check vulnerability status, even for older versions

#### [Proprietary vulnerability handling](#proprietary-vulnerability-handling)

Some image vendors use proprietary advisory feeds or internal databases instead of VEX. While this may result in fewer reported vulnerabilities, it creates significant limitations:

* Tool dependency: You must use the vendor's preferred scanning tools to see their vulnerability filtering, while standard scanners will still report all CVEs; scanners must implement proprietary feeds rather than using open standards that work with all images
* No transparency: Proprietary feeds act as "black boxes" - vulnerabilities simply disappear from vendor tools with no explanation
* Limited verifiability: Security teams have no way to independently verify why vulnerabilities are excluded or whether the reasoning is sound
* Maintenance challenges: If you scan older image versions with standard tools, you can't determine which vulnerabilities actually applied at that time, making long-term security tracking difficult
* Ecosystem incompatibility: Your existing security tools (SCA, policy engines, compliance scanners) can't access or verify the vendor's proprietary vulnerability data

The fundamental difference: VEX-based approaches explain vulnerability assessments using open standards that any tool can verify and audit. Proprietary approaches hide vulnerabilities in vendor-specific systems where the reasoning can't be independently validated.

For Docker Hardened Images, use VEX-enabled scanners to get accurate results that work across your entire security toolchain.

## [What to expect from different scanners](#what-to-expect-from-different-scanners)

When scanning Docker Hardened Images with different tools, you'll see significant differences in reported vulnerability counts.

### [What VEX-enabled scanners filter automatically](#what-vex-enabled-scanners-filter-automatically)

When you scan Docker Hardened Images with VEX-enabled scanners, they automatically exclude vulnerabilities that don't apply:

* Hardware-specific vulnerabilities: Issues that only affect specific hardware architectures (for example, Power10 processors) that are irrelevant to containerized workloads.
* Unreachable code paths: CVEs in code that exists in the package but isn't executed in the image's runtime configuration.
* Build-time only issues: Vulnerabilities in build tools or dependencies that don't exist in the final runtime image.
* Temporary identifiers: Placeholder vulnerability IDs (like Debian's `TEMP-xxxxxxx`) that aren't intended for external tracking.

### [Using scanners without VEX support](#using-scanners-without-vex-support)

If your scanner doesn't support VEX, you'll need to manually exclude vulnerabilities through scanner-specific mechanisms like ignore lists or policy exceptions. This requires:

* Reviewing VEX statements from Docker Hardened Images
* Translating VEX justifications into your scanner's format
* Maintaining these exclusions as new vulnerabilities are discovered
* Repeating this process if you switch scanners or add additional scanning tools

## [What's next](#whats-next)

Learn how to [scan Docker Hardened Images](https://docs.docker.com/dhi/how-to/scan/) with VEX-compliant scanners.

----
url: https://docs.docker.com/compose/how-tos/gpu-support/
----

# Run Docker Compose services with GPU access

***

Table of contents

***

Compose services can define GPU device reservations if the Docker host contains such devices and the Docker Daemon is set accordingly. For this, make sure you install the [prerequisites](https://docs.docker.com/engine/containers/resource_constraints/#gpu) if you haven't already done so.

The examples in the following sections focus specifically on providing service containers access to GPU devices with Docker Compose.

## [Enabling GPU access to service containers](#enabling-gpu-access-to-service-containers)

GPUs are referenced in a `compose.yaml` file using the [device](https://docs.docker.com/reference/compose-file/deploy/#devices) attribute from the Compose Deploy specification, within your services that need them.

This provides more granular control over a GPU reservation as custom values can be set for the following device properties:

* `capabilities`. This value is specified as a list of strings. For example, `capabilities: [gpu]`. You must set this field in the Compose file. Otherwise, it returns an error on service deployment.
* `count`. Specified as an integer or the value `all`, represents the number of GPU devices that should be reserved (providing the host holds that number of GPUs). If `count` is set to `all` or not specified, all GPUs available on the host are used by default.
* `device_ids`. This value, specified as a list of strings, represents GPU device IDs from the host. You can find the device ID in the output of `nvidia-smi` on the host. If no `device_ids` are set, all GPUs available on the host are used by default.
* `driver`. Specified as a string, for example `driver: 'nvidia'`
* `options`. Key-value pairs representing driver specific options.

> Important
>
> You must set the `capabilities` field. Otherwise, it returns an error on service deployment.

> Note
>
> `count` and `device_ids` are mutually exclusive. You must only define one field at a time.

For more information on these properties, see the [Compose Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#devices).

### [Example of a Compose file for running a service with access to 1 GPU device](#example-of-a-compose-file-for-running-a-service-with-access-to-1-gpu-device)

```yaml
services:
  test:
    image: nvidia/cuda:12.9.0-base-ubuntu22.04
    command: nvidia-smi
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

Run with Docker Compose:

```console
$ docker compose up
Creating network "gpu_default" with the default driver
Creating gpu_test_1 ... done
Attaching to gpu_test_1    
test_1  | +-----------------------------------------------------------------------------+
test_1  | | NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.1     |
test_1  | |-------------------------------+----------------------+----------------------+
test_1  | | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
test_1  | | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
test_1  | |                               |                      |               MIG M. |
test_1  | |===============================+======================+======================|
test_1  | |   0  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
test_1  | | N/A   23C    P8     9W /  70W |      0MiB / 15109MiB |      0%      Default |
test_1  | |                               |                      |                  N/A |
test_1  | +-------------------------------+----------------------+----------------------+
test_1  |                                                                                
test_1  | +-----------------------------------------------------------------------------+
test_1  | | Processes:                                                                  |
test_1  | |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
test_1  | |        ID   ID                                                   Usage      |
test_1  | |=============================================================================|
test_1  | |  No running processes found                                                 |
test_1  | +-----------------------------------------------------------------------------+
gpu_test_1 exited with code 0
```

On machines hosting multiple GPUs, the `device_ids` field can be set to target specific GPU devices and `count` can be used to limit the number of GPU devices assigned to a service container.

You can use `count` or `device_ids` in each of your service definitions. An error is returned if you try to combine both, specify an invalid device ID, or use a value of count that’s higher than the number of GPUs in your system.

```console
$ nvidia-smi   
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 450.80.02    Driver Version: 450.80.02    CUDA Version: 11.0     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  Tesla T4            On   | 00000000:00:1B.0 Off |                    0 |
| N/A   72C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   1  Tesla T4            On   | 00000000:00:1C.0 Off |                    0 |
| N/A   67C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   2  Tesla T4            On   | 00000000:00:1D.0 Off |                    0 |
| N/A   74C    P8    12W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
|   3  Tesla T4            On   | 00000000:00:1E.0 Off |                    0 |
| N/A   62C    P8    11W /  70W |      0MiB / 15109MiB |      0%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+
```

## [Access specific devices](#access-specific-devices)

To allow access only to GPU-0 and GPU-3 devices:

```yaml
services:
  test:
    image: tensorflow/tensorflow:latest-gpu
    command: python -c "import tensorflow as tf;tf.test.gpu_device_name()"
    deploy:
      resources:
        reservations:
          devices:
          - driver: nvidia
            device_ids: ['0', '3']
            capabilities: [gpu]
```

----
url: https://docs.docker.com/reference/cli/docker/container/prune/
----

# docker container prune

***

| Description | Remove all stopped containers      |
| ----------- | ---------------------------------- |
| Usage       | `docker container prune [OPTIONS]` |

## [Description](#description)

Removes all stopped containers.

## [Options](#options)

| Option                | Default | Description                                      |
| --------------------- | ------- | ------------------------------------------------ |
| [`--filter`](#filter) |         | Provide filter values (e.g. `until=<timestamp>`) |
| `-f, --force`         |         | Do not prompt for confirmation                   |

## [Examples](#examples)

### [Prune containers](#prune-containers)

```console
$ docker container prune
WARNING! This will remove all stopped containers.
Are you sure you want to continue? [y/N] y
Deleted Containers:
4a7f7eebae0f63178aff7eb0aa39cd3f0627a203ab2df258c1a00b456cf20063
f98f9c2aa1eaf727e4ec9c0283bc7d4aa4762fbdba7f26191f26c97f64090360

Total reclaimed space: 212 B
```

### [Filtering (--filter)](#filter)

The filtering flag (`--filter`) format is of "key=value". If there is more than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

When multiple filters are provided, they are combined as follows:

* Multiple filters with **different keys** are combined using AND logic. A container must satisfy all filter conditions to be pruned.
* Multiple filters with the **same key** are combined using OR logic. A container is pruned if it matches any of the values for that key.

For example, `--filter "label=foo" --filter "until=24h"` prunes containers that have the `foo` label **and** were created more than 24 hours ago. Conversely, `--filter "label=foo" --filter "label=bar"` prunes containers that have **either** the `foo` **or** `bar` label.

The currently supported filters are:

* until (`<timestamp>`) - only remove containers created before given timestamp
* label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove containers with (or without, in case `label!=...` is used) the specified labels.

The `until` filter can be Unix timestamps, date formatted timestamps, or Go duration strings supported by [ParseDuration](https://pkg.go.dev/time#ParseDuration) (e.g. `10m`, `1h30m`) computed relative to the daemon machine’s time. Supported formats for date formatted time stamps include RFC3339Nano, RFC3339, `2006-01-02T15:04:05`, `2006-01-02T15:04:05.999999999`, `2006-01-02T07:00`, and `2006-01-02`. The local timezone on the daemon will be used if you do not provide either a `Z` or a `+-00:00` timezone offset at the end of the timestamp. When providing Unix timestamps enter seconds\[.nanoseconds], where seconds is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds (aka Unix epoch or Unix time), and the optional .nanoseconds field is a fraction of a second no more than nine digits long.

The `label` filter accepts two formats. One is the `label=...` (`label=<key>` or `label=<key>=<value>`), which removes containers with the specified labels. The other format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes containers without the specified labels.

The following removes containers created more than 5 minutes ago:

```console
$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
61b9efa71024        busybox             "sh"                2017-01-04 13:23:33 -0800 PST   Exited (0) 41 seconds ago
53a9bc23a516        busybox             "sh"                2017-01-04 13:11:59 -0800 PST   Exited (0) 12 minutes ago

$ docker container prune --force --filter "until=5m"

Deleted Containers:
53a9bc23a5168b6caa2bfbefddf1b30f93c7ad57f3dec271fd32707497cb9369

Total reclaimed space: 25 B

$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
61b9efa71024        busybox             "sh"                2017-01-04 13:23:33 -0800 PST   Exited (0) 44 seconds ago
```

The following removes containers created before `2017-01-04T13:10:00`:

```console
$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
53a9bc23a516        busybox             "sh"                2017-01-04 13:11:59 -0800 PST   Exited (0) 7 minutes ago
4a75091a6d61        busybox             "sh"                2017-01-04 13:09:53 -0800 PST   Exited (0) 9 minutes ago

$ docker container prune --force --filter "until=2017-01-04T13:10:00"

Deleted Containers:
4a75091a6d618526fcd8b33ccd6e5928ca2a64415466f768a6180004b0c72c6c

Total reclaimed space: 27 B

$ docker ps -a --format 'table {{.ID}}\t{{.Image}}\t{{.Command}}\t{{.CreatedAt}}\t{{.Status}}'

CONTAINER ID        IMAGE               COMMAND             CREATED AT                      STATUS
53a9bc23a516        busybox             "sh"                2017-01-04 13:11:59 -0800 PST   Exited (0) 9 minutes ago
```

----
url: https://docs.docker.com/engine/release-notes/17.03/
----

# Docker Engine 17.03 release notes

***

Table of contents

***

## [17.03.3-ce](#17033-ce)

2018-08-30

### [Runtime](#runtime)

* Update go-connections to d217f8e [#28](https://github.com/docker/engine/pull/28)

## [17.03.2-ce](#17032-ce)

2017-05-29

### [Networking](#networking)

* Fix a concurrency issue preventing network creation [#33273](https://github.com/moby/moby/pull/33273)

### [Runtime](#runtime-1)

* Relabel secrets path to avoid a Permission Denied on selinux enabled systems [#33236](https://github.com/moby/moby/pull/33236) (ref [#32529](https://github.com/moby/moby/pull/32529)
* Fix cases where local volume were not properly relabeled if needed [#33236](https://github.com/moby/moby/pull/33236) (ref [#29428](https://github.com/moby/moby/pull/29428))
* Fix an issue while upgrading if a plugin rootfs was still mounted [#33236](https://github.com/moby/moby/pull/33236) (ref [#32525](https://github.com/moby/moby/pull/32525))
* Fix an issue where volume wouldn't default to the `rprivate` propagation mode [#33236](https://github.com/moby/moby/pull/33236) (ref [#32851](https://github.com/moby/moby/pull/32851))
* Fix a panic that could occur when a volume driver could not be retrieved [#33236](https://github.com/moby/moby/pull/33236) (ref [#32347](https://github.com/moby/moby/pull/32347))

- Add a warning in `docker info` when the `overlay` or `overlay2` graphdriver is used on a filesystem without `d_type` support [#33236](https://github.com/moby/moby/pull/33236) (ref [#31290](https://github.com/moby/moby/pull/31290))

* Fix an issue with backporting mount spec to older volumes [#33207](https://github.com/moby/moby/pull/33207)
* Fix issue where a failed unmount can lead to data loss on local volume remove [#33120](https://github.com/moby/moby/pull/33120)

### [Swarm Mode](#swarm-mode)

* Fix a case where tasks could get killed unexpectedly [#33118](https://github.com/moby/moby/pull/33118)
* Fix an issue preventing to deploy services if the registry cannot be reached despite the needed images being locally present [#33117](https://github.com/moby/moby/pull/33117)

## [17.03.1-ce](#17031-ce)

2017-03-27

### [Remote API (v1.27) & Client](#remote-api-v127--client)

* Fix autoremove on older api [#31692](https://github.com/docker/docker/pull/31692)
* Fix default network customization for a stack [#31258](https://github.com/docker/docker/pull/31258/)
* Correct CPU usage calculation in presence of offline CPUs and newer Linux [#31802](https://github.com/docker/docker/pull/31802)
* Fix issue where service healthcheck is `{}` in remote API [#30197](https://github.com/docker/docker/pull/30197)

### [Runtime](#runtime-2)

* Update runc to 54296cf40ad8143b62dbcaa1d90e520a2136ddfe [#31666](https://github.com/docker/docker/pull/31666)
* Ignore cgroup2 mountpoints [opencontainers/runc#1266](https://github.com/opencontainers/runc/pull/1266)
* Update containerd to 4ab9917febca54791c5f071a9d1f404867857fcc [#31662](https://github.com/docker/docker/pull/31662) [#31852](https://github.com/docker/docker/pull/31852)
* Register healtcheck service before calling restore() [docker/containerd#609](https://github.com/docker/containerd/pull/609)
* Fix `docker exec` not working after unattended upgrades that reload apparmor profiles [#31773](https://github.com/docker/docker/pull/31773)
* Fix unmounting layer without merge dir with Overlay2 [#31069](https://github.com/docker/docker/pull/31069)
* Do not ignore "volume in use" errors when force-delete [#31450](https://github.com/docker/docker/pull/31450)

### [Swarm Mode](#swarm-mode-1)

* Update swarmkit to 17756457ad6dc4d8a639a1f0b7a85d1b65a617bb [#31807](https://github.com/docker/docker/pull/31807)
* Scheduler now correctly considers tasks which have been assigned to a node but aren't yet running [docker/swarmkit#1980](https://github.com/docker/swarmkit/pull/1980)
* Allow removal of a network when only dead tasks reference it [docker/swarmkit#2018](https://github.com/docker/swarmkit/pull/2018)
* Retry failed network allocations less aggressively [docker/swarmkit#2021](https://github.com/docker/swarmkit/pull/2021)
* Avoid network allocation for tasks that are no longer running [docker/swarmkit#2017](https://github.com/docker/swarmkit/pull/2017)
* Bookkeeping fixes inside network allocator allocator [docker/swarmkit#2019](https://github.com/docker/swarmkit/pull/2019) [docker/swarmkit#2020](https://github.com/docker/swarmkit/pull/2020)

### [Windows](#windows)

* Cleanup HCS on restore [#31503](https://github.com/docker/docker/pull/31503)

## [17.03.0-ce](#17030-ce)

2017-03-01

> Important
>
> Starting with this release, Docker is on a monthly release cycle and uses a new YY.MM versioning scheme to reflect this. Two channels are available: monthly and quarterly. Any given monthly release will only receive security and bugfixes until the next monthly release is available. Quarterly releases receive security and bugfixes for 4 months after initial release. This release includes bugfixes for 1.13.1 but there are no major feature additions and the API version stays the same. Upgrading from Docker 1.13.1 to 17.03.0 is expected to be simple and low-risk.

### [Client](#client)

* Fix panic in `docker stats --format` [#30776](https://github.com/docker/docker/pull/30776)

### [Contrib](#contrib)

* Update various `bash` and `zsh` completion scripts [#30823](https://github.com/docker/docker/pull/30823), [#30945](https://github.com/docker/docker/pull/30945) and more...
* Block obsolete socket families in default seccomp profile - mitigates unpatched kernels' CVE-2017-6074 [#29076](https://github.com/docker/docker/pull/29076)

### [Networking](#networking-1)

* Fix bug on overlay encryption keys rotation in cross-datacenter swarm [#30727](https://github.com/docker/docker/pull/30727)
* Fix side effect panic in overlay encryption and network control plane communication failure ("No installed keys could decrypt the message") on frequent swarm leader re-election [#25608](https://github.com/docker/docker/pull/25608)
* Several fixes around system responsiveness and datapath programming when using overlay network with external kv-store [docker/libnetwork#1639](https://github.com/docker/libnetwork/pull/1639), [docker/libnetwork#1632](https://github.com/docker/libnetwork/pull/1632) and more...
* Discard incoming plain vxlan packets for encrypted overlay network [#31170](https://github.com/docker/docker/pull/31170)
* Release the network attachment on allocation failure [#31073](https://github.com/docker/docker/pull/31073)
* Fix port allocation when multiple published ports map to the same target port [docker/swarmkit#1835](https://github.com/docker/swarmkit/pull/1835)

### [Runtime](#runtime-3)

* Fix a deadlock in docker logs [#30223](https://github.com/docker/docker/pull/30223)
* Fix CPU spin waiting for log write events [#31070](https://github.com/docker/docker/pull/31070)
* Fix a possible crash when using journald [#31231](https://github.com/docker/docker/pull/31231) [#31263](https://github.com/docker/docker/pull/31263)
* Fix a panic on close of nil channel [#31274](https://github.com/docker/docker/pull/31274)
* Fix duplicate mount point for `--volumes-from` in `docker run` [#29563](https://github.com/docker/docker/pull/29563)
* Fix `--cache-from` does not cache last step [#31189](https://github.com/docker/docker/pull/31189)

### [Swarm Mode](#swarm-mode-2)

* Shutdown leaks an error when the container was never started [#31279](https://github.com/docker/docker/pull/31279)
* Fix possibility of tasks getting stuck in the "NEW" state during a leader failover [docker/swarmkit#1938](https://github.com/docker/swarmkit/pull/1938)
* Fix extraneous task creations for global services that led to confusing replica counts in `docker service ls` [docker/swarmkit#1957](https://github.com/docker/swarmkit/pull/1957)
* Fix problem that made rolling updates slow when `task-history-limit` was set to 1 [docker/swarmkit#1948](https://github.com/docker/swarmkit/pull/1948)
* Restart tasks elsewhere, if appropriate, when they are shut down as a result of nodes no longer satisfying constraints [docker/swarmkit#1958](https://github.com/docker/swarmkit/pull/1958)
* (experimental)

----
url: https://docs.docker.com/compose/how-tos/lifecycle/
----

# Using lifecycle hooks with Compose

***

Table of contents

***

Requires: Docker Compose [2.30.0](https://github.com/docker/compose/releases/tag/v2.30.0) and later

## [Services lifecycle hooks](#services-lifecycle-hooks)

When Docker Compose runs a container, it uses two elements, [ENTRYPOINT and COMMAND](https://docs.docker.com/engine/containers/run/#default-command-and-options), to manage what happens when the container starts and stops.

However, it can sometimes be easier to handle these tasks separately with lifecycle hooks - commands that run right after the container starts or just before it stops.

Lifecycle hooks are particularly useful because they can have special privileges (like running as the root user), even when the container itself runs with lower privileges for security. This means that certain tasks requiring higher permissions can be done without compromising the overall security of the container.

### [Post-start hooks](#post-start-hooks)

Post-start hooks are commands that run after the container has started, but there's no set time for when exactly they will execute. The hook execution timing is not assured during the execution of the container's `entrypoint`.

Because there is no ordering guarantee between the hook and the container's entrypoint, post-start hooks are best suited for tasks that do not need to complete before the application begins running, such as registering the container with an external system.

In the following example, after the container starts, a root-level hook registers the service with an internal service registry. The application does not depend on registration being complete before it starts serving requests.

```yaml
services:
  app:
    image: backend
    user: 1001
    post_start:
      - command: /opt/scripts/register-service.sh
        user: root
```

### [Pre-stop hooks](#pre-stop-hooks)

Pre-stop hooks are commands that run before the container is stopped by a specific command (like `docker compose down` or stopping it manually with `Ctrl+C`). These hooks won't run if the container stops by itself or gets killed suddenly.

Because the pre-stop hook runs before the stop signal is sent to the container, it is suited for actions that must complete while the application is still fully running.

In the following example, the hook backs up a data file before the container receives the stop signal.

```yaml
services:
  app:
    image: backend
    volumes:
      - data:/data
    pre_stop:
      - command: cp /data/app.db /data/app.db.bak

volumes:
  data: {} # a Docker volume is created with root ownership
```

## [Reference information](#reference-information)

* [`post_start`](https://docs.docker.com/reference/compose-file/services/#post_start)
* [`pre_stop`](https://docs.docker.com/reference/compose-file/services/#pre_stop)

----
url: https://docs.docker.com/guides/php/configure-ci-cd/
----

# Configure CI/CD for your PHP application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize a PHP application](https://docs.docker.com/guides/php/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. In your local repository on your machine, run the following command to rename the branch to main.

   ```console
   $ git branch -M main
   ```

8. Run the following commands to stage, commit, and then push your local repository to GitHub.

   ```console
   $ git add -A
   $ git commit -m "my first commit"
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

         - name: Build and test
           uses: docker/build-push-action@v7
           with:
             target: test
             load: true

         - name: Build and push
           uses: docker/build-push-action@v7
           with:
             platforms: linux/amd64,linux/arm64
             push: true
             target: final
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

[Test your PHP deployment »](https://docs.docker.com/guides/php/deploy/)

----
url: https://docs.docker.com/reference/cli/sbx/create/opencode/
----

# sbx create opencode

| Description | Create a sandbox for opencode                |
| ----------- | -------------------------------------------- |
| Usage       | `sbx create opencode PATH [PATH...] [flags]` |

## [Description](#description)

Create a sandbox with access to a host workspace for opencode.

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
sbx create opencode .

# Create with a specific path
sbx create opencode /path/to/project

# Create with additional read-only workspaces
sbx create opencode . /path/to/docs:ro
```

----
url: https://docs.docker.com/guides/github-sonarqube-sandbox/workflow/
----

# Build a code quality check workflow

***

Table of contents

***

In this section, you'll build a complete code quality automation workflow step-by-step. You'll start by creating an E2B sandbox with GitHub and SonarQube MCP servers, then progressively add functionality until you have a production-ready workflow that analyzes code quality and creates pull requests.

By working through each step sequentially, you'll learn how MCP servers work, how to interact with them through Claude, and how to chain operations together to build powerful automation workflows.

## [Prerequisites](#prerequisites)

Before you begin, make sure you have:

* E2B account with [API access](https://e2b.dev/docs/api-key)

* [Anthropic API key](https://docs.claude.com/en/api/admin-api/apikeys/get-api-key)

  > Note
  >
  > This example uses Claude CLI which comes pre-installed in E2B sandboxes, but you can adapt the example to work with other AI assistants of your choice. See [E2B's MCP documentation](https://e2b.dev/docs/mcp/quickstart) for alternative connection methods.

* GitHub account with:

  * A repository containing code to analyze
  * [Personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with `repo` scope

* SonarCloud account with:

  * [Organization](https://docs.sonarsource.com/sonarqube-cloud/administering-sonarcloud/resources-structure/organization) created
  * [Project configured](https://docs.sonarsource.com/sonarqube-community-build/project-administration/creating-and-importing-projects) for your repository
  * [User token](https://docs.sonarsource.com/sonarqube-server/instance-administration/security/administering-tokens) generated

* Language runtime installed:

  * TypeScript: [Node.js 18+](https://nodejs.org/en/download)
  * Python: [Python 3.8+](https://www.python.org/downloads/)

> Note
>
> This guide uses Claude's `--dangerously-skip-permissions` flag to enable automated command execution in E2B sandboxes. This flag bypasses permission prompts, which is appropriate for isolated container environments like E2B where sandboxes are disposable and separate from your local machine.
>
> However, be aware that Claude can execute any commands within the sandbox, including accessing files and credentials available in that environment. Only use this approach with trusted code and workflows. For more information, see [Anthropic's guidance on container security](https://docs.anthropic.com/en/docs/claude-code/devcontainer).

## [Set up your project](#set-up-your-project)

1. Create a new directory for your workflow and initialize Node.js:

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   npm init -y
   ```

2. Open `package.json` and configure it for ES modules:

   ```json
   {
     "name": "github-sonarqube-workflow",
     "version": "1.0.0",
     "description": "Automated code quality workflow using E2B, GitHub, and SonarQube",
     "type": "module",
     "main": "quality-workflow.ts",
     "scripts": {
       "start": "tsx quality-workflow.ts"
     },
     "keywords": ["e2b", "github", "sonarqube", "mcp", "code-quality"],
     "author": "",
     "license": "MIT"
   }
   ```

3. Install required dependencies:

   ```bash
   npm install e2b dotenv
   npm install -D typescript tsx @types/node
   ```

4. Create a `.env` file in your project root:

   ```bash
   touch .env
   ```

5. Add your API keys and configuration, replacing the placeholders with your actual credentials:

   ```plaintext
   E2B_API_KEY=your_e2b_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GITHUB_TOKEN=ghp_your_personal_access_token_here
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   SONARQUBE_ORG=your_sonarcloud_org_key
   SONARQUBE_TOKEN=your_sonarqube_user_token
   SONARQUBE_URL=https://sonarcloud.io
   ```

6. Protect your credentials by adding `.env` to `.gitignore`:

   ```bash
   echo ".env" >> .gitignore
   echo "node_modules/" >> .gitignore
   ```

1) Create a new directory for your workflow:

   ```bash
   mkdir github-sonarqube-workflow
   cd github-sonarqube-workflow
   ```

2) Create a virtual environment and activate it:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3) Install required dependencies:

   ```bash
   pip install e2b python-dotenv
   ```

4) Create a `.env` file in your project root:

   ```bash
   touch .env
   ```

5) Add your API keys and configuration, replacing the placeholders with your actual credentials:

   ```plaintext
   E2B_API_KEY=your_e2b_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GITHUB_TOKEN=ghp_your_personal_access_token_here
   GITHUB_OWNER=your_github_username
   GITHUB_REPO=your_repository_name
   SONARQUBE_ORG=your_sonarcloud_org_key
   SONARQUBE_TOKEN=your_sonarqube_user_token
   SONARQUBE_URL=https://sonarcloud.io
   ```

6) Protect your credentials by adding `.env` to `.gitignore`:

   ```bash
   echo ".env" >> .gitignore
   echo "venv/" >> .gitignore
   echo "__pycache__/" >> .gitignore
   ```

## [Step 1: Create your first sandbox](#step-1-create-your-first-sandbox)

Let's start by creating a sandbox and verifying the MCP servers are configured correctly.

Create a file named `01-test-connection.ts` in your project root:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function testConnection() {
  console.log(
    "Creating E2B sandbox with GitHub and SonarQube MCP servers...\n",
  );

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
