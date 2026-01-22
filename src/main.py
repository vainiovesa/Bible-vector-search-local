from search import search


def main():
    query = "The creation of the World."

    result = search(query, 10)
    for row in result:
        print("; ".join([str(item) for item in row]) + "\n")


if __name__ == "__main__":
    main()
