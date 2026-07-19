url: https://docs.docker.com/guides/reactjs/configure-github-actions/
----

# Automate your builds with GitHub Actions

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete all the previous sections of this guide, starting with [Containerize React.js application](https://docs.docker.com/guides/reactjs/containerize/).

You must also have:

* A [GitHub](https://github.com/signup) account.
* A verified [Docker Hub](https://hub.docker.com/signup) account.

***

## [Overview](#overview)

In this section, you'll set up a CI/CD pipeline using [GitHub Actions](https://docs.github.com/en/actions) to automatically:

* Build your React.js application inside a Docker container.
* Run tests in a consistent environment.
* Push the production-ready image to [Docker Hub](https://hub.docker.com).

***

## [Connect your GitHub repository to Docker Hub](#connect-your-github-repository-to-docker-hub)

To enable GitHub Actions to build and push Docker images, you’ll securely store your Docker Hub credentials in your new GitHub repository.

### [Step 1: Connect your GitHub repository to Docker Hub](#step-1-connect-your-github-repository-to-docker-hub)

1. Create a Personal Access Token (PAT) from [Docker Hub](https://hub.docker.com)

   1. Go to your **Docker Hub account → Account Settings → Security**.
   2. Generate a new Access Token with **Read/Write** permissions.
   3. Name it something like `docker-reactjs-sample`.
   4. Copy and save the token — you’ll need it in Step 4.

2. Create a repository in [Docker Hub](https://hub.docker.com/repositories/)

   1. Go to your **Docker Hub account → Create a repository**.
   2. For the Repository Name, use something descriptive — for example: `reactjs-sample`.
   3. Once created, copy and save the repository name — you’ll need it in Step 4.

3. Create a new [GitHub repository](https://github.com/new) for your React.js project

4. Add Docker Hub credentials as GitHub repository secrets

   In your newly created GitHub repository:

   1. Navigate to: **Settings → Secrets and variables → Actions → New repository secret**.

   2. Add the following secrets:

   | Name                     | Value                                            |
   | ------------------------ | ------------------------------------------------ |
   | `DOCKER_USERNAME`        | Your Docker Hub username                         |
   | `DOCKERHUB_TOKEN`        | Your Docker Hub access token (created in Step 1) |
   | `DOCKERHUB_PROJECT_NAME` | Your Docker Project Name (created in Step 2)     |

   These secrets let GitHub Actions to authenticate securely with Docker Hub during automated workflows.

5. Connect Your Local Project to GitHub

   Link your local project `docker-reactjs-sample` to the GitHub repository you just created by running the following command from your project root:

   ```console
      $ git remote set-url origin https://github.com/{your-username}/{your-repository-name}.git
   ```

   > Important
   >
   > Replace `{your-username}` and `{your-repository}` with your actual GitHub username and repository name.

   To confirm that your local project is correctly connected to the remote GitHub repository, run:

   ```console
   $ git remote -v
   ```

   You should see output similar to:

   ```console
   origin  https://github.com/{your-username}/{your-repository-name}.git (fetch)
   origin  https://github.com/{your-username}/{your-repository-name}.git (push)
   ```

   This confirms that your local repository is properly linked and ready to push your source code to GitHub.

6. Push Your Source Code to GitHub

   Follow these steps to commit and push your local project to your GitHub repository:

   1. Stage all files for commit.

      ```console
      $ git add -A
      ```

      This command stages all changes — including new, modified, and deleted files — preparing them for commit.

   2. Commit your changes.

      ```console
      $ git commit -m "Initial commit"
      ```

      This command creates a commit that snapshots the staged changes with a descriptive message.

   3. Push the code to the `main` branch.

      ```console
      $ git push -u origin main
      ```

      This command pushes your local commits to the `main` branch of the remote GitHub repository and sets the upstream branch.

Once completed, your code will be available on GitHub, and any GitHub Actions workflow you’ve configured will run automatically.

> Note
>
> Learn more about the Git commands used in this step:
>
> * [Git add](https://git-scm.com/docs/git-add) – Stage changes (new, modified, deleted) for commit
> * [Git commit](https://git-scm.com/docs/git-commit) – Save a snapshot of your staged changes
> * [Git push](https://git-scm.com/docs/git-push) – Upload local commits to your GitHub repository
> * [Git remote](https://git-scm.com/docs/git-remote) – View and manage remote repository URLs

***

### [Step 2: Set up the workflow](#step-2-set-up-the-workflow)

Now you'll create a GitHub Actions workflow that builds your Docker image, runs tests, and pushes the image to Docker Hub.

1. Go to your repository on GitHub and select the **Actions** tab in the top menu.

2. Select **Set up a workflow yourself** when prompted.

   This opens an inline editor to create a new workflow file. By default, it will be saved to: `.github/workflows/main.yml`

3. Add the following workflow configuration to the new file:

```yaml
name: CI/CD – React.js Application with Docker

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
    types: [opened, synchronize, reopened]

jobs:
  build-test-push:
    name: Build, Test and Push Docker Image
    runs-on: ubuntu-latest

    steps:
      # 1. Checkout source code
      - name: Checkout source code
        uses: actions/checkout@v6
        with:
          fetch-depth: 0 # Fetches full history for better caching/context

      # 2. Set up Docker Buildx
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v4

      # 3. Cache Docker layers
      - name: Cache Docker layers
        uses: actions/cache@v5
        with:
          path: /tmp/.buildx-cache
          key: ${{ runner.os }}-buildx-${{ github.sha }}
          restore-keys: ${{ runner.os }}-buildx-

      # 4. Cache npm dependencies
      - name: Cache npm dependencies
        uses: actions/cache@v5
        with:
          path: ~/.npm
          key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-npm-

      # 5. Extract metadata
      - name: Extract metadata
        id: meta
        run: |
          echo "REPO_NAME=${GITHUB_REPOSITORY##*/}" >> "$GITHUB_OUTPUT"
          echo "SHORT_SHA=${GITHUB_SHA::7}" >> "$GITHUB_OUTPUT"

      # 6. Build dev Docker image
      - name: Build Docker image for tests
        uses: docker/build-push-action@v7
        with:
          context: .
          file: Dockerfile.dev
          tags: ${{ steps.meta.outputs.REPO_NAME }}-dev:latest
          load: true # Load to local Docker daemon for testing
          cache-from: type=local,src=/tmp/.buildx-cache
          cache-to: type=local,dest=/tmp/.buildx-cache,mode=max

      # 7. Run Vitest tests
      - name: Run Vitest tests and generate report
        run: |
          docker run --rm \
            --workdir /app \
            --entrypoint "" \
            ${{ steps.meta.outputs.REPO_NAME }}-dev:latest \
            sh -c "npm ci && npx vitest run --reporter=verbose"
        env:
          CI: true
          NODE_ENV: test
        timeout-minutes: 10

      # 8. Login to Docker Hub
      - name: Log in to Docker Hub
        uses: docker/login-action@v4
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      # 9. Build and push prod image
      - name: Build and push production image
        uses: docker/build-push-action@v7
        with:
          context: .
          file: Dockerfile
          push: true
          platforms: linux/amd64,linux/arm64
          tags: |
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:latest
            ${{ secrets.DOCKER_USERNAME }}/${{ secrets.DOCKERHUB_PROJECT_NAME }}:${{ steps.meta.outputs.SHORT_SHA }}
          cache-from: type=local,src=/tmp/.buildx-cache
```

This workflow performs the following tasks for your React.js application:

> Note
>
> For more information about `docker/build-push-action`, refer to the [GitHub Action README](https://github.com/docker/build-push-action/blob/master/README.md).

***

     * Repository name: `${your-repository-name}`

     * Tags include:

       * `latest` – represents the most recent successful build; ideal for quick testing or deployment.
       * `<short-sha>` – a unique identifier based on the commit hash, useful for version tracking, rollbacks, and traceability.

> Tip
>
> To maintain code quality and prevent accidental direct pushes, enable branch protection rules:
>
> * Navigate to your **GitHub repo → Settings → Branches**.
>
> * Under Branch protection rules, click **Add rule**.
>
> * Specify `main` as the branch name.
>
> * Enable options like:
>
>   * *Require a pull request before merging*.
>   * *Require status checks to pass before merging*.
>
> This ensures that only tested and reviewed code is merged into `main` branch.

***

## [Summary](#summary)

In this section, you set up a complete CI/CD pipeline for your containerized React.js application using GitHub Actions.

With this setup, your React.js application is now ready for automated testing and deployment across environments — increasing confidence, consistency, and team productivity.

***

***

## [Next steps](#next-steps)

Next, learn how you can locally test and debug your React.js workloads on Kubernetes before deploying. This helps you ensure your application behaves as expected in a production-like environment, reducing surprises during deployment.

[Test your React.js deployment »](https://docs.docker.com/guides/reactjs/deploy/)

----
