# .github/README.md
# .github folder

Purpose: repository‑level configuration and automation.

Contents
- `branch-protection.json`: settings used to apply branch protection to `main` via the GitHub API.
- `ISSUE_TEMPLATE/`: GitHub Issues templates.
- `PULL_REQUEST_TEMPLATE.md`: PR template.

Notes
- Treat files here as infrastructure, not project content.
- If you change `branch-protection.json`, re‑apply with:
  ```bash
  gh api -X PUT \
    -H "Accept: application/vnd.github+json" \
    /repos/<owner>/<repo>/branches/main/protection \
    --input .github/branch-protection.json
  ```
- Branch is protected, so changes must flow through a PR.
