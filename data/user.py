from data.init import conn, curs, get_db, IntegrityError
from model.user import User
from errors import Missing, Duplicate


curs.execute("""CREATE TABLE IF NOT EXISTS user(
name TEXT PRIMARY KEY,
hash TEXT)""")

curs.execute("""CREATE TABLE IF NOT EXISTS xuser(
name TEXT PRIMARY KEY,
hash TEXT)""")

def row_to_model(row: tuple) -> User:
    name, hash = row
    return User(name=name, hash=hash)

def model_to_dict(user: User) -> dict:
    return user.dict()

def get_one(name: str) -> User:
    qry = "SELECT * FROM user WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    row = curs.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"User {name} not found.")

def get_all() -> list[User]:
    gry = "SELECT * FROM user"
    curs.execute(gry)
    return [row_to_model(row) for row in curs.fetchall()]

def create(user: User, table: str = "user"):
    gry = f"""insert into {table} (name, hash) values (:name, :hash)"""
    params = model_to_dict(user)
    try:
        curs.execute(gry, params)
    except IntegrityError:
        raise Duplicate(f"{table}: user {user.name} already exists.")

def modify(name: str, user: User) -> User:
    qry = """UPDATE user SET 
             name=:name, hash=:hash
             WHERE name=:name"""
    params = {
        "name": user.name,
        "hash": user.hash,
        "name0": name}
    curs.execute(qry, params)
    if curs.rowcount == 1:
        return get_one(user.name)
    else:
        raise Missing(msg=f"User {name} not found.")

def delete(name: str) -> None:
    user = get_one(name)
    qry = "DELETE FROM user WHERE name=:name"
    params = {"name": name}
    curs.execute(qry, params)
    if curs.rowcount != 1:
        raise Missing(msg=f"User {name} not found.")
    create(user, table="xuser")