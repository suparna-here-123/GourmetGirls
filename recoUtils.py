'''
Rule-based recipe recommendation engine based on that user's recipe corpus

'''

import json

# Load recipes
with open("recipes.json") as f:
    recipes = json.load(f)

# Load user inputs
with open("inputs.json") as f:
    inputs = json.load(f)

# Extract user input details
num_ppl = inputs["numPpl"]
user_cuisine = inputs["userCuisine"]
user_course = inputs["userCourse"]
user_allergens = set([a.strip() for a in inputs["userAllergens"].split(",") if a.strip()])
user_non_dairy = inputs["Non-dairy ingredients"]
user_dairy = inputs["dairy ingredients"]
has_dairy = bool(user_dairy)

# Scoring parameters
dairy_bonus_value = 10
cuisine_bonus_value = 5
course_bonus_value = 5

def getCuisines() :
    return ('Asian', 'Chinese', 'Continental', 'Indian', 'Fusion')


def scoreRecipes() :
    scored_recipes = []

    for recipe in recipes:
        
        # --- Allergens Filter ---
        if any(allergen in user_allergens for allergen in recipe.get("allergens", [])):
            continue
        
        # --- Ingredient Match ---
        total_ingredients = len(recipe.get("Non-dairy ingredients", {})) + len(recipe.get("dairy ingredients", {}))
        if total_ingredients == 0:
            continue  # skip weird empty recipes

        sufficiency_sum = 0

        # Non-dairy matching
        for ingredient, required_qty in recipe.get("Non-dairy ingredients", {}).items():
            available_qty = user_non_dairy.get(ingredient, 0)
            sufficiency_sum += min(available_qty / required_qty, 1)

        # Dairy matching
        for ingredient, required_qty in recipe.get("dairy ingredients", {}).items():
            available_qty = user_dairy.get(ingredient, 0)
            sufficiency_sum += min(available_qty / required_qty, 1)

        ingredient_match_score = (sufficiency_sum / total_ingredients) * 100
        if not (ingredient_match_score >= 50) :
            continue

        # --- Dairy Bonus ---
        dairy_bonus = dairy_bonus_value if has_dairy and recipe.get("dairy ingredients") else 0

        # --- Cuisine Bonus ---
        cuisine_bonus = cuisine_bonus_value if user_cuisine == "Any" or recipe.get("Cuisine") == user_cuisine else 0

        # --- Course Bonus ---
        course_bonus = course_bonus_value if user_course == "Any" or recipe.get("Course") == user_course else 0

        # --- Final Score ---
        final_score = ingredient_match_score + dairy_bonus + cuisine_bonus + course_bonus

        scored_recipes.append({
            "recipe": recipe["Name"],
            "total_score": final_score,
            "ingredient_match_score" : ingredient_match_score,
            "cuisine": recipe.get("Cuisine"),
            "course": recipe.get("Course"),
            "matched_ingredients": sufficiency_sum,
            "prep_time": recipe.get("Prep time"),
            "servings": recipe.get("servings"),
            "full_recipe": recipe["recipe"]
        })

        return scored_recipes

# --- Get Top 5 Recipes ---
def topKRecipes(K) :
    scoredRecipes = scoreRecipes()
    top_k_recipes = sorted(scoredRecipes, key=lambda x: x["total_score"], reverse=True)[:K]
    return top_k_recipes



# --- Present Results ---
# print("\nTop 5 Recommended Recipes:\n")
# for i, r in enumerate(top_5_recipes, 1):
#     print(f"#{i}: {r['recipe']} (Score: {r['total_score']:.2f})")
#     print(f"   Cuisine: {r['cuisine']}, Course: {r['course']}, Prep Time: {r['prep_time']}, Servings: {r['servings']}")
#     print(f"   Recipe: {r['full_recipe']}")
#     print(f"   Ingredient match score: {r['ingredient_match_score']}\n")
