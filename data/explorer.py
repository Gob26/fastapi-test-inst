
from data.init import curs, conn
from model.explorer import Explorer

curs.execute("""CREATE TABLE IF NOT EXISTS explorer(
name TEXT PRIMARY KEY,
country TEXT,
description TEXT)""")

def row_to_model(row: tuple) -> Explorer:
    return Explorer(name=row[0], country=row[1], description=row[2])

def model_to_dict(explorer: Explorer) -> dict:
    return explorer.dict() if explorer else None

def get_one(name: str) -> Explorer:
    qry = "SELECT * FROM explorer WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    return row_to_model(curs.fetchone())

def get_all() -> list[Explorer]:
    qry = "SELECT * FROM explorer"
    curs.execute(qry)
    return [row_to_model(row) for row in curs.fetchall()]

def create(explorer: Explorer) -> Explorer:
    qry = '''INSERT INTO explorer (name, country, description)
    VALUES (:name, :country, :description)'''
    params = model_to_dict(explorer)
    _ = curs.execute(qry, params)
    conn.commit()
    return get_one(explorer.name)

def modify(name: str, explorer: Explorer) -> Explorer:
    qry = """UPDATE explorer
    SET country=:country,
    name=:name,
    description=:description
    WHERE name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = name
    _ = curs.execute(qry, params)
    explorer2 = get_one(explorer.name)
    return explorer2

def delete(name: str) -> bool:
    qry = "DELETE FROM explorer WHERE name=:name"
    params = {"name": name}
    res = curs.execute(qry, params)
    return bool(res)
