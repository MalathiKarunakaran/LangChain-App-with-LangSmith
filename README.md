# Trace a LangChain App with LangSmith

Week 2 · Day 3 assignment. A minimal LangChain app (`ChatOpenAI`, `gpt-4o-mini`) that sends 3 prompts to OpenAI. Tracing is switched on purely through environment variables; `traced_app.py` contains no LangSmith code.

## Run

```bash
python3 -m venv venv && source venv/bin/activate
pip install langchain langchain-openai

export OPENAI_API_KEY="your-openai-key"
export LANGSMITH_TRACING="true"
export LANGSMITH_API_KEY="your-langsmith-key"
export LANGSMITH_PROJECT="caie-week2"

python traced_app.py
```

## Verify tracing is on before checking the dashboard

```bash
python -c "from langsmith import utils; import os; print(utils.tracing_is_enabled(), os.getenv('LANGSMITH_PROJECT'))"
```
Expected: `True caie-week2`. Tracing fails silently, so this check comes first. A `403 Forbidden` at the end of a run means the LangSmith key or region endpoint is wrong.

## Results (LangSmith project: caie-week2)

| Run | Prompt | Latency | Prompt tokens | Completion tokens | Total |
|---|---|---|---|---|---|
| 1 | Capital of Australia (one word) | 2.25 s | 19 | 3 | 22 |
| 2 | Rewrite sentence formally | 1.13 s | 25 | 12 | 37 |
| 3 | Explain RAG (~400 words) | 8.82 s | 50 | 645 | 695 |

## Which prompt is expensive, and why

Run 3. The input is short, so almost all of the cost and latency comes from **completion tokens**. Output tokens are priced higher than input tokens and are generated one by one, so latency scales with answer length. The cost is justified because a long answer was requested.

The real lesson: when a short-looking prompt shows high **prompt** tokens, the waste is hidden in the input (system prompt, retrieved context, chat history). The terminal can't show this; LangSmith makes it visible.

## Observations

- **Run 3 is the expensive one:** 695 tokens, $0.0004, 8.82 s. 98% of the tokens (645) are output. The input was only 50 tokens, so the cost is driven by the long answer that was requested. Expensive, but for a good reason.
- **Latency follows output length:** 3 output tokens took ~2 s, 12 took ~1 s, 645 took ~9 s. Tokens are generated one at a time.
- **Run 1 is slower than run 2 despite a one-word answer.** The first call pays one-time connection and client warm-up costs. Latency is not only about tokens, and this is only visible in a trace.
- **Failures are traced too:** earlier runs with a bad API key appear in the project as `OpenAIAuthenticationError`, so LangSmith shows the cause of a failed run without reading the terminal.
