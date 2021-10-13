from current_state_data import CurrentStateDataFacade


def return_0(fn):
    def wrapper(*args):
        fn(*args)
        return 0
    return wrapper


class FoodBlogMenus:
    def __init__(self, data_facade: CurrentStateDataFacade):
        self._data_facade = data_facade
        pass

    @return_0
    def welcome_msg(self):
        print('Pass the empty recipe name to exit.')

    def read_recipe_name(self) -> int:
        name = input('Recipe name: ')
        if not name:
            return 0
        self._data_facade.set_name(name)
        return 1

    @return_0
    def read_recipe_desc(self):
        self._data_facade.set_desc(input('Recipe description: '))
