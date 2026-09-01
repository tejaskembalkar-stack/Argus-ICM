# Cost Limits

Treat cost as a first-class constraint.

- `fast`: single worker, no planner, one review pass.
- `standard`: one planner, one worker, one reviewer.
- `frontier`: one planner, two workers, one reviewer.

If a task needs more than these limits, split it into stages before increasing agent count.
