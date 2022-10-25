from dataclasses import dataclass
from sqlite3 import connect
from typing import List


@dataclass
class RecipeItem:
    id: int = 0
    name: str = ''
    description: str = ''


@dataclass
class MealItem:
    id: int = 0
    name: str = ''


@dataclass
class ServeItem:
    id: int = 0
    recipe_id: int = 0
    meal_id: int = 0


RECIPES = 'recipes'
MEALS = 'meals'
SERVE = 'serve'


class DatabaseAccess:
    def __init__(self, db_name: str):
        self._conn = connect(db_name)
        self.cursor = self._conn.cursor()

    def close(self):
        self._conn.commit()
        self._conn.close()


class RecipeDao:
    def __init__(self, db_name: str):
        self._db_name = db_name

    def save_recipe(self, recipe_item: RecipeItem) -> int:
        dba = DatabaseAccess(self._db_name)
        item_id = dba.cursor.execute(
            f'''INSERT INTO {RECIPES} (recipe_name, recipe_description) 
                VALUES (?, ?)''', (recipe_item.name, recipe_item.description)).lastrowid
        dba.close()
        return int(item_id)

    def read_meal_items(self) -> List[MealItem]:
        dba = DatabaseAccess(self._db_name)
        rows = dba.cursor.execute(f'''SELECT * FROM {MEALS}''').fetchall()
        meals = [MealItem(record[0], record[1]) for record in rows]
        dba.close()
        return meals

    def save_serve_items(self, items: List[ServeItem]):
        dba = DatabaseAccess(self._db_name)
        ins_sql = f'INSERT INTO {SERVE}(recipe_id, meal_id) VALUES (?, ?)'
        values = ((item.recipe_id, item.meal_id,) for item in items)
        dba.cursor.executemany(ins_sql, values)
        dba.close()
