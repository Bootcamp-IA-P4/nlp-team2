from pydantic import BaseModel

class Item(BaseModel):
    id: int
    nombre: str
    descripcion: str = None
    precio: float
