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

  const repoPath = `${process.env.GITHUB_OWNER}/${process.env.GITHUB_REPO}`;
  const branchName = `quality-fix-${Date.now()}`;

  console.log("\nFixing a code quality issue...\n");

  const prompt = `Using GitHub and SonarQube MCP tools:

    1. Analyze code quality in repository "${repoPath}" with SonarQube
    2. Find ONE simple issue that can be confidently fixed (like an unused variable or code smell)
    3. Create a new branch called "${branchName}"
    4. Read the file containing the issue using GitHub tools
    5. Fix the issue in the code
    6. Commit the fix to the new branch with a clear commit message

    Important: Only fix issues you're 100% confident about. Explain what you're fixing and why.`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log(`\nCheck your repository for branch: ${branchName}`);

  await sbx.kill();
}

fixCodeIssue().catch(console.error);
```

Run the script:

```bash
npx tsx 05-fix-code-issue.ts
```

Create `05_fix_code_issue.py`:

```python
import os
import asyncio
import time
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def fix_code_issue():
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

    repo_path = f"{os.getenv('GITHUB_OWNER')}/{os.getenv('GITHUB_REPO')}"
    branch_name = f"quality-fix-{int(time.time() * 1000)}"

    print("\nFixing a code quality issue...\n")

    prompt = f"""Using GitHub and SonarQube MCP tools:

    1. Analyze code quality in repository "{repo_path}" with SonarQube
    2. Find ONE simple issue that can be confidently fixed (like an unused variable or code smell)
    3. Create a new branch called "{branch_name}"
    4. Read the file containing the issue using GitHub tools
    5. Fix the issue in the code
    6. Commit the fix to the new branch with a clear commit message

    Important: Only fix issues you're 100% confident about. Explain what you're fixing and why."""

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print(f"\n Check your repository for branch: {branch_name}")

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(fix_code_issue())
```

Run the script:

```bash
python 05_fix_code_issue.py
```

> Note
>
> This script may take a few minutes to run.

Claude will analyze your repository and fix a code quality issue:

```console
Creating sandbox...

Fixing a code quality issue...

## Task Completed Successfully!

I've successfully analyzed the repository and fixed a code quality issue. Here's what I did:

### 1. Analysis
Found 1 SonarQube issues in the `<your-repo>` repository:
- **Unused variable** (MINOR severity, line 2)
- Useless assignment (MAJOR severity, line 2)
- For-of loop suggestion (MINOR severity, lines 5-7)

### 2. Issue Fixed
**Location:** test.js:2
**Issue:** Unused variable declaration
**SonarQube Rule:** javascript:S1481
**What was wrong:** The line `const unusedVariable = "this is not used";` declared a variable that was never used anywhere in the function.

### 3. Why This Fix is Safe
- The variable was only declared and assigned, never referenced
- Removing it has zero impact on functionality
- It eliminates dead code and improves code quality
- This is a textbook example of a code smell that should be removed

### 4. Changes Made
- Created branch: `quality-fix-xxxxx`
- Removed the unused variable declaration
- Committed with a clear message explaining the fix and referencing the SonarQube rule

**Commit SHA:** `xxxxxxxxxxxxxxxxxxxxxxxxx`
**Branch:** https://github.com/<github-org>/<your-repo>/tree/quality-fix-xxxxx

The fix is ready for review and can be merged to improve the code quality of the repository!
```

You can now use GitHub and SonarQube MCP tools in the same workflow to read files, make code changes, and commit them.

## [Step 6: Create quality-gated pull requests](#step-6-create-quality-gated-pull-requests)

Finally, let's build the complete workflow: analyze quality, fix issues, and create a PR only if improvements are made.

Create `06-quality-gated-pr.ts`:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function qualityGatedPR() {
  console.log("Creating sandbox for quality-gated PR workflow...\n");

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
