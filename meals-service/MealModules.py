meal_keys = ['appetizer', 'main', 'dessert']
nutrients = ['cal', 'sodium', 'sugar']

def add_meal_data(meal_data: dict, dishes):
    meal_nutrients = {nutrient: 0 for nutrient in nutrients}

    for nutrient in meal_nutrients:
        meal_data[nutrient] = 0

    for meal_key in meal_keys:
        dish_id = meal_data[meal_key]
        dish = dishes.find_one({'ID': dish_id})

        if not dish:
            meal_data[meal_key] = None
            continue

        for nutrient in nutrients:
            meal_nutrients[nutrient] += dish[nutrient]
    
    meal_data.update(meal_nutrients)

def update_meals(meals, deleted_dish):

    for meal_key in meal_keys:
        query = {meal_key: deleted_dish['ID']}
        update = {'$set': {meal_key: None}, '$inc': {
        'cal': -deleted_dish['cal'],
        'sodium': -deleted_dish['sodium'],
        'sugar': -deleted_dish['sugar']
        }}
        meals.update_many(query, update)

    for nutrient in nutrients:
        meals.update_many({f'{nutrient}': {'$lt': 0.0001}}, {'$set': {f'{nutrient}': 0}})