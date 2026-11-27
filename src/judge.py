"""
This module handles the initialization of LLM judges and embedding models
used for RAG evaluation.

It provides:
- A smaller LLM judge for faster evaluation.
- A larger LLM judge for comparing evaluation results.
- An embedding model used by Ragas metrics.

Model IDs, API URLs, and API keys are loaded from environment variables
in the .env file. A connection to the University of Oulu network or VPN
is required to access Lehmus AI.
"""
import os

from dotenv import load_dotenv
from ragas.llms import llm_factory
from openai import AsyncOpenAI
from ragas.embeddings.base import embedding_factory


load_dotenv() # Load environment variables from .env file

# Create a judge using smaller and faster model
def create_judge_smaller():
    """" Creating llm as a judge, ensure that you're connected into university's network or use VPN"""
    #get model id, url and key from .env
    model_id = os.getenv("Smaller_Model_ID")
    base_url = os.getenv("URL_LEHMUS_AI") 
    api_key = os.getenv("API_KEY_LEHMUS_AI")

    if not model_id or not base_url or not api_key:
        raise ValueError("Something is missing from .env file")

    # init "Standard" openai client but traffic is routed through lehmus ai
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )

    judge = llm_factory(
        model=model_id,
        client=client
    )
    return judge

def create_judge_larger():
    """" Creating llm as a judge, ensure that you're connected into university's network or use VPN"""
    #get model id, url and key from .env
    model_id = os.getenv("Larger_Model_ID")
    base_url = os.getenv("URL_LEHMUS_AI") 
    api_key = os.getenv("API_KEY_LEHMUS_AI")

    if not model_id or not base_url or not api_key:
        raise ValueError("Something is missing from .env file")

    # init "Standard" openai client but traffic is routed through lehmus ai
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )

    judge = llm_factory(
        model=model_id,
        client=client
    )
    return judge

# Create embeddings
def create_embeddings():

    #get model id, url and key from .env
    embedding_id= os.getenv("Model_ID_EMBEDDINGS")
    base_url = os.getenv("URL_LEHMUS_AI") 
    api_key = os.getenv("API_KEY_LEHMUS_AI")

    if not embedding_id or not base_url or not api_key:
        raise ValueError("Something is missing from .env file")

    # init "Standard" openai client
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url
    )

    #Instance for transformating text into vectors.
    embedder = embedding_factory(
        provider="openai",
        model=embedding_id,
        client=client,
        interface="modern"
    )

    # example: embedder = embedding_factory("openai", model="text-embedding-3-small", client=openai_client)

    return embedder