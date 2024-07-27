from model.creature import Creature


_creatures = [
    Creature(
        name="Claude Hande",
        country="FR",
        area="Paris",
        description="fake description",
        aka="fake aka",
    ),
    Creature(
        name="John Doe",
        country="US",
        area="New York",
        description="fake description",
        aka="fake aka",
    ),
    Creature(
        name="Gne Doe",
        country="US",
        area="New York",
        description="as description",
        aka="as fake aka",
    ),
    Creature(
        name="Bob Smith",
        country="US",
        area="New York",
        description="fake description",
        aka="fake aka",
    ),
]


def get_all():
    return _creatures


def get_one(name: str):
    for creature in _creatures:
        if creature.name == name:
            return creature

    return None


def create(creature: Creature):
    _creatures.append(creature)


def modify(creature: Creature) -> Creature:
    return creature


def replace(creature: Creature) -> Creature:
    return creature


def delete(name: str):
    return None