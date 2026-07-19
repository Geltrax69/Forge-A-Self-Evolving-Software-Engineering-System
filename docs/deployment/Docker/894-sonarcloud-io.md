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
  const branchName = `quality-improvements-${Date.now()}`;

  console.log("\nRunning quality-gated PR workflow...\n");

  const prompt = `You are a code quality engineer. Using GitHub and SonarQube MCP tools:

    STEP 1: ANALYSIS
    - Get current code quality status from SonarQube for "${repoPath}"
    - Record the current number of bugs, code smells, and vulnerabilities
    - Identify 1-3 issues that you can confidently fix

    STEP 2: FIX ISSUES
    - Create branch "${branchName}"
    - For each issue you're fixing:
        * Read the file with the issue
        * Make the fix
        * Commit with a descriptive message
    - Only fix issues where you're 100% confident the fix is correct

    STEP 3: VERIFICATION
        - After your fixes, check if quality metrics would improve
        - Calculate: Would this reduce bugs/smells/vulnerabilities?

    STEP 4: QUALITY GATE
        - Only proceed if your changes improve quality
        - If quality would not improve, explain why and stop

    STEP 5: CREATE PR (only if quality gate passes)
        - Create a pull request from "${branchName}" to main
        - Title: "Quality improvements: [describe what you fixed]"
        - Description should include:
            * What issues you fixed
            * Before/after quality metrics
            * Why these fixes improve code quality
        - Add a comment with detailed SonarQube analysis

    Be thorough and explain your decisions at each step.`;

  await sbx.commands.run(
    `echo '${prompt.replace(/'/g, "'\\''")}' | claude -p --dangerously-skip-permissions`,
    {
      timeoutMs: 0,
      onStdout: console.log,
      onStderr: console.log,
    },
  );

  console.log(`\n Workflow complete! Check ${repoPath} for new pull request.`);

  await sbx.kill();
}

qualityGatedPR().catch(console.error);
```

Run the script:

```bash
npx tsx 06-quality-gated-pr.ts
```

Create `06_quality_gated_pr.py`:

```python
import os
import asyncio
import time
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def quality_gated_pr():
    print("Creating sandbox for quality-gated PR workflow...\n")

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
    branch_name = f"quality-improvements-{int(time.time() * 1000)}"

    print("\nRunning quality-gated PR workflow...\n")

    prompt = f"""You are a code quality engineer. Using GitHub and SonarQube MCP tools:

    STEP 1: ANALYSIS
    - Get current code quality status from SonarQube for "{repo_path}"
    - Record the current number of bugs, code smells, and vulnerabilities
    - Identify 1-3 issues that you can confidently fix

    STEP 2: FIX ISSUES
    - Create branch "{branch_name}"
    - For each issue you are fixing:
        Read the file with the issue
        Make the fix
        Commit with a descriptive message
    - Only fix issues where you are 100 percent confident the fix is correct

    STEP 3: VERIFICATION
        - After your fixes, check if quality metrics would improve
        - Calculate: Would this reduce bugs/smells/vulnerabilities?

    STEP 4: QUALITY GATE
        - Only proceed if your changes improve quality
        - If quality would not improve, explain why and stop

    STEP 5: CREATE PR (only if quality gate passes)
        - Create a pull request from "{branch_name}" to main
        - Title: "Quality improvements: [describe what you fixed]"
        - Description should include:
            What issues you fixed
            Before/after quality metrics
            Why these fixes improve code quality
        - Add a comment with detailed SonarQube analysis

    Be thorough and explain your decisions at each step."""

    await sbx.commands.run(
        f"echo '{prompt.replace(chr(39), chr(39) + chr(92) + chr(39) + chr(39))}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print(f"\n Workflow complete! Check {repo_path} for new pull request.")

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(quality_gated_pr())
```

Run the script:

```bash
python 06_quality_gated_pr.py
```

> Note
>
> This script may take a few minutes to run.

Claude will run the entire workflow, creating a quality improvement and opening a PR in GitHub:

```console
Creating sandbox for quality-gated PR workflow...

Running quality-gated PR workflow...

## Complete - Code Quality Improvement Successfully Executed

### Summary of Work Completed

**Pull Request Created:** https://github.com/<github-org>/<your-repo>/pull/1

---

### STEP 1: ANALYSIS

**Current State:**
- **Bugs:** 0
- **Vulnerabilities:** 0
- **Code Smells:** 1
- **Lines of Code:** 12
- **All Ratings:** A (Reliability, Security, Maintainability)

**Issues Identified (all in test.js):**
1. xxxxxxxxx - Unused variable declaration (MINOR)

---

### STEP 2: FIX ISSUES

**Branch Created:** `quality-improvements-xxxxxxxx`

**Changes Made:**
1. **Removed unused variable** (line 2) - Eliminated dead code that served no purpose
2. **Modernized loop pattern** (lines 5-7) - Converted `for (let i = 0; i < items.length; i++)` to `for (const item of items)`

**Commit:** xxxxxxxxxx

---

### STEP 3: VERIFICATION

**Expected Impact:**
- Code Smells: 1 → 0 (100% reduction)
- Bugs: 0 → 0 (maintained)
- Vulnerabilities: 0 → 0 (maintained)
- All quality ratings maintained at A

---

### STEP 4: QUALITY GATE PASSED

**Decision Criteria Met:**
- ✅ Reduces code smells by 100%
- ✅ No new bugs or vulnerabilities introduced
- ✅ Code is more readable and maintainable
- ✅ Follows modern JavaScript best practices
- ✅ All fixes are low-risk refactorings with no behavioral changes

---

### STEP 5: CREATE PR

**Pull Request Details:**
- **Number:** #1
- **Title:** Quality improvements: Remove unused variable and modernize for loop
- **Branch:** quality-improvements-xxxxxxxx → main
- **URL:** https://github.com/<github-org)/<your-repo>/pull/1

**PR Includes:**
- Comprehensive description with before/after metrics
- Detailed SonarQube analysis comment with issue breakdown
- Code comparison showing improvements
- Quality metrics table

The pull request is now ready for review and merge!
```

You've now built a complete, multi-step workflow with conditional logic. Claude analyzes quality with SonarQube, makes fixes using GitHub tools, verifies improvements, and only creates a PR if quality actually improves.

## [Step 7: Add error handling](#step-7-add-error-handling)

Production workflows need error handling. Let's make the workflow more robust.

Create `07-robust-workflow.ts`:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function robustWorkflow() {
  let sbx: Sandbox | undefined;

  try {
    console.log("Creating sandbox...\n");

    sbx = await Sandbox.betaCreate({
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
