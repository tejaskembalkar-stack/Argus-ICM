# OpenRouter Integration

OpenRouter is the preferred model gateway for swarm roles when credentials are available to the runtime.

## Role

OpenRouter provides:

- provider-agnostic model access;
- model and provider fallbacks;
- cost and latency routing;
- a single OpenAI-compatible API surface.

Local ICM still owns planning, context packs, git isolation, validation, memory, and winner selection.

## Runtime check

```bash
python .brain/scripts/icm.py status
```

If `OPENROUTER_API_KEY` is not visible in the terminal environment, Hermes app-level configuration may still exist, but local scripts cannot directly call the gateway yet.
