url: https://docs.docker.com/ai/gordon/how-to/cli/
----

# Using Gordon via CLI

***

Table of contents

***

Requires: Docker Desktop [4.74.0](https://docs.docker.com/desktop/release-notes/#4740) or later

The `docker ai` command provides a Terminal User Interface (TUI) for Gordon, integrating AI assistance directly into your terminal.

## [Basic usage](#basic-usage)

Launch the interactive TUI:

```console
$ docker ai
```

This opens Gordon's terminal interface where you can type prompts, approve actions, and continue conversations with full context.

Pass a prompt directly as an argument:

```console
$ docker ai "list my running containers"
```

Exit the TUI with `/exit` or `Ctrl+C`.

## [Working directory](#working-directory)

The working directory sets the default context for Gordon's file operations.

Gordon uses your current shell directory as the working directory:

```console
$ cd ~/my-project
$ docker ai
```

Override with `-C` or `--working-dir`:

```console
$ docker ai -C ~/different-project
```

## [Disabling Gordon](#disabling-gordon)

Gordon CLI is part of Docker Desktop. To disable it, disable Gordon in Docker Desktop Settings:

1. Open Docker Desktop Settings.
2. Navigate to the **AI** section.
3. Clear the **Enable Gordon** option.
4. Select **Apply**.

## [Commands](#commands)

The `docker ai` command includes several subcommands:

Interactive mode (default):

```console
$ docker ai
```

Opens the TUI for conversational interaction.

Version:

```console
$ docker ai version
```

Displays the Gordon version.

Feedback:

```console
$ docker ai feedback
```

Opens a feedback form in your browser.

----
