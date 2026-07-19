url: https://docs.docker.com/guides/deno/develop/
----

# Use containers for Deno development

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Containerize a Deno application](https://docs.docker.com/guides/deno/containerize/).

## [Overview](#overview)

In this section, you'll learn how to set up a development environment for your containerized application. This includes:

* Configuring Compose to automatically update your running Compose services as you edit and save your code

## [Get the sample application](#get-the-sample-application)

Clone the sample application to use with this guide. Open a terminal, change directory to a directory that you want to work in, and run the following command to clone the repository:

```console
$ git clone https://github.com/dockersamples/docker-deno.git && cd docker-deno
```

## [Automatically update services](#automatically-update-services)

Use Compose Watch to automatically update your running Compose services as you edit and save your code. For more details about Compose Watch, see [Use Compose Watch](https://docs.docker.com/compose/how-tos/file-watch/).

Open your `compose.yml` file in an IDE or text editor and then add the Compose Watch instructions. The following example shows how to add Compose Watch to your `compose.yml` file.

|                                             |                                                                                                                                                                                                                      |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ```
``` | ```yaml
services:
  server:
    image: deno-server
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    develop:
      watch:
        - action: rebuild
          path: .
``` |

Run the following command to run your application with Compose Watch.

```console
$ docker compose watch
```

Now, if you modify your `server.ts` you will see the changes in real time without re-building the image.

To test it out, open the `server.ts` file in your favorite text editor and change the message from `{"Status" : "OK"}` to `{"Status" : "Updated"}`. Save the file and refresh your browser at `http://localhost:8000`. You should see the updated message.

[Configure CI/CD for your Deno application »](https://docs.docker.com/guides/deno/configure-ci-cd/)

----
