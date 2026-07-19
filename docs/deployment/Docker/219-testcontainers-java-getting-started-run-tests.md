url: https://docs.docker.com/guides/testcontainers-java-getting-started/run-tests/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Run tests and next steps

***

Table of contents

***

## [Run the tests](#run-the-tests)

Run the tests using Maven:

```console
$ mvn test
```

You can see in the logs that Testcontainers pulls the Postgres Docker image from Docker Hub (if not already available locally), starts the container, and runs the test.

Writing an integration test using Testcontainers works like writing a unit test that you can run from your IDE. Your teammates can clone the project and run tests without installing Postgres on their machines.

## [Summary](#summary)

The Testcontainers for Java library helps you write integration tests using the same type of database (Postgres) that you use in production, instead of mocks. Because you aren't using mocks and instead talk to real services, you're free to refactor code and still verify that the application works as expected.

In addition to Postgres, Testcontainers provides dedicated modules for many SQL databases, NoSQL databases, messaging queues, and more. You can use Testcontainers to run any containerized dependency for your tests.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [Testcontainers container lifecycle management using JUnit 5](https://testcontainers.com/guides/testcontainers-container-lifecycle/)
* [Replace H2 with a real database for testing](https://testcontainers.com/guides/replace-h2-with-real-database-for-testing/)
* [Getting started with Testcontainers in a Java Spring Boot project](https://testcontainers.com/guides/testing-spring-boot-rest-api-using-testcontainers/)

----
