url: https://docs.docker.com/enterprise/security/single-sign-on/
----

# Single sign-on overview

***

Table of contents

***

Subscription: Business

For: Administrators

Single sign-on (SSO) lets users access Docker by authenticating through their identity providers (IdPs). SSO can be configured for an entire company, including all associated organizations, or for a single organization that has a Docker Business subscription.

## [How SSO works](#how-sso-works)

When SSO is enabled, Docker supports a non-IdP-initiated flow for user sign-in. Instead of signing in with a Docker username and password, users are redirected to your IdP’s sign-in page. Users must initiate the SSO authentication process by signing in to Docker Hub or Docker Desktop.

The following diagram illustrates how SSO operates and is managed between Docker Hub, Docker Desktop, and your IdP.

## [Set up SSO](#set-up-sso)

To configure SSO in Docker, follow these steps:

1. [Configure your domain](https://docs.docker.com/enterprise/security/single-sign-on/connect/) by creating and verifying it.
2. [Create your SSO connection](https://docs.docker.com/enterprise/security/single-sign-on/connect/) in Docker and your IdP.
3. Link Docker to your identity provider.
4. Test your SSO connection.
5. Provision users in Docker.
6. Optional. [Enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).
7. [Manage your SSO configuration](https://docs.docker.com/enterprise/security/single-sign-on/manage/).

Once configuration is complete, users can sign in to Docker services using their company email address. After signing in, users are added to your company, assigned to an organization, and added to a team.

> Important
>
> Docker plans to deprecate CLI password-based sign-in in future releases. Using a PAT ensures continued CLI access. For more information, see the [security announcement](https://docs.docker.com/security/security-announcements/#deprecation-of-password-logins-on-cli-when-sso-enforced).

## [Next steps](#next-steps)

* Start [configuring SSO](https://docs.docker.com/enterprise/security/single-sign-on/connect/).
* Read the [FAQs](https://docs.docker.com/enterprise/security/single-sign-on/faqs/general/).
* [Troubleshoot](https://docs.docker.com/enterprise/security/single-sign-on/troubleshoot-sso/) SSO issues.

----
