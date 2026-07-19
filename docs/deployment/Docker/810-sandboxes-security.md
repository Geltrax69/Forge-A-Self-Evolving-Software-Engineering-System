url: https://docs.docker.com/ai/sandboxes/security/
----

# Security model

***

Table of contents

***

Docker Sandboxes run AI agents in microVMs so they can execute code, install packages, and use tools without accessing your host system. Multiple isolation layers protect your host system.

## [Trust boundaries](#trust-boundaries)

The primary trust boundary is the microVM. The agent has full control inside the VM, including sudo access. The VM boundary prevents the agent from reaching anything on your host except what is explicitly shared.

What crosses the boundary into the VM:

* **Workspace directory:** mounted into the VM. The default direct mount is read-write — the agent edits your working tree in place. With [`--clone`](https://docs.docker.com/ai/sandboxes/usage/#clone-mode), your repository is mounted read-only and the agent works on a private clone.
* **Credentials:** the host-side proxy injects authentication headers into outbound HTTP requests. The raw credential values never enter the VM.
* **Network access:** HTTP and HTTPS requests to [allowed domains](https://docs.docker.com/ai/sandboxes/security/defaults/) are proxied through the host.

What crosses the boundary back to the host:

* **Workspace file changes:** visible on your host in real time with the default direct mount.
* **HTTP/HTTPS requests:** sent to allowed domains through the host proxy.

Everything else is blocked. The agent cannot access your host filesystem (outside the workspace), your host Docker daemon, your host network or localhost, other sandboxes, or any domain not in the allow list. Raw TCP, UDP, and ICMP are blocked at the network layer.

## [Isolation layers](#isolation-layers)

The sandbox security model has five layers. See [Isolation layers](https://docs.docker.com/ai/sandboxes/security/isolation/) for technical details on each.

* **Hypervisor isolation:** separate kernel per sandbox. No shared memory or processes with the host.
* **Network isolation:** all HTTP/HTTPS traffic proxied through the host. [Deny-by-default policy](https://docs.docker.com/ai/sandboxes/security/defaults/). Non-HTTP protocols blocked entirely.
* **Docker Engine isolation:** each sandbox has its own Docker Engine with no path to the host daemon.
* **Workspace isolation** (opt-in via `--clone`): the agent works on a private in-VM clone and your repository is mounted read-only. The default direct mode applies no workspace boundary — the agent edits your working tree in place.
* **Credential isolation:** API keys are injected into HTTP headers by the host-side proxy. Credential values never enter the VM.

## [What the agent can do inside the sandbox](#what-the-agent-can-do-inside-the-sandbox)

Inside the VM, the agent has full privileges: sudo access, package installation, a private Docker Engine, and read-write access to the workspace. Installed packages, Docker images, and other VM state persist across restarts. See [Default security posture](https://docs.docker.com/ai/sandboxes/security/defaults/) for the full breakdown of what is permitted and what is blocked.

## [What is not isolated by default](#what-is-not-isolated-by-default)

The sandbox isolates the agent from your host system, but the agent's actions can still affect you through the shared workspace and allowed network channels.

In direct mode, workspace changes are live on your host. With the default direct mount, the agent edits the same files you see on your host. This includes files that execute implicitly during normal development: Git hooks, CI configuration, IDE task configs, `Makefile`, `package.json` scripts, and similar build files. Review changes before running any modified code. Note that Git hooks live inside `.git/` and do not appear in `git diff` output — check them separately. See [Workspace isolation](https://docs.docker.com/ai/sandboxes/security/isolation/#workspace-isolation) for the full list and for the alternative clone-mode boundary.

The default allowed domains include broad wildcards. Some defaults like `*.googleapis.com` cover many services beyond AI APIs. Run `sbx policy ls` to see the full list of active rules, and remove entries you don't need. See [Default security posture](https://docs.docker.com/ai/sandboxes/security/defaults/).

## [Organization-wide control](#organization-wide-control)

On a single developer's machine, security and policy are configured locally — for example, network and filesystem rules set with `sbx policy`. Admins can move these controls to the organization level so that security, policy, and access apply consistently across every developer's sandboxes, rather than depending on local configuration.

See [Governance](https://docs.docker.com/ai/sandboxes/governance/) for the controls available to organization admins.

## [Learn more](#learn-more)

* [Isolation layers](https://docs.docker.com/ai/sandboxes/security/isolation/): how hypervisor, network, Docker, workspace, and credential isolation work
* [Default security posture](https://docs.docker.com/ai/sandboxes/security/defaults/): what a fresh sandbox permits and blocks
* [Credentials](https://docs.docker.com/ai/sandboxes/security/credentials/): how to provide and manage API keys
* [Governance](https://docs.docker.com/ai/sandboxes/governance/): configure network and filesystem access rules, locally or across your organization

----
