
class MealsCollection:

    def __init__(self) -> None:
        self.meals = {}
        self.next_available_id = 1
        self.nutrients = ['cal', 'sodium', 'sugar']
        self.courses = ['appetizer', 'main', 'dessert']

    def add_meal(self, meal_data: dict, dishes_data: dict) -> int:
        meal_id = self._get_next_id()
        self.update_meal_data(meal_data, dishes_data)
        meal_data['ID'] = meal_id
        self.meals[meal_id] = meal_data
        return meal_id

    def remove_meal(self, meal_name) -> None:
        for meal in self.meals.values():
            if meal['name'] == meal_name:
                self.meals.remove(meal)


    def meal_exists(self, meal_name: str) -> bool:
        return self.get_meal_id(meal_name) != -1
    
    def get_meal(self, meal_id: int) -> dict:
        return self.meals.get(meal_id, None)
    
    def delete_meal(self, meal_id: int) -> int:
        if meal_id in self.meals.keys():
            del self.meals[meal_id]
            return meal_id
        return -1
    
    def get_meal_id(self, meal_name: str) -> int:
        for meal_id, meal in self.meals.items():
            if meal['name'] == meal_name:
                return meal_id
        return -1
    
    def update_meal(self, meal_id: int, meal: dict, dishes_data: dict) -> None:
        for key in meal.keys():
            self.meals[meal_id][key] = meal[key]
        self.update_meal_data(self.meals[meal_id], dishes_data)

    def _reset_nutrients(self, meal: dict) -> None:
        for nutrient in self.nutrients:
            meal[nutrient] = 0

    def _get_next_id(self) -> int:
        self.next_available_id += 1
        return self.next_available_id - 1

    def update_meal_data(self, meal_data: dict, dishes_data: dict) -> None:
        dish_ids = [meal_data[key] for key in meal_data.keys() if key in self.courses] # to make sure i only take the dish ids
        self._reset_nutrients(meal_data)
        for dish_id in dish_ids:
            for nutrient in self.nutrients:
                meal_data[nutrient] = meal_data.get(nutrient, 0) + dishes_data[dish_id][nutrient]

    def reset_meal(self, meal: dict) -> None:
        for nutrient in self.nutrients:
            meal[nutrient] = None


                

        
