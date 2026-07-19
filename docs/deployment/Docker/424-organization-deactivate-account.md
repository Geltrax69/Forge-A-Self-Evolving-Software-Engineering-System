url: https://docs.docker.com/admin/organization/deactivate-account/
----

# Deactivate an organization

***

Table of contents

***

For: Administrators

Learn how to deactivate a Docker organization, including required prerequisite steps. For information about deactivating user accounts, see [Deactivate a user account](https://docs.docker.com/accounts/deactivate-user-account/).

> Warning
>
> All Docker products and services that use your Docker account or organization account will be inaccessible after deactivating your account.

## [Prerequisites](#prerequisites)

You must complete all the following steps before you can deactivate your organization:

* Download any images and tags you want to keep. Use `docker pull -a <image>` to pull all tags, or `docker pull <image>:<tag>` to pull a specific tag.
* If you have an active Docker subscription, [downgrade it to a free subscription](https://docs.docker.com/subscription/change/).
* Remove all other members within the organization.
* Unlink your [GitHub and Bitbucket accounts](https://docs.docker.com/docker-hub/repos/manage/builds/link-source/#unlink-a-github-user-account).
* For Business organizations, [remove your SSO connection](https://docs.docker.com/enterprise/security/single-sign-on/manage/#delete-a-connection).

## [Deactivate](#deactivate)

You can deactivate your organization using either the Admin Console or Docker Hub.

> Warning
>
> This cannot be undone. Be sure you've gathered all the data you need from your organization before deactivating it.

1. Sign in to [Docker Home](https://app.docker.com) and select the organization you want to deactivate.
2. Select **Admin Console**, then **Deactivate**. If the **Deactivate** button is unavailable, confirm you've completed all [Prerequisites](#prerequisites).
3. Enter the organization name to confirm deactivation.
4. Select **Deactivate organization**.

----
