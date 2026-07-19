url: https://docs.docker.com/guides/testcontainers-java-jooq-flyway/run-tests/
----

# Run tests and next steps

***

Table of contents

***

## [Run the tests](#run-the-tests)

```console
$ ./mvnw test
```

You should see the PostgreSQL Docker container start, jOOQ code generation complete, and all tests pass. After the tests finish, the container stops and is removed automatically.

## [Summary](#summary)

The Testcontainers library helps you generate Java code from the database using the jOOQ code generator and test your persistence layer against the same type of database (PostgreSQL) that you use in production, instead of mocks or in-memory databases.

Because the code is always generated from the database's current state, you can be confident that your code stays in sync with database changes. You're free to refactor and still verify that the application works as expected.

To learn more about Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/).

## [Further reading](#further-reading)

* [jOOQ documentation](https://www.jooq.org/)
* [jOOQ code generation](https://www.jooq.org/doc/latest/manual/code-generation/)
* [Spring Boot Testcontainers support](https://docs.spring.io/spring-boot/reference/testing/testcontainers.html)
* [Replace H2 with a real database for testing](/guides/testcontainers-java-replace-h2/)

----
