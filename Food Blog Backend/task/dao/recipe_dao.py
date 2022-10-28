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
                f'''INSERT INTO recipes (recipe_name, recipe_description) 
                    VALUES (?, ?)''', (recipe_item.name, recipe_item.description)).lastrowid
            return int(item_id)

    def get_meal_items(self) -> List[MealItem]:
        with DatabaseAccess(self._db_name) as dba:
            rows = dba.cursor.execute(f'SELECT * FROM meals').fetchall()
            return [MealItem(*row) for row in rows]

    def save_serve_items(self, items: List[ServeItem]):
        with DatabaseAccess(self._db_name) as dba:
            ins_sql = f'INSERT INTO serve(recipe_id, meal_id) VALUES (?, ?)'
            values = ((item.recipe_id, item.meal_id,) for item in items)
            dba.cursor.executemany(ins_sql, values)

    def get_measure_by_name(self, name) -> MeasureItem:
        with DatabaseAccess(self._db_name) as dba:
            if name == '':
                row = dba.cursor.execute(f'''SELECT * FROM measures
                    WHERE measure_name='';''').fetchone()
                return MeasureItem(row[0], row[1])
            rows = dba.cursor.execute(f'''SELECT * FROM measures
                WHERE measure_name LIKE ?;''', (name + '%',)).fetchall()
            return MeasureItem(*rows[0]) \
                if len(rows) == 1 \
                else None

    def get_ingredient_by_name(self, name) -> IngredientItem:
        with DatabaseAccess(self._db_name) as dba:
            rows = dba.cursor.execute(f'''SELECT * FROM ingredients
                WHERE ingredient_name LIKE ?;''', (name + '%',)).fetchall()
            return IngredientItem(*rows[0]) \
                if len(rows) == 1 \
                else None

    def save_quantity_item(self, q: QuantityItem):
        with DatabaseAccess(self._db_name) as dba:
            dba.cursor.execute(f'''INSERT INTO quantity (quantity, recipe_id, measure_id, ingredient_id)
                VALUES (?, ?, ?, ?)''', (q.quantity, q.recipe_id, q.measure_id, q.ingredient_id))

    @staticmethod
    def in_placeholder(num: int) -> str:
        return f"IN ({','.join('?' * num)})"

    def get_recipes_by_ingredients_and_meals_names(self, ingr_names: List[str], meal_names: List[str]) -> List[RecipeItem]:
        with DatabaseAccess(self._db_name) as dba:
            params = (*ingr_names, len(ingr_names), *meal_names)
            result = dba.cursor.execute(f'''
SELECT *
FROM recipes r
WHERE r.recipe_id IN (SELECT q.recipe_id
                      from quantity q
                      WHERE q.ingredient_id IN (SELECT i.ingredient_id
                                                FROM ingredients i
                                                WHERE i.ingredient_name {self.in_placeholder(len(ingr_names))})
                      GROUP BY q.recipe_id
                      HAVING COUNT(q.ingredient_id) = ?)
  AND r.recipe_id IN (SELECT DISTINCT s.recipe_id
                      from serve s
                      WHERE s.meal_id IN (SELECT m.meal_id
                                          FROM meals m
                                          WHERE m.meal_name {self.in_placeholder(len(meal_names))}));'''
                                        , params)
            return [RecipeItem(*row) for row in result.fetchall()]
