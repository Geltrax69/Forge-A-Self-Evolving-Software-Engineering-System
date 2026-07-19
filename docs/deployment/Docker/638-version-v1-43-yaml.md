url: https://docs.docker.com/reference/api/engine/version/v1.43.yaml
----

basePath: "/v1.43"
info:
 title: "Docker Engine API"
 version: "1.43"

 If you omit the version-prefix, the current version of the API (v1.43) is used.
 For example, calling \`/info\` is the same as calling \`/v1.43/info\`. Using the

 \- \`cluster\` a Swarm cluster volume.

 KernelMemoryTCP:
 description: \|
 Hard limit for kernel TCP buffer memory (in bytes). Depending on the
 OCI runtime in use, this option may be ignored. It is no longer supported
 by the default (runc) runtime.

 This field is omitted when empty.
 type: "integer"
 format: "int64"

 the image itself and all of its parent images. Images are now stored
 self-contained, and no longer use a parent-chain, making this field
 an equivalent of the Size field.

 \> \*\*Deprecated\*\*: this field is kept for backward compatibility, but
 \> will be removed in API v1.44.
 type: "integer"
 format: "int64"

 VirtualSize:
 description: \|-
 Total size of the image including all layers it is composed of.

 In versions of Docker before v1.10, this field was calculated from
 the image itself and all of its parent images. Images are now stored
 self-contained, and no longer use a parent-chain, making this field
 an equivalent of the Size field.

 Deprecated: this field is kept for backward compatibility, and will be removed in API v1.44.
 type: "integer"
 format: "int64"
 example: 172064416

 EnableIPv6:
 description: \|
 Whether the network was created with IPv6 enabled.
 type: "boolean"
 example: false
 IPAM:
 $ref: "#/definitions/IPAM"
 Internal:
 description: \|
 Whether the network is created to only allow internal networking
 connectivity.
 type: "boolean"
 default: false
 example: false
 Ingress:
 description: \|
 Whether the network is providing the routing-mesh for the swarm cluster.
 type: "boolean"
 default: false
 example: false
 ConfigFrom:
 $ref: "#/definitions/ConfigReference"
 default: false
 Containers:
 description: \|
 Contains endpoints attached to the network.
 type: "object"
 additionalProperties:
 $ref: "#/definitions/NetworkContainer"
 description: \|
 Network-specific options uses when creating the network.
 type: "object"
 description: "User-defined key/value metadata."
 type: "object"
 items:
 $ref: "#/definitions/PeerInfo"
 x-nullable: true
 # TODO: Add Services (only present when "verbose" is set).

 ConfigReference:
 example: "config\_only\_network\_01"

 IPAM:
 type: "object"

 NetworkContainer:
 type: "object"
 properties:
 Name:
 type: "string"
 example: "container\_1"
 EndpointID:
 type: "string"
 example: "628cadb8bcb92de107b2a1e516cbffe463e321f548feb37697cce00ad694f21a"
 MacAddress:
 type: "string"
 example: "02:42:ac:13:00:02"
 IPv4Address:
 type: "string"
 example: "172.19.0.2/16"
 IPv6Address:
 type: "string"
 example: ""

 PeerInfo:
 description: \|
 PeerInfo represents one peer of an overlay network.
 type: "object"
 properties:
 Name:
 description:
 ID of the peer-node in the Swarm cluster.
 type: "string"
 example: "6869d7c1732b"
 IP:
 description:
 IP-address of the peer-node in the Swarm cluster.
 type: "string"
 example: "10.133.77.91"

 description: "Specifies which networks the service should attach to."

 KernelMemoryTCP:
 description: \|
 Indicates if the host has kernel memory TCP limit support enabled. This
 field is omitted if not supported.

 example: "16.04"

 example: "24.0.2"

 \- name: "platform"
 in: "query"
 description: \|
 Platform in the format \`os\[/arch\[/variant\]\]\` used for image lookup.

 When specified, the daemon checks if the requested image is present
 in the local image cache with the given OS and Architecture, and
 otherwise returns a \`404\` status.

 If the option is not set, the host's native OS and Architecture are
 used to look up the image in the image cache. However, if no platform
 is passed and the given image does exist in the local image cache,
 but its OS or architecture does not match, the container is created
 with the available image, and a warning is added to the \`Warnings\`
 field in the response, for example;

 WARNING: The requested image's platform (linux/arm64/v8) does not
 match the detected host platform (linux/amd64) and no
 specific platform was requested

 type: "string"
 default: ""

 type: "string"\
 \- name: "shared-size"\
 in: "query"\
 description: "Compute and show shared size as a \`SharedSize\` field on each image."\
 type: "boolean"\
 default: false\
 \- \`until=\` remove cache older than \`\`. The \`\` can be Unix timestamps, date formatted timestamps, or Go duration strings (e.g. \`10m\`, \`1h30m\`) computed relative to the daemon's local time.\
 $ref: "#/definitions/IdResponse"\
 Images report these events: \`delete\`, \`import\`, \`load\`, \`pull\`, \`push\`, \`save\`, \`tag\`, \`untag\`, and \`prune\`\
 Parents: \[\]\
 Parents: \["ndlpt0hhvkqcdfkputsk4cq9c"\]\
 Tty:\
 type: "boolean"\
 description: "Allocate a pseudo-TTY."\
 example:\
 Detach: false\
 Tty: true\
 ConsoleSize: \[80, 64\]\
 example: "my\_network"\
 title: "NetworkConnectRequest"\
 title: "NetworkDisconnectRequest"\

----
