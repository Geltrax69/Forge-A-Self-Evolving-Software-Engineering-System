url: https://docs.docker.com/guides/lab-container-getting-started/
----

[Lab: Getting Started with Docker](https://docs.docker.com/guides/lab-container-getting-started/)

Hands-on lab: Run your first containers, write a Dockerfile, build a custom image from a Node.js app, and optionally push it to Docker Hub.

Labs

30 minutes

Resources:

* [Docker overview](/get-started/docker-overview/)
* [Dockerfile reference](/reference/dockerfile/)
* [Labspace repository](https://github.com/dockersamples/labspace-container-getting-started)

[« Back to all guides](/guides/)

# Lab: Getting Started with Docker

***

Table of contents

***

Start from zero and learn Docker's core building blocks. You'll run pre-built containers, write a `Dockerfile` to package a Node.js app, build your own image, and see container immutability and isolation in action.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-container-getting-started up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Understand what containers are and how they differ from virtual machines
* Run containers in the background, inspect their logs and filesystem, and manage their lifecycle
* Write a `Dockerfile` to package an application, using layer caching for fast rebuilds
* Build a custom image with `docker build` and run it as a container
* Optionally publish your image to Docker Hub

## [Modules](#modules)

| # | Module                    | Description                                                                    |
| - | ------------------------- | ------------------------------------------------------------------------------ |
| 1 | Welcome to Docker         | Introduction to containers and running your first `hello-world` container      |
| 2 | Running Containers        | Launch Nginx, inspect logs and internals, and manage the container lifecycle   |
| 3 | Building Your First Image | Write a `Dockerfile` and build a custom image from a Node.js app               |
| 4 | Running Your App          | Run your image, explore container isolation, and optionally push to Docker Hub |
| 5 | Wrap-up                   | Summary of key concepts and next steps                                         |

----
