# app/main.py
from fastapi import FastAPI
from app.routes import items

app = FastAPI(title="Mi API con FastAPI")

app.include_router(items.router, prefix="/items", tags=["Items"])

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola desde FastAPI!"}
