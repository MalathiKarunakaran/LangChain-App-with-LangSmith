from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompts = [
    # 1. Short factual: tiny input, tiny output -> cheapest
    "What is the capital of Australia? Answer in one word.",
    # 2. Short transformation: small input, small output
    "Rewrite this sentence in formal English: 'gonna push the fix to prod after lunch'.",
    # 3. Long generation: small input, large output -> the expensive one
    "Explain how Retrieval-Augmented Generation (RAG) works, covering chunking, "
    "embeddings, vector search, re-ranking and prompt assembly, with a short "
    "Python-style pseudocode example. Aim for about 400 words.",
]

for i, p in enumerate(prompts, start=1):
    print(f"\n=== Prompt {i} ===\n{p}\n--- Answer ---")
    print(llm.invoke(p).content)
