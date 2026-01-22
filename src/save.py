import json
import numpy as np
import ollama
import psycopg
from db import get_connection, reinitialize, save_data, search


BIBLE_PATH = "en_kjv_bible.json"


def load():
    with open(BIBLE_PATH, "r") as file:
        Bible = json.loads(file.read())
    return Bible


def save(data:list, reinit:bool=False):
    if reinit:
        reinitialize()

    inputs = ["search_document: " + row[3] for row in data]
    embeddings = ollama.embed(model="nomic-embed-text", input=inputs).embeddings

    save_data(data, embeddings)
