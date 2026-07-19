url: https://docs.docker.com/guides/lab-agentic-apps/
----

[Lab: Building Agentic Apps with Docker](https://docs.docker.com/guides/lab-agentic-apps/)

Hands-on lab: Build agentic apps with Docker Model Runner, MCP Gateway, and Compose. Learn about models, tools, and agentic frameworks.

AI Labs

20 minutes

Resources:

* [Docker Model Runner docs](/ai/model-runner/)
* [Docker MCP Gateway docs](/ai/mcp-gateway/)
* [Labspace repository](https://github.com/dockersamples/labspace-agentic-apps-with-docker)

[« Back to all guides](/guides/)

# Lab: Building Agentic Apps with Docker

***

Table of contents

***

Get up and running with building agentic applications using Compose, Docker Model Runner, and the Docker MCP Gateway. This hands-on lab takes you from understanding AI models to building complete agentic applications.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-agentic-apps-with-docker up -d
   ```

   > Note
   >
   > This lab uses an AI model, which requires [the Docker Model Runner to be enabled](https://docs.docker.com/ai/model-runner/get-started/). The model may take some time to download.

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

This lab covers three core areas of agentic application development:

**Models**: What models are, how to interact with them, configuring Docker Model Runner in Compose, and writing code that connects to the Model Runner

**Tools**: Understanding tools and how they work, how MCP (Model Context Protocol) fits in, configuring the Docker MCP Gateway, and connecting to the MCP Gateway in code

**Code**: What agentic frameworks are, defining models and tools in a Compose file, and configuring your app to use those models and tools

## [Modules](#modules)

| # | Module                           | Description                                              |
| - | -------------------------------- | -------------------------------------------------------- |
| 1 | Introduction                     | Overview of agentic applications and the Docker AI stack |
| 2 | Understanding Model Interactions | Learn how to interact with AI models                     |
| 3 | The Docker Model Runner          | Configure and use Docker Model Runner with Compose       |
| 4 | Understanding Tools and MCP      | Deep dive into tools, tool calling, and MCP              |
| 5 | The Docker MCP Gateway           | Set up and configure the MCP Gateway                     |
| 6 | Putting It All Together          | Build a complete agentic application                     |
| 7 | Conclusion                       | Summary and next steps                                   |

----
