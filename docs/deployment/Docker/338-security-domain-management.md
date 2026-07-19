url: https://docs.docker.com/enterprise/security/domain-management/
----

# Add and manage domains

***

Table of contents

***

Subscription: Business

For: Administrators

Domain management lets you add and verify domains for your organization, then enable auto-provisioning to automatically add users when they sign in with email addresses that match your verified domains. This approach simplifies user management, ensures consistent security settings, and reduces the risk of unmanaged users accessing Docker without visibility or control.

This page provides steps to add and delete domains, configure auto-provisioning, and audit uncaptured users.

## [Add and verify a domain](#add-and-verify-a-domain)

Adding a domain requires verification to confirm ownership. The verification process uses DNS records to prove you control the domain.

### [Add a domain](#add-a-domain)

1. Sign in to [Docker Home](https://app.docker.com) and select your organization. If your organization is part of a company, select the company and configure the domain for the organization at the company level.
2. Select **Admin Console**, then **Domain management**.
3. Select **Add a domain**.
4. Enter your domain and select **Add domain**.
5. In the pop-up modal, copy the **TXT Record Value** to verify your domain.

### [Verify a domain](#verify-a-domain)

Verification confirms that you own the domain by adding a TXT record to your Domain Name System (DNS) host. It can take up to 72 hours for the DNS change to propagate. Docker automatically checks for the record and confirms ownership once the change is recognized.

> Tip
>
> The record name field determines where the TXT record is added in your domain (root or subdomain). For root domains like `example.com`, use `@` or leave the record name empty, depending on your provider. Don't enter values like docker, `docker-verification`, `www`, or your domain name, as these may direct to the wrong place. Check your DNS provider's documentation to verify record name requirements.

Follow the steps for your DNS provider to add the **TXT Record Value**. If your provider isn't listed, use the steps for "Other providers":

1. Add your TXT record to AWS by following [Creating records by using the Amazon Route 53 console](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-creating.html).
2. Wait up to 72 hours for TXT record verification.
3. Return to the **Domain management** page of the [Admin Console](https://app.docker.com/admin) and select **Verify** next to your domain name.

1) Add your TXT record to Google Cloud DNS by following [Verifying your domain with a TXT record](https://cloud.google.com/identity/docs/verify-domain-txt).
2) Wait up to 72 hours for TXT record verification.
3) Return to the **Domain management** page of the [Admin Console](https://app.docker.com/admin) and select **Verify** next to your domain name.

1. Add your TXT record to GoDaddy by following [Add a TXT record](https://www.godaddy.com/help/add-a-txt-record-19232).
2. Wait up to 72 hours for TXT record verification.
3. Return to the **Domain management** page of the [Admin Console](https://app.docker.com/admin) and select **Verify** next to your domain name.

1) Sign in to your domain host.
2) Add a TXT record to your DNS settings using the **TXT Record Value** from Docker.
3) Wait up to 72 hours for TXT record verification.
4) Return to the **Domain management** page of the [Admin Console](https://app.docker.com/admin) and select **Verify** next to your domain name.

## [Audit domains for uncaptured users](#audit-domains-for-uncaptured-users)

Domain audit identifies uncaptured users. Uncaptured users are Docker users who have authenticated using an email address associated with your verified domains but aren't members of your Docker organization.

### [Limitations](#limitations)

Domain audit can't identify:

* Users who access Docker Desktop without authenticating
* Users who authenticate using an account that doesn't have an email address associated with one of your verified domains

To prevent unidentifiable users from accessing Docker Desktop, [enforce sign-in](https://docs.docker.com/enterprise/security/enforce-sign-in/).

### [Run a domain audit](#run-a-domain-audit)

1. Sign in to [Docker Home](https://app.docker.com) and choose your company.
2. Select **Admin Console**, then **Domain management**.
3. In **Domain audit**, select **Export Users** to export a CSV file of uncaptured users.

The CSV file contains the following columns:

* Name: Docker user's display name
* Username: Docker ID of the user
* Email: Email address of the user

### [Invite uncaptured users](#invite-uncaptured-users)

You can bulk invite uncaptured users to your organization using the exported CSV file. For more information on bulk inviting users, see [Manage organization members](https://docs.docker.com/admin/organization/manage/members/).

## [Auto-provisioning](#auto-provisioning)

[Auto-provisioning](https://docs.docker.com/enterprise/security/provisioning/auto-provisioning/) uses verified domains to associate organization members with email address that match the verified domains. To override auto-provisioning, you can configure one of the two alternative methods:

* [Just-in-Time (JIT)](https://docs.docker.com/enterprise/security/provisioning/just-in-time/) provisioning
* [System for Cross-domain Identity Management (SCIM)](https://docs.docker.com/enterprise/security/provisioning/scim/)

## [Delete a domain](#delete-a-domain)

Deleting a domain removes its TXT record value and disables any associated auto-provisioning.

> Warning
>
> Deleting a domain will disable auto-provisioning for that domain and remove verification. This action cannot be undone.

To delete a domain:

1. Sign in to [Docker Home](https://app.docker.com) and select your organization. If your organization is part of a company, select the company and configure the domain for the organization at the company level.
2. Select **Admin Console**, then **Domain management**.
3. For the domain you want to delete, select the **Actions** menu, then **Delete domain**.
4. To confirm, select **Delete domain** in the pop-up modal.

----
