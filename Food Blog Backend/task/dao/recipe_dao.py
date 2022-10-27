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
class MeasureItem:
    id: int = 0
    name: str = ''


@dataclass
class IngredientItem:
    id: int = 0
    name: str = ''


@dataclass
class ServeItem:
    id: int = 0
    recipe_id: int = 0
    meal_id: int = 0


@dataclass
class QuantityItem:
    id: int = 0
    quantity: int = 0
    recipe_id: int = 0
    measure_id: int = 0
    ingredient_id: int = 0


RECIPES = 'recipes'
MEALS = 'meals'
MEASURES = 'measures'
INGREDIENTS = 'ingredients'
SERVE = 'serve'
QUANTITY = 'quantity'


class DatabaseAccess:
    def __init__(self, db_name: str):
        self._conn = connect(db_name)
        self.cursor = self._conn.cursor()

    def close_(self):
        self._conn.commit()
        self._conn.close()

    # to use this class with 'with'
    def __enter__(self):
        return self

    # to use this class with 'with'
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_()


class RecipeDao:
    def __init__(self, db_name: str):
        self._db_name = db_name

    def save_recipe(self, recipe_item: RecipeItem) -> int:
        with DatabaseAccess(self._db_name) as dba:
            item_id = dba.cursor.execute(
                f'''INSERT INTO {RECIPES} (recipe_name, recipe_description) 
                    VALUES (?, ?)''', (recipe_item.name, recipe_item.description)).lastrowid
            return int(item_id)

    def read_meal_items(self) -> List[MealItem]:
        with DatabaseAccess(self._db_name) as dba:
            rows = dba.cursor.execute(f'SELECT * FROM {MEALS}').fetchall()
            meals = [MealItem(record[0], record[1]) for record in rows]
            return meals

    def save_serve_items(self, items: List[ServeItem]):
        with DatabaseAccess(self._db_name) as dba:
            ins_sql = f'INSERT INTO {SERVE}(recipe_id, meal_id) VALUES (?, ?)'
            values = ((item.recipe_id, item.meal_id,) for item in items)
            dba.cursor.executemany(ins_sql, values)

    def get_measure_by_name(self, name) -> MeasureItem:
        with DatabaseAccess(self._db_name) as dba:
            if name == '':
                row = dba.cursor.execute(f'''SELECT * FROM {MEASURES}
                    WHERE measure_name='';''').fetchone()
                return MeasureItem(row[0], row[1])
            rows = dba.cursor.execute(f'''SELECT * FROM {MEASURES}
                WHERE measure_name LIKE ?;''', (name + '%',)).fetchall()
            return MeasureItem(rows[0][0], rows[0][1]) \
                if len(rows) == 1 \
                else None

    def get_ingredient_by_name(self, name) -> IngredientItem:
        with DatabaseAccess(self._db_name) as dba:
            rows = dba.cursor.execute(f'''SELECT * FROM {INGREDIENTS}
                WHERE ingredient_name LIKE ?;''', (name + '%',)).fetchall()
            return IngredientItem(rows[0][0], rows[0][1]) \
                if len(rows) == 1 \
                else None

    def save_quantity_item(self, q: QuantityItem):
        with DatabaseAccess(self._db_name) as dba:
            dba.cursor.execute(f'''INSERT INTO {QUANTITY} (quantity, recipe_id, measure_id, ingredient_id)
                VALUES (?, ?, ?, ?)''', (q.quantity, q.recipe_id, q.measure_id, q.ingredient_id))
