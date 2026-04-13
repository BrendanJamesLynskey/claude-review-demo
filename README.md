# Claude Code — GitHub PR Reviews with GitHub Actions

A step-by-step tutorial for setting up automated AI-powered pull request reviews using Claude Code and GitHub Actions.

## Overview

This tutorial walks through configuring Claude to automatically review pull requests in your GitHub repositories. When a PR is opened or updated, Claude analyses the diff and posts inline review comments identifying bugs, security issues, and code quality concerns.

## Prerequisites

- A GitHub account
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed (included with Claude Pro/Max subscriptions)
- The [GitHub CLI](https://cli.github.com/) (`gh`) installed and authenticated

## Setup Guide

### 1. Install the Claude GitHub App

1. Go to [github.com/apps/claude](https://github.com/apps/claude)
2. Click **Install**
3. Select your account or organisation
4. Choose which repositories to grant access to
5. Click **Install & Authorise**

### 2. Generate an OAuth Token

In a terminal, run:

```bash
claude setup-token
```

This opens a browser-based OAuth flow. Log in with your Claude account and it will output a long-lived token. Copy it.

> **Note:** This command requires an interactive terminal — it cannot be run inside Claude Code itself.

### 3. Add the Token as a GitHub Secret

```bash
gh secret set CLAUDE_CODE_OAUTH_TOKEN --repo <owner>/<repo>
```

Paste the token when prompted.

> **Security:** GitHub encrypts repository secrets at rest. They are never exposed in logs or to forks. Only workflows in your repository can access them at runtime. You can revoke the token at any time with `claude setup-token` (and generate a new one).

### 4. Add the Workflow File

Create `.github/workflows/claude.yml` in your repository:

```yaml
name: Claude PR Review

on:
  pull_request:
    types: [opened, synchronize]
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]

jobs:
  claude-review:
    if: |
      github.event_name == 'pull_request' ||
      (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
      (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude'))
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pull-requests: write
      issues: write
      id-token: write
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: anthropics/claude-code-action@v1
        with:
          claude_code_oauth_token: ${{ secrets.CLAUDE_CODE_OAUTH_TOKEN }}
```

Commit and push this to your default branch.

### 5. Open a Pull Request

Create a branch, make changes, push, and open a PR:

```bash
git checkout -b feature/my-change
# ... make changes ...
git add -A && git commit -m "Add my feature"
git push -u origin feature/my-change
gh pr create --title "My feature" --body "Description of changes"
```

Claude will automatically review the PR when it is opened.

## How It Works

| Trigger | What happens |
|---------|-------------|
| PR opened | Claude automatically reviews the diff |
| New commits pushed to PR | Claude re-reviews the changes |
| Comment `@claude review` | On-demand full review |
| Comment `@claude <question>` on a specific line | Claude answers about that specific code |

## Customising Reviews with CLAUDE.md

Add a `CLAUDE.md` file to your repository root to guide Claude's review focus:

```markdown
# Review Guidelines
- Flag all SQL injection vulnerabilities as critical
- Ensure all database connections use context managers
- Check for missing input validation on public functions
```

Claude reads this file and tailors its reviews accordingly.

## Example Files

- [utils.py](utils.py) — Utility functions for data processing
- [user_handler.py](user_handler.py) — Database operations (intentionally contains issues for Claude to find)
- [.github/workflows/claude.yml](.github/workflows/claude.yml) — The GitHub Actions workflow

## What Claude Finds

In [PR #2](https://github.com/BrendanJamesLynskey/claude-review-demo/pull/2), Claude identified:

- **SQL injection vulnerabilities** — string interpolation in queries instead of parameterised statements
- **Resource leaks** — database connections not closed or managed with context managers
- **Missing safety guards** — destructive operations without confirmation or authorisation checks

## Further Reading

- [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- [claude-code-action on GitHub](https://github.com/anthropics/claude-code-action)
- [Claude GitHub App](https://github.com/apps/claude)
