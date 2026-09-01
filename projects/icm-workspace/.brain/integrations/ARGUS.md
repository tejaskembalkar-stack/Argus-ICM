# Argus Security Gate

Argus/ECC is the local security and reliability gate for this ICM workspace.

## Local checkout

```text
C:\Users\Spectrex\Documents\GitHub\Argus
```

The checkout is read from GitHub and used as a local tool source. Do not vendor the whole Argus repository into this project.

## Gate command

Run from this project root:

```bash
python .brain/scripts/argus_gate.py --json
```

The wrapper runs:

1. `npx --yes ecc-agentshield scan --path <root> --format json`
2. `node scripts/ci/scan-supply-chain-iocs.js --root <root> --json` from the Argus checkout
3. `node scripts/harness-audit.js --root <root> --format json` from the Argus checkout

## Pass/fail policy

The gate fails when:

- AgentShield reports any critical/high finding;
- Argus IOC scan reports any active IOC finding;
- any gate command exits non-zero;
- scanner output cannot be parsed as JSON.

Harness audit findings are advisory for maturity unless they identify runtime security failures.

## Before commits or swarm merges

Run:

```bash
python .brain/scripts/icm.py validate
python .brain/scripts/argus_gate.py --json
```

Do not merge or push agent-written code until both pass.

## Current verified state

- GitHub CLI authenticated: yes, account `tejaskembalkar-stack`.
- Argus checkout cloned: yes.
- Access to `tejaskembalkar-ship-it/Argus`: read-only for the authenticated account.
- ICM validation: passing.
