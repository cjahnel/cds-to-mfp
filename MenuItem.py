from typing import TypedDict

class MenuItem(TypedDict):
    name: str
    recipe_id: int
    amount_per_serving: str # e.g. 2.61 oz, 1 cup, 1 serving, 2 pieces
    calories: int
    calories_from_fat: int
    total_fat: int # g
    saturated_fat: int # g
    trans_fat: int # g
    cholesterol: int # mg
    sodium: int # mg
    total_carbohydrate: int # g
    dietary_fiber: int # g
    sugars: int # g
    protein: int # g
    calcium: int # %
    iron: int # %
    potassium: float # mg
    vitamin_d: int # %
