# GitHub CI v2 and repository automation

## Included files

- `.github/workflows/ci.yml` — split quality, PostgreSQL test, and build jobs.
- `.github/workflows/codeql.yml` — scheduled and change-triggered CodeQL analysis for TypeScript/JavaScript.
- `.github/dependabot.yml` — weekly dependency and GitHub Actions update PRs.

## CI v2 design

The current all-in-one verification job is split into three jobs:

1. **Quality** — formatting, lint, TypeScript.
2. **Tests / PostgreSQL** — PostgreSQL 17 service, migrations, tests.
3. **Build** — runs after quality and tests pass; uploads build artifacts for seven days.

All jobs use read-only repository permissions. CI has concurrency cancellation, explicit timeouts, and a manual `workflow_dispatch` trigger.

The workflows preserve the repository's pinned toolchain:

- Node.js 26.13.0
- pnpm 11.9.0
- PostgreSQL 17

No deployment, publishing, release, or automated merge is configured.

## Apply

Copy these files into the repository, preserving their paths:

```text
.github/
  dependabot.yml
  workflows/
    ci.yml
    codeql.yml
```

Run from the repository root:

```powershell
pnpm format
pnpm format:check
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

Review the changes and commit them on a feature branch. Open a pull request into `main` and inspect the Actions results.

## GitHub Actions settings

Open repository **Settings → Actions → General**.

- Allow the GitHub and verified creator actions used by these workflows.
- If using an allow-list, permit `actions/checkout`, `pnpm/action-setup`, `actions/setup-node`, `actions/upload-artifact`, and `github/codeql-action`.
- Keep the default workflow permission at **Read repository contents permission**.
- Do not grant general write permissions.

CodeQL's `security-events: write` permission is scoped to its workflow and is needed to publish analysis results.

## Code scanning

After the first successful CodeQL run:

1. Open **Security → Code scanning**.
2. Confirm that CodeQL analysis appears.
3. Review findings and remediate genuine issues.
4. Check the repository's Security settings for any additional code-scanning setup prompts.

Feature availability can depend on repository visibility and GitHub plan. Verify the actual Security tab rather than assuming every security feature is enabled.

## Secret scanning

In repository **Settings → Security** (or **Advanced Security**, depending on the UI):

1. Inspect secret scanning availability.
2. Enable push protection if GitHub offers it.
3. Keep credentials out of source files and workflow YAML.
4. Add Actions secrets only if a future deployment or external integration actually requires them.

The current CI uses deliberately public local/CI PostgreSQL credentials and no external service secrets.

## Dependabot

Dependabot will create weekly dependency and GitHub Actions update PRs. Review and test updates rather than automatically merging them.

## Required status checks

Do not require status checks until GitHub has observed a successful PR workflow run. Then edit **Settings → Rules → Protect main** and require these CI job checks:

- `Quality / lint / typecheck / format`
- `Tests / PostgreSQL`
- `Build / production artifacts`

Select the exact check names shown by GitHub if its display differs. Keep CodeQL informational initially rather than making it a required check for every PR.

## Current limitations

- This is CI, not deployment.
- The web workspace does not yet have browser end-to-end tests.
- Existing test coverage is small and does not yet exercise multiplayer behavior.
- Build artifact upload is for inspection/retrieval, not a release.
- No workflow creates commits, pushes branches, merges PRs, or deploys the application.
