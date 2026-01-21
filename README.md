# Bible vector search local

## Overview

### Rationale

Good Finnish software for searching for Bible verses is rare to come by.
As far as I know, vector searching for the Finnish translations does not exist.
This project makes it possible to store any given translation to a vector database and perform semantic searching.
This means that users can search verses based on meaning rather than exact wording.

### Implementation

This project uses PostgreSQL with the [pgvector](https://github.com/pgvector/pgvector-python)
extension to store embeddings made with Ollama's [nomic-embed-text](https://ollama.com/library/nomic-embed-text).

### Source

The Bible translations in json format used in this project came from [this project](https://github.com/thiagobodruk/bible?tab=readme-ov-file).
