# Review Gate

Before any swarm output is accepted:

1. `python .brain/scripts/icm.py validate` must pass.
2. `python .brain/scripts/argus_gate.py --json` must pass.
3. The reviewer must compare at least one implementation artifact against the task brief.
4. Unverified outputs remain proposals, not accepted changes.
