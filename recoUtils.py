'''
Rule-based recipe recommendation engine based on that user's recipe corpus

'''

import json, pickle

# Load recipes
with open("data/recipes.json") as f:
    recipes = json.load(f)

# Scoring parameters
dairy_bonus_value = 10
cuisine_bonus_value = 5
course_bonus_value = 5

def getCuisines() :
    return ('Asian', 'Chinese', 'Continental', 'Indian', 'Fusion')


def getUsers() :
    return ('suparna@123', 'aditi@456', 'chefMaster', 'gordon@ramsay', 
            'tArLaDaLaL', 'yumCook123', 'food4lyf', 'burpista@89', 
            'foodLover123', 'kaapiLover57', 'delishrelish564', 'marcoPierre',
            'g0rgeMehigan', 'sanjayKapoor2004', 'sihikahi34', 'emptyPlate45', 
            'I<3Food', 'gourmetGal', 'remy&Linguini')


def scoreRecipes(numPpl:int, user_cuisine:str, user_course:int, user_allergens:list,
                 maxPrepTime:int, user_non_dairy:dict, user_dairy:list) :
    scored_recipes = []

    for recipe in recipes:
        # --- Allergens Filter ---
        if any(allergen in user_allergens for allergen in recipe.get("allergens", [])):
            continue
        
        # Prep-time filter
        if maxPrepTime < int(recipe["Prep time"].split()[0]):
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
        dairy_bonus = dairy_bonus_value if user_dairy and recipe.get("dairy ingredients") else 0

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
def topKRecipes(K, recipes) :
    top_k_recipes = sorted(recipes, key=lambda x: x["total_score"], reverse=True)[:K]
    return top_k_recipes

# -- Recommend new recipes for user
def getRecos(user_id : str, n : int) :
    with open('/home/suppra/Desktop/GourmetGirls/models/svd_model_17.pkl', 'rb') as f:
        algo = pickle.load(f)

    with open('/home/suppra/Desktop/GourmetGirls/models/trainset_17.pkl', 'rb') as f:
        trainset = pickle.load(f)
    
    all_items = trainset.all_items()
    # Convert internal surprise-assigned itemIDs back to what I gave
    all_items_raw = [trainset.to_raw_iid(iid) for iid in all_items]

    # Get items the user has already interacted with
    user_inner_id = trainset.to_inner_uid(user_id)
    items_user_has_rated = set([j for (j, _) in trainset.ur[user_inner_id]])

    # Recommend items the user hasn't rated
    items_to_predict = [iid for iid in all_items if iid not in items_user_has_rated]

    # Predict ratings
    predictions = [
        (trainset.to_raw_iid(iid), algo.predict(user_id, trainset.to_raw_iid(iid)).est)
        for iid in items_to_predict
    ]

    # Sort by predicted rating
    predictions.sort(key=lambda x: x[1], reverse=True)

    # Top-N Recommendations
    top_n = predictions[:n]
    return matchRecos(top_n)

# Matching passed recipes IDs to their full description
def matchRecos(recosList : list) :
    toSend = []
    for r_id, score in recosList :
        # Find this recipe's details
        recipeDesc = recipes[r_id]
        score = min(100, score * 100)
        toSend.append((score, recipeDesc))
    return toSend

if __name__ == "__main__" :
    # input = json.loads(open('data/inputs.json').read())
    # sr = scoreRecipes(input['numPpl'], input['userCuisine'], input['userCourse'],
    #                    input['userAllergens'], input['maxPrepTime'], input['Non-dairy ingredients'],
    #                    input['dairy ingredients'])
    
    # topK = topKRecipes(5, sr)
    
    # # --- Present Results ---
    # print("\nTop 5 Recommended Recipes:\n")
    # for i, r in enumerate(topK, 1):
    #     print(f"#{i}: {r['recipe']} (Score: {r['total_score']:.2f})")
    #     print(f"   Cuisine: {r['cuisine']}, Course: {r['course']}, Prep Time: {r['prep_time']}, Servings: {r['servings']}")
    #     print(f"   Recipe: {r['full_recipe']}")
    #     print(f"   Ingredient match score: {r['ingredient_match_score']}\n")
    print(getRecos('suparna@123', 10))