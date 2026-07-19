url: https://docs.docker.com/reference/cli/docker/dhi/customization/delete/
----

# docker dhi customization delete

***

| Description | Delete one or more customizations              |
| ----------- | ---------------------------------------------- |
| Usage       | `docker dhi customization delete <id> [id...]` |

## [Description](#description)

Delete one or more Docker Hardened Images customizations by their IDs.

Multiple IDs can be specified as positional arguments.

Examples:

# [Delete a single customization](#delete-a-single-customization)

docker dhi customization delete abc123

# [Delete multiple customizations](#delete-multiple-customizations)

docker dhi customization delete abc123 def456 ghi789

# [Delete without confirmation prompt](#delete-without-confirmation-prompt)

docker dhi customization delete abc123 def456 --force

## [Options](#options)

| Option        | Default | Description                                                   |
| ------------- | ------- | ------------------------------------------------------------- |
| `-f, --force` |         | Skip the confirmation prompt; aborts if any ID does not exist |

----
