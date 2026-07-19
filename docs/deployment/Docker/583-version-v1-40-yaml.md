url: https://docs.docker.com/reference/api/engine/version/v1.40.yaml
----

basePath: "/v1.40"
info:
 title: "Docker Engine API"
 version: "1.40"

 If you omit the version-prefix, the current version of the API (v1.40) is used.
 For example, calling \`/info\` is the same as calling \`/v1.40/info\`. Using the

 \- \`npipe\` a named pipe from the host into the container.
 \- \`tmpfs\` a \`tmpfs\`.
 \- \`volume\` a docker volume with the given \`Name\`.
 type: "string"
 enum:
 \- "bind"
 \- "npipe"
 \- "tmpfs"
 \- "volume"
 example: "volume"

 MountPoint:
 type: "object"
 description: \|
 MountPoint represents a mount point configuration inside the container.
 This is used for reporting the mountpoints in use by a container.
 properties:
 Type:
 description: \|
 The mount type:

 \- \`bind\` a mount of a file or directory from the host into the container.

 must exist prior to creating the container.

 For \`Type=npipe\`, the pipe must exist prior to creating the container.
 type: "string"
 Type:
 description: \|
 The mount type. Available types:

 \- \`bind\` Mounts a file or directory from the host into the container. The \`Source\` must exist prior to creating the container.
 \- \`npipe\` Mounts a named pipe from the host into the container. The \`Source\` must exist prior to creating the container.
 \- \`tmpfs\` Create a tmpfs with the given options. The mount \`Source\` cannot be specified for tmpfs.
 \- \`volume\` Creates a volume with the given name and options (or uses a pre-existing volume with the same name and options). These are \*\*not\*\* removed when the container is removed.
 allOf:
 \- $ref: "#/definitions/MountType"
 ReadOnly:
 description: "Whether the mount should be read-only."
 type: "boolean"
 Consistency:
 description: "The consistency requirement for the mount: \`default\`, \`consistent\`, \`cached\`, or \`delegated\`."
 type: "string"
 BindOptions:
 description: "Optional configuration for the \`bind\` type."
 type: "object"
 properties:
 Propagation:
 description: "A propagation mode with the value \`\[r\]private\`, \`\[r\]shared\`, or \`\[r\]slave\`."
 type: "string"
 enum:
 \- "private"
 \- "rprivate"
 \- "shared"
 \- "rshared"
 \- "slave"
 \- "rslave"
 NonRecursive:
 description: "Disable recursive bind mount."

 KernelMemory:
 description: "Kernel memory limit in bytes."
 type: "integer"
 format: "int64"
 example: 209715200
 KernelMemoryTCP:
 description: "Hard limit for kernel TCP buffer memory (in bytes)."
 type: "integer"
 format: "int64"
 MemoryReservation:
 description: "Memory soft limit in bytes."
 type: "integer"
 format: "int64"
 MemorySwap:
 description: \|
 Total memory limit (memory + swap). Set as \`-1\` to enable unlimited
 swap.
 type: "integer"
 format: "int64"
 MemorySwappiness:
 description: \|
 Tune a container's memory swappiness behavior. Accepts an integer
 between 0 and 100.
 type: "integer"
 format: "int64"
 minimum: 0
 maximum: 100
 NanoCpus:
 description: "CPU quota in units of 10-9 CPUs."
 type: "integer"
 format: "int64"
 OomKillDisable:
 description: "Disable OOM Killer for the container."
 type: "boolean"
 Init:
 description: \|
 Run an init inside the container that forwards signals and reaps
 processes. This field is omitted if empty, and the default (as
 configured on the daemon) is used.
 type: "boolean"
 x-nullable: true
 PidsLimit:
 description: \|
 Tune a container's PIDs limit. Set \`0\` or \`-1\` for unlimited, or \`null\`
 to not change.
 type: "integer"
 format: "int64"
 x-nullable: true
 Ulimits:
 description: \|
 A list of resource limits to set in the container. For example:

 \`\`\`
 {"Name": "nofile", "Soft": 1024, "Hard": 2048}
 \`\`\`
 type: "array"
 items:
 type: "object"
 properties:
 Name:
 description: "Name of ulimit"
 type: "string"
 Soft:
 description: "Soft limit"
 type: "integer"
 Hard:
 description: "Hard limit"
 type: "integer"
 # Applicable to Windows
 CpuCount:
 description: \|
 The number of usable CPUs (Windows only).

 On Windows Server containers, the processor resource controls are
 mutually exclusive. The order of precedence is \`CPUCount\` first, then
 \`CPUShares\`, and \`CPUPercent\` last.
 type: "integer"
 format: "int64"
 CpuPercent:
 description: \|
 The usable percentage of the available CPUs (Windows only).

 On Windows Server containers, the processor resource controls are
 mutually exclusive. The order of precedence is \`CPUCount\` first, then
 \`CPUShares\`, and \`CPUPercent\` last.
 type: "integer"
 format: "int64"
 IOMaximumIOps:
 description: "Maximum IOps for the container system drive (Windows only)"
 type: "integer"
 format: "int64"
 IOMaximumBandwidth:
 description: \|
 Maximum IO in bytes per second for the container system drive
 (Windows only).
 type: "integer"
 format: "int64"


 # Applicable to UNIX platforms
 Capabilities:
 type: "array"
 description: \|
 A list of kernel capabilities to be available for container (this
 overrides the default set).

 Conflicts with options 'CapAdd' and 'CapDrop'"
 items:
 type: "string"
 CapAdd:
 type: "array"
 description: \|
 A list of kernel capabilities to add to the container. Conflicts
 with option 'Capabilities'.
 items:
 type: "string"
 CapDrop:
 type: "array"
 description: \|
 A list of kernel capabilities to drop from the container. Conflicts
 with option 'Capabilities'.
 items:
 type: "string"

 ConsoleSize:
 type: "array"
 description: \|
 Initial console size, as an \`\[height, width\]\` array. (Windows only)
 minItems: 2
 maxItems: 2
 items:
 type: "integer"
 minimum: 0

 the image itself and all of its parent images. Docker v1.10 and up
 store images self-contained, and no longer use a parent-chain, making
 this field an equivalent of the Size field.

 This field is kept for backward compatibility, but may be removed in
 a future version of the API.
 type: "integer"
 format: "int64"
 x-nullable: false

 required:
 \- Id
 \- ParentId
 \- RepoTags
 \- RepoDigests
 \- Created
 \- Size
 \- SharedSize
 \- VirtualSize
 \- Labels
 \- Containers

 ParentId:
 description: \|
 ID of the parent image.

 Depending on how the image was created, this field may be empty and
 is only set for images that were built/created locally. This field
 is empty if the image was pulled from an image registry.
 type: "string"
 x-nullable: false
 example: ""

 x-nullable: false

 x-nullable: false
 items:
 type: "string"
 example:
 \- "example@sha256:afcc7f1ac1b49db317a7196c902e61c6c3c4607d63599ee1a82d702d249a0ccb"
 \- "internal.registry.example.com:5000/example@sha256:b69959407d21e8a062e0416bf13405bb2b71ed7a84dde4158ebafacfa06f5578"
 Created:
 description: \|
 Date and time at which the image was created as a Unix timestamp
 (number of seconds since EPOCH).
 type: "integer"
 x-nullable: false
 example: "1644009612"
 Size:
 description: \|
 Total size of the image including all layers it is composed of.
 type: "integer"
 format: "int64"
 x-nullable: false
 example: 172064416
 SharedSize:
 description: \|
 Total size of image layers that are shared between this image and other
 images.

 This size is not calculated by default. \`-1\` indicates that the value
 has not been set / calculated.
 type: "integer"
 format: "int64"
 x-nullable: false
 example: 1239828
 VirtualSize:
 description: \|
 Total size of the image including all layers it is composed of.

 In versions of Docker before v1.10, this field was calculated from
 the image itself and all of its parent images. Docker v1.10 and up
 store images self-contained, and no longer use a parent-chain, making
 this field an equivalent of the Size field.

 This field is kept for backward compatibility, but may be removed in
 a future version of the API.
 type: "integer"
 format: "int64"
 x-nullable: false
 example: 172064416
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 x-nullable: false
 additionalProperties:
 type: "string"
 example:
 com.example.some-label: "some-value"
 com.example.some-other-label: "some-other-value"
 Containers:
 description: \|
 Number of containers using this image. Includes both stopped and running
 containers.

 This size is not calculated by default, and depends on which API endpoint
 is used. \`-1\` indicates that the value has not been set / calculated.
 x-nullable: false
 type: "integer"
 example: 2

 Options:
 type: "object"
 description: \|
 The driver specific options used when creating the volume.
 additionalProperties:
 type: "string"
 example:
 device: "tmpfs"
 o: "size=100m,uid=1000"
 type: "tmpfs"
 UsageData:
 type: "object"
 x-nullable: true
 required: \[Size, RefCount\]
 description: \|
 Usage details about the volume. This information is used by the
 \`GET /system/df\` endpoint, and omitted in other endpoints.
 properties:
 Size:
 type: "integer"
 format: "int64"
 default: -1
 description: \|
 Amount of disk space used by the volume (in bytes). This information
 is only available for volumes created with the \`"local"\` volume
 driver. For volumes created with other volume drivers, this field
 is set to \`-1\` ("not available")
 x-nullable: false
 RefCount:
 type: "integer"
 format: "int64"
 default: -1
 description: \|
 The number of containers referencing this volume. This field
 is set to \`-1\` if the reference-count is not available.
 x-nullable: false

 VolumeCreateOptions:
 description: "Volume configuration"
 type: "object"
 title: "VolumeConfig"
 x-go-name: "VolumeCreateBody"
 properties:
 Name:
 description: \|
 The new volume's name. If not specified, Docker generates a name.
 type: "string"
 x-nullable: false
 example: "tardis"
 Driver:
 description: "Name of the volume driver to use."
 type: "string"
 default: "local"
 x-nullable: false
 example: "custom"
 DriverOpts:
 description: \|
 A mapping of driver options and values. These options are
 passed directly to the driver and are driver specific.
 type: "object"
 additionalProperties:
 type: "string"
 example:
 device: "tmpfs"
 o: "size=100m,uid=1000"
 type: "tmpfs"

 VolumeListResponse:
 type: "object"
 title: "VolumeListResponse"
 x-go-name: "VolumeListOKBody"
 description: "Volume list response"
 properties:
 Volumes:
 type: "array"
 description: "List of volumes"
 items:
 $ref: "#/definitions/Volume"
 Warnings:
 type: "array"
 description: \|
 Warnings that occurred when fetching the list of volumes.
 items:
 type: "string"
 example: \[\]

 Network:
 type: "object"
 properties:
 Name:
 type: "string"
 Id:
 type: "string"
 Created:
 type: "string"
 format: "dateTime"
 Scope:
 type: "string"
 Driver:
 type: "string"
 EnableIPv6:
 type: "boolean"
 IPAM:
 $ref: "#/definitions/IPAM"
 Internal:
 type: "boolean"
 Attachable:
 type: "boolean"
 Ingress:
 type: "boolean"
 Containers:
 type: "object"
 additionalProperties:
 $ref: "#/definitions/NetworkContainer"
 Options:
 type: "object"
 additionalProperties:
 type: "string"
 Labels:
 type: "object"
 additionalProperties:
 type: "string"
 example:
 Name: "net01"
 Id: "7d86d31b1478e7cca9ebed7e73aa0fdeec46c5ca29497431d3007d2d9e15ed99"
 Created: "2016-10-19T04:33:30.360899459Z"
 Scope: "local"
 Driver: "bridge"
 EnableIPv6: false
 IPAM:
 Driver: "default"
 Config:
 \- Subnet: "172.19.0.0/16"
 Gateway: "172.19.0.1"
 Options:
 foo: "bar"
 Internal: false
 Attachable: false
 Ingress: false
 Containers:
 com.docker.network.bridge.default\_bridge: "true"
 com.docker.network.bridge.enable\_icc: "true"
 com.docker.network.bridge.enable\_ip\_masquerade: "true"
 com.docker.network.bridge.host\_binding\_ipv4: "0.0.0.0"
 com.docker.network.bridge.name: "docker0"
 com.docker.network.driver.mtu: "1500"
 Labels:
 com.example.some-label: "some-value"
 com.example.some-other-label: "some-other-value"
 IPAM:
 type: "object"
 properties:
 Driver:
 description: "Name of the IPAM driver to use."
 type: "string"
 default: "default"
 Config:
 description: \|
 List of IPAM configuration options, specified as a map:

 \`\`\`
 {"Subnet": , "IPRange": , "Gateway": , "AuxAddress": }
 \`\`\`
 type: "array"
 items:
 type: "object"
 additionalProperties:
 type: "string"
 Options:
 description: "Driver-specific options, specified as a map."
 type: "object"
 additionalProperties:
 type: "string"

 NetworkContainer:
 type: "object"
 properties:
 Name:
 type: "string"
 EndpointID:
 type: "string"
 MacAddress:
 type: "string"
 IPv4Address:
 type: "string"
 IPv6Address:
 type: "string"

 Parent:
 description: \|
 ID of the parent build cache record.
 type: "string"
 example: "hw53o5aio51xtltp5xjp8v7fx"

NetworkAttachmentSpec:
description: \|
Read-only spec type for non-swarm containers attached to swarm overlay
networks.



 \> \*\*Note\*\*: ContainerSpec, NetworkAttachmentSpec, and PluginSpec are
 \> mutually exclusive. PluginSpec is only used when the Runtime field
 \> is set to \`plugin\`. NetworkAttachmentSpec is used when the Runtime
 \> field is set to \`attachment\`.
 type: "object"
 properties:
 ContainerID:
 description: "ID of the container represented by this task"
 type: "string"
 Resources:
 description: \|
 Resource requirements which apply to each individual container created
 as part of the service.
 type: "object"
 properties:
 Limits:
 description: "Define resources limits."
 $ref: "#/definitions/ResourceObject"

 DesiredState:
 $ref: "#/definitions/TaskState"
 example:
 ID: "0kzzo1i0y4jz6027t0k7aezc7"
 Version:
 Index: 71
 CreatedAt: "2016-06-07T21:07:31.171892745Z"
 UpdatedAt: "2016-06-07T21:07:31.376370513Z"
 Spec:
 ServiceID: "9mnpnzenvg8p8tdbtq4wvbkcz"
 Slot: 1
 NodeID: "60gvrl6tm78dmak4yl7srz94v"
 Status:
 Timestamp: "2016-06-07T21:07:31.290032978Z"
 State: "running"
 Message: "started"
 ContainerStatus:
 ContainerID: "e5d62702a1b48d01c3e02ca1e0212a250801fa8d67caca0b6f35919ebc12f035"
 PID: 677
 DesiredState: "running"
 NetworksAttachments:
 \- Network:
 ID: "4qvuz4ko70xaltuqbt8956gd1"
 Version:
 Index: 18
 CreatedAt: "2016-06-07T20:31:11.912919752Z"
 UpdatedAt: "2016-06-07T21:07:29.955277358Z"
 Spec:
 Name: "ingress"
 Labels:
 com.docker.swarm.internal: "true"
 DriverConfiguration: {}
 IPAMOptions:
 Driver: {}
 Configs:
 \- Subnet: "10.255.0.0/16"
 Gateway: "10.255.0.1"
 DriverState:
 Name: "overlay"
 Options:
 com.docker.network.driver.overlay.vxlanid\_list: "256"
 IPAMOptions:
 Driver:
 Name: "default"
 Configs:
 \- Subnet: "10.255.0.0/16"
 Gateway: "10.255.0.1"
 Addresses:
 \- "10.255.0.10/16"
 AssignedGenericResources:

 ServiceSpec:
 description: "User modifiable configuration for a service."
 type: object
 properties:
 Name:
 description: "Name of the service."
 type: "string"
 Labels:
 description: "User-defined key/value metadata."
 type: "object"
 additionalProperties:
 type: "string"
 TaskTemplate:
 $ref: "#/definitions/TaskSpec"
 Mode:
 description: "Scheduling mode for the service."
 type: "object"
 properties:
 Replicated:
 type: "object"
 properties:
 Replicas:
 type: "integer"
 format: "int64"
 Global:
 type: "object"
 UpdateConfig:
 description: "Specification for the update strategy of the service."
 type: "object"
 properties:
 Parallelism:
 description: \|
 Maximum number of tasks to be updated in one iteration (0 means
 unlimited parallelism).
 type: "integer"
 format: "int64"
 Delay:
 description: "Amount of time between updates, in nanoseconds."
 type: "integer"
 format: "int64"
 FailureAction:
 description: \|
 Action to take if an updated task fails to run, or stops running
 during the update.
 type: "string"
 enum:
 \- "continue"
 \- "pause"
 \- "rollback"
 Monitor:
 description: \|
 Amount of time to monitor each updated task for failures, in
 nanoseconds.
 type: "integer"
 format: "int64"
 MaxFailureRatio:
 description: \|
 The fraction of tasks that may fail during an update before the
 failure action is invoked, specified as a floating point number
 between 0 and 1.
 type: "number"
 default: 0
 Order:
 description: \|
 The order of operations when rolling out an updated task. Either
 the old task is shut down before the new task is started, or the
 new task is started before the old task is shut down.
 type: "string"
 enum:
 \- "stop-first"
 \- "start-first"
 RollbackConfig:
 description: "Specification for the rollback strategy of the service."
 type: "object"
 properties:
 Parallelism:
 description: \|
 Maximum number of tasks to be rolled back in one iteration (0 means
 unlimited parallelism).
 type: "integer"
 format: "int64"
 Delay:
 description: \|
 Amount of time between rollback iterations, in nanoseconds.
 type: "integer"
 format: "int64"
 FailureAction:
 description: \|
 Action to take if an rolled back task fails to run, or stops
 running during the rollback.
 type: "string"
 enum:
 \- "continue"
 \- "pause"
 Monitor:
 description: \|
 Amount of time to monitor each rolled back task for failures, in
 nanoseconds.
 type: "integer"
 format: "int64"
 MaxFailureRatio:
 description: \|
 The fraction of tasks that may fail during a rollback before the
 failure action is invoked, specified as a floating point number
 between 0 and 1.
 type: "number"
 default: 0
 Order:
 description: \|
 The order of operations when rolling back a task. Either the old
 task is shut down before the new task is started, or the new task
 is started before the old task is shut down.
 type: "string"
 enum:
 \- "stop-first"
 \- "start-first"
 Networks:
 description: "Specifies which networks the service should attach to."
 type: "array"
 items:
 $ref: "#/definitions/NetworkAttachmentConfig"

 EndpointSpec:
 $ref: "#/definitions/EndpointSpec"

 EndpointPortConfig:
 type: "object"
 properties:
 Name:
 type: "string"
 Protocol:
 type: "string"
 enum:
 \- "tcp"
 \- "udp"
 \- "sctp"
 TargetPort:
 description: "The port inside the container."
 type: "integer"
 PublishedPort:
 description: "The port on the swarm hosts."
 type: "integer"
 PublishMode:
 description: \|
 The mode in which port is published.



 \- "ingress" makes the target port accessible on every node,
 regardless of whether there is a task for the service running on
 that node or not.
 \- "host" bypasses the routing mesh and publish the port directly on
 the swarm node where that service is running.

 type: "string"
 enum:
 \- "ingress"
 \- "host"
 default: "ingress"
 example: "ingress"

 EndpointSpec:
 description: "Properties that can be configured to access and load balance a service."
 type: "object"
 properties:
 Mode:
 description: \|
 The mode of resolution to use for internal load balancing between tasks.
 type: "string"
 enum:
 \- "vip"
 \- "dnsrr"
 default: "vip"
 Ports:
 description: \|
 List of exposed ports that this service is accessible on from the
 outside. Ports can only be provided if \`vip\` resolution mode is used.
 type: "array"
 items:
 $ref: "#/definitions/EndpointPortConfig"

 Service:
 $ref: "#/definitions/ServiceSpec"
 Endpoint:
 type: "object"
 properties:
 Spec:
 $ref: "#/definitions/EndpointSpec"
 Ports:
 type: "array"
 items:
 $ref: "#/definitions/EndpointPortConfig"
 VirtualIPs:
 type: "array"
 items:
 type: "object"
 properties:
 NetworkID:
 type: "string"
 Addr:
 type: "string"
 UpdateStatus:
 description: "The status of a service update."
 type: "object"
 properties:
 State:
 type: "string"
 enum:
 \- "updating"
 \- "paused"
 \- "completed"
 StartedAt:
 type: "string"
 format: "dateTime"
 CompletedAt:
 type: "string"
 format: "dateTime"
 Message:
 type: "string"

 Whether this container has been killed because it ran out of memory.
 type: "boolean"
 example: false
 Dead:
 type: "boolean"
 example: false
 Pid:
 description: "The process ID of this container"
 type: "integer"
 example: 1234
 ExitCode:
 description: "The last exit code of this container"
 type: "integer"
 example: 0
 Error:
 type: "string"
 StartedAt:
 description: "The time when this container was last started."
 type: "string"
 example: "2020-01-06T09:06:59.461876391Z"
 FinishedAt:
 description: "The time when this container last exited."
 type: "string"
 example: "2020-01-06T09:07:59.461876391Z"
 Health:
 $ref: "#/definitions/Health"

 ContainerWaitResponse:
 description: "OK response to ContainerWait operation"
 type: "object"
 x-go-name: "ContainerWaitOKBody"
 title: "ContainerWaitResponse"
 required: \[StatusCode\]
 properties:
 StatusCode:
 description: "Exit code of the container"
 type: "integer"
 format: "int64"
 x-nullable: false
 Error:
 $ref: "#/definitions/ContainerWaitExitError"

 ContainerWaitExitError:
 description: "container waiting error, if any"
 type: "object"
 x-go-name: "ContainerWaitOKBodyError"

 SystemStatus:
 description: \|
 Status information about this node (standalone Swarm API).



 \> \*\*Note\*\*: The information returned in this field is only propagated
 \> by the Swarm standalone API, and is empty (\`null\`) when using
 \> built-in swarm mode.
 type: "array"
 items:
 type: "array"
 items:
 type: "string"
 example:
 \- \["Role", "primary"\]
 \- \["State", "Healthy"\]
 \- \["Strategy", "spread"\]
 \- \["Filters", "health, port, containerslots, dependency, affinity, constraint, whitelist"\]
 \- \["Nodes", "2"\]
 \- \[" swarm-agent-00", "192.168.99.102:2376"\]
 \- \[" └ ID", "5CT6:FBGO:RVGO:CZL4:PB2K:WCYN:2JSV:KSHH:GGFW:QOPG:6J5Q:IOZ2\|192.168.99.102:2376"\]
 \- \[" └ Status", "Healthy"\]
 \- \[" └ Containers", "1 (1 Running, 0 Paused, 0 Stopped)"\]
 \- \[" └ Reserved CPUs", "0 / 1"\]
 \- \[" └ Reserved Memory", "0 B / 1.021 GiB"\]
 \- \[" └ Labels", "kernelversion=4.4.74-boot2docker, operatingsystem=Boot2Docker 17.06.0-ce (TCL 7.2); HEAD : 0672754 - Thu Jun 29 00:06:31 UTC 2017, ostype=linux, provider=virtualbox, storagedriver=aufs"\]
 \- \[" └ UpdatedAt", "2017-08-09T10:03:46Z"\]
 \- \[" └ ServerVersion", "17.06.0-ce"\]
 \- \[" swarm-manager", "192.168.99.101:2376"\]
 \- \[" └ ID", "TAMD:7LL3:SEF7:LW2W:4Q2X:WVFH:RTXX:JSYS:XY2P:JEHL:ZMJK:JGIW\|192.168.99.101:2376"\]
 \- \[" └ Status", "Healthy"\]
 \- \[" └ Containers", "2 (2 Running, 0 Paused, 0 Stopped)"\]
 \- \[" └ Reserved CPUs", "0 / 1"\]
 \- \[" └ Reserved Memory", "0 B / 1.021 GiB"\]
 \- \[" └ Labels", "kernelversion=4.4.74-boot2docker, operatingsystem=Boot2Docker 17.06.0-ce (TCL 7.2); HEAD : 0672754 - Thu Jun 29 00:06:31 UTC 2017, ostype=linux, provider=virtualbox, storagedriver=aufs"\]
 \- \[" └ UpdatedAt", "2017-08-09T10:04:11Z"\]
 \- \[" └ ServerVersion", "17.06.0-ce"\]
 KernelMemory:
 description: "Indicates if the host has kernel memory limit support enabled."
 type: "boolean"
 example: true
 KernelMemoryTCP:
 description: \|
 Indicates if the host has kernel memory TCP limit support enabled.

 example: "17.06.0-ce"
 ClusterStore:
 description: \|
 URL of the distributed storage backend.

 The storage backend is used for multihost networking (to store
 network and endpoint information) and by the node discovery mechanism.



 \> \*\*Note\*\*: This field is only propagated when using standalone Swarm
 \> mode, and overlay networking using an external k/v store. Overlay
 \> networks with Swarm mode enabled use the built-in raft store, and
 \> this field will be empty.
 type: "string"
 example: "consul://consul.corp.example.com:8600/some/path"
 ClusterAdvertise:
 description: \|
 The network endpoint that the Engine advertises for the purpose of
 node discovery. ClusterAdvertise is a \`host:port\` combination on which
 the daemon is reachable by other hosts.



 \> \*\*Note\*\*: This field is only propagated when using standalone Swarm
 \> mode, and overlay networking using an external k/v store. Overlay
 \> networks with Swarm mode enabled use the built-in raft store, and
 \> this field will be empty.
 type: "string"
 example: "node5.corp.example.com:8000"
 Runtimes:
 description: \|
 List of \[OCI compliant\](https://github.com/opencontainers/runtime-spec)
 runtimes configured on the daemon. Keys hold the "name" used to
 reference the runtime.

 The Docker daemon relies on an OCI compliant runtime (invoked via the
 \`containerd\` daemon) as its interface to the Linux kernel namespaces,
 cgroups, and SELinux.

 The default runtime is \`runc\`, and automatically configured. Additional
 runtimes can be configured by the user and will be listed here.
 type: "object"
 additionalProperties:
 $ref: "#/definitions/Runtime"
 default:
 runc:
 path: "runc"
 example:
 runc:
 path: "runc"
 runc-master:
 path: "/go/bin/runc"
 custom:
 path: "/usr/local/bin/my-oci-runtime"
 runtimeArgs: \["--debug", "--systemd-cgroup=false"\]
 DefaultRuntime:
 description: \|
 Name of the default OCI runtime that is used when starting containers.

 The default can be overridden per-container at create time.
 type: "string"
 default: "runc"
 example: "runc"
 Swarm:
 $ref: "#/definitions/SwarmInfo"
 LiveRestoreEnabled:
 description: \|
 Indicates if live restore is enabled.

 If enabled, containers are kept running when the daemon is shutdown
 or upon daemon start if running containers are detected.
 type: "boolean"
 default: false
 example: false
 Isolation:
 description: \|
 Represents the isolation technology to use as a default for containers.
 The supported values are platform-specific.

 If no isolation value is specified on daemon start, on Windows client,
 the default is \`hyperv\`, and on Windows server, the default is \`process\`.

 This option is currently not used on other platforms.
 default: "default"
 type: "string"
 enum:
 \- "default"
 \- "hyperv"
 \- "process"
 \- ""
 InitBinary:
 description: \|
 Name and, optional, path of the \`docker-init\` binary.

 If the path is omitted, the daemon searches the host's \`$PATH\` for the
 binary and uses the first result.
 type: "string"
 example: "docker-init"
 ContainerdCommit:
 $ref: "#/definitions/Commit"
 RuncCommit:
 $ref: "#/definitions/Commit"
 InitCommit:
 $ref: "#/definitions/Commit"
 SecurityOptions:
 description: \|
 List of security features that are enabled on the daemon, such as
 apparmor, seccomp, SELinux, user-namespaces (userns), and rootless.

 Additional configuration options for each security feature may
 be present, and are included as a comma-separated list of key/value
 pairs.
 type: "array"
 items:
 type: "string"
 example:
 \- "name=apparmor"
 \- "name=seccomp,profile=default"
 \- "name=selinux"
 \- "name=userns"
 \- "name=rootless"
 ProductLicense:
 description: \|
 Reports a summary of the product license on the daemon.

 If a commercial license has been applied to the daemon, information
 such as number of nodes, and expiration are included.
 type: "string"
 example: "Community Engine"

 KernelMemory: 0

 required: true
 responses:
 201:
 description: "Container created successfully"
 schema:
 type: "object"
 title: "ContainerCreateResponse"
 description: "OK response to ContainerCreate operation"
 required: \[Id, Warnings\]
 properties:
 Id:
 description: "The ID of the created container"
 type: "string"
 x-nullable: false
 Warnings:
 description: "Warnings encountered when creating the container"
 type: "array"
 x-nullable: false
 items:
 type: "string"
 examples:
 application/json:
 Id: "e90e34656806"
 Warnings: \[\]
 $ref: "#/definitions/GraphDriverData"
 KernelMemory: 0

 \- \`0\`: Modified
 \- \`1\`: Added
 \- \`2\`: Deleted
 type: "object"
 x-go-name: "ContainerChangeResponseItem"
 title: "ContainerChangeResponseItem"
 description: "change item in response to ContainerChanges operation"
 required: \[Path, Kind\]
 properties:
 Path:
 description: "Path to file that has changed"
 type: "string"
 x-nullable: false
 Kind:
 description: "Kind of change"
 type: "integer"
 format: "uint8"
 enum: \[0, 1, 2\]
 x-nullable: false

 KernelMemory: 52428800\
 the stream over the hijacked connected is multiplexed to separate out\
 type: "string"\
 \- \`until=\`: duration relative to daemon's time, during which build cache was not used, in Go's duration format (e.g., '24h')\
 description: "Platform in the format os\[/arch\[/variant\]\]"\
 description: "Default version of docker image builder"\
 Docker-Experimental:\
 type: "boolean"\
 description: "If the server is running with experimental mode enabled"\
 Cache-Control:\
 type: "string"\
 default: "no-cache, no-store, must-revalidate"\
 Pragma:\
 type: "string"\
 default: "no-cache"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 headers:\
 Cache-Control:\
 type: "string"\
 default: "no-cache, no-store, must-revalidate"\
 Pragma:\
 type: "string"\
 default: "no-cache"\
 tags: \["System"\]\
 head:\
 summary: "Ping"\
 description: "This is a dummy endpoint you can use to test if the server is accessible."\
 operationId: "SystemPingHead"\
 produces: \["text/plain"\]\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "string"\
 example: "(empty)"\
 headers:\
 Api-Version:\
 type: "string"\
 description: "Max API Version the server supports"\
 Builder-Version:\
 type: "string"\
 description: "Default version of docker image builder"\
 Docker-Experimental:\
 type: "boolean"\
 description: "If the server is running with experimental mode enabled"\
 Cache-Control:\
 type: "string"\
 default: "no-cache, no-store, must-revalidate"\
 Pragma:\
 type: "string"\
 default: "no-cache"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["System"\]\
 /commit:\
 post:\
 summary: "Create a new image from a container"\
 operationId: "ImageCommit"\
 $ref: "#/definitions/IdResponse"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "containerConfig"\
 in: "body"\
 description: "The container configuration"\
 schema:\
 $ref: "#/definitions/ContainerConfig"\
 \- name: "container"\
 in: "query"\
 description: "The ID or name of the container to commit"\
 type: "string"\
 \- name: "repo"\
 in: "query"\
 description: "Repository name for the created image"\
 type: "string"\
 \- name: "tag"\
 in: "query"\
 description: "Tag name for the create image"\
 type: "string"\
 \- name: "comment"\
 in: "query"\
 description: "Commit message"\
 type: "string"\
 \- name: "author"\
 in: "query"\
 description: "Author of the image (e.g., \`John Hannibal Smith \`)"\
 type: "string"\
 \- name: "pause"\
 in: "query"\
 description: "Whether to pause the container before committing"\
 type: "boolean"\
 default: true\
 \- name: "changes"\
 in: "query"\
 description: "\`Dockerfile\` instructions to apply while committing"\
 type: "string"\
 tags: \["Image"\]\
 /events:\
 get:\
 summary: "Monitor events"\
 description: \|\
 Stream real-time events from the server.\
\
 Various objects within Docker report events when something happens to them.\
\
 Containers report these events: \`attach\`, \`commit\`, \`copy\`, \`create\`, \`destroy\`, \`detach\`, \`die\`, \`exec\_create\`, \`exec\_detach\`, \`exec\_start\`, \`exec\_die\`, \`export\`, \`health\_status\`, \`kill\`, \`oom\`, \`pause\`, \`rename\`, \`resize\`, \`restart\`, \`start\`, \`stop\`, \`top\`, \`unpause\`, and \`update\`\
\
 Images report these events: \`delete\`, \`import\`, \`load\`, \`pull\`, \`push\`, \`save\`, \`tag\`, and \`untag\`\
\
 Volumes report these events: \`create\`, \`mount\`, \`unmount\`, and \`destroy\`\
\
 Networks report these events: \`create\`, \`connect\`, \`disconnect\`, \`destroy\`, \`update\`, and \`remove\`\
\
 The Docker daemon reports these events: \`reload\`\
\
 Services report these events: \`create\`, \`update\`, and \`remove\`\
\
 Nodes report these events: \`create\`, \`update\`, and \`remove\`\
\
 Secrets report these events: \`create\`, \`update\`, and \`remove\`\
\
 Configs report these events: \`create\`, \`update\`, and \`remove\`\
 Parent: ""\
 Parent: "ndlpt0hhvkqcdfkputsk4cq9c"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 DetachKeys:\
 type: "string"\
 description: \|\
 Override the key sequence for detaching a container. Format is\
 a single character \`\[a-Z\]\` or \`ctrl-\` where \`\`\
 is one of: \`a-z\`, \`@\`, \`^\`, \`\[\`, \`,\` or \`\_\`.\
 Tty:\
 type: "boolean"\
 description: "Allocate a pseudo-TTY."\
 Env:\
 description: \|\
 A list of environment variables in the form \`\["VAR=value", ...\]\`.\
 type: "array"\
 items:\
 type: "string"\
 Cmd:\
 type: "array"\
 description: "Command to run, as a string or array of strings."\
 items:\
 type: "string"\
 Privileged:\
 type: "boolean"\
 description: "Runs the exec process with extended privileges."\
 default: false\
 User:\
 type: "string"\
 description: \|\
 The user, and optionally, group to run the exec process inside\
 the container. Format is one of: \`user\`, \`user:group\`, \`uid\`,\
 or \`uid:gid\`.\
 WorkingDir:\
 type: "string"\
 description: \|\
 The working directory for the exec process inside the container.\
 example:\
 AttachStdin: false\
 AttachStdout: true\
 AttachStderr: true\
 DetachKeys: "ctrl-p,ctrl-q"\
 Tty: false\
 Cmd:\
 \- "date"\
 Env:\
 \- "FOO=bar"\
 \- "BAZ=quux"\
 required: true\
 \- name: "id"\
 in: "path"\
 description: "ID or name of container"\
 type: "string"\
 required: true\
 tags: \["Exec"\]\
 /exec/{id}/start:\
 post:\
 summary: "Start an exec instance"\
 description: \|\
 Starts a previously set up exec instance. If detach is true, this endpoint\
 returns immediately after starting the command. Otherwise, it sets up an\
 interactive session with the command.\
 operationId: "ExecStart"\
 consumes:\
 \- "application/json"\
 produces:\
 \- "application/vnd.docker.raw-stream"\
 responses:\
 200:\
 description: "No error"\
 404:\
 description: "No such exec instance"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 409:\
 description: "Container is stopped or paused"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "execStartConfig"\
 in: "body"\
 schema:\
 type: "object"\
 title: "ExecStartConfig"\
 properties:\
 Detach:\
 type: "boolean"\
 description: "Detach from the command."\
 Tty:\
 type: "boolean"\
 description: "Allocate a pseudo-TTY."\
 example:\
 Detach: false\
 Tty: false\
 delete:\
 summary: "Remove a volume"\
 description: "Instruct the driver to remove the volume."\
 operationId: "VolumeDelete"\
 responses:\
 204:\
 description: "The volume was removed"\
 404:\
 description: "No such volume or volume driver"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 409:\
 description: "Volume is in use and cannot be removed"\
 \- name: "force"\
 in: "query"\
 description: "Force the removal of the volume"\
 type: "boolean"\
 default: false\
 tags: \["Volume"\]\
\
 /volumes/prune:\
 post:\
 summary: "Delete unused volumes"\
 produces:\
 \- "application/json"\
 operationId: "VolumePrune"\
 parameters:\
 \- name: "filters"\
 in: "query"\
 description: \|\
 Filters to process on the prune list, encoded as JSON (a \`map\[string\]\[\]string\`).\
\
 Available filters:\
 \- \`label\` (\`label=\`, \`label==\`, \`label!=\`, or \`label!==\`) Prune volumes with (or without, in case \`label!=...\` is used) the specified labels.\
 type: "boolean"\
 Driver:\
 description: "Name of the network driver plugin to use."\
 type: "string"\
 default: "bridge"\
 Internal:\
 description: "Restrict external access to the network."\
 type: "boolean"\
 Attachable:\
 description: \|\
 Globally scoped network is manually attachable by regular\
 containers from workers in swarm mode.\
 type: "boolean"\
 Ingress:\
 description: \|\
 Ingress network is the network which provides the routing-mesh\
 in swarm mode.\
 type: "boolean"\
 IPAM:\
 description: "Optional custom IP scheme for the network."\
 $ref: "#/definitions/IPAM"\
 EnableIPv6:\
 description: "Enable IPv6 on the network."\
 type: "boolean"\
 Options:\
 description: "Network specific options to be used by the drivers."\
 type: "object"\
 additionalProperties:\
 type: "string"\
 Labels:\
 description: "User-defined key/value metadata."\
 type: "object"\
 additionalProperties:\
 type: "string"\
 example:\
 Name: "isolated\_nw"\
 CheckDuplicate: false\
 Driver: "bridge"\
 EnableIPv6: true\
 IPAM:\
 Driver: "default"\
 Config:\
 \- Subnet: "172.20.0.0/16"\
 IPRange: "172.20.10.0/24"\
 Gateway: "172.20.10.11"\
 \- Subnet: "2001:db8:abcd::/64"\
 Gateway: "2001:db8:abcd::1011"\
 Options:\
 foo: "bar"\
 Internal: true\
 Attachable: false\
 Ingress: false\
 Labels:\
 title: "NetworkDisconnectRequest"\
 title: "NetworkConnectRequest"\
 tags: \["Network"\]\
 /networks/prune:\
 post:\
 summary: "Delete unused networks"\
 produces:\
 \- "application/json"\
 operationId: "NetworkPrune"\
 parameters:\
 \- name: "filters"\
 in: "query"\
 description: \|\
 Filters to process on the prune list, encoded as JSON (a \`map\[string\]\[\]string\`).\
\
 Available filters:\
 \- \`until=\` Prune networks created before this timestamp. The \`\` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. \`10m\`, \`1h30m\`) computed relative to the daemon machine’s time.\
 \- \`label\` (\`label=\`, \`label==\`, \`label!=\`, or \`label!==\`) Prune networks with (or without, in case \`label!=...\` is used) the specified labels.\
 type: "string"\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "object"\
 title: "NetworkPruneResponse"\
 properties:\
 NetworksDeleted:\
 description: "Networks that were deleted"\
 type: "array"\
 items:\
 type: "string"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Network"\]\
 /plugins:\
 get:\
 summary: "List plugins"\
 operationId: "PluginList"\
 description: "Returns information about installed plugins."\
 produces: \["application/json"\]\
 responses:\
 200:\
 description: "No error"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/Plugin"\
 type: "string"\
 description: \|\
 A JSON encoded value of the filters (a \`map\[string\]\[\]string\`) to\
 process on the plugin list.\
\
 Available filters:\
\
 \- \`capability=\`\
 \- \`enable=\|\`\
 tags: \["Plugin"\]\
\
 /plugins/privileges:\
 get:\
 summary: "Get plugin privileges"\
 operationId: "GetPluginPrivileges"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/PluginPrivilege"\
 example:\
 \- Name: "network"\
 Description: ""\
 Value:\
 \- "host"\
 \- Name: "mount"\
 Description: ""\
 Value:\
 \- "/data"\
 \- Name: "device"\
 Description: ""\
 Value:\
 \- "/dev/cpu\_dma\_latency"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "remote"\
 in: "query"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 tags:\
 \- "Plugin"\
\
 /plugins/pull:\
 post:\
 summary: "Install a plugin"\
 operationId: "PluginPull"\
 description: \|\
 Pulls and installs a plugin. After the plugin is installed, it can be\
 enabled using the \[\`POST /plugins/{name}/enable\` endpoint\](#operation/PostPluginsEnable).\
 produces:\
 \- "application/json"\
 responses:\
 204:\
 description: "no error"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "remote"\
 in: "query"\
 description: \|\
 Remote reference for plugin to install.\
\
 The \`:latest\` tag is optional, and is used as the default if omitted.\
 required: true\
 type: "string"\
 \- name: "name"\
 in: "query"\
 description: \|\
 Local name for the pulled plugin.\
\
 The \`:latest\` tag is optional, and is used as the default if omitted.\
 required: false\
 type: "string"\
 \- name: "X-Registry-Auth"\
 in: "header"\
 description: \|\
 A base64url-encoded auth configuration to use when pulling a plugin\
 from a registry.\
\
 Refer to the \[authentication section\](#section/Authentication) for\
 details.\
 type: "string"\
 \- name: "body"\
 in: "body"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/PluginPrivilege"\
 example:\
 \- Name: "network"\
 Description: ""\
 Value:\
 \- "host"\
 \- Name: "mount"\
 Description: ""\
 Value:\
 \- "/data"\
 \- Name: "device"\
 Description: ""\
 Value:\
 \- "/dev/cpu\_dma\_latency"\
 tags: \["Plugin"\]\
 /plugins/{name}/json:\
 get:\
 summary: "Inspect a plugin"\
 operationId: "PluginInspect"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Plugin"\
 404:\
 description: "plugin is not installed"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 tags: \["Plugin"\]\
 /plugins/{name}:\
 delete:\
 summary: "Remove a plugin"\
 operationId: "PluginDelete"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Plugin"\
 404:\
 description: "plugin is not installed"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 \- name: "force"\
 in: "query"\
 description: \|\
 Disable the plugin before removing. This may result in issues if the\
 plugin is in use by a container.\
 type: "boolean"\
 default: false\
 tags: \["Plugin"\]\
 /plugins/{name}/enable:\
 post:\
 summary: "Enable a plugin"\
 operationId: "PluginEnable"\
 responses:\
 200:\
 description: "no error"\
 404:\
 description: "plugin is not installed"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 \- name: "timeout"\
 in: "query"\
 description: "Set the HTTP client timeout (in seconds)"\
 type: "integer"\
 default: 0\
 tags: \["Plugin"\]\
 /plugins/{name}/disable:\
 post:\
 summary: "Disable a plugin"\
 operationId: "PluginDisable"\
 responses:\
 200:\
 description: "no error"\
 404:\
 description: "plugin is not installed"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 \- name: "force"\
 in: "query"\
 description: \|\
 Force disable a plugin even if still in use.\
 required: false\
 type: "boolean"\
 tags: \["Plugin"\]\
 /plugins/{name}/upgrade:\
 post:\
 summary: "Upgrade a plugin"\
 operationId: "PluginUpgrade"\
 responses:\
 204:\
 description: "no error"\
 404:\
 description: "plugin not installed"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 \- name: "remote"\
 in: "query"\
 description: \|\
 Remote reference to upgrade to.\
\
 The \`:latest\` tag is optional, and is used as the default if omitted.\
 required: true\
 type: "string"\
 \- name: "X-Registry-Auth"\
 in: "header"\
 description: \|\
 A base64url-encoded auth configuration to use when pulling a plugin\
 from a registry.\
\
 Refer to the \[authentication section\](#section/Authentication) for\
 details.\
 type: "string"\
 \- name: "body"\
 in: "body"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/PluginPrivilege"\
 example:\
 \- Name: "network"\
 Description: ""\
 Value:\
 \- "host"\
 \- Name: "mount"\
 Description: ""\
 Value:\
 \- "/data"\
 \- Name: "device"\
 Description: ""\
 Value:\
 \- "/dev/cpu\_dma\_latency"\
 tags: \["Plugin"\]\
 /plugins/create:\
 post:\
 summary: "Create a plugin"\
 operationId: "PluginCreate"\
 consumes:\
 \- "application/x-tar"\
 responses:\
 204:\
 description: "no error"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "name"\
 in: "query"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 \- name: "tarContext"\
 in: "body"\
 description: "Path to tar containing plugin rootfs and manifest"\
 schema:\
 type: "string"\
 format: "binary"\
 tags: \["Plugin"\]\
 /plugins/{name}/push:\
 post:\
 summary: "Push a plugin"\
 operationId: "PluginPush"\
 description: \|\
 Push a plugin to the registry.\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 responses:\
 200:\
 description: "no error"\
 404:\
 description: "plugin not installed"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Plugin"\]\
 /plugins/{name}/set:\
 post:\
 summary: "Configure a plugin"\
 operationId: "PluginSet"\
 consumes:\
 \- "application/json"\
 parameters:\
 \- name: "name"\
 in: "path"\
 description: \|\
 The name of the plugin. The \`:latest\` tag is optional, and is the\
 default if omitted.\
 required: true\
 type: "string"\
 \- name: "body"\
 in: "body"\
 schema:\
 type: "array"\
 items:\
 type: "string"\
 example: \["DEBUG=1"\]\
 responses:\
 204:\
 description: "No error"\
 404:\
 description: "Plugin not installed"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 500:\
 description: "Server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Plugin"\]\
 /nodes:\
 get:\
 summary: "List nodes"\
 operationId: "NodeList"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/Node"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 503:\
 description: "node is not part of a swarm"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "filters"\
 in: "query"\
 description: \|\
 Filters to process on the nodes list, encoded as JSON (a \`map\[string\]\[\]string\`).\
\
 Available filters:\
 \- \`id=\`\
 \- \`label=\`\
 \- \`membership=\`(\`accepted\`\|\`pending\`)\`\
 \- \`name=\`\
 \- \`node.label=\`\
 \- \`role=\`(\`manager\`\|\`worker\`)\`\
 type: "string"\
 tags: \["Node"\]\
 /nodes/{id}:\
 get:\
 summary: "Inspect a node"\
 operationId: "NodeInspect"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Node"\
 404:\
 description: "no such node"\
 description: "The ID or name of the node"\
 type: "string"\
 required: true\
 tags: \["Node"\]\
 delete:\
 summary: "Delete a node"\
 operationId: "NodeDelete"\
 responses:\
 200:\
 description: "no error"\
 404:\
 description: "no such node"\
 description: "The ID or name of the node"\
 type: "string"\
 required: true\
 \- name: "force"\
 in: "query"\
 description: "Force remove a node from the swarm"\
 default: false\
 type: "boolean"\
 tags: \["Node"\]\
 /nodes/{id}/update:\
 post:\
 summary: "Update a node"\
 operationId: "NodeUpdate"\
 description: "no such node"\
 description: "The ID of the node"\
 type: "string"\
 required: true\
 \- name: "body"\
 in: "body"\
 schema:\
 $ref: "#/definitions/NodeSpec"\
 \- name: "version"\
 in: "query"\
 description: \|\
 The version number of the node object being updated. This is required\
 to avoid conflicting writes.\
 type: "integer"\
 format: "int64"\
 required: true\
 tags: \["Node"\]\
 /swarm:\
 get:\
 summary: "Inspect swarm"\
 operationId: "SwarmInspect"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Swarm"\
 404:\
 description: "no such swarm"\
 tags: \["Swarm"\]\
 /swarm/init:\
 post:\
 summary: "Initialize a new swarm"\
 operationId: "SwarmInit"\
 produces:\
 \- "application/json"\
 \- "text/plain"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 description: "The node ID"\
 type: "string"\
 example: "7v2t30z9blmxuhnyo6s4cpenp"\
 503:\
 description: "node is already part of a swarm"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "body"\
 in: "body"\
 required: true\
 schema:\
 type: "object"\
 title: "SwarmInitRequest"\
 properties:\
 ListenAddr:\
 description: \|\
 Listen address used for inter-manager communication, as well\
 as determining the networking interface used for the VXLAN\
 Tunnel Endpoint (VTEP). This can either be an address/port\
 combination in the form \`192.168.1.1:4567\`, or an interface\
 followed by a port number, like \`eth0:4567\`. If the port number\
 is omitted, the default swarm listening port is used.\
 type: "string"\
 AdvertiseAddr:\
 description: \|\
 Externally reachable address advertised to other nodes. This\
 can either be an address/port combination in the form\
 \`192.168.1.1:4567\`, or an interface followed by a port number,\
 like \`eth0:4567\`. If the port number is omitted, the port\
 number from the listen address is used. If \`AdvertiseAddr\` is\
 not specified, it will be automatically detected when possible.\
 type: "string"\
 DataPathAddr:\
 description: \|\
 Address or interface to use for data path traffic (format:\
 \`\`), for example, \`192.168.1.1\`, or an interface,\
 like \`eth0\`. If \`DataPathAddr\` is unspecified, the same address\
 as \`AdvertiseAddr\` is used.\
\
 The \`DataPathAddr\` specifies the address that global scope\
 network drivers will publish towards other nodes in order to\
 reach the containers running on this node. Using this parameter\
 it is possible to separate the container data traffic from the\
 management traffic of the cluster.\
 type: "string"\
 DataPathPort:\
 description: \|\
 DataPathPort specifies the data path port number for data traffic.\
 Acceptable port range is 1024 to 49151.\
 if no port is set or is set to 0, default port 4789 will be used.\
 type: "integer"\
 format: "uint32"\
 DefaultAddrPool:\
 description: \|\
 Default Address Pool specifies default subnet pools for global\
 scope networks.\
 type: "array"\
 items:\
 type: "string"\
 example: \["10.10.0.0/16", "20.20.0.0/16"\]\
 ForceNewCluster:\
 description: "Force creation of a new swarm."\
 type: "boolean"\
 SubnetSize:\
 description: \|\
 SubnetSize specifies the subnet size of the networks created\
 from the default subnet pool.\
 type: "integer"\
 format: "uint32"\
 Spec:\
 $ref: "#/definitions/SwarmSpec"\
 example:\
 ListenAddr: "0.0.0.0:2377"\
 AdvertiseAddr: "192.168.1.1:2377"\
 DataPathPort: 4789\
 DefaultAddrPool: \["10.10.0.0/8", "20.20.0.0/8"\]\
 SubnetSize: 24\
 ForceNewCluster: false\
 Spec:\
 Orchestration: {}\
 Raft: {}\
 Dispatcher: {}\
 CAConfig: {}\
 EncryptionConfig:\
 AutoLockManagers: false\
 tags: \["Swarm"\]\
 /swarm/join:\
 post:\
 summary: "Join an existing swarm"\
 operationId: "SwarmJoin"\
 responses:\
 200:\
 description: "no error"\
 503:\
 description: "node is already part of a swarm"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "body"\
 in: "body"\
 required: true\
 schema:\
 type: "object"\
 title: "SwarmJoinRequest"\
 properties:\
 ListenAddr:\
 description: \|\
 Listen address used for inter-manager communication if the node\
 gets promoted to manager, as well as determining the networking\
 interface used for the VXLAN Tunnel Endpoint (VTEP).\
 type: "string"\
 AdvertiseAddr:\
 description: \|\
 Externally reachable address advertised to other nodes. This\
 can either be an address/port combination in the form\
 \`192.168.1.1:4567\`, or an interface followed by a port number,\
 like \`eth0:4567\`. If the port number is omitted, the port\
 number from the listen address is used. If \`AdvertiseAddr\` is\
 not specified, it will be automatically detected when possible.\
 type: "string"\
 DataPathAddr:\
 description: \|\
 Address or interface to use for data path traffic (format:\
 \`\`), for example, \`192.168.1.1\`, or an interface,\
 like \`eth0\`. If \`DataPathAddr\` is unspecified, the same address\
 as \`AdvertiseAddr\` is used.\
\
 The \`DataPathAddr\` specifies the address that global scope\
 network drivers will publish towards other nodes in order to\
 reach the containers running on this node. Using this parameter\
 it is possible to separate the container data traffic from the\
 management traffic of the cluster.\
\
 type: "string"\
 RemoteAddrs:\
 description: \|\
 Addresses of manager nodes already participating in the swarm.\
 type: "array"\
 items:\
 type: "string"\
 JoinToken:\
 description: "Secret token for joining this swarm."\
 type: "string"\
 example:\
 ListenAddr: "0.0.0.0:2377"\
 AdvertiseAddr: "192.168.1.1:2377"\
 DataPathAddr: "192.168.1.1"\
 RemoteAddrs:\
 \- "node1:2377"\
 JoinToken: "SWMTKN-1-3pu6hszjas19xyp7ghgosyx9k8atbfcr8p2is99znpy26u2lkl-7p73s1dx5in4tatdymyhg9hu2"\
 tags: \["Swarm"\]\
 /swarm/leave:\
 post:\
 summary: "Leave a swarm"\
 operationId: "SwarmLeave"\
 503:\
 description: "node is not part of a swarm"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 parameters:\
 \- name: "force"\
 description: \|\
 Force leave swarm, even if this is the last manager or that it will\
 break the cluster.\
 in: "query"\
 type: "boolean"\
 default: false\
 tags: \["Swarm"\]\
 /swarm/update:\
 post:\
 summary: "Update a swarm"\
 operationId: "SwarmUpdate"\
 responses:\
 200:\
 description: "no error"\
 400:\
 description: "bad parameter"\
 $ref: "#/definitions/SwarmSpec"\
 \- name: "version"\
 in: "query"\
 description: \|\
 The version number of the swarm object being updated. This is\
 required to avoid conflicting writes.\
 type: "integer"\
 format: "int64"\
 required: true\
 \- name: "rotateWorkerToken"\
 in: "query"\
 description: "Rotate the worker join token."\
 type: "boolean"\
 default: false\
 \- name: "rotateManagerToken"\
 in: "query"\
 description: "Rotate the manager join token."\
 type: "boolean"\
 default: false\
 \- name: "rotateManagerUnlockKey"\
 in: "query"\
 description: "Rotate the manager unlock key."\
 type: "boolean"\
 default: false\
 tags: \["Swarm"\]\
 /swarm/unlockkey:\
 get:\
 summary: "Get the unlock key"\
 operationId: "SwarmUnlockkey"\
 consumes:\
 \- "application/json"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "object"\
 title: "UnlockKeyResponse"\
 properties:\
 UnlockKey:\
 description: "The swarm's unlock key."\
 type: "string"\
 example:\
 UnlockKey: "SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8"\
 500:\
 description: "server error"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 503:\
 description: "node is not part of a swarm"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Swarm"\]\
 /swarm/unlock:\
 post:\
 summary: "Unlock a locked manager"\
 operationId: "SwarmUnlock"\
 consumes:\
 \- "application/json"\
 produces:\
 \- "application/json"\
 parameters:\
 \- name: "body"\
 in: "body"\
 required: true\
 schema:\
 type: "object"\
 title: "SwarmUnlockRequest"\
 properties:\
 UnlockKey:\
 description: "The swarm's unlock key."\
 type: "string"\
 example:\
 UnlockKey: "SWMKEY-1-7c37Cc8654o6p38HnroywCi19pllOnGtbdZEgtKxZu8"\
 503:\
 description: "node is not part of a swarm"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 tags: \["Swarm"\]\
 /services:\
 get:\
 summary: "List services"\
 operationId: "ServiceList"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 type: "array"\
 items:\
 $ref: "#/definitions/Service"\
 process on the services list.\
\
 Available filters:\
\
 \- \`id=\`\
 \- \`label=\`\
 \- \`mode=\["replicated"\|"global"\]\`\
 \- \`name=\`\
 tags: \["Service"\]\
 /services/create:\
 post:\
 summary: "Create a service"\
 operationId: "ServiceCreate"\
 Resources:\
 Limits: {}\
 Reservations: {}\
 RestartPolicy:\
 Condition: "any"\
 MaxAttempts: 0\
 Placement: {}\
 ForceUpdate: 0\
 Mode:\
 Replicated:\
 Replicas: 1\
 Mode: "vip"\
\
 \- name: "version"\
 in: "query"\
 description: \|\
 The version number of the service object being updated. This is\
 required to avoid conflicting writes.\
 This version number should be the value as currently set on the\
 service \*before\* the update. You can find the current version by\
 calling \`GET /services/{id}\`\
 required: true\
 type: "integer"\
 \- name: "registryAuthFrom"\
 in: "query"\
 description: \|\
 If the \`X-Registry-Auth\` header is not specified, this parameter\
 indicates where to find registry authorization credentials.\
 type: "string"\
 enum: \["spec", "previous-spec"\]\
 default: "spec"\
 \- name: "rollback"\
 in: "query"\
 description: \|\
 Set to this parameter to \`previous\` to cause a server-side rollback\
 to the previous service spec. The supplied spec will be ignored in\
 this case.\
 type: "string"\
\
 tags: \["Service"\]\
 /services/{id}/logs:\
 get:\
 summary: "Get service logs"\
 description: \|\
 Get \`stdout\` and \`stderr\` logs from a service. See also\
 \[\`/containers/{id}/logs\`\](#operation/ContainerLogs).\
\
 \*\*Note\*\*: This endpoint works only for services with the \`local\`,\
 \`json-file\` or \`journald\` logging drivers.\
 operationId: "ServiceLogs"\
 description: "no such service"\
 schema:\
 $ref: "#/definitions/ErrorResponse"\
 examples:\
 application/json:\
 message: "No such service: c2ada9df5af8"\
 description: "ID or name of the service"\
 type: "string"\
 \- name: "details"\
 in: "query"\
 description: "Show service context and extra details provided to logs."\
 tags: \["Service"\]\
 /tasks:\
 get:\
 summary: "List tasks"\
 operationId: "TaskList"\
 $ref: "#/definitions/Task"\
 example:\
 \- ID: "0kzzo1i0y4jz6027t0k7aezc7"\
 Version:\
 Index: 71\
 CreatedAt: "2016-06-07T21:07:31.171892745Z"\
 UpdatedAt: "2016-06-07T21:07:31.376370513Z"\
 Spec:\
 ContainerSpec:\
 Image: "redis"\
 Resources:\
 Limits: {}\
 Reservations: {}\
 RestartPolicy:\
 Condition: "any"\
 MaxAttempts: 0\
 Placement: {}\
 ServiceID: "9mnpnzenvg8p8tdbtq4wvbkcz"\
 Slot: 1\
 NodeID: "60gvrl6tm78dmak4yl7srz94v"\
 Status:\
 Timestamp: "2016-06-07T21:07:31.290032978Z"\
 State: "running"\
 Message: "started"\
 ContainerStatus:\
 ContainerID: "e5d62702a1b48d01c3e02ca1e0212a250801fa8d67caca0b6f35919ebc12f035"\
 PID: 677\
 DesiredState: "running"\
 NetworksAttachments:\
 \- Network:\
 ID: "4qvuz4ko70xaltuqbt8956gd1"\
 Version:\
 Index: 18\
 CreatedAt: "2016-06-07T20:31:11.912919752Z"\
 UpdatedAt: "2016-06-07T21:07:29.955277358Z"\
 Spec:\
 Name: "ingress"\
 Labels:\
 com.docker.swarm.internal: "true"\
 DriverConfiguration: {}\
 IPAMOptions:\
 Driver: {}\
 Configs:\
 \- Subnet: "10.255.0.0/16"\
 Gateway: "10.255.0.1"\
 DriverState:\
 Name: "overlay"\
 Options:\
 com.docker.network.driver.overlay.vxlanid\_list: "256"\
 IPAMOptions:\
 Driver:\
 Name: "default"\
 Configs:\
 \- Subnet: "10.255.0.0/16"\
 Gateway: "10.255.0.1"\
 Addresses:\
 \- "10.255.0.10/16"\
 \- ID: "1yljwbmlr8er2waf8orvqpwms"\
 Version:\
 Index: 30\
 CreatedAt: "2016-06-07T21:07:30.019104782Z"\
 UpdatedAt: "2016-06-07T21:07:30.231958098Z"\
 Name: "hopeful\_cori"\
 Spec:\
 ContainerSpec:\
 Image: "redis"\
 Resources:\
 Limits: {}\
 Reservations: {}\
 RestartPolicy:\
 Condition: "any"\
 MaxAttempts: 0\
 Placement: {}\
 ServiceID: "9mnpnzenvg8p8tdbtq4wvbkcz"\
 Slot: 1\
 NodeID: "60gvrl6tm78dmak4yl7srz94v"\
 Status:\
 Timestamp: "2016-06-07T21:07:30.202183143Z"\
 State: "shutdown"\
 Message: "shutdown"\
 ContainerStatus:\
 ContainerID: "1cf8d63d18e79668b0004a4be4c6ee58cddfad2dae29506d8781581d0688a213"\
 DesiredState: "shutdown"\
 NetworksAttachments:\
 \- Network:\
 ID: "4qvuz4ko70xaltuqbt8956gd1"\
 Version:\
 Index: 18\
 CreatedAt: "2016-06-07T20:31:11.912919752Z"\
 UpdatedAt: "2016-06-07T21:07:29.955277358Z"\
 Spec:\
 Name: "ingress"\
 Labels:\
 com.docker.swarm.internal: "true"\
 DriverConfiguration: {}\
 IPAMOptions:\
 Driver: {}\
 Configs:\
 \- Subnet: "10.255.0.0/16"\
 Gateway: "10.255.0.1"\
 DriverState:\
 Name: "overlay"\
 Options:\
 com.docker.network.driver.overlay.vxlanid\_list: "256"\
 IPAMOptions:\
 Driver:\
 Name: "default"\
 Configs:\
 \- Subnet: "10.255.0.0/16"\
 Gateway: "10.255.0.1"\
 Addresses:\
 \- "10.255.0.5/16"\
 process on the tasks list.\
\
 Available filters:\
\
 \- \`desired-state=(running \| shutdown \| accepted)\`\
 \- \`id=\`\
 \- \`label=key\` or \`label="key=value"\`\
 \- \`name=\`\
 \- \`node=\`\
 \- \`service=\`\
 tags: \["Task"\]\
 /tasks/{id}:\
 get:\
 summary: "Inspect a task"\
 operationId: "TaskInspect"\
 produces:\
 \- "application/json"\
 responses:\
 200:\
 description: "no error"\
 schema:\
 $ref: "#/definitions/Task"\
 404:\
 description: "no such task"\
 description: "ID of the task"\
 required: true\
 type: "string"\
 tags: \["Task"\]\
 /tasks/{id}/logs:\
 get:\
 summary: "Get task logs"\
 description: \|\
 Get \`stdout\` and \`stderr\` logs from a task.\
 See also \[\`/containers/{id}/logs\`\](#operation/ContainerLogs).\
\
 \*\*Note\*\*: This endpoint works only for services with the \`local\`,\
 \`json-file\` or \`journald\` logging drivers.\
 operationId: "TaskLogs"\

----
