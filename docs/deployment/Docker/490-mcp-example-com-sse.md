          url: https://mcp.example.com/sse
          transport_type: sse
          headers:
            Authorization: Bearer ${API_TOKEN}

      # Custom shell tools
      - type: script
        tools:
          build:
            cmd: npm run build
            description: Build the project
```

### [Common configuration options](#common-configuration-options)

All toolset types support these optional properties:

| Property      | Type             | Description                                                                                                                                                                                                                         |
| ------------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `instruction` | string           | Additional instructions for using the toolset                                                                                                                                                                                       |
| `tools`       | array            | Specific tool names to enable (defaults to all)                                                                                                                                                                                     |
| `env`         | object           | Environment variables for the toolset                                                                                                                                                                                               |
| `toon`        | string           | Comma-delimited regex patterns matching tool names whose JSON outputs should be compressed. Reduces token usage by simplifying/compressing JSON responses from matched tools using automatic encoding. Example: `"search.*,list.*"` |
| `defer`       | boolean or array | Control which tools load into initial context. Set to `true` to defer all tools, or array of tool names to defer specific tools. Deferred tools don't consume context until explicitly loaded via `search_tool`/`add_tool`.         |

### [Tool selection](#tool-selection)

By default, agents have access to all tools from their configured toolsets. You can restrict this using the `tools` option:

```yaml
toolsets:
  - type: filesystem
    tools: [read_file, write_file, list_directory]
```

This is useful for:

* Limiting agent capabilities for security
* Reducing context size for smaller models
* Creating specialized agents with focused tool access

### [Deferred loading](#deferred-loading)

Deferred loading keeps tools out of the initial context window, loading them only when explicitly requested. This is useful for large toolsets where most tools won't be used, significantly reducing context consumption.

Defer all tools in a toolset:

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    defer: true # All tools load on-demand
```

Or defer specific tools while loading others immediately:

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/path"]
    defer: [search_files, list_directory] # Only these are deferred
```

Agents can discover deferred tools via `search_tool` and load them into context via `add_tool` when needed. Best for toolsets with dozens of tools where only a few are typically used.

### [Output compression](#output-compression)

The `toon` property compresses JSON outputs from matched tools to reduce token usage. When a tool's output is JSON, it's automatically compressed using efficient encoding before being returned to the agent:

```yaml
toolsets:
  - type: mcp
    command: npx
    args: ["-y", "@modelcontextprotocol/server-github"]
    toon: "search.*,list.*" # Compress outputs from search/list tools
```

Useful for tools that return large JSON responses (API results, file listings, search results). The compression is transparent to the agent but can significantly reduce context consumption for verbose tool outputs.

### [Auto-installation of tool binaries](#auto-installation-of-tool-binaries)

MCP and LSP toolsets that require a binary command can be auto-installed if the command isn't on your system. Docker Agent uses the [aqua registry](https://github.com/aquaproj/aqua-registry), a curated index of CLI tool packages, to resolve and download binaries.

When a toolset with a `command` property is loaded, Docker Agent:

1. Checks if the command exists in your `PATH`.
2. Checks the Docker Agent tools directory (`~/.cagent/tools/bin/`).
3. If still not found, looks up the command in the aqua registry and installs it.

Installed binaries are stored under `~/.cagent/tools/`. You can override this location with the `DOCKER_AGENT_TOOLS_DIR` environment variable.

Use the `version` property to pin a specific package and version:

```yaml
toolsets:
  - type: lsp
    command: gopls
    version: "golang/tools@v0.21.0"
    file_types: [".go"]

  - type: mcp
    command: some-mcp-server
    version: "owner/repo@v1.2.3"
```

The format is `owner/repo` or `owner/repo@version`. Without a version tag, Docker Agent uses the latest release. Without the `version` property entirely, Docker Agent tries to auto-detect the package from the command name.

To disable auto-installation for a single toolset, set `version` to `"false"`:

```yaml
toolsets:
  - type: mcp
    command: my-custom-server
    version: "false"
```

To disable auto-installation globally, set the `DOCKER_AGENT_AUTO_INSTALL` environment variable to `false`.

### [Per-agent tool configuration](#per-agent-tool-configuration)

Different agents can have different toolsets:

```yaml
agents:
  coordinator:
    model: anthropic/claude-sonnet-4-5
    sub_agents: [code_writer, code_reviewer]
    toolsets:
      - type: filesystem
        tools: [read_file]

  code_writer:
    model: openai/gpt-5-mini
    toolsets:
      - type: filesystem
      - type: shell

  code_reviewer:
    model: anthropic/claude-sonnet-4-5
    toolsets:
      - type: filesystem
        tools: [read_file, read_multiple_files]
```

This allows specialized agents with focused capabilities, security boundaries, and optimized performance.

## [Built-in tools reference](#built-in-tools-reference)

### [Filesystem](#filesystem)

The `filesystem` toolset gives your agent the ability to work with files and directories. Your agent can read files to understand context, write new files, make targeted edits to existing files, search for content, and explore directory structures. Essential for code analysis, documentation updates, configuration management, and any agent that needs to understand or modify project files.

Access is restricted to the current working directory by default. Agents can request access to additional directories at runtime, which requires your approval.

#### [Configuration](#configuration-1)

```yaml
toolsets:
  - type: filesystem

  # Optional: restrict to specific tools
  - type: filesystem
    tools: [read_file, write_file, edit_file]
```

### [LSP](#lsp)

The `lsp` toolset connects your agent to [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) servers, providing code intelligence like go-to-definition, find references, diagnostics, rename, formatting, and more.

You can configure multiple LSP servers for different programming languages, giving your agent code intelligence across your project.

#### [Configuration](#configuration-2)

```yaml
toolsets:
  - type: lsp
    command: gopls
    file_types: [".go"]

  - type: lsp
    command: typescript-language-server
    args: ["--stdio"]
    file_types: [".ts", ".tsx", ".js", ".jsx"]

  - type: lsp
    command: pylsp
    file_types: [".py"]
```

If an LSP server binary isn't in your PATH, Docker Agent can [auto-install it](#auto-installation-of-tool-binaries) using the `version` property.

#### [Properties](#properties)

| Property     | Type             | Required | Description                                                                                                         |
| ------------ | ---------------- | -------- | ------------------------------------------------------------------------------------------------------------------- |
| `command`    | string           | Yes      | LSP server executable command                                                                                       |
| `args`       | array of strings | No       | Command-line arguments for the LSP server                                                                           |
| `env`        | object           | No       | Environment variables for the LSP server process                                                                    |
| `file_types` | array of strings | No       | File extensions this server handles (e.g., `[".go", ".mod"]`)                                                       |
| `version`    | string           | No       | Package reference for auto-installing the server binary (e.g., `"golang/tools@v0.21.0"`). Set `"false"` to disable. |

#### [Available tools](#available-tools)

| Tool                    | Description                                   | Read-only |
| ----------------------- | --------------------------------------------- | --------- |
| `lsp_workspace`         | Get workspace info and available capabilities | Yes       |
| `lsp_hover`             | Get type info and documentation for a symbol  | Yes       |
| `lsp_definition`        | Find where a symbol is defined                | Yes       |
| `lsp_references`        | Find all references to a symbol               | Yes       |
| `lsp_document_symbols`  | List all symbols in a file                    | Yes       |
| `lsp_workspace_symbols` | Search symbols across the workspace           | Yes       |
| `lsp_diagnostics`       | Get errors and warnings for a file            | Yes       |
| `lsp_code_actions`      | Get available quick fixes and refactorings    | Yes       |
| `lsp_rename`            | Rename a symbol across the workspace          | No        |
| `lsp_format`            | Format a file                                 | No        |
| `lsp_call_hierarchy`    | Find incoming and outgoing calls              | Yes       |
| `lsp_type_hierarchy`    | Find supertypes and subtypes                  | Yes       |
| `lsp_implementations`   | Find interface implementations                | Yes       |
| `lsp_signature_help`    | Get function signature at call site           | Yes       |
| `lsp_inlay_hints`       | Get type annotations and parameter names      | Yes       |

Not all LSP servers support all features. The agent uses `lsp_workspace` to discover the capabilities of each configured server.

#### [Language server examples](#language-server-examples)

The following examples show configurations for common languages:

| Language              | Command                      | `file_types`                     |
| --------------------- | ---------------------------- | -------------------------------- |
| Go                    | `gopls`                      | `[".go"]`                        |
| TypeScript/JavaScript | `typescript-language-server` | `[".ts", ".tsx", ".js", ".jsx"]` |
| Python                | `pylsp`                      | `[".py"]`                        |
| Rust                  | `rust-analyzer`              | `[".rs"]`                        |
| C/C++                 | `clangd`                     | `[".c", ".cpp", ".h", ".hpp"]`   |

For TypeScript/JavaScript, pass `args: ["--stdio"]` to the language server.

### [Shell](#shell)

The `shell` toolset lets your agent execute commands in your system's shell environment. Use this for agents that need to run builds, execute tests, manage processes, interact with CLI tools, or perform system operations. The agent can run commands in the foreground or background.

Commands execute in the current working directory and inherit environment variables from the Docker Agent process. This toolset is powerful but should be used with appropriate security considerations.

#### [Configuration](#configuration-3)

```yaml
toolsets:
  - type: shell
```

### [Think](#think)

The `think` toolset provides your agent with a reasoning scratchpad. The agent can record thoughts and reasoning steps without taking actions or modifying data. Particularly useful for complex tasks where the agent needs to plan multiple steps, verify requirements, or maintain context across a long conversation.

Agents use this to break down problems, list applicable rules, verify they have all needed information, and document their reasoning process before acting.

#### [Configuration](#configuration-4)

```yaml
toolsets:
  - type: think
```

### [Todo](#todo)

The `todo` toolset gives your agent task-tracking capabilities for managing multi-step operations. Your agent can break down complex work into discrete tasks, track progress through each step, and ensure nothing is missed before completing a request. Especially valuable for agents handling complex workflows with multiple dependencies.

The `shared` option allows todos to persist across different agents in a multi-agent system, enabling coordination.

#### [Configuration](#configuration-5)

```yaml
toolsets:
  - type: todo

  # Optional: share todos across agents
  - type: todo
    shared: true
```

### [Tasks](#tasks)

The `tasks` toolset is an advanced version of the `todo` toolset, and provides task management with priorities, dependencies, and persistence. Your agent can create tasks with different priority levels, establish prerequisite relationships between tasks, and automatically track which tasks are blocked by incomplete dependencies. Tasks are sorted by priority and blocking status, making it easy to identify the next actionable work.

Tasks are stored in a JSON file and persist across Docker Agent sessions.

#### [Configuration](#configuration-6)

```yaml
toolsets:
  - type: tasks

  # Optional: specify storage location
  - type: tasks
    path: ./project-tasks.json
```

#### [Available tools](#available-tools-1)

The tasks toolset provides these tools:

* **create\_task**: Create a new task with title, description, priority, and dependencies
* **get\_task**: Retrieve full details of a task by ID, including effective status
* **update\_task**: Modify task fields (title, description, priority, status, dependencies)
* **delete\_task**: Remove a task and clean up its dependencies
* **list\_tasks**: List all tasks sorted by priority, optionally filtered by status or priority
* **next\_task**: Get the highest-priority actionable task (not blocked or done)
* **add\_dependency**: Add a dependency between tasks (with cycle detection)
* **remove\_dependency**: Remove a dependency from a task

#### [Task statuses and priorities](#task-statuses-and-priorities)

Tasks have four statuses: `pending`, `in_progress`, `done`, and `blocked`. The agent automatically calculates the effective status. A task becomes `blocked` if any of its dependencies are not `done`, regardless of its assigned status.

Priority levels (from highest to lowest): `critical`, `high`, `medium` (default), `low`. Tasks are sorted by blocking status first (unblocked tasks first), then by priority, then by creation time.

### [Memory](#memory)

The `memory` toolset allows your agent to store and retrieve information across conversations and sessions. Your agent can remember user preferences, project context, previous decisions, and other information that should persist. Useful for agents that interact with users over time or need to maintain state about a project or environment.

Memories are stored in a local database file and persist across Docker Agent sessions.

#### [Configuration](#configuration-7)

```yaml
toolsets:
  - type: memory

  # Optional: specify database location
  - type: memory
    path: ./agent-memories.db
```

### [Fetch](#fetch)

The `fetch` toolset enables your agent to retrieve content from HTTP/HTTPS URLs. Your agent can fetch documentation, API responses, web pages, or any content accessible via HTTP GET requests. Useful for agents that need to access external resources, check API documentation, or retrieve web content.

The agent can specify custom HTTP headers when needed for authentication or other purposes.

#### [Configuration](#configuration-8)

```yaml
toolsets:
  - type: fetch
```

### [User Prompt](#user-prompt)

The `user_prompt` toolset lets your agent ask you questions during task execution. When the agent needs clarification, decisions, or additional information it can't determine on its own, it displays a dialog and waits for your response.

You'll see a prompt with the agent's question. Depending on what the agent needs, you might provide free-form text, select from options, or fill out a form with multiple fields. You can accept and provide the information, decline to answer, or cancel the operation entirely.

#### [Configuration](#configuration-9)

```yaml
toolsets:
  - type: user_prompt
```

No additional configuration is required. The tool becomes available to the agent once configured. When the agent calls this tool, the user sees a dialog with the prompt. The user can:

* **Accept**: Provide the requested information
* **Decline**: Refuse to provide the information
* **Cancel**: Cancel the operation

### [API](#api)

The `api` toolset lets you define custom tools that call HTTP APIs. Similar to `script` but for web services, this allows you to expose REST APIs, webhooks, or any HTTP endpoint as a tool your agent can use. The agent sees these as typed tools with automatic parameter validation.

Use this to integrate with external services, call internal APIs, trigger webhooks, or interact with any HTTP-based system.

#### [Configuration](#configuration-10)

Each API tool is defined with an `api_config` containing the endpoint, HTTP method, and optional typed parameters:

```yaml
toolsets:
  - type: api
    api_config:
      name: search_docs
      endpoint: https://api.example.com/search
      method: GET
      instruction: Search the documentation database
      headers:
        Authorization: Bearer ${API_TOKEN}
      args:
        query:
          type: string
          description: Search query
        limit:
          type: number
          description: Maximum results
      required: [query]

  - type: api
    api_config:
      name: create_ticket
      endpoint: https://api.example.com/tickets
      method: POST
      instruction: Create a support ticket
      args:
        title:
          type: string
          description: Ticket title
        description:
          type: string
          description: Ticket description
      required: [title, description]
```

For GET requests, parameters are interpolated into the endpoint URL. For POST requests, parameters are sent as JSON in the request body.

Supported argument types: `string`, `number`, `boolean`, `array`, `object`.

### [Script](#script)

The `script` toolset lets you define custom tools by wrapping shell commands with typed parameters. This allows you to expose domain-specific operations to your agent as first-class tools. The agent sees these custom tools just like built-in tools, with parameter validation and type checking handled automatically.

Use this to create tools for deployment scripts, build commands, test runners, or any operation specific to your project or workflow.

#### [Configuration](#configuration-11)

Each custom tool is defined with a command, description, and optional typed parameters:

```yaml
toolsets:
  - type: script
    tools:
      deploy:
        cmd: ./deploy.sh
        description: Deploy the application to an environment
        args:
          environment:
            type: string
            description: Target environment (dev, staging, prod)
          version:
            type: string
            description: Version to deploy
        required: [environment]

      run_tests:
        cmd: npm test
        description: Run the test suite
        args:
          filter:
            type: string
            description: Test name filter pattern
```

Supported argument types: `string`, `number`, `boolean`, `array`, `object`.

#### [Tools](#tools)

The tools you define become available to your agent. In the previous example, the agent would have access to `deploy` and `run_tests` tools.

## [Automatic tools](#automatic-tools)

Some tools are automatically added to agents based on their configuration. You don't configure these explicitly—they appear when needed.

### [transfer\_task](#transfer_task)

Automatically available when your agent has `sub_agents` configured. Allows the agent to delegate tasks to sub-agents and receive results back.

### [handoff](#handoff)

Automatically available when your agent has `handoffs` configured. Allows the agent to transfer the entire conversation to a different agent.

## [What's next](#whats-next)

* Read the [Configuration file reference](https://docs.docker.com/ai/docker-agent/reference/config/) for YAML file structure
* Review the [CLI reference](https://docs.docker.com/ai/docker-agent/reference/cli/) for running agents
* Explore [MCP servers](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/) for extended capabilities
* Browse [example configurations](https://github.com/docker/docker-agent/tree/main/examples)

----
url: https://docs.docker.com/reference/cli/docker/swarm/unlock-key/
----

# docker swarm unlock-key

***

| Description | Manage the unlock key               |
| ----------- | ----------------------------------- |
| Usage       | `docker swarm unlock-key [OPTIONS]` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

An unlock key is a secret key needed to unlock a manager after its Docker daemon restarts. These keys are only used when the autolock feature is enabled for the swarm.

You can view or rotate the unlock key using `swarm unlock-key`. To view the key, run the `docker swarm unlock-key` command without any arguments:

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                  | Default | Description        |
| ----------------------- | ------- | ------------------ |
| [`-q, --quiet`](#quiet) |         | Only display token |
| [`--rotate`](#rotate)   |         | Rotate unlock key  |

## [Examples](#examples)

```console
$ docker swarm unlock-key

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233...

Remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

Use the `--rotate` flag to rotate the unlock key to a new, randomly-generated key:

```console
$ docker swarm unlock-key --rotate

Successfully rotated manager unlock key.

To unlock a swarm manager after it restarts, run the `docker swarm unlock`
command and provide the following key:

    SWMKEY-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233...

Remember to store this key in a password manager, since without it you
will not be able to restart the manager.
```

The `-q` (or `--quiet`) flag only prints the key:

```console
$ docker swarm unlock-key -q

SWMKEY-1-aabbccdd00112233aabbccdd00112233aabbccdd00112233aa-aabbccdd00112233...
```

### [`--rotate`](#rotate)

This flag rotates the unlock key, replacing it with a new randomly-generated key. The old unlock key will no longer be accepted.

### [`--quiet`](#quiet)

Only print the unlock key, without instructions.

----
url: https://docs.docker.com/offload/about/
----

# About Docker Offload

***

Table of contents

***

Subscription: Docker Offload

Requires: Docker Desktop 4.68 or later

Docker Offload is a fully managed service for building and running containers in the cloud using the Docker tools you already know, including Docker Desktop, the Docker CLI, and Docker Compose. It extends your local development workflow into a scalable, cloud-powered environment, enabling developers to work efficiently even in virtual desktop infrastructure (VDI) environments or systems that don't support nested virtualization.

## [Key features](#key-features)

Docker Offload includes the following capabilities to support modern container workflows:

