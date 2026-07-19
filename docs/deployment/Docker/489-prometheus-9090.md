    url: http://prometheus:9090
    isDefault: true
  ```

  In the `grafana.yml` file, you have defined a Prometheus data source named `Prometheus (Main)`. The `type` field specifies the type of the data source, which is `prometheus`. The `url` field specifies the URL of the Prometheus server to fetch the metrics from. In this case, the URL is `http://prometheus:9090`. `prometheus` is the service name of the Prometheus server in the Docker Compose file. The `isDefault` field specifies whether the data source is the default data source in Grafana.

Apart from the services, the Docker Compose file also defines a volume named `grafana-data` to persist the Grafana data and a network named `go-network` to connect the services together. You have created a custom network `go-network` to connect the services together. The `driver: bridge` field specifies the network driver to use for the network.

## [Building and running the services](#building-and-running-the-services)

Now that you have the Docker Compose file, you can build the services and run them together using Docker Compose.

To build and run the services, run the following command in the terminal:

```console
$ docker compose up
```

The `docker compose up` command builds the services defined in the Docker Compose file and runs them together. You will see the similar output in the terminal:

```console
 ✔ Network go-prometheus-monitoring_go-network  Created                                                           0.0s 
 ✔ Container grafana                            Created                                                           0.3s 
 ✔ Container go-api                             Created                                                           0.2s 
 ✔ Container prometheus                         Created                                                           0.3s 
Attaching to go-api, grafana, prometheus
go-api      | [GIN-debug] [WARNING] Creating an Engine instance with the Logger and Recovery middleware already attached.
go-api      | 
go-api      | [GIN-debug] [WARNING] Running in "debug" mode. Switch to "release" mode in production.
go-api      |  - using env:     export GIN_MODE=release
go-api      |  - using code:    gin.SetMode(gin.ReleaseMode)
go-api      | 
go-api      | [GIN-debug] GET    /metrics                  --> main.PrometheusHandler.func1 (3 handlers)
go-api      | [GIN-debug] GET    /health                   --> main.main.func1 (4 handlers)
go-api      | [GIN-debug] GET    /v1/users                 --> main.main.func2 (4 handlers)
go-api      | [GIN-debug] [WARNING] You trusted all proxies, this is NOT safe. We recommend you to set a value.
go-api      | Please check https://pkg.go.dev/github.com/gin-gonic/gin#readme-don-t-trust-all-proxies for details.
go-api      | [GIN-debug] Listening and serving HTTP on :8000
prometheus  | ts=2025-03-15T05:57:06.676Z caller=main.go:627 level=info msg="No time or size retention was set so using the default time retention" duration=15d
prometheus  | ts=2025-03-15T05:57:06.678Z caller=main.go:671 level=info msg="Starting Prometheus Server" mode=server version="(version=2.55.0, branch=HEAD, revision=91d80252c3e528728b0f88d254dd720f6be07cb8)"
grafana     | logger=settings t=2025-03-15T05:57:06.865335506Z level=info msg="Config overridden from command line" arg="default.log.mode=console"
grafana     | logger=settings t=2025-03-15T05:57:06.865337131Z level=info msg="Config overridden from Environment variable" var="GF_PATHS_DATA=/var/lib/grafana"
grafana     | logger=ngalert.state.manager t=2025-03-15T05:57:07.088956839Z level=info msg="State
.
.
grafana     | logger=plugin.angulardetectorsprovider.dynamic t=2025-03-15T05:57:07.530317298Z level=info msg="Patterns update finished" duration=440.489125ms
```

The services will start running, and you can access the Golang application at `http://localhost:8000`, Prometheus at `http://localhost:9090/health`, and Grafana at `http://localhost:3000`. You can also check the running containers using the `docker ps` command.

```console
$ docker ps
```

## [Summary](#summary)

In this section, you learned how to connect services together using Docker Compose. You created a Docker Compose file to run multiple services together and connect them using networks. You also learned how to build and run the services using Docker Compose.

Related information:

* [Docker Compose overview](https://docs.docker.com/compose/)
* [Compose file reference](https://docs.docker.com/reference/compose-file/)

Next, you will learn how to develop the Golang application with Docker Compose and monitor it with Prometheus and Grafana.

## [Next steps](#next-steps)

In the next section, you will learn how to develop the Golang application with Docker. You will also learn how to use Docker Compose Watch to rebuild the image whenever you make changes to the code. Lastly, you will test the application and visualize the metrics in Grafana using Prometheus as the data source.

[Developing your application »](https://docs.docker.com/guides/go-prometheus-monitoring/develop/)

----
url: https://docs.docker.com/compose/
----

# Docker Compose

***

***

Docker Compose is a tool for defining and running multi-container applications. It is the key to unlocking a streamlined and efficient development and deployment experience.

Compose simplifies the control of your entire application stack, making it easy to manage services, networks, and volumes in a single YAML configuration file. Then, with a single command, you create and start all the services from your configuration file.

Compose works in all environments - production, staging, development, testing, as well as CI workflows. It also has commands for managing the whole lifecycle of your application:

* Start, stop, and rebuild services
* View the status of running services
* Stream the log output of running services
* Run a one-off command on a service

### [Why use Compose?](/compose/intro/features-uses/)

[Understand Docker Compose's key benefits](/compose/intro/features-uses/)

### [How Compose works](/compose/intro/compose-application-model/)

[Understand how Compose works](/compose/intro/compose-application-model/)

### [Install Compose](/compose/install)

[Follow the instructions on how to install Docker Compose.](/compose/install)

### [Quickstart](/compose/gettingstarted)

[Learn the key concepts of Docker Compose whilst building a simple Python web application.](/compose/gettingstarted)

### [View the release notes](https://github.com/docker/compose/releases)

[Find out about the latest enhancements and bug fixes.](https://github.com/docker/compose/releases)

### [Explore the Compose file reference](/reference/compose-file)

[Find information on defining services, networks, and volumes for a Docker application.](/reference/compose-file)

### [Use Compose Bridge](/compose/bridge)

[Transform your Compose configuration file into configuration files for different platforms, such as Kubernetes.](/compose/bridge)

### [Browse common FAQs](/compose/faq)

[Explore general FAQs and find out how to give feedback.](/compose/faq)

----
url: https://docs.docker.com/reference/samples/go/
----

# Go samples

| Name                                                                                                   | Description                                                                |
| ------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| [Go / NGINX / MySQL](https://github.com/docker/awesome-compose/tree/master/nginx-golang-mysql)         | A sample Go application with an Nginx proxy and a MySQL database.          |
| [Go / NGINX / PostgreSQL](https://github.com/docker/awesome-compose/tree/master/nginx-golang-postgres) | A sample Go application with an Nginx proxy and a PostgreSQL database.     |
| [NGINX / Go](https://github.com/docker/awesome-compose/tree/master/nginx-golang)                       | A sample Nginx proxy with a Go backend.                                    |
| [Traefik](https://github.com/docker/awesome-compose/tree/master/traefik-golang)                        | A sample Traefik proxy with a Go backend.                                  |
| [wordsmith](https://github.com/dockersamples/wordsmith)                                                | A demo app that runs three containers, including PostgreSQL, Java, and Go. |
| [gopher-task-system](https://github.com/dockersamples/gopher-task-system)                              | A Task System using Go Docker SDK.                                         |

## Looking for more samples?

Visit the following GitHub repositories for more Docker samples.

* [Awesome Compose](https://github.com/docker/awesome-compose): A curated repository containing over 30 Docker Compose samples. These samples offer a starting point for how to integrate different services using a Compose file.

* [Docker Samples](https://github.com/dockersamples?q=\&type=all\&language=\&sort=stargazers): A collection of over 30 repositories that offer sample containerized demo applications, tutorials, and labs.

----
url: https://docs.docker.com/guides/dotnet/develop/
----

# Use containers for .NET development

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/).

## [Overview](#overview)

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

* Adding a local database and persisting data
* Configuring Compose to automatically update your running Compose services as you edit and save your code
* Creating a development container that contains the .NET Core SDK tools and dependencies

## [Update the application](#update-the-application)

This section uses a different branch of the `docker-dotnet-sample` repository that contains an updated .NET application. The updated application is on the `add-db` branch of the repository you cloned in [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/).

To get the updated code, you need to checkout the `add-db` branch. For the changes you made in [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/), for this section, you can stash them. In a terminal, run the following commands in the `docker-dotnet-sample` directory.

1. Stash any previous changes.

   ```console
   $ git stash -u
   ```

2. Check out the new branch with the updated application.

   ```console
   $ git checkout add-db
   ```

In the `add-db` branch, only the .NET application has been updated. None of the Docker assets have been updated yet.

You should now have the following in your `docker-dotnet-sample` directory.

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── src/
│ │ ├── Data/
│ │ ├── Models/
│ │ ├── Pages/
│ │ ├── Properties/
│ │ ├── wwwroot/
│ │ ├── appsettings.Development.json
│ │ ├── appsettings.json
│ │ ├── myWebApp.csproj
│ │ └── Program.cs
│ ├── tests/
│ │ ├── tests.csproj
│ │ ├── UnitTest1.cs
│ │ └── Usings.cs
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

## [Add a local database and persist data](#add-a-local-database-and-persist-data)

You can use containers to set up local services, like a database. In this section, you'll update the `compose.yaml` file to define a database service and a volume to persist data.

Open the `compose.yaml` file in an IDE or text editor. You'll notice it already contains commented-out instructions for a PostgreSQL database and volume.

Open `docker-dotnet-sample/src/appsettings.json` in an IDE or text editor. You'll notice the connection string with all the database information. The `compose.yaml` already contains this information, but it's commented out. Uncomment the database instructions in the `compose.yaml` file.

The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

> Note
>
> To learn more about the instructions in the Compose file, see [Compose file reference](/reference/compose-file/).

Before you run the application using Compose, notice that this Compose file uses `secrets` and specifies a `password.txt` file to hold the database's password. You must create this file as it's not included in the source repository.

In the `docker-dotnet-sample` directory, create a new directory named `db` and inside that directory create a file named `password.txt`. Open `password.txt` in an IDE or text editor and add the following password. The password must be on a single line, with no additional lines in the file.

```text
example
```

Save and close the `password.txt` file.

You should now have the following in your `docker-dotnet-sample` directory.

```text
├── docker-dotnet-sample/
│ ├── .git/
│ ├── db/
│ │ └── password.txt
│ ├── src/
│ ├── tests/
│ ├── .dockerignore
│ ├── .gitignore
│ ├── compose.yaml
│ ├── Dockerfile
│ └── README.md
```

Run the following command to start your application.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:8080>. You should see a simple web application with the text `Student name is`.

The application doesn't display a name because the database is empty. For this application, you need to access the database and then add records.

## [Add records to the database](#add-records-to-the-database)

For the sample application, you must access the database directly to create sample records.

You can run commands inside the database container using the `docker exec` command. Before running that command, you must get the ID of the database container. Open a new terminal window and run the following command to list all your running containers.

```console
$ docker container ls
```

You should see output like the following.

```console
CONTAINER ID   IMAGE                         COMMAND                  CREATED              STATUS                        PORTS                    NAMES
cb36e310aa7e   docker-dotnet-sample-server   "dotnet myWebApp.dll"    About a minute ago   Up About a minute             0.0.0.0:8080->8080/tcp   docker-dotnet-sample-server-1
39fdcf0aff7b   postgres:18                   "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   5432/tcp                 docker-dotnet-sample-db-1
```

In the previous example, the container ID is `39fdcf0aff7b`. Run the following command to connect to the postgres database in the container. Replace the container ID with your own container ID.

```console
$ docker exec -it 39fdcf0aff7b psql -d example -U postgres
```

And finally, insert a record into the database.

```console
example=# INSERT INTO "Students" ("ID", "LastName", "FirstMidName", "EnrollmentDate") VALUES (DEFAULT, 'Whale', 'Moby', '2013-03-20');
```

You should see output like the following.

```console
INSERT 0 1
```

Close the database connection and exit the container shell by running `exit`.

```console
example=# exit
```

## [Verify that data persists in the database](#verify-that-data-persists-in-the-database)

Open a browser and view the application at <http://localhost:8080>. You should see a simple web application with the text `Student name is Moby Whale`.

Press `ctrl+c` in the terminal to stop your application.

In the terminal, run `docker compose rm` to remove your containers and then run `docker compose up` to run your application again.

```console
$ docker compose rm
$ docker compose up --build
```

Refresh <http://localhost:8080> in your browser and verify that the student name persisted, even after the containers were removed and ran again.

Press `ctrl+c` in the terminal to stop your application.

## [Automatically update services](#automatically-update-services)

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yaml` file in an IDE or text editor and then add the Compose Watch instructions. The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: final
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: .
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Open a browser and verify that the application is running at <http://localhost:8080>.

Any changes to the application's source files on your local machine will now be immediately reflected in the running container.

Open `docker-dotnet-sample/src/Pages/Index.cshtml` in an IDE or text editor and update the student name text on line 13 from `Student name is` to `Student name:`.

```diff
-    <p>Student name is @Model.StudentName</p>
+    <p>Student name: @Model.StudentName</p>
```

Save the changes to `Index.cshtml` and then wait a few seconds for the application to rebuild. Refresh <http://localhost:8080> in your browser and verify that the updated text appears.

Press `ctrl+c` in the terminal to stop your application.

## [Create a development container](#create-a-development-container)

At this point, when you run your containerized application, it's using the .NET runtime image. While this small image is good for production, it lacks the SDK tools and dependencies you may need when developing. Also, during development, you may not need to run `dotnet publish`. You can use multi-stage builds to build stages for both development and production in the same Dockerfile. For more details, see [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/).

Add a new development stage to your Dockerfile and update your `compose.yaml` file to use this stage for local development.

The following is the updated Dockerfile.

```Dockerfile
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM dhi.io/dotnet:10-sdk AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM dhi.io/dotnet:10-sdk AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM dhi.io/aspnetcore:10 AS final
WORKDIR /app
COPY --from=build /app .
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

```Dockerfile
# syntax=docker/dockerfile:1

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS build
ARG TARGETARCH
COPY . /source
WORKDIR /source/src
RUN --mount=type=cache,id=nuget,target=/root/.nuget/packages \
    dotnet publish -a ${TARGETARCH/amd64/x64} --use-current-runtime --self-contained false -o /app

FROM mcr.microsoft.com/dotnet/sdk:10.0-alpine AS development
COPY . /source
WORKDIR /source/src
CMD dotnet run --no-launch-profile

FROM mcr.microsoft.com/dotnet/aspnet:10.0-alpine AS final
WORKDIR /app
COPY --from=build /app .
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser
USER appuser
ENTRYPOINT ["dotnet", "myWebApp.dll"]
```

The following is the updated `compose.yaml` file.

```yaml
services:
  server:
    build:
      context: .
      target: development
    ports:
      - 8080:8080
    depends_on:
      db:
        condition: service_healthy
    develop:
      watch:
        - action: rebuild
          path: .
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
  db:
    image: postgres:18
    restart: always
    user: postgres
    secrets:
      - db-password
    volumes:
      - db-data:/var/lib/postgresql
    environment:
      - POSTGRES_DB=example
      - POSTGRES_PASSWORD_FILE=/run/secrets/db-password
    expose:
      - 5432
    healthcheck:
      test: ["CMD", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 5
volumes:
  db-data:
secrets:
  db-password:
    file: db/password.txt
```

Your containerized application will now use the SDK image (either `dhi.io/dotnet:10-sdk` for DHI or `mcr.microsoft.com/dotnet/sdk:10.0-alpine` for official images), which includes development tools like `dotnet test`. Continue to the next section to learn how you can run `dotnet test`.

## [Summary](#summary)

In this section, you took a look at setting up your Compose file to add a local database and persist data. You also learned how to use Compose Watch to automatically rebuild and run your container when you update your code. And finally, you learned how to create a development container that contains the SDK tools and dependencies needed for development.

Related information:

* [Compose file reference](/reference/compose-file/)
* [Compose file watch](https://docs.docker.com/compose/how-tos/file-watch/)
* [Multi-stage builds](https://docs.docker.com/build/building/multi-stage/)

## [Next steps](#next-steps)

In the next section, you'll learn how to run unit tests using Docker.

[Run .NET tests in a container »](https://docs.docker.com/guides/dotnet/run-tests/)

----
url: https://docs.docker.com/desktop/setup/install/mac-permission-requirements/
----

# Understand permission requirements for Docker Desktop on Mac

***

Table of contents

***

This page contains information about the permission requirements for running and installing Docker Desktop on Mac.

It also provides clarity on running containers as `root` as opposed to having `root` access on the host.

Docker Desktop on Mac is designed with security in mind. Administrative rights are only required when absolutely necessary.

## [Permission requirements](#permission-requirements)

Docker Desktop for Mac is run as an unprivileged user. However, Docker Desktop requires certain functionalities to perform a limited set of privileged configurations such as:

* [Installing symlinks](#installing-symlinks) in`/usr/local/bin`.
* [Binding privileged ports](#binding-privileged-ports) that are less than 1024. Although privileged ports (ports below 1024) are not typically used as a security boundary, operating systems still prevent unprivileged processes from binding to them which breaks commands like `docker run -p 127.0.0.1:80:80 docker/getting-started`.
* [Ensuring `localhost` and `kubernetes.docker.internal` are defined](#ensuring-localhost-and-kubernetesdockerinternal-are-defined) in `/etc/hosts`. Some old macOS installs don't have `localhost` in `/etc/hosts`, which causes Docker to fail. Defining the DNS name `kubernetes.docker.internal` allows Docker to share Kubernetes contexts with containers.
* Securely caching the Registry Access Management policy which is read-only for the developer.

Privileged access is granted during installation.

The first time Docker Desktop for Mac launches, it presents an installation window where you can choose to either use the default settings, which work for most developers and requires you to grant privileged access, or use advanced settings.

If you work in an environment with elevated security requirements, for instance where local administrative access is prohibited, then you can use the advanced settings to remove the need for granting privileged access. You can configure:

* The location of the Docker CLI tools either in the system or user directory
* The default Docker socket
* Privileged port mapping

Depending on which advanced settings you configure, you must enter your password to confirm.

You can change these configurations at a later date from the **Advanced** page in **Settings**.

### [Installing symlinks](#installing-symlinks)

The Docker binaries are installed by default in `/Applications/Docker.app/Contents/Resources/bin`. Docker Desktop creates symlinks for the binaries in `/usr/local/bin`, which means they're automatically included in `PATH` on most systems.

You can choose whether to install symlinks either in `/usr/local/bin` or `$HOME/.docker/bin` during installation of Docker Desktop.

If `/usr/local/bin` is chosen, and this location is not writable by unprivileged users, Docker Desktop requires authorization to confirm this choice before the symlinks to Docker binaries are created in `/usr/local/bin`. If `$HOME/.docker/bin` is chosen, authorization is not required, but then you must [manually add `$HOME/.docker/bin`](https://docs.docker.com/desktop/settings-and-maintenance/settings/#advanced) to your PATH.

You are also given the option to enable the installation of the `/var/run/docker.sock` symlink. Creating this symlink ensures various Docker clients relying on the default Docker socket path work without additional changes.

As the `/var/run` is mounted as a tmpfs, its content is deleted on restart, symlink to the Docker socket included. To ensure the Docker socket exists after restart, Docker Desktop sets up a `launchd` startup task that creates the symlink by running `ln -s -f /Users/<user>/.docker/run/docker.sock /var/run/docker.sock`. This ensures the you aren't prompted on each startup to create the symlink. If you don't enable this option at installation, the symlink and the startup task is not created and you may have to explicitly set the `DOCKER_HOST` environment variable to `/Users/<user>/.docker/run/docker.sock` in the clients it is using. The Docker CLI relies on the current context to retrieve the socket path, the current context is set to `desktop-linux` on Docker Desktop startup.

### [Binding privileged ports](#binding-privileged-ports)

You can choose to enable privileged port mapping during installation, or from the **Advanced** page in **Settings** post-installation. Docker Desktop requires authorization to confirm this choice.

### [Ensuring `localhost` and `kubernetes.docker.internal` are defined](#ensuring-localhost-and-kubernetesdockerinternal-are-defined)

It is your responsibility to ensure that localhost is resolved to `127.0.0.1` and if Kubernetes is used, that `kubernetes.docker.internal` is resolved to `127.0.0.1`.

## [Installing from the command line](#installing-from-the-command-line)

Privileged configurations are applied during the installation with the `--user` flag on the [install command](https://docs.docker.com/desktop/setup/install/mac-install/#install-from-the-command-line). In this case, you are not prompted to grant root privileges on the first run of Docker Desktop. Specifically, the `--user` flag:

* Uninstalls the previous `com.docker.vmnetd` if present
* Sets up symlinks
* Ensures that `localhost` is resolved to `127.0.0.1`

The limitation of this approach is that Docker Desktop can only be run by one user-account per machine, namely the one specified in the `-–user` flag.

## [Privileged helper](#privileged-helper)

In the limited situations when the privileged helper is needed, for example binding privileged ports or caching the Registry Access Management policy, the privileged helper is started by `launchd` and runs in the background unless it is disabled at runtime as previously described. The Docker Desktop backend communicates with the privileged helper over the UNIX domain socket `/var/run/com.docker.vmnetd.sock`. The functionalities it performs are:

* Binding privileged ports that are less than 1024.
* Securely caching the Registry Access Management policy which is read-only for the developer.
* Uninstalling the privileged helper.

The removal of the privileged helper process is done in the same way as removing `launchd` processes.

```console
$ ps aux | grep vmnetd
root             28739   0.0  0.0 34859128    228   ??  Ss    6:03PM   0:00.06 /Library/PrivilegedHelperTools/com.docker.vmnetd
user             32222   0.0  0.0 34122828    808 s000  R+   12:55PM   0:00.00 grep vmnetd

$ sudo launchctl unload -w /Library/LaunchDaemons/com.docker.vmnetd.plist
Password:

$ ps aux | grep vmnetd
user             32242   0.0  0.0 34122828    716 s000  R+   12:55PM   0:00.00 grep vmnetd

$ rm /Library/LaunchDaemons/com.docker.vmnetd.plist

$ rm /Library/PrivilegedHelperTools/com.docker.vmnetd
```

## [Containers running as root within the Linux VM](#containers-running-as-root-within-the-linux-vm)

With Docker Desktop, the Docker daemon and containers run in a lightweight Linux VM managed by Docker. This means that although containers run by default as `root`, this doesn't grant `root` access to the Mac host machine. The Linux VM serves as a security boundary and limits what resources can be accessed from the host. Any directories from the host bind mounted into Docker containers still retain their original permissions.

## [Enhanced Container Isolation](#enhanced-container-isolation)

In addition, Docker Desktop supports [Enhanced Container Isolation mode](https://docs.docker.com/enterprise/security/hardened-desktop/enhanced-container-isolation/) (ECI), available to Business customers only, which further secures containers without impacting developer workflows.

ECI automatically runs all containers within a Linux user-namespace, such that root in the container is mapped to an unprivileged user inside the Docker Desktop VM. ECI uses this and other advanced techniques to further secure containers within the Docker Desktop Linux VM, such that they are further isolated from the Docker daemon and other services running inside the VM.

----
url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/profiles/
----

# MCP Profiles

***

Table of contents

***

Availability: Early Access

Requires: Docker Desktop 4.63 and later

Profiles organize your MCP servers into named collections. Without profiles, you'd configure servers separately for every AI application you use. Each time you want to change which servers are available, you'd update Claude Desktop, VS Code, Cursor, and other tools individually. Profiles solve this by centralizing your server configurations.

## [What profiles do](#what-profiles-do)

A profile is a named collection of MCP servers with their configurations and settings. You select servers from the [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/) (the source of available servers) and add them to your profiles (your configured server collections for specific work). Think of the catalog as a library of tools, and profiles as your toolboxes organized for different jobs.

Your "web-dev" profile might include GitHub, Playwright, and database servers. Your "data-analysis" profile might include spreadsheet, API, and visualization servers. Connect different AI clients to different profiles, or switch between profiles as you change tasks.

When you run the MCP Gateway or connect a client without specifying a profile, Docker MCP uses your default profile. If you're upgrading from a previous version of MCP Toolkit, your existing server configurations are already in the default profile.

## [Profile capabilities](#profile-capabilities)

Each profile maintains its own isolated collection of servers and configurations. Your "web-dev" profile might include GitHub, Playwright, and database servers, while your "data-analysis" profile includes spreadsheet, API, and visualization servers. Create as many profiles as you need, each containing only the servers relevant to that context.

You can connect different AI applications to different profiles. When you connect a client, you specify which profile it should use. This means Claude Desktop and VS Code can have access to different server collections if needed.

Profiles can be shared with your team. Push a profile to your registry, and team members can pull it to get the exact same server collection and configuration you use.

## [Creating and managing profiles](#creating-and-managing-profiles)

### [Create a profile](#create-a-profile)

1. In Docker Desktop, select **MCP Toolkit** and select the **Profiles** tab.
2. Select **Create profile**.
3. Enter a name for your profile (e.g., "web-dev").
4. Optionally, search and add servers to your profile now, or add them later.
5. Optionally, search and add clients to connect to your profile.
6. Select **Create**.

Your new profile appears in the profiles list.

### [View profile details](#view-profile-details)

Select a profile in the **Profiles** tab to view its details. The profile view has two tabs:

* **Overview**: Shows the servers in your profile, secrets configuration, and connected clients. Use the **+** buttons to add more servers or clients.
* **Tools**: Lists all available tools from your profile's servers. You can enable or disable individual tools.

### [Remove a profile](#remove-a-profile)

1. In the **Profiles** tab, find the profile you want to remove.
2. Select ⋮ next to the profile name, and then **Delete**.
3. Confirm the removal.

> Caution
>
> Removing a profile deletes all its server configurations and settings, and updates the client configuration (removes MCP Toolkit). This action can't be undone.

### [Default profile](#default-profile)

When you run the MCP Gateway or use MCP Toolkit without specifying a profile, Docker MCP uses a profile named `default`, or an empty configuration if a `default` profile does not exist.

If you're upgrading from a previous version of MCP Toolkit, your existing server configurations automatically migrate to the `default` profile. You don't need to manually recreate your setup - everything continues to work as before.

You can always specify a different profile using the `--profile` flag with the gateway command:

```console
$ docker mcp gateway run --profile web-dev
```

## [Adding servers to profiles](#adding-servers-to-profiles)

Profiles contain the MCP servers you select from the catalog. Add servers to organize your tools for specific workflows.

### [Add a server](#add-a-server)

You can add servers to a profile in two ways.

From the Catalog tab:

1. Select the **Catalog** tab.
2. Select the checkbox next to servers you want to add to see which profile to add them to.
3. Choose your profile from the drop-down.

From within a profile:

1. Select the **Profiles** tab and select your profile.
2. In the **Servers** section, select the **+** button.
3. Search for and select servers to add.

If a server requires OAuth authentication, you're prompted to authorize it. See [OAuth authentication](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#oauth-authentication) for details.

### [List servers in a profile](#list-servers-in-a-profile)

Select a profile in the **Profiles** tab to see all servers it contains.

### [Remove a server](#remove-a-server)

1. Select the **Profiles** tab and select your profile.
2. In the **Servers** section, find the server you want to remove.
3. Select the delete icon next to the server.

## [Configuring profiles](#configuring-profiles)

### [Server configuration](#server-configuration)

Some servers require configuration beyond authentication. Configure server settings within your profile.

1. Select the **Profiles** tab and select your profile.
2. In the **Servers** section, select the configure icon next to the server.
3. Adjust the server's configuration settings as needed.

### [OAuth credentials](#oauth-credentials)

OAuth credentials are shared across all profiles. When you authorize access to a service like GitHub or Notion, that authorization is available to any server in any profile that needs it.

This means all profiles use the same OAuth credentials for a given service. If you need to use different accounts for different projects, you'll need to revoke and re-authorize between switching profiles.

See [OAuth authentication](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/#oauth-authentication) for details on authorizing servers.

### [Configuration persistence](#configuration-persistence)

Profile configurations persist in your Docker installation. When you restart Docker Desktop or your system, your profiles, servers, and configurations remain intact.

## [Sharing profiles](#sharing-profiles)

Profiles can be shared with your team by pushing them to OCI-compliant registries as artifacts. This is useful for distributing standardized MCP setups across your organization. Credentials are not included in shared profiles for security reasons. Team members configure OAuth separately after pulling.

### [Push a profile](#push-a-profile)

1. Select the profile you want to share in the **Profiles** tab.
2. Select **Push to Registry**.
3. Enter the registry destination (e.g., `registry.example.com/profiles/web-dev:v1`).
4. Complete authentication if required.

### [Pull a profile](#pull-a-profile)

1. Select **Pull from Registry** in the **Profiles** tab.
2. Enter the registry reference (e.g., `registry.example.com/profiles/team-standard:latest`).
3. Complete authentication if required.

The profile is downloaded and added to your profiles list. Configure any required OAuth credentials separately.

### [Team collaboration workflow](#team-collaboration-workflow)

A typical workflow for sharing profiles across a team:

1. Create and configure a profile with the servers your team needs.
2. Test the profile to ensure it works as expected.
3. Push the profile to your team's registry with a version tag (e.g., `registry.example.com/profiles/team-dev:v1`).
4. Share the registry reference with your team.
5. Team members pull the profile and configure any required OAuth credentials.

This ensures everyone uses the same server collection and configuration, reducing setup time and inconsistencies.

## [Using profiles with clients](#using-profiles-with-clients)

When you connect an AI client to the MCP Gateway, you specify which profile's servers the client can access.

### [Run the gateway with a profile](#run-the-gateway-with-a-profile)

Connect clients to your profile through the **Clients** section in the MCP Toolkit. You can add clients when creating a profile or add them to existing profiles later.

### [Configure clients for specific profiles](#configure-clients-for-specific-profiles)

When setting up a client manually, you can specify which profile the client uses. This lets different clients connect to different profiles.

For example, your Claude Desktop configuration might use:

```json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run", "--profile", "claude-work"]
    }
  }
}
```

While your VS Code configuration uses a different profile:

```json
{
  "mcp": {
    "servers": {
      "MCP_DOCKER": {
        "command": "docker",
        "args": ["mcp", "gateway", "run", "--profile", "vscode-dev"],
        "type": "stdio"
      }
    }
  }
}
```

### [Switching between profiles](#switching-between-profiles)

To switch the profile your clients use, update the client configuration to specify a different `--profile` value in the gateway command arguments.

## [Further reading](#further-reading)

* [Get started with MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/get-started/)
* [Use MCP Toolkit from the CLI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/cli/)
* [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
* [MCP Toolkit](https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/)

----
url: https://docs.docker.com/reference/cli/docker/buildx/history/open/
----

# docker buildx history open

***

| Description | Open a build record in Docker Desktop        |
| ----------- | -------------------------------------------- |
| Usage       | `docker buildx history open [OPTIONS] [REF]` |

## [Description](#description)

Open a build record in Docker Desktop for visual inspection. This requires Docker Desktop to be installed and running on the host machine.

## [Examples](#examples)

### [Open the most recent build in Docker Desktop](#open-the-most-recent-build-in-docker-desktop)

```console
docker buildx history open
```

By default, this opens the most recent build on the current builder.

### [Open a specific build](#open-a-specific-build)

```console
# Using a build ID
docker buildx history open qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history open ^1
```

----
url: https://docs.docker.com/reference/cli/docker/container/ls/
----

# docker container ls

***

| Description                                                               | List containers                                           |
| ------------------------------------------------------------------------- | --------------------------------------------------------- |
| Usage                                                                     | `docker container ls [OPTIONS]`                           |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker container list` `docker container ps` `docker ps` |

## [Description](#description)

List containers

## [Options](#options)

| Option                    | Default | Description                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`-a, --all`](#all)       |         | Show all containers (default shows just running)                                                                                                                                                                                                                                                                                                                                       |
| [`-f, --filter`](#filter) |         | Filter output based on conditions provided                                                                                                                                                                                                                                                                                                                                             |
| [`--format`](#format)     |         | Format output using a custom template: 'table': Print output in table format with column headers (default) 'table TEMPLATE': Print output in table format using the given Go template 'json': Print in JSON format 'TEMPLATE': Print output using the given Go template. Refer to <https://docs.docker.com/go/formatting/> for more information about formatting output with templates |
| `-n, --last`              | `-1`    | Show n last created containers (includes all states)                                                                                                                                                                                                                                                                                                                                   |
| `-l, --latest`            |         | Show the latest created container (includes all states)                                                                                                                                                                                                                                                                                                                                |
| [`--no-trunc`](#no-trunc) |         | Don't truncate output                                                                                                                                                                                                                                                                                                                                                                  |
| `-q, --quiet`             |         | Only display container IDs                                                                                                                                                                                                                                                                                                                                                             |
| [`-s, --size`](#size)     |         | Display total file sizes                                                                                                                                                                                                                                                                                                                                                               |

## [Examples](#examples)

### [Do not truncate output (--no-trunc)](#no-trunc)

Running `docker ps --no-trunc` showing 2 linked containers.

```console
$ docker ps --no-trunc

CONTAINER ID                                                     IMAGE                        COMMAND                CREATED              STATUS              PORTS               NAMES
ca5534a51dd04bbcebe9b23ba05f389466cf0c190f1f8f182d7eea92a9671d00 ubuntu:24.04                 bash                   17 seconds ago       Up 16 seconds       3300-3310/tcp       webapp
9ca9747b233100676a48cc7806131586213fa5dab86dd1972d6a8732e3a84a4d crosbymichael/redis:latest   /redis-server --dir    33 minutes ago       Up 33 minutes       6379/tcp            redis,webapp/db
```

### [Show both running and stopped containers (-a, --all)](#all)

The `docker ps` command only shows running containers by default. To see all containers, use the `--all` (or `-a`) flag:

```console
$ docker ps -a
```

`docker ps` groups exposed ports into a single range if possible. E.g., a container that exposes TCP ports `100, 101, 102` displays `100-102/tcp` in the `PORTS` column.

### [Show disk usage by container (--size)](#size)

The `docker ps --size` (or `-s`) command displays two different on-disk-sizes for each container:

```console
$ docker ps --size

CONTAINER ID   IMAGE          COMMAND                  CREATED        STATUS       PORTS   NAMES        SIZE
e90b8831a4b8   nginx          "/bin/bash -c 'mkdir "   11 weeks ago   Up 4 hours           my_nginx     35.58 kB (virtual 109.2 MB)
00c6131c5e30   telegraf:1.5   "/entrypoint.sh"         11 weeks ago   Up 11 weeks          my_telegraf  0 B (virtual 209.5 MB)
```

* The "size" information shows the amount of data (on disk) that is used for the *writable* layer of each container
* The "virtual size" is the total amount of disk-space used for the read-only *image* data used by the container and the writable layer.

For more information, refer to the [container size on disk](/engine/storage/drivers/#container-size-on-disk) section.

### [Filtering (--filter)](#filter)

The `--filter` (or `-f`) flag format is a `key=value` pair. If there is more than one filter, then pass multiple flags (e.g. `--filter "foo=bar" --filter "bif=baz"`).

The currently supported filters are:

| Filter                | Description                                                                                                                         |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------- |
| `id`                  | Container's ID                                                                                                                      |
| `name`                | Container's name                                                                                                                    |
| `label`               | An arbitrary string representing either a key or a key-value pair. Expressed as `<key>` or `<key>=<value>`                          |
| `exited`              | An integer representing the container's exit code. Only useful with `--all`.                                                        |
| `status`              | One of `created`, `restarting`, `running`, `removing`, `paused`, `exited`, or `dead`                                                |
| `ancestor`            | Filters containers which share a given image as an ancestor. Expressed as `<image-name>[:<tag>]`, `<image id>`, or `<image@digest>` |
| `before` or `since`   | Filters containers created before or after a given container ID or name                                                             |
| `volume`              | Filters running containers which have mounted a given volume or bind mount.                                                         |
| `network`             | Filters running containers connected to a given network.                                                                            |
| `publish` or `expose` | Filters containers which publish or expose a given port. Expressed as `<port>[/<proto>]` or `<startport-endport>/[<proto>]`         |
| `health`              | Filters containers based on their healthcheck status. One of `starting`, `healthy`, `unhealthy` or `none`.                          |
| `isolation`           | Windows daemon only. One of `default`, `process`, or `hyperv`.                                                                      |
| `is-task`             | Filters containers that are a "task" for a service. Boolean option (`true` or `false`)                                              |

#### [label](#label)

The `label` filter matches containers based on the presence of a `label` alone or a `label` and a value.

The following filter matches containers with the `color` label regardless of its value.

```console
$ docker ps --filter "label=color"

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
673394ef1d4c        busybox             "top"               47 seconds ago      Up 45 seconds                           nostalgic_shockley
d85756f57265        busybox             "top"               52 seconds ago      Up 51 seconds                           high_albattani
```

The following filter matches containers with the `color` label with the `blue` value.

```console
$ docker ps --filter "label=color=blue"

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
d85756f57265        busybox             "top"               About a minute ago   Up About a minute                       high_albattani
```

#### [name](#name)

The `name` filter matches on all or part of a container's name.

The following filter matches all containers with a name containing the `nostalgic_stallman` string.

```console
$ docker ps --filter "name=nostalgic_stallman"

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9b6247364a03        busybox             "top"               2 minutes ago       Up 2 minutes                            nostalgic_stallman
```

You can filter for a substring in a name as this shows:

```console
$ docker ps --filter "name=nostalgic"

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
715ebfcee040        busybox             "top"               3 seconds ago       Up 1 second                             i_am_nostalgic
9b6247364a03        busybox             "top"               7 minutes ago       Up 7 minutes                            nostalgic_stallman
673394ef1d4c        busybox             "top"               38 minutes ago      Up 38 minutes                           nostalgic_shockley
```

#### [exited](#exited)

The `exited` filter matches containers by exist status code. For example, to filter for containers that have exited successfully:

```console
$ docker ps -a --filter 'exited=0'

CONTAINER ID        IMAGE             COMMAND                CREATED             STATUS                   PORTS                      NAMES
ea09c3c82f6e        registry:latest   /srv/run.sh            2 weeks ago         Exited (0) 2 weeks ago   127.0.0.1:5000->5000/tcp   desperate_leakey
106ea823fe4e        fedora:latest     /bin/sh -c 'bash -l'   2 weeks ago         Exited (0) 2 weeks ago                              determined_albattani
48ee228c9464        fedora:20         bash                   2 weeks ago         Exited (0) 2 weeks ago                              tender_torvalds
```

#### [Filter by exit signal](#filter-by-exit-signal)

You can use a filter to locate containers that exited with status of `137` meaning a `SIGKILL(9)` killed them.

```console
$ docker ps -a --filter 'exited=137'

CONTAINER ID        IMAGE               COMMAND                CREATED             STATUS                       PORTS               NAMES
b3e1c0ed5bfe        ubuntu:latest       "sleep 1000"           12 seconds ago      Exited (137) 5 seconds ago                       grave_kowalevski
a2eb5558d669        redis:latest        "/entrypoint.sh redi   2 hours ago         Exited (137) 2 hours ago                         sharp_lalande
```

Any of these events result in a `137` status:

* the `init` process of the container is killed manually
* `docker kill` kills the container
* Docker daemon restarts which kills all running containers

#### [status](#status)

The `status` filter matches containers by status. The possible values for the container status are:

| Status       | Description                                                                                                                                                                                     |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `created`    | A container that has never been started.                                                                                                                                                        |
| `running`    | A running container, started by either `docker start` or `docker run`.                                                                                                                          |
| `paused`     | A paused container. See `docker pause`.                                                                                                                                                         |
| `restarting` | A container which is starting due to the designated restart policy for that container.                                                                                                          |
| `exited`     | A container which is no longer running. For example, the process inside the container completed or the container was stopped using the `docker stop` command.                                   |
| `removing`   | A container which is in the process of being removed. See `docker rm`.                                                                                                                          |
| `dead`       | A "defunct" container; for example, a container that was only partially removed because resources were kept busy by an external process. `dead` containers cannot be (re)started, only removed. |

For example, to filter for `running` containers:

```console
$ docker ps --filter status=running

CONTAINER ID        IMAGE                  COMMAND             CREATED             STATUS              PORTS               NAMES
715ebfcee040        busybox                "top"               16 minutes ago      Up 16 minutes                           i_am_nostalgic
d5c976d3c462        busybox                "top"               23 minutes ago      Up 23 minutes                           top
9b6247364a03        busybox                "top"               24 minutes ago      Up 24 minutes                           nostalgic_stallman
```

To filter for `paused` containers:

```console
$ docker ps --filter status=paused

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                      PORTS               NAMES
673394ef1d4c        busybox             "top"               About an hour ago   Up About an hour (Paused)                       nostalgic_shockley
```

#### [ancestor](#ancestor)

The `ancestor` filter matches containers based on its image or a descendant of it. The filter supports the following image representation:

* `image`
* `image:tag`
* `image:tag@digest`
* `short-id`
* `full-id`

If you don't specify a `tag`, the `latest` tag is used. For example, to filter for containers that use the latest `ubuntu` image:

```console
$ docker ps --filter ancestor=ubuntu

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
919e1179bdb8        ubuntu-c1           "top"               About a minute ago   Up About a minute                       admiring_lovelace
5d1e4a540723        ubuntu-c2           "top"               About a minute ago   Up About a minute                       admiring_sammet
82a598284012        ubuntu              "top"               3 minutes ago        Up 3 minutes                            sleepy_bose
bab2a34ba363        ubuntu              "top"               3 minutes ago        Up 3 minutes                            focused_yonath
```

Match containers based on the `ubuntu-c1` image which, in this case, is a child of `ubuntu`:

```console
$ docker ps --filter ancestor=ubuntu-c1

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
919e1179bdb8        ubuntu-c1           "top"               About a minute ago   Up About a minute                       admiring_lovelace
```

Match containers based on the `ubuntu` version `24.04` image:

```console
$ docker ps --filter ancestor=ubuntu:24.04

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
82a598284012        ubuntu:24.04        "top"               3 minutes ago        Up 3 minutes                            sleepy_bose
```

The following matches containers based on the layer `d0e008c6cf02` or an image that have this layer in its layer stack.

```console
$ docker ps --filter ancestor=d0e008c6cf02

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS               NAMES
82a598284012        ubuntu:24.04        "top"               3 minutes ago        Up 3 minutes                            sleepy_bose
```

#### [Create time](#create-time)

##### [before](#before)

The `before` filter shows only containers created before the container with a given ID or name. For example, having these containers created:

```console
$ docker ps

CONTAINER ID        IMAGE       COMMAND       CREATED              STATUS              PORTS              NAMES
9c3527ed70ce        busybox     "top"         14 seconds ago       Up 15 seconds                          desperate_dubinsky
4aace5031105        busybox     "top"         48 seconds ago       Up 49 seconds                          focused_hamilton
6e63f6ff38b0        busybox     "top"         About a minute ago   Up About a minute                      distracted_fermat
```

Filtering with `before` would give:

```console
$ docker ps -f before=9c3527ed70ce

CONTAINER ID        IMAGE       COMMAND       CREATED              STATUS              PORTS              NAMES
4aace5031105        busybox     "top"         About a minute ago   Up About a minute                      focused_hamilton
6e63f6ff38b0        busybox     "top"         About a minute ago   Up About a minute                      distracted_fermat
```

##### [since](#since)

The `since` filter shows only containers created since the container with a given ID or name. For example, with the same containers as in `before` filter:

```console
$ docker ps -f since=6e63f6ff38b0

CONTAINER ID        IMAGE       COMMAND       CREATED             STATUS              PORTS               NAMES
9c3527ed70ce        busybox     "top"         10 minutes ago      Up 10 minutes                           desperate_dubinsky
4aace5031105        busybox     "top"         10 minutes ago      Up 10 minutes                           focused_hamilton
```

#### [volume](#volume)

The `volume` filter shows only containers that mount a specific volume or have a volume mounted in a specific path:

```console
$ docker ps --filter volume=remote-volume --format "table {{.ID}}\t{{.Mounts}}"

CONTAINER ID        MOUNTS
9c3527ed70ce        remote-volume

$ docker ps --filter volume=/data --format "table {{.ID}}\t{{.Mounts}}"

CONTAINER ID        MOUNTS
9c3527ed70ce        remote-volume
```

#### [network](#network)

The `network` filter shows only containers that are connected to a network with a given name or ID.

The following filter matches all containers that are connected to a network with a name containing `net1`.

```console
$ docker run -d --net=net1 --name=test1 ubuntu top
$ docker run -d --net=net2 --name=test2 ubuntu top

$ docker ps --filter network=net1

CONTAINER ID        IMAGE       COMMAND       CREATED             STATUS              PORTS               NAMES
9d4893ed80fe        ubuntu      "top"         10 minutes ago      Up 10 minutes                           test1
```

The network filter matches on both the network's name and ID. The following example shows all containers that are attached to the `net1` network, using the network ID as a filter:

```console
$ docker network inspect --format "{{.ID}}" net1

8c0b4110ae930dbe26b258de9bc34a03f98056ed6f27f991d32919bfe401d7c5

$ docker ps --filter network=8c0b4110ae930dbe26b258de9bc34a03f98056ed6f27f991d32919bfe401d7c5

CONTAINER ID        IMAGE       COMMAND       CREATED             STATUS              PORTS               NAMES
9d4893ed80fe        ubuntu      "top"         10 minutes ago      Up 10 minutes                           test1
```

#### [publish and expose](#publish-and-expose)

The `publish` and `expose` filters show only containers that have published or exposed port with a given port number, port range, and/or protocol. The default protocol is `tcp` when not specified.

The following filter matches all containers that have published port of 80:

```console
$ docker run -d --publish=80 busybox top
$ docker run -d --expose=8080 busybox top

$ docker ps -a

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS                   NAMES
9833437217a5        busybox             "top"               5 seconds ago       Up 4 seconds        8080/tcp                dreamy_mccarthy
fc7e477723b7        busybox             "top"               50 seconds ago      Up 50 seconds       0.0.0.0:32768->80/tcp   admiring_roentgen

$ docker ps --filter publish=80

CONTAINER ID        IMAGE               COMMAND             CREATED              STATUS              PORTS                   NAMES
fc7e477723b7        busybox             "top"               About a minute ago   Up About a minute   0.0.0.0:32768->80/tcp   admiring_roentgen
```

The following filter matches all containers that have exposed TCP port in the range of `8000-8080`:

```console
$ docker ps --filter expose=8000-8080/tcp

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
9833437217a5        busybox             "top"               21 seconds ago      Up 19 seconds       8080/tcp            dreamy_mccarthy
```

The following filter matches all containers that have exposed UDP port `80`:

```console
$ docker ps --filter publish=80/udp

CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

### [Format the output (--format)](#format)

The formatting option (`--format`) pretty-prints container output using a Go template.

Valid placeholders for the Go template are listed below:

| Placeholder     | Description                                                                                     |
| --------------- | ----------------------------------------------------------------------------------------------- |
| `.ID`           | Container ID                                                                                    |
| `.Image`        | Image ID                                                                                        |
| `.Command`      | Quoted command                                                                                  |
| `.CreatedAt`    | Time when the container was created.                                                            |
| `.RunningFor`   | Elapsed time since the container was started.                                                   |
| `.Ports`        | Exposed ports.                                                                                  |
| `.State`        | Container status (for example; "created", "running", "exited").                                 |
| `.Status`       | Container status with details about duration and health-status.                                 |
| `.HealthStatus` | Container health status ("starting", "healthy", "unhealthy"; empty when unavailable).           |
| `.Size`         | Container disk size.                                                                            |
| `.Names`        | Container names.                                                                                |
| `.Labels`       | All labels assigned to the container.                                                           |
| `.Label`        | Value of a specific label for this container. For example `'{{.Label "com.docker.swarm.cpu"}}'` |
| `.Mounts`       | Names of the volumes mounted in this container.                                                 |
| `.Networks`     | Names of the networks attached to this container.                                               |

When using the `--format` option, the `ps` command will either output the data exactly as the template declares or, when using the `table` directive, includes column headers as well.

The following example uses a template without headers and outputs the `ID` and `Command` entries separated by a colon (`:`) for all running containers:

```console
$ docker ps --format "{{.ID}}: {{.Command}}"

a87ecb4f327c: /bin/sh -c #(nop) MA
01946d9d34d8: /bin/sh -c #(nop) MA
c1d3b0166030: /bin/sh -c yum -y up
41d50ecd2f57: /bin/sh -c #(nop) MA
```

To list all running containers with their labels in a table format you can use:

```console
$ docker ps --format "table {{.ID}}\t{{.Labels}}"

CONTAINER ID        LABELS
a87ecb4f327c        com.docker.swarm.node=ubuntu,com.docker.swarm.storage=ssd
01946d9d34d8
c1d3b0166030        com.docker.swarm.node=debian,com.docker.swarm.cpu=6
41d50ecd2f57        com.docker.swarm.node=fedora,com.docker.swarm.cpu=3,com.docker.swarm.storage=ssd
```

To list all running containers in JSON format, use the `json` directive:

```console
$ docker ps --format json
{"Command":"\"/docker-entrypoint.…\"","CreatedAt":"2021-03-10 00:15:05 +0100 CET","ID":"a762a2b37a1d","Image":"nginx","Labels":"maintainer=NGINX Docker Maintainers \u003cdocker-maint@nginx.com\u003e","LocalVolumes":"0","Mounts":"","Names":"boring_keldysh","Networks":"bridge","Ports":"80/tcp","RunningFor":"4 seconds ago","Size":"0B","State":"running","Status":"Up 3 seconds"}
```

----
url: https://docs.docker.com/reference/cli/docker/sandbox/
----

# docker sandbox

***

| Description | Docker Sandbox   |
| ----------- | ---------------- |
| Usage       | `docker sandbox` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Local sandbox environments for AI agents, using Docker.

## [Options](#options)

| Option        | Default | Description          |
| ------------- | ------- | -------------------- |
| `-D, --debug` |         | Enable debug logging |

## [Subcommands](#subcommands)

| Command                                                                                   | Description                                           |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| [`docker sandbox create`](https://docs.docker.com/reference/cli/docker/sandbox/create/)   | Create a sandbox for an agent                         |
| [`docker sandbox exec`](https://docs.docker.com/reference/cli/docker/sandbox/exec/)       | Execute a command inside a sandbox                    |
| [`docker sandbox inspect`](https://docs.docker.com/reference/cli/docker/sandbox/inspect/) | Display detailed information on one or more sandboxes |
| [`docker sandbox ls`](https://docs.docker.com/reference/cli/docker/sandbox/ls/)           | List VMs                                              |
| [`docker sandbox network`](https://docs.docker.com/reference/cli/docker/sandbox/network/) | Manage sandbox networking                             |
| [`docker sandbox reset`](https://docs.docker.com/reference/cli/docker/sandbox/reset/)     | Reset all VM sandboxes and clean up state             |
| [`docker sandbox rm`](https://docs.docker.com/reference/cli/docker/sandbox/rm/)           | Remove one or more sandboxes                          |
| [`docker sandbox run`](https://docs.docker.com/reference/cli/docker/sandbox/run/)         | Run an agent in a sandbox                             |
| [`docker sandbox save`](https://docs.docker.com/reference/cli/docker/sandbox/save/)       | Save a snapshot of the sandbox as a template          |
| [`docker sandbox stop`](https://docs.docker.com/reference/cli/docker/sandbox/stop/)       | Stop one or more sandboxes without removing them      |
| [`docker sandbox version`](https://docs.docker.com/reference/cli/docker/sandbox/version/) | Show sandbox version information                      |

----
url: https://docs.docker.com/reference/cli/docker/trust/signer/add/
----

# docker trust signer add

***

| Description | Add a signer                                                      |
| ----------- | ----------------------------------------------------------------- |
| Usage       | `docker trust signer add OPTIONS NAME REPOSITORY [REPOSITORY...]` |

## [Description](#description)

`docker trust signer add` adds signers to signed repositories.

## [Options](#options)

| Option  | Default | Description                          |
| ------- | ------- | ------------------------------------ |
| `--key` |         | Path to the signer's public key file |

## [Examples](#examples)

### [Add a signer to a repository](#add-a-signer-to-a-repository)

To add a new signer, `alice`, to this repository:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo


List of signers and their keys:

SIGNER              KEYS
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 642692c14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

Add `alice` with `docker trust signer add`:

```console
$ docker trust signer add alice example/trust-demo --key alice.crt
  Adding signer "alice" to example/trust-demo...
  Enter passphrase for repository key with ID 642692c:
Successfully added signer: alice to example/trust-demo
```

`docker trust inspect --pretty` now lists `alice` as a valid signer:

```console
$ docker trust inspect --pretty example/trust-demo

No signatures for example/trust-demo


List of signers and their keys:

SIGNER              KEYS
alice               05e87edcaecb
bob                 5600f5ab76a2

Administrative keys for example/trust-demo:
Repository Key: 642692c14c9fc399da523a5f4e24fe306a0a6ee1cc79a10e4555b3c6ab02f71e
Root Key:       3cb2228f6561e58f46dbc4cda4fcaff9d5ef22e865a94636f82450d1d2234949
```

----
url: https://docs.docker.com/reference/api/extensions-sdk/
----

# Extensions API Reference

***

Table of contents

***

## [Dashboard interfaces](#dashboard-interfaces)

* [Host](https://docs.docker.com/reference/api/extensions-sdk/Host/)
* [NavigationIntents](https://docs.docker.com/reference/api/extensions-sdk/NavigationIntents/)
* [Toast](https://docs.docker.com/reference/api/extensions-sdk/Toast/)

## [Other interfaces](#other-interfaces)

* [ExecResultV0](https://docs.docker.com/reference/api/extensions-sdk/ExecResultV0/)
* [RequestConfigV0](https://docs.docker.com/reference/api/extensions-sdk/RequestConfigV0/)
* [BackendV0](https://docs.docker.com/reference/api/extensions-sdk/BackendV0/)
* [OpenDialogResult](https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/)
* [Dialog](https://docs.docker.com/reference/api/extensions-sdk/Dialog/)
* [Docker](https://docs.docker.com/reference/api/extensions-sdk/Docker/)
* [DockerCommand](https://docs.docker.com/reference/api/extensions-sdk/DockerCommand/)
* [ExecOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecOptions/)
* [SpawnOptions](https://docs.docker.com/reference/api/extensions-sdk/SpawnOptions/)
* [Exec](https://docs.docker.com/reference/api/extensions-sdk/Exec/)
* [ExecProcess](https://docs.docker.com/reference/api/extensions-sdk/ExecProcess/)
* [ExecStreamOptions](https://docs.docker.com/reference/api/extensions-sdk/ExecStreamOptions/)
* [ExecResult](https://docs.docker.com/reference/api/extensions-sdk/ExecResult/)
* [RawExecResult](https://docs.docker.com/reference/api/extensions-sdk/RawExecResult/)
* [Extension](https://docs.docker.com/reference/api/extensions-sdk/Extension/)
* [DesktopUI](https://docs.docker.com/reference/api/extensions-sdk/DesktopUI/)
* [ExtensionVM](https://docs.docker.com/reference/api/extensions-sdk/ExtensionVM/)
* [ExtensionHost](https://docs.docker.com/reference/api/extensions-sdk/ExtensionHost/)
* [ExtensionCli](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/)
* [HttpService](https://docs.docker.com/reference/api/extensions-sdk/HttpService/)
* [RequestConfig](https://docs.docker.com/reference/api/extensions-sdk/RequestConfig/)
* [ServiceError](https://docs.docker.com/reference/api/extensions-sdk/ServiceError/)
* [DockerDesktopClient](https://docs.docker.com/reference/api/extensions-sdk/DockerDesktopClient/)

----
url: https://docs.docker.com/guides/ruby/
----

# Ruby on Rails language-specific guide

***

This guide explains how to containerize Ruby on Rails applications using Docker.

**Time to complete** 20 minutes

The Ruby language-specific guide teaches you how to containerize a Ruby on Rails application using Docker. In this guide, you’ll learn how to:

* Containerize and run a Ruby on Rails application
* Configure a GitHub Actions workflow to build and push a Docker image to Docker Hub
* Set up a local environment to develop a Ruby on Rails application using containers
* Deploy your containerized Ruby on Rails application locally to Kubernetes to test and debug your deployment

Start by containerizing an existing Ruby on Rails application.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/ruby/containerize/)

   Learn how to containerize a Ruby on Rails application.

2. [GitHub Actions CI](https://docs.docker.com/guides/ruby/configure-github-actions/)

   Learn how to configure CI/CD using GitHub Actions for your Ruby on Rails application.

3. [Develop your app](https://docs.docker.com/guides/ruby/develop/)

   Learn how to develop your Ruby on Rails application locally.

4. [Test your deployment](https://docs.docker.com/guides/ruby/deploy/)

   Learn how to develop locally using Kubernetes

----
url: https://docs.docker.com/guides/docker-build-cloud/common-questions/
----

# Common challenges and questions

***

Table of contents

***

### [Is Docker Build Cloud a standalone product or a part of Docker Desktop?](#is-docker-build-cloud-a-standalone-product-or-a-part-of-docker-desktop)

Docker Build Cloud is a service that can be used both with Docker Desktop and standalone. It lets you build your container images faster, both locally and in CI, with builds running on cloud infrastructure. The service uses a remote build cache, ensuring fast builds anywhere and for all team members.

When used with Docker Desktop, the [Builds view](/desktop/use-desktop/builds/) works with Docker Build Cloud out-of-the-box. It shows information about your builds and those initiated by your team members using the same builder, enabling collaborative troubleshooting.

To use Docker Build Cloud without Docker Desktop, you must [download and install](/build-cloud/setup/#use-docker-build-cloud-without-docker-desktop) a version of Buildx with support for Docker Build Cloud (the `cloud` driver). If you plan on building with Docker Build Cloud using the `docker compose build` command, you also need a version of Docker Compose that supports Docker Build Cloud.

### [How does Docker Build Cloud work with Docker Compose?](#how-does-docker-build-cloud-work-with-docker-compose)

Docker Compose works out of the box with Docker Build Cloud. Install the Docker Build Cloud-compatible client (buildx) and it works with both commands.

### [How many minutes are included in Docker Build Cloud Team plans?](#how-many-minutes-are-included-in-docker-build-cloud-team-plans)

Pricing details for Docker Build Cloud can be found on the [pricing page](https://www.docker.com/pricing?ref=Docs\&refAction=DocsGuidesBuildCloudFaq).

### [I’m a Docker personal user. Can I try Docker Build Cloud?](#im-a-docker-personal-user-can-i-try-docker-build-cloud)

Docker subscribers (Pro, Team, Business) receive a set number of minutes each month, shared across the account, to use Build Cloud.

If you do not have a Docker subscription, you may sign up for a free Personal account and start a trial of Docker Build Cloud. Personal accounts are limited to a single user.

For teams to receive the shared cache benefit, they must either be on a Docker Team or Docker Business subscription.

### [Does Docker Build Cloud support CI platforms? Does it work with GitHub Actions?](#does-docker-build-cloud-support-ci-platforms-does-it-work-with-github-actions)

Yes, Docker Build Cloud can be used with various CI platforms including GitHub Actions, CircleCI, Jenkins, and others. It can speed up your build pipelines, which means less time spent waiting and context switching.

Docker Build Cloud can be used with GitHub Actions to automate your build, test, and deployment pipeline. Docker provides a set of official GitHub Actions that you can use in your workflows.

Using GitHub Actions with Docker Build Cloud is straightforward. With a one-line change in your GitHub Actions configuration, everything else stays the same. You don't need to create new pipelines. Learn more in the [CI documentation](/build-cloud/ci/) for Docker Build Cloud.

----
url: https://docs.docker.com/dhi/core-concepts/ssdlc/
----

# Secure Software Development Lifecycle

***

Table of contents

***

## [What is a Secure Software Development Lifecycle?](#what-is-a-secure-software-development-lifecycle)

A Secure Software Development Lifecycle (SSDLC) integrates security practices into every phase of software delivery, from design and development to deployment and monitoring. It’s not just about writing secure code, but about embedding security throughout the tools, environments, and workflows used to build and ship software.

SSDLC practices are often guided by compliance frameworks, organizational policies, and supply chain security standards such as SLSA (Supply-chain Levels for Software Artifacts) or NIST SSDF.

## [Why SSDLC matters](#why-ssdlc-matters)

Modern applications depend on fast, iterative development, but rapid delivery often introduces security risks if protections aren’t built in early. An SSDLC helps:

* Prevent vulnerabilities before they reach production
* Ensure compliance through traceable and auditable workflows
* Reduce operational risk by maintaining consistent security standards
* Enable secure automation in CI/CD pipelines and cloud-native environments

By making security a first-class citizen in each stage of software delivery, organizations can shift left and reduce both cost and complexity.

## [How Docker supports a secure SDLC](#how-docker-supports-a-secure-sdlc)

Docker provides tools and secure content that make SSDLC practices easier to adopt across the container lifecycle. With [Docker Hardened Images](https://docs.docker.com/dhi/) (DHIs), [Docker Debug](/reference/cli/docker/debug/), and [Docker Scout](https://docs.docker.com/scout/), teams can add security without losing velocity.

### [Plan and design](#plan-and-design)

During planning, teams define architectural constraints, compliance goals, and threat models. Docker Hardened Images help at this stage by providing:

* Secure-by-default base images for common languages and runtimes
* Verified metadata including SBOMs, provenance, and VEX documents
* Support for both glibc and musl across multiple Linux distributions

You can use DHI metadata and attestations to support design reviews, threat modeling, or architecture sign-offs.

### [Develop](#develop)

In development, security should be transparent and easy to apply. Docker Hardened Images support secure-by-default development:

* Dev variants include shells, package managers, and compilers for convenience
* Minimal runtime variants reduce attack surface in final images
* Multi-stage builds let you separate build-time tools from runtime environments

[Docker Debug](/reference/cli/docker/debug/) helps developers:

* Temporarily inject debugging tools into minimal containers
* Avoid modifying base images during troubleshooting
* Investigate issues securely, even in production-like environments

### [Build and test](#build-and-test)

Build pipelines are an ideal place to catch issues early. Docker Scout integrates with Docker Hub and the CLI to:

* Scan for known CVEs using multiple vulnerability databases
* Trace vulnerabilities to specific layers and dependencies
* Interpret signed VEX data to suppress known-irrelevant issues
* Export JSON scan reports for CI/CD workflows

Build pipelines that use Docker Hardened Images benefit from:

* Reproducible, signed images
* Minimal build surfaces to reduce exposure
* Built-in compliance with SLSA Build Level 3 standards

### [Release and deploy](#release-and-deploy)

Security automation is critical as you release software at scale. Docker supports this phase by enabling:

* Signature verification and provenance validation before deployment
* Policy enforcement gates using Docker Scout
* Safe, non-invasive container inspection using Docker Debug

DHIs ship with the metadata and signatures required to automate image verification during deployment.

### [Monitor and improve](#monitor-and-improve)

Security continues after release. With Docker tools, you can:

* Continuously monitor image vulnerabilities through Docker Hub
* Get CVE remediation guidance and patch visibility using Docker Scout
* Receive updated DHI images with rebuilt and re-signed secure layers
* Debug running workloads with Docker Debug without modifying the image

## [Summary](#summary)

Docker helps teams embed security throughout the SSDLC by combining secure content (DHIs) with developer-friendly tooling (Docker Scout and Docker Debug). These integrations promote secure practices without introducing friction, making it easier to adopt compliance and supply chain security across your software delivery lifecycle.

----
url: https://docs.docker.com/reference/api/extensions-sdk/ExtensionHost/
----

# Interface: ExtensionHost

***

Table of contents

***

**`Since`**

0.2.0

## [Properties](#properties)

### [cli](#cli)

• `Readonly` **cli**: [`ExtensionCli`](https://docs.docker.com/reference/api/extensions-sdk/ExtensionCli/)

Executes a command in the host.

For example, execute the shipped binary `kubectl -h` command in the host:

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"]);
```

***

Streams the output of the command executed in the backend container or in the host.

Provided the `kubectl` binary is shipped as part of your extension, you can spawn the `kubectl -h` command in the host:

```typescript
await ddClient.extension.host.cli.exec("kubectl", ["-h"], {
           stream: {
             onOutput(data): void {
                 // As we can receive both `stdout` and `stderr`, we wrap them in a JSON object
                 JSON.stringify(
                   {
                     stdout: data.stdout,
                     stderr: data.stderr,
                   },
                   null,
                   "  "
                 );
             },
             onError(error: any): void {
               console.error(error);
             },
             onClose(exitCode: number): void {
               console.log("onClose with exit code " + exitCode);
             },
           },
         });
```

----
url: https://docs.docker.com/reference/cli/docker/checkpoint/ls/
----

# docker checkpoint ls

***

| Description                                                               | List checkpoints for a container           |
| ------------------------------------------------------------------------- | ------------------------------------------ |
| Usage                                                                     | `docker checkpoint ls [OPTIONS] CONTAINER` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker checkpoint list`                   |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

List checkpoints for a container

## [Options](#options)

| Option             | Default | Description                               |
| ------------------ | ------- | ----------------------------------------- |
| `--checkpoint-dir` |         | Use a custom checkpoint storage directory |

----
url: https://docs.docker.com/guides/ruby/configure-github-actions/
----

# Automate your builds with GitHub Actions

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize a Ruby on Rails application](https://docs.docker.com/guides/ruby/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

If you didn't create a [GitHub repository](https://github.com/new) for your project yet, it is time to do it. After creating the repository, don't forget to [add a remote](https://docs.github.com/en/get-started/getting-started-with-git/managing-remote-repositories) and ensure you can commit and [push your code](https://docs.github.com/en/get-started/using-git/pushing-commits-to-a-remote-repository#about-git-push) to GitHub.

1. In your project's GitHub repository, open **Settings**, and go to **Secrets and variables** > **Actions**.

2. Under the **Variables** tab, create a new **Repository variable** named `DOCKER_USERNAME` and your Docker ID as a value.

3. Create a new [Personal Access Token (PAT)](https://docs.docker.com/security/access-tokens/#create-an-access-token) for Docker Hub. You can name this token `docker-tutorial`. Make sure access permissions include Read and Write.

4. Add the PAT as a **Repository secret** in your GitHub repository, with the name `DOCKERHUB_TOKEN`.

## [Overview](#overview)

GitHub Actions is a CI/CD (Continuous Integration and Continuous Deployment) automation tool built into GitHub. It allows you to define custom workflows for building, testing, and deploying your code when specific events occur (e.g., pushing code, creating a pull request, etc.). A workflow is a YAML-based automation script that defines a sequence of steps to be executed when triggered. Workflows are stored in the `.github/workflows/` directory of a repository.

In this section, you'll learn how to set up and use GitHub Actions to build your Docker image as well as push it to Docker Hub. You will complete the following steps:

1. Define the GitHub Actions workflow.
2. Run the workflow.

## [1. Define the GitHub Actions workflow](#1-define-the-github-actions-workflow)

You can create a GitHub Actions workflow by creating a YAML file in the `.github/workflows/` directory of your repository. To do this use your favorite text editor or the GitHub web interface. The following steps show you how to create a workflow file using the GitHub web interface.

If you prefer to use the GitHub web interface, follow these steps:

1. Go to your repository on GitHub and then select the **Actions** tab.

2. Select **set up a workflow yourself**.

   This takes you to a page for creating a new GitHub Actions workflow file in your repository. By default, the file is created under `.github/workflows/main.yml`, let's change it name to `build.yml`.

If you prefer to use your text editor, create a new file named `build.yml` in the `.github/workflows/` directory of your repository.

Add the following content to the file:

```yaml
name: Build and push Docker image

on:
  push:
    branches:
      - main

jobs:
  build_and_push:
    runs-on: ubuntu-latest
    steps:
      - name: Login to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ vars.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      - name: Build and push
        uses: docker/build-push-action@v7
        with:
          push: true
          tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
```

In this section, you learned how to set up a GitHub Actions workflow for your Ruby on Rails application.

Related information:

* [Introduction to GitHub Actions](https://docs.docker.com/guides/gha/)
* [Docker Build GitHub Actions](https://docs.docker.com/build/ci/github-actions/)
* [Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

## [Next steps](#next-steps)

In the next section, you'll learn how you can develop your application using containers.

[Use containers for Ruby on Rails development »](https://docs.docker.com/guides/ruby/develop/)

----
url: https://docs.docker.com/engine/deprecated/
----

# Deprecated Docker Engine features

***

Table of contents

***

This page provides an overview of features that are deprecated in Engine. Changes in packaging, and supported (Linux) distributions are not included. To learn about end of support for Linux distributions, refer to the [release notes](https://docs.docker.com/engine/release-notes/).

## [Feature deprecation policy](#feature-deprecation-policy)

As changes are made to Docker there may be times when existing features need to be removed or replaced with newer features. Before an existing feature is removed it is labeled as "deprecated" within the documentation and remains in Docker for at least one stable release unless specified explicitly otherwise. After that time it may be removed.

Users are expected to take note of the list of deprecated features each release and plan their migration away from those features, and (if applicable) towards the replacement features as soon as possible.

## [Deprecated engine features](#deprecated-engine-features)

The following table provides an overview of the current status of deprecated features:

* **Deprecated**: the feature is marked "deprecated" and should no longer be used.

  The feature may be removed, disabled, or change behavior in a future release. The *"Deprecated"* column contains the release in which the feature was marked deprecated, whereas the *"Remove"* column contains a tentative release in which the feature is to be removed. If no release is included in the *"Remove"* column, the release is yet to be decided on.

* **Removed**: the feature was removed, disabled, or hidden.

  Refer to the linked section for details. Some features are "soft" deprecated, which means that they remain functional for backward compatibility, and to allow users to migrate to alternatives. In such cases, a warning may be printed, and users should not rely on this feature.

| Status     | Feature                                                                                                                            | Deprecated | Remove |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------- | ---------- | ------ |
| Deprecated | [Support for cgroup v1](#support-for-cgroup-v1)                                                                                    | v29.0      | -      |
| Deprecated | [`--pause` option on `docker commit`](#--pause-option-on-docker-commit)                                                            | v29.0      | v30.0  |
| Deprecated | [Legacy links environment variables](#legacy-links-environment-variables)                                                          | v28.4      | v30.0  |
| Deprecated | [Special handling for quoted values for TLS flags](#special-handling-for-quoted-values-for-tls-flags)                              | v28.4      | v29.0  |
| Deprecated | [Empty/nil fields in image Config from inspect API](#emptynil-fields-in-image-config-from-inspect-api)                             | v28.3      | v29.0  |
| Deprecated | [Configuration for pushing non-distributable artifacts](#configuration-for-pushing-non-distributable-artifacts)                    | v28.0      | v29.0  |
| Deprecated | [`--time` option on `docker stop` and `docker restart`](#--time-option-on-docker-stop-and-docker-restart)                          | v28.0      | -      |
| Removed    | [Non-standard fields in image inspect](#non-standard-fields-in-image-inspect)                                                      | v27.0      | v28.2  |
| Removed    | [API CORS headers](#api-cors-headers)                                                                                              | v27.0      | v28.0  |
| Removed    | [Graphdriver plugins (experimental)](#graphdriver-plugins-experimental)                                                            | v27.0      | v28.0  |
| Deprecated | [Unauthenticated TCP connections](#unauthenticated-tcp-connections)                                                                | v26.0      | v28.0  |
| Removed    | [`Container` and `ContainerConfig` fields in Image inspect](#container-and-containerconfig-fields-in-image-inspect)                | v25.0      | v26.0  |
| Removed    | [Deprecate legacy API versions](#deprecate-legacy-api-versions)                                                                    | v25.0      | v26.0  |
| Removed    | [Container short ID in network Aliases field](#container-short-id-in-network-aliases-field)                                        | v25.0      | v26.0  |
| Removed    | [Mount `bind-nonrecursive` option](#mount-bind-nonrecursive-option)                                                                | v25.0      | v29.0  |
| Removed    | [IsAutomated field, and `is-automated` filter on `docker search`](#isautomated-field-and-is-automated-filter-on-docker-search)     | v25.0      | v28.2  |
| Removed    | [logentries logging driver](#logentries-logging-driver)                                                                            | v24.0      | v25.0  |
| Removed    | [OOM-score adjust for the daemon](#oom-score-adjust-for-the-daemon)                                                                | v24.0      | v25.0  |
| Removed    | [BuildKit build information](#buildkit-build-information)                                                                          | v23.0      | v24.0  |
| Deprecated | [Legacy builder for Linux images](#legacy-builder-for-linux-images)                                                                | v23.0      | -      |
| Deprecated | [Legacy builder fallback](#legacy-builder-fallback)                                                                                | v23.0      | -      |
| Removed    | [Btrfs storage driver on CentOS 7 and RHEL 7](#btrfs-storage-driver-on-centos-7-and-rhel-7)                                        | v20.10     | v23.0  |
| Removed    | [Support for encrypted TLS private keys](#support-for-encrypted-tls-private-keys)                                                  | v20.10     | v23.0  |
| Removed    | [Kubernetes stack and context support](#kubernetes-stack-and-context-support)                                                      | v20.10     | v23.0  |
| Removed    | [Pulling images from non-compliant image registries](#pulling-images-from-non-compliant-image-registries)                          | v20.10     | v28.2  |
| Removed    | [Linux containers on Windows (LCOW)](#linux-containers-on-windows-lcow-experimental)                                               | v20.10     | v23.0  |
| Deprecated | [BLKIO weight options with cgroups v1](#blkio-weight-options-with-cgroups-v1)                                                      | v20.10     | -      |
| Removed    | [Kernel memory limit](#kernel-memory-limit)                                                                                        | v20.10     | v23.0  |
| Removed    | [Classic Swarm and overlay networks using external key/value stores](#classic-swarm-and-overlay-networks-using-cluster-store)      | v20.10     | v23.0  |
| Removed    | [Support for the legacy `~/.dockercfg` configuration file for authentication](#support-for-legacy-dockercfg-configuration-files)   | v20.10     | v23.0  |
| Deprecated | [CLI plugins support](#cli-plugins-support)                                                                                        | v20.10     | -      |
| Deprecated | [Dockerfile legacy `ENV name value` syntax](#dockerfile-legacy-env-name-value-syntax)                                              | v20.10     | -      |
| Removed    | [`docker build --stream` flag (experimental)](#docker-build---stream-flag-experimental)                                            | v20.10     | v20.10 |
| Removed    | [`fluentd-async-connect` log opt](#fluentd-async-connect-log-opt)                                                                  | v20.10     | v28.0  |
| Removed    | [Configuration options for experimental CLI features](#configuration-options-for-experimental-cli-features)                        | v19.03     | v23.0  |
| Removed    | [Pushing and pulling with image manifest v2 schema 1](#pushing-and-pulling-with-image-manifest-v2-schema-1)                        | v19.03     | v28.2  |
| Removed    | [`docker engine` subcommands](#docker-engine-subcommands)                                                                          | v19.03     | v20.10 |
| Removed    | [Top-level `docker deploy` subcommand (experimental)](#top-level-docker-deploy-subcommand-experimental)                            | v19.03     | v20.10 |
| Removed    | [`docker stack deploy` using "dab" files (experimental)](#docker-stack-deploy-using-dab-files-experimental)                        | v19.03     | v20.10 |
| Removed    | [Support for the `overlay2.override_kernel_check` storage option](#support-for-the-overlay2override_kernel_check-storage-option)   | v19.03     | v24.0  |
| Removed    | [AuFS storage driver](#aufs-storage-driver)                                                                                        | v19.03     | v24.0  |
| Removed    | [Legacy "overlay" storage driver](#legacy-overlay-storage-driver)                                                                  | v18.09     | v24.0  |
| Removed    | [Device mapper storage driver](#device-mapper-storage-driver)                                                                      | v18.09     | v25.0  |
| Removed    | [Use of reserved namespaces in engine labels](#use-of-reserved-namespaces-in-engine-labels)                                        | v18.06     | v20.10 |
| Removed    | [`--disable-legacy-registry` override daemon option](#--disable-legacy-registry-override-daemon-option)                            | v17.12     | v19.03 |
| Removed    | [Interacting with V1 registries](#interacting-with-v1-registries)                                                                  | v17.06     | v17.12 |
| Removed    | [Asynchronous `service create` and `service update` as default](#asynchronous-service-create-and-service-update-as-default)        | v17.05     | v17.10 |
| Removed    | [`-g` and `--graph` flags on `dockerd`](#-g-and---graph-flags-on-dockerd)                                                          | v17.05     | v23.0  |
| Deprecated | [Top-level network properties in NetworkSettings](#top-level-network-properties-in-networksettings)                                | v1.13      | v17.12 |
| Removed    | [`filter` option for `/images/json` endpoint](#filter-option-for-imagesjson-endpoint)                                              | v1.13      | v20.10 |
| Removed    | [`repository:shortid` image references](#repositoryshortid-image-references)                                                       | v1.13      | v17.12 |
| Removed    | [`docker daemon` subcommand](#docker-daemon-subcommand)                                                                            | v1.13      | v17.12 |
| Removed    | [Duplicate keys with conflicting values in engine labels](#duplicate-keys-with-conflicting-values-in-engine-labels)                | v1.13      | v17.12 |
| Deprecated | [`MAINTAINER` in Dockerfile](#maintainer-in-dockerfile)                                                                            | v1.13      | -      |
| Deprecated | [API calls without a version](#api-calls-without-a-version)                                                                        | v1.13      | v17.12 |
| Removed    | [Backing filesystem without `d_type` support for overlay/overlay2](#backing-filesystem-without-d_type-support-for-overlayoverlay2) | v1.13      | v17.12 |
| Removed    | [`--automated` and `--stars` flags on `docker search`](#--automated-and---stars-flags-on-docker-search)                            | v1.12      | v20.10 |
| Deprecated | [`-h` shorthand for `--help`](#-h-shorthand-for---help)                                                                            | v1.12      | v17.09 |
| Removed    | [`-e` and `--email` flags on `docker login`](#-e-and---email-flags-on-docker-login)                                                | v1.11      | v17.06 |
| Deprecated | [Separator (`:`) of `--security-opt` flag on `docker run`](#separator--of---security-opt-flag-on-docker-run)                       | v1.11      | v17.06 |
| Deprecated | [Ambiguous event fields in API](#ambiguous-event-fields-in-api)                                                                    | v1.10      | -      |
| Removed    | [`-f` flag on `docker tag`](#-f-flag-on-docker-tag)                                                                                | v1.10      | v1.12  |
| Removed    | [HostConfig at API container start](#hostconfig-at-api-container-start)                                                            | v1.10      | v1.12  |
| Removed    | [`--before` and `--since` flags on `docker ps`](#--before-and---since-flags-on-docker-ps)                                          | v1.10      | v1.12  |
| Removed    | [Driver-specific log tags](#driver-specific-log-tags)                                                                              | v1.9       | v1.12  |
| Removed    | [Docker Content Trust `ENV` passphrase variables name change](#docker-content-trust-env-passphrase-variables-name-change)          | v1.9       | v1.12  |
| Removed    | [`/containers/(id or name)/copy` endpoint](#containersid-or-namecopy-endpoint)                                                     | v1.8       | v1.12  |
| Removed    | [LXC built-in exec driver](#lxc-built-in-exec-driver)                                                                              | v1.8       | v1.10  |
| Removed    | [Old Command Line Options](#old-command-line-options)                                                                              | v1.8       | v1.10  |
| Removed    | [`--api-enable-cors` flag on `dockerd`](#--api-enable-cors-flag-on-dockerd)                                                        | v1.6       | v17.09 |
| Removed    | [`--run` flag on `docker commit`](#--run-flag-on-docker-commit)                                                                    | v0.10      | v1.13  |
| Removed    | [Three arguments form in `docker import`](#three-arguments-form-in-docker-import)                                                  | v0.6.7     | v1.12  |

### [Support for cgroup v1](#support-for-cgroup-v1)

**Deprecated in release: v29.0**

Support for cgroup v1 is deprecated in the v29.0 release, however, it will continue to be supported until May 2029. The latest release in May 2029 may not necessarily support cgroup v1, but there will be at least one maintained branch with the support for cgroup v1.

The cgroup version currently in use can be checked by running the `docker info` command:

```console
$ docker info
<...>
Server:
 <...>
 Cgroup Version: 2
 <...>
```

### [`--pause` option on `docker commit`](#--pause-option-on-docker-commit)

**Deprecated in release: v29.0**

**Target for removal in release: v30.0**

The `--pause` option is enabled by default since Docker v1.1.0 to prevent committing containers in an inconsistent state, but can be disabled by setting the `--pause=false` option. In docker CLI v29.0 this flag is replaced by a `--no-pause` flag instead. The `--pause` option is still functional in the v29.0 release, printing a deprecation warning, but will be removed in docker CLI v30.

### [Legacy links environment variables](#legacy-links-environment-variables)

**Deprecated in release: v28.4**

**Disabled by default in release: v29.0**

**Target for removal in release: v30.0**

Containers attached to the default bridge network can specify "legacy links" (e.g. using `--links` on the CLI) to get access to other containers attached to that network. The linking container (i.e., the container created with `--links`) automatically gets environment variables that specify the IP address and port mappings of the linked container. However, these environment variables are prefixed with the linked container's names, making them impractical.

Starting with Docker v29.0, these environment variables are no longer set by default. Users who still depend on them can start Docker Engine with the environment variable `DOCKER_KEEP_DEPRECATED_LEGACY_LINKS_ENV_VARS=1` set.

Support for legacy links environment variables, as well as the `DOCKER_KEEP_DEPRECATED_LEGACY_LINKS_ENV_VARS` will be removed in Docker Engine v30.0.

### [Special handling for quoted values for TLS flags](#special-handling-for-quoted-values-for-tls-flags)

**Deprecated in release: v28.4**

**Target for removal in release: v29.0**

The `--tlscacert`, `--tlscert`, and `--tlskey` command-line flags had non-standard behavior for handling values contained in quotes (`"` or `'`). Normally, quotes are handled by the shell, for example, in the following example, the shell takes care of handling quotes before passing the values to the `docker` CLI:

```console
docker --some-option "some-value-in-quotes" ...
```

However, when passing values using an equal sign (`=`), this may not happen and values may be handled including quotes;

```console
docker --some-option="some-value-in-quotes" ...
```

This caused issues with "Docker Machine", which used this format as part of its `docker-machine config` output, and the CLI carried special, non-standard handling for these flags.

Docker Machine reached EOL, and this special handling made the processing of flag values inconsistent with other flags used, so this behavior is deprecated. Users depending on this behavior are recommended to specify the quoted values using a space between the flag and its value, as illustrated above.

### [Empty/nil fields in image Config from inspect API](#emptynil-fields-in-image-config-from-inspect-api)

**Deprecated in release: v28.3**

**Target for removal in release: v29.0**

The `Config` field returned by `docker image inspect` (and the `GET /images/{name}/json` API endpoint) currently includes certain fields even when they are empty or nil. Starting in Docker v29.0, the following fields will be omitted from the API response when they contain empty or default values:

* `Cmd`
* `Entrypoint`
* `Env`
* `Labels`
* `OnBuild`
* `User`
* `Volumes`
* `WorkingDir`

Applications consuming the image inspect API should be updated to handle the absence of these fields gracefully, treating missing fields as having their default/empty values.

For API version corresponding to Docker v29.0, these fields will be omitted when empty. They will continue to be included when using clients that request an older API version for backward compatibility.

### [Configuration for pushing non-distributable artifacts](#configuration-for-pushing-non-distributable-artifacts)

**Deprecated in release: v28.0**

**Target for removal in release: v29.0**

Non-distributable artifacts (also called foreign layers) were introduced in docker v1.12 to accommodate Windows images for which the EULA did not allow layers to be distributed through registries other than those hosted by Microsoft. The concept of foreign / non-distributable layers was adopted by the OCI distribution spec in [oci#233](https://github.com/opencontainers/image-spec/pull/233). These restrictions were relaxed later to allow distributing these images through non-public registries, for which a configuration was added in Docker v17.0.6.0.

In 2022, Microsoft updated the EULA and [removed these restrictions](https://techcommunity.microsoft.com/blog/containers/announcing-windows-container-base-image-redistribution-rights-change/3645201), followed by the OCI distribution specification deprecating foreign layers in [oci#965](https://github.com/opencontainers/image-spec/pull/965). In 2023, Microsoft [removed the use of foreign data layers](https://techcommunity.microsoft.com/blog/containers/announcing-removal-of-foreign-layers-from-windows-container-images/3846833) for their images, making this functionality obsolete.

Docker v28.0 deprecates the `--allow-nondistributable-artifacts` daemon flag and corresponding `allow-nondistributable-artifacts` field in `daemon.json`. Setting either option no longer takes an effect, but a deprecation warning log is added to raise awareness about the deprecation. This warning is planned to become an error in the Docker v29.0.

Users currently using these options are therefore recommended to remove this option from their configuration to prevent the daemon from starting when upgrading to Docker v29.0.

The `AllowNondistributableArtifactsCIDRs` and `AllowNondistributableArtifactsHostnames` fields in the `RegistryConfig` of the `GET /info` API response are also deprecated. For API version v1.48 and lower, the fields are still included in the response but always `null`. In API version v1.49 and higher, the field will be omitted entirely.

### [`--time` option on `docker stop` and `docker restart`](#--time-option-on-docker-stop-and-docker-restart)

**Deprecated in release: v28.0**

The `--time` option for the `docker stop`, `docker container stop`, `docker restart`, and `docker container restart` commands has been renamed to `--timeout` for consistency with other uses of timeout options. The `--time` option is now deprecated and hidden, but remains functional for backward compatibility. Users are encouraged to migrate to using the `--timeout` option instead.

### [Non-standard fields in image inspect](#non-standard-fields-in-image-inspect)

**Deprecated in release: v27.0**

**Removed in release: v28.2**

The `Config` field returned shown in `docker image inspect` (and as returned by the `GET /images/{name}/json` API endpoint) returns additional fields that are not part of the image's configuration and not part of the [Docker image specification](https://github.com/moby/docker-image-spec/blob/v1.3.1/specs-go/v1/image.go#L19-L32) and [OCI image specification](https://github.com/opencontainers/image-spec/blob/v1.1.0/specs-go/v1/config.go#L24-L62).

These fields are never set (and always return the default value for the type), but are not omitted in the response when left empty. As these fields were not intended to be part of the image configuration response, they are deprecated, and will be removed from the API in thee next release.

The following fields are not part of the underlying image's `Config` field, and removed in the API response for API v1.50 and newer, corresponding with v28.2. They continue to be included when using clients that use an older API version:

* `Hostname`
* `Domainname`
* `AttachStdin`
* `AttachStdout`
* `AttachStderr`
* `Tty`
* `OpenStdin`
* `StdinOnce`
* `Image`
* `NetworkDisabled` (omitted unless set on older API versions)
* `MacAddress` (omitted unless set on older API versions)
* `StopTimeout` (omitted unless set on older API versions)

### [Graphdriver plugins (experimental)](#graphdriver-plugins-experimental)

**Deprecated in**: v27.0\*\*.

**Disabled by default in release: v27.0**

**Target for removal in release: v28.0**

[Graphdriver plugins](https://github.com/docker/cli/blob/v26.1.4/docs/extend/plugins_graphdriver.md) were an experimental feature that allowed extending the Docker Engine with custom storage drivers for storing images and containers. This feature was not maintained since its inception.

Support for graphdriver plugins was disabled by default in v27.0, and removed in v28.0. Users of this feature are recommended to instead configure the Docker Engine to use the [containerd image store](https://docs.docker.com/storage/containerd/) and a custom [snapshotter](https://github.com/containerd/containerd/tree/v1.7.18/docs/snapshotters)

### [API CORS headers](#api-cors-headers)

**Deprecated in release: v27.0**

**Disabled by default in release: v27.0**

**Removed in release: v28.0**

The `api-cors-header` configuration option for the Docker daemon is insecure, and is therefore deprecated and scheduled for removal. Incorrectly setting this option could leave a window of opportunity for unauthenticated cross-origin requests to be accepted by the daemon.

In Docker Engine v27.0, this flag can still be set, but it has no effect unless the environment variable `DOCKERD_DEPRECATED_CORS_HEADER` is also set to a non-empty value.

This flag has been removed altogether in v28.0.

This is a breaking change for authorization plugins and other programs that depend on this option for accessing the Docker API from a browser. If you need to access the API through a browser, use a reverse proxy.

### [Unauthenticated TCP connections](#unauthenticated-tcp-connections)

**Deprecated in release: v26.0**

**Target for removal in release: v28.0**

Configuring the Docker daemon to listen on a TCP address will require mandatory TLS verification. This change aims to ensure secure communication by preventing unauthorized access to the Docker daemon over potentially insecure networks. This mandatory TLS requirement applies to all TCP addresses except `tcp://localhost`.

In version 27.0 and later, specifying `--tls=false` or `--tlsverify=false` CLI flags causes the daemon to fail to start if it's also configured to accept remote connections over TCP. This also applies to the equivalent configuration options in `daemon.json`.

To facilitate remote access to the Docker daemon over TCP, you'll need to implement TLS verification. This secures the connection by encrypting data in transit and providing a mechanism for mutual authentication.

For environments remote daemon access isn't required, we recommend binding the Docker daemon to a Unix socket. For daemons where remote access is required and where TLS encryption is not feasible, you may want to consider using SSH as an alternative solution.

For further information, assistance, and step-by-step instructions on configuring TLS (or SSH) for the Docker daemon, refer to [Protect the Docker daemon socket](https://docs.docker.com/engine/security/protect-access/).

### [`Container` and `ContainerConfig` fields in Image inspect](#container-and-containerconfig-fields-in-image-inspect)

**Deprecated in release: v25.0**

**Removed in release: v26.0**

The `Container` and `ContainerConfig` fields returned by `docker inspect` are mostly an implementation detail of the classic (non-BuildKit) image builder. These fields are not portable and are empty when using the BuildKit-based builder (enabled by default since v23.0). These fields are deprecated in v25.0 and are omitted starting from v26.0 ( API version v1.45 and up). If image configuration of an image is needed, you can obtain it from the `Config` field.

### [Deprecate legacy API versions](#deprecate-legacy-api-versions)

**Deprecated in release: v25.0**

**Target for removal in release: v26.0**

The Docker daemon provides a versioned API for backward compatibility with old clients. Docker clients can perform API-version negotiation to select the most recent API version supported by the daemon (downgrading to and older version of the API when necessary). API version negotiation was introduced in Docker v1.12.0 (API 1.24), and clients before that used a fixed API version.

Docker Engine versions through v25.0 provide support for all [API versions](https://docs.docker.com/engine/api/#api-version-matrix) included in stable releases for a given platform. For Docker daemons on Linux, the earliest supported API version is 1.12 (corresponding with Docker Engine v1.0.0), whereas for Docker daemons on Windows, the earliest supported API version is 1.24 (corresponding with Docker Engine v1.12.0).

Support for legacy API versions (providing old API versions on current versions of the Docker Engine) is primarily intended to provide compatibility with recent, but still supported versions of the client, which is a common scenario (the Docker daemon may be updated to the latest release, but not all clients may be up-to-date or vice versa). Support for API versions before that (API versions provided by EOL versions of the Docker Daemon) is provided on a "best effort" basis.

Use of old API versions is rare, and support for legacy API versions involves significant complexity (Docker 1.0.0 having been released 10 years ago). Because of this, we'll start deprecating support for legacy API versions.

Docker Engine v25.0 by default disables API version older than 1.24 (aligning the minimum supported API version between Linux and Windows daemons). When connecting with a client that uses an API version older than 1.24, the daemon returns an error. The following example configures the Docker CLI to use API version 1.23, which produces an error:

```console
DOCKER_API_VERSION=1.23 docker version
Error response from daemon: client version 1.23 is too old. Minimum supported API version is 1.24,
upgrade your client to a newer version
```

Support for API versions lower than `1.24` has been permanently removed in Docker Engine v26, and the minimum supported API version will be incrementally raised in releases following that.

### [Container short ID in network Aliases field](#container-short-id-in-network-aliases-field)

**Deprecated in release: v25.0**

**Removed in release: v26.0**

The `Aliases` field returned by `docker inspect` contains the container short ID once the container is started. This behavior is deprecated in v25.0 but kept until the next release, v26.0. Starting with that version, the `Aliases` field will only contain the aliases set through the `docker container create` and `docker run` flag `--network-alias`.

A new field `DNSNames` containing the container name (if one was specified), the hostname, the network aliases, as well as the container short ID, has been introduced in v25.0 and should be used instead of the `Aliases` field.

### [Mount `bind-nonrecursive` option](#mount-bind-nonrecursive-option)

**Deprecated in release: v25.0**

**Removed in release: v29.0**

The `bind-nonrecursive` option was replaced with the [`bind-recursive`](https://docs.docker.com/engine/storage/bind-mounts/#recursive-mounts) option (see [cli-4316](https://github.com/docker/cli/pull/4316), [cli-4671](https://github.com/docker/cli/pull/4671)). The option was still accepted, but printed a deprecation warning:

```console
bind-nonrecursive is deprecated, use bind-recursive=disabled instead
```

In the v29.0 release, this warning is removed, and returned as an error. Users should use the equivalent `bind-recursive=disabled` option instead.

### [IsAutomated field, and `is-automated` filter on `docker search`](#isautomated-field-and-is-automated-filter-on-docker-search)

**Deprecated in release: v25.0**

**Removed in release: v28.2**

The `is_automated` field has been deprecated by Docker Hub's search API. Consequently, the `IsAutomated` field in image search will always be set to `false` in future, and searching for "is-automated=true" will yield no results.

The `AUTOMATED` column has been removed from the default `docker search` and `docker image search` output in v25.0, and the corresponding `IsAutomated` templating has been removed in v28.2.

### [Logentries logging driver](#logentries-logging-driver)

**Deprecated in release: v24.0**

**Removed in release: v25.0**

The logentries service SaaS was shut down on November 15, 2022, rendering this logging driver non-functional. Users should no longer use this logging driver, and the driver has been removed in Docker 25.0. Existing containers using this logging-driver are migrated to use the "local" logging driver after upgrading.

### [OOM-score adjust for the daemon](#oom-score-adjust-for-the-daemon)

**Deprecated in release: v24.0**

**Removed in release: v25.0**

The `oom-score-adjust` option was added to prevent the daemon from being OOM-killed before other processes. This option was mostly added as a convenience, as running the daemon as a systemd unit was not yet common.

Having the daemon set its own limits is not best-practice, and something better handled by the process-manager starting the daemon.

Docker v20.10 and newer no longer adjust the daemon's OOM score by default, instead setting the OOM-score to the systemd unit (OOMScoreAdjust) that's shipped with the packages.

Users currently depending on this feature are recommended to adjust the daemon's OOM score using systemd or through other means, when starting the daemon.

### [BuildKit build information](#buildkit-build-information)

**Deprecated in release: v23.0**

**Removed in release: v24.0**

[Build information](https://github.com/moby/buildkit/blob/v0.11/docs/buildinfo.md) structures have been introduced in [BuildKit v0.10.0](https://github.com/moby/buildkit/releases/tag/v0.10.0) and are generated with build metadata that allows you to see all the sources (images, Git repositories) that were used by the build with their exact versions and also the configuration that was passed to the build. This information is also embedded into the image configuration if one is generated.

### [Legacy builder for Linux images](#legacy-builder-for-linux-images)

**Deprecated in release: v23.0**

Docker v23.0 now uses BuildKit by default to build Linux images, and uses the [Buildx](https://docs.docker.com/buildx/working-with-buildx/) CLI component for `docker build`. With this change, `docker build` now exposes all advanced features that BuildKit provides and which were previously only available through the `docker buildx` subcommands.

The Buildx component is installed automatically when installing the `docker` CLI using our `.deb` or `.rpm` packages, and statically linked binaries are provided both on `download.docker.com`, and through the [`docker/buildx-bin` image](https://hub.docker.com/r/docker/buildx-bin) on Docker Hub. Refer the [Buildx section](http://docs.docker.com/go/buildx/) for detailed instructions on installing the Buildx component.

This release marks the beginning of the deprecation cycle of the classic ("legacy") builder for Linux images. No active development will happen on the classic builder (except for bugfixes). BuildKit development started five Years ago, left the "experimental" phase since Docker 18.09, and is already the default builder for [Docker Desktop](https://docs.docker.com/desktop/previous-versions/3.x-mac/#docker-desktop-320). While we're comfortable that BuildKit is stable for general use, there may be some changes in behavior. If you encounter issues with BuildKit, we encourage you to report issues in the [BuildKit issue tracker on GitHub](https://github.com/moby/buildkit/){:target="*blank" rel="noopener" class="*"}

> Classic builder for building Windows images
>
> BuildKit does not (yet) provide support for building Windows images, and `docker build` continues to use the classic builder to build native Windows images on Windows daemons.

### [Legacy builder fallback](#legacy-builder-fallback)

**Deprecated in release: v23.0**

[Docker v23.0 now uses BuildKit by default to build Linux images](#legacy-builder-for-linux-images), which requires the Buildx component to build images with BuildKit. There may be situations where the Buildx component is not available, and BuildKit cannot be used.

To provide a smooth transition to BuildKit as the default builder, Docker v23.0 has an automatic fallback for some situations, or produces an error to assist users to resolve the problem.

In situations where the user did not explicitly opt-in to use BuildKit (i.e., `DOCKER_BUILDKIT=1` is not set), the CLI automatically falls back to the classic builder, but prints a deprecation warning:

```text
DEPRECATED: The legacy builder is deprecated and will be removed in a future release.
            Install the buildx component to build images with BuildKit:
            https://docs.docker.com/go/buildx/
```

This situation may occur if the `docker` CLI is installed using the static binaries, and the Buildx component is not installed or not installed correctly. This fallback will be removed in a future release, therefore we recommend to [install the Buildx component](https://docs.docker.com/go/buildx/) and use BuildKit for your builds, or opt-out of using BuildKit with `DOCKER_BUILDKIT=0`.

If you opted-in to use BuildKit (`DOCKER_BUILDKIT=1`), but the Buildx component is missing, an error is printed instead, and the `docker build` command fails:

```text
ERROR: BuildKit is enabled but the buildx component is missing or broken.
       Install the buildx component to build images with BuildKit:
       https://docs.docker.com/go/buildx/
```

We recommend to [install the Buildx component](https://docs.docker.com/go/buildx/) to continue using BuildKit for your builds, but alternatively, users can either unset the `DOCKER_BUILDKIT` environment variable to fall back to the legacy builder, or opt-out of using BuildKit with `DOCKER_BUILDKIT=0`.

Be aware that the [classic builder is deprecated](#legacy-builder-for-linux-images) so both the automatic fallback and opting-out of using BuildKit will no longer be possible in a future release.

### [Btrfs storage driver on CentOS 7 and RHEL 7](#btrfs-storage-driver-on-centos-7-and-rhel-7)

**Removed in release: v23.0**

The `btrfs` storage driver on CentOS and RHEL was provided as a technology preview by CentOS and RHEL, but has been deprecated since the [Red Hat Enterprise Linux 7.4 release](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/storage_administration_guide/ch-btrfs), and removed in CentOS 8 and RHEL 8. Users of the `btrfs` storage driver on CentOS are recommended to migrate to a different storage driver, such as `overlay2`, which is now the default storage driver. Docker 23.0 continues to provide the `btrfs` storage driver to allow users to migrate to an alternative driver. The next release of Docker will no longer provide this driver.

### [Support for encrypted TLS private keys](#support-for-encrypted-tls-private-keys)

**Deprecated in release: v20.10**

**Removed in release: v23.0**

Use of encrypted TLS private keys has been deprecated, and has been removed. Golang has deprecated support for legacy PEM encryption (as specified in [RFC 1423](https://datatracker.ietf.org/doc/html/rfc1423)), as it is insecure by design (see <https://go-review.googlesource.com/c/go/+/264159>).

This feature allowed using an encrypted private key with a supplied password, but did not provide additional security as the encryption is known to be broken, and the key is sitting next to the password in the filesystem. Users are recommended to decrypt the private key, and store it un-encrypted to continue using it.

### [Kubernetes stack and context support](#kubernetes-stack-and-context-support)

**Deprecated in release: v20.10**

**Removed in release: v23.0**

Following the deprecation of [Compose on Kubernetes](https://github.com/docker/compose-on-kubernetes), support for Kubernetes in the `stack` and `context` commands has been removed from the CLI, and options related to this functionality are now either ignored, or may produce an error.

The following command-line flags are removed from the `docker context` subcommands:

* `--default-stack-orchestrator` - swarm is now the only (and default) orchestrator for stacks.
* `--kubernetes` - the Kubernetes endpoint can no longer be stored in `docker context`.
* `--kubeconfig` - exporting a context as a kubeconfig file is no longer supported.

The output produced by the `docker context inspect` subcommand no longer contains information about `StackOrchestrator` and `Kubernetes` endpoints for new contexts.

The following command-line flags are removed from the `docker stack` subcommands:

* `--kubeconfig` - using a kubeconfig file as context is no longer supported.
* `--namespace` - configuring the Kubernetes namespace for stacks is no longer supported.
* `--orchestrator` - swarm is now the only (and default) orchestrator for stacks.

The `DOCKER_STACK_ORCHESTRATOR`, `DOCKER_ORCHESTRATOR`, and `KUBECONFIG` environment variables, as well as the `stackOrchestrator` option in the `~/.docker/config.json` CLI configuration file are no longer used, and ignored.

### [Pulling images from non-compliant image registries](#pulling-images-from-non-compliant-image-registries)

**Deprecated in release: v20.10**

**Removed in release: v28.2**

Docker Engine v20.10 and up includes optimizations to verify if images in the local image cache need updating before pulling, preventing the Docker Engine from making unnecessary API requests. These optimizations require the container image registry to conform to the [Open Container Initiative Distribution Specification](https://github.com/opencontainers/distribution-spec).

While most registries conform to the specification, we encountered some registries to be non-compliant, resulting in `docker pull` to fail.

As a temporary solution, Docker Engine v20.10 added a fallback mechanism to allow `docker pull` to be functional when using a non-compliant registry. A warning message is printed in this situation:

```
WARNING Failed to pull manifest by the resolved digest. This registry does not
        appear to conform to the distribution registry specification; falling back to
        pull by tag. This fallback is DEPRECATED, and will be removed in a future
        release.
```

The fallback was added to allow users to either migrate their images to a compliant registry, or for these registries to become compliant.

GitHub deprecated the legacy `docker.pkg.github.com` registry, and it was [sunset on Feb 24th, 2025](https://github.blog/changelog/2025-01-23-legacy-docker-registry-closing-down/) in favor of GitHub Container Registry (GHCR, ghcr.io), making this fallback no longer needed.

### [Linux containers on Windows (LCOW) (experimental)](#linux-containers-on-windows-lcow-experimental)

**Deprecated in release: v20.10**

**Removed in release: v23.0**

The experimental feature to run Linux containers on Windows (LCOW) was introduced as a technical preview in Docker 17.09. While many enhancements were made after its introduction, the feature never reached completeness, and development has now stopped in favor of running Docker natively on Linux in WSL2.

Developers who want to run Linux workloads on a Windows host are encouraged to use [Docker Desktop with WSL2](https://docs.docker.com/docker-for-windows/wsl/) instead.

### [BLKIO weight options with cgroups v1](#blkio-weight-options-with-cgroups-v1)

**Deprecated in release: v20.10**

Specifying blkio weight (`docker run --blkio-weight` and `docker run --blkio-weight-device`) is now marked as deprecated when using cgroups v1 because the corresponding features were [removed in Linux kernel v5.0 and up](https://github.com/torvalds/linux/commit/f382fb0bcef4c37dc049e9f6963e3baf204d815c). When using cgroups v2, the `--blkio-weight` options are implemented using [\`io.weight](https://github.com/torvalds/linux/blob/v5.0/Documentation/admin-guide/cgroup-v2.rst#io).

### [Kernel memory limit](#kernel-memory-limit)

**Deprecated in release: v20.10**

**Removed in release: v23.0**

Specifying kernel memory limit (`docker run --kernel-memory`) is no longer supported because the [Linux kernel deprecated `kmem.limit_in_bytes` in v5.4](https://github.com/torvalds/linux/commit/0158115f702b0ba208ab0b5adf44cae99b3ebcc7). The OCI runtime specification now marks this option as ["NOT RECOMMENDED"](https://github.com/opencontainers/runtime-spec/pull/1093), and OCI runtimes such as `runc` no longer support this option.

The Docker API no longer handles the kernel-memory fields, and Docker CLI v29.0 removes the `--kernel-memory` option.

### [Classic Swarm and overlay networks using cluster store](#classic-swarm-and-overlay-networks-using-cluster-store)

**Deprecated in release: v20.10**

**Removed in release: v23.0**

Standalone ("classic") Swarm has been deprecated, and with that the use of overlay networks using an external key/value store. The corresponding`--cluster-advertise`, `--cluster-store`, and `--cluster-store-opt` daemon options have been removed.

### [Support for legacy `~/.dockercfg` configuration files](#support-for-legacy-dockercfg-configuration-files)

**Deprecated in release: v20.10**

**Removed in release: v23.0**

The Docker CLI up until v1.7.0 used the `~/.dockercfg` file to store credentials after authenticating to a registry (`docker login`). Docker v1.7.0 replaced this file with a new CLI configuration file, located in `~/.docker/config.json`. When implementing the new configuration file, the old file (and file-format) was kept as a fall-back, to assist existing users with migrating to the new file.

Given that the old file format encourages insecure storage of credentials (credentials are stored unencrypted), and that no version of the CLI since Docker v1.7.0 has created this file, support for this file, and its format has been removed.

### [Configuration options for experimental CLI features](#configuration-options-for-experimental-cli-features)

**Deprecated in release: v19.03**

**Removed in release: v23.0**

The `DOCKER_CLI_EXPERIMENTAL` environment variable and the corresponding `experimental` field in the CLI configuration file are deprecated. Experimental features are enabled by default, and these configuration options are no longer functional.

Starting with v23.0, the Docker CLI no longer prints `Experimental` for the client in the output of `docker version`, and the field has been removed from the JSON format.

### [CLI plugins support](#cli-plugins-support)

**Deprecated in release: v20.10**

CLI Plugin API is now marked as deprecated.

### [Dockerfile legacy `ENV name value` syntax](#dockerfile-legacy-env-name-value-syntax)

**Deprecated in release: v20.10**

The Dockerfile `ENV` instruction allows values to be set using either `ENV name=value` or `ENV name value`. The latter (`ENV name value`) form can be ambiguous, for example, the following defines a single env-variable (`ONE`) with value `"TWO= THREE=world"`, but may have intended to be setting three env-vars:

```dockerfile
ENV ONE TWO= THREE=world
```

This format also does not allow setting multiple environment-variables in a single `ENV` line in the Dockerfile.

Use of the `ENV name value` syntax is discouraged, and may be removed in a future release. Users are encouraged to update their Dockerfiles to use the `ENV name=value` syntax, for example:

```dockerfile
ENV ONE="" TWO="" THREE="world"
```

### [`docker build --stream` flag (experimental)](#docker-build---stream-flag-experimental)

**Deprecated in release: v20.10**

**Removed in release: v20.10**

Docker v17.07 introduced an experimental `--stream` flag on `docker build` which allowed the build-context to be incrementally sent to the daemon, instead of unconditionally sending the whole build-context.

This functionality has been reimplemented as part of BuildKit, which uses streaming by default and the `--stream` option will be ignored when using the classic builder, printing a deprecation warning instead.

Users that want to use this feature are encouraged to enable BuildKit by setting the `DOCKER_BUILDKIT=1` environment variable or through the daemon or CLI configuration files.

### [`fluentd-async-connect` log opt](#fluentd-async-connect-log-opt)

**Deprecated in release: v20.10**

**Removed in release: v28.0**

The `--log-opt fluentd-async-connect` option for the fluentd logging driver is [deprecated in favor of `--log-opt fluentd-async`](https://github.com/moby/moby/pull/39086). A deprecation message is logged in the daemon logs if the old option is used:

```console
fluent#New: AsyncConnect is now deprecated, use Async instead
```

Users are encouraged to use the `fluentd-async` option going forward, as support for the old option has been removed.

### [Pushing and pulling with image manifest v2 schema 1](#pushing-and-pulling-with-image-manifest-v2-schema-1)

**Deprecated in release: v19.03**

**Disabled by default in release: v26.0**

**Removed in release: v28.2**

The image manifest [v2 schema 1](https://distribution.github.io/distribution/spec/deprecated-schema-v1/) and "Docker Image v1" formats were deprecated in favor of the [v2 schema 2](https://distribution.github.io/distribution/spec/manifest-v2-2/) and [OCI image spec](https://github.com/opencontainers/image-spec/tree/v1.1.0) formats.

These legacy formats should no longer be used, and users are recommended to update images to use current formats, or to upgrade to more current images. Starting with Docker v26.0, pulling these images is disabled by default, and support has been removed in v28.2. Attempting to pull a legacy image now produces an error:

```console
$ docker pull ubuntu:10.04
Error response from daemon:
Docker Image Format v1 and Docker Image manifest version 2, schema 1 support has been removed.
Suggest the author of docker.io/library/ubuntu:10.04 to upgrade the image to the OCI Format or Docker Image manifest v2, schema 2.
More information at https://docs.docker.com/go/deprecated-image-specs/
```

### [`docker engine` subcommands](#docker-engine-subcommands)

**Deprecated in release: v19.03**

**Removed in release: v20.10**

The `docker engine activate`, `docker engine check`, and `docker engine update` provided an alternative installation method to upgrade Docker Community engines to Docker Enterprise, using an image-based distribution of the Docker Engine.

This feature was only available on Linux, and only when executed on a local node. Given the limitations of this feature, and the feature not getting widely adopted, the `docker engine` subcommands will be removed, in favor of installation through standard package managers.

### [Top-level `docker deploy` subcommand (experimental)](#top-level-docker-deploy-subcommand-experimental)

**Deprecated in release: v19.03**

**Removed in release: v20.10**

The top-level `docker deploy` command (using the "Docker Application Bundle" (.dab) file format was introduced as an experimental feature in Docker 1.13 / 17.03, but superseded by support for Docker Compose files using the `docker stack deploy` subcommand.

### [`docker stack deploy` using "dab" files (experimental)](#docker-stack-deploy-using-dab-files-experimental)

**Deprecated in release: v19.03**

**Removed in release: v20.10**

With no development being done on this feature, and no active use of the file format, support for the DAB file format and the top-level `docker deploy` command (hidden by default in 19.03), will be removed, in favour of `docker stack deploy` using compose files.

### [Support for the `overlay2.override_kernel_check` storage option](#support-for-the-overlay2override_kernel_check-storage-option)

**Deprecated in release: v19.03**

**Removed in release: v24.0**

This daemon configuration option disabled the Linux kernel version check used to detect if the kernel supported OverlayFS with multiple lower dirs, which is required for the overlay2 storage driver. Starting with Docker v19.03.7, the detection was improved to no longer depend on the kernel *version*, so this option was no longer used.

### [AuFS storage driver](#aufs-storage-driver)

**Deprecated in release: v19.03**

**Removed in release: v24.0**

The `aufs` storage driver is deprecated in favor of `overlay2`, and has been removed in a Docker Engine v24.0. Users of the `aufs` storage driver must migrate to a different storage driver, such as `overlay2`, before upgrading to Docker Engine v24.0.

The `aufs` storage driver facilitated running Docker on distros that have no support for OverlayFS, such as Ubuntu 14.04 LTS, which originally shipped with a 3.14 kernel.

Now that Ubuntu 14.04 is no longer a supported distro for Docker, and `overlay2` is available to all supported distros (as they are either on kernel 4.x, or have support for multiple lowerdirs backported), there is no reason to continue maintenance of the `aufs` storage driver.

### [Legacy overlay storage driver](#legacy-overlay-storage-driver)

**Deprecated in release: v18.09**

**Removed in release: v24.0**

The `overlay` storage driver is deprecated in favor of the `overlay2` storage driver, which has all the benefits of `overlay`, without its limitations (excessive inode consumption). The legacy `overlay` storage driver has been removed in Docker Engine v24.0. Users of the `overlay` storage driver should migrate to the `overlay2` storage driver before upgrading to Docker Engine v24.0.

The legacy `overlay` storage driver allowed using overlayFS-backed filesystems on kernels older than v4.x. Now that all supported distributions are able to run `overlay2` (as they are either on kernel 4.x, or have support for multiple lowerdirs backported), there is no reason to keep maintaining the `overlay` storage driver.

### [Device mapper storage driver](#device-mapper-storage-driver)

**Deprecated in release: v18.09**

**Disabled by default in release: v23.0**

**Removed in release: v25.0**

The `devicemapper` storage driver is deprecated in favor of `overlay2`, and has been removed in Docker Engine v25.0. Users of the `devicemapper` storage driver must migrate to a different storage driver, such as `overlay2`, before upgrading to Docker Engine v25.0.

The `devicemapper` storage driver facilitates running Docker on older (3.x) kernels that have no support for other storage drivers (such as overlay2, or btrfs).

Now that support for `overlay2` is added to all supported distros (as they are either on kernel 4.x, or have support for multiple lowerdirs backported), there is no reason to continue maintenance of the `devicemapper` storage driver.

### [Use of reserved namespaces in engine labels](#use-of-reserved-namespaces-in-engine-labels)

**Deprecated in release: v18.06**

**Removed in release: v20.10**

The namespaces `com.docker.*`, `io.docker.*`, and `org.dockerproject.*` in engine labels were always documented to be reserved, but there was never any enforcement.

Usage of these namespaces will now cause a warning in the engine logs to discourage their use, and will error instead in v20.10 and above.

### [`--disable-legacy-registry` override daemon option](#--disable-legacy-registry-override-daemon-option)

**Disabled In Release: v17.12**

**Removed in release: v19.03**

The `--disable-legacy-registry` flag was disabled in Docker 17.12 and will print an error when used. For this error to be printed, the flag itself is still present, but hidden. The flag has been removed in Docker 19.03.

### [Interacting with V1 registries](#interacting-with-v1-registries)

**Disabled by default in release: v17.06**

**Removed in release: v17.12**

Version 1.8.3 added a flag (`--disable-legacy-registry=false`) which prevents the Docker daemon from `pull`, `push`, and `login` operations against v1 registries. Though enabled by default, this signals the intent to deprecate the v1 protocol.

Support for the v1 protocol to the public registry was removed in 1.13. Any mirror configurations using v1 should be updated to use a [v2 registry mirror](https://docs.docker.com/registry/recipes/mirror/).

Starting with Docker 17.12, support for V1 registries has been removed, and the `--disable-legacy-registry` flag can no longer be used, and `dockerd` will fail to start when set.

### [Asynchronous `service create` and `service update` as default](#asynchronous-service-create-and-service-update-as-default)

**Deprecated in release: v17.05**

**Disabled by default in release: [v17.10](https://github.com/docker/docker-ce/releases/tag/v17.10.0-ce)**

Docker 17.05 added an optional `--detach=false` option to make the `docker service create` and `docker service update` work synchronously. This option will be enabled by default in Docker 17.10, at which point the `--detach` flag can be used to use the previous (asynchronous) behavior.

The default for this option will also be changed accordingly for `docker service rollback` and `docker service scale` in Docker 17.10.

### [`-g` and `--graph` flags on `dockerd`](#-g-and---graph-flags-on-dockerd)

**Deprecated in release: v17.05**

**Removed in release: v23.0**

The `-g` or `--graph` flag for the `dockerd` or `docker daemon` command was used to indicate the directory in which to store persistent data and resource configuration and has been replaced with the more descriptive `--data-root` flag. These flags were deprecated and hidden in v17.05, and removed in v23.0.

### [Top-level network properties in NetworkSettings](#top-level-network-properties-in-networksettings)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Target for removal in release: v17.12**

When inspecting a container, `NetworkSettings` contains top-level information about the default ("bridge") network;

`EndpointID`, `Gateway`, `GlobalIPv6Address`, `GlobalIPv6PrefixLen`, `IPAddress`, `IPPrefixLen`, `IPv6Gateway`, and `MacAddress`.

These properties are deprecated in favor of per-network properties in `NetworkSettings.Networks`. These properties were already "deprecated" in Docker 1.9, but kept around for backward compatibility.

Refer to [#17538](https://github.com/docker/docker/pull/17538) for further information.

### [`filter` option for `/images/json` endpoint](#filter-option-for-imagesjson-endpoint)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Removed in release: v20.10**

The `filter` option to filter the list of image by reference (name or name:tag) is now implemented as a regular filter, named `reference`.

### [`repository:shortid` image references](#repositoryshortid-image-references)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Removed in release: v17.12**

The `repository:shortid` syntax for referencing images is very little used, collides with tag references, and can be confused with digest references.

Support for the `repository:shortid` notation to reference images was removed in Docker 17.12.

### [`docker daemon` subcommand](#docker-daemon-subcommand)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Removed in release: v17.12**

The daemon is moved to a separate binary (`dockerd`), and should be used instead.

### [Duplicate keys with conflicting values in engine labels](#duplicate-keys-with-conflicting-values-in-engine-labels)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Removed in release: v17.12**

When setting duplicate keys with conflicting values, an error will be produced, and the daemon will fail to start.

### [`MAINTAINER` in Dockerfile](#maintainer-in-dockerfile)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

`MAINTAINER` was an early very limited form of `LABEL` which should be used instead.

### [API calls without a version](#api-calls-without-a-version)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Target for removal in release: v17.12**

API versions should be supplied to all API calls to ensure compatibility with future Engine versions. Instead of just requesting, for example, the URL `/containers/json`, you must now request `/v1.25/containers/json`.

### [Backing filesystem without `d_type` support for overlay/overlay2](#backing-filesystem-without-d_type-support-for-overlayoverlay2)

**Deprecated in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

**Removed in release: v17.12**

The overlay and overlay2 storage driver does not work as expected if the backing filesystem does not support `d_type`. For example, XFS does not support `d_type` if it is formatted with the `ftype=0` option.

Support for these setups has been removed, and Docker v23.0 and up now fails to start when attempting to use the `overlay2` or `overlay` storage driver on a backing filesystem without `d_type` support.

Refer to [#27358](https://github.com/docker/docker/issues/27358) for details.

### [`--automated` and `--stars` flags on `docker search`](#--automated-and---stars-flags-on-docker-search)

**Deprecated in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

**Removed in release: v20.10**

The `docker search --automated` and `docker search --stars` options are deprecated. Use `docker search --filter=is-automated=<true|false>` and `docker search --filter=stars=...` instead.

### [`-h` shorthand for `--help`](#-h-shorthand-for---help)

**Deprecated in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

**Target for removal in release: v17.09**

The shorthand (`-h`) is less common than `--help` on Linux and cannot be used on all subcommands (due to it conflicting with, e.g. `-h` / `--hostname` on `docker create`). For this reason, the `-h` shorthand was not printed in the "usage" output of subcommands, nor documented, and is now marked "deprecated".

### [`-e` and `--email` flags on `docker login`](#-e-and---email-flags-on-docker-login)

**Deprecated in release: [v1.11.0](https://github.com/docker/docker/releases/tag/v1.11.0)**

**Removed in release: [v17.06](https://github.com/docker/docker-ce/releases/tag/v17.06.0-ce)**

The `docker login` no longer automatically registers an account with the target registry if the given username doesn't exist. Due to this change, the email flag is no longer required, and will be deprecated.

### [Separator (`:`) of `--security-opt` flag on `docker run`](#separator--of---security-opt-flag-on-docker-run)

**Deprecated in release: [v1.11.0](https://github.com/docker/docker/releases/tag/v1.11.0)**

**Target for removal in release: v17.06**

The flag `--security-opt` doesn't use the colon separator (`:`) anymore to divide keys and values, it uses the equal symbol (`=`) for consistency with other similar flags, like `--storage-opt`.

### [Ambiguous event fields in API](#ambiguous-event-fields-in-api)

**Deprecated in release: [v1.10.0](https://github.com/docker/docker/releases/tag/v1.10.0)**

The fields `ID`, `Status` and `From` in the events API have been deprecated in favor of a more rich structure. See the events API documentation for the new format.

### [`-f` flag on `docker tag`](#-f-flag-on-docker-tag)

**Deprecated in release: [v1.10.0](https://github.com/docker/docker/releases/tag/v1.10.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

To make tagging consistent across the various `docker` commands, the `-f` flag on the `docker tag` command is deprecated. It is no longer necessary to specify `-f` to move a tag from one image to another. Nor will `docker` generate an error if the `-f` flag is missing and the specified tag is already in use.

### [HostConfig at API container start](#hostconfig-at-api-container-start)

**Deprecated in release: [v1.10.0](https://github.com/docker/docker/releases/tag/v1.10.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

Passing an `HostConfig` to `POST /containers/{name}/start` is deprecated in favor of defining it at container creation (`POST /containers/create`).

### [`--before` and `--since` flags on `docker ps`](#--before-and---since-flags-on-docker-ps)

**Deprecated in release: [v1.10.0](https://github.com/docker/docker/releases/tag/v1.10.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

The `docker ps --before` and `docker ps --since` options are deprecated. Use `docker ps --filter=before=...` and `docker ps --filter=since=...` instead.

### [Driver-specific log tags](#driver-specific-log-tags)

**Deprecated in release: [v1.9.0](https://github.com/docker/docker/releases/tag/v1.9.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

Log tags are now generated in a standard way across different logging drivers. Because of which, the driver specific log tag options `syslog-tag`, `gelf-tag` and `fluentd-tag` have been deprecated in favor of the generic `tag` option.

```console
$ docker --log-driver=syslog --log-opt tag="{{.ImageName}}/{{.Name}}/{{.ID}}"
```

### [Docker Content Trust ENV passphrase variables name change](#docker-content-trust-env-passphrase-variables-name-change)

**Deprecated in release: [v1.9.0](https://github.com/docker/docker/releases/tag/v1.9.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

Since 1.9, Docker Content Trust Offline key has been renamed to Root key and the Tagging key has been renamed to Repository key. Due to this renaming, we're also changing the corresponding environment variables

* DOCKER\_CONTENT\_TRUST\_OFFLINE\_PASSPHRASE is now named DOCKER\_CONTENT\_TRUST\_ROOT\_PASSPHRASE
* DOCKER\_CONTENT\_TRUST\_TAGGING\_PASSPHRASE is now named DOCKER\_CONTENT\_TRUST\_REPOSITORY\_PASSPHRASE

### [`/containers/(id or name)/copy` endpoint](#containersid-or-namecopy-endpoint)

**Deprecated in release: [v1.8.0](https://github.com/docker/docker/releases/tag/v1.8.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

The endpoint `/containers/(id or name)/copy` is deprecated in favor of `/containers/(id or name)/archive`.

### [LXC built-in exec driver](#lxc-built-in-exec-driver)

**Deprecated in release: [v1.8.0](https://github.com/docker/docker/releases/tag/v1.8.0)**

**Removed in release: [v1.10.0](https://github.com/docker/docker/releases/tag/v1.10.0)**

The built-in LXC execution driver, the lxc-conf flag, and API fields have been removed.

### [Old Command Line Options](#old-command-line-options)

**Deprecated in release: [v1.8.0](https://github.com/docker/docker/releases/tag/v1.8.0)**

**Removed in release: [v1.10.0](https://github.com/docker/docker/releases/tag/v1.10.0)**

The flags `-d` and `--daemon` are deprecated. Use the separate `dockerd` binary instead.

The following single-dash (`-opt`) variant of certain command line options are deprecated and replaced with double-dash options (`--opt`):

* `docker attach -nostdin`
* `docker attach -sig-proxy`
* `docker build -no-cache`
* `docker build -rm`
* `docker commit -author`
* `docker commit -run`
* `docker events -since`
* `docker history -notrunc`
* `docker images -notrunc`
* `docker inspect -format`
* `docker ps -beforeId`
* `docker ps -notrunc`
* `docker ps -sinceId`
* `docker rm -link`
* `docker run -cidfile`
* `docker run -dns`
* `docker run -entrypoint`
* `docker run -expose`
* `docker run -link`
* `docker run -lxc-conf`
* `docker run -n`
* `docker run -privileged`
* `docker run -volumes-from`
* `docker search -notrunc`
* `docker search -stars`
* `docker search -t`
* `docker search -trusted`
* `docker tag -force`

The following double-dash options are deprecated and have no replacement:

* `docker run --cpuset`
* `docker run --networking`
* `docker ps --since-id`
* `docker ps --before-id`
* `docker search --trusted`

**Deprecated in release: [v1.5.0](https://github.com/docker/docker/releases/tag/v1.5.0)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

The single-dash (`-help`) was removed, in favor of the double-dash `--help`

### [`--api-enable-cors` flag on `dockerd`](#--api-enable-cors-flag-on-dockerd)

**Deprecated in release: [v1.6.0](https://github.com/docker/docker/releases/tag/v1.6.0)**

**Removed in release: [v17.09](https://github.com/docker/docker-ce/releases/tag/v17.09.0-ce)**

The flag `--api-enable-cors` is deprecated since v1.6.0. Use the flag `--api-cors-header` instead.

### [`--run` flag on `docker commit`](#--run-flag-on-docker-commit)

**Deprecated in release: [v0.10.0](https://github.com/docker/docker/releases/tag/v0.10.0)**

**Removed in release: [v1.13.0](https://github.com/docker/docker/releases/tag/v1.13.0)**

The flag `--run` of the `docker commit` command (and its short version `-run`) were deprecated in favor of the `--changes` flag that allows to pass `Dockerfile` commands.

### [Three arguments form in `docker import`](#three-arguments-form-in-docker-import)

**Deprecated in release: [v0.6.7](https://github.com/docker/docker/releases/tag/v0.6.7)**

**Removed in release: [v1.12.0](https://github.com/docker/docker/releases/tag/v1.12.0)**

The `docker import` command format `file|URL|- [REPOSITORY [TAG]]` is deprecated since November 2013. It's no longer supported.

----
url: https://docs.docker.com/docker-hub/repos/manage/export/
----

# Export organization repositories to CSV

***

Table of contents

***

This guide shows you how to export a complete list of repositories from your Docker Hub organization, including private repositories. You'll use a Personal Access Token (PAT) from an administrator account to authenticate with the Docker Hub API and export repository details to a CSV file for reporting or analysis.

The exported data includes repository name, visibility status, last updated date, pull count, and star count.

## [Prerequisites](#prerequisites)

Before you begin, ensure you have:

* Administrator access to a Docker Hub organization
* `curl` installed for making API requests
* `jq` installed for JSON parsing
* A spreadsheet application to view the CSV

## [Create a personal access token](#create-a-personal-access-token)

[Create a personal access token](/security/access-tokens/) from a user account that has access to the organization's repositories. When creating the token, select at minimum **Read-only** access permissions to list repositories.

> Important
>
> Use a PAT from a user account that is a member of the organization. Users with owner roles can export all organization repositories. Members can only export repositories they have permission to access.

## [Authenticate with the Docker Hub API](#authenticate-with-the-docker-hub-api)

Exchange your personal access token for a JWT bearer token that you'll use for subsequent API requests.

1. Set your Docker Hub username, organization name, and personal access token as variables:

   ```bash
   USERNAME="<your-docker-username>"
   ORG="<org-name>"
   PAT="<your_personal_access_token>"
   ```

2. Call the authentication endpoint to get a JWT:

   ```bash
   TOKEN=$(
     curl -s https://hub.docker.com/v2/auth/token \
       -H 'Content-Type: application/json' \
       -d "{\"identifier\":\"$USERNAME\",\"secret\":\"$PAT\"}" \
     | jq -r '.access_token'
   )
   ```

3. Verify the token was retrieved successfully:

   ```console
   $ echo "Got JWT: ${#TOKEN} chars"
   ```

You'll use this JWT as a Bearer token in the `Authorization` header for all subsequent API calls.

## [Retrieve all repositories](#retrieve-all-repositories)

The Docker Hub API paginates repository lists. This script retrieves all pages and combines the results.

1. Set the page size and initial API endpoint:

   ```bash
   PAGE_SIZE=100
   URL="https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=$PAGE_SIZE"
   ```

2. Paginate through all results:

   ```bash
   ALL=$(
     while [ -n "$URL" ] && [ "$URL" != "null" ]; do
       RESP=$(curl -s "$URL" -H "Authorization: Bearer $TOKEN")
       echo "$RESP" | jq -c '.results[]'
       URL=$(echo "$RESP" | jq -r '.next')
     done | jq -s '.'
   )
   ```

3. Verify the number of repositories retrieved:

   ```console
   $ echo "$ALL" | jq 'length'
   ```

The script continues requesting the `next` URL from each response until pagination is complete.

## [Export to CSV](#export-to-csv)

Generate a CSV file with repository details that you can open in spreadsheet applications.

Run the following command to create `repos.csv`:

```bash
echo "$ALL" | jq -r '
  (["namespace","name","is_private","last_updated","pull_count","star_count"] | @csv),
  (.[] | [
    .namespace, .name, .is_private, .last_updated, (.pull_count//0), (.star_count//0)
  ] | @csv)
' > repos.csv
```

Verify the export completed:

```console
$ echo "Rows:" $(wc -l < repos.csv)
```

Open the `repos.csv` file in your preferred spreadsheet application to view and analyze your repository data.

## [Troubleshooting](#troubleshooting)

### [Only public repositories appear](#only-public-repositories-appear)

The Docker Hub account associated with your personal access token may not have access to private repositories in the organization.

To fix this:

1. Verify the account is a member of the organization
2. Check that the account has appropriate permissions (owner or member role)
3. Ensure the personal access token has sufficient access permissions
4. Regenerate the JWT and retry the export

### [API returns 403 or missing fields](#api-returns-403-or-missing-fields)

Ensure you're using the JWT from the `/v2/auth/token` endpoint as a Bearer token in the `Authorization` header, not the personal access token directly.

Verify your authentication:

```console
$ curl -s "https://hub.docker.com/v2/namespaces/$ORG/repositories?page_size=1" \
  -H "Authorization: Bearer $TOKEN" | jq
```

If this returns an error, re-run the authentication step to get a fresh JWT.

----
url: https://docs.docker.com/scout/integrations/team-collaboration/slack/
----

# Integrate Docker Scout with Slack

***

Table of contents

***

You can integrate Docker Scout with Slack by creating a Slack webhook and adding it to the Docker Scout Dashboard. Docker Scout will notify you about when a new vulnerability is disclosed, and it affects one or more of your images.

Example Slack notification from Docker Scout

## [How it works](#how-it-works)

After configuring the integration, Docker Scout sends notifications about changes to policy compliance and vulnerability exposure for your repositories, to the Slack channels associated with the webhook.

> Note
>
> Notifications are only triggered for the *last pushed* image tags for each repository. "Last pushed" refers to the image tag that was most recently pushed to the registry and analyzed by Docker Scout. If the last pushed image is not affected by a newly disclosed CVE, then no notification will be triggered.

For more information about Docker Scout notifications, see [Notification settings](https://docs.docker.com/scout/explore/dashboard/#notification-settings)

## [Setup](#setup)

To add a Slack integration:

1. Create a webhook, see [Slack documentation](https://api.slack.com/messaging/webhooks).

2. Go to the [Slack integration page](https://scout.docker.com/settings/integrations/slack/) in the Docker Scout Dashboard.

3. In the **How to integrate** section, enter a **Configuration name**. Docker Scout uses this label as a display name for the integration, so you might want to change the default name into something more meaningful. For example the `#channel-name`, or the name of the team that this configuration belongs to.

4. Paste the webhook you just created in the **Slack webhook** field.

   Select the **Test webhook** button if you wish to verify the connection. Docker Scout will send a test message to the specified webhook.

5. Select whether you want to enable notifications for all your Scout-enabled image repositories, or enter the names of the repositories that you want to send notifications for.

6. When you're ready to enable the integration, select **Create**.

After creating the webhook, Docker Scout begins to send notifications updates to the Slack channels associated with the webhook.

## [Remove a Slack integration](#remove-a-slack-integration)

To remove a Slack integration:

1. Go to the [Slack integration page](https://scout.docker.com/settings/integrations/slack/) in the Docker Scout Dashboard.
2. Select the **Remove** icon for the integration that you want to remove.
3. Confirm by selecting **Remove** again in the confirmation dialog.

----
url: https://docs.docker.com/engine/install/rhel/
----

# Install Docker Engine on RHEL

***

Table of contents

***

To get started with Docker Engine on RHEL, make sure you [meet the prerequisites](#prerequisites), and then follow the [installation steps](#installation-methods).

## [Prerequisites](#prerequisites)

### [OS requirements](#os-requirements)

To install Docker Engine, you need a maintained version of one of the following RHEL versions:

* RHEL 8
* RHEL 9
* RHEL 10

### [Uninstall old versions](#uninstall-old-versions)

Before you can install Docker Engine, you need to uninstall any conflicting packages.

Your Linux distribution may provide unofficial Docker packages, which may conflict with the official packages provided by Docker. You must uninstall these packages before you install the official version of Docker Engine.

```console
$ sudo dnf remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine \
                  podman \
                  runc
```

```console
$ sudo dnf -y install dnf-plugins-core
$ sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
```

#### [Install Docker Engine](#install-docker-engine)

1. Install the Docker packages.

   To install the latest version, run:

   ```console
   $ sudo dnf install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   If prompted to accept the GPG key, verify that the fingerprint matches `060A 61C5 1B55 8A7F 742B 77AA C52F EB6B 621E 9F35`, and if so, accept it.

   This command installs Docker, but it doesn't start Docker. It also creates a `docker` group, however, it doesn't add any users to the group by default.

   To install a specific version, start by listing the available versions in the repository:

   ```console
   $ dnf list docker-ce --showduplicates | sort -r

   docker-ce.x86_64    3:29.5.3-1.el9    docker-ce-stable
   docker-ce.x86_64    3:29.5.2-1.el9    docker-ce-stable
   <...>
   ```

   The list returned depends on which repositories are enabled, and is specific to your version of RHEL (indicated by the `.el9` suffix in this example).

   Install a specific version by its fully qualified package name, which is the package name (`docker-ce`) plus the version string (2nd column), separated by a hyphen (`-`). For example, `docker-ce-3:29.5.3-1.el9`.

   Replace `<VERSION_STRING>` with the desired version and then run the following command to install:

   ```console
   $ sudo dnf install docker-ce-VERSION_STRING docker-ce-cli-VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   This command installs Docker, but it doesn't start Docker. It also creates a `docker` group, however, it doesn't add any users to the group by default.

2. Start Docker Engine.

   ```console
   $ sudo systemctl enable --now docker
   ```

   This configures the Docker systemd service to start automatically when you boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.

3. Verify that the installation is successful by running the `hello-world` image:

   ```console
   $ sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
> The `docker` user group exists but contains no users, which is why you’re required to use `sudo` to run Docker commands. Continue to [Linux postinstall](/engine/install/linux-postinstall) to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### [Upgrade Docker Engine](#upgrade-docker-engine)

To upgrade Docker Engine, follow the [installation instructions](#install-using-the-repository), choosing the new version you want to install.

### [Install from a package](#install-from-a-package)

If you can't use Docker's `rpm` repository to install Docker Engine, you can download the `.rpm` file for your release and install it manually. You need to download a new file each time you want to upgrade Docker Engine.

1. Go to <https://download.docker.com/linux/rhel/>.

2. Select your RHEL version in the list.

3. Select the applicable architecture (`x86_64`, `aarch64`, or `s390x`), and then go to `stable/Packages/`.

4. Download the following `rpm` files for the Docker Engine, CLI, containerd, and Docker Compose packages:

   * `containerd.io-<version>.<arch>.rpm`
   * `docker-ce-<version>.<arch>.rpm`
   * `docker-ce-cli-<version>.<arch>.rpm`
   * `docker-buildx-plugin-<version>.<arch>.rpm`
   * `docker-compose-plugin-<version>.<arch>.rpm`

5. Install Docker Engine, changing the following path to the path where you downloaded the packages.

   ```console
   $ sudo dnf install ./containerd.io-<version>.<arch>.rpm \
     ./docker-ce-<version>.<arch>.rpm \
     ./docker-ce-cli-<version>.<arch>.rpm \
     ./docker-buildx-plugin-<version>.<arch>.rpm \
     ./docker-compose-plugin-<version>.<arch>.rpm
   ```

   Docker is installed but not started. The `docker` group is created, but no users are added to the group.

6. Start Docker Engine.

   ```console
   $ sudo systemctl enable --now docker
   ```

   This configures the Docker systemd service to start automatically when you boot your system. If you don't want Docker to start automatically, use `sudo systemctl start docker` instead.

7. Verify that the installation is successful by running the `hello-world` image:

   ```console
   $ sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
> The `docker` user group exists but contains no users, which is why you’re required to use `sudo` to run Docker commands. Continue to [Linux postinstall](/engine/install/linux-postinstall) to allow non-privileged users to run Docker commands and for other optional configuration steps.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the script will run when invoked:
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from <https://get.docker.com/> and runs it to install the latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker` service starts automatically on Debian based distributions. On `RPM` based distributions, such as CentOS, Fedora or RHEL, you need to start it manually using the appropriate `systemctl` or `service` command. As the message indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
> The installation script requires `root` or `sudo` privileges to install and use Docker. If you want to grant non-root users access to Docker, refer to the [post-installation steps for Linux](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user). You can also install Docker without `root` privileges, or configured to run in rootless mode. For instructions on running Docker in rootless mode, refer to [run the Docker daemon as a non-root user (rootless mode)](/engine/security/rootless/).

#### [Install pre-releases](#install-pre-releases)

Docker also provides a convenience script at <https://test.docker.com/> to install pre-releases of Docker on Linux. This script is equal to the script at `get.docker.com`, but configures your package manager to use the test channel of the Docker package repository. The test channel includes both stable and pre-releases (beta versions, release-candidates) of Docker. Use this script to get early access to new releases, and to evaluate them in a testing environment before they're released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### [Upgrade Docker after using the convenience script](#upgrade-docker-after-using-the-convenience-script)

If you installed Docker using the convenience script, you should upgrade Docker using your package manager directly. There's no advantage to re-running the convenience script. Re-running it can cause issues if it attempts to re-install repositories which already exist on the host machine.

## [Uninstall Docker Engine](#uninstall-docker-engine)

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:

   ```console
   $ sudo dnf remove docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

You have to delete any edited configuration files manually.

## [Next steps](#next-steps)

* Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).

----
url: https://docs.docker.com/ai/docker-agent/reference/examples/
----

# Examples

***

Table of contents

***

Get inspiration from the following agent examples. See more examples in the [Docker Agent GitHub repository](https://github.com/docker/docker-agent/tree/main/examples).

## [Development team](#development-team)

```yaml
models:
  model:
    provider: anthropic
    model: claude-sonnet-4-0
    max_tokens: 64000

agents:
  root:
    model: model
    description: Product Manager - Leads the development team and coordinates iterations
    instruction: |
      You are the Product Manager leading a development team consisting of a designer, frontend engineer, full stack engineer, and QA tester.

      Your responsibilities:
      - Break down user requirements into small, manageable iterations
      - Each iteration should deliver one complete feature end-to-end
      - Ensure each iteration is small enough to be completed quickly but substantial enough to provide value
      - Coordinate between team members to ensure smooth workflow
      - Define clear acceptance criteria for each feature
      - Prioritize features based on user value and technical dependencies

      IMPORTANT ITERATION PRINCIPLES:
      - Start with the most basic, core functionality first
      - Each iteration must result in working, testable code
      - Features should be incrementally built upon previous iterations
      - Don't try to build everything at once - focus on one feature at a time
      - Ensure proper handoffs between designer → frontend → fullstack → QA

      Workflow for each iteration:
      1. Define the feature and acceptance criteria
      2. Have designer create UI mockups/wireframes
      3. Have frontend engineer implement the UI
      4. Have fullstack engineer build backend and integrate
      5. Have QA test the complete feature and report issues
      6. Address any issues before moving to next iteration

      Always start by understanding what the user wants to build, then break it down into logical, small iterations.

      Always make sure to ask the right agent to do the right task using the appropriate toolset. don't try to do everything yourself.

      Always read and write all decisions and important information to a .md file called dev-team.md in the .dev-team directory.
      Make sure to append to the file and edit what is not needed anymore. Consult this file to understand the current state of the project and the team.
      This file might include references to other files that should all be placed inside the .dev-team folder. Don't write anything but code outside of this directory.

    sub_agents: [designer, awesome_engineer]
    toolsets:
      - type: filesystem
      - type: think
      - type: todo
      - type: memory
        path: dev_memory.db
      - type: mcp
        ref: docker:context7

  designer:
    model: model
    description: UI/UX Designer - Creates user interface designs and wireframes
    instruction: |
      You are a UI/UX Designer working on a development team. Your role is to create user-friendly, intuitive designs for each feature iteration.

      Your responsibilities:
      - Create wireframes and mockups for each feature
      - Design responsive layouts that work on different screen sizes
      - Ensure consistent design patterns across the application
      - Consider user experience and accessibility
      - Provide detailed design specifications for the frontend engineer
      - Use modern design principles and best practices

      For each feature you design:
      1. Create a clear wireframe showing layout and components
      2. Specify colors, fonts, spacing, and styling details
      3. Define user interactions and hover states
      4. Consider mobile responsiveness
      5. Provide clear handoff documentation for the frontend engineer

      Keep designs simple and focused on the specific feature being built in the current iteration.
      Build upon previous designs to maintain consistency across the application.

      Always read and write all decisions and important information to a .md file called dev-team.md in the .dev-team directory.
      Make sure to append to the file and edit what is not needed anymore. Consult this file to understand the current state of the project and the team. 
      This file might include references to other files that should all be placed inside the .dev-team folder. Don't write anything but code outside of this directory.
    toolsets:
      - type: filesystem
      - type: think
      - type: memory
        path: dev_memory.db
      - type: mcp
        ref: docker:context7

  awesome_engineer:
    model: model
    description: Awesome Engineer - Implements user interfaces based on designs
    instruction: |
      You are an Awesome Engineer responsible for implementing user interfaces based on the designer's specifications.

      Your responsibilities:
      - Convert design mockups into responsive, interactive web interfaces
      - Write clean, maintainable HTML, CSS, and JavaScript
      - Ensure cross-browser compatibility and mobile responsiveness
      - Implement proper accessibility features
      - Create reusable components and maintain code consistency
      - Integrate with backend APIs provided by the fullstack engineer

      Technical guidelines:
      - Use modern frontend frameworks/libraries (React, Vue, or vanilla JS as appropriate)
      - Write semantic HTML with proper structure
      - Use CSS best practices (flexbox, grid, responsive design)
      - Implement proper error handling for API calls
      - Follow accessibility guidelines (WCAG)
      - Write clean, commented code that's easy to maintain

      For each iteration:
      1. Review the design specifications carefully
      2. Break down the UI into logical components
      3. Implement the interface with proper styling
      4. Test the UI functionality before handoff
      5. Document any deviations from the design and rationale

      Focus on creating a working, polished UI for the specific feature in the current iteration.

      You are also a Full Stack Engineer responsible for building backend systems, APIs, and integrating them with the frontend.

      Your responsibilities:
      - Design and implement backend APIs and services
      - Set up databases and data models
      - Handle authentication, authorization, and security
      - Integrate frontend with backend systems
      - Ensure proper error handling and logging
      - Write tests for backend functionality
      - Deploy and maintain the application infrastructure

      Technical guidelines:
      - Choose appropriate technology stack based on requirements
      - Design RESTful APIs with proper HTTP methods and status codes
      - Implement proper data validation and sanitization
      - Use appropriate database design patterns
      - Follow security best practices
      - Write comprehensive error handling
      - Include proper logging and monitoring
      - Write unit and integration tests

      For each iteration:
      1. Design the backend architecture for the feature
      2. Implement necessary APIs and database changes
      3. Test backend functionality thoroughly
      4. Integrate with the frontend implementation
      5. Ensure end-to-end functionality works correctly
      6. Document API endpoints and usage

      Focus on building robust, scalable backend systems that support the current iteration's feature.
      Ensure seamless integration with the frontend implementation.

      Always read and write all decisions and important information to a .md file called dev-team.md in the .dev-team directory.
      Make sure to append to the file and edit what is not needed anymore. Consult this file to understand the current state of the project and the team. 
      This file might include references to other files that should all be placed inside the .dev-team folder. Don't write anything but code outside of this directory.
    toolsets:
      - type: filesystem
      - type: shell
      - type: think
      - type: memory
        path: dev_memory.db
      - type: mcp
        ref: docker:context7
```

## [Go developer](#go-developer)

```yaml
models:
  claude:
    provider: anthropic
    model: claude-opus-4-6
  haiku:
    provider: anthropic
    model: claude-haiku-4-5

agents:
  root:
    model: claude
    description: Expert Golang Developer specialized in implementing features and improving code quality.
    skills: true
    instruction: |
      **Goal:**
      Help with Go code-related tasks by examining, modifying, and validating code changes.

      TASK
          **Workflow:**
          1. **Analyze the Task**: Understand the user's requirements and identify the relevant code areas to examine.

          2. **Code Examination**: 
          - Search for relevant code files and functions
          - Analyze code structure and dependencies
          - Identify potential areas for modification

          3. **Code Modification**:
          - Make necessary code changes
          - Ensure changes follow best practices
          - Maintain code style consistency

          4. **Validation Loop**:
          - Run linters and tests to check code quality
          - Verify changes meet requirements
          - If issues found, return to step 3
          - Continue until all requirements are met

          5. **Summary**:
          - Very concisely summarize the changes made (not in a file)
          - For trivial tasks, answer the question without extra information
      </TASK>

      **Details:**
       - Be thorough in code examination before making changes
       - Always validate changes before considering the task complete
       - Follow Go best practices
       - Maintain or improve code quality
       - Be proactive in identifying potential issues
       - Only ask for clarification if necessary, try your best to use all the tools to get the info you need

       **Tools:**
        - When needed and possible, call multiple tools concurrently. It's faster and cheaper.

    add_date: true
    add_environment_info: true
    add_prompt_files:
      - AGENTS.md
    sub_agents:
      - librarian
    toolsets:
      - type: filesystem
      - type: shell
      - type: todo
      - type: mcp
        command: gopls
        version: "golang/tools@v0.21.0"
        args: ["mcp"]
    commands:
      fix-lint:
        description: "Fix the lint issues"
        instruction: |
          Fix the lint issues (if any).

          Here the result of the linting command:
          $ task lint
          ${shell({cmd: "task lint"})}

          $go_diagnostics
          ${go_diagnostics()}

          $go_vulncheck
          ${go_vulncheck()}
      remove-comments-tests: "Remove useless comments in test files (*_test.go)"
      commit:
        description: "Commit local changes"
        instruction: |
          Based on the below changes: create a single commit with an appropriate message.

          - Current git status: !shell(cmd="git status")
          - Current git diff (staged and unstaged changes): !shell(cmd="git diff HEAD")
          - Current branch: !shell(cmd="git branch --show-current")
      simplify: "Look at the local changes and try to simplify the code and architecture but don't remove any feature. I just want the code to be easier to read and maintain."
      init: |
        Create an AGENTS.md file for this project by inspecting the codebase. The AGENTS.md should help AI coding agents understand how to work with this project effectively.

        Analyze the project structure and include:
        1. **Development Commands**: Build, test, lint, and run commands (check Makefile, Taskfile.yml, package.json, Cargo.toml, etc.)
        2. **Architecture Overview**: Key packages/modules, their responsibilities, and how they interact
        3. **Code Style and Conventions**: Patterns used, error handling approaches, naming conventions
        4. **Testing Guidelines**: How to run tests, test patterns used, any special testing setup
        5. **Configuration**: Important config files and environment variables
        6. **Common Development Patterns**: Frequently used patterns specific to this codebase
        7. **Key Files Reference**: Quick reference table of important files and their purposes

        Focus on information that would help an AI agent navigate and modify the codebase correctly. Be concise but comprehensive.
      security-review: |
        Perform a security review of the local changes in this Git repository.

        **Workflow:**
        1. **Identify Changes**: Run `git diff` to see uncommitted changes, and `git diff HEAD~1` or `git log --oneline -5` to understand recent commits if needed.

        2. **Security Analysis**: Review the changes for common security issues:
           - **Input Validation**: Check for missing or inadequate input validation
           - **SQL Injection**: Look for raw SQL queries or improper use of query builders
           - **Command Injection**: Identify unsafe use of exec, shell commands, or system calls
           - **Path Traversal**: Check for unsafe file path handling
           - **Sensitive Data Exposure**: Look for hardcoded secrets, API keys, or credentials
           - **Authentication/Authorization**: Review any auth-related changes
           - **Error Handling**: Check for information leakage in error messages
           - **Dependency Security**: Note any new dependencies that should be vetted
           - **Race Conditions**: Identify potential concurrency issues in Go code
           - **Unsafe Pointer Usage**: Check for unsafe package usage

        3. **Go-Specific Checks**:
           - Run `go_vulncheck` to check for known vulnerabilities
           - Review use of `unsafe` package
           - Check for proper context cancellation and timeout handling
           - Verify proper error wrapping and handling

        4. **Report**: Provide a structured security review with:
           - **Summary**: Overall security posture of the changes
           - **Findings**: List of identified issues with severity (Critical/High/Medium/Low/Info)
           - **Recommendations**: Specific suggestions to improve security
           - **Tips**: General security best practices relevant to the changes

  planner:
    model: claude
    instruction: |
      You are a planning agent responsible for gathering user requirements and creating a development plan.
      Always ask clarifying questions to ensure you fully understand the user's needs before creating the plan.
      Once you have a clear understanding, analyze the existing code and create a detailed development plan in a markdown file. Do not write any code yourself.
      Once the plan is created, you will delegate tasks to the root agent. Make sure to provide the file name of the plan when delegating. Write the plan in the current directory.
      Use the `user_prompt` tool to ask questions to the user. Prefer Multiple Choice Questions.
    toolsets:
      - type: filesystem
      - type: user_prompt
    sub_agents:
      - root

  reviewer:
    model: google/gemini-3-pro-preview
    instruction: |
      Give me feedback about the local changes. Don't be too picky, think about code quality, security, duplication, idiomatic Go,
      performance, maintainability, and best practices.
      Provide suggestions for improvements and point out any potential issues.
      Don't be too verbose, keep your review concise and to the point.
    add_prompt_files:
      - AGENTS.md
    sub_agents:
      - librarian
    toolsets:
      - type: filesystem
      - type: shell
      - type: mcp
        command: gopls
        version: "golang/tools@v0.21.0"
        args: ["mcp"]

  librarian:
    model: haiku
    description: Documentation librarian. Can search the Web and look for relevant documentation to help the golang developer agent.
    instruction: |
      You are the librarian, your job is to look for relevant documentation to help the golang developer agent.
      When given a query, search the internet for relevant documentation, articles, or resources that can assist in completing the task.
      Use context7 for searching documentation and brave for general web searches.
      A good source of information available to agents is https://deepwiki.com/.
    toolsets:
      - type: mcp
        ref: docker:context7
      - type: mcp
        ref: docker:brave
      - type: fetch

permissions:
  allow:
    - go_diagnostics
    - go_file_context
    - go_package_api
    - go_symbol_references
    - go_vulncheck
    - go_workspace
    - shell:cmd=gh --version
    - shell:cmd=gh pr view *
    - shell:cmd=gh pr diff *
    - shell:cmd=git remote -v
    - shell:cmd=ls *
    - shell:cmd=cat *
    - shell:cmd=head *
    - shell:cmd=tail *
    - shell:cmd=wc *
    - shell:cmd=find *
    - shell:cmd=grep *
    - shell:cmd=pwd
    - shell:cmd=echo *
    - shell:cmd=which *
    - shell:cmd=type *
    - shell:cmd=file *
    - shell:cmd=stat *
    - shell:cmd=git status*
    - shell:cmd=git log*
    - shell:cmd=git diff*
    - shell:cmd=git show*
    - shell:cmd=git branch*
    - shell:cmd=git remote -v*
    - shell:cmd=git commit *
    - shell:cmd=go test*
    - shell:cmd=go build*
```

## [Technical blog writer](#technical-blog-writer)

```yaml
agents:
  root:
    model: anthropic
    description: Writes technical blog posts
    instruction: |
      You are the leader of a team of AI agents for a technical blog writing workflow.

      Here are the members in your team:
      <team_members>
      - web_search_agent: Searches the web
      - writer: Writes a 750-word technical blog post based on the chosen prompt
      </team_members>

      WORKFLOW
        1. Call the `web_search_agent` agent to search for the web to get important information about the task that is asked

        3. Call the `writer` agent to write a 750-word technical blog post based on the research done by the web_search_agent
      </WORKFLOW>

      - Use the transfer_to_agent tool to call the right agent at the right time to complete the workflow.
      - DO NOT transfer to multiple members at once
      - ONLY CALL ONE AGENT AT A TIME
      - When using the `transfer_to_agent` tool, make exactly one call and wait for the result before making another. Do not batch or parallelize tool calls.
    sub_agents:
      - web_search_agent
      - writer
    toolsets:
      - type: think

  web_search_agent:
    model: anthropic
    add_date: true
    description: Search the web for the information
    instruction: |
      Search the web for the information

      Always include sources
    toolsets:
      - type: mcp
        ref: docker:duckduckgo

  writer:
    model: anthropic
    description: Writes a 750-word technical blog post based on the chosen prompt.
    instruction: |
      You are an agent that receives a single technical writing prompt and generates a detailed, informative, and well-structured technical blog post.

      - Ensure the content is technically accurate and includes relevant code examples, diagrams, or technical explanations where appropriate.
      - Structure the blog post with clear sections, including an introduction, main content, and conclusion.
      - Use technical terminology appropriately and explain complex concepts clearly.
      - Include practical examples and real-world applications where relevant.
      - Make sure the content is engaging for a technical audience while maintaining professional standards.

      Constraints:
      - DO NOT use lists

models:
  anthropic:
    provider: anthropic
    model: claude-sonnet-4-6
```

----
url: https://docs.docker.com/engine/release-notes/17.04/
----

# Docker Engine 17.04 release notes

***

Table of contents

***

## [17.04.0-ce](#17040-ce)

2017-04-05

### [Builder](#builder)

* Disable container logging for build containers [#29552](https://github.com/docker/docker/pull/29552)
* Fix use of `**/` in `.dockerignore` [#29043](https://github.com/docker/docker/pull/29043)

### [Client](#client)

* Sort `docker stack ls` by name [#31085](https://github.com/docker/docker/pull/31085)
* Flags for specifying bind mount consistency [#31047](https://github.com/docker/docker/pull/31047)

- Output of docker CLI --help is now wrapped to the terminal width [#28751](https://github.com/docker/docker/pull/28751)
- Suppress image digest in docker ps [#30848](https://github.com/docker/docker/pull/30848)
- Hide command options that are related to Windows [#30788](https://github.com/docker/docker/pull/30788)
- Fix `docker plugin install` prompt to accept "enter" for the "N" default [#30769](https://github.com/docker/docker/pull/30769)

* Add `truncate` function for Go templates [#30484](https://github.com/docker/docker/pull/30484)

- Support expanded syntax of ports in `stack deploy` [#30476](https://github.com/docker/docker/pull/30476)
- Support expanded syntax of mounts in `stack deploy` [#30597](https://github.com/docker/docker/pull/30597) [#31795](https://github.com/docker/docker/pull/31795)

* Add `--add-host` for docker build [#30383](https://github.com/docker/docker/pull/30383)
* Add `.CreatedAt` placeholder for `docker network ls --format` [#29900](https://github.com/docker/docker/pull/29900)

- Update order of `--secret-rm` and `--secret-add` [#29802](https://github.com/docker/docker/pull/29802)

* Add `--filter enabled=true` for `docker plugin ls` [#28627](https://github.com/docker/docker/pull/28627)
* Add `--format` to `docker service ls` [#28199](https://github.com/docker/docker/pull/28199)
* Add `publish` and `expose` filter for `docker ps --filter` [#27557](https://github.com/docker/docker/pull/27557)

- Support multiple service IDs on `docker service ps` [#25234](https://github.com/docker/docker/pull/25234)

* Allow swarm join with `--availability=drain` [#24993](https://github.com/docker/docker/pull/24993)

- Docker inspect now shows "docker-default" when AppArmor is enabled and no other profile was defined [#27083](https://github.com/docker/docker/pull/27083)

### [Logging](#logging)

* Implement optional ring buffer for container logs [#28762](https://github.com/docker/docker/pull/28762)
* Add `--log-opt awslogs-create-group=<true|false>` for awslogs (CloudWatch) to support creation of log groups as needed [#29504](https://github.com/docker/docker/pull/29504)

- Fix segfault when using the gcplogs logging driver with a "static" binary [#29478](https://github.com/docker/docker/pull/29478)

### [Networking](#networking)

* Check parameter `--ip`, `--ip6` and `--link-local-ip` in `docker network connect` [#30807](https://github.com/docker/docker/pull/30807)

- Added support for `dns-search` [#30117](https://github.com/docker/docker/pull/30117)
- Added --verbose option for docker network inspect to show task details from all swarm nodes [#31710](https://github.com/docker/docker/pull/31710)

* Clear stale datapath encryption states when joining the cluster [docker/libnetwork#1354](https://github.com/docker/libnetwork/pull/1354)

- Ensure iptables initialization only happens once [docker/libnetwork#1676](https://github.com/docker/libnetwork/pull/1676)

* Fix bad order of iptables filter rules [docker/libnetwork#961](https://github.com/docker/libnetwork/pull/961)

- Add anonymous container alias to service record on attachable network [docker/libnetwork#1651](https://github.com/docker/libnetwork/pull/1651)
- Support for `com.docker.network.container_iface_prefix` driver label [docker/libnetwork#1667](https://github.com/docker/libnetwork/pull/1667)
- Improve network list performance by omitting network details that are not used [#30673](https://github.com/docker/docker/pull/30673)

### [Runtime](#runtime)

* Handle paused container when restoring without live-restore set [#31704](https://github.com/docker/docker/pull/31704)

- Do not allow sub second in healthcheck options in Dockerfile [#31177](https://github.com/docker/docker/pull/31177)

* Support name and id prefix in `secret update` [#30856](https://github.com/docker/docker/pull/30856)
* Use binary frame for websocket attach endpoint [#30460](https://github.com/docker/docker/pull/30460)
* Fix linux mount calls not applying propagation type changes [#30416](https://github.com/docker/docker/pull/30416)
* Fix ExecIds leak on failed `exec -i` [#30340](https://github.com/docker/docker/pull/30340)
* Prune named but untagged images if `danglingOnly=true` [#30330](https://github.com/docker/docker/pull/30330)

- Add daemon flag to set `no_new_priv` as default for unprivileged containers [#29984](https://github.com/docker/docker/pull/29984)
- Add daemon option `--default-shm-size` [#29692](https://github.com/docker/docker/pull/29692)
- Support registry mirror config reload [#29650](https://github.com/docker/docker/pull/29650)

* Ignore the daemon log config when building images [#29552](https://github.com/docker/docker/pull/29552)

- Move secret name or ID prefix resolving from client to daemon [#29218](https://github.com/docker/docker/pull/29218)

* Allow adding rules to `cgroup devices.allow` on container create/run [#22563](https://github.com/docker/docker/pull/22563)

- Fix `cpu.cfs_quota_us` being reset when running `systemd daemon-reload` [#31736](https://github.com/docker/docker/pull/31736)

### [Swarm Mode](#swarm-mode)

* Topology-aware scheduling [#30725](https://github.com/docker/docker/pull/30725)
* Automatic service rollback on failure [#31108](https://github.com/docker/docker/pull/31108)
* Worker and manager on the same node are now connected through a UNIX socket [docker/swarmkit#1828](https://github.com/docker/swarmkit/pull/1828), [docker/swarmkit#1850](https://github.com/docker/swarmkit/pull/1850), [docker/swarmkit#1851](https://github.com/docker/swarmkit/pull/1851)

- Improve raft transport package [docker/swarmkit#1748](https://github.com/docker/swarmkit/pull/1748)
- No automatic manager shutdown on demotion/removal [docker/swarmkit#1829](https://github.com/docker/swarmkit/pull/1829)
- Use TransferLeadership to make leader demotion safer [docker/swarmkit#1939](https://github.com/docker/swarmkit/pull/1939)
- Decrease default monitoring period [docker/swarmkit#1967](https://github.com/docker/swarmkit/pull/1967)

* Add Service logs formatting [#31672](https://github.com/docker/docker/pull/31672)

- Fix service logs API to be able to specify stream [#31313](https://github.com/docker/docker/pull/31313)

* Add `--stop-signal` for `service create` and `service update` [#30754](https://github.com/docker/docker/pull/30754)
* Add `--read-only` for `service create` and `service update` [#30162](https://github.com/docker/docker/pull/30162)
* Renew the context after communicating with the registry [#31586](https://github.com/docker/docker/pull/31586)
* (experimental) Add `--tail` and `--since` options to `docker service logs` [#31500](https://github.com/docker/docker/pull/31500)
* (experimental) Add `--no-task-ids` and `--no-trunc` options to `docker service logs` [#31672](https://github.com/docker/docker/pull/31672)

### [Windows](#windows)

* Block pulling Windows images on non-Windows daemons [#29001](https://github.com/docker/docker/pull/29001)

----
url: https://docs.docker.com/reference/cli/docker/sandbox/exec/
----

# docker sandbox exec

***

| Description | Execute a command inside a sandbox                       |
| ----------- | -------------------------------------------------------- |
| Usage       | `docker sandbox exec [OPTIONS] SANDBOX COMMAND [ARG...]` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Execute a command in a sandbox that was previously created with 'docker sandbox create'.

The command and any additional arguments are executed inside the sandbox container.

## [Options](#options)

| Option                      | Default | Description                                             |
| --------------------------- | ------- | ------------------------------------------------------- |
| [`-d, --detach`](#detach)   |         | Detached mode: run command in the background            |
| `--detach-keys`             |         | Override the key sequence for detaching a container     |
| [`-e, --env`](#env)         |         | Set environment variables                               |
| `--env-file`                |         | Read in a file of environment variables                 |
| `-i, --interactive`         |         | Keep STDIN open even if not attached                    |
| `--privileged`              |         | Give extended privileges to the command                 |
| `-t, --tty`                 |         | Allocate a pseudo-TTY                                   |
| [`-u, --user`](#user)       |         | Username or UID (format: \<name\|uid>\[:\<group\|gid>]) |
| [`-w, --workdir`](#workdir) |         | Working directory inside the container                  |

## [Examples](#examples)

### [Execute a command in a sandbox](#execute-a-command-in-a-sandbox)

```console
$ docker sandbox exec my-sandbox ls -la
```

### [Run an interactive shell](#run-an-interactive-shell)

```console
$ docker sandbox exec -it my-sandbox /bin/bash
```

### [Set environment variables (-e, --env)](#env)

```text
--env KEY=VALUE
```

Pass environment variables to the command:

```console
$ docker sandbox exec \
  --env NODE_ENV=development \
  --env DATABASE_URL=postgresql://localhost/myapp \
  my-sandbox npm test
```

### [Set working directory (-w, --workdir)](#workdir)

```text
--workdir PATH
```

Run the command in a specific directory:

```console
$ docker sandbox exec --workdir /app my-sandbox python script.py
```

### [Run as specific user (-u, --user)](#user)

```text
--user USER[:GROUP]
```

Execute command as a different user:

```console
$ docker sandbox exec --user 1000:1000 my-sandbox id
```

### [Run in background (-d, --detach)](#detach)

Run a long-running command in the background:

```console
$ docker sandbox exec -d my-sandbox python server.py
```

----
url: https://docs.docker.com/reference/cli/docker/system/prune/
----

# docker system prune

***

| Description | Remove unused data              |
| ----------- | ------------------------------- |
| Usage       | `docker system prune [OPTIONS]` |

## [Description](#description)

Remove all unused containers, networks, images (both dangling and unused), and optionally, volumes.

## [Options](#options)

| Option                | Default | Description                                                  |
| --------------------- | ------- | ------------------------------------------------------------ |
| `-a, --all`           |         | Remove all unused images not just dangling ones              |
| [`--filter`](#filter) |         | API 1.28+ Provide filter values (e.g. `label=<key>=<value>`) |
| `-f, --force`         |         | Do not prompt for confirmation                               |
| `--volumes`           |         | Prune anonymous volumes                                      |

## [Examples](#examples)

```console
$ docker system prune

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all dangling images
        - unused build cache
Are you sure you want to continue? [y/N] y

Deleted Containers:
f44f9b81948b3919590d5f79a680d8378f1139b41952e219830a33027c80c867
792776e68ac9d75bce4092bc1b5cc17b779bc926ab04f4185aec9bf1c0d4641f

Deleted Networks:
network1
network2

Deleted Images:
untagged: hello-world@sha256:f3b3b28a45160805bb16542c9531888519430e9e6d6ffc09d72261b0d26ff74f
deleted: sha256:1815c82652c03bfd8644afda26fb184f2ed891d921b20a0703b46768f9755c57
deleted: sha256:45761469c965421a92a69cc50e92c01e0cfa94fe026cdd1233445ea00e96289a

Total reclaimed space: 1.84kB
```

By default, volumes aren't removed to prevent important data from being deleted if there is currently no container using the volume. Use the `--volumes` flag when running the command to prune anonymous volumes as well:

```console
$ docker system prune -a --volumes

WARNING! This will remove:
        - all stopped containers
        - all networks not used by at least one container
        - all anonymous volumes not used by at least one container
        - all images without at least one container associated to them
        - all build cache
Are you sure you want to continue? [y/N] y

Deleted Containers:
0998aa37185a1a7036b0e12cf1ac1b6442dcfa30a5c9650a42ed5010046f195b
73958bfb884fa81fa4cc6baf61055667e940ea2357b4036acbbe25a60f442a4d

Deleted Networks:
my-network-a
my-network-b

Deleted Volumes:
1e31bcd425e913d9f65ec0c3841e9c4ebb543aead2a1cfe0d95a7c5e88bb5026
6a6ab3d6b8d740a1c1d4dbe36a9c5f043dd4bac5f78abfa7d1f2ae5789fe60b0

Deleted Images:
untagged: my-curl:latest
deleted: sha256:7d88582121f2a29031d92017754d62a0d1a215c97e8f0106c586546e7404447d
deleted: sha256:dd14a93d83593d4024152f85d7c63f76aaa4e73e228377ba1d130ef5149f4d8b
untagged: alpine:3.3
deleted: sha256:695f3d04125db3266d4ab7bbb3c6b23aa4293923e762aa2562c54f49a28f009f
untagged: alpine:latest
deleted: sha256:ee4603260daafe1a8c2f3b78fd760922918ab2441cbb2853ed5c439e59c52f96
deleted: sha256:9007f5987db353ec398a223bc5a135c5a9601798ba20a1abba537ea2f8ac765f
deleted: sha256:71fa90c8f04769c9721459d5aa0936db640b92c8c91c9b589b54abd412d120ab
deleted: sha256:bb1c3357b3c30ece26e6604aea7d2ec0ace4166ff34c3616701279c22444c0f3
untagged: my-jq:latest
deleted: sha256:6e66d724542af9bc4c4abf4a909791d7260b6d0110d8e220708b09e4ee1322e1
deleted: sha256:07b3fa89d4b17009eb3988dfc592c7d30ab3ba52d2007832dffcf6d40e3eda7f
deleted: sha256:3a88a5c81eb5c283e72db2dbc6d65cbfd8e80b6c89bb6e714cfaaa0eed99c548

Total reclaimed space: 13.5 MB
```

### [Filtering (--filter)](#filter)

The filtering flag (`--filter`) format is of "key=value". If there is more than one filter, then pass multiple flags (e.g., `--filter "foo=bar" --filter "bif=baz"`).

When multiple filters are provided, they are combined as follows:

* Multiple filters with **different keys** are combined using AND logic. An item must satisfy all filter conditions to be pruned.
* Multiple filters with the **same key** are combined using OR logic. An item is pruned if it matches any of the values for that key.

For example, `--filter "label=foo" --filter "until=24h"` prunes items that have the `foo` label **and** were created more than 24 hours ago. Conversely, `--filter "label=foo" --filter "label=bar"` prunes items that have **either** the `foo` **or** `bar` label.

The currently supported filters are:

* until (`<timestamp>`) - only remove containers, images, and networks created before given timestamp
* label (`label=<key>`, `label=<key>=<value>`, `label!=<key>`, or `label!=<key>=<value>`) - only remove containers, images, networks, and volumes with (or without, in case `label!=...` is used) the specified labels.

The `until` filter can be Unix timestamps, date formatted timestamps, or Go duration strings supported by [ParseDuration](https://pkg.go.dev/time#ParseDuration) (e.g. `10m`, `1h30m`) computed relative to the daemon machine’s time. Supported formats for date formatted time stamps include RFC3339Nano, RFC3339, `2006-01-02T15:04:05`, `2006-01-02T15:04:05.999999999`, `2006-01-02T07:00`, and `2006-01-02`. The local timezone on the daemon will be used if you do not provide either a `Z` or a `+-00:00` timezone offset at the end of the timestamp. When providing Unix timestamps enter seconds\[.nanoseconds], where seconds is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds (aka Unix epoch or Unix time), and the optional .nanoseconds field is a fraction of a second no more than nine digits long.

The `label` filter accepts two formats. One is the `label=...` (`label=<key>` or `label=<key>=<value>`), which removes containers, images, networks, and volumes with the specified labels. The other format is the `label!=...` (`label!=<key>` or `label!=<key>=<value>`), which removes containers, images, networks, and volumes without the specified labels.

----
url: https://docs.docker.com/engine/storage/drivers/windowsfilter-driver/
----

# windowsfilter storage driver

***

Table of contents

***

The windowsfilter storage driver is the default storage driver for Docker Engine on Windows. The windowsfilter driver uses Windows-native file system layers to for storing Docker layers and volume data on disk. The windowsfilter storage driver only works on file systems formatted with NTFS.

## [Configure the windowsfilter storage driver](#configure-the-windowsfilter-storage-driver)

For most use case, no configuring the windowsfilter storage driver is not necessary.

The default storage limit for Docker Engine on Windows is 127GB. To use a different storage size, set the `size` option for the windowsfilter storage driver. See [windowsfilter options](https://docs.docker.com/reference/cli/dockerd/#windowsfilter-options).

Data is stored on the Docker host in `image` and `windowsfilter` subdirectories within `C:\ProgramData\docker` by default. You can change the storage location by configuring the `data-root` option in the [Daemon configuration file](https://docs.docker.com/reference/cli/dockerd/#on-windows):

```json
{
  "data-root": "d:\\docker"
}
```

You must restart the daemon for the configuration change to take effect.

## [Additional information](#additional-information)

For more information about how container storage works on Windows, refer to Microsoft's [Containers on Windows documentation](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-storage).

----
url: https://docs.docker.com/build/buildkit/configure/
----

# Configure BuildKit

***

Table of contents

***

If you create a `docker-container` or `kubernetes` builder with Buildx, you can apply a custom [BuildKit configuration](https://docs.docker.com/build/buildkit/toml-configuration/) by passing the [`--buildkitd-config` flag](/reference/cli/docker/buildx/create/#buildkitd-config) to the `docker buildx create` command.

## [Registry mirror](#registry-mirror)

You can define a registry mirror to use for your builds. Doing so redirects BuildKit to pull images from a different hostname. The following steps exemplify defining a mirror for `docker.io` (Docker Hub) to `mirror.gcr.io`.

1. Create a TOML at `/etc/buildkitd.toml` with the following content:

   ```toml
   debug = true
   [registry."docker.io"]
     mirrors = ["mirror.gcr.io"]
   ```

   > Note
   >
   > `debug = true` turns on debug requests in the BuildKit daemon, which logs a message that shows when a mirror is being used.

2. Create a `docker-container` builder that uses this BuildKit configuration:

   ```console
   $ docker buildx create --use --bootstrap \
     --name mybuilder \
     --driver docker-container \
     --buildkitd-config /etc/buildkitd.toml
   ```

3. Build an image:

   ```bash
   docker buildx build --load . -f - <<EOF
   FROM alpine
   RUN echo "hello world"
   EOF
   ```

The BuildKit logs for this builder now shows that it uses the GCR mirror. You can tell by the fact that the response messages include the `x-goog-*` HTTP headers.

```console
$ docker logs buildx_buildkit_mybuilder0
```

```text
...
time="2022-02-06T17:47:48Z" level=debug msg="do request" request.header.accept="application/vnd.docker.container.image.v1+json, */*" request.header.user-agent=containerd/1.5.8+unknown request.method=GET spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=1356 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=1469 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:25:17 GMT" response.header.etag="\"774380abda8f4eae9a149e5d5d3efc83\"" response.header.expires="Sun, 06 Feb 2022 18:25:17 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:57 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788077652182 response.header.x-goog-hash="crc32c=V3DSrg==" response.header.x-goog-hash.1="md5=d0OAq9qPTq6aFJ5dXT78gw==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=1469 response.header.x-guploader-uploadid=ADPycduqQipVAXc3tzXmTzKQ2gTT6CV736B2J628smtD1iDytEyiYCgvvdD8zz9BT1J1sASUq9pW_ctUyC4B-v2jvhIxnZTlKg response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=760 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=1471 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:35:13 GMT" response.header.etag="\"35d688bd15327daafcdb4d4395e616a8\"" response.header.expires="Sun, 06 Feb 2022 18:35:13 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:12 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788032100793 response.header.x-goog-hash="crc32c=aWgRjA==" response.header.x-goog-hash.1="md5=NdaIvRUyfar8201DleYWqA==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=1471 response.header.x-guploader-uploadid=ADPycdtR-gJYwC7yHquIkJWFFG8FovDySvtmRnZBqlO3yVDanBXh_VqKYt400yhuf0XbQ3ZMB9IZV2vlcyHezn_Pu3a1SMMtiw response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg=fetch spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="do request" request.header.accept="application/vnd.docker.image.rootfs.diff.tar.gzip, */*" request.header.user-agent=containerd/1.5.8+unknown request.method=GET spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
time="2022-02-06T17:47:48Z" level=debug msg="fetch response received" response.header.accept-ranges=bytes response.header.age=1356 response.header.alt-svc="h3=\":443\"; ma=2592000,h3-29=\":443\"; ma=2592000,h3-Q050=\":443\"; ma=2592000,h3-Q046=\":443\"; ma=2592000,h3-Q043=\":443\"; ma=2592000,quic=\":443\"; ma=2592000; v=\"46,43\"" response.header.cache-control="public, max-age=3600" response.header.content-length=2818413 response.header.content-type=application/octet-stream response.header.date="Sun, 06 Feb 2022 17:25:17 GMT" response.header.etag="\"1d55e7be5a77c4a908ad11bc33ebea1c\"" response.header.expires="Sun, 06 Feb 2022 18:25:17 GMT" response.header.last-modified="Wed, 24 Nov 2021 21:07:06 GMT" response.header.server=UploadServer response.header.x-goog-generation=1637788026431708 response.header.x-goog-hash="crc32c=ZojF+g==" response.header.x-goog-hash.1="md5=HVXnvlp3xKkIrRG8M+vqHA==" response.header.x-goog-metageneration=1 response.header.x-goog-storage-class=STANDARD response.header.x-goog-stored-content-encoding=identity response.header.x-goog-stored-content-length=2818413 response.header.x-guploader-uploadid=ADPycdsebqxiTBJqZ0bv9zBigjFxgQydD2ESZSkKchpE0ILlN9Ibko3C5r4fJTJ4UR9ddp-UBd-2v_4eRpZ8Yo2llW_j4k8WhQ response.status="200 OK" spanID=9460e5b6e64cec91 traceID=b162d3040ddf86d6614e79c66a01a577
...
```

## [Setting registry certificates](#setting-registry-certificates)

If you specify registry certificates in the BuildKit configuration, the daemon copies the files into the container under `/etc/buildkit/certs`. The following steps show adding a self-signed registry certificate to the BuildKit configuration.

1. Add the following configuration to `/etc/buildkitd.toml`:

   ```toml
   # /etc/buildkitd.toml
   debug = true
   [registry."myregistry.com"]
     ca=["/etc/certs/myregistry.pem"]
     [[registry."myregistry.com".keypair]]
       key="/etc/certs/myregistry_key.pem"
       cert="/etc/certs/myregistry_cert.pem"
   ```

   This tells the builder to push images to the `myregistry.com` registry using the certificates in the specified location (`/etc/certs`).

2. Create a `docker-container` builder that uses this configuration:

   ```console
   $ docker buildx create --use --bootstrap \
     --name mybuilder \
     --driver docker-container \
     --buildkitd-config /etc/buildkitd.toml
   ```

3. Inspect the builder's configuration file (`/etc/buildkit/buildkitd.toml`), it shows that the certificate configuration is now configured in the builder.

   ```console
   $ docker exec -it buildx_buildkit_mybuilder0 cat /etc/buildkit/buildkitd.toml
   ```

   ```toml
   debug = true

   [registry]

     [registry."myregistry.com"]
       ca = ["/etc/buildkit/certs/myregistry.com/myregistry.pem"]

       [[registry."myregistry.com".keypair]]
         cert = "/etc/buildkit/certs/myregistry.com/myregistry_cert.pem"
         key = "/etc/buildkit/certs/myregistry.com/myregistry_key.pem"
   ```

4. Verify that the certificates are inside the container:

   ```console
   $ docker exec -it buildx_buildkit_mybuilder0 ls /etc/buildkit/certs/myregistry.com/
   myregistry.pem    myregistry_cert.pem   myregistry_key.pem
   ```

Now you can push to the registry using this builder, and it will authenticate using the certificates:

```console
$ docker buildx build --push --tag myregistry.com/myimage:latest .
```

## [CNI networking](#cni-networking)

CNI networking for builders can be useful for dealing with network port contention during concurrent builds.

### [Bridge networking](#bridge-networking)

The BuildKit image ships with a built-in bridge network provider that uses a minimal set of bundled CNI plugins, so you don't need to build a custom image or supply your own CNI configuration. To use it, set the worker network mode to `bridge` when you create the builder:

```console
$ docker buildx create --use --bootstrap \
  --name mybuilder \
  --driver docker-container \
  --buildkitd-flags "--oci-worker-net=bridge"
```

BuildKit creates a `buildkit0` bridge with a default subnet of `10.10.0.0/16`, and cleans up the bridge automatically when the daemon shuts down.

### [Custom CNI configuration](#custom-cni-configuration)

For more control over networking, build a custom BuildKit image with your own CNI configuration and plugins.

The following Dockerfile example shows a custom BuildKit image with CNI support. It uses the [CNI config for integration tests](https://github.com/moby/buildkit/blob/master//hack/fixtures/cni.json) in BuildKit as an example. Feel free to include your own CNI configuration.

```dockerfile
# syntax=docker/dockerfile:1

ARG BUILDKIT_VERSION=v0.28.0
ARG CNI_VERSION=v1.0.1

FROM --platform=$BUILDPLATFORM alpine AS cni-plugins
RUN apk add --no-cache curl
ARG CNI_VERSION
ARG TARGETOS
ARG TARGETARCH
WORKDIR /opt/cni/bin
RUN curl -Ls https://github.com/containernetworking/plugins/releases/download/$CNI_VERSION/cni-plugins-$TARGETOS-$TARGETARCH-$CNI_VERSION.tgz | tar xzv

FROM moby/buildkit:${BUILDKIT_VERSION}
ARG BUILDKIT_VERSION
RUN apk add --no-cache iptables
COPY --from=cni-plugins /opt/cni/bin /opt/cni/bin
ADD https://raw.githubusercontent.com/moby/buildkit/${BUILDKIT_VERSION}/hack/fixtures/cni.json /etc/buildkit/cni.json
```

Now you can build this image, and create a builder instance from it using [the `--driver-opt image` option](/reference/cli/docker/buildx/create/#driver-opt):

```console
$ docker buildx build --tag buildkit-cni:local --load .
$ docker buildx create --use --bootstrap \
  --name mybuilder \
  --driver docker-container \
  --driver-opt "image=buildkit-cni:local" \
  --buildkitd-flags "--oci-worker-net=cni"
```

## [Resource limiting](#resource-limiting)

### [Max parallelism](#max-parallelism)

You can limit the parallelism of the BuildKit solver, which is particularly useful for low-powered machines, using a [BuildKit configuration](https://docs.docker.com/build/buildkit/toml-configuration/) while creating a builder with the [`--buildkitd-config` flag](/reference/cli/docker/buildx/create/#buildkitd-config).

```toml
# /etc/buildkitd.toml
[worker.oci]
  max-parallelism = 4
```

Now you can [create a `docker-container` builder](https://docs.docker.com/build/builders/drivers/docker-container/) that will use this BuildKit configuration to limit parallelism.

```console
$ docker buildx create --use \
  --name mybuilder \
  --driver docker-container \
  --buildkitd-config /etc/buildkitd.toml
```

### [TCP connection limit](#tcp-connection-limit)

TCP connections are limited to 4 simultaneous connections per registry for pulling and pushing images, plus one additional connection dedicated to metadata requests. This connection limit prevents your build from getting stuck while pulling images. The dedicated metadata connection helps reduce the overall build time.

More information: [moby/buildkit#2259](https://github.com/moby/buildkit/pull/2259)

----
url: https://docs.docker.com/reference/cli/docker/dhi/mirror/stop/
----

# docker dhi mirror stop

***

| Description | Stop mirroring one or more Docker Hardened Images     |
| ----------- | ----------------------------------------------------- |
| Usage       | `docker dhi mirror stop <repository> [repository...]` |

## [Description](#description)

Stop mirroring one or more Docker Hardened Image repositories.

Multiple repositories can be specified as positional arguments.

Each repository can be specified as:

* namespace/name (e.g., myorg/dhi-python) - org must match --org flag or config
* name only (e.g., dhi-python) - the namespace can be omitted for simplicity and the command will default to the current org automatically

Examples:

# [Stop mirroring a single repository](#stop-mirroring-a-single-repository)

docker dhi mirror stop myorg/dhi-python --org myorg

# [Stop mirroring using just the name (defaults to current org)](#stop-mirroring-using-just-the-name-defaults-to-current-org)

docker dhi mirror stop dhi-python --org myorg

# [Stop mirroring multiple repositories](#stop-mirroring-multiple-repositories)

docker dhi mirror stop dhi-python dhi-golang dhi-node --org myorg

# [Stop mirroring and delete the repositories](#stop-mirroring-and-delete-the-repositories)

docker dhi mirror stop dhi-python dhi-golang --org myorg --delete

# [Stop mirroring, delete without confirmation prompt](#stop-mirroring-delete-without-confirmation-prompt)

docker dhi mirror stop dhi-python dhi-golang --org myorg --delete --force

# [Stop mirroring all repositories matching a filter (using shell substitution)](#stop-mirroring-all-repositories-matching-a-filter-using-shell-substitution)

docker dhi mirror stop $(docker dhi mirror list --org myorg --filter golang --json | jq -r '.\[].repository') --org myorg

## [Options](#options)

| Option        | Default | Description                                         |
| ------------- | ------- | --------------------------------------------------- |
| `--delete`    |         | Delete the repositories after stopping mirroring    |
| `-f, --force` |         | Skip confirmation prompt when deleting repositories |

----
url: https://docs.docker.com/reference/cli/docker/swarm/
----

# docker swarm

***

| Description | Manage Swarm   |
| ----------- | -------------- |
| Usage       | `docker swarm` |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Manage the swarm.

## [Subcommands](#subcommands)

| Command                                                                                     | Description                           |
| ------------------------------------------------------------------------------------------- | ------------------------------------- |
| [`docker swarm ca`](https://docs.docker.com/reference/cli/docker/swarm/ca/)                 | Display and rotate the root CA        |
| [`docker swarm init`](https://docs.docker.com/reference/cli/docker/swarm/init/)             | Initialize a swarm                    |
| [`docker swarm join`](https://docs.docker.com/reference/cli/docker/swarm/join/)             | Join a swarm as a node and/or manager |
| [`docker swarm join-token`](https://docs.docker.com/reference/cli/docker/swarm/join-token/) | Manage join tokens                    |
| [`docker swarm leave`](https://docs.docker.com/reference/cli/docker/swarm/leave/)           | Leave the swarm                       |
| [`docker swarm unlock`](https://docs.docker.com/reference/cli/docker/swarm/unlock/)         | Unlock swarm                          |
| [`docker swarm unlock-key`](https://docs.docker.com/reference/cli/docker/swarm/unlock-key/) | Manage the unlock key                 |
| [`docker swarm update`](https://docs.docker.com/reference/cli/docker/swarm/update/)         | Update the swarm                      |

----
url: https://docs.docker.com/engine/logging/drivers/json-file/
----

# JSON File logging driver

***

Table of contents

***

By default, Docker captures the standard output (and standard error) of all your containers, and writes them in files using the JSON format. The JSON format annotates each line with its origin (`stdout` or `stderr`) and its timestamp. Each log file contains information about only one container.

```json
{
  "log": "Log line is here\n",
  "stream": "stdout",
  "time": "2019-01-01T11:11:11.111111111Z"
}
```

> Warning
>
> The `json-file` logging driver uses file-based storage. These files are designed to be exclusively accessed by the Docker daemon. Interacting with these files with external tools may interfere with Docker's logging system and result in unexpected behavior, and should be avoided.

## [Usage](#usage)

To use the `json-file` driver as the default logging driver, set the `log-driver` and `log-opts` keys to appropriate values in the `daemon.json` file. For more information about configuring Docker using `daemon.json`, see [daemon.json](https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file).

> Note
>
> If you're using Docker Desktop, edit the daemon configuration through the Docker Desktop Dashboard. Open **Settings** and select **Docker Engine**. For details, see [Docker Engine settings](https://docs.docker.com/desktop/settings-and-maintenance/settings/#docker-engine).

The following example sets the log driver to `json-file` and sets the `max-size` and `max-file` options to enable automatic log-rotation.

```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

> Note
>
> `log-opts` configuration options in the `daemon.json` configuration file must be provided as strings. Boolean and numeric values (such as the value for `max-file` in the example above) must therefore be enclosed in quotes (`"`).

Restart Docker for the changes to take effect for newly created containers. Existing containers don't use the new logging configuration automatically.

You can set the logging driver for a specific container by using the `--log-driver` flag to `docker container create` or `docker run`:

```console
$ docker run \
      --log-driver json-file --log-opt max-size=10m \
      alpine echo hello world
```

### [Options](#options)

The `json-file` logging driver supports the following logging options:

| Option         | Description                                                                                                                                                                                                          | Example value                                      |
| -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------- |
| `max-size`     | The maximum size of the log before it is rolled. A positive integer plus a modifier representing the unit of measure (`k`, `m`, or `g`). Defaults to -1 (unlimited).                                                 | `--log-opt max-size=10m`                           |
| `max-file`     | The maximum number of log files that can be present. If rolling the logs creates excess files, the oldest file is removed. **Only effective when `max-size` is also set.** A positive integer. Defaults to 1.        | `--log-opt max-file=3`                             |
| `labels`       | Applies when starting the Docker daemon. A comma-separated list of logging-related labels this daemon accepts. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                | `--log-opt labels=production_status,geo`           |
| `labels-regex` | Similar to and compatible with `labels`. A regular expression to match logging-related labels. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                                | `--log-opt labels-regex=^(production_status\|geo)` |
| `env`          | Applies when starting the Docker daemon. A comma-separated list of logging-related environment variables this daemon accepts. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/). | `--log-opt env=os,customer`                        |
| `env-regex`    | Similar to and compatible with `env`. A regular expression to match logging-related environment variables. Used for advanced [log tag options](https://docs.docker.com/engine/logging/log_tags/).                    | `--log-opt env-regex=^(os\|customer)`              |
| `compress`     | Toggles compression for rotated logs. Defaults to `false` (no compression).                                                                                                                                          | `--log-opt compress=true`                          |

### [Examples](#examples)

This example starts an `alpine` container which can have a maximum of 3 log files no larger than 10 megabytes each.

```console
$ docker run -it --log-opt max-size=10m --log-opt max-file=3 alpine ash
```

----
url: https://docs.docker.com/engine/release-notes/29/
----

# Docker Engine version 29 release notes

***

Table of contents

***

This page describes the latest changes, additions, known issues, and fixes for Docker Engine version 29.

For more information about:

* Deprecated and removed features, see [Deprecated Engine Features](https://docs.docker.com/engine/deprecated/).
* Changes to the Engine API, see [Engine API version history](/reference/api/engine/version-history/).

## [29.5.3](#2953)

*2026-06-03*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.5.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.5.3)
* [moby/moby, 29.5.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.5.3)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements)

* Reduce `docker system df` errors when images are pruned at the same time with the containerd image store. [moby/moby#52672](https://github.com/moby/moby/pull/52672)

### [Packaging updates](#packaging-updates)

* Update containerd (static binaries only) to [v2.2.4](https://github.com/containerd/containerd/releases/tag/v2.2.4). [moby/moby#52683](https://github.com/moby/moby/pull/52683)
* Update Go runtime to [1.26.4](https://go.dev/doc/devel/release#go1.26.4). [moby/moby#52753](https://github.com/moby/moby/pull/52753), [docker/cli#7025](https://github.com/docker/cli/pull/7025)

### [Rootless](#rootless)

* Fix AWS IMDS access with `gvisor-tap-vsock` and UDP port forwarding for non-loopback clients. [moby/moby#52710](https://github.com/moby/moby/pull/52710)
* Fix installation of plugins that require host networking. [moby/moby#52735](https://github.com/moby/moby/pull/52735)
* Update RootlessKit to [v3.0.1](https://github.com/rootless-containers/rootlesskit/releases/tag/v3.0.1). [moby/moby#52710](https://github.com/moby/moby/pull/52710)

## [29.5.2](#2952)

*2026-05-20*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.5.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.5.2)
* [moby/moby, 29.5.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.5.2)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-1)

* Fix a regression introduced in 29.5.1 where `docker cp` failed with "mkdirat: file exists" when a container had a bind mount whose target traversed an in-container symlink (e.g. `/var/run -> /run`). [moby/moby#52655](https://github.com/moby/moby/pull/52655)

## [29.5.1](#2951)

*2026-05-18*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.5.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.5.1)
* [moby/moby, 29.5.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.5.1)

### [Security](#security)

This release includes fixes for multiple security vulnerabilities affecting Docker Engine.

* **CVE-2026-41567** Fix a vulnerability in `docker cp` where archive decompression binaries (e.g. `xz`, `unpigz`) were resolved via `PATH` inside the container filesystem while running as host root, allowing a malicious container to execute arbitrary binaries with host root privileges.\
  [GHSA-x86f-5xw2-fm2r](https://github.com/moby/moby/security/advisories/GHSA-x86f-5xw2-fm2r)

* **CVE-2026-41568** Fix a TOCTOU vulnerability in `docker cp` that allowed a container process to create files or directories at arbitrary locations on the host filesystem.\
  [GHSA-vp62-88p7-qqf5](https://github.com/moby/moby/security/advisories/GHSA-vp62-88p7-qqf5)

* **CVE-2026-42306** Fix a TOCTOU vulnerability in `docker cp` that allowed a container process to redirect a bind mount to an arbitrary location on the host filesystem.\
  [GHSA-rg2x-37c3-w2rh](https://github.com/moby/moby/security/advisories/GHSA-rg2x-37c3-w2rh)

### [Networking](#networking)

* Fix UDP conntrack entries not being deleted when not bound to a specific IP address. [moby/moby#52640](https://github.com/moby/moby/pull/52640)

## [29.5.0](#2950)

*2026-05-14*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.5.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.5.0)
* [moby/moby, 29.5.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.5.0)

> Note
>
> Rootless: `gvisor-tap-vsock` is now the new default rootless network driver and should be preferred over `slirp4netns` which is no longer installed via Docker packaging.

### [New](#new)

* Rootless: Add new default `gvisor-tap-vsock` network driver. [moby/moby#52319](https://github.com/moby/moby/pull/52319)
* Enable private time namespace for containers by default on supported kernels. [moby/moby#52326](https://github.com/moby/moby/pull/52326)
* The `local` logging driver now has support for custom attributes, adding support for the `label`, `label-regex`, `env`, `env-regex`, and `tag` log options. [moby/moby#52348](https://github.com/moby/moby/pull/52348)
* Windows: The daemon now supports listening on a Unix socket (`-H unix://...`), with optional group-based access control via `--group`. [moby/moby#52365](https://github.com/moby/moby/pull/52365)

### [Security](#security-1)

* CVE-2026-32288: Fix a denial of service where pulling a maliciously crafted image could cause the daemon to allocate unbounded memory when processing sparse tar archives. [GHSA-x4jj-h2v8-hqqv](https://github.com/advisories/GHSA-x4jj-h2v8-hqqv). [moby/moby#52478](https://github.com/moby/moby/pull/52478)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-2)

* `docker ps --format` now supports a `.HealthStatus` placeholder to print container health state (`starting`, `healthy`, `unhealthy`) as a dedicated field. [docker/cli#6913](https://github.com/docker/cli/pull/6913)
* Add "time-namespaces" feature flag to disable time-namespaces. [moby/moby#52577](https://github.com/moby/moby/pull/52577)
* containerd integration: Fix auth token requests ignoring per-host TLS settings (custom CAs, insecure-registries). [moby/moby#52600](https://github.com/moby/moby/pull/52600)
* Daemon reload events now signify that the daemon reload has fully completed. [moby/moby#52589](https://github.com/moby/moby/pull/52589)
* Expose diagnostic data about userland proxy in `docker info`. [moby/moby#52321](https://github.com/moby/moby/pull/52321)
* Fix `docker image ls --filter reference=...` (`GET /images/json`) to also match fully qualified canonical image names (e.g. `docker.io/library/alpine`), not only the familiar short form. [moby/moby#52333](https://github.com/moby/moby/pull/52333)
* Fix a bug where leaving an autolock-enabled swarm could leave orphaned state, causing subsequent swarm init to fail with "Swarm is encrypted and needs to be unlocked". [moby/moby#52479](https://github.com/moby/moby/pull/52479)
* Fix an issue where logging errors appeared as empty strings in the daemon log instead of the message that failed to write. [moby/moby#52442](https://github.com/moby/moby/pull/52442)
* Fix incorrect SHARED SIZE and UNIQUE SIZE reporting in `docker system df -v` by including shared content blobs in size calculation. [moby/moby#52482](https://github.com/moby/moby/pull/52482)
* Fix support for CDI specifications that request additional group IDs. [moby/moby#52579](https://github.com/moby/moby/pull/52579)
* Fix volume subpath file mounts over an existing file in the image failing container creation with "not a directory". [moby/moby#52584](https://github.com/moby/moby/pull/52584)
* Sort labels in `volume`, `network`, `config`, and `secret` formatters for deterministic output. [docker/cli#6954](https://github.com/docker/cli/pull/6954)
* Swarm: Prevent corruption of Raft snapshots when swarm state is large. [moby/moby#52441](https://github.com/moby/moby/pull/52441)

### [Packaging updates](#packaging-updates-1)

* Update BuildKit to [v0.30.0](https://github.com/moby/buildkit/releases/tag/v0.30.0). [moby/moby#52618](https://github.com/moby/moby/pull/52618)
* Update Go runtime to [1.26.3](https://go.dev/doc/devel/release#go1.26.3). [moby/moby#52572](https://github.com/moby/moby/pull/52572), [docker/cli#6967](https://github.com/docker/cli/pull/6967)

### [Networking](#networking-1)

* Fix conntrack entries being incorrectly deleted for UDP containers sharing the same port on different IPs when one container is restarted. [moby/moby#52423](https://github.com/moby/moby/pull/52423)
* Fix stale VIP DNS records for swarm service network aliases not being removed during rolling updates. [moby/moby#52236](https://github.com/moby/moby/pull/52236)
* Fix the userland proxy silently dropping UDP datagrams when a previous write to an unavailable backend left a stale ECONNREFUSED error on the socket. [moby/moby#52483](https://github.com/moby/moby/pull/52483)
* Rootless: Properly support `--net=host` and localhost registries. [moby/moby#47103](https://github.com/moby/moby/pull/47103)

### [Rootless](#rootless-1)

* Update RootlessKit to [v3.0.0](https://github.com/rootless-containers/rootlesskit/releases/tag/v3.0.0). [moby/moby#52319](https://github.com/moby/moby/pull/52319)

### [Go SDK](#go-sdk)

* cli/config/configfile: `GetAuthConfig`, `GetCredentialsStore`: normalize hostname when resolving auth. [docker/cli#6846](https://github.com/docker/cli/pull/6846)

### [Deprecations](#deprecations)

* cli/command/image/build: remove deprecated `DefaultDockerfileName` const. [docker/cli#6737](https://github.com/docker/cli/pull/6737)
* cli/command/image/build: remove deprecated `DetectArchiveReader` util. [docker/cli#6737](https://github.com/docker/cli/pull/6737)
* cli/command/image/build: remove deprecated `IsArchive` utility. [docker/cli#6737](https://github.com/docker/cli/pull/6737)
* cli/command/image/build: remove deprecated `ResolveAndValidateContextPath` util. [docker/cli#6737](https://github.com/docker/cli/pull/6737)
* cli/command/image/build: remove deprecated `WriteTempDockerfile` util. [docker/cli#6737](https://github.com/docker/cli/pull/6737)

## [29.4.3](#2943)

*2026-05-06*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.4.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.4.3)
* [moby/moby, 29.4.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.4.3)

### [Security](#security-2)

* **CVE-2026-31431**: Replace the socketcall(2) seccomp deny that broke 32-bit programs with targeted AppArmor (deny network alg) and SELinux (alg\_socket) rules that block AF\_ALG at the LSM layer, covering both socket(2) and socketcall(2) paths without disrupting legitimate 32-bit workloads. [moby/moby#52537](https://github.com/moby/moby/pull/52537)

  On SELinux-based systems, the SELinux mitigation requires the daemon to be configured with `selinux-enabled: true` (via `daemon.json` or the `--selinux-enabled` CLI flag). This option is not enabled by default.

* Fix the default AppArmor profile not being updated on daemon restart, requiring a system reboot to pick up profile changes from daemon upgrades. [moby/moby#52537](https://github.com/moby/moby/pull/52537)

## [29.4.2](#2942)

*2026-05-01*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.4.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.4.2)
* [moby/moby, 29.4.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.4.2)

### [Security](#security-3)

This release includes hardening for **CVE-2026-31431**.

* Block `AF_ALG` sockets and the `socketcall(2)` multiplexer in the default seccomp profile to prevent in-container privilege escalation via the kernel crypto API ("Copy Fail"). [moby/moby#52501](https://github.com/moby/moby/pull/52501)

### [Known issues](#known-issues)

The hardening can break 32-bit programs and i386 images, including SteamCMD and some Wine-based workloads. [moby/moby#52506](https://github.com/moby/moby/issues/52506)

#### [Workaround](#workaround)

> Warning
>
> Don't use `--security-opt seccomp=unconfined` to work around this issue.\
> Don't use the `seccomp/v0.2.0` profile.

If you need a workaround, use the `seccomp/v0.2.1` profile from `moby/profiles`. Make sure you use a kernel that includes the fix for CVE-2026-31431.

This profile unblocks `socketcall` while keeping `AF_ALG` blocked for `socket`.

> Important
>
> Use this workaround only for containers that require it.\
> Containers that use this profile can still exploit CVE-2026-31431 through the `socketcall` syscall.

Download the `seccomp/v0.2.1` profile:

```console
$ curl -fsSL https://raw.githubusercontent.com/moby/profiles/refs/tags/seccomp/v0.2.1/seccomp/default.json \
  -o /etc/docker/seccomp-profile-v0.2.1.json
```

Use one of these options. You don't need both.

1. To use the profile for a specific container when you control the `docker run` command, use `--security-opt`:

```console
$ docker run --security-opt seccomp=<path> ...
```

2. To use the profile as the default for containers created by the daemon, add `seccomp-profile` to your `daemon.json`:

```json
{
  "seccomp-profile": "/etc/docker/seccomp-profile-v0.2.1.json"
}
```

## [29.4.1](#2941)

*2026-04-20*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.4.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.4.1)
* [moby/moby, 29.4.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.4.1)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-3)

* containerd image store: Fix `docker image prune --filter label!=key=value` incorrectly skipping images that don't have the specified label. [moby/moby#52338](https://github.com/moby/moby/pull/52338)
* Fix `--log-opt "tag={{.ImageID}}"` not stripping the digest's algorithm. [moby/moby#52343](https://github.com/moby/moby/pull/52343)
* Fix intermittent container start failures (`EBUSY` on secrets/configs remount) on busy Swarm nodes by retrying the read-only remount. [moby/moby#52235](https://github.com/moby/moby/pull/52235)

### [Packaging updates](#packaging-updates-2)

* Update containerd (static binaries only) to [v2.2.3](https://github.com/containerd/containerd/releases/tag/v2.2.3). [moby/moby#52360](https://github.com/moby/moby/pull/52360)
* Update Go runtime to [1.26.2](https://go.dev/doc/devel/release#go1.26.2). [docker/cli#6920](https://github.com/docker/cli/pull/6920), [moby/moby#52329](https://github.com/moby/moby/pull/52329)

### [Networking](#networking-2)

* if a container has an IPv4-only or an IPv6-only endpoint with higher "gateway priority" than a dual stack endpoint, the single stack endpoint will now be used as the default gateway for its address family. [moby/moby#52328](https://github.com/moby/moby/pull/52328)

## [29.4.0](#2940)

*2026-04-07*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.4.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.4.0)
* [moby/moby, 29.4.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.4.0)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-4)

* docker cp: report both content size and transferred size. [docker/cli#6800](https://github.com/docker/cli/pull/6800)
* Fix `docker stats --all` still showing containers that were removed. [docker/cli#6863](https://github.com/docker/cli/pull/6863)
* Fix a rare bug that could cause containers to become unremovable. [moby/moby#51724](https://github.com/moby/moby/pull/51724)
* Fixed privileged containers losing their explicit AppArmor profile (`--security-opt apparmor=<profile>`) after a container restart. [moby/moby#52215](https://github.com/moby/moby/pull/52215)
* Improved duplicate container-exit handling by using live containerd task state (not timestamps). [moby/moby#52156](https://github.com/moby/moby/pull/52156)
* Improved image pull and push performance by enabling HTTP keep-alive for registry connections, avoiding redundant TCP and TLS handshakes. [moby/moby#52198](https://github.com/moby/moby/pull/52198)
* shell completions: add shell completion for `docker rm --link` and exclude legacy links for container names. [docker/cli#6872](https://github.com/docker/cli/pull/6872)
* shell completions: don't provide completions that were already used. [docker/cli#6871](https://github.com/docker/cli/pull/6871)
* Update runc (in static binaries) to [v1.3.5](https://github.com/opencontainers/runc/releases/tag/v1.3.5). [moby/moby#52244](https://github.com/moby/moby/pull/52244)
* Windows: Fix `DOCKER_TMPDIR` not being respected. [moby/moby#52181](https://github.com/moby/moby/pull/52181)

### [Packaging updates](#packaging-updates-3)

* Update BuildKit to [v0.29.0](https://github.com/moby/buildkit/releases/tag/v0.29.0). [moby/moby#52272](https://github.com/moby/moby/pull/52272)

### [Networking](#networking-3)

* Prevent a daemon crash during startup after upgrading if a container config containers a malformed IP-address. [moby/moby#52275](https://github.com/moby/moby/pull/52275)

### [Go SDK](#go-sdk-1)

* cli/streams: Out, In: preserve original os.File when available. [docker/cli#6906](https://github.com/docker/cli/pull/6906)
* Update minimum go version to go1.25. [docker/cli#6897](https://github.com/docker/cli/pull/6897)

### [Deprecations](#deprecations-1)

* Go SDK: cli-plugins/hooks: deprecate `HookMessage `and rename to `cli-plugins/hooks.Response`. [docker/cli#6859](https://github.com/docker/cli/pull/6859)
* Go SDK: cli-plugins/hooks: deprecate `HookType` and rename to `cli-plugins/hooks.ResponseType`. [docker/cli#6859](https://github.com/docker/cli/pull/6859)
* Go SDK: cli-plugins/manager: deprecate `HookPluginData` and move to `cli-plugins/hooks.Request`. [docker/cli#6859](https://github.com/docker/cli/pull/6859)

## [29.3.1](#2931)

*2026-03-25*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.3.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.3.1)
* [moby/moby, 29.3.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.3.1)

### [Security](#security-4)

This release includes fixes for multiple security vulnerabilities affecting Docker Engine and related components.

* **CVE-2026-34040** Fix an authorization bypass in AuthZ plugins that could allow authorization plugins to be bypassed under specific conditions. [GHSA-x744-4wpc-v9h2](https://github.com/moby/moby/security/advisories/GHSA-x744-4wpc-v9h2)

* **CVE-2026-33997** Fix a flaw in `docker plugin install` where privilege validation could be partially bypassed, potentially leading to unauthorized privilege escalation. [GHSA-pxq6-2prw-chj9](https://github.com/moby/moby/security/advisories/GHSA-pxq6-2prw-chj9)

* **CVE-2026-33748** Fix insufficient validation of Git URL `#ref:subdir` fragments in BuildKit, which could allow access to files outside the intended repository scope. [GHSA-4vrq-3vrq-g6gg](https://github.com/moby/buildkit/security/advisories/GHSA-4vrq-3vrq-g6gg)

* **CVE-2026-33747** Fix a vulnerability in BuildKit where an untrusted frontend could cause files to be written outside the BuildKit state directory. [GHSA-3c29-8rgm-jvjj](https://github.com/moby/buildkit/security/advisories/GHSA-4c29-8rgm-jvjj)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-5)

* Fix a daemon crash during docker build if `.dockerignore` contained an invalid pattern. [moby/moby#52214](https://github.com/moby/moby/pull/52214)
* Fix a panic when the containerd client uses a closed stream. [moby/moby#52211](https://github.com/moby/moby/pull/52211)

### [Packaging updates](#packaging-updates-4)

* Update containerd (static binaries) to [v2.2.2](https://github.com/containerd/containerd/releases/tag/v2.2.2). [moby/moby#52213](https://github.com/moby/moby/pull/52213)
* Update Go runtime to [1.25.8](https://go.dev/doc/devel/release#go1.25.8). [moby/moby#52210](https://github.com/moby/moby/pull/52210), [docker/cli#6883](https://github.com/docker/cli/pull/6883)

### [Go SDK](#go-sdk-2)

* Add missing build-tag, which could cause `cannot range over 10 (untyped int constant)` when importing the `cli/command` package. [docker/cli#6884](https://github.com/docker/cli/pull/6884)

## [29.3.0](#2930)

*2026-03-05*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.3.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.3.0)
* [moby/moby, 29.3.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.3.0)

### [New](#new-1)

* Add `bind-create-src` option to `--mount` flag for bind mounts. [docker/cli#6792](https://github.com/docker/cli/pull/6792)
* CLI plugin hooks now fire on command failure (not just success), and plugins can use "error-hooks" to show hints only when commands fail. [docker/cli#6794](https://github.com/docker/cli/pull/6794)
* Lower minimum API version from v1.44 to v1.40 (Docker 19.03). [moby/moby#52067](https://github.com/moby/moby/pull/52067)

### [Packaging updates](#packaging-updates-5)

* Update BuildKit to [v0.28.0](https://github.com/moby/buildkit/releases/tag/v0.28.0). [moby/moby#52135](https://github.com/moby/moby/pull/52135)

### [Networking](#networking-4)

* Fix DNS config corruption on daemon reload. [moby/moby#52060](https://github.com/moby/moby/pull/52060)

### [API](#api)

* `POST /networks/{id}/connect` now correctly applies the `MacAddress` field in `EndpointSettings`. This field was added in API v1.44, but was previously ignored. [moby/moby#52040](https://github.com/moby/moby/pull/52040)
* `GET /images/json` now supports an `identity` query parameter. When set, the response includes manifest summaries and may include an `Identity` field for each manifest with trusted identity and origin information. [moby/moby#52030](https://github.com/moby/moby/pull/52030)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-6)

* The `--gpus` option now uses CDI-based injection for AMD GPUs. [moby/moby#52048](https://github.com/moby/moby/pull/52048)
* Add `sd_notify` ["RELOADING"](https://www.freedesktop.org/software/systemd/man/latest/sd_notify.html#RELOADING=1) notifications when signalling the daemon to reload its configuration. [moby/moby#52041](https://github.com/moby/moby/pull/52041)
* Send `sd_notify` ["READY"](https://www.freedesktop.org/software/systemd/man/latest/sd_notify.html#READY=1) and ["STOPPING"](https://www.freedesktop.org/software/systemd/man/latest/sd_notify.html#STOPPING=1) synchronously to make sure they are sent before we proceed. [moby/moby#52041](https://github.com/moby/moby/pull/52041)
* Add support for the systemd 253 `Type=notify-reload` service reload protocol. [moby/moby#52041](https://github.com/moby/moby/pull/52041)
* Don't log "failed to determine if container is already mounted" warnings for stopped containers during startup. [moby/moby#52076](https://github.com/moby/moby/pull/52076)
* Fix `docker system prune` failing with "rw layer snapshot not found" when a container is concurrently removed. [moby/moby#52090](https://github.com/moby/moby/pull/52090)
* Fix a panic when running `docker top` on a non-running Windows container. [moby/moby#52025](https://github.com/moby/moby/pull/52025)
* Fix a regression in v29.2.0 that prevented registering the dockerd service on Windows if system requirements were not yet installed. [moby/moby#52006](https://github.com/moby/moby/pull/52006)
* Fix shared mount detection for paths mounted multiple times, which caused "not a shared mount" errors when using bind propagation. [moby/moby#51787](https://github.com/moby/moby/pull/51787)
* Fix spurious "ShouldRestart failed" warning on shutdown. [moby/moby#52079](https://github.com/moby/moby/pull/52079)
* Preserve leading and trailing whitespace when storing registry passwords. [docker/cli#6784](https://github.com/docker/cli/pull/6784)
* Prevent logging "not found" warnings when calculating volume sizes. [moby/moby#52018](https://github.com/moby/moby/pull/52018)
* Update Go runtime to [1.25.7](https://go.dev/doc/devel/release#go1.25.7). [moby/moby#52003](https://github.com/moby/moby/pull/52003), [docker/cli#6780](https://github.com/docker/cli/pull/6780)

## [29.2.1](#2921)

*2026-02-02*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.2.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.2.1)
* [moby/moby, 29.2.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.2.1)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-7)

* Update BuildKit to [v0.27.1](https://github.com/moby/buildkit/releases/tag/v0.27.1). [moby/moby#51962](https://github.com/moby/moby/pull/51962)
* Fix `docker system df` failing when run concurrently with `docker system prune`. [moby/moby#51979](https://github.com/moby/moby/pull/51979)
* Fix daemon handling of duplicate container exit events to avoid repeated cleanup and state transitions. [moby/moby#51925](https://github.com/moby/moby/pull/51925)
* Fix panic after failed daemon initialization. [moby/moby#51943](https://github.com/moby/moby/pull/51943)
* Fix encrypted overlay networks not passing traffic to containers on v28 and older Engines. Encrypted overlay networks will no longer pass traffic to containers on v29.2.0 thru v29.0.0, v28.2.2, v25.0.14 or v25.0.13. [moby/moby#51951](https://github.com/moby/moby/pull/51951)
* Fix potential panic on `docker network prune`. [moby/moby#51966](https://github.com/moby/moby/pull/51966)

## [29.2.0](#2920)

*2026-01-26*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.2.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.2.0)
* [moby/moby, 29.2.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.2.0)

### [New](#new-2)

* `docker info` now includes `NRI` section. [docker/cli#6710](https://github.com/docker/cli/pull/6710)
* Add experimental NRI support. [moby/moby#51711](https://github.com/moby/moby/pull/51711), [moby/moby#51712](https://github.com/moby/moby/pull/51712), [moby/moby#51675](https://github.com/moby/moby/pull/51675), [moby/moby#51674](https://github.com/moby/moby/pull/51674), [moby/moby#51636](https://github.com/moby/moby/pull/51636), [moby/moby#51634](https://github.com/moby/moby/pull/51634)
* New `Identity` field has been added to the inspect endpoint to show trusted origin information about the image. This includes build ref for locally built images, remote registry repository for pulled images, and verified signature information for images that contain a valid signed provenance attestation. [moby/moby#51737](https://github.com/moby/moby/pull/51737)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-8)

* Improve validation of `--detach-keys` command-line options. [docker/cli#6742](https://github.com/docker/cli/pull/6742)
* Prevent a potential panic on daemon shutdown after an incomplete initialization. [moby/moby#51797](https://github.com/moby/moby/pull/51797)
* Remove restriction on anonymous read-only volumes. [moby/moby#51682](https://github.com/moby/moby/pull/51682)
* The `--validate` flag on dockerd now also verifies system requirements, allowing for system requirements to be checked before starting the daemon. [moby/moby#51868](https://github.com/moby/moby/pull/51868)
* Handle `--gpus` requests for NVIDIA devices using CDI if possible. [moby/moby#50228](https://github.com/moby/moby/pull/50228)

### [Packaging updates](#packaging-updates-6)

* Update BuildKit to [v0.27.0](https://github.com/moby/buildkit/releases/tag/v0.27.0). [moby/moby#51886](https://github.com/moby/moby/pull/51886)
* Update containerd (static binaries only) to [v2.2.1](https://github.com/containerd/containerd/releases/tag/v2.2.1). [moby/moby#51765](https://github.com/moby/moby/pull/51765)

### [Rootless](#rootless-2)

* Rootless: Consider `$XDG_CONFIG_HOME/cdi` and `$XDG_RUNTIME_DIR/cdi` when looking for CDI devices. [moby/moby#51624](https://github.com/moby/moby/pull/51624)
* Update RootlessKit to [v2.3.6](https://github.com/rootless-containers/rootlesskit/releases/tag/v2.3.6). [moby/moby#51757](https://github.com/moby/moby/pull/51757)

### [API](#api-1)

* Natively support gRPC on the listening socket. [moby/moby#50744](https://github.com/moby/moby/pull/50744)

### [Go SDK](#go-sdk-3)

* cli/command: add WithAPIClientOptions option. [docker/cli#6740](https://github.com/docker/cli/pull/6740)

### [Deprecations](#deprecations-2)

* Remove `%PROGRAMDATA%\Docker\cli-plugins` from the list of paths used for CLI plugins on Windows. This path was present for backward compatibility with old installation, but replaced by `%ProgramFiles%\Docker\cli-plugins`. [docker/cli#6713](https://github.com/docker/cli/pull/6713)

## [29.1.5](#2915)

*2026-01-16*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.1.5 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.5)
* [moby/moby, 29.1.5 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.5)

### [Packaging updates](#packaging-updates-7)

* Update Go runtime to [1.25.6](https://go.dev/doc/devel/release#go1.25.6). [moby/moby#51860](https://github.com/moby/moby/pull/51860), [docker/cli#6750](https://github.com/docker/cli/pull/6750)

### [Networking](#networking-5)

* Fixed a regression where established network connections could be disrupted during a container's shutdown grace period. [moby/moby#51843](https://github.com/moby/moby/pull/51843)

## [29.1.4](#2914)

*2026-01-08*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.1.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.4)
* [moby/moby, 29.1.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.4)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-9)

* Fix `docker run --network none` panic on Windows. [moby/moby#51830](https://github.com/moby/moby/pull/51830)
* Fix image mounts failing with "file name too long" for long mount paths. [moby/moby#51829](https://github.com/moby/moby/pull/51829)
* Fix potential creation of orphaned overlay2 layers. [moby/moby#51826](https://github.com/moby/moby/pull/51826), [moby/moby#51824](https://github.com/moby/moby/pull/51824)

### [Packaging updates](#packaging-updates-8)

* Update BuildKit to [v0.26.3](https://github.com/moby/buildkit/releases/tag/v0.26.3). [moby/moby#51821](https://github.com/moby/moby/pull/51821)

## [29.1.3](#2913)

*2025-12-12*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.1.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.3)
* [moby/moby, 29.1.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.3)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-10)

* Add shell completion for `docker stack deploy --compose-file`. [docker/cli#6690](https://github.com/docker/cli/pull/6690)
* containerd image store: Fix a bug causing `docker build` to ignore the explicitly set `unpack` image exporter option. [moby/moby#51514](https://github.com/moby/moby/pull/51514)
* Fix `docker image ls` dangling image handling. [docker/cli#6704](https://github.com/docker/cli/pull/6704)
* Fix a bug that could cause the Engine to leave containers with autoremove set in 'dead' state on shutdown, and never reclaim them. [moby/moby#51693](https://github.com/moby/moby/pull/51693)
* Fix build on i386. [moby/moby#51528](https://github.com/moby/moby/pull/51528)
* Fix explicit graphdriver configuration (`"storage-driver"`) being treated as containerd snapshotter when prior graphdriver state exists. [moby/moby#51516](https://github.com/moby/moby/pull/51516)
* Fix potential creation of orphaned overlay2 layers. [moby/moby#51703](https://github.com/moby/moby/pull/51703)

### [Networking](#networking-6)

* Allow creation of a container with a specific IP address when its networks were not configured with a specific subnet. [moby/moby#51583](https://github.com/moby/moby/pull/51583)
* Don't crash when starting a container created via the API before upgrade to v29.1.2, with `PublishAll` and a nil `PortBindings` map. [moby/moby#51691](https://github.com/moby/moby/pull/51691)
* Fix a bug preventing DNS resolution of containers attached to non swarm-scoped networks once the node has joined a Swarm cluster. [moby/moby#51515](https://github.com/moby/moby/pull/51515)
* Fix an issue that caused daemon crash when using a remote network driver plugin. [moby/moby#51558](https://github.com/moby/moby/pull/51558)
* Fix an issue that could lead to an "endpoint not found" error when creating a container with multiple network connections, when one of the networks is non-internal but does not have its own external IP connectivity. [moby/moby#51538](https://github.com/moby/moby/pull/51538)
* Fix an issue that prevented rootless Docker from starting on a host with IPv6 disabled. [moby/moby#51543](https://github.com/moby/moby/pull/51543)
* Return an error when a container is created with a port-mapping pointing to container port 0. [moby/moby#51695](https://github.com/moby/moby/pull/51695)

## [29.1.2](#2912)

*2025-12-02*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.1.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.2)
* [moby/moby, 29.1.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.2)

### [Security](#security-5)

* Update Go runtime to [1.25.5](https://go.dev/doc/devel/release#go1.25.5). [moby/moby#51648](https://github.com/moby/moby/pull/51648), [docker/cli#6688](https://github.com/docker/cli/pull/6688)

  * Fixes a potential DoS via excessive resource usage when formatting hostname validation errors [**CVE-2025-61729**](https://nvd.nist.gov/vuln/detail/CVE-2025-61729)
  * Fixes incorrect enforcement of excluded subdomain constraints for wildcard SANs, which could allow improperly trusted certificates [**CVE-2025-61727**](https://nvd.nist.gov/vuln/detail/CVE-2025-22874)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-11)

* containerd image store: Fix `docker image inspect` failing to return available image data in case where not all distributable blobs are available locally. [moby/moby#51629](https://github.com/moby/moby/pull/51629)
* dockerd-rootless-setuptool.sh: fix `nsenter: no namespace specified`. [moby/moby#51622](https://github.com/moby/moby/pull/51622)
* Fix `docker system df` showing `N/A` for shared size and unique size when using graph-drivers as storage. [moby/moby#51631](https://github.com/moby/moby/pull/51631)

### [Packaging updates](#packaging-updates-9)

* Update runc (in static binaries) to [v1.3.4](https://github.com/opencontainers/runc/releases/tag/v1.3.4). [moby/moby#51633](https://github.com/moby/moby/pull/51633)

### [Networking](#networking-7)

* Fix a bug preventing port mappings in rootless mode when slirp4netns is used. [moby/moby#51616](https://github.com/moby/moby/pull/51616)
* Prevent a crash when making an API request with `HostConfig.PublishAllPorts` set (`-P`), and no port bindings. [moby/moby#51621](https://github.com/moby/moby/pull/51621)

## [29.1.1](#2911)

*2025-11-28*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.1.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.1)
* [moby/moby, 29.1.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.1)

### [Networking](#networking-8)

* Revert a PR breaking external DNS resolution on all custom bridge networks. [moby/moby#51615](https://github.com/moby/moby/pull/51615)

## [29.1.0](#2910)

*2025-11-27*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.1.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.1.0)
* [moby/moby, 29.1.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.1.0)

### [Packaging updates](#packaging-updates-10)

* Update BuildKit to [v0.26.1](https://github.com/moby/buildkit/releases/tag/v0.26.1). [moby/moby#51551](https://github.com/moby/moby/pull/51551)
* Update containerd binary to v2.2.0 (static binaries). [moby/moby#51271](https://github.com/moby/moby/pull/51271)

### [Networking](#networking-9)

* Do not overwrite user-modified `/etc/resolv.conf` across container restarts. [moby/moby#51507](https://github.com/moby/moby/pull/51507)
* fix `--publish-all` / `-P` for Windows containers. [moby/moby#51586](https://github.com/moby/moby/pull/51586)
* Fix an issue that prevented container restart or network reconnection when gateway configuration failed during container stop or network disconnect. [moby/moby#51592](https://github.com/moby/moby/pull/51592)
* Windows containers: don't display an IPv6-mapped IPv4 address in port mappings. For example, `[::ffff:0.0.0.0]:8080->80/tcp` instead of `0.0.0.0:8080->80/tcp`. [moby/moby#51587](https://github.com/moby/moby/pull/51587)

## [29.0.4](#2904)

*2025-11-24*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.0.4 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.4)
* [moby/moby, 29.0.4 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.4)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-12)

* `docker image ls` no longer truncates the image names. [docker/cli#6675](https://github.com/docker/cli/pull/6675)

### [Networking](#networking-10)

* Allow creation of a container with a specific IP address when its networks were not configured with a specific subnet. [moby/moby#51583](https://github.com/moby/moby/pull/51583)

## [29.0.3](#2903)

*2025-11-24*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.0.3 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.3)
* [moby/moby, 29.0.3 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.3)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-13)

* `docker version --format json`: restore top-level `BuildTime` field to use RFC3339Nano format. [docker/cli#6668](https://github.com/docker/cli/pull/6668)
* Fix `docker image ls` ignoring a custom `imageFormat` from `docker.json`. [docker/cli#6667](https://github.com/docker/cli/pull/6667)

### [Networking](#networking-11)

* Fix an issue that caused daemon crash when using a remote network driver plugin. [moby/moby#51558](https://github.com/moby/moby/pull/51558)

## [29.0.2](#2902)

*2025-11-17*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.0.2 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.2)
* [moby/moby, 29.0.2 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.2)

### [Networking](#networking-12)

* Fix an issue that could lead to an "endpoint not found" error when creating a container with multiple network connections, when one of the networks is non-internal but does not have its own external IP connectivity. [moby/moby#51538](https://github.com/moby/moby/pull/51538)
* Fix an issue that prevented rootless Docker from starting on a host with IPv6 disabled. [moby/moby#51543](https://github.com/moby/moby/pull/51543)

## [29.0.1](#2901)

*2025-11-14*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.0.1 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.1)
* [moby/moby, 29.0.1 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.1)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-14)

* `docker image ls` no longer truncates the name width when output is redirect (e.g. for `grep`). [docker/cli#6656](https://github.com/docker/cli/pull/6656)
* `docker image ls` now considers the `NO_COLOR` environment variable for choosing the colored output. [docker/cli#6654](https://github.com/docker/cli/pull/6654)
* containerd image store: Fix a bug causing `docker build` to ignore the explicitly set `unpack` image exporter option. [moby/moby#51514](https://github.com/moby/moby/pull/51514)
* Fix a bug causing `docker image ls --all` to not show untagged/dangling images. [docker/cli#6657](https://github.com/docker/cli/pull/6657)
* Fix build on i386. [moby/moby#51528](https://github.com/moby/moby/pull/51528)
* Fix explicit graphdriver configuration (`"storage-driver"`) being treated as containerd snapshotter when prior graphdriver state exists. [moby/moby#51516](https://github.com/moby/moby/pull/51516)
* Fix output format of the `ApiVersion` and `MinApiVersion` fields in `docker version --format=json` to align with previous versions. [docker/cli#6648](https://github.com/docker/cli/pull/6648)

### [Networking](#networking-13)

* Fix a bug preventing DNS resolution of containers attached to non swarm-scoped networks once the node has joined a Swarm cluster. [moby/moby#51515](https://github.com/moby/moby/pull/51515)

## [29.0.0](#2900)

*2025-11-10*

For a full list of pull requests and changes in this release, refer to the relevant GitHub milestones:

* [docker/cli, 29.0.0 milestone](https://github.com/docker/cli/issues?q=is%3Aclosed+milestone%3A29.0.0)
* [moby/moby, 29.0.0 milestone](https://github.com/moby/moby/issues?q=is%3Aclosed+milestone%3A29.0.0)

> Caution
>
> This release includes several breaking changes and deprecations. Review the release notes carefully before upgrading.

* Experimental support for nftables can now be enabled by setting Docker daemon's `firewall-backend` option to `nftables`. For more information, see [Docker Engine docs](https://docs.docker.com/engine/network/firewall-nftables/).
* containerd image store is now the default for **fresh installs**. This doesn't apply to daemons configured with `userns-remap` (see [moby#47377](https://github.com/moby/moby/issues/47377)).

### [Breaking Changes](#breaking-changes)

* The Go module `github.com/docker/docker` is deprecated in favor of `github.com/moby/moby/client` and `github.com/moby/moby/api`. The `github.com/moby/moby` module is considered an **internal implementation detail** - the only supported public modules are `client` and `api`. Starting with v29, releases are tagged with the `docker-` prefix (e.g., `docker-v29.0.0`). **This only affects Go module users and package maintainers.**
* The daemon now requires API version `v1.44` or later (Docker v25.0+).
* Debian armhf (32-bit) packages now target ARMv7 CPUs and will not work on ARMv6 devices.
* Official Raspbian (32-bit) packages are no longer provided. Use Debian arm64 packages for 64-bit devices, or Debian armhf packages for 32-bit ARMv7 devices.
* **cgroup v1 is deprecated.** Support continues until at least May 2029, but migrate to cgroup v2 as soon as possible. See [moby#51111](https://github.com/moby/moby/issues/51111).
* Docker Content Trust was removed from the Docker CLI. Can be built as a separate plugin: <https://github.com/docker/cli/blob/v29.0.0/cmd/docker-trust/main.go>

***

### [New](#new-3)

* `docker image load` and `docker image save` now supports multiple platform selection via `--platform` flag (e.g., `docker image load --platform linux/amd64,linux/arm64 -i image.tar`). [docker/cli#6126](https://github.com/docker/cli/pull/6126)
* `docker image ls` now uses the new view (like `--tree` but collapsed) by default. [docker/cli#6566](https://github.com/docker/cli/pull/6566)
* `docker run --runtime <...>` is now supported on Windows. [moby/moby#50546](https://github.com/moby/moby/pull/50546)
* `GET /containers/json` now includes a `Health` field describing container healthcheck status. [moby/moby#50281](https://github.com/moby/moby/pull/50281)
* Add `device` entitlement to builder configuration. [moby/moby#50386](https://github.com/moby/moby/pull/50386)
* Add support for `memory-swap` and `memory-swappiness` flags to `docker service create` and `docker service update` commands. [docker/cli#6619](https://github.com/docker/cli/pull/6619)
* Allow Docker CLI to set the `GODEBUG` environment variable when the key-value pair (`"GODEBUG":"..."`) exists inside the Docker context metadata. [docker/cli#6371](https://github.com/docker/cli/pull/6371)

### [Bug fixes and enhancements](#bug-fixes-and-enhancements-15)

* `docker image ls --tree` now sorts images alphabetically by name instead of by creation date. [docker/cli#6595](https://github.com/docker/cli/pull/6595)
* `docker image ls` no longer shows untagged images by default if no `--all` flag is provided. [docker/cli#6574](https://github.com/docker/cli/pull/6574)
* `docker save`: Fixed inconsistent tar member timestamps when exporting images with the overlay2 storage driver. [moby/moby#51365](https://github.com/moby/moby/pull/51365)
* Add a new log option for fluentd log driver (`fluentd-read-timeout`), which enables specifying read timeouts for reading acks from fluentd connections. [moby/moby#50249](https://github.com/moby/moby/pull/50249)
* Add image name completion for `docker images`. [docker/cli#6452](https://github.com/docker/cli/pull/6452)
* Add shell completion for `docker inspect` if a `--type` is set. [docker/cli#6444](https://github.com/docker/cli/pull/6444)
* Add shell completion for `docker plugin` subcommands. [docker/cli#6445](https://github.com/docker/cli/pull/6445)
* api/types/container: make ContainerState, HealthStatus concrete types. [moby/moby#51439](https://github.com/moby/moby/pull/51439)
* containerd image store is temporarily not available when userns remapping is enabled as a workaround for [moby#47377](https://github.com/moby/moby/issues/47377). [moby/moby#51042](https://github.com/moby/moby/pull/51042)
* contrib: remove contrib/httpserver, which was only used for integration tests. [moby/moby#50654](https://github.com/moby/moby/pull/50654)
* daemon: improve validation of the `--dns` option and corresponding `"dns"` field in `daemon.json`. [moby/moby#50600](https://github.com/moby/moby/pull/50600)
* dockerd-rootless.sh: if slirp4netns is not installed, try using pasta (passt). [moby/moby#51149](https://github.com/moby/moby/pull/51149)
* Fix `--mount type=image` failure when mounting the same image multiple times to a different destinations. [moby/moby#50268](https://github.com/moby/moby/pull/50268)
* Fix `docker stats <container>` not exiting gracefully. [docker/cli#6582](https://github.com/docker/cli/pull/6582)
* Fix a bug preventing the API server from shutting down quickly when there's an open connection to the `/events` endpoint. [moby/moby#51448](https://github.com/moby/moby/pull/51448)
* Fix a bug where collecting container stats in "one-shot" mode would not include the container's ID and Name. [moby/moby#51302](https://github.com/moby/moby/pull/51302)
* Fix an issue where all new tasks in the Swarm could get stuck in the PENDING state forever after scaling up a service with placement preferences. [moby/moby#50202](https://github.com/moby/moby/pull/50202)
* Fix issue where custom meta-headers were not passed through when using the containerd image store. [moby/moby#51024](https://github.com/moby/moby/pull/51024)
* Fix requests not being logged when running the daemon with `--log-level=trace`. [moby/moby#50986](https://github.com/moby/moby/pull/50986)
* Fix Swarm services becoming unreachable from published ports after a firewalld reload. [moby/moby#50443](https://github.com/moby/moby/pull/50443)
* Improve errors when failing to connect to the API to provide more context to the user. [moby/moby#50285](https://github.com/moby/moby/pull/50285)
* Improve shell completion for `docker secret` and `docker config` subcommands. [docker/cli#6446](https://github.com/docker/cli/pull/6446)
* Prefer explicit device driver name over GPU capabilities when selecting the device driver with `docker run --gpus`. [moby/moby#50717](https://github.com/moby/moby/pull/50717)
* Update runc to [v1.3.3](https://github.com/opencontainers/runc/releases/tag/v1.3.3). [moby/moby#51393](https://github.com/moby/moby/pull/51393)
* Update SwarmKit internal TLS configuration to exclude known insecure cipher suites. [moby/moby#51139](https://github.com/moby/moby/pull/51139)
* Windows: Fix BuildKit creating containers which isolation mode is inconsistent with the daemon's config. [moby/moby#50942](https://github.com/moby/moby/pull/50942)

### [Packaging updates](#packaging-updates-11)

* client: remove legacy CBC cipher suites from client config. [moby/moby#50126](https://github.com/moby/moby/pull/50126)

* contrib: remove `editorconfig` as it was unmaintained. [moby/moby#50607](https://github.com/moby/moby/pull/50607)

* contrib: remove Dockerfile syntax highlighting files for `nano` and TextMate (`tmbundle`) as they were unmaintained and outdated. [moby/moby#50606](https://github.com/moby/moby/pull/50606)

* contrib: remove mkimage-xxx scripts as they were unmaintained and not tested. [moby/moby#50297](https://github.com/moby/moby/pull/50297)

* If Docker is downgraded to a version that does not have this support the network will become unusable, it must be deleted and re-created. [moby/moby#50114](https://github.com/moby/moby/pull/50114)

* The Windows overlay network driver now supports option `--dns`. [moby/moby#51229](https://github.com/moby/moby/pull/51229)

* Update BuildKit to [v0.25.2](https://github.com/moby/buildkit/releases/tag/v0.25.2). [moby/moby#51397](https://github.com/moby/moby/pull/51397)

* Update containerd to [v2.1.5](https://github.com/containerd/containerd/releases/tag/v2.1.5). [moby/moby#51409](https://github.com/moby/moby/pull/51409)

  containerd v2.1.5 now uses systemd's default `LimitNOFILE` for containers, changing the open file descriptor limit (`ulimit -n`) from `1048576` to `1024`. This extends a change introduced in Docker Engine v25.0 for build containers to all containers.

  This prevents programs that adjust behavior based on ulimits from consuming excessive memory when the limit is set to `infinity`. Containers now behave the same way as programs running on the host.

  If your workload needs a higher limit, use `--ulimit` with `docker run`, or set defaults in `/etc/docker/daemon.json`:

  ```json
  {
    "default-ulimits": {
      "nofile": {
        "Name": "nofile",
        "Soft": 1048576,
        "Hard": 1048576
      }
    }
  }
  ```

  For more information, see [moby#51485](https://github.com/moby/moby/issues/51485).

* Update Go runtime to [1.25.4](https://go.dev/doc/devel/release#go1.25.4). [moby/moby#51418](https://github.com/moby/moby/pull/51418), [docker/cli#6632](https://github.com/docker/cli/pull/6632)

* Users can request a specific prefix size for networks allocated from the default pools by using the unspecified address, for example `--subnet 0.0.0.0/24 --subnet ::/96`. [moby/moby#50114](https://github.com/moby/moby/pull/50114)

### [Networking](#networking-14)

* Add daemon option `--bridge-accept-fwmark`. Packets with this firewall mark will accepted by bridge networks, overriding Docker's iptables or nftables "drop" rules. [moby/moby#50476](https://github.com/moby/moby/pull/50476)

* api/types/system: deprecated top level `DiskUsage` fields for type specific fields. [moby/moby#51235](https://github.com/moby/moby/pull/51235)

* Ensure bridge devices are removed when bridge network creation fails. [moby/moby#51147](https://github.com/moby/moby/pull/51147)

* Ensure that Windows NAT networks are recreated with their original labels when the Engine restarts. [moby/moby#50447](https://github.com/moby/moby/pull/50447)

* Environment variables set on a container using legacy links are deprecated and aren't added automatically anymore. [moby/moby#50719](https://github.com/moby/moby/pull/50719)

  * The daemon can be started with `DOCKER_KEEP_DEPRECATED_LEGACY_LINKS_ENV_VARS=1` to get them back
  * Users are encouraged to stop relying on these as they're deprecated, and the escape hatch will be removed in a later version

* Fix a bug in NetworkDB which would sometimes cause entries to get stuck deleted on some of the nodes, leading to connectivity issues between containers on overlay networks. [moby/moby#50342](https://github.com/moby/moby/pull/50342)

* Fix a bug that could cause the Engine and another host process to bind the same UDP port. [moby/moby#50669](https://github.com/moby/moby/pull/50669)

* Fix a deadlock that could happen if a firewalld reload was processed while the bridge networking driver was starting up, or creating or deleting a network, or creating port-mappings. [moby/moby#50620](https://github.com/moby/moby/pull/50620)

* Fix an issue preventing container startup or selection of its network gateway when IPv6 is only disabled on a specific interface. [moby/moby#48971](https://github.com/moby/moby/pull/48971)

* For Linux, `docker info` now reports the firewall backend if available. [docker/cli#6191](https://github.com/docker/cli/pull/6191)

* Greatly improve the reliability of overlay networking and the Swarm routing mesh. [moby/moby#50393](https://github.com/moby/moby/pull/50393)

* Improve the convergence rate of NetworkDB, part of the management plane for overlay networking, after bursts of updates. [moby/moby#50193](https://github.com/moby/moby/pull/50193)

* Improve the reliability of the overlay network driver. [moby/moby#50260](https://github.com/moby/moby/pull/50260)

* Improved error handling for connection of a container to a network. [moby/moby#50945](https://github.com/moby/moby/pull/50945)

* macvlan and IPvlan-l2 networks: no default gateway will be configured unless a `--gateway` is explicitly included in IPAM configuration. This addresses an issue which could cause container startup to fail in networks with IPv6 auto-configuration enabled. [moby/moby#50929](https://github.com/moby/moby/pull/50929)

* nftables: Docker will not enable IP forwarding on the host. If forwarding is needed by a bridge network, but not enabled, daemon startup or network creation will fail with an error. You must either enable forwarding and ensure firewall rules are in place to prevent unwanted forwarding between non-Docker interfaces. Or, use daemon option `--ip-forward=false` to disable the check, but some bridge network functionality including port forwarding may not work. See [Engine Docs](https://docs.docker.com/engine/network/firewall-nftables) for more information about migration from iptables to nftables. [moby/moby#50646](https://github.com/moby/moby/pull/50646)

* On daemon startup, restart containers that share their network stacks before containers that need those stacks. [moby/moby#50327](https://github.com/moby/moby/pull/50327)

* Published ports are now always accessible in networks with gateway mode "routed". Previously, rules to open those ports were only added when the routed mode network was selected as the container's default gateway. [moby/moby#50140](https://github.com/moby/moby/pull/50140)

* Since 28.0.0, an `iptables` mangle rule for checksumming SCTP was only added if environment variable `DOCKER_IPTABLES_SCTP_CHECKSUM=1` was set. The rule has now been removed, the environment variable now has no effect. [moby/moby#50539](https://github.com/moby/moby/pull/50539)

* The iptables rules for bridge networks have been updated, including removal of the `DOCKER-ISOLATION-STAGE-1` and `DOCKER-ISOLATION-STAGE-2` chains. With these changes:. [moby/moby#49981](https://github.com/moby/moby/pull/49981)

  * Containers can now access ports published to host addresses by containers in other networks when the userland-proxy is not running
  * Containers can now access ports on container addresses in other networks that have gateway mode "nat-unprotected"

* When dynamically linked, the Docker daemon now depends on libnftables. [moby/moby#51033](https://github.com/moby/moby/pull/51033)

* Windows: `network inspect`: the HNS network name is now reported in option `com.docker.network.windowsshim.networkname` rather than the Docker network name, which was only reported after a daemon restart. [moby/moby#50961](https://github.com/moby/moby/pull/50961)

* Windows: when restoring networks on daemon restart, preserve their association with non-default IPAM drivers. [moby/moby#50649](https://github.com/moby/moby/pull/50649)

### [API](#api-2)

* `events` API now reports content-type as `application/x-ndjson` for newline-delimited JSON event stream. [moby/moby#50953](https://github.com/moby/moby/pull/50953)

* `GET /images/{name}/get` and `POST /images/load` now accept multiple `platform` query parameters, allowing export and load of images for multiple platforms. [moby/moby#50166](https://github.com/moby/moby/pull/50166)

* `GET /images/{name}/json` now omits the following fields if their value is empty: `Parent`, `Comment`, `DockerVersion`, `Author`. [moby/moby#51072](https://github.com/moby/moby/pull/51072)

* `GET /images/{name}/json`: omit empty `Config` fields when not set. [moby/moby#50915](https://github.com/moby/moby/pull/50915)

* `POST /images/{name:}/push`: remove compatibility with API v1.4 auth-config in body. [moby/moby#50371](https://github.com/moby/moby/pull/50371)

* Add support for memory swappiness in Swarm services. [moby/moby#51114](https://github.com/moby/moby/pull/51114)

  * `GET /services` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements
  * `GET /services/{id}` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements
  * `POST /services/create` now accepts `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements
  * `POST /services/{id}/update` now accepts `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements
  * `GET /tasks` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements
  * `GET /tasks/{id}` now returns `SwapBytes` and `MemorySwappiness` fields as part of the `Resource` requirements

* api/types/build: move `CachePruneOptions` type to `client.BuildCachePruneOptions`. [moby/moby#50772](https://github.com/moby/moby/pull/50772)

* api/types/checkpoint: move checkpoint options to client module. [moby/moby#50905](https://github.com/moby/moby/pull/50905)

* api/types/container: `OnBuild` will now be omitted if its value is empty or zero. [moby/moby#51154](https://github.com/moby/moby/pull/51154)

* api/types/container: make the container config `MacAddress` obsolete for v1.52 and onwards. Use network endpoint settings instead. [moby/moby#51189](https://github.com/moby/moby/pull/51189)

* api/types/container: move `ResizeOptions` type to `ContainerResizeOptions` in the client. [moby/moby#50773](https://github.com/moby/moby/pull/50773)

* api/types/events: move `ListOptions` type to the client `EventsListOptions`. [moby/moby#50774](https://github.com/moby/moby/pull/50774)

* api/types/image: move image options out to the client. [moby/moby#50776](https://github.com/moby/moby/pull/50776)

* api/types/network: move `CreateOptions`, `ConnectOptions` and `DisconnectOptions` to the client module. [moby/moby#50817](https://github.com/moby/moby/pull/50817)

* api/types/network: move the `ListOptions` and `InspectOptions` types to the client. [moby/moby#50786](https://github.com/moby/moby/pull/50786)

* api/types/plugin: change `ListResponse` to a non-pointer slice. [moby/moby#51440](https://github.com/moby/moby/pull/51440)

* api/types/plugin: remove deprecated `Config.DockerVersion`. [moby/moby#51458](https://github.com/moby/moby/pull/51458)

* api/types/registry: move `SearchOptions` to `ImageSearchOptions` in the client. [moby/moby#50787](https://github.com/moby/moby/pull/50787)

* api/types/registry: moved `ServiceConfig` legacy field marshaling support into daemon backend. [moby/moby#50826](https://github.com/moby/moby/pull/50826)

* api/types/registry: moved encode/decode auth config functions into reference utility package. [moby/moby#50785](https://github.com/moby/moby/pull/50785)

* api/types/storage: add `Storage` type and integrate in container inspect. [moby/moby#50857](https://github.com/moby/moby/pull/50857)

* api/types/swarm: deprecated and dropped support for `PortConfigProtocol`; use `network.IPProtocol` instead. [moby/moby#51094](https://github.com/moby/moby/pull/51094)

* api/types/swarm: move option types to the client module. [moby/moby#50794](https://github.com/moby/moby/pull/50794)

* api/types/swarm: move the `SecretListOptions` type to the client module. [moby/moby#50816](https://github.com/moby/moby/pull/50816)

* api/types/system: move `DiskUsageOptions` to the client. [moby/moby#50788](https://github.com/moby/moby/pull/50788)

* api/types/system: move `SecurityOpt` and `DecodeSecurityOptions` to client module. [moby/moby#50825](https://github.com/moby/moby/pull/50825)

* api/types/volume: change ListResponse.Volumes to a non-pointer slice. [moby/moby#51454](https://github.com/moby/moby/pull/51454)

* api/types/volume: move the `ListOptions` type to the client module. [moby/moby#50789](https://github.com/moby/moby/pull/50789)

* api/types/volume: moved `UpdateOptions` into client module. [moby/moby#51205](https://github.com/moby/moby/pull/51205)

* api/types: daemon: move the disk usage structs to the backend server. [moby/moby#50764](https://github.com/moby/moby/pull/50764)

* api: make `GraphDriver` field in `image.InspectResponse` optional. This field will continue to be emitted when using the legacy graph drivers and will be omitted when using the containerd image backend. [moby/moby#50893](https://github.com/moby/moby/pull/50893)

* api: redefine container network port types. [moby/moby#50710](https://github.com/moby/moby/pull/50710)

* client: PluginListResult: change Items field to a non-pointer slice. [moby/moby#51440](https://github.com/moby/moby/pull/51440)

* Inspecting networks with API v1.52 and newer provides statistics about IPAM allocations for the subnets assigned to the network. [moby/moby#50917](https://github.com/moby/moby/pull/50917)

* MAC address fields are represented as byte slices compatible with the standard library net.HardwareAddr type instead of strings. [moby/moby#51355](https://github.com/moby/moby/pull/51355)

* Swagger definitions for `NetworkSummary` and `NetworkInspect` have been added to the Swagger spec describing the Engine API. [moby/moby#50855](https://github.com/moby/moby/pull/50855)

* Update API version to 1.52. [moby/moby#50418](https://github.com/moby/moby/pull/50418)

### [Go SDK](#go-sdk-4)

* `api/pkg/progress` and `api/pkg/streamformatter` have been removed. [moby/moby#51153](https://github.com/moby/moby/pull/51153)
* `api/types/registry`: `EncodeAuthConfig`: use empty string for zero value. [moby/moby#50426](https://github.com/moby/moby/pull/50426)
* `api/types/versions` has moved to the client and daemon. [moby/moby#51284](https://github.com/moby/moby/pull/51284)
* `client.ConfigCreate`, `client.ConfigList`, `client.ConfigInspectWithRaw`, `client.ConfigUpdate`, and `client.ConfigRemove` methods now accept option structs instead of positional arguments, and return dedicated result structs. [moby/moby#51078](https://github.com/moby/moby/pull/51078)
* `client.ImageBuild`, `client.BuildCancel`, `client.ImageList`, `client.ImageRemove`, `client.ImageTag`, and `client.ImageSearch` methods now accept option structs instead of positional arguments, and return dedicated result structs. [moby/moby#51227](https://github.com/moby/moby/pull/51227)
* `client`: `ContainerExec...` methods were renamed to `Exec...`. [moby/moby#51262](https://github.com/moby/moby/pull/51262)
* `client`: Wrap return values of `ImageInspect`, `ImageHistory`, `ImageLoad` and `ImageSave` in a struct. [moby/moby#51236](https://github.com/moby/moby/pull/51236)
* `ImagePull` now returns an object with `JSONMessages` method returning iterator over the message objects. [moby/moby#50935](https://github.com/moby/moby/pull/50935)
* `ImagePush` now returns an object with `JSONMessages` method returning iterator over the message objects. [moby/moby#51148](https://github.com/moby/moby/pull/51148)
* api/types/container: move `StatsResponseReader` to `client` package. [moby/moby#50521](https://github.com/moby/moby/pull/50521)
* api/types/container: move container options to client. [moby/moby#50897](https://github.com/moby/moby/pull/50897)
* api/types/container: rename `Port` to `PortSummary`. [moby/moby#50711](https://github.com/moby/moby/pull/50711)
* api/types/container: StatsResponse: add `OSType` field. [moby/moby#51305](https://github.com/moby/moby/pull/51305)
* api/types: move `ErrorResponse` to `common/ErrorResponse`. [moby/moby#50632](https://github.com/moby/moby/pull/50632)
* api: remove unused `DefaultVersion`, `MinSupportedAPIVersion` consts. [moby/moby#50587](https://github.com/moby/moby/pull/50587)
* cli/command: add `WithUserAgent` option. [docker/cli#4574](https://github.com/docker/cli/pull/4574)
* client: `ContainerCommitOptions`: remove `Pause` field in favor of `NoPause`. [moby/moby#51019](https://github.com/moby/moby/pull/51019)
* client: add `DefaultAPIVersion` const, which defines the default (and maximum) API version supported by the client. [moby/moby#50433](https://github.com/moby/moby/pull/50433)
* client: add `ExecAPIClient` interface for exec methods provided by the client. [moby/moby#50997](https://github.com/moby/moby/pull/50997)
* client: Client.PluginList: add options-struct. [moby/moby#51207](https://github.com/moby/moby/pull/51207)
* client: ContainersPrune: rewrite to use option structs and result. [moby/moby#51200](https://github.com/moby/moby/pull/51200)
* client: ImagesPrune: rewrite to use option structs and result. [moby/moby#51200](https://github.com/moby/moby/pull/51200)
* client: NetworksPrune: rewrite to use option structs and result. [moby/moby#51200](https://github.com/moby/moby/pull/51200)
* client: remove `client.ContainerStatsResult.OSType` field. [moby/moby#51305](https://github.com/moby/moby/pull/51305)
* client: VolumesPrune: rewrite to use option structs and result. [moby/moby#51200](https://github.com/moby/moby/pull/51200)
* daemon/config: add `DefaultAPIVersion` const, which defines the default (and maximum) API version supported by the daemon. [moby/moby#50436](https://github.com/moby/moby/pull/50436)
* Fix data race in `ContainerExecStart`, `ContainerList`, and `Events`. [moby/moby#50448](https://github.com/moby/moby/pull/50448)
* IP addresses and subnets are now of type `netip.Addr` and `netip.Prefix`, respectively. [moby/moby#50956](https://github.com/moby/moby/pull/50956)
* Remove structs `NetworkSettingsBase` and `DefaultNetworkSettings`. Fields in `NetworkSettingsBase` that were not deprecated are now directly in `NetworkSettings`. [moby/moby#50846](https://github.com/moby/moby/pull/50846)
* the client now uses its own `client.Filters` type for filtering API requests, with a more ergonomic interface. Users of the `github.com/docker/docker/api/types/filters` package will need to refactor when they upgrade to the v29 client. [moby/moby#51115](https://github.com/moby/moby/pull/51115)
* Types `"github.com/moby/moby/api/types/network".Summary` and `"github.com/moby/moby/api/types/network".Inspect` are no longer aliases, and most of their fields have been moved into an embedded struct. Engine API clients may require some source-level changes when migrating to the new github.com/moby/moby/api module. [moby/moby#50878](https://github.com/moby/moby/pull/50878)
* Update minimum Go version to 1.24. [docker/cli#6624](https://github.com/docker/cli/pull/6624)

### [Deprecations](#deprecations-3)

* `client/pkg/jsonmessage`: remove deprecated `ProgressMessage`, `ErrorMessage`, `DisplayJSONMessagesToStream` and `Stream` interface. [moby/moby#49264](https://github.com/moby/moby/pull/49264)
* `GET /events` no longer includes the deprecated `status`, `id`, and `from` fields. These fields were removed in API v1.22, but still included in the response. These fields are now omitted when using API v1.52 or later. [moby/moby#50832](https://github.com/moby/moby/pull/50832)
* api/types/network: CreateRequest: remove deprecated CheckDuplicate field. [moby/moby#50998](https://github.com/moby/moby/pull/50998)
* api/types/plugin: deprecate `Config.DockerVersion` field. [moby/moby#51109](https://github.com/moby/moby/pull/51109)
* api/types/registry: remove deprecated AuthConfig.Email field. [moby/moby#51059](https://github.com/moby/moby/pull/51059)
* api/types/strslice: deprecate StrSlice in favor of using a regular `[]string`. [moby/moby#50292](https://github.com/moby/moby/pull/50292)
* api/types/system: remove deprecated `DiskUsage.BuilderSize`. [moby/moby#51180](https://github.com/moby/moby/pull/51180)
* api/types: move plugin types to api/types/plugin. [moby/moby#48114](https://github.com/moby/moby/pull/48114)
* API: Deprecation: the Engine was automatically backfilling empty `PortBindings` lists with a PortBinding with an empty HostIP and HostPort when starting a container. This behavior is deprecated for API 1.52, and will be dropped in API 1.53. [moby/moby#50874](https://github.com/moby/moby/pull/50874)
* build: remove DCT support for classic builder. [docker/cli#6195](https://github.com/docker/cli/pull/6195)
* cli/command: Remove deprecated `ResolveDefaultContext`. [docker/cli#6555](https://github.com/docker/cli/pull/6555)
* client: ImageBuildResponse: remove OSType field. [moby/moby#50995](https://github.com/moby/moby/pull/50995)
* client: Remove `ImageCreate` method - use`ImagePull` or `ImageImport` instead. [moby/moby#51366](https://github.com/moby/moby/pull/51366)
* client: remove deprecated `ImageListOptions.ContainerCount`. [moby/moby#51006](https://github.com/moby/moby/pull/51006)
* client: remove support for negotiating API version < v1.44 (docker 25.0). [moby/moby#51119](https://github.com/moby/moby/pull/51119)
* client: remove unused `Client.HTTPClient()` method. [moby/moby#51011](https://github.com/moby/moby/pull/51011)
* daemon/graphdriver: remove deprecated `GetDriver()`. [moby/moby#50377](https://github.com/moby/moby/pull/50377)
* daemon: raise minimum API version to v1.44. [moby/moby#51186](https://github.com/moby/moby/pull/51186)
* Deprecate the `--pause` flag on `docker commit` in favor of `--no-pause`. [docker/cli#6460](https://github.com/docker/cli/pull/6460)
* Deprecate cgroup v1. [moby/moby#51360](https://github.com/moby/moby/pull/51360), [docker/cli#6598](https://github.com/docker/cli/pull/6598)
* Go SDK: `cli-plugins/manager`: deprecate metadata aliases in favor of their equivalent in `cli-plugins/manager/metadata`. [docker/cli#6237](https://github.com/docker/cli/pull/6237)
* Go SDK: `cli-plugins/manager`: remove `Candidate` interface, which was only for internal use. [docker/cli#6237](https://github.com/docker/cli/pull/6237)
* Go SDK: `cli-plugins/manager`: remove `NewPluginError` function, which was only for internal use. [docker/cli#6237](https://github.com/docker/cli/pull/6237)
* Go SDK: `cli-plugins/manager`: remove deprecated `ResourceAttributesEnvvar` const. [docker/cli#6237](https://github.com/docker/cli/pull/6237)
* Go SDK: `cli/command`: remove the `ErrPromptTerminated`, `DisableInputEcho`, `PromptForInput`, and `PromptForConfirmation` utilities. These utilities were for internal use and are no longer used. [docker/cli#6243](https://github.com/docker/cli/pull/6243)
* Go SDK: `cli/registry/client`: remove deprecated `RepoNameForReference`. [docker/cli#6206](https://github.com/docker/cli/pull/6206)
* Go SDK: api/types/build: remove deprecated BuildCache.Parent field. [moby/moby#51185](https://github.com/moby/moby/pull/51185)
* Go SDK: api/types/container: remove deprecated `ContainerTopOKBody` alias. [moby/moby#50400](https://github.com/moby/moby/pull/50400)
* Go SDK: api/types/container: remove deprecated `ContainerUpdateOKBody` alias. [moby/moby#50400](https://github.com/moby/moby/pull/50400)
* Go SDK: api/types/container: remove deprecated `Stats` type. [moby/moby#50492](https://github.com/moby/moby/pull/50492)
* Go SDK: api/types/filters: remove deprecated `ToParamWithVersion`. [moby/moby#50561](https://github.com/moby/moby/pull/50561)
* Go SDK: api/types/image: `InspectResponse`: remove deprecated `VirtualSize`, `Container`, `ContainerConfig`, `Parent`, and `DockerVersion` fields. [moby/moby#51103](https://github.com/moby/moby/pull/51103)
* Go SDK: api/types/image: remove deprecated Summary.VirtualSize field. [moby/moby#51190](https://github.com/moby/moby/pull/51190)
* Go SDK: api/types/registry: remove deprecated `ServiceConfig.AllowNondistributableArtifactsCIDRs` and `ServiceConfig.AllowNondistributableArtifactsHostnames` fields. [moby/moby#50375](https://github.com/moby/moby/pull/50375)
* Go SDK: api/types/swarm: remove deprecated ServiceSpec.Networks field. [moby/moby#51184](https://github.com/moby/moby/pull/51184)
* GO SDK: api/types/system: remove deprecated `Commit.Expected` field. [moby/moby#51127](https://github.com/moby/moby/pull/51127)
* Go SDK: api/types: remove deprecated aliases. [moby/moby#50452](https://github.com/moby/moby/pull/50452)
* Go SDK: api: deprecate `NoBaseImageSpecifier` const. This const is no longer used and will be removed in the next release. [moby/moby#50437](https://github.com/moby/moby/pull/50437)
* Go SDK: api: remove `NoBaseImageSpecifier`. [moby/moby#50574](https://github.com/moby/moby/pull/50574)
* Go SDK: cli/command/builder: remove `CachePrune()`, which was no longer used. [docker/cli#6236](https://github.com/docker/cli/pull/6236)
* Go SDK: cli/command/builder: remove `NewBuilderCommand` and `NewBakeStubCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/checkpoint: remove `NewCheckpointCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/checkpoint: remove deprecated `NewFormat`, `FormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/completion: remove deprecated `NoComplete`. [docker/cli#6408](https://github.com/docker/cli/pull/6408)
* Go SDK: cli/command/config: remove `NewConfigCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/config: remove deprecated `NewFormat`, `FormatWrite`, `InspectFormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/config: remove deprecated `RunConfigCreate`, `CreateOptions`, `RunConfigInspect`, `InspectOptions`, `RunConfigList`, `ListOptions`, `RunConfigRemove`, and `RemoveOptions`. [docker/cli#6370](https://github.com/docker/cli/pull/6370)
* Go SDK: cli/command/container: deprecate `NewDiffFormat`, `DiffFormatWrite`. These functions were only used internally and will be removed in the next release. [docker/cli#6187](https://github.com/docker/cli/pull/6187)
* Go SDK: cli/command/container: remove `NewBuildCommand`, `NewPullCommand`, `NewPushCommand`, `NewImagesCommand`, `NewImageCommand`, `NewHistoryCommand`, `NewImportCommand`, `NewLoadCommand`, `NewRemoveCommand`, `NewSaveCommand`, `NewTagCommand`, `NewPruneCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/container: remove `NewRunCommand`, `NewExecCommand`, `NewPsCommand`, `NewContainerCommand`, `NewAttachCommand`, `NewCommitCommand`, `NewCopyCommand`, `NewCreateCommand`, `NewDiffCommand`, `NewExportCommand`, `NewKillCommand`, `NewLogsCommand`, `NewPauseCommand`, `NewPortCommand`, `NewRenameCommand`, `NewRestartCommand`, `NewRmCommand`, `NewStartCommand`, `NewStatsCommand`, `NewStopCommand`, `NewTopCommand`, `NewUnpauseCommand`, `NewUpdateCommand`, `NewWaitCommand`, `NewPruneCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/container: remove `RunPrune()`, which was no longer used. [docker/cli#6236](https://github.com/docker/cli/pull/6236)
* Go SDK: cli/command/container: remove deprecated `NewDiffFormat`, `DiffFormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/context: remove `NewContextCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/context: remove deprecated `RunCreate` and `CreateOptions`. [docker/cli#6407](https://github.com/docker/cli/pull/6407)
* Go SDK: cli/command/context: remove deprecated `RunExport` and `ExportOptions`. [docker/cli#6407](https://github.com/docker/cli/pull/6407)
* Go SDK: cli/command/context: remove deprecated `RunImport`. [docker/cli#6407](https://github.com/docker/cli/pull/6407)
* Go SDK: cli/command/context: remove deprecated `RunRemove` and `RemoveOptions`. [docker/cli#6407](https://github.com/docker/cli/pull/6407)
* Go SDK: cli/command/context: remove deprecated `RunUpdate` and `UpdateOptions`. [docker/cli#6407](https://github.com/docker/cli/pull/6407)
* Go SDK: cli/command/context: remove deprecated `RunUse`. [docker/cli#6407](https://github.com/docker/cli/pull/6407)
* Go SDK: cli/command/formatter/swarm: remove deprecated `GetStacks` function. [docker/cli#6406](https://github.com/docker/cli/pull/6406)
* Go SDK: cli/command/image/build: deprecate `DefaultDockerfileName`, `DetectArchiveReader`, `WriteTempDockerfile`, `ResolveAndValidateContextPath`. These utilities were only used internally and will be removed in the next release. [docker/cli#6561](https://github.com/docker/cli/pull/6561)
* Go SDK: cli/command/image: remove `RunPrune()`, which was no longer used. [docker/cli#6236](https://github.com/docker/cli/pull/6236)
* Go SDK: cli/command/image: remove deprecated `AuthResolver` utility. [docker/cli#6373](https://github.com/docker/cli/pull/6373)
* Go SDK: cli/command/image: remove deprecated `NewHistoryFormat`, `HistoryWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339), [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/manifest: remove `NewManifestCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/network: remove `NewNetworkCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/network: remove `RunPrune()`, which was no longer used. [docker/cli#6236](https://github.com/docker/cli/pull/6236)
* Go SDK: cli/command/network: remove deprecated `NewFormat`, `FormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/node: remove `NewNodeCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/node: remove deprecated `NewFormat`, `FormatWrite`, `InspectFormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/plugin: remove `NewPluginCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/plugin: remove deprecated `NewFormat`, `FormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/registry: remove `NewLoginCommand`, `NewLogoutCommand`, `NewSearchCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/registry: remove deprecated `NewSearchFormat`, `SearchWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/registry: remove deprecated `OauthLoginEscapeHatchEnvVar` const. [docker/cli#6463](https://github.com/docker/cli/pull/6463)
* Go SDK: cli/command/secret: remove `NewSecretCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/secret: remove deprecated `NewFormat`, `FormatWrite`, `InspectFormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/service: remove `NewServiceCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/service: remove deprecated `NewFormat`, `InspectFormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/stack/swarm: remove deprecated RunPS and options.PS. [docker/cli#6398](https://github.com/docker/cli/pull/6398)
* Go SDK: cli/command/stack: remove `NewStackCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/stack: remove deprecated RunList and options.List. [docker/cli#6398](https://github.com/docker/cli/pull/6398)
* Go SDK: cli/command/stack: remove deprecated RunServices and swarm.GetServices. [docker/cli#6398](https://github.com/docker/cli/pull/6398)
* Go SDK: cli/command/swarm: remove `NewSwarmCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/system: remove `NewVersionCommand`, `NewInfoCommand`, `NewSystemCommand`, `NewEventsCommand`, `NewInspectCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/task: remove deprecated `NewTaskFormat`, `FormatWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/trust: remove `NewTrustCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/trust: remove deprecated `NewPruneCommand`. [docker/cli#6344](https://github.com/docker/cli/pull/6344)
* Go SDK: cli/command/trust: remove deprecated `SignedTagInfo`, `SignerInfo`, `NewTrustTagFormat`, `NewSignerInfoFormat`, `TagWrite`, `SignerInfoWrite`. [docker/cli#6339](https://github.com/docker/cli/pull/6339)
* Go SDK: cli/command/volume: remove `NewVolumeCommand`, `NewPruneCommand`. [docker/cli#6335](https://github.com/docker/cli/pull/6335)
* Go SDK: cli/command/volume: remove `RunPrune()`, which was no longer used. [docker/cli#6236](https://github.com/docker/cli/pull/6236)
* Go SDK: cli/command: remove `AddTrustSigningFlags`, `AddTrustVerificationFlags`, and `AddPlatformFlag` utilities, which were only used internally. [docker/cli#6244](https://github.com/docker/cli/pull/6244)
* Go SDK: cli/command: remove deprecated `DockerCli.Apply`. [docker/cli#6503](https://github.com/docker/cli/pull/6503)
* Go SDK: cli/command: remove deprecated `DockerCli.ContentTrustEnabled`. [docker/cli#6502](https://github.com/docker/cli/pull/6502)
* Go SDK: cli/command: remove deprecated `DockerCli.DefaultVersion`. [docker/cli#6502](https://github.com/docker/cli/pull/6502)
* Go SDK: cli/command: remove deprecated `RegistryAuthenticationPrivilegedFunc`. [docker/cli#6349](https://github.com/docker/cli/pull/6349)
* Go SDK: cli/command: remove deprecated `WithContentTrustFromEnv`, `WithContentTrust` options. [docker/cli#6502](https://github.com/docker/cli/pull/6502)
* Go SDK: cli/config/configfile: remove deprecated `ConfigFile.Experimental` field. [docker/cli#6464](https://github.com/docker/cli/pull/6464)
* Go SDK: cli/config/types: remove deprecated `AuthConfig.Email` field. [docker/cli#6515](https://github.com/docker/cli/pull/6515)
* Go SDK: cli/manifest/store: remove deprecated `IsNotFound`. [docker/cli#6523](https://github.com/docker/cli/pull/6523)
* Go SDK: cli: remove deprecated `VisitAll`, `DisableFlagsInUseLine` utilities. [docker/cli#6296](https://github.com/docker/cli/pull/6296)
* Go SDK: client: remove `APIClient.ImageInspectWithRaw` from the `APIClient` interface. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove `ImageAPIClient.ImageInspectWithRaw` from the `ImageAPIClient` interface. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove `ImageAPIClientDeprecated.ImageInspectWithRaw` from the `ImageAPIClientDeprecated`. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove deprecated `ErrorConnectionFailed` and `IsErrNotFound` functions. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove deprecated `NewClient` and `NewEnvClient` functions. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove the `CommonAPIClient` interface. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove the `ImageAPIClientDeprecated` interface. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: client: remove the deprecated `Client.ImageInspectWithRaw` method. [moby/moby#50485](https://github.com/moby/moby/pull/50485)
* Go SDK: container: remove deprecated `IsValidHealthString`. [moby/moby#50378](https://github.com/moby/moby/pull/50378)
* Go SDK: container: remove deprecated `IsValidStateString`. [moby/moby#50378](https://github.com/moby/moby/pull/50378)
* Go SDK: container: remove deprecated `StateStatus`, `WaitCondition`, and the related `WaitConditionNotRunning`, `WaitConditionNextExit`, and `WaitConditionRemoved` consts. [moby/moby#50378](https://github.com/moby/moby/pull/50378)
* Go SDK: deprecate `pkg/stdcopy`, which was moved to `api/pkg/stdcopy`. [moby/moby#50462](https://github.com/moby/moby/pull/50462)
* Go SDK: Deprecate field `NetworkSettingsBase.Bridge`, struct `NetworkSettingsBase`, all the fields of `DefaultNetworkSettings`, and struct `DefaultNetworkSettings`. [moby/moby#50848](https://github.com/moby/moby/pull/50848)
* Go SDK: deprecate pkg/stringid in favour of `github.com/moby/moby/client/pkg/stringid`. [moby/moby#50504](https://github.com/moby/moby/pull/50504)
* Go SDK: deprecate profiles package which got migrated to `github.com/moby/profiles`. [moby/moby#50481](https://github.com/moby/moby/pull/50481)
* Go SDK: oci: deprecate SetCapabilities, and some minor cleanups/fixes. [moby/moby#50461](https://github.com/moby/moby/pull/50461)
* Go SDK: opts: remove deprecated `ListOpts.GetAll`. It's no longer used and replaced by `ListOpts.GetSlice`. [docker/cli#6293](https://github.com/docker/cli/pull/6293)
* Go SDK: opts: remove deprecated `NewNamedListOptsRef`, `NewNamedMapOpts`, `NamedListOpts`, `NamedMapOpts`, and `NamedOption`. These types and functions are no longer used and will be removed in the next release. [docker/cli#6293](https://github.com/docker/cli/pull/6293)
* Go SDK: opts: remove deprecated `ParseEnvFile` in favour of `kvfile.Parse`. [docker/cli#6382](https://github.com/docker/cli/pull/6382)
* Go SDK: opts: remove deprecated `QuotedString`. [docker/cli#6293](https://github.com/docker/cli/pull/6293)
* Go SDK: opts: remove deprecated `ValidateHost`. [docker/cli#6293](https://github.com/docker/cli/pull/6293)
* Go SDK: pkg/system was removed, and is now an internal package. [moby/moby#50559](https://github.com/moby/moby/pull/50559)
* Go SDK: pkg/system: deprecate `EscapeArgs()` and `IsAbs`. These functions were only used internally and will be removed in the next release. [moby/moby#50399](https://github.com/moby/moby/pull/50399)
* Go SDK: registry: remove deprecated `APIEndpoint.TrimHostName`, `APIEndpoint.Official`, and `APIEndpoint.AllowNondistributableArtifacts` fields. [moby/moby#50376](https://github.com/moby/moby/pull/50376)
* Go SDK: registry: remove deprecated `HostCertsDir()` and `SetCertsDir()` functions. [moby/moby#50373](https://github.com/moby/moby/pull/50373)
* Go SDK: registry: remove deprecated `RepositoryInfo.Official` and `RepositoryInfo.Class` field. [moby/moby#50498](https://github.com/moby/moby/pull/50498)
* Go SDK: registry: remove deprecated `Service.ResolveRepository()`. [moby/moby#50374](https://github.com/moby/moby/pull/50374)
* Go SDK: Remove `buildkit.ClientOpts`. [moby/moby#50318](https://github.com/moby/moby/pull/50318)
* Go SDK: remove `pkg/fileutils`. [moby/moby#50558](https://github.com/moby/moby/pull/50558)
* Go SDK: Remove deprecated `IsNotFound`, `CommandAnnotationPlugin`, `CommandAnnotationPluginVendor`, `CommandAnnotationPluginVersion`, `CommandAnnotationPluginInvalid`, `CommandAnnotationPluginCommandPath`, `NamePrefix`, `MetadataSubcommandName`, `HookSubcommandName`, `Metadata`, and `ReexecEnvvar` from `cli-plugins/manager` in favor of their `cli-plugins/manager/metadata` equivalents. [docker/cli#6414](https://github.com/docker/cli/pull/6414)
* Go SDK: remove deprecated `types/plugins/logdriver` and `types/swarm/runtime` packages; plugin-runtime spec is now exposed as `types/swarm.RuntimeSpec` and `types/swarm.RuntimePrivilege`. [moby/moby#50554](https://github.com/moby/moby/pull/50554)
* Go SDK: remove deprecated `cli/command/formatter` package. [docker/cli#6406](https://github.com/docker/cli/pull/6406)
* Go SDK: remove deprecated `cli/registry/client` package. [docker/cli#6462](https://github.com/docker/cli/pull/6462)
* Go SDK: remove deprecated `pkg/idtools` package. [moby/moby#50456](https://github.com/moby/moby/pull/50456)
* Go SDK: templates: remove deprecated `NewParse` function. [docker/cli#6453](https://github.com/docker/cli/pull/6453)
* Hide the `--kernel-memory` option on `docker run` and `docker create`, and produce a warning when used as it's no longer supported by the daemon and kernel. [docker/cli#6455](https://github.com/docker/cli/pull/6455)
* Remove `VirtualSize` field from `docker image ls` output when using JSON format. [docker/cli#6524](https://github.com/docker/cli/pull/6524)
* Remove `VirtualSize` formatting options and output. [docker/cli#6524](https://github.com/docker/cli/pull/6524)
* Remove API version compatibility for API version < v1.44 (Docker v24.0 and older). [docker/cli#6551](https://github.com/docker/cli/pull/6551)
* Remove deprecated `bind-nonrecursive` option for `--mount`. [docker/cli#6241](https://github.com/docker/cli/pull/6241)
* Remove deprecated packages (`pkg/archive`, `pkg/chrootarchive`, `pkg/atomicwriter`, `pkg/reexec`, `pkg/platform`, `pkg/parsers`), `pkg/system.MkdirAll`. For replacements, see `github.com/moby/go-archive`, `github.com/moby/sys` and the standard library. [moby/moby#50208](https://github.com/moby/moby/pull/50208)
* Remove special handling for quoted values for the `--tlscacert`, `--tlscert`, and `--tlskey` command-line flags. [docker/cli#6306](https://github.com/docker/cli/pull/6306)
* Remove support for AutoRemove (`--rm`) on API < 1.30. [docker/cli#6525](https://github.com/docker/cli/pull/6525)
* Remove support for loading legacy (pre-Docker 1.10) images. [moby/moby#50324](https://github.com/moby/moby/pull/50324)

----
url: https://docs.docker.com/compose/how-tos/use-secrets/
----

# Manage secrets securely in Docker Compose

***

Table of contents

***

A secret is any piece of data, such as a password, certificate, or API key, that shouldn’t be transmitted over a network or stored unencrypted in a Dockerfile or in your application’s source code.

Docker Compose provides a way for you to use secrets without having to use environment variables to store information. If you’re injecting passwords and API keys as environment variables, you risk unintentional information exposure. Services can only access secrets when explicitly granted by a `secrets` attribute within the `services` top-level element.

Environment variables are often available to all processes, and it can be difficult to track access. They can also be printed in logs when debugging errors without your knowledge. Using secrets mitigates these risks.

## [Use secrets](#use-secrets)

Secrets are mounted as a file in `/run/secrets/<secret_name>` inside the container.

Getting a secret into a container is a two-step process. First, define the secret using the [top-level secrets element in your Compose file](https://docs.docker.com/reference/compose-file/secrets/). Next, update your service definitions to reference the secrets they require with the [secrets attribute](https://docs.docker.com/reference/compose-file/services/#secrets). Compose grants access to secrets on a per-service basis.

Unlike the other methods, this permits granular access control within a service container via standard filesystem permissions.

## [Examples](#examples)

### [Single-service secret injection](#single-service-secret-injection)

In the following example, the frontend service is given access to the `my_secret` secret. In the container, `/run/secrets/my_secret` is set to the contents of the file `./my_secret.txt`.

```yaml
services:
  myapp:
    image: myapp:latest
    secrets:
      - my_secret
secrets:
  my_secret:
    file: ./my_secret.txt
```

### [Multi-service secret sharing and password management](#multi-service-secret-sharing-and-password-management)

```yaml
services:
   db:
     image: mysql:latest
     volumes:
       - db_data:/var/lib/mysql
     environment:
       MYSQL_ROOT_PASSWORD_FILE: /run/secrets/db_root_password
       MYSQL_DATABASE: wordpress
       MYSQL_USER: wordpress
       MYSQL_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_root_password
       - db_password

   wordpress:
     depends_on:
       - db
     image: wordpress:latest
     ports:
       - "8000:80"
     environment:
       WORDPRESS_DB_HOST: db:3306
       WORDPRESS_DB_USER: wordpress
       WORDPRESS_DB_PASSWORD_FILE: /run/secrets/db_password
     secrets:
       - db_password


secrets:
   db_password:
     file: db_password.txt
   db_root_password:
     file: db_root_password.txt

volumes:
    db_data:
```

In the advanced example above:

* The `secrets` attribute under each service defines the secrets you want to inject into the specific container.
* The top-level `secrets` section defines the variables `db_password` and `db_root_password` and provides the `file` that populates their values.
* The deployment of each container means Docker creates a bind mount under `/run/secrets/<secret_name>` with their specific values.

> Note
>
> The `_FILE` environment variables demonstrated here are a convention used by some images, including Docker Official Images like [mysql](https://hub.docker.com/_/mysql) and [postgres](https://hub.docker.com/_/postgres).

### [Build secrets](#build-secrets)

In the following example, the `npm_token` secret is made available at build time. Its value is taken from the `NPM_TOKEN` environment variable.

```yaml
services:
  myapp:
    build:
      secrets:
        - npm_token
      context: .

secrets:
  npm_token:
    environment: NPM_TOKEN
```

## [Resources](#resources)

* [Familiarize yourself with Compose's trust model](https://docs.docker.com/compose/trust-model/)
* [Secrets top-level element](https://docs.docker.com/reference/compose-file/secrets/)
* [Secrets attribute for services top-level element](https://docs.docker.com/reference/compose-file/services/#secrets)
* [Build secrets](https://docs.docker.com/build/building/secrets/)

----
url: https://docs.docker.com/reference/cli/docker/volume/rm/
----

# docker volume rm

***

| Description                                                               | Remove one or more volumes                      |
| ------------------------------------------------------------------------- | ----------------------------------------------- |
| Usage                                                                     | `docker volume rm [OPTIONS] VOLUME [VOLUME...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker volume remove`                          |

## [Description](#description)

Remove one or more volumes. You can't remove a volume that's in use by a container.

## [Options](#options)

| Option        | Default | Description                                        |
| ------------- | ------- | -------------------------------------------------- |
| `-f, --force` |         | API 1.25+ Force the removal of one or more volumes |

## [Examples](#examples)

```console
$ docker volume rm hello

hello
```

----
url: https://docs.docker.com/reference/cli/docker/scout/cache/
----

# docker scout cache

***

| Description | Manage Docker Scout cache and temporary files |
| ----------- | --------------------------------------------- |

## [Description](#description)

Manage Docker Scout cache and temporary files

## [Subcommands](#subcommands)

| Command                                                                                       | Description                     |
| --------------------------------------------------------------------------------------------- | ------------------------------- |
| [`docker scout cache df`](https://docs.docker.com/reference/cli/docker/scout/cache/df/)       | Show Docker Scout disk usage    |
| [`docker scout cache prune`](https://docs.docker.com/reference/cli/docker/scout/cache/prune/) | Remove temporary or cached data |

----
url: https://docs.docker.com/reference/api/extensions-sdk/ExecStreamOptions/
----

# Interface: ExecStreamOptions

***

Table of contents

***

**`Since`**

0.2.2

## [Properties](#properties)

### [onOutput](#onoutput)

• `Optional` **onOutput**: (`data`: { `stdout`: `string` ; `stderr?`: `undefined` } | { `stdout?`: `undefined` ; `stderr`: `string` }) => `void`

#### [Type declaration](#type-declaration)

▸ (`data`): `void`

Invoked when receiving output from command execution. By default, the output is split into chunks at arbitrary boundaries. If you prefer the output to be split into complete lines, set `splitOutputLines` to true. The callback is then invoked once for each line.

**`Since`**

0.2.0

##### [Parameters](#parameters)

| Name   | Type                                                                               | Description                                                                        |
| ------ | ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `data` | `{ stdout: string; stderr?: undefined } \| { stdout?: undefined; stderr: string }` | Output content. Can include either stdout string, or stderr string, one at a time. |

##### [Returns](#returns)

`void`

***

### [onError](#onerror)

• `Optional` **onError**: (`error`: `any`) => `void`

#### [Type declaration](#type-declaration-1)

▸ (`error`): `void`

Invoked to report error if the executed command errors.

##### [Parameters](#parameters-1)

| Name    | Type  | Description                                 |
| ------- | ----- | ------------------------------------------- |
| `error` | `any` | The error happening in the executed command |

##### [Returns](#returns-1)

`void`

***

### [onClose](#onclose)

• `Optional` **onClose**: (`exitCode`: `number`) => `void`

#### [Type declaration](#type-declaration-2)

▸ (`exitCode`): `void`

Invoked when process exits.

##### [Parameters](#parameters-2)

| Name       | Type     | Description           |
| ---------- | -------- | --------------------- |
| `exitCode` | `number` | The process exit code |

##### [Returns](#returns-2)

`void`

***

### [splitOutputLines](#splitoutputlines)

• `Optional` `Readonly` **splitOutputLines**: `boolean`

Specifies the behaviour invoking `onOutput(data)`. Raw output by default, splitting output at any position. If set to true, `onOutput` will be invoked once for each line.

----
url: https://docs.docker.com/engine/storage/tmpfs/
----

# tmpfs mounts

***

Table of contents

***

[Volumes](https://docs.docker.com/engine/storage/volumes/) and [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/) let you share files between the host machine and container so that you can persist data even after the container is stopped.

If you're running Docker on Linux, you have a third option: tmpfs mounts. When you create a container with a tmpfs mount, the container can create files outside the container's writable layer.

As opposed to volumes and bind mounts, a tmpfs mount is temporary, and only persisted in the host memory. When the container stops, the tmpfs mount is removed, and files written there won't be persisted.

tmpfs mounts are best used for cases when you do not want the data to persist either on the host machine or within the container. This may be for security reasons or to protect the performance of the container when your application needs to write a large volume of non-persistent state data.

> Important
>
> tmpfs mounts in Docker map directly to [tmpfs](https://en.wikipedia.org/wiki/Tmpfs) in the Linux kernel. As such, the temporary data may be written to a swap file, and thereby persisted to the filesystem.

## [Mounting over existing data](#mounting-over-existing-data)

If you create a tmpfs mount into a directory in the container in which files or directories exist, the pre-existing files are obscured by the mount. This is similar to if you were to save files into `/mnt` on a Linux host, and then mounted a USB drive into `/mnt`. The contents of `/mnt` would be obscured by the contents of the USB drive until the USB drive was unmounted.

With containers, there's no straightforward way of removing a mount to reveal the obscured files again. Your best option is to recreate the container without the mount.

## [Limitations of tmpfs mounts](#limitations-of-tmpfs-mounts)

* Unlike volumes and bind mounts, you can't share tmpfs mounts between containers.
* This functionality is only available if you're running Docker on Linux.
* Setting permissions on tmpfs may cause them to [reset after container restart](https://github.com/docker/for-linux/issues/138). In some cases [setting the uid/gid](https://github.com/docker/compose/issues/3425#issuecomment-423091370) can serve as a workaround.

## [Syntax](#syntax)

To mount a tmpfs with the `docker run` command, you can use either the `--mount` or `--tmpfs` flag.

```console
$ docker run --mount type=tmpfs,dst=<mount-path>
$ docker run --tmpfs <mount-path>
```

In general, `--mount` is preferred. The main difference is that the `--mount` flag is more explicit. On the other hand, `--tmpfs` is less verbose and gives you more flexibility as it lets you set more mount options.

The `--tmpfs` flag cannot be used with swarm services. You must use `--mount`.

### [Options for --tmpfs](#options-for---tmpfs)

The `--tmpfs` flag consists of two fields, separated by a colon character (`:`).

```console
$ docker run --tmpfs <mount-path>[:opts]
```

The first field is the container path to mount into a tmpfs. The second field is optional and lets you set mount options. Valid mount options for `--tmpfs` include:

| Option       | Description                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------- |
| `ro`         | Creates a read-only tmpfs mount.                                                            |
| `rw`         | Creates a read-write tmpfs mount (default behavior).                                        |
| `nosuid`     | Prevents `setuid` and `setgid` bits from being honored during execution.                    |
| `suid`       | Allows `setuid` and `setgid` bits to be honored during execution (default behavior).        |
| `nodev`      | Device files can be created but are not functional (access results in an error).            |
| `dev`        | Device files can be created and are fully functional.                                       |
| `exec`       | Allows the execution of executable binaries in the mounted file system.                     |
| `noexec`     | Does not allow the execution of executable binaries in the mounted file system.             |
| `sync`       | All I/O to the file system is done synchronously.                                           |
| `async`      | All I/O to the file system is done asynchronously (default behavior).                       |
| `dirsync`    | Directory updates within the file system are done synchronously.                            |
| `atime`      | Updates file access time each time the file is accessed.                                    |
| `noatime`    | Does not update file access times when the file is accessed.                                |
| `diratime`   | Updates directory access times each time the directory is accessed.                         |
| `nodiratime` | Does not update directory access times when the directory is accessed.                      |
| `size`       | Specifies the size of the tmpfs mount, for example, `size=64m`.                             |
| `mode`       | Specifies the file mode (permissions) for the tmpfs mount (for example, `mode=1777`).       |
| `uid`        | Specifies the user ID for the owner of the tmpfs mount (for example, `uid=1000`).           |
| `gid`        | Specifies the group ID for the owner of the tmpfs mount (for example, `gid=1000`).          |
| `nr_inodes`  | Specifies the maximum number of inodes for the tmpfs mount (for example, `nr_inodes=400k`). |
| `nr_blocks`  | Specifies the maximum number of blocks for the tmpfs mount (for example, `nr_blocks=1024`). |

Example

```console
$ docker run --tmpfs /data:noexec,size=1024,mode=1777
```

Not all tmpfs mount features available in the Linux mount command are supported with the `--tmpfs` flag. If you require advanced tmpfs options or features, you may need to use a privileged container or configure the mount outside of Docker.

> Caution
>
> Running containers with `--privileged` grants elevated permissions and can expose the host system to security risks. Use this option only when absolutely necessary and in trusted environments.

```console
$ docker run --privileged -it debian sh
/# mount -t tmpfs -o <options> tmpfs /data
```

### [Options for --mount](#options-for---mount)

The `--mount` flag consists of multiple key-value pairs, separated by commas and each consisting of a `<key>=<value>` tuple. The order of the keys isn't significant.

```console
$ docker run --mount type=tmpfs,dst=<mount-path>[,<key>=<value>...]
```

Valid options for `--mount type=tmpfs` include:

| Option                         | Description                                                                                                            |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| `destination`, `dst`, `target` | Container path to mount into a tmpfs.                                                                                  |
| `tmpfs-size`                   | Size of the tmpfs mount in bytes. If unset, the default maximum size of a tmpfs volume is 50% of the host's total RAM. |
| `tmpfs-mode`                   | File mode of the tmpfs in octal. For instance, `700` or `0770`. Defaults to `1777` or world-writable.                  |

Example

```console
$ docker run --mount type=tmpfs,dst=/app,tmpfs-size=21474836480,tmpfs-mode=1770
```

## [Use a tmpfs mount in a container](#use-a-tmpfs-mount-in-a-container)

To use a `tmpfs` mount in a container, use the `--tmpfs` flag, or use the `--mount` flag with `type=tmpfs` and `destination` options. There is no `source` for `tmpfs` mounts. The following example creates a `tmpfs` mount at `/app` in a Nginx container. The first example uses the `--mount` flag and the second uses the `--tmpfs` flag.

```console
$ docker run -d \
  -it \
  --name tmptest \
  --mount type=tmpfs,destination=/app \
  nginx:latest
```

Verify that the mount is a `tmpfs` mount by looking in the `Mounts` section of the `docker inspect` output:

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
[{"Type":"tmpfs","Source":"","Destination":"/app","Mode":"","RW":true,"Propagation":""}]
```

```console
$ docker run -d \
  -it \
  --name tmptest \
  --tmpfs /app \
  nginx:latest
```

Verify that the mount is a `tmpfs` mount by looking in the `Mounts` section of the `docker inspect` output:

```console
$ docker inspect tmptest --format '{{ json .Mounts }}'
{"/app":""}
```

Stop and remove the container:

```console
$ docker stop tmptest
$ docker rm tmptest
```

## [Next steps](#next-steps)

* Learn about [volumes](https://docs.docker.com/engine/storage/volumes/)
* Learn about [bind mounts](https://docs.docker.com/engine/storage/bind-mounts/)
* Learn about [storage drivers](/engine/storage/drivers/)

----
url: https://docs.docker.com/guides/r/
----

# R language-specific guide

***

This guide details how to containerize R applications using Docker.

**Time to complete** 10 minutes

The R language-specific guide teaches you how to containerize a R application using Docker. In this guide, you’ll learn how to:

* Containerize and run a R application
* Set up a local environment to develop a R application using containers
* Configure a CI/CD pipeline for a containerized R application using GitHub Actions
* Deploy your containerized R application locally to Kubernetes to test and debug your deployment

Start by containerizing an existing R application.

## [Modules](#modules)

1. [Containerize your app](https://docs.docker.com/guides/r/containerize/)

   Learn how to containerize a R application.

2. [Develop your app](https://docs.docker.com/guides/r/develop/)

   Learn how to develop your R application locally.

3. [Configure CI/CD](https://docs.docker.com/guides/r/configure-ci-cd/)

   Learn how to configure CI/CD using GitHub Actions for your R application.

4. [Test your deployment](https://docs.docker.com/guides/r/deploy/)

   Learn how to develop locally using Kubernetes

----
url: https://docs.docker.com/reference/cli/docker/model/launch/
----

# docker model launch

***

| Description | Launch an app configured to use Docker Model Runner |
| ----------- | --------------------------------------------------- |
| Usage       | `docker model launch [APP] [-- APP_ARGS...]`        |

## [Description](#description)

Launch an app configured to use Docker Model Runner.

Without arguments, lists all supported apps.

Supported apps: anythingllm, claude, codex, openclaw, opencode, openwebui

Examples: docker model launch docker model launch opencode docker model launch claude -- --help docker model launch openwebui --port 3000 docker model launch claude --config

## [Options](#options)

| Option      | Default | Description                                     |
| ----------- | ------- | ----------------------------------------------- |
| `--config`  |         | Print configuration without launching           |
| `--detach`  |         | Run containerized app in background             |
| `--dry-run` |         | Print what would be executed without running it |
| `--image`   |         | Override container image for containerized apps |
| `--model`   |         | Model to use (for opencode)                     |
| `--port`    |         | Host port to expose (web UIs)                   |

----
url: https://docs.docker.com/reference/cli/docker/network/connect/
----

# docker network connect

***

| Description | Connect a container to a network                     |
| ----------- | ---------------------------------------------------- |
| Usage       | `docker network connect [OPTIONS] NETWORK CONTAINER` |

## [Description](#description)

Connects a container to a network. You can connect a container by name or by ID. Once connected, the container can communicate with other containers in the same network.

## [Options](#options)

| Option              | Default | Description                                                                              |
| ------------------- | ------- | ---------------------------------------------------------------------------------------- |
| [`--alias`](#alias) |         | Add network-scoped alias for the container                                               |
| `--driver-opt`      |         | driver options for the network                                                           |
| `--gw-priority`     |         | Highest gw-priority provides the default gateway. Accepts positive and negative values.  |
| [`--ip`](#ip)       | ``      | IPv4 address (e.g., `172.30.100.104`)                                                    |
| `--ip6`             | ``      | IPv6 address (e.g., `2001:db8::33`)                                                      |
| [`--link`](#link)   |         | Add link to another container                                                            |
| `--link-local-ip`   |         | Add a link-local address for the container                                               |

## [Examples](#examples)

### [Connect a running container to a network](#connect-a-running-container-to-a-network)

```console
$ docker network connect multi-host-network container1
```

### [Connect a container to a network when it starts](#connect-a-container-to-a-network-when-it-starts)

You can also use the `docker run --network=<network-name>` option to start a container and immediately connect it to a network.

```console
$ docker run -itd --network=multi-host-network busybox
```

### [Specify the IP address a container will use on a given network (--ip)](#ip)

You can specify the IP address you want to be assigned to the container's interface.

```console
$ docker network connect --ip 10.10.36.122 multi-host-network container2
```

### [Use the legacy `--link` option (--link)](#link)

You can use `--link` option to link another container with a preferred alias.

```console
$ docker network connect --link container1:c1 multi-host-network container2
```

### [Create a network alias for a container (--alias)](#alias)

`--alias` option can be used to resolve the container by another name in the network being connected to.

```console
$ docker network connect --alias db --alias mysql multi-host-network container2
```

### [Set sysctls for a container's interface (--driver-opt)](#sysctl)

`sysctl` settings that start with `net.ipv4.` and `net.ipv6.` can be set per-interface using `--driver-opt` label `com.docker.network.endpoint.sysctls`. The name of the interface must be replaced by `IFNAME`.

To set more than one `sysctl` for an interface, quote the whole value of the `driver-opt` field, remembering to escape the quotes for the shell if necessary. For example, if the interface to `my-net` is given name `eth3`, the following example sets `net.ipv4.conf.eth3.log_martians=1` and `net.ipv4.conf.eth3.forwarding=0`.

```console
$ docker network connect --driver-opt=\"com.docker.network.endpoint.sysctls=net.ipv4.conf.IFNAME.log_martians=1,net.ipv4.conf.IFNAME.forwarding=0\" multi-host-network container2
```

> Note
>
> Network drivers may restrict the sysctl settings that can be modified and, to protect the operation of the network, new restrictions may be added in the future.

### [Network implications of stopping, pausing, or restarting containers](#network-implications-of-stopping-pausing-or-restarting-containers)

You can pause, restart, and stop containers that are connected to a network. A container connects to its configured networks when it runs.

If specified, the container's IP address(es) is reapplied when a stopped container is restarted. If the IP address is no longer available, the container fails to start. One way to guarantee that the IP address is available is to specify an `--ip-range` when creating the network, and choose the static IP address(es) from outside that range. This ensures that the IP address is not given to another container while this container is not on the network.

```console
$ docker network create --subnet 172.20.0.0/16 --ip-range 172.20.240.0/20 multi-host-network
```

```console
$ docker network connect --ip 172.20.128.2 multi-host-network container2
```

To verify the container is connected, use the `docker network inspect` command. Use `docker network disconnect` to remove a container from the network.

Once connected in network, containers can communicate using only another container's IP address or name. For `overlay` networks or custom plugins that support multi-host connectivity, containers connected to the same multi-host network but launched from different Engines can also communicate in this way.

You can connect a container to one or more networks. The networks need not be the same type. For example, you can connect a single container bridge and overlay networks.

----
url: https://docs.docker.com/reference/cli/docker/node/rm/
----

# docker node rm

***

| Description                                                               | Remove one or more nodes from the swarm   |
| ------------------------------------------------------------------------- | ----------------------------------------- |
| Usage                                                                     | `docker node rm [OPTIONS] NODE [NODE...]` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker node remove`                      |

Swarm This command works with the Swarm orchestrator.

## [Description](#description)

Removes the specified nodes from a swarm.

> Note
>
> This is a cluster management command, and must be executed on a swarm manager node. To learn about managers and workers, refer to the [Swarm mode section](/engine/swarm/) in the documentation.

## [Options](#options)

| Option                  | Default | Description                        |
| ----------------------- | ------- | ---------------------------------- |
| [`-f, --force`](#force) |         | Force remove a node from the swarm |

## [Examples](#examples)

### [Remove a stopped node from the swarm](#remove-a-stopped-node-from-the-swarm)

```console
$ docker node rm swarm-node-02

Node swarm-node-02 removed from swarm
```

### [Attempt to remove a running node from a swarm](#attempt-to-remove-a-running-node-from-a-swarm)

Removes the specified nodes from the swarm, but only if the nodes are in the down state. If you attempt to remove an active node you will receive an error:

```console
$ docker node rm swarm-node-03

Error response from daemon: rpc error: code = 9 desc = node swarm-node-03 is not
down and can't be removed
```

### [Forcibly remove an inaccessible node from a swarm (--force)](#force)

If you lose access to a worker node or need to shut it down because it has been compromised or is not behaving as expected, you can use the `--force` option. This may cause transient errors or interruptions, depending on the type of task being run on the node.

```console
$ docker node rm --force swarm-node-03

Node swarm-node-03 removed from swarm
```

A manager node must be demoted to a worker node (using `docker node demote`) before you can remove it from the swarm.

----
url: https://docs.docker.com/reference/cli/docker/builder/prune/
----

# docker builder prune

***

| Description | Remove build cache     |
| ----------- | ---------------------- |
| Usage       | `docker builder prune` |

## [Description](#description)

Remove build cache

## [Options](#options)

| Option           | Default | Description                                           |
| ---------------- | ------- | ----------------------------------------------------- |
| `-a, --all`      |         | Remove all unused build cache, not just dangling ones |
| `--filter`       |         | Provide filter values (e.g. `until=24h`)              |
| `-f, --force`    |         | Do not prompt for confirmation                        |
| `--keep-storage` |         | Amount of disk space to keep for cache                |

----
url: https://docs.docker.com/reference/cli/docker/buildx/dap/
----

# docker buildx dap

***

| Description | Start debug adapter protocol compatible debugger |
| ----------- | ------------------------------------------------ |

## [Description](#description)

Start debug adapter protocol compatible debugger

## [Subcommands](#subcommands)

| Command                                                                                     | Description   |
| ------------------------------------------------------------------------------------------- | ------------- |
| [`docker buildx dap build`](https://docs.docker.com/reference/cli/docker/buildx/dap/build/) | Start a build |

----
url: https://docs.docker.com/engine/release-notes/17.06/
----

# Docker Engine 17.06 release notes

***

Table of contents

***

## [17.06.2-ce](#17062-ce)

2017-09-05

### [Client](#client)

* Enable TCP keepalive in the client to prevent loss of connection [docker/cli#415](https://github.com/docker/cli/pull/415)

### [Runtime](#runtime)

* Devmapper: ensure UdevWait is called after calls to setCookie [moby/moby#33732](https://github.com/moby/moby/pull/33732)
* Aufs: ensure diff layers are correctly removed to prevent leftover files from using up storage [moby/moby#34587](https://github.com/moby/moby/pull/34587)

### [Swarm mode](#swarm-mode)

* Ignore PullOptions for running tasks [docker/swarmkit#2351](https://github.com/docker/swarmkit/pull/2351)

## [17.06.1-ce](#17061-ce)

2017-08-15

### [Builder](#builder)

* Fix a regression, where `ADD` from remote URL's extracted archives [#89](https://github.com/docker/docker-ce/pull/89)
* Fix handling of remote "git@" notation [#100](https://github.com/docker/docker-ce/pull/100)
* Fix copy `--from` conflict with force pull [#86](https://github.com/docker/docker-ce/pull/86)

### [Client](#client-1)

* Make pruning volumes optional when running `docker system prune`, and add a `--volumes` flag [#109](https://github.com/docker/docker-ce/pull/109)
* Show progress of replicated tasks before they are assigned [#97](https://github.com/docker/docker-ce/pull/97)
* Fix `docker wait` hanging if the container does not exist [#106](https://github.com/docker/docker-ce/pull/106)
* If `docker swarm ca` is called without the `--rotate` flag, warn if other flags are passed [#110](https://github.com/docker/docker-ce/pull/110)
* Fix API version negotiation not working if the daemon returns an error [#115](https://github.com/docker/docker-ce/pull/115)
* Print an error if "until" filter is combined with "--volumes" on system prune [#154](https://github.com/docker/docker-ce/pull/154)

### [Logging](#logging)

* Fix stderr logging for `journald` and `syslog` [#95](https://github.com/docker/docker-ce/pull/95)
* Fix log readers can block writes indefinitely [#98](https://github.com/docker/docker-ce/pull/98)
* Fix `awslogs` driver repeating last event [#151](https://github.com/docker/docker-ce/pull/151)

### [Networking](#networking)

* Fix issue with driver options not received by network drivers [#127](https://github.com/docker/docker-ce/pull/127)

### [Plugins](#plugins)

* Make plugin removes more resilient to failure [#91](https://github.com/docker/docker-ce/pull/91)

### [Runtime](#runtime-1)

* Prevent a `goroutine` leak when `healthcheck` gets stopped [#90](https://github.com/docker/docker-ce/pull/90)
* Do not error on relabel when relabel not supported [#92](https://github.com/docker/docker-ce/pull/92)
* Limit max backoff delay to 2 seconds for GRPC connection [#94](https://github.com/docker/docker-ce/pull/94)
* Fix issue preventing containers to run when memory cgroup was specified due to bug in certain kernels [#102](https://github.com/docker/docker-ce/pull/102)
* Fix container not responding to SIGKILL when paused [#102](https://github.com/docker/docker-ce/pull/102)
* Improve error message if an image for an incompatible OS is loaded [#108](https://github.com/docker/docker-ce/pull/108)
* Fix a handle leak in `go-winio` [#112](https://github.com/docker/docker-ce/pull/112)
* Fix issue upon upgrade, preventing docker from showing running containers when `--live-restore` is enabled [#117](https://github.com/docker/docker-ce/pull/117)
* Fix bug where services using secrets would fail to start on daemons using the `userns-remap` feature [#121](https://github.com/docker/docker-ce/pull/121)
* Fix error handling with `not-exist` errors on remove [#142](https://github.com/docker/docker-ce/pull/142)
* Fix REST API Swagger representation cannot be loaded with SwaggerUI [#156](https://github.com/docker/docker-ce/pull/156)

### [Security](#security)

* Redact secret data on secret creation [#99](https://github.com/docker/docker-ce/pull/99)

### [Swarm mode](#swarm-mode-1)

* Do not add duplicate platform information to service spec [#107](https://github.com/docker/docker-ce/pull/107)
* Cluster update and memory issue fixes [#114](https://github.com/docker/docker-ce/pull/114)
* Changing get network request to return predefined network in swarm [#150](https://github.com/docker/docker-ce/pull/150)

## [17.06.0-ce](#17060-ce)

2017-06-28

> Note
>
> of the `ADD` instruction of Dockerfile when referencing a remote `.tar.gz` file. The issue will be fixed in Docker 17.06.1.

> Note
>
> for IBM Z using the s390x architecture.

> Note
>
> registries. If you require interaction with registries that have not yet migrated to the v2 protocol, set the `--disable-legacy-registry=false` daemon option. Interaction with v1 registries will be removed in Docker 17.12.

### [Builder](#builder-1)

* Add `--iidfile` option to docker build. It allows specifying a location where to save the resulting image ID
* Allow specifying any remote ref in git checkout URLs [#32502](https://github.com/moby/moby/pull/32502)

### [Client](#client-2)

* Add `--format` option to `docker stack ls` [#31557](https://github.com/moby/moby/pull/31557)
* Add support for labels in compose initiated builds [#32632](https://github.com/moby/moby/pull/32632) [#32972](https://github.com/moby/moby/pull/32972)
* Add `--format` option to `docker history` [#30962](https://github.com/moby/moby/pull/30962)
* Add `--format` option to `docker system df` [#31482](https://github.com/moby/moby/pull/31482)
* Allow specifying Nameservers and Search Domains in stack files [#32059](https://github.com/moby/moby/pull/32059)
* Add support for `read_only` service to `docker stack deploy` [#docker/cli/73](https://github.com/docker/cli/pull/73)

- Display Swarm cluster and node TLS information [#docker/cli/44](https://github.com/docker/cli/pull/44)

* Add support for placement preference to `docker stack deploy` [#docker/cli/35](https://github.com/docker/cli/pull/35)
* Add new `ca` subcommand to `docker swarm` to allow managing a swarm CA [#docker/cli/48](https://github.com/docker/cli/pull/48)
* Add credential-spec to compose [#docker/cli/71](https://github.com/docker/cli/pull/71)
* Add support for csv format options to `--network` and `--network-add` [#docker/cli/62](https://github.com/docker/cli/pull/62) [#33130](https://github.com/moby/moby/pull/33130)

- Fix stack compose bind-mount volumes on Windows [#docker/cli/136](https://github.com/docker/cli/pull/136)
- Correctly handle a Docker daemon without registry info [#docker/cli/126](https://github.com/docker/cli/pull/126)

* Allow `--detach` and `--quiet` flags when using --rollback [#docker/cli/144](https://github.com/docker/cli/pull/144)
* Remove deprecated `--email` flag from `docker login` [#docker/cli/143](https://github.com/docker/cli/pull/143)

- Adjusted `docker stats` memory output [#docker/cli/80](https://github.com/docker/cli/pull/80)

### [Distribution](#distribution)

* Select digest over tag when both are provided during a pull [#33214](https://github.com/moby/moby/pull/33214)

### [Logging](#logging-1)

* Add monitored resource type metadata for GCP logging driver [#32930](https://github.com/moby/moby/pull/32930)
* Add multiline processing to the AWS CloudWatch logs driver [#30891](https://github.com/moby/moby/pull/30891)

### [Networking](#networking-1)

* Add Support swarm-mode services with node-local networks such as macvlan, ipvlan, bridge, host [#32981](https://github.com/moby/moby/pull/32981)
* Pass driver-options to network drivers on service creation [#32981](https://github.com/moby/moby/pull/33130)
* Isolate Swarm Control-plane traffic from Application data traffic using --data-path-addr [#32717](https://github.com/moby/moby/pull/32717)

- Several improvements to Service Discovery [#docker/libnetwork/1796](https://github.com/docker/libnetwork/pull/1796)

### [Packaging](#packaging)

* Rely on `container-selinux` on Centos/Fedora/RHEL when available [#32437](https://github.com/moby/moby/pull/32437)

### [Runtime](#runtime-2)

* Add build & engine info prometheus metrics [#32792](https://github.com/moby/moby/pull/32792)

- Update containerd to d24f39e203aa6be4944f06dd0fe38a618a36c764 [#33007](https://github.com/moby/moby/pull/33007)
- Update runc to 992a5be178a62e026f4069f443c6164912adbf09 [#33007](https://github.com/moby/moby/pull/33007)

* Add option to auto-configure blkdev for devmapper [#31104](https://github.com/moby/moby/pull/31104)
* Add log driver list to `docker info` [#32540](https://github.com/moby/moby/pull/32540)
* Add API endpoint to allow retrieving an image manifest [#32061](https://github.com/moby/moby/pull/32061)

- Do not remove container from memory on error with `forceremove` [#31012](https://github.com/moby/moby/pull/31012)

* Add support for metric plugins [#32874](https://github.com/moby/moby/pull/32874)

- Return an error when an invalid filter is given to `prune` commands [#33023](https://github.com/moby/moby/pull/33023)

* Add daemon option to allow pushing foreign layers [#33151](https://github.com/moby/moby/pull/33151)

- Fix an issue preventing containerd to be restarted after it died [#32986](https://github.com/moby/moby/pull/32986)

* Add cluster events to Docker event stream. [#32421](https://github.com/moby/moby/pull/32421)
* Add support for DNS search on windows [#33311](https://github.com/moby/moby/pull/33311)

- Upgrade to Go 1.8.3 [#33387](https://github.com/moby/moby/pull/33387)

* Prevent a containerd crash when journald is restarted [#containerd/930](https://github.com/containerd/containerd/pull/930)
* Fix healthcheck failures due to invalid environment variables [#33249](https://github.com/moby/moby/pull/33249)
* Prevent a directory to be created in lieu of the daemon socket when a container mounting it is to be restarted during a shutdown [#30348](https://github.com/moby/moby/pull/33330)
* Prevent a container to be restarted upon stop if its stop signal is set to `SIGKILL` [#33335](https://github.com/moby/moby/pull/33335)
* Ensure log drivers get passed the same filename to both StartLogging and StopLogging endpoints [#33583](https://github.com/moby/moby/pull/33583)
* Remove daemon data structure dump on `SIGUSR1` to avoid a panic [#33598](https://github.com/moby/moby/pull/33598)

### [Security](#security-1)

* Allow personality with UNAME26 bit set in default seccomp profile [#32965](https://github.com/moby/moby/pull/32965)

### [Swarm Mode](#swarm-mode-2)

* Add an option to allow specifying a different interface for the data traffic (as opposed to control traffic) [#32717](https://github.com/moby/moby/pull/32717)

- Allow specifying a secret location within the container [#32571](https://github.com/moby/moby/pull/32571)

* Add support for secrets on Windows [#32208](https://github.com/moby/moby/pull/32208)
* Add TLS Info to swarm info and node info endpoint [#32875](https://github.com/moby/moby/pull/32875)
* Add support for services to carry arbitrary config objects [#32336](https://github.com/moby/moby/pull/32336), [#docker/cli/45](https://github.com/docker/cli/pull/45),[#33169](https://github.com/moby/moby/pull/33169)
* Add API to rotate swarm CA certificate [#32993](https://github.com/moby/moby/pull/32993)

- Service digest pining is now handled client side [#32388](https://github.com/moby/moby/pull/32388), [#33239](https://github.com/moby/moby/pull/33239)

* Placement now also take platform in account [#33144](https://github.com/moby/moby/pull/33144)

- Fix possible hang when joining fails [#docker-ce/19](https://github.com/docker/docker-ce/pull/19)
- Fix an issue preventing external CA to be accepted [#33341](https://github.com/moby/moby/pull/33341)
- Fix possible orchestration panic in mixed version clusters [#swarmkit/2233](https://github.com/docker/swarmkit/pull/2233)
- Avoid assigning duplicate IPs during initialization [#swarmkit/2237](https://github.com/docker/swarmkit/pull/2237)

### [Deprecation](#deprecation)

* Disable legacy registry (v1) by default [#33629](https://github.com/moby/moby/pull/33629)

----
url: https://docs.docker.com/guides/testcontainers-java-jooq-flyway/
----

[Insights on the state of AI agents from 800+ builders and leaders. Download your copy](https://www.docker.com/resources/the-state-of-agentic-ai-white-paper/)

✕

# Working with jOOQ and Flyway using Testcontainers

Table of contents

***

Generate typesafe jOOQ code from a real PostgreSQL database managed by Flyway migrations, then test repositories using Testcontainers.

**Time to complete** 25 minutes

In this guide, you will learn how to:

* Create a Spring Boot application with jOOQ support
* Generate jOOQ code using Testcontainers, Flyway, and a Maven plugin
* Implement basic database operations using jOOQ
* Load complex object graphs using jOOQ's MULTISET feature
* Test the jOOQ persistence layer using Testcontainers

## [Prerequisites](#prerequisites)

* Java 17+
* Maven
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-java-jooq-flyway/create-project/)

   Set up a Spring Boot project with jOOQ, Flyway, PostgreSQL, and Testcontainers code generation.

2. [Write tests](https://docs.docker.com/guides/testcontainers-java-jooq-flyway/write-tests/)

   Test jOOQ repositories using Testcontainers with the @JooqTest slice and @SpringBootTest.

3. [Run tests](https://docs.docker.com/guides/testcontainers-java-jooq-flyway/run-tests/)

   Run the jOOQ and Flyway integration tests and explore next steps.

----
url: https://docs.docker.com/desktop/troubleshoot-and-support/feedback/
----

***

Table of contents

***

There are many ways you can provide feedback on Docker Desktop or Docker Desktop features.

### [In-product feedback](#in-product-feedback)

On each Docker Desktop Dashboard view, there is a **Give feedback** link. This opens a feedback form where you can share ideas directly with the Docker Team.

### [Feedback via Docker Community forums](#feedback-via-docker-community-forums)

To get help from the community, review current user topics, join or start a discussion, sign in to the appropriate Docker forums:

* [Docker Desktop for Mac forum](https://forums.docker.com/c/docker-for-mac)
* [Docker Desktop for Windows forum](https://forums.docker.com/c/docker-for-windows)
* [Docker Desktop for Linux forum](https://forums.docker.com/c/docker-desktop-for-linux/60)

### [Report bugs or problems on GitHub](#report-bugs-or-problems-on-github)

To report bugs or problems, visit:

* [Docker Desktop issues on GitHub](https://github.com/docker/desktop-feedback)
* [Docker Extensions issues on GitHub](https://github.com/docker/extensions-sdk/issues)

### [Feedback via Community Slack channels](#feedback-via-community-slack-channels)

You can also provide feedback through the following [Docker Community Slack](https://dockr.ly/comm-slack) channels:

* \#docker-desktop-mac
* \#docker-desktop-windows
* \#docker-desktop-linux
* \#extensions

----
url: https://docs.docker.com/reference/cli/docker/manifest/rm/
----

# docker manifest rm

***

| Description | Delete one or more manifest lists from local storage  |
| ----------- | ----------------------------------------------------- |
| Usage       | `docker manifest rm MANIFEST_LIST [MANIFEST_LIST...]` |

**Experimental**

**This command is experimental.**

Experimental features are intended for testing and feedback as their functionality or design may change between releases without warning or can be removed entirely in a future release.

## [Description](#description)

Delete one or more manifest lists from local storage

----
url: https://docs.docker.com/desktop/troubleshoot-and-support/faqs/general/
----

# General FAQs for Desktop

***

Table of contents

***

### [Can I use Docker Desktop offline?](#can-i-use-docker-desktop-offline)

Yes, you can use Docker Desktop offline. However, you cannot access features that require an active internet connection. Additionally, any functionality that requires you to sign in won't work while using Docker Desktop offline or in air-gapped environments.

### [How do I connect to the remote Docker Engine API?](#how-do-i-connect-to-the-remote-docker-engine-api)

To connect to the remote Engine API, you might need to provide the location of the Engine API for Docker clients and development tools.

Mac and Windows WSL 2 users can connect to the Docker Engine through a Unix socket: `unix:///var/run/docker.sock`. Docker Desktop for Linux uses a [per-user socket](https://docs.docker.com/desktop/troubleshoot-and-support/faqs/linuxfaqs/#how-do-i-use-docker-sdks-with-docker-desktop-for-linux) located at `~/.docker/desktop/docker.sock` instead of the system-wide `/var/run/docker.sock`.

If you are working with applications like [Apache Maven](https://maven.apache.org/) that expect settings for `DOCKER_HOST` and `DOCKER_CERT_PATH` environment variables, specify these to connect to Docker instances through Unix sockets.

For example:

```console
$ export DOCKER_HOST=unix:///var/run/docker.sock
```

Docker Desktop Windows users can connect to the Docker Engine through a **named pipe**: `npipe:////./pipe/docker_engine`, or **TCP socket** at this URL: `tcp://localhost:2375`.

For details, see [Docker Engine API](https://docs.docker.com/reference/api/engine/).

### [How do I connect from a container to a service on the host?](#how-do-i-connect-from-a-container-to-a-service-on-the-host)

The host has a changing IP address, or none if you have no network access. It is recommend that you connect to the special DNS name `host.docker.internal`, which resolves to the internal IP address used by the host.

For more information and examples, see [how to connect from a container to a service on the host](https://docs.docker.com/desktop/features/networking/#connect-a-container-to-a-service-on-the-host).

### [Can I pass through a USB device to a container?](#can-i-pass-through-a-usb-device-to-a-container)

Docker Desktop does not support direct USB device passthrough. However, you can use USB over IP to connect common USB devices to the Docker Desktop VM and in turn be forwarded to a container. For more details, see [Using USB/IP with Docker Desktop](https://docs.docker.com/desktop/features/usbip/).

### [How do I verify Docker Desktop is using a proxy server ?](#how-do-i-verify-docker-desktop-is-using-a-proxy-server-)

To verify, look at the most recent events logged in `httpproxy.log`. This is located at `~/Library/Containers/com.docker.docker/Data/log/host` on macOS or `%LOCALAPPDATA%/Docker/log/host/` on Windows.

The following shows a few examples of what you can expect to see:

* Docker Desktop using app level settings (proxy mode manual) for proxy:

  ```console
  host will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
  Linux will use proxy: app settings http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128
  ```

* Docker Desktop using system level settings (proxy mode system) for proxy:

  ```console
  host will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
  Linux will use proxy: static system http_proxy=http://172.211.16.3:3128 https_proxy=http://172.211.16.3:3128 no_proxy=
  ```

* Docker Desktop is not configured to use a proxy server:

  ```console
  host will use proxy: disabled
  Linux will use proxy: disabled
  ```

* Docker Desktop is configured to use app level settings (proxy mode manual) and using a PAC file:

  ```console
  using a proxy PAC file: http://127.0.0.1:8081/proxy.pac
  host will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
  Linux will use proxy: app settings from PAC file http://127.0.0.1:8081/proxy.pac
  ```

* Connect request using the configured proxy server:

  ```console
  CONNECT desktop.docker.com:443: host connecting via static system HTTPS proxy http://172.211.16.3:3128
  ```

### [How do I run Docker Desktop without administrator privileges?](#how-do-i-run-docker-desktop-without-administrator-privileges)

Docker Desktop requires administrator privileges only for installation. Once installed, administrator privileges are not needed to run it. However, for non-admin users to run Docker Desktop, it must be installed using a specific installer flag and meet certain prerequisites, which vary by platform.

To run Docker Desktop on Mac without requiring administrator privileges, install via the command line and pass the `—user=<userid>` installer flag:

```console
$ /Applications/Docker.app/Contents/MacOS/install --user=<userid>
```

You can then sign in to your machine with the user ID specified, and launch Docker Desktop.

> Note
>
> Before launching Docker Desktop, if a `settings-store.json` file already exists in the `~/Library/Group Containers/group.com.docker/` directory, you will see a **Finish setting up Docker Desktop** window that prompts for administrator privileges when you select **Finish**. To avoid this, ensure you delete the `settings-store.json` file left behind from any previous installations before launching the application.

> Note
>
> If you are using the WSL 2 backend, first make sure that you meet the [minimum required version](https://docs.docker.com/desktop/features/wsl/best-practices/) for WSL 2. Otherwise, update WSL 2 first.

To run Docker Desktop on Windows without requiring administrator privileges, install via the command line and pass the `—always-run-service` installer flag.

```console
$ "Docker Desktop Installer.exe" install —always-run-service
```

----
url: https://docs.docker.com/ai/mcp-catalog-and-toolkit/toolkit/
----

# Docker MCP Toolkit

***

Table of contents

***

Availability: Beta

> Note
>
> This page describes the MCP Toolkit interface in Docker Desktop 4.62 and later. Earlier versions have a different UI. Upgrade to follow these instructions exactly.

The Docker MCP Toolkit is a management interface integrated into Docker Desktop that lets you set up, manage, and run containerized MCP servers in profiles and connect them to AI agents. It removes friction from tool usage by offering secure defaults, easy setup, and support for a growing ecosystem of LLM-based clients. It is the fastest way from MCP tool discovery to local execution.

## [Key features](#key-features)

* Cross-LLM compatibility: Works with Claude, Cursor, and other MCP clients.
* Integrated tool discovery: Browse and launch MCP servers from the Docker MCP Catalog directly in Docker Desktop.
* Zero manual setup: No dependency management, runtime configuration, or setup required.
* Profile-based organization: Create separate server collections for different projects or environments.
* Organizes MCP servers into profiles, acting as a gateway for clients to access the servers in each profile.

> Tip
>
> The MCP Toolkit includes [Dynamic MCP](https://docs.docker.com/ai/mcp-catalog-and-toolkit/dynamic-mcp/), which enables AI agents to discover, add, and compose MCP servers on-demand during conversations, without manual configuration. Your agent can search the catalog and add tools as needed when you connect to the gateway.

## [How the MCP Toolkit works](#how-the-mcp-toolkit-works)

MCP introduces two core concepts: MCP clients and MCP servers.

* MCP clients are typically embedded in LLM-based applications, such as the Claude Desktop app. They request resources or actions.
* MCP servers are launched by the client to perform the requested tasks, using any necessary tools, languages, or processes.

Docker standardizes the development, packaging, and distribution of applications, including MCP servers. By packaging MCP servers as containers, Docker eliminates issues related to isolation and environment differences. You can run a container directly, without managing dependencies or configuring runtimes.

Depending on the MCP server, the tools it provides might run within the same container as the server or in dedicated containers for better isolation.

The MCP Toolkit organizes servers into profiles: named collections of servers with their configurations. This lets you maintain different server setups for different projects or environments. When you connect a client, you specify which profile it should use.

## [Security](#security)

The Docker MCP Toolkit combines passive and active measures to reduce attack surfaces and ensure safe runtime behavior.

### [Passive security](#passive-security)

Passive security refers to measures implemented at build-time, when the MCP server code is packaged into a Docker image.

* Image signing and attestation: All MCP server images under `mcp/` in the [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/) are built by Docker and digitally signed to verify their source and integrity. Each image includes a Software Bill of Materials (SBOM) for full transparency.

### [Active security](#active-security)

Active security refers to security measures at runtime, before and after tools are invoked, enforced through resource and access limitations.

* CPU allocation: MCP tools are run in their own container. They are restricted to 1 CPU, limiting the impact of potential misuse of computing resources.

* Memory allocation: Containers for MCP tools are limited to 2 GB.

* Filesystem access: By default, MCP Servers have no access to the host filesystem. The user explicitly selects the servers that will be granted file mounts.

* Interception of tool requests: Requests to and from tools that contain sensitive information such as secrets are blocked.

### [OAuth authentication](#oauth-authentication)

Some MCP servers require authentication to access external services like GitHub, Notion, and Linear. The MCP Toolkit handles OAuth authentication automatically. You authorize access through your browser, and the Toolkit manages credentials securely. You don't need to manually create API tokens or configure authentication for each service.

#### [Authorize a server with OAuth](#authorize-a-server-with-oauth)

1. In Docker Desktop, go to **MCP Toolkit** and select the **Catalog** tab.
2. Find and add an MCP server that requires OAuth.
3. In the server's **Configuration** tab, select the **OAuth** authentication method. Follow the link to begin the OAuth authorization.
4. Your browser opens the authorization page for the service. Follow the on-screen instructions to complete authentication.
5. Return to Docker Desktop when authentication is complete.

View all authorized services in the **OAuth** tab. To revoke access, select **Revoke** next to the service you want to disconnect.

## [Usage examples](#usage-examples)

### [Example: Use Claude Desktop as a client](#example-use-claude-desktop-as-a-client)

Imagine you have Claude Desktop installed, and you want to use the GitHub MCP server and the Puppeteer MCP server. You do not have to install the servers in Claude Desktop. You can add these 2 MCP servers to your profile in the MCP Toolkit and connect Claude Desktop as a client:

1. From the **MCP Toolkit** menu, select the **Catalog** tab and find the **Puppeteer** server and add it to your profile.

2. Repeat for the **GitHub Official** server.

3. From the **Clients** tab, select **Connect** next to **Claude Desktop**. Restart Claude Desktop if it's running, and it can now access all the servers in the MCP Toolkit.

4. Within Claude Desktop, run a test by submitting the following prompt using the Sonnet 3.5 model:

   ```text
   Take a screenshot of docs.docker.com and then invert the colors
   ```

### [Example: Use Visual Studio Code as a client](#example-use-visual-studio-code-as-a-client)

You can interact with all your installed MCP servers in Visual Studio Code:

1. To enable the MCP Toolkit:

   1. Insert the following in your Visual Studio Code's User `mcp.json`:

      ```json
      "mcp": {
       "servers": {
         "MCP_DOCKER": {
           "command": "docker",
           "args": [
             "mcp",
             "gateway",
             "run",
             "--profile",
             "my_profile"
           ],
           "type": "stdio"
         }
       }
      }
      ```

   1) In your terminal, navigate to your project's folder.

   2) Run:

      ```bash
      docker mcp client connect vscode --profile my_profile
      ```

      > Note
      >
      > This command creates a `.vscode/mcp.json` file in the current directory that connects VSCode to your profile. As this is a user-specific file, add it to your `.gitignore` file to prevent it from being committed to the repository.
      >
      > ```console
      > echo ".vscode/mcp.json" >> .gitignore
      > ```

2. In Visual Studio Code, open a new Chat and select the **Agent** mode:

3. You can also check the available MCP tools:

For more information about the Agent mode, see the [Visual Studio Code documentation](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode).

## [Further reading](#further-reading)

* [Use MCP Toolkit from the CLI](https://docs.docker.com/ai/mcp-catalog-and-toolkit/cli/)
* [MCP Catalog](https://docs.docker.com/ai/mcp-catalog-and-toolkit/catalog/)
* [MCP Gateway](https://docs.docker.com/ai/mcp-catalog-and-toolkit/mcp-gateway/)

----
url: https://docs.docker.com/reference/cli/docker/mcp/catalog/push/
----

# docker mcp catalog push

***

| Description | Push a catalog to an OCI registry         |
| ----------- | ----------------------------------------- |
| Usage       | `docker mcp catalog push <oci-reference>` |

## [Description](#description)

Push a catalog to an OCI registry

----
url: https://docs.docker.com/enterprise/enterprise-deployment/
----

# Deploy Docker Desktop

***

***

Docker Desktop supports scalable deployment options tailored for enterprise IT environments. Whether you're rolling out Docker across hundreds of developer workstations or enforcing consistent configuration through MDM solutions like Intune or Jamf, this section provides everything you need to install, configure, and manage Docker Desktop in a secure, repeatable way. Learn how to use MSI and PKG installers, configure default settings, control updates, and ensure compliance with your organization's policies—across Windows, macOS, and Linux systems.

### [MSI installer](/enterprise/enterprise-deployment/msi-install-and-configure/)

[Learn how to install Docker Desktop with the MSI installer.](/enterprise/enterprise-deployment/msi-install-and-configure/)

### [PKG installer](/enterprise/enterprise-deployment/pkg-install-and-configure/)

[Learn how to install Docker Desktop with the PKG installer.](/enterprise/enterprise-deployment/pkg-install-and-configure/)

### [MS Store](/enterprise/enterprise-deployment/ms-store/)

[Learn how to install Docker Desktop through the Microsoft Store.](/enterprise/enterprise-deployment/ms-store/)

### [Deploy with Intune](/enterprise/enterprise-deployment/use-intune/)

[Learn how to deploy Docker Desktop on Windows and macOS devices using Microsoft Intune.](/enterprise/enterprise-deployment/use-intune/)

### [Deploy with Jamf Pro](/enterprise/enterprise-deployment/use-jamf-pro/)

[Learn how to deploy Docker Desktop for Mac using Jamf Pro](/enterprise/enterprise-deployment/use-jamf-pro/)

### [Docker Desktop for Microsoft Dev Box](/enterprise/enterprise-deployment/dev-box/)

[Install Docker Desktop for Microsoft Dev Box via the Microsoft Azure Marketlplace](/enterprise/enterprise-deployment/dev-box/)

### [FAQs](/enterprise/enterprise-deployment/faq/)

[Common questions when deploying Docker Desktop](/enterprise/enterprise-deployment/faq/)

----
url: https://docs.docker.com/guides/testcontainers-java-spring-boot-kafka/write-tests/
----

# Write tests with Testcontainers

***

Table of contents

***

To test the Kafka listener, you need a running Kafka broker and a MySQL database, plus a started Spring context. Testcontainers spins up both services in Docker containers and `@DynamicPropertySource` connects them to Spring.

## [Write the test](#write-the-test)

Create `ProductPriceChangedEventHandlerTest.java`:

```java
package com.testcontainers.demo;

import static java.util.concurrent.TimeUnit.SECONDS;
import static org.assertj.core.api.Assertions.assertThat;
import static org.awaitility.Awaitility.await;

import java.math.BigDecimal;
import java.time.Duration;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.test.context.DynamicPropertyRegistry;
import org.springframework.test.context.DynamicPropertySource;
import org.springframework.test.context.TestPropertySource;
import org.testcontainers.kafka.ConfluentKafkaContainer;
import org.testcontainers.junit.jupiter.Container;
import org.testcontainers.junit.jupiter.Testcontainers;

@SpringBootTest
@TestPropertySource(
  properties = {
    "spring.kafka.consumer.auto-offset-reset=earliest",
    "spring.datasource.url=jdbc:tc:mysql:8.0.32:///db",
  }
)
@Testcontainers
class ProductPriceChangedEventHandlerTest {

  @Container
  static final ConfluentKafkaContainer kafka =
    new ConfluentKafkaContainer("confluentinc/cp-kafka:7.8.0");

  @DynamicPropertySource
  static void overrideProperties(DynamicPropertyRegistry registry) {
    registry.add("spring.kafka.bootstrap-servers", kafka::getBootstrapServers);
  }

  @Autowired
  private KafkaTemplate<String, Object> kafkaTemplate;

  @Autowired
  private ProductRepository productRepository;

  @BeforeEach
  void setUp() {
    Product product = new Product(null, "P100", "Product One", BigDecimal.TEN);
    productRepository.save(product);
  }

  @Test
  void shouldHandleProductPriceChangedEvent() {
    ProductPriceChangedEvent event = new ProductPriceChangedEvent(
      "P100",
      new BigDecimal("14.50")
    );

    kafkaTemplate.send("product-price-changes", event.productCode(), event);

    await()
      .pollInterval(Duration.ofSeconds(3))
      .atMost(10, SECONDS)
      .untilAsserted(() -> {
        Optional<Product> optionalProduct = productRepository.findByCode(
          "P100"
        );
        assertThat(optionalProduct).isPresent();
        assertThat(optionalProduct.get().getCode()).isEqualTo("P100");
        assertThat(optionalProduct.get().getPrice())
          .isEqualTo(new BigDecimal("14.50"));
      });
  }
}
```

Here's what the test does:

* `@SpringBootTest` starts the full Spring application context.
* The Testcontainers special JDBC URL (`jdbc:tc:mysql:8.0.32:///db`) in `@TestPropertySource` spins up a MySQL container and configures it as the datasource automatically.
* `@Testcontainers` and `@Container` manage the lifecycle of the Kafka container. `@DynamicPropertySource` registers the Kafka bootstrap servers with Spring so that the producer and consumer connect to the test container.
* `@BeforeEach` creates a `Product` record in the database before each test.
* The test sends a `ProductPriceChangedEvent` to the `product-price-changes` topic using `KafkaTemplate`. Spring Boot converts the object to JSON using `JsonSerializer`.
* Because Kafka message processing is asynchronous, the test uses [Awaitility](http://www.awaitility.org/) to poll every 3 seconds (up to a maximum of 10 seconds) until the product price in the database matches the expected value.
* The property `spring.kafka.consumer.auto-offset-reset` is set to `earliest` so that the listener consumes messages even if they're sent to the topic before the listener is ready. This setting is helpful when running tests.

[Run tests and next steps »](https://docs.docker.com/guides/testcontainers-java-spring-boot-kafka/run-tests/)

----
url: https://docs.docker.com/reference/cli/docker/network/disconnect/
----

# docker network disconnect

***

| Description | Disconnect a container from a network                   |
| ----------- | ------------------------------------------------------- |
| Usage       | `docker network disconnect [OPTIONS] NETWORK CONTAINER` |

## [Description](#description)

Disconnects a container from a network. The container must be running to disconnect it from the network.

## [Options](#options)

| Option        | Default | Description                                      |
| ------------- | ------- | ------------------------------------------------ |
| `-f, --force` |         | Force the container to disconnect from a network |

## [Examples](#examples)

```console
$ docker network disconnect multi-host-network container1
```

----
url: https://docs.docker.com/guides/dotnet/configure-ci-cd/
----

# Configure CI/CD for your .NET application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize a .NET application](https://docs.docker.com/guides/dotnet/containerize/). You must have a [GitHub](https://github.com/signup) account and a verified [Docker](https://hub.docker.com/signup) account to complete this section.

   ```console
   $ git remote set-url origin https://github.com/your-username/your-repository.git
   ```

7. In your local repository on your machine, run the following command to rename the branch to main.

   ```console
   $ git branch -M main
   ```

8. Run the following commands to stage, commit, and then push your local repository to GitHub.

   ```console
   $ git add -A
   $ git commit -m "my first commit"
   $ git push -u origin main
   ```

## [Step two: Set up the workflow](#step-two-set-up-the-workflow)

Set up your GitHub Actions workflow for building, testing, and pushing the image to Docker Hub.

1. Go to your repository on GitHub and then select the **Actions** tab.

2. Select **set up a workflow yourself**.

   This takes you to a page for creating a new GitHub actions workflow file in your repository, under `.github/workflows/main.yml` by default.

3. In the editor window, copy and paste the following YAML configuration.

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
             target: build
             load: true

         - name: Build and push
           uses: docker/build-push-action@v7
           with:
             platforms: linux/amd64,linux/arm64
             push: true
             target: final
             tags: ${{ vars.DOCKER_USERNAME }}/${{ github.event.repository.name }}:latest
   ```

[Test your .NET deployment »](https://docs.docker.com/guides/dotnet/deploy/)

----
url: https://docs.docker.com/engine/swarm/swarm-tutorial/rolling-update/
----

# Apply rolling updates to a service

***

***

In a previous step of the tutorial, you [scaled](https://docs.docker.com/engine/swarm/swarm-tutorial/scale-service/) the number of instances of a service. In this part of the tutorial, you deploy a service based on the Redis 7.4.0 container tag. Then you upgrade the service to use the Redis 7.4.1 container image using rolling updates.

1. If you haven't already, open a terminal and ssh into the machine where you run your manager node. For example, the tutorial uses a machine named `manager1`.

2. Deploy your Redis tag to the swarm and configure the swarm with a 10 second update delay. Note that the following example shows an older Redis tag:

   ```console
   $ docker service create \
     --replicas 3 \
     --name redis \
     --update-delay 10s \
     redis:7.4.0

   0u6a4s31ybk7yw2wyvtikmu50
   ```

   You configure the rolling update policy at service deployment time.

   The `--update-delay` flag configures the time delay between updates to a service task or sets of tasks. You can describe the time `T` as a combination of the number of seconds `Ts`, minutes `Tm`, or hours `Th`. So `10m30s` indicates a 10 minute 30 second delay.

   By default the scheduler updates 1 task at a time. You can pass the `--update-parallelism` flag to configure the maximum number of service tasks that the scheduler updates simultaneously.

   By default, when an update to an individual task returns a state of `RUNNING`, the scheduler schedules another task to update until all tasks are updated. If at any time during an update a task returns `FAILED`, the scheduler pauses the update. You can control the behavior using the `--update-failure-action` flag for `docker service create` or `docker service update`.

3. Inspect the `redis` service:

   ```console
   $ docker service inspect --pretty redis

   ID:             0u6a4s31ybk7yw2wyvtikmu50
   Name:           redis
   Service Mode:   Replicated
    Replicas:      3
   Placement:
    Strategy:	    Spread
   UpdateConfig:
    Parallelism:   1
    Delay:         10s
   ContainerSpec:
    Image:         redis:7.4.0
   Resources:
   Endpoint Mode:  vip
   ```

4. Now you can update the container image for `redis`. The swarm manager applies the update to nodes according to the `UpdateConfig` policy:

   ```console
   $ docker service update --image redis:7.4.1 redis
   redis
   ```

   The scheduler applies rolling updates as follows by default:

   * Stop the first task.
   * Schedule update for the stopped task.
   * Start the container for the updated task.
   * If the update to a task returns `RUNNING`, wait for the specified delay period then start the next task.
   * If, at any time during the update, a task returns `FAILED`, pause the update.

5. Run `docker service inspect --pretty redis` to see the new image in the desired state:

   ```console
   $ docker service inspect --pretty redis

   ID:             0u6a4s31ybk7yw2wyvtikmu50
   Name:           redis
   Service Mode:   Replicated
    Replicas:      3
   Placement:
    Strategy:	    Spread
   UpdateConfig:
    Parallelism:   1
    Delay:         10s
   ContainerSpec:
    Image:         redis:7.4.1
   Resources:
   Endpoint Mode:  vip
   ```

   The output of `service inspect` shows if your update paused due to failure:

   ```console
   $ docker service inspect --pretty redis

   ID:             0u6a4s31ybk7yw2wyvtikmu50
   Name:           redis
   ...snip...
   Update status:
    State:      paused
    Started:    11 seconds ago
    Message:    update paused due to failure or early termination of task 9p7ith557h8ndf0ui9s0q951b
   ...snip...
   ```

   To restart a paused update run `docker service update <SERVICE-ID>`. For example:

   ```console
   $ docker service update redis
   ```

   To avoid repeating certain update failures, you may need to reconfigure the service by passing flags to `docker service update`.

6. Run `docker service ps <SERVICE-ID>` to watch the rolling update:

   ```console
   $ docker service ps redis

   NAME                                   IMAGE        NODE       DESIRED STATE  CURRENT STATE            ERROR
   redis.1.dos1zffgeofhagnve8w864fco      redis:7.4.1  worker1    Running        Running 37 seconds
    \_ redis.1.88rdo6pa52ki8oqx6dogf04fh  redis:7.4.0  worker2    Shutdown       Shutdown 56 seconds ago
   redis.2.9l3i4j85517skba5o7tn5m8g0      redis:7.4.1  worker2    Running        Running About a minute
    \_ redis.2.66k185wilg8ele7ntu8f6nj6i  redis:7.4.0  worker1    Shutdown       Shutdown 2 minutes ago
   redis.3.egiuiqpzrdbxks3wxgn8qib1g      redis:7.4.1  worker1    Running        Running 48 seconds
    \_ redis.3.ctzktfddb2tepkr45qcmqln04  redis:7.4.0  mmanager1  Shutdown       Shutdown 2 minutes ago
   ```

   Before Swarm updates all of the tasks, you can see that some are running `redis:7.4.0` while others are running `redis:7.4.1`. The output above shows the state once the rolling updates are done.

## [Next steps](#next-steps)

Next, you'll learn how to drain a node in the swarm.

[Drain a node](https://docs.docker.com/engine/swarm/swarm-tutorial/drain-node/)

----
url: https://docs.docker.com/reference/cli/docker/container/logs/
----

# docker container logs

***

| Description                                                               | Fetch the logs of a container               |
| ------------------------------------------------------------------------- | ------------------------------------------- |
| Usage                                                                     | `docker container logs [OPTIONS] CONTAINER` |
| AliasesAn alias is a short or memorable alternative for a longer command. | `docker logs`                               |

## [Description](#description)

The `docker logs` command batch-retrieves logs present at the time of execution.

For more information about selecting and configuring logging drivers, refer to [Configure logging drivers](/engine/logging/configure/).

## [Options](#options)

| Option                            | Default | Description                                                                                                   |
| --------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| [`--details`](#details)           |         | Show extra details provided to logs                                                                           |
| [`-f, --follow`](#follow)         |         | Follow log output                                                                                             |
| [`--since`](#since)               |         | Show logs since timestamp (e.g. `2013-01-02T13:23:37Z`) or relative (e.g. `42m` for 42 minutes)               |
| [`-n, --tail`](#tail)             | `all`   | Number of lines to show from the end of the logs                                                              |
| [`-t, --timestamps`](#timestamps) |         | Show timestamps                                                                                               |
| [`--until`](#until)               |         | API 1.35+ Show logs before a timestamp (e.g. `2013-01-02T13:23:37Z`) or relative (e.g. `42m` for 42 minutes)  |

## [Examples](#examples)

### [Stream log output (-f, --follow)](#follow)

The `docker logs --follow` command will continue streaming the new output from the container's `STDOUT` and `STDERR`.

### [Retrieve the last logs (-n, --tail)](#tail)

Passing a negative number or a non-integer to `--tail` is invalid and the value is set to `all` in that case.

### [Retrieve logs with timestamps (-t, --timestamps)](#timestamps)

The `docker logs --timestamps` command will add an [RFC3339Nano timestamp](https://pkg.go.dev/time#RFC3339Nano) , for example `2014-09-16T06:17:46.000000000Z`, to each log entry. To ensure that the timestamps are aligned the nano-second part of the timestamp will be padded with zero when necessary.

### [Retrieve logs with additional attributes (--details)](#details)

The `docker logs --details` command will add on extra attributes, such as environment variables and labels, provided to `--log-opt` when creating the container.

### [Retrieve logs generated since a specific point in time (--since)](#since)

The `--since` option shows only the container logs generated after a given date. You can specify the date as an RFC 3339 date, a UNIX timestamp, or a Go duration string (e.g. `1m30s`, `3h`). Besides RFC3339 date format you may also use RFC3339Nano, `2006-01-02T15:04:05`, `2006-01-02T15:04:05.999999999`, `2006-01-02T07:00`, and `2006-01-02`. The local timezone on the client will be used if you do not provide either a `Z` or a `+-00:00` timezone offset at the end of the timestamp. When providing Unix timestamps enter seconds\[.nanoseconds], where seconds is the number of seconds that have elapsed since January 1, 1970 (midnight UTC/GMT), not counting leap seconds (aka Unix epoch or Unix time), and the optional .nanoseconds field is a fraction of a second no more than nine digits long. You can combine the `--since` option with either or both of the `--follow` or `--tail` options.

### [Retrieve logs until a specific point in time (--until)](#until)

In order to retrieve logs before a specific point in time, run:

```console
$ docker run --name test -d busybox sh -c "while true; do $(echo date); sleep 1; done"
$ date
Tue 14 Nov 2017 16:40:00 CET
$ docker logs -f --until=2s test
Tue 14 Nov 2017 16:40:00 CET
Tue 14 Nov 2017 16:40:01 CET
Tue 14 Nov 2017 16:40:02 CET
```

----
url: https://docs.docker.com/get-started/introduction/get-docker-desktop/
----

# Get Docker Desktop

***

Table of contents

***

## [Explanation](#explanation)

Docker Desktop is the all-in-one package to build images, run containers, and so much more. This guide will walk you through the installation process, enabling you to experience Docker Desktop firsthand.

> **Docker Desktop terms**
>
> Commercial use of Docker Desktop in larger enterprises (more than 250 employees OR more than $10 million USD in annual revenue) requires a [paid subscription](https://www.docker.com/pricing?ref=Docs\&refAction=DocsGetDockerDesktop).

### Docker Desktop for Mac

[Download (Apple Silicon)](https://desktop.docker.com/mac/main/arm64/Docker.dmg?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-mac-arm64) | [Download (Intel)](https://desktop.docker.com/mac/main/amd64/Docker.dmg?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-mac-amd64) | [Install instructions](/desktop/setup/install/mac-install)

### Docker Desktop for Windows

[Download](https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe?utm_source=docker\&utm_medium=webreferral\&utm_campaign=docs-driven-download-windows) | [Install instructions](/desktop/setup/install/windows-install)

### Docker Desktop for Linux

[Install instructions](/desktop/setup/install/linux/)

Once it's installed, complete the setup process and you're all set to run a Docker container.

## [Try it out](#try-it-out)

In this hands-on guide, you will see how to run a Docker container using Docker Desktop.

Follow the instructions to run a container using the CLI.

## [Run your first container](#run-your-first-container)

Open your CLI terminal and start a container by running the `docker run` command:

```console
$ docker run -d -p 8080:80 docker/welcome-to-docker
```

## [Access the frontend](#access-the-frontend)

For this container, the frontend is accessible on port `8080`. To open the website, visit <http://localhost:8080> in your browser.

## [Manage containers using Docker Desktop](#manage-containers-using-docker-desktop)

1. Open Docker Desktop and select the **Containers** field on the left sidebar.

2. You can view information about your container including logs, and files, and even access the shell by selecting the **Exec** tab.

3. Select the **Inspect** field to obtain detailed information about the container. You can perform various actions such as pause, resume, start or stop containers, or explore the **Logs**, **Bind mounts**, **Exec**, **Files**, and **Stats** tabs.

Docker Desktop simplifies container management for developers by streamlining the setup, configuration, and compatibility of applications across different environments, thereby addressing the pain points of environment inconsistencies and deployment challenges.

## [What's next?](#whats-next)

Now that you have Docker Desktop installed and ran your first container, it's time to start developing with containers.

[Develop with containers](https://docs.docker.com/get-started/introduction/develop-with-containers/)

----
url: https://docs.docker.com/engine/install/raspberry-pi-os/
----

# Install Docker Engine on Raspberry Pi OS (32-bit / armhf)

***

Table of contents

***

> Warning
>
> **Raspberry Pi OS 32-bit (armhf) Deprecation**
>
> Docker Engine v28 will be the last major version to support Raspberry Pi OS 32-bit (armhf). Starting with Docker Engine v29, new major versions will no longer provide packages for Raspberry Pi OS 32-bit (armhf).
>
> **Migration options**
>
> * **64-bit ARM:** Install the Debian `arm64` packages (fully supported). See the [Debian installation instructions](https://docs.docker.com/engine/install/debian/).
> * **32-bit ARM (v7):** Install the Debian `armhf` packages (targets ARMv7 CPUs).
>
> **Note:** Older devices based on the ARMv6 architecture are no longer supported by official packages, including:
>
> * Raspberry Pi 1 (Model A/B/A+/B+)
> * Raspberry Pi Zero and Zero W

To get started with Docker Engine on Raspberry Pi OS, make sure you [meet the prerequisites](#prerequisites), and then follow the [installation steps](#installation-methods).

> Important
>
> This installation instruction refers to the 32-bit (armhf) version of Raspberry Pi OS. If you're using the 64-bit (arm64) version, follow the instructions for [Debian](https://docs.docker.com/engine/install/debian/).

## [Prerequisites](#prerequisites)

### [Firewall limitations](#firewall-limitations)

> Warning
>
> Before you install Docker, make sure you consider the following security implications and firewall incompatibilities.

* If you use ufw or firewalld to manage firewall settings, be aware that when you expose container ports using Docker, these ports bypass your firewall rules. For more information, refer to [Docker and ufw](https://docs.docker.com/engine/network/packet-filtering-firewalls/#docker-and-ufw).
* Docker is only compatible with `iptables-nft` and `iptables-legacy`. Firewall rules created with `nft` are not supported on a system with Docker installed. Make sure that any firewall rulesets you use are created with `iptables` or `ip6tables`, and that you add them to the `DOCKER-USER` chain, see [Packet filtering and firewalls](https://docs.docker.com/engine/network/packet-filtering-firewalls/).

### [OS requirements](#os-requirements)

To install Docker Engine, you need one of the following OS versions:

* 32-bit Raspberry Pi OS Bookworm 12 (stable)
* 32-bit Raspberry Pi OS Bullseye 11 (oldstable)

> Warning
>
> Docker Engine v28 is the last major version to support Raspberry Pi OS 32-bit (armhf). Starting with v29, no new packages will be provided for 32-bit Raspberry Pi OS.
>
> Migration options:
>
> * 64-bit ARM: use Debian `arm64` packages; see the [Debian installation instructions](https://docs.docker.com/engine/install/debian/).
> * 32-bit ARM (v7): use Debian `armhf` packages (targets ARMv7 CPUs).
>
> Note: ARMv6-based devices (Raspberry Pi 1 models and Raspberry Pi Zero/Zero W) are not supported by official packages.

```console
$ for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

`apt-get` might report that you have none of these packages installed.

Images, containers, volumes, and networks stored in `/var/lib/docker/` aren't automatically removed when you uninstall Docker. If you want to start with a clean installation, and prefer to clean up any existing data, read the [uninstall Docker Engine](#uninstall-docker-engine) section.

## [Installation methods](#installation-methods)

You can install Docker Engine in different ways, depending on your needs:

* Docker Engine comes bundled with [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/). This is the easiest and quickest way to get started.

* Set up and install Docker Engine from [Docker's `apt` repository](#install-using-the-repository).

* [Install it manually](#install-from-a-package) and manage upgrades manually.

* Use a [convenience script](#install-using-the-convenience-script). Only recommended for testing and development environments.

Apache License, Version 2.0. See [LICENSE](https://github.com/moby/moby/blob/master/LICENSE) for the full license.

### [Install using the `apt` repository](#install-using-the-repository)

Before you install Docker Engine for the first time on a new host machine, you need to set up the Docker `apt` repository. Afterward, you can install and update Docker from the repository.

1. Set up Docker's `apt` repository.

   ```bash
   # Add Docker's official GPG key:
   sudo apt-get update
   sudo apt-get install ca-certificates curl
   sudo install -m 0755 -d /etc/apt/keyrings
   sudo curl -fsSL https://download.docker.com/linux/raspbian/gpg -o /etc/apt/keyrings/docker.asc
   sudo chmod a+r /etc/apt/keyrings/docker.asc

   # Add the repository to Apt sources:
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/raspbian \
     $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
     sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   sudo apt-get update
   ```

2. Install the Docker packages.

   To install the latest version, run:

   ```console
   $ sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   To install a specific version of Docker Engine, start by listing the available versions in the repository:

   ```console
   # List the available versions:
   $ apt-cache madison docker-ce | awk '{ print $3 }'

   5:29.5.3-1~raspbian.12~bookworm
   5:29.5.2-1~raspbian.12~bookworm
   ...
   ```

   Select the desired version and install:

   ```console
   $ VERSION_STRING=5:29.5.3-1~raspbian.12~bookworm
   $ sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
   ```

   > Note
   >
   > After installation, verify that Docker is running:
   >
   > ```console
   > $ sudo systemctl status docker
   > ```
   >
   > If Docker is not running, start it manually:
   >
   > ```console
   > $ sudo systemctl start docker
   > ```

3. Verify that the installation is successful by running the `hello-world` image:

   ```console
   $ sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
> The `docker` user group exists but contains no users, which is why you’re required to use `sudo` to run Docker commands. Continue to [Linux postinstall](/engine/install/linux-postinstall) to allow non-privileged users to run Docker commands and for other optional configuration steps.

#### [Upgrade Docker Engine](#upgrade-docker-engine)

To upgrade Docker Engine, follow step 2 of the [installation instructions](#install-using-the-repository), choosing the new version you want to install.

### [Install from a package](#install-from-a-package)

If you can't use Docker's `apt` repository to install Docker Engine, you can download the `deb` file for your release and install it manually. You need to download a new file each time you want to upgrade Docker Engine.

1. Go to [`https://download.docker.com/linux/raspbian/dists/`](https://download.docker.com/linux/raspbian/dists/).

2. Select your Raspberry Pi OS version in the list.

   ```console
   $ sudo dpkg -i ./containerd.io_<version>_<arch>.deb \
     ./docker-ce_<version>_<arch>.deb \
     ./docker-ce-cli_<version>_<arch>.deb \
     ./docker-buildx-plugin_<version>_<arch>.deb \
     ./docker-compose-plugin_<version>_<arch>.deb
   ```

   > Note
   >
   > After installation, verify that Docker is running:
   >
   > ```console
   > $ sudo systemctl status docker
   > ```
   >
   > If Docker is not running, start it manually:
   >
   > ```console
   > $ sudo systemctl start docker
   > ```

6. Verify that the installation is successful by running the `hello-world` image:

   ```console
   $ sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

You have now successfully installed and started Docker Engine.

> Tip
>
> Receiving errors when trying to run without root?
>
> The `docker` user group exists but contains no users, which is why you’re required to use `sudo` to run Docker commands. Continue to [Linux postinstall](/engine/install/linux-postinstall) to allow non-privileged users to run Docker commands and for other optional configuration steps.

> Tip
>
> Preview script steps before running. You can run the script with the `--dry-run` option to learn what steps the script will run when invoked:
>
> ```console
> $ curl -fsSL https://get.docker.com -o get-docker.sh
> $ sudo sh ./get-docker.sh --dry-run
> ```

This example downloads the script from <https://get.docker.com/> and runs it to install the latest stable release of Docker on Linux:

```console
$ curl -fsSL https://get.docker.com -o get-docker.sh
$ sudo sh get-docker.sh
Executing docker install script, commit: 7cae5f8b0decc17d6571f9f52eb840fbc13b2737
<...>
```

You have now successfully installed and started Docker Engine. The `docker` service starts automatically on Debian based distributions. On `RPM` based distributions, such as CentOS, Fedora or RHEL, you need to start it manually using the appropriate `systemctl` or `service` command. As the message indicates, non-root users can't run Docker commands by default.

> **Use Docker as a non-privileged user, or install in rootless mode?**
>
> The installation script requires `root` or `sudo` privileges to install and use Docker. If you want to grant non-root users access to Docker, refer to the [post-installation steps for Linux](/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user). You can also install Docker without `root` privileges, or configured to run in rootless mode. For instructions on running Docker in rootless mode, refer to [run the Docker daemon as a non-root user (rootless mode)](/engine/security/rootless/).

#### [Install pre-releases](#install-pre-releases)

Docker also provides a convenience script at <https://test.docker.com/> to install pre-releases of Docker on Linux. This script is equal to the script at `get.docker.com`, but configures your package manager to use the test channel of the Docker package repository. The test channel includes both stable and pre-releases (beta versions, release-candidates) of Docker. Use this script to get early access to new releases, and to evaluate them in a testing environment before they're released as stable.

To install the latest version of Docker on Linux from the test channel, run:

```console
$ curl -fsSL https://test.docker.com -o test-docker.sh
$ sudo sh test-docker.sh
```

#### [Upgrade Docker after using the convenience script](#upgrade-docker-after-using-the-convenience-script)

If you installed Docker using the convenience script, you should upgrade Docker using your package manager directly. There's no advantage to re-running the convenience script. Re-running it can cause issues if it attempts to re-install repositories which already exist on the host machine.

## [Uninstall Docker Engine](#uninstall-docker-engine)

1. Uninstall the Docker Engine, CLI, containerd, and Docker Compose packages:

   ```console
   $ sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
   ```

2. Images, containers, volumes, or custom configuration files on your host aren't automatically removed. To delete all images, containers, and volumes:

   ```console
   $ sudo rm -rf /var/lib/docker
   $ sudo rm -rf /var/lib/containerd
   ```

3. Remove source list and keyrings

   ```console
   $ sudo rm /etc/apt/sources.list.d/docker.list
   $ sudo rm /etc/apt/keyrings/docker.asc
   ```

You have to delete any edited configuration files manually.

## [Next steps](#next-steps)

* Continue to [Post-installation steps for Linux](https://docs.docker.com/engine/install/linux-postinstall/).

----
url: https://docs.docker.com/reference/cli/docker/sandbox/network/log/
----

# docker sandbox network log

***

| Description | Show network logs            |
| ----------- | ---------------------------- |
| Usage       | `docker sandbox network log` |

## [Description](#description)

> Warning
>
> The Docker Desktop-integrated `docker sandbox` commands are deprecated and replaced by the standalone [`sbx` CLI](https://docs.docker.com/ai/sandboxes/). This deprecation applies only to the Docker Desktop integration, not to Docker Sandboxes.

Show network logs

## [Options](#options)

| Option                  | Default | Description                           |
| ----------------------- | ------- | ------------------------------------- |
| [`--json`](#json)       |         | Output in JSON format                 |
| [`--limit`](#limit)     |         | Maximum number of log entries to show |
| [`-q, --quiet`](#quiet) |         | Only display log entries              |

## [Examples](#examples)

### [Show network logs](#show-network-logs)

```console
$ docker sandbox network log
2026-01-29T10:15:23Z sandbox=my-sandbox request GET https://api.example.com/data allowed
2026-01-29T10:15:24Z sandbox=my-sandbox request POST https://api.example.com/submit allowed
2026-01-29T10:15:25Z sandbox=my-sandbox request GET https://blocked.example.com/ denied
```

### [Show only log entries (--quiet)](#quiet)

```text
--quiet
```

Suppress headers and only show log entries:

```console
$ docker sandbox network log --quiet
2026-01-29T10:15:23Z sandbox=my-sandbox request GET https://api.example.com/data allowed
2026-01-29T10:15:24Z sandbox=my-sandbox request POST https://api.example.com/submit allowed
```

### [Limit number of entries (--limit)](#limit)

```text
--limit N
```

Show only the last N log entries:

```console
$ docker sandbox network log --limit 10
```

### [JSON output (--json)](#json)

Output logs in JSON format for parsing:

```console
$ docker sandbox network log --json
{
  "entries": [
    {
      "timestamp": "2026-01-29T10:15:23Z",
      "sandbox": "my-sandbox",
      "type": "request",
      "method": "GET",
      "url": "https://api.example.com/data",
      "action": "allowed"
    }
  ]
}
```

----
url: https://docs.docker.com/scout/explore/metrics-exporter/
----

# Docker Scout metrics exporter

***

Table of contents

***

Docker Scout exposes a metrics HTTP endpoint that lets you scrape vulnerability and policy data from Docker Scout, using Prometheus or Datadog. With this you can create your own, self-hosted Docker Scout dashboards for visualizing supply chain metrics.

## [Metrics](#metrics)

The metrics endpoint exposes the following metrics:

| Metric                          | Description                                         | Labels                            | Type  |
| ------------------------------- | --------------------------------------------------- | --------------------------------- | ----- |
| `scout_stream_vulnerabilities`  | Vulnerabilities in a stream                         | `streamName`, `severity`          | Gauge |
| `scout_policy_compliant_images` | Compliant images for a policy in a stream           | `id`, `displayName`, `streamName` | Gauge |
| `scout_policy_evaluated_images` | Total images evaluated against a policy in a stream | `id`, `displayName`, `streamName` | Gauge |

> **Streams**
>
> In Docker Scout, the streams concept is a superset of [environments](https://docs.docker.com/scout/integrations/environment/). Streams include all runtime environments that you've defined, as well as the special `latest-indexed` stream. The `latest-indexed` stream contains the most recently pushed (and analyzed) tag for each repository.
>
> Streams is mostly an internal concept in Docker Scout, with the exception of the data exposed through this metrics endpoint.

## [Creating an access token](#creating-an-access-token)

To export metrics from your organization, first make sure your organization is enrolled in Docker Scout. Then, create a Personal Access Token (PAT) - a secret token that allows the exporter to authenticate with the Docker Scout API.

The PAT does not require any specific permissions, but it must be created by a user who is an owner of the Docker organization. To create a PAT, follow the steps in [Create an access token](https://docs.docker.com/security/access-tokens/).

Once you have created the PAT, store it in a secure location. You will need to provide this token to the exporter when scraping metrics.

## [Prometheus](#prometheus)

This section describes how to scrape the metrics endpoint using Prometheus.

### [Add a job for your organization](#add-a-job-for-your-organization)

In the Prometheus configuration file, add a new job for your organization. The job should include the following configuration; replace `ORG` with your organization name:

```yaml
scrape_configs:
  - job_name: ORG
    metrics_path: /v1/exporter/org/ORG/metrics
    scheme: https
    static_configs:
      - targets:
          - api.scout.docker.com
```

The address in the `targets` field is set to the domain name of the Docker Scout API, `api.scout.docker.com`. Make sure that there's no firewall rule in place preventing the server from communicating with this endpoint.

### [Add bearer token authentication](#add-bearer-token-authentication)

To scrape metrics from the Docker Scout Exporter endpoint using Prometheus, you need to configure Prometheus to use the PAT as a bearer token. The exporter requires the PAT to be passed in the `Authorization` header of the request.

Update the Prometheus configuration file to include the `authorization` configuration block. This block defines the PAT as a bearer token stored in a file:

```yaml
scrape_configs:
  - job_name: $ORG
    authorization:
      type: Bearer
      credentials_file: /etc/prometheus/token
```

The content of the file should be the PAT in plain text:

```console
dckr_pat_...
```

If you are running Prometheus in a Docker container or Kubernetes pod, mount the file into the container using a volume or secret.

Finally, restart Prometheus to apply the changes.

### [Prometheus sample project](#prometheus-sample-project)

If you don't have a Prometheus server set up, you can run a [sample project](https://github.com/dockersamples/scout-metrics-exporter) using Docker Compose. The sample includes a Prometheus server that scrapes metrics for a Docker organization enrolled in Docker Scout, alongside Grafana with a pre-configured dashboard to visualize the vulnerability and policy metrics.

1. Clone the starter template for bootstrapping a set of Compose services for scraping and visualizing the Docker Scout metrics endpoint:

   ```console
   $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
   $ cd scout-metrics-exporter/prometheus
   ```

2. [Create a Docker access token](https://docs.docker.com/security/access-tokens/) and store it in a plain text file at `/prometheus/prometheus/token` under the template directory.

   token

   ```plaintext
   $ echo $DOCKER_PAT > ./prometheus/token
   ```

3. In the Prometheus configuration file at `/prometheus/prometheus/prometheus.yml`, replace `ORG` in the `metrics_path` property on line 6 with the namespace of your Docker organization.

   prometheus/prometheus.yml

   |                                                |                                                                                                                                                                                                                                                                                                                                               |
   | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | ```
    1
    2
    3
    4
    5
    6
    7
    8
    9
   10
   11
   12
   13
   ``` | ```yaml
   global:
     scrape_interval: 60s
     scrape_timeout: 40s
   scrape_configs:
     - job_name: Docker Scout policy
       metrics_path: /v1/exporter/org/ORG/metrics
       scheme: https
       static_configs:
         - targets:
             - api.scout.docker.com
       authorization:
         type: Bearer
         credentials_file: /etc/prometheus/token
   ``` |

4. Start the compose services.

   ```console
   docker compose up -d
   ```

   This command starts two services: the Prometheus server and Grafana. Prometheus scrapes metrics from the Docker Scout endpoint, and Grafana visualizes the metrics using a pre-configured dashboard.

To stop the demo and clean up any resources created, run:

```console
docker compose down -v
```

### [Access to Prometheus](#access-to-prometheus)

After starting the services, you can access the Prometheus expression browser by visiting <http://localhost:9090>. The Prometheus server runs in a Docker container and is accessible on port 9090.

After a few seconds, you should see the metrics endpoint as a target in the Prometheus UI at <http://localhost:9090/targets>.

Docker Scout metrics exporter Prometheus target

### [Viewing the metrics in Grafana](#viewing-the-metrics-in-grafana)

To view the Grafana dashboards, go to <http://localhost:3000/dashboards>, and sign in using the credentials defined in the Docker Compose file (username: `admin`, password: `grafana`).

Vulnerability dashboard in Grafana

Policy dashboard in Grafana

The dashboards are pre-configured to visualize the vulnerability and policy metrics scraped by Prometheus.

## [Datadog](#datadog)

This section describes how to scrape the metrics endpoint using Datadog. Datadog pulls data for monitoring by running a customizable [agent](https://docs.datadoghq.com/agent/?tab=Linux) that scrapes available endpoints for any exposed metrics. The OpenMetrics and Prometheus checks are included in the agent, so you don’t need to install anything else on your containers or hosts.

This guide assumes you have a Datadog account and a Datadog API Key. Refer to the [Datadog documentation](https://docs.datadoghq.com/agent) to get started.

### [Configure the Datadog agent](#configure-the-datadog-agent)

To start collecting the metrics, you will need to edit the agent’s configuration file for the OpenMetrics check. If you're running the agent as a container, such file must be mounted at `/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml`.

The following example shows a Datadog configuration that:

* Specifies the OpenMetrics endpoint targeting the `dockerscoutpolicy` Docker organization
* A `namespace` that all collected metrics will be prefixed with
* The [`metrics`](#metrics) you want the agent to scrape (`scout_*`)
* An `auth_token` section for the Datadog agent to authenticate to the Metrics endpoint, using a Docker PAT as a Bearer token.

```yaml
instances:
  - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/dockerscoutpolicy/metrics"
    namespace: "scout-metrics-exporter"
    metrics:
      - scout_*
    auth_token:
      reader:
        type: file
        path: /var/run/secrets/scout-metrics-exporter/token
      writer:
        type: header
        name: Authorization
        value: Bearer TOKEN
```

> Important
>
> Do not replace the `<TOKEN>` placeholder in the previous configuration example. It must stay as it is. Only make sure the Docker PAT is correctly mounted into the Datadog agent in the specified filesystem path. Save the file as `conf.yaml` and restart the agent.

When creating a Datadog agent configuration of your own, make sure to edit the `openmetrics_endpoint` property to target your organization, by replacing `dockerscoutpolicy` with the namespace of your Docker organization.

### [Datadog sample project](#datadog-sample-project)

If you don't have a Datadog server set up, you can run a [sample project](https://github.com/dockersamples/scout-metrics-exporter) using Docker Compose. The sample includes a Datadog agent, running as a container, that scrapes metrics for a Docker organization enrolled in Docker Scout. This sample project assumes that you have a Datadog account, an API key, and a Datadog site.

1. Clone the starter template for bootstrapping a Datadog Compose service for scraping the Docker Scout metrics endpoint:

   ```console
   $ git clone git@github.com:dockersamples/scout-metrics-exporter.git
   $ cd scout-metrics-exporter/datadog
   ```

2. [Create a Docker access token](https://docs.docker.com/security/access-tokens/) and store it in a plain text file at `/datadog/token` under the template directory.

   token

   ```plaintext
   $ echo $DOCKER_PAT > ./token
   ```

3. In the `/datadog/compose.yaml` file, update the `DD_API_KEY` and `DD_SITE` environment variables with the values for your Datadog deployment.

   ```yaml
     datadog-agent:
       container_name: datadog-agent
       image: gcr.io/datadoghq/agent:7
       environment:
         - DD_API_KEY=${DD_API_KEY} # e.g. 1b6b3a42...
         - DD_SITE=${DD_SITE} # e.g. datadoghq.com
         - DD_DOGSTATSD_NON_LOCAL_TRAFFIC=true
       volumes:
         - /var/run/docker.sock:/var/run/docker.sock:ro
         - ./conf.yaml:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml:ro
         - ./token:/var/run/secrets/scout-metrics-exporter/token:ro
   ```

   The `volumes` section mounts the Docker socket from the host to the container. This is required to obtain an accurate hostname when running as a container ([more details here](https://docs.datadoghq.com/agent/troubleshooting/hostname_containers/)).

   It also mounts the agent's config file and the Docker access token.

4. Edit the `/datadog/config.yaml` file by replacing the placeholder `<ORG>` in the `openmetrics_endpoint` property with the namespace of the Docker organization that you want to collect metrics for.

   ```yaml
   instances:
     - openmetrics_endpoint: "https://api.scout.docker.com/v1/exporter/org/<ORG>/metrics"
       namespace: "scout-metrics-exporter"
   # ...
   ```

5. Start the Compose services.

   ```console
   docker compose up -d
   ```

If configured properly, you should see the OpenMetrics check under Running Checks when you run the agent’s status command whose output should look similar to:

```text
openmetrics (4.2.0)
-------------------
  Instance ID: openmetrics:scout-prometheus-exporter:6393910f4d92f7c2 [OK]
  Configuration Source: file:/etc/datadog-agent/conf.d/openmetrics.d/conf.yaml
  Total Runs: 1
  Metric Samples: Last Run: 236, Total: 236
  Events: Last Run: 0, Total: 0
  Service Checks: Last Run: 1, Total: 1
  Average Execution Time : 2.537s
  Last Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
  Last Successful Execution Date : 2024-05-08 10:41:07 UTC (1715164867000)
```

For a comprehensive list of options, take a look at this [example config file](https://github.com/DataDog/integrations-core/blob/master/openmetrics/datadog_checks/openmetrics/data/conf.yaml.example) for the generic OpenMetrics check.

### [Visualizing your data](#visualizing-your-data)

Once the agent is configured to grab Prometheus metrics, you can use them to build comprehensive Datadog graphs, dashboards, and alerts.

Go into your [Metric summary page](https://app.datadoghq.com/metric/summary?filter=scout_prometheus_exporter) to see the metrics collected from this example. This configuration will collect all exposed metrics starting with `scout_` under the namespace `scout_metrics_exporter`.

The following screenshots show examples of a Datadog dashboard containing graphs about vulnerability and policy compliance for a specific [stream](#stream).

> The reason why the lines in the graphs look flat is due to the own nature of vulnerabilities (they don't change too often) and the short time interval selected in the date picker.

## [Scrape interval](#scrape-interval)

By default, Prometheus and Datadog scrape metrics at a 15 second interval. Because of the own nature of vulnerability data, the metrics exposed through this API are unlikely to change at a high frequency. For this reason, the metrics endpoint has a 60-minute cache by default, which means a scraping interval of 60 minutes or higher is recommended. If you set the scrape interval to less than 60 minutes, you will see the same data in the metrics for multiple scrapes during that time window.

To change the scrape interval:

* Prometheus: set the `scrape_interval` field in the Prometheus configuration file at the global or job level.
* Datadog: set the `min_collection_interval` property in the Datadog agent configuration file, see [Datadog documentation](https://docs.datadoghq.com/developers/custom_checks/write_agent_check/#updating-the-collection-interval).

## [Revoke an access token](#revoke-an-access-token)

If you suspect that your PAT has been compromised or is no longer needed, you can revoke it at any time. To revoke a PAT, follow the steps in the [Create and manage access tokens](https://docs.docker.com/security/access-tokens/).

Revoking a PAT immediately invalidates the token, and prevents Prometheus from scraping metrics using that token. You will need to create a new PAT and update the Prometheus configuration to use the new token.

----
url: https://docs.docker.com/build/ci/
----

# Continuous integration with Docker

***

Table of contents

***

Continuous Integration (CI) is the part of the development process where you're looking to get your code changes merged with the main branch of the project. At this point, development teams run tests and builds to vet that the code changes don't cause any unwanted or unexpected behaviors.

There are several uses for Docker at this stage of development, even if you don't end up packaging your application as a container image.

## [Docker as a build environment](#docker-as-a-build-environment)

Containers are reproducible, isolated environments that yield predictable results. Building and testing your application in a Docker container makes it easier to prevent unexpected behaviors from occurring. Using a Dockerfile, you define the exact requirements for the build environment, including programming runtimes, operating system, binaries, and more.

Using Docker to manage your build environment also eases maintenance. For example, updating to a new version of a programming runtime can be as simple as changing a tag or digest in a Dockerfile. No need to SSH into a pet VM to manually reinstall a newer version and update the related configuration files.

Additionally, just as you expect third-party open source packages to be secure, the same should go for your build environment. You can scan and index a builder image, just like you would for any other containerized application.

The following links provide instructions for how you can get started using Docker for building your applications in CI:

* [GitHub Actions](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action)
* [GitLab](https://docs.gitlab.com/runner/executors/docker.html)
* [Circle CI](https://circleci.com/docs/using-docker/)
* [Render](https://render.com/docs/docker)

### [Docker in Docker](#docker-in-docker)

You can also use a Dockerized build environment to build container images using Docker. That is, your build environment runs inside a container which itself is equipped to run Docker builds. This method is referred to as "Docker in Docker".

Docker provides an official [Docker image](https://hub.docker.com/_/docker) that you can use for this purpose.

## [What's next](#whats-next)

Docker maintains a set of official GitHub Actions that you can use to build, annotate, and push container images on the GitHub Actions platform. See [Introduction to GitHub Actions](https://docs.docker.com/build/ci/github-actions/) to learn more and get started.

----
url: https://docs.docker.com/scout/how-tos/create-exceptions-vex/
----

# Create an exception using the VEX

***

Table of contents

***

Vulnerability Exploitability eXchange (VEX) is a standard format for documenting vulnerabilities in the context of a software package or product. Docker Scout supports VEX documents to create [exceptions](https://docs.docker.com/scout/explore/exceptions/) for vulnerabilities in images.

> Note
>
> You can also create exceptions using the Docker Scout Dashboard or Docker Desktop. The GUI provides a user-friendly interface for creating exceptions, and it's easy to manage exceptions for multiple images. It also lets you create exceptions for multiple images, or your entire organization, all at once. For more information, see [Create an exception using the GUI](https://docs.docker.com/scout/how-tos/create-exceptions-gui/).

## [Prerequisites](#prerequisites)

To create exceptions using OpenVEX documents, you need:

* The latest version of Docker Desktop or the Docker Scout CLI plugin
* The [`vexctl`](https://github.com/openvex/vexctl) command line tool.

Additional requirements depend on how you attach the VEX document:

* The [containerd image store](https://docs.docker.com/desktop/features/containerd/) must be enabled to attach the document as an attestation.
* Write permissions to the registry repository where the image is stored are required to attach the document as an attestation.

## [Introduction to VEX](#introduction-to-vex)

The VEX standard is defined by a working group by the United States Cybersecurity and Infrastructure Security Agency (CISA). At the core of VEX are exploitability assessments. These assessments describe the status of a given CVE for a product. The possible vulnerability statuses in VEX are:

* Not affected: No remediation is required regarding this vulnerability.
* Affected: Actions are recommended to remediate or address this vulnerability.
* Fixed: These product versions contain a fix for the vulnerability.
* Under investigation: It is not yet known whether these product versions are affected by the vulnerability. An update will be provided in a later release.

There are multiple implementations and formats of VEX. Docker Scout supports the [OpenVex](https://github.com/openvex/spec) implementation. Regardless of the specific implementation, the core idea is the same: to provide a framework for describing the impact of vulnerabilities. Key components of VEX regardless of implementation includes:

* VEX document

  A type of security advisory for storing VEX statements. The format of the document depends on the specific implementation.

* VEX statement

  Describes the status of a vulnerability in a product, whether it's exploitable, and whether there are ways to remediate the issue.

* Justification and impact

  Depending on the vulnerability status, statements include a justification or impact statement describing why a product is or isn't affected.

* Action statements

  Describe how to remediate or mitigate the vulnerability.

## [`vexctl` example](#vexctl-example)

The following example command creates a VEX document stating that:

* The software product described by this VEX document is the Docker image `example/app:v1`
* The image contains the npm package `express@4.17.1`
* The npm package is affected by a known vulnerability: `CVE-2022-24999`
* The image is unaffected by the CVE, because the vulnerable code is never executed in containers that run this image

```console
$ vexctl create \
  --author="author@example.com" \
  --product="pkg:docker/example/app@v1" \
  --subcomponents="pkg:npm/express@4.17.1" \
  --vuln="CVE-2022-24999" \
  --status="not_affected" \
  --justification="vulnerable_code_not_in_execute_path" \
  --file="CVE-2022-24999.vex.json"
```

Here's a description of the options in this example:

* `--author`

  The email of the author of the VEX document.

* `--product`

  Package URL (PURL) of the Docker image. A PURL is an identifier for the image in a standardized format, defined in the PURL [specification](https://github.com/package-url/purl-spec/blob/master/PURL-TYPES.rst#docker).

  Docker image PURL strings begin with a `pkg:docker` type prefix, followed by the image repository and version (the image tag or SHA256 digest). Unlike image tags, where the version is specified like `example/app:v1`, in PURL the image repository and version are separated by an `@`.

* `--subcomponents`

  PURL of the vulnerable package in the image. In this example, the vulnerability exists in an npm package, so the `--subcomponents` PURL is the identifier for the npm package name and version (`pkg:npm/express@4.17.1`).

  If the same vulnerability exists in multiple packages, `vexctl` lets you specify the `--subcomponents` flag multiple times for a single `create` command.

  You can also omit `--subcomponents`, in which case the VEX statement applies to the entire image.

* `--vuln`

  ID of the CVE that the VEX statement addresses.

* `--status`

  This is the status label of the vulnerability. This describes the relationship between the software (`--product`) and the CVE (`--vuln`). The possible values for the status label in OpenVEX are:

  * `not_affected`
  * `affected`
  * `fixed`
  * `under_investigation`

  In this example, the VEX statement asserts that the Docker image is `not_affected` by the vulnerability. The `not_affected` status is the only status that results in CVE suppression, where the CVE is filtered out of the analysis results. The other statuses are useful for documentation purposes, but they do not work for creating exceptions. For more information about all the possible status labels, see [Status Labels](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-labels) in the OpenVEX specification.

* `--justification`

  Justifies the `not_affected` status label, informing why the product is not affected by the vulnerability. In this case, the justification given is `vulnerable_code_not_in_execute_path`, signalling that the vulnerability can't be executed as used by the product.

  In OpenVEX, status justifications can have one of the five possible values:

  * `component_not_present`
  * `vulnerable_code_not_present`
  * `vulnerable_code_not_in_execute_path`
  * `vulnerable_code_cannot_be_controlled_by_adversary`
  * `inline_mitigations_already_exist`

  For more information about these values and their definitions, see [Status Justifications](https://github.com/openvex/spec/blob/main/OPENVEX-SPEC.md#status-justifications) in the OpenVEX specification.

* `--file`

  Filename of the VEX document output

## [Example JSON document](#example-json-document)

Here's the OpenVEX JSON generated by this command:

```json
{
  "@context": "https://openvex.dev/ns/v0.2.0",
  "@id": "https://openvex.dev/docs/public/vex-749f79b50f5f2f0f07747c2de9f1239b37c2bda663579f87a35e5f0fdfc13de5",
  "author": "author@example.com",
  "timestamp": "2024-05-27T13:20:22.395824+02:00",
  "version": 1,
  "statements": [
    {
      "vulnerability": {
        "name": "CVE-2022-24999"
      },
      "timestamp": "2024-05-27T13:20:22.395829+02:00",
      "products": [
        {
          "@id": "pkg:docker/example/app@v1",
          "subcomponents": [
            {
              "@id": "pkg:npm/express@4.17.1"
            }
          ]
        }
      ],
      "status": "not_affected",
      "justification": "vulnerable_code_not_in_execute_path"
    }
  ]
}
```

Understanding how VEX documents are supposed to be structured can be a bit of a mouthful. The [OpenVEX specification](https://github.com/openvex/spec) describes the format and all the possible properties of documents and statements. For the full details, refer to the specification to learn more about the available fields and how to create a well-formed OpenVEX document.

To learn more about the available flags and syntax of the `vexctl` CLI tool and how to install it, refer to the [`vexctl` GitHub repository](https://github.com/openvex/vexctl).

## [Verifying VEX documents](#verifying-vex-documents)

To test whether the VEX documents you create are well-formed and produce the expected results, use the `docker scout cves` command with the `--vex-location` flag to apply a VEX document to a local image analysis using the CLI.

The following command invokes a local image analysis that incorporates all VEX documents in the specified location, using the `--vex-location` flag. In this example, the CLI is instructed to look for VEX documents in the current working directory.

```console
$ docker scout cves IMAGE --vex-location .
```

The output of the `docker scout cves` command displays the results with any VEX statements found in under the `--vex-location` location factored into the results. For example, CVEs assigned a status of `not_affected` are filtered out from the results. If the output doesn't seem to take the VEX statements into account, that's an indication that the VEX documents might be invalid in some way.

Things to look out for include:

* The PURL of a Docker image must begin with `pkg:docker/` followed by the image name.
* In a Docker image PURL, the image name and version is separated by `@`. An image named `example/myapp:1.0` has the following PURL: `pkg:docker/example/myapp@1.0`.
* Remember to specify an `author` (it's a mandatory field in OpenVEX)
* The [OpenVEX specification](https://github.com/openvex/spec) describes how and when to use `justification`, `impact_statement`, and other fields in the VEX documents. Specifying these in an incorrect way results in an invalid document. Make sure your VEX documents comply with the OpenVEX specification.

## [Attach VEX documents to images](#attach-vex-documents-to-images)

When you've created a VEX document, you can attach it to your image in the following ways:

* Attach the document as an [attestation](#attestation)
* Embed the document in the [image filesystem](#image-filesystem)

You can't remove a VEX document from an image once it's been added. For documents attached as attestations, you can create a new VEX document and attach it to the image again. Doing so will overwrite the previous VEX document (but it won't remove the attestation). For images where the VEX document has been embedded in the image's filesystem, you need to rebuild the image to change the VEX document.

### [Attestation](#attestation)

To attach VEX documents as an attestation, you can use the `docker scout attestation add` CLI command. Using attestations is the recommended option for attaching exceptions to images when using VEX. This method requires the [containerd image store](https://docs.docker.com/desktop/features/containerd/) and write access to the registry repository where the image is stored.

You can attach attestations to images that have already been pushed to a registry. You don't need to build or push the image again. Additionally, having the exceptions attached to the image as attestations means consumers can inspect the exceptions for an image, directly from the registry.

To attach an attestation to an image:

1. Build the image and push it to a registry.

   ```console
   $ docker build --provenance=true --sbom=true --tag IMAGE --push .
   ```

2. Attach the exception to the image as an attestation.

   ```console
   $ docker scout attestation add \
     --file <cve-id>.vex.json \
     --predicate-type https://openvex.dev/ns/v0.2.0 \
     IMAGE
   ```

   The options for this command are:

   * `--file`: the location and filename of the VEX document
   * `--predicate-type`: the in-toto `predicateType` for OpenVEX

### [Image filesystem](#image-filesystem)

Embedding VEX documents directly on the image filesystem is a good option if you know the exceptions ahead of time, before you build the image. And it's relatively easy; just `COPY` the VEX document to the image in your Dockerfile. Unlike attestations, this method doesn't require the containerd image store or write access to a registry before the image is pushed.

The downside with this approach is that you can't change or update the exception later. Image layers are immutable, so anything you put in the image's filesystem is there forever. Attaching the document as an [attestation](#attestation) provides better flexibility.

> Note
>
> VEX documents embedded in the image filesystem are not considered for images that have attestations. If your image has **any** attestations, Docker Scout will only look for exceptions in the attestations, and not in the image filesystem.
>
> If you want to use the VEX document embedded in the image filesystem, you must remove the attestation from the image. Note that provenance attestations may be added automatically for images. To ensure that no attestations are added to the image, you can explicitly disable both SBOM and provenance attestations using the `--provenance=false` and `--sbom=false` flags when building the image.

To embed a VEX document on the image filesystem, `COPY` the file into the image as part of the image build. The following example shows how to copy all VEX documents under `.vex/` in the build context, to `/var/lib/db` in the image.

```dockerfile
# syntax=docker/dockerfile:1

FROM alpine
COPY .vex/* /var/lib/db/
```

The filename of the VEX document must match the `*.vex.json` glob pattern. It doesn't matter where on the image's filesystem you store the file.

Note that the copied files must be part of the filesystem of the final image, For multi-stage builds, the documents must persist in the final stage.

----
url: https://docs.docker.com/guides/testcontainers-java-replace-h2/
----

# Replace H2 with a real database for testing

Table of contents

***

Replace your H2 in-memory test database with a real PostgreSQL instance using the Testcontainers special JDBC URL — a one-line change.

**Time to complete** 15 minutes

In this guide, you will learn how to:

* Understand the drawbacks of using H2 in-memory databases for testing
* Replace H2 with a real PostgreSQL database using the Testcontainers special JDBC URL
* Use the Testcontainers JUnit 5 extension for more control over the container
* Test both Spring Data JPA and JdbcTemplate-based repositories

## [Prerequisites](#prerequisites)

* Java 17+
* Maven or Gradle
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [The H2 problem](https://docs.docker.com/guides/testcontainers-java-replace-h2/problem-with-h2/)

   Understand why using H2 in-memory databases for testing gives false confidence.

2. [JDBC URL approach](https://docs.docker.com/guides/testcontainers-java-replace-h2/jdbc-url-approach/)

   Use the Testcontainers special JDBC URL to swap H2 for a real PostgreSQL database.

3. [JUnit 5 extension](https://docs.docker.com/guides/testcontainers-java-replace-h2/junit-extension-approach/)

   Use the Testcontainers JUnit 5 extension for more control over the PostgreSQL container.

----
url: https://docs.docker.com/ai/model-runner/ide-integrations/
----

# IDE and tool integrations

***

Table of contents

***

Docker Model Runner can serve as a local backend for popular AI coding assistants and development tools. This guide shows how to configure common tools to use models running in DMR.

## [Prerequisites](#prerequisites)

Before configuring any tool:

1. [Enable Docker Model Runner](https://docs.docker.com/ai/model-runner/get-started/#enable-docker-model-runner) in Docker Desktop or Docker Engine.

2. Enable TCP host access:

   * Docker Desktop: Enable **host-side TCP support** in Settings > AI, or run:
     ```console
     $ docker desktop enable model-runner --tcp 12434
     ```
   * Docker Engine: TCP is enabled by default on port 12434.

3. Pull a model:
   ```console
   $ docker model pull ai/qwen2.5-coder
   ```

> Tip
>
> The default context size for many models (such as `gpt-oss`) is 4,096 tokens, which is limiting for coding tasks. You can repackage it with a larger context window:
>
> ```console
> $ docker model pull gpt-oss
> $ docker model package --from ai/gpt-oss --context-size 32000 gpt-oss:32k
> ```
>
> Alternatively, models like ai/glm-4.7-flash, ai/qwen2.5-coder, and ai/devstral-small-2 come with 128K context by default and work without repackaging.

## [Cline (VS Code)](#cline-vs-code)

[Cline](https://github.com/cline/cline) is an AI coding assistant for VS Code.

### [Configuration](#configuration)

1. Open VS Code and go to the Cline extension settings.
2. Select **OpenAI Compatible** as the API provider.
3. Configure the following settings:

| Setting  | Value                                        |
| -------- | -------------------------------------------- |
| Base URL | `http://localhost:12434/engines/v1`          |
| API Key  | `not-needed` (or any placeholder value)      |
| Model ID | `ai/qwen2.5-coder` (or your preferred model) |

> Important
>
> The base URL must include `/engines/v1` at the end. Do not include a trailing slash.

### [Troubleshooting Cline](#troubleshooting-cline)

If Cline fails to connect:

1. Verify DMR is running:

   ```console
   $ docker model status
   ```

2. Test the endpoint directly:

   ```console
   $ curl http://localhost:12434/engines/v1/models
   ```

3. Check that CORS is configured if running a web-based version:

   * In Docker Desktop Settings > AI, add your origin to **CORS Allowed Origins**

## [Continue (VS Code / JetBrains)](#continue-vs-code--jetbrains)

[Continue](https://continue.dev) is an open-source AI code assistant that works with VS Code and JetBrains IDEs.

### [Configuration](#configuration-1)

Edit your Continue configuration file (`~/.continue/config.json`):

```json
{
  "models": [
    {
      "title": "Docker Model Runner",
      "provider": "openai",
      "model": "ai/qwen2.5-coder",
      "apiBase": "http://localhost:12434/engines/v1",
      "apiKey": "not-needed"
    }
  ]
}
```

### [Using Ollama provider](#using-ollama-provider)

Continue also supports the Ollama provider, which works with DMR:

```json
{
  "models": [
    {
      "title": "Docker Model Runner (Ollama)",
      "provider": "ollama",
      "model": "ai/qwen2.5-coder",
      "apiBase": "http://localhost:12434"
    }
  ]
}
```

## [Cursor](#cursor)

[Cursor](https://cursor.sh) is an AI-powered code editor.

### [Configuration](#configuration-2)

1. Open Cursor Settings (Cmd/Ctrl + ,).

2. Navigate to **Models** > **OpenAI API Key**.

3. Configure:

   | Setting                  | Value                               |
   | ------------------------ | ----------------------------------- |
   | OpenAI API Key           | `not-needed`                        |
   | Override OpenAI Base URL | `http://localhost:12434/engines/v1` |

4. In the model drop-down, enter your model name: `ai/qwen2.5-coder`

> Note
>
> Some Cursor features may require models with specific capabilities (e.g., function calling). Use capable models like `ai/qwen2.5-coder` or `ai/llama3.2` for best results.

## [Zed](#zed)

[Zed](https://zed.dev) is a high-performance code editor with AI features.

### [Configuration](#configuration-3)

Edit your Zed settings (`~/.config/zed/settings.json`):

```json
{
  "language_models": {
    "openai": {
      "api_url": "http://localhost:12434/engines/v1",
      "available_models": [
        {
          "name": "ai/qwen2.5-coder",
          "display_name": "Qwen 2.5 Coder (DMR)",
          "max_tokens": 8192
        }
      ]
    }
  }
}
```

## [Open WebUI](#open-webui)

[Open WebUI](https://github.com/open-webui/open-webui) provides a ChatGPT-like interface for local models.

See [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) for detailed setup instructions.

## [Aider](#aider)

[Aider](https://aider.chat) is an AI pair programming tool for the terminal.

### [Configuration](#configuration-4)

Set environment variables or use command-line flags:

```bash
export OPENAI_API_BASE=http://localhost:12434/engines/v1
export OPENAI_API_KEY=not-needed

aider --model openai/ai/qwen2.5-coder
```

Or in a single command:

```console
$ aider --openai-api-base http://localhost:12434/engines/v1 \
        --openai-api-key not-needed \
        --model openai/ai/qwen2.5-coder
```

## [LangChain](#langchain)

### [Python](#python)

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="not-needed",
    model="ai/qwen2.5-coder"
)

response = llm.invoke("Write a hello world function in Python")
print(response.content)
```

### [JavaScript/TypeScript](#javascripttypescript)

```typescript
import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({
  configuration: {
    baseURL: "http://localhost:12434/engines/v1",
  },
  apiKey: "not-needed",
  modelName: "ai/qwen2.5-coder",
});

const response = await model.invoke("Write a hello world function");
console.log(response.content);
```

## [LlamaIndex](#llamaindex)

```python
from llama_index.llms.openai_like import OpenAILike

llm = OpenAILike(
    api_base="http://localhost:12434/engines/v1",
    api_key="not-needed",
    model="ai/qwen2.5-coder"
)

response = llm.complete("Write a hello world function")
print(response.text)
```

## [OpenCode](#opencode)

[OpenCode](https://opencode.ai/) is an open-source coding assistant designed to integrate directly into developer workflows. It supports multiple model providers and exposes a flexible configuration system that makes it easy to switch between them.

See [Use OpenCode with Docker Model Runner](https://docs.docker.com/guides/opencode-model-runner/) for a task-focused guide that walks through model setup, configuration, and troubleshooting.

### [Configuration](#configuration-5)

1. Install OpenCode (see [docs](https://opencode.ai/docs/#install))
2. Reference DMR in your OpenCode configuration, either globally at `~/.config/opencode/opencode.json` or project specific with a `opencode.json` file in the root of your project
   ```json
   {
     "$schema": "https://opencode.ai/config.json",
     "provider": {
       "dmr": {
         "npm": "@ai-sdk/openai-compatible",
         "name": "Docker Model Runner",
         "options": {
           "baseURL": "http://localhost:12434/v1"
         },
         "models": {
           "ai/qwen2.5-coder": {
             "name": "ai/qwen2.5-coder"
           },
           "ai/llama3.2": {
             "name": "ai/llama3.2"
           }
         }
       }
     }
   }
   ```
3. Select the model you want in OpenCode

You can find more details in [this Docker Blog post](https://www.docker.com/blog/opencode-docker-model-runner-private-ai-coding/)

## [Claude Code](#claude-code)

[Claude Code](https://claude.com/product/claude-code) is [Anthropic's](https://www.anthropic.com/) command-line tool for agentic coding. It lives in your terminal, understands your codebase, and executes routine tasks, explains complex code, and handles Git workflows through natural language commands.

See [Use Claude Code with Docker Model Runner](https://docs.docker.com/guides/claude-code-model-runner/) for a task-focused guide that walks through model setup, configuration, and inspecting requests. To run Claude Code in an isolated Docker Sandbox against a local model, see [Run Claude Code in a Docker Sandbox with Docker Model Runner](https://docs.docker.com/guides/claude-code-sandbox-model-runner/).

### [Configuration](#configuration-6)

1. Install Claude Code (see [docs](https://code.claude.com/docs/en/quickstart#step-1-install-claude-code))

2. Use the `ANTHROPIC_BASE_URL` environment variable to point Claude Code at DMR. On Mac or Linux, you can do this, for example if you want to use the `gpt-oss:32k` model:

   ```bash
   ANTHROPIC_BASE_URL=http://localhost:12434 claude --model qwen2.5-coder
   ```

   On Windows (PowerShell) you can do it like this:

   ```powershell
   $env:ANTHROPIC_BASE_URL="http://localhost:12434"
   claude --model gpt-oss:32k
   ```

> Tip
>
> To avoid setting the variable each time, add it to your shell profile (`~/.bashrc`, `~/.zshrc`, or equivalent):
>
> ```shell
> export ANTHROPIC_BASE_URL=http://localhost:12434
> ```

You can find more details in [this Docker Blog post](https://www.docker.com/blog/run-claude-code-locally-docker-model-runner/)

> Note
>
> While the other integrations on this page use the [OpenAI-compatible API](/ai/model-runner/api-reference/#openai-compatible-api), DMR also exposes a [Anthropic-compatible API](/ai/model-runner/api-reference/#anthropic-compatible-api) used here.

## [Common issues](#common-issues)

### ["Connection refused" errors](#connection-refused-errors)

1. Ensure Docker Model Runner is enabled and running:

   ```console
   $ docker model status
   ```

2. Verify TCP access is enabled:

   ```console
   $ curl http://localhost:12434/engines/v1/models
   ```

3. Check if another service is using port 12434.

4. If you run your tool in WSL and want to connect to DMR on the host via `localhost`, this might not directly work. Configuring WSL to use [mirrored networking](https://learn.microsoft.com/en-us/windows/wsl/networking#mirrored-mode-networking) can solve this.

### ["Model not found" errors](#model-not-found-errors)

1. Verify the model is pulled:

   ```console
   $ docker model list
   ```

2. Use the full model name including namespace (e.g., `ai/qwen2.5-coder`, not just `qwen2.5-coder`).

### [Slow responses or timeouts](#slow-responses-or-timeouts)

1. For first requests, models need to load into memory. Subsequent requests are faster.

2. Consider using a smaller model or adjusting the context size:

   ```console
   $ docker model configure --context-size 4096 ai/qwen2.5-coder
   ```

3. Check available system resources (RAM, GPU memory).

### [CORS errors (web-based tools)](#cors-errors-web-based-tools)

If using browser-based tools, add the origin to CORS allowed origins:

1. Docker Desktop: Settings > AI > CORS Allowed Origins
2. Add your tool's URL (e.g., `http://localhost:3000`)

## [Recommended models by use case](#recommended-models-by-use-case)

| Use case          | Recommended model     | Notes                                                  |
| ----------------- | --------------------- | ------------------------------------------------------ |
| Code completion   | `ai/qwen3-coder`      | Optimized for coding tasks with a large context window |
| Agentic coding    | `ai/devstral-small-2` | Good fit for tools such as Claude Code and OpenCode    |
| General assistant | `ai/llama3.2`         | Good balance of capabilities                           |
| Small/fast        | `ai/smollm2`          | Low resource usage                                     |
| Embeddings        | `ai/all-minilm`       | For RAG and semantic search                            |

## [What's next](#whats-next)

* [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - Full API documentation
* [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Tune model behavior
* [Open WebUI integration](https://docs.docker.com/ai/model-runner/openwebui-integration/) - Set up a web interface

----
url: https://docs.docker.com/scout/integrations/ci/azure/
----

# Integrate Docker Scout with Microsoft Azure DevOps Pipelines

***

***

The following examples runs in an Azure DevOps-connected repository containing a Docker image's definition and contents. Triggered by a commit to the main branch, the pipeline builds the image and uses Docker Scout to create a CVE report.

First, set up the rest of the workflow and set up the variables available to all pipeline steps. Add the following to an *azure-pipelines.yml* file:

```yaml
trigger:
  - main

resources:
  - repo: self

variables:
  tag: "$(Build.BuildId)"
  image: "vonwig/nodejs-service"
```

This sets up the workflow to use a particular container image for the application and tag each new image build with the build ID.

Add the following to the YAML file:

```yaml
stages:
  - stage: Build
    displayName: Build image
    jobs:
      - job: Build
        displayName: Build
        pool:
          vmImage: ubuntu-latest
        steps:
          - task: Docker@2
            displayName: Build an image
            inputs:
              command: build
              dockerfile: "$(Build.SourcesDirectory)/Dockerfile"
              repository: $(image)
              tags: |
                $(tag)
          - task: CmdLine@2
            displayName: Find CVEs on image
            inputs:
              script: |
                # Install the Docker Scout CLI
                curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh -s --
                # Login to Docker Hub required for Docker Scout CLI
                echo $(DOCKER_HUB_PAT) | docker login -u $(DOCKER_HUB_USER) --password-stdin
                # Get a CVE report for the built image and fail the pipeline when critical or high CVEs are detected
                docker scout cves $(image):$(tag) --exit-code --only-severity critical,high
```

This creates the flow mentioned previously. It builds and tags the image using the checked-out Dockerfile, downloads the Docker Scout CLI, and then runs the `cves` command against the new tag to generate a CVE report. It only shows critical or high-severity vulnerabilities.

----
url: https://docs.docker.com/reference/samples/prometheus/
----

# Prometheus samples

| Name                                                                                             | Description                                                                        |
| ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| [Prometheus / Grafana](https://github.com/docker/awesome-compose/tree/master/prometheus-grafana) | A sample Prometheus and Grafana stack.                                             |
| [aspnet-monitoring](https://github.com/dockersamples/aspnet-monitoring)                          | Monitoring ASP.NET Fx applications in Windows Docker containers, using Prometheus. |

----
url: https://docs.docker.com/guides/localstack/
----

[Develop and test AWS Cloud applications using LocalStack and Docker](https://docs.docker.com/guides/localstack/)

This guide explains how to use Docker to run LocalStack, a local AWS cloud stack emulator.

JavaScript Cloud services

20 minutes

[« Back to all guides](/guides/)

# Develop and test AWS Cloud applications using LocalStack and Docker

***

Table of contents

***

In modern application development, testing cloud applications locally before deploying them to a live environment helps you ship faster and with more confidence. This approach involves simulating services locally, identifying and fixing issues early, and iterating quickly without incurring costs or facing the complexities of a full cloud environment. Tools like [LocalStack](https://www.localstack.cloud/) have become invaluable in this process, enabling you to emulate AWS services and containerize applications for consistent, isolated testing environments.

In this guide, you'll learn how to:

* Use Docker to launch up a LocalStack container
* Connect to LocalStack from a non-containerized application
* Connect to LocalStack from a containerized application

## [What is LocalStack?](#what-is-localstack)

LocalStack is a cloud service emulator that runs in a single container on your laptop. It provides a powerful, flexible, and cost-effective way to test and develop AWS-based applications locally.

## [Why use LocalStack?](#why-use-localstack)

Simulating AWS services locally allows you to test how your app interacts with services like S3, Lambda, and DynamoDB without needing to connect to the real AWS cloud. You can quickly iterate on your development, avoiding the cost and complexity of deploying to the cloud during this phase.

By mimicking the behavior of these services locally, LocalStack enables faster feedback loops. Your app can interact with external APIs, but everything runs locally, removing the need to deal with cloud provisioning or network latency.

This makes it easier to validate integrations and test cloud-based scenarios without needing to configure IAM roles or policies in a live environment. You can simulate complex cloud architectures locally and push your changes to AWS only when you’re ready.

## [Using LocalStack with Docker](#using-localstack-with-docker)

The [official Docker image for LocalStack](https://hub.docker.com/r/localstack/localstack) provides a convenient way to run LocalStack on your development machine. It’s free to use and doesn’t require any API key to run. You can even use [LocalStack Docker Extension](https://www.docker.com/blog/develop-your-cloud-app-locally-with-the-localstack-extension/) to use LocalStack with a graphical user interface.

## [Prerequisites](#prerequisites)

The following prerequisites are required to follow along with this how-to guide:

* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Node.js](https://nodejs.org/en/download/package-manager)
* [Python and pip](https://www.python.org/downloads/)
* Basic knowledge of Docker

## [Launching LocalStack](#launching-localstack)

Launch a quick demo of LocalStack by using the following steps:

1. Start by [cloning a sample application](https://github.com/dockersamples/todo-list-localstack-docker). Open the terminal and run the following command:

   ```console
   $ git clone https://github.com/dockersamples/todo-list-localstack-docker
   $ cd todo-list-localstack-docker
   ```

2. Bring up LocalStack

   Run the following command to bring up LocalStack.

   ```console
   $ docker compose -f compose-native.yml up -d
   ```

   This Compose file also includes specifications for a required Mongo database. You can verify the services are up and running by visiting the Docker Desktop Dashboard.

3. Verify that LocalStack is up and running by selecting the container and checking the logs.

4. Creating a Local Amazon S3 Bucket

   When you create a local S3 bucket using LocalStack, you're essentially simulating the creation of an S3 bucket on AWS. This lets you to test and develop applications that interact with S3 without needing an actual AWS account.

   To create Local Amazon S3 bucket, install the [`awscli-local` CLI](https://github.com/localstack/awscli-local) on your system. The `awslocal` command is a thin wrapper around the AWS command line interface for use with LocalStack. It lets you to test and develop against a simulated environment on your local machine without needing to access the real AWS services.

   ```console
   $ pip install awscli-local
   ```

   Create a new S3 bucket within the LocalStack environment with the following command:

   ```console
   $ awslocal s3 mb s3://mysamplebucket
   ```

   The command `s3 mb s3://mysamplebucket` tells the AWS CLI to create a new S3 bucket (mb stands for `make bucket`) named `mysamplebucket`.

   You can verify if the S3 bucket gets created or not by selecting the LocalStack container on the Docker Desktop Dashboard and viewing the logs. The logs indicates that your LocalStack environment is configured correctly and you can now use the `mysamplebucket` for storing and retrieving objects.

## [Using LocalStack in development](#using-localstack-in-development)

Now that you've familiarized yourself with LocalStack, it's time to see it in action. In this demonstration, you'll use a sample application featuring a React frontend and a Node.js backend. This application stack utilizes the following components:

* React: A user-friendly frontend for accessing the todo-list application
* Node: A backend responsible for handling the HTTP requests.
* MongoDB: A database to store all the to-do list data
* LocalStack: Emulates the Amazon S3 service and stores and retrieve images.

## [Connecting to LocalStack from a non-containerized app](#connecting-to-localstack-from-a-non-containerized-app)

Now it’s time to connect your app to LocalStack. The `index.js` file, located in the backend/ directory, serves as the main entry point for the backend application.

The code interacts with LocalStack’s S3 service, which is accessed via the endpoint defined by the `S3_ENDPOINT_URL` environment variable, typically set to `http://localhost:4566` for local development.

The `S3Client` from the AWS SDK is configured to use this LocalStack endpoint, along with test credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) that are also sourced from environment variables. This setup lets the application to perform operations on the locally simulated S3 service as if it were interacting with the real AWS S3, making the code flexible for different environments.

The code uses `multer` and `multer-s3` to handle file uploads. When a user uploads an image through the /upload route, the file is stored directly in the S3 bucket simulated by LocalStack. The bucket name is retrieved from the environment variable `S3_BUCKET_NAME`. Each uploaded file is given a unique name by appending the current timestamp to the original filename. The route then returns the URL of the uploaded file within the local S3 service, making it accessible just as it would be if hosted on a real AWS S3 bucket.

Let’s see it in action. Start by launching the Node.js backend service.

1. Change to the backend/ directory

   ```console
   $ cd backend/
   ```

2. Install the required dependencies:

   ```console
   $ npm install
   ```

3. Setting up AWS environment variables

   The `.env` file located in the backend/ directory already contains placeholder credentials and configuration values that LocalStack uses to emulate AWS services. The `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are placeholder credentials, while `S3_BUCKET_NAME` and `S3_ENDPOINT_URL` are configuration settings. No changes are needed as these values are already correctly set for LocalStack.

   > Tip
   >
   > Given that you’re running Mongo in a Docker container and the backend Node app is running natively on your host, ensure that `MONGODB_URI=mongodb://localhost:27017/todos` is set in your `.env` file.

   ```plaintext
   MONGODB_URI=mongodb://localhost:27017/todos
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   S3_BUCKET_NAME=mysamplebucket
   S3_ENDPOINT_URL=http://localhost:4566
   AWS_REGION=us-east-1
   ```

   While the AWS SDK might typically use environment variables starting with `AWS_`, this specific application directly references the following `S3_*` variables in the index.js file (under the `backend/` directory) to configure the S3Client.

   ```js
   const s3 = new S3Client({
     endpoint: process.env.S3_ENDPOINT_URL, // Use the provided endpoint or fallback to defaults
     credentials: {
       accessKeyId: process.env.AWS_ACCESS_KEY_ID || 'default_access_key', // Default values for development
       secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || 'default_secret_key',  
     },
   });
   ```

4. Start the backend server:

   ```console
   $ node index.js
   ```

   You will see the message that the backend service has successfully started at port 5000.

## [Start the frontend service](#start-the-frontend-service)

To start the frontend service, open a new terminal and follow these steps:

1. Navigate to the `frontend` directory:

   ```console
   $ cd frontend
   ```

2. Install the required dependencies

   ```console
   $ npm install
   ```

3. Start the frontend service

   ```console
   $ npm run dev
   ```

   By now, you should see the following message:

   ```console
   VITE v5.4.2  ready in 110 ms
   ➜  Local: http://localhost:5173/
   ➜  Network: use --host to expose
   ➜  press h + enter to show help
   ```

   You can now access the app via <http://localhost:5173>. Go ahead, and upload an image by choosing an image file and clicking the **Upload** button.

   You can verify the image is uploaded to the S3 bucket by checking the LocalStack container logs:

   The `200` status code signifies that the `putObject` operation, which involves uploading an object to the S3 bucket, was executed successfully within the LocalStack environment. LocalStack logs this entry to provide visibility into the operations being performed. It helps debug and confirm that your application is interacting correctly with the emulated AWS services.

   Since LocalStack is designed to simulate AWS services locally, this log entry shows that your application is functioning as expected when performing cloud operations in a local sandbox environment.

## [Connecting to LocalStack from containerized Node app](#connecting-to-localstack-from-containerized-node-app)

Now that you have learnt how to connect a non-containerized Node.js application to LocalStack, it's time to explore the necessary changes to run the complete application stack in a containerized environment. To achieve this, you will create a Compose file specifying all required services - frontend, backend, database, and LocalStack.

1. Examine the Docker Compose file.

   The following Docker Compose file defines four services: `backend`, `frontend`, `mongodb`, and `localstack`. The `backend` and `frontend` services are your Node.js applications, while `mongodb` provides a database and `localstack` simulates AWS services like S3.

   The `backend` service depends on `localstack` and `mongodb` services, ensuring they are running before it starts. It also uses a .env file for environment variables. The frontend service depends on the backend and sets the API URL. The `mongodb` service uses a persistent volume for data storage, and `localstack` is configured to run the S3 service. This setup lets you to develop and test your application locally with AWS-like services.

   ```yaml
   services:
     backend:
       build:
         context: ./backend
         dockerfile: Dockerfile
       ports:
         - 5000:5000
       depends_on:
         - localstack
         - mongodb
       env_file:
         - backend/.env

     frontend:
       build:
         context: ./frontend
         dockerfile: Dockerfile
       ports:
         - 5173:5173
       depends_on:
         - backend
       environment:
         - REACT_APP_API_URL=http://backend:5000/api

     mongodb:
       image: mongo
       container_name: mongodb
       volumes:
         - mongodbdata:/data/db
       ports:
         - 27017:27017

     localstack:
       image: localstack/localstack
       container_name: localstack
       ports:
         - 4566:4566
       environment:
         - SERVICES=s3
         - GATEWAY_LISTEN=0.0.0.0:4566
       volumes:
         - ./localstack:/etc/localstack/init/ready.d

   volumes:
     mongodbdata:
   ```

2. Modify the `.env` file under the `backend/` directory to have the resources connect using the internal network names.

   > Tip
   >
   > Given the previous Compose file, the app would connect to LocalStack using the hostname `localstack` while Mongo would connect using the hostname `mongodb`.

   ```plaintext
   MONGODB_URI=mongodb://mongodb:27017/todos
   AWS_ACCESS_KEY_ID=test
   AWS_SECRET_ACCESS_KEY=test
   S3_BUCKET_NAME=mysamplebucket
   S3_ENDPOINT_URL=http://localstack:4566
   AWS_REGION=us-east-1
   ```

3. Stop the running services

   Ensure that you stop the Node frontend and backend service from the previous step by pressing “Ctrl+C” in the terminal. Also, you'll need to stop the LocalStack and Mongo containers by selecting them in the Docker Desktop Dashboard and selecting the "Delete" button.

4. Start the application stack by executing the following command at the root of your cloned project directory:

   ```console
   $ docker compose -f compose.yml up -d --build
   ```

   After a brief moment, the application will be up and running.

5. Create an S3 bucket manually

   The AWS S3 bucket is not created beforehand by the Compose file. Run the following command to create a new bucket within the LocalStack environment:

   ```console
   $ awslocal s3 mb s3://mysamplebucket
   ```

   The command creates an S3 bucket named `mysamplebucket`.

   > Tip
   >
   > You can automate this step by placing a shell script (for example, `init.sh`) under the local `./localstack` directory. Make sure the script is executable (`chmod +x ./localstack/init.sh`). LocalStack runs files mounted in `/etc/localstack/init/ready.d` once it is ready. See [LocalStack init hooks](https://docs.localstack.cloud/references/init-hooks/) for more details.

   Open <http://localhost:5173> to access the complete to-do list application and start uploading images to the Amazon S3 bucket.

   > Tip
   >
   > To optimize performance and reduce upload times during development, consider uploading smaller image files. Larger images may take longer to process and could impact the overall responsiveness of the application.

## [Recap](#recap)

This guide has walked you through setting up a local development environment using LocalStack and Docker. You’ve learned how to test AWS-based applications locally, reducing costs and increasing the efficiency of your development workflow.

----
url: https://docs.docker.com/engine/security/protect-access/
----

# Protect the Docker daemon socket

***

Table of contents

***

By default, Docker runs through a non-networked UNIX socket. It can also optionally communicate using SSH or a TLS (HTTPS) socket.

## [Use SSH to protect the Docker daemon socket](#use-ssh-to-protect-the-docker-daemon-socket)

> Note
>
> The given `USERNAME` must have permissions to access the docker socket on the remote machine. Refer to [manage Docker as a non-root user](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user) to learn how to give a non-root user access to the docker socket.

The following example creates a [`docker context`](https://docs.docker.com/engine/manage-resources/contexts/) to connect with a remote `dockerd` daemon on `host1.example.com` using SSH, and as the `docker-user` user on the remote machine:

```console
$ docker context create \
    --docker host=ssh://docker-user@host1.example.com \
    --description="Remote engine" \
    my-remote-engine

my-remote-engine
Successfully created context "my-remote-engine"
```

After creating the context, use `docker context use` to switch the `docker` CLI to use it, and to connect to the remote engine:

```console
$ docker context use my-remote-engine
my-remote-engine
Current context is now "my-remote-engine"

$ docker info
<prints output of the remote engine>
```

Use the `default` context to switch back to the default (local) daemon:

```console
$ docker context use default
default
Current context is now "default"
```

Alternatively, use the `DOCKER_HOST` environment variable to temporarily switch the `docker` CLI to connect to the remote host using SSH. This does not require creating a context, and can be useful to create an ad-hoc connection with a different engine:

```console
$ export DOCKER_HOST=ssh://docker-user@host1.example.com
$ docker info
<prints output of the remote engine>
```

### [SSH Tips](#ssh-tips)

For the best user experience with SSH, configure `~/.ssh/config` as follows to allow reusing a SSH connection for multiple invocations of the `docker` CLI:

```text
ControlMaster     auto
ControlPath       ~/.ssh/control-%C
ControlPersist    yes
```

## [Use TLS (HTTPS) to protect the Docker daemon socket](#use-tls-https-to-protect-the-docker-daemon-socket)

If you need Docker to be reachable through HTTP rather than SSH in a safe manner, you can enable TLS (HTTPS) by specifying the `tlsverify` flag and pointing Docker's `tlscacert` flag to a trusted CA certificate.

In the daemon mode, it only allows connections from clients authenticated by a certificate signed by that CA. In the client mode, it only connects to servers with a certificate signed by that CA.

> Important
>
> Using TLS and managing a CA is an advanced topic. Familiarize yourself with OpenSSL, x509, and TLS before using it in production.

### [Create a CA, server and client keys with OpenSSL](#create-a-ca-server-and-client-keys-with-openssl)

> Note
>
> Replace all instances of `$HOST` in the following example with the DNS name of your Docker daemon's host.

First, on the Docker daemon's host machine, generate CA private and public keys:

```console
$ openssl genrsa -aes256 -out ca-key.pem 4096
Generating RSA private key, 4096 bit long modulus
..............................................................................++
........++
e is 65537 (0x10001)
Enter pass phrase for ca-key.pem:
Verifying - Enter pass phrase for ca-key.pem:

$ openssl req -new -x509 -days 365 -key ca-key.pem -sha256 -out ca.pem
Enter pass phrase for ca-key.pem:
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:Queensland
Locality Name (eg, city) []:Brisbane
Organization Name (eg, company) [Internet Widgits Pty Ltd]:Docker Inc
Organizational Unit Name (eg, section) []:Sales
Common Name (e.g. server FQDN or YOUR name) []:$HOST
Email Address []:Sven@home.org.au
```

Now that you have a CA, you can create a server key and certificate signing request (CSR). Make sure that "Common Name" matches the hostname you use to connect to Docker:

> Note
>
> Replace all instances of `$HOST` in the following example with the DNS name of your Docker daemon's host.

```console
$ openssl genrsa -out server-key.pem 4096
Generating RSA private key, 4096 bit long modulus
.....................................................................++
.................................................................................................++
e is 65537 (0x10001)

$ openssl req -subj "/CN=$HOST" -sha256 -new -key server-key.pem -out server.csr
```

Next, we're going to sign the public key with our CA:

Since TLS connections can be made through IP address as well as DNS name, the IP addresses need to be specified when creating the certificate. For example, to allow connections using `10.10.10.20` and `127.0.0.1`:

```console
$ echo subjectAltName = DNS:$HOST,IP:10.10.10.20,IP:127.0.0.1 >> extfile.cnf
```

Set the Docker daemon key's extended usage attributes to be used only for server authentication:

```console
$ echo extendedKeyUsage = serverAuth >> extfile.cnf
```

Now, generate the signed certificate:

```console
$ openssl x509 -req -days 365 -sha256 -in server.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out server-cert.pem -extfile extfile.cnf
Signature ok
subject=/CN=your.host.com
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

[Authorization plugins](/engine/extend/plugins_authorization/) offer more fine-grained control to supplement authentication from mutual TLS. In addition to other information described in the above document, authorization plugins running on a Docker daemon receive the certificate information for connecting Docker clients.

For client authentication, create a client key and certificate signing request:

> Note
>
> For simplicity of the next couple of steps, you may perform this step on the Docker daemon's host machine as well.

```console
$ openssl genrsa -out key.pem 4096
Generating RSA private key, 4096 bit long modulus
.........................................................++
................++
e is 65537 (0x10001)

$ openssl req -subj '/CN=client' -new -key key.pem -out client.csr
```

To make the key suitable for client authentication, create a new extensions config file:

```console
$ echo extendedKeyUsage = clientAuth > extfile-client.cnf
```

Now, generate the signed certificate:

```console
$ openssl x509 -req -days 365 -sha256 -in client.csr -CA ca.pem -CAkey ca-key.pem \
  -CAcreateserial -out cert.pem -extfile extfile-client.cnf
Signature ok
subject=/CN=client
Getting CA Private Key
Enter pass phrase for ca-key.pem:
```

After generating `cert.pem` and `server-cert.pem` you can safely remove the two certificate signing requests and extensions config files:

```console
$ rm -v client.csr server.csr extfile.cnf extfile-client.cnf
```

With a default `umask` of 022, your secret keys are *world-readable* and writable for you and your group.

To protect your keys from accidental damage, remove their write permissions. To make them only readable by you, change file modes as follows:

```console
$ chmod -v 0400 ca-key.pem key.pem server-key.pem
```

Certificates can be world-readable, but you might want to remove write access to prevent accidental damage:

```console
$ chmod -v 0444 ca.pem server-cert.pem cert.pem
```

Now you can make the Docker daemon only accept connections from clients providing a certificate trusted by your CA:

```console
$ dockerd \
    --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=server-cert.pem \
    --tlskey=server-key.pem \
    -H=0.0.0.0:2376
```

To connect to Docker and validate its certificate, provide your client keys, certificates and trusted CA:

> Tip
>
> This step should be run on your Docker client machine. As such, you need to copy your CA certificate, your server certificate, and your client certificate to that machine.

> Note
>
> Replace all instances of `$HOST` in the following example with the DNS name of your Docker daemon's host.

```console
$ docker --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=cert.pem \
    --tlskey=key.pem \
    -H=$HOST:2376 version
```

> Note
>
> Docker over TLS should run on TCP port 2376.

> Warning
>
> As shown in the example above, you don't need to run the `docker` client with `sudo` or the `docker` group when you use certificate authentication. That means anyone with the keys can give any instructions to your Docker daemon, giving them root access to the machine hosting the daemon. Guard these keys as you would a root password!

### [Secure by default](#secure-by-default)

If you want to secure your Docker client connections by default, you can move the files to the `.docker` directory in your home directory --- and set the `DOCKER_HOST` and `DOCKER_TLS_VERIFY` variables as well (instead of passing `-H=tcp://$HOST:2376` and `--tlsverify` on every call).

```console
$ mkdir -pv ~/.docker
$ cp -v {ca,cert,key}.pem ~/.docker

$ export DOCKER_HOST=tcp://$HOST:2376 DOCKER_TLS_VERIFY=1
```

Docker now connects securely by default:

```
$ docker ps
```

### [Other modes](#other-modes)

If you don't want to have complete two-way authentication, you can run Docker in various other modes by mixing the flags.

#### [Daemon modes](#daemon-modes)

* `tlsverify`, `tlscacert`, `tlscert`, `tlskey` set: Authenticate clients
* `tls`, `tlscert`, `tlskey`: Do not authenticate clients

#### [Client modes](#client-modes)

* `tls`: Authenticate server based on public/default CA pool
* `tlsverify`, `tlscacert`: Authenticate server based on given CA
* `tls`, `tlscert`, `tlskey`: Authenticate with client certificate, do not authenticate server based on given CA
* `tlsverify`, `tlscacert`, `tlscert`, `tlskey`: Authenticate with client certificate and authenticate server based on given CA

If found, the client sends its client certificate, so you just need to drop your keys into `~/.docker/{ca,cert,key}.pem`. Alternatively, if you want to store your keys in another location, you can specify that location using the environment variable `DOCKER_CERT_PATH`.

```console
$ export DOCKER_CERT_PATH=~/.docker/zone1/
$ docker --tlsverify ps
```

#### [Connecting to the secure Docker port using `curl`](#connecting-to-the-secure-docker-port-using-curl)

To use `curl` to make test API requests, you need to use three extra command line flags:

```console
$ curl https://$HOST:2376/images/json \
  --cert ~/.docker/cert.pem \
  --key ~/.docker/key.pem \
  --cacert ~/.docker/ca.pem
```

## [Related information](#related-information)

* [Using certificates for repository client verification](https://docs.docker.com/engine/security/certificates/)
* [Use trusted images](https://docs.docker.com/engine/security/trust/)

----
url: https://docs.docker.com/desktop/use-desktop/container/
----

# Explore the Containers view in Docker Desktop

***

Table of contents

***

The **Containers** view lists all running and stopped containers and applications. It provides a clean interface to manage the lifecycle of your containers, interact with running applications, and inspect Docker objects—including Docker Compose apps.

## [Container actions](#container-actions)

Use the **Search** field to find a specific container by name.

From the **Containers** view you can:

* Start, stop, pause, resume, or restart containers
* View image packages and CVEs
* Delete containers
* Open the application in VS code
* Open the port exposed by the container in a browser
* Copy the `docker run` command for reuse or modification
* Use [Docker Debug](#execdebug)

## [Resource usage](#resource-usage)

From the **Containers** view you can monitor your containers' CPU and memory usage over time. This can help you understand if something is wrong with your containers or if you need to allocate additional resources.

When you [inspect a container](#inspect-a-container), the **Stats** tab displays further information about a container's resource utilization. You can see how much CPU, memory, network and disk space your container is using over time.

## [Inspect a container](#inspect-a-container)

You can obtain detailed information about the container when you select it.

From here, you can use the quick action buttons to perform various actions such as pause, resume, start or stop, or explore the **Logs**, **Inspect**, **Bind mounts**, **Debug**, **Files**, and **Stats** tabs.

### [Logs](#logs)

Select **Logs** to view output from the container in real time. While viewing logs, you can:

* Use `Cmd + f`/`Ctrl + f` to open the search bar and find specific entries. Search matches are highlighted in yellow.
* Press `Enter` or `Shift + Enter` to jump to the next or previous search match respectively.
* Use the **Copy** icon in the top right-hand corner to copy all the logs to your clipboard.
* Show timestamps
* Use the **Clear terminal** icon in the top right-hand corner to clear the logs terminal.
* Select and view external links that may be in your logs.

You can refine your view by:

* Filtering logs for specific containers, if you're running a multi-container application.
* Using regular expressions or exact match search terms

### [Inspect](#inspect)

Select **Inspect** to view low-level information about the container. It displays the local path, version number of the image, SHA-256, port mapping, and other details.

### [Exec/Debug](#execdebug)

If you have not enabled Docker Debug in settings, the **Exec** tab displays. It lets you quickly run commands within your running container.

Using the **Exec** tab is the same as running one of the following commands:

* `docker exec -it <container-id> /bin/sh`
* `docker exec -it <container-id> cmd.exe` when accessing Windows containers

For more details, see the [`docker exec` CLI reference](/reference/cli/docker/container/exec/).

If you have enabled Docker Debug in settings, or toggled on **Debug mode** to the right of the tab options, the **Debug** tab displays.

Debug mode has several advantages, such as:

* A customizable toolbox. The toolbox comes with many standard Linux tools pre-installed, such as `vim`, `nano`, `htop`, and `curl`. For more details, see the [`docker debug` CLI reference](/reference/cli/docker/debug/).
* The ability to access containers that don't have a shell, for example, slim or distroless containers.

To use debug mode:

* Hover over your running container and under the **Actions** column, select the **Show container actions** menu. From the drop-down menu, select **Use Docker Debug**.
* Or, select the container and then select the **Debug** tab.

To use debug mode by default, navigate to the **General** tab in **Settings** and select the **Enable Docker Debug by default** option.

### [Files](#files)

Select **Files** to explore the filesystem of running or stopped containers. You can also:

* See which files have been recently added, modified, or deleted
* Edit a file straight from the built-in editor
* Drag and drop files and folders between the host and the container
* Delete unnecessary files when you right-click on a file
* Download files and folders from the container straight to the host

## [Additional resources](#additional-resources)

* [What is a container](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/)
* [Run multi-container applications](https://docs.docker.com/get-started/docker-concepts/running-containers/multi-container-applications/)

----
url: https://docs.docker.com/get-started/workshop/03_updating_app/
----

# Update the application

***

Table of contents

***

In [part 1](https://docs.docker.com/get-started/workshop/02_our_app/), you containerized a todo application. In this part, you'll update the application and image. You'll also learn how to stop and remove a container.

## [Update the source code](#update-the-source-code)

In the following steps, you'll change the "empty text" when you don't have any todo list items to "You have no todo items yet! Add one above!"

1. In the `src/static/js/app.js` file, update line 56 to use the new empty text.

   ```diff
   - <p className="text-center">No items yet! Add one above!</p>
   + <p className="text-center">You have no todo items yet! Add one above!</p>
   ```

2. Build your updated version of the image, using the `docker build` command.

   ```console
   $ docker build -t getting-started .
   ```

3. Start a new container using the updated code.

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

You probably saw an error like this:

```console
docker: Error response from daemon: driver failed programming external connectivity on endpoint laughing_burnell 
(bb242b2ca4d67eba76e79474fb36bb5125708ebdabd7f45c8eaf16caaabde9dd): Bind for 127.0.0.1:3000 failed: port is already allocated.
```

The error occurred because you aren't able to start the new container while your old container is still running. The reason is that the old container is already using the host's port 3000 and only one process on the machine (containers included) can listen to a specific port. To fix this, you need to remove the old container.

## [Remove the old container](#remove-the-old-container)

To remove a container, you first need to stop it. Once it has stopped, you can remove it. You can remove the old container using the CLI or Docker Desktop's graphical interface. Choose the option that you're most comfortable with.

### [Remove a container using the CLI](#remove-a-container-using-the-cli)

1. Get the ID of the container by using the `docker ps` command.

   ```console
   $ docker ps
   ```

2. Use the `docker stop` command to stop the container. Replace `<the-container-id>` with the ID from `docker ps`.

   ```console
   $ docker stop <the-container-id>
   ```

3. Once the container has stopped, you can remove it by using the `docker rm` command.

   ```console
   $ docker rm <the-container-id>
   ```

> Note
>
> You can stop and remove a container in a single command by adding the `force` flag to the `docker rm` command. For example: `docker rm -f <the-container-id>`

### [Remove a container using Docker Desktop](#remove-a-container-using-docker-desktop)

1. Open Docker Desktop to the **Containers** view.
2. Select the trash can icon under the **Actions** column for the container that you want to delete.
3. In the confirmation dialog, select **Delete forever**.

### [Start the updated app container](#start-the-updated-app-container)

1. Now, start your updated app using the `docker run` command.

   ```console
   $ docker run -dp 127.0.0.1:3000:3000 getting-started
   ```

2. Refresh your browser on <http://localhost:3000> and you should see your updated help text.

## [Summary](#summary)

In this section, you learned how to update and rebuild an image, as well as how to stop and remove a container.

Related information:

* [docker CLI reference](/reference/cli/docker/)

## [Next steps](#next-steps)

Next, you'll learn how to share images with others.

[Share the application](https://docs.docker.com/get-started/workshop/04_sharing_app/)

----
url: https://docs.docker.com/ai/docker-agent/integrations/
----

# Integrations

***

Table of contents

***

Agents created with Docker Agent can integrate with different environments depending on how you want to use them. Each integration type serves a specific purpose.

## [Integration types](#integration-types)

### [ACP - Editor integration](#acp---editor-integration)

Run agents directly in your editor (Neovim, Zed). The agent sees your editor's file context and can read and modify files through the editor's interface. Use ACP when you want an AI coding assistant embedded in your editor.

See [ACP integration](https://docs.docker.com/ai/docker-agent/integrations/acp/) for setup instructions.

### [MCP - Tool integration](#mcp---tool-integration)

Expose agents as tools in MCP clients like Claude Desktop or Claude Code. Your agents appear in the client's tool list, and the client can call them when needed. Use MCP when you want Claude Desktop (or another MCP client) to have access to your specialized agents.

See [MCP integration](https://docs.docker.com/ai/docker-agent/integrations/mcp/) for setup instructions.

### [A2A - Agent-to-agent communication](#a2a---agent-to-agent-communication)

Run agents as HTTP servers that other agents or systems can call using the Agent-to-Agent protocol. Your agent becomes a service that other systems can discover and invoke over the network. Use A2A when you want to build multi-agent systems or expose your agent as an HTTP service.

See [A2A integration](https://docs.docker.com/ai/docker-agent/integrations/a2a/) for setup instructions.

## [Choosing the right integration](#choosing-the-right-integration)

| Feature       | ACP                | MCP                | A2A                  |
| ------------- | ------------------ | ------------------ | -------------------- |
| Use case      | Editor integration | Agents as tools    | Agent-to-agent calls |
| Transport     | stdio              | stdio/SSE          | HTTP                 |
| Discovery     | Editor plugin      | Server manifest    | Agent card           |
| Best for      | Code editing       | Tool integration   | Multi-agent systems  |
| Communication | Editor calls agent | Client calls tools | Between agents       |

Choose ACP if you want your agent embedded in your editor while you code. Choose MCP if you want Claude Desktop (or another MCP client) to be able to call your specialized agents as tools. Choose A2A if you're building multi-agent systems where agents need to call each other over HTTP.

----
url: https://docs.docker.com/reference/cli/docker/buildx/history/logs/
----

# docker buildx history logs

***

| Description | Print the logs of a build record             |
| ----------- | -------------------------------------------- |
| Usage       | `docker buildx history logs [OPTIONS] [REF]` |

## [Description](#description)

Print the logs for a completed build. The output appears in the same format as `--progress=plain`, showing the full logs for each step.

By default, this shows logs for the most recent build on the current builder.

You can also specify an earlier build using an offset. For example:

* `^1` shows logs for the build before the most recent
* `^2` shows logs for the build two steps back

## [Options](#options)

| Option                    | Default | Description                                       |
| ------------------------- | ------- | ------------------------------------------------- |
| [`--progress`](#progress) | `plain` | Set type of progress output (plain, rawjson, tty) |

## [Examples](#examples)

### [Print logs for the most recent build](#print-logs-for-the-most-recent-build)

```console
$ docker buildx history logs
#1 [internal] load build definition from Dockerfile
#1 transferring dockerfile: 31B done
#1 DONE 0.0s
#2 [internal] load .dockerignore
#2 transferring context: 2B done
#2 DONE 0.0s
...
```

By default, this shows logs for the most recent build on the current builder.

### [Print logs for a specific build](#print-logs-for-a-specific-build)

To print logs for a specific build, use a build ID or offset:

```console
# Using a build ID
docker buildx history logs qu2gsuo8ejqrwdfii23xkkckt

# Or using a relative offset
docker buildx history logs ^1
```

### [Set type of progress output (--progress)](#progress)

```console
$ docker buildx history logs ^1 --progress rawjson
{"id":"buildx_step_1","status":"START","timestamp":"2024-05-01T12:34:56.789Z","detail":"[internal] load build definition from Dockerfile"}
{"id":"buildx_step_1","status":"COMPLETE","timestamp":"2024-05-01T12:34:57.001Z","duration":212000000}
...
```

----
url: https://docs.docker.com/build/ci/github-actions/
----

# Docker Build GitHub Actions

***

Table of contents

***

GitHub Actions is a popular CI/CD platform for automating your build, test, and deployment pipeline. Docker provides a set of official GitHub Actions for you to use in your workflows. These official actions are reusable, easy-to-use components for building, annotating, and pushing images.

The following GitHub Actions are available:

* [Build and push Docker images](https://github.com/marketplace/actions/build-and-push-docker-images): build and push Docker images with BuildKit.
* [Docker Buildx Bake](https://github.com/marketplace/actions/docker-buildx-bake): enables using high-level builds with [Bake](https://docs.docker.com/build/bake/).
* [Docker Login](https://github.com/marketplace/actions/docker-login): sign in to a Docker registry.
* [Docker Setup Buildx](https://github.com/marketplace/actions/docker-setup-buildx): creates and boots a BuildKit builder.
* [Docker Metadata action](https://github.com/marketplace/actions/docker-metadata-action): extracts metadata from Git reference and GitHub events to generate tags, labels, and annotations.
* [Docker Setup Compose](https://github.com/marketplace/actions/docker-setup-compose): installs and sets up [Compose](https://docs.docker.com/compose/).
* [Docker Setup Docker](https://github.com/marketplace/actions/docker-setup-docker): installs Docker Engine.
* [Docker Setup QEMU](https://github.com/marketplace/actions/docker-setup-qemu): installs [QEMU](https://github.com/qemu/qemu) static binaries for multi-platform builds.
* [Docker Scout](https://github.com/docker/scout-action): analyze Docker images for security vulnerabilities.

Using Docker's actions provides an easy-to-use interface, while still allowing flexibility for customizing build parameters.

## [Examples](#examples)

If you're looking for examples on how to use the Docker GitHub Actions, refer to the following sections:

* [Add image annotations with GitHub Actions](/build/ci/github-actions/annotations/)

* [Add SBOM and provenance attestations with GitHub Actions](/build/ci/github-actions/attestations/)

* [Validating build configuration with GitHub Actions](/build/ci/github-actions/checks/)

* [Using secrets with GitHub Actions](/build/ci/github-actions/secrets/)

* [GitHub Actions build summary](/build/ci/github-actions/build-summary/)

* [Configuring your GitHub Actions builder](/build/ci/github-actions/configure-builder/)

* [Cache management with GitHub Actions](/build/ci/github-actions/cache/)

* [Copy image between registries with GitHub Actions](/build/ci/github-actions/copy-image-registries/)

* [Export to Docker with GitHub Actions](/build/ci/github-actions/export-docker/)

* [Docker GitHub Builder](/build/ci/github-actions/github-builder/)

* [Local registry with GitHub Actions](/build/ci/github-actions/local-registry/)

* [Multi-platform image with GitHub Actions](/build/ci/github-actions/multi-platform/)

* [Named contexts with GitHub Actions](/build/ci/github-actions/named-contexts/)

* [Push to multiple registries with GitHub Actions](/build/ci/github-actions/push-multi-registries/)

* [Reproducible builds with GitHub Actions](/build/ci/github-actions/reproducible-builds/)

* [Share built image between jobs with GitHub Actions](/build/ci/github-actions/share-image-jobs/)

* [Manage tags and labels with GitHub Actions](/build/ci/github-actions/manage-tags-labels/)

* [Test before push with GitHub Actions](/build/ci/github-actions/test-before-push/)

* [Update Docker Hub description with GitHub Actions](/build/ci/github-actions/update-dockerhub-desc/)

## [Get started with GitHub Actions](#get-started-with-github-actions)

The [Introduction to GitHub Actions with Docker](https://docs.docker.com/guides/gha/) guide walks you through the process of setting up and using Docker GitHub Actions for building Docker images, and pushing images to Docker Hub.

----
url: https://docs.docker.com/reference/cli/sbx/create/kiro/
----

# sbx create kiro

| Description | Create a sandbox for kiro                |
| ----------- | ---------------------------------------- |
| Usage       | `sbx create kiro PATH [PATH...] [flags]` |

## [Description](#description)

Create a sandbox with access to a host workspace for kiro.

The workspace path is required and will be mounted inside the sandbox at the same path as on the host. Additional workspaces can be provided as extra arguments. Append ":ro" to mount them read-only.

Use "sbx run --name SANDBOX" to attach to the agent after creation.

## [Global options](#global-options)

| Option           | Default | Description                                                                                                                                                                                                            |
| ---------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--clone`        |         | Run the agent on a private in-container clone of the host Git repository (mounted read-only) instead of bind-mounting the workspace; the agent's commits are accessible via the sandbox-\<name> git remote on the host |
| `--cpus`         | `0`     | Number of CPUs to allocate to the sandbox (0 = auto: N-1 host CPUs, min 1)                                                                                                                                             |
| `-D, --debug`    |         | Enable debug logging                                                                                                                                                                                                   |
| `--kit`          |         | experimental Kit reference (directory, ZIP, or OCI). Can be specified multiple times                                                                                                                                   |
| `-m, --memory`   |         | Memory limit in binary units (e.g., 1024m, 8g). Default: 50% of host memory, max 32 GiB                                                                                                                                |
| `--name`         |         | Name for the sandbox (default: \<agent>-\<workdir>, letters, numbers, hyphens, periods, plus signs and minus signs only)                                                                                               |
| `-q, --quiet`    |         | Suppress verbose output                                                                                                                                                                                                |
| `-t, --template` |         | Container image to use for the sandbox (default: agent-specific image)                                                                                                                                                 |

## [Examples](#examples)

```console
# Create in the current directory
sbx create kiro .

# Create with a specific path
sbx create kiro /path/to/project

# Create with additional read-only workspaces
sbx create kiro . /path/to/docs:ro
```

----
url: https://docs.docker.com/guides/angular/containerize/
----

# Containerize an Angular Application

***

Table of contents

***

## [Prerequisites](#prerequisites)

Before you begin, make sure the following tools are installed and available on your system:

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
* You have a [git client](https://git-scm.com/downloads). The examples in this section use a command-line based git client, but you can use any client.

> **New to Docker?**\
> Start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide to get familiar with key concepts like images, containers, and Dockerfiles.

***

## [Overview](#overview)

This guide walks you through the complete process of containerizing an Angular application with Docker. You’ll learn how to create a production-ready Docker image using best practices that improve performance, security, scalability, and deployment efficiency.

By the end of this guide, you will:

* Containerize an Angular application using Docker.
* Create and optimize a Dockerfile for production builds.
* Use multi-stage builds to minimize image size.
* Serve the application efficiently with a custom Nginx configuration.
* Build secure and maintainable Docker images by following best practices.

***

## [Get the sample application](#get-the-sample-application)

Clone the sample application to use with this guide. Open a terminal, navigate to the directory where you want to work, and run the following command to clone the git repository:

```console
$ git clone https://github.com/kristiyan-velkov/docker-angular-sample
```

***

## [Build the Docker image](#build-the-docker-image)

Angular is a front-end framework that compiles into static assets, so the Dockerfile uses a multi-stage build: one stage compiles the app with Node.js, and a second minimal stage serves the static output with Nginx.

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

### [Step 1: Create the Dockerfile](#step-1-create-the-dockerfile)

Before creating a Dockerfile, you need to choose a base image. You can either use the [Node.js Official Image](https://hub.docker.com/_/node) or a Docker Hardened Image (DHI) from the [Hardened Image catalog](https://hub.docker.com/hardened-images/catalog).

Choosing DHI offers the advantage of a production-ready image that is lightweight and secure. For more information, see [Docker Hardened Images](https://docs.docker.com/dhi/).

> Important
>
> This guide uses a stable Node.js LTS image tag that is considered secure when the guide is written. Because new releases and security patches are published regularly, the tag shown here may no longer be the safest option when you follow the guide. Always review the latest available image tags and select a secure, up-to-date version before building or deploying your application.
>
> Official Node.js Docker Images: <https://hub.docker.com/_/node>

Docker Hardened Images (DHIs) are available for Node.js in the [Docker Hardened Images catalog](https://hub.docker.com/hardened-images/catalog/dhi/node). Docker Hardened Images are freely available to everyone with no subscription required. You can pull and use them like any other Docker image after signing in to the DHI registry. For more information, see the [DHI quickstart](/dhi/get-started/) guide.

1. Sign in to the DHI registry:

   ```console
   $ docker login dhi.io
   ```

2. Pull the Node.js DHI (check the catalog for available versions):

   ```console
   $ docker pull dhi.io/node:24-alpine3.22-dev
   ```

In the following Dockerfile, the `FROM` instruction uses `dhi.io/node:24-alpine3.22-dev` as the base image.

```dockerfile
# =========================================
# Stage 1: Build the Angular Application
# =========================================

# Use a lightweight DHI Node.js image for building
FROM dhi.io/node:24-alpine3.22-dev AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Angular application
RUN npm run build 

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM dhi.io/nginx:1.28.0-alpine3.21-dev AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# Use a non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80 
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

Create a file named `Dockerfile` with the following contents:

```dockerfile
# =========================================
# Stage 1: Build the Angular Application
# =========================================
ARG NODE_VERSION=24.12.0-alpine
ARG NGINX_VERSION=alpine3.22

# Use a lightweight Node.js image for building (customizable via ARG)
FROM node:${NODE_VERSION} AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package-related files first to leverage Docker's caching mechanism
COPY package.json *package-lock.json* ./

# Install project dependencies using npm ci (ensures a clean, reproducible install)
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application source code into the container
COPY . .

# Build the Angular application
RUN npm run build 

# =========================================
# Stage 2: Prepare Nginx to Serve Static Files
# =========================================

FROM nginxinc/nginx-unprivileged:${NGINX_VERSION} AS runner

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the static build output from the build stage to Nginx's default HTML serving directory
COPY --chown=nginx:nginx --from=builder /app/dist/*/browser /usr/share/nginx/html

# Use a built-in non-root user for security best practices
USER nginx

# Expose port 8080 to allow HTTP traffic
# Note: The default Nginx container now listens on port 8080 instead of 80 
EXPOSE 8080

# Start Nginx directly with custom config
ENTRYPOINT ["nginx", "-c", "/etc/nginx/nginx.conf"]
CMD ["-g", "daemon off;"]
```

> Note
>
> We are using nginx-unprivileged instead of the standard Nginx image to follow security best practices. Running as a non-root user in the final image:
>
> * Reduces the attack surface
> * Aligns with Docker’s recommendations for container hardening
> * Helps comply with stricter security policies in production environments

### [Step 2: Create the compose.yaml file](#step-2-create-the-composeyaml-file)

Create a file named `compose.yaml` with the following contents:

compose.yaml

```yaml
services:
  server:
    build:
      context: .
    ports:
      - 8080:8080
```

### [Step 3: Create the .dockerignore file](#step-3-create-the-dockerignore-file)

The `.dockerignore` file tells Docker which files and folders to exclude when building the image.

> Note
>
> This helps:
>
> * Reduce image size
> * Speed up the build process
> * Prevent sensitive or unnecessary files (like `.env`, `.git`, or `node_modules`) from being added to the final image.
>
> To learn more, visit the [.dockerignore reference](https://docs.docker.com/reference/dockerfile/#dockerignore-file).

Create a file named `.dockerignore` with the following contents:

```dockerignore
# ================================
# Node and build output
# ================================
node_modules
dist
out-tsc
.angular
.cache
.tmp

# ================================
# Testing & Coverage
# ================================
coverage
jest
cypress
cypress/screenshots
cypress/videos
reports
playwright-report
.vite
.vitepress

# ================================
# Environment & log files
# ================================
*.env*
!*.env.production
*.log
*.tsbuildinfo

# ================================
# IDE & OS-specific files
# ================================
.vscode
.idea
.DS_Store
Thumbs.db
*.swp

# ================================
# Version control & CI files
# ================================
.git
.gitignore

# ================================
# Docker & local orchestration
# ================================
Dockerfile
Dockerfile.*
.dockerignore
docker-compose.yml
docker-compose*.yml

# ================================
# Miscellaneous
# ================================
*.bak
*.old
*.tmp
```

### [Step 4: Create the `nginx.conf` file](#step-4-create-the-nginxconf-file)

To serve your Angular application efficiently inside the container, you’ll configure Nginx with a custom setup. This configuration is optimized for performance, browser caching, gzip compression, and support for client-side routing.

Create a file named `nginx.conf` in the root of your project directory, and add the following content:

> Note
>
> To learn more about configuring Nginx, see the [official Nginx documentation](https://nginx.org/en/docs/).

```nginx
worker_processes auto;

pid /tmp/nginx.pid;

events {
    worker_connections 1024;
}

http {
    include       /etc/nginx/mime.types;
    default_type  application/octet-stream;

    client_body_temp_path /tmp/client_temp;
    proxy_temp_path       /tmp/proxy_temp_path;
    fastcgi_temp_path     /tmp/fastcgi_temp;
    uwsgi_temp_path       /tmp/uwsgi_temp;
    scgi_temp_path        /tmp/scgi_temp;

    # Logging
    access_log off;
    error_log  /dev/stderr warn;

    # Performance
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    keepalive_requests 1000;

    # Compression
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_min_length 256;
    gzip_comp_level 6;
    gzip_types
        text/plain
        text/css
        text/xml
        text/javascript
        application/javascript
        application/x-javascript
        application/json
        application/xml
        application/xml+rss
        font/ttf
        font/otf
        image/svg+xml;

    server {
        listen       8080;
        server_name  localhost;

        root /usr/share/nginx/html;
        index index.html;

        # Angular Routing
        location / {
            try_files $uri $uri/ /index.html;
        }

        # Static Assets Caching
        location ~* \.(?:ico|css|js|gif|jpe?g|png|woff2?|eot|ttf|svg|map)$ {
            expires 1y;
            access_log off;
            add_header Cache-Control "public, immutable";
        }

        # Optional: Explicit asset route
        location /assets/ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }
}
```

### [Step 5: Build the Angular application image](#step-5-build-the-angular-application-image)

With your custom configuration in place, you're now ready to build the Docker image for your Angular application.

The updated setup includes:

* The updated setup includes a clean, production-ready Nginx configuration tailored specifically for Angular.
* Efficient multi-stage Docker build, ensuring a small and secure final image.

After completing the previous steps, your project directory should now contain the following files:

```text
├── docker-angular-sample/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── compose.yaml
│ └── nginx.conf
```

Now that your Dockerfile is configured, you can build the Docker image for your Angular application.

> Note
>
> The `docker build` command packages your application into an image using the instructions in the Dockerfile. It includes all necessary files from the current directory (called the [build context](/build/concepts/context/#what-is-a-build-context)).

Run the following command from the root of your project:

```console
$ docker build --tag docker-angular-sample .
```

What this command does:

* Uses the Dockerfile in the current directory (.)
* Packages the application and its dependencies into a Docker image
* Tags the image as docker-angular-sample so you can reference it later

### [Step 6: View local images](#step-6-view-local-images)

After building your Docker image, you can check which images are available on your local machine using either the Docker CLI or [Docker Desktop](https://docs.docker.com/desktop/use-desktop/images/). Since you're already working in the terminal, let's use the Docker CLI.

To list all locally available Docker images, run the following command:

```console
$ docker images
```

Example Output:

```shell
REPOSITORY                TAG               IMAGE ID       CREATED         SIZE
docker-angular-sample     latest            34e66bdb9d40   14 seconds ago   76.4MB
```

This output provides key details about your images:

* **Repository** – The name assigned to the image.
* **Tag** – A version label that helps identify different builds (e.g., latest).
* **Image ID** – A unique identifier for the image.
* **Created** – The timestamp indicating when the image was built.
* **Size** – The total disk space used by the image.

If the build was successful, you should see `docker-angular-sample` image listed.

***

## [Run the containerized application](#run-the-containerized-application)

In the previous step, you created a Dockerfile for your Angular application and built a Docker image using the docker build command. Now it’s time to run that image in a container and verify that your application works as expected.

Inside the `docker-angular-sample` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:8080>. You should see a simple Angular web application.

Press `ctrl+c` in the terminal to stop your application.

### [Run the application in the background](#run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option. Inside the `docker-angular-sample` directory, run the following command in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at <http://localhost:8080>. You should see your Angular application running in the browser.

To confirm that the container is running, use `docker ps` command:

```console
$ docker ps
```

This will list all active containers along with their ports, names, and status. Look for a container exposing port 8080.

Example Output:

```shell
CONTAINER ID   IMAGE                          COMMAND                  CREATED             STATUS             PORTS                    NAMES
eb13026806d1   docker-angular-sample-server   "nginx -c /etc/nginx…"   About a minute ago  Up About a minute  0.0.0.0:8080->8080/tcp   docker-angular-sample-server-1
```

To stop the application, run:

```console
$ docker compose down
```

> Note
>
> For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

***

## [Summary](#summary)

In this guide, you learned how to containerize, build, and run an Angular application using Docker. By following best practices, you created a secure, optimized, and production-ready setup.

What you accomplished:

* Created a multi-stage `Dockerfile` that compiles the Angular application and serves the static files using Nginx.
* Created a `.dockerignore` file to exclude unnecessary files and keep the image clean and efficient.
* Built your Docker image using `docker build`.
* Ran the container using `docker compose up`, both in the foreground and in detached mode.
* Verified that the app was running by visiting <http://localhost:8080>.
* Learned how to stop the containerized application using `docker compose down`.

You now have a fully containerized Angular application, running in a Docker container, and ready for deployment across any environment with confidence and consistency.

***

***

## [Next steps](#next-steps)

With your Angular application now containerized, you're ready to move on to the next step.

In the next section, you'll learn how to develop your application using Docker containers, enabling a consistent, isolated, and reproducible development environment across any machine.

[Use containers for Angular development »](https://docs.docker.com/guides/angular/develop/)

----
url: https://docs.docker.com/extensions/marketplace/
----

# Marketplace extensions

***

Table of contents

***

There are two types of extensions available in the Extensions Marketplace:

* Docker-reviewed extensions
* Self-published extensions

Docker-reviewed extensions are manually reviewed by the Docker Extensions team to ensure an extra level of trust and quality. They appear as **Reviewed** in the Marketplace.

Self-published extensions are autonomously published by extension developers and go through an automated validation process. They appear as **Not reviewed** in the Marketplace.

> Important
>
> Marketplace extensions are reviewed by Docker, but are not subject to a full security audit. Extensions run with host-level privileges. They can install binaries, access Docker Engine, invoke commands, and access files on your machine. Only install extensions from publishers you trust.

## [Install an extension](#install-an-extension)

> Note
>
> For some extensions, a separate account needs to be created before use.

To install an extension:

1. Open Docker Desktop.
2. From the Docker Desktop Dashboard, select the **Extensions** tab. The Extensions Marketplace opens on the **Browse** tab.
3. Browse the available extensions. You can sort the list of extensions by **Recently added**, **Most installed**, or alphabetically. Alternatively, use the **Content** or **Categories** drop-down menu to search for extensions by whether they have been reviewed or not, or by category.
4. Choose an extension and select **Install**.

From here, you can select **Open** to access the extension or install additional extensions. The extension also appears in the left-hand menu and in the **Manage** tab.

## [Update an extension](#update-an-extension)

You can update any extension outside of Docker Desktop releases. To update an extension to the latest version, navigate to the Docker Desktop Dashboard and select the **Manage** tab.

The **Manage** tab displays with all your installed extensions. If an extension has a new version available, it displays an **Update** button.

## [Uninstall an extension](#uninstall-an-extension)

You can uninstall an extension at any time.

> Note
>
> Any data used by the extension that's stored in a volume must be manually deleted.

1. Navigate to the Docker Desktop Dashboard and select the **Manage** tab. This displays a list of extensions you've installed.
2. Select the ellipsis to the right of extension you want to uninstall.
3. Select **Uninstall**.

----
url: https://docs.docker.com/ai/sandboxes/governance/monitoring/
----

# Monitoring policies

***

Table of contents

***

`sbx policy ls` and `sbx policy log` give you a combined view of all active policy rules and sandbox network activity, regardless of whether those rules come from local configuration or organization governance. They're useful both for verifying rules you've written and for debugging why a request is being blocked or allowed.

## [Listing rules](#listing-rules)

Use `sbx policy ls` to see all active rules and their current status:

```console
$ sbx policy ls
NAME                  TYPE      ORIGIN               DECISION   STATUS   RESOURCES
balanced-dev          network   local                allow      active   api.anthropic.com
ads-block             network   local                deny       active   ads.example.com
kit:my-sandbox        network   sandbox:my-sandbox   allow      active   api.example.com
kit:my-sandbox:deny   network   sandbox:my-sandbox   deny       active   telemetry.example.com
```

The columns are:

* `NAME`: the rule name.
* `TYPE`: the rule domain, such as `network`.
* `ORIGIN`: where the rule was configured. `local` means the rule is global and applies to all sandboxes. `sandbox:<name>` means the rule is scoped to the named sandbox. `remote` means the rule was set by your organization.
* `DECISION`: whether the rule allows or denies the resource.
* `STATUS`: whether the rule is in effect. A rule may be `inactive` if it's overridden or suppressed — for example, when organization governance is active, local rules are not evaluated. Inactive rules are hidden by default; pass `--include-inactive` to list them. See [Showing inactive rules](#showing-inactive-rules).
* `RESOURCES`: the hosts or patterns the rule applies to.

When organization governance is active, the output starts with a governance header showing which organization manages the policy and when it last synced:

```console
$ sbx policy ls
Governance: managed by my-org
[OK] last synced 13:54:21
NAME                  TYPE      ORIGIN               DECISION   STATUS   RESOURCES
allow AI services     network   remote               allow      active   api.anthropic.com
                                                                         api.openai.com
allow Docker services network   remote               allow      active   *.docker.com
                                                                         *.docker.io
```

The governance header shows which organization is managing the policy and confirms the daemon has successfully pulled the latest rules. If the sync status shows an error or a stale timestamp, the daemon may not have the most recent org policy. Run `sbx policy reset` to force a fresh pull.

### [Showing inactive rules](#showing-inactive-rules)

When organization governance is active, local and kit-defined rules are not evaluated, so `sbx policy ls` hides them by default. To list them too — for example, to confirm which local rules the organization policy overrides — pass `--include-inactive`:

```console
$ sbx policy ls --include-inactive
Governance: managed by my-org
[OK] last synced 13:54:21
NAME                  TYPE      ORIGIN               DECISION   STATUS     RESOURCES
balanced-dev          network   local                allow      inactive   api.anthropic.com
allow AI services     network   remote               allow      active     api.anthropic.com
                                                                           api.openai.com
allow Docker services network   remote               allow      active     *.docker.com
                                                                           *.docker.io
```

Inactive rules show with an `inactive` status. They have no effect while organization governance is active.

Use `--type network` to show only network rules. Without a sandbox argument, `sbx policy ls` shows every rule across all sandboxes. Pass a sandbox name to filter to global rules and rules scoped to that sandbox:

```console
$ sbx policy ls my-sandbox
```

## [Monitoring traffic](#monitoring-traffic)

Use `sbx policy log` to see which hosts your sandboxes have contacted and which rules matched:

```console
$ sbx policy log
Blocked requests:
SANDBOX      TYPE     HOST                   PROXY        RULE            REASON         LAST SEEN        COUNT
my-sandbox   network  blocked.example.com    transparent  domain-blocked  default-deny   10:15:25 29-Jan  1

Allowed requests:
SANDBOX      TYPE     HOST                   PROXY          RULE             REASON   LAST SEEN        COUNT
my-sandbox   network  api.anthropic.com      forward        domain-allowed            10:15:23 29-Jan  42
my-sandbox   network  registry.npmjs.org     forward-bypass domain-allowed            10:15:20 29-Jan  18
my-sandbox   network  app.example.com        browser-open                             10:15:10 29-Jan  1
```

The `PROXY` column shows how the request left the sandbox:

| Value            | Description                                                                                                                    |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| `forward`        | Routed through the forward proxy. Supports [credential injection](https://docs.docker.com/ai/sandboxes/security/credentials/). |
| `forward-bypass` | Routed through the forward proxy without credential injection.                                                                 |
| `transparent`    | Intercepted by the transparent proxy. Policy is enforced but credential injection is not available.                            |
| `network`        | Non-HTTP traffic (raw TCP, UDP, ICMP). TCP can be allowed with a policy rule; UDP and ICMP are always blocked.                 |
| `browser-open`   | A sandbox process requested opening a URL in the host browser. Policy is enforced before opening the URL.                      |

The `RULE` column identifies the policy rule that matched the request. The `REASON` column includes extra context when the daemon records one.

Filter by sandbox name by passing it as an argument:

```console
$ sbx policy log my-sandbox
```

Use `--limit N` to show only the last `N` entries, `--json` for machine-readable output, or `--type network` to filter by policy type.

----
url: https://docs.docker.com/guides/pgadmin/
----

[Visualizing your PostgreSQL databases with pgAdmin](https://docs.docker.com/guides/pgadmin/)

Explore how to add pgAdmin to your development stack and make it as easy as possible for your teammates to navigate through your PostgreSQL databases.

Databases

10 minutes

[« Back to all guides](/guides/)

# Visualizing your PostgreSQL databases with pgAdmin

***

Table of contents

***

Many applications use PostgreSQL databases in the application stack. However, not all developers are knowledgeable about navigating and working with PostgreSQL databases.

Fortunately, when you use containers in development, it is easy to add additional services to help with troubleshooting and debugging.

The [pgAdmin](https://www.pgadmin.org/) tool is a popular open-source tool designed to help administer and visualize PostgreSQL databases.

In this guide you will learn how to:

1. Add pgAdmin to your application stack
2. Configure pgAdmin to automatically connect to the development database

## [Adding pgAdmin to your stack](#adding-pgadmin-to-your-stack)

1. In your `compose.yaml` file, add the `pgadmin` service next to your existing `postgres` service:

   ```yaml
   services:
     postgres:
       image: postgres:18
       environment:
         POSTGRES_USER: postgres
         POSTGRES_PASSWORD: secret
         POSTGRES_DB: demo

     pgadmin:
       image: dpage/pgadmin4:9.8
       ports:
         - 5050:80
       environment:
         # Required by pgAdmin
         PGADMIN_DEFAULT_EMAIL: demo@example.com
         PGADMIN_DEFAULT_PASSWORD: secret

         # Don't require the user to login
         PGADMIN_CONFIG_SERVER_MODE: 'False'

         # Don't require a "master" password after logging in
         PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED: 'False'
   ```

2. Start the Compose stack with the following command:

   ```console
   $ docker compose up
   ```

   After the image is downloaded the container starts, you will see output that looks similar to the following indicating pgAdmin is ready:

   ```console
   pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Starting gunicorn 23.0.0
   pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
   pgadmin-1   | [2025-09-22 15:52:47 +0000] [1] [INFO] Using worker: gthread
   pgadmin-1   | [2025-09-22 15:52:47 +0000] [119] [INFO] Booting worker with pid: 119
   ```

3. Open pgAdmin by going to http\://localhost:5050.

4. Once in the admin panel, select the **Add New Server** link to define a new server. Enter the following details:

   * **General** tab:
     * **Name**: `postgres`

   * **Connection** tab:

     * **Host name/address**: `postgres`
     * **Username**: `postgres`
     * **Password**: `secret`
     * Enable the **Save password?** field

   > Important
   >
   > These connection details assume you are using the previous Compose file snippet. If you are using an existing Compose file, adjust the connection details as required. The **Host name/address** field should match the name of your postgres service.

5. Select the **Save** button to create the new database.

You now have pgAdmin setup and connected to your containerized database. Feel free to navigate around, view the tables, and explore your database.

## [Configuring pgAdmin to auto-connect to the database](#configuring-pgadmin-to-auto-connect-to-the-database)

Although you have pgAdmin running, it would be nice if you could simply open the app without needing to configure the database connection. Reducing the setup steps would be a great way to make it easier for teammates to get value from this tool.

Fortunately, there is an ability to auto-connect to the database.

> Warning
>
> In order to auto-connect, the database credentials are shared using plaintext files. During local development, this is often acceptable as local data is not real customer data. However, if you are using production or sensitive data, this practice is strongly discouraged.

1. First, you need to define the server itself, which pgAdmin does using a `servers.json` file.

   Add the following to your `compose.yaml` file to define a config file for the `servers.json` file:

   ```yaml
   configs:
     pgadmin-servers:
       content: |
         {
           "Servers": {
             "1": {
               "Name": "Local Postgres",
               "Group": "Servers",
               "Host": "postgres",
               "Port": 5432,
               "MaintenanceDB": "postgres",
               "Username": "postgres",
               "PassFile": "/config/pgpass"
             }
           }
         }
   ```

2. The `servers.json` file defines a `PassFile` field, which is a reference to a [postgreSQL password files](https://www.postgresql.org/docs/current/libpq-pgpass.html). These are often referred to as a pgpass file.

   Add the following config to your `compose.yaml` file to define a pgpass file:

   ```yaml
   configs:
     pgadmin-pgpass:
       content: |
         postgres:5432:*:postgres:secret
   ```

   This will indicate any connection requests to `postgres:5432` using the username `postgres` should provide a password of `secret`.

3. In your `compose.yaml`, update the `pgadmin` service to inject the config files:

   ```yaml
   services:
     pgadmin:
       ...
       configs:
         - source: pgadmin-pgpass
           target: /config/pgpass
           uid: "5050"
           gid: "5050"
           mode: 0400
         - source: pgadmin-servers
           target: /pgadmin4/servers.json
           mode: 0444
   ```

4. Update the application stack by running `docker compose up` again:

   ```console
   $ docker compose up
   ```

5. Once the application is restarted, open your browser to http\://localhost:5050. You should be able to access the database without any logging in or configuration.

## [Conclusion](#conclusion)

Using containers makes it easy to not only run your application's dependencies, but also additional tools to help with troubleshooting and debugging.

When you add tools, think about the experience and possible friction your teammates might experience and how you might be able to remove it. In this case, you were able to take an extra step to add configuration to automatically configure and connect the databases, saving your teammates valuable time.

----
url: https://docs.docker.com/reference/samples/ai-ml/
----

# AI/ML samples

| Name                                                                                                                                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [AI/ML with Docker](https://github.com/docker/genai-stack)                                                                            | Get started with AI and ML using Docker, Neo4j, LangChain, and Ollama                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| [Agent-to-Agent](https://github.com/docker/compose-for-agents/tree/main/a2a)                                                          | This app is a modular AI agent runtime built on Google's Agent Development Kit (ADK) and the A2A (Agent-to-Agent) protocol. It wraps a large language model (LLM)-based agent in an HTTP API and uses structured execution flows with streaming responses, memory, and tools. It is designed to make agents callable as network services and composable with other agents.                                                                                                                                |
| [ADK Multi-Agent Fact Checker](https://github.com/docker/compose-for-agents/tree/main/adk)                                            | This project demonstrates a collaborative multi-agent system built with the Agent Development Kit (ADK), where a top-level Auditor agent coordinates the workflow to verify facts. The Critic agent gathers evidence via live internet searches using DuckDuckGo through the Model Context Protocol (MCP), while the Reviser agent analyzes and refines the conclusion using internal reasoning alone. The system showcases how agents with distinct roles and tools can collaborate under orchestration. |
| [DevDuck agents](https://github.com/docker/compose-for-agents/tree/main/adk-cerebras)                                                 | A multi-agent system for Go programming assistance built with Google Agent Development Kit (ADK). This project features a coordinating agent (DevDuck) that manages two specialized sub-agents (Bob and Cerebras) for different programming tasks.                                                                                                                                                                                                                                                        |
| [Agno](https://github.com/docker/compose-for-agents/tree/main/agno)                                                                   | This app is a multi-agent orchestration system powered by LLMs (like Qwen and OpenAI) and connected to tools via a Model Control Protocol (MCP) gateway. Its purpose is to retrieve, summarize, and document GitHub issues—automatically creating Notion pages from the summaries. It also supports file content summarization from GitHub.                                                                                                                                                               |
| [CrewAI](https://github.com/docker/compose-for-agents/tree/main/crew-ai)                                                              | This project showcases an autonomous, multi-agent virtual marketing team built with CrewAI. It automates the creation of a high-quality, end-to-end marketing strategy — from research to copywriting — using task delegation, web search, and creative synthesis.                                                                                                                                                                                                                                        |
| [SQL Agent with LangGraph](https://github.com/docker/compose-for-agents/tree/main/langgraph)                                          | This project demonstrates a zero-config AI agent that uses LangGraph to answer natural language questions by querying a SQL database — all orchestrated with Docker Compose.                                                                                                                                                                                                                                                                                                                              |
| [Langchaingo Brave Search Example - Model Context Protocol (MCP)](https://github.com/docker/compose-for-agents/tree/main/langchaingo) | This example demonstrates how to create a Go Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses the official Go SDK for Model Context Protocol servers and clients, to set up the MCP client.                                                         |
| [Spring AI Brave Search Example - Model Context Protocol (MCP)](https://github.com/docker/compose-for-agents/tree/main/spring-ai)     | This example demonstrates how to create a Spring AI Model Context Protocol (MCP) client that communicates with the Brave Search MCP Server. The application shows how to build an MCP client that enables natural language interactions with Brave Search, allowing you to perform internet searches through a conversational interface. This example uses Spring Boot autoconfiguration to set up the MCP client through configuration files.                                                            |
| [MCP UI with Vercel AI SDK](https://github.com/docker/compose-for-agents/tree/main/vercel)                                            | Start an MCP UI application that uses the Vercel AI SDK to provide a chat interface for local models, provided by the Docker Model Runner, with access to MCPs from the Docker MCP Catalog.                                                                                                                                                                                                                                                                                                               |

----
url: https://docs.docker.com/reference/cli/docker/trust/key/generate/
----

# docker trust key generate

***

| Description | Generate and load a signing key-pair |
| ----------- | ------------------------------------ |
| Usage       | `docker trust key generate NAME`     |

## [Description](#description)

`docker trust key generate` generates a key-pair to be used with signing, and loads the private key into the local Docker trust keystore.

## [Options](#options)

| Option  | Default | Description                                                 |
| ------- | ------- | ----------------------------------------------------------- |
| `--dir` |         | Directory to generate key in, defaults to current directory |

## [Examples](#examples)

### [Generate a key-pair](#generate-a-key-pair)

```console
$ docker trust key generate alice

Generating key for alice...
Enter passphrase for new alice key with ID 17acf3c:
Repeat passphrase for new alice key with ID 17acf3c:
Successfully generated and loaded private key. Corresponding public key available: alice.pub
$ ls
alice.pub
```

The private signing key is encrypted by the passphrase and loaded into the Docker trust keystore. All passphrase requests to sign with the key will be referred to by the provided `NAME`.

The public key component `alice.pub` will be available in the current working directory, and can be used directly by `docker trust signer add`.

Provide the `--dir` argument to specify a directory to generate the key in:

```console
$ docker trust key generate alice --dir /foo

Generating key for alice...
Enter passphrase for new alice key with ID 17acf3c:
Repeat passphrase for new alice key with ID 17acf3c:
Successfully generated and loaded private key. Corresponding public key available: alice.pub
$ ls /foo
alice.pub
```

----
url: https://docs.docker.com/reference/api/extensions-sdk/OpenDialogResult/
----

# Interface: OpenDialogResult

***

Table of contents

***

**`Since`**

0.2.3

## [Properties](#properties)

### [canceled](#canceled)

• `Readonly` **canceled**: `boolean`

Whether the dialog was canceled.

***

### [filePaths](#filepaths)

• `Readonly` **filePaths**: `string`\[]

An array of file paths chosen by the user. If the dialog is cancelled this will be an empty array.

***

### [bookmarks](#bookmarks)

• `Optional` `Readonly` **bookmarks**: `string`\[]

macOS only. An array matching the `filePaths` array of `base64` encoded strings which contains security scoped bookmark data. `securityScopedBookmarks` must be enabled for this to be populated.

----
url: https://docs.docker.com/reference/samples/
----

# Samples overview

***

Table of contents

***

Learn how to containerize different types of services by walking through Official Docker samples.

## [Databases](#databases)

[MariaDB](https://docs.docker.com/reference/samples/mariadb/) | [MongoDB](https://docs.docker.com/reference/samples/mongodb/) | [MS-SQL](https://docs.docker.com/reference/samples/ms-sql/) | [MySQL](https://docs.docker.com/reference/samples/mysql/) | [PostgreSQL](https://docs.docker.com/reference/samples/postgres/) | [Redis](https://docs.docker.com/reference/samples/redis/)

## [Frameworks](#frameworks)

[.NET](https://docs.docker.com/reference/samples/dotnet/) | [Angular](https://docs.docker.com/reference/samples/angular/) | [Django](https://docs.docker.com/reference/samples/django/) | [Express](https://docs.docker.com/reference/samples/express/) |[FastAPI](https://docs.docker.com/reference/samples/fastapi/) | [Flask](https://docs.docker.com/reference/samples/flask/) | [Node.js](https://docs.docker.com/reference/samples/nodejs/) | [React](https://docs.docker.com/reference/samples/react/) | [Rails](https://docs.docker.com/reference/samples/rails/) | [Spark](https://docs.docker.com/reference/samples/spark/) | [Spring Boot](https://docs.docker.com/reference/samples/spring/) | [Vue.js](https://docs.docker.com/reference/samples/vuejs/)

## [Languages](#languages)

[Go](https://docs.docker.com/reference/samples/go/) | [Java](https://docs.docker.com/reference/samples/java/) | [JavaScript](https://docs.docker.com/reference/samples/javascript/) | [PHP](https://docs.docker.com/reference/samples/php/) | [Python](https://docs.docker.com/reference/samples/python/) | [Ruby](https://docs.docker.com/reference/samples/ruby/) | [Rust](https://docs.docker.com/reference/samples/rust/) | [TypeScript](https://docs.docker.com/reference/samples/typescript/)

## [Platforms](#platforms)

[Gitea](https://docs.docker.com/reference/samples/gitea/) | [Nextcloud](https://docs.docker.com/reference/samples/nextcloud/) | [Portainer](https://docs.docker.com/reference/samples/portainer/) | [Prometheus](https://docs.docker.com/reference/samples/prometheus/) | [WordPress](https://docs.docker.com/reference/samples/wordpress/)

## [Other samples](#other-samples)

[Agentic AI](https://docs.docker.com/reference/samples/agentic-ai/) | [AI/ML](https://docs.docker.com/reference/samples/ai-ml/) | [Cloudflared](https://docs.docker.com/reference/samples/cloudflared/) | [Elasticsearch / Logstash / Kibana](https://docs.docker.com/reference/samples/elasticsearch/) | [Minecraft](https://docs.docker.com/reference/samples/minecraft/) | [NGINX](https://docs.docker.com/reference/samples/nginx/) | [Pi-hole](https://docs.docker.com/reference/samples/pi-hole/) | [Plex](https://docs.docker.com/reference/samples/plex/) | [Traefik](https://docs.docker.com/reference/samples/traefik/) | [WireGuard](https://docs.docker.com/reference/samples/wireguard/)

----
url: https://docs.docker.com/guides/ruby/containerize/
----

# Containerize a Ruby on Rails application

***

Table of contents

***

## [Prerequisites](#prerequisites)

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
* You have a [Git client](https://git-scm.com/downloads). The examples in this section show the Git CLI, but you can use any client.

## [Overview](#overview)

This section walks you through containerizing and running a [Ruby on Rails](https://rubyonrails.org/) application.

Starting from Rails 7.1 [Docker is supported out of the box](https://guides.rubyonrails.org/7_1_release_notes.html#generate-dockerfiles-for-new-rails-applications). This means that you will get a `Dockerfile`, `.dockerignore` and `bin/docker-entrypoint` files generated for you when you create a new Rails application.

If you have an existing Rails application, you will need to create the Docker assets manually from the examples below.

## [1. Create Docker assets](#1-create-docker-assets)

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

Rails 7.1 and newer generates multistage Dockerfile out of the box. Following are two versions of such a file: one using Docker Hardened Images (DHIs) and another using the Docker Official Image (DOIs). Although the Dockerfile is generated automatically, understanding its purpose and functionality is important. Reviewing the following example is highly recommended.

[Docker Hardened Images (DHIs)](https://docs.docker.com/dhi/) are minimal, secure, and production-ready container base and application images maintained by Docker. DHIs are recommended whenever it is possible for better security. They are designed to reduce vulnerabilities and simplify compliance, freely available to everyone with no subscription required, no usage restrictions, and no vendor lock-in.

Multistage Dockerfiles help create smaller, more efficient images by separating build and runtime dependencies, ensuring only necessary components are included in the final image. Read more in the [Multi-stage builds guide](/get-started/docker-concepts/building-images/multi-stage-builds/).

You must authenticate to `dhi.io` before you can pull Docker Hardened Images. Run `docker login dhi.io` to authenticate.

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=error=true

# This Dockerfile is designed for production, not development.
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<value from config/master.key> --name app app

# For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# Make sure RUBY_VERSION matches the Ruby version in .ruby-version
ARG RUBY_VERSION=3.4.8
FROM dhi.io/ruby:$RUBY_VERSION-dev AS base

# Rails app lives here
WORKDIR /rails

# Install base packages
# Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Set production environment
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# Throw-away build stage to reduce size of final image
FROM base AS build

# Install packages needed to build gems
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Install JavaScript dependencies and Node.js for asset compilation
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# Install application gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# Install node modules
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# Copy application code
COPY . .

# Precompile bootsnap code for faster boot times
RUN bundle exec bootsnap precompile app/ lib/

# Precompiling assets for production without requiring secret RAILS_MASTER_KEY
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# Final stage for app image
FROM base

# Copy built artifacts: gems, application
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# Run and own only the runtime files as a non-root user for security
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# Entrypoint prepares the database.
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# Start server via Thruster by default, this can be overwritten at runtime
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

Dockerfile

```dockerfile
# syntax=docker/dockerfile:1
# check=error=true

# This Dockerfile is designed for production, not development.
# docker build -t app .
# docker run -d -p 80:80 -e RAILS_MASTER_KEY=<value from config/master.key> --name app app

# For a containerized dev environment, see Dev Containers: https://guides.rubyonrails.org/getting_started_with_devcontainer.html

# Make sure RUBY_VERSION matches the Ruby version in .ruby-version
ARG RUBY_VERSION=3.4.8
FROM docker.io/library/ruby:$RUBY_VERSION-slim AS base

# Rails app lives here
WORKDIR /rails

# Install base packages
# Replace libpq-dev with sqlite3 if using SQLite, or libmysqlclient-dev if using MySQL
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y curl libjemalloc2 libvips libpq-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Set production environment
ENV RAILS_ENV="production" \
    BUNDLE_DEPLOYMENT="1" \
    BUNDLE_PATH="/usr/local/bundle" \
    BUNDLE_WITHOUT="development"

# Throw-away build stage to reduce size of final image
FROM base AS build

# Install packages needed to build gems
RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential curl git pkg-config libyaml-dev && \
    rm -rf /var/lib/apt/lists /var/cache/apt/archives

# Install JavaScript dependencies and Node.js for asset compilation
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# ARG NODE_VERSION=18.12.0
# ARG YARN_VERSION=1.22.19
# ENV PATH=/usr/local/node/bin:$PATH
# RUN curl -sL https://github.com/nodenv/node-build/archive/master.tar.gz | tar xz -C /tmp/ && \
#     /tmp/node-build-master/bin/node-build "${NODE_VERSION}" /usr/local/node && \
#     npm install -g yarn@$YARN_VERSION && \
#     npm install -g mjml && \
#     rm -rf /tmp/node-build-master

# Install application gems
COPY Gemfile Gemfile.lock ./
RUN bundle install && \
    rm -rf ~/.bundle/ "${BUNDLE_PATH}"/ruby/*/cache "${BUNDLE_PATH}"/ruby/*/bundler/gems/*/.git && \
    bundle exec bootsnap precompile --gemfile

# Install node modules
#
# Uncomment the following lines if you are using NodeJS need to compile assets
#
# COPY package.json yarn.lock ./
# RUN --mount=type=cache,id=yarn,target=/rails/.cache/yarn YARN_CACHE_FOLDER=/rails/.cache/yarn \
#     yarn install --frozen-lockfile

# Copy application code
COPY . .

# Precompile bootsnap code for faster boot times
RUN bundle exec bootsnap precompile app/ lib/

# Precompiling assets for production without requiring secret RAILS_MASTER_KEY
RUN SECRET_KEY_BASE_DUMMY=1 ./bin/rails assets:precompile

# Final stage for app image
FROM base

# Copy built artifacts: gems, application
COPY --from=build "${BUNDLE_PATH}" "${BUNDLE_PATH}"
COPY --from=build /rails /rails

# Run and own only the runtime files as a non-root user for security
RUN groupadd --system --gid 1000 rails && \
    useradd rails --uid 1000 --gid 1000 --create-home --shell /bin/bash && \
    chown -R rails:rails db log storage tmp
USER 1000:1000

# Entrypoint prepares the database.
ENTRYPOINT ["/rails/bin/docker-entrypoint"]

# Start server via Thruster by default, this can be overwritten at runtime
EXPOSE 80
CMD ["./bin/thrust", "./bin/rails", "server"]
```

The Dockerfile above assumes you are using Thruster together with Puma as an application server. In case you are using any other server, you can replace the last three lines with the following:

```dockerfile
# Start the application server
EXPOSE 3000
CMD ["./bin/rails", "server"]
```

This Dockerfile uses a script at `./bin/docker-entrypoint` as the container's entrypoint. This script prepares the database and runs the application server. Below is an example of such a script.

docker-entrypoint

```bash
#!/bin/bash -e

# Enable jemalloc for reduced memory usage and latency.
if [ -z "${LD_PRELOAD+x}" ]; then
    LD_PRELOAD=$(find /usr/lib -name libjemalloc.so.2 -print -quit)
    export LD_PRELOAD
fi

# If running the rails server then create or migrate existing database
if [ "${@: -2:1}" == "./bin/rails" ] && [ "${@: -1:1}" == "server" ]; then
  ./bin/rails db:prepare
fi

exec "${@}"
```

Besides the two files above you will also need a `.dockerignore` file. This file is used to exclude files and directories from the context of the build. Below is an example of a `.dockerignore` file.

.dockerignore

```text
# See https://docs.docker.com/engine/reference/builder/#dockerignore-file for more about ignoring files.

# Ignore git directory.
/.git/
/.gitignore

# Ignore bundler config.
/.bundle

# Ignore all environment files.
/.env*

# Ignore all default key files.
/config/master.key
/config/credentials/*.key

# Ignore all logfiles and tempfiles.
/log/*
/tmp/*
!/log/.keep
!/tmp/.keep

# Ignore pidfiles, but keep the directory.
/tmp/pids/*
!/tmp/pids/.keep

# Ignore storage (uploaded files in development and any SQLite databases).
/storage/*
!/storage/.keep
/tmp/storage/*
!/tmp/storage/.keep

# Ignore assets.
/node_modules/
/app/assets/builds/*
!/app/assets/builds/.keep
/public/assets

# Ignore CI service files.
/.github

# Ignore development files
/.devcontainer

# Ignore Docker-related files
/.dockerignore
/Dockerfile*
```

The last optional file that you may want is the `compose.yaml` file, which is used by Docker Compose to define the services that make up the application. Since SQLite is being used as the database, there is no need to define a separate service for the database. The only service required is the Rails application itself.

compose.yaml

```yaml
services:
  web:
    build: .
    environment:
      - RAILS_MASTER_KEY
    ports:
      - "3000:80"
```

You should now have the following files in your application folder:

* `.dockerignore`
* `compose.yaml`
* `Dockerfile`
* `bin/docker-entrypoint`

To learn more about the files, see the following:

* [Dockerfile](/reference/dockerfile)
* [.dockerignore](/reference/dockerfile#dockerignore-file)
* [compose.yaml](https://docs.docker.com/reference/compose-file/)
* [docker-entrypoint](/reference/dockerfile/#entrypoint)

## [2. Run the application](#2-run-the-application)

To run the application, run the following command in a terminal inside the application's directory.

```console
$ RAILS_MASTER_KEY=<master_key_value> docker compose up --build
```

Open a browser and view the application at <http://localhost:3000>. You should see a simple Ruby on Rails application.

In the terminal, press `ctrl`+`c` to stop the application.

## [3. Run the application in the background](#3-run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option. Inside the `docker-ruby-on-rails` directory, run the following command in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at <http://localhost:3000>.

You should see a simple Ruby on Rails application.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

## [Summary](#summary)

In this section, you learned how you can containerize and run your Ruby application using Docker.

Related information:

* [Docker Compose overview](https://docs.docker.com/compose/)

## [Next steps](#next-steps)

In the next section, you'll take a look at how to set up a CI/CD pipeline using GitHub Actions.

[Automate your builds with GitHub Actions »](https://docs.docker.com/guides/ruby/configure-github-actions/)

----
url: https://docs.docker.com/build/cache/backends/registry/
----

# Registry cache

***

Table of contents

***

The `registry` cache storage can be thought of as an extension to the `inline` cache. Unlike the `inline` cache, the `registry` cache is entirely separate from the image, which allows for more flexible usage - `registry`-backed cache can do everything that the inline cache can do, and more:

* Allows for separating the cache and resulting image artifacts so that you can distribute your final image without the cache inside.
* It can efficiently cache multi-stage builds in `max` mode, instead of only the final stage.
* It works with other exporters for more flexibility, instead of only the `image` exporter.

This cache storage backend is not supported with the default `docker` driver. To use this feature, create a new builder using a different driver. See [Build drivers](https://docs.docker.com/build/builders/drivers/) for more information.

## [Synopsis](#synopsis)

Unlike the simpler `inline` cache, the `registry` cache supports several configuration parameters:

```console
$ docker buildx build --push -t <registry>/<image> \
  --cache-to type=registry,ref=<registry>/<cache-image>[,parameters...] \
  --cache-from type=registry,ref=<registry>/<cache-image> .
```

The following table describes the available CSV parameters that you can pass to `--cache-to` and `--cache-from`.

| Name                | Option                  | Type                    | Default | Description                                                                                                                                                                                 |
| ------------------- | ----------------------- | ----------------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ref`               | `cache-to`,`cache-from` | String                  |         | Full name of the cache image to import.                                                                                                                                                     |
| `mode`              | `cache-to`              | `min`,`max`             | `min`   | Cache layers to export, see [cache mode](https://docs.docker.com/build/cache/backends/#cache-mode).                                                                                         |
| `oci-mediatypes`    | `cache-to`              | `true`,`false`          | `true`  | Use OCI media types in exported manifests, see [OCI media types](https://docs.docker.com/build/cache/backends/#oci-media-types).                                                            |
| `image-manifest`    | `cache-to`              | `true`,`false`          | `true`  | When using OCI media types, generate an image manifest instead of an image index for the cache image, see [OCI media types](https://docs.docker.com/build/cache/backends/#oci-media-types). |
| `compression`       | `cache-to`              | `gzip`,`estargz`,`zstd` | `gzip`  | Compression type, see [cache compression](https://docs.docker.com/build/cache/backends/#cache-compression).                                                                                 |
| `compression-level` | `cache-to`              | `0..22`                 |         | Compression level, see [cache compression](https://docs.docker.com/build/cache/backends/#cache-compression).                                                                                |
| `force-compression` | `cache-to`              | `true`,`false`          | `false` | Forcibly apply compression, see [cache compression](https://docs.docker.com/build/cache/backends/#cache-compression).                                                                       |
| `ignore-error`      | `cache-to`              | Boolean                 | `false` | Ignore errors caused by failed cache exports.                                                                                                                                               |

You can choose any valid value for `ref`, as long as it's not the same as the target location that you push your image to. You might choose different tags (e.g. `foo/bar:latest` and `foo/bar:build-cache`), separate image names (e.g. `foo/bar` and `foo/bar-cache`), or even different repositories (e.g. `docker.io/foo/bar` and `ghcr.io/foo/bar`). It's up to you to decide the strategy that you want to use for separating your image from your cache images.

If the `--cache-from` target doesn't exist, then the cache import step will fail, but the build continues.

## [Further reading](#further-reading)

For an introduction to caching see [Docker build cache](https://docs.docker.com/build/cache/).

For more information on the `registry` cache backend, see the [BuildKit README](https://github.com/moby/buildkit#registry-push-image-and-cache-separately).

----
url: https://docs.docker.com/extensions/extensions-sdk/process/
----

# The build and publish process

***

Table of contents

***

This documentation is structured so that it matches the steps you need to take when creating your extension.

There are two main parts to creating a Docker extension:

1. Build the foundations
2. Publish the extension

> Note
>
> You do not need to pay to create a Docker extension. The [Docker Extension SDK](https://www.npmjs.com/package/@docker/extension-api-client) is licensed under the Apache 2.0 License and is free to use. Anyone can create new extensions and share them without constraints.
>
> There is also no constraint on how each extension should be licensed, this is up to you to decide when creating a new extension.

## [Part one: Build the foundations](#part-one-build-the-foundations)

The build process consists of:

* Installing the latest version of Docker Desktop.
* Setting up the directory with files, including the extension’s source code and the required extension-specific files.
* Creating the `Dockerfile` to build, publish, and run your extension in Docker Desktop.
* Configuring the metadata file which is required at the root of the image filesystem.
* Building and installing the extension.

For further inspiration, see the other examples in the [samples folder](https://github.com/docker/extensions-sdk/tree/main/samples).

> Tip
>
> Whilst creating your extension, make sure you follow the [design](https://docs.docker.com/extensions/extensions-sdk/design/design-guidelines/) and [UI styling](https://docs.docker.com/extensions/extensions-sdk/design/) guidelines to ensure visual consistency and [level AA accessibility standards](https://www.w3.org/WAI/WCAG2AA-Conformance).

## [Part two: Publish and distribute your extension](#part-two-publish-and-distribute-your-extension)

> Important
>
> New submissions to the Docker Extensions Marketplace are paused while Docker reviews Marketplace security. You can still update existing extensions, and private Marketplace extensions are unaffected. Contact <extensions@docker.com> if you have additional questions.

Docker Desktop displays published extensions in the Extensions Marketplace. The Extensions Marketplace is a curated space where developers can discover extensions to improve their developer experience and upload their own extension to share with the world.

If you want your extension published in the Marketplace, read the [publish documentation](https://docs.docker.com/extensions/extensions-sdk/extensions/publish/).

> Already built an extension?
>
> Let us know about your experience using the [feedback form](https://survey.alchemer.com/s3/7184948/Publishers-Feedback-Form).

## [What’s next?](#whats-next)

If you want to get up and running with creating a Docker Extension, see the [Quickstart guide](https://docs.docker.com/extensions/extensions-sdk/quickstart/).

Alternatively, get started with reading the "Part one: Build" section for more in-depth information about each step of the extension creation process.

For an in-depth tutorial of the entire build process, we recommend the following video walkthrough from DockerCon 2022.

----
url: https://docs.docker.com/reference/cli/docker/compose/cp/
----

# docker compose cp

***

| Description | Copy files/folders between a service container and the local filesystem                                               |
| ----------- | --------------------------------------------------------------------------------------------------------------------- |
| Usage       | `docker compose cp [OPTIONS] SERVICE:SRC_PATH DEST_PATH\|- docker compose cp [OPTIONS] SRC_PATH\|- SERVICE:DEST_PATH` |

## [Description](#description)

Copy files/folders between a service container and the local filesystem

## [Options](#options)

| Option              | Default | Description                                             |
| ------------------- | ------- | ------------------------------------------------------- |
| `--all`             |         | Include containers created by the run command           |
| `-a, --archive`     |         | Archive mode (copy all uid/gid information)             |
| `-L, --follow-link` |         | Always follow symbol link in SRC\_PATH                  |
| `--index`           |         | Index of the container if service has multiple replicas |

----
url: https://docs.docker.com/guides/testcontainers-java-quarkus/
----

# Testing Quarkus applications with Testcontainers

Table of contents

***

Learn how to create a Quarkus REST API with Hibernate ORM with Panache and PostgreSQL, then test it using Quarkus Dev Services, Testcontainers, and REST Assured.

**Time to complete** 25 minutes

In this guide, you'll learn how to:

* Create a Quarkus application with REST API endpoints
* Use Hibernate ORM with Panache and PostgreSQL for persistence
* Test the REST API using Quarkus Dev Services, which uses Testcontainers behind the scenes
* Test with services not supported by Dev Services using `QuarkusTestResourceLifecycleManager`

## [Prerequisites](#prerequisites)

* Java 17+
* Maven or Gradle
* A Docker environment supported by Testcontainers

> Note
>
> If you're new to Testcontainers, visit the [Testcontainers overview](https://testcontainers.com/getting-started/) to learn more about Testcontainers and the benefits of using it.

## [Modules](#modules)

1. [Create the project](https://docs.docker.com/guides/testcontainers-java-quarkus/create-project/)

   Set up a Quarkus project with Hibernate ORM with Panache, PostgreSQL, Flyway, and REST API endpoints.

2. [Write tests](https://docs.docker.com/guides/testcontainers-java-quarkus/write-tests/)

   Test the Quarkus REST API using Dev Services with Testcontainers, and test with services not supported by Dev Services.

3. [Run tests](https://docs.docker.com/guides/testcontainers-java-quarkus/run-tests/)

   Run your Testcontainers-based Quarkus integration tests and explore next steps.

----
url: https://docs.docker.com/ai/model-runner/inference-engines/
----

# Inference engines

***

Table of contents

***

Docker Model Runner supports three inference engines: **llama.cpp**, **vLLM**, and **Diffusers**. Each engine has different strengths, supported platforms, and model format requirements. This guide helps you choose the right engine and configure it for your use case.

## [Engine comparison](#engine-comparison)

| Feature               | llama.cpp                                            | vLLM                        | Diffusers                           |
| --------------------- | ---------------------------------------------------- | --------------------------- | ----------------------------------- |
| **Model formats**     | GGUF                                                 | Safetensors, HuggingFace    | DDUF                                |
| **Platforms**         | All (macOS, Windows, Linux)                          | Linux x86\_64 only          | Linux (x86\_64, ARM64)              |
| **GPU support**       | NVIDIA, AMD, Apple Silicon, Vulkan                   | NVIDIA CUDA only            | NVIDIA CUDA only                    |
| **CPU inference**     | Yes                                                  | No                          | No                                  |
| **Quantization**      | Built-in (Q4, Q5, Q8, etc.)                          | Limited                     | Limited                             |
| **Memory efficiency** | High (with quantization)                             | Moderate                    | Moderate                            |
| **Throughput**        | Good                                                 | High (with batching)        | Good                                |
| **Best for**          | Local development, resource-constrained environments | Production, high throughput | Image generation                    |
| **Use case**          | Text generation (LLMs)                               | Text generation (LLMs)      | Image generation (Stable Diffusion) |

## [llama.cpp](#llamacpp)

[llama.cpp](https://github.com/ggerganov/llama.cpp) is the default inference engine in Docker Model Runner. It's designed for efficient local inference and supports a wide range of hardware configurations.

### [Platform support](#platform-support)

| Platform              | GPU support         | Notes                           |
| --------------------- | ------------------- | ------------------------------- |
| macOS (Apple Silicon) | Metal               | Automatic GPU acceleration      |
| Windows (x64)         | NVIDIA CUDA         | Requires NVIDIA drivers 576.57+ |
| Windows (ARM64)       | Adreno OpenCL       | Qualcomm 6xx series and later   |
| Linux (x64)           | NVIDIA, AMD, Vulkan | Multiple backend options        |
| Linux                 | CPU only            | Works on any x64/ARM64 system   |

### [Model format: GGUF](#model-format-gguf)

llama.cpp uses the GGUF format, which supports efficient quantization for reduced memory usage without significant quality loss.

#### [Quantization levels](#quantization-levels)

| Quantization | Bits per weight | Memory usage | Quality       |
| ------------ | --------------- | ------------ | ------------- |
| Q2\_K        | \~2.5           | Lowest       | Reduced       |
| Q3\_K\_M     | \~3.5           | Minimal      | Acceptable    |
| Q4\_K\_M     | \~4.5           | Low          | Good          |
| Q5\_K\_M     | \~5.5           | Moderate     | Excellent     |
| Q6\_K        | \~6.5           | Higher       | Excellent     |
| Q8\_0        | 8               | High         | Near-original |
| F16          | 16              | Highest      | Original      |

**Recommended**: Q4\_K\_M offers the best balance of quality and memory usage for most use cases.

#### [Pulling quantized models](#pulling-quantized-models)

Models on Docker Hub often include quantization in the tag:

```console
$ docker model pull ai/llama3.2:3B-Q4_K_M
```

### [Using llama.cpp](#using-llamacpp)

llama.cpp is the default engine. No special configuration is required:

```console
$ docker model run ai/smollm2
```

To explicitly specify llama.cpp when running models:

```console
$ docker model run ai/smollm2 --backend llama.cpp
```

### [llama.cpp API endpoints](#llamacpp-api-endpoints)

When using llama.cpp, API calls use the llama.cpp engine path:

```text
POST /engines/llama.cpp/v1/chat/completions
```

Or without the engine prefix:

```text
POST /engines/v1/chat/completions
```

## [vLLM](#vllm)

[vLLM](https://github.com/vllm-project/vllm) is a high-performance inference engine optimized for production workloads with high throughput requirements.

### [Platform support](#platform-support-1)

| Platform          | GPU         | Support status                   |
| ----------------- | ----------- | -------------------------------- |
| Linux x86\_64     | NVIDIA CUDA | Supported                        |
| Windows with WSL2 | NVIDIA CUDA | Supported (Docker Desktop 4.54+) |
| macOS             | -           | Not supported                    |
| Linux ARM64       | -           | Not supported                    |
| AMD GPUs          | -           | Not supported                    |

> Important
>
> vLLM requires an NVIDIA GPU with CUDA support. It does not support CPU-only inference.

### [Model format: Safetensors](#model-format-safetensors)

vLLM works with models in Safetensors format, which is the standard format for HuggingFace models. These models typically use more memory than quantized GGUF models but may offer better quality and faster inference on powerful hardware.

### [Setting up vLLM](#setting-up-vllm)

#### [Docker Engine (Linux)](#docker-engine-linux)

Install the Model Runner with vLLM backend:

```console
$ docker model install-runner --backend vllm --gpu cuda
```

Verify the installation:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: c22473b
vllm: running vllm version: 0.11.0
```

#### [Docker Desktop (Windows with WSL2)](#docker-desktop-windows-with-wsl2)

1. Ensure you have:

   * Docker Desktop 4.54 or later (minimum version for vLLM support)
   * NVIDIA GPU with updated drivers
   * WSL2 enabled

2. Install vLLM backend:

   ```console
   $ docker model install-runner --backend vllm --gpu cuda
   ```

### [Running models with vLLM](#running-models-with-vllm)

vLLM models are typically tagged with `-vllm` suffix:

```console
$ docker model run ai/smollm2-vllm
```

To specify the vLLM backend explicitly:

```console
$ docker model run ai/model --backend vllm
```

### [vLLM API endpoints](#vllm-api-endpoints)

When using vLLM, specify the engine in the API path:

```text
POST /engines/vllm/v1/chat/completions
```

### [vLLM configuration](#vllm-configuration)

#### [HuggingFace overrides](#huggingface-overrides)

Use `--hf_overrides` to pass model configuration overrides:

```console
$ docker model configure --hf_overrides '{"max_model_len": 8192}' ai/model-vllm
```

#### [Common vLLM settings](#common-vllm-settings)

| Setting                  | Description                   | Example |
| ------------------------ | ----------------------------- | ------- |
| `max_model_len`          | Maximum context length        | 8192    |
| `gpu_memory_utilization` | Fraction of GPU memory to use | 0.9     |
| `tensor_parallel_size`   | GPUs for tensor parallelism   | 2       |

### [vLLM and llama.cpp performance comparison](#vllm-and-llamacpp-performance-comparison)

| Scenario                       | Recommended engine             |
| ------------------------------ | ------------------------------ |
| Single user, local development | llama.cpp                      |
| Multiple concurrent requests   | vLLM                           |
| Limited GPU memory             | llama.cpp (with quantization)  |
| Maximum throughput             | vLLM                           |
| CPU-only system                | llama.cpp                      |
| Apple Silicon Mac              | llama.cpp                      |
| Production deployment          | vLLM (if hardware supports it) |

## [Diffusers](#diffusers)

[Diffusers](https://github.com/huggingface/diffusers) is an inference engine for image generation models, including Stable Diffusion. Unlike llama.cpp and vLLM which focus on text generation with LLMs, Diffusers enables you to generate images from text prompts.

### [Platform support](#platform-support-2)

| Platform      | GPU         | Support status |
| ------------- | ----------- | -------------- |
| Linux x86\_64 | NVIDIA CUDA | Supported      |
| Linux ARM64   | NVIDIA CUDA | Supported      |
| Windows       | -           | Not supported  |
| macOS         | -           | Not supported  |

> Important
>
> Diffusers requires an NVIDIA GPU with CUDA support. It does not support CPU-only inference.

### [Setting up Diffusers](#setting-up-diffusers)

Install the Model Runner with Diffusers backend:

```console
$ docker model reinstall-runner --backend diffusers --gpu cuda
```

Verify the installation:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: 34ce48d
mlx: not installed
sglang: sglang package not installed
vllm: vLLM binary not found
diffusers: running diffusers version: 0.36.0
```

### [Pulling Diffusers models](#pulling-diffusers-models)

Pull a Stable Diffusion model:

```console
$ docker model pull stable-diffusion:Q4
```

### [Generating images with Diffusers](#generating-images-with-diffusers)

Diffusers uses an image generation API endpoint. To generate an image:

```console
$ curl -s -X POST http://localhost:12434/engines/diffusers/v1/images/generations \
  -H "Content-Type: application/json" \
  -d '{
    "model": "stable-diffusion:Q4",
    "prompt": "A picture of a nice cat",
    "size": "512x512"
  }' | jq -r '.data[0].b64_json' | base64 -d > image.png
```

This command:

1. Sends a POST request to the Diffusers image generation endpoint
2. Specifies the model, prompt, and output image size
3. Extracts the base64-encoded image from the response
4. Decodes it and saves it as `image.png`

### [Diffusers API endpoint](#diffusers-api-endpoint)

When using Diffusers, specify the engine in the API path:

```text
POST /engines/diffusers/v1/images/generations
```

### [Supported parameters](#supported-parameters)

| Parameter | Type   | Description                                                   |
| --------- | ------ | ------------------------------------------------------------- |
| `model`   | string | Required. The model identifier (e.g., `stable-diffusion:Q4`). |
| `prompt`  | string | Required. The text description of the image to generate.      |
| `size`    | string | Image dimensions in `WIDTHxHEIGHT` format (e.g., `512x512`).  |

## [Running multiple engines](#running-multiple-engines)

You can run llama.cpp, vLLM, and Diffusers simultaneously. Docker Model Runner routes requests to the appropriate engine based on the model or explicit engine selection.

Check which engines are running:

```console
$ docker model status
Docker Model Runner is running

Status:
llama.cpp: running llama.cpp version: 34ce48d
mlx: not installed
sglang: sglang package not installed
vllm: running vllm version: 0.11.0
diffusers: running diffusers version: 0.36.0
```

### [Engine-specific API paths](#engine-specific-api-paths)

| Engine      | API path                                   | Use case                              |
| ----------- | ------------------------------------------ | ------------------------------------- |
| llama.cpp   | `/engines/llama.cpp/v1/chat/completions`   | Text generation                       |
| vLLM        | `/engines/vllm/v1/chat/completions`        | Text generation                       |
| Diffusers   | `/engines/diffusers/v1/images/generations` | Image generation                      |
| Auto-select | `/engines/v1/chat/completions`             | Text generation (auto-selects engine) |

## [Managing inference engines](#managing-inference-engines)

### [Install an engine](#install-an-engine)

```console
$ docker model install-runner --backend <engine> [--gpu <type>]
```

Options:

* `--backend`: `llama.cpp`, `vllm`, or `diffusers`
* `--gpu`: `cuda`, `rocm`, `vulkan`, or `metal` (depends on platform)

### [Reinstall an engine](#reinstall-an-engine)

```console
$ docker model reinstall-runner --backend <engine>
```

### [Check engine status](#check-engine-status)

```console
$ docker model status
```

### [View engine logs](#view-engine-logs)

```console
$ docker model logs
```

## [Packaging models for each engine](#packaging-models-for-each-engine)

### [Package a GGUF model (llama.cpp)](#package-a-gguf-model-llamacpp)

```console
$ docker model package --gguf ./model.gguf --push myorg/mymodel:Q4_K_M
```

### [Package a Safetensors model (vLLM)](#package-a-safetensors-model-vllm)

```console
$ docker model package --safetensors ./model/ --push myorg/mymodel-vllm
```

## [Troubleshooting](#troubleshooting)

### [vLLM won't start](#vllm-wont-start)

1. Verify NVIDIA GPU is available:

   ```console
   $ nvidia-smi
   ```

2. Check Docker has GPU access:

   ```console
   $ docker run --rm --gpus all nvidia/cuda:12.0-base nvidia-smi
   ```

3. Verify you're on a supported platform (Linux x86\_64 or Windows WSL2).

### [llama.cpp is slow](#llamacpp-is-slow)

1. Ensure GPU acceleration is working (check logs for Metal/CUDA messages).

2. Try a more aggressive quantization:

   ```console
   $ docker model pull ai/model:Q4_K_M
   ```

3. Reduce context size:

   ```console
   $ docker model configure --context-size 2048 ai/model
   ```

### [Out of memory errors](#out-of-memory-errors)

1. Use a smaller quantization (Q4 instead of Q8).
2. Reduce context size.
3. For vLLM, adjust `gpu_memory_utilization`:
   ```console
   $ docker model configure --hf_overrides '{"gpu_memory_utilization": 0.8}' ai/model
   ```

## [What's next](#whats-next)

* [Configuration options](https://docs.docker.com/ai/model-runner/configuration/) - Detailed parameter reference
* [API reference](https://docs.docker.com/ai/model-runner/api-reference/) - API documentation
* [GPU support](https://docs.docker.com/desktop/features/gpu/) - GPU configuration for Docker Desktop

----
url: https://docs.docker.com/docker-hub/repos/manage/access/
----

# Access management

***

Table of contents

***

In this topic learn about the features available to manage access to your repositories. This includes visibility, collaborators, roles, teams, and organization access tokens.

## [Repository visibility](#repository-visibility)

The most basic repository access is controlled via the visibility. A repository's visibility can be public or private.

With public visibility, the repository appears in Docker Hub search results and can be pulled by everyone. To manage push access to public personal repositories, you can use collaborators. To manage push access to public organization repositories, you can use roles, teams, or organization access tokens.

With private visibility, the repository doesn't appear in Docker Hub search results and is only accessible to those with granted permission. To manage push and pull access to private personal repositories, you can use collaborators. To manage push and pull access to private organization repositories, you can use roles, teams, or organization access tokens.

### [Change repository visibility](#change-repository-visibility)

When creating a repository in Docker Hub, you can set the repository visibility. In addition, you can set the default repository visibility when a repository is created in your personal repository settings. The following describes how to change the visibility after the repository has been created.

To change repository visibility:

1. Sign in to [Docker Hub](https://hub.docker.com).

2. Select **My Hub** > **Repositories**.

3. Select a repository.

   The **General** page for the repository appears.

4. Select the **Settings** tab.

5. Under **Visibility settings**, select one of the following:

   * **Make public**: The repository appears in Docker Hub search results and can be pulled by everyone.
   * **Make private**: The repository doesn't appear in Docker Hub search results and is only accessible to you and collaborators. In addition, if the repository is in an organization's namespace, then the repository is accessible to those with applicable roles or permissions.

6. Type the repository's name to verify the change.

7. Select **Make public** or **Make private**.

## [Collaborators](#collaborators)

A collaborator is someone you want to give `push` and `pull` access to a personal repository. Collaborators aren't able to perform any administrative tasks such as deleting the repository or changing its visibility from private to public. In addition, collaborators can't add other collaborators.

Only personal repositories can use collaborators. You can add unlimited collaborators to public repositories, and Docker Pro accounts can add up to 1 collaborator on private repositories.

Organization repositories can't use collaborators, but can use member roles, teams, or organization access tokens to manage access.

### [Manage collaborators](#manage-collaborators)

1. Sign in to [Docker Hub](https://hub.docker.com).

2. Select **My Hub** > **Repositories**.

   A list of your repositories appears.

3. Select a repository.

   The **General** page for the repository appears.

4. Select the **Collaborators** tab.

5. Add or remove collaborators based on their Docker username.

You can choose collaborators and manage their access to a private repository from that repository's **Settings** page.

## [Organization roles](#organization-roles)

Organizations can use roles for individuals, giving them different permissions in the organization. For more details, see [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/).

## [Organization teams](#organization-teams)

Organizations can use teams. A team can be assigned fine-grained repository access.

### [Configure team repository permissions](#configure-team-repository-permissions)

You must create a team before you are able to configure repository permissions. For more details, see [Create and manage a team](https://docs.docker.com/admin/organization/manage/manage-a-team/).

To configure team repository permissions:

## [Organization access tokens (OATs)](#organization-access-tokens-oats)

Organizations can use OATs. OATs let you assign fine-grained repository access permissions to tokens. For more details, see [Organization access tokens](https://docs.docker.com/enterprise/security/access-tokens/).

## [Gated distribution](#gated-distribution)

Availability: Early Access

Gated distribution allows publishers to securely share private container images with external customers or partners, without giving them full organization access or visibility into your teams, collaborators, or other repositories.

This feature is ideal for commercial software publishers who want to control who can pull specific images while preserving a clean separation between internal users and external consumers.

If you are interested in Gated Distribution contact the [Docker Sales Team](https://www.docker.com/pricing/contact-sales/) for more information.

### [Key features](#key-features)

* **Private repository distribution**: Content is stored in private repositories and only accessible to explicitly invited users.

* **External access without organization membership**: External users don't need to be added to your internal organization to pull images.

* **Pull-only permissions**: External users receive pull-only access and cannot push or modify repository content.

* **Invite-only access**: Access is granted through authenticated email invites, managed via API.

### [Invite distributor members via API](#invite-distributor-members-via-api)

> Note
>
> When you invite members, you assign them a role. See [Roles and permissions](https://docs.docker.com/enterprise/security/roles-and-permissions/) for details about the access permissions for each role.

Distributor members (used for gated distribution) can only be invited using the Docker Hub API. UI-based invitations are not currently supported for this role. To invite distributor members, use the Bulk create invites API endpoint.

To invite distributor members:

1. Use the [Authentication API](https://docs.docker.com/reference/api/hub/latest/#tag/authentication-api/operation/AuthCreateAccessToken) to generate a bearer token for your Docker Hub account.

2. Create a team in the Hub UI or use the [Teams API](https://docs.docker.com/reference/api/hub/latest/#tag/groups/paths/~1v2~1orgs~1%7Borg_name%7D~1groups/post).

3. Grant repository access to the team:

   * In the Hub UI: Navigate to your repository settings and add the team with "Read-only" permissions
   * Using the [Repository Teams API](https://docs.docker.com/reference/api/hub/latest/#tag/repositories/paths/~1v2~1repositories~1%7Bnamespace%7D~1%7Brepository%7D~1groups/post): Assign the team to your repositories with "read-only" access level

4. Use the [Bulk create invites endpoint](https://docs.docker.com/reference/api/hub/latest/#tag/invites/paths/~1v2~1invites~1bulk/post) to send email invites with the distributor member role. In the request body, set the "role" field to "distributor\_member".

5. The invited user will receive an email with a link to accept the invite. After signing in with their Docker ID, they'll be granted pull-only access to the specified private repository as a distributor member.

----
url: https://docs.docker.com/compose/how-tos/multiple-compose-files/extends/
----

# Extend your Compose file

***

Table of contents

***

Docker Compose's [`extends` attribute](https://docs.docker.com/reference/compose-file/services/#extends) lets you share common configurations among different files, or even different projects entirely.

Extending services is useful if you have several services that reuse a common set of configuration options. With `extends` you can define a common set of service options in one place and refer to it from anywhere. You can refer to another Compose file and select a service you want to also use in your own application, with the ability to override some attributes for your own needs.

> Important
>
> When you use multiple Compose files, you must make sure all paths in the files are relative to the base Compose file (i.e. the Compose file in your main-project folder). This is required because extend files need not be valid Compose files. Extend files can contain small fragments of configuration. Tracking which fragment of a service is relative to which path is difficult and confusing, so to keep paths easier to understand, all paths must be defined relative to the base file.

> Note
>
> `extends` is not supported when deploying with `docker stack deploy`. Running `docker stack config` on a Compose file that uses `extends` returns the error: `Configuration contains forbidden properties`.

## [How the `extends` attribute works](#how-the-extends-attribute-works)

### [Extending services from another file](#extending-services-from-another-file)

Take the following example:

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
```

This instructs Compose to reuse only the properties of the `webapp` service defined in the `common-services.yml` file. The `webapp` service itself is not part of the final project.

If `common-services.yml` looks like this:

```yaml
services:
  webapp:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - "/data"
```

You get exactly the same result as if you wrote `compose.yaml` with the same `build`, `ports`, and `volumes` configuration values defined directly under `web`.

To include the service `webapp` in the final project when extending services from another file, you need to explicitly include both services in your current Compose file. For example (this is for illustrative purposes only):

```yaml
services:
  web:
    build: ./alpine
    command: echo
    extends:
      file: common-services.yml
      service: webapp
  webapp:
    extends:
      file: common-services.yml
      service: webapp
```

Alternatively, you can use [include](https://docs.docker.com/compose/how-tos/multiple-compose-files/include/).

### [Extending services within the same file](#extending-services-within-the-same-file)

If you define services in the same Compose file and extend one service from another, both the original service and the extended service will be part of your final configuration. For example:

```yaml
services:
  web:
    build: ./alpine
    extends: webapp
  webapp:
    environment:
      - DEBUG=1
```

### [Extending services within the same file and from another file](#extending-services-within-the-same-file-and-from-another-file)

You can go further and define, or re-define, configuration locally in `compose.yaml`:

```yaml
services:
  web:
    extends:
      file: common-services.yml
      service: webapp
    environment:
      - DEBUG=1
    cpu_shares: 5

  important_web:
    extends: web
    cpu_shares: 10
```

## [Additional example](#additional-example)

Extending an individual service is useful when you have multiple services that have a common configuration. The example below is a Compose app with two services, a web application and a queue worker. Both services use the same codebase and share many configuration options.

The `common.yaml` file defines the common configuration:

```yaml
services:
  app:
    build: .
    environment:
      CONFIG_FILE_PATH: /code/config
      API_KEY: xxxyyy
    cpu_shares: 5
```

The `compose.yaml` defines the concrete services which use the common configuration:

```yaml
services:
  webapp:
    extends:
      file: common.yaml
      service: app
    command: /code/run_web_app
    ports:
      - 8080:8080
    depends_on:
      - queue
      - db

  queue_worker:
    extends:
      file: common.yaml
      service: app
    command: /code/run_worker
    depends_on:
      - queue
```

## [Relative paths](#relative-paths)

When using `extends` with a `file` attribute which points to another folder, relative paths declared by the service being extended are converted so they still point to the same file when used by the extending service. This is illustrated in the following example:

Base Compose file:

```yaml
services:
  webapp:
    image: example
    extends:
      file: ../commons/compose.yaml
      service: base
```

The `commons/compose.yaml` file:

```yaml
services:
  base:
    env_file: ./container.env
```

The resulting service refers to the original `container.env` file within the `commons` directory. This can be confirmed with `docker compose config` which inspects the actual model:

```yaml
services:
  webapp:
    image: example
    env_file: 
      - ../commons/container.env
```

## [Reference information](#reference-information)

* [`extends`](https://docs.docker.com/reference/compose-file/services/#extends)

----
url: https://docs.docker.com/ai/docker-agent/reference/toolsets/
----

# Toolsets reference

***

Table of contents

***

This reference documents the toolsets available in Docker Agent and what each one does. Tools give agents the ability to take action—interacting with files, executing commands, accessing external resources, and managing state.

For configuration file syntax and how to set up toolsets in your agent YAML, see the [Configuration file reference](https://docs.docker.com/ai/docker-agent/reference/config/).

## [How agents use tools](#how-agents-use-tools)

When you configure toolsets for an agent, those tools become available in the agent's context. The agent can invoke tools by name with appropriate parameters based on the task at hand.

Tool invocation flow:

1. Agent analyzes the task and determines which tool to use
2. Agent constructs tool parameters based on requirements
3. Docker Agent executes the tool and returns results
4. Agent processes results and decides next steps

Agents can call multiple tools in sequence or make decisions based on tool results. Tool selection is automatic based on the agent's understanding of the task and available capabilities.

## [Tool types](#tool-types)

Docker Agent supports three types of toolsets:

* Built-in toolsets

  * Core functionality built directly into Docker Agent (`filesystem`, `shell`, `memory`, etc.). These provide essential capabilities for file operations, command execution, and state management. MCP toolsets
  * Tools provided by Model Context Protocol servers, either local processes (stdio) or remote servers (HTTP/SSE). MCP enables access to a wide ecosystem of standardized tools. Custom toolsets
  * Shell scripts wrapped as tools with typed parameters (`script`). This lets you define domain-specific tools for your use case.

## [Configuration](#configuration)

Toolsets are configured in your agent's YAML file under the `toolsets` array:

```yaml
agents:
  my_agent:
    model: anthropic/claude-sonnet-4-5
    description: A helpful coding assistant
    toolsets:
      # Built-in toolset
      - type: filesystem

      # Built-in toolset with configuration
      - type: memory
        path: ./memories.db

      # Local MCP server (stdio)
      - type: mcp
        command: npx
        args: ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"]

      # Remote MCP server (SSE)
      - type: mcp
        remote:
