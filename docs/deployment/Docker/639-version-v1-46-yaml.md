url: https://docs.docker.com/reference/api/engine/version/v1.46.yaml
----

basePath: "/v1.46"
info:
 title: "Docker Engine API"
 version: "1.46"

 If you omit the version-prefix, the current version of the API (v1.46) is used.
 For example, calling \`/info\` is the same as calling \`/v1.46/info\`. Using the

 GraphDriverData:

 $ref: "#/definitions/GraphDriverData"
 RootFS:
 description: \|
 Information about the image's RootFS, including the layer IDs.
 type: "object"
 required: \[Type\]
 properties:
 Type:
 type: "string"
 x-nullable: false
 example: "layers"
 Layers:
 type: "array"
 items:
 type: "string"
 example:
 \- "sha256:1834950e52ce4d5a88a1bbd131c537f4d0e56d10ff0dd69e66be3b7dfa9df7e6"
 \- "sha256:5f70bf18a086007016e948b04aed3b82103a36bea41755b6cddfaf10ace3c6ef"
 Metadata:
 description: \|
 Additional metadata of the image in the local cache. This information
 is local to the daemon, and not part of the image itself.
 type: "object"
 properties:
 LastTagTime:
 description: \|
 Date and time at which the image was last tagged in
 \[RFC 3339\](https://www.ietf.org/rfc/rfc3339.txt) format with nano-seconds.

 This information is only available if the image was tagged locally,
 and omitted otherwise.
 type: "string"
 format: "dateTime"
 example: "2022-02-28T14:40:02.623929178Z"
 x-nullable: true

 ImageSummary:
 type: "object"
 x-go-name: "Summary"

 example: "1.46"
 MinAPIVersion:
 description: \|
 The minimum API version that is supported by the daemon
 type: "string"
 example: "1.24"
 GitCommit:
 description: \|
 The Git commit of the source code that was used to build the daemon
 type: "string"
 example: "48a66213fe"
 GoVersion:
 description: \|
 The version Go used to compile the daemon, and the version of the Go
 runtime in use.
 type: "string"
 example: "go1.21.11"

 description: "Indicates if \`bridge-nf-call-iptables\` is available on the host."

 EnableIPv6: false\
 Internal: false\
 Attachable: false\
 Ingress: false\
 IPAM:\
 Driver: "default"\
 Config:\
 -\
 Subnet: "172.17.0.0/16"\
 \- Name: "none"\
 Id: "e086a3893b05ab69242d3c44e49483a3bbbd3a26b46baa8f61ab797c1088d794"\
 Created: "0001-01-01T00:00:00Z"\
 Scope: "local"\
 Driver: "null"\
 \- Name: "host"\
 Id: "13e871235c677f196c4e1ecebb9dc733b9b2d2ab589e30c539efeda84a24215e"\
 Created: "0001-01-01T00:00:00Z"\
 Scope: "local"\
 Driver: "host"\

----
