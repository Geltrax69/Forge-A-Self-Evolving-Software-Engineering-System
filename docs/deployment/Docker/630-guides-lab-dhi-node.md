url: https://docs.docker.com/guides/lab-dhi-node/
----

[Lab: Migrating a Node App to Docker Hardened Images](https://docs.docker.com/guides/lab-dhi-node/)

Hands-on lab: Replace a Node.js base image with a Docker Hardened Image. Analyze CVEs with Docker Scout, rewrite the Dockerfile to use multi-stage builds with DHI, and explore SBOMs, VEX, and compliance attestations.

Labs Docker Hardened Images

30 minutes

Resources:

* [Docker Hardened Images](/dhi/)
* [Docker Scout docs](/scout/)
* [Build attestations](/build/metadata/attestations/)
* [Labspace repository](https://github.com/dockersamples/labspace-dhi-node)

[« Back to all guides](/guides/)

# Lab: Migrating a Node App to Docker Hardened Images

***

Table of contents

***

Migrate a Node.js application from a standard `node:24-trixie-slim` base image to a Docker Hardened Image. You'll measure the before-and-after impact on CVE count, image size, and policy compliance using Docker Scout, then explore the supply chain attestations DHI ships with every image.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-dhi-node up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Analyze a Node.js container image with Docker Scout to identify CVE and policy failures
* Rewrite a Dockerfile to use a multi-stage build with DHI dev and runtime variants
* Compare image size and vulnerability counts before and after the migration
* Inspect supply chain attestations included with Docker Hardened Images (SBOMs, SLSA, VEX)
* Export VEX documents for integration with external scanners such as Grype or Trivy

## [Modules](#modules)

| # | Module                                   | Description                                                                     |
| - | ---------------------------------------- | ------------------------------------------------------------------------------- |
| 1 | Introduction                             | Overview of Docker Hardened Images and their security benefits                  |
| 2 | Setup                                    | Perform setup tasks required for the lab.                                       |
| 3 | Analyzing the Starting Image             | Build the app, scan it with Docker Scout, and review failing policies           |
| 4 | Migrating to DHI                         | Rewrite the Dockerfile with multi-stage DHI build and compare results           |
| 5 | DHI Attestations and Scanner Integration | Inspect SBOMs, FIPS attestations, STIG scans, and export VEX for external tools |

----
