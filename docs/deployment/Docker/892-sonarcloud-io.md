        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  console.log("\nAnalyzing code quality with SonarQube...\n");

  const prompt = `Using the SonarQube MCP tools:
    1. List all projects in my organization
    2. For the first project, show:
    - Quality gate status (pass/fail)
    - Number of bugs
    - Number of code smells
    - Number of security vulnerabilities
    3. List the top 5 most critical issues found`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  await sbx.kill();
}

testSonarQube().catch(console.error);
```

Run the script:

```bash
npx tsx 04-test-sonarqube.ts
```

Create `04_test_sonarqube.py`:

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def test_sonarqube():
    print("Creating sandbox...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
            "SONARQUBE_TOKEN": os.getenv("SONARQUBE_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
            },
            "sonarqube": {
                "org": os.getenv("SONARQUBE_ORG"),
                "token": os.getenv("SONARQUBE_TOKEN"),
                "url": "https://sonarcloud.io",
            },
        },
    )

    mcp_url = sbx.beta_get_mcp_url()
    mcp_token = await sbx.beta_get_mcp_token()

    await asyncio.sleep(1)

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print("\nAnalyzing code quality with SonarQube...\n")

    prompt = """Using the SonarQube MCP tools:
    1. List all projects in my organization
    2. For the first project, show:
    - Quality gate status (pass/fail)
    - Number of bugs
    - Number of code smells
    - Number of security vulnerabilities
    3. List the top 5 most critical issues found"""

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(test_sonarqube())
```

Run the script:

```bash
python 04_test_sonarqube.py
```

> Note
>
> This script may take a few minutes to run.

You should see Claude output SonarQube analysis results:

```console
Creating sandbox...

Analyzing code quality with SonarQube...

## SonarQube Analysis Results

### 1. Projects in Your Organization

Found **1 project**:
- **Project Name**: project-1
- **Project Key**: project-testing

### 2. Project Analysis

...

### 3. Top 5 Most Critical Issues

Found 1 total issues (all are code smells with no critical/blocker severity):

1. **MAJOR Severity** - test.js:2
   - **Rule**: javascript:S1854
   - **Message**: Remove this useless assignment to variable "unusedVariable"
   - **Status**: OPEN

**Summary**: The project is in good health with no bugs or vulnerabilities detected.
```

You can now use SonarQube MCP tools to analyze code quality through natural language. You can retrieve quality metrics, identify issues, and understand what code needs fixing.

## [Step 5: Create a branch and make code changes](#step-5-create-a-branch-and-make-code-changes)

Now, let's teach Claude to fix code based on quality issues discovered by SonarQube.

Create `05-fix-code-issue.ts`:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function fixCodeIssue() {
  console.log("Creating sandbox...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
      SONARQUBE_TOKEN: process.env.SONARQUBE_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
      },
      sonarqube: {
        org: process.env.SONARQUBE_ORG!,
        token: process.env.SONARQUBE_TOKEN!,
