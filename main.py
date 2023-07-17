from typing import Union

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from models import *
import uvicorn

app = FastAPI()


@app.get("/")
def index():
    return {"Hello": "World"}

register_tortoise(
    app,
    db_url="sqlite://database.sqlite3",
    modules={"models" : ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host="0.0.0.0")