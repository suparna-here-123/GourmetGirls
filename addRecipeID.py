import json
from random import choice

recipes = json.loads(open('recipes.json').read())

users = ['General', 'suparna@123', 'aditi@456', 'chefMaster', 'gordon@ramsay', 
         'tArLaDaLaL', 'yumCook123', 'food4lyf', 'burpista@89', 
         'foodLover123', 'kaapiLover57', 'delishrelish564', 'marcoPierre',
          'g0rgeMehigan', 'sanjayKapoor2004', 'sihikahi34', 'emptyPlate45', 
          'I<3Food', 'gourmetGal', 'remy&Linguini']

sources = ['General', 'suparna@123', 'tArLaDaLaL', 'foodLover123', 'g0rgeMehigan', 'I<3Food']

# Adding recipe ID and source
for i, recipe in enumerate(recipes) :
    recipes[i]['RecipeID'] = f'R_{i}'
    recipes[i]['source'] = choice(sources)

with open('modifiedRecipes.json', 'w') as f :
    f.write(json.dumps(recipes, indent=3))