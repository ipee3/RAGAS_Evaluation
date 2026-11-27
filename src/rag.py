"""
This module handles communication with the LiteratureExplorer RAG API.

The collected RAG responses are saved and reused later
for evaluation with Ragas, without having to query the RAG
application again.

"""
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

def retrieval_and_generation_rag(question: str) -> dict | None:
    """Asks one question from RAG-endpoint. Return answer or None if error"""

    rag_endpoint = os.getenv("ENDPOINT_LITERATURE_EXPLORER")
    rag_key = os.getenv("API_KEY_LITERATURE_EXPLORER")

    print("Asking questions from RAG application...")

    #Post question to endpoint
    try:
        response = requests.post(
            f"{rag_endpoint}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {rag_key}",
                "Content-Type": "application/json"
            },
            #Question here
            #json={"query": question},
            json={"messages": [{"role": "user", "content": question}]},
            timeout=120
        )
        #Raises an http error if one occurs
        response.raise_for_status()

        #Returns response as a dictionary
        return response.json()

        #BASH command below for doing this^^
        # curl -s -X POST rag_endpoint + /v1/chat/completions \
        # -H "Authorization: Bearer rag_key" \
        # -H "Content-Type: application/json" \
        # -d '{"messages":[{"role":"user","content":"What is WOLF?"}
    
    except requests.exceptions.Timeout:
        print(f"Timeout with question: {question}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP-error: {http_err} - {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"connection error: {err}")
        
    # if something fails nothing returns
    return