url: https://docs.docker.com/guides/nextjs/
----

# Containerize a Next.js application

Table of contents

***

This guide explains how to containerize Next.js applications, set up development and testing in containers, automate builds with GitHub Actions, and deploy to Kubernetes.

**Time to complete** 20 minutes

This guide shows you how to containerize a Next.js application using Docker, following best practices for creating efficient, production-ready containers.

[Next.js](https://nextjs.org/) is a React framework that enables server-side rendering, static site generation, and full-stack capabilities. Docker provides a consistent containerized environment from development to production.

> **Acknowledgment**
>
> Docker extends its sincere gratitude to [Kristiyan Velkov](https://www.linkedin.com/in/kristiyan-velkov-763130b3/) for authoring this guide and contributing the official [Next.js Docker examples](https://github.com/vercel/next.js/tree/canary/examples/with-docker) to the Vercel Next.js repository, including the standalone and export output examples. As a Docker Captain and experienced engineer, his expertise in Docker, DevOps, and modern web development has made this resource invaluable for the community, helping developers navigate and optimize their Docker workflows.

***

## [What will you learn?](#what-will-you-learn)

In this guide, you will learn how to:

* Containerize and run a Next.js application using Docker.
* Set up a local development environment for Next.js inside a container.
* Run tests for your Next.js application within a Docker container.
* Configure a CI/CD pipeline using GitHub Actions for your containerized app.
* Deploy the containerized Next.js application to a local Kubernetes cluster for testing and debugging.

To begin, you'll start by containerizing an existing Next.js application.

***

## [Prerequisites](#prerequisites)

Before you begin, make sure you're familiar with the following:

* Basic understanding of [JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) or [TypeScript](https://www.typescriptlang.org/).
* Basic knowledge of [Node.js](https://nodejs.org/en) and [npm](https://docs.npmjs.com/about-npm) for managing dependencies and running scripts.
* Familiarity with [React](https://react.dev/) and [Next.js](https://nextjs.org/) fundamentals.
* Understanding of Docker concepts such as images, containers, and Dockerfiles. If you're new to Docker, start with the [Docker basics](https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-a-container/) guide.

Once you've completed the Next.js getting started modules, you'll be ready to containerize your own Next.js application using the examples and instructions provided in this guide.

## [Modules](#modules)

1. [Containerize](https://docs.docker.com/guides/nextjs/containerize/)

   Learn how to containerize a Next.js application with Docker by creating an optimized, production-ready image using best practices for performance, security, and scalability.

2. [Develop your app](https://docs.docker.com/guides/nextjs/develop/)

   Learn how to develop your Next.js application locally using containers.

3. [Run your tests and lint](https://docs.docker.com/guides/nextjs/run-tests/)

   Learn how to run your Next.js tests and lint in a container.

4. [GitHub Actions CI](https://docs.docker.com/guides/nextjs/configure-github-actions/)

   Learn how to configure CI/CD using GitHub Actions for your Next.js application.

5. [Test your deployment](https://docs.docker.com/guides/nextjs/deploy/)

   Learn how to deploy locally to test and debug your Kubernetes deployment

----
