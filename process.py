import pandas as pd

data = pd.read_csv('RAW_recipes.csv').values.tolist()


def filter_by_ingredients(available_ingredients):
    can_make = []

    for recipe in data:
        recipe_ingredients = map(lambda x: x.strip("'"), recipe[10].strip('][').split(', '))

        if all(map(lambda x: x in available_ingredients, recipe_ingredients)):
            can_make.append(recipe)

    return can_make


results = filter_by_ingredients(
    ['all-purpose flour', 'flour', 'baking soda', 'baking powder', 'cocoa powder', 'butter', 'sugar', 'oil'])

print(list(map(lambda x: x[0], results)))
