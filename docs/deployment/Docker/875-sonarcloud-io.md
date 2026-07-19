         url: "https://sonarcloud.io",
       },
     },
   });
   ```

   ```python
   # python
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
   ```

4. Verify your API tokens are valid and have proper scopes.

## [GitHub tools work but SonarQube doesn't](#github-tools-work-but-sonarqube-doesnt)

Issue: GitHub MCP tools load but SonarQube tools don't appear.

Solution: SonarQube MCP server requires GitHub to be configured simultaneously. Always include both servers in your sandbox configuration, even if you're only testing one.

```typescript
// Include both servers even if only using one
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
