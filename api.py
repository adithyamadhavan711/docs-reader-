from fastapi import FastAPI
from sqlite import search_doc

app = FastAPI()


@app.get("/search")
def search(word: str):

    results = search_doc(word)

    output = []

    for title, content in results:
        output.append({"title": title, "content": content})

    return output
