url: https://docs.docker.com/guides/lab-attestation-basics/
----

[Lab: Container Image Attestations](https://docs.docker.com/guides/lab-attestation-basics/)

Hands-on lab: Add supply chain metadata to a container image. Generate SBOMs and SLSA provenance with BuildKit, sign images with Cosign, and attach OpenVEX statements to declare vulnerability exploitability status.

Labs

45 minutes

Resources:

* [Build attestations](/build/metadata/attestations/)
* [SBOM attestations](/build/metadata/attestations/sbom/)
* [Provenance attestations](/build/metadata/attestations/slsa-provenance/)
* [Labspace repository](https://github.com/dockersamples/labspace-attestation-basics)

[« Back to all guides](/guides/)

# Lab: Container Image Attestations

***

Table of contents

***

Prove where your container images came from and that they haven't been tampered with. This lab walks through generating SBOMs and SLSA build provenance with BuildKit, signing images with Cosign, and writing VEX statements to declare which CVEs affect your image — the techniques used to meet supply chain security requirements like NIST SSDF and EO 14028.

## [Launch the lab](#launch-the-lab)

1. Start the labspace:

   ```console
   $ docker compose -p labspace -f oci://dockersamples/labspace-attestation-basics up -d
   ```

2. Open your browser to <http://localhost:3030>.

3. When you're done, tear down the labspace:

   ```console
   $ docker compose -p labspace down
   ```

## [What you'll learn](#what-youll-learn)

By the end of this Labspace, you will have completed the following:

* Generate and inspect an SPDX SBOM attached to a container image with `--sbom=true`
* Generate SLSA build provenance with `--provenance=mode=max` and understand how multi-stage builds are fully recorded
* Install Cosign and use key-based signing to sign and verify a container image
* Write an OpenVEX statement to declare CVE exploitability status and attach it as a signed attestation
* Understand how SBOMs, provenance, signatures, and VEX complement each other in a complete supply chain story

## [Modules](#modules)

| # | Module                            | Description                                                                          |
| - | --------------------------------- | ------------------------------------------------------------------------------------ |
| 1 | Introduction                      | Overview of supply chain attestations and the sample Go app                          |
| 2 | Software Bill of Materials (SBOM) | Build with `--sbom=true`, inspect SPDX contents, and understand scanner integration  |
| 3 | Build Provenance                  | Generate SLSA provenance and explore how multi-stage builds are recorded             |
| 4 | Signing Images with Cosign        | Generate a key pair, sign the image, verify the signature, and learn keyless signing |
| 5 | VEX Statements                    | Scan for CVEs, write an OpenVEX document, and attach it as a signed attestation      |
| 6 | Bringing It All Together          | Run the complete build-sign-attest workflow and see the full supply chain picture    |
| 7 | Recap                             | Summary of skills and next steps for policy enforcement and higher SLSA levels       |

----
