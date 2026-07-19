url: https://docs.docker.com/guides/lab-containerized-sdlc/
----

[Lab: The Containerized SDLC](https://docs.docker.com/guides/lab-containerized-sdlc/)

Hands-on lab: Take a Node.js app from source to live Kubernetes deployment using Docker Compose, Testcontainers, Gitea Actions CI/CD, and kubectl — with containers at every stage of the SDLC.

Labs

60 minutes

Resources:

* [Docker Compose docs](/compose/)
* [Testcontainers docs](https://testcontainers.com/)
* [Labspace repository](https://github.com/dockersamples/labspace-containerized-sdlc)

[« Back to all guides](/guides/)

# Lab: The Containerized SDLC

***

Table of contents

***

Build a real Node.js API, then apply containers at every stage of the software development lifecycle. You'll write a Compose file for local development, integration tests using Testcontainers, a CI/CD pipeline, and Kubernetes manifests — using the same container image throughout.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-containerized-sdlc up -d
   ```

2. Open your browser to <http://dockerlabs.xyz>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Set up a containerized local development environment with Docker Compose and Compose Watch
* Write integration tests that spin up a real database using Testcontainers
* Build a CI/CD pipeline that tests, builds, and pushes a container image automatically
* Write Kubernetes manifests and deploy a live application to a k3s cluster
* Configure the pipeline to cause an automatic deployment on every push to `main`

## [Modules](#modules)

| # | Module                                    | Description                                                              |
| - | ----------------------------------------- | ------------------------------------------------------------------------ |
| 1 | Introduction: Meet the App                | Tour the TaskFlow API and understand the SDLC journey ahead              |
| 2 | Local Dev with Docker Compose             | Write a `compose.yaml` to provision a local database and visualizer      |
| 3 | Containerizing Your Dev Environment       | Add the app to Compose with hot-reloading via Compose Watch              |
| 4 | Integration Testing with Testcontainers   | Write self-contained tests that start a real PostgreSQL container        |
| 5 | Continuous Integration with Gitea Actions | Build a pipeline that tests, builds, and pushes a container image        |
| 6 | Deploying to Kubernetes                   | Write manifests and deploy to a live k3s cluster with automated rollouts |
| 7 | The Containerized SDLC: A Recap           | Review the portability, consistency, and reproducibility gains           |

----
