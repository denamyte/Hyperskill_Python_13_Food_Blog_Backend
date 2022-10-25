from sqlite3 import connect
from .recipe_item import RecipeItem


class RecipeDao:

    def __init__(self, db_name: str, recipe_table: str):
        self._db_name = db_name
        self._recipe_table = recipe_table

    def save_recipe(self, recipe_item: RecipeItem):
        conn = connect(self._db_name)
        cursor = conn.cursor()
        cursor.execute(f'''INSERT INTO {self._recipe_table} (recipe_name, recipe_description) 
                            VALUES (?, ?)''', (recipe_item.name, recipe_item.desc))
        conn.commit()
        cursor.close()
        conn.close()

