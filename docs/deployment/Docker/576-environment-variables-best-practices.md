url: https://docs.docker.com/compose/how-tos/environment-variables/best-practices/
----

# Best practices for working with environment variables in Docker Compose

***

Table of contents

***

#### [Handle sensitive information securely](#handle-sensitive-information-securely)

Be cautious about including sensitive data in environment variables. Consider using [Secrets](https://docs.docker.com/compose/how-tos/use-secrets/) for managing sensitive information.

#### [Understand environment variable precedence](#understand-environment-variable-precedence)

Be aware of how Docker Compose handles the [precedence of environment variables](https://docs.docker.com/compose/how-tos/environment-variables/envvars-precedence/) from different sources (`.env` files, shell variables, Dockerfiles).

#### [Use specific environment files](#use-specific-environment-files)

Consider how your application adapts to different environments. For example development, testing, production, and use different `.env` files as needed.

#### [Know interpolation](#know-interpolation)

Understand how [interpolation](https://docs.docker.com/compose/how-tos/environment-variables/variable-interpolation/) works within compose files for dynamic configurations.

#### [Command line overrides](#command-line-overrides)

Be aware that you can [override environment variables](https://docs.docker.com/compose/how-tos/environment-variables/set-environment-variables/#cli) from the command line when starting containers. This is useful for testing or when you have temporary changes.

----
