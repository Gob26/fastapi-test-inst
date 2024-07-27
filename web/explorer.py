from fastapi import APIRouter
from model.explorer import Explorer
import data.explorer as service  # Изменили на импорт из data/explorer

router = APIRouter(prefix="/explorer", tags=["explorer"])

@router.get("")
@router.get("/")
def get_all() -> list[Explorer]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Explorer | None:
    return service.get_one(name)

@router.post("/")
def create(explorer: Explorer) -> Explorer:
    return service.create(explorer)

@router.patch("/{name}")
def modify(name: str, explorer: Explorer) -> Explorer | None:
    return service.modify(name, explorer)

@router.put("/{name}")
def replace(name: str, explorer: Explorer) -> Explorer | None:
    return service.modify(name, explorer)

@router.delete("/{name}")
def delete(name: str) -> bool:
    return service.delete(name)
