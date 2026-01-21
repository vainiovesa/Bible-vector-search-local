import json
import numpy as np
import ollama
from pgvector.psycopg import register_vector
import psycopg


BIBLE_PATH = "en_kjv_bible.json"
BIBLE_DB_NAME = "bible_db"


def load():
    with open(BIBLE_PATH, "r") as file:
        Bible = json.loads(file.read())
    return Bible


def get_connection():
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname=BIBLE_DB_NAME,
        user="postgres",
        password="postgres",
        autocommit=True,
    )
    conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
    register_vector(conn)
    return conn


def save(conn:psycopg.Connection, data:list):
    conn.execute("DROP TABLE IF EXISTS Bible")
    sql = """CREATE TABLE Bible (
        book        TEXT,
        chapter     INTEGER,
        verse       INTEGER,
        content     TEXT,
        embedding   VECTOR(768),
        PRIMARY KEY (book, chapter, verse)
        )"""
    conn.execute(sql)

    inputs = ["search_document: " + row[3] for row in data]
    embeddings = ollama.embed(model="nomic-embed-text", input=inputs).embeddings

    cur = conn.cursor()
    with cur.copy("COPY Bible (book, chapter, verse, content, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
        copy.set_types(["text", "integer", "integer", "text", "vector"])

        book_name = data[0][0]
        print(book_name)

        for row, embedding in zip(data, embeddings):

            if row[0] != book_name:
                print(book_name)

            copy.write_row([*row, embedding])


def view(conn:psycopg.Connection):
    result = conn.execute("SELECT * FROM Bible").fetchall()
    return result
