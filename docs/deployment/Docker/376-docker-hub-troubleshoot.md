url: https://docs.docker.com/docker-hub/troubleshoot/
----

# Troubleshoot Docker Hub

***

Table of contents

***

If you experience issues with Docker Hub, refer to the following solutions.

## [You have reached your pull rate limit (429 response code)](#you-have-reached-your-pull-rate-limit-429-response-code)

### [Error message](#error-message)

When this issue occurs, you receive following error message in the Docker CLI or in the Docker Engine logs:

```text
You have reached your pull rate limit. You may increase the limit by authenticating and upgrading: https://www.docker.com/increase-rate-limits
```

### [Possible causes](#possible-causes)

* You have reached your pull rate limit as an authenticated Docker Personal user.
* You have reached your pull rate limit as an unauthenticated user based on your IPv4 address or IPv6 /64 subnet.

### [Solution](#solution)

You can use one of the following solutions:

* [Authenticate](https://docs.docker.com/docker-hub/usage/pulls/#authentication) or [upgrade](https://docs.docker.com/subscription/change/#upgrade-your-subscription) your Docker account.
* [View your pull rate limit](https://docs.docker.com/docker-hub/usage/pulls/#view-hourly-pull-rate-and-limit), wait until your pull rate limit decreases, and then try again.

## [Too many requests (429 response code)](#too-many-requests-429-response-code)

### [Error message](#error-message-1)

When this issue occurs, you receive following error message in the Docker CLI or in the Docker Engine logs:

```text
Too Many Requests
```

### [Possible causes](#possible-causes-1)

* You have reached the [Abuse rate limit](https://docs.docker.com/docker-hub/usage/#abuse-rate-limit).

### [Solution](#solution-1)

1. Check for broken CI/CD pipelines accessing Docker Hub and fix them.
2. Implement a retry with back-off solution in your automated scripts to ensure that you're not resending thousands of requests per minute.

## [500 response code](#500-response-code)

### [Error message](#error-message-2)

When this issue occurs, the following error message is common in the Docker CLI or in the Docker Engine logs:

```text
Unexpected status code 500
```

### [Possible causes](#possible-causes-2)

* There is a temporary Docker Hub service issue.

### [Solution](#solution-2)

1. View the [Docker System Status Page](https://www.dockerstatus.com/) and verify that all services are operational.
2. Try accessing Docker Hub again. It may be a temporary issue.
3. [Contact Docker Support](https://www.docker.com/support/) to report the issue.

----
