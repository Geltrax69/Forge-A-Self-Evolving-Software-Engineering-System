        url: "https://sonarcloud.io",
      },
    },
  });

  const mcpUrl = sbx.betaGetMcpUrl();
  const mcpToken = await sbx.betaGetMcpToken();

  // Wait for MCP initialization
  await new Promise((resolve) => setTimeout(resolve, 1000));

  await sbx.commands.run(
    `claude mcp add --transport http e2b-mcp-gateway ${mcpUrl} --header "Authorization: Bearer ${mcpToken}"`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  console.log("\nDiscovering available MCP tools...\n");

  const prompt =
    "List all MCP tools you have access to. For each tool, show its exact name and a brief description.";

  await sbx.commands.run(
    `echo '${prompt}' | claude -p --dangerously-skip-permissions`,
    { timeoutMs: 0, onStdout: console.log, onStderr: console.log },
  );

  await sbx.kill();
}

listTools().catch(console.error);
```

Run the script:

```bash
npx tsx 02-list-tools.ts
```

Create `02_list_tools.py`:

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def list_tools():
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

    # Wait for MCP initialization
    await asyncio.sleep(1)

    await sbx.commands.run(
        f'claude mcp add --transport http e2b-mcp-gateway {mcp_url} --header "Authorization: Bearer {mcp_token}"',
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    print("\nDiscovering available MCP tools...\n")

    prompt = "List all MCP tools you have access to. For each tool, show its exact name and a brief description."

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(list_tools())
```

Run the script:

```bash
python 02_list_tools.py
```

In the console, you should see a list of MCP tools:

```console
Creating sandbox...

Sandbox created
Connecting to MCP gateway...

Discovering available MCP tools...

I have access to the following MCP tools:

**GitHub Tools:**
1. mcp__create_repository - Create a new GitHub repository
2. mcp__list_issues - List issues in a repository
3. mcp__create_issue - Create a new issue
4. mcp__get_file_contents - Get file contents from a repository
5. mcp__create_or_update_file - Create or update files in a repository
6. mcp__create_pull_request - Create a pull request
7. mcp__create_branch - Create a new branch
8. mcp__push_files - Push multiple files in a single commit
... (30+ more GitHub tools)

**SonarQube Tools:**
1. mcp__get_projects - List projects in organization
2. mcp__get_quality_gate_status - Get quality gate status for a project
3. mcp__list_project_issues - List quality issues in a project
4. mcp__search_issues - Search for specific quality issues
... (SonarQube analysis tools)
```

## [Step 3: Test GitHub MCP tools](#step-3-test-github-mcp-tools)

Let's try testing GitHub using MCP tools. Start simple by listing repository issues.

Create `03-test-github.ts`:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function testGitHub() {
  console.log("Creating sandbox...\n");

  const sbx = await Sandbox.betaCreate({
    envs: {
      ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY!,
      GITHUB_TOKEN: process.env.GITHUB_TOKEN!,
    },
    mcp: {
      githubOfficial: {
        githubPersonalAccessToken: process.env.GITHUB_TOKEN!,
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

  console.log(`\nListing issues in ${repoPath}...\n`);

  const prompt = `Using the GitHub MCP tools, list all open issues in the repository "${repoPath}". Show the issue number, title, and author for each.`;

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

testGitHub().catch(console.error);
```

Run the script:

```bash
npx tsx 03-test-github.ts
```

Create `03_test_github.py`:

```python
import os
import asyncio
from dotenv import load_dotenv
from e2b import AsyncSandbox

load_dotenv()

async def test_github():
    print("Creating sandbox...\n")

    sbx = await AsyncSandbox.beta_create(
        envs={
            "ANTHROPIC_API_KEY": os.getenv("ANTHROPIC_API_KEY"),
            "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN"),
        },
        mcp={
            "githubOfficial": {
                "githubPersonalAccessToken": os.getenv("GITHUB_TOKEN"),
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

    print(f"\nListing issues in {repo_path}...\n")

    prompt = f'Using the GitHub MCP tools, list all open issues in the repository "{repo_path}". Show the issue number, title, and author for each.'

    await sbx.commands.run(
        f"echo '{prompt}' | claude -p --dangerously-skip-permissions",
        timeout=0,
        on_stdout=print,
        on_stderr=print,
    )

    await sbx.kill()

if __name__ == "__main__":
    asyncio.run(test_github())
```

Run the script:

```bash
python 03_test_github.py
```

You should see Claude use the GitHub MCP tools to list your repository's issues:

```console
Creating sandbox...
Connecting to MCP gateway...

Listing issues in <your-repo>...

Here are the first 10 open issues in the <your-repo> repository:

1. **Issue #23577**: Update README (author: user1)
2. **Issue #23575**: release-notes for Compose v2.40.1 version (author: user2)
3. **Issue #23570**: engine-cli: fix `docker volume prune` output (author: user3)
4. **Issue #23568**: Engdocs update (author: user4)
5. **Issue #23565**: add new section (author: user5)
... (continues with more issues)
```

You can now send prompts to Claude and interact with GitHub through natural language. Claude decides what tool to call based on your prompt.

## [Step 4: Test SonarQube MCP tools](#step-4-test-sonarqube-mcp-tools)

Let's analyze code quality using SonarQube MCP tools.

Create `04-test-sonarqube.ts`:

```typescript
import "dotenv/config";
import { Sandbox } from "e2b";

async function testSonarQube() {
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
