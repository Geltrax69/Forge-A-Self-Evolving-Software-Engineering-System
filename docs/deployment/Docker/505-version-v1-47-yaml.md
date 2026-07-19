url: https://docs.docker.com/reference/api/engine/version/v1.47.yaml
----

basePath: "/v1.47"
info:
 title: "Docker Engine API"
 version: "1.47"

 If you omit the version-prefix, the current version of the API (v1.47) is used.
 For example, calling \`/info\` is the same as calling \`/v1.47/info\`. Using the

 DriverData:

 VolumeCreateOptions:
 description: "Volume configuration"
 type: "object"
 title: "VolumeConfig"
 x-go-name: "CreateOptions"

 Id:
 description: \|
 ID that uniquely identifies a network on a single machine.
 type: "string"
 example: "2016-10-19T04:33:30.360899459Z"
 Scope:
 description: \|
 The level at which the network exists (e.g. \`swarm\` for cluster-wide
 or \`local\` for machine level)
 type: "string"
 example: "local"
 Driver:
 description: \|
 The name of the driver used to create the network (e.g. \`bridge\`,
 \`overlay\`).
 type: "string"
 example: "overlay"
 EnableIPv4:
 description: \|
 Whether the network was created with IPv4 enabled.
 type: "boolean"
 example: true

 example: "go1.21.13"

 description: \|
 Indicates if \`bridge-nf-call-iptables\` is available on the host when
 the daemon was started.

 The \`br\_netfilter\`

 Containers:
 description: \|
 The IDs of the containers that are using this image.
 type: "array"
 items:
 type: "string"
 example: \["ede54ee1fda366ab42f824e8a5ffd195155d853ceaec74a927f249ea270c7430", "abadbce344c096744d8d6071a90d474d28af8f1034b5ea9fb03c3f4bfc6d005e"\]
 Size:
 type: "object"
 x-nullable: false
 required: \["Unpacked"\]
 properties:
 Unpacked:
 type: "integer"
 format: "int64"
 example: 3987495
 description: \|
 Unpacked is the size (in bytes) of the locally unpacked
 (uncompressed) image content that's directly usable by the containers
 running this image.
 It's independent of the distributable content - e.g.
 the image might still have an unpacked data that's still used by
 some container even when the distributable/compressed content is
 already gone.
 AttestationData:
 description: \|
 The image data for the attestation manifest.
 This field is only populated when Kind is "attestation".
 type: "object"
 x-nullable: true
 x-omitempty: true
 required: \["For"\]
 properties:
 For:
 description: \|
 The digest of the image manifest that this attestation is for.
 type: "string"
 example: "sha256:95869fbcf224d947ace8d61d0e931d49e31bb7fc67fffbbe9c3198c33aa8e93f"



 required: true
 responses:
 201:
 description: "Container created successfully"
 schema:
 $ref: "#/definitions/ContainerCreateResponse"
 $ref: "#/definitions/DriverData"

 produces:
 \- "application/vnd.docker.raw-stream"
 \- "application/vnd.docker.multiplexed-stream"

 \- \`0\`: Modified ("C")
 \- \`1\`: Added ("A")
 \- \`2\`: Deleted ("D")
 $ref: "#/definitions/FilesystemChange"


 On a cgroup v2 host, the following fields are not set
 \\* \`blkio\_stats\`: all fields other than \`io\_service\_bytes\_recursive\`
 \\* \`cpu\_stats\`: \`cpu\_usage.percpu\_usage\`
 \\* \`memory\_stats\`: \`max\_usage\` and \`failcnt\`
 Also, \`memory\_stats.stats\` fields are incompatible with cgroup v1.

 \- name: "one-shot"
 in: "query"
 description: \|
 Only get a single stat instead of waiting for 2 cycles. Must be used
 with \`stream=false\`.
 type: "boolean"
 default: false
 \- name: "signal"\
 in: "query"\
 description: \|\
 Signal to send to the container as an integer or string (e.g. \`SIGINT\`).\
 type: "string"\
 type: "string"\
 \- name: "signal"\
 in: "query"\
 description: \|\
 Signal to send to the container as an integer or string (e.g. \`SIGINT\`).\
 the HTTP Content-Type header is set to application/vnd.docker.multiplexed-stream\
 and the stream over the hijacked connected is multiplexed to separate out\
 \- "application/vnd.docker.multiplexed-stream"\
 type: "boolean"\
 default: false\
 \- name: "stdin"\
 in: "query"\
 description: "Attach to \`stdin\`"\
 type: "boolean"\
 default: false\
 \- name: "stdout"\
 in: "query"\
 description: "Attach to \`stdout\`"\
 type: "boolean"\
 default: false\
 \- name: "stderr"\
 in: "query"\
 description: "Attach to \`stderr\`"\
 type: "boolean"\
 default: false\
 \- name: "manifests"\
 in: "query"\
 description: "Include \`Manifests\` in the image summary."\
 EnableIPv4:\
 description: \|\
 Enable IPv4 on the network.\
 To disable IPv4, the daemon must be started with experimental features enabled.\
 type: "boolean"\
 example: true\

----
