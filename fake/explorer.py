from model.explorer import Explorer

_explorer = [
    Explorer(
    name="Claude Hande",
    country="FR",
    description="Scarce during full moon",),
    Explorer(
    name="Norbert Kowalski",
    country="DE",
    description="Mythical in full moon",)
]

def get_all() -> list[Explorer]:
    return _explorer

def get_one(name: str) -> Explorer|None:
    for explorer in _explorer:
        if explorer.name == name:
            return explorer
    return None

def create(name: str, country: str, description: str) -> Explorer:
    explorer = Explorer(name=name, country=country, description=description)
    _explorer.append(explorer)
    return explorer

def modify(name: str, description: str) -> Explorer|None:
    for explorer in _explorer:
        if explorer.name == name:
            explorer.description = description
            return explorer
    return None

def replace(name: str, explorer: Explorer) -> Explorer|None:
    for i in range(len(_explorer)):
        if _explorer[i].name == name:
            _explorer[i] = explorer
            return explorer
    return None

def delete(name: str) -> Explorer|None:
    for explorer in _explorer:
        if explorer.name == name:
            _explorer.remove(explorer)
            return explorer
    return None
