url: https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/
----

# Testing an ASP.NET Core web app with Testcontainers

Table of contents

***

Learn how to test an ASP.NET Core web app using Testcontainers for .NET with a real Microsoft SQL Server instance instead of SQLite.

**Time to complete** 25 minutes

In this guide, you'll learn how to:

* Use Testcontainers for .NET to spin up a Microsoft SQL Server container for integration tests
* Replace SQLite with a production-like database provider in ASP.NET Core tests
* Customize `WebApplicationFactory` to configure test dependencies with Testcontainers
* Manage container lifecycle with xUnit's `IAsyncLifetime`

## [Prerequisites](#prerequisites)

* .NET 8.0+ SDK
* A code editor or IDE (Visual Studio, VS Code, Rider)
* A Docker environment supported by Testcontainers. For details, see the [Testcontainers .NET system requirements](https://dotnet.testcontainers.org/supported_docker_environment/).

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/create-project/)

   Set up an ASP.NET Core Razor Pages project with integration test dependencies.

2. [Write tests](https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/write-tests/)

   Replace SQLite with a real Microsoft SQL Server using Testcontainers for .NET.

3. [Run tests](https://docs.docker.com/guides/testcontainers-dotnet-aspnet-core/run-tests/)

   Run the Testcontainers-based integration tests and explore next steps.

----
