url: https://docs.docker.com/guides/cpp/containerize/
----

# Containerize a C++ application

***

Table of contents

***

## [Prerequisites](#prerequisites)

* You have a [Git client](https://git-scm.com/downloads). The examples in this section use a command-line based Git client, but you can use any client.

## [Overview](#overview)

This section walks you through containerizing and running a C++ application, using Docker Compose.

## [Get the sample application](#get-the-sample-application)

We're using the same sample repository that you used in the previous sections of this guide. If you haven't already cloned the repository, clone it now:

```console
$ git clone https://github.com/dockersamples/c-plus-plus-docker.git
```

You should now have the following contents in your `c-plus-plus-docker` (root) directory.

```text
├── c-plus-plus-docker/
│ ├── compose.yml
│ ├── Dockerfile
│ ├── LICENSE
│ ├── ok_api.cpp
│ └── README.md
```

To learn more about the files in the repository, see the following:

* [Dockerfile](https://docs.docker.com/reference/dockerfile/)
* [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
* [compose.yml](https://docs.docker.com/reference/compose-file/)

## [Run the application](#run-the-application)

Inside the `c-plus-plus-docker` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:8080>. You will see a message `{"Status" : "OK"}` in the browser.

In the terminal, press `ctrl`+`c` to stop the application.

### [Run the application in the background](#run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option. Inside the `c-plus-plus-docker` directory, run the following command in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at <http://localhost:8080>.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

## [Summary](#summary)

In this section, you learned how you can containerize and run your C++ application using Docker.

Related information:

* [Docker Compose overview](https://docs.docker.com/compose/)

## [Next steps](#next-steps)

In the next section, you'll learn how you can develop your application using containers.

[Use containers for C++ development »](https://docs.docker.com/guides/cpp/develop/)

----
