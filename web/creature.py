from fastapi import APIRouter
from model.creature import Creature
import data.creature as service  # Изменили на импорт из data/creature

router = APIRouter(prefix="/creature", tags=["creature"])

@router.get("")
@router.get("/")
def get_all() -> list[Creature]:
    return service.get_all()

@router.get("/{name}")
def get_one(name: str) -> Creature | None:
    return service.get_one(name)

@router.post("/")
def create(creature: Creature) -> Creature:
    return service.create(creature)

@router.patch("/{name}")
def modify(name: str, creature: Creature) -> Creature | None:
    return service.modify(name, creature)

@router.put("/{name}")
def replace(name: str, creature: Creature) -> Creature | None:
    return service.modify(name, creature)

@router.delete("/{name}")
def delete(name: str) -> None:
    return service.delete(name)
