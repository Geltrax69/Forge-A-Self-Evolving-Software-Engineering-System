url: https://react.dev/community/versioning-policy
----

[Community](/community)

# Versioning Policy[](#undefined "Link for this heading")

All stable builds of React go through a high level of testing and follow semantic versioning (semver). React also offers unstable release channels to encourage early feedback on experimental features. This page describes what you can expect from React releases.

This versioning policy describes our approach to version numbers for packages such as `react` and `react-dom`. For a list of previous releases, see the [Versions](/versions) page.

We know our users continue to use old versions of React in production. If we learn of a security vulnerability in React, we release a backported fix for all major versions that are affected by the vulnerability.

### Breaking changes[](#breaking-changes "Link for Breaking changes ")

  ```
  npm update react@canary react-dom@canary
  ```

  Or yarn:

  ```
  yarn upgrade react@canary react-dom@canary
  ```

***

----
