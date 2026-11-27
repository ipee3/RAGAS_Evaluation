# Oulu University – AI Engineering Assignment 2

## Project Description

This project focuses on evaluating LiteratureExplorer, a Retrieval-Augmented Generation (RAG) system developed by XYZ Inc. as part of the AI Engineering course at the University of Oulu.

The main objective is to assess the quality and reliability of the RAG system before the company continues develop its user interface.

The evaluation consists of two main parts:

1. **RAG System Evaluation:** Testing the system through its API.
2. **RAG Output Evaluation:** Evaluating the quality of generated answers using the Ragas framework and an LLM-as-a-Judge approach.

The project uses Python scripts to automate question generation, collect RAG responses and evaluate them using selected Ragas metrics.

## Results and Documentation

**The evaluation results, findings, and final project report are available in the project's documentation.**

**SharePoint: [View Project Documentation](https://unioulu-my.sharepoint.com/:f:/g/personal/itauriai20_student_oulu_fi/IgAd2hTtVi6GQ7TnRDAzw4pKAXfN7OLhliQpLAHuMrxY7do?e=rXP3fp) (Notice: link expires 31.5.2027 **

# Instructions on How to Run the Code

**1. Install the required packages**

Run the following command:

`pip install -r requirements.txt`

**2. Configure the `.env` file**

Make sure your `.env` file includes the following variables:

- `ENDPOINT_LITERATURE_EXPLORER`
- `API_KEY_LITERATURE_EXPLORER`
- `URL_LEHMUS_AI`
- `API_KEY_LEHMUS_AI`
- `Model_LEHMUS_AI_SMALL`
- `Smaller_Model_ID`
- `Model_LEHMUS_AI_LARGE`
- `Larger_Model_ID`
- `Model_ID_EMBEDDINGS`

**3. Prepare the test data**

Make sure the `data` directory contains the `test_question.json` file.

**4. Connect to the University of Oulu network**

Make sure you are connected to the University of Oulu network or have the fortiCLient VPN enabled before running the application.

**5. Run the application**

The application consists of two main parts:

- **First: `run_rag.py`**

  This script reads questions from `test_question.json`, sends them to the RAG system, and saves the generated responses to `/data/rag_responses.json`.

- **Second: `run_evaluation.py`**

  This script reads the generated responses from `rag_responses.json`, uses an LLM-as-a-judge approach, and performs an evaluation using the Ragas framework.

  The evaluation results are saved to `/results/assessment_results.json` or `/results/assessment_largerLL_results.json` depending which of the model using on evaluation (small or large). There you can find the questions and their corresponding evaluation metrics.

## Included Evaluation Results

This repository includes the results from one completed evaluation run.

The RAG system has already been executed using the test questions, and the generated responses are available in `data/rag_responses.json`. The original test questions can be found in `data/test_questions.json`.

The generated RAG responses have also been evaluated using two different LLM models with an LLM-as-a-Judge approach.

- **Larger LLM:** GPT-OSS 120B. The evaluation results are available in `results/assessment_largerLLM_results.json`.
- **Smaller LLM:** Gemma 4 26B MoE. The evaluation results are available in `results/assessment_results.json`.

Both models evaluated the same set of generated RAG responses, making it possible to compare their assessments and evaluation results.

The JSON files are included in the repository to provide examples of the generated responses and the corresponding evaluation results. They represent one completed run of the evaluation process.
