import sqlite3
from model.creature import Creature
from data.init import conn, curs


curs.execute(
    """
    CREATE TABLE IF NOT EXISTS creature (
        name TEXT PRIMARY KEY, 
        description TEXT, 
        country TEXT, 
        area TEXT, 
        aka TEXT
    )
    """
)

# Преобразование строки базы данных в объект Creature
# Преобразование строки базы данных в объект Creature
def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(name=name, description=description, country=country, area=area, aka=aka)

# Преобразование объекта Creature в словарь
def model_to_dict(creature: Creature) -> dict:
    return creature.dict() if creature else None

# Получение одного объекта Creature по имени
def get_one(name: str) -> Creature:
    qry = "SELECT * FROM creature WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    return row_to_model(row) if row else None

# Получение всех объектов Creature
def get_all() -> list[Creature]:
    qry = "SELECT * FROM creature"
    curs.execute(qry)
    rows = curs.fetchall()
    return [row_to_model(row) for row in rows]

# Создание нового объекта Creature
def create(creature: Creature) -> Creature:
    qry = """INSERT INTO creature (name, description, country, area, aka) 
             VALUES (:name, :description, :country, :area, :aka)"""
    params = model_to_dict(creature)
    curs.execute(qry, params)
    conn.commit()
    return get_one(creature.name)

# Изменение объекта Creature
def modify(name: str, creature: Creature) -> Creature:
    qry = """UPDATE creature SET 
             description=:description, country=:country, area=:area, aka=:aka 
             WHERE name=:name"""
    params = model_to_dict(creature)
    params["name"] = name
    curs.execute(qry, params)
    conn.commit()
    return get_one(name)

# Замена объекта Creature
def replace(name: str, creature: Creature) -> Creature:
    delete(name)
    return create(creature)

# Удаление объекта Creature
def delete(name: str) -> Creature:
    qry = "DELETE FROM creature WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    conn.commit()
    return None


