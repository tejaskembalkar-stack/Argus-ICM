# GitHub Integration

GitHub access is enabled through `gh` CLI.

## Readiness

```bash
gh --version
gh auth status
gh api user --jq '{login:.login,name:.name,email:.email}'
git status --short --branch
git remote -v
```

## Verified state

- `gh` installed: yes, version 2.98.0.
- Authenticated account: `tejaskembalkar-stack`.
- Token scopes reported by `gh`: `gist`, `read:org`, `repo`, `workflow`.
- Git protocol: HTTPS.
- Access to `tejaskembalkar-ship-it/Argus`: `READ` only.
- Local Argus checkout: `C:\Users\Spectrex\Documents\GitHub\Argus`.

## Boundary

Creating repositories, pushing branches, opening pull requests, merging, editing issues, or changing repository settings are external writes. Confirm the exact target first, perform the action, then read back the exact resource URL/ID.

Never place tokens in commands, files, prompts, or logs. Prefer the native credential store used by `gh`.
