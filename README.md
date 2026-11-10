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
| 1 | Capital of Australia (one word) | _ s | _ | _ | _ |
| 2 | Rewrite sentence formally | _ s | _ | _ | _ |
| 3 | Explain RAG (~400 words) | _ s | _ | _ | _ |

## Which prompt is expensive, and why

Run 3. The input is short, so almost all of the cost and latency comes from **completion tokens**. Output tokens are priced higher than input tokens and are generated one by one, so latency scales with answer length. The cost is justified because a long answer was requested.

The real lesson: when a short-looking prompt shows high **prompt** tokens, the waste is hidden in the input (system prompt, retrieved context, chat history). The terminal can't show this; LangSmith makes it visible.
