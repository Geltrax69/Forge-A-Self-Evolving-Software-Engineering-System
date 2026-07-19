url: https://docs.docker.com/guides/nodejs/containerize/
----

# Containerize a Node.js application

***

Table of contents

***

## [Prerequisites](#prerequisites)

* You have installed the latest version of [Docker Desktop](https://docs.docker.com/get-started/get-docker/).
* You're familiar with basic Docker concepts. If you're new to Docker, start with [Get started](/get-started/introduction/).

## [Overview](#overview)

Containerizing your application means packaging it together with its dependencies, configuration, and runtime into a single portable unit called a container image. Running that image creates a container, an isolated process that behaves the same on any machine, whether it's your laptop, a CI runner, or a production server.

In this section, you'll containerize a simple [Express.js](https://expressjs.com/) API written in TypeScript. You'll write a `Dockerfile` that describes how to build the image, add a `compose.yaml` file that defines how Docker runs your container, and then build and start the application with one command.

You'll use [Docker Hardened Images](/dhi/) as the base. These are minimal, secure Node.js images maintained by Docker.

This guide focuses on a backend Node.js API. If you're building a standalone frontend application, Docker has dedicated guides for [React.js](/guides/reactjs/), [Vue.js](/guides/vuejs/), [Angular](/guides/angular/), and [Next.js](/guides/nextjs/).

## [Create the application](#create-the-application)

The sample application is a minimal Express API with a single endpoint that returns a JSON greeting. Create the following files in a new `nodejs-docker-example` directory. To create all the files at once, switch to the **Scaffold script** tab in the file browser and copy the shell command.

nodejs-docker-example

```typescript
// A minimal Express application.
// The root endpoint (GET /) returns a JSON greeting.
// See https://expressjs.com/ for the framework reference.

import express, { type Request, type Response } from 'express';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

```json
{
  // TypeScript compiler configuration for the Node.js application.
  // Compiles src/ to dist/ as CommonJS modules targeting ES2022.
  // See https://www.typescriptlang.org/tsconfig/ for all options.
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

```text
# Files and directories that Git should ignore. Covers Node.js dependencies,
# TypeScript build output, environment files, and common editor artifacts.
# See https://git-scm.com/docs/gitignore for syntax reference.

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir -p nodejs-docker-example/src && cd nodejs-docker-example
cat > src/index.ts <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
// A minimal Express application.
// The root endpoint (GET /) returns a JSON greeting.
// See https://expressjs.com/ for the framework reference.

import express, { type Request, type Response } from 'express';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > package.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > tsconfig.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  // TypeScript compiler configuration for the Node.js application.
  // Compiles src/ to dist/ as CommonJS modules targeting ES2022.
  // See https://www.typescriptlang.org/tsconfig/ for all options.
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > .gitignore <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Files and directories that Git should ignore. Covers Node.js dependencies,
# TypeScript build output, environment files, and common editor artifacts.
# See https://git-scm.com/docs/gitignore for syntax reference.

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
New-Item -ItemType Directory -Force -Path nodejs-docker-example/src | Out-Null
Set-Location nodejs-docker-example
WriteFile 'src/index.ts' @'
// A minimal Express application.
// The root endpoint (GET /) returns a JSON greeting.
// See https://expressjs.com/ for the framework reference.

import express, { type Request, type Response } from 'express';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
'@
WriteFile 'package.json' @'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
'@
WriteFile 'tsconfig.json' @'
{
  // TypeScript compiler configuration for the Node.js application.
  // Compiles src/ to dist/ as CommonJS modules targeting ES2022.
  // See https://www.typescriptlang.org/tsconfig/ for all options.
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
'@
WriteFile '.gitignore' @'
# Files and directories that Git should ignore. Covers Node.js dependencies,
# TypeScript build output, environment files, and common editor artifacts.
# See https://git-scm.com/docs/gitignore for syntax reference.

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
'@
```

If you have Node.js installed and want to verify the app works before containerizing it, you can run it locally.

To run in development mode with hot-reload:

```console
$ npm install
$ npm run dev
```

To run the compiled production build (matching what the Dockerfile does):

```console
$ npm install
$ npm run build
$ npm start
```

Then open <http://localhost:3000> in your browser. You should see `{"message":"Hello World"}`.

If you don't have Node.js installed, skip ahead. The remaining steps run the application in a container, with no local Node.js required.

## [Create the Docker assets](#create-the-docker-assets)

Sign in to the DHI registry so Docker can pull the Node.js base images during the build. The available Node.js images are listed in the [catalog](https://hub.docker.com/hardened-images/catalog/dhi/node).

```console
$ docker login dhi.io
```

Add the following three files to your `nodejs-docker-example` directory. The `Dockerfile` describes how to build the image, `compose.yaml` defines how Docker runs the container, and `.dockerignore` keeps unwanted files out of the build context.

> Tip
>
> [Gordon](/ai/gordon/), Docker's AI assistant, can generate Docker assets for your project. Ask Gordon to create a Dockerfile, Compose file, and `.dockerignore` tailored to your application.

nodejs-docker-example

```typescript
// A minimal Express application.
// The root endpoint (GET /) returns a JSON greeting.
// See https://expressjs.com/ for the framework reference.

import express, { type Request, type Response } from 'express';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
```

```json
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
```

```json
{
  // TypeScript compiler configuration for the Node.js application.
  // Compiles src/ to dist/ as CommonJS modules targeting ES2022.
  // See https://www.typescriptlang.org/tsconfig/ for all options.
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

```dockerfile
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Builder stage: install all dependencies and compile TypeScript.
FROM dhi.io/node:24-alpine3.23-dev AS builder

WORKDIR /app

# Install dependencies as a separate step to take advantage of Docker's
# caching. Leverage a cache mount to /root/.npm to speed up subsequent
# builds. Leverage a bind mount to package.json to avoid having to copy
# it into this layer.
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# Copy the source code into the container and compile TypeScript.
COPY . .
RUN npm run build


# Deps stage: install production dependencies only.
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# Runner stage: minimal runtime image with compiled app and production deps.
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["node", "dist/index.js"]
```

```yaml
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 3000:3000
```

```text
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

node_modules/
dist/
.env
.git
.gitignore
.DS_Store
npm-debug.log*
coverage/
db/
```

```text
# Files and directories that Git should ignore. Covers Node.js dependencies,
# TypeScript build output, environment files, and common editor artifacts.
# See https://git-scm.com/docs/gitignore for syntax reference.

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir -p nodejs-docker-example/src && cd nodejs-docker-example
cat > src/index.ts <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
// A minimal Express application.
// The root endpoint (GET /) returns a JSON greeting.
// See https://expressjs.com/ for the framework reference.

import express, { type Request, type Response } from 'express';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > package.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > tsconfig.json <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
{
  // TypeScript compiler configuration for the Node.js application.
  // Compiles src/ to dist/ as CommonJS modules targeting ES2022.
  // See https://www.typescriptlang.org/tsconfig/ for all options.
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > Dockerfile <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Builder stage: install all dependencies and compile TypeScript.
FROM dhi.io/node:24-alpine3.23-dev AS builder

WORKDIR /app

# Install dependencies as a separate step to take advantage of Docker's
# caching. Leverage a cache mount to /root/.npm to speed up subsequent
# builds. Leverage a bind mount to package.json to avoid having to copy
# it into this layer.
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# Copy the source code into the container and compile TypeScript.
COPY . .
RUN npm run build


# Deps stage: install production dependencies only.
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# Runner stage: minimal runtime image with compiled app and production deps.
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["node", "dist/index.js"]
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > compose.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 3000:3000
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > .dockerignore <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

node_modules/
dist/
.env
.git
.gitignore
.DS_Store
npm-debug.log*
coverage/
db/
__DOCKER_DOCS_SCAFFOLD_EOF__
cat > .gitignore <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Files and directories that Git should ignore. Covers Node.js dependencies,
# TypeScript build output, environment files, and common editor artifacts.
# See https://git-scm.com/docs/gitignore for syntax reference.

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path nodejs-docker-example | Out-Null
New-Item -ItemType Directory -Force -Path nodejs-docker-example/src | Out-Null
Set-Location nodejs-docker-example
WriteFile 'src/index.ts' @'
// A minimal Express application.
// The root endpoint (GET /) returns a JSON greeting.
// See https://expressjs.com/ for the framework reference.

import express, { type Request, type Response } from 'express';

const app = express();
const port = parseInt(process.env.PORT ?? '3000', 10);

app.get('/', (_req: Request, res: Response) => {
  res.json({ message: 'Hello World' });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
'@
WriteFile 'package.json' @'
{
  "name": "nodejs-docker-example",
  "version": "1.0.0",
  "description": "A minimal Node.js TypeScript application.",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts"
  },
  "dependencies": {
    "express": "^4.21.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.21",
    "@types/node": "^22.0.0",
    "tsx": "^4.19.3",
    "typescript": "^5.8.3"
  }
}
'@
WriteFile 'tsconfig.json' @'
{
  // TypeScript compiler configuration for the Node.js application.
  // Compiles src/ to dist/ as CommonJS modules targeting ES2022.
  // See https://www.typescriptlang.org/tsconfig/ for all options.
  "compilerOptions": {
    "target": "ES2022",
    "module": "commonjs",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
'@
WriteFile 'Dockerfile' @'
# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# This Dockerfile uses Docker Hardened Images (DHI) for enhanced security.
# For more information, see https://docs.docker.com/dhi/

# Builder stage: install all dependencies and compile TypeScript.
FROM dhi.io/node:24-alpine3.23-dev AS builder

WORKDIR /app

# Install dependencies as a separate step to take advantage of Docker's
# caching. Leverage a cache mount to /root/.npm to speed up subsequent
# builds. Leverage a bind mount to package.json to avoid having to copy
# it into this layer.
RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci

# Copy the source code into the container and compile TypeScript.
COPY . .
RUN npm run build


# Deps stage: install production dependencies only.
FROM dhi.io/node:24-alpine3.23-dev AS deps

WORKDIR /app

RUN --mount=type=cache,target=/root/.npm \
    --mount=type=bind,source=package.json,target=package.json \
    npm install --omit=dev
# Once you create a package-lock.json by running npm install locally, switch to npm ci and bind both files:
# RUN --mount=type=cache,target=/root/.npm \
#     --mount=type=bind,source=package.json,target=package.json \
#     --mount=type=bind,source=package-lock.json,target=package-lock.json \
#     npm ci --omit=dev


# Runner stage: minimal runtime image with compiled app and production deps.
FROM dhi.io/node:24-alpine3.23 AS runner

ENV PATH=/app/node_modules/.bin:$PATH

WORKDIR /app

COPY --from=deps --chown=node:node /app/node_modules ./node_modules
COPY --from=builder --chown=node:node /app/dist ./dist

# Expose the port that the application listens on.
EXPOSE 3000

# Run the application.
CMD ["node", "dist/index.js"]
'@
WriteFile 'compose.yaml' @'
# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Docker Compose reference guide at
# https://docs.docker.com/go/compose-spec-reference/

# Here the instructions define your application as a service called "server".
# This service is built from the Dockerfile in the current directory.
# You can add other services your application may depend on here, such as a
# database or a cache. For examples, see the Awesome Compose repository:
# https://github.com/docker/awesome-compose
services:
  server:
    build:
      context: .
    ports:
      - 3000:3000
'@
WriteFile '.dockerignore' @'
# Include any files or directories that you don't want to be copied to your
# container here (e.g., local build artifacts, temporary files, etc.).
#
# For more help, visit the .dockerignore file reference guide at
# https://docs.docker.com/go/build-context-dockerignore/

node_modules/
dist/
.env
.git
.gitignore
.DS_Store
npm-debug.log*
coverage/
db/
'@
WriteFile '.gitignore' @'
# Files and directories that Git should ignore. Covers Node.js dependencies,
# TypeScript build output, environment files, and common editor artifacts.
# See https://git-scm.com/docs/gitignore for syntax reference.

node_modules/
dist/
.env
*.log
.DS_Store
coverage/
db/password.txt
'@
```

The `Dockerfile` uses three stages. The `builder` stage installs all dependencies and compiles TypeScript. The `deps` stage does a fresh install of production-only dependencies. The `runner` stage copies the compiled output and production node\_modules into a minimal runtime image that contains only Node.js.

To learn more about each file, see the following:

* [Dockerfile](https://docs.docker.com/reference/dockerfile/)
* [.dockerignore](https://docs.docker.com/reference/dockerfile/#dockerignore-file)
* [compose.yaml](https://docs.docker.com/reference/compose-file/)

## [Run the application](#run-the-application)

Inside the `nodejs-docker-example` directory, run the following command in a terminal.

```console
$ docker compose up --build
```

Open a browser and view the application at <http://localhost:3000>. You should see `{"message":"Hello World"}`.

In the terminal, press `ctrl`+`c` to stop the application.

### [Run the application in the background](#run-the-application-in-the-background)

You can run the application detached from the terminal by adding the `-d` option. Inside the `nodejs-docker-example` directory, run the following command in a terminal.

```console
$ docker compose up --build -d
```

Open a browser and view the application at <http://localhost:3000>.

In the terminal, run the following command to stop the application.

```console
$ docker compose down
```

For more information about Compose commands, see the [Compose CLI reference](/reference/cli/docker/compose/).

## [Summary](#summary)

In this section, you learned how to containerize and run a Node.js application using Docker.

[Use containers for Node.js development »](https://docs.docker.com/guides/nodejs/develop/)

----
