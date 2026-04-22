import sqlite3

def crear_db():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        precio REAL NOT NULL CHECK(precio >= 0),
        stock INTEGER NOT NULL CHECK(stock >= 0)
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_db()