url: https://docs.docker.com/subscription/change/
----

# Change your subscription

***

Table of contents

***

You can upgrade or downgrade your Docker subscription at any time to match your changing needs. This page explains how to make subscription changes and what to expect with billing and feature access.

## [Upgrade your subscription](#upgrade-your-subscription)

When you upgrade your Docker subscription, you immediately get access to all features and entitlements in your new subscription tier.

> Tip
>
> If you're upgrading from a Personal subscription to a Team subscription and want to keep your username, [convert your user account into an organization](https://docs.docker.com/admin/organization/setup/convert-account/).

To upgrade your subscription:

1. Sign in to [Docker Home](https://app.docker.com/) and select the organization you want to upgrade.

2. Select **Billing** to view your current plans.

3. Select **Browse products**.

4. Choose **View plans** from the Docker product tile on the products catalog page.

5. Choose a Docker Team or Docker Business plan for the organization.

6. Follow the on-screen instructions to complete your upgrade.

   * If you choose to pay using a US bank account, you must verify the account.
   * For more information, see [Verify a bank account](https://docs.docker.com/billing/payment-method/#verify-a-bank-account).

For detailed feature information, see [Docker Pricing](https://www.docker.com/pricing?ref=Docs\&refAction=DocsSubscriptionChange).

## [Downgrade considerations](#downgrade-considerations)

Consider the following before downgrading:

* Team size and repositories: You may need to reduce team members and convert private repositories to public or delete them based on your new subscription limits.
* SSO and SCIM: If downgrading from Docker Business and your organization uses single sign-on, remove your SSO connection and verified domains first. Organization members who were auto-provisioned through SCIM need to reset their passwords to sign in without SSO.
* Private repository collaborators: Personal subscriptions don't include collaborators for private repositories. When downgrading from Pro to Personal, all collaborators are removed and additional private repositories are locked.

For feature limits in each tier, see [Docker Pricing](https://www.docker.com/pricing?ref=Docs\&refAction=DocsSubscriptionChange).

## [Downgrade your subscription](#downgrade-your-subscription)

You can downgrade your Docker subscription at any time before the renewal date. The unused portion isn't refundable, but you retain access to paid features until the end of the current billing cycle.

To downgrade your subscription:

1. Sign in to [Docker Home](https://app.docker.com/) and select the organization you want to downgrade.
2. Select **Billing**.
3. Select the action menu, then **Cancel subscription**.
4. Fill out the feedback survey to continue with cancellation.

> Important
>
> If you have a sales-assisted Docker Business subscription, contact your account manager to downgrade your subscription.

## [Subscription pause policy](#subscription-pause-policy)

You can't pause or delay a subscription. If a subscription invoice isn't paid by the due date, there's a 15-day grace period starting from the due date.

----
