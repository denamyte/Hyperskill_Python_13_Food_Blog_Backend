from sqlite3 import connect, Connection, Cursor

DATA = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
NOT_NULL = {"meals": "NOT NULL",
            "ingredients": "NOT NULL",
            "measures": ""}


def ini_db(db_name: str):
    conn = connect(db_name)
    cursor = conn.cursor()
    if not table_created(conn, 'meals'):
        create_and_populate_helper_tables(cursor)
    if not table_created(conn, 'recipes'):
        create_recipe_table(cursor)
    conn.commit()
    cursor.close()
    conn.close()


def table_created(conn: Connection, table_name: str):
    c = conn.cursor()
    c.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return c.fetchone()[0] == 1


def create_and_populate_helper_tables(cursor: Cursor):
    for name in DATA.keys():
        cursor.execute('''CREATE TABLE {0}s(
                              {0}_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              {0}_name TEXT {1} UNIQUE
                       );'''.format(name[:-1], NOT_NULL[name]))
        ins_sql = 'INSERT INTO {0}s({0}_name) VALUES(?);'.format(name[:-1])
        values = [(value,) for value in DATA[name]]
        cursor.executemany(ins_sql, values)


def create_recipe_table(cursor: Cursor):
    cursor.execute('''CREATE TABLE recipes(
                          recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                          recipe_name TEXT NOT NULL,
                          recipe_description TEXT
                      )''')
