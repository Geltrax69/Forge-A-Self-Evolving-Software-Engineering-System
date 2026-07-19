url: https://docs.docker.com/guides/testcontainers-go-getting-started/
----

# Getting started with Testcontainers for Go

Table of contents

***

Learn how to create a Go application and test database interactions using Testcontainers for Go with a real PostgreSQL instance.

**Time to complete** 20 minutes

In this guide, you will learn how to:

* Create a Go application with modules support
* Implement a Repository to manage customer data in a PostgreSQL database using the pgx driver
* Write integration tests using testcontainers-go
* Reuse containers across multiple tests using test suites

## [Prerequisites](#prerequisites)

* Go 1.25+
* Your preferred IDE (VS Code, GoLand)
* A Docker environment supported by Testcontainers. For details, see the [testcontainers-go system requirements](https://golang.testcontainers.org/system_requirements/).

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-go-getting-started/create-project/)

   Set up a Go project with a PostgreSQL-backed repository.

2. [Write tests](https://docs.docker.com/guides/testcontainers-go-getting-started/write-tests/)

   Write your first integration test using testcontainers-go and PostgreSQL.

3. [Test suites](https://docs.docker.com/guides/testcontainers-go-getting-started/test-suites/)

   Share a single Postgres container across multiple tests using testify suites.

4. [Run tests](https://docs.docker.com/guides/testcontainers-go-getting-started/run-tests/)

----
