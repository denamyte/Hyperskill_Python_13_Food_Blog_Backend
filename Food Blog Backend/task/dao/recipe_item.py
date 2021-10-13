class RecipeItem:
    def __init__(self, name: str, description: str, id_: int = 0):
        self._id = id_
        self._name = name
        self._description = description

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def desc(self):
        return self._description

    def __str__(self):
        return f'RecipeItem({self.name}, {self.desc})'
