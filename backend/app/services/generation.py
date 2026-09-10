import ollama

from app.core.config import settings
from app.services.retrieval import find_relevant_chunks

def build_prompt(question, results):
    context = ""
    for i in range(len(results["documents"][0])):

        source = results["metadatas"][0][i]["source"]
        page = results["metadatas"][0][i]["page"]
        text = results["documents"][0][i]

        context += f"\nSource: {source}, Page: {page}\n"
        context += f"{text}\n"

    prompt = f"""
You are an AI and Computer Science Learning Assistant.
Answer the user's question using ONLY the provided context.
If the answer cannot be found in the context, say:
"I couldn't find the answer in the provided documents."
Answer the question clearly and concisely.
Do not invent information or citations.
Context:
{context}

Question:
{question}

Answer:
"""
    return prompt


def get_sources(results):
    sources = []
    for i in range(len(results["documents"][0])):
        source = results["metadatas"][0][i]["source"]
        page = results["metadatas"][0][i]["page"]
        citation = f"{source}, page {page}"
        if citation not in sources:
            sources.append(citation)
    return sources


def generate_answer(question, n_results=3):
    results = find_relevant_chunks(question, n_results)
    prompt = build_prompt(question, results)
    response = ollama.chat(
        model=settings.llm_model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    answer = response["message"]["content"]
    sources = get_sources(results)
    return answer, sources