from sqlite3 import Cursor
from dao.recipe_dao import DatabaseAccess

DATA = {"meals": ("breakfast", "brunch", "lunch", "supper"),
        "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
        "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}
NOT_NULL = {"meals": "NOT NULL",
            "ingredients": "NOT NULL",
            "measures": ""}


def ini_db(db_name: str):
    with DatabaseAccess(db_name) as dba:
        dba.cursor.execute('PRAGMA foreign_keys = ON;')
        if not table_created(dba.cursor, 'meals'):
            create_and_populate_helper_tables(dba.cursor)
            create_recipe_table(dba.cursor)
            create_serve_table(dba.cursor)
            create_quantity_table(dba.cursor)


def table_created(cursor: Cursor, table_name: str):
    cursor.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    return cursor.fetchone()[0] == 1


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
                    );''')


def create_serve_table(cursor: Cursor):
    cursor.execute('''CREATE TABLE serve(
                        serve_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        recipe_id INTEGER NOT NULL,
                        meal_id INTEGER NOT NULL,
                        FOREIGN KEY (recipe_id)
                        REFERENCES recipes(recipe_id),
                        FOREIGN KEY (meal_id)
                        REFERENCES meals(meal_id)
    );''')


def create_quantity_table(cursor: Cursor):
    cursor.execute('''CREATE TABLE quantity(
                        quantity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        quantity INTEGER NOT NULL,
                        recipe_id INTEGER NOT NULL,
                        measure_id INTEGER NOT NULL,
                        ingredient_id INTEGER NOT NULL,
                        FOREIGN KEY (measure_id)
                        REFERENCES measures(measure_id),
                        FOREIGN KEY (ingredient_id)
                        REFERENCES ingredients(ingredient_id),
                        FOREIGN KEY (recipe_id)
                        REFERENCES recipes(recipe_id)
    )''')
