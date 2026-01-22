import json
import ollama
from db import reinitialize, save_data


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


def embed_all_verses():
    Bible = load()

    for book in Bible:
        data = []

        book_name = book["name"]
        for chapter_num, chapter in enumerate(book["chapters"]):
            for verse_num, verse in enumerate(chapter):
                data.append((book_name, chapter_num, verse_num, verse))
        print(f"Started saving {book_name}")

        try:
            save(data)
            print(f"Saved {book_name}")
        except:
            print(f"Saving {book_name} failed")
