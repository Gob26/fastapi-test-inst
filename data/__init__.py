import os
from pathlib import Path
from sqlite3 import Connection, connect, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    global conn
    global curs
    if conn:
        if not reset:
            return
        conn = None

    if not name:
        name = os.getenv("CRYPTID_SQLITE_DB")
        if not name:
            top_dir = Path(__file__).resolve().parents[1]
            db_dir = top_dir / "db"
            db_name = "cryptid.db"
            db_path = db_dir / db_name
            name = str(db_path)

        print(f"Database path: {name}")

    try:
        # Ensure the directory exists
        db_dir = Path(name).parent
        if not db_dir.exists():
            db_dir.mkdir(parents=True, exist_ok=True)

        conn = connect(name, check_same_thread=False)
        curs = conn.cursor()
        print("Database connection established")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")


get_db()
