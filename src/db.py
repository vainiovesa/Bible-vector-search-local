from pgvector.psycopg import register_vector
import psycopg


BIBLE_DB_NAME = "bible_db"


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


def reinitialize():
    conn = get_connection()

    sql = "DROP TABLE IF EXISTS Bible"
    conn.execute(sql)

    sql = """CREATE TABLE Bible (
        book        TEXT,
        chapter     INTEGER,
        verse       INTEGER,
        content     TEXT,
        embedding   VECTOR(768),
        PRIMARY KEY (book, chapter, verse)
        )"""
    conn.execute(sql)


def save_data(data:list, embeddings:list):
    conn = get_connection()
    cur = conn.cursor()
    with cur.copy("COPY Bible (book, chapter, verse, content, embedding) FROM STDIN WITH (FORMAT BINARY)") as copy:
        copy.set_types(["text", "integer", "integer", "text", "vector"])

        book_name = data[0][0]
        print(book_name)

        for row, embedding in zip(data, embeddings):

            if row[0] != book_name:
                print(book_name)

            copy.write_row([*row, embedding])


def view_all():
    conn = get_connection()
    result = conn.execute("SELECT * FROM Bible").fetchall()
    return result


def fetch(embedding, limit):
    conn = get_connection()

    sql = "SELECT book, chapter + 1, verse + 1, content FROM Bible ORDER BY embedding <=> %s LIMIT %s"
    params = [embedding, limit]

    result = conn.execute(sql, params).fetchall()
    return result
