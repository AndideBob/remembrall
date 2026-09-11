# llm-gateway

Thin service abstracting LLM providers behind one internal interface.

**Language:** Python

**Responsibilities**
- Exposes a single internal endpoint: `POST /generate`.
- Routes to a provider selected by `LLM_PROVIDER`:
  - Anthropic (default).
  - Ollama (fully local).
- Keeps "which LLM am I using" a config decision, not a code change.
