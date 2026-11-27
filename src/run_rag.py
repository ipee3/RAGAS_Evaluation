#Tämä tiedosto:
# 1. Hakee kysymykset jsonista
# 2. rag.py olevan funktion avulla kysyy silmukassa kaikki kysymykset läpi
# 3. Tallentaa kysymykset erilliseen tiedostoon
"""
This module collects responses from the LiteratureExplorer RAG application.

It loads test questions from a JSON file, sends them to the RAG API,
measures the response time, and saves the results for later evaluation
with Ragas.

This way, the same responses can be evaluated multiple times without
having to query the RAG application again.
"""
import json
from rag import retrieval_and_generation_rag
from pathlib import Path #Build, read, edit file paths
import time

# paths
get_question_path = Path("../data/test_questions.json")
save_responses_path = Path("../data/rag_responses.json")

def load_questions(path: str):
    """Reads questions from a JSON file and returns them as a list of dicts.

    every dict has the keys "id", "Question" and "Reference".
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)["Questions"]

def save_responses(path: Path, results: list[str]) -> None:
    """Writes all results to a JSON file (replaces the previous file)."""
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=2)

def run_rag():
    """Asks every question (defined on test_questions file) from the RAG application and saves the responses."""

    question_list = load_questions(get_question_path)

    results = []
    for q in question_list:
        id = q["id"]
        question_text = q["Question"]
        reference_answer = q["Reference"]

        print()
        print(f"Asking question: {id}..")
        print()

        start_time = time.perf_counter()
        rag_response = retrieval_and_generation_rag(q["Question"])
        end_time = time.perf_counter()
        response_time = end_time - start_time

        results.append({
            "id": id,
            "question": question_text,
            "reference": reference_answer,
            "response_time": round(response_time, 3),
            "raw": rag_response, #whole answer from server
        })

        save_responses(save_responses_path, results)
        
if __name__ == "__main__":
    run_rag()