"""

This module evaluates the quality of LiteratureExplorer RAG responses
using the Ragas framework and a single-turn evaluation approach.

The evaluation uses an LLM-as-a-Judge approach, where a smaller or
larger language model evaluates the generated answers using selected
Ragas metrics.

"""

import asyncio
import json

#ragas metrics
from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    FactualCorrectness,
    ContextPrecision,
    ContextRecall
)
from pathlib import Path
from ragas.dataset_schema import SingleTurnSample
from judge import create_judge_smaller, create_judge_larger, create_embeddings

get_responses_path = Path("../data/rag_responses.json")
save_scores_path = Path("../results/assessment_results.json")
save_path = Path("../results/assessment_largerLLM_results.json")

def load_responses(path: Path):
    """Reads responses from a JSON file and returns them as a list of dicts.
    """
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def parse_response(raw):
    """Extracts the generated answer text from the raw RAG API response."""
    return raw["choices"][0]["message"]["content"]

def save_score_json(path: Path, scores: list[dict] ) -> None:
    """Writes all scores to a JSON file (replaces the previous file)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as file:
        json.dump(scores, file, ensure_ascii=False, indent=2)

def parse_contexts(raw):
    """ Parse contexts from responses, save it and return """
    parsed_contexts = []

    for context in raw["contexts"]:
        parsed_contexts.append(context["text"])

    return parsed_contexts

def create_ragas_sample():
    """ Loads RAG responses and converts them into objects. """
    data = load_responses(get_responses_path)

    samples = []

    for q in data:
        raw = q["raw"]

        sample = SingleTurnSample(
            user_input=q["question"],
            response=parse_response(raw),
            retrieved_contexts=parse_contexts(raw),
            reference=q["reference"]
        )
        #samples has answers from RAG system, contexts and reference answers
        samples.append(sample)

    return samples



async def run_evaluation():
    """

    Evaluates RAG responses using a smaller LLM as a judge.

    Runs the selected Ragas metrics for each sample and saves
    the evaluation scores to a JSON file.

    """
    evaluator = create_judge_smaller()
    evaluation_data = create_ragas_sample()
    embedder = create_embeddings()

    # Create metric / evaluator and devided which llm we using for evaluating
    faithfulness = Faithfulness(llm=evaluator) #Measures how factually consistent a response is with the retrieved context.
    relevancy = AnswerRelevancy(llm=evaluator, embeddings=embedder ) #Evaluates answer relevancy by generating multiple questions from the response and comparing them to the original question using cosine similarity.
    factualCorrectness = FactualCorrectness(llm=evaluator) #Evaluates the factual correctness of responses by comparing claims made in the response against a reference text.
    precision = ContextPrecision(llm=evaluator) # Evaluates whether retrieved contexts are useful for answering a question by comparing each context against a reference answer. 
    recall = ContextRecall(llm=evaluator) # Evaluates context recall by classifying if statements in a reference answer can be attributed to the retrieved context.

    scores_arr = []
    number = 1
    for sample in evaluation_data:
        print()
        print(f"Question {number}: {sample.user_input}")
        print(f"LiteratureExplorer: {sample.response}")
        #sample = evaluation_data[number]

        #ascore starts faithfulness evaluation asyncronized way
        faithfulness_result = await faithfulness.ascore(
            user_input= sample.user_input,
            response= sample.response,
            retrieved_contexts= sample.retrieved_contexts  
        )
        print(f"Faithfulness score: {faithfulness_result.value}")

        relevancy_result = await relevancy.ascore(
            user_input= sample.user_input ,
            response= sample.response,
        )
        print(f"Answer relevancy: {relevancy_result.value}")

        factualCorrectness_result = await factualCorrectness.ascore(
            response= sample.response,
            reference= sample.reference
        )
        print(f"Factual correctness: {factualCorrectness_result.value}")

        precision_result = await precision.ascore(
            user_input=sample.user_input,
            reference= sample.reference,
            retrieved_contexts=sample.retrieved_contexts
        )
        print(f"Context precision: {precision_result.value}")

        recall_result = await recall.ascore(
            user_input=sample.user_input,
            retrieved_contexts=sample.retrieved_contexts,
            reference=sample.reference,
        )
        print(f"Context recall: {recall_result.value}")

        scores_arr.append({
            "question_number": number,
            "question": sample.user_input,
            "RAG's_answer": sample.response,
            "faithfulness": faithfulness_result.value,
            "answer_relevancy": relevancy_result.value,
            "factual_correctness": factualCorrectness_result.value,
            "context_precision": precision_result.value,
            "context_recall": recall_result.value,
        })

        # save results to json
        save_score_json(save_scores_path, scores_arr)

        number += 1

# async def run_evaluation_larger():
#     """scores the metrics using larger llm as a judge"""
#     evaluator = create_judge_larger()
#     evaluation_data = create_ragas_sample()
#     embedder = create_embeddings()

#     # Create metric / evaluator and devided which llm we using for evaluating
#     faithfulness = Faithfulness(llm=evaluator) #Measures how factually consistent a response is with the retrieved context.
#     relevancy = AnswerRelevancy(llm=evaluator, embeddings=embedder ) #Evaluates answer relevancy by generating multiple questions from the response and comparing them to the original question using cosine similarity.
#     factualCorrectness = FactualCorrectness(llm=evaluator) #Evaluates the factual correctness of responses by comparing claims made in the response against a reference text.
#     precision = ContextPrecision(llm=evaluator) # Evaluates whether retrieved contexts are useful for answering a question by comparing each context against a reference answer. 
#     recall = ContextRecall(llm=evaluator) # Evaluates context recall by classifying if statements in a reference answer can be attributed to the retrieved context.

#     scores_arr = []
#     number = 1
#     for sample in evaluation_data:
#         print()
#         print(f"Question {number}: {sample.user_input}")
#         print(f"LiteratureExplorer: {sample.response}")
#         #sample = evaluation_data[number]

#         #ascore starts faithfulness evaluation asyncronized way
#         faithfulness_result = await faithfulness.ascore(
#             user_input= sample.user_input,
#             response= sample.response,
#             retrieved_contexts= sample.retrieved_contexts  
#         )
#         print(f"Faithfulness score: {faithfulness_result.value}")

#         relevancy_result = await relevancy.ascore(
#             user_input= sample.user_input ,
#             response= sample.response,
#         )
#         print(f"Answer relevancy: {relevancy_result.value}")

#         factualCorrectness_result = await factualCorrectness.ascore(
#             response= sample.response,
#             reference= sample.reference
#         )
#         print(f"Factual correctness: {factualCorrectness_result.value}")

#         precision_result = await precision.ascore(
#             user_input=sample.user_input,
#             reference= sample.reference,
#             retrieved_contexts=sample.retrieved_contexts
#         )
#         print(f"Context precision: {precision_result.value}")

#         recall_result = await recall.ascore(
#             user_input=sample.user_input,
#             retrieved_contexts=sample.retrieved_contexts,
#             reference=sample.reference,
#         )
#         print(f"Context recall: {recall_result.value}")

#         scores_arr.append({
#             "question_number": number,
#             "question": sample.user_input,
#             "RAG's_answer": sample.response,
#             "faithfulness": faithfulness_result.value,
#             "answer_relevancy": relevancy_result.value,
#             "factual_correctness": factualCorrectness_result.value,
#             "context_precision": precision_result.value,
#             "context_recall": recall_result.value,
#         })

#         # save results to json
#         save_score_json(save_path, scores_arr)

#         number += 1

if __name__ == "__main__":
    asyncio.run(run_evaluation())
    #asyncio.run(run_evaluation_larger())
