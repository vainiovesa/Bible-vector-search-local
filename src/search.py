import numpy as np
import ollama
from db import fetch


def search(query:str, limit:int=5):
    input = "search_query: " + query
    embedding = ollama.embed(model='nomic-embed-text', input=input).embeddings[0]

    result = fetch(np.array(embedding), limit)
    return result
