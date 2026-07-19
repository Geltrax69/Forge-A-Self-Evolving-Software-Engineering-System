url: https://docs.docker.com/guides/python/lint-format-typing/
----

# Linting, formatting, and type checking for Python

***

Table of contents

***

## [Prerequisites](#prerequisites)

Complete [Develop your app](https://docs.docker.com/guides/python/develop/). This topic requires a local Python installation because the tools and Git hooks introduced here run on your host. If you don't want to install Python locally, skip this topic. The same checks run in CI in the [next topic](https://docs.docker.com/guides/python/configure-github-actions/).

## [Overview](#overview)

Linting, formatting, and type checking are automated ways to catch bugs, enforce style, and spot type errors before code runs. Running them on every commit, in CI, and in your editor catches problems early when they're cheap to fix.

In this section, you'll configure three tools for your Python application. Ruff handles linting and formatting in a single fast pass. Pyright statically checks your code for type errors. Pre-commit hooks run both of these automatically before each Git commit so problems are caught locally before they're committed.

## [Linting and formatting with Ruff](#linting-and-formatting-with-ruff)

Ruff is an extremely fast Python linter and formatter written in Rust. It replaces multiple tools like flake8, isort, and black with a single unified tool.

Create a `pyproject.toml` file in your `python-docker-example` directory:

python-docker-example

```toml
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir python-docker-example && cd python-docker-example
cat > pyproject.toml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path python-docker-example | Out-Null
Set-Location python-docker-example
WriteFile 'pyproject.toml' @'
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]
'@
```

Install Ruff:

```console
$ pip install ruff
```

If you're using a virtual environment, make sure it is activated so the `ruff` command is available.

Run these commands to check and format your code:

```console
# Check for errors
$ ruff check .

# Automatically fix fixable errors
$ ruff check --fix .

# Format code
$ ruff format .
```

## [Type checking with Pyright](#type-checking-with-pyright)

Pyright is a fast static type checker for Python that works well with modern Python features.

Update `pyproject.toml` to add the Pyright configuration at the bottom.

python-docker-example

```toml
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir python-docker-example && cd python-docker-example
cat > pyproject.toml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path python-docker-example | Out-Null
Set-Location python-docker-example
WriteFile 'pyproject.toml' @'
# Configuration for code-quality tools.
# - [tool.ruff]: linting and formatting (https://docs.astral.sh/ruff/)
# - [tool.pyright]: static type checking (https://microsoft.github.io/pyright/)

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",  # pycodestyle errors
    "W",  # pycodestyle warnings
    "F",  # pyflakes
    "I",  # isort
    "B",  # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
    "ARG001", # unused arguments in functions
]
ignore = [
    "E501",  # line too long, handled by black
    "B008",  # do not perform function calls in argument defaults
    "W191",  # indentation contains tabs
    "B904",  # Allow raising exceptions without from e, for HTTPException
]

[tool.pyright]
typeCheckingMode = "strict"
pythonVersion = "3.12"
exclude = [".venv"]
'@
```

Install Pyright and run it:

```console
$ pip install pyright
$ pyright
```

## [Setting up pre-commit hooks](#setting-up-pre-commit-hooks)

Pre-commit hooks run checks automatically before each commit on your local machine. Create a `.pre-commit-config.yaml` file in your `python-docker-example` directory to set up Ruff hooks:

python-docker-example

```yaml
# Pre-commit hook configuration. Runs Ruff (lint + format) on every
# `git commit`. See https://pre-commit.com/

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.15
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Overwrites existing files with the same names. Run from the parent of your project directory.

```bash
mkdir python-docker-example && cd python-docker-example
cat > .pre-commit-config.yaml <<'__DOCKER_DOCS_SCAFFOLD_EOF__'
# Pre-commit hook configuration. Runs Ruff (lint + format) on every
# `git commit`. See https://pre-commit.com/

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.15
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
__DOCKER_DOCS_SCAFFOLD_EOF__
```

```powershell
# Write files as UTF-8 without BOM. Works on Windows PowerShell 5.1 and PowerShell 7+.
function WriteFile([string]$Path, [string]$Content) {
    $full = Join-Path -Path (Get-Location).ProviderPath -ChildPath $Path
    [System.IO.File]::WriteAllText($full, $Content, [System.Text.UTF8Encoding]::new($false))
}

New-Item -ItemType Directory -Force -Path python-docker-example | Out-Null
Set-Location python-docker-example
WriteFile '.pre-commit-config.yaml' @'
# Pre-commit hook configuration. Runs Ruff (lint + format) on every
# `git commit`. See https://pre-commit.com/

repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.15.15
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
'@
```

To install and use:

```console
$ pip install pre-commit
$ pre-commit install
$ git commit -m "Test commit"  # Automatically runs checks
```

## [Summary](#summary)

In this section, you learned how to:

* Configure and use Ruff for linting and formatting
* Set up Pyright for static type checking
* Automate checks with pre-commit hooks

These tools help maintain code quality and catch errors early in development.

Related information:

* [Ruff documentation](https://docs.astral.sh/ruff/)
* [Pyright documentation](https://microsoft.github.io/pyright/)
* [pre-commit framework](https://pre-commit.com/)

## [Next steps](#next-steps)

* [Configure GitHub Actions](https://docs.docker.com/guides/python/configure-github-actions/) to run these checks automatically
* Customize linting rules to match your team's style preferences
* Explore advanced type checking features

[Automate your builds with GitHub Actions »](https://docs.docker.com/guides/python/configure-github-actions/)

----