* Ephemeral cloud runners: Automatically provision and tear down cloud environments for each container session.
* Secure communication: Use encrypted tunnels between Docker Desktop and cloud environments with support for secure secrets and image pulling.
* Port forwarding and bind mounts: Retain a local development experience even when running containers in the cloud.
* VDI-friendly: [Use Docker Desktop](https://docs.docker.com/desktop/setup/vm-vdi/) in virtual desktop environments or systems that don't support nested virtualization.

For more information, see the [Docker Offload product page](https://www.docker.com/products/docker-offload/).

## [How Docker Offload works](#how-docker-offload-works)

Docker Offload replaces the need to build or run containers locally by connecting Docker Desktop to secure, dedicated cloud resources.

### [Running containers with Docker Offload](#running-containers-with-docker-offload)

When you use Docker Offload to build or run containers, Docker Desktop creates a secure SSH tunnel to a Docker daemon running in the cloud. Your containers are started and managed entirely in that remote environment.

Here's what happens:

1. Docker Desktop connects to the cloud and triggers container creation.
2. Docker Offload builds or pulls the required images and starts containers in the cloud.
3. The connection stays open while the containers run and you remain active.
4. When the containers stop running, the environment shuts down and is cleaned up automatically.

This setup avoids the overhead of running containers locally and enables fast, reliable containers even on low-powered machines, including machines that do not support nested virtualization. This makes Docker Offload ideal for developers using environments such as virtual desktops, cloud-hosted development machines, or older hardware.

Despite running remotely, features like bind mounts and port forwarding continue to work seamlessly, providing a local-like experience from within Docker Desktop and the CLI.

### [Cloud resources](#cloud-resources)

Docker Offload uses cloud hosts with 4 vCPUs and 8 GiB of memory. If you have different requirements, [contact Docker](https://www.docker.com/pricing/contact-sales/) to explore options.

### [Session management and idle state](#session-management-and-idle-state)

Docker Offload uses session management and idle state policies to ensure fair use of cloud resources across all users, see [Fair use](#fair-use).

Each user can run one Docker Offload session at a time. When Docker Desktop is in an **Offload idle** state, it waits for activity on the Docker API and only connects to a cloud environment when needed. Once connected, the session moves to an **Offload running** state and stays connected as long as Docker detects activity. Activity includes any Docker API call, a running container, or an active build.

#### [When you'll see a prompt](#when-youll-see-a-prompt)

While Docker Offload is running, Docker Desktop shows prompts in the Dashboard to check if you're still active. Prompts appear in two cases:

1. No activity is detected for more than 3 minutes.
2. The session has been running for a long time.

When a prompt appears, you can:

* Select **Ask me again later** to confirm you're still active and continue your session.
* Select **Idle now** to return to an idle state immediately.
* Do nothing, and the session returns to an idle state automatically.

#### [What happens when your session goes idle](#what-happens-when-your-session-goes-idle)

After your session returns to an idle state, there is a 5-minute grace period. You can resume the session during this time by running any Docker command.

> Important
>
> If the idle period exceeds 5 minutes without activity, the session is terminated. Docker Offload environments are ephemeral, so the remote environment and any containers, images, or volumes in it are deleted. To keep work between sessions, push images to a registry such as [Docker Hub](/docker-hub/) before your session ends.

#### [Long session prompts](#long-session-prompts)

Long session prompts appear every 3 hours during a session. After 8 hours of cumulative usage in a day, prompts appear every hour. The 8-hour counter resets at the start of each day.

## [Fair use](#fair-use)

Docker Offload enforces a fair use policy to prevent resource abuse. Fair use is defined as up to 8 compute hours per named user per day, totaled across all user sessions. Usage in excess of this threshold may be subject to session management at Docker's discretion.

## [What's next](#whats-next)

Get hands-on with Docker Offload by following the [Docker Offload quickstart](/offload/quickstart/).

----
url: https://docs.docker.com/guides/php/run-tests/
----

# Run PHP tests in a container

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize a PHP application](https://docs.docker.com/guides/php/containerize/).

## [Overview](#overview)

Testing is an essential part of modern software development. Testing can mean a lot of things to different development teams. There are unit tests, integration tests and end-to-end testing. In this guide you take a look at running your unit tests in Docker when developing and when building.

## [Run tests when developing locally](#run-tests-when-developing-locally)

The sample application already has a PHPUnit test inside the `tests` directory. When developing locally, you can use Compose to run your tests.

Run the following command in the `docker-php-sample` directory to run the tests inside a container.

```console
$ docker compose run --build --rm server ./vendor/bin/phpunit tests/HelloWorldTest.php
```

You should see output that contains the following.

```console
Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.

.                                                                   1 / 1 (100%)

Time: 00:00.003, Memory: 4.00 MB

OK (1 test, 1 assertion)
```

To learn more about the command, see [docker compose run](/reference/cli/docker/compose/run/).

## [Run tests when building](#run-tests-when-building)

To run your tests when building, you need to update your Dockerfile. Create a new test stage that runs the tests.

The following is the updated Dockerfile.

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

FROM development as test
WORKDIR /var/www/html
RUN ./vendor/bin/phpunit tests/HelloWorldTest.php

FROM base as final
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"
COPY --from=prod-deps app/vendor/ /var/www/html/vendor
USER www-data
```

Run the following command to build an image using the test stage as the target and view the test results. Include `--progress plain` to view the build output, `--no-cache` to ensure the tests always run, and `--target test` to target the test stage.

```console
$ docker build -t php-docker-image-test --progress plain --no-cache --target test .
```

You should see output containing the following.

```console
#18 [test 2/2] RUN ./vendor/bin/phpunit tests/HelloWorldTest.php
#18 0.385 Hello, Docker!PHPUnit 9.6.13 by Sebastian Bergmann and contributors.
#18 0.392
#18 0.394 .                                                                   1 / 1 (100%)
#18 0.395
#18 0.395 Time: 00:00.003, Memory: 4.00 MB
#18 0.395
#18 0.395 OK (1 test, 1 assertion)
```

## [Summary](#summary)

In this section, you learned how to run tests when developing locally using Compose and how to run tests when building your image.

Related information:

* [docker compose run](/reference/cli/docker/compose/run/)

## [Next steps](#next-steps)

Next, you’ll learn how to set up a CI/CD pipeline using GitHub Actions.

[Configure CI/CD for your PHP application »](https://docs.docker.com/guides/php/configure-ci-cd/)

----
url: https://docs.docker.com/reference/cli/docker/container/rename/
----

# docker container rename

***

| Description                                                               | Rename a container                           |
| ------------------------------------------------------------------------- | -------------------------------------------- |
| Usage                                                                     | `docker container rename CONTAINER NEW_NAME` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker rename`                              |

## [Description](#description)

The `docker rename` command renames a container.

## [Examples](#examples)

```console
$ docker rename my_container my_new_container
```

----
url: https://docs.docker.com/reference/build-checks/invalid-definition-description/
----

# InvalidDefinitionDescription

***

Table of contents

***

> Note
>
> This check is experimental and is not enabled by default. To enable it, see [Experimental checks](https://docs.docker.com/go/build-checks-experimental/).

## [Output](#output)

```text
Comment for build stage or argument should follow the format: `# <arg/stage name> <description>`. If this is not intended to be a description comment, add an empty line or comment between the instruction and the comment.
```

## [Description](#description)

The [`--call=outline`](https://docs.docker.com/reference/cli/docker/buildx/build/#call-outline) and [`--call=targets`](https://docs.docker.com/reference/cli/docker/buildx/build/#call-outline) flags for the `docker build` command print descriptions for build targets and arguments. The descriptions are generated from [Dockerfile comments](https://docs.docker.com/reference/cli/docker/buildx/build/#descriptions) that immediately precede the `FROM` or `ARG` instruction and that begin with the name of the build stage or argument. For example:

```dockerfile
# build-cli builds the CLI binary
FROM alpine AS build-cli
# VERSION controls the version of the program
ARG VERSION=1
```

In cases where preceding comments are not meant to be descriptions, add an empty line or comment between the instruction and the preceding comment.

## [Examples](#examples)

❌ Bad: A non-descriptive comment on the line preceding the `FROM` command.

```dockerfile
# a non-descriptive comment
FROM scratch AS base

# another non-descriptive comment
ARG VERSION=1
```

✅ Good: An empty line separating non-descriptive comments.

```dockerfile
# a non-descriptive comment

FROM scratch AS base

# another non-descriptive comment

ARG VERSION=1
```

✅ Good: Comments describing `ARG` keys and stages immediately proceeding the command.

```dockerfile
# base is a stage for compiling source
FROM scratch AS base
# VERSION This is the version number.
ARG VERSION=1
```

----
url: https://docs.docker.com/build/policies/intro/
----

# Introduction to build policies

***

Table of contents

***

Build policies let you validate the inputs to your Docker builds before they run. This tutorial walks you through creating your first policy, teaching the Rego basics you need along the way.

## [What you'll learn](#what-youll-learn)

By the end of this tutorial, you'll understand:

* How to create and organize policy files
* Basic Rego syntax and patterns
* How to write policies that validate URLs, checksums, and images
* How policies evaluate during builds

## [Prerequisites](#prerequisites)

* Buildx version 0.31 or later
* Basic familiarity with Dockerfiles and building images

## [How policies work](#how-policies-work)

When you build an image, Buildx resolves all the inputs your Dockerfile references: base images from `FROM` instructions, files from `ADD` or `COPY` or build contexts, and Git repositories. Before running the build, Buildx evaluates your policies against these inputs. If any input violates a policy, the build fails before any instructions execute.

Policies are written in Rego, a declarative language designed for expressing rules and constraints. You don't need to know Rego to get started - this tutorial teaches you what you need.

## [Create your first policy](#create-your-first-policy)

Create a new directory for this tutorial and add a Dockerfile:

```console
$ mkdir policy-tutorial
$ cd policy-tutorial
```

Create a `Dockerfile` that downloads a file with `ADD`:

```dockerfile
FROM scratch
ADD https://example.com/index.html /index.html
```

Now create a policy file. Policies use the `.rego` extension and live alongside your Dockerfile. Create `Dockerfile.rego`:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local
allow if {
  input.http.host == "example.com"
}

decision := {"allow": allow}
```

Save this file as `Dockerfile.rego` in the same directory as your Dockerfile.

Let's break down what this policy does:

* `package docker` - All build policies must start with this package declaration
* `default allow := false` - This example uses a deny-by-default rule: if inputs do not match an `allow` rule, the policy check fails
* `allow if input.local` - The first rule allows any local files (your build context)
* `allow if { input.http.host == "example.com" }` - The second rule allows HTTP downloads from `example.com`
* `decision := {"allow": allow}` - The final decision object tells Buildx whether to allow or deny the input

This policy says: "Only allow local files and HTTP downloads from `example.com`". Rego evaluates all the policy rules to figure out the return value for the `decision` variable, for each build input. The evaluations happen in parallel and on-demand; the order of the policy rules has no significance.

### [About `input.local`](#about-inputlocal)

You'll see `allow if input.local` in nearly every policy. This rule allows local file access, which includes your build context (typically, the `.` directory) and importantly, the Dockerfile itself. Without this rule, Buildx can't read your Dockerfile to start the build.

Even builds that don't reference any files from the build context often need `input.local` because the Dockerfile is a local file. The policy evaluates before the build starts, and denying local access means denying access to the Dockerfile.

In rare cases, you might want stricter local file policies - for example, in CI builds where the build context uses a Git URL as a context directly. In these cases, you may want to deny local sources to prevent untracked files or changes from making their way into your build.

## [Automatic policy loading](#automatic-policy-loading)

Buildx automatically loads policies that match your Dockerfile name. When you build with `Dockerfile`, Buildx looks for `Dockerfile.rego` in the same directory. For a file named `app.Dockerfile`, it looks for `app.Dockerfile.rego`.

This automatic loading means you don't need any command-line flags in most cases - create the policy file and build.

The policy file must be in the same directory as the Dockerfile. If Buildx can't find a matching policy, the build proceeds without policy evaluation (unless you use `--policy strict=true`).

For more control over policy loading, see the [Usage guide](https://docs.docker.com/build/policies/usage/).

## [Run a build with your policy](#run-a-build-with-your-policy)

Build the image with policy evaluation enabled:

```console
$ docker build .
```

The build succeeds because the URL in your Dockerfile matches the policy. Now try changing the URL in your Dockerfile to something else:

```dockerfile
FROM scratch
ADD https://api.github.com/users/octocat /user.json
```

Build again:

```console
$ docker build .
```

This time the build fails with a policy violation. The `api.github.com` hostname doesn't match the rule in your policy, so Buildx rejects it before running any build steps.

## [Debugging policy failures](#debugging-policy-failures)

If your build fails with a policy violation, use `--progress=plain` to see exactly what went wrong:

```console
$ docker buildx build --progress=plain .
```

This shows all policy checks, the input data for each source, and allow/deny decisions. For complete debugging guidance, see [Debugging](https://docs.docker.com/build/policies/debugging/).

## [Add helpful error messages](#add-helpful-error-messages)

When a policy denies an input, users see a generic error message. You can provide custom messages that explain why the build was denied:

Dockerfile.rego

```rego
package docker

default allow := false

allow if input.local
allow if {
  input.http.host == "example.com"
  input.http.schema == "https"
}

deny_msg contains msg if {
  not allow
  input.http
  msg := "only HTTPS downloads from example.com are allowed"
}

decision := {"allow": allow, "deny_msg": deny_msg}
```

Now when a build is denied, users see your custom message explaining what went wrong:

```console
$ docker buildx build .
Policy: only HTTPS downloads from example.com are allowed
ERROR: failed to build: ... source not allowed by policy
```

The `deny_msg` rule uses `contains` to add messages to a set. You can add multiple deny messages for different failure conditions to help users understand exactly what needs to change.

## [Understand Rego rules](#understand-rego-rules)

Rego policies are built from rules. A rule defines when something is allowed. The basic pattern is:

```rego
allow if {
    condition_one
    condition_two
    condition_three
}
```

All conditions must be true for the rule to match. Think of it as an AND operation - the URL must match AND the checksum must match AND any other conditions you specify.

You can have multiple `allow` rules in one policy. If any rule matches, the input is allowed:

```rego
# Allow downloads from example.com
allow if {
    input.http.host == "example.com"
}

# Also allow downloads from api.github.com
allow if {
    input.http.host == "api.github.com"
}
```

This works like OR - the input can match the first rule OR the second rule.

## [Access input fields](#access-input-fields)

The `input` object gives you access to information about build inputs. The structure depends on the input type:

* `input.http` - Files downloaded with `ADD https://...`
* `input.image` - Container images from `FROM` or `COPY --from`
* `input.git` - Git repositories from `ADD git://...` or build context
* `input.local` - Local file context

Refer to the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available input fields.

For HTTP downloads, you can access:

| Key                 | Description                        | Example                          |
| ------------------- | ---------------------------------- | -------------------------------- |
| `input.http.url`    | The full URL                       | `https://example.com/index.html` |
| `input.http.schema` | The protocol (HTTP/HTTPS)          | `https`                          |
| `input.http.host`   | The hostname                       | `example.com`                    |
| `input.http.path`   | The URL path, including parameters | `/index.html`                    |

Update your policy to require HTTPS:

```rego
package docker

default allow := false

allow if {
    input.http.host == "example.com"
    input.http.schema == "https"
}

decision := {"allow": allow}
```

Now the policy requires both the hostname to be `example.com` and the protocol to be HTTPS. HTTP URLs (without TLS) would fail the policy check.

## [Pattern matching and strings](#pattern-matching-and-strings)

Rego provides [built-in functions](https://www.openpolicyagent.org/docs/policy-language#built-in-functions) for pattern matching. Use `startswith()` to match URL prefixes:

```rego
allow if {
    startswith(input.http.url, "https://example.com/")
}
```

This allows any URL that starts with `https://example.com/`.

Use `regex.match()` for complex patterns:

```rego
allow if {
    regex.match(`^https://example\.com/.+\.json$`, input.http.url)
}
```

This matches URLs that:

* Start with `https://example.com/`
* End with `.json`
* Have at least one character between the domain and extension

## [Policy file location](#policy-file-location)

Policy files live adjacent to the Dockerfile they validate, using the naming pattern `<dockerfile-name>.rego`:

```text
project/
├── Dockerfile           # Main Dockerfile
├── Dockerfile.rego      # Policy for Dockerfile
├── lint.Dockerfile      # Linting Dockerfile
└── lint.Dockerfile.rego # Policy for lint.Dockerfile
```

When you build, Buildx automatically loads the corresponding policy file:

```console
$ docker buildx build -f Dockerfile .        # Loads Dockerfile.rego
$ docker buildx build -f lint.Dockerfile .   # Loads lint.Dockerfile.rego
```

## [Next steps](#next-steps)

You now understand how to write basic build policies for HTTP resources. To continue learning:

* Apply and test policies: [Using build policies](https://docs.docker.com/build/policies/usage/)
* Learn [Image validation](https://docs.docker.com/build/policies/validate-images/) to validate container images from `FROM` instructions
* Learn [Git validation](https://docs.docker.com/build/policies/validate-git/) to validate Git repositories used in builds
* See [Example policies](https://docs.docker.com/build/policies/examples/) for copy-paste-ready policies covering common scenarios
* Write unit tests for your policies: [Test build policies](https://docs.docker.com/build/policies/testing/)
* Debug policy failures: [Debugging](https://docs.docker.com/build/policies/debugging/)
* Read the [Input reference](https://docs.docker.com/build/policies/inputs/) for all available input fields
* Check the [Built-in functions](https://docs.docker.com/build/policies/built-ins/) for signature verification, attestations, and other security checks

----
url: https://docs.docker.com/ai/docker-agent/reference/cli/
----

# CLI reference

***

Table of contents

***

Command-line interface for running, managing, and deploying AI agents.

For agent configuration file syntax, see the [Configuration file reference](https://docs.docker.com/ai/docker-agent/reference/config/). For toolset capabilities, see the [Toolsets reference](https://docs.docker.com/ai/docker-agent/reference/toolsets/).

## [Synopsis](#synopsis)

```console
$ docker agent [command] [flags]
```

## [Global flags](#global-flags)

Work with all commands:

| Flag            | Type    | Default | Description          |
| --------------- | ------- | ------- | -------------------- |
| `-d`, `--debug` | boolean | false   | Enable debug logging |
| `-o`, `--otel`  | boolean | false   | Enable OpenTelemetry |
| `--log-file`    | string  | -       | Debug log file path  |

Debug logs write to `~/.cagent/cagent.debug.log` by default. Override with `--log-file`.

## [Runtime flags](#runtime-flags)

Work with most commands. Supported commands link to this section.

| Flag                | Type    | Default | Description                          |
| ------------------- | ------- | ------- | ------------------------------------ |
| `--models-gateway`  | string  | -       | Models gateway address               |
| `--env-from-file`   | array   | -       | Load environment variables from file |
| `--code-mode-tools` | boolean | false   | Enable JavaScript tool orchestration |
| `--working-dir`     | string  | -       | Working directory for the session    |

Set `--models-gateway` via `CAGENT_MODELS_GATEWAY` environment variable.

## [Commands](#commands)

### [a2a](#a2a)

Expose agent via the Agent2Agent (A2A) protocol. Allows other A2A-compatible systems to discover and interact with your agent. Auto-selects an available port if not specified.

```console
$ docker agent serve a2a agent-file|registry-ref
```

> Note
>
> A2A support is experimental. Tool calls are handled internally and not exposed as separate ADK events. Some ADK features are not integrated.

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Flags:

| Flag            | Type    | Default | Description       |
| --------------- | ------- | ------- | ----------------- |
| `-a`, `--agent` | string  | root    | Agent name        |
| `--port`        | integer | 0       | Port (0 = random) |

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ docker agent serve a2a ./agent.yaml --port 8080
$ docker agent serve a2a agentcatalog/pirate --port 9000
```

### [acp](#acp)

Start agent as ACP (Agent Client Protocol) server on stdio for editor integration. See [ACP integration](https://docs.docker.com/ai/docker-agent/integrations/acp/) for setup guides.

```console
$ docker agent serve acp agent-file|registry-ref
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

### [alias add](#alias-add)

Create alias for agent.

```console
$ docker agent alias add name target
```

Arguments:

* `name` - Alias name (required)
* `target` - Path to YAML or registry reference (required)

Examples:

```console
$ docker agent alias add dev ./dev-agent.yaml
$ docker agent alias add prod docker.io/user/prod-agent:latest
$ docker agent alias add default ./agent.yaml
```

Setting alias name to "default" lets you run `docker agent run` without arguments.

### [alias list](#alias-list)

List all aliases.

```console
$ docker agent alias list
$ docker agent alias ls
```

### [alias remove](#alias-remove)

Remove alias.

```console
$ docker agent alias remove name
$ docker agent alias rm name
```

Arguments:

* `name` - Alias name (required)

### [api](#api)

HTTP API server.

```console
$ docker agent serve api agent-file|agents-dir
```

Arguments:

* `agent-file|agents-dir` - Path to YAML or directory with agents (required)

Flags:

| Flag                 | Type    | Default    | Description                       |
| -------------------- | ------- | ---------- | --------------------------------- |
| `-l`, `--listen`     | string  | :8080      | Listen address                    |
| `-s`, `--session-db` | string  | session.db | Session database path             |
| `--pull-interval`    | integer | 0          | Auto-pull OCI ref every N minutes |

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ docker agent serve api ./agent.yaml
$ docker agent serve api ./agents/ --listen :9000
$ docker agent serve api docker.io/user/agent --pull-interval 10
```

The `--pull-interval` flag works only with OCI references. Automatically pulls and reloads at the specified interval.

### [build](#build)

Build Docker image for agent.

```console
$ docker agent build agent-file|registry-ref [image-name]
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)
* `image-name` - Docker image name (optional)

Flags:

| Flag         | Type    | Default | Description                |
| ------------ | ------- | ------- | -------------------------- |
| `--dry-run`  | boolean | false   | Print Dockerfile only      |
| `--push`     | boolean | false   | Push image after build     |
| `--no-cache` | boolean | false   | Build without cache        |
| `--pull`     | boolean | false   | Pull all referenced images |

Example:

```console
$ docker agent build ./agent.yaml myagent:latest
$ docker agent build ./agent.yaml --dry-run
```

### [catalog list](#catalog-list)

List catalog agents.

```console
$ docker agent catalog list [org]
```

Arguments:

* `org` - Organization name (optional, default: `agentcatalog`)

Queries Docker Hub for agent repositories.

### [debug config](#debug-config)

Show resolved agent configuration.

```console
$ docker agent debug config agent-file|registry-ref
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

Shows canonical configuration in YAML after all processing and defaults.

### [debug toolsets](#debug-toolsets)

List agent tools.

```console
$ docker agent debug toolsets agent-file|registry-ref
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

Lists all tools for each agent in the configuration.

### [eval](#eval)

Run evaluation tests.

```console
$ docker agent eval agent-file|registry-ref [eval-dir]
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)
* `eval-dir` - Evaluation files directory (optional, default: `./evals`)

Supports [runtime flags](#runtime-flags).

### [exec](#exec)

Single message execution without TUI.

```console
$ docker agent exec agent-file|registry-ref [message|-]
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)
* `message` - Prompt, or `-` for stdin (optional)

Same flags as [run](#run).

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ docker agent exec ./agent.yaml
$ docker agent exec ./agent.yaml "Check for security issues"
$ echo "Instructions" | docker agent exec ./agent.yaml -
```

### [feedback](#feedback)

Submit feedback.

```console
$ docker agent feedback
```

Shows link to submit feedback.

### [mcp](#mcp)

MCP (Model Context Protocol) server on stdio. Exposes agents as tools to MCP clients. See [MCP integration](https://docs.docker.com/ai/docker-agent/integrations/mcp/) for setup guides.

```console
$ docker agent serve mcp agent-file|registry-ref
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (required)

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ docker agent serve mcp ./agent.yaml
$ docker agent serve mcp docker.io/user/agent:latest
```

### [new](#new)

Create agent configuration interactively.

```console
$ docker agent new [message...]
```

Flags:

| Flag               | Type    | Default | Description                     |
| ------------------ | ------- | ------- | ------------------------------- |
| `--model`          | string  | -       | Model as `provider/model`       |
| `--max-iterations` | integer | 0       | Maximum agentic loop iterations |

Supports [runtime flags](#runtime-flags).

Opens interactive TUI to configure and generate agent YAML.

### [pull](#pull)

Pull agent from OCI registry.

```console
$ docker agent share pull registry-ref
```

Arguments:

* `registry-ref` - OCI registry reference (required)

Flags:

| Flag      | Type    | Default | Description                 |
| --------- | ------- | ------- | --------------------------- |
| `--force` | boolean | false   | Pull even if already exists |

Example:

```console
$ docker agent share pull docker.io/user/agent:latest
```

Saves to local YAML file.

### [push](#push)

Push agent to OCI registry.

```console
$ docker agent share push agent-file registry-ref
```

Arguments:

* `agent-file` - Path to local YAML (required)
* `registry-ref` - OCI reference like `docker.io/user/agent:latest` (required)

Example:

```console
$ docker agent share push ./agent.yaml docker.io/myuser/myagent:latest
```

### [run](#run)

Interactive terminal UI for agent sessions.

```console
$ docker agent run [agent-file|registry-ref] [message|-]
```

Arguments:

* `agent-file|registry-ref` - Path to YAML or OCI registry reference (optional)
* `message` - Initial prompt, or `-` for stdin (optional)

Flags:

| Flag            | Type    | Default | Description                  |
| --------------- | ------- | ------- | ---------------------------- |
| `-a`, `--agent` | string  | root    | Agent name                   |
| `--yolo`        | boolean | false   | Auto-approve all tool calls  |
| `--attach`      | string  | -       | Attach image file            |
| `--model`       | array   | -       | Override model (repeatable)  |
| `--dry-run`     | boolean | false   | Initialize without executing |
| `--remote`      | string  | -       | Remote runtime address       |

Supports [runtime flags](#runtime-flags).

Examples:

```console
$ docker agent run ./agent.yaml
$ docker agent run ./agent.yaml "Analyze this codebase"
$ docker agent run ./agent.yaml --agent researcher
$ echo "Instructions" | docker agent run ./agent.yaml -
$ docker agent run
```

Running without arguments uses the default agent or a "default" alias if configured.

Shows interactive TUI in a terminal. Falls back to exec mode otherwise.

#### [Interactive commands](#interactive-commands)

TUI slash commands:

| Command    | Description                      |
| ---------- | -------------------------------- |
| `/exit`    | Exit                             |
| `/reset`   | Clear history                    |
| `/eval`    | Save conversation for evaluation |
| `/compact` | Compact conversation             |
| `/yolo`    | Toggle auto-approval             |

### [version](#version)

Print version information.

```console
$ docker agent version
```

Shows Docker Agent version and commit hash.

## [Environment variables](#environment-variables)

| Variable                       | Description                     |
| ------------------------------ | ------------------------------- |
| `CAGENT_MODELS_GATEWAY`        | Models gateway address          |
| `TELEMETRY_ENABLED`            | Telemetry control (set `false`) |
| `CAGENT_HIDE_TELEMETRY_BANNER` | Hide telemetry banner (set `1`) |
| `OTEL_EXPORTER_OTLP_ENDPOINT`  | OpenTelemetry endpoint          |

## [Model overrides](#model-overrides)

Override models specified in your configuration file using the `--model` flag.

Format: `[agent=]provider/model`

Without an agent name, the model applies to all agents. With an agent name, it applies only to that specific agent.

Apply to all agents:

```console
$ docker agent run ./agent.yaml --model gpt-5
$ docker agent run ./agent.yaml --model anthropic/claude-sonnet-4-5
```

Apply to specific agents only:

```console
$ docker agent run ./agent.yaml --model researcher=gpt-5
$ docker agent run ./agent.yaml --model "agent1=gpt-5,agent2=claude-sonnet-4-5"
```

Providers: `openai`, `anthropic`, `google`, `dmr`

Omit provider for automatic selection based on model name.

----
url: https://docs.docker.com/guides/admin-set-up/
----

# Set up your company for success with Docker

Table of contents

***

Get the most out of Docker by streamlining workflows, standardizing development environments, and ensuring smooth deployments across your company.

**Time to complete** 20 minutes

Docker's tools provide a scalable, secure platform that empowers your developers to create, ship, and run applications faster. As an administrator, you can streamline workflows, standardize development environments, and ensure smooth deployments across your organization.

By configuring Docker products to suit your company's needs, you can optimize performance, simplify user management, and maintain control over resources. This guide helps you set up and configure Docker products to maximize productivity and success for your team while meeting compliance and security policies.

## [Who’s this for?](#whos-this-for)

* Administrators responsible for managing Docker environments within their organization
* IT leaders looking to streamline development and deployment workflows
* Teams aiming to standardize application environments across multiple users
* Organizations seeking to optimize their use of Docker products for greater scalability and efficiency
* Organizations with a [Docker Business subscription](https://www.docker.com/pricing?ref=DocsGuides\&refAction=DocsGuidesCTAClicked)

## [What you’ll learn](#what-youll-learn)

* Why signing into your company's Docker organization provides access to usage data and enhanced functionality
* How to standardize Docker Desktop versions and settings to create a consistent baseline for all users, while allowing flexibility for advanced developers
* Strategies for implementing Docker's security configurations to meet company IT and software development security requirements without hindering developer productivity

## [Features covered](#features-covered)

This guide covers the following Docker features:

* [Organizations](https://docs.docker.com/admin/organization/): The core structure for managing your Docker environment, grouping users, teams, and image repositories. Your organization was created with your subscription and is managed by one or more owners. Users signed into the organization are assigned seats based on the purchased subscription.
* [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/): By default, Docker Desktop doesn't require sign-in. You can configure settings to enforce this and ensure your developers sign in to your Docker organization.
* [SSO](https://docs.docker.com/enterprise/security/single-sign-on/): Without SSO, user management in a Docker organization is manual. Setting up an SSO connection between your identity provider and Docker ensures compliance with your security policy and automates user provisioning. Adding SCIM further automates user provisioning and de-provisioning.
* General and security settings: Configuring key settings ensures smooth onboarding and usage of Docker products within your environment. You can also enable security features based on your company's specific security needs.

## [Who needs to be involved](#who-needs-to-be-involved)

* Docker organization owner: Must be involved in the process and is required for several key steps
* DNS team: Needed during the SSO setup to verify the company domain
* MDM team: Responsible for distributing Docker-specific configuration files to developer machines
* Identity Provider team: Required for configuring the identity provider and establishing the SSO connection during setup
* Development lead: A development lead with knowledge of Docker configurations to help establish a baseline for developer settings
* IT team: An IT representative familiar with company desktop policies to assist with aligning Docker configuration to those policies
* Infosec: A security team member with knowledge of company development security policies to help configure security features
* Docker testers: A small group of developers to test the new settings and configurations before full deployment

## [Tools integration](#tools-integration)

This guide covers integration with:

* Okta
* Entra ID SAML 2.0
* Azure Connect (OIDC)
* MDM solutions like Intune

## [Modules](#modules)

1. [Communication and information gathering](https://docs.docker.com/guides/admin-set-up/comms-and-info-gathering/)

   Gather your company's requirements from key stakeholders and communicate to your developers.

2. [Finalize plans and begin setup](https://docs.docker.com/guides/admin-set-up/finalize-plans-and-setup/)

   Collaborate with your MDM team to distribute configurations and set up SSO and Docker product trials.

3. [Testing](https://docs.docker.com/guides/admin-set-up/testing/)

   Test your Docker setup.

4. [Deploy your Docker setup](https://docs.docker.com/guides/admin-set-up/deploy/)

   Deploy your Docker setup across your company.

----
url: https://docs.docker.com/get-started/workshop/09_image_best/
----

# Image-building best practices

***

Table of contents

***

## [Image layering](#image-layering)

Using the `docker image history` command, you can see the command that was used to create each layer within an image.

1. Use the `docker image history` command to see the layers in the `getting-started` image you created.

   ```console
   $ docker image history getting-started
   ```

   You should get output that looks something like the following.

   ```plaintext
   IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
   a78a40cbf866        18 seconds ago      /bin/sh -c #(nop)  CMD ["node" "src/index.j…    0B                  
   f1d1808565d6        19 seconds ago      /bin/sh -c npm install --omit=dev               85.4MB              
   a2c054d14948        36 seconds ago      /bin/sh -c #(nop) COPY dir:5dc710ad87c789593…   198kB               
   9577ae713121        37 seconds ago      /bin/sh -c #(nop) WORKDIR /app                  0B                  
   b95baba1cfdb        13 days ago         /bin/sh -c #(nop)  CMD ["node"]                 0B                  
   <missing>           13 days ago         /bin/sh -c #(nop)  ENTRYPOINT ["docker-entry…   0B                  
   <missing>           13 days ago         /bin/sh -c #(nop) COPY file:238737301d473041…   116B                
   <missing>           13 days ago         /bin/sh -c apk add --no-cache --virtual .bui…   5.35MB              
   <missing>           13 days ago         /bin/sh -c addgroup -g 1000 node     && addu…   74.3MB              
   <missing>           13 days ago         /bin/sh -c #(nop)  ENV NODE_VERSION=12.14.1     0B                  
   <missing>           13 days ago         /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B                  
   <missing>           13 days ago         /bin/sh -c #(nop) ADD file:e69d441d729412d24…   5.59MB   
   ```

   Each of the lines represents a layer in the image. The display here shows the base at the bottom with the newest layer at the top. Using this, you can also quickly see the size of each layer, helping diagnose large images.

2. You'll notice that several of the lines are truncated. If you add the `--no-trunc` flag, you'll get the full output.

   ```console
   $ docker image history --no-trunc getting-started
   ```

## [Layer caching](#layer-caching)

Now that you've seen the layering in action, there's an important lesson to learn to help decrease build times for your container images. Once a layer changes, all downstream layers have to be recreated as well.

Look at the following Dockerfile you created for the getting started app.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:24-alpine
WORKDIR /app
COPY . .
RUN npm install --omit=dev
CMD ["node", "src/index.js"]
EXPOSE 3000
```

Going back to the image history output, you see that each command in the Dockerfile becomes a new layer in the image. You might remember that when you made a change to the image, the dependencies had to be reinstalled. It doesn't make much sense to ship around the same dependencies every time you build.

To fix it, you need to restructure your Dockerfile to help support the caching of the dependencies. For Node-based applications, those dependencies are defined in the `package.json` file. You can copy only that file in first, install the dependencies, and then copy in everything else. Then, you only recreate the dependencies if there was a change to the `package.json`.

1. Update the Dockerfile to copy in the `package.json` first, install dependencies, and then copy everything else in.

   ```dockerfile
   # syntax=docker/dockerfile:1
   FROM node:24-alpine
   WORKDIR /app
   COPY package.json package-lock.json ./
   RUN npm install --omit=dev
   COPY . .
   CMD ["node", "src/index.js"]
   ```

2. Build a new image using `docker build`.

   ```console
   $ docker build -t getting-started .
   ```

   You should see output like the following.

   ```plaintext
   [+] Building 16.1s (10/10) FINISHED
   => [internal] load build definition from Dockerfile
   => => transferring dockerfile: 175B
   => [internal] load .dockerignore
   => => transferring context: 2B
   => [internal] load metadata for docker.io/library/node:24-alpine
   => [internal] load build context
   => => transferring context: 53.37MB
   => [1/5] FROM docker.io/library/node:24-alpine
   => CACHED [2/5] WORKDIR /app
   => [3/5] COPY package.json package-lock.json ./
   => [4/5] RUN npm install --omit=dev
   => [5/5] COPY . .
   => exporting to image
   => => exporting layers
   => => writing image     sha256:d6f819013566c54c50124ed94d5e66c452325327217f4f04399b45f94e37d25
   => => naming to docker.io/library/getting-started
   ```

3. Now, make a change to the `src/static/index.html` file. For example, change the `<title>` to "The Awesome Todo App".

4. Build the Docker image now using `docker build -t getting-started .` again. This time, your output should look a little different.

   ```plaintext
   [+] Building 1.2s (10/10) FINISHED
   => [internal] load build definition from Dockerfile
   => => transferring dockerfile: 37B
   => [internal] load .dockerignore
   => => transferring context: 2B
   => [internal] load metadata for docker.io/library/node:24-alpine
   => [internal] load build context
   => => transferring context: 450.43kB
   => [1/5] FROM docker.io/library/node:24-alpine
   => CACHED [2/5] WORKDIR /app
   => CACHED [3/5] COPY package.json package-lock.json ./
   => CACHED [4/5] RUN npm install
   => [5/5] COPY . .
   => exporting to image
   => => exporting layers
   => => writing image     sha256:91790c87bcb096a83c2bd4eb512bc8b134c757cda0bdee4038187f98148e2eda
   => => naming to docker.io/library/getting-started
   ```

   First off, you should notice that the build was much faster. And, you'll see that several steps are using previously cached layers. Pushing and pulling this image and updates to it will be much faster as well.

## [Multi-stage builds](#multi-stage-builds)

Multi-stage builds are an incredibly powerful tool to help use multiple stages to create an image. There are several advantages for them:

* Separate build-time dependencies from runtime dependencies
* Reduce overall image size by shipping only what your app needs to run

### [Maven/Tomcat example](#maventomcat-example)

When building Java-based applications, you need a JDK to compile the source code to Java bytecode. However, that JDK isn't needed in production. Also, you might be using tools like Maven or Gradle to help build the app. Those also aren't needed in your final image. Multi-stage builds help.

```dockerfile
# syntax=docker/dockerfile:1
FROM maven AS build
WORKDIR /app
COPY . .
RUN mvn package

FROM tomcat
COPY --from=build /app/target/file.war /usr/local/tomcat/webapps 
```

In this example, you use one stage (called `build`) to perform the actual Java build using Maven. In the second stage (starting at `FROM tomcat`), you copy in files from the `build` stage. The final image is only the last stage being created, which can be overridden using the `--target` flag.

### [React example](#react-example)

When building React applications, you need a Node environment to compile the JS code (typically JSX), SASS stylesheets, and more into static HTML, JS, and CSS. If you aren't doing server-side rendering, you don't even need a Node environment for your production build. You can ship the static resources in a static nginx container.

```dockerfile
# syntax=docker/dockerfile:1
FROM node:24-alpine AS build
WORKDIR /app
COPY package* ./
RUN npm install
COPY public ./public
COPY src ./src
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
```

In the previous Dockerfile example, it uses the `node:24-alpine` image to perform the build (maximizing layer caching) and then copies the output into an nginx container.

> Tips
>
> This React example is for illustration purposes. The getting-started todo app is a `Node.js` backend application, not a React frontend.

## [Summary](#summary)

In this section, you learned a few image building best practices, including layer caching and multi-stage builds.

Related information:

* [Dockerfile reference](/reference/dockerfile/)
* [Dockerfile best practices](https://docs.docker.com/build/building/best-practices/)

## [Next steps](#next-steps)

In the next section, you'll learn about additional resources you can use to continue learning about containers.

[What next](https://docs.docker.com/get-started/workshop/10_what_next/)

----
url: https://docs.docker.com/docker-hub/repos/manage/builds/setup/
----

# Set up automated builds

***

Table of contents

***

> Warning
>
> Docker Hub Automated Builds is a deprecated feature. It will be fully retired on April 1, 2027.

> Note
>
> Automated builds require a Docker Pro, Team, or Business subscription.

## [Configure automated builds](#configure-automated-builds)

You can configure repositories in Docker Hub so that they automatically build an image each time you push new code to your source provider. If you have [automated tests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/) configured, the new image is only pushed when the tests succeed.

1. In [Docker Hub](https://hub.docker.com), go to **My Hub** > **Repositories**, and select a repository to view its details.

2. Select the **Builds** tab.

3. Select either GitHub or Bitbucket to connect where the image's source code is stored.

   > Note
   >
   > You may be redirected to the settings page to [link the code repository service](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/). Otherwise, if you are editing the build settings for an existing automated build, select **Configure automated builds**.

4. Select the **source repository** to build the Docker images from.

   > Note
   >
   > You might need to specify an organization or user from the source code provider. Once you select a user, source code repositories appear in the **Select repository** drop-down list.

5. Optional. Enable [autotests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/#enable-automated-tests-on-a-repository).

6. Review the default **Build Rules**.

   Build rules control what Docker Hub builds into images from the contents of the source code repository, and how the resulting images are tagged within the Docker repository.

   A default build rule is set up for you, which you can edit or delete. This default rule sets builds from the `Branch` in your source code repository called `master` or `main`, and creates a Docker image tagged with `latest`. For more information, see [set up build rules](#set-up-build-rules).

7. Optional. Select the **plus** icon to add and [configure more build rules](#set-up-build-rules).

8. For each branch or tag, enable or disable the **Autobuild** toggle.

   Only branches or tags with autobuild enabled are built, tested, and have the resulting image pushed to the repository. Branches with autobuild disabled are built for test purposes (if enabled at the repository level), but the built Docker image isn't pushed to the repository.

9. For each branch or tag, enable or disable the **Build Caching** toggle.

   [Build caching](https://docs.docker.com/build/building/best-practices/#leverage-build-cache) can save time if you are building a large image frequently or have many dependencies. Leave the build caching disabled to make sure all of your dependencies are resolved at build time, or if you have a large layer that's quicker to build locally.

10. Select **Save** to save the settings, or select **Save and build** to save and run an initial test.

    > Note
    >
    > A webhook is automatically added to your source code repository to notify Docker Hub on every push. Only pushes to branches that are listed as the source for one or more tags, trigger a build.

### [Set up build rules](#set-up-build-rules)

By default when you set up automated builds, a basic build rule is created for you. This default rule watches for changes to the `master` or `main` branch in your source code repository, and builds the `master` or `main` branch into a Docker image tagged with `latest`.

In the **Build Rules** section, enter one or more sources to build.

For each source:

* Select the **Source type** to build either a tag or a branch. This tells the build system what to look for in the source code repository.

* Enter the name of the **Source** branch or tag you want to build.

  The first time you configure automated builds, a default build rule is set up for you. This default set builds from the `Branch` in your source code called `master`, and creates a Docker image tagged with `latest`.

  You can also use a regex to select which source branches or tags to build. To learn more, see [regexes](#regexes-and-automated-builds).

* Enter the tag to apply to Docker images built from this source.

  If you configured a regex to select the source, you can reference the capture groups and use its result as part of the tag. To learn more, see [regexes](#regexes-and-automated-builds).

* Specify the **Dockerfile location** as a path relative to the root of the source code repository. If the Dockerfile is at the repository root, leave this path set to `/`.

> Note
>
> When Docker Hub pulls a branch from a source code repository, it performs a shallow clone - only the tip of the specified branch. Refer to [Advanced options for autobuild and autotest](https://docs.docker.com/docker-hub/repos/manage/builds/advanced/#source-repository-or-branch-clones) for more information.

### [Environment variables for builds](#environment-variables-for-builds)

You can set the values for environment variables used in your build processes when you configure an automated build. Add your build environment variables by selecting the **plus** icon next to the **Build environment variables** section, and then entering a variable name and the value.

When you set variable values from the Docker Hub UI, you can use them by the commands you set in `hooks` files. However, they're stored so that only users who have `admin` access to the Docker Hub repository can see their values. This means you can use them to store access tokens or other information that should remain secret.

> Note
>
> The variables set on the build configuration screen are used during the build processes only and shouldn't get confused with the environment values used by your service, for example to create service links.

## [Advanced automated build options](#advanced-automated-build-options)

At the minimum you need a build rule composed of a source branch, or tag, and a destination Docker tag to set up an automated build. You can also:

* Change where the build looks for the Dockerfile
* Set a path to the files the build should use (the build context)
* Set up multiple static tags or branches to build from
* Use regular expressions (regexes) to dynamically select source code to build and create dynamic tags

All of these options are available from the **Build configuration** screen for each repository. In [Docker Hub](https://hub.docker.com), select **My Hub** > **Repositories**, and select the name of the repository you want to edit. Select the **Builds** tab, and then select **Configure Automated builds**.

### [Tag and branch builds](#tag-and-branch-builds)

You can configure your automated builds so that pushes to specific branches or tags trigger a build.

1. In the **Build Rules** section, select the **plus** icon to add more sources to build.

2. Select the **Source type** to build either a tag or a branch.

   > Note
   >
   > This tells the build system what type of source to look for in the code repository.

3. Enter the name of the **Source** branch or tag you want to build.

   > Note
   >
   > You can enter a name, or use a regex to match which source branch or tag names to build. To learn more, see [regexes](#regexes-and-automated-builds).

4. Enter the tag to apply to Docker images built from this source.

   > Note
   >
   > If you configured a regex to select the source, you can reference the capture groups and use its result as part of the tag. To learn more, see [regexes](#regexes-and-automated-builds).

5. Repeat steps 2 through 4 for each new build rule you set up.

### [Set the build context and Dockerfile location](#set-the-build-context-and-dockerfile-location)

Depending on how you arrange the files in your source code repository, the files required to build your images may not be at the repository root. If that's the case, you can specify a path where the build looks for the files.

The build context is the path to the files needed for the build, relative to the root of the repository. Enter the path to these files in the **Build context** field. Enter `/` to set the build context as the root of the source code repository.

> Note
>
> If you delete the default path `/` from the **Build context** field and leave it blank, the build system uses the path to the Dockerfile as the build context. However, to avoid confusion it's recommended that you specify the complete path.

You can specify the **Dockerfile location** as a path relative to the build context. If the Dockerfile is at the root of the build context path, leave the Dockerfile path set to `/`. If the build context field is blank, set the path to the Dockerfile from the root of the source repository.

### [Regexes and automated builds](#regexes-and-automated-builds)

You can specify a regular expression (regex) so that only matching branches or tags are built. You can also use the results of the regex to create the Docker tag that's applied to the built image.

You can use up to nine regular expression capture groups, or expressions enclosed in parentheses, to select a source to build, and reference these in the **Docker Tag** field using `{\1}` through `{\9}`.

### [Build images with BuildKit](#build-images-with-buildkit)

Autobuilds use the BuildKit build system by default. If you want to use the legacy Docker build system, add the [environment variable](https://docs.docker.com/docker-hub/repos/manage/builds/#environment-variables-for-builds) `DOCKER_BUILDKIT=0`. Refer to the [BuildKit](https://docs.docker.com/build/buildkit/) page for more information on BuildKit.

## [Autobuild for teams](#autobuild-for-teams)

When you create an automated build repository in your own user account, you can start, cancel, and retry builds, and edit and delete your own repositories.

These same actions are also available for team repositories from Docker Hub if you are an owner. If you are a member of a team with `write` permissions you can start, cancel, and retry builds in your team's repositories, but you cannot edit the team repository settings or delete the team repositories. If your user account has `read` permission, or if you're a member of a team with `read` permission, you can view the build configuration including any testing settings.

| Action/Permission    | Read | Write | Admin | Owner |
| -------------------- | ---- | ----- | ----- | ----- |
| view build details   | x    | x     | x     | x     |
| start, cancel, retry |      | x     | x     | x     |
| edit build settings  |      |       | x     | x     |
| delete build         |      |       |       | x     |

### [Service users for team autobuilds](#service-users-for-team-autobuilds)

> Note
>
> Only owners can set up automated builds for teams.

When you set up automated builds for teams, you grant Docker Hub access to your source code repositories using OAuth tied to a specific user account. This means that Docker Hub has access to everything that the linked source provider account can access.

For organizations and teams, it's recommended you create a dedicated service account to grant access to the source provider. This ensures that no builds break as individual users' access permissions change, and that an individual user's personal projects aren't exposed to an entire organization.

This service account should have access to any repositories to be built, and must have administrative access to the source code repositories so it can manage deploy keys. If needed, you can limit this account to only a specific set of repositories required for a specific build.

If you are building repositories with linked private submodules (private dependencies), you also need to add an override `SSH_PRIVATE` environment variable to automated builds associated with the account. For more information, see [Troubleshoot](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/#build-repositories-with-linked-private-submodules)

1. Create a service user account on your source provider, and generate SSH keys for it.

2. Create a "build" team in your organization.

3. Ensure that the new "build" team has access to each repository and submodule you need to build.

   1. On GitHub or Bitbucket, go to the repository's **Settings** page.

   2. Add the new "build" team to the list of approved users.

      * GitHub: Add the team in **Collaborators and Teams**.
      * Bitbucket: Add the team in **Access management**.

4. Add the service user to the "build" team on the source provider.

5. Sign in to Docker Hub as an owner, switch to the organization, and follow the instructions to [link to source code repository](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/) using the service account.

   > Note
   >
   > You may need to sign out of your individual account on the source code provider to create the link to the service account.

6. Optional. Use the SSH keys you generated to set up any builds with private submodules, using the service account and [the previous instructions](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/#build-repositories-with-linked-private-submodules).

## [What's Next?](#whats-next)

* [Customize your build process](https://docs.docker.com/docker-hub/repos/manage/builds/advanced/) with environment variables, hooks, and more
* [Add automated tests](https://docs.docker.com/docker-hub/repos/manage/builds/automated-testing/)
* [Manage your builds](https://docs.docker.com/docker-hub/repos/manage/builds/manage-builds/)
* [Troubleshoot](https://docs.docker.com/docker-hub/repos/manage/builds/troubleshoot/)

----
url: https://docs.docker.com/guides/testcontainers-java-quarkus/run-tests/
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

You should see the PostgreSQL Docker container start and all tests pass. After the tests finish, the container stops and is removed automatically.

## [Run the application locally](#run-the-application-locally)

Quarkus Dev Services automatically provisions unconfigured services in development mode. Start the Quarkus application in dev mode:

```console
$ ./mvnw compile quarkus:dev
```

Or with Gradle:

```console
$ ./gradlew quarkusDev
```

Dev Services starts a PostgreSQL container automatically. If you're running a PostgreSQL database on your system and want to use that instead, configure the datasource properties in `src/main/resources/application.properties`:

```properties
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/postgres
quarkus.datasource.username=postgres
quarkus.datasource.password=postgres
```

When these properties are set explicitly, Dev Services doesn't provision the database container and instead connects to the configured database.

## [Summary](#summary)

Quarkus Dev Services improves the developer experience by automatically provisioning the required services using Testcontainers during development and testing. This guide covered:

* Building a REST API using JAX-RS with Hibernate ORM with Panache
* Testing API endpoints using REST Assured with Dev Services handling database provisioning
* Using `QuarkusTestResourceLifecycleManager` for services not supported by Dev Services
* Running the application locally with Dev Services

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Quarkus Dev Services overview](https://quarkus.io/guides/dev-services)
* [Quarkus testing guide](https://quarkus.io/guides/getting-started-testing)
* [Testcontainers Postgres module](https://java.testcontainers.org/modules/databases/postgres/)

----
url: https://docs.docker.com/build/cache/backends/inline/
----

# Inline cache

***

Table of contents

***

The `inline` cache storage backend is the simplest way to get an external cache and is easy to get started using if you're already building and pushing an image.

The downside of inline cache is that it doesn't scale with multi-stage builds as well as the other drivers do. It also doesn't offer separation between your output artifacts and your cache output. This means that if you're using a particularly complex build flow, or not exporting your images directly to a registry, then you may want to consider the [registry](https://docs.docker.com/build/cache/backends/registry/) cache.

## [Synopsis](#synopsis)

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline \
  --cache-from type=registry,ref=<registry>/<image> .
```

No additional parameters are supported for the `inline` cache.

To export cache using `inline` storage, pass `type=inline` to the `--cache-to` option:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=inline .
```

Alternatively, you can also export inline cache by setting the build argument `BUILDKIT_INLINE_CACHE=1`, instead of using the `--cache-to` flag:

```console
$ docker buildx build --push -t <registry>/<image> \
  --build-arg BUILDKIT_INLINE_CACHE=1 .
```

To import the resulting cache on a future build, pass `type=registry` to `--cache-from` which lets you extract the cache from inside a Docker image in the specified registry:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-from type=registry,ref=<registry>/<image> .
```

## [Further reading](#further-reading)

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `inline` cache backend, see the [BuildKit README](https://github.com/moby/buildkit#inline-push-image-and-cache-together).

----
url: https://docs.docker.com/reference/cli/docker/scout/integration/list/
----

# docker scout integration list

***

| Description | List integrations which can be installed      |
| ----------- | --------------------------------------------- |
| Usage       | `docker scout integration list [INTEGRATION]` |

## [Description](#description)

The docker scout integration list configured integrations for an organization.

## [Options](#options)

| Option   | Default | Description                               |
| -------- | ------- | ----------------------------------------- |
| `--name` |         | Name of integration configuration to list |
| `--org`  |         | Namespace of the Docker organization      |

----
url: https://docs.docker.com/manuals/
----

# Manuals

***

***

This section contains user guides on how to install, set up, configure, and use Docker products.

## [AI and agents](#ai-and-agents)

All the Docker AI tools in one easy-to-access location.

### [Docker Sandboxes](/ai/sandboxes/)

[Run AI coding agents in isolated environments.](/ai/sandboxes/)

### [MCP Catalog and Toolkit](/ai/mcp-catalog-and-toolkit/)

[Augment your AI workflow with MCP servers.](/ai/mcp-catalog-and-toolkit/)

### [Gordon](/ai/gordon/)

[Streamline your workflow and get the most out of the Docker ecosystem with your personal AI assistant.](/ai/gordon/)

### [Docker Model Runner](/ai/model-runner/)

[View and manage your local models.](/ai/model-runner/)

### [Docker Agent](/ai/docker-agent)

[The open-source multi-agent solution to assist you in your tasks.](/ai/docker-agent)

## [Application development](#application-development)

End-to-end developer solutions for innovative teams.

### [Docker Desktop](/desktop/)

[Your command center for container development.](/desktop/)

### [Docker Offload](/offload/)

[Build and run containers in the cloud.](/offload/)

### [Docker Build Cloud](/build-cloud/)

[Build your images faster in the cloud.](/build-cloud/)

### [Testcontainers](/testcontainers/)

[Run containers programmatically in your preferred programming language.](/testcontainers/)

### [Docker Build](/build/)

[Build and ship any application anywhere.](/build/)

### [Docker Engine](/engine/)

[The industry-leading container runtime.](/engine/)

### [Docker Compose](/compose/)

[Define and run multi-container applications.](/compose/)

## [Supply chain security](#supply-chain-security)

Security guardrails and image analysis for your software supply chain.

### [Docker Hub](/docker-hub/)

[Discover, share, and integrate container images.](/docker-hub/)

### [Docker Hardened Images](/dhi/)

[Secure, minimal images for trusted software delivery.](/dhi/)

### [Docker Scout](/scout/)

[Image analysis and policy evaluation.](/scout/)

## [Platform](#platform)

Documentation related to the Docker platform, such as administration and subscription management.

### [Administration](/admin/)

[Centralized observability for companies and organizations.](/admin/)

### [Billing](/billing/)

[Manage billing and payment methods.](/billing/)

### [Accounts](/accounts/)

[Manage your Docker account.](/accounts/)

### [Security](/security/)

[Security guardrails for both administrators and developers.](/security/)

### [Subscription](/subscription/)

[Commercial use licenses for Docker products.](/subscription/)

## [Enterprise](#enterprise)

Targeted at IT administrators with help on deploying Docker Desktop at scale with configuration guidance on security related features.

### [Deploy Docker Desktop](/enterprise/enterprise-deployment/)

[Deploy Docker Desktop at scale within your company](/enterprise/enterprise-deployment/)

----
url: https://docs.docker.com/build/bake/targets/
----

# Bake targets

***

Table of contents

***

A target in a Bake file represents a build invocation. It holds all the information you would normally pass to a `docker build` command using flags.

docker-bake.hcl

```hcl
target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

To build a target with Bake, pass name of the target to the `bake` command.

```console
$ docker buildx bake webapp
```

You can build multiple targets at once by passing multiple target names to the `bake` command.

```console
$ docker buildx bake webapp api tests
```

## [Default target](#default-target)

If you don't specify a target when running `docker buildx bake`, Bake will build the target named `default`.

docker-bake.hcl

```hcl
target "default" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}
```

To build this target, run `docker buildx bake` without any arguments:

```console
$ docker buildx bake
```

## [Target properties](#target-properties)

The properties you can set for a target closely resemble the CLI flags for `docker build`, with a few additional properties that are specific to Bake.

The `dockerfile` property specifies the path to the Dockerfile for a target. If you also set a `context`, the `dockerfile` path resolves relative to that context.

docker-bake.hcl

```hcl
target "default" {
  context = "app"
  # resolves to app/src/www/Dockerfile
  dockerfile = "src/www/Dockerfile"
}
```

For all the properties you can set for a target, see the [Bake reference](/build/bake/reference#target).

## [Grouping targets](#grouping-targets)

You can group targets together using the `group` block. This is useful when you want to build multiple targets at once.

docker-bake.hcl

```hcl
group "all" {
  targets = ["webapp", "api", "tests"]
}

target "webapp" {
  dockerfile = "webapp.Dockerfile"
  tags = ["docker.io/username/webapp:latest"]
  context = "https://github.com/username/webapp"
}

target "api" {
  dockerfile = "api.Dockerfile"
  tags = ["docker.io/username/api:latest"]
  context = "https://github.com/username/api"
}

target "tests" {
  dockerfile = "tests.Dockerfile"
  contexts = {
    webapp = "target:webapp"
    api = "target:api"
  }
  output = ["type=local,dest=build/tests"]
  context = "."
}
```

To build all the targets in a group, pass the name of the group to the `bake` command.

```console
$ docker buildx bake all
```

## [Pattern matching for targets and groups](#pattern-matching-for-targets-and-groups)

Bake supports shell-style wildcard patterns when specifying target or grouped targets. This makes it easier to build multiple targets without listing each one explicitly.

Supported patterns:

* `*` matches any sequence of characters
* `?` matches any single character
* `[abc]` matches any character in brackets

> Note
>
> Always wrap wildcard patterns in quotes. Without quotes, your shell will expand the wildcard to match files in the current directory, causing errors.

Examples:

```console
# Match all targets starting with 'foo-'
$ docker buildx bake "foo-*"

# Match all targets
$ docker buildx bake "*"

# Matches: foo-baz, foo-caz, foo-daz, etc.
$ docker buildx bake "foo-?az"

# Matches: foo-bar, boo-bar
$ docker buildx bake "[fb]oo-bar"

# Matches: mtx-a-b-d, mtx-a-b-e, mtx-a-b-f
$ docker buildx bake "mtx-a-b-*"
```

You can also combine multiple patterns:

```console
$ docker buildx bake "foo*" "tests"
```

## [Additional resources](#additional-resources)

Refer to the following pages to learn more about Bake's features:

* Learn how to use [variables](https://docs.docker.com/build/bake/variables/) in Bake to make your build configuration more flexible.
* Learn how you can use matrices to build multiple images with different configurations in [Matrices](https://docs.docker.com/build/bake/matrices/).
* Head to the [Bake file reference](/build/bake/reference/) to learn about all the properties you can set in a Bake file, and its syntax.

----
url: https://docs.docker.com/guides/testcontainers-java-mockserver/write-tests/
----

# Write tests with Testcontainers MockServer

***

Table of contents

***

Mocking external API interactions at the HTTP protocol level, rather than mocking Java methods, lets you verify marshalling and unmarshalling behavior and simulate network issues.

Testcontainers provides a MockServer module that starts a [MockServer](https://www.mock-server.com/) instance inside a Docker container. You can then use `MockServerClient` to configure mock expectations.

## [Write the test](#write-the-test)

Create `AlbumControllerTest.java`:

```java
package com.testcontainers.demo;

import static io.restassured.RestAssured.given;
import static org.hamcrest.CoreMatchers.is;
import static org.hamcrest.Matchers.hasSize;
import static org.mockserver.model.HttpRequest.request;
import static org.mockserver.model.HttpResponse.response;
import static org.mockserver.model.JsonBody.json;

import io.restassured.RestAssured;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockserver.client.MockServerClient;
import org.mockserver.model.Header;
import org.mockserver.verify.VerificationTimes;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.server.LocalServerPort;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.testcontainers.mockserver.MockServerContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Testcontainers
class AlbumControllerTest {

  @LocalServerPort
  private Integer port;

  @Container
  static MockServerContainer mockServerContainer =
    new MockServerContainer("mockserver/mockserver:5.15.0");

  static MockServerClient mockServerClient;

  @DynamicPropertySource
  static void overrideProperties(DynamicPropertyRegistry registry) {
    mockServerClient =
    new MockServerClient(
      mockServerContainer.getHost(),
      mockServerContainer.getServerPort()
    );
    registry.add("photos.api.base-url", mockServerContainer::getEndpoint);
  }

  @BeforeEach
  void setUp() {
    RestAssured.port = port;
    mockServerClient.reset();
  }

  @Test
  void shouldGetAlbumById() {
    Long albumId = 1L;

    mockServerClient
      .when(
        request().withMethod("GET").withPath("/albums/" + albumId + "/photos")
      )
      .respond(
        response()
          .withStatusCode(200)
          .withHeaders(
            new Header("Content-Type", "application/json; charset=utf-8")
          )
          .withBody(
            json(
              """
              [
                   {
                       "id": 1,
                       "title": "accusamus beatae ad facilis cum similique qui sunt",
                       "url": "https://via.placeholder.com/600/92c952",
                       "thumbnailUrl": "https://via.placeholder.com/150/92c952"
                   },
                   {
                       "id": 2,
                       "title": "reprehenderit est deserunt velit ipsam",
                       "url": "https://via.placeholder.com/600/771796",
                       "thumbnailUrl": "https://via.placeholder.com/150/771796"
                   }
               ]
              """
            )
          )
      );

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(200)
      .body("albumId", is(albumId.intValue()))
      .body("photos", hasSize(2));

    verifyMockServerRequest("GET", "/albums/" + albumId + "/photos", 1);
  }

  @Test
  void shouldReturn404StatusWhenAlbumNotFound() {
    Long albumId = 1L;
    mockServerClient
      .when(
        request().withMethod("GET").withPath("/albums/" + albumId + "/photos")
      )
      .respond(response().withStatusCode(404));

    given()
      .contentType(ContentType.JSON)
      .when()
      .get("/api/albums/{albumId}", albumId)
      .then()
      .statusCode(404);

    verifyMockServerRequest("GET", "/albums/" + albumId + "/photos", 1);
  }

  private void verifyMockServerRequest(String method, String path, int times) {
    mockServerClient.verify(
      request().withMethod(method).withPath(path),
      VerificationTimes.exactly(times)
    );
  }
}
```

Here's what the test does:

* `@SpringBootTest` starts the full application on a random port.
* The `@Testcontainers` and `@Container` annotations start a `MockServerContainer` and create a `MockServerClient` connected to it.
* `@DynamicPropertySource` overrides `photos.api.base-url` to point at the MockServer endpoint, so the application talks to MockServer instead of the real photo service.
* `@BeforeEach` resets the `MockServerClient` before every test so that expectations from one test don't affect another.
* `shouldGetAlbumById()` configures a mock response for `/albums/{albumId}/photos`, sends a request to the application's `/api/albums/{albumId}` endpoint, and verifies the response body. It also uses `mockServerClient.verify()` to confirm that the expected API call reached MockServer.
* `shouldReturn404StatusWhenAlbumNotFound()` configures MockServer to return a 404 status and verifies the application propagates that status to the caller.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-java-mockserver/run-tests/)

----
url: https://docs.docker.com/guides/testcontainers-java-aws-localstack/run-tests/
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

You should see the LocalStack Docker container start and the test pass. After the tests finish, the container stops and is removed automatically.

## [Summary](#summary)

LocalStack lets you develop and test AWS-based applications locally. The Testcontainers LocalStack module makes it straightforward to write integration tests by using ephemeral LocalStack containers that start on random ports with no external setup required.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Testcontainers LocalStack module](https://java.testcontainers.org/modules/localstack/)
* [Getting started with Testcontainers for Java](https://java.testcontainers.org/quickstart/junit_5_quickstart/)
* [Spring Cloud AWS documentation](https://docs.awspring.io/spring-cloud-aws/docs/3.0.3/reference/html/index.html)

----
url: https://docs.docker.com/scout/deep-dive/advisory-db-sources/
----

# Advisory database sources and matching service

***

Table of contents

***

Reliable information sources are key for Docker Scout's ability to surface relevant and accurate assessments of your software artifacts. Given the diversity of sources and methodologies in the industry, discrepancies in vulnerability assessment results can and do happen. This page describes how the Docker Scout advisory database and its CVE-to-package matching approach works to deal with these discrepancies.

## [Advisory database sources](#advisory-database-sources)

Docker Scout aggregates vulnerability data from multiple sources. The data is continuously updated to ensure that your security posture is represented using the latest available information, in real-time.

Docker Scout uses the following package repositories and security trackers:

* [AlmaLinux Security Advisory](https://errata.almalinux.org/)
* [Alpine secdb](https://secdb.alpinelinux.org/)
* [Amazon Linux Security Center](https://alas.aws.amazon.com/)
* [Bitnami Vulnerability Database](https://github.com/bitnami/vulndb)
* [CISA Known Exploited Vulnerability Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
* [CISA Vulnrichment](https://github.com/cisagov/vulnrichment)
* [Chainguard Security Feed](https://packages.cgr.dev/chainguard/osv/all.json)
* [Debian Security Bug Tracker](https://security-tracker.debian.org/tracker/)
* [Exploit Prediction Scoring System (EPSS)](https://api.first.org/epss/)
* [GitHub Advisory Database](https://github.com/advisories/)
* [GitLab Advisory Database](https://gitlab.com/gitlab-org/advisories-community/)
* [Golang VulnDB](https://github.com/golang/vulndb)
* [National Vulnerability Database](https://nvd.nist.gov/)
* [Oracle Linux Security](https://linux.oracle.com/security/)
* [Photon OS 3.0 Security Advisories](https://github.com/vmware/photon/wiki/Security-Updates-3)
* [Python Packaging Advisory Database](https://github.com/pypa/advisory-database)
* [RedHat Security Data](https://www.redhat.com/security/data/metrics/)
* [Rocky Linux Security Advisory](https://errata.rockylinux.org/)
* [RustSec Advisory Database](https://github.com/rustsec/advisory-db)
* [SUSE Security CVRF](http://ftp.suse.com/pub/projects/security/cvrf/)
* [Ubuntu CVE Tracker](https://people.canonical.com/~ubuntu-security/cve/)
* [Wolfi Security Feed](https://packages.wolfi.dev/os/security.json)
* [inTheWild, a community-driven open database of vulnerability exploitation](https://github.com/gmatuz/inthewilddb)

When you enable Docker Scout for your Docker organization, a new database instance is provisioned on the Docker Scout platform. The database stores the Software Bill of Materials (SBOM) and other metadata about your images. When a security advisory has new information about a vulnerability, your SBOM is cross-referenced with the CVE information to detect how it affects you.

For more details on how image analysis works, see the [image analysis page](https://docs.docker.com/scout/explore/analysis/).

## [Severity and scoring priority](#severity-and-scoring-priority)

Docker Scout uses two main principles when determining severity and scoring for CVEs:

* Source priority
* CVSS version preference

For source priority, Docker Scout follows this order:

1. Vendor advisories: Scout always uses the severity and scoring data from the source that matches the package and version. For example, Debian data for Debian packages.

2. NIST scoring data: If the vendor doesn't provide scoring data for a CVE, Scout falls back to NIST scoring data.

For CVSS version preference, once Scout has selected a source, it prefers CVSS v4 over v3 when both are available, as v4 is the more modern and precise scoring model.

## [Vulnerability matching](#vulnerability-matching)

Traditional tools often rely on broad [Common Product Enumeration (CPE)](https://en.wikipedia.org/wiki/Common_Platform_Enumeration) matching, which can lead to many false-positive results.

Docker Scout uses [Package URLs (PURLs)](https://github.com/package-url/purl-spec) to match packages against CVEs, which yields more precise identification of vulnerabilities. PURLs significantly reduce the chances of false positives, focusing only on genuinely affected packages.

## [Supported package ecosystems](#supported-package-ecosystems)

Docker Scout supports the following package ecosystems:

* .NET
* GitHub packages
* Go
* Java
* JavaScript
* PHP
* Python
* RPM
* Ruby
* `alpm` (Arch Linux)
* `apk` (Alpine Linux)
* `deb` (Debian Linux and derivatives)

----
url: https://docs.docker.com/guides/java/configure-ci-cd/
----

# Configure CI/CD for your Java application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete the previous sections of this guide, starting with [Containerize your app](https://docs.docker.com/guides/java/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

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

1. Go to your repository on GitHub and then select the **Actions** tab. The project already has the `maven-build` workflow to build and test your Java application with Maven. If you want, you can optionally disable this workflow because you won't use it in this guide. You'll create a new, alternate workflow to build, test, and push your image.

2. Select **New workflow**.

3. Select **set up a workflow yourself**.

   This takes you to a page for creating a new GitHub actions workflow file in your repository, under `.github/workflows/main.yml` by default.

4. In the editor window, copy and paste the following YAML configuration.

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

[Test your Java deployment »](https://docs.docker.com/guides/java/deploy/)

----
url: https://docs.docker.com/reference/api/extensions-sdk/Toast/
----

# Interface: Toast

***

Table of contents

***

Toasts provide a brief notification to the user. They appear temporarily and shouldn't interrupt the user experience. They also don't require user input to disappear.

**`Since`**

0.2.0

## [Methods](#methods)

### [success](#success)

▸ **success**(`msg`): `void`

Display a toast message of type success.

```typescript
ddClient.desktopUI.toast.success("message");
```

#### [Parameters](#parameters)

| Name  | Type     | Description                          |
| ----- | -------- | ------------------------------------ |
| `msg` | `string` | The message to display in the toast. |

#### [Returns](#returns)

`void`

***

### [warning](#warning)

▸ **warning**(`msg`): `void`

Display a toast message of type warning.

```typescript
ddClient.desktopUI.toast.warning("message");
```

#### [Parameters](#parameters-1)

| Name  | Type     | Description                            |
| ----- | -------- | -------------------------------------- |
| `msg` | `string` | The message to display in the warning. |

#### [Returns](#returns-1)

`void`

***

### [error](#error)

▸ **error**(`msg`): `void`

Display a toast message of type error.

```typescript
ddClient.desktopUI.toast.error("message");
```

#### [Parameters](#parameters-2)

| Name  | Type     | Description                          |
| ----- | -------- | ------------------------------------ |
| `msg` | `string` | The message to display in the toast. |

#### [Returns](#returns-2)

`void`

----
url: https://docs.docker.com/reference/build-checks/workdir-relative-path/
----

# WorkdirRelativePath

***

Table of contents

***

## [Output](#output)

```text
Relative workdir 'app/src' can have unexpected results if the base image changes
```

## [Description](#description)

When specifying `WORKDIR` in a build stage, you can use an absolute path, like `/build`, or a relative path, like `./build`. Using a relative path means that the working directory is relative to whatever the previous working directory was. So if your base image uses `/usr/local/foo` as a working directory, and you specify a relative directory like `WORKDIR build`, the effective working directory becomes `/usr/local/foo/build`.

The `WorkdirRelativePath` build rule warns you if you use a `WORKDIR` with a relative path without first specifying an absolute path in the same Dockerfile. The rationale for this rule is that using a relative working directory for base image built externally is prone to breaking, since working directory may change upstream without warning, resulting in a completely different directory hierarchy for your build.

## [Examples](#examples)

❌ Bad: this assumes that `WORKDIR` in the base image is `/` (if that changes upstream, the `web` stage is broken).

```dockerfile
FROM nginx AS web
WORKDIR usr/share/nginx/html
COPY public .
```

✅ Good: a leading slash ensures that `WORKDIR` always ends up at the desired path.

```dockerfile
FROM nginx AS web
WORKDIR /usr/share/nginx/html
COPY public .
```

----
url: https://docs.docker.com/guides/lab-docker-agent/
----

[Lab: Getting Started with Docker Agent](https://docs.docker.com/guides/lab-docker-agent/)

Hands-on lab: Create, share, and orchestrate intelligent AI agents using Docker Agent, MCP Toolkit, and Docker.

AI Labs

20 minutes

Resources:

* [Docker Agent documentation](https://github.com/docker/docker-agent)
* [Docker MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)
* [Labspace repository](https://github.com/ajeetraina/labspace-cagent)

[« Back to all guides](/guides/)

# Lab: Getting Started with Docker Agent

***

Table of contents

***

This lab walks you through building intelligent agents with Docker Agent. You'll learn beginner agent concepts, then build sophisticated multi-agent teams that handle complex real-world tasks. Learn how to create, share, and orchestrate AI agents with Docker.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-cagent up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

* Create simple agents with Docker Agent
* Use built-in generic agentic tools for common tasks
* Integrate MCP servers from the MCP Toolkit
* Share agents using the Docker Registry
* Build multi-agent systems for complex workflows
* Use Docker Model Runner with Docker Agent (preview)

## [Modules](#modules)

| # | Module                     | Description                                             |
| - | -------------------------- | ------------------------------------------------------- |
| 1 | Introduction               | Overview of Docker Agent and intelligent agent concepts |
| 2 | Getting Started            | Create your first agent with Docker Agent               |
| 3 | Using Built-in Tools       | Leverage the generic agentic tools in Docker Agent      |
| 4 | Using MCP                  | Integrate MCP servers from the MCP Toolkit              |
| 5 | Sharing Agents             | Package and share agents via Docker Registry            |
| 6 | Introduction to Sub-agents | Build multi-agent systems with sub-agent orchestration  |
| 7 | Conclusion                 | Summary and next steps                                  |

----
url: https://docs.docker.com/guides/nextjs/configure-github-actions/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Automate your builds with GitHub Actions

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize Next.js application](https://docs.docker.com/guides/nextjs/containerize/).

You must also have:

* A [GitHub](https://github.com/signup) account.
* A verified [Docker Hub](https://hub.docker.com/signup) account.

***

## [Overview](#overview)

In this section, you'll set up a CI/CD pipeline using [GitHub Actions](https://docs.github.com/en/actions) to automatically:

* Build your Next.js application inside a Docker container.
* Run tests in a consistent environment.
* Push the production-ready image to [Docker Hub](https://hub.docker.com).

***

## [Integrate GitHub and Docker Hub](#integrate-github-and-docker-hub)

To enable GitHub Actions to build and push Docker images, you'll securely store your Docker Hub credentials in your new GitHub repository.

### [Step 1: Connect your GitHub repository to Docker Hub](#step-1-connect-your-github-repository-to-docker-hub)

1. Create a Personal Access Token (PAT) from [Docker Hub](https://hub.docker.com)

   1. Go to your **Docker Hub account → Account Settings → Security**.
   2. Generate a new Access Token with **Read/Write** permissions.
   3. Name it something like `nextjs-sample`.
   4. Copy and save the token — you'll need it in Step 4.

2. Create a repository in [Docker Hub](https://hub.docker.com/repositories/)

   1. Go to your **Docker Hub account → Create a repository**.
   2. For the Repository Name, use something descriptive — for example: `nextjs-sample`.
   3. Once created, copy and save the repository name — you'll need it in Step 4.

3. Create a new [GitHub repository](https://github.com/new) for your Next.js project

4. Add Docker Hub credentials as GitHub repository secrets

   In your newly created GitHub repository:

   1. Navigate to: **Settings → Secrets and variables → Actions → New repository secret**.

   2. Add the following secrets:

   | Name                     | Value                                            |
   | ------------------------ | ------------------------------------------------ |
   | `DOCKER_USERNAME`        | Your Docker Hub username                         |
   | `DOCKERHUB_TOKEN`        | Your Docker Hub access token (created in Step 1) |
   | `DOCKERHUB_PROJECT_NAME` | Your Docker Project Name (created in Step 2)     |

   These secrets let GitHub Actions authenticate securely with Docker Hub during automated workflows.

5. Connect Your Local Project to GitHub

   Link your local project to the GitHub repository you just created by running the following command from your project root:

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

6. Push Your Source Code to GitHub

   Follow these steps to commit and push your local project to your GitHub repository:

   1. Stage all files for commit.

      ```console
      $ git add -A
      ```

      This command stages all changes — including new, modified, and deleted files — preparing them for commit.

   2. Commit your changes.

      ```console
      $ git commit -m "Initial commit"
      ```

      This command creates a commit that snapshots the staged changes with a descriptive message.

   3. Push the code to the `main` branch.

      ```console
      $ git push -u origin main
      ```

      This command pushes your local commits to the `main` branch of the remote GitHub repository and sets the upstream branch.

Once completed, your code will be available on GitHub, and any GitHub Actions workflow you've configured will run automatically.

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
# CI/CD – Next.js Application with Docker
# Builds the app, runs tests in a container, and pushes the production image to Docker Hub.

name: CI/CD – Next.js Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-push:
    name: Build, Test and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout source code
      - name: Checkout source code
        uses: actions/checkout@v5
        with:
          fetch-depth: 0

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      # 3. Cache Docker layers
      - name: Cache Docker layers
        uses: actions/cache@v5
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: ${{ runner.os }}-buildx-

      # 4. Cache pnpm dependencies
      - name: Cache pnpm dependencies
        uses: actions/cache@v4
        with:
          path: ~/.local/share/pnpm/store
          key: ${{ runner.os }}-pnpm-${{ hashFiles('**/pnpm-lock.yaml') }}
          restore-keys: ${{ runner.os }}-pnpm-

      # 5. Extract metadata
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build dev Docker image (for running tests)
      - name: Build Docker image for tests
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run Vitest tests inside the container
      # Use same package-manager detection as Dockerfile (no corepack at runtime; node user can't write to /usr/local/bin)
      - name: Run tests
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            -e CI=true \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "if [ -f package-lock.json ]; then npm run test:run; elif [ -f yarn.lock ]; then yarn test:run; elif [ -f pnpm-lock.yaml ]; then pnpm run test:run; else npm run test:run; fi"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Log in to Docker Hub (only needed for push)
      - name: Log in to Docker Hub
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push production image (only on push to main)
      - name: Build and push production image
        if: github.event_name == 'push' && github.ref == 'refs/heads/main'
        uses: docker/build-push-action@v6
        with:
          context: .
          file: Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max
```

This workflow performs the following tasks for your Next.js application:

* Triggers on every `push` or `pull request` targeting the `main` branch.
* Builds a development Docker image using `Dockerfile.dev`, optimized for testing.
* Executes unit tests using Jest inside a clean, containerized environment to ensure consistency.
* Halts the workflow immediately if any test fails — enforcing code quality.
* Caches both Docker build layers and npm dependencies for faster CI runs.
* Authenticates securely with Docker Hub using GitHub repository secrets.
* Builds a production-ready image using the `Dockerfile`.
* Tags and pushes the final image to Docker Hub with both `latest` and short SHA tags for traceability.

> Note
>
> For more information about `docker/build-push-action`, refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

***

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
> * Under Branch protection rules, select **Add rule**.
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

In this section, you set up a complete CI/CD pipeline for your containerized Next.js application using GitHub Actions.

With this setup, your Next.js application is now ready for automated testing and deployment across environments — increasing confidence, consistency, and team productivity.

***

***

## [Next steps](#next-steps)

Next, learn how you can locally test and debug your Next.js workloads on Kubernetes before deploying. This helps you ensure your application behaves as expected in a production-like environment, reducing surprises during deployment.

[Test your Next.js deployment »](https://docs.docker.com/guides/nextjs/deploy/)

----
url: https://docs.docker.com/build/ci/github-actions/share-image-jobs/
----

# Share built image between jobs with GitHub Actions

***

***

As each job is isolated in its own runner, you can't use your built image between jobs, except if you're using [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) or [Docker Build Cloud](/build-cloud). However, you can [pass data between jobs](https://docs.github.com/en/actions/using-workflows/storing-workflow-data-as-artifacts#passing-data-between-jobs-in-a-workflow) in a workflow using the [actions/upload-artifact](https://github.com/actions/upload-artifact) and [actions/download-artifact](https://github.com/actions/download-artifact) actions:

```yaml
name: ci

on:
  push:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and export
        uses: docker/build-push-action@v7
        with:
          tags: myimage:latest
          outputs: type=docker,dest=${{ runner.temp }}/myimage.tar

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}/myimage.tar

  use:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Download artifact
        uses: actions/download-artifact@v4
        with:
          name: myimage
          path: ${{ runner.temp }}

      - name: Load image
        run: |
          docker load --input ${{ runner.temp }}/myimage.tar
          docker image ls -a
```

----
url: https://docs.docker.com/reference/build-checks/undefined-arg-in-from/
----

# UndefinedArgInFrom

***

Table of contents

***

## [Output](#output)

```text
FROM argument 'VARIANT' is not declared
```

## [Description](#description)

This rule warns for cases where you're consuming an undefined build argument in `FROM` instructions.

Interpolating build arguments in `FROM` instructions can be a good way to add flexibility to your build, and lets you pass arguments that overriding the base image of a stage. For example, you might use a build argument to specify the image tag:

```dockerfile
ARG ALPINE_VERSION=3.20

FROM alpine:${ALPINE_VERSION}
```

This makes it possible to run the build with a different `alpine` version by specifying a build argument:

```console
$ docker buildx build --build-arg ALPINE_VERSION=edge .
```

This check also tries to detect and warn when a `FROM` instruction reference miss-spelled built-in build arguments, like `BUILDPLATFORM`.

## [Examples](#examples)

❌ Bad: the `VARIANT` build argument is undefined.

```dockerfile
FROM node:22${VARIANT} AS jsbuilder
```

✅ Good: the `VARIANT` build argument is defined.

```dockerfile
ARG VARIANT="-alpine3.20"
FROM node:22${VARIANT} AS jsbuilder
```

----
url: https://docs.docker.com/reference/cli/docker/image/history/
----

# docker image history

***

| Description                                                               | Show the history of an image           |
| ------------------------------------------------------------------------- | -------------------------------------- |
| Usage                                                                     | `docker image history [OPTIONS] IMAGE` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker history`                       |

## [Description](#description)

Show the history of an image

## [Options](#options)

| Option                    | Default | Description                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`--format`](#format)     |         | Format output using a custom template: 'table': Print output in table format with column headers (default) 'table TEMPLATE': Print output in table format using the given Go template 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `-H, --human`             | `true`  | Print sizes and dates in human readable format                                                                                                                                                                                                                                                                                                                                         |
| `--no-trunc`              |         | Don't truncate output                                                                                                                                                                                                                                                                                                                                                                  |
| [`--platform`](#platform) |         | API 1.48+ Show history for the given platform. Formatted as `os[/arch[/variant]]` (e.g., `linux/amd64`)                                                                                                                                                                                                                                                                                |
| `-q, --quiet`             |         | Only show image IDs                                                                                                                                                                                                                                                                                                                                                                    |

## [Examples](#examples)

To see how the `docker:latest` image was built:

```console
$ docker history docker

IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
3e23a5875458        8 days ago          /bin/sh -c #(nop) ENV LC_ALL=C.UTF-8            0 B
8578938dd170        8 days ago          /bin/sh -c dpkg-reconfigure locales &&    loc   1.245 MB
be51b77efb42        8 days ago          /bin/sh -c apt-get update && apt-get install    338.3 MB
4b137612be55        6 weeks ago         /bin/sh -c #(nop) ADD jessie.tar.xz in /        121 MB
750d58736b4b        6 weeks ago         /bin/sh -c #(nop) MAINTAINER Tianon Gravi <ad   0 B
511136ea3c5a        9 months ago                                                        0 B                 Imported from -
```

To see how the `docker:apache` image was added to a container's base image:

```console
$ docker history docker:scm
IMAGE               CREATED             CREATED BY                                      SIZE                COMMENT
2ac9d1098bf1        3 months ago        /bin/bash                                       241.4 MB            Added Apache to Fedora base image
88b42ffd1f7c        5 months ago        /bin/sh -c #(nop) ADD file:1fd8d7f9f6557cafc7   373.7 MB
c69cab00d6ef        5 months ago        /bin/sh -c #(nop) MAINTAINER Lokesh Mandvekar   0 B
511136ea3c5a        19 months ago                                                       0 B                 Imported from -
```

### [Format the output (--format)](#format)

The formatting option (`--format`) will pretty-prints history output using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder     | Description                                                                                               |
| --------------- | --------------------------------------------------------------------------------------------------------- |
| `.ID`           | Image ID                                                                                                  |
| `.CreatedSince` | Elapsed time since the image was created if `--human=true`, otherwise timestamp of when image was created |
| `.CreatedAt`    | Timestamp of when image was created                                                                       |
| `.CreatedBy`    | Command that was used to create the image                                                                 |
| `.Size`         | Image disk size                                                                                           |
| `.Comment`      | Comment for image                                                                                         |

When using the `--format` option, the `history` command either outputs the data exactly as the template declares or, when using the `table` directive, includes column headers as well.

The following example uses a template without headers and outputs the `ID` and `CreatedSince` entries separated by a colon (`:`) for the `busybox` image:

```console
$ docker history --format "{{.ID}}: {{.CreatedSince}}" busybox

f6e427c148a7: 4 weeks ago
<missing>: 4 weeks ago
```

### [Show history for a specific platform (--platform)](#platform)

The `--platform` option allows you to specify which platform variant to show history for if multiple platforms are present. By default, `docker history` shows the history for the daemon's native platform or if not present, the first available platform.

If the local image store has multiple platform variants of an image, the `--platform` option selects which variant to show the history for. An error is produced if the given platform is not present in the local image cache.

The platform option takes the `os[/arch[/variant]]` format; for example, `linux/amd64` or `linux/arm64/v8`. Architecture and variant are optional, and if omitted falls back to the daemon's defaults.

The following example pulls the RISC-V variant of the `alpine:latest` image and shows its history.

```console
$ docker image pull --quiet --platform=linux/riscv64 alpine
docker.io/library/alpine:latest

$ docker image history --platform=linux/s390x alpine
IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
beefdbd8a1da   3 weeks ago   /bin/sh -c #(nop)  CMD ["/bin/sh"]              0B
<missing>      3 weeks ago   /bin/sh -c #(nop) ADD file:ba2637314e600db5a…   8.46MB
```

The following example attempts to show the history for a platform variant of `alpine:latest` that doesn't exist in the local image store, resulting in an error.

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

$ docker image history --platform=linux/s390x alpine
Error response from daemon: image with reference alpine:latest was found but does not match the specified platform: wanted linux/s390x
```

----
url: https://docs.docker.com/engine/
----

# Docker Engine

***

Table of contents

***

Docker Engine is an open source containerization technology for building and containerizing your applications. Docker Engine acts as a client-server application with:

* A server with a long-running daemon process [`dockerd`](/reference/cli/dockerd).
* APIs which specify interfaces that programs can use to talk to and instruct the Docker daemon.
* A command line interface (CLI) client [`docker`](/reference/cli/docker/).

The CLI uses [Docker APIs](https://docs.docker.com/reference/api/engine/) to control or interact with the Docker daemon through scripting or direct CLI commands. Many other Docker applications use the underlying API and CLI. The daemon creates and manages Docker objects, such as images, containers, networks, and volumes.

For more details, see [Docker Architecture](https://docs.docker.com/get-started/docker-overview/#docker-architecture).

### [Install Docker Engine](/engine/install)

[Learn how to install the open source Docker Engine for your distribution.](/engine/install)

### [Storage](/storage)

[Use persistent data with Docker containers.](/storage)

### [Networking](/network)

[Manage network connections between containers.](/network)

### [Container logs](/config/containers/logging/)

[Learn how to view and read container logs.](/config/containers/logging/)

### [Prune](/config/pruning)

[Tidy up unused resources.](/config/pruning)

### [Configure the daemon](/config/daemon)

[Delve into the configuration options of the Docker daemon.](/config/daemon)

### [Rootless mode](/engine/security/rootless)

[Run Docker without root privileges.](/engine/security/rootless)

### [Deprecated features](/engine/deprecated/)

[Find out what features of Docker Engine you should stop using.](/engine/deprecated/)

### [Release notes](/engine/release-notes)

[Read the release notes for the latest version.](/engine/release-notes)

## [Licensing](#licensing)

Commercial use of Docker Engine obtained via Docker Desktop within larger enterprises (exceeding 250 employees OR with annual revenue surpassing $10 million USD), requires a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsEngine). Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

----
url: https://docs.docker.com/reference/cli/docker/compose/push/
----

# docker compose push

***

| Description | Push service images                          |
| ----------- | -------------------------------------------- |
| Usage       | `docker compose push [OPTIONS] [SERVICE...]` |

## [Description](#description)

Pushes images for services to their respective registry/repository.

The following assumptions are made:

* You are pushing an image you have built locally
* You have access to the build key

Examples

```yaml
services:
  service1:
    build: .
    image: localhost:5000/yourimage  ## goes to local registry

  service2:
    build: .
    image: your-dockerid/yourimage  ## goes to your repository on Docker Hub
```

## [Options](#options)

| Option                   | Default | Description                                            |
| ------------------------ | ------- | ------------------------------------------------------ |
| `--ignore-push-failures` |         | Push what it can and ignores images with push failures |
| `--include-deps`         |         | Also push images of services declared as dependencies  |
| `-q, --quiet`            |         | Push without printing progress information             |

----
url: https://docs.docker.com/reference/api/extensions-sdk/BackendV0/
----

# Interface: BackendV0

***

Table of contents

***

## [Container Methods](#container-methods)

### [execInContainer](#execincontainer)

▸ **execInContainer**(`container`, `cmd`): `Promise`<[`ExecResultV0`](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

Executes a command inside a container.

```typescript
const output = await window.ddClient.backend.execInContainer(container, cmd);

console.log(output);
```

> Warning
>
> It will be removed in a future version.

#### [Parameters](#parameters)

| Name        | Type     | Description                 |
| ----------- | -------- | --------------------------- |
| `container` | `string` | -                           |
| `cmd`       | `string` | The command to be executed. |

#### [Returns](#returns)

`Promise`<[`ExecResultV0`](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

***

## [HTTP Methods](#http-methods)

### [get](#get)

▸ **get**(`url`): `Promise`<`unknown`>

Performs an HTTP GET request to a backend service.

```typescript
window.ddClient.backend
 .get("/some/service")
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [get](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#get) instead.

#### [Parameters](#parameters-1)

| Name  | Type     | Description                     |
| ----- | -------- | ------------------------------- |
| `url` | `string` | The URL of the backend service. |

#### [Returns](#returns-1)

`Promise`<`unknown`>

***

### [post](#post)

▸ **post**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP POST request to a backend service.

```typescript
window.ddClient.backend
 .post("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [post](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#post) instead.

#### [Parameters](#parameters-2)

| Name   | Type     | Description                     |
| ------ | -------- | ------------------------------- |
| `url`  | `string` | The URL of the backend service. |
| `data` | `any`    | The body of the request.        |

#### [Returns](#returns-2)

`Promise`<`unknown`>

***

### [put](#put)

▸ **put**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP PUT request to a backend service.

```typescript
window.ddClient.backend
 .put("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [put](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#put) instead.

#### [Parameters](#parameters-3)

| Name   | Type     | Description                     |
| ------ | -------- | ------------------------------- |
| `url`  | `string` | The URL of the backend service. |
| `data` | `any`    | The body of the request.        |

#### [Returns](#returns-3)

`Promise`<`unknown`>

***

### [patch](#patch)

▸ **patch**(`url`, `data`): `Promise`<`unknown`>

Performs an HTTP PATCH request to a backend service.

```typescript
window.ddClient.backend
 .patch("/some/service", { ... })
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [patch](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#patch) instead.

#### [Parameters](#parameters-4)

| Name   | Type     | Description                     |
| ------ | -------- | ------------------------------- |
| `url`  | `string` | The URL of the backend service. |
| `data` | `any`    | The body of the request.        |

#### [Returns](#returns-4)

`Promise`<`unknown`>

***

### [delete](#delete)

▸ **delete**(`url`): `Promise`<`unknown`>

Performs an HTTP DELETE request to a backend service.

```typescript
window.ddClient.backend
 .delete("/some/service")
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [delete](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#delete) instead.

#### [Parameters](#parameters-5)

| Name  | Type     | Description                     |
| ----- | -------- | ------------------------------- |
| `url` | `string` | The URL of the backend service. |

#### [Returns](#returns-5)

`Promise`<`unknown`>

***

### [head](#head)

▸ **head**(`url`): `Promise`<`unknown`>

Performs an HTTP HEAD request to a backend service.

```typescript
window.ddClient.backend
 .head("/some/service")
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [head](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#head) instead.

#### [Parameters](#parameters-6)

| Name  | Type     | Description                     |
| ----- | -------- | ------------------------------- |
| `url` | `string` | The URL of the backend service. |

#### [Returns](#returns-6)

`Promise`<`unknown`>

***

### [request](#request)

▸ **request**(`config`): `Promise`<`unknown`>

Performs an HTTP request to a backend service.

```typescript
window.ddClient.backend
 .request({ url: "/url", method: "GET", headers: { 'header-key': 'header-value' }, data: { ... }})
 .then((value: any) => console.log(value));
```

> Warning
>
> It will be removed in a future version. Use [request](https://docs.docker.com/reference/api/extensions-sdk/HttpService/#request) instead.

#### [Parameters](#parameters-7)

| Name     | Type                                                                                       | Description                     |
| -------- | ------------------------------------------------------------------------------------------ | ------------------------------- |
| `config` | [`RequestConfigV0`](https://docs.docker.com/reference/api/extensions-sdk/RequestConfigV0/) | The URL of the backend service. |

#### [Returns](#returns-7)

`Promise`<`unknown`>

***

## [VM Methods](#vm-methods)

### [execInVMExtension](#execinvmextension)

▸ **execInVMExtension**(`cmd`): `Promise`<[`ExecResultV0`](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

Executes a command inside the backend container. If your extensions ships with additional binaries that should be run inside the backend container you can use the `execInVMExtension` function.

```typescript
const output = await window.ddClient.backend.execInVMExtension(
  `cliShippedInTheVm xxx`
);

console.log(output);
```

> Warning
>
> It will be removed in a future version. Use [exec](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/#exec) instead.

#### [Parameters](#parameters-8)

| Name  | Type     | Description                 |
| ----- | -------- | --------------------------- |
| `cmd` | `string` | The command to be executed. |

#### [Returns](#returns-8)

`Promise`<[`ExecResultV0`](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)>

***

### [spawnInVMExtension](#spawninvmextension)

▸ **spawnInVMExtension**(`cmd`, `args`, `callback`): `void`

Returns a stream from the command executed in the backend container.

```typescript
window.ddClient.spawnInVMExtension(
  `cmd`,
  [`arg1`, `arg2`],
  (data: any, err: any) => {
    console.log(data.stdout, data.stderr);
    // Once the command exits we get the status code
    if (data.code) {
      console.log(data.code);
    }
  }
);
```

> Warning
>
> It will be removed in a future version.

#### [Parameters](#parameters-9)

| Name       | Type                                      | Description                                                                    |
| ---------- | ----------------------------------------- | ------------------------------------------------------------------------------ |
| `cmd`      | `string`                                  | The command to be executed.                                                    |
| `args`     | `string`\[]                               | The arguments of the command to execute.                                       |
| `callback` | (`data`: `any`, `error`: `any`) => `void` | The callback function where to listen from the command output data and errors. |

#### [Returns](#returns-9)

`void`

----
url: https://docs.docker.com/reference/cli/docker/container/start/
----

# docker container start

***

| Description                                                               | Start one or more stopped containers                        |
| ------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Usage                                                                     | `docker container start [OPTIONS] CONTAINER [CONTAINER...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker start`                                              |

## [Description](#description)

Start one or more stopped containers

## [Options](#options)

| Option              | Default | Description                                                     |
| ------------------- | ------- | --------------------------------------------------------------- |
| `-a, --attach`      |         | Attach STDOUT/STDERR and forward signals                        |
| `--checkpoint`      |         | experimental (daemon) Restore from this checkpoint              |
| `--checkpoint-dir`  |         | experimental (daemon) Use a custom checkpoint storage directory |
| `--detach-keys`     |         | Override the key sequence for detaching a container             |
| `-i, --interactive` |         | Attach container's STDIN                                        |

## [Examples](#examples)

```console
$ docker start my_container
```

----
url: https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/
----

# Enhanced Container Isolation

***

Table of contents

***

Subscription: Business

For: Administrators

Enhanced Container Isolation (ECI) prevents malicious containers from compromising Docker Desktop or the host system. It applies advanced security techniques automatically while maintaining full developer productivity and workflow compatibility.

* ECI strengthens container isolation and locks in security configurations created by administrators, such as [Registry Access Management policies](https://docs.docker.com/enterprise/security/hardened-desktop/registry-access-management/) and [Settings Management](https://docs.docker.com/enterprise/security/hardened-desktop/settings-management/) controls.
* ECI works alongside other Docker security features like reduced Linux capabilities, seccomp, and AppArmor.

If you are using WSL2 backend, ensure you’re running WSL version 2.6 or later. This is required because ECI depends on a Linux kernel version of at least 6.3.0, and WSL 2.6+ includes kernel version 6.6.

## [Who should use Enhanced Container Isolation?](#who-should-use-enhanced-container-isolation)

ECI is designed for:

* Organizations that want to prevent container-based attacks and reduce security vulnerabilities in developer environments
* Security teams that need stronger container isolation without impacting developer workflows
* Enterprises that require additional protection when running untrusted or third-party container images

## [How Enhanced Container Isolation works](#how-enhanced-container-isolation-works)

Docker implements ECI using the [Sysbox container runtime](https://github.com/nestybox/sysbox), a security-enhanced fork of the standard OCI runc runtime. When ECI is turned on, containers created through `docker run` or `docker create` automatically use Sysbox instead of runc without requiring any changes to developer workflows. Docker's default runtime remains runc, but all user containers implicitly launch with Sysbox.

When ECI is turned on, the Docker CLI `--runtime` flag is ignored. Even containers using the `--privileged` flag run securely with ECI, preventing them from breaching the Docker Desktop virtual machine or other containers.

## [Key security features](#key-security-features)

### [Linux user namespace isolation](#linux-user-namespace-isolation)

With Enhanced Container Isolation, all containers leverage Linux user namespaces for stronger isolation. Container root users map to unprivileged users in the Docker Desktop VM:

```console
$ docker run -it --rm --name=first alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

This output shows that container root (0) maps to unprivileged user 100000 in the VM, with a range of 64K user IDs. Each container gets exclusive mappings:

```console
$ docker run -it --rm --name=second alpine
/ # cat /proc/self/uid_map
         0     165536      65536
```

Without Enhanced Container Isolation, containers run as true root:

```console
$ docker run -it --rm alpine
/ # cat /proc/self/uid_map
         0       0     4294967295
```

By using Linux user namespaces, ECI ensures container processes never run with valid user IDs in the Linux VM, constraining their capabilities to resources within the container only.

### [Secured privileged containers](#secured-privileged-containers)

Privileged containers (`docker run --privileged`) normally pose significant security risks because they provide unrestricted access to the Linux kernel. Without ECI, privileged containers can:

* Run as true root with all capabilities
* Bypass seccomp and AppArmor restrictions
* Access all hardware devices
* Modify global kernel settings

Organizations securing developer environments face challenges with privileged containers because they can gain control of the Docker Desktop VM and alter security settings like registry access management and network proxies.

Enhanced Container Isolation transforms privileged containers by ensuring they can only access resources within their container boundary. For example, privileged containers can't access Docker Desktop's network configuration:

```console
$ docker run --privileged djs55/bpftool map show
Error: can't get next map: Operation not permitted
```

Without ECI, privileged containers can easily access and modify these settings:

```console
$ docker run --privileged djs55/bpftool map show
17: ringbuf  name blocked_packets  flags 0x0
        key 0B  value 0B  max_entries 16777216  memlock 0B
18: hash  name allowed_map  flags 0x0
        key 4B  value 4B  max_entries 10000  memlock 81920B
```

Advanced container workloads like Docker-in-Docker and Kubernetes-in-Docker still work with ECI but run much more securely.

> Note
>
> ECI doesn't prevent users from running privileged containers, but makes them secure by containing their access. Privileged workloads that modify global kernel settings (loading kernel modules, changing Berkeley Packet Filter settings) receive "permission denied" errors.

### [Namespace isolation enforcement](#namespace-isolation-enforcement)

Enhanced Container Isolation prevents containers from sharing Linux namespaces with the Docker Desktop VM, maintaining isolation boundaries:

**PID namespace sharing blocked:**

```console
$ docker run -it --rm --pid=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share namespaces [pid] with the host (because they use the linux user-namespace for isolation): unknown.
```

**Network namespace sharing blocked:**

```console
$ docker run -it --rm --network=host alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: invalid or unsupported container spec: sysbox containers can't share a network namespace with the host (because they use the linux user-namespace for isolation): unknown.
```

**User namespace override ignored:**

```console
$ docker run -it --rm --userns=host alpine
/ # cat /proc/self/uid_map
         0     100000      65536
```

Docker build operations using `--network-host` and Docker buildx entitlements (`network.host`, `security.insecure`) are also blocked.

### [Protected bind mounts](#protected-bind-mounts)

Enhanced Container Isolation maintains support for standard file sharing while preventing access to sensitive VM directories:

Host directory mounts continue to work:

```console
$ docker run -it --rm -v $HOME:/mnt alpine
/ # ls /mnt
# Successfully lists home directory contents
```

VM configuration mounts are blocked:

```console
$ docker run -it --rm -v /etc/docker/daemon.json:/mnt/daemon.json alpine
docker: Error response from daemon: failed to create shim task: OCI runtime create failed: error in the container spec: can't mount /etc/docker/daemon.json because it's configured as a restricted host mount: unknown
```

This prevents containers from reading or modifying Docker Engine configurations, registry access management settings, proxy configurations, and other security-related VM files.

> Note
>
> By default, ECI blocks bind mounting the Docker Engine socket (/var/run/docker.sock) as this would grant containers control over Docker Engine. Administrators can create exceptions for trusted container images.

### [Advanced system call protection](#advanced-system-call-protection)

Enhanced Container Isolation intercepts sensitive system calls to prevent containers from using legitimate capabilities maliciously:

```console
$ docker run -it --rm --cap-add SYS_ADMIN -v $HOME:/mnt:ro alpine
/ # mount -o remount,rw /mnt /mnt
mount: permission denied (are you root?)
```

Even with `CAP_SYS_ADMIN` capability, containers can't change read-only bind mounts to read-write, ensuring they can't breach container boundaries.

Containers can still create internal mounts within their filesystem:

```console
/ # mkdir /root/tmpfs
/ # mount -t tmpfs tmpfs /root/tmpfs
/ # mount -o remount,ro /root/tmpfs /root/tmpfs
/ # findmnt | grep tmpfs
├─/root/tmpfs    tmpfs      tmpfs    ro,relatime,uid=100000,gid=100000
```

ECI performs system call filtering efficiently by intercepting only control-path system calls (rarely used) while leaving data-path system calls unaffected, maintaining container performance.

### [Automatic filesystem user ID mapping](#automatic-filesystem-user-id-mapping)

Enhanced Container Isolation solves file sharing challenges between containers with different user ID ranges through automatic filesystem mapping.

Each container gets exclusive user ID mappings, but Sysbox uses filesystem user ID remapping via Linux kernel ID-mapped mounts (added in 2021) or alternative shiftsfs module. This maps filesystem accesses from containers' real user IDs to standard ranges, enabling:

* Volume sharing across containers with different user ID ranges
* Consistent file ownership regardless of container user ID mappings
* Transparent file access without user intervention

### [Information hiding through filesystem emulation](#information-hiding-through-filesystem-emulation)

ECI emulates portions of `/proc` and `/sys` filesystems within containers to hide sensitive host information and provide per-container views of kernel resources:

```console
$ docker run -it --rm alpine
/ # cat /proc/uptime
5.86 5.86
```

This shows container uptime instead of Docker Desktop VM uptime, preventing system information from leaking into containers.

Several `/proc/sys` resources that aren't namespaced by the Linux kernel are emulated per-container, with Sysbox coordinating values when programming kernel settings. This enables container workloads that normally require privileged access to run securely.

## [Performance and compatibility](#performance-and-compatibility)

Enhanced Container Isolation maintains optimized performance and full compatibility:

* No performance impact: System call filtering targets only control-path calls, leaving data-path operations unaffected
* Full workflow compatibility: Existing development processes, tools, and container images work unchanged
* Advanced workload support: Docker-in-Docker, Kubernetes-in-Docker, and other complex scenarios work securely
* Automatic management: User ID mappings, filesystem access, and security policies are handled automatically
* Standard image support: No special container images or modifications required

> Important
>
> ECI protection varies by Docker Desktop version and doesn't yet protect extension containers. Docker builds and Kubernetes in Docker Desktop have varying protection levels depending on the version. For details, see [Enhanced Container Isolation limitations](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/limitations/).

----
url: https://docs.docker.com/guides/
----

***

## All guides

Filtered results: showing 103 out of 103 guides.

----
url: https://docs.docker.com/dhi/how-to/
----

# How-tos

***

Table of contents

***

This section provides practical, task-based guidance for working with Docker Hardened Images (DHIs). Whether you're evaluating DHIs for the first time or integrating them into a production CI/CD pipeline, these topics cover the key tasks across the adoption journey: discover, adopt, verify, and govern.

The topics are organized around the typical lifecycle of working with DHIs, but you can use them as needed based on your specific workflow.

Explore the topics below that match your current needs.

## [Discover](#discover)

Explore available images and metadata in the DHI catalog.

### [Search and evaluate Docker Hardened Images](/dhi/how-to/explore/)

[Learn how to find and evaluate image repositories, variants, metadata, and attestations in the DHI catalog on Docker Hub.](/dhi/how-to/explore/)

## [Adopt](#adopt)

Mirror trusted images, customize as needed, and integrate into your workflows.

### [Get started with DHI Select and Enterprise](/dhi/how-to/select-enterprise/)

[Learn how to mirror repositories, customize images, and access compliance variants with DHI Select and Enterprise subscriptions.](/dhi/how-to/select-enterprise/)

### [Use the DHI CLI](/dhi/how-to/cli/)

[Use the dhictl command-line tool to manage and interact with Docker Hardened Images.](/dhi/how-to/cli/)

### [Mirror a Docker Hardened Image repository](/dhi/how-to/mirror/)

[Learn how to mirror an image into your organization's namespace and optionally push it to another private registry.](/dhi/how-to/mirror/)

### [Customize a Docker Hardened Image or chart](/dhi/how-to/customize/)

[Learn how to customize Docker Hardened Images and charts.](/dhi/how-to/customize/)

### [Use hardened system packages](/dhi/how-to/hardened-packages/)

[Learn how to use Docker's hardened system packages in your images.](/dhi/how-to/hardened-packages/)

### [Use a Docker Hardened Image](/dhi/how-to/use/)

[Learn how to pull, run, and reference Docker Hardened Images in Dockerfiles, CI pipelines, and standard development workflows.](/dhi/how-to/use/)

### [Use a Docker Hardened Image chart](/dhi/how-to/helm/)

[Learn how to use a Docker Hardened Image chart.](/dhi/how-to/helm/)

## [Verify](#verify)

Check signatures, SBOMs, and provenance, and scan for vulnerabilities.

### [Verify a Docker Hardened Image or chart](/dhi/how-to/verify/)

[Use Docker Scout or cosign to verify signed attestations like SBOMs, provenance, and vulnerability data for Docker Hardened Images and charts.](/dhi/how-to/verify/)

### [Scan Docker Hardened Images](/dhi/how-to/scan/)

[Learn how to scan Docker Hardened Images for known vulnerabilities using Docker Scout, Grype, or Trivy.](/dhi/how-to/scan/)

## [Govern](#govern)

Enforce policies to maintain security and compliance.

### [Enforce Docker Hardened Image usage with policies](/dhi/how-to/policies/)

[Learn how to use image policies with Docker Scout for Docker Hardened Images.](/dhi/how-to/policies/)

----
url: https://docs.docker.com/reference/api/hub/latest.yaml
----

\# yaml-language-server: $schema=https\://raw\.githubusercontent.com/OAI/OpenAPI-Specification/refs/heads/main/schemas/v3.0/schema.yaml openapi: 3.0.3 info: title: Docker HUB API version: 2-beta x-logo: url: https\://docs.docker.com/assets/images/logo-docker-main.png href: /reference description: | Docker Hub is a service provided by Docker for finding and sharing container images with your team. It is the world's largest library and community for container images. In addition to the \[Docker Hub UI]\(https\://docs.docker.com/docker-hub/) and \[Docker Hub CLI tool]\(https\://github.com/docker/hub-tool#readme) (currently experimental), Docker provides an API that allows you to interact with Docker Hub. Browse through the Docker Hub API documentation to explore the supported endpoints. servers: - description: Docker HUB API x-audience: public url: https\://hub.docker.com tags: - name: changelog x-displayName: Changelog description: | See the \[Changelog]\(/reference/api/hub/changelog) for a summary of changes across Docker Hub API versions. - name: resources x-displayName: Resources description: | The following resources are available to interact with the documented API: - \[Docker Hub CLI tool]\(https\://github.com/docker/hub-tool#readme) (currently experimental) - name: rate-limiting x-displayName: Rate Limiting description: | The Docker Hub API is limited on the amount of requests you can perform per minute against it. If you haven't hit the limit, each request to the API will return the following headers in the response. - \`X-RateLimit-Limit\` - The limit of requests per minute. - \`X-RateLimit-Remaining\` - The remaining amount of calls within the limit period. - \`X-RateLimit-Reset\` - The unix timestamp of when the remaining resets. If you have hit the limit, you will receive a response status of \`429\` and the \`Retry-After\` header in the response. The \[\`Retry-After\` header]\(https\://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Retry-After) specifies the number of seconds to wait until you can call the API again. \*\*Note\*\*: These rate limits are separate from anti-abuse and Docker Hub download, or pull rate limiting. To learn more about Docker Hub pull rate limiting, see \[Usage and limits]\(https\://docs.docker.com/docker-hub/usage/). - name: authentication x-displayName: Authentication description: | Most Docker Hub API endpoints require you to authenticate using your Docker credentials before using them. Additionally, similar to the Docker Hub UI features, API endpoint responses may vary depending on your subscription (Personal, Pro, or Team) and your account's permissions. To learn more about the features available in each subscription and to upgrade your existing subscription, see \[Docker Pricing]\(https\://www\.docker.com/pricing?ref=Docs\&refAction=DocsApiHub). # Types The Docker Hub API supports the following authentication types. You must use each authentication type with the \[Create access token]\(#tag/authentication-api/operation/AuthCreateAccessToken) route to obtain a bearer token. ## Password Using a username and password is the most powerful, yet least secure way to authenticate with Docker as a user. It allows access to resources for the user without scopes. \_In general, it is recommended to use a personal access token (PAT) instead.\_ \_\*\*The password authentication type is not available if your organization has SSO enforced.\*\*\_ ## Personal Access Token (PAT) Using a username and PAT is the most secure way to authenticate with Docker as a user. PATs are scoped to specific resources and scopes. Currently, a PAT is a more secure password due to limited functionality. In the future, we may add fine-grained access like organization access tokens for enhanced usage and security. ## Organization Access Token (OAT) Organization access tokens are scoped to specific resources and scopes in an organization. They are managed by organization owners. These tokens are meant for automation and are not meant to be used by users. # Labels These labels will show up on routes in this reference that allow for use of bearer tokens issued from them. - name: authentication-api x-displayName: Authentication description: | The authentication endpoints allow you to authenticate with Docker Hub APIs. For more information, see \[Authentication]\(#tag/authentication). - name: access-tokens x-displayName: Personal Access Tokens description: | The Personal Access Token endpoints lets you manage personal access tokens. For more information, see \[Access Tokens]\(https\://docs.docker.com/security/access-tokens/). You can use a personal access token instead of a password in the \[Docker CLI]\(https\://docs.docker.com/engine/reference/commandline/cli/) or in the \[Create an authentication token]\(#operation/PostUsersLogin) route to obtain a bearer token. ### Scopes For each scope grouping (in this case "repo"), you only need to define 1 scope as any lower scopes are assumed. For example: If you define \`repo:write\`, the API assumes the scope of both \`repo:read\` \*and\* \`repo:public\_read\` as well. If you were to define both \`repo:write\` \*and\* \`repo:read\`, then \`repo:read\` is assumed by \`repo:write\` and ignored. \*\*\*Treat your personal access token like your password and keep it secret. You cannot retrieve your token after it is generated.\*\*\* - name: audit-logs x-displayName: Audit Logs description: | The Audit Logs API endpoints allow you to query audit log events across a namespace. For more information, see \[Audit Logs]\(https\://docs.docker.com/admin/activity-logs/). - name: org-settings x-displayName: Org Settings description: | The Org Settings API endpoints allow you to manage your organization's settings. - name: repositories x-displayName: Repositories description: | The repository endpoints allow you to access your repository's tags. - name: orgs x-displayName: Organizations x-audience: public description: | The organization endpoints allow you to interact with and manage your organizations. For more information, see \[Organization administration overview]\(https\://docs.docker.com/admin/organization/). - name: groups x-displayName: Groups (Teams) x-audience: public description: | The groups endpoints allow you to manage your organization's teams and their members. For more information, see \[Create and manage a team]\(https\://docs.docker.com/admin/organization/manage/manage-a-team/). - name: invites x-displayName: Invites x-audience: public description: | The invites endpoints allow you to manage invites for users to join your Docker organization. For more information, see \[Invite members]\(https\://docs.docker.com/admin/organization/manage/members/#invite-members). - name: scim x-displayName: SCIM x-audience: public description: | SCIM is a provisioning system that lets you manage users within your identity provider (IdP). For more information, see \[System for Cross-domain Identity management]\(https\://docs.docker.com/security/for-admins/provisioning/scim/). - name: org-access-tokens x-displayName: Organization Access Tokens x-audience: public description: | The organization access token endpoints allow you to manage organization access tokens (OATs). See \[Organization access tokens]\(https\://docs.docker.com/security/for-admins/access-tokens/) for more information. paths: /v2/users/login: post: tags: - authentication-api summary: Create an authentication token operationId: PostUsersLogin security: \[] deprecated: true description: | Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs. The returned token is used in the HTTP Authorization header like \`Authorization: Bearer {TOKEN}\`. \_\*\*As of September 16, 2024, this route requires a personal access token (PAT) instead of a password if your organization has SSO enforced.\*\*\_

**Deprecated**: Use \[[Create access token](#tag/authentication-api/operation/AuthCreateAccessToken)] instead.

requestBody: content: application/json: schema: $ref: "#/components/schemas/UsersLoginRequest" description: Login details. required: true responses: "200": description: Authentication successful content: application/json: schema: $ref: "#/components/schemas/PostUsersLoginSuccessResponse" "401": description: Authentication failed or second factor required content: application/json: schema: $ref: "#/components/schemas/PostUsersLoginErrorResponse" /v2/users/2fa-login: post: tags: - authentication-api summary: Second factor authentication operationId: PostUsers2FALogin security: \[] description: | When a user has two-factor authentication (2FA) enabled, this is the second call to perform after \`/v2/users/login\` call. Creates and returns a bearer token in JWT format that you can use to authenticate with Docker Hub APIs. The returned token is used in the HTTP Authorization header like \`Authorization: Bearer {TOKEN}\`. Most Docker Hub APIs require this token either to consume or to get detailed information. For example, to list images in a private repository. requestBody: content: application/json: schema: $ref: "#/components/schemas/Users2FALoginRequest" description: Login details. required: true responses: "200": description: Authentication successful content: application/json: schema: $ref: "#/components/schemas/PostUsersLoginSuccessResponse" "401": description: Authentication failed content: application/json: schema: $ref: "#/components/schemas/PostUsers2FALoginErrorResponse" /v2/auth/token: post: tags: - authentication-api security: \[] summary: Create access token operationId: AuthCreateAccessToken description: | Creates and returns a short-lived access token in JWT format for use as a bearer when calling Docker APIs. If successful, the access token returned should be used in the HTTP Authorization header like \`Authorization: Bearer {access\_token}\`. \_\*\*If your organization has SSO enforced, you must use a personal access token (PAT) instead of a password.\*\*\_ requestBody: content: application/json: schema: description: Request to create access token type: object required: - identifier - secret properties: identifier: description: | The identifier of the account to create an access token for. If using a password or personal access token, this must be a username. If using an organization access token, this must be an organization name. type: string example: myusername secret: description: | The secret of the account to create an access token for. This can be a password, personal access token, or organization access token. type: string example: dckr\_pat\_124509ugsdjga93 responses: "200": description: Token created content: application/json: schema: $ref: "#/components/schemas/AuthCreateTokenResponse" "401": description: Authentication failed $ref: "#/components/responses/unauthorized" /v2/access-tokens: post: summary: Create personal access token description: Creates and returns a personal access token. tags: - access-tokens security: - bearerAuth: \[] requestBody: content: application/json: schema: $ref: "#/components/schemas/createAccessTokenRequest" required: true responses: "201": description: Created content: application/json: schema: $ref: "#/components/schemas/createAccessTokensResponse" "400": $ref: "#/components/responses/BadRequest" "401": $ref: "#/components/responses/Unauthorized" get: summary: List personal access tokens description: Returns a paginated list of personal access tokens. tags: - access-tokens security: - bearerAuth: \[] parameters: - in: query name: page schema: type: number default: 1 - in: query name: page\_size schema: type: number default: 10 responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/getAccessTokensResponse" "400": $ref: "#/components/responses/BadRequest" "401": $ref: "#/components/responses/Unauthorized" /v2/access-tokens/{uuid}: parameters: - in: path name: uuid required: true schema: type: string patch: summary: Update personal access token description: | Updates a personal access token partially. You can either update the token's label or enable/disable it. tags: - access-tokens security: - bearerAuth: \[] requestBody: content: application/json: schema: $ref: "#/components/schemas/patchAccessTokenRequest" required: true responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/patchAccessTokenResponse" "400": $ref: "#/components/responses/BadRequest" "401": $ref: "#/components/responses/Unauthorized" get: summary: Get personal access token description: Returns a personal access token by UUID. tags: - access-tokens security: - bearerAuth: \[] responses: "200": description: OK content: application/json: schema: allOf: - $ref: "#/components/schemas/accessToken" - type: object properties: token: type: string example: "" "401": $ref: "#/components/responses/Unauthorized" "404": $ref: "#/components/responses/NotFound" delete: summary: Delete personal access token description: | Deletes a personal access token permanently. This cannot be undone. tags: - access-tokens security: - bearerAuth: \[] responses: "204": description: A successful response. "401": $ref: "#/components/responses/Unauthorized" "404": $ref: "#/components/responses/NotFound" /v2/auditlogs/{account}/actions: get: summary: List audit log actions description: | List audit log actions for a namespace to be used as a filter for querying audit log events. operationId: AuditLogs\_ListAuditActions security: - bearerAuth: \[] responses: "200": description: A successful response. content: application/json: schema: $ref: "#/components/schemas/GetAuditActionsResponse" examples: response: value: actions: billing: actions: - name: plan.upgrade description: Occurs when your organization’s billing plan is upgraded to a higher tier plan. label: Plan Upgraded - name: plan.downgrade description: Occurs when your organization’s billing plan is downgraded to a lower tier plan. label: Plan Downgraded - name: plan.seat\_add description: Occurs when a seat is added to your organization’s billing plan. label: Seat Added - name: plan.seat\_remove description: Occurs when a seat is removed from your organization’s billing plan. label: Seat Removed - name: plan.cycle\_change description: Occurs when there is a change in the recurring interval that your organization is charged. label: Billing Cycle Changed - name: plan.downgrade\_cancel description: Occurs when a scheduled plan downgrade for your organization is canceled. label: Plan Downgrade Canceled - name: plan.seat\_removal\_cancel description: Occurs when a scheduled seat removal for an organization’s billing plan is canceled. label: Seat Removal Canceled - name: plan.upgrade.request description: Occurs when a user in your organization requests a plan upgrade. label: Plan Upgrade Requested - name: plan.downgrade.request description: Occurs when a user in your organization requests a plan downgrade. label: Plan Downgrade Requested - name: plan.seat\_add.request description: Occurs when a user in your organization requests an increase in the number of seats. label: Seat Addition Requested - name: plan.seat\_removal.request description: Occurs when a user in your organization requests a decrease in the number of seats. label: Seat Removal Requested - name: plan.cycle\_change.request description: Occurs when a user in your organization requests a change in the billing cycle. label: Billing Cycle Change Requested - name: plan.downgrade\_cancel.request description: Occurs when a user in your organization requests a cancellation of a scheduled plan downgrade. label: Plan Downgrade Cancellation Requested - name: plan.seat\_removal\_cancel.request description: Occurs when a user in your organization requests a cancellation of a scheduled seat removal. label: Seat Removal Cancellation Requested - name: plan.product\_change description: Occurs when there is a change in the product that your organization subscribes to. label: Billing Product Changed label: Billing enterprise: actions: - name: setting.policy.create description: Details of adding an admin settings policy label: Policy created - name: setting.policy.update description: Details of updating an admin settings policy label: Policy updated - name: setting.policy.delete description: Details of deleting an admin settings policy label: Policy deleted - name: setting.policy.transfer description: Details of transferring an admin settings policy to another owner label: Policy transferred - name: sso.connection.create description: Details of creating a new org/company SSO connection label: Create SSO Connection - name: sso.connection.update description: Details of updating an existing org/company SSO connection label: Update SSO Connection - name: sso.connection.delete description: Details of deleting an existing org/company SSO connection label: Delete SSO Connection - name: sso.connection.enforcement\_toggle description: Details of toggling enforcement on an existing org/company SSO connection label: Enforce SSO - name: sso.connection.scim\_toggle description: Details of toggling SCIM on an existing org/company SSO connection label: Enforce SCIM - name: sso.connection.scim\_token\_refresh description: Details of a SCIM token refresh on an existing org/company SSO connection label: Refresh SCIM Token - name: sso.connection.connection\_type\_change description: Details of a connection type change on an existing org/company SSO connection label: Change SSO Connection Type - name: sso.connection.jit\_toggle description: Details of a JIT toggle on an existing org/company SSO connection label: Toggle JIT provisioning label: Enterprise offload: actions: - name: lease.start description: Details of the started Offload lease. label: Offload lease start - name: lease.end description: Details of the ended Offload lease. label: Offload lease end label: Offload oidc: actions: - name: connection.create description: Details of creating an OIDC connection. label: OIDC connection created - name: connection.update description: Details of updating an OIDC connection. label: OIDC connection updated - name: connection.delete description: Details of deleting an OIDC connection. label: OIDC connection deleted label: OIDC org: actions: - name: create description: Activities related to the creation of a new organization label: Organization Created - name: member.add description: Details of the member added to your organization label: Organization Member Added - name: member.remove description: Details about the member removed from your organization label: Organization Member Removed - name: member.role.change description: Details about the role changed for a member in your organization label: Member Role Changed - name: member.invite.send description: Details of the member invited to your organization label: Org Member Invited - name: team.create description: Activities related to the creation of a team label: Organization Created - name: team.update description: Activities related to the modification of a team label: Organization Deleted - name: team.delete description: Activities related to the deletion of a team label: Organization Deleted - name: team.member.add description: Details of the member added to your team label: Team Member Added - name: team.member.remove description: Details of the member removed from your team label: Team Member Removed - name: domain.create description: Details of the single sign-on domain added to your organization label: Single Sign-On domain added - name: domain.verify description: Details of the single sign-on domain verified for your organization label: Single Sign-On domain verified - name: domain.delete description: Details of the single sign-on domain removed from your organization label: Single Sign-On domain deleted - name: domain.auto-provisioning.toggle description: Details of toggling the Auto-Provisioning feature on a domain on or off label: Organization Auto-Provisioning Toggled - name: settings.update description: Details related to the organization setting that was updated label: Organization Settings Updated - name: registry\_access.enabled description: Activities related to enabling Registry Access Management label: Registry Access Management enabled - name: registry\_access.disabled description: Activities related to disabling Registry Access Management label: Registry Access Management disabled - name: registry\_access.registry\_added description: Activities related to the addition of a registry label: Registry Access Management registry added - name: registry\_access.registry\_updated description: Details related to the registry that was updated label: Registry Access Management registry updated - name: registry\_access.registry\_removed description: Activities related to the removal of a registry label: Registry Access Management registry removed - name: access\_token.create description: Access token created in organization label: Access token created - name: access\_token.update description: Access token updated in organization label: Access token updated - name: access\_token.delete description: Access token deleted in organization label: Access token deleted - name: customrole.create description: A custom role was created label: Custom role created - name: customrole.update description: An existing custom role was updated label: Custom role updated - name: customrole.delete description: A custom role was deleted label: Custom role deleted - name: securepolicyconfigure.create description: A secure policy configuration was created label: Secure Policy Configuration created - name: securepolicyconfigure.update description: A secure policy configuration was updated label: Secure Policy Configuration updated - name: securepolicyconfigure.delete description: A secure policy configuration was deleted label: Secure Policy Configuration deleted - name: securepolicyclient.create description: A secure policy client was created label: Secure Policy Client created - name: securepolicyclient.update description: A secure policy client was updated label: Secure Policy Client updated - name: securepolicyclient.delete description: A secure policy client was deleted label: Secure Policy Client deleted - name: securepolicyprofile.create description: A secure policy profile was created label: Secure Policy Profile created - name: securepolicyprofile.update description: A secure policy profile was updated label: Secure Policy Profile updated - name: securepolicyprofile.delete description: A secure policy profile was deleted label: Secure Policy Profile deleted label: Organization repo: actions: - name: create description: Activities related to the creation of a new repository label: Repository Created - name: update description: Activities related to the modification of a repository label: Repository Updated - name: delete description: Activities related to the deletion of a repository label: Repository Deleted - name: change\_privacy description: Details related to the privacy policies that were updated label: Privacy Changed - name: category.updated description: Details related to updating a repository categories label: Categories updated - name: immutable.tags.updated description: Details related to updating tag immutability of a repository label: Tag immutability updated - name: tag.push description: Activities related to the tags pushed label: Tag Pushed - name: tag.delete description: Activities related to the tags deleted label: Tag Deleted label: Repository "429": description: "" content: application/json: schema: {} examples: response: value: detail: Rate limit exceeded error: false "500": description: "" content: application/json: schema: {} default: description: An unexpected error response. content: application/json: schema: $ref: "#/components/schemas/rpcStatus" parameters: - name: account description: Namespace to query audit log actions for. in: path required: true schema: type: string tags: - audit-logs /v2/auditlogs/{account}: get: summary: List audit log events description: | List audit log events for a given namespace. operationId: AuditLogs\_ListAuditLogs security: - bearerAuth: \[] responses: "200": description: A successful response. content: application/json: schema: $ref: "#/components/schemas/GetAuditLogsResponse" examples: response: value: logs: - account: docker action: repo.tag.push name: docker/example actor: docker data: digest: sha256:c1ae9c435032a276f80220c7d9b40f76266bbe79243d34f9cda30b76fe114dfa tag: latest timestamp: "2021-02-19T01:34:35Z" action\_description: | pushed the tag latest with the digest sha256:c1ae9c435032a to the repository docker/example - account: docker action: offload.lease.end name: docker actor: docker data: lease\_id: l\_3EgPuRCjtUqT279CFPOQWcO8zOf resource\_type: run\_4cpu\_8mem started\_at: "2026-06-04T18:24:21Z" updated\_at: "2026-06-04T18:36:43Z" org\_id: b908ca6e-b9a9-4a53-a9a5-6bec96f72432 user\_id: ecae6747-e42c-43cb-925d-cfce1ab32b02 timestamp: "2026-06-04T18:36:43Z" action\_description: "offload lease 'l\_3EgPuRCjtUqT279CFPOQWcO8zOf' ended, ran for '12m22s'" "429": description: "" content: application/json: schema: {} examples: response: value: detail: Rate limit exceeded error: false "500": description: "" content: application/json: schema: {} default: description: An unexpected error response. content: application/json: schema: $ref: "#/components/schemas/rpcStatus" parameters: - name: account description: Namespace to query audit logs for. in: path required: true schema: type: string - name: action description: | action name one of \["repo.tag.push", ...]. Optional parameter to filter specific audit log actions. in: query required: false schema: type: string - name: name description: | name. Optional parameter to filter audit log events to a specific name. For repository events, this is the name of the repository. For organization events, this is the name of the organization. For team member events, this is the username of the team member. in: query required: false schema: type: string - name: actor description: | actor name. Optional parameter to filter audit log events to the specific user who triggered the event. in: query required: false schema: type: string - name: from description: Start of the time window you wish to query audit events for. in: query required: false schema: type: string format: date-time - name: to description: End of the time window you wish to query audit events for. in: query required: false schema: type: string format: date-time - name: page description: page - specify page number. Page number to get. in: query required: false schema: type: integer format: int32 default: 1 - name: page\_size description: page\_size - specify page size. Number of events to return per page. in: query required: false schema: type: integer format: int32 default: 25 tags: - audit-logs /v2/orgs/{name}/settings: parameters: - in: path name: name description: Name of the organization. required: true schema: type: string get: summary: Get organization settings description: | Returns organization settings by name. tags: - org-settings security: - bearerAuth: \[] responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/orgSettings" "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" put: summary: Update organization settings description: | Updates an organization's settings. Some settings are only used when the organization is on a business subscription. \*\*\*Only users with administrative privileges for the organization (owner role) can modify these settings.\*\*\* The following settings are only used on a business subscription: - \`restricted\_images\` tags: - org-settings security: - bearerAuth: \[] requestBody: content: application/json: schema: required: - restricted\_images properties: restricted\_images: allOf: - $ref: "#/components/schemas/restricted\_images" - type: object required: - enabled - allow\_official\_images - allow\_verified\_publishers required: true responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/orgSettings" "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" /v2/orgs/{name}/access-tokens: post: summary: Create access token description: | Create an access token for an organization. tags: - org-access-tokens security: - bearerAuth: \[] requestBody: content: application/json: schema: $ref: "#/components/schemas/createOrgAccessTokenRequest" required: true responses: "201": description: Created content: application/json: schema: $ref: "#/components/schemas/createOrgAccessTokenResponse" "400": $ref: "#/components/responses/BadRequest" "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" get: summary: List access tokens description: | List access tokens for an organization. tags: - org-access-tokens security: - bearerAuth: \[] parameters: - in: query name: page schema: type: number default: 1 - in: query name: page\_size schema: type: number default: 10 responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/getOrgAccessTokensResponse" "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" /v2/orgs/{org\_name}/access-tokens/{access\_token\_id}: parameters: - $ref: "#/components/parameters/org\_name" - in: path name: access\_token\_id required: true schema: type: string description: The ID of the access token to retrieve example: "a7a5ef25-8889-43a0-8cc7-f2a94268e861" get: summary: Get access token description: | Get details of a specific access token for an organization. tags: - org-access-tokens security: - bearerAuth: \[] responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/getOrgAccessTokenResponse" "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" patch: summary: Update access token description: | Update a specific access token for an organization. tags: - org-access-tokens security: - bearerAuth: \[] requestBody: content: application/json: schema: $ref: "#/components/schemas/updateOrgAccessTokenRequest" required: true responses: "200": description: OK content: application/json: schema: $ref: "#/components/schemas/updateOrgAccessTokenResponse" "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" delete: summary: Delete access token description: | Delete a specific access token for an organization. This action cannot be undone. tags: - org-access-tokens security: - bearerAuth: \[] responses: "204": description: Access token deleted successfully "401": $ref: "#/components/responses/Unauthorized" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" /v2/namespaces/{namespace}/repositories/{repository}/tags: parameters: - $ref: "#/components/parameters/namespace" - $ref: "#/components/parameters/repository" get: operationId: ListRepositoryTags summary: List repository tags tags: - repositories security: - bearerAuth: \[] parameters: - in: query name: page required: false schema: type: integer description: Page number to get. Defaults to 1. - in: query name: page\_size required: false schema: type: integer description: Number of items to get per page. Defaults to 10. Max of 100. responses: "200": $ref: "#/components/responses/list\_tags" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" head: summary: Check repository tags tags: - repositories security: - bearerAuth: \[] responses: "200": description: Repository contains tags "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" /v2/namespaces/{namespace}/repositories/{repository}/tags/{tag}: parameters: - $ref: "#/components/parameters/namespace" - $ref: "#/components/parameters/repository" - $ref: "#/components/parameters/tag" get: operationId: GetRepositoryTag summary: Read repository tag tags: - repositories security: - bearerAuth: \[] responses: "200": $ref: "#/components/responses/get\_tag" "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" head: summary: Check repository tag tags: - repositories security: - bearerAuth: \[] responses: "200": description: Repository tag exists "403": $ref: "#/components/responses/Forbidden" "404": $ref: "#/components/responses/NotFound" /v2/namespaces/{namespace}/repositories/{repository}/immutabletags: parameters: - $ref: "#/components/parameters/namespace" - $ref: "#/components/parameters/repository" patch: operationId: UpdateRepositoryImmutableTags summary: "Update repository immutable tags" description: | Updates the immutable tags configuration for this repository. \*\*Only users with administrative privileges for the repository can modify these settings.\*\* tags: - repositories security: - bearerAuth: \[] requestBody: $ref: "#/components/requestBodies/update\_repository\_immutable\_tags\_request" responses: 200: $ref: "#/components/responses/update\_repository\_immutable\_tags\_response" 400: $ref: "#/components/responses/bad\_request" 401: $ref: "#/components/responses/unauthorized" 403: $ref: "#/components/responses/forbidden" 404: $ref: "#/components/responses/not\_found" /v2/namespaces/{namespace}/repositories/{repository}/immutabletags/verify: parameters: - $ref: "#/components/parameters/namespace" - $ref: "#/components/parameters/repository" post: operationId: VerifyRepositoryImmutableTags summary: "Verify repository immutable tags" description: | Validates the immutable tags regex pass in parameter and returns a list of tags matching it in this repository. \*\*Only users with administrative privileges for the repository call this endpoint.\*\* tags: - repositories security: - bearerAuth: \[] requestBody: $ref: "#/components/requestBodies/immutable\_tags\_verify\_request" responses: 200: $ref: "#/components/responses/immutable\_tags\_verify\_response" 400: $ref: "#/components/responses/bad\_request" 401: $ref: "#/components/responses/unauthorized" 403: $ref: "#/components/responses/forbidden" 404: $ref: "#/components/responses/not\_found" /v2/repositories/{namespace}/{repository}/groups: parameters: - $ref: "#/components/parameters/namespace" - $ref: "#/components/parameters/repository" post: summary: Assign a group (Team) to a repository for access tags: - repositories operationId: CreateRepositoryGroup security: - bearerAuth: \[] requestBody: required: true content: application/json: schema: $ref: "#/components/schemas/RepositoryGroupCreationRequest" example: group\_id: 12345 permission: "write" responses: "200": description: Repository group permission created successfully content: application/json: schema: $ref: "#/components/schemas/RepositoryGroup" example: group\_name: "developers" permission: "write" group\_id: 12345 "400": description: Bad Request - Invalid request parameters content: application/json: schema: $ref: "#/components/schemas/error" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/NotFound" /v2/namespaces/{namespace}/repositories: parameters: - $ref: "#/components/parameters/namespace" get: operationId: listNamespaceRepositories summary: List repositories in a namespace description: | Returns a list of repositories within the specified namespace (organization or user). Public repositories are accessible to everyone, while private repositories require appropriate authentication and permissions. tags: - repositories security: - bearerAuth: \[] - {} # Allow anonymous access for public repositories parameters: - in: query name: page required: false schema: type: integer minimum: 1 default: 1 description: Page number to get. Defaults to 1. - in: query name: page\_size required: false schema: type: integer minimum: 1 maximum: 100 default: 10 description: Number of repositories to get per page. Defaults to 10. Max of 100. - in: query name: name required: false schema: type: string description: Filter repositories by name (partial match). - in: query name: ordering required: false schema: type: string enum: - name - -name - last\_updated - -last\_updated - pull\_count - -pull\_count description: | Order repositories by the specified field. Prefix with '-' for descending order. Available options: - \`name\` / \`-name\`: Repository name (ascending/descending) - \`last\_updated\` / \`-last\_updated\`: Last update time (ascending/descending) - \`pull\_count\` / \`-pull\_count\`: Number of pulls (ascending/descending) responses: "200": description: List of repositories content: application/json: schema: $ref: "#/components/schemas/list\_repositories\_response" examples: repositories\_list: value: count: 287 next: "https\://hub.docker.com/v2/namespaces/docker/repositories?page=2\&page\_size=2" previous: null results: - name: "highland\_builder" namespace: "docker" repository\_type: "image" status: 1 status\_description: "active" description: "Image for performing Docker build requests" is\_private: false star\_count: 7 pull\_count: 15722123 last\_updated: "2023-06-20T10:44:45.459826Z" last\_modified: "2024-10-16T13:48:34.145251Z" date\_registered: "2015-05-19T21:13:35.937763Z" affiliation: "" media\_types: - "application/octet-stream" - "application/vnd.docker.container.image.v1+json" - "application/vnd.docker.distribution.manifest.v1+prettyjws" content\_types: - "unrecognized" - "image" categories: - name: "Languages & frameworks" slug: "languages-and-frameworks" - name: "Integration & delivery" slug: "integration-and-delivery" - name: "Operating systems" slug: "operating-systems" storage\_size: 488723114800 - name: "whalesay" namespace: "docker" repository\_type: null status: 1 status\_description: "active" description: "An image for use in the Docker demo tutorial" is\_private: false star\_count: 757 pull\_count: 130737682 last\_updated: "2015-06-19T19:06:27.388123Z" last\_modified: "2024-10-16T13:48:34.145251Z" date\_registered: "2015-06-09T18:16:36.527329Z" affiliation: "" media\_types: - "application/vnd.docker.distribution.manifest.v1+prettyjws" content\_types: - "image" categories: - name: "Languages & frameworks" slug: "languages-and-frameworks" - name: "Integration & delivery" slug: "integration-and-delivery" storage\_size: 103666708 "400": description: Bad Request - Invalid request parameters content: application/json: schema: $ref: "#/components/schemas/error" examples: invalid\_ordering: summary: Invalid ordering value value: fields: ordering: \[ "Invalid ordering value. Must be one of: name, -name, last\_updated, -last\_updated, pull\_count, -pull\_count", ] text: "Invalid ordering value" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": description: Page not found - occurs when requesting a page number \`>1\` that exceeds the available results content: application/json: schema: $ref: "#/components/schemas/error" post: summary: Create a new repository description: | Creates a new repository within the specified namespace. The repository will be created with the provided metadata including name, description, and privacy settings. operationId: CreateRepository tags: - repositories security: - BearerAuth: \[] requestBody: required: true content: application/json: schema: $ref: "#/components/schemas/repo\_creation\_request" example: name: "my-app" namespace: "myorganization" description: "A sample application repository" full\_description: "This is a comprehensive description of my application repository that contains additional details about the project." registry: "docker.io" is\_private: false responses: 201: description: Repository created successfully content: application/json: schema: $ref: "#/components/schemas/repository\_info" example: name: "my-app" namespace: "myorganization" repository\_type: "image" status: 1 status\_description: "Active" description: "A sample application repository" is\_private: false is\_automated: false star\_count: 0 pull\_count: 0 last\_updated: "2025-01-20T10:30:00Z" date\_registered: "2025-01-20T10:30:00Z" collaborator\_count: 0 hub\_user: "myorganization" has\_starred: false full\_description: "This is a comprehensive description of my application repository that contains additional details about the project." media\_types: \[] content\_types: \[] categories: \[] immutable\_tags\_settings: enabled: false rules: \[] storage\_size: null source: null 400: $ref: "#/components/responses/bad\_request" 401: $ref: "#/components/responses/unauthorized" 403: $ref: "#/components/responses/forbidden" 404: $ref: "#/components/responses/not\_found" 500: $ref: "#/components/responses/internal\_error" /v2/namespaces/{namespace}/repositories/{repository}: parameters: - $ref: "#/components/parameters/namespace" - $ref: "#/components/parameters/repository" get: operationId: GetRepository summary: Get repository in a namespace description: | Returns a repository within the specified namespace (organization or user). Public repositories are accessible to everyone, while private repositories require appropriate authentication and permissions. tags: - repositories security: - bearerAuth: \[] - {} # Allow anonymous access for public repositories responses: 200: content: application/json: schema: $ref: "#/components/schemas/repository\_info" example: name: "my-app" namespace: "myorganization" repository\_type: "image" status: 1 status\_description: "Active" description: "A sample application repository" is\_private: false is\_automated: false star\_count: 0 pull\_count: 0 last\_updated: "2025-01-20T10:30:00Z" date\_registered: "2025-01-20T10:30:00Z" collaborator\_count: 0 hub\_user: "myorganization" has\_starred: false full\_description: "This is a comprehensive description of my application repository that contains additional details about the project." media\_types: \[] content\_types: \[] categories: \[] immutable\_tags\_settings: enabled: false rules: \[] storage\_size: null source: null 401: $ref: "#/components/responses/unauthorized" 403: $ref: "#/components/responses/forbidden" 404: $ref: "#/components/responses/not\_found" 500: $ref: "#/components/responses/internal\_error" head: operationId: CheckRepository summary: Check repository in a namespace description: | Check a repository within the specified namespace (organization or user). Public repositories are accessible to everyone, while private repositories require appropriate authentication and permissions. tags: - repositories security: - bearerAuth: \[] - {} # Allow anonymous access for public repositories responses: 200: content: application/json: schema: $ref: "#/components/schemas/repository\_info" example: name: "my-app" namespace: "myorganization" repository\_type: "image" status: 1 status\_description: "Active" description: "A sample application repository" is\_private: false is\_automated: false star\_count: 0 pull\_count: 0 last\_updated: "2025-01-20T10:30:00Z" date\_registered: "2025-01-20T10:30:00Z" collaborator\_count: 0 hub\_user: "myorganization" has\_starred: false full\_description: "This is a comprehensive description of my application repository that contains additional details about the project." media\_types: \[] content\_types: \[] categories: \[] immutable\_tags\_settings: enabled: false rules: \[] storage\_size: null source: null 401: $ref: "#/components/responses/unauthorized" 403: $ref: "#/components/responses/forbidden" 404: $ref: "#/components/responses/not\_found" 500: $ref: "#/components/responses/internal\_error" /v2/orgs/{org\_name}/members: parameters: - $ref: "#/components/parameters/org\_name" - $ref: "#/components/parameters/search" - $ref: "#/components/parameters/page" - $ref: "#/components/parameters/page\_size" - $ref: "#/components/parameters/invites" - $ref: "#/components/parameters/type" - $ref: "#/components/parameters/role" get: summary: List org members description: | Returns a list of members for an organization. \_The following fields are only visible to orgs with insights enabled.\_ - \`last\_logged\_in\_at\` - \`last\_seen\_at\` - \`last\_desktop\_version\` To make visible, please see \[View Insights for organization users]\(https\://docs.docker.com/admin/insights/#view-insights-for-organization-users). tags: - orgs security: - bearerAuth: \[] responses: "200": description: List of members content: application/json: schema: type: array items: $ref: "#/components/schemas/org\_member\_paginated" "400": $ref: "#/components/responses/bad\_request" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/orgs/{org\_name}/members/export: parameters: - $ref: "#/components/parameters/org\_name" get: summary: Export org members CSV description: | Export members of an organization as a CSV tags: - orgs security: - bearerAuth: \[] responses: "200": description: Exported members content: text/csv: schema: type: array items: type: object required: - Name - Username - Email - Type - Role - Date Joined properties: Name: type: string description: First and last name of the member Username: type: string description: Username of the member Email: type: string description: Email address of the member Type: type: string description: Type of the member enum: - Invitee - User Permission: type: string description: Permission of the member enum: - Owner - Member Teams: type: string description: Comma-separated list of teams the member is part of example: team-1, team-2 Date Joined: type: string description: Date the member joined the organization example: 2020-01-01 15:00:51.193355 +0000 UTC headers: Content-Disposition: schema: type: string example: attachment;filename="{org\_name}-members-{timestamp}.csv" "400": $ref: "#/components/responses/bad\_request" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/orgs/{org\_name}/members/{username}: x-audience: public parameters: - $ref: "#/components/parameters/org\_name" - $ref: "#/components/parameters/username" put: summary: Update org member (role) description: | Updates the role of a member in the organization. \*\*\*Only users in the "owners" group of the organization can use this endpoint.\*\*\* tags: - orgs security: - bearerAuth: \[] requestBody: required: true content: application/json: schema: required: - role properties: role: type: string description: Role of the member enum: - owner - editor - member responses: "200": description: Member role updated content: application/json: schema: $ref: "#/components/schemas/org\_member" "400": $ref: "#/components/responses/bad\_request" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" delete: summary: Remove member from org description: | Removes the member from the org, ie. all groups in the org, unless they're the last owner tags: - orgs security: - bearerAuth: \[] responses: "204": description: Member removed successfully "400": $ref: "#/components/responses/bad\_request" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/orgs/{org\_name}/invites: x-audience: public parameters: - $ref: "#/components/parameters/org\_name" get: summary: List org invites description: | Return all pending invites for a given org, only team owners can call this endpoint tags: - invites security: - bearerAuth: \[] responses: "200": description: "" content: application/json: schema: type: object properties: data: type: array items: $ref: "#/components/schemas/invite" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/orgs/{org\_name}/groups: x-audience: public parameters: - $ref: "#/components/parameters/org\_name" get: summary: Get groups of an organization description: | tags: - groups security: - bearerAuth: \[] parameters: - $ref: "#/components/parameters/page" - $ref: "#/components/parameters/page\_size" - in: query name: username schema: type: string description: Get groups for the specified username in the organization. - in: query name: search schema: type: string description: Get groups for the specified group in the organization. responses: "200": description: "" content: application/json: schema: properties: count: type: number example: 1 next: type: string example: null previous: type: string example: null results: type: array items: $ref: "#/components/schemas/org\_group" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" post: summary: Create a new group description: | Create a new group within an organization. tags: - groups security: - bearerAuth: \[] requestBody: content: application/json: schema: required: - name properties: name: type: string description: type: string responses: "201": description: Group created successfully content: application/json: schema: $ref: "#/components/schemas/org\_group" "400": $ref: "#/components/responses/bad\_request" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" /v2/orgs/{org\_name}/groups/{group\_name}: x-audience: public parameters: - $ref: "#/components/parameters/org\_name" - $ref: "#/components/parameters/group\_name" get: summary: Get a group of an organization description: | tags: - groups security: - bearerAuth: \[] responses: "200": description: "" content: application/json: schema: $ref: "#/components/schemas/org\_group" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" put: summary: Update the details for an organization group description: | tags: - groups security: - bearerAuth: \[] requestBody: content: application/json: schema: required: - name properties: name: type: string description: type: string responses: "200": description: "" content: application/json: schema: $ref: "#/components/schemas/org\_group" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" patch: summary: Update some details for an organization group description: | tags: - groups security: - bearerAuth: \[] requestBody: content: application/json: schema: properties: name: type: string description: type: string responses: "200": description: "" content: application/json: schema: $ref: "#/components/schemas/org\_group" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" delete: summary: Delete an organization group description: | tags: - groups security: - bearerAuth: \[] responses: "204": description: Group deleted successfully "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/orgs/{org\_name}/groups/{group\_name}/members: x-audience: public get: security: - bearerAuth: \[] parameters: - $ref: "#/components/parameters/org\_name" - $ref: "#/components/parameters/group\_name" - $ref: "#/components/parameters/page" - $ref: "#/components/parameters/page\_size" - in: query name: search schema: type: string description: Search members by username, full\_name or email. summary: List members of a group description: | List the members (users) that are in a group. If user is owner of the org or has otherwise elevated permissions, they can search by email and the result will also contain emails. tags: - groups responses: "200": description: "" content: application/json: schema: properties: count: type: number example: 1 next: type: string example: null previous: type: string example: null results: type: array items: $ref: "#/components/schemas/group\_member" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" post: parameters: - $ref: "#/components/parameters/org\_name" - $ref: "#/components/parameters/group\_name" summary: Add a member to a group description: | tags: - groups security: - bearerAuth: \[] requestBody: $ref: "#/components/requestBodies/add\_member\_to\_org\_group" responses: "200": description: OK "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" "500": $ref: "#/components/responses/internal\_error" /v2/orgs/{org\_name}/groups/{group\_name}/members/{username}: x-audience: public parameters: - $ref: "#/components/parameters/org\_name" - $ref: "#/components/parameters/group\_name" - $ref: "#/components/parameters/username" delete: summary: Remove a user from a group description: | tags: - groups security: - bearerAuth: \[] responses: "204": description: User removed successfully "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/invites/{id}: x-audience: public parameters: - in: path name: id required: true schema: type: string delete: summary: Cancel an invite description: | Mark the invite as cancelled so it doesn't show up on the list of pending invites tags: - invites security: - bearerAuth: \[] responses: "204": description: "" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/invites/{id}/resend: x-audience: public parameters: - in: path name: id schema: type: string required: true patch: summary: Resend an invite description: | Resend a pending invite to the user, any org owner can resend an invite tags: - invites security: - bearerAuth: \[] responses: "204": description: "" "401": $ref: "#/components/responses/unauthorized" "403": $ref: "#/components/responses/forbidden" "404": $ref: "#/components/responses/not\_found" /v2/invites/bulk: x-audience: public parameters: - $ref: "#/components/parameters/bulk\_invite" post: summary: Bulk create invites description: | Create multiple invites by emails or DockerIDs. Only a team owner can create invites. tags: - invites requestBody: $ref: "#/components/requestBodies/bulk\_invite\_request" security: - bearerAuth: \[] responses: "202": description: Accepted content: application/json: schema: type: object properties: invitees: $ref: "#/components/schemas/bulk\_invite" "400": $ref: "#/components/responses/bad\_request" "409": $ref: "#/components/responses/conflict" /v2/scim/2.0/ServiceProviderConfig: x-audience: public get: summary: Get service provider config description: | Returns a service provider config for Docker's configuration. tags: - scim security: - bearerSCIMAuth: \[] responses: "200": $ref: "#/components/responses/scim\_get\_service\_provider\_config\_resp" "401": $ref: "#/components/responses/scim\_unauthorized" "500": $ref: "#/components/responses/scim\_error" /v2/scim/2.0/ResourceTypes: x-audience: public get: summary: List resource types description: | Returns all resource types supported for the SCIM configuration. tags: - scim security: - bearerSCIMAuth: \[] responses: "200": $ref: "#/components/responses/scim\_get\_resource\_types\_resp" "401": $ref: "#/components/responses/scim\_unauthorized" "500": $ref: "#/components/responses/scim\_error" /v2/scim/2.0/ResourceTypes/{name}: x-audience: public get: summary: Get a resource type description: | Returns a resource type by name. tags: - scim parameters: - name: name in: path schema: type: string example: User required: true security: - bearerSCIMAuth: \[] responses: "200": $ref: "#/components/responses/scim\_get\_resource\_type\_resp" "401": $ref: "#/components/responses/scim\_unauthorized" "404": $ref: "#/components/responses/scim\_not\_found" "500": $ref: "#/components/responses/scim\_error" /v2/scim/2.0/Schemas: x-audience: public get: summary: List schemas description: | Returns all schemas supported for the SCIM configuration. tags: - scim security: - bearerSCIMAuth: \[] responses: "200": $ref: "#/components/responses/scim\_get\_schemas\_resp" "401": $ref: "#/components/responses/scim\_unauthorized" "500": $ref: "#/components/responses/scim\_error" /v2/scim/2.0/Schemas/{id}: x-audience: public get: summary: Get a schema description: | Returns a schema by ID. tags: - scim parameters: - name: id in: path schema: type: string example: urn:ietf:params:scim:schemas:core:2.0:User required: true security: - bearerSCIMAuth: \[] responses: "200": $ref: "#/components/responses/scim\_get\_schema\_resp" "401": $ref: "#/components/responses/scim\_unauthorized" "404": $ref: "#/components/responses/scim\_not\_found" "500": $ref: "#/components/responses/scim\_error" /v2/scim/2.0/Users: x-audience: public get: summary: List users description: | Returns paginated users for an organization. Use \`startIndex\` and \`count\` query parameters to receive paginated results. \*\*Sorting:\*\* Sorting allows you to specify the order in which resources are returned by specifying a combination of \`sortBy\` and \`sortOrder\` query parameters. The \`sortBy\` parameter specifies the attribute whose value will be used to order the returned responses. The \`sortOrder\` parameter defines the order in which the \`sortBy\` parameter is applied. Allowed values are "ascending" and "descending". \*\*Filtering:\*\* You can request a subset of resources by specifying the \`filter\` query parameter containing a filter expression. Attribute names and attribute operators used in filters are case insensitive. The filter parameter must contain at least one valid expression. Each expression must contain an attribute name followed by an attribute operator and an optional value. Supported operators are listed below. - \`eq\` equal - \`ne\` not equal - \`co\` contains - \`sw\` starts with - \`and\` Logical "and" - \`or\` Logical "or" - \`not\` "Not" function - \`()\` Precedence grouping tags: - scim security: - bearerSCIMAuth: \[] parameters: - name: startIndex in: query schema: type: integer minimum: 1 description: "" example: 1 - name: count in: query schema: type: integer minimum: 1 maximum: 200 description: "" example: 10 - name: filter in: query schema: type: string description: "" example: userName eq "jon.snow\@docker.com" - $ref: "#/components/parameters/scim\_attributes" - name: sortOrder in: query schema: type: string enum: - ascending - descending - name: sortBy in: query schema: type: string description: User attribute to sort by. example: userName responses: "200": $ref: "#/components/responses/scim\_get\_users\_resp" "400": $ref: "#/components/responses/scim\_bad\_request" "401": $ref: "#/components/responses/scim\_unauthorized" "403": $ref: "#/components/responses/scim\_forbidden" "404": $ref: "#/components/responses/scim\_not\_found" "500": $ref: "#/components/responses/scim\_error" post: summary: Create user description: | Creates a user. If the user already exists by email, they are assigned to the organization on the "company" team. tags: - scim security: - bearerSCIMAuth: \[] requestBody: $ref: "#/components/requestBodies/scim\_create\_user\_request" responses: "201": $ref: "#/components/responses/scim\_create\_user\_resp" "400": $ref: "#/components/responses/scim\_bad\_request" "401": $ref: "#/components/responses/scim\_unauthorized" "403": $ref: "#/components/responses/scim\_forbidden" "404": $ref: "#/components/responses/scim\_not\_found" "409": $ref: "#/components/responses/scim\_conflict" "500": $ref: "#/components/responses/scim\_error" /v2/scim/2.0/Users/{id}: x-audience: public parameters: - $ref: "#/components/parameters/scim\_user\_id" get: summary: Get a user description: | Returns a user by ID. tags: - scim security: - bearerSCIMAuth: \[] responses: "200": $ref: "#/components/responses/scim\_get\_user\_resp" "400": $ref: "#/components/responses/scim\_bad\_request" "401": $ref: "#/components/responses/scim\_unauthorized" "403": $ref: "#/components/responses/scim\_forbidden" "404": $ref: "#/components/responses/scim\_not\_found" "500": $ref: "#/components/responses/scim\_error" put: summary: Update a user description: | Updates a user. This route is used to change the user's name, activate, and deactivate the user. tags: - scim security: - bearerSCIMAuth: \[] requestBody: $ref: "#/components/requestBodies/scim\_update\_user\_request" responses: "200": $ref: "#/components/responses/scim\_update\_user\_resp" "400": $ref: "#/components/responses/scim\_bad\_request" "401": $ref: "#/components/responses/scim\_unauthorized" "403": $ref: "#/components/responses/scim\_forbidden" "404": $ref: "#/components/responses/scim\_not\_found" "409": $ref: "#/components/responses/scim\_conflict" "500": $ref: "#/components/responses/scim\_error" components: responses: BadRequest: description: Bad Request content: application/json: schema: $ref: "#/components/schemas/ValueError" Unauthorized: description: Unauthorized content: application/json: schema: $ref: "#/components/schemas/Error" Forbidden: description: Forbidden content: application/json: schema: $ref: "#/components/schemas/Error" NotFound: description: Not Found content: application/json: schema: $ref: "#/components/schemas/Error" list\_tags: description: list repository tags content: application/json: schema: $ref: "#/components/schemas/paginated\_tags" get\_tag: description: repository tag content: application/json: schema: $ref: "#/components/schemas/tag" bad\_request: description: Bad Request content: application/json: schema: $ref: "#/components/schemas/error" unauthorized: description: Unauthorized content: application/json: schema: $ref: "#/components/schemas/error" forbidden: description: Forbidden content: application/json: schema: $ref: "#/components/schemas/error" not\_found: description: Not Found content: application/json: schema: $ref: "#/components/schemas/error" conflict: description: Conflict content: application/json: schema: $ref: "#/components/schemas/error" internal\_error: description: Internal content: application/json: schema: $ref: "#/components/schemas/error" scim\_bad\_request: description: Bad Request content: application/scim+json: schema: allOf: - $ref: "#/components/schemas/scim\_error" - properties: status: example: "400" scimType: type: string description: Some types of errors will return this per the specification. scim\_unauthorized: description: Unauthorized content: application/scim+json: schema: allOf: - $ref: "#/components/schemas/scim\_error" - properties: status: example: "401" scim\_forbidden: description: Forbidden content: application/scim+json: schema: allOf: - $ref: "#/components/schemas/scim\_error" - properties: status: example: "403" scim\_not\_found: description: Not Found content: application/scim+json: schema: allOf: - $ref: "#/components/schemas/scim\_error" - properties: status: example: "404" scim\_conflict: description: Conflict content: application/scim+json: schema: allOf: - $ref: "#/components/schemas/scim\_error" - properties: status: example: "409" scim\_error: description: Internal Error content: application/scim+json: schema: allOf: - $ref: "#/components/schemas/scim\_error" - properties: status: example: "500" scim\_get\_service\_provider\_config\_resp: description: "" content: application/scim+json: schema: $ref: "#/components/schemas/scim\_service\_provider\_config" scim\_get\_resource\_types\_resp: description: "" content: application/scim+json: schema: type: object properties: schemas: type: array items: type: string example: urn:ietf:params:scim:api:messages:2.0:ListResponse totalResults: type: integer example: 1 resources: type: array items: $ref: "#/components/schemas/scim\_resource\_type" scim\_get\_resource\_type\_resp: description: "" content: application/scim+json: schema: $ref: "#/components/schemas/scim\_resource\_type" scim\_get\_schemas\_resp: description: "" content: application/scim+json: schema: type: object properties: schemas: type: array items: type: string example: urn:ietf:params:scim:api:messages:2.0:ListResponse totalResults: type: integer example: 1 resources: type: array items: $ref: "#/components/schemas/scim\_schema" scim\_get\_schema\_resp: description: "" content: application/scim+json: schema: $ref: "#/components/schemas/scim\_schema" scim\_get\_users\_resp: description: "" content: application/scim+json: schema: type: object properties: schemas: type: array items: type: string example: - urn:ietf:params:scim:api:messages:2.0:ListResponse totalResults: type: integer example: 1 startIndex: type: integer example: 1 itemsPerPage: type: integer example: 10 resources: type: array items: $ref: "#/components/schemas/scim\_user" scim\_create\_user\_resp: description: "" content: application/scim+json: schema: $ref: "#/components/schemas/scim\_user" scim\_get\_user\_resp: description: "" content: application/scim+json: schema: $ref: "#/components/schemas/scim\_user" scim\_update\_user\_resp: description: "" content: application/scim+json: schema: $ref: "#/components/schemas/scim\_user" update\_repository\_immutable\_tags\_response: description: "" content: application/json: schema: $ref: "#/components/schemas/repository\_info" immutable\_tags\_verify\_response: description: "" content: application/json: schema: $ref: "#/components/schemas/immutable\_tags\_verify\_response" schemas: update\_repository\_immutable\_tags\_request: type: object properties: immutable\_tags: type: boolean description: Whether immutable tags are enabled immutable\_tags\_rules: type: array items: type: string description: List of immutable tag rules example: - "v.\*" - ".\*-RELEASE" required: - immutable\_tags - immutable\_tags\_rules repo\_creation\_request: type: object required: - name - namespace properties: name: type: string description: | The name of the repository. Must be 2-255 characters long and may only include alphanumeric characters, periods (.), underscores (\_), or hyphens (-). Letters must be lowercase. minLength: 2 maxLength: 255 pattern: "^\[a-z0-9]+(?:\[.\_-]\[a-z0-9]+)\*$" example: "my-app" namespace: type: string description: The namespace where the repository will be created example: "myorganization" description: type: string description: Short description of the repository maxLength: 100 example: "A sample application repository" full\_description: type: string description: Detailed description of the repository maxLength: 25000 example: "This is a comprehensive description of my application repository that contains additional details about the project, its purpose, usage instructions, and other relevant information." registry: type: string description: The registry where the repository will be hosted example: "docker.io" is\_private: type: boolean description: Whether the repository should be private default: false example: false RepositoryGroupCreationRequest: type: object required: - group\_id - permission properties: group\_id: type: integer format: int64 description: The ID of the organization group to grant access to example: 12345 permission: type: string description: | The permission level to grant to the group: - read: Can view and pull from the repository - write: Can view, pull, and push to the repository - admin: Can view, pull, push, and manage repository settings enum: \["read", "write", "admin"] example: "write" RepositoryGroup: type: object properties: group\_name: type: string description: The name of the group example: "developers" permission: type: string description: The permission level granted to the group enum: \["read", "write", "admin"] example: "write" group\_id: type: integer format: int64 description: The ID of the group example: 12345 repository\_info: type: object properties: user: type: string description: Username of the repository owner name: type: string description: Repository name namespace: type: string description: Repository namespace repository\_type: type: string nullable: true description: Type of the repository status: type: integer description: Repository status code status\_description: type: string description: Description of the repository status description: type: string description: Short description of the repository is\_private: type: boolean description: Whether the repository is private is\_automated: type: boolean description: Whether the repository has automated builds star\_count: type: integer format: int64 description: Number of stars pull\_count: type: integer format: int64 description: Number of pulls last\_updated: type: string format: date-time example: "2021-01-05T21:06:53.506400Z" description: ISO 8601 timestamp of when repository was last updated last\_modified: type: string format: date-time example: "2021-01-05T21:06:53.506400Z" nullable: true description: ISO 8601 timestamp of when repository was last modified date\_registered: type: string format: date-time example: "2021-01-05T21:06:53.506400Z" description: ISO 8601 timestamp of when repository was created collaborator\_count: type: integer format: int64 description: Number of collaborators affiliation: type: string nullable: true description: Repository affiliation hub\_user: type: string nullable: true description: Hub user information has\_starred: type: boolean description: Whether the current user has starred this repository full\_description: type: string nullable: true description: Full description of the repository permissions: $ref: "#/components/schemas/repo\_permissions" media\_types: type: array items: type: string nullable: true description: Supported media types content\_types: type: array items: type: string description: Supported content types categories: type: array items: $ref: "#/components/schemas/category" description: Repository categories immutable\_tags\_settings: $ref: "#/components/schemas/immutable\_tags\_settings" storage\_size: type: integer format: int64 nullable: true description: Storage size in bytes source: type: string nullable: true description: Source of the repository, where it was created from required: - user - name - namespace - status - status\_description - description - is\_private - is\_automated - star\_count - pull\_count - last\_updated - date\_registered - collaborator\_count - has\_starred - permissions - media\_types - content\_types - categories - immutable\_tags\_settings repo\_permissions: type: object properties: read: type: boolean description: Read permission write: type: boolean description: Write permission admin: type: boolean description: Admin permission required: - read - write - admin immutable\_tags\_settings: type: object properties: enabled: type: boolean description: Whether immutable tags are enabled rules: type: array items: type: string description: List of immutable tag rules required: - enabled - rules immutable\_tags\_verify\_request: type: object properties: regex: type: string pattern: '^\[a-z0-9]+((\\\\.|\_|\_\_|-+)\[a-z0-9]+)\*(\\\\/\[a-z0-9]+((\\\\.|\_|\_\_|-+)\[a-z0-9]+)\*)\*$' description: 'Immutable tags rule regex pattern. Must match format: \[a-z0-9]+((\\\\.|\_|\_\_|-+)\[a-z0-9]+)\*(\\\\/\[a-z0-9]+((\\\\.|\_|\_\_|-+)\[a-z0-9]+)\*)\*' example: "v.\*" required: - regex immutable\_tags\_verify\_response: type: object properties: tags: type: array items: type: string description: List of tags that match the provided regex pattern example: - "v1.0.0" - "v2.1.3" - "latest" required: - tags repository\_list\_entry: type: object properties: name: type: string description: Name of the repository example: "hello-world" namespace: type: string description: Namespace (organization or username) that owns the repository example: "docker" repository\_type: type: string description: Type of repository enum: - image - plugin - null example: "image" nullable: true status: type: integer description: Repository status code example: 1 status\_description: type: string description: Human-readable repository status enum: - active - inactive example: "active" description: type: string description: Repository description nullable: true example: "Hello World! (an example of minimal Dockerization)" is\_private: type: boolean description: Whether the repository is private example: false star\_count: type: integer description: Number of users who starred this repository minimum: 0 example: 1234 pull\_count: type: integer description: Total number of pulls for this repository minimum: 0 example: 50000000 last\_updated: type: string format: date-time description: ISO 8601 timestamp of when the repository was last updated example: "2023-12-01T10:30:00Z" nullable: true last\_modified: type: string format: date-time description: ISO 8601 timestamp of when the repository was last modified example: "2023-12-01T10:30:00Z" nullable: true date\_registered: type: string format: date-time description: ISO 8601 timestamp of when the repository was created example: "2013-06-19T19:07:54Z" affiliation: type: string description: User's affiliation with the repository (empty string if no affiliation) example: "" media\_types: type: array description: Media types supported by this repository items: type: string example: - "application/vnd.docker.plugin.v1+json" content\_types: type: array description: Content types supported by this repository items: type: string example: - "plugin" categories: type: array description: Categories associated with this repository items: $ref: "#/components/schemas/category" example: \[] storage\_size: type: integer description: Storage size in bytes used by this repository minimum: 0 example: 232719127 category: type: object required: - name - slug properties: name: type: string description: Human-readable name of the category example: "Databases" minLength: 1 slug: type: string description: URL-friendly identifier for the category example: "databases" minLength: 1 pattern: "^\[a-z0-9]+(?:-\[a-z0-9]+)\*$" description: Repository category for classification and discovery list\_repositories\_response: allOf: - $ref: "#/components/schemas/page" - type: object properties: results: type: array items: $ref: "#/components/schemas/repository\_list\_entry" UsersLoginRequest: description: User login details type: object required: - username - password properties: username: description: The username of the Docker Hub account to authenticate with. type: string example: myusername password: description: | The password or personal access token (PAT) of the Docker Hub account to authenticate with. type: string example: p\@ssw0rd AuthCreateTokenResponse: description: successful access token response type: object properties: access\_token: description: The created access token. This expires in 10 minutes. type: string example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c PostUsersLoginSuccessResponse: description: successful user login response type: object properties: token: description: | Created authentication token. This token can be used in the HTTP Authorization header as a JWT to authenticate with the Docker Hub APIs. type: string example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c nullable: false PostUsersLoginErrorResponse: description: failed user login response or second factor required type: object required: - detail properties: detail: description: Description of the error. type: string example: Incorrect authentication credentials nullable: false login\_2fa\_token: description: | Short time lived token to be used on \`/v2/users/2fa-login\` to complete the authentication. This field is present only if 2FA is enabled. type: string example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c nullable: true Users2FALoginRequest: description: Second factor user login details type: object required: - login\_2fa\_token - code properties: login\_2fa\_token: description: The intermediate 2FA token returned from \`/v2/users/login\` API. type: string example: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV\_adQssw5c code: description: | The Time-based One-Time Password of the Docker Hub account to authenticate with. type: string example: 123456 PostUsers2FALoginErrorResponse: description: failed second factor login response. type: object properties: detail: description: Description of the error. type: string example: Incorrect authentication credentials nullable: false protobufAny: type: object properties: type\_url: type: string value: type: string format: byte rpcStatus: type: object properties: code: type: integer format: int32 message: type: string details: type: array items: $ref: "#/components/schemas/protobufAny" AuditLogAction: type: object properties: name: type: string description: Name of audit log action. description: type: string description: Description of audit log action. label: type: string description: Label for audit log action. description: Audit Log action AuditLogActions: type: object properties: actions: type: array items: $ref: "#/components/schemas/AuditLogAction" description: List of audit log actions. label: type: string description: Grouping label for a particular set of audit log actions. GetAuditActionsResponse: type: object properties: actions: type: object additionalProperties: $ref: "#/components/schemas/AuditLogActions" description: Map of audit log actions. description: GetAuditActions response. GetAuditLogsResponse: type: object properties: logs: type: array items: $ref: "#/components/schemas/AuditLog" description: List of audit log events. description: GetAuditLogs response. AuditLog: type: object properties: account: type: string action: type: string name: type: string actor: type: string data: type: object additionalProperties: type: string timestamp: type: string format: date-time action\_description: type: string description: Audit log event. ValueError: type: object description: Used to error if input validation fails. properties: fields: type: object items: type: string text: type: string Error: type: object properties: detail: type: string message: type: string accessToken: type: object properties: uuid: type: string example: b30bbf97-506c-4ecd-aabc-842f3cb484fb client\_id: type: string example: HUB creator\_ip: type: string example: 127.0.0.1 creator\_ua: type: string example: some user agent created\_at: type: string example: "2021-07-20T12:00:00.000000Z" last\_used: type: string example: null nullable: true generated\_by: type: string example: manual is\_active: type: boolean example: true token: type: string example: a7a5ef25-8889-43a0-8cc7-f2a94268e861 token\_label: type: string example: My read only token scopes: type: array example: - repo:read items: type: string expires\_at: type: string format: date-time example: "2021-10-28T18:30:19.520861Z" createAccessTokenRequest: type: object required: - token\_label - scopes properties: token\_label: type: string description: Friendly name for you to identify the token. example: My read only token minLength: 1 maxLength: 100 scopes: type: array description: | Valid scopes: "repo:admin", "repo:write", "repo:read", "repo:public\_read" example: - repo:read items: type: string expires\_at: type: string description: | Optional expiration date for the token. If omitted, the token will remain valid indefinitely. format: date-time example: "2021-10-28T18:30:19.520861Z" createAccessTokensResponse: $ref: "#/components/schemas/accessToken" getAccessTokensResponse: type: object properties: count: type: number example: 1 next: type: string example: null previous: type: string example: null active\_count: type: number example: 1 results: type: array items: allOf: - $ref: "#/components/schemas/accessToken" - type: object properties: token: type: string example: "" patchAccessTokenRequest: type: object properties: token\_label: type: string example: My read only token minLength: 1 maxLength: 100 is\_active: type: boolean example: false patchAccessTokenResponse: $ref: "#/components/schemas/accessToken" orgSettings: type: object properties: restricted\_images: $ref: "#/components/schemas/restricted\_images" restricted\_images: type: object properties: enabled: type: boolean description: Whether or not to restrict image usage for users in the organization. example: true allow\_official\_images: type: boolean description: Allow usage of official images if "enabled" is \`true\`. example: true allow\_verified\_publishers: type: boolean description: Allow usage of verified publisher images if "enabled" is \`true\`. example: true layer: type: object properties: digest: type: string description: image layer digest nullable: true size: type: integer description: size of the layer instruction: type: string description: Dockerfile instruction image: type: object properties: architecture: type: string description: CPU architecture features: type: string description: CPU features variant: type: string description: CPU variant digest: type: string description: image digest nullable: true layers: type: array items: $ref: "#/components/schemas/layer" os: type: string description: operating system os\_features: type: string description: OS features os\_version: type: string description: OS version size: type: integer description: size of the image status: type: string enum: - active - inactive description: Status of the image last\_pulled: type: string example: "2021-01-05T21:06:53.506400Z" description: datetime of last pull nullable: true last\_pushed: type: string example: "2021-01-05T21:06:53.506400Z" description: datetime of last push nullable: true tag: type: object properties: id: type: integer description: tag ID images: type: object $ref: "#/components/schemas/image" creator: type: integer description: ID of the user that pushed the tag last\_updated: type: string example: "2021-01-05T21:06:53.506400Z" description: datetime of last update nullable: true last\_updater: type: integer description: ID of the last user that updated the tag last\_updater\_username: type: string description: Hub username of the user that updated the tag name: type: string description: name of the tag repository: type: integer description: repository ID full\_size: type: integer description: compressed size (sum of all layers) of the tagged image v2: type: string description: repository API version status: type: string enum: - active - inactive description: whether a tag has been pushed to or pulled in the past month tag\_last\_pulled: type: string example: "2021-01-05T21:06:53.506400Z" description: datetime of last pull nullable: true tag\_last\_pushed: type: string example: "2021-01-05T21:06:53.506400Z" description: datetime of last push nullable: true paginated\_tags: allOf: - $ref: "#/components/schemas/page" - type: object properties: results: type: array items: $ref: "#/components/schemas/tag" page: type: object properties: count: type: integer description: total number of results available across all pages next: type: string description: link to next page of results if any nullable: true previous: type: string description: link to previous page of results if any nullable: true scim\_schema\_attribute: type: object properties: name: type: string example: userName type: enum: - string - boolean - complex type: string example: string multiValued: type: boolean example: false description: type: string example: Unique identifier for the User, typically used by the user to directly authenticate to the service provider. Each User MUST include a non-empty userName value. This identifier MUST be unique across the service provider's entire set of Users. required: type: boolean example: true caseExact: type: boolean example: false mutability: type: string example: readWrite returned: type: string example: default uniqueness: type: string example: server scim\_schema\_parent\_attribute: allOf: - $ref: "#/components/schemas/scim\_schema\_attribute" - type: object properties: subAttributes: type: array items: $ref: "#/components/schemas/scim\_schema\_attribute" invite: type: object properties: id: type: string description: uuid representing the invite id example: e36eca69-4cc8-4f17-9845-ae8c2b832691 inviter\_username: type: string example: moby invitee: type: string description: can either be a dockerID for registered users or an email for non-registered users example: invitee\@docker.com org: type: string description: name of the org to join example: docker team: type: string description: name of the team (user group) to join example: owners created\_at: type: string example: "2021-10-28T18:30:19.520861Z" bulk\_invite: type: object properties: invitees: type: array description: A list of invitees items: type: object properties: invitee: type: string description: invitee email or Docker ID status: type: string description: status of the invite or validation error invite: description: Invite data if successfully invited $ref: "#/components/schemas/invite" example: invitees: - invitee: invitee\@docker.com status: invited invite: id: e36eca69-4cc8-4f17-9845-ae8c2b832691 inviter\_username: moby invitee: invitee\@docker.com org: docker team: owners created\_at: "2021-10-28T18:30:19.520861Z" - invitee: invitee2\@docker.com status: existing\_org\_member - invitee: invitee3\@docker.com status: invalid\_email\_or\_docker\_id error: type: object properties: errinfo: type: object items: type: string detail: type: string message: type: string scim\_error: type: object properties: status: type: string description: The status code for the response in string format. schemas: type: array items: type: string default: urn:ietf:params:scim:api:messages:2.0:Error detail: type: string description: Details about why the request failed. user: type: object properties: id: type: string example: 0ab70deb065a43fcacd55d48caa945d8 description: The UUID trimmed company: type: string example: Docker Inc date\_joined: type: string example: "2021-01-05T21:06:53.506400Z" full\_name: type: string example: Jon Snow gravatar\_email: type: string gravatar\_url: type: string location: type: string profile\_url: type: string type: type: string enum: - User - Org example: User username: type: string example: dockeruser org\_member: allOf: - $ref: "#/components/schemas/user" properties: email: type: string description: User's email address example: example\@docker.com role: type: string description: User's role in the Organization enum: - Owner - Member - Invitee example: Owner groups: type: array description: Groups (Teams) that the user is member of items: type: string example: - developers - owners is\_guest: type: boolean description: If the organization has verified domains, members that have email addresses outside of those domains will be flagged as guests. example: false primary\_email: type: string description: The user's email primary address. example: example\@docker.com deprecated: true last\_logged\_in\_at: type: string format: date-time description: | Last time the user logged in. To access this field, you must have insights visible for your organization. See \[Insights]\(https\://docs.docker.com/admin/insights/#view-insights-for-organization-users). example: "2021-01-05T21:06:53.506400Z" last\_seen\_at: type: string format: date-time description: | Last time the user was seen. To access this field, you must have insights visible for your organization. See \[Insights]\(https\://docs.docker.com/admin/insights/#view-insights-for-organization-users). example: "2021-01-05T21:06:53.506400Z" last\_desktop\_version: type: string description: | Last desktop version the user used. To access this field, you must have insights visible for your organization. See \[Insights]\(https\://docs.docker.com/admin/insights/#view-insights-for-organization-users). example: 4.29.0 org\_member\_paginated: type: object properties: count: type: number description: The total number of items that match with the search. example: 120 previous: type: string description: The URL or link for the previous page of items. example: https\://hub.docker.com/v2/some/resources/items?page=1\&page\_size=20 next: type: string description: The URL or link for the next page of items. example: https\://hub.docker.com/v2/some/resources/items?page=3\&page\_size=20 results: type: array description: List of accounts. items: $ref: "#/components/schemas/org\_member" org\_group: type: object properties: id: type: number example: 10 description: Group ID uuid: type: string description: UUID for the group name: type: string example: mygroup description: Name of the group description: type: string example: Groups description description: Description of the group member\_count: type: number example: 10 description: Member count of the group group\_member: type: object properties: id: type: string example: 0ab70deb065a43fcacd55d48caa945d8 description: The UUID trimmed company: type: string example: Docker Inc date\_joined: type: string format: date-time example: "2021-01-05T21:06:53.506400Z" full\_name: type: string example: John Snow gravatar\_email: type: string gravatar\_url: type: string location: type: string profile\_url: type: string type: type: string enum: - User - Org example: User username: type: string example: dockeruser email: type: string example: dockeruser\@docker.com email\_address: type: object properties: id: type: number user\_id: type: number email: type: string example: dockeruser\@docker.com verified: type: boolean primary: type: boolean legacy\_email\_address: allOf: - $ref: "#/components/schemas/email\_address" - type: object properties: user: type: string example: dockeruser email\_with\_username: allOf: - $ref: "#/components/schemas/email\_address" - type: object properties: username: type: string example: dockeruser scim\_service\_provider\_config: type: object properties: schemas: type: array items: type: string example: - urn:ietf:params:scim:schemas:core:2.0:ServiceProviderConfig documentationUri: type: string example: "" patch: properties: supported: type: boolean example: false bulk: type: object properties: supported: type: boolean example: false maxOperations: type: integer maxPayloadSize: type: integer filter: type: object properties: supported: type: boolean example: true maxResults: type: integer example: 99999 changePassword: type: object properties: supported: type: boolean example: false sort: type: object properties: supported: type: boolean example: true etag: type: object properties: supported: type: boolean example: false authenticationSchemes: type: object properties: name: type: string example: OAuth 2.0 Bearer Token description: type: string example: The OAuth 2.0 Bearer Token Authentication scheme. OAuth enables clients to access protected resources by obtaining an access token, which is defined in RFC 6750 as "a string representing an access authorization issued to the client", rather than using the resource owner's credentials directly. specUri: type: string example: http\://tools.ietf.org/html/rfc6750 type: type: string example: oauthbearertoken scim\_resource\_type: type: object properties: schemas: type: array items: type: string example: - urn:ietf:params:scim:schemas:core:2.0:ResourceType id: type: string example: User name: type: string example: User description: type: string example: User endpoint: type: string example: /Users schema: type: string example: urn:ietf:params:scim:schemas:core:2.0:User scim\_schema: type: object properties: schemas: type: array items: type: string example: - urn:ietf:params:scim:schemas:core:2.0:Schema id: type: string example: urn:ietf:params:scim:schemas:core:2.0:User name: type: string example: User description: type: string example: User Account attributes: type: array example: \[] items: $ref: "#/components/schemas/scim\_schema\_parent\_attribute" scim\_email: type: object properties: value: type: string example: jon.snow\@docker.com display: type: string example: jon.snow\@docker.com primary: type: boolean example: true scim\_group: type: object properties: value: type: string example: nightswatch display: type: string example: nightswatch scim\_user\_username: type: string description: The user's email address. This must be reachable via email. example: jon.snow\@docker.com scim\_user\_name: type: object properties: givenName: type: string example: Jon familyName: type: string example: Snow scim\_user\_display\_name: type: string description: The username in Docker. Also known as the "Docker ID". example: jonsnow scim\_user\_schemas: type: array items: type: string example: urn:ietf:params:scim:schemas:core:2.0:User minItems: 1 scim\_user\_id: type: string example: d80f7c79-7730-49d8-9a41-7c42fb622d9c description: The unique identifier for the user. A v4 UUID. scim\_user: type: object properties: schemas: $ref: "#/components/schemas/scim\_user\_schemas" id: $ref: "#/components/schemas/scim\_user\_id" userName: $ref: "#/components/schemas/scim\_user\_username" name: $ref: "#/components/schemas/scim\_user\_name" displayName: $ref: "#/components/schemas/scim\_user\_display\_name" active: type: boolean example: true emails: type: array items: $ref: "#/components/schemas/scim\_email" groups: type: array items: $ref: "#/components/schemas/scim\_group" meta: type: object properties: resourceType: type: string example: User location: type: string example: https\://hub.docker.com/v2/scim/2.0/Users/d80f7c79-7730-49d8-9a41-7c42fb622d9c created: type: string format: date-time description: The creation date for the user as a RFC3339 formatted string. example: "2022-05-20T00:54:18Z" lastModified: type: string format: date-time description: The date the user was last modified as a RFC3339 formatted string. example: "2022-05-20T00:54:18Z" orgAccessToken: type: object properties: id: type: string example: "a7a5ef25-8889-43a0-8cc7-f2a94268e861" label: type: string example: "My organization token" created\_by: type: string example: "johndoe" is\_active: type: boolean example: true created\_at: type: string format: date-time example: "2022-05-20T00:54:18Z" expires\_at: type: string format: date-time example: "2023-05-20T00:54:18Z" nullable: true last\_used\_at: type: string format: date-time example: "2022-06-15T12:30:45Z" nullable: true orgAccessTokenResource: type: object properties: type: type: string enum: - TYPE\_REPO - TYPE\_ORG example: "TYPE\_REPO" description: The type of resource required: true path: type: string example: "myorg/myrepo" description: | The path of the resource. The format of this will change depending on the type of resource. For TYPE\_REPO resources: - Must be an existing repository name (e.g., "myorg/myrepo") - Can use glob patterns (e.g., "myorg/\*" for all repositories in the organization) - Use "\*/\*/public" to reference all public repositories required: true scopes: type: array description: The scopes this token has access to items: type: string example: "scope-image-pull" required: true getOrgAccessTokensResponse: type: object properties: total: type: number example: 10 next: type: string example: https\://hub.docker.com/v2/orgs/docker/access-tokens?page=2\&page\_size=10 previous: type: string example: https\://hub.docker.com/v2/orgs/docker/access-tokens?page=1\&page\_size=10 results: type: array items: $ref: "#/components/schemas/orgAccessToken" getOrgAccessTokenResponse: allOf: - $ref: "#/components/schemas/orgAccessToken" - type: object properties: resources: type: array description: Resources this token has access to items: $ref: "#/components/schemas/orgAccessTokenResource" createOrgAccessTokenRequest: type: object properties: label: type: string description: Label for the access token example: "My organization token" required: true description: type: string description: Description of the access token example: "Token for CI/CD pipeline" resources: type: array description: Resources this token has access to items: $ref: "#/components/schemas/orgAccessTokenResource" expires\_at: type: string format: date-time description: Expiration date for the token example: "2023-05-20T00:54:18Z" nullable: true createOrgAccessTokenResponse: type: object allOf: - type: object properties: id: type: string example: "a7a5ef25-8889-43a0-8cc7-f2a94268e861" label: type: string example: "My organization token" is\_active: type: boolean example: true created\_at: type: string format: date-time example: "2022-05-20T00:54:18Z" expires\_at: type: string format: date-time example: "2023-05-20T00:54:18Z" nullable: true last\_used\_at: type: string format: date-time example: "2022-06-15T12:30:45Z" nullable: true - type: object properties: token: type: string description: The actual token value that can be used for authentication example: "dckr\_oat\_7awgM4jG5SQvxcvmNzhKj8PQjxo" resources: type: array items: $ref: "#/components/schemas/orgAccessTokenResource" updateOrgAccessTokenRequest: type: object properties: label: type: string description: Label for the access token example: "My organization token" description: type: string description: Description of the access token example: "Token for CI/CD pipeline" resources: type: array description: Resources this token has access to items: $ref: "#/components/schemas/orgAccessTokenResource" is\_active: type: boolean description: Whether the token is active example: true updateOrgAccessTokenResponse: type: object allOf: - $ref: "#/components/schemas/orgAccessToken" - type: object properties: resources: type: array description: Resources this token has access to items: $ref: "#/components/schemas/orgAccessTokenResource" team\_repo: allOf: - $ref: "#/components/responses/team\_repo" properties: group\_name: type: string description: Name of the group permission: type: string description: Repo access permission enum: - read - write - admin parameters: namespace: in: path name: namespace required: true schema: type: string repository: in: path name: repository required: true schema: type: string tag: in: path name: tag required: true schema: type: string org\_name: in: path name: org\_name description: Name of the organization (namespace). schema: type: string example: myorganization required: true group\_name: in: path name: group\_name description: Name of the group (team) in the organization. schema: type: string example: developers required: true username: in: path name: username description: Username, identifier for the user (namespace, DockerID). schema: type: string example: jonsnow required: true page: in: query name: page description: Page number (starts on 1). schema: type: integer page\_size: in: query name: page\_size description: Number of items (rows) per page. schema: type: integer invites: in: query name: invites description: Include invites in the response. schema: type: boolean search: in: query name: search schema: type: integer description: Search term. scim\_attributes: in: query name: attributes schema: type: string description: Comma delimited list of attributes to limit to in the response. example: userName,displayName scim\_user\_id: name: id in: path schema: type: string description: The user ID. example: d80f7c79-7730-49d8-9a41-7c42fb622d9c required: true type: in: query name: type schema: type: string enum: - all - invitee - member example: all role: in: query name: role schema: type: string enum: - owner - editor - member example: owner bulk\_invite: in: header name: X-Analytics-Client-Feature description: Optional string that indicates the feature used to submit the bulk invites (e.g.'file', 'web') schema: type: string requestBodies: bulk\_invite\_request: required: true content: application/json: schema: type: object required: - org - invitees properties: org: type: string description: organization name example: docker team: type: string description: team name example: owners role: type: string description: role for invitees example: member invitees: type: array description: list of invitees emails or Docker Ids items: type: string description: invitee email or Docker ID example: - invitee1DockerId - invitee2\@docker.com - invitee3\@docker.com dry\_run: type: boolean description: Optional, run through validation but don't actually change data. example: true scim\_create\_user\_request: required: true content: application/scim+json: schema: type: object required: - schemas - userName properties: schemas: $ref: "#/components/schemas/scim\_user\_schemas" userName: $ref: "#/components/schemas/scim\_user\_username" name: $ref: "#/components/schemas/scim\_user\_name" scim\_update\_user\_request: required: true content: application/scim+json: schema: type: object required: - schemas properties: schemas: $ref: "#/components/schemas/scim\_user\_schemas" name: allOf: - $ref: "#/components/schemas/scim\_user\_name" - description: If this is omitted from the request, the update will skip the update on it. We will only ever change the name, but not clear it. enabled: type: boolean default: false description: If this is omitted from the request, it will default to false resulting in a deactivated user. add\_member\_to\_org\_group: required: true content: application/json: schema: type: object required: - member properties: member: type: string example: jonsnow update\_repository\_immutable\_tags\_request: required: true content: application/json: schema: $ref: "#/components/schemas/update\_repository\_immutable\_tags\_request" immutable\_tags\_verify\_request: required: true content: application/json: schema: $ref: "#/components/schemas/immutable\_tags\_verify\_request" securitySchemes: bearerAuth: type: http scheme: bearer bearerFormat: JWT bearerSCIMAuth: type: http scheme: bearer x-tagGroups: - name: General tags: - changelog - resources - rate-limiting - authentication - name: API tags: - authentication-api - access-tokens - images - audit-logs - org-settings - repositories - scim - orgs - org-access-tokens - groups - invites

----
url: https://docs.docker.com/reference/cli/docker/mcp/profile/export/
----

# docker mcp profile export

***

| Description | Export profile to file                                 |
| ----------- | ------------------------------------------------------ |
| Usage       | `docker mcp profile export <profile-id> <output-file>` |

## [Description](#description)

Export profile to file

----
url: https://docs.docker.com/reference/build-checks/consistent-instruction-casing/
----

# ConsistentInstructionCasing

***

Table of contents

***

## [Output](#output)

```text
Command 'EntryPoint' should be consistently cased
```

## [Description](#description)

Instruction keywords should use consistent casing (all lowercase or all uppercase). Using a case that mixes uppercase and lowercase, such as `PascalCase` or `snakeCase`, letters result in poor readability.

## [Examples](#examples)

❌ Bad: don't mix uppercase and lowercase.

```dockerfile
From alpine
Run echo hello > /greeting.txt
EntRYpOiNT ["cat", "/greeting.txt"]
```

✅ Good: all uppercase.

```dockerfile
FROM alpine
RUN echo hello > /greeting.txt
ENTRYPOINT ["cat", "/greeting.txt"]
```

✅ Good: all lowercase.

```dockerfile
from alpine
run echo hello > /greeting.txt
entrypoint ["cat", "/greeting.txt"]
```

----
url: https://docs.docker.com/reference/compose-file/services/
----

# Define services in Docker Compose

***

Table of contents

***

A service is an abstract definition of a computing resource within an application which can be scaled or replaced independently from other components. Services are backed by a set of containers, run by the platform according to replication requirements and placement constraints. As services are backed by containers, they are defined by a Docker image and set of runtime arguments. All containers within a service are identically created with these arguments.

A Compose file must declare a `services` top-level element as a map whose keys are string representations of service names, and whose values are service definitions. A service definition contains the configuration that is applied to each service container.

Each service may also include a `build` section, which defines how to create the Docker image for the service. Compose supports building Docker images using this service definition. If not used, the `build` section is ignored and the Compose file is still considered valid. Build support is an optional aspect of the Compose Specification, and is described in detail in the [Compose Build Specification](https://docs.docker.com/reference/compose-file/build/) documentation.

Each service defines runtime constraints and requirements to run its containers. The `deploy` section groups these constraints and lets the platform adjust the deployment strategy to best match containers' needs with available resources. Deploy support is an optional aspect of the Compose Specification, and is described in detail in the [Compose Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/) documentation. If not implemented the `deploy` section is ignored and the Compose file is still considered valid.

## [Examples](#examples)

### [Simple example](#simple-example)

The following example demonstrates how to define two simple services, set their images, map ports, and configure basic environment variables using Docker Compose.

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8080:80"

  db:
    image: postgres:18
    environment:
      POSTGRES_USER: example
      POSTGRES_DB: exampledb
```

### [Advanced example](#advanced-example)

In the following example, the `proxy` service uses the Nginx image, mounts a local Nginx configuration file into the container, exposes port `80` and depends on the `backend` service.

The `backend` service builds an image from the Dockerfile located in the `backend` directory that is set to build at stage `builder`.

```yaml
services:
  proxy:
    image: nginx
    volumes:
      - type: bind
        source: ./proxy/nginx.conf
        target: /etc/nginx/conf.d/default.conf
        read_only: true
    ports:
      - 80:80
    depends_on:
      - backend

  backend:
    build:
      context: backend
      target: builder
```

For more example Compose files, explore the [Awesome Compose samples](https://github.com/docker/awesome-compose).

## [Attributes](#attributes)

### [`annotations`](#annotations)

`annotations` defines annotations for the container. `annotations` can use either an array or a map.

```yml
annotations:
  com.example.foo: bar
```

```yml
annotations:
  - com.example.foo=bar
```

### [`attach`](#attach)

Requires: Docker Compose [2.20.0](https://github.com/docker/compose/releases/tag/v2.20.0) and later

When `attach` is defined and set to `false` Compose does not collect service logs, until you explicitly request it to.

The default service configuration is `attach: true`.

### [`build`](#build)

`build` specifies the build configuration for creating a container image from source, as defined in the [Compose Build Specification](https://docs.docker.com/reference/compose-file/build/).

### [`blkio_config`](#blkio_config)

`blkio_config` defines a set of configuration options to set block I/O limits for a service.

```yml
services:
  foo:
    image: busybox
    blkio_config:
       weight: 300
       weight_device:
         - path: /dev/sda
           weight: 400
       device_read_bps:
         - path: /dev/sdb
           rate: '12mb'
       device_read_iops:
         - path: /dev/sdb
           rate: 120
       device_write_bps:
         - path: /dev/sdb
           rate: '1024k'
       device_write_iops:
         - path: /dev/sdb
           rate: 30
```

#### [`device_read_bps`, `device_write_bps`](#device_read_bps-device_write_bps)

Set a limit in bytes per second for read / write operations on a given device. Each item in the list must have two keys:

* `path`: Defines the symbolic path to the affected device.
* `rate`: Either as an integer value representing the number of bytes or as a string expressing a byte value.

#### [`device_read_iops`, `device_write_iops`](#device_read_iops-device_write_iops)

Set a limit in operations per second for read / write operations on a given device. Each item in the list must have two keys:

* `path`: Defines the symbolic path to the affected device.
* `rate`: As an integer value representing the permitted number of operations per second.

#### [`weight`](#weight)

Modify the proportion of bandwidth allocated to a service relative to other services. Takes an integer value between 10 and 1000, with 500 being the default.

#### [`weight_device`](#weight_device)

Fine-tune bandwidth allocation by device. Each item in the list must have two keys:

* `path`: Defines the symbolic path to the affected device.
* `weight`: An integer value between 10 and 1000.

### [`cpu_count`](#cpu_count)

`cpu_count` defines the number of usable CPUs for service container.

### [`cpu_percent`](#cpu_percent)

`cpu_percent` defines the usable percentage of the available CPUs.

### [`cpu_shares`](#cpu_shares)

`cpu_shares` defines, as integer value, a service container's relative CPU weight versus other containers.

### [`cpu_period`](#cpu_period)

`cpu_period` configures CPU CFS (Completely Fair Scheduler) period when a platform is based on Linux kernel.

### [`cpu_quota`](#cpu_quota)

`cpu_quota` configures CPU CFS (Completely Fair Scheduler) quota when a platform is based on Linux kernel.

### [`cpu_rt_runtime`](#cpu_rt_runtime)

`cpu_rt_runtime` configures CPU allocation parameters for platforms with support for real-time scheduler. It can be either an integer value using microseconds as unit or a [duration](https://docs.docker.com/reference/compose-file/extension/#specifying-durations).

```yml
 cpu_rt_runtime: '400ms'
 cpu_rt_runtime: '95000'
```

### [`cpu_rt_period`](#cpu_rt_period)

`cpu_rt_period` configures CPU allocation parameters for platforms with support for real-time scheduler. It can be either an integer value using microseconds as unit or a [duration](https://docs.docker.com/reference/compose-file/extension/#specifying-durations).

```yml
 cpu_rt_period: '1400us'
 cpu_rt_period: '11000'
```

### [`cpus`](#cpus)

`cpus` define the number of (potentially virtual) CPUs to allocate to service containers. This is a fractional number. `0.000` means no limit.

When set, `cpus` must be consistent with the `cpus` attribute in the [Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#cpus).

### [`cpuset`](#cpuset)

`cpuset` defines the explicit CPUs in which to permit execution. Can be a range `0-3` or a list `0,1`

### [`cap_add`](#cap_add)

`cap_add` specifies additional container [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) as strings.

```yaml
cap_add:
  - ALL
```

### [`cap_drop`](#cap_drop)

`cap_drop` specifies container [capabilities](https://man7.org/linux/man-pages/man7/capabilities.7.html) to drop as strings.

```yaml
cap_drop:
  - NET_ADMIN
  - SYS_ADMIN
```

### [`cgroup`](#cgroup)

Requires: Docker Compose [2.15.0](https://github.com/docker/compose/releases/tag/v2.15.0) and later

`cgroup` specifies the cgroup namespace to join. When unset, it is the container runtime's decision to select which cgroup namespace to use, if supported.

* `host`: Runs the container in the Container runtime cgroup namespace.
* `private`: Runs the container in its own private cgroup namespace.

### [`cgroup_parent`](#cgroup_parent)

`cgroup_parent` specifies an optional parent [cgroup](https://man7.org/linux/man-pages/man7/cgroups.7.html) for the container.

```yaml
cgroup_parent: m-executor-abcd
```

### [`command`](#command)

`command` overrides the default command declared by the container image, for example by Dockerfile's `CMD`.

```yaml
command: bundle exec thin -p 3000
```

If the value is `null`, the default command from the image is used.

If the value is `[]` (empty list) or `''` (empty string), the default command declared by the image is ignored, or in other words overridden to be empty.

> Note
>
> Unlike the `CMD` instruction in a Dockerfile, the `command` field doesn't automatically run within the context of the [`SHELL`](https://docs.docker.com/reference/dockerfile/#shell-form) instruction defined in the image. If your `command` relies on shell-specific features, such as environment variable expansion, you need to explicitly run it within a shell. For example:
>
> ```yaml
> command: /bin/sh -c 'echo "hello $$HOSTNAME"'
> ```

The value can also be a list, similar to the [exec-form syntax](https://docs.docker.com/reference/dockerfile/#exec-form) used by the [Dockerfile](https://docs.docker.com/reference/dockerfile/#exec-form).

### [`configs`](#configs)

`configs` let services adapt their behaviour without the need to rebuild a Docker image. Services can only access configs when explicitly granted by the `configs` attribute. Two different syntax variants are supported.

Compose reports an error if `config` doesn't exist on the platform or isn't defined in the [`configs` top-level element](https://docs.docker.com/reference/compose-file/configs/) in the Compose file.

There are two syntaxes defined for configs: a short syntax and a long syntax.

You can grant a service access to multiple configs, and you can mix long and short syntax.

#### [Short syntax](#short-syntax)

The short syntax variant only specifies the config name. This grants the container access to the config and mounts it as files into a service’s container’s filesystem. The location of the mount point within the container defaults to `/<config_name>` in Linux containers, and `C:\<config-name>` in Windows containers.

The following example uses the short syntax to grant the `redis` service access to the `my_config` and `my_other_config` configs. The value of `my_config` is set to the contents of the file `./my_config.txt`, and `my_other_config` is defined as an external resource, which means that it has already been defined in the platform. If the external config does not exist, the deployment fails.

```yml
services:
  redis:
    image: redis:latest
    configs:
      - my_config
      - my_other_config
configs:
  my_config:
    file: ./my_config.txt
  my_other_config:
    external: true
```

#### [Long syntax](#long-syntax)

The long syntax provides more granularity in how the config is created within the service's task containers.

* `source`: The name of the config as it exists in the platform.
* `target`: The path and name of the file to be mounted in the service's task containers. Defaults to `/<source>` if not specified.
* `uid` and `gid`: The numeric uid or gid that owns the mounted config file within the service's task containers.
* `mode`: The [permissions](https://wintelguy.com/permissions-calc.pl) for the file that is mounted within the service's task containers, in octal notation. Default value is world-readable (`0444`). Writable bit must be ignored. The executable bit can be set.

The following example sets the name of `my_config` to `redis_config` within the container, sets the mode to `0440` (group-readable) and sets the user and group to `103`. The `redis` service does not have access to the `my_other_config` config.

```yml
services:
  redis:
    image: redis:latest
    configs:
      - source: my_config
        target: /redis_config
        uid: "103"
        gid: "103"
        mode: 0440
configs:
  my_config:
    external: true
  my_other_config:
    external: true
```

### [`container_name`](#container_name)

`container_name` is a string that specifies a custom container name, rather than a name generated by default.

```yml
container_name: my-web-container
```

Compose does not scale a service beyond one container if the Compose file specifies a `container_name`. Attempting to do so results in an error.

`container_name` follows the regex format of `[a-zA-Z0-9][a-zA-Z0-9_.-]+`

### [`credential_spec`](#credential_spec)

`credential_spec` configures the credential spec for a managed service account.

If you have services that use Windows containers, you can use `file:` and `registry:` protocols for `credential_spec`. Compose also supports additional protocols for custom use-cases.

The `credential_spec` must be in the format `file://<filename>` or `registry://<value-name>`.

```yml
credential_spec:
  file: my-credential-spec.json
```

When using `registry:`, the credential spec is read from the Windows registry on the daemon's host. A registry value with the given name must be located in:

```bash
HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Virtualization\Containers\CredentialSpecs
```

The following example loads the credential spec from a value named `my-credential-spec` in the registry:

```yml
credential_spec:
  registry: my-credential-spec
```

#### [Example gMSA configuration](#example-gmsa-configuration)

When configuring a gMSA credential spec for a service, you only need to specify a credential spec with `config`, as shown in the following example:

```yml
services:
  myservice:
    image: myimage:latest
    credential_spec:
      config: my_credential_spec

configs:
  my_credentials_spec:
    file: ./my-credential-spec.json
```

### [`depends_on`](#depends_on)

With the `depends_on` attribute, you can control the order of service startup and shutdown. It is useful if services are closely coupled, and the startup sequence impacts the application's functionality.

#### [Short syntax](#short-syntax-1)

The short syntax variant only specifies service names of the dependencies. Service dependencies cause the following behaviors:

* Compose creates services in dependency order. In the following example, `db` and `redis` are created before `web`.

* Compose removes services in dependency order. In the following example, `web` is removed before `db` and `redis`.

Simple example:

```yml
services:
  web:
    build: .
    depends_on:
      - db
      - redis
  redis:
    image: redis
  db:
    image: postgres:18
```

Compose guarantees dependency services have been started before starting a dependent service. With short syntax, Compose does not wait for dependency services to be "healthy" before starting a dependent service.

#### [Long syntax](#long-syntax-1)

The long form syntax enables the configuration of additional fields that can't be expressed in the short form.

* `restart`: When set to `true` Compose restarts this service after it updates the dependency service. This applies to an explicit restart controlled by a Compose operation, and excludes automated restart by the container runtime after the container dies. Introduced in Docker Compose version [2.17.0](https://github.com/docker/compose/releases/tag/v2.17.0).

* `condition`: Sets the condition under which dependency is considered satisfied

  * `service_started`: An equivalent of the short syntax described previously
  * `service_healthy`: Specifies that a dependency is expected to be "healthy" (as indicated by [`healthcheck`](#healthcheck)) before starting a dependent service.
  * `service_completed_successfully`: Specifies that a dependency is expected to run to successful completion before starting a dependent service.

* `required`: When set to `false` Compose only warns you when the dependency service isn't started or available. If it's not defined the default value of `required` is `true`. Introduced in Docker Compose version [2.20.0](https://github.com/docker/compose/releases/tag/v2.20.0).

Service dependencies cause the following behaviors:

* Compose creates services in dependency order. In the following example, `db` and `redis` are created before `web`.

* Compose waits for healthchecks to pass on dependencies marked with `service_healthy`. In the following example, `db` is expected to be "healthy" before `web` is created.

* Compose removes services in dependency order. In the following example, `web` is removed before `db` and `redis`.

```yml
services:
  web:
    build: .
    depends_on:
      db:
        condition: service_healthy
        restart: true
      redis:
        condition: service_started
  redis:
    image: redis
  db:
    image: postgres:18
```

Compose guarantees dependency services are started before starting a dependent service. Compose guarantees dependency services marked with `service_healthy` are "healthy" before starting a dependent service.

### [`deploy`](#deploy)

`deploy` specifies the configuration for the deployment and lifecycle of services, as defined [in the Compose Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/).

### [`develop`](#develop)

Requires: Docker Compose [2.22.0](https://github.com/docker/compose/releases/tag/v2.22.0) and later

`develop` specifies the development configuration for maintaining a container in sync with source, as defined in the [Development Section](https://docs.docker.com/reference/compose-file/develop/).

### [`device_cgroup_rules`](#device_cgroup_rules)

`device_cgroup_rules` defines a list of device cgroup rules for this container. The format is the same format the Linux kernel specifies in the [Control Groups Device Whitelist Controller](https://www.kernel.org/doc/html/latest/admin-guide/cgroup-v1/devices.html).

```yml
device_cgroup_rules:
  - 'c 1:3 mr'
  - 'a 7:* rmw'
```

### [`devices`](#devices)

`devices` defines a list of device mappings for created containers in the form of `HOST_PATH:CONTAINER_PATH[:CGROUP_PERMISSIONS]`.

```yml
devices:
  - "/dev/ttyUSB0:/dev/ttyUSB0"
  - "/dev/sda:/dev/xvda:rwm"
```

`devices` can also rely on the [CDI](https://github.com/cncf-tags/container-device-interface) syntax to let the container runtime select a device:

```yml
devices:
  - "vendor1.com/device=gpu"
```

### [`dns`](#dns)

`dns` defines custom DNS servers to set on the container network interface configuration. It can be a single value or a list.

```yml
dns: 8.8.8.8
```

```yml
dns:
  - 8.8.8.8
  - 9.9.9.9
```

### [`dns_opt`](#dns_opt)

`dns_opt` list custom DNS options to be passed to the container’s DNS resolver (`/etc/resolv.conf` file on Linux).

```yml
dns_opt:
  - use-vc
  - no-tld-query
```

### [`dns_search`](#dns_search)

`dns_search` defines custom DNS search domains to set on container network interface configuration. It can be a single value or a list.

```yml
dns_search: example.com
```

```yml
dns_search:
  - dc1.example.com
  - dc2.example.com
```

### [`domainname`](#domainname)

`domainname` declares a custom domain name to use for the service container. It must be a valid RFC 1123 hostname.

### [`driver_opts`](#driver_opts)

Requires: Docker Compose [2.27.1](https://github.com/docker/compose/releases/tag/v2.27.1) and later

`driver_opts` specifies a list of options as key-value pairs to pass to the driver. These options are driver-dependent.

```yml
services:
  app:
    networks:
      app_net:
        driver_opts:
          com.docker.network.bridge.host_binding_ipv4: "127.0.0.1"
```

Consult the [network drivers documentation](https://docs.docker.com/engine/network/) for more information.

### [`entrypoint`](#entrypoint)

`entrypoint` declares the default entrypoint for the service container. This overrides the `ENTRYPOINT` instruction from the service's Dockerfile.

If `entrypoint` is non-null, Compose ignores any default command from the image, for example the `CMD` instruction in the Dockerfile.

See also [`command`](#command) to set or override the default command to be executed by the entrypoint process.

In its short form, the value can be defined as a string:

```yml
entrypoint: /code/entrypoint.sh
```

Alternatively, the value can also be a list, in a manner similar to the [Dockerfile](https://docs.docker.com/reference/dockerfile/#cmd):

```yml
entrypoint:
  - php
  - -d
  - zend_extension=/usr/local/lib/php/extensions/no-debug-non-zts-20100525/xdebug.so
  - -d
  - memory_limit=-1
  - vendor/bin/phpunit
```

If the value is `null`, the default entrypoint from the image is used.

If the value is `[]` (empty list) or `''` (empty string), the default entrypoint declared by the image is ignored, or in other words, overridden to be empty.

### [`env_file`](#env_file)

The `env_file` attribute is used to specify one or more files that contain environment variables to be passed to the containers.

```yml
env_file: .env
```

Relative paths are resolved from the Compose file's parent folder. As absolute paths prevent the Compose file from being portable, Compose warns you when such a path is used to set `env_file`.

Environment variables declared in the [`environment`](#environment) section override these values. This holds true even if those values are empty or undefined.

`env_file` can also be a list. The files in the list are processed from the top down. For the same variable specified in two environment files, the value from the last file in the list stands.

```yml
env_file:
  - ./a.env
  - ./b.env
```

List elements can also be declared as a mapping, which then lets you set additional attributes.

#### [`required`](#required)

Requires: Docker Compose [2.24.0](https://github.com/docker/compose/releases/tag/v2.24.0) and later

The `required` attribute defaults to `true`. When `required` is set to `false` and the `.env` file is missing, Compose silently ignores the entry.

```yml
env_file:
  - path: ./default.env
    required: true # default
  - path: ./override.env
    required: false
```

#### [`format`](#format)

Requires: Docker Compose [2.30.0](https://github.com/docker/compose/releases/tag/v2.30.0) and later

The `format` attribute lets you use an alternative file format for the `env_file`. When not set, `env_file` is parsed according to the Compose rules outlined in [`Env_file` format](#env_file-format).

`raw` format lets you use an `env_file` with key=value items, but without any attempt from Compose to parse the value for interpolation. This let you pass values as-is, including quotes and `$` signs.

```yml
env_file:
  - path: ./default.env
    format: raw
```

#### [`Env_file` format](#env_file-format)

Each line in an `.env` file must be in `VAR[=[VAL]]` format. The following syntax rules apply:

* Lines beginning with `#` are processed as comments and ignored.

* Blank lines are ignored.

* Unquoted and double-quoted (`"`) values have [Interpolation](https://docs.docker.com/reference/compose-file/interpolation/) applied.

`VAL` may be omitted, in such cases the variable value is an empty string. `=VAL` may be omitted, in such cases the variable is unset.

```bash
# Set Rails/Rack environment
RACK_ENV=development
VAR="quoted"
```

### [`environment`](#environment)

The `environment` attribute defines environment variables set in the container. `environment` can use either an array or a map. Any boolean values; true, false, yes, no, should be enclosed in quotes to ensure they are not converted to True or False by the YAML parser.

Environment variables can be declared by a single key (no value to equals sign). In this case Compose relies on you to resolve the value. If the value is not resolved, the variable is unset and is removed from the service container environment.

Map syntax:

```yml
environment:
  RACK_ENV: development
  SHOW: "true"
  USER_INPUT:
```

Array syntax:

```yml
environment:
  - RACK_ENV=development
  - SHOW=true
  - USER_INPUT
```

When both `env_file` and `environment` are set for a service, values set by `environment` have precedence.

### [`expose`](#expose)

`expose` defines the (incoming) port or a range of ports that Compose exposes from the container. These ports must be accessible to linked services and should not be published to the host machine. Only the internal container ports can be specified.

Syntax is `<portnum>/[<proto>]` or `<startport-endport>/[<proto>]` for a port range. When not explicitly set, `tcp` protocol is used.

```yml
expose:
  - "3000"
  - "8000"
  - "8080-8085/tcp"
```

> Note
>
> If the Dockerfile for the image already exposes ports, it is visible to other containers on the network even if `expose` is not set in your Compose file.

### [`extends`](#extends)

`extends` lets you share common configurations among different files, or even different projects entirely. With `extends` you can define a common set of service options in one place and refer to it from anywhere. You can refer to another Compose file and select a service you want to also use in your own application, with the ability to override some attributes for your own needs.

You can use `extends` on any service together with other configuration keys. The `extends` value must be a mapping defined with a required `service` and an optional `file` key.

```yaml
extends:
  file: common.yml
  service: webapp
```

* `service`: Defines the name of the service being referenced as a base, for example `web` or `database`.
* `file`: The location of a Compose configuration file defining that service.

`extends` is not supported when deploying with `docker stack deploy`.

#### [Restrictions](#restrictions)

When a service is referenced using `extends`, it can declare dependencies on other resources. These dependencies may be explicitly defined through attributes like `volumes`, `networks`, `configs`, `secrets`, `links`, `volumes_from`, or `depends_on`. Alternatively, dependencies can reference another service using the `service:{name}` syntax in namespace declarations such as `ipc`, `pid`, or `network_mode`.

Compose does not automatically import these referenced resources into the extended model. It is your responsibility to ensure all required resources are explicitly declared in the model that relies on extends.

Circular references with `extends` are not supported, Compose returns an error when one is detected.

#### [Finding referenced service](#finding-referenced-service)

`file` value can be:

* Not present. This indicates that another service within the same Compose file is being referenced.

* File path, which can be either:

  * Relative path. This path is considered as relative to the location of the main Compose file.
  * Absolute path.

A service denoted by `service` must be present in the identified referenced Compose file. Compose returns an error if:

* The service denoted by `service` is not found.
* The Compose file denoted by `file` is not found.

#### [Merging service definitions](#merging-service-definitions)

Two service definitions, the main one in the current Compose file and the referenced one specified by `extends`, are merged in the following way:

* Mappings: Keys in mappings of the main service definition override keys in mappings of the referenced service definition. Keys that aren't overridden are included as is.
* Sequences: Items are combined together into a new sequence. The order of elements is preserved with the referenced items coming first and main items after.
* Scalars: Keys in the main service definition take precedence over keys in the referenced one.

##### [Mappings](#mappings)

The following keys should be treated as mappings: `annotations`, `build.args`, `build.labels`, `build.extra_hosts`, `deploy.labels`, `deploy.update_config`, `deploy.rollback_config`, `deploy.restart_policy`, `deploy.resources.limits`, `environment`, `healthcheck`, `labels`, `logging.options`, `sysctls`, `storage_opt`, `extra_hosts`, `ulimits`.

One exception that applies to `healthcheck` is that the main mapping cannot specify `disable: true` unless the referenced mapping also specifies `disable: true`. Compose returns an error in this case. For example, the following input:

```yaml
services:
  common:
    image: busybox
    environment:
      TZ: utc
      PORT: 80
  cli:
    extends:
      service: common
    environment:
      PORT: 8080
```

Produces the following configuration for the `cli` service. The same output is produced if array syntax is used.

```yaml
environment:
  PORT: 8080
  TZ: utc
image: busybox
```

Items under `blkio_config.device_read_bps`, `blkio_config.device_read_iops`, `blkio_config.device_write_bps`, `blkio_config.device_write_iops`, `devices` and `volumes` are also treated as mappings where key is the target path inside the container.

For example, the following input:

```yaml
services:
  common:
    image: busybox
    volumes:
      - common-volume:/var/lib/backup/data:rw
  cli:
    extends:
      service: common
    volumes:
      - cli-volume:/var/lib/backup/data:ro
```

Produces the following configuration for the `cli` service. Note that the mounted path now points to the new volume name and `ro` flag was applied.

```yaml
image: busybox
volumes:
- cli-volume:/var/lib/backup/data:ro
```

If the referenced service definition contains `extends` mapping, the items under it are simply copied into the new merged definition. The merging process is then kicked off again until no `extends` keys are remaining.

For example, the following input:

```yaml
services:
  base:
    image: busybox
    user: root
  common:
    image: busybox
    extends:
      service: base
  cli:
    extends:
      service: common
```

Produces the following configuration for the `cli` service. Here, `cli` services gets `user` key from `common` service, which in turn gets this key from `base` service.

```yaml
image: busybox
user: root
```

##### [Sequences](#sequences)

The following keys should be treated as sequences: `cap_add`, `cap_drop`, `configs`, `deploy.placement.constraints`, `deploy.placement.preferences`, `deploy.reservations.generic_resources`, `device_cgroup_rules`, `expose`, `external_links`, `ports`, `secrets`, `security_opt`. Any duplicates resulting from the merge are removed so that the sequence only contains unique elements.

For example, the following input:

```yaml
services:
  common:
    image: busybox
    security_opt:
      - label=role:ROLE
  cli:
    extends:
      service: common
    security_opt:
      - label=user:USER
```

Produces the following configuration for the `cli` service.

```yaml
image: busybox
security_opt:
- label=role:ROLE
- label=user:USER
```

In case list syntax is used, the following keys should also be treated as sequences: `dns`, `dns_search`, `env_file`, `tmpfs`. Unlike sequence fields mentioned previously, duplicates resulting from the merge are not removed.

##### [Scalars](#scalars)

Any other allowed keys in the service definition should be treated as scalars.

### [`external_links`](#external_links)

`external_links` link service containers to services managed outside of your Compose application. `external_links` define the name of an existing service to retrieve using the platform lookup mechanism. An alias of the form `SERVICE:ALIAS` can be specified.

```yml
external_links:
  - redis
  - database:mysql
  - database:postgresql
```

### [`extra_hosts`](#extra_hosts)

`extra_hosts` adds hostname mappings to the container network interface configuration (`/etc/hosts` for Linux).

#### [Short syntax](#short-syntax-2)

Short syntax uses plain strings in a list. Values must set hostname and IP address for additional hosts in the form of `HOSTNAME=IP`.

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

#### [Long syntax](#long-syntax-2)

Alternatively, `extra_hosts` can be set as a mapping between hostname(s) and IP(s)

```yml
extra_hosts:
  somehost: "162.242.195.82"
  otherhost: "50.31.209.229"
  myhostv6: "::1"
```

Compose creates a matching entry with the IP address and hostname in the container's network configuration, which means for Linux `/etc/hosts` get extra lines:

```console
162.242.195.82  somehost
50.31.209.229   otherhost
::1             myhostv6
```

### [`gpus`](#gpus)

Requires: Docker Compose [2.30.0](https://github.com/docker/compose/releases/tag/v2.30.0) and later

`gpus` specifies GPU devices to be allocated for container usage. This is equivalent to a [device request](https://docs.docker.com/reference/compose-file/deploy/#devices) with an implicit `gpu` capability.

```yaml
services:
  model:
    gpus:
      - driver: 3dfx
        count: 2
```

`gpus` also can be set as string `all` to allocate all available GPU devices to the container.

```yaml
services:
  model:
    gpus: all
```

### [`group_add`](#group_add)

`group_add` specifies additional groups, by name or number, which the user inside the container must be a member of.

An example of where this is useful is when multiple containers (running as different users) need to all read or write the same file on a shared volume. That file can be owned by a group shared by all the containers, and specified in `group_add`.

```yml
services:
  myservice:
    image: alpine
    group_add:
      - mail
```

Running `id` inside the created container must show that the user belongs to the `mail` group, which would not have been the case if `group_add` were not declared.

### [`healthcheck`](#healthcheck)

The `healthcheck` attribute declares a check that's run to determine whether or not the service containers are "healthy". It works in the same way, and has the same default values, as the HEALTHCHECK Dockerfile instruction set by the service's Docker image. Your Compose file can override the values set in the Dockerfile.

For more information on `HEALTHCHECK`, see the [Dockerfile reference](https://docs.docker.com/reference/dockerfile/#healthcheck).

```yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost"]
  interval: 1m30s
  timeout: 10s
  retries: 3
  start_period: 40s
  start_interval: 5s
```

`interval`, `timeout`, `start_period`, and `start_interval` are [specified as durations](https://docs.docker.com/reference/compose-file/extension/#specifying-durations). Introduced in Docker Compose version [2.20.2](https://github.com/docker/compose/releases/tag/v2.20.2)

`test` defines the command Compose runs to check container health. It can be either a string or a list. If it's a list, the first item must be either `NONE`, `CMD` or `CMD-SHELL`. If it's a string, it's equivalent to specifying `CMD-SHELL` followed by that string.

```yml
# Hit the local web app
test: ["CMD", "curl", "-f", "http://localhost"]
```

Using `CMD-SHELL` runs the command configured as a string using the container's default shell (`/bin/sh` for Linux). Both of the following forms are equivalent:

```yml
test: ["CMD-SHELL", "curl -f http://localhost || exit 1"]
```

```yml
test: curl -f https://localhost || exit 1
```

`NONE` disables the healthcheck, and is mostly useful to disable the Healthcheck Dockerfile instruction set by the service's Docker image. Alternatively, the healthcheck set by the image can be disabled by setting `disable: true`:

```yml
healthcheck:
  disable: true
```

### [`hostname`](#hostname)

`hostname` declares a custom host name to use for the service container. It must be a valid RFC 1123 hostname.

### [`image`](#image)

`image` specifies the image to start the container from. `image` must follow the Open Container Specification [addressable image format](https://github.com/opencontainers/org/blob/master/docs/docs/introduction/digests.md), as `[<registry>/][<project>/]<image>[:<tag>|@<digest>]`.

```yml
    image: redis
    image: redis:5
    image: redis@sha256:0ed5d5928d4737458944eb604cc8509e245c3e19d02ad83935398bc4b991aac7
    image: library/redis
    image: docker.io/library/redis
    image: my_private.registry:5000/redis
```

If the image does not exist on the platform, Compose attempts to pull it based on the `pull_policy`. If you are also using the [Compose Build Specification](https://docs.docker.com/reference/compose-file/build/), there are alternative options for controlling the precedence of pull over building the image from source, however pulling the image is the default behavior.

`image` may be omitted from a Compose file as long as a `build` section is declared. If you are not using the Compose Build Specification, Compose won't work if `image` is missing from the Compose file.

### [`init`](#init)

`init` runs an init process (PID 1) inside the container that forwards signals and reaps processes. Set this option to `true` to enable this feature for the service.

```yml
services:
  web:
    image: alpine:latest
    init: true
```

The init binary that is used is platform specific.

### [`ipc`](#ipc)

`ipc` configures the IPC isolation mode set by the service container.

* `shareable`: Gives the container its own private IPC namespace, with a possibility to share it with other containers.
* `service:{name}`: Makes the container join another container's (`shareable`) IPC namespace.

```yml
    ipc: "shareable"
    ipc: "service:[service name]"
```

### [`isolation`](#isolation)

`isolation` specifies a container’s isolation technology. Supported values are platform specific.

### [`labels`](#labels)

`labels` add metadata to containers. You can use either an array or a map.

It's recommended that you use reverse-DNS notation to prevent your labels from conflicting with those used by other software.

```yml
labels:
  com.example.description: "Accounting webapp"
  com.example.department: "Finance"
  com.example.label-with-empty-value: ""
```

```yml
labels:
  - "com.example.description=Accounting webapp"
  - "com.example.department=Finance"
  - "com.example.label-with-empty-value"
```

Compose creates containers with canonical labels:

* `com.docker.compose.project` set on all resources created by Compose to the user project name
* `com.docker.compose.service` set on service containers with service name as defined in the Compose file

The `com.docker.compose` label prefix is reserved. Specifying labels with this prefix in the Compose file results in a runtime error.

### [`label_file`](#label_file)

Requires: Docker Compose [2.32.2](https://github.com/docker/compose/releases/tag/v2.32.2) and later

The `label_file` attribute lets you load labels for a service from an external file or a list of files. This provides a convenient way to manage multiple labels without cluttering the Compose file.

The file uses a key-value format, similar to `env_file`. You can specify multiple files as a list. When using multiple files, they are processed in the order they appear in the list. If the same label is defined in multiple files, the value from the last file in the list overrides earlier ones.

```yaml
services:
  one:
    label_file: ./app.labels

  two:
    label_file:
      - ./app.labels
      - ./additional.labels
```

If a label is defined in both the `label_file` and the `labels` attribute, the value in [labels](#labels) takes precedence.

### [`links`](#links)

`links` defines a network link to containers in another service. Either specify both the service name and a link alias (`SERVICE:ALIAS`), or just the service name.

```yml
web:
  links:
    - db
    - db:database
    - redis
```

Containers for the linked service are reachable at a hostname identical to the alias, or the service name if no alias is specified.

Links are not required to enable services to communicate. When no specific network configuration is set, any service is able to reach any other service at that service’s name on the `default` network. If services specify the networks they are attached to, `links` does not override the network configuration. Services that are not connected to a shared network are not be able to communicate with each other. Compose doesn't warn you about a configuration mismatch.

Links also express implicit dependency between services in the same way as [`depends_on`](#depends_on), so they determine the order of service startup.

### [`logging`](#logging)

`logging` defines the logging configuration for the service.

```yml
logging:
  driver: syslog
  options:
    syslog-address: "tcp://192.168.0.42:123"
```

The `driver` name specifies a logging driver for the service's containers. The default and available values are platform specific. Driver specific options can be set with `options` as key-value pairs.

### [`mac_address`](#mac_address)

> Available with Docker Compose version 2.24.0 and later.

`mac_address` sets a Mac address for the service container.

> Note
>
> Container runtimes might reject this value, for example Docker Engine >= v25.0. In that case, you should use [networks.mac\_address](#mac_address) instead.

### [`mem_limit`](#mem_limit)

`mem_limit` configures a limit on the amount of memory a container can allocate, set as a string expressing a [byte value](https://docs.docker.com/reference/compose-file/extension/#specifying-byte-values).

When set, `mem_limit` must be consistent with the `limits.memory` attribute in the [Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#memory).

### [`mem_reservation`](#mem_reservation)

`mem_reservation` configures a reservation on the amount of memory a container can allocate, set as a string expressing a [byte value](https://docs.docker.com/reference/compose-file/extension/#specifying-byte-values).

When set, `mem_reservation` must be consistent with the `reservations.memory` attribute in the [Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#memory).

### [`mem_swappiness`](#mem_swappiness)

`mem_swappiness` defines as a percentage, a value between 0 and 100, for the host kernel to swap out anonymous memory pages used by a container.

* `0`: Turns off anonymous page swapping.
* `100`: Sets all anonymous pages as swappable.

The default value is platform specific.

### [`memswap_limit`](#memswap_limit)

`memswap_limit` defines the amount of memory the container is allowed to swap to disk. This is a modifier attribute that only has meaning if [`memory`](https://docs.docker.com/reference/compose-file/deploy/#memory) is also set. Using swap lets the container write excess memory requirements to disk when the container has exhausted all the memory that is available to it. There is a performance penalty for applications that swap memory to disk often.

* If `memswap_limit` is set to a positive integer, then both `memory` and `memswap_limit` must be set. `memswap_limit` represents the total amount of memory and swap that can be used, and `memory` controls the amount used by non-swap memory. So if `memory`="300m" and `memswap_limit`="1g", the container can use 300m of memory and 700m (1g - 300m) swap.
* If `memswap_limit` is set to 0, the setting is ignored, and the value is treated as unset.
* If `memswap_limit` is set to the same value as `memory`, and `memory` is set to a positive integer, the container does not have access to swap.
* If `memswap_limit` is unset, and `memory` is set, the container can use as much swap as the `memory` setting, if the host container has swap memory configured. For instance, if `memory`="300m" and `memswap_limit` is not set, the container can use 600m in total of memory and swap.
* If `memswap_limit` is explicitly set to -1, the container is allowed to use unlimited swap, up to the amount available on the host system.

### [`models`](#models)

Requires: Docker Compose [2.38.0](https://github.com/docker/compose/releases/tag/v2.38.0) and later

`models` defines which AI models the service should use at runtime. Each referenced model must be defined under the [`models` top-level element](https://docs.docker.com/reference/compose-file/models/).

```yaml
services:
  short_syntax:
    image: app
    models:
      - my_model
  long_syntax:
    image: app
    models:
      my_model:
        endpoint_var: MODEL_URL
        model_var: MODEL
```

When a service is linked to a model, Docker Compose injects environment variables to pass connection details and model identifiers to the container. This allows the application to locate and communicate with the model dynamically at runtime, without hard-coding values.

#### [Long syntax](#long-syntax-3)

The long syntax gives you more control over the environment variable names.

* `endpoint_var` sets the name of the environment variable that holds the model runner’s URL.
* `model_var` sets the name of the environment variable that holds the model identifier.

If either is omitted, Compose automatically generates the environment variable names based on the model key using the following rules:

* Convert the model key to uppercase
* Replace any '-' characters with '\_'
* Append `_URL` for the endpoint variable

### [`network_mode`](#network_mode)

`network_mode` sets a service container's network mode.

* `bridge`: Connects the container to Docker's default bridge network instead of a project-specific network. Containers on the default bridge network cannot resolve each other by service name . Instead, use a user-defined network for DNS resolution.
* `none`: Turns off all container networking.
* `host`: Gives the container raw access to the host's network interface.
* `service:{name}`: Gives the container access to the specified container by referring to its service name.
* `container:{name}`: Gives the container access to the specified container by referring to its container ID.

For more information container networks, see the [Docker Engine documentation](https://docs.docker.com/engine/network/#container-networks).

```yml
    network_mode: "bridge"
    network_mode: "host"
    network_mode: "none"
    network_mode: "service:[service name]"
```

When set, the [`networks`](#networks) attribute is not allowed and Compose rejects any Compose file containing both attributes.

### [`networks`](#networks)

The `networks` attribute defines the networks that service containers are attached to, referencing entries under the `networks` top-level element. The `networks` attribute helps manage the networking aspects of containers, providing control over how services are segmented and interact within the Docker environment. This is used to specify which networks the containers for that service should connect to. This is important for defining how containers communicate with each other and externally.

```yml
services:
  some-service:
    networks:
      - some-network
      - other-network
```

For more information about the `networks` top-level element, see [Networks](https://docs.docker.com/reference/compose-file/networks/).

#### [Implicit default network](#implicit-default-network)

If `networks` is empty or absent from the Compose file, Compose considers an implicit definition for the service to be connected to the `default` network:

```yml
services:
  some-service:
    image: foo
```

This example is actually equivalent to:

```yml
services:
  some-service:
    image: foo
    networks:
      default: {}
```

If you want the service to not be connected a network, you must set [`network_mode: none`](#network_mode).

#### [`aliases`](#aliases)

`aliases` declares alternative hostnames for the service on the network. Other containers on the same network can use either the service name or an alias to connect to one of the service's containers.

Since `aliases` are network-scoped, the same service can have different aliases on different networks.

> Note
>
> A network-wide alias can be shared by multiple containers, and even by multiple services. If it is, then exactly which container the name resolves to is not guaranteed.

```yml
services:
  some-service:
    networks:
      some-network:
        aliases:
          - alias1
          - alias3
      other-network:
        aliases:
          - alias2
```

In the following example, service `frontend` is able to reach the `backend` service at the hostname `backend` or `database` on the `back-tier` network. The service `monitoring` is able to reach same `backend` service at `backend` or `mysql` on the `admin` network.

```yml
services:
  frontend:
    image: example/webapp
    networks:
      - front-tier
      - back-tier

  monitoring:
    image: example/monitoring
    networks:
      - admin

  backend:
    image: example/backend
    networks:
      back-tier:
        aliases:
          - database
      admin:
        aliases:
          - mysql

networks:
  front-tier: {}
  back-tier: {}
  admin: {}
```

#### [`interface_name`](#interface_name)

Requires: Docker Compose [2.36.0](https://github.com/docker/compose/releases/tag/v2.36.0) and later

`interface_name` lets you specify the name of the network interface used to connect a service to a given network. This ensures consistent and predictable interface naming across services and networks.

```yaml
services:
  backend:
    image: alpine
    command: ip link show
    networks:
      back-tier:
        interface_name: eth0
```

Running the example Compose application shows:

```console
backend-1  | 11: eth0@if64: <BROADCAST,MULTICAST,UP,LOWER_UP,M-DOWN> mtu 1500 qdisc noqueue state UP
```

#### [`ipv4_address`, `ipv6_address`](#ipv4_address-ipv6_address)

Specify a static IP address for a service container when joining the network.

The corresponding network configuration in the [top-level networks section](https://docs.docker.com/reference/compose-file/networks/) must have an `ipam` attribute with subnet configurations covering each static address.

```yml
services:
  frontend:
    image: example/webapp
    networks:
      front-tier:
        ipv4_address: 172.16.238.10
        ipv6_address: 2001:3984:3989::10

networks:
  front-tier:
    ipam:
      driver: default
      config:
        - subnet: "172.16.238.0/24"
        - subnet: "2001:3984:3989::/64"
```

#### [`link_local_ips`](#link_local_ips)

`link_local_ips` specifies a list of link-local IPs. Link-local IPs are special IPs which belong to a well known subnet and are purely managed by the operator, usually dependent on the architecture where they are deployed.

Example:

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net:
        link_local_ips:
          - 57.123.22.11
          - 57.123.22.13
networks:
  app_net:
    driver: bridge
```

#### [`mac_address`](#mac_address-1)

Requires: Docker Compose [2.23.2](https://github.com/docker/compose/releases/tag/v2.23.2) and later

`mac_address` sets the Mac address used by the service container when connecting to this particular network.

#### [`driver_opts`](#driver_opts-1)

`driver_opts` specifies a list of options as key-value pairs to pass to the driver. These options are driver-dependent. Consult the driver's documentation for more information.

```yml
services:
  app:
    networks:
      app_net:
        driver_opts:
          foo: "bar"
          baz: 1
```

#### [`gw_priority`](#gw_priority)

Requires: Docker Compose [2.33.1](https://github.com/docker/compose/releases/tag/v2.33.1) and later

The network with the highest `gw_priority` is selected as the default gateway for the service container. If unspecified, the default value is 0.

In the following example, `app_net_2` will be selected as the default gateway.

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net_1:
      app_net_2:
        gw_priority: 1
      app_net_3:
networks:
  app_net_1:
  app_net_2:
  app_net_3:
```

#### [`priority`](#priority)

`priority` indicates in which order Compose connects the service’s containers to its networks. If unspecified, the default value is 0.

If the container runtime accepts a `mac_address` attribute at service level, it is applied to the network with the highest `priority`. In other cases, use attribute `networks.mac_address`.

`priority` does not affect which network is selected as the default gateway. Use the [`gw_priority`](#gw_priority) attribute instead.

`priority` does not control the order in which networks connections are added to the container, it cannot be used to determine the device name (`eth0` etc.) in the container.

```yaml
services:
  app:
    image: busybox
    command: top
    networks:
      app_net_1:
        priority: 1000
      app_net_2:

      app_net_3:
        priority: 100
networks:
  app_net_1:
  app_net_2:
  app_net_3:
```

### [`oom_kill_disable`](#oom_kill_disable)

If `oom_kill_disable` is set, Compose configures the platform so it won't kill the container in case of memory starvation.

### [`oom_score_adj`](#oom_score_adj)

`oom_score_adj` tunes the preference for containers to be killed by platform in case of memory starvation. Value must be within -1000,1000 range.

### [`pid`](#pid)

`pid` sets the PID mode for container created by Compose. Supported values are platform specific.

### [`pids_limit`](#pids_limit)

`pids_limit` tunes a container’s PIDs limit. Set to -1 for unlimited PIDs.

```yml
pids_limit: 10
```

When set, `pids_limit` must be consistent with the `pids` attribute in the [Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#pids).

### [`platform`](#platform)

`platform` defines the target platform the containers for the service run on. It uses the `os[/arch[/variant]]` syntax.

The values of `os`, `arch`, and `variant` must conform to the convention used by the [OCI Image Spec](https://github.com/opencontainers/image-spec/blob/v1.0.2/image-index.md).

Compose uses this attribute to determine which version of the image is pulled and/or on which platform the service’s build is performed.

```yml
platform: darwin
platform: windows/amd64
platform: linux/arm64/v8
```

### [`ports`](#ports)

The `ports` is used to define the port mappings between the host machine and the containers. This is crucial for allowing external access to services running inside containers. It can be defined using short syntax for simple port mapping or long syntax, which includes additional options like protocol type and network mode.

> Note
>
> Port mapping must not be used with `network_mode: host`. Doing so causes a runtime error because `network_mode: host` already exposes container ports directly to the host network, so port mapping isn’t needed.

#### [Short syntax](#short-syntax-3)

The short syntax is a colon-separated string to set the host IP, host port, and container port in the form:

`[HOST:]CONTAINER[/PROTOCOL]` where:

* `HOST` is `[IP:](port | range)` (optional). If it is not set, it binds to all network interfaces (`0.0.0.0`).
* `CONTAINER` is `port | range`.
* `PROTOCOL` restricts ports to a specified protocol either `tcp` or `udp`(optional). Default is `tcp`.

> Warning
>
> If you do not specify a host IP (such as `127.0.0.1`), Docker binds to all interfaces (`0.0.0.0`), bypassing host firewall rules. This can expose the container directly to the internet if the host has a public IP address. For more information, see [Port publishing and mapping](https://docs.docker.com/engine/network/port-publishing/).

Ports can be either a single value or a range. `HOST` and `CONTAINER` must use equivalent ranges.

You can either specify both ports (`HOST:CONTAINER`), or just the container port. In the latter case, the container runtime automatically allocates any unassigned port of the host.

`HOST:CONTAINER` should always be specified as a (quoted) string, to avoid conflicts with [YAML base-60 float](https://yaml.org/type/float.html).

IPv6 addresses can be enclosed in square brackets.

Examples:

```yml
ports:
  - "3000"
  - "3000-3005"
  - "8000:8000"
  - "9090-9091:8080-8081"
  - "49100:22"
  - "8000-9000:80"
  - "127.0.0.1:8001:8001"
  - "127.0.0.1:5000-5010:5000-5010"
  - "::1:6000:6000"
  - "[::1]:6001:6001"
  - "6060:6060/udp"
```

> Note
>
> If host IP mapping is not supported by a container engine, Compose rejects the Compose file and ignores the specified host IP.

#### [Long syntax](#long-syntax-4)

The long form syntax lets you configure additional fields that can't be expressed in the short form.

* `target`: The container port.
* `published`: The publicly exposed port. It is defined as a string and can be set as a range using syntax `start-end`. It means the actual port is assigned a remaining available port, within the set range.
* `host_ip`: The host IP mapping. If it is not set, it binds to all network interfaces (`0.0.0.0`).
* `protocol`: The port protocol (`tcp` or `udp`). Defaults to `tcp`.
* `app_protocol`: The application protocol (TCP/IP level 4 / OSI level 7) this port is used for. This is optional and can be used as a hint for Compose to offer richer behavior for protocols that it understands. Introduced in Docker Compose version [2.26.0](https://github.com/docker/compose/releases/tag/v2.26.0).
* `mode`: Specifies how the port is published in a Swarm setup. If set to `host`, it publishes the port on every node in Swarm. If set to `ingress`, it allows load balancing across the nodes in Swarm. Defaults to `ingress`.
* `name`: A human-readable name for the port, used to document its usage within the service.

```yml
ports:
  - name: web
    target: 80
    host_ip: 127.0.0.1
    published: "8080"
    protocol: tcp
    app_protocol: http
    mode: host

  - name: web-secured
    target: 443
    host_ip: 127.0.0.1
    published: "8083-9000"
    protocol: tcp
    app_protocol: https
    mode: host
```

### [`post_start`](#post_start)

Requires: Docker Compose [2.30.0](https://github.com/docker/compose/releases/tag/v2.30.0) and later

`post_start` defines a sequence of lifecycle hooks to run after a container has started. The exact timing of when the command is run is not guaranteed.

* `command`: Specifies the command to run once the container starts. This attribute is required, and you can choose to use either the shell form or the exec form.
* `user`: The user to run the command. If not set, the command is run with the same user as the main service command.
* `privileged`: Lets the `post_start` command run with privileged access.
* `working_dir`: The working directory in which to run the command. If not set, it is run in the same working directory as the main service command.
* `environment`: Sets environment variables specifically for the `post_start` command. While the command inherits the environment variables defined for the service’s main command, this section lets you add new variables or override existing ones.

```yaml
services:
  test:
    post_start:
      - command: ./do_something_on_startup.sh
        user: root
        privileged: true
        environment:
          - FOO=BAR
```

For more information, see [Use lifecycle hooks](https://docs.docker.com/compose/how-tos/lifecycle/).

### [`pre_stop`](#pre_stop)

Requires: Docker Compose [2.30.0](https://github.com/docker/compose/releases/tag/v2.30.0) and later

`pre_stop` defines a sequence of lifecycle hooks to run before the container is stopped. These hooks won't run if the container stops by itself or is terminated suddenly.

Configuration is equivalent to [post\_start](#post_start).

### [`privileged`](#privileged)

`privileged` configures the service container to run with elevated privileges. Support and actual impacts are platform specific.

### [`profiles`](#profiles)

`profiles` defines a list of named profiles for the service to be enabled under. If unassigned, the service is always started but if assigned, it is only started if the profile is activated.

If present, `profiles` follow the regex format of `[a-zA-Z0-9][a-zA-Z0-9_.-]+`.

```yaml
services:
  frontend:
    image: frontend
    profiles: ["frontend"]

  phpmyadmin:
    image: phpmyadmin
    depends_on:
      - db
    profiles:
      - debug
```

### [`provider`](#provider)

Requires: Docker Compose [2.36.0](https://github.com/docker/compose/releases/tag/v2.36.0) and later

`provider` can be used to define a service that Compose won't manage directly. Compose delegated the service lifecycle to a dedicated or third-party component.

```yaml
  database:
    provider:
      type: awesomecloud
      options:
        type: mysql
        foo: bar
  app:
    image: myapp
    depends_on:
       - database
```

As Compose runs the application, the `awesomecloud` binary is used to manage the `database` service setup. Dependent service `app` receives additional environment variables prefixed by the service name so it can access the resource.

For illustration, assuming `awesomecloud` execution produced variables `URL` and `API_KEY`, the `app` service runs with environment variables `DATABASE_URL` and `DATABASE_API_KEY`.

As Compose stops the application, the `awesomecloud` binary is used to manage the `database` service tear down.

The mechanism used by Compose to delegate the service lifecycle to an external binary is described in the [Compose extensibility documentation](https://github.com/docker/compose/tree/main/docs/extension.md).

For more information on using the `provider` attribute, see [Use provider services](https://docs.docker.com/compose/how-tos/provider-services/).

#### [`type`](#type)

`type` attribute is required. It defines the external component used by Compose to manage setup and tear down lifecycle events.

#### [`options`](#options)

`options` are specific to the selected provider and not validated by the compose specification

### [`pull_policy`](#pull_policy)

`pull_policy` defines the decisions Compose makes when it starts to pull images. Possible values are:

* `always`: Compose always pulls the image from the registry.
* `never`: Compose doesn't pull the image from a registry and relies on the platform cached image. If there is no cached image, a failure is reported.
* `missing`: Compose pulls the image only if it's not available in the platform cache. This is the default option if you are not also using the [Compose Build Specification](https://docs.docker.com/reference/compose-file/build/). `if_not_present` is considered an alias for this value for backward compatibility. The `latest` tag is always pulled even when the `missing` pull policy is used.
* `build`: Compose builds the image. Compose rebuilds the image if it's already present.
* `daily`: Compose checks the registry for image updates if the last pull took place more than 24 hours ago.
* `weekly`: Compose checks the registry for image updates if the last pull took place more than 7 days ago.
* `every_<duration>`: Compose checks the registry for image updates if the last pull took place before `<duration>`. Duration can be expressed in weeks (`w`), days (`d`), hours (`h`), minutes (`m`), seconds (`s`) or a combination of these.

```yaml
services:
  test:
    image: nginx
    pull_policy: every_12h
```

### [`read_only`](#read_only)

`read_only` configures the service container to be created with a read-only filesystem.

### [`restart`](#restart)

`restart` defines the policy that the platform applies on container termination.

* `no`: The default restart policy. It does not restart the container under any circumstances.
* `always`: The policy always restarts the container until its removal.
* `on-failure[:max-retries]`: The policy restarts the container if the exit code indicates an error. Optionally, limit the number of restart retries the Docker daemon attempts.
* `unless-stopped`: The policy restarts the container irrespective of the exit code but stops restarting when the service is stopped or removed.

```yml
    restart: "no"
    restart: always
    restart: on-failure
    restart: on-failure:3
    restart: unless-stopped
```

You can find more detailed information on restart policies in the [Restart Policies (--restart)](/reference/cli/docker/container/run/#restart) section of the Docker run reference page.

### [`runtime`](#runtime)

`runtime` specifies which runtime to use for the service’s containers.

For example, `runtime` can be the name of [an implementation of OCI Runtime Spec](https://github.com/opencontainers/runtime-spec/blob/master/implementations.md), such as "runc".

```yml
web:
  image: busybox:latest
  command: true
  runtime: runc
```

The default is `runc`. To use a different runtime, see [Alternative runtimes](https://docs.docker.com/engine/daemon/alternative-runtimes/).

### [`scale`](#scale)

`scale` specifies the default number of containers to deploy for this service. When both are set, `scale` must be consistent with the `replicas` attribute in the [Deploy Specification](https://docs.docker.com/reference/compose-file/deploy/#replicas).

### [`secrets`](#secrets)

The `secrets` attribute grants access to sensitive data defined by the secrets top-level element on a per-service basis. Services can be granted access to multiple secrets.

Two different syntax variants are supported; the short syntax and the long syntax. Long and short syntax for secrets may be used in the same Compose file.

Compose reports an error if the secret doesn't exist on the platform or isn't defined in the [`secrets` top-level section](https://docs.docker.com/reference/compose-file/secrets/) of the Compose file.

Defining a secret in the top-level `secrets` must not imply granting any service access to it. Such grant must be explicit within service specification as [secrets](https://docs.docker.com/reference/compose-file/secrets/) service element.

#### [Short syntax](#short-syntax-4)

The short syntax variant only specifies the secret name. This grants the container access to the secret and mounts it as read-only to `/run/secrets/<secret_name>` within the container. The source name and destination mountpoint are both set to the secret name.

The following example uses the short syntax to grant the `frontend` service access to the `server-certificate` secret. The value of `server-certificate` is set to the contents of the file `./server.cert`.

```yml
services:
  frontend:
    image: example/webapp
    secrets:
      - server-certificate
secrets:
  server-certificate:
    file: ./server.cert
```

#### [Long syntax](#long-syntax-5)

The long syntax provides more granularity in how the secret is created within the service's containers.

* `source`: The name of the secret as it exists on the platform.
* `target`: The name of the file to be mounted in `/run/secrets/` in the service's task container, or absolute path of the file if an alternate location is required. Defaults to `source` if not specified.
* `uid` and `gid`: The numeric uid or gid that owns the file within `/run/secrets/` in the service's task containers.
* `mode`: The [permissions](https://wintelguy.com/permissions-calc.pl) for the file to be mounted in `/run/secrets/` in the service's task containers, in octal notation. The default value is world-readable permissions (mode `0444`). The writable bit must be ignored if set. The executable bit may be set.

Note that support for `uid`, `gid`, and `mode` attributes are only implemented in Docker Compose when the source of the secret is [`environment`](https://docs.docker.com/reference/compose-file/secrets/). When the source is a [`file`](https://docs.docker.com/reference/compose-file/secrets/), Compose uses a bind-mount under the hood which doesn't allow `uid` remapping, and these attributes are silently ignored.

The following example sets the name of the `my-token` secret file within the container, sets the mode to `0440` (group-readable), and sets the user and group to `103`. The value of `my-token` is read from the `MY_TOKEN` environment variable.

```yml
services:
  frontend:
    image: example/webapp
    secrets:
      - source: my-token
        uid: "103"
        gid: "103"
        mode: 0o440
secrets:
  my-token:
    environment: "MY_TOKEN"
```

### [`security_opt`](#security_opt)

`security_opt` overrides the default labeling scheme for each container.

Options accept either `option=value` or `option:value` syntax. For boolean options such as `no-new-privileges`, the value may be omitted entirely, in which case the option is treated as enabled. The following syntaxes are all equivalent:

```yml
security_opt:
  - no-new-privileges
  - no-new-privileges=true
  - no-new-privileges:true
```

```yml
security_opt:
  - label=user:USER
  - label=role:ROLE
```

For further default labeling schemes you can override, see [Security configuration](/reference/cli/docker/container/run/#security-opt).

### [`shm_size`](#shm_size)

`shm_size` configures the size of the shared memory (`/dev/shm` partition on Linux) allowed by the service container. It's specified as a [byte value](https://docs.docker.com/reference/compose-file/extension/#specifying-byte-values).

### [`stdin_open`](#stdin_open)

`stdin_open` configures a service's container to run with an allocated stdin. This is the same as running a container with the `-i` flag. For more information, see [Keep stdin open](/reference/cli/docker/container/run/#interactive).

Supported values are `true` or `false`.

### [`stop_grace_period`](#stop_grace_period)

`stop_grace_period` specifies how long Compose must wait when attempting to stop a container if it doesn't handle SIGTERM (or whichever stop signal has been specified with [`stop_signal`](#stop_signal)), before sending SIGKILL. It's specified as a [duration](https://docs.docker.com/reference/compose-file/extension/#specifying-durations).

```yml
    stop_grace_period: 1s
    stop_grace_period: 1m30s
```

Default value is 10 seconds for the container to exit before sending SIGKILL.

### [`stop_signal`](#stop_signal)

`stop_signal` defines the signal that Compose uses to stop the service containers. If unset containers are stopped by Compose by sending `SIGTERM`.

```yml
stop_signal: SIGUSR1
```

### [`storage_opt`](#storage_opt)

`storage_opt` defines storage driver options for a service.

```yml
storage_opt:
  size: '1G'
```

### [`sysctls`](#sysctls)

`sysctls` defines kernel parameters to set in the container. `sysctls` can use either an array or a map.

```yml
sysctls:
  net.core.somaxconn: 1024
  net.ipv4.tcp_syncookies: 0
```

```yml
sysctls:
  - net.core.somaxconn=1024
  - net.ipv4.tcp_syncookies=0
```

You can only use sysctls that are namespaced in the kernel. Docker does not support changing sysctls inside a container that also modify the host system. For an overview of supported sysctls, refer to [configure namespaced kernel parameters (sysctls) at runtime](/reference/cli/docker/container/run/#sysctl).

### [`tmpfs`](#tmpfs)

`tmpfs` mounts a temporary file system inside the container. It can be a single value or a list.

```yml
tmpfs:
 - <path>
 - <path>:<options>
```

* `path`: The path inside the container where the tmpfs will be mounted.
* `options`: Comma-separated list of options for the tmpfs mount.

Available options:

* `mode`: Sets the file system permissions.
* `uid`: Sets the user ID that owns the mounted tmpfs.
* `gid`: Sets the group ID that owns the mounted tmpfs.

```yml
services:
  app:
    tmpfs:
      - /data:mode=755,uid=1009,gid=1009
      - /run
```

### [`tty`](#tty)

`tty` configures a service's container to run with a TTY. This is the same as running a container with the `-t` or `--tty` flag. For more information, see [Allocate a pseudo-TTY](/reference/cli/docker/container/run/#tty).

Supported values are `true` or `false`.

### [`ulimits`](#ulimits)

`ulimits` overrides the default `ulimits` for a container. It's specified either as an integer for a single limit or as mapping for soft/hard limits.

```yml
ulimits:
  nproc: 65535
  nofile:
    soft: 20000
    hard: 40000
```

### [`use_api_socket`](#use_api_socket)

When `use_api_socket` is set, the container is able to interact with the underlying container engine through the API socket. Your credentials are mounted inside the container so the container acts as a pure delegate for your commands relating to the container engine. Typically, commands ran by container can `pull` and `push` to your registry.

### [`user`](#user)

`user` overrides the user used to run the container process. The default is set by the image, for example Dockerfile `USER`. If it's not set, then `root`.

### [`userns_mode`](#userns_mode)

`userns_mode` sets the user namespace for the service. Supported values are platform specific and may depend on platform configuration.

```yml
userns_mode: "host"
```

### [`uts`](#uts)

Requires: Docker Compose [2.15.1](https://github.com/docker/compose/releases/tag/v2.15.1) and later

`uts` configures the UTS namespace mode set for the service container. When unspecified it is the runtime's decision to assign a UTS namespace, if supported. Available values are:

* `'host'`: Results in the container using the same UTS namespace as the host.

```yml
    uts: "host"
```

### [`volumes`](#volumes)

The `volumes` attribute define mount host paths or named volumes that are accessible by service containers. You can use `volumes` to define multiple types of mounts; `volume`, `bind`, `tmpfs`, or `npipe`.

If the mount is a host path and is only used by a single service, it can be declared as part of the service definition. To reuse a volume across multiple services, a named volume must be declared in the `volumes` top-level element.

The following example shows a named volume (`db-data`) being used by the `backend` service, and a bind mount defined for a single service.

```yml
services:
  backend:
    image: example/backend
    volumes:
      - type: volume
        source: db-data
        target: /data
        volume:
          nocopy: true
          subpath: sub
      - type: bind
        source: /var/run/postgres/postgres.sock
        target: /var/run/postgres/postgres.sock

volumes:
  db-data:
```

For more information about the `volumes` top-level element, see [Volumes](https://docs.docker.com/reference/compose-file/volumes/).

#### [Short syntax](#short-syntax-5)

The short syntax uses a single string with colon-separated values to specify a volume mount (`VOLUME:CONTAINER_PATH`), or an access mode (`VOLUME:CONTAINER_PATH:ACCESS_MODE`).

* `VOLUME`: Can be either a host path on the platform hosting containers (bind mount) or a volume name.

* `CONTAINER_PATH`: The path in the container where the volume is mounted.

* `ACCESS_MODE`: A comma-separated `,` list of options:

  * `rw`: Read and write access. This is the default if none is specified.
  * `ro`: Read-only access.
  * `z`: SELinux option indicating that the bind mount host content is shared among multiple containers.
  * `Z`: SELinux option indicating that the bind mount host content is private and unshared for other containers.

> Note
>
> The SELinux re-labeling bind mount option is ignored on platforms without SELinux.

> Note
>
> Relative host paths are only supported by Compose that deploy to a local container runtime. This is because the relative path is resolved from the Compose file’s parent directory which is only applicable in the local case. When Compose deploys to a non-local platform it rejects Compose files which use relative host paths with an error. To avoid ambiguities with named volumes, relative paths should always begin with `.` or `..`.

> Note
>
> For bind mounts, the short syntax creates a directory at the source path on the host if it doesn't exist. This is for backward compatibility with `docker-compose` legacy. It can be prevented by using long syntax and setting `create_host_path` to `false`.

#### [Long syntax](#long-syntax-6)

The long form syntax lets you configure additional fields that can't be expressed in the short form.

* `type`: The mount type. Either `volume`, `bind`, `tmpfs`, `image`, `npipe`, or `cluster`

* `source`: The source of the mount, a path on the host for a bind mount, a Docker image reference for an image mount, or the name of a volume defined in the [top-level `volumes` key](https://docs.docker.com/reference/compose-file/volumes/). Not applicable for a tmpfs mount.

* `target`: The path in the container where the volume is mounted.

* `read_only`: Flag to set the volume as read-only.

* `bind`: Used to configure additional bind options:

  * `propagation`: The propagation mode used for the bind.
  * `create_host_path`: Creates a directory at the source path on host if there is nothing present. Defaults to `true`.
  * `selinux`: The SELinux re-labeling option `z` (shared) or `Z` (private)

* `volume`: Configures additional volume options:

  * `nocopy`: Flag to disable copying of data from a container when a volume is created.
  * `subpath`: Path inside a volume to mount instead of the volume root.

* `tmpfs`: Configures additional tmpfs options:

  * `size`: The size for the tmpfs mount in bytes (either numeric or as bytes unit).
  * `mode`: The file mode for the tmpfs mount as Unix permission bits as an octal number. Introduced in Docker Compose version [2.14.0](https://github.com/docker/compose/releases/tag/v2.14.0).

* `image`: Configures additional image options:
  * `subpath`: Path inside the source image to mount instead of the image root. Available in [Docker Compose version 2.35.0](https://github.com/docker/compose/releases/tag/v2.35.0)

* `consistency`: The consistency requirements of the mount. Available values are platform specific.

> Tip
>
> Working with large repositories or monorepos, or with virtual file systems that are no longer scaling with your codebase? Compose now takes advantage of [Synchronized file shares](https://docs.docker.com/desktop/features/synchronized-file-sharing/) and automatically creates file shares for bind mounts. Ensure you're signed in to Docker with a paid subscription and have enabled both **Access experimental features** and **Manage Synchronized file shares with Compose** in Docker Desktop's settings.

### [`volumes_from`](#volumes_from)

`volumes_from` mounts all of the volumes from another service or container. You can optionally specify read-only access `ro` or read-write `rw`. If no access level is specified, then read-write access is used.

You can also mount volumes from a container that is not managed by Compose by using the `container:` prefix.

```yaml
volumes_from:
  - service_name
  - service_name:ro
  - container:container_name
  - container:container_name:rw
```

### [`working_dir`](#working_dir)

`working_dir` overrides the container's working directory which is specified by the image, for example Dockerfile's `WORKDIR`.

----
url: https://docs.docker.com/engine/daemon/remote-access/
----

# Configure remote access for Docker daemon

***

Table of contents

***

By default, the Docker daemon listens for connections on a Unix socket to accept requests from local clients. You can configure Docker to accept requests from remote clients by configuring it to listen on an IP address and port as well as the Unix socket.

> Warning
>
> Configuring Docker to accept connections from remote clients can leave you vulnerable to unauthorized access to the host and other attacks.
>
> It's critically important that you understand the security implications of opening Docker to the network. If steps aren't taken to secure the connection, it's possible for remote non-root users to gain root access on the host.
>
> Remote access without TLS is **not recommended**, and will require explicit opt-in in a future release. For more information on how to use TLS certificates to secure this connection, see [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/).

## [Enable remote access](#enable-remote-access)

You can enable remote access to the daemon either using a `docker.service` systemd unit file for Linux distributions using systemd. Or you can use the `daemon.json` file, if your distribution doesn't use systemd.

Configuring Docker to listen for connections using both the systemd unit file and the `daemon.json` file causes a conflict that prevents Docker from starting.

### [Configuring remote access with systemd unit file](#configuring-remote-access-with-systemd-unit-file)

1. Use the command `sudo systemctl edit docker.service` to open an override file for `docker.service` in a text editor.

2. Add or modify the following lines, substituting your own values.

   ```systemd
   [Service]
   ExecStart=
   ExecStart=/usr/bin/dockerd -H fd:// -H tcp://127.0.0.1:2375
   ```

3. Save the file.

4. Reload the `systemctl` configuration.

   ```console
   $ sudo systemctl daemon-reload
   ```

5. Restart Docker.

   ```console
   $ sudo systemctl restart docker.service
   ```

6. Verify that the change has gone through.

   ```console
   $ sudo netstat -lntp | grep dockerd
   tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
   ```

### [Configuring remote access with `daemon.json`](#configuring-remote-access-with-daemonjson)

1. Set the `hosts` array in the `/etc/docker/daemon.json` to connect to the Unix socket and an IP address, as follows:

   ```json
   {
     "hosts": ["unix:///var/run/docker.sock", "tcp://127.0.0.1:2375"]
   }
   ```

2. Restart Docker.

3. Verify that the change has gone through.

   ```console
   $ sudo netstat -lntp | grep dockerd
   tcp        0      0 127.0.0.1:2375          0.0.0.0:*               LISTEN      3758/dockerd
   ```

### [Allow access to the remote API through a firewall](#allow-access-to-the-remote-api-through-a-firewall)

If you run a firewall on the same host as you run Docker, and you want to access the Docker Remote API from another remote host, you must configure your firewall to allow incoming connections on the Docker port. The default port is `2376` if you're using TLS encrypted transport, or `2375` otherwise.

Two common firewall daemons are:

* [Uncomplicated Firewall (ufw)](https://help.ubuntu.com/community/UFW), often used for Ubuntu systems.
* [firewalld](https://firewalld.org), often used for RPM-based systems.

Consult the documentation for your OS and firewall. The following information might help you get started. The settings used in this instruction are permissive, and you may want to use a different configuration that locks your system down more.

* For ufw, set `DEFAULT_FORWARD_POLICY="ACCEPT"` in your configuration.

* For firewalld, add rules similar to the following to your policy. One for incoming requests, and one for outgoing requests.

  ```xml
  <direct>
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -i zt0 -j ACCEPT </rule> ]
    [ <rule ipv="ipv6" table="filter" chain="FORWARD_direct" priority="0"> -o zt0 -j ACCEPT </rule> ]
  </direct>
  ```

  Make sure that the interface names and chain names are correct.

## [Additional information](#additional-information)

For more detailed information on configuration options for remote access to the daemon, refer to the [dockerd CLI reference](/reference/cli/dockerd/#bind-docker-to-another-hostport-or-a-unix-socket).

----
url: https://docs.docker.com/build/ci/github-actions/github-builder/
----

# Docker GitHub Builder

***

***

Docker GitHub Builder is a set of [reusable workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows) in the [`docker/github-builder` repository](https://github.com/docker/github-builder) for building container images and local artifacts with [BuildKit](https://docs.docker.com/build/buildkit/). This section explains what the workflows solve, how they differ from wiring together individual GitHub Actions in each repository, and when to use [`build.yml`](https://docs.docker.com/build/ci/github-actions/github-builder/build/) or [`bake.yml`](https://docs.docker.com/build/ci/github-actions/github-builder/bake/).

If you compose a build job from `docker/login-action`, `docker/setup-buildx-action`, `docker/metadata-action`, and either `docker/build-push-action` or `docker/bake-action`, your repository owns every detail of how the build runs. That approach works, but it also means every repository has to maintain its own runner selection, [cache setup](https://docs.docker.com/build/ci/github-actions/cache/), [Provenance settings](https://docs.docker.com/build/ci/github-actions/attestations/), signing behavior, and [multi-platform manifest handling](https://docs.docker.com/build/ci/github-actions/multi-platform/). Docker GitHub Builder moves that implementation into Docker-maintained reusable workflows, so your workflow only decides when to build and which inputs to pass.

The difference is easiest to see in the job definition. A conventional workflow spells out each action step:

```yaml
jobs:
  docker:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up QEMU
        uses: docker/setup-qemu-action@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4
        
      - name: Docker meta
        uses: docker/metadata-action@v6
        id: meta
        with:
          images: name/app

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha
```

With Docker GitHub Builder, the same build is a reusable workflow call:

```yaml
jobs:
  build:
    uses: docker/github-builder/.github/workflows/build.yml@v1
    permissions:
      contents: read # to fetch the repository content
      id-token: write # for signing attestation(s) with GitHub OIDC Token
    with:
      output: image
      push: ${{ github.event_name != 'pull_request' }}
      meta-images: name/app
    secrets:
      registry-auths: |
        - registry: docker.io
          username: ${{ vars.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
```

This model gives you a build pipeline that is maintained in the Docker organization, uses a pinned [BuildKit](https://docs.docker.com/build/buildkit/) environment, distributes [multi-platform builds](https://docs.docker.com/build/building/multi-platform/) across runners when that helps, and emits signed [SLSA provenance](https://docs.docker.com/build/metadata/attestations/slsa-provenance/) that records both the source commit and the builder identity.

That tradeoff is intentional. You keep control of when the build runs and which inputs it uses, but the build implementation itself lives in the Docker-maintained workflow rather than in per-repository job steps.

Use [`build.yml`](https://docs.docker.com/build/ci/github-actions/github-builder/build/) when your repository builds from a Dockerfile and the familiar `build-push-action` inputs map cleanly to your workflow. Use [`bake.yml`](https://docs.docker.com/build/ci/github-actions/github-builder/bake/) when your repository already describes builds in a [Bake definition](https://docs.docker.com/build/bake/), or when you want Bake targets, overrides, and variables to stay as the source of truth.

Both workflows support image output, local output, cache export to the [GitHub Actions cache backend](https://docs.docker.com/build/cache/backends/gha/), [SBOM generation](https://docs.docker.com/build/metadata/attestations/sbom/), and signing. The Bake workflow adds Bake definition validation and builds one target per workflow call.

* [Docker GitHub Builder architecture](/build/ci/github-actions/github-builder/architecture/)

* [Build with Docker GitHub Builder](/build/ci/github-actions/github-builder/build/)

* [Bake with Docker GitHub Builder](/build/ci/github-actions/github-builder/bake/)

----
url: https://docs.docker.com/desktop/setup/sign-in/
----

# Sign in to Docker Desktop

***

Table of contents

***

Docker recommends signing in with the **Sign in** option in the top-right corner of the Docker Dashboard.

In large enterprises where admin access is restricted, administrators can [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

> Tip
>
> Explore [Docker's core subscriptions](https://www.docker.com/pricing?ref=Docs\&refAction=DocsDesktopSignIn) to see what else Docker can offer you.

## [Benefits of signing in](#benefits-of-signing-in)

* Access your Docker Hub repositories directly from Docker Desktop.

* Increase your pull rate limit compared to anonymous users. See [Usage and limits](https://docs.docker.com/docker-hub/usage/).

* Enhance your organization’s security posture for containerized development with [Hardened Desktop](https://docs.docker.com/enterprise/security/hardened-desktop/).

> Note
>
> Docker Desktop automatically signs you out after 90 days, or after 30 days of inactivity.

## [Signing in with Docker Desktop for Linux](#signing-in-with-docker-desktop-for-linux)

Docker Desktop for Linux relies on [`pass`](https://www.passwordstore.org/) to store credentials in GPG-encrypted files. Before signing in to Docker Desktop with your [Docker ID](/accounts/create-account/), you must initialize `pass`. Docker Desktop displays a warning if `pass` is not configured.

1. Generate a GPG key. You can initialize pass by using a gpg key. To generate a gpg key, run:

   ```console
   $ gpg --generate-key
   ```

2. Enter your name and email once prompted.

   Once confirmed, GPG creates a key pair. Look for the `pub` line that contains your GPG ID, for example:

   ```text
   ...
   pubrsa3072 2022-03-31 [SC] [expires: 2024-03-30]
    3ABCD1234EF56G78
   uid          Molly <molly@example.com>
   ```

3. Copy the GPG ID and use it to initialize `pass`. For example

   ```console
   $ pass init 3ABCD1234EF56G78
   ```

   You should see output similar to:

   ```text
   mkdir: created directory '/home/molly/.password-store/'
   Password store initialized for <generated_gpg-id_public_key>
   ```

Once you initialize `pass`, you can sign in and pull your private images. When Docker CLI or Docker Desktop use credentials, a user prompt may pop up for the password you set during the GPG key generation.

```console
$ docker pull molly/privateimage
Using default tag: latest
latest: Pulling from molly/privateimage
3b9cc81c3203: Pull complete 
Digest: sha256:3c6b73ce467f04d4897d7a7439782721fd28ec9bf62ea2ad9e81a5fb7fb3ff96
Status: Downloaded newer image for molly/privateimage:latest
docker.io/molly/privateimage:latest
```

## [What's next?](#whats-next)

* [Explore Docker Desktop](https://docs.docker.com/desktop/use-desktop/) and its features.
* Change your [Docker Desktop settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/).
* [Browse common FAQs](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/).

----
url: https://docs.docker.com/reference/api/engine/version/v1.51/
----

# Docker Engine API (1.51)

Download OpenAPI specification:[Download](https://docs.docker.com/reference/api/engine/version/v1.51.yaml)

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

If you omit the version-prefix, the current version of the API (v1.50) is used. For example, calling `/info` is the same as calling `/v1.51/info`. Using the API without a version-prefix is deprecated and will be removed in a future release.

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

/v1.51/containers/json

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

/v1.51/containers/create

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

/v1.51/containers/{id}/json

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

/v1.51/containers/{id}/top

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

/v1.51/containers/{id}/logs

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

/v1.51/containers/{id}/changes

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

/v1.51/containers/{id}/export

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

/v1.51/containers/{id}/stats

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

/v1.51/containers/{id}/resize

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

/v1.51/containers/{id}/start

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

/v1.51/containers/{id}/stop

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

/v1.51/containers/{id}/restart

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

/v1.51/containers/{id}/kill

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

|                    |                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CpuShares          | integerAn integer value representing this container's relative CPU weight versus other containers.                                                                                                                                                                                                                                                                                                          |
| Memory             | integer \<int64>Default: 0Memory limit in bytes.                                                                                                                                                                                                                                                                                                                                                            |
| CgroupParent       | stringPath to `cgroups` under which the container's `cgroup` is created. If the path is not absolute, the path is considered to be relative to the `cgroups` path of the init process. Cgroups are created if they do not already exist.                                                                                                                                                                    |
| BlkioWeight        | integer \[ 0 .. 1000 ]Block IO weight (relative weight).                                                                                                                                                                                                                                                                                                                                                    |
|                    | Array of objectsBlock IO weight (relative device weight) in the form:```
[{"Path": "device_path", "Weight": weight}]
```                                                                                                                                                                                                                                                                                    |
|                    | Array of objects (ThrottleDevice)Limit read rate (bytes per second) from a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                                                                                                                                                                              |
|                    | Array of objects (ThrottleDevice)Limit write rate (bytes per second) to a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                                                                                                                                                                               |
|                    | Array of objects (ThrottleDevice)Limit read rate (IO per second) from a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                                                                                                                                                                                 |
|                    | Array of objects (ThrottleDevice)Limit write rate (IO per second) to a device, in the form:```
[{"Path": "device_path", "Rate": rate}]
```                                                                                                                                                                                                                                                                  |
| CpuPeriod          | integer \<int64>The length of a CPU period in microseconds.                                                                                                                                                                                                                                                                                                                                                 |
| CpuQuota           | integer \<int64>Microseconds of CPU time that the container can get in a CPU period.                                                                                                                                                                                                                                                                                                                        |
| CpuRealtimePeriod  | integer \<int64>The length of a CPU real-time period in microseconds. Set to 0 to allocate no time allocated to real-time tasks.                                                                                                                                                                                                                                                                            |
| CpuRealtimeRuntime | integer \<int64>The length of a CPU real-time runtime in microseconds. Set to 0 to allocate no time allocated to real-time tasks.                                                                                                                                                                                                                                                                           |
| CpusetCpus         | stringCPUs in which to allow execution (e.g., `0-3`, `0,1`).                                                                                                                                                                                                                                                                                                                                                |
| CpusetMems         | stringMemory nodes (MEMs) in which to allow execution (0-3, 0,1). Only effective on NUMA systems.                                                                                                                                                                                                                                                                                                           |
|                    | Array of objects (DeviceMapping)A list of devices to add to the container.                                                                                                                                                                                                                                                                                                                                  |
| DeviceCgroupRules  | Array of stringsa list of cgroup rules to apply to the container                                                                                                                                                                                                                                                                                                                                            |
|                    | Array of objects (DeviceRequest)A list of requests for devices to be sent to device drivers.                                                                                                                                                                                                                                                                                                                |
| KernelMemoryTCP    | integer \<int64>Hard limit for kernel TCP buffer memory (in bytes). Depending on the OCI runtime in use, this option may be ignored. It is no longer supported by the default (runc) runtime.This field is omitted when empty.**Deprecated**: This field is deprecated as kernel 6.12 has deprecated `memory.kmem.tcp.limit_in_bytes` field for cgroups v1. This field will be removed in a future release. |
| MemoryReservation  | integer \<int64>Memory soft limit in bytes.                                                                                                                                                                                                                                                                                                                                                                 |
| MemorySwap         | integer \<int64>Total memory limit (memory + swap). Set as `-1` to enable unlimited swap.                                                                                                                                                                                                                                                                                                                   |
| MemorySwappiness   | integer \<int64> \[ 0 .. 100 ]Tune a container's memory swappiness behavior. Accepts an integer between 0 and 100.                                                                                                                                                                                                                                                                                          |
| NanoCpus           | integer \<int64>CPU quota in units of 10-9 CPUs.                                                                                                                                                                                                                                                                                                                                                            |
| OomKillDisable     | booleanDisable OOM Killer for the container.                                                                                                                                                                                                                                                                                                                                                                |
| Init               | boolean or nullRun an init inside the container that forwards signals and reaps processes. This field is omitted if empty, and the default (as configured on the daemon) is used.                                                                                                                                                                                                                           |
| PidsLimit          | integer or null \<int64>Tune a container's PIDs limit. Set `0` or `-1` for unlimited, or `null` to not change.                                                                                                                                                                                                                                                                                              |
|                    | Array of objectsA list of resource limits to set in the container. For example:```
{"Name": "nofile", "Soft": 1024, "Hard": 2048}
```                                                                                                                                                                                                                                                                       |
| CpuCount           | integer \<int64>The number of usable CPUs (Windows only).On Windows Server containers, the processor resource controls are mutually exclusive. The order of precedence is `CPUCount` first, then `CPUShares`, and `CPUPercent` last.                                                                                                                                                                        |
| CpuPercent         | integer \<int64>The usable percentage of the available CPUs (Windows only).On Windows Server containers, the processor resource controls are mutually exclusive. The order of precedence is `CPUCount` first, then `CPUShares`, and `CPUPercent` last.                                                                                                                                                      |
| IOMaximumIOps      | integer \<int64>Maximum IOps for the container system drive (Windows only)                                                                                                                                                                                                                                                                                                                                  |
| IOMaximumBandwidth | integer \<int64>Maximum IO in bytes per second for the container system drive (Windows only).                                                                                                                                                                                                                                                                                                               |
|                    | object (RestartPolicy)The behavior to apply when the container exits. The default is not to restart.An ever increasing delay (double the previous delay, starting at 100ms) is added before each restart to prevent flooding the server.                                                                                                                                                                    |

### Responses

/v1.51/containers/{id}/update

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

/v1.51/containers/{id}/rename

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

/v1.51/containers/{id}/pause

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

/v1.51/containers/{id}/unpause

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

/v1.51/containers/{id}/attach

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

/v1.51/containers/{id}/attach/ws

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

/v1.51/containers/{id}/wait

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

/v1.51/containers/{id}

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

/v1.51/containers/{id}/archive

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

/v1.51/containers/{id}/archive

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

/v1.51/containers/{id}/archive

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

/v1.51/containers/prune

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

/v1.51/images/json

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

/v1.51/build

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

/v1.51/build/prune

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

/v1.51/images/create

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

/v1.51/images/{name}/json

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
"User": "web:web",
"ExposedPorts": {
"80/tcp": { },
"443/tcp": { }
},
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

/v1.51/images/{name}/history

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

/v1.51/images/{name}/push

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

/v1.51/images/{name}/tag

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

|           |                                                                                                                                                     |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| force     | booleanDefault: falseRemove the image even if it is being used by stopped containers or has other tags                                              |
| noprune   | booleanDefault: falseDo not delete untagged parent images                                                                                           |
| platforms | Array of stringsSelect platform-specific content to delete. Multiple values are accepted. Each platform is a OCI platform encoded as a JSON string. |

### Responses

/v1.51/images/{name}

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

/v1.51/images/search

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

/v1.51/images/prune

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

/v1.51/commit

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

/v1.51/images/{name}/get

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

/v1.51/images/get

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

/v1.51/images/load

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

/v1.51/networks

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

/v1.51/networks/{id}

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

/v1.51/networks/{id}

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

/v1.51/networks/create

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

/v1.51/networks/{id}/connect

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

/v1.51/networks/{id}/disconnect

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

/v1.51/networks/prune

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

/v1.51/volumes

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

/v1.51/volumes/create

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

/v1.51/volumes/{name}

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

/v1.51/volumes/{name}

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

/v1.51/volumes/{name}

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

/v1.51/volumes/prune

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

/v1.51/containers/{id}/exec

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

/v1.51/exec/{id}/start

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

/v1.51/exec/{id}/resize

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

/v1.51/exec/{id}/json

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

/v1.51/swarm

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

/v1.51/swarm/init

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

/v1.51/swarm/join

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

/v1.51/swarm/leave

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

/v1.51/swarm/update

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

/v1.51/swarm/unlockkey

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

/v1.51/swarm/unlock

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

/v1.51/nodes

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

/v1.51/nodes/{id}

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

/v1.51/nodes/{id}

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

/v1.51/nodes/{id}/update

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

/v1.51/services

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

/v1.51/services/create

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

/v1.51/services/{id}

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

/v1.51/services/{id}

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

/v1.51/services/{id}/update

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

/v1.51/services/{id}/logs

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

/v1.51/tasks

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

/v1.51/tasks/{id}

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

/v1.51/tasks/{id}/logs

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

/v1.51/secrets

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

/v1.51/secrets/create

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

/v1.51/secrets/{id}

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

/v1.51/secrets/{id}

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

/v1.51/secrets/{id}/update

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

/v1.51/configs

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

/v1.51/configs/create

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

/v1.51/configs/{id}

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

/v1.51/configs/{id}

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

/v1.51/configs/{id}/update

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

/v1.51/plugins

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
"DockerVersion": "string",
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

/v1.51/plugins/privileges

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

/v1.51/plugins/pull

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

/v1.51/plugins/{name}/json

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
"DockerVersion": "string",
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

/v1.51/plugins/{name}

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
"DockerVersion": "string",
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

/v1.51/plugins/{name}/enable

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

/v1.51/plugins/{name}/disable

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

/v1.51/plugins/{name}/upgrade

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

/v1.51/plugins/create

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

/v1.51/plugins/{name}/push

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

/v1.51/plugins/{name}/set

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

/v1.51/auth

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

/v1.51/info

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
"DiscoveredDevices": [
{
"Source": "cdi",
"ID": "vendor.com/gpu=0"
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

/v1.51/version

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

/v1.51/\_ping

## [](#tag/System/operation/SystemPingHead)Ping

This is a dummy endpoint you can use to test if the server is accessible.

### Responses

/v1.51/\_ping

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

/v1.51/events

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

/v1.51/system/df

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

/v1.51/distribution/{name}/json

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

/v1.51/session

----
