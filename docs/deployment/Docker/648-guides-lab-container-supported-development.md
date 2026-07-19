url: https://docs.docker.com/guides/lab-container-supported-development/
----

[Lab: Container-Supported Development](https://docs.docker.com/guides/lab-container-supported-development/)

Hands-on lab: Run dependent services in containers during local development. Start a PostgreSQL database, write a compose.yaml, and add a database visualizer — all without installing anything on the host.

Labs

30 minutes

Resources:

* [Docker Compose docs](/compose/)
* [Bind mounts](/engine/storage/bind-mounts/)
* [Labspace repository](https://github.com/dockersamples/labspace-container-supported-development)

[« Back to all guides](/guides/)

# Lab: Container-Supported Development

***

Table of contents

***

Use containers to run the services your app depends on — databases, caches, message queues — without installing anything locally. This lab walks through running PostgreSQL in a container, writing a `compose.yaml` your whole team can share, and adding a pgAdmin visualizer to the dev stack.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-container-supported-development up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Run a PostgreSQL database in a container with no local installation
* Use bind mounts to seed a database with schema and initial data at startup
* Write a `compose.yaml` that codifies the entire dev stack for the team
* Add a pgAdmin container to visualize and inspect the database
* Understand how containerized dev stacks reduce onboarding time and environment drift

## [Modules](#modules)

| # | Module                           | Description                                                                     |
| - | -------------------------------- | ------------------------------------------------------------------------------- |
| 1 | Introduction                     | Meet the sample app and understand the container-supported development approach |
| 2 | Running a Containerized Database | Start PostgreSQL, connect the app, and seed the database using bind mounts      |
| 3 | Making Life Easier with Compose  | Replace `docker run` commands with a shared `compose.yaml`                      |
| 4 | Adding Dev Tools                 | Add pgAdmin to the Compose stack for database visualization                     |
| 5 | Recap                            | Review key takeaways and explore related guides                                 |

----
