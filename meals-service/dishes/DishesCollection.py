
class DishesCollection:
    def __init__(self, meals_collection) -> None:
        self.dishes = {}
        self.next_available_id = 1
        self.meals_collection = meals_collection

    def add_dish(self, dish_stats: dict) -> None:
        dish_id = self._get_next_id()
        dish_stats["ID"] = dish_id
        self.dishes[dish_id] = dish_stats
        return dish_id

    def dish_exists(self, dish_name: str) -> bool:
        return self.get_dish_id(dish_name) != -1

    def get_dish(self, dish_id: int) -> int:
        return self.dishes.get(dish_id, None)

    def delete_dish(self, dish_id: int) -> int:
        if dish_id in self.dishes.keys():
            self._update_meals(dish_id)
            del self.dishes[dish_id]
            return dish_id
        return -1

    def get_dish_id(self, dish_name: str) -> int:
        for id, dish in self.dishes.items():
            if dish["name"] == dish_name:
                return id
        return -1

    def _update_meals(self, dish_id: int) -> None:
        meals = self.meals_collection.meals.values()
        to_update = False
        for meal in meals:
            for key, value in meal.items():
                if value == dish_id and key != "ID":
                    meal[key] = None
                    to_update = True
            if to_update:
                self.meals_collection.reset_meal(meal)
                to_update = False
    
    def _get_next_id(self) -> int:
        self.next_available_id += 1
        return self.next_available_id - 1
