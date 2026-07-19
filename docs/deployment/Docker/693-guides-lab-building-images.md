url: https://docs.docker.com/guides/lab-building-images/
----

[Lab: Building Container Images](https://docs.docker.com/guides/lab-building-images/)

Hands-on lab: Transform a basic Dockerfile into a production-ready image. Master layer caching, multi-stage builds, .dockerignore, non-root users, base image selection, and build secrets.

Labs

45 minutes

Resources:

* [Dockerfile reference](/reference/dockerfile/)
* [Multi-stage builds](/build/building/multi-stage/)
* [Build secrets](/build/building/secrets/)
* [Labspace repository](https://github.com/dockersamples/labspace-building-images)

[« Back to all guides](/guides/)

# Lab: Building Container Images

***

Table of contents

***

Take a working but naïve Dockerfile and progressively improve it into a production-grade image. Each section introduces one technique, applied to a real Python Flask app, so you can see the impact directly.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-building-images up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Read an image's layer history and understand the layer cleanup pitfall
* Restructure a Dockerfile for fast, cache-efficient incremental builds
* Write a `.dockerignore` file and run containers as a non-root user
* Use multi-stage builds to run tests as a build gate and dramatically reduce image size
* Choose the right base image for production, including Docker Hardened Images
* Inject secrets safely at build time using `--mount=type=secret`

## [Modules](#modules)

| # | Module                     | Description                                                            |
| - | -------------------------- | ---------------------------------------------------------------------- |
| 1 | Welcome & Your First Build | Explore the sample app and build the initial image                     |
| 2 | Understanding Image Layers | Inspect layers with `docker history` and see the layer cleanup pitfall |
| 3 | Dockerfile Best Practices  | Fix cache ordering, add `.dockerignore`, and switch to a non-root user |
| 4 | Multi-Stage Builds         | Run tests as a build gate and use a slim base for the production stage |
| 5 | Choosing a Base Image      | Compare slim, Alpine, and Docker Hardened Images                       |
| 6 | Build Secrets              | Show why `ARG` leaks secrets and use `--mount=type=secret` safely      |
| 7 | Wrap-up                    | Review the complete best-practices checklist and next steps            |

----
