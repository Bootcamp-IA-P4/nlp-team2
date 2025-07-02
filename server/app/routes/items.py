from fastapi import APIRouter
from app.models.item import Item

router = APIRouter()

@router.post("/", response_model=Item)
def crear_item(item: Item):
    return item  # Aquí iría lógica para guardar en DB

@router.get("/{item_id}", response_model=Item)
def obtener_item(item_id: int):
    return Item(id=item_id, nombre="Ejemplo", descripcion="Un item de prueba", precio=12.5)